# -*- coding: utf-8 -*-
"""claims_r135_block.py -- the R135 entries of CLAIMS.md (2026-09-21; the brief 'R135: THE LAST CONTENT PASS ON v23', 'R135 ADDENDUM', the rulings on ADDENDUM 2
and on the TABLE step), written inside the R133 AUTHORIZATION BLOCK after the R134 section (one lineage, one base, one block). Written to
reviews/v23/claims_r135_block.md and inserted at the end of the R133 block (idempotent: an existing R135 section, from its 'Program R135' line to the next '## '
heading, is replaced). Entries: one per unit of reviews/v23/tools/port_r135.py that has been applied (reviews/v23/results/port_r135_log.json), the gate
interactions, and R135-F, which quotes every frozen string of the v22 close that R135 changed on top of the R134 close (the strings not KEPT now that were KEPT
in reviews/v23/results/frozen_r134_close.json).
Usage: python reviews/v23/tools/claims_r135_block.py [--json=reviews/v23/results/frozen_<tag>.json]
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
CLAIMS = SUB / "CLAIMS.md"
BLOCK = ROOT / "reviews" / "v23" / "claims_r135_block.md"
LOG = ROOT / "reviews" / "v23" / "results" / "port_r135_log.json"
HEAD133 = "## R133 AUTHORIZATION BLOCK — dated 2026-09-21"
HEAD135 = "Program R135 (2026-09-21), inside this block:"

ENTRIES = {
    "table": ("R135-TABLE [section 2 of the brief and the R135 ADDENDUM: the robustness table]",
              "The evidence box at the end of Section 3 removed (its four limits: the matched comparison is post hoc in Section 4's AUROC paragraph and Limitations; alignment can miss forbidding records in Limitations' 22 obligations; "
              "census counts have no sampling interval in Table 2's caption; the answer detector is provisional in Limitations' 'exploratory ... human validation is unfinished'). Section 5.2's opening paragraph gains "
              "'Table~\\ref{tab:robust} lists the checks we ran to break this result and what each removes.' and the float tab:robust follows it (reviews/v23/src/robust_table.tex from robust_tex.py: three columns, ten rows, "
              "rows 2 and 5 marked post hoc; the caption states metric and population per row and ends with the deleted paragraph's caveat 'Short ground-truth lists do not establish robustness to longer store-written ones.'). "
              "The two paragraphs the table absorbs leave 5.2 ('List length and coverage lift both metrics.'; 'Long or wrong name lists weaken the readers together.'): 0.13, 60 and 0.67 print in the table, 0.75 in Appendix C.2 "
              "(NUMBER_MOVES_V23.md, moved). The rewording paragraph reads 'With the questions rewritten to share no content word with any name in the summary ($115$ pairs), the embedding lookup loses $0.02$ and the two smaller "
              "models lose more (Table~\\ref{tab:robust}).' before its unchanged Branch B, all-states and vaguer sentences; 5.2 points to Appendix C.2 once. The R135 ADDENDUM: Section 5.1's second paragraph opens "
              "'The two smaller models lose nothing when the counts are removed. With every count deleted, mini and Haiku score as before (Table~\\ref{tab:robust}); given the counts alone, they fall by $0.14$.' and its third paragraph "
              "is the ADDENDUM's text verbatim (no 0.28 to 0.33, 0.06 or 0.04; they print in the table). The cells shrunk twice so every row is one line (the brief's section 6); the five ledger-driven cell wordings "
              "accepted by the author's ruling, row 9 reading 'mini and Haiku falling with it, within $0.02$ of the lookup'. Every cell through r135_number_gate.py (99 checks, 0 mismatches; reviews/NUMBERS_R135.md)."),
    "abstract": ("R135-ABSTRACT [section 3 of the brief]",
                 "The abstract replaced by the brief's text, verbatim but for the G2 ruling (option c): the parenthetical '(all readers at $0.88$ AUROC or higher)' deleted, because prose_scan's G2 (the abstract must not state the lookup's own level; no allowlist by the 14 September ruling) fired on it; no rule change, no exemption; 0.88 moved to tab:robust row 3. "
                 "The HV-1 placeholder clause leaves with the abstract's last sentence 'All stores are synthetic, and we do not show that better judgments "
                 "yield better answers.'; 0.08 to 0.10 and 0.05 to 0.06 leave the abstract and still print in Section 5.2 (NUMBER_MOVES_V23.md, moved). Numbers through r135_number_gate.py (148; 0.88 the sibling floor; 0.02; 0.04; "
                 "0.73 / 0.82 / 0.75 to 0.60 / 0.71 / 0.59). The two R134 AUTHOR-RULING entries for the R134 abstract's sentences retired (gate_edits_r135.py)."),
    "fig3": ("R135-FIG3 [section 4 of the brief; the ruling: no height raise]",
             "Figure 3 redrawn from the same data file in the Okabe-Ito palette (mini E69F00, Haiku 56B4E9, Luna 009E73, Sol D55E00, Opus 0072B2, the lookup black as before, the count reader CC79A7), the R126 marker shapes kept so the figure "
             "survives greyscale, the legend's content, size and layout unchanged; the height not raised (the ruling reserves the slack for two later landings)."),
    "small": ("R135-SMALL [section 5 of the brief]",
              "5.1 the builders box's sentence gains 'and under FR-Bank's store-written summary, where Haiku sits $0.12$ above the lookup' before 'and in the scenario we priced' (AUX-BH-H45-15 Haiku minus lookup +0.1212, "
              "both intervals above zero). 5.3 G.5's opaque sentence 'Valentina's omitted source supports the disputed hobbies; ...' reads 'For one question, a persona's hobbies, the original reference packet had omitted the session "
              "that supports the answer; with that source restored, the repaired judge marks every condition's answer correct for that question.'; G.5 kept. 5.2 not applied: the HV-1 status lines stay verbatim by the pass's own rule "
              "and the ADDENDUM 2 ruling. 5.4 repro_mem0_erase.py copied to ARTIFACT/verifier/ beside repro_amem_links.py; the five uncited bibliography entries checked (REPORT_R135.md)."),
    "a2": ("R135-A2 [ADDENDUM 2 as ruled: the last unit before the close]",
           "1 Section 4, after 'Readers return probabilities under a fixed rubric.': 'The scored step asks whether stale content about the question's target is present, which coincides with Definition 1's obligation on the counterfactual set, "
           "where every question has current or upcoming intent; Section 5.3 tests intent separately.' (the definition and the section through their labels). 2 Section 7: 'Propagating a lifecycle tag to matching lines under the same attribute "
           "changes $1$ of $452$ assembled views under the reference tags. Under FR-Bank's own tags the same rule changes $90$ views and fully tags $15$ of the $35$ duplicate views, but it also propagates falsely ($69$ of $2{,}333$ licensed "
           "active lines).' (tab:ds-a8's own-tags primary column; AUX-DS-A8-RULE-CENSUS, -DUP35, -FALSEPROP). 3 G.2's clause 'the control is the paraphrased counterfactual set, registered and pending (tab:registrations-c)' reads 'the control is "
           "the paraphrase check reported in Appendix C.2, with this split recomputed on the rewrites (tab:para-flags)'. 4 the three Graphiti Amendment 2 lines (tab:registrations-d's outcome, the count paragraph, G.5) read 'not completed at "
           "submission' for 'pending'; the C.2 run notes read 'then pending'; the three HV-1 placeholders in E.10 untouched."),
    "fig3h": ("R135-FIG3H [not applied]", "The height raise is not applied (the ruling)."),
}


def quotable(text):
    if '"' not in text:
        return text
    parts = [p.strip() for p in text.split('"')]
    best = max(parts, key=len)
    assert len(best) >= 30, text
    return best


def flat(s):
    return s.strip().replace("\n\n", " [paragraph break] ").replace("\n", " ")


def main():
    js = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--json=")), None)
    log = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else {"units": [], "edits": []}
    units = log["units"]
    L = ["", HEAD135 + " the last content pass on v23 (the brief 'R135: THE LAST CONTENT PASS ON v23', 'R135 ADDENDUM', the ruling on ADDENDUM 2 and the ruling on the TABLE step; 2026-09-21; $0) on the R134 close 69ca17a. "
         "The results pipeline is reviews/v23/tools/robust_tex.py (tab:robust and reviews/v23/results/robust_printed.json), the number gate r135_number_gate.py (R134's 62 checks and 37 of its own), the ledger reviews/NUMBERS_R135.md "
         "(ledger_r135.py), the edits port_r135.py (every edit asserted, on the regenerated R134 close), the gate edits gate_edits_r135.py, the pins pin_appendix_r134.py (steps r135 and small), the probe slack_r135.py, the report "
         "reviews/v23/REPORT_R135.md, the sign-off file reviews/v23/OLD_BESIDE_NEW_R135.md. v22 stays frozen. No model call.", ""]
    for u in units:
        title, text = ENTRIES[u]
        L.append(f"- **{title}** (recorded). {text}")
    L.append("- **R135-G [the gate interactions]** (recorded). tools/prose_scan.py WHITELIST: the two R134 entries for the R134 abstract's sentences retired (neither sentence remains); an entry for the brief's abstract only where a prose rule "
             "fires inside it and the ruling allows it (listed in REPORT_R135.md); nothing else exempted. reviews/v23/tools/r134_number_gate.py numerals(): '{,}' read as ',' and tabular column specs dropped (layout, as trace_scan reads them). "
             "run_gates.py runs r135_number_gate.py; build_v23.py splices tab:robust at its marker; number_moves_wp.py records the tokens that moved within the paper (the two deleted paragraphs', the 5.1 trims', the abstract's) and the evidence box's layout token.")
    if js:
        rows = json.loads((ROOT / js).read_text(encoding="utf-8"))
        base = {r["text"] for r in json.loads((ROOT / "reviews" / "v23" / "results" / "frozen_r134_close.json").read_text(encoding="utf-8")) if r["status"] != "KEPT"}
        changed = [r for r in rows if r["status"] != "KEPT" and r["text"] not in base]
        L.append(f"- **R135-F [the frozen strings of the v22 close that R135 changed on top of the R134 close; `{js}`]** (recorded). Each string below was kept through the R134 close and occurs a different number of times after R135 "
                 "(a count of zero means the sentence left the text; where a sentence carries the claim now it is in reviews/v23/OLD_BESIDE_NEW_R135.md). Every one is authorized as changed by the pass under the entries above.")
        for r in changed:
            L.append(f"  - CHANGED [{r['tag']} {r['key']}] {r['base']} -> {r['new']}: \"{flat(quotable(r['text']))}\"")
    text = "\n".join(L) + "\n"
    BLOCK.write_text(text, encoding="utf-8", newline="\n")
    claims = CLAIMS.read_text(encoding="utf-8", errors="replace")
    crlf = "\r\n" in claims
    c = claims.replace("\r\n", "\n")
    i = c.index(HEAD133)
    m = re.search(r"^## (?!R133 AUTHORIZATION)", c[i + len(HEAD133):], flags=re.M)
    end = i + len(HEAD133) + m.start() if m else len(c)
    block = c[i:end]
    if HEAD135 in block:
        j = block.index("\n" + HEAD135)
        block = block[:j].rstrip("\n") + "\n" + text + ("\n" if m else "")
        what = "replaced"
    else:
        block = block.rstrip("\n") + "\n" + text + ("\n" if m else "")
        what = "inserted"
    c = c[:i] + block + c[end:]
    CLAIMS.write_bytes((c.replace("\n", "\r\n") if crlf else c).encode("utf-8"))
    print(f"-> {BLOCK} (units {units}; {len(changed) if js else 0} frozen strings quoted); CLAIMS.md R135 section {what} inside the R133 block")


if __name__ == "__main__":
    main()
