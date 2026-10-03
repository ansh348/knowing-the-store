# -*- coding: utf-8 -*-
"""wp_phase4.py -- Phase 4 of the writing pass on paper_v18 (paper_v18_writing_prompt.md section 16: the prose pass under section 15, in the
author's order Sections 1, 5, 6, 7, 8, 9, 3, 4, 2, Limitations, Conclusion; items 8-16, 23, 26-29, 31-33, 37-48, 62-67, 85, 86, 88, 93,
94, with 19 and 25 by the ruling), and the author's three steps of 2026-09-15: Step 1 layout (the placeins barrier, the notation box in
two columns, Figure 3's height, the cross-model table in \\small), Step 2 the prose pass with its cut targets, Step 3 the three levers in
order only while the main text is still past page 9. Applied to reviews/v18/src/body_v18.tex after Phase 3 (wp_phase3.py on 6dbabdf).

Every edit is an asserted string replacement (each old string occurs exactly once). No number changes: every value that leaves the body
stands in a table or an appendix (reviews/v18/NUMBER_MOVES_WP.md carries the reasons). Usage:
    python reviews/v18/tools/wp_phase4.py --step=1            layout only
    python reviews/v18/tools/wp_phase4.py --step=2:S7         layout + the prose pass through Section 7 (the halfway reading)
    python reviews/v18/tools/wp_phase4.py --step=2            layout + the whole prose pass
    python reviews/v18/tools/wp_phase4.py --step=3:N          ... + the first N levers of Step 3
The script restores the body from commit 6dbabdf, runs wp_phase3.py, then applies its own edits, so one command yields the state.
"""
from __future__ import annotations

import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v18" / "src"
BODY = SRC / "body_v18.tex"
TOOLS = ROOT / "reviews" / "v18" / "tools"

ORDER = ["S1", "S5", "S6", "S7", "S8", "S9", "S3", "S4", "S2", "LIM", "CON"]


def rep(text, old, new, n=1):
    assert text.count(old) == n, (text.count(old), n, old[:90])
    return text.replace(old, new)


# ----------------------------------------------------------------------------------------------------------------------------------
# Step 1: layout
# ----------------------------------------------------------------------------------------------------------------------------------

def step1(t):
    # the placeins barrier: Figure 2's source moves past \section{Setup}, so the [section] barrier no longer holds it before Section 4 ends
    i = t.index("\\begin{figure}[t]\n\\centering\n%% R110: Figure 2, the worked example")
    j = t.index("\\label{fig:example}\n\\end{figure}\n", i) + len("\\label{fig:example}\n\\end{figure}\n")
    fig2 = t[i:j]
    t = t[:i] + t[j:]
    t = rep(t, "\\section{Setup}\\label{sec:setup}\n\n",
            "\\section{Setup}\\label{sec:setup}\n\n%% Writing pass Phase 4, Step 1 (2026-09-15): Figure 2's source sits here so that placeins' [section] barrier lets it take the top of Section 4's first page;\n%% Section 3 refers to it forward (the author's ruling).\n" + fig2 + "\n")
    # the notation box in two columns of six rows at the box's width
    i = t.index("\\begin{center}\n\\fbox{\\begin{minipage}{0.97\\linewidth}\n\\scriptsize\n\\setlength{\\tabcolsep}{3pt}\n\\begin{tabular}{@{}p{0.22\\linewidth}p{0.76\\linewidth}@{}}")
    j = t.index("\\end{minipage}}\n\\end{center}\n", i) + len("\\end{minipage}}\n\\end{center}\n")
    box = t[i:j]
    rows = [l for l in box.split("\n") if l.endswith("\\\\") and " & " in l and not l.startswith("\\multicolumn")]
    assert len(rows) == 12, len(rows)
    col = "\\begin{tabular}[t]{@{}p{0.115\\linewidth}p{0.355\\linewidth}@{}}\n\\midrule\n{rows}\n\\end{tabular}"
    left = col.replace("{rows}", "\n".join(rows[:6]))
    right = col.replace("{rows}", "\n".join(rows[6:]))
    new_box = ("\\begin{center}\n\\fbox{\\begin{minipage}{0.97\\linewidth}\n\\scriptsize\n\\setlength{\\tabcolsep}{2pt}\n"
               "\\noindent\\textbf{Notation.} The terms below are used verbatim throughout.\\par\\vspace{1pt}\n"
               "\\noindent" + left + "\\hfill" + right + "\n\\end{minipage}}\n\\end{center}\n")
    t = t[:i] + new_box + t[j:]
    # Figure 3's height
    t = rep(t, "width=0.5\\linewidth, height=4.1cm, ymin=0.4, ymax=1.0,", "width=0.5\\linewidth, height=3.3cm, ymin=0.4, ymax=1.0,")
    t = rep(t, "legend style={at={(-0.05,-0.3)}, anchor=north,", "legend style={at={(-0.05,-0.34)}, anchor=north,")
    # the cross-model table in \small
    t = rep(t, "\\label{tab:crossmodel}\n\\centering\n\\scriptsize\n", "\\label{tab:crossmodel}\n\\centering\n\\small\n")
    return t


# ----------------------------------------------------------------------------------------------------------------------------------
# Step 2: the prose pass, one section at a time in the author's order
# ----------------------------------------------------------------------------------------------------------------------------------

def sec_S1(t):
    t = rep(t,
        "The first judgment is feeling of knowing (FOK), a classical judgment about one's own memory transferred to an external store \\citep{hart1965,nelson1990,koriat1993}; we call it the coverage judgment.\n"
        "The second, which we call negative-obligation knowledge (NOK) or the obligation judgment, is made before any content is retrieved and asks whether the store holds anything that must be suppressed at all.\n"
        "Prior work on memory scores what an agent retrieves or answers, a different observable at a different time \\citep{longmemeval,locomo,memoryagentbench,stale}; on the conflict questions of a recent benchmark no memory agent exceeds $7\\%$ accuracy \\citep{memoryagentbench}.\n"
        "We measure both judgments on stores we built, so that every label is exact, across three memory backends and language models from three vendors.\n",
        "We call that record, a non-active record whose use would make the answer wrong, the \\emph{forbidding record}.\n"
        "The judgment that such a record exists, made before any content is retrieved, is negative-obligation knowledge (NOK), the obligation judgment.\n"
        "The other judgment is feeling of knowing (FOK), a classical judgment about one's own memory transferred to an external store \\citep{hart1965,nelson1990,koriat1993}; we call it the coverage judgment.\n"
        "Prior work on memory scores what an agent retrieves or answers, a different observable at a different time \\citep{longmemeval,locomo,memoryagentbench,stale}; on MemoryAgentBench's conflict-resolution questions no memory agent exceeds $7\\%$ accuracy \\citep{memoryagentbench}.\n"
        "We measure both judgments on stores we built, so that every label is exact, across three memory backends and six language models from three vendors.\n")
    t = rep(t,
        "Removing the target's name from the list removes the obligation judgment, no model follows the counts, and a reader that knows the question's category separates the counted states where no model does.\n"
        "% AUX-RESP-L1-MINI, AUX-RESP-A1-H45-OWN (the own-name ablation); AUX-CF2-EQUIV-V2R and AUX-V2RCAT-MINI / -H45 (the tallies); AUX-R110-A1-CR (the category-aware count reader)\n"
        "Every score in this paper is an AUROC, the chance that a positive scores above a negative.\n",
        "Removing the target's name from the list removes the obligation judgment, and no model follows the counts.\n"
        "A reader that knows the question's category separates the states the summary only counts, retracted and expired, where no model does.\n"
        "% AUX-RESP-L1-MINI, AUX-RESP-A1-H45-OWN (the own-name ablation); AUX-CF2-EQUIV-V2R and AUX-V2RCAT-MINI / -H45 (the tallies); AUX-R110-A1-CR (the category-aware count reader)\n"
        "Every score in this paper is an AUROC, the chance that a positive scores above a negative, so $0.50$ is chance.\n"
        "A \\emph{gain}, reported as $\\Delta$ in every table, is the indexed score minus the blind score on the same questions.\n")
    t = rep(t,
        "\\end{itemize}\n"
        "Figure~\\ref{fig:framework} shows the two routes: route A is a summary the store maintains outside query time, read by a lookup or by a model, and route B is retrieval that does not mask, returning non-active records with their tags.\n",
        "\\end{itemize}\n"
        "Most of the evidence in this paper concerns the obligation judgment; the coverage judgment rides on the same summary and is reported in Section~\\ref{sec:populations}.\n"
        "Figure~\\ref{fig:framework} shows the two routes.\n"
        "Route A is a summary the store maintains outside query time, read by a lookup or by a model; route B is retrieval that does not mask, returning non-active records with their tags.\n")
    return t


def sec_S5(t):
    t = rep(t,
        "On the counterfactual set, where only the store varies, what the models read is the list of names.\n"
        "The set asks $148$ questions, written before any version of the store existed, of three versions of one store that differ in one attribute, so the same wording gets three labels and the summary is the only input that varies.\n"
        "Blind NOK is $0.50$ by construction, and every AUROC below is also a gain against it.\n"
        "Table~\\ref{tab:cf-main} gives every reader on the whole set and Figure~\\ref{fig:perstate} per state, with two readers that have no model in them.\n"
        "One is the name lookup, a similarity lookup over the superseded-names list; the other is a count reader that knows the question's category and reads that category's retracted and expired \\emph{counts}.\n",
        "When the question is fixed and only the store changes, the models' judgment tracks the attribute names in the summary, not the counts beside them.\n"
        "The counterfactual set asks $148$ questions of three versions of one store that differ in one attribute.\n"
        "The questions were written before any version of the store existed, so the same wording gets three labels and the summary is the only input that varies.\n"
        "Blind NOK is $0.50$ by construction on this set, and every AUROC below is also a gain against it.\n"
        "Table~\\ref{tab:cf-main} gives every reader on the whole set and Figure~\\ref{fig:perstate} per state, with two readers that have no model in them.\n"
        "One is the name lookup, a similarity lookup over the superseded-names list; the other is a count reader that guesses the question's category from its text and reads that category's retracted and expired \\emph{counts}.\n"
        "A category-aware count reader, which takes the category from the manifest, is that reader's oracle upper bound.\n")
    t = rep(t,
        "Taking the target's own name and its nearest neighbours out of the superseded-names list drops GPT-4.1 mini's supersession judgment from $0.86$ to $0.53$ on the full obligation set ($63$ supersession obligations), with both intervals excluding zero.\n"
        "The same edit drops Haiku 4.5's from $0.89$ to $0.68$ with both intervals excluding zero, while Haiku 4.5 keeps $0.69$ on the whole population (Appendix~\\ref{app:resp}).\n",
        "Taking the target's own name and its nearest neighbours out of the superseded-names list drops GPT-4.1 mini's supersession judgment from $0.86$ to $0.53$ on the full obligation set ($63$ supersession obligations), a reliable drop.\n"
        "The same edit drops Haiku 4.5's reliably from $0.89$ to $0.68$, while Haiku 4.5 keeps $0.69$ on the whole population (Appendix~\\ref{app:resp}).\n")
    t = rep(t,
        "The two counted states are separable from the count table, and no model separates them.\n"
        "That reader separates the retracted versions at $0.73$ and the expired versions at $0.78$ on the counterfactual set ($30$ pairs each); every model reads them at $0.53$ to $0.62$ on the same items.\n"
        "No model follows the counts: permuting the lifecycle totals across the store versions moves none of them by more than $0.01$.\n"
        "Moving the obligation's own per-category increment to a sibling version sends a reader of that count to $0.30$ on retraction and $0.36$ on expiry.\n"
        "The same move leaves GPT-4.1 mini at $+0.03$ and $+0.06$ and Haiku 4.5 at $-0.01$ and $-0.05$ against its unmoved rows, so no model followed it (Appendix~\\ref{app:counterfactual}).\n"
        "The count identifies the right version here because the category usually has no other retracted or expired entry ($26$ of $30$ retraction pairs, $15$ of $30$ expiry pairs), so the count goes from zero to one.\n",
        "The retracted and expired states are recoverable from the count table, but no model recovers them.\n"
        "The category-aware reader separates the retracted versions at $0.73$ and the expired versions at $0.78$ on the counterfactual set ($30$ pairs each), where every model scores $0.53$ to $0.62$.\n"
        "The count identifies the right version here because the category usually has no other retracted or expired entry ($26$ of $30$ retraction pairs, $15$ of $30$ expiry pairs), so the count goes from zero to one.\n"
        "No model follows the counts: permuting the lifecycle totals across the store versions moves none of them by more than $0.01$.\n"
        "Moving the obligation's own increment to a sibling version, the moved-count control, sends a count reader below chance and moves no model (Appendix~\\ref{app:counterfactual}).\n")
    t = rep(t,
        "A count cannot say which attribute is retracted or expired.\n"
        "When the summary names those attributes, every model improves (Table~\\ref{tab:cf-main}).\n"
        "Once the summary names the retracted and expired attributes, every model separates the retracted attributes and all but GPT-4.1 mini the expired ones (Table~\\ref{tab:cf-main}).\n"
        "The all-states lookup scores $0.88$ on the whole set, and Haiku 4.5's paired gain on the two counted states is $+0.30$ with both intervals excluding zero.\n",
        "A count cannot say which attribute is retracted or expired.\n"
        "When the summary names those attributes, every model improves (Table~\\ref{tab:cf-main}).\n"
        "Every model then separates the retracted versions, and all but GPT-4.1 mini the expired ones (Figure~\\ref{fig:perstate}).\n"
        "The all-states lookup scores $0.88$ on the whole set, and Haiku 4.5's gain on the two counted states is a reliable $+0.30$.\n")
    t = rep(t,
        "The counted-state evidence rests on $30$ retraction and $44$ expiry pairs, the $30$ plus the $14$ of the descriptive extension draw in Appendix~\\ref{app:counterfactual}. On the full obligation set ($661$ questions) the counted-state rows give only a direction (Section~\\ref{sec:populations}).\n",
        "The counted-state evidence rests on $30$ retraction and $44$ expiry pairs, the $30$ plus the $14$ of the descriptive extension draw in Appendix~\\ref{app:counterfactual}.\n"
        "On the full obligation set the counted-state groups are $26$ retraction and $15$ expiry obligations, and their rows give only a direction (Section~\\ref{sec:populations}).\n")
    return t


def sec_S6(t):
    t = rep(t,
        "Retrieval that keeps the lifecycle tag on every returned record is a second route to the obligation, and it carries the states the list leaves uncounted.\n"
        "Such retrieval is a modification of FR-Bank rather than its stock configuration, because the store's own cosine search runs over every entry, active or not, with the lifecycle mask off.\n"
        "The tag on each returned line comes from the ground-truth join (Appendix~\\ref{app:resp}), and the retrieved view is the five lines that search returns for the question.\n"
        "Without a fetch, a five-item view contains the forbidding record for $54$ of the $104$ obligations on the full obligation set, a reach of $0.52$, and a ten-item view reaches $74$ of them.\n",
        "A retriever that returns non-active records with their tags is a second route to the obligation (route B in Figure~\\ref{fig:framework}).\n"
        "It covers the states the list does not name.\n"
        "A five-record view holds the forbidding record for $54$ of the $104$ obligations on the full obligation set, a reach of $0.52$.\n"
        "Shown that view and no summary, GPT-4.1 mini scores $0.69$ against $0.73$ under the summary; shown both, $0.83$ (Table~\\ref{tab:routes}).\n"
        "The retriever is FR-Bank's own cosine search with its lifecycle mask off, a modification of the stock configuration, and each returned line carries the ground-truth tag (Appendix~\\ref{app:resp}).\n")
    t = rep(t,
        "The tagged view carries the counted states the list misses.\n"
        "A monitor shown the five tagged records and no summary scores $0.69$ on the obligation judgment against the summary's $0.73$ for GPT-4.1 mini on the full obligation set, a difference of $-0.05$ whose intervals include zero (Table~\\ref{tab:routes}).\n"
        "Per state the two routes are mirror images: the tagged view leads the summary on expiry by $+0.24$ and trails it on supersession by $-0.17$, both intervals excluding zero.\n"
        "The reason is that a retrieved entry tagged retracted or expired is a name the summary never lists (Appendix~\\ref{app:resp}).\n"
        "Shown both, GPT-4.1 mini scores $0.83$, a gain of $+0.10$ over the summary alone with both intervals excluding zero, its best monitor.\n"
        "Haiku 4.5 scores $0.79$ shown both against $0.82$ under its summary alone and $0.71$ on the tagged view alone, so the combined monitor is the best measured for GPT-4.1 mini only (Appendix~\\ref{app:resp}).\n",
        "Per state the two routes are mirror images.\n"
        "On the full obligation set the tagged view leads the summary on expiry by a reliable $+0.24$ and trails it on supersession by a reliable $-0.17$.\n"
        "The reason is that a retrieved entry tagged retracted or expired is a name the summary never lists (Appendix~\\ref{app:resp}).\n"
        "Shown both, GPT-4.1 mini gains a reliable $+0.10$ over the summary alone, its best monitor.\n"
        "Haiku 4.5 scores $0.79$ shown both against $0.82$ under its summary alone, so the combined monitor is the best measured for GPT-4.1 mini only (Appendix~\\ref{app:resp}).\n")
    t = rep(t,
        "With the store's own tags instead of ground-truth tags, the same view scores higher. The reason is that the store's tags reach more of the forbidding records, not that there are more tags.\n"
        "With FR-Bank's own tags in place of the ground-truth tags, the view scores the obligation at $0.81$ against $0.69$ for GPT-4.1 mini, a difference of $+0.13$ with both intervals excluding zero.\n"
        "The store's own tags mark $1{,}389$ of the $3{,}305$ lines shown as non-active where the ground-truth tags mark $217$, and $1{,}273$ lines carry a different tag under the store's own tags than under the ground-truth tags.\n"
        "A count of tagged lines scores the obligation at $0.62$ under either source, against the monitor's $0.81$ under the store's own tags, and the tagged-name lookup at $0.65$, so the monitor reads more than density or name match. The four readers with no model in them are in Table~\\ref{tab:routes-full} (Appendix~\\ref{app:resp}).\n"
        "Of the $99$ forbidding records in view, the store's own tags mark $70$ non-active against the ground-truth tags' $60$.\n"
        "The indicator that the item's forbidding record is in view and tagged scores $0.72$ under the store's own tags against $0.67$ under the ground-truth tags, and the monitor exceeds it by $+0.09$.\n",
        "With the store's own tags instead of ground-truth tags, the same view scores higher.\n"
        "FR-Bank's tags mark $1{,}389$ of the $3{,}305$ lines shown as non-active where the ground-truth tags mark $217$, a precision of $0.14$.\n"
        "GPT-4.1 mini's obligation score on that view rises from $0.69$ to a reliable $0.81$ on the full obligation set.\n"
        "More tags is not the reason: a count of tagged lines scores $0.62$ under either tag source.\n"
        "The reason is that the store's tags reach more of the forbidding records, not that there are more tags.\n"
        "Of the $99$ forbidding records in view, the store's tags mark $70$ non-active against the ground-truth tags' $60$, and the indicator that the item's forbidding record is in view and tagged scores $0.72$ against $0.67$.\n"
        "The monitor exceeds that indicator by $+0.09$ (Table~\\ref{tab:routes-full}, Appendix~\\ref{app:resp}).\n")
    # item 38's eight lines: the masked-retriever sentence repeats Section 3's last paragraph ("cannot supply the obligation judgment on its own")
    t = rep(t, "A masked retriever cannot carry this route, because the mask removes exactly the records whose tags carry it.\n", "")
    return t


def sec_S7(t):
    t = rep(t,
        "No tested backend writes the list.\n"
        "FR-Bank overstates: it marks",
        "No tested backend writes the list: FR-Bank over-marks, Mem0 overwrites, and A-MEM's links dangle (Table~\\ref{tab:census}).\n"
        "FR-Bank marks")
    t = rep(t,
        "FR-Bank's own metadata leaves GPT-4.1 mini and the name lookup close to chance and costs Haiku 4.5 about a quarter of its gain.\n"
        "GPT-4.1 mini and the lookup score $0.60$ and $0.59$ capped and $0.65$ and $0.66$ lifted on the obligation judgment, while Haiku 4.5 scores $0.71$ capped and $0.74$ lifted.\n"
        "Haiku 4.5 keeps $72\\%$ of its gain capped, with a profile lower bound of $0.59$, and $79\\%$ lifted (Table~\\ref{tab:levels}).\n",
        "FR-Bank's own metadata leaves GPT-4.1 mini and the name lookup close to chance and costs Haiku 4.5 about a quarter of its gain.\n"
        "The store-written summary is read capped (with the renderer's fifteen-name cap in place) and lifted (with the cap removed).\n"
        "On the full obligation set GPT-4.1 mini and the lookup score $0.60$ and $0.59$ capped and $0.65$ and $0.66$ lifted, while Haiku 4.5 scores $0.71$ capped and $0.74$ lifted.\n"
        "Haiku 4.5 keeps $72\\%$ of its gain capped and $79\\%$ lifted (Table~\\ref{tab:levels}).\n")
    t = rep(t,
        "Where the store still writes the item's own name Haiku 4.5 scores it at its ground-truth level, and where it does not the model falls to the floor the own-name ablation found.\n"
        "Haiku 4.5 scores $0.87$ against $0.89$ under the ground-truth summary on the $53$ of the $63$ supersession obligations whose name survives under the lifted rendering, and $0.68$ on the $10$ whose name is gone.\n"
        "That floor is the own-name ablation's, $0.69$ on the whole population after the item's own name is removed (Section~\\ref{sec:counterfactual}).\n",
        "Where the store still writes the item's own name Haiku 4.5 scores it at its ground-truth level, and where it does not the model falls to the floor the own-name ablation found.\n"
        "That floor is the score after the target's own name is removed from the list.\n"
        "On the $53$ of the $63$ supersession obligations whose name survives under the lifted rendering, Haiku 4.5 scores $0.87$ against $0.89$ under the ground-truth summary, and $0.68$ on the $10$ whose name is gone.\n"
        "It is $0.69$ on the whole population (Section~\\ref{sec:counterfactual}).\n")
    return t


def sec_S8(t):
    t = rep(t,
        "The obligation gain replicates across models, and the coverage margin lives on ordinary records.\n"
        "Every paired obligation gain excludes zero where the blind score varies (Tables~\\ref{tab:crossmodel} and~\\ref{tab:e1}), and on the cross-model set the five models with a varying blind score gain $+0.15$ to $+0.45$ (Appendix~\\ref{app:laddertable}).\n"
        "On the full obligation set the name lookup scores $0.75$ against GPT-4.1 mini's $0.73$, inside tolerance.\n"
        "Haiku 4.5, Opus 5 and GPT-5.6 Luna sit $+0.07$ to $+0.08$ above it, with item-level intervals excluding zero and persona-grouped intervals including it (Appendix~\\ref{app:baselines}).\n",
        "The obligation gain replicates across six models from three vendors.\n"
        "Every paired gain excludes zero where the blind score varies, on the cross-model set (Table~\\ref{tab:crossmodel}) and on the full obligation set (Table~\\ref{tab:e1}).\n"
        "On the full obligation set the name lookup scores $0.75$ against GPT-4.1 mini's $0.73$, within tolerance.\n"
        "Haiku 4.5, Opus 5 and GPT-5.6 Luna sit $+0.07$ to $+0.08$ above it, with item-level intervals excluding zero and persona-grouped intervals including it (Appendix~\\ref{app:baselines}).\n")
    # item 41, "cut the rest": the two lookup-tolerance sentences (the 0.75 stands in Table 6's note beside the 0.73 row; the differences in Appendix E.8)
    t = rep(t,
        "On the full obligation set the name lookup scores $0.75$ against GPT-4.1 mini's $0.73$, within tolerance.\n"
        "Haiku 4.5, Opus 5 and GPT-5.6 Luna sit $+0.07$ to $+0.08$ above it, with item-level intervals excluding zero and persona-grouped intervals including it (Appendix~\\ref{app:baselines}).\n", "")
    t = rep(t,
        "The coverage margin lives on ordinary records, and on the hard tier the coverage result is the obligation result restated.\n"
        "On the hard tier the two judgments are label-identical, and the name lookup scores coverage there at $0.79$ against the model's $0.70$ with both intervals of that $-0.09$ including zero (Appendix~\\ref{app:baselines}).\n"
        "On the easy tier the positives are ordinary present records, and the model scores $0.78$ against the lookup's $0.61$, a margin of $+0.18$ with both intervals excluding zero.\n"
        "FOK does not detect a deleted record: against facts the user never had it improves from $0.55$ to $0.88$, while against a record we deleted it moves from $0.43$ to $0.50$ and stays at chance.\n"
        "The single missing record is therefore NOK's target.\n"
        "The score ranks well and calibrates badly (Appendix~\\ref{app:posthoc}), so a deployed monitor thresholds at the base rate of positives.\n",
        "The coverage margin lives on ordinary records.\n"
        "On the easy tier ($354$ questions), where the positives are ordinary present records, GPT-4.1 mini scores $0.78$ against the name lookup's $0.61$, a reliable margin of $+0.18$.\n"
        "On the hard tier every coverage positive is an obligation, so the FOK row is the NOK row relabeled, and the lookup's $0.79$ against the model's $0.70$ is not a reliable difference (Appendix~\\ref{app:baselines}).\n"
        "Against a record we deleted, FOK moves from $0.43$ to $0.50$ and stays at chance, so the single missing record is NOK's target.\n"
        "The score ranks well and calibrates badly (Appendix~\\ref{app:posthoc}), so a deployed monitor thresholds at the base rate of positives.\n")
    return t


def sec_S9(t):
    t = sec_S9_body(t)
    t = rep(t,
        "As a rate over the reached scorable obligations, GPT-4.1 mini gives the stale value in $0.19$ of cases under retrieval alone and $0.19$ under the oracle, with the gated rules between and every Wilson interval overlapping (Table~\\ref{tab:ds-body}).\n",
        "As a rate over the reached scorable obligations, GPT-4.1 mini gives the stale value in $0.19$ of cases under retrieval alone and $0.19$ under the oracle.\n"
        "The gated rules fall between, and every Wilson interval overlaps (Table~\\ref{tab:ds-body}).\n")
    t = rep(t,
        "Retagging the $35$ duplicates the audit found cuts stale answers under the gated fetch from $0.15$ to $0.03$ of the reached obligations for GPT-4.1 mini and from $0.37$ to $0.23$ for Haiku~4.5, the correct count untouched.\n",
        "Retagging the $35$ duplicates the audit found cuts stale answers under the gated fetch from $0.15$ to $0.03$ of the reached obligations for GPT-4.1 mini.\n"
        "For Haiku~4.5 the rate falls from $0.37$ to $0.23$, and the correct count is untouched for both.\n")
    return t


def sec_S9_body(t):
    # Table 7 gains the Wilson interval of the stale rate (item 43); the values of tab:ds-body-lower at two decimals
    t = rep(t, "\\begin{tabular}{@{}lrrlr@{}}\n\\toprule\nPolicy & \\hd{Forbidding records}{in view (of $104$)} & \\hd{Stale answers}{(of $104$)} & \\hdl{Stale rate over the}{reached, scorable} & \\hd{Correct}{(of $174$)} \\\\",
               "\\begin{tabular}{@{}lrrllr@{}}\n\\toprule\nPolicy & \\hd{Forbidding records}{in view (of $104$)} & \\hd{Stale answers}{(of $104$)} & \\hdl{Stale rate over the}{reached, scorable} & \\hdl{Wilson}{interval} & \\hd{Correct}{(of $174$)} \\\\")
    for old, new in [
        ("Top-5 retrieval & $54$ & $9$ & $8$ of $42$, $0.19$ & $46$ \\\\", "Top-5 retrieval & $54$ & $9$ & $8$ of $42$, $0.19$ & $[0.10,0.33]$ & $46$ \\\\"),
        ("Model rule & $85$ & $9$ & $8$ of $62$, $0.13$ & $44$ \\\\", "Model rule & $85$ & $9$ & $8$ of $62$, $0.13$ & $[0.07,0.23]$ & $44$ \\\\"),
        ("Lookup rule & $85$ & $7$ & $6$ of $58$, $0.10$ & $40$ \\\\", "Lookup rule & $85$ & $7$ & $6$ of $58$, $0.10$ & $[0.05,0.21]$ & $40$ \\\\"),
        ("Model rule, all states named and scored & $89$ & $12$ & $11$ of $65$, $0.17$ & $44$ \\\\", "Model rule, all states named and scored & $89$ & $12$ & $11$ of $65$, $0.17$ & -- & $44$ \\\\"),
        ("Literal lookup rule (descriptive) & $94$ & $14$ & $13$ of $82$, $0.16$ & $46$ \\\\", "Literal lookup rule (descriptive) & $94$ & $14$ & $13$ of $82$, $0.16$ & $[0.10,0.25]$ & $46$ \\\\"),
        ("Oracle & $99$ & $17$ & $16$ of $85$, $0.19$ & $46$ \\\\", "Oracle & $99$ & $17$ & $16$ of $85$, $0.19$ & $[0.12,0.28]$ & $46$ \\\\"),
    ]:
        t = rep(t, old, new)
    t = rep(t, "The detector's $0.80$ threshold gives zero stale answers under every policy. The items on which each rule fires, the reach as a rate, the Wilson interval of the stale rate, the mean view size, tagged records and coverage are in Table~\\ref{tab:ds-body-lower} (Appendix~\\ref{app:resp}).",
               "The preregistered reading is stale use at the detector's $0.80$ threshold over the obligations whose forbidding record is in view and tagged, and it is zero under every policy. The counts and rates here are the descriptive reading at $0.50$. The items on which each rule fires, the reach as a rate, the mean view size, tagged records and coverage are in Table~\\ref{tab:ds-body-lower} (Appendix~\\ref{app:resp}).")
    t = rep(t,
        "Gating a lifecycle fetch on the obligation judgment reaches far more forbidding records than retrieval alone at the same budget.\n"
        "The reach rises from $0.52$ to $0.82$ of the obligations at a mean view of $7.08$ records, where a seven-item retrieval view reaches $0.60$; the lookup's rule reaches the same $0.82$ and the oracle $0.95$ (Table~\\ref{tab:ds-body}).\n",
        "Gating a lifecycle fetch on the obligation judgment reaches far more forbidding records than retrieval alone at the same budget.\n"
        "On the full obligation set the reach rises from $0.52$ to $0.82$ of the obligations at a mean view of about seven records, where a seven-record retrieval view reaches $0.60$.\n"
        "The lookup rule reaches the same $0.82$ and the oracle $0.95$ (Table~\\ref{tab:ds-body}).\n")
    t = rep(t,
        "Tags in view are respected, and the stale answers come from a duplicate the store keeps active.\n"
        "GPT-4.1 mini gives the stale value on $0$ of the $50$ views where every stale line is tagged or absent, and each of its $16$ stale answers under the oracle falls on a view with an untagged duplicate.\n"
        "% AUX-DS-AUDIT-SOURCE, AUX-DS-AUDIT-READ\n"
        "As a rate over the scorable obligations each policy reaches, GPT-4.1 mini gives the stale value in $0.19$ of cases under retrieval alone and $0.19$ under the oracle, and Haiku 4.5 in $0.26$ and $0.22$.\n"
        "The counts in Table~\\ref{tab:ds-body} therefore grow with the reached set while the rate holds.\n"
        "Of the $89$ scorable obligation views, $35$ carry an active line asserting the stale value, the retained obsolete assertions Section~\\ref{sec:backends} censused.\n",
        "Stale answers do not fall under the gated fetch, because the store keeps an untagged active duplicate of the superseded content.\n"
        "Of the $89$ scorable obligation views, $35$ carry an active line asserting the stale value, the retained obsolete assertions Section~\\ref{sec:backends} censused.\n"
        "% AUX-DS-AUDIT-SOURCE, AUX-DS-AUDIT-READ\n"
        "Tags in view are respected: GPT-4.1 mini gives the stale value on $0$ of the $50$ views where every stale line is tagged or absent.\n"
        "Each of its $16$ stale answers under the oracle falls on a view with an untagged duplicate.\n"
        "As a rate over the reached scorable obligations, GPT-4.1 mini gives the stale value in $0.19$ of cases under retrieval alone and $0.19$ under the oracle, with the gated rules between and every Wilson interval overlapping (Table~\\ref{tab:ds-body}).\n")
    t = rep(t,
        "Correct answers are bounded by the view and by whether the prompt binds the entries to the person asking.\n"
        "The licensed record is in the view for $65$ of the $174$ items.\n"
        "A header naming the persona and the date raises in-view correct answers from $37$ to $48$ for GPT-4.1 mini and from $38$ to $59$ for Haiku 4.5, both intervals above zero (Appendix~\\ref{app:resp}).\n"
        "% AUX-DS-AUDIT-RANK, AUX-DS-AUDIT-IDENTITY, AUX-DS-A4-STAGE2-*\n"
        "\n"
        "%% R110: the repair, src/amend5_e10.tex's Section 8 sentence split for the length rule (AUX-DS-A5-STAGE2-MINI / -H45, -CHANGED-*, -FIRSTSENT-*).\n"
        "Tagging the store's untagged duplicates, and nothing else, removes most of the stale answers; the fix belongs in the write path.\n"
        "Retagging the $35$ duplicates the audit found cuts stale answers under the gated fetch from $0.15$ to $0.03$ of the reached obligations for GPT-4.1 mini and from $0.37$ to $0.23$ for Haiku~4.5, the correct count untouched.\n"
        "Haiku~4.5's residual comes from tagged lines, mostly a mention of the tagged content beyond the answer's first sentence (Table~\\ref{tab:ds-a5}, Appendix~\\ref{app:resp}).\n",
        "%% R110: the repair, src/amend5_e10.tex's Section 8 sentence split for the length rule (AUX-DS-A5-STAGE2-MINI / -H45, -CHANGED-*, -FIRSTSENT-*).\n"
        "Tagging the store's untagged duplicates, and nothing else, removes most of the stale answers; the fix belongs in the write path.\n"
        "Retagging the $35$ duplicates the audit found cuts stale answers under the gated fetch from $0.15$ to $0.03$ of the reached obligations for GPT-4.1 mini and from $0.37$ to $0.23$ for Haiku~4.5, the correct count untouched.\n"
        "Haiku~4.5's residual comes from tagged lines, mostly a mention of the tagged content beyond the answer's first sentence (Table~\\ref{tab:ds-a5}, Appendix~\\ref{app:resp}).\n"
        "\n"
        "Three further results are stated in one sentence each.\n"
        "A header naming the persona and the date raises in-view correct answers from $37$ to $48$ for GPT-4.1 mini and from $38$ to $59$ for Haiku 4.5, both reliable (Appendix~\\ref{app:resp}).\n"
        "% AUX-DS-AUDIT-RANK, AUX-DS-AUDIT-IDENTITY, AUX-DS-A4-STAGE2-*\n"
        "%%DEPTH-COMPOSITE%%\n")
    t = rep(t,
        "The coverage judgment sets the depth of the view, and the extra lines land on the licensed items.\n"
        "For Haiku~4.5 the expanded view matches a ten-line view's correct count at $8.3$ lines, $+0.04$ over a flat view of equal cost with both intervals excluding zero.\n"
        "GPT-4.1 mini gains $+0.02$ under the same comparison, with intervals including zero (Table~\\ref{tab:ds-a6}, Appendix~\\ref{app:resp}).\n",
        "%%DEPTH%%\n")
    t = rep(t,
        "A composite that scores each policy on all three jobs at once rises under the gated fetch for GPT-4.1 mini and stays level for Haiku 4.5.\n"
        "It counts a licensed item answered correctly, an obligation reached and reported, and an absent item abstained on. Under the model rule it rises by $+0.03$ against retrieval alone for GPT-4.1 mini with both intervals excluding zero, and for Haiku 4.5 by a rate whose intervals include zero (Table~\\ref{tab:ds-a7}, Appendix~\\ref{app:resp}).\n",
        "%%COMPOSITE%%\n")
    t = rep(t, "%%DEPTH-COMPOSITE%%\n",
               "Where the coverage judgment expands the view, Haiku~4.5 matches a ten-line view's correct count at $8.3$ lines, a reliable $+0.04$ over a flat view of equal cost (Table~\\ref{tab:ds-a6}, Appendix~\\ref{app:resp}).\n"
               "A composite over all three jobs rises under the model rule by a reliable $+0.03$ against retrieval alone for GPT-4.1 mini and stays level for Haiku 4.5 (Table~\\ref{tab:ds-a7}, Appendix~\\ref{app:resp}).\n"
               "It counts a licensed item answered correctly, an obligation reached and reported, and an absent item abstained on.\n")
    t = rep(t, "%%DEPTH%%\n", "")
    t = rep(t, "%%COMPOSITE%%\n", "")
    return t


def sec_S3(t):
    t = rep(t, "The gain, reported as $\\Delta$ in every table, is the indexed score minus the blind score on the same questions.\n", "")
    t = rep(t, "n.a.\\ is a combination the question construction does not produce.}", "n.a.\\ means a combination the question construction never produces.}")
    t = rep(t, "n.a. is a combination the definition does not assign because the question construction never produces it (Appendix E.3).",
               "n.a. is a combination the definition does not assign because the question construction never produces it (Appendix E.3, where the intent is typed structurally).")
    t = rep(t,
        "Listing~\\ref{lst:summary} is what the indexed monitor sees: counts per category and state, and names with no values.\n"
        "Every result in this paper rests on the name map.\n"
        "The count table is carried because it was part of the summary as fixed before the study and was tested (Section~\\ref{sec:counterfactual}, Appendix~\\ref{app:counterfactual}).\n"
        "The name map carries only superseded content, so an entry that expires or is retracted reaches the summary as a count and is never named.\n"
        "Section~\\ref{sec:counterfactual} also tests an all-states summary that names all three non-active states; Figure~\\ref{fig:example} shows both cases on real store versions.\n",
        "Listing~\\ref{lst:summary} is what the indexed monitor sees: counts per category and state, and names with no values.\n"
        "Every result in this paper rests on the name map, which carries only superseded content: an entry that expires or is retracted reaches the summary as a count and is never named.\n"
        "The count table is carried because it was part of the summary as fixed before the study, and Section~\\ref{sec:counterfactual} also tests an all-states summary that names all three non-active states (Figure~\\ref{fig:example}).\n"
        "\n"
        "%% Writing pass Phase 4 (2026-09-15), items 14 and 88: Section 2's framing moved here as plain framing, no claim of precedent.\n"
        "The summary route is retrieval over a metadata index.\n"
        "The store maintains, outside query time, an index of what it holds and in which lifecycle state, with every value removed, and the monitor is a reader of that index.\n"
        "The name lookup is the plainest such reader, a retriever that scores the question against the index's names.\n")
    t = rep(t,
        "Under the mask a lifecycle record that changes intent-conditional coverage ranks below $k$ common items, so two stores can present identical retrieved sets while only one holds the forbidding record.\n"
        "Every decision rule over the monitor's output then errs on at least half of such pairs (supplement).\n",
        "Under the mask a lifecycle record that changes intent-conditional coverage ranks below $k$ common items, so two stores can present identical retrieved sets while only one holds the forbidding record.\n")
    return t


def sec_S4(t):
    t = rep(t,
        "Labels follow Definition~\\ref{def:coverage}; every \\pn{} label was verified by hand from the judgments that compose it, and a presence control confirms that each target is stored, so a mislabeled \\absent{} item is unlikely ($5.2\\%$ at the observed base rate; Appendix~\\ref{app:construction}).\n",
        "Labels follow Definition~\\ref{def:coverage}, and every \\pn{} label was verified by hand from the judgments that compose it.\n"
        "A presence control confirms that each target is stored, so a mislabeled \\absent{} item is unlikely ($5.2\\%$ at the observed base rate; Appendix~\\ref{app:construction}).\n")
    t = rep(t,
        "FR-Bank is the lifecycle-tracking store of \\mbox{\\citet{fr}}, the one evaluated store that records a lifecycle state on every entry; its stock configuration masks non-active records from retrieval, and retraction records pass that mask at $5\\%$ (Appendix~\\ref{app:census}).\n"
        "Mem0 (\\texttt{mem0ai} 1.0.5) overwrites the record it exposes and A-MEM links notes \\citep{mem0,amem}; neither records lifecycle structure, so this paper calls them the structureless backends.\n"
        "The models are GPT-4.1 mini, GPT-5.6 Luna and GPT-5.6 Sol from one family in ascending size and price, Anthropic's Opus 5 and Haiku 4.5, and Kimi K3 with open weights.\n"
        "Table~\\ref{tab:setup} names every population with its size, its positives and the models that ran on it, and every later number is stated on one of them.\n",
        "FR-Bank \\citep{fr} is the only backend that tags every entry with a lifecycle state; its stock configuration masks non-active records from retrieval, and retraction records pass that mask at $5\\%$ (Appendix~\\ref{app:census}).\n"
        "Mem0 (\\texttt{mem0ai} 1.0.5) overwrites the record it exposes and A-MEM links notes \\citep{mem0,amem}; neither records lifecycle structure, so this paper calls them the structureless backends.\n"
        "The models are OpenAI's GPT-4.1 mini, GPT-5.6 Luna and GPT-5.6 Sol, in ascending size and price, Anthropic's Haiku 4.5 and Opus 5, and Moonshot's Kimi K3 with open weights.\n"
        "GPT-4.1 mini ran the main study at one call per question, and Opus 5, Haiku 4.5 and GPT-5.6 Luna ran every population at five calls.\n"
        "GPT-5.6 Sol and Kimi K3 ran the cross-model set only, their full-population runs stopped at the budget.\n"
        "Table~\\ref{tab:setup} names every population with its size, its positives and the models that ran on it, and every later number is stated on one of them.\n")
    t = rep(t,
        "It binds on the store's own metadata, so the lifted rendering is reported beside the capped figure (Appendix~\\ref{app:repro}).\n"
        "The sixty-percent retention line was fixed before the main study, on 10 August 2026, for coverage and inherited unchanged for the obligation judgment, a conventional threshold with no recorded reason for its value.\n",
        "It binds on the store's own metadata, so the lifted rendering is reported beside the capped figure (Appendix~\\ref{app:repro}).\n")
    t = rep(t,
        "The name lookup scores each question by its maximum cosine similarity, under a small local sentence encoder, to the names in the summary's superseded list.\n"
        "It has no model in it and is the baseline every model is measured against (Appendix~\\ref{app:baselines}).\n"
        "The item-level paired bootstrap interval is primary and the interval grouped by persona is the sensitivity; where they disagree the wider decides, and two scores are within tolerance at $\\pm0.05$.\n"
        "On the counterfactual set the persona-grouped interval is the one printed, because resampling whole questions keeps each triple intact.\n"
        "Probes on the question text alone reach $0.80$ to $0.97$ (Appendix~\\ref{app:questionprior}), so no absolute blind level here is a finding; the evidence is the paired gain on identical questions and the counterfactual set.\n",
        "The name lookup scores each question by its maximum cosine similarity, under the sentence encoder \\texttt{all-MiniLM-L6-v2}, to the names in the summary's superseded list.\n"
        "It has no model in it and is the baseline every model is measured against (Appendix~\\ref{app:baselines}).\n"
        "We report the item-level paired bootstrap interval first and the persona-grouped interval second, and where they disagree the wider decides.\n"
        "We call a difference \\emph{reliable} when both intervals exclude zero, and \\emph{within tolerance} when $|\\Delta| \\le 0.05$.\n"
        "On the counterfactual set the persona-grouped interval is the one printed, because resampling whole questions keeps each triple intact.\n"
        "Question wording alone carries much of a blind score: probes on the question text reach $0.80$ to $0.97$ (Appendix~\\ref{app:questionprior}), which is why we report paired gains and the counterfactual set.\n")
    return t


def sec_S2(t):
    i = t.index("The judgment this paper isolates is made before retrieval and about the store itself, which the memory benchmarks do not score.\n")
    j = t.index("\\section{Framework}\\label{sec:framework}")
    new = (
        "%% Writing pass Phase 4 (2026-09-15), items 13 to 16: three paragraphs with plain topic sentences; the finding and the framing out (items 3, 14, 88);\n"
        "%% the knowledge-conflict and temporal-LM work cited (item 15); STALE's citation on its name (item 16).\n"
        "Metamemory studies judgments about one's own memory, and two of its judgments transfer to an external store.\n"
        "Classical work treats monitoring as a judgment about memory state \\citep{nelson1990,koriat1996}, and this paper asks the same two questions of a store the agent does not own.\n"
        "\n"
        "Adaptive retrieval, abstention and calibration each decide something before or about an answer, and none has an external store to be right about.\n"
        "Adaptive retrieval decides whether to query a static corpus from parametric or generated-content signals \\citep{lewis2020,flare,mallen2023,ren2025,wang2023,selfrag,su2024,seakr,verbrouting,metamem}, abstention benchmarks score whether a question admits an answer \\citep{rajpurkar2018,kamath2020,yang2024,abstentionbench}, and calibration work scores confidence in an answer \\citep{kadavath2022,lin2022,tian2023,xiong2024}.\n"
        "Those that retrieve observe a bounded view rather than a maintained summary (Section~\\ref{sec:framework}).\n"
        "\n"
        "Memory systems and memory benchmarks score what is retrieved or answered, after retrieval.\n"
        "One line trains the loop that writes, updates and queries a store \\citep{automem,supersede}; long-term stores \\citep{packer2023,zhong2024,zhang2025survey,mem0,amem} and remembered-answer benchmarks \\citep{longmemeval,locomo} measure what comes out once memory has been consulted.\n"
        "Reliance on obsolete memory \\citep{memora}, conflict resolution across turns \\citep{memoryagentbench} and, closest to this paper, recognition that a memory the agent holds is no longer valid, STALE \\citep{stale}, are scored after retrieval too.\n"
        "The benchmarks that grade obligations supplied by policy or after the fact \\citep{nissenbaum2004,cimemories,maini2024,gatemem,pmbench,hushbench,statemembench} grade an outcome once a cue or a revision has arrived.\n"
        "Obsolete-versus-current conflict inside a store is the phenomenon that knowledge-conflict and temporal work studies inside a model \\citep{xu2024conflicts,longpre2021,dhingra2022}.\n"
        "What this paper measures is the judgment made before retrieval, about the store itself, from the content's own lifecycle state.\n"
        "\n")
    return t[:i] + new + t[j:]


def sec_LIM(t):
    t = rep(t,
        "One closed model family supplies the primary capability comparison, and two runs stopped at the budget on the full populations.\n",
        "One closed model family supplies the primary capability comparison, and two runs stopped at the budget on the full populations.\n"
        "The sixty-percent retention line was a conventional threshold, fixed before the main study, with no recorded reason for its value.\n")
    return t


def sec_CON(t):
    t = rep(t,
        "What the models read in a lifecycle summary is the list of names, and the counts beside it carry nothing to them.\n"
        "The name of the stale attribute supplies the judgment.\n"
        "The counts supply none of it, for any model.\n"
        "A lookup over the names is a baseline two of the three models do not exceed.\n"
        "Tags on returned records are the other route, and no tested backend writes the list.\n"
        "FR-Bank's own metadata is enough for Haiku 4.5 wherever it still writes the name, and not enough for GPT-4.1 mini or the name lookup anywhere.\n"
        "The stale answers downstream come from duplicates the store keeps active, so the fix is in the write path.\n",
        "What the models read in a lifecycle summary is the list of names, and the counts beside it carry nothing to them.\n"
        "Tags on returned records are the other route, and no tested backend writes the list.\n"
        "The stale answers downstream come from duplicates the store keeps active, so the fix is in the write path.\n")
    t = rep(t,
        "Maintain the list of attribute names that hold non-active content, superseded, retracted and expired alike: a similarity lookup reads a clean list, and over the list a real store writes, spend the model call, which exceeds the lookup by $+0.08$ lifted and $+0.12$ capped under the store's own metadata (Sections~\\ref{sec:counterfactual} and~\\ref{sec:backends}).\n",
        "Maintain the list of attribute names that hold non-active content, superseded, retracted and expired alike: a similarity lookup reads a clean list, and over the list a real store writes, spend the model call (Sections~\\ref{sec:counterfactual} and~\\ref{sec:backends}).\n")
    return t


SECTIONS = {"S1": sec_S1, "S5": sec_S5, "S6": sec_S6, "S7": sec_S7, "S8": sec_S8, "S9": sec_S9, "S3": sec_S3, "S4": sec_S4, "S2": sec_S2, "LIM": sec_LIM, "CON": sec_CON}


# ----------------------------------------------------------------------------------------------------------------------------------
# Step 3: the three levers, in the author's order, only while page 9 does not hold
# ----------------------------------------------------------------------------------------------------------------------------------

def lever1(t):
    """the contributions to 30 words a bullet"""
    old_items = t[t.index("\\begin{itemize}\\setlength{\\itemsep}{1pt}\n"):t.index("\\end{itemize}\n") + len("\\end{itemize}\n")]
    new_items = (
        "\\begin{itemize}\\setlength{\\itemsep}{1pt}\n"
        "\\item We define two pre-retrieval judgments about a memory store, FOK (coverage) and NOK (obligation), with an intent-conditional coverage label and a value-free lifecycle summary as the monitor's input (Definitions~\\ref{def:coverage} and~\\ref{def:index}).\n"
        "\\item We build a counterfactual test in which one question is asked of three store versions differing in a single attribute ($n=444$), so the summary is the only input that varies.\n"
        "\\item We show that monitors read the summary's \\emph{names}, not its counts: the name lookup matches two of three models on the named state, and none reads counted states until named.\n"
        "\\item We show that unmasked retrieval returning non-active records \\emph{with their tags} is a second route to what the list misses, and that no tested backend writes a usable list.\n"
        "\\item We show downstream that gating retrieval on the judgment reaches more forbidding records but does not reduce stale answers; tagging the untagged duplicates the store keeps does.\n"
        "\\end{itemize}\n")
    return t.replace(old_items, new_items)


def lever2(t):
    """Figure 2 to the retraction triple; the supersession triple to C.2 (the appendix edit is in wp_phase4_appendix)"""
    i = t.index("\\multicolumn{4}{@{}l}{\\textbf{Row one, a supersession triple.}")
    j = t.index("\\multicolumn{4}{@{}l}{\\textbf{Row two, a retraction triple.}")
    t = t[:i] + t[j:]
    t = t.replace("Row two, a retraction triple.}", "A retraction triple.}")
    t = rep(t, "\\caption{Two triples of the counterfactual set. The question is fixed; the three store versions differ in one attribute. Only the summary lines that differ are shown, with the name lookup's score under each. In row one the obligation is named and the lookup separates the versions; in row two only the count row differs and no reader over names can.}",
               "\\caption{A retraction triple of the counterfactual set. The question is fixed; the three store versions differ in one attribute, and only the summary lines that differ are shown, with the name lookup's score under each. Only the count row differs, so no reader over names can separate the versions; the supersession triple, where the obligation is named and the lookup separates the versions, is in Appendix~\\ref{app:counterfactual}.}")
    return t


def lever3(t):
    """the cross-model table to Appendix A with one Section 8 sentence (item 84 option b); the appendix edit is in wp_phase4_appendix"""
    i = t.index("\\begin{table}[h]\n%% Writing pass Phase 3 (2026-09-15), item 84 (a)")
    j = t.index("\\end{table}\n", i) + len("\\end{table}\n")
    t = t[:i] + t[j:]
    t = rep(t, "Every paired gain excludes zero where the blind score varies, on the cross-model set (Table~\\ref{tab:crossmodel}) and on the full obligation set (Table~\\ref{tab:e1}).\n",
               "Every paired gain excludes zero where the blind score varies, on the cross-model set (Table~\\ref{tab:ladder-exact}, Appendix~\\ref{app:laddertable}) and on the full obligation set (Table~\\ref{tab:e1}).\n"
               "On the cross-model set the five models with a varying blind score gain $+0.15$ to $+0.45$, Kimi K3 among them at $+0.26$.\n")
    return t


APPX = SRC / "appendix_v18.tex"
SUP_TRIPLE = (
    "%% Writing pass Phase 4, Step 3 (2026-09-15), lever 2: the supersession triple of Figure 2 moved here; the retraction triple stays in the body (reviews/NUMBERS_R110.md AUX-R110-FIG2).\n"
    "\\begin{table}[H]\n"
    "\\caption{The supersession triple of the counterfactual set that Figure~\\ref{fig:example} leaves out: the question is fixed, the three store versions differ in one attribute, and only the summary lines that differ are shown, with the name lookup's score under each. The obligation is named, and the lookup separates the versions.}\n"
    "\\label{tab:sup-triple}\n"
    "\\centering\n"
    "\\footnotesize\n"
    "\\setlength{\\tabcolsep}{5pt}\n"
    "\\begin{tabular}{@{}>{\\raggedright\\arraybackslash}p{0.27\\linewidth}>{\\raggedright\\arraybackslash}p{0.21\\linewidth}>{\\raggedright\\arraybackslash}p{0.23\\linewidth}>{\\raggedright\\arraybackslash}p{0.21\\linewidth}@{}}\n"
    "\\multicolumn{4}{@{}l}{Question: \\textit{What is my current work style or preference?}}\\\\\n"
    "\\toprule\n"
    "summary line & version 1: \\present{} & version 2: \\pn{} & version 3: \\absent{}\\\\\n"
    "\\midrule\n"
    "lifecycle total, superseded & \\texttt{0} & \\texttt{1} & \\texttt{0}\\\\\n"
    "\\texttt{PREFERENCES\\_HABITS}: entries, active, superseded & \\texttt{46, 46, 0} & \\texttt{47, 46, 1} & \\texttt{45, 45, 0}\\\\\n"
    "names carrying superseded content & \\texttt{(none)} & \\texttt{work\\_preference} & \\texttt{(none)}\\\\\n"
    "the name lookup's score & $0.00$ & $0.73$ & $0.00$\\\\\n"
    "the label & a current value, licensed & the old value must not be used & no such record\\\\\n"
    "\\bottomrule\n"
    "\\end{tabular}\n"
    "\\end{table}\n")


def appendix_lever2():
    a = io.open(APPX, encoding="utf-8").read()
    anchor = "\\subsection{Store-counterfactual set}\\label{app:counterfactual}\n\n"
    if "tab:sup-triple" in a:
        return
    assert a.count(anchor) == 1
    a = a.replace(anchor, anchor + SUP_TRIPLE + "\n")
    io.open(APPX, "w", encoding="utf-8", newline="\n").write(a)


def appendix_reset():
    src = subprocess.run(["git", "show", "6dbabdf:reviews/v18/src/appendix_v18.tex"], cwd=ROOT, capture_output=True).stdout.decode("utf-8")
    io.open(APPX, "w", encoding="utf-8", newline="\n").write(src.replace("\r\n", "\n"))


LEVERS = [lever1, lever2, lever3]


def main():
    step = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--step=")), "2")
    src = subprocess.run(["git", "show", "6dbabdf:reviews/v18/src/body_v18.tex"], cwd=ROOT, capture_output=True).stdout.decode("utf-8")
    io.open(BODY, "w", encoding="utf-8", newline="\n").write(src.replace("\r\n", "\n"))
    r = subprocess.run([sys.executable, str(TOOLS / "wp_phase3.py")], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-800:]
    t = io.open(BODY, encoding="utf-8").read()
    t = step1(t)
    done = ["step 1"]
    if step.startswith("2") or step.startswith("3"):
        upto = step.split(":", 1)[1] if step.startswith("2:") else None
        for s in ORDER:
            t = SECTIONS[s](t); done.append(s)
            if s == upto:
                break
    appendix_reset()
    if step.startswith("3"):
        n = int(step.split(":", 1)[1]) if ":" in step else len(LEVERS)
        for k in range(n):
            t = LEVERS[k](t); done.append(f"lever {k + 1}")
            if k == 1:
                appendix_lever2()
    io.open(BODY, "w", encoding="utf-8", newline="\n").write(t)
    print("wp_phase4: " + ", ".join(done))


if __name__ == "__main__":
    main()
