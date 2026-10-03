"""place_f3.py -- the page ruling of 2026-09-16 (review-2 A1, program R112): Figure 3's placement and the definition paragraph's
looseness, tried in the ruling's order before any word moves. Rebuilds and prints the fine number after each change.

Usage: python reviews/v19/tools/place_f3.py <spec>          Figure 3's placement specifier (e.g. t, !t, !tb)
       python reviews/v19/tools/place_f3.py --loose[=-1]     put \\looseness=<n> on the paragraph carrying the constrained-rendering
                                                             definition (Section 4), or --loose=0 to remove it
The figure is the one `\\begin{figure}[...]` immediately followed by `\\centering` and the item-30 comment (the per-state bars).
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
BODY = ROOT / "reviews" / "v19" / "src" / "body_v19.tex"
sys.path.insert(0, str(ROOT / "reviews" / "v19" / "tools"))
import run_gates as G  # noqa: E402

F3_ANCHOR = "\n\\centering\n%% Writing pass Phase 3 (2026-09-15), item 30"
DEF_LINE = "A ground-truth summary is built from ground truth and a store-written summary from the fields the backend itself exposes, rendered by the same code with a cap of fifteen names per list.\n"
LOOSE = "\\looseness=-1 "   # placed at the head of the definition paragraph's first line (TeX applies it to the paragraph it ends)


def build_and_read():
    subprocess.run([sys.executable, str(ROOT / "reviews" / "v19" / "tools" / "build_v19.py")], cwd=ROOT, capture_output=True)
    G.pdflatex("paper_v19", SUB)
    rb, page_no, where = G.raggedbottom_reading()
    out, _ = G.run([sys.executable, "tools/page_census_v2.py", "paper_v19.pdf"])
    return rb, page_no, where, G.last(out)[:100]


def main(arg):
    s = BODY.read_text(encoding="utf-8")
    if arg.startswith("--loose"):
        n = arg.split("=", 1)[1] if "=" in arg else "-1"
        s = s.replace(LOOSE + DEF_LINE, DEF_LINE)
        assert s.count(DEF_LINE) == 1
        if n != "0":
            s = s.replace(DEF_LINE, f"\\looseness={n} " + DEF_LINE)
        BODY.write_text(s, encoding="utf-8", newline="\n")
        print(f"definition paragraph looseness: {'removed' if n == '0' else n}")
    else:
        m = re.search(r"\\begin\{figure\}\[([^\]]*)\](?=" + re.escape(F3_ANCHOR) + ")", s)
        assert m, "Figure 3's environment not found"
        s = s[:m.start()] + f"\\begin{{figure}}[{arg}]" + s[m.end():]
        BODY.write_text(s, encoding="utf-8", newline="\n")
        print(f"Figure 3 placement: [{m.group(1)}] -> [{arg}]")
    rb, page_no, where, census = build_and_read()
    print(f"fine number {rb} (label page {page_no}, the AI-use statement {where}); page_census_v2: {census}")


if __name__ == "__main__":
    main(sys.argv[1])
