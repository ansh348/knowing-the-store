# -*- coding: utf-8 -*-
"""margins_r124.py -- program R124 (the rulings on REPORT_R123, 2026-09-19), rulings B2 and B5: two readings from recorded rows, no model call.
  (1) Opus 5's per-state margins over the all-states lookup on the counterfactual set under the all-states summary (rows_OP5.jsonl, INDEXED-V3,
      the X4 collapse), whole set and per state, item-level and persona-grouped paired intervals (cf2_reader_score.score_lane with the v3 lookup
      of reviews/r122/tools/oai_score.py); gate: the whole-set margin equals the recorded +0.0323 (AUX-R103-MARGIN, tab:counterfactual).
  (2) GPT-4.1 mini at five draws (reviews/r122/rows/rows_MINI5.jsonl, INDEXED-V2 and INDEXED-V3): the per-state AUROC with the item-level and the
      persona-grouped bootstrap interval of the gain over blind (0.50 by construction), the reading Section 5's 'separates' sentence rests on
      (AUX-CF2-PERSTATE's convention: both intervals exclude zero); gate: the per-state points equal tab:mini-k5's.
Writes reviews/v21/results/margins_r124.json and prints both tables. Usage: python reviews/v21/tools/margins_r124.py
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
sys.path.insert(0, str(ROOT / "reviews" / "r122" / "tools"))
import cf2_reader_score as R  # noqa: E402
import oai_score as O  # noqa: E402
from common_e1r import auroc, boot_cluster_single  # noqa: E402

OUT = ROOT / "reviews" / "v21" / "results" / "margins_r124.json"


def r4(x):
    return round(float(x), 4)


def gain_intervals(v, y, g):
    """The per-state gain over blind: the AUROC's bootstrap interval minus 0.5, item-level (each item its own cluster) and persona-grouped."""
    item = boot_cluster_single(v, y, np.arange(len(v)))
    pers = boot_cluster_single(v, y, g)
    f = lambda c: {"ci_lo": r4(c["ci_lo"] - 0.5), "ci_hi": r4(c["ci_hi"] - 0.5), "excludes_zero": bool(c["ci_lo"] - 0.5 > 0 or c["ci_hi"] - 0.5 < 0)}
    return {"item": f(item), "persona": f(pers)}


def main():
    items, idx = R.cell()
    look3 = O.lookup_v3(items, idx)
    look2 = R.lookup_v2(items, idx)
    out = {}
    # (1) Opus 5 under the all-states summary against the all-states lookup
    op5 = R.score_lane(ROOT / "r82_counterfactual" / "cf2" / "rows" / "rows_OP5.jsonl", "INDEXED-V3", items, look3)
    assert op5["missing_items"] == 0 and op5["whole"] == 0.9079 and op5["lookup"] == 0.8756, (op5["whole"], op5["lookup"])
    assert r4(op5["vs_lookup"]["delta"]) == 0.0323, op5["vs_lookup"]["delta"]
    out["opus5_v3_vs_allstates_lookup"] = {"whole": {"model": op5["whole"], "lookup": op5["lookup"], "vs_lookup": op5["vs_lookup"]},
                                           "per_state": {s: {"model": op5["per_state"][s]["auroc"], "lookup": op5["per_state"][s]["lookup"], "vs_lookup": op5["per_state"][s]["vs_lookup"]} for s in R.STATES}}
    print("Opus 5 under the all-states summary minus the all-states lookup (item; persona):")
    print(f"  whole   {op5['whole']:.4f} vs {op5['lookup']:.4f}  {R.fmt_paired(op5['vs_lookup'])}")
    for s in R.STATES:
        p = op5["per_state"][s]
        print(f"  {s:12s} {p['auroc']:.4f} vs {p['lookup']:.4f}  {R.fmt_paired(p['vs_lookup'])}")
    # (2) GPT-4.1 mini at five draws: per-state gains over blind with both intervals
    y = np.array([it["y_nok"] for it in items], int); g = np.array([it["persona"] for it in items]); st = np.array([it["state"] for it in items])
    mini = {}
    for arm, look, gate in (("INDEXED-V2", look2, {"SUPERSESSION": 0.8793, "RETRACTION": 0.5761, "EXPIRY": 0.5594}),
                            ("INDEXED-V3", look3, {"SUPERSESSION": 0.8829, "RETRACTION": 0.8433, "EXPIRY": 0.6719})):
        col, census = R.collapse(ROOT / "reviews" / "r122" / "rows" / "rows_MINI5.jsonl", arm)
        v = np.array([col[it["item_id"]] for it in items], float)
        mini[arm] = {}
        print(f"GPT-4.1 mini, five draws, {arm}: per-state AUROC and the gain over blind (item; persona)")
        for s in R.STATES:
            m = st == s
            a = r4(auroc(v[m], y[m])); assert a == gate[s], (arm, s, a, gate[s])
            gi = gain_intervals(v[m], y[m], g[m])
            mini[arm][s] = {"auroc": a, "gain": r4(a - 0.5), "item_ci": gi["item"], "persona_ci": gi["persona"], "separates": bool(gi["item"]["excludes_zero"] and gi["persona"]["excludes_zero"])}
            print(f"  {s:12s} {a:.4f}  gain {a - 0.5:+.4f}  [{gi['item']['ci_lo']:+.4f}, {gi['item']['ci_hi']:+.4f}]; [{gi['persona']['ci_lo']:+.4f}, {gi['persona']['ci_hi']:+.4f}]  separates {mini[arm][s]['separates']}")
    out["mini_k5_per_state_gain"] = mini
    OUT.parent.mkdir(exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(out, indent=1, sort_keys=True, default=float))
    print("->", OUT)


if __name__ == "__main__":
    main()
