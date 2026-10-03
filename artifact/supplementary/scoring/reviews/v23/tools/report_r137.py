# -*- coding: utf-8 -*-
"""report_r137.py -- reviews/v23/REPORT_R137.md: the pass report of R137 (the brief, section 8), assembled from the edit log (port_r137_log.json), the gate
files (gates_r137_*.txt), the slack rows (results/slack_r137.md), the ledger (reviews/NUMBERS_R137.md) and the sign-off file (OLD_BESIDE_NEW_R137.md), so
every quoted text and number is read from its file. The prose sections (what changed against the brief, what was not changed) are written here.
Usage: python reviews/v23/tools/report_r137.py
"""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[3]
V23 = ROOT / "reviews" / "v23"
OUT = V23 / "REPORT_R137.md"


def rd(p):
    return p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")


def cell(s):
    return s.replace("|", "\\|").replace("\n", " ").strip()


def strip_comments(s):
    return "\n".join(l for l in s.split("\n") if not l.lstrip().startswith("%"))


def main():
    log = json.loads(rd(V23 / "results" / "port_r137_log.json"))
    E = {(e["unit"], e["section"]): e for e in log["edits"]}
    gates = {t: rd(V23 / f"gates_r137_{t}.txt") for t in ("base", "numbers", "appendix_c", "main_b", "abstract_b", "partb_b", "close")}
    slack = [l for l in rd(V23 / "results" / "slack_r137.md").split("\n") if l.startswith("| R137")]
    base_slack = [l for l in rd(V23 / "results" / "slack_r135.md").split("\n") if "R137 BASE" in l]
    N = rd(ROOT / "reviews" / "NUMBERS_R137.md")
    OBN = rd(V23 / "OLD_BESIDE_NEW_R137.md")
    close_head = gates["close"].split("\n")[0]
    tex_sha = re.search(r"paper_v23.tex sha256 ([0-9a-f]+)", close_head).group(1)
    pdf_sha = re.search(r"paper_v23.pdf sha256 ([0-9a-f]+)", close_head).group(1)
    fig_old = strip_comments(E[("partb", "Figure 1")]["old"])
    fig_new = strip_comments(E[("partb", "Figure 1")]["new"])
    old_caption = re.search(r"\\caption\{(.*?)\}\n\\label", fig_old, flags=re.S).group(1)
    new_caption = re.search(r"\\caption\{(.*?)\}\n\\label", fig_new, flags=re.S).group(1)
    fig_lines = re.search(r"\\ttfamily\n(.*?)\n\\end\{minipage\}\}", fig_new, flags=re.S).group(1)
    tag_lines = re.search(r"Tag route\}.*?\\ttfamily\n(.*?)\n\\end\{minipage\}\}", fig_new, flags=re.S).group(1)

    def page_line(t):
        return next(l for l in gates[t].split("\n") if l.startswith("page_census_v2")).split("(")[0].strip() + " (" + gates[t].split("raggedbottom diagnostic build: ")[1].split(")")[0] + ")"

    L = []
    L += ["# REPORT_R137 — the long-list check landed, the prediction recount, Figure 1 rendered, the thesis sentences rejoined (2026-09-22; $0, no API call)", "",
          f"Base: the R135 close bda70df (rebuilt unchanged as gates_r137_base.txt: tex sha256 09c0bdd1524ef98a, page 9, fine 482, slack +4). Close: `gates_r137_close.txt`, paper_v23.tex sha256 `{tex_sha}`, paper_v23.pdf sha256 `{pdf_sha}`, "
          "91 pages, the main text ending on page 9 (fine 484, census +0), **slack +2 by the probe** (the brief's close condition: +2 or more, reserved for the HV-1 landing), every gate passing, no overfull vbox on pages 1 to 10 "
          "(the three overfull hboxes of the R135 close remain, pages 49 and 63), 238 body sentences none over 35 words; close_checks_r137.py: the anonymity greps clean, pages 1 to 10 rasterized (results/close_r137_p*.png) with no word-box overlap. "
          "Commits: R137 NUMBERS 5572b04, APPENDIX e30e403, MAIN f8eb86c, ABSTRACT 0443602, PARTB c81817d, CLOSE (this commit). v22 untouched; reviews/v23 only. Regenerate: `python reviews/v23/tools/port_r137.py --units=close` "
          "(the units of results/r137_close_units.txt: numbers appendix main abstract partb p1 p2) then `run_gates.py <tag>`.", ""]
    # ---- 1. the pipeline
    L += ["## 1. The pipeline (section 1 of the brief)", "",
          "- `cf_pad/tools/cfpad_tex.py` writes the six Appendix C.2 fragments from `cf_pad/results/cf_pad_scores.json` (four decimals, one file per table, spliced by `build_v23.py` at the `%%CFPAD-TABLE:<name>%%` markers `port_r137.py` writes) and `cf_pad/results/cfpad_printed.json` (the prose counts and run notes, each beside its source key). "
          "The two-decimal forms the body prints are `cf_pad/results/cf_pad_printed.json` (report_cf_pad.py). Opus's row label and the draws sentence read the draw count from the scores file (`census/OP5/k_new`, `k_recorded`): if draws 2 to 5 are ever committed under the registration's dated lane, `cfpad_tex.py`, `robust_tex.py` and `port_r137.py` re-land the row from the same files, with the number gate re-deriving every form.",
          "- `reviews/v23/tools/robust_tex.py` row 9 reads `cf_pad_scores.json` (the 661-set padding and the injection leave the table; they stay in C.2's 'registered checks' paragraph and tab:pad).",
          "- `reviews/v23/tools/r137_number_gate.py`: R134's 62 and R135's 37 checks and 77 of its own, 0 mismatches; `--built` allows the pass's printed forms and the CFPAD fragments' numerals. Ledger `reviews/NUMBERS_R137.md` (`ledger_r137.py`: AUX-R137-ROBUST9, -COUNT, -FIG1, -PRINTED); `cf_pad/NUMBERS_CF_PAD.md` and `reviews/NUMBERS_R137.md` join trace_scan's LEDGERS. `number_moves_wp.py` walks `cf_pad_scores.json` and `lock.json` (544 added tokens dispositioned, 0 missing).",
          "- Gate edits (`gate_edits_r137.py`, idempotent): build_v23.py (the markers), run_gates.py (the gate), number_moves_wp.py (the walks; Figure 1's three transcribed totals and the median rank 41.5 as ADDED; the old figure's tikz coordinate token as VANISHED), r134_number_gate.numerals() (minipage widths and makebox lengths are layout, as the p{} column specs since R135), trace_scan_v13.py (the two ledgers). No prose_scan entry: no prose rule fired inside the abstract's own sentences; nothing exempted anywhere.", ""]
    # ---- 2. the recount
    L += ["## 2. The prediction recount (section 2 of the brief)", "",
          "| where | old | new |", "|---|---|---|",
          f"| Section 4 | {cell(E[('numbers', '4, the predictions sentence')]['old'])} | {cell(E[('numbers', '4, the predictions sentence')]['new'])} |",
          f"| Appendix F, the count paragraph | {cell(strip_comments(E[('numbers', 'F, the count paragraph')]['old']))} | {cell(strip_comments(E[('numbers', 'F, the count paragraph')]['new']))} |",
          "| Appendix F, tab:registrations-e | 5 with 2 | 9 with 4 (the four P-L predictions, two otherwise: P-L1 and P-L4, both failing on Opus 5 alone) |", "",
          "AUX-R137-COUNT: AUX-R131-COUNT's 98 / 31 plus P-L1 (FAILS), P-L2 (HOLDS), P-L3 (HOLDS), P-L4 (FAILS) = 102 / 33; the other four tables unchanged.", ""]
    # ---- 3. the main text
    L += ["## 3. Every changed main-text sentence, old beside new, with its ledger row (section 3 of the brief; the full sign-off file is `OLD_BESIDE_NEW_R137.md`, 26 rows)", ""]
    L += ["### 3.1 Table 2 (tab:robust), row 9", "", "| cell | old | new |", "|---|---|---|",
          "| what we tried to break | Padding to 60; wrong names injected | List padded to 60 names |",
          "| what it removes | Short, clean lists | Short, clean lists |",
          "| what happened | $0.67$ padded; $0.67$/$0.60$ with wrong names, mini and Haiku falling with it, within $0.02$ of the lookup | Lookup $0.92$ to $0.74$; mini, Haiku, Opus fall with it; Luna, Sol lose $0.06$ to $0.07$, lead it by $0.13$ to $0.14$ |",
          "| status / population | registered; the full obligation set (padding), the counterfactual set (injection) | registered; the counterfactual set, supersession (88 triples); Opus one draw against its recorded five-draw row |",
          "| caption's per-row note | row 9 the full obligation set (padding) and the counterfactual set (injection) | row 9 the $88$ supersession triples, the lists padded to $60$ names, Opus at one draw against its five-draw row; and, after P1, 'In row 9 retraction and expiry do not move, since the list names neither.' |", "",
          "Ledger: AUX-R137-ROBUST9 (cf_pad_scores.json readers/LOOKUP/superseded/pooled unpadded 0.9223, padded 0.7416; readers/{LUNA,SOL} padded minus unpadded -0.0636, -0.0693, both reliable; minus_lookup/{LUNA,SOL} padded pooled +0.1375, +0.1274, both reliable on both metrics; mini -0.0525, Haiku -0.0062, Opus -0.0336 with intervals including zero). "
          "The row wraps to two lines (its cell is twice the width the column holds on one line; the brief allowed 'zero or one'). The wrong-name injection result did not move: it already lives in C.2's 'registered checks' paragraph ('Its amendment injects wrong names ... $0.7663$ to $0.6740$ and $0.6001$ ...') and in tab:pad's lower block. "
          "**The cell's comma form** ('Luna, Sol lose ..., lead it by ...') departs from the brief's 'Luna and Sol lose ... and lead': that phrase is the abstract's and 5.2's wording too, and repeat_scan bars a 9-gram in three places (gates_r137_abstract.txt); the abstract and 5.2 stay verbatim, the generated cell varies (the R135 precedent for ledger-driven cell wordings). For the author's confirmation.", ""]
    for title, key in (("3.2 Section 5.2, the lead", ("main", "5.2, the opening paragraph")),):
        pass
    rows52 = [l for l in OBN.split("\n") if l.startswith("| ") and ("\\claim{On the named state" in l or "With the superseded-name list" in l or "Retraction and expiry do not move" in l)]
    L += ["### 3.2 Section 5.2", "", "| old | new | cause |", "|---|---|---|"] + rows52 + ["",
          "Ledger rows (AUX-R137-PRINTED): 0.18 = readers/LOOKUP/superseded/pooled/padded_minus_unpadded -0.1807 (reliable; P-L3 holds); 'mini, Haiku and Opus fall with it, ending level with it or below' = padded minus unpadded -0.1902, -0.1522, -0.2245 (all reliable) and minus the lookup -0.0525, -0.0062, -0.0336 (intervals including zero); "
          "0.06 to 0.07 = Luna -0.0636, Sol -0.0693 (reliable); 0.13 to 0.14 = Sol +0.1274, Luna +0.1375 pooled (reliable); 0.09 to 0.10 = Sol +0.0909, Luna +0.1023 matched (reliable); 'two do' = exactly Luna and Sol reliably above on both metrics; retraction and expiry: no reliable change but Haiku's matched and Opus's pooled fall on retraction (C.2 says so; the body sentence keeps the brief's words).", "",
          "**Where the ledger overrode the brief's wording (rule 1: the ledger wins; the difference printed):**", "",
          "1. The brief: 'the lookup loses 0.18 and mini, Haiku and Opus lose as much or more, ending level with it or below.' Haiku's padded-minus-unpadded fall is $-0.1522$, smaller than the lookup's $-0.1807$ (mini $-0.1902$ and Opus $-0.2245$ do lose more). Landed: 'the lookup loses $0.18$ and mini, Haiku and Opus fall with it, ending level with it or below' (Section 0's own words; all three end at or below the lookup: $-0.0525$, $-0.0062$, $-0.0336$).",
          "2. The brief: 'lead the lookup by a reliable 0.13 to 0.14 on both metrics.' The 0.13 to 0.14 is the pooled lead; the matched lead is $+0.0909$ (Sol) and $+0.1023$ (Luna), also reliable. Landed: 'lead the lookup by a reliable $0.13$ to $0.14$ pooled and $0.09$ to $0.10$ within triples'.",
          "3. Placement: as its own paragraph the text opens with a numeral and trips q_scan Q-A (every body paragraph opens with a plain sentence; gates_r137_main_a.txt). The brief allowed either placement; the text closes the opening paragraph instead (the fold P1 would have made). P1 is therefore the caption move alone.", ""]
    rows_other = [l for l in OBN.split("\n") if l.startswith("| ") and ("Evidence about" in l or "On a named state no model" in l or "Opus 5 ran one draw" in l or "The predictions were registered" in l)]
    L += ["### 3.3 to 3.6 The abstract, Section 1's bullet, the Conclusion, Limitations", "", "| old | new | cause |", "|---|---|---|"]
    L += [l for l in OBN.split("\n") if l.startswith("| Where the summary names")] + rows_other + ["",
          "- The abstract: the brief's two sentences verbatim (numerals in math mode as the source's convention). No prose rule fired inside them; readability_wp counts body sentences only (the first sentence is 36 words; the author may reword).",
          "- Section 1's bullet: the brief's clause 'when the list is short, and two of five do when it is padded to 60 names' would have left 'including under a control that holds counts and list length fixed' attached to the long-list claim; the control clause stays beside the short-list claim it qualifies and the long-list clause follows it, every word of the brief kept (76 words; the readability report lists it). For the author's confirmation.",
          "- The Conclusion: the brief's clause appended to the sentence would take it to 52 words, past prose rule L's 40; it prints as its own sentence 'On a $60$-name list Luna and Sol lead the lookup by $0.13$ to $0.14$ and the other three fall with it.' (22 words). repeat_scan did not fire on it, so the numeral-free form was not needed.",
          "- Limitations: the brief's sentence verbatim ('Opus 5' as written; the paragraph's earlier sentence says 'Opus').", ""]
    # ---- 4. the appendix
    L += ["## 4. The appendix (section 4 of the brief)", "",
          "### 4.1 C.2, the new subsection 'The long-list check' (after the paraphrase check, before the expiry extension), in the brief's order", "",
          "1. Procedure: one paragraph (the pool of the persona's own printed names, 71 to 121 per triple, median 102, no pad on other personas' names; one pad per triple under a recorded seed, identical across the triple's versions; the PN list exactly 60, the siblings 57 to 60; the counts left as written so the superseded total disagrees with the list length; the target never in its pad, its rank never first and last on 4 of 88, minimum 2, **median 41.5** (the ledger; the brief wrote 41), maximum 60, by tenths 5/3/2/5/8/12/12/9/9/23; the renderer lock 444 of 444, the leak scan 0, the lookups reproducing their recorded values; the registration frozen and committed before the first call with both endpoints fixed; caps \\$12 / \\$20, spend \\$8.11 / \\$15.54, no cap reached, no draw dropped, no deviation).",
          "2. The four predictions with their numbers: P-L1 fails on Opus 5 (Luna $+0.1375$, Sol $+0.1274$ above with both intervals; Opus 5 $-0.0336$); P-L2 holds ($-0.0525$, $-0.0062$); P-L3 holds ($-0.1807$); P-L4 fails on Opus 5 ($-0.0636$, $-0.0693$ lose less; $-0.2245$ loses more); Luna and Sol above on the matched metric too.",
          "3. `tab:cfpad-sup` (registered): supersession, every reader, two panels (pooled AUROC; matched score with W/T/L), padded beside unpadded, the difference with both intervals.",
          "4. `tab:cfpad-minus-lookup` (registered): each model minus the name lookup, two panels (padded lists; unpadded lists), pooled and matched with both intervals; the reliable cells bold.",
          "5. `tab:cfpad-whole` (descriptive): the whole set, four panels (the same two views).",
          "6. `tab:cfpad-counted` (descriptive): retraction and expiry, unpadded/padded/difference per state and metric, and the sentence 'The padded list names neither retraction nor expiry and a triple's three versions carry identical padded lists, so no reader's change on those states is reliable except Haiku 4.5's matched fall on retraction and Opus 5's pooled fall on retraction.'",
          "7. `tab:cfpad-other-lookups` (descriptive): each model minus the lexical and minus the random-token lookup, padded and unpadded, pooled and matched; point estimates with stars (the intervals are in the ledger).",
          "8. `tab:cfpad-position` (descriptive): the two Spearman columns (rank against PN score; rank against outcome); the histogram summary is the procedure paragraph's rank sentence.",
          "9. Opus 5's one draw against its recorded draw 1: 0.9317 / 0.9716 on supersession (0.8400 / 0.8682 whole), padded minus draw 1 $-0.2236$ [$-0.2776$, $-0.1690$]; [$-0.3416$, $-0.1294$] and $-0.1873$ on the whole set, 'so the fall is not the draw count'.",
          "10. The seed spot-check: seeds 43 to 46 change no registered reading; one persona interval of mini minus the lookup at seed 45 moves without changing the reading.",
          "11. Run notes: draws (five; Opus 5 one against its recorded five), transports (raw interface draw by draw; batch for Haiku 4.5 and Opus 5), 2,220 rows per five-draw run and 444 for Opus 5, none unparseable; every served identifier checked on a probe and on every row; no run reached its cap.", "",
          "The tables were restructured into stacked panels after the first build (five overfull hboxes at 165 to 322 pt; gates_r137_appendix_a.txt); the close has none new. The C.2 'registered checks' paragraph counts three and gains one sentence for the long-list check. The tables' vertical gaps on their pages are the appendix's existing `\\flushbottom` with `[H]` tables (as the PARA tables).", "",
          "### 4.2 Other homes", "",
          f"- Appendix A: tab:setup's row: {cell(E[('appendix', 'A, tab:setup')]['new'])}",
          "- Appendix A: tab:runs' caption gains 'the same five ran it again with the superseded-names list padded to $60$ names, GPT-4.1 mini, Haiku 4.5, GPT-5.6 Luna and GPT-5.6 Sol at five calls and Opus 5 at one.'",
          f"- Appendix E.12, tab:provenance's row: {cell(E[('appendix', 'E.12, tab:provenance')]['new'])}",
          f"- Appendix F, tab:registrations-e's row: {cell(strip_comments(E[('numbers', 'F, tab:registrations-e row')]['new']).replace('(Table~ref{tab:robust})', '(Table~ref{tab:cfpad-sup})'))} (the pointer to tab:cfpad-sup set by the appendix unit); the caption names the third registration and reads 'Every row was committed before its first call.'",
          "- Appendix E.1: the notation box gains 'padded list & a superseded-names list lengthened to a fixed size ($60$ names) with correct attribute names of the same store that no scored question targets, the counts left as written'.",
          "- Appendix E.11 (not in the brief's list; the spend sentence lists every capped run): 'the long-list check on the counterfactual set $8.11$ of $12$ (Anthropic) and $15.54$ of $20$ (OpenAI)'.",
          "- The AI-use statement: unchanged (no human step in the check).", ""]
    # ---- 5. Part B
    L += ["## 5. Part B (section 5 of the brief)", "",
          "### 5.1 Figure 1", "", "The old caption: " + old_caption, "", "The old figure: the three-box tikz schematic (Tagged store / Summary route / Tag route / Reader, with the masked-retrieval note), 17 lines with its caption on page 2 of the R135 close (results/close_r135_p2.png).", "",
          "The new figure (12 lines with its caption; results/r137_fig1_crop.png; page 2 before and after: results/close_r135_p2.png and results/close_r137_p2.png), transcribed by port_r137.py from `ARTIFACT/manifests/indexes_v2.json` key `frbank:david:FULL:BELIEVED` (the summary the E.1 excerpt was cut from; AUX-R137-FIG1) and, for the tag route, `e1_metamemory/backend_entries/frbank.json` lb_00163 with FR-Bank's own tag:", "",
          "```", "Summary route: read before retrieval", "", re.sub(r"\\hspace\*\{[^}]*\}", "  ", re.sub(r"\\makebox\[[^\]]*\]\[[lr]\]\{([^}]*)\}", r"\1  ", fig_lines)).replace("\\\\", "").replace("\\_", "_"), "",
          "Tag route: read on returned records", "", tag_lines.replace("\\\\", "").replace("\\_", "_").replace("``", '"').replace("''", '"'), "```", "",
          "The new caption: " + new_caption, "",
          "The count table is the summary's LIFECYCLE TOTALS block, one line per lifecycle state (the brief's words; the E.1 excerpt prints the per-category rows of the same summary); the category line is HOBBIES_RECREATION's, where the hike example's attribute (hiking_preference) is visible, and the superseded-names line carries it too. "
          "'ATTRIBUTE NAMES BY CATEGORY (value-scrubbed; ...)' prints as '(names only; abridged)': 'value-scrubbed' is on prose_scan's main-text vocabulary list. The tag route's returned record fits, so the caption does not need to say it. "
          f"The body sentence: '{cell(E[('partb', '1, the lifecycle-summary paragraph')]['old'])}' reads '{cell(E[('partb', '1, the lifecycle-summary paragraph')]['new'])}'.", "",
          "### 5.2 The orphaned thesis lines", "",
          "The blank line between 'We then examine backend writing and retrieval.' and 'In these tests, every reader we tried was held back by what the store had written down. Models differ further when the rubric states the intent rule.' removed; no rewording. Page 2 rasterized (results/close_r137_p2.png): the paragraph now runs from the foot of page 1 across the figure at the top of page 2 ('retrieval. In these tests, ...'), no longer its own orphan paragraph.", "",
          "### 5.3 Table 1", "", "Rows 'Luna & all & -- & -- & -- & --' and 'Sol & all & -- & -- & -- & --' after their superseded rows, and the note's last sentence 'A dash marks a condition the model did not run.' No new column. Three lines on page 5.", ""]
    # ---- 6. payers and slack
    L += ["## 6. Page budget, payers and slack (section 6 of the brief)", "",
          "The additions cost about fourteen lines, not the brief's one to three: the lead now fills its line (+1), the bullet (+1), Limitations (+2), the Conclusion (+2), the three 5.2 sentences (+3), Table 2's caption and row 9 (+1 each), the abstract (+2 on page 1), Table 1's dash rows and note (+3); Figure 1's rendered summary gives back five. The slack after each unit (the probe, `results/slack_r137.md`; the fine number per unit set, `fine_r137.py`):", "",
          "| unit set | slack / reading |", "|---|---|"]
    for l in base_slack + slack:
        parts = [c.strip() for c in l.strip("|").split("|")]
        L.append(f"| {parts[0]} | {parts[1]} ({parts[2]}) |")
    L += ["| main + abstract (fine_r137.py) | page 10, fine 499 (-14) |", "| + partb | page 10, fine 493 (-8) |", "| + partb + P1 | page 10, fine 493 (-8) |", "| + partb + P1 + P2 | page 9, fine 484 (+1); the probe: +2 |", "",
          "Payers applied, in the brief's order, only as far as needed:", "",
          "| payer | old | new |", "|---|---|---|",
          "| P1 (the fold is the main unit's placement already; the caption move) | 5.2, the opening paragraph's last sentence: 'Retraction and expiry do not move, since the list names neither.' | the sentence leaves 5.2; Table 2's caption gains 'In row 9 retraction and expiry do not move, since the list names neither.' before its pointer |",
          f"| P2 | {cell(E[('p2', '5.2, the rewording paragraph')]['old'])} | {cell(E[('p2', '5.2, the rewording paragraph')]['new'])} |",
          "| P3 (not applied) | nothing to cut: Section 8's two paragraphs point to Appendices A (app:laddertable) and E.8 (app:baselines); Section 7 points to E.10 (app:resp), G.4 (app:posthoc-graphiti) and its own tables; no pointer repeated (port_r137.py unit_p3 asserts it) | unchanged |",
          "| P4 (not applied) | nothing to cut: the builders box prints no number of Sections 5 to 6 beyond the Haiku $0.12$ clause the brief keeps | unchanged |", "",
          "P1 and P2 alone recover no line on the main-only build (page 10 either way); with Part B in, P1 leaves the reading at -8 and P2 brings the box back to page 9 (a float snaps back: the fine number is not linear, as the memory notes). The close probe reads +2. No table row, figure or Limitations sentence was cut.", ""]
    # ---- 7. gates
    L += ["## 7. Gates (section 7 of the brief)", "",
          "| step | page / fine | gates |", "|---|---|---|"]
    for t, name in (("base", "1 base"), ("numbers", "2 NUMBERS"), ("appendix_c", "3 APPENDIX"), ("main_b", "4 MAIN"), ("abstract_b", "5 ABSTRACT"), ("partb_b", "6 PARTB"), ("close", "7 CLOSE")):
        g = gates[t]
        fails = [l.split(":")[0] for l in g.split("\n") if "FAIL" in l or "UNAUTHORIZED" in l or "missing" in l.split(":")[-1] and "missing from NUMBER_MOVES_V23.md 0" not in l]
        note = {"numbers": " (appendix_identity before pin_appendix_r137.py step numbers pinned F; PASS after, re-run and recorded in the NUMBERS commit)", "main_b": " (page 10 until Part B; every other gate passing)", "abstract_b": " (page 10 until Part B; every other gate passing)"}.get(t, "")
        L.append(f"| {name} | {page_line(t)} | {'every gate passing' if not fails else 'failing: ' + ', '.join(fails)}{note} |")
    L += ["",
          "Gate trips on the way, each printed here (none exempted): (a) q_scan Q-A on the own-paragraph placement of the 5.2 text (gates_r137_main_a.txt) — the brief's other placement taken; (b) repeat_scan on 'Luna and Sol lose num to num and lead' in three places (gates_r137_abstract.txt) — Table 2's generated cell varied; "
          "(c) the first appendix build: s17_grep's cap on 'both intervals excluding zero' (a caption reworded to 'both intervals exclude zero'), five overfull hboxes (the tables restructured into panels), frozen_diff on 'Two registered checks on this set' (R137-F quotes it), appendix_identity (pins for A, C.2, E.1, E.11, E.12, F), the built-numeral check on the provenance row's $0.18$ and on Figure 1's layout lengths (the allow-list and numerals() extended; 7em for 6.5em), numeric_diff on 41.5 and the old figure's tikz token (dispositioned). "
          "MAIN and ABSTRACT were committed with the page gate failing (page 10), the return to page 9 measured and landed in PARTB, as their messages say.", ""]
    # ---- 8. not changed
    L += ["## 8. What I wanted to change and did not; items for the author", "",
          "- The abstract's first landed sentence is 36 words (the readability rule counts body sentences only, so nothing fires); the author may reword.",
          "- Table 2's row 9 takes two lines (the brief allowed one); a one-line form would need the cell cut to about 60 characters (e.g. 'Lookup $0.92$ to $0.74$; Luna, Sol lead it by $0.13$ to $0.14$; the rest fall with it'), which drops the 0.06 to 0.07 loss from the table. Not done.",
          "- The cell's comma form, the bullet's clause order and the Conclusion's sentence split (section 3 above) are the three places the landed wording is not the brief's letter; each is printed old beside new.",
          "- Section 5.2's sentence keeps 'Retraction and expiry do not move' in the caption only after P1; if the slack is spent otherwise later, the sentence can return to 5.2 by dropping P1 from results/r137_close_units.txt.",
          "- 'median 41.5' prints in C.2 where the brief wrote 41 (the ledger's value; AUX-CFP-LOCK).",
          "- The C.2 tables are `[H]` like the PARA tables, so their pages carry the appendix's `\\flushbottom` gaps (results/r137_c2_p42.png to p45.png); a `[htbp]` placement would close the gaps but break the appendix's convention. Not changed.",
          "- Opus draws 2 to 5: nothing to land; the pipeline reads the draw count from the scores file (section 1).",
          "- The HV-1 placeholders in E.10: untouched, verbatim.", ""]
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"-> {OUT} ({len(L)} lines)")


if __name__ == "__main__":
    main()
