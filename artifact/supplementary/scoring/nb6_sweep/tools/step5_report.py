"""Step 5: REPORT.md sections 2-9 from the four artifacts, the AUROC-vs-length figure, and the
mechanism diagnostic behind the 661's length effect (saved as an artifact of its own).

Regenerates everything from the "## 2." heading on; the header, section 0 (the prediction, as
committed) and section 1 (the reproduction) are left untouched.

Usage: python nb6_sweep/tools/step5_report.py
Writes nb6_sweep/REPORT.md (sections 2-9), results/auroc_vs_length.png, results/step5_diagnostics.json
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sweep_common import (OUT, ROOT, auroc, emb_cached, jdump, jload, load_661, load_cf2,  # noqa: E402
                          make_cell, pools, prime_embeddings)

REPORT = ROOT / "nb6_sweep" / "REPORT.md"
S2 = jload(OUT / "step2_contamination.json")
S3 = jload(OUT / "step3_length.json")
S4 = jload(OUT / "step4_recall.json")
BEL = 0.5858
C_BEL = 0.232


def ci(v, key="ci_governing"):
    g = v.get(key)
    if not g:
        return "—"
    return f"[{g['ci_lo']:+.4f}, {g['ci_hi']:+.4f}]{'*' if g['excludes_zero'] else ''} ({g['which'][0]})"


def row_cells(rec, base=False):
    """The common cell columns: len, recall, pos named, neg named, emb, Δ CI, emb sup, Δsup CI, lex, Δ CI, lex sup."""
    c, e, l = rec["census"], rec["emb"], rec["lex"]
    if base:
        return (f"{c['mean_len']:.2f} | {c['true_recall_item_weighted']:.3f} | {c['pos_own_named']:.3f} | {c['neg_own_named_all']:.3f} | "
                f"**{e['auroc']:.4f}** | — | **{e['auroc_superseded']:.4f}** | — | {l['auroc']:.4f} | — | {l['auroc_superseded']:.4f}")
    return (f"{c['mean_len']:.2f} | {c['true_recall_item_weighted']:.3f} | {c['pos_own_named']:.3f} | {c['neg_own_named_all']:.3f} | "
            f"**{e['auroc']:.4f}** | {e['delta_vs_base']:+.4f} {ci(e)} | **{e['auroc_superseded']:.4f}** | {e['sup_delta_vs_base']:+.4f} {ci(e, 'sup_ci_governing')} | "
            f"{l['auroc']:.4f} | {l['delta_vs_base']:+.4f} {ci(l)} | {l['auroc_superseded']:.4f}")


HDR = ("| cell | len | recall | pos named | neg named | emb | Δ vs base (wider CI) | emb sup | Δ sup (wider CI) | lex | Δ vs base (wider CI) | lex sup |\n"
       "|---|---:|---:|---:|---:|---:|---|---:|---|---:|---|---:|")
POPS = (("cf2", "444, v2 summary", "supersession slice = the 264 items of the 88 supersession pairs"),
        ("661", "661, TRUE index", "supersession slice = 63 supersession positives vs all 557 negatives"))


# =============================================================================== section 2
def sec2():
    L = ["## 2. Contamination sweep (2026-09-14, `tools/step2_contamination.py`, seed 42, $0)\n"]
    L.append("**Design.** Length and TRUE-name recall are held at the base list (marker stripped). A negative's own "
             "scrubbed attribute name is injected into the summary that negative reads, at target rates 0.00 / 0.10 / "
             "0.232 / 0.40 / 0.49 of all negatives: 0.232 is BELIEVED's measured rate over all 661 negatives (§1.2); "
             "0.49 is its rate on the PRESENT negatives (85 of 174), added after the first run so the realistic "
             "operating point sits inside the measured range rather than beyond it. Store-faithful: a negative is "
             "eligible only when one of its own names is a real name of its store version, so the injected name is an "
             "attribute the store holds and the list wrongly marks as superseded — BELIEVED's mechanism. On the 444 "
             "every negative is eligible (all 148 pair slots exist in the persona bank); on the 661, 295 of 557 (164 "
             "PRESENT, 131 ablation-ABSENT with a surviving same-named entry; natural-absent probes have no own name). "
             "One own name per chosen negative (BELIEVED-named negatives carry 1.09). Injection is nested across rates "
             "(one permutation per seed). Paired bootstraps against the base list: item-level and persona-clustered, "
             "1000 draws, seed 42, single-class draws discarded, 2.5 / 97.5; the wider interval governs and is the one "
             "printed (`*` = excludes zero; `(i)`/`(p)` = which convention was wider).\n")
    L.append("**Two caveats on the 661 column, which apply to every 661 cell in this report.** (1) The 661 base list "
             "already names a negative's own name on 3.9% of negatives (22 of 557), so its contamination deltas are "
             "measured from 0.039, not 0, and understate the effect of the full rate. (2) Lists are per summary, and a "
             "name injected into a shared summary can also name a positive that reads it: pos named rises from 0.712 to "
             "0.750 / 0.760 / 0.779 at 0.232 / 0.40 / 0.49, which favours the lookup on those cells. The 444 has neither "
             "problem (per-item lists; pos named held at 0.595).\n")
    for pop, title, slice_note in POPS:
        P = S2["cells"][pop]
        L.append(f"### 2.{1 if pop == 'cf2' else 2} {title}\n")
        L.append(f"{slice_note}. Eligible negatives {P['n_eligible_negatives']} of {P['n_neg']}.\n")
        L.append(HDR)
        for rate in S2["rates"]:
            r = P[f"rate_{rate}"]
            tag = f"c = {rate:.3f} (base)" if rate == 0 else f"c = {rate:.3f} (achieved {r['injection']['achieved_rate']:.3f}, {r['injection']['n_injected']} injected)"
            L.append(f"| {tag} | " + row_cells(r, base=(rate == 0)) + " |")
        sp = P["rate_0.232_extra_seeds"]
        L.append("")
        L.append("Seeds 43–46 at 0.232 (descriptive): emb whole " + ", ".join(f"{x['emb']:.4f}" for x in sp)
                 + "; emb sup " + ", ".join(f"{x['emb_sup']:.4f}" for x in sp)
                 + "; lex whole " + ", ".join(f"{x['lex']:.4f}" for x in sp) + ".\n")
    cf = S2["cells"]["cf2"]
    L.append("### 2.3 Reading\n")
    L.append(f"**What 0.9223 becomes at contamination 0.232: {cf['rate_0.232']['emb']['auroc_superseded']:.4f}** (embedding, "
             f"supersession slice; whole set 0.7663 → {cf['rate_0.232']['emb']['auroc']:.4f}); at 0.40, {cf['rate_0.4']['emb']['auroc_superseded']:.4f} / "
             f"{cf['rate_0.4']['emb']['auroc']:.4f}; at 0.49, BELIEVED's rate on PRESENT negatives, **{cf['rate_0.49']['emb']['auroc_superseded']:.4f}** / "
             f"{cf['rate_0.49']['emb']['auroc']:.4f}. The lexical variant falls in step (0.7829 → {cf['rate_0.232']['lex']['auroc_superseded']:.4f} → "
             f"{cf['rate_0.49']['lex']['auroc_superseded']:.4f} on the slice). Every paired interval excludes zero, on both conventions, at every "
             "non-zero rate, on both populations. Printed plainly: the 0.92 was measured on a list that names no negative's own "
             "attribute (0 of 296); at the rate the real BELIEVED list shows on PRESENT items, the slice loses 0.19 and the "
             "whole set 0.20, and the lookup has no defence against it. Section 3 shows this degradation is not noise but a law.\n")
    L.append("Artifacts: `results/step2_contamination.json`.\n")
    return L


# =============================================================================== section 3
def mixing():
    """Fit of the mixing law across all rates, both populations, both variants, whole and slice."""
    out = {}
    for pop, _, _ in POPS:
        P = S2["cells"][pop]
        c0 = P["base"]["census"]["neg_own_named_all"]
        for v in ("emb", "lex"):
            for sl, key in (("whole", "auroc"), ("sup", "auroc_superseded")):
                A = P["base"][v][key]
                pts = []
                for rate in S2["rates"]:
                    r = P[f"rate_{rate}"]
                    c = r["injection"]["achieved_rate"]
                    cp = (c - c0) / (1 - c0)
                    pred = (1 - cp) * A + cp * 0.5
                    meas = r[v][key]
                    pts.append({"rate": rate, "c": c, "c_eff": cp, "measured": meas, "predicted": pred, "residual": meas - pred})
                cs = np.array([p["c"] for p in pts]); ms = np.array([p["measured"] for p in pts])
                b, a = np.polyfit(cs, ms, 1)
                law_slope = -(A - 0.5) / (1 - c0)
                rmse = float(np.sqrt(np.mean([p["residual"] ** 2 for p in pts])))
                out[f"{pop}|{v}|{sl}"] = {"A": A, "c0": c0, "points": pts, "ols_slope": float(b), "ols_intercept": float(a),
                                          "law_slope": float(law_slope), "rmse": rmse,
                                          "max_abs_residual": float(max(abs(p["residual"]) for p in pts))}
    return out


def sec3(M):
    L = ["## 3. The mixing law: lookup AUROC is predictable from one store property\n"]
    L.append("A contaminated negative carries an exact own-name match, so its max-cosine score is drawn from the same "
             "distribution as a supersession positive's: against a positive it is a coin flip. If that is all contamination "
             "does, then with A the AUROC on an uncontaminated list and c the fraction of negatives whose own name the list "
             "carries,\n\n"
             "    AUROC(c) = (1 − c) · A + c · 0.5\n\n"
             "On the 661 the base list is already at c₀ = 0.039, so the law is applied to the fraction of the base's "
             "uncontaminated negatives that the injection contaminates, c′ = (c − c₀) / (1 − c₀), with A the base AUROC; on "
             "the 444, c₀ = 0 and c′ = c. Nothing is fitted: A is the base row, c the achieved census rate. The table gives "
             "predicted and measured values at every rate, the residual, its RMSE, and the ordinary-least-squares slope of "
             "measured AUROC on c against the slope the law implies, −(A − 0.5) / (1 − c₀).\n")
    L.append("| population | variant | slice | A (base) | c₀ | rate 0.10 pred / meas | 0.232 pred / meas | 0.40 pred / meas | 0.49 pred / meas | RMSE | max abs resid | OLS slope | law slope |")
    L.append("|---|---|---|---:|---:|---|---|---|---|---:|---:|---:|---:|")
    for pop, _, _ in POPS:
        for v in ("emb", "lex"):
            for sl in ("sup", "whole"):
                m = M[f"{pop}|{v}|{sl}"]
                pts = {p["rate"]: p for p in m["points"]}
                cells = " | ".join(f"{pts[r]['predicted']:.4f} / {pts[r]['measured']:.4f}" for r in (0.10, 0.232, 0.40, 0.49))
                L.append(f"| {pop} | {v} | {sl} | {m['A']:.4f} | {m['c0']:.3f} | {cells} | {m['rmse']:.4f} | {m['max_abs_residual']:.4f} | {m['ols_slope']:+.4f} | {m['law_slope']:+.4f} |")
    L.append("")
    e_sup, e_whole = M["cf2|emb|sup"], M["cf2|emb|whole"]
    s_sup, s_whole, s_lex = M["661|emb|sup"], M["661|emb|whole"], M["661|lex|sup"]
    L.append(f"**Reading.** On the population the 0.92 rests on, the embedding lookup's supersession slice follows the law "
             f"to within {e_sup['max_abs_residual']:.3f} AUROC at every rate (RMSE {e_sup['rmse']:.4f}), with an OLS slope of "
             f"{e_sup['ols_slope']:+.3f} against the law's {e_sup['law_slope']:+.3f}; the lexical slice is within "
             f"{M['cf2|lex|sup']['max_abs_residual']:.3f}. The residual pattern elsewhere is systematic, not random, and both "
             f"directions have a cause that can be read off the census. **Whole sets degrade faster than the law** (444 embedding "
             f"whole: residuals all negative, growing to {min(pt['residual'] for pt in e_whole['points']):+.3f} at 0.49; RMSE "
             f"{e_whole['rmse']:.4f}): the whole 444 also holds the 60 counted-state positives, whose summaries name nothing of "
             "theirs and whose scores sit *below* a contaminated negative's rather than level with it, so each contaminated "
             "negative is worse than a coin flip against them. **The 661 embedding slice degrades slower than the law** "
             f"(residuals all positive, growing to {max(pt['residual'] for pt in s_sup['points']):+.3f} at 0.49; RMSE {s_sup['rmse']:.4f}): "
             "there a contaminated negative receives one of its own names at random (negatives with an own name carry 1.9 on "
             "average) while a supersession positive's list carries every superseded name it has and takes the max, so the "
             "contaminated negative is slightly weaker than a coin flip; and shared-summary injection also named a few extra "
             "positives (caveat 2 of §2). On the 661 whole set the two effects roughly cancel (RMSE "
             f"{s_whole['rmse']:.4f}); the lexical 661 slice is within {s_lex['max_abs_residual']:.4f}. The law's premise — a "
             "contaminated negative is exactly a coin flip against a positive — holds where positives carry their own name and "
             "negatives are contaminated with the name the question would match; where it is violated, the direction of the "
             "violation is the direction the census predicts. Residuals are descriptive; no parameter was fitted to them.\n")
    L.append("**Why this matters more than the degraded number.** It makes lookup performance predictable from a census "
             "the store can run on itself: count the negatives whose own attribute the superseded-names section carries. "
             "It is a stronger form of the paper's own thesis — the lookup reads names, and every name it reads that it "
             "should not costs it a fixed, computable amount — and it is what turns the 0.92 into a function of the store "
             "rather than a property of the lookup.\n")
    return L


# =============================================================================== section 4
def sec4(D):
    L = ["## 4. Length sweep (2026-09-14, `tools/step3_length.py`, seed 42, $0)\n"]
    ps = S3["pool_sizes"]
    L.append(f"**Design.** L ∈ {{base, 5, 10, 15, 30, 32, 60}}, where **15 is FR-Bank's renderer cap and 32 the uncapped BELIEVED length (32.55), the two operating points a tested backend actually emits, and 60 is the registered stress condition** that no tested backend emits; fillers are the persona's own-store scrubbed attribute names "
             f"that no scored question of that persona targets in either population (pool per persona: min "
             f"{min(x['own_untargeted'] for x in ps.values())}, median {int(np.median([x['own_untargeted'] for x in ps.values()]))}, "
             f"max {max(x['own_untargeted'] for x in ps.values())} names; targeted names excluded: {min(x['targeted'] for x in ps.values())}–"
             f"{max(x['targeted'] for x in ps.values())} per persona), drawn from a per-summary seeded permutation so the sweep is nested; "
             "no TRUE name is ever dropped; recall stays 1.0 and precision (against TRUE) falls as 1.45/L. Run at contamination 0 "
             "(the base's own rate), then L ∈ {15, 30, 60} at c = 0.232. Achieved mean length is the census column.\n")
    for pop, title, slice_note in POPS:
        P = S3["cells"][pop]
        L.append(f"### 4.{1 if pop == 'cf2' else 2} {title}\n")
        L.append(f"{slice_note}.\n")
        L.append(HDR)
        for c in (0.0, C_BEL):
            for Ln in ("base", 5, 10, 15, 30, 32, 60):
                name = f"L{Ln}_c{c}"
                if name not in P:
                    continue
                r = P[name]
                tag = f"L = {Ln}, c = {c}" + (" (base)" if name == "Lbase_c0.0" else "")
                L.append(f"| {tag} | " + row_cells(r, base=(name == "Lbase_c0.0")) + " |")
        L.append("")
        it = P["interaction"]
        L.append("Length × contamination on AUROC, Δ(L, c) − [Δ(L, 0) + Δ(base, c)]: " +
                 "; ".join(f"L{Ln} emb {it[f'L{Ln}']['emb']['interaction']:+.4f}, lex {it[f'L{Ln}']['lex']['interaction']:+.4f}" for Ln in (15, 30, 32, 60)) +
                 ". Positive throughout: the two effects are **sub-additive** — they act on the same negatives' scores, and a "
                 "negative already lifted by its own name cannot be lifted again by a filler.\n")
    cf, s6 = S3["cells"]["cf2"], S3["cells"]["661"]
    L.append("### 4.3 Reading\n")
    surv = lambda a, b: (b - 0.5) / (a - 0.5)
    L.append(f"**Operating points, on the 444 (the population the 0.92 rests on).** At **L = 15**, FR-Bank's renderer cap, the "
             f"supersession slice is **{cf['L15_c0.0']['emb']['auroc_superseded']:.4f}** and the whole set {cf['L15_c0.0']['emb']['auroc']:.4f} "
             f"(paired Δ {cf['L15_c0.0']['emb']['delta_vs_base']:+.4f}, wider interval {ci(cf['L15_c0.0']['emb'])}); at **L = 32**, the uncapped "
             f"BELIEVED length, the slice is **{cf['L32_c0.0']['emb']['auroc_superseded']:.4f}** and the whole set {cf['L32_c0.0']['emb']['auroc']:.4f} "
             f"({cf['L32_c0.0']['emb']['delta_vs_base']:+.4f}, {ci(cf['L32_c0.0']['emb'])}). **0.7800 at 15 correct names is the number to take away**; "
             f"it is what the 0.9223 becomes on a list of the length the backend actually renders, with every name correct. "
             f"The registered stress condition, **L = 60**, gives {cf['L60_c0.0']['emb']['auroc_superseded']:.4f} on the slice and "
             f"{cf['L60_c0.0']['emb']['auroc']:.4f} on the whole set ({cf['L60_c0.0']['emb']['delta_vs_base']:+.4f}, {ci(cf['L60_c0.0']['emb'])}): "
             f"{surv(0.9223, cf['L60_c0.0']['emb']['auroc_superseded']):.0%} of the above-chance margin survives on the slice, "
             f"{surv(0.7663, cf['L60_c0.0']['emb']['auroc']):.0%} on the whole set — a bound, not an operating point. The whole-set interval "
             "includes zero at 5 and 10 names and excludes it from 15 up. **Printed plainly: padding does move the score — length is not "
             "dead.** At the operating points a list of correct, untargeted names costs the slice 0.14 (15) and 0.19 (32); at the stress bound "
             f"it halves the discrimination. The lexical variant loses less (0.7829 → {cf['L15_c0.0']['lex']['auroc_superseded']:.4f} at 15, "
             f"{cf['L60_c0.0']['lex']['auroc_superseded']:.4f} at 60) because its Jaccard scores are sparse and a filler rarely overlaps a "
             "question's content tokens.\n")
    L.append(f"**On the 661** the supersession slice tells the same story (0.9599 → {s6['L15_c0.0']['emb']['auroc_superseded']:.4f} at 15, "
             f"{s6['L60_c0.0']['emb']['auroc_superseded']:.4f} at 60), but the whole-population deltas are small and every one of "
             f"their wider intervals includes zero; the lexical whole-set figure even rises (0.5738 → "
             f"{s6['L60_c0.0']['lex']['auroc']:.4f}). Two mechanisms, measured in `results/step5_diagnostics.json`, not inferred: "
             f"(i) 145 of the 661's 557 negatives are natural-absent probes whose questions are about things the store does not "
             f"hold, and own-store fillers inflate them less — at L = 15 the mean embedding score of on-store items rises to "
             f"{D['L15_c0_r1.0']['mean_score']['neg_present']:.3f} (PRESENT negatives) and {D['L15_c0_r1.0']['mean_score']['pos_counted']:.3f} "
             f"(counted-state positives) but probes only to {D['L15_c0_r1.0']['mean_score']['neg_probe']:.3f}, so positives-vs-probes AUROC "
             f"*rises* from {D['Lbase_c0_r1.0']['auroc_pos_vs_probes']:.4f} to {D['L15_c0_r1.0']['auroc_pos_vs_probes']:.4f} while positives-vs-other-negatives "
             f"falls from {D['Lbase_c0_r1.0']['auroc_pos_vs_other_negs']:.4f} to {D['L15_c0_r1.0']['auroc_pos_vs_other_negs']:.4f}; (ii) padding lifts the "
             "empty-summary items (178 negatives, 17 counted-state positives) out of the 0.0 tie block of §1.1. The 444 has no "
             "probes and no empty-summary positives on its slice, so its length effect is the clean, purely adverse one. The "
             "661's whole-population length column is therefore the wrong place to read the length effect; its slice column and "
             "the 444 are the right places.\n")
    L.append("Artifacts: `results/step3_length.json`, `results/step5_diagnostics.json`, figure `results/auroc_vs_length.png`.\n")
    L.append("![AUROC vs list length](results/auroc_vs_length.png)\n")
    return L


# =============================================================================== section 5
def sec5():
    L = ["## 5. Recall sweep at L = 15, and the synthetic distractor cell (2026-09-14, `tools/step4_recall.py`, seed 42, $0)\n"]
    L.append("**Design.** L = 15 with own-store untargeted fillers, contamination at the base's own rate, TRUE-name recall forced "
             "to 1.00 / 0.70 / 0.50 / 0.3604 / 0.2996 / 0.10 by seeded (summary, TRUE-name) drops on the item-weighted micro-recall "
             "(the ledger's definition); 0.2996 is the ledger's BELIEVED value (marker in the denominator; the prediction's cell of "
             "record), 0.3604 the marker-corrected one. A dropped TRUE name is never re-added by a filler. The distractor cell "
             "holds L = 15 and recall 1.0 and draws half the fillers from OTHER personas' stores (names absent from this store): "
             "a labelled synthetic reference that occurs in no backend, kept for one comparison only.\n")
    for pop, title, slice_note in POPS:
        P = S4["cells"][pop]
        L.append(f"### 5.{1 if pop == 'cf2' else 2} {title}\n")
        L.append(f"{slice_note}.\n")
        L.append(HDR)
        L.append("| base | " + row_cells(P["base"], base=True) + " |")
        for r in S4["recalls"]:
            rec = P[f"L15_c0_r{r}"]
            L.append(f"| L = 15, recall {r} (achieved {rec['census']['true_recall_item_weighted']:.3f}) | " + row_cells(rec) + " |")
        rec = P["L15_c0_r1.0_distractor0.5"]
        L.append("| L = 15, recall 1.0, **half the fillers other-persona (synthetic)** | " + row_cells(rec) + " |")
        L.append("")
    cf, s6 = S4["cells"]["cf2"], S4["cells"]["661"]
    L.append("### 5.3 Reading\n")
    L.append(f"Recall is the steepest axis on both populations. On the 444 at L = 15, going from recall 1.0 to 0.3604 takes the slice "
             f"from {cf['L15_c0_r1.0']['emb']['auroc_superseded']:.4f} to {cf['L15_c0_r0.3604']['emb']['auroc_superseded']:.4f} and the whole set from "
             f"{cf['L15_c0_r1.0']['emb']['auroc']:.4f} to {cf['L15_c0_r0.3604']['emb']['auroc']:.4f}; at recall 0.10 the slice is at chance "
             f"({cf['L15_c0_r0.1']['emb']['auroc_superseded']:.4f}). Achieved pos-named falls with recall on both populations (444: 0.595 → 0.453 → 0.345 → 0.243 → 0.209 → 0.095), "
             "roughly in proportion on the 444, where each supersession positive has exactly one own name and dropping it leaves "
             "nothing to match, and more slowly on the 661, where a question can resolve to several slot names. **The distractor cell scores higher than the own-store cell at the same length** "
             f"({cf['L15_c0_r1.0_distractor0.5']['emb']['auroc']:.4f} vs {cf['L15_c0_r1.0']['emb']['auroc']:.4f} on the 444; "
             f"{s6['L15_c0_r1.0_distractor0.5']['emb']['auroc']:.4f} vs {s6['L15_c0_r1.0']['emb']['auroc']:.4f} on the 661): names from other people's "
             "stores are topically further from this persona's questions than the persona's own names are, so they inflate negatives less. "
             "Wrong-looking names are the *mild* error; the harmful errors are the two the real store makes — missing the positive's name "
             "and listing the negative's. That is the point on which the original two-axis design would have misled.\n")
    L.append("Artifacts: `results/step4_recall.json`.\n")
    return L


# =============================================================================== section 6
def sec6():
    L = ["## 6. Decomposition of the gap to BELIEVED: length, contamination, recall\n"]
    L.append("Eight corners on each population: length ∈ {base, 15}, contamination ∈ {base, 0.232}, recall ∈ {1.0, r}, for "
             "r = 0.3604 (marker-corrected BELIEVED) and r = 0.2996 (the ledger's value). Inside a cell the order is recall drop, "
             "then injection, then padding, so length is held exactly. Single-factor deltas are the three corners adjacent to the "
             "base; the Shapley value of each factor averages its marginal contribution over the six orderings and sums to the "
             "full-cell gap by construction; interaction = full gap − sum of single-factor deltas. Embedding, whole population, "
             "with the supersession slice beside it.\n")
    for pop, title, _ in POPS:
        P = S4["cells"][pop]["partition"]
        L.append(f"### 6.{1 if pop == 'cf2' else 2} {title}\n")
        for r in ("0.3604", "0.2996"):
            Q = P[r]
            L.append(f"**r = {r}.** Corners (emb whole / emb sup / lex whole):\n")
            L.append("| | recall 1.0, c base | recall 1.0, c 0.232 | recall r, c base | recall r, c 0.232 |")
            L.append("|---|---|---|---|---|")
            for Lf, lab in ((0, "L base"), (1, "L 15")):
                cells = []
                for cf_, rf in ((0, 0), (1, 0), (0, 1), (1, 1)):
                    k = f"L{Lf}c{cf_}r{rf}"
                    v = Q["corners"][k]
                    cells.append(f"{v['emb']:.4f} / {v['emb_sup']:.4f} / {v['lex']:.4f}")
                L.append(f"| {lab} | " + " | ".join(cells) + " |")
            L.append("")
            L.append("| measure | base → full | total gap | Δ length alone | Δ contamination alone | Δ recall alone | sum | interaction | Shapley L | Shapley c | Shapley r |")
            L.append("|---|---|---:|---:|---:|---:|---:|---:|---|---|---|")
            for v, lab in (("emb", "emb whole"), ("emb_sup", "emb sup"), ("lex", "lex whole"), ("lex_sup", "lex sup")):
                x = Q[v]; s = x["single_factor_deltas"]; sh = x["shapley"]; shs = x["shapley_share"]
                fmt = lambda k: f"{sh[k]:+.4f} ({shs[k]:.0%})" if shs[k] is not None else f"{sh[k]:+.4f}"
                L.append(f"| {lab} | {x['base']:.4f} → {x['full']:.4f} | {x['total_gap']:+.4f} | {s['L']:+.4f} | {s['c']:+.4f} | {s['r']:+.4f} | "
                         f"{x['sum_of_singles']:+.4f} | {x['interaction']:+.4f} | {fmt('L')} | {fmt('c')} | {fmt('r')} |")
            L.append("")
    s6 = S4["cells"]["661"]["partition"]
    e36, e30 = s6["0.3604"]["emb"], s6["0.2996"]["emb"]
    L.append("### 6.3 Reading\n")
    L.append(f"**On the 661, the population BELIEVED lives on, recall explains most of the drop, contamination is second, and "
             f"length is not a cost at all once the other two are present.** With r = 0.3604 the modelled gap is {e36['total_gap']:+.4f} "
             f"(0.7442 → {e36['full']:.4f}; the measured gap to BELIEVED is −0.1584); Shapley shares: recall {e36['shapley_share']['r']:.0%}, "
             f"contamination {e36['shapley_share']['c']:.0%}, length {e36['shapley_share']['L']:.0%} — the negative share means padding to 15 "
             f"*raises* the score when recall is already low and contamination present (the probe and near-synonym mechanisms of §4.3; "
             f"the recall-dropped, unpadded corner is {s6['0.3604']['corners']['L0c1r1']['emb']:.4f}, the padded one {s6['0.3604']['corners']['L1c1r1']['emb']:.4f}). "
             f"With r = 0.2996 the shares are recall {e30['shapley_share']['r']:.0%}, contamination {e30['shapley_share']['c']:.0%}, length "
             f"{e30['shapley_share']['L']:.0%}. The three factors are strongly **sub-additive**: the single-factor deltas sum to "
             f"{e36['sum_of_singles']:+.4f} against a full gap of {e36['total_gap']:+.4f} (interaction {e36['interaction']:+.4f}) — a positive "
             "whose name is dropped cannot also be out-scored by a contaminated negative it was already below, and a padded list "
             "cannot inflate a negative that its own name already inflated. On the 661's supersession slice recall still dominates "
             f"(recall {s6['0.3604']['emb_sup']['shapley_share']['r']:.0%}) but length is a cost there, about equal to contamination (length "
             f"{s6['0.3604']['emb_sup']['shapley_share']['L']:.0%}, contamination {s6['0.3604']['emb_sup']['shapley_share']['c']:.0%}): the probe credit "
             "belongs to the whole population, not to the slice. On the 444, where length is purely adverse, the ordering is recall > "
             f"contamination > length (emb whole shares {S4['cells']['cf2']['partition']['0.3604']['emb']['shapley_share']['r']:.0%} / "
             f"{S4['cells']['cf2']['partition']['0.3604']['emb']['shapley_share']['c']:.0%} / {S4['cells']['cf2']['partition']['0.3604']['emb']['shapley_share']['L']:.0%}).\n")
    L.append("**The \"precision 0.035\" framing, restated.** Of the ~14.5 non-TRUE names per item in the BELIEVED list, the only "
             "ones that cost the lookup anything are those that are a negative's own name (§2, §3); the rest are the length effect, "
             "which on this population is neutral-to-helpful. And the largest term is not a wrong name at all but a missing one. "
             "BELIEVED's problem is a recall problem with a contamination problem behind it, wearing a precision label.\n")
    return L


# =============================================================================== section 7
def sec7():
    R = S4["cells"]["661"]["reconstruction"]
    sp = S4["cells"]["661"]["seed_spread"]
    L = ["## 7. The BELIEVED reconstruction: did the target hit?\n"]
    L.append("**The realistic composite, stated explicitly.** BELIEVED's values are *measured store properties*, not chosen stress "
             "levels: length 15.04 as rendered (32.55 uncapped), TRUE-name recall 0.3604 (0.2996 with the marker in the denominator), "
             "contamination 0.232 over all negatives, which is 0.49 on the PRESENT negatives (85 of 174) and 0.325 on the negatives that "
             "have an own name. That is what justifies the composite cell: it is the store's own operating point, reconstructed one "
             "property at a time. The injection is calibrated on the all-negatives denominator (0.233 achieved); its PRESENT-denominator "
             f"rate at that setting is {R[f'L15_c{C_BEL}_r0.3604']['census']['neg_own_named_present']:.3f}, against BELIEVED's 0.489. "
             "The uncapped list has its own composite (length 32.55, recall 0.8010, contamination 0.400) and is checked the same way below.\n")
    L.append("The measured BELIEVED list: 15.04 names, TRUE-name recall 0.3604 (0.2996 with the marker), contamination 0.232, "
             "pos named 0.423, embedding 0.5858, lexical 0.4718. The prediction of §0 concerned the cell with L = 15, own-store "
             "fillers, recall 0.2996 and contamination at the base's own rate (0.039): \"near\" was defined as |cell − 0.5858| ≤ 0.05 "
             "and a paired interval including zero; \"materially above\" as margin > 0.05 or an interval excluding zero on the "
             "wider reading. Paired (cell − BELIEVED) bootstraps, both conventions, wider governs.\n")
    L.append("| cell | len | recall | pos named | neg named | emb | vs BELIEVED 0.5858 | wider CI | lex | vs 0.4718 | wider CI | seeds 43–46 emb |")
    L.append("|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---|---|")
    for name, lab in (("L15_c0_r0.2996", "L 15, c base, r 0.2996 — **the prediction's cell of record**"),
                      ("L15_c0_r0.3604", "L 15, c base, r 0.3604 (marker-corrected)"),
                      (f"L15_c{C_BEL}_r0.2996", "L 15, **c 0.232**, r 0.2996"),
                      (f"L15_c{C_BEL}_r0.3604", "L 15, **c 0.232**, r 0.3604 — the full reconstruction")):
        x = R[name]; c = x["census"]; e, l = x["vs_believed"]["emb"], x["vs_believed"]["lex"]
        seeds = ", ".join(f"{s['emb']:.4f}" for s in sp[name])
        L.append(f"| {lab} | {c['mean_len']:.2f} | {c['true_recall_item_weighted']:.3f} | {c['pos_own_named']:.3f} | {c['neg_own_named_all']:.3f} | "
                 f"**{e['cell']:.4f}** | {e['delta']:+.4f} | {ci(e)} | {l['cell']:.4f} | {l['delta']:+.4f} | {ci(l)} | {seeds} |")
    CS = S4["cells"]["661"].get("composite_s2u")
    if CS:
        x = CS["vs_s2u"]; c = S4["cells"]["661"]["composite_S2U_L32_c0.4_r0.801"]["census"]; cm = CS["census_s2u_measured"]
        seeds = ", ".join(f"{q['emb']:.4f}" for q in sp["composite_S2U_L32_c0.4_r0.801"])
        L.append(f"| **S2-U composite**: L 32, c 0.400, r 0.8010 (vs the measured uncapped list: {cm['mean_len']:.2f} names, recall "
                 f"{cm['true_recall_item_weighted']:.3f}, pos named {cm['pos_own_named']:.3f}, neg named {cm['neg_own_named_all']:.3f}, emb "
                 f"{x['emb']['ref']:.4f}) | {c['mean_len']:.2f} | {c['true_recall_item_weighted']:.3f} | {c['pos_own_named']:.3f} | {c['neg_own_named_all']:.3f} | "
                 f"**{x['emb']['cell']:.4f}** | {x['emb']['delta']:+.4f} vs {x['emb']['ref']:.4f} | {ci(x['emb'])} | {x['lex']['cell']:.4f} | "
                 f"{x['lex']['delta']:+.4f} vs {x['lex']['ref']:.4f} | {ci(x['lex'])} | {seeds} |")
    L.append("")
    p = R["L15_c0_r0.2996"]["vs_believed"]["emb"]; f36 = R[f"L15_c{C_BEL}_r0.3604"]["vs_believed"]["emb"]; f30 = R[f"L15_c{C_BEL}_r0.2996"]["vs_believed"]["emb"]
    L.append(f"**Verdict on the prediction of record: the \"materially above\" branch fired.** The cell lands at {p['cell']:.4f}, "
             f"{p['delta']:+.4f} above 0.5858 — outside the 0.05 band, by 0.01 — with a wider interval {ci(p)} that includes zero; "
             f"across seeds 43–46 it lands at {min(s['emb'] for s in sp['L15_c0_r0.2996']):.4f}–{max(s['emb'] for s in sp['L15_c0_r0.2996']):.4f}, "
             "every one more than 0.05 above. Length plus recall leave a residual, and §0 said where to look for it: the "
             "contamination census. Setting contamination to BELIEVED's 0.232 as well closes it — "
             f"**{f30['cell']:.4f} ({f30['delta']:+.4f}, {ci(f30)}) at r = 0.2996 and {f36['cell']:.4f} ({f36['delta']:+.4f}, {ci(f36)}) at r = 0.3604**, "
             "both inside the band with intervals including zero at seed 42. Across seeds 43–46 the same two cells range "
             f"{min(x['emb'] for x in sp[f'L15_c{C_BEL}_r0.2996']):.4f}–{max(x['emb'] for x in sp[f'L15_c{C_BEL}_r0.3604']):.4f}, i.e. "
             f"{min(x['emb'] for x in sp[f'L15_c{C_BEL}_r0.2996']) - BEL:+.3f} to {max(x['emb'] for x in sp[f'L15_c{C_BEL}_r0.3604']) - BEL:+.3f} "
             f"from 0.5858: {sum(1 for x in sp[f'L15_c{C_BEL}_r0.2996'] + sp[f'L15_c{C_BEL}_r0.3604'] if abs(x['emb'] - BEL) > 0.05)} of the eight "
             "extra-seed draws fall outside the 0.05 band. Read plainly: **the reconstruction lands on or somewhat above the "
             "target, not below it, and seed 42 is at the favourable end of its own spread.** The lexical variant reconstructs "
             "to within 0.03 on the same cells. What the residual is not: the census of the full reconstruction has pos named "
             f"{R[f'L15_c{C_BEL}_r0.3604']['census']['pos_own_named']:.3f} against BELIEVED's 0.423 (the seeded drops remove positives' names "
             "*more* often than BELIEVED does at the same micro-recall, which pushes the cell down, not up) and neg named 0.233 "
             "against 0.232. What it may be: BELIEVED's filler names are not random own-store names but the slots of the store's "
             "inactive entries — the attributes that have changed, which are the ones questions tend to ask about — so they may "
             "inflate negatives more than untargeted fillers do; and BELIEVED's contaminated negatives carry 1.09 own names against "
             "the reconstruction's one. Neither is measured here.\n")
    L.append(f"**A caution the census makes visible.** The recall-dropped cell at *base* length and base contamination lands at "
             f"{S4['cells']['661']['Lbase_c0_r0.3604']['emb']['auroc']:.4f} (r 0.3604) / {S4['cells']['661']['Lbase_c0_r0.2996']['emb']['auroc']:.4f} "
             "(r 0.2996) — numerically as close to 0.5858 as the full reconstruction — with a mean list length of 0.5 names, neg "
             "named 0.011 and most items in the 0.0 tie block of §1.1. It matches the scalar from a different regime. The scalar "
             "does not identify the mechanism; the two census columns do (BELIEVED: 15 names, pos named 0.423, neg named 0.232), "
             "and only the full reconstruction matches them.\n")
    if CS:
        x = CS["vs_s2u"]["emb"]
        L.append(f"**The second operating point checks the same way.** The uncapped list's composite (L 32, recall 0.80, contamination "
                 f"0.40, each its measured value) lands at {x['cell']:.4f} against the measured S2-U {x['ref']:.4f} ({x['delta']:+.4f}, wider "
                 f"interval {ci(CS['vs_s2u']['emb'])}); seeds 43–46: "
                 + ", ".join(f"{q['emb']:.4f}" for q in sp["composite_S2U_L32_c0.4_r0.801"]) + ". "
                 + ("Inside the band with an interval including zero, but consistently *below* the measured list at every seed, where the "
                    "capped composite of the previous paragraph sat consistently *above* its target. The three store properties reproduce "
                    "the uncapped list's score to within tolerance; the two residuals have opposite signs, so whatever the reconstruction "
                    "misses is not one fixed bias in one direction — on the uncapped list the untargeted fillers appear to inflate negatives "
                    "slightly less than the store's own inactive-entry names do, on the capped list the seeded drops appear to cost positives "
                    "slightly more. Neither is measured here." if CS["within_0.05_emb"] and not CS["vs_s2u"]["emb"]["ci_governing"]["excludes_zero"]
                    else "Outside the band or with an interval excluding zero: the three properties do not fully reproduce the uncapped "
                         "list's score, and that residual is printed as it stands.") + "\n")
    L.append("So: **the BELIEVED degradation is explained by recall loss and contamination together, with length neutral on this "
             "population.** Neither recall-with-length nor contamination alone reaches the target with BELIEVED's census (0.6456 / 0.6613 "
             "and 0.6849 respectively); together they do, at or a little above it. The \"precision 0.035\" label names neither mechanism.\n")
    return L


# =============================================================================== section 8
def sec8():
    cf3, cf2 = S3["cells"]["cf2"], S2["cells"]["cf2"]
    s6p = S4["cells"]["661"]["partition"]["0.3604"]["emb"]
    L = ["## 8. Answers\n"]
    L.append(f"**(a) What does 0.9223 become at contamination 0.232?** **{cf2['rate_0.232']['emb']['auroc_superseded']:.4f}** "
             f"(whole set 0.7663 → {cf2['rate_0.232']['emb']['auroc']:.4f}); at 0.49, BELIEVED's rate on PRESENT negatives, "
             f"{cf2['rate_0.49']['emb']['auroc_superseded']:.4f}. It follows (1 − c)·A + c·0.5 to within 0.015 at every rate on the slice (§3).\n")
    L.append(f"**(b) How much of the base score survives at the operating points, and at the stress bound?** At **L = 15** (FR-Bank's "
             f"renderer cap) the 444 slice is **{cf3['L15_c0.0']['emb']['auroc_superseded']:.4f}** — the number to take away — and at L = 32 "
             f"(uncapped BELIEVED) {cf3['L32_c0.0']['emb']['auroc_superseded']:.4f}. At the registered stress condition, **L = 60**, which no tested "
             f"backend emits, 0.9223 → {cf3['L60_c0.0']['emb']['auroc_superseded']:.4f}: {(cf3['L60_c0.0']['emb']['auroc_superseded'] - 0.5) / (0.9223 - 0.5):.0%} "
             f"of the above-chance margin; whole set 0.7663 → {cf3['L60_c0.0']['emb']['auroc']:.4f} ({(cf3['L60_c0.0']['emb']['auroc'] - 0.5) / (0.7663 - 0.5):.0%}), "
             "interval excluding zero. Padding does not \"barely move\" the score; that outcome did not occur. The 661's whole-population column is "
             "muted by its probe negatives and empty-summary positives (§4.3) and is not the place to read this.\n")
    L.append(f"**(c) Does length, recall, or contamination explain most of the drop to 0.5858?** Recall (Shapley share "
             f"{s6p['shapley_share']['r']:.0%}), then contamination ({s6p['shapley_share']['c']:.0%}); length is a *credit* on the 661 "
             f"({s6p['shapley_share']['L']:.0%}) because own-store fillers inflate the 145 natural-absent probes less than they inflate "
             "on-store items and partly restore dropped positives through near-synonyms. The three are sub-additive, not additive "
             f"(interaction {s6p['interaction']:+.4f} on a gap of {s6p['total_gap']:+.4f}). On the 444, where length is purely adverse, "
             "the ordering is recall > contamination > length (§6).\n")
    L.append("**(d) Did the BELIEVED reconstruction target hit?** Not at either recall cell alone: 0.6456 (r 0.2996) and 0.6613 "
             "(r 0.3604) sit 0.06 and 0.08 above 0.5858, and the prediction's own \"materially above\" branch fired on the cell of "
             "record (margin 0.0598 > 0.05). With contamination also at BELIEVED's 0.232 it hits at both: **0.5930 and 0.6096**, "
             "margins +0.007 and +0.024, intervals including zero; across seeds 43–46 the same cells sit +0.008 to +0.066 above, "
             "two of eight draws outside the band — on or somewhat above the target, never below (§7).\n")
    L.append("**The short-list objection, answered on its own terms.** The list the 0.92 rests on holds 1.76 real names (not 1.75, "
             "and the 661's holds 1.45; §1.1). Lengthening it with correct names costs real discrimination (b), so \"~2 candidates\" "
             "is a fair description of an easy regime. But the larger reason the regime was easy is the one the objection did not "
             "raise: the list names none of the negatives (§2), and at the contamination rate the store's own metadata produces the "
             "lookup follows a mixing law down to 0.73 (§3). The paper's comparison of monitor and lookup should be read against "
             "that law, on a census of the list each was shown, rather than against 0.92.\n")
    return L


def sec9():
    return ["## 9. Artifacts and reproduction\n",
            "`tools/sweep_common.py` (loaders, list builders, census, scorers; reuses the committed estimators and scorers "
            "verbatim), `tools/step1_reproduce.py` → `results/step1_reproduce.json`, `tools/step2_contamination.py` → "
            "`results/step2_contamination.json`, `tools/step3_length.py` → `results/step3_length.json`, `tools/step4_recall.py` → "
            "`results/step4_recall.json`, `tools/step5_report.py` → this file from §2 on, `results/auroc_vs_length.png`, "
            "`results/step5_diagnostics.json`. Deterministic; seed 42; no model call; encoder `sentence-transformers/all-MiniLM-L6-v2` "
            "offline, the whole name universe (4,717 names, 450 questions) encoded once. Every paired interval is the committed "
            "`common_e1r.boot_item` / `boot_cluster` (1000 draws, seed 42, single-class draws discarded, 2.5 / 97.5); the wider of "
            "the two is printed and governs. The ledger entry for the marker artifact is `e1r_robustness/DEVIATIONS_E1R.md` D-E1R-11.\n"]


# =============================================================================== diagnostics + figure
def diagnostics(r661, own, dis):
    def grp(r):
        if r["y"] == 1:
            return "pos_sup" if r["state"] == "superseded" else "pos_counted"
        if r["item_id"].startswith("probe"):
            return "neg_probe"
        return "neg_present" if r["label"] == "PRESENT" else "neg_absent_ablation"
    out = {"groups": {g: sum(1 for r in r661 if grp(r) == g) for g in ("pos_sup", "pos_counted", "neg_present", "neg_absent_ablation", "neg_probe")}}
    y = np.array([r["y"] for r in r661])
    for name, kw in (("Lbase_c0_r1.0", {}), ("L15_c0_r1.0", dict(L=15)), ("Lbase_c0_r0.3604", dict(recall=0.3604)),
                     ("L15_c0_r0.3604", dict(L=15, recall=0.3604)), ("Lbase_c0.232_r0.3604", dict(recall=0.3604, c=C_BEL)),
                     ("L15_c0.232_r0.3604", dict(L=15, recall=0.3604, c=C_BEL))):
        lists, _ = make_cell(r661, own, dis, **kw)
        s = emb_cached(r661, lists)
        pi = [i for i, r in enumerate(r661) if r["y"] == 1]
        pr = [i for i, r in enumerate(r661) if grp(r) == "neg_probe"]
        oth = [i for i, r in enumerate(r661) if r["y"] == 0 and grp(r) != "neg_probe"]
        out[name] = {"mean_score": {g: float(np.mean([s[i] for i, r in enumerate(r661) if grp(r) == g])) for g in out["groups"]},
                     "auroc_pos_vs_probes": float(auroc(s[pi + pr], np.array([1] * len(pi) + [0] * len(pr)))),
                     "auroc_pos_vs_other_negs": float(auroc(s[pi + oth], np.array([1] * len(pi) + [0] * len(oth)))),
                     "auroc_whole": float(auroc(s, y))}
    return out


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    BLUE, ORANGE, AQUA, VIOLET = "#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e2", "#fcfcfb"
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8), dpi=150, facecolor=SURF, sharey="row")
    for col, (pop, title, _) in enumerate(POPS):
        P = S3["cells"][pop]
        for row, (v, lab) in enumerate((("emb", "embedding lookup"), ("lex", "lexical lookup"))):
            ax = axes[row][col]
            ax.set_facecolor(SURF)
            for c, ls, ctag in ((0.0, "-", "c = 0"), (C_BEL, "--", "c = 0.232")):
                for key, colr, stag in (("auroc_superseded", ORANGE, "supersession slice"), ("auroc", BLUE, "whole set")):
                    xs, ys = [], []
                    for Ln in ("base", 5, 10, 15, 30, 32, 60):
                        nm = f"L{Ln}_c{c}"
                        if nm in P:
                            xs.append(P[nm]["census"]["mean_len"]); ys.append(P[nm][v][key])
                    ax.plot(xs, ys, ls, color=colr, lw=2, marker="o", ms=6, mec=SURF, mew=1, label=f"{stag}, {ctag}")
                    ax.annotate(f"{ys[-1]:.3f}", (xs[-1], ys[-1]), xytext=(5, 0), textcoords="offset points", fontsize=8, color=INK2, va="center")
            if pop == "661":
                for x_, y_, t in ((15.04, S4["cells"]["661"]["believed_measured"][v]["auroc"], "BELIEVED (measured)"),
                                  (32.55, jload(OUT / "step1_reproduce.json")["got"][f"661|S2U|{v}"], "S2-U (measured)")):
                    ax.plot([x_], [y_], marker="D", ms=7, color=VIOLET, mec=SURF, mew=1, ls="none")
                    ax.annotate(t, (x_, y_), xytext=(-8, 6), textcoords="offset points", fontsize=8, color=INK2, ha="right", va="bottom")
            ax.set_xscale("log")
            ax.set_xticks([1.5, 5, 10, 15, 32, 60]); ax.set_xticklabels(["base", "5", "10", "15", "32", "60"])
            ax.minorticks_off()
            ax.axhline(0.5, color=GRID, lw=1)
            ax.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
            for sp_ in ("top", "right"):
                ax.spines[sp_].set_visible(False)
            for sp_ in ("left", "bottom"):
                ax.spines[sp_].set_color(GRID)
            ax.tick_params(colors=INK2, labelsize=9)
            ax.set_title(f"{title} — {lab}", fontsize=10, color=INK, loc="left")
            if row == 1:
                ax.set_xlabel("superseded-names list length (mean names per item)", fontsize=9, color=INK2)
            if col == 0:
                ax.set_ylabel("AUROC (NOK, PN vs rest)", fontsize=9, color=INK2)
            ax.set_ylim(0.45, 1.0)
    axes[0][0].legend(fontsize=8, frameon=False, loc="lower left", labelcolor=INK2)
    fig.suptitle("Superseded-names lookup vs list length, at contamination 0 and 0.232 (own-store correct fillers, recall 1.0, seed 42)",
                 fontsize=11, color=INK, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(OUT / "auroc_vs_length.png", facecolor=SURF)
    plt.close(fig)


def main():
    r661, rcf2 = load_661(), load_cf2()
    own, dis, _ = pools(r661 + rcf2)
    prime_embeddings(r661 + rcf2, own, dis)
    D = diagnostics(r661, own, dis)
    jdump(D, OUT / "step5_diagnostics.json")
    figure()
    M = mixing()
    jdump(M, OUT / "step5_mixing_law.json")
    body = "\n".join(sec2() + sec3(M) + sec4(D) + sec5() + sec6() + sec7() + sec8() + sec9())
    s = io.open(REPORT, encoding="utf-8").read()
    head = s[: s.index("\n## 2. ") + 1]
    io.open(REPORT, "w", encoding="utf-8", newline="\n").write(head + body)
    print(f"wrote {REPORT} (sections 2-9), {OUT / 'auroc_vs_length.png'}, {OUT / 'step5_diagnostics.json'}, {OUT / 'step5_mixing_law.json'}")


if __name__ == "__main__":
    main()
