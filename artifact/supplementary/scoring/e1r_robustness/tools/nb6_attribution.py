"""The attribution gate, and clustered intervals on the mini per-state rows. R81 Phase 1d.

Registered in registrations/ADDENDUM_R81.md section 11, frozen at cfe5415 BEFORE any number
here existed. Deterministic given the seed; $0, no model call.

WHY THIS EXISTS. Phase 1c compared each lane against the superseded-names matcher and
concluded that larger models "recover part of the obligation the index only counts". That
comparison cannot establish attribution: the matcher is intent-blind, the lanes see the
question, and this paper's own question-prior audit shows question text carries
state-flavoured signal (Opus 5 blinds at 0.6429 on this population). The prior-controlled
quantity is the paired indexed-minus-blind delta, per state. This file computes it.

  Item 1  nine rows: three lanes x three originating states, blind point, indexed point,
          and the paired indexed-minus-blind difference with interval. Mini excluded: its
          blind NOK arm is the standing all-tie degeneracy (NUMBERS_E1R section 1).
  Item 3  persona-clustered intervals beside the item-level ones for all three mini
          per-state paired differences (monitor minus matcher).

The hybrid monitor implied by the crossover is NOT computed here; it is queued unregistered
(ADDENDUM_R81 section 11.5). Computing it is a STOP for this pass.

Usage: python e1r_robustness/tools/nb6_attribution.py
Writes results/nb6_attribution.json.
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
from nb6_perstate import paired_ci                                  # noqa: E402

N_BOOT, SEED = 1000, 42
STATES = ("superseded", "expired", "retracted")
LANES = {"LUNA": "luna", "OP5": "Opus 5", "H45": "Haiku 4.5"}


def clustered_paired_ci(a, b, pos_idx, neg_idx, groups, n=N_BOOT, seed=SEED):
    """Persona-clustered paired difference on one state's subset.

    Mirrors common_e1r.boot_cluster: draw as many personas with replacement as the subset
    holds, take every item of each drawn persona, discard single-class draws.
    """
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a, float), np.asarray(b, float)
    sub = np.concatenate([np.asarray(pos_idx), np.asarray(neg_idx)])
    y = np.zeros(len(a), int)
    y[np.asarray(pos_idx)] = 1
    g = np.asarray(groups)[sub]
    ys, as_, bs = y[sub], a[sub], b[sub]
    uniq = np.unique(g)
    by = {u: np.flatnonzero(g == u) for u in uniq}
    d = []
    for _ in range(n):
        drawn = rng.integers(0, len(uniq), len(uniq))
        k = np.concatenate([by[uniq[t]] for t in drawn])
        if ys[k].sum() in (0, len(k)):
            continue
        d.append(auroc(as_[k], ys[k]) - auroc(bs[k], ys[k]))
    d = np.asarray(d, float)
    lo, hi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    return {"ci_lo": lo, "ci_hi": hi, "n_draws": int(len(d)), "n_personas": int(len(uniq)),
            "excludes_zero": bool(lo > 0 or hi < 0)}


def main():
    items, blind, idxT, _ = load_e1()
    rows = []
    for it in [i for i in items if POPULATIONS["R-NOK-FRB"]["filt"](i)]:
        q, tag = it["question"], it["item_id"]
        if q not in blind or tag not in idxT:
            continue
        if blind[q].get("nok") is None or idxT[tag].get("nok") is None:
            continue
        sup, alln = name_lists(it, "TRUE")
        rows.append({"y": 1 if it.get("label", it["label_pre"]) == "PRESENT-NEGATIVE" else 0,
                     "question": q, "sup": sup, "all": alln, "av": it.get("attack_vector"),
                     "item_id": tag, "persona": it["persona"],
                     "mini": idxT[tag].get("nok")})

    matcher = emb_scores(rows, "sup")
    mini = [r["mini"] for r in rows]
    personas = [r["persona"] for r in rows]
    neg = [i for i, r in enumerate(rows) if r["y"] == 0]
    pos = {st: [i for i, r in enumerate(rows)
                if r["y"] == 1 and AV_STATE.get(r["av"]) == st] for st in STATES}
    byid = {r["item_id"]: i for i, r in enumerate(rows)}

    out = {"n": len(rows), "n_neg": len(neg),
           "n_pos_by_state": {k: len(v) for k, v in pos.items()},
           "mini_excluded_reason": ("blind NOK arm is constant, the standing all-tie "
                                    "degeneracy recorded at NUMBERS_E1R section 1")}

    # ---------------- Item 1: the attribution gate --------------------------------
    from x4_score import load_lane                                   # noqa: E402
    item1 = {}
    for code, label in LANES.items():
        coll, _ = load_lane(code)
        ind = np.full(len(rows), np.nan, float)
        bl = np.full(len(rows), np.nan, float)
        for (iid, arm), v in coll.items():
            if iid not in byid or v.get("nok") is None:
                continue
            if arm == "INDEXED-TRUE":
                ind[byid[iid]] = v["nok"]
            elif arm == "BLIND":
                bl[byid[iid]] = v["nok"]
        item1[label] = {}
        for st in STATES:
            ok = ~(np.isnan(ind) | np.isnan(bl))
            pi = [i for i in pos[st] if ok[i]]
            ni = [i for i in neg if ok[i]]
            sub = np.concatenate([np.asarray(pi), np.asarray(ni)])
            y = np.zeros(len(rows), int)
            y[np.asarray(pi)] = 1
            pd = paired_ci(ind, bl, pi, ni)
            item1[label][st] = {
                "n_pos": len(pi), "n_neg": len(ni),
                "blind": float(auroc(bl[sub], y[sub])),
                "indexed": float(auroc(ind[sub], y[sub])),
                "delta": pd["delta"], "ci_lo": pd["ci_lo"], "ci_hi": pd["ci_hi"],
                "excludes_zero": pd["excludes_zero"],
            }
            r = item1[label][st]
            print(f"  [item1] {label:10s} {st:12s} n={r['n_pos']:3d}  "
                  f"blind {r['blind']:.4f}  indexed {r['indexed']:.4f}  "
                  f"delta {r['delta']:+.4f} [{r['ci_lo']:+.4f},{r['ci_hi']:+.4f}]"
                  f"{'  EXCLUDES 0' if r['excludes_zero'] else '  includes 0'}")
    out["item1_indexed_minus_blind"] = item1

    # ---------------- adjudicate the frozen reading -------------------------------
    fired_i = all(
        sum(1 for L in item1
            if item1[L][st]["excludes_zero"] and item1[L][st]["delta"] > 0) >= 2
        for st in ("expired", "retracted"))
    fired = "(i)" if fired_i else "(ii)"
    out["attribution_reading"] = {
        "condition_two_of_three_lanes_exclude_zero_on_expiry_AND_retraction": bool(fired_i),
        "fired": fired,
        "s43": ("That matcher reaches the smallest model tested. Larger models recover part "
                "of the obligation the index only counts."
                if fired_i else
                "That matcher reaches the smallest model tested. Larger models score higher "
                "on the states the index only counts."),
    }

    # ---------------- Item 3: clustered intervals on the mini per-state rows -------
    print()
    item3 = {}
    for st in STATES:
        it_ci = paired_ci(mini, matcher, pos[st], neg)
        cl = clustered_paired_ci(mini, matcher, pos[st], neg, personas)
        item3[st] = {"delta": it_ci["delta"],
                     "item_lo": it_ci["ci_lo"], "item_hi": it_ci["ci_hi"],
                     "item_excludes_zero": it_ci["excludes_zero"],
                     "clustered_lo": cl["ci_lo"], "clustered_hi": cl["ci_hi"],
                     "clustered_excludes_zero": cl["excludes_zero"],
                     "n_personas": cl["n_personas"], "n_draws": cl["n_draws"]}
        r = item3[st]
        print(f"  [item3] {st:12s} delta {r['delta']:+.4f}  "
              f"item [{r['item_lo']:+.4f},{r['item_hi']:+.4f}]  "
              f"clustered [{r['clustered_lo']:+.4f},{r['clustered_hi']:+.4f}] "
              f"({r['n_personas']} personas)"
              f"{'  EXCLUDES 0' if r['clustered_excludes_zero'] else '  includes 0'}")
    out["item3_mini_clustered"] = item3
    out["retraction_sentence"] = (
        "The retraction row is marginal at item level (lower bound $+0.0002$) and survives "
        "persona clustering."
        if item3["retracted"]["clustered_excludes_zero"] else
        "The retraction row is marginal at item level (lower bound $+0.0002$) and not "
        "separated under persona clustering.")

    out["registration"] = "registrations/ADDENDUM_R81.md section 11 @ cfe5415"
    jdump(out, OUT / "nb6_attribution.json")

    print(f"\n  ATTRIBUTION READING FIRED: {fired}")
    print(f"  -> {out['attribution_reading']['s43']}")
    print(f"  retraction: {out['retraction_sentence']}")
    print(f"\nwrote {OUT / 'nb6_attribution.json'}")


if __name__ == "__main__":
    main()
