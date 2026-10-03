# -*- coding: utf-8 -*-
"""cost_payers_r129e.py -- one variant of the slack probe per call (R129, 2026-09-20): cost_payers_r129d.py was stopped by the system mid-run (memory
pressure), so each remaining variant is measured in its own foreground call and appended to reviews/v22/results/cost_payers_r129.md. Same instrument:
the slack in baselines before the box (a \\vspace probe; positive = fits with k more lines, negative = the lines to remove). Nothing it writes
survives: port_v22.py regenerates the body at the end. Usage: python reviews/v22/tools/cost_payers_r129e.py <variant>  (see PLAN)
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "reviews" / "v22" / "tools"
BODY = ROOT / "reviews" / "v22" / "src" / "body_v22.tex"
OUT = ROOT / "reviews" / "v22" / "results" / "cost_payers_r129.md"
sys.path.insert(0, str(TOOLS))
from cost_payers_r129 import VARIANTS  # noqa: E402
from cost_payers_r129d import apply, slack  # noqa: E402

PLAN = {"close": set(), "A1": {"A1"}, "A2": {"A2"}, "S4": {"S4"}, "B1": {"B1"}, "B2": {"B2"}, "C1": {"C1"}, "C2": {"C2"}, "C1C2": {"C1", "C2"},
        "B1C": {"B1", "C1", "C2"}, "B2C": {"B2", "C1", "C2"}, "noB2": {"A1", "A2", "S4", "B1", "C1", "C2"}, "noB1": {"A1", "A2", "S4", "B2", "C1", "C2"},
        "landing": {"A1", "A2", "S4", "B1", "B2", "C1", "C2"}}
LABEL = {"close": "the R128 close", "A1": "A1 alone", "A2": "A2 alone", "S4": "S4 alone", "B1": "B1 alone", "B2": "B2 alone", "C1": "C1 alone", "C2": "C2 alone",
         "C1C2": "C1 and C2", "B1C": "B1 with C1 and C2", "B2C": "B2 with C1 and C2", "noB2": "the landing without B2", "noB1": "the landing without B1", "landing": "the landing (every change)"}


def main():
    which = sys.argv[1]
    subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
    base = BODY.read_text(encoding="utf-8")
    close = base
    for name, new, old in VARIANTS:
        assert close.count(new) == 1, name
        close = close.replace(new, old)
    try:
        s = slack(apply(close, PLAN[which]))
    finally:
        subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
        subprocess.run([sys.executable, str(TOOLS / "build_v22.py")], check=True, capture_output=True)
    row = f"| {LABEL[which]} | {s:+d} |"
    md = OUT.read_text(encoding="utf-8")
    head = "\n## The costed table in lines of slack (cost_payers_r129d.py, finished one variant per call by cost_payers_r129e.py)\n\nSlack = the largest k such that k baselines added before the box still leave it on page 9; a negative value is the smallest k of baselines that must be removed for the box to return. The fine number itself is not linear (483 whenever the box fits, 492 whenever it moves), so this is the instrument.\n\n| variant (on the R128 close) | slack in lines |\n|---|---:|\n"
    if head not in md:
        md += head
    md += row + "\n"
    OUT.write_text(md, encoding="utf-8", newline="\n")
    print(row)


if __name__ == "__main__":
    main()
