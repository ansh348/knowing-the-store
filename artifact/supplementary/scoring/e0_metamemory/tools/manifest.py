"""
manifest.py -- sha256 manifest of every E0 artifact, plus the git commit.

NO API CALLS. Run last, after RESULTS_E0.md is written, so the manifest covers it.
"""

from __future__ import annotations

import hashlib
import subprocess

from e0_common import E0, PROJECT_ROOT, jdump

SKIP = {"manifest.json"}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    files = {}
    for p in sorted(E0.rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts or p.name in SKIP:
            continue
        files[str(p.relative_to(E0)).replace("\\", "/")] = {
            "sha256": sha256(p), "bytes": p.stat().st_size}
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(PROJECT_ROOT),
                                capture_output=True, text=True, check=True).stdout.strip()
    except Exception:                                            # noqa: BLE001
        commit = "unknown"
    combined = hashlib.sha256(
        "\n".join(f"{k} {v['sha256']}" for k, v in sorted(files.items())).encode()).hexdigest()
    jdump({"git_commit_at_manifest_time": commit, "n_files": len(files),
           "combined_sha256": combined, "files": files}, E0 / "manifest.json")
    print(f"{len(files)} files, combined sha256 {combined[:16]}...")
    for k in ("PREREG_E0.md", "AMENDMENT_1.md", "AMENDMENT_2.md", "RESULTS_E0.md",
              "items.json", "elicitation.json", "cache/responses.json",
              "results/scores.json", "results/reliability_fok.png",
              "results/reliability_nok.png", "thresholds.json",
              "tau_audit_sample.json", "pn_verification.json"):
        if k in files:
            print(f"  {k:34s} {files[k]['sha256'][:16]}...  {files[k]['bytes']:>9,d} B")


if __name__ == "__main__":
    main()
