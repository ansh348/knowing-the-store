"""score_e1qp.py -- E1-QP scoring, per PREREG_E1QP.md (f4dafdd…) and nothing else.

NO new calls. Produces:
  (b) matched-contrast blind/indexed NOK per lineage, with the paper's bootstrap CIs
  (c) blind NOK residualised against the probe scores, descriptive
      and the E1-XV deltas restated beside CEILING(P1)
  QP-1 / QP-2 / QP-3 adjudicated mechanically.

Estimators imported from the committed scorers, not reimplemented.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "e1_metamemory" / "tools"))

from qp_common import (QP, population, matched_slice, strict_slice,  # noqa: E402
                       model_scores)
from score_e1 import auroc, boot          # noqa: E402
from score_ladder import auroc_ci         # noqa: E402

RES = QP / "results"
MODELS = ["gpt-4.1-mini", "gpt-5.6-luna", "gpt-5.6-sol",
          "claude-opus-5", "claude-haiku-4-5-20251001", "kimi-k3"]
# E1-XV / NUMBERS.md section 9 blind NOK on P1, cited constants
BLIND_NOK_P1 = {"gpt-4.1-mini": 0.5000, "gpt-5.6-luna": 0.5585, "gpt-5.6-sol": 0.5290,
                "claude-opus-5": 0.6994, "claude-haiku-4-5-20251001": 0.3688,
                "kimi-k3": 0.5983}
NOK_DELTA_P1 = {"gpt-4.1-mini": 0.2139, "gpt-5.6-luna": 0.2940, "gpt-5.6-sol": 0.3298,
                "claude-opus-5": 0.1528, "claude-haiku-4-5-20251001": 0.4511,
                "kimi-k3": 0.2605}
BLIND_NOK_CI_P1 = {"claude-opus-5": (0.5712, 0.8135),
                   "claude-haiku-4-5-20251001": (0.2571, 0.4789),
                   "kimi-k3": (0.4629, 0.7160)}


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def arm_cell(rows, S, judgment="nok"):
    """blind vs indexed AUROC on `rows` for one model's committed scores."""
    tags = [r["item_id"] for r in rows
            if (r["item_id"], "BLIND") in S and (r["item_id"], "INDEXED-TRUE") in S
            and S[(r["item_id"], "BLIND")].get(judgment) is not None
            and S[(r["item_id"], "INDEXED-TRUE")].get(judgment) is not None]
    idx = {r["item_id"]: r for r in rows}
    y = [idx[t]["y_nok"] for t in tags]
    if len(set(y)) < 2:
        return {"n": len(tags), "note": "single-class or no coverage"}
    b = [S[(t, "BLIND")][judgment] for t in tags]
    i = [S[(t, "INDEXED-TRUE")][judgment] for t in tags]
    bci, ici, bs = auroc_ci(b, y), auroc_ci(i, y), boot(b, i, y)
    return {"n": len(tags), "n_pos": int(sum(y)),
            "blind": auroc(b, y), "indexed": auroc(i, y),
            "delta": auroc(i, y) - auroc(b, y),
            # E1's D23 pathology travels with any cell that shows it: a blind arm
            # with almost no distinct values is not a measurement of "fails to
            # discriminate", it is a measurement of "never varies".
            "distinct_blind": len(set(b)), "distinct_indexed": len(set(i)),
            "blind_modal_share": max(b.count(v) for v in set(b)) / len(b),
            "blind_near_degenerate": len(set(b)) <= 2
            or max(b.count(v) for v in set(b)) / len(b) >= 0.95,
            "blind_ci": [bci["ci_lo"], bci["ci_hi"]],
            "blind_includes_0.50": bci["includes_0.50"],
            "indexed_ci": [ici["ci_lo"], ici["ci_hi"]],
            "indexed_includes_0.50": ici["includes_0.50"],
            "delta_ci": [bs["ci_lo"], bs["ci_hi"]],
            "delta_excludes_zero": bs["excludes_zero"]}


def main():
    T = jload(RES / "probe_tfidf.json")["probes"]
    L = jload(RES / "probe_llm.json")["probes"]
    R = {"prereg_sha256": "f4dafdd1117461a1d95b4382dffbcac3aefad022967602794d7f2a5e67572a28"}

    # ---------- ceilings
    ceil = {}
    for pn, tk, lk in (("P1", "P1:full:PN-vs-rest", "P1:full:y_nok"),
                       ("P2", "P2:full:PN-vs-rest", "P2:full:y_nok")):
        ceil[pn] = {"tfidf": T[tk]["auroc"], "tfidf_ci": T[tk]["ci"],
                    "llm": L[lk]["auroc"], "llm_ci": L[lk]["ci"],
                    "ceiling": max(T[tk]["auroc"], L[lk]["auroc"]),
                    "ceiling_source": "tfidf" if T[tk]["auroc"] >= L[lk]["auroc"] else "llm"}
    R["ceilings"] = ceil
    C1 = ceil["P1"]["ceiling"]

    # ---------- QP-1
    qp1 = {}
    for m in MODELS:
        bn = BLIND_NOK_P1[m]
        ci = BLIND_NOK_CI_P1.get(m)
        above = bn > C1 and (ci is not None and ci[0] > C1)
        qp1[m] = {"blind_nok": bn, "ceiling": C1, "under_ceiling": bn <= C1,
                  "ci": list(ci) if ci else None,
                  "entirely_above_ceiling": bool(above), "HOLDS": bool(not above)}
    R["QP-1"] = {"per_model": qp1, "HOLDS": all(v["HOLDS"] for v in qp1.values())}

    # ---------- QP-2, the neutralisation check
    qp2 = {}
    for pn in ("P1", "P2"):
        k = f"{pn}:matched:PN-vs-slotablated"
        qp2[pn] = {"n": T[k]["n"], "n_pos": T[k]["n_pos"], "auroc": T[k]["auroc"],
                   "ci": T[k]["ci"], "includes_0.50": T[k]["includes_0.50"],
                   "HOLDS": bool(T[k]["includes_0.50"])}
    # the powered population governs
    R["QP-2"] = {"per_population": qp2, "powered": "P2", "HOLDS": qp2["P2"]["HOLDS"]}

    # ---------- (b) matched contrast
    S = model_scores()
    P1, P2 = population("P1"), population("P2")
    slices = {"P1:full": P1, "P1:matched": matched_slice(P1), "P1:strict": strict_slice(P1),
              "P2:full": P2, "P2:matched": matched_slice(P2), "P2:strict": strict_slice(P2)}
    mc = {}
    for m in MODELS:
        mc[m] = {nm: arm_cell(rows, S[m]) for nm, rows in slices.items()}
    R["matched_contrast"] = mc

    # ---------- QP-3
    powered = mc["gpt-4.1-mini"]["P2:matched"]
    R["QP-3"] = {"lineage": "gpt-4.1-mini", "population": "P2:matched",
                 "cell": powered,
                 "HOLDS": bool(powered.get("indexed_includes_0.50") is False
                               and powered.get("blind_includes_0.50") is True),
                 "blind_near_degenerate": bool(powered.get("blind_near_degenerate")),
                 "caveat": ("the powered lineage's blind arm is near-degenerate "
                            "(D23-E1); the gate is satisfied by an arm that barely "
                            "varies, not by a varying arm that fails to discriminate")
                 if powered.get("blind_near_degenerate") else None}
    R["coverage_P2_matched"] = {m: mc[m]["P2:matched"].get("n", 0) for m in MODELS}

    # ---------- (c) residualisation, descriptive
    tf_all, llm_all = {}, {}
    for ln in io.open(RES / "probe_llm_raw.jsonl", encoding="utf-8"):
        if ln.strip():
            r = json.loads(ln)
            llm_all[r["item_id"]] = r.get("pn_likelihood")
    # out-of-fold TF-IDF predictions on P1, recomputed with the frozen config
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from probes import oof_tfidf
    pred, y, _ = oof_tfidf(P1, "y_nok")
    for r, p in zip(P1, pred):
        tf_all[r["item_id"]] = float(p)

    resid = {}
    for m in MODELS:
        tags = [r["item_id"] for r in P1
                if (r["item_id"], "BLIND") in S[m]
                and S[m][(r["item_id"], "BLIND")].get("nok") is not None
                and tf_all.get(r["item_id"]) is not None
                and llm_all.get(r["item_id"]) is not None]
        if len(tags) < 10:
            resid[m] = {"note": "insufficient coverage"}
            continue
        idx = {r["item_id"]: r for r in P1}
        b = np.array([S[m][(t, "BLIND")]["nok"] for t in tags], float)
        yy = np.array([idx[t]["y_nok"] for t in tags], int)
        X = np.column_stack([np.ones(len(tags)),
                             [tf_all[t] for t in tags], [llm_all[t] for t in tags]])
        beta, *_ = np.linalg.lstsq(X, b, rcond=None)
        r_ = b - X @ beta
        rc = auroc_ci(r_, yy)
        resid[m] = {"n": len(tags), "auroc_raw_blind": auroc(b, yy),
                    "auroc_residual": auroc(r_, yy),
                    "residual_ci": [rc["ci_lo"], rc["ci_hi"]],
                    "residual_includes_0.50": rc["includes_0.50"],
                    "beta_tfidf": float(beta[1]), "beta_llm": float(beta[2])}
    R["residualised"] = resid
    R["xv_restated"] = {m: {"blind_nok": BLIND_NOK_P1[m], "nok_delta": NOK_DELTA_P1[m],
                            "ceiling_P1": C1} for m in MODELS}
    R["llm_cost_usd"] = jload(RES / "probe_llm.json")["usd_this_run"]

    io.open(RES / "e1qp_scores.json", "w", encoding="utf-8").write(
        json.dumps(R, indent=2))

    # ---------- console
    print("CEILINGS")
    for pn, c in ceil.items():
        print(f"  {pn}  tfidf {c['tfidf']:.4f}  llm {c['llm']:.4f}  -> CEILING "
              f"{c['ceiling']:.4f} ({c['ceiling_source']})")
    print(f"\nQP-1  (blind NOK on P1 vs CEILING(P1) = {C1:.4f})")
    for m, v in qp1.items():
        print(f"  {'ok  ' if v['HOLDS'] else 'FAIL'} {m:28s} blind NOK {v['blind_nok']:.4f}"
              f"  under ceiling {v['under_ceiling']}")
    print(f"  QP-1 HOLDS: {R['QP-1']['HOLDS']}")
    print("\nQP-2  neutralisation check (TF-IDF on the matched slice)")
    for pn, v in qp2.items():
        print(f"  {'ok  ' if v['HOLDS'] else 'FAIL'} {pn} n={v['n']:3d} "
              f"AUROC {v['auroc']:.4f} CI [{v['ci'][0]:.4f}, {v['ci'][1]:.4f}] "
              f"includes 0.50 {v['includes_0.50']}")
    print(f"  QP-2 HOLDS (powered P2): {R['QP-2']['HOLDS']}")
    print("\n(b) MATCHED CONTRAST -- blind / indexed NOK")
    for m in MODELS:
        for nm in ("P1:matched", "P2:matched"):
            c = mc[m][nm]
            if "note" in c:
                continue
            print(f"  {m:28s} {nm:12s} n={c['n']:4d} pos={c['n_pos']:3d}  "
                  f"blind {c['blind']:.4f} [{c['blind_ci'][0]:.4f},{c['blind_ci'][1]:.4f}]"
                  f" inc0.50={str(c['blind_includes_0.50']):5s}  "
                  f"indexed {c['indexed']:.4f} [{c['indexed_ci'][0]:.4f},{c['indexed_ci'][1]:.4f}]"
                  f" inc0.50={str(c['indexed_includes_0.50']):5s}  "
                  f"delta {c['delta']:+.4f} excl0={c['delta_excludes_zero']}")
    print(f"\nQP-3 HOLDS: {R['QP-3']['HOLDS']}")
    print("\n(c) RESIDUALISED blind NOK on P1")
    for m, v in resid.items():
        if "note" in v:
            print(f"  {m:28s} {v['note']}")
            continue
        print(f"  {m:28s} raw {v['auroc_raw_blind']:.4f} -> residual "
              f"{v['auroc_residual']:.4f} [{v['residual_ci'][0]:.4f},"
              f"{v['residual_ci'][1]:.4f}] includes0.50={v['residual_includes_0.50']}")
    print(f"\n  written: results/e1qp_scores.json   LLM arm ${R['llm_cost_usd']}")


if __name__ == "__main__":
    main()
