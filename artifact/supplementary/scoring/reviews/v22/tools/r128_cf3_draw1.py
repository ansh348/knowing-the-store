# -*- coding: utf-8 -*-
"""r128_cf3_draw1.py -- R128 B8 (2026-09-20; offline, $0): Opus 5's pooled expiry row (CF-2's 30 pairs + CF-3's 14 = 44 pairs, 132 items) read at
draw 1 on every pair, beside the recorded pooled row (k = 5 on the CF-2 rows, k = 1 on the CF-3 rows; AUX-CF3-POOLED). Exactly cf3_score.score_set
on the same items with one change: the CF-2 lane is built from the draw-1 rows of r82_counterfactual/cf2/rows/rows_OP5.jsonl (status OK), where the
recorded row averages the five draws. Blind is the recorded one-call-per-question row in both. Writes reviews/v22/results/r128_cf3_draw1.json.
Usage: python reviews/v22/tools/r128_cf3_draw1.py
"""
from __future__ import annotations

import collections
import io
import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("r82_counterfactual/cf3", "r82_counterfactual/tools", "r82_counterfactual", "e1r_robustness/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
import cf3_score as C  # noqa: E402
import score_cf as S  # noqa: E402

OUT = ROOT / "reviews" / "v22" / "results" / "r128_cf3_draw1.json"


def lane_draw1(path):
    """{(unit_id, arm): the draw-1 score} from a rows file (status OK); a unit with no draw-1 row is skipped."""
    per = collections.defaultdict(dict)
    for line in io.open(path, encoding="utf-8"):
        r = json.loads(line)
        if r.get("status") == "OK" and r.get("nok") is not None:
            per[(r["unit_id"], r["arm"])][r["draw"]] = r["nok"]
    return {k: float(d[1]) for k, d in per.items() if 1 in d}


def main():
    it2, idx2 = C.load_cell(C.CF2, "cf2"); it3, idx3 = C.load_cell(C.CF3, "cf3")
    idx = {"cf2": idx2, "cf3": idx3}
    exp2 = [it for it in it2 if it["state"] == "EXPIRY"]; assert len(exp2) == 90 and len(it3) == 42
    S.R82 = C.CF2; rec2 = {code: S.load_lane(code) for code in C.LANES}
    S.R82 = C.CF3; rec3 = {code: S.load_lane(code) for code in C.LANES}
    d1_2 = lane_draw1(C.CF2 / "rows" / "rows_OP5.jsonl")
    d1_3 = lane_draw1(C.CF3 / "rows" / "rows_OP5.jsonl")
    op5 = next(code for code, model in C.LANES.items() if "opus" in model)
    lanes_rec = {"cf2": rec2, "cf3": rec3}
    lanes_d1 = {"cf2": dict(rec2, **{op5: d1_2}), "cf3": dict(rec3, **{op5: d1_3})}
    res = {"recorded": C.score_set(exp2 + it3, idx, lanes_rec, "pooled expiry, recorded (Opus 5 k = 5 on CF-2's rows, k = 1 on CF-3's)"),
           "draw1": C.score_set(exp2 + it3, idx, lanes_d1, "pooled expiry, Opus 5 at draw 1 on every pair (CF-2's draw-1 rows; CF-3's single call)"),
           "draw1_cf2_expiry": C.score_set(exp2, idx, lanes_d1, "CF-2 expiry slice at draw 1: 30 pairs, 90 items (Opus 5's draw-1 rows)")}
    model = C.LANES[op5]
    for k in ("recorded", "draw1", "draw1_cf2_expiry"):
        res[k] = {"label": res[k]["label"], "n": res[k]["n"], "pairs": res[k]["pairs"], "pos": res[k]["pos"], "personas": res[k]["personas"],
                  "opus": {arm: {kk: vv for kk, vv in res[k]["models"][model][arm].items() if kk in ("indexed", "indexed_ci_persona", "delta", "item_ci", "persona_ci", "both_exclude_zero")}
                           for arm in ("v2", "v3", "v2r")}, "blind_auroc": res[k]["models"][model]["blind_auroc"]}
    # the recorded reading reproduces AUX-CF3-POOLED
    rec = res["recorded"]["opus"]
    assert (rec["v2"]["indexed"], rec["v3"]["indexed"], rec["v2r"]["indexed"]) == (0.5914, 0.9232, 0.6068), rec
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    for k in ("recorded", "draw1", "draw1_cf2_expiry"):
        print(k, res[k]["label"])
        for arm in ("v2", "v3", "v2r"):
            a = res[k]["opus"][arm]
            print(f"  {arm}: AUROC {a['indexed']} persona CI [{a['indexed_ci_persona']['ci_lo']:.4f}, {a['indexed_ci_persona']['ci_hi']:.4f}]; "
                  f"delta vs blind {a['delta']:+.4f} item [{a['item_ci']['ci_lo']:+.4f}, {a['item_ci']['ci_hi']:+.4f}] persona [{a['persona_ci']['ci_lo']:+.4f}, {a['persona_ci']['ci_hi']:+.4f}]")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
