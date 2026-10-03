# -*- coding: utf-8 -*-
"""pin_appendix_r139.py -- program R139 (2026-09-23): pins for the appendix sections the pass changes, the shape of pin_appendix_r137.py (the tool's own report
supplies the hashes; a REASONS entry per changed section is required, so a section changed without a recorded reason stops the run). Later PINS.update calls
override the earlier hash for a section pinned twice. Usage: python reviews/r139/tools/pin_appendix_r139.py
"""
import pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v23" / "base_tree.txt").read_text().strip()
ARGS = [BASE, "--tex=paper_v23.tex", "--base=iclr2027_monitoring_submission/paper_v22.tex"]
HEAD = ("R139 (2026-09-23; the brief 'KtS R139', the author's GO with rulings, the Unit G addendum and the rulings on the STOP; reviews/r139/tools/port_r139.py on the R137 close, every edit asserted; "
        "every number through reviews/r139/tools/r139_number_gate.py; CLAIMS.md R133 block, the R139 entries; reviews/r139/REPORT_R139.md). Nothing of substance removed from the appendix. ")
REASONS = {
    "C.2": "Phase 1 (post hoc): the paragraphs 'Equivalence within the tolerance, post hoc' (tab:equiv, tab:equiv-para; AUX-R139-EQUIV) and 'The length-only reader, post hoc' (tab:length; AUX-R139-LENGTH) after the long-list check; "
           "B3's clause on the default list lengths moved here from 5.2 (the ruling's fallback); payers P9 (Table 2's per-row notes) and P10 (Table 1's notes b and c) give their notes a home in the registered-checks paragraph.",
    "E.4": "payer Q8: A2's second clause ('Each registered family of model-minus-lookup comparisons holds five readers (three under the all-states summary).') moved here from Section 4.",
    "E.10": "sweep S3: the HV-1 wording at four sites reads 'registered, with its workbooks built and no label collected at submission'; S4: Tables tab:resp-l1 and tab:resp-l2 scaled to the text width (both ran past the right margin; the second found by the close's margin scan). Q2's U5 is in E.7, not here.",
    "B": "sweep S5: an em dash in a caption of this appendix replaced by a comma or parentheses (no wording change).",
    "C.1": "sweep S5: an em dash in a caption replaced by parentheses (no wording change).",
    "E.6": "sweep S5: an em dash in the prose replaced by a colon (no wording change).",
    "E.7": "payer Q2 (approved 23 Sep): the pinned claim U5 moved here verbatim from Section 6; sweep S5: an em-dash pair in the prose replaced by parentheses (no wording change).",
    "A": "sweep S5: an em dash in a caption replaced (no wording change).",
    "E.3": "sweep S5: an em dash in the prose replaced (no wording change).",
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
block = "\n# R139 (2026-09-23): pins written by reviews/r139/tools/pin_appendix_r139.py from the tool's own report (the base is the v23 base tree, paper_v22.tex at the R131 close).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8", newline="\n")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
