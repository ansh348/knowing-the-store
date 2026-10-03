# -*- coding: utf-8 -*-
"""r123_apply.py -- program R123 (2026-09-19; the v21 update and writing pass, the author's brief with its amendments from R122's report): the
v21 lineage's edits, each an asserted replacement in reviews/v21/src (OLD occurs exactly once; LF preserved; idempotent; --check reports without
writing). Table blocks come from reviews/v21/src/r123_tables_v21.tex (ledger_r123_tables.py; never typed by hand). Groups, one per phase:

  phase_a   the finished results landed: the intent crossover (R121 HELD_TEXTS_R121.md, the author's wording), R122 T1, T3, T4, T5 (HELD_TEXTS.md
            and the amendments: Table 1's GPT-4.1 mini rows at five draws with the one-draw note, the Limitations sentence in the author's
            wording, P-R2 in the registration record only), the supersession-margin table (amendment 2: at five draws GPT-4.1 mini's margin
            over the lookup is no longer reliably negative), the registration record's fourth table and the recount (58 / 16 -> 90 / 27).
  phase_b   Section 9 retitled and cut to two paragraphs and the reach table; the detector-scored rows and sentences moved to Appendix E.10
            under an exploratory heading.
  phase_c   the reframing: abstract, Section 1, the Section 5 sentence, the Conclusion, the builders box, Limitations (added sentences and
            their payers).
  phase_d   the language sweep (review and process leftovers, internal vocabulary, anonymity, known errors, related work).
Usage: python reviews/v21/tools/r123_apply.py --only phase_a[,phase_b,...] [--check]
"""
from __future__ import annotations

import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v21" / "src"
TABLES = SRC / "r123_tables_v21.tex"
BODY = SRC / "body_v21.tex"
APPX = SRC / "appendix_v21.tex"
ABS = SRC / "abstract_v21.tex"


def block(name):
    t = TABLES.read_text(encoding="utf-8")
    m = re.search(r"%%BLOCK " + re.escape(name) + r"%%\n(.*?)\n%%END " + re.escape(name) + r"%%", t, flags=re.S)
    assert m, name
    return m.group(1)


# ----------------------------------------------------------------------------------------------------------------------- Phase A texts
CROSSOVER_S5 = (
    "%% R123 (2026-09-19), the intent crossover (R121; registrations/ADDENDUM_CF2_INTENT_CROSSOVER.md frozen at 648d671, Amendment 1 at 2c441a7;\n"
    "%% r82_counterfactual/cf2/NUMBERS_CF2.md section 14d, AUX-CF2-IX-*): the held paragraph of reviews/r121/HELD_TEXTS_R121.md section 1 in the\n"
    "%% author's wording; its second sentence split in three for the sentence-length rule (63 words), no word otherwise changed.\n"
    "Definition~\\ref{def:coverage} makes the label depend on intent, and no main-study row varies the intent over a fixed store.\n"
    "A crossover on the counterfactual set does.\n"
    "Each supersession pair is asked its recorded present-tense question and a second question about how the attribute has changed, of the same two store versions, and each expiry pair a question about the past event under the all-states summary.\n"
    "The same stale record is then forbidden under one question and licensed under the other (Appendix~\\ref{app:counterfactual}).\n"
    "Under the main-study rubric four of the five models do not condition on intent: on a fixed store they score the change or past question higher than the original (same-store AUROC $0.35$ to $0.44$ on supersession).\n"
    "Opus 5 does, without being told ($0.90$, and $0.85$ on expiry).\n"
    "GPT-5.6 Sol reads $0.64$ on expiry under the old rubric.\n"
    "Under a rubric that states the rule, Opus 5, GPT-5.6 Luna and GPT-5.6 Sol separate the intents ($0.99$, $0.96$ and $0.88$ at one draw), the first two at the level of a fixed cue list ($0.99$).\n"
    "GPT-4.1 mini and Haiku 4.5 do not ($0.48$ and $0.55$).\n"
    "In $9$ of GPT-5.6 Sol's $11$ losses ($76/0/11$ within pairs) both questions score $0.96$ or higher, so the rule was not applied on those pairs.\n"
    "The name lookup is within tolerance of $0.50$ on both populations ($0.47$, $0.45$).\n"
    "The intent-explicit rubric lowers no model's original-task discrimination by more than $0.05$ (the largest fall $0.05$, Haiku 4.5 on the supersession pairs; the largest rise $0.17$, GPT-4.1 mini on the expiry pairs).\n"
    "\n")

E3_SENTENCES = (
    " %% R123: the E.3 sentences of HELD_TEXTS_R121.md section 2 (AUX-CF2-IX-*).\n"
    "For four of the five models the main-study rubric does not elicit the intent condition; Opus 5 applies it unprompted.\n"
    "In the main populations every \\pn{} question has current or upcoming intent by construction, so there a staleness judgment and an obligation judgment coincide; they come apart only in the crossover of Appendix~\\ref{app:counterfactual}.\n")

LIMITATIONS_T4 = (
    "%% R123: the R122 T4 sentence in the author's wording (amendment 3 to the brief; AUX-R122-P1-*: Luna +0.0113, mini +0.0085; Luna minus the lookup +0.0867 [+0.0447,+0.1302]; [+0.0562,+0.1219]).\n"
    "Under the intent-explicit rubric GPT-5.6 Luna and GPT-4.1 mini score within $0.02$ of their main-rubric values on the counterfactual set, and Luna's margin over the name lookup holds ($+0.09$, both intervals excluding zero); the other models were not rerun.\n")

C2_INTENT_PARA = (
    "\\paragraph{The intent crossover.}\n"
    "%% R123 (2026-09-19): the crossover of reviews/r121 (registrations/ADDENDUM_CF2_INTENT_CROSSOVER.md, 648d671; Amendment 1, 2c441a7; NUMBERS_CF2.md section 14d) and R122's T4\n"
    "%% (reviews/r122/registrations/ADDENDUM_R122_CF2_P1.md, 77bc0d9; reviews/r122/NUMBERS_R122.md AUX-R122-P1-*). Every number is the tables' (ledger_r123_tables.py).\n"
    "The crossover asks each in-scope supersession pair of the set its recorded present-tense question and a second question about how the attribute has changed, and each expiry pair a question about the past event, of the same two store versions, so that the same stale record is forbidden under the original question and licensed under the crossed one (Table~\\ref{tab:cf-intent}).\n"
    "The crossed questions were drafted by GPT-4.1 mini from the attribute path and the time sense alone, never from any stored value, screened for value leakage, and read by us before any monitor call; five pairs were dropped and two took a second drafting seed.\n"
    "Two rubrics were used: the main-study rubric, and one that states that the obligation depends on the question's intent.\n"
    "The name lookup, a keyword-intent lookup over a fixed cue list, and an oracle-intent lookup that reads the constructed intent are the readers with no generative-model call.\n"
    "Three predictions were written before any call.\n"
    "The first, that every model would sit within tolerance of $0.50$ on the same-store contrast under the main-study rubric, came out otherwise: four models sit below it and Opus 5 above it.\n"
    "The second, that Opus 5 and Haiku 4.5 would separate the intents under the intent-explicit rubric, came out otherwise for Haiku 4.5.\n"
    "The third, that the name lookup would sit within tolerance of $0.50$, came out as written.\n"
    "GPT-5.6 Sol's prediction, made after an interim read of three models' rows, that it separates the intents under the intent-explicit rubric, came out as written.\n"
    "Under the intent-explicit rubric the counterfactual set itself was rerun for GPT-5.6 Luna at five draws and GPT-4.1 mini at one (Table~\\ref{tab:cf-p1}).\n"
    "Each reads within $0.02$ of its main-rubric row ($0.8531$ against $0.8417$; $0.7253$ against $0.7167$).\n"
    "Luna keeps its per-state order and a reliable margin over the name lookup ($+0.0867$, intervals $[+0.0447,+0.1302]$ and $[+0.0562,+0.1219]$); GPT-4.1 mini's two counted states swap order (expiry $0.5489$ to $0.4758$, retraction $0.5283$ to $0.5456$), neither move reliable, which is a failed prediction.\n"
    "\n")

C2_MINI_K5 = (
    "%% R123: R122 T3 (reviews/r122/registrations/ADDENDUM_R122_MINI_K5.md, 77bc0d9; reviews/r122/NUMBERS_R122.md AUX-R122-K5-*; the supersession margin from the same rows, tab:sup-margins).\n"
    "At five draws with the provider's default temperature GPT-4.1 mini reads $0.76$ under the superseded-only summary and $0.83$ under the all-states summary, within $0.05$ of its one-draw rows, with the tied triples falling from $51$ to $6$ (Table~\\ref{tab:mini-k5}).\n"
    "Table~\\ref{tab:cf-main} prints those rows.\n"
    "At five draws the model sits within tolerance of the name lookup on the whole set ($-0.0016$, both intervals including zero) and on supersession ($-0.0429$, intervals $[-0.0898,+0.0006]$ and $[-0.1001,+0.0035]$), where its one-draw row is reliably below (Table~\\ref{tab:sup-margins}).\n")

C2_ENC = (
    "\\paragraph{The lookup under other encoders.}\n"
    "%% R123: R122 T1 (reviews/r122/registrations/ADDENDUM_R122_ENCODERS.md, 77bc0d9; reviews/r122/NUMBERS_R122.md AUX-R122-ENC-*).\n"
    "Two further encoders, \\texttt{all-mpnet-base-v2} and \\texttt{bge-small-en-v1.5}, score the same lookup at $0.76$ and $0.76$ on the counterfactual set, within $0.01$ of MiniLM; replacing every name by a random token scores $0.60$ (Table~\\ref{tab:enc-lookup}).\n"
    "\n")

E10_GATE = (
    "\\paragraph{What the gate buys, reach only.}\n"
    "%% R123: R122 T5 (reviews/r122/registrations/ADDENDUM_R122_GATE_REACH.md, 77bc0d9; reviews/r122/NUMBERS_R122.md AUX-R122-GATE-*; reviews/v21/results/reach_rows_r123.json for the recorded policies' 661-means).\n"
    "Three policies with no monitor call and no answer call, assembled from the recorded ranking and the store's records, are read against the model rule at its mean view of $5.43$ lines over the $661$ questions (Table~\\ref{tab:gatereach}); over the $104$ obligations alone the same view averages $7.08$ lines, the denominator of Table~\\ref{tab:ds-body-lower}.\n"
    "A fetch keyed on the name the lookup matches best, with no gate, reaches $0.8164$ at the matched budget against the model rule's $0.8173$, a difference of $-0.0009$ with both intervals including zero.\n"
    "Unmatched, it spends $6.51$ lines per question against $5.43$, a ratio of $1.20$, and cut to the matched budget it loses licensed records reliably ($-0.0375$).\n"
    "The recorded similarity view at seven lines reaches $0.5962$, and matched $0.5443$.\n"
    "A view that keeps only the newest record of each attribute reaches $0.2337$ matched, $-0.5836$ below the rule with both intervals excluding zero, and none of the $26$ retraction obligations, because a cancellation is never the newest record of what it cancels.\n"
    "All three predictions came out as written.\n"
    "\n")

REG_D = (
    "%% R123 (2026-09-19): the registration record's fourth table, the programs landed since the R101 count: the Graphiti trial's frozen readings\n"
    "%% (registrations/ADDENDUM_R85_GRAPHITI.md, f2d7688), the five R117 registrations (177697a), the intent crossover and its amendment (648d671, 2c441a7)\n"
    "%% and the four R122 registrations (77bc0d9; copied into registrations/ at landing, no byte above the markers changed).\n"
    "\\begin{table}[H]\n"
    "\\caption{The registration record, continued: the fourth backend's frozen readings, the five registrations of the counterfactual and downstream follow-ups, the intent crossover, and the four registrations of the encoder, draw, rubric and reach checks; the Outcome column lists each prediction's outcome, and a prediction registered after an interim read of other models' rows is labelled so. Every row was committed before its first call.}\n"
    "\\label{tab:registrations-d}\n"
    "\\centering\n"
    "\\scriptsize\n"
    "\\setlength{\\tabcolsep}{1.5pt}\n"
    "\\begin{tabular}{@{}p{0.15\\linewidth}p{0.11\\linewidth}p{0.11\\linewidth}p{0.42\\linewidth}p{0.15\\linewidth}@{}}\n"
    "\\toprule\n"
    "Artifact & Commit hash & Freeze date & What it froze & Outcome \\\\\n"
    "\\midrule\n"
    "Graphiti, three personas: the ingestion trial and its readings & \\texttt{f2d7688a54} & 2026-08-30 & the unmodified release on three personas, its census, and five readings written before any run and read at forty personas: two with a bar, that the obligation gain under the store-written summary excludes zero and that the superseded-names lookup sits within tolerance of the model or above it; one uncomputable on that population; two descriptive (Appendix~\\ref{app:posthoc-graphiti}) & the gain reading failed, the lookup reading held; the coverage reading not computable \\\\\n"
    "Moved-count control, Amendment 1: Opus 5 at five draws & \\texttt{177697a4ae} & 2026-09-19 & Opus 5 at five draws on the moved-count texts against its recorded five-draw row; one prediction, that the one-draw movement on retraction and expiry replicates with both intervals excluding zero (Table~\\ref{tab:v2rcat}) & held \\\\\n"
    "Names against counts on the counterfactual set & \\texttt{177697a4ae} & 2026-09-19 & the default summary with its counts removed and with its names removed, GPT-4.1 mini and Haiku 4.5 against their recorded one-draw and five-draw rows; two predictions, that names only sits within tolerance of the recorded row and that counts only falls reliably below names only, and one descriptive reading (Table~\\ref{tab:cf-names-counts}) & both held \\\\\n"
    "The marker ablation on the structureless stores & \\texttt{177697a4ae} & 2026-09-19 & the constrained rendering with its marker omitted and reworded, GPT-4.1 mini on both stores and GPT-5.6 Luna through the raw API; one prediction, that the coverage loss disappears under the neutral wording, and one descriptive reading (Table~\\ref{tab:marker}) & failed on Mem0, held on A-MEM \\\\\n"
    "DS Amendment 8: label propagation inside the view & \\texttt{177697a4ae} & 2026-09-19 & a view-only rule propagating a tagged line's tag to same-attribute lines that repeat it, under ground-truth and own tags; five predictions on the views changed, false propagation and the flagged rate (Table~\\ref{tab:ds-a8}) & one held (false propagation under ground-truth tags at most $5\\%$); three failed; one not defined \\\\\n"
    "GPT-5.6 Sol and GPT-5.6 Luna on the counterfactual set & \\texttt{177697a4ae} & 2026-09-19 & both models at five draws through the raw API on the $444$ under the default summary; two predictions, that Sol exceeds the name lookup reliably and that Luna does not (Table~\\ref{tab:cf-main}) & Sol's held; Luna's failed, Luna exceeds it reliably \\\\\n"
    "The intent crossover & \\texttt{648d67192c} & 2026-09-19 & the crossed questions, their author check and leak screen, two rubrics, four models, three lookups; three predictions with failure texts and two descriptive readings (Table~\\ref{tab:cf-intent}): that every model sits within tolerance of $0.50$ on the same-store contrast under the main-study rubric (observed: four below the band, GPT-4.1 mini $0.40$, Haiku 4.5 $0.38$, GPT-5.6 Luna $0.35$, GPT-5.6 Sol $0.44$, the crossed question scoring higher on the same store, and Opus 5 above it, $0.90$); that Opus 5 and Haiku 4.5 separate the intents under the intent-explicit rubric (Opus 5 $0.99$; Haiku 4.5 $0.55$, both intervals including $0.50$); that the name lookup sits within tolerance of $0.50$ ($0.47$, $0.45$) & the first failed on all five models and the second on Haiku 4.5; the third held \\\\\n"
    "The intent crossover, Amendment 1: GPT-5.6 Sol & \\texttt{2c441a72ac} & 2026-09-19 & Sol as a fifth reader of the crossover, one draw; its prediction, that it separates the intents under the intent-explicit rubric with both intervals excluding $0.50$, was made after an interim read of three models' rows and is labelled so & held ($0.88$; a prediction made after the interim read) \\\\\n"
    "Lookup encoders & \\texttt{77bc0d9595} & 2026-09-19 & the name lookup under two further encoders and a random-token control (Table~\\ref{tab:enc-lookup}); one prediction, both encoders within $0.05$ of MiniLM on the counterfactual set & held \\\\\n"
    "GPT-4.1 mini at five draws & \\texttt{77bc0d9595} & 2026-09-19 & five draws at the provider's default temperature under both summaries (Table~\\ref{tab:mini-k5}); one prediction, within $0.05$ of the one-draw row with fewer tied triples & held \\\\\n"
    "The counterfactual set under the intent-explicit rubric & \\texttt{77bc0d9595} & 2026-09-19 & GPT-5.6 Luna and GPT-4.1 mini on the $444$ under the rubric that states the intent rule (Table~\\ref{tab:cf-p1}); three predictions: each within $0.05$ of its recorded row, the same per-state order, Luna's margin over the lookup reliable & the first and third held; the second failed on GPT-4.1 mini, whose counted states swap order with neither move reliable \\\\\n"
    "What the gate buys, reach only & \\texttt{77bc0d9595} & 2026-09-19 & an always-open fetch, the similarity view and a recency-aware view, budget-matched to the model rule (Table~\\ref{tab:gatereach}); three predictions on reach and lines & all three held \\\\\n"
    "\\bottomrule\n"
    "\\end{tabular}\n"
    "\\end{table}\n"
    "\n"
    "%% R123: the recount behind Section 4's sentence (reviews/NUMBERS_R123.md AUX-R123-TALLY).\n"
    "\\noindent\\textbf{The count of predictions.} A prediction counts when it was registered with a bar, whether it held, failed or could not be evaluated; readings registered as descriptive are not counted, and the pending answer-stage predictions of Graphiti Amendment 2 and the moved-count control's second amendment are not yet in the count. Table~\\ref{tab:registrations} carries $47$ such predictions with $8$ that came out otherwise, Table~\\ref{tab:registrations-b} $17$ with $10$, Table~\\ref{tab:registrations-c} none, and Table~\\ref{tab:registrations-d} $26$ with $9$: $90$ predictions, $27$ of which came out otherwise, the count Section~\\ref{sec:setup} states.\\\\\n"
    "\n")


# ----------------------------------------------------------------------------------------------------------------------- Phase B texts
SEC9_HEAD = "\\section{Acting on the judgment}\\label{sec:downstream}\n"
SEC9_END = "\\section{Limitations}\\label{sec:limitations}\\label{sec:discussion}\n"
SEC9_NEW = (
    "\\section{What the judgment buys at retrieval}\\label{sec:downstream}\n"
    "\n"
    "%% R123 Phase B (2026-09-19; the author's brief): Section 9 retitled and cut to the author's two paragraphs and the reach table; every\n"
    "%% detector-scored answer-stage number (Table tab:ds-body with its note, the 0-of-50, retagging, Haiku-residual and paired-comparison sentences)\n"
    "%% moved whole to Appendix E.10 under the heading 'Answer-level outcomes under the policies (exploratory)'. The gate adjustments to the author's\n"
    "%% text: 'with the gate always open' -> 'with the fetch always on', 'What the gate buys' -> 'What gating buys', 'Ungated, the fetch' -> 'Always on,\n"
    "%% the fetch' (prose_scan rule V bars the noun 'gate' in the main text). Numbers: AUX-R123-REACH-ROWS, AUX-R122-GATE-MATCHED, -GATE-PREDICTIONS;\n"
    "%% AUX-DS-AUDIT-SOURCE (35 of 89); AUX-DS-A8-* (1 of 452; 187 of 272).\n"
    "Acting on the judgment changes what the agent sees; whether it changes what the agent answers is not established here.\n"
    "A lifecycle fetch keyed on the name list reaches far more forbidding records than retrieval alone at the same budget.\n"
    "On the full obligation set, top-five retrieval puts the forbidding record in view for $54$ of the $104$ obligations ($0.52$), and the fetch reaches $0.82$ (Table~\\ref{tab:reach}).\n"
    "The model's judgment is not what buys that reach: with the fetch always on, it reaches $0.82$ at a matched budget.\n"
    "What gating buys is budget.\n"
    "Always on, the fetch spends $1.20$ times the lines per question, and cut to the gated budget it pushes licensed records out of view, a reliable loss of $0.04$.\n"
    "Retrieval that keeps only the newest record of each attribute reaches $0.23$ and none of the $26$ retraction obligations, because a cancellation is never the newest record of what it cancels.\n"
    "\n"
    "%%REACH-TABLE%%\n"
    "\n"
    "What the agent then does with those records depends on the store's tags, and the store keeps untagged copies.\n"
    "Of the $89$ scorable obligation views, $35$ carry an active line that asserts the stale value, the retained obsolete assertions Section~\\ref{sec:backends} censused.\n"
    "A view-only rule that propagates a line's tag to same-attribute lines repeating it changes $1$ of $452$ views, because $187$ of the $272$ stale lines sit under a different attribute key from their tagged twin.\n"
    "The repair therefore belongs to the write path.\n"
    "Answer-level outcomes under these policies are exploratory (Appendix~\\ref{app:resp}).\n"
    "\n")

E10_EXPLORATORY_HEAD = (
    "\\paragraph{Answer-level outcomes under the policies (exploratory).}\n"
    "%% R123 Phase B (2026-09-19): Section 9's detector-scored table (tab:ds-body, [h] to [H]) and sentences moved here whole; the words and values unchanged\n"
    "%% except the table note's self-pointer to this appendix and the pointer to Table tab:reach where the sentence pointed at the old Table 3.\n"
    "The table and the sentences below are exploratory: every stale and correct count is a token detector's, read by one of us where flagged, and the detector's human validation is in progress (the validation sample is described at the end of this appendix).\n")


def sec9_edits():
    """Phase B as one span replacement in the body and one insertion in the appendix, built from the current Section 9 text."""
    body = BODY.read_text(encoding="utf-8")
    if SEC9_HEAD not in body:
        return []      # already applied
    i = body.index(SEC9_HEAD); j = body.index(SEC9_END)
    span = body[i:j]
    # the table, its note and the detector-scored sentences move; the two framing sentences and the stale comments are dropped
    t0 = span.index("\\begin{table}[h]"); t1 = span.index("\\end{table}\n", t0) + len("\\end{table}\n")
    tbl = span[t0:t1].replace("\\begin{table}[h]", "\\begin{table}[H]", 1)
    tbl = tbl.replace("are in Table~\\ref{tab:ds-body-lower} (Appendix~\\ref{app:resp}).", "are in Table~\\ref{tab:ds-body-lower}.")
    assert tbl.count("\\begin{table}[H]") == 1 and "Table~\\ref{tab:ds-body-lower}." in tbl
    rest = span[t1:]
    keep = []
    for ln in rest.split("\n"):
        s = ln.strip()
        if not s or s.startswith("%"):
            continue
        if s.startswith("Of the $89$ scorable obligation views") or s.startswith("A view-only rule propagating"):
            continue      # the author's Section 9 carries these two facts in its own words
        keep.append(ln)
    moved = "\n".join(keep) + "\n"
    moved = moved.replace("(Table~\\ref{tab:ds-a5}, Appendix~\\ref{app:resp})", "(Table~\\ref{tab:ds-a5})")
    assert "Gating a lifecycle fetch on the obligation judgment" in moved and "Haiku~4.5's residual" in moved and "Tags in view are respected" in moved
    assert len(keep) == 14, len(keep)
    new_body = SEC9_NEW.replace("%%REACH-TABLE%%\n", block("reach") + "\n")
    appx_anchor = "%% R110: the lower block of Section 8's Table 7, moved here by the author's trim order of 2026-09-15"
    return [(BODY, span, new_body),
            (APPX, appx_anchor, E10_EXPLORATORY_HEAD + tbl + moved + "\n" + appx_anchor)]


# ----------------------------------------------------------------------------------------------------------------------- Phase C texts
ABSTRACT_NEW = (
    "% R123 Phase C (2026-09-19): the author's abstract (the brief, Phase C), replacing abstract v8 (in git at 5aaa103 and before). Gate adjustments,\n"
    "% each shown in the pass report: the 'First, ...' sentence split at 'read the names.' (52 words, the sentence-length rule); the numerals of the two\n"
    "% sentences that state no lookup difference (148; 0.01, 0.12, 0.16) set in text mode so rule G2, which reads math-mode numerals, does not fire.\n"
    "% Amendment 2's case: the clause 'and GPT-4.1 mini falls below it' is not printed (at five draws the margin is not reliably negative, AUX-R123-SUP-MARGINS).\n"
    "\\begin{abstract}\n"
    "An agent with a persistent memory store can judge, before retrieving anything, whether the store holds something it must no longer use, such as a cancelled plan or a replaced preference. "
    "We study what such a monitor can know from a value-free lifecycle summary that the store maintains: record counts per lifecycle state and the names of attributes whose content is no longer current. "
    "This is a diagnostic study on synthetic stores with exact labels, four memory backends and up to six language models. "
    "Its central test asks each of 148 questions against three versions of one store, so question wording cannot predict the label. "
    "Three findings follow. "
    "First, the summary carries each label twice, as a name and as a count, and monitors read the names. "
    "Removing every count leaves the two models tested within 0.01 of the full summary, removing the names costs them 0.12 and 0.16 AUROC, and naming a lifecycle state is what makes it detectable. "
    "Second, where a state is named, a cosine lookup over the names is enough: no model reliably exceeds it. "
    "Opus 5, GPT-5.6 Sol and GPT-5.6 Luna exceed the lookup on the whole set by $0.07$ to $0.08$, a margin earned on the states the summary only counts. "
    "The same three follow a rubric that makes the obligation depend on the question's intent; GPT-4.1 mini and Haiku 4.5 do not, and only Opus 5 does so untold. "
    "Third, real backends write this summary poorly. "
    "FR-Bank over-marks, Mem0 overwrites and A-MEM's links resolve to nothing; under FR-Bank's own metadata GPT-4.1 mini and the lookup fall near chance, and Graphiti's own names serve a lookup better than the model. "
    "At retrieval, a lifecycle fetch keyed on the name list reaches far more of the records an agent must not use than retrieval alone, and as many without a model's judgment as with it. "
    "Flagged stale answers trace to untagged duplicates the store keeps active, most under a different attribute key; the answer-stage detector's human validation is in progress.\n"
    "\\end{abstract}\n")

S1_OLD_START = "A monitor makes both judgments from a lifecycle summary, a count table and a name map with the values removed (Figure~\\ref{fig:framework}).\n"
S1_OLD_END = "\\end{itemize}\n"
S1_NEW = (
    "Prior work on memory scores what an agent retrieves or answers \\citep{longmemeval,locomo,memoryagentbench,stale}.\n"
    "On MemoryAgentBench's conflict-resolution questions no memory agent exceeds $7\\%$ accuracy.\n"
    "\n"
    "%% R123 Phase C (2026-09-19): Section 1 after the hike paragraph and the prior-work paragraph replaced by the author's two paragraphs and three\n"
    "%% contributions (the brief, Phase C). Gate adjustments, shown in the pass report: 'carries' -> 'states' in the thesis sentence (rule D read it as a\n"
    "%% near-duplicate of the abstract's and the Conclusion's sentence, 80 percent of content tokens shared); one sentence and two bullets split at a\n"
    "%% semicolon or a comma for the sentence-length rule (47, 51 and 47 words). Every number is Section 5's, Table 1's or Appendix C.2's.\n"
    "This paper is a diagnostic study of what such a monitor can know, and from what.\n"
    "The monitor reads a lifecycle summary that the store maintains: a count of records per lifecycle state and a map of attribute names with every value removed (Figure~\\ref{fig:framework}).\n"
    "We ask three questions of it.\n"
    "Which part of the summary carries the judgment?\n"
    "What does a language model add over a reader with no generative-model call?\n"
    "And do the summaries that real memory backends can write support the judgment at all?\n"
    "Every score is an AUROC, the chance that a positive scores above a negative, so $0.50$ is chance.\n"
    "\n"
    "The answers agree.\n"
    "The summary states each label twice, as a name and as a count, and the models read the names (Section~\\ref{sec:counterfactual}).\n"
    "Where a state is named, a similarity lookup over the names is not reliably exceeded by any of five models.\n"
    "Three models pull ahead only on the states the summary merely counts, and the same three follow an intent rule that the other two do not (Section~\\ref{sec:counterfactual}).\n"
    "The backends we tested write the list of names poorly or not at all, and what they write bounds every reader (Sections~\\ref{sec:routes} and~\\ref{sec:backends}).\n"
    "At retrieval, the reach that matters comes from a lifecycle fetch keyed on the name list, with or without a model's judgment in front of it (Section~\\ref{sec:downstream}).\n"
    "What the store writes down matters more than which reader reads it.\n"
    "\\begin{itemize}\\setlength{\\itemsep}{1pt}\n"
    "\\item A counterfactual test for pre-retrieval memory judgments: one question asked of three versions of a store that differ in one attribute ($n=444$), so question wording cannot predict the label, with readers that make no generative-model call as baselines. An intent crossover holds the store fixed and varies the question.\n"
    "\\item Evidence that attribute names, rather than counts or the choice of reader, carry the judgment. Removing the counts changes nothing and removing the names costs $0.12$ to $0.16$. No model reliably exceeds a name lookup on a named state. Opus 5, GPT-5.6 Sol and GPT-5.6 Luna exceed it by $0.07$ to $0.08$ only through the states the summary counts, and the same three follow an intent-explicit rubric that GPT-4.1 mini and Haiku 4.5 do not.\n"
    "\\item A census of what four memory backends write about themselves, and its consequences. FR-Bank over-marks, Mem0 overwrites and A-MEM's links resolve to nothing; under store-written metadata a small model and the lookup fall near chance. A lifecycle fetch keyed on the name list reaches as many forbidding records ungated as gated, which locates the value in the list.\n"
    "\\end{itemize}\n")

CONCL_OLD_START = "The models draw most of their signal from a lifecycle summary's attribute names.\n"
CONCL_OLD_END = "Downstream, the flagged stale answers trace to duplicates the store keeps active, and answer-level benefit awaits the detector's human validation.\n"
CONCL_NEW = (
    "%% R123 Phase C (2026-09-19): the Conclusion replaced by the author's paragraph (the brief, Phase C; the moved-count sentence in its three-model form until\n"
    "%% E9 lands). Gate adjustment, shown in the pass report: 'bounds what a reader can know' for 'bounds what any reader can know' (rule G1 bars that phrase).\n"
    "What a memory store writes down bounds what a reader can know about it before retrieval.\n"
    "A lifecycle summary carries each obligation twice, as a name and as a count, and the models read the names.\n"
    "On a state the list names, no model reliably exceeds a name lookup.\n"
    "Opus 5, GPT-5.6 Sol and GPT-5.6 Luna exceed it by $0.07$ to $0.08$ on the whole set, on the states the summary only counts, and the same three follow an intent rule that GPT-4.1 mini and Haiku 4.5 do not.\n"
    "Only Opus 5 conditions on intent untold, and of the three models given the moved-count control only Opus 5 responds.\n"
    "The backends we tested degrade the list, and under FR-Bank's own metadata GPT-4.1 mini and the lookup fall near chance.\n"
    "At retrieval the reach comes from a fetch keyed on the list, gated or not.\n"
    "Whether answers improve is not established: the flagged stale answers trace to duplicates the store keeps active under other keys, and the detector's human validation is in progress.\n")

LIMITATIONS_ADDED = (
    "%% R123 Phase C: the three added Limitations sentences (the brief, Phase C; AUX-R122-ENC-RANDOM 0.5954, AUX-R122-ENC-ROWS -0.0059 / -0.0080, AUX-CF2-IX-LOOKUPS keyword A 0.9943).\n"
    "A list of meaningless tokens in place of the names still scores $0.60$ on the counterfactual set, so part of every reader's score comes from whether the list is empty.\n"
    "Two further encoders score within $0.01$ of the one we use.\n"
    "The crossed questions carry explicit cue words, so a fixed cue list separates their intents as well as the best model; questions without such cues are untested.\n")


def phase_c_edits():
    body = BODY.read_text(encoding="utf-8")
    edits = []
    # the abstract
    abs_t = ABS.read_text(encoding="utf-8")
    m = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}\n", abs_t, flags=re.S)
    if "R123 Phase C" not in abs_t:
        edits.append((ABS, m.group(0), ABSTRACT_NEW))
    # Section 1
    if S1_OLD_START in body:
        i = body.index(S1_OLD_START); j = body.index(S1_OLD_END, i) + len(S1_OLD_END)
        edits.append((BODY, body[i:j], S1_NEW))
    # Section 5: the added sentence at the end of the crossover paragraph
    edits.append((BODY,
                  "The intent-explicit rubric lowers no model's original-task discrimination by more than $0.05$ (the largest fall $0.05$, Haiku 4.5 on the supersession pairs; the largest rise $0.17$, GPT-4.1 mini on the expiry pairs).\n",
                  "The intent-explicit rubric lowers no model's original-task discrimination by more than $0.05$ (the largest fall $0.05$, Haiku 4.5 on the supersession pairs; the largest rise $0.17$, GPT-4.1 mini on the expiry pairs).\n"
                  "Five models cannot say why three differ from two; the split does not follow size, since GPT-5.6 Luna is the smaller GPT-5.6 model.\n"))
    # the Conclusion
    if CONCL_OLD_START in body:
        i = body.index(CONCL_OLD_START); j = body.index(CONCL_OLD_END, i) + len(CONCL_OLD_END)
        edits.append((BODY, body[i:j], CONCL_NEW))
    # the builders box
    edits.append((BODY,
                  "Keep non-active records reachable with their lifecycle tags; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags (Section~\\ref{sec:routes}).\n",
                  "Keep non-active records reachable with their lifecycle tags where deletion or access revocation is not required; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags (Section~\\ref{sec:routes}).\n"))
    edits.append((BODY,
                  "Compare a name lookup with the model on the actual store before paying for the model call (Sections~\\ref{sec:counterfactual} and~\\ref{sec:backends}).\n",
                  "Compare a name lookup with the model on the actual store before paying for the model call; a model earns its call on states the summary only counts and on questions whose intent licenses old content (Sections~\\ref{sec:counterfactual} and~\\ref{sec:backends}).\n"))
    # Limitations: the added sentences after the T4 sentence, and the two payers
    edits.append((BODY,
                  "and Luna's margin over the name lookup holds ($+0.09$, a reliable difference); the other models were not rerun.\n",
                  "and Luna's margin over the name lookup holds ($+0.09$, a reliable difference); the other models were not rerun.\n" + LIMITATIONS_ADDED))
    edits.append((BODY,
                  "The counted-state groups are small: $30$ retraction and $30$ expiry pairs on the counterfactual set, and $44$ expiry with the extension draw of Appendix~\\ref{app:counterfactual}. On the full obligation set",
                  "The counted-state groups are small: $30$ retraction and $30$ expiry pairs on the counterfactual set. On the full obligation set"))
    edits.append((BODY,
                  "Two closed vendors supply the capability comparison, no open-weights model was run on the counterfactual set, and two runs stopped at the budget on the full populations.\n",
                  "Two closed vendors supply the capability comparison, and no open-weights model was run on the counterfactual set.\n"))
    # the payers' facts in the appendix (the extension paragraph of C.2; tab:runs' caption already carries the budget-stopped runs)
    edits.append((APPX,
                  "Table~\\ref{tab:cf3-expiry} prints the extension beside the $444$'s expiry pairs and pools the two, $44$ pairs, with the pooling stated in the caption.\n",
                  "Table~\\ref{tab:cf3-expiry} prints the extension beside the $444$'s expiry pairs and pools the two, $44$ pairs, with the pooling stated in the caption.\n"
                  "%% R123 Phase C: the Limitations clause on the extension draw moved here (the payer for the three added Limitations sentences).\n"
                  "The counted-state group stays small with it, $44$ expiry pairs against $88$ supersession pairs.\n"))
    return edits


# ----------------------------------------------------------------------------------------------------------------------- Phase D texts
E9_RECONCILE = (
    "%% R123 Phase D (2026-09-19): the four counts near one hundred reconciled in one sentence (AUX-BELIEVED-FR: 109 events, approximately 102 explained; AUX-SIDE-S2-CENSUS: 104 TRUE-superseded entries, 40 active; the 104 obligations: 63 / 26 / 15).\n"
    "Four counts near one hundred in that census are four different things: the manifests record $109$ supersession events across the forty personas; the ground-truth join explains about $102$ of the store's inactive entries; the manifest's supersessions touch $104$ stored entries, $40$ of them still active; and the $104$ obligations of the full obligation set are questions, $63$ supersession, $26$ retraction and $15$ expiry, not entries.\n")

BIB_NEW = {
    "dhingra2022": (
        "B.~Dhingra et al. Time-Aware Language Models as Temporal Knowledge Bases. \\emph{Transactions of the Association for Computational Linguistics}, 10:257--273, 2022.\n",
        "B.~Dhingra et al. Time-Aware Language Models as Temporal Knowledge Bases. \\emph{Transactions of the Association for Computational Linguistics}, 10:257--273, 2022.\n"
        "\n"
        "% R123 (2026-09-19): three references for the Related Work sentence on precedents of lifecycle tags; each VERIFIED against its Crossref DOI record on 2026-09-19 (reviews/NUMBERS_R123.md AUX-R123-REFS; tools/refcheck_v11.py OUT_OF_SCOPE).\n"
        "\\bibitem[Doyle(1979)]{doyle1979}\n"
        "J.~Doyle. A truth maintenance system. \\emph{Artificial Intelligence}, 12(3):231--272, 1979.\n"),
    "verbrouting": (
        "C.~K. Sah et al. Beyond Self-Knowledge: Propagating Uncertainty Across Reasoning and Retrieval in LLMs. \\emph{arXiv preprint arXiv:2607.25600}, 2026.\n",
        "C.~K. Sah et al. Beyond Self-Knowledge: Propagating Uncertainty Across Reasoning and Retrieval in LLMs. \\emph{arXiv preprint arXiv:2607.25600}, 2026.\n"
        "\n"
        "\\bibitem[Shapiro et al.(2011)]{shapiro2011}\n"
        "M.~Shapiro, N.~Pregui\\c{c}a, C.~Baquero, and M.~Zawirski. Conflict-free replicated data types. In \\emph{Stabilization, Safety, and Security of Distributed Systems (SSS)}, LNCS, pages 386--400. Springer, 2011.\n"
        "\n"
        "\\bibitem[Snodgrass \\& Ahn(1986)]{snodgrass1986}\n"
        "R.~Snodgrass and I.~Ahn. Temporal databases. \\emph{Computer}, 19(9):35--42, 1986.\n"),
}


def phase_d_edits():
    E = []
    # --- the body: known errors and vocabulary
    E += [
        # Figure 2's caption: only the count row differs between PRESENT and PN; the ABSENT version also loses the name
        (BODY,
         "Only the count row differs, so no reader over names separates the versions (supersession triple: Appendix~\\ref{app:counterfactual}).}\n",
         "Only the count row differs between the \\present{} and \\pn{} versions, and the \\absent{} version also loses the name, so the name lookup separates none of the three (supersession triple: Appendix~\\ref{app:counterfactual}).}\n"),
        # Section 8: the 661 margins over the lookup do not survive the persona-grouped interval (tab:margin-661)
        (BODY,
         "levels that include what the question wording gives away (Section~\\ref{sec:setup}).\n",
         "levels that include what the question wording gives away (Section~\\ref{sec:setup}).\n"
         "%% R123 Phase D: AUX-R103-MARGIN / tab:margin-661: the embedding margins +0.0698, +0.0843, +0.0726 with persona intervals [-0.0180,+0.1520], [-0.0091,+0.1759], [-0.0143,+0.1634].\n"
         "Their margins over the lookup do not survive the persona-grouped interval (Table~\\ref{tab:margin-661}, Appendix~\\ref{app:baselines}).\n"),
        # 'no model' -> 'no generative-model call' in the body's prose and Table 1's row label
        (BODY,
         "the similarity lookup over the summary's superseded-names list, the no-model baseline every model is measured against \\\\\n",
         "the similarity lookup over the summary's superseded-names list, the baseline with no generative-model call that every model is measured against \\\\\n"),
        (BODY,
         "with two readers that have no model in them.\n",
         "with two readers that make no generative-model call.\n"),
        (BODY,
         "\\multicolumn{5}{@{}l}{\\textit{Readers with no model in them}}\\\\\n",
         "\\multicolumn{5}{@{}l}{\\textit{Readers with no generative-model call}}\\\\\n"),
        # Related work: STALE's write-side component engaged; three verified citations in one sentence
        (BODY,
         "STALE \\citep{stale}, the closest work, asks whether an agent can tell that a memory it has already retrieved is no longer valid; this paper asks whether the store holds such a memory before anything is retrieved.\n",
         "STALE \\citep{stale}, the closest work, asks whether an agent can tell that a memory it has already retrieved is no longer valid; this paper asks whether the store holds such a memory before anything is retrieved.\n"
         "%% R123 Phase D: STALE's write-side component (its abstract, read 2026-09-19: 'CUPMem, a prototype that strengthens write-time revision through structured state consolidation and propagation-aware search').\n"
         "Its CUPMem prototype revises state at write time and consolidates it; we measure what such write-time structure has to expose, the names of the states it revises, for a judgment before retrieval.\n"
         "%% R123 Phase D: three verified references (AUX-R123-REFS), one sentence of 25 words or fewer.\n"
         "Lifecycle tags have precedents: temporal databases keep validity intervals \\citep{snodgrass1986}, replicated sets keep tombstones for removed elements \\citep{shapiro2011}, and truth maintenance tracks retracted beliefs \\citep{doyle1979}.\n"),
        (BODY, "\\begin{thebibliography}{63}\n", "\\begin{thebibliography}{66}\n"),
    ]
    for key, (old, new) in BIB_NEW.items():
        E.append((BODY, old, new))
    # --- the appendix: process leftovers, vocabulary, anonymity, known errors
    E += [
        (APPX, "and the five capability items registered before the ladder run.\n", "and the five capability items registered before the cross-model run.\n"),
        (APPX, "When the expansion tried to complete GPT-5.6 Sol through the same agent,", "When the full-population runs tried to complete GPT-5.6 Sol through the same agent,"),
        (APPX, "$0$ of $12$ and $0$ of $12$ (the expansion's deviation ledger),", "$0$ of $12$ and $0$ of $12$ (the deviation record of those runs),"),
        (APPX, "re-derived exactly by the expansion scorer.\n", "re-derived exactly by the full-population scorer.\n"),
        (APPX, "under the three summaries, the first form of the set, the adverse rows,", "under the three summaries, the set's earlier thirty-question draw (labelled first form in Table~\\ref{tab:counterfactual}), the adverse rows,"),
        (APPX, "Two readers with no model in them read the count table alone,", "Two readers with no generative-model call read the count table alone,"),
        (APPX, "so neither registered lane established that it followed the count. Opus 5, the optional lane, was run once per item", "so neither registered run established that it followed the count. Opus 5, added as an optional reader, was run once per item"),
        (APPX, "against the five-draw row that the two registered lanes did not.\n", "against the five-draw row that the two registered runs did not.\n"),
        (APPX, "The first form of this set asked thirty questions ($n=90$, ten positives per state)", "The earlier draw of this set asked thirty questions ($n=90$, ten positives per state)"),
        (APPX, "against $3$ of $30$ in the first form.\n", "against $3$ of $30$ in the earlier draw.\n"),
        (APPX, "our label-transfer read had not been made at this build, so no paraphrase row is printed.\n", "our label-transfer read has not been made, so no paraphrase row is printed.\n"),
        (APPX, "germane to E0, E1, the capability ladder, the question-signal audit,", "germane to E0, E1, the cross-model set, the question-signal audit,"),
        (APPX, "scored on the coverage rows, a new measurement of this pass.\n", "scored on the coverage rows, a measurement added after the main study.\n"),
        # (the NB-6 sentence "Under a truthful summary ..." is registered text that ships verbatim, ADDENDUM_R81; it keeps its word and the glossary maps it)
        (APPX, "does not survive the stronger no-model reader (Table~\\ref{tab:cov-lookup}, last row).\n", "does not survive the stronger reader with no generative-model call (Table~\\ref{tab:cov-lookup}, last row).\n"),
        (APPX, "The score ranks well and calibrates badly (Appendix~\\ref{app:posthoc}), so a deployed monitor thresholds at the base rate of positives.\n", "The score ranks well and calibrates badly (Appendix~\\ref{app:posthoc}).\n"),
        (APPX, "were ingested into that backend in early 2026 under a copy carrying", "were ingested into that backend earlier under a copy carrying"),
        (APPX, "Haiku 4.5 and the no-model readers are in Appendix~\\ref{app:resp}.}\n", "Haiku 4.5 and the readers with no generative-model call are in Appendix~\\ref{app:resp}.}\n"),
        (APPX, "A descriptive registration written after the ninth review re-rendered the same five retrieved records", "A descriptive registration re-rendered the same five retrieved records"),
        (APPX, "\\caption{The tagged view, the rows Section~\\ref{sec:routes}'s table leaves out: Haiku 4.5 on the view and on summary plus view under ground-truth tags, and the four readers with no model in them under each tag source,",
         "\\caption{The tagged view, the rows Table~\\ref{tab:routes} leaves out: Haiku 4.5 on the view and on summary plus view under ground-truth tags, and the four readers with no generative-model call under each tag source,"),
        (APPX, "minus the reader with no model in it}}\\\\\n", "minus the reader with no generative-model call}}\\\\\n"),
        (APPX, "Table~\\ref{tab:ds-body} carries each policy's fires, reach, view size, tagged reach and coverage;", "Table~\\ref{tab:ds-body-lower} carries each policy's fires, reach, view size, tagged reach and coverage;"),
        (APPX, "A second descriptive registration, written after the first draft, ran the answer stage", "A second descriptive registration ran the answer stage"),
        (APPX, "(DS Amendment 7, descriptive; no prediction was registered; no model call).", "(DS Amendment 7, descriptive; no prediction was registered; no generative-model call)."),
        (APPX, "\\caption{The downstream policies, the columns Section 8's table leaves out:", "\\caption{The downstream policies, the columns Table~\\ref{tab:ds-body} leaves out:"),
        (APPX, "the paraphrase drafting lane $0.12$ over $413$ calls;", "the paraphrase drafting run $0.12$ over $413$ calls;"),
        (APPX, "the constants of the expansion's lane code, to $2.67$ and $12.39$,", "the price constants of the full-population run code, to $2.67$ and $12.39$,"),
        (APPX, "The continuation's cumulative token-accounted list cost is $22.025336$ under that same ceiling;", "The Graphiti follow-up's cumulative token-accounted list cost is $22.025336$ under that same ceiling;"),
        (APPX, "and both automated judging passes; remaining cached-depth judging is blocked by provider credits.\n", "and both automated judging passes; the cached-depth judging that remains was not run.\n"),
        (APPX, "Coverage FOK, easy tier $0.78$ (Section~\\ref{sec:populations}) &", "Coverage FOK, easy tier $0.78$ (Appendix~\\ref{app:baselines}) &"),
        (APPX, "Downstream reach, flagged stale answers, retagging (Section~\\ref{sec:downstream}, Table~\\ref{tab:ds-body}) &", "Downstream reach, flagged stale answers, retagging (Section~\\ref{sec:downstream}, Table~\\ref{tab:reach}; Appendix~\\ref{app:resp}, Table~\\ref{tab:ds-body}) &"),
        (APPX, "at the cross-vendor preregistration (the R74 addendum, Table~\\ref{tab:registrations}; 2026-08-14)", "at the cross-vendor preregistration (the cross-vendor addendum, Table~\\ref{tab:registrations}; 2026-08-14)"),
        (APPX, "alongside the explicitly registered Graphiti continuation in Section~\\ref{app:posthoc-graphiti}.\n", "alongside the registered Graphiti follow-up in Section~\\ref{app:posthoc-graphiti}.\n"),
        (APPX, "GPT-4.1 mini's retention figures above divide by an indexed-minus-blind difference that Section~\\ref{sec:populations} does not report as a gain,", "GPT-4.1 mini's retention figures above divide by an indexed-minus-blind difference that Appendix~\\ref{app:laddertable} does not report as a gain,"),
        (APPX, "\\paragraph{The registered paragraph.} The paragraph that Section~\\ref{sec:populations} points to reads, with its numbers, as follows.\n", "\\paragraph{The registered paragraph.} The downstream experiment's registered paragraph reads, with its numbers, as follows.\n"),
        # anonymity: the quoted registered text's 'our own store', redacted and said so
        (APPX, "so the gain measured on our own store does not reproduce where the lifecycle record is thinner.''\n", "so the gain measured on [the lifecycle store] does not reproduce where the lifecycle record is thinner.'' (The quotation is redacted for anonymity.)\n"),
        # E.9: the four counts near one hundred
        (APPX, "Table~\\ref{tab:census} in Section~\\ref{sec:backends} carries the census behind the overstate, erase and invent reading.\n", "Table~\\ref{tab:census} in Section~\\ref{sec:backends} carries the census behind the overstate, erase and invent reading.\n" + E9_RECONCILE),
        # Appendix A: the duplicate population tables merged (tab:populations dropped; tab:setup defines each population)
        (APPX, "This appendix carries the cross-model set in full; Table~\\ref{tab:populations} defines every population the body names, and Table~\\ref{tab:runs} records which model ran on which question set.\n",
         "This appendix carries the cross-model set in full; Table~\\ref{tab:setup} defines every population the body names, with the models that ran on each, and Table~\\ref{tab:runs} records which model ran on which question set.\n"),
        (APPX, "\\caption{The populations, with their sizes and positives and the models that ran on each (calls per question in parentheses); Appendix~\\ref{app:laddertable} defines each population in full and records the runs.}\n",
         "\\caption{The populations, with their sizes and positives and the models that ran on each (calls per question in parentheses). The body refers to a population by these names only.}\n"),
    ]
    appx = APPX.read_text(encoding="utf-8")
    if "\\label{tab:populations}" in appx:
        i = appx.index("%% R110: the population list (OUTLINE.md section C), moved here from Section 4")
        j = appx.index("\\end{table}\n", appx.index("\\label{tab:populations}")) + len("\\end{table}\n")
        E.append((APPX, appx[i:j], "%% R123 Phase D: Table tab:populations (the population list) dropped; tab:setup carries every row of it (the name, n, positives and what each isolates) and the models that ran on each.\n"))
    return E


def groups():
    G = {}
    G["phase_b"] = sec9_edits()
    G["phase_c"] = phase_c_edits()
    G["phase_d"] = phase_d_edits()
    # the gate adjustments to the Phase C texts (repeat_scan: no 9-gram in three or more places; prose_scan rule D); no number or claim changed
    G["phase_c_gates"] = [
        (BODY,
         "Opus 5, GPT-5.6 Sol and GPT-5.6 Luna exceed it by $0.07$ to $0.08$ on the whole set, on the states the summary only counts, and the same three follow an intent rule that GPT-4.1 mini and Haiku 4.5 do not.\n",
         "GPT-5.6 Sol, GPT-5.6 Luna and Opus 5 exceed it by $0.07$ to $0.08$ on the whole set, on the states the summary only counts, and the same three follow an intent rule that neither GPT-4.1 mini nor Haiku 4.5 does.\n"),
        (BODY,
         "A lifecycle summary carries each obligation twice, as a name and as a count, and the models read the names.\n",
         "A lifecycle summary carries each obligation twice, as a name and as a count; the models read the names.\n"),
        (BODY,
         "Opus 5, GPT-5.6 Sol and GPT-5.6 Luna exceed it by $0.07$ to $0.08$ only through the states the summary counts, and the same three follow an intent-explicit rubric that GPT-4.1 mini and Haiku 4.5 do not.\n",
         "GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 exceed it by $0.07$ to $0.08$ only through the states the summary counts, and the same three follow an intent-explicit rubric that the other two do not.\n"),
        # with the abstract and the Conclusion in place, the Section 5 sentence returns to the author's wording (the Phase A adjustment is no longer needed:
        # the 9-gram now stands in the abstract and Section 5 only, and rule D reads the seven-token 'Neither ... does' form as a duplicate of the Conclusion's)
        (BODY,
         "Neither GPT-4.1 mini nor Haiku 4.5 does ($0.48$ and $0.55$).\n",
         "GPT-4.1 mini and Haiku 4.5 do not ($0.48$ and $0.55$).\n"),
        # q_scan rule Q-C wants the plain definition 'with the values removed' before the summary's first numeric use
        (BODY,
         "a count of records per lifecycle state and a map of attribute names with every value removed (Figure~\\ref{fig:framework}).\n",
         "a count of records per lifecycle state and a map of attribute names with the values removed (Figure~\\ref{fig:framework}).\n"),
        (BODY,
         "FR-Bank over-marks, Mem0 overwrites and A-MEM's links resolve to nothing; under store-written metadata a small model and the lookup fall near chance. A lifecycle fetch keyed on the name list reaches as many forbidding records ungated as gated, which locates the value in the list.\n",
         "FR-Bank over-marks, Mem0 overwrites, A-MEM's links resolve to nothing; under store-written metadata a small model and the lookup fall near chance. A lifecycle fetch keyed on the list of names reaches as many forbidding records ungated as gated, which locates the value in the list.\n"),
        # amendment 2's Section 5 wording; rule D read the appositive as a near-duplicate of the Conclusion's sentence (75 percent)
        (BODY,
         "On the counterfactual set no model reliably exceeds the name lookup on supersession, the state the list names (Appendix~\\ref{app:counterfactual}).\n",
         "On the counterfactual set no model reliably exceeds the name lookup on supersession (Appendix~\\ref{app:counterfactual}).\n"),
    ]
    G["phase_a"] = [
        # Section 5: the crossover paragraph after the coverage-only reader sentence
        (BODY,
         "A reader that only knows whether the store covers the question would score $0.75$ on the whole set and tie every triple.\n\n",
         "A reader that only knows whether the store covers the question would score $0.75$ on the whole set and tie every triple.\n\n" + CROSSOVER_S5),
        # Table 1: GPT-4.1 mini's rows at five draws, with the note
        (BODY,
         "GPT-4.1 mini, sup.\\ only & $0.72$ & $[0.67,0.76]$ & $0.71$ & $81/57/10$ \\\\\nGPT-4.1 mini, all three & $0.80$ & $[0.74,0.85]$ & $0.78$ & $105/32/11$ \\\\\n",
         "%% R123 (amendment 1 to the brief): the five-draw rows (reviews/r122/results/scores_r122_oai.json T3; AUX-R122-K5-*), written by ledger_r123_tables.py; the one-draw rows in the note.\n" + block("cf_main_mini") + "\n"),
        (BODY,
         "Category-aware count reader, sup.\\ only & $0.60$ & $[0.58,0.64]$ & $0.59$ & $60/88/0$ \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n",
         "Category-aware count reader, sup.\\ only & $0.60$ & $[0.58,0.64]$ & $0.59$ & $60/88/0$ \\\\\n\\bottomrule\n\\end{tabular}\n\\par\\smallskip\n\\begin{minipage}{0.97\\linewidth}\\scriptsize\n" + block("cf_main_note") + "\n\\end{minipage}\n\\end{table}\n"),
        # Figure 3's caption: its GPT-4.1 mini bars stay the recorded one-draw rows
        (BODY,
         "The two markers on the left are GPT-5.6 Sol and GPT-5.6 Luna, which ran the default summary only.}\n",
         "The two markers on the left are GPT-5.6 Sol and GPT-5.6 Luna, which ran the default summary only; GPT-4.1 mini's bars are its recorded one-draw rows, and Table~\\ref{tab:cf-main} prints its five-draw rows.}\n"),
        # Section 4: the recount
        (BODY,
         "Of the $58$ predictions preregistered before data collection, $16$ came out otherwise (Appendix~\\ref{app:registration}).\n",
         "%% R123: the recount over every program now printed (reviews/NUMBERS_R123.md AUX-R123-TALLY; Appendix F's count paragraph).\nOf the $90$ predictions preregistered before data collection, $27$ came out otherwise (Appendix~\\ref{app:registration}).\n"),
        # Limitations: the T4 sentence in the author's wording, after the paraphrase sentence
        (BODY,
         "A paraphrase check of one rewording per question, fixed in advance, is not yet scored.\n",
         "A paraphrase check of one rewording per question, fixed in advance, is not yet scored.\n" + LIMITATIONS_T4),
        # Appendix E.3: the intent-condition sentences after "Step 2 is the scored quantity."
        (APPX,
         "Step 2 is the scored quantity.\n",
         "Step 2 is the scored quantity.\n" + E3_SENTENCES),
        # Appendix C.2: the post hoc intent paragraph's opener, and the crossover paragraph with its two tables after it
        (APPX,
         "The test the review asked for on intent, the same store history judged under two intents, cannot be built from the recorded rows: each question carries one constructed intent and the \\textsc{change} intent is never \\pn{}, so any comparison across intents would vary intent with the label.\n",
         "The same store judged under two intents cannot be read from the recorded rows: each question carries one constructed intent and the \\textsc{change} intent is never \\pn{}, so any comparison across intents would vary intent with the label; the crossover below builds that test with new questions.\n"),
        (APPX,
         "below the floor of five the specification set for a reading, so no monitor comparison is printed on them.\n\n",
         "below the floor of five the specification set for a reading, so no monitor comparison is printed on them.\n\n" + C2_INTENT_PARA + block("cf_intent") + "\n\n" + block("cf_p1") + "\n\n"),
        # Appendix C.2: the five-draw row after the single-draw note, and its table before the registered texts
        (APPX,
         "GPT-4.1 mini's single draw takes $12$ values.\n",
         "GPT-4.1 mini's single draw takes $12$ values.\n" + C2_MINI_K5),
        (APPX,
         "The registered texts for this set (Appendix~\\ref{app:registration}) read as follows.\n",
         block("mini_k5") + "\n\nThe registered texts for this set (Appendix~\\ref{app:registration}) read as follows.\n"),
        # Appendix C.2: the supersession-margin table after the adverse rows
        (APPX,
         "That is what a reader of the whole map should do when the counted names sit in that map.\n",
         "That is what a reader of the whole map should do when the counted names sit in that map.\nTable~\\ref{tab:sup-margins} gives each model's supersession-only margin over the name lookup with both intervals.\n\n" + block("sup_margins") + "\n"),
        # Appendix C.2: the encoders after the lexical lookup's table
        (APPX,
         "\\paragraph{GPT-4.1 mini on the expiry pairs under the all-states summary.}\n",
         C2_ENC + block("enc_lookup") + "\n\n\\paragraph{GPT-4.1 mini on the expiry pairs under the all-states summary.}\n"),
        # tab:cf-names-counts: the comparator stays the one-draw row, and says so
        (APPX,
         "The recorded intact row is the comparator; differences carry the item-level and the persona-grouped interval.",
         "The recorded intact row is the comparator, GPT-4.1 mini's at one draw (the five-draw row of Table~\\ref{tab:cf-main} is not used here); differences carry the item-level and the persona-grouped interval."),
        # Appendix E.10: the reach-only paragraph and its table after tab:reach-k
        (APPX,
         "\\paragraph{Registered texts.} The eleven prediction texts of the mechanism tests and the downstream experiment,",
         E10_GATE + block("gate_reach") + "\n\n\\paragraph{Registered texts.} The eleven prediction texts of the mechanism tests and the downstream experiment,"),
        # Appendix A: the run-coverage and population tables name every model that ran the counterfactual set
        (APPX,
         "GPT-4.1 mini & OpenAI & ran & ran (the main study) & ran & ran & one call, temperature $0$ \\\\\n",
         "GPT-4.1 mini & OpenAI & ran & ran (the main study) & ran & ran & one call, temperature $0$; on the counterfactual set also five calls at the provider default (Table~\\ref{tab:mini-k5}) \\\\\n"),
        (APPX,
         "GPT-5.6 Sol & OpenAI & ran & stopped at the budget & stopped at the budget & ran$^{h}$ & five calls, through the agent harness at reasoning effort low \\\\\n",
         "GPT-5.6 Sol & OpenAI & ran & stopped at the budget & stopped at the budget & ran$^{h}$ & five calls; the cross-model set through the agent harness at reasoning effort low, the counterfactual set through the raw API \\\\\n"),
        (APPX,
         "($148$ obligations: $88$ supersession, $30$ retraction, $30$ expiry) & GPT-4.1 mini (1), Haiku 4.5 (5), Opus 5 (5) \\\\\n",
         "($148$ obligations: $88$ supersession, $30$ retraction, $30$ expiry) & GPT-4.1 mini (1, and 5), Haiku 4.5 (5), Opus 5 (5), GPT-5.6 Sol (5), GPT-5.6 Luna (5) \\\\\n"),
        # Appendix F: the fourth table and the count paragraph before the attestation paragraph
        (APPX,
         "%% R116 (2026-09-18): the provenance audit (reviews/r115/PROVENANCE_AUDIT.md sections 1, 3 and 4); the lock-attested set named from its table.\n",
         REG_D + "%% R116 (2026-09-18): the provenance audit (reviews/r115/PROVENANCE_AUDIT.md sections 1, 3 and 4); the lock-attested set named from its table.\n"),
    ]
    # the gate adjustments to the Phase A texts (the brief: where a prose gate trips, adjust minimally and show the diff); no number changed
    G["phase_a_gates"] = [
        # repeat_scan: 'GPT-4.1 mini and Haiku 4.5 do not' would stand in the abstract, Section 5 and the Conclusion (a 9-gram in three places)
        (BODY,
         "GPT-4.1 mini and Haiku 4.5 do not ($0.48$ and $0.55$).\n",
         "Neither GPT-4.1 mini nor Haiku 4.5 does ($0.48$ and $0.55$).\n"),
        # s17_grep caps the phrase 'both intervals excluding zero' at three occurrences outside registered texts; 'reliable' is the defined word (Section 4)
        (BODY,
         "and Luna's margin over the name lookup holds ($+0.09$, both intervals excluding zero); the other models were not rerun.\n",
         "and Luna's margin over the name lookup holds ($+0.09$, a reliable difference); the other models were not rerun.\n"),
        (APPX,
         "reaches $0.2337$ matched, $-0.5836$ below the rule with both intervals excluding zero, and none of the $26$ retraction obligations,",
         "reaches $0.2337$ matched, $-0.5836$ below the rule, a reliable difference, and none of the $26$ retraction obligations,"),
        (APPX,
         "that the one-draw movement on retraction and expiry replicates with both intervals excluding zero (Table~\\ref{tab:v2rcat})",
         "that the one-draw movement on retraction and expiry replicates reliably (Table~\\ref{tab:v2rcat})"),
        # layout: the crossover row's per-model directions moved from the narrow Outcome column into the What-it-froze column (the same words)
        (APPX,
         "three predictions with failure texts and two descriptive readings (Table~\\ref{tab:cf-intent}) & the first failed on all five models (four below the band, GPT-4.1 mini $0.40$, Haiku 4.5 $0.38$, GPT-5.6 Luna $0.35$, GPT-5.6 Sol $0.44$, the crossed question scoring higher on the same store; Opus 5 above it, $0.90$); the second failed on Haiku 4.5 ($0.55$, both intervals including $0.50$; Opus 5 $0.99$); the third held (the name lookup $0.47$, $0.45$) \\\\\n",
         "three predictions with failure texts and two descriptive readings (Table~\\ref{tab:cf-intent}): that every model sits within tolerance of $0.50$ on the same-store contrast under the main-study rubric (observed: four below the band, GPT-4.1 mini $0.40$, Haiku 4.5 $0.38$, GPT-5.6 Luna $0.35$, GPT-5.6 Sol $0.44$, the crossed question scoring higher on the same store, and Opus 5 above it, $0.90$); that Opus 5 and Haiku 4.5 separate the intents under the intent-explicit rubric (Opus 5 $0.99$; Haiku 4.5 $0.55$, both intervals including $0.50$); that the name lookup sits within tolerance of $0.50$ ($0.47$, $0.45$) & the first failed on all five models and the second on Haiku 4.5; the third held \\\\\n"),
    ]
    return G


def n_old_del(t, old):
    return t.count(old) == 0


def apply(edits, check):
    texts = {}
    for p, old, new in edits:
        t = texts.get(p)
        if t is None:
            raw = p.read_bytes(); assert b"\r\n" not in raw, f"{p}: CRLF source, refusing"
            t = raw.decode("utf-8")
        n_old = t.count(old)
        n_new = t.count(new) if new else (0 if n_old else 1)     # a deletion counts as applied once OLD is gone
        # an insertion (OLD kept inside NEW) is recognised as applied by the first line it adds (its %% marker comment or its first sentence),
        # so a later gate adjustment to the inserted text can never make the insertion run twice
        added = new.replace(old, "", 1).strip().split("\n")[0] if old in new else None
        marker = new.split("\n")[0] if new.startswith("%%") else None          # a replacement that opens with its own %% comment line
        if n_new == 1 and (old not in new or n_old == 1):
            print(f"  already applied : {p.name}: {new[:70]!r}")
        elif added and t.count(added) == 1 and n_new == 0:
            print(f"  already applied (adjusted since): {p.name}: {added[:70]!r}")
        elif marker and n_old == 0 and n_new == 0 and t.count(marker) == 1:
            print(f"  already applied (adjusted since): {p.name}: {marker[:70]!r}")
        elif n_new == 0 and n_old == 1:
            print(f"  {'would apply' if check else 'applied'}     : {p.name}: {old[:70]!r}")
            if not check:
                t = t.replace(old, new)
        else:
            raise SystemExit(f"ANCHOR NOT UNIQUE ({n_old} old, {n_new} new) in {p}: {old[:90]!r}")
        texts[p] = t
    return texts


def main():
    check = "--check" in sys.argv
    G = groups()
    names = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else ["phase_a"]
    edits = [e for g in names for e in G[g]]
    texts = apply(edits, check)
    if not check:
        for p, t in texts.items():
            io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("r123_apply:", "check only" if check else "written", f"({len(edits)} edits, groups {names})")


if __name__ == "__main__":
    main()
