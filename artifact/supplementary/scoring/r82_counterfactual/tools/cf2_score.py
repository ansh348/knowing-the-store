"""cf2_score.py -- CF-2: score the 444-item cell under ADDENDUM_CF2 sections 6-8.

NO API CALLS. Estimators are the committed ones (common_e1r): Mann-Whitney AUROC with ties at
0.5; the item-level paired bootstrap (1000 draws, seed 42, single-class draws discarded) is
PRIMARY; the persona-clustered paired bootstrap (boot_cluster with the group vector = persona,
the section-3 cluster unit) prints beside it. A prediction holds only when both intervals
agree; when they disagree the weaker reading governs (the D.2 rule). Tolerance 0.05.

Two further estimators, registered in section 6: the per-state paired interval (boot_item on one
state's items) and the two-subset difference bootstrap boot_subset_diff_ci, ported verbatim from
the Phase 3 script (reviews/CF2_SCOPE.md:431-437; cf2/power/power_sim_comp.py:72-78), the
estimator for P2. P5 is an equivalence reading: the paired V2R-minus-V2 interval inside
[-0.05, +0.05] on both intervals.

Draw collapse is score_cf.load_lane (X4: dedup on draw, MIN_DRAWS 3, arithmetic mean), called
with its rows directory re-pointed to cf2/rows. Blind is one call per question, reused across
the question's three versions, so blind AUROC is 0.5 by identity; it prints.

Baselines on the same 444: the superseded-names matcher on v2 (NB-6), the all-states matcher over
the three named sections on v3, the whole-map matcher on v2 (NB-5); score_cf.matcher, the E1-R
offline encoder. Any baseline exceeding a reader on any row is flagged (section 8 adverse branch).
FOK is descriptive only and labelled so.

Usage:  python r82_counterfactual/tools/cf2_score.py
Writes: r82_counterfactual/cf2/results/cf_scores_cf2.json; prints the section-8 branch texts with
the numbers filled, for every prediction whose lane has rows, and a dash with its reason otherwise.
"""
from __future__ import annotations

import collections
import io
import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from common_e1r import auroc, boot_cluster, boot_cluster_single, boot_item  # noqa: E402
from index_features import parse as parse_index  # noqa: E402
from index_v3 import named_sections  # noqa: E402
import score_cf as S  # noqa: E402

CF2 = ROOT / "r82_counterfactual" / "cf2"
S.R82 = CF2                                 # load_lane reads <R82>/rows/rows_<code>.jsonl
OUT = CF2 / "results" / "cf_scores_cf2.json"
TOL = 0.05
LANES = {"MINI": "gpt-4.1-mini", "H45": "claude-haiku-4-5-20251001", "OP5": "claude-opus-5"}
ARMS = (("INDEXED-V2", "v2"), ("INDEXED-V3", "v3"), ("INDEXED-V2R", "v2r"))
N_BOOT, SEED = 1000, 42
OPUS_DASH = "lane not run: the drop rule of section 11 is evaluated on 2026-09-19, after the Haiku 4.5 lane is scored"
HAIKU_DASH = ("lane pending: Haiku 4.5 batch submitted, not yet collected" if (CF2 / "rows" / "batch_H45.json").exists()
              else "lane not yet run: the Haiku 4.5 batch is submitted after the mini lane is scored")


# ---- the Phase 3 script's two-subset difference bootstrap, verbatim (cf2/power/power_sim_comp.py:52-78)
def auc_hist(Sidx, Yk, V):
    R, N = Sidx.shape; off = (np.arange(R) * V)[:, None]
    pos = np.bincount((Sidx + off)[Yk == 1], minlength=R * V).reshape(R, V).astype(float)
    neg = np.bincount((Sidx + off)[Yk == 0], minlength=R * V).reshape(R, V).astype(float)
    below = np.cumsum(neg, axis=1) - neg
    return (pos * (below + 0.5 * neg)).sum(1) / (pos.sum(1) * neg.sum(1))


def boot_subset_diff_ci(sA, yA, sB, yB, n=N_BOOT, seed=SEED):
    grid = np.unique(np.concatenate([sA, sB])); V = len(grid); rng = np.random.default_rng(seed)
    a = np.searchsorted(grid, sA); bb = np.searchsorted(grid, sB); NA, NB = len(yA), len(yB)
    KA = rng.integers(0, NA, (n, NA)); KB = rng.integers(0, NB, (n, NB)); YA = yA[KA]; YB = yB[KB]
    keep = (YA.sum(1) > 0) & (YA.sum(1) < NA) & (YB.sum(1) > 0) & (YB.sum(1) < NB)
    d = auc_hist(a[KA][keep], YA[keep], V) - auc_hist(bb[KB][keep], YB[keep], V)
    return float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


def boot_subset_diff_cluster(sA, yA, gA, sB, yB, gB, n=N_BOOT, seed=SEED):
    """The two-subset difference under the persona-clustered convention: personas drawn with
    replacement (the union of both subsets' personas), each draw's A and B items are the drawn
    personas' items in each subset; single-class draws on either side discarded. Prints beside
    boot_subset_diff_ci under the D.2 rule; it is not the registered estimator for P2."""
    rng = np.random.default_rng(seed)
    groups = np.unique(np.concatenate([gA, gB]))
    iA = {u: np.flatnonzero(gA == u) for u in groups}; iB = {u: np.flatnonzero(gB == u) for u in groups}
    d = []
    for _ in range(n):
        drawn = rng.integers(0, len(groups), len(groups))
        ka = np.concatenate([iA[groups[t]] for t in drawn]); kb = np.concatenate([iB[groups[t]] for t in drawn])
        if len(ka) == 0 or len(kb) == 0 or yA[ka].sum() in (0, len(ka)) or yB[kb].sum() in (0, len(kb)):
            continue
        d.append(auroc(sA[ka], yA[ka]) - auroc(sB[kb], yB[kb]))
    lo, hi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    return {"ci_lo": lo, "ci_hi": hi, "n_draws": len(d), "excludes_zero": bool(lo > 0 or hi < 0)}


def load_field(code, field):
    """load_lane's X4 collapse for the fok field (descriptive)."""
    path = CF2 / "rows" / f"rows_{code}.jsonl"
    if not path.exists():
        return None
    per = collections.defaultdict(dict)
    for line in io.open(path, encoding="utf-8"):
        r = json.loads(line)
        if r.get("status") == "OK":
            per[(r["unit_id"], r["arm"])][r["draw"]] = r
    out = {}
    for k, draws in per.items():
        rs = list(draws.values())
        if len(rs) < S.MIN_DRAWS and len(rs) != 1:
            continue
        v = [x[field] for x in rs if x[field] is not None]
        if v:
            out[k] = float(np.mean(v))
    return out


def ci(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"


def paired(b, i, y, g):
    it, cl = boot_item(b, i, y), boot_cluster(b, i, y, g)
    return {"delta": round(float(auroc(i, y) - auroc(b, y)), 4), "item_ci": it, "persona_ci": cl,
            "both_exclude_zero": bool(it.get("excludes_zero") and cl.get("excludes_zero")),
            "agree": bool(it.get("excludes_zero") == cl.get("excludes_zero"))}


def main():
    cell = json.load(io.open(CF2 / "cf_cell.json", encoding="utf-8")); items = cell["items"]
    idx = json.load(io.open(CF2 / "cf_indexes.json", encoding="utf-8"))["indexes"]
    qmap = {q: f"q{n:03d}" for n, q in enumerate(sorted({it["question"] for it in items}))}
    y = np.array([it["y_nok"] for it in items], int); yf = np.array([it["y_fok"] for it in items], int)
    g = np.array([it["persona"] for it in items]); st = np.array([it["state"] for it in items])
    qs = [it["question"] for it in items]
    m_sup, m_cnt = st == "SUPERSESSION", st != "SUPERSESSION"
    res = {"meta": {"n": len(items), "pairs": len(items) // 3, "pos": int(y.sum()), "composition": cell["meta"]["composition"], "tol": TOL,
                    "cluster_unit": "persona", "primary": "item-level paired bootstrap", "rule": "D.2: both intervals must agree; the weaker governs",
                    "blind_is_half_by_construction": True, "n_boot": N_BOOT, "seed": SEED}, "lanes": {}, "baselines": {}, "predictions": {}, "flags": []}

    # ---------------------------------------------------------------- monitors
    lanes = {}
    for code, model in LANES.items():
        lane = S.load_lane(code)
        if not lane:
            continue
        b = np.array([lane.get((qmap[it["question"]], "BLIND"), np.nan) for it in items])
        if np.isnan(b).any():
            print(f"{code}: blind incomplete ({int(np.isnan(b).sum())} missing), skipping"); continue
        arms = {}
        for arm, tag in ARMS:
            i = np.array([lane.get((it["item_id"], arm), np.nan) for it in items])
            if np.isnan(i).any():
                print(f"{code} {tag}: {int(np.isnan(i).sum())} items missing, skipping arm"); continue
            arms[tag] = i
        row = {"n_rows_collapsed": len(lane), "blind_auroc": round(float(auroc(b, y)), 4)}
        for tag, i in arms.items():
            r = paired(b, i, y, g)
            r.update({"indexed": round(float(auroc(i, y)), 4), "indexed_ci_persona": boot_cluster_single(i, y, g)})
            r["per_state"] = {}
            for s_ in ("SUPERSESSION", "RETRACTION", "EXPIRY"):
                m = st == s_
                r["per_state"][s_] = {"n": int(m.sum()), "pos": int(y[m].sum()), "blind": round(float(auroc(b[m], y[m])), 4),
                                      "indexed": round(float(auroc(i[m], y[m])), 4), **paired(b[m], i[m], y[m], g[m])}
            r["counted_pooled"] = {"n": int(m_cnt.sum()), "pos": int(y[m_cnt].sum()), "indexed": round(float(auroc(i[m_cnt], y[m_cnt])), 4)}
            r["named_minus_counted"] = {"sup": round(float(auroc(i[m_sup], y[m_sup])), 4), "counted": round(float(auroc(i[m_cnt], y[m_cnt])), 4),
                                        "delta": round(float(auroc(i[m_sup], y[m_sup]) - auroc(i[m_cnt], y[m_cnt])), 4),
                                        "two_subset_ci": dict(zip(("ci_lo", "ci_hi"), boot_subset_diff_ci(i[m_sup], y[m_sup], i[m_cnt], y[m_cnt]))),
                                        "two_subset_ci_persona": boot_subset_diff_cluster(i[m_sup], y[m_sup], g[m_sup], i[m_cnt], y[m_cnt], g[m_cnt])}
            row[tag] = r
        if "v2" in arms and "v3" in arms:
            row["counted_paired_v3_minus_v2"] = {"n": int(m_cnt.sum()), "pairs": int(m_cnt.sum() // 3), "v2": round(float(auroc(arms["v2"][m_cnt], y[m_cnt])), 4),
                                                 "v3": round(float(auroc(arms["v3"][m_cnt], y[m_cnt])), 4), **paired(arms["v2"][m_cnt], arms["v3"][m_cnt], y[m_cnt], g[m_cnt])}
        if "v2" in arms and "v2r" in arms:
            e = paired(arms["v2"], arms["v2r"], y, g)
            e["inside_band_item"] = bool(-TOL <= e["item_ci"]["ci_lo"] and e["item_ci"]["ci_hi"] <= TOL)
            e["inside_band_persona"] = bool(-TOL <= e["persona_ci"]["ci_lo"] and e["persona_ci"]["ci_hi"] <= TOL)
            e["inside_band_both"] = e["inside_band_item"] and e["inside_band_persona"]
            row["equiv_v2r_minus_v2"] = e
        fok = load_field(code, "fok")
        if fok:
            row["fok_descriptive"] = {tag: round(float(auroc(np.array([fok.get((it["item_id"], arm), np.nan) for it in items]), yf)), 4)
                                      for arm, tag in ARMS if all((it["item_id"], arm) in fok for it in items)}
        lanes[code] = row; res["lanes"][model] = row

    # ---------------------------------------------------------------- baselines
    sup2 = [named_sections(idx[it["item_id"]]["v2"])["superseded"] for it in items]
    s3 = [named_sections(idx[it["item_id"]]["v3"]) for it in items]
    all3 = [s["superseded"] + s["retracted"] + s["expired"] for s in s3]
    whole = [sorted({n for lst in parse_index(idx[it["item_id"]]["v2"])["attr_by_cat"].values() for n in lst}) for it in items]
    base = {}
    for name, lists in (("NB6-superseded-names-v2", sup2), ("all-states-names-v3", all3), ("NB5-whole-map-v2", whole)):
        s_ = S.matcher(qs, lists)
        base[name] = {"auroc": round(float(auroc(s_, y)), 4), "persona_ci": boot_cluster_single(s_, y, g),
                      "per_state": {k: round(float(auroc(s_[st == k], y[st == k])), 4) for k in ("SUPERSESSION", "RETRACTION", "EXPIRY")}}
    res["baselines"] = base
    # adverse branch: a baseline exceeding a reader on any row
    for code, row in lanes.items():
        for tag in ("v2", "v3", "v2r"):
            if tag not in row:
                continue
            for bname, bres in base.items():
                if bres["auroc"] > row[tag]["indexed"]:
                    res["flags"].append(f"baseline {bname} ({bres['auroc']:.4f}) exceeds {LANES[code]} {tag} ({row[tag]['indexed']:.4f}) on the whole cell")
                for k in ("SUPERSESSION", "RETRACTION", "EXPIRY"):
                    if bres["per_state"][k] > row[tag]["per_state"][k]["indexed"]:
                        res["flags"].append(f"baseline {bname} ({bres['per_state'][k]:.4f}) exceeds {LANES[code]} {tag} on {k} ({row[tag]['per_state'][k]['indexed']:.4f})")

    # ---------------------------------------------------------------- predictions, section 7 read under the D.2 rule
    P = res["predictions"]; mini, h45, op5 = lanes.get("MINI"), lanes.get("H45"), lanes.get("OP5")
    N_Q = len(items) // 3
    if mini and "v2" in mini:
        r = mini["v2"]; hold = r["delta"] > 0 and r["both_exclude_zero"]
        P["P1"] = {"verdict": "HOLDS" if hold else "FAILS", "reader": "gpt-4.1-mini", "arm": "v2", "X": r["indexed"], "delta": r["delta"],
                   "I_item": ci(r["item_ci"]), "I_persona": ci(r["persona_ci"]), "agree": r["agree"], "N": N_Q,
                   "text": (f"On {N_Q} questions written before any version of the store existed, and asked of three versions of the same store that differ in one "
                            f"attribute each, the smallest model's obligation judgment reaches {r['indexed']:.3f} against the 0.5 a question-only reader attains here, "
                            f"with an interval of {ci(r['item_ci'])} (persona-clustered {ci(r['persona_ci'])}). The gain survives where the question cannot carry the label."
                            if hold else
                            f"On {N_Q} questions written before any version of the store existed, the smallest model's obligation judgment under the summary that names "
                            f"only superseded content reaches {r['indexed']:.3f} against the 0.5 a question-only reader attains here, with an interval of {ci(r['item_ci'])} "
                            f"(persona-clustered {ci(r['persona_ci'])}) that includes zero. On this cell the gain is not established for that reader.")}
    else:
        P["P1"] = {"verdict": "—", "reason": "mini lane not scored"}
    for lane_code, key, dash in (("H45", "P2", HAIKU_DASH), ("OP5", "P2_opus", OPUS_DASH)):
        L = lanes.get(lane_code)
        if L and "v2" in L:
            nm = L["v2"]["named_minus_counted"]; lo, hi = nm["two_subset_ci"]["ci_lo"], nm["two_subset_ci"]["ci_hi"]
            pc = nm["two_subset_ci_persona"]; item_ex = lo > 0 or hi < 0
            hold = nm["delta"] > TOL and item_ex and pc["excludes_zero"]           # both conventions; the weaker governs
            rdr = "Haiku 4.5" if lane_code == "H45" else "Opus 5"
            P[key] = {"verdict": "HOLDS" if hold else "FAILS", "reader": LANES[lane_code], "D": nm["delta"], "I": f"[{lo:+.4f}, {hi:+.4f}]", "I_persona": ci(pc),
                      "agree": item_ex == pc["excludes_zero"], "named": nm["sup"], "counted": nm["counted"],
                      "text": (f"Under the summary that names only superseded content, {rdr}'s judgment on the named state exceeds its judgment on the two counted "
                               f"states by {nm['delta']:+.3f}, interval [{lo:+.4f}, {hi:+.4f}] (persona-clustered {ci(pc)})." if hold else
                               f"Under that summary {rdr}'s judgment on the named state exceeds the judgment on the counted states by {nm['delta']:+.3f}, interval "
                               f"[{lo:+.4f}, {hi:+.4f}] (persona-clustered {ci(pc)}), which is inside tolerance or includes zero; the boundary between named and counted states is not established on this cell for that reader.")}
        else:
            P[key] = {"verdict": "—", "reason": dash}
    if mini and "v2" in mini:
        nm = mini["v2"]["named_minus_counted"]
        P["P2_mini_descriptive"] = {"D": nm["delta"], "I": f"[{nm['two_subset_ci']['ci_lo']:+.4f}, {nm['two_subset_ci']['ci_hi']:+.4f}]", "named": nm["sup"], "counted": nm["counted"],
                                    "note": "descriptive, carries no prediction (section 7)"}
    if h45 and "counted_paired_v3_minus_v2" in h45:
        c = h45["counted_paired_v3_minus_v2"]; hold = c["delta"] > TOL and c["both_exclude_zero"]
        P["P3"] = {"verdict": "HOLDS" if hold else "FAILS", "X": c["v2"], "Y": c["v3"], "D": c["delta"], "I_item": ci(c["item_ci"]), "I_persona": ci(c["persona_ci"]), "N": c["pairs"],
                   "text": (f"Naming retracted and expired content lifts Haiku 4.5's judgment on those states from {c['v2']:.3f} to {c['v3']:.3f} on the store-counterfactual set "
                            f"({c['pairs']} questions), a paired gain of {c['delta']:+.3f} with interval {ci(c['item_ci'])} (persona-clustered {ci(c['persona_ci'])})." if hold else
                            f"Naming retracted and expired content raises Haiku 4.5's judgment on those states by {c['delta']:+.3f}, interval {ci(c['item_ci'])} (persona-clustered "
                            f"{ci(c['persona_ci'])}), which does not clear tolerance with an interval excluding zero; the counted states are not recovered by naming alone on this cell.")}
    else:
        P["P3"] = {"verdict": "—", "reason": HAIKU_DASH}
    if mini and "counted_paired_v3_minus_v2" in mini:
        c = mini["counted_paired_v3_minus_v2"]
        P["P3_mini_descriptive"] = {"X": c["v2"], "Y": c["v3"], "D": c["delta"], "I_item": ci(c["item_ci"]), "I_persona": ci(c["persona_ci"]), "note": "descriptive"}
    # P4
    p4 = {}
    if mini and "v2" in mini:
        yb, xr = base["NB6-superseded-names-v2"]["auroc"], mini["v2"]["indexed"]; d = round(yb - xr, 4)
        p4["v2_lookup_vs_mini"] = {"Y_lookup": yb, "X_reader": xr, "D": d, "within_tolerance": abs(d) <= TOL, "favour": "lookup" if d > 0 else "reader"}
    if h45 and "v3" in h45:
        yb, xr = base["all-states-names-v3"]["auroc"], h45["v3"]["indexed"]; d = round(yb - xr, 4)
        p4["v3_lookup_vs_haiku"] = {"Y_lookup": yb, "X_reader": xr, "D": d, "within_tolerance": abs(d) <= TOL, "favour": "lookup" if d > 0 else "reader"}
    else:
        p4["v3_lookup_vs_haiku"] = {"verdict": "—", "reason": HAIKU_DASH}
    if "v2_lookup_vs_mini" in p4:
        a = p4["v2_lookup_vs_mini"]; hb = p4["v3_lookup_vs_haiku"]
        half2 = (f", and the all-states lookup reaches {hb['Y_lookup']:.3f} against Haiku 4.5's {hb['X_reader']:.3f} under the all-three-named summary"
                 + (", within tolerance" if hb["within_tolerance"] else f", a margin of {abs(hb['D']):.3f} outside tolerance, in the {hb['favour']}'s favour")
                 if "Y_lookup" in hb else "; the all-states lookup against Haiku 4.5 under the all-three-named summary prints when that lane is scored")
        p4["text"] = (f"On this cell the superseded-names lookup reaches {a['Y_lookup']:.3f} against the smallest reader's {a['X_reader']:.3f} under the superseded-only summary"
                      + (", within tolerance" if a["within_tolerance"] else f", a margin of {abs(a['D']):.3f} outside tolerance, in the {a['favour']}'s favour")
                      + half2 + ".")
        p4["verdict"] = "prints either way"
    P["P4"] = p4
    # P5
    p5 = {}
    for code, key, dash in (("MINI", "mini", None), ("H45", "haiku", HAIKU_DASH), ("OP5", "opus", OPUS_DASH)):
        L = lanes.get(code)
        if L and "equiv_v2r_minus_v2" in L:
            e = L["equiv_v2r_minus_v2"]
            p5[key] = {"D": e["delta"], "I_item": ci(e["item_ci"]), "I_persona": ci(e["persona_ci"]), "inside_band": e["inside_band_both"],
                       "inside_item": e["inside_band_item"], "inside_persona": e["inside_band_persona"], "reader": LANES[code]}
        else:
            p5[key] = {"verdict": "—", "reason": dash or "lane not scored"}
    if "D" in p5["mini"]:
        e, h = p5["mini"], p5["haiku"]
        if "D" in h:
            both = e["inside_band"] and h["inside_band"]
            p5["text"] = (f"Randomizing the retracted and expired counts in the superseded-only summary moves gpt-4.1-mini's whole-cell judgment by {e['D']:+.3f} and "
                          f"Haiku 4.5's by {h['D']:+.3f}, intervals {e['I_item']} (persona-clustered {e['I_persona']}) and {h['I_item']} (persona-clustered {h['I_persona']})"
                          + (", both inside the tolerance band; on this cell neither reader takes anything from the counts" if both else
                             ", which is not inside the tolerance band on " + (" and ".join(r for r, x in (("gpt-4.1-mini", e), ("Haiku 4.5", h)) if not x["inside_band"]))
                             + "; on this cell that reader takes something from the counts") + ".")
            p5["verdict"] = "both inside the band" if both else "outside the band"
            o = p5["opus"]
            if "D" in o:      # Opus 5 appended in the same form when the lane runs (section 8)
                p5["text"] += (f" Opus 5, run under the §11 rule: {o['D']:+.3f}, intervals {o['I_item']} (persona-clustered {o['I_persona']})"
                               + (", inside the band." if o["inside_band"] else ", which is not inside the tolerance band; on this cell that reader takes something from the counts."))
                p5["verdict"] += "; Opus 5 " + ("inside" if o["inside_band"] else "OUTSIDE")
        else:
            p5["text"] = (f"Randomizing the retracted and expired counts in the superseded-only summary moves gpt-4.1-mini's whole-cell judgment by {e['D']:+.3f}, "
                          f"intervals {e['I_item']} (persona-clustered {e['I_persona']})"
                          + (", inside the tolerance band; on this cell that reader takes nothing from the counts" if e["inside_band"]
                             else ", which is not inside the tolerance band; on this cell that reader takes something from the counts")
                          + "; Haiku 4.5's row prints when that lane is scored.")
    P["P5"] = p5

    pathlib.Path(OUT).parent.mkdir(parents=True, exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=2, sort_keys=True, default=float); f.write("\n")

    # ---------------------------------------------------------------- report
    print("=" * 96)
    print(f"CF-2  n={len(items)} ({len(items)//3} pairs, {res['meta']['composition']})  PN positives={int(y.sum())}  tol +/-{TOL}  cluster=persona  D.2 rule")
    print("=" * 96)
    for code, row in lanes.items():
        print(f"\n{LANES[code]}   blind AUROC {row['blind_auroc']:.4f} (0.5 by identity)")
        for tag in ("v2", "v3", "v2r"):
            if tag not in row:
                continue
            r = row[tag]
            print(f"  {tag:3s}: indexed {r['indexed']:.4f}  delta {r['delta']:+.4f}  item {ci(r['item_ci'])}{'*' if r['item_ci']['excludes_zero'] else ' '}  "
                  f"persona {ci(r['persona_ci'])}{'*' if r['persona_ci']['excludes_zero'] else ' '}  {'agree' if r['agree'] else 'DISAGREE'}")
            print("       per state: " + "  ".join(f"{k[:3]} {v['indexed']:.4f} {ci(v['item_ci'])}{'*' if v['item_ci']['excludes_zero'] else ''}" for k, v in r["per_state"].items()))
            nm = r["named_minus_counted"]
            print(f"       named-counted {nm['delta']:+.4f} two-subset [{nm['two_subset_ci']['ci_lo']:+.4f}, {nm['two_subset_ci']['ci_hi']:+.4f}]  persona-clustered {ci(nm['two_subset_ci_persona'])}")
        if "counted_paired_v3_minus_v2" in row:
            c = row["counted_paired_v3_minus_v2"]
            print(f"  counted paired v3-v2 ({c['pairs']} pairs): {c['v2']:.4f} -> {c['v3']:.4f}  delta {c['delta']:+.4f}  item {ci(c['item_ci'])}  persona {ci(c['persona_ci'])}")
        if "equiv_v2r_minus_v2" in row:
            e = row["equiv_v2r_minus_v2"]
            print(f"  equivalence v2r-v2: delta {e['delta']:+.4f}  item {ci(e['item_ci'])}  persona {ci(e['persona_ci'])}  inside band: {e['inside_band_both']}")
        if "fok_descriptive" in row:
            print(f"  FOK (descriptive only): {row['fok_descriptive']}")
    print("\nbaselines (NOK, all 444):")
    for k, v in base.items():
        print(f"  {k:28s} {v['auroc']:.4f}  persona {ci(v['persona_ci'])}  per state {v['per_state']}")
    if res["flags"]:
        print("\nADVERSE BRANCH (section 8): " + "; ".join(res["flags"]))
    print("\nVERDICTS (section 8 texts)")
    for k in ("P1", "P2", "P2_opus", "P2_mini_descriptive", "P3", "P3_mini_descriptive", "P4", "P5"):
        v = P.get(k, {})
        head = f"  {k}: {v.get('verdict', '')}".rstrip()
        print(head)
        if "text" in v:
            print("     " + v["text"])
        elif "reason" in v:
            print("     — " + v["reason"])
        elif "note" in v:
            print(f"     {json.dumps({kk: vv for kk, vv in v.items() if kk != 'note'})}  ({v['note']})")
    print(f"\n-> {OUT}")


if __name__ == "__main__":
    main()
