# -*- coding: utf-8 -*-
"""fig3_data_r131.py -- Figure 3 on the matched metric (program R131, 2026-09-20; the author's brief 'KtS R131', section D): copies
reviews/r125/results/fig3_data_matched.tex (written by reviews/r125/tools/r125_t1_report.py from r125_matched.json; the schema of fig3_data.tex)
to reviews/v22/src/fig3_data_matched.tex, after asserting every value in it against reviews/r125/results/r125_matched.json (the per-state matched
AUROC of PN against PRESENT, four decimals). The pooled data file, reviews/v22/src/fig3_data.tex (fig3_data.py), stays: build_v22.py splices it at
%%FIG3-DATA-POOLED%% in Appendix C.2 with the table macros renamed (\\figthreeSupPooled, \\figthreeAllPooled), and the matched file at
%%FIG3-DATA-MATCHED%% in the body. Usage: python reviews/v22/tools/fig3_data_r131.py
"""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "r125" / "results" / "fig3_data_matched.tex"
OUT = ROOT / "reviews" / "v22" / "src" / "fig3_data_matched.tex"
M = json.load(open(ROOT / "reviews" / "r125" / "results" / "r125_matched.json", encoding="utf-8"))["readers"]
KEYS = {"mini": "MINI5_v2", "haiku": "H45_v2", "luna": "LUNA_v2", "sol": "SOL_v2", "opus": "OP5_v2", "lookup": "LOOKUP_v2", "count": "CR-nb1_v2"}
KEYS_ALL = {"mini": "MINI5_v3", "haiku": "H45_v3", "opus": "OP5_v3", "lookup": "ALLSTATES_v3"}
STATES = ["SUPERSESSION", "RETRACTION", "EXPIRY"]


def table(text, macro):
    m = re.search(r"\\pgfplotstableread\[col sep=comma\]\{\n((?:[^\n}]*\n)*?)\}" + re.escape(macro), text)
    rows = [r.split(",") for r in m.group(1).strip("\n").split("\n")]
    head = rows[0]
    return {row[1].upper(): {head[i]: float(row[i]) for i in range(2, len(head))} for row in rows[1:]}


def main():
    text = SRC.read_text(encoding="utf-8").replace("\r\n", "\n")
    sup = table(text, "\\figthreeSup"); allst = table(text, "\\figthreeAll")
    n = 0
    for st in STATES:
        for col, key in KEYS.items():
            v = M[key]["pn_vs_present"]["per_state"][st]["matched"]
            assert abs(sup[st][col] - v) < 5e-5, (st, col, sup[st][col], v); n += 1
        for col, key in KEYS_ALL.items():
            v = M[key]["pn_vs_present"]["per_state"][st]["matched"]
            assert abs(allst[st][col] - v) < 5e-5, (st, col, allst[st][col], v); n += 1
    assert min(sup["EXPIRY"].values()) == sup["EXPIRY"]["mini"] == 0.4, sup["EXPIRY"]   # the y axis must reach 0.35 (the brief, section D)
    OUT.write_text("%% R131 (2026-09-20): copied from reviews/r125/results/fig3_data_matched.tex by reviews/v22/tools/fig3_data_r131.py after checking every value against r125_matched.json.\n" + text, encoding="utf-8", newline="\n")
    print(f"{n} values checked against r125_matched.json -> {OUT}")


if __name__ == "__main__":
    main()
