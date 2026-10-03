# -*- coding: utf-8 -*-
"""cost_payers_r129g.py -- candidate payers measured, none applied (R129, 2026-09-20): each candidate is a sentence of Section 5.2 before Figure 3's
placement point, deleted in a scratch build of the landing; the row reads whether the box returns to page 9 and where Figure 3 lands. The author
rules; nothing this script writes survives (port_v22.py regenerates the body at the end). Usage: python reviews/v22/tools/cost_payers_r129g.py
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

CANDIDATES = [
    ("(i) 5.2, the Figure 3 sentence of the all-states paragraph deleted",
     "Figure~\\ref{fig:perstate} uses mini's repeated-call rows, matching Table~\\ref{tab:cf-main}; mini still scores lower on expiry than on retraction. (Appendix~\\ref{app:counterfactual})\n",
     "(Appendix~\\ref{app:counterfactual})\n"),
    ("(ii) 5.2, the pooled-metric paragraph's last two sentences deleted",
     "Comparing \\pn{} against \\present{} alone keeps relevant content present on both sides.\nThat post hoc comparison preserves the model-versus-lookup pattern. (Appendix~\\ref{app:counterfactual})\n",
     "(Appendix~\\ref{app:counterfactual})\n"),
    ("(iii) 5.2, 'List length and emptiness carry signal without conveying what the names mean.' deleted",
     "List length and emptiness carry signal without conveying what the names mean.\n", ""),
]


def build():
    out = subprocess.run([sys.executable, str(TOOLS / "fine.py")], capture_output=True, text=True).stdout
    m = re.search(r"main-text-end page (\d+); fine number (\d+)", out)
    import fitz
    doc = fitz.open(ROOT / "iclr2027_monitoring_submission" / "paper_v22.pdf")
    f3 = [i + 1 for i in range(4, 10) if "Figure 3:" in doc[i].get_text()]
    return int(m.group(1)), int(m.group(2)), (f3[0] if f3 else "?")


def main():
    subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
    base = BODY.read_text(encoding="utf-8")
    rows = []
    try:
        single = "--combos" not in sys.argv
        for label, old, new in (CANDIDATES if single else []):
            assert base.count(old) == 1, label
            BODY.write_text(base.replace(old, new), encoding="utf-8", newline="\n")
            p, f, f3 = build()
            rows.append(f"| {label} | {p} | {f} | {485 - f:+d} | Figure 3 on page {f3} |")
            print(rows[-1], flush=True)
        for combo in ([(0, 1), (0, 2), (1, 2)] if not single else []):
            v = base
            for c in combo:
                v = v.replace(CANDIDATES[c][1], CANDIDATES[c][2])
            BODY.write_text(v, encoding="utf-8", newline="\n")
            p, f, f3 = build()
            rows.append(f"| {' and '.join(CANDIDATES[c][0].split(',')[0] for c in combo)} together | {p} | {f} | {485 - f:+d} | Figure 3 on page {f3} |")
            print(rows[-1], flush=True)
    finally:
        subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
        subprocess.run([sys.executable, str(TOOLS / "build_v22.py")], check=True, capture_output=True)
    md = OUT.read_text(encoding="utf-8")
    md += "\n## Candidate payers, measured and not applied (cost_payers_r129g.py)\n\n| candidate (on the landing) | page | fine number | against 485 | Figure 3 |\n|---|---:|---:|---:|---|\n" + "\n".join(rows) + "\n"
    OUT.write_text(md, encoding="utf-8", newline="\n")
    print("->", OUT)


if __name__ == "__main__":
    main()
