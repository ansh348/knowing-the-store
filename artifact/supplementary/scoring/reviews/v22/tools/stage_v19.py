# -*- coding: utf-8 -*-
"""stage_v19.py -- the v19 lineage's commits (program R112): into the index named by GIT_INDEX_FILE (a private index read from HEAD),
stage HEAD's content plus this lineage's hunks for CLAIMS.md (the R112 block as reviews/v19/claims_r112_block.md stands, appended after
HEAD's last block, or replacing HEAD's R112 block once one is committed) and, when named on the command line, the gate tools whose
v19 hunks are given as (file, anchor-in-HEAD, insertion-taken-from-the-working-copy) triples in HUNKS. The same technique as
reviews/v18/tools/stage_tools_wp4c.py; the lineage's other uncommitted hunks stay with the lineage. Run from the repo root with
GIT_INDEX_FILE set: python reviews/v19/tools/stage_v19.py [hunk-name ...]

RETIRED for the gate tools and CLAIMS.md by the housekeeping commit of 2026-09-18 (reviews/r115/HOUSEKEEPING_PROPOSAL.md): that
commit put the working copies of the thirteen gate tools and the whole CLAIMS.md into HEAD, so HEAD plus hunks equals the working
copy and later commits `git add` those files directly. The HUNKS table stays as the record of how the v19 commits before it were
staged; running this script after that commit would re-insert spans HEAD already holds, and the assertion in main() stops it.
"""
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
T = "iclr2027_monitoring_submission/tools/"
assert os.environ.get("GIT_INDEX_FILE"), "GIT_INDEX_FILE not set"

# name -> (file, the HEAD text the hunk follows, the working-copy start marker, the working-copy end marker[, "before"]); the text between the
# markers in the working copy (end excluded) is inserted after the HEAD anchor (or before it, with the fifth element). Filled in as v19 touches a gate tool.
# The integration pass (2026-09-16): the six hunks below and the appendix pins (review-2 A1 and the integration pass, one contiguous block).
HUNKS = {
    "trace_header": ("trace_scan_v13.py", '"""Independent numeric-occurrence re-scan of a manuscript against the central number record.\n',
                     "R112 (2026-09-16, the integration pass): LEDGERS gains", "R111 (2026-09-15, the writing pass on paper_v18): LEDGERS gains"),
    # Checkpoint before R115 (2026-09-18): 5e1a031 carried the R112 spans, so the two hunks below were re-anchored on the last committed
    # line and take the working copy from the first line HEAD lacks; main() asserts a hunk is not already in HEAD. R115 (the same day):
    # re-anchored again on what the checkpoint af6d63e committed (the R113 / R114 / completion spans).
    "trace_ledger": ("trace_scan_v13.py", '    pathlib.Path("../reviews/NUMBERS_COMPLETION_V1.md"),\n',
                     "    # R115 (2026-09-18, the Knowing-the-Store patch)", "]\n"),
    "prose_header": ("prose_scan.py", 'r"""prose_scan -- R79 plain-language gates for the paper_v2 lineage.\n\n',
                     "R112 (2026-09-16, the integration pass; CLAIMS.md R112 block): rule G4", "R111 (2026-09-15, the writing pass on paper_v18; CLAIMS.md R111 block): rule G4"),
    "prose_g4": ("prose_scan.py", "read (a lifecycle summary|it) by its names and not by its counts",
                 "|attribute names carry most of the (observed )?signal", '"'),
    "hygiene_header": ("hygiene_scan.py", 'r"""hygiene_scan -- the submission is anonymous, Letter, and free of Type 3 fonts.\n\n',
                       "R112 (2026-09-16, the integration pass): CITE_TEXT admits", "R111 (2026-09-15, the writing pass on paper_v18): CITE_TEXT"),
    "hygiene_comment": ("hygiene_scan.py", 'so up to two digit tokens are admitted at each slot.\n',
                        "# R112 (2026-09-16, the integration pass): the same citation", '    r"[AUTHOR-1]'),
    "hygiene_regex": ("hygiene_scan.py", r"[AUTHOR-1](?:\s+\d{1,3}){0,2}\s*(?:&|and)", r"(?:\s+\d{1,3}){0,2}\s*(?:e\.", r"\s*(?:e\."),
    "pins": ("appendix_identity.py", "\n\ndef sections(text):", "# R115 (2026-09-18): pins for the Knowing-the-Store patch", "\n\ndef sections(text):", "before"),
    # R115: refcheck_v11.py retires the nine removed bibliography keys (RETIRED, defined above the verification loop, skipped there,
    # subtracted from the orphan set); three insertions, each after or before a line HEAD holds once.
    "refcheck_retired": ("refcheck_v11.py", "# ---- direction 1: every checked record verifies (v10 logic, unchanged) --------------\n",
                         "# R115 (2026-09-18): the nine bibitems no citation reached", "# ---- direction 1: every checked record verifies (v10 logic, unchanged) --------------\n", "before"),
    "refcheck_skip": ("refcheck_v11.py", "for k in sorted(official):\n",
                      "    if k in RETIRED:\n", "    aid, title, yr, lead = official[k]\n"),
    "refcheck_orphan": ("refcheck_v11.py", "orphan_records = (checked | declared) - present\n",
                        "orphan_records -= RETIRED", "\nprint()"),
}


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
    rel = "iclr2027_monitoring_submission/CLAIMS.md"
    h = head(rel)
    block = (ROOT / "reviews" / "v19" / "claims_r112_block.md").read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n") + "\n"
    if "## R112 AUTHORIZATION BLOCK" in h:
        i = h.index("## R112 AUTHORIZATION BLOCK")
        staged = h[:i] + block
    else:
        staged = h.rstrip("\n") + "\n\n" + block
    print(f"staged {rel}: HEAD with the R112 block, blob {stage(rel, staged)[:12]}")
    # several hunks of one file accumulate: the staged text of a file starts from HEAD once and each hunk is applied to it in turn
    staged_files = {}
    for name in sys.argv[1:]:
        f, anchor, start, end, *mode = HUNKS[name]
        h = staged_files.get(f, head(T + f)); w = work(T + f)
        ins = between(w, start, end)
        assert h.count(anchor) == 1 and ins in w, name
        assert ins.strip() not in h, f"{name}: the hunk is already in HEAD; re-anchor it on the last committed line"
        h = h.replace(anchor, ("\n" + ins + anchor) if mode == ["before"] else (anchor + ins))
        staged_files[f] = h
    for f, text in staged_files.items():
        print(f"staged {T + f}: HEAD + hunks, blob {stage(T + f, text)[:12]}")


if __name__ == "__main__":
    main()
