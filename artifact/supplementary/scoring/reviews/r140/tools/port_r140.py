# -*- coding: utf-8 -*-
"""port_r140.py -- R140 (2026-09-23; the brief 'R140: the mock-15 fixes', $0, no model run) on top of the R139 close (reviews/r139/tools/port_r139.py --units=close,
which regenerates the R137, R135, R134 and R133 closes underneath). Every edit is an asserted replacement; the verdicts the new words state (none of the five
readers equivalent to the lookup, and none reliably above it, under the sibling-name control) are read from reviews/r139/results/equiv_r139.json and checked
again by reviews/r140/tools/r140_number_gate.py.

Units: t1 (items 1 to 7, mandatory); t8, t9, t10 (T2, in order, only while the probe keeps slack >= 1); t11 (the non-zero-start split, conditional).
Usage: python reviews/r140/tools/port_r140.py --units=t1,t8,...   (--units=close reads reviews/r140/results/r140_close_units.txt)
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v23" / "src"
RES = ROOT / "reviews" / "r140" / "results"
BODY, ABS = SRC / "body_v23.tex", SRC / "abstract_v23.tex"
ORDER = ["t1", "t8", "t9", "t10", "t11"]
EQ = json.load(open(ROOT / "reviews" / "r139" / "results" / "equiv_r139.json", encoding="utf-8"))
SB = [r for r in EQ["rows"] if r["condition"] == "sibling-name control"]
assert len(SB) == 5 and not any(r["equivalent"] for r in SB) and not any(r["reliable"] and r["delta"] > 0 for r in SB), "the sibling-control verdicts the words state"
TEXT = {}
LOGGED = []


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def rep(which, old, new, unit="", note=""):
    t = TEXT[which]
    assert t.count(old) == 1, f"[{unit}] {which}: expected 1 occurrence, found {t.count(old)} of {old[:100]!r}"
    TEXT[which] = t.replace(old, new)
    LOGGED.append(dict(unit=unit, file=which, old=old, new=new, note=note))


def unit_t1():
    u = "t1"
    rep("abstract", "none of five language models reliably beats a cosine-similarity lookup over the names, including under a control that fixes counts and list length. The three stronger ones are equivalent to it within $0.05$.\n",
        "none of five language models reliably beats a cosine-similarity lookup over the names, and the three stronger ones are equivalent to it within $0.05$. Under a control that fixes counts and list length, none is reliably above it and none is shown equivalent.\n",
        u, "item 1 (AUX-R139-EQUIV: the five sibling-control rows, none equivalent, none reliably above); split at the semicolon (prose rule L: 56 words as one sentence)")
    rep("abstract", "On lists as long as real stores write, padded to $60$ names,", "On lists longer than the stores we tested write, padded to $60$ names,", u,
        "item 2 as ruled on 23 Sep ('longer than'; FR-Bank's own lists: 15.04 capped, 32.55 lifted, at most 50, Appendix E.9)")
    rep("abstract", "lead it by $0.13$ to $0.14$, while the other three fall with it.\n", "lead it by $0.13$ to $0.14$, while the other three fall with it. A list-length cue is uncontrolled there.\n", u,
        "item 2, the appended clause as its own sentence (prose rule L: the one sentence would run 46 words; the R139 precedent of ruled splits)")
    rep("body", "(Opus, the closest, $+0.02$ $[-0.02,+0.07]$)", "(Opus, the closest, $+0.02$ $[-0.02,+0.07]$) and none shown equivalent", u, "item 3")
    rep("body", "We apply that distinction to an external store \\citep{koriat1996}:", "Metamemory's monitoring and control distinction (Section~\\ref{sec:intro}) carries over to an external store \\citep{koriat1996}:", u, "item 4")
    rep("body", "(Sections~\\ref{sec:lookup} and~\\ref{sec:backends}), and a model call before every query cost more than the retrieval it saved (Appendix~\\ref{app:utility-completion}).",
        "(Sections~\\ref{sec:lookup} and~\\ref{sec:backends}); whether the judgment pays for itself is unresolved (Appendix~\\ref{app:utility-completion}).", u, "item 5")
    rep("body", "Under the explicit-intent rubric only mini and Luna were rerun.",
        "The counterfactual set itself was rerun under the explicit-intent rubric for mini and Luna only; the crossover ran every reader under both rubrics.", u, "item 6")
    rep("body", "On a named state no model reliably exceeds the name lookup on the short list, with list length kept fixed or not; the three stronger readers are equivalent to it within $0.05$.",
        "On a named state no model reliably exceeds the name lookup on the short list; the three stronger readers are equivalent to it within $0.05$, though not under the control that fixes list length.", u, "item 7")


def unit_t8():
    # the brief's 'registered in the repository's commit history' trips prose rule V and code_scan ('registered' in the main text); the R139 ruling on S3 ('keep the meaning, lose the word') applied
    rep("body", "The predictions were registered with a bar, each before the run that tests it", "The predictions were written into the repository's commit history (Appendix~\\ref{app:registration}), each before the run that tests it", "t8",
        "item 8 (rule V: 'registered' -> 'written into', the S3 precedent)")


def unit_t9():
    rep("body", "an attribute-name list with the values removed.", "an attribute-name list with the values removed, so a store can expose it without disclosing content.", "t9", "item 9")


def unit_t10():
    rep("body", "for Haiku neither holds (Appendix~\\ref{app:counterfactual}).",
        "for Haiku neither holds (Appendix~\\ref{app:counterfactual}). At that ceiling equivalence is the expected outcome; the sibling-name control is where a reader could show more, and none does.", "t10", "item 10")


def unit_t11():
    raise SystemExit("t11 is conditional (slack >= 2 after t8 to t10, before 19:00); not built")


UNITS = {k: globals()[f"unit_{k}"] for k in ORDER}


def main():
    arg = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--units=")), "")
    units = (RES / "r140_close_units.txt").read_text(encoding="utf-8").split() if arg == "close" else [u for u in arg.split(",") if u]
    assert units == [u for u in ORDER if u in units], units
    r = subprocess.run([sys.executable, str(ROOT / "reviews" / "r139" / "tools" / "port_r139.py"), "--units=close"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-600:] + r.stderr[-600:]
    TEXT.update(body=rd(BODY), abstract=rd(ABS))
    for u in units:
        UNITS[u]()
        print(f"unit {u}: applied")
    BODY.write_text(TEXT["body"], encoding="utf-8", newline="\n")
    ABS.write_text(TEXT["abstract"], encoding="utf-8", newline="\n")
    RES.mkdir(parents=True, exist_ok=True)
    (RES / "port_r140_log.json").write_text(json.dumps(dict(units=units, edits=LOGGED), indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"-> {len(LOGGED)} edits")


if __name__ == "__main__":
    main()
