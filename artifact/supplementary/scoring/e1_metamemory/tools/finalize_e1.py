"""finalize_e1.py -- append the Phase C/D deviations and write the sha256 manifest."""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"

DEV = """
---

### D16 -- elicitation run on scoreable items only
The pre-registration lists the arms but does not require eliciting UNRESOLVED items, and section 8
computes every metric on the scoreable subset. Eliciting the 1,184 UNRESOLVED (question, variant)
pairs would have bought nothing and roughly doubled cost. 1,183 scoreable items elicited.
**Status:** logged.

---

### D17 -- a test run collided with the in-flight full elicitation
While the full Phase-C run was in the background I launched `elicit_e1.py --limit 40` to diagnose
what looked like a stall. Both wrote the same output files and the same cache. The full run
rewrote every output on completion and its parse counts are intact (2,698/2,698; arms 332 blind /
1,183 INDEXED-TRUE / 1,183 INDEXED-BELIEVED), so the only cost was a small number of re-called
cache entries. The apparent stall was not one -- the run was progressing with buffered output, and
my own test run then satisfied the file-based wait condition I had set, which is what made it look
finished. **Status:** logged; no correctness impact.

---

### D18-E1 -- the strong-model lane needed a Windows path fix
`subprocess` cannot resolve the bare name `codex` to the npm `.CMD` shim without a shell, so the
first strong-model attempt returned `FileNotFoundError` on all 150 items. Resolved with
`shutil.which`. Re-ran: **150/150 parsed**. The cost-routing guard (stripping `ANTHROPIC_API_KEY`
and `OPENAI_API_KEY` from the subprocess environment) is in place, closing the hazard the Phase-0
inventory flagged in the FR re-judge harness, which strips only the Anthropic key.
**Status:** resolved, logged.
"""


def main():
    with io.open(E1 / "DEVIATIONS.md", "a", encoding="utf-8", newline="\n") as f:
        f.write(DEV)

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
    except Exception:
        commit = "unknown"
    combined = hashlib.sha256(
        "\n".join(f"{k} {v['sha256']}" for k, v in sorted(files.items())).encode()).hexdigest()
    with io.open(E1 / "manifest.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump({"git_commit": commit, "n_files": len(files),
                   "combined_sha256": combined, "files": files},
                  f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"manifest: {len(files)} files, combined {combined[:16]}...")
    led = json.load(io.open(E1 / "cache" / "cost_ledger.json", encoding="utf-8"))
    print(f"ledger: calls {led['calls']} cached {led['cached']} usd {led['usd']:.4f}")
    for k in ("PREREG_E1.md", "AMENDMENT_1_E1.md", "RESULTS_E1.md", "STOP_POINT_2.md",
              "results/scores_e1.json", "../HEADLINE.md"):
        if k in files:
            print(f"  {k:28s} {files[k]['sha256'][:16]}...  {files[k]['bytes']:>10,d} B")


if __name__ == "__main__":
    main()
