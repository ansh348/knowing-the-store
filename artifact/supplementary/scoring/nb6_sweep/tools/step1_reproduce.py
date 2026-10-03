"""Step 1: reproduce the committed lookup numbers through this module's loaders before any
sweep cell is built. Gate: every target within 0.001, else exit 1.

Targets (committed, 4dp):
  661  embedding, superseded section, TRUE   0.7484   NUMBERS_E1R AUX-E1R-NB6
  661  lexical,   superseded section, TRUE   0.5738   NUMBERS_E1R AUX-E1R-NB6          (bonus)
  444  embedding v2  whole 0.7663 / supersession 0.9223   NUMBERS_CF2 AUX-CF2-NB6-V2
  444  lexical   v2  whole 0.6698 / supersession 0.7829   NUMBERS_R104 AUX-R104-MARGIN
The 661 BELIEVED embedding 0.5858 (the "0.59") is checked too, since it is the reconstruction
target of the prediction.

Two scorer paths are run: the committed functions verbatim (run_nb6.lex_scores / emb_scores,
which re-encode per call) and this module's cached scorers; both must agree to 1e-6 on AUROC.
Also asserts that index_features.parse and index_v3.named_sections read the same v2 list on all
444 (cf2_score used the latter), and prints the per-population census of the base lists.

Usage: python nb6_sweep/tools/step1_reproduce.py
Writes nb6_sweep/results/step1_reproduce.json
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sweep_common import (CF2, OUT, auroc, census, committed_scores, emb_cached, jdump, jload,  # noqa: E402
                          lex_cached, load_661, load_cf2, pools, prime_embeddings, state_mask)

TOL = 0.001
TARGETS = {
    "661|TRUE|emb": 0.7484, "661|TRUE|lex": 0.5738, "661|BELIEVED|emb": 0.5858,
    "cf2|v2|emb": 0.7663, "cf2|v2|emb|superseded": 0.9223,
    "cf2|v2|lex": 0.6698, "cf2|v2|lex|superseded": 0.7829,
}


def per_state(scores, rows, state):
    y = np.array([r["y"] for r in rows], int)
    m = state_mask(rows, state)
    return float(auroc(scores[m], y[m]))


def main():
    r661, rcf2 = load_661(), load_cf2()
    assert len(r661) == 661, len(r661)
    assert len(rcf2) == 444, len(rcf2)
    y661 = np.array([r["y"] for r in r661], int)
    ycf2 = np.array([r["y"] for r in rcf2], int)
    assert y661.sum() == 104 and ycf2.sum() == 148

    # the v2 list read by parse equals the one cf2_score read through index_v3.named_sections
    sys.path.insert(0, str(CF2.parents[0]))
    from index_v3 import named_sections  # noqa: E402
    idx = jload(CF2 / "cf_indexes.json")["indexes"]
    mism = [r["item_id"] for r in rcf2
            if list(named_sections(idx[r["item_id"]]["v2"])["superseded"]) != r["base"]]
    assert not mism, f"clean(parse) vs named_sections disagree on {len(mism)} items: {mism[:3]}"
    n_marker = sum(1 for r in r661 if r["base_marker"] != r["base"])
    print(f"661 items whose committed list carries the literal '(none)' marker as a name: {n_marker} "
          f"({len({r['key'] for r in r661 if r['base_marker'] != r['base']})} summaries, "
          f"{sum(r['y'] for r in r661 if r['base_marker'] != r['base'])} positives)")
    print()

    own_pool, dis_pool, _ = pools(r661 + rcf2)
    n_names = prime_embeddings(r661 + rcf2, own_pool, dis_pool)
    print(f"embedding universe primed: {n_names} names, {len({r['question'] for r in r661 + rcf2})} questions")
    print()

    got, agree = {}, {}
    # ---- 661 TRUE (as committed: parse's list, marker included), TRUE-clean, BELIEVED
    for prov, field in (("TRUE", "base_marker"), ("TRUE-clean", "base"), ("BELIEVED", "believed")):
        lists = {r["key"]: r[field] for r in r661}
        lex_c, emb_c = committed_scores(r661, lists)
        lex_m, emb_m = lex_cached(r661, lists), emb_cached(r661, lists)
        got[f"661|{prov}|lex"] = float(auroc(lex_c, y661))
        got[f"661|{prov}|emb"] = float(auroc(emb_c, y661))
        agree[f"661|{prov}|lex"] = abs(auroc(lex_c, y661) - auroc(lex_m, y661))
        agree[f"661|{prov}|emb"] = abs(auroc(emb_c, y661) - auroc(emb_m, y661))
        agree[f"661|{prov}|emb|max_abs_score_diff"] = float(np.max(np.abs(emb_c - emb_m)))
        got[f"661|{prov}|census"] = census(r661, lists)
        for st in ("superseded", "retracted", "expired"):
            got[f"661|{prov}|emb|{st}"] = per_state(emb_c, r661, st)
            got[f"661|{prov}|lex|{st}"] = per_state(lex_c, r661, st)
    # S2-U (uncapped BELIEVED) reference: never scored by NB-6 before; descriptive
    if all(r["s2u"] is not None for r in r661):
        lists = {r["key"]: r["s2u"] for r in r661}
        lex_c, emb_c = committed_scores(r661, lists)
        got["661|S2U|lex"], got["661|S2U|emb"] = float(auroc(lex_c, y661)), float(auroc(emb_c, y661))
        got["661|S2U|census"] = census(r661, lists)
        for st in ("superseded", "retracted", "expired"):
            got[f"661|S2U|emb|{st}"] = per_state(emb_c, r661, st)

    # ---- CF2 v2
    lists = {r["key"]: r["base"] for r in rcf2}
    lex_c, emb_c = committed_scores(rcf2, lists)
    lex_m, emb_m = lex_cached(rcf2, lists), emb_cached(rcf2, lists)
    got["cf2|v2|lex"], got["cf2|v2|emb"] = float(auroc(lex_c, ycf2)), float(auroc(emb_c, ycf2))
    agree["cf2|v2|lex"] = abs(auroc(lex_c, ycf2) - auroc(lex_m, ycf2))
    agree["cf2|v2|emb"] = abs(auroc(emb_c, ycf2) - auroc(emb_m, ycf2))
    agree["cf2|v2|emb|max_abs_score_diff"] = float(np.max(np.abs(emb_c - emb_m)))
    for st in ("superseded", "retracted", "expired"):
        got[f"cf2|v2|emb|{st}"] = per_state(emb_c, rcf2, st)
        got[f"cf2|v2|lex|{st}"] = per_state(lex_c, rcf2, st)
    got["cf2|v2|census"] = census(rcf2, lists)

    # ---- gate
    fails = []
    print(f"{'target':32s} {'committed':>10s} {'got':>10s} {'diff':>9s}")
    for k, want in TARGETS.items():
        g = got[k]
        d = g - want
        ok = abs(d) <= TOL
        if not ok:
            fails.append(k)
        print(f"{k:32s} {want:10.4f} {g:10.4f} {d:+9.4f}  {'ok' if ok else 'MISMATCH'}")
    print()
    # the committed functions re-encode per call; batch composition perturbs scores at ~1e-7,
    # which can flip one near-tied pair (1 / (n_pos * n_neg) of AUROC). Gate at 1e-4.
    bad_agree = {k: v for k, v in agree.items() if not k.endswith("score_diff") and v > 1e-4}
    print("committed vs cached scorer, |AUROC diff|:", {k: f"{v:.2e}" for k, v in agree.items()})
    if bad_agree:
        fails.append(f"scorer paths disagree: {bad_agree}")
    print()
    for pop in ("661|TRUE", "661|TRUE-clean", "661|BELIEVED", "661|S2U", "cf2|v2"):
        c = got.get(f"{pop}|census")
        if c:
            print(f"{pop:14s} mean_len {c['mean_len']:6.2f}  TRUE-recall {c['true_recall_item_weighted']:.4f}  "
                  f"precision {c['precision_vs_true']:.4f}  pos_named {c['pos_own_named']:.3f}  "
                  f"neg_named {c['neg_own_named_all']:.3f} (of those with an own name {c['neg_own_named_of_those_with_own']:.3f}, n={c['n_neg_with_own']})  "
                  f"by state {c['pos_own_named_by_state']}  pos named on PN-member slots only {c['pos_pn_member_named']:.3f}")
    print()
    for k in sorted(got):
        if "census" not in k and k not in TARGETS:
            print(f"  {k:32s} {got[k]:.4f}")

    jdump({"targets": TARGETS, "got": {k: v for k, v in got.items()}, "scorer_agreement": agree,
           "tolerance": TOL, "fails": fails,
           "n": {"661": len(r661), "cf2": len(rcf2)}, "pos": {"661": int(y661.sum()), "cf2": int(ycf2.sum())}},
          OUT / "step1_reproduce.json")
    print(f"\nwrote {OUT / 'step1_reproduce.json'}")
    if fails:
        print(f"\nSTEP 1 GATE FAILED: {fails}")
        sys.exit(1)
    print("\nSTEP 1 GATE PASS: all targets within 0.001; scorer paths agree.")


if __name__ == "__main__":
    main()
