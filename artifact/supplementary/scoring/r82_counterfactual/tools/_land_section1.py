r"""_land_section1.py -- land the HELD Section 1 proposal into paper bytes.

_land_abstract.py landed the abstract and left Section 1 held, because the user had not
supplied it. The user has now ruled: land the full Section 1.

WHAT LANDS. The R81 proposal exactly as it stands in reviews/R81_ABSTRACT_INTRO_PROPOSED.md
(and mirrored in the generated scratchpad/paper_v2_proposed.tex), with ONE wording change,
described below.

  1. One sentence inserted after the novelty sentence, closing paragraph 4 on the object of
     measurement.
  2. Contribution bullets 2, 3 and 4 replaced.

THE ONE WORDING CHANGE (user ruling). The proposal's bullet 2 ended:

    ..., so on that store the truthful case is a ceiling a direct lookup attains

The user ruled that this clause be replaced by the abstract's formulation rather than
deleted: a lookup on the superseded-names list matches the smallest model tested. Landing the
clause literally in place would have restated the first half of its own sentence, which
already gives 0.7484 against 0.7339 in words. The bullet is therefore reordered so the claim
leads and the two numbers support it once:

    With a truthful summary the paired NOK gain is positive on every model tested, and a
    lookup on the superseded-names list matches the smallest model tested, 0.7484 against
    0.7339.

Same claim, same two numbers, same direction, and it satisfies STYLE_SPEC S1 (claim first,
evidence second). If a literal swap is preferred instead, replace NEW_B2 below with the
proposal's sentence and substitute only the trailing clause; the rest of this script is
unaffected.

CLAIM BOOKKEEPING. The outgoing bullet 2 previewed 0.3307 and 0.0389 (the blind-span
collapse). Those figures are NOT dropped from the paper: Section 5.2 continues to print
"the blind spread of 0.3307 contracts to 0.0389". CLAIMS.md requires each claim to appear at
identical strength somewhere in paper_v2, not in a fixed location, and CL-C015 is the
contributions list whose reordering the R78 order already authorises. The outgoing bullet 3's
"design law" phrasing goes with it, which is the direction R81 REFRAME 5 already took in
Section 6.

PAGE COST, measured before landing rather than after. Section 1 sits one page break away from
tipping: adding one word costs nothing, adding eight words costs 18 review lines, and every
further addition inside Section 1 is then free. The census moves 460 -> 478 against a
boundary of 485. This is a cascade (24 of 53 labels shift exactly one page, triggered at
Definition 3 and Table 1 on pages 3-4), not the intrinsic length of the new prose. Trimming
the clause was measured and buys zero.

Idempotent. Anchors are asserted, never guessed; a missing anchor is reported and the file is
left untouched.
"""
import io
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
TEX = ROOT / "iclr2027_monitoring_submission" / "paper_v2.tex"
NL = "\r\n"

ANCHOR = ("To our knowledge, this is the first direct measurement of store-level metamemory, "
          "and no prior work we reviewed defines or measures NOK.")

NEW_SENTENCE = ("What a store exposes about itself is therefore the object of measurement, "
                "and what happens when it exposes the wrong thing is the second half of the result.")

OLD_BULLETS = NL.join([
    r"\item Across six model lineages from three vendors, a compact lifecycle index yields a positive paired NOK gain on every lineage and collapses a $0.3307$ blind span to $0.0389$ (Section~\ref{sec:ladder}).",
    r"\item A store self-description audit yields the design law: the benefit exists where the backend exposes lifecycle structure and inverts where it does not (Sections~\ref{sec:inversion} and~\ref{sec:stores}).",
    r"\item Controls and instrument lessons: a wrong-index control that inverts coverage judgment below chance, a question-prior decomposition, and an instrument ledger of measurement failures and their corrections (Sections~\ref{sec:mechanism} and~\ref{sec:discussion}).",
])

NEW_B2 = (r"\item With a truthful summary the paired NOK gain is positive on every model tested, "
          r"and a lookup on the superseded-names list matches the smallest model tested, "
          r"$0.7484$ against $0.7339$ (Sections~\ref{sec:ladder} and~\ref{sec:calibration}).")

NEW_BULLETS = NL.join([
    NEW_B2,
    r"\item Under the metadata real backends expose, the obligation gain keeps $42.3\%$ of its truthful-summary value, and a census of three backends records overstatement, erasure, and invention (Section~\ref{sec:stores}).",
    r"\item Inversion and controls: on the two backends without lifecycle structure the same summary hurts at every tested scale, and a wrong-index control inverts coverage judgment below chance (Sections~\ref{sec:inversion}, \ref{sec:mechanism} and~\ref{sec:discussion}).",
])


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()
    done = []

    if NEW_SENTENCE in s:
        done.append("sentence already present")
    else:
        if ANCHOR not in s:
            print("ABORT: novelty-sentence anchor not found; nothing written")
            return 1
        s = s.replace(ANCHOR, ANCHOR + NL + NEW_SENTENCE, 1)
        done.append("sentence inserted")

    if NEW_BULLETS in s:
        done.append("bullets already present")
    elif OLD_BULLETS in s:
        s = s.replace(OLD_BULLETS, NEW_BULLETS, 1)
        done.append("bullets 2-4 replaced")
    else:
        print("ABORT: contribution-bullet anchor not found; nothing written")
        return 1

    io.open(TEX, "w", encoding="utf-8", newline="").write(s)
    print("_land_section1: " + "; ".join(done))
    print("  next: latexmk -pdf paper_v2.tex, then the gate battery incl. page_census")
    return 0


sys.exit(main())
