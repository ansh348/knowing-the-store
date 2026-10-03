# -*- coding: utf-8 -*-
"""port_r144.py -- R144 (2026-09-23; $0): the last wording pass before upload, on top of the R143 close with unit xd (port_r143.py --units=close
underneath). Every edit is an asserted replacement. Units: e1 (builders box: the 60-name list), e2 (abstract: 'On the short lists'), e3 (Table 2's caption:
'Rows marked p are post hoc.'), e4 (Section 6 claim: 'little above chance'; optional), p1 (payer: mini's Limitations sentence dropped), p2 (payer: the Kimi
Limitations sentence dropped), bs (the box sentence split at its semicolon, only if q_scan's 40-word rule fires). A2's comparison count is recomputed on the
final main text through R139's list.
Usage: python reviews/r144/tools/port_r144.py --units=e1,e2,...   (--units=close reads reviews/r144/results/r144_close_units.txt)
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v23" / "src"
RES = ROOT / "reviews" / "r144" / "results"
BODY, ABS, APPX, ROBUST = SRC / "body_v23.tex", SRC / "abstract_v23.tex", SRC / "appendix_v23.tex", SRC / "robust_table.tex"
ORDER = ["e1", "bs", "e2", "e3", "e4", "p1", "p2"]
TEXT, LOG = {}, []


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def rep(which, old, new, unit, note=""):
    t = TEXT[which]
    assert t.count(old) == 1, f"[{unit}] {which}: expected 1, found {t.count(old)}: {old[:100]!r}"
    TEXT[which] = t.replace(old, new)
    LOG.append(dict(unit=unit, file=which, old=old, new=new, note=note))


def unit_e1():
    rep("body", "on explicit intent questions and, pooled only, in two further conditions",
        "on explicit intent questions, on a $60$-name list and, pooled only, in two further conditions", "e1", "R144 E1 (builders box)")


def unit_bs():
    rep("body", "(Sections~\\ref{sec:lookup} and~\\ref{sec:backends}); whether the judgment pays for itself is unresolved",
        "(Sections~\\ref{sec:lookup} and~\\ref{sec:backends}). Whether the judgment pays for itself is unresolved", "bs", "R144: the box sentence split at its semicolon (q_scan 40-word rule)")


def unit_e2():
    rep("abstract", "The three stronger readers lead only where the summary counts a state without naming it,",
        "On the short lists the three stronger readers lead only where the summary counts a state without naming it,", "e2", "R144 E2 (abstract)")


def unit_e3():
    rep("robust", "In row 9 retraction and expiry do not move, since the list names neither. (Appendices",
        "In row 9 retraction and expiry do not move, since the list names neither. Rows marked $^{p}$ are post hoc. (Appendices", "e3", "R144 E3 (Table 2 caption; the row labels' $^{p}$ markup)")


def unit_e4():
    rep("body", "\\claim{FR-Bank's metadata leave mini and the lookup near chance.}",
        "\\claim{FR-Bank's metadata leave mini and the lookup little above chance.}", "e4", "R144 E4 (Section 6; optional)")


def unit_p1():
    rep("body", " \\mbox{GPT-4.1} mini drafted the questions and is also a reader, the weakest.", "", "p1", "R144 payer P1 (Limitations)")


def unit_p2():
    rep("body", " Kimi K3, the one open-weights model, completed only the cross-vendor replication.", "", "p2", "R144 payer P2 (Limitations)")


UNITS = {k: globals()[f"unit_{k}"] for k in ORDER}


def main():
    arg = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--units=")), "")
    units = (RES / "r144_close_units.txt").read_text(encoding="utf-8").split() if arg == "close" else [u for u in arg.split(",") if u]
    assert units == [u for u in ORDER if u in units], units
    r = subprocess.run([sys.executable, str(ROOT / "reviews" / "r143" / "tools" / "port_r143.py"), "--units=close"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-500:] + r.stderr[-500:]
    TEXT.update(body=rd(BODY), abstract=rd(ABS), appendix=rd(APPX), robust=rd(ROBUST))
    for u in units:
        UNITS[u]()
        print(f"unit {u}: applied")
    sys.path.insert(0, str(ROOT / "reviews" / "r139" / "tools"))
    import port_r139 as P139
    P139.TEXT.update(body=TEXT["body"], abstract=TEXT["abstract"])
    n = P139.count_n()
    m = re.search(r"reliable describes each of the \$(\d+)\$ comparisons the main text makes on its own\.", TEXT["body"])
    assert m and int(m.group(1)) == n, (n, m and m.group(1))
    for k, p in (("body", BODY), ("abstract", ABS), ("appendix", APPX), ("robust", ROBUST)):
        p.write_text(TEXT[k], encoding="utf-8", newline="\n")
    RES.mkdir(parents=True, exist_ok=True)
    (RES / "port_r144_log.json").write_text(json.dumps(dict(units=units, n=n, edits=LOG), indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"-> {len(LOG)} edits; A2 {n}")


if __name__ == "__main__":
    main()
