# -*- coding: utf-8 -*-
"""gate_edits_r134.py -- the gate changes R134 needs, each asserted and idempotent; listed in reviews/v23/REPORT_R134.md and CLAIMS.md R134-G.

  tools/slogan_scan.py   EXEMPT_S9: the R133 entry for S2's abstract sentence ('but not when all items are pooled, where the models stay') is retired: that
                         sentence left with the author's abstract of 2026-09-21 (RULING 2, agreed).
  tools/prose_scan.py    WHITELIST: the author's abstract is verbatim by the ruling of 2026-09-21 ('Do not reword it and let no prose gate reword it'; RULING 2:
                         'If a prose rule fires inside it, record an AUTHOR-RULING entry for the abstract only and list it. Nothing else gets an exemption.').
                         Two of its sentences trip prose rules and are excised before the scan: the sibling-control sentence (rule V, 'held' in 'held fixed')
                         and the count-feature sentence (rule L, 48 words; rule D, a 73% token overlap with Section 5.2's lead 'The stronger models' lead
                         comes from counts, and a count feature closes it within a question.'). No other text gets an entry.
Usage: python reviews/v23/tools/gate_edits_r134.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "iclr2027_monitoring_submission" / "tools"
ABS_HELD = "Second, for superseded records, the one state whose names the summary lists, no model reliably beats a cosine-similarity lookup over those names, even with counts and list length held fixed."
ABS_COUNT = ("The stronger models' lead over the lookup of $0.08$ to $0.10$ comes from retracted and expired records, which the summary only counts; one count feature added to the lookup closes it "
             "within a question's three store versions, though not when all items are pooled ($0.05$ to $0.06$ remains).")


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
    edit(TOOLS / "slogan_scan.py", [
        ('    # R133 (2026-09-21): the author\'s abstract swap S2, verbatim by instruction (reviews/v23/tools/port_r133.py; CLAIMS.md R133 block, R133-G): the pooled qualification\n'
         '    "but not when all items are pooled, where the models stay",\n]\n',
         '    # R133 (2026-09-21): the author\'s abstract swap S2 carried \'but not when all items are pooled, where the models stay\'; R134 (2026-09-21): that sentence left with the\n'
         '    # author\'s abstract (reviews/v23/tools/port_r134.py, unit abstract; RULING 2), so the entry is retired (gate_edits_r134.py); the new abstract carries no S9 pattern.\n'
         ']\n'),
    ])
    entry = (
        '    # R134 (2026-09-21): the author\'s abstract, verbatim by the ruling of 2026-09-21 (\'let no prose gate reword it\'; RULING 2: an AUTHOR-RULING entry for the abstract only,\n'
        '    # listed in REPORT_R134.md; nothing else exempted). Two of its sentences trip prose rules: \'held\' in \'held fixed\' (rule V) and the count-feature sentence (rule L, 48 words;\n'
        '    # rule D, 73% with Section 5.2\'s lead \'The stronger models\' lead comes from counts, and a count feature closes it within a question.\'). CLAIMS.md R133 block, R134-G.\n'
        f'    ({ABS_HELD!r},\n'
        '     "AUTHOR-RULING R134 (the abstract, verbatim)", "vocab held",\n'
        '     "CLAIMS.md R133 block (R134-G)"),\n'
        f'    ({ABS_COUNT!r},\n'
        '     "AUTHOR-RULING R134 (the abstract, verbatim)", "sentence over 40 words; rule D pair with Section 5.2\'s lead (73%)",\n'
        '     "CLAIMS.md R133 block (R134-G)"),\n')
    edit(TOOLS / "prose_scan.py", [
        ('    ("In these tests, no reader we tried made up for what the store had failed to write down.",\n'
         '     "AUTHOR-RULING R133 RULINGS 1 (the Conclusion\'s first sentence)", "vocab failed",\n'
         '     "CLAIMS.md R133 block (R133-RULINGS)"),\n]\n',
         '    ("In these tests, no reader we tried made up for what the store had failed to write down.",\n'
         '     "AUTHOR-RULING R133 RULINGS 1 (the Conclusion\'s first sentence)", "vocab failed",\n'
         '     "CLAIMS.md R133 block (R133-RULINGS)"),\n' + entry + ']\n'),
    ])
    print("gate edits applied: slogan_scan EXEMPT_S9 entry retired; prose_scan WHITELIST gains the two abstract entries")


if __name__ == "__main__":
    main()
