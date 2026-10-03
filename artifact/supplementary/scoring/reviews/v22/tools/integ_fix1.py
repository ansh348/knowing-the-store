# -*- coding: utf-8 -*-
"""integ_fix1.py -- the gate fixes after the second integrated build (2026-09-16, program R112): the 35-word sentences split, the repeated
9-gram and the near-duplicate pair varied, the abstract to 270 words, the alias label issued through a preamble macro (so the token scan,
which skips the preamble, does not read a label as prose), the quoted P1 text marked as shipping verbatim. Asserted replacements.
Run from the repository root: python reviews/v19/tools/integ_fix1.py
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v19" / "src"
A, B, X = SRC / "abstract_v19.tex", SRC / "body_v19.tex", SRC / "appendix_v19.tex"
E = []


def rep(f, old, new):
    E.append((f, old, new))


# ---- the abstract to 270 words
rep(A, "(three models, one question asked of three store versions)", "(three models; one question, three store versions)")
rep(A, "and measure them on three backends with six models from three vendors.", "and measure them on three backends with six models.")
rep(A, "reduced the flagged answers, which points to the write path pending human validation of the detector.", "reduced the flagged answers, pointing to the write path, pending human validation of the detector.")
rep(A, "is a second route, at retrieval time, that covers what the list misses.", "is a second route, at retrieval time, covering what the list misses.")
rep(A, "such as a cancelled plan or a replaced value", "such as a cancelled plan or replaced value")

# ---- the 9-gram and the near-duplicate pair
rep(B, "For the three models tested on the summary alone, the attribute names carry most of the signal, and the count interventions do not establish consistent count use (Section~\\ref{sec:counterfactual}).",
    "For the three models tested on the summary alone, the attribute names carry most of the signal, and no count intervention establishes consistent count use (Section~\\ref{sec:counterfactual}).")
rep(B, "In a lifecycle summary the attribute names carry most of the signal the models use, and the count interventions do not establish consistent count use.",
    "The models draw most of their signal from a lifecycle summary's attribute names; nothing we tried with the counts establishes that they use them consistently.")

# ---- the sentences over 35 words
rep(B, "Table~\\ref{tab:setup} (Appendix~\\ref{app:laddertable}) names every population with its size, positives and the models that ran on it; every later number is stated on one of them, and Appendix~\\ref{app:provenance} traces each headline number to its labels, tag source and evaluator.",
    "Table~\\ref{tab:setup} (Appendix~\\ref{app:laddertable}) names every population with its size, positives and models, and every later number is stated on one of them.\nAppendix~\\ref{app:provenance} traces each headline number to its labels, tag source and evaluator.")
rep(B, "The cap, fixed before the pilot, never binds on the ground-truth summary, whose superseded list averages under two names, and binds on the store's own metadata, which is reported capped and with the cap lifted (Appendix~\\ref{app:repro}).",
    "The cap, fixed before the pilot, never binds on the ground-truth summary, whose superseded list averages under two names; it binds on the store's own metadata, reported capped and with the cap lifted (Appendix~\\ref{app:repro}).")
rep(B, "Scored against the PRESENT versions alone, which also hold relevant content, every reader moves by at most $0.03$ from its whole-set value, so the comparison stands where coverage is equal (post hoc; PN vs PRESENT and the wins, ties and losses per triple in Table~\\ref{tab:cf-main}).",
    "Scored against the PRESENT versions alone, which also hold relevant content, every reader moves by at most $0.03$ from its whole-set value, so the comparison stands where coverage is equal.\nTable~\\ref{tab:cf-main} gives that score and the wins, ties and losses per triple, both post hoc.")
rep(B, "Moving the obligation's own increment to a sibling version, the moved-count control, sends a count reader below chance; GPT-4.1 mini moves $+0.06$ on expiry with interval $[-0.04,+0.16]$, Haiku 4.5 stays within tolerance (Appendix~\\ref{app:counterfactual}), and Opus 5 was not run on this control.",
    "Moving the obligation's own increment to a sibling version, the moved-count control, sends a count reader below chance.\nGPT-4.1 mini moves $+0.06$ on expiry with interval $[-0.04,+0.16]$ and Haiku 4.5 stays within tolerance (Appendix~\\ref{app:counterfactual}); Opus 5 was not run on this control.")
rep(B, "Shown both, GPT-4.1 mini gains a reliable $+0.10$ over the summary alone, while Haiku 4.5 scores $0.79$ shown both against $0.82$ under its summary alone, so the combined monitor is best for GPT-4.1 mini only (Appendix~\\ref{app:resp}).",
    "Shown both, GPT-4.1 mini gains a reliable $+0.10$ over the summary alone.\nHaiku 4.5 scores $0.79$ shown both against $0.82$ under its summary alone, so the combined monitor is best for GPT-4.1 mini only (Appendix~\\ref{app:resp}).")
rep(B, "FR-Bank's tags mark $1{,}389$ of the $3{,}305$ lines shown as non-active where the ground-truth tags mark $217$, a precision of $0.14$, and GPT-4.1 mini's obligation score on that view rises from $0.69$ to a reliable $0.81$.\nThe reason is reach rather than volume: the store's tags mark $70$ of the $99$ forbidding records in view against the ground-truth tags' $60$, while a count of tagged lines scores $0.62$ under either tag source (Table~\\ref{tab:routes-full}, Appendix~\\ref{app:resp}).",
    "FR-Bank's tags mark $1{,}389$ of the $3{,}305$ lines shown as non-active where the ground-truth tags mark $217$, a precision of $0.14$.\nGPT-4.1 mini's obligation score on that view rises from $0.69$ to a reliable $0.81$.\nThe reason is reach rather than volume.\nThe store's tags mark $70$ of the $99$ forbidding records in view against the ground-truth tags' $60$, while a count of tagged lines scores $0.62$ under either tag source (Table~\\ref{tab:routes-full}, Appendix~\\ref{app:resp}).")
rep(B, "Its invalidation marks reach $13$ of the $34$ obligations of the full store that the ground truth marks superseded or expired, more than the quarter we had predicted, and $54$ of its $807$ non-active edges fall on such a record (Appendix~\\ref{app:posthoc-graphiti}).",
    "Its invalidation marks reach $13$ of the $34$ obligations of the full store that the ground truth marks superseded or expired, more than the quarter we had predicted.\nOf its $807$ non-active edges, $54$ fall on such a record (Appendix~\\ref{app:posthoc-graphiti}).")
rep(B, "Tags in view are respected: the detector flags GPT-4.1 mini on $0$ of the $50$ views where every stale line is tagged or absent, and each of its $16$ flagged answers under the oracle falls on a view with an untagged duplicate.",
    "Tags in view are respected: the detector flags GPT-4.1 mini on $0$ of the $50$ views where every stale line is tagged or absent.\nEach of its $16$ flagged answers under the oracle falls on a view with an untagged duplicate.")
rep(B, "The ground-truth tags come from an alignment of the manifests to the stored records that marks the forbidding record for $82$ of the $104$ obligations; the duplicate retagging used the obligations' reference information, so it is diagnostic, and the detector that flags stale answers awaits its human validation.",
    "The ground-truth tags come from an alignment of the manifests to the stored records that marks the forbidding record for $82$ of the $104$ obligations.\nThe duplicate retagging used the obligations' reference information, so it is diagnostic, and the detector that flags stale answers awaits its human validation.")

# ---- the alias label through a preamble macro (the token scan skips the preamble; a label is not prose)
rep(B, "\\newcommand{\\believed}{\\textsc{believed}}", "\\newcommand{\\believed}{\\textsc{believed}}\n%% R112 (2026-09-16), review-2 F6: the frozen DS paragraph of Appendix E.10 refers to the census table by its pre-R111 label; the alias is issued on Table tab:census through this macro, so no registered byte changes.\n\\newcommand{\\censusalias}{\\label{tab:believed}}")
rep(B, "\\label{tab:census}\\label{tab:believed}%% R112 (2026-09-16): alias for the frozen DS paragraph's reference in Appendix E.10 (review-2 F6); no registered byte changes",
    "\\label{tab:census}\\censusalias%% R112 (2026-09-16): the alias label for the frozen DS paragraph's reference in Appendix E.10 (review-2 F6)")

# ---- the quoted P1 text ships verbatim
rep(X, "Its outcome text, quoted verbatim with the artifact's names (Appendix~\\ref{app:glossary}), reads:",
    "%% The registered P1 outcome text as r85_graphiti/NUMBERS_R85.md AUX-R85-G10-CENSUS-FORBIDDING filled it; the registration's wording ships verbatim.\nIts outcome text, quoted verbatim with the artifact's names (Appendix~\\ref{app:glossary}), reads:")


def main():
    files = {p: p.read_text(encoding="utf-8") for p in (A, B, X)}
    for f, old, new in E:
        n = files[f].count(old)
        if n != 1:
            print(f"ABORT {f.name}: {n} of {old[:120]!r}"); sys.exit(1)
        files[f] = files[f].replace(old, new)
    for p, t in files.items():
        p.write_text(t, encoding="utf-8", newline="\n")
    print(f"applied {len(E)}")


if __name__ == "__main__":
    main()
