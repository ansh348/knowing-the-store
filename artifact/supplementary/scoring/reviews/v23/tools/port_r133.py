# -*- coding: utf-8 -*-
"""port_r133.py -- the R133 readability pass (2026-09-21; the author's brief 'R133: V23 READABILITY PASS') applied to the v23 sources, unit by unit,
on a fresh copy of the v22 close's sources (bump_v23.py --refresh). Every edit is an asserted replacement (the old text must occur exactly the stated
number of times), so a unit that no longer matches its base stops the run instead of drifting. Units, cumulative in the brief's order (section 8):

  homes   the coverage homes (section 4): the dagger notes under Appendix A's run-coverage table; Table 74's stale first row corrected (0.76 to 0.85)
  swaps   the author's verbatim swaps S1 to S11 (section 5), the S9 mode labels in Table 2 and Appendix E.9, the S11 identifiers
  s4      Section 4 rewritten from its second paragraph (sections 4.2, 6)
  s51     Section 5.1 rewritten (section 6; the worked example of section 7)
  s52     Section 5.2 rewritten (section 6; the worked example of section 7)
  s53     Section 5.3 rewritten (section 6; S10)
  s6      Section 6 rewritten
  s7      Section 7 rewritten
  s8      Section 8 rewritten
  s12     the optional Limitations sentence (S12; only if the final slack is +3 or better)
  rulings the author's R133 RULINGS of 2026-09-21 (1, 3, 5)

Every replacement is logged to reviews/v23/results/port_r133_log.json (unit, file, section, old, new) for OLD_BESIDE_NEW_V23.md (changes_r133.py).
Usage: python reviews/v23/tools/port_r133.py --units=homes,swaps,...   [--no-refresh]   (--units=all applies every unit but s12 and rulings; --units=close applies every unit)
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
V23 = ROOT / "reviews" / "v23"
SRC = V23 / "src"
BODY, ABS, APPX = SRC / "body_v23.tex", SRC / "abstract_v23.tex", SRC / "appendix_v23.tex"
LOG = V23 / "results" / "port_r133_log.json"
ORDER = ["homes", "swaps", "s4", "s51", "s52", "s53", "s6", "s7", "s8", "s12", "rulings"]

TEXT = {}
LOGGED = []


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def wr(p, t):
    p.write_text(t, encoding="utf-8", newline="\n")


def rep(which, old, new, n=1, unit="", section="", note=""):
    """Replace old by new in the named file exactly n times; log the pair."""
    t = TEXT[which]
    c = t.count(old)
    assert c == n, f"[{unit}] {which}: expected {n} occurrence(s), found {c} of: {old[:90]!r}"
    TEXT[which] = t.replace(old, new)
    LOGGED.append(dict(unit=unit, file=which, section=section, old=old, new=new, note=note))


def ins_after(which, anchor, new, unit="", section="", note=""):
    t = TEXT[which]
    assert t.count(anchor) == 1, f"[{unit}] {which}: anchor not unique: {anchor[:90]!r}"
    TEXT[which] = t.replace(anchor, anchor + new)
    LOGGED.append(dict(unit=unit, file=which, section=section, old="", new=new, note=note))


# ====================================================================================================================== homes
def unit_homes():
    u = "homes"
    # (a) Appendix A: the coverage notes the daggers resolve to (section 4.3), after tab:runs and before the two sentences R109 moved from Section 8.
    anchor = "\\end{tabular}\n\\end{table}\n% R109: two sentences moved verbatim from Section 8 (page-9 gate).\n"
    note = ("%% R133 (2026-09-21), the coverage notes: each dagger in the main text resolves to one item here (the author's brief, sections 4.1 and 4.3); the facts are\n"
            "%% those of tab:runs, tab:setup and the tables named, restated in one place.\n"
            "\\paragraph{Coverage notes for the daggers in the main text.}\n"
            "A dagger on a number in the main text marks a run setting that differs from its neighbours in the same sentence, or a comparison set that is incomplete; each resolves to one note here.\n"
            "(i) Section~\\ref{sec:names_counts}, the count-removal result for GPT-4.1 mini: the names-and-counts ablation ran on its one-call row at temperature $0$ (Table~\\ref{tab:cf-names-counts}); its five-draw row of Table~\\ref{tab:cf-main} was not rerun under the ablation.\n"
            "(ii) Section~\\ref{sec:names_counts}, the count-removal result for the stronger models: GPT-5.6 Luna at five draws through the raw API and Opus 5 at one draw; GPT-5.6 Sol was not run, dropped by the registration's budget rule (Table~\\ref{tab:cf-nc-strong}).\n"
            "(iii) Section~\\ref{sec:lookup}, the summary naming all states: GPT-4.1 mini, Haiku 4.5 and Opus 5 ran it; GPT-5.6 Luna and GPT-5.6 Sol ran the default summary only (Table~\\ref{tab:cf-matched}).\n"
            "(iv) Section~\\ref{sec:intent}, the intent crossover: GPT-4.1 mini, Opus 5 and GPT-5.6 Sol ran one draw and Haiku 4.5 and GPT-5.6 Luna five, the body reading their draw-1 column; Sol was added after an interim read of three models' rows (Table~\\ref{tab:cf-intent}).\n"
            "(v) Section~\\ref{sec:populations}, the full obligation set: Haiku 4.5, GPT-5.6 Luna and Opus 5 completed it; the GPT-5.6 Sol and Kimi K3 runs stopped at the budget and are not scored as sets (Table~\\ref{tab:x4-expansion}).\n"
            "\n")
    t = TEXT["appendix"]
    assert t.count(anchor) == 1
    TEXT["appendix"] = t.replace(anchor, anchor.replace("% R109:", note + "% R109:"))
    LOGGED.append(dict(unit=u, file="appendix", section="A", old="", new=note, note="section 4.1/4.3: the coverage notes; the facts of tab:runs, tab:setup, tab:cf-names-counts, tab:cf-nc-strong, tab:cf-matched, tab:cf-intent, tab:x4-expansion restated"))
    # (b) Table 74 (tab:provenance), row 1: the models' range against Table 1 as built (r133_number_gate.py: MINI5 0.7648, H45 0.7566, LUNA 0.8417, SOL 0.8500, OP5 0.8405).
    rep("appendix", "Counterfactual NOK AUROC, lookup $0.77$ and models $0.72$ to $0.84$ (Section~\\ref{sec:counterfactual}, Table~\\ref{tab:cf-main})",
        "Counterfactual NOK AUROC, lookup $0.77$ and models $0.76$ to $0.85$ (Section~\\ref{sec:counterfactual}, Table~\\ref{tab:cf-main})",
        unit=u, section="E.12", note="section 4.4: the stale range (0.72 was mini's one-draw row; 0.84 omitted Sol's 0.85) corrected from r125_matched.json readers/*/gate through r133_number_gate.py")


# ====================================================================================================================== swaps
def unit_swaps():
    """Section 5 of the brief: the author's verbatim swaps S1 to S11 (numbers verified by r133_number_gate.py before writing)."""
    u = "swaps"
    # S1 (the abstract)
    rep("abstract", "First, ablations show that the two smaller of five models rely on the attribute names alone, while the three stronger ones also use the state counts.",
        "First, ablations show that the two smaller of five models score the same with the state counts removed, while the three stronger ones also use them.",
        unit=u, section="Abstract", note="S1")
    # S2 (the abstract)
    rep("abstract", "which the summary only counts; adding one count feature to the lookup closes it.\n",
        "which the summary only counts.\nAdding one count feature to the lookup closes that lead when a question's three store versions are compared with each other, but not when all items are pooled, where the models stay $0.05$ to $0.06$ ahead.\n",
        unit=u, section="Abstract", note="S2 (0.05 to 0.06: AUX-CF2-HYB-VS-MODELS, each reliable)")
    # S3 (the abstract): the two sentences from 'Given only what FR-Bank' to 'which model read it.'
    rep("abstract", "Given only what FR-Bank, a backend that tags every entry with a lifecycle state, actually writes, GPT-4.1 mini and the lookup drop from $0.73$ and $0.75$ to $0.60$ and $0.59$ on our larger question set.\n"
        "In these tests, what the store wrote down mattered more than which model read it.\n",
        "Given only what FR-Bank, a backend that tags every entry with a lifecycle state, actually writes, GPT-4.1 mini, Haiku 4.5 and the lookup drop from $0.73$, $0.82$ and $0.75$ to $0.60$, $0.71$ and $0.59$ on our larger question set.\n"
        "In these tests, what the store wrote down limited every reader we gave it to.\n",
        unit=u, section="Abstract", note="S3 (Haiku 0.82 / 0.71: AUX-R74-X4-H45-NOK, AUX-BH-H45-15; same population and conditions as mini's and the lookup's pair)")
    # S4 (Section 1)
    rep("body", "In these tests, what the store writes down mattered more than which reader read it.\n",
        "In these tests, what the store wrote down limited every reader we gave it to.\n", unit=u, section="1", note="S4")
    # S5 (Section 1, the second and third bullets)
    rep("body", "The two smaller models use only the names and three stronger models also use the counts;",
        "The two smaller models score the same with the counts removed and three stronger models also use the counts;", unit=u, section="1", note="S5")
    rep("body", "and a lookup with one count feature matches the stronger models within triples.",
        "and a lookup with one count feature matches the stronger models within triples, though not on the pooled metric.", unit=u, section="1", note="S5")
    rep("body", "Under FR-Bank's own metadata mini and the lookup fall to $0.60$ and $0.59$,",
        "Under FR-Bank's own metadata mini, Haiku and the lookup fall to $0.60$, $0.71$ and $0.59$,", unit=u, section="1", note="S5 (Haiku 0.71: AUX-BH-H45-15)")
    # S6 (the Conclusion)
    rep("body", "In these tests, the information a store wrote down counted for more than the choice of reader. The smaller models read only the names; the stronger ones also read the counts, and a lookup given one count feature matches them within triples.",
        "In these tests, what a store wrote down limited every reader we gave it to. The smaller models score the same with the counts removed; the stronger ones also read the counts, and a lookup given one count feature matches them within triples, though not on the pooled metric.",
        unit=u, section="10", note="S6")
    # S7 (Section 5's bold leads and the 'level with' clause)
    rep("body", "\\claim{The two smaller models read only the names.}", "\\claim{The two smaller models lose nothing when the counts are removed.}", unit=u, section="5.1", note="S7")
    rep("body", "\\claim{The stronger models' lead comes from counts, and a count feature closes it.}", "\\claim{The stronger models' lead comes from counts, and a count feature closes it within a question.}", unit=u, section="5.2", note="S7")
    rep("body", "\\claim{Naming all states lifts every reader.}", "\\claim{Naming all states lifts every reader that ran it.}", unit=u, section="5.2", note="S7")
    rep("body", "scores $0.89$: reliably above the lookup and level with the three models.",
        "scores $0.89$, reliably above the lookup, beside the three models' $0.86$ to $0.88$; we ran no equivalence test.",
        unit=u, section="5.2", note="S7 (the three models' matched values 0.8784, 0.8581, 0.8750 beside the reader's 0.8851)")
    # S8 (Section 4)
    rep("body", "A difference is \\emph{reliable} when both the item-level paired and persona-grouped bootstrap intervals exclude zero.",
        "A difference is \\emph{reliable} when both the item-level paired and persona-grouped bootstrap intervals exclude zero. We apply no multiplicity correction, so reliable describes each comparison on its own.",
        unit=u, section="4", note="S8")
    # S9 (Table 2's FR-Bank cell and the three mode labels; the appendix sentences that name the modes)
    rep("body", "against ${\\sim}102$ in ground truth (about $58\\times$)", "against ${\\sim}102$ in the reference (about $58\\times$)", unit=u, section="6 (Table 2)", note="S9")
    rep("body", "FR-Bank & Overstate &", "FR-Bank & Over-mark &", unit=u, section="6 (Table 2)", note="S9")
    rep("body", "Mem0 & Erase &", "Mem0 & Overwrite &", unit=u, section="6 (Table 2)", note="S9")
    rep("body", "A-MEM & Invent &", "A-MEM & Unresolved links &", unit=u, section="6 (Table 2)", note="S9")
    rep("appendix", "carries the census behind the overstate, erase and invent reading.", "carries the census behind the over-mark, overwrite and unresolved-links reading.", unit=u, section="E.9", note="S9")
    rep("appendix", "so the erase reading is of the record as exposed", "so the overwrite reading is of the record as exposed", unit=u, section="E.9", note="S9")
    rep("appendix", "The failure mode is erasure with overstatement in what survives,", "The failure mode is loss of content with over-marking in what survives,", unit=u, section="E.9", note="S9 (the Graphiti sentence's descriptive use of the old labels; listed for a ruling)")
    # S10 (Section 5.3): the rubric point explicit in one sentence
    rep("body", "Those models score the change question higher, consistent with a scored step that asks whether stale content exists.",
        "Those models score the change question higher. The main-study rubric's scored step asks whether stale content is present, which is not the intent-conditional target of Definition~\\ref{def:coverage}; the explicit-intent rubric asks the defined question.",
        unit=u, section="5.3", note="S10")
    # S11 (the appendix): the internal identifiers in the built PDF
    rep("appendix", "(the artifact's R108 ledger)", "(the artifact's mechanism-score ledger)", unit=u, section="E.5", note="S11")
    rep("appendix", "five recorded deviations (D-CF2-1 to D-CF2-5)", "five recorded deviations", unit=u, section="F", note="S11")
    rep("appendix", "one prediction unfulfillable by its own gate (D-DS-3)", "one prediction unfulfillable by its own gate, recorded as a deviation", unit=u, section="F", note="S11")


def rep_para(which, prefix, new, unit="", section="", note=""):
    """Replace the whole source paragraph that starts with prefix (unique) and ends at the next blank line; comment lines inside it are kept in front."""
    t = TEXT[which]
    assert t.count("\n" + prefix) == 1, f"[{unit}] {which}: paragraph prefix not unique: {prefix[:80]!r} ({t.count(chr(10) + prefix)})"
    i = t.index("\n" + prefix) + 1
    j = t.index("\n\n", i)
    old = t[i:j]
    TEXT[which] = t[:i] + new.rstrip("\n") + t[j:]
    LOGGED.append(dict(unit=unit, file=which, section=section, old=old, new=new.rstrip("\n"), note=note))


def del_para(which, prefix, unit="", section="", note=""):
    """Delete the whole source paragraph that starts with prefix (unique), with the blank line after it."""
    t = TEXT[which]
    assert t.count("\n" + prefix) == 1, f"[{unit}] {which}: paragraph prefix not unique: {prefix[:80]!r}"
    i = t.index("\n" + prefix) + 1
    j = t.index("\n\n", i) + 2
    old = t[i:j - 2]
    TEXT[which] = t[:i] + t[j:]
    LOGGED.append(dict(unit=unit, file=which, section=section, old=old, new="", note=note))


DRAWS_SENTENCE = "Every model row in Table~\\ref{tab:cf-main} averages five draws. "


# ====================================================================================================================== s4
def unit_s4():
    """Section 4 from its second paragraph (the brief, sections 4.2 and 6)."""
    u = "s4"
    caption = "--draws-caption" in sys.argv   # section 4.2: the five-draw sentence into Table 1's caption if it costs no line there
    rep_para("body", "The models are GPT-4.1 mini, Haiku 4.5, GPT-5.6 Luna, GPT-5.6 Sol and Opus 5, abbreviated",
             "The models are GPT-4.1 mini, Haiku 4.5, GPT-5.6 Luna, GPT-5.6 Sol and Opus 5, abbreviated mini, Haiku, Luna, Sol and Opus in that order, and Kimi K3 (open weights) joins the cross-vendor comparison. "
             + ("" if caption else DRAWS_SENTENCE) +
             "Not every reader ran every condition, and run settings differ across rows; Appendix~\\ref{app:laddertable} lists both, and a dagger marks a number in the text that has a coverage note there.\n",
             unit=u, section="4", note="section 4.2: the five models and their short names; Kimi K3 (open weights); the five-draw sentence" + (" (in Table 1's caption)" if caption else "") + "; the one coverage sentence. H03 to H09 leave (tab:runs; the coverage notes)")
    if caption:
        rep("body", "Question-only AUROC is $0.50$. Differences at four decimals.", "Question-only AUROC is $0.50$. Every model row averages five draws. Differences at four decimals.",
            unit=u, section="5.1 (Table 1)", note="section 4.2: the five-draw sentence in Table 1's caption (it cost no line there)")
    rep_para("body", "The personas, their human-written manifests and sessions,",
             "The personas, their human-written manifests and sessions, the FR-Bank, Mem0 and A-MEM stores and part of the main question set come from the FR-Bank release \\citep{fr}. Language models drafted our other questions, and we built the Graphiti graphs from the released FR-Bank records, with lifecycle fields removed. Those manifests provide the labels, with every \\pn{} label checked by hand, and a presence control checks that targets are stored. Intent is fixed by question construction and is not supplied as a label to the reader. (Appendix~\\ref{app:construction})\n",
             unit=u, section="4", note="the provenance sentences verbatim (R131 A1'); H12 (the 5.2% residual) leaves for Appendix E.3, where it is stated; one pointer")
    rep_para("body", "A \\emph{ground-truth summary} uses the manifest-based ground truth;",
             "A \\emph{ground-truth summary} uses the manifest-based ground truth; a \\emph{store-written summary} uses fields the backend exposes. The same renderer caps each list at fifteen names, a cap that binds only on store-written lists, which Section~\\ref{sec:backends} reports capped and uncapped. For Mem0 and A-MEM we also render the manifest under each backend's constraints; this constrained rendering is ours and differs from a summary built from their own fields. (Appendix~\\ref{app:inversion})\n",
             unit=u, section="4", note="H13 in one sentence (section 3.1); H14 kept, 'is ours' said")
    rep_para("body", "The \\emph{counterfactual set} asks each of its questions of three versions of one store.",
             "The \\emph{counterfactual set} asks each of its questions of three versions of one store. It contains $444$ items from $148$ questions, and the versions differ only in the target attribute. Questions are written before any version exists, so wording cannot predict which version carries the obligation; Figure~\\ref{fig:example} shows the Carnival example. The \\emph{full obligation set}, $661$ questions about the original stores and their variants, supports the backend and retrieval comparisons.\n",
             unit=u, section="4", note="the two population paragraphs joined; words unchanged but for the join")
    del_para("body", "The \\emph{full obligation set} supports the backend and retrieval comparisons.", unit=u, section="4", note="joined into the paragraph above")
    rep_para("body", "Readers return probabilities under a fixed rubric.",
             "Readers return probabilities under a fixed rubric. A \\emph{question-only} prompt omits the summary; a prompt \\emph{with the summary} adds only that text. The \\emph{name lookup} scores the largest cosine similarity between the question and a name on the superseded list, computed by a small sentence encoder, and makes no generative-model call. Under the summary naming all states, the same lookup reads all non-active names. (Appendix~\\ref{app:baselines})\n",
             unit=u, section="4", note="H16: the encoder's name leaves for Appendix C.2 (tab:enc-lookup) and F, where it is stated")
    rep_para("body", "We score separation by AUROC, the chance that a positive scores above a negative",
             "We score separation by AUROC, the chance that a positive scores above a negative \\citep{hanley1982}. Chance is $0.50$. The pooled AUROC over all items was fixed in advance. Because the counterfactual set fixes the question, we also report the matched AUROC, the share of triples in which the \\pn{} version outscores the \\present{} version, ties counting half. It is post hoc, and we say where the two metrics disagree. A difference is \\emph{reliable} when both the item-level paired and persona-grouped bootstrap intervals exclude zero. We apply no multiplicity correction, so reliable describes each comparison on its own. \\emph{Within tolerance} means an absolute difference no greater than $0.05$. A gain compares the same questions with and without the summary.\n",
             unit=u, section="4", note="section 6.6: the gate-forced 'The metric fixed in advance pools all items.' undone to 'The pooled AUROC over all items was fixed in advance.' (rule V bars 'preregistered'; 'fixed in advance' is not barred); S8 kept")


# ====================================================================================================================== s51
def unit_s51():
    u = "s51"
    rep_para("body", "\\claim{Within a triple, a name or a count can identify the obligation.}",
             "\\claim{Within a triple, a name or a count can identify the obligation.}\n"
             "The \\pn{} version differs from its siblings in one attribute, so its category holds one more non-active record. A privileged count reader, handed the question's category that the models must infer, wins every retraction and expiry triple, and the name lookup wins $82$ of the $88$ supersession triples and loses none. For $26$ of $30$ retraction pairs and $15$ of $30$ expiry pairs that count starts at zero, so a reader can identify the store version without identifying the attribute. What differs across readers is which of the two they use.\n",
             unit=u, section="5.1", note="the 36-word sentence split; H25 kept as 'a privileged count reader'; the pointer moves to the subsection's end")
    rep_para("body", "\\claim{The two smaller models lose nothing when the counts are removed.}",
             "\\claim{The two smaller models lose nothing when the counts are removed.}\n"
             "With every count deleted, mini$^{\\dagger}$ and Haiku stay within $0.01$ of their intact-summary scores; given the counts alone, they fall by $0.14$. Told that one more plan was cancelled without being told which, they cannot use it: on retraction and expiry both stay reliably below a count reader that merely guesses the category.\n",
             unit=u, section="5.1", note="the brief's worked example (section 7), 'but not which' reworded for slogan_scan S9; H28 (mini's single-call row) to the dagger's note (i); H29 (the pooled 0.12 and 0.16) and H30 (the count reader's 0.77 and 0.75) to tab:cf-names-counts and tab:cf-matched")
    rep_para("body", "\\claim{The three stronger models also read the counts.}",
             "\\claim{The three stronger models also read the counts.}\n"
             "On retraction and expiry, which the default summary only counts, none of Luna, Sol and Opus sits reliably below the guessing count reader (Figure~\\ref{fig:perstate}). When the obligation's extra count moves to a sibling version with the names unchanged, all three follow it, falling by $0.27$ to $0.33$ on the counted states, while mini and Haiku show no reliable change. The falls are reliable on the matched metric and, pooled, on expiry for all three and on retraction for Opus alone. Removing every count costs Luna $0.06$ and Opus $0.04^{\\dagger}$ on the pooled metric, and the counts alone still score below the names alone for both; all four differences are reliable. Cancelling the hike changes only a count in the default summary, and these three readers follow it. (Appendix~\\ref{app:counterfactual})\n",
             unit=u, section="5.1", note="the per-state matched values (0.58 to 0.87) are Figure 3's; the four moved-count falls as one range; H37 (Sol not run) to the dagger's note (ii); the hike carried")


# ====================================================================================================================== s52
def unit_s52():
    u = "s52"
    rep_para("body", "\\claim{On the named state, no model reliably beats the lookup.}",
             "\\claim{On the named state, no model reliably beats the lookup.}\n"
             "Readers are compared within each triple on the matched metric, the pooled metric named where the two disagree. The default summary names only supersession; on its triples the lookup scores $0.97$, Opus is $0.01$ above it, Luna and Sol $0.01$ below, and only mini reliably below. A sibling-name control removes list length and counts with a fourth store version listing a different attribute of the same category, with the same counts and as many names. The lookup and every model pick the \\pn{} version over it at $0.88$ or higher, none reliably above the lookup, while meaningless tokens and the count reader sit near chance.\n",
             unit=u, section="5.2", note="section 6.5: the pooled and matched split stated once at the top; H41 (0.47 and 0.50) to tab:cf-sibling; mini's 0.07 left (the reliability is the point)")
    rep_para("body", "\\claim{The stronger models' lead comes from counts, and a count feature closes it within a question.}",
             "\\claim{The stronger models' lead comes from counts, and a count feature closes it within a question.}\n"
             "Across all $148$ triples Luna, Sol and Opus score a reliable $0.08$ to $0.10$ above the lookup. All of that comes from retraction and expiry, where the summary lists no name and the lookup ties every triple. It cannot tell the cancelled hike from the planned one. A lookup given one more feature, the guessed category's share of non-active records, scores $0.89$ beside the three models' $0.86$ to $0.88$; we ran no equivalence test. Pooled across questions the gap remains: the same reader scores $0.79$ and the models stay a reliable $0.05$ to $0.06$ above it (Table~\\ref{tab:cf-main}). Their scores stay comparable from one question to the next and the fitted reader's do not.\n",
             unit=u, section="5.2", note="the brief's worked example (section 7), its two long sentences split at 35 words; H42 (0.07 to 0.08 pooled) to tab:counterfactual; H44 (fit with personas left out) to Table 1's note b; the hike carried")
    rep_para("body", "\\claim{Naming all states lifts every reader that ran it.}",
             "\\claim{Naming all states lifts every reader that ran it.}\n"
             "With the retracted and expired attributes listed too, every reader that ran the summary rises (Table~\\ref{tab:cf-main}), Haiku by a reliable $0.35^{\\dagger}$ on the two states that were only counted. Opus's $0.03$ lead over the all-states lookup is reliable on the pooled metric and not on the matched one, so with every state named no model is reliably ahead on both.\n",
             unit=u, section="5.2", note="0.91 and 0.94 are Table 1's; H50 (Luna and Sol did not run) to the dagger's note (iii) and the lead's 'that ran it'")
    rep_para("body", "\\claim{List length and coverage lift both metrics.}",
             "\\claim{List length and coverage lift both metrics.}\n"
             "A reader that only knows whether the store covers the question ties every triple and still scores $0.75$ pooled, and the name lookup stays a reliable $0.13$ above a lookup over meaningless tokens within triples.\n",
             unit=u, section="5.2", note="'0.50 matched' said as 'ties every triple' (0/148/0); one sentence")
    rep_para("body", "\\claim{Long or wrong name lists weaken the readers together.}",
             "\\claim{Long or wrong name lists weaken the readers together.}\n"
             "Padding the default list to $60$ names lowers the lookup to $0.67$ on the full obligation set, and injected wrong names lower mini, Haiku and the lookup together. Short ground-truth lists therefore do not establish robustness to longer store-written ones. (Appendix~\\ref{app:counterfactual})\n",
             unit=u, section="5.2", note="the 40-word sentence split; one pointer at the subsection's end")


# ====================================================================================================================== s53
def unit_s53():
    u = "s53"
    rep_para("body", "\\claim{The stated intent rule separates the readers.}",
             "\\claim{The stated intent rule separates the stronger readers.}\n"
             "The supersession crossover holds the store fixed and changes the question from the current value to how it changed, using the default summary; the change question licenses the old content. When the rubric states that rule, Luna, Sol and Opus score $0.88$ to $0.99^{\\dagger}$, while mini and Haiku, told the same rule, score $0.48$ and $0.55$. A fixed cue list matches the best model, so the test shows rule-following on cued questions and no general model advantage over deterministic intent handling.\n",
             unit=u, section="5.3", note="the first two paragraphs joined (the lead scoped to the stronger readers); the cue list's 0.99 is tab:cf-intent's; H61 to the dagger's note (iv)")
    del_para("body", "\\claim{Mini and Haiku struggle even when told the rule.}", unit=u, section="5.3", note="joined into the paragraph above")
    rep_para("body", "\\claim{Only Opus lowers its judgment without being told.}",
             "\\claim{Only Opus lowers its judgment without being told.}\n"
             "Under the main-study rubric, mini, Haiku, Luna and Sol score $0.35$ to $0.44$ on the same contrast, against Opus's $0.90$. Those models score the change question higher. The main-study rubric's scored step asks whether stale content is present, which is not the intent-conditional target of Definition~\\ref{def:coverage}; the explicit-intent rubric asks the defined question. Opus's behaviour under this underspecified prompt differs from compliance with the explicit rule.\n",
             unit=u, section="5.3", note="S10 kept verbatim")
    rep_para("body", "\\claim{The explicit rule also separates readers on expired events.}",
             "\\claim{The explicit rule also separates readers on expired events.}\n"
             "The expiry crossover uses the summary naming all states; its past-event question licenses the record forbidden by the upcoming-event question. Under the explicit rule Luna, Sol and Opus score $0.92$ to $1.00$ and mini and Haiku do not separate the intents; Sol also separates them under the main-study rubric, at $0.64$. (Appendix~\\ref{app:counterfactual})\n",
             unit=u, section="5.3", note="three values as one range; one pointer at the subsection's end")


# ====================================================================================================================== s6
def unit_s6():
    u = "s6"
    rep_para("body", "\\claim{Backends omit or misstate the lifecycle information readers need.}",
             "\\claim{Backends omit or misstate the lifecycle information readers need.}\n"
             "FR-Bank marks far more entries stale than the reference does, yet retains obsolete assertions as active and conflates retraction with supersession. Mem0 overwrites at the retrieval surface we evaluated, and A-MEM's links resolve to no note in our integration (Table~\\ref{tab:census}).\n",
             unit=u, section="6", note="'about 58 times' is Table 2's; the pointer moves to the FR-Bank paragraph")
    rep_para("body", "\\claim{FR-Bank's metadata leave mini and the lookup near chance.}",
             "\\claim{FR-Bank's metadata leave mini and the lookup near chance.}\n"
             "Given only what the store wrote, its capped summary on the full obligation set leaves mini at $0.60$ and the lookup at $0.59$. Haiku, at $0.71$, keeps more of its gain. Lifting the cap raises all three without restoring their ground-truth scores. The loss is no artifact of the obligations the alignment misses: on the ones it marks, the capped summary still costs each reader a reliable $0.13$ to $0.20$. The cancelled hike is only as findable as the store's own marks make it. (Appendix~\\ref{app:census})\n",
             unit=u, section="6", note="H66, H67 kept; the three costs as one range and the 82 left to tab:levels-strata; the hike carried")
    rep_para("body", "\\claim{Graphiti writes part of what the judgment needs, and part of its loss is extraction.}",
             "\\claim{Graphiti writes part of what the judgment needs, and part of its loss is extraction.}\n"
             "Of the $34$ full-store obligations it could express, its invalidation marks $13$, and $11$ were never extracted into the graph. Retraction is inexpressible under this backend's mapping. On the $23$ obligations whose content the graph retains, mini's capped store-written score of $0.69$ against $0.84$ under ground truth is still a reliable loss. (Appendix~\\ref{app:posthoc-graphiti})\n",
             unit=u, section="6", note="H68 and H70 kept; H69 (all 47: 0.58 against 0.74; the store's lookup 0.68) to Appendix G.4")
    rep_para("body", "\\claim{Mem0 and A-MEM lose coverage when their summaries lose names.}",
             "\\claim{Mem0 and A-MEM lose coverage when their summaries lose names.}\n"
             "Under the constrained rendering mini loses coverage on both stores and Luna and Sol lose on the questions pooled across them, each loss reliable (Table~\\ref{tab:census}). Omitting or rewording the unavailable-field marker does not remove the Mem0 loss, and Luna loses $0.27$ to $0.34$ under every rendering tested through the raw API. Scores collapse onto a few low values, with positives slightly below negatives, and the trigger remains unresolved. Store-written summaries remain within tolerance of question only, and rebuilding name-bearing summaries from ground truth restores mini's coverage on both stores (Table~\\ref{tab:census}). (Appendix~\\ref{app:inversion})\n",
             unit=u, section="6", note="H71 and H75 (Table 2's 0.10, 0.11, 0.88, 0.90) not repeated; H73 (U5 and its four conditions) verbatim")


# ====================================================================================================================== s7
def unit_s7():
    u = "s7"
    rep_para("body", "\\claim{The tagged view complements the summary for mini.}",
             "\\claim{The tagged view complements the summary for mini.}\n"
             "FR-Bank's cosine search returns records without a lifecycle mask on the full obligation set. Mini scores $0.73$ with the default summary, $0.69$ with the retrieved records and their ground-truth tags, and $0.83$ with both, a reliable gain over the summary alone. The two routes mirror each other by state: the view helps mini on expiry, where the summary only counts, and hurts it on supersession, where the summary names, both effects reliable. Haiku's score with both stays within tolerance of its summary alone.\n",
             unit=u, section="7", note="the per-state magnitudes (0.24, 0.17) leave the prose; they have no appendix row (AUX-RESP-L2-MINI-NOK), listed in the report")
    rep_para("body", "\\claim{FR-Bank's own tags help mini despite over-marking.}",
             "\\claim{FR-Bank's own tags help mini despite over-marking.}\n"
             "With the store's native tags in place of the ground-truth ones, mini's view-only score rises reliably to $0.81$. Their precision over retrieved lines is only $0.14$, and the rise comes from their marking more of the forbidding records already in view. A reader that merely counts tagged lines scores $0.62$ under either tag source. On Graphiti, native tags on the same retrieved edges bring no reliable improvement. (Appendix~\\ref{app:posthoc-graphiti})\n",
             unit=u, section="7", note="0.69 said once (the paragraph above); H78, H79, H80 kept")
    rep_para("body", "\\claim{The lifecycle fetch supplies the added reach, gated or not.}",
             "\\claim{The lifecycle fetch supplies the added reach, gated or not.}\n"
             "The fetch adds the store's non-active records for an attribute matched to the default name list. It raises reach from $0.52$ to $0.82$, the always-on fetch reaching as far as the model-gated one at the matched budget, and the name-lookup rule reaches the same level (Table~\\ref{tab:reach}).\n",
             unit=u, section="7", note="joined; the pointer moves to the section's end")
    rep_para("body", "\\claim{Gating trades budget against licensed-record reach.}",
             "\\claim{Gating trades budget against licensed-record reach.}\n"
             "Unmatched, the always-on fetch spends $1.20$ times the lines per question; truncated to the gated budget it loses licensed records, a reliable $0.04$.\n",
             unit=u, section="7", note="the author's paragraph (R131 H1); the pointer moves to the section's end")
    rep_para("body", "\\claim{Keeping the newest record misses every tested retraction obligation.}",
             "\\claim{Keeping the newest record misses every tested retraction obligation.}\n"
             "At the matched budget, newest-per-attribute retrieval reaches none of the $26$ retraction obligations (Table~\\ref{tab:reach}). The cancelled hike shows why: its cancellation is not the newest record of the attribute it cancels.\n",
             unit=u, section="7", note="0.23 is Table 3's; the hike carried")
    rep_para("body", "\\claim{Active copies complicate the use of tagged records.}",
             "\\claim{Active copies complicate the use of tagged records.}\n"
             "Among $89$ scorable obligation views, $35$ contain an active line asserting the stale value. The flagged stale answers trace to these untagged copies even when the forbidding record is present and tagged. An intervention that tags the copies uses the obligations' reference information, so it diagnoses a source of stale use rather than supplying a deployable repair.\n",
             unit=u, section="7", note="H84 (34 once the inverted tag is corrected) to Appendix E.10's paragraph; H85 kept")
    rep_para("body", "\\claim{The tested rule cannot repair copies under different attribute keys.}",
             "\\claim{The tested rule cannot repair copies under different attribute keys.}\n"
             "Propagating a lifecycle tag to matching lines under the same attribute changes $1$ of $452$ assembled views. But $187$ of $272$ audited stale lines sit under a different attribute key from their tagged twin, which leaves the write path. A reference-free repair for copies under other keys remains open. (Appendix~\\ref{app:resp})\n",
             unit=u, section="7", note="one pointer at the section's end")


# ====================================================================================================================== s8
def unit_s8():
    u = "s8"
    rep_para("body", "\\claim{The summary's obligation benefit replicates across vendors.}",
             "The summary's obligation benefit replicates across vendors. On the shared cross-vendor questions, every model whose question-only score varies gains a reliable $0.15$ to $0.45$ with the summary, Kimi included. (Appendix~\\ref{app:laddertable})\n",
             unit=u, section="8", note="section 6.3: two paragraphs, so no bold leads; H87 kept")
    rep_para("body", "\\claim{Full-set models do not reliably beat the lookup.}",
             "On the full obligation set, no completed model reliably beats the lookup. Haiku, Luna and Opus score $0.82$ to $0.83^{\\dagger}$ against the lookup's $0.75$, but their margins fail the persona-grouped interval. On the easier coverage questions, mini's advantage over the superseded-name lookup disappears against a lookup over the whole name map. (Appendix~\\ref{app:baselines})\n",
             unit=u, section="8", note="the lead scoped to the completed models (section 3.1, S7's rule); H89 to the dagger's note (v)")


# ====================================================================================================================== s12
def unit_s12():
    u = "s12"
    rep("body", "Retraction and expiry are small groups ($30$ counterfactual pairs each; $26$ and $15$ obligations on the full set), so state-specific results give only a direction.",
        "Retraction and expiry are small groups ($30$ counterfactual pairs each; $26$ and $15$ obligations on the full set), so state-specific results give only a direction. Counts cannot say which record changed: two stores that cancel different plans in one category can share a summary, so only a named state identifies the obligation.",
        unit=u, section="9", note="S12 (only if the final slack is +3 or better)")


# ====================================================================================================================== rulings
def unit_rulings():
    """R133 RULINGS (the author, 2026-09-21): 1 the intro and Conclusion thesis sentences in the author's words (the abstract keeps S3), the repeat_scan and
    slogan_scan S7 exemptions removed (gate_edits_r133.py rulings); 3 tab:routes gains mini's per-state view-minus-summary rows (expiry, supersession) from
    resp_review/run/scores_resp.json through r133_number_gate.routes_rows, Section 7 pointing to it; 5 the three 'reliable' candidates of REPORT_R133.md
    section 9 dropped."""
    u = "rulings"
    rep("body", "In these tests, what the store wrote down limited every reader we gave it to.\n",
        "In these tests, every reader we tried was held back by what the store had written down.\n", unit=u, section="1", note="RULINGS 1 (S4 in the author's words)")
    rep("body", "In these tests, what a store wrote down limited every reader we gave it to. The smaller models",
        "In these tests, no reader we tried made up for what the store had failed to write down. The smaller models", unit=u, section="10", note="RULINGS 1 (S6's first sentence in the author's words)")
    rep("body", "and the name lookup stays a reliable $0.13$ above a lookup over meaningless tokens within triples.",
        "and the name lookup stays $0.13$ above a lookup over meaningless tokens within triples.", unit=u, section="5.2", note="RULINGS 5 (the first 'reliable' candidate dropped)")
    rep("body", "Luna and Sol lose on the questions pooled across them, each loss reliable (Table~\\ref{tab:census}).",
        "Luna and Sol lose on the questions pooled across them (Table~\\ref{tab:census}).", unit=u, section="6", note="RULINGS 5 (the second 'reliable' candidate dropped)")
    rep("body", "every model whose question-only score varies gains a reliable $0.15$ to $0.45$ with the summary, Kimi included.",
        "every model whose question-only score varies gains $0.15$ to $0.45$ with the summary, Kimi included.", unit=u, section="8", note="RULINGS 5 (the third 'reliable' candidate dropped)")
    rep("body", "and hurts it on supersession, where the summary names, both effects reliable. Haiku's score",
        "and hurts it on supersession, where the summary names, both effects reliable (Table~\\ref{tab:routes}). Haiku's score", unit=u, section="7", note="RULINGS 3 (Section 7 keeps the direction and points to tab:routes)")
    sys.path.insert(0, str(V23 / "tools"))
    import r133_number_gate as G
    rows, _ = G.routes_rows()
    anchor = "Tagged view, ground-truth tags & $0.69$ & $-0.05$ (the summary alone) & $[-0.13,+0.03]$ & $[-0.15,+0.04]$ \\\\\n"
    rep("appendix", anchor, anchor + "\n".join(rows) + "\n", unit=u, section="E.10",
        note="RULINGS 3: mini's per-state view-minus-summary rows (expiry, supersession) with both intervals, from resp_review/run/scores_resp.json (AUX-RESP-L2-MINI-NOK; reviews/NUMBERS_R133.md) through the number gate")
    rep("appendix", "$\\Delta$ is the monitor minus the comparison named in its row, with both intervals; Haiku 4.5 and the readers with no generative-model call are in Appendix~\\ref{app:resp}.}",
        "$\\Delta$ is the monitor minus the comparison named in its row, with both intervals; the two indented rows score that state's obligations against the same $557$ negatives. Haiku 4.5 and the readers with no generative-model call are in Appendix~\\ref{app:resp}.}",
        unit=u, section="E.10", note="RULINGS 3: the caption names the per-state rows' population")


UNITS = {"homes": unit_homes, "swaps": unit_swaps, "s4": unit_s4, "s51": unit_s51, "s52": unit_s52, "s53": unit_s53, "s6": unit_s6, "s7": unit_s7, "s8": unit_s8, "s12": unit_s12, "rulings": unit_rulings}


def main():
    units = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--units=")), "")
    units = [u for u in ORDER if u not in ("s12", "rulings")] if units == "all" else ([u for u in ORDER] if units == "close" else [u for u in units.split(",") if u])
    assert all(u in UNITS for u in units), f"unknown unit in {units}; known: {list(UNITS)}"
    assert units == [u for u in ORDER if u in units], f"units must be in the brief's order {ORDER}"
    if "--no-refresh" not in sys.argv:
        subprocess.run([sys.executable, str(V23 / "tools" / "bump_v23.py"), "--refresh"], check=True, capture_output=True)
    TEXT["body"], TEXT["abstract"], TEXT["appendix"] = rd(BODY), rd(ABS), rd(APPX)
    for u in units:
        UNITS[u]()
        print(f"unit {u}: applied ({sum(1 for r in LOGGED if r['unit'] == u)} edits)")
    wr(BODY, TEXT["body"]); wr(ABS, TEXT["abstract"]); wr(APPX, TEXT["appendix"])
    LOG.parent.mkdir(exist_ok=True)
    LOG.write_text(json.dumps(dict(units=units, edits=LOGGED), indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"-> {len(LOGGED)} edits logged to {LOG.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
