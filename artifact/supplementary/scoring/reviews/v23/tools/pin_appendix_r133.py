# -*- coding: utf-8 -*-
"""pin_appendix_r133.py -- program R133 (the readability pass, v23; 2026-09-21): pins for the appendix sections the pass changed, the same shape as
reviews/v22/tools/pin_appendix_r126.py (the tool's own report supplies the hashes; a REASONS entry per changed section is required, so a section
changed without a recorded reason stops the run). A later PINS.update overrides the earlier hash for a section pinned twice. The base is the v23 base
tree (paper_v22.tex at the R131 close), so a pin is needed for every section the pass touches, and the reason names the brief's item.
Usage: python reviews/v23/tools/pin_appendix_r133.py <step>      steps: homes, swaps, rulings
"""
import pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v23" / "base_tree.txt").read_text().strip()
ARGS = [BASE, "--tex=paper_v23.tex", "--base=iclr2027_monitoring_submission/paper_v22.tex"]
HEAD = ("R133 (2026-09-21, the readability pass, v23; the author's brief 'R133: V23 READABILITY PASS'; reviews/v23/tools/port_r133.py, every edit asserted; "
        "CLAIMS.md R133 block; reviews/v23/REPORT_R133.md). No number changes except Table 74's stale range corrected through r133_number_gate.py. ")
REASONS = {
    "homes": {
        "A": "section 4.1/4.3: the paragraph 'Coverage notes for the daggers in the main text' after tab:runs, five items (i) to (v), each the facts of tab:runs, tab:setup, "
             "tab:cf-names-counts, tab:cf-nc-strong, tab:cf-matched, tab:cf-intent and tab:x4-expansion restated so that each dagger in the main text resolves to one note; nothing removed; numbers unchanged.",
        "E.12": "section 4.4: tab:provenance's first row reads 'lookup $0.77$ and models $0.76$ to $0.85$' for the stale '$0.72$ to $0.84$' (0.72 was GPT-4.1 mini's one-draw temperature-0 row, "
                "no longer a row of Table 1; 0.84 omitted GPT-5.6 Sol's 0.85; r125_matched.json readers/*/gate through r133_number_gate.py); nothing else changes.",
    },
    "swaps": {
        "E.5": "S11: tab:count-destruction's caption reads 'the artifact's mechanism-score ledger' for 'the artifact's R108 ledger' (an internal program identifier in the built PDF); numbers unchanged.",
        "E.9": "S9: the census paragraph names the modes as Table 2 now labels them ('the over-mark, overwrite and unresolved-links reading'; 'the overwrite reading is of the record as exposed'); "
               "the two reproduction script names and the frozen registered texts untouched; numbers unchanged.",
        "F": "S11: tab:registrations' R94 row reads 'five recorded deviations' without the codes D-CF2-1 to D-CF2-5, and its DS row 'one prediction unfulfillable by its own gate, recorded as a deviation' "
             "for '(D-DS-3)' (internal deviation numbers in the built PDF; the rows are our summaries, not quoted registration text); numbers unchanged.",
    },
    "rulings": {
        "E.10": "R133 RULINGS 3 (the author, 2026-09-21): tab:routes gains two indented rows, GPT-4.1 mini's tagged view under ground-truth tags minus the summary alone on expiry "
                "(0.75; +0.24 (the summary alone, 0.51); [+0.11,+0.38]; [+0.06,+0.40]; 15 obligations) and on supersession (0.69; -0.17 (0.86); [-0.26,-0.07]; [-0.28,-0.07]; 63), each state's "
                "obligations against the same 557 negatives, from resp_review/run/scores_resp.json (AUX-RESP-L2-MINI-NOK) through r133_number_gate.py (reviews/NUMBERS_R133.md); the caption "
                "names the rows' population; nothing removed.",
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
    return HEAD + r


src = TOOL.read_text(encoding="utf-8")
block = f"\n# R133 (2026-09-21), {step}: pins written by reviews/v23/tools/pin_appendix_r133.py from the tool's own report (the base is the v23 base tree, paper_v22.tex at the R131 close).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
