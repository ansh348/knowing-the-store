# -*- coding: utf-8 -*-
"""r125_readers.py -- Task 1, step 0: every reader's score vector on the 444, from the recorded rows and the committed no-model readers.
NO MODEL CALL. $0. Writes reviews/r125/results/r125_vectors.json ({reader: {label, summary, source, gate, got, vector{item_id: score}}}).

Every vector is gated on its recorded whole-set pooled AUROC (four decimals) where one is ledgered; a mismatch is a STOP. Readers:

  Table 1 / the appendix's counterfactual table (tab:counterfactual), three summaries:
    GPT-4.1 mini one draw (t = 0)          cf2/rows/rows_MINI.jsonl       INDEXED-V2 / -V3 / -V2R       AUX-CF2-MINI-V2/-V3/-V2R
    GPT-4.1 mini five draws (default t)    reviews/r122/rows/rows_MINI5.jsonl  INDEXED-V2 / -V3         AUX-R122-K5-*
    Haiku 4.5 five draws (+ draw 1, v2)    cf2/rows/rows_H45.jsonl        INDEXED-V2 / -V3 / -V2R       AUX-CF2-H45-*
    Opus 5 five draws (+ draw 1, v2, v3)   cf2/rows/rows_OP5.jsonl        INDEXED-V2 / -V3 / -V2R       AUX-CF2-OP5-*, AUX-R110-A3
    GPT-5.6 Luna, Sol five draws (+ draw 1)  cf2/rows/rows_LUNA.jsonl, rows_SOL.jsonl  INDEXED-V2     AUX-CF2-OAI-LUNA-V2, -SOL-V2
    name lookup (v2), all-states lookup (v3), whole name-map lookup (v2)   score_cf.matcher              AUX-CF2-NB6-V2, -ALLSTATES-V3, -NB5
    count readers (v2, v2r): category-guessing, category-aware, state-aware, totals, category-given share   a1_count_readers.reader_scores
  E2 (names against counts): Haiku counts-only / names-only; mini counts-only / names-only / names-only dash   cf2/rows/rows_*_nc.jsonl
  the moved-count control (v2r-cat): mini k=1, Haiku k=5, Opus k=5 (+ draw 1), Luna k=5, Sol k=5 (+ draw 1); the state-aware and totals readers on the moved texts
  E10 the hybrid reader (cf2_hybrid.py's fit reproduced: leave-persona-out logistic regression on the lookup, the share and the assigned indicator)
  the intent-explicit rerun (R122 T4): Luna k=5, mini k=1            reviews/r122/rows/rows_P1LUNA.jsonl, rows_P1MINI.jsonl
  the lookup under two further encoders (mpnet, bge-small; v2, v3) and the random-token control (MiniLM; v2, v3)   enc_lookup.py's functions
"""
from __future__ import annotations

import sys
import time

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r125_common as C  # noqa: E402
from r125_common import CF2, V2C, R122, ROOT, STATES, auroc, r4  # noqa: E402
from index_features import parse as parse_index  # noqa: E402
from index_v3 import named_sections  # noqa: E402
import score_cf as S  # noqa: E402
import cf2_score  # noqa: E402,F401  (sets S.R82 = cf2 at import)
from a1_count_readers import reader_scores  # noqa: E402

OUT = C.RESULTS / "r125_vectors.json"
MINILM = "sentence-transformers/all-MiniLM-L6-v2"
ENCODERS = {"MPNET": "sentence-transformers/all-mpnet-base-v2", "BGE": "BAAI/bge-small-en-v1.5"}


def add(res, key, label, summary, source, gate, vec, cell, note=None):
    ok = ~np.isnan(vec)
    got = r4(auroc(vec[ok], cell.y[ok]))
    if gate is not None:
        assert got == gate, f"GATE {key}: got {got} != recorded {gate} -- STOP"
    res[key] = {"label": label, "summary": summary, "source": source, "gate": gate, "got": got, "covered": int(ok.sum()),
                "distinct_values": int(len(np.unique(np.round(vec[ok], 6)))), "vector": {i: (None if np.isnan(x) else float(x)) for i, x in zip(cell.ids, vec)}}
    if note:
        res[key]["note"] = note
    print(f"  {key:22s} {label:52s} {summary:8s} pooled {got}  gate {gate}  covered {int(ok.sum())}")


def lane_vec(cell, path, arm, draw=None):
    if draw is None:
        col, census = C.collapse(path, arm)
    else:
        col, census = C.draw_k(path, arm, draw), None
    return cell.vector(col), census


def count_reader_vecs(cell, texts_by_item):
    keys = ("CR-nb1", "CR-oracle-a", "CR-oracle-state", "CR-totals-a", "CR-oracle-share")
    out = {k: np.zeros(444) for k in keys}
    for k, it in enumerate(cell.items):
        d = reader_scores(texts_by_item[it["item_id"]], it["question"], cell.cats[k], it["state"])
        for key in keys:
            out[key][k] = d[key]
    return out


def hybrid_vec(cell):
    from sklearn.linear_model import LogisticRegression
    import cf2_reader_score as R
    from cf2_hybrid import nb1_share
    f1 = R.lookup_v2(cell.items, cell.idx)
    f2 = np.zeros(444); f3 = np.zeros(444)
    for k, it in enumerate(cell.items):
        f2[k], f3[k] = nb1_share(cell.idx[it["item_id"]]["v2"], it["question"])
    assert r4(auroc(f2, cell.y)) == 0.6623
    v = np.full(444, np.nan); g, y = cell.g, cell.y
    for persona in sorted(set(g)):
        tr, te = g != persona, g == persona
        mu = np.array([f1[tr].mean(), f2[tr].mean()]); sd = np.array([f1[tr].std(), f2[tr].std()]); sd[sd == 0] = 1.0
        X = np.column_stack([(f1 - mu[0]) / sd[0], (f2 - mu[1]) / sd[1], f3])
        clf = LogisticRegression(C=1.0, penalty="l2", solver="lbfgs", max_iter=1000).fit(X[tr], y[tr])
        v[te] = clf.predict_proba(X[te])[:, 1]
    assert not np.isnan(v).any()
    return v


def main():
    t0 = time.time()
    cell = C.Cell()
    res = {}
    print("recorded lanes")
    L = {  # key, label, summary, path, arm, gate
        "MINI1_v2": ("GPT-4.1 mini, one draw (t = 0)", "v2", CF2 / "rows/rows_MINI.jsonl", "INDEXED-V2", 0.7167),
        "MINI1_v3": ("GPT-4.1 mini, one draw (t = 0)", "v3", CF2 / "rows/rows_MINI.jsonl", "INDEXED-V3", 0.7967),
        "MINI1_v2r": ("GPT-4.1 mini, one draw (t = 0)", "v2r", CF2 / "rows/rows_MINI.jsonl", "INDEXED-V2R", 0.7179),
        "MINI5_v2": ("GPT-4.1 mini, five draws (provider default t)", "v2", R122 / "rows/rows_MINI5.jsonl", "INDEXED-V2", 0.7648),
        "MINI5_v3": ("GPT-4.1 mini, five draws (provider default t)", "v3", R122 / "rows/rows_MINI5.jsonl", "INDEXED-V3", 0.8323),
        "H45_v2": ("Haiku 4.5, five draws", "v2", CF2 / "rows/rows_H45.jsonl", "INDEXED-V2", 0.7566),
        "H45_v3": ("Haiku 4.5, five draws", "v3", CF2 / "rows/rows_H45.jsonl", "INDEXED-V3", 0.8773),
        "H45_v2r": ("Haiku 4.5, five draws", "v2r", CF2 / "rows/rows_H45.jsonl", "INDEXED-V2R", 0.7638),
        "OP5_v2": ("Opus 5, five draws", "v2", CF2 / "rows/rows_OP5.jsonl", "INDEXED-V2", 0.8405),
        "OP5_v3": ("Opus 5, five draws", "v3", CF2 / "rows/rows_OP5.jsonl", "INDEXED-V3", 0.9079),
        "OP5_v2r": ("Opus 5, five draws", "v2r", CF2 / "rows/rows_OP5.jsonl", "INDEXED-V2R", 0.8353),
        "LUNA_v2": ("GPT-5.6 Luna, five draws", "v2", CF2 / "rows/rows_LUNA.jsonl", "INDEXED-V2", 0.8417),
        "SOL_v2": ("GPT-5.6 Sol, five draws", "v2", CF2 / "rows/rows_SOL.jsonl", "INDEXED-V2", 0.8500),
        # E2 arms (the superseded-only summary with lines removed)
        "H45_COUNTS": ("Haiku 4.5, counts only (E2)", "v2-counts", CF2 / "rows/rows_H45_nc.jsonl", "INDEXED-COUNTS", 0.5945),
        "H45_NAMES": ("Haiku 4.5, names only (E2)", "v2-names", CF2 / "rows/rows_H45_nc.jsonl", "INDEXED-NAMES", 0.7507),
        "MINI1_COUNTS": ("GPT-4.1 mini, counts only (E2)", "v2-counts", CF2 / "rows/rows_MINI_nc.jsonl", "INDEXED-COUNTS", 0.5862),
        "MINI1_NAMES": ("GPT-4.1 mini, names only (E2)", "v2-names", CF2 / "rows/rows_MINI_nc.jsonl", "INDEXED-NAMES", 0.7103),
        "MINI1_NAMES_DASH": ("GPT-4.1 mini, names only, dash rule (E2)", "v2-names", CF2 / "rows/rows_MINI_nc.jsonl", "INDEXED-NAMES-DASH", 0.6891),
        # the moved-count control
        "MINI1_v2rcat": ("GPT-4.1 mini, one draw, moved count", "v2rcat", V2C / "rows/rows_MINI.jsonl", "INDEXED-V2R-CAT", 0.7410),
        "H45_v2rcat": ("Haiku 4.5, five draws, moved count", "v2rcat", V2C / "rows/rows_H45.jsonl", "INDEXED-V2R-CAT", 0.7525),
        "OP5_v2rcat": ("Opus 5, five draws, moved count (E1 Amendment 1)", "v2rcat", V2C / "rows/rows_OP5.jsonl", "INDEXED-V2R-CAT", 0.8075),
        "LUNA_v2rcat": ("GPT-5.6 Luna, five draws, moved count (E9)", "v2rcat", V2C / "rows/rows_LUNA.jsonl", "INDEXED-V2R-CAT", 0.8121),
        "SOL_v2rcat": ("GPT-5.6 Sol, five draws, moved count (E9)", "v2rcat", V2C / "rows/rows_SOL.jsonl", "INDEXED-V2R-CAT", 0.8172),
        # the intent-explicit rerun (R122 T4)
        "LUNA5_P1_v2": ("GPT-5.6 Luna, five draws, intent-explicit rubric (R122 T4)", "v2", R122 / "rows/rows_P1LUNA.jsonl", "INDEXED-V2", 0.8531),
        "MINI1_P1_v2": ("GPT-4.1 mini, one draw, intent-explicit rubric (R122 T4)", "v2", R122 / "rows/rows_P1MINI.jsonl", "INDEXED-V2", 0.7253),
    }
    for key, (label, summ, path, arm, gate) in L.items():
        vec, census = lane_vec(cell, path, arm)
        add(res, key, label, summ, f"{path.relative_to(ROOT)} {arm} (collapsed)", gate, vec, cell)
        res[key]["census"] = census
    print("draw-1 rows of the five-draw lanes")
    D = {
        "H45_v2_d1": ("Haiku 4.5, draw 1", "v2", CF2 / "rows/rows_H45.jsonl", "INDEXED-V2", 0.7555),
        "OP5_v2_d1": ("Opus 5, draw 1", "v2", CF2 / "rows/rows_OP5.jsonl", "INDEXED-V2", 0.8400),
        "OP5_v3_d1": ("Opus 5, draw 1", "v3", CF2 / "rows/rows_OP5.jsonl", "INDEXED-V3", None),
        "LUNA_v2_d1": ("GPT-5.6 Luna, draw 1", "v2", CF2 / "rows/rows_LUNA.jsonl", "INDEXED-V2", None),
        "SOL_v2_d1": ("GPT-5.6 Sol, draw 1", "v2", CF2 / "rows/rows_SOL.jsonl", "INDEXED-V2", None),
        "OP5_v2rcat_d1": ("Opus 5, draw 1, moved count", "v2rcat", V2C / "rows/rows_OP5.jsonl", "INDEXED-V2R-CAT", 0.8049),
        "LUNA_v2rcat_d1": ("GPT-5.6 Luna, draw 1, moved count", "v2rcat", V2C / "rows/rows_LUNA.jsonl", "INDEXED-V2R-CAT", None),
        "SOL_v2rcat_d1": ("GPT-5.6 Sol, draw 1, moved count", "v2rcat", V2C / "rows/rows_SOL.jsonl", "INDEXED-V2R-CAT", None),
        "MINI5_v2_d1": ("GPT-4.1 mini, draw 1 of five (provider default t)", "v2", R122 / "rows/rows_MINI5.jsonl", "INDEXED-V2", None),
        "MINI5_v3_d1": ("GPT-4.1 mini, draw 1 of five (provider default t)", "v3", R122 / "rows/rows_MINI5.jsonl", "INDEXED-V3", None),
    }
    for key, (label, summ, path, arm, gate) in D.items():
        vec, _ = lane_vec(cell, path, arm, draw=1)
        add(res, key, label, summ, f"{path.relative_to(ROOT)} {arm} draw 1", gate, vec, cell, note=None if gate is not None else "no recorded whole-set gate; descriptive")

    print("no-model readers: the lookups")
    sup2 = [named_sections(cell.idx[i]["v2"])["superseded"] for i in cell.ids]
    s3 = [named_sections(cell.idx[i]["v3"]) for i in cell.ids]
    all3 = [s["superseded"] + s["retracted"] + s["expired"] for s in s3]
    whole = [sorted({n for lst in parse_index(cell.idx[i]["v2"])["attr_by_cat"].values() for n in lst}) for i in cell.ids]
    add(res, "LOOKUP_v2", "Name lookup (superseded-names list, MiniLM)", "v2", "score_cf.matcher on the v2 superseded-names lists", 0.7663, np.asarray(S.matcher(cell.qs, sup2), float), cell)
    add(res, "ALLSTATES_v3", "All-states lookup (three named sections, MiniLM)", "v3", "score_cf.matcher on the v3 superseded+retracted+expired lists", 0.8756, np.asarray(S.matcher(cell.qs, all3), float), cell)
    add(res, "WHOLEMAP_v2", "Whole name-map lookup (MiniLM)", "v2", "score_cf.matcher on every name of the v2 map", 0.5776, np.asarray(S.matcher(cell.qs, whole), float), cell)

    print("no-model readers: the count readers on v2, v2r and the moved-count texts")
    cr_label = {"CR-nb1": ("Count reader, guessed category (share; CR-nb1)", 0.6623), "CR-oracle-a": ("Count reader, given category (retracted+expired; CR-oracle-a)", 0.6043),
                "CR-oracle-state": ("State-aware count reader (the state's own cell; CR-oracle-state)", 0.8580), "CR-totals-a": ("Totals reader (the two lifecycle totals; CR-totals-a)", 0.5603),
                "CR-oracle-share": ("Category-given share reader (privileged, post hoc; CR-oracle-share)", 0.8473)}
    v2texts = {i: cell.idx[i]["v2"] for i in cell.ids}
    for k, v in count_reader_vecs(cell, v2texts).items():
        add(res, f"{k}_v2", cr_label[k][0], "v2", "a1_count_readers.reader_scores on the v2 texts", cr_label[k][1], v, cell)
    v2rtexts = {i: cell.idx[i]["v2r"] for i in cell.ids}
    gates_v2r = {"CR-nb1": 0.6623, "CR-oracle-a": 0.6043, "CR-oracle-state": 0.8580, "CR-totals-a": 0.4472, "CR-oracle-share": 0.8473}
    for k, v in count_reader_vecs(cell, v2rtexts).items():
        add(res, f"{k}_v2r", cr_label[k][0], "v2r", "a1_count_readers.reader_scores on the v2r texts", gates_v2r[k], v, cell)
    cat_texts = C.jload(V2C / "build/texts_v2rcat.json")
    cattexts = {i: cat_texts[f"{i}|INDEXED-V2R-CAT"] for i in cell.ids}
    for k, v in count_reader_vecs(cell, cattexts).items():
        if k in ("CR-oracle-state", "CR-totals-a", "CR-nb1", "CR-oracle-a", "CR-oracle-share"):
            add(res, f"{k}_v2rcat", cr_label[k][0], "v2rcat", "a1_count_readers.reader_scores on the moved-count texts (texts_v2rcat.json)", None, v, cell,
                note="per-state gates: state-aware 0.3028 / 0.3611 and totals 0.4044 / 0.3894 (AUX-V2RCAT-REF) asserted in r125_matched.py")

    print("E10 the hybrid reader")
    add(res, "HYBRID_v2", "Hybrid reader (E10; lookup + share + assigned, leave-persona-out logistic)", "v2", "cf2_hybrid.py's fit reproduced (no model call)", 0.7865, hybrid_vec(cell), cell)

    print("the lookup under further encoders, and the random-token control (enc_lookup.py's functions)")
    import enc_lookup as E
    names = sorted({n for lst in sup2 + all3 for n in lst})
    tok = {n: E.random_token(n) for n in names}
    assert len(set(tok.values())) == len(tok)
    tok2 = [[tok[n] for n in lst] for lst in sup2]; tok3 = [[tok[n] for n in lst] for lst in all3]
    add(res, "RANDTOK_v2", "Random-token lookup (names replaced by stable tokens; MiniLM)", "v2", "score_cf.matcher on the token lists (enc_lookup.random_token, seed 42)", 0.5954, np.asarray(S.matcher(cell.qs, tok2), float), cell)
    add(res, "RANDTOK_v3", "Random-token lookup (all-states list; MiniLM)", "v3", "score_cf.matcher on the token lists (enc_lookup.random_token, seed 42)", 0.5479, np.asarray(S.matcher(cell.qs, tok3), float), cell)
    enc_gates = {"MPNET": {"v2": 0.7605, "v3": 0.8646}, "BGE": {"v2": 0.7584, "v3": 0.8690}}
    for code, model in ENCODERS.items():
        E.set_encoder(model)
        add(res, f"{code}_v2", f"Name lookup under {model.split('/')[-1]}", "v2", f"score_cf.matcher with the encoder swapped ({model})", enc_gates[code]["v2"], np.asarray(S.matcher(cell.qs, sup2), float), cell)
        add(res, f"{code}_v3", f"All-states lookup under {model.split('/')[-1]}", "v3", f"score_cf.matcher with the encoder swapped ({model})", enc_gates[code]["v3"], np.asarray(S.matcher(cell.qs, all3), float), cell)
    E.set_encoder(MINILM)

    C.jdump({"meta": {"script": "reviews/r125/tools/r125_readers.py", "model_calls": 0, "n_readers": len(res), "seconds": round(time.time() - t0, 1),
                      "collapse": "mean over >= 3 OK draws (X4); k = 1 lanes their single draw; draw-1 rows draw 1 alone"}, "readers": res}, OUT)
    print(f"{len(res)} readers -> {OUT.relative_to(ROOT)} ({time.time() - t0:.0f} s)")


if __name__ == "__main__":
    main()
