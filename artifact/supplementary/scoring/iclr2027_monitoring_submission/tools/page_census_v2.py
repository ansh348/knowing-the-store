r"""page_census_v2 -- PINNED main-text page-limit instrument, anchored on a label.

PINNED 2026-09-09 (R86-2 ruling). This file is the authority; `page_census.py` (v1) is
retired. Phase 4 gates on the PAGE CHECK below, with the slack diagnostic printed beside it.

THE GATE. ICLR 2027 allows nine pages of main text and excludes the AI use, ethics and
reproducibility statements. The official condition is therefore a page, not a line:

    the page recorded for \label{main-text-end} in the .aux must be 9 or less.

That quantity is invariant to everything below the label, which is what a main-text page
limit must be. It is read from `\newlabel{main-text-end}{{sec}{PAGE}...}`, so it is the
label anchor `INSTRUMENT_RULES.md` Rule 1 prescribes, and a heading rename cannot touch it.

THE SLACK DIAGNOSTIC. The review-line reading is reported as `485 - reading` and gates
nothing. 485 is page 9's last margin number (PAGE_CENSUS_V09.md: 54 review lines per page).

  DATED NOTE, 2026-09-09. The line reading can move by one when material BELOW the label
  changes length. R86-1 grew the AI use statement from one paragraph to six; that pushed the
  reproducibility statement to page 10, LaTeX redistributed the stretchable space above the
  `\subsection*`, and the reading moved from 470 to 469 although main text was byte-identical
  (`\begin{document}` .. `\label{main-text-end}` hashing to 6c7895ad4ed3e7e3 in both builds),
  page boundaries were identical, and page 9 carried the same 54 margin numbers. A reading of
  486 while the label is on page 9 is therefore a PASS: it means the numbered blank line before
  the statement heading fell on page 10, not that main text overran. Read the page, then the
  slack.

  RECORDED READINGS, 2026-09-09, under this tool, with a matcher correction applied the same
  day (see below): r77 `paper.pdf` **500**; `paper_v2.pdf` at a5b3f78 **470**; at 03e29bc
  **469**. v1 read 499, 470 and 468 on those three files.

  So the two tools AGREE on a5b3f78 and differ by one on the other two. The earlier claim that
  the offset was a constant +1 on every lineage was wrong, and it was wrong because this tool's
  first heading matcher was fragile: it slid a window over a y-sorted word list, and the ICLR
  style sets the heading in small caps whose glyph runs carry slightly different baselines, so
  an unrelated word landing between them broke the run. It now uses PyMuPDF's own text search,
  clusters the per-quad rectangles it returns onto one line, and falls back to the word window.
  Where v1 and this tool still differ, the cause is the one already recorded: v1's `-layout`
  row grouping merges the numbered blank line before the heading and drops it.

  The substantive finding survives the correction and is now measured at one line rather than
  two: between a5b3f78 and 03e29bc this tool reads 470 then 469, for main text that hashes
  identically, so the review-line reading is not invariant to material below the label. That is
  why the gate is the page and the reading is only a diagnostic. 485 is page 9's last margin
  number under both conventions, so every past decision taken against the 485 boundary stands.

METHOD, for the diagnostic.
  1. `<stem>.tex`: find `\label{main-text-end}`. The first `\subsection*{NAME}` after it is
     the first uncounted statement. NAME is READ FROM SOURCE, never hard-coded.
  2. `<stem>.aux`: `\newlabel{main-text-end}{{sec}{PAGE}...}` gives the page. This is the gate.
  3. On that page, collect margin numbers by POSITION: three-digit integers whose left edge
     sits at the modal margin x. `lineno` sets them in a rigid column, so this is geometry
     rather than a parsing guess, and row grouping is never consulted.
  4. Locate NAME's rendered heading by matching normalized text against the page's word stream
     (the ICLR style upper-cases it, so matching is case- and space-insensitive).
  5. The reading is the greatest margin number whose baseline is strictly above the heading's.

CHECKS, each of which exits rather than reporting a number it cannot defend:
  - the recovered margin numbers are strictly increasing down the page;
  - the heading is found exactly once on the page the .aux names;
  - at least one margin number lies above it (else the statement leads its page, and the tool
     falls back to the preceding page, as v1 learned to do under D-R81-2);
  - the reading is strictly less than the heading's own margin number, when it has one.

Usage:
    python tools/page_census_v2.py paper_v2.pdf [more.pdf ...]
Exit 0 when every PDF passes the page check; 1 when one fails it; 2 when a stated assumption
is broken.
"""
import re
import sys
import pathlib
import statistics

PAGE_LIMIT = 9          # ICLR 2027 main-text pages; the gate
BOUNDARY = 485          # page 9's last margin number; the slack diagnostic's reference
LABEL = "main-text-end"
MARGIN_X_TOL = 1.5      # points; lineno sets the column rigidly
BASELINE_EPS = 4.0      # points; less than one line height (~11.96)

try:
    import fitz         # PyMuPDF
except ImportError:                                          # pragma: no cover
    raise SystemExit("page_census_v2 requires PyMuPDF (import fitz)")


def _norm(s):
    return re.sub(r"\s+", "", s).lower()


def _statement_name(tex_path):
    """The first \\subsection*{...} after \\label{main-text-end}, read from source."""
    text = pathlib.Path(tex_path).read_text(encoding="utf-8", errors="replace")
    i = text.find("\\label{" + LABEL + "}")
    if i < 0:
        raise SystemExit(f"{tex_path}: no \\label{{{LABEL}}}; this tool anchors on it")
    m = re.search(r"\\subsection\*\{([^}]*)\}", text[i:])
    if not m:
        raise SystemExit(f"{tex_path}: no \\subsection* after \\label{{{LABEL}}}")
    return m.group(1)


def _label_page(aux_path):
    """The page \\label{main-text-end} resolved to. This is the gated quantity."""
    text = pathlib.Path(aux_path).read_text(encoding="utf-8", errors="replace")
    m = re.search(r"\\newlabel\{" + re.escape(LABEL) + r"\}\{\{([^}]*)\}\{([^}]*)\}", text)
    if not m:
        raise SystemExit(f"{aux_path}: no \\newlabel for {LABEL}; run LaTeX first")
    return int(m.group(2))


def _margin_numbers(page):
    """(number, baseline_y) for every three-digit integer in the lineno column."""
    words = [w for w in page.get_text("words") if re.fullmatch(r"\d{3}", w[4])]
    if not words:
        return []
    modal_x = statistics.mode([round(w[0], 1) for w in words])
    return sorted(((int(w[4]), w[1]) for w in words
                   if abs(w[0] - modal_x) <= MARGIN_X_TOL), key=lambda t: t[1])


def _heading_hits(page, name):
    """Top y of every occurrence of the heading on this page.

    The ICLR style sets `\\subsection*` in upper case small caps, and the glyph runs for
    "AI", "USE" and "STATEMENT" carry slightly different baselines, so a sliding window over
    a y-sorted word list is fragile: an unrelated word landing between them breaks the run.
    PyMuPDF's own text search handles the spacing and the case, and is tried first; the word
    window stays as a fallback for a heading search_for cannot express.
    """
    def _cluster(ys):
        """One occurrence per line: search_for returns a rect per quad, and a heading set in
        small caps yields several quads on the same baseline."""
        out = []
        for y in sorted(ys):
            if not out or y - out[-1] > BASELINE_EPS * 2:
                out.append(y)
        return out

    hits = []
    for variant in (name, name.upper()):
        try:
            hits = _cluster([r.y0 for r in page.search_for(variant)])
        except Exception:                                    # pragma: no cover
            hits = []
        if hits:
            return hits

    words = sorted(page.get_text("words"), key=lambda w: (round(w[1], 1), w[0]))
    target = _norm(name)
    for i in range(len(words)):
        acc = ""
        for j in range(i, min(i + 12, len(words))):
            acc += _norm(words[j][4])
            if acc == target:
                hits.append(words[i][1])
                break
            if not target.startswith(acc):
                break
    return hits


def census(pdf):
    pdf = pathlib.Path(pdf)
    stem = pdf.with_suffix("")
    name = _statement_name(stem.with_suffix(".tex"))
    page_no = _label_page(stem.with_suffix(".aux"))

    doc = fitz.open(pdf)
    source = f"page {page_no} (\\label{{{LABEL}}} via .aux)"
    page = doc[page_no - 1]
    hits = _heading_hits(page, name)
    if len(hits) > 1:
        raise SystemExit(f"{pdf}: heading {name!r} found {len(hits)} times on page "
                         f"{page_no}; the anchor is not unique")
    if not hits:
        # Main text ENDS on the label's page and the statement begins on the next one. This is
        # the D-R81-2 case in its other form: v1 met it when the statement led its own page
        # with its own number above nothing, and this is the same boundary seen from the label
        # side. The reading is then simply the last margin number on the label's page.
        if page_no < doc.page_count and _heading_hits(doc[page_no], name):
            nums = _margin_numbers(page)
            if not nums:
                raise SystemExit(f"{pdf}: no margin numbers on page {page_no}")
            last = max(n for n, _ in nums)
            doc.close()
            return {"pdf": str(pdf), "page": page_no, "statement": name, "reading": last,
                    "source": f"page {page_no} (statement begins on page {page_no + 1})",
                    "slack": BOUNDARY - last, "pass": page_no <= PAGE_LIMIT}
        raise SystemExit(f"{pdf}: heading {name!r} not found on page {page_no} (the page the "
                         f".aux gives for \\label{{{LABEL}}}) or on page {page_no + 1}; "
                         f"method invalid here")
    head_y = hits[0]

    nums = _margin_numbers(page)
    if [n for n, _ in nums] != sorted(n for n, _ in nums):
        raise SystemExit(f"{pdf}: margin numbers on page {page_no} are not increasing "
                         f"down the page; the lineno column assumption is broken")
    head_num = next((n for n, y in nums if abs(y - head_y) < BASELINE_EPS), None)
    above = [n for n, y in nums if y < head_y - BASELINE_EPS]

    if not above:
        # the statement leads its own page: main text ends on the page before (cf. D-R81-2)
        prev = doc[page_no - 2]
        above = [n for n, _ in _margin_numbers(prev)]
        source = f"page {page_no - 1} (statement leads page {page_no})"
        if not above:
            raise SystemExit(f"{pdf}: no margin numbers above the statement on page "
                             f"{page_no} or on page {page_no - 1}")
    last = max(above)
    if head_num is not None and last >= head_num:
        raise SystemExit(f"{pdf}: recovered reading {last} is not above the statement's own "
                         f"line {head_num}; method invalid here")
    doc.close()
    return {"pdf": str(pdf), "page": page_no, "statement": name, "reading": last,
            "source": source, "slack": BOUNDARY - last,
            "pass": page_no <= PAGE_LIMIT}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    rows = [census(p) for p in sys.argv[1:]]
    w = max(len(pathlib.Path(r["pdf"]).name) for r in rows)
    print(f"{'pdf':{w}s}  label page  gate (<= {PAGE_LIMIT})  reading  slack (485 - reading)")
    for r in rows:
        verdict = "PASS" if r["pass"] else "FAIL"
        print(f"{pathlib.Path(r['pdf']).name:{w}s}  {r['page']:10d}  {verdict:>13s}  "
              f"{r['reading']:7d}  {r['slack']:+21d}")
    print("\nThe gate is the page. The reading is a diagnostic and can move by one when "
          "material\nbelow the label changes length; a reading of 486 with the label on page "
          f"{PAGE_LIMIT} is a pass.")
    if len(rows) == 2:
        d = rows[1]["reading"] - rows[0]["reading"]
        print(f"\ndelta ({pathlib.Path(rows[1]['pdf']).name} vs "
              f"{pathlib.Path(rows[0]['pdf']).name}): {d:+d} review lines")
    raise SystemExit(0 if all(r["pass"] for r in rows) else 1)
