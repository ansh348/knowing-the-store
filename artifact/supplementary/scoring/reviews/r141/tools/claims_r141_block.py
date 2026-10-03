# -*- coding: utf-8 -*-
"""claims_r141_block.py -- the R141 entries of CLAIMS.md (2026-09-23), inside the R133 AUTHORIZATION BLOCK after the R140 section (idempotent: an existing R141
section, from its 'Program R141' line to the next '## ' heading or the end, is replaced). Entries: the landing of ADDENDUM_R141_SB60's fired branch, the ruled
wording, the payers, and R141-F quoting every frozen string of the v22 close that R141 changed on top of the R140 close (strings listed now and absent from
reviews/v23/results/frozen_r140_close.json).
Usage: python reviews/r141/tools/claims_r141_block.py --json=reviews/v23/results/frozen_<tag>.json
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
CLAIMS = ROOT / "iclr2027_monitoring_submission" / "CLAIMS.md"
HEAD = "Program R141 (2026-09-23), inside this block:"
UNITS = ROOT / "reviews" / "r141" / "results" / "r141_close_units.txt"


def main():
    jarg = next(a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--json="))
    now = json.load(open(ROOT / jarg, encoding="utf-8"))
    base = {r["text"] for r in json.load(open(ROOT / "reviews" / "v23" / "results" / "frozen_r140_close.json", encoding="utf-8"))}
    changed = [r for r in now if r["text"] not in base]
    units = UNITS.read_text(encoding="utf-8").split()
    out = [f"\n{HEAD} the brief 'R141: the sibling-name control at 60 names' on the R140 close 86a72dd / 42b6951; the registration reviews/r141/registrations/ADDENDUM_R141_SB60.md frozen alone at f224177 "
           "(registered text sha256 4fc25a8b; the commit date 2026-09-23, day 44, governs over the text's '24 Sep' line); run 2588717 (OpenAI $2.9372 of the $12 cap), scored 7a62892; "
           f"branch B-ii fired (P-S1 fails, P-S2 to P-S4 hold), landed with Sol named; units applied: {', '.join(units)} (reviews/r141/tools/port_r141.py, every edit asserted; "
           "the numbers reviews/NUMBERS_R141.md, the number gate reviews/r141/tools/r141_number_gate.py; report reviews/r141/REPORT_R141.md).\n",
           "- **R141-LAND [the fired branch; dated 2026-09-23]** (recorded). The B-ii texts are the frozen B-i texts with Sol named (the author's ruling 1 on the B-ii stop); the abstract reads "
           "'The lead holds for Sol against a sibling padded to the same length and counts.'; the Conclusion '... and, with list length and counts fixed, Sol by 0.09; the other three fall with it.'; "
           "5.2 words Luna's result as 'Luna's lead holds on the pooled metric only (0.11, reliable) and not within triples (+0.04)', a wording deviation from the registered clause "
           "'Luna's lead is not separated from the cue' (which Limitations keeps), recorded in C.2 and AUX-R141-DISCREPANCIES. The prediction count moves to 106 / 34 and A2's comparison count to 71.",
           "- **R141-PAY [the page payers; no claim changes meaning]** (recorded). Payers a, b, c (ruled 23 Sep) and payer (v) of the ruling on the last line: Limitations' two alignment sentences "
           "merged into one ('The 22 obligations the manifest-to-record alignment does not mark are invisible to every summary (mini scores 0.52 on them under ground truth).'). "
           "Payers (i) to (iv) left the probe at +0 and were reverted by ruling; (v) gave +1 (reviews/r141/results/slack_r141.md).",
           f"- **R141-F [the frozen strings R141 changed on top of the R140 close; `{jarg}`]** (recorded). Every one is authorized as changed by the entries above."]
    for r in changed:
        out.append(f"  - CHANGED [{r['tag']} {r['key']}] {r['base']} -> {r['new']}: \"{r['text']}\"")
    text = "\n".join(out) + "\n"
    c = CLAIMS.read_text(encoding="utf-8")
    m = re.search(r"\n" + re.escape(HEAD) + r".*?(?=\n## |\Z)", c, flags=re.S)
    c = (c[:m.start()] + c[m.end():]) if m else c
    CLAIMS.write_text(c.rstrip("\n") + "\n" + text, encoding="utf-8", newline="\n")
    (ROOT / "reviews" / "r141" / "claims_r141_block.md").write_text(text, encoding="utf-8", newline="\n")
    print(f"-> CLAIMS.md R141 section: {len(changed)} frozen strings quoted")


if __name__ == "__main__":
    main()
