# -*- coding: utf-8 -*-
"""cost_payers_r129d.py -- the costed table in lines (R129, 2026-09-20). The fine number is not linear in lines under flushbottom: it reads 483 whenever
the builders box fits on page 9 and 492 whenever the box moves whole to page 10, so a change's cost has to be read as slack. For each variant this
script finds the slack in baselines: the largest k such that a \\vspace{k\\baselineskip} inserted before the box still leaves the box on page 9
(positive slack), or the smallest k such that \\vspace{-k\\baselineskip} brings it back (a deficit, printed negative). Scratch builds only; nothing it
writes survives (port_v22.py regenerates the body at the end). Usage: python reviews/v22/tools/cost_payers_r129d.py
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "reviews" / "v22" / "tools"
BODY = ROOT / "reviews" / "v22" / "src" / "body_v22.tex"
OUT = ROOT / "reviews" / "v22" / "results" / "cost_payers_r129.md"
sys.path.insert(0, str(TOOLS))
from cost_payers_r129 import VARIANTS, fine  # noqa: E402

POOLED = "\\claim{The pooled metric rewards readers that miss the obligation.}\n"
ANCHOR = "%% R126: the box as in the inbox (the R124-F wording)"
MAXK = 9


def apply(close, names):
    v = close
    for name, new, old in VARIANTS:
        if name[:2] in names:
            v = v.replace(old, new) if old else v.replace(POOLED, new + POOLED, 1)
    return v


def fits(text, k):
    BODY.write_text(text.replace(ANCHOR, f"\\vspace{{{k}\\baselineskip}}\n" + ANCHOR) if k else text, encoding="utf-8", newline="\n")
    p, f = fine()
    return p == 9 and f <= 485


def slack(text):
    if fits(text, 0):
        k = 0
        while k < MAXK and fits(text, k + 1):
            k += 1
        return k
    k = 1
    while k <= MAXK and not fits(text, -k):
        k += 1
    return -k


def main():
    subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
    base = BODY.read_text(encoding="utf-8")
    close = apply(base, set())
    for name, new, old in VARIANTS:
        assert close.count(new) == 1, name
        close = close.replace(new, old)
    plan = [("the R128 close", set()), ("A1 alone", {"A1"}), ("A2 alone", {"A2"}), ("S4 alone", {"S4"}), ("B1 alone", {"B1"}), ("B2 alone", {"B2"}),
            ("C1 alone", {"C1"}), ("C2 alone", {"C2"}), ("C1 and C2", {"C1", "C2"}), ("the landing without B2", {"A1", "A2", "S4", "B1", "C1", "C2"}),
            ("the landing without B1", {"A1", "A2", "S4", "B2", "C1", "C2"}), ("the landing (every change)", {"A1", "A2", "S4", "B1", "B2", "C1", "C2"})]
    rows = []
    try:
        for label, names in plan:
            s = slack(apply(close, names))
            rows.append(f"| {label} | {s:+d} |")
            print(rows[-1], flush=True)
    finally:
        subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
        subprocess.run([sys.executable, str(TOOLS / "build_v22.py")], check=True, capture_output=True)
    md = OUT.read_text(encoding="utf-8")
    md += ("\n## The costed table in lines of slack (cost_payers_r129d.py)\n\nSlack = the largest k such that k baselines added before the box still leave it on page 9; "
           "a negative value is the smallest k of baselines that must be removed for the box to return. The fine number itself is not linear (483 whenever the box fits, 492 whenever it moves), so this is the instrument.\n\n"
           "| variant (on the R128 close) | slack in lines |\n|---|---:|\n" + "\n".join(rows) + "\n")
    OUT.write_text(md, encoding="utf-8", newline="\n")
    print("->", OUT)


if __name__ == "__main__":
    main()
