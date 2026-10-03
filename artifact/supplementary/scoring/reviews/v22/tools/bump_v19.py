# -*- coding: utf-8 -*-
"""bump_v19.py -- create the v19 lineage from the v18 close (program R112, 2026-09-15), the way v17 became v18: copy the v18 sources,
build_v18.py, the tools directory and the ledgers into reviews/v19/, retarget the live helpers to paper_v19.tex, and write the base
record (the tree object holding paper_v18.tex, paper_v18.pdf and SUPPLEMENT.tex as the 4c close built them, with their sha256).

  reviews/v18/src/*.tex             -> reviews/v19/src/ (body_v19.tex, abstract_v19.tex, appendix_v19.tex, moved_tables_v19.tex; amend*_e10.tex as named)
  reviews/v18/tools/*.py            -> reviews/v19/tools/ (build_v19.py retargeted; q_scan, s17_grep, readability_wp default to paper_v19.tex;
                                       frozen_list_wp and number_moves_wp read the v19 base; the wp_phase*, stage_tools_* and pin scripts are
                                       the v18 record and are copied unchanged, never run in v19: README.md in the tools directory says which)
  reviews/v18/NUMBER_MOVES_WP.md    -> reviews/v19/NUMBER_MOVES_WP_v18.md (the inherited dispositions, frozen); reviews/NUMBERS_WP.md stays where it is
  reviews/v18/WRITING_PASS.md       -> reviews/v19/WRITING_PASS.md (the record continues there)

Usage: python reviews/v19/tools/bump_v19.py   (idempotent on the copies; refuses to overwrite an existing base record)
"""
from __future__ import annotations

import hashlib
import os
import pathlib
import re
import shutil
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
V18 = ROOT / "reviews" / "v18"
V19 = ROOT / "reviews" / "v19"

RENAME = {"body_v18.tex": "body_v19.tex", "abstract_v18.tex": "abstract_v19.tex", "appendix_v18.tex": "appendix_v19.tex",
          "moved_tables_v18.tex": "moved_tables_v19.tex"}
HISTORY = ["wp_phase1.py", "wp_phase2.py", "wp_phase3.py", "wp_phase4.py", "wp_phase4b.py", "wp_phase4c.py", "stage_tools_r110.py",
           "stage_tools_r111.py", "stage_tools_wp2.py", "stage_tools_wp3.py", "stage_tools_wp4c.py", "pin_appendix.py", "pin_appendix_wp.py",
           "appendix_v18.py", "claims_r110_pass2.py", "ledger_r110.py", "wording_v17.py", "a1_count_readers.py", "a2_tag_baselines.py",
           "a3_single_draw.py", "a4_pad_extend.py", "wilson_a7.py", "wp_inventory.py", "wp_vlines.py", "frozen_list.py", "number_moves.py"]
LIVE = ["build_v19.py", "q_scan.py", "s17_grep.py", "readability_wp.py", "frozen_list_wp.py", "number_moves_wp.py", "bump_v19.py"]

HEADER_LINE = ("% R112 (2026-09-15): paper_v19.tex, the v19 lineage created from the v18 close (Phase 4c of the writing pass, 5078fe5): the v18\n"
               "% sources copied by reviews/v19/tools/bump_v19.py; Phase 5 (appendix and references), the review-driven additions and Phase 6 land here.\n"
               "% Built by reviews/v19/tools/build_v19.py; CLAIMS.md R112 block; reviews/v19/.\n")


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def wr(p, t):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8", newline="\n")


def rep(t, old, new, n=1):
    assert t.count(old) == n, (t.count(old), old[:80])
    return t.replace(old, new)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def base_tree():
    """A tree object holding the three files as they stand, written with a scratch index (the R110 / R111 technique)."""
    files = ["iclr2027_monitoring_submission/paper_v18.tex", "iclr2027_monitoring_submission/paper_v18.pdf", "iclr2027_monitoring_submission/SUPPLEMENT.tex"]
    fd, idx = tempfile.mkstemp(prefix="v19_base_index_")
    os.close(fd); os.unlink(idx)
    env = dict(os.environ, GIT_INDEX_FILE=idx)
    subprocess.run(["git", "add", "-f", *files], cwd=ROOT, env=env, check=True)
    tree = subprocess.run(["git", "write-tree"], cwd=ROOT, env=env, capture_output=True, text=True, check=True).stdout.strip()
    os.unlink(idx)
    return tree, files


def main():
    assert not (V19 / "base_tree.txt").exists(), "the v19 base record exists; not overwriting"
    # sources
    for src in sorted((V18 / "src").glob("*.tex")):
        name = RENAME.get(src.name, src.name)
        t = rd(src)
        if name == "body_v19.tex":
            anchor = "\\documentclass{article}\n"
            t = rep(t, anchor, HEADER_LINE + anchor)
        wr(V19 / "src" / name, t)
        print(f"src: {src.name} -> {name}")
    # tools
    for src in sorted((V18 / "tools").glob("*.py")):
        name = "build_v19.py" if src.name == "build_v18.py" else src.name
        t = rd(src)
        if name == "build_v19.py":
            t = rep(t, '"""build_v18.py -- assemble iclr2027_monitoring_submission/paper_v18.tex from the v18 sources (CC_PASS_v18, R110).',
                    '"""build_v19.py -- assemble iclr2027_monitoring_submission/paper_v19.tex from the v19 sources (R112; the v18 builder retargeted by bump_v19.py).')
            t = rep(t, 'SRC = ROOT / "reviews" / "v18" / "src"', 'SRC = ROOT / "reviews" / "v19" / "src"')
            t = rep(t, 'OUT = SUB / "paper_v18.tex"', 'OUT = SUB / "paper_v19.tex"')
            t = rep(t, 'read(SRC / "body_v18.tex")', 'read(SRC / "body_v19.tex")')
            t = rep(t, 'read(SRC / "abstract_v18.tex")', 'read(SRC / "abstract_v19.tex")')
            t = rep(t, 'read(SRC / "appendix_v18.tex")', 'read(SRC / "appendix_v19.tex")')
        elif name == "q_scan.py":
            t = rep(t, 'else "paper_v18.tex")', 'else "paper_v19.tex")   # v19 (R112)')
        elif name == "s17_grep.py":
            t = rep(t, 'sys.path.insert(0, str(ROOT / "reviews" / "v18" / "tools"))', 'sys.path.insert(0, str(ROOT / "reviews" / "v19" / "tools"))')
            t = rep(t, 'else "paper_v18.tex")', 'else "paper_v19.tex")   # v19 (R112)')
        elif name == "readability_wp.py":
            t = rep(t, 'else "paper_v18.tex")', 'else "paper_v19.tex")   # v19 (R112)')
        elif name == "frozen_list_wp.py":
            t = rep(t, 'base = FD.norm(FD.git_show(base_rev, "iclr2027_monitoring_submission/paper_v18.tex"))',
                    'base_tex = next((a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--base-tex=")), "paper_v18.tex")   # v19 (R112): the base is the v18 close\n'
                    '    tex = next((a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--tex=")), "paper_v19.tex")\n'
                    '    base = FD.norm(FD.git_show(base_rev, "iclr2027_monitoring_submission/" + base_tex))')
            t = rep(t, 'new_raw = (SUB / "paper_v18.tex").read_text', 'new_raw = (SUB / tex).read_text')
            t = rep(t, 'outside, inside = FD.claims_sections(claims, "R111")',
                    'program = next((a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--program=")), "R112")\n    outside, inside = FD.claims_sections(claims, program)')
        elif name == "number_moves_wp.py":
            t = rep(t, 'TEX = SUB / "paper_v18.tex"', 'TEX = SUB / "paper_v19.tex"   # v19 (R112)')
            t = rep(t, 'OUT = ROOT / "reviews" / "v18" / "NUMBER_MOVES_WP.md"', 'OUT = ROOT / "reviews" / "v19" / "NUMBER_MOVES_V19.md"')
            t = rep(t, 'BASE = (ROOT / "reviews" / "v18" / "base_tree_wp.txt").read_text().strip()', 'BASE = (ROOT / "reviews" / "v19" / "base_tree.txt").read_text().strip()')
            t = rep(t, '"--tex=paper_v18.tex", "--base-tex=paper_v18.tex", "--round2"', '"--tex=paper_v19.tex", "--base-tex=paper_v18.tex", "--round2"')
            # the v19 ledger starts empty: the v18 dispositions are inherited as reviews/v19/NUMBER_MOVES_WP_v18.md
            i = t.index("ADDED = {"); j = t.index("\n}\n", i) + 3
            t = t[:i] + "ADDED = {   # v19 (R112): the v18 dispositions are inherited in reviews/v19/NUMBER_MOVES_WP_v18.md; this ledger starts at the v18 close\n}\n" + t[j:]
            i = t.index("VANISHED = {"); j = t.index("\n}\n", i) + 3
            t = t[:i] + "VANISHED = {\n}\n" + t[j:]
            t = rep(t, '"# NUMBER_MOVES_WP.md: every printed number added or removed by the writing pass on paper_v18 (numeric_diff, --round2, against the pass base)\\n\\n"',
                    '"# NUMBER_MOVES_V19.md: every printed number added or removed in the v19 lineage (numeric_diff, --round2, against the v18 close)\\n\\n"')
            t = rep(t, '"Written by `reviews/v18/tools/number_moves_wp.py` on the built manuscript; the base is the tree object in `reviews/v18/base_tree_wp.txt` ",',
                    '"Written by `reviews/v19/tools/number_moves_wp.py` on the built manuscript; the base is the tree object in `reviews/v19/base_tree.txt` ",')
            t = rep(t, '"(paper_v18.tex after Phase 0, commit 78d8f8b). Each token carries its disposition: where it stands now, or the ledger key it is read from. ",',
                    '"(paper_v18.tex at the Phase 4c close, commit 5078fe5). Each token carries its disposition: where it stands now, or the ledger key it is read from. ",')
            t = rep(t, '"`python reviews/v18/tools/number_moves_wp.py --check` fails if a token is unaccounted for.\\n\\n",',
                    '"`python reviews/v19/tools/number_moves_wp.py --check` fails if a token is unaccounted for.\\n\\n",')
        wr(V19 / "tools" / name, t)
    wr(V19 / "tools" / "README.md",
       "# reviews/v19/tools\n\nCopied from reviews/v18/tools by `bump_v19.py` (R112, 2026-09-15).\n\n"
       "Live in v19 (retargeted to `paper_v19.tex`, `reviews/v19/src`, `reviews/v19/base_tree.txt`): " + ", ".join(f"`{n}`" for n in LIVE) + ".\n\n"
       "The v18 record, copied unchanged and never run in v19 (they regenerate the v18 sources from the v18 commits): " + ", ".join(f"`{n}`" for n in HISTORY) + ".\n")
    # ledgers and the record
    shutil.copyfile(V18 / "NUMBER_MOVES_WP.md", V19 / "NUMBER_MOVES_WP_v18.md")
    wr(V19 / "WRITING_PASS.md", rd(V18 / "WRITING_PASS.md").rstrip("\n") + "\n\n# v19 (program R112): the lineage from the v18 close\n\n"
       "Created by `reviews/v19/tools/bump_v19.py` from the Phase 4c close (`5078fe5`; paper_v18.tex as gates_wp_phase4c.txt records it). The base for\n"
       "frozen_diff, numeric_diff and appendix_identity is `reviews/v19/base_tree.txt` (paper_v18.tex, paper_v18.pdf, SUPPLEMENT.tex; sha256 in\n"
       "`base_files_sha256.txt`); the program is R112 (`claims_r112_block.md`); the inherited number dispositions are `NUMBER_MOVES_WP_v18.md` and the\n"
       "v19 ledger is `NUMBER_MOVES_V19.md`; `reviews/NUMBERS_WP.md` continues (section 6 onward). v18 stays as the build the mock reviewer read.\n")
    # the base record
    tree, files = base_tree()
    wr(V19 / "base_tree.txt", tree + "\n")
    wr(V19 / "base_files_sha256.txt", "".join(f"{sha(ROOT / f)} *{f}\n" for f in files))
    print(f"base tree {tree}")
    for f in files:
        print(f"  {sha(ROOT / f)[:16]} {f}")


if __name__ == "__main__":
    main()
