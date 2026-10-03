# -*- coding: utf-8 -*-
"""pin_appendix.py -- run appendix_identity against the v17 base tree and append the R110 pins (EXEMPT basis + PINS hash) for every
appendix section it reports changed or added (none is removed in this program). Idempotent per hash.
Usage: python reviews/v18/tools/pin_appendix.py
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v18" / "base_tree.txt").read_text().strip()
BASIS = ("R110 (2026-09-15, CC_PASS_v18, the pass from the tenth review; CLAIMS.md R110 block; reviews/v18/CHANGES.md): the appendix is derived from v17 by "
         "reviews/v18/tools/appendix_v18.py (28 asserted edits). C.2 gains the count readers (tab:cf-cr), the increment moved within the triple (tab:v2rcat), the "
         "score-resolution paragraph and the lookup at 100 and 200 names in tab:pad (reviews/NUMBERS_R110.md AUX-R110-A1, -A3, -A4; NUMBERS_V2RCAT.md); E.1 gains the "
         "names / counts / reads vocabulary (rule G3); E.9 gains Haiku 4.5 under the store's own metadata and its own-name split (believed_h/NUMBERS_BELIEVED_H.md "
         "AUX-BH-*) and the retention-denominator caveat; E.10 gains the retagging, depth and composite tables (tab:ds-a5, tab:ds-a6, tab:ds-a7; NUMBERS_DS.md "
         "sections 11 to 13) and loses its dollar figures and its pre-scoring pointers (A5_EDITS.md items 6 and 8); E.11 becomes the spend table; F gains five "
         "registration rows; every row label of the totals-randomized summary says totals. No frozen number changed; frozen_diff PASS with the R110 block.")
ARGS = [BASE, "--tex=paper_v18.tex", "--base=iclr2027_monitoring_submission/paper_v17.tex"]
out = subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout
pins = re.findall(r"to authorize this state, add to PINS:\s+(['\"])(.+?)\1: '([0-9a-f]{64})'", out)
removed = re.findall(r"REMOVED\s+UNLISTED\s+(.+?)\n", out)
entries = [(k, h) for _, k, h in pins] + [(k.strip(), "REMOVED") for k in removed]
if not entries:
    print("nothing to pin\n", out[-800:]); sys.exit(0)
src = TOOL.read_text(encoding="utf-8")
block = "\n# R110 (2026-09-15): pins for the v18 appendix state (reviews/v18/tools/pin_appendix.py wrote this block from the tool's own report).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {BASIS!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
print(subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout[-600:])
