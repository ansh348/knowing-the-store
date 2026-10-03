r"""page_census -- RETIRED 2026-09-09 (R86-2 ruling). Superseded by page_census_v2.py.

RETIRED. Do not gate on this file. `tools/page_census_v2.py` is the pinned instrument: it
anchors on \label{main-text-end}, gates on the PAGE the label resolves to, and prints the
review-line reading as a slack diagnostic only. This file is kept because reports before
2026-09-09 quote its numbers.

  WHAT IT READ, for anyone reading an older report: r77 `paper.pdf` 499, `paper_v2.pdf` at
  a5b3f78 470, and at 03e29bc 468. v2 reads 500, 470 and 469 on the same three. The two agree
  on a5b3f78 and differ by one elsewhere; where they differ, this file's `-layout` row grouping
  merged the numbered blank line before the heading and dropped it. 485 is page 9's last margin
  number under both conventions, so every past decision taken against the 485 boundary stands
  unchanged.

  WHY IT WAS RETIRED, beyond the offset. It anchors on a rendered heading rather than a label,
  against INSTRUMENT_RULES Rule 1, and it trusts row order in a layout extraction, which is a
  heuristic that silently shifted the answer in R86-1.

WHY THIS EXISTS. Before R76 the census method was unpinned: PAGE_CENSUS_V09.md describes
it in prose, no script implements it, and successive reports quoted absolute review-line
numbers that cannot be reproduced from the repo. R76 measured the R75 build at 492 where
the R75-V report had said 490. Neither number could be checked against the other, because
there was no instrument -- only two prose claims. This file is the instrument. From R76
onward the reported quantity is the count under THIS tool, and prior absolute claims are
annotated in DESCOPE_REPORT as method-unpinned.

METHOD (the R76 method, since it is the one that exists).
  1. The compiled PDF carries `lineno` margin numbers on every main-text line.
  2. ICLR 2027 excludes the AI use statement and the reproducibility statement from the
     9-page limit (official_style/iclr2027/iclr2027_conference.tex, lines 399 and 416),
     so the binding quantity is the last review line BEFORE the AI use statement.
  3. Locate the page carrying "AI USE STATEMENT"; take the greatest margin line number
     appearing above it on that page. That is the last main-text review line.
  4. The page-9 boundary is review line 485 (PAGE_CENSUS_V09.md headline: 54 review lines
     per page, last line on page 9 = 485). Slack = 485 - count; a positive `over` is a
     violation carried to the hand-pass.

ASSUMPTIONS, stated so a future reader can invalidate them rather than guess:
  - margin numbers are three digits and begin the extracted line (true from page ~2 on);
  - the AI use statement precedes the reproducibility statement (true in this template);
  - no table on the AI-statement page starts a line with a bare three-digit number.
  Assumption 3 is checked: the recovered numbers must be strictly increasing.

Usage:
    python tools/page_census.py paper.pdf [more.pdf ...]
Exit 0 always; this reports, it does not gate. The page limit is adjudicated by a human.
"""
import re, subprocess, sys, pathlib, tempfile

BOUNDARY = 485          # last review line on page 9 (PAGE_CENSUS_V09.md)
SEARCH_PAGES = range(8, 15)
MARKER = "AI USE STATEMENT"


def _page_numbers(pdf, pg):
    """Margin line numbers on one page, in order, via -layout so a number and the text it
    numbers stay on one extracted line."""
    with tempfile.TemporaryDirectory() as td:
        out = str(pathlib.Path(td) / "p.txt")
        subprocess.run(["pdftotext", "-layout", "-f", str(pg), "-l", str(pg), pdf, out],
                       check=True, capture_output=True)
        text = pathlib.Path(out).read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    nums = [(i, int(m.group(1))) for i, l in enumerate(lines)
            if (m := re.match(r"\s*(\d{3})(?:\s|$)", l))]
    return text, lines, nums


def census(pdf):
    """The last main-text review line, i.e. the greatest margin number strictly BEFORE the
    AI use statement and belonging to a line other than the statement's own.

    D-R81-2 (2026-08-30). The original method took the greatest margin number "above the
    marker on that page". When the statement is the FIRST line of its page that set is
    empty or contains only the statement's own number, and the tool returned the marker's
    line -- overstating the census by exactly one line. It now falls back to the preceding
    page in that case, and asserts the recovered line is not the marker's.
    """
    pdf = str(pdf)
    for pg in SEARCH_PAGES:
        text, lines, nums = _page_numbers(pdf, pg)
        if MARKER not in text:
            continue
        cut = next(i for i, l in enumerate(lines) if MARKER in l)
        marker_num = next((v for i, v in nums if i == cut), None)
        above = [v for i, v in nums if i < cut and v != marker_num]
        source = f"page {pg}"
        if not above:
            # the statement leads its own page: the last main-text line is on the page before
            _, _, prev = _page_numbers(pdf, pg - 1)
            above = [v for _, v in prev]
            source = f"page {pg - 1} (statement leads page {pg})"
            if not above:
                raise SystemExit(f"{pdf}: no margin line numbers before '{MARKER}' on "
                                 f"page {pg} or on page {pg - 1} -- lineno assumption broken")
        if above != sorted(above):
            raise SystemExit(f"{pdf}: recovered margin numbers are not increasing "
                             f"({above}) -- a non-line-number matched; method invalid here")
        last = max(above)
        if marker_num is not None and last >= marker_num:
            raise SystemExit(f"{pdf}: recovered last main-text line {last} is not before the "
                             f"statement's own line {marker_num} -- method invalid here")
        return {"pdf": pdf, "page": pg, "last_main_text_line": last, "source": source,
                "boundary": BOUNDARY, "over": last - BOUNDARY}
    raise SystemExit(f"{pdf}: '{MARKER}' not found on pages {SEARCH_PAGES.start}"
                     f"-{SEARCH_PAGES.stop - 1}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    rows = [census(p) for p in sys.argv[1:]]
    w = max(len(pathlib.Path(r["pdf"]).name) for r in rows)
    print(f"{'pdf':{w}s}  page  last main-text line  boundary  over")
    for r in rows:
        print(f"{pathlib.Path(r['pdf']).name:{w}s}  {r['page']:4d}  "
              f"{r['last_main_text_line']:19d}  {r['boundary']:8d}  {r['over']:+4d}")
    if len(rows) == 2:
        d = rows[1]["last_main_text_line"] - rows[0]["last_main_text_line"]
        print(f"\ndelta ({pathlib.Path(rows[1]['pdf']).name} vs "
              f"{pathlib.Path(rows[0]['pdf']).name}): {d:+d} review lines")
