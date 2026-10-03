# -*- coding: utf-8 -*-
"""integ_cuts.py -- the page-budget step of the integration pass (2026-09-16, program R112): asserted replacements that consolidate
repetition and move supporting detail to the appendix (the author's authorization of 2026-09-16). Tables 3 (tab:routes) and 5 (tab:levels)
move verbatim to Appendices E.10 and E.9, where their rows already stand in tab:routes-full and the store-written census prose; the body
keeps every number it states in prose. No number, n, interval or population changes; every vanished token is dispositioned in
reviews/v19/NUMBER_MOVES_V19.md. Run from the repository root: python reviews/v19/tools/integ_cuts.py [--step N]
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v19" / "src"
B, X = SRC / "body_v19.tex", SRC / "appendix_v19.tex"


def table_block(t, label):
    """The \\begin{table}...\\end{table} block carrying \\label{label}, with the preceding blank line."""
    i = t.index("\\label{" + label + "}")
    s = t.rfind("\\begin{table}", 0, i)
    e = t.index("\\end{table}", i) + len("\\end{table}")
    return t[s:e]


def rep(t, old, new, name):
    n = t.count(old)
    assert n == 1, f"{name}: expected 1, found {n}: {old[:100]!r}"
    return t.replace(old, new)


def main():
    step = int(sys.argv[sys.argv.index("--step") + 1]) if "--step" in sys.argv else 99
    only = set(int(s) for s in sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
    def on(k):
        return (k in only) if only is not None else (step >= k)
    b = B.read_text(encoding="utf-8"); x = X.read_text(encoding="utf-8")

    if on(1):
        # ---- Table 3 to E.10 (before the own-tags paragraph), Table 5 to E.9 (before the Haiku-under-own-metadata paragraph)
        t3 = table_block(b, "tab:routes"); t5 = table_block(b, "tab:levels")
        b = rep(b, "\n" + t3 + "\n", "\n", "table 3 out")
        b = rep(b, "\n" + t5 + "\n", "\n", "table 5 out")
        note = "%% R112 (2026-09-16), the page-budget step of the integration pass: this table moved verbatim from the main text (its rows also stand in Table~\\ref{tab:routes-full}); the body states its numbers in prose.\n"
        x = rep(x, "\\paragraph{The tagged view under the store's own tags, and Haiku 4.5 on the retrieved-view monitors.}",
                note + t3.replace("\\begin{table}[h]", "\\begin{table}[H]") + "\n\n\\paragraph{The tagged view under the store's own tags, and Haiku 4.5 on the retrieved-view monitors.}", "table 3 in")
        note5 = "%% R112 (2026-09-16), the page-budget step of the integration pass: this table moved verbatim from the main text; the body states its numbers in prose.\n"
        anchor5 = x[x.index("\\paragraph{", x.index("\\label{tab:bh-split}") - 4000):]  # not used; the anchor below is textual
        x = rep(x, "\\paragraph{A fourth backend, measured on three personas.}", note5 + t5.replace("\\begin{table}[h]", "\\begin{table}[H]") + "\n\n\\paragraph{A fourth backend, measured on three personas.}", "table 5 in")
        # body pointers: Table 3 -> the appendix table; Table 5 stays referenced by label
        b = rep(b, "Shown that view and no summary, GPT-4.1 mini scores $0.69$ against $0.73$ under the summary; shown both, $0.83$ (Table~\\ref{tab:routes}).",
                "Shown that view and no summary, GPT-4.1 mini scores $0.69$ against $0.73$ under the summary; shown both, $0.83$ (Table~\\ref{tab:routes}, Appendix~\\ref{app:resp}).", "t3 pointer")
        b = rep(b, "Haiku 4.5 keeps $72\\%$ of its gain capped and $79\\%$ lifted (Table~\\ref{tab:levels}).",
                "Haiku 4.5 keeps $72\\%$ of its gain capped and $79\\%$ lifted (Table~\\ref{tab:levels}, Appendix~\\ref{app:census}).", "t5 pointer")

    if on(2):
        # ---- Section 6: the own-tags paragraph consolidated; the mirror paragraph's last two sentences merged
        b = rep(b, "FR-Bank's tags mark $1{,}389$ of the $3{,}305$ lines shown as non-active where the ground-truth tags mark $217$, a precision of $0.14$.\nGPT-4.1 mini's obligation score on that view rises from $0.69$ to a reliable $0.81$ on the full obligation set.\nMore tags is not the reason: a count of tagged lines scores $0.62$ under either tag source.\nThe reason is that the store's tags reach more of the forbidding records.\nOf the $99$ forbidding records in view, the store's tags mark $70$ non-active against the ground-truth tags' $60$, and the indicator that the item's forbidding record is in view and tagged scores $0.72$ against $0.67$.\nThe monitor exceeds that indicator by $+0.09$ (Table~\\ref{tab:routes-full}, Appendix~\\ref{app:resp}).",
                "FR-Bank's tags mark $1{,}389$ of the $3{,}305$ lines shown as non-active where the ground-truth tags mark $217$, a precision of $0.14$, and GPT-4.1 mini's obligation score on that view rises from $0.69$ to a reliable $0.81$.\nThe reason is reach rather than volume: the store's tags mark $70$ of the $99$ forbidding records in view against the ground-truth tags' $60$, while a count of tagged lines scores $0.62$ under either tag source (Table~\\ref{tab:routes-full}, Appendix~\\ref{app:resp}).", "s6 own-tags")
        b = rep(b, "Shown both, GPT-4.1 mini gains a reliable $+0.10$ over the summary alone, its best monitor.\nHaiku 4.5 scores $0.79$ shown both against $0.82$ under its summary alone, so the combined monitor is the best measured for GPT-4.1 mini only (Appendix~\\ref{app:resp}).",
                "Shown both, GPT-4.1 mini gains a reliable $+0.10$ over the summary alone, while Haiku 4.5 scores $0.79$ shown both against $0.82$ under its summary alone, so the combined monitor is best for GPT-4.1 mini only (Appendix~\\ref{app:resp}).", "s6 mirror")

    if on(3):
        # ---- Section 9: the two further results as one pointer sentence; the stale paragraph's two respected-tags sentences merged
        b = rep(b, "Two further results, one sentence each.\nA header naming the persona and the date raises in-view correct answers from $37$ to $48$ for GPT-4.1 mini and from $38$ to $59$ for Haiku 4.5, both reliable (Appendix~\\ref{app:resp}).\n",
                "Two further results stand in Appendix~\\ref{app:resp}: a header naming the persona and the date raises in-view correct answers reliably for both answerers, and the composite below.\n", "s9 pointers")
        b = rep(b, "Tags in view are respected: the detector flags GPT-4.1 mini on $0$ of the $50$ views where every stale line is tagged or absent.\nEach of its $16$ flagged answers under the oracle falls on a view with an untagged duplicate.",
                "Tags in view are respected: the detector flags GPT-4.1 mini on $0$ of the $50$ views where every stale line is tagged or absent, and each of its $16$ flagged answers under the oracle falls on a view with an untagged duplicate.", "s9 respected")

    if on(4):
        # ---- Section 8: the deleted-record pair to the appendix pointer (E.3 prints the four-decimal pair); Section 5: list-length in one sentence
        b = rep(b, "FOK detects a missing topic, $0.55$ to $0.88$, but not a single deleted record, $0.43$ to $0.50$, chance.\nThe missing record is NOK's target.\n",
                "FOK detects a missing topic and not a single deleted record, which is NOK's target (Appendix~\\ref{app:construction}).\n", "s8 deleted record")
        b = rep(b, "The lookup works because the list is short and clean.\nAs the list grows or fills with wrong names, the lookup and the models fall together (Appendix~\\ref{app:counterfactual}).",
                "The lookup works because the list is short and clean; as it grows or fills with wrong names, the lookup and the models fall together (Appendix~\\ref{app:counterfactual}).", "s5 list length")

    if on(5):
        # ---- Section 7: the FR-Bank census in one sentence; the own-name split without the lookup halves (they stand in tab:bh-split)
        b = rep(b, "FR-Bank marks $5{,}968$ of its $18{,}936$ entries inactive, where the ground-truth manifest explains about $102$ of those marks as supersessions.\nIn entries, the manifest's supersessions touch $104$, and the store still lists $40$ of those as active.",
                "FR-Bank marks $5{,}968$ of its $18{,}936$ entries inactive where the manifest explains about $102$, and still lists $40$ of the $104$ entries the manifest's supersessions touch as active.", "s7 census")
        b = rep(b, "\nThe lookup on the same halves scores $0.76$ where the name is present and $0.80$ where it is absent, on $10$ items with item interval $[0.67,0.90]$ (Table~\\ref{tab:bh-split}, Appendix~\\ref{app:census}).",
                " The lookup on the same halves is in Table~\\ref{tab:bh-split} (Appendix~\\ref{app:census}).", "s7 split")

    if on(6):
        # ---- Section 1 bullet 3 to 31 words; Section 4's cap sentences merged; Limitations' two new sentences merged (and no 'join' token)
        b = rep(b, "\\item We show that attribute names carry most of the monitors' signal: the name lookup matches two of three models, and the count interventions do not establish count use for the states the summary only counts (retracted and expired).",
                "\\item We show that attribute names carry most of the monitors' signal: the name lookup matches two of three models, and the count interventions do not establish count use for retracted and expired content.", "bullet 3")
        b = rep(b, "The cap, fixed before the pilot, never binds on the ground-truth summary, whose superseded list averages under two names.\nIt binds on the store's own metadata, so both renderings are reported, capped and with the cap lifted (Appendix~\\ref{app:repro}).",
                "The cap, fixed before the pilot, never binds on the ground-truth summary, whose superseded list averages under two names, and binds on the store's own metadata, which is reported capped and with the cap lifted (Appendix~\\ref{app:repro}).", "s4 cap")
        b = rep(b, "The ground-truth tags come from a join of the manifests to the stored records that marks the forbidding record for $82$ of the $104$ obligations, so record-level precision and recall rest on that alignment.\nThe duplicate retagging used the obligations' reference information, so it is diagnostic, and the detector that flags stale answers awaits its human validation.",
                "The ground-truth tags come from an alignment of the manifests to the stored records that marks the forbidding record for $82$ of the $104$ obligations; the duplicate retagging used the obligations' reference information, so it is diagnostic, and the detector that flags stale answers awaits its human validation.", "limitations")

    if on(7):
        # ---- Section 5's reader introduction in two lines; Table 4's FR-Bank cell without its threshold clause (E.9 keeps it); Section 7's capped/lifted
        # definition (Section 4 defines it); Limitations' counted-state sentences merged; Definition 2's pointer; Section 4's interval sentences merged; Figure 3 at 3.0 cm
        b = rep(b, "Table~\\ref{tab:cf-main} gives every reader on the whole set and Figure~\\ref{fig:perstate} per state, with two readers that have no model in them.\nOne is the name lookup, a similarity lookup over the superseded-names list; the other is a count reader that guesses the question's category from its text and reads that category's retracted and expired \\emph{counts}.\nA category-aware count reader, which takes the category from the manifest, is that reader's upper bound on the two counted states.",
                "Table~\\ref{tab:cf-main} and Figure~\\ref{fig:perstate} add two readers with no model in them: the name lookup over the superseded-names list, and a count reader that guesses the question's category from its text and reads that category's retracted and expired \\emph{counts}, with a category-aware version, the category taken from the manifest, as its upper bound.", "s5 readers")
        b = rep(b, " and retains an active obsolete assertion after $72\\%$ of supersession events, at the stored-versus-obsolete matching threshold of the census. \\\\",
                " and retains an active obsolete assertion after $72\\%$ of supersession events (Appendix~\\ref{app:census}). \\\\", "table 4 cell")
        b = rep(b, "The store-written summary is read capped (with the renderer's fifteen-name cap in place) and lifted (with the cap removed).\n", "", "s7 capped def")
        b = rep(b, "The counted-state groups are small: $30$ retraction and $30$ expiry pairs on the counterfactual set, and $44$ expiry with the extension draw of Appendix~\\ref{app:counterfactual}. On the full obligation set they are $26$ retraction and $15$ expiry obligations, whose counted-state rows give only a direction.",
                "The counted-state groups are small, $30$ retraction and $30$ expiry pairs on the counterfactual set ($44$ expiry with the extension draw of Appendix~\\ref{app:counterfactual}) and $26$ and $15$ obligations on the full set, whose rows give only a direction.", "limitations counted")
        b = rep(b, "A rendered summary is Listing~\\ref{lst:summary} in Appendix~\\ref{app:construction}; the count table is included because it was part of the summary as fixed before the study.",
                "A rendered summary is Listing~\\ref{lst:summary} in Appendix~\\ref{app:construction}, the count table included because it was part of the summary as fixed before the study.", "def2 pointer")
        b = rep(b, "We report the item-level paired bootstrap interval first and the persona-grouped interval second, and where they disagree the wider decides.\nWe call a difference \\emph{reliable} when both intervals exclude zero, and \\emph{within tolerance} when $|\\Delta| \\le 0.05$.",
                "We report the item-level paired bootstrap interval first and the persona-grouped interval second, the wider deciding where they disagree; a difference is \\emph{reliable} when both intervals exclude zero and \\emph{within tolerance} when $|\\Delta| \\le 0.05$.", "s4 intervals")
        b = rep(b, "width=0.5\\linewidth, height=3.3cm,", "width=0.5\\linewidth, height=3.0cm,", "figure 3 height")

    if on(8):
        # ---- Table 1 (tab:setup) to Appendix A, before tab:populations, which defines the same populations in full
        t1 = table_block(b, "tab:setup")
        b = rep(b, "\n" + t1 + "\n", "\n", "table 1 out")
        b = rep(b, "Table~\\ref{tab:setup} names every population, every later number is stated on one of them, and Appendix~\\ref{app:provenance} traces each headline number to its labels, tag source and evaluator.",
                "Table~\\ref{tab:setup} (Appendix~\\ref{app:laddertable}) names every population with its size, positives and the models that ran on it; every later number is stated on one of them, and Appendix~\\ref{app:provenance} traces each headline number to its labels, tag source and evaluator.", "t1 pointer")
        x = rep(x, "%% R110: the population list (OUTLINE.md section C), moved here from Section 4",
                "%% R112 (2026-09-16), the page-budget step of the integration pass: Table tab:setup moved verbatim from Section 4; tab:populations and tab:runs below define the same populations in full.\n" + t1.replace("\\begin{table}[h]", "\\begin{table}[H]") + "\n\n%% R110: the population list (OUTLINE.md section C), moved here from Section 4", "table 1 in")

    B.write_text(b, encoding="utf-8", newline="\n"); X.write_text(x, encoding="utf-8", newline="\n")
    print(f"cuts applied: {sorted(only) if only is not None else list(range(1, min(step, 8) + 1))}")


if __name__ == "__main__":
    main()
