# -*- coding: utf-8 -*-
"""pin_appendix_r123.py -- program R123 (the v21 update and writing pass, 2026-09-19): pins for the appendix sections a phase changed, the same
shape as reviews/v21/tools/pin_appendix_r118.py (the tool's own report supplies the hashes; a REASONS entry per changed section is required, so
a section changed without a recorded reason stops the run). A later PINS.update overrides the earlier hash for a section pinned twice.
Usage: python reviews/v21/tools/pin_appendix_r123.py <phase>      phases: phase_a, phase_b, phase_c, phase_d
"""
import pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v21" / "base_tree.txt").read_text().strip()
ARGS = [BASE, "--tex=paper_v21.tex", "--base=iclr2027_monitoring_submission/paper_v19.tex"]
HEAD = "R123 (2026-09-19, the v21 update and writing pass, the author's brief with its amendments; reviews/v21/tools/r123_apply.py, every edit asserted; ledger_r123_tables.py, every table from its artifact; CLAIMS.md R118 block, the R123 continuation): "
REASONS = {
    "phase_a": {
        "A": "Phase A: tab:setup's counterfactual row names every model that ran it (GPT-4.1 mini at one and five calls, Haiku 4.5, Opus 5, GPT-5.6 Sol, GPT-5.6 Luna); tab:runs' GPT-4.1 mini scoring cell adds the five-call run at the provider default (Table tab:mini-k5) and GPT-5.6 Sol's cell says the counterfactual set ran through the raw API. No number changed.",
        "C.2": "Phase A: the post hoc intent paragraph's opener rewritten as plain motivation pointing at the crossover; the crossover paragraph with tab:cf-intent (AUX-CF2-IX-*) and tab:cf-p1 (AUX-R122-P1-*); the five-draw sentence after the single-draw note with tab:mini-k5 (AUX-R122-K5-*); tab:sup-margins after the adverse rows (AUX-R123-SUP-MARGINS); the encoders paragraph and tab:enc-lookup after the lexical lookup (AUX-R122-ENC-*); tab:cf-names-counts' caption says its comparator is the one-draw row.",
        "E.3": "Phase A: two sentences after 'Step 2 is the scored quantity.' (HELD_TEXTS_R121.md section 2): for four of five models the main-study rubric does not elicit the intent condition; in the main populations every PN question has current or upcoming intent by construction. No number changed.",
        "E.10": "Phase A: the reach-only paragraph and tab:gatereach after tab:reach-k (AUX-R122-GATE-*; the 661 and 104 denominators stated, AUX-R123-REACH-ROWS).",
        "F": "Phase A: tab:registrations-d (the Graphiti trial's readings, the five R117 registrations, the intent crossover and its amendment, the four R122 registrations, each with its outcome; a prediction made after an interim read labelled so) and the count paragraph (AUX-R123-TALLY: 47 + 17 + 0 + 26 = 90 predictions, 8 + 10 + 0 + 9 = 27 otherwise).",
    },
    "phase_b": {
        "E.10": "Phase B: Section 9's detector-scored table (tab:ds-body, its note and the 0-of-50, retagging, Haiku-residual and paired-comparison sentences) moved whole under the heading 'Answer-level outcomes (exploratory)', which says they rest on a token detector whose human validation is in progress; the reach-only table's label renamed tab:gatereach (the body's reference to it tripped the vocabulary rule on the word); numbers unchanged.",
        "F": "Phase B: tab:registrations-d's reference to the reach-only table follows the label rename (tab:gatereach); words and numbers unchanged.",
    },
    "phase_c": {
        "C.2": "Phase C: the Limitations payers moved here whole (the 44-expiry extension-draw clause; the two budget-stopped runs sentence); numbers unchanged.",
        "A": "Phase C: the Limitations sentence on the two budget-stopped runs moved here whole after tab:runs; numbers unchanged.",
    },
    "r124": {
        "C.2": "R124 B2: one sentence after tab:sup-margins' pointer: Opus 5's margin over the all-states lookup is reliable on the whole set (+0.0323) but on no single state (+0.0324, +0.0125, +0.0556, each interval including zero; AUX-R124-OP5-V3-MARGINS).",
        "C": "R124 D2: 'the registered R74 FOK-target probe' in the question-signal table's note (a carried block, build_v21.py REPAIRS_R123_BLOCK) printed as 'the registered coverage-target probe'; numbers unchanged.",
        "APPENDIX PREAMBLE": "R124 D1: the reader's guide (five sentences naming the tables behind each of the three findings and the provenance table) before Appendix A's heading; numbers unchanged.",
        "A": "R124 D1: the reader's guide sits before Appendix A's heading; Appendix A itself unchanged in words and numbers (its hash moves with the surrounding comment lines).",
        "E.9": "R124 D2: the four-counts sentence gains the clause that the 72 percent of Table 2 is a share of the 109 events (78 of them), not of the 104 entries (AUX-BELIEVED-FR).",
    },
    "r124_e": {
        "C.2": "R124 E1 (E10, the hybrid reader; registrations/ADDENDUM_CF2_HYBRID_READER.md frozen at fe6ff84, r82_counterfactual/cf2/NUMBERS_CF2.md section 14e): the paragraph 'A hybrid reader with no model in it' and tab:cf-hybrid after tab:enc-lookup (AUX-CF2-HYB-*; the registration's section 6: in every branch the C.2 table prints; the Section 5 sentence held).",
        "F": "R124 E1: tab:registrations-d gains the hybrid reader's row (fe6ff84e12; P-H1 failed, P-H2 held) and its caption names it; the count paragraph reads 28 with 10, 92 predictions, 28 otherwise (AUX-R124-TALLY).",
    },
    "r124_f": {
        "F": "R124 addition 3: the first paragraph gains 'The September additions were registered before their runs but after earlier results on the same items were known; we claim no confirmatory design for them.'; numbers unchanged.",
    },
    "phase_d": {
        "A": "Phase D: internal vocabulary rewritten in prose (the expansion, the ladder run, the captions of the carried tables); tab:populations dropped, its rows all carried by tab:setup, whose caption now says the body refers to a population by these names only; numbers unchanged.",
        "B": "Phase D: internal vocabulary rewritten in prose (ladder); numbers unchanged.",
        "C": "Phase D: internal vocabulary rewritten in prose; numbers unchanged.",
        "C.1": "Phase D: internal vocabulary rewritten in prose; numbers unchanged.",
        "C.2": "Phase D: internal vocabulary and process leftovers rewritten in prose (first form, v2/v3 forms, no-model); numbers unchanged.",
        "E.1": "Phase D: the glossary's rows for the store-written and ground-truth summaries and the run vocabulary; numbers unchanged.",
        "E.3": "Phase D: internal vocabulary rewritten in prose; numbers unchanged.",
        "E.6": "Phase D: internal vocabulary rewritten in prose; numbers unchanged.",
        "E.7": "Phase D: internal vocabulary and process leftovers rewritten in prose (the review's marker question as plain motivation); numbers unchanged.",
        "E.8": "Phase D: internal vocabulary rewritten in prose; numbers unchanged.",
        "E.9": "Phase D: the four counts near one hundred reconciled in one sentence (109 events, about 102 entries, 104 entries, 104 obligations); internal vocabulary; numbers unchanged.",
        "E.10": "Phase D: process leftovers rewritten as plain motivation ('written after the ninth review', 'written after the first draft' dropped); internal vocabulary ('no model' readers, the possessive table references, the registered paragraph's pointer); numbers unchanged.",
        "E.11": "Phase D: 'the continuation', 'blocked by provider credits' rewritten; numbers unchanged.",
        "D": "Phase D: 'the capability ladder' rewritten as 'the cross-model set' in the ledger's scope sentence; numbers unchanged.",
        "E.12": "Phase D: the provenance table's pointers follow the moves (the easy-tier coverage row to Appendix E.8; the downstream row to Table tab:reach and Appendix E.10); numbers unchanged.",
        "G": "Phase D: 'the explicitly registered Graphiti continuation' rewritten as 'the registered Graphiti follow-up'; numbers unchanged.",
        "F": "Phase D: the registration tables' vocabulary in prose cells; numbers unchanged.",
        "G.2": "Phase D: the sentence under the pooled-halves table corrected (a pooled AUROC also orders positives of one half against negatives of the other, so it is not a weighted average of the halves); numbers unchanged.",
        "G.4": "Phase D: the quoted registered text's 'our own store' printed as '[the lifecycle store]' with a note that the quotation is redacted for anonymity; the date removed from the early-ingest disclosure; numbers unchanged.",
        "G.5": "Phase D: the date removed from the early-ingest disclosure; process leftovers; numbers unchanged.",
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
block = f"\n# R123 (2026-09-19), {step}: pins written by reviews/v21/tools/pin_appendix_r123.py from the tool's own report.\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
print(subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout[-300:])
