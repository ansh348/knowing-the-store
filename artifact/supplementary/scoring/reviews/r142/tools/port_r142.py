# -*- coding: utf-8 -*-
"""port_r142.py -- R142 (2026-09-23; $0): the two headline sentences B-ii left stale, plus one scoping edit, on top of the R141 close (port_r141.py --units=close
underneath). Every edit is an asserted replacement. Units: e1 (5.2's lead claim, the brief's wording), e1s (its shorter alternative, used only if e1 costs a line),
e2 (the Introduction's second bullet), e3 (Section 6's lead claim). A2's comparison count is recomputed on the final main text through R139's list.
Usage: python reviews/r142/tools/port_r142.py --units=e1,e2,...   (--units=close reads reviews/r142/results/r142_close_units.txt)
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v23" / "src"
RES = ROOT / "reviews" / "r142" / "results"
BODY, ABS = SRC / "body_v23.tex", SRC / "abstract_v23.tex"
ORDER = ["e1", "e1s", "e2", "e3"]
TEXT, LOG = {}, []
CLAIM_OLD = "\\claim{On the named state, no model reliably beats the lookup on the short list; on a long one, two do.}"


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def rep(which, old, new, unit, note=""):
    t = TEXT[which]
    assert t.count(old) == 1, f"[{unit}] {which}: expected 1, found {t.count(old)}: {old[:100]!r}"
    TEXT[which] = t.replace(old, new)
    LOG.append(dict(unit=unit, file=which, old=old, new=new, note=note))


def unit_e1():
    rep("body", CLAIM_OLD, "\\claim{On the named state, no model reliably beats the lookup on the short list; on a long one, Sol does with list length and counts fixed.}", "e1", "R142 item 1 (B-ii carried into 5.2's lead)")


def unit_e1s():
    rep("body", CLAIM_OLD, "\\claim{On the named state, no model reliably beats the lookup on the short list; on a long one, one does with list length fixed.}", "e1s", "R142 item 1, the shorter alternative")


def unit_e2():
    rep("body", "and two of five do when it is padded to $60$ names.", "and one does on a $60$-name list with its length and counts fixed.", "e2", "R142 item 2 (B-ii carried into the Introduction's second bullet)")


def unit_e3():
    rep("body", "\\claim{Backends omit or misstate the lifecycle information readers need.}", "\\claim{The backends we tested omit or misstate the lifecycle information readers need.}", "e3", "R142 item 3 (scoping)")


UNITS = {k: globals()[f"unit_{k}"] for k in ORDER}


def main():
    arg = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--units=")), "")
    units = (RES / "r142_close_units.txt").read_text(encoding="utf-8").split() if arg == "close" else [u for u in arg.split(",") if u]
    assert units == [u for u in ORDER if u in units] and not {"e1", "e1s"} <= set(units), units
    r = subprocess.run([sys.executable, str(ROOT / "reviews" / "r141" / "tools" / "port_r141.py"), "--units=close"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-500:] + r.stderr[-500:]
    TEXT.update(body=rd(BODY), abstract=rd(ABS))
    for u in units:
        UNITS[u]()
        print(f"unit {u}: applied")
    sys.path.insert(0, str(ROOT / "reviews" / "r139" / "tools"))
    import port_r139 as P139
    P139.TEXT.update(body=TEXT["body"], abstract=TEXT["abstract"])
    n = P139.count_n()
    m = re.search(r"reliable describes each of the \$(\d+)\$ comparisons the main text makes on its own\.", TEXT["body"])
    assert m, "A2's count sentence not found"
    if int(m.group(1)) != n:
        rep("body", m.group(0), m.group(0).replace(f"${m.group(1)}$", f"${n}$"), "N", f"A2's count recomputed: {n}")
    for k, p in (("body", BODY), ("abstract", ABS)):
        p.write_text(TEXT[k], encoding="utf-8", newline="\n")
    RES.mkdir(parents=True, exist_ok=True)
    (RES / "port_r142_log.json").write_text(json.dumps(dict(units=units, n=n, edits=LOG), indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"-> {len(LOG)} edits; A2 {n}")


if __name__ == "__main__":
    main()
