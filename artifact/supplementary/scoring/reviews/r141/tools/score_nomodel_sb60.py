# -*- coding: utf-8 -*-
"""score_nomodel_sb60.py -- R141 Phase 0.3 (2026-09-24; $0, no model call; the values are RECORDED before the freeze, not predicted).

The five no-model readers on PN-60 against SB-60 over the 88 supersession pairs, matched (W/T/L, (W + T/2)/88, the triple-level and persona-grouped
intervals: 1,000 draws, seed 42, reviews/r125/tools/r125_common's estimators through r125_t45_score.matched) with the pooled AUROC over the 176 items
beside it; and each on SB-60 against the padded PRESENT version (the list-length component, descriptive, as R125 read it).
  the embedding name lookup    NB-6's emb_cached (MiniLM max cosine) on the printed lists; PN-60 and PRESENT from cf_pad/results/lookup_vectors.json 'padded'
  the lexical lookup           lex_cached; the same source
  the random-token lookup      enc_lookup.random_token per name, score_cf.matcher (the R125 / R136 control)
  the length-only reader       the number of names in the superseded-names section (R139)
  the count reader             a1_count_readers.reader_scores 'CR-nb1' (guessed category) on each version's own text
The PN-60 lookups are recomputed here on the printed lists and asserted equal to the recorded R136 vectors.
Writes reviews/r141/results/nomodel_sb60.json. Usage: python reviews/r141/tools/score_nomodel_sb60.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[3]
for p in ("reviews/r125/tools", "cf_pad/tools", "pad_probe/tools", "nb6_sweep/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
import r125_t45_score as T  # noqa: E402
import cf_pad_common as CP  # noqa: E402
import pad_common as PC  # noqa: E402
from sweep_common import emb_cached, lex_cached  # noqa: E402

OUT = ROOT / "reviews" / "r141" / "results" / "nomodel_sb60.json"


def J(rel):
    return json.load(open(ROOT / rel, encoding="utf-8"))


def main():
    C = T.C
    cell = C.Cell()
    B = J("reviews/r141/build/build_sb60.json")
    pad = J("cf_pad/build/texts.json")
    LV = J("cf_pad/results/lookup_vectors.json")
    pos = {k: i for i, k in enumerate(LV["keys"])}
    rows = B["rows"]
    pids = [r["pair_id"] for r in rows]
    gp = np.array([cell.pair_persona[p] for p in pids])
    qs = [r["question"] for r in rows]
    lists = {}
    for p in pids:
        for v, key in (("PN", f"{p}|PN"), ("PRESENT", f"{p}|PRESENT"), ("SB60", f"{p}|SB60")):
            text = pad[key] if v != "SB60" else B["texts"][key]
            lists[(p, v)] = PC.committed_names(text)
    V = {}
    for v in ("PN", "PRESENT", "SB60"):
        rr = [{"key": f"{p}|{v}", "question": q} for p, q in zip(pids, qs)]
        lk = {f"{p}|{v}": lists[(p, v)] for p in pids}
        V.setdefault("Name lookup (embedding)", {})[v] = emb_cached(rr, lk)
        V.setdefault("Lexical lookup", {})[v] = lex_cached(rr, lk)
    # the PN-60 and PRESENT lookups equal the recorded R136 vectors
    for name, src in (("Name lookup (embedding)", "emb"), ("Lexical lookup", "lex")):
        for v in ("PN", "PRESENT"):
            rec = np.array([LV["padded"][src][pos[f"{p}|{v}"]] for p in pids], float)
            assert np.allclose(rec, V[name][v], atol=1e-6), (name, v)
    # the random-token lookup: one token per distinct name, the R125 map (its gate asserted inside r125_t45_score's own module on its own lists)
    import enc_lookup as E
    import score_cf as S
    names = sorted({n for lst in lists.values() for n in lst})
    tok = {n: E.random_token(n) for n in names}
    assert len(set(tok.values())) == len(tok)
    V["Random-token lookup"] = {v: np.asarray(S.matcher(qs, [[tok[n] for n in lists[(p, v)]] for p in pids]), float) for v in ("PN", "PRESENT", "SB60")}
    for v in ("PN", "PRESENT"):
        rec = np.array([LV["padded"]["randtok"][pos[f"{p}|{v}"]] for p in pids], float)
        assert np.allclose(rec, V["Random-token lookup"][v], atol=1e-6), ("randtok", v)
    V["Length-only reader"] = {v: np.array([len(lists[(p, v)]) for p in pids], float) for v in ("PN", "PRESENT", "SB60")}
    cat = {r["pair_id"]: r["category"] for r in rows}
    def cr(text, p, q):
        return T.reader_scores(text, q, cat[p], "SUPERSESSION")["CR-nb1"]
    V["Count reader, guessed category"] = {
        "PN": np.array([cr(pad[f"{p}|PN"], p, q) for p, q in zip(pids, qs)], float),
        "PRESENT": np.array([cr(pad[f"{p}|PRESENT"], p, q) for p, q in zip(pids, qs)], float),
        "SB60": np.array([cr(B["texts"][f"{p}|SB60"], p, q) for p, q in zip(pids, qs)], float)}
    assert np.array_equal(V["Count reader, guessed category"]["PN"], V["Count reader, guessed category"]["SB60"])
    out = {"meta": {"script": "reviews/r141/tools/score_nomodel_sb60.py", "model_calls": 0, "n_pairs": len(pids), "n_boot": C.N_BOOT, "seed": C.SEED,
                    "sb60_texts_sha256": B["meta"]["texts_sha256"], "recorded_before_freeze": True}, "readers": {}}
    for name, d in V.items():
        ones, zeros = np.ones(len(pids)), np.zeros(len(pids))
        out["readers"][name] = {
            "pn60_vs_sb60": T.matched(d["PN"], d["SB60"], gp),
            "pooled_pn60_vs_sb60": T.r4(T.auroc(np.concatenate([d["PN"], d["SB60"]]), np.concatenate([ones, zeros]))),
            "sb60_vs_present": T.matched(d["SB60"], d["PRESENT"], gp),
            "means": {v: T.r4(float(np.mean(d[v]))) for v in d}}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    C.jdump(out, OUT)
    for name, r in out["readers"].items():
        m, s = r["pn60_vs_sb60"], r["sb60_vs_present"]
        print(f"{name:32s} PN-60 vs SB-60 {m['W']:2d}/{m['T']:2d}/{m['L']:2d} matched {m['matched']:.4f} [{m['ci_triple']['ci_lo']:.4f},{m['ci_triple']['ci_hi']:.4f}] "
              f"[{m['ci_persona']['ci_lo']:.4f},{m['ci_persona']['ci_hi']:.4f}] pooled {r['pooled_pn60_vs_sb60']:.4f} | SB-60 vs PRESENT {s['matched']:.4f} ({s['W']}/{s['T']}/{s['L']})")


if __name__ == "__main__":
    main()
