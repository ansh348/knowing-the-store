# -*- coding: utf-8 -*-
"""port_r143.py -- R143 (2026-09-23; $0): the merged alignment sentence restored to a place where it follows, on top of the R142 close (port_r142.py --units=close
underneath). Every edit is an asserted replacement. Units: mv (the sentence moves from after 'Control is outside this paper's scope.' to the end of the
run-conditions paragraph, after its pointer), p9 (payer (ix): mini's sentence shortened), pk (the Kimi sentence shortened), fb (the fallback: the sentence
moves to the end of the Control paragraph, after its pointer; not with mv). A2's comparison count is recomputed on the final main text through R139's list.
Usage: python reviews/r143/tools/port_r143.py --units=mv,p9,...   (--units=close reads reviews/r143/results/r143_close_units.txt)
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v23" / "src"
RES = ROOT / "reviews" / "r143" / "results"
BODY, ABS, APPX = SRC / "body_v23.tex", SRC / "abstract_v23.tex", SRC / "appendix_v23.tex"
ORDER = ["mv", "fb", "p9", "pk"]
TEXT, LOG = {}, []
M = "The $22$ obligations the manifest-to-record alignment does not mark are invisible to every summary (mini scores $0.52$ on them under ground truth)."
CTRL = "Control is outside this paper's scope. "


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def rep(which, old, new, unit, note=""):
    t = TEXT[which]
    assert t.count(old) == 1, f"[{unit}] {which}: expected 1, found {t.count(old)}: {old[:100]!r}"
    TEXT[which] = t.replace(old, new)
    LOG.append(dict(unit=unit, file=which, old=old, new=new, note=note))


def unit_mv():
    rep("body", CTRL + M + " ", CTRL, "mv", "R143 option 1/2: the sentence leaves the Control paragraph")
    rep("body", "the crossover ran every reader under both rubrics. (Appendix~\\ref{app:counterfactual})\n",
        "the crossover ran every reader under both rubrics. (Appendix~\\ref{app:counterfactual}) " + M + "\n", "mv", "R143: to the end of the run-conditions paragraph, its original home")


def unit_fb():
    rep("body", CTRL + M + " ", CTRL, "fb", "R143 option 3: the sentence leaves the paragraph's second place")
    rep("body", "nothing here shows that a better judgment changes an answer. (Appendix~\\ref{app:resp})\n",
        "nothing here shows that a better judgment changes an answer. (Appendix~\\ref{app:resp}) " + M + "\n", "fb", "R143 option 3: the Control paragraph's last sentence")


def unit_p9():
    rep("body", "mini drafted the questions and is also a reader; it is the weakest reader.", "mini drafted the questions and is also a reader, the weakest.", "p9", "R143 option 1: payer (ix)")


def unit_pk():
    rep("body", "Kimi K3, the one open-weights model, completed only the cross-vendor replication.", "Kimi K3 (open weights) completed only the cross-vendor replication.", "pk", "R143 option 2: the Kimi payer")


def unit_xa():
    rep("appendix", "; no sibling padded to equal length was run.", "; the sibling padded to equal length is the control of the next paragraph (Table~\\ref{tab:sb60}).", "xa", "R143 addendum a (C.2)")


def unit_xb():
    rep("appendix", "The notation box and the definition of the lifecycle summary, which the main text stated in full until this version, follow the two blocks,",
        "The notation box and the definition of the lifecycle summary follow the two blocks,", "xb", "R143 addendum b (E.1)")


def unit_xc():
    rep("body", "so a store can expose it without disclosing content", "so a store can expose it without disclosing stored values", "xc", "R143 addendum c (Section 1)")


def unit_xd():
    rep("body", "data cleaning, result interpretation, drafting,", "data cleaning, discussion of results, drafting,", "xd", "R143 addendum d (AI-use statement; the author: results were discussed with a model, interpreted by the authors)")


ORDER += ["xa", "xb", "xc", "xd"]
UNITS = {k: globals()[f"unit_{k}"] for k in ORDER}


def main():
    arg = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--units=")), "")
    units = (RES / "r143_close_units.txt").read_text(encoding="utf-8").split() if arg == "close" else [u for u in arg.split(",") if u]
    assert units == [u for u in ORDER if u in units] and not {"mv", "fb"} <= set(units), units
    r = subprocess.run([sys.executable, str(ROOT / "reviews" / "r142" / "tools" / "port_r142.py"), "--units=close"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-500:] + r.stderr[-500:]
    TEXT.update(body=rd(BODY), abstract=rd(ABS), appendix=rd(APPX))
    for u in units:
        UNITS[u]()
        print(f"unit {u}: applied")
    sys.path.insert(0, str(ROOT / "reviews" / "r139" / "tools"))
    import port_r139 as P139
    P139.TEXT.update(body=TEXT["body"], abstract=TEXT["abstract"])
    n = P139.count_n()
    m = re.search(r"reliable describes each of the \$(\d+)\$ comparisons the main text makes on its own\.", TEXT["body"])
    assert m and int(m.group(1)) == n, (n, m and m.group(1))
    for k, p in (("body", BODY), ("abstract", ABS), ("appendix", APPX)):
        p.write_text(TEXT[k], encoding="utf-8", newline="\n")
    RES.mkdir(parents=True, exist_ok=True)
    (RES / "port_r143_log.json").write_text(json.dumps(dict(units=units, n=n, edits=LOG), indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"-> {len(LOG)} edits; A2 {n}")


if __name__ == "__main__":
    main()
