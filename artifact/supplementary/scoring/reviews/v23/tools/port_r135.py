# -*- coding: utf-8 -*-
"""port_r135.py -- R135 (2026-09-21; the author's brief 'R135: THE LAST CONTENT PASS ON v23', 'R135 ADDENDUM' (the Section 5.1 trims) and the ruling on
'R135 ADDENDUM 2') applied to the v23 sources on top of the R134 close (port_r134.py with every unit, which regenerates the R133 close underneath). Every
edit is an asserted replacement; every number the new texts print comes from reviews/v23/results/robust_printed.json (robust_tex.py) or
cf2_paraphrase/results/para_printed.json, and reviews/v23/tools/r135_number_gate.py checks each against its artifact. Units, in the brief's order of work:

  table     section 2 and the ADDENDUM: the evidence box leaves Section 3 (its four limits live in Section 4, Table 2's caption and Limitations); Section 5.2's
            opening paragraph gains the sentence pointing to tab:robust and the table's marker follows it; the two paragraphs the table absorbs leave 5.2;
            the rewording paragraph in the section 2.5 form; Section 5.1's second paragraph opens with the ADDENDUM's two sentences and its third paragraph
            is the ADDENDUM's, so 5.1 repeats no number the table prints
  abstract  section 3: the brief's abstract, verbatim (no newer text from the author since R134)
  fig3      section 4: Figure 3 in the Okabe-Ito palette with the marker shapes kept, same data file, same size and layout
  small     section 5: 5.1 the builders box's clause; 5.3 the G.5 sentence explained; (5.2 not applied: the HV-1 status lines stay verbatim by the pass's own
            rule and the ADDENDUM 2 ruling; 5.4 is a file copy and a bibliography check outside the sources)
  a2        ADDENDUM 2 as ruled: 1 the shorter Section 4 sentence; 2 the Section 7 propagation sentences with the trimmed second sentence; 3 G.2's clause;
            4 the three Graphiti Amendment 2 lines 'not completed at submission', the C.2 run notes 'then pending', the three HV-1 placeholders in E.10 untouched
  fig3h     section 4's height raise (about 15 percent), applied only if the slack after a2 is +4 or more (the ADDENDUM 2 ruling, item 4)

Logged to reviews/v23/results/port_r135_log.json for OLD_BESIDE_NEW_R135.md (changes_r135.py).
Usage: python reviews/v23/tools/port_r135.py --units=table,abstract,...   [--no-refresh]   (--units=all applies every unit but fig3h; --units=close applies every unit)
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
LOG = V23 / "results" / "port_r135_log.json"
P = json.load(open(ROOT / "cf2_paraphrase" / "results" / "para_printed.json", encoding="utf-8"))
RB = json.load(open(V23 / "results" / "robust_printed.json", encoding="utf-8"))
A8 = json.load(open(ROOT / "ds_downstream" / "run" / "lock_amend8.json", encoding="utf-8"))
R134_UNITS = "appendix,main,main_short,abstract,partb,payers"
ORDER = ["table", "abstract", "fig3", "small", "a2", "fig3h"]

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


def m(key):
    return f"${P[key]['printed']}$"


def rb(n):
    """The printed forms of tab:robust's row n (robust_printed.json 'values': printed -> value)."""
    return list(RB["rows"][n - 1]["values"].keys())


# ====================================================================================================================== table (+ the ADDENDUM's 5.1 trims)
def unit_table():
    u = "table"
    # 2.1 the evidence box leaves Section 3
    t = TEXT["body"]
    a = t.index("\\begin{center}\n\\small\n%% R126 (2026-09-19): the inbox's evidence table")
    b = t.index("\\end{center}\n", a) + len("\\end{center}\n")
    box = t[a:b]
    assert "What kind of evidence supports each result?" in box and box.count("\\begin{center}") == 1
    TEXT["body"] = t[:a] + t[b:]
    LOGGED.append(dict(unit=u, file="body", section="3, the evidence box", old=box, new="", note="section 2.1: the box removed; its four limits live in Section 4 (the matched metric is post hoc), Limitations (the 22 unmarked obligations; the detector exploratory and unvalidated) and Table 2's caption (no sampling interval)"))
    # 2.2 the pointer sentence at the end of 5.2's opening paragraph, and the table's marker after it
    rep("body", "none reliably above the lookup, while meaningless tokens and the count reader sit near chance.\n\n",
        "none reliably above the lookup, while meaningless tokens and the count reader sit near chance. Table~\\ref{tab:robust} lists the checks we ran to break this result and what each removes.\n\n"
        "%% R135 (2026-09-21): the robustness table (reviews/v23/src/robust_table.tex, written by reviews/v23/tools/robust_tex.py; every cell through r135_number_gate.py; reviews/NUMBERS_R135.md).\n"
        "%%ROBUST-TABLE%%\n\n",
        unit=u, section="5.2, the opening paragraph", note="section 2.2: the one sentence and the float")
    # 2.4 the two paragraphs the table absorbs
    rep("body", "%% R131 close, payer 8 (2026-09-20): the paragraph in the author's two sentences (MERGED RULINGS 1C; the lead keeps its run-in form with the author's verb); 0.60 / 0.65 and 24 of 88 stay in tab:cf-emptiness and tab:cf-matched.\n"
        "\\claim{List length and coverage lift both metrics.}\n"
        "A reader that only knows whether the store covers the question ties every triple and still scores $0.75$ pooled, and the name lookup stays $0.13$ above a lookup over meaningless tokens within triples.\n\n"
        "%% R126 addendum A6 (2026-09-20): the author's paragraph.\n%% R129 C2 (2026-09-20): the author's paragraph.\n"
        "\\claim{Long or wrong name lists weaken the readers together.}\n"
        "Padding the default list to $60$ names lowers the lookup to $0.67$ on the full obligation set, and injected wrong names lower mini, Haiku and the lookup together. Short ground-truth lists therefore do not establish robustness to longer store-written ones. (Appendix~\\ref{app:counterfactual})\n\n",
        "", unit=u, section="5.2, the two absorbed paragraphs", note="section 2.4: 0.13, 60 and 0.67 print in tab:robust (rows 2 and 9); 0.75 (the coverage-only reader) prints in Appendix C.2; the caveat sentence closes the table's caption")
    # 2.5 the rewording paragraph
    assert rb(7) == ["0.50", "0.02"]
    rep("body", f"With the questions rewritten to share no content word with any name in the summary ($115$ pairs), a word-matching lookup falls to chance and the embedding lookup loses {m('lookup_loss_v2')}. "
        f"Mini loses {m('mini_loss_v2')}, Haiku a reliable {m('haiku_loss_v2')} and Opus a reliable {m('opus_loss_v2')}; Luna and Sol do not move, and the stronger models keep their lead. ",
        f"With the questions rewritten to share no content word with any name in the summary ($115$ pairs), the embedding lookup loses {m('lookup_loss_v2')} and the two smaller models lose more (Table~\\ref{{tab:robust}}). ",
        unit=u, section="5.2, the rewording paragraph", note="section 2.5: the paragraph's first two sentences in the brief's form; the rest unchanged; 5.2 now points to Appendix C.2 once")
    # the ADDENDUM: Section 5.1 repeats no number the table prints
    rep("body", "With every count deleted, mini and Haiku stay within $0.01$ of their intact-summary scores; given the counts alone, they fall by $0.14$. ",
        "With every count deleted, mini and Haiku score as before (Table~\\ref{tab:robust}); given the counts alone, they fall by $0.14$. ",
        unit=u, section="5.1, the second paragraph", note="R135 ADDENDUM: the first two sentences; 0.01 prints in tab:robust (row 6)")
    rep("body", "On retraction and expiry, which the default summary only counts, none of Luna, Sol and Opus sits reliably below the guessing count reader (Figure~\\ref{fig:perstate}). When the obligation's extra count moves to a sibling version with the names unchanged, all three follow it, falling by $0.28$ to $0.33$ on the counted states, while mini and Haiku show no reliable change. "
        "The falls are reliable on the matched metric and, pooled, on expiry for all three and on retraction for Opus alone. Removing every count costs Luna $0.06$ and Opus $0.04$ on the pooled metric, and the counts alone still score below the names alone for both; all four differences are reliable. Cancelling the hike changes only a count in the default summary, and these three readers follow it. (Appendix~\\ref{app:counterfactual})",
        "On retraction and expiry, which the default summary only counts, none of Luna, Sol and Opus sits reliably below the guessing count reader (Figure~\\ref{fig:perstate}). When the obligation's extra count moves to a sibling version with the names unchanged, all three follow it, while mini and Haiku show no reliable change (Table~\\ref{tab:robust}). "
        "The falls are reliable on the matched metric and, pooled, on expiry for all three and on retraction for Opus alone. Removing every count costs Luna and Opus reliably, and the counts alone still score below the names alone for both. Cancelling the hike changes only a count in the default summary, and these three readers follow it. (Appendix~\\ref{app:counterfactual})",
        unit=u, section="5.1, the third paragraph", note="R135 ADDENDUM, verbatim; 0.28 to 0.33, 0.06 and 0.04 print in tab:robust (rows 5 and 6)")


# ====================================================================================================================== abstract
ABSTRACT = (
    "An agent with long-term memory can answer from a record it should no longer use, such as a plan the user later cancelled.\n"
    "We ask what a memory store must expose for an agent to know this before retrieving anything.\n"
    "Readers see only a value-free summary: record counts by lifecycle state and a list of attribute names.\n"
    "Each of $148$ questions is asked against three versions of one store that differ in one attribute, so wording cannot give the answer away.\n"
    "Where the summary names the affected attribute, none of five language models reliably beats a cosine-similarity lookup over the names, including under a control that fixes counts and list length.\n"
    "Reworded to share no word with the names, the lookup loses $0.02$ and one stronger model edges $0.04$ ahead.\n"
    "The three stronger models lead only where the summary counts a state without naming it, and one count feature closes that lead within a question, though not when items are pooled.\n"
    "The backends we tested omit or misstate this information: under FR-Bank's own metadata, GPT-4.1 mini, Haiku 4.5 and the lookup fall from $0.73$, $0.82$ and $0.75$ to $0.60$, $0.71$ and $0.59$.\n"
    "In these tests, what the store wrote down limited every reader we gave it to.\n"
    "All stores are synthetic, and we do not show that better judgments yield better answers.\n")


def unit_abstract():
    u = "abstract"
    t = TEXT["abstract"]
    a, b = t.index("\\begin{abstract}\n") + len("\\begin{abstract}\n"), t.index("\\end{abstract}")
    old = t[a:b]
    assert "human validation is pending." in old   # the R134 abstract; the placeholder leaves with the author's new last sentence (the brief, section 3)
    new = ("%% R135 (2026-09-21): the brief's abstract (section 3), verbatim but for the G2 ruling (option c): the parenthetical '(all readers at $0.88$ AUROC or higher)' deleted, 0.88 moved to tab:robust row 3.\n"
           "%% Numbers: r135_number_gate.py (148 = the triples;\n"
           "%% 0.02 = AUX-PARA-LOOKUP-EMB-V2 -0.0216; 0.04 = AUX-PARA-POSTHOC-MINUS-LOOKUP-LUNA-V2 +0.0445; 0.73 / 0.82 / 0.75 -> 0.60 / 0.71 / 0.59 = AUX-E1R-TRUE-NOK, AUX-R74-X4-H45-NOK, AUX-E1R-NB6,\n"
           "%% AUX-E1R-BELIEVED-NOK, AUX-BH-H45-15, AUX-E1R-NB6). The HV-1 placeholder clause is gone with the author's last sentence; 0.08 to 0.10 and 0.05 to 0.06 moved to Section 5.2 (NUMBER_MOVES_V23.md).\n"
           + ABSTRACT)
    TEXT["abstract"] = t[:a] + new + t[b:]
    LOGGED.append(dict(unit=u, file="abstract", section="the abstract", old=old, new=new, note="section 3 of the brief: the abstract, verbatim but for the G2 ruling (option c): the parenthetical '(all readers at $0.88$ AUROC or higher)' deleted; no rule change, no exemption"))


# ====================================================================================================================== fig3
OKABE = {"mini": "E69F00", "haiku": "56B4E9", "luna": "009E73", "sol": "D55E00", "opus": "0072B2", "count": "CC79A7"}   # the lookup keeps 'black' (Okabe-Ito's black; no HTML 000000, which numeric_diff would read as a numeral)


def unit_fig3():
    """Section 4 of the brief: the Okabe-Ito palette, one colour and one marker shape per reader (the shapes are the R126 ones), the same data file, size and layout."""
    u = "fig3"
    defs = "\n".join(f"\\definecolor{{fig{k}}}{{HTML}}{{{v}}}" for k, v in OKABE.items())
    # the definitions go in the preamble (after \pgfplotsset), outside the scanned document body: hex codes are not printed numbers
    rep("body", "\\pgfplotsset{compat=1.18}\n",
        "\\pgfplotsset{compat=1.18}\n%% R135 (2026-09-21), section 4: Figure 3's Okabe-Ito palette (one colour per reader; the marker shapes of R126 kept so the figure survives greyscale; the lookup stays black).\n"
        + defs + "\n", unit=u, section="the preamble (Figure 3's colours)", note="the colour definitions")
    rep("body", "%%FIG3-DATA-MATCHED%%\n\\begin{tikzpicture}\n",
        "%%FIG3-DATA-MATCHED%%\n%% R135 (2026-09-21), section 4: the Okabe-Ito palette (the colours are defined in the preamble); the legend's content, the size and the layout unchanged; the height not raised (the ruling).\n\\begin{tikzpicture}\n",
        unit=u, section="Figure 3", note="the figure's comment")
    pairs = [("mark=*, mark size=2.0pt, black,", "mark=*, mark size=2.0pt, figmini,", 2),
             ("mark=square*, mark size=1.9pt, black,", "mark=square*, mark size=1.9pt, fighaiku,", 2),
             ("mark=triangle*, mark size=2.3pt, black, mark options={fill=white},", "mark=triangle*, mark size=2.3pt, figluna, mark options={fill=white},", 1),
             ("mark=diamond*, mark size=2.3pt, black, mark options={fill=white},", "mark=diamond*, mark size=2.3pt, figsol, mark options={fill=white},", 1),
             ("mark=pentagon*, mark size=2.2pt, black,", "mark=pentagon*, mark size=2.2pt, figopus,", 2),
             ("mark=+, mark size=2.6pt, black!60, thick,", "mark=+, mark size=2.6pt, figcount, thick,", 1)]
    for old, new, n in pairs:
        rep("body", old, new, n=n, unit=u, section="Figure 3", note="the reader's colour")
    # the legend images of the right panel (Luna, Sol, the count reader) carry the same colours
    rep("body", "\\addlegendimage{only marks, mark=triangle*, mark size=2.3pt, black, mark options={fill=white}}", "\\addlegendimage{only marks, mark=triangle*, mark size=2.3pt, figluna, mark options={fill=white}}", unit=u, section="Figure 3", note="legend image")
    rep("body", "\\addlegendimage{only marks, mark=diamond*, mark size=2.3pt, black, mark options={fill=white}}", "\\addlegendimage{only marks, mark=diamond*, mark size=2.3pt, figsol, mark options={fill=white}}", unit=u, section="Figure 3", note="legend image")
    rep("body", "\\addlegendimage{only marks, mark=+, mark size=2.6pt, black!60, thick}", "\\addlegendimage{only marks, mark=+, mark size=2.6pt, figcount, thick}", unit=u, section="Figure 3", note="legend image")


def unit_fig3h():
    """The height raise, about 15 percent (4.5cm -> 5.2cm), only if the slack after a2 is +4 or more (the ADDENDUM 2 ruling, item 4)."""
    rep("body", "width=0.41\\linewidth, height=4.5cm,", "width=0.41\\linewidth, height=5.2cm,", unit="fig3h", section="Figure 3", note="section 4: the plot height raised by about 15 percent (the slack allowed it)")


# ====================================================================================================================== small
def unit_small():
    u = "small"
    # 5.1 the builders box
    rep("body", "in our tests a model added something only on counted states, on explicit intent questions and, on the pooled metric only, in the all-states comparison, and in the scenario we priced,",
        "in our tests a model added something only on counted states, on explicit intent questions and, on the pooled metric only, in the all-states comparison and under FR-Bank's store-written summary, where Haiku sits $0.12$ above the lookup, and in the scenario we priced,",
        unit=u, section="the builders box", note="section 5.1: the author's clause; 0.12 = AUX-BH-H45-15 Haiku minus lookup +0.1212, both intervals above zero")
    # 5.3 G.5's Valentina sentence explained in one clause
    rep("appendix", "Valentina's omitted source supports the disputed hobbies; the repaired judge now marks every condition's answer correct for that question.",
        "For one question, a persona's hobbies, the original reference packet had omitted the session that supports the answer; with that source restored, the repaired judge marks every condition's answer correct for that question.",
        unit=u, section="G.5", note="section 5.3: the opaque phrase explained (analysis/downstream_repair_v1/REPORT.md, the Valentina row: the omitted session supports the partner-hobby detail); G.5 kept")


# ====================================================================================================================== a2 (ADDENDUM 2 as ruled)
def unit_a2():
    u = "a2"
    # 1. Section 4 (the ruling's shorter sentence)
    rep("body", "Readers return probabilities under a fixed rubric. A \\emph{question-only} prompt omits the summary;",
        "Readers return probabilities under a fixed rubric. The scored step asks whether stale content about the question's target is present, which coincides with Definition~\\ref{def:coverage}'s obligation on the counterfactual set, "
        "where every question has current or upcoming intent; Section~\\ref{sec:intent} tests intent separately. A \\emph{question-only} prompt omits the summary;",
        unit=u, section="4, the readers paragraph", note="ADDENDUM 2 item 1 in the ruling's shorter form (Definition 1 and Section 5.3 through their labels)")
    # 2. Section 7 (the ruling's trimmed second sentence)
    c, d, f, g = A8["census"]["own"]["primary"], A8["dup35"]["own/primary"], A8["false_propagation"]["own/primary"], A8["census"]["gt"]["primary"]
    assert g["changed"] == 1 and g["views"] == 452 and d["items"] == 35 and f["active_lines_gt"] == 2333
    rep("body", "Propagating a lifecycle tag to matching lines under the same attribute changes $1$ of $452$ assembled views. ",
        f"Propagating a lifecycle tag to matching lines under the same attribute changes ${g['changed']}$ of ${g['views']}$ assembled views under the reference tags. "
        f"Under FR-Bank's own tags the same rule changes ${c['changed']}$ views and fully tags ${d['items_fully_tagged']}$ of the ${d['items']}$ duplicate views, but it also propagates falsely "
        f"(${f['false_propagations']}$ of ${f['active_lines_gt'] // 1000}{{,}}{f['active_lines_gt'] % 1000:03d}$ licensed active lines). ",
        unit=u, section="7, the propagation paragraph", note="ADDENDUM 2 item 2 (approved with the ruling's trim): the tag source; tab:ds-a8's own-tags primary column (AUX-DS-A8-RULE-CENSUS, -DUP35, -FALSEPROP)")
    # 3. G.2
    rep("appendix", "the control is the paraphrased counterfactual set, registered and pending (Table~\\ref{tab:registrations-c}).",
        "the control is the paraphrase check reported in Appendix~\\ref{app:counterfactual}, with this split recomputed on the rewrites (Table~\\ref{tab:para-flags}).",
        unit=u, section="G.2, the disclosure paragraph", note="ADDENDUM 2 item 3: one clause and a pointer to C.2")
    # 4. the grep hits: the three Graphiti Amendment 2 lines, the C.2 run notes; the three HV-1 placeholders in E.10 untouched
    rep("appendix", "& human scoring and prediction rulings pending \\\\", "& human scoring and prediction rulings not completed at submission \\\\", unit=u, section="F, tab:registrations-d (Graphiti Amendment 2)", note="ADDENDUM 2 item 4 (the ruling)")
    rep("appendix", "and the pending answer-stage predictions of Graphiti Amendment 2 are not yet in the count.", "and the answer-stage predictions of Graphiti Amendment 2, not completed at submission, are not in the count.", unit=u, section="F, the count paragraph", note="ADDENDUM 2 item 4 (the ruling)")
    rep("appendix", "Its registered human endpoints and prediction rulings remain pending;", "Its registered human endpoints and prediction rulings were not completed at submission;", unit=u, section="G.5", note="ADDENDUM 2 item 4 (the ruling)")
    rep("appendix", "An interim aggregate read was taken with the Opus 5 and Sol lanes pending;", "An interim aggregate read was taken with the Opus 5 and Sol lanes then pending;", unit=u, section="C.2, the run notes", note="ADDENDUM 2 item 4 (the ruling)")


UNITS = {"table": unit_table, "abstract": unit_abstract, "fig3": unit_fig3, "small": unit_small, "a2": unit_a2, "fig3h": unit_fig3h}


def main():
    units = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--units=")), "")
    units = [u for u in ORDER if u != "fig3h"] if units == "all" else ([u for u in ORDER] if units == "close" else [u for u in units.split(",") if u])
    assert all(u in UNITS for u in units), f"unknown unit in {units}; known: {list(UNITS)}"
    assert units == [u for u in ORDER if u in units], f"units must be in the brief's order {ORDER}"
    if "--no-refresh" not in sys.argv:
        subprocess.run([sys.executable, str(V23 / "tools" / "port_r134.py"), f"--units={R134_UNITS}"], check=True, capture_output=True)
    TEXT["body"], TEXT["abstract"], TEXT["appendix"] = rd(BODY), rd(ABS), rd(APPX)
    for u in units:
        UNITS[u]()
        print(f"unit {u}: applied ({sum(1 for r in LOGGED if r['unit'] == u)} edits)")
    wr(BODY, TEXT["body"]); wr(ABS, TEXT["abstract"]); wr(APPX, TEXT["appendix"])
    LOG.write_text(json.dumps(dict(units=units, edits=LOGGED), indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"-> {len(LOGGED)} edits logged to {LOG.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
