# -*- coding: utf-8 -*-
"""stage_tools_wp3.py -- the Phases 3, 4 and 4b checkpoint commit of the writing pass: into the index named by GIT_INDEX_FILE (a private
index read from HEAD), stage HEAD's content plus this pass's hunks for slogan_scan.py (the Phase 3 and Phase 4 EXEMPT_S9 entries),
appendix_identity.py (the R111 pin blocks the working copy carries, in place of the ones HEAD has) and CLAIMS.md (the R111 block as it
stands now, in place of HEAD's). The same technique as stage_tools_wp2.py; the lineage's other uncommitted hunks stay with the lineage.
Run from the repo root with GIT_INDEX_FILE set.
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
    # slogan_scan.py: HEAD + the Phase 3 and Phase 4 EXEMPT_S9 entries (four lines, taken from the working copy)
    rel = T + "slogan_scan.py"
    h, w = head(rel), work(rel)
    anchor = '    "the store\'s tags reach more of the forbidding records, not that there are more tags",\n]'
    ins = between(w, "    # R111 Phase 3 (2026-09-15): the author's contributions list", "]")
    assert h.count(anchor) == 1 and ins in w and "Phase 4 (2026-09-15)" in ins
    staged = h.replace(anchor, anchor[:-1] + ins + "]")
    assert staged.count("EXEMPT_S9 = [") == 1
    print(f"staged {rel}: HEAD + the Phase 3 and Phase 4 S9 entries, blob {stage(rel, staged)[:12]}")
    # appendix_identity.py: HEAD's R111 pin blocks replaced by every R111 pin block the working copy carries
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
