# -*- coding: utf-8 -*-
"""port_r131.py -- program R131 (2026-09-20; the author's brief 'KtS R131: land R125 in the body (main session only)'): the body landings, applied to
reviews/v22/src/body_v22.tex and abstract_v22.tex after port_v22.py (regeneration order: cp v21 -> appendix_r126.py -> appendix_r128.py ->
appendix_r129.py -> appendix_r131.py -> fig3_data.py -> fig3_data_r131.py -> port_v22.py -> port_r131.py [--payers=1,2,3,4]). Every edit is an
asserted replacement (rep); the author's texts are verbatim with the LaTeX conversions of port_v22.py (numerals in math mode, \\pn{} / \\present{},
Appendix pointers as \\ref), and every gate-driven wording change is named with its rule in GATE_CHANGES and printed at the end (the report and
CLAIMS.md list old beside new). Sections of the brief: A Section 4's metric paragraph; B Section 5.1 (retitled 'Names and counts'); C Section 5.2;
D Table 1 and Figure 3 (the matched data file; y axis to 0.35; the pooled figure moves to C.2); E the abstract, Section 1, the Conclusion, the
evidence table; F Section 6; G Limitations; H the payers, only as needed, in the brief's order. Nothing from R130 lands here.
Usage: python reviews/v22/tools/port_r131.py [--payers=1,2,3,4] [--check]
"""
from __future__ import annotations

import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT_B = ROOT / "reviews" / "v22" / "src" / "body_v22.tex"
OUT_A = ROOT / "reviews" / "v22" / "src" / "abstract_v22.tex"

GATE_CHANGES = []  # (rule, section, before, after)


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def rep(t, old, new, n=1, where=""):
    assert t.count(old) == n, (where, t.count(old), n, old[:120])
    return t.replace(old, new)


def gate(rule, section, t, old, new):
    GATE_CHANGES.append((rule, section, old, new))
    return rep(t, old, new, 1, rule + " " + section)


AP = "(Appendix~\\ref{app:counterfactual})"

# ----------------------------------------------------------------------------------------------------------------------- A. Section 4, the metric paragraph
S4_OLD = ("We score separation by AUROC, the chance that a positive scores above a negative \\citep{hanley1982}. Chance is $0.50$. A difference is \\emph{reliable} when both the item-level paired and persona-grouped bootstrap intervals exclude zero; when they disagree, the wider governs. "
          "\\emph{Within tolerance} means an absolute difference no greater than $0.05$. A gain compares the same questions with and without the summary. The counterfactual table prints persona intervals, which keep triples intact.\n")
S4_NEW = ("%% R131 A (2026-09-20): the author's metric paragraph (the matched AUROC defined; the persona-interval sentence moves to Table 1's caption).\n"
          "We score separation by AUROC, the chance that a positive ranks above a negative \\citep{hanley1982}; chance is $0.50$. The registered metric pools all items. "
          "Because the counterfactual set fixes the question, we also report the matched AUROC: the share of triples in which the \\pn{} version outscores the \\present{} version, ties counting half. "
          "It is post hoc, and we say where the two metrics disagree. A difference is \\emph{reliable} when both the item-level paired and persona-grouped bootstrap intervals exclude zero. "
          "\\emph{Within tolerance} means an absolute difference no greater than $0.05$. A gain compares the same questions with and without the summary.\n")

# ----------------------------------------------------------------------------------------------------------------------- B. Section 5.1
S51_NEW = ("\\subsection{Names and counts}\\label{sec:names_counts}\n"
           "%% R131 B (2026-09-20): Section 5.1 in the author's words, whole (R125 Task 1's matched metric, AUX-CF2-R125-*; Task 5's E2 Amendment 1, AUX-CF2-R125-NC-*; reviews/NUMBERS_R131.md).\n"
           "\\claim{Within a triple, a name or a count can identify the obligation.}\n"
           "On the counterfactual set the \\pn{} version differs from its siblings in one attribute, so its category always holds one more non-active record.\n"
           "A count reader handed the question's category wins every retraction and expiry triple (a privileged reader: the models must infer the category), and the name lookup wins $82$ of the $88$ supersession triples and loses none.\n"
           "For $26$ of $30$ retraction pairs and $15$ of $30$ expiry pairs that count starts at zero, so a reader can identify the store version without identifying the attribute.\n"
           "What differs across readers is which of the two they use. " + AP + "\n\n"
           "\\claim{The two smaller models read only the names.}\n"
           "Removing every count leaves mini and Haiku within $0.01$ of their intact-summary scores on either metric (mini on its single-call row).\n"
           "Counts alone score reliably below names alone, by $0.14$ for each model on the matched metric ($0.12$ and $0.16$ pooled), and the whole loss falls on supersession, where the names are.\n"
           "On retraction and expiry both models stay reliably below a count reader that only guesses the question's category ($0.77$ and $0.75$). " + AP + "\n\n"
           "\\claim{Removing the target name leaves mini near chance.}\n"
           "On supersession questions in the full obligation set, removing the target name and its nearest neighbours lowers mini from $0.86$ to $0.53$ and Haiku from $0.89$ to $0.68$, both reliably. (Appendix~\\ref{app:resp})\n\n"
           "\\claim{The three stronger models also read the counts.}\n"
           "On retraction and expiry, which the default summary only counts, Luna, Sol and Opus score $0.58$ to $0.87$ on the matched metric, and none is reliably below the guessing count reader.\n"
           "When the obligation's increment is moved to a sibling version with the names unchanged, all three follow it: across the two counted states Opus falls by $0.28$ and Sol by $0.33$, and Luna falls by $0.32$ on retraction and $0.27$ on expiry, each reliable; mini and Haiku show no reliable change.\n"
           "On the pooled metric the expiry falls are reliable for all three and the retraction falls for Opus alone.\n"
           "Removing every count costs Luna a reliable $0.06$ and Opus $0.04$ on the pooled metric, though counts alone still score reliably below names alone for both; Sol was not run. " + AP + "\n\n")

# ----------------------------------------------------------------------------------------------------------------------- D. Table 1 (the inbox's layout; the matched column; the hybrid row; both metrics in the difference row)
TAB1 = r"""\begin{table}[t]
%% R126 (2026-09-19): Table 1 in the inbox's layout (rows by reader, a named-states column, the Opus-minus-lookup difference row), our style; the
%% values are v21's tab:cf-main rows (AUX-R122-K5-* for GPT-4.1 mini at five draws; AUX-CF2-*-V2/-V3; AUX-CF2-OAI-SOL-V2, -LUNA-V2; AUX-WP-B-PNPRESENT,
%% -B-ORDERING; AUX-R110-A1-CR) and the difference row is AUX-R103-MARGIN (+0.0323, [+0.0060,+0.0617]; [+0.0077,+0.0608]).
%% R131 D (2026-09-20): the 'PN vs PRESENT' column becomes 'matched', (W + T/2) / 148 from the printed W/T/L (AUX-CF2-R125-MATCHED-V2, -V3; reviews/NUMBERS_R131.md
%% AUX-R131-TAB1); the hybrid reader's row (AUX-CF2-HYB-WHOLE 0.7865 [0.7488, 0.8234]; AUX-CF2-R125-MATCHED-V2 HYBRID_v2 0.8851, 114/34/0); the difference row prints
%% both metrics at four decimals (AUX-R103-MARGIN; AUX-CF2-R125-OP5-V3 +0.0304 [-0.0068,+0.0643]; [-0.0038,+0.0648], not reliable).
\caption{Counterfactual obligation AUROC: $88$ supersession, $30$ retraction and $30$ expiry positives. Brackets: persona intervals. The matched column is the within-triple comparison of \pn{} against \present{}, $(W+T/2)/148$; it and W/T/L are post hoc; persona intervals keep triples intact. Question-only AUROC is $0.50$. (Appendix~\ref{app:counterfactual})}
\label{tab:cf-main}
\centering
\scriptsize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}llrlrl@{}}
\toprule
Reader & Named states & AUROC & persona interval & matched & W/T/L \\
\midrule
mini$^{a}$ & superseded & $0.76$ & $[0.72,0.80]$ & $0.73$ & $100/15/33$ \\
mini$^{a}$ & all & $0.83$ & $[0.79,0.87]$ & $0.90$ & $130/5/13$ \\
Haiku & superseded & $0.76$ & $[0.71,0.80]$ & $0.78$ & $89/52/7$ \\
Haiku & all & $0.88$ & $[0.84,0.91]$ & $0.91$ & $125/18/5$ \\
Luna & superseded & $0.84$ & $[0.80,0.88]$ & $0.88$ & $129/2/17$ \\
Sol & superseded & $0.85$ & $[0.81,0.88]$ & $0.86$ & $126/2/20$ \\
Opus & superseded & $0.84$ & $[0.80,0.88]$ & $0.88$ & $128/3/17$ \\
Opus & all & $0.91$ & $[0.88,0.94]$ & $0.94$ & $139/0/9$ \\
\midrule
\multicolumn{6}{@{}l}{\textit{Readers with no generative-model call}}\\
Name lookup & superseded & $0.77$ & $[0.72,0.81]$ & $0.78$ & $82/66/0$ \\
Name lookup & all & $0.88$ & $[0.84,0.91]$ & $0.91$ & $121/27/0$ \\
Count reader, guessed category & superseded & $0.66$ & $[0.63,0.70]$ & $0.72$ & $65/83/0$ \\
Count reader, given category & superseded & $0.60$ & $[0.58,0.64]$ & $0.70$ & $60/88/0$ \\
Lookup with one count feature$^{b}$ & superseded & $0.79$ & $[0.75,0.82]$ & $0.89$ & $114/34/0$ \\
\bottomrule
\end{tabular}
\par\vspace{2pt}
\begin{tabular}{@{}llrll@{}}
\toprule
All states named: Opus minus name lookup & metric & difference & item interval & persona interval \\
\midrule
 & pooled & $+0.0323$ & $[+0.0060,+0.0617]$ & $[+0.0077,+0.0608]$ \\
 & matched & $+0.0304$ & $[-0.0068,+0.0643]$ & $[-0.0038,+0.0648]$ \\
\bottomrule
\end{tabular}
\par\smallskip
\begin{minipage}{0.97\linewidth}\scriptsize
$^{a}$Mini uses the provider's default temperature here. Its earlier one-draw rows at temperature $0$ score $0.72$ and $0.80$; both draw count and temperature change (Table~\ref{tab:mini-k5}). The difference row's pooled comparison is from Table~\ref{tab:counterfactual}, its matched comparison from Table~\ref{tab:cf-matched}. $^{b}$A logistic reader over the name lookup's similarity and the guessed category's non-active share, fit with personas left out (Table~\ref{tab:cf-hybrid}).
\end{minipage}
\end{table}
"""

# ----------------------------------------------------------------------------------------------------------------------- C. Section 5.2
S52_NEW = ("\\subsection{The lookup against the models}\\label{sec:lookup}\n"
           "%% R131 C (2026-09-20): Section 5.2 in the author's words, whole but for the last paragraph (R125 Task 1 AUX-CF2-R125-*; Task 2 AUX-CF2-R125-T2-*; Task 4 AUX-CF2-R125-SB-*; the hybrid reader AUX-CF2-HYB-*; reviews/NUMBERS_R131.md).\n"
           "\\claim{On the named state, no model reliably beats the lookup.}\n"
           "The default summary names only supersession.\n"
           "On its $88$ triples the lookup scores $0.97$ on the matched metric; Opus is $0.01$ above it, Luna and Sol $0.01$ below, and mini reliably below by $0.07$.\n"
           "A sibling-name control removes list length and counts from the comparison: a fourth store version lists a different attribute of the same category, with the same counts and the same number of names.\n"
           "The lookup and every model separate the \\pn{} version from it at $0.88$ to $0.97$, none reliably above the lookup, while a list of meaningless tokens and the count reader fall to $0.47$ and $0.50$. " + AP + "\n\n"
           "\\claim{The stronger models' lead comes from counts, and a count feature closes it.}\n"
           "Across all $148$ triples the lookup and Haiku score $0.78$ and mini $0.73$; Luna, Sol and Opus score $0.86$ to $0.88$, a reliable $0.08$ to $0.10$ above the lookup ($0.07$ to $0.08$ pooled), all of it from retraction and expiry, where the lookup ties every triple.\n"
           "A logistic reader over the lookup's similarity and the guessed category's non-active share, fit with personas left out, scores $0.89$: reliably above the lookup and level with the three models.\n"
           "On the pooled metric the same reader scores $0.79$ and the three stay a reliable $0.05$ to $0.06$ above it; their remaining edge is in pairs that cross questions and states, where their scores stay comparable and the fitted reader's do not. " + AP + "\n\n"
           "\\claim{Naming all states lifts every reader.}\n"
           "With the retracted and expired attributes listed too, the lookup scores $0.91$, Haiku gains a reliable $0.35$ on the two states that were only counted, and Opus reaches $0.94$.\n"
           "Opus's $0.03$ lead over that lookup is reliable on the pooled metric and not on the matched one, so with every state named no model is reliably ahead on both.\n"
           "Luna and Sol did not run this summary. " + AP + "\n\n"
           "\\claim{List length and coverage inflate both metrics.}\n"
           "A reader that only knows whether the store covers the question scores $0.75$ pooled and $0.50$ matched.\n"
           "A lookup over meaningless tokens scores $0.60$ pooled and $0.65$ matched, because the \\pn{} version's list is one name longer and $24$ of the $88$ \\present{} lists are empty; the name lookup is a reliable $0.13$ above it on the matched metric.\n"
           "The sibling-name control is the comparison that removes both. " + AP + "\n\n")

# ----------------------------------------------------------------------------------------------------------------------- D. Figure 3 on the matched metric
FIG3_OLD_HEAD = ("%% R126 (2026-09-19), Phase 3: Figure 3 redrawn in pgfplots from reviews/v22/src/fig3_data.tex (written by reviews/v22/tools/fig3_data.py from the\n"
                 "%% recorded artifacts; the marker spliced by build_v22.py), not from the inbox figure: two panels, states on the x axis, markers only, readers dodged\n"
                 "%% within each state, one marker shape per reader, one legend column at the right, the chance line dashed. Provisional: redrawn on the matched\n"
                 "%% metric when R125 reports, by regenerating the data file. GPT-4.1 mini is its five-draw per-state rows (AUX-R122-K5-ROWS).\n"
                 "%%FIG3-DATA%%\n")
FIG3_NEW_HEAD = ("%% R126 (2026-09-19), Phase 3: Figure 3 redrawn in pgfplots: two panels, states on the x axis, markers only, readers dodged within each state, one\n"
                 "%% marker shape per reader, one legend column at the right, the chance line dashed. R131 D (2026-09-20): drawn on the matched metric from\n"
                 "%% reviews/v22/src/fig3_data_matched.tex (fig3_data_r131.py, checked against reviews/r125/results/r125_matched.json; AUX-CF2-R125-FIG3), spliced by\n"
                 "%% build_v22.py; the y axis reaches 0.35 (mini's expiry value is 0.40); the pooled version of the figure is in Appendix C.2 (fig:perstate-pooled).\n"
                 "%%FIG3-DATA-MATCHED%%\n")
FIG3_AXIS_OLD = "    width=0.41\\linewidth, height=5.0cm, xmin=-0.5, xmax=2.5, ymin=0.45, ymax=1.0,\n    xtick={0,1,2}, xticklabels={Supersession,Retraction,Expiry}, ytick={0.5,0.6,0.7,0.8,0.9,1.0},\n    ylabel={obligation AUROC},"
FIG3_AXIS_NEW = "    width=0.41\\linewidth, height=5.0cm, xmin=-0.5, xmax=2.5, ymin=0.35, ymax=1.0,\n    xtick={0,1,2}, xticklabels={Supersession,Retraction,Expiry}, ytick={0.4,0.5,0.6,0.7,0.8,0.9,1.0},\n    ylabel={matched AUROC},"
FIG3_CAP_OLD = "\\caption{Per-state obligation AUROC on the counterfactual set under the summary naming supersession only (left) and the summary naming all states (right); the dashed line is chance. Mini uses five draws, matching Table~\\ref{tab:cf-main}. The count reader guesses the category. Luna and Sol ran only the default summary. Every value is in the tables of Appendix~\\ref{app:counterfactual}.}"
FIG3_CAP_NEW = "\\caption{Per-state matched AUROC on the counterfactual set (\\pn{} against \\present{} within the triple; post hoc); the dashed line is chance. Mini uses five draws, matching Table~\\ref{tab:cf-main}. The count reader guesses the category. Luna and Sol ran only the default summary. Every value is in the tables of Appendix~\\ref{app:counterfactual}.}"

# ----------------------------------------------------------------------------------------------------------------------- E. the abstract, Section 1, the Conclusion, the evidence table
ABS_OLD = ("We test that judgment before retrieval on $148$ questions, each asked of three store versions through summaries with values removed.\n"
           "First, names carry the signal: removing counts leaves GPT-4.1 mini and Haiku 4.5 within $0.01$, whereas counts alone cost mini $0.12$ and Haiku $0.16$ against names alone.\n"
           "Second, no model reliably beats a name lookup on the state named by the default summary.\n"
           "%% R128 A1 (2026-09-20): the margin is on the counterfactual set (AUX-CF2-OAI-P-S1/-S2, AUX-R103-MARGIN); on the 661 no margin survives the persona interval.\n"
           "GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 lead it by $0.07$ to $0.08$ on the counterfactual set; Opus leads by $0.03$ when all states are named.\n"
           "%% R126 (2026-09-19), Phase 2.2: the author's third finding (AUX-E1R-BELIEVED-NOK 0.5959, AUX-E1R-NB6 0.5858, the capped store-written rows of Table tab:levels).\n"
           "Third, the backends we tested omit or misstate this information: under FR-Bank's own metadata, mini and the lookup fall to $0.60$ and $0.59$.\n")
ABS_NEW = ("%% R131 E (2026-09-20): the author's second sentence and three findings (AUX-CF2-R125-SB-*, AUX-CF2-R125-VS-LOOKUP, AUX-CF2-R125-CONTRASTS; the third finding's numbers as before: AUX-E1R-BELIEVED-NOK 0.5959, AUX-E1R-NB6 0.5858).\n"
           "We test that judgment before retrieval on $148$ questions, each asked of three versions of one store, through summaries that list counts and attribute names with values removed.\n"
           "First, GPT-4.1 mini and Haiku 4.5 read only the names; GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 also read the counts and follow one when it is moved.\n"
           "Second, on the state a summary names, no model reliably beats a cosine lookup over the names: with counts and list length held fixed, the lookup and every model separate the right name from a sibling at $0.88$ or higher, while meaningless tokens and counts fall to chance.\n"
           "The three stronger models lead the lookup by $0.08$ to $0.10$ within matched triples, and a lookup given one count feature closes that lead.\n"
           "Third, the backends we tested omit or misstate this information: under FR-Bank's own metadata, GPT-4.1 mini and the lookup fall to $0.60$ and $0.59$.\n")

S1_OLD = ("In these tests, what the store writes down mattered more than which reader read it.\n"
          "Attribute names carry most of the observed signal.\n"
          "%% R126 addendum B1 (2026-09-20): the author's two sentences (the inbox's tripped rule D against the abstract at 88 and 83 percent).\n"
          "On the one state the default summary names, no model reliably outscores the lookup.\n"
          "%% R128 A1 (2026-09-20): 'on the counterfactual set' for 'on the whole set'.\n"
          "Luna, Sol and Opus pull ahead of it on the counterfactual set, and Opus stays ahead by $0.03$ when every state is named.\n"
          "Models differ further when the rubric states the intent rule.\n"
          "Backend errors weaken the information supplied to every reader, while the retrieval fetch supplies much of the added reach.\n")
S1_NEW = ("%% R131 E (2026-09-20): the author's findings paragraph.\n"
          "In these tests, what the store writes down mattered more than which reader read it.\n"
          "The two smaller models read only the attribute names; Luna, Sol and Opus also read the counts.\n"
          "On the one state the default summary names, no model reliably outscores the lookup, with list length held fixed or not.\n"
          "The three stronger models pull ahead of it through the counted states, and a lookup given one count feature catches them within matched triples.\n"
          "Models differ further when the rubric states the intent rule.\n"
          "Backend errors weaken the information supplied to every reader, while the retrieval fetch supplies much of the added reach.\n")
BULLET_OLD = "\\item Evidence that names carry the judgment. The two models ablated score $0.12$ and $0.16$ lower on counts alone than on names alone; no model reliably exceeds a name lookup on the named state, and Luna, Sol and Opus lead it only through the states the summary merely counts.\n"
BULLET_NEW = ("%% R131 E (2026-09-20): the author's second contribution.\n"
              "\\item Evidence about what readers read. The two smaller models use only the names and three stronger models also use the counts; on the named state no model reliably exceeds a name lookup, including under a sibling-name control that holds counts and list length fixed; and a lookup with one count feature matches the stronger models within triples.\n")
CONC_OLD = ("In these tests, the information a store wrote down counted for more than the choice of reader. Removing names weakens the obligation judgment more than removing counts. Under the default summary, no model reliably exceeds the name lookup on supersession, while some models add signal on counted states. With all states named, Opus has a reliable overall advantage. The explicit intent test shows a further distinction among readers, bounded by the fixed cue list's performance.\n")
CONC_NEW = ("%% R131 E (2026-09-20): sentences two to four in the author's words.\n"
            "In these tests, the information a store wrote down counted for more than the choice of reader. The smaller models read only the names; the stronger ones also read the counts, and a lookup given one count feature matches them within triples. On a named state no model reliably exceeds the name lookup, with list length held fixed or not; with all states named, Opus's $0.03$ lead is reliable on one metric and not on the other. The explicit intent test shows a further distinction among readers, bounded by the fixed cue list's performance.\n")
EVID_OLD = "Exact counterfactual labels & Constructed store versions isolate summary information; comparison with \\present{} alone is post hoc.\\\\\n"
EVID_NEW = "Exact counterfactual labels & Constructed store versions isolate summary information; the matched within-triple comparison is post hoc.\\\\\n"

# ----------------------------------------------------------------------------------------------------------------------- F. Section 6
FRB_OLD = ("%% R126 addendum A7 (2026-09-20): the author's sentence; the 'Haiku fares better' paragraph moved to Appendix E.9 (AUX-BH-SPLIT).\n"
           "Haiku retains more of its gain than mini does, and more where the target's name survives the store's list ($0.87$ against $0.68$ where it does not; descriptive). (Appendix~\\ref{app:census})\n")
FRB_NEW = ("%% R131 F (2026-09-20): the author's two sentences (R125 Task 3, AUX-CF2-R125-T3-FRBANK: on the 82 join-marked, capped minus ground truth mini -0.1274, Haiku -0.1258, the lookup -0.2027, each reliable); the name-survival clause is in Appendix E.9 (AUX-BH-SPLIT).\n"
           "Haiku retains more of its gain than mini does. The loss is not an artifact of the obligations the join misses: on the $82$ it marks, the capped summary still costs mini $0.13$, Haiku $0.13$ and the lookup $0.20$, each reliable. (Appendix~\\ref{app:census})\n")
GRA_OLD = ("\\claim{Graphiti's names serve the lookup better than mini.}\n"
           "On Graphiti's full-store questions, mini scores $0.58$ with the capped store-written summary, against $0.74$ under ground truth.\n"
           "It gains nothing reliable over question only.\n"
           "The lookup scores $0.68$, a reliable margin of $0.10$ over mini.\n"
           "The reduced variants used elsewhere do not exist on these graphs. (Appendix~\\ref{app:posthoc-graphiti})\n\n"
           "\\claim{Graphiti's invalidation recovers some forbidding records, but misses most.}\n"
           "On its full-store obligations eligible for invalidation, Graphiti reaches $13$ of $34$, exceeding the predicted quarter.\n"
           "Retraction remains inexpressible under this backend's mapping. (Appendix~\\ref{app:posthoc-graphiti})\n")
GRA_NEW = ("%% R131 F (2026-09-20): the two Graphiti paragraphs merged in the author's words (AUX-R85-G10-*; R125 Task 3, AUX-CF2-R125-T3-GRAPHITI: retained 23 of 34, extraction misses 11; on the 23 mini capped 0.6920 against ground truth 0.8433, -0.1512 reliable).\n"
           "\\claim{Graphiti writes part of what the judgment needs, and part of its loss is extraction.}\n"
           "Its invalidation marks $13$ of the $34$ full-store obligations it could express, and $11$ of the $34$ were never extracted into the graph; retraction is inexpressible under this backend's mapping.\n"
           "With its capped store-written summary mini scores $0.58$ over all $47$ obligations, against $0.74$ under ground truth, and the store's own name lookup scores $0.68$, a reliable $0.10$ above mini.\n"
           "On the $23$ obligations whose content the graph retains, mini scores $0.69$ against $0.84$ under ground truth, still a reliable loss. (Appendix~\\ref{app:posthoc-graphiti})\n")

# ----------------------------------------------------------------------------------------------------------------------- G. Limitations
LIM_OLD_1 = ("The paraphrase check, with one rewording per question fixed in advance, is not yet scored. The intent questions contain explicit cues; questions without them are untested. The reader split cannot establish why the models differ and does not simply follow size. The capability comparison on the counterfactual set covers closed models from two vendors, with no open-weights model.\n"
             "Two further encoders leave the default lookup within $0.01$ of its score. Under the explicit-intent rubric, only mini and Luna were rerun on the original counterfactual task: both stay within $0.02$ of their main-study scores, and Luna retains a reliable lookup margin. (Appendix~\\ref{app:counterfactual})\n")
LIM_NEW_1 = ("%% R131 G (2026-09-20): the author's two sentences added; the encoder sentence (it stays in E.8) and the reader-split sentence deleted.\n"
             "The matched metric and every comparison made with it are post hoc; the registered metric is the pooled AUROC. Sol did not run the names-and-counts ablation, and among the stronger models only Opus ran the all-states summary. "
             "The paraphrase check, with one rewording per question fixed in advance, is not yet scored. The intent questions contain explicit cues; questions without them are untested. The capability comparison on the counterfactual set covers closed models from two vendors, with no open-weights model.\n"
             "Under the explicit-intent rubric, only mini and Luna were rerun on the original counterfactual task: both stay within $0.02$ of their main-study scores, and Luna retains a reliable lookup margin. (Appendix~\\ref{app:counterfactual})\n")
LIM_OLD_2 = "The ground-truth tags in retrieved views depend on aligning manifests to stored records. That alignment marks the forbidding record for $82$ of $104$ obligations. Answer outcomes remain exploratory:"
LIM_NEW_2 = ("%% R131 G (2026-09-20): the author's sentence for the alignment sentence (R125 Task 3, AUX-CF2-R125-T3-FRBANK: the 22 unmarked; mini's ground-truth row on them 0.5210).\n"
             "The ground-truth name lists are built through the manifest-to-record alignment, so the $22$ obligations it does not mark are invisible to every summary (mini scores $0.52$ on them under ground truth). Answer outcomes remain exploratory:")

# ----------------------------------------------------------------------------------------------------------------------- H. the payers, in the brief's order, only as needed
PAYERS = {
    1: ("Section 7, the gating paragraph",
        "\\claim{Gating trades retrieval budget against licensed-record reach.}\n"
        "Unmatched, the always-on fetch spends $1.20$ times the lines per question.\n"
        "Truncating it to the gated budget removes licensed records, a reliable loss of $0.04$.\n"
        "This budget comparison averages over all questions, rather than obligations alone. (Appendix~\\ref{app:resp})\n",
        "%% R131 H1 (2026-09-20): the page payer, the author's paragraph.\n"
        "\\claim{Gating trades budget against licensed-record reach.}\n"
        "Unmatched, the always-on fetch spends $1.20$ times the lines per question; truncated to the gated budget it loses licensed records, a reliable $0.04$. (Appendix~\\ref{app:resp})\n"),
    2: ("Section 7, the FR-Bank tags paragraph",
        "\\claim{FR-Bank's own tags help mini despite over-marking.}\n"
        "Its view-only score rises reliably from $0.69$ to $0.81$ with native tags, whose precision over retrieved lines is $0.14$.\n"
        "The native tags mark more forbidding records already in view.\n"
        "A reader that merely counts tagged lines scores $0.62$ under either tag source.\n"
        "This is descriptive, without a prediction fixed in advance.\n"
        "On Graphiti's full-store questions, adding native tags to the same retrieved edges produces no reliable improvement. (Appendix~\\ref{app:posthoc-graphiti})\n",
        "%% R131 H2 (2026-09-20): the page payer, the author's paragraph.\n"
        "\\claim{FR-Bank's own tags help mini despite over-marking.}\n"
        "Its view-only score rises reliably from $0.69$ to $0.81$ with native tags, whose precision over retrieved lines is $0.14$, because they mark more of the forbidding records already in view; a reader that merely counts tagged lines scores $0.62$ under either tag source.\n"
        "On Graphiti, native tags on the same retrieved edges bring no reliable improvement. (Appendix~\\ref{app:posthoc-graphiti})\n"),
    3: ("Related work, the last paragraph",
        "Lifecycle information also appears in temporal databases, removal tombstones in replicated sets, and truth maintenance \\citep{snodgrass1986,shapiro2011,doyle1979}. Zep's validity intervals provide related metadata for agent memory \\citep{zep}. Other work evaluates obligations supplied by policies or revisions \\citep{nissenbaum2004,cimemories,maini2024,gatemem,pmbench,hushbench,statemembench}, or studies knowledge conflicts and temporal knowledge inside models \\citep{xu2024conflicts,longpre2021,dhingra2022}. Our target is the pre-retrieval judgment about the store, derived from the stored content's lifecycle state.\n",
        "%% R131 H3 (2026-09-20): the page payer, the paragraph trimmed to its first and last sentences (the citation keys of the two dropped sentences move to the first so every bibliography entry stays cited).\n"
        "Lifecycle information also appears in temporal databases, removal tombstones in replicated sets, and truth maintenance \\citep{snodgrass1986,shapiro2011,doyle1979,zep,nissenbaum2004,cimemories,maini2024,gatemem,pmbench,hushbench,statemembench,xu2024conflicts,longpre2021,dhingra2022}. Our target is the pre-retrieval judgment about the store, derived from the stored content's lifecycle state.\n"),
    4: ("Section 3, the masking sentence",
        "Masking non-active records removes the very records whose tags could reveal an obligation, so masked retrieval cannot provide that judgment on its own.",
        "Masking non-active records removes the records whose tags could reveal an obligation."),
}


def main():
    check = "--check" in sys.argv
    payers = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--payers=")), "")
    payers = sorted(int(x) for x in payers.split(",") if x.strip())
    b = rd(OUT_B)
    a = rd(OUT_A)
    assert "%% R131" not in b and "%% R131" not in a, "port_r131.py: already applied (run port_v22.py first)"

    # A
    b = rep(b, S4_OLD, S4_NEW, where="A Section 4")
    # B: Section 5.1 whole, from the subsection head to Table 1
    i = b.index("\\subsection{Names against counts}\\label{sec:names_counts}\n")
    j = b.index("\\begin{table}[t]\n%% R126 (2026-09-19): Table 1 in the inbox's layout", i)
    b = b[:i] + S51_NEW + b[j:]
    # D: Table 1
    i = b.index("\\begin{table}[t]\n%% R126 (2026-09-19): Table 1 in the inbox's layout")
    j = b.index("\\end{table}\n", i) + len("\\end{table}\n")
    b = b[:i] + TAB1 + b[j:]
    # C: Section 5.2 from the subsection head to the long-or-wrong-lists paragraph (kept, the R129 version)
    i = b.index("\\subsection{The lookup against the models}\\label{sec:lookup}\n")
    j = b.index("%% R126 addendum A6 (2026-09-20): the author's paragraph.\n%% R129 C2 (2026-09-20): the author's paragraph.\n\\claim{Long or wrong name lists weaken the readers together.}", i)
    b = b[:i] + S52_NEW + b[j:]
    # D: Figure 3
    b = rep(b, FIG3_OLD_HEAD, FIG3_NEW_HEAD, where="D Figure 3 head")
    b = rep(b, FIG3_AXIS_OLD, FIG3_AXIS_NEW, where="D Figure 3 axis")
    b = rep(b, FIG3_CAP_OLD, FIG3_CAP_NEW, where="D Figure 3 caption")
    # E
    a = rep(a, ABS_OLD, ABS_NEW, where="E abstract")
    b = rep(b, S1_OLD, S1_NEW, where="E Section 1")
    b = rep(b, BULLET_OLD, BULLET_NEW, where="E bullet 2")
    b = rep(b, CONC_OLD, CONC_NEW, where="E Conclusion")
    b = rep(b, EVID_OLD, EVID_NEW, where="E evidence table")
    # F
    b = rep(b, FRB_OLD, FRB_NEW, where="F FR-Bank")
    b = rep(b, GRA_OLD, GRA_NEW, where="F Graphiti")
    # G
    b = rep(b, LIM_OLD_1, LIM_NEW_1, where="G Limitations 1")
    b = rep(b, LIM_OLD_2, LIM_NEW_2, where="G Limitations 2")
    # H (the appendix): the prediction count with the two R125 registrations in it (reviews/NUMBERS_R131.md AUX-R131-COUNT: 93 / 29 -> 98 / 31; P-SB1 and P-SB3 not counted)
    b = rep(b, "each before the run that tests it: $29$ of $93$ came out otherwise.", "each before the run that tests it: $31$ of $98$ came out otherwise.", where="H the count")
    # H
    for k in payers:
        where, old, new = PAYERS[k]
        b = rep(b, old, new, where=f"H payer {k}: {where}")

    # ---- the gate-driven wording changes (each the smallest change satisfying its rule; listed old beside new in the report and CLAIMS.md)
    b, a = gates(b, a)

    for bad in ("%%FIG3-DATA%%",):
        assert bad not in b, bad
    assert "\u2014" not in b and "\u2014" not in a, "em dash"
    if check:
        print("port_r131.py --check: would write", OUT_B, OUT_A, "payers", payers)
        return
    io.open(OUT_B, "w", encoding="utf-8", newline="\n").write(b)
    io.open(OUT_A, "w", encoding="utf-8", newline="\n").write(a)
    print(f"-> {OUT_B} ({len(b.splitlines())} lines); {OUT_A}; payers applied: {payers or 'none'}")
    print("gate-driven wording changes:")
    for rule, sec, old, new in GATE_CHANGES:
        print(f"  [{rule}] {sec}\n     - {old[:160]}\n     + {new[:160]}")


# The gate-driven wording changes, added after the first gate run on the author's verbatim texts (reviews/v22/gates_r131_a.txt): each the smallest
# change satisfying its rule, listed old beside new in REPORT_R131.md and CLAIMS.md (entry R131-G). (target 'b' = the body, 'a' = the abstract.)
GATES = [
    # Section 4 (A): q_scan Q-C needs the AUROC definition's exact words ('scores above', as R126); Q-A bars a numeral in a paragraph's opening sentence
    # (the semicolon joined 'chance is $0.50$' to the opener); prose_scan rule V and code_scan bar 'registered' in the main text.
    ("b", "Q-C (the AUROC definition's words) and Q-A (the opener carried the numeral 0.50; split at the semicolon)", "Section 4",
     "the chance that a positive ranks above a negative \\citep{hanley1982}; chance is $0.50$.",
     "the chance that a positive scores above a negative \\citep{hanley1982}. Chance is $0.50$."),
    ("b", "V and code_scan ('registered' in the main text)", "Section 4",
     "The registered metric pools all items.", "The metric fixed in advance pools all items."),
    # Section 5.1 (B): prose_scan rule L caps a sentence at 40 words (51); split at the colon.
    ("b", "L (51 words; split at the colon)", "Section 5.1",
     "with the names unchanged, all three follow it: across the two counted states Opus falls",
     "with the names unchanged, all three follow it. Across the two counted states Opus falls"),
    # Section 5.2 (C): rule L (46 and 42 words); each split at its semicolon.
    ("b", "L (46 words; split at the semicolon)", "Section 5.2",
     "the lookup and Haiku score $0.78$ and mini $0.73$; Luna, Sol and Opus score $0.86$ to $0.88$,",
     "the lookup and Haiku score $0.78$ and mini $0.73$. Luna, Sol and Opus score $0.86$ to $0.88$,"),
    ("b", "L (42 words; split at the semicolon)", "Section 5.2",
     "the three stay a reliable $0.05$ to $0.06$ above it; their remaining edge is in pairs",
     "the three stay a reliable $0.05$ to $0.06$ above it. Their remaining edge is in pairs"),
    # The abstract (E): rule L (48 words; split at the colon); rule V bars 'held' ('kept'); rule G2 bars the lookup's own level as 'at $0.xx$' in an
    # abstract sentence that names the lookup ('at or above $0.88$' states the same bound outside the pattern).
    ("a", "L (48 words; split at the colon), V ('held'), G2 ('at $0.88$ or higher' in a sentence naming the lookup)", "Abstract",
     "no model reliably beats a cosine lookup over the names: with counts and list length held fixed, the lookup and every model separate the right name from a sibling at $0.88$ or higher, while meaningless tokens and counts fall to chance.",
     "no model reliably beats a cosine lookup over the names. With counts and list length kept fixed, the lookup and every model separate the right name from a sibling at or above $0.88$, while meaningless tokens and counts fall to chance."),
    # Section 1 (E): rule V ('held'); rule D (71% with the abstract's third sentence: 'matched' dropped; 71% with the 5.1 claim: 'only the attribute
    # names' reads 'the attribute names alone').
    ("b", "V ('held')", "Section 1",
     "no model reliably outscores the lookup, with list length held fixed or not.",
     "no model reliably outscores the lookup, with list length kept fixed or not."),
    ("b", "D (71% with the abstract's third sentence)", "Section 1",
     "a lookup given one count feature catches them within matched triples.",
     "a lookup given one count feature catches them within triples."),
    ("b", "D (71% with Section 5.1's first claim)", "Section 1",
     "The two smaller models read only the attribute names; Luna, Sol and Opus also read the counts.",
     "The two smaller models read the attribute names alone; Luna, Sol and Opus also read the counts."),
    # The Conclusion (E): rule V ('held').
    ("b", "V ('held')", "Conclusion",
     "no model reliably exceeds the name lookup, with list length held fixed or not;",
     "no model reliably exceeds the name lookup, with list length kept fixed or not;"),
    # Section 6 (F): s17_grep bars 'the join' in the main text (E.1 maps it; Section 9 calls it the alignment).
    ("b", "S17 ('the join')", "Section 6",
     "The loss is not an artifact of the obligations the join misses: on the $82$ it marks,",
     "The loss is not an artifact of the obligations the alignment misses: on the $82$ it marks,"),
    # Limitations (G): rule V and code_scan ('registered'); Q-A (the new paragraph opened on a numeral; split after 'alignment').
    ("b", "V and code_scan ('registered' in the main text)", "Limitations",
     "the registered metric is the pooled AUROC.", "the metric fixed in advance is the pooled AUROC."),
    ("b", "Q-A (the opener carried the numeral 22; split after 'alignment')", "Limitations",
     "The ground-truth name lists are built through the manifest-to-record alignment, so the $22$ obligations it does not mark are invisible to every summary",
     "The ground-truth name lists are built through the manifest-to-record alignment. The $22$ obligations it does not mark are therefore invisible to every summary"),
]


# The payers' own gate-driven change (gates_r131_c.txt): payer 2's first sentence is 43 words (rule L caps 40); split at its semicolon. Applied only when payer 2 is in.
GATES_PAYERS = [
    ("b", "L (43 words; split at the semicolon)", "Section 7, payer 2",
     "because they mark more of the forbidding records already in view; a reader that merely counts tagged lines scores $0.62$ under either tag source.",
     "because they mark more of the forbidding records already in view. A reader that merely counts tagged lines scores $0.62$ under either tag source."),
]


def gates(b, a):
    for target, rule, section, old, new in GATES + [g for g in GATES_PAYERS if g[3] in b]:
        if target == "b":
            b = gate(rule, section, b, old, new)
        else:
            a = gate(rule, section, a, old, new)
    return b, a


if __name__ == "__main__":
    main()
