r"""_phase5_u7.py -- R81 Phase 5: relocate U7 verbatim to Appendix F beside Table 14.

Same mechanism as U2 and U4: the block moves BYTE-IDENTICAL into the appendix and main text
receives a plain replacement at the same claim strength. U7 still appears exactly once in the
document, which is the level slogan_scan's pinned check counts at.

Destination is beside tab:wrongindex, whose "Own index, categories shuffled" rows are the
manipulation U7 scopes.

Idempotent.
"""
import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SUB = ROOT / "iclr2027_monitoring_submission"
TEX = SUB / "paper_v2.tex"
CLAIMS = SUB / "CLAIMS.md"
NL = "\r\n"

U7 = (r"Permuting which counts and attribute-name lists belong to which category changes "
      r"neither judgment, which bounds the mechanism rather than that specificity---"
      r"per-category correspondence is not necessary on FR-Bank, consistent with the name map "
      r"rather than the count structure carrying the effect (Definition~\ref{def:index}), "
      r"though the shuffle preserves the global name and count multiset and the flat "
      r"superseded-names section and so bounds correspondence alone.")

MAIN_REPLACEMENT = (
    "% U7 RELOCATED 2026-08-30 to Appendix F beside Table~\\ref{tab:wrongindex} under the"
    + NL +
    "% U-BLOCK RELOCATIONS ruling as extended this date. Byte-identical there, still exactly"
    + NL +
    "% once in the document. Plain replacement below at equal claim strength."
    + NL +
    "Permuting which counts and attribute-name lists belong to which category changes neither "
    "judgment." + NL +
    "Per-category correspondence is therefore unnecessary on FR-Bank, and the shuffle "
    "preserves the global name and count multiset, so it bounds correspondence alone "
    "(Appendix~\\ref{app:repro}).")

APPENDIX_ANCHOR = (
    "Permuting which counts and names belong to which category leaves both judgments "
    "unchanged, which bounds the mechanism rather than the store specificity: the effect on "
    "FR-Bank does not require per-category correspondence, and is consistent with a flat "
    "lookup asking whether a question-matching attribute name appears anywhere in the index "
    "and whether it is flagged as carrying superseded content.")

APPENDIX_INSERT = (APPENDIX_ANCHOR + NL +
                   "% U7 (CLAIMS.md untouchable, byte-identical), relocated from Section 4.4 on"
                   + NL +
                   "% 2026-08-30 under the U-BLOCK RELOCATIONS ruling as extended that date."
                   + NL + U7)

CLAIMS_ANCHOR = ("- **U4** (\"This law is directional but not mechanistic: the source of the "
                 "observed\n  below-chance behavior remains open.\") moves from §6 into "
                 "Appendix F.7.")
CLAIMS_ADD = (CLAIMS_ANCHOR + "\n- **U7** (the SW-2 sentence ending \"...and so bounds "
              "correspondence alone\") moves from\n  §4.4 into Appendix F beside "
              "`tab:wrongindex`. **Added 2026-08-30** on the user's ruling,\n  after Phase 4 "
              "reported that rewriting it in place would have broken byte-identity,\n  "
              "`EXEMPT_S8` and the `PINNED` check at once. Main text receives a two-sentence "
              "plain\n  replacement at the same claim strength. **U1, U3, U5, U6 and U8 stay "
              "where they are.**")


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()
    if U7 not in s:
        sys.exit("STOP: U7 bytes not found in paper_v2.tex")
    if s.count(U7) != 1:
        sys.exit(f"STOP: U7 appears {s.count(U7)} times; must be exactly once")

    already = APPENDIX_ANCHOR + NL + "% U7 (CLAIMS.md untouchable" in s
    if already:
        print("paper_v2.tex: U7 already relocated")
    else:
        # 1. main text: U7 line -> plain replacement
        s = s.replace(U7, MAIN_REPLACEMENT, 1)
        # 2. appendix: reinsert U7 verbatim after the two-arm prose
        if APPENDIX_ANCHOR not in s:
            sys.exit("STOP: appendix anchor not found; U7 not reinserted")
        s = s.replace(APPENDIX_ANCHOR, APPENDIX_INSERT, 1)
        assert s.count(U7) == 1, "U7 must still appear exactly once"
        io.open(TEX, "w", encoding="utf-8", newline="").write(s)
        print("paper_v2.tex: U7 relocated verbatim; main text carries the plain replacement")

    c = io.open(CLAIMS, encoding="utf-8", newline="").read()
    if "**U7** (the SW-2 sentence" in c:
        print("CLAIMS.md: U7 relocation already authorized")
    elif CLAIMS_ANCHOR.replace("\n", "\r\n") in c:
        c = c.replace(CLAIMS_ANCHOR.replace("\n", "\r\n"),
                      CLAIMS_ADD.replace("\n", "\r\n"), 1)
        c = c.replace("No other U-block moves. U1, U3, U5, U6, U7, U8 stay where they are.",
                      "No other U-block moves. U1, U3, U5, U6 and U8 stay where they are.", 1)
        io.open(CLAIMS, "w", encoding="utf-8", newline="").write(c)
        print("CLAIMS.md: U7 relocation authorized, dated 2026-08-30")
    elif CLAIMS_ANCHOR in c:
        c = c.replace(CLAIMS_ANCHOR, CLAIMS_ADD, 1)
        c = c.replace("No other U-block moves. U1, U3, U5, U6, U7, U8 stay where they are.",
                      "No other U-block moves. U1, U3, U5, U6 and U8 stay where they are.", 1)
        io.open(CLAIMS, "w", encoding="utf-8", newline="").write(c)
        print("CLAIMS.md: U7 relocation authorized, dated 2026-08-30")
    else:
        sys.exit("STOP: CLAIMS.md U-BLOCK RELOCATIONS anchor not found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
