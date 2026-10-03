"""R76 NS-5 scorer -- Haiku 4.5 lane on the authorship-matched cell (ADDENDUM_R76 §A3).

Committed estimators only, identical to the R75 X5 scorer: score_e1.auroc / score_e1.boot
(paired, 1,000 draws, seed 42, single-class draws discarded) and score_ladder.auroc_ci
(one-sample). Haiku is a k=5 lane, so it is scored exactly as the Opus 5 lane was:
per-item mean over parse-OK draws, MIN_DRAWS=3.

NS-5 is DESCRIPTIVE ("reports"). It adjudicates nothing: XV-1's registered failed verdict
is untouched in every branch. The branch is chosen from the blind NOK one-sample interval:
  (i)   ci_hi < 0.50                          -> prior survives authorship matching here
  (ii)  includes 0.50 and point >= 0.45       -> consistent with artifact attenuation
  (iii) includes 0.50 and point <  0.45       -> indeterminate at n=36
  (iv)  ci_lo > 0.50                          -> NOT a frozen branch; A5.6 contradiction
                                                 rule fires (own cell + new D-entry)
"""
import collections, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
from score_e1 import auroc, boot
from score_ladder import auroc_ci

X5 = ROOT / "r74" / "x5"
X6 = ROOT / "r74" / "x6"
R = json.load(open(X5 / "x5_render.json", encoding="utf-8"))
ITEMS = sorted(R["rows"], key=lambda r: r["item_id"])
IDS = [it["item_id"] for it in ITEMS]
Y_NOK = {it["item_id"]: (1 if it["label"] == "PN" else 0) for it in ITEMS}
Y_FOK = {it["item_id"]: (0 if it["label"] == "ABSENT" else 1) for it in ITEMS}
MIN_DRAWS = 3

rows = [json.loads(l) for l in open(X6 / "rows_H45.jsonl", encoding="utf-8")]
by = collections.defaultdict(dict)
fails, total, spend = collections.Counter(), collections.Counter(), 0.0
for r in rows:
    total[r["arm"]] += 1
    spend += r.get("usd", 0.0)
    if r.get("status") != "OK":
        fails[r["arm"]] += 1
        continue
    by[(r["item_id"], r["arm"])][r["draw"]] = r

scores, stab = {}, {}
for arm in ("BLIND", "INDEXED-TRUE"):
    scores[arm] = {"fok": {}, "nok": {}}
    sds, ident, n_items = [], 0, 0
    for iid in IDS:
        draws = by.get((iid, arm), {})
        ok = sorted(draws)
        if len(ok) < MIN_DRAWS:
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
                 "items_all_draws_identical": ident if sds else None}

out = {"registration": "ADDENDUM_R76 §A3 @ 692e379bdc; branches amended pre-launch "
                       "per D-R74-14; batch msgbatch_018hCZkAZFxg6iwz92rKKaSM",
       "lane": "claude-haiku-4-5-20251001", "cell": R["cell"],
       "spend_usd": round(spend, 4),
       "parse_failures": {a: {"failed": fails[a], "of": total[a],
                              "rate": (fails[a] / total[a]) if total[a] else 0.0}
                          for a in ("BLIND", "INDEXED-TRUE")},
       "stability": stab, "cells": {}}

for judgment, Y in (("nok", Y_NOK), ("fok", Y_FOK)):
    ks = [i for i in IDS if i in scores["BLIND"][judgment]
          and i in scores["INDEXED-TRUE"][judgment]]
    y = [Y[i] for i in ks]
    b = [scores["BLIND"][judgment][i] for i in ks]
    v = [scores["INDEXED-TRUE"][judgment][i] for i in ks]
    deg = {}
    for name, arr in (("blind", b), ("indexed", v)):
        cnt = collections.Counter(arr)
        deg[name] = {"distinct": len(cnt), "modal_share": max(cnt.values()) / len(arr)}
    out["cells"][judgment] = {"n": len(ks), "pos": sum(y),
                              "blind_auroc": auroc(b, y), "indexed_auroc": auroc(v, y),
                              "blind_one_sample": auroc_ci(b, y),
                              "paired_delta": boot(b, v, y), "degeneracy": deg}

n = out["cells"]["nok"]
o = n["blind_one_sample"]
point, lo, hi = n["blind_auroc"], o["ci_lo"], o["ci_hi"]
if lo > 0.50:
    branch = "iv-UNANTICIPATED"
elif hi < 0.50:
    branch = "i"
elif point >= 0.45:
    branch = "ii"
else:
    branch = "iii"
out["NS5_branch"] = branch
out["NS5_blind_includes_chance"] = bool(o["includes_0.50"])
out["XV1_verdict"] = "untouched (registered failed verdict is never re-adjudicated)"

json.dump(out, open(X6 / "x6_ns5_scores.json", "w", encoding="utf-8"), indent=1,
          sort_keys=True, default=float)

f = out["cells"]["fok"]
d, od = n["paired_delta"], f["paired_delta"]
print(f"== NS-5 Haiku 4.5  spend ${out['spend_usd']}  parse_fail "
      f"B {fails['BLIND']}/{total['BLIND']} I {fails['INDEXED-TRUE']}/{total['INDEXED-TRUE']}")
print(f"  NOK n={n['n']} pos={n['pos']}  blind {point:.4f} [{lo:.4f},{hi:.4f}] "
      f"includes.5={o['includes_0.50']}  indexed {n['indexed_auroc']:.4f}  "
      f"delta {d['mean']:+.4f} [{d['ci_lo']:+.4f},{d['ci_hi']:+.4f}]")
print(f"  FOK (descriptive) n={f['n']} pos={f['pos']}  blind {f['blind_auroc']:.4f} "
      f"indexed {f['indexed_auroc']:.4f}  delta {od['mean']:+.4f} "
      f"[{od['ci_lo']:+.4f},{od['ci_hi']:+.4f}]")
print(f"  degeneracy NOK: blind distinct {n['degeneracy']['blind']['distinct']} "
      f"modal {n['degeneracy']['blind']['modal_share']:.2f}; indexed distinct "
      f"{n['degeneracy']['indexed']['distinct']} modal {n['degeneracy']['indexed']['modal_share']:.2f}")
print(f"  >>> NS-5 BRANCH {branch}")
