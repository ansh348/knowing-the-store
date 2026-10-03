"""R74 X4 scorer (ADDENDUM_R74 SX4 @ 35f8416a55).

Collapse k draws per (item, arm) with MIN_DRAWS=3 (mini = the committed E1 rows, k=1 by
its original protocol); NOK cell on the 661-item population (y_nok), FOK cell on the
hard-tier 307 subset (y_fok). Committed estimators only (score_e1.auroc/boot,
score_ladder.auroc_ci). XP-1..XP-5 verdicts per the registration.
"""
import json, pathlib, sys, collections
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
from score_e1 import auroc, boot
from score_ladder import auroc_ci

X4 = ROOT / "r74" / "x4"
CELL = json.load(open(X4 / "cell_661.json", encoding="utf-8"))["items"]
BYID = {c["item_id"]: c for c in CELL}
HARD = {c["item_id"] for c in CELL if c["tier"] == "hard"}
MIN_DRAWS = 3
LANES = {"gpt-4.1-mini": None, "gpt-5.6-luna": "LUNA", "gpt-5.6-sol": "SOL",
         "claude-opus-5": "OP5", "claude-haiku-4-5-20251001": "H45", "kimi-k3": "K3"}
# D-R74-6 (PI budget directive): stopped-incomplete lanes are never scored as cells;
# they report row counts and spend only. Completed lanes only below.
COMPLETED = {"gpt-4.1-mini", "gpt-5.6-luna", "claude-opus-5", "claude-haiku-4-5-20251001"}

def load_lane(code):
    pth = X4 / f"rows_{code}.jsonl"
    if not pth.exists():
        return None
    per = collections.defaultdict(list)
    for line in open(pth, encoding="utf-8"):
        r = json.loads(line)
        if r.get("status") == "OK" and r.get("fok") is not None:
            per[(r["item_id"], r["arm"])].append(r)
    coll = {}
    for (iid, arm), rs in per.items():
        rs = {r["draw"]: r for r in rs}.values()          # dedup on draw
        if len(rs) < MIN_DRAWS:
            continue
        coll[(iid, arm)] = {"fok": float(np.mean([r["fok"] for r in rs])),
                            "nok": float(np.mean([r["nok"] for r in rs if r["nok"] is not None]))
                            if any(r["nok"] is not None for r in rs) else None,
                            "n_draws": len(rs)}
    usd = sum(json.loads(l).get("usd", 0.0) for l in open(pth, encoding="utf-8"))
    return coll, usd

def load_mini():
    main = json.load(open(ROOT / "e1_metamemory" / "elicitation_main.json", encoding="utf-8"))
    blind_by_q = {r["tag"]: r for r in main if r["arm"] == "BLIND" and r["status"] == "OK"}
    inx = {r["tag"]: r for r in main if r["arm"] == "INDEXED-TRUE" and r["status"] == "OK"}
    coll = {}
    for c in CELL:
        b = blind_by_q.get(c["question"]); i = inx.get(c["item_id"])
        if b and b["fok"] is not None:
            coll[(c["item_id"], "BLIND")] = {"fok": b["fok"], "nok": b["nok"], "n_draws": 1}
        if i and i["fok"] is not None:
            coll[(c["item_id"], "INDEXED-TRUE")] = {"fok": i["fok"], "nok": i["nok"], "n_draws": 1}
    return coll, 0.0

def cellstats(coll, judgment):
    ids = [c["item_id"] for c in CELL
           if (judgment == "nok" or c["item_id"] in HARD)
           and (c["item_id"], "BLIND") in coll and (c["item_id"], "INDEXED-TRUE") in coll
           and coll[(c["item_id"], "BLIND")][judgment] is not None
           and coll[(c["item_id"], "INDEXED-TRUE")][judgment] is not None]
    y = np.array([BYID[i]["y_" + judgment] for i in ids])
    b = np.array([coll[(i, "BLIND")][judgment] for i in ids], float)
    a = np.array([coll[(i, "INDEXED-TRUE")][judgment] for i in ids], float)
    personas = [BYID[i]["persona"] for i in ids]
    rng = np.random.default_rng(42)
    ps = sorted(set(personas))
    byp = {p: np.array([k for k, q in enumerate(personas) if q == p]) for p in ps}
    ds = []
    for _ in range(1000):
        take = np.concatenate([byp[ps[j]] for j in rng.integers(0, len(ps), len(ps))])
        yy = y[take]
        if len(set(yy.tolist())) < 2:
            continue
        ds.append(auroc(a[take], yy) - auroc(b[take], yy))
    return {"n": len(ids), "n_pos": int(y.sum()),
            "blind": auroc(b, y), "blind_ci": auroc_ci(list(b), list(y)),
            "indexed": auroc(a, y), "indexed_ci": auroc_ci(list(a), list(y)),
            "delta": auroc(a, y) - auroc(b, y), "boot": boot(b, a, y),
            "clustered_ci": [float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5))],
            "blind_tie_degenerate": len(set(b.tolist())) == 1}

res = {"registration": "ADDENDUM_R74 SX4 @ 35f8416a55", "lanes": {}, "usd": {}}
for lane, code in LANES.items():
    got = load_mini() if code is None else load_lane(code)
    if got is None:
        res["lanes"][lane] = {"status": "NOT_RUN"}
        continue
    coll, usd = got
    res["usd"][lane] = usd
    if lane not in COMPLETED:
        pth = X4 / f"rows_{code}.jsonl"
        nrows = sum(1 for _ in open(pth, encoding="utf-8"))
        res["lanes"][lane] = {"status": "STOPPED_INCOMPLETE", "n_rows": nrows,
                              "usd": usd, "note": "D-R74-6 budget stop; not scored as a cell"}
        continue
    res["lanes"][lane] = {"status": "OK",
                          "n_cells": len(coll),
                          "nok_661": cellstats(coll, "nok"),
                          "fok_307": cellstats(coll, "fok")}

L = res["lanes"]
new = [m for m in LANES if m != "gpt-4.1-mini" and L[m].get("status") == "OK"]
mini = L["gpt-4.1-mini"]
xp5 = (round(mini["nok_661"]["blind"], 4) == 0.4946 and round(mini["nok_661"]["indexed"], 4) == 0.7339
       and round(mini["nok_661"]["delta"], 4) == 0.2393 and round(mini["fok_307"]["blind"], 4) == 0.4966
       and round(mini["fok_307"]["indexed"], 4) == 0.7003 and round(mini["fok_307"]["delta"], 4) == 0.2037)
xp1 = {m: L[m]["nok_661"]["boot"]["ci_lo"] > 0 for m in new}
xp2 = {m: L[m]["fok_307"]["delta"] > 0 for m in new}
allm = ["gpt-4.1-mini"] + new
bspan = max(L[m]["nok_661"]["blind"] for m in allm) - min(L[m]["nok_661"]["blind"] for m in allm)
ispan = max(L[m]["nok_661"]["indexed"] for m in allm) - min(L[m]["nok_661"]["indexed"] for m in allm)
xp3 = ispan < bspan
def dirn(m, below):
    s = L[m]["nok_661"]; ci = s["blind_ci"]
    return (s["blind"] < 0.5 and ci["ci_hi"] < 0.5) if below else (s["blind"] > 0.5 and ci["ci_lo"] > 0.5)
xp4 = {"haiku_below": dirn("claude-haiku-4-5-20251001", True) if "claude-haiku-4-5-20251001" in new else None,
       "opus_above": dirn("claude-opus-5", False) if "claude-opus-5" in new else None}
res["predictions"] = {"XP-1": xp1, "XP-2": xp2,
                      "XP-3": {"blind_span": bspan, "indexed_span": ispan, "holds": bool(xp3)},
                      "XP-4": xp4, "XP-5_mini_reproduction": bool(xp5)}
json.dump(res, open(X4 / "x4_scores.json", "w", encoding="utf-8"), indent=1, sort_keys=True,
          default=float)
print("XP-5 mini reproduction:", xp5)
for m in allm:
    for j in ("nok_661", "fok_307"):
        s = L[m][j]
        print(f"{m:28s} {j} n={s['n']} blind={s['blind']:.4f} idx={s['indexed']:.4f} "
              f"d={s['delta']:+.4f} ci=[{s['boot']['ci_lo']:+.4f},{s['boot']['ci_hi']:+.4f}]"
              f"{' TIE' if s['blind_tie_degenerate'] else ''}")
print(json.dumps(res["predictions"], indent=1, default=str))
