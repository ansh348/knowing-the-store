r"""_phase4_read.py -- R81 Phase 4: readability, jargon and yield edits on paper_v2.tex.

Applies the ruled items of the Phase 4 order. Idempotent: re-running reports anchors it
cannot find and changes nothing. Item 2 is NOT applied; see the STOP note in the report.
"""
# R83: anchors re-keyed from heading TEXT to \label{}. Retitling Appendix H broke
# _r82_int's guard because it keyed on the title; a heading is an identity key for prose,
# exemption tables AND splicer anchors, and only the label survives a rename.
import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
TEX = ROOT / "iclr2027_monitoring_submission" / "paper_v2.tex"
PROSE = ROOT / "iclr2027_monitoring_submission" / "tools" / "prose_scan.py"

NL = "\r\n"

U2 = ("Scope: the negative index effect is measured; the single-channel ablations do not "
      "identify its cause.")

EDITS = [
    # ---- item 1: three paragraphs in 4.3. Two breaks added, one removed. No new sentence.
    ("The obligation judgment behaves differently.",
     "" + NL + "The obligation judgment behaves differently."),
    ("% C051" + NL + "Splitting the negatives by kind narrows the claim.",
     "" + NL + "% C051" + NL + "Splitting the negatives by kind narrows the claim."),
    # remove the pre-existing break so retention and calibration join the third paragraph
    ("this is a descriptive comparison, and we ran no equivalence test." + NL + NL + "% C054",
     "this is a descriptive comparison, and we ran no equivalence test." + NL + "% C054"),

    # ---- item 3: precision on what a hard question targets
    ("hard questions target stores whose category stays populated.",
     "hard questions target a record whose category stays populated."),

    # ---- item 4: the reader count reads as six throughout
    ("A sixth reader, NB-3, was disqualified before scoring",
     "One of the six, NB-3, was disqualified before scoring"),

    # ---- item 5: an antecedent for the relocated U4. U4's own bytes are untouched.
    ("The inversion table collects the backend and model rows behind the cross-scale claim.",
     "The inversion table collects the backend and model rows behind the cross-scale claim."
     + NL + "Section~\\ref{sec:stores} reads one generalization from them: the benefit "
     "appears on the backend that carries lifecycle structure and inverts on the two "
     "that do not."),

    # ---- item 6: the footnote says what it means
    ("The mini $\\Delta$ interval cells print --- because",
     "The mini $\\Delta$ interval cells print a dash because"),

    # ---- item 10: U2 moves verbatim to the appendix; main text gets plain words
    ("% U2 below is byte-identical, including its Scope: label (whitelisted in prose_scan; "
     "listed in the R79 report)" + NL + U2,
     "% U2 RELOCATED 2026-08-30 to Appendix F (index-channel probe, inside the L1249-1294"
     + NL + "% range CLAIMS.md labels F.6) under the U-BLOCK RELOCATIONS ruling. Byte-identical"
     + NL + "% there, still exactly once in the document. Plain replacement at equal strength:"
     + NL + "The negative index effect is measured here, and these ablations do not identify "
     "what causes it."),
    ("\\label{app:factorial}",
     "% U2 (CLAIMS.md untouchable, byte-identical), relocated from Section 5.3 under the"
     + NL + "% R81 U-BLOCK RELOCATIONS ruling. Placed in the index-channel probe because that is"
     + NL + "% where the single-channel ablations it scopes are reported."
     + NL + U2 + NL + NL + "\\label{app:factorial}"),

    # ---- item 11: economics cut to one sentence, moved to 7.2
    ("Monitoring runs before every query, so its cost turns on prompt caching." + NL
     + "The projected and the billed arithmetic disagree about which monitor is cheaper: the "
     "list-price projection favors the indexed mini monitor, and a small run at actual billed "
     "prices reverses that ordering." + NL
     + "Appendix~\\ref{app:economics} records both orderings, the telemetry behind them, and "
     "the reasons they differ.",
     "% ECONOMICS RELOCATED 2026-08-30 to Section 7.2 as one sentence (Phase 4 item 11)."),
    ("% C150" + NL + "Whether acting on these judgments improves retrieval or answering is "
     "not measured here.",
     "% C150" + NL + "The projected and the billed cost arithmetic disagree about which "
     "monitor is cheaper, and Appendix~\\ref{app:economics} records both orderings with the "
     "telemetry behind them." + NL
     + "Whether acting on these judgments improves retrieval or answering is not measured "
     "here."),

    # ---- item 12: the Remark pointer leaves main text
    ("% C038" + NL + "Appendix~\\ref{app:proofs} states and proves Remark~\\ref{prop:scalar}, "
     "a motivating impossibility for region-conditioned trust rather than a claimed "
     "contribution." + NL, "% C038 pointer cut from main text (Phase 4 item 12); the remark "
     "stands in Appendix A." + NL),
]

# ---- item 9: ban-list extension, with the instrument carve-out
PROSE_OLD = '    r"\\bstaircase\\b",'
PROSE_NEW = ('    r"\\bstaircase\\b",\n'
             '    # R81 Phase 4 item 9: Reframe 5 bars these as CLAIM words in main text.\n'
             '    # Section 7.1 may use "instrument"; that is a different sense and is not listed.\n'
             '    r"\\bdesign law\\b", r"\\blaws?\\b", r"\\bprecondition\\b",')


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()
    before, applied, missing = s, 0, []
    for old, new in EDITS:
        if old not in s:
            missing.append(old.replace(NL, " | ")[:72])
            continue
        s = s.replace(old, new, 1)
        applied += 1
    if s != before:
        io.open(TEX, "w", encoding="utf-8", newline="").write(s)
    for m in missing:
        print("  NOT FOUND:", m)
    print(f"paper_v2.tex: {applied}/{len(EDITS)} edits applied")

    p = io.open(PROSE, encoding="utf-8", newline="").read()
    if PROSE_OLD in p and "design law" not in p:
        io.open(PROSE, "w", encoding="utf-8", newline="").write(
            p.replace(PROSE_OLD, PROSE_NEW, 1))
        print("prose_scan.py: VOCAB extended with design law / law / precondition")
    else:
        print("prose_scan.py: unchanged (already extended, or anchor drifted)")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
