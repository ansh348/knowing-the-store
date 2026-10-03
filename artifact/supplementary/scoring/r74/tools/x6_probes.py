"""R76 A3 -- the two $0 items (ADDENDUM_R76 §A4). No metered calls.

A4.1 AV-CENSUS      deterministic census on committed labels: P(PN | attack_vector) on
                    the committed matched-84 cell, and the AUROC of that one feature with
                    0.5 tie credit. Same family as the committed one-bit is-FR-Bank rule
                    (0.7541) and the Table 16 registration census: no model is fit, nothing
                    is held out, no sample is drawn -- so NO INTERVAL is defined or
                    reported. Provenance: this value was computed pre-freeze as the R76 STOP
                    premise diagnostic (D-R74-13); it is a deterministic function of
                    committed labels with no seed, so it is invariant to run order, and the
                    pre-freeze computation is the reported one.

A4.2 MATCHED-PROBE  the committed E1-QP supervised TF-IDF probe, unchanged, on the 36
                    authorship-matched rendered questions (target y_nok, 12 PN vs 24
                    non-PN). Same featurization and CV protocol as the Table 7 rows.
                    Zero-shot reader row: SKIPPED -- the committed cache holds no ns:* rows,
                    so it would cost metered calls ($0 rule).

Writes r74/x6/x6_probes.json.
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e1qp_questionprior" / "tools"))
from score_e1 import auroc                      # committed estimator
from score_ladder import auroc_ci               # committed one-sample bootstrap
from probes import oof_tfidf, TFIDF, LOGREG, NSPLITS, SEED   # committed probe, unchanged

X6 = ROOT / "r74" / "x6"
X6.mkdir(parents=True, exist_ok=True)
out = {"registration": "ADDENDUM_R76 §A4 @ 692e379bdc"}

# ---------------------------------------------------------------- A4.1 AV-CENSUS ----
cell = json.load(open(ROOT / "e1xv_crossvendor" / "manifests" / "cell_84.json",
                      encoding="utf-8"))
meta = {i["item_id"]: i for i in
        json.load(open(ROOT / "e1_metamemory" / "build" / "items_final.json",
                       encoding="utf-8"))}
assert cell["expect"] == cell["rebuilt"] == {"n": 84, "n_fok_pos": 54, "n_nok_pos": 40}
rows = [(i, meta[i["item_id"]]) for i in cell["items"]]
assert len(rows) == 84

strata = collections.defaultdict(list)
for i, m in rows:
    strata[m["attack_vector"]].append(i["y_nok"])
rate = {k: sum(v) / len(v) for k, v in strata.items()}

scores = [rate[m["attack_vector"]] for i, m in rows]
y = [i["y_nok"] for i, m in rows]
pos = [s for s, yy in zip(scores, y) if yy == 1]
neg = [s for s, yy in zip(scores, y) if yy == 0]
num = sum((a > b) + 0.5 * (a == b) for a in pos for b in neg)
av_auroc = num / (len(pos) * len(neg))
assert abs(av_auroc - auroc(scores, y)) < 1e-9, "tie handling differs from the committed estimator"

single = [k for k, v in strata.items() if sum(v) in (0, len(v))]
both = [k for k in strata if k not in single]
out["AV_CENSUS"] = {
    "class": "deterministic census on committed labels; no model fit, no holdout, "
             "no resampling; NO INTERVAL (is-FR-Bank 0.7541 / Table 16 family)",
    "provenance": "computed pre-freeze as the R76 STOP premise diagnostic (D-R74-13); "
                  "seedless and sampling-free, so invariant to run order",
    "population": "committed matched-84 FR-Bank cell (cell_84.json), target y_nok",
    "n": 84, "pn": sum(y), "auroc_one_feature": av_auroc,
    "tie_pairs": sum(1 for a in pos for b in neg if a == b),
    "total_pairs": len(pos) * len(neg),
    "committed_tfidf_same_cell": 0.7972,
    "n_strata": len(strata), "n_single_class_strata": len(single),
    "strata_with_both_classes": sorted(both),
    "strata": {k: {"n": len(v), "pn": sum(v), "p_pn": rate[k]}
               for k, v in sorted(strata.items(), key=lambda kv: -len(kv[1]))},
}

# ------------------------------------------------------------ A4.2 MATCHED-PROBE ----
R = json.load(open(ROOT / "r74" / "x5" / "x5_render.json", encoding="utf-8"))
assert R["spot_check"]["verdict"] == "PASS" and R["cell"]["n"] == 36
prows = [{"question": r["rendered_question"], "persona": r["persona"],
          "y_nok": 1 if r["label"] == "PN" else 0}
         for r in sorted(R["rows"], key=lambda r: r["item_id"])]
assert len(prows) == 36 and sum(r["y_nok"] for r in prows) == 12

pred, yy, nsp = oof_tfidf(prows, "y_nok")
ci = auroc_ci(pred, yy)
out["MATCHED_PROBE"] = {
    "apparatus": "committed e1qp probes.oof_tfidf, unchanged",
    "config": {"tfidf": TFIDF, "logreg": LOGREG, "n_splits_cap": NSPLITS,
               "n_splits_used": nsp, "seed": SEED, "grouped_by": "persona"},
    "population": "the 36 authorship-matched rendered E1-NS questions (x5_render.json)",
    "n": int(len(yy)), "pn": int(yy.sum()), "personas": len({r["persona"] for r in prows}),
    "auroc": auroc(pred, yy), "ci": [ci["ci_lo"], ci["ci_hi"]],
    "includes_0.50": ci["includes_0.50"],
    "width_disclosure": "wide interval expected at n=36 with 12 positives; this row is a "
                        "construction check on the E1-NS cell, not a measurement of the "
                        "FR-Bank populations, and is not compared against 0.7972 as if the "
                        "two sat on one population",
}

# zero-shot row: registered SKIP, with the reason recorded
raw = ROOT / "e1qp_questionprior" / "results" / "probe_llm_raw.jsonl"
cached = [json.loads(l) for l in open(raw, encoding="utf-8") if l.strip()]
ns_cached = [r for r in cached if r["item_id"].startswith("ns:")]
out["ZERO_SHOT_MATCHED"] = {
    "status": "SKIPPED (registered)", "cached_rows_total": len(cached),
    "cached_rows_for_matched_cell": len(ns_cached),
    "reason": "no ns:* responses exist in the committed cache and the matched questions are "
              "newly rendered text, so the row would require fresh metered calls ($0 rule)",
}
assert not ns_cached, "ns:* rows unexpectedly present -- re-examine the $0 skip"

json.dump(out, open(X6 / "x6_probes.json", "w", encoding="utf-8"), indent=1,
          sort_keys=True, default=float)

A = out["AV_CENSUS"]
print(f"AV-CENSUS  n={A['n']} pn={A['pn']}  one-feature AUROC {A['auroc_one_feature']:.4f} "
      f"(committed TF-IDF same cell {A['committed_tfidf_same_cell']})  "
      f"single-class strata {A['n_single_class_strata']}/{A['n_strata']}  NO INTERVAL")
for k, v in A["strata"].items():
    print(f"    {k:32s} n={v['n']:3d} PN={v['pn']:3d} P(PN)={v['p_pn']:.3f}")
M = out["MATCHED_PROBE"]
print(f"MATCHED-PROBE  n={M['n']} pn={M['pn']} personas={M['personas']} splits={nsp}  "
      f"AUROC {M['auroc']:.4f} [{M['ci'][0]:.4f}, {M['ci'][1]:.4f}]  "
      f"includes 0.50: {M['includes_0.50']}")
print(f"ZERO-SHOT  {out['ZERO_SHOT_MATCHED']['status']} -- "
      f"{out['ZERO_SHOT_MATCHED']['cached_rows_for_matched_cell']} cached ns:* rows of "
      f"{out['ZERO_SHOT_MATCHED']['cached_rows_total']}")
