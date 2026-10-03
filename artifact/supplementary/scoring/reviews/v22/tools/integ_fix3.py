# -*- coding: utf-8 -*-
"""integ_fix3.py -- the author's four fixes after reading the integrated build (2026-09-16, evening; program R112): (1) the count claim
stated as weaker discrimination, not none (Opus 5 reads 0.5689 / 0.6128 PN-vs-PRESENT on retraction / expiry with persona intervals above
0.50); (2) the opening example names the cancelled plan as the forbidding record, the cancellation as the evidence that marks it; (3) the
tag recommendation narrowed to keeping tagged non-active records reachable for the obligation judgment, unmasked retrieval's effect on
final answers untested; (4) Figure 3's legend no longer clipped, the Graphiti table's paragraph columns ragged right. Asserted replacements.
Run from the repository root: python reviews/v19/tools/integ_fix3.py
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


# (1) the count claim
rep(A, "The attribute names carry most of the observed signal; the count interventions do not establish consistent count use. Where the summary names the stale attribute, a similarity lookup over the list matches every model but the largest (three models; one question, three store versions). Where the summary only counts a state, no tested model separates the versions, and naming the state lifts every model.",
    "The attribute names carry most of the observed signal. Where the summary names the stale attribute, a similarity lookup over the list matches every model but the largest (three models; one question, three store versions). Where the summary only counts a state, every model discriminates more weakly, naming that state lifts it, and the count interventions do not establish consistent count use.")
rep(B, "The retracted and expired states are recoverable from the count table, but no tested model recovers them.",
    "The retracted and expired states are recoverable from the count table, and every tested model separates them more weakly than a count reader does.")
rep(B, "On the state the summary names the lookup and the models are high together; on the states it only counts, the count reader separates the versions and no model does, and naming those states lifts every reader.}",
    "On the state the summary names the lookup and the models are high together; on the states it only counts, every model discriminates more weakly than the count reader, and naming those states lifts every reader.}")
rep(B, "\\legend{lookup (name; all-states), GPT-4.1 mini, Haiku 4.5, Opus 5, count reader (category-aware, left panel)}",
    "\\legend{lookup (name; all-states), GPT-4.1 mini, Haiku 4.5, Opus 5, count reader (left)}")
# (2) the opening example
rep(B, "We call the cancellation a \\emph{forbidding record}: a non-active record whose use would make the answer wrong.",
    "We call the cancelled plan a \\emph{forbidding record}, a non-active record whose use would make the answer wrong; the cancellation is the evidence that marks it.")
# (3) the tag recommendation
rep(A, "Backends should return tags, not masks, and maintain the list.",
    "Backends should keep tagged non-active records reachable for the obligation judgment, and maintain the list.")
rep(B, "Return non-active records with their lifecycle tags instead of masking them; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags (Section~\\ref{sec:routes}).",
    "Keep non-active records reachable with their lifecycle tags for the obligation judgment; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags, and whether unmasked retrieval also improves final answers is untested (Section~\\ref{sec:routes}).")
# (4) the Graphiti table's paragraph columns ragged right
rep(X, "\\begin{tabular}{@{}p{0.28\\linewidth}rrrrp{0.19\\linewidth}p{0.12\\linewidth}@{}}",
    "\\begin{tabular}{@{}>{\\raggedright\\arraybackslash}p{0.28\\linewidth}rrrr>{\\raggedright\\arraybackslash}p{0.19\\linewidth}>{\\raggedright\\arraybackslash}p{0.12\\linewidth}@{}}")


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
