# -*- coding: utf-8 -*-
"""sup_margins.py -- the author's ruling 3 of 19 September (program R118): the supersession-only margin over the name lookup for all five
models on the counterfactual set, with both intervals, from the recorded rows (GPT-4.1 mini rows_MINI.jsonl, Haiku 4.5 rows_H45.jsonl,
Opus 5 rows_OP5.jsonl: the INDEXED-V2 arm, the X4 collapse) and the E5 rows (rows_LUNA.jsonl, rows_SOL.jsonl), through
r82_counterfactual/tools/cf2_reader_score.py (cf2_score.paired: item-level and persona-grouped bootstrap, 1,000 draws, seed 42).
Read-only; no model call. Writes reviews/r117/results/sup_margins.json and prints the table. Gate: each model's whole-set AUROC must
equal its recorded value (Table 1 / AUX-CF2-OAI-*)."""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
import cf2_reader_score as R  # noqa: E402

ROWS = ROOT / "r82_counterfactual" / "cf2" / "rows"
LANES = [("GPT-4.1 mini", "rows_MINI.jsonl", 0.7167), ("Haiku 4.5", "rows_H45.jsonl", 0.7566), ("Opus 5", "rows_OP5.jsonl", 0.8405),
         ("GPT-5.6 Sol", "rows_SOL.jsonl", 0.8500), ("GPT-5.6 Luna", "rows_LUNA.jsonl", 0.8417)]
OUT = ROOT / "reviews" / "r117" / "results" / "sup_margins.json"


def main():
    items, idx = R.cell()
    look = R.lookup_v2(items, idx)
    res = {}
    print(f"{'model':14s} {'whole':>7s} {'sup AUROC':>9s} {'lookup':>7s}  sup minus lookup (item; persona)                        {'reliable':>8s}   ret minus lookup   exp minus lookup")
    for name, fn, gate in LANES:
        r = R.score_lane(ROWS / fn, "INDEXED-V2", items, look)
        assert r["missing_items"] == 0, (name, r["missing_items"])
        assert r["whole"] == gate, ("GATE: whole-set AUROC", name, r["whole"], gate)
        ps = r["per_state"]
        sup = ps["SUPERSESSION"]; ret = ps["RETRACTION"]; exp = ps["EXPIRY"]
        rel = sup["vs_lookup"]["item_ci"]["excludes_zero"] and sup["vs_lookup"]["persona_ci"]["excludes_zero"]
        res[name] = {"whole": r["whole"], "census": r["census"], "supersession": sup, "retraction": ret, "expiry": exp, "reliable_sup_margin": bool(rel)}
        print(f"{name:14s} {r['whole']:7.4f} {sup['auroc']:9.4f} {sup['lookup']:7.4f}  {R.fmt_paired(sup['vs_lookup']):58s} {str(rel):>8s}   {ret['vs_lookup']['delta']:+.4f}            {exp['vs_lookup']['delta']:+.4f}")
    OUT.parent.mkdir(exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(res, indent=1, sort_keys=True, default=float))
    print("->", OUT)


if __name__ == "__main__":
    main()
