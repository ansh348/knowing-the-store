# -*- coding: utf-8 -*-
"""r116_apply.py -- R116, the provenance fix (reviews/r115/PROVENANCE_AUDIT.md; the author's Appendix R of 18 September 2026).

Asserted edits on reviews/v19/src/{body,appendix}_v19.tex and reviews/v19/tools/build_v19.py: each OLD occurs exactly once,
LF preserved, idempotent (a second run finds every NEW present and every OLD absent and changes nothing). --check reports without
writing. Item 1 of Appendix R ("Every protocol was committed before its run (hashes and order: Appendix F).") has no anchor in the
v19 sources or in v20 and is reported, not forced (reviews/r116/REPORT_R116.md). Item 2(a), the R81 hash inside the carried
paper_v11 table (lines 2084-2118), is a block-keyed repair in build_v19.py (REPAIRS_R116_BLOCK), the R115 mechanism.
"""
from __future__ import annotations

import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v19" / "src"
BUILD = ROOT / "reviews" / "v19" / "tools" / "build_v19.py"

EDITS = [
    # 2(b) table b: DS Amendment 4's file hash labelled as Graphiti Amendment 2's is
    (SRC / "appendix_v19.tex",
     "DS Amendment 4: a view header binding the entries to the persona and pinning the date & \\texttt{fb4b2ca8c8} & 2026-09-14 &",
     "DS Amendment 4: a view header binding the entries to the persona and pinning the date & \\texttt{fb4b2ca8c8} (file hash) & 2026-09-14 &"),
    # 2(c) table c caption
    (SRC / "appendix_v19.tex",
     "\\caption{The registration record, continued: twelve descriptive registrations, each frozen by sha256 before its first call and carrying no prediction and no bar, so nothing in them could hold or fail. Every one has run except the paraphrase check, which waits on our read.}",
     "\\caption{The registration record, continued: twelve descriptive registrations, each hashed by the runner before its first call (the commits of 18 September do not date them) and carrying no prediction and no bar, so nothing in them could hold or fail. Every one has run except the paraphrase check, which waits on our read.}"),
    # 2(d) the mechanism paragraph and the lock-attested set, after table c and before "When Opus 5 entered"
    (SRC / "appendix_v19.tex",
     "\\noindent\\textbf{When Opus 5 entered.}",
     "%% R116 (2026-09-18): the provenance audit (reviews/r115/PROVENANCE_AUDIT.md sections 1, 3 and 4); the lock-attested set named from its table.\n"
     "\\noindent\\textbf{How each freeze is attested.} Each runner wrote a lock record at its start holding the registration's sha256, and dated additions sit below the registered-text marker, outside the hash. "
     "For most registrations a commit holding the registered text also predates the run's first output. "
     "For CF-3, committed 33 minutes after its first call, and for DS Amendments 1 to 4, Q4, RESP Amendment 1 and Graphiti Amendment 2, first committed on 18 September 2026, the evidence that the text predates the run is the runner's lock record and the file times.\\\\\n"
     "\n"
     "\\noindent\\textbf{When Opus 5 entered.}"),
    # 3. E.9 (app:resp)
    (SRC / "appendix_v19.tex",
     "Each was preregistered with its texts written before any call (Table~\\ref{tab:registrations-b}), so every outcome below is read against a text that predates it.",
     "Each was preregistered with its texts written before any call (Table~\\ref{tab:registrations-b}), by commit except DS Amendment 4 and Graphiti Amendment 2, which hold by the runner's record, so every outcome below is read against a text that predates it."),
    # 4. the reproducibility statement
    (SRC / "body_v19.tex",
     "holds the frozen registrations with their commit hashes, the prompts,",
     "holds the frozen registrations with their hashes (commit hashes where a commit predates the run; Appendix~\\ref{app:registration}), the prompts,"),
    # 2(a) the carried table a: R81's hash (the audit, section 2; first commit of registrations/ADDENDUM_R81.md is 5c3621b75e, 2026-08-29)
    (BUILD,
     "REPAIRS_R115_BLOCK = {\n    (1004, 1020): [('\\\\begin{table}[h]', '\\\\begin{table}[H]', 1)],\n}\n",
     "REPAIRS_R115_BLOCK = {\n    (1004, 1020): [('\\\\begin{table}[h]', '\\\\begin{table}[H]', 1)],\n}\n"
     "\n"
     "# R116 (2026-09-18, the provenance fix; reviews/r115/PROVENANCE_AUDIT.md section 2): the R81 row of the carried registration table a\n"
     "# cites a commit prefix that does not exist (2bb7fd97... is the R79 clarity-report commit and holds no R81 text); the registration file's\n"
     "# first commit is 5c3621b75e (2026-08-29 17:11 +05:30), before the first NB-6 output. Keyed to the table's block; asserted to its count.\n"
     "REPAIRS_R116_BLOCK = {\n    (2084, 2118): [('\\\\texttt{2bb7fd9dc4}', '\\\\texttt{5c3621b75e}', 1)],\n}\n"),
    (BUILD,
     "    n_r115 = {(lo, hi, o): 0 for (lo, hi), rules in REPAIRS_R115_BLOCK.items() for o, _, _ in rules}\n",
     "    n_r115 = {(lo, hi, o): 0 for (lo, hi), rules in REPAIRS_R115_BLOCK.items() for o, _, _ in rules}\n"
     "    n_r116 = {(lo, hi, o): 0 for (lo, hi), rules in REPAIRS_R116_BLOCK.items() for o, _, _ in rules}\n"),
    (BUILD,
     "            for o, n_, _ in REPAIRS_R115_BLOCK.get((a, b), []):   # R115: keyed to this block's line range\n"
     "                k = ln.count(o)\n"
     "                if k:\n"
     "                    ln = ln.replace(o, n_); n_r115[(a, b, o)] += k\n",
     "            for o, n_, _ in REPAIRS_R115_BLOCK.get((a, b), []):   # R115: keyed to this block's line range\n"
     "                k = ln.count(o)\n"
     "                if k:\n"
     "                    ln = ln.replace(o, n_); n_r115[(a, b, o)] += k\n"
     "            for o, n_, _ in REPAIRS_R116_BLOCK.get((a, b), []):   # R116: the R81 hash in the carried table a\n"
     "                k = ln.count(o)\n"
     "                if k:\n"
     "                    ln = ln.replace(o, n_); n_r116[(a, b, o)] += k\n"),
    (BUILD,
     "    assert not bad115, bad115\n",
     "    assert not bad115, bad115\n"
     "    bad116 = [(key, n_r116[key], k) for (lo, hi), rules in REPAIRS_R116_BLOCK.items() for o, _, k in rules for key in [(lo, hi, o)] if n_r116[key] != k]\n"
     "    print(f\"R116 block repairs applied inside carried blocks: {sum(n_r116.values())} substitutions over {len(n_r116)} rules\" + (f\"; COUNT MISMATCH {bad116}\" if bad116 else \"\"))\n"
     "    assert not bad116, bad116\n"),
]


def main():
    check = "--check" in sys.argv
    texts = {}
    for p, old, new in EDITS:
        t = texts.get(p)
        if t is None:
            raw = p.read_bytes()
            assert b"\r\n" not in raw, f"{p}: CRLF source, refusing"
            t = raw.decode("utf-8")
        n_old, n_new = t.count(old), t.count(new)
        if n_new == 1:                      # NEW present once: applied (OLD may be a substring of NEW for the insertions)
            print(f"  already applied : {p.name}: {new[:70]!r}")
        elif n_new == 0 and n_old == 1:
            print(f"  {'would apply' if check else 'applied'}     : {p.name}: {old[:70]!r}")
            if not check:
                t = t.replace(old, new)
        else:
            raise SystemExit(f"ANCHOR NOT UNIQUE ({n_old} old, {n_new} new) in {p}: {old[:90]!r}")
        texts[p] = t
    if not check:
        for p, t in texts.items():
            io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("r116_apply:", "check only" if check else "written", f"({len(EDITS)} edits over {len(texts)} files)")


if __name__ == "__main__":
    main()
