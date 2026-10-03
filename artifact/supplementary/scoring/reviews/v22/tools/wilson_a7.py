# -*- coding: utf-8 -*-
"""wilson_a7.py -- the writing pass, Phase 4c (2026-09-15; the author's cold-read ruling, item 7): the Wilson 95% interval of the stale
rate on the "model rule, all states named and scored" row of Table 7 (AUX-DS-A7-REPORTED: 11 stale of 65 reached scorable obligations),
which NUMBERS_DS.md records as a count without an interval. Computed with the downstream experiment's own function
(ds_downstream/tools/amend4_header.py, wilson(k, n, z=1.959964), the function behind AUX-DS-AUDIT-RATES), no model call.
Usage: python reviews/v18/tools/wilson_a7.py  -> prints the interval at four decimals and the two-decimal form Table 7 prints.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "ds_downstream" / "tools" / "amend4_header.py"


def load_wilson():
    """The wilson() function of amend4_header.py, taken from its source without importing the module (the module runs its pipeline on import)."""
    text = SRC.read_text(encoding="utf-8")
    i = text.index("def wilson(k, n, z=1.959964):")
    j = text.index("\n\n\n", i)
    ns = {}
    exec("import math\n" + text[i:j], ns)
    return ns["wilson"]


def main():
    wilson = load_wilson()
    k, n = 11, 65
    lo, hi = wilson(k, n)
    checks = {(8, 42): [0.0998, 0.333], (16, 85): [0.1193, 0.2841]}   # AUX-DS-AUDIT-RATES prints these at three decimals: [0.100, 0.333], [0.119, 0.284]
    for (ck, cn), ref in checks.items():
        got = wilson(ck, cn)
        assert [round(g, 3) for g in got] == [round(r, 3) for r in ref], (ck, cn, got, ref)
    print(f"AUX-WP-WILSON-A7: {k} of {n} = {k / n:.4f}; Wilson 95% [{lo:.4f}, {hi:.4f}]; Table 7 prints [{lo:.2f},{hi:.2f}] (two decimals, half up)")
    print("check: the same function reproduces AUX-DS-AUDIT-RATES' intervals for 8 of 42 and 16 of 85 at three decimals")


if __name__ == "__main__":
    main()
