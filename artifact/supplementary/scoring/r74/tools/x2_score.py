"""R74 X2 scorer (ADDENDUM_R74 SX2 @ 35f8416a55).

Paired against the COMMITTED blind rows; intact arm = committed INDEXED-TRUE rows.
Recovery rule (frozen, verbatim): an arm "recovers" if its indexed-minus-blind AUROC CI
excludes zero on the positive side OR the inversion delta shrinks by >=50% with CI
excluding the intact delta. Item-level primary; persona-clustered sensitivity reported.
X2b-names-removed is byte-identical to intact (no ablation site): scored as the committed
intact rows, flagged by construction.
"""
import json, pathlib, sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
from score_e1 import auroc, boot

SC = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}
E1 = ROOT / "e1_metamemory"
X2 = ROOT / "r74" / "x2"
items = {i["item_id"]: i for i in json.load(open(E1 / "build" / "items_final.json", encoding="utf-8"))}
main = json.load(open(E1 / "elicitation_main.json", encoding="utf-8"))
blind_by_q = {r["tag"]: r for r in main if r["arm"] == "BLIND" and r["status"] == "OK"}
intact = {r["tag"]: r for r in main if r["arm"] == "INDEXED-TRUE" and r["status"] == "OK"}
qmap = {r["tag"]: r["question"] for r in main if r["arm"] != "BLIND"}
x2rows = json.load(open(X2 / "x2_elicitation.json", encoding="utf-8"))
by_arm = {}
for r in x2rows:
    if r["status"] == "OK":
        by_arm.setdefault(r["arm"], {})[r["tag"]] = r

ARMS = ("X2a-count-removed", "X2b-names-removed", "X2c-markers-removed", "X2d-count-markers-removed")

def pop_items(backend):
    return sorted(t for t, it in items.items()
                  if it.get("label", it["label_pre"]) in SC and it["backend"] == backend)

def paired(backend, arm_rows):
    tags, b, a, y, personas = [], [], [], [], []
    for t in pop_items(backend):
        br = blind_by_q.get(qmap.get(t))
        ar = arm_rows.get(t)
        if not br or not ar or br["fok"] is None or ar["fok"] is None:
            continue
        tags.append(t); b.append(br["fok"]); a.append(ar["fok"])
        y.append(0 if items[t].get("label", items[t]["label_pre"]) == "ABSENT" else 1)
        personas.append(items[t]["persona"])
    return tags, np.array(b, float), np.array(a, float), np.array(y, int), personas

def cluster_ci(b, a, y, personas, n=1000, seed=42):
    rng = np.random.default_rng(seed)
    ps = sorted(set(personas))
    byp = {p: np.array([i for i, q in enumerate(personas) if q == p]) for p in ps}
    ds = []
    for _ in range(n):
        take = np.concatenate([byp[ps[j]] for j in rng.integers(0, len(ps), len(ps))])
        yy = y[take]
        if len(set(yy)) < 2:
            continue
        ds.append(auroc(a[take], yy) - auroc(b[take], yy))
    return [float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5))] if ds else None

res = {"registration": "ADDENDUM_R74 SX2 @ 35f8416a55", "backends": {}}
for backend in ("mem0", "amem"):
    out = {}
    _, b0, a0, y0, _ = paired(backend, intact)
    intact_delta = auroc(a0, y0) - auroc(b0, y0)
    out["intact_reproduction"] = {"n": len(y0), "blind_auroc": auroc(b0, y0),
                                  "indexed_auroc": auroc(a0, y0), "delta": intact_delta}
    for arm in ARMS:
        rows = intact if arm == "X2b-names-removed" else by_arm.get(arm, {})
        tags, b, a, y, personas = paired(backend, rows)
        d = auroc(a, y) - auroc(b, y)
        bt = boot(b, a, y)
        cl = cluster_ci(b, a, y, personas)
        r1 = bt["ci_lo"] > 0
        shrink = abs(d) <= 0.5 * abs(intact_delta)
        excl_intact = not (bt["ci_lo"] <= intact_delta <= bt["ci_hi"])
        r2 = shrink and excl_intact
        out[arm] = {"n": len(y), "arm_auroc": auroc(a, y), "blind_auroc": auroc(b, y),
                    "delta": d, "boot": bt, "clustered_ci": cl,
                    "recovers_R1_positive": bool(r1),
                    "recovers_R2_shrink50_excl_intact": bool(r2),
                    "recovers": bool(r1 or r2),
                    "by_construction_equals_intact": arm == "X2b-names-removed"}
    res["backends"][backend] = out

rec = {(a, bk) for a in ARMS for bk, o in res["backends"].items() if o[a]["recovers"]}
res["recovering_arm_store_pairs"] = sorted(f"{a}@{bk}" for a, bk in rec)
single_channels = {"X2a-count-removed", "X2b-names-removed", "X2c-markers-removed"}
rec_channels = {a for a, _ in rec if a in single_channels}
rec_compound = {a for a, _ in rec if a not in single_channels}
stores_per = {a: {bk for aa, bk in rec if aa == a} for a in {a for a, _ in rec}}
# Branch (i) requires exactly one SINGLE channel recovering, consistently on both stores,
# and nothing else; the compound arm or a one-store-only recovery is partial by the frozen
# wording ("multiple/partial").
if not rec:
    res["branch"] = "iii-nothing-separates"
elif (len(rec_channels) == 1 and not rec_compound
      and stores_per[next(iter(rec_channels))] == set(res["backends"])):
    res["branch"] = "i-single-channel"
else:
    res["branch"] = "ii-multiple-partial"
json.dump(res, open(X2 / "x2_scores.json", "w", encoding="utf-8"), indent=1, sort_keys=True,
          default=float)
print(json.dumps({"branch": res["branch"],
                  "recovering_arm_store_pairs": res["recovering_arm_store_pairs"]}, indent=1))
for bk, o in res["backends"].items():
    print(bk, "intact delta %.4f" % o["intact_reproduction"]["delta"])
    for arm in ARMS:
        r = o[arm]
        print(f"  {arm:28s} n={r['n']} d={r['delta']:+.4f} ci=[{r['boot']['ci_lo']:+.4f},{r['boot']['ci_hi']:+.4f}] rec={r['recovers']}")
