# -*- coding: utf-8 -*-
"""appendix_v18.py -- derive reviews/v18/src/appendix_v18.tex from reviews/v17/src/appendix_v17.tex (CC_PASS_v18, R110).

Every edit is an exact replacement asserted to occur once, in order; the carried-block markers (%%V11:a-b%%) are untouched and resolve at build
time (build_v18.py). Edits, by appendix: C.2 (the count readers, the increment moved within the triple, score resolution, the lookup at 100 and
200 names, the paraphrase slot, the totals sentence), E.1 (the names / counts / reads vocabulary), E.9 (Haiku 4.5 under the store's own metadata,
the retention denominator, Graphiti), E.10 (the retagging, depth and composite tables; dollar figures out; the pointer phrases), E.11 (spend and
caching), F (the registration record rows). No em dash is written; every number carries its key in a comment.
"""
from __future__ import annotations

import io
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC17 = ROOT / "reviews" / "v17" / "src" / "appendix_v17.tex"
SRC18 = ROOT / "reviews" / "v18" / "src"
OUT = SRC18 / "appendix_v18.tex"


def block(name):
    return io.open(SRC18 / name, encoding="utf-8").read().replace("\r\n", "\n")


def table_part(text, label):
    """The \\begin{table}...\\end{table} block whose \\label is `label`, plus any sentence lines that follow it in the source until a blank line."""
    m = re.search(r"\\begin\{table\}\[H\].*?\\label\{" + re.escape(label) + r"\}.*?\\end\{table\}\n", text, flags=re.S)
    assert m, label
    return m.group(0)


CR_TABLE = r"""
\paragraph{Count readers on this set.}
%% R110: the count readers (reviews/NUMBERS_R110.md AUX-R110-A1-CR, -MODELS, -V2R; reviews/v18/tools/a1_count_readers.py; no model call).
Two readers with no model in them read the count table alone, so that what a tally carries can be measured beside what the models read from it.
The category-aware count reader knows the question's category from the manifest and reads that category's retracted-plus-expired tally; the category-guessing reader assigns the category from the question by the recorded rule of the question-only baseline suite and reads the same tally; a state-aware reader, an upper bound that knows the state as well as the category, reads the state's own cell.
Under the superseded-only summary the category-aware reader separates the retracted versions at $0.7306$ (item interval $[0.6194,0.8228]$, profile $[0.6900,0.8090]$) and the expired versions at $0.7778$ ($[0.6793,0.8625]$, $[0.7153,0.8680]$), the state-aware reader at $0.8944$ and $0.7778$, and the models on the same items at $0.5283$ to $0.6150$ (Table~\ref{tab:cf-cr}).
The tally individuates the version because $26$ of the $30$ retraction pairs and $15$ of the $30$ expiry pairs have a category base count of zero, so the present-negative version's increment reads against zero within its triple.
A reader of the two lifecycle totals, the lines the totals-randomized summary permutes, reads retraction at $0.6347$ and expiry at $0.6922$ under the superseded-only summary and $0.4044$ and $0.3894$ under the recorded permutation, at chance in expectation over $200$ permutation seeds ($0.4900$ and $0.5065$); the per-category tallies are untouched by that permutation, so the category-aware reader is identical under both.

\begin{table}[H]
\caption{The count readers on the counterfactual set beside the models, under the superseded-only summary: AUROC on the whole set and per state, the profile interval of the whole-set AUROC, and each model minus the category-aware reader on the two counted states. The category-aware reader reads the retracted-plus-expired tally at the question's category, the state-aware reader the state's own cell at that category, the totals reader the two lifecycle totals, and the category-guessing reader the tally at the category the question-only suite's rule assigns. The category-aware reader separates the versions on the states the summary only counts; every model is below it on both. Descriptive; computed after the fact on the recorded texts and rows.}
\label{tab:cf-cr}
\centering
\tiny
\setlength{\tabcolsep}{2pt}
\begin{tabular}{@{}lrrrrl@{}}
\toprule
Reader & whole & supersession & retraction & expiry & profile interval (whole) \\
\midrule
Category-aware reader & $0.6043$ & $0.5000$ & $0.7306$ & $0.7778$ & $[0.5753,0.6389]$ \\
State-aware reader (an upper bound) & $0.8580$ & $0.9006$ & $0.8944$ & $0.7778$ & $[0.8150,0.8998]$ \\
Totals reader & $0.5603$ & $0.5028$ & $0.6347$ & $0.6922$ & $[0.5452,0.5882]$ \\
Category-guessing reader & $0.6623$ & $0.6573$ & $0.6669$ & $0.6872$ & $[0.6273,0.6991]$ \\
\addlinespace
\multicolumn{6}{@{}l}{\textit{Model minus the category-aware reader: whole set (difference; item interval; profile interval), and on the counted states (model level; difference)}}\\
GPT-4.1 mini & $+0.1124$ & & $0.5283$; $-0.2022$ & $0.5489$; $-0.2289$ & $[+0.0272,+0.1944]$; $[+0.0400,+0.1756]$ \\
Haiku 4.5 & $+0.1523$ & & $0.5433$; $-0.1872$ & $0.5794$; $-0.1983$ & $[+0.0706,+0.2319]$; $[+0.0843,+0.2168]$ \\
Opus 5 & $+0.2362$ & & $0.5872$; $-0.1433$ & $0.6150$; $-0.1628$ & $[+0.1663,+0.3114]$; $[+0.1745,+0.2938]$ \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{The increment moved within the triple.}
%% R110: ADDENDUM_V2R_CAT (frozen 257a090; r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md AUX-V2RCAT-LOCK, -REF, -LEAK, -MINI, -H45, -BRANCH, -POSTHOC; D-V2RCAT-1).
A second tally check starts from the totals-randomized text and, for each of the $60$ counted-state pairs, moves the obligation's own increment in the category row's retracted or expired column from the present-negative version to one non-present-negative sibling under a recorded seed, so that the version carrying the obligation reads the base count and a sibling reads the increment; every other line is unchanged, every name section equals the superseded-only summary's, the renderer lock holds on all $120$ changed texts, and the leakage screen returns $0$ of $30$.
A reader that follows the moved cell falls below chance on that state, the state-aware reader to $0.3028$ on retraction and $0.3611$ on expiry (Table~\ref{tab:v2rcat}).
The registered reading asked whether a model stays within the $0.05$ band of its superseded-only row on both counted states or moves beyond it with both intervals excluding zero, and fired as neither for both models, so each row prints as it came out.
Read after the fact against the direction a tally reader falls, and labelled so: GPT-4.1 mini moves by $+0.0269$ on retraction and $+0.0611$ on expiry, upward, with both intervals including zero, and Haiku 4.5 by $-0.0072$ and $-0.0453$, so no model followed the tally.

\begin{table}[H]
\caption{The increment moved within the triple: each model under the moved text against its recorded superseded-only row, whole set and per state, with the paired difference and both intervals, beside the reference readers on the same text. Descriptive; no prediction was registered.}
\label{tab:v2rcat}
\centering
\tiny
\setlength{\tabcolsep}{2pt}
\begin{tabular}{@{}llrrl@{}}
\toprule
Reader & row & sup.\ only & increment moved & difference (item; profile) \\
\midrule
GPT-4.1 mini ($k=1$) & whole set & $0.7167$ & $0.7410$ & $+0.0242$ $[-0.0047,+0.0523]$; $[-0.0032,+0.0530]$ \\
GPT-4.1 mini & retraction ($30$ pairs) & $0.5283$ & $0.5553$ & $+0.0269$ $[-0.0491,+0.1080]$; $[-0.0692,+0.1331]$ \\
GPT-4.1 mini & expiry ($30$ pairs) & $0.5489$ & $0.6100$ & $+0.0611$ $[-0.0404,+0.1641]$; $[-0.0217,+0.1417]$ \\
Haiku 4.5 ($k=5$) & whole set & $0.7566$ & $0.7525$ & $-0.0041$ $[-0.0220,+0.0133]$; $[-0.0233,+0.0146]$ \\
Haiku 4.5 & retraction ($30$ pairs) & $0.5433$ & $0.5361$ & $-0.0072$ $[-0.0925,+0.0781]$; $[-0.0981,+0.0795]$ \\
Haiku 4.5 & expiry ($30$ pairs) & $0.5794$ & $0.5342$ & $-0.0453$ $[-0.0958,+0.0014]$; $[-0.0781,-0.0169]$ \\
\addlinespace
State-aware count reader & retraction; expiry & $0.8944$; $0.7778$ & $0.3028$; $0.3611$ & \\
Totals reader & retraction; expiry & $0.6347$; $0.6922$ & $0.4044$; $0.3894$ & \\
Superseded-names lookup & whole set & $0.7663$ & $0.7663$ & the name sections are unchanged \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{Score resolution.}
%% R110: AUX-R110-A3 (reviews/v18/tools/a3_single_draw.py; no model call).
The models scored from five calls carry finer score resolution than the smallest model's single call, and the margin over the lookup does not depend on it.
Opus 5's first draw alone reads $0.8400$ on this set ($53$ distinct values against $264$ after averaging), $+0.0736$ above the superseded-names lookup with intervals $[+0.0298,+0.1223]$ and $[+0.0388,+0.1129]$, and its five draws span $0.0059$; Haiku 4.5's first draw reads $0.7555$ ($17$ values), $-0.0108$ against the lookup with both intervals including zero; GPT-4.1 mini's single draw takes $12$ values.
On the full obligation set the first draws read $0.8156$ (Haiku 4.5), $0.8335$ (Opus 5) and $0.8141$ (GPT-5.6 Luna) against averaged rows of $0.8210$, $0.8327$ and $0.8182$.
"""

BH_PARA = r"""
\paragraph{Haiku 4.5 under the store's own metadata.}
%% R110: ADDENDUM_BELIEVED_H (frozen 257a090; believed_h/NUMBERS_BELIEVED_H.md AUX-BH-LOCK, -LOOKUP-LIFTED, -H45-15, -H45-LIFTED, -RETENTION-15, -RETENTION-LIFTED, -BRANCH, -SPLIT).
A descriptive registration scored Haiku 4.5 at five calls per question on the recorded \believed{} texts under both renderings, the capped ($15.04$ superseded names per item) and the lifted ($32.55$ names, at most $50$), against its recorded blind ($0.4150$) and truthful ($0.8210$) rows on the full obligation set, with the superseded-names lookup on the same lists ($0.5858$ capped, $0.6588$ lifted, profile interval $[0.5777,0.7319]$).
Haiku 4.5 reads $0.7069$ capped ($[0.6657,0.7504]$; $[0.6620,0.7541]$) and $0.7364$ lifted ($[0.6911,0.7858]$; $[0.6665,0.8024]$), $-0.1141$ and $-0.0847$ below its truthful row with both intervals excluding zero, and $+0.1212$ ($[+0.0628,+0.1849]$; $[+0.0317,+0.2107]$) and $+0.0776$ ($[+0.0272,+0.1355]$; $[-0.0031,+0.1498]$) above the lookup.
Its retention, the ratio of the paired resampled differences, is $0.7190$ capped ($[0.6214,0.8497]$; $[0.5935,0.8603]$) and $0.7916$ lifted ($[0.6838,0.9243]$; $[0.6342,0.9425]$), at or above the sixty-percent line under both renderings.
GPT-4.1 mini's retention figures above divide by an indexed-minus-blind difference that Section~\ref{sec:populations} does not report as a gain, because its blind score is one value on $604$ of the $661$ questions, so Table~\ref{tab:levels} reports retention for Haiku 4.5 only.
Split by whether the obligation's own scrubbed name survives in the \believed{} list (Table~\ref{tab:bh-split}), Haiku 4.5 reads the $53$ supersession obligations whose name survives under the lifted rendering at $0.8658$ against $0.8855$ truthful ($-0.0197$, $[-0.0690,+0.0303]$; $[-0.0842,+0.0424]$), and the $10$ whose name is gone at $0.6839$ against $0.9122$ ($-0.2283$, $[-0.4288,-0.0430]$; $[-0.6568,+0.0182]$); under the cap the halves are $24$ and $39$, at $0.7993$ and $0.6933$.

\begin{table}[H]
\caption{Haiku 4.5 under the store's own metadata, the $63$ supersession obligations split by whether the item's own scrubbed name survives in the \believed{} list, each half against the same $557$ negatives: Haiku 4.5 under the \believed{} and the truthful summary, the lookup on the \believed{} list, and the paired differences, each with its item-level and profile-grouped intervals on the rows beneath. Descriptive; no prediction was registered.}
\label{tab:bh-split}
\centering
\tiny
\setlength{\tabcolsep}{1.5pt}
\begin{tabular}{@{}llrrrrll@{}}
\toprule
Rend. & own name & $n$ & Haiku, \believed{} & truthful & lookup & \believed{} minus truthful & Haiku minus lookup \\
\midrule
capped & present & $24$ & $0.7993$ & $0.8925$ & $0.7292$ & $-0.0932$ & $+0.0701$ \\
 & item & & & & & $[-0.1746,-0.0006]$ & $[-0.0204,+0.1663]$ \\
 & profile & & & & & $[-0.2041,+0.0235]$ & $[-0.0261,+0.1709]$ \\
capped & absent & $39$ & $0.6933$ & $0.8880$ & $0.6146$ & $-0.1947$ & $+0.0787$ \\
 & item & & & & & $[-0.2673,-0.1224]$ & $[-0.0137,+0.1666]$ \\
 & profile & & & & & $[-0.2813,-0.1011]$ & $[-0.0497,+0.2355]$ \\
lifted & present & $53$ & $0.8658$ & $0.8855$ & $0.7593$ & $-0.0197$ & $+0.1065$ \\
 & item & & & & & $[-0.0690,+0.0303]$ & $[+0.0411,+0.1785]$ \\
 & profile & & & & & $[-0.0842,+0.0424]$ & $[+0.0233,+0.1846]$ \\
lifted & absent & $10$ & $0.6839$ & $0.9122$ & $0.7969$ & $-0.2283$ & $-0.1130$ \\
 & item & & & & $[0.6722,0.8992]$ & $[-0.4288,-0.0430]$ & $[-0.3613,+0.1503]$ \\
 & profile & & & & & $[-0.6568,+0.0182]$ & $[-0.5208,+0.4381]$ \\
\bottomrule
\end{tabular}
\end{table}
"""

E11 = r"""\subsection{Spend and caching}\label{app:economics}

Monitoring runs before every query, so its cost turns on prompt caching.
The projection and the billed micro-run are in the supplement (Section~S.8).
%% R110: A5_EDITS.md item 6; one line per run from its ledger key (AUX-RESP-SPEND, AUX-DS-SPEND, AUX-RESP-A1-SPEND, AUX-DS-A1-SPEND to -A7-SPEND, AUX-CF2-SPEND, AUX-CF3-SPEND, AUX-PAD-SPEND, AUX-PARA-DRAFT, AUX-BH-SPEND, AUX-V2RCAT-SPEND).
Every model run in this paper was capped before its first call and metered from its rows at list or batch prices; the amounts, in dollars, are: the mechanism tests $0.94$ and the downstream experiment $0.11$; Haiku 4.5 on the retrieved-view monitors $6.72$ of a $12$ cap; the downstream answer-stage registrations $0.46$, $0.41$, $0.56$, $0.54$ (of $8$), $0.10$ (of $2$), $3.63$ (of $6$) and $0$; the counterfactual set $1.08$ of $22$ (OpenAI) and $72.50$ of $130$ (Anthropic); its expiry extension $2.21$ of $5$; the list-length check and its amendment $7.89$ of $28$; the paraphrase drafting lane $0.12$ over $413$ calls; Haiku 4.5 under the store's own metadata $9.36$ of $12$; the increment moved within the triple $3.23$ of $4$.
"""

REG_ROWS = r"""Haiku 4.5 under the store's own metadata & \texttt{77de1e37} & 2026-09-14 & Haiku 4.5 at five calls on the recorded \believed{} texts under the capped and the lifted rendering; retention against its recorded blind and truthful rows; the lookup on the same lists; three branches enumerated (Table~\ref{tab:bh-split}) & no prediction; at or above the sixty-percent line under both \\
The increment moved within the triple & \texttt{de2dd0ba} & 2026-09-14 & for each counted-state pair, the obligation's own per-category increment moved from the present-negative version to a sibling under a recorded seed; GPT-4.1 mini and Haiku 4.5 against their recorded superseded-only rows; the state-cell and totals readers; the band reading (Table~\ref{tab:v2rcat}) & no prediction; the band reading fired as neither \\
DS Amendment 5: the store's untagged duplicates tagged & \texttt{a820195f} & 2026-09-14 & every active line asserting the stale value on the $35$ obligations the audit found retagged with the obligation's state; the $74$ changed views re-answered under the Amendment 4 header by both answerers; the same detector (Table~\ref{tab:ds-a5}) & no prediction \\
DS Amendment 6: coverage-gated depth of the retrieval view & \texttt{52effd8d} & 2026-09-15 & views of five to ten lines from the recorded ten-deep ranking and a gated view that expands to ten where the recorded coverage score is at or above its threshold; both answerers under the header; the budget-matched comparison at the gated view's mean depth (Table~\ref{tab:ds-a6}) & no prediction \\
DS Amendment 7: an obligation-reported detector and a composite & \texttt{6566bf09} & 2026-09-15 & a closed word list scored on every recorded answer under every policy; a composite per policy over the full obligation set; the detector's agreement with the second annotator's fourth question (Table~\ref{tab:ds-a7}) & no prediction; no model call \\
"""


def moved_block(name):
    """A %%BLOCK <name> ... %%END block of src/moved_tables_v18.tex (the tables the author's trim order moved out of the body)."""
    t = block("moved_tables_v18.tex")
    m = re.search(r"%%BLOCK " + name + r"\n(.*?)\n%%END", t, flags=re.S)
    assert m, name
    return "\n" + m.group(1) + "\n"


def main():
    RUNS_TABLE, ROUTES_FULL, DS_LOWER, POPULATIONS = moved_block("RUNS"), moved_block("ROUTES_FULL"), moved_block("DS_LOWER"), moved_block("POPULATIONS")
    s = io.open(SRC17, encoding="utf-8").read().replace("\r\n", "\n")
    a5 = block("amend5_e10.tex"); a6 = block("amend6_e10.tex"); a7 = block("amend7_e10.tex")
    a5_table = table_part(a5, "tab:ds-a5")
    a5_sent = a5.split("% ---- Appendix E.10, the sentence under the table (the changed views alone; AUX-DS-A5-CHANGED-*)\n", 1)[1].strip() + "\n"
    a6_table = table_part(a6, "tab:ds-a6"); a7_table = table_part(a7, "tab:ds-a7")
    a7_sent = a7.split("% ---- Appendix E.10, the sentences under the table (AUX-DS-A7-COMPOSITE-ANSWERED-DIFF; AUX-DS-A7-COMPOSITE-DIFF; AUX-DS-A7-REPORTED)\n", 1)[1].strip() + "\n"

    edits = [
        # ---- C.2
        ("so the boundary the first summary draws is the summary's.", "so the difference belongs to what the summary names."),
        ("every interval inside the tolerance band, so no reader takes anything from the counts.\n",
         "every interval inside the tolerance band, so no model takes anything from the totals.\n" + CR_TABLE),
        ("The two texts written before scoring that Section~\\ref{sec:counterfactual} points to read as follows.",
         "The registered texts for this set (Appendix~\\ref{app:registration}) read as follows."),
        ("drafted by the smallest model under a deterministic screen; the author's label-transfer read is in progress, and its table lands here when the run completes.",
         "drafted by the smallest model under a deterministic screen; the author's label-transfer read had not been made at this build, so no paraphrase row is printed."),
        # the A4 rows in tab:pad (reading (i), the registered order; AUX-R110-A4) and the caption note
        ("Superseded-names lookup & $60$ names & $0.6696$ & $-0.0788$ & $[-0.1541,-0.0096]$ & $[-0.1794,+0.0284]$ \\\\\n",
         "Superseded-names lookup & $60$ names & $0.6696$ & $-0.0788$ & $[-0.1541,-0.0096]$ & $[-0.1794,+0.0284]$ \\\\\n"
         "%% R110: the lookup at 100 and 200 names under the registered draw order (reviews/NUMBERS_R110.md AUX-R110-A4; reviews/v18/results/a4_table16_rows.tex).\n"
         "Superseded-names lookup & $100$ names & $0.6558$ & $-0.0926$ & $[-0.1718,-0.0221]$ & $[-0.1953,+0.0199]$ \\\\\n"
         "Superseded-names lookup & $200$ names & $0.5960$ & $-0.1525$ & $[-0.2357,-0.0773]$ & $[-0.2595,-0.0399]$ \\\\\n"),
        ("Lexical lookup & $60$ names & $0.5825$ & $+0.0087$ & $[-0.0434,+0.0592]$ & $[-0.0662,+0.0865]$ \\\\\n",
         "Lexical lookup & $60$ names & $0.5825$ & $+0.0087$ & $[-0.0434,+0.0592]$ & $[-0.0662,+0.0865]$ \\\\\n"
         "Lexical lookup & $100$ names & $0.5601$ & -- & $[0.5001,0.6162]$ & -- \\\\\n"
         "Lexical lookup & $200$ names & $0.5383$ & -- & $[0.4737,0.6006]$ & -- \\\\\n"),
        # ---- E.9
        ("(persona-clustered $[+0.0217,+0.1744]$, the interval Table~\\ref{tab:believed} carries)", "(persona-clustered $[+0.0217,+0.1744]$)"),
        ("The three texts written before scoring that Section~\\ref{sec:backends} points to read as follows.",
         "The three registered texts for this row (Appendix~\\ref{app:registration}) read as follows."),
        ("NOK degrades materially under believed metadata but remains positive.\n",
         "NOK degrades materially under believed metadata but remains positive.\n" + BH_PARA),
        ("so those modifications are near-inert on this corpus.\n",
         "so those modifications are near-inert on this corpus.\nIts tag route at trial scale is left for the discussion period.\n"),
        # ---- E.10: dollar figures out (A5_EDITS.md item 6), the pointer phrases (item 8)
        ("The runs billed $\\$0.9415$ and the downstream experiment $\\$0.1093$.\n", ""),
        ("under a cap of \\$12 in that order; hybrid ran, retrieved ran, the own-name ablation ran, and the lanes billed \\$6.72.",
         "in that order; hybrid ran, retrieved ran, the own-name ablation ran (Appendix~\\ref{app:economics})."),
        ("at the gold threshold, and the runs billed $\\$0.4579$.", "at the gold threshold."),
        ("with the untagged records again the worse half; the two runs billed $\\$0.4141$.", "with the untagged records again the worse half."),
        ("(the lower rows of Tables~\\ref{tab:ds} and~\\ref{tab:ds-h45}); the two lanes billed $\\$0.5576$.", "(the lower rows of Tables~\\ref{tab:ds} and~\\ref{tab:ds-h45})."),
        ("(\\texttt{AUX-DS-A4-*}); the two lanes billed $\\$0.5441$ against the $\\$8.00$ cap.", "(\\texttt{AUX-DS-A4-*})."),
        ("Both readings were fixed before scoring, the whole-population comparison", "Both readings were registered, the whole-population comparison"),
        ("The texts written before scoring that Sections~\\ref{sec:populations} and~\\ref{sec:backends} point to read as follows.",
         "The registered texts for these rows (Appendix~\\ref{app:registration}) read as follows."),
        ("The text written before scoring (supplement, Section~S.3) reports the same interval at four decimals.",
         "The registered text (supplement, Section~S.3) reports the same interval at four decimals."),
        ("The two bars fixed before scoring were a reach gain", "The two registered bars were a reach gain"),
        ("\\paragraph{The paragraph written before scoring.} The paragraph that Section~\\ref{sec:populations} points to reads, with its numbers, as follows.",
         "\\paragraph{The registered paragraph.} The paragraph that Section~\\ref{sec:populations} points to reads, with its numbers, as follows."),
        ("\\paragraph{Texts written before scoring.} The eleven prediction texts of the mechanism tests and the downstream experiment, written before any call and filled with their numbers, are in the supplement (Section~S.3), and the outcome sentence written before scoring for the neutral-slice prediction is in its Section~S.9.",
         "\\paragraph{Registered texts.} The eleven prediction texts of the mechanism tests and the downstream experiment, written before any call and filled with their numbers, are in the supplement (Section~S.3), and the registered outcome sentence for the neutral-slice prediction is in its Section~S.9."),
        # the retagging, depth and composite tables after the Haiku answerer table
        ("Lookup, literal threshold & $94$ & $7$ & $16$ of $75$ / $12$ of $19$ & $174$ & $47$ ($0.2701$) \\\\\n\\bottomrule\\end{tabular}\\end{table}\n",
         "Lookup, literal threshold & $94$ & $7$ & $16$ of $75$ / $12$ of $19$ & $174$ & $47$ ($0.2701$) \\\\\n\\bottomrule\\end{tabular}\\end{table}\n\n"
         "%% R110: the store's untagged duplicates tagged (DS Amendment 5; reviews/v18/src/amend5_e10.tex; AUX-DS-A5-*).\n" + a5_table + a5_sent +
         "\n%% R110: the depth of the retrieval view (DS Amendment 6; reviews/v18/src/amend6_e10.tex; AUX-DS-A6-*; D-DS-A6-1).\n" + a6_table +
         "\n%% R110: the obligation-reported detector and the composite (DS Amendment 7; reviews/v18/src/amend7_e10.tex; AUX-DS-A7-*; D-DS-A7-1).\n" + a7_table + a7_sent + DS_LOWER),
        # the full routes table into E.10 after the own-marks paragraph (the author's trim order of 2026-09-15)
        ("Its one-sample discrimination is $0.4888$ with interval $[0.4646,0.5165]$, so the constant was not the gate.\n",
         "Its one-sample discrimination is $0.4888$ with interval $[0.4646,0.5165]$, so the constant was not the gate.\n" + ROUTES_FULL),
        # the run-coverage table into Appendix A after its first paragraph
        ("This appendix carries the cross-model set in full.\n",
         "This appendix carries the cross-model set in full; Table~\\ref{tab:populations} defines every population the body names, and Table~\\ref{tab:runs} records which model ran on which question set.\n" + POPULATIONS + RUNS_TABLE),
        # ---- E.11
        ("\\subsection{Caching economics}\\label{app:economics}\n\nMonitoring runs before every query, so its cost turns on prompt caching; the projection and the billed micro-run are in the supplement (Section~S.8).\n", E11),
        # ---- F: the registration record rows (tab:registrations-c) and its caption; the Opus paragraph's hash (A5_EDITS.md item 7)
        ("\\caption{The registration record, continued: seven descriptive registrations, each frozen by sha256 before its first call and carrying no prediction and no bar, so nothing in them could hold or fail. The padding check, the expiry extension and the two later downstream amendments have run (Tables~\\ref{tab:pad}, \\ref{tab:cf3-expiry} and~\\ref{tab:ds}); the paraphrase check waits on the author's read.}",
         "\\caption{The registration record, continued: twelve descriptive registrations, each frozen by sha256 before its first call and carrying no prediction and no bar, so nothing in them could hold or fail. Every one has run except the paraphrase check, which waits on the author's read.}"),
        ("stale and correct beside the recorded rows (Tables~\\ref{tab:ds} and~\\ref{tab:ds-h45}) & no prediction \\\\\n\\bottomrule",
         "stale and correct beside the recorded rows (Tables~\\ref{tab:ds} and~\\ref{tab:ds-h45}) & no prediction \\\\\n" + REG_ROWS + "\\bottomrule"),
        ("because the answer bounds what any reader can take from this summary.", "because the answer says what a reader can take from this summary and what it cannot."),
        # the author's Pass 2 rule of 2026-09-15 for the appendix: every subsection opens with a plain sentence carrying no numeral
        ("The pilot preceded the main study with a different prompt, so its values support the design lesson and cannot be compared numerically with the main study; its estimands and their table are in the supplement (Section~S.7).",
         "The pilot preceded the main study with a different prompt, so its values support the design lesson and cannot be compared numerically with the main study.\nIts estimands and their table are in the supplement (Section~S.7)."),
        ("FOK AUROC treats non-\\absent{} coverage as positive, while NOK AUROC treats \\pn{} as positive; items are nested within the $40$ personas.",
         "FOK AUROC treats non-\\absent{} coverage as positive, while NOK AUROC treats \\pn{} as positive.\nItems are nested within the $40$ personas."),
        ("The registrations number the non-model readers of the summary NB-1 to NB-6, and the main text calls NB-6 the superseded-names lookup.",
         "The non-model readers of the summary carry numbered names in the registrations, and the main text calls the sixth the superseded-names lookup.\nThe registrations number them NB-1 to NB-6."),
        ("The elicited score is rescaled by three monotone maps \\citep{platt2000,zadrozny2002,guo2017} under leave-one-persona-out cross-validation on the pooled hard-tier coverage set of $588$ questions.",
         "The elicited score is rescaled by three monotone maps \\citep{platt2000,zadrozny2002,guo2017} under leave-one-persona-out cross-validation on the pooled hard-tier coverage set.\nThat set holds $588$ questions."),
        ("Opus 5 entered the study at the cross-vendor preregistration (\\texttt{776bce07b3}, 2026-08-14), carrying three of its predictions.",
         "Opus 5 entered the study at the cross-vendor preregistration (the R74 addendum, Table~\\ref{tab:registrations}; 2026-08-14), carrying three of its predictions."),
    ]
    for old, new in edits:
        n = s.count(old)
        assert n == 1, (old[:90], n)
        s = s.replace(old, new)
    # the names / counts / reads vocabulary enters the glossary (rule G3; READER_CLAIM.md section 2)
    old = "%%V11:1309-1326%%\n"
    assert s.count(old) == 1
    s = s.replace(old, old + "\n%% R110: Definition 3 of v17 returns to vocabulary here (rule G3; READER_CLAIM.md section 2).\n\\noindent A summary \\emph{names} a state when it lists the attribute names in that state and \\emph{counts} it when it gives only a tally of it; a reader \\emph{reads} a state when its score separates that state's items from the rest.\n")
    # every mention of the totals-randomized summary says "totals" (the v17 W wording rule; AUX-CF2-V2R-DEF): the row labels of tab:cf-fok and tab:cf3-expiry
    assert s.count("& counts rand. &") == 6, s.count("& counts rand. &")
    s = s.replace("& counts rand. &", "& totals rand. &")
    assert "\u2014" not in s, "em dash"
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(s)
    print(f"-> {OUT} ({len(s.splitlines())} lines); edits {len(edits) + 1}")


if __name__ == "__main__":
    main()
