# -*- coding: utf-8 -*-
"""pin_appendix_r143.py -- program R143 (2026-09-23): pins for the appendix sections the pass changes, the shape of pin_appendix_r137.py (the tool's own report
supplies the hashes; a REASONS entry per changed section is required, so a section changed without a recorded reason stops the run). Later PINS.update calls
override the earlier hash for a section pinned twice. Usage: python reviews/r141/tools/pin_appendix_r143.py
"""
import pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v23" / "base_tree.txt").read_text().strip()
ARGS = [BASE, "--tex=paper_v23.tex", "--base=iclr2027_monitoring_submission/paper_v22.tex"]
HEAD = ("R143 (2026-09-23; the addendum 'three zero-cost fixes, before the close'; reviews/r143/tools/port_r143.py on the R142 close, every edit asserted; CLAIMS.md R133 block, "
        "the R143 entries; reviews/r143/REPORT_R143.md). Nothing of substance removed from the appendix. ")
REASONS = {
    "C.2": "addendum a: the length-only reader paragraph's '; no sibling padded to equal length was run.' now points to the next paragraph's control (tab:sb60), which R141 ran.",
    "E.1": "addendum b: the clause 'which the main text stated in full until this version,' deleted from the notation-box sentence (no other word changed).",
}
out = subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout
pins = re.findall(r"to authorize this state, add to PINS:\s+(['\"])(.+?)\1: '([0-9a-f]{64})'", out)
removed = re.findall(r"REMOVED\s+UNLISTED\s+(.+?)\n", out)
entries = [(k, h) for _, k, h in pins] + [(k.strip(), "REMOVED") for k in removed]
if not entries:
    print("nothing to pin\n", out[-800:]); sys.exit(0)


def reason(k):
    key = k.split(":")[0].strip()
    r = REASONS.get(key)
    assert r, f"no reason recorded for the changed section {k!r}\n{out[-2000:]}"
    return HEAD + r


src = TOOL.read_text(encoding="utf-8")
block = "\n# R143 (2026-09-23): pins written by reviews/r141/tools/pin_appendix_r143.py from the tool's own report (the base is the v23 base tree, paper_v22.tex at the R131 close).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8", newline="\n")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
