# -*- coding: utf-8 -*-
"""reach_rows_r123.py -- program R123 (the v21 update and writing pass, 2026-09-19): the recorded downstream policies' reach rows for the
Section 9 reach table, read from the recorded downstream record (ds_downstream/stage1.json per_item: view_size, reach, gold_in_view;
no model call, nothing re-run), and the reconciliation of the two view-size denominators the paper had used: the mean over all 661
questions (the budget the R122 matched rows share, 5.4342 for the model rule) and the mean over the 104 obligations alone (7.08 for the
model rule, tab:ds-body-lower). Gates: the model rule reproduces AUX-DS-REACH (85 of 104), AUX-DS-PRESENT (65 of 174) and R122's
target_mean_661; the top-five view reproduces 54 of 104 and 5.00 lines. Writes reviews/v21/results/reach_rows_r123.json and prints the rows.
Usage: python reviews/v21/tools/reach_rows_r123.py
"""
from __future__ import annotations

import io
import json
import pathlib
import statistics

ROOT = pathlib.Path(__file__).resolve().parents[3]
ST1 = ROOT / "ds_downstream" / "stage1.json"
GR = ROOT / "reviews" / "r122" / "results" / "gate_reach.json"
OUT = ROOT / "reviews" / "v21" / "results" / "reach_rows_r123.json"
POLICIES = ("ALWAYS", "LOOKUP", "MODEL", "ORACLE")


def main():
    per = json.load(io.open(ST1, encoding="utf-8"))["per_item"]
    gr = json.load(io.open(GR, encoding="utf-8"))
    assert len(per) == 661, len(per)
    out = {}
    for p in POLICIES:
        sizes = [per[i][p]["view_size"] for i in per]
        obl = {i: per[i][p] for i in per if per[i][p]["reach"] is not None}
        pres = {i: per[i][p] for i in per if per[i][p]["gold_in_view"] is not None}
        assert len(obl) == 104 and len(pres) == 174, (p, len(obl), len(pres))
        out[p] = {"reach": sum(1 for r in obl.values() if r["reach"]), "n_obl": 104,
                  "rate": sum(1 for r in obl.values() if r["reach"]) / 104,
                  "licensed_in_view": sum(1 for r in pres.values() if r["gold_in_view"]), "n_lic": 174,
                  "licensed_rate": sum(1 for r in pres.values() if r["gold_in_view"]) / 174,
                  "mean_lines_661": statistics.mean(sizes),
                  "mean_lines_104": statistics.mean(obl[i]["view_size"] for i in obl)}
    # gates against the recorded ledger values and R122's target
    assert out["MODEL"]["reach"] == 85 and out["MODEL"]["licensed_in_view"] == 65, out["MODEL"]
    assert abs(out["MODEL"]["mean_lines_661"] - gr["meta"]["target_mean_661"]) < 1e-9, (out["MODEL"]["mean_lines_661"], gr["meta"]["target_mean_661"])
    assert abs(out["MODEL"]["mean_lines_104"] - gr["meta"]["target_mean_104"]) < 1e-9
    assert out["ALWAYS"]["reach"] == 54 and out["ALWAYS"]["mean_lines_661"] == 5.0 and out["ALWAYS"]["licensed_in_view"] == 65
    assert out["LOOKUP"]["reach"] == 85 and out["ORACLE"]["reach"] == 99
    res = {"source": "ds_downstream/stage1.json per_item (view_size, reach, gold_in_view), the recorded downstream record; no model call",
           "denominators": {"mean_lines_661": "mean view size over all 661 questions of the full obligation set (the budget the R122 matched rows share)",
                            "mean_lines_104": "mean view size over the 104 obligations alone (the 'about seven records' of the earlier Section 9 and tab:ds-body-lower)"},
           "policies": out}
    OUT.parent.mkdir(exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1, sort_keys=True))
    for p, r in out.items():
        print(f"{p:8s} reach {r['reach']:3d}/104 = {r['rate']:.4f}   licensed in view {r['licensed_in_view']}/174 = {r['licensed_rate']:.4f}   mean lines 661 {r['mean_lines_661']:.4f}   104 {r['mean_lines_104']:.4f}")
    print("->", OUT)


if __name__ == "__main__":
    main()
