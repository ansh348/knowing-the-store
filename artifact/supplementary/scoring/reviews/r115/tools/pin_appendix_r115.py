# -*- coding: utf-8 -*-
"""pin_appendix_r115.py -- program R115 (2026-09-18, the author's "Knowing the Store" patch): run appendix_identity against the v19 base
tree and append the R115 pins (EXEMPT basis + PINS hash) for every appendix section the patch changed, each with its reason. Idempotent
per hash. The same shape as reviews/v19/tools/pin_appendix_int.py. Usage: python reviews/r115/tools/pin_appendix_r115.py
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v19" / "base_tree.txt").read_text().strip()
HEAD = ("R115 (2026-09-18, the author's patch of 17 September, reviews/r115/PATCH_KTS.md, with the rulings of 18 September; "
        "reviews/r115/tools/kts_patch.py, every edit asserted; CLAIMS.md R115 block): ")
REASONS = {
    "B": "deviation D6: Table tab:crossvendor-predictions placed [H] instead of [h] (build_v19.py REPAIRS_R115_BLOCK, keyed to the carried block 1004-1020, asserted once): after the nine uncited bibliography entries left, the table no longer fit at the foot of its page, was deferred to the top of the next, and the float barrier before Appendix C ended that page after two lines; the placement returns the 17 September pagination. Content unchanged.",
    "C.2": "patch A1, the moved-count paragraph's 'run after this draft' reads 'run once per item' (a changelog leak); patch A6(a), 'profile' reads 'persona' in the count-reader sentence and in the headers of tab:v2rcat and tab:pad.",
    "E.9": "patch A3, the sentence Limitations gave up ('The sixty-percent line was a conventional threshold, fixed before the main study, with no recorded reason for its value.') placed after the retention sentence; patch A6(a), tab:bh-split's interval rows read 'persona' for 'profile'.",
    "E.11": "patch A2, 'two runs after this draft' reads 'two later runs' (a changelog leak).",
    "G.4": "patch A5 as ruled: Amendment 1's predictions P2 to P4 and readings GR-1 to GR-5 defined in two sentences before the paragraph that rules on them, and the registration's GR-1 FAILS and GR-3 HOLDS texts printed verbatim with their placeholders filled from AUX-R85-G10-GR (GR-1's text is tagged [MAIN] and prints here for the page limit; a Section 7 clause carries its content). The table is unchanged.",
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
    r = REASONS.get(key)
    assert r, f"no reason recorded for the changed section {k!r}"
    return HEAD + r + " No number, n, interval or population changed."


src = TOOL.read_text(encoding="utf-8")
block = "\n# R115 (2026-09-18): pins for the Knowing-the-Store patch (reviews/r115/tools/pin_appendix_r115.py wrote this block from the tool's own report).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
print(subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout[-600:])
