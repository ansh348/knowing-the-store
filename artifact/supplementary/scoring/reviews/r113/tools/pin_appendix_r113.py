# -*- coding: utf-8 -*-
"""pin_appendix_r113.py -- program R113 (2026-09-16, the zero-cost audit pass): run appendix_identity against the v19 base tree and append the
R113 pins (EXEMPT basis + PINS hash) for the appendix section the pass changed (C.2), with its reason. Idempotent per hash; the same shape as
reviews/v19/tools/pin_appendix_int.py. Byte edit: appendix_identity.py is CRLF. Usage: python reviews/r113/tools/pin_appendix_r113.py
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v19" / "base_tree.txt").read_text().strip()
HEAD = ("R113 (2026-09-16, the zero-cost audit pass; reviews/r113/SPEC_R113.md section Z6; reviews/r113/tools/z6_apply_manuscript.py, every edit asserted; "
        "CLAIMS.md R113 block): ")
REASONS = {
    "C.2": "the list-length statements reconciled with the recorded rows at 100 and 200 names (reviews/NUMBERS_R110.md AUX-R110-A4): the store's-own-pool sentence "
           "states the registered-order rows at 100 and 200 (drawn from other personas' names once the store's own pool is exhausted; 0.6558 and 0.5960) and what stays "
           "untested (a longer list of the store's own names); tab:pad's caption names those two rows and the pool they draw on (79 of the 242 summaries at 100, every "
           "summary at 200); the lexical rows at 100 and 200 print the paired difference against the committed list and both intervals (reviews/NUMBERS_R113.md "
           "AUX-R113-PAD-LEX-PAIRED, read from reviews/v18/results/a4_pad_extend.json) in the columns the table defines, in place of the single-arm interval printed in "
           "the item-interval column. This section also carries the R112 pins' content unchanged.",
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
    return HEAD + r + " No number, n, interval or population changed; the lexical intervals are the recorded artifact's, ledgered at R113."


raw = TOOL.read_bytes(); nl = b"\r\n" if b"\r\n" in raw else b"\n"
src = raw.decode("utf-8")
block = "\n# R113 (2026-09-16): pins for the zero-cost audit pass (reviews/r113/tools/pin_appendix_r113.py wrote this block from the tool's own report).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
src_lf = src.replace("\r\n", "\n")
assert marker in src_lf
src_lf = src_lf.replace(marker, block + marker, 1)
TOOL.write_bytes(src_lf.replace("\n", nl.decode()).encode("utf-8"))
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
print(subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout[-600:])
