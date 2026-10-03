# -*- coding: utf-8 -*-
"""land_r118.py -- program R118: land one step of the v21 lineage (the author's rulings of 19 September). A step = the r118_apply groups it
applies + the CLAIMS.md R118 entries it records (appended to the R118 block in CLAIMS.md, CRLF, and to reviews/v21/claims_r118_block.md, LF)
+ the number_moves_wp.py dispositions for the numerals the step adds or removes. Idempotent: an entry already present is not appended twice;
r118_apply's own idempotence covers the sources. The gates (run_gates.py) and the appendix pins (pin_appendix_r118.py) run after.
Usage: python reviews/v21/tools/land_r118.py <step> [--no-moves]      steps: sec8_cr, payers, e5, e2, e3, e4, e1, notation_clause
"""
from __future__ import annotations

import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
V21 = ROOT / "reviews" / "v21"
CLAIMS = SUB / "CLAIMS.md"
BLOCK = V21 / "claims_r118_block.md"
NM = V21 / "tools" / "number_moves_wp.py"
PY = sys.executable

STEPS = {
    "sec8_cr": {
        "groups": "sec8,cr",
        "entries": [
            "- **R118-2 [Section 8 restructured for page space; Appendix A and E.8; the author's ruling 4 of 19 September; `reviews/v21/tools/r118_apply.py` group `sec8`]** (recorded). "
            "Section 8 is cut to four sentences: its opener \"The obligation gain replicates across six models from three vendors.\" (kept); the cross-model sentence, Before: \"Every paired gain excludes zero where the blind score varies, on the cross-model set (Table~\\ref{tab:ladder-exact}, Appendix~\\ref{app:laddertable}) and on the full obligation set (Table~\\ref{tab:e1}).\" followed by \"On the cross-model set the five models with a varying blind score gain $+0.15$ to $+0.45$, Kimi K3 among them at $+0.26$.\", After: \"Every paired gain excludes zero where the blind score varies, the five such models on the cross-model set gaining $+0.15$ to $+0.45$, Kimi K3 among them at $+0.26$ (Table~\\ref{tab:ladder-exact}, Appendix~\\ref{app:laddertable}).\"; "
            "the indexed levels against the lookup on the $661$ questions with the question-signal caveat, new: \"Haiku 4.5, Opus 5 and GPT-5.6 Luna score $0.82$ to $0.83$ indexed on the full obligation set against the name lookup's $0.75$ on the same $661$ questions (Table~\\ref{tab:e1}), levels that include what the question wording gives away (Section~\\ref{sec:setup}).\" (the values are Table tab:e1's, AUX-R74-X4-*, and the lookup's $0.7484$ of tab:baselines); "
            "one coverage sentence, new: \"On coverage the easy-tier margin over the name lookup does not survive a lookup over the whole name map (Table~\\ref{tab:cov-lookup}, Appendix~\\ref{app:baselines}), and on the counterfactual set every model's coverage interval excludes chance (Table~\\ref{tab:cf-fok}, Appendix~\\ref{app:counterfactual}).\" (AUX-WP-F1-WHOLEMAP; AUX-R104-CF-FOK, every persona interval above $0.50$). "
            "Table tab:e1 moved whole to Appendix A after the expansion table (float specifier [h] to [H]; words and values unchanged) with a lead sentence; Section 8's coverage paragraph moved whole to Appendix E.8 after tab:cov-lookup under the heading \"The coverage judgment against its floor.\", its pointer \"(Appendix~\\ref{app:baselines})\" replaced by \"(Table~\\ref{tab:cov-lookup})\" (the paragraph now sits in that appendix); frozen_diff reads its two CLAIMS-quoted sentences as MOVED: \"The coverage margin over the name lookup does not survive a lookup over the whole name map.\" and \"On the hard tier every coverage positive is an obligation, so the coverage and obligation scores are one row, and the lookup's $0.79$ against the model's $0.70$ is not a reliable difference.\". "
            "No number, interval or population changed; numeric_diff ADDED 0, VANISHED 0. Page: fine number 466 against 485 after this step alone (from 480), the label on page 9.",
            "- **R118-3 [the count readers' descriptions; Section 5 and Appendix C.2; the author's ruling 2 of 19 September; reviews/r117/COUNT_READERS_NOTE.md; `r118_apply.py` group `cr`]** (recorded). "
            "The category-guessing reader (CR-nb1, `reviews/v18/tools/a1_count_readers.py`) reads the share of a category's entries that are superseded, retracted or expired at the category `assign_category` picks from the question; the category-aware reader (CR-oracle-a) reads the retracted-plus-expired count at the manifest category. Three descriptions said otherwise. "
            "Section 5, Before: \"the other is a count reader that guesses the question's category from its text and reads that category's retracted and expired \\emph{counts}.\" then \"A category-aware count reader, which takes the category from the manifest, is that reader's upper bound on the two counted states.\" After: \"the other is a count reader that guesses the question's category from its text and reads the share of that category's entries that are no longer active.\" then \"A category-aware count reader takes the category from the manifest instead and reads that category's retracted-plus-expired \\emph{count}.\" "
            "Section 5, Before: \"The category-guessing count reader separates the retracted versions at $0.67$ and the expired at $0.69$ ($30$ pairs each), its category-aware oracle at $0.73$ and $0.78$, where every model scores $0.53$ to $0.62$.\" After: \"The category-guessing count reader separates the retracted versions at $0.67$ and the expired at $0.69$ ($30$ pairs each), the category-aware count reader at $0.73$ and $0.78$, where every model scores $0.53$ to $0.62$.\" (word-neutral; the numbers unchanged). "
            "Appendix C.2, Before: \"the category-guessing reader assigns the category from the question by the recorded rule of the question-only baseline suite and reads the same count; a state-aware reader, an upper bound that knows the state as well as the category, reads the state's own cell.\" After: three sentences giving each reader's quantity exactly (a count; a different quantity, the share of the category's entries that are superseded, retracted or expired; the state's own cell), \"an upper bound\" dropped from the state-aware reader's description and from its row label in tab:cf-cr, because the privileged share reader is above it on expiry ($0.8528$ against $0.7778$). "
            "Added to C.2: the sentence explaining the $34$ wins (within a supersession triple the count table differs only in the superseded column of the target's category, which the category-aware reader does not read and the category-guessing reader's share includes; AUX-WP-B-ORDERING: $0$ / $88$ / $0$ and $34$ / $54$ / $0$), and the sentence printing that share at the manifest category: $0.8473$ whole set, $0.8981$ / $0.7336$ / $0.8528$ per state, a privileged post hoc reader above GPT-4.1 mini, Haiku 4.5 and Opus 5 (AUX-R110-A1-CR, CR-oracle-share, v2 row, persona interval $[0.8071,0.8873]$); tab:cf-cr gains that row, labelled post hoc and privileged, and its caption describes the category-guessing reader's quantity as the share and the new row. "
            "The Section 5 clause \"A count reader given the question's category scores $0.85$ on the whole set from the count table alone\" is drafted (group `cr_clause`) and not landed: its page cost on the scratch build is 0 at the fine number.",
        ],
        "added": {   # numeric_diff ADDED tokens -> disposition
            "0.7336": "reviews/NUMBERS_R110.md AUX-R110-A1-CR: CR-oracle-share, v2, retraction (Appendix C.2 prose and tab:cf-cr; R118-3)",
            "0.8071": "reviews/NUMBERS_R110.md AUX-R110-A1-CR: CR-oracle-share, v2, whole-set persona interval, lower (tab:cf-cr; R118-3)",
            "0.8473": "reviews/NUMBERS_R110.md AUX-R110-A1-CR: CR-oracle-share, v2, whole set (Appendix C.2 prose and tab:cf-cr; R118-3)",
            "0.8528": "reviews/NUMBERS_R110.md AUX-R110-A1-CR: CR-oracle-share, v2, expiry (Appendix C.2 prose and tab:cf-cr; R118-3)",
            "0.8873": "reviews/NUMBERS_R110.md AUX-R110-A1-CR: CR-oracle-share, v2, whole-set persona interval, upper (tab:cf-cr; R118-3)",
            "0.8981": "reviews/NUMBERS_R110.md AUX-R110-A1-CR: CR-oracle-share, v2, supersession (Appendix C.2 prose and tab:cf-cr; R118-3)",
        },
        "vanished": {},
    },
    "payers": {
        "groups": "payer_e4,payer_c2",
        "entries": [
            "- **R118-4 [the payers of the landing map, the author's ruling 6 of 19 September and ruling 2 on REPORT_R118_A; `r118_apply.py` groups `payer_e4`, `payer_c2`]** (recorded). "
            "Section 9's paragraph moved whole to Appendix E.10 after tab:ds-a7: its two content sentences \"A header naming the persona and the date raises in-view correct answers reliably for both answerers.\" and \"A composite over all three jobs rises under the model rule by a reliable $+0.03$ for GPT-4.1 mini and stays level for Haiku 4.5 (Table~\\ref{tab:ds-a7}).\" (MOVED, words unchanged) and its pointer sentence, Before: \"Two further results are in Appendix~\\ref{app:resp}.\" After: (deleted; self-referential once the paragraph sits in that appendix). "
            "Section 5's two sentences moved to the head of Appendix C.2: Before: \"Opus 5's first draw alone keeps that margin (Appendix~\\ref{app:counterfactual}).\" After, at C.2: \"Opus 5's first draw alone keeps its margin over the name lookup on the whole set.\" (the antecedent named, the self-pointer dropped; AUX-R104-MARGIN); and \"Scored post hoc against the PRESENT versions alone, which also hold relevant content, every reader moves by at most $0.03$ from its whole-set value, so the comparison stands where coverage is equal.\" (MOVED, words unchanged; AUX-WP-B-PNPRESENT). No number changed.",
        ],
        "added": {}, "vanished": {},
    },
    "e5": {
        "groups": "e5,fig3",
        "entries": [
            "- **R118-5 [E5, GPT-5.6 Sol and Luna on the 444 (ADDENDUM_CF2_OPENAI.md, frozen at 177697a; r82_counterfactual/NUMBERS_CF2.md section 13, AUX-CF2-OAI-*; P-S1 held, P-S2 failed); the author's R117 ruling 3 and rulings 3 of 19 September and on REPORT_R118_A (directions (i) and (ii), gap form, models named); `r118_apply.py` groups `e5`, `fig3`]** (recorded). "
            "Abstract, Before: \"With one question asked of three store versions, GPT-4.1 mini and Haiku 4.5 do not exceed a similarity lookup over the list, and Opus 5 exceeds it by $0.07$.\" After: \"With one question asked of three store versions, no model reliably exceeds a similarity lookup over the list on the state the list names. On the whole set GPT-4.1 mini and Haiku 4.5 do not exceed that lookup, and Opus 5, GPT-5.6 Sol and GPT-5.6 Luna do, by $0.07$ to $0.08$, a margin that comes from the states the summary only counts.\" (the OpenReview abstract field is the author's). "
            "Section 1, the thesis sentence: \"For the three models tested on the summary alone\" becomes \"For the five models tested on the summary alone\" (the sentence is replaced whole at the E1 landing, R118-10). "
            "Section 1, bullet 3, Before: \"We show that attribute names carry most of the monitors' signal: the name lookup matches two of three models, and the count interventions do not establish count use for retracted and expired content.\" After: \"We show that attribute names carry most of the monitors' signal: the name lookup matches two of five models, and three exceed it by $0.07$ to $0.08$ through the states the summary only counts. The count interventions do not establish count use for retracted and expired content.\" "
            "Section 5, Before: \"On the counterfactual set, GPT-4.1 mini and Haiku 4.5 do not exceed the name lookup and Opus 5 exceeds it by $0.07$ (Table~\\ref{tab:cf-main}).\" After: \"On the counterfactual set no model reliably exceeds the name lookup on supersession, the state the list names (Appendix~\\ref{app:counterfactual}). The lookup is not exceeded on the whole set by GPT-4.1 mini or Haiku 4.5, while Opus 5, GPT-5.6 Sol and GPT-5.6 Luna exceed it by $0.07$ to $0.08$, a margin on the states the summary only counts (Table~\\ref{tab:cf-main}).\" (the supersession-only margins over the lookup, reviews/r117/results/sup_margins.json: GPT-4.1 mini $-0.0915$ reliably below, Haiku 4.5 $-0.0347$, Opus 5 $+0.0102$, Sol $+0.0161$, Luna $+0.0204$, the last four with both intervals including zero; the whole-set margins Sol $+0.0836$ and Luna $+0.0754$, both reliable). "
            "Table 1: the rows \"GPT-5.6 Sol, sup. only\" $0.85$ $[0.81,0.88]$ $0.85$ $126/2/20$ and \"GPT-5.6 Luna, sup. only\" $0.84$ $[0.80,0.88]$ $0.85$ $129/2/17$ after \"Opus 5, all three\" (AUX-CF2-OAI-SOL-V2, -LUNA-V2, -PNPRESENT). "
            "Conclusion, Before: \"The models draw most of their signal from a lifecycle summary's attribute names, and a name lookup over a clean list is not exceeded by two of the three.\" After: \"The models draw most of their signal from a lifecycle summary's attribute names. On the state a clean list names, no model reliably exceeds a name lookup over it. Over the whole set two of the five, GPT-4.1 mini and Haiku 4.5, do not exceed that lookup; GPT-5.6 Sol, GPT-5.6 Luna and Opus 5 are above it by $0.07$ to $0.08$, on the states the summary only counts.\" "
            "Limitations, Before: \"One closed model family supplies the primary capability comparison, and two runs stopped at the budget on the full populations.\" After: \"Two closed vendors supply the capability comparison, no open-weights model was run on the counterfactual set, and two runs stopped at the budget on the full populations.\" "
            "Appendix A, tab:runs: the Sol and Luna counterfactual cells \"not run\" become \"ran\"; caption \"three models ran on the counterfactual set\" becomes \"five models ran on the counterfactual set\". Appendix C.2, tab:pnpresent: the Sol and Luna blocks (whole and per state) before the name-lookup block (AUX-CF2-OAI-PNPRESENT). "
            "Figure 3, left panel: GPT-5.6 Sol and GPT-5.6 Luna as markers beside each state's Opus 5 bar at their per-state values (whole $0.8500$ / $0.8417$, supersession $0.9383$ / $0.9426$, retraction $0.5322$ / $0.5458$, expiry $0.6403$ / $0.6167$), two legend entries, and the caption's added sentence \"The two markers on the left are GPT-5.6 Sol and GPT-5.6 Luna, which ran the default summary only.\" The optional per-state sentence of HELD_TEXTS_R117 does not land (direction (i) covers it).",
        ],
        "added": {}, "vanished": {},
    },
    "e2": {
        "groups": "e2",
        "entries": [
            "- **R118-6 [E2, names against counts on the 444 (ADDENDUM_CF2_NAMES_COUNTS.md, frozen at 177697a; r82_counterfactual/NUMBERS_CF2.md section 12, AUX-CF2-NC-*; P-N1 and P-N2 held); the author's R117 ruling 3; `r118_apply.py` group `e2`]** (recorded). "
            "Section 5, after the own-name ablation's Haiku sentence, new: \"Removing every count from the summary leaves both readers within tolerance of the intact summary, and removing the names instead puts both a reliable $0.12$ and $0.16$ below the names-only summary (Appendix~\\ref{app:counterfactual}).\" (GPT-4.1 mini and Haiku 4.5; P-N1: names only minus intact $-0.0064$ and $-0.0059$, within tolerance; P-N2: counts only minus names only $-0.1242$ and $-0.1562$, both intervals excluding zero; AUX-CF2-NC-P-N1, -P-N2, -MINI-*, -H45-*). "
            "Appendix C.2, after tab:v2rcat: tab:cf-names-counts (per reader the intact recorded row, names only, counts only, and for GPT-4.1 mini the dash-rule form; AUROC with the persona interval, minus intact with both intervals, retraction and expiry; the caption states that P-N1 and P-N2 held and records the identity correction AUX-CF2-NC-IDENTITY). No frozen string changed.",
        ],
        "added": {}, "vanished": {},
    },
    "e3": {
        "groups": "e3,e3_u5",
        "entries": [
            "- **R118-7 [E3, the marker ablation on Mem0 and A-MEM (ADDENDUM_MARKER_ABLATION.md, frozen at 177697a; e1_metamemory/NUMBERS.md section 12, AUX-MARKER-*; P-X2 failed on Mem0, held on A-MEM); the author's R117 ruling 3; `r118_apply.py` group `e3`]** (recorded). "
            "Section 7, Before: \"Under it GPT-4.1 mini loses $0.10$ on Mem0 and $0.11$ on A-MEM, and on the pooled $66$ questions of both stores GPT-5.6 Luna loses $0.34$ and GPT-5.6 Sol $0.10$, every interval excluding zero$^{h}$.\" After: \"Under it GPT-4.1 mini loses $0.10$ on Mem0 and $0.11$ on A-MEM, and on the pooled $66$ questions of both stores GPT-5.6 Luna loses $0.29$ through the raw API and GPT-5.6 Sol $0.10$$^{h}$, every interval excluding zero.\" followed by \"The loss survives omitting or rewording the marker on Mem0, and for GPT-5.6 Luna it appears under every rendering, $0.27$ to $0.34$, so the marker's wording is not the cause (Appendix~\\ref{app:inversion}).\" (Luna's harness number replaced by the raw-API structural-minus-blind reading $-0.2926$ and its marker dropped; Sol's $0.10$ keeps the marker; Luna raw API: neutral $-0.2671$, structural $-0.2926$, omitted $-0.3366$ against blind; GPT-4.1 mini neutral on Mem0 $-0.0722$ against blind, both intervals excluding zero, the failed P-X2; A-MEM within tolerance). "
            "Appendix E.7: the sentence closing the distribution paragraph gains \"; the marker's wording is not it (Table~\\ref{tab:marker})\"; tab:marker after tab:dist (GPT-4.1 mini on Mem0 and A-MEM under blind, structural, omitted (the recorded arm) and neutral; GPT-5.6 Luna raw API on the 66, four arms; the recorded harness rows beside, marked $^{h}$).",
            "- **R118-8 [U5, C090, the Limitations sentence pinned byte-identical; the author's ruling 5 of 19 September and ruling 3 on REPORT_R118_A (the four conditions); `r118_apply.py` group `e3_u5`]** (recorded). "
            "Before: \"The structureless-store inversion is measured across scales, but its below-chance mechanism remains unresolved.\" After: \"The structureless-store inversion is measured across scales, and neither omitting the marker nor rewording it removes the Mem0 loss; GPT-5.6 Luna, through the raw API, loses $0.27$ to $0.34$ under every rendering. The marker's wording is therefore not the cause, and the below-chance mechanism remains unresolved.\" (the inversion claim kept; the Mem0 loss survives omitting and rewording; the raw-API Luna range; no cause claimed beyond the marker's wording; slogan_scan's pinned fragment \"below-chance mechanism remains unresolved\" occurs once).",
        ],
        "added": {}, "vanished": {},
    },
    "e4": {
        "groups": "e4",
        "entries": [
            "- **R118-9 [E4, label propagation inside the view (ADDENDUM_DS_AMENDMENT_8.md, frozen at 177697a; ds_downstream/NUMBERS_DS.md section 15, AUX-DS-A8-*; P-L1, P-L3, P-L5 failed, P-L2 held; D-DS-A8-1); the author's R117 ruling 3; `r118_apply.py` group `e4`]** (recorded). "
            "Section 9, after the Haiku residual sentence, new: \"A view-only rule propagating a line's tag to same-attribute lines that repeat it at the census threshold changes $1$ of $452$ views: $187$ of the $272$ stale lines sit under a different attribute key from their tagged twin (Appendix~\\ref{app:resp}).\" "
            "Appendix E.10, after tab:ds-a7 and the moved Section 9 paragraph: tab:ds-a8 (views changed, lines propagated, audited duplicate items fully tagged, false propagation, under ground-truth and own tags, primary and secondary; the own-tag re-answers per policy for both answerers), its caption carrying the diagnosis ($187$ of $272$ stale lines under a different attribute key; $45$ and $40$). No cross-key variant designed or run. No frozen string changed.",
        ],
        "added": {"0.13%": "ds_downstream/NUMBERS_DS.md section 15, AUX-DS-A8-FALSEPROP: 3 of 2333 under ground-truth tags, primary and secondary (tab:ds-a8; R118-9)",
                  "2.96%": "ds_downstream/NUMBERS_DS.md section 15, AUX-DS-A8-FALSEPROP: 69 of 2333 under own tags, primary; P-L5 failed at or under 5% (tab:ds-a8; R118-9)",
                  "3.56%": "ds_downstream/NUMBERS_DS.md section 15, AUX-DS-A8-FALSEPROP: 83 of 2333 under own tags, secondary (tab:ds-a8; R118-9)"}, "vanished": {},
    },
    "e1": {
        "groups": "e1",
        "entries": [
            "- **R118-10 [E1, Opus 5 at five draws on the moved-count texts (ADDENDUM_V2R_CAT_AMENDMENT_1.md, frozen at 177697a; r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md section 9, AUX-V2RCAT-A1-*; P-M1 held); the registration's HOLDS branch; the author's ruling 4 on REPORT_R118_A (every site names the three models given the moved-count control; L111 takes the landing map's sentence); `r118_apply.py` group `e1`]** (recorded). "
            "Section 5, Before: \"Opus 5, run once per item against its five-draw row, moves $-0.10$ on retraction and $-0.12$ on expiry, both intervals excluding zero.\" After: \"Opus 5, at five draws against its five-draw row, moves $-0.10$ on retraction and $-0.13$ on expiry, both intervals excluding zero.\" (five-draw V2R-CAT $0.8075$ against v2 $0.8405$, $-0.0330$; retraction $-0.1003$, expiry $-0.1281$, both intervals excluding zero; five-draw minus draw-1 $+0.0026$, intervals including zero). "
            "Section 5, Before: \"Names carry most of the observed signal; Opus 5 also responds to moved counts.\" After: \"Names carry most of the observed signal; of the three models given the moved-count control, only Opus 5 responds to it.\" "
            "Conclusion, Before: \"Only Opus 5 responds to a moved count.\" After: \"Of the three models given the moved-count control, only Opus 5 responds.\" "
            "Section 1, the thesis sentence, Before: \"For the five models tested on the summary alone, the attribute names carry most of the signal, and no count intervention establishes consistent count use (Section~\\ref{sec:counterfactual}).\" After, the landing map's candidate: \"The summary carries each label twice, as a name or as a count; the models use the names and barely use the counts, and the states they miss when counted they detect once named (Section~\\ref{sec:counterfactual}).\" "
            "Section 1, bullet 3, Before: \"The count interventions do not establish count use for retracted and expired content.\" After: \"The count interventions, run on GPT-4.1 mini, Haiku 4.5 and Opus 5, do not establish count use for retracted and expired content.\" "
            "Appendix C.2, tab:v2rcat: Opus 5's rows read $k=5$ ($0.8075$; retraction $0.4869$, expiry $0.4869$; the differences with both intervals) with the draw-1 rows kept beside them; the caption records that this row, unlike the others, was registered with a prediction, which held.",
        ],
        "added": {}, "vanished": {"-0.12": "Section 5's Opus sentence: the draw-1 expiry movement $-0.1236$ printed as $-0.12$ is replaced by the five-draw $-0.1281$, printed $-0.13$ (AUX-V2RCAT-A1-OP5-K5; R118-10)"},
    },
    "notation_clause": {
        "groups": "notation,cr_clause",
        "entries": [
            "- **R118-11 [the notation box and the Section 5 count-reader clause; the author's ruling 5 on REPORT_R118_A]** (recorded). "
            "Notation box: the row \"named state; counted state\" dropped (0 and 2 uses in the body prose); \"reads\" dropped from the verbs row (0 uses in the defined sense), which now reads \"names, counts\"; \"all-states lookup\" dropped from the lookup row, its one use defined inline, Section 5, Before: \"The all-states lookup scores $0.88$ on the whole set, and Haiku 4.5 gains a reliable $+0.30$ on the two counted states once they are named.\" After: \"The same lookup over a list naming all three non-active states scores $0.88$ on the whole set, and Haiku 4.5 gains a reliable $+0.30$ on the two counted states once they are named.\" "
            "Section 5, after the count readers' numbers sentence, new: \"A count reader given the question's category, a privileged reader computed post hoc, scores $0.85$ on the whole set from the count table alone (Appendix~\\ref{app:counterfactual}).\" (AUX-R110-A1-CR, CR-oracle-share $0.8473$).",
        ],
        "added": {"0.85": "reviews/NUMBERS_R110.md AUX-R110-A1-CR: CR-oracle-share, v2, whole set 0.8473 printed at two decimals (Section 5; R118-11); also the E5 rows of Table 1 (Sol 0.8500)"}, "vanished": {},
    },
    "read1": {
        "groups": "read1",
        "entries": [
            "- **R118-13 [the author's read of paper_v21.pdf at fc42d2d, 19 September: five items and the Limitations payers of the landing map; `r118_apply.py` group `read1`]** (recorded). "
            "(1) Section 1, contribution 3, Before: \"the name lookup matches two of five models, and three exceed it by $0.07$ to $0.08$ through the states the summary only counts. The count interventions, run on GPT-4.1 mini, Haiku 4.5 and Opus 5, do not establish count use for retracted and expired content.\" After: \"the name lookup is not exceeded by two of five models, and three exceed it by $0.07$ to $0.08$ through the states the summary only counts. Of the three models given the count interventions, only Opus 5 responds to a moved count.\" Section 5, first sentence, Before: \"the count interventions do not establish that it tracks the counts.\" After: \"of the three models given the count interventions, only Opus 5 tracks the counts.\" (repeat_scan and the near-duplicate rule pass on the built paper.) "
            "(2) Section 4, the roster, Before: \"GPT-4.1 mini ran the main study at one call per question, Opus 5, Haiku 4.5 and GPT-5.6 Luna ran every population at five calls, and GPT-5.6 Sol and Kimi K3 ran the cross-model set only (Table~\\ref{tab:setup}).\" then \"The GPT-5.6 cross-model rows are harness rows (Appendix~\\ref{app:laddertable}).\" After: \"GPT-4.1 mini ran the main study at one call per question, and Opus 5, Haiku 4.5 and GPT-5.6 Luna ran every population at five calls (Table~\\ref{tab:setup}).\" then \"GPT-5.6 Sol ran the cross-model set and, through the raw API, the counterfactual set; Kimi K3 ran the cross-model set only.\" then \"The GPT-5.6 cross-model rows are harness rows; their counterfactual rows are raw-API (Appendix~\\ref{app:laddertable}).\" (the harness disclosure paragraph is in Appendix A, app:laddertable, before tab:ladder-exact; the pointer's letter confirmed against the build.) "
            "(3) Section 5, Before: \"where every model scores $0.53$ to $0.62$\" After: \"where every model scores $0.53$ to $0.64$\": the range over the five models on retraction and expiry (GPT-4.1 mini $0.5283$ / $0.5489$, Haiku 4.5 $0.5433$ / $0.5794$, Opus 5 $0.5872$ / $0.6150$, GPT-5.6 Sol $0.5322$ / $0.6403$, GPT-5.6 Luna $0.5458$ / $0.6167$; AUX-CF2-PERSTATE, AUX-CF2-OAI-SOL-V2, -LUNA-V2). The abstract's and Figure 3's statement that every model discriminates more weakly than the count reader on the counted states holds for both: the category-guessing reader reads $0.6669$ on retraction and $0.6872$ on expiry, above every model's value, and the category-aware reader $0.7306$ and $0.7778$. "
            "(4) Section 5, the privileged reader sentence, Before: \"A count reader given the question's category, a privileged reader computed post hoc, scores $0.85$ on the whole set from the count table alone (Appendix~\\ref{app:counterfactual}).\" After: \"A reader given the question's category that reads the share of its entries no longer active, superseded included (privileged, post hoc), scores $0.85$ on the whole set from the count table alone (Appendix~\\ref{app:counterfactual}).\" "
            "(5) Section 5, the E2 sentence: \"leaves both readers within tolerance\" becomes \"leaves GPT-4.1 mini and Haiku 4.5 within tolerance\". "
            "Payers: the Limitations sentence \"Beyond the store's own name pool, a mean of $99$ names, the lookup is tested only with other personas' names.\" moved whole to Appendix C.2 after the store's-own-pool sentence (R113-4's sentence, MOVED); the Limitations opening, Before: \"The primary evidence comes from synthetic stores and FR-Bank, the benchmark's lifecycle backend \\citep{fr}.\" then \"The added Graphiti evaluation extends implementation coverage using the same synthetic personas.\" After, the landing map's text: \"Lifecycle ground truth (which record replaced which, what was never stored) is unobservable in real user data, so the stores are synthetic.\" then \"The counterfactual test scores ground-truth summaries and depends on no backend's write path; FR-Bank and Graphiti are scored on the same personas.\" (neither old sentence is a frozen fragment: no CLAIMS quote, registration, U block or slogan pin carries them).",
        ],
        "added": {"0.64": "r82_counterfactual/cf2/NUMBERS_CF2.md section 13, AUX-CF2-OAI-SOL-V2: GPT-5.6 Sol on expiry 0.6403, the top of the five-model range on the counted states (Section 5; R118-13)"},
        "vanished": {"0.62": "Section 5's range over the three recorded models on the counted states (Opus 5 on expiry 0.6150) replaced by the five-model range ending at GPT-5.6 Sol's 0.6403 (R118-13); 0.62 stays where it is the count of tagged lines (Section 9)"},
    },
    "e1_fix": {   # no groups: the two E1 strings were corrected in place (r118_apply's group e1 carries the corrected forms)
        "groups": "",
        "entries": [
            "- **R118-12 [correction of R118-10, and the frozen quote R118-11 lacked]** (recorded). The R118-10 commit (5c1be2e) reported every gate passing; two were not: prose_scan rule G4 (Section 1's reader-claim anchor must precede its first mention of tags, and the landing map's sentence did not match the anchor, so the anchor fell to the bullet after the route sentence) and rule D (the Section 5 and Conclusion moved-count sentences were near-duplicates at 89 percent). The gate driver read only the words FAIL and missing and missed a finding printed without them; it now fails any gate line that does not say PASS. "
            "Corrections: Section 1, Before: \"The summary carries each label twice, as a name or as a count; the models use the names and barely use the counts, and the states they miss when counted they detect once named (Section~\\ref{sec:counterfactual}).\" After: \"The summary carries each label twice, as a name or as a count; the models read the names and barely read the counts, and the states they miss when counted they detect once named (Section~\\ref{sec:counterfactual}).\" (the one-word change that satisfies the anchor rule without editing it; the author's verbatim sentence is shown as the alternative in the landing report). "
            "Conclusion, Before: \"Of the three models given the moved-count control, only Opus 5 responds.\" After: \"Of GPT-4.1 mini, Haiku 4.5 and Opus 5, the three given the moved-count control, only Opus 5 responds.\" (names the three; no longer a near-duplicate of the Section 5 sentence). "
            "R118-11's notation-box row, Before: \"names, counts, reads & a summary \\emph{names} a state when it lists the attribute names in that state and \\emph{counts} it when it gives only a count of it; a reader \\emph{reads} a state when its score separates that state's items from the rest\" After: \"names, counts & a summary \\emph{names} a state when it lists the attribute names in that state and \\emph{counts} it when it gives only a count of it\".",
        ],
        "added": {}, "vanished": {},
    },
}


def append_entries(entries):
    for path, nl in ((CLAIMS, "\r\n"), (BLOCK, "\n")):
        raw = path.read_bytes().decode("utf-8")
        assert "## R118 AUTHORIZATION BLOCK" in raw
        assert raw.rstrip("\r\n").endswith(")") or raw.rstrip("\r\n").endswith(".") , path
        body = raw.replace("\r\n", "\n")
        new = [e for e in entries if e.split("]**")[0] not in body]
        if not new:
            print(f"  {path.name}: entries already present"); continue
        if not body.endswith("\n"):
            body += "\n"
        body += "\n".join(new) + "\n"
        path.write_bytes(body.replace("\n", nl).encode("utf-8"))
        print(f"  {path.name}: appended {len(new)} entries")


def add_dispositions(added, vanished):
    src = NM.read_text(encoding="utf-8")
    for name, d in (("ADDED", added), ("VANISHED", vanished)):
        if not d:
            continue
        m = re.search(r"^%s = \{[^\n]*\n" % name, src, flags=re.M)
        assert m, name
        lines = "".join(f"    {k!r}: {v!r},\n" for k, v in d.items() if f"    {k!r}:" not in src)
        src = src[:m.end()] + lines + src[m.end():]
    NM.write_text(src, encoding="utf-8", newline="\n")
    print("  number_moves_wp.py: dispositions written")


def main():
    step = STEPS[sys.argv[1]]
    if step["groups"]:
        r = subprocess.run([PY, str(V21 / "tools" / "r118_apply.py"), "--only", step["groups"]], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        print(r.stdout.strip()[-1500:]); assert "written" in r.stdout, r.stderr[-800:]
    append_entries(step["entries"])
    add_dispositions(step["added"], step["vanished"])
    if "--no-moves" not in sys.argv:      # the number-moves ledger is regenerated after the build (run_gates builds paper_v21.tex first)
        r = subprocess.run([PY, str(V21 / "tools" / "build_v21.py")], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        assert r.returncode == 0, r.stdout[-800:] + r.stderr[-800:]
        r = subprocess.run([PY, str(NM)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        print("  " + (r.stdout.strip().splitlines() or ["(no output)"])[-1])


if __name__ == "__main__":
    main()
