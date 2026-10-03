"""score_cf_pad.py -- ADDENDUM_CF_PAD sections 5-8: the scoring, run ONCE when every lane is complete or a registered halt rule has
fired. No model call. Reads cf_pad/results/lookup_vectors.json, cf_pad/rows/rows_*.jsonl, the recorded vectors
(reviews/r125/results/r125_vectors.json) and writes cf_pad/results/cf_pad_scores.json.

Endpoints: pooled AUROC (common_e1r.auroc; item-level paired bootstrap and persona-grouped paired bootstrap, 1,000 draws, seed 42) and the
matched within-triple score (W + T/2) / n, PN against PRESENT (r125_common.outcomes / wtl; triple-level and persona-grouped bootstraps of the
mean per-triple outcome difference). Reliable = both intervals exclude zero. Scopes: whole (444 items / 148 triples) and per state in the
CF-2 convention (the items of that state; supersession 264 items / 88 triples).
"""
from __future__ import annotations

import collections
import io
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cf_pad_common as C  # noqa: E402
from cf_pad_common import ARM, RES, ROWS, jdump, jload  # noqa: E402
import r125_common as R  # noqa: E402
from r125_common import boot_persona, boot_triple, outcomes, wtl  # noqa: E402

TOL = 0.05
LANES = {"MINI": "gpt-4.1-mini", "H45": "claude-haiku-4-5-20251001", "LUNA": "gpt-5.6-luna", "SOL": "gpt-5.6-sol", "OP5": "claude-opus-5"}
K_NEW = {"MINI": 5, "H45": 5, "LUNA": 5, "SOL": 5, "OP5": 1}
RECORDED_KEY = {"MINI": "MINI5_v2", "H45": "H45_v2", "LUNA": "LUNA_v2", "SOL": "SOL_v2", "OP5": "OP5_v2"}
MODELS = ("MINI", "H45", "LUNA", "SOL", "OP5")
LOOKUPS = ("LOOKUP", "LEX", "RANDTOK")
READERS = LOOKUPS + MODELS
STATE_UP = {"superseded": "SUPERSESSION", "retracted": "RETRACTION", "expired": "EXPIRY"}
SCOPES = ("whole", "superseded", "retracted", "expired")
STRONG = ("LUNA", "SOL", "OP5")
WEAK = ("MINI", "H45")


def identifier_ok(lane, served):
    if lane in ("gpt-5.6-luna", "gpt-5.6-sol"):
        return lane in (served or "")
    return (lane.split("-2025")[0] in (served or "")) or (lane in (served or ""))


def cell_for(pop):
    cell = R.Cell()
    assert cell.ids == [r["key"] for r in pop.rows], "the cell's item order differs from the population's"
    return cell


def matched(cell, v, neg="PRESENT", state=None):
    pids = cell.pids(state)
    out = outcomes(cell, v, neg, pids)
    gp = np.array([cell.pair_persona[p] for p in pids])
    res = wtl(out)
    res["ci_triple"] = boot_triple(out); res["ci_persona"] = boot_persona(out, gp)
    return res


def matched_paired(cell, va, vb, neg="PRESENT", state=None, seed=42):
    """Reader A minus reader B (or padded minus unpadded) under the matched metric: mean over triples of (outcome_A - outcome_B)."""
    pids = cell.pids(state)
    oa, ob = outcomes(cell, va, neg, pids), outcomes(cell, vb, neg, pids)
    d = oa - ob
    gp = np.array([cell.pair_persona[p] for p in pids])
    keep = ~np.isnan(d)
    it, cl = boot_triple(d, seed=seed), boot_persona(d, gp, seed=seed)
    return {"delta": float(d[keep].mean()) if keep.any() else None, "n": int(keep.sum()), "a_matched": float(oa[keep].mean()) if keep.any() else None,
            "b_matched": float(ob[keep].mean()) if keep.any() else None, "ci_triple": it, "ci_persona": cl,
            "both_exclude_zero": bool(it.get("excludes_zero") and cl.get("excludes_zero")), "agree": bool(it.get("excludes_zero") == cl.get("excludes_zero"))}


def pooled_paired(base, new, y, g, seed=42):
    """new minus base, pooled AUROC, both bootstraps (common_e1r.boot_item / boot_cluster through sweep_common)."""
    it, cl = C.boot_item(base, new, y, seed=seed), C.boot_cluster(base, new, y, g, seed=seed)
    return {"delta": float(C.auroc(new, y) - C.auroc(base, y)), "a_auroc": float(C.auroc(new, y)), "b_auroc": float(C.auroc(base, y)), "n": int(len(y)),
            "ci_item": it, "ci_persona": cl, "both_exclude_zero": bool(it.get("excludes_zero") and cl.get("excludes_zero")),
            "agree": bool(it.get("excludes_zero") == cl.get("excludes_zero"))}


def scope_mask(pop, scope):
    return np.ones(444, bool) if scope == "whole" else C.state_mask(pop.rows, scope)


def scope_state(scope):
    return None if scope == "whole" else STATE_UP[scope]


# ------------------------------------------------------------------ vectors
def lane_vectors(pop, code):
    """The padded vector (X4 collapse: mean nok over >= 3 OK draws, or the single draw for a k = 1 lane), the census, the served check."""
    path = ROWS / f"rows_{code}.jsonl"
    if not path.exists():
        return None, {"status": "lane not run"}, None
    col, census = R.collapse(path, ARM)
    lane = LANES[code]
    rows = [json.loads(l) for l in io.open(path, encoding="utf-8") if l.strip()]
    ok = [r for r in rows if r.get("status") == "OK"]
    served = collections.Counter(r.get("served_model") for r in ok)
    bad_served = [s for s in served if not identifier_ok(lane, s)]
    draws_present = sorted({int(r["draw"]) for r in rows})
    per_draw = {d: sum(1 for r in rows if int(r["draw"]) == d) for d in draws_present}
    complete_draws = [d for d, n in per_draw.items() if n == 444]
    census.update({"served": dict(served), "served_ok": not bad_served, "bad_served": bad_served, "draws_present": draws_present, "rows_per_draw": per_draw,
                   "complete_draws": complete_draws, "not_ok_share": census["not_ok"] / max(1, census["rows"]),
                   "over_1pct_not_ok": census["not_ok"] / max(1, census["rows"]) > 0.01,
                   "k_new": K_NEW[code], "k_recorded": 5})
    v = pop_vector(pop, col)
    census["distinct_values"] = int(len(np.unique(np.round(v[~np.isnan(v)], 6))))
    return v, census, rows


def pop_vector(pop, by_unit):
    return np.array([by_unit.get(r["key"], np.nan) for r in pop.rows], float)


def tied_triples(cell, v):
    n = 0
    for p in cell.pair_ids:
        a, b, c = (v[cell.pos_of[(p, ver)]] for ver in ("PN", "PRESENT", "ABSENT"))
        if not (np.isnan(a) or np.isnan(b) or np.isnan(c)) and a == b == c:
            n += 1
    return n


try:
    from scipy.stats import rankdata
except Exception:  # noqa: BLE001
    def rankdata(a):
        a = np.asarray(a, float); o = np.argsort(a, kind="mergesort"); r = np.empty(len(a), float); i = 0
        while i < len(a):
            j = i
            while j + 1 < len(a) and a[o[j + 1]] == a[o[i]]:
                j += 1
            r[o[i:j + 1]] = (i + j) / 2.0 + 1.0; i = j + 1
        return r


def spearman(x, y):
    """Spearman correlation: Pearson on average ranks; None when fewer than three pairs or a constant side."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = ~np.isnan(x) & ~np.isnan(y); x, y = x[keep], y[keep]
    if len(x) < 3:
        return None
    rx, ry = rankdata(x), rankdata(y)
    if rx.std() == 0 or ry.std() == 0:
        return None
    return float(np.corrcoef(rx, ry)[0, 1])


# ------------------------------------------------------------------ the scoring
def main():
    assert C.registration_ok(), "STOP: registration sha256 mismatch"
    lock = jload(C.BUILD / "lock.json")
    pop = C.Pop(); cell = cell_for(pop)
    y, g = pop.y, pop.g
    LV = jload(RES / "lookup_vectors.json")
    assert LV["keys"] == [r["key"] for r in pop.rows]
    rv = C.recorded_vectors()
    padded, unpadded, census = {}, {}, {}
    padded["LOOKUP"] = np.array(LV["padded"]["emb"], float); padded["LEX"] = np.array(LV["padded"]["lex"], float); padded["RANDTOK"] = np.array(LV["padded"]["randtok"], float)
    unpadded["LOOKUP"] = np.array([rv["LOOKUP_v2"][r["key"]] for r in pop.rows], float)
    unpadded["RANDTOK"] = np.array([rv["RANDTOK_v2"][r["key"]] for r in pop.rows], float)
    unpadded["LEX"] = np.array(LV["committed"]["lex"], float)
    # gates on the recorded / committed vectors, again
    assert round(float(C.auroc(unpadded["LOOKUP"], y)), 4) == C.RECORDED["LOOKUP_v2"]
    assert round(float(C.auroc(unpadded["LEX"], y)), 4) == C.LEX_V2
    assert round(float(C.auroc(unpadded["RANDTOK"], y)), 4) == C.RECORDED["RANDTOK_v2"]
    assert round(float(C.auroc(np.array(LV["committed"]["emb"], float), y)), 4) == C.RECORDED["LOOKUP_v2"]
    stops = []
    for code in MODELS:
        v, cen, rows = lane_vectors(pop, code)
        census[code] = cen
        if v is None:
            continue
        if not cen["served_ok"]:
            stops.append(f"{code}: served identifier differs ({cen['bad_served']}); rows not scored")
            continue
        if cen["over_1pct_not_ok"]:
            stops.append(f"{code}: {cen['not_ok']} of {cen['rows']} rows not OK (> 1%)")
        padded[code] = v
        unpadded[code] = np.array([rv[RECORDED_KEY[code]][r["key"]] for r in pop.rows], float)
        assert round(float(C.auroc(unpadded[code], y)), 4) == C.RECORDED[RECORDED_KEY[code]]
    unpadded["OP5_d1"] = np.array([rv_d1(r["key"]) for r in pop.rows], float) if "OP5" in padded else None
    res = {"registration_sha256": C.REG_SHA, "lock": {k: lock[k] for k in ("registration_sha256", "frozen_commit", "indexes_sha256", "texts_sha256", "recorded_gates", "lookup_gate")},
           "arm": ARM, "tol": TOL, "stops": stops, "census": census, "readers": {}, "minus_lookup": {}, "predictions": {}, "descriptive": {}}
    # ---- per reader, per scope: padded and unpadded, pooled and matched, padded minus unpadded
    for code in READERS:
        if code not in padded:
            res["readers"][code] = {"status": "lane not run or not scored"}
            continue
        p, o = padded[code], unpadded[code]
        okm = ~np.isnan(p) & ~np.isnan(o)
        rec = {"n_scored": int(okm.sum()), "n_missing": int((~okm).sum()), "k_new": K_NEW.get(code), "k_recorded": (5 if code in MODELS else None)}
        for scope in SCOPES:
            m = scope_mask(pop, scope) & okm
            st = scope_state(scope)
            rec[scope] = {"pooled": {"padded": float(C.auroc(p[m], y[m])), "unpadded": float(C.auroc(o[m], y[m])),
                                     "padded_minus_unpadded": pooled_paired(o[m], p[m], y[m], g[m])},
                          "matched": {"padded": matched(cell, p, "PRESENT", st), "unpadded": matched(cell, o, "PRESENT", st),
                                      "padded_minus_unpadded": matched_paired(cell, p, o, "PRESENT", st)},
                          "matched_vs_absent": {"padded": matched(cell, p, "ABSENT", st), "unpadded": matched(cell, o, "ABSENT", st)}}
        rec["tied_triples"] = {"padded": tied_triples(cell, p), "unpadded": tied_triples(cell, o)}
        rec["distinct_values"] = {"padded": int(len(np.unique(np.round(p[~np.isnan(p)], 6)))), "unpadded": int(len(np.unique(np.round(o[~np.isnan(o)], 6))))}
        res["readers"][code] = rec
        print(f"{code:8s} sup pooled {rec['superseded']['pooled']['unpadded']:.4f} -> {rec['superseded']['pooled']['padded']:.4f} (d {rec['superseded']['pooled']['padded_minus_unpadded']['delta']:+.4f}); "
              f"matched {rec['superseded']['matched']['unpadded']['matched']} -> {rec['superseded']['matched']['padded']['matched']}; "
              f"whole pooled {rec['whole']['pooled']['unpadded']:.4f} -> {rec['whole']['pooled']['padded']:.4f}")
    # ---- each model minus each lookup, padded lists (and the same on the unpadded lists), pooled and matched, per scope
    for code in MODELS:
        if code not in padded:
            continue
        p, o = padded[code], unpadded[code]
        rec = {}
        for lk in LOOKUPS:
            lp, lo = padded[lk], unpadded[lk]
            okm = ~np.isnan(p) & ~np.isnan(o)
            rec[lk] = {}
            for scope in SCOPES:
                m = scope_mask(pop, scope) & okm; st = scope_state(scope)
                rec[lk][scope] = {"padded": {"pooled": pooled_paired(lp[m], p[m], y[m], g[m]), "matched": matched_paired(cell, p, lp, "PRESENT", st)},
                                  "unpadded": {"pooled": pooled_paired(lo[m], o[m], y[m], g[m]), "matched": matched_paired(cell, o, lo, "PRESENT", st)}}
        res["minus_lookup"][code] = rec
        s = rec["LOOKUP"]["superseded"]
        print(f"{code:8s} minus emb lookup, sup: padded pooled {s['padded']['pooled']['delta']:+.4f} item [{s['padded']['pooled']['ci_item'].get('ci_lo', 0):+.4f},{s['padded']['pooled']['ci_item'].get('ci_hi', 0):+.4f}] "
              f"persona [{s['padded']['pooled']['ci_persona'].get('ci_lo', 0):+.4f},{s['padded']['pooled']['ci_persona'].get('ci_hi', 0):+.4f}]; matched {s['padded']['matched']['delta']:+.4f}; "
              f"unpadded pooled {s['unpadded']['pooled']['delta']:+.4f}")
    # ---- predictions (section 7): pooled AUROC, supersession slice
    P = {}

    def reliably_above(d):
        return bool(d["delta"] > 0 and d["ci_item"].get("ci_lo", -1) > 0 and d["ci_persona"].get("ci_lo", -1) > 0)

    def reliably_below(d, thr=0.0):
        return bool(d["delta"] < thr and d["ci_item"].get("ci_hi", 1) < 0 and d["ci_persona"].get("ci_hi", 1) < 0)

    l1 = {c: (res["minus_lookup"].get(c, {}).get("LOOKUP", {}).get("superseded", {}).get("padded", {}).get("pooled")) for c in STRONG}
    P["P-L1"] = {"per_model": {c: (None if d is None else {"delta": d["delta"], "ci_item": d["ci_item"], "ci_persona": d["ci_persona"], "reliably_above": reliably_above(d)}) for c, d in l1.items()},
                 "holds": all(d is not None and reliably_above(d) for d in l1.values()) if all(d is not None for d in l1.values()) else None}
    l2 = {c: (res["minus_lookup"].get(c, {}).get("LOOKUP", {}).get("superseded", {}).get("padded", {}).get("pooled")) for c in WEAK}
    P["P-L2"] = {"per_model": {c: (None if d is None else {"delta": d["delta"], "ci_item": d["ci_item"], "ci_persona": d["ci_persona"], "reliably_above": reliably_above(d)}) for c, d in l2.items()},
                 "holds": all(d is not None and not reliably_above(d) for d in l2.values()) if all(d is not None for d in l2.values()) else None}
    lk = res["readers"]["LOOKUP"]["superseded"]["pooled"]["padded_minus_unpadded"]
    P["P-L3"] = {"lookup_padded_minus_unpadded": {"delta": lk["delta"], "ci_item": lk["ci_item"], "ci_persona": lk["ci_persona"]},
                 "holds": bool(reliably_below(lk, -TOL))}
    l4 = {}
    for c in STRONG:
        if c in res["readers"] and "superseded" in res["readers"][c]:
            dm = res["readers"][c]["superseded"]["pooled"]["padded_minus_unpadded"]["delta"]
            l4[c] = {"model_delta": dm, "lookup_delta": lk["delta"], "loses_less": bool(dm > lk["delta"])}
        else:
            l4[c] = None
    P["P-L4"] = {"per_model": l4, "holds": all(v is not None and v["loses_less"] for v in l4.values()) if all(v is not None for v in l4.values()) else None}
    for k, v in P.items():
        v["text"] = f"{k} {'HOLDS' if v['holds'] else ('FAILS' if v['holds'] is False else 'NOT DECIDABLE (a lane missing)')}"
        print(v["text"])
    res["predictions"] = P
    # ---- descriptive: the target's position against each reader (supersession triples)
    pos = jload(C.BUILD / "pads.json")["target_position"]
    sup_pids = cell.pids("SUPERSESSION")
    ranks = np.array([pos[p] for p in sup_pids], float)
    D = {"n_triples": len(sup_pids), "rank_histogram": lock["target_position"]["histogram"], "by_reader": {}}
    tenth = np.ceil(ranks / 6.0).astype(int)
    for code in READERS:
        if code not in padded:
            continue
        v = padded[code]
        out = outcomes(cell, v, "PRESENT", sup_pids)
        pn = np.array([v[cell.pos_of[(p, "PN")]] for p in sup_pids], float)
        D["by_reader"][code] = {"spearman_rank_vs_pn_score": spearman(ranks, pn), "spearman_rank_vs_outcome": spearman(ranks, out),
                                "matched_by_tenth": {str(t): (float(np.nanmean(out[tenth == t])) if (tenth == t).any() else None) for t in range(1, 11)},
                                "n_by_tenth": {str(t): int((tenth == t).sum()) for t in range(1, 11)}}
    res["descriptive"]["target_position"] = D
    if unpadded.get("OP5_d1") is not None and "OP5" in padded:
        d1 = unpadded["OP5_d1"]; p = padded["OP5"]
        okm = ~np.isnan(p) & ~np.isnan(d1)
        res["descriptive"]["opus_recorded_draw1"] = {sc: {"pooled_unpadded_d1": float(C.auroc(d1[scope_mask(pop, sc) & okm], y[scope_mask(pop, sc) & okm])),
                                                          "padded_minus_d1_pooled": pooled_paired(d1[scope_mask(pop, sc) & okm], p[scope_mask(pop, sc) & okm], y[scope_mask(pop, sc) & okm], g[scope_mask(pop, sc) & okm]),
                                                          "matched_unpadded_d1": matched(cell, d1, "PRESENT", scope_state(sc))["matched"]} for sc in ("whole", "superseded")}
    # ---- seed spot-check 43-46 on the registered pooled differences (supersession slice)
    spot = {}
    m = scope_mask(pop, "superseded")
    for code in MODELS:
        if code in padded:
            spot[f"{code}_minus_LOOKUP"] = {str(sd): {"item": C.boot_item(padded["LOOKUP"][m], padded[code][m], y[m], seed=sd).get("excludes_zero"),
                                                      "persona": C.boot_cluster(padded["LOOKUP"][m], padded[code][m], y[m], g[m], seed=sd).get("excludes_zero")} for sd in (43, 44, 45, 46)}
    for code in READERS:
        if code in padded:
            spot[f"{code}_padded_minus_unpadded"] = {str(sd): {"item": C.boot_item(unpadded[code][m], padded[code][m], y[m], seed=sd).get("excludes_zero"),
                                                               "persona": C.boot_cluster(unpadded[code][m], padded[code][m], y[m], g[m], seed=sd).get("excludes_zero")} for sd in (43, 44, 45, 46)}
    res["descriptive"]["seed_spot_check"] = spot
    # ---- spend
    import run_cf_pad as RUN
    res["spend"] = {v: {"usd": round(RUN.spent(v)[0], 4), "parts": RUN.spent(v)[1], "cap": RUN.CAPS[v]} for v in ("anthropic", "openai")}
    res["probes"] = jload(C.BUILD / "probes.json") if (C.BUILD / "probes.json").exists() else {}
    jdump(res, RES / "cf_pad_scores.json")
    print(f"wrote {RES / 'cf_pad_scores.json'}; STOPs: {stops or 'none'}")
    return res


_RV = {}


def rv_d1(key):
    if not _RV:
        _RV.update(jload(C.ROOT / "reviews" / "r125" / "results" / "r125_vectors.json")["readers"]["OP5_v2_d1"]["vector"])
    v = _RV.get(key)
    return np.nan if v is None else v


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
