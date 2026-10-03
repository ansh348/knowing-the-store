# -*- coding: utf-8 -*-
"""claims_r137_block.py -- the R137 entries of CLAIMS.md (2026-09-22; the brief 'R137: LAND THE LONG-LIST CHECK, PLUS THE LAST TWO READABILITY ITEMS'), written
inside the R133 AUTHORIZATION BLOCK after the R135 section (one lineage, one base, one block). Written to reviews/v23/claims_r137_block.md and inserted at the
end of the R133 block (idempotent: an existing R137 section, from its 'Program R137' line to the next '## ' heading, is replaced). Entries: one per unit of
reviews/v23/tools/port_r137.py that has been applied (reviews/v23/results/port_r137_log.json), the gate interactions, and R137-F, which quotes every frozen
string of the v22 close that R137 changed on top of the R135 close (the strings not KEPT now that were KEPT in reviews/v23/results/frozen_r135_close.json).
Usage: python reviews/v23/tools/claims_r137_block.py [--json=reviews/v23/results/frozen_<tag>.json]
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
CLAIMS = SUB / "CLAIMS.md"
BLOCK = ROOT / "reviews" / "v23" / "claims_r137_block.md"
LOG = ROOT / "reviews" / "v23" / "results" / "port_r137_log.json"
HEAD133 = "## R133 AUTHORIZATION BLOCK — dated 2026-09-21"
HEAD137 = "Program R137 (2026-09-22), inside this block:"

ENTRIES = {
    "numbers": ("R137-NUMBERS [sections 2 and 3.1 of the brief: the pipeline, tab:robust row 9, the recount]",
                "cf_pad/tools/cfpad_tex.py writes the six Appendix C.2 tables (cf_pad/results/cfpad_tab_{sup,minus-lookup,whole,counted,other-lookups,position}.tex, four decimals) and cfpad_printed.json from cf_pad_scores.json; "
                "robust_tex.py row 9 reads cf_pad_scores.json: 'List padded to 60 names / Short, clean lists / Lookup $0.92$ to $0.74$; mini, Haiku, Opus fall with it; Luna, Sol lose $0.06$ to $0.07$, lead it by $0.13$ to $0.14$' (the comma form: the brief's 'Luna and Sol lose ... and lead' is the abstract's and 5.2's wording too, and repeat_scan bars a third place) "
                "(registered), the caption's per-row note naming the $88$ supersession triples, the $60$-name list and Opus at one draw against its recorded five-draw row; the 661-set padding and the wrong-name injection leave the row and stay "
                "in Appendix C.2's 'registered checks' paragraph and tab:pad. Section 4 reads '$33$ of $102$ came out otherwise' and Appendix F's count paragraph 'tab:registrations-e $9$ with $4$: $102$ predictions, $33$ of which' "
                "(AUX-R137-COUNT: 98 / 31 plus P-L1 to P-L4, P-L1 and P-L4 otherwise); tab:registrations-e's caption names the long-list check and its row follows the R125 rows (06c611f, day 43). Every number through r137_number_gate.py "
                "(R134's 62, R135's 37 and 77 of its own, 0 mismatches; reviews/NUMBERS_R137.md)."),
    "appendix": ("R137-APPENDIX [section 4 of the brief]",
                 "C.2: the 'registered checks' paragraph counts three and gains one sentence for the long-list check; after the paraphrase check the paragraph 'The long-list check' (the padding rule with the pool, seed, identical pad and "
                 "list lengths, the target's rank with the ledger's median $41.5$ where the brief wrote 41, the renderer lock, the leak scan, the frozen registration with both endpoints; the caps and spend; the four predictions with their "
                 "numbers; the six tables through the %%CFPAD-TABLE:<name>%% markers; the counted states' sentence; Opus 5's one draw against its recorded draw 1; the seed check; the run notes). A: tab:setup's row and tab:runs' caption "
                 "sentence. E.12: tab:provenance's row. F: the row's pointer to tab:cfpad-sup. E.11: the spend list. E.1: the notation box's 'padded list' row. Every value from cf_pad/results/cf_pad_scores.json "
                 "(cf_pad/NUMBERS_CF_PAD.md AUX-CFP-*; reviews/NUMBERS_R137.md AUX-R137-PRINTED)."),
    "main": ("R137-MAIN [sections 3.2, 3.4, 3.5 and 3.6 of the brief]",
             "5.2's lead reads 'On the named state, no model reliably beats the lookup on the short list; on a long one, two do.' and the long-list sentences close the opening paragraph (the brief's first placement; as their own paragraph they open with a numeral and trip q_scan Q-A): 'With the superseded-name list padded to $60$ names "
             "(Table~\\ref{tab:robust}), the lookup loses $0.18$ and mini, Haiku and Opus fall with it, ending level with it or below. Luna and Sol lose $0.06$ to $0.07$ and lead the lookup by a reliable $0.13$ to $0.14$ pooled and $0.09$ to $0.10$ "
             "within triples. Retraction and expiry do not move, since the list names neither. (Appendix~\\ref{app:counterfactual})' (the ledger over the brief's wording in two places, listed in REPORT_R137.md: Haiku loses $0.15$, less than the "
             "lookup's $0.18$, so 'as much or more' is not printed; the matched lead is $0.09$ to $0.10$, so 'on both metrics' prints both). Section 1's second bullet: 'when the list is short, including under a control that holds counts and "
             "list length fixed, and two of five do when it is padded to $60$ names; the lookup loses $0.02$ ...'. The Conclusion's sentence gains 'on the short list' and a second sentence 'On a $60$-name list Luna and Sol lead the lookup by "
             "$0.13$ to $0.14$ and the other three fall with it.' (its own sentence: the clause would take the sentence past rule L's 40 words). Limitations gains the brief's sentence verbatim."),
    "abstract": ("R137-ABSTRACT [section 3.3 of the brief]",
                 "The fifth sentence replaced by the brief's two, verbatim: 'Where the summary names the affected attribute and the list is short, none of five language models reliably beats a cosine-similarity lookup over the names, "
                 "including under a control that fixes counts and list length. Padded to $60$ names, the lookup loses $0.18$; GPT-5.6 Luna and Sol lose $0.06$ to $0.07$ and lead it by $0.13$ to $0.14$, while the other three fall with it.' "
                 "Numbers through r137_number_gate.py. No AUTHOR-RULING entry was needed (no prose rule fired inside it)."),
    "partb": ("R137-PARTB [section 5 of the brief: the two readability items and Table 1]",
              "5.1 Figure 1 is a rendered lifecycle summary in the old figure's footprint: the LIFECYCLE TOTALS block (active $377$, superseded $197$, retracted $1$, expired $49$), the HOBBIES_RECREATION name line and the superseded-names line "
              "of the summary the E.1 excerpt was cut from (frbank:david:FULL:BELIEVED, transcribed by port_r137.py from the artifact's manifest; AUX-R137-FIG1), labelled 'Summary route: read before retrieval', beside one returned record with its "
              "tag ('hiking_preference [superseded]', the store's own hiking_preference entry) labelled 'Tag route: read on returned records'; the brief's caption; the body sentence reads 'Figure~\\ref{fig:framework} shows one such summary, "
              "abridged, beside a returned record with its tag.' The old schematic and caption are in REPORT_R137.md. 5.2 the two thesis sentences rejoined to the paragraph they follow (the blank line removed; no rewording). 5.3 Table 1 gains "
              "'Luna & all' and 'Sol & all' rows of dashes and the note 'A dash marks a condition the model did not run.'"),
    "p1": ("R137-P1 [section 6 of the brief, payer P1]", "The retraction-and-expiry sentence moved from 5.2's opening paragraph to Table 2's caption ('In row 9 retraction and expiry do not move, since the list names neither.'); the fold is the main unit's placement already."),
    "p2": ("R137-P2 [payer P2]", "'The rewrites are also vaguer than the originals.' leaves the body (it stays in C.2 and tab:para-flags' caption)."),
    "p3": ("R137-P3 [payer P3]", "Section 8 points to Appendices A and E.8, Section 7 to E.10, G.4 and its tables: no pointer is repeated, nothing cut (asserted by port_r137.py)."),
    "p4": ("R137-P4 [payer P4]", "The builders box prints no number of Sections 5 to 6 beyond the Haiku $0.12$ clause the brief keeps: nothing cut."),
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
    L = ["", HEAD137 + " the long-list check landed, the prediction recount, the two readability items (the brief 'R137: LAND THE LONG-LIST CHECK, PLUS THE LAST TWO READABILITY ITEMS'; 2026-09-22; $0) on the R135 close bda70df "
         "(the run 6d7f224 under registrations/ADDENDUM_CF_PAD.md, frozen alone at 06c611f). The results pipeline is cf_pad/tools/cfpad_tex.py (the C.2 fragments) and reviews/v23/tools/robust_tex.py (tab:robust row 9), the number gate "
         "r137_number_gate.py (R134's 62 and R135's 37 checks and 77 of its own), the ledger reviews/NUMBERS_R137.md (ledger_r137.py), the edits port_r137.py (every edit asserted, on the regenerated R135 close), the gate edits "
         "gate_edits_r137.py, the pins pin_appendix_r137.py, the probe slack_r137.py, the report reviews/v23/REPORT_R137.md, the sign-off file reviews/v23/OLD_BESIDE_NEW_R137.md. v22 stays frozen. No model call.", ""]
    for u in units:
        title, text = ENTRIES[u]
        L.append(f"- **{title}** (recorded). {text}")
    L.append("- **R137-G [the gate interactions]** (recorded). reviews/v23/tools/build_v23.py splices the six CFPAD tables at their markers; run_gates.py runs r137_number_gate.py; number_moves_wp.py walks cf_pad/results/cf_pad_scores.json and "
             "cf_pad/build/lock.json and dispositions Figure 1's three transcribed totals and the median rank 41.5 (ADDED) and the old figure's tikz coordinate token (VANISHED); r134_number_gate.numerals() drops minipage widths and makebox lengths (layout, as the p{} column specs since R135); tools/trace_scan_v13.py LEDGERS gains cf_pad/NUMBERS_CF_PAD.md and reviews/NUMBERS_R137.md; r137_number_gate.py's built check allows the CFPAD "
             "fragments' numerals and the pass's printed forms. tools/prose_scan.py: no entry added (no prose rule fired on the abstract's own sentence); nothing exempted.")
    if js:
        rows = json.loads((ROOT / js).read_text(encoding="utf-8"))
        base = {r["text"] for r in json.loads((ROOT / "reviews" / "v23" / "results" / "frozen_r135_close.json").read_text(encoding="utf-8")) if r["status"] != "KEPT"}
        changed = [r for r in rows if r["status"] != "KEPT" and r["text"] not in base]
        L.append(f"- **R137-F [the frozen strings of the v22 close that R137 changed on top of the R135 close; `{js}`]** (recorded). Each string below was kept through the R135 close and occurs a different number of times after R137 "
                 "(a count of zero means the sentence left the text; where a sentence carries the claim now it is in reviews/v23/OLD_BESIDE_NEW_R137.md). Every one is authorized as changed by the pass under the entries above.")
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
    if HEAD137 in block:
        j = block.index("\n" + HEAD137)
        block = block[:j].rstrip("\n") + "\n" + text + ("\n" if m else "")
        what = "replaced"
    else:
        block = block.rstrip("\n") + "\n" + text + ("\n" if m else "")
        what = "inserted"
    c = c[:i] + block + c[end:]
    CLAIMS.write_bytes((c.replace("\n", "\r\n") if crlf else c).encode("utf-8"))
    print(f"-> {BLOCK} (units {units}; {len(changed) if js else 0} frozen strings quoted); CLAIMS.md R137 section {what} inside the R133 block")


if __name__ == "__main__":
    main()
