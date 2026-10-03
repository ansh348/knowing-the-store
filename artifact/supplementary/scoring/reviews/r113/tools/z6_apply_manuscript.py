# -*- coding: utf-8 -*-
"""z6_apply_manuscript.py -- SPEC_R113 section Z6: the list-length statements reconciled with the recorded rows at 100 and 200 names
(reviews/NUMBERS_R110.md AUX-R110-A4; reviews/NUMBERS_R113.md AUX-R113-PAD-LEX-PAIRED). Asserted replacements in reviews/v19/src
(LF files). Run from the repository root: python reviews/r113/tools/z6_apply_manuscript.py
(1) Appendix C.2: the store's-own-pool sentence gains the registered-order rows at 100 and 200 (other personas' names) and states what
    stays untested (a longer list of the store's own names).
(2) tab:pad's caption names the 100- and 200-name rows and the pool they draw on (79 of 242 summaries at 100, every summary at 200).
(3) tab:pad's lexical rows at 100 and 200 print the paired difference and both intervals (from the R110 artifact, ledgered at R113) in
    the columns the table defines, in place of a single-arm interval printed in the item-interval column.
(4) Limitations: "untested beyond the store's own name pool" reads "beyond the store's own name pool ... tested only with other personas'
    names".
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v19" / "src"
B, X = SRC / "body_v19.tex", SRC / "appendix_v19.tex"
E = []


def rep(f, old, new):
    E.append((f, old, new))


# (1) Appendix C.2
rep(X, "With every untargeted name the store holds on the list, a mean of $99$ names per summary and at most $129$, the embedding lookup reads $0.6531$; beyond the store's own name pool it is untested.",
    "With every untargeted name the store holds on the list, a mean of $99$ names per summary and at most $129$, the embedding lookup reads $0.6531$; continued past that pool with other personas' names to $100$ and $200$ it reads $0.6558$ and $0.5960$ (Table~\\ref{tab:pad}), so a longer list of the store's own names is untested.")
# (2) the caption
rep(X, "padded with correct attribute names that no scored question of the persona targets, to $15$, $30$ and $60$ names; obligation AUROC of each reader against its recorded $1.75$-name row, with the paired difference and both intervals.",
    "padded with correct attribute names that no scored question of the persona targets, to $15$, $30$ and $60$ names, and for the two lookups to $100$ and $200$ names under the registered draw order, which continues into other personas' names once the store's own pool is exhausted ($79$ of the $242$ summaries at $100$, every summary at $200$); obligation AUROC of each reader against its recorded $1.75$-name row, with the paired difference and both intervals.")
# (3) the lexical rows
rep(X, "%% R110: the lookup at 100 and 200 names under the registered draw order (reviews/NUMBERS_R110.md AUX-R110-A4; reviews/v18/results/a4_table16_rows.tex).\n",
    "%% R110: the lookup at 100 and 200 names under the registered draw order (reviews/NUMBERS_R110.md AUX-R110-A4; reviews/v18/results/a4_table16_rows.tex).\n"
    "%% R113 (2026-09-16): the lexical rows at 100 and 200 print the paired difference and both intervals from the same artifact (reviews/NUMBERS_R113.md AUX-R113-PAD-LEX-PAIRED); the caption names the pool the rows draw on.\n")
rep(X, "Lexical lookup & $100$ names & $0.5601$ & -- & $[0.5001,0.6162]$ & -- \\\\",
    "Lexical lookup & $100$ names & $0.5601$ & $-0.0137$ & $[-0.0672,+0.0369]$ & $[-0.0926,+0.0716]$ \\\\")
rep(X, "Lexical lookup & $200$ names & $0.5383$ & -- & $[0.4737,0.6006]$ & -- \\\\",
    "Lexical lookup & $200$ names & $0.5383$ & $-0.0355$ & $[-0.0903,+0.0189]$ & $[-0.1125,+0.0455]$ \\\\")
# (4) Limitations
rep(B, "The lookup is untested beyond the store's own name pool, a mean of $99$ names, and a paraphrase check of one rewording per question, fixed in advance, is not yet scored.",  # split into two sentences at the readability listing (36 words)
    "Beyond the store's own name pool, a mean of $99$ names, the lookup is tested only with other personas' names. A paraphrase check of one rewording per question, fixed in advance, is not yet scored.")


def main():
    files = {p: p.read_text(encoding="utf-8") for p in (B, X)}
    for f, old, new in E:
        n = files[f].count(old)
        if n != 1:
            print(f"ABORT {f.name}: {n} of {old[:120]!r}"); sys.exit(1)
        files[f] = files[f].replace(old, new)
    for p, t in files.items():
        p.write_text(t, encoding="utf-8", newline="\n")
    print(f"applied {len(E)}")


if __name__ == "__main__":
    main()
