r"""_land_abstract.py -- land the user's abstract into paper bytes.

The HELD status existed to protect the user's own decision about the front matter. The user
supplied this text and asked for it directly, which is that decision. Section 1 was not
supplied and stays held.

TWO MECHANICAL EDITS to the supplied text, both forced by gates the constitution already
sets, neither changing a claim:

  "cell" -> "set"   slogan_scan's S10 ban list contains \bcells?\b, so the supplied wording
                    fails a hard gate. "set" is the word the paper already uses for its
                    36-question and 90-question populations.

  sentence 7 split  The supplied sentence joined the 42.3% retention figure and the matcher
                    result with "and" inside one sentence. CLAIMS.md U9 keeps that link
                    UNdrawn and calls drawing it a VIOLATION; the R81 block permits the two
                    findings in adjacent sentences but forbids asserting that one explains
                    the other. Splitting also takes the count from 8 to 10, inside S6's
                    9-to-11 band, which the supplied text sat below.

The user's second version removed "value-scrubbed" in favour of "with every value removed",
which also clears a prose_scan VOCAB term and so removes an obstacle to dropping the HELD
carve-out at full LAND.
"""
import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
TEX = ROOT / "iclr2027_monitoring_submission" / "paper_v2.tex"
NL = "\r\n"

ABSTRACT = NL.join([
    r"An agent with persistent external memory must judge, before retrieval, whether its store covers a question and whether it holds anything that must not be used, as when a hiking plan outlives its cancellation.",
    r"We define and measure both judgments, feeling of knowing (FOK) and negative-obligation knowledge (NOK), before any retrieval, against deterministic labels on constructed stores.",
    r"Similarity retrieval cannot settle the second in principle, so the monitor needs the store's own self-description.",
    r"Given a truthful summary of store metadata with every value removed, the paired obligation gain is positive on all six models we test across three vendors.",
    r"The summary is doing the work: a lookup over the names it marks superseded performs as well as the smallest model we tested, and naming the states it only counts lifts them from chance on a set where the question cannot carry the label.",
    r"No backend we tested writes such a summary.",
    r"Under the metadata real systems expose, obligation judgment keeps $42.3\%$ of its gain.",
    r"On that row it falls to a matcher's level.",
    r"A self-description without lifecycle structure hurts at every model scale.",
    r"Scale improves what a model guesses from the question; what a store exposes about itself supplies its obligations.",
])

# Section 8's move-3 sentence restated the abstract's retention finding almost word for word
# (prose_scan measured 88%). The abstract is the user's text and keeps its wording; Section 8
# carries the same claim through the asymmetry between the two judgments, which the abstract
# does not state.
S8_OLD = ("No backend we tested supplies such a summary, and under the metadata real backends "
          "expose, coverage judgment survives while obligation judgment keeps part of its gain.")
S8_NEW = ("The two judgments part company on real metadata: coverage holds up, while "
          "obligations lose most of their benefit.")


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()
    a = s.index(r"\begin{abstract}") + len(r"\begin{abstract}")
    b = s.index(r"\end{abstract}")
    if ABSTRACT in s:
        print("abstract already landed")
    else:
        s = s[:a] + NL + ABSTRACT + NL + s[b:]
        print(f"abstract landed: {len(ABSTRACT.split(NL))} sentences")
    if S8_OLD in s:
        s = s.replace(S8_OLD, S8_NEW, 1)
        print("section 8 move 3 reworded to clear the 88% near-duplicate")
    else:
        print("section 8 already reworded")
    io.open(TEX, "w", encoding="utf-8", newline="").write(s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
