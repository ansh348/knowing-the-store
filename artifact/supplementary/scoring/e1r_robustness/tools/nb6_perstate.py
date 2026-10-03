"""Per-state intervals and the frontier per-state split. R81 Phase 1c.

Registered in registrations/ADDENDUM_R81.md section 10, frozen at e8ba22c BEFORE any interval
here existed. Deterministic given the seed; $0, no model call.

ESTIMATOR (ADDENDUM_R81 section 10.1, frozen). Stratified paired item-level bootstrap:
1,000 draws, seed 42. Within a draw, positives are resampled with replacement from that
lifecycle state's positives and negatives from the shared negative pool, both at observed
counts; both readers are scored on the IDENTICAL resampled index set. Single-class draws
discarded. Percentile 2.5/97.5.

WHAT IT PRODUCES
  Item 2  monitor-minus-matcher paired difference per lifecycle state on the mini census,
          plus one-sample intervals against 0.5 for both readers on all three states.
  Item 3  the same three states for the three completed n=661 lanes (luna, Opus 5,
          Haiku 4.5): AUROC point, one-sample interval, and the paired lane-minus-matcher
          difference with interval. Twelve rows. sol and K3 are excluded because the budget
          directive stopped them and they were never scored as cells here (D-R74-6).

Lane scores come from the committed collapse in r74/tools/x4_score.py (dedup on draw, mean
over draws, MIN_DRAWS=3), imported rather than reimplemented (the D-E1R-6 lesson).

Usage: python e1r_robustness/tools/nb6_perstate.py
Writes results/nb6_perstate.json.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "r74" / "tools"))

from common_e1r import OUT, POPULATIONS, auroc, jdump, load_e1     # noqa: E402
from run_nb6 import emb_scores, name_lists                          # noqa: E402
from nb6_composition import AV_STATE                                # noqa: E402

N_BOOT, SEED, TOL = 1000, 42, 0.05
STATES = ("superseded", "expired", "retracted")
LANES = {"gpt-5.6-luna": "luna", "claude-opus-5": "Opus 5",
         "claude-haiku-4-5-20251001": "Haiku 4.5"}


def _draws(pos_idx, neg_idx, rng):
    """One stratified resample: positives within state, negatives from the shared pool."""
    p = rng.integers(0, len(pos_idx), len(pos_idx))
    q = rng.integers(0, len(neg_idx), len(neg_idx))
    return np.concatenate([np.asarray(pos_idx)[p], np.asarray(neg_idx)[q]])


def paired_ci(a, b, pos_idx, neg_idx, n=N_BOOT, seed=SEED):
    """auroc(a) - auroc(b) under the stratified paired bootstrap."""
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a, float), np.asarray(b, float)
    y_all = np.zeros(len(a), int)
    y_all[np.asarray(pos_idx)] = 1
    d = []
    for _ in range(n):
        k = _draws(pos_idx, neg_idx, rng)
        yy = y_all[k]
        if yy.sum() in (0, len(yy)):
            continue
        d.append(auroc(a[k], yy) - auroc(b[k], yy))
    d = np.asarray(d, float)
    lo, hi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    # the point must be computed on the SAME subset the bootstrap resamples: this state's
    # positives plus the shared negatives. Using the full array would silently enter the
    # other states' positives as negatives.
    sub = np.concatenate([np.asarray(pos_idx), np.asarray(neg_idx)])
    ys = y_all[sub]
    return {"delta": float(auroc(a[sub], ys)) - float(auroc(b[sub], ys)),
            "ci_lo": lo, "ci_hi": hi, "n_draws": int(len(d)),
            "excludes_zero": bool(lo > 0 or hi < 0)}


def single_ci(s, pos_idx, neg_idx, n=N_BOOT, seed=SEED):
    """One-sample AUROC interval under the same stratified resampling."""
    rng = np.random.default_rng(seed)
    s = np.asarray(s, float)
    y_all = np.zeros(len(s), int)
    y_all[np.asarray(pos_idx)] = 1
    v = []
    for _ in range(n):
        k = _draws(pos_idx, neg_idx, rng)
        yy = y_all[k]
        if yy.sum() in (0, len(yy)):
            continue
        v.append(auroc(s[k], yy))
    v = np.asarray(v, float)
    lo, hi = float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))
    sub = np.concatenate([np.asarray(pos_idx), np.asarray(neg_idx)])
    return {"auroc": float(auroc(s[sub], y_all[sub])), "ci_lo": lo, "ci_hi": hi,
            "n_draws": int(len(v)),
            "excludes_half": bool(lo > 0.5 or hi < 0.5)}


def main():
    items, blind, idxT, _ = load_e1()
    sub = [it for it in items if POPULATIONS["R-NOK-FRB"]["filt"](it)]

    rows = []
    for it in sub:
        q, tag = it["question"], it["item_id"]
        if q not in blind or tag not in idxT:
            continue
        if blind[q].get("nok") is None or idxT[tag].get("nok") is None:
            continue
        y = 1 if it.get("label", it["label_pre"]) == "PRESENT-NEGATIVE" else 0
        sup, alln = name_lists(it, "TRUE")
        rows.append({"y": y, "question": q, "sup": sup, "all": alln,
                     "av": it.get("attack_vector"), "item_id": tag,
                     "mini": idxT[tag].get("nok")})

    matcher = emb_scores(rows, "sup")
    mini = [r["mini"] for r in rows]
    neg_idx = [i for i, r in enumerate(rows) if r["y"] == 0]
    pos_by_state = {st: [i for i, r in enumerate(rows)
                         if r["y"] == 1 and AV_STATE.get(r["av"]) == st]
                    for st in STATES}

    out = {"n": len(rows), "n_neg": len(neg_idx),
           "n_pos_by_state": {k: len(v) for k, v in pos_by_state.items()}}

    # ---------------- Item 2: mini census, per-state intervals ---------------------
    item2 = {}
    for st in STATES:
        pi = pos_by_state[st]
        item2[st] = {
            "n_pos": len(pi),
            "matcher": single_ci(matcher, pi, neg_idx),
            "monitor": single_ci(mini, pi, neg_idx),
            "monitor_minus_matcher": paired_ci(mini, matcher, pi, neg_idx),
        }
        r = item2[st]
        print(f"  [item2] {st:12s} n={len(pi):3d}  matcher {r['matcher']['auroc']:.4f} "
              f"[{r['matcher']['ci_lo']:+.4f},{r['matcher']['ci_hi']:+.4f}]  "
              f"monitor {r['monitor']['auroc']:.4f} "
              f"[{r['monitor']['ci_lo']:+.4f},{r['monitor']['ci_hi']:+.4f}]  "
              f"diff {r['monitor_minus_matcher']['delta']:+.4f} "
              f"[{r['monitor_minus_matcher']['ci_lo']:+.4f},"
              f"{r['monitor_minus_matcher']['ci_hi']:+.4f}]"
              f"{'  EXCLUDES 0' if r['monitor_minus_matcher']['excludes_zero'] else '  includes 0'}")
    out["item2_mini_per_state"] = item2

    # ---------------- Item 3: the three completed lanes ----------------------------
    from x4_score import load_lane                                   # noqa: E402
    byid = {r["item_id"]: i for i, r in enumerate(rows)}
    item3, codes = {}, {"gpt-5.6-luna": "LUNA", "claude-opus-5": "OP5",
                        "claude-haiku-4-5-20251001": "H45"}
    print()
    for model, label in LANES.items():
        coll, _usd = load_lane(codes[model])
        lane = np.full(len(rows), np.nan, float)
        for (iid, arm), v in coll.items():
            if arm != "INDEXED-TRUE" or iid not in byid or v.get("nok") is None:
                continue
            lane[byid[iid]] = v["nok"]
        item3[label] = {"coverage": int(np.sum(~np.isnan(lane)))}
        for st in STATES:
            pi = [i for i in pos_by_state[st] if not np.isnan(lane[i])]
            ni = [i for i in neg_idx if not np.isnan(lane[i])]
            item3[label][st] = {
                "n_pos": len(pi),
                "lane": single_ci(lane, pi, ni),
                "lane_minus_matcher": paired_ci(lane, matcher, pi, ni),
            }
            d = item3[label][st]
            print(f"  [item3] {label:10s} {st:12s} n={len(pi):3d}  "
                  f"lane {d['lane']['auroc']:.4f} "
                  f"[{d['lane']['ci_lo']:+.4f},{d['lane']['ci_hi']:+.4f}]  "
                  f"lane-matcher {d['lane_minus_matcher']['delta']:+.4f} "
                  f"[{d['lane_minus_matcher']['ci_lo']:+.4f},"
                  f"{d['lane_minus_matcher']['ci_hi']:+.4f}]"
                  f"{'  EXCLUDES 0' if d['lane_minus_matcher']['excludes_zero'] else '  includes 0'}")
    out["item3_lanes_per_state"] = item3

    # ---------------- adjudicate the frozen reading --------------------------------
    cond1 = all(
        sum(1 for L in item3
            if item3[L][st]["lane_minus_matcher"]["excludes_zero"]
            and item3[L][st]["lane_minus_matcher"]["delta"] > 0) >= 2
        for st in ("retracted", "expired"))
    cond2 = all(item3[L]["superseded"]["lane_minus_matcher"]["delta"] <= TOL
                for L in item3)
    fired = "(i)" if (cond1 and cond2) else "(ii)"
    out["frontier_reading"] = {
        "condition_1_two_of_three_lanes_clear_on_both_count_only_states": bool(cond1),
        "condition_2_no_lane_clears_by_more_than_tol_on_supersession": bool(cond2),
        "fired": fired,
        "sentence": ("Larger models recover part of the obligation the index only counts."
                     if fired == "(i)" else
                     "Larger models exceed the lookup on the same population, and the split "
                     "by lifecycle state does not attribute that margin."),
    }
    out["registration"] = "registrations/ADDENDUM_R81.md section 10 @ e8ba22c"
    out["estimator"] = ("stratified paired item-level bootstrap, 1000 draws, seed 42, "
                        "positives within state, negatives from the shared pool")
    jdump(out, OUT / "nb6_perstate.json")

    print(f"\n  condition 1 (two of three lanes clear on retraction AND expiry): {cond1}")
    print(f"  condition 2 (no lane clears by >{TOL} on supersession):           {cond2}")
    print(f"  FROZEN READING FIRED: {fired}")
    print(f"  -> {out['frontier_reading']['sentence']}")
    print(f"\nwrote {OUT / 'nb6_perstate.json'}")


if __name__ == "__main__":
    main()
