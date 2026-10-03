# -*- coding: utf-8 -*-
"""ix_score.py -- ADDENDUM_CF2_INTENT_CROSSOVER (program R121): score the crossover. NO MODEL CALL.

Reads the new rows (cf2/rows/rows_IX_{MINI,LUNA,H45,OP5}.jsonl) and the recorded CF-2 rows for P0 cells 1 and 2 (rows_MINI/H45/OP5
INDEXED-V2 for population A and INDEXED-V3 for B; rows_LUNA INDEXED-V2 for A; Opus 5's draw 1 for the primary reading and its
five-draw mean as the registered sensitivity row), collapses draws by the X4 rule (mean over >= 3 OK draws; a k = 1 lane its single
draw), and computes, per population, arm and reader (registration section 7):
  same-store intent discrimination  AUROC of cell 1 (y = 1) against cell 3 (y = 0); intervals by boot_cluster_single with the pair
                                    and with the persona as the cluster (1,000 draws, seed 42); W/T/L within pairs with the Wilson
                                    interval and the persona-clustered interval on the strict-win fraction
  interaction                       mean over pairs of [c1 - c2] - [c3 - c4], pair-resampled and persona-resampled intervals
  pooled                            AUROC of cell 1 against cells 2 to 4, both intervals
  P-I5                              cell 1 against cell 2 on the original questions, P1 minus P0, cf2_score.paired with g = pair / persona
  P-I4 (descriptive)                model under P1 minus the keyword-intent lookup, same-store and pooled, both intervals
and the three lookups (name; keyword-intent = name zeroed where a cue fires; oracle-intent = name zeroed on cells 3 and 4), the
question-length difference (e0_common.toks content tokens and characters, crossed minus original), the predictions P-I1 to P-I3 with
their registered texts, the per-draw census and the spend. Writes cf2/results/cf_scores_ix.json and appends ledger section 14d.
"""
from __future__ import annotations

import collections
import datetime as dt
import io
import json
import pathlib
import statistics as st
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("reviews/r121/tools", "e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "reviews/v19/tools", "reviews/v18/tools", "e0_metamemory/tools"):
    sys.path.insert(0, str(ROOT / p))
import ix_run as R  # noqa: E402  (asserts every frozen hash at setup)
import cue_list as CUES  # noqa: E402
from common_e1r import N_BOOT, SEED, auroc, boot_cluster, boot_cluster_single, _summarise  # noqa: E402
from index_v3 import named_sections  # noqa: E402
import score_cf as S  # noqa: E402
from cf2_score import paired  # noqa: E402
from posthoc_b_pnpresent import boot_fraction_cluster  # noqa: E402
from wilson_a7 import load_wilson  # noqa: E402
from e0_common import toks  # noqa: E402

CF2 = R.CF2; ROWS = R.ROWS
OUT = CF2 / "results" / "cf_scores_ix.json"
TOL = 0.05
MIN_DRAWS = 3
READERS = ("MINI", "H45", "LUNA", "OP5", "SOL")          # SOL: Amendment 1 (one draw; recorded E5 draw 1 for P0 cells 1-2 on A; new on B)
NAMES = {"MINI": "GPT-4.1 mini", "H45": "Haiku 4.5", "LUNA": "GPT-5.6 Luna", "OP5": "Opus 5", "SOL": "GPT-5.6 Sol"}
RECORDED_CODE = {"MINI": "MINI", "H45": "H45", "LUNA": "LUNA", "OP5": "OP5", "SOL": "SOL"}
NO_V3 = ("LUNA", "SOL")                                   # no recorded all-states rows: P0 cells 1-2 on B are new calls
DRAW1 = ("OP5", "SOL")                                    # the one-draw-per-cell rule: the recorded draw 1 for P0 cells 1-2 on A


def r4(x):
    return None if x is None else round(float(x), 4)


# ------------------------------------------------------------------------------------------------ rows and collapses
def collapse_new(lane):
    """{unit_id: mean nok over >= MIN_DRAWS OK draws (or the single draw)} from rows_IX_<lane>.jsonl, with the census."""
    per = collections.defaultdict(dict); n_rows = n_bad = 0; usd = 0.0
    for line in io.open(R.rows_path(lane), encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line); n_rows += 1; usd += r.get("usd", 0.0)
        if r.get("status") == "OK" and r.get("nok") is not None:
            per[r["unit_id"]][int(r["draw"])] = float(r["nok"])
        else:
            n_bad += 1
    out = {u: float(np.mean(list(d.values()))) for u, d in per.items() if len(d) >= MIN_DRAWS or len(d) == 1}
    rng = [max(d.values()) - min(d.values()) for d in per.values() if len(d) >= 2]
    census = {"rows": n_rows, "not_ok": n_bad, "usd": round(usd, 4), "units": len(per), "units_collapsed": len(out),
              "draws_per_unit": dict(collections.Counter(len(d) for d in per.values())),
              "identical_across_draws": sum(1 for d in per.values() if len(d) >= 2 and len(set(d.values())) == 1), "median_range": r4(np.median(rng)) if rng else None}
    return out, census


def collapse_recorded(code, arm, draw_only=None):
    """{item_id: nok} from the recorded cf2 rows of one arm: the mean over >= 3 OK draws, or draw `draw_only` alone."""
    per = collections.defaultdict(dict)
    for line in io.open(ROWS / f"rows_{code}.jsonl", encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("arm") != arm or r.get("status") != "OK" or r.get("nok") is None:
            continue
        per[r["unit_id"]][int(r["draw"])] = float(r["nok"])
    if draw_only is not None:
        return {u: d[draw_only] for u, d in per.items() if draw_only in d}
    return {u: float(np.mean(list(d.values()))) for u, d in per.items() if len(d) >= MIN_DRAWS or len(d) == 1}


def scores_for(reader, units, sensitivity=False):
    """Score vector over `units` for one reader: new rows for the new cells, the recorded rows for P0 cells 1 and 2."""
    new, _ = collapse_new(reader)
    rec = {}
    for pop, arm_key in (("A", "INDEXED-V2"), ("B", "INDEXED-V3")):
        if reader in NO_V3 and pop == "B":
            continue
        rec[pop] = collapse_recorded(RECORDED_CODE[reader], arm_key, draw_only=(None if (reader not in DRAW1 or sensitivity) else 1))
    v = []
    for u in units:
        if u["arm"] == "P0" and u["cell"] in (1, 2) and not (reader in NO_V3 and u["population"] == "B"):
            v.append(rec[u["population"]].get(f"{u['pair_id']}|{u['version']}", np.nan))
        else:
            v.append(new.get(u["unit_id"], np.nan))
    return np.array(v, float)


def scores_draw1(reader, units):
    """The one-draw analogue: draw 1 alone in every cell (new rows and the recorded rows), the comparable column beside the Sol and Opus lanes."""
    per = {}
    for line in io.open(R.rows_path(reader), encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("status") == "OK" and r.get("nok") is not None and int(r["draw"]) == 1:
            per[r["unit_id"]] = float(r["nok"])
    rec = {}
    for pop, arm_key in (("A", "INDEXED-V2"), ("B", "INDEXED-V3")):
        if reader in NO_V3 and pop == "B":
            continue
        rec[pop] = collapse_recorded(RECORDED_CODE[reader], arm_key, draw_only=1)
    v = []
    for u in units:
        if u["arm"] == "P0" and u["cell"] in (1, 2) and not (reader in NO_V3 and u["population"] == "B"):
            v.append(rec[u["population"]].get(f"{u['pair_id']}|{u['version']}", np.nan))
        else:
            v.append(per.get(u["unit_id"], np.nan))
    return np.array(v, float)


MULTI_DRAW = ("LUNA", "H45")


# ------------------------------------------------------------------------------------------------ lookups
_ENC = {}


def lookups(units):
    qs = [u["question"] for u in units]
    lists = []
    for u in units:
        sec = named_sections(u["index"])
        lists.append(sec["superseded"] if u["population"] == "A" else sec["superseded"] + sec["retracted"] + sec["expired"])
    name = np.asarray(S.matcher(qs, lists), float)
    cue = np.array([CUES.matches(q) for q in qs], bool)
    keyword = np.where(cue, 0.0, name)
    oracle = np.array([0.0 if u["cell"] in (3, 4) else s for u, s in zip(units, name)], float)
    return {"name": name, "keyword": keyword, "oracle": oracle, "cue_fired": cue}


# ------------------------------------------------------------------------------------------------ estimands
def boot_mean(x, g, n=N_BOOT, seed=SEED):
    rng = np.random.default_rng(seed); x, g = np.asarray(x, float), np.asarray(g)
    groups = np.unique(g); idx = {u: np.flatnonzero(g == u) for u in groups}
    d = []
    for _ in range(n):
        drawn = rng.integers(0, len(groups), len(groups))
        d.append(float(x[np.concatenate([idx[groups[t]] for t in drawn])].mean()))
    return _summarise(d)


def ci_half(v, y, g):
    """boot_cluster_single's interval, plus whether it excludes 0.50."""
    c = boot_cluster_single(v, y, g)
    c["excludes_half"] = bool(c.get("ci_lo", 0.5) > 0.5 or c.get("ci_hi", 0.5) < 0.5)
    return c


def estimands(v, units, wilson):
    """The primary and secondary estimands over the four cells of one population under one score vector."""
    pos = {(u["pair_id"], u["cell"]): k for k, u in enumerate(units)}
    pairs = sorted({u["pair_id"] for u in units}); persona = {u["pair_id"]: u["persona"] for u in units}
    c = {cell: np.array([v[pos[(p, cell)]] for p in pairs], float) for cell in (1, 2, 3, 4)}
    gp = np.array(pairs); gper = np.array([persona[p] for p in pairs])
    # same-store: cell 1 (1) vs cell 3 (0)
    ss_v = np.concatenate([c[1], c[3]]); ss_y = np.concatenate([np.ones(len(pairs)), np.zeros(len(pairs))]).astype(int)
    ss_gp = np.concatenate([gp, gp]); ss_gper = np.concatenate([gper, gper])
    wins = (c[1] > c[3]).astype(float); ties = (c[1] == c[3]).astype(float)
    W, T = int(wins.sum()), int(ties.sum()); wl = wilson(W, len(pairs))
    same = {"auroc": r4(auroc(ss_v, ss_y)), "ci_pair": ci_half(ss_v, ss_y, ss_gp), "ci_persona": ci_half(ss_v, ss_y, ss_gper),
            "wtl": [W, T, len(pairs) - W - T], "strict_win_fraction": r4(W / len(pairs)), "win_wilson": [r4(wl[0]), r4(wl[1])], "win_ci_persona": boot_fraction_cluster(wins, gper),
            "within_tolerance_of_half": bool(abs(auroc(ss_v, ss_y) - 0.5) <= TOL)}
    # interaction
    inter = (c[1] - c[2]) - (c[3] - c[4])
    interaction = {"mean": r4(inter.mean()), "ci_pair": boot_mean(inter, gp), "ci_persona": boot_mean(inter, gper), "cell_means": {k: r4(c[k].mean()) for k in (1, 2, 3, 4)}}
    # pooled: cell 1 vs cells 2-4
    pv = np.concatenate([c[1], c[2], c[3], c[4]]); py = np.concatenate([np.ones(len(pairs)), np.zeros(3 * len(pairs))]).astype(int)
    pgp = np.concatenate([gp] * 4); pgper = np.concatenate([gper] * 4)
    pooled = {"auroc": r4(auroc(pv, py)), "ci_pair": ci_half(pv, py, pgp), "ci_persona": ci_half(pv, py, pgper)}
    # cells 1 vs 2 (the original task)
    ov = np.concatenate([c[1], c[2]]); oy = ss_y
    orig = {"auroc": r4(auroc(ov, oy)), "ci_persona": ci_half(ov, oy, ss_gper)}
    return {"n_pairs": len(pairs), "same_store": same, "interaction": interaction, "pooled": pooled, "cell1_vs_cell2": orig,
            "_vectors": {"same": (ss_v, ss_y, ss_gp, ss_gper), "pooled": (pv, py, pgp, pgper), "orig": (ov, oy, ss_gp, ss_gper)}}


def strip(e):
    return {k: v for k, v in e.items() if k != "_vectors"}


def qlen(units):
    """crossed minus original question length, content tokens (e0_common.toks) and characters, per pair."""
    by = {}
    for u in units:
        by.setdefault(u["pair_id"], {})[u["cell"]] = u["question"]
    dt_ = [len(toks(q[3])) - len(toks(q[1])) for q in by.values()]; dc = [len(q[3]) - len(q[1]) for q in by.values()]
    return {"tokens_mean_delta": r4(np.mean(dt_)), "chars_mean_delta": r4(np.mean(dc)), "tokens_original_mean": r4(np.mean([len(toks(q[1])) for q in by.values()])),
            "tokens_crossed_mean": r4(np.mean([len(toks(q[3])) for q in by.values()]))}


# ------------------------------------------------------------------------------------------------ main
def main():
    sys.stdout.reconfigure(encoding="utf-8")
    R.setup()
    U = R.units_all(); wilson = load_wilson()
    lock = json.load(io.open(R.LOCK, encoding="utf-8")); probes = json.load(io.open(R.PROBES, encoding="utf-8"))
    res = {"registration_sha256": R.REG_SHA, "frozen_at": R.FROZEN_AT, "lock": lock, "probes": probes, "tol": TOL, "n_boot": N_BOOT, "seed": SEED,
           "when": dt.datetime.now().isoformat(timespec="seconds"), "census": {}, "readers": {}, "lookups": {}, "predictions": {}, "spend": {}}
    for lane in READERS:
        _, res["census"][lane] = collapse_new(lane)
    L = {}
    for pop in ("A", "B"):
        units_p = {arm: [u for u in U if u["population"] == pop and u["arm"] == arm] for arm in ("P0", "P1")}
        # the lookups are arm-independent; computed on the P0 units (the same questions and summaries)
        lk = lookups(units_p["P0"])
        cue_share = {c: r4(np.mean([f for u, f in zip(units_p["P0"], lk["cue_fired"]) if u["cell"] == c])) for c in (1, 2, 3, 4)}
        L[pop] = {}
        for name in ("name", "keyword", "oracle"):
            e = estimands(lk[name], units_p["P0"], wilson); L[pop][name] = e
            res["lookups"].setdefault(pop, {})[name] = strip(e)
        res["lookups"][pop]["cue_fired_share_by_cell"] = cue_share
        res["lookups"][pop]["question_length"] = qlen(units_p["P0"])
        for lane in READERS:
            rd = res["readers"].setdefault(lane, {"name": NAMES[lane]})
            rd[pop] = {}
            vec = {}
            for arm in ("P0", "P1"):
                v = scores_for(lane, units_p[arm]); missing = int(np.isnan(v).sum())
                assert missing == 0, (lane, pop, arm, "missing collapsed scores", missing)
                e = estimands(v, units_p[arm], wilson); vec[arm] = e
                rd[pop][arm] = strip(e)
                if lane in MULTI_DRAW:
                    v1 = scores_draw1(lane, units_p[arm]); assert not np.isnan(v1).any(), (lane, pop, arm, "draw 1")
                    e1 = estimands(v1, units_p[arm], wilson); vec[arm + "_draw1"] = e1; rd[pop][arm]["draw1"] = strip(e1)
                # P-I4 descriptive: model under P1 minus the keyword-intent lookup, same-store and pooled (the same items)
                if arm == "P1":
                    for est in ("same", "pooled"):
                        mv, my, mgp, mgper = e["_vectors"][est]; kv = L[pop]["keyword"]["_vectors"][est][0]
                        rd[pop][arm][f"vs_keyword_{est}"] = {"delta": r4(auroc(mv, my) - auroc(kv, my)), "ci_pair": boot_cluster(kv, mv, my, mgp), "ci_persona": boot_cluster(kv, mv, my, mgper)}
                        rd[pop][arm][f"vs_keyword_{est}"]["both_exclude_zero"] = bool(rd[pop][arm][f"vs_keyword_{est}"]["ci_pair"].get("excludes_zero") and rd[pop][arm][f"vs_keyword_{est}"]["ci_persona"].get("excludes_zero"))
            # P-I5: cells 1 vs 2 on the original questions, P1 minus P0
            b = vec["P0"]["_vectors"]["orig"]; i = vec["P1"]["_vectors"]["orig"]
            rd[pop]["p1_minus_p0_cell1_vs_cell2"] = {"p0": vec["P0"]["cell1_vs_cell2"]["auroc"], "p1": vec["P1"]["cell1_vs_cell2"]["auroc"], "delta": r4(auroc(i[0], i[1]) - auroc(b[0], b[1])),
                                                    "ci_pair": boot_cluster(b[0], i[0], b[1], b[2]), "ci_persona": boot_cluster(b[0], i[0], b[1], b[3])}
            if lane in MULTI_DRAW:
                b1 = vec["P0_draw1"]["_vectors"]["orig"]; i1 = vec["P1_draw1"]["_vectors"]["orig"]
                rd[pop]["p1_minus_p0_cell1_vs_cell2"]["draw1"] = {"p0": vec["P0_draw1"]["cell1_vs_cell2"]["auroc"], "p1": vec["P1_draw1"]["cell1_vs_cell2"]["auroc"], "delta": r4(auroc(i1[0], i1[1]) - auroc(b1[0], b1[1]))}
            if lane == "SOL" and pop == "A":
                # the author's correction (14d-interim-3): the pairs Sol loses under P1, and how many have both questions at 0.96 or higher
                pos = {(u["pair_id"], u["cell"]): k for k, u in enumerate(units_p["P1"])}; v = vec["P1"]["_vectors"]
                sv = scores_for("SOL", units_p["P1"]); losses = []
                for pid in sorted({u["pair_id"] for u in units_p["P1"]}):
                    s1, s3 = float(sv[pos[(pid, 1)]]), float(sv[pos[(pid, 3)]])
                    if s1 < s3:
                        losses.append({"pair_id": pid, "nok_cell1": r4(s1), "nok_cell3": r4(s3), "both_at_least_0_96": bool(s1 >= 0.96 and s3 >= 0.96),
                                       "original": units_p["P1"][pos[(pid, 1)]]["question"], "crossed": units_p["P1"][pos[(pid, 3)]]["question"]})
                rd[pop]["sol_losses_P1"] = {"n": len(losses), "n_both_at_least_0_96": sum(l["both_at_least_0_96"] for l in losses), "wtl": vec["P1"]["same_store"]["wtl"], "losses": losses,
                                           "reading": "a CHANGE question licenses the old value, so a correct reading is low; the pairs with both questions at 0.96 or higher are failures to apply the intent rule (the author, 2026-09-19)"}
            if lane in DRAW1 and not (lane in NO_V3 and pop == "B"):
                v5 = scores_for(lane, units_p["P0"], sensitivity=True)
                rd[pop]["P0_sensitivity_five_draw_cells12"] = strip(estimands(v5, units_p["P0"], wilson))
    # predictions
    P = res["predictions"]
    fails = [(lane, res["readers"][lane]["A"]["P0"]["same_store"]["auroc"]) for lane in READERS if not res["readers"][lane]["A"]["P0"]["same_store"]["within_tolerance_of_half"]]
    P["P-I1"] = {"holds": not fails, "readings": {lane: res["readers"][lane]["A"]["P0"]["same_store"]["auroc"] for lane in READERS},
                 "text": ("P-I1 HOLDS: under the frozen rubric every model's same-store intent discrimination on population A is within tolerance of 0.50 (" + ", ".join(f"{NAMES[l]} {res['readers'][l]['A']['P0']['same_store']['auroc']:.4f}" for l in READERS) + ")."
                          if not fails else " ".join(f"P-I1 FAILS: under the frozen rubric {NAMES[l]} reads {a:.4f} on population A, outside the band [0.45, 0.55]." for l, a in fails))}
    i2 = {}
    for lane in ("OP5", "H45"):
        s_ = res["readers"][lane]["A"]["P1"]["same_store"]
        i2[lane] = {"auroc": s_["auroc"], "ci_pair": [r4(s_["ci_pair"]["ci_lo"]), r4(s_["ci_pair"]["ci_hi"])], "ci_persona": [r4(s_["ci_persona"]["ci_lo"]), r4(s_["ci_persona"]["ci_hi"])],
                    "separates": bool(s_["auroc"] > 0.5 and s_["ci_pair"]["ci_lo"] > 0.5 and s_["ci_persona"]["ci_lo"] > 0.5)}
    P["P-I2"] = {"holds": all(x["separates"] for x in i2.values()), "readings": i2,
                 "text": ("P-I2 HOLDS: told that the obligation depends on the question, Opus 5 and Haiku 4.5 separate the intents on population A (" + ", ".join(f"{NAMES[l]} {x['auroc']:.4f} [{x['ci_pair'][0]:.4f}, {x['ci_pair'][1]:.4f}] [{x['ci_persona'][0]:.4f}, {x['ci_persona'][1]:.4f}]" for l, x in i2.items()) + "), both intervals excluding 0.50."
                          if all(x["separates"] for x in i2.values()) else " ".join(f"P-I2 FAILS: told that the obligation depends on the question, {NAMES[l]} reads {x['auroc']:.4f} with intervals [{x['ci_pair'][0]:.4f}, {x['ci_pair'][1]:.4f}] and [{x['ci_persona'][0]:.4f}, {x['ci_persona'][1]:.4f}]." for l, x in i2.items() if not x["separates"]))}
    s_ = res["readers"]["SOL"]["A"]["P1"]["same_store"]
    sep = bool(s_["auroc"] > 0.5 and s_["ci_pair"]["ci_lo"] > 0.5 and s_["ci_persona"]["ci_lo"] > 0.5)
    P["P-I2b"] = {"holds": sep, "made_after_interim_read": True, "reading": {"auroc": s_["auroc"], "ci_pair": [r4(s_["ci_pair"]["ci_lo"]), r4(s_["ci_pair"]["ci_hi"])], "ci_persona": [r4(s_["ci_persona"]["ci_lo"]), r4(s_["ci_persona"]["ci_hi"])]},
                  "text": (f"P-I2b HOLDS (a prediction made after the interim read of three lanes): told that the obligation depends on the question, GPT-5.6 Sol separates the intents on population A, {s_['auroc']:.4f} with intervals [{s_['ci_pair']['ci_lo']:.4f}, {s_['ci_pair']['ci_hi']:.4f}] and [{s_['ci_persona']['ci_lo']:.4f}, {s_['ci_persona']['ci_hi']:.4f}], both excluding 0.50."
                           if sep else f"P-I2b FAILS (a prediction made after the interim read of three lanes): told that the obligation depends on the question, GPT-5.6 Sol reads {s_['auroc']:.4f} on population A with intervals [{s_['ci_pair']['ci_lo']:.4f}, {s_['ci_pair']['ci_hi']:.4f}] and [{s_['ci_persona']['ci_lo']:.4f}, {s_['ci_persona']['ci_hi']:.4f}].")}
    i3 = {pop: res["lookups"][pop]["name"]["same_store"] for pop in ("A", "B")}
    fails3 = [pop for pop in ("A", "B") if not i3[pop]["within_tolerance_of_half"]]
    P["P-I3"] = {"holds": not fails3, "readings": {pop: i3[pop]["auroc"] for pop in i3}, "question_length": {pop: res["lookups"][pop]["question_length"] for pop in ("A", "B")},
                 "text": (f"P-I3 HOLDS: the name lookup reads {i3['A']['auroc']:.4f} on population A and {i3['B']['auroc']:.4f} on population B, within tolerance of 0.50."
                          if not fails3 else " ".join(f"P-I3 FAILS: the name lookup reads {i3[pop]['auroc']:.4f} on population {pop}; the crossed questions are {res['lookups'][pop]['question_length']['tokens_mean_delta']:+.2f} content tokens longer than the originals on average, and dilution of the cosine by the longer wording, not intent, is the likely reason." for pop in fails3))}
    P["P-I4"] = {"descriptive": True, "readings": {lane: {pop: {est: res["readers"][lane][pop]["P1"][f"vs_keyword_{est}"]["delta"] for est in ("same", "pooled")} for pop in ("A", "B")} for lane in READERS},
                 "keyword_lookup": {pop: {"same_store": res["lookups"][pop]["keyword"]["same_store"]["auroc"], "pooled": res["lookups"][pop]["keyword"]["pooled"]["auroc"]} for pop in ("A", "B")}}
    i5 = {lane: {pop: res["readers"][lane][pop]["p1_minus_p0_cell1_vs_cell2"]["delta"] for pop in ("A", "B")} for lane in READERS}
    P["P-I5"] = {"descriptive": True, "readings": i5, "no_model_lowered_by_more_than_tol": bool(all(d >= -TOL for x in i5.values() for d in x.values()))}
    # spend
    sp = {lane: round(res["census"][lane]["usd"], 4) for lane in READERS}
    sp["probes"] = {lane: probes[lane]["usd"] for lane in READERS}
    sp["anthropic"] = round(sp["H45"] + sp["OP5"] + probes["H45"]["usd"] + probes["OP5"]["usd"], 4)
    sp["openai_run"] = round(sp["MINI"] + sp["LUNA"] + probes["MINI"]["usd"] + probes["LUNA"]["usd"], 4)
    sp["openai_with_phase1"] = round(sp["openai_run"] + R.PHASE1_OPENAI, 4); sp["caps"] = R.CAP
    sp["sol_amend1"] = round(sp["SOL"] + probes["SOL"]["usd"], 4); sp["sol_cap"] = R.LANE_CAP["SOL"]
    res["amendment_1"] = {"sha256": R.AMEND1_SHA, "lock": json.load(io.open(R.ROWS / "lock_ix_amend1.json", encoding="utf-8"))}
    res["spend"] = sp
    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1, sort_keys=True, default=float) + "\n")
    print(f"-> {OUT.relative_to(ROOT)}")
    for k in ("P-I1", "P-I2", "P-I2b", "P-I3"):
        print(k, P[k]["text"])
    print("P-I4", json.dumps(P["P-I4"]["readings"])); print("P-I5", json.dumps(i5), "none below -0.05:", P["P-I5"]["no_model_lowered_by_more_than_tol"])
    print("spend", json.dumps(sp))
    return res


if __name__ == "__main__":
    main()
