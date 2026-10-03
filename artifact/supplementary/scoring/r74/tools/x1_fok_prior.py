"""R74 X1 -- FOK question-prior probe (registered: ADDENDUM_R74 SX1, commit 35f8416a55).

Offline, $0. Supervised TF-IDF, target non-ABSENT vs ABSENT (y_fok), persona-grouped
StratifiedGroupKFold identical to E1-QP (oof_tfidf imported, not reimplemented).
Populations: (a) pooled hard tier n=588; (b) FR-Bank hard n=307.
On both populations the hard tier contains no PRESENT items, so y_fok == y_nok as a
label vector; the FR-Bank-hard result is therefore label-identical to the committed
P2 PN probe. Computed fresh here anyway (both directions of the check).
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1qp_questionprior" / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))

from probes import oof_tfidf                     # frozen CV apparatus
from score_ladder import auroc_ci                # one-sample bootstrap, seed 42
from score_e1 import auroc

SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}
E1 = ROOT / "e1_metamemory"
items = json.load(open(E1 / "build" / "items_final.json", encoding="utf-8"))
rows_main = json.load(open(E1 / "elicitation_main.json", encoding="utf-8"))
qmap = {r["tag"]: r["question"] for r in rows_main if r["arm"] != "BLIND"}

def pop_rows(pred):
    out = []
    for it in items:
        lab = it.get("label", it["label_pre"])
        if lab not in SCOREABLE or it["tier"] != "hard" or not pred(it):
            continue
        q = qmap.get(it["item_id"]) or it.get("question")
        if not q:
            continue
        out.append({"item_id": it["item_id"], "persona": it["persona"],
                    "question": q, "label": lab,
                    "y_fok": 0 if lab == "ABSENT" else 1,
                    "y_nok": 1 if lab == "PRESENT-NEGATIVE" else 0})
    return out

pops = {"hard-pooled": pop_rows(lambda it: True),
        "hard-frbank": pop_rows(lambda it: it["backend"] == "frbank")}

res = {"registration": "ADDENDUM_R74 SX1 @ 35f8416a55", "target": "y_fok (non-ABSENT vs ABSENT)",
       "apparatus": "e1qp probes.oof_tfidf (StratifiedGroupKFold, persona-grouped, seed 42)",
       "probes": {}}
for name, rows in pops.items():
    ident = sum(1 for r in rows if r["y_fok"] != r["y_nok"])
    pred, y, nsp = oof_tfidf(rows, "y_fok")
    if pred is None:
        res["probes"][name] = {"n": len(rows), "note": "not computable"}
        continue
    ci = auroc_ci(list(pred), list(y))
    res["probes"][name] = {
        "n": len(rows), "n_pos": int(sum(y)), "n_splits": nsp,
        "auroc": auroc(pred, y), "ci": [ci["ci_lo"], ci["ci_hi"]],
        "includes_0.50": ci["includes_0.50"],
        "n_items_where_yfok_differs_from_ynok": ident,
    }
    print(name, res["probes"][name])

out = ROOT / "r74" / "x1"
out.mkdir(parents=True, exist_ok=True)
json.dump(res, open(out / "x1_results.json", "w", encoding="utf-8"), indent=2, sort_keys=True)
print("written", out / "x1_results.json")
