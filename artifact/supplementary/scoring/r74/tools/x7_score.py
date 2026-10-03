"""R77 S scorer -- intact vs manipulated index (ADDENDUM_R77 §S).

Committed estimators only: score_e1.auroc / score_e1.boot (paired, 1,000 draws, seed 42,
single-class draws discarded). The INTACT arm is the committed E1 indexed-TRUE row, read
from the committed elicitation, never re-elicited. SW-1/SW-2 test the paired
intact-minus-manipulated delta; SW-3 is the frozen adverse branch.
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
from score_e1 import auroc, boot

X4, X7 = ROOT / "r74" / "x4", ROOT / "r74" / "x7"
CELL = json.load(open(X4 / "cell_661.json", encoding="utf-8"))
items = {i["item_id"]: i for i in CELL["items"]}
hard = {i["item_id"] for i in json.load(
    open(ROOT / "e1_metamemory" / "build" / "items_final.json", encoding="utf-8"))
    if i["backend"] == "frbank" and i["tier"] == "hard"}
FOK_IDS = sorted(hard & set(items))
NOK_IDS = sorted(items)
assert len(FOK_IDS) == 307 and len(NOK_IDS) == 661

# INTACT = the committed E1 indexed-TRUE arm, loaded exactly as the committed X4 scorer
# loads it (r74/tools/x4_score.py::load_mini). Read, never re-elicited.
mini_src = ROOT / "e1_metamemory" / "elicitation_main.json"
main = json.load(open(mini_src, encoding="utf-8"))
intact = {r["tag"]: {"fok": r["fok"], "nok": r["nok"]}
          for r in main
          if r["arm"] == "INDEXED-TRUE" and r["status"] == "OK" and r["fok"] is not None}

rows = [json.loads(l) for l in open(X7 / "rows_SWAP.jsonl", encoding="utf-8")]
man = collections.defaultdict(dict)
fails = collections.Counter()
tot = collections.Counter()
spend = 0.0
for r in rows:
    tot[r["arm"]] += 1
    spend += r.get("usd", 0.0)
    if r.get("status") != "OK":
        fails[r["arm"]] += 1
        continue
    man[r["arm"]][r["item_id"]] = r

out = {"registration": "ADDENDUM_R77 §S @ 41e31e7", "lane": "gpt-4.1-mini",
       "spend_usd": round(spend, 4),
       "parse_failures": {a: {"failed": fails[a], "of": tot[a]} for a in sorted(tot)},
       "intact_source": str(mini_src.relative_to(ROOT)) + " (INDEXED-TRUE, keyed by tag; "
                        "same loader as x4_score.load_mini)",
       "cells": {}}

for arm in ("WRONG-PERSON", "SHUFFLED"):
    out["cells"][arm] = {}
    for judgment, ids in (("fok", FOK_IDS), ("nok", NOK_IDS)):
        ks = [i for i in ids if i in intact and i in man[arm]
              and intact[i].get(judgment) is not None
              and man[arm][i].get(judgment) is not None]
        y = [items[i]["y_fok"] if judgment == "fok" else items[i]["y_nok"] for i in ks]
        a_int = [intact[i][judgment] for i in ks]
        a_man = [man[arm][i][judgment] for i in ks]
        d = boot(a_man, a_int, y)          # boot(blind-like, indexed-like) -> indexed - blind
        out["cells"][arm][judgment] = {
            "n": len(ks), "pos": sum(y),
            "intact_auroc": auroc(a_int, y), "manipulated_auroc": auroc(a_man, y),
            "delta_intact_minus_manipulated": d["mean"],
            "ci": [d["ci_lo"], d["ci_hi"]],
            "excludes_zero_positive": bool(d["ci_lo"] > 0)}

sw = {"SW-1": all(out["cells"]["WRONG-PERSON"][j]["excludes_zero_positive"]
                  for j in ("fok", "nok")),
      "SW-2": all(out["cells"]["SHUFFLED"][j]["excludes_zero_positive"]
                  for j in ("fok", "nok"))}
adverse = [(a, j) for a in ("WRONG-PERSON", "SHUFFLED") for j in ("fok", "nok")
           if not out["cells"][a][j]["excludes_zero_positive"]]
out["SW1_wrong_person"] = sw["SW-1"]
out["SW2_shuffled"] = sw["SW-2"]
out["SW3_adverse_cells"] = [f"{a}/{j}" for a, j in adverse]
json.dump(out, open(X7 / "x7_scores.json", "w", encoding="utf-8"), indent=1,
          sort_keys=True, default=float)

print(f"intact source: {out['intact_source']}   spend ${out['spend_usd']}")
for arm in ("WRONG-PERSON", "SHUFFLED"):
    for j in ("fok", "nok"):
        c = out["cells"][arm][j]
        print(f"  {arm:13s} {j.upper()} n={c['n']:3d} pos={c['pos']:3d}  "
              f"intact {c['intact_auroc']:.4f}  manipulated {c['manipulated_auroc']:.4f}  "
              f"delta {c['delta_intact_minus_manipulated']:+.4f} "
              f"[{c['ci'][0]:+.4f},{c['ci'][1]:+.4f}]  excl0={c['excludes_zero_positive']}")
print(f"  SW-1 {'HOLDS' if sw['SW-1'] else 'FAILS'}   SW-2 {'HOLDS' if sw['SW-2'] else 'FAILS'}")
if adverse:
    print(f"  >>> SW-3 ADVERSE BRANCH fires on: {out['SW3_adverse_cells']}")
