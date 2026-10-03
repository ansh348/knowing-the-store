# -*- coding: utf-8 -*-
"""r127b_groups.py -- R127b items 2 and 3 (2026-09-20; offline, $0, no model call), on the same groups as r127_groups.py:
  (a) the 33 PRESENT questions whose own attribute holds a non-active record under current or upcoming intent, (b) the 11 under change intent,
  (c) the remaining 130 PRESENT, and the 104 PN.
Item 2: the rule that makes group (a) PRESENT (read from the items' fields: label_pre, pn_members, pn_evidence, attack_vector) and six examples with the
attribute's records and their ground-truth states. Item 3: per reader, the mean question-only (BLIND) score and the mean with-summary (INDEXED-TRUE)
score on each group and on the 104, and, for each PRESENT group, the paired gain (indexed AUROC minus blind AUROC of the 104 against that group) with
the item-level and the persona-grouped interval (common_e1r.boot_item / boot_cluster, 1,000 draws, seed 42). The name lookup has no question-only form.
Rows as r127_groups.py reads them. Writes reviews/v22/results/r127b_groups.json.
Usage: python reviews/v22/tools/r127b_groups.py
"""
from __future__ import annotations

import collections
import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "resp_review/tools", "ds_downstream/tools", "r74/tools", "reviews/v22/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from common_e1r import auroc, boot_item, boot_cluster, load_e1  # noqa: E402
from run_nb6 import build as nb6_build  # noqa: E402
from ds_common import load_cell  # noqa: E402
from resp_common import true_flags, variant_ids  # noqa: E402
import x4_score  # noqa: E402
from e3_intent_table import own_slot_marks  # noqa: E402

OUT = ROOT / "reviews" / "v22" / "results" / "r127b_groups.json"


def r4(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)


def ci(d):
    return {"ci_lo": r4(d.get("ci_lo")), "ci_hi": r4(d.get("ci_hi")), "excludes_zero": d.get("excludes_zero")}


def main():
    items = load_cell(); assert len(items) == 661
    by_id = {it["item_id"]: it for it in items}
    e1_items, blind, idxT, _ = load_e1()
    rows = nb6_build([it for it in e1_items if it["item_id"] in by_id], blind, idxT, "nok", "TRUE")
    order = [r["item_id"] for r in rows]
    persona = np.array([r["persona"] for r in rows])
    fl = true_flags()
    grp = {}
    for i in order:
        it = by_id[i]
        if it["label"] == "PRESENT-NEGATIVE":
            grp[i] = "pn"
        elif it["label"] == "PRESENT":
            marks = own_slot_marks(it, fl)
            grp[i] = ("a" if it["intent"] in ("CURRENT-STATE", "UPCOMING") else "b" if it["intent"] == "CHANGE-AWARE" else "c") if marks else "c"
        else:
            grp[i] = "absent"
    g = np.array([grp[i] for i in order], dtype=object)
    assert collections.Counter(g) == {"pn": 104, "a": 33, "b": 11, "c": 130, "absent": 383}

    # ---- item 2: the fields that make group (a) PRESENT, and six examples with the attribute's records
    a_items = [by_id[i] for i in order if grp[i] == "a"]
    fields = collections.Counter((it["label_pre"], it["attack_vector"], bool(it.get("pn_members")), it["variant"]) for it in a_items)
    examples = []
    want = [("CURRENT-STATE", "expired"), ("CURRENT-STATE", "superseded"), ("CURRENT-STATE", "retracted"), ("UPCOMING", "superseded"), ("UPCOMING", "retracted"), ("UPCOMING", "expired")]
    for intent, mark in want:
        for it in a_items:
            marks = own_slot_marks(it, fl)
            if it["intent"] == intent and mark in marks and not any(e["item_id"] == it["item_id"] for e in examples):
                present = set(variant_ids(it))
                fp = {e: d for e, d in fl[it["persona"]].items() if e in present}
                slots = {fp[e]["slot"] for e in it["gold"] if e in fp}
                recs = [{"entry": e, "gold": e in it["gold"], "state": ", ".join(m for m in ("retracted", "superseded", "expired") if d[m]) or "active",
                         "age_days": d["age"], "text": d["text"][:220]} for e, d in fp.items() if d["slot"] in slots]
                examples.append({"item_id": it["item_id"], "question": it["question"], "intent": it["intent"], "label": it["label"], "label_pre": it["label_pre"],
                                 "attack_vector": it["attack_vector"], "pn_members": it.get("pn_members"), "slots": sorted(slots), "records": recs})
                break
    # R128 (2026-09-20): no group-(a) item pairs CURRENT-STATE with a retracted own-slot record, so the sixth example is the next CURRENT-STATE item
    # whose own slot carries an expired record (a second instance of the first combination).
    if len(examples) < 6:
        for it in a_items:
            marks = own_slot_marks(it, fl)
            if it["intent"] == "CURRENT-STATE" and "expired" in marks and not any(e["item_id"] == it["item_id"] for e in examples):
                present = set(variant_ids(it))
                fp = {e: d for e, d in fl[it["persona"]].items() if e in present}
                slots = {fp[e]["slot"] for e in it["gold"] if e in fp}
                recs = [{"entry": e, "gold": e in it["gold"], "state": ", ".join(m for m in ("retracted", "superseded", "expired") if d[m]) or "active",
                         "age_days": d["age"], "text": d["text"][:220]} for e, d in fp.items() if d["slot"] in slots]
                examples.append({"item_id": it["item_id"], "question": it["question"], "intent": it["intent"], "label": it["label"], "label_pre": it["label_pre"],
                                 "attack_vector": it["attack_vector"], "pn_members": it.get("pn_members"), "slots": sorted(slots), "records": recs, "note": "second CURRENT-STATE + expired instance (no CURRENT-STATE + retracted item exists in group (a))"})
                break
    assert len(examples) == 6, len(examples)
    # ---- item 3: means and paired gains per reader
    qof = {r["item_id"]: r["question"] for r in rows}     # blind is keyed by the question text (one call per question, load_e1)
    readers = {"GPT-4.1 mini": (np.array([blind[qof[i]]["nok"] for i in order], float), np.array([idxT[i]["nok"] for i in order], float))}
    for model, code in (("Haiku 4.5", "H45"), ("Opus 5", "OP5"), ("GPT-5.6 Luna", "LUNA")):
        coll, _ = x4_score.load_lane(code)
        readers[model] = (np.array([coll.get((i, "BLIND"), {}).get("nok", np.nan) for i in order], float),
                          np.array([coll.get((i, "INDEXED-TRUE"), {}).get("nok", np.nan) for i in order], float))
    res = {"groups": dict(collections.Counter(g)), "group_a_fields": [{"label_pre": k[0], "attack_vector": k[1], "has_pn_members": k[2], "variant": k[3], "n": n} for k, n in fields.items()],
           "examples": examples, "readers": {}}
    for name, (b, s) in readers.items():
        ok = ~np.isnan(b) & ~np.isnan(s)
        entry = {"missing": int((~ok).sum()), "means": {}}
        for gname in ("pn", "a", "b", "c"):
            m = (g == gname) & ok
            entry["means"][gname] = {"n": int(m.sum()), "blind": r4(b[m].mean()), "indexed": r4(s[m].mean()), "mean_paired_diff": r4((s[m] - b[m]).mean())}
        for gname in ("a", "b", "c"):
            m = ((g == "pn") | (g == gname)) & ok
            yy = (g[m] == "pn").astype(int)
            entry[gname] = {"blind_auroc": r4(auroc(b[m], yy)), "indexed_auroc": r4(auroc(s[m], yy)), "gain": r4(auroc(s[m], yy) - auroc(b[m], yy)),
                            "item_ci": ci(boot_item(b[m], s[m], yy)), "persona_ci": ci(boot_cluster(b[m], s[m], yy, persona[m]))}
        res["readers"][name] = entry
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("group (a) fields:", res["group_a_fields"])
    for e in examples:
        print(f"\n{e['item_id']} | {e['intent']} | {e['label']} (pre {e['label_pre']}; {e['attack_vector']}; pn_members {e['pn_members']})\n  Q: {e['question']}\n  slots: {e['slots']}")
        for r in e["records"]:
            print(f"    [{r['state']:9s}] gold={r['gold']!s:5s} age {r['age_days']}: {r['text'][:170]}")
    for name, e in res["readers"].items():
        print(f"\n{name} (missing {e['missing']})")
        for gname in ("pn", "a", "b", "c"):
            m = e["means"][gname]; print(f"   {gname}: n {m['n']} blind {m['blind']} indexed {m['indexed']} paired mean diff {m['mean_paired_diff']}")
        for gname in ("a", "b", "c"):
            x = e[gname]; print(f"   PN vs {gname}: blind AUROC {x['blind_auroc']} indexed {x['indexed_auroc']} gain {x['gain']} item [{x['item_ci']['ci_lo']}, {x['item_ci']['ci_hi']}] persona [{x['persona_ci']['ci_lo']}, {x['persona_ci']['ci_hi']}]")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
