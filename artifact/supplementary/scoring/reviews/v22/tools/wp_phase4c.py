# -*- coding: utf-8 -*-
"""wp_phase4c.py -- the writing pass, Phase 4c (2026-09-15): the eleven lines, on the author's ruling. Layout first, no words changed, in the
author's order: (L1) Figure 2's tabular with the row padding tightened, target 13 lines; (L2) Table 1 tightened, target 15; (L3) Figure 1's
drawing compacted so the float is 16 lines with the caption; (L4) the box's inter-row and frame spacing tightened, target 13. Nothing set
below its present size (Figure 2's tabular is \\footnotesize, Table 1 and the box \\scriptsize already; \\small, 9 pt, would enlarge them),
no change to line spacing, margins or the style file. Then (W) the author's cold-read ruling: eight meaning fixes and twelve free fixes,
plus the writer's cold-read stalls that the ruling did not supersede. Then, only if the fine number is still above 483, the cuts in the
author's order: (C1) Section 1's second and third paragraphs to five lines each; (C2) Section 9's pointers paragraph to two sentences;
(C3) Section 7's 53-of-63 paragraph to three sentences.

Then (R) the author's ruling on the Phase 4c report (2026-09-15, evening): Figure 2's caption in the author's three lines, Tables 6 and 7's
row padding to 0.9, and bullet 3 gains "(retracted and expired)" (it stays on two lines).

Regenerates from the Phase 4b state (wp_phase4b.py, itself from 6dbabdf). Usage: python reviews/v18/tools/wp_phase4c.py [--layout=N] [--words] [--cuts=N] [--ruling]
(--layout=4 --words is the state before the cuts; --cuts=N applies the first N cuts; --ruling applies the author's ruling on the 4c report;
the committed 4c state is --layout=4 --words --cuts=3 --ruling).
"""
from __future__ import annotations

import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "reviews" / "v18" / "tools"
BODY = ROOT / "reviews" / "v18" / "src" / "body_v18.tex"


def rep(text, old, new, n=1):
    assert text.count(old) == n, (text.count(old), old[:90])
    return text.replace(old, new)


# ---------------------------------------------------------------------------------------------------------------------------
# layout
# ---------------------------------------------------------------------------------------------------------------------------
def L1_figure2(t):
    """Figure 2's tabular: row padding 1.1 -> 0.95, column separation 5pt -> 3pt, the first and last columns widened so their cells stop wrapping."""
    t = rep(t, "\\footnotesize\n\\setlength{\\tabcolsep}{5pt}\n\\renewcommand{\\arraystretch}{1.1}\n"
               "\\begin{tabular}{@{}>{\\raggedright\\arraybackslash}p{0.27\\linewidth}>{\\raggedright\\arraybackslash}p{0.21\\linewidth}>{\\raggedright\\arraybackslash}p{0.23\\linewidth}>{\\raggedright\\arraybackslash}p{0.21\\linewidth}@{}}\n",
               "\\footnotesize\n\\setlength{\\tabcolsep}{2pt}\n\\renewcommand{\\arraystretch}{0.95}\n"
               "%% Phase 4c (L1): the row padding tightened and the outer columns widened so no cell wraps; the words are unchanged.\n"
               "\\begin{tabular}{@{}>{\\raggedright\\arraybackslash}p{0.34\\linewidth}>{\\raggedright\\arraybackslash}p{0.20\\linewidth}>{\\raggedright\\arraybackslash}p{0.20\\linewidth}>{\\raggedright\\arraybackslash}p{0.23\\linewidth}@{}}\n")
    return t


def L2_table1(t):
    """Table 1: column separation 3pt -> 2pt, row padding 0.9, the middle column widened so the population cells wrap once."""
    t = rep(t, "\\label{tab:setup}\n\\centering\n\\scriptsize\n\\setlength{\\tabcolsep}{3pt}\n\\begin{tabular}{@{}p{0.19\\linewidth}p{0.45\\linewidth}p{0.32\\linewidth}@{}}\n",
               "\\label{tab:setup}\n\\centering\n\\scriptsize\n\\setlength{\\tabcolsep}{2pt}\n\\renewcommand{\\arraystretch}{0.9}\n"
               "%% Phase 4c (L2): the row padding and column separation tightened, the population column widened; the words are unchanged.\n"
               "\\begin{tabular}{@{}p{0.165\\linewidth}p{0.505\\linewidth}p{0.31\\linewidth}@{}}\n")
    return t


def L3_figure1(t):
    """Figure 1's drawing compacted: the route boxes closer and the masked path nearer; fonts, widths and words unchanged."""
    t = rep(t, "  box/.style={draw, thick, rounded corners=2pt, inner sep=3.5pt, align=left, font=\\footnotesize},",
               "  box/.style={draw, thick, rounded corners=2pt, inner sep=2.5pt, align=left, font=\\footnotesize},   % Phase 4c (L3): the drawing compacted")
    t = rep(t, "  \\node[box, right=0.45cm of store.east, anchor=west, yshift=1.0cm, text width=4.0cm] (summ)",
               "  \\node[box, right=0.45cm of store.east, anchor=west, yshift=0.85cm, text width=4.0cm] (summ)")
    t = rep(t, "  \\node[box, below=0.22cm of summ, text width=4.0cm] (tags)", "  \\node[box, below=0.12cm of summ, text width=4.0cm] (tags)")
    t = rep(t, "  \\coordinate (my) at ($(tags.south)+(0mm,-4.2mm)$);", "  \\coordinate (my) at ($(tags.south)+(0mm,-3.6mm)$);")
    return t


def L4_box(t):
    """The notation box: frame padding 3pt -> 1.5pt, no lead gap, row padding 0.92, the description column a little wider (the term column keeps its width so "route A; route B" does not break)."""
    old = ("\\begin{center}\n\\fbox{\\begin{minipage}{0.97\\linewidth}\n\\scriptsize\n\\setlength{\\tabcolsep}{2pt}\n"
           "\\noindent\\textbf{Notation.} The terms below are used verbatim throughout.\\par\\vspace{1pt}\n")
    new = ("\\begin{center}\n\\setlength{\\fboxsep}{1.5pt}%% Phase 4c (L4): the frame and row spacing tightened; the words are unchanged\n"
           "\\fbox{\\begin{minipage}{0.97\\linewidth}\n\\scriptsize\n\\setlength{\\tabcolsep}{1.5pt}\n\\renewcommand{\\arraystretch}{0.92}\n"
           "\\noindent\\textbf{Notation.} The terms below are used verbatim throughout.\\par\n")
    t = rep(t, old, new)
    t = rep(t, "\\begin{tabular}[t]{@{}p{0.115\\linewidth}p{0.355\\linewidth}@{}}", "\\begin{tabular}[t]{@{}p{0.115\\linewidth}p{0.36\\linewidth}@{}}", 2)
    return t


LAYOUT = [L1_figure2, L2_table1, L3_figure1, L4_box]


# ---------------------------------------------------------------------------------------------------------------------------
# the cold-read ruling (the author's items 1 to 20) and the writer's stalls the ruling did not supersede
# ---------------------------------------------------------------------------------------------------------------------------
def words(t):
    # Section 1, paragraph 1: the two things named (stall 1), the store and the never-asked-for record (stall 2), the author's 9
    t = rep(t, "An agent with a long memory has to know two things before it retrieves.\n"
               "A user plans a Saturday hike and then cancels it; an agent that fetches the plan and not the cancellation answers wrong.\n"
               "We call that record, a non-active record whose use would make the answer wrong, the \\emph{forbidding record}.\n"
               "The judgment that such a record exists, made before retrieval, is negative-obligation knowledge (NOK), the obligation judgment.\n"
               "That the store covers the question is feeling of knowing (FOK), the coverage judgment \\citep{hart1965,nelson1990,koriat1993}.\n",
               "An agent with a long memory has to know two things before it retrieves: whether the store covers the question, and whether it holds something it must no longer use.\n"
               "A user plans a Saturday hike and then cancels it, and the store keeps both.\n"
               "An agent that fetches the plan and not the cancellation answers wrong, and the record that would have stopped it is one it never asked for.\n"
               "We call the cancellation a \\emph{forbidding record}: a non-active record whose use would make the answer wrong.\n"
               "The judgment that such a record exists, made before retrieval, is negative-obligation knowledge (NOK), the obligation judgment.\n"
               "Whether the store covers the question at all is feeling of knowing (FOK), the coverage judgment \\citep{hart1965,nelson1990,koriat1993}.\n")
    # paragraph 2: the monitor named (stall 4), the author's 5, the routes introduced (stall 5), indexed and blind glossed (stall 6)
    t = rep(t, "The monitor sees a lifecycle summary: a count table per category and state, and a name map with the values removed (Figure~\\ref{fig:framework}).\n",
               "Both judgments are made by a monitor, a lookup or a model, from a lifecycle summary: a count table per category and state, and a name map with the values removed (Figure~\\ref{fig:framework}).\n")
    t = rep(t, "Three language models from two vendors read a lifecycle summary by its names and not by its counts.\n",
               "The three models tested on the summary alone read it by its names and not by its counts (Section~\\ref{sec:counterfactual}).\n")
    t = rep(t, "The summary is route A; route B is unmasked retrieval, which returns non-active records with their tags.\n",
               "Two routes carry the obligation to the monitor: the summary is route A; route B is unmasked retrieval, which returns non-active records with their tags.\n")
    t = rep(t, "A \\emph{gain} is the indexed score minus the blind score on the same questions.\n",
               "A \\emph{gain} is the score with the summary (indexed) minus the score without it (blind), on the same questions.\n")
    # bullet 3, the author's 6
    t = rep(t, "\\item We show monitors read the summary's \\emph{names}, not its counts: the name lookup matches two of three models and none reads counted states until named.\n",
               "\\item We show monitors read names, not counts: the name lookup matches two of three models, and no model reads a state the summary only counts.\n")
    # Section 3: the author's 10 and 11
    t = rep(t, "A retriever that masks non-active records from its ranking, as lifecycle-tracking and overwriting stores do, cannot supply the obligation judgment on its own.\n"
               "That is the crossed-out path",
               "A retriever that masks non-active records from its ranking, as lifecycle-tracking and overwriting stores do, cannot supply the obligation judgment on its own, because the mask drops the records whose tags carry it.\n"
               "That is the crossed-out path")
    t = rep(t, "the count table is carried because it was part of the summary as fixed before the study.\n",
               "the count table is included because it was part of the summary as fixed before the study.\n")
    # Section 4: stall 9, the author's 8 (stall 10), stall 11, stall 16 (persona), stall 12, stall 13, stall 14, stall 15, stall 18, stall 17; Table 1's 12 and 13
    t = rep(t, "FR-Bank \\citep{fr} is the only backend that tags every entry with a lifecycle state.\n"
               "Its stock configuration masks non-active records from retrieval, and retraction records pass that mask at $5\\%$ (Appendix~\\ref{app:census}).\n",
               "Of the three backends, FR-Bank \\citep{fr} is the only one that tags every entry with a lifecycle state.\n"
               "Its stock configuration masks non-active records from retrieval, and under that mask its own retraction questions pass at $5\\%$ (Appendix~\\ref{app:census}).\n")
    t = rep(t, "ran every population at five, and GPT-5.6 Sol", "ran every population at five calls, and GPT-5.6 Sol")
    t = rep(t, "Every question set was generated with large language models from human-written manifests, and the manifests are the ground truth every label is scored against.\n"
               "Labels follow Definition~\\ref{def:coverage}, and every \\pn{} label was verified by hand from the judgments that compose it.\n"
               "A presence control confirms that each target is stored, so a mislabeled \\absent{} item is unlikely ($5.2\\%$ at the observed base rate; Appendix~\\ref{app:construction}).\n",
               "Every question set was generated with large language models from human-written manifests of synthetic users (personas), and the manifests are the ground truth every label is scored against.\n"
               "Labels follow Definition~\\ref{def:coverage}, and every \\pn{} label was verified by hand.\n"
               "A presence control confirms that each target is stored, so the chance that an \\absent{} label is wrong is $5.2\\%$ at the observed base rate (Appendix~\\ref{app:construction}).\n")
    t = rep(t, "It binds on the store's own metadata, so the lifted rendering is reported beside the capped figure (Appendix~\\ref{app:repro}).\n",
               "It binds on the store's own metadata, so both renderings are reported, capped and with the cap lifted (Appendix~\\ref{app:repro}).\n")
    t = rep(t, "The monitor returns a probability under a fixed rubric, and the two prompts differ only in whether the summary precedes the question, so the gain isolates the summary (Appendix~\\ref{app:construction}).\n",
               "The monitor returns a probability under a fixed rubric, and the blind and the indexed prompt differ only in whether the summary precedes the question, so the gain isolates the summary (Appendix~\\ref{app:construction}).\n")
    t = rep(t, "to the names in the summary's superseded list (Appendix~\\ref{app:baselines}).\n", "to the summary's superseded-names list (Appendix~\\ref{app:baselines}).\n")
    t = rep(t, "Probes on the question text alone reach $0.80$ to $0.97$ (Appendix~\\ref{app:questionprior}), which is why we report paired gains and the counterfactual set.\n",
               "Question wording alone carries much of a blind score: probes on the question text reach $0.80$ to $0.97$ (Appendix~\\ref{app:questionprior}), which is why we report paired gains and the counterfactual set.\n")
    t = rep(t, "$^{a}$Three draws per question under each prompt on this set, one call on every other; the score resolution of the one-call and five-call rows is in Appendix~\\ref{app:counterfactual}.\n",
               "$^{a}$GPT-4.1 mini ran three draws per question under each prompt on this set and one call per question on every other set; the score resolution of the one-call and five-call rows is in Appendix~\\ref{app:counterfactual}.\n")
    t = rep(t, "the easy tier & $354$ questions ($243$ non-\\absent{}, $69$ obligations): a whole category removed for absence & the same \\\\",
               "the easy tier & $354$ questions ($243$ non-\\absent{}, $69$ obligations): absent items made by removing a whole category from the store & the same \\\\")
    # Section 5: the author's 2 (the bound on the counted states; both readers' numbers; the legend), 3 and 14
    t = rep(t, "A category-aware count reader, which takes the category from the manifest, is that reader's oracle upper bound.\n",
               "A category-aware count reader, which takes the category from the manifest, is that reader's upper bound on the two counted states.\n")
    t = rep(t, "The category-aware reader separates the retracted versions at $0.73$ and the expired versions at $0.78$ on the counterfactual set ($30$ pairs each), where every model scores $0.53$ to $0.62$.\n"
               "The count identifies the right version here because the category usually has no other retracted or expired entry ($26$ of $30$ retraction pairs, $15$ of $30$ expiry pairs), so the count goes from zero to one.\n",
               "The category-guessing count reader separates the retracted versions at $0.67$ and the expired at $0.69$ ($30$ pairs each), its category-aware oracle at $0.73$ and $0.78$, where every model scores $0.53$ to $0.62$.\n"
               "% AUX-R110-A1-CR: the category-guessing reader 0.6669 / 0.6872, the category-aware reader 0.7306 / 0.7778 on retraction / expiry (Table tab:cf-cr); the models 0.5283 to 0.6150 (reviews/NUMBERS_WP.md section 5)\n"
               "In most retraction pairs and half the expiry pairs the category has no other such entry ($26$ of $30$ and $15$ of $30$), so the count goes from zero to one.\n")
    t = rep(t, "count reader (left panel)}", "count reader (category-aware, left panel)}")
    t = rep(t, "The all-states lookup scores $0.88$ on the whole set, and Haiku 4.5's gain on the two counted states is a reliable $+0.30$.\n",
               "The all-states lookup scores $0.88$ on the whole set, and Haiku 4.5 gains a reliable $+0.30$ on the two counted states once they are named.\n")
    # Section 6: the author's 15
    t = rep(t, "The reason is that the store's tags reach more of the forbidding records, not that there are more tags.\n",
               "The reason is that the store's tags reach more of the forbidding records.\n")
    # Table 4's caption: the author's 16
    t = rep(t, "The store that conflates retraction with supersession is described in Appendix~\\ref{app:census}.}",
               "FR-Bank's conflation of retraction with supersession is described in Appendix~\\ref{app:census}.}")
    # Section 7: the author's 17
    t = rep(t, "It is $0.69$ on the whole population (Section~\\ref{sec:counterfactual}).\n", "That floor is $0.69$ on the whole population (Section~\\ref{sec:counterfactual}).\n")
    # Section 8: the author's 4
    t = rep(t, "Against a record we deleted, FOK moves from $0.43$ to $0.50$ and stays at chance, so the single missing record is NOK's target.\n",
               "FOK detects a missing topic, $0.55$ to $0.88$, but not a single deleted record, $0.43$ to $0.50$, chance.\n"
               "The missing record is NOK's target.\n")
    # Section 9: the author's 1, 18, 19; Table 7's Wilson interval on the all-states row (the author's 7; reviews/v18/tools/wilson_a7.py)
    t = rep(t, "The gated rules fall between, and every Wilson interval overlaps (Table~\\ref{tab:ds-body}).\n",
               "The gated rules are lower, $0.13$ and $0.10$, and every Wilson interval overlaps, so no policy changes the rate reliably (Table~\\ref{tab:ds-body}).\n")
    t = rep(t, "Three further results are stated in one sentence each.\n", "Three further results, one sentence each.\n")
    t = rep(t, "Retagging the $35$ duplicates the audit found cuts stale answers under the gated fetch from $0.15$ to $0.03$ of the reached obligations for GPT-4.1 mini.\n",
               "Retagging the $35$ duplicates the audit found cuts stale answers under the gated fetch from $0.15$ to $0.03$ for GPT-4.1 mini, over all reached obligations, a wider denominator than Table~\\ref{tab:ds-body}'s scorable set.\n")
    t = rep(t, "Model rule, all states named and scored & $89$ & $12$ & $11$ of $65$, $0.17$ & -- & $44$ \\\\",
               "Model rule, all states named and scored & $89$ & $12$ & $11$ of $65$, $0.17$ & $[0.10,0.28]$ & $44$ \\\\")
    # Limitations: the author's 20
    t = rep(t, "The tagged route under the store's own tags is descriptive, with no prediction fixed in advance for its rise, which is the tags' reach of the forbidding records rather than their density (Section~\\ref{sec:routes}).\n",
               "The tagged route under the store's own tags is descriptive, with no prediction fixed in advance for its rise.\n")
    return t


# ---------------------------------------------------------------------------------------------------------------------------
# the cuts, only if the fine number is still above 483, in the author's order
# ---------------------------------------------------------------------------------------------------------------------------
def C1_section1(t):
    """Section 1's second and third paragraphs to five lines each (the author's C1); the first paragraph gives back the store clause of stall 2,
    because the notation box fits page 3 only if Section 1 does not grow."""
    t = rep(t, "A user plans a Saturday hike and then cancels it, and the store keeps both.\n", "A user plans a Saturday hike and then cancels it.\n")
    t = rep(t, "Both judgments are made by a monitor, a lookup or a model, from a lifecycle summary: a count table per category and state, and a name map with the values removed (Figure~\\ref{fig:framework}).\n",
               "A monitor makes both judgments from a lifecycle summary, a count table and a name map with the values removed (Figure~\\ref{fig:framework}).\n")
    t = rep(t, "Two routes carry the obligation to the monitor: the summary is route A; route B is unmasked retrieval, which returns non-active records with their tags.\n"
               "Every score in this paper is an AUROC, the chance that a positive scores above a negative, so $0.50$ is chance.\n"
               "A \\emph{gain} is the score with the summary (indexed) minus the score without it (blind), on the same questions.\n",
               "Route A is that summary; route B is unmasked retrieval, returning non-active records with their tags.\n"
               "Every score is an AUROC, the chance that a positive scores above a negative, so $0.50$ is chance and a \\emph{gain} is the indexed score minus the blind score.\n")
    t = rep(t, "Prior work on memory scores what an agent retrieves or answers, after retrieval \\citep{longmemeval,locomo,memoryagentbench,stale}.\n"
               "On MemoryAgentBench's conflict-resolution questions no memory agent exceeds $7\\%$ accuracy \\citep{memoryagentbench}.\n"
               "We measure both judgments on stores we built, so that every label is exact, across three memory backends and six language models from three vendors.\n"
               "Most of the evidence concerns the obligation judgment; the coverage judgment rides on the same summary (Section~\\ref{sec:populations}).\n"
               "This paper makes five contributions.\n",
               "Prior work on memory scores what an agent retrieves or answers \\citep{longmemeval,locomo,memoryagentbench,stale}.\n"
               "On MemoryAgentBench's conflict-resolution questions no memory agent exceeds $7\\%$ accuracy.\n"
               "We measure both judgments on stores built with exact labels, across three backends and six models from three vendors.\n"
               "Most of the evidence concerns the obligation judgment, and the coverage judgment rides on the same summary (Section~\\ref{sec:populations}); the contributions are five.\n")
    return t


def C2_section9(t):
    """Section 9's pointers paragraph to the two results of item 42, the header and the composite, under the plain opener (Q-A); the depth
    sentence and the composite's gloss go, and the opener's list of links drops the depth."""
    t = rep(t, "The links are reach, the tags, the store's untagged duplicates, their repair, and the depth the coverage judgment buys.\n",
               "The links are reach, the tags, the store's untagged duplicates and their repair.\n")
    t = rep(t, "Three further results, one sentence each.\n", "Two further results, one sentence each.\n")
    t = rep(t, "Where the coverage judgment expands the view, Haiku~4.5 matches a ten-line view's correct count at $8.3$ lines, a reliable $+0.04$ over a flat view of equal cost (Table~\\ref{tab:ds-a6}, Appendix~\\ref{app:resp}).\n", "")
    t = rep(t, "It counts a licensed item answered correctly, an obligation reached and reported, and an absent item abstained on.\n", "")
    return t


def C3_section7(t):
    """Section 7's 53-of-63 paragraph to three sentences: the floor's definition folds into Section 5's pointer, and the whole-population
    floor (0.69) stands in Section 5."""
    t = rep(t, "Where the store still writes the item's own name Haiku 4.5 scores it at its ground-truth level, and where it does not the model falls to the floor the own-name ablation found.\n"
               "That floor is the score after the target's own name is removed from the list.\n",
               "Where the store still writes the item's own name Haiku 4.5 scores it at its ground-truth level, and where it does not the model falls to the floor the own-name ablation found (Section~\\ref{sec:counterfactual}).\n")
    t = rep(t, "That floor is $0.69$ on the whole population (Section~\\ref{sec:counterfactual}).\n", "")
    return t


CUTS = [C1_section1, C2_section9, C3_section7]


# ---------------------------------------------------------------------------------------------------------------------------
# the author's ruling on the Phase 4c report (2026-09-15, evening): the two lines that bring the Conclusion's box onto page 9
# ---------------------------------------------------------------------------------------------------------------------------
def ruling(t):
    """Figure 2's caption in the author's words (three lines; the C.2 pointer in a clause); Tables 6 and 7 at row padding 0.9 (the
    values and words unchanged); bullet 3 names the two counted states in a parenthetical (28 words, still two lines)."""
    t = rep(t, "\\caption{A retraction triple of the counterfactual set. The question is fixed; the three store versions differ in one attribute, and only the summary lines that differ are shown, with the name lookup's score under each. Only the count row differs, so no reader over names can separate the versions; the supersession triple, where the obligation is named and the lookup separates the versions, is in Appendix~\\ref{app:counterfactual}.}",
               "\\caption{A retraction triple of the counterfactual set: one question, three store versions differing in one attribute; only the differing summary lines are shown, with the name lookup's score. Only the count row differs, so no reader over names separates the versions (supersession triple: Appendix~\\ref{app:counterfactual}).}")
    t = rep(t, "\\label{tab:e1}\n\\centering\n\\scriptsize\n\\setlength{\\tabcolsep}{2pt}\n",
               "\\label{tab:e1}\n\\centering\n\\scriptsize\n\\setlength{\\tabcolsep}{2pt}\n\\renewcommand{\\arraystretch}{0.9}%% Phase 4c ruling: row padding 0.9; the values are unchanged\n")
    t = rep(t, "\\label{tab:ds-body}\n\\centering\n\\scriptsize\n\\setlength{\\tabcolsep}{3pt}\n",
               "\\label{tab:ds-body}\n\\centering\n\\scriptsize\n\\setlength{\\tabcolsep}{3pt}\n\\renewcommand{\\arraystretch}{0.9}%% Phase 4c ruling: row padding 0.9; the values are unchanged\n")
    t = rep(t, "and no model reads a state the summary only counts.\n",
               "and no model reads a state the summary only counts (retracted and expired).\n")
    return t


def main():
    nl = int(next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--layout=")), "4"))
    do_words = "--words" in sys.argv[1:]
    nc = int(next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--cuts=")), "0"))
    r = subprocess.run([sys.executable, str(TOOLS / "wp_phase4b.py"), "--upto=S4"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-800:]
    t = io.open(BODY, encoding="utf-8").read()
    done = ["phase 4b"]
    for k in range(nl):
        t = LAYOUT[k](t); done.append(LAYOUT[k].__name__)
    if do_words:
        t = words(t); done.append("words")
    for k in range(nc):
        t = CUTS[k](t); done.append(CUTS[k].__name__)
    if "--ruling" in sys.argv[1:]:
        t = ruling(t); done.append("ruling")
    io.open(BODY, "w", encoding="utf-8", newline="\n").write(t)
    print("wp_phase4c: " + ", ".join(done))


if __name__ == "__main__":
    main()
