r"""_pass7_proposal.py -- build the Pass 7 abstract proposal for approval. LANDS NOTHING.

Writes a scratch copy so the census can be measured, then leaves paper_v2.tex untouched.
Run with --apply only after the user approves.

FOUR CHANGES:

  1. The Section 1 duplicate, fixed from the SECTION 1 side as ruled. prose_scan reports an
     82% token overlap between abstract sentence 2 and Section 1's "We measure that judgment
     directly...". Both state the same thing; the abstract is the user's own text, so Section
     1 moves. Claim C011-C014 is unchanged: the judgment is still measured directly, still
     before retrieval, still against labels that are exact by construction.

  2. Abstract sentence 5 split. It runs 44 words and is the last L-gate item in the paper.
     Splitting takes the abstract from 10 sentences to 11, which is inside STYLE_SPEC S6's
     9-to-11 band.

  3. Swap A, abstract sentence 3. Adds the REASON similarity retrieval cannot settle the
     obligation, which is Proposition 1's premise and the paper's central mechanism. The
     abstract currently asserts the impossibility without saying why.

  4. Swap B, abstract sentence 9. "hurts at every model scale" becomes "makes judgments worse
     at every model size tested", which is the rewrite's wording and matches how Section 5.3
     states the same result.

No number, citation or claim changes. Sentence count 10 -> 11.
"""
import io
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
TEX = ROOT / "iclr2027_monitoring_submission" / "paper_v2.tex"
SCRATCH = ROOT / "scratchpad" / "paper_v2_p7.tex"

CHANGES = [
    ("1. Section 1 duplicate, fixed from the Section 1 side",
     "We measure that judgment directly, before any retrieval, against deterministic labels "
     "on constructed stores.",
     "We measure that judgment directly, ahead of any lookup, against labels known exactly "
     "because we built the stores."),

    ("2. Abstract sentence 5 split (44 words, the last L-gate item)",
     "The summary is doing the work: a lookup over the names it marks superseded performs as "
     "well as the smallest model we tested, and naming the states it only counts lifts them "
     "from chance on a set where the question cannot carry the label.",
     "The summary is doing the work. A lookup over the names it marks superseded performs as "
     "well as the smallest model we tested, and naming the states it only counts lifts them "
     "from chance on a set where the question cannot carry the label."),

    ("3. Swap A: the abstract asserts the impossibility without its reason",
     "Similarity retrieval cannot settle the second in principle, so the monitor needs the "
     "store's own self-description.",
     "Similarity retrieval cannot settle the second in principle, because the record that "
     "forbids use can rank below the cutoff, so the monitor needs the store's own "
     "self-description."),

    ("4. Swap B: matches how Section 5.3 states the same result",
     "A self-description without lifecycle structure hurts at every model scale.",
     "A self-description without lifecycle structure makes judgments worse at every model "
     "size tested."),
]


def build(apply):
    s = io.open(TEX, encoding="utf-8", newline="").read()
    total = 0
    for label, old, new in CHANGES:
        if new in s:
            print("  [already present] %s" % label)
            continue
        if old not in s:
            print("  ABORT: anchor not found for %s" % label)
            return 1
        total += len(new) - len(old)
        s = s.replace(old, new, 1)
        print("\n%s   (%+d chars)" % (label, len(new) - len(old)))
        print("  BEFORE: %s" % old)
        print("  AFTER : %s" % new)
    target = TEX if apply else SCRATCH
    io.open(target, "w", encoding="utf-8", newline="").write(s)
    print("\nnet %+d characters -> %s" % (total, target.name))
    print("LANDED" if apply else "NOT LANDED: paper_v2.tex is untouched")
    return 0


sys.exit(build("--apply" in sys.argv))
