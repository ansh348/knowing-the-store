"""
manifest_e1.py -- rewrite e1_metamemory/manifest.json. Manifest ONLY.

Split out of `finalize_e1.py`, which writes the manifest *and* appends a fixed
block of D16/D17/D18-E1 text to DEVIATIONS.md every time it runs. That append is
what produced the four duplicate copies of those three entries that E1.8
consolidated, so `finalize_e1.py` must not be re-run. This file does the manifest
half and nothing else: same file walk, same hashes, same combined digest.

Usage:  python e1_metamemory/tools/manifest_e1.py
"""

from __future__ import annotations

import hashlib
import io
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"


def main():
    files = {}
    for p in sorted(E1.rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts or p.name == "manifest.json":
            continue
        files[str(p.relative_to(E1)).replace("\\", "/")] = {
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "bytes": p.stat().st_size}
    hp = ROOT / "HEADLINE.md"
    files["../HEADLINE.md"] = {"sha256": hashlib.sha256(hp.read_bytes()).hexdigest(),
                               "bytes": hp.stat().st_size}
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(ROOT),
                                capture_output=True, text=True, check=True).stdout.strip()
    except Exception:                                              # noqa: BLE001
        commit = "unknown"
    combined = hashlib.sha256(
        "\n".join(f"{k} {v['sha256']}" for k, v in sorted(files.items())).encode()).hexdigest()

    prev = {}
    mp = E1 / "manifest.json"
    if mp.exists():
        prev = json.load(io.open(mp, encoding="utf-8")).get("files", {})

    with io.open(mp, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"git_commit": commit, "n_files": len(files),
                   "combined_sha256": combined, "files": files},
                  f, indent=2, sort_keys=True)
        f.write("\n")

    added = sorted(set(files) - set(prev))
    changed = sorted(k for k in set(files) & set(prev)
                     if files[k]["sha256"] != prev[k]["sha256"])
    removed = sorted(set(prev) - set(files))
    print(f"manifest: {len(files)} files (was {len(prev)}), "
          f"combined {combined[:16]}...")
    print(f"  added {len(added)}, changed {len(changed)}, removed {len(removed)}")
    for k in added:
        print(f"    + {k}")
    for k in changed:
        print(f"    ~ {k}")
    for k in removed:
        print(f"    - {k}")


if __name__ == "__main__":
    main()
