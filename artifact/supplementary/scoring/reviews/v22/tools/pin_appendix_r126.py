# -*- coding: utf-8 -*-
"""pin_appendix_r126.py -- program R126 (the readable body, v22; 2026-09-20): pins for the appendix sections Phase 4 changed, the same shape as
reviews/v21/tools/pin_appendix_r123.py (the tool's own report supplies the hashes; a REASONS entry per changed section is required, so a section
changed without a recorded reason stops the run). A later PINS.update overrides the earlier hash for a section pinned twice.
Usage: python reviews/v22/tools/pin_appendix_r126.py <step>      steps: phase4
"""
import pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v22" / "base_tree.txt").read_text().strip()
ARGS = [BASE, "--tex=paper_v22.tex", "--base=iclr2027_monitoring_submission/paper_v21.tex"]
HEAD = ("R126 (2026-09-20, the readable body, v22; the author's brief 'KtS R126: build v22 from the readable body', Phase 4; reviews/v22/tools/appendix_r126.py, every edit asserted, "
        "and build_v22.py REPAIRS_R126_BLOCK for the carried blocks; CLAIMS.md R126 block, entry R126-8; reviews/NUMBERS_R126.md). ")
REASONS = {
    "phase4": {
        "APPENDIX PREAMBLE": "4.2(a): the reader's guide of eight sentences (the term bridge in one sentence; the tables behind each finding; the provenance table; the registration record) replaces the R124 D1 guide; numbers unchanged.",
        "C.2": "4.1: the PN-versus-PRESENT paragraph's pointer reads Section~\\ref{sec:lookup} (5.2) for Section~\\ref{sec:counterfactual}; 4.2(c): tab:cf3-expiry's caption says 'question only (blind)'; numbers unchanged.",
        "E.1": "the notation box and Definition 2 (def:index) from the v21 body, verbatim (the readable body states the summary in prose); the terms table gains seven bridge rows (blind, indexed, route A, route B, NOK, FOK, the monitor) and its header names both vocabularies; numbers unchanged.",
        "E.3": "4.6: the coincidence sentence corrected to tab:e3-intent (AUX-R126-E3-INTENT: every PN question has current or upcoming intent; 44 PRESENT questions hold a non-active record of their own attribute, 33 current or upcoming, 11 change) and the table added; 4.4: the preregistration's date printed as day 0 of the registration record.",
        "E.7": "4.2(c): the captions of tab:dist and tab:marker say 'question only (blind)' and 'with the summary (indexed)' (tab:inversion, tab:q4-marker, tab:s1-names in the carried block, build_v22.py); numbers unchanged.",
        "E.10": "4.5: three recorded rows (top-five retrieval, the lookup rule, the oracle) in tab:gatereach's licensed panel from reach_rows_r123.json (AUX-R126-GATEREACH: 5.00, 5.46, 5.33 over the 661; 5.00, 6.88, 7.07 over the 104), so Table 3's numbers have an appendix home; 4.2(c): its caption says 'no reader (monitor) call'; 4.3: tab:ds-a8's two multicolumn rows lose their extra brace (the 21 inherited LaTeX errors); 4.4: the fourth amendment's date printed as day 35.",
        "E.12": "4.1: the provenance table's own-name ablation and moved-count rows point to Section~\\ref{sec:names_counts} (5.1); numbers unchanged.",
        "F": "4.4 (anonymity): the calendar dates of tab:registrations-b, -c and -d become day indices (day 0 = the first freeze; AUX-R126-DAYS) under a 'Freeze day' header; the intro says so; the attestation paragraph's '18 September 2026' and the -c caption's '18 September' read day 39; the Opus-entry paragraph reads days 4, 0 and 19; the hashes unchanged. (tab:registrations, the carried block: build_v22.py.)",
        "G.4": "4.4: the parenthetical after GR-1's quotation reads '(The bracketed words stand in for the store's name as the registered text gives it.)' so nothing is marked as redacted; numbers unchanged.",
    },
    "addendum2": {
        "APPENDIX PREAMBLE": "the reader's guide names an eighth bridged term, the structureless stores (Mem0 and A-MEM), which the readable body never uses; numbers unchanged.",
        "E.1": "the terms table gains the row 'the structureless stores'; the intro sentence says eight terms; numbers unchanged.",
    },
    "addendum": {
        "E.3": "the addendum's A5 (2026-09-20): Section 3's two summary-size sentences moved here, after the rendered summary's explanation; numbers unchanged.",
        "E.9": "the addendum's A2 and A7 (2026-09-20): Table 2's caption notes (the matching threshold; the two reproduction scripts) in the census-facts paragraph; Section 6's 'Haiku fares better' paragraph moved here in the readable body's words (AUX-BH-SPLIT), before the paragraph on Haiku 4.5 under the store's own metadata.",
    },
    # R128 (2026-09-20): the Program Chairs' feedback filtered against v22 (reviews/v22/R128_BRIEF.md sections B and C; appendix_r128.py, every edit
    # asserted, and build_v22.py REPAIRS_R128_BLOCK; CLAIMS.md R126 block, entries R128-B and R128-C; reviews/NUMBERS_R128.md).
    "r128": {
        "A": "R128 C: tab:ladder-predictions' notes define the harness marker $^{h}$ (REPAIRS_R128_BLOCK); the NOK-by-model table's caption reads '$0.75$ (rounded from $0.7484$)'; numbers unchanged.",
        "C.2": "R128 B8: tab:cf3-expiry gains three 'Opus 5, draw 1' rows (draw 1 on every pair; AUX-R128-CF3-DRAW1: pooled 0.5917 / 0.9247 / 0.6043) and its caption says the recorded Opus row pools 30 pairs at five draws with 14 at one; the lookup rows' persona intervals print unsigned; R128 C: 'expiry triples' for 'expiry pairs'; tab:v2rcat's draw-1 row labelled $^{d}$ with the note (0.8400, -0.0351; nothing numeric changed); the whole-name-map row's interval unsigned (REPAIRS_R128_BLOCK).",
        "E.3": "R128 B1: the coverage half of the rubric and the reply schema verbatim from e1_metamemory/tools/prompts_e1.py (the FOK line; the JSON schema) beside the obligation half, one call eliciting both; R128 C: the prompt template's backticks printed from T1 slot 0 (REPAIRS_R128_BLOCK); numbers unchanged.",
        "E.5": "R128 B5: tab:destruction's caption gains the cross-store qualification (every positive of the pooled tier an FR-Bank item, every Mem0 and A-MEM item a negative) and names tab:destruction-fr as the controlled within-store comparison (REPAIRS_R128_BLOCK); numbers unchanged.",
        "E.7": "R128 B2: the explanation of the below-chance rows corrected to what tab:dist shows (a collapse onto five values, positives 0.1617 against 0.1688 on Mem0 and 0.1544 against 0.1658 on A-MEM; store-written rows lose nothing; rebuilt names restore); tab:dist's caption; B3: how the pooled 66 were sampled (AUX-R128-POOLED66); B4: the Q4 probe's paragraph says the instruction's word 'absent' is also a label's name; C: tab:inversion's caption defines $^{h}$ (REPAIRS_R128_BLOCK); numbers unchanged.",
        "E.8": "R128 C: tab:baselines' caption reads 'the NB-6 column (the name lookup)' (REPAIRS_R128_BLOCK); numbers unchanged.",
        "E.9": "R128 C: tab:bh-split's $[0.6722,0.8992]$ moved to the persona row (the store-written levels table); numbers unchanged.",
        "E.10": "R128 B7: tab:ds-body's stale-rate columns print both denominators (of the reached scorable obligations; of the answered subset, with Wilson) and the caption says gated policies abstain on some reached obligations; tab:ds-body-lower's dash becomes $[0.097,0.278]$ (AUX-R128-DS-DENOM); tab:ds's second header block gains a divider; C: '$1{,}273$ of the $3{,}305$'.",
        "E.11": "R128 C: dollar signs on $0.14$, $4.52$ and $40$; numbers unchanged.",
        "F": "R128 B10: both Graphiti rows list GR-1 to GR-5 (GR-1 failed, GR-2 not computable, GR-3 held, GR-4 and GR-5 descriptive) beside P1 to P4; numbers unchanged.",
        "G.4": "R128 C: '+0.1014 (from the unrounded scores)' and the sentence placing the 784 untimed and 72 post-dated edges inside the three state counts; numbers unchanged.",
    },
    # R129 (2026-09-20): the author's rulings on R127b and R128's held items (reviews/v22/R129 brief; appendix_r129.py, every edit asserted; CLAIMS.md
    # R126 block, entries R129-A2, R129-B1, R129-B2, R129-D; reviews/NUMBERS_R129.md).
    "r129": {
        "C.2": "R129 B1: E9's six rows (GPT-5.6 Luna and GPT-5.6 Sol at five draws, whole set and per state; AUX-V2RCAT-A2-LUNA-K5, -SOL-K5) in tab:v2rcat, two sentences of prose and the caption's sentence (P-M2 failed on retraction for both); R129 B2: tab:cf-hybrid gains GPT-4.1 mini's five-draw row minus the hybrid, -0.0217 with both intervals including zero (AUX-R129-HYB-MINI5), and its caption says so.",
        "E.3": "R129 D: tab:e3-groups (AUX-R129-GROUPS: the 104 obligations against the three PRESENT groups per reader, means, AUROC with the summary and both intervals, the question-only AUROC and the paired gain) with four sentences after tab:e3-intent (two of the six group-(a) examples; the with-summary ranges 0.57 to 0.68 against 0.69 to 0.83; the question-only 0.29 to 0.40; the lookup 0.74, 0.69, 0.74).",
        "E.10": "R129 A2 (the ruling on R128's B9): the inverted tag's paragraph after the negation sentences (AUX-R129-B9: 35 -> 34, retraction 14 -> 13, the oracle split 16 / 0 and 14 / 5 as joined, 15 / 1 and 13 / 6 corrected; nothing re-answered); the eight answer-stage captions (tab:ds, -h45, -a5, -a6, -a7, -a8, -body, -body-lower) say the tables were scored with the store's tags as joined.",
        "F": "R129 B1: E9's row in tab:registrations-d (Amendment 2, b0bee9329d, day 40; one prediction, failed for both on retraction) and the count paragraph with it (AUX-R129-COUNT: -d 29 with 11; 93 predictions, 29 otherwise; the pending clause drops the second amendment).",
    },
    # R131 (2026-09-20): the R125 results landed in the body (the author's brief 'KtS R131', section H; appendix_r131.py, every edit asserted, every table
    # written from reviews/r125/results/*.json; CLAIMS.md R126 block, entry R131-H; reviews/NUMBERS_R131.md; r82_counterfactual/cf2/NUMBERS_CF2.md section 15).
    "r131": {
        "APPENDIX PREAMBLE": "R131 H: the reader's guide's three finding sentences point to the R125 tables (tab:cf-nc-strong, tab:cf-matched-ablations, tab:cf-matched, tab:cf-sibling, tab:cf-hybrid, tab:levels-strata, tab:graphiti-strata) and state the first finding as the body now does (the two smaller models read only the names, the three stronger ones also the counts); numbers unchanged.",
        "C.2": "R131 H: E2 Amendment 1 (tab:cf-nc-strong with its paragraph; P-N3 failed on Luna, P-N4 held, P-N5 failed; Sol's lane not run) after tab:cf-names-counts; the matched metric after tab:pnpresent (the paragraph; tab:cf-matched, tab:cf-classes, tab:cf-matched-vs, tab:cf-matched-ablations; the pooled Figure 3 as fig:perstate-pooled; tab:cf-emptiness, Task 2); the hybrid paragraph's matched sentences and tab:cf-hybrid's matched panels; the sibling-name control (tab:cf-sibling with its paragraph; P-SB1 to P-SB4 with the pre-freeze disclosure) before the expiry-pairs paragraph. Every value from reviews/r125/results (AUX-CF2-R125-*).",
        "E.9": "R131 H: the paragraph on what the store is in each scored condition and where the labels come from (R125 Task 3), and tab:levels-strata (the rows of tab:levels re-scored per stratum; the store-written minus ground-truth differences on the 82 the alignment marks) before the three-persona trial (AUX-CF2-R125-T3-FRBANK).",
        "F": "R131 H: tab:registrations-e (the two R125 registrations, frozen 5cd8f809f2 on day 41: the sibling-name control, P-SB2 and P-SB4 held, P-SB1 and P-SB3 recorded values; E2 Amendment 1, P-N3 failed on Luna, P-N4 held, P-N5 failed, Sol not evaluable) after tab:registrations-d, which is a [H] table at its page's height; the count paragraph (AUX-R131-COUNT: 98 predictions, 31 otherwise; -e 5 with 2; P-SB1 and P-SB3 not counted).",
        "G.4": "R131 H: the paragraph reading the 47 obligations relative to what the graph retains (23 of 34 retained, 13 recovered, 10 stale-active, 11 extraction misses) and tab:graphiti-strata (the rows of tab:graphiti-completed re-scored per stratum; the capped summary's loss against the FR-Bank ground-truth summary on the 23 retained) after tab:graphiti-completed (AUX-CF2-R125-T3-GRAPHITI).",
    },
    # R131 close (2026-09-20): the author's rulings (CONSOLIDATED ADDITIONS, ABSTRACT SWAP, MERGED RULINGS, FINAL RULINGS; appendix_r131_close.py, every edit asserted, every count from
    # r131_close_gate.py; build_v22.py REPAIRS_R131CLOSE_BLOCK; CLAIMS.md R126 block, the R131-CLOSE entries; reviews/NUMBERS_R131.md AUX-R131-CLOSE-*).
    "r131close": {
        "B": "R131 close, A5 (FINAL RULINGS 6): 'the preregistered primary endpoint' reads 'the registered primary endpoint'; numbers unchanged.",
        "E.3": "R131 close, A1'' (FINAL RULINGS 2): the provenance paragraph after the section's opening paragraph, third person for the release (40 personas and manifests, 35 sessions each, 1,400; the three released stores; 516 released questions, 187 asked on the full store and its two ablated variants, 178 / 176 / 162, for 516 of the 661 items; 145 natural-absent probes; 148 counterfactual questions and 444 items, the extension's 14 pairs and 42 items, 113 crossed questions of 118 drafted, 148 paraphrases, all GPT-4.1 mini; the cross-vendor set 84 of the 661, 76 released and 8 probes, and the question-only probes listed as subsets or analyses; 40 Graphiti graphs from 1,365 episodes rendered from the FR-Bank records). AUX-R131-CLOSE-PROV.",
        "E.4": "R131 close, A5 (FINAL RULINGS 6): 'The preregistered item-level interval' reads 'The registered item-level interval' (prose) and tab:cluster-sensitivity's caption 'reports the registered item-level interval' (REPAIRS_R131CLOSE_BLOCK); numbers unchanged.",
        "E.9": "R131 close, A3 follow-up (FINAL RULINGS 5): the Graphiti disclosure sentence attributes the earlier modified-copy ingestion to the FR-Bank release in the third person (the release vendors graphiti/ and graphiti_patches/); numbers unchanged.",
    },
    # R131 close, the page 8-9 payers (2026-09-20; 'R131 CLOSE: PAGE 8-9 PAYERS'; port_r131_w.py; CLAIMS.md the R131-W entries).
    "r131w": {
        "E.8": "R131 close, W7: the pointer sentence 'On the counterfactual set every model's coverage interval excludes chance (Table tab:cf-fok, Appendix C.2).' after the paragraph on where the lookup has values, so E.8 prints the claim Section 8 dropped; numbers unchanged.",
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
block = f"\n# R126 (2026-09-20), {step}: pins written by reviews/v22/tools/pin_appendix_r126.py from the tool's own report.\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
