"""POST-HOC composition census for NB-6. R81, unregistered, deterministic, $0.

STATUS. This is POST HOC. It was designed after NB6-1 failed, to ask why a matcher over the
superseded-names section reaches the smallest monitor. It carries no registered prediction,
and it prints whatever it finds. Nothing here may be reported as confirmatory.

THE STRUCTURAL PREMISE (verifiable from the generator, not from this file).
`e1_metamemory/tools/index_v2.py` emits per-category active/superseded/retracted/expired
COUNTS, but names attributes in exactly one place: the flat section
`ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT`. Expired and retracted content therefore
appears in the index as a count and never as a name. A matcher over that section is
structurally unable to find an obligation that arises from expiry or retraction.

WHAT THIS MEASURES.
  1. PN composition by attack vector, on the n=661 population and on the matched-84 cell.
  2. Whether each PN item's obligation is NAMED: does any slot of its `pn_members` appear
     in that index's superseded-names section?
  3. NB-6's discrimination split by named vs unnamed positives, against the same negatives.
  4. Mean NB-6 score on named PN, unnamed PN, and negatives.

Usage: python e1r_robustness/tools/nb6_composition.py
Writes results/nb6_composition.json. Exit 0 regardless of what it finds.
"""
from __future__ import annotations

import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_e1r import E1, OUT, POPULATIONS, auroc, jdump, jload, load_e1   # noqa: E402
from index_features import index_key, indexes, parse                        # noqa: E402
from run_nb6 import emb_scores, lex_scores, name_lists                      # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

# Which lifecycle state each attack vector's obligation arises from. Read off the taxonomy,
# not inferred here: AV1/AV4 are supersession, AV2 is expiry, AV7 is retraction/forgetting.
AV_STATE = {
    "AV1_superseded_preference": "superseded",
    "AV4_multi_version_fact": "superseded",
    "AV2_expired_logistics": "expired",
    "AV7_selective_forgetting": "retracted",
}


def slot_map():
    """entry_id -> slot (the attribute name the index would print)."""
    return {e["entry_id"]: e.get("slot") for e in
            jload(E1 / "backend_entries" / "frbank.json")}


def named(item, provenance, slots):
    """Is this PN item's obligation NAMED in the superseded-names section it was shown?"""
    sup, _ = name_lists(item, provenance)
    supset = {s.strip().lower() for s in sup}
    mine = {slots.get(m) for m in (item.get("pn_members") or []) if slots.get(m)}
    return bool(mine & supset), sorted(mine)


def census(rows, label):
    out = {"population": label, "n": len(rows),
           "n_pn": sum(1 for r in rows if r["y"] == 1)}
    by_av = Counter(r["av"] for r in rows if r["y"] == 1)
    by_state = Counter(AV_STATE.get(r["av"], "unknown") for r in rows if r["y"] == 1)
    out["pn_by_attack_vector"] = dict(sorted(by_av.items()))
    out["pn_by_lifecycle_state"] = dict(sorted(by_state.items()))
    tot = max(1, out["n_pn"])
    out["pn_supersession_share"] = by_state["superseded"] / tot
    return out


def main():
    items, blind, idxT, idxB = load_e1()
    slots = slot_map()
    results = {}

    for prov, idx in (("TRUE", idxT), ("BELIEVED", idxB)):
        sub = [it for it in items if POPULATIONS["R-NOK-FRB"]["filt"](it)]
        rows = []
        for it in sub:
            q, tag = it["question"], it["item_id"]
            if q not in blind or tag not in idx:
                continue
            if blind[q].get("nok") is None or idx[tag].get("nok") is None:
                continue
            lab = it.get("label", it["label_pre"])
            y = 1 if lab == "PRESENT-NEGATIVE" else 0
            sup, alln = name_lists(it, prov)
            is_named, mine = named(it, prov, slots) if y == 1 else (False, [])
            rows.append({"y": y, "question": q, "sup": sup, "all": alln,
                         "av": it.get("attack_vector"), "named": is_named,
                         "slots": mine, "monitor": idx[tag].get("nok"),
                         "item_id": tag})

        lex = lex_scores(rows, "sup")
        emb = emb_scores(rows, "sup")
        y = np.array([r["y"] for r in rows], int)
        rec = census(rows, f"R-NOK-FRB {prov}")

        # naming rate among PN, overall and by lifecycle state
        pn = [r for r in rows if r["y"] == 1]
        rec["pn_named_in_index"] = sum(1 for r in pn if r["named"])
        rec["pn_named_rate"] = rec["pn_named_in_index"] / max(1, len(pn))
        byst = defaultdict(lambda: [0, 0])
        for r in pn:
            st = AV_STATE.get(r["av"], "unknown")
            byst[st][1] += 1
            byst[st][0] += int(r["named"])
        rec["named_by_lifecycle_state"] = {
            k: {"named": v[0], "total": v[1], "rate": v[0] / max(1, v[1])}
            for k, v in sorted(byst.items())}

        # discrimination split by named vs unnamed positives, SAME negatives
        neg = [i for i, r in enumerate(rows) if r["y"] == 0]
        for tag_, sel in (("named", [i for i, r in enumerate(rows) if r["y"] == 1 and r["named"]]),
                          ("unnamed", [i for i, r in enumerate(rows) if r["y"] == 1 and not r["named"]])):
            keep = sorted(sel + neg)
            yy = np.array([rows[i]["y"] for i in keep], int)
            rec[f"nb6_emb_auroc_{tag_}_pn"] = float(auroc([emb[i] for i in keep], yy))
            rec[f"nb6_lex_auroc_{tag_}_pn"] = float(auroc([lex[i] for i in keep], yy))
            rec[f"monitor_auroc_{tag_}_pn"] = float(
                auroc([rows[i]["monitor"] for i in keep], yy))
            rec[f"n_{tag_}_pn"] = len(sel)

        # discrimination split by lifecycle state of the positive
        for st in ("superseded", "expired", "retracted"):
            sel = [i for i, r in enumerate(rows)
                   if r["y"] == 1 and AV_STATE.get(r["av"]) == st]
            if not sel:
                continue
            keep = sorted(sel + neg)
            yy = np.array([rows[i]["y"] for i in keep], int)
            rec[f"nb6_emb_auroc_pn_{st}"] = float(auroc([emb[i] for i in keep], yy))
            rec[f"monitor_auroc_pn_{st}"] = float(
                auroc([rows[i]["monitor"] for i in keep], yy))
            rec[f"n_pn_{st}"] = len(sel)

        rec["mean_nb6_emb_named_pn"] = float(np.mean(
            [emb[i] for i, r in enumerate(rows) if r["y"] == 1 and r["named"]] or [np.nan]))
        rec["mean_nb6_emb_unnamed_pn"] = float(np.mean(
            [emb[i] for i, r in enumerate(rows) if r["y"] == 1 and not r["named"]] or [np.nan]))
        rec["mean_nb6_emb_negatives"] = float(np.mean([emb[i] for i in neg]))
        results[f"R-NOK-FRB|{prov}"] = rec

    # ---- matched-84 composition (descriptive) --------------------------------------
    man = jload(ROOT / "e1xv_crossvendor" / "manifests" / "cell_84.json")
    byid = {i["item_id"]: i for i in items}
    m84rows = [{"y": it["y_nok"], "av": byid.get(it["item_id"], {}).get("attack_vector")}
               for it in man["items"]]
    results["matched-84"] = census(m84rows, "matched-84")

    jdump({"rows": results,
           "status": "POST HOC, unregistered, deterministic; no prediction attached",
           "structural_premise": (
               "index_v2.py names attributes only under ATTRIBUTE NAMES CARRYING SUPERSEDED "
               "CONTENT; expired and retracted content appears as counts only"),
           "av_state_map": AV_STATE},
          OUT / "nb6_composition.json")

    for k, r in results.items():
        print(f"\n{k}  n={r['n']}  PN={r['n_pn']}")
        print(f"   by lifecycle state : {r['pn_by_lifecycle_state']}")
        print(f"   supersession share : {r['pn_supersession_share']:.3f}")
        if "pn_named_rate" in r:
            print(f"   PN named in index  : {r['pn_named_in_index']}/{r['n_pn']} "
                  f"({r['pn_named_rate']:.3f})")
            for st, v in r["named_by_lifecycle_state"].items():
                print(f"       {st:12s} named {v['named']:3d}/{v['total']:3d} = {v['rate']:.3f}")
            print(f"   NB-6 emb AUROC  named PN {r['nb6_emb_auroc_named_pn']:.4f} "
                  f"(n={r['n_named_pn']})   unnamed PN {r['nb6_emb_auroc_unnamed_pn']:.4f} "
                  f"(n={r['n_unnamed_pn']})")
            print(f"   monitor  AUROC  named PN {r['monitor_auroc_named_pn']:.4f}"
                  f"                unnamed PN {r['monitor_auroc_unnamed_pn']:.4f}")
            for st in ("superseded", "expired", "retracted"):
                if f"nb6_emb_auroc_pn_{st}" in r:
                    print(f"   by state {st:11s} NB-6 {r[f'nb6_emb_auroc_pn_{st}']:.4f}  "
                          f"monitor {r[f'monitor_auroc_pn_{st}']:.4f}  (n={r[f'n_pn_{st}']})")
            print(f"   mean NB-6 emb: named {r['mean_nb6_emb_named_pn']:.4f}  "
                  f"unnamed {r['mean_nb6_emb_unnamed_pn']:.4f}  "
                  f"negatives {r['mean_nb6_emb_negatives']:.4f}")
    print(f"\nwrote {OUT / 'nb6_composition.json'}")


if __name__ == "__main__":
    main()
