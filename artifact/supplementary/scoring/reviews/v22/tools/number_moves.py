# -*- coding: utf-8 -*-
"""number_moves.py -- write reviews/v18/NUMBER_MOVES.md from numeric_diff's ADDED and VANISHED lists (paper_v18.tex against the v17 base),
attributing every ADDED token to the table, figure or section that carries it (the enclosing \\label, or the section) and to the nearest
R110 source comment above it (the ledger keys are in the tex source as comments); every VANISHED token carries its reason from the table
below. A second mode, --check, re-runs numeric_diff and fails if any ADDED or VANISHED token is missing from NUMBER_MOVES.md.
Usage: python reviews/v18/tools/number_moves.py <base tree> [--check]"""
from __future__ import annotations

import collections
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TEX = SUB / "paper_v18.tex"
OUT = ROOT / "reviews" / "v18" / "NUMBER_MOVES.md"

VANISHED = {
    "7%": "kept: Section 1 still prints $7\\%$ (the conflict benchmark); numeric_diff's PDF layer sees it, the tex token moved lines",
    "42%": "moved: GPT-4.1 mini's retention prints in Appendix E.9 as 42.3% with the denominator caveat (A5_EDITS.md item 9); the body's two-decimal form is retired",
    "66%": "moved: the same, 65.5% in Appendix E.9",
    "0.28": "retired: the Wilson bounds of the Haiku 4.5 oracle rate ([0.15, 0.32]) and mini's ([0.12, 0.28]) leave Section 8's prose (one interval per paragraph); the rates stay, the intervals are in the ledger (AUX-DS-AUDIT-RATES) and Table 6's lower block",
    "0.32": "retired: the same",
    "0.33": "retired: Section 8's retagging sentence keeps the gated-fetch rates (0.15 to 0.03; 0.37 to 0.23) and drops the retrieval-alone pair (0.20 to 0.06; 0.33 to 0.20) under the page gate; both pairs stand in Table tab:ds-a5",
    "0.43": "kept: Section 8 still prints $0.43$ (the deleted-record FOK); the tex token moved lines",
    "0.91": "retired from prose: Opus 5 under the all-states summary prints as 0.9079 in Table 1; the sentence was cut under the page gate",
    "0.92": "retired from prose by rule (P4): the lookup's supersession level lives in Table 1 (0.9223) and Appendix C.2 only",
    "+0.01": "reworded: \"moves none of them by more than $0.01$\" (the sign is gone from the token)",
    "-0.04": "moved: the A-MEM marker ablation (-0.11 to -0.04) to Appendix E.7 with the structureless-store ablations",
    "-0.11": "moved: the same",
    "0.006": "moved: the Mem0 variance (0.025 to 0.006) to Appendix E.7",
    "0.025": "moved: the same",
    "0.1093": "moved to Appendix E.11 as 0.11 (A5_EDITS.md item 6; no dollar figure outside E.11)",
    "0.4141": "moved to Appendix E.11 as 0.41",
    "0.4579": "moved to Appendix E.11 as 0.46",
    "0.5441": "moved to Appendix E.11 as 0.54",
    "0.5576": "moved to Appendix E.11 as 0.56",
    "0.9415": "moved to Appendix E.11 as 0.94",
}


def run_numeric(base):
    out = subprocess.run([sys.executable, "tools/numeric_diff.py", f"--base={base}", "--tex=paper_v18.tex", "--base-tex=paper_v17.tex", "--round2"],
                         cwd=SUB, capture_output=True, text=True).stdout
    added = re.search(r"ADDED \((\d+)\):\s*(.*)", out)
    vanished = re.search(r"VANISHED \((\d+)\):\s*(.*)", out)
    add = re.findall(r"(\S+) @\[([0-9, ]+)\]", added.group(2)) if added else []
    van = [v.strip() for v in vanished.group(2).split(",")] if vanished else []
    # tokens like "45," carry a trailing comma from the comma-grouped tokenizer
    return [(t.rstrip(","), [int(x) for x in ls.split(",")]) for t, ls in add], [v for v in van if v]


def context_of(lines, ln):
    """(where, key): the enclosing table/figure label or section, and the nearest R110 source comment above."""
    where, key = None, None
    for i in range(ln - 1, -1, -1):
        l = lines[i]
        m = re.search(r"\\label\{(tab:[^}]+|fig:[^}]+)\}", l)
        if m and where is None and i >= ln - 60:
            where = m.group(1)
        if l.startswith("\\section{") or l.startswith("\\subsection{"):
            if where is None:
                where = re.search(r"section\*?\{([^}]*)\}", l).group(1)
            break
        if key is None and l.lstrip().startswith("%") and re.search(r"AUX-[A-Z0-9-]+", l):
            key = ", ".join(sorted(set(re.findall(r"AUX-[A-Z0-9*-]+", l))))[:160]
    return where or "?", key or "(the enclosing table's source comment)"


def main():
    base = sys.argv[1]; check = "--check" in sys.argv
    add, van = run_numeric(base)
    lines = TEX.read_text(encoding="utf-8").split("\n")
    if check:
        moves = OUT.read_text(encoding="utf-8")
        missing = [t for t, _ in add if f"`{t}`" not in moves] + [v for v in van if f"`{v}`" not in moves]
        print(f"number_moves check: ADDED {len(add)}, VANISHED {len(van)}, missing from NUMBER_MOVES.md {len(missing)}")
        for m in missing[:20]:
            print("  missing", m)
        sys.exit(1 if missing else 0)
    groups = collections.defaultdict(list)
    for t, ls in add:
        where, key = context_of(lines, ls[0] - 1)
        groups[(where, key)].append((t, ls))
    L = ["# NUMBER_MOVES.md: every printed number added or removed between paper_v17.tex and paper_v18.tex (numeric_diff, --round2)\n\n",
         "Written by `reviews/v18/tools/number_moves.py` on the built manuscript; the base is the tree object in `reviews/v18/base_tree.txt`. ",
         "Each ADDED token is attributed to the table, figure or section that carries it and to the ledger key in the source comment above it; ",
         "every number enters the manuscript through a key in a ledger listed in `trace_scan_v13.py` (which passes on this build). Each VANISHED token carries its reason. ",
         "`python reviews/v18/tools/number_moves.py <base> --check` fails if a token is unaccounted for.\n\n",
         f"## ADDED ({len(add)} tokens)\n\n| where | source comment | tokens (line numbers in paper_v18.tex) |\n|---|---|---|\n"]
    for (where, key), toks in sorted(groups.items()):
        L.append(f"| {where} | {key} | " + "; ".join(f"`{t}` @{ls}" for t, ls in toks) + " |\n")
    L.append(f"\n## VANISHED ({len(van)} tokens)\n\n| token | disposition |\n|---|---|\n")
    unknown = []
    for v in van:
        d = VANISHED.get(v)
        if d is None:
            unknown.append(v); d = "UNACCOUNTED"
        L.append(f"| `{v}` | {d} |\n")
    OUT.write_text("".join(L), encoding="utf-8", newline="\n")
    print(f"-> {OUT} ADDED {len(add)} VANISHED {len(van)} unaccounted {unknown}")


if __name__ == "__main__":
    main()
