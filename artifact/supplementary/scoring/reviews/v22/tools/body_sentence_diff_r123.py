# -*- coding: utf-8 -*-
"""body_sentence_diff_r123.py -- program R123, Phase E: every changed body sentence, old beside new, between the fallback build
(fallback/v21-pre-pass = 61b0bd8) and HEAD, read from the sources (abstract_v21.tex and body_v21.tex up to \\label{main-text-end}; the
sources keep one sentence per line, table rows and comments excluded). Pairs are made by difflib's opcodes: a 'replace' block prints
old lines beside new lines, a 'delete' block prints old lines with an empty right side, an 'insert' block the reverse.
Writes reviews/v21/BODY_SENTENCES_R123.md. Usage: python reviews/v21/tools/body_sentence_diff_r123.py [old-rev]
"""
from __future__ import annotations

import difflib
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews" / "v21" / "BODY_SENTENCES_R123.md"
OLD = sys.argv[1] if len(sys.argv) > 1 else "fallback/v21-pre-pass"


def show(rev, rel):
    return subprocess.run(["git", "show", f"{rev}:{rel}"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout


def sentences(abstract, body):
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", abstract, flags=re.S)
    abs_lines = [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\\$(`])", m.group(1).strip()) if s.strip()]
    main = body[:body.index("\\label{main-text-end}")]
    out = ["[abstract] " + s for s in abs_lines]
    in_tab = 0; in_fig = 0
    sec = "S1"
    for ln in main.split("\n"):
        s = ln.strip()
        if not s or s.startswith("%"):
            continue
        if s.startswith("\\section{"):
            sec = re.search(r"\\section\{([^}]*)\}", s).group(1)
        if "\\begin{tabular}" in s or "\\begin{tikzpicture}" in s or "\\begin{figure}" in s or "\\begin{table}" in s:
            in_tab += 1
        if in_tab == 0 and not s.startswith("\\") and not s.startswith("%"):
            out.append(f"[{sec}] " + re.sub(r"\s*%.*$", "", s))
        elif in_tab and s.startswith("\\caption{"):
            out.append(f"[{sec}, caption] " + s)
        if "\\end{tabular}" in s or "\\end{tikzpicture}" in s or "\\end{figure}" in s or "\\end{table}" in s:
            in_tab = max(0, in_tab - 1)
    return out


def main():
    old = sentences(show(OLD, "reviews/v21/src/abstract_v21.tex"), show(OLD, "reviews/v21/src/body_v21.tex"))
    new = sentences((ROOT / "reviews/v21/src/abstract_v21.tex").read_text(encoding="utf-8"), (ROOT / "reviews/v21/src/body_v21.tex").read_text(encoding="utf-8"))
    sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
    L = [f"# BODY_SENTENCES_R123.md: every changed body sentence, old ({OLD}) beside new (HEAD)", "",
         "Read from reviews/v21/src/abstract_v21.tex and body_v21.tex up to the main-text-end label (one sentence per source line; table rows, figures and comments excluded; captions included). "
         "Written by reviews/v21/tools/body_sentence_diff_r123.py. An empty right cell is a deleted sentence, an empty left cell an added one.", "",
         "| old | new |", "|---|---|"]
    n_rep = n_del = n_ins = 0
    def cell(s):
        return s.replace("|", "\\|")
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        a = old[i1:i2]; b = new[j1:j2]
        k = max(len(a), len(b))
        for x in range(k):
            l = cell(a[x]) if x < len(a) else ""
            r = cell(b[x]) if x < len(b) else ""
            L.append(f"| {l} | {r} |")
        n_rep += min(len(a), len(b)); n_del += max(0, len(a) - len(b)); n_ins += max(0, len(b) - len(a))
    L.insert(4, f"Counts: {n_rep} sentences replaced, {n_del} removed, {n_ins} added; {len(old)} sentences before, {len(new)} after.")
    L.insert(5, "")
    io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(f"-> {OUT}: {n_rep} replaced, {n_del} removed, {n_ins} added ({len(old)} -> {len(new)} sentences)")


if __name__ == "__main__":
    main()
