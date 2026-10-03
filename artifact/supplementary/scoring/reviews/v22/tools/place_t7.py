"""place_t7.py -- the page ruling of 2026-09-15 (review-2 A1, program R112): Table 7's placement, tried before any word moves.

Sets the placement specifier of Table 7 (tab:ds-body, the downstream policies table at the head of Section 9) in
reviews/v19/src/body_v19.tex, rebuilds, and prints the fine number (run_gates.raggedbottom_reading) and the page census row.
Usage: python reviews/v19/tools/place_t7.py <spec>      e.g. t, b, tb, h, H, !t
The source line is the one `\\begin{table}[...]` immediately followed by the item-55 comment of Table 7.
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

ANCHOR = "\n%% Writing pass Phase 1 (2026-09-15), item 55:"


def main(spec):
    s = BODY.read_text(encoding="utf-8")
    m = re.search(r"\\begin\{table\}\[([^\]]*)\](?=" + re.escape(ANCHOR) + ")", s)
    assert m, "Table 7's environment not found"
    old = m.group(1)
    s = s[:m.start()] + f"\\begin{{table}}[{spec}]" + s[m.end():]
    BODY.write_text(s, encoding="utf-8", newline="\n")
    print(f"Table 7 placement: [{old}] -> [{spec}]")
    subprocess.run([sys.executable, str(ROOT / "reviews" / "v19" / "tools" / "build_v19.py")], cwd=ROOT, capture_output=True)
    G.pdflatex("paper_v19", SUB)
    rb, page_no, where = G.raggedbottom_reading()
    out, _ = G.run([sys.executable, "tools/page_census_v2.py", "paper_v19.pdf"])
    print(f"fine number {rb} (label page {page_no}, the AI-use statement {where}); page_census_v2: {G.last(out)}")


if __name__ == "__main__":
    main(sys.argv[1])
