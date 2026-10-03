# -*- coding: utf-8 -*-
"""claims_r139_block.py -- the R139 entries of CLAIMS.md (2026-09-23), written inside the R133 AUTHORIZATION BLOCK after the R137 section (one lineage,
one base, one block; idempotent: an existing R139 section, from its 'Program R139' line to the next '## ' heading or the end, is replaced).
Entries: the POSTHOC block (the two analyses, dated), the scope line (monitoring only, control deferred), the clarifications that narrow a claim's wording,
the units, and R139-F, which quotes every frozen string of the v22 close that R139 changed on top of the R137 close (the strings not KEPT now that were KEPT in
reviews/v23/results/frozen_r137_close.json), with the G9 Limitations text quoted old beside new.
Usage: python reviews/r139/tools/claims_r139_block.py --json=reviews/v23/results/frozen_<tag>.json
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
CLAIMS = SUB / "CLAIMS.md"
BLOCK = ROOT / "reviews" / "r139" / "claims_r139_block.md"
HEAD139 = "Program R139 (2026-09-23), inside this block:"
UNITS = (ROOT / "reviews" / "r139" / "results" / "r139_close_units.txt")

ENTRIES = [
    ("R139-POSTHOC [the brief 'KtS R139', Phase 1; dated 2026-09-22/23; POSTHOC class]",
     "Two analyses were added after every result they touch had been read, and each is labelled post hoc where it is printed. (1) Equivalence within $0.05$ by two one-sided tests at $5\\%$: "
     "a model-minus-lookup difference is equivalent when both of its $90\\%$ intervals (item-level or triple-level, and persona-grouped; the 5th and 95th percentiles of the same $1{,}000$ draws that give the "
     "printed $95\\%$ intervals) lie inside $[-0.05,+0.05]$; applied to every printed model-minus-lookup row of the default summary, the sibling-name control, the all-states summary, the padded set and the "
     "paraphrase set, and to the lookup with one count feature against each stronger reader (reviews/NUMBERS_R139.md AUX-R139-EQUIV, -E-GROUPS, -B6; Appendix C.2, tab:equiv and tab:equiv-para). "
     "No reliable verdict changed. (2) The length-only reader: its score is the number of names in the superseded-names section of the summary it is given; it wins every supersession triple on the default and "
     "the padded lists and ties every triple of the sibling-name control (AUX-R139-LENGTH; Appendix C.2, tab:length). The branch texts that use them were committed before either ran (reviews/r139/BRANCHES_R139.md, 6616e57)."),
    ("R139-SCOPE [the Unit G addendum and G9; dated 2026-09-23]",
     "The paper's scope is stated as monitoring only: it scores how accurately a reader judges the store from what it exposes (metamemory monitoring); whether the judgment changes what is retrieved or answered "
     "(control) is deferred to a later study, and so is any write-path intervention: every intervention in the paper is on the read side and the reach results describe what a store as shipped affords a reader. "
     "The abstract, Section 1, Section 7's title and first paragraph, Limitations and the Conclusion's first sentence say so (the author's texts, Q5, Q6 and Q9 as ruled)."),
    ("R139-CLARIFY [clarifications that narrow a claim's wording; no frozen claim changes meaning; dated 2026-09-23]",
     "'Within tolerance' is defined as a point difference no greater than $0.05$ that does not establish equivalence (Section 4); 'A fixed cue list matches the best model' reads 'is not reliably below the best model' "
     "with the crossover's own interval (5.3 and the Conclusion); 'ending level with it or below' reads 'ending at or below it with no reliable difference' (5.2); 'we ran no equivalence test' reads 'equivalence within $0.05$ "
     "is neither shown nor excluded' (5.2); the two Section 7 sentences on flagged answers are exploratory pointers to Appendix E.10 (G8); NOK is stated as a term the paper introduces (Section 1); "
     "A-MEM's census row is marked as not checked against the reference implementation (Table 3)."),
    ("R139-G7 [prose_scan WHITELIST; dated 2026-09-23]",
     "The Conclusion's first sentence as Unit G7 words it carries 'failed' in its ordinary sense and is whitelisted beside the R133 entry: \"In these monitoring tests, no reader we tried made up for what the store had failed to write down.\""),
    ("R139-TOOLS [gate and build changes; dated 2026-09-23]",
     "q_scan unwraps \\mbox{...} before it scans (a scanner defect the S6 guard exposed, not an exemption); build_v23.py applies reviews/r139/results/build_repairs_r139.json (S4 Table 73 to the text width; S5 four em-dash sites "
     "in appendix prose; the registered ADDENDUM_SIDE text keeps its em dashes verbatim by ruling); the style zip's own fancyhdr.sty beside the paper (S1; the .sty untouched); refcheck_v11's RETIRED gains the five "
     "bibitems S2 removed (ren2025, verbrouting, wang2023, metamem, seakr)."),
]


def frozen_rows(path):
    doc = json.load(open(ROOT / path, encoding="utf-8"))
    return doc


def main():
    jarg = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--json=")), None)
    assert jarg, "--json=reviews/v23/results/frozen_<tag>.json"
    now = json.load(open(ROOT / jarg, encoding="utf-8"))
    base = json.load(open(ROOT / "reviews" / "v23" / "results" / "frozen_r137_close.json", encoding="utf-8"))

    # the frozen_list_wp JSON lists the strings that are not KEPT; a string listed now and absent from the R137 close's list was KEPT there
    base_texts = {r["text"] for r in base}
    nn = {r["text"]: r for r in now if r["text"] not in base_texts}
    changed = list(nn)
    units = UNITS.read_text(encoding="utf-8").split() if UNITS.exists() else []
    out = [f"\n{HEAD139} the brief 'KtS R139: answer mock review 14 (W1, W2) in the paper, then the pre-upload sweep' (2026-09-22), the author's GO with rulings, the Unit G addendum with G9, and the rulings on the STOP "
           f"(22 Sep, 23:54), on the R137 close eb37054. Units applied: {', '.join(units) or '(see port_r139_log.json)'}. The edits are reviews/r139/tools/port_r139.py (every edit asserted), the numbers reviews/NUMBERS_R139.md "
           "(ledger_r139.py), the number gate reviews/r139/tools/r139_number_gate.py, the report reviews/r139/REPORT_R139.md. No model or API call.\n"]
    for head, body in ENTRIES:
        out.append(f"- **{head}** (recorded). {body}")
    out.append("- **R139-G9 [Limitations; the frozen sentence G9 and Q5 replace; dated 2026-09-23]** (recorded). Old: \"The counterfactual test bypasses backend writing, and no backend tested here is shown maintaining the summary.\" "
               "New: \"We change no backend's write path: the counterfactual test bypasses writing, every intervention is read-side, and no backend tested here is shown maintaining the summary, so the reach results describe "
               "what a store as shipped affords a reader; a write-path intervention is a separate study.\" The old sentence's claim (the test bypasses writing; no backend is shown maintaining the summary) is kept inside the new one.")
    out.append(f"- **R139-F [the frozen strings of the v22 close that R139 changed on top of the R137 close; `{jarg}`]** (recorded). Each string below was kept through the R137 close and occurs a different number of times after R139 "
               "(a count of zero means the sentence left the text or was reworded as the entries above record). Every one is authorized as changed by the pass under the entries above.")
    for t in changed:
        r = nn[t]
        out.append(f"  - CHANGED [{r['tag']} {r['key']}] {r['base']} -> {r['new']}: \"{t}\"")
    text = "\n".join(out) + "\n"
    BLOCK.write_text(text, encoding="utf-8", newline="\n")
    c = CLAIMS.read_text(encoding="utf-8")
    m = re.search(r"\n" + re.escape(HEAD139) + r".*?(?=\n## |\Z)", c, flags=re.S)
    c = (c[:m.start()] + c[m.end():]) if m else c
    c = c.rstrip("\n") + "\n" + text
    CLAIMS.write_text(c, encoding="utf-8", newline="\n")
    print(f"-> CLAIMS.md R139 section: {len(ENTRIES) + 2} entries, {len(changed)} frozen strings quoted in R139-F")


if __name__ == "__main__":
    main()
