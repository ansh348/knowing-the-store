# -*- coding: utf-8 -*-
"""cost_payers_r129f.py -- where the missing lines are (R129, 2026-09-20): in the landing Figure 3 moves from page 6 to page 7 (beside Table 2) and the
packing changes, which is why the landing reads 5 lines short while B1 and B2 cost 3 lines each on the close and the payers pay none. This probe
removes k baselines inside Section 5.2 (after the hybrid paragraph, a scratch \\vspace, not a payer) and reads where Figure 3 lands and whether the
box returns, so the author knows how many lines a Section 5 payer must pay. Nothing it writes survives. Usage: python reviews/v22/tools/cost_payers_r129f.py
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
ANCHOR = "\\claim{The pooled metric rewards readers that miss the obligation.}\n"


def probe(base, k):
    BODY.write_text(base.replace(ANCHOR, f"\\vspace{{-{k}\\baselineskip}}\n" + ANCHOR), encoding="utf-8", newline="\n")
    out = subprocess.run([sys.executable, str(TOOLS / "fine.py")], capture_output=True, text=True).stdout
    m = re.search(r"main-text-end page (\d+); fine number (\d+)", out)
    import fitz
    doc = fitz.open(ROOT / "iclr2027_monitoring_submission" / "paper_v22.pdf")
    f3 = [i + 1 for i in range(4, 10) if "Figure 3:" in doc[i].get_text()]
    return int(m.group(1)), int(m.group(2)), f3


def main():
    subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
    base = BODY.read_text(encoding="utf-8")
    assert base.count(ANCHOR) == 1
    rows = []
    try:
        for k in (1, 2, 3, 4, 5):
            p, f, f3 = probe(base, k)
            rows.append(f"| the landing with {k} baseline{'s' if k > 1 else ''} removed inside Section 5.2 (scratch, not a payer) | {p} | {f} | Figure 3 on page {f3[0] if f3 else '?'} |")
            print(rows[-1], flush=True)
            if p == 9:
                break
    finally:
        subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
        subprocess.run([sys.executable, str(TOOLS / "build_v22.py")], check=True, capture_output=True)
    md = OUT.read_text(encoding="utf-8")
    md += ("\n## Where the lines go (cost_payers_r129f.py)\n\nIn the landing Figure 3 moves from page 6 to page 7 (the close and the landing without B2 keep it on page 6), so the deficit is not the sum of the parts. "
           "Lines removed inside Section 5.2, before the figure's placement point:\n\n| variant | page | fine number | Figure 3 |\n|---|---:|---:|---|\n" + "\n".join(rows) + "\n")
    OUT.write_text(md, encoding="utf-8", newline="\n")
    print("->", OUT)


if __name__ == "__main__":
    main()
