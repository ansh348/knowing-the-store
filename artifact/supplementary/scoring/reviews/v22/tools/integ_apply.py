# -*- coding: utf-8 -*-
"""integ_apply.py -- the integration pass of 2026-09-16 (program R112): asserted replacements in reviews/v19/src/{abstract,body,appendix}_v19.tex.
Each entry is (file, old, new, count); the script asserts the count before replacing and never touches a frozen registered line.
Sources: the author's corrections of 2026-09-16 (six points), review2_cc_prompt.md D/E/F, v19_prompt.md Step 3 (R1-R8), the post-hoc results
(reviews/v19/results/posthoc_*.json; reviews/NUMBERS_WP.md sections 7-10) and the forty-persona Graphiti census (r85_graphiti/NUMBERS_R85.md).
Run from the repository root: python reviews/v19/tools/integ_apply.py   (idempotent: a second run finds the new strings and stops)
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v19" / "src"
A, B, X = SRC / "abstract_v19.tex", SRC / "body_v19.tex", SRC / "appendix_v19.tex"

E = []  # (file, old, new)


def rep(f, old, new):
    E.append((f, old, new))


# ============================================================ abstract (R1; D1; the author's points 3 and 4)
rep(A, "We find that models read the summary by its names, not by its counts. Where the summary names the stale attribute, a similarity lookup over the list matches every model but the largest (three models, one question asked of three store versions). Where the summary only counts a state, no model reads the count, and naming that state lifts every model. Returning non-active records with their lifecycle tags, instead of masking them, is a second route that covers what the list misses.",
    "We find that the attribute names carry most of the observed signal, and the count interventions do not establish consistent count use. Where the summary names the stale attribute, a similarity lookup over the list matches every model but the largest (three models, one question asked of three store versions). Where the summary only counts a state, no tested model separates the store versions, and naming that state lifts every model. Returning non-active records with their lifecycle tags, instead of masking them, is a second route, at retrieval time, that covers what the list misses.")
rep(A, "Downstream, gating retrieval on the judgment reaches more forbidding records but does not reduce stale answers, because the store keeps untagged duplicates of superseded content. Tagging those duplicates removes most of the stale answers, so the fix is in the write path. Backends should return tags, not masks, and maintain the list.",
    "Downstream, gating retrieval on the judgment reaches more of the records the agent must not use but does not reduce detector-flagged stale answers, because the store keeps untagged duplicates of superseded content. Reference-assisted retagging of those duplicates reduced detector-flagged stale responses, which points to the write path; human validation of the detector is pending. Backends should return tags, not masks, and maintain the list.")

# ============================================================ Section 1
rep(B, "The three models tested on the summary alone read it by its names and not by its counts (Section~\\ref{sec:counterfactual}).\nRoute A is that summary; route B is unmasked retrieval, returning non-active records with their tags.",
    "For the three models tested on the summary alone, the attribute names carry most of the signal, and the count interventions do not establish consistent count use (Section~\\ref{sec:counterfactual}).\nRoute A is that summary, read before any retrieval; route B is unmasked retrieval whose returned records keep their tags and are read at retrieval time.")
rep(B, "\\item We show monitors read names, not counts: the name lookup matches two of three models, and no model reads a state the summary only counts (retracted and expired).",
    "\\item We show that attribute names carry most of the monitors' signal: the name lookup matches two of three models, and the count interventions do not establish count use for the states the summary only counts (retracted and expired).")
rep(B, "\\item We show that retrieval returning non-active records \\emph{with their tags} is a second route to the obligation, and no tested backend writes a usable list.",
    "\\item We show that retrieval returning non-active records \\emph{with their tags} is a second route to the obligation, read at retrieval time, and no tested backend writes a usable list.")
rep(B, "\\item We show that gating retrieval on the judgment reaches more forbidding records but does not reduce stale answers; tagging the store's untagged duplicates does.",
    "\\item We show that gating retrieval on the judgment reaches more forbidding records but does not reduce detector-flagged stale answers; reference-assisted retagging of the store's untagged duplicates does.")
# Figure 1 (D1)
rep(B, "{\\textbf{route B: the tags}, top-$k$ retrieval with no mask, lines keep their tags:\\\\ \\texttt{[2] superseded trip\\_plan}\\\\ \\texttt{[3] retracted hike\\_sat}};",
    "{\\textbf{route B: the tags}, at retrieval: top-$k$ with no mask, returned lines keep their tags:\\\\ \\texttt{[2] superseded trip\\_plan}\\\\ \\texttt{[3] retracted hike\\_sat}};")
rep(B, "{\\textbf{monitor}\\\\ a lookup or a model\\\\ emits FOK and NOK before any content is retrieved};",
    "{\\textbf{monitor}\\\\ a lookup or a model\\\\ emits FOK and NOK: route A before any retrieval, route B on the returned records};")
rep(B, "\\caption{The framework: a tagged store (grey rows non-active), route A (the summary) and route B (the tags) to a monitor that emits FOK and NOK before retrieval, and masked retrieval with no route.}",
    "\\caption{The framework: a tagged store (grey rows non-active), route A (the summary, read before any retrieval) and route B (the tags on the returned records, read at retrieval time) to a monitor that emits FOK and NOK, and masked retrieval with no route.}")

# ============================================================ Section 2 (R6)
rep(B, "Reliance on obsolete memory \\citep{memora}, conflict resolution across turns \\citep{memoryagentbench} and, closest to this paper, recognition that a memory the agent holds is no longer valid, STALE \\citep{stale}, are scored after retrieval too.",
    "Reliance on obsolete memory \\citep{memora} and conflict resolution across turns \\citep{memoryagentbench} are scored after retrieval too.\nSTALE \\citep{stale}, the closest work, asks whether an agent can tell that a memory it has already retrieved is no longer valid; this paper asks whether the store holds such a memory before anything is retrieved.\nZep's validity intervals \\citep{zep} are lifecycle tags of the kind route B returns.")

# ============================================================ Section 3 (F2)
rep(B, "The lifecycle state is the tag a record carries, and the last three states are the non-active ones.",
    "The lifecycle state is the tag a record carries; expiry is a flag derived from the event-time anchor rather than a tag the store writes, so an expired record may still carry the active tag.\nA record is non-active when it is superseded, retracted or expired, and a record carrying more than one mark is labelled by the first of retracted, superseded, expired (Appendix~\\ref{app:glossary}).")
rep(B, "route A; route B & the summary route; the tag route, retrieval without a mask that returns non-active records with their tags (Figure~\\ref{fig:framework}) \\\\",
    "route A; route B & the summary route, read before any retrieval; the tag route, retrieval without a mask whose returned records keep their tags, read at retrieval time (Figure~\\ref{fig:framework}) \\\\")

# ============================================================ Section 4 (R5; the provenance pointer)
rep(B, "Labels follow Definition~\\ref{def:coverage}, and every \\pn{} label was verified by hand.",
    "Labels follow Definition~\\ref{def:coverage}; the intent is fixed by the question's construction and used only to label, the monitor is never told it, and every \\pn{} label was verified by hand.")
rep(B, "Table~\\ref{tab:setup} names every population, and every later number is stated on one of them.",
    "Table~\\ref{tab:setup} names every population, every later number is stated on one of them, and Appendix~\\ref{app:provenance} traces each headline number to its labels, tag source and evaluator.")

# ============================================================ Section 5 (F3; the author's point 4; B1-B3; E)
rep(B, "When the question is fixed and only the store changes, the models' judgment tracks the attribute names in the summary, not the counts beside them.",
    "When the question is fixed and only the store changes, the models' judgment tracks the attribute names in the summary; the count interventions do not establish that it tracks the counts.")
rep(B, "Blind NOK is $0.50$ by construction on this set, and every AUROC below is also a gain against it.",
    "Blind NOK is $0.50$ by construction on this set, so each gain below is the AUROC minus that chance value.")
rep(B, "\\caption{Obligation AUROC on the counterfactual set ($n=444$; positives $88$ supersession, $30$ retraction, $30$ expiry), whole set; the per-state values are Figure~\\ref{fig:perstate}. Blind NOK is $0.50$ by construction, so each AUROC is also a gain; the interval is the persona-grouped interval of the AUROC; the item-level paired gain intervals are in Appendix~\\ref{app:counterfactual}.}",
    "\\caption{Obligation AUROC on the counterfactual set ($n=444$; positives $88$ supersession, $30$ retraction, $30$ expiry), whole set, with the persona-grouped interval of the AUROC; the per-state values are Figure~\\ref{fig:perstate}. Blind NOK is $0.50$ by construction, so the gain is the AUROC minus $0.50$. PN vs PRESENT and W/T/L are post hoc (Appendix~\\ref{app:counterfactual}); the item-level paired gain intervals are there too.}")
rep(B, "\\begin{tabular}{@{}lrl@{}}\n\\toprule\nReader, summary & AUROC & persona interval \\\\\n\\midrule\nGPT-4.1 mini, sup.\\ only & $0.72$ & $[0.67,0.76]$ \\\\\nGPT-4.1 mini, all three & $0.80$ & $[0.74,0.85]$ \\\\\nHaiku 4.5, sup.\\ only & $0.76$ & $[0.71,0.80]$ \\\\\nHaiku 4.5, all three & $0.88$ & $[0.84,0.91]$ \\\\\nOpus 5, sup.\\ only & $0.84$ & $[0.80,0.88]$ \\\\\nOpus 5, all three & $0.91$ & $[0.88,0.94]$ \\\\\n\\midrule\n\\multicolumn{3}{@{}l}{\\textit{Readers with no model in them}}\\\\\nName lookup, sup.\\ only & $0.77$ & $[0.72,0.81]$ \\\\\nAll-states lookup, all three & $0.88$ & $[0.84,0.91]$ \\\\\nCategory-guessing count reader, sup.\\ only & $0.66$ & $[0.63,0.70]$ \\\\\nCategory-aware count reader, sup.\\ only & $0.60$ & $[0.58,0.64]$ \\\\\n\\bottomrule",
    "%% R112 (2026-09-16), post hoc: the PN vs PRESENT column and the W/T/L column from reviews/NUMBERS_WP.md section 8 (AUX-WP-B-PNPRESENT, -B-ORDERING; two-decimal forms ledgered there).\n\\begin{tabular}{@{}lrlrl@{}}\n\\toprule\nReader, summary & AUROC & persona interval & PN vs PRESENT & W/T/L \\\\\n\\midrule\nGPT-4.1 mini, sup.\\ only & $0.72$ & $[0.67,0.76]$ & $0.71$ & $81/57/10$ \\\\\nGPT-4.1 mini, all three & $0.80$ & $[0.74,0.85]$ & $0.78$ & $105/32/11$ \\\\\nHaiku 4.5, sup.\\ only & $0.76$ & $[0.71,0.80]$ & $0.75$ & $89/52/7$ \\\\\nHaiku 4.5, all three & $0.88$ & $[0.84,0.91]$ & $0.87$ & $125/18/5$ \\\\\nOpus 5, sup.\\ only & $0.84$ & $[0.80,0.88]$ & $0.84$ & $128/3/17$ \\\\\nOpus 5, all three & $0.91$ & $[0.88,0.94]$ & $0.91$ & $139/0/9$ \\\\\n\\midrule\n\\multicolumn{5}{@{}l}{\\textit{Readers with no model in them}}\\\\\nName lookup, sup.\\ only & $0.77$ & $[0.72,0.81]$ & $0.77$ & $82/66/0$ \\\\\nAll-states lookup, all three & $0.88$ & $[0.84,0.91]$ & $0.87$ & $121/27/0$ \\\\\nCategory-guessing count reader, sup.\\ only & $0.66$ & $[0.63,0.70]$ & $0.64$ & $65/83/0$ \\\\\nCategory-aware count reader, sup.\\ only & $0.60$ & $[0.58,0.64]$ & $0.59$ & $60/88/0$ \\\\\n\\bottomrule")
rep(B, "On the counterfactual set, GPT-4.1 mini and Haiku 4.5 do not exceed the name lookup and Opus 5 exceeds it by $0.07$ (Table~\\ref{tab:cf-main}).\nWhat the list does not name, no model reads.",
    "On the counterfactual set, GPT-4.1 mini and Haiku 4.5 do not exceed the name lookup and Opus 5 exceeds it by $0.07$ (Table~\\ref{tab:cf-main}).\n%% R112 (2026-09-16), post hoc B1-B3 (reviews/NUMBERS_WP.md section 8): the largest move from the pooled AUROC is 0.0230; the coverage-only reference is 0.75 pooled and ties every triple.\nScored against the PRESENT versions alone, which also hold relevant content, every reader moves by at most $0.03$ from its whole-set value, so the comparison stands where coverage is equal (post hoc; PN vs PRESENT and the wins, ties and losses per triple in Table~\\ref{tab:cf-main}).\nA reader that only knows whether the store covers the question would score $0.75$ on the whole set and tie every triple.")
rep(B, "The retracted and expired states are recoverable from the count table, but no model recovers them.",
    "The retracted and expired states are recoverable from the count table, but no tested model recovers them.")
rep(B, "No model follows the counts: permuting the lifecycle totals across the store versions moves none of them by more than $0.01$.\nMoving the obligation's own increment to a sibling version, the moved-count control, sends a count reader below chance and moves no model (Appendix~\\ref{app:counterfactual}).",
    "Permuting the lifecycle totals across the store versions moves no tested model by more than $0.01$.\n%% R112 (2026-09-16), review-2 item E (the author's form, one interval in prose under Q-B): AUX-V2RCAT-MINI expiry +0.0611 [-0.0404, +0.1641] / [-0.0217, +0.1417]; Haiku 4.5 -0.0072 / -0.0453; Opus 5 not run.\nMoving the obligation's own increment to a sibling version, the moved-count control, sends a count reader below chance; GPT-4.1 mini moves $+0.06$ on expiry with interval $[-0.04,+0.16]$, Haiku 4.5 stays within tolerance (Appendix~\\ref{app:counterfactual}), and Opus 5 was not run on this control.\nUnder the tested prompts the names carry the judgment, and the count representations tested carry no signal we can detect.")

# ============================================================ Section 6 (D1; the retriever swap)
rep(B, "A retriever that returns non-active records with their tags is a second route to the obligation (route B in Figure~\\ref{fig:framework}).",
    "A retriever that returns non-active records with their tags is a second route to the obligation, read at retrieval time from the returned records (route B in Figure~\\ref{fig:framework}).")
rep(B, "The retriever is FR-Bank's own cosine search with its lifecycle mask off, a modification of the stock configuration, and each returned line carries the ground-truth tag (Appendix~\\ref{app:resp}).",
    "The retriever is FR-Bank's own cosine search with its mask off, each line carrying the ground-truth tag (Appendix~\\ref{app:resp}).")

# ============================================================ Section 7 (the Graphiti census; the q_scan opener; clarity)
rep(B, "FR-Bank marks $5{,}968$ of its $18{,}936$ entries inactive, and the ground-truth manifest explains about $102$ of those marks as supersessions, so the stale marks outnumber the true ones about $58\\times$.",
    "FR-Bank marks $5{,}968$ of its $18{,}936$ entries inactive, where the ground-truth manifest explains about $102$ of those marks as supersessions.")
rep(B, "A-MEM invents: all $23{,}186$ link references across its $11{,}319$ notes resolve to zero note identifiers (Table~\\ref{tab:census}).",
    "A-MEM invents: all $23{,}186$ link references across its $11{,}319$ notes resolve to zero note identifiers (Table~\\ref{tab:census}).\n%% R112 (2026-09-16): the forty-persona Graphiti census (r85_graphiti/NUMBERS_R85.md AUX-R85-G10-CENSUS-FORBIDDING-FULL 13 / 34 = 0.3824 on the FULL-variant obligations, the main-text reading under D-R85-16; precision 54 / 807 = 0.0669; the registered 30 / 74 and P1's text in Appendix G.4).\nOn Graphiti \\citep{zep}, a fourth backend whose validity intervals are the closest thing to lifecycle tags in a shipped store, a census over forty personas recovers some of the forbidding records.\nIts invalidation marks reach $13$ of the $34$ obligations of the full store that the ground truth marks superseded or expired, more than the quarter we had predicted, and $54$ of its $807$ non-active edges fall on such a record (Appendix~\\ref{app:posthoc-graphiti}).")
rep(B, "Where the store still writes the item's own name Haiku 4.5 scores it at its ground-truth level, and where it does not the model falls to the floor the own-name ablation found (Section~\\ref{sec:counterfactual}).",
    "Where the store still writes the item's own name, Haiku 4.5 scores as it does under the ground-truth summary; where the name is gone it falls to the level the own-name ablation produced (Section~\\ref{sec:counterfactual}).")
rep(B, "Under the constrained rendering GPT-4.1 mini loses $0.10$ on Mem0 and $0.11$ on A-MEM, and on the pooled $66$ questions of both stores GPT-5.6 Luna loses $0.34$ and GPT-5.6 Sol $0.10$, every interval excluding zero.",
    "The constrained rendering loses coverage on both structureless stores.\nUnder it GPT-4.1 mini loses $0.10$ on Mem0 and $0.11$ on A-MEM, and on the pooled $66$ questions of both stores GPT-5.6 Luna loses $0.34$ and GPT-5.6 Sol $0.10$, every interval excluding zero.")

# ============================================================ Section 8 (F1; the relabeled wording)
rep(B, "On the hard tier every coverage positive is an obligation, so that FOK row is the NOK row relabeled.}",
    "On the hard tier every coverage positive is an obligation, so that FOK row scores the same positives as the NOK row.}")
rep(B, "The coverage margin lives on ordinary records.\nOn the easy tier ($354$ questions), where the positives are ordinary present records, GPT-4.1 mini scores $0.78$ against the name lookup's $0.61$, a reliable margin of $+0.18$.\nOn the hard tier every coverage positive is an obligation, so the FOK row is the NOK row relabeled, and the lookup's $0.79$ against the model's $0.70$ is not a reliable difference (Appendix~\\ref{app:baselines}).",
    "The coverage margin over the name lookup does not survive a lookup over the whole name map.\nOn the easy tier ($354$ questions), where the positives are ordinary present records, GPT-4.1 mini scores $0.78$ against the name lookup's $0.61$, a reliable margin.\n%% R112 (2026-09-16), post hoc F1 (reviews/NUMBERS_WP.md section 10, AUX-WP-F1-WHOLEMAP): whole-map lookup 0.7469; model minus whole-map +0.0367 [-0.0127, +0.0861] / [-0.0036, +0.0776].\nA lookup over every name in the map, computed post hoc, scores $0.75$ on the same questions, and the model's margin over it is $+0.04$ with interval $[-0.01,+0.09]$, not reliable (Appendix~\\ref{app:baselines}).\nOn the hard tier every coverage positive is an obligation, so the coverage and obligation scores are one row, and the lookup's $0.79$ against the model's $0.70$ is not a reliable difference.")

# ============================================================ Section 9 (W1 wording; F4; D2; R4; the detector swap)
rep(B, "\\caption{The downstream policies for GPT-4.1 mini on the full obligation set: forbidding records put in view, stale answers at the detector's $0.50$ threshold, and correct answers on the licensed items. The stale rate holds under every gated policy until the store's untagged duplicates are tagged (Table~\\ref{tab:ds-a5}, Appendix~\\ref{app:resp}).}",
    "\\caption{The downstream policies for GPT-4.1 mini on the full obligation set: forbidding records put in view, detector-flagged stale answers at the $0.50$ threshold, and correct answers on the licensed items. The flagged rate holds under every gated policy until the store's untagged duplicates are retagged (Table~\\ref{tab:ds-a5}, Appendix~\\ref{app:resp}).}")
rep(B, "The preregistered reading is stale use at the detector's $0.80$ threshold over the obligations whose forbidding record is in view and tagged, and it is zero under every policy. The counts and rates here are the descriptive reading at $0.50$.",
    "The stale and correct counts are a token detector's, read by one of us where flagged, with its limits in Appendix~\\ref{app:resp}; its human validation is pending. The preregistered reading is stale use at the detector's $0.80$ threshold over the obligations whose forbidding record is in view and tagged, and it is zero under every policy. The counts and rates here are the descriptive reading at $0.50$; the Wilson intervals describe each policy alone and are not a paired test.")
rep(B, "The lookup rule reaches the same $0.82$ and the oracle $0.95$ (Table~\\ref{tab:ds-body}).",
    "The lookup rule reaches the same $0.82$ and the oracle $0.95$ (Table~\\ref{tab:ds-body}).\nThe lookup rule also costs correct answers on the licensed items, $40$ against $46$ under retrieval alone.")
rep(B, "Tags in view are respected: GPT-4.1 mini gives the stale value on $0$ of the $50$ views where every stale line is tagged or absent.\nEach of its $16$ stale answers under the oracle falls on a view with an untagged duplicate.\nAs a rate over the reached scorable obligations, GPT-4.1 mini gives the stale value in $0.19$ of cases under retrieval alone and $0.19$ under the oracle.\nThe gated rules are lower, $0.13$ and $0.10$, and every Wilson interval overlaps, so no policy changes the rate reliably (Table~\\ref{tab:ds-body}).",
    "Tags in view are respected: the detector flags GPT-4.1 mini on $0$ of the $50$ views where every stale line is tagged or absent.\nEach of its $16$ flagged answers under the oracle falls on a view with an untagged duplicate.\nAs a rate over the reached scorable obligations, the detector flags GPT-4.1 mini in $0.19$ of cases under retrieval alone and $0.19$ under the oracle, and the gated rules read $0.13$ and $0.10$ (Table~\\ref{tab:ds-body}).\n%% R112 (2026-09-16), review-2 F4: the paired comparison on the common-reach items, ds_downstream/NUMBERS_DS.md AUX-DS-AUDIT-PAIRED (mini D.4: 8 / 42 under ALWAYS, 9 / 42 under ORACLE; extended views F->T 2, T->F 1).\nOn the $42$ obligations retrieval alone reaches, the oracle's flagged count is $9$ against $8$, two answers turning stale and one turning clean, so no paired comparison separates the policies.")
rep(B, "Tagging the store's untagged duplicates, and nothing else, removes most of the stale answers; the fix belongs in the write path.\nRetagging the $35$ duplicates the audit found cuts stale answers under the gated fetch from $0.15$ to $0.03$ for GPT-4.1 mini, over all reached obligations, a wider denominator than Table~\\ref{tab:ds-body}'s scorable set.\nFor Haiku~4.5 the rate falls from $0.37$ to $0.23$, and the correct count is untouched for both.",
    "Retagging the store's untagged duplicates, and nothing else, removes most of the detector-flagged stale answers, which points to the write path.\nThe retagging is reference-assisted, the lines identified with the obligation's reference information and the detector, so it is a diagnostic intervention rather than a deployable repair.\nRetagging the $35$ duplicates the audit found cuts flagged stale answers under the gated fetch from $0.15$ to $0.03$ for GPT-4.1 mini, over all reached obligations, a wider denominator than Table~\\ref{tab:ds-body}'s scorable set.\nFor Haiku~4.5 the rate falls from $0.37$ to $0.23$; the licensed views were unchanged by construction, so this measures no cost on them.")
rep(B, "The stale and correct counts are a token detector's, read by hand where flagged, with its limits in Appendix~\\ref{app:resp}.\n",
    "")

# ============================================================ Limitations (A2; D2; the paraphrase status)
rep(B, "The lookup is untested beyond the store's own name pool, a mean of $99$ names, and the paraphrase check covers one rewording per question.",
    "The lookup is untested beyond the store's own name pool, a mean of $99$ names, and a paraphrase check of one rewording per question, fixed in advance, is not yet scored.")
rep(B, "The tagged route under the store's own tags is descriptive, with no prediction fixed in advance for its rise.",
    "The tagged route under the store's own tags is descriptive, with no prediction fixed in advance for its rise.\nThe ground-truth tags come from a join of the manifests to the stored records that marks the forbidding record for $82$ of the $104$ obligations, so record-level precision and recall rest on that alignment.\nThe duplicate retagging used the obligations' reference information, so it is diagnostic, and the detector that flags stale answers awaits its human validation.")

# ============================================================ Conclusion and the box (the author's points 3 and 4; D1)
rep(B, "What the models read in a lifecycle summary is the list of names, and the counts beside it carry nothing to them.\nTags on returned records are the other route, and no tested backend writes the list.\nThe stale answers downstream come from duplicates the store keeps active, so the fix is in the write path.",
    "In a lifecycle summary the attribute names carry most of the signal the models use, and the count interventions do not establish consistent count use.\nTags on returned records, read at retrieval time, are the other route, and no tested backend writes the list.\nThe detector-flagged stale answers downstream come from duplicates the store keeps active, and reference-assisted retagging removed most of them; whether that survives human validation is pending.")
rep(B, "Return non-active records with their lifecycle tags instead of masking them; under FR-Bank's own tags the tagged view kept its reading (Section~\\ref{sec:routes}).",
    "Return non-active records with their lifecycle tags instead of masking them; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags (Section~\\ref{sec:routes}).")
rep(B, "Fix the write path: tag the duplicates the store keeps active, because that removes most of the stale answers and no fetch policy does (Section~\\ref{sec:downstream}).",
    "Tag the duplicates the store keeps active: in our reference-assisted retagging that removed most of the detector-flagged stale answers, and no tested fetch policy showed an improvement (Section~\\ref{sec:downstream}).")
# Table 4: the alias label for the frozen DS paragraph's reference (F6)
rep(B, "\\label{tab:census}\n\\centering", "\\label{tab:census}\\label{tab:believed}%% R112 (2026-09-16): alias for the frozen DS paragraph's reference in Appendix E.10 (review-2 F6); no registered byte changes\n\\centering")

# ============================================================ Appendix
# E.1 (F2)
rep(X, "The EXPIRED column is derived from each entry's event time, and an expired entry can still be ACTIVE, so the four lifecycle columns overlap and do not sum to the ENTRIES column.",
    "The EXPIRED column is a flag derived from each entry's event time and the ACTIVE column counts the entries that are neither superseded nor retracted, so an expired entry can also be counted ACTIVE and the four lifecycle columns overlap; a record carrying more than one mark is labelled by the first of retracted, superseded, expired (Section~\\ref{sec:framework}).")
# C.2 (F3)
rep(X, "Blind coverage is $0.5000$ by construction, so each AUROC is also a gain.", "Blind coverage is $0.5000$ by construction, so the gain is the AUROC minus $0.5000$.")
# item 26 residue (editable lines only)
rep(X, "or moves beyond it with both intervals excluding zero, and fired as neither for both models", "or moves beyond it reliably, and fired as neither for both models")
rep(X, "GPT-4.1 mini degrades first at $15$ names, below $-0.05$ with both intervals excluding zero at $15$ and $30$.", "GPT-4.1 mini degrades first at $15$ names, reliably below $-0.05$ at $15$ and $30$.")
rep(X, "Against the lexical variant, which reads $0.5738$ on this population, every model leads with both intervals excluding zero.", "Against the lexical variant, which reads $0.5738$ on this population, every model leads reliably.")
rep(X, "there the model reads $0.7835$ against the lookup's $0.6083$, a margin of $+0.1752$ with both intervals excluding zero.",
    "there the model reads $0.7835$ against the superseded-section lookup's $0.6083$, a reliable margin of $+0.1752$.\n%% R112 (2026-09-16), post hoc F1 (reviews/NUMBERS_WP.md section 10, AUX-WP-F1-WHOLEMAP; reviews/v19/results/posthoc_f1.json).\nA lookup over the whole name map, the reader the coverage rows of Table~\\ref{tab:baselines} score, was computed on the easy tier after the fact and specified before recomputation: it reads $0.7469$ (persona interval $[0.6866,0.8028]$), and the model's margin over it is $+0.0367$ with intervals $[-0.0127,+0.0861]$ and $[-0.0036,+0.0776]$, not reliable and within tolerance, so the coverage margin the superseded-section lookup showed does not survive the stronger no-model reader (Table~\\ref{tab:cov-lookup}, last row).")
rep(X, "$-0.1141$ and $-0.0847$ below its ground-truth row with both intervals excluding zero, and", "$-0.1141$ and $-0.0847$ below its ground-truth row, both reliable, and")
rep(X, "(the fall is not beyond the tolerance with both intervals excluding zero)", "(the fall is not a reliable one beyond the tolerance)")
rep(X, "would rise by at least $0.10$ for each answerer with both intervals excluding zero, and that", "would rise reliably by at least $0.10$ for each answerer, and that")
rep(X, "the lookup rule reads $+25$ ($+0.04$, both intervals excluding zero) and $+10$ ($+0.02$, both including zero).", "the lookup rule reads $+25$ ($+0.04$, reliable) and $+10$ ($+0.02$, both intervals including zero).")
rep(X, "($+0.25$, both intervals excluding zero for both answerers)", "($+0.25$, reliable for both answerers)")
# item 73 residue
rep(X, "are read from the recorded probe scores (reviews/NUMBERS\\_R108.md).}", "are read from the recorded probe scores (the artifact's R108 ledger).}")
rep(X, "(\\texttt{reviews/DOWNSTREAM\\_AUDIT.md} in the artifact; \\texttt{NUMBERS\\_DS.md} section 9).", "(the downstream audit report in the artifact and its ledger, section 9).")
# tab:cov-lookup: the whole-map row (F1)
rep(X, "Easy tier, all backends & $595$ / $463$ & $0.4422$ & $0.6336$ & $0.5071$ & $0.4021$ & $+0.2315$ & $[+0.1628,+0.2979]$ & $[+0.1680,+0.2970]$ \\\\\n\\bottomrule",
    "Easy tier, all backends & $595$ / $463$ & $0.4422$ & $0.6336$ & $0.5071$ & $0.4021$ & $+0.2315$ & $[+0.1628,+0.2979]$ & $[+0.1680,+0.2970]$ \\\\\n\\midrule\n%% R112 (2026-09-16), post hoc F1: the whole-map lookup on the FR-Bank easy tier (AUX-WP-F1-WHOLEMAP); the lexical column is the whole-map lexical reader of the same run.\nFR-Bank easy tier, whole name map (post hoc) & $354$ / $243$ & $0.4660$ & $0.7835$ & $0.6311$ & $0.7469$ & $+0.0367$ & $[-0.0127,+0.0861]$ & $[-0.0036,+0.0776]$ \\\\\n\\bottomrule")
rep(X, "\\caption{The name lookup, lexical and embedding, on the coverage populations, beside GPT-4.1 mini's recorded blind and indexed coverage AUROC, with the model minus the embedding lookup and both intervals. Where the coverage positives are obligations the lookup reads them; where they are ordinary records the model leads. Exploratory, computed after the fact on the recorded rows.}",
    "\\caption{The name lookup, lexical and embedding, on the coverage populations, beside GPT-4.1 mini's recorded blind and indexed coverage AUROC, with the model minus the embedding lookup and both intervals; the last row reads the whole name map instead of the superseded section (post hoc, specified before recomputation). Where the coverage positives are obligations the lookup reads them; where they are ordinary records the model leads the superseded-section lookup and not, reliably, the whole-map lookup. Exploratory, computed after the fact on the recorded rows.}")
# E.9: the trial paragraph's last sentence
rep(X, "Its tag route at trial scale is left for the discussion period.",
    "Since the trial, the census was run on all forty personas (Appendix~\\ref{app:posthoc-graphiti}); the summary route and the tag route on this backend have not been run.")
# E.10: the audit read wording
rep(X, "Read by hand, GPT-4.1 mini gives the stale value in $11$ of its $16$ scorable oracle flags and Haiku 4.5 in $8$ of its $19$, the rest naming the value while stating it superseded or restating the question's words; those classes are the auditor's.",
    "Read by one of us, GPT-4.1 mini gives the stale value in $11$ of its $16$ scorable oracle flags and Haiku 4.5 in $8$ of its $19$, the rest naming the value while stating it superseded or restating the question's words; those classes are one reader's and not an independent validation.")
# F: the registration record gains the R85 Amendment 1 row
rep(X, "DS Amendment 4: a view header binding the entries to the persona and pinning the date & \\texttt{fb4b2ca8c8} & 2026-09-14 & the same $452$ views answered once more by GPT-4.1 mini and Haiku 4.5 with a header naming the persona and the current date; the same detector with first-sentence and source columns beside; two predictions on the $65$ licensed items in view, with failure texts & two predictions; both held \\\\",
    "DS Amendment 4: a view header binding the entries to the persona and pinning the date & \\texttt{fb4b2ca8c8} & 2026-09-14 & the same $452$ views answered once more by GPT-4.1 mini and Haiku 4.5 with a header naming the persona and the current date; the same detector with first-sentence and source columns beside; two predictions on the $65$ licensed items in view, with failure texts & two predictions; both held \\\\\n% R112 (2026-09-16): the forty-persona Graphiti run (registrations/ADDENDUM_R85_GRAPHITI_AMENDMENT_1.md, frozen 43132a3; r85_graphiti/NUMBERS_R85.md AUX-R85-G10-*; D-R85-12, -15, -16). P1 failed on recall and held on precision; P2 to P4 not run at this build.\nGraphiti, forty personas: the event census, the forbidding-record census, a summary route and a tag route & \\texttt{43132a3469} & 2026-09-15 & the unmodified release ingesting all forty personas; the two censuses against the manifests with four predictions and their failure texts, P1 on the census recall and precision, P2 to P4 on the summary and tag routes & P1 failed on recall, held on precision (Appendix~\\ref{app:posthoc-graphiti}); P2 to P4 not run at this build \\\\")
# G: the opener gains the specified-before-recomputation convention; G.4 and the provenance table are inserted by markers below
rep(X, "Everything in this appendix was done after seeing the data and carries no registered prediction.\nIt is collected here so that unregistered material has one home and is never read as though it had been predicted.",
    "Everything in this appendix was done after seeing the data and carries no registered prediction.\nIt is collected here so that unregistered material has one home and is never read as though it had been predicted.\nThe analyses marked ``specified before recomputation'' (the PN-versus-PRESENT decomposition, the intent-aware lookup, the whole-map coverage lookup and the reading of the forty-persona census) were written up as definitions with expected outcomes in one file, hashed before any of them ran (sha256 \\texttt{ae2600fc}), and are post-hoc analyses, not predictions made before the original study.")


def main():
    files = {p: p.read_text(encoding="utf-8") for p in (A, B, X)}
    for f, old, new in E:
        t = files[f]
        n = t.count(old)
        if n != 1:
            print(f"ABORT: {f.name}: expected 1 occurrence, found {n}:\n  {old[:160]!r}")
            sys.exit(1)
        files[f] = t.replace(old, new)
    for p, t in files.items():
        p.write_text(t, encoding="utf-8", newline="\n")
    print(f"applied {len(E)} replacements to {', '.join(p.name for p in files)}")


if __name__ == "__main__":
    main()
