"""posthoc_minus_lookup.py -- POST HOC (requested by the author after the PARA run of 2026-09-21; not in registrations/ADDENDUM_PARA.md):
each model minus the embedding lookup under the same summary, on the paraphrase set AND on the original questions of the same pairs, whole set
and supersession only, under both metrics:

  pooled   AUROC difference with the item-level and the persona-clustered paired bootstrap (score_para.paired, the registration's construction:
           1,000 draws, seed 42; the same function that wrote every model-minus-lookup row of para_scores.json);
  matched  R125's construction (reviews/r125/tools/r125_common: within-triple PN vs PRESENT outcome, model minus lookup = the mean over triples of
           the per-triple outcome difference; triple-level and persona-grouped bootstrap, 1,000 draws, seed 42), the same estimator score_para.matched_metric
           uses for paraphrase minus original.

Reads the rows already scored (cf2_paraphrase/rows/, the recorded CF-2 rows through score_cf.load_lane, results/lookups*.json); no model call.
The registered rows (para_scores.json) are not touched: the whole-set "model minus embedding lookup on the paraphrase set" rows of section 4c
are re-derived here from the same arrays and asserted equal to para_scores.json at eight decimals before anything is written.
-> cf2_paraphrase/results/para_minus_lookup_posthoc.json (the 115); PARA_POP=all124 -> para_minus_lookup_posthoc_all124.json (sensitivity, not registered).
Usage: python cf2_paraphrase/tools/posthoc_minus_lookup.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_para as sp  # noqa: E402
from para_common import jdump, jload  # noqa: E402
from sweep_common import auroc, state_mask  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "reviews" / "r125" / "tools"))
from r125_common import boot_persona, boot_triple  # noqa: E402

S = sp.S
CODES = (("MINI", "gpt-4.1-mini"), ("H45", "claude-haiku-4-5-20251001"), ("OP5", "claude-opus-5"), ("LUNA", "gpt-5.6-luna"), ("SOL", "gpt-5.6-sol"))


def matched_minus(rows, v_model, v_lookup, pids, gp_all):
    """Model minus lookup under the matched metric on the given triples: per-triple outcome (PN vs PRESENT) of the model minus that of the lookup."""
    pos = {(r["pair_id"], r["version"]): k for k, r in enumerate(rows)}

    def outcomes(v):
        a = np.array([v[pos[(q, "PN")]] for q in pids], float); b = np.array([v[pos[(q, "PRESENT")]] for q in pids], float)
        out = np.where(a > b, 1.0, np.where(a == b, 0.5, 0.0)); out[np.isnan(a) | np.isnan(b)] = np.nan
        return out

    om, ol = outcomes(v_model), outcomes(v_lookup)
    d = om - ol; keep = ~np.isnan(d); gp = np.array([gp_all[q] for q in pids])
    it, cl = boot_triple(d), boot_persona(d, gp)
    return {"delta": float(d[keep].mean()) if keep.any() else None, "n": int(keep.sum()),
            "model_matched": float(om[keep].mean()) if keep.any() else None, "lookup_matched": float(ol[keep].mean()) if keep.any() else None,
            "ci_triple": it, "ci_persona": cl,
            "both_exclude_zero": bool(it.get("excludes_zero") and cl.get("excludes_zero")), "agree": bool(it.get("excludes_zero") == cl.get("excludes_zero"))}


def pooled_minus(lookup, model, y, g):
    """Model minus lookup, pooled AUROC, both paired bootstraps (score_para.paired: delta = auroc(new) - auroc(base))."""
    r = sp.paired(lookup, model, y, g)
    r["model_auroc"] = float(auroc(model, y)); r["lookup_auroc"] = float(auroc(lookup, y))
    return r


def main():
    SC = jload(sp.res_path("para_scores.json"))
    LK = jload(sp.res_path("lookups.json"))
    assert SC["population"] == sp.POP == LK.get("population", "accepted")
    P = sp.accepted_pairs(); rows = sp.items(P)
    y = np.array([r["y"] for r in rows], int); g = np.array([r["persona"] for r in rows])
    sup = state_mask(rows, "superseded")
    pids_all = sorted({r["pair_id"] for r in rows})
    pstate = {r["pair_id"]: r["state"] for r in rows}
    pids_sup = [q for q in pids_all if pstate[q] == "superseded"]
    gp_all = {r["pair_id"]: r["persona"] for r in rows}
    lk = {k: {"orig": np.array(v["orig"], float), "para": np.array(v["para"], float)} for k, v in LK["scores"].items()}
    out = {"label": "POST HOC, not registered: each model minus the embedding lookup under the same summary, paraphrase set and original questions of the same pairs, "
                    "whole set and supersession only, pooled AUROC (item / persona paired bootstrap) and the matched metric (R125's construction; triple / persona bootstrap)",
           "population": sp.POP, "n_pairs": len(P), "n_pairs_superseded": len(pids_sup), "n_items": len(rows), "n_items_superseded": int(sup.sum()),
           "registration_sha256": SC["registration_sha256"], "sheet_sha256": SC["sheet_sha256"], "models": {}}
    for code, lane in CODES:
        M = SC["models"].get(code)
        if not M or "v2" not in M:
            out["models"][code] = {"status": "lane not run"}; continue
        rec = S.load_lane(code); newd, _ = sp.load_new(code)
        R = {"added_not_registered": bool(M.get("added_not_registered"))}
        for arm in sp.ARMS:
            sv = sp.ARM_KEY[arm]
            if sv not in M:
                continue
            o = np.array([rec.get((r["item_id"], arm), np.nan) for r in rows], float)
            p = np.array([newd.get((r["item_id"], arm), np.nan) for r in rows], float)
            ok = ~np.isnan(o) & ~np.isnan(p)
            e = lk[f"emb_{sv}"]
            # the registered whole-set row re-derived and asserted against para_scores.json (same arrays, same function)
            chk = sp.paired(e["para"][ok], p[ok], y[ok], g[ok])
            reg = M[sv]["model_minus_emb"]
            assert abs(chk["delta"] - reg["delta"]) < 1e-8 and abs(chk["ci_item"]["ci_lo"] - reg["ci_item"]["ci_lo"]) < 1e-8 \
                and abs(chk["ci_persona"]["ci_hi"] - reg["ci_persona"]["ci_hi"]) < 1e-8, (code, sv, chk["delta"], reg["delta"])
            m = ok & sup
            R[sv] = {"n_scored": int(ok.sum()), "n_scored_superseded": int(m.sum()),
                     "whole": {"pooled": {"paraphrase": pooled_minus(e["para"][ok], p[ok], y[ok], g[ok]), "original": pooled_minus(e["orig"][ok], o[ok], y[ok], g[ok])},
                               "matched": {"paraphrase": matched_minus(rows, p, e["para"], pids_all, gp_all), "original": matched_minus(rows, o, e["orig"], pids_all, gp_all)}},
                     "superseded": {"pooled": {"paraphrase": pooled_minus(e["para"][m], p[m], y[m], g[m]), "original": pooled_minus(e["orig"][m], o[m], y[m], g[m])},
                                    "matched": {"paraphrase": matched_minus(rows, p, e["para"], pids_sup, gp_all), "original": matched_minus(rows, o, e["orig"], pids_sup, gp_all)}}}
            for scope in ("whole", "superseded"):
                for met in ("pooled", "matched"):
                    for which in ("paraphrase", "original"):
                        d = R[sv][scope][met][which]
                        ci1, ci2 = (("ci_item", "ci_persona") if met == "pooled" else ("ci_triple", "ci_persona"))
                        print(f"{code} {sv} {scope:10s} {met:7s} {which:10s} model-emb {d['delta']:+.4f} [{d[ci1]['ci_lo']:+.4f},{d[ci1]['ci_hi']:+.4f}] [{d[ci2]['ci_lo']:+.4f},{d[ci2]['ci_hi']:+.4f}]{' *' if d['both_exclude_zero'] else ''}")
        out["models"][code] = R
    path = sp.res_path("para_minus_lookup_posthoc.json")
    jdump(out, path)
    print(f"wrote {path} (population {sp.POP})")


if __name__ == "__main__":
    main()
