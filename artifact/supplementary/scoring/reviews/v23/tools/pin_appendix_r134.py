# -*- coding: utf-8 -*-
"""pin_appendix_r134.py -- program R134 (the paraphrase check landed in v23; 2026-09-21): pins for the appendix sections the pass changes, the same shape as
pin_appendix_r133.py (the tool's own report supplies the hashes; a REASONS entry per changed section is required, so a section changed without a recorded
reason stops the run). A later PINS.update overrides the earlier hash for a section pinned twice (R133's pins for A, E.12 and F are superseded by these).
The base is the v23 base tree (paper_v22.tex at the R131 close), so the reason names both what R133 did to the section and what R134 adds.
Usage: python reviews/v23/tools/pin_appendix_r134.py <step>      steps: appendix, partb (Part B and RULING 3's payers), small (R135 5.3), r135 (ADDENDUM 2 as ruled)
"""
import pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v23" / "base_tree.txt").read_text().strip()
ARGS = [BASE, "--tex=paper_v23.tex", "--base=iclr2027_monitoring_submission/paper_v22.tex"]
HEAD = ("R134 (2026-09-21, the paraphrase check landed in v23; the brief 'R134: LAND THE PARAPHRASE CHECK IN v23' and the author's rulings of the same day; "
        "reviews/v23/tools/port_r134.py on the R133 close, every edit asserted; the tables from cf2_paraphrase/results/para_tab_*.tex (para_tex.py); every number through "
        "r134_number_gate.py; CLAIMS.md R133 block, the R134 entries; reviews/v23/REPORT_R134.md). Nothing removed from the appendix. ")
REASONS = {
    "appendix": {
        "A": "R133's coverage notes stand; R134 adds the paraphrase set's row to tab:setup (345 items, the 115 of the 148 questions, their states, the five readers with calls per question) "
             "and one sentence to tab:runs' caption naming the paraphrase lanes (section 5.2 of the brief: the run coverage).",
        "C.2": "section 5 of the brief: the 'Two registered checks' paragraph's pending sentence becomes one sentence and a pointer; after tab:pad the paragraph 'The paraphrase check' "
               "(the procedure, the AI-assisted read disclosed with its agreement counts, the six tables tab:para-pooled, -matched, -minus-lookup, -sup, -sens, -flags at four decimals, "
               "the author's ruling stated under the supersession-only table, the sensitivity sentence, the branch readings, the genericity paragraph, the run notes); "
               "every value from cf2_paraphrase/results/*.json (NUMBERS_PARA.md AUX-PARA-*; reviews/NUMBERS_R134.md).",
        "E.12": "R133's corrected first row stands; R134 adds tab:provenance's paraphrase-check row (345 items, 115 of the 148 triples; labels transferred from the original triples; "
                "the rewrites screened and read by an author with disclosed AI assistance; ground-truth summary; AUROC with the paired bootstrap; descriptive registration, no prediction).",
        "F": "R133's S11 wording stands; R134: tab:registrations-c's caption no longer says the paraphrase check waits on the read, its row's outcome reads 'run on day 42 on the 115 accepted pairs', "
             "and a row for the registration's dated notes and amendment follows it (the whole file 2848f1ad, day 42: the AI-assisted read disclosed, the floor amended from 120 to the 115 "
             "before any scoring call with the 124 as a sensitivity analysis, the two added readers); the prediction count is unchanged (the registration carries no prediction).",
        "G.5": "flag (b) of the report, agreed by the author: the dependency sentence no longer lists the paraphrase approvals, which are made.",
    },
    "small": {
        "G.5": "R135 (2026-09-21), section 5.3: the opaque sentence 'Valentina's omitted source supports the disputed hobbies; the repaired judge now marks every condition's answer correct for that question.' "
               "reads 'For one question, a persona's hobbies, the original reference packet had omitted the session that supports the answer; with that source restored, the repaired judge marks every condition's answer correct for that question.'; G.5 kept (the builders box cites it).",
    },
    "r135": {
        "G.2": "R135 ADDENDUM 2 as ruled (2026-09-21), item 3: the disclosure paragraph's clause 'the control is the paraphrased counterfactual set, registered and pending (tab:registrations-c)' reads "
               "'the control is the paraphrase check reported in Appendix C.2, with this split recomputed on the rewrites (tab:para-flags)'.",
        "G.4": "R135 ADDENDUM 2 as ruled, item 4: 'Its registered human endpoints and prediction rulings remain pending' reads 'were not completed at submission'.",
        "F": "R135 ADDENDUM 2 as ruled, item 4: tab:registrations-d's Graphiti Amendment 2 outcome reads 'human scoring and prediction rulings not completed at submission' and the count paragraph reads "
             "'the answer-stage predictions of Graphiti Amendment 2, not completed at submission, are not in the count' (R134's rows stand).",
        "C.2": "R135 ADDENDUM 2 as ruled, item 4: the paraphrase check's run notes read 'with the Opus 5 and Sol lanes then pending' (R134's block stands).",
    },
    "partb": {
        "E.1": "B3 of the brief (agreed): a three-pair term bridge at the top of the glossary (blind and indexed; route A and route B; the monitor), pointing to the table at the section's end; nothing renamed in pinned text.",
        "A": "RULING 3 (the author, 2026-09-21), P1: the five daggers leave the main text, so the coverage notes' heading reads 'Coverage notes for the main text.' and their first sentence no longer refers to a dagger "
             "('Each note below records a run setting that differs from its neighbours in the same sentence of the main text, or a comparison set that is incomplete.'); items (i) to (v) unchanged; the paraphrase row and caption sentence of the appendix step stand.",
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
block = f"\n# R134 (2026-09-21), {step}: pins written by reviews/v23/tools/pin_appendix_r134.py from the tool's own report (the base is the v23 base tree, paper_v22.tex at the R131 close).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
