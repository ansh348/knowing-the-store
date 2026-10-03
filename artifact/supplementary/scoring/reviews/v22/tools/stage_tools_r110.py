# -*- coding: utf-8 -*-
"""stage_tools_r110.py -- stage only this pass's hunks of three gate tools (HEAD's content plus the R110 insertion), so the commit
carries the R110 change and none of the lineage's earlier uncommitted hunks (the HEAD+rule staging technique; project rule: commit
by pathspec, never sweep another program's hunks). Run from the repo root (optionally with the file names to stage), then `git commit` without a pathspec (a pathspec commit takes the working tree).
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
T = "iclr2027_monitoring_submission/tools/"

INSERTS = {
    T + "slogan_scan.py": (
        '    "ranks items well but cannot yet be trusted as a probability",\n]',
        '    "ranks items well but cannot yet be trusted as a probability",\n'
        '    # R110 (2026-09-15): the author\'s abstract v7, the downstream sentence in the author\'s words (reviews/v18/src/abstract_v18.tex; CLAIMS.md R110 block)\n'
        '    "reaches more forbidding records but does not reduce stale answers",\n]'),
    T + "trace_scan_v13.py": (
        '    pathlib.Path("../reviews/NUMBERS_R87.md"),\n]',
        '    pathlib.Path("../reviews/NUMBERS_R87.md"),\n'
        '    # R110 (2026-09-15, CC_PASS_v18). The Phase 1 analyses (count readers, tag baselines, single-draw scores, the lookup at 100\n'
        '    # and 200 names; reviews/NUMBERS_R110.md, AUX-R110-*), Haiku 4.5 under the store\'s own metadata (believed_h/NUMBERS_BELIEVED_H.md,\n'
        '    # AUX-BH-*) and the per-category increment moved within the triple (r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md, AUX-V2RCAT-*)\n'
        '    # enter the manuscript: Tables 1, 2 and 4, Sections 4 to 8, Appendices C.2, E.9, E.10. DS Amendments 5 to 7 write into\n'
        '    # ds_downstream/NUMBERS_DS.md sections 11 to 13, already listed.\n'
        '    pathlib.Path("../reviews/NUMBERS_R110.md"),\n'
        '    pathlib.Path("../believed_h/NUMBERS_BELIEVED_H.md"),\n'
        '    pathlib.Path("../r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md"),\n]'),
}


def git(*a, **k):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, **k)


def main():
    work = (ROOT / T / "appendix_identity.py").read_text(encoding="utf-8")
    i = work.index("\n# R110 (2026-09-15): pins for the v18 appendix state")
    j = work.index("\n\ndef sections(text):")
    INSERTS[T + "appendix_identity.py"] = ("\n\ndef sections(text):", work[i:j] + "\n\ndef sections(text):")
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    for rel, (anchor, new) in INSERTS.items():
        if only and not any(rel.endswith(o) for o in only):
            continue
        head = git("show", f"HEAD:{rel}").stdout
        if rel.endswith("appendix_identity.py") and "\n# R110 (2026-09-15): pins for the v18 appendix state" in head:
            # HEAD already carries an earlier R110 pin block: replace it with the working copy's
            a = head.index("\n# R110 (2026-09-15): pins for the v18 appendix state"); b = head.index("\n\ndef sections(text):")
            head = head[:a] + head[b:]
        assert head.count(anchor) == 1, (rel, head.count(anchor))
        staged = head.replace(anchor, new)
        cur = (ROOT / rel).read_text(encoding="utf-8").replace("\r\n", "\n")
        core = new.split("\n", 1)[1].rsplit("\n", 1)[0]     # the inserted lines without the anchor's first and last line
        assert core in cur, ("the working copy does not carry the insertion", rel)
        blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=ROOT, input=staged.encode("utf-8"), capture_output=True).stdout.decode().strip()
        r = git("update-index", "--cacheinfo", f"100644,{blob},{rel}")
        assert r.returncode == 0, r.stderr
        print(f"staged {rel}: HEAD + R110 insertion ({len(staged.splitlines()) - len(head.splitlines())} lines)")


if __name__ == "__main__":
    main()
