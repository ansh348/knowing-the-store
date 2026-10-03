# -*- coding: utf-8 -*-
"""para_compare_r133.py -- section 6.8 of the brief (every rewritten paragraph shorter than or equal to the one it replaces, in built lines): for every
paragraph-level edit in reviews/v23/results/port_r133_log.json, the old paragraph's rows in the v22 build (iclr2027_monitoring_submission/paper_v22.pdf,
the R131 close) beside the new paragraph's rows in the v23 build, each located by its first three and last three words in the PDF text layer (rows
grouped by baseline; a paragraph straddling a page break is starred and its count is approximate, floats between the two anchors being counted too).
Usage: python reviews/v23/tools/para_compare_r133.py
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))
from run_gates import margin_lines  # noqa: E402
from para_lines_r133 import words, norm_row  # noqa: E402

LOG = ROOT / "reviews" / "v23" / "results" / "port_r133_log.json"


def rows_of(pdf):
    import fitz
    doc = fitz.open(pdf)
    rows = []
    for p in range(1, min(len(doc), 12) + 1):
        try:
            rows += [(p, norm_row(txt)) for n, y, txt in margin_lines(pdf, p)]
        except Exception:
            break
    return rows


def locate(rows, text):
    w = words(text)
    if len(w) < 6:
        return None
    head, tail = " ".join(w[:3]), " ".join(w[-3:])
    joined = [" ".join(r[1] for r in rows[i:i + 3]) for i in range(len(rows))]
    i0 = next((i for i in range(len(rows)) if head in joined[i]), None)
    if i0 is None:
        return None
    i1 = next((i for i in range(i0, len(rows)) if tail in joined[i]), None)
    if i1 is None:
        return None
    j1 = i1
    for k in range(i1, min(i1 + 3, len(rows))):
        if w[-1] in rows[k][1].split():
            j1 = k
    n = j1 - i0 + 1
    straddle = rows[i0][0] != rows[j1][0]
    if straddle:
        n -= sum(1 for r in rows[i0:j1 + 1] if re.fullmatch(r"\d{1,2}", r[1].strip()))
    return n, straddle, rows[i0][0]


def main():
    old_rows, new_rows = rows_of(SUB / "paper_v22.pdf"), rows_of(SUB / "paper_v23.pdf")
    log = json.loads(LOG.read_text(encoding="utf-8"))
    print(f"{'unit':5s} {'section':10s} {'old':>6s} {'new':>6s}  paragraph")
    for e in log["edits"]:
        if e["file"] != "body" or not e["old"] or not e["new"] or len(words(e["old"])) < 12 or len(words(e["new"])) < 12:
            continue
        if e["unit"] in ("swaps", "s12"):
            continue
        a, b = locate(old_rows, e["old"]), locate(new_rows, e["new"])
        fa = f"{a[0]}{'*' if a[1] else ' '}" if a else "?"
        fb = f"{b[0]}{'*' if b[1] else ' '}" if b else "?"
        flag = "" if (a and b and b[0] <= a[0]) else ("  LONGER" if (a and b) else "")
        print(f"{e['unit']:5s} {e['section']:10s} {fa:>6s} {fb:>6s}  {' '.join(words(e['new'])[:6])}{flag}")


if __name__ == "__main__":
    main()
