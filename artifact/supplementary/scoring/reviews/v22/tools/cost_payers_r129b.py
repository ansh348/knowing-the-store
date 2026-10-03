# -*- coding: utf-8 -*-
"""cost_payers_r129b.py -- the shortfall behind the costed table (R129, 2026-09-20): the builders box is one unbreakable minipage, so once the main
text spills it moves whole to page 10 and the fine number reads the same (-7) whether the spill is one line or six. This script measures the spill in
lines by removing trailing lines from the landing in a scratch variant that no ruling could adopt (a \\vspace pull-up of k baselines before the box),
so the author sees how many lines the landing is short. Nothing it writes survives: port_v22.py regenerates the body at the end.
Usage: python reviews/v22/tools/cost_payers_r129b.py
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
ANCHOR = "%% R126: the box as in the inbox (the R124-F wording)"


def fine():
    out = subprocess.run([sys.executable, str(TOOLS / "fine.py")], capture_output=True, text=True).stdout
    m = re.search(r"main-text-end page (\d+); fine number (\d+)", out)
    return int(m.group(1)), int(m.group(2))


def main():
    subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
    base = BODY.read_text(encoding="utf-8")
    assert base.count(ANCHOR) == 1
    rows = []
    try:
        for k in (1, 2, 3, 4, 5, 6):
            BODY.write_text(base.replace(ANCHOR, f"\\vspace{{-{k}\\baselineskip}}\n" + ANCHOR), encoding="utf-8", newline="\n")
            p, f = fine()
            rows.append(f"| the landing with {k} baseline{'s' if k > 1 else ''} pulled up before the box (scratch, not a payer) | {p} | {f} | {485 - f:+d} |")
            print(rows[-1], flush=True)
            if p == 9:
                break
    finally:
        subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
        subprocess.run([sys.executable, str(TOOLS / "build_v22.py")], check=True, capture_output=True)
    md = OUT.read_text(encoding="utf-8")
    md += "\n## The spill in lines (cost_payers_r129b.py)\n\nThe box moves whole, so the fine number reads -7 for any spill; the rows below pull the box up by k baselines in a scratch build to find the first k that fits.\n\n| variant | page | fine number | against 485 |\n|---|---:|---:|---:|\n" + "\n".join(rows) + "\n"
    OUT.write_text(md, encoding="utf-8", newline="\n")
    print("->", OUT)


if __name__ == "__main__":
    main()
