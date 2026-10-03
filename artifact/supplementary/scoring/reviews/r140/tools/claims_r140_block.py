# -*- coding: utf-8 -*-
"""claims_r140_block.py -- the R140 entries of CLAIMS.md (2026-09-23), inside the R133 AUTHORIZATION BLOCK after the R139 section (idempotent: an existing R140
section, from its 'Program R140' line to the next '## ' heading or the end, is replaced). Entries: the units applied, the clarifications, and R140-F quoting every
frozen string of the v22 close that R140 changed on top of the R139 close (strings listed now and absent from reviews/v23/results/frozen_r139_close.json).
Usage: python reviews/r140/tools/claims_r140_block.py --json=reviews/v23/results/frozen_<tag>.json
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
CLAIMS = ROOT / "iclr2027_monitoring_submission" / "CLAIMS.md"
HEAD = "Program R140 (2026-09-23), inside this block:"
UNITS = ROOT / "reviews" / "r140" / "results" / "r140_close_units.txt"


def main():
    jarg = next(a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--json="))
    now = json.load(open(ROOT / jarg, encoding="utf-8"))
    base = {r["text"] for r in json.load(open(ROOT / "reviews" / "v23" / "results" / "frozen_r139_close.json", encoding="utf-8"))}
    changed = [r for r in now if r["text"] not in base]
    units = UNITS.read_text(encoding="utf-8").split() if UNITS.exists() else ["t1"]
    out = [f"\n{HEAD} the brief 'R140: the mock-15 fixes' ($0, no model run) on the R139 close 3342217; units applied: {', '.join(units)} (reviews/r140/tools/port_r140.py, every edit asserted; "
           "the verdicts the new words state checked by reviews/r140/tools/r140_number_gate.py against reviews/r139/results/equiv_r139.json; report reviews/r140/REPORT_R140.md).\n",
           "- **R140-CLARIFY [clarifications that narrow a claim's wording; no frozen claim changes meaning; dated 2026-09-23]** (recorded). The abstract, 5.2 and the Conclusion say that under the sibling-name control "
           "none of the five readers is reliably above the lookup and none is shown equivalent (AUX-R139-EQUIV, the five control rows 'neither'); the abstract's padded-list sentence reads 'longer than the stores we tested write' (the ruling of 23 Sep; FR-Bank's own lists 15.04 capped, 32.55 lifted, at most 50) "
           "and states that a list-length cue is uncontrolled there (AUX-R139-LENGTH); the builders box no longer states the priced-scenario outcome and reads 'whether the judgment pays for itself is unresolved (Appendix G.5)'; "
           "Limitations names what the explicit-intent rerun covered. Two ruled sentences are split at their own semicolon or clause for prose rule L (the R139 precedent).",
           f"- **R140-F [the frozen strings R140 changed on top of the R139 close; `{jarg}`]** (recorded). Every one is authorized as changed by the entry above."]
    for r in changed:
        out.append(f"  - CHANGED [{r['tag']} {r['key']}] {r['base']} -> {r['new']}: \"{r['text']}\"")
    text = "\n".join(out) + "\n"
    c = CLAIMS.read_text(encoding="utf-8")
    m = re.search(r"\n" + re.escape(HEAD) + r".*?(?=\n## |\Z)", c, flags=re.S)
    c = (c[:m.start()] + c[m.end():]) if m else c
    CLAIMS.write_text(c.rstrip("\n") + "\n" + text, encoding="utf-8", newline="\n")
    (ROOT / "reviews" / "r140" / "claims_r140_block.md").write_text(text, encoding="utf-8", newline="\n")
    print(f"-> CLAIMS.md R140 section: {len(changed)} frozen strings quoted")


if __name__ == "__main__":
    main()
