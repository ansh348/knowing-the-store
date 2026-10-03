# -*- coding: utf-8 -*-
"""pin_appendix_r116b.py -- R116, the rulings of 19 September: pins for the appendix sections the rulings changed (the same shape as
pin_appendix_r116.py; a later PINS.update overrides the earlier hash for a section pinned twice). Usage: python reviews/r116/tools/pin_appendix_r116b.py
"""
import pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v19" / "base_tree.txt").read_text().strip()
HEAD = ("R116 (2026-09-19, the author's rulings on REPORT_R116 and PHASE0_REPORT item 6; reviews/r116/RULINGS_R116.md; "
        "reviews/r116/tools/r116b_apply.py, every edit asserted; CLAIMS.md R116 block): ")
REASONS = {
    "B": "the harness disclosure paragraph before tab:ladder-exact (the vendor's command-line agent, its own system text, the single flattened turn, reasoning effort low, subscription billing, the two probe gates of D-R74-8 at 0 of 12); the row marker $^{h}$ on the four GPT-5.6 rows of tab:ladder-exact and its caption's definition (build_v19.py REPAIRS_R116_BLOCK, block 913-943), and on the five Population cells of tab:ladder-predictions (block 980-997).",
    "A": "tab:runs: the GPT-5.6 Luna and Sol cross-model cells marked $^{h}$, their Scoring cells corrected ('provider default' was wrong for the harness rows: reasoning effort low through the agent harness), the caption defining the marker.",
    "E.7": "tab:inversion: the two pooled-66 rows marked $^{h}$ (build_v19.py REPAIRS_R116_BLOCK, block 1575-1766).",
    "E.10": "ruling 3: the sentence 'Each was preregistered with its texts written before any call' restored to its R115 form (the exception moved to table b's caption).",
    "E.11": "the price constants and metered totals of the two frontier lanes of the expansion printed beside OpenAI's page prices of 18 September 2026 (AUX-R116-PRICES).",
    "F": "ruling 3: table b's caption carries the exception (every row committed before its first call except DS Amendment 4 and Graphiti Amendment 2, attested by the runner's lock, file hashes shown); the attestation paragraph, table a's R81 hash, table b's '(file hash)' label and table c's caption as in the first R116 block.",
}
ARGS = [BASE, "--tex=paper_v19.tex", "--base=iclr2027_monitoring_submission/paper_v18.tex"]
out = subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout
pins = re.findall(r"to authorize this state, add to PINS:\s+(['\"])(.+?)\1: '([0-9a-f]{64})'", out)
removed = re.findall(r"REMOVED\s+UNLISTED\s+(.+?)\n", out)
entries = [(k, h) for _, k, h in pins] + [(k.strip(), "REMOVED") for k in removed]
if not entries:
    print("nothing to pin\n", out[-800:]); sys.exit(0)
def reason(k):
    key = k.split(":")[0].strip()
    r = REASONS.get(key); assert r, f"no reason recorded for the changed section {k!r}"
    return HEAD + r + " No number, n, interval or population changed."
src = TOOL.read_text(encoding="utf-8")
block = "\n# R116 (2026-09-19): pins for the rulings of 19 September (reviews/r116/tools/pin_appendix_r116b.py wrote this block from the tool's own report).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
print(subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout[-300:])
