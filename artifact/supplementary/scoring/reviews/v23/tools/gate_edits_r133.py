# -*- coding: utf-8 -*-
"""gate_edits_r133.py -- the smallest gate changes the author's verbatim swaps need (the brief, sections 1.3 and 2: no prose gate may reword a swap), each
asserted and idempotent; listed in reviews/v23/REPORT_R133.md and CLAIMS.md R133-G.

  tools/slogan_scan.py   EXEMPT_S7 (new): S3 and S4 put the thesis sentence verbatim in the abstract and in Section 1 (the R131 close's B4 precedent: restating
                         the thesis in both places is intended), which S7's duplicate-sentence check would otherwise fail; the one sentence is exempt.
                         EXEMPT_S9: S2's abstract sentence carries 'but not when all items are pooled' (the pattern but .. not).
  tools/prose_scan.py    WHITELIST: the R131 close's B4 entry (the abstract's old thesis sentence, rule D against Section 1) becomes its S3 form, the rule D
                         pair with Section 1 (S4, identical) and the Conclusion (S6) overridden by the swaps.
  tools/repeat_scan.py   EXEMPT (new): the thesis sentence's 9-grams occur three times (the abstract, Section 1, the Conclusion) by the same instruction.
Usage: python reviews/v23/tools/gate_edits_r133.py [--rulings]   (--rulings: the R133 RULINGS 1 stage, on top of the first)
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "iclr2027_monitoring_submission" / "tools"
THESIS = "In these tests, what the store wrote down limited every reader we gave it to."
INTRO = "In these tests, every reader we tried was held back by what the store had written down."
CONCL = "In these tests, no reader we tried made up for what the store had failed to write down."


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
        ('    "We show monitors read names, not counts",\n    "but not a single deleted record",\n]\n',
         '    "We show monitors read names, not counts",\n    "but not a single deleted record",\n'
         '    # R133 (2026-09-21): the author\'s abstract swap S2, verbatim by instruction (reviews/v23/tools/port_r133.py; CLAIMS.md R133 block, R133-G): the pooled qualification\n'
         '    "but not when all items are pooled, where the models stay",\n]\n'
         '# R133 (2026-09-21): the author\'s swaps S3 and S4 put the thesis sentence verbatim in the abstract and in Section 1 (the R131 close\'s B4 precedent: restating the\n'
         '# thesis in both places is intended; no gate rewords a swap), so S7\'s duplicate-sentence check exempts that one sentence. CLAIMS.md R133 block, R133-G.\n'
         'EXEMPT_S7 = [\n'
         f'    "{THESIS}",\n'
         ']\n'),
        ('dups = {s: c for s, c in sentences.items() if c > 1}\n',
         'dups = {s: c for s, c in sentences.items() if c > 1 and s not in EXEMPT_S7}   # R133: the one exempt sentence (EXEMPT_S7)\n'),
    ])
    edit(TOOLS / "prose_scan.py", [
        ('    ("In these tests, what the store wrote down mattered more than which model read it.",\n'
         '     "AUTHOR-RULING R131 close B4 (the abstract\'s thesis sentence, restated in Section 1 by design)", "rule D near-duplicate with Section 1\'s thesis (85%)",\n'
         '     "CLAIMS.md R126 block (R131-CLOSE-B4)"),\n',
         '    # R133 (2026-09-21), the author\'s swaps S3, S4 and S6: the thesis sentence is put verbatim in the abstract and in Section 1 and, with \'a store\', in the Conclusion\n'
         '    # (no gate rewords a swap; the R131 close\'s B4 precedent), so rule D\'s pairs are overridden here rather than reworded. Was the B4 entry: "In these tests, what the\n'
         '    # store wrote down mattered more than which model read it." CLAIMS.md R133 block, R133-G.\n'
         f'    ("{THESIS}",\n'
         '     "AUTHOR-RULING R133 S3/S4/S6 (the abstract\'s thesis sentence, restated in Section 1 and the Conclusion by design)", "rule D near-duplicate with Section 1\'s and the Conclusion\'s thesis",\n'
         '     "CLAIMS.md R133 block (R133-G)"),\n'),
    ])
    edit(TOOLS / "repeat_scan.py", [
        ("N = 9\n",
         "N = 9\n"
         "# R133 (2026-09-21): the author's swaps S3, S4 and S6 put one thesis sentence in the abstract, Section 1 and the Conclusion ('the store' twice, 'a store' once), so\n"
         "# its 9-grams occur three times by instruction (no gate rewords a swap; the R131 close's B4 precedent). The one phrase is exempt. CLAIMS.md R133 block, R133-G.\n"
         'EXEMPT = ["store wrote down limited every reader we gave it to"]\n'),
        ("        if len(spread) >= 3:\n            bad[g] = spread\n",
         "        if len(spread) >= 3 and not any(g in e or e in g for e in EXEMPT):   # R133: the one exempt phrase\n            bad[g] = spread\n"),
    ])
    print("gate edits applied: slogan_scan.py (EXEMPT_S7, EXEMPT_S9), prose_scan.py (WHITELIST), repeat_scan.py (EXEMPT)")


def rulings():
    """R133 RULINGS 1 (the author, 2026-09-21): the abstract keeps S3; Section 1 and the Conclusion take the author's two sentences, so the thesis sentence no longer
    repeats. The repeat_scan EXEMPT and slogan_scan EXEMPT_S7 exemptions are removed (both scans pass unexempted). Kept: slogan_scan's EXEMPT_S9 entry for S2's
    abstract sentence ('but not when all items are pooled'), which the ruling did not change and which S9 would otherwise fail. prose_scan's WHITELIST: the R133
    thesis entry (rule D) becomes two entries for the ruled sentences, which carry rule V's outcome words 'held' (Section 1) and 'failed' (the Conclusion); the
    words are the author's and no gate rewords a swap, the R101 precedent (the ordered D-DS-3 (a) sentence carries 'failed')."""
    edit(TOOLS / "slogan_scan.py", [
        ('# R133 (2026-09-21): the author\'s swaps S3 and S4 put the thesis sentence verbatim in the abstract and in Section 1 (the R131 close\'s B4 precedent: restating the\n'
         '# thesis in both places is intended; no gate rewords a swap), so S7\'s duplicate-sentence check exempts that one sentence. CLAIMS.md R133 block, R133-G.\n'
         'EXEMPT_S7 = [\n'
         f'    "{THESIS}",\n'
         ']\n',
         '# R133 RULINGS 1 (2026-09-21): the thesis sentence no longer repeats (Section 1 and the Conclusion in the author\'s words), so the S7 exemption R133 added is removed;\n'
         '# S7 runs unexempted. The S9 entry above for S2\'s abstract sentence stays (the ruling kept the abstract).\n'
         'EXEMPT_S7 = []\n'),
    ])
    edit(TOOLS / "repeat_scan.py", [
        ('# R133 (2026-09-21): the author\'s swaps S3, S4 and S6 put one thesis sentence in the abstract, Section 1 and the Conclusion (\'the store\' twice, \'a store\' once), so\n'
         '# its 9-grams occur three times by instruction (no gate rewords a swap; the R131 close\'s B4 precedent). The one phrase is exempt. CLAIMS.md R133 block, R133-G.\n'
         'EXEMPT = ["store wrote down limited every reader we gave it to"]\n',
         '# R133 RULINGS 1 (2026-09-21): the thesis sentence no longer repeats (Section 1 and the Conclusion in the author\'s words), so the exemption R133 added is removed;\n'
         '# the rule runs unexempted (EXEMPT is empty).\n'
         'EXEMPT = []\n'),
    ])
    edit(TOOLS / "prose_scan.py", [
        (f'    ("{THESIS}",\n'
         '     "AUTHOR-RULING R133 S3/S4/S6 (the abstract\'s thesis sentence, restated in Section 1 and the Conclusion by design)", "rule D near-duplicate with Section 1\'s and the Conclusion\'s thesis",\n'
         '     "CLAIMS.md R133 block (R133-G)"),\n',
         '    # R133 RULINGS 1 (2026-09-21): the abstract keeps S3 and Section 1 and the Conclusion take the author\'s sentences below, verbatim by instruction (no gate rewords a\n'
         '    # swap; the R101 precedent of an ordered sentence carrying an outcome word). They carry rule V\'s \'held\' and \'failed\' in their ordinary senses, so rule V is overridden\n'
         '    # here rather than reworded; the R133 thesis entry (rule D) is no longer needed and is replaced. CLAIMS.md R133 block, R133-RULINGS.\n'
         f'    ("{INTRO}",\n'
         '     "AUTHOR-RULING R133 RULINGS 1 (Section 1\'s thesis sentence)", "vocab held",\n'
         '     "CLAIMS.md R133 block (R133-RULINGS)"),\n'
         f'    ("{CONCL}",\n'
         '     "AUTHOR-RULING R133 RULINGS 1 (the Conclusion\'s first sentence)", "vocab failed",\n'
         '     "CLAIMS.md R133 block (R133-RULINGS)"),\n'),
    ])
    print("gate edits applied (rulings): slogan_scan.py EXEMPT_S7 emptied, repeat_scan.py EXEMPT emptied, prose_scan.py WHITELIST (the two ruled sentences, rule V)")


if __name__ == "__main__":
    if "--rulings" in sys.argv:
        rulings()
    else:
        main()
