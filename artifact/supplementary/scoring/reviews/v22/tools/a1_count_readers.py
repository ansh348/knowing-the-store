# -*- coding: utf-8 -*-
"""a1_count_readers.py -- CC_PASS_v18 A1: count readers on the counterfactual set (444) and, secondarily, the 661.
NO MODEL CALL. $0. Every input is a recorded artifact; frozen lane code is imported, never edited.

Readers (the tally parsed with index_features.parse, the function NB-1 uses):
  CR-oracle (a)  RETRACT + EXPIRED at the target attribute's manifest category (cf_pairs_cf2.json pairs[].category);
  CR-oracle (b)  SUPRSD + RETRACT + EXPIRED at that category;
  CR-oracle-share  (SUPRSD+RETRACT+EXPIRED)/ENTRIES at that category (NB-1's share at the oracle category; extra);
  CR-totals (a)  the LIFECYCLE TOTALS retracted + expired lines (index_v2r.counts_of), the two fields v2r permutes;
  CR-totals (b)  the same plus the superseded total;
  CR-nb1         NB-1 exactly (index_features.assign_category, then (suprsd+retract+expired)/entries), on the cf text.
  CR-oracle-state  the state's own cell (RETRACT for a retraction pair, EXPIRED for an expiry pair, SUPRSD for a
                 supersession pair) at the oracle category: a reader that knows the question's state as well as its
                 category, the upper bound of any tally reader (extra; 444 only).

The v2r reading. v2r's derangement moves every position together (one rotation of a shuffled line of value groups), so a
single seed's CR-totals AUROC scatters widely around chance; the script therefore also prints CR-totals under 200
derangement seeds and 200 uniform permutations of the same totals. v2r counts as broken only if CR-totals keeps a
positive signal under the recorded seed (above 0.55 on a counted state) or the derangement's expectation over seeds is
not at chance. The base-count census (how many counted-state pairs have a category base count of 0, so the PN version
reads 1 against 0 within its triple) is printed beside the CR-oracle rows.

The author's ruling of 2026-09-14 (recorded in the plan): CR-oracle reads the per-category tallies, which v2r does not
touch (index_v2r.py:19-21, AUX-CF2-V2R-DEF), so it holds under v2r by construction; CR-totals is the reader that must
fall to chance under v2r, and if it does not, v2r is broken and the session stops. On the 661 no category source is
mixed across labels: CR-oracle runs only on items that carry a gold category (n dropped printed by label) and CR-nb1
runs on all 661. The 444 is the primary population; the 661 row is secondary.

Estimators: common_e1r (Mann-Whitney AUROC, ties 0.5; item-level and persona-clustered bootstraps, 1000 draws, seed 42);
paired differences through cf2_score.paired (delta = model minus reader; both intervals; the weaker governs).
Per-state convention: on the 444 within the state's own items (cf2_score); on the 661 positives of one state against
all negatives (Table 34's convention).

Reproduction gates (stop on mismatch): NB6 superseded-names lookup on v2 = 0.7663 (AUX-CF2-NB6-V2); NB-1 on the 661
under TRUE = 0.5514 (e1r_robustness/results/baselines.json); the three models' recorded v2 rows.

Usage: python reviews/v18/tools/a1_count_readers.py
Writes: reviews/v18/results/a1_count_readers.json
"""
from __future__ import annotations

import io
import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "resp_review/tools", "ds_downstream/tools", "r74/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from common_e1r import N_BOOT, SEED, auroc, boot_cluster_single, _summarise  # noqa: E402
from index_features import assign_category, index_key, indexes, parse  # noqa: E402
from index_v2r import counts_of  # noqa: E402
from index_v3 import named_sections  # noqa: E402
import score_cf as S  # noqa: E402
from cf2_score import paired  # noqa: E402  (sets S.R82 = cf2 at import)

CF2 = ROOT / "r82_counterfactual" / "cf2"
OUT = ROOT / "reviews" / "v18" / "results" / "a1_count_readers.json"
LANES = {"MINI": "gpt-4.1-mini", "H45": "claude-haiku-4-5-20251001", "OP5": "claude-opus-5"}
ARMS = (("INDEXED-V2", "v2"), ("INDEXED-V3", "v3"), ("INDEXED-V2R", "v2r"))
STATES = ("SUPERSESSION", "RETRACTION", "EXPIRY")
GATES = {"lookup_v2": 0.7663, "nb1_661_true": 0.5514, "mini_v2": 0.7167, "h45_v2": 0.7566, "op5_v2": 0.8405}
CHANCE_TOL = 0.05


def boot_item_single(s, y, n=N_BOOT, seed=SEED):
    """Item-level bootstrap for a single-arm AUROC, the same draw discipline as common_e1r.boot_item."""
    rng = np.random.default_rng(seed)
    s, y = np.asarray(s, float), np.asarray(y, int)
    d = []
    for _ in range(n):
        k = rng.integers(0, len(y), len(y))
        if y[k].sum() in (0, len(k)):
            continue
        d.append(auroc(s[k], y[k]))
    return _summarise(d)


def r4(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)


def single(s, y, g):
    return {"auroc": r4(auroc(s, y)), "item_ci": boot_item_single(s, y), "persona_ci": boot_cluster_single(s, y, g)}


def cat_cells(parsed, cat):
    c = parsed["categories"].get(cat)
    if not c:
        return None
    return {k: int(c.get(k, 0) or 0) for k in ("entries", "active", "suprsd", "retract", "expired")}


def reader_scores(text, question, cat, state=None):
    """-> dict reader -> score for one (summary text, question, oracle category[, state])."""
    p = parse(text)
    cc = cat_cells(p, cat) if cat else None
    ret_tot, exp_tot = counts_of(text)
    m = None
    for lab in ("superseded",):
        for ln in text.split("\n"):
            if ln.startswith(f"  {lab:<22s}"):
                m = int(ln[24:].strip()); break
    a_cat, _, _, _ = assign_category(p, question)
    ac = cat_cells(p, a_cat) if a_cat else None
    return {
        "CR-oracle-a": float(cc["retract"] + cc["expired"]) if cc else 0.0,
        "CR-oracle-b": float(cc["suprsd"] + cc["retract"] + cc["expired"]) if cc else 0.0,
        "CR-oracle-share": (float(cc["suprsd"] + cc["retract"] + cc["expired"]) / max(1, cc["entries"])) if cc else 0.0,
        "CR-totals-a": float(ret_tot + exp_tot),
        "CR-totals-b": float(ret_tot + exp_tot + (m or 0)),
        "CR-nb1": (float(ac["suprsd"] + ac["retract"] + ac["expired"]) / max(1, ac["entries"])) if ac else 0.0,
        "CR-oracle-state": (float(cc[{"RETRACTION": "retract", "EXPIRY": "expired", "SUPERSESSION": "suprsd"}[state]]) if (cc and state) else 0.0),
        "_cat_row_present": cc is not None, "_nb1_cat": a_cat,
    }


def at_chance(res):
    a = res["auroc"]; lo, hi = res["item_ci"].get("ci_lo"), res["item_ci"].get("ci_hi")
    return bool(a is not None and abs(a - 0.5) <= CHANCE_TOL and (lo is None or (lo <= 0.5 <= hi)))


# ---------------------------------------------------------------- the 444 (primary)
def run_444(res):
    cell = json.load(io.open(CF2 / "cf_cell.json", encoding="utf-8")); items = cell["items"]
    pairs = {p["pair_id"]: p for p in json.load(io.open(CF2 / "cf_pairs_cf2.json", encoding="utf-8"))["pairs"]}
    idx = json.load(io.open(CF2 / "cf_indexes.json", encoding="utf-8"))["indexes"]
    y = np.array([it["y_nok"] for it in items], int); g = np.array([it["persona"] for it in items])
    st = np.array([it["state"] for it in items]); qs = [it["question"] for it in items]
    cats = [pairs[it["pair_id"]]["category"] for it in items]
    assert len(items) == 444 and int(y.sum()) == 148

    # gate: the recorded lookup on v2
    sup2 = [named_sections(idx[it["item_id"]]["v2"])["superseded"] for it in items]
    look = S.matcher(qs, sup2); lk = r4(auroc(look, y))
    assert lk == GATES["lookup_v2"], f"GATE: lookup v2 {lk} != {GATES['lookup_v2']}"
    res["gates"]["lookup_v2"] = lk

    # models, collapsed by the recorded rule
    lanes = {}
    for code in LANES:
        lane = S.load_lane(code)
        if not lane:
            continue
        arms = {}
        for arm, tag in ARMS:
            v = np.array([lane.get((it["item_id"], arm), np.nan) for it in items])
            if not np.isnan(v).any():
                arms[tag] = v
        lanes[code] = arms
    for code, key in (("MINI", "mini_v2"), ("H45", "h45_v2"), ("OP5", "op5_v2")):
        got = r4(auroc(lanes[code]["v2"], y)); assert got == GATES[key], f"GATE: {code} v2 {got} != {GATES[key]}"; res["gates"][key] = got

    readers = ("CR-oracle-a", "CR-oracle-b", "CR-oracle-share", "CR-oracle-state", "CR-totals-a", "CR-totals-b", "CR-nb1")
    out = {"n": 444, "pos": 148, "per_state_convention": "within the state's own items (cf2_score)", "summaries": {}}
    # base-count census: counted-state pairs whose category base count (ABSENT version, v2) is 0
    census = {"RETRACTION": {"base_zero": 0, "base_nonzero": 0}, "EXPIRY": {"base_zero": 0, "base_nonzero": 0}}
    for k, it in enumerate(items):
        if it["version"] == "ABSENT" and it["state"] in census:
            c = cat_cells(parse(idx[it["item_id"]]["v2"]), cats[k]) or {}
            b = c.get("retract" if it["state"] == "RETRACTION" else "expired", 0)
            census[it["state"]]["base_zero" if b == 0 else "base_nonzero"] += 1
    out["base_count_census"] = census
    scores = {}
    for tag in ("v2", "v3", "v2r"):
        sc = {r: np.zeros(len(items)) for r in readers}; missing = 0; nb1_assigned = 0
        for k, it in enumerate(items):
            d = reader_scores(idx[it["item_id"]][tag], it["question"], cats[k], it["state"])
            for r in readers:
                sc[r][k] = d[r]
            missing += 0 if d["_cat_row_present"] else 1; nb1_assigned += 1 if d["_nb1_cat"] else 0
        scores[tag] = sc
        block = {"category_row_missing": missing, "nb1_assigned_a_category": nb1_assigned, "readers": {}}
        for r in readers:
            row = {"whole": single(sc[r], y, g), "per_state": {}, "vs_models": {}}
            for s_ in STATES:
                m = st == s_
                row["per_state"][s_] = {"n": int(m.sum()), "pos": int(y[m].sum()), **single(sc[r][m], y[m], g[m])}
            for code, arms in lanes.items():
                if tag not in arms:
                    continue
                v = arms[tag]
                row["vs_models"][LANES[code]] = {"model_auroc": r4(auroc(v, y)), "whole": paired(sc[r], v, y, g),
                                                 "per_state": {s_: {"model": r4(auroc(v[st == s_], y[st == s_])), "reader": r4(auroc(sc[r][st == s_], y[st == s_])),
                                                                    **paired(sc[r][st == s_], v[st == s_], y[st == s_], g[st == s_])} for s_ in STATES}}
            block["readers"][r] = row
        out["summaries"][tag] = block

    # the v2r check (the author's redefinition): CR-totals must be at chance on retraction and expiry; CR-oracle equals v2
    chk = {}
    for r in ("CR-totals-a", "CR-totals-b"):
        chk[r] = {s_: {"v2": out["summaries"]["v2"]["readers"][r]["per_state"][s_]["auroc"], "v2r": out["summaries"]["v2r"]["readers"][r]["per_state"][s_]["auroc"],
                       "v2r_at_chance": at_chance(out["summaries"]["v2r"]["readers"][r]["per_state"][s_])} for s_ in ("RETRACTION", "EXPIRY")}
        chk[r]["whole"] = {"v2": out["summaries"]["v2"]["readers"][r]["whole"]["auroc"], "v2r": out["summaries"]["v2r"]["readers"][r]["whole"]["auroc"]}
    # the derangement's expectation: CR-totals-a under 200 derangement seeds and 200 uniform permutations of the true totals
    from index_v2r import derangement
    ct = json.load(io.open(CF2 / "cf_indexes.json", encoding="utf-8"))["meta"]["v2r"]["counts_true"]
    vals = [tuple(ct[it["item_id"]]) for it in items]; tt = np.array([a + b for a, b in vals], float)
    D, U = [], []
    for seed in range(200):
        pp, _ = derangement(vals, seed=seed); d = np.array([tt[pp[i]] for i in range(len(vals))])
        D.append([auroc(d[st == "RETRACTION"], y[st == "RETRACTION"]), auroc(d[st == "EXPIRY"], y[st == "EXPIRY"]), auroc(d, y)])
        q = np.random.default_rng(seed).permutation(len(vals)); u = tt[q]
        U.append([auroc(u[st == "RETRACTION"], y[st == "RETRACTION"]), auroc(u[st == "EXPIRY"], y[st == "EXPIRY"]), auroc(u, y)])
    D, U = np.array(D), np.array(U)
    sim = {}
    for name, M in (("derangement_200_seeds", D), ("uniform_permutation_200_seeds", U)):
        sim[name] = {k: {"mean": r4(M[:, j].mean()), "p2.5": r4(np.percentile(M[:, j], 2.5)), "p97.5": r4(np.percentile(M[:, j], 97.5))}
                     for j, k in enumerate(("RETRACTION", "EXPIRY", "whole"))}
    chk["CR-totals-a_expectation_over_seeds"] = sim
    rec = {s_: chk["CR-totals-a"][s_]["v2r"] for s_ in ("RETRACTION", "EXPIRY")}
    fell = all(rec[s_] <= 0.55 for s_ in rec)
    expect_chance = all(abs(sim["derangement_200_seeds"][s_]["mean"] - 0.5) <= CHANCE_TOL for s_ in ("RETRACTION", "EXPIRY"))
    totals_ok = fell and expect_chance
    chk["recorded_seed_reading"] = ("CR-totals falls past chance under the recorded seed 42 (%.4f / %.4f on retraction / expiry), inside the derangement's own "
                                    "spread over seeds; the totals carry no label information in expectation" % (rec["RETRACTION"], rec["EXPIRY"]))
    oracle_same = all(np.array_equal(scores["v2"][r], scores["v2r"][r]) for r in ("CR-oracle-a", "CR-oracle-b", "CR-oracle-share"))
    chk["CR-oracle_scores_identical_v2_v2r"] = bool(oracle_same)
    chk["v2r_permutes_only_the_totals_lines"] = "index_v2r.py:19-21; AUX-CF2-V2R-DEF (NUMBERS_CF2.md:263)"
    chk["verdict"] = ("v2r randomizes the totals: CR-totals fell on both counted states under the recorded seed and is at chance in expectation over seeds"
                      if totals_ok else "STOP: CR-totals keeps a positive signal under v2r or the derangement is not at chance in expectation; v2r is broken")
    out["v2r_check"] = chk

    # branch on CR-oracle (a) under v2, retraction and expiry
    ra = out["summaries"]["v2"]["readers"]["CR-oracle-a"]["per_state"]
    ret, exp = ra["RETRACTION"]["auroc"], ra["EXPIRY"]["auroc"]
    if ret >= 0.80 or exp >= 0.80:
        br = "B1"
    elif 0.60 <= ret < 0.80 and 0.60 <= exp < 0.80:
        br = "B2"
    elif ret < 0.60 and exp < 0.60:
        br = "B3"
    else:
        br = "MIXED"
    models = out["summaries"]["v2"]["readers"]["CR-oracle-a"]["vs_models"]
    lo = min(v["per_state"][s_]["model"] for v in models.values() for s_ in ("RETRACTION", "EXPIRY"))
    hi = max(v["per_state"][s_]["model"] for v in models.values() for s_ in ("RETRACTION", "EXPIRY"))
    # the author's note of 2026-09-14 on the Phase 1 report: "read weakly" is withdrawn; the paragraph and the abstract clause
    # state the numbers, and the state-aware reader is an upper bound that stays in C.2 with its definition.
    from decimal import Decimal, ROUND_HALF_UP
    two = lambda x: str(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))   # the paper's rounding rule (numeric_diff --round2)
    wording = (f"a reader that knows the question's category reads the retracted versions at {two(ret)} and the expired at {two(exp)}; "
               f"every model reads them at {two(lo)} to {two(hi)}")
    out["branch"] = {"reader": "CR-oracle-a under v2", "retraction": ret, "expiry": exp, "fires": br, "wording": wording,
                     "note": {"B1": "at or above 0.80 on at least one counted state; " + wording,
                              "B2": "between 0.60 and 0.80 on both counted states; the numbers are stated: " + wording,
                              "B3": "below 0.60 on both counted states; " + wording,
                              "MIXED": "one counted state at or above 0.60, the other below; " + wording}[br],
                     "state_aware_upper_bound": {"retraction": out["summaries"]["v2"]["readers"]["CR-oracle-state"]["per_state"]["RETRACTION"]["auroc"],
                                                 "expiry": out["summaries"]["v2"]["readers"]["CR-oracle-state"]["per_state"]["EXPIRY"]["auroc"],
                                                 "site": "Appendix C.2, with its definition; not the body"}}
    res["cf444"] = out
    return out, totals_ok


# ---------------------------------------------------------------- the 661 (secondary)
def run_661(res):
    from ds_common import load_cell  # noqa: E402  (661 items with gold and pn_members attached)
    from resp_common import true_flags  # noqa: E402
    import x4_score  # noqa: E402
    from common_e1r import load_e1  # noqa: E402
    items = load_cell(); fl = true_flags(); idx = indexes()
    _, _, idxT, _ = load_e1()
    retr = json.load(io.open(ROOT / "resp_review" / "l2" / "retrieval.json", encoding="utf-8"))["items"]
    assert len(items) == 661
    y = np.array([1 if it["label"] == "PRESENT-NEGATIVE" else 0 for it in items], int)
    g = np.array([it["persona"] for it in items]); qs = [it["question"] for it in items]
    state = np.array([{"sup": "SUPERSESSION", "ret": "RETRACTION", "exp": "EXPIRY"}.get(retr[it["item_id"]]["state"], "-") for it in items])
    texts = [idx[index_key(it, "TRUE")] for it in items]

    # target categories: PN from pn_members, otherwise from gold; never from NB-1
    tcats, src = [], {"PRESENT-NEGATIVE": [0, 0], "PRESENT": [0, 0], "ABSENT": [0, 0]}
    multi = 0
    for it in items:
        p = it["persona"]
        ids = (it.get("pn_members") or []) if it["label"] == "PRESENT-NEGATIVE" else (it.get("gold") or [])
        cs = sorted({fl[p][e]["category"] for e in ids if e in fl[p]})
        tcats.append(cs); src[it["label"]][0 if cs else 1] += 1; multi += 1 if len(cs) > 1 else 0
    keep = np.array([bool(c) for c in tcats])

    # CR-nb1 on all 661 (gate 0.5514) and CR-oracle on the gold-category items only
    nb1 = np.zeros(661); ora = np.zeros(661); orb = np.zeros(661); tot = np.zeros(661)
    for k, it in enumerate(items):
        p = parse(texts[k]); a_cat, _, _, _ = assign_category(p, it["question"]); ac = cat_cells(p, a_cat) if a_cat else None
        nb1[k] = (float(ac["suprsd"] + ac["retract"] + ac["expired"]) / max(1, ac["entries"])) if ac else 0.0
        cells = [cat_cells(p, c) for c in tcats[k]]; cells = [c for c in cells if c]
        ora[k] = max((float(c["retract"] + c["expired"]) for c in cells), default=0.0)
        orb[k] = max((float(c["suprsd"] + c["retract"] + c["expired"]) for c in cells), default=0.0)
        rt, ex = counts_of(texts[k]); tot[k] = float(rt + ex)
    nb1_a = r4(auroc(nb1, y)); assert nb1_a == GATES["nb1_661_true"], f"GATE: NB-1 on the 661 {nb1_a} != {GATES['nb1_661_true']}"
    res["gates"]["nb1_661_true"] = nb1_a

    # models on the 661 under TRUE
    models = {"gpt-4.1-mini": np.array([idxT[it["item_id"]]["nok"] for it in items], float)}
    for model, code in (("claude-haiku-4-5-20251001", "H45"), ("claude-opus-5", "OP5"), ("gpt-5.6-luna", "LUNA")):
        coll, _ = x4_score.load_lane(code)
        v = np.array([coll.get((it["item_id"], "INDEXED-TRUE"), {}).get("nok", np.nan) for it in items], float)
        if np.isnan(v).any():
            res.setdefault("notes", []).append(f"661: {model} has {int(np.isnan(v).sum())} items without a collapsed INDEXED-TRUE score; paired rows use the covered items")
        models[model] = v

    def per_state_661(s, yy, gg, ss):
        d = {}
        for s_ in STATES:
            m = (ss == s_) | (yy == 0)
            d[s_] = {"n": int(m.sum()), "pos": int(yy[m].sum()), **single(s[m], yy[m], gg[m])}
        return d

    out = {"n": 661, "pos": 104, "per_state_convention": "positives of one state against all negatives (Table 34)",
           "category_source": {"PRESENT-NEGATIVE": "pn_members' entries", "PRESENT": "gold entries", "ABSENT": "gold entries", "never": "NB-1 assignment"},
           "with_category_vs_dropped_by_label": {k: {"with_category": v[0], "dropped": v[1]} for k, v in src.items()},
           "items_with_more_than_one_target_category": multi, "readers": {}}
    subsets = {"CR-oracle-a": (ora, keep), "CR-oracle-b": (orb, keep), "CR-totals-a": (tot, np.ones(661, bool)), "CR-nb1": (nb1, np.ones(661, bool))}
    for r, (s, m) in subsets.items():
        row = {"population": "gold-category items only" if r.startswith("CR-oracle") else "all 661", "n": int(m.sum()), "pos": int(y[m].sum()),
               "whole": single(s[m], y[m], g[m]), "per_state": per_state_661(s[m], y[m], g[m], state[m]), "vs_models": {}}
        for model, v in models.items():
            mm = m & ~np.isnan(v)
            row["vs_models"][model] = {"n": int(mm.sum()), "model_auroc": r4(auroc(v[mm], y[mm])), "reader_auroc": r4(auroc(s[mm], y[mm])), **paired(s[mm], v[mm], y[mm], g[mm])}
        out["readers"][r] = row
    res["obl661"] = out
    return out


def main():
    res = {"meta": {"script": "reviews/v18/tools/a1_count_readers.py", "model_calls": 0, "n_boot": N_BOOT, "seed": SEED,
                    "paired_sign": "model minus reader", "chance_tolerance": CHANCE_TOL}, "gates": {}}
    out444, totals_ok = run_444(res)
    out661 = run_661(res)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=1, sort_keys=True, default=float); f.write("\n")

    # ---- report
    print("A1 count readers -- gates:", res["gates"])
    print("\n== v2r check (the author's redefinition) ==")
    for r in ("CR-totals-a", "CR-totals-b"):
        c = out444["v2r_check"][r]
        print(f"  {r}: whole v2 {c['whole']['v2']} -> v2r {c['whole']['v2r']}; RET v2 {c['RETRACTION']['v2']} -> v2r {c['RETRACTION']['v2r']} (at chance: {c['RETRACTION']['v2r_at_chance']}); "
              f"EXP v2 {c['EXPIRY']['v2']} -> v2r {c['EXPIRY']['v2r']} (at chance: {c['EXPIRY']['v2r_at_chance']})")
    print(f"  CR-oracle scores identical under v2 and v2r: {out444['v2r_check']['CR-oracle_scores_identical_v2_v2r']}  ({out444['v2r_check']['v2r_permutes_only_the_totals_lines']})")
    for name, M in out444["v2r_check"]["CR-totals-a_expectation_over_seeds"].items():
        print(f"  CR-totals-a {name}: RET mean {M['RETRACTION']['mean']} [{M['RETRACTION']['p2.5']},{M['RETRACTION']['p97.5']}]; EXP mean {M['EXPIRY']['mean']} [{M['EXPIRY']['p2.5']},{M['EXPIRY']['p97.5']}]; whole mean {M['whole']['mean']}")
    print(f"  {out444['v2r_check']['recorded_seed_reading']}")
    print(f"  base-count census (ABSENT version, v2): {out444['base_count_census']}")
    print(f"  verdict: {out444['v2r_check']['verdict']}")
    print("\n== the 444 (primary): AUROC whole / SUP / RET / EXP ==")
    for tag in ("v2", "v3", "v2r"):
        b = out444["summaries"][tag]
        print(f"  [{tag}] category row missing on {b['category_row_missing']} items; NB-1 assigned a category on {b['nb1_assigned_a_category']}")
        for r, row in b["readers"].items():
            ps = row["per_state"]
            print(f"    {r:16s} {row['whole']['auroc']:.4f}  {ps['SUPERSESSION']['auroc']:.4f} / {ps['RETRACTION']['auroc']:.4f} / {ps['EXPIRY']['auroc']:.4f}"
                  f"   item [{row['whole']['item_ci'].get('ci_lo', float('nan')):.4f},{row['whole']['item_ci'].get('ci_hi', float('nan')):.4f}]"
                  f" persona [{row['whole']['persona_ci'].get('ci_lo', float('nan')):.4f},{row['whole']['persona_ci'].get('ci_hi', float('nan')):.4f}]")
        for r in ("CR-oracle-a", "CR-oracle-state", "CR-totals-a", "CR-nb1"):
            for model, vm in b["readers"][r]["vs_models"].items():
                w = vm["whole"]
                print(f"      {model} minus {r}: whole {w['delta']:+.4f} item [{w['item_ci']['ci_lo']:+.4f},{w['item_ci']['ci_hi']:+.4f}] persona [{w['persona_ci']['ci_lo']:+.4f},{w['persona_ci']['ci_hi']:+.4f}]"
                      f" | RET model {vm['per_state']['RETRACTION']['model']} reader {vm['per_state']['RETRACTION']['reader']} d {vm['per_state']['RETRACTION']['delta']:+.4f}"
                      f" | EXP model {vm['per_state']['EXPIRY']['model']} reader {vm['per_state']['EXPIRY']['reader']} d {vm['per_state']['EXPIRY']['delta']:+.4f}")
    br = out444["branch"]
    print(f"\n== branch: {br['fires']} ({br['note']}); CR-oracle-a under v2: retraction {br['retraction']:.4f}, expiry {br['expiry']:.4f}; state-aware upper bound (C.2) {br['state_aware_upper_bound']}")
    if br["fires"] in ("B1", "B2"):
        print("  reader claim: the tally carried the label and no model read it (see the per-state model rows above).")
    print("\n== the 661 (secondary) ==")
    print("  category source by label (with / dropped):", out661["with_category_vs_dropped_by_label"], "; items with >1 target category:", out661["items_with_more_than_one_target_category"])
    for r, row in out661["readers"].items():
        ps = row["per_state"]
        print(f"    {r:12s} [{row['population']}, n {row['n']}, pos {row['pos']}] {row['whole']['auroc']:.4f}  {ps['SUPERSESSION']['auroc']:.4f} / {ps['RETRACTION']['auroc']:.4f} / {ps['EXPIRY']['auroc']:.4f}")
        for model, vm in row["vs_models"].items():
            print(f"      {model} ({vm['model_auroc']}) minus reader ({vm['reader_auroc']}): {vm['delta']:+.4f} item [{vm['item_ci']['ci_lo']:+.4f},{vm['item_ci']['ci_hi']:+.4f}] persona [{vm['persona_ci']['ci_lo']:+.4f},{vm['persona_ci']['ci_hi']:+.4f}] n {vm['n']}")
    for n in res.get("notes", []):
        print("  note:", n)
    print("\nwrote", OUT.relative_to(ROOT))
    if not totals_ok:
        print("STOP: CR-totals did not fall under v2r; v2r is broken (the author's rule)."); sys.exit(2)


if __name__ == "__main__":
    main()
