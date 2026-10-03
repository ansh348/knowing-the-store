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
TEX = SUB / "paper_v22.tex"   # v22 (R126)
OUT = ROOT / "reviews" / "v22" / "NUMBER_MOVES_V22.md"
BASE = (ROOT / "reviews" / "v22" / "base_tree.txt").read_text().strip()

ADDED = {   # v22 (R126): the v21 dispositions are inherited in reviews/v22/NUMBER_MOVES_V21_inherited.md; this ledger starts at the R124 close
    # R126 (2026-09-20), the readable body
    '-2': "layout, not a printed value: the evidence table's second column is \\dimexpr\\linewidth-1.62in-2\\tabcolsep (Section 3; port_v22.py EVIDENCE)",
    '0.6': "Figure 3's y ticks (0.5, 0.6, 0.7, 0.8, 0.9, 1.0), pgfplots axis options; the plotted values are reviews/v22/src/fig3_data.tex (AUX-R126-FIG3)",
    '0.7': "Figure 3's y ticks (as 0.6)",
    '0.8': "Figure 3's y ticks (as 0.6)",
    '1.0': "Figure 3's y ticks (as 0.6)",
    '0,1,2': "Figure 3's x ticks, the three states (pgfplots axis options)",
    '-0.5': "Figure 3's dashed chance line, drawn from x = -0.5 to 2.5 at 0.5 (pgfplots coordinates, not a printed value)",
    '274': "reviews/NUMBERS_R126.md AUX-R126-E3-INTENT: the current-intent ABSENT questions of the 661 (tab:e3-intent, Appendix E.3)",
    '0,': "Figure 1's TikZ coordinates (0,-3.5mm), (0,-0.5mm): the masked-retrieval line and note under the tag route (the addendum's A1); layout, not a printed value",
    # R128 (2026-09-20)
    '0.5981': "tab:v2rcat's whole-name-map row prints its persona interval unsigned, [0.5587,0.5981] for [+0.5587,+0.5981] (AUX-V2RCAT-*; the value is unchanged)",
    # R129 (2026-09-20)
    '28%': "Section 1's MemoryAgentBench sentence in the author's words (the ruling on R127b item 1): Hu et al.'s Table 3, column FC-MH, the long-context GPT-5-mini (400K) row 28.0 and the paper's own 'at most 28%' sentence (a cited figure, as the 7% beside it)",
    '93': "the prediction count with E9's one prediction in it (reviews/NUMBERS_R129.md AUX-R129-COUNT): Section 4 and Appendix F",
    '29': "as 93: the predictions that came out otherwise, with P-M2 (failed for both models) in the count; tab:registrations-d 29 with 11",
    '34': "Section 7's parenthetical and Appendix E.10: the 35 obligations with an active stale line read 34 once the inverted tag is corrected (reviews/NUMBERS_R129.md AUX-R129-B9)",
    '0.79': "Section 5.2's hybrid paragraph: the hybrid's whole-set AUROC 0.7865 (AUX-CF2-HYB-WHOLE; reviews/NUMBERS_R129.md AUX-R129-HYB-PRINTED)",
    '0.19': "Section 5.1's moved-count paragraph: GPT-5.6 Sol's expiry fall -0.1914 (AUX-V2RCAT-A2-SOL-K5; reviews/NUMBERS_R129.md AUX-R129-E9-PRINTED)",
    '0.57': "Appendix E.3's group sentences: the with-summary AUROC of the obligations against group (a), Opus 5 0.5747 (AUX-R129-GROUPS-PRINTED)",
    '0.68': "as 0.57: GPT-4.1 mini 0.6801 on group (a) (AUX-R129-GROUPS-PRINTED)",
    '0.69': "as 0.57: GPT-4.1 mini 0.6947 on group (c) and the lookup 0.6932 on group (b) (AUX-R129-GROUPS-PRINTED)",
    '0.83': "as 0.57: GPT-5.6 Luna 0.8311 on group (c) (AUX-R129-GROUPS-PRINTED)",
    '0.29': "as 0.57: Haiku 4.5's question-only AUROC against group (a) 0.2902 (AUX-R129-GROUPS-PRINTED)",
    '0.40': "as 0.57: Opus 5's question-only AUROC against group (a) 0.3977 (AUX-R129-GROUPS-PRINTED)",
    '0.74': "as 0.57: the lookup 0.7395 and 0.7428 on groups (a) and (c) (AUX-R129-GROUPS-PRINTED)",
    # R131 (2026-09-20): the R125 results landed in the body (reviews/NUMBERS_R131.md; r82_counterfactual/cf2/NUMBERS_CF2.md section 15). The hand entries below
    # name the exact source of the body's tokens where the set-based walk above would otherwise credit an unrelated file that happens to hold the same value.
    # R131 close (2026-09-20): the provenance paragraph of Appendix E.3 (A1''; reviews/NUMBERS_R131.md AUX-R131-CLOSE-PROV, every count from the tree by r131_close_gate.py) and Limitations L1
    '1,400': "Appendix E.3's provenance paragraph: the release's sessions, 35 per persona over 40 personas (LifeMemEval/<n>_<name>/sessions/session_*.json; AUX-R131-CLOSE-PROV)",
    '35': "Appendix E.3's provenance paragraph: sessions per persona (AUX-R131-CLOSE-PROV; also the recorded 35 PN items of the hard tier elsewhere)",
    '516': "Appendix E.3's provenance paragraph: the release's question file holds 516 questions, and 516 of the 661 FR-Bank items ask one of them (two quantities of the same value; AUX-R131-CLOSE-PROV)",
    '187': "Appendix E.3's provenance paragraph: the distinct released questions the main study asks (AUX-R131-CLOSE-PROV; the token also occurs in Section 7's 187 of 272 audited stale lines, a different quantity)",
    '178': "Appendix E.3's provenance paragraph: released questions asked of the full FR-Bank store (AUX-R131-CLOSE-PROV; also the recorded 178 common full-store items of the answer-stage comparison, Appendix G)",
    '176': "Appendix E.3's provenance paragraph: released questions asked of the category-removed variant (AUX-R131-CLOSE-PROV)",
    '162': "Appendix E.3's provenance paragraph: released questions asked of the slot-removed variant (AUX-R131-CLOSE-PROV)",
    '113': "Appendix E.3's provenance paragraph: the crossed intent questions asked, 87 + 26 (cf_scores_ix.json lock/counts; AUX-R131-CLOSE-PROV)",
    '118': "Appendix E.3's provenance paragraph: the crossed intent questions drafted, 88 + 30 (AUX-R131-CLOSE-PROV)",
    '76': "Appendix E.3's provenance paragraph: cross-vendor items with a released question (cell_84.json; AUX-R131-CLOSE-PROV)",
    '0.4': "Figure 3's y ticks now start at 0.4 (R131 D: the y axis reaches 0.35 because mini's expiry value under the default summary is 0.4000; pgfplots axis options)",
    '0.4000': "Figure 3's data on the matched metric (reviews/v22/src/fig3_data_matched.tex; AUX-CF2-R125-FIG3, AUX-R131-FIG3): GPT-4.1 mini's expiry matched AUROC under the default summary, 9/6/15 (MINI5_v2); also tab:cf-matched, tab:cf-matched-ablations",
    '0.5833': "Figure 3's data on the matched metric (AUX-CF2-R125-FIG3): Haiku 4.5's expiry and GPT-5.6 Sol's retraction matched AUROC under the default summary; also Appendix C.2's matched tables",
    '0.6932': "Figure 3's data on the matched metric (AUX-CF2-R125-FIG3): the guessing count reader's supersession matched AUROC (34/54/0); also Appendix C.2's matched tables",
    '0.7667': "Figure 3's data on the matched metric (AUX-CF2-R125-FIG3): the guessing count reader's retraction value and Opus 5's retraction value under the default summary; also Appendix C.2's matched tables",
    '0.7833': "Figure 3's data on the matched metric (AUX-CF2-R125-FIG3): GPT-4.1 mini's expiry matched AUROC under the all-states summary (22/3/5); also tab:cf-matched",
    '0.8167': "Figure 3's data on the matched metric (AUX-CF2-R125-FIG3): the all-states lookup's retraction matched AUROC (19/11/0); also tab:cf-matched",
    '0.9333': "Figure 3's data on the matched metric (AUX-CF2-R125-FIG3): GPT-4.1 mini's and Haiku 4.5's retraction matched AUROC under the all-states summary; also tab:cf-matched",
    '+0.0643': "Table 1's difference row, matched: Opus 5 under the all-states summary minus the all-states lookup, the triple interval's upper bound (AUX-CF2-R125-OP5-V3; AUX-R131-TAB1)",
    '-0.0038': "Table 1's difference row, matched: the persona interval's lower bound (AUX-CF2-R125-OP5-V3; AUX-R131-TAB1)",
    '-0.0068': "Table 1's difference row, matched: the triple interval's lower bound (AUX-CF2-R125-OP5-V3; AUX-R131-TAB1)",
    '114': "Table 1's hybrid row and tab:cf-hybrid: the hybrid reader's W/T/L 114/34/0 (AUX-CF2-HYB-WHOLE; AUX-CF2-R125-MATCHED-V2 HYBRID_v2)",
    '98': "the prediction count with the two R125 registrations in it (reviews/NUMBERS_R131.md AUX-R131-COUNT): 98 predictions, Section 4 and Appendix F",
    '31': "as 98: 31 came out otherwise (P-N3 and P-N5 join P-M2 and the earlier 28); Appendix F's tab:registrations-e carries 5 with 2",
    '41': "Appendix F, tab:registrations-e: the two R125 registrations' freeze day, day 41 (2026-09-20 from day 0 = 2026-08-10; AUX-R126-DAYS)",
}
VANISHED = {
    # R126 (2026-09-20), the readable body: sentences of the v21 body that the inbox text does not carry (each value stays in its ledger and, where noted, in the appendix)
    '0,1': "Section 3's formal range FOK(q,S), NOK(q,S) in [0,1] left the body with the notation (the readable body's Section 4: readers return probabilities); the notation box is Appendix E.1",
    '217': "Section 6's line counts under FR-Bank's own tags (1,389 of the 3,305 lines shown marked non-active where the ground-truth tags mark 217) left the body; the precision 0.14 stays (Section 7); AUX-R110-A2-OWNVSJOIN",
    '1,389': "as 217",
    '79%': "Section 7's retention sentence (Haiku 4.5 keeps 72% capped and 79% lifted) left the body; tab:levels (Appendix E.9) carries 0.7190 and 0.7916 (AUX-BH-RETENTION-15 / -LIFTED)",
    '+0.15': "Section 8's gains print unsigned in the readable body: 'a reliable 0.15 to 0.45' (AUX-R74-X4 / tab:ladder-exact)",
    '+0.45': "as +0.15",
    '+0.26': "Kimi K3's cross-model gain +0.26 left the body ('including Kimi'); tab:ladder-exact (Appendix A) carries it",
    '+0.30': "Haiku 4.5's counted-state gain prints unsigned in the readable body: 'a reliable 0.30' (AUX-CF2-COUNTED)",
    '2026': "the registration record's calendar dates replaced by day indices (Phase 4.4, anonymity; reviews/NUMBERS_R126.md AUX-R126-DAYS)",
    # R129 (2026-09-20): the count sentence and the two payers
    '92': "the prediction count 92 / 28 becomes 93 / 29 with E9's prediction (AUX-R129-COUNT); Section 4 and Appendix F",
    '0.06': "Section 5.1's moved-count paragraph in the author's words: mini's +0.0611 expiry rise ('rises by 0.06') left the body; tab:v2rcat carries it (AUX-V2RCAT-MINI)",
    # R128 (2026-09-20), the author's B8
    **{k: "the lookup rows' persona intervals print unsigned (a level, not a gain): tab:cf3-expiry's all-states lookup row and tab:v2rcat's whole-name-map row (REPAIRS_R128_BLOCK (1191,1268); appendix_r128.py B8); the values are unchanged (AUX-CF3-*, AUX-V2RCAT-*)"
       for k in ('+0.5587', '+0.7226', '+0.7864', '+0.8051', '+0.8376', '+0.8391', '+0.9111', '+0.9424', '+0.9475', '+0.9477', '+1.0000')},
    '+0.5000': "tab:cf3-expiry's name-lookup rows print their degenerate intervals unsigned ([0.5000,0.5000] for [+0.5000,+0.5000]; the lookup ties every retraction and expiry triple under the superseded-only summary); the values are unchanged (AUX-CF3-*)",
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
                      ("reviews/r125/results/r125_t5_nc.json", "r82_counterfactual/cf2/NUMBERS_CF2.md section 15e, AUX-CF2-R125-NC-* (E2 Amendment 1; Section 5.1, Appendix C.2 tab:cf-nc-strong, Appendix F)")):
        walk3(json.load(open(ROOT / path, encoding="utf-8")), [], key + "; " + path)
    r85 = (ROOT / "r85_graphiti" / "NUMBERS_R85.md").read_text(encoding="utf-8")
    return out, r85


def all_added():
    gen, r85 = generated()
    d = dict(gen)
    d.update(ADDED)
    return d, r85


def run_numeric():
    out = subprocess.run([sys.executable, "tools/numeric_diff.py", f"--base={BASE}", "--tex=paper_v22.tex", "--base-tex=paper_v21.tex", "--round2"],
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
        print(f"number_moves_wp check: ADDED {len(add)}, VANISHED {len(van)}, missing from NUMBER_MOVES_V22.md {len(missing)}")
        for m in missing[:20]:
            print("  missing", m)
        sys.exit(1 if missing else 0)
    L = ["# NUMBER_MOVES_V22.md: every printed number added or removed in the v22 lineage (numeric_diff, --round2, against the R124 close)\n\n",
         "Written by `reviews/v22/tools/number_moves_wp.py` on the built manuscript; the base is the tree object in `reviews/v22/base_tree.txt` ",
         "(paper_v21.tex at the R124 close, ee6b735). Each token carries its disposition: where it stands now, or the ledger key it is read from. ",
         "`python reviews/v22/tools/number_moves_wp.py --check` fails if a token is unaccounted for.\n\n",
         f"## ADDED ({len(add)} tokens)\n\n| token | lines in paper_v22.tex | disposition |\n|---|---|---|\n"]
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
    OUT.write_text("".join(L), encoding="utf-8", newline="\n")
    print(f"-> {OUT} ADDED {len(add)} VANISHED {len(van)} unaccounted {unknown}")


if __name__ == "__main__":
    main()
