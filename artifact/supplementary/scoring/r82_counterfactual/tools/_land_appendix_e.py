r"""_land_appendix_e.py -- rewrite the Appendix E ledger items in two parts.

WHAT CHANGES. Each of the twelve numbered records and the preventive record is split into
"What went wrong" and "What we changed". The word "instrument" is replaced by "measurement
step" in the item bodies and in the section preamble.

WHAT DOES NOT CHANGE, deliberately:

  The section HEADING keeps the word "instrument". appendix_identity keys each section by its
  heading text, so renaming it reports the section as one REMOVED plus one ADDED rather than
  one CHANGED, and every report and CLAIMS entry that names "the instrument ledger" in prose
  would drift out of step with the manuscript. The rewrite asked for the substitution inside
  each ledger item, and that is the scope taken here. Renaming the heading is a separate,
  larger decision.

  The COUNT. Twelve numbered records plus one preventive, exactly as CLAIMS.md C119 records
  the composition. No item is added, merged or dropped.

  Every NUMBER and every claim comment marker (C109 through C119, AUX-E1R-NB3). The splits are
  presentational: each item says what it said, in two labelled halves.

  The C120 closing sentence and the R83 pattern paragraph after it.

The pattern paragraph added in R83 is left where it is, after C120, because it is about this
manuscript's verification battery rather than about a monitoring measurement step, and the
section preamble scopes the numbered list to the latter.

Idempotent. Anchors asserted, never guessed.
"""
import io
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
TEX = ROOT / "iclr2027_monitoring_submission" / "paper_v2.tex"
NL = "\r\n"

WW = r"\textbf{What went wrong.}"
WC = r"\textbf{What we changed.}"

OLD_PREAMBLE = ("The following ledger contains only instruments germane to E0, E1, the "
                "capability ladder, the question-prior audit, and their economics; instruments "
                "outside this paper's monitoring scope are excluded.")
NEW_PREAMBLE = ("The following ledger contains only measurement steps germane to E0, E1, the "
                "capability ladder, the question-prior audit, and their economics; measurement "
                "steps outside this paper's monitoring scope are excluded.")

ITEMS = [
    ("% C109",
     r"The expiry route that ignored query intent looked mechanical and was treated as one. It reached $20\%$ precision.",
     r"\pn{} is defined conditionally on intent, which is the definition this paper uses."),
    ("% C110",
     r"The half of \pn{} labeling that looked mechanical reached $69$--$86\%$ precision under spot check.",
     r"Every candidate receives human verification, and no part of the label is taken as mechanical."),
    ("% C111",
     r"The pilot's monitor prompt asserted lifecycle structure that two of the three backends do not expose, so it stated something false to them.",
     r"The prompt was rebuilt before the main study, which is why pilot and main-study values are not comparable."),
    ("% C112",
     r"Lexical presence recall was $0.697$, low enough that every \absent{} label rested on a weak check.",
     r"A two-channel replacement reached $0.995$, so its miss rate on present targets is $\varepsilon=0.005$. That is a conditional rate and not the error rate of an absence claim; the posterior, which also needs the base rate, is given in Section~\ref{sec:calibration}."),
    ("% C113",
     r"Wall-clock ingestion time would have converted a measurement-step error into a lifecycle claim.",
     r"A proper recency time was added."),
    ("% C114",
     r"The probe screen fired on every content word.",
     r"It was replaced by a corpus-measured filter."),
    ("% C115",
     r"Only $3/300$ sol cells and $1/300$ luna cells reproduced across five draws.",
     r"The $k=5$ frontier protocol followed."),
    ("% C116",
     r"A frontier conclusion had already been drafted when that redraw ran.",
     r"The preregistered redraw reversed it before distribution."),
    ("% C117",
     r"The frontier provider/API's ``tokens used'' field reports a turn total rather than output telemetry.",
     r"Exact frontier economics are not reported."),
    ("% C118",
     r"An import-shadowing bug wrote this study's usage records into another study's cache.",
     r"It is disclosed here rather than repaired retrospectively."),
    ("",
     r"A label-supervised question-only probe exposed generator-specific template signal.",
     r"The powered matched slice is reported as a second population rather than as prior-controlled evidence."),
    ("% AUX-E1R-NB3",
     r"A term-frequency index-reader baseline (NB-3), frozen for the offline robustness pass with the question concatenated to the index text, read the question rather than the store. Its index-only ablation sits near chance while its question-only ablation exceeds the concatenated score on every population.",
     r"NB-3 was disqualified as an index reader and is retained as a measurement-step failure record."),
]

PREVENTIVE = (r"\item[Preventive.] % C119",
              r"The generic frontier-family model string routed server-side to the top tier.",
              r"Exact model-identifier verification caught the mismatch before any call.")


def build():
    out = [r"\begin{enumerate}"]
    for marker, wrong, changed in ITEMS:
        out.append((r"\item " + marker).rstrip())
        out.append("%s %s %s %s" % (WW, wrong, WC, changed))
    out.append(PREVENTIVE[0])
    out.append("%s %s %s %s" % (WW, PREVENTIVE[1], WC, PREVENTIVE[2]))
    out.append(r"\end{enumerate}")
    return NL.join(out)


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()
    if WW in s:
        print("_land_appendix_e: already landed")
        return 0
    if OLD_PREAMBLE not in s:
        print("ABORT: Appendix E preamble anchor not found; nothing written")
        return 1
    s = s.replace(OLD_PREAMBLE, NEW_PREAMBLE, 1)

    start = s.index(r"\begin{enumerate}", s.index(NEW_PREAMBLE))
    end = s.index(r"\end{enumerate}", start) + len(r"\end{enumerate}")
    s = s[:start] + build() + s[end:]

    io.open(TEX, "w", encoding="utf-8", newline="").write(s)
    print("_land_appendix_e: 12 records plus the preventive rewritten in two parts")
    print("  next: latexmk, then appendix_identity for the pin, then the battery")
    return 0


sys.exit(main())
