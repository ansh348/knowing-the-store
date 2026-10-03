# -*- coding: utf-8 -*-
"""section_lines.py -- lines per main-text section on the built paper_v22.pdf, read from the margin line numbers (the page-census instrument),
so a page-budget step can be measured section by section. Read-only. Usage: python reviews/v19/tools/section_lines.py [pdf]"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "v22" / "tools"))
from run_gates import margin_lines  # noqa: E402

PDF = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "iclr2027_monitoring_submission" / "paper_v22.pdf"
HEADS = ["1 INTRODUCTION", "2 RELATED WORK", "3 FRAMEWORK", "4 SETUP", "5 THE CLEAN TEST", "6 TWO ROUTES", "7 WHAT BACKENDS", "8 REPLICATION", "9 ACTING", "10 LIMITATIONS", "11 CONCLUSION", "AI USE STATEMENT"]


def main():
    import fitz
    doc = fitz.open(PDF)
    rows = []
    for p in range(1, min(len(doc), 13) + 1):
        try:
            for n, y, txt in margin_lines(PDF, p):
                rows.append((p, n, txt))
        except Exception:
            break
    marks = []
    for i, (p, n, txt) in enumerate(rows):
        u = txt.upper()
        for h in HEADS:
            if u.startswith(h) and not any(m[0] == h for m in marks):
                marks.append((h, p, n, i))
    for j, (h, p, n, i) in enumerate(marks):
        nxt = marks[j + 1][3] if j + 1 < len(marks) else len(rows)
        span = [r[1] for r in rows[i:nxt] if r[1] is not None]
        print(f"{h:22s} page {p:2d} margin {n}  lines in span {len(rows[i:nxt]):3d}  (margin {min(span) if span else '-'} to {max(span) if span else '-'})")


if __name__ == "__main__":
    main()
