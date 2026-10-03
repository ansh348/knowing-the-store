# -*- coding: utf-8 -*-
"""pin_appendix_r141.py -- program R141 (2026-09-23): pins for the appendix sections the pass changes, the shape of pin_appendix_r137.py (the tool's own report
supplies the hashes; a REASONS entry per changed section is required, so a section changed without a recorded reason stops the run). Later PINS.update calls
override the earlier hash for a section pinned twice. Usage: python reviews/r141/tools/pin_appendix_r141.py
"""
import pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v23" / "base_tree.txt").read_text().strip()
ARGS = [BASE, "--tex=paper_v23.tex", "--base=iclr2027_monitoring_submission/paper_v22.tex"]
HEAD = ("R141 (2026-09-23; the brief 'R141: the sibling-name control at 60 names', the registration ADDENDUM_R141_SB60 frozen at f224177, the run 2588717 scored 7a62892, branch B-ii landed by "
        "reviews/r141/tools/port_r141.py on the R140 close, every edit asserted; every number through reviews/r141/tools/r141_number_gate.py; CLAIMS.md R133 block, the R141 entries; reviews/r141/REPORT_R141.md). "
        "Nothing of substance removed from the appendix. ")
REASONS = {
    "A": "the population row for the padded sibling control (SB-60) added to the exact capability table.",
    "C.2": "the paragraph 'The sibling-name control at 60 names' and tab:sb60 after tab:length (AUX-R141-BUILD, -NOMODEL, -RESULTS), with Luna's wording deviation recorded (AUX-R141-DISCREPANCIES).",
    "F": "the registration row for ADDENDUM_R141_SB60 (day 44, P-S1 fails, P-S2 to P-S4 hold), the caption's count and the prediction count 106 / 34.",
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
block = "\n# R141 (2026-09-23): pins written by reviews/r141/tools/pin_appendix_r141.py from the tool's own report (the base is the v23 base tree, paper_v22.tex at the R131 close).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8", newline="\n")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
