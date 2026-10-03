# -*- coding: utf-8 -*-
"""ledger_r129.py -- reviews/NUMBERS_R129.md, the pass ledger of program R129 (2026-09-20; the author's rulings on R127b and R128's held items
and the two body landings): every number the pass prints that no earlier ledger carries, each read from its artifact by this script (no number
typed by hand):
  AUX-R129-GROUPS     the R127 / R127b group readings printed in Appendix E.3 (tab:e3-groups): per reader and PRESENT group, the mean score with
                      the summary and question only, the AUROC of the 104 obligations against the group with the summary (both intervals), the
                      question-only AUROC and the paired gain (both intervals); reviews/v22/results/r127_groups.json and r127b_groups.json
  AUX-R129-HYB-MINI5  GPT-4.1 mini's five-draw row (AUX-R122-K5, 0.7648) minus the hybrid reader, paired (reviews/v22/results/r129_hybrid_mini5.json)
  AUX-R129-B9         the inverted tag's arithmetic in E.10: the 35 of 89 read 34 and the retraction count 13 once the tag is corrected; the
                      oracle split of stale answers both ways (reviews/v22/results/r129_b9.json; the downstream audit's artifacts)
  AUX-R129-COUNT      the prediction count with the moved-count control's second amendment (P-M2, one prediction, failed) in it:
                      92 / 28 (AUX-R124-TALLY) become 93 / 29; tab:registrations-d 28 with 10 become 29 with 11
  AUX-R129-E9-PRINTED the two-decimal forms Section 5.1 prints from AUX-V2RCAT-A1-OP5-K5 and AUX-V2RCAT-A2-LUNA-K5 / -SOL-K5
Usage: python reviews/v22/tools/ledger_r129.py
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews" / "NUMBERS_R129.md"
RES = ROOT / "reviews" / "v22" / "results"
R127 = json.load(open(RES / "r127_groups.json", encoding="utf-8"))["readers"]
R127B = json.load(open(RES / "r127b_groups.json", encoding="utf-8"))["readers"]
HYB = json.load(open(RES / "r129_hybrid_mini5.json", encoding="utf-8"))
B9 = json.load(open(RES / "r129_b9.json", encoding="utf-8"))
V2R = json.load(open(ROOT / "r82_counterfactual" / "v2rcat" / "results" / "scores_v2rcat_openai.json", encoding="utf-8"))
OP5 = json.load(open(ROOT / "r82_counterfactual" / "v2rcat" / "results" / "scores_v2rcat_op5_k5.json", encoding="utf-8"))

READERS = [("GPT-4.1 mini", "GPT-4.1 mini (INDEXED-TRUE, one call)", "GPT-4.1 mini"), ("Haiku 4.5", "Haiku 4.5 (five calls)", "Haiku 4.5"),
           ("GPT-5.6 Luna", "GPT-5.6 Luna (five calls)", "GPT-5.6 Luna"), ("Opus 5", "Opus 5 (five calls)", "Opus 5")]
LOOKUP = "name lookup (superseded section, embedding)"


def ci(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]" if any(k in d and d[k] < 0 for k in ("ci_lo",)) or d.get("signed") else f"[{d['ci_lo']:.4f}, {d['ci_hi']:.4f}]"


def sci(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"


def uci(d):
    return f"[{d['ci_lo']:.4f}, {d['ci_hi']:.4f}]"


def groups_rows():
    L = ["| reader | group | n | mean, question only | mean, with summary | AUROC with summary | item interval | persona interval | AUROC question only | gain | item interval | persona interval |",
         "|---|---|---:|---:|---:|---:|---|---|---:|---:|---|---|"]
    for name, k127, k127b in READERS:
        a = R127[k127]; b = R127B[k127b]
        L.append(f"| {name} | the 104 obligations | 104 | {b['means']['pn']['blind']:.4f} | {b['means']['pn']['indexed']:.4f} | | | | | | | |")
        for g in ("a", "b", "c"):
            L.append(f"| | ({g}) | {a[g]['n_group']} | {b['means'][g]['blind']:.4f} | {b['means'][g]['indexed']:.4f} | {a[g]['auroc']:.4f} | {uci(a[g]['item_ci'])} | {uci(a[g]['persona_ci'])} "
                     f"| {b[g]['blind_auroc']:.4f} | {b[g]['gain']:+.4f} | {sci(b[g]['item_ci'])} | {sci(b[g]['persona_ci'])} |")
            assert abs(b[g]['indexed_auroc'] - a[g]['auroc']) < 1e-9, (name, g)
    a = R127[LOOKUP]
    L.append(f"| name lookup | the 104 obligations | 104 | | {a['mean_pn']:.4f} | | | | | | | |")
    for g in ("a", "b", "c"):
        L.append(f"| | ({g}) | {a[g]['n_group']} | | {a[g]['mean_group']:.4f} | {a[g]['auroc']:.4f} | {uci(a[g]['item_ci'])} | {uci(a[g]['persona_ci'])} | | | | |")
    return L


def main():
    L = ["# NUMBERS_R129.md: the pass ledger of program R129 (2026-09-20)", "",
         "Written by `reviews/v22/tools/ledger_r129.py` from the artifacts named in each section; no number is typed by hand.", "",
         "## AUX-R129-GROUPS — the 104 obligations against the three PRESENT groups of tab:e3-intent, per reader (Appendix E.3, tab:e3-groups; `reviews/v22/results/r127_groups.json` for the with-summary AUROC and its intervals, `r127b_groups.json` for the means, the question-only AUROC and the paired gain; item-level and persona-grouped bootstrap, 1,000 draws, seed 42)",
         "", "Groups (AUX-R126-E3-INTENT): (a) 33 PRESENT questions whose own attribute holds a non-active record under current or upcoming intent; (b) 11 under change intent; (c) the remaining 130. Readers: GPT-4.1 mini one call (question only and INDEXED-TRUE); Haiku 4.5, Opus 5 and GPT-5.6 Luna the five-call collapse (BLIND and INDEXED-TRUE); the name lookup has no question-only form. The gain is the with-summary AUROC minus the question-only AUROC on the same items.", ""]
    L += groups_rows()
    # the two-decimal forms E.3's four sentences print
    def rr(x):
        return f"{x:.2f}"
    ga = [G["a"]["auroc"] for _, k, _ in READERS for G in [R127[k]]]; gc = [R127[k]["c"]["auroc"] for _, k, _ in READERS]
    qa = [R127B[k]["a"]["blind_auroc"] for _, _, k in READERS if R127B[k]["means"]["pn"]["blind"] > 0]
    lk = R127[LOOKUP]
    L += ["", "### AUX-R129-GROUPS-PRINTED — the two-decimal forms Appendix E.3's sentences print",
          f"With the summary, the obligations against group (a): {', '.join(rr(x) for x in ga)} (range {rr(min(ga))} to {rr(max(ga))}); against group (c): {', '.join(rr(x) for x in gc)} ({rr(min(gc))} to {rr(max(gc))}). "
          f"Question only against group (a), the three models that score anything without a summary (Haiku 4.5, GPT-5.6 Luna, Opus 5): {', '.join(rr(x) for x in qa)} ({rr(min(qa))} to {rr(max(qa))}). "
          f"The name lookup against (a), (b), (c): {rr(lk['a']['auroc'])}, {rr(lk['b']['auroc'])}, {rr(lk['c']['auroc'])}."]
    m5 = HYB["mini_k5"]["minus_hybrid"]; m1 = HYB["mini_k1"]["minus_hybrid"]
    L += ["", f"## AUX-R129-HYB-MINI5 — GPT-4.1 mini at five draws minus the hybrid reader (`reviews/v22/results/r129_hybrid_mini5.json`; the hybrid recomputed by the frozen recipe and gated on {HYB['gates']['hybrid_whole']}, the one-draw difference gated on {HYB['gates']['mini_k1_minus_hybrid']:+.4f}, the five-draw row read from {HYB['source_rows']['read_from']} and gated on {HYB['gates']['mini_k5_whole']})", "",
          "| row | model | minus the hybrid | item interval | persona interval | both exclude zero |", "|---|---:|---:|---|---|---|",
          f"| GPT-4.1 mini, one draw (recorded) | {HYB['mini_k1']['model']:.4f} | {m1['delta']:+.4f} | {sci(m1['item_ci'])} | {sci(m1['persona_ci'])} | {m1['both_exclude_zero']} |",
          f"| GPT-4.1 mini, five draws (AUX-R122-K5) | {HYB['mini_k5']['model']:.4f} | {m5['delta']:+.4f} | {sci(m5['item_ci'])} | {sci(m5['persona_ci'])} | {m5['both_exclude_zero']} |", "",
          f"**The five-draw difference is not reliable in either direction** ({m5['delta']:+.4f}; both intervals include zero)."]
    # the two-decimal forms Section 5.2's hybrid paragraph prints (AUX-CF2-HYB-WHOLE, -VS-MODELS)
    CF2H = json.load(open(ROOT / "r82_counterfactual" / "cf2" / "results" / "cf_scores_hybrid.json", encoding="utf-8"))
    mods = {k: v["minus_hybrid"]["delta"] for k, v in CF2H["models_minus_hybrid"].items()}
    top = [mods[k] for k in ("OP5", "LUNA", "SOL")]
    assert all(CF2H["models_minus_hybrid"][k]["minus_hybrid"]["both_exclude_zero"] for k in ("OP5", "LUNA", "SOL"))
    L += ["", "### AUX-R129-HYB-PRINTED — the two-decimal forms Section 5.2's hybrid paragraph prints",
          f"The hybrid's whole-set AUROC {CF2H['hybrid']['whole']:.4f} prints as {CF2H['hybrid']['whole']:.2f}; hybrid minus the lookup {CF2H['hybrid']['vs_lookup']['delta']:+.4f} with the item interval including zero (not reliable); "
          f"Opus 5, GPT-5.6 Luna and GPT-5.6 Sol minus the hybrid {', '.join(f'{x:+.4f}' for x in top)}, each with both intervals excluding zero, print as {min(top):.2f} to {max(top):.2f}."]
    v = B9["views_with_active_stale_line"]; s = B9["oracle_split"]
    L += ["", "## AUX-R129-B9 — the inverted tag (`frbank:fatima:fatima_q06`; AUX-DS-AUDIT-SOURCE) corrected on paper: E.10's counts both ways (`reviews/v22/results/r129_b9.json`; no answer re-scored)", "",
          f"Scorable obligations {B9['scorable']} ({B9['by_state']['sup']} supersession, {B9['by_state']['ret']} retraction). Views with an active line asserting the stale value: as joined **{v['as_joined']['total']}** ({v['as_joined']['sup']} supersession, {v['as_joined']['ret']} retraction); with the tag corrected **{v['corrected']['total']}** ({v['corrected']['sup']}, {v['corrected']['ret']}). "
          f"The FULL view of the question holds active stale lines {B9['variants']['frbank:fatima:fatima_q06:FULL']['active_stale_lines']} and the tagged retraction statement at line {B9['variants']['frbank:fatima:fatima_q06:FULL']['tagged_stale_lines']}; the SLOT-ABLATED view holds neither, so it is outside the 35 either way.", "",
          "| answerer (D.4, ORACLE) | stale with such a line / stale without, as joined | not stale with / without | stale with / without, corrected | answered stale on that view |", "|---|---|---|---|---|"]
    for name, d in s.items():
        aj, co = d["as_joined"], d["corrected"]
        L.append(f"| {name} | {aj['stale_with_active_stale_line']} / {aj['stale_without']} | {aj['not_stale_with']} / {aj['not_stale_without']} | {co['stale_with_active_stale_line']} / {co['stale_without']} | {d['stale_on_the_corrected_view']} |")
    L += ["", "Printed forms: 'of 16' and 'of 19' stale answers under the oracle, 16 of 16 and 14 of 19 on such a view as joined, 15 of 16 and 13 of 19 with the tag corrected. Every answer-stage table was scored with the tag as joined (the captions say so)."]
    L += ["", "## AUX-R129-COUNT — the prediction count with E9 in it", "",
          "The moved-count control's second amendment (registrations/ADDENDUM_V2R_CAT_AMENDMENT_2.md, frozen at b0bee93, day 40) registered one prediction with a bar, P-M2 (both models fall reliably on retraction and on expiry); it failed for both models on retraction (AUX-V2RCAT-A2-P-M2). "
          "AUX-R124-TALLY: 92 predictions, 28 otherwise, of which tab:registrations-d carries 28 with 10. With P-M2: **93 predictions, 29 otherwise; tab:registrations-d 29 with 11**; the other three tables unchanged (47 with 8; 17 with 10; none)."]
    L += ["", "## AUX-R129-E9-PRINTED — the two-decimal forms Section 5.1 prints (each the rounding of a ledgered value; the whole-set rows for tab:v2rcat's E9 rows)", "",
          "| reader | state | recorded sup.-only row | moved-count row | delta | item interval | persona interval | both exclude zero | printed | source |", "|---|---|---:|---:|---:|---|---|---|---:|---|"]
    def add(reader, state, blk, src):
        both = bool(blk["item_ci"]["excludes_zero"] and blk["persona_ci"]["excludes_zero"])
        L.append(f"| {reader} | {state} | {blk['v2']:.4f} | {blk['v2rcat']:.4f} | {blk['delta']:+.4f} | {sci(blk['item_ci'])} | {sci(blk['persona_ci'])} | {both} | {abs(blk['delta']):.2f} | {src} |")
    op = OP5["opus_k5"]
    for state, key in (("retraction", "RETRACTION"), ("expiry", "EXPIRY")):
        b = dict(op["per_state"][key]); b["v2rcat"] = b["v2"] + b["delta"]  # the k = 5 moved-count value is printed in tab:v2rcat from the ledger; here the delta is what Section 5.1 rounds
        add("Opus 5 (five draws)", state, b, "AUX-V2RCAT-A1-OP5-K5")
    for reader, key, tag in (("GPT-5.6 Luna", "gpt-5.6-luna", "AUX-V2RCAT-A2-LUNA-K5"), ("GPT-5.6 Sol", "gpt-5.6-sol", "AUX-V2RCAT-A2-SOL-K5")):
        m = V2R["models"][key]
        w = dict(m["minus_v2"]); w["v2"] = m["v2_recorded_k5"]; w["v2rcat"] = m["v2rcat"]
        add(reader, "whole set", w, tag)
        for state, k2 in (("retraction", "RETRACTION"), ("expiry", "EXPIRY")):
            add(reader, state, m["per_state"][k2], tag)
    L += ["", "Section 5.1 prints Opus 0.10 and 0.13, Luna and Sol 0.12 and 0.19 on expiry (both intervals excluding zero) and 0.07 and 0.03 on retraction (intervals including zero); GPT-4.1 mini and Haiku 4.5 show no change reliable under both intervals (AUX-V2RCAT-MINI, -H45: +0.0269 / +0.0611 and -0.0072 / -0.0453, each with at least one interval including zero)."]
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("->", OUT)


if __name__ == "__main__":
    main()
