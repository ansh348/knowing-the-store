# -*- coding: utf-8 -*-
"""stage_tools_wp2.py -- the Phase 2 commit of the writing pass: into the index named by GIT_INDEX_FILE (a private index read from HEAD),
stage HEAD's content plus this pass's hunks for slogan_scan.py (the Phase 2 S9 entry), frozen_diff.py (registration_fragments(), the R111
parser fix, and its header note), appendix_identity.py (the R111 pin blocks the working copy carries, in place of the one HEAD has) and
CLAIMS.md (the R111 block as it stands now, in place of HEAD's). The same technique as stage_tools_r111.py; the lineage's other
uncommitted hunks stay with the lineage. Run from the repo root with GIT_INDEX_FILE set.
"""
import os
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]
T = "iclr2027_monitoring_submission/tools/"
assert os.environ.get("GIT_INDEX_FILE"), "GIT_INDEX_FILE not set"


def git(*a, **k):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", **k)


def head(rel):
    return git("show", f"HEAD:{rel}").stdout.replace("\r\n", "\n")


def work(rel):
    return (ROOT / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


def stage(rel, staged):
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=ROOT, input=staged.encode("utf-8"), capture_output=True).stdout.decode().strip()
    r = git("update-index", "--cacheinfo", f"100644,{blob},{rel}")
    assert r.returncode == 0, r.stderr
    return blob


def between(text, start, end):
    i = text.index(start); j = text.index(end, i)
    return text[i:j]


def main():
    # slogan_scan.py: HEAD + the Phase 2 EXEMPT_S9 entry (two lines, taken from the working copy)
    rel = T + "slogan_scan.py"
    h, w = head(rel), work(rel)
    anchor = '    "read the summary by its names, not by its counts",\n]'
    ins = between(w, "    # R111 Phase 2 (2026-09-15): the author's own sentence", "]")
    assert h.count(anchor) == 1 and ins in w
    staged = h.replace(anchor, '    "read the summary by its names, not by its counts",\n' + ins + "]")
    print(f"staged {rel}: HEAD + Phase 2 S9 entry, blob {stage(rel, staged)[:12]}")
    # frozen_diff.py: HEAD + the header note + registration_fragments() + the loop replaced (all three taken from the working copy)
    rel = T + "frozen_diff.py"
    h, w = head(rel), work(rel)
    note = between(w, "  R111 (2026-09-15, the writing pass; the author's ruling on the Phase 2 report)", "\nUsage:")
    a1 = "landed branch sentence such as the NB6-1 failure text is watched without a hand-kept list.\n"
    assert h.count(a1) == 1
    staged = h.replace(a1, a1 + note + "\n")
    func = between(w, "def registration_fragments():", "def claims_sections(claims, program):")
    a2 = "def claims_sections(claims, program):"
    assert staged.count(a2) == 1
    staged = staged.replace(a2, func + a2)
    m = re.search(r"    for reg in sorted\(\(SUB / \"ARTIFACT\" / \"registrations\"\)\.glob\(\"\*\.md\"\)\):\n(?:        .*\n)+?(?=\n)", staged)
    assert m, "the old registration loop not found in HEAD"
    staged = staged.replace(m.group(0), '    src += [("R", name, frag) for name, frag in registration_fragments()]\n')
    assert staged.count("registration_fragments()") == 3   # the header note, the def, the call
    print(f"staged {rel}: HEAD + registration_fragments(), blob {stage(rel, staged)[:12]}")
    # appendix_identity.py: HEAD's first R111 pin block replaced by every R111 pin block the working copy carries
    rel = T + "appendix_identity.py"
    h, w = head(rel), work(rel)
    marker = "\n\ndef sections(text):"
    wb = w[w.index("\n# R111 (2026-09-15): pins"):w.index(marker)]
    hb = h[h.index("\n# R111 (2026-09-15): pins"):h.index(marker)]
    staged = h.replace(hb, wb)
    assert staged.count("# R111 (2026-09-15): pins") == w.count("# R111 (2026-09-15): pins")
    print(f"staged {rel}: HEAD + the R111 pin blocks ({staged.count('# R111 (2026-09-15): pins')}), blob {stage(rel, staged)[:12]}")
    # CLAIMS.md: HEAD's R111 block replaced by the block file
    rel = "iclr2027_monitoring_submission/CLAIMS.md"
    h = head(rel)
    block = (ROOT / "reviews" / "v18" / "claims_r111_block.md").read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n") + "\n"
    i = h.index("## R111 AUTHORIZATION BLOCK")
    staged = h[:i] + block
    print(f"staged {rel}: HEAD with the R111 block refreshed, blob {stage(rel, staged)[:12]}")


if __name__ == "__main__":
    main()
