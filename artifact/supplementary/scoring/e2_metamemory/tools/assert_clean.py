"""
assert_clean.py -- phase-boundary hygiene assertion. NO API CALLS.

From ledger item 11 (R2_INCIDENTS Incident 8): twice now a load-bearing thing has
been left untracked. E1's 3,037 Phase-C usage records sat in the working tree
through the whole E1.8 closeout and through the `e1-complete` tag, while
ECONOMICS.md read every measured figure from them; and the scoop rule existed
only in conversation while a scan was run against it. Same failure class.

  AN UNTRACKED FILE THAT A COMMITTED ARTIFACT READS FROM IS A STOP CONDITION.

Two checks, both fatal:

  1. `git status --porcelain` is empty over the guarded paths.
  2. Every path that a committed tool opens is tracked. Paths are recovered by
     scanning the tools' source for string literals that name a repo file, which
     is coarse but has no false negatives that matter: a path that never appears
     as a literal is not being read by that tool.

Exit 0 = boundary may be crossed. Exit 1 = stop.

Usage:  python e2_metamemory/tools/assert_clean.py [--boundary NAME]
"""

from __future__ import annotations

import io
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Directories whose cleanliness gates a phase boundary. The repo at large carries
# unrelated untracked work from other lines; guarding everything would make the
# check meaningless noise, so it is scoped to the study's own trees plus the
# root-level artifacts the study writes.
GUARDED = ["e0_metamemory", "e1_metamemory", "e2_metamemory",
           "HEADLINE.md", "LANDSCAPE.md", "SCOOP_RULE.md"]

TOOL_DIRS = [ROOT / "e1_metamemory" / "tools", ROOT / "e2_metamemory" / "tools"]

# String literals that look like a repo-relative artifact path.
PATH_RE = re.compile(r'["\']([A-Za-z0-9_\-./]+\.(?:json|jsonl|md|npz|csv|txt))["\']')


def git(*args):
    return subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True,
                          text=True, encoding="utf-8", errors="replace").stdout


def regenerable():
    """Files accounted for by a recorded hash + a one-command rebuild.

    Incident 8's rule is that no load-bearing state may be UNACCOUNTED FOR.
    Tracking is one way to account for a file; for a 67 MB derived artifact that
    git would carry forever, a recorded sha256 plus a deterministic, cheap
    rebuild is the better one. The hash is verified here, so a silently altered
    artifact fails the boundary exactly as an untracked one would.
    """
    import hashlib
    p = ROOT / "e2_metamemory" / "REGENERABLE.json"
    if not p.exists():
        return set(), []
    ok, bad = set(), []
    for e in json.load(io.open(p, encoding="utf-8"))["files"]:
        f = ROOT / e["path"]
        if not f.exists():
            bad.append(f"{e['path']}: declared regenerable but absent "
                       f"(rebuild: {e['rebuild']})")
            continue
        got = hashlib.sha256(f.read_bytes()).hexdigest()
        if got != e["sha256"]:
            bad.append(f"{e['path']}: sha256 {got[:16]} != declared {e['sha256'][:16]}")
        else:
            ok.add(e["path"])
    return ok, bad


def main():
    boundary = (sys.argv[sys.argv.index("--boundary") + 1]
                if "--boundary" in sys.argv else "unnamed")
    fail = []
    accounted, regen_bad = regenerable()
    fail.extend(regen_bad)

    # ---- check 1: guarded paths clean
    dirty = [ln for ln in git("status", "--porcelain", "--", *GUARDED).splitlines()
             if ln.strip()]
    if dirty:
        fail.append(f"guarded paths not clean ({len(dirty)} entries)")
        for ln in dirty[:20]:
            fail.append(f"    {ln}")

    # ---- check 2: every artifact path a committed tool names is tracked
    tracked = set(git("ls-files").split("\n"))
    missing = {}
    for d in TOOL_DIRS:
        if not d.exists():
            continue
        for py in sorted(d.glob("*.py")):
            rel = str(py.relative_to(ROOT)).replace("\\", "/")
            if rel not in tracked:
                missing.setdefault("(the tool itself is untracked)", []).append(rel)
                continue
            src = io.open(py, encoding="utf-8", errors="replace").read()
            for m in PATH_RE.finditer(src):
                cand = m.group(1)
                if cand.startswith(("http", "//")) or "*" in cand:
                    continue
                for base in ("e0_metamemory", "e1_metamemory", "e2_metamemory", ""):
                    p = ((ROOT / base / cand) if base else (ROOT / cand)).resolve()
                    if not (p.exists() and p.is_file()):
                        continue
                    try:                       # `../HEADLINE.md` must normalise
                        r = str(p.relative_to(ROOT.resolve())).replace("\\", "/")
                    except ValueError:         # outside the repo: not ours to guard
                        break
                    if r not in tracked and r not in accounted:
                        missing.setdefault(rel, []).append(r)
                    break
    for tool, paths in missing.items():
        fail.append(f"untracked file read by a committed tool: {tool}")
        for p in sorted(set(paths)):
            fail.append(f"    {p}")

    print(f"phase-boundary assertion: {boundary}")
    print(f"  guarded: {', '.join(GUARDED)}")
    if fail:
        print("  RESULT: STOP")
        for f in fail:
            print(f"  {f}")
        sys.exit(1)
    print(f"  git status over guarded paths: clean")
    print(f"  artifact paths named by committed tools: all accounted for")
    if accounted:
        print(f"  regenerable (hash-verified): {len(accounted)}")
    print("  RESULT: may cross")


if __name__ == "__main__":
    main()
