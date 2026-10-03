# -*- coding: utf-8 -*-
"""r127_groups.py -- R127 item 2 (2026-09-20; offline, $0, no model call): from the recorded rows on the 661, for GPT-4.1 mini, Haiku 4.5, GPT-5.6 Luna
and Opus 5 and for the name lookup, the obligation score's AUROC of the 104 PN questions against
  (a) the 33 PRESENT questions whose own attribute holds a non-active record under current or upcoming intent,
  (b) the 11 such questions under change intent,
  (c) the remaining 130 PRESENT questions,
the mean score per group (and of the 104), and both intervals of each AUROC: the item-level bootstrap (items of the two groups resampled
together) and the persona-grouped bootstrap (personas resampled), 1,000 draws, seed 42, percentile 2.5 / 97.5 (common_e1r's conventions;
boot_cluster_single for the persona interval, the same resampling for the item interval).

Rows: GPT-4.1 mini's recorded INDEXED-TRUE nok (load_e1, one call); Haiku 4.5, Opus 5 and GPT-5.6 Luna from r74/x4 rows_*.jsonl through
x4_score.load_lane (the five-call collapse, INDEXED-TRUE nok), exactly as reviews/v19/tools/posthoc_b4_intent.py B4c reads them; the name
lookup from run_nb6.emb_scores on the superseded section (the recorded 0.7484 on the 661 asserted). The groups are those of
reviews/v22/results/e3_intent_table.json (reviews/v22/tools/e3_intent_table.py, the same own_slot_marks rule). Writes reviews/v22/results/r127_groups.json.
Usage: python reviews/v22/tools/r127_groups.py
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "resp_review/tools", "ds_downstream/tools", "r74/tools", "reviews/v22/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from common_e1r import N_BOOT, SEED, auroc, load_e1  # noqa: E402
from run_nb6 import build as nb6_build, emb_scores  # noqa: E402
from ds_common import load_cell  # noqa: E402
from resp_common import true_flags  # noqa: E402
import x4_score  # noqa: E402
from e3_intent_table import own_slot_marks  # noqa: E402

OUT = ROOT / "reviews" / "v22" / "results" / "r127_groups.json"
GROUPS = {"a": "PRESENT, non-active own-attribute record, current or upcoming intent", "b": "PRESENT, non-active own-attribute record, change intent",
          "c": "PRESENT, the rest"}


def r4(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)


def boot_item_single(s, y, n=N_BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    s, y = np.asarray(s, float), np.asarray(y, int)
    d = []
    for _ in range(n):
        k = rng.integers(0, len(y), len(y))
        if y[k].sum() in (0, len(k)):
            continue
        d.append(auroc(s[k], y[k]))
    return summ(d)


def boot_persona_single(s, y, g, n=N_BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    s, y, g = np.asarray(s, float), np.asarray(y, int), np.asarray(g)
    groups = np.unique(g)
    idx = {u: np.flatnonzero(g == u) for u in groups}
    d = []
    for _ in range(n):
        drawn = rng.integers(0, len(groups), len(groups))
        k = np.concatenate([idx[groups[t]] for t in drawn])
        if y[k].sum() in (0, len(k)):
            continue
        d.append(auroc(s[k], y[k]))
    return summ(d)


def summ(d):
    d = np.asarray(d, float)
    return {"n_draws": int(len(d)), "ci_lo": r4(np.percentile(d, 2.5)), "ci_hi": r4(np.percentile(d, 97.5))} if len(d) else {"n_draws": 0}


def main():
    items = load_cell(); assert len(items) == 661
    by_id = {it["item_id"]: it for it in items}
    e1_items, blind, idxT, _ = load_e1()
    rows = nb6_build([it for it in e1_items if it["item_id"] in by_id], blind, idxT, "nok", "TRUE")
    assert len(rows) == 661
    order = [r["item_id"] for r in rows]
    y = np.array([r["y"] for r in rows], int); persona = np.array([r["persona"] for r in rows])
    assert int(y.sum()) == 104
    fl = true_flags()
    grp = np.array([""] * 661, dtype=object)
    for k, i in enumerate(order):
        it = by_id[i]
        if it["label"] == "PRESENT-NEGATIVE":
            grp[k] = "pn"
        elif it["label"] == "PRESENT":
            marks = own_slot_marks(it, fl)
            if marks:
                grp[k] = "a" if it["intent"] in ("CURRENT-STATE", "UPCOMING") else ("b" if it["intent"] == "CHANGE-AWARE" else "c")
            else:
                grp[k] = "c"
        else:
            grp[k] = "absent"
    counts = {g: int((grp == g).sum()) for g in ("pn", "a", "b", "c", "absent")}
    assert counts == {"pn": 104, "a": 33, "b": 11, "c": 130, "absent": 383}, counts
    readers = {"GPT-4.1 mini (INDEXED-TRUE, one call)": np.array([idxT[i]["nok"] for i in order], float)}
    for model, code in (("Haiku 4.5 (five calls)", "H45"), ("Opus 5 (five calls)", "OP5"), ("GPT-5.6 Luna (five calls)", "LUNA")):
        coll, _ = x4_score.load_lane(code)
        readers[model] = np.array([coll.get((i, "INDEXED-TRUE"), {}).get("nok", np.nan) for i in order], float)
    lookup = np.asarray(emb_scores(rows, "sup"), float)
    assert r4(auroc(lookup, y)) == 0.7484, r4(auroc(lookup, y))
    assert r4(auroc(readers["GPT-4.1 mini (INDEXED-TRUE, one call)"], y)) == 0.7339
    readers["name lookup (superseded section, embedding)"] = lookup
    res = {"groups": {**GROUPS, "counts": counts}, "readers": {}}
    for name, s in readers.items():
        ok = ~np.isnan(s)
        entry = {"missing_scores": int((~ok).sum()), "mean_pn": r4(s[(grp == "pn") & ok].mean())}
        for g in ("a", "b", "c"):
            m = ((grp == "pn") | (grp == g)) & ok
            yy = (grp[m] == "pn").astype(int)
            entry[g] = {"n_pn": int(yy.sum()), "n_group": int((1 - yy).sum()), "mean_group": r4(s[(grp == g) & ok].mean()),
                        "auroc": r4(auroc(s[m], yy)), "item_ci": boot_item_single(s[m], yy), "persona_ci": boot_persona_single(s[m], yy, persona[m])}
        res["readers"][name] = entry
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(f"groups: {counts}")
    for name, e in res["readers"].items():
        print(f"{name}  (missing {e['missing_scores']}; mean over the 104 PN {e['mean_pn']})")
        for g in ("a", "b", "c"):
            x = e[g]
            print(f"   {g}: n {x['n_pn']} PN vs {x['n_group']}; mean {x['mean_group']}; AUROC {x['auroc']}; item [{x['item_ci']['ci_lo']}, {x['item_ci']['ci_hi']}]; persona [{x['persona_ci']['ci_lo']}, {x['persona_ci']['ci_hi']}]")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
