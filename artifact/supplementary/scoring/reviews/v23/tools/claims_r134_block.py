# -*- coding: utf-8 -*-
"""claims_r134_block.py -- the R134 entries of CLAIMS.md (program R134, the paraphrase check landed in v23; 2026-09-21), written inside the R133 AUTHORIZATION
BLOCK the way R128, R129 and R131 wrote theirs inside the R126 block (one lineage, one base, one block; frozen_diff --program=R133 reads the whole block).
Written to reviews/v23/claims_r134_block.md and inserted at the end of the R133 block (idempotent: an existing R134 section, from its 'Program R134' line to the
next '## ' heading, is replaced). Entries: one per unit of reviews/v23/tools/port_r134.py that has been applied (reviews/v23/results/port_r134_log.json), the
gate interactions, and R134-F, which quotes every frozen string of the v22 close that R134 changed on top of the R133 close (the UNAUTHORIZED rows of the
frozen_<tag>.json named by --json=, written by frozen_list_wp.py), so frozen_diff reads each as CHANGED-AUTHORIZED.
Usage: python reviews/v23/tools/claims_r134_block.py [--json=reviews/v23/results/frozen_<tag>.json]
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
CLAIMS = SUB / "CLAIMS.md"
BLOCK = ROOT / "reviews" / "v23" / "claims_r134_block.md"
LOG = ROOT / "reviews" / "v23" / "results" / "port_r134_log.json"
HEAD133 = "## R133 AUTHORIZATION BLOCK — dated 2026-09-21"
HEAD134 = "Program R134 (2026-09-21), inside this block:"

ENTRIES = {
    "appendix": ("R134-APPENDIX [section 5 of the brief: the appendix]",
                 "Appendix C.2 (the registration's 'Appendix D.2'; the pointer renders through the label): the 'Two registered checks' paragraph's pending sentence becomes one sentence and a pointer; after tab:pad the paragraph "
                 "'The paraphrase check' (the procedure: 148 questions, 24 failing the screen at drafting, 124 read, 9 excluded, 115 accepted with 76 / 17 / 22 by state, the floor amended from 120 before any scoring call, the 124 as a sensitivity; "
                 "the AI-assisted read disclosed with its agreement counts 5 of 5, 3 of 4, 1 of 12, 0 of 103; the six tables tab:para-pooled, tab:para-matched, tab:para-minus-lookup, tab:para-sup, tab:para-sens and tab:para-flags at four decimals "
                 "from cf2_paraphrase/results/para_tab_*.tex; the author's ruling on the branch stated under the supersession-only table (Luna the only reader above the lookup, the added reader, its matched interval including zero, "
                 "its pooled lower bounds 0.009 and 0.004, one of five comparisons with no multiplicity correction, Haiku's readings also disagreeing); the sensitivity sentence; the branch readings A, D and C, D; the genericity paragraph "
                 "(0.486 to 0.317; 0.484 to 0.000); the run notes). Appendix A: tab:setup's paraphrase row and tab:runs' caption sentence. E.12: tab:provenance's row. F: tab:registrations-c's caption, the row's outcome, the dated-notes row "
                 "(the whole file 2848f1ad, day 42); the prediction count unchanged. The AI-use statement: one sentence (an assistant pre-read the sheet and flagged rows; an author made every verdict). G.5: 'paraphrase approvals' dropped from the "
                 "dependency sentence (flag (b), agreed). Every number through r134_number_gate.py (reviews/NUMBERS_R134.md AUX-R134-PRINTED; cf2_paraphrase/NUMBERS_PARA.md AUX-PARA-*)."),
    "main": ("R134-MAIN [section 4 of the brief: the main text]",
             "Section 5.2 gains the paragraph 'The result survives rewording.' directly after the sibling-name control paragraph (section 4.1 of the brief, with the Branch B sentences of the author's RULING 2: "
             "'On the named state, reworded, mini and Haiku sit reliably below the lookup on the pooled metric (by $0.12$ and $0.07$), and Opus and Sol do not differ from it. Luna, a reader we added after fixing the design, "
             "edges above it by $0.04$, reliable on the pooled metric and not within triples; on the original questions no model exceeded it.'); Section 1's second contribution gains ', and the lookup loses $0.02$ when the questions "
             "are reworded to share no word with the names' (4.4); the Limitations sentence 'The paraphrase check is not yet scored.' is replaced by 'The paraphrase check covers $115$ of the $148$ questions, its rewrites are vaguer than "
             "the originals, and Opus ran it with one draw.' with 'GPT-4.1 mini drafted the questions and is also a reader; it is the weakest reader.' beside it (4.5); the Conclusion gains RULING 2's numeral-free sentence "
             "'When the questions are reworded, the lookup holds up at least as well as the smaller models, and only one stronger model edges past it on a named state.' (4.6). Every number from cf2_paraphrase/results/para_printed.json "
             "through r134_number_gate.py; no gate rewords a ruled sentence."),
    "main_short": ("R134-MAIN-SHORT [section 4.2 of the brief]", "The shorter Section 5.2 paragraph in place of 4.1's, applied because the page gate failed with the longer one."),
    "abstract": ("R134-ABSTRACT [the author's abstract, verbatim]",
                 "The whole abstract replaced by the author's text of 2026-09-21 (the ruling superseding the brief's section 4.3), numerals in math mode as the source's convention, no other change; the sentence "
                 "'Under a control that holds counts and list length fixed, the lookup and every model pick the correct name over a similar one at an AUROC of $0.88$ or higher (chance $0.50$).' leaves the abstract "
                 "(its numbers still print in Section 5.2; NUMBER_MOVES_V23.md); the placeholder 'human validation is pending' stays. Numbers through r134_number_gate.py. No gate rewords it."),
    "payers": ("R134-PAYERS [the author's RULING 3 of 2026-09-21: the payers for Part B's page]",
               "P1: Section 4's coverage sentence reads 'Appendix A lists both.'; the five daggers leave the main text (5.1 twice, 5.2, 5.3, Section 8); Appendix A's notes stay, headed 'Coverage notes for the main text.' with a first sentence that no longer refers to a dagger. "
               "P2: the adaptive-retrieval citation string keeps Lewis et al. 2020, Jiang et al. 2023, Mallen et al. 2023, Asai et al. 2024 and Su et al. 2024 and drops the other five (ren2025, wang2023, seakr, verbrouting, metamem); no other citation touched; the five entries stay in the bibliography, uncited (listed for the sweep). "
               "P3: the Introduction's two metamemory sentences become 'In metamemory terms these are negative-obligation knowledge (NOK) and the feeling of knowing (FOK) (Hart, 1965; Nelson & Narens, 1990; Koriat, 1993), here judged about an external store.' "
               "P4: the Conclusion's first paragraph keeps its first sentence and reads, after it, 'On a named state no model reliably exceeds the name lookup, with list length kept fixed or not, and when the questions are reworded only one stronger model edges past it. "
               "The stronger models' lead comes from counts the smaller models do not use. Told the intent rule, only the stronger models apply it, and a fixed cue list matches the best of them.' (RULING 2's Conclusion sentence is superseded by this). "
               "P5: the second contribution bullet reads 'Evidence about what readers read. On the named state no model reliably exceeds a name lookup, including under a control that holds counts and list length fixed, and the lookup loses $0.02$ when the questions are reworded to share no word with the names. "
               "The stronger models' lead comes from the counts, which the two smaller models do not use.' The 5.1 check: the three stronger models' matched moved-count falls on the counted states are Opus 5 -0.2833, GPT-5.6 Luna -0.2917, GPT-5.6 Sol -0.3250 (tab:cf-matched-ablations; AUX-CF2-R125-CONTRASTS), "
               "so 'falling by $0.27$ to $0.33$' reads 'falling by $0.28$ to $0.33$' through r134_number_gate.py (the 0.27 was Luna's expiry value, a per-state row). B4 follow-up: repro_amem_links.py copied to ARTIFACT/verifier/ and listed for the 24 September sweep."),
    "partb": ("R134-PARTB [section 6 of the brief: the four agreed items]",
              "B1: Table 1's given-category count reader carries a mark and the note explains, from C.2, that the two count readers read different quantities (the given-category reader ties every supersession triple and is perfect on the "
              "counted states by construction; the guessed-category reader's share includes the superseded column). B2: Setup names the release's personas once, 'the FR-Bank release (its LifecycleBench personas)'. B3: a three-pair term bridge "
              "at the top of Appendix E.1's glossary; the AI-use statement's sentence on the intent crossover's AI-assisted check (the author's addition to step 6), from the registration's disclosure line, beside the paraphrase sentence. B4: report only; the artifact-named repro_amem_links.py reproduces the census row from the frozen banks of our integration and does not exercise the stock package outside it, so Table 2's cell is unchanged. "
              "Table 1's note is the one-line form (the three-line form cost the page; gates_r134_partb_a.txt)."),
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
    L = ["", HEAD134 + " the paraphrase check (registrations/ADDENDUM_PARA.md, registered text sha256 45cad63d; scored 2026-09-21, commit 4f1484a; the post hoc supersession-only table e650dd5) landed in v23 on the R133 close "
         "by the author's brief 'R134: LAND THE PARAPHRASE CHECK IN v23' and the rulings of the same day (Branch B by the pre-stated rule, worded in both directions; RULING 2: no whitelisting of the ruled texts, the texts replaced). "
         "The results pipeline is cf2_paraphrase/tools/para_tex.py (the six tables and the printed forms), the number gate reviews/v23/tools/r134_number_gate.py, the ledger reviews/NUMBERS_R134.md (ledger_r134.py), the edits "
         "reviews/v23/tools/port_r134.py (every edit asserted, on the regenerated R133 close), the pins pin_appendix_r134.py, the report reviews/v23/REPORT_R134.md, the sign-off file reviews/v23/OLD_BESIDE_NEW_R134.md. "
         "v22 stays frozen. No model call.", ""]
    for u in units:
        title, text = ENTRIES[u]
        L.append(f"- **{title}** (recorded). {text}")
    L.append("- **R134-G [the gate interactions]** (recorded). tools/slogan_scan.py: the stale EXEMPT_S9 entry for the R133 abstract sentence that left with the author's abstract ('but not when all items are pooled') retired; "
             "tools/prose_scan.py: no entry for any ruled text of RULING 2 (the texts were replaced instead); two AUTHOR-RULING entries for the author's abstract only, as RULING 2 allows (gate_edits_r134.py; listed in REPORT_R134.md): its sibling-control sentence ('... even with counts and list length held fixed.'; rule V, 'held') and its count-feature sentence ('The stronger models' lead over the lookup of $0.08$ to $0.10$ ...'; rule L at 48 words; rule D, a 73% token overlap with Section 5.2's lead 'The stronger models' lead comes from counts, and a count feature closes it within a question.'). "
             "tools/trace_scan_v13.py LEDGERS gains cf2_paraphrase/NUMBERS_PARA.md and reviews/NUMBERS_R134.md; reviews/v23/tools/number_moves_wp.py walks the PARA artifacts; run_gates.py runs r134_number_gate.py --built; build_v23.py splices the six tables at the per-table markers.")
    if js:
        rows = json.loads((ROOT / js).read_text(encoding="utf-8"))
        # R134's strings = every string not KEPT now that was KEPT at the R133 close (reviews/v23/results/frozen_r133_rulings_b.json), whatever its current
        # authorization status (a string quoted by an earlier run of this tool reads AUTHORIZED afterwards and must stay quoted)
        r133 = {r["text"] for r in json.loads((ROOT / "reviews" / "v23" / "results" / "frozen_r133_rulings_b.json").read_text(encoding="utf-8")) if r["status"] != "KEPT"}
        changed = [r for r in rows if r["status"] != "KEPT" and r["text"] not in r133]
        L.append(f"- **R134-F [the frozen strings of the v22 close that R134 changed on top of the R133 close; `{js}`]** (recorded). Each string below occurred in paper_v22.tex, was kept by the R133 close and occurs a different number of times after R134 "
                 "(a count of zero means the sentence left the text; the sentence carrying the claim now, where one does, is in reviews/v23/OLD_BESIDE_NEW_R134.md). Every one is authorized as changed by the pass under the entries above.")
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
    if HEAD134 in block:
        j = block.index("\n" + HEAD134)
        block = block[:j].rstrip("\n") + "\n" + text + ("\n" if m else "")
        what = "replaced"
    else:
        block = block.rstrip("\n") + "\n" + text + ("\n" if m else "")
        what = "inserted"
    c = c[:i] + block + c[end:]
    CLAIMS.write_bytes((c.replace("\n", "\r\n") if crlf else c).encode("utf-8"))
    n = len(changed) if js else 0
    print(f"-> {BLOCK} (units {units}; {n} frozen strings quoted); CLAIMS.md R134 section {what} inside the R133 block")


if __name__ == "__main__":
    main()
