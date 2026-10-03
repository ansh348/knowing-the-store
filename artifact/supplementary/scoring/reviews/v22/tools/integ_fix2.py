# -*- coding: utf-8 -*-
"""integ_fix2.py -- the overfull-box fixes of the integration pass (2026-09-16, program R112): the PN-vs-PRESENT table re-inlined from its
regenerated source (two columns fewer), the cov-lookup row label shortened, the provenance table's column widths reduced, the Graphiti
census table's wide columns set as paragraph columns. Asserted; idempotent. Run from the repository root.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v19" / "src"
X = SRC / "appendix_v19.tex"


def rep(t, old, new, name):
    n = t.count(old)
    if n == 0:
        return t                      # already applied (a later step may have moved past this state)
    assert n == 1, f"{name}: expected 1, found {n}"
    return t.replace(old, new)


def main():
    subprocess.run([sys.executable, str(ROOT / "reviews" / "v19" / "tools" / "ledger_posthoc.py")], check=True)
    gen = (SRC / "posthoc_tables_v19.tex").read_text(encoding="utf-8")
    table = gen[gen.index("\\begin{table}[H]"):gen.index("\\end{table}") + len("\\end{table}")]
    t = X.read_text(encoding="utf-8")
    i = t.index("\\label{tab:pnpresent}")
    s = t.rfind("\\begin{table}[H]", 0, i); e = t.index("\\end{table}", i) + len("\\end{table}")
    t = t[:s] + table + t[e:]
    t = rep(t, "FR-Bank easy tier, whole name map (post hoc) & $354$ / $243$", "Easy tier, whole map & $354$ / $243$", "cov-lookup label")
    t = rep(t, "\\begin{tabular}{@{}p{0.19\\linewidth}p{0.13\\linewidth}p{0.14\\linewidth}p{0.13\\linewidth}p{0.13\\linewidth}p{0.12\\linewidth}p{0.12\\linewidth}@{}}",
            "\\begin{tabular}{@{}p{0.18\\linewidth}p{0.12\\linewidth}p{0.135\\linewidth}p{0.125\\linewidth}p{0.125\\linewidth}p{0.115\\linewidth}p{0.115\\linewidth}@{}}", "provenance widths")
    t = rep(t, "\\begin{tabular}{@{}p{0.34\\linewidth}rrrrll@{}}", "\\begin{tabular}{@{}p{0.30\\linewidth}rrrrp{0.20\\linewidth}p{0.13\\linewidth}@{}}", "graphiti widths")
    t = rep(t, "\\begin{tabular}{@{}p{0.30\\linewidth}rrrrp{0.20\\linewidth}p{0.13\\linewidth}@{}}", "\\begin{tabular}{@{}p{0.28\\linewidth}rrrrp{0.19\\linewidth}p{0.12\\linewidth}@{}}", "graphiti widths 2")
    t = rep(t, "\\setlength{\\tabcolsep}{3pt}\n\\begin{tabular}{@{}p{0.28\\linewidth}", "\\setlength{\\tabcolsep}{2.5pt}\n\\begin{tabular}{@{}p{0.28\\linewidth}", "graphiti colsep")
    X.write_text(t, encoding="utf-8", newline="\n")
    print("fix2 applied")


if __name__ == "__main__":
    main()
