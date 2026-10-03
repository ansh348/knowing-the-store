# -*- coding: utf-8 -*-
"""wp_inventory.py -- Phase 2 of the writing pass: every occurrence of the section 17 tokens and the item 61 terms in the assembled
paper_v18.tex, classified by origin (S the abstract, B the body source, A the appendix source, V a carried paper_v11 block), by whether
the line is a comment, and by whether it lies inside a frozen registered text (slogan_scan's EXEMPT_FROZEN_REGISTERED strings and the
appendix's 'ships verbatim' lines), so the replacements of items 34, 35, 61, 80 and 83 touch only what may be touched.
Usage: python reviews/v18/tools/wp_inventory.py [--tokens=a,b,c] [--show=token]"""
from __future__ import annotations

import ast
import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
SRC = ROOT / "reviews" / "v18" / "src"

TOKENS = ["smallest model", "larger model", "believed", "truthful", "BELIEVED", "TRUTHFUL", "the join", "the marks", "the matcher",
          "tally", "tallies", "individuat", "sixtyfold", "the ruler", "the author", "reviewer", "prior store", "inherited store",
          "as released", "NUMBERS_R", "reviews/", "both intervals excluding zero", "user profile", "profile interval", "profile-grouped",
          "the lookup", "lifecycle store", "over a third", "margin one call", "increment moved", "PN item", "present-negative item",
          "carries the obligation", "carries the judgment", "the level two", "the states the summary only", "trueidx"]


def read(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")


def assemble():
    """(line, origin) pairs of the assembled paper, mirroring build_v18.py."""
    v11 = read(SUB / "paper_v11.tex")
    body = read(SRC / "body_v18.tex")
    abstract = read(SRC / "abstract_v18.tex")
    a0 = next(i for i, l in enumerate(abstract) if l.startswith("\\begin{abstract}"))
    a1 = next(i for i, l in enumerate(abstract) if l.startswith("\\end{abstract}"))
    abstract = abstract[a0:a1 + 1]          # the builder splices the environment only, not the file's comment lines
    appx = read(SRC / "appendix_v18.tex")
    out = []
    for src_lines, tag in ((body, "B"), (appx, "A")):
        for ln in src_lines:
            m = re.fullmatch(r"%%V11:(\d+)-(\d+)%%", ln)
            if ln == "%%ABSTRACT%%":
                out += [(l, "S") for l in abstract]
            elif m:
                a, b = int(m.group(1)), int(m.group(2))
                out += [(l, "V") for l in v11[a - 1:b]]     # the body carries the bibliography this way
            else:
                out.append((ln, tag))
    return out


def frozen_strings():
    src = (SUB / "tools" / "slogan_scan.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    out = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "EXEMPT_FROZEN_REGISTERED" for t in node.targets):
            out = [ast.literal_eval(e) for e in node.value.elts]
    return out


def main():
    toks = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--tokens=")), TOKENS)
    show = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--show=")), None)
    lines = assemble()
    frozen = frozen_strings()
    fro_heads = [f[:60] for f in frozen]
    rows = []
    for i, (ln, org) in enumerate(lines):
        stripped = ln.lstrip()
        is_comment = stripped.startswith("%")
        text = re.sub(r"(?<!\\)%.*$", "", ln)
        in_frozen = any(h in ln for h in fro_heads) or (i > 0 and re.search(r"ships verbatim|frozen", lines[i - 1][0]) is not None and lines[i - 1][0].lstrip().startswith("%"))
        for t in toks:
            pat = re.escape(t) if t not in ("trueidx", "believed") else t
            hay = ln if is_comment else text
            for m in re.finditer(pat, hay):
                rows.append((t, i + 1, org, "comment" if is_comment else ("FROZEN" if in_frozen else "text"), ln.strip()[:150]))
    c = collections.Counter((r[0], r[2], r[3]) for r in rows)
    print(f"{'token':32s} {'S/B/A/V text':>14s} {'frozen':>7s} {'comment':>8s}")
    for t in toks:
        text_n = {o: c[(t, o, 'text')] for o in 'SBAV'}
        fro = sum(c[(t, o, 'FROZEN')] for o in 'SBAV')
        com = sum(c[(t, o, 'comment')] for o in 'SBAV')
        print(f"{t:32s} {text_n['S']:3d}/{text_n['B']:3d}/{text_n['A']:3d}/{text_n['V']:3d}    {fro:7d} {com:8d}")
    if show:
        print()
        for r in rows:
            if r[0] == show and r[3] != "comment":
                print(f"  L{r[1]:5d} {r[2]} {r[3]:7s} {r[4]}")


if __name__ == "__main__":
    main()
