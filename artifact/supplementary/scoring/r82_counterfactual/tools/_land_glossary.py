r"""_land_glossary.py -- replace Appendix F.1 with the term-mapping glossary.

WHY. The existing box defines printed terms only, in a cramped two-pair layout, and it still
carries internal vocabulary ("arm / cell", "lineage / prior") as though those were reader-facing
terms. The rewrite asks for an old-term to new-term mapping instead. Appendix pages are uncounted,
so this is the one place the expansion is free.

SOURCE OF THE MAPPING. reviews/R79_CLARITY_REPORT.md section 2 is the de-facto authority: a ~45-row
internal-term to printed-replacement table produced by the R79 plain-language pass. The rewrite's
glossary extends it rather than replacing it, so the two are merged here and the printed term leads
each row.

NO NEW TABLE NUMBERS. The replacement uses unnumbered center/tabular blocks, exactly as the box it
replaces does. Wrapping any of this in \begin{table} would renumber Tables 9 through 22 and every
report, ledger and registration that refers to them by number would silently drift.

THREE BLOCKS, not one. A plain tabular cannot break across a page, and longtable is not in the
preamble. Splitting on meaning keeps each block short enough to set without a preamble change.

AUTHORIZATION. CLAIMS.md CL-GLOSSARY marks the box as moving byte-verbatim to Appendix F under
ORDERED-MECHANICAL. Replacing its content goes beyond that relocation, so this needs both an
appendix_identity EXEMPT entry and the CLAIMS.md note this script writes alongside. No claim
changes: a glossary defines terms and states no result.

Idempotent. Anchors asserted, never guessed.
"""
import io
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
TEX = ROOT / "iclr2027_monitoring_submission" / "paper_v2.tex"
NL = "\r\n"

START = r"\subsection{Notation and study glossary}\label{app:glossary}"
END = r"% R78-INSERT(glossary)-END"

NEW = NL.join([
    START,
    r"",
    r"The paper prints one vocabulary and the artifact records another. The first two blocks define",
    r"every term the main text uses; the third maps the internal names a reader will meet in the",
    r"registrations, ledgers and row files onto the printed term, so the repository can be read",
    r"against the paper without a decoder.",
    r"",
    r"\begin{center}",
    r"\fbox{\begin{minipage}{0.97\linewidth}",
    r"\scriptsize",
    r"\textbf{The two judgments, and the label they are scored against.}\par\smallskip",
    r"\begin{tabular}{@{}p{.20\linewidth}p{.74\linewidth}@{}}",
    r"FOK & feeling of knowing: the score elicited as a probability that the store covers the query under its intent \\",
    r"NOK & negative-obligation knowledge: the score elicited as a probability that the store holds content whose lifecycle state forbids use \\",
    r"\pn{} & present-negative: the label for a query whose relevant content is present and would make the answer wrong if used \\",
    r"intent & the time frame a query asks about: \textsc{current}, \textsc{upcoming}, \textsc{past}, or \textsc{change} \\",
    r"lifecycle state & \textsc{active}, \textsc{superseded}, \textsc{expired}, or \textsc{retracted} \\",
    r"AUROC & the probability that a randomly chosen positive scores above a randomly chosen negative \\",
    r"ECE & expected calibration error: the gap between stated probabilities and observed frequencies \\",
    r"\end{tabular}",
    r"\end{minipage}}",
    r"\end{center}",
    r"",
    r"\begin{center}",
    r"\fbox{\begin{minipage}{0.97\linewidth}",
    r"\scriptsize",
    r"\textbf{Conditions, stores, and populations.}\par\smallskip",
    r"\begin{tabular}{@{}p{.20\linewidth}p{.74\linewidth}@{}}",
    r"blind / indexed & the monitor sees the question only / also sees the metadata index \\",
    r"the gain ($\Delta$) & the indexed score minus the blind score on the same questions \\",
    r"\trueidx{} / \believed{} & index built from ground truth / from the fields the backend itself exposes \\",
    r"easy / hard tier & a whole category removed / a target missing inside a populated category \\",
    r"monitor call & one pre-retrieval request returning FOK and NOK \\",
    r"FR-Bank & the lifecycle-bearing store from the prior system \\",
    r"Mem0 & a production memory layer whose \texttt{UPDATE} overwrites history \\",
    r"A-MEM & an agentic memory system organized around linked notes \\",
    r"pilot / main study & the feasibility probe / the registered study \\",
    r"mini / luna / sol & \texttt{gpt-4.1-mini} / \texttt{gpt-5.6-luna} / \texttt{gpt-5.6-sol}, in ascending size and price \\",
    r"\end{tabular}",
    r"\end{minipage}}",
    r"\end{center}",
    r"",
    r"\begin{center}",
    r"\fbox{\begin{minipage}{0.97\linewidth}",
    r"\scriptsize",
    r"\textbf{Internal names in the artifact, and the term this paper prints for each.}\par\smallskip",
    r"\begin{tabular}{@{}p{.26\linewidth}p{.68\linewidth}@{}}",
    r"E0 / E1 & the pilot / the main study \\",
    r"lineage & one model family and version \\",
    r"lane & one model scored on one question set \\",
    r"cell & a fixed question set used for one comparison \\",
    r"prior & what the question alone gives away, measured by the blind score \\",
    r"arm & one experimental condition \\",
    r"provenance & which index a row used, \trueidx{} or \believed{} \\",
    r"committed & recorded and frozen before later analysis \\",
    r"registered & preregistered, with the prediction fixed before data collection \\",
    r"NB-1 \ldots NB-6 & the six mechanical readers of the same index \\",
    r"NB-6 & the superseded-names matcher, scoring the query against the flat superseded-names list \\",
    r"cross-model cell & the matched $84$-question set \\",
    r"authorship-matched slice & the $36$-question set rewritten in one voice \\",
    r"counterfactual cell & the $90$-question set: $30$ queries asked of three versions of one store \\",
    r"count-destruction probe & the test that randomizes every count in the index \\",
    r"SWAP control & scoring the monitor against another persona's index \\",
    r"D-numbers & entries in the deviation ledgers of Appendix~\ref{app:registration} \\",
    r"\end{tabular}",
    r"\end{minipage}}",
    r"\end{center}",
    END,
])


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()
    if "Internal names in the artifact" in s:
        print("_land_glossary: already landed")
        return 0
    if START not in s or END not in s:
        print("ABORT: glossary anchors not found; nothing written")
        return 1
    a = s.index(START)
    b = s.index(END, a) + len(END)
    io.open(TEX, "w", encoding="utf-8", newline="").write(s[:a] + NEW + s[b:])
    print("_land_glossary: Appendix F.1 replaced with the three-block term mapping")
    print("  next: add the appendix_identity EXEMPT entry, then latexmk and the battery")
    return 0


sys.exit(main())
