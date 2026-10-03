r"""_phase4c.py -- R81 Phase 4c: cuts and placements.

Idempotent. Reports any anchor it cannot find and changes nothing for that item.

ITEM 1 IS APPLIED AS A RELOCATION, NOT A CUT. The two sentences it names are U3, an
UNTOUCHABLE BYTE-IDENTICAL block. Deleting them would break CLAIMS.md's exactly-once rule,
slogan_scan's PINNED check and claims_diff at once. They move verbatim into Appendix F.7
beside the inversion tables that are their evidence, exactly as U2, U4 and U7 moved. Main
text keeps only the last sentence, which is what the item asks for.
"""
# R83: anchors re-keyed from heading TEXT to \label{}. Retitling Appendix H broke
# _r82_int's guard because it keyed on the title; a heading is an identity key for prose,
# exemption tables AND splicer anchors, and only the label survives a rename.
import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SUB = ROOT / "iclr2027_monitoring_submission"
TEX = SUB / "paper_v2.tex"
CLAIMS = SUB / "CLAIMS.md"
NL = "\r\n"

U3 = ("The association does not identify which rendered feature causes the inversion." + NL +
      "The candidate mechanisms in Section~\\ref{sec:inversion} remain unresolved after the "
      "registered single-channel probe.")
U2 = ("Scope: the negative index effect is measured; the single-channel ablations do not "
      "identify its cause.")
U7 = (r"Permuting which counts and attribute-name lists belong to which category changes "
      r"neither judgment, which bounds the mechanism rather than that specificity---"
      r"per-category correspondence is not necessary on FR-Bank, consistent with the name map "
      r"rather than the count structure carrying the effect (Definition~\ref{def:index}), "
      r"though the shuffle preserves the global name and count multiset and the flat "
      r"superseded-names section and so bounds correspondence alone.")

FACTORIAL_PROSE = (
    "The factorial separates the lifecycle-index change from the two prompt changes and "
    "checks the main-study reproduction." + NL +
    "The lifecycle-index main effect is $+0.1980$, the two prompt-fix effects are $+0.0134$ "
    "and $-0.0193$, and the matching factorial condition reproduces the main study at "
    "$0.7344$ against its indexed NOK of $0.7339$; endpoints for these summary effects were "
    "not separately recorded, so no intervals exist.")

ECON_TWO = (
    "Monitoring runs before every query, so its cost turns on prompt caching." + NL +
    "The list-price projection and the billed micro-run disagree about which monitor is "
    "cheaper: with caching the indexed monitor is projected at \\$207 per million calls "
    "against \\$234 blind, while as billed it costs \\$360 against \\$233, because cached "
    "input bills at $25\\%$ of list and $64.3\\%$ of indexed prompt tokens hit the "
    "block-aligned cache.")


def cut_table(s, label, report):
    """Remove the whole table environment carrying \\label{label}."""
    i = s.find("\\label{" + label + "}")
    if i < 0:
        report.append(f"table {label}: label not found")
        return s
    a = s.rfind("\\begin{table}", 0, i)
    b = s.find("\\end{table}", i)
    if a < 0 or b < 0:
        report.append(f"table {label}: environment not found")
        return s
    b += len("\\end{table}")
    while s[b:b + 2] == NL:
        b += 2
    return s[:a] + s[b:]


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()
    rep, done = [], []

    # ---- item 1: U3 relocates to F.7; main text keeps the last sentence only
    if U3 in s and "% U3 (CLAIMS.md untouchable" not in s:
        s = s.replace(U3 + NL, "", 1)
        anchor = "\\label{app:inversion}"
        s = s.replace(anchor, anchor + NL + NL +
                      "% U3 (CLAIMS.md untouchable, byte-identical), relocated from Section 6 on"
                      + NL +
                      "% 2026-08-30 under the U-BLOCK RELOCATIONS ruling as extended that date."
                      + NL +
                      "% Section 6 states the open mechanism once; its two further statements"
                      + NL +
                      "% are kept verbatim here beside the inversion tables that evidence them."
                      + NL + U3, 1)
        done.append("1 (U3 relocated, not cut)")
    else:
        rep.append("item 1: U3 already relocated or not found")

    # ---- item 2: 7.2 projected-vs-billed sentence moves to the end of its paragraph
    econ = ("The projected and the billed cost arithmetic disagree about which monitor is "
            "cheaper, and Appendix~\\ref{app:economics} records both orderings with the "
            "telemetry behind them.")
    tail = ("This paper establishes the pre-retrieval measurement; the downstream effect of "
            "FOK and NOK remains open.")
    if econ + NL in s and s.index(econ) < s.index(tail):
        s = s.replace(econ + NL, "", 1)
        s = s.replace(tail, tail + NL + econ, 1)
        done.append("2")
    else:
        rep.append("item 2: already moved or anchors not found")

    # ---- item 3: the word headline stops pointing at the FOK row
    if "FOK, FR-Bank hard (headline)" in s:
        s = s.replace("FOK, FR-Bank hard (headline)", "FOK, FR-Bank hard", 1)
        s = s.replace(
            "The within-FR-Bank gain is the headline because the pooled rows mix backends.",
            "The within-FR-Bank gain is the primary coverage row because the pooled rows mix "
            "backends.", 1)
        done.append("3")
    else:
        rep.append("item 3: already applied")

    # ---- item 4: Remark 1 removed entirely
    if "\\subsection{Scalar-trust infeasibility}" in s:
        a = s.index("\\subsection{Scalar-trust infeasibility}")
        b = s.index("\\section{", a)
        s = s[:a] + s[b:]
        done.append("4")
    else:
        rep.append("item 4: already removed")

    # ---- item 5: economics table and the 25x paragraph go; F.10 becomes two sentences
    if "\\label{tab:economics}" in s:
        s = cut_table(s, "tab:economics", rep)
        i = s.find("The tested luna and sol input prices span a $25\\times$")
        if i >= 0:
            j = s.index(NL, i) + 2
            s = s[:i] + s[j:]
        a = s.index("\\label{app:economics}")
        b = s.index("\\subsection{", a + 10) if "\\subsection{" in s[a + 10:] else len(s)
        nxt = s.find("\\section{", a)
        b = min(x for x in (b, nxt if nxt > 0 else len(s)) if x > a)
        head = "\\label{app:economics}\\label{app:economics}"
        s = s[:a] + head + NL + NL + ECON_TWO + NL + NL + s[b:]
        done.append("5")
    else:
        rep.append("item 5: already applied")

    # ---- item 6: the factorial table becomes prose
    if "\\label{tab:factorial}" in s:
        s = cut_table(s, "tab:factorial", rep)
        old = ("The factorial separates the lifecycle-index change from the two prompt "
               "changes and checks the main-study reproduction.")
        s = s.replace(old, FACTORIAL_PROSE, 1)
        done.append("6")
    else:
        rep.append("item 6: already applied")

    # ---- item 7: U7 moves under Table 14's footnote, with U4's lead-in form
    if U7 in s and "Section 4.4's sentence is kept verbatim:" not in s:
        s = s.replace(NL + U7, "", 1)
        end = s.index("\\label{tab:wrongindex}")
        end = s.index("\\end{table}", end) + len("\\end{table}")
        s = (s[:end] + NL + NL +
             "% U7 (CLAIMS.md untouchable, byte-identical), placed under Table 14's footnote"
             + NL + "% on 2026-08-30 with the lead-in form U4 carries." + NL +
             "Section 4.4's sentence is kept verbatim:" + NL + U7 + s[end:])
        done.append("7")
    else:
        rep.append("item 7: already placed")

    # ---- item 8: U2 moves to F.7 beside the inversion tables
    if U2 in s and "% U2 relocated to F.7" not in s:
        i = s.index(U2)
        a = s.rfind(NL, 0, s.rfind(NL, 0, i))
        s = s[:a] + s[i + len(U2):]
        anchor = "\\label{app:inversion}"
        s = s.replace(anchor, anchor + NL + NL + "% U2 relocated to F.7 on 2026-08-30: its "
                      "evidence is the two inversion tables below." + NL + U2, 1)
        done.append("8")
    else:
        rep.append("item 8: already placed")

    # ---- item 9: float barriers
    if "\\FloatBarrier" in s:
        h = "\\label{app:economics}"
        if s.count("\\FloatBarrier" + NL + NL + h) == 0 and h in s:
            s = s.replace(h, "\\FloatBarrier" + NL + NL + h, 1)
        f5 = "\\label{app:factorial}"
        if f5 in s and "\\FloatBarrier" + NL + NL + f5 not in s:
            s = s.replace(f5, "\\FloatBarrier" + NL + NL + f5, 1)
        done.append("9")

    for tag, blk in (("U2", U2), ("U3", U3), ("U7", U7)):
        n = re.sub(r"\s+", " ", s).count(re.sub(r"\s+", " ", blk))
        if n != 1:
            sys.exit(f"STOP: {tag} appears {n} times after Phase 4c; must be exactly once")

    io.open(TEX, "w", encoding="utf-8", newline="").write(s)
    print("applied:", ", ".join(done) or "nothing")
    for r in rep:
        print("  note:", r)

    c = io.open(CLAIMS, encoding="utf-8", newline="").read()
    if "PHASE 4C AUTHORIZATIONS" not in c:
        block = (NL + "**PHASE 4C AUTHORIZATIONS (dated 2026-08-30).**" + NL + NL +
                 "- **U3 relocates**, verbatim, from §6 into Appendix F.7 beside the inversion "
                 "tables that" + NL + "  evidence it. The Phase 4c order asked for two of its "
                 "three unresolved-mechanism" + NL + "  sentences to be cut; U3 is untouchable "
                 "and byte-identical, so it moves instead and" + NL + "  §6 keeps the last "
                 "sentence alone. Main text states the open mechanism once, which is" + NL +
                 "  what the item asked for. U1, U5, U6 and U8 stay where they are." + NL +
                 "- **Remark 1 (scalar-trust infeasibility) is removed** from Appendix A. Its "
                 "CLAIMS class" + NL + "  was procedural and the manuscript called it a "
                 "motivating impossibility rather than a" + NL + "  claimed contribution, so "
                 "nothing changes strength. Nothing in paper_v2.tex cites it." + NL +
                 "- **The economics table is not printed.** Its figures remain in the ledger "
                 "and in" + NL + "  `AUX-R74-X3`; the R2 requirement that the projected and "
                 "billed orderings disagree is" + NL + "  satisfied by the §7.2 sentence and "
                 "the two F.10 sentences, which print all four" + NL + "  figures inline. **No "
                 "number is deleted from any ledger.**" + NL)
        c = c.replace("## MAIN TEXT CLAIMS", block + NL + "## MAIN TEXT CLAIMS", 1)
        io.open(CLAIMS, "w", encoding="utf-8", newline="").write(c)
        print("CLAIMS.md: Phase 4c authorizations added")
    return 0


if __name__ == "__main__":
    sys.exit(main())
