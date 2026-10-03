# -*- coding: utf-8 -*-
"""pin_appendix_wp.py -- the writing pass (R111): run appendix_identity against the pass base tree (reviews/v18/base_tree_wp.txt, paper_v18.tex
after Phase 0) and append the R111 pins (EXEMPT basis + PINS hash) for every appendix section it reports changed. Idempotent per hash.
The same shape as pin_appendix.py (R110). Usage: python reviews/v18/tools/pin_appendix_wp.py
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v18" / "base_tree_wp.txt").read_text().strip()
BASIS = ("R111 (2026-09-15, the writing pass on paper_v18, paper_v18_writing_prompt.md; CLAIMS.md R111 block; reviews/v18/tools/wp_phase1.py, every edit "
         "asserted by line range). Phase 1: the appendix preamble comment records that appendix_v18.tex is now edited in place; C.2 gains the store's-own-pool "
         "sentence from Section 5 (reviews/NUMBERS_R110.md AUX-R110-A4: 0.6531, 99 names, at most 129; item 90); E.7's carried v11 block is split around the "
         "compression reading and the U1 sentence moved verbatim from Section 7 (pinned once; item 1); E.9 gains a paragraph with the 5% mask provenance from "
         "Section 4 and the Conflate row of Table 3 as prose (items 52, 83, 90); E.10's tab:routes-full gains the four readers with no model in them under the "
         "store's own tags from the body's Table 2 (AUX-R110-A2, -OWNVSJOIN; AUX-RESP-A1-BELIEVED) and the sign fix of item 36 (the monitor named first on every "
         "no-model row; no cell value changes). No number changed; frozen_diff PASS with the R111 block; numeric_diff accounted in reviews/v18/NUMBER_MOVES_WP.md.")
ARGS = [BASE, "--tex=paper_v18.tex", "--base=iclr2027_monitoring_submission/paper_v18.tex"]
out = subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout
pins = re.findall(r"to authorize this state, add to PINS:\s+(['\"])(.+?)\1: '([0-9a-f]{64})'", out)
removed = re.findall(r"REMOVED\s+UNLISTED\s+(.+?)\n", out)
entries = [(k, h) for _, k, h in pins] + [(k.strip(), "REMOVED") for k in removed]
if not entries:
    print("nothing to pin\n", out[-800:]); sys.exit(0)
src = TOOL.read_text(encoding="utf-8")
block = "\n# R111 (2026-09-15): pins for the writing pass's appendix state (reviews/v18/tools/pin_appendix_wp.py wrote this block from the tool's own report).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {BASIS!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
print(subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout[-600:])
