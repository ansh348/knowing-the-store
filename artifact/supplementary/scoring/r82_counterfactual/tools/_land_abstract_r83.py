r"""_land_abstract_r83.py -- land the user's reframed abstract.

SUPERSEDES the abstract half of _pass7_proposal.py. That proposal fixed what the gates
flagged; this fixes what a reader stumbles on. Change 1 of the proposal, the Section 1
duplicate fix, is separate and stays.

WHAT THE USER'S VERSION DOES THAT THE PROPOSAL DID NOT:

  - "The summary is doing the work." no longer stands alone. Splitting sentence 5 at its
    colon fixed the 44-word gate item and left that idiom as its own sentence, with more
    emphasis than it had inside the longer one, not less.
  - "the paired obligation gain is positive" and "On that row it falls to a matcher's level"
    are both gone. Those were the two sentences the abstract needed to lose.
  - The truthful result is stated and immediately bounded, and the boundary is the finding:
    sentence 5 states the lookup result and the naming bound together, and sentence 6 gives
    the named-versus-counted split with its two numbers.

ELEVEN SENTENCES, inside STYLE_SPEC S6's 9-to-11 band. None over 40 words. No em dashes
(S8). No "not X but Y" (S9).

U9. The retention figure and the text-match result sit in ADJACENT sentences, 8 and 9, never
in one. That is the arrangement CLAIMS.md:202 permits and u9_scan enforces.

TWO CHECKS THE USER ASKED FOR BEFORE LANDING:

  1. AUTHORITY FOR "bounded by what it names" (sentence 5). This restates the
     naming-granularity claim, SCOPELIMIT-R81-1, which the manuscript already carries in
     Section 6: "The index names superseded content and only counts retracted and expired
     content". Recorded in CLAIMS.md rather than left implicit.

  2. CENSUS. The new abstract is longer. Measured before landing; if it tips, sentence 2 is
     the one to trim.

NUMBERS. 0.5656 and 0.8489 are promoted from Section 7.1 into the abstract. Both are
ledgered in NUMBERS_R82 section 7 and both already print in main text, so this is emphasis,
which CLAIMS.md permits, and not a new measurement. 42.3% is unchanged.

Idempotent.
"""
import io
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
TEX = ROOT / "iclr2027_monitoring_submission" / "paper_v2.tex"
NL = "\r\n"

ABSTRACT = NL.join([
    r"An agent with persistent external memory must judge, before retrieval, whether its store covers a question and whether it holds anything that must not be used, as when a hiking plan outlives its cancellation.",
    r"We define and measure both judgments, feeling of knowing (FOK) and negative-obligation knowledge (NOK), before any retrieval, against deterministic labels on constructed stores.",
    r"Similarity retrieval cannot settle the second in principle, because the record that forbids use can rank below the cutoff, so the monitor needs the store's own self-description.",
    r"Given a truthful summary of store metadata with every value removed, the obligation judgment improves on all six models we test across three vendors.",
    r"A lookup over the names the summary marks superseded performs as well as the smallest of them, and what the summary transmits is bounded by what it names.",
    r"On a set where the question cannot carry the label, the state the summary names is judged better than the states it only counts, and naming those states lifts the judgment on them from $0.5656$ to $0.8489$.",
    r"No backend we tested writes such a summary.",
    r"Under the metadata real systems expose, coverage judgment keeps all of its gain and obligation judgment keeps $42.3\%$.",
    r"There the model does no better than a text match against the summary.",
    r"A self-description without lifecycle structure makes judgments worse at every model size tested.",
    r"Scale improves what a model guesses from the question; what a store exposes about itself supplies its obligations.",
])

# sentence 2 is the trim target if the census tips
TRIM_OLD = ("We define and measure both judgments, feeling of knowing (FOK) and "
            "negative-obligation knowledge (NOK), before any retrieval, against deterministic "
            "labels on constructed stores.")
TRIM_NEW = ("We define and measure both judgments, feeling of knowing (FOK) and "
            "negative-obligation knowledge (NOK), against deterministic labels on constructed "
            "stores.")


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()
    if "what the summary transmits is bounded by what it names" in s:
        print("_land_abstract_r83: already landed")
        return 0
    a = s.index(r"\begin{abstract}") + len(r"\begin{abstract}")
    b = s.index(r"\end{abstract}")
    old = s[a:b]
    new = NL + ABSTRACT + NL
    if "--trim" in sys.argv:
        new = new.replace(TRIM_OLD, TRIM_NEW, 1)
        print("  sentence 2 trimmed (census relief)")
    s = s[:a] + new + s[b:]
    io.open(TEX, "w", encoding="utf-8", newline="").write(s)
    print("_land_abstract_r83: abstract replaced, %+d characters, %d sentences"
          % (len(new) - len(old), len(ABSTRACT.split(NL))))
    return 0


sys.exit(main())
