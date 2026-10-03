# -*- coding: utf-8 -*-
"""number_moves_wp.py -- the v19 lineage (R112; the R111 tool retargeted): write reviews/v19/NUMBER_MOVES_V19.md from numeric_diff's ADDED and VANISHED lists
(paper_v19.tex against the v19 base, reviews/v19/base_tree.txt, which holds paper_v18.tex at the Phase 4c close), with a disposition for
every token; --check re-runs numeric_diff and fails if any token is missing from the file. The same shape as number_moves.py (R110).
Usage: python reviews/v19/tools/number_moves_wp.py [--check]"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TEX = SUB / "paper_v23.tex"   # v23 (R133)
OUT = ROOT / "reviews" / "v23" / "NUMBER_MOVES_V23.md"
BASE = (ROOT / "reviews" / "v23" / "base_tree.txt").read_text().strip()

ADDED = {   # v23 (R133): the v22 dispositions are inherited in reviews/v23/NUMBER_MOVES_V22_inherited.md; this ledger starts at the R131 close
    # R133 RULINGS 3 (2026-09-21): tab:routes' two per-state rows, the tagged view under ground-truth tags minus the summary alone on that state's items
    # (resp_review/run/scores_resp.json L2/arms/RETRIEVED/{expiry,supersession}; AUX-RESP-L2-MINI-NOK; reviews/NUMBERS_R133.md AUX-R133-ROUTES-PERSTATE)
    # R137 (2026-09-22), Part B 5.1: Figure 1's rendered summary transcribes the LIFECYCLE TOTALS block of the summary the E.1 excerpt was cut from (ARTIFACT/manifests/indexes_v2.json
    # frbank:david:FULL:BELIEVED; AUX-R86-INDEX-EXCERPT names the same summary; reviews/NUMBERS_R137.md AUX-R137-FIG1, through r137_number_gate.py)
    '377': "Figure 1: the summary's LIFECYCLE TOTALS, active (frbank:david:FULL:BELIEVED, transcribed; AUX-R137-FIG1)",
    '197': "Figure 1: the summary's LIFECYCLE TOTALS, superseded (AUX-R137-FIG1)",
    '49': "Figure 1: the summary's LIFECYCLE TOTALS, expired (AUX-R137-FIG1)",
    # R137: Appendix C.2's long-list paragraph prints the target's median rank in the PN list as the ledger records it (cf_pad/build/lock.json target_position median 41.5; AUX-CFP-LOCK)
    '41.5': "Appendix C.2, the long-list check: the target's median alphabetical rank in the 60-name PN list over the 88 supersession triples (cf_pad/build/lock.json target_position; AUX-CFP-LOCK)",
    **{k: "tab:routes (Appendix E.10), the per-state rows added by R133 RULINGS 3: " + v for k, v in (
        ('+0.24', 'expiry, the difference +0.2364'), ('+0.11', 'expiry, item interval low +0.1053'), ('+0.38', 'expiry, item interval high +0.3829'),
        ('+0.06', 'expiry, persona interval low +0.0645'), ('+0.40', 'expiry, persona interval high +0.4037'), ('0.51', 'expiry, the summary alone 0.5110'),
        ('-0.17', 'supersession, the difference -0.1719'), ('-0.26', 'supersession, item interval low -0.2641'), ('-0.07', 'supersession, item interval high -0.0734 and persona interval high -0.0682'),
        ('-0.28', 'supersession, persona interval low -0.2764'), ('0.86', 'supersession, the summary alone 0.8572'), ('0.75', 'expiry, the tagged view 0.7474'))},
    # R141 (2026-09-23): tab:sb60 (Appendix C.2, the padded sibling control) prints the four-decimal cells of reviews/r141/results/scores_sb60.json (the models, the lookup) and
    # nomodel_sb60.json (the no-model readers, recorded before the freeze); every cell is checked by reviews/r141/tools/r141_number_gate.py (allowed141); AUX-R141-RESULTS, AUX-R141-NOMODEL
    **{k: 'tab:sb60 (Appendix C.2, R141 SB-60): ' + v + ' (AUX-R141-RESULTS / AUX-R141-NOMODEL)' for k, v in (
        ('0.4830', 'random-token lookup, triple interval low'), ('0.4837', 'random-token lookup, persona interval low'), ('0.5114', 'Sol and the lexical lookup, SB-60 vs padded PRESENT'),
        ('0.5170', 'random-token lookup, interval highs'), ('0.5227', 'the name lookup, SB-60 vs padded PRESENT'), ('0.5931', 'mini, pooled AUROC'), ('0.6307', 'mini, SB-60 vs padded PRESENT'),
        ('0.6420', 'mini, triple interval low; count reader (guessed), interval low'), ('0.6455', 'mini, persona interval low'), ('0.6818', 'Luna, SB-60 vs padded PRESENT'),
        ('0.7330', 'mini, matched'), ('0.7386', 'the lexical lookup, matched; count reader (guessed), interval high'), ('0.7670', 'the name lookup, persona interval low'),
        ('0.7898', 'the lexical lookup, triple interval high'), ('0.7927', 'the lexical lookup, persona interval high'), ('0.8193', 'mini, persona interval high'),
        ('0.8239', 'the name lookup, matched (the recorded value reproduced); mini, triple interval high'), ('0.8506', 'Sol, persona interval low'), ('0.8517', 'Luna, pooled AUROC'), ('+0.1398', 'Sol minus the lookup, matched, persona interval high'))},
    '106': 'the prediction count: 102 before R141 plus P-S1 to P-S4 of ADDENDUM_R141_SB60 (Section 4 and Appendix F; r141_number_gate.py; AUX-R137-COUNT plus the R141 predictions)',
}
VANISHED = {
    # R137 (2026-09-22), Part B 5.1: the schematic Figure 1 replaced by the rendered summary; its tikz coordinate '(0,-3.5mm)' carried the bare token
    '0': "the old Figure 1's tikz coordinate (0,-3.5mm), a layout constant, removed with the schematic (R137 Part B 5.1); not a research number (the W/T/L zeros and the counts print as before)",
    # R135 (2026-09-21), section 2.1: the evidence box at the end of Section 3 removed; its column-width expression (\dimexpr\linewidth-1.62in-2\tabcolsep) carried the token
    '-2': "the evidence box's tabular column width (\\dimexpr\\linewidth-1.62in-2\\tabcolsep), a layout constant, removed with the box (R135 section 2.1); not a research number",
    # R133 (2026-09-21), the readability pass: Section 5.1's moved-count sentence prints the four falls as one range, $0.27$ to $0.33$
    # Section 5.3's expiry-crossover sentence prints the three stronger models' explicit-rule scores as one range, $0.92$ to $1.00$
    '0.98': "Section 5.3: GPT-5.6 Luna's expiry-crossover score under the intent-explicit rubric, draw 1 (0.9808, tab:cf-intent; r82_counterfactual/cf2/NUMBERS_CF2.md section 14d, AUX-CF2-IX-*), is inside the printed range 0.92 to 1.00",
    # Section 7's two-routes sentence keeps the direction of the view's per-state effects and drops their magnitudes
    '0.24': "Section 7: the view's expiry gain for GPT-4.1 mini over the summary alone, +0.2364 (resp_review/NUMBERS_RESP.md AUX-RESP-L2-MINI-NOK, 'RETRIEVED, expiry'), left the prose ('helps mini on expiry'); no appendix row prints it (REPORT_R133.md lists it for a ruling); the supersession cost -0.1719 prints as 0.17 elsewhere",
    '0.32': "Section 5.1: GPT-5.6 Luna's retraction fall under the moved count on the matched metric, -0.3167 (AUX-CF2-R125-CONTRASTS 'moved count Luna k5 minus sup-only k5 (E9)' ret; reviews/NUMBERS_R131.md row '5.1 p4'), is inside the printed range 0.27 to 0.33",
}

# R134 (2026-09-21), the author's abstract (RULING 2, agreed): two numbers leave the abstract without leaving the paper, so numeric_diff reports neither; recorded here as moved.
MOVED = {
    # R139 (2026-09-23), the payers Q1, Q3, Q4 as ruled ('every number cut below is printed in the appendix the sentence points at')
    '0.12 (the builders box, R139 Q1)': "R139 Q1: the box's 'where Haiku sits $0.12$ above the lookup' leaves the main text; prints in Appendix E.9 (the store-written summary, Haiku minus the lookup)",
    '0.02 (Section 1 bullet, R139 Q3)': "R139 Q3: the bullet's 'the lookup loses $0.02$ when the questions are reworded' leaves; the abstract and Section 5.2 still print it (AUX-PARA-LOOKUP-EMB-V2 -0.0216)",
    '0.62 (Section 7, R139 Q4)': "R139 Q4: 'A reader that merely counts tagged lines scores $0.62$ under either tag source' leaves the main text; prints in Appendix E.10 and G.4",
    # R135 (2026-09-21): the tokens the robustness table absorbs from Section 5.2's two deleted paragraphs and Section 5.1's trims, and the abstract's two ranges; each still prints in the paper
    '0.13': "R135: 5.2's deleted 'List length and coverage' paragraph ('the name lookup stays $0.13$ above a lookup over meaningless tokens within triples'); prints in tab:robust row 2 (AUX-CF2-R125-CONTRASTS 'random-token minus name lookup (v2)' -0.1318)",
    '0.75 (the coverage-only reader)': "R135: the same deleted paragraph's 'still scores $0.75$ pooled' (the coverage-only reader); prints in Appendix C.2's emptiness paragraph ('which gives $0.75$ pooled on this set'); the token 0.75 also prints as the lookup's ground-truth level (Section 6, tab:robust row 10)",
    '60 / 0.67': "R135: 5.2's deleted 'Long or wrong name lists' paragraph ('Padding the default list to $60$ names lowers the lookup to $0.67$'); print in tab:robust row 9 (AUX-PAD-LOOKUP-EMB 60 names 0.6696) and its first column",
    '0.01 (5.1)': "R135 ADDENDUM: 5.1's 'stay within $0.01$ of their intact-summary scores' leaves the prose; prints in tab:robust row 6 (AUX-CF2-NC-MINI-NAMES -0.0064, -H45-NAMES -0.0059) and row 8",
    '0.28 to 0.33 (5.1)': "R135 ADDENDUM: 5.1's moved-count range leaves the prose; prints in tab:robust row 5 (AUX-CF2-R125-CONTRASTS counted: Opus -0.2833, Luna -0.2917, Sol -0.3250)",
    '0.06 / 0.04 (5.1)': "R135 ADDENDUM: 5.1's 'Removing every count costs Luna $0.06$ and Opus $0.04$' leaves the prose; prints in tab:robust row 6 (AUX-CF2-R125-NC-LUNA-NAMES -0.0598, -OP5-NAMES -0.0426)",
    '0.08 to 0.10 (abstract)': "R135: the abstract's 'lead over the lookup of $0.08$ to $0.10$' leaves with the brief's abstract; prints in Section 5.2's second paragraph (AUX-CF2-R125-VS-LOOKUP)",
    '0.88 (abstract, R135)': "R135, the G2 ruling (option c): the abstract's parenthetical '(all readers at $0.88$ AUROC or higher)' deleted; 0.88 prints in tab:robust row 3 ('models $0.88$ to $0.97$'; AUX-CF2-R125-SB-*, Haiku 0.8807) and in Table 1",
    '0.05 to 0.06 (abstract)': "R135: the abstract's '($0.05$ to $0.06$ remains)' leaves with the brief's abstract; prints in Section 5.2's second paragraph (AUX-CF2-HYB-VS-MODELS)",
    # R134 (2026-09-21), the author's abstract (RULING 2, agreed): two numbers left the abstract without leaving the paper
    '0.88': "the abstract's sibling-control sentence ('at an AUROC of $0.88$ or higher (chance $0.50$)') left with the author's abstract of 2026-09-21; the value still prints in Section 5.2's first paragraph ('The lookup and every model pick the PN version over it at $0.88$ or higher'; AUX-CF2-R125-SB-*) and in Table 1 (Haiku's and the name lookup's all-states rows, the persona intervals)",
    '0.50': "the abstract's '(chance $0.50$)' left with the same sentence; the value still prints in Section 4 ('Chance is $0.50$.') and in Table 1's caption ('Question-only AUROC is $0.50$')",
}


def generated():
    import json
    RES = ROOT / "reviews" / "v19" / "results"
    out = {}

    def walk(o, path, key):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, path + [str(k)], key)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, path + [str(i)], key)
        elif isinstance(o, bool):
            return
        elif isinstance(o, (int, float)):
            forms = {f"{o:.4f}", f"{o:+.4f}", f"{round(o, 2):.2f}", f"{round(o, 2):+.2f}"} if isinstance(o, float) else {str(o), f"{o:,}"}
            for f in forms:
                out.setdefault(f, f"{key}: {'/'.join(path[-6:])}")
    for name, key in (("posthoc_b.json", "reviews/NUMBERS_WP.md section 8, AUX-WP-B-PNPRESENT / -B-ORDERING / -B-COVONLY (reviews/v19/results/posthoc_b.json)"),
                      ("posthoc_b4.json", "reviews/NUMBERS_WP.md section 9, AUX-WP-B4-INTENT (reviews/v19/results/posthoc_b4.json)"),
                      ("posthoc_f1.json", "reviews/NUMBERS_WP.md section 10, AUX-WP-F1-WHOLEMAP (reviews/v19/results/posthoc_f1.json)")):
        walk(json.load(open(RES / name, encoding="utf-8")), [], key)
    for name, key in (("r85_graphiti/g10/census_g10.json", "r85_graphiti/NUMBERS_R85.md AUX-R85-G10-CENSUS (Appendix G.4)"),
                      ("r85_graphiti/g10/census_forbidding_g10.json", "r85_graphiti/NUMBERS_R85.md AUX-R85-G10-CENSUS-FORBIDDING (Section 7, Appendix G.4)"),
                      ("r85_graphiti/g10/census_full_variant_g10.json", "r85_graphiti/NUMBERS_R85.md AUX-R85-G10-CENSUS-FORBIDDING-FULL (Section 7, Appendix G.4)"),
                      ("r85_graphiti/g10/ingest_all_status.json", "r85_graphiti/NUMBERS_R85.md AUX-R85-G10-INGEST (Appendix G.4, E.11)")):
        try:
            walk(json.load(open(ROOT / name, encoding="utf-8")), [], key)
        except Exception:
            pass
    # Completion 2026-09-17: completed monitoring and blank human endpoint census.
    for path in ["r85_graphiti/g10/results/summary_g10.json", "r85_graphiti/g10/results/view_g10.json", "r85_graphiti/a2/results/detector_a2.json"]:
        walk(json.load(open(ROOT / path, encoding="utf-8")), [], "r85_graphiti/NUMBERS_R85.md AUX-R85-G10 / A2; " + path)
    # R118 (2026-09-19), the R117 experiments' result files (each number printed from them resolves to the ledger section named):
    for path, key in (("r82_counterfactual/cf2/results/cf_scores_openai.json", "r82_counterfactual/NUMBERS_CF2.md section 13, AUX-CF2-OAI-* (E5: GPT-5.6 Sol and Luna on the 444)"),
                      ("r82_counterfactual/cf2/results/cf_scores_nc.json", "r82_counterfactual/NUMBERS_CF2.md section 12, AUX-CF2-NC-* (E2: names against counts)"),
                      ("e1_metamemory/marker/scores_marker.json", "e1_metamemory/NUMBERS.md section 12, AUX-MARKER-* (E3: the marker ablation)"),
                      ("ds_downstream/run/scores_amend8.json", "ds_downstream/NUMBERS_DS.md section 15, AUX-DS-A8-* (E4: label propagation inside the view)"),
                      ("r82_counterfactual/v2rcat/results/scores_v2rcat_op5_k5.json", "r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md section 9, AUX-V2RCAT-A1-* (E1: Opus 5 at five draws)"),
                      ("reviews/v18/results/a1_count_readers.json", "reviews/NUMBERS_R110.md AUX-R110-A1-CR (the count readers; R118-3)")):
        walk(json.load(open(ROOT / path, encoding="utf-8")), [], key + "; " + path)
    # R123 (2026-09-19, the update and writing pass): the R121 and R122 result files and the pass's own two artifacts; the Wilson intervals of
    # tab:gatereach print at three decimals, so these files are walked with a three-decimal form as well.
    def walk3(o, path, key):
        if isinstance(o, dict):
            for k, v in o.items():
                walk3(v, path + [str(k)], key)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk3(v, path + [str(i)], key)
        elif isinstance(o, bool):
            return
        elif isinstance(o, (int, float)):
            forms = {f"{o:.4f}", f"{o:+.4f}", f"{round(o, 2):.2f}", f"{round(o, 2):+.2f}", f"{o:.3f}"} if isinstance(o, float) else {str(o), f"{o:,}"}
            for f in forms:
                out.setdefault(f, f"{key}: {'/'.join(path[-6:])}")
    for path, key in (("r82_counterfactual/cf2/results/cf_scores_ix.json", "r82_counterfactual/cf2/NUMBERS_CF2.md section 14d, AUX-CF2-IX-* (the intent crossover, R121; Section 5, Appendix C.2 tab:cf-intent, Appendix F)"),
                      ("reviews/r122/results/scores_r122_oai.json", "reviews/r122/NUMBERS_R122.md AUX-R122-K5-*, AUX-R122-P1-* (GPT-4.1 mini at five draws; the intent-explicit rubric on the 444; Table 1, Appendix C.2, Limitations)"),
                      ("reviews/r122/results/enc_lookup.json", "reviews/r122/NUMBERS_R122.md AUX-R122-ENC-* (the lookup under further encoders; Appendix C.2 tab:enc-lookup)"),
                      ("reviews/r122/results/gate_reach.json", "reviews/r122/NUMBERS_R122.md AUX-R122-GATE-* (what the gate buys, reach only; Section 9 tab:reach, Appendix E.10 tab:gatereach)"),
                      ("reviews/r117/results/sup_margins.json", "reviews/NUMBERS_R123.md AUX-R123-SUP-MARGINS (the supersession-only margins over the name lookup; Appendix C.2 tab:sup-margins)"),
                      ("reviews/v21/results/reach_rows_r123.json", "reviews/NUMBERS_R123.md AUX-R123-REACH-ROWS (the recorded policies' reach rows; Section 9 tab:reach)"),
                      # R124 block E (2026-09-19): E10, the hybrid reader
                      ("r82_counterfactual/cf2/results/cf_scores_hybrid.json", "r82_counterfactual/cf2/NUMBERS_CF2.md section 14e, AUX-CF2-HYB-* (E10, the hybrid reader; Appendix C.2 tab:cf-hybrid, Appendix F)"),
                      # R128 (2026-09-20), the author's B7 and B8
                      ("reviews/v22/results/r128_cf3_draw1.json", "reviews/NUMBERS_R128.md AUX-R128-CF3-DRAW1 (Opus 5 read at draw 1 on every expiry pair; Appendix C.3 tab:cf3-expiry)"),
                      ("reviews/v22/results/r128_ds_denoms.json", "reviews/NUMBERS_R128.md AUX-R128-DS-DENOM (the stale rates over both denominators, Wilson at three decimals; Appendix E.10 tab:ds-body, tab:ds-body-lower)"),
                      # R129 (2026-09-20), the author's rulings and the two body landings
                      ("r82_counterfactual/v2rcat/results/scores_v2rcat_openai.json", "r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md section 10, AUX-V2RCAT-A2-LUNA-K5 / -SOL-K5 (E9: GPT-5.6 Luna and Sol on the moved-count texts; Section 5.1, Appendix C.2 tab:v2rcat, Appendix F)"),
                      ("reviews/v22/results/r129_hybrid_mini5.json", "reviews/NUMBERS_R129.md AUX-R129-HYB-MINI5 (GPT-4.1 mini at five draws minus the hybrid; Appendix C.2 tab:cf-hybrid)"),
                      ("reviews/v22/results/r127_groups.json", "reviews/NUMBERS_R129.md AUX-R129-GROUPS (the 104 obligations against the three PRESENT groups; Appendix E.3 tab:e3-groups)"),
                      ("reviews/v22/results/r127b_groups.json", "reviews/NUMBERS_R129.md AUX-R129-GROUPS (the means, the question-only AUROC and the paired gains; Appendix E.3 tab:e3-groups)"),
                      ("reviews/v22/results/r129_b9.json", "reviews/NUMBERS_R129.md AUX-R129-B9 (the inverted tag corrected on paper; Section 7, Appendix E.10)"),
                      # R131 (2026-09-20), the R125 results landed in the body (r82_counterfactual/cf2/NUMBERS_CF2.md section 15; the two-decimal forms reviews/NUMBERS_R131.md)
                      ("reviews/r125/results/r125_matched.json", "r82_counterfactual/cf2/NUMBERS_CF2.md section 15, AUX-CF2-R125-* (the matched metric; Sections 1, 5.1, 5.2, 10, the abstract, Table 1, Figure 3, Appendix C.2 tab:cf-matched, tab:cf-classes, tab:cf-matched-vs, tab:cf-matched-ablations, tab:cf-hybrid)"),
                      ("reviews/r125/results/r125_t2_emptiness.json", "r82_counterfactual/cf2/NUMBERS_CF2.md section 15b, AUX-CF2-R125-T2-* (list emptiness; Section 5.2, Appendix C.2 tab:cf-emptiness)"),
                      ("reviews/r125/results/r125_t3_frbank.json", "r82_counterfactual/cf2/NUMBERS_CF2.md section 15c, AUX-CF2-R125-T3-FRBANK (the FR-Bank strata; Sections 6 and 9, Appendix E.9 tab:levels-strata)"),
                      ("reviews/r125/results/r125_t3_graphiti.json", "r82_counterfactual/cf2/NUMBERS_CF2.md section 15c, AUX-CF2-R125-T3-GRAPHITI (the Graphiti strata; Section 6, Appendix G.4 tab:graphiti-strata)"),
                      ("reviews/r125/results/r125_t4_sibling.json", "r82_counterfactual/cf2/NUMBERS_CF2.md section 15d, AUX-CF2-R125-SB-* (the sibling-name control; the abstract, Section 5.2, Appendix C.2 tab:cf-sibling, Appendix F)"),
                      ("reviews/r125/results/r125_t5_nc.json", "r82_counterfactual/cf2/NUMBERS_CF2.md section 15e, AUX-CF2-R125-NC-* (E2 Amendment 1; Section 5.1, Appendix C.2 tab:cf-nc-strong, Appendix F)"),
                      # R134 (2026-09-21), the paraphrase check landed (cf2_paraphrase/NUMBERS_PARA.md; the printed forms reviews/NUMBERS_R134.md AUX-R134-PRINTED)
                      ("cf2_paraphrase/results/para_scores.json", "cf2_paraphrase/NUMBERS_PARA.md section 4, AUX-PARA-{LOOKUP,MINI,H45,OP5,LUNA,SOL}-V2/V3, AUX-PARA-MATCHED-*, AUX-PARA-FLAGS, AUX-PARA-GENERIC (the 115; Section 5.2, the abstract, Appendix C.2 tab:para-pooled, tab:para-matched, tab:para-minus-lookup, tab:para-flags)"),
                      ("cf2_paraphrase/results/para_scores_all124.json", "cf2_paraphrase/NUMBERS_PARA.md section 4, the sensitivity rows (the 124, not registered; Appendix C.2 tab:para-sens)"),
                      ("cf2_paraphrase/results/para_minus_lookup_posthoc.json", "cf2_paraphrase/NUMBERS_PARA.md section 4, AUX-PARA-POSTHOC-MINUS-LOOKUP-* (post hoc; Section 5.2, the abstract, the Conclusion, Appendix C.2 tab:para-minus-lookup, tab:para-sup)"),
                      # R135 ADDENDUM 2 as ruled (2026-09-21): Section 7's propagation sentences print tab:ds-a8's own-tags primary column (the views changed, the duplicate views fully tagged, the false propagations of the licensed items' 2,333 active lines)
                      ("ds_downstream/run/lock_amend8.json", "ds_downstream/NUMBERS_DS.md section 15, AUX-DS-A8-RULE-CENSUS, -DUP35, -FALSEPROP (DS Amendment 8; Section 7, Appendix E.10 tab:ds-a8)"),
                      # R137 (2026-09-22), the long-list check landed (cf_pad/NUMBERS_CF_PAD.md AUX-CFP-*; the printed forms reviews/NUMBERS_R137.md AUX-R137-PRINTED)
                      ("cf_pad/results/cf_pad_scores.json", "cf_pad/NUMBERS_CF_PAD.md AUX-CFP-READERS-*, -MINUS-LOOKUP-*, -MINUS-LEX-*, -MINUS-RANDTOK-*, -POSITION, -OP5-D1, -P-L1 to -P-L4, -SPEND (the 60-name lists; Section 5.2, the abstract, Sections 1 and 10, tab:robust row 9, Appendix C.2 tab:cfpad-*, Appendix F)"),
                      ("cf_pad/build/lock.json", "cf_pad/NUMBERS_CF_PAD.md AUX-CFP-LOCK (the build census: list lengths, pools, the target's rank; Appendix C.2)")):
        walk3(json.load(open(ROOT / path, encoding="utf-8")), [], key + "; " + path)
    # R139 (2026-09-23): the pass's post hoc results (reviews/NUMBERS_R139.md AUX-R139-*) and the derived forms it prints
    for path, key in (("reviews/r139/results/equiv_r139.json", "reviews/NUMBERS_R139.md AUX-R139-EQUIV (equivalence within 0.05, post hoc; Appendix C.2 tab:equiv, tab:equiv-para)"),
                      ("reviews/r139/results/length_r139.json", "reviews/NUMBERS_R139.md AUX-R139-LENGTH (the length-only reader, post hoc; Appendix C.2 tab:length)"),
                      ("reviews/r139/results/n_count_r139.json", "reviews/NUMBERS_R139.md AUX-R139-N (the comparisons the main text calls reliable; Section 4)")):
        walk3(json.load(open(ROOT / path, encoding="utf-8")), [], key + "; " + path)
    R = json.load(open(ROOT / "reviews" / "r125" / "results" / "r125_matched.json", encoding="utf-8"))["readers"]
    for rk in ("MINI5_v2", "H45_v2", "LUNA_v2", "SOL_v2", "OP5_v2", "LOOKUP_v2", "CR-nb1_v2", "MINI5_v3", "H45_v3", "OP5_v3", "ALLSTATES_v3"):
        for st, b in R[rk]["pn_vs_present"]["per_state"].items():
            for f, what in ((f"{b['ci_persona']['ci_hi'] - b['matched']:.4f}", "upper"), (f"{b['matched'] - b['ci_persona']['ci_lo']:.4f}", "lower")):
                out.setdefault(f, f"Figure 3's bars (R139 Unit F): the persona-grouped 95% interval's {what} offset, {rk} {st} (AUX-CF2-R125-PERSTATE; reviews/r125/results/r125_matched.json)")
    L = json.load(open(ROOT / "reviews" / "r139" / "results" / "length_r139.json", encoding="utf-8"))
    out.setdefault("90%", "Appendix C.2, the equivalence test: the 90% intervals of the two one-sided tests at 5% (AUX-R139-EQUIV)")
    out.setdefault("2.6", "the default summary's PN superseded list, mean names over the 88 supersession triples, 2.625 at one decimal half-up (AUX-R139-LENGTH; the abstract, Appendix C.2)")
    for d, n in L["hist_pn_minus_sibling"]["unpadded|supersession"].items():
        out.setdefault(str(n // 2), f"Appendix C.2, the length-only reader: triples whose PN list is {d} name(s) longer than each sibling's (AUX-R139-LENGTH, the histogram halved: two siblings per triple)")
    for f in ("0.93", "0.94", "0.92", "+0.02", "-0.02", "+0.07", "+0.01", "+0.03"):
        out.setdefault(f, "R139 printed forms: 5.2's B1 (0.92 / 0.93 to 0.94), B2 (+0.02 [-0.02, +0.07]) and 5.3's B7 (+0.01 [-0.02, +0.03]); reviews/NUMBERS_R139.md AUX-R139-B1, -B2, -B7")
    r85 = (ROOT / "r85_graphiti" / "NUMBERS_R85.md").read_text(encoding="utf-8")
    return out, r85


def all_added():
    gen, r85 = generated()
    d = dict(gen)
    d.update(ADDED)
    return d, r85


def run_numeric():
    out = subprocess.run([sys.executable, "tools/numeric_diff.py", f"--base={BASE}", "--tex=paper_v23.tex", "--base-tex=paper_v22.tex", "--round2"],
                         cwd=SUB, capture_output=True, text=True).stdout
    # v19 (R112): [ \t]* rather than \s*, so an empty list does not swallow the next line ("COUNT-CHANGED (0):") as a token
    added = re.search(r"ADDED \((\d+)\):[ \t]*(.*)", out)
    vanished = re.search(r"VANISHED \((\d+)\):[ \t]*(.*)", out)
    add = re.findall(r"(\S+) @\[([0-9, ]+)\]", added.group(2)) if added else []
    # R126: numeric_diff separates VANISHED tokens by ', ' and a token itself may carry a comma ('0,1', '1,389'), so the split is on ', ' (v21 split on ',')
    van = [v.strip().rstrip(",") for v in vanished.group(2).split(", ")] if vanished else []
    return [(t.rstrip(","), [int(x) for x in ls.split(",")]) for t, ls in add], [v for v in van if v]


def main():
    check = "--check" in sys.argv
    add, van = run_numeric()
    ADDED_ALL, r85 = all_added()
    for t, _ in add:
        if t not in ADDED_ALL and (f" {t} " in r85 or f" {t}," in r85 or f"**{t}" in r85 or f"= {t}" in r85):
            ADDED_ALL[t] = "r85_graphiti/NUMBERS_R85.md AUX-R85-G10-* (Section 7, Appendix G.4): the token appears in that ledger"
    if check:
        moves = OUT.read_text(encoding="utf-8")
        missing = [t for t, _ in add if f"`{t}`" not in moves] + [v for v in van if f"`{v}`" not in moves]
        # Phase 4 (2026-09-15): a token written with the placeholder disposition counts as missing too
        missing += [t for t, _ in add if t not in ADDED_ALL] + [v for v in van if v not in VANISHED]
        print(f"number_moves_wp check: ADDED {len(add)}, VANISHED {len(van)}, missing from NUMBER_MOVES_V23.md {len(missing)}")
        for m in missing[:20]:
            print("  missing", m)
        sys.exit(1 if missing else 0)
    L = ["# NUMBER_MOVES_V23.md: every printed number added or removed in the v23 lineage (numeric_diff, --round2, against the R131 close)\n\n",
         "Written by `reviews/v23/tools/number_moves_wp.py` on the built manuscript; the base is the tree object in `reviews/v23/base_tree.txt` ",
         "(paper_v22.tex at the R131 close, b3cc631). Each token carries its disposition: where it stands now, or the ledger key it is read from. ",
         "`python reviews/v23/tools/number_moves_wp.py --check` fails if a token is unaccounted for.\n\n",
         f"## ADDED ({len(add)} tokens)\n\n| token | lines in paper_v23.tex | disposition |\n|---|---|---|\n"]
    unknown = []
    for t, ls in add:
        d = ADDED_ALL.get(t)
        if d is None:
            unknown.append(t); d = "UNACCOUNTED"
        L.append(f"| `{t}` | {ls} | {d} |\n")
    L.append(f"\n## VANISHED ({len(van)} tokens)\n\n| token | disposition |\n|---|---|\n")
    for v in van:
        d = VANISHED.get(v)
        if d is None:
            unknown.append(v); d = "UNACCOUNTED"
        L.append(f"| `{v}` | {d} |\n")
    L.append(f"\n## MOVED within the paper ({len(MOVED)} tokens; not reported by numeric_diff, recorded by the author's instruction of 2026-09-21)\n\n| token | disposition |\n|---|---|\n")
    for v, d in MOVED.items():
        L.append(f"| `{v}` | {d} |\n")
    OUT.write_text("".join(L), encoding="utf-8", newline="\n")
    print(f"-> {OUT} ADDED {len(add)} VANISHED {len(van)} unaccounted {unknown}")


if __name__ == "__main__":
    main()
