"""Step 3: length sweep. L in {base, 5, 10, 15, 30, 60}; fillers are the persona's own-store
attribute names that no scored question of that persona targets (either population), drawn from
a per-summary seeded permutation so the sweep is nested; no TRUE name is ever dropped; seed 42.

Run once at contamination 0 (length isolated; on the 661 "0" is the base list's own 0.039), then
L in {15, 30, 32, 60} at c = 0.232 (BELIEVED's rate over all negatives) to see whether length and
contamination add or interact: interaction = d(L, c) - [d(L, 0) + d(base, c)], on AUROC.

Paired item-level and persona-clustered bootstrap against the marker-stripped base for every
cell, 1000 draws, seed 42, single-class draws discarded, 2.5 / 97.5, the wider interval governs.

Usage: python nb6_sweep/tools/step3_length.py
Writes nb6_sweep/results/step3_length.json
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sweep_common import (LENGTHS, OUT, SEED, jdump, load_661, load_cf2, make_cell, pools,  # noqa: E402
                          prime_embeddings, score_cell, strip_scores)

C_INTERACT = 0.232
L_INTERACT = (15, 30, 32, 60)


def ci(v, key="ci_governing"):
    g = v.get(key)
    return f"[{g['ci_lo']:+.4f},{g['ci_hi']:+.4f}]{'*' if g['excludes_zero'] else ' '}" if g else " " * 20


def main():
    r661, rcf2 = load_661(), load_cf2()
    own_pool, dis_pool, targets = pools(r661 + rcf2)
    prime_embeddings(r661 + rcf2, own_pool, dis_pool)
    res = {"design": __doc__, "seed": SEED, "lengths": LENGTHS, "c_interact": C_INTERACT,
           "pool_sizes": {p: {"own_untargeted": len(own_pool[p]), "targeted": len(targets.get(p, ())),
                              "distractor": len(dis_pool[p])} for p in sorted(own_pool)},
           "cells": {}}
    for pop, rows in (("cf2", rcf2), ("661", r661)):
        base_lists, _ = make_cell(rows, own_pool, dis_pool)
        base = score_cell(rows, base_lists)
        bs = base["_scores"]
        P = res["cells"][pop] = {}
        print(f"\n=== {pop}: base emb {base['emb']['auroc']:.4f} (sup {base['emb']['auroc_superseded']:.4f})  "
              f"lex {base['lex']['auroc']:.4f} (sup {base['lex']['auroc_superseded']:.4f})")
        print(f"{'cell':>14s} {'len':>6s} {'recall':>6s} {'pos_nm':>6s} {'neg_nm':>6s} | {'emb':>7s} {'d':>8s} {'CI(wider)':>20s} {'sup':>7s} {'d_sup':>8s} | "
              f"{'lex':>7s} {'d':>8s} {'CI(wider)':>20s} {'sup':>7s}")
        for c in (0.0, C_INTERACT):
            Ls = (None,) + tuple(LENGTHS) if c == 0.0 else (None,) + tuple(L_INTERACT)
            for L in Ls:
                lists, meta = make_cell(rows, own_pool, dis_pool, L=L, c=c)
                is_base = (L is None and c == 0.0)
                cell = score_cell(rows, lists, bs, boot=not is_base)
                rec = strip_scores(cell)
                rec["meta"] = meta
                name = f"L{L if L else 'base'}_c{c}"
                P[name] = rec
                cs, e, l = rec["census"], rec["emb"], rec["lex"]
                print(f"{name:>14s} {cs['mean_len']:6.2f} {cs['true_recall_item_weighted']:6.3f} {cs['pos_own_named']:6.3f} {cs['neg_own_named_all']:6.3f} | "
                      f"{e['auroc']:7.4f} {e.get('delta_vs_base', 0):+8.4f} {ci(e):>20s} {e['auroc_superseded']:7.4f} {e.get('sup_delta_vs_base', 0):+8.4f} | "
                      f"{l['auroc']:7.4f} {l.get('delta_vs_base', 0):+8.4f} {ci(l):>20s} {l['auroc_superseded']:7.4f}")
        # interaction on AUROC: d(L,c) - [d(L,0) + d(base,c)]
        inter = {}
        dc = {v: P[f"Lbase_c{C_INTERACT}"][v]["delta_vs_base"] for v in ("emb", "lex")}
        for L in L_INTERACT:
            inter[f"L{L}"] = {}
            for v in ("emb", "lex"):
                dL = P[f"L{L}_c0.0"][v]["delta_vs_base"]
                dLc = P[f"L{L}_c{C_INTERACT}"][v]["delta_vs_base"]
                inter[f"L{L}"][v] = {"d_L": dL, "d_c": dc[v], "d_Lc": dLc, "additive_prediction": dL + dc[v],
                                     "interaction": dLc - (dL + dc[v])}
        P["interaction"] = inter
        print("  interaction d(L,c) - [d(L,0) + d(base,c)]: " +
              "; ".join(f"L{L} emb {inter[f'L{L}']['emb']['interaction']:+.4f} lex {inter[f'L{L}']['lex']['interaction']:+.4f}" for L in L_INTERACT))
    jdump(res, OUT / "step3_length.json")
    print(f"\nwrote {OUT / 'step3_length.json'}")


if __name__ == "__main__":
    main()
