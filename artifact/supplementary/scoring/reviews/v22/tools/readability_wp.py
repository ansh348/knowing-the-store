# -*- coding: utf-8 -*-
"""readability_wp.py -- the section 15 readability listing of the writing pass, on the built manuscript: every body sentence counted with
its word count (section 15 rule 1: none over 35 words; the count over 35 is printed with each offender), the first sentence of every
body paragraph (rule 3, the cold-read listing the phase reports carry as first_sentences_phase*.txt), and the word count of each
contributions bullet (item 5). Paragraphs and sentences are split as q_scan.py splits them (the same helpers); words are counted after
\\ref / \\cite / \\label are removed and macros reduced to their names, a number being one word.
Usage: python reviews/v18/tools/readability_wp.py [paper_v18.tex] [--first=out.txt]     (exit 0 always; a report, not a gate)"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import q_scan as Q  # noqa: E402


def words(s):
    s = Q.strip_refs(s)
    s = re.sub(r"\$[^$]*\$", " N ", s)            # a math run (a number, a symbol) is one word
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    s = re.sub(r"[{}~]", " ", s)
    return [w for w in re.split(r"\s+", s) if re.search(r"[A-Za-z0-9]", w)]


def sentences(text):
    # R126 (2026-09-19): a sentence also ends at '.}' (a bold run-in claim sentence), as q_scan.first_sentence splits since R126
    return [s for s in re.split(r"(?:(?<=[.!?])|(?<=[.!?]\}))\s+(?=[A-Z\\$(`])", text) if s.strip()]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tex = SUB / (args[0] if args else "paper_v22.tex")   # v19 (R112)
    out_first = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--first=")), None)
    lines = tex.read_text(encoding="utf-8").split("\n")
    intro = next(i for i, l in enumerate(lines) if l.startswith("\\section{Introduction}"))
    end = next(i for i, l in enumerate(lines) if "main-text-end" in l)
    secs = [(i, re.match(r"\\section\{([^}]*)\}", lines[i]).group(1)) for i in range(intro, end) if re.match(r"\\section\{", lines[i])]
    body = Q.paragraphs(lines, intro, end)
    n_sent, over = 0, []
    first = []
    for ln, text in body:
        sec = next((name for i, name in reversed(secs) if i < ln), "?")
        for s in sentences(text):
            n = len(words(s))
            n_sent += 1
            if n > 35:
                over.append((ln, sec, n, s))
        first.append((ln, sec, Q.first_sentence(text)))
    print(f"readability: {n_sent} body sentences, {len(over)} over 35 words")
    for ln, sec, n, s in over:
        print(f"  L{ln} [{sec}] {n} words :: {s[:160]}")
    # the contributions bullets
    i0 = next((i for i in range(intro, end) if "\\begin{itemize}" in lines[i]), None)
    if i0 is not None:
        i1 = next(i for i in range(i0, end) if "\\end{itemize}" in lines[i])
        counts = [len(words(l[len("\\item"):])) for l in lines[i0 + 1:i1] if l.startswith("\\item")]
        print("contributions: " + ", ".join(str(c) for c in counts) + " words")
    if out_first:
        with open(out_first, "w", encoding="utf-8", newline="\n") as f:
            cur = None
            for ln, sec, fs in first:
                if sec != cur:
                    cur = sec
                    k = sum(1 for _, s, _ in first if s == sec)
                    f.write(f"\n## {sec} ({k} paragraphs)\n")
                s = re.sub(r"\\emph\{([^}]*)\}", r"\1", Q.strip_refs(fs)).replace("~", " ")
                s = re.sub(r"\\[a-zA-Z]+\*?(\[[^]]*\])?(\{[^}]*\})?", "", s)
                s = re.sub(r"\s+([.,;:)])", r"\1", re.sub(r"\s+", " ", s)).replace("( ", "(").strip()
                f.write(f"- L{ln}: {s}\n")
        print(f"first sentences -> {out_first}")


if __name__ == "__main__":
    main()
