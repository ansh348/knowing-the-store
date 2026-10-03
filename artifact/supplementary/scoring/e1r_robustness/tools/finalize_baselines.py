"""Consolidate E1-R (b) into the corrected baseline table of record.

Two corrections are applied to the as-run table, both forced by the diagnostic:

  1. NB-3 (TF-IDF over index text + question) is DISQUALIFIED as an index-reading
     baseline. Its index-only ablation sits at 0.45-0.69 while its question-only
     ablation reaches 0.87-0.97, higher than the concatenated version on every
     population. NB-3 was reading question templates -- the E1-QP / D94 authorship
     confound -- not the store index. It is retained in the record as NB-3-idx
     (index text only), which is what the frozen spec was trying to measure.

  2. Pooled hard-tier rows carry a backend-identity reference. All 35 positives in that
     population are FR-Bank, so the one-bit rule "this item is FR-Bank" scores 0.7541 --
     above the monitor's pooled indexed AUROC. Absolute levels on the pooled row are
     therefore not interpretable as coverage discrimination. Paired DELTAS are unaffected,
     because a constant-across-arms indicator cannot produce a delta.
"""
from __future__ import annotations

from common_e1r import OUT, jdump, jload

LEGIT = ["NB-1 deterministic rule", "NB-2 logistic/index feats",
         "NB-4 lexical match", "NB-5 embedding match"]
TOL = 0.05
BACKEND_INDICATOR_HARD = 0.7541


def main():
    base = jload(OUT / "baselines.json")["rows"]
    diag = jload(OUT / "baselines_diagnostic.json")
    out = {}

    for key, r in base.items():
        d = diag.get(key, {})
        cands = {k: r["baselines"][k] for k in LEGIT}
        cands["NB-3-idx index text only"] = d.get("nb3_index_only")
        cands = {k: v for k, v in cands.items() if v is not None}
        best = max(cands, key=lambda k: cands[k])
        mon = r["monitor_indexed_auroc"]
        pooled = r["row"] == "R-FOK-HARD"
        out[key] = {
            "row": r["row"], "provenance": r["provenance"], "judgment": r["judgment"],
            "n": r["n"], "n_pos": r["n_pos"],
            "monitor_blind": r["monitor_blind_auroc"],
            "monitor_indexed": mon,
            "legitimate_baselines": cands,
            "best_legit_baseline": best,
            "best_legit_auroc": cands[best],
            "monitor_minus_best": mon - cands[best],
            "monitor_wins_beyond_tol": bool(mon - cands[best] > TOL),
            "baseline_matches": bool(abs(mon - cands[best]) <= TOL),
            "baseline_wins_beyond_tol": bool(cands[best] - mon > TOL),
            "DISQUALIFIED_nb3_index_plus_question": r["baselines"]["NB-3 TF-IDF/index text"],
            "nb3_question_only": d.get("nb3_question_only"),
            "nb3_index_only": d.get("nb3_index_only"),
            "backend_identity_reference": BACKEND_INDICATOR_HARD if pooled else None,
            "absolute_levels_interpretable": not pooled,
        }

    jdump({"rows": out, "tolerance": TOL,
           "disqualification": "NB-3 index+question reads question templates (D94), not the index",
           "backend_indicator_pooled_hard": BACKEND_INDICATOR_HARD,
           "spec": "e1r_robustness/SPEC_E1R.md @ 9ac91a2"},
          OUT / "baselines_final.json")

    print("=" * 118)
    print("E1-R (b) CORRECTED  --  monitor vs. legitimate index-reading baselines")
    print("=" * 118)
    hdr = (f"{'population':12s} {'prov':9s} {'n':>4s} {'blind':>7s} {'monitor':>8s} "
           f"{'NB-1':>7s} {'NB-2':>7s} {'NB-4':>7s} {'NB-5':>7s} {'NB-3idx':>8s} "
           f"{'best':>7s} {'mon-best':>9s}  verdict")
    print(hdr)
    print("-" * len(hdr))
    for k, r in out.items():
        c = r["legitimate_baselines"]
        v = r["monitor_minus_best"]
        verdict = ("MONITOR WINS" if r["monitor_wins_beyond_tol"]
                   else ("baseline wins" if r["baseline_wins_beyond_tol"] else "matches"))
        print(f"{r['row']:12s} {r['provenance']:9s} {r['n']:4d} {r['monitor_blind']:7.4f} "
              f"{r['monitor_indexed']:8.4f} "
              f"{c['NB-1 deterministic rule']:7.4f} {c['NB-2 logistic/index feats']:7.4f} "
              f"{c['NB-4 lexical match']:7.4f} {c['NB-5 embedding match']:7.4f} "
              f"{c['NB-3-idx index text only']:8.4f} {r['best_legit_auroc']:7.4f} "
              f"{v:+9.4f}  {verdict}")
    print()
    print("DISQUALIFIED NB-3 (index+question) and its ablation:")
    print(f"  {'population':12s} {'prov':9s} {'idx+q':>8s} {'idx only':>9s} {'question only':>14s}")
    for k, r in out.items():
        print(f"  {r['row']:12s} {r['provenance']:9s} "
              f"{r['DISQUALIFIED_nb3_index_plus_question']:8.4f} "
              f"{r['nb3_index_only']:9.4f} {r['nb3_question_only']:14.4f}")
    print()
    print(f"Pooled hard-tier backend-identity reference: {BACKEND_INDICATOR_HARD:.4f}")
    print("  (all 35 pooled-hard positives are FR-Bank; this exceeds the monitor's pooled")
    print("   indexed 0.7530, so pooled ABSOLUTE levels are not coverage discrimination.")
    print("   Paired deltas are unaffected: the indicator is constant across arms.)")
    print(f"\nwrote {OUT / 'baselines_final.json'}")


if __name__ == "__main__":
    main()