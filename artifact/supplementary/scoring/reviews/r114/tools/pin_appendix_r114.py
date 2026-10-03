# -*- coding: utf-8 -*-
"""pin_appendix_r114.py -- program R114 (2026-09-17): run appendix_identity against the v19 base tree and append the R114 pins (EXEMPT basis +
PINS hash) for the appendix sections the pass changed (E.10: tab:ds-a7 on the actual views; C.2: the Opus 5 moved-count row; E.11: the spend
sentence if touched), with their reasons. Idempotent per hash; the same shape as reviews/r113/tools/pin_appendix_r113.py. Byte edit:
appendix_identity.py is CRLF. Usage: python reviews/r114/tools/pin_appendix_r114.py
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v19" / "base_tree.txt").read_text().strip()
HEAD = ("R114 (2026-09-17, the remaining runnable paid experiments; reviews/r114/SPEC_R114.md; reviews/r114/tools/m1_apply_manuscript.py, every edit asserted; "
        "CLAIMS.md R114 block): ")
REASONS = {
    "E.10": "tab:ds-a7 (DS Amendment 7) reads the absent items the gated rules answer on a longer view on that view's own answer instead of the five-line proxy "
            "(ds_downstream/NUMBERS_DS.md section 14, AUX-DS-R114-VIEWS, -COMPOSITE-ACTUAL, -ACTUAL-DIFF): twelve rows, the caption's proxy clause and the two prose "
            "sentences (model rule +19 / +3, lookup rule +25 / +9, the rule adds 24 and 12); every composite within one of the proxy reading, which stands in the ledger beside it. "
            "The section also carries the R112 and R113 pins' content unchanged.",
    "C.2": "the optional Opus 5 lane on the moved-count control run at k = 1 under the author's instruction (r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md section 8, "
           "AUX-V2RCAT-OP5; D-V2RCAT-2): three rows in tab:v2rcat beside the two registered lanes, one sentence in the prose with the draw-count disclosure; the recorded "
           "comparator is the k = 5 row. The section also carries the R112 and R113 pins' content unchanged.",
    "E.11": "the spend sentence gains the pass's lines (AUX-DS-R114-SPEND; AUX-V2RCAT-OP5).",
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
    return HEAD + r + " No population, repeat, model or threshold changed; every new number is ledgered."


raw = TOOL.read_bytes(); nl = b"\r\n" if b"\r\n" in raw else b"\n"
src = raw.decode("utf-8")
block = "\n# R114 (2026-09-17): pins for the remaining runnable paid experiments (reviews/r114/tools/pin_appendix_r114.py wrote this block from the tool's own report).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
src_lf = src.replace("\r\n", "\n")
assert marker in src_lf
src_lf = src_lf.replace(marker, block + marker, 1)
TOOL.write_bytes(src_lf.replace("\n", nl.decode()).encode("utf-8"))
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
print(subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout[-600:])
