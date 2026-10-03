# -*- coding: utf-8 -*-
"""posthoc_b4_intent.py -- B4a, B4b, B4c of reviews/integration/POSTHOC_SPEC_R112.md (program R112, 2026-09-16).
NO MODEL CALL. $0. Post-hoc, specified before recomputation. The intent-held-fixed test the review asked for is not
definable from the recorded rows (spec section B4); what runs is:

B4a  the plain name lookup (superseded section, embedding; run_nb6 rows on the 661) against an intent-aware variant whose
     score is 0 on CHANGE-AWARE items; the same for the all-states lookup (ds_common.names_for v3 lists), where PAST-EVENT
     items are zeroed when the best-matching name lies in the expired section. Paired difference, both intervals.
B4b  CHANGE-AWARE licensed items whose own gold slot holds a join-superseded record (resp_common.true_flags), and the
     share of them the plain lookup flags at the base-rate threshold (the 104th-highest lookup score on the 661).
B4c  the recorded monitors' NOK on the B4b items beside the 63 supersession-derived obligations: median and
     interquartile range only; no AUROC between the two groups (they differ in intent and wording).

Reproduction gates: the plain lookup on the 661 = 0.7484 (AUX-E1R-NB6); mini INDEXED-TRUE NOK = 0.7339 (AUX-E1R-TRUE-NOK).
Usage: python reviews/v19/tools/posthoc_b4_intent.py       Writes reviews/v19/results/posthoc_b4.json
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "resp_review/tools", "ds_downstream/tools", "r74/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from common_e1r import N_BOOT, SEED, auroc, boot_item, boot_cluster, load_e1  # noqa: E402
from run_nb6 import build as nb6_build, emb_scores  # noqa: E402
from index_v3 import named_sections  # noqa: E402
import score_cf as S  # noqa: E402
import cf2_score  # noqa: E402,F401
from ds_common import load_cell, names_for  # noqa: E402
from resp_common import true_flags  # noqa: E402
import x4_score  # noqa: E402

SPEC = ROOT / "reviews" / "integration" / "POSTHOC_SPEC_R112.md"
SPEC_SHA = "ae2600fcf39cf2d626c449835dbbf4dde308cc2e1b07d3e1991d566f920564a6"
OUT = ROOT / "reviews" / "v19" / "results" / "posthoc_b4.json"
GATES = {"lookup_661": 0.7484, "mini_true_nok": 0.7339}


def r4(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)


def paired(base, arm, y, g):
    it, cl = boot_item(base, arm, y), boot_cluster(base, arm, y, g)
    return {"delta": r4(auroc(arm, y) - auroc(base, y)), "item_ci": it, "persona_ci": cl,
            "both_exclude_zero": bool(it.get("excludes_zero") and cl.get("excludes_zero"))}


def matcher_best(questions, name_lists):
    """The name attaining score_cf.matcher's max cosine per item (the same encoder and normalisation; None on an empty list)."""
    enc = S.encoder()
    uq = sorted(set(questions))
    qv = dict(zip(uq, enc.encode(uq, normalize_embeddings=True, batch_size=128, show_progress_bar=False)))
    un = sorted({n for lst in name_lists for n in lst})
    nv = dict(zip(un, enc.encode([n.replace("_", " ") for n in un], normalize_embeddings=True, batch_size=256, show_progress_bar=False))) if un else {}
    out = []
    for q, lst in zip(questions, name_lists):
        out.append(max(lst, key=lambda n: float(qv[q] @ nv[n])) if lst else None)
    return out


def quart(v):
    v = np.asarray(v, float)
    return {"n": int(len(v)), "median": r4(np.median(v)), "q1": r4(np.percentile(v, 25)), "q3": r4(np.percentile(v, 75)),
            "min": r4(v.min()), "max": r4(v.max())} if len(v) else {"n": 0}


def main():
    assert hashlib.sha256(SPEC.read_bytes()).hexdigest() == SPEC_SHA, "the spec file changed after its hash was ledgered"
    items = load_cell(); assert len(items) == 661
    by_id = {it["item_id"]: it for it in items}
    e1_items, blind, idxT, _ = load_e1()
    rows = nb6_build([it for it in e1_items if it["item_id"] in by_id], blind, idxT, "nok", "TRUE")
    assert len(rows) == 661, len(rows)
    order = [r["item_id"] for r in rows]
    y = np.array([r["y"] for r in rows], int); g = np.array([r["persona"] for r in rows])
    intent = np.array([by_id[i]["intent"] for i in order])
    label = np.array([by_id[i]["label"] for i in order])
    assert int(y.sum()) == 104
    res = {"meta": {"script": "reviews/v19/tools/posthoc_b4_intent.py", "spec_sha256": SPEC_SHA, "model_calls": 0, "n_boot": N_BOOT, "seed": SEED,
                    "status": "post hoc, specified before recomputation",
                    "not_definable": "the intent-held-fixed comparison (the same store history under two intents) cannot be built from the recorded rows: "
                                     "each question carries one constructed intent and the CHANGE intent is never PN; no discrimination test across intents is computed"},
           "gates": {}, "B4a": {}, "B4b": {}, "B4c": {}}

    # ---- B4a plain and intent-aware lookups
    plain = np.asarray(emb_scores(rows, "sup"), float)
    lk = r4(auroc(plain, y)); assert lk == GATES["lookup_661"], f"GATE lookup {lk}"; res["gates"]["lookup_661"] = lk
    aware = plain.copy(); aware[intent == "CHANGE-AWARE"] = 0.0
    res["B4a"]["superseded_section"] = {"plain": lk, "intent_aware": r4(auroc(aware, y)), "items_zeroed": int((intent == "CHANGE-AWARE").sum()),
                                        "rule": "score 0 on CHANGE-AWARE items (superseded content licensed under CHANGE, Definition 1); PAST zeroing inapplicable, the section names no expired content",
                                        "aware_minus_plain": paired(plain, aware, y, g)}
    # all-states lookup on the 661 (v3 lists as DS Amendment 1 built them), with the section of the best match recorded
    all_lists, exp_sets = [], []
    for i in order:
        _, v3txt, _, _, _, _ = names_for(by_id[i])
        sec = named_sections(v3txt)
        all_lists.append(sec["superseded"] + sec["retracted"] + sec["expired"]); exp_sets.append(set(sec["expired"]))
    qs = [r["question"] for r in rows]
    s_all = np.asarray(S.matcher(qs, all_lists), float)
    # the best-matching name per item, to apply the PAST rule
    best = matcher_best(qs, all_lists)
    aware_all = s_all.copy(); aware_all[intent == "CHANGE-AWARE"] = 0.0
    past_zeroed = 0
    for k in range(len(order)):
        if intent[k] == "PAST-EVENT" and best[k] is not None and best[k] in exp_sets[k]:
            aware_all[k] = 0.0; past_zeroed += 1
    res["B4a"]["all_states"] = {"plain": r4(auroc(s_all, y)), "intent_aware": r4(auroc(aware_all, y)), "items_zeroed_change": int((intent == "CHANGE-AWARE").sum()),
                                "items_zeroed_past": past_zeroed,
                                "aware_minus_plain": paired(s_all, aware_all, y, g)}

    # ---- B4b: CHANGE-AWARE licensed items whose own gold slot holds a join-superseded record
    fl = true_flags()
    thr = np.sort(plain)[::-1][103]   # the 104th-highest lookup score
    b4b = []
    for k, i in enumerate(order):
        it = by_id[i]
        if intent[k] != "CHANGE-AWARE" or label[k] != "PRESENT":
            continue
        p = it["persona"]; gold = it.get("gold") or []
        slots = {fl[p][e]["slot"] for e in gold if e in fl[p]}
        sup_slots = {d["slot"] for d in fl[p].values() if d["superseded"]}
        own = bool(slots & sup_slots)
        b4b.append({"item_id": i, "own_slot_superseded": own, "lookup_score": r4(plain[k]), "flagged_at_base_rate": bool(plain[k] >= thr), "k": k})
    own_items = [d for d in b4b if d["own_slot_superseded"]]
    res["B4b"] = {"change_aware_licensed": len(b4b), "own_slot_holds_superseded": len(own_items),
                  "flagged_at_base_rate_threshold": {"own_slot_items": int(sum(d["flagged_at_base_rate"] for d in own_items)),
                                                     "all_change_aware_licensed": int(sum(d["flagged_at_base_rate"] for d in b4b))},
                  "base_rate_threshold": r4(thr), "items": [{k_: v_ for k_, v_ in d.items() if k_ != "k"} for d in b4b]}
    if len(own_items) < 5:
        res["B4b"]["status"] = f"not definable from the recorded data: {len(own_items)} items reached (fewer than 5)"

    # ---- B4c: the monitors on those items, descriptive
    monitors = {"gpt-4.1-mini": np.array([idxT[i]["nok"] for i in order], float)}
    m_gate = r4(auroc(monitors["gpt-4.1-mini"], y)); assert m_gate == GATES["mini_true_nok"], f"GATE mini {m_gate}"; res["gates"]["mini_true_nok"] = m_gate
    for model, code in (("claude-haiku-4-5-20251001", "H45"), ("claude-opus-5", "OP5"), ("gpt-5.6-luna", "LUNA")):
        coll, _ = x4_score.load_lane(code)
        monitors[model] = np.array([coll.get((i, "INDEXED-TRUE"), {}).get("nok", np.nan) for i in order], float)
    sup_obl = np.array([label[k] == "PRESENT-NEGATIVE" and by_id[i]["state"] == "sup" for k, i in enumerate(order)])
    res["B4c"]["supersession_obligations_n"] = int(sup_obl.sum())
    own_idx = np.array([d["k"] for d in own_items], int)
    res["B4c"]["definition"] = "median and interquartile range of the NOK score; descriptive; not a discrimination test"
    res["B4c"]["monitors"] = {}
    for model, v in monitors.items():
        res["B4c"]["monitors"][model] = {"own_slot_change_items": quart(v[own_idx][~np.isnan(v[own_idx])]) if len(own_idx) else {"n": 0},
                                          "supersession_obligations": quart(v[sup_obl][~np.isnan(v[sup_obl])])}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1, ensure_ascii=False))
    print(json.dumps({k: res[k] for k in ("gates", "B4a")}, indent=1))
    print("B4b", {k: v for k, v in res["B4b"].items() if k != "items"})
    print("B4c", json.dumps(res["B4c"], indent=1))
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
