# -*- coding: utf-8 -*-
"""bump_v23.py -- open the v23 lineage from the R131 close (b3cc631; paper_v22.pdf sha256 ed94f96a, 83 pages, the main text ending on page 9),
the way v22 was opened from the R124 close (program R133, the readability pass, 2026-09-21; the author's brief 'R133: V23 READABILITY PASS'):
copy the v22 sources and the live helpers into reviews/v23/, retarget the helpers to paper_v23.tex, and write the base record (the tree object
holding paper_v22.tex, paper_v22.pdf and SUPPLEMENT.tex as the R131 close built them, with sha256).

  reviews/v22/src/*.tex          -> reviews/v23/src/ (body_v23.tex, abstract_v23.tex, appendix_v23.tex; the data and carried fragments as named);
                                    body_v23.tex gains the lineage header comment. The pass's edits are then applied by reviews/v23/tools/port_r133.py
                                    on top of these copies (every edit asserted; the copies are never hand-edited).
  reviews/v22/tools/<live>.py    -> reviews/v23/tools/ (build_v23.py, run_gates.py, number_moves_wp.py, frozen_list_wp.py, q_scan.py, s17_grep.py,
                                    readability_wp.py, fine.py, section_lines.py retargeted; wp_phase2.py copied unchanged, s17_grep's helper).
                                    The v22 record (port_*.py, appendix_*.py, cost_payers_*.py, ...) is not copied: it stays in reviews/v22/tools
                                    and is never run in v23.
  reviews/v22/NUMBER_MOVES_V22.md -> reviews/v23/NUMBER_MOVES_V22_inherited.md (frozen); the v23 ledger NUMBER_MOVES_V23.md starts empty.
  CLAIMS.md gains an R133 AUTHORIZATION BLOCK (reviews/v23/tools/claims_r133_block.py); frozen_diff runs with --program=R133.

reviews/v22/ stays as committed (never edited in place); v22 is the fallback build.
Usage: python reviews/v23/tools/bump_v23.py [--refresh]
  (idempotent on the copies; refuses to overwrite an existing base record; --refresh re-copies the three sources from v22 only, which is how
   port_r133.py starts from a clean base).
"""
from __future__ import annotations

import hashlib
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
V22 = ROOT / "reviews" / "v22"
V23 = ROOT / "reviews" / "v23"
BASE_COMMIT = "b3cc631"
TEX_SHA = "cb888cd665d0dc77"
PDF_SHA = "ed94f96a82426be5"

RENAME = {"body_v22.tex": "body_v23.tex", "abstract_v22.tex": "abstract_v23.tex", "appendix_v22.tex": "appendix_v23.tex"}
LIVE = ["build_v23.py", "run_gates.py", "number_moves_wp.py", "frozen_list_wp.py", "q_scan.py", "s17_grep.py", "readability_wp.py", "fine.py", "section_lines.py", "wp_phase2.py", "bump_v23.py"]
HEADER = ("% R133 (2026-09-21): paper_v23.tex, the v23 lineage opened from the R131 close (b3cc631; paper_v22.tex as gates_r131_close_f.txt records it,\n"
          "% pdf sha256 ed94f96a): the v22 sources copied by reviews/v23/tools/bump_v23.py and edited by reviews/v23/tools/port_r133.py (the readability\n"
          "% pass: bookkeeping hedges to the appendix, the author's claim-narrowing swaps, Sections 4 to 8 rewritten; no number changes). v22 stays as\n"
          "% committed, the fallback build. Built by reviews/v23/tools/build_v23.py; CLAIMS.md R133 block; reviews/v23/.\n")


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def wr(p, t):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8", newline="\n")


def rep(t, old, new, n=1):
    assert t.count(old) == n, (t.count(old), n, old[:80])
    return t.replace(old, new)


def rep_all(t, old, new):
    assert old in t, old[:80]
    return t.replace(old, new)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def base_tree():
    files = ["iclr2027_monitoring_submission/paper_v22.tex", "iclr2027_monitoring_submission/paper_v22.pdf", "iclr2027_monitoring_submission/SUPPLEMENT.tex"]
    fd, idx = tempfile.mkstemp(prefix="v23_base_index_")
    os.close(fd); os.unlink(idx)
    env = dict(os.environ, GIT_INDEX_FILE=idx)
    subprocess.run(["git", "add", "-f", *files], cwd=ROOT, env=env, check=True)
    tree = subprocess.run(["git", "write-tree"], cwd=ROOT, env=env, capture_output=True, text=True, check=True).stdout.strip()
    os.unlink(idx)
    return tree, files


def copy_sources():
    for src in sorted((V22 / "src").glob("*.tex")):
        name = RENAME.get(src.name, src.name)
        t = rd(src)
        if name == "body_v23.tex":
            t = rep(t, "\\documentclass{article}\n", HEADER + "\\documentclass{article}\n")
        wr(V23 / "src" / name, t)
        print(f"src: {src.name} -> {name}")


def main():
    if "--refresh" in sys.argv:
        copy_sources()
        return
    assert not (V23 / "base_tree.txt").exists(), "the v23 base record exists; not overwriting"
    d = subprocess.run(["git", "diff", "--stat", BASE_COMMIT, "--", "reviews/v22/src"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    assert not d, f"reviews/v22/src differs from {BASE_COMMIT}:\n{d}"
    assert sha(SUB / "paper_v22.tex").startswith(TEX_SHA), "paper_v22.tex is not the gates_r131_close_f build"
    assert sha(SUB / "paper_v22.pdf").startswith(PDF_SHA), "paper_v22.pdf is not the gates_r131_close_f build"
    copy_sources()
    for name in LIVE:
        if name == "bump_v23.py":
            continue
        src = V22 / "tools" / ("build_v22.py" if name == "build_v23.py" else name)
        t = rd(src)
        if name == "build_v23.py":
            t = rep(t, '"""build_v22.py -- assemble iclr2027_monitoring_submission/paper_v22.tex from the v22 sources (R126; the v21 builder retargeted by bump_v22.py).',
                    '"""build_v23.py -- assemble iclr2027_monitoring_submission/paper_v23.tex from the v23 sources (R133; the v22 builder retargeted by bump_v23.py).')
            t = rep(t, 'SRC = ROOT / "reviews" / "v22" / "src"', 'SRC = ROOT / "reviews" / "v23" / "src"')
            t = rep(t, 'OUT = SUB / "paper_v22.tex"', 'OUT = SUB / "paper_v23.tex"')
            t = rep(t, 'read(SRC / "body_v22.tex")', 'read(SRC / "body_v23.tex")')
            t = rep(t, 'read(SRC / "abstract_v22.tex")', 'read(SRC / "abstract_v23.tex")')
            t = rep(t, 'read(SRC / "appendix_v22.tex")', 'read(SRC / "appendix_v23.tex")')
            t = rep(t, "  reviews/v22/src/body_v22.tex      the preamble", "  reviews/v23/src/body_v23.tex      the preamble")
            t = rep(t, "  reviews/v22/src/abstract_v22.tex  the abstract", "  reviews/v23/src/abstract_v23.tex  the abstract")
            t = rep(t, "  reviews/v22/src/fig3_data.tex     Figure 3's data", "  reviews/v23/src/fig3_data.tex     Figure 3's data")
            t = rep(t, "  reviews/v22/src/appendix_v22.tex  the appendices' prose", "  reviews/v23/src/appendix_v23.tex  the appendices' prose")
        elif name == "run_gates.py":
            t = rep_all(t, "paper_v22", "paper_v23")
            t = rep_all(t, "paper_v21", "paper_v22")           # the base manuscript (frozen_diff --base-tex, appendix_identity --base, frozen_list_wp)
            t = rep_all(t, 'ROOT / "reviews" / "v22"', 'ROOT / "reviews" / "v23"')
            t = rep_all(t, "reviews/v22/", "reviews/v23/")
            t = rep_all(t, "--program=R126", "--program=R133")
            t = rep_all(t, 'prefix="v22_rb_"', 'prefix="v23_rb_"')
            t = rep_all(t, 'tmp.name.startswith("v22_rb_")', 'tmp.name.startswith("v23_rb_")')
            t = rep_all(t, "(program R126), base tree {BASE} (paper_v22.tex at the R124 close, ee6b735)", "(program R133), base tree {BASE} (paper_v22.tex at the R131 close, b3cc631)")
            t = rep(t, '"""run_gates.py -- the gate battery on paper_v23.tex (program R126; the v21 runner retargeted by bump_v22.py)', '"""run_gates.py -- the gate battery on paper_v23.tex (program R133; the v22 runner retargeted by bump_v23.py)')
            t = rep_all(t, "build_v22.py", "build_v23.py")
        elif name == "number_moves_wp.py":
            t = rep(t, 'TEX = SUB / "paper_v22.tex"   # v22 (R126)', 'TEX = SUB / "paper_v23.tex"   # v23 (R133)')
            t = rep(t, 'OUT = ROOT / "reviews" / "v22" / "NUMBER_MOVES_V22.md"', 'OUT = ROOT / "reviews" / "v23" / "NUMBER_MOVES_V23.md"')
            t = rep(t, 'BASE = (ROOT / "reviews" / "v22" / "base_tree.txt").read_text().strip()', 'BASE = (ROOT / "reviews" / "v23" / "base_tree.txt").read_text().strip()')
            t = rep(t, '"--tex=paper_v22.tex", "--base-tex=paper_v21.tex", "--round2"', '"--tex=paper_v23.tex", "--base-tex=paper_v22.tex", "--round2"')
            i = t.index("ADDED = {")
            k = t.index("\ndef generated():")
            t = t[:i] + "ADDED = {   # v23 (R133): the v22 dispositions are inherited in reviews/v23/NUMBER_MOVES_V22_inherited.md; this ledger starts at the R131 close\n}\nVANISHED = {\n}\n" + t[k:]
            t = rep_all(t, "# NUMBER_MOVES_V22.md: every printed number added or removed in the v22 lineage (numeric_diff, --round2, against the R124 close)",
                        "# NUMBER_MOVES_V23.md: every printed number added or removed in the v23 lineage (numeric_diff, --round2, against the R131 close)")
            t = rep_all(t, "Written by `reviews/v22/tools/number_moves_wp.py` on the built manuscript; the base is the tree object in `reviews/v22/base_tree.txt` ",
                        "Written by `reviews/v23/tools/number_moves_wp.py` on the built manuscript; the base is the tree object in `reviews/v23/base_tree.txt` ")
            t = rep_all(t, "(paper_v21.tex at the R124 close, ee6b735).", "(paper_v22.tex at the R131 close, b3cc631).")
            t = rep_all(t, "`python reviews/v22/tools/number_moves_wp.py --check`", "`python reviews/v23/tools/number_moves_wp.py --check`")
            t = rep_all(t, "lines in paper_v22.tex", "lines in paper_v23.tex")
            t = rep_all(t, "missing from NUMBER_MOVES_V22.md", "missing from NUMBER_MOVES_V23.md")
        elif name == "frozen_list_wp.py":
            t = rep(t, 'if a.startswith("--base-tex=")), "paper_v21.tex")', 'if a.startswith("--base-tex=")), "paper_v22.tex")')
            t = rep(t, 'if a.startswith("--tex=")), "paper_v22.tex")', 'if a.startswith("--tex=")), "paper_v23.tex")')
            t = rep(t, 'if a.startswith("--program=")), "R126")', 'if a.startswith("--program=")), "R133")')
        elif name in ("q_scan.py", "readability_wp.py"):
            t = rep(t, 'else "paper_v22.tex")', 'else "paper_v23.tex")')
        elif name == "s17_grep.py":
            t = rep(t, 'sys.path.insert(0, str(ROOT / "reviews" / "v22" / "tools"))', 'sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))')
            t = rep(t, 'else "paper_v22.tex")', 'else "paper_v23.tex")')
        elif name in ("fine.py", "section_lines.py"):
            t = rep_all(t, "paper_v22", "paper_v23")
            t = rep_all(t, '"reviews" / "v22"', '"reviews" / "v23"')
            t = t.replace("build_v22", "build_v23")
        elif name == "wp_phase2.py":
            pass   # copied unchanged: s17_grep.py imports is_frozen from it (its own v18 paths are used only by its main())
        wr(V23 / "tools" / name, t)
        print(f"tools: {src.name} -> {name}")
    wr(V23 / "tools" / "README.md",
       "# reviews/v23/tools\n\nOpened from reviews/v22/tools by `bump_v23.py` (R133, 2026-09-21).\n\n"
       "Live in v23 (retargeted to `paper_v23.tex`, `reviews/v23/src`, `reviews/v23/base_tree.txt`, program R133): " + ", ".join(f"`{n}`" for n in LIVE) + ".\n\n"
       "The v22 record (port_v22.py, port_r131*.py, appendix_r1*.py, cost_payers_*.py, ledger_*.py, claims_r126_block.py, pin_appendix_r126.py and the rest) stays in "
       "reviews/v22/tools and is never run in v23: the v23 sources are the v22 close's sources copied, not regenerated.\n\n"
       "New in v23 (R133): `port_r133.py` (the pass's edits on the copied sources, unit by unit, every edit asserted), `r133_number_gate.py` (the number gate on every "
       "number the pass's new texts print), `claims_r133_block.py` (the R133 block of CLAIMS.md), `pin_appendix_r133.py` (appendix_identity pins), `slack_r133.py` "
       "(the slack probe), `changes_r133.py` (OLD_BESIDE_NEW_V23.md), `counts_r133.py` (the report's counts).\n\n"
       "Regenerating v23 from the sources: `python reviews/v23/tools/bump_v23.py --refresh && python reviews/v23/tools/port_r133.py --units=<list> && python reviews/v23/tools/run_gates.py <tag>`.\n")
    shutil.copyfile(V22 / "NUMBER_MOVES_V22.md", V23 / "NUMBER_MOVES_V22_inherited.md")
    tree, files = base_tree()
    wr(V23 / "base_tree.txt", tree + "\n")
    wr(V23 / "base_files_sha256.txt", "".join(f"{sha(ROOT / f)} *{f}\n" for f in files))
    wr(V23 / "LINEAGE_V23.md",
       "# v23 (program R133): the lineage from the R131 close\n\n"
       f"Opened 2026-09-21 by `reviews/v23/tools/bump_v23.py` from `{BASE_COMMIT}` (paper_v22.tex as `reviews/v22/gates_r131_close_f.txt` records it: tex sha256\n"
       f"{TEX_SHA}, pdf sha256 {PDF_SHA}, 83 pages, the main text ending on page 9). The base for frozen_diff, numeric_diff and appendix_identity is\n"
       "`reviews/v23/base_tree.txt` (paper_v22.tex, paper_v22.pdf, SUPPLEMENT.tex; sha256 in `base_files_sha256.txt`); the program is R133 (CLAIMS.md R133 block);\n"
       "the inherited number dispositions are `NUMBER_MOVES_V22_inherited.md` and the v23 ledger is `NUMBER_MOVES_V23.md`. The pass is the author's brief\n"
       "'R133: V23 READABILITY PASS' (hedges to the appendix, claims narrowed, Sections 4 to 8 rewritten; no number changes, no new experiments, no API calls);\n"
       "its edits are `reviews/v23/tools/port_r133.py` on the copied v22 sources. reviews/v22/ is never edited in place and is the fallback build.\n")
    print(f"base tree {tree}")
    for f in files:
        print(f"  {sha(ROOT / f)[:16]} {f}")


if __name__ == "__main__":
    main()
