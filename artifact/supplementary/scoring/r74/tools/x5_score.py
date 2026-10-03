"""R75 X5 -- scorer for the authorship-matched slice (ADDENDUM_R74 SX5; prereg
E1-NS SS3). Committed estimators only: score_e1.auroc / score_e1.boot (paired,
1,000 draws, seed 42, single-class draws discarded) and score_ladder.auroc_ci
(one-sample). Mini: k=1 primary (draw 1), draws 1-3 are the stability sample.
Opus 5: per-item mean over parse-OK draws, MIN_DRAWS=3.

NS-1 per lane: blind NOK one-sample CI includes 0.50.
NS-2 per lane: indexed-blind NOK delta > 0 with paired CI excluding 0.
FAILS texts are frozen in the prereg (gate and verdict only).
"""
import collections, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
from score_e1 import auroc, boot
from score_ladder import auroc_ci

X5 = ROOT / "r74" / "x5"
R = json.load(open(X5 / "x5_render.json", encoding="utf-8"))
ITEMS = sorted(R["rows"], key=lambda r: r["item_id"])
IDS = [it["item_id"] for it in ITEMS]
Y_NOK = {it["item_id"]: (1 if it["label"] == "PN" else 0) for it in ITEMS}
Y_FOK = {it["item_id"]: (0 if it["label"] == "ABSENT" else 1) for it in ITEMS}

LANES = {"MINI": dict(primary="k1", min_draws=None),
         "OP5":  dict(primary="mean", min_draws=3)}

def load(code):
    rows = [json.loads(l) for l in open(X5 / f"rows_{code}.jsonl", encoding="utf-8")]
    return rows

def lane_scores(code):
    rows = load(code)
    cfg = LANES[code]
    by = collections.defaultdict(dict)   # (item, arm) -> {draw: row}
    fails = collections.Counter()
    total = collections.Counter()
    spend = 0.0
    for r in rows:
        total[r["arm"]] += 1
        spend += r.get("usd", 0.0)
        if r.get("status") != "OK":
            fails[r["arm"]] += 1
            continue
        by[(r["item_id"], r["arm"])][r["draw"]] = r
    scores = {}   # arm -> judgment -> {item: value}
    stab = {}
    for arm in ("BLIND", "INDEXED-TRUE"):
        scores.setdefault(arm, {"fok": {}, "nok": {}})
        sds = []
        ident = 0
        n_items = 0
        for iid in IDS:
            draws = by.get((iid, arm), {})
            ok = sorted(draws)
            if not ok:
                continue
            if cfg["primary"] == "k1":
                if 1 not in draws:
                    continue
                for j in ("fok", "nok"):
                    scores[arm][j][iid] = draws[1][j]
            else:
                if len(ok) < cfg["min_draws"]:
                    continue
                for j in ("fok", "nok"):
                    scores[arm][j][iid] = sum(draws[d][j] for d in ok) / len(ok)
            vals = [draws[d]["nok"] for d in ok]
            n_items += 1
            if len(vals) > 1:
                sds.append(statistics.pstdev(vals))
                if len(set(vals)) == 1:
                    ident += 1
        stab[arm] = {"items_scored": n_items,
                     "mean_per_item_nok_sd": (sum(sds) / len(sds)) if sds else None,
                     "items_all_draws_identical": ident if sds else None,
                     "draws_per_item": len(next(iter(by.values()))) if by else 0}
    out = {"lane": code, "spend_usd": round(spend, 4),
           "parse_failures": {a: {"failed": fails[a], "of": total[a],
                                  "rate": fails[a] / total[a] if total[a] else 0.0,
                                  "flagged": (fails[a] / total[a] > 0.05) if total[a] else False}
                              for a in ("BLIND", "INDEXED-TRUE")},
           "stability": stab, "cells": {}}
    if stab["BLIND"]["mean_per_item_nok_sd"] not in (None, 0) and \
       stab["INDEXED-TRUE"]["mean_per_item_nok_sd"] is not None:
        out["dispersion_ratio_blind_over_indexed"] = (
            stab["INDEXED-TRUE"]["mean_per_item_nok_sd"] /
            stab["BLIND"]["mean_per_item_nok_sd"]
            if stab["BLIND"]["mean_per_item_nok_sd"] else None)
    for judgment, Y in (("nok", Y_NOK), ("fok", Y_FOK)):
        ks = [i for i in IDS if i in scores["BLIND"][judgment]
              and i in scores["INDEXED-TRUE"][judgment]]
        y = [Y[i] for i in ks]
        b = [scores["BLIND"][judgment][i] for i in ks]
        v = [scores["INDEXED-TRUE"][judgment][i] for i in ks]
        one = auroc_ci(b, y)
        delta = boot(b, v, y)
        deg = {}
        for name, arr in (("blind", b), ("indexed", v)):
            cnt = collections.Counter(arr)
            deg[name] = {"distinct": len(cnt),
                         "modal_share": max(cnt.values()) / len(arr)}
        out["cells"][judgment] = {
            "n": len(ks), "pos": sum(y),
            "blind_auroc": auroc(b, y), "indexed_auroc": auroc(v, y),
            "blind_one_sample": one, "paired_delta": delta,
            "degeneracy": deg}
    nok = out["cells"]["nok"]
    out["NS1_blind_at_chance"] = bool(nok["blind_one_sample"]["includes_0.50"])
    out["NS2_delta_excludes_zero_positive"] = bool(
        nok["paired_delta"]["ci_lo"] > 0)
    return out

res = {"registration": "ADDENDUM_R74 SX5 @ 35f8416a55; launch per D-R74-10",
       "cell": R["cell"], "lanes": {}}
for code in ("MINI", "OP5"):
    res["lanes"][code] = lane_scores(code)
oracle = json.load(open(X5 / "x5_oracle.json", encoding="utf-8"))
res["index_oracle_n36"] = {"auroc": oracle["auroc"], "pn_named": oracle["pn_named"],
                           "registered_99cell_value": 0.5379}
json.dump(res, open(X5 / "x5_scores.json", "w", encoding="utf-8"), indent=1,
          sort_keys=True, default=float)

for code, L in res["lanes"].items():
    n = L["cells"]["nok"]
    f = L["cells"]["fok"]
    print(f"== {code}  spend ${L['spend_usd']}  parse_fail "
          f"B {L['parse_failures']['BLIND']['failed']}/{L['parse_failures']['BLIND']['of']} "
          f"I {L['parse_failures']['INDEXED-TRUE']['failed']}/{L['parse_failures']['INDEXED-TRUE']['of']}")
    o = n["blind_one_sample"]
    d = n["paired_delta"]
    print(f"  NOK n={n['n']} pos={n['pos']}  blind {n['blind_auroc']:.4f} "
          f"[{o['ci_lo']:.4f},{o['ci_hi']:.4f}] includes.5={o['includes_0.50']}  "
          f"indexed {n['indexed_auroc']:.4f}  delta {d['mean']:+.4f} "
          f"[{d['ci_lo']:+.4f},{d['ci_hi']:+.4f}]")
    print(f"  NS-1 {'HOLDS' if L['NS1_blind_at_chance'] else 'FAILS'}   "
          f"NS-2 {'HOLDS' if L['NS2_delta_excludes_zero_positive'] else 'FAILS'}")
    od = f["paired_delta"]
    print(f"  FOK (descriptive) n={f['n']} pos={f['pos']}  blind {f['blind_auroc']:.4f} "
          f"indexed {f['indexed_auroc']:.4f}  delta {od['mean']:+.4f} "
          f"[{od['ci_lo']:+.4f},{od['ci_hi']:+.4f}]")
    print(f"  degeneracy NOK: blind distinct {n['degeneracy']['blind']['distinct']} "
          f"modal {n['degeneracy']['blind']['modal_share']:.2f}; "
          f"indexed distinct {n['degeneracy']['indexed']['distinct']} "
          f"modal {n['degeneracy']['indexed']['modal_share']:.2f}")
print("oracle n36:", res["index_oracle_n36"])
