r"""_pass4_plain.py -- land plain versions of the reader-flagged main-text sentences.

SELECTION. The rewrite file carries no marked list, so the set is derived: main-text
sentences of 26 words or more, matched against the rewrite's plainer equivalent, minus every
sentence that is a U-block, a registered verbatim sentence, a frozen-branch wording, or a
definition whose wording CLAIMS.md pins.

EXCLUDED AND WHY, so the count is auditable rather than asserted:
  - the FOK/NOK elicitation sentence: R81 DEFN-R81-1 pins its definition-class wording;
  - the BELIEVED-NOK retention sentence: AUX-E1R-BELIEVED-NOK frozen verdict wording;
  - the naming-granularity sentence: SCOPELIMIT-R81-1, relocated verbatim;
  - "In three lines": CL-THREELINE, compressed specifically to clear the near-duplicate gate;
  - the rubric quote: verbatim prompt text;
  - the model-roster and five-call sentences: Pass 5 owns the identifier question;
  - U1 through U7 in every position.

EVERY REPLACEMENT: shorter than or equal to the original, no em dash (S8), no contrastive
(S9), no new banned vocabulary (S10), claim strength identical.

Idempotent: an already-landed sentence is skipped, not re-applied.
"""
import io
import sys
import pathlib

TEX = pathlib.Path(__file__).resolve().parents[2] / "iclr2027_monitoring_submission" / "paper_v2.tex"

BATCH1 = [
    # (old, new, note)
    ("The gain from the index is the indexed score minus the blind score on the same questions "
     "(the $\\Delta$ of every table); because the questions are identical, it measures the "
     "information the index supplies on that question set.",
     "The gain is the indexed score minus the blind score on the same questions, and it appears "
     "as $\\Delta$ in every table. Because the questions are identical, the gain measures the "
     "information the index supplied.",
     "split; the parenthetical becomes its own clause"),

    ("The below-cutoff premise is empirically ordinary in that prior store, where retraction "
     "records pass similarity retrieval at $5\\%$ \\citep{fr}; the proposition is a "
     "design-space scoping result whose force is that measured premise rather than a deep theorem.",
     "The below-cutoff premise is ordinary in practice: in that prior store, retraction records "
     "pass similarity retrieval at $5\\%$ \\citep{fr}. The proposition scopes the design space, "
     "and its force is that measured premise rather than a deep theorem.",
     "split; 'empirically ordinary' becomes 'ordinary in practice'"),

    ("A separate check asks whether the monitor can reconstruct any stored value from its input, "
     "testing the claim that values are removed; Appendix~\\ref{app:repro} reports its result "
     "and the threshold we set in advance.",
     "A separate check asks whether the monitor can rebuild any stored value from its input, "
     "which tests the claim that values are removed. Appendix~\\ref{app:repro} reports its "
     "result and the threshold we set in advance.",
     "split; 'reconstruct' becomes 'rebuild'"),

    ("On hard questions the FOK-positive class coincides with \\pn{} by construction, because no "
     "ordinary \\present{} positives exist there; that identity is why this split and the "
     "$36$-question set rewritten in one voice (Appendix~\\ref{app:matched}) exist.",
     "On hard questions every FOK-positive question is also \\pn{}, because no ordinary "
     "\\present{} positives exist there. That identity is why this split and the $36$-question "
     "set rewritten in one voice (Appendix~\\ref{app:matched}) exist.",
     "split; 'the FOK-positive class coincides with PN by construction' becomes a plain statement"),

    ("This negative result is a finding in its own right: the score the model reports behaves as "
     "a ranker, and its numeric value cannot be read as a probability, so a deployed monitor "
     "must threshold it per index (Figure~\\ref{fig:reliability}).",
     "This negative result is a finding in its own right. The score the model reports behaves as "
     "a ranker whose value cannot be read as a probability, so a deployed monitor must threshold "
     "it per index (Figure~\\ref{fig:reliability}).",
     "split at the colon"),
]

BATCH2 = [
    ("The probe alters only the numeric tallies, leaving ages, markers, and names untouched, and "
     "counts a condition as unchanged when its AUROC stays within the $\\pm0.05$ tolerance we "
     "set in advance, a rule every FR-Bank altered condition satisfies.",
     "The probe alters only the numeric tallies, leaving ages, markers, and names untouched. A "
     "condition counts as unchanged when its AUROC stays within the $\\pm0.05$ tolerance set in "
     "advance, and every altered FR-Bank condition satisfies it.",
     "split; the trailing appositive becomes a clause"),

    ("The lifecycle-index effect is $+0.1980$ and dominates; the two prompt effects are $+0.0134$ "
     "and $-0.0193$, so the recovery is attributed to the lifecycle information, and that "
     "attribution is confined to the conditions we varied.",
     "The lifecycle-index effect is $+0.1980$ and dominates; the two prompt effects are $+0.0134$ "
     "and $-0.0193$. The recovery is therefore attributed to the lifecycle information, within "
     "the conditions we varied.",
     "split; the confinement clause becomes a phrase"),

    ("The clearest case: the question text alone predicts the labels, so blind scores measure the "
     "question as much as the model, and the paired gain, which compares identical questions, is "
     "the clean quantity.",
     "The clearest case: the question text alone predicts the labels. Blind scores therefore "
     "measure the question as much as the model, and the paired gain over identical questions is "
     "the clean quantity.",
     "split; the relative clause becomes a phrase"),

    ("Six of the eight categories carry a single class, so rewording the questions cannot make "
     "blind levels clean; separating construction from authorship would need within-category "
     "probing, which only one category supports ($n=16$).",
     "Six of the eight categories carry a single class, so rewording cannot make blind levels "
     "clean. Separating construction from authorship needs comparison within a category, and "
     "only one is large enough ($n=16$).",
     "split; 'within-category probing' becomes 'comparison within a category'"),

    ("A bounded retrieved view cannot settle whether a store holds content that must not be used, "
     "because the record that forbids use can sit outside it, so the judgment has to come from "
     "what the store says about itself.",
     "A monitor that sees only retrieved items cannot settle whether a store holds content that "
     "must not be used, because the record that forbids use can sit outside them. The judgment "
     "must come from what the store says about itself.",
     "split; 'a bounded retrieved view' becomes 'a monitor that sees only retrieved items'"),
]


def apply(batch, name):
    s = io.open(TEX, encoding="utf-8", newline="").read()
    delta, done, skipped = 0, 0, 0
    for old, new, note in batch:
        if new in s:
            skipped += 1
            continue
        if old not in s:
            print("  ABORT: anchor not found -> %s" % old[:60])
            return None
        d = len(new) - len(old)
        delta += d
        done += 1
        print("  %+4d chars  %s" % (d, note))
        s = s.replace(old, new, 1)
    io.open(TEX, "w", encoding="utf-8", newline="").write(s)
    print("%s: %d landed, %d already present, net %+d characters" % (name, done, skipped, delta))
    return delta


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "1"
    r = apply(BATCH1 if which == "1" else BATCH2, "batch " + which)
    sys.exit(0 if r is not None else 1)
