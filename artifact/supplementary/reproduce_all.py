# -*- coding: utf-8 -*-
"""reproduce_all.py -- check every number the paper prints, offline, and regenerate what can be
regenerated from the stored scores. See "What 'reproduce' means here" in README.md: not every
printed number is recomputed from raw data, and this script does not claim it is.

No API key. No network. No GPU. No LaTeX. Nothing outside the working directory is written.

What it does, in order:

  0. materialise    rebuild one working tree from the package's sections, using PATHMAP.tsv
                    (package path -> repo-relative path) and DUPLICATES.tsv (repo-relative paths
                    whose bytes are shared with another). The package stores each distinct file
                    once; the working tree restores every logical path the scripts expect.
  1. manifest       every file in the package against MANIFEST.sha256.
  2. regenerate     the scoring, ledger and table-fragment scripts, in dependency order, each
                    writing into the working tree; every declared output is then compared BYTE
                    FOR BYTE with the copy shipped in the package.
  3. gates          the paper's own number gates against paper_v23.tex: r141_number_gate (which
                    chains R140's, R139's, R137's, R135's and R134's checks), trace_scan_v13 and refcheck_v11.

Exit status is the check: 0 only if every comparison is byte-identical and every gate passes.

  python reproduce_all.py [--work DIR] [--skip-manifest]
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys
import time

PKG = pathlib.Path(__file__).resolve().parent
PY = sys.executable

# ---------------------------------------------------------------------------
# (label, argv relative to the working tree, cwd relative to it, declared outputs)
#
# An output marked with a tolerance is compared after the named pattern is normalised; the
# tolerance is printed, so nothing is silently forgiven. Everything else must be byte-identical.

TODAY = re.compile(r"\b20\d\d-\d\d-\d\d\b")

# One authored edit is applied to a generated fragment after its generator runs. It is named
# here, in full, so the difference it accounts for is declared rather than forgiven: R137's
# payer P1 moved this sentence out of Section 5.2 into the table's caption, and
# reviews/v23/tools/port_r137.py re-applies it after robust_tex.py regenerates the file.
P1_CAPTION = [" In row 9 retraction and expiry do not move, since the list names neither."]
# R140 rebuild: R139's payer P9 moved the table's per-row notes out of its caption into Appendix C.2;
# reviews/r139/tools/port_r139.py removes them after robust_tex.py regenerates the file. A tuple
# (text in the produced file, what the shipped file has instead) declares that second edit.
P9_NOTES = ("Pooled AUROC on the counterfactual set unless noted: rows 2 and 5 matched and post hoc ($^{p}$), row 5 on the $60$ counted-state pairs; "
            "row 3 the \\pn{} version against its sibling, matched, on the $88$ supersession pairs; row 7 the $115$ reworded pairs; row 9 the $88$ supersession "
            "triples, the lists padded to $60$ names, Opus at one draw against its five-draw row; row 10 the full obligation set. ", "")
P1_CAPTION = P1_CAPTION + [P9_NOTES]

STEPS = [
    ("CF-PAD: score the long-list check from its rows",
     ["cf_pad/tools/score_cf_pad.py"], ".",
     ["cf_pad/results/cf_pad_scores.json"], None, None),
    ("CF-PAD: the ledger and the printed forms",
     ["cf_pad/tools/report_cf_pad.py"], ".",
     ["cf_pad/results/cf_pad_printed.json", "cf_pad/NUMBERS_CF_PAD.md"], TODAY, None),
    ("CF-PAD: Appendix C.2's six table fragments",
     ["cf_pad/tools/cfpad_tex.py"], ".",
     ["cf_pad/results/cfpad_tab_sup.tex", "cf_pad/results/cfpad_tab_minus-lookup.tex",
      "cf_pad/results/cfpad_tab_whole.tex", "cf_pad/results/cfpad_tab_counted.tex",
      "cf_pad/results/cfpad_tab_other-lookups.tex", "cf_pad/results/cfpad_tab_position.tex",
      "cf_pad/results/cfpad_printed.json"], None, None),
    # PARA's lookup comparator is encoded at scoring time and has no on-disk vector cache, so
    # re-deriving para_scores.json from the rows needs the MiniLM encoder. Every number the
    # paper prints from PARA is regenerated from the stored score by the three steps that
    # follow, all of which run without it. Install requirements-runners.txt to include this one.
    ("PARA: score the paraphrase check from its rows (needs the encoder)",
     ["cf2_paraphrase/tools/score_para.py", "score"], ".",
     ["cf2_paraphrase/results/para_scores.json"], None, "sentence_transformers"),
    ("PARA: the ledger sections",
     ["cf2_paraphrase/tools/ledger_para.py"], ".",
     ["cf2_paraphrase/NUMBERS_PARA.md"], TODAY, None),
    ("PARA: Appendix C.2's six table fragments",
     ["cf2_paraphrase/tools/para_tex.py"], ".",
     ["cf2_paraphrase/results/para_tab_pooled.tex", "cf2_paraphrase/results/para_tab_matched.tex",
      "cf2_paraphrase/results/para_tab_minus-lookup.tex", "cf2_paraphrase/results/para_tab_sup.tex",
      "cf2_paraphrase/results/para_tab_sens.tex", "cf2_paraphrase/results/para_tab_flags.tex",
      "cf2_paraphrase/results/para_printed.json"], None, None),
    ("Figure 3: the pooled data file",
     ["reviews/v22/tools/fig3_data.py"], ".",
     ["reviews/v22/src/fig3_data.tex"], None, None),
    ("Figure 3: the matched data file",
     ["reviews/v22/tools/fig3_data_r131.py"], ".",
     ["reviews/v22/src/fig3_data_matched.tex"], None, None),
    ("Table 'robust': the robustness table",
     ["reviews/v23/tools/robust_tex.py"], ".",
     ["reviews/v23/results/robust_printed.json"], None, None),
    ("Table 'robust': the fragment, with R137's and R139's declared caption edits",
     ["reviews/v23/tools/robust_tex.py"], ".",
     ["reviews/v23/src/robust_table.tex"], P1_CAPTION, None),
]

GATES = [
    ("r141_number_gate (R140's, R139's, R137's, R135's and R134's checks included)",
     ["reviews/r141/tools/r141_number_gate.py", "--built"], "."),
    ("trace_scan_v13 (every printed number against a ledger)",
     ["tools/trace_scan_v13.py", "paper_v23.tex"], "iclr2027_monitoring_submission"),
    ("refcheck_v11 (every citation)",
     ["tools/refcheck_v11.py", "paper_v23.tex"], "iclr2027_monitoring_submission"),
]


def read_map(name: str):
    rows = []
    for line in (PKG / name).read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) == 2:
            rows.append((parts[0], parts[1]))
    return rows


def materialise(work: pathlib.Path):
    """package section paths -> one repo-relative working tree."""
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    shipped = {}
    n = 0
    for pkg_rel, repo_rel in read_map("PATHMAP.tsv"):
        if not repo_rel:
            continue
        src = PKG / pkg_rel
        if not src.is_file():
            continue
        dst = work / repo_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        shipped[repo_rel] = src
        n += 1
    for repo_rel, shares_with in read_map("DUPLICATES.tsv"):
        src = shipped.get(shares_with)
        if src is None:
            continue
        dst = work / repo_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        shipped[repo_rel] = src
        n += 1
    # the scripts write reports into directories the package does not carry
    for d in ("reviews/r136", "reviews/para", "reviews/v23/results"):
        (work / d).mkdir(parents=True, exist_ok=True)
    return shipped, n


def check_manifest() -> tuple:
    ok = bad = 0
    missing = []
    for line in (PKG / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        want, rel = line.split("  ", 1)
        p = PKG / rel
        if not p.is_file():
            missing.append(rel)
            continue
        if hashlib.sha256(p.read_bytes()).hexdigest() == want:
            ok += 1
        else:
            bad += 1
            missing.append(rel + "  (hash differs)")
    return ok, bad, missing


def compare(work: pathlib.Path, shipped: dict, rel: str, tol):
    src = shipped.get(rel)
    produced = work / rel
    if src is None:
        return "not-shipped", ""
    if not produced.is_file():
        return "MISSING", "the step wrote no such file"
    a, b = src.read_bytes(), produced.read_bytes()
    if a == b:
        return "identical", ""
    if tol is not None:
        ta, tb = a.decode("utf-8", "replace"), b.decode("utf-8", "replace")
        if isinstance(tol, list):
            for s in tol:
                if isinstance(s, tuple):          # R140: (in the produced file, in the shipped file)
                    tb = tb.replace(s[0], s[1], 1)
                else:
                    ta = ta.replace(s, "", 1)
            if ta == tb:
                return "identical-modulo-edit", "the declared authored edit accounts for it"
        else:
            if tol.sub("<date>", ta) == tol.sub("<date>", tb):
                return "identical-modulo-date", "only a run-date line differs"
    return "DIFFERS", f"{len(a)} shipped bytes against {len(b)} produced"


def have(mod: str) -> bool:
    import importlib.util
    return importlib.util.find_spec(mod) is not None


def run(argv, cwd):
    t = time.time()
    r = subprocess.run([PY] + argv, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout + r.stderr).strip(), time.time() - t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=str(PKG.parent / "kts_work"))
    ap.add_argument("--skip-manifest", action="store_true")
    a = ap.parse_args()
    work = pathlib.Path(a.work).resolve()
    t0 = time.time()
    fails = []
    skipped = []

    print(f"package      {PKG}")
    print(f"working tree {work}")
    print(f"python       {sys.version.split()[0]}")
    print()

    if not a.skip_manifest:
        ok, bad, missing = check_manifest()
        print(f"[1] MANIFEST.sha256: {ok} file(s) match, {bad} differ, "
              f"{len([m for m in missing if 'hash differs' not in m])} missing")
        if bad or missing:
            fails.append("manifest")
            for m in missing[:10]:
                print(f"      {m}")
        print()

    shipped, n = materialise(work)
    print(f"[0] materialised {n} file(s) into the working tree")
    print()

    print("[2] regeneration, each output compared byte for byte with the shipped copy")
    for label, argv, cwd, outs, tol, needs in STEPS:
        if needs and not have(needs):
            print(f"  {label}  [skip] {needs} is not installed; "
                  f"see requirements-runners.txt. The printed numbers do not depend on it.")
            skipped.append(label)
            continue
        rc, out, secs = run(argv, work / cwd)
        head = f"  {label}  ({secs:.1f}s)"
        if rc != 0:
            print(f"{head}  STEP FAILED rc={rc}")
            print("      " + "\n      ".join(out.splitlines()[-6:]))
            fails.append(label)
            continue
        print(head)
        for rel in outs:
            verdict, note = compare(work, shipped, rel, tol)
            mark = {"identical": "ok", "identical-modulo-date": "ok*", "identical-modulo-edit": "ok+"}.get(verdict, "FAIL")
            if mark == "FAIL":
                fails.append(f"{label} -> {rel}")
            print(f"      [{mark:>4}] {rel}" + (f"   {note}" if note else ""))
    print()

    print("[3] the paper's number gates on paper_v23.tex")
    for label, argv, cwd in GATES:
        rc, out, secs = run(argv, work / cwd)
        tail = out.splitlines()[-1] if out.splitlines() else "(no output)"
        mark = "ok" if rc == 0 else "FAIL"
        if rc != 0:
            fails.append(label)
        print(f"      [{mark:>4}] {label}  ({secs:.1f}s)")
        print(f"             {tail[:160]}")
    print()

    total = time.time() - t0
    print(f"runtime {total:.1f}s ({total / 60:.1f} min)")
    if skipped:
        print(f"skipped {len(skipped)} optional step(s), each named above")
    if fails:
        print(f"RESULT: FAIL -- {len(fails)} check(s) did not pass:")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("RESULT: PASS -- every fragment byte-identical (or date-only), every gate passed.")
    print("        ok* marks a file whose only difference is the run-date line its "
          "generator stamps; ok+ the two authored caption edits named at the top of this file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
