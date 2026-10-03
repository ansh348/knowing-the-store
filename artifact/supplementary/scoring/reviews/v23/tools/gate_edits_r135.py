# -*- coding: utf-8 -*-
"""gate_edits_r135.py -- the gate changes R135 needs, each asserted and idempotent; listed in reviews/v23/REPORT_R135.md and CLAIMS.md R135-G.

  tools/prose_scan.py    WHITELIST: the two AUTHOR-RULING entries R134 recorded for the R134 abstract's sentences ('held fixed'; the count-feature sentence) are
                         retired: neither sentence is in the abstract the brief lands (section 3). Any entry for the new abstract's own sentences, if a prose rule
                         fires inside it, is added by --abstract-entries (the brief's rule: the abstract may carry AUTHOR-RULING entries for its own sentences only).
Usage: python reviews/v23/tools/gate_edits_r135.py [--abstract-entries]
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "iclr2027_monitoring_submission" / "tools"
OLD_HELD = "Second, for superseded records, the one state whose names the summary lists, no model reliably beats a cosine-similarity lookup over those names, even with counts and list length held fixed."
OLD_COUNT = ("The stronger models' lead over the lookup of $0.08$ to $0.10$ comes from retracted and expired records, which the summary only counts; one count feature added to the lookup closes it "
             "within a question's three store versions, though not when all items are pooled ($0.05$ to $0.06$ remains).")
NEW_COUNT = "The three stronger models lead only where the summary counts a state without naming it, and one count feature closes that lead within a question, though not when items are pooled."


def edit(path, pairs):
    raw = path.read_bytes()
    crlf = b"\r\n" in raw
    t = raw.decode("utf-8").replace("\r\n", "\n")
    for old, new in pairs:
        if new in t and old not in t:
            continue   # already applied
        assert t.count(old) == 1, (path.name, old[:80])
        t = t.replace(old, new)
    path.write_bytes((t.replace("\n", "\r\n") if crlf else t).encode("utf-8"))


def main():
    retired = (
        '    # R134 (2026-09-21): the author\'s abstract, verbatim by the ruling of 2026-09-21 (\'let no prose gate reword it\'; RULING 2: an AUTHOR-RULING entry for the abstract only,\n'
        '    # listed in REPORT_R134.md; nothing else exempted). Two of its sentences trip prose rules: \'held\' in \'held fixed\' (rule V) and the count-feature sentence (rule L, 48 words;\n'
        '    # rule D, 73% with Section 5.2\'s lead \'The stronger models\' lead comes from counts, and a count feature closes it within a question.\'). CLAIMS.md R133 block, R134-G.\n'
        f'    ({OLD_HELD!r},\n'
        '     "AUTHOR-RULING R134 (the abstract, verbatim)", "vocab held",\n'
        '     "CLAIMS.md R133 block (R134-G)"),\n'
        f'    ({OLD_COUNT!r},\n'
        '     "AUTHOR-RULING R134 (the abstract, verbatim)", "sentence over 40 words; rule D pair with Section 5.2\'s lead (73%)",\n'
        '     "CLAIMS.md R133 block (R134-G)"),\n')
    note = ('    # R135 (2026-09-21): the two R134 entries for the R134 abstract\'s sentences (\'held fixed\'; the count-feature sentence) retired (gate_edits_r135.py): neither sentence is\n'
            '    # in the abstract the R135 brief lands (section 3). CLAIMS.md R133 block, R135-G.\n')
    edit(TOOLS / "prose_scan.py", [(retired + "]\n", note + "]\n")])
    print("gate edits applied: the R134 abstract entries retired")
    if "--abstract-entries" in sys.argv:
        entry = (
            '    # R135 (2026-09-21): the brief\'s abstract (section 3), verbatim by the pass\'s rule (\'no gate exemption for my texts ... The abstract is the author\'s text and may carry\n'
            '    # AUTHOR-RULING entries for its own sentences only\'): its count-feature sentence trips rule D against Section 5.2\'s lead \'The stronger models\' lead comes from counts, and a\n'
            '    # count feature closes it within a question.\' and is excised before the scan. CLAIMS.md R133 block, R135-G; listed in REPORT_R135.md.\n'
            f'    ({NEW_COUNT!r},\n'
            '     "AUTHOR-RULING R135 (the abstract, verbatim)", "rule D pair with Section 5.2\'s lead",\n'
            '     "CLAIMS.md R133 block (R135-G)"),\n')
        edit(TOOLS / "prose_scan.py", [(note + "]\n", note + entry + "]\n")])
        print("gate edits applied: the R135 abstract's rule D entry added")


if __name__ == "__main__":
    main()
