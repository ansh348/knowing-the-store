# -*- coding: utf-8 -*-
"""port_r134.py -- R134 (2026-09-21; the brief 'R134: LAND THE PARAPHRASE CHECK IN v23' and the author's rulings of the same day) applied to the v23
sources on top of the R133 close (port_r133.py --units=close, which refreshes the sources from v22 and applies every R133 unit). Every edit is an
asserted replacement (the old text must occur exactly the stated number of times) and every number the prose prints is read from
cf2_paraphrase/results/para_printed.json (para_tex.py), never typed; reviews/v23/tools/r134_number_gate.py checks each against its artifact.
Units, cumulative in the brief's order of work (section 7):

  appendix   section 5: Appendix C.2 gains the paraphrase check (the registration's 'Appendix D.2'): the procedure and disclosure paragraphs, the six
             tables through the %%PARA-TABLE:<name>%% markers, the ruling's statement under the supersession-only table, the sensitivity sentence, the
             branch readings, the genericity paragraph and the run notes; the 'Two registered checks' sentence and the pointer; tab:setup's row and
             tab:runs' caption sentence (Appendix A); tab:provenance's row; tab:registrations-c's caption, row and the dated-notes row; the AI-use
             sentence; G.5's dependency sentence (flag (b))
  main       section 4: the Section 5.2 paragraph (4.1, with the author's Branch B sentences of RULING 2), the Section 1 bullet (4.4), the Limitations
             sentences (4.5), the Conclusion sentence (4.6, RULING 2's numeral-free form)
  main_short section 4.2: the shorter Section 5.2 paragraph, only if the page gate fails with 'main'
  abstract   the author's abstract, verbatim (the ruling superseding 4.3)
  partb      section 6: B1 Table 1's note, B2 LifecycleBench in Setup, B3 the term bridge at the top of E.1, and the author's addition: the AI-use
             statement's sentence on the intent crossover's AI-assisted check, beside the paraphrase sentence
  payers     the author's RULING 3 (2026-09-21), the payers for Part B's page: P1 Section 4's coverage sentence shortened, the five daggers deleted, Appendix A's
             notes reworded; P2 the adaptive-retrieval citation string cut to five; P3 the Introduction's metamemory sentence; P4 the Conclusion's first
             paragraph after its first sentence; P5 the second contribution bullet; and the 5.1 moved-count range corrected to 0.28 to 0.33 through the number gate

Every replacement is logged to reviews/v23/results/port_r134_log.json (unit, file, section, old, new) for OLD_BESIDE_NEW_R134.md (changes_r134.py).
Usage: python reviews/v23/tools/port_r134.py --units=appendix,main,...   [--no-refresh]   (--units=all applies every unit but main_short; --units=close likewise;
       without --no-refresh the R133 close is regenerated first)
"""
from __future__ import annotations

import csv
import io
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
V23 = ROOT / "reviews" / "v23"
SRC = V23 / "src"
BODY, ABS, APPX = SRC / "body_v23.tex", SRC / "abstract_v23.tex", SRC / "appendix_v23.tex"
LOG = V23 / "results" / "port_r134_log.json"
P = json.load(open(ROOT / "cf2_paraphrase" / "results" / "para_printed.json", encoding="utf-8"))
SHEET = {int(r["row"]): r for r in csv.DictReader(io.open(ROOT / "reviews" / "para" / "PARA_APPROVAL_SHEET.csv", encoding="utf-8"))}
ORDER = ["appendix", "main", "main_short", "abstract", "partb", "payers"]

TEXT = {}
LOGGED = []


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def wr(p, t):
    p.write_text(t, encoding="utf-8", newline="\n")


def rep(which, old, new, n=1, unit="", section="", note=""):
    t = TEXT[which]
    c = t.count(old)
    assert c == n, f"[{unit}] {which}: expected {n} occurrence(s), found {c} of: {old[:90]!r}"
    TEXT[which] = t.replace(old, new)
    LOGGED.append(dict(unit=unit, file=which, section=section, old=old, new=new, note=note))


def ins_after(which, anchor, new, unit="", section="", note=""):
    t = TEXT[which]
    assert t.count(anchor) == 1, f"[{unit}] {which}: anchor not unique ({t.count(anchor)}): {anchor[:90]!r}"
    TEXT[which] = t.replace(anchor, anchor + new)
    LOGGED.append(dict(unit=unit, file=which, section=section, old="", new=new, note=note))


def ins_before(which, anchor, new, unit="", section="", note=""):
    t = TEXT[which]
    assert t.count(anchor) == 1, f"[{unit}] {which}: anchor not unique ({t.count(anchor)}): {anchor[:90]!r}"
    TEXT[which] = t.replace(anchor, new + anchor)
    LOGGED.append(dict(unit=unit, file=which, section=section, old="", new=new, note=note))


def m(key):
    """A two-decimal printed form from para_printed.json, in math mode."""
    return f"${P[key]['printed']}$"


def n_(key):
    return f"${P[key]}$"


# ====================================================================================================================== appendix
def unit_appendix():
    u = "appendix"
    bs = P["by_state"]; fl = P["ai_flags"]; dr = P["draws"]
    assert P["sup_original_none_above"] and not P["sup_haiku_matched_reliable"]
    assert P["branches"]["v2"]["headings"] == ["A", "D"] and P["branches"]["v3"]["headings"] == ["C", "D"]
    assert P["branches_sens"]["v2"]["headings"] == ["A", "D"] and P["branches_sens"]["v3"]["headings"] == ["C", "D"] and P["sens_lower_for_every_reader"]
    ex = {k: (SHEET[k]["original_question"], SHEET[k]["paraphrase"]) for k in (1, 12, 63)}
    # (a) C.2, the 'Two registered checks' paragraph: the pending sentence becomes one sentence and a pointer (section 5.2 of the brief)
    rep("appendix",
        "The paraphrase check asks each of the $148$ questions again in a wording that shares no content token with the attribute's slot path or with any attribute name the summary lists, drafted by GPT-4.1 mini under a deterministic screen; our label-transfer read has not been made, so no paraphrase row is printed.\n",
        f"The paraphrase check asks each of the {n_('n_questions')} questions again in a wording that shares no content token with the attribute's slot path or with any attribute name the summary lists; it is reported after Table~\\ref{{tab:pad}}.\n",
        unit=u, section="C.2, 'Two registered checks on this set'", note="section 5.2 of the brief: one sentence and a pointer")
    # (b) C.2 after tab:pad: the paraphrase check, items 1 to 11 of section 5.1
    block = (
        "%% R134 (2026-09-21): the paraphrase check landed (registrations/ADDENDUM_PARA.md, registered text sha256 45cad63d..., descriptive; the home its section 9 names,\n"
        "%% 'Appendix D.2', is this appendix). The prose is written by reviews/v23/tools/port_r134.py from cf2_paraphrase/results/para_printed.json and the tables by\n"
        "%% cf2_paraphrase/tools/para_tex.py (spliced at the per-table markers by build_v23.py); every number through r134_number_gate.py; ledgers\n"
        "%% cf2_paraphrase/NUMBERS_PARA.md (AUX-PARA-*) and reviews/NUMBERS_R134.md (AUX-R134-PRINTED). Report reviews/para/REPORT_PARA.md.\n"
        "\\paragraph{The paraphrase check.}\n"
        f"Each of the {n_('n_questions')} questions was rewritten by GPT-4.1 mini under a deterministic screen that forbids the attribute's own words and every name the summary prints; {n_('n_failed_screen')} pairs had no rewrite that passed the screen after three drafts.\n"
        f"An author read the remaining {n_('n_screen_passing')} against two questions, whether the rewrite asks the same thing under the same intent and whether it names the plan or value, and excluded {n_('n_excluded_by_read')} on the first, "
        f"leaving {n_('n_pairs')} (${bs['superseded']}$ supersession, ${bs['retracted']}$ retraction, ${bs['expired']}$ expiry) whose labels transfer from the original triples because the store versions are unchanged.\n"
        f"The registered floor of {n_('floor_registered')} accepted pairs was amended to the {n_('n_pairs')} before any scoring call, nothing was revisited, and the {n_('n_screen_passing')} are reported as a sensitivity analysis, not registered.\n"
        "The registration is descriptive: it carries no prediction, only the branch readings of Table~\\ref{tab:para-pooled} at a $\\pm0.05$ tolerance.\n"
        "\n"
        "The read was assisted.\n"
        "An AI assistant pre-read the exported sheet and flagged rows with a one-line reason, and a coding session printed persona evidence for nine flagged rows; neither saw a reader's output or a score, and every verdict is an author's.\n"
        f"Against those verdicts, the rows the assistant flagged as ones it would have rejected were excluded ${fl['A']['excluded']}$ of ${fl['A']['of']}$, the rows it flagged as depending on the persona ${fl['B']['excluded']}$ of ${fl['B']['of']}$, "
        f"the rows it flagged as vaguer but passable ${fl['C']['excluded']}$ of ${fl['C']['of']}$, and the unflagged rows ${fl['unflagged']['excluded']}$ of ${fl['unflagged']['of']}$.\n"
        "The sheet, the flags, the evidence and every verdict are in the artifact.\n"
        "\n"
        "%%PARA-TABLE:pooled%%\n"
        "%%PARA-TABLE:matched%%\n"
        "%%PARA-TABLE:minus-lookup%%\n"
        "%%PARA-TABLE:sup%%\n"
        # item 6 of section 5.1, in the words of the author's ruling on the branch
        f"On the named state, reworded, GPT-5.6 Luna is the only reader above the lookup (Table~\\ref{{tab:para-sup}}), by {m('sup_luna')} on the pooled metric.\n"
        f"It is the reader added after the registration; its matched interval includes zero; its pooled lower bounds are ${P['sup_luna_item_lo']['printed']}$ and ${P['sup_luna_persona_lo']['printed']}$; this is one of five comparisons and no multiplicity correction is applied; "
        "and Haiku 4.5's pooled and matched readings also disagree on this state.\n"
        "On the original questions of the same pairs no reader is reliably above the lookup.\n"
        "\n"
        "%%PARA-TABLE:sens%%\n"
        "The picture is the same with the nine excluded pairs put back, slightly lower for every reader (Table~\\ref{tab:para-sens}).\n"
        "\n"
        # item 8: the branch readings, both summaries, as the report states them
        "The registered readings, per summary, at the $\\pm0.05$ tolerance on the point estimate: under the summary naming superseded records only, the lexical lookup collapses and the embedding lookup holds; GPT-4.1 mini and Opus 5 hold where the lexical lookup collapses, Haiku 4.5 collapses, and the two added readers hold.\n"
        "Under the summary naming all states both lookups collapse and only Opus 5 holds; the embedding lookup's pooled loss there is beyond the registered tolerance, while its within-triple loss is not reliable (Table~\\ref{tab:para-matched}).\n"
        "\n"
        "%%PARA-TABLE:flags%%\n"
        # item 10: genericity
        "The rewrites are systematically more generic than the originals.\n"
        "Because the screen forbids the attribute's own words and every printed name, specific nouns give way to generic ones: "
        + "; ".join(f"``{o}'' became ``{p}''" for o, p in ex.values()) + ".\n"
        f"Over the {n_('n_pairs')} pairs the mean cosine of the question to its target name falls from ${P['cos_orig']}$ to ${P['cos_para']}$ and the mean content-token overlap with it from ${P['ov_orig']}$ to ${P['ov_para']}$, "
        "so every change above reflects both the loss of shared words and vaguer wording.\n"
        "\n"
        # item 11: run notes
        f"Draws: GPT-4.1 mini ${dr['MINI']}$, Haiku 4.5 ${dr['H45']}$, Opus 5 ${dr['OP5']}$ against its recorded ${dr['OP5_recorded']}$, GPT-5.6 Luna and GPT-5.6 Sol ${dr['LUNA']}$; the GPT-4.1 mini lane synchronous at list price, the Haiku 4.5 and Opus 5 lanes through the batch interface, "
        "the two added readers through the raw interface with the settings of their Table~\\ref{tab:cf-main} rows.\n"
        "Every served model identifier was checked before its lane, every lock of the registration held, and the lookup gate reproduced the recorded values on the original questions at four decimals.\n"
        "An interim aggregate read was taken with the Opus 5 and Sol lanes pending; no lane or analysis changed after it.\n"
        "\n")
    ins_after("appendix", "% PAD-TABLE-END\n\n", block, unit=u, section="C.2, after tab:pad: the paraphrase check", note="section 5.1 of the brief, items 1 to 11; the tables through the markers")
    # (c) Appendix A: tab:setup's row (the paraphrase lanes) and tab:runs' caption sentence
    ins_before("appendix", "the full obligation set & $661$ questions",
               f"the paraphrase set & {n_('n_items')} items: the {n_('n_pairs')} of the {n_('n_questions')} questions whose rewrite, sharing no content word with any printed name, passed a word screen and an author's read, asked of the same three store versions "
               f"({n_('n_pairs')} obligations: ${bs['superseded']}$ supersession, ${bs['retracted']}$ retraction, ${bs['expired']}$ expiry) & GPT-4.1 mini ({dr['MINI']}), Haiku 4.5 ({dr['H45']}), Opus 5 ({dr['OP5']}), GPT-5.6 Luna ({dr['LUNA']}), GPT-5.6 Sol ({dr['SOL']}); the last two under the default summary only \\\\\n",
               unit=u, section="A, tab:setup", note="section 5.2 of the brief: the paraphrase lanes in the run coverage")
    rep("appendix", "five models ran on the counterfactual set. $^{h}$: elicited through the vendor's agent harness",
        f"five models ran on the counterfactual set, and five ran its paraphrase set (Table~\\ref{{tab:setup}}): GPT-4.1 mini one call, Haiku 4.5 five, Opus 5 one, GPT-5.6 Luna and GPT-5.6 Sol five through the raw interface under the default summary only. $^{{h}}$: elicited through the vendor's agent harness",
        unit=u, section="A, tab:runs caption", note="the paraphrase lanes")
    # (d) Table 74: the provenance row
    ins_after("appendix", "& ground-truth summary & AUROC, persona-grouped bootstrap & registered predictions held; PN-vs-PRESENT decomposition post hoc \\\\\n",
              f"Paraphrase check, the lookup's loss of {m('lookup_loss_v2')} (Section~\\ref{{sec:lookup}}, Table~\\ref{{tab:para-pooled}}) & {n_('n_items')} items, {n_('n_pairs')} of the {n_('n_questions')} triples & manifest; labels transferred from the original triples, whose store versions are unchanged; rewrites screened by a word rule and read by an author with disclosed AI assistance & not needed: versions built from the manifest & ground-truth summary & AUROC, paired bootstrap (item and persona) & descriptive registration, no prediction; readings as they came out; the matched metric and the supersession-only comparison post hoc \\\\\n",
              unit=u, section="E.12, tab:provenance", note="section 5.2 of the brief: the provenance row")
    # (e) Appendix F: tab:registrations-c's caption, the paraphrase row's outcome, the dated-notes row
    rep("appendix", "Every one has run except the paraphrase check, which waits on our read.}",
        "Every one has run; the paraphrase check ran last, on the pairs an author's read accepted, and its dated notes and amendment are the row below it.}",
        unit=u, section="F, tab:registrations-c caption", note="the pending clause")
    rep("appendix", "both lookups and three models on the same store versions, paired against the originals; four branches enumerated & no prediction; pending \\\\\n",
        f"both lookups and three models on the same store versions, paired against the originals; four branches enumerated & no prediction; run on day $42$ on the {n_('n_pairs')} accepted pairs (Table~\\ref{{tab:para-pooled}}) \\\\\n"
        f"Paraphrased counterfactual set: the dated notes and the amendment & \\texttt{{2848f1ad}} (the whole file) & day 42 & below the registered text's marker, dated and never editing the text above: the read disclosed as AI-assisted (an assistant flagged rows with reasons and a coding session printed persona evidence; every verdict an author's); "
        f"the floor amended from {n_('floor_registered')} to the {n_('n_pairs')} accepted pairs before any scoring call, with the {n_('n_screen_passing')} screen-passing pairs as a sensitivity analysis, not registered; GPT-5.6 Luna and GPT-5.6 Sol added as readers, not registered, declared after the lookup result and before any model result & no prediction \\\\\n",
        unit=u, section="F, tab:registrations-c rows", note="section 5.2 of the brief: the dated notes and amendment in the list's style")
    # (f) the AI-use statement (body_v23.tex): one sentence beside the drafting sentence (the statement carries no crossover-check sentence to sit next to)
    rep("body", "the benchmark's human-written manifests are the ground truth against which every label is scored.\n",
        "the benchmark's human-written manifests are the ground truth against which every label is scored.\nAn AI assistant pre-read the paraphrase sheet and flagged rows with reasons; an author read every row and made every verdict.\n",
        unit=u, section="AI use statement", note="section 5.2 of the brief")
    # (g) flag (b): G.5's dependency sentence
    rep("appendix", "The registered human evaluation, detector validation and paraphrase approvals remain explicit dependencies.",
        "The registered human evaluation and detector validation remain explicit dependencies.", unit=u, section="G.5", note="flag (b), agreed: the paraphrase approvals are made")


# ====================================================================================================================== main
def para_52(short=False):
    if not short:
        return ("%% R134 (2026-09-21): the paraphrase check's paragraph (the brief, section 4.1; the Branch B sentences of the author's RULING 2); every number from\n"
                "%% cf2_paraphrase/results/para_printed.json through r134_number_gate.py (reviews/NUMBERS_R134.md AUX-R134-PRINTED).\n"
                "\\claim{The result survives rewording.}\n"
                f"We rewrote the questions so that none shares a content word with any name in the summary; {n_('n_pairs')} rewrites passed a word screen and an author's read. "
                f"A word-matching lookup falls to chance by construction. The embedding lookup loses {m('lookup_loss_v2')}, within tolerance. "
                f"Rewording costs mini {m('mini_loss_v2')}, Haiku a reliable {m('haiku_loss_v2')} and Opus a reliable {m('opus_loss_v2')}, while Luna and Sol do not move, so the lookup now sits a reliable {m('mini_minus_lookup_v2')} above mini and the stronger models keep the lead they had. "
                f"On the named state, reworded, mini and Haiku sit reliably below the lookup on the pooled metric (by {m('sup_mini')} and {m('sup_haiku')}), and Opus and Sol do not differ from it. "
                f"Luna, a reader we added after fixing the design, edges above it by {m('sup_luna')}, reliable on the pooled metric and not within triples; on the original questions no model exceeded it. "
                f"Under the all-states summary the lookup loses {m('lookup_loss_v3_pooled')} pooled, beyond tolerance, and {m('lookup_loss_v3_matched')} within triples. "
                "The rewrites are also vaguer than the originals, so each change reflects both. (Appendix~\\ref{app:counterfactual})\n\n")
    return ("%% R134 (2026-09-21): the paraphrase check's paragraph, the shorter form (the brief, section 4.2; the Branch B sentence of the author's RULING 2); every number from\n"
            "%% cf2_paraphrase/results/para_printed.json through r134_number_gate.py (reviews/NUMBERS_R134.md AUX-R134-PRINTED).\n"
            "\\claim{The result survives rewording.}\n"
            f"With the questions rewritten to share no content word with any name in the summary ({n_('n_pairs')} pairs), a word-matching lookup falls to chance and the embedding lookup loses {m('lookup_loss_v2')}. "
            f"Mini loses {m('mini_loss_v2')}, Haiku a reliable {m('haiku_loss_v2')} and Opus a reliable {m('opus_loss_v2')}; Luna and Sol do not move, and the stronger models keep their lead. "
            f"On the named state, reworded, mini and Haiku sit below the lookup and Luna, a reader we added later, edges {m('sup_luna')} above it on the pooled metric only. "
            f"Under the all-states summary the lookup loses {m('lookup_loss_v3_pooled')} pooled and {m('lookup_loss_v3_matched')} within triples. "
            "The rewrites are also vaguer than the originals. (Appendix~\\ref{app:counterfactual})\n\n")


def unit_main():
    u = "main"
    assert P["lookup_loss_v2"]["printed"] == "0.02" and P["sup_luna"]["printed"] == "0.04"
    # 4.1: the paragraph directly after the sibling-name control paragraph (Section 5.2's first paragraph)
    ins_after("body", "while meaningless tokens and the count reader sit near chance.\n\n", para_52(False), unit=u, section="5.2, after the sibling-name control paragraph", note="section 4.1 of the brief; RULING 2's Branch B sentences")
    # 4.4: the second contribution bullet
    rep("body", "including under a sibling-name control that holds counts and list length fixed; and a lookup with one count feature",
        f"including under a sibling-name control that holds counts and list length fixed, and the lookup loses {m('lookup_loss_v2')} when the questions are reworded to share no word with the names; and a lookup with one count feature",
        unit=u, section="1, the second contribution", note="section 4.4 of the brief")
    # 4.5: Limitations
    rep("body", "The paraphrase check is not yet scored. ",
        f"The paraphrase check covers {n_('n_pairs')} of the {n_('n_questions')} questions, its rewrites are vaguer than the originals, and Opus ran it with one draw. GPT-4.1 mini drafted the questions and is also a reader; it is the weakest reader. ",
        unit=u, section="9, Limitations", note="section 4.5 of the brief: the sentence replaced and the drafting sentence added in the same paragraph")
    # 4.6: the Conclusion (RULING 2's numeral-free sentence)
    rep("body", "On a named state no model reliably exceeds the name lookup, with list length kept fixed or not. ",
        "On a named state no model reliably exceeds the name lookup, with list length kept fixed or not. When the questions are reworded, the lookup holds up at least as well as the smaller models, and only one stronger model edges past it on a named state. ",
        unit=u, section="10, Conclusion", note="section 4.6 of the brief; RULING 2's sentence")


def unit_main_short():
    """Section 4.2 of the brief: the shorter Section 5.2 paragraph in place of 4.1's, only when the page gate fails."""
    u = "main_short"
    rep("body", para_52(False), para_52(True), unit=u, section="5.2, the paraphrase paragraph", note="section 4.2 of the brief: the shorter version after the page gate failed")


# ====================================================================================================================== abstract
ABSTRACT = (
    "An agent with long-term memory can answer from a record it should no longer use, such as a plan the user later cancelled.\n"
    "We test whether an agent can tell, before retrieving anything, that its store holds such a record, from a summary alone: counts of records by lifecycle state, and a list of attribute names with the values removed.\n"
    "Each of $148$ questions is asked against three versions of one store that differ in one attribute, so a question's wording cannot give the answer away.\n"
    "First, the two smaller of five models score the same with the counts removed, while the three stronger ones also use them.\n"
    "Second, for superseded records, the one state whose names the summary lists, no model reliably beats a cosine-similarity lookup over those names, even with counts and list length held fixed.\n"
    "Reworded so that no question shares a word with the names, the lookup loses $0.02$, the two smaller models fall below it, and one stronger model edges ahead by $0.04$.\n"
    "The stronger models' lead over the lookup of $0.08$ to $0.10$ comes from retracted and expired records, which the summary only counts; one count feature added to the lookup closes it within a question's three store versions, though not when all items are pooled ($0.05$ to $0.06$ remains).\n"
    "Third, the backends we tested omit or misstate this information.\n"
    "Given only what FR-Bank, which tags every entry with a lifecycle state, actually writes, GPT-4.1 mini, Haiku 4.5 and the lookup drop from $0.73$, $0.82$ and $0.75$ to $0.60$, $0.71$ and $0.59$ on our larger question set.\n"
    "In these tests, what the store wrote down limited every reader we gave it to.\n"
    "All stores are synthetic, and whether better judgments yield better answers is not established; human validation is pending.\n")


def unit_abstract():
    u = "abstract"
    t = TEXT["abstract"]
    a, b = t.index("\\begin{abstract}\n") + len("\\begin{abstract}\n"), t.index("\\end{abstract}")
    old = t[a:b]
    assert "human validation is pending." in old and "human validation is pending." in ABSTRACT
    assert P["lookup_loss_v2"]["printed"] == "0.02" and P["sup_luna"]["printed"] == "0.04"
    new = ("%% R134 (2026-09-21): the author's abstract, verbatim (the ruling superseding the brief's section 4.3; no gate rewords it). Numbers: r134_number_gate.py (148 = the triples;\n"
           "%% 0.02 = AUX-PARA-LOOKUP-EMB-V2 -0.0216; 0.04 = AUX-PARA-POSTHOC-MINUS-LOOKUP-LUNA-V2, supersession only, pooled, +0.0445; 0.08 to 0.10 = AUX-CF2-R125-VS-LOOKUP; 0.05 to 0.06 = AUX-CF2-HYB-VS-MODELS;\n"
           "%% 0.73 / 0.82 / 0.75 -> 0.60 / 0.71 / 0.59 = AUX-E1R-TRUE-NOK, AUX-R74-X4-H45-NOK, AUX-E1R-NB6, AUX-E1R-BELIEVED-NOK, AUX-BH-H45-15, AUX-E1R-NB6). The last clause is a placeholder (B5): it stays until the HV-1 numbers exist.\n"
           + ABSTRACT)
    TEXT["abstract"] = t[:a] + new + t[b:]
    LOGGED.append(dict(unit=u, file="abstract", section="the abstract", old=old, new=new, note="the author's abstract of 2026-09-21, verbatim; numerals in math mode as the source's convention"))


# ====================================================================================================================== Part B
def unit_partb():
    u = "partb"
    # B1: Table 1's note on the two count readers, from C.2's own explanation
    rep("body", "Count reader, given category & superseded & $0.60$", "Count reader, given category$^{c}$ & superseded & $0.60$", unit=u, section="Table 1", note="B1: the mark")
    rep("body", "fit with personas left out (Table~\\ref{tab:cf-hybrid}).\n",
        "fit with personas left out (Table~\\ref{tab:cf-hybrid}). $^{c}$The two read different quantities: the given-category reader ties every supersession triple and is perfect on the counted states by construction.\n",
        unit=u, section="Table 1, the note", note="B1: taken from C.2's explanation of the two readers; one line, as the brief asks (the three-line form cost the page: gates_r134_partb_a.txt)")
    # B2: LifecycleBench, once, where the FR-Bank release is introduced
    rep("body", "and part of the main question set come from the FR-Bank release \\citep{fr}.",
        "and part of the main question set come from the FR-Bank release (its LifecycleBench personas) \\citep{fr}.", unit=u, section="4, Labels and summaries", note="B2")
    # the author's addition to step 6 (2026-09-21): the AI-assisted check of the intent-crossover questions, in the AI-use statement beside the paraphrase sentence,
    # accurate to the record (registrations/ADDENDUM_CF2_INTENT_CROSSOVER.md, 'Author check': "The author's check was assisted by an AI model that pre-flagged candidate
    # failures; every verdict was made by the author and entered from the author's dictated list.")
    rep("body", "An AI assistant pre-read the paraphrase sheet and flagged rows with reasons; an author read every row and made every verdict.\n",
        "An AI assistant pre-read the paraphrase sheet and flagged rows with reasons; an author read every row and made every verdict.\n"
        "For the intent crossover's questions an AI model pre-flagged candidate failures before an author's check; every verdict was an author's, entered from a dictated list.\n",
        unit=u, section="AI use statement", note="the author's addition to step 6: the crossover check's sentence, from the registration's disclosure line")
    # B3: the term bridge at the top of E.1
    rep("appendix", "The paper uses one vocabulary and the artifact records another.\n",
        "The paper uses one vocabulary and the artifact records another.\n"
        "Three pairs of terms recur in the appendix prose before the table at the end of this section defines them: \\emph{blind} and \\emph{indexed} are the main text's question only and with the summary; \\emph{route A} and \\emph{route B} are the summary route and the tag route; and \\emph{the monitor} is the reader, a name lookup or a model.\n",
        unit=u, section="E.1, the glossary's opening", note="B3: the term bridge; nothing renamed in pinned text")


# ====================================================================================================================== payers (RULING 3)
def unit_payers():
    """The author's RULING 3 of 2026-09-21 (the payers for Part B's page): P1 to P5 verbatim, and the 5.1 moved-count range corrected through the number gate."""
    u = "payers"
    # P1: Section 4's coverage sentence; the five daggers; Appendix A's notes no longer refer to a dagger
    rep("body", "Appendix~\\ref{app:laddertable} lists both, and a dagger marks a number in the text that has a coverage note there.", "Appendix~\\ref{app:laddertable} lists both.",
        unit=u, section="4, the models paragraph", note="P1")
    rep("body", "With every count deleted, mini$^{\\dagger}$ and Haiku stay within", "With every count deleted, mini and Haiku stay within", unit=u, section="5.1", note="P1: the first dagger")
    rep("body", "Removing every count costs Luna $0.06$ and Opus $0.04^{\\dagger}$ on the pooled metric", "Removing every count costs Luna $0.06$ and Opus $0.04$ on the pooled metric", unit=u, section="5.1", note="P1: the second dagger")
    rep("body", "Haiku by a reliable $0.35^{\\dagger}$ on the two states that were only counted", "Haiku by a reliable $0.35$ on the two states that were only counted", unit=u, section="5.2", note="P1: the third dagger")
    rep("body", "Luna, Sol and Opus score $0.88$ to $0.99^{\\dagger}$, while mini and Haiku", "Luna, Sol and Opus score $0.88$ to $0.99$, while mini and Haiku", unit=u, section="5.3", note="P1: the fourth dagger")
    rep("body", "Haiku, Luna and Opus score $0.82$ to $0.83^{\\dagger}$ against the lookup's $0.75$", "Haiku, Luna and Opus score $0.82$ to $0.83$ against the lookup's $0.75$", unit=u, section="8", note="P1: the fifth dagger")
    rep("appendix", "\\paragraph{Coverage notes for the daggers in the main text.}\n"
        "A dagger on a number in the main text marks a run setting that differs from its neighbours in the same sentence, or a comparison set that is incomplete; each resolves to one note here.\n",
        "\\paragraph{Coverage notes for the main text.}\n"
        "Each note below records a run setting that differs from its neighbours in the same sentence of the main text, or a comparison set that is incomplete.\n",
        unit=u, section="A, the coverage notes", note="P1: the notes stay, reworded so they no longer refer to a dagger")
    # P2: the adaptive-retrieval citation string only
    rep("body", "\\citep{lewis2020,flare,mallen2023,ren2025,wang2023,selfrag,su2024,seakr,verbrouting,metamem}", "\\citep{lewis2020,flare,mallen2023,selfrag,su2024}",
        unit=u, section="2, Related work", note="P2: Lewis 2020, Jiang 2023 (flare), Mallen 2023, Asai 2024 (selfrag), Su 2024 kept; ren2025, wang2023, seakr, verbrouting, metamem dropped from the string; no other citation touched")
    # P3: the metamemory sentences of the Introduction
    rep("body", "Their metamemory names are negative-obligation knowledge (NOK) and feeling of knowing (FOK), which connect these questions to judgments about one's own memory \\citep{hart1965,nelson1990,koriat1993}. Here, the object of the judgment is an external store.",
        "In metamemory terms these are negative-obligation knowledge (NOK) and the feeling of knowing (FOK) \\citep{hart1965,nelson1990,koriat1993}, here judged about an external store.",
        unit=u, section="1", note="P3, verbatim (the citation as \\citep)")
    # P4: the Conclusion's first paragraph after its first sentence (the author's)
    rep("body", "In these tests, no reader we tried made up for what the store had failed to write down. The smaller models score the same with the counts removed; the stronger ones also read the counts, and a lookup given one count feature matches them within triples, though not on the pooled metric. "
        "On a named state no model reliably exceeds the name lookup, with list length kept fixed or not. When the questions are reworded, the lookup holds up at least as well as the smaller models, and only one stronger model edges past it on a named state. "
        "Told the intent rule, only the three stronger models apply it, and a fixed cue list matches the best of them.",
        "In these tests, no reader we tried made up for what the store had failed to write down. On a named state no model reliably exceeds the name lookup, with list length kept fixed or not, and when the questions are reworded only one stronger model edges past it. "
        "The stronger models' lead comes from counts the smaller models do not use. Told the intent rule, only the stronger models apply it, and a fixed cue list matches the best of them.",
        unit=u, section="10, Conclusion", note="P4, verbatim; the first sentence kept as it stands")
    # P5: the second contribution bullet
    rep("body", "\\item Evidence about what readers read. The two smaller models score the same with the counts removed and three stronger models also use the counts; on the named state no model reliably exceeds a name lookup, including under a sibling-name control that holds counts and list length fixed, "
        f"and the lookup loses {m('lookup_loss_v2')} when the questions are reworded to share no word with the names; and a lookup with one count feature matches the stronger models within triples, though not on the pooled metric.",
        f"\\item Evidence about what readers read. On the named state no model reliably exceeds a name lookup, including under a control that holds counts and list length fixed, and the lookup loses {m('lookup_loss_v2')} when the questions are reworded to share no word with the names. "
        "The stronger models' lead comes from the counts, which the two smaller models do not use.",
        unit=u, section="1, the second contribution", note="P5, verbatim")
    # the 5.1 check: the three stronger models' matched moved-count differences on the counted states (tab:cf-matched-ablations' 'counted states' rows; r125_matched.json contrasts) are
    # Opus -0.2833, Luna -0.2917, Sol -0.3250, so the range prints 0.28 to 0.33 (0.27 was Luna's expiry value; r134_number_gate.py checks the range)
    rep("body", "falling by $0.27$ to $0.33$ on the counted states", "falling by $0.28$ to $0.33$ on the counted states", unit=u, section="5.1", note="the moved-count range on the counted states, corrected through the number gate (AUX-CF2-R125-CONTRASTS counted: Opus -0.2833, Luna -0.2917, Sol -0.3250)")


UNITS = {"appendix": unit_appendix, "main": unit_main, "main_short": unit_main_short, "abstract": unit_abstract, "partb": unit_partb, "payers": unit_payers}


def main():
    units = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--units=")), "")
    units = [u for u in ORDER if u != "main_short"] if units in ("all", "close") else [u for u in units.split(",") if u]
    assert all(u in UNITS for u in units), f"unknown unit in {units}; known: {list(UNITS)}"
    assert units == [u for u in ORDER if u in units], f"units must be in the brief's order {ORDER}"
    if "--no-refresh" not in sys.argv:
        subprocess.run([sys.executable, str(V23 / "tools" / "port_r133.py"), "--units=close"], check=True, capture_output=True)
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
