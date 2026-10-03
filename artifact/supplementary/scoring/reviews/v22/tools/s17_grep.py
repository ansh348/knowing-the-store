# -*- coding: utf-8 -*-
"""s17_grep.py -- the section 17 grep block of paper_v18_writing_prompt.md over the built paper_v18.tex, under the author's rule of
2026-09-15: each token must be zero in the main text and zero in the appendix outside registered-text blocks; the residue inside
registered-text blocks (frozen wording that ships verbatim, R78-2c) is reported on its own line so nobody mistakes it for a miss.
A registered-text block is detected as wp_phase2.py detects it (frozen_diff's registration fragments and slogan_scan's
EXEMPT_FROZEN_REGISTERED strings, normalized; the "ships verbatim" comment blocks). Comments are stripped; the bibliography is cut;
"the authorship-matched" is not "the author". Also prints the PDF text layer's counts for the main text and the whole document.
Usage: python reviews/v18/tools/s17_grep.py [paper_v18.tex]   (exit 1 if any token is nonzero in the main text or outside the blocks)"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
sys.path.insert(0, str(ROOT / "reviews" / "v22" / "tools"))
import wp_phase2 as P  # noqa: E402

TOKENS = ["smallest model", "larger model", "believed", "truthful", "BELIEVED", "TRUTHFUL", "the join", "the marks", "the matcher",
          "tally", "tallies", "individuat", "sixtyfold", "the ruler", "the author", "reviewer", "prior store", "inherited store",
          "as released", "NUMBERS_R", "reviews/", "both intervals excluding zero", "user profile"]
CAPS = {"both intervals excluding zero": 3}          # section 17: <= 3
PATTERNS = {"the author": r"the author(?!ship)", "NUMBERS_R": r"NUMBERS\\?_R"}


def main():
    tex = SUB / (sys.argv[1] if len(sys.argv) > 1 else "paper_v22.tex")   # v19 (R112)
    lines = tex.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    a0 = next(i for i, l in enumerate(lines) if l.startswith("\\begin{abstract}"))
    ap = next(i for i, l in enumerate(lines) if l.strip() == "\\appendix")
    b0 = next(i for i, l in enumerate(lines) if l.startswith("\\begin{thebibliography}"))
    b1 = next(i for i, l in enumerate(lines) if l.startswith("\\end{thebibliography}"))
    zones = {"main": [], "appendix": [], "registered": [], "map": []}
    in_map = False
    for i, l in enumerate(lines):
        if "this map carries them to the paper's terms" in l:
            in_map = True                     # the E.1 map of the artifact's names (the author's ruling of 2026-09-15): the names belong there
        if i < a0 or b0 <= i <= b1 or l.lstrip().startswith("%"):
            continue
        text = re.sub(r"(?<!\\)%.*$", "", l)
        if i < ap:
            zones["main"].append(text)
        elif in_map:
            zones["map"].append(text)
            if l.startswith("\\end{center}"):
                in_map = False
        elif P.is_frozen(lines, i):
            zones["registered"].append(text)
        else:
            zones["appendix"].append(text)
    joined = {k: "\n".join(v) for k, v in zones.items()}
    pdf_main = pdf_all = None
    try:
        import fitz
        doc = fitz.open(str(tex.with_suffix(".pdf")))
        aux = tex.with_suffix(".aux").read_text(encoding="utf-8", errors="replace")
        end_page = int(re.search(r"\\newlabel\{main-text-end\}\{\{[^}]*\}\{(\d+)\}", aux).group(1))
        pdf_main = "\n".join(doc[i].get_text() for i in range(end_page))
        pdf_all = "\n".join(pg.get_text() for pg in doc)
    except Exception as e:  # noqa: BLE001
        print(f"(PDF text layer not read: {e})")
    print(f"{'token':30s} {'main':>5s} {'appendix':>9s} {'registered':>11s} {'E.1 map':>8s} {'pdf main':>9s} {'pdf whole':>10s}")
    fails = []
    for k in TOKENS:
        pat = PATTERNS.get(k, re.escape(k))
        c = {z: len(re.findall(pat, joined[z])) for z in zones}
        pm = len(re.findall(pat, pdf_main)) if pdf_main is not None else -1
        pa = len(re.findall(pat, pdf_all)) if pdf_all is not None else -1
        print(f"{k:30s} {c['main']:5d} {c['appendix']:9d} {c['registered']:11d} {c['map']:8d} {pm:9d} {pa:10d}")
        cap = CAPS.get(k, 0)
        if c["main"] > cap or c["appendix"] > cap:
            fails.append(k)
    print("registered = inside registered-text blocks (frozen wording that ships verbatim; not a miss); E.1 map = the rows of the artifact-name map. the author: 'the authorship-matched' excluded.")
    print("s17_grep: " + ("PASS" if not fails else "FAIL on " + ", ".join(fails)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
