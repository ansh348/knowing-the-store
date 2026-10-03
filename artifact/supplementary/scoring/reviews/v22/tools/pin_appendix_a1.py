# -*- coding: utf-8 -*-
"""pin_appendix_a1.py -- review-2 A1 (R112): run appendix_identity against the v19 base tree (reviews/v19/base_tree.txt, paper_v18.tex at the
Phase 4c close) and append the R112 pins (EXEMPT basis + PINS hash) for every appendix section it reports changed, with the reason the
author's ruling of 2026-09-15 gave: "rename collision from item 34, constrained rendering relabelled". E.9's basis names the page swap
instead (the Section 7 history-call sentence moved there under the same ruling). Idempotent per hash. The same shape as
reviews/v19/tools/pin_appendix_wp.py (R111). Usage: python reviews/v19/tools/pin_appendix_a1.py
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v19" / "base_tree.txt").read_text().strip()
REASON = "rename collision from item 34, constrained rendering relabelled"
BASIS = ("R112 (2026-09-15, review-2 A1, the author's ruling; CLAIMS.md R112 block; reviews/v19/A1_CONSTRAINED_RENDERING.md; reviews/v19/tools/a1_apply.py "
         "and REPAIRS_R112 in build_v19.py, every edit asserted): " + REASON + ". On Mem0 and A-MEM the TRUE index is the manifest rendered under the "
         "backend's constraints (e1_metamemory/indexes_v2.json meta.availability), so the Phase 2 rename TRUE -> ground-truth put 'ground-truth' on that "
         "meaning; the term 'the constrained rendering' is defined once in Section 4 and used at every site of A1_CONSTRAINED_RENDERING.md section 2 "
         "(E.1 map row; E.7 one added passage with the store-written deltas from AUX-WP-A1-BELIEVED-BLIND, reviews/NUMBERS_WP.md section 6, and three "
         "renames; E.8 the tab:baselines rows Mem0 FOK and A-MEM FOK as 'constrained' with the double-dagger note, the dagger note extended, and one "
         "sentence renamed). No number, n, interval or population changed.")
BASIS_E9 = ("R112 (2026-09-15, review-2 A1, the author's ruling; CLAIMS.md R112 block; reviews/v19/tools/a1_apply.py --swap): the Section 7 sentence on "
            "Mem0's per-memory history call moved here verbatim (its subject named) as the page swap the ruling authorized. No number changed.")
ARGS = [BASE, "--tex=paper_v19.tex", "--base=iclr2027_monitoring_submission/paper_v18.tex"]
out = subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout
pins = re.findall(r"to authorize this state, add to PINS:\s+(['\"])(.+?)\1: '([0-9a-f]{64})'", out)
removed = re.findall(r"REMOVED\s+UNLISTED\s+(.+?)\n", out)
entries = [(k, h) for _, k, h in pins] + [(k.strip(), "REMOVED") for k in removed]
if not entries:
    print("nothing to pin\n", out[-800:]); sys.exit(0)
allowed = {"E.1: Notation and study glossary", "E.7: Structureless-store inversion", "E.8: Non-LLM baseline suite", "E.9: Census of the store-written state"}
unexpected = [k for k, _ in entries if k not in allowed]
assert not unexpected, f"sections outside the A1 ruling changed: {unexpected}"
src = TOOL.read_text(encoding="utf-8")
block = "\n# R112 (2026-09-15): pins for review-2 A1 under the author's ruling (reviews/v19/tools/pin_appendix_a1.py wrote this block from the tool's own report).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {(BASIS_E9 if k.startswith('E.9') else BASIS)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
print(subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout[-400:])
