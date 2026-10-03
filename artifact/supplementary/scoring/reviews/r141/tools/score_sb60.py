# -*- coding: utf-8 -*-
"""score_sb60.py -- R141 Phase 2 (ADDENDUM_R141_SB60, frozen f224177; the run 2588717): every reader on PN-60 against SB-60, matched (primary) and pooled
(secondary), each model minus the name lookup on both metrics with the 95% (reliable) and 90% (equivalent within 0.05) intervals from the same draws, the
SB-60 vs padded-PRESENT component (descriptive), the four predictions, the fired branch, and seeds 43 to 46 on every registered difference. $0, no model call.

Vectors: the SB-60 model rows collapse as every five-draw lane does (r125_common.collapse: the mean nok over >= 3 OK draws); PN-60 and PRESENT model rows
are R136's recorded padded rows (cf_pad score_cf_pad.lane_vectors); the no-model readers as reviews/r141/results/nomodel_sb60.json computed them (recomputed
here and asserted equal). Writes reviews/r141/results/scores_sb60.json. Usage: python reviews/r141/tools/score_sb60.py
"""
from __future__ import annotations

import collections
import io
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[3]
for p in ("reviews/r125/tools", "cf_pad/tools", "pad_probe/tools", "nb6_sweep/tools", "e1r_robustness/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
import common_e1r  # noqa: E402
import r125_common  # noqa: E402
import r125_t45_score as T  # noqa: E402
import score_cf_pad as SP  # noqa: E402
import pad_common as PC  # noqa: E402
from sweep_common import emb_cached  # noqa: E402

OUT = ROOT / "reviews" / "r141" / "results" / "scores_sb60.json"
TOL = 0.05


def _summ(d):
    d = np.asarray(d, float)
    if not len(d):
        return {"n_draws": 0}
    lo, hi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    return {"n_draws": int(len(d)), "mean": float(d.mean()), "ci_lo": lo, "ci_hi": hi, "excludes_zero": bool(lo > 0 or hi < 0),
            "ci90_lo": float(np.percentile(d, 5.0)), "ci90_hi": float(np.percentile(d, 95.0))}


common_e1r._summarise = _summ
r125_common._summarise = _summ
C = r125_common


def J(rel):
    return json.load(open(ROOT / rel, encoding="utf-8"))


def outc(a, b):
    o = np.where(a > b, 1.0, np.where(a == b, 0.5, 0.0))
    o[np.isnan(a) | np.isnan(b)] = np.nan
    return o


def flags(a, b):
    rel = bool(a["excludes_zero"] and b["excludes_zero"])
    eq = all(-TOL <= x <= TOL for x in (a["ci90_lo"], a["ci90_hi"], b["ci90_lo"], b["ci90_hi"]))
    return rel, eq


def matched_diff(pa, sa, pb, sb, gp, seed=42):
    d = outc(pa, sa) - outc(pb, sb)
    it, cl = C.boot_triple(d, seed=seed), C.boot_persona(d, gp, seed=seed)
    rel, eq = flags(it, cl)
    return {"delta": float(np.nanmean(d)), "ci_triple": it, "ci_persona": cl, "reliable": rel, "equivalent": eq}


def pooled_diff(pa, sa, pb, sb, gp, seed=42):
    y = np.r_[np.ones(len(pa)), np.zeros(len(sa))].astype(int)
    new, base, g = np.r_[pa, sa], np.r_[pb, sb], np.r_[gp, gp]
    it, cl = common_e1r.boot_item(base, new, y, seed=seed), common_e1r.boot_cluster(base, new, y, g, seed=seed)
    rel, eq = flags(it, cl)
    return {"delta": float(common_e1r.auroc(new, y) - common_e1r.auroc(base, y)), "a_auroc": float(common_e1r.auroc(new, y)), "b_auroc": float(common_e1r.auroc(base, y)),
            "ci_item": it, "ci_persona": cl, "reliable": rel, "equivalent": eq}


def pooled_single(pa, sa, gp):
    y = np.r_[np.ones(len(pa)), np.zeros(len(sa))].astype(int)
    s, g = np.r_[pa, sa], np.r_[gp, gp]
    return {"auroc": float(common_e1r.auroc(s, y)), "ci_persona": common_e1r.boot_cluster_single(s, y, g)}


def main():
    cell = C.Cell()
    B = J("reviews/r141/build/build_sb60.json")
    pad = J("cf_pad/build/texts.json")
    LV = J("cf_pad/results/lookup_vectors.json")
    pos = {k: i for i, k in enumerate(LV["keys"])}
    rows = B["rows"]
    pids = [r["pair_id"] for r in rows]
    gp = np.array([cell.pair_persona[p] for p in pids])
    qs = [r["question"] for r in rows]
    V = {}
    # the name lookup (the registered comparator): PN-60 and PRESENT recorded (R136), SB-60 on its printed list
    # all three versions computed the same way in one process (emb_cached), as the registration's recorded values were: a pad name that is the maximum in both
    # versions then gives bit-identical scores, so the pair ties exactly. Mixing the stored R136 floats (rounded in JSON) with fresh ones breaks those ties at
    # the last digit (62/21/5 instead of 57/31/0); the stored vectors are only the equality check, at 1e-6.
    lk = {}
    for v in ("PN", "PRESENT", "SB60"):
        rr = [{"key": f"{p}|{v}", "question": q} for p, q in zip(pids, qs)]
        text = (lambda p: B["texts"][f"{p}|SB60"]) if v == "SB60" else (lambda p, v=v: pad[f"{p}|{v}"])
        lk[v] = emb_cached(rr, {f"{p}|{v}": PC.committed_names(text(p)) for p in pids})
    for v in ("PN", "PRESENT"):
        assert np.allclose(lk[v], np.array([LV["padded"]["emb"][pos[f"{p}|{v}"]] for p in pids], float), atol=1e-6)
    V["Name lookup"] = lk
    NM = J("reviews/r141/results/nomodel_sb60.json")["readers"]
    w = C.wtl(outc(lk["PN"], lk["SB60"]))
    rec = NM["Name lookup (embedding)"]["pn60_vs_sb60"]
    assert (w["W"], w["T"], w["L"]) == (rec["W"], rec["T"], rec["L"]), ("the lookup does not reproduce its recorded W/T/L", w, rec)
    # the models: PN-60 / PRESENT from R136's recorded padded rows; SB-60 from the R141 rows
    pop = SP.C.Pop()
    kpos = {r["key"]: i for i, r in enumerate(pop.rows)}
    census = {}
    for code, name, lane in (("LUNA", "GPT-5.6 Luna", "SB60-LUNA"), ("SOL", "GPT-5.6 Sol", "SB60-SOL"), ("MINI", "GPT-4.1 mini", "SB60-MINI")):
        pv, cen, _ = SP.lane_vectors(pop, code)
        path = ROOT / "reviews" / "r141" / "rows" / f"rows_{lane}.jsonl"
        col, c2 = C.collapse(path, "SB60")
        allrows = [json.loads(l) for l in io.open(path, encoding="utf-8") if l.strip()]
        served = collections.Counter(r.get("served_model") for r in allrows)
        census[name] = {"rows": len(allrows), "ok": sum(r.get("status") == "OK" for r in allrows), "served": dict(served), "usd": round(sum(float(r.get("usd") or 0) for r in allrows), 4),
                        "draws_per_unit": c2["draws_per_unit"]}
        V[name] = {"PN": np.array([pv[kpos[f"{p}|PN"]] for p in pids], float), "PRESENT": np.array([pv[kpos[f"{p}|PRESENT"]] for p in pids], float),
                   "SB60": np.array([col[f"{p}|SB60"] for p in pids], float)}
    out = {"meta": {"script": "reviews/r141/tools/score_sb60.py", "model_calls": 0, "registration": "ADDENDUM_R141_SB60 f224177 sha 4fc25a8b", "run": "2588717", "n_pairs": len(pids),
                    "n_boot": 1000, "seed": 42, "census": census}, "readers": {}, "minus_lookup": {}, "predictions": {}, "seeds": {}}
    for name, d in V.items():
        out["readers"][name] = {"pn60_vs_sb60": T.matched(d["PN"], d["SB60"], gp), "pooled_pn60_vs_sb60": pooled_single(d["PN"], d["SB60"], gp),
                                "sb60_vs_present": T.matched(d["SB60"], d["PRESENT"], gp), "pn60_vs_present": T.matched(d["PN"], d["PRESENT"], gp)}
    L = V["Name lookup"]
    for name in ("GPT-5.6 Luna", "GPT-5.6 Sol", "GPT-4.1 mini"):
        d = V[name]
        out["minus_lookup"][name] = {"matched": matched_diff(d["PN"], d["SB60"], L["PN"], L["SB60"], gp), "pooled": pooled_diff(d["PN"], d["SB60"], L["PN"], L["SB60"], gp)}
        out["seeds"][name] = {str(s): {"matched": {k: matched_diff(d["PN"], d["SB60"], L["PN"], L["SB60"], gp, seed=s)[k] for k in ("reliable", "equivalent")},
                                       "pooled": {k: pooled_diff(d["PN"], d["SB60"], L["PN"], L["SB60"], gp, seed=s)[k] for k in ("reliable", "equivalent")}} for s in (43, 44, 45, 46)}
    ML = out["minus_lookup"]
    above = lambda n: ML[n]["matched"]["reliable"] and ML[n]["matched"]["delta"] > 0
    P = out["predictions"]
    P["P-S1"] = {"text": "Luna exceeds the name lookup on PN-60 vs SB-60 with both intervals clear of zero", "holds": above("GPT-5.6 Luna"), "pooled_reading": ML["GPT-5.6 Luna"]["pooled"]["reliable"] and ML["GPT-5.6 Luna"]["pooled"]["delta"] > 0}
    P["P-S2"] = {"text": "Sol exceeds the name lookup on PN-60 vs SB-60 with both intervals clear of zero", "holds": above("GPT-5.6 Sol"), "pooled_reading": ML["GPT-5.6 Sol"]["pooled"]["reliable"] and ML["GPT-5.6 Sol"]["pooled"]["delta"] > 0}
    P["P-S3"] = {"text": "mini does not reliably exceed the name lookup", "holds": not above("GPT-4.1 mini"), "pooled_reading": not (ML["GPT-4.1 mini"]["pooled"]["reliable"] and ML["GPT-4.1 mini"]["pooled"]["delta"] > 0)}
    s4 = {n: {"matched": out["readers"][n]["pn60_vs_sb60"]["matched"], "persona_lo": out["readers"][n]["pn60_vs_sb60"]["ci_persona"]["ci_lo"]} for n in ("GPT-5.6 Luna", "GPT-5.6 Sol")}
    P["P-S4"] = {"text": "each of Luna and Sol at or above 0.80 matched on PN-60 vs SB-60 with the persona interval above 0.50", "per_model": s4,
                 "holds": all(v["matched"] >= 0.80 and v["persona_lo"] > 0.50 for v in s4.values())}
    s1, s2 = P["P-S1"]["holds"], P["P-S2"]["holds"]
    out["branch"] = "B-i" if (s1 and s2) else ("B-iii" if not (s1 or s2) else "B-ii")
    out["seed_reading_changes"] = [(n, s, m, k) for n, dd in out["seeds"].items() for s, v in dd.items() for m in ("matched", "pooled") for k in ("reliable", "equivalent")
                                   if v[m][k] != ML[n][m][k]]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    C.jdump(out, OUT)
    for name, r in out["readers"].items():
        m = r["pn60_vs_sb60"]
        print(f"{name:14s} PN-60 vs SB-60 {m['W']:2d}/{m['T']:2d}/{m['L']:2d} {m['matched']:.4f} [{m['ci_triple']['ci_lo']:.4f},{m['ci_triple']['ci_hi']:.4f}] [{m['ci_persona']['ci_lo']:.4f},{m['ci_persona']['ci_hi']:.4f}] "
              f"pooled {r['pooled_pn60_vs_sb60']['auroc']:.4f} | SB-60 vs PRESENT {r['sb60_vs_present']['matched']:.4f}")
    for name, d in ML.items():
        for met in ("matched", "pooled"):
            x = d[met]; a = x["ci_triple"] if met == "matched" else x["ci_item"]; b = x["ci_persona"]
            print(f"  {name} minus lookup, {met}: {x['delta']:+.4f} [{a['ci_lo']:+.4f},{a['ci_hi']:+.4f}] [{b['ci_lo']:+.4f},{b['ci_hi']:+.4f}] reliable={x['reliable']} equivalent={x['equivalent']}")
    for k, v in P.items():
        print(k, "HOLDS" if v["holds"] else "FAILS", {kk: vv for kk, vv in v.items() if kk not in ("text",)})
    print("branch:", out["branch"], "| seed reading changes:", out["seed_reading_changes"])


if __name__ == "__main__":
    main()
