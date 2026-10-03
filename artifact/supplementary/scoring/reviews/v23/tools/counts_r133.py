# -*- coding: utf-8 -*-
"""counts_r133.py -- the report's counts (the brief, section 11) on a built manuscript: 'reliable' / 'reliably' in the main text (target 15 or fewer, section
6.4), appendix pointers in Sections 4 to 8, numerals in running prose per subsection (tables, figures, captions and boxes excluded), the daggers in the main
text, and sentences over 35 words. Read-only.
Usage: python reviews/v23/tools/counts_r133.py [paper_v23.tex|paper_v22.tex]
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))
import q_scan as Q  # noqa: E402


def main():
    tex = SUB / (sys.argv[1] if len(sys.argv) > 1 else "paper_v23.tex")
    lines = tex.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    a0 = next(i for i, l in enumerate(lines) if l.startswith("\\begin{abstract}"))
    end = next(i for i, l in enumerate(lines) if "main-text-end" in l)
    main_lines = [re.sub(r"(?<!\\)%.*$", "", l) for l in lines[a0:end + 1]]
    main = "\n".join(main_lines)
    print(f"{tex.name}: reliable/reliably in the main text: {len(re.findall(r'[Rr]eliabl[ey]', main))}")
    heads = [(i, re.match(r"\\(sub)?section\{([^}]*)\}", l).group(2)) for i, l in enumerate(main_lines) if re.match(r"\\(sub)?section\{", l)]
    heads = [(0, "Abstract and front")] + heads + [(len(main_lines), "END")]
    total_ptr = 0
    for (i, name), (j, _) in zip(heads, heads[1:]):
        block = main_lines[i:j]
        text = "\n".join(block)
        paras = Q.paragraphs(block, 0, len(block))
        prose = " ".join(p for _, p in paras)
        ptr = len(re.findall(r"Appendix~?\\ref\{", prose)) + len(re.findall(r"Appendices~?\\ref\{", prose))
        nums = re.findall(r"\$[^$]*\d[^$]*\$", prose)
        rel = len(re.findall(r"[Rr]eliabl[ey]", text))
        dag = text.count("\\dagger") + text.count("†")
        if name in ("Setup", "Names and counts", "The lookup against the models", "When intent licenses old content", "What backends write", "At retrieval", "Replication and the coverage judgment"):
            total_ptr += ptr
        print(f"  {name[:42]:42s} reliable {rel:2d}  appendix pointers in prose {ptr:2d}  numerals in prose {len(nums):3d}  daggers {dag}")
    print(f"appendix pointers in the running prose of Sections 4 to 8: {total_ptr}")


if __name__ == "__main__":
    main()
