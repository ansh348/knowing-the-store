"""NB-6: the superseded-names matcher, over the SAME committed serialized indexes.

Registered in registrations/ADDENDUM_R81.md, frozen at HEAD 2bb7fd9 before any score here
existed. R81 Phase 1.

The question NB-6 answers. Under the TRUE index, is the monitor's NOK judgment close to
reading the answer off one section of the index it is shown, the flat list under
`ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT`? NB-4 and NB-5 cannot answer it: they match the
question against the WHOLE per-category name map, which dilutes exactly the signal at issue.

    NOK-6  max sim(question, name) over the superseded-names section
    FOK-6  max sim(question, name) over the whole per-category name map

Each in two variants, lexical (Jaccard, NB-4's tokenizer) and embedding (NB-5's local offline
encoder). Unsupervised and intent-blind: no gold intent, no gold label, no tier, no category
ground truth is read here.

DECLARED IDENTITY (ADDENDUM_R81 section 3, D-E1R-7). FOK-6 lexical IS NB-4 and FOK-6
embedding IS NB-5, by construction: same name list, same tokenizer, same encoder, same
estimator. FOK-6 is therefore not a prediction. It is a reproduction check against the
committed baselines_final.json at four decimal places, and this file asserts it.

WHY THIS IS A SEPARATE FILE and not an edit to run_baselines.py: re-running run_baselines
would recompute NB-1..NB-5, whose values are committed and printed. This file reads those
values and never recomputes them, so the published suite cannot drift underneath the addition.

Usage: python e1r_robustness/tools/run_nb6.py
Writes results/nb6.json. Exit 1 if the reproduction check fails at 4dp.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_e1r import OUT, POPULATIONS, auroc, jload, jdump, load_e1   # noqa: E402
from index_features import index_key, indexes, parse, toks              # noqa: E402
from run_baselines import encoder, jac                                  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TOL = 0.05          # inherited from the count-destruction probe, as the E1-R suite uses
DP = 4              # reproduction check precision (ADDENDUM_R81 section 3)

# The two registered rows, plus the coverage row that carries only the reproduction check.
ROWS = {
    "R-NOK-FRB": "nok",
    "R-FOK-FRB": "fok",
}


# ------------------------------------------------------------------ name lists
def name_lists(item, provenance):
    """(superseded_names, all_map_names) for one item's exact index string.

    Both come from index_features.parse, so NB-6 reads the index through the same parser
    NB-1/NB-2/NB-4 read it through. An inexpressible index yields two empty lists: the
    literal 'not expressible by this backend' is a marker, not an attribute name, and
    scoring against it would measure the marker.
    """
    p = parse(indexes().get(index_key(item, provenance)))
    if not p["expressible"]:
        return [], []
    sup = list(p["superseded_attrs"])
    alln = [a for v in p["attr_by_cat"].values() for a in v]
    return sup, alln


# ------------------------------------------------------------------ similarity
def lex_scores(rows, field):
    """Max Jaccard over content-token sets. NB-4's tokenizer and NB-4's jac()."""
    out = []
    for r in rows:
        qt = toks(r["question"])
        out.append(max((jac(qt, toks(a.replace("_", " "))) for a in r[field]), default=0.0))
    return out


def emb_scores(rows, field):
    """Max cosine against the local offline encoder. Mirrors run_baselines.embed_scores."""
    uniq_q = sorted({r["question"] for r in rows})
    uniq_a = sorted({a for r in rows for a in r[field]})
    if not uniq_a:
        return [0.0] * len(rows)
    enc = encoder()
    qv = enc.encode(uniq_q, normalize_embeddings=True, batch_size=128,
                    show_progress_bar=False)
    av = enc.encode([a.replace("_", " ") for a in uniq_a], normalize_embeddings=True,
                    batch_size=256, show_progress_bar=False)
    qi = {q: k for k, q in enumerate(uniq_q)}
    ai = {a: k for k, a in enumerate(uniq_a)}
    out = []
    for r in rows:
        if not r[field]:
            out.append(0.0)
            continue
        idx = [ai[a] for a in r[field]]
        out.append(float(np.max(av[idx] @ qv[qi[r["question"]]])))
    return out


# ------------------------------------------------------------------ assembly
def build(items, blind, indexed, judgment, provenance):
    """Join one population exactly as run_baselines.build does, plus the two name lists."""
    rows = []
    for it in items:
        q, tag = it["question"], it["item_id"]
        if q not in blind or tag not in indexed:
            continue
        bv, iv = blind[q].get(judgment), indexed[tag].get(judgment)
        if bv is None or iv is None:
            continue
        lab = it.get("label", it["label_pre"])
        y = (0 if lab == "ABSENT" else 1) if judgment == "fok" \
            else (1 if lab == "PRESENT-NEGATIVE" else 0)
        sup, alln = name_lists(it, provenance)
        rows.append({"y": y, "persona": it["persona"], "item_id": tag, "question": q,
                     "monitor": iv, "sup": sup, "all": alln})
    return rows


def score_population(rows, judgment):
    y = np.array([r["y"] for r in rows], int)
    field = "sup" if judgment == "nok" else "all"
    lex = auroc(lex_scores(rows, field), y)
    emb = auroc(emb_scores(rows, field), y)
    mon = auroc([r["monitor"] for r in rows], y)
    best = max(lex, emb)
    return {
        "n": len(rows), "n_pos": int(y.sum()),
        "field": ("superseded-names section" if judgment == "nok"
                  else "per-category name map"),
        "nb6_lexical": float(lex), "nb6_embedding": float(emb),
        "nb6_best": float(best),
        "nb6_best_variant": "lexical" if lex >= emb else "embedding",
        "monitor_indexed_auroc": float(mon),
        "monitor_minus_nb6_best": float(mon - best),
        "nb6_matches_monitor": bool(abs(mon - best) < TOL),
        "nb6_beats_monitor": bool(best > mon + TOL),
        "mean_names_per_item": float(np.mean([len(r[field]) for r in rows])),
        "items_with_no_names": int(sum(1 for r in rows if not r[field])),
    }


# ------------------------------------------------------------------ matched-84
def matched84():
    """Descriptive only (ADDENDUM_R81 section 4): NB-6 on the 84-item authorship-matched set.

    Carries no prediction. The monitor comparators for this set are the cross-vendor rows in
    e1xv_crossvendor, not a single number, so nothing here is subtracted from a monitor. The
    manifest supplies y_nok directly and every item is an frbank FULL key, so no join is
    needed.
    """
    man = jload(ROOT / "e1xv_crossvendor" / "manifests" / "cell_84.json")
    out = {}
    for prov in ("TRUE", "BELIEVED"):
        rows = []
        for it in man["items"]:
            item = {"backend": it["item_id"].split(":")[0], "persona": it["persona"],
                    "variant": it["variant"], "question_id": None}
            sup, alln = name_lists(item, prov)
            rows.append({"y": it["y_nok"], "question": it["question"],
                         "sup": sup, "all": alln})
        y = np.array([r["y"] for r in rows], int)
        lex, emb = auroc(lex_scores(rows, "sup"), y), auroc(emb_scores(rows, "sup"), y)
        out[prov] = {
            "n": len(rows), "n_pos": int(y.sum()),
            "nb6_lexical": float(lex), "nb6_embedding": float(emb),
            "nb6_best": float(max(lex, emb)),
            "nb6_best_variant": "lexical" if lex >= emb else "embedding",
            "judgment": "nok", "status": "DESCRIPTIVE, carries no prediction",
        }
        print(f"  matched-84  {prov:9s} n={len(rows):4d}  lex={lex:.4f} emb={emb:.4f} "
              f"best={max(lex, emb):.4f}   [descriptive]")
    return out


# ------------------------------------------------------------------ main
def main():
    items, blind, idxT, idxB = load_e1()
    committed = jload(ROOT / "e1r_robustness" / "results" / "baselines_final.json")

    results, fails = {}, []

    for rid, judgment in ROWS.items():
        spec = POPULATIONS[rid]
        sub = [it for it in items if spec["filt"](it)]
        for prov, idx in (("TRUE", idxT), ("BELIEVED", idxB)):
            rows = build(sub, blind, idx, judgment, prov)
            if not rows or len(set(r["y"] for r in rows)) < 2:
                continue
            rec = score_population(rows, judgment)
            rec.update({"row": rid, "provenance": prov, "judgment": judgment})
            key = f"{rid}|{prov}"
            results[key] = rec

            # ---- the FOK reproduction check (ADDENDUM_R81 section 3) ----------------
            if judgment == "fok":
                legit = committed["rows"][key]["legitimate_baselines"]
                for variant, ref in (("nb6_lexical", "NB-4 lexical match"),
                                     ("nb6_embedding", "NB-5 embedding match")):
                    got, want = round(rec[variant], DP), round(legit[ref], DP)
                    rec[f"reproduces_{ref.split()[0]}"] = bool(got == want)
                    rec[f"{variant}_vs_committed_abs"] = abs(rec[variant] - legit[ref])
                    if got != want:
                        fails.append(f"REPRODUCTION {key} {variant}: {got} != {want} "
                                     f"({ref} in baselines_final.json) at {DP}dp")

            mark = ""
            if rec["nb6_beats_monitor"]:
                mark = "   <-- NB-6 WINS"
            elif rec["nb6_matches_monitor"]:
                mark = "   <-- matches"
            print(f"  {rid:11s} {prov:9s} n={rec['n']:4d}  monitor={rec['monitor_indexed_auroc']:.4f} "
                  f" lex={rec['nb6_lexical']:.4f} emb={rec['nb6_embedding']:.4f} "
                  f" best={rec['nb6_best']:.4f}  mon-best={rec['monitor_minus_nb6_best']:+.4f}{mark}")

    m84 = matched84()

    # ---- registered predictions ------------------------------------------------------
    nok_t = results.get("R-NOK-FRB|TRUE", {})
    nok_b = results.get("R-NOK-FRB|BELIEVED", {})
    verdicts = {
        "NB6-1": {
            "statement": "monitor NOK-TRUE exceeds best NB-6 NOK-TRUE by more than the tolerance",
            "monitor": nok_t.get("monitor_indexed_auroc"),
            "nb6_best": nok_t.get("nb6_best"),
            "margin": nok_t.get("monitor_minus_nb6_best"),
            "outcome": "HOLDS" if (nok_t.get("monitor_minus_nb6_best", 0) > TOL) else "FAILS",
        },
        "NB6-2": {
            "statement": "monitor NOK-BELIEVED and best NB-6 NOK-BELIEVED are within the tolerance",
            "monitor": nok_b.get("monitor_indexed_auroc"),
            "nb6_best": nok_b.get("nb6_best"),
            "margin": nok_b.get("monitor_minus_nb6_best"),
            "outcome": "HOLDS" if nok_b.get("nb6_matches_monitor") else "FAILS",
        },
    }
    if verdicts["NB6-2"]["outcome"] == "FAILS":
        verdicts["NB6-2"]["direction"] = (
            "monitor" if verdicts["NB6-2"]["margin"] > TOL else "matcher")

    jdump({"rows": results,
           "matched_84_descriptive": m84,
           "verdicts": verdicts,
           "tolerance": TOL,
           "reproduction_dp": DP,
           "reproduction_failures": fails,
           "encoder": "sentence-transformers/all-MiniLM-L6-v2 (local, offline)",
           "registration": "registrations/ADDENDUM_R81.md @ 2bb7fd9 (+ Amendment 1, da0d4a0)",
           "note": ("FOK-6 is definitionally NB-4/NB-5 and is a reproduction check, not a "
                    "prediction; see ADDENDUM_R81 section 3 and D-E1R-7.")},
          OUT / "nb6.json")

    print()
    for k, v in verdicts.items():
        print(f"  {k}  {v['outcome']:6s}  monitor={v['monitor']:.4f} "
              f"nb6_best={v['nb6_best']:.4f} margin={v['margin']:+.4f}"
              + (f"  (against the {v['direction']})" if v.get("direction") else ""))
    print()
    if fails:
        print(f"REPRODUCTION CHECK FAILED ({len(fails)}):")
        for f in fails:
            print("  ", f)
    else:
        print(f"reproduction check: FOK-6 reproduces NB-4 and NB-5 at {DP}dp on both arms.")
    print(f"wrote {OUT / 'nb6.json'}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
