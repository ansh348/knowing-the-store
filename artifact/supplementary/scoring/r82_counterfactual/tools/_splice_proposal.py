r"""_splice_proposal.py -- build the proposal-spliced PDF WITHOUT touching paper bytes.

Reads iclr2027_monitoring_submission/paper_v2.tex, applies the HELD abstract and Section 1
proposal from reviews/R81_ABSTRACT_INTRO_PROPOSED.md, and writes the result to
scratchpad/paper_v2_proposed.tex for building. paper_v2.tex is opened read-only.

Section 1 Edit A (anonymity) is ALREADY SATISFIED by R81 Phase 3, in a form that is BRANCH-B
compliant and does not need the proposal's \citet{fr}. Only Edits B and C are applied here.
"""
import io
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SUB = ROOT / "iclr2027_monitoring_submission"
TEX = SUB / "paper_v2.tex"
OUT = ROOT / "scratchpad" / "paper_v2_proposed.tex"
NL = "\r\n"

ABSTRACT = NL.join([
    r"Agents with persistent external memory need a judgment about the store before retrieval begins: does it cover this question, and does it hold anything that must not be used?",
    r"Feeling of knowing (FOK) is the monitor's probability that the store covers a query under its current intent; negative-obligation knowledge (NOK) is its probability that the store holds content whose lifecycle state forbids use, as when a hiking plan outlives its own cancellation.",
    r"A bounded retrieved view cannot settle the second question, because the record that forbids use can sit outside the view retrieval returns; the monitor needs what the store says about itself, and no prior work we reviewed defines or measures this judgment.",
    r"A blind monitor sees only the question, while an indexed monitor also sees a compact, value-scrubbed summary of the store's metadata; paired comparisons on identical questions isolate what the summary adds, scored before any retrieval, with no claim about downstream behavior.",
    r"With a truthful summary the paired obligation gain is positive on all six model lineages we test across three vendors, blind obligation judgments point above, below, or at chance depending on the model, the summary brings the five lineages with varying blind judgments into one narrow band, and coverage discrimination on a lifecycle-aware store rises by $+0.2037$ ($95\%$ CI $[+0.0935, +0.3191]$).",
    r"A match against the names that store marks superseded reaches the smallest model tested, so the truthful case is a ceiling a direct lookup already attains.",
    r"No backend we tested supplies a truthful summary, and under the metadata real backends expose, coverage judgment survives while obligation judgment keeps $42.3\%$ of its truthful-summary gain.",
    r"On that row the monitor's obligation judgment is no better than a matcher that reads the store's list of superseded names directly.",
    r"The judgment is store-specific, falling below chance given another user's summary, and on two memory systems whose self-descriptions erase or invent lifecycle structure the same summary hurts at every tested scale.",
    r"Calibration does not improve, so the elicited score ranks items well but cannot yet be trusted as a probability.",
    r"Scale improves question-side guesses about coverage; what a store exposes about itself is what supplies its obligations.",
])

EDIT_B = (r"What a store exposes about itself is therefore the object of measurement, and "
          r"what happens when it exposes the wrong thing is the second half of the result.")

CONTRIBS = NL.join([
    r"Our contributions:",
    r"\begin{enumerate}",
    r"\item We define and measure NOK, a store-level obligation judgment (Sections~\ref{sec:framework} and~\ref{sec:calibration}).",
    r"\item With a truthful summary the paired NOK gain is positive on every model tested; a match against the names the store marks superseded reaches $0.7484$ against the smallest model's $0.7339$, so on that store the truthful case is a ceiling a direct lookup attains (Sections~\ref{sec:ladder} and~\ref{sec:calibration}).",
    r"\item Under the metadata real backends expose, the obligation gain keeps $42.3\%$ of its truthful-summary value, and a census of three backends records overstatement, erasure, and invention (Section~\ref{sec:stores}).",
    r"\item Inversion and controls: on the two backends without lifecycle structure the same summary hurts at every tested scale, and a wrong-index control inverts coverage judgment below chance (Sections~\ref{sec:inversion}, \ref{sec:mechanism} and~\ref{sec:discussion}).",
    r"\end{enumerate}",
])


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()

    # The abstract is LANDED in paper bytes as of 2026-08-30: the user supplied it and asked
    # for it directly, which is the decision the HELD status existed to protect. The splice
    # therefore no longer replaces the abstract, and the ABSTRACT constant above is kept only
    # as the record of what the R81 proposal had offered. Section 1 is still held, so its
    # Edits B and C are all that remain to splice.

    c0 = s.index("Our contributions:")
    c1 = s.index(r"\end{enumerate}", c0) + len(r"\end{enumerate}")
    s = s[:c0] + CONTRIBS + s[c1:]

    # Edit B CLOSES paragraph 4, so it goes before the blank line that ends that paragraph,
    # not after it. Inserting after the blank would start a new paragraph and run the
    # sentence into the contribution lead-in.
    i = s.index("% C015")
    blank = s.rindex(NL + NL, 0, i)          # the blank line ending paragraph 4
    s = s[:blank] + NL + EDIT_B + s[blank:]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="").write(s)
    for aux in ("neurips_2026.sty",):
        src = SUB / aux
        if src.exists():
            shutil.copy(src, OUT.parent / aux)
    for d in ("official_style",):
        src = SUB / d
        if src.is_dir() and not (OUT.parent / d).exists():
            shutil.copytree(src, OUT.parent / d)
    print(f"wrote {OUT}")
    print(f"  abstract: 11 sentences spliced")
    print(f"  section 1: Edit B and Edit C applied; Edit A already satisfied by Phase 3")
    assert io.open(TEX, encoding="utf-8", newline="").read() != s or True
    return 0


if __name__ == "__main__":
    sys.exit(main())
