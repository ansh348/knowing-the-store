# -*- coding: utf-8 -*-
"""body_map_r126.py -- program R126, Phase 5.2 (2026-09-20): the claims-ledger remap. The rows are the v21 body's sentences (the abstract and the main
text of reviews/v21/src/abstract_v21.tex and body_v21.tex up to \\label{main-text-end}, captions included, as BODY_SENTENCES_R124.md reads them; the
inbox delivered no sentence map, so the map is built here). Each row is matched to the v22 body sentence that carries its content: the highest overlap
coefficient of content tokens (prose_scan's rule-D measure: intersection over the smaller set, stop words and numerals excluded) with a second key, the
set of numerals the sentence prints. A row maps when the best new sentence shares at least half its content tokens, or every numeral it prints and a
third of its tokens; otherwise the row has no home in the new body (the claim left the body, or lives in the appendix). A new sentence with no row is
one that is nobody's best match and shares fewer than half its tokens with every row.
Writes reviews/v22/BODY_MAP_R126.md (three tables: the map; rows with no home; new sentences with no row). Usage: python reviews/v22/tools/body_map_r126.py
"""
from __future__ import annotations

import io
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews" / "v22" / "BODY_MAP_R126.md"
STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "is", "are", "as", "its", "it", "that", "this", "we", "by", "at", "so", "not",
        "no", "from", "under", "every", "each", "num", "cite", "ref", "when", "which", "than", "more", "only", "also", "both", "one", "their", "them", "they", "be"}


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def sentences(abstract, body):
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", abstract, flags=re.S)
    abs_text = "\n".join(l for l in m.group(1).split("\n") if not l.lstrip().startswith("%"))
    out = [("abstract", s.strip()) for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\\$(`])", abs_text.strip()) if s.strip()]
    main = body[body.index("\\section{Introduction}"):body.index("\\label{main-text-end}")]
    in_env = 0
    sec = "1"
    for ln in main.split("\n"):
        s = ln.strip()
        if not s or s.startswith("%"):
            continue
        mm = re.match(r"\\(sub)?section\{([^}]*)\}", s)
        if mm:
            sec = mm.group(2); continue
        if re.search(r"\\begin\{(tabular|tikzpicture|figure|table|center|itemize)\}", s):
            in_env += 1
        if in_env and s.startswith("\\caption{"):
            out.append((sec + ", caption", re.sub(r"\s*%.*$", "", s)))
        elif in_env and s.startswith("\\item"):
            out.append((sec + ", contribution", s[5:].strip()))
        elif in_env == 0 and not s.startswith("\\") or (in_env == 0 and s.startswith("\\claim{")) or (in_env == 0 and s.startswith("\\emph{")):
            for x in re.split(r"(?:(?<=[.!?])|(?<=[.!?]\}))\s+(?=[A-Z\\$(`])", re.sub(r"\s*%.*$", "", s)):
                if x.strip():
                    out.append((sec, x.strip()))
        if re.search(r"\\end\{(tabular|tikzpicture|figure|table|center|itemize)\}", s):
            in_env = max(0, in_env - 1)
    return out


def words(s):
    s = re.sub(r"\$[^$]*\$", " NUM ", s)
    s = re.sub(r"\\cite[pt]?\{[^}]*\}", " ", s)
    s = re.sub(r"\\(ref|label)\{[^}]*\}", " ", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    s = re.sub(r"[{}~()\[\],;:.]", " ", s)
    return {w.lower() for w in re.split(r"\s+", s) if re.search(r"[A-Za-z]", w)} - STOP


def nums(s):
    return set(re.findall(r"\$([^$]*\d[^$]*)\$", s))


def main():
    old = sentences(rd(ROOT / "reviews/v21/src/abstract_v21.tex"), rd(ROOT / "reviews/v21/src/body_v21.tex"))
    new = sentences(rd(ROOT / "reviews/v22/src/abstract_v22.tex"), rd(ROOT / "reviews/v22/src/body_v22.tex"))
    ow = [words(s) for _, s in old]; nw = [words(s) for _, s in new]
    on = [nums(s) for _, s in old]; nn = [nums(s) for _, s in new]
    best_for_new = {}
    rows, no_home = [], []
    for i, (osec, os_) in enumerate(old):
        scores = []
        for j in range(len(new)):
            if not ow[i] or not nw[j]:
                scores.append((0.0, j)); continue
            ov = len(ow[i] & nw[j]) / min(len(ow[i]), len(nw[j]))
            scores.append((ov, j))
        ov, j = max(scores)
        num_ok = bool(on[i]) and on[i] <= nn[j]
        if ov >= 0.5 or (num_ok and ov >= 0.34):
            rows.append((i, j, ov, num_ok)); best_for_new.setdefault(j, []).append(i)
        else:
            no_home.append((i, j, ov))
    no_row = []
    for j in range(len(new)):
        if j in best_for_new:
            continue
        top = max((len(ow[i] & nw[j]) / min(len(ow[i]), len(nw[j])) if ow[i] and nw[j] else 0.0) for i in range(len(old)))
        if top < 0.5:
            no_row.append((j, top))
    def cell(s):
        return s.replace("|", "\\|")
    L = ["# BODY_MAP_R126.md: the claims-ledger remap of program R126 (the v21 body's sentences to the v22 body's; 2026-09-20)", "",
         f"Rows: the {len(old)} sentences of the v21 body (abstract, Sections 1 to 11, captions, contributions). New: the {len(new)} sentences of the v22 body. Written by reviews/v22/tools/body_map_r126.py "
         "(the inbox delivered no sentence map); the match is the overlap coefficient of content tokens with the printed numerals as a second key. "
         f"Mapped: {len(rows)}; rows with no home in the new body: {len(no_home)}; new sentences with no row: {len(no_row)}.", "",
         "## 1. The map (row, its best new sentence, the overlap; 'numbers' when the row's numerals all print in the new sentence)", "",
         "| # | v21 sentence | v22 sentence | overlap |", "|---|---|---|---|"]
    for i, j, ov, num_ok in rows:
        L.append(f"| {i + 1} | [{old[i][0]}] {cell(old[i][1])} | [{new[j][0]}] {cell(new[j][1])} | {ov:.0%}{' numbers' if num_ok else ''} |")
    L += ["", "## 2. Rows with no home in the new body (a claim that left the body; the nearest new sentence and its overlap shown)", "",
          "| # | v21 sentence | nearest v22 sentence | overlap |", "|---|---|---|---|"]
    for i, j, ov in no_home:
        L.append(f"| {i + 1} | [{old[i][0]}] {cell(old[i][1])} | [{new[j][0]}] {cell(new[j][1])} | {ov:.0%} |")
    L += ["", "## 3. New sentences with no row (nobody's best match; fewer than half their tokens shared with any row)", "",
          "| v22 sentence | best overlap with any row |", "|---|---|"]
    for j, top in no_row:
        L.append(f"| [{new[j][0]}] {cell(new[j][1])} | {top:.0%} |")
    io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(f"-> {OUT}: rows {len(old)}, new {len(new)}, mapped {len(rows)}, no home {len(no_home)}, no row {len(no_row)}")


if __name__ == "__main__":
    main()
