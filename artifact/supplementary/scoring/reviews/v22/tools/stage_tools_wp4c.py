# -*- coding: utf-8 -*-
"""stage_tools_wp4c.py -- the Phase 4c commit of the writing pass (closed with the author's ruling on the 4c report): into the index named by
GIT_INDEX_FILE (a private index read from HEAD), stage HEAD's content plus this pass's hunks for slogan_scan.py (the Phase 4c EXEMPT_S9
entries, the author's two sentences), prose_scan.py (rule G4's anchor regex accepting the new thesis sentence) and CLAIMS.md (the R111
block as it stands now, in place of HEAD's). The same technique as stage_tools_wp3.py; the lineage's other uncommitted hunks stay with
the lineage. Run from the repo root with GIT_INDEX_FILE set.
"""
import os
import pathlib
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
    # slogan_scan.py: HEAD + the Phase 4c EXEMPT_S9 entries (three lines, taken from the working copy)
    rel = T + "slogan_scan.py"
    h, w = head(rel), work(rel)
    anchor = '    "tracks the attribute names in the summary, not the counts beside them",\n]'
    ins = between(w, "    # R111 Phase 4c (2026-09-15): the author's cold-read ruling", "]")
    assert h.count(anchor) == 1 and ins in w and '"but not a single deleted record",\n' in ins
    staged = h.replace(anchor, anchor[:-1] + ins + "]")
    assert staged.count("EXEMPT_S9 = [") == 1
    print(f"staged {rel}: HEAD + the Phase 4c S9 entries, blob {stage(rel, staged)[:12]}")
    # prose_scan.py: HEAD + the G4 anchor hunk (the comment's two added lines and the regex line)
    rel = T + "prose_scan.py"
    h, w = head(rel), work(rel)
    old = ('        # any sentence containing "by its names".\n'
           '        anchor = next((i for i in s1_lines if re.search(r"name[- ]readers?|reads? (the )?names|as a (list|map) of names|name list|read a lifecycle summary by its names and not by its counts", stripped[i], flags=re.IGNORECASE)), None)\n')
    new = between(w, '        # any sentence containing "by its names". Phase 4c', '        first_tag = next(')
    assert h.count(old) == 1 and new in w and "read (a lifecycle summary|it) by its names" in new
    staged = h.replace(old, new)
    print(f"staged {rel}: HEAD + the Phase 4c G4 anchor, blob {stage(rel, staged)[:12]}")
    # CLAIMS.md: HEAD's R111 block replaced by the block file
    rel = "iclr2027_monitoring_submission/CLAIMS.md"
    h = head(rel)
    block = (ROOT / "reviews" / "v18" / "claims_r111_block.md").read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n") + "\n"
    i = h.index("## R111 AUTHORIZATION BLOCK")
    staged = h[:i] + block
    print(f"staged {rel}: HEAD with the R111 block refreshed, blob {stage(rel, staged)[:12]}")


if __name__ == "__main__":
    main()
