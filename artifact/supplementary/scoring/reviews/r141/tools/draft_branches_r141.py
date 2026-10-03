# -*- coding: utf-8 -*-
"""draft_branches_r141.py -- R141 Phase 0.5 (2026-09-24; $0, no model call): the main-text landing of each branch with PLACEHOLDER numbers of the printed
width ($0.82$ for the lookup, $0.10$ for a lead), applied on the R140 close (port_r140.py --units=close underneath), so the slack probe measures the page
cost of each branch before the run. Nothing here is the landing: the real numbers and the final wording land in Phase 3.
Usage: python reviews/r141/tools/draft_branches_r141.py --branch=bi|biii
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v23" / "src"
BODY, ABS = SRC / "body_v23.tex", SRC / "abstract_v23.tex"
AC2 = "(Appendix~\\ref{app:counterfactual})"
OLD_ABS = ("On lists longer than the stores we tested write, padded to $60$ names, the lookup loses $0.18$; \\mbox{GPT-5.6} Luna and Sol lose $0.06$ to $0.07$ and lead it by $0.13$ to $0.14$, "
           "while the other three fall with it. A list-length cue is uncontrolled there.")
OLD_52 = f"; the padded set has no such control {AC2}."
OLD_CON = "On a $60$-name list Luna and Sol lead the lookup by $0.13$ to $0.14$ and the other three fall with it. "
LIM_ANCHOR = "and the two readers that keep their lead there are from one model family. "


def rep(t, old, new):
    assert t.count(old) == 1, old[:80]
    return t.replace(old, new)


def main_bi_pay(a, b):
    b = rep(b, "Haiku and Opus were not run on it, and the padded lists' counts stay as written, so the superseded total disagrees with the list length in both versions alike. ",
            "Haiku and Opus were not run on it. ")
    ABS.write_text(a, encoding="utf-8", newline="\n")
    BODY.write_text(b, encoding="utf-8", newline="\n")
    print("draft branch bi_pay applied (placeholders)")


def main():
    br = next(a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--branch="))
    r = subprocess.run([sys.executable, str(ROOT / "reviews" / "r140" / "tools" / "port_r140.py"), "--units=close"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-500:]
    a, b = ABS.read_text(encoding="utf-8"), BODY.read_text(encoding="utf-8")
    if br in ("bi", "bi_pay"):
        a = rep(a, OLD_ABS, "Padded to $60$ names, the lookup loses $0.18$; \\mbox{GPT-5.6} Luna and Sol lose $0.06$ to $0.07$ and lead it by $0.13$ to $0.14$ while the other three fall with it, "
                            "and the lead holds against a sibling padded to the same length and counts.")
        b = rep(b, OLD_52, f". A sibling padded to the same length and counts, run on Luna, Sol and mini, removes that cue: the length-only reader ties every pair, the lookup scores $0.82$, "
                           f"and Luna and Sol lead it by a reliable $0.10$ and $0.10$ {AC2}.")
        b = rep(b, LIM_ANCHOR, LIM_ANCHOR + "The padded sibling control ran on Luna, Sol and mini; Haiku and Opus were not run on it, and the padded lists' counts stay as written, "
                                            "so the superseded total disagrees with the list length in both versions alike. ")
        b = rep(b, OLD_CON, "On a $60$-name list Luna and Sol lead the lookup by $0.13$ to $0.14$, with list length and counts fixed, and the other three fall with it. ")
    if br == "bi_pay":   # B-i with the L6 payer: Limitations' L1 sentence shortened to its first clause
        return main_bi_pay(a, b)
    elif br == "biii":
        a = rep(a, OLD_ABS, "Padded to $60$ names, the lookup loses $0.18$ and \\mbox{GPT-5.6} Luna and Sol keep more of their score, but against a sibling padded to the same length and counts "
                            "no model reliably beats the lookup.")
        b = rep(b, "\\claim{On the named state, no model reliably beats the lookup on the short list; on a long one, two do.}",
                "\\claim{On the named state, no model reliably beats the lookup on the short list, and on a $60$-name list none does once list length and counts are fixed.}")
        b = rep(b, OLD_52, f". A sibling padded to the same length and counts, run on Luna, Sol and mini, removes that cue and the lead with it: the lookup scores $0.82$ and no model is reliably above it {AC2}.")
        b = rep(b, ", and two of five do when it is padded to $60$ names.", ".")
        b = rep(b, OLD_CON, "")
        b = rep(b, "On a named state no model reliably exceeds the name lookup on the short list;", "On a named state no model reliably exceeds the name lookup on the short list, nor on a $60$-name list once its length is fixed;")
        b = rep(b, LIM_ANCHOR, LIM_ANCHOR + "The padded sibling control ran on Luna, Sol and mini; Haiku and Opus were not run on it. ")
    ABS.write_text(a, encoding="utf-8", newline="\n")
    BODY.write_text(b, encoding="utf-8", newline="\n")
    print(f"draft branch {br} applied (placeholders)")


if __name__ == "__main__":
    main()
