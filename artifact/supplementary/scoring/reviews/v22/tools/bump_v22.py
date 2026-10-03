# -*- coding: utf-8 -*-
"""bump_v22.py -- open the v22 lineage from the R124 close (ee6b735), the way v21 was opened from the R116 commit (program R126, 2026-09-19):
copy the v21 sources, the tools directory and the ledgers into reviews/v22/, retarget the live helpers to paper_v22.tex, and write the
base record (the tree object holding paper_v21.tex, paper_v21.pdf and SUPPLEMENT.tex as the R124 gate run built them, with sha256).

  reviews/v21/src/*.tex          -> reviews/v22/src/ (body_v22.tex, abstract_v22.tex, appendix_v22.tex; amend*_e10.tex as named);
                                    body_v22.tex gains the lineage header comment. The body is then replaced, section by section, by the
                                    readable body of reviews/v22/inbox/ (the port is reviews/v22/tools/port_v22.py); the appendix is
                                    repaired in place (reviews/v22/tools/appendix_r126.py).
  reviews/v21/tools/*.py         -> reviews/v22/tools/ (build_v22.py, run_gates.py, number_moves_wp.py, frozen_list_wp.py, q_scan.py,
                                    s17_grep.py, readability_wp.py, fine.py, section_lines.py retargeted; every other script is the v21
                                    record, copied unchanged and never run in v22: README.md says which)
  reviews/v21/NUMBER_MOVES_V21.md -> reviews/v22/NUMBER_MOVES_V21_inherited.md (frozen); the v22 ledger NUMBER_MOVES_V22.md starts empty
  reviews/v21/claims_r123_block.md is not carried: v22's authorizations go in a new R126 block of CLAIMS.md (frozen_diff --program=R126)

reviews/v21/ stays as committed (never edited in place); v21 is the fallback build, tagged fallback/v22-pre-restructure at ee6b735.
Usage: python reviews/v22/tools/bump_v22.py   (idempotent on the copies; refuses to overwrite an existing base record).
"""
from __future__ import annotations

import hashlib
import os
import pathlib
import shutil
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
V21 = ROOT / "reviews" / "v21"
V22 = ROOT / "reviews" / "v22"
BASE_COMMIT = "ee6b735"

RENAME = {"body_v21.tex": "body_v22.tex", "abstract_v21.tex": "abstract_v22.tex", "appendix_v21.tex": "appendix_v22.tex"}
LIVE = ["build_v22.py", "run_gates.py", "number_moves_wp.py", "frozen_list_wp.py", "q_scan.py", "s17_grep.py", "readability_wp.py", "fine.py", "section_lines.py", "bump_v22.py"]
HEADER = ("% R126 (2026-09-19): paper_v22.tex, the v22 lineage opened from the R124 close (ee6b735; paper_v21.tex as gates_r124_f.txt records it):\n"
          "% the v21 sources copied by reviews/v22/tools/bump_v22.py. The main text is the readable body of reviews/v22/inbox/ ported section by\n"
          "% section (reviews/v22/tools/port_v22.py); the statements, the references and the appendix are ours. v21 stays as committed, the\n"
          "% fallback build (tag fallback/v22-pre-restructure). Built by reviews/v22/tools/build_v22.py; CLAIMS.md R126 block; reviews/v22/.\n")


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
    files = ["iclr2027_monitoring_submission/paper_v21.tex", "iclr2027_monitoring_submission/paper_v21.pdf", "iclr2027_monitoring_submission/SUPPLEMENT.tex"]
    fd, idx = tempfile.mkstemp(prefix="v22_base_index_")
    os.close(fd); os.unlink(idx)
    env = dict(os.environ, GIT_INDEX_FILE=idx)
    subprocess.run(["git", "add", "-f", *files], cwd=ROOT, env=env, check=True)
    tree = subprocess.run(["git", "write-tree"], cwd=ROOT, env=env, capture_output=True, text=True, check=True).stdout.strip()
    os.unlink(idx)
    return tree, files


def main():
    assert not (V22 / "base_tree.txt").exists(), "the v22 base record exists; not overwriting"
    # the sources must be the R124 close's
    d = subprocess.run(["git", "diff", "--stat", BASE_COMMIT, "--", "reviews/v21/src"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    assert not d, f"reviews/v21/src differs from {BASE_COMMIT}:\n{d}"
    # the base build must be the one gates_r124_f.txt records
    assert sha(SUB / "paper_v21.tex").startswith("2c29b092401d63f8"), "paper_v21.tex is not the gates_r124_f build"
    assert sha(SUB / "paper_v21.pdf").startswith("6f9d859a0b1dc650"), "paper_v21.pdf is not the gates_r124_f build"
    for src in sorted((V21 / "src").glob("*.tex")):
        name = RENAME.get(src.name, src.name)
        t = rd(src)
        if name == "body_v22.tex":
            t = rep(t, "\\documentclass{article}\n", HEADER + "\\documentclass{article}\n")
        wr(V22 / "src" / name, t)
        print(f"src: {src.name} -> {name}")
    for src in sorted((V21 / "tools").glob("*.py")):
        name = "build_v22.py" if src.name == "build_v21.py" else src.name
        if name in ("bump_v22.py", "bump_v21.py"):
            continue
        t = rd(src)
        if name == "build_v22.py":
            t = rep(t, '"""build_v21.py -- assemble iclr2027_monitoring_submission/paper_v21.tex from the v21 sources (R118; the v19 builder retargeted by bump_v21.py).',
                    '"""build_v22.py -- assemble iclr2027_monitoring_submission/paper_v22.tex from the v22 sources (R126; the v21 builder retargeted by bump_v22.py).')
            t = rep(t, 'SRC = ROOT / "reviews" / "v21" / "src"', 'SRC = ROOT / "reviews" / "v22" / "src"')
            t = rep(t, 'OUT = SUB / "paper_v21.tex"', 'OUT = SUB / "paper_v22.tex"')
            t = rep(t, 'read(SRC / "body_v21.tex")', 'read(SRC / "body_v22.tex")')
            t = rep(t, 'read(SRC / "abstract_v21.tex")', 'read(SRC / "abstract_v22.tex")')
            t = rep(t, 'read(SRC / "appendix_v21.tex")', 'read(SRC / "appendix_v22.tex")')
        elif name == "run_gates.py":
            t = rep_all(t, "paper_v21", "paper_v22")
            t = rep_all(t, 'ROOT / "reviews" / "v21"', 'ROOT / "reviews" / "v22"')
            t = rep_all(t, "reviews/v21/", "reviews/v22/")
            t = rep_all(t, "--program=R118", "--program=R126")
            t = rep_all(t, "--base-tex=paper_v19.tex", "--base-tex=paper_v21.tex")
            t = rep_all(t, "--base=iclr2027_monitoring_submission/paper_v19.tex", "--base=iclr2027_monitoring_submission/paper_v21.tex")
            t = rep_all(t, 'prefix="v21_rb_"', 'prefix="v22_rb_"')
            t = rep_all(t, 'tmp.name.startswith("v21_rb_")', 'tmp.name.startswith("v22_rb_")')
            t = rep_all(t, "(program R118), base tree {BASE} (paper_v19.tex at the R116 commit, e439141)", "(program R126), base tree {BASE} (paper_v21.tex at the R124 close, ee6b735)")
            t = rep(t, '"""run_gates.py -- the gate battery on paper_v22.tex (program R118; the v19 runner retargeted by bump_v21.py)', '"""run_gates.py -- the gate battery on paper_v22.tex (program R126; the v21 runner retargeted by bump_v22.py)')
            t = rep_all(t, "build_v21.py", "build_v22.py")
        elif name == "number_moves_wp.py":
            t = rep(t, 'TEX = SUB / "paper_v21.tex"   # v21 (R118)', 'TEX = SUB / "paper_v22.tex"   # v22 (R126)')
            t = rep(t, 'OUT = ROOT / "reviews" / "v21" / "NUMBER_MOVES_V21.md"', 'OUT = ROOT / "reviews" / "v22" / "NUMBER_MOVES_V22.md"')
            t = rep(t, 'BASE = (ROOT / "reviews" / "v21" / "base_tree.txt").read_text().strip()', 'BASE = (ROOT / "reviews" / "v22" / "base_tree.txt").read_text().strip()')
            t = rep(t, '"--tex=paper_v21.tex", "--base-tex=paper_v19.tex", "--round2"', '"--tex=paper_v22.tex", "--base-tex=paper_v21.tex", "--round2"')
            i = t.index("ADDED = {")
            k = t.index("\ndef generated():")
            # the v22 ledger starts empty: every v21 disposition is inherited as reviews/v22/NUMBER_MOVES_V21_inherited.md
            t = t[:i] + "ADDED = {   # v22 (R126): the v21 dispositions are inherited in reviews/v22/NUMBER_MOVES_V21_inherited.md; this ledger starts at the R124 close\n}\nVANISHED = {\n}\n" + t[k:]
            t = rep_all(t, "# NUMBER_MOVES_V21.md: every printed number added or removed in the v21 lineage (numeric_diff, --round2, against the R116 commit)",
                        "# NUMBER_MOVES_V22.md: every printed number added or removed in the v22 lineage (numeric_diff, --round2, against the R124 close)")
            t = rep_all(t, "Written by `reviews/v21/tools/number_moves_wp.py` on the built manuscript; the base is the tree object in `reviews/v21/base_tree.txt` ",
                        "Written by `reviews/v22/tools/number_moves_wp.py` on the built manuscript; the base is the tree object in `reviews/v22/base_tree.txt` ")
            t = rep_all(t, "(paper_v19.tex at the R116 commit, e439141).", "(paper_v21.tex at the R124 close, ee6b735).")
            t = rep_all(t, "`python reviews/v21/tools/number_moves_wp.py --check`", "`python reviews/v22/tools/number_moves_wp.py --check`")
            t = rep_all(t, "lines in paper_v19.tex", "lines in paper_v22.tex")
            t = rep_all(t, "missing from NUMBER_MOVES_V21.md", "missing from NUMBER_MOVES_V22.md")
        elif name == "frozen_list_wp.py":
            t = rep(t, 'if a.startswith("--base-tex=")), "paper_v19.tex")', 'if a.startswith("--base-tex=")), "paper_v21.tex")')
            t = rep(t, 'if a.startswith("--tex=")), "paper_v21.tex")', 'if a.startswith("--tex=")), "paper_v22.tex")')
            t = rep(t, 'if a.startswith("--program=")), "R118")', 'if a.startswith("--program=")), "R126")')
        elif name in ("q_scan.py", "readability_wp.py"):
            t = rep(t, 'else "paper_v21.tex")', 'else "paper_v22.tex")')
        elif name == "s17_grep.py":
            t = rep(t, 'sys.path.insert(0, str(ROOT / "reviews" / "v21" / "tools"))', 'sys.path.insert(0, str(ROOT / "reviews" / "v22" / "tools"))')
            t = rep(t, 'else "paper_v21.tex")', 'else "paper_v22.tex")')
        elif name in ("fine.py", "section_lines.py"):
            t = rep_all(t, "paper_v21", "paper_v22")
            t = rep_all(t, '"reviews" / "v21"', '"reviews" / "v22"')
            t = t.replace("build_v21", "build_v22")
        wr(V22 / "tools" / name, t)
    hist = sorted(p.name for p in (V22 / "tools").glob("*.py") if p.name not in LIVE)
    wr(V22 / "tools" / "README.md",
       "# reviews/v22/tools\n\nCopied from reviews/v21/tools by `bump_v22.py` (R126, 2026-09-19).\n\n"
       "Live in v22 (retargeted to `paper_v22.tex`, `reviews/v22/src`, `reviews/v22/base_tree.txt`, program R126): " + ", ".join(f"`{n}`" for n in LIVE) + ".\n\n"
       "The v21 record, copied unchanged and never run in v22: " + ", ".join(f"`{n}`" for n in hist) + ".\n\n"
       "New in v22: `port_v22.py` (the readable body ported into body_v22.tex and abstract_v22.tex), `appendix_r126.py` (the appendix repairs), "
       "`fig3_data.py` and `reviews/v22/src/fig3_data.tex` (Figure 3 from the ledger), `claims_r126_block.py`, `pin_appendix_r126.py`, `body_map_r126.py`.\n")
    shutil.copyfile(V21 / "NUMBER_MOVES_V21.md", V22 / "NUMBER_MOVES_V21_inherited.md")
    tree, files = base_tree()
    wr(V22 / "base_tree.txt", tree + "\n")
    wr(V22 / "base_files_sha256.txt", "".join(f"{sha(ROOT / f)} *{f}\n" for f in files))
    wr(V22 / "LINEAGE_V22.md",
       "# v22 (program R126): the lineage from the R124 close\n\n"
       f"Opened 2026-09-19 by `reviews/v22/tools/bump_v22.py` from `{BASE_COMMIT}` (paper_v21.tex as `reviews/v21/gates_r124_f.txt` records it; HEAD tagged\n"
       "`fallback/v22-pre-restructure`). The base for frozen_diff, numeric_diff and appendix_identity is `reviews/v22/base_tree.txt` (paper_v21.tex,\n"
       "paper_v21.pdf, SUPPLEMENT.tex; sha256 in `base_files_sha256.txt`; tag `base-tree/v22`); the program is R126 (CLAIMS.md R126 block); the\n"
       "inherited number dispositions are `NUMBER_MOVES_V21_inherited.md` and the v22 ledger is `NUMBER_MOVES_V22.md`. The main text of v22 is the\n"
       "readable body delivered to `reviews/v22/inbox/` (v22_readable_main.tex; no PDF, ledger, sentence map or key list was delivered), ported by\n"
       "`reviews/v22/tools/port_v22.py`; the inbox text is a draft to port, not a file to trust, and every number and pointer is checked by the gates.\n"
       "reviews/v21/ is never edited in place; reviews/r125/ belongs to the R125 session and nothing from it lands here.\n")
    print(f"base tree {tree}")
    for f in files:
        print(f"  {sha(ROOT / f)[:16]} {f}")


if __name__ == "__main__":
    main()
