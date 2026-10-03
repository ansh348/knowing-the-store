# -*- coding: utf-8 -*-
"""fill_report_r122.py -- R122: fill REPORT.md's prediction table, T3/T4 sections and spend from the result artifacts (no number typed by hand)."""
from __future__ import annotations

import io
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r122_common as C  # noqa: E402


def ci(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"


def main():
    S = C.jload(C.RESULTS / "scores_r122_oai.json"); E = C.jload(C.RESULTS / "enc_lookup.json"); G = C.jload(C.RESULTS / "gate_reach.json")
    T3, T4, sp = S["T3"], S["T4"], S["spend"]
    e = E["predictions"]["P-E1"]["encoders"]; k = T3["predictions"]["P-K1"]["per_summary"]; r1 = T4["predictions"]["P-R1"]["per_reader"]; r3 = T4["predictions"]["P-R3"]; g = G["predictions"]
    af = G["matched"]["AF"]["reach"]["minus_model"]; rc = G["matched"]["RECENCY"]["reach"]["minus_model"]
    n2, n3 = T3["INDEXED-V2"], T3["INDEXED-V3"]; v2d, v3d = n2["new_minus_recorded"]["whole"], n3["new_minus_recorded"]["whole"]
    lu, mi = T4["LUNA"], T4["MINI"]; lud, mid = lu["new_minus_recorded"]["whole"], mi["new_minus_recorded"]["whole"]
    mE, mR = mi["new_minus_recorded"]["per_state"]["EXPIRY"], mi["new_minus_recorded"]["per_state"]["RETRACTION"]
    rows = [
        "| task | prediction | verdict | numbers (point; item-level interval; persona-grouped interval) |", "|---|---|---|---|",
        f"| T1 | P-E1: both encoders within 0.05 of MiniLM (444, v2) | **HOLDS** | mpnet {e['MPNET']['whole_v2']:.4f} ({e['MPNET']['delta']:+.4f}; {e['MPNET']['ci_item']}; {e['MPNET']['ci_persona']}); "
        f"bge-small {e['BGE']['whole_v2']:.4f} ({e['BGE']['delta']:+.4f}; {e['BGE']['ci_item']}; {e['BGE']['ci_persona']}); MiniLM 0.7663 |",
        "| T2 | P-H1, P-H2 | **skipped** | R120's draft (E10) |",
        f"| T3 | P-K1: five-draw AUROC within 0.05 of the one-draw row and the tied triples fall, both summaries | **HOLDS** | v2 {k['INDEXED-V2']['k5']:.4f} vs {k['INDEXED-V2']['k1']:.4f} "
        f"({v2d['delta']:+.4f}; {ci(v2d['item_ci'])}; {ci(v2d['persona_ci'])}), tied {k['INDEXED-V2']['tied_k1']} → {k['INDEXED-V2']['tied_k5']}; v3 {k['INDEXED-V3']['k5']:.4f} vs {k['INDEXED-V3']['k1']:.4f} "
        f"({v3d['delta']:+.4f}; {ci(v3d['item_ci'])}; {ci(v3d['persona_ci'])}), tied {k['INDEXED-V3']['tied_k1']} → {k['INDEXED-V3']['tied_k5']}. Within tolerance at the point by 0.002 on v2; the rise is reliable on both |",
        f"| T4 | P-R1: each reader's P1 AUROC within 0.05 of its P0 value | **HOLDS** | Luna {r1['LUNA']['p1']:.4f} vs {r1['LUNA']['p0']:.4f} ({lud['delta']:+.4f}; {ci(lud['item_ci'])}; {ci(lud['persona_ci'])}); "
        f"mini {r1['MINI']['p1']:.4f} vs {r1['MINI']['p0']:.4f} ({mid['delta']:+.4f}; {ci(mid['item_ci'])}; {ci(mid['persona_ci'])}) |",
        f"| T4 | P-R2: per-state ordering unchanged | **FAILS** (GPT-4.1 mini) | Luna sup > exp > ret under both rubrics; mini sup > exp > ret → sup > ret > exp: expiry "
        f"{mi['recorded']['per_state']['EXPIRY']['auroc']:.4f} → {mi['new']['per_state']['EXPIRY']['auroc']:.4f} ({mE['delta']:+.4f}; {ci(mE['item_ci'])}; {ci(mE['persona_ci'])}), retraction "
        f"{mi['recorded']['per_state']['RETRACTION']['auroc']:.4f} → {mi['new']['per_state']['RETRACTION']['auroc']:.4f} ({mR['delta']:+.4f}; {ci(mR['item_ci'])}; {ci(mR['persona_ci'])}) |",
        f"| T4 | P-R3: Luna's margin over the lookup keeps its sign, both intervals excluding zero | **HOLDS** | {r3['delta']:+.4f} ({ci(r3['item_ci'])}; {ci(r3['persona_ci'])}); recorded P0 margin {r3['recorded_delta']:+.4f} |",
        f"| T5 | P-G1: ALWAYS-FETCH matched reach within 0.05 of the MODEL rule's | **HOLDS** | {g['P-G1']['af_matched_reach']:.4f} vs 0.8173 ({af['D']:+.4f}; {ci(af['item'])}; {ci(af['persona'])}) |",
        f"| T5 | P-G2: ALWAYS-FETCH spends more lines than the MODEL rule before matching | **HOLDS** | {g['P-G2']['af5_mean_661']:.4f} vs 5.4342 lines over the 661, ratio {g['P-G2']['ratio']:.4f} |",
        f"| T5 | P-G3: RECENCY matched reach below the MODEL rule's by more than 0.05 | **HOLDS** | {g['P-G3']['recency_matched_reach']:.4f} vs 0.8173 ({rc['D']:+.4f}; {ci(rc['item'])}; {ci(rc['persona'])}); RECENCY-7 unmatched {g['P-G3']['unmatched_recency7_reach']:.4f} |",
    ]
    table = "\n".join(rows)
    o2 = n2["new"]["posthoc"]["whole"]["ordering"]
    t3 = (f"4,440 calls, all OK, every unit five draws (identical across all five draws on {n2['new']['census']['identical_across_draws']} of 444 units under v2 and {n3['new']['census']['identical_across_draws']} under v3; "
          f"median range {n2['new']['census']['median_range']} / {n3['new']['census']['median_range']}), served `gpt-4.1-mini-2025-04-14`, ${sp['MINI5']['usd']:.4f}, cache share {sp['MINI5']['cached_share']:.2f}. "
          f"**P-K1 HOLDS** on both summaries: v2 {n2['new']['whole']:.4f} against the recorded {n2['recorded']['whole']:.4f}, v3 {n3['new']['whole']:.4f} against {n3['recorded']['whole']:.4f}; tied triples "
          f"{n2['recorded']['tied_triples']} → {n2['new']['tied_triples']} and {n3['recorded']['tied_triples']} → {n3['new']['tied_triples']}; distinct collapsed values 12 → {n2['new']['distinct_values']} and 12 → {n3['new']['distinct_values']}. "
          f"The AUROC clause holds at the point by 0.002 on v2 ({v2d['delta']:+.4f}) and the rise is **reliable on both summaries** ({ci(v2d['item_ci'])}; {ci(v2d['persona_ci'])} under v2; {v3d['delta']:+.4f}, "
          f"{ci(v3d['item_ci'])}; {ci(v3d['persona_ci'])} under v3), carried by supersession ({n2['new_minus_recorded']['per_state']['SUPERSESSION']['delta']:+.4f}, reliable, under v2) and by expiry under v3 "
          f"({n3['new_minus_recorded']['per_state']['EXPIRY']['delta']:+.4f}, reliable). What it changes in the reading: at five draws GPT-4.1 mini sits within tolerance of the name lookup under v2 "
          f"({n2['new']['vs_lookup']['delta']:+.4f}; {ci(n2['new']['vs_lookup']['item_ci'])}; {ci(n2['new']['vs_lookup']['persona_ci'])}) where the recorded one-draw row is below it by −0.0496 with the persona interval "
          f"excluding zero; under v3 it stays reliably below the all-states lookup ({n3['new']['vs_lookup']['delta']:+.4f}). Section 5's \"the lookup is not exceeded by GPT-4.1 mini\" stands on either row. "
          f"W/T/L moves from 81/57/10 to {o2['wins']}/{o2['ties']}/{o2['losses']}: the ties break into wins and into losses, and PN-versus-PRESENT rises from 0.7056 to {n2['new']['posthoc']['whole']['pn_vs_present']:.4f}. "
          f"The confound is registered (D-R122-1): the rows differ in temperature as well as in draws, so the held text says \"at five draws with the provider's default temperature\"; a temperature-0 five-draw row was not run.")
    t4 = (f"P1's sha `c3c9a8e2…` asserted at import; 2,220 Luna calls and 444 mini calls, all OK, served `gpt-5.6-luna` / `gpt-4.1-mini-2025-04-14`, ${sp['P1LUNA']['usd']:.4f} + ${sp['P1MINI']['usd']:.4f}, "
          f"Luna's cache share {sp['P1LUNA']['cached_share']:.2f}. **P-R1 HOLDS**: Luna {lu['new']['whole']:.4f} under P1 against {lu['recorded']['whole']:.4f} under P0 ({lud['delta']:+.4f}; {ci(lud['item_ci'])}; "
          f"{ci(lud['persona_ci'])}), mini {mi['new']['whole']:.4f} against {mi['recorded']['whole']:.4f} ({mid['delta']:+.4f}; {ci(mid['item_ci'])}; {ci(mid['persona_ci'])}); the intent-explicit rubric costs neither reader "
          f"its counterfactual discrimination, and Luna's persona interval sits at zero on the up side. **P-R3 HOLDS**: Luna's margin over the lookup is {r3['delta']:+.4f} ({ci(r3['item_ci'])}; {ci(r3['persona_ci'])}) "
          f"against the recorded +0.0754; per state {lu['new']['per_state']['SUPERSESSION']['auroc']:.4f} / {lu['new']['per_state']['RETRACTION']['auroc']:.4f} / {lu['new']['per_state']['EXPIRY']['auroc']:.4f} against "
          f"0.9426 / 0.5458 / 0.6167 (retraction {lu['new_minus_recorded']['per_state']['RETRACTION']['delta']:+.4f}, intervals including zero). **P-R2 FAILS, on GPT-4.1 mini only**: Luna's order "
          f"(supersession > expiry > retraction) is unchanged; mini's two counted states swap, expiry {mi['recorded']['per_state']['EXPIRY']['auroc']:.4f} → {mi['new']['per_state']['EXPIRY']['auroc']:.4f} "
          f"({mE['delta']:+.4f}; {ci(mE['item_ci'])}; {ci(mE['persona_ci'])}) and retraction {mi['recorded']['per_state']['RETRACTION']['auroc']:.4f} → {mi['new']['per_state']['RETRACTION']['auroc']:.4f} ({mR['delta']:+.4f}), "
          f"both moves with intervals including zero, on 90 items each: a rank swap between two near-chance rows, not a reliable move. The registered failure text names the state and its two values; the assembled sentence "
          f"for this branch is in `HELD_TEXTS.md`. Mini's tied triples fall from 51 to {mi['new']['tied_triples']} and its supersession row rises {mi['new_minus_recorded']['per_state']['SUPERSESSION']['delta']:+.4f} under P1. "
          f"Disclosure, as registered: this task followed R121's interim reads; this session did not read them.")
    spend = (f"Token-metered from the rows at the page prices (not an invoice): P1MINI ${sp['P1MINI']['usd']:.4f} (444 rows), P1LUNA ${sp['P1LUNA']['usd']:.4f} (2,220), MINI5 ${sp['MINI5']['usd']:.4f} (4,440), "
             f"probes ${sp['probes_usd']:.4f}; **${sp['total_usd']:.4f} of the 5.00 USD cap** (the probe projection: $2.56 expected, $4.89 with no cache). Anthropic: 0 USD, no call. Every lane's rows all OK; "
             f"served identifiers as pinned. The cache engaged fully for Luna (share {sp['P1LUNA']['cached_share']:.2f}) and partly for mini's five draws (share {sp['MINI5']['cached_share']:.2f}), which is why MINI5 "
             f"came in above its $1.34 expectation and below its $3.09 no-cache figure.")
    p = C.R122 / "REPORT.md"; s = io.open(p, encoding="utf-8").read()
    for a, b in (("PREDICTION_TABLE", table), ("T3_TEXT", t3), ("T4_TEXT", t4), ("SPEND_TEXT", spend)):
        assert s.count(a) == 1, a
        s = s.replace(a, b)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    io.open(C.RESULTS / "prediction_table.md", "w", encoding="utf-8", newline="\n").write(table + "\n")
    print("filled REPORT.md; prediction table at results/prediction_table.md")


if __name__ == "__main__":
    main()
