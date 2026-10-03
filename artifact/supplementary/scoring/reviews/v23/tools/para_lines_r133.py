# -*- coding: utf-8 -*-
"""para_lines_r133.py -- built lines per main-text paragraph of Sections 4 to 8 (and per section), read from the margin line numbers of the built
paper_v23.pdf (the page-census instrument, run_gates.margin_lines), so section 6.8 of the brief (every rewritten paragraph no longer than the one it
replaces, in built lines) and the report's built-line delta per unit can be measured. A paragraph is located by the first four and the last four words
of its source text (reviews/v23/src/body_v23.tex, split as q_scan splits paragraphs); lines are counted as the numbered text lines between the two
anchors, inclusive (rows of the extracted text; a paragraph straddling a page break is starred and its count is approximate). Writes reviews/v23/results/para_lines_<tag>.json and prints the table. Read-only on the build.
Usage: python reviews/v23/tools/para_lines_r133.py <tag>
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))
import q_scan as Q  # noqa: E402
from run_gates import margin_lines  # noqa: E402

PDF = SUB / "paper_v23.pdf"
BODY = ROOT / "reviews" / "v23" / "src" / "body_v23.tex"


def words(s):
    s = Q.strip_refs(s)
    s = re.sub(r"\\claim\{", " ", s)
    s = re.sub(r"\$([^$]*)\$", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    s = re.sub(r"[{}~]", " ", s)
    s = s.replace("``", "").replace("''", "")
    return [w.lower() for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9.'-]*", s)]


def norm_row(txt):
    return " ".join(re.findall(r"[A-Za-z0-9][A-Za-z0-9.'-]*", txt.replace("\u2019", "'").replace("\ufb01", "fi").replace("\ufb02", "fl"))).lower()


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "now"
    import fitz
    doc = fitz.open(PDF)
    rows = []   # (page, line number, text): the margin numbers print every fifth line, so the rows between two numbered rows of a page are
    # given their numbers by interpolation when the spacing is consistent (no float rows between them); otherwise the row keeps None.
    for p in range(1, min(len(doc), 12) + 1):
        try:
            page_rows = [(n, norm_row(txt)) for n, y, txt in margin_lines(PDF, p)]
        except Exception:
            break
        idx = [i for i, (n, _) in enumerate(page_rows) if n is not None]
        nums = [None] * len(page_rows)
        for i in idx:
            nums[i] = page_rows[i][0]
        for a, b in zip(idx, idx[1:]):
            if page_rows[b][0] - page_rows[a][0] == b - a:
                for i in range(a + 1, b):
                    nums[i] = page_rows[a][0] + (i - a)
        if idx:   # the rows before the first and after the last numbered row, when contiguous with it
            a = idx[0]
            for i in range(a - 1, -1, -1):
                nums[i] = page_rows[a][0] - (a - i)
            b = idx[-1]
            for i in range(b + 1, len(page_rows)):
                nums[i] = page_rows[b][0] + (i - b)
        rows.extend((p, nums[i], page_rows[i][1]) for i in range(len(page_rows)))
    lines = BODY.read_text(encoding="utf-8").split("\n")
    s4 = next(i for i, l in enumerate(lines) if l.startswith("\\section{Setup}"))
    s9 = next(i for i, l in enumerate(lines) if l.startswith("\\section{Limitations}"))
    paras = Q.paragraphs(lines, s4, s9)
    secs = [(i, re.match(r"\\(sub)?section\{([^}]*)\}", lines[i]).group(2)) for i in range(s4, s9) if re.match(r"\\(sub)?section\{", lines[i])]
    out = []
    joined_rows = [" ".join(r[2] for r in rows[i:i + 3]) for i in range(len(rows))]   # a phrase may straddle a line break

    def find(phrase, start):
        for i in range(start, len(rows)):
            if phrase in joined_rows[i]:
                return i
        return None

    cursor = 0
    for ln, text in paras:
        w = words(text)
        if len(w) < 8:
            continue
        head, tail = " ".join(w[:4]), " ".join(w[-4:])
        sec = next((name for i, name in reversed(secs) if i < ln), "?")
        i0 = find(head, cursor)
        i1 = find(tail, i0) if i0 is not None else None
        if i0 is None or i1 is None:
            out.append(dict(line=ln, section=sec, head=head, tail=tail, lines=None, note="anchor not found"))
            continue
        # the tail anchor may sit on the row after its phrase started (joined rows): count numbered rows from i0 to the row holding the last word
        j1 = i1
        for k in range(i1, min(i1 + 3, len(rows))):
            if w[-1] in rows[k][2].split():
                j1 = k
        # rows are text lines (words grouped by baseline); a paragraph that straddles a page break is flagged, since the rows between then include the
        # page number and any float at the top of the next page
        n = j1 - i0 + 1
        straddle = rows[i0][0] != rows[j1][0]
        if straddle:
            n -= sum(1 for r in rows[i0:j1 + 1] if re.fullmatch(r"\d{1,2}", r[2].strip()))   # the page numbers
        out.append(dict(line=ln, section=sec, head=head, tail=tail, lines=n, page=rows[i0][0], margin=rows[i0][1], straddles_pages=straddle))
        cursor = j1 + 1
    (ROOT / "reviews" / "v23" / "results").mkdir(exist_ok=True)
    (ROOT / "reviews" / "v23" / "results" / f"para_lines_{tag}.json").write_text(json.dumps(out, indent=1), encoding="utf-8", newline="\n")
    by_sec = {}
    for r in out:
        print(f"  L{r['line']:4d} {r['section'][:28]:28s} {str(r.get('lines')):>4s}{'*' if r.get('straddles_pages') else ' '} {r['head']} ... {r['tail']}" + (f"  [{r['note']}]" if r.get("note") else ""))
        if r.get("lines"):
            by_sec[r["section"]] = by_sec.get(r["section"], 0) + r["lines"]
    print("per section (paragraph lines summed): " + "; ".join(f"{k}: {v}" for k, v in by_sec.items()))
    print(f"-> reviews/v23/results/para_lines_{tag}.json")


if __name__ == "__main__":
    main()
