# -*- coding: utf-8 -*-
"""verify_frbank.py -- check a local copy of the FR-Bank release against the bytes the
experiments consumed.

The FR-Bank release is not redistributed here. Obtain it from the source cited in the paper's
bibliography (the \\bibitem{fr} entry; a DOI is marked in README.md and will be filled in by the
authors when the record is minted), place it so that the directory holding `lifemembench_questions.json`
is the one you pass, and run:

    python verify_frbank.py --path /where/you/put/LifeMemEval

Every file listed in data/frbank_manifest.sha256 is hashed and compared. A mismatch means the
copy you have is not the one the stored scores were computed from; the package's own numbers are
unaffected, because every printed number is regenerated from the stored scores, not from the
release. Nothing here writes to the release.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

PKG = pathlib.Path(__file__).resolve().parent
MANIFEST = PKG / "data" / "frbank_manifest.sha256"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True,
                    help="the local LifeMemEval directory (the one holding lifemembench_questions.json)")
    a = ap.parse_args()
    root = pathlib.Path(a.path).resolve()
    if not MANIFEST.is_file():
        print(f"no manifest at {MANIFEST}")
        return 2

    ok = miss = bad = 0
    problems = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        want, rel = line.split("  ", 1)
        # manifest paths are written relative to the LifeMemEval directory
        p = root / rel
        if not p.is_file():
            miss += 1
            problems.append(f"missing   {rel}")
            continue
        h = hashlib.sha256()
        with p.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        if h.hexdigest() == want:
            ok += 1
        else:
            bad += 1
            problems.append(f"differs   {rel}")

    print(f"{ok} file(s) match, {bad} differ, {miss} missing (root {root})")
    for line in problems[:40]:
        print("   " + line)
    if len(problems) > 40:
        print(f"   ... and {len(problems) - 40} more")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
