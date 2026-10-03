# -*- coding: utf-8 -*-
"""wp_phase4b.py -- the writing pass, Phase 4b (2026-09-15): Sections 1, 3 and 4 written fresh from the author's skeleton to their line
ceilings (Section 1: 50 lines with Figure 1 and the contributions; Section 3: 54 with the grid, the box and Figure 2; Section 4: 50 with
Table 1). The current text (the Phase 4 build) is the source of truth for every claim and number; nothing new is claimed. Tables, figures,
the grid, the box and both definitions are carried verbatim from the Phase 4 build. Listing 1 moves to Appendix E.3 (the skeleton's
"Listing N in App. E.3"); Figure 2 moves to the head of Section 5 (a transfer, counted there); Table 1 keeps one footnote, the draws, and
the score-resolution sentences of its old note land in Appendix C.2's score-resolution paragraph.

Regenerates from the Phase 4 state: runs wp_phase4.py --step=3 (which restores the sources from 6dbabdf and runs wp_phase3.py), then
rewrites the three sections in order. Usage: python reviews/v18/tools/wp_phase4b.py [--upto=S1|S3|S4]
"""
from __future__ import annotations

import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "reviews" / "v18" / "tools"
BODY = ROOT / "reviews" / "v18" / "src" / "body_v18.tex"
APPX = ROOT / "reviews" / "v18" / "src" / "appendix_v18.tex"


def block(t, start, end, start_from=0):
    """The text from the unique occurrence of `start` (searched from start_from) through the following `end`, inclusive."""
    i = t.index(start, start_from)
    assert t.count(start) == 1 or start_from > 0, start[:60]
    j = t.index(end, i) + len(end)
    return t[i:j]


def rep(text, old, new, n=1):
    assert text.count(old) == n, (text.count(old), old[:80])
    return text.replace(old, new)


# ---------------------------------------------------------------------------------------------------------------------------
# Section 1
# ---------------------------------------------------------------------------------------------------------------------------
def rewrite_S1(t):
    head = "\\section{Introduction}\\label{sec:intro}\n"
    nxt = "\\section{Related work}\\label{sec:related}\n"
    old = t[t.index(head):t.index(nxt)]
    fig1 = block(old, "\\begin{figure}[t]\n\\centering\n%% Writing pass Phase 3 (2026-09-15), item 56: Figure 1", "\\label{fig:framework}\n\\end{figure}\n")
    fig1 = rep(fig1,
        "\\caption{The framework. A store tags every record with a lifecycle state (grey rows are non-active). Route A is a summary the store maintains outside query time, a count table and a name map with every value removed; route B is top-$k$ retrieval without a mask, which returns non-active records with their tags. Either carries the obligation to a monitor that emits FOK and NOK before any content is retrieved; masked retrieval drops the tagged records and carries nothing.}\n",
        "\\caption{The framework: a tagged store (grey rows non-active), route A (the summary) and route B (the tags) to a monitor that emits FOK and NOK before retrieval, and masked retrieval with no route.}\n")
    new = (head + "\n"
        "%% Writing pass Phase 4b (2026-09-15): Section 1 written fresh from the author's skeleton (three paragraphs and five bullets at or under 25 words;\n"
        "%% reviews/v18/tools/wp_phase4b.py). Every claim and number is the Phase 4 text's; Figure 1 is carried verbatim. The thesis sentence stays in the\n"
        "%% second paragraph before the routes (the reader claim first, READER_CLAIM.md section 2; prose_scan rule G4).\n"
        "An agent with a long memory has to know two things before it retrieves.\n"
        "A user plans a Saturday hike and then cancels it; an agent that fetches the plan and not the cancellation answers wrong.\n"
        "We call that record, a non-active record whose use would make the answer wrong, the \\emph{forbidding record}.\n"
        "The judgment that such a record exists, made before retrieval, is negative-obligation knowledge (NOK), the obligation judgment.\n"
        "That the store covers the question is feeling of knowing (FOK), the coverage judgment \\citep{hart1965,nelson1990,koriat1993}.\n"
        "\n"
        "The monitor sees a lifecycle summary: a count table per category and state, and a name map with the values removed (Figure~\\ref{fig:framework}).\n"
        "%% The thesis sentence of READER_CLAIM.md section 2, split at its colon for the sentence-length rule; the abstract carries it whole.\n"
        "Three language models from two vendors read a lifecycle summary by its names and not by its counts.\n"
        "The summary is route A; route B is unmasked retrieval, which returns non-active records with their tags.\n"
        "Every score in this paper is an AUROC, the chance that a positive scores above a negative, so $0.50$ is chance.\n"
        "A \\emph{gain} is the indexed score minus the blind score on the same questions.\n"
        "\n"
        "Prior work on memory scores what an agent retrieves or answers, after retrieval \\citep{longmemeval,locomo,memoryagentbench,stale}.\n"
        "On MemoryAgentBench's conflict-resolution questions no memory agent exceeds $7\\%$ accuracy \\citep{memoryagentbench}.\n"
        "We measure both judgments on stores we built, so that every label is exact, across three memory backends and six language models from three vendors.\n"
        "Most of the evidence concerns the obligation judgment; the coverage judgment rides on the same summary (Section~\\ref{sec:populations}).\n"
        "This paper makes five contributions.\n"
        "\\begin{itemize}\\setlength{\\itemsep}{1pt}\n"
        "\\item We define two pre-retrieval judgments about a memory store, FOK (coverage) and NOK (obligation), with an intent-conditional coverage label and a value-free lifecycle summary.\n"
        "\\item We build a counterfactual test in which one question is asked of three store versions differing in one attribute ($n=444$), so only the summary varies.\n"
        "\\item We show monitors read the summary's \\emph{names}, not its counts: the name lookup matches two of three models and none reads counted states until named.\n"
        "\\item We show that retrieval returning non-active records \\emph{with their tags} is a second route to the obligation, and no tested backend writes a usable list.\n"
        "\\item We show that gating retrieval on the judgment reaches more forbidding records but does not reduce stale answers; tagging the store's untagged duplicates does.\n"
        "\\end{itemize}\n"
        "\n" + fig1 + "\n")
    return t.replace(old, new)


# ---------------------------------------------------------------------------------------------------------------------------
# Section 3
# ---------------------------------------------------------------------------------------------------------------------------
def rewrite_S3(t):
    head = "\\section{Framework}\\label{sec:framework}\n"
    nxt = "\\section{Setup}\\label{sec:setup}\n"
    old = t[t.index(head):t.index(nxt)]
    def1 = block(old, "\\begin{definition}[Intent-conditional coverage]", "\\end{definition}\n")
    grid = block(old, "%% Writing pass Phase 3 (2026-09-15), items 20 and 94: Definition 1's cases as a grid", "\\end{center}\n")
    def2 = block(old, "\\begin{definition}[Lifecycle summary]", "\\end{definition}\n")
    box = block(old, "%% Writing pass Phase 3 (2026-09-15), item 17 with its addendum and item 23: the notation box", "\\end{minipage}}\n\\end{center}\n")
    listing = block(old, "\\begin{listing}[h]\n", "\\end{listing}\n")
    tuple_s = "Let a store $S$ be a finite set of items $e$ with content and metadata $m(e)=(c_e,\\kappa_e,\\xi_e,h_e,t_e)$: category, slot key (the attribute name), lifecycle state $\\xi_e\\in\\{\\textsc{active},\\textsc{superseded},\\textsc{expired},\\textsc{retracted}\\}$, optional event-time anchor, and ingest time \\citep{fr}.\n"
    state_s = "The lifecycle state is the tag a record carries, and the last three states are the non-active ones.\n"
    intent_s = "A query $q$ has intent $i(q)\\in\\{\\textsc{current},\\textsc{upcoming},\\textsc{past},\\textsc{change}\\}$, the time frame it asks about, because the same record can be licensed under one intent and forbidden under another.\n"
    prob_s = ("Both judgments are probabilities, scored by AUROC \\citep{hanley1982}.\n"
              "We elicit $\\mathrm{FOK}(q,S)\\in[0,1]$ as a probability that coverage is not \\absent{} and $\\mathrm{NOK}(q,S)\\in[0,1]$ as a probability that coverage is \\pn{}.\n"
              "A blind monitor sees only the question, so its AUROC measures what the question alone gives away, and an indexed monitor also sees the store's summary.\n")
    mask_s = "A retriever that masks non-active records from its ranking, as lifecycle-tracking and overwriting stores do, cannot supply the obligation judgment on its own.\n"
    for s in (tuple_s, state_s, intent_s, prob_s, mask_s):
        assert s in old, s[:60]
    new = (head + "\n"
        "%% Writing pass Phase 4b (2026-09-15): Section 3 written fresh from the author's skeleton (reviews/v18/tools/wp_phase4b.py). Both definitions, the grid\n"
        "%% and the box are carried verbatim from the Phase 4 build; Listing 1 moves to Appendix E.3 and Figure 2 to the head of Section 5.\n"
        "A store is a set of tagged records, and a question comes with an intent.\n"
        + tuple_s + state_s + intent_s + "\n"
        + def1 + "\n" + grid
        + prob_s + "\n"
        + def2
        + "A rendered summary is Listing~\\ref{lst:summary} in Appendix~\\ref{app:construction}; the count table is carried because it was part of the summary as fixed before the study.\n"
        + box + "\n"
        "%% The skeleton's third paragraph: the mask claim and Figure 1's no route. Item 19's sentence is gone; the two-store argument (\"ranks below $k$ common items\")\n"
        "%% is Phase 5's appendix item; item 14's framing sentence (\"the summary route is retrieval over a metadata index\") is dropped under the skeleton, reported.\n"
        + mask_s
        + "That is the crossed-out path of Figure~\\ref{fig:framework}, masked retrieval with no route.\n"
        "\n")
    t = t.replace(old, new)
    LISTING_OUT.append(listing)
    return t


LISTING_OUT: list[str] = []
FIG2_OUT: list[str] = []


# ---------------------------------------------------------------------------------------------------------------------------
# Section 4
# ---------------------------------------------------------------------------------------------------------------------------
def rewrite_S4(t):
    head = "\\section{Setup}\\label{sec:setup}\n"
    nxt = "\\section{The clean test: one question, three stores}\\label{sec:counterfactual}\n"
    old = t[t.index(head):t.index(nxt)]
    fig2 = block(old, "\\begin{figure}[t]\n\\centering\n%% R110: Figure 2, the worked example", "\\label{fig:example}\n\\end{figure}\n")
    tab1 = block(old, "\\begin{table}[h]\n%% Writing pass Phase 1 (2026-09-15), item 24: Table tab:populations", "\\end{table}\n")
    old_note = ("$^{a}$Three draws per question under each prompt on this set, one call on every other. GPT-4.1 mini is scored from one call in the main study and every other model from five. "
                "The finer resolution of the averaged scores is not their margin: Opus 5's first call alone keeps its margin over the name lookup on the counterfactual set. "
                "GPT-4.1 mini's repeated calls return identical scores on $46$ of $50$ questions (Appendix~\\ref{app:counterfactual}).\n")
    new_note = "$^{a}$Three draws per question under each prompt on this set, one call on every other; the score resolution of the one-call and five-call rows is in Appendix~\\ref{app:counterfactual}.\n"
    tab1 = rep(tab1, old_note, new_note)
    # the caption's manifest sentence now stands in the second paragraph, so the caption drops it (no number)
    tab1 = rep(tab1,
        "\\caption{The populations, with their sizes and positives and the models that ran on each (calls per question in parentheses). Every question set was generated from human-written manifests, which are the ground truth every label is scored against; Appendix~\\ref{app:laddertable} defines each population in full and records the runs.}\n",
        "\\caption{The populations, with their sizes and positives and the models that ran on each (calls per question in parentheses); Appendix~\\ref{app:laddertable} defines each population in full and records the runs.}\n")
    tab1 = rep(tab1, "%% The note carries the score-resolution paragraph (items 1 and 29; AUX-R110-A3, k3_noise 46 of 50).\n",
               "%% Phase 4b: the note keeps the draws (the author's skeleton); the score-resolution sentences stand in Appendix C.2 (AUX-R110-A3; k3_noise 46 of 50).\n")
    cap_s = ("A ground-truth summary is built from ground truth and a store-written summary from the fields the backend itself exposes, rendered by the same code with a cap of fifteen names per list.\n"
             "%% R110: the cap and its recorded reason; the sixty-percent line's provenance (A5_EDITS.md item 9; AUX-E1R-NB6 1.75; indexes_s2u.json meta 15.04).\n"
             "The cap, a rendering choice fixed before the pilot, never binds on the ground-truth summary, whose superseded list averages under two names.\n"
             "It binds on the store's own metadata, so the lifted rendering is reported beside the capped figure (Appendix~\\ref{app:repro}).\n")
    lookup_s = "The name lookup scores each question by its maximum cosine similarity, under the sentence encoder \\texttt{all-MiniLM-L6-v2}, to the names in the summary's superseded list.\n"
    interval_s = ("We report the item-level paired bootstrap interval first and the persona-grouped interval second, and where they disagree the wider decides.\n"
                  "We call a difference \\emph{reliable} when both intervals exclude zero, and \\emph{within tolerance} when $|\\Delta| \\le 0.05$.\n"
                  "On the counterfactual set the persona-grouped interval is the one printed, because resampling whole questions keeps each triple intact.\n")
    prereg_s = "Of the $58$ predictions preregistered before data collection, $16$ came out otherwise, and every preregistered text, prediction and outcome is in Appendix~\\ref{app:registration}.\n"
    label_s = "Labels follow Definition~\\ref{def:coverage}, and every \\pn{} label was verified by hand from the judgments that compose it.\n"
    presence_s = "A presence control confirms that each target is stored, so a mislabeled \\absent{} item is unlikely ($5.2\\%$ at the observed base rate; Appendix~\\ref{app:construction}).\n"
    table_s = "Table~\\ref{tab:setup} names every population with its size, its positives and the models that ran on it, and every later number is stated on one of them.\n"
    table_new = "Table~\\ref{tab:setup} names every population, and every later number is stated on one of them.\n"
    for s in (cap_s, lookup_s, interval_s, prereg_s, label_s, presence_s, table_s):
        assert s in old, s[:60]
    new = (head + "\n"
        "%% Writing pass Phase 4b (2026-09-15): Section 4 written fresh from the author's skeleton (reviews/v18/tools/wp_phase4b.py). Table 1 is carried with its\n"
        "%% note reduced to the draws; Figure 2's source moves to the head of Section 5. The 5% mask pass rate (Appendix E.9), the 5.2% presence bound (E.3),\n"
        "%% the 0.80 to 0.97 question probes (Appendix C) and the 58 / 16 predictions (Appendix F) are kept with their pointers.\n"
        "FR-Bank \\citep{fr} is the only backend that tags every entry with a lifecycle state.\n"
        "Its stock configuration masks non-active records from retrieval, and retraction records pass that mask at $5\\%$ (Appendix~\\ref{app:census}).\n"
        "Mem0 (\\texttt{mem0ai} 1.0.5) overwrites the record it exposes and A-MEM links notes \\citep{mem0,amem}; neither records lifecycle structure, so we call them the structureless backends.\n"
        "The models are OpenAI's GPT-4.1 mini, GPT-5.6 Luna and GPT-5.6 Sol, Anthropic's Haiku 4.5 and Opus 5, and Moonshot's Kimi K3 with open weights.\n"
        "GPT-4.1 mini ran the main study at one call per question, Opus 5, Haiku 4.5 and GPT-5.6 Luna ran every population at five, and GPT-5.6 Sol and Kimi K3 ran the cross-model set only (Table~\\ref{tab:setup}).\n"
        "\n"
        "Every question set was generated with large language models from human-written manifests, and the manifests are the ground truth every label is scored against.\n"
        + label_s + presence_s + table_new
        + "\n" + tab1 + "\n"
        + cap_s.replace("The cap, a rendering choice fixed before the pilot, never binds", "The cap, fixed before the pilot, never binds") + "\n"
        "The monitor returns a probability under a fixed rubric, and the two prompts differ only in whether the summary precedes the question, so the gain isolates the summary (Appendix~\\ref{app:construction}).\n"
        "The name lookup, the baseline every model is measured against, scores each question by its maximum cosine similarity under the sentence encoder \\texttt{all-MiniLM-L6-v2} to the names in the summary's superseded list (Appendix~\\ref{app:baselines}).\n"
        + interval_s
        + "Probes on the question text alone reach $0.80$ to $0.97$ (Appendix~\\ref{app:questionprior}), which is why we report paired gains and the counterfactual set.\n"
        "Of the $58$ predictions preregistered before data collection, $16$ came out otherwise (Appendix~\\ref{app:registration}).\n"
        + "\n")
    t = t.replace(old, new)
    # Figure 2 to the head of Section 5 (a transfer, counted there)
    fig2 = fig2.replace("\\begin{figure}[t]\n\\centering\n%% R110: Figure 2, the worked example",
                        "\\begin{figure}[t]\n\\centering\n%% Writing pass Phase 4b (2026-09-15): Figure 2's source at the head of Section 5, the section that reads the triples (the author's option).\n%% R110: Figure 2, the worked example")
    t = rep(t, nxt + "\n", nxt + "\n" + fig2 + "\n")
    return t


# ---------------------------------------------------------------------------------------------------------------------------
# the appendix: Listing 1 into E.3; the score-resolution sentence of Table 1's old note into C.2
# ---------------------------------------------------------------------------------------------------------------------------
def appendix_edits(listing):
    a = io.open(APPX, encoding="utf-8").read()
    lead = "This appendix carries the two user prompts, the obligation half of the rubric, and the construction record of the main study, because every reported estimate is bounded by one of them.\n"
    a = rep(a, lead, lead + "Listing~\\ref{lst:summary} is the abridged summary the indexed monitor sees, rendered from the store of one persona.\n"
            "\n%% Writing pass Phase 4b (2026-09-15): the example summary moved here from Section 3 (the author's skeleton, \"Listing N in App. E.3\"); the lines are those of the E.1 excerpt (AUX-R86-INDEX-EXCERPT).\n"
            + listing)
    old = "On the full obligation set the first draws read $0.8156$ (Haiku 4.5), $0.8335$ (Opus 5) and $0.8141$ (GPT-5.6 Luna) against averaged rows of $0.8210$, $0.8327$ and $0.8182$.\n"
    a = rep(a, old, old + "GPT-4.1 mini's repeated calls return identical scores on $46$ of $50$ questions.\n"
            "%% Phase 4b: the sentence of Table 1's old note (item 29; reviews/NUMBERS_R110.md, k3_noise; e1_metamemory/results/scores_e1.json).\n")
    io.open(APPX, "w", encoding="utf-8", newline="\n").write(a)


def main():
    upto = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--upto=")), "S4")
    r = subprocess.run([sys.executable, str(TOOLS / "wp_phase4.py"), "--step=3"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-800:]
    t = io.open(BODY, encoding="utf-8").read()
    done = ["phase 4"]
    # the placeins barrier: with [above] a float still pending at a section's barrier may sit above that section's heading on the same page, so
    # the barrier no longer forces a page break (Figure 2 at the head of Section 5 left twenty blank lines on page 6 under [section] alone)
    t = rep(t, "\\usepackage[section]{placeins}\n",
            "\\usepackage[section,above]{placeins}   % Phase 4b: a pending float may sit above the next heading on its page; the barrier forces no page break\n")
    done.append("placeins [above]")
    t = rewrite_S1(t); done.append("S1")
    if upto in ("S3", "S4"):
        t = rewrite_S3(t); done.append("S3")
        appendix_edits(LISTING_OUT[0]); done.append("E.3 listing, C.2 sentence")
    if upto == "S4":
        t = rewrite_S4(t); done.append("S4 (Figure 2 to Section 5)")
    io.open(BODY, "w", encoding="utf-8", newline="\n").write(t)
    print("wp_phase4b: " + ", ".join(done))


if __name__ == "__main__":
    main()
