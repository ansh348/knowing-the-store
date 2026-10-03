# -*- coding: utf-8 -*-
"""r134_number_gate.py -- the number gate of R134 (2026-09-21; the brief 'R134: LAND THE PARAPHRASE CHECK IN v23', section 2, and the author's
ruling on the branch): every number the pass's new texts print (the Section 5.2 paragraph, the abstract, the Section 1 bullet, the Limitations
sentence, the Conclusion sentence, the appendix prose of the paraphrase check, tab:setup's row, the provenance row, tab:registrations-c's rows) is read
from its artifact here, independently of cf2_paraphrase/results/para_printed.json (which port_r134.py fills its texts from), and compared at the printed
precision (two decimals half-up on the four-decimal recorded value, r131_number_gate.r2; three decimals where the appendix prose prints three), with the
reliability or direction each sentence claims. A mismatch is listed; nothing is adjusted; exit 1 on any mismatch (the hard stop of section 8).
With --built, on iclr2027_monitoring_submission/paper_v23.tex: every numeral new to the main text against the v22 base is one of the pass's printed forms,
and every numeral new to the appendix is in the PARA fragment (cf2_paraphrase/results/para_tab_*.tex) or among the prose numerals listed here
(R133's own allowed set inherited).
Usage: python reviews/v23/tools/r134_number_gate.py [--built]
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
PARA = ROOT / "cf2_paraphrase"
RES = PARA / "results"
sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))
import r133_number_gate as G133  # noqa: E402  (the inherited abstract numbers: 0.73 / 0.82 / 0.75 -> 0.60 / 0.71 / 0.59, 0.05 to 0.06, 0.08 to 0.10)

SC = json.load(open(RES / "para_scores.json", encoding="utf-8"))
SCs = json.load(open(RES / "para_scores_all124.json", encoding="utf-8"))
PH = json.load(open(RES / "para_minus_lookup_posthoc.json", encoding="utf-8"))
SH = json.load(open(PARA / "sheet.json", encoding="utf-8"))
Q = json.load(open(PARA / "para_questions.json", encoding="utf-8"))
R125 = json.load(open(ROOT / "reviews" / "r125" / "results" / "r125_matched.json", encoding="utf-8"))
BASE = (ROOT / "reviews" / "v23" / "base_tree.txt").read_text().strip()
L, MO, MT = SC["lookups"], SC["models"], SC["matched"]
SUP = {c: PH["models"][c]["v2"]["superseded"] for c in ("MINI", "H45", "OP5", "LUNA", "SOL")}
WH = {c: PH["models"][c]["v2"]["whole"] for c in ("MINI", "H45", "OP5", "LUNA", "SOL")}

CHECKS = []


def r2(x):
    """Two decimals, half-up on the four-decimal recorded value (the R131 / R133 convention); the magnitude, the direction being in words."""
    return str(abs(Decimal(str(round(x, 4))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)))


def chk(where, printed, value, source, reliable=None, actual_reliable=None):
    ok = (r2(value) == printed) if isinstance(value, float) else (str(value) == str(printed))
    if reliable is not None:
        ok = ok and (bool(actual_reliable) == reliable)
    CHECKS.append(dict(where=where, printed=str(printed), value=value, source=source, reliable=reliable, actual_reliable=actual_reliable, ok=bool(ok)))


def reliable_neg(d):
    return d["delta"] < 0 and d["both_exclude_zero"]


def reliable_pos(d):
    return d["delta"] > 0 and d["both_exclude_zero"]


def checks():
    del CHECKS[:]
    tol = SC["tol"]
    # ------------------------------------------------------------------ Section 5.2, the paragraph 'The result survives rewording.' (4.1 with the author's Branch B sentence)
    chk("5.2: '115 rewrites passed a word screen and an author's read'", "115", SC["n_pairs"], "para_scores.json n_pairs (sheet.json n_accepted 115 of 124 screen-passing; para_questions.json 124 accepted of 148)")
    chk("5.2 / abstract / Section 1: 'the embedding lookup loses 0.02, within tolerance' (whole set, superseded-names summary)", "0.02", L["emb_v2"]["paired"]["delta"],
        f"lookups.json emb_v2 paired delta {L['emb_v2']['paired']['delta']:+.4f} (AUX-PARA-LOOKUP-EMB-V2); within tolerance = |d| <= {tol}", reliable=False, actual_reliable=L["emb_v2"]["paired"]["both_exclude_zero"])
    chk("5.2: the lookup's loss is within the registered tolerance", "within", "within" if abs(L["emb_v2"]["paired"]["delta"]) <= tol else "beyond", "as above; the registered reading 'holds'")
    chk("5.2: 'A word-matching lookup falls to chance by construction'", "0.5000", f"{L['lex_v2']['paraphrase']:.4f}", "lookups.json lex_v2 paraphrase (AUX-PARA-LOOKUP-LEX-V2)")
    chk("5.2: 'Rewording costs mini 0.03' (not reliable)", "0.03", MO["MINI"]["v2"]["paired"]["delta"], f"para_scores.json MINI v2 paired delta {MO['MINI']['v2']['paired']['delta']:+.4f} (AUX-PARA-MINI-V2)", reliable=False, actual_reliable=MO["MINI"]["v2"]["paired"]["both_exclude_zero"])
    chk("5.2: 'Haiku a reliable 0.06'", "0.06", MO["H45"]["v2"]["paired"]["delta"], f"para_scores.json H45 v2 paired delta {MO['H45']['v2']['paired']['delta']:+.4f} (AUX-PARA-H45-V2)", reliable=True, actual_reliable=reliable_neg(MO["H45"]["v2"]["paired"]))
    chk("5.2: 'Opus a reliable 0.03'", "0.03", MO["OP5"]["v2"]["paired"]["delta"], f"para_scores.json OP5 v2 paired delta {MO['OP5']['v2']['paired']['delta']:+.4f} (AUX-PARA-OP5-V2; one draw against the recorded five)", reliable=True, actual_reliable=reliable_neg(MO["OP5"]["v2"]["paired"]))
    for c, nm in (("LUNA", "Luna"), ("SOL", "Sol")):
        d = MO[c]["v2"]["paired"]
        chk(f"5.2: '{nm} ... do not move' (within tolerance, intervals include zero)", "holds", "holds" if abs(d["delta"]) <= tol and not d["both_exclude_zero"] else f"{d['delta']:+.4f}, reliable={d['both_exclude_zero']}",
            f"para_scores.json {c} v2 paired delta {d['delta']:+.4f} (AUX-PARA-{c}-V2; added, not registered)")
    chk("5.2: 'the lookup now sits a reliable 0.09 above mini'", "0.09", MO["MINI"]["v2"]["model_minus_emb"]["delta"], f"para_scores.json MINI v2 model_minus_emb {MO['MINI']['v2']['model_minus_emb']['delta']:+.4f} (AUX-PARA-MINI-V2)",
        reliable=True, actual_reliable=reliable_neg(MO["MINI"]["v2"]["model_minus_emb"]))
    keep = all(reliable_pos(WH[c]["pooled"]["paraphrase"]) and reliable_pos(WH[c]["pooled"]["original"]) for c in ("OP5", "LUNA", "SOL"))
    chk("5.2: 'the stronger models keep the lead they had' (Opus, Luna, Sol reliably above the lookup on the paraphrase set and on the original questions, whole set, pooled)", "holds", "holds" if keep else "fails",
        "para_minus_lookup_posthoc.json models/{OP5,LUNA,SOL}/v2/whole/pooled: paraphrase " + ", ".join(f"{WH[c]['pooled']['paraphrase']['delta']:+.4f}" for c in ("OP5", "LUNA", "SOL")) + "; original " + ", ".join(f"{WH[c]['pooled']['original']['delta']:+.4f}" for c in ("OP5", "LUNA", "SOL")) + " (AUX-PARA-POSTHOC-MINUS-LOOKUP-*)")
    # the author's Branch B sentence: supersession only, paraphrase set, pooled, model minus the embedding lookup
    chk("5.2 (Branch B): 'mini ... reliably below the lookup on the pooled metric (by 0.12'", "0.12", SUP["MINI"]["pooled"]["paraphrase"]["delta"], f"para_minus_lookup_posthoc.json MINI v2 superseded pooled paraphrase {SUP['MINI']['pooled']['paraphrase']['delta']:+.4f} (AUX-PARA-POSTHOC-MINUS-LOOKUP-MINI-V2)",
        reliable=True, actual_reliable=reliable_neg(SUP["MINI"]["pooled"]["paraphrase"]))
    chk("5.2 (Branch B): 'Haiku ... reliably below ... and 0.07)'", "0.07", SUP["H45"]["pooled"]["paraphrase"]["delta"], f"para_minus_lookup_posthoc.json H45 v2 superseded pooled paraphrase {SUP['H45']['pooled']['paraphrase']['delta']:+.4f} (AUX-PARA-POSTHOC-MINUS-LOOKUP-H45-V2)",
        reliable=True, actual_reliable=reliable_neg(SUP["H45"]["pooled"]["paraphrase"]))
    for c, nm in (("OP5", "Opus"), ("SOL", "Sol")):
        d = SUP[c]["pooled"]["paraphrase"]
        chk(f"5.2 (Branch B): '{nm} ... do not differ from it' (intervals include zero)", "not reliable", "not reliable" if not d["both_exclude_zero"] else "reliable", f"para_minus_lookup_posthoc.json {c} v2 superseded pooled paraphrase {d['delta']:+.4f} item [{d['ci_item']['ci_lo']:+.4f},{d['ci_item']['ci_hi']:+.4f}] persona [{d['ci_persona']['ci_lo']:+.4f},{d['ci_persona']['ci_hi']:+.4f}]")
    d = SUP["LUNA"]["pooled"]["paraphrase"]
    chk("5.2 (Branch B) / abstract / Conclusion: 'Luna ... edges above it by 0.04, reliable on the pooled metric'", "0.04", d["delta"], f"para_minus_lookup_posthoc.json LUNA v2 superseded pooled paraphrase {d['delta']:+.4f} item [{d['ci_item']['ci_lo']:+.4f},{d['ci_item']['ci_hi']:+.4f}] persona [{d['ci_persona']['ci_lo']:+.4f},{d['ci_persona']['ci_hi']:+.4f}] (AUX-PARA-POSTHOC-MINUS-LOOKUP-LUNA-V2)",
        reliable=True, actual_reliable=reliable_pos(d))
    chk("ruling check: Luna's pooled intervals are [+0.009, +0.084] and [+0.004, +0.089]", "[+0.009,+0.084] [+0.004,+0.089]", f"[{d['ci_item']['ci_lo']:+.3f},{d['ci_item']['ci_hi']:+.3f}] [{d['ci_persona']['ci_lo']:+.3f},{d['ci_persona']['ci_hi']:+.3f}]", "as above")
    m = SUP["LUNA"]["matched"]["paraphrase"]
    chk("5.2 (Branch B): Luna '... and not within triples' (matched interval includes zero)", "not reliable", "not reliable" if not m["both_exclude_zero"] else "reliable", f"para_minus_lookup_posthoc.json LUNA v2 superseded matched paraphrase {m['delta']:+.4f} triple [{m['ci_triple']['ci_lo']:+.4f},{m['ci_triple']['ci_hi']:+.4f}] persona [{m['ci_persona']['ci_lo']:+.4f},{m['ci_persona']['ci_hi']:+.4f}]")
    chk("appendix (the ruling): Luna's matched difference prints 0.04", "0.04", m["delta"], "as above")
    chk("appendix (the ruling): Luna's pooled lower bounds print 0.009 and 0.004", "0.009 / 0.004", f"{d['ci_item']['ci_lo']:.3f} / {d['ci_persona']['ci_lo']:.3f}", "as above")
    none_above = all(not reliable_pos(SUP[c]["pooled"]["original"]) for c in SUP)
    chk("5.2 (Branch B): 'On the original questions no model exceeded it' (supersession only, original questions, pooled: none reliably above)", "holds", "holds" if none_above else "fails",
        "para_minus_lookup_posthoc.json */v2/superseded/pooled/original: " + ", ".join(f"{c} {SUP[c]['pooled']['original']['delta']:+.4f}{'*' if SUP[c]['pooled']['original']['both_exclude_zero'] else ''}" for c in SUP))
    only_luna = [c for c in SUP if reliable_pos(SUP[c]["pooled"]["paraphrase"])] == ["LUNA"]
    chk("appendix (the ruling): Luna is the only reader above the lookup on the named state, reworded (pooled)", "holds", "holds" if only_luna else "fails", "as above, the paraphrase column")
    chk("appendix (the ruling): Haiku's pooled and matched readings disagree on supersession", "disagree", "disagree" if SUP["H45"]["pooled"]["paraphrase"]["both_exclude_zero"] != SUP["H45"]["matched"]["paraphrase"]["both_exclude_zero"] else "agree",
        f"H45 v2 superseded pooled paraphrase {SUP['H45']['pooled']['paraphrase']['delta']:+.4f} reliable={SUP['H45']['pooled']['paraphrase']['both_exclude_zero']}; matched {SUP['H45']['matched']['paraphrase']['delta']:+.4f} reliable={SUP['H45']['matched']['paraphrase']['both_exclude_zero']}")
    chk("appendix (the ruling): 'one of five comparisons' (five models on the named state)", "5", len(SUP), "para_minus_lookup_posthoc.json models with a v2 row")
    chk("5.2: 'Under the all-states summary the lookup loses 0.06 pooled, beyond tolerance'", "0.06", L["emb_v3"]["paired"]["delta"], f"lookups.json emb_v3 paired delta {L['emb_v3']['paired']['delta']:+.4f} (AUX-PARA-LOOKUP-EMB-V3)", reliable=True, actual_reliable=reliable_neg(L["emb_v3"]["paired"]))
    chk("5.2: the all-states lookup's pooled loss is beyond the tolerance", "beyond", "beyond" if abs(L["emb_v3"]["paired"]["delta"]) > tol else "within", "as above; the registered reading 'collapses'")
    dm = MT["emb_v3"]["pn_vs_present"]["paired"]["whole"]
    chk("5.2: '... and 0.02 within triples' (matched, not reliable)", "0.02", dm["delta"], f"para_scores.json matched emb_v3 pn_vs_present paired whole {dm['delta']:+.4f} triple [{dm['ci_triple']['ci_lo']:+.4f},{dm['ci_triple']['ci_hi']:+.4f}] persona [{dm['ci_persona']['ci_lo']:+.4f},{dm['ci_persona']['ci_hi']:+.4f}] (AUX-PARA-MATCHED-EMB_V3)",
        reliable=False, actual_reliable=dm["both_exclude_zero"])
    # ------------------------------------------------------------------ the abstract (the author's text), the Section 1 bullet, the Conclusion
    chk("abstract: 'Each of 148 questions'", "148", R125["readers"]["LOOKUP_v2"]["pn_vs_present"]["whole"]["n"], "r125_matched.json readers/LOOKUP_v2/pn_vs_present/whole/n (the triples); para_questions.json 148 rows")
    both_below = reliable_neg(SUP["MINI"]["pooled"]["paraphrase"]) and reliable_neg(SUP["H45"]["pooled"]["paraphrase"])
    chk("abstract / Conclusion: 'the two smaller models fall below it' (mini and Haiku reliably below the lookup on the named state, reworded, pooled)", "holds", "holds" if both_below else "fails", "MINI and H45 v2 superseded pooled paraphrase, as above")
    chk("abstract / Conclusion: 'one stronger model edges ahead by 0.04'", "0.04", SUP["LUNA"]["pooled"]["paraphrase"]["delta"], "LUNA v2 superseded pooled paraphrase, as above", reliable=True, actual_reliable=reliable_pos(SUP["LUNA"]["pooled"]["paraphrase"]))
    leads = {k: R125["paired"]["vs_lookup"][k]["pn_vs_present"]["whole"] for k in ("LUNA_v2", "SOL_v2", "OP5_v2")}
    chk("abstract: 'lead over the lookup of 0.08 to 0.10' (lower end; matched, whole set)", "0.08", min(v["delta"] for v in leads.values()), "r125_matched.json paired/vs_lookup/{LUNA_v2 +0.1014, SOL_v2 +0.0811, OP5_v2 +0.0980}/pn_vs_present/whole (AUX-CF2-R125-VS-LOOKUP)",
        reliable=True, actual_reliable=all(v["both_exclude_zero"] for v in leads.values()))
    chk("abstract: 'lead over the lookup of 0.08 to 0.10' (upper end)", "0.10", max(v["delta"] for v in leads.values()), "as above")
    hv = G133.hyb_vs_models()
    strong = {k: hv[k] for k in ("Opus 5", "GPT-5.6 Sol", "GPT-5.6 Luna")}
    chk("abstract: '(0.05 to 0.06 remains)' (pooled; lower end)", "0.05", min(v[0] for v in strong.values()), "r82_counterfactual/cf2/NUMBERS_CF2.md AUX-CF2-HYB-VS-MODELS (Opus +0.0540, Luna +0.0553, Sol +0.0635)", reliable=True, actual_reliable=all(v[1] for v in strong.values()))
    chk("abstract: '(0.05 to 0.06 remains)' (upper end)", "0.06", max(v[0] for v in strong.values()), "as above")
    closes = all(not R125["paired"]["contrasts"][n]["pn_vs_present"]["whole"]["both_exclude_zero"] for n in ("Luna minus hybrid", "Sol minus hybrid (P-H2)", "Opus minus hybrid"))
    chk("abstract: 'one count feature added to the lookup closes it within a question's three store versions' (no stronger model reliably above the count-feature lookup, matched)", "holds", "holds" if closes else "fails",
        "r125_matched.json paired/contrasts 'Luna minus hybrid', 'Sol minus hybrid (P-H2)', 'Opus minus hybrid'")
    mini_true, lookup_true = G133.e1r_row("| R-NOK-FRB | TRUE |")
    mini_bel, lookup_bel = G133.e1r_row("| R-NOK-FRB | BELIEVED |")
    chk("abstract: mini 0.73 under the ground-truth summary", "0.73", mini_true, "e1r_robustness/NUMBERS_E1R.md section 11 R-NOK-FRB TRUE, monitor (AUX-E1R-TRUE-NOK)")
    chk("abstract: mini 0.60 under FR-Bank's capped store-written summary", "0.60", mini_bel, "e1r_robustness/NUMBERS_E1R.md section 11 R-NOK-FRB BELIEVED, monitor (AUX-E1R-BELIEVED-NOK)")
    chk("abstract: the lookup 0.75 under the ground-truth summary", "0.75", lookup_true, "e1r_robustness/NUMBERS_E1R.md section 11 R-NOK-FRB TRUE, NB-6 (AUX-E1R-NB6)")
    chk("abstract: the lookup 0.59 under the capped store-written summary", "0.59", lookup_bel, "e1r_robustness/NUMBERS_E1R.md section 11 R-NOK-FRB BELIEVED, NB-6 (AUX-E1R-NB6)")
    mm = re.search(r"^\| H45-NOK \| Haiku 4\.5 \| NOK \| (\d+) \| (\d\.\d{4}) \| (\d\.\d{4}) \|", G133.R74, flags=re.M)
    chk("abstract: Haiku 0.82 under the ground-truth summary (n = 661)", "0.82", float(mm.group(3)), f"r74/NUMBERS_R74.md AUX-R74-X4-H45-NOK (n = {mm.group(1)})")
    mb = re.search(r"^\| INDEXED-BELIEVED-15 \| \*\*(\d\.\d{4})\*\* \|", G133.BH, flags=re.M)
    chk("abstract: Haiku 0.71 under FR-Bank's capped store-written summary", "0.71", float(mb.group(1)), "believed_h/NUMBERS_BELIEVED_H.md section 5 AUX-BH-H45-15")
    # ------------------------------------------------------------------ Limitations
    chk("Limitations: 'covers 115 of the 148 questions'", "115 / 148", f"{SC['n_pairs']} / {len(Q['rows'])}", "para_scores.json n_pairs; para_questions.json rows")
    chk("Limitations: 'Opus ran it with one draw'", "1", MO["OP5"]["k_new"], f"para_scores.json OP5 k_new (k_recorded {MO['OP5']['k_recorded']})")
    # ------------------------------------------------------------------ the appendix prose, tab:setup's row, the provenance row, tab:registrations-c
    chk("appendix: 148 questions; 24 failed the screen at drafting; 124 read; 9 excluded; 115 accepted", "148 / 24 / 124 / 9 / 115",
        f"{len(Q['rows'])} / {len(Q['rows']) - sum(1 for r in Q['rows'] if r['accepted'])} / {SH['n_rows']} / {SH['n_excluded_by_author']} / {SH['n_accepted']}", "para_questions.json rows and accepted; sheet.json n_rows, n_excluded_by_author, n_accepted (AUX-PARA-DRAFT, AUX-PARA-SHEET)")
    chk("appendix / tab:setup: supersession 76, retraction 17, expiry 22", "76 / 17 / 22", f"{SH['by_state']['SUPERSESSION']} / {SH['by_state']['RETRACTION']} / {SH['by_state']['EXPIRY']}", "sheet.json by_state (AUX-PARA-SHEET)")
    chk("appendix / tab:setup: 345 items", "345", SC["n"], "para_scores.json n")
    chk("appendix: the registered floor was 120", "120", SH["floor_registered"], "sheet.json floor_registered (the registration's STOP list); floor amended to 115 before any scoring call")
    xt = {"A": {30, 40, 77, 82, 28}, "B": {11, 46, 33, 79}, "C": {12, 27, 45, 49, 52, 57, 63, 68, 92, 94, 102, 112}}
    no_nums = {r["num"] for r in SH["rows"] if r["same_intent"] != "YES"}
    unfl = set(range(1, 125)) - xt["A"] - xt["B"] - xt["C"]
    chk("appendix: the assistant's flags against the read: A 5 of 5, B 3 of 4, C 1 of 12, unflagged 0 of 103", "5/5 3/4 1/12 0/103",
        f"{len(xt['A'] & no_nums)}/{len(xt['A'])} {len(xt['B'] & no_nums)}/{len(xt['B'])} {len(xt['C'] & no_nums)}/{len(xt['C'])} {len(unfl & no_nums)}/{len(unfl)}", "sheet.json rows (column 1) against the flag levels of reviews/para/PARA_AI_FLAGS.md (report_para.py FLAGS_A/B/C)")
    F1, F2 = SC["flags"]["author_column2_on_paraphrases"], SC["flags"]["token_rule_on_paraphrases"]
    chk("appendix: the attribute-naming split, 61 of 115 by the appendix's sentence and 32 of 115 by the token rule", "61 / 32", f"{F1['n_flagged_pairs']} / {F2['n_flagged_pairs']}", "para_scores.json flags (AUX-PARA-FLAGS both rules; AUX-PARA-SHEET column 2)")
    ex = SC["extras"]["target_name_similarity"]
    chk("appendix: mean cosine to the target name 0.486 to 0.317", "0.486 / 0.317", f"{ex['cosine_original_mean']:.3f} / {ex['cosine_paraphrase_mean']:.3f}", "para_scores.json extras.target_name_similarity (AUX-PARA-GENERIC)")
    chk("appendix: content-token overlap 0.484 to 0.000", "0.484 / 0.000", f"{ex['token_overlap_original_mean']:.3f} / {ex['token_overlap_paraphrase_mean']:.3f}", "as above")
    chk("appendix / tab:setup: draws mini 1, Haiku 5, Opus 1 (recorded 5), Luna 5, Sol 5", "1 5 1/5 5 5", f"{MO['MINI']['k_new']} {MO['H45']['k_new']} {MO['OP5']['k_new']}/{MO['OP5']['k_recorded']} {MO['LUNA']['k_new']} {MO['SOL']['k_new']}", "para_scores.json models/*/k_new, k_recorded")
    for sv, heads in (("v2", ["A", "D"]), ("v3", ["C", "D"])):
        chk(f"appendix: the branch readings under the {sv} summary", " ".join(heads), " ".join(SC["branches"][sv]["headings"]), f"para_scores.json branches/{sv}/headings (AUX-PARA-BRANCH-{sv.upper()}); status {SC['branches'][sv]['status']}")
    sens_lower = all(rec(SCs, k)["paraphrase"] <= rec(SC, k)["paraphrase"] for k in ("emb_v2", "lex_v2", "emb_v3", "lex_v3", "MINI_v2", "MINI_v3", "H45_v2", "H45_v3", "OP5_v2", "OP5_v3", "LUNA_v2", "SOL_v2"))
    chk("appendix: 'the picture is the same with the nine excluded pairs put back, slightly lower for every reader' (every paraphrase-set AUROC on the 124 at or below the 115's)", "holds", "holds" if sens_lower else "fails", "para_scores_all124.json against para_scores.json, every reader's paraphrase AUROC")
    chk("appendix: the same headings on the 124", "A D | C D", " | ".join(" ".join(SCs["branches"][sv]["headings"]) for sv in ("v2", "v3")), "para_scores_all124.json branches (sensitivity, not registered)")
    chk("tab:registrations-c: the registered text's sha256 45cad63d and the whole file 2848f1ad", "45cad63d 2848f1ad", f"{SC['registration_sha256'][:8]} {REG_WHOLE()[:8]}", "para_scores.json registration_sha256; sha256 of registrations/ADDENDUM_PARA.md (REPORT_PARA.md section 8)")
    # ------------------------------------------------------------------ RULING 3's check: Section 5.1's moved-count range on the counted states (matched; tab:cf-matched-ablations 'counted states' rows)
    CT = R125["paired"]["contrasts"]
    mc = {"Opus 5": CT["moved count Opus k5 minus sup-only k5"]["pn_vs_present"]["counted"], "GPT-5.6 Luna": CT["moved count Luna k5 minus sup-only k5 (E9)"]["pn_vs_present"]["counted"],
          "GPT-5.6 Sol": CT["moved count Sol k5 minus sup-only k5 (E9)"]["pn_vs_present"]["counted"]}
    for nm, d in mc.items():
        chk(f"5.1: {nm}'s matched moved-count fall on the counted states (five against five draws)", r2(d["delta"]), d["delta"], f"r125_matched.json paired/contrasts/.../pn_vs_present/counted {d['delta']:+.4f} (AUX-CF2-R125-CONTRASTS; tab:cf-matched-ablations)", reliable=True, actual_reliable=reliable_neg(d))
    chk("5.1: 'falling by 0.28 to 0.33 on the counted states' (lower end)", "0.28", min(abs(d["delta"]) for d in mc.values()), "the smallest of the three counted-states falls (Opus -0.2833); the R133 text's 0.27 was Luna's expiry value -0.2667, a per-state row")
    chk("5.1: 'falling by 0.28 to 0.33 on the counted states' (upper end)", "0.33", max(abs(d["delta"]) for d in mc.values()), "the largest of the three (Sol -0.3250)")
    return CHECKS


def rec(S, key):
    if key in S["lookups"]:
        return S["lookups"][key]
    c, sv = key.split("_")
    return S["models"][c][sv]


def REG_WHOLE():
    import hashlib
    return hashlib.sha256((ROOT / "registrations" / "ADDENDUM_PARA.md").read_bytes()).hexdigest()


def printed_forms():
    """Every numeral the pass prints in the main text (two-decimal forms and counts) and in the appendix prose: the allowed set for --built."""
    main = {"115", "0.02", "0.03", "0.06", "0.09", "0.12", "0.07", "0.04", "148", "0.28"}   # 0.28: RULING 3's corrected 5.1 range (Opus's counted-states fall -0.2833)
    appx = {"115", "148", "24", "124", "9", "120", "76", "17", "22", "345", "228", "5", "3", "4", "1", "12", "0", "103", "61", "32", "0.486", "0.317", "0.484", "0.000", "0.009", "0.004", "0.04", "42", "34", "0.05"}
    return main, appx


NUM = re.compile(r"(?<![\w.])[+-]?\d[\d,]*(?:\.\d+)?%?")


def numerals(text):
    text = "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in text.replace("\r\n", "\n").split("\n"))
    text = text.replace("{,}", ",")                 # R135: the thousands separator, as trace_scan_v13 reads it (2{,}333 is one token)
    text = re.sub(r"p\{[^}]*\}", " ", text)          # R135: tabular column specs (p{0.255\linewidth}) are layout, as trace_scan_v13 drops them
    text = re.sub(r"\\begin\{minipage\}(\[[^\]]*\])?\{[^}]*\}", " ", text)   # R137: minipage widths (0.625\linewidth) are layout (Figure 1's rendered summary)
    text = re.sub(r"\\makebox\[[^\]]*\](\[[^\]]*\])?", " ", text)              # R137: makebox lengths (7em) are layout
    text = re.sub(r"\\texttt\{[0-9a-f]{6,}\}", " ", text)          # commit hashes and sha256 prefixes (tab:registrations-*), before the macro strip
    text = re.sub(r"\\(ref|label|cite[pt]?|eqref|hd|vspace|hspace|setlength|includegraphics)\{[^}]*\}", " ", text)
    text = re.sub(r"\\(begin|end)\{[^}]*\}(\[[^\]]*\])?", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    return set(NUM.findall(text))


def split(tex):
    a = tex.index("\\begin{abstract}")
    b = tex.index("\\label{main-text-end}")
    c = tex.index("\\appendix")
    return tex[a:b], tex[c:]


def built_checks():
    new = (SUB / "paper_v23.tex").read_text(encoding="utf-8", errors="replace")
    old = subprocess.run(["git", "show", f"{BASE}:iclr2027_monitoring_submission/paper_v22.tex"], cwd=ROOT, capture_output=True).stdout.decode("utf-8", errors="replace")
    nm, na = split(new)
    if "\\begin{abstract}" in old:
        om, oa = split(old)
        om_nums, oa_nums = numerals(om), numerals(oa)
    else:
        # R138: an unpacked archive is neither a git checkout nor a place the previous draft
        # belongs. The packager derived these two sets from paper_v22.tex with the split()
        # and numerals() above, so this is the same check on the same input, reduced to the
        # only part of it the check reads.
        import json as _json
        _base = _json.loads((SUB / "v22_numerals.json").read_text(encoding="utf-8"))
        om_nums, oa_nums = set(_base["main"]), set(_base["appendix"])
    new_main = numerals(nm) - om_nums
    new_appx = numerals(na) - oa_nums
    main_allowed, appx_prose = printed_forms()
    frag = set()
    for f in sorted(RES.glob("para_tab_*.tex")):
        frag |= numerals(f.read_text(encoding="utf-8"))
    frag = {t.lstrip("+") for t in frag} | frag
    allowed_appx = {"0.76", "0.85"} | G133.routes_rows()[1] | {"557"} | frag | appx_prose
    out = []
    print(f"  built: main-text numerals new against the v22 main text: {sorted(new_main) or 'none'} (allowed: {sorted(main_allowed)})")
    print(f"  built: appendix numerals new against the v22 appendix: {len(new_appx)} tokens; not in the PARA fragment, the prose list or R133's set: {sorted(new_appx - allowed_appx) or 'none'}")
    if new_main - main_allowed:
        out.append(dict(where="built main text", printed=sorted(new_main - main_allowed), ok=False))
        print("  [MISMATCH] a numeral of the v23 main text is neither in the v22 main text nor one of the pass's printed forms")
    if new_appx - allowed_appx:
        out.append(dict(where="built appendix", printed=sorted(new_appx - allowed_appx), ok=False))
        print("  [MISMATCH] a numeral of the v23 appendix is not in the v22 appendix, the PARA fragment, the pass's prose list or R133's allowed set")
    return out


def main():
    checks()
    bad = [c for c in CHECKS if not c["ok"]]
    for c in CHECKS:
        v = c["value"]
        vs = f"{v:.4f}" if isinstance(v, float) else str(v)
        rel = "" if c["reliable"] is None else f"  reliable claimed={c['reliable']} actual={c['actual_reliable']}"
        print(f"  [{'ok' if c['ok'] else 'MISMATCH'}] {c['where']}: printed {c['printed']} <- {vs}{rel}  ({c['source']})")
    print(f"r134_number_gate: {len(CHECKS)} checks, {len(bad)} mismatches")
    if "--built" in sys.argv:
        bad += built_checks()
    if bad:
        print("r134_number_gate: FAIL")
        sys.exit(1)
    print("r134_number_gate: PASS")


if __name__ == "__main__":
    main()
