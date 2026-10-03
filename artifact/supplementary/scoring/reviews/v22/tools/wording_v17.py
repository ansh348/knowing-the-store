# -*- coding: utf-8 -*-
"""wording_v17.py -- the v17 wording corrections ordered by the author on 2026-09-14 (CC_PASS_v18 Phase 1, item W).
NO NUMBER CHANGES. Two corrections, both wording:

  1. What the count-randomized summary did. v2r permutes the two LIFECYCLE TOTALS lines (retracted, expired) across the
     444 store versions; the PER-CATEGORY BREAKDOWN's RETRACT and EXPIRED columns are untouched (index_v2r.py:19-21;
     AUX-CF2-V2R-DEF, r82_counterfactual/cf2/NUMBERS_CF2.md). Section 5's sentence "No reader uses the tally, because
     randomizing the counts across versions ..." over-reached; it becomes the author's sentence. Every mention of the
     arm says "totals": the arm is renamed from "count-randomized summary" to "totals-randomized summary" in the
     Appendix C.2 prose, the Table 13 caption and its row label, and the Table 39 row.
     The author's third clause ("Table 1 shows what they carry against what the models read") enters with v18, when
     Table 1 carries the CR rows; v17's Table 1 has none.
  2. The concession sentence and its echo are deleted with nothing in their place (the reader-claim ruling; prose_scan
     rule G): Section 1's "That a similarity lookup does so is the sanity check of this paper rather than its finding."
     and "The contribution lies past that check, in three parts."

Edits the v17 sources in place (reviews/v17/src/body_v17.tex, appendix_v17.tex), each replacement asserted to occur
exactly once; the two edits inside carried v11 blocks (the Table 13 caption and row label) go through build_v17.py's
REPAIRS list, which this script installs. Then run reviews/v17/tools/build_v17.py.

Usage: python reviews/v18/tools/wording_v17.py
"""
from __future__ import annotations

import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v17" / "src"
BUILD = ROOT / "reviews" / "v17" / "tools" / "build_v17.py"

BODY = [
    ("No reader uses the tally, because randomizing the counts across versions moves each reader by at most $+0.01$ on the whole set, with every interval within $\\pm0.05$.\n",
     "Randomizing the lifecycle totals moves each reader by at most $+0.01$ on the whole set, with every interval within $\\pm0.05$; the per-category tallies were not randomized in that check.\n"),
    ("That a similarity lookup does so is the sanity check of this paper rather than its finding.\n", ""),
    ("The contribution lies past that check, in three parts.\n", ""),
]
APPX = [
    ("The count-randomized summary permutes the retracted and expired totals across the $444$ store versions under a recorded seed, so that no version keeps its own pair and every value keeps its multiplicity",
     "The totals-randomized summary permutes the retracted and expired lifecycle totals across the $444$ store versions under a recorded seed, so that no version keeps its own pair and every value keeps its multiplicity; the per-category tallies are not touched"),
    ("and $0$ of $30$ on the count-randomized one.", "and $0$ of $30$ on the totals-randomized one."),
    ("every reader inside the count-randomization band", "every reader inside the totals-randomization band"),
]
# inside carried v11 blocks (Table 13 caption, v11:1195; its row label, v11:1251)
REPAIRS = [
    ("and the first with its retracted and expired counts randomized across store versions.",
     "and the first with its two lifecycle totals, retracted and expired, permuted across store versions (the per-category tallies untouched)."),
    ("it had no count-randomized summary", "it had no totals-randomized summary"),
    ("the first form has no count-randomized value", "the first form has no totals-randomized value"),
    ("\\textit{Counts randomized minus superseded only, whole set (band $\\pm0.05$)}",
     "\\textit{Totals randomized minus superseded only, whole set (band $\\pm0.05$)}"),
]
REPAIRS_MARK = "REPAIRS = [  # v18 W: wording corrections inside carried blocks (reviews/v18/tools/wording_v17.py)\n"


def edit(path, pairs):
    t = io.open(path, encoding="utf-8").read()
    for old, new in pairs:
        n = t.count(old)
        assert n == 1, f"{path.name}: expected exactly one occurrence, found {n}: {old[:70]!r}"
        t = t.replace(old, new)
    io.open(path, "w", encoding="utf-8", newline="\n").write(t)
    print(f"  {path.relative_to(ROOT)}: {len(pairs)} replacement(s)")


def install_repairs():
    t = io.open(BUILD, encoding="utf-8").read()
    if REPAIRS_MARK in t:
        print("  build_v17.py: REPAIRS already installed"); return
    block = REPAIRS_MARK + "".join(f"    ({old!r},\n     {new!r}),\n" for old, new in REPAIRS) + "]\n\n\n"
    anchor = "def main():\n"
    assert t.count(anchor) == 1
    t = t.replace(anchor, block + anchor)
    old_loop = "        for ln in block:\n            if \"\\textit{Monitors}\" in ln:"
    assert t.count(old_loop) == 1, "repair loop anchor not found"
    new_loop = ("        for ln in block:\n"
                "            for o, n_ in REPAIRS:\n"
                "                if o in ln:\n"
                "                    ln = ln.replace(o, n_); n_repair[0] += 1\n"
                "            if \"\\textit{Monitors}\" in ln:")
    t = t.replace(old_loop, new_loop)
    t = t.replace("    n_typo = 0\n", "    n_typo = 0\n    n_repair = [0]\n", 1)
    t = t.replace('    print(f"typo repairs applied inside carried blocks: {n_typo}")\n',
                  '    print(f"typo repairs applied inside carried blocks: {n_typo}")\n'
                  '    print(f"v18 W wording repairs applied inside carried blocks: {n_repair[0]} (expected {len(REPAIRS)})")\n'
                  '    assert n_repair[0] == len(REPAIRS), "a carried-block repair did not apply exactly once"\n', 1)
    io.open(BUILD, "w", encoding="utf-8", newline="\n").write(t)
    print(f"  build_v17.py: REPAIRS installed ({len(REPAIRS)} entries)")


def main():
    edit(SRC / "body_v17.tex", BODY)
    edit(SRC / "appendix_v17.tex", APPX)
    install_repairs()
    print("now run: python reviews/v17/tools/build_v17.py")


if __name__ == "__main__":
    main()
