# -*- coding: utf-8 -*-
"""posthoc_f1_wholemap.py -- F1 of reviews/integration/POSTHOC_SPEC_R112.md (program R112, 2026-09-16).
NO MODEL CALL. $0. Post-hoc, specified before recomputation. The whole-name-map embedding lookup (run_nb6's FOK-6
reader, the NB-5 column of Table tab:baselines) on the FR-Bank easy tier (354 questions, 243 non-ABSENT positives), the
population reviews/v12/tools/phase1.py item 1 built, beside GPT-4.1 mini's recorded indexed FOK and the superseded-section
lookup; the model minus the whole-map lookup, paired, both intervals. The hard tier prints beside it as a check against
the recorded NB-5 value (0.6186).

Reproduction gates: easy tier monitor 0.7835 and superseded-section embedding lookup 0.6083 (AUX-R104-COV-LOOKUP);
hard tier whole-map lookup 0.6186 (AUX-E1R-BASELINES NB-5).
Usage: python reviews/v19/tools/posthoc_f1_wholemap.py       Writes reviews/v19/results/posthoc_f1.json
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
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from common_e1r import N_BOOT, SEED, auroc, boot_item, boot_cluster, boot_cluster_single, load_e1, POPULATIONS  # noqa: E402
from run_nb6 import build as nb6_build, emb_scores, lex_scores  # noqa: E402

SPEC = ROOT / "reviews" / "integration" / "POSTHOC_SPEC_R112.md"
SPEC_SHA = "ae2600fcf39cf2d626c449835dbbf4dde308cc2e1b07d3e1991d566f920564a6"
OUT = ROOT / "reviews" / "v19" / "results" / "posthoc_f1.json"
GATES = {"easy_monitor": 0.7835, "easy_sup_emb": 0.6083, "hard_whole_emb": 0.6186}
TOL = 0.05


def r4(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)


def paired(base, arm, y, g):
    it, cl = boot_item(base, arm, y), boot_cluster(base, arm, y, g)
    return {"delta": r4(auroc(arm, y) - auroc(base, y)), "item_ci": it, "persona_ci": cl,
            "both_exclude_zero": bool(it.get("excludes_zero") and cl.get("excludes_zero"))}


def main():
    assert hashlib.sha256(SPEC.read_bytes()).hexdigest() == SPEC_SHA, "the spec file changed after its hash was ledgered"
    items, blind, idxT, _ = load_e1()
    res = {"meta": {"script": "reviews/v19/tools/posthoc_f1_wholemap.py", "spec_sha256": SPEC_SHA, "model_calls": 0, "n_boot": N_BOOT, "seed": SEED,
                    "status": "post hoc, specified before recomputation", "reader": "whole-map embedding lookup: max cosine of the question over every attribute name of the summary's name map (run_nb6 'all', FOK-6 / NB-5)"},
           "gates": {}, "populations": {}}
    for rid, label, filt in (("R-FOK-EASY-FRB", "FR-Bank easy tier", lambda it: it["tier"] == "easy" and it["backend"] == "frbank"),
                             ("R-FOK-FRB", "FR-Bank hard tier (307)", POPULATIONS["R-FOK-FRB"]["filt"])):
        sub = [it for it in items if filt(it)]
        rows = nb6_build(sub, blind, idxT, "fok", "TRUE")
        y = np.array([r["y"] for r in rows], int); g = np.array([r["persona"] for r in rows])
        mon = np.array([r["monitor"] for r in rows], float)
        sup = np.array(emb_scores(rows, "sup"), float); whole = np.array(emb_scores(rows, "all"), float)
        lexw = np.array(lex_scores(rows, "all"), float)
        d = {"label": label, "n": len(rows), "pos": int(y.sum()), "personas": int(len(set(g.tolist()))),
             "mean_map_names_per_item": r4(np.mean([len(r["all"]) for r in rows])), "mean_sup_names_per_item": r4(np.mean([len(r["sup"]) for r in rows])),
             "monitor_indexed": r4(auroc(mon, y)), "lookup_sup_embedding": r4(auroc(sup, y)),
             "lookup_whole_embedding": r4(auroc(whole, y)), "lookup_whole_lexical": r4(auroc(lexw, y)),
             "lookup_whole_embedding_ci_persona": boot_cluster_single(whole, y, g),
             "model_minus_whole_embedding": paired(whole, mon, y, g), "model_minus_sup_embedding": paired(sup, mon, y, g),
             "whole_minus_sup_embedding": paired(sup, whole, y, g)}
        d["reading"] = ("reliable margin: both intervals of model minus whole-map exclude zero" if d["model_minus_whole_embedding"]["both_exclude_zero"]
                        else "not reliable: an interval of model minus whole-map includes zero")
        d["within_tolerance"] = bool(abs(d["model_minus_whole_embedding"]["delta"]) <= TOL)
        res["populations"][rid] = d
    e, h = res["populations"]["R-FOK-EASY-FRB"], res["populations"]["R-FOK-FRB"]
    res["gates"] = {"easy_monitor": e["monitor_indexed"], "easy_sup_emb": e["lookup_sup_embedding"], "hard_whole_emb": h["lookup_whole_embedding"]}
    for k, v in GATES.items():
        assert res["gates"][k] == v, f"GATE {k}: {res['gates'][k]} != {v}"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1, ensure_ascii=False))
    for rid, d in res["populations"].items():
        m = d["model_minus_whole_embedding"]
        print(f"{d['label']}: n {d['n']} pos {d['pos']}  monitor {d['monitor_indexed']:.4f}  sup-emb {d['lookup_sup_embedding']:.4f}  whole-emb {d['lookup_whole_embedding']:.4f} "
              f"(persona CI [{d['lookup_whole_embedding_ci_persona']['ci_lo']:.4f},{d['lookup_whole_embedding_ci_persona']['ci_hi']:.4f}])  whole-lex {d['lookup_whole_lexical']:.4f}  "
              f"model-whole {m['delta']:+.4f} item [{m['item_ci']['ci_lo']:+.4f},{m['item_ci']['ci_hi']:+.4f}] persona [{m['persona_ci']['ci_lo']:+.4f},{m['persona_ci']['ci_hi']:+.4f}]  -> {d['reading']}; "
              f"map names/item {d['mean_map_names_per_item']}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
