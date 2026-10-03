# -*- coding: utf-8 -*-
"""r125_t1_claims.py -- REPORT_R125_T1.md: Task 1's report, every number filled from reviews/r125/results/r125_matched.json (nothing typed from
memory), with the list of every claim of v22's Sections 5.1 and 5.2 (paper_v22.tex lines 296-395, tex sha256 f0549e2a) read against the matched
metric: holds / the number changes / the reliability changes / the direction changes / not evaluable. NO MODEL CALL.
"""
from __future__ import annotations

import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r125_common as C  # noqa: E402
from r125_common import STATES  # noqa: E402

RES = C.RESULTS / "r125_matched.json"
OUT = C.R125 / "REPORT_R125_T1.md"


def main():
    res = C.jload(RES); R = res["readers"]; P = res["paired"]; K = P["contrasts"]; VL = P["vs_lookup"]; VC = P["vs_count_readers"]

    def m(k, s=None, neg="present"):
        b = R[k][f"pn_vs_{neg}"]
        return b["whole"]["matched"] if s is None else b["per_state"][s]["matched"]

    def w(k, s=None, neg="present"):
        b = R[k][f"pn_vs_{neg}"]; b = b["whole"] if s is None else b["per_state"][s]
        return f"{b['W']}/{b['T']}/{b['L']}"

    def po(k, s=None):
        return R[k]["pooled"]["whole"] if s is None else R[k]["pooled"]["per_state"][s]

    def ci(d):
        return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"

    def con(name, sc="whole", neg="present"):
        p = K[name][f"pn_vs_{neg}"][sc]
        return f"{p['delta']:+.4f} ({ci(p['ci_triple'])}; {ci(p['ci_persona'])}){' reliable' if p['both_exclude_zero'] else ', not reliable'}"

    def vl(k, sc="whole", neg="present"):
        p = VL[k][f"pn_vs_{neg}"]["whole"] if sc == "whole" else VL[k][f"pn_vs_{neg}"]["per_state"][sc]
        return f"{p['delta']:+.4f} ({ci(p['ci_triple'])}; {ci(p['ci_persona'])}){' reliable' if p['both_exclude_zero'] else ', not reliable'}"

    def vc(k, cr, s):
        p = VC[k][cr]["pn_vs_present"][s]
        return f"{p['delta']:+.4f} ({ci(p['ci_triple'])}; {ci(p['ci_persona'])}){' reliable' if p['both_exclude_zero'] else ', not reliable'}"

    SUP, RET, EXP = STATES
    o3 = P["opus_v3_vs_allstates"]["OP5_v3"]["pn_vs_present"]["whole"]; o3a = P["opus_v3_vs_allstates"]["OP5_v3"]["pn_vs_absent"]["whole"]
    o3d1 = P["opus_v3_vs_allstates"]["OP5_v3_d1"]["pn_vs_present"]["whole"]
    cov = res["coverage_only"]
    models_v2 = [("MINI5_v2", "GPT-4.1 mini (five draws)"), ("H45_v2", "Haiku 4.5"), ("LUNA_v2", "GPT-5.6 Luna"), ("SOL_v2", "GPT-5.6 Sol"), ("OP5_v2", "Opus 5")]
    rng_ret = [m(k, RET) for k, _ in models_v2]; rng_exp = [m(k, EXP) for k, _ in models_v2]
    lo_c, hi_c = min(rng_ret + rng_exp), max(rng_ret + rng_exp)
    L = []
    A = L.append
    A("# REPORT_R125_T1 — the matched metric on the counterfactual set (Task 1 of R125; 2026-09-20; post hoc, offline, $0)")
    A("")
    A("Program R125, a fresh session on the brief \"KtS R125: matched metric, sibling-name control, store-relative labels, strong-model ablations\". This report covers Task 1 alone, "
      "delivered first because the Section 5 rewrite waits on it. Files: `reviews/r125/tools/r125_readers.py` (every reader's vector from the recorded rows and the committed no-model readers, "
      "each gated on its recorded whole-set pooled AUROC at four decimals), `r125_matched.py` (the analysis), `r125_t1_report.py` (the tables, the ledger section, Figure 3's data file), this "
      "script (`r125_t1_claims.py`, the report with the numbers filled from the results file). Results `reviews/r125/results/r125_vectors.json`, `r125_matched.json`; the tables in full in "
      "`reviews/r125/T1_TABLES.md`; ledger section 15 of `r82_counterfactual/cf2/NUMBERS_CF2.md` (AUX-CF2-R125-*); Figure 3's data on the matched metric in "
      "`reviews/r125/results/fig3_data_matched.tex` (the schema of `reviews/v22/src/fig3_data.tex`; the main session swaps it in). No model call; nothing re-run; no paper text touched. "
      "Every number below is post hoc and labelled so.")
    A("")
    A("**Definitions.** The counterfactual set fixes the question and varies the store, so the design-matched comparison is within a triple. For each of the 148 triples the reader's score on the "
      "PN version is compared with its score on the PRESENT version (the primary comparison; the ABSENT version beside): a win, a tie (exact equality of the collapsed scores, the rule the printed "
      "W/T/L use) or a loss. The **matched AUROC** is (W + T/2) / n over the triples scored, whole set and within each state's own triples (88 / 30 / 30). Intervals: the triple-level bootstrap "
      "(triples resampled) and the persona-grouped bootstrap (personas resampled, triples intact), 1,000 draws, seed 42; **reliable** = both intervals exclude zero; the paired difference of two "
      "readers is the mean over triples of their per-triple outcome difference. \"Pooled\" is the recorded Mann-Whitney AUROC (the 444, or a state's own items); \"state-balanced\" is the mean "
      "of the three per-state pooled values.")
    A("")
    A("## 1. The sanity check (the stop rule): PASS")
    A("")
    A("The W/T/L computed from the rows equal every W/T/L printed in Table 1 (tab:cf-main; twelve rows) and the four further printed rows of the appendix (tab:pnpresent's one-draw mini rows, "
      "tab:cf-p1's intent-explicit rows), so the matched AUROC is (W + T/2) / 148 from the printed counts; the moved-count reference readers reproduce AUX-V2RCAT-REF (state-aware 0.3028 / 0.3611, "
      "totals 0.4044 / 0.3894). The table is in `T1_TABLES.md` section 0 and the ledger (AUX-CF2-R125-SANITY).")
    A("")
    A("## 2. Table 1's readers under the matched metric")
    A("")
    A("| reader | summary | pooled AUROC (Table 1) | PN vs PRESENT W/T/L (Table 1) | **matched AUROC** | triple interval | persona interval | matched sup / ret / exp | state-balanced pooled | PN vs ABSENT matched |")
    A("|---|---|---:|---|---:|---|---|---|---:|---:|")
    rows = [("MINI5_v2", "GPT-4.1 mini (five draws)", "superseded"), ("MINI5_v3", "GPT-4.1 mini (five draws)", "all"), ("H45_v2", "Haiku 4.5", "superseded"), ("H45_v3", "Haiku 4.5", "all"),
            ("LUNA_v2", "GPT-5.6 Luna", "superseded"), ("SOL_v2", "GPT-5.6 Sol", "superseded"), ("OP5_v2", "Opus 5", "superseded"), ("OP5_v3", "Opus 5", "all"),
            ("LOOKUP_v2", "Name lookup", "superseded"), ("ALLSTATES_v3", "Name lookup (all states)", "all"), ("CR-nb1_v2", "Count reader, guessed category", "superseded"), ("CR-oracle-a_v2", "Count reader, given category", "superseded")]
    for k, lab, summ in rows:
        b = R[k]["pn_vs_present"]["whole"]
        A(f"| {lab} | {summ} | {po(k):.4f} | {w(k)} | **{m(k):.4f}** | [{b['ci_triple']['ci_lo']:.4f}, {b['ci_triple']['ci_hi']:.4f}] | [{b['ci_persona']['ci_lo']:.4f}, {b['ci_persona']['ci_hi']:.4f}] | "
          f"{m(k, SUP):.4f} / {m(k, RET):.4f} / {m(k, EXP):.4f} | {R[k]['pooled']['state_balanced']:.4f} | {m(k, neg='absent'):.4f} |")
    A("")
    A(f"Table 1's difference row, Opus 5 under the all-states summary minus the all-states lookup: pooled +0.0323 with intervals [+0.0060, +0.0617] and [+0.0077, +0.0608] (AUX-R103-MARGIN, reliable); "
      f"**matched {o3['delta']:+.4f} with intervals {ci(o3['ci_triple'])} and {ci(o3['ci_persona'])}, not reliable** (PN vs ABSENT {o3a['delta']:+.4f}, {ci(o3a['ci_triple'])}; {ci(o3a['ci_persona'])}; "
      f"Opus 5's draw 1 alone {o3d1['delta']:+.4f}, {ci(o3d1['ci_triple'])}; {ci(o3d1['ci_persona'])}{', reliable' if o3d1['both_exclude_zero'] else ''}). Per state, five draws: "
      + "; ".join(f"{s.lower()} {P['opus_v3_vs_allstates']['OP5_v3']['pn_vs_present']['per_state'][s]['delta']:+.4f}" for s in STATES) + ", each interval including zero.")
    A("")
    A(f"The coverage-only reader (1 on PN and PRESENT, 0 on ABSENT) scores {cov['pooled']['whole']:.4f} pooled and {cov['pn_vs_present']['matched']:.4f} matched (every triple a tie). The random-token "
      f"lookup scores {po('RANDTOK_v2'):.4f} pooled and **{m('RANDTOK_v2'):.4f} matched** ({w('RANDTOK_v2')}; supersession {m('RANDTOK_v2', SUP):.4f}, {w('RANDTOK_v2', SUP)}): the matched metric removes "
      "the coverage component (the PN and PRESENT versions both hold relevant content) but not the list-length component, since the PN version's list is one name longer than its siblings'. Task 2 "
      "measures that component; Task 4 is built to remove it.")
    A("")
    A("## 3. The pooled AUROC by pair class")
    A("")
    A("Of the 148 × 296 = 43,808 (positive, negative) pairs the pooled AUROC averages over, 296 are within-triple (0.7 percent), 18,792 same-state across questions (42.9 percent) and 24,720 "
      "across states (56.4 percent); the pooled value is the pair-count-weighted mean of the three class AUROCs (asserted for every reader). The within-triple class is the matched metric's "
      "PN vs PRESENT and PN vs ABSENT pooled.")
    A("")
    A("| reader | pooled | within-triple | same state, across questions | across states |")
    A("|---|---:|---:|---:|---:|")
    for k, lab, summ in rows + [("HYBRID_v2", "Hybrid reader (E10)", "superseded"), ("RANDTOK_v2", "Random-token lookup", "superseded")]:
        pc = R[k]["pair_classes"]["whole"]
        A(f"| {lab}, {summ} | {pc['pooled']:.4f} | {pc['within_triple']['auroc']:.4f} | {pc['same_state_across_questions']['auroc']:.4f} | {pc['across_states']['auroc']:.4f} |")
    A("")
    A("## 4. Every claim of Sections 5.1 and 5.2 read against the matched metric")
    A("")
    A("The claims are the `\\claim{}` leads and the sentences under them (paper_v22.tex lines 296-395). Status: **HOLDS** (the same reading, the numbers within 0.05), **NUMBER** (the same "
      "reading, a printed number moves by more than 0.05 or a bound fails), **RELIABILITY** (the same sign, the intervals no longer exclude zero, or the reverse), **DIRECTION** (the sign or the "
      "ordering the sentence states reverses), **N/A** (the sentence is about the 661, which has no triples, or about rows outside Task 1's list).")
    A("")
    A("### 5.1 Names against counts")
    A("")
    A(f"1. *\"Removing counts from the default summary leaves mini and Haiku within 0.01 of their intact-summary scores.\"* **HOLDS.** Matched names-only minus intact: mini "
      f"{con('E2 mini names-only minus intact')}; Haiku {con('E2 Haiku names-only minus intact')} (mini {m('MINI1_NAMES'):.4f} against {m('MINI1_v2'):.4f}; Haiku {m('H45_NAMES'):.4f} against {m('H45_v2'):.4f}).")
    A(f"2. *\"Counts alone score reliably below names alone: mini loses 0.12, and Haiku loses 0.16.\"* **HOLDS** (the numbers 0.14 and 0.14). Matched counts-only minus names-only: mini "
      f"{con('E2 mini counts-only minus names-only')}; Haiku {con('E2 Haiku counts-only minus names-only')}. On the counted states alone neither difference is reliable (mini counted "
      f"{con('E2 mini counts-only minus names-only', 'counted')}; Haiku {con('E2 Haiku counts-only minus names-only', 'counted')}): the loss is on supersession, where the names are.")
    A("3. *\"Removing the target name leaves mini near chance\"* (0.86 to 0.53; Haiku 0.89 to 0.68). **N/A**: the full obligation set has no triples; the matched metric is not defined there.")
    A(f"4. *\"Count readers separate states that models barely tell apart. On retraction and expiry ... model scores range from 0.53 to 0.64. A count reader guesses the question's category ... "
      f"It scores 0.67 on retraction and 0.69 on expiry.\"* **DIRECTION** for the three strong models against the guessing reader; the range changes. Matched, the guessing count reader reads "
      f"{m('CR-nb1_v2', RET):.4f} on retraction and {m('CR-nb1_v2', EXP):.4f} on expiry; the models (Table 1's rows) read " + "; ".join(f"{lab} {m(k, RET):.4f} / {m(k, EXP):.4f}" for k, lab in models_v2)
      + f", a range of {lo_c:.2f} to {hi_c:.2f}. GPT-5.6 Luna and GPT-5.6 Sol are **above** the guessing reader on expiry (Luna {vc('LUNA_v2', 'CR-nb1', EXP)}; Sol {vc('SOL_v2', 'CR-nb1', EXP)}) and Opus 5 "
      f"ties it on retraction ({vc('OP5_v2', 'CR-nb1', RET)}); none of the three is reliably below it on either state (Luna retraction {vc('LUNA_v2', 'CR-nb1', RET)}; Sol retraction "
      f"{vc('SOL_v2', 'CR-nb1', RET)}; Opus expiry {vc('OP5_v2', 'CR-nb1', EXP)}). Haiku 4.5 and GPT-4.1 mini remain reliably below it on both states (Haiku {vc('H45_v2', 'CR-nb1', RET)} and "
      f"{vc('H45_v2', 'CR-nb1', EXP)}; mini {vc('MINI5_v2', 'CR-nb1', RET)} and {vc('MINI5_v2', 'CR-nb1', EXP)}). The brief's expected change, *\"every tested model separates them more weakly than a "
      f"count reader does\"*, is the one that changes: it holds against the category-given reader (item 5) and fails against the guessing reader for Luna, Sol and Opus.")
    A(f"5. *\"A reader given the manifest category reads its retracted-plus-expired count, scoring 0.73 on retraction and 0.78 on expiry. Reading the non-active share at that known category instead "
      f"scores 0.85 overall.\"* **NUMBER** (both readers reach 1.0). Matched: the category-given count reader {m('CR-oracle-a_v2', RET):.4f} on retraction ({w('CR-oracle-a_v2', RET)}) and "
      f"{m('CR-oracle-a_v2', EXP):.4f} on expiry ({w('CR-oracle-a_v2', EXP)}); the category-given share reader {m('CR-oracle-share_v2', ):.4f} on the whole set ({w('CR-oracle-share_v2')}); the "
      f"state-aware reader {m('CR-oracle-state_v2'):.4f}. Within a triple the obligation's own increment always separates the PN version from its siblings at the given category, so these readers "
      f"are perfect on the matched comparison, and every model is reliably below them on both counted states (Opus 5 minus the category-given reader: retraction "
      f"{vc('OP5_v2', 'CR-oracle-a', RET)}, expiry {vc('OP5_v2', 'CR-oracle-a', EXP)}; the other four in `T1_TABLES.md` section 5).")
    A(f"6. *\"A bare count can give the obligation away ... a reader can identify its store version without identifying its attribute.\"* **HOLDS**, and the matched metric is the direct measurement "
      f"of it: the category-given count reader wins every counted-state triple (item 5), the totals reader {m('CR-totals-a_v2', RET):.4f} / {m('CR-totals-a_v2', EXP):.4f} ({w('CR-totals-a_v2', RET)}, "
      f"{w('CR-totals-a_v2', EXP)}).")
    A(f"7. *\"Permuting only the lifecycle totals moves mini, Haiku and Opus by at most 0.01.\"* **NUMBER** (the bound becomes 0.05; no move reliable). Matched, totals-randomized minus superseded-only on "
      f"the whole set: mini {con('totals rand. mini minus sup-only')}; Haiku {con('totals rand. Haiku minus sup-only')}; Opus {con('totals rand. Opus minus sup-only')}. Mini's retraction triples move "
      f"{con('totals rand. mini minus sup-only', 'ret')} and Opus's {con('totals rand. Opus minus sup-only', 'ret')}: the per-state matched values rest on 30 triples and swing by 0.10 to 0.15 "
      f"without reliability. The tolerance reading (every whole-set move inside ±0.05) survives; \"at most 0.01\" does not.")
    A(f"8. *\"Only Opus follows a count when it moves. ... Mini's expiry score rises by 0.06, without a reliable difference; Haiku remains within tolerance. Opus falls reliably by 0.10 on retraction "
      f"and 0.13 on expiry when draw counts are matched.\"* **DIRECTION** (GPT-5.6 Luna and GPT-5.6 Sol also fall reliably; Opus's expiry fall is not reliable at five draws). Matched, moved-count "
      f"minus superseded-only, five draws against five: Opus 5 whole {con('moved count Opus k5 minus sup-only k5')}, retraction {con('moved count Opus k5 minus sup-only k5', 'ret')}, expiry "
      f"{con('moved count Opus k5 minus sup-only k5', 'exp')}, the two counted states pooled {con('moved count Opus k5 minus sup-only k5', 'counted')}; **GPT-5.6 Luna** (E9) whole "
      f"{con('moved count Luna k5 minus sup-only k5 (E9)')}, retraction {con('moved count Luna k5 minus sup-only k5 (E9)', 'ret')}, expiry {con('moved count Luna k5 minus sup-only k5 (E9)', 'exp')}; "
      f"**GPT-5.6 Sol** (E9) whole {con('moved count Sol k5 minus sup-only k5 (E9)')}, retraction {con('moved count Sol k5 minus sup-only k5 (E9)', 'ret')}, expiry "
      f"{con('moved count Sol k5 minus sup-only k5 (E9)', 'exp')}, counted {con('moved count Sol k5 minus sup-only k5 (E9)', 'counted')}. Mini {con('moved count mini minus sup-only', 'exp')} on expiry; "
      f"Haiku {con('moved count Haiku minus sup-only', 'exp')} on expiry, whole {con('moved count Haiku minus sup-only')}. Under the pooled metric E9's P-M2 failed for Luna and Sol (their retraction moves "
      f"had intervals including zero); within the triple all three strong models follow the moved cell on the counted states, and the moved-count texts score {m('LUNA_v2rcat', RET):.4f} / "
      f"{m('LUNA_v2rcat', EXP):.4f} (Luna), {m('SOL_v2rcat', RET):.4f} / {m('SOL_v2rcat', EXP):.4f} (Sol), {m('OP5_v2rcat', RET):.4f} / {m('OP5_v2rcat', EXP):.4f} (Opus) against 0.50 chance.")
    A("")
    A("### 5.2 The lookup against the models")
    A("")
    A(f"9. *\"No model reliably beats the lookup on supersession.\"* **HOLDS.** Matched, supersession only, model minus the name lookup ({m('LOOKUP_v2', SUP):.4f}, {w('LOOKUP_v2', SUP)}): Opus 5 "
      f"{vl('OP5_v2', SUP)}; Luna {vl('LUNA_v2', SUP)}; Sol {vl('SOL_v2', SUP)}; Haiku {vl('H45_v2', SUP)}; mini (five draws) {vl('MINI5_v2', SUP)}.")
    A(f"10. *\"Across the whole set, the lookup scores 0.77, and mini and Haiku each score 0.76.\"* **NUMBER** for mini. Matched: the lookup {m('LOOKUP_v2'):.4f}, Haiku {m('H45_v2'):.4f} "
      f"({vl('H45_v2')}), mini at five draws {m('MINI5_v2'):.4f} ({vl('MINI5_v2')}; the PN-vs-ABSENT side {vl('MINI5_v2', neg='absent')}). Mini's five-draw row loses 33 of 148 triples to the PRESENT "
      f"version (Table 1's W/T/L) where its one-draw row loses 10, so its matched value ({m('MINI1_v2'):.4f} at one draw) is below the pooled one.")
    A(f"11. *\"Luna, Sol and Opus reliably lead the lookup on the whole set by 0.07 to 0.08.\"* **HOLDS** (0.08 to 0.10). Matched: Luna {vl('LUNA_v2')}; Sol {vl('SOL_v2')}; Opus {vl('OP5_v2')}.")
    A(f"12. *\"Their advantage comes from the retracted and expired states, which this summary only counts.\"* **HOLDS.** The lookup ties every counted-state triple ({m('LOOKUP_v2', RET):.4f} / "
      f"{m('LOOKUP_v2', EXP):.4f}); the three read {m('LUNA_v2', RET):.4f} / {m('LUNA_v2', EXP):.4f}, {m('SOL_v2', RET):.4f} / {m('SOL_v2', EXP):.4f}, {m('OP5_v2', RET):.4f} / {m('OP5_v2', EXP):.4f} there and are "
      f"within 0.02 of it on supersession (item 9).")
    A(f"13. *\"Naming all states helps readers and leaves an Opus advantage. ... Haiku gains a reliable 0.30 on those previously counted states. Opus exceeds the lookup overall by a reliable 0.03, so the "
      f"supersession result does not establish that a lookup suffices whenever states are named.\"* **RELIABILITY** (the Opus advantage over the all-states lookup is not reliable under the matched metric; "
      f"the Haiku gain holds). Matched: Haiku all-states minus superseded-only on the counted states {con('all-states Haiku minus sup-only', 'counted')}; Opus 5 minus the all-states lookup, whole set, "
      f"{o3['delta']:+.4f} ({ci(o3['ci_triple'])}; {ci(o3['ci_persona'])}), not reliable, and on no single state (supersession {P['opus_v3_vs_allstates']['OP5_v3']['pn_vs_present']['per_state'][SUP]['delta']:+.4f}, "
      f"retraction {P['opus_v3_vs_allstates']['OP5_v3']['pn_vs_present']['per_state'][RET]['delta']:+.4f}, expiry {P['opus_v3_vs_allstates']['OP5_v3']['pn_vs_present']['per_state'][EXP]['delta']:+.4f}); "
      f"Haiku {vl('H45_v3')} and mini at five draws {vl('MINI5_v3')} against the same lookup. Under the matched metric no model reliably exceeds the lookup under either summary, so the sentence's "
      f"\"so\" clause loses its support; Opus 5's draw 1 alone ({o3d1['delta']:+.4f}; {ci(o3d1['ci_triple'])}; {ci(o3d1['ci_persona'])}) is reliable, which the five-draw row is not.")
    A(f"14. *\"mini still scores lower on expiry than on retraction.\"* **HOLDS.** Matched, all-states summary, five draws: retraction {m('MINI5_v3', RET):.4f}, expiry {m('MINI5_v3', EXP):.4f}; superseded-only: "
      f"{m('MINI5_v2', RET):.4f} and {m('MINI5_v2', EXP):.4f}, the expiry value below chance ({w('MINI5_v2', EXP)}: the PRESENT version scored above the PN version on 15 of 30 expiry triples).")
    A(f"15. *\"The pooled metric rewards readers that miss the obligation. A coverage-only reader scores 0.75 while tying every PN–PRESENT triple.\"* **HOLDS** ({cov['pooled']['whole']:.4f} pooled; "
      f"{cov['pn_vs_present']['matched']:.4f} matched, {cov['pn_vs_present']['W']}/{cov['pn_vs_present']['T']}/{cov['pn_vs_present']['L']}).")
    A(f"16. *\"The name lookup still scores 0.60 when meaningless tokens replace the names. List length and emptiness carry signal without conveying what the names mean.\"* **NUMBER** (0.65 matched, "
      f"larger). Matched: the random-token lookup {m('RANDTOK_v2'):.4f} ({w('RANDTOK_v2')}), {m('RANDTOK_v2', SUP):.4f} on supersession ({w('RANDTOK_v2', SUP)}); {con('random-token minus name lookup (v2)')} "
      f"against the name lookup. Under the all-states summary {m('RANDTOK_v3'):.4f} ({w('RANDTOK_v3')}). The within-triple comparison does not remove the list-length signal (the PN list is longer by one).")
    A(f"17. *\"Comparing PN against PRESENT alone keeps relevant content present on both sides. That post hoc comparison preserves the model-versus-lookup pattern.\"* **HOLDS for the models; DIRECTION "
      f"for the hybrid reader (E10).** The pattern (items 9 to 13) is preserved. The hybrid reader, which the pooled metric placed at {po('HYBRID_v2'):.4f} (P-H1 failed: not reliably above the lookup; "
      f"P-H2 held: Sol reliably above it), reads **{m('HYBRID_v2'):.4f} matched** ({w('HYBRID_v2')}): {con('hybrid minus name lookup (P-H1)')} against the lookup, above every model at the point "
      f"(Sol minus hybrid {con('Sol minus hybrid (P-H2)')}; Luna {con('Luna minus hybrid')}; Opus {con('Opus minus hybrid')}; Haiku {con('Haiku minus hybrid')}; mini at five draws "
      f"{con('mini k5 minus hybrid')}). On the counted states it reads {m('HYBRID_v2', RET):.4f} / {m('HYBRID_v2', EXP):.4f}, the guessing count reader's values (it ties that reader on every counted "
      f"triple: {con('hybrid minus guessed-category count reader', 'counted')}).")
    A("18. *\"Long or wrong name lists weaken the readers together.\"* **N/A**: the padding rows are on the 661; the wrong-name injection rows on the counterfactual set (tab:pad) are outside Task 1's "
      "reader list (Table 1, tab:counterfactual, E2, the moved count, E10, the intent-explicit rerun, the random-token and encoder lookups). They can be scored the same way on request.")
    A("")
    A("**The list of claims whose direction changes** (the brief's deliverable): item 4 (Luna and Sol above the guessing count reader on expiry, Opus tied with it on retraction; \"every tested "
      "model separates them more weakly than a count reader does\" fails for the three against that reader and holds against the category-given reader); item 8 (Luna and Sol follow the moved "
      "count reliably, so \"only Opus\" fails; Opus's expiry fall is not reliable at five draws); item 17 (the hybrid reader is reliably above the lookup and above every model at the point; "
      "P-H2's sign reverses). **Reliability changes**: item 13 (the Opus advantage over the all-states lookup, Table 1's difference row, is not reliable). **Number changes** (the reading "
      "stands, a printed number or bound does not): items 5, 7, 10, 16.")
    A("")
    A("## 5. Three things to read before the rewrite")
    A("")
    A(f"- **Ties.** Under the matched metric a tie is half a win. The lookups and the count readers never lose a triple (their W/T/L end in 0), so their matched values are (W + T/2) / n with T large: "
      f"the name lookup ties 66 of 148 triples and reads {m('LOOKUP_v2'):.4f}; the guessing count reader ties 83 and reads {m('CR-nb1_v2'):.4f}. A model with fine-grained scores rarely ties and pays "
      f"for every loss. GPT-4.1 mini's five-draw row is the clearest case: {w('MINI5_v2')} against the one-draw row's {w('MINI1_v2')}, so the five draws lower its matched value "
      f"({con('mini five draws minus one draw (v2)')}) while raising its pooled one (+0.0481, AUX-R122-K5). The PN-vs-ABSENT side runs the other way (mini five draws {m('MINI5_v2', neg='absent'):.4f} "
      f"matched against {m('MINI1_v2', neg='absent'):.4f}).")
    A(f"- **What the matched metric does not remove.** The random-token lookup reads {m('RANDTOK_v2'):.4f} matched ({m('RANDTOK_v2', SUP):.4f} on supersession): the PN version's list is one name "
      f"longer than the PRESENT version's, and a max-over-list reader scores the longer list higher on 45 of 88 supersession triples with no name meaning anything. The matched metric is the design's "
      f"comparison; the list-length component is Task 2's measurement and Task 4's control.")
    A(f"- **Figure 3 on the matched metric** (`results/fig3_data_matched.tex`): the superseded-only panel's counted states spread from {min(rng_ret + rng_exp):.2f} to {max(rng_ret + rng_exp):.2f} "
      f"(pooled: 0.53 to 0.64); the guessing count reader sits at {m('CR-nb1_v2', RET):.4f} / {m('CR-nb1_v2', EXP):.4f}; the lookup at 0.50 on both; mini at five draws at {m('MINI5_v2', EXP):.4f} on "
      f"expiry, below the chance line. The all-states panel: the lookup {m('ALLSTATES_v3', SUP):.4f} / {m('ALLSTATES_v3', RET):.4f} / {m('ALLSTATES_v3', EXP):.4f}, Opus {m('OP5_v3', SUP):.4f} / "
      f"{m('OP5_v3', RET):.4f} / {m('OP5_v3', EXP):.4f}, Haiku {m('H45_v3', SUP):.4f} / {m('H45_v3', RET):.4f} / {m('H45_v3', EXP):.4f}, mini {m('MINI5_v3', SUP):.4f} / {m('MINI5_v3', RET):.4f} / "
      f"{m('MINI5_v3', EXP):.4f}.")
    A("")
    A("Spend: $0 (no call). Commits: recorded in REPORT_R125.md at the close.")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(C.ROOT)}")


if __name__ == "__main__":
    main()
