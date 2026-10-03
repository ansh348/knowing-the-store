# -*- coding: utf-8 -*-
"""claims_r126_block.py -- the R126 AUTHORIZATION BLOCK of CLAIMS.md (program R126, the readable body; 2026-09-20), written to
reviews/v22/claims_r126_block.md and appended to iclr2027_monitoring_submission/CLAIMS.md once (idempotent: the block is replaced in place when it
already exists, so a re-run after a further gate run refreshes the quoted list). Entries: the structured changes of the pass (R126-1 to R126-9) and
R126-F, which quotes every frozen string of the v21 build that the readable body replaced (from the latest reviews/v22/results/frozen_<tag>.json,
written by frozen_list_wp.py), so frozen_diff --program=R126 reads each as CHANGED-AUTHORIZED. A quoted string is a fragment between double quotes;
where a frozen string itself carries a double quote, its longest quote-free fragment of 30+ characters is quoted instead (frozen_diff authorizes a
string when a quoted fragment is contained in it).
Usage: python reviews/v22/tools/claims_r126_block.py [--json=reviews/v22/results/frozen_<tag>.json]
"""
from __future__ import annotations

import io
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
CLAIMS = SUB / "CLAIMS.md"
BLOCK = ROOT / "reviews" / "v22" / "claims_r126_block.md"
sys.path.insert(0, str(ROOT / "reviews" / "v22" / "tools"))
import port_v22  # noqa: E402

HEAD = "## R126 AUTHORIZATION BLOCK — dated 2026-09-20"


def gate_changes():
    argv = sys.argv
    sys.argv = ["port_v22.py", "--check"]
    try:
        port_v22.main()
    finally:
        sys.argv = argv
    return list(port_v22.GATE_CHANGES)


def quotable(text):
    """The string as a double-quoted fragment frozen_diff can pair: the text itself, or its longest quote-free fragment of 30+ characters."""
    if '"' not in text:
        return text
    parts = [p.strip() for p in text.split('"')]
    best = max(parts, key=len)
    assert len(best) >= 30, text
    return best


def r128_entries(js128, changed128):
    """R128 (2026-09-20; the author's brief reviews/v22/R128_BRIEF.md, section A lifted from the R127 hold; Sections 5.1 and 5.2 untouched): the
    entries sit inside the R126 block because frozen_diff runs with --program=R126 for the whole v22 lineage."""
    L = ["", "Program R128 (2026-09-20), inside this block: the author's section A (the abstract, Section 1, the Section 6 sentence, Section 7's last paragraph, the builders box; "
         "port_v22.py), sections B and C in the appendix (reviews/v22/tools/appendix_r128.py; build_v22.py REPAIRS_R128_BLOCK), the ledger reviews/NUMBERS_R128.md, the report reviews/v22/REPORT_R128.md. "
         "Sections 5.1 and 5.2 are unchanged (the R127 hold stands there). No model call was made.", ""]
    L.append("- **R128-A1 [which whole set]** (recorded). Abstract, before: \"GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 lead overall by $0.07$ to $0.08$; Opus leads by $0.03$ when all states are named.\" "
             "After: \"GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 lead it by $0.07$ to $0.08$ on the counterfactual set; Opus leads by $0.03$ when all states are named.\" "
             "Section 1, before: \"Luna, Sol and Opus pull ahead of it on the whole set, and Opus stays ahead by $0.03$ when every state is named.\" "
             "After: \"Luna, Sol and Opus pull ahead of it on the counterfactual set, and Opus stays ahead by $0.03$ when every state is named.\" "
             "The margins are AUX-CF2-OAI-P-S1/-S2 and AUX-R103-MARGIN on the counterfactual set; on the $661$ the lookup's persona interval covers every model. "
             "The Conclusion and Section 5.2 carry no 'whole set' sentence about this margin (checked; 5.2 untouched).")
    L.append("- **R128-A2 [the Section 6 sentence; U5]** (recorded). Before: \"Scores compress toward a low value, but the trigger remains unresolved.\" "
             "After: \"Scores collapse onto a few low values, with positives slightly below negatives, and the trigger remains unresolved.\" "
             "Checked against tab:dist (AUX-E7-*): the indexed positives read $0.1617$ against the negatives' $0.1688$ on Mem0 and $0.1544$ against $0.1658$ on A-MEM, over five distinct values. "
             "U5 re-pinned to the new sentence (tools/claims_diff.py U_BLOCKS, tools/slogan_scan.py PINNED). Appendix E.7 gains the explanation (R128-B2).")
    L.append("- **R128-A3 [Section 7's last paragraph]** (recorded). Before: \"This result limits that rule; it does not rule out other repairs that operate on retrieved content.\" "
             "After: \"A reference-free repair for copies under other keys remains open.\" (the Appendix pointer kept).")
    L.append("- **R128-A4 [the builders box]** (recorded). The lookup sentence gains \", and in the scenario we priced, a model call before every query cost more than the retrieval it saved (Appendix G.5)\"; "
             "checked against Appendix G.5 (AUX-UC-*): the measured mean monitor cost applied to the cached-depth batch adds \\$0.289083 against maximum selector allowances of \\$0.038258 and \\$0.106836.")
    L.append("- **R128-B [the appendix, substance]** (recorded). B1 the coverage rubric verbatim from e1_metamemory/tools/prompts_e1.py in E.3 (the FOK line and the JSON schema), beside the obligation half. "
             "B2 E.7's explanation of the collapse (five distinct values; positives below negatives; store-written rows lose nothing; rebuilt names restore) and tab:dist's caption. "
             "B3 the pooled-66 paragraph in E.7 (AUX-R128-POOLED66). B4 the Q4 probe's paragraph says the instruction's word 'absent' is also a label's name, so the probe cannot separate the two readings (REPAIRS_R128_BLOCK). B5 tab:destruction's caption gains the cross-store qualification (every positive an FR-Bank item, every Mem0 and A-MEM item a negative) with tab:destruction-fr named as the controlled comparison. B6 skipped: tab:setup and tab:counterfactual already carry Sol and Luna. "
             "B7 tab:ds-body's stale-rate columns carry both denominators (of the reached scorable obligations; of the answered subset, Wilson) with the abstention sentence in the caption; "
             "tab:ds-body-lower's dash becomes $[0.097,0.278]$ (AUX-R128-DS-DENOM). B8 tab:cf3-expiry gains three 'Opus 5, draw 1' rows (AUX-R128-CF3-DRAW1; the lookup rows' plus signs removed). "
             "B9 STOPPED, reported only: the one negation-cued question (fatima_q06) is among the 35 obligations with an active stale line, so correcting its tags would change the printed 35 of 89 and the ORACLE split. "
             "B10 the five Graphiti readings (GR-1 failed, GR-2 not computable, GR-3 held, GR-4 and GR-5 descriptive) in both Graphiti rows of Appendix F.")
    L.append("- **R128-C [the punch list]** (recorded). $1{,}273$ of the $3{,}305$; tab:v2rcat's draw-1 row labelled against the recorded $k=5$ row with the $0.8400$ / $-0.0351$ note (nothing numeric changed; AUX-V2RCAT-OP5 compares the $k=1$ run with the recorded $k=5$ row); "
             "'$0.75$ (rounded from $0.7484$)'; 'expiry triples' for 'expiry pairs'; tab:bh-split's $[0.6722,0.8992]$ on the persona row; E.11's three dollar amounts printed with the sign; "
             "G.4's '+0.1014 (from the unrounded scores)' and the 784 / 72 edge counts explained; the harness marker $^{h}$ defined in tab:ladder-predictions' notes and tab:inversion's caption (the two tables that used it undefined; tab:runs, tab:ladder-exact and tab:marker already defined it); the prompt template's backticks printed from T1 slot 0 (the TS1 glyph pulled a Type 3 font); "
             "tab:cf-hybrid's header 'first draw & first-draw gain'; tab:destruction, tab:inversion and the NB-6 caption qualified. The dagger and the 'TRUE $-0.0969$' items needed nothing: every dagger is defined in its table, and no caption carries 'TRUE' (it survives only as the key line of the two summaries E.7 reproduces verbatim; E.1 bridges INDEXED-TRUE).")
    L.append(f"- **R128-F [the frozen strings R128 changed on top of the R126 close; `{js128}`]** (recorded). Each string below occurred in paper_v21.tex, was kept by the R126 close and occurs a different number of times after R128: "
             "the first and third are E.7's prose under R128-B2 ('What triggers the compression is unresolved' reads 'collapse'; the clause '; the marker's wording is not it' closes the corrected sentence as ', and the marker's wording is not it'); "
             "the second is E.11's cost sentence, now printed with dollar signs (R128-C). Each is authorized under the entry named.")
    for r in changed128:
        L.append(f"  - {r['status']} [{r['tag']} {r['key']}] {r['base']} -> {r['new']}: \"{quotable(r['text'])}\"")
    return L


def r129_entries(js129, changed129):
    """R129 (2026-09-20; the author's brief 'KtS R129': rulings on R127b and R128's held items, two body landings, two payers, the E.3 table)."""
    L = ["", "Program R129 (2026-09-20), inside this block: the author's rulings A1 to A3, the body landings B1 and B2 with the payers C1 and C2 (port_v22.py), the appendix (appendix_r129.py), "
         "the ledger reviews/NUMBERS_R129.md (ledger_r129.py), the report reviews/v22/REPORT_R129.md. No model call. Section 5.1's count-reader paragraphs and Figure 3 stay held for R125.", ""]
    L.append("- **R129-A1 [Section 1, the MemoryAgentBench sentence; the ruling on R127b item 1]** (recorded). Before: \"On MemoryAgentBench's multi-hop conflict-resolution questions, no memory agent exceeds $7\\%$ accuracy \\citep{memoryagentbench}.\" "
             "After: \"On MemoryAgentBench's multi-hop conflict-resolution questions, no memory mechanism exceeds $7\\%$ accuracy and the best long-context model reaches $28\\%$ \\citep{memoryagentbench}.\" "
             "Source: Hu et al., Table 3, column FC-MH (every memory mechanism 7.0 or below; the long-context GPT-5-mini (400K) row 28.0) and the paper's own sentence.")
    L.append("- **R129-A2 [Section 7's stale-line count; the ruling on R128's B9]** (recorded). Before: \"Among $89$ scorable obligation views, $35$ contain an active line asserting the stale value.\" "
             "After: \"Among $89$ scorable obligation views, $35$ contain an active line asserting the stale value ($34$ once one inverted tag from the join is corrected).\" "
             "E.10 gains the paragraph (AUX-R129-B9: the FULL view of frbank:fatima:fatima_q06 leaves the 35, the retraction count 14 -> 13, the oracle split 16 / 0 and 14 / 5 as joined, 15 / 1 and 13 / 6 corrected; nothing re-answered) and the eight answer-stage captions say the tables were scored with the tag as joined.")
    L.append("- **R129-A3 [the moved-count table's draw-1 row and note]** (recorded). Accepted as R128 left it; no change.")
    L.append("- **R129-B1 [Section 5.1's moved-count paragraph; E9 in the body]** (recorded). Before: \"\\claim{Only Opus follows a count when it moves.} The \\emph{moved-count control} transfers the obligation's increment to a sibling store version while preserving the names. A reader following that count should rank the wrong version higher. Mini's expiry score rises by $0.06$, without a reliable difference; Haiku remains within tolerance. Opus falls reliably by $0.10$ on retraction and $0.13$ on expiry when draw counts are matched.\" "
             "After (the author's paragraph): \"\\claim{The three stronger models follow a count when it moves.} The \\emph{moved-count control} transfers the obligation's increment to a sibling store version while preserving the names, so a reader following that count should rank the wrong version higher. Opus falls reliably by $0.10$ on retraction and $0.13$ on expiry when draw counts are matched. Luna and Sol fall reliably on expiry, by $0.12$ and $0.19$; their retraction falls, $0.07$ and $0.03$, do not clear zero. Mini and Haiku show no reliable change.\" "
             "(AUX-V2RCAT-A1-OP5-K5; AUX-V2RCAT-A2-LUNA-K5, -SOL-K5; AUX-R129-E9-PRINTED.) E9's rows join tab:v2rcat with two sentences of prose and its row joins tab:registrations-d; its one prediction (P-M2, failed for both models) joins the count: Section 4 and Appendix F read $29$ of $93$ for $28$ of $92$ (AUX-R129-COUNT).")
    L.append("- **R129-B2 [Section 5.2, the hybrid reader's paragraph; E10 in the body]** (recorded). New paragraph after 'Naming all states helps readers and leaves an Opus advantage': "
             "\"\\claim{A cheap combined reader does not close the gap.} A logistic reader over the name similarity and the guessed category's non-active share, fit with personas held out, scores $0.79$ on the counterfactual set. It does not reliably beat the lookup, and Luna, Sol and Opus stay a reliable $0.05$ to $0.06$ above it.\" "
             "(AUX-CF2-HYB-WHOLE 0.7865; AUX-CF2-HYB-VS-LOOKUP +0.0201, the item interval including zero; AUX-CF2-HYB-VS-MODELS +0.0540, +0.0553, +0.0635; AUX-R129-HYB-PRINTED.) "
             "Built at the checkpoint 659737d with one word for prose_scan rule V ('left out' for 'held out'); **WITHDRAWN at the close by the author's ruling on REPORT_R129.md** (with B1 and B2 both in the body Figure 3 moved to page 7 and the box to page 10; the hybrid returns with the Section 5 rewrite once R125 Task 1 reports). "
             "tab:cf-hybrid keeps GPT-4.1 mini's five-draw row minus the hybrid, $-0.0217$ with both intervals including zero (AUX-R129-HYB-MINI5); the body says nothing about the hybrid.")
    L.append("- **R129-B3 [the search for other only-Opus count sentences]** (recorded). The main text carries no other sentence saying only Opus responds to counts (Section 1's bullet, the Conclusion, the box and the body captions checked; 'Only Opus lowers its judgment without being told' in Section 5.3 is about intent and stays).")
    L.append("- **R129-C1 [the payer in Section 5.1's first paragraph]** (recorded). Before: \"Counts alone score reliably below names alone: mini loses $0.12$, and Haiku loses $0.16$. This ablation uses mini's recorded single-call row rather than the repeated-call row in Table~\\ref{tab:cf-main}.\" "
             "After: \"Counts alone score reliably below names alone: mini loses $0.12$ on its single-call row, and Haiku loses $0.16$.\"")
    L.append("- **R129-C2 [the payer in Section 5.2, the long-or-wrong-lists paragraph]** (recorded). Before: \"On the full obligation set, padding the default list to $60$ names lowers the lookup to $0.67$, and mini falls with it; on the counterfactual set, injecting wrong names lowers mini, Haiku and the lookup together. Not every decline is reliable, and short ground-truth lists do not establish robustness to longer store-written lists.\" "
             "After: \"Padding the default list to $60$ names lowers the lookup to $0.67$ on the full obligation set, and injected wrong names lower mini, Haiku and the lookup together, so short ground-truth lists do not establish robustness to longer store-written ones.\"")
    L.append("- **R129-D [Appendix E.3, tab:e3-groups]** (recorded). The R127 / R127b group readings (AUX-R129-GROUPS) with four sentences; no body text (it comes with the Section 5 rewrite).")
    L.append(f"- **R129-F [the frozen strings R129 changed on top of the R128 close; `{js129}`]** (recorded). Each string below occurred in paper_v21.tex, was kept through the R128 close and occurs a different number of times after R129; each is authorized under the entry named above that replaced it.")
    for r in changed129:
        L.append(f"  - {r['status']} [{r['tag']} {r['key']}] {r['base']} -> {r['new']}: \"{quotable(r['text'])}\"")
    return L


def r131_entries(js131, changed131):
    """R131 (2026-09-20; the author's brief 'KtS R131: land R125 in the body (main session only)'): the R125 results landed in the body, the appendix,
    the ledger reviews/NUMBERS_R131.md and the report reviews/v22/REPORT_R131.md. No model call. Nothing from R130 lands."""
    import port_r131  # noqa: E402  (the gate table; the port is not re-run)
    L = ["", "Program R131 (2026-09-20), inside this block: the author's texts of sections A to G of the brief landed by reviews/v22/tools/port_r131.py on top of port_v22.py (Section 4's metric paragraph; "
         "Section 5.1 whole, retitled 'Names and counts'; Section 5.2 whole but its last paragraph; Table 1's matched column, hybrid row and two-metric difference row; Figure 3 on the matched metric "
         "(fig3_data_r131.py); the abstract's second sentence and three findings; Section 1's findings paragraph and second contribution; the Conclusion's sentences two to four; the evidence table's first row; "
         "Section 6's FR-Bank sentence and the merged Graphiti paragraph; the Limitations), the appendix by appendix_r131.py (C.2, E.9, F, G.4, the reader's guide; every table from reviews/r125/results), "
         "the number gate reviews/v22/tools/r131_number_gate.py (135 checks, 0 mismatches), the ledger reviews/NUMBERS_R131.md (ledger_r131.py), the page payers of section H as applied "
         "(port_r131.py --payers), the report reviews/v22/REPORT_R131.md. Sources: reviews/r125/REPORT_R125_T1.md, REPORT_R125.md, r82_counterfactual/cf2/NUMBERS_CF2.md section 15.", ""]
    L.append("- **R131-A [Section 4, the metric paragraph]** (recorded). The author's paragraph: the matched AUROC defined ('the share of triples in which the PN version outscores the PRESENT version, ties counting half'), post hoc, with the pooled metric as the one fixed in advance; "
             "the sentence 'when they disagree, the wider governs' leaves with it (the author's text); the persona-interval sentence moves to Table 1's caption.")
    L.append("- **R131-B [Section 5.1, 'Names and counts', whole]** (recorded). Four paragraphs in the author's words: 'Within a triple, a name or a count can identify the obligation.' (the category-given reader wins every counted-state triple, 30/0/0 and 30/0/0; the lookup 82/6/0 on supersession); "
             "'The two smaller models read only the names.' (names-only within 0.01 on either metric; counts alone below names alone by 0.14 matched for each, 0.12 and 0.16 pooled; both reliably below the guessing count reader, 0.77 and 0.75); "
             "'Removing the target name leaves mini near chance.' (0.86 to 0.53; 0.89 to 0.68); 'The three stronger models also read the counts.' (0.58 to 0.87 matched on the counted states, none reliably below the guessing reader; the moved count: Opus -0.2833 and Sol -0.3250 on the counted states, Luna -0.3167 / -0.2667, each reliable; mini and Haiku no reliable change; pooled as R129 printed; names-only costs Luna -0.0598 and Opus -0.0426 pooled, reliable; Sol not run). "
             "The R126 and R129 paragraphs 'Models read the names more than the counts', 'Count readers separate states that models barely tell apart', 'A bare count can give the obligation away' and 'The three stronger models follow a count when it moves' are replaced whole. AUX-CF2-R125-*, AUX-R131-PRINTED.")
    L.append("- **R131-C [Section 5.2, whole but the last paragraph]** (recorded). Four paragraphs in the author's words: 'On the named state, no model reliably beats the lookup.' (the lookup 0.9659 on supersession; Opus +0.0114, Luna and Sol -0.0057, mini -0.0739 reliable; the sibling-name control 0.8807 to 0.9716, none reliably above the lookup; random tokens 0.4716, the count reader 0.5000); "
             "'The stronger models' lead comes from counts, and a count feature closes it.' (the lookup and Haiku 0.7770, mini 0.7264; Luna 0.8784, Sol 0.8581, Opus 0.8750, +0.0811 to +0.1014 reliable; the hybrid 0.8851, +0.1081 reliable, level with the three; pooled 0.7865 with the three +0.0540 to +0.0635 above); "
             "'Naming all states lifts every reader.' (the lookup 0.9088; Haiku +0.3500 on the counted states; Opus 0.9392; +0.0304 not reliable against +0.0323 reliable pooled); 'List length and coverage inflate both metrics.' (0.7500 / 0.5000; 0.5954 / 0.6453; 24 of 88 empty; +0.1318 reliable). "
             "The R129 paragraph 'Long or wrong name lists weaken the readers together.' stays as the last paragraph. The R129 hybrid paragraph (withdrawn at the R129 close) returns inside the second paragraph with its comparison reversed under the matched metric.")
    L.append("- **R131-D [Table 1 and Figure 3]** (recorded). Table 1: the column 'PN vs PRESENT' (the pooled PN-against-PRESENT AUROC) becomes 'matched', (W + T/2) / 148 from the printed W/T/L (AUX-R131-TAB1); the hybrid reader's row ('Lookup with one count feature', 0.79 [0.75, 0.82]; matched 0.89; 114/34/0); "
             "the difference row prints both metrics at four decimals (pooled +0.0323 [+0.0060,+0.0617]; [+0.0077,+0.0608]; matched +0.0304 [-0.0068,+0.0643]; [-0.0038,+0.0648]) because the matched persona interval's lower bound rounds to -0.00 at two decimals; the caption's post hoc clause in the author's words; footnote b defines the hybrid row. "
             "Figure 3: reviews/v22/src/fig3_data_matched.tex (copied from reviews/r125/results/fig3_data_matched.tex after checking every value against r125_matched.json), the y axis from 0.35 (mini's expiry value 0.40), the y label 'matched AUROC', the author's caption; the pooled figure moves to Appendix C.2 as fig:perstate-pooled (build_v22.py splices the pooled data there with its macros renamed).")
    L.append("- **R131-E [the abstract, Section 1, the Conclusion, the evidence table]** (recorded). The abstract's second sentence and three findings, Section 1's findings paragraph and second contribution bullet, the Conclusion's sentences two to four and the evidence table's first-row limit in the author's words (the gate-driven words under R131-G). "
             "Before (abstract, findings one and two): \"First, names carry the signal: removing counts leaves GPT-4.1 mini and Haiku 4.5 within $0.01$, whereas counts alone cost mini $0.12$ and Haiku $0.16$ against names alone. Second, no model reliably beats a name lookup on the state named by the default summary. GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 lead it by $0.07$ to $0.08$ on the counterfactual set; Opus leads by $0.03$ when all states are named.\" "
             "After: \"First, GPT-4.1 mini and Haiku 4.5 read only the names; GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 also read the counts and follow one when it is moved. Second, on the state a summary names, no model reliably beats a cosine lookup over the names. With counts and list length kept fixed, the lookup and every model separate the right name from a sibling at or above $0.88$, while meaningless tokens and counts fall to chance. The three stronger models lead the lookup by $0.08$ to $0.10$ within matched triples, and a lookup given one count feature closes that lead.\" "
             "Before (Conclusion, sentences two to four): \"Removing names weakens the obligation judgment more than removing counts. Under the default summary, no model reliably exceeds the name lookup on supersession, while some models add signal on counted states. With all states named, Opus has a reliable overall advantage.\" "
             "After: \"The smaller models read only the names; the stronger ones also read the counts, and a lookup given one count feature matches them within triples. On a named state no model reliably exceeds the name lookup, with list length kept fixed or not; with all states named, Opus's $0.03$ lead is reliable on one metric and not on the other.\" "
             "The evidence table's first row: \"comparison with \\present{} alone is post hoc\" becomes \"the matched within-triple comparison is post hoc\".")
    L.append("- **R131-F2 [Section 6]** (recorded). The FR-Bank paragraph's last sentence, before: \"Haiku retains more of its gain than mini does, and more where the target's name survives the store's list ($0.87$ against $0.68$ where it does not; descriptive).\" "
             "After: \"Haiku retains more of its gain than mini does. The loss is not an artifact of the obligations the alignment misses: on the $82$ it marks, the capped summary still costs mini $0.13$, Haiku $0.13$ and the lookup $0.20$, each reliable.\" (AUX-CF2-R125-T3-FRBANK: -0.1274, -0.1258, -0.2027; the name-survival clause stays in Appendix E.9, AUX-BH-SPLIT). "
             "The two Graphiti paragraphs ('Graphiti's names serve the lookup better than mini.' and 'Graphiti's invalidation recovers some forbidding records, but misses most.') merge into the author's one: \"Graphiti writes part of what the judgment needs, and part of its loss is extraction.\" (13 of 34; 11 of 34 never extracted; 0.58 over all 47 against 0.74; the lookup 0.68, +0.10 reliable; on the 23 retained 0.69 against 0.84, -0.1512 reliable; AUX-CF2-R125-T3-GRAPHITI). "
             "Leaving the body with them: 'It gains nothing reliable over question only.', 'The reduced variants used elsewhere do not exist on these graphs.', 'exceeding the predicted quarter' (G.4 keeps all three).")
    L.append("- **R131-G2 [Limitations]** (recorded). Added: \"The matched metric and every comparison made with it are post hoc; the metric fixed in advance is the pooled AUROC. Sol did not run the names-and-counts ablation, and among the stronger models only Opus ran the all-states summary.\" "
             "Replaced, before: \"The ground-truth tags in retrieved views depend on aligning manifests to stored records. That alignment marks the forbidding record for $82$ of $104$ obligations.\" After: \"The ground-truth name lists are built through the manifest-to-record alignment. The $22$ obligations it does not mark are therefore invisible to every summary (mini scores $0.52$ on them under ground truth).\" (AUX-CF2-R125-T3-FRBANK, the 22: mini's ground-truth row 0.5210.) "
             "Deleted: \"Two further encoders leave the default lookup within $0.01$ of its score.\" (it stays in E.8) and \"The reader split cannot establish why the models differ and does not simply follow size.\" The pending sentences stay.")
    L.append("- **R131-H [the appendix]** (recorded). C.2: tab:cf-nc-strong (E2 Amendment 1; P-N3 failed on Luna, held on Opus 5; P-N4 held; P-N5 failed; Sol not run) after tab:cf-names-counts; the matched metric after tab:pnpresent (tab:cf-matched, tab:cf-classes, tab:cf-matched-vs, tab:cf-matched-ablations, fig:perstate-pooled, tab:cf-emptiness); "
             "tab:cf-hybrid's matched panels; the sibling-name control (tab:cf-sibling; P-SB1 to P-SB4 held, P-SB1 and P-SB3 disclosed as recorded values from the pre-freeze dry run). E.9: what the store is in each scored condition; tab:levels-strata. G.4: tab:graphiti-strata with its paragraph. "
             "F: tab:registrations-e (the two R125 registrations, 5cd8f809f2, day 41; tab:registrations-d is a [H] table at its page's height) and the count paragraph: 98 predictions, 31 otherwise (AUX-R131-COUNT; P-SB1 and P-SB3 not counted). The reader's guide points to the new tables. Every value from reviews/r125/results; pinned under pin_appendix_r126.py r131.")
    L.append("- **R131-G [the gate-driven wording changes on the author's texts; each the smallest change satisfying its rule, old beside new]** (recorded).")
    for target, rule, sec, old_, new_ in port_r131.GATES + port_r131.GATES_PAYERS:
        L.append(f"  - [{rule}] {sec}. Before: \"{old_}\" After: \"{new_}\"")
    L.append("  - [S7 (a sentence twice)] Appendix C.2, the pooled figure's caption: \"Luna and Sol ran only the default summary.\" (Figure 3's caption, the author's) reads \"Luna and Sol have rows under the default summary only.\" in the appendix copy.")
    L.append("  - [S17 ('both intervals excluding zero', capped at three outside registered blocks)] the appendix prose and captions of R131 say 'both intervals clear of zero'.")
    L.append(f"- **R131-F [the frozen strings R131 changed on top of the R129 close; `{js131}`]** (recorded). Each string below occurred in paper_v21.tex, was kept through the R129 close and occurs a different number of times after R131; each is authorized under the entry above that replaced it.")
    for r in changed131:
        L.append(f"  - {r['status']} [{r['tag']} {r['key']}] {r['base']} -> {r['new']}: \"{quotable(r['text'])}\"")
    return L


C_ABS_OLD = ("An agent with persistent memory must judge whether its store holds content it should no longer use. "
             "We test that judgment before retrieval on $148$ questions, each asked of three versions of one store, through summaries that list counts and attribute names with values removed. "
             "First, GPT-4.1 mini and Haiku 4.5 read only the names; GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 also read the counts and follow one when it is moved. "
             "Second, on the state a summary names, no model reliably beats a cosine lookup over the names. With counts and list length kept fixed, the lookup and every model separate the right name from a sibling at or above $0.88$, while meaningless tokens and counts fall to chance. "
             "The three stronger models lead the lookup by $0.08$ to $0.10$ within matched triples, and a lookup given one count feature closes that lead. "
             "Third, the backends we tested omit or misstate this information: under FR-Bank's own metadata, GPT-4.1 mini and the lookup fall to $0.60$ and $0.59$. "
             "At retrieval, a fetch keyed on the names raises reach from $0.52$ to $0.82$, gated by a model or always on, with a budget trade-off. "
             "These synthetic-store tests establish neither better answers nor a validated answer-stage detector; human validation remains pending.")


def _prov_text():
    import contextlib, io as _io
    import appendix_r131_close as A
    with contextlib.redirect_stdout(_io.StringIO()):
        A.G.main()
    return " ".join(l for l in A.prov_paragraph(A.G.PROV).strip().split("\n") if not l.startswith("%%"))


PROV_TEXT = _prov_text()


def r131_close_entries(jsc, changedc):
    """The R131 close (2026-09-20; the author's blocks 'R131 CONSOLIDATED ADDITIONS', 'ABSTRACT SWAP + ITS PAYER', 'R131 MERGED RULINGS', 'R131 FINAL
    RULINGS'): the body and abstract by port_r131_close.py, the appendix by appendix_r131_close.py, the number gate r131_close_gate.py (37 checks, 0
    mismatches), the ledger rows AUX-R131-CLOSE-* of reviews/NUMBERS_R131.md, the cumulative costed table cost_payers_r131_close.md, the report
    reviews/v22/REPORT_R131_CLOSE.md. No model call."""
    import port_r131_close as C  # noqa: E402  (the texts; the port is not re-run)
    import appendix_r131_close as A  # noqa: E402

    def flat(t):
        return " ".join(l for l in t.strip().split("\n") if not l.startswith("%%")).replace("\n", " ")

    L = ["", "The R131 close (2026-09-20), inside this block: the author's four blocks landed in one pass by reviews/v22/tools/port_r131_close.py on top of port_v22.py and port_r131.py --payers=1,2,3,4 "
         "(the abstract verbatim; L1 to L4; A1', A2' and the tex-658 word drop; 1A; 1B; the payers 5, 5b, 6, 7, 8 and B2, cumulative), the appendix by appendix_r131_close.py (E.3's provenance paragraph, "
         "E.9's disclosure sentence, A5 in B and E.4; build_v22.py REPAIRS_R131CLOSE_BLOCK for E.4's carried caption), the number gate reviews/v22/tools/r131_close_gate.py (37 checks, 0 mismatches; every "
         "count of E.3's paragraph from the tree), the ledger rows AUX-R131-CLOSE-PRINTED and -PROV of reviews/NUMBERS_R131.md (ledger_r131_close.py), the cumulative costed table "
         "reviews/v22/results/cost_payers_r131_close.md, the report reviews/v22/REPORT_R131_CLOSE.md.", ""]
    L.append("- **R131-CLOSE-B1 [the abstract, whole, verbatim; hand-tuned (B4)]** (recorded). Before: \"" + flat(C_ABS_OLD) + "\" After: \"" + flat(C.ABS_NEW) + "\" "
             "Its numbers: 148 (the triples); 0.88 (the sibling floor, Haiku 4.5 0.8807, AUX-CF2-R125-SB-*); chance 0.50; 0.08 to 0.10 (AUX-CF2-R125-VS-LOOKUP +0.0811 to +0.1014, each reliable; the lead decomposes to retraction and expiry, "
             "supersession -0.0057, -0.0057, +0.0114 none reliable); 0.73 and 0.75 to 0.60 and 0.59 (AUX-E1R-TRUE-NOK 0.7339, AUX-E1R-NB6 0.7484 / 0.5858, AUX-E1R-BELIEVED-NOK 0.5959; the full obligation set, ground truth against FR-Bank's capped store-written summary). "
             "The last clause ('human validation is pending') is a placeholder (B5), replaced when the HV-1 numbers exist. The fetch sentence (0.52 to 0.82) leaves the abstract; Section 7 and Table 3 keep it.")
    L.append("- **R131-CLOSE-B4 [the gate rulings on the abstract]** (recorded). Rule D's near-duplicate pair, the abstract's last-but-one sentence against Section 1's thesis sentence (85%), is overridden by the author "
             "('Restating the thesis in both places is intended.'): tools/prose_scan.py WHITELIST gains the abstract's sentence with this entry as its authority. Rule V on 'holds ... fixed': overridden, recorded; the rule bars 'held', not 'holds', so it did not fire. "
             "G2 (FINAL RULINGS 3): the pattern reading governs; 'drop from $0.73$ and $0.75$ to $0.60$ and $0.59$' stands (G2 concerns the lookup's level on the counterfactual set, where the level depends on the metric; the full-set numbers have one metric; "
             "R124 block C states no contradicting reason); the drops, for the record, 0.1380 and 0.1626 (AUX-R131-CLOSE-PRINTED). No gate changed a word of the abstract.")
    L.append("- **R131-CLOSE-B2 [Section 1, the findings paragraph; the abstract's payer]** (recorded). Before: \"" + flat(C.B2_OLD) + "\" After: \"" + flat(C.B2_NEW) + "\" "
             "Every deleted claim is in the contribution bullets below it or in Section 5 (names alone / counts, bullet 2; no reliable lookup margin including the sibling-name control, bullet 2; the one-count-feature lookup within triples, bullet 2; the backend loss and the fetch's reach, bullet 3). No number leaves.")
    L.append("- **R131-CLOSE-L [Limitations L1 to L3; Section 4 L4]** (recorded). L1 before: \"" + C.L1_OLD + "\" after: \"" + C.L1_NEW + "\" (40 verified against the bank). "
             "L2 before: \"" + C.L2_OLD + "\" after: \"" + C.L2_NEW + "\" ('completed only', FINAL RULINGS 4: Kimi K3 ran the cross-model set and was stopped at the budget on the full populations, tab:runs; 'open weights' is the authors' assertion, weights published by the vendor, July 2026). "
             "L3 before: \"" + C.L3_OLD + "\" after: \"" + C.L3_NEW + "\" (C.2 prints the within-0.02 result, 0.8531 against 0.8417 and 0.7253 against 0.7167, and Luna's reliable margin +0.0867). "
             "L4 before: \"" + C.L4_OLD + "\" after: \"" + C.L4_NEW + "\"")
    L.append("- **R131-CLOSE-A [provenance and anonymity: A1', A2', A5 (the statement), A1'' (E.3), the A3 follow-up (E.9)]** (recorded). "
             "A1' (Section 4) before: \"" + C.A1_OLD + "\" after: \"" + flat(C.A1_NEW) + "\" "
             "A2' (the AI-use statement) before: \"" + flat(C.A2_OLD) + "\" after: \"" + flat(C.A2_NEW) + "\" "
             "A5 before: \"" + C.A5_OLD + "\" after: \"" + C.A5_NEW + "\" (the word dropped, FINAL RULINGS 6). "
             "Verified against the tree (A4'): the 40 personas, their manifests, 1,400 sessions, the FR-Bank, Mem0 and A-MEM stores (LifeMemEval/artifacts/lifecycle_banks, mem0_41mini_banks, amem_banks, the directories e1_metamemory/tools/backends.py reads) and the 516 questions are in the FR-Bank release's freeze 5b097fb; "
             "this study drafted the natural-absent probes, the counterfactual questions and versions, the crossed intent questions and the paraphrases, and built the Graphiti graphs from FR-Bank's store records rendered one episode per session with every lifecycle field removed (r85_graphiti/render_episodes.py), not from the session transcripts (the correction of FINAL RULINGS 1). "
             "A1'' (Appendix E.3): \"" + PROV_TEXT + "\" "
             "A3 follow-up (Appendix E.9) before: \"" + A.E9_OLD + "\" after: \"" + flat(A.E9_NEW) + "\" (the release vendors graphiti/ 0.28.1 and graphiti_patches/; the FR paper's FR-Graphiti row). "
             "A5 in the appendix (FINAL RULINGS 6): B \"" + A.B_OLD + "\" -> \"" + A.B_NEW + "\"; E.4 \"" + A.E4_OLD + "\" -> \"" + A.E4_NEW + "\" and tab:cluster-sensitivity's caption 'reports the preregistered item-level interval' -> 'reports the registered item-level interval' (REPAIRS_R131CLOSE_BLOCK); "
             "left as ruled: the pinned sections' hits (A: the ladder table's caption and the expansion sentence; E.3: the corpus row's 'preregistered Mem0 exclusions' and the retention-threshold sentence; E.7: 'reported as they were preregistered'; E.10: 'Each was preregistered' and 'The preregistered reading'; F: the Opus-entry paragraph) and the four artifact names of tab:registrations (E0, E1, E1-XV, E1-QP preregistration). "
             "The A3 census (we / our / an agentless passive on creating personas, sessions or manifests) found the two replaced sentences, the AI-use opener (now 'to draft questions') and, borderline, E.9's disclosure (now attributed) and G.4's 'episodes rendered from FR-Bank's persona banks' (stays, FINAL RULINGS).")
    L.append("- **R131-CLOSE-1 [MERGED RULINGS 1A and 1B]** (recorded). 1A: the count 98 / 31 stands (P-SB1 and P-SB3 out of the count, in tab:registrations-e as recorded before the freeze; 100 / 31 printed nowhere); Table 1's difference sub-table at four decimals, uniform, with the caption note "
             "\"Differences at four decimals.\"; Sol's 0.33 confirmed as half-up on the recorded four-decimal value, the convention of every check (AUX-R131-CLOSE-PRINTED). "
             "1B: the builders box before: \"" + C.BOX_OLD + "\" after: \"" + C.BOX_NEW + "\" (the author's words, FINAL RULINGS 4: deletion alone would omit the pooled reliable lead). 'one name longer' -> 'at least one name longer': the body's only instance leaves with payer 8; C.2's two sentences stay (the section is pinned; tab:cf-emptiness prints 81 / 6 / 1; FINAL RULINGS 3).")
    L.append("- **R131-CLOSE-P [the page payers, cumulative in the ruled order (MERGED RULINGS 1C); the costed table reviews/v22/results/cost_payers_r131_close.md]** (recorded). "
             "Payer 5 (Section 5.1): the target-name paragraph out, \"" + flat(C.P5_PAR) + "\" (E.10 tab:resp-l1 prints 0.8572 -> 0.5310 and 0.8897 -> 0.6759, both reliable); the pointer \"" + C.P5_PTR_OLD.strip() + "\" -> \"" + C.P5_PTR_NEW.strip() + "\". "
             "Payer 5b (the Conclusion): \"" + C.P5B_OLD + "\" -> \"" + C.P5B_NEW + "\" (Luna 0.96, Sol 0.88, Opus 0.99 under the explicit rubric; mini 0.48, Haiku 0.55; the cue list 0.9943 against Opus's 0.99). "
             "Payer 6 (Section 5.3, P6a to P6d): deleted \"" + C.P6A_OLD.strip() + "\" (tab:cf-intent's caption says the body reads the draw-1 column; no caption addition, P6a); deleted \"When Sol fails, it often scores both questions high, leaving the rule unapplied.\" (the caption: 9 of Sol's 11 losses score both questions 0.96 or higher); "
             "\"Those models score the change question higher, consistent with the scored step asking whether stale content exists. The content remains in the store.\" -> \"" + C.P6C_NEW.strip() + "\"; deleted \"Across these tests, stating the rule lowers no model's score on its original questions beyond tolerance.\" (the caption: the largest fall -0.0458). Every bold lead, the 0.96 / 0.88 / 0.99 sentence, the cue list at 0.99, the no-general-advantage sentence, the underspecified-prompt sentence and Sol's 0.64 untouched. "
             "Payer 7 (Figure 3): height 5.0cm -> 4.5cm, width, markers and fonts unchanged; rendered at both heights: the Luna 0.8667 / Sol 0.8333 expiry markers (the only pair near the 0.86 to 0.88 band) do not overlap at either height; one new corner touch of 0.26pt appears between mini 0.9205 and Haiku 0.8920 in the right panel's supersession cluster (outside the band; reported). "
             "Payer 8 (Section 5.2): \"" + flat(C.P8_OLD) + "\" -> \"" + flat(C.P8_NEW) + "\" (0.60 / 0.65 and 24 of 88 stay in tab:cf-emptiness and tab:cf-matched). "
             "Payer B2: the entry R131-CLOSE-B2. Section 8 and the evidence table are not payers (ruled). O1 lands only at slack +5 or better.")
    L.append("- **R131-CLOSE-G [the gate-driven wording changes on the close's texts; each the smallest change satisfying its rule, old beside new]** (recorded).")
    for target, rule, sec, old_, new_ in C.GATES:
        L.append(f"  - [{rule}] {sec}. Before: \"{old_}\" After: \"{new_}\"")
    if not C.GATES:
        L.append("  - none: every prose gate passed on the author's texts as given (the D override of R131-CLOSE-B4 is a ruling, not a wording change).")
    L.append(f"- **R131-CLOSE-F [the frozen strings the close changed on top of the R131 checkpoint; `{jsc}`]** (recorded). Each string below occurred in paper_v21.tex, was kept through the R131 checkpoint and occurs a different number of times after the close; each is authorized under the entry above that replaced it.")
    for r in changedc:
        L.append(f"  - {r['status']} [{r['tag']} {r['key']}] {r['base']} -> {r['new']}: \"{quotable(r['text'])}\"")
    return L


def r131_w_entries(jsw, changedw, skip):
    """The R131 close's page 8-9 payers (2026-09-20; 'R131 CLOSE: PAGE 8-9 PAYERS', W1 to W7 by port_r131_w.py; the cumulative costed table
    reviews/v22/results/cost_payers_r131_w.md). A W item the author withdrew after a gate trip is listed as withdrawn."""
    import port_r131_w as W  # noqa: E402

    def flat(t):
        return " ".join(l for l in t.strip().split("\n") if not l.startswith("%%")).replace("\n", " ")

    L = ["", "The R131 close's page 8-9 payers (2026-09-20), inside this block: W1 to W7 landed cumulatively by reviews/v22/tools/port_r131_w.py on top of port_r131_close.py "
         "--payers=5,5b,6,7,8,B2 (the number gate r131_w_gate: 9 checks, 0 mismatches), costed by cost_payers_r131_w.py (W1 -4; +W2 -3; +W3 -3; +W4 -2; +W5 -1; +W6 +0; +W7 +1; "
         "without W3 +1). Gates may not reword these texts; a trip is reported and the author rules.", ""]
    L.append("- **R131-W1 [Section 8, the first paragraph]** (recorded). Before: \"" + W.W1A_OLD + "\" After: \"" + W.W1A_NEW + "\" (the pointer '(Appendix A)' joined the line above after W1a, so W1b, 'Kimi included', was not needed).")
    L.append("- **R131-W2 [Limitations, paragraph 1]** (recorded). Before: \"" + W.W2_OLD + "\" After: \"" + W.W2_NEW + "\" (30 / 30 pairs, r125_matched.json; 26 and 15 obligations, r125_t3_frbank.json all_104 by_state).")
    if 3 in skip:
        L.append("- **R131-W3 [Limitations, paragraph 3] WITHDRAWN pending the ruling** (recorded). The author's sentence \"" + W.W3_NEW + "\" opens its paragraph on the numeral 22, which q_scan rule Q-A bars (the R131 checkpoint had split it for that reason); "
                 "gates may not reword it, so it is reported; the R131 split stands meanwhile (\"" + W.W3_OLD + "\"). W3 bought no line (-3 to -3), and W1 to W7 without it read +1.")
    else:
        L.append("- **R131-W3 [Limitations, paragraph 3]** (recorded). Before: \"" + W.W3_OLD + "\" After: \"" + W.W3_NEW + "\" (the author's sentence; q_scan Q-A exempted by ruling).")
    L.append("- **R131-W4 [Section 7, the tested-rule paragraph]** (recorded). Before: \"" + flat(W.W4_OLD) + "\" After: \"" + flat(W.W4_NEW) + "\" (the third sentence repeated the bold lead).")
    L.append("- **R131-W5 [Limitations, paragraph 2]** (recorded). \"" + W.W5A_OLD + "\" -> \"" + W.W5A_NEW + "\"; \"" + W.W5B_OLD + "\" -> \"" + W.W5B_NEW + "\" (the one-rewording design is stated in Appendix C.2's paraphrase paragraph, checked; the sentence is replaced on 22 Sep).")
    L.append("- **R131-W6 [Conclusion]** (recorded). \"" + W.W6_OLD + "\" -> \"" + W.W6_NEW + "\" (the all-states clause deleted because still short of +2; Section 5.2 keeps 'Opus's $0.03$ lead over that lookup is reliable on the pooled metric and not on the matched one').")
    L.append("- **R131-W7 [Section 8, the second paragraph; Appendix E.8]** (recorded). Before: \"" + flat(W.W7_OLD) + "\" After: \"" + flat(W.W7_NEW) + "\" E.8 gains, after the paragraph on where the lookup has values: "
             "\"On the counterfactual set every model's coverage interval excludes chance (Table~\\ref{tab:cf-fok}, Appendix~\\ref{app:counterfactual}).\" (C.2 prints the intervals, tab:cf-fok; pinned under pin_appendix_r126.py r131w).")
    L.append(f"- **R131-W-F [the frozen strings the W payers changed; `{jsw}`]** (recorded). Each string below occurred in paper_v21.tex, was kept through the close checkpoint and occurs a different number of times after W1 to W7; each is authorized under the entry above that removed it.")
    for r in changedw:
        L.append(f"  - {r['status']} [{r['tag']} {r['key']}] {r['base']} -> {r['new']}: \"{quotable(r['text'])}\"")
    return L


def main():
    # R128 (2026-09-20): R126-F is pinned to the R126 close's list (frozen_r126_final.json, 97 strings); the strings R128 changed on top of it are
    # quoted under R128-F from the latest frozen_r128_*.json (--r128-json= names another), so each pass's strings sit under its own entry.
    js = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--json=")), "reviews/v22/results/frozen_r126_final.json")
    rows = json.loads((ROOT / js).read_text(encoding="utf-8"))
    changed = [r for r in rows if r["status"] != "KEPT"]
    # R129 (2026-09-20): R128-F pinned to the R128 close's list (frozen_r128_final.json); the strings R129 changed on top of it are quoted under
    # R129-F from the latest frozen_r129_*.json (--r129-json= names another).
    js128 = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--r128-json=")), "reviews/v22/results/frozen_r128_final.json")
    seen = {r["text"] for r in changed}
    changed128 = [r for r in json.loads((ROOT / js128).read_text(encoding="utf-8")) if r["status"] != "KEPT" and r["text"] not in seen]
    js129 = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--r129-json=")), "reviews/v22/results/frozen_r129_close.json")   # R131: pinned to the R129 close
    seen |= {r["text"] for r in changed128}
    changed129 = [r for r in json.loads((ROOT / js129).read_text(encoding="utf-8")) if r["status"] != "KEPT" and r["text"] not in seen] if js129 else []
    gc = gate_changes()
    L = [HEAD, "",
         "Program R126: the v22 lineage, opened from the R124 close `ee6b735` (`reviews/v22/`, base tree `ea71a9d0`, tag `base-tree/v22`; HEAD tagged `fallback/v22-pre-restructure`; "
         "`reviews/v22/tools/bump_v22.py`). The main text (title through the box) is the readable body delivered to `reviews/v22/inbox/v22_readable_main.tex`, ported by "
         "`reviews/v22/tools/port_v22.py` (every conversion and wording change asserted); the appendix is repaired by `appendix_r126.py` and `build_v22.py` REPAIRS_R126_BLOCK; "
         "Figure 3 is `fig3_data.py`; the ledgers are `reviews/NUMBERS_R126.md` and `reviews/v22/NUMBER_MOVES_V22.md`; the report is `reviews/v22/REPORT_R126.md`. "
         "frozen_diff runs with `--program=R126` against the v22 base. This block supersedes the body entries of R124 (their texts are inside the readable body or replaced by it); "
         "R124's non-body items stand.", ""]
    L.append("- **R126-1 [the readable body; the brief, Phase 1]** (recorded). Sections 1 to 10 and the box are the inbox text in the new order (1 Introduction, 2 Related work, 3 Framework, 4 Setup, "
             "5 What readers read with 5.1 names against counts, 5.2 the lookup against the models, 5.3 when intent licenses old content, 6 What backends write, 7 At retrieval, 8 Replication and the coverage judgment, "
             "9 Limitations, 10 Conclusion, the builders box). Ours, verbatim from v21: the preamble, Definition 1 with its grid (def:coverage), Table 2's census rows, the statements, the bibliography. "
             "Figure 1 is the inbox's three-box TikZ with the masked-retrieval note under the tag route (the addendum's A1; our adapted v21 drawing was retired); our Figure 2 table with the inbox's row labels and caption; Table 1 in the inbox's layout with v21's values; Table 3 with v21's rows. "
             "Every \\N{value}{provenance} of the inbox is printed as the value (math mode for numerals; `reviews/v22/INBOX_NUMBERS_R126.md`); every \\ap{} pointer is a \\ref to our label; "
             "the inbox's labels map to ours (tab:readers to tab:cf-main, fig:triple to fig:example, fig:states to fig:perstate, def:state_intent to def:coverage, sec:readers to sec:counterfactual, "
             "sec:retrieval to sec:downstream and sec:routes, sec:replication to sec:populations); the sixteen citation keys the inbox dropped are restored at their sentences (no new entry). "
             "The notation box and Definition 2 (def:index) move to Appendix E.1 verbatim.")
    L.append("- **R126-2 [Phase 2.1, the contributions]** (recorded). The author's three bullets replace the inbox's three (CONTRIB in port_v22.py).")
    L.append("- **R126-3 [Phase 2.2, the abstract's third finding]** (recorded). Before (the inbox): \"Third, backend metadata omit or misstate lifecycle information, weakening readers' judgments.\" "
             "After (the author's): \"Third, the backends we tested omit or misstate this information: under FR-Bank's own metadata, mini and the lookup fall to $0.60$ and $0.59$.\"")
    L.append("- **R126-4 [Phase 2.3, the Mem0 and A-MEM paragraph and U5]** (recorded). Before: \"Luna loses under every rendering tested through the raw API\" After: \"Luna loses $0.27$ to $0.34$ under every rendering tested through the raw API\" "
             "(AUX-MARKER-*), so the paragraph carries all four U5 conditions. U5 re-pinned (claims_diff.U_BLOCKS, slogan_scan.PINNED): old pinned string \"What triggers the loss under the constrained rendering is unresolved\" "
             "(R124 A2, v21's Limitations pointer), new pinned string \"Scores compress toward a low value, but the trigger remains unresolved.\" (the paragraph's own closing sentence, unchanged from the inbox).")
    L.append("- **R126-5 [Phase 2.4, Table 2's caption]** (recorded). The inbox's \"These are counts, without sampling intervals.\" becomes the author's sentence, printed as "
             "\"Counts of disagreement with the manifest-and-alignment reference, without hand adjudication; no sampling intervals.\" (the author's \", not adjudicated by hand\" trips slogan_scan S9 in the main text); "
             "superseded by the addendum's A2 (2026-09-20): the caption reads \"Backend census: counts of disagreement with the manifest-and-alignment reference, without hand adjudication or sampling intervals. Lower panel: coverage losses and rebuilt-summary scores. (Appendices E.7 and E.9)\", "
             "and the matching-threshold note, the conflation note and the two reproduction script names are in Appendix E.9.")
    L.append("- **R126-10 [the author's addendum of 2026-09-20 after the read of the mid-progress build]** (recorded). A1 Figure 1 (above); A3 Section 6's first paragraph in the author's words; "
             "A4 Definition 1's 'under $i(q)$' printed as 'under the question's intent' and the hike paragraph's last two sentences deleted; A5 Section 3's two summary-size sentences to Appendix E.3; "
             "A6 the long-or-wrong-lists paragraph in the author's words (the 0.02 injection margin leaves the body; AUX-PAD-C-MINI +0.0122, -C-H45 +0.0192 verified); A7 the 'Haiku fares better' paragraph to Appendix E.9 and the author's sentence "
             "'Haiku retains more of its gain than mini does, and more where the target's name survives the store's list ($0.87$ against $0.68$ where it does not; descriptive).'; "
             "A8 Section 7's first two paragraphs merged in the author's words (the 0.79 / 0.82 pair leaves the body; AUX-RESP-A1-H45-HYBRID 0.7863 against Haiku 4.5's ground-truth row 0.8210, verified, within tolerance at -0.0347). "
             "B1 Section 1's two finding sentences in the author's words; B2 'registered with a bar' kept, tools/prose_scan.py rule V gaining that collocation; B3 the Conclusion's first sentence in the author's words with one word changed for rule D ('wrote'; R126-9). "
             "Aggregate cost: page 10, fine number 501 to page 9, fine number 482 (the target 480 not reached; the costed table is reviews/v22/results/cost_payers_r126.md and REPORT_R126.md).")
    L.append("- **R126-6 [Phase 2.5, the Section 5.1 merges]** (recorded). \"Knowing the category helps a count reader\" folded into the paragraph before it (its bold lead dropped); "
             "\"Permuting the totals barely changes the models' scores\" folded into \"A bare count can give the obligation away\" as its closing sentences. No word of the sentences changed.")
    L.append("- **R126-7 [Phase 3, Figure 3]** (recorded). Redrawn in pgfplots from `reviews/v22/src/fig3_data.tex` (fig3_data.py: AUX-R122-K5-ROWS for GPT-4.1 mini at five draws, AUX-CF2-*-V2/-V3, AUX-CF2-OAI-*, AUX-R110-A1-CR); "
             "provisional until R125 reports, when the data file is regenerated.")
    L.append("- **R126-8 [Phase 4, the appendix; appendix_r126.py and REPAIRS_R126_BLOCK]** (recorded). (4.1) three pointers retargeted to Section 5's sub-labels; no hardcoded cross-reference number exists. "
             "(4.2) the reader's guide of eight sentences with the term bridge; seven rows in E.1's terms table; the captions of tab:cf3-expiry, tab:dist, tab:marker, tab:gatereach (prose) and tab:inversion, tab:q4-marker, tab:s1-names (E.7's carried block) use the body's terms "
             "with the old term in parentheses. (4.3) the R124 leftovers had landed in v21 (checked); tab:ds-a8's two rows lose their extra brace (the 21 inherited LaTeX errors). "
             "(4.4) the registration record's calendar dates become day indices beside the hashes (day 0 = the first freeze; AUX-R126-DAYS), in tab:registrations (carried; the caption and header say 'freeze day'), -b, -c, -d, "
             "E.3's threshold sentence, E.10's fourth-amendment sentence and F's attestation and Opus-entry paragraphs; the G.4 parenthetical after GR-1's quotation reads \"(The bracketed words stand in for the store's name as the registered text gives it.)\" "
             "in place of \"(The quotation is redacted for anonymity.)\". (4.5) three recorded rows (top-five, the lookup rule, the oracle) in tab:gatereach's licensed panel from reach_rows_r123.json (AUX-R126-GATEREACH). "
             "(4.6) E.3's sentence corrected to tab:e3-intent (AUX-R126-E3-INTENT): every PN question has current or upcoming intent, and 44 PRESENT questions hold a non-active record of their own attribute (33 current or upcoming, 11 change).")
    L.append("- **R126-9 [Phase 5.3, the gate-driven wording changes; each the smallest change satisfying its rule, listed with the rule]** (recorded).")
    def flat(s):   # a paragraph break inside a quoted string would split the block's paragraph and unpair frozen_diff's quotes
        return s.strip().replace("\n\n", " [paragraph break] ").replace("\n", " ")
    for rule, sec, old, new in gc:
        L.append(f"  - [{rule}] {sec}. Before: \"{flat(old)}\" After: \"{flat(new)}\"")
    L.append("  - [Q-A, the tool's sentence splitter] reviews/v22/tools/q_scan.py and readability_wp.py end a sentence at '.}' as well, so a bold run-in claim sentence (\\claim{...}) is read as its paragraph's opener; "
             "the rule's text is unchanged. Without it Q-A tripped 22 times for that one reason (REPORT_R126.md, Phase 5.3).")
    L.append("  - [G2] tools/prose_scan.py rule G2 stands as R124 block C narrowed it (a hit is an abstract sentence that names the lookup and states its own AUROC level); recorded here as the rule in force for v22.")
    L.append(f"- **R126-F [the frozen strings of the v21 build that the readable body replaced; `{js}`]** (recorded). Each string below occurred in paper_v21.tex and occurs a different number of times in paper_v22.tex "
             "(a count of zero means the sentence left the body; the new sentence carrying the claim is in reviews/v22/BODY_MAP_R126.md). Every one is authorized as replaced by the readable body under R126-1.")
    for r in changed:
        L.append(f"  - {r['status']} [{r['tag']} {r['key']}] {r['base']} -> {r['new']}: \"{quotable(r['text'])}\"")
    L += r128_entries(js128, changed128)
    L += r129_entries(js129, changed129)
    # R131 (2026-09-20): R129-F pinned to the R129 close's list (frozen_r129_close.json); the strings R131 changed on top of it under R131-F from the
    # latest frozen_r131_*.json (--r131-json= names another).
    js131 = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--r131-json=")), None)
    if js131 is None:
        files = sorted((ROOT / "reviews" / "v22" / "results").glob("frozen_r131_[a-z].json"), key=lambda p: p.stat().st_mtime)   # the checkpoint's own tags (a to e), not the close's
        js131 = files[-1].relative_to(ROOT).as_posix() if files else None
    seen |= {r["text"] for r in changed129}
    changed131 = [r for r in json.loads((ROOT / js131).read_text(encoding="utf-8")) if r["status"] != "KEPT" and r["text"] not in seen] if js131 else []
    L += r131_entries(js131, changed131)
    # The R131 close (2026-09-20): R131-F pinned to the R131 checkpoint's list (frozen_r131_e.json); the strings the close changed on top of it under
    # R131-CLOSE-F from the latest frozen_r131_close_*.json (--r131close-json= names another).
    jsc = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--r131close-json=")), None)
    if jsc is None:
        files = sorted((ROOT / "reviews" / "v22" / "results").glob("frozen_r131_close_*.json"), key=lambda p: p.stat().st_mtime)
        jsc = files[-1].relative_to(ROOT).as_posix() if files else None
    seen |= {r["text"] for r in changed131}
    changedc = [r for r in json.loads((ROOT / jsc).read_text(encoding="utf-8")) if r["status"] != "KEPT" and r["text"] not in seen] if jsc else []
    L += r131_close_entries(jsc, changedc)
    # The page 8-9 payers (W1 to W7): the strings they changed on top of the close's list under R131-W-F from --r131w-json= (none without it).
    jsw = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--r131w-json=")), None)
    skipw = {int(x) for x in next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--w-skip=")), "").split(",") if x.strip()}
    if jsw:
        seen |= {r["text"] for r in changedc}
        changedw = [r for r in json.loads((ROOT / jsw).read_text(encoding="utf-8")) if r["status"] != "KEPT" and r["text"] not in seen]
        L += r131_w_entries(jsw, changedw, skipw)
    text = "\n".join(L) + "\n"
    BLOCK.write_text(text, encoding="utf-8", newline="\n")
    claims = CLAIMS.read_text(encoding="utf-8", errors="replace")
    crlf = "\r\n" in claims
    c = claims.replace("\r\n", "\n")
    if HEAD in c:
        i = c.index(HEAD)
        m = re.search(r"^## (?!R126 AUTHORIZATION)", c[i + len(HEAD):], flags=re.M)
        j = i + len(HEAD) + m.start() if m else len(c)
        c = c[:i] + text + ("\n" if m else "") + c[j:]
        what = "replaced"
    else:
        c = c.rstrip("\n") + "\n\n" + text
        what = "appended"
    CLAIMS.write_bytes((c.replace("\n", "\r\n") if crlf else c).encode("utf-8"))
    print(f"-> {BLOCK} ({len(changed)} R126 + {len(changed128)} R128 + {len(changed129)} R129 + {len(changed131)} R131 + {len(changedc)} R131-close frozen strings quoted, {len(gc)} gate changes); CLAIMS.md block {what}")


if __name__ == "__main__":
    main()
