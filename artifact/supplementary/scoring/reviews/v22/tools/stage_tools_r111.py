# -*- coding: utf-8 -*-
"""stage_tools_r111.py -- into the index named by GIT_INDEX_FILE (a private index read from HEAD), stage HEAD's content plus this pass's
hunks only for the four gate tools and CLAIMS.md the writing pass touched (the HEAD+insertion technique of stage_tools_r110.py; project
rule: never sweep another program's uncommitted hunks). Each anchor is asserted once in HEAD's text and each inserted core is asserted
present in the working copy. Run from the repo root with GIT_INDEX_FILE set, then `git commit -F <msg>` on that index.
"""
import os
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]
T = "iclr2027_monitoring_submission/tools/"
assert os.environ.get("GIT_INDEX_FILE"), "GIT_INDEX_FILE not set"

# (anchor in HEAD, replacement) pairs per file, applied in order to HEAD's text (LF)
EDITS = {
    T + "prose_scan.py": [
        ('r"""prose_scan -- R79 plain-language gates for the paper_v2 lineage.\n',
         'r"""prose_scan -- R79 plain-language gates for the paper_v2 lineage.\n'
         '\n'
         "R111 (2026-09-15, the writing pass on paper_v18; CLAIMS.md R111 block): rule G4's anchor regex also accepts Section 1's\n"
         'approved thesis sentence ("read a lifecycle summary by its names and not by its counts"). Reason: item 7 of the pass deletes\n'
         'the four-finding paragraph that carried "name readers", the only anchor form the regex matched; the thesis sentence is the\n'
         "reader claim itself and precedes the first mention of tags. The author's ruling: that sentence specifically, no wider form.\n"),
        ('        anchor = next((i for i in s1_lines if re.search(r"name[- ]readers?|reads? (the )?names|as a (list|map) of names|name list", stripped[i], flags=re.IGNORECASE)), None)',
         "        # R111 (2026-09-15, the writing pass): the approved thesis sentence of Section 1 is the anchor once item 7 deletes the\n"
         '        # four-finding paragraph that carried "name readers"; the regex accepts that sentence specifically (the author\'s ruling), not\n'
         '        # any sentence containing "by its names".\n'
         '        anchor = next((i for i in s1_lines if re.search(r"name[- ]readers?|reads? (the )?names|as a (list|map) of names|name list|read a lifecycle summary by its names and not by its counts", stripped[i], flags=re.IGNORECASE)), None)'),
    ],
    T + "hygiene_scan.py": [
        ('r"""hygiene_scan -- the submission is anonymous, Letter, and free of Type 3 fonts.\n',
         'r"""hygiene_scan -- the submission is anonymous, Letter, and free of Type 3 fonts.\n'
         '\n'
         'R111 (2026-09-15, the writing pass on paper_v18): CITE_TEXT admits up to two interleaved 1-3 digit tokens after the first surname\n'
         'and after the comma (R101 admitted one). Reason: the Limitations citation of the prior store now sits on the page 9 / 10 break,\n'
         'and pdftotext interleaves the page number and the margin line number before the year ("[AUTHOR-1] & [AUTHOR-2], 9 486 2026");\n'
         'the span must still carry both surnames and the year, so nothing outside a rendered citation is admitted.\n'),
        ('    r"[AUTHOR-1]\\s*(?:&|and)\\s*(?:e\\.\\s*)?t\\S{3,5}n(?:\\s+\\d{1,3})?\\s*"\n'
         '    r"(?:\\(2026\\)|,\\s*2026|\\.\\s*fortunate recall)", re.I)',
         '# R111 (2026-09-15, the writing pass): a citation set at a page break carries a page number and a margin number before the year\n'
         '# ("[AUTHOR-1] & [AUTHOR-2], 9 486 2026", Limitations on the page 9 / 10 break), so up to two digit tokens are admitted at each slot.\n'
         '    r"[AUTHOR-1](?:\\s+\\d{1,3}){0,2}\\s*(?:&|and)\\s*(?:e\\.\\s*)?t\\S{3,5}n(?:\\s+\\d{1,3}){0,2}\\s*"\n'
         '    r"(?:\\(2026\\)|,\\s*(?:\\d{1,3}\\s+){0,2}2026|\\.\\s*fortunate recall)", re.I)'),
    ],
    T + "trace_scan_v13.py": [
        ('"""Independent numeric-occurrence re-scan of a manuscript against the central number record.\n',
         '"""Independent numeric-occurrence re-scan of a manuscript against the central number record.\n'
         'R111 (2026-09-15, the writing pass on paper_v18): LEDGERS gains reviews/NUMBERS_WP.md. Reason: the six body tables print two-decimal\n'
         'forms of recorded four-decimal values (items 45, 50 to 55) and the population table prints the calls per question from the\n'
         'recorded rows (AUX-WP-X5-DRAWS); the set-based match needs the printed strings in a ledger, each beside its source key.\n'),
        ('    pathlib.Path("../r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md"),\n]',
         '    pathlib.Path("../r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md"),\n'
         '    # R111 (2026-09-15, the writing pass): the two-decimal forms of the six body tables and the calls per question of the population table (reviews/NUMBERS_WP.md, AUX-WP-*).\n'
         '    pathlib.Path("../reviews/NUMBERS_WP.md"),\n]'),
    ],
}


def git(*a, **k):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", **k)


def stage(rel, staged):
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=ROOT, input=staged.encode("utf-8"), capture_output=True).stdout.decode().strip()
    r = git("update-index", "--cacheinfo", f"100644,{blob},{rel}")
    assert r.returncode == 0, r.stderr
    return blob


def main():
    for rel, edits in EDITS.items():
        head = git("show", f"HEAD:{rel}").stdout.replace("\r\n", "\n")
        work = (ROOT / rel).read_text(encoding="utf-8").replace("\r\n", "\n")
        staged = head
        for old, new in edits:
            assert staged.count(old) == 1, (rel, staged.count(old), old[:60])
            staged = staged.replace(old, new)
            core = new[len(old):] if new.startswith(old) else new
            assert core.strip() in work, ("the working copy does not carry the insertion", rel, core[:60])
        print(f"staged {rel}: HEAD + R111 ({len(staged.splitlines()) - len(head.splitlines()):+d} lines), blob {stage(rel, staged)[:12]}")
    # appendix_identity.py: HEAD plus the R111 pin block the working copy carries
    rel = T + "appendix_identity.py"
    head = git("show", f"HEAD:{rel}").stdout.replace("\r\n", "\n")
    work = (ROOT / rel).read_text(encoding="utf-8").replace("\r\n", "\n")
    i = work.index("\n# R111 (2026-09-15): pins for the writing pass's appendix state")
    j = work.index("\n\ndef sections(text):")
    block = work[i:j]
    marker = "\n\ndef sections(text):"
    assert head.count(marker) == 1 and "R111" not in head
    staged = head.replace(marker, block + marker)
    print(f"staged {rel}: HEAD + R111 pins ({len(staged.splitlines()) - len(head.splitlines()):+d} lines), blob {stage(rel, staged)[:12]}")
    # CLAIMS.md: HEAD plus the R111 block (the lineage's earlier uncommitted blocks stay with the lineage)
    rel = "iclr2027_monitoring_submission/CLAIMS.md"
    head = git("show", f"HEAD:{rel}").stdout.replace("\r\n", "\n")
    block = (ROOT / "reviews" / "v18" / "claims_r111_block.md").read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n") + "\n"
    assert "## R111 AUTHORIZATION BLOCK" not in head
    staged = head.rstrip("\n") + "\n\n" + block
    print(f"staged {rel}: HEAD + R111 block ({len(staged.splitlines()) - len(head.splitlines()):+d} lines), blob {stage(rel, staged)[:12]}")


if __name__ == "__main__":
    main()
