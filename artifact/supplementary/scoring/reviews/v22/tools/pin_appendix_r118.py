# -*- coding: utf-8 -*-
"""pin_appendix_r118.py -- program R118 (the v21 lineage): pins for the appendix sections a landing step changed, the same shape as
reviews/r116/tools/pin_appendix_r116b.py (the tool's own report supplies the hashes; a REASONS entry per changed section is required, so a
section changed without a recorded reason stops the run). A later PINS.update overrides the earlier hash for a section pinned twice.
Usage: python reviews/v21/tools/pin_appendix_r118.py <step>      steps: sec8_cr
"""
import pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v21" / "base_tree.txt").read_text().strip()
ARGS = [BASE, "--tex=paper_v21.tex", "--base=iclr2027_monitoring_submission/paper_v19.tex"]
HEAD = "R118 (2026-09-19, the author's rulings of 19 September; reviews/v21/tools/r118_apply.py, every edit asserted; reviews/v21/tools/land_r118.py; CLAIMS.md R118 block): "
REASONS = {
    "sec8_cr": {
        "A": "R118-2 (ruling 4, page space): Table tab:e1 moved whole from Section 8 to after the expansion table, its float specifier [h] to [H], with a one-sentence lead; words and values unchanged.",
        "E.8": "R118-2 (ruling 4, page space): Section 8's coverage paragraph moved whole to after tab:cov-lookup under the heading 'The coverage judgment against its floor.'; its pointer to this appendix replaced by the table's number; words and values otherwise unchanged.",
        "C.2": "R118-3 (ruling 2, the count readers): the category-guessing reader's quantity corrected (the share of the category's entries that are superseded, retracted or expired, not 'the same count'); 'an upper bound' dropped from the state-aware reader's description and row label; one sentence explaining the 34 supersession wins (AUX-WP-B-ORDERING); the privileged post hoc share reader printed, 0.8473 whole set and 0.8981 / 0.7336 / 0.8528 per state with its persona interval (AUX-R110-A1-CR, CR-oracle-share), as a row of tab:cf-cr and in the prose; the caption describes both.",
    },
    "payers": {
        "C.2": "R118-4 (the landing map's payers): Section 5's first-draw sentence and its post-hoc PRESENT-versions sentence moved to the head of this appendix, the first rephrased to name its antecedent (AUX-R104-MARGIN; AUX-WP-B-PNPRESENT); numbers unchanged.",
        "E.10": "R118-4 (the landing map's payer for E4): Section 9's two-sentence paragraph (the persona-and-date header; the composite over all three jobs, Table tab:ds-a7) moved whole after tab:ds-a7, its self-referential pointer sentence dropped; numbers unchanged.",
    },
    "e5": {
        "A": "R118-5 (E5): tab:runs, the GPT-5.6 Luna and Sol counterfactual cells 'not run' to 'ran'; the caption 'three models ran on the counterfactual set' to 'five'.",
        "C.2": "R118-5 (E5): tab:pnpresent gains the GPT-5.6 Sol and Luna blocks (whole and per state; AUX-CF2-OAI-PNPRESENT) before the name-lookup block.",
    },
    "e2": {
        "C.2": "R118-6 (E2): tab:cf-names-counts after tab:v2rcat (AUX-CF2-NC-*: intact, names only, counts only, and the dash-rule form for GPT-4.1 mini; P-N1 and P-N2 held; the identity correction AUX-CF2-NC-IDENTITY in the caption).",
    },
    "e3": {
        "E.7": "R118-7 (E3): the sentence closing the distribution paragraph names the marker's wording as not the cause (Table tab:marker); tab:marker after tab:dist (AUX-MARKER-*: GPT-4.1 mini on Mem0 and A-MEM under four renderings, GPT-5.6 Luna raw API on the 66, the recorded harness rows beside, marked h).",
    },
    "e4": {
        "E.10": "R118-9 (E4): tab:ds-a8 after tab:ds-a7 and the moved paragraph (AUX-DS-A8-*: views changed, lines propagated, audited duplicates fully tagged, false propagation, the own-tag re-answers; the 187 / 45 / 40 diagnosis in the caption).",
    },
    "read1": {
        "C.2": "R118-13 (the author's read of 19 September; the landing map's Limitations payer): the Limitations sentence on the store's own name pool (a mean of 99 names; R113-4) moved whole after the store's-own-pool sentence; numbers unchanged.",
    },
    "e1": {
        "C.2": "R118-10 (E1): tab:v2rcat's Opus 5 rows read k = 5 (AUX-V2RCAT-A1-OP5-K5) with the draw-1 rows kept beside them; the caption records the registered prediction that held.",
    },
}
step = sys.argv[1]
out = subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout
pins = re.findall(r"to authorize this state, add to PINS:\s+(['\"])(.+?)\1: '([0-9a-f]{64})'", out)
removed = re.findall(r"REMOVED\s+UNLISTED\s+(.+?)\n", out)
entries = [(k, h) for _, k, h in pins] + [(k.strip(), "REMOVED") for k in removed]
if not entries:
    print("nothing to pin\n", out[-800:]); sys.exit(0)
def reason(k):
    key = k.split(":")[0].strip()
    r = REASONS[step].get(key); assert r, f"no reason recorded for the changed section {k!r} in step {step}"
    return HEAD + r + (" No number, n, interval or population changed." if "unchanged" in r else "")
src = TOOL.read_text(encoding="utf-8")
block = f"\n# R118 (2026-09-19), step {step}: pins written by reviews/v21/tools/pin_appendix_r118.py from the tool's own report.\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
print(subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout[-300:])
