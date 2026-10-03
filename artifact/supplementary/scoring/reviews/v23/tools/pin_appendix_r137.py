# -*- coding: utf-8 -*-
"""pin_appendix_r137.py -- program R137 (the long-list check landed; 2026-09-22): pins for the appendix sections the pass changes, the same shape as
pin_appendix_r134.py (the tool's own report supplies the hashes; a REASONS entry per changed section is required, so a section changed without a recorded
reason stops the run). A later PINS.update overrides the earlier hash for a section pinned twice (R134's and R135's pins for A, C.2, E.1, E.12 and F are superseded by these).
Usage: python reviews/v23/tools/pin_appendix_r137.py <step>      steps: numbers (F), appendix (A, C.2, E.1, E.11, E.12, F)
"""
import pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v23" / "base_tree.txt").read_text().strip()
ARGS = [BASE, "--tex=paper_v23.tex", "--base=iclr2027_monitoring_submission/paper_v22.tex"]
HEAD = ("R137 (2026-09-22, the long-list check landed in v23; the brief 'R137: LAND THE LONG-LIST CHECK, PLUS THE LAST TWO READABILITY ITEMS'; reviews/v23/tools/port_r137.py on the R135 close, "
        "every edit asserted; the tables from cf_pad/results/cfpad_tab_*.tex (cfpad_tex.py); every number through r137_number_gate.py; CLAIMS.md R133 block, the R137 entries; reviews/v23/REPORT_R137.md). "
        "Nothing removed from the appendix. ")
REASONS = {
    "numbers": {
        "F": "section 2 of the brief: the count paragraph reads 'Table tab:registrations-e $9$ with $4$: $102$ predictions, $33$ of which came out otherwise' (AUX-R137-COUNT: 98 / 31 plus P-L1 to P-L4, two otherwise); "
             "tab:registrations-e's caption names the long-list check and its row follows the two R125 rows (06c611f, day 43; what it froze; P-L2 and P-L3 held, P-L1 and P-L4 failed on Opus 5 alone). R134's and R135's rows stand.",
    },
    "appendix": {
        "A": "section 4.2 of the brief: tab:setup gains the row 'the counterfactual set, lists padded to $60$ names' (444 items, the same 148 questions, the five readers with calls per question) and tab:runs' caption "
             "the sentence naming the five padded runs; R133's coverage notes and R134's paraphrase row stand.",
        "C.2": "section 4.1 of the brief: the 'registered checks' paragraph counts three and gains one sentence for the long-list check; after the paraphrase check the paragraph 'The long-list check' "
               "(the padding rule, the lock, the caps and spend; the four predictions with their numbers; the six tables tab:cfpad-sup, -minus-lookup, -whole, -counted, -other-lookups, -position at four decimals; "
               "the counted states' sentence; Opus 5's recorded draw 1; the seed check; the run notes); every value from cf_pad/results/cf_pad_scores.json (NUMBERS_CF_PAD.md AUX-CFP-*; reviews/NUMBERS_R137.md). R134's and R135's text stands.",
        "E.1": "section 4.2 of the brief: the notation box gains the row 'padded list' (a superseded-names list lengthened to a fixed size with correct attribute names of the same store that no scored question targets, the counts left as written); nothing renamed in pinned text.",
        "E.11": "the spend sentence lists every capped run; the long-list check's $8.11$ of $12$ (Anthropic) and $15.54$ of $20$ (OpenAI) join it (AUX-CFP-SPEND; token-metered, not an invoice).",
        "E.12": "section 4.2 of the brief: tab:provenance gains the long-list check's row (444 items with 60-name lists, the 88 supersession triples registered; labels and store versions unchanged; pooled AUROC primary and the matched score secondary, both fixed in advance; registration committed before the run; two of four predictions held; Opus 5 at one draw).",
        "F": "the long-list check's row points to Table tab:cfpad-sup now that the table exists (the numbers step's row pointed to tab:robust).",
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
block = f"\n# R137 (2026-09-22), {step}: pins written by reviews/v23/tools/pin_appendix_r137.py from the tool's own report (the base is the v23 base tree, paper_v22.tex at the R131 close).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
