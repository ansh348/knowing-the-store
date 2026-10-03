"""Step 4: recall sweep at L = 15, the synthetic distractor cell, the three-factor decomposition
corners, the BELIEVED reconstruction check, and the seed-robustness spot check.

Recall sweep: L = 15, own-store untargeted fillers, contamination 0 (the base's own rate), TRUE-name
recall forced to 1.00 / 0.70 / 0.50 / 0.3604 / 0.2996 / 0.10 by seeded (summary, name) drops on
the item-weighted micro-recall (the ledger's definition); 0.2996 is the ledger's BELIEVED value
(marker in the denominator, the prediction's cell of record), 0.3604 the marker-corrected one.
Distractor cell: L = 15, recall 1.0, contamination 0, half the fillers drawn from OTHER personas'
stores (names absent from this store) -- a labelled synthetic reference, occurring in no backend.

Decomposition corners (both populations; the partition is the 661's gap to BELIEVED's 0.5858):
every combination of length in {base, 15}, contamination in {base, 0.232}, recall in {1.0, r}
for r in {0.3604, 0.2996}. Order inside a cell: recall drop, then injection, then padding.
Shapley attribution over the three factors from the eight corners, and the interaction
(total gap minus the sum of the three single-factor deltas).

Reconstruction check: the four cells with recall at a BELIEVED value and L = 15 -- with
contamination at base (the prediction of record, section 0) and at 0.232 -- against the
measured BELIEVED list: margin, and the paired (cell - BELIEVED) bootstrap, both conventions,
wider governs. Seeds 43-46 (descriptive, no bootstrap) on L15, the two Lr cells and the two
cLr cells.

Usage: python nb6_sweep/tools/step4_recall.py
Writes nb6_sweep/results/step4_recall.json
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sweep_common import (OUT, SEED, auroc, boot_cluster, boot_item, jdump, load_661, load_cf2,  # noqa: E402
                          make_cell, pools, prime_embeddings, score_cell, strip_scores)

RECALLS = (1.0, 0.70, 0.50, 0.3604, 0.2996, 0.10)
R_BEL = (0.3604, 0.2996)
L15, C_BEL = 15, 0.232
EXTRA_SEEDS = (43, 44, 45, 46)
BELIEVED_EMB = 0.5858


def ci(v, key="ci_governing"):
    g = v.get(key)
    return f"[{g['ci_lo']:+.4f},{g['ci_hi']:+.4f}]{'*' if g['excludes_zero'] else ' '}" if g else " " * 20


def shapley(corners, v):
    """corners: {(L, c, r) in {0,1}^3: auroc}. Returns per-factor Shapley value of (full - base)."""
    names = ("L", "c", "r")
    out = {n: 0.0 for n in names}
    for perm in itertools.permutations(range(3)):
        state = [0, 0, 0]
        prev = corners[tuple(state)][v]
        for f in perm:
            state[f] = 1
            cur = corners[tuple(state)][v]
            out[names[f]] += (cur - prev) / 6.0
            prev = cur
    return out


def paired_vs(rows, cell_scores, ref_scores):
    y = np.array([r["y"] for r in rows], int)
    g = np.array([r["persona"] for r in rows])
    out = {}
    for v in ("emb", "lex"):
        a, b = cell_scores[v], ref_scores[v]
        it, cl = boot_item(b, a, y), boot_cluster(b, a, y, g)
        wide = it if (it["ci_hi"] - it["ci_lo"]) >= (cl["ci_hi"] - cl["ci_lo"]) else cl
        out[v] = {"cell": float(auroc(a, y)), "ref": float(auroc(b, y)), "delta": float(auroc(a, y) - auroc(b, y)),
                  "ci_item": it, "ci_persona": cl,
                  "ci_governing": {"which": "item" if wide is it else "persona", "ci_lo": wide["ci_lo"],
                                   "ci_hi": wide["ci_hi"], "excludes_zero": wide["excludes_zero"]}}
    return out


def main():
    r661, rcf2 = load_661(), load_cf2()
    own_pool, dis_pool, _ = pools(r661 + rcf2)
    prime_embeddings(r661 + rcf2, own_pool, dis_pool)
    res = {"design": __doc__, "seed": SEED, "recalls": RECALLS, "cells": {}}
    for pop, rows in (("cf2", rcf2), ("661", r661)):
        P = res["cells"][pop] = {}
        base_lists, _ = make_cell(rows, own_pool, dis_pool)
        base = score_cell(rows, base_lists)
        bs = base["_scores"]
        P["base"] = strip_scores(base)
        print(f"\n=== {pop}: base emb {base['emb']['auroc']:.4f} (sup {base['emb']['auroc_superseded']:.4f})  lex {base['lex']['auroc']:.4f}")
        hdr = (f"{'cell':>22s} {'len':>6s} {'recall':>6s} {'pos_nm':>6s} {'neg_nm':>6s} | {'emb':>7s} {'d':>8s} {'CI(wider)':>20s} {'sup':>7s} | "
               f"{'lex':>7s} {'d':>8s} {'CI(wider)':>20s} {'sup':>7s}")
        print(hdr)

        def run(name, boot=True, **kw):
            lists, meta = make_cell(rows, own_pool, dis_pool, **kw)
            cell = score_cell(rows, lists, bs, boot=boot)
            rec = strip_scores(cell)
            rec["meta"] = meta
            P[name] = rec
            cs, e, l = rec["census"], rec["emb"], rec["lex"]
            print(f"{name:>22s} {cs['mean_len']:6.2f} {cs['true_recall_item_weighted']:6.3f} {cs['pos_own_named']:6.3f} {cs['neg_own_named_all']:6.3f} | "
                  f"{e['auroc']:7.4f} {e.get('delta_vs_base', 0):+8.4f} {ci(e):>20s} {e['auroc_superseded']:7.4f} | "
                  f"{l['auroc']:7.4f} {l.get('delta_vs_base', 0):+8.4f} {ci(l):>20s} {l['auroc_superseded']:7.4f}")
            return cell

        # ---- recall sweep at L = 15, c = 0
        for r in RECALLS:
            run(f"L15_c0_r{r}", L=L15, recall=r)
        # ---- the synthetic distractor cell
        run("L15_c0_r1.0_distractor0.5", L=L15, recall=1.0, distractor_share=0.5)
        # ---- decomposition corners
        kept = {}
        for r in R_BEL:
            for Lf, cf in itertools.product((0, 1), (0, 1)):
                name = f"L{'15' if Lf else 'base'}_c{C_BEL if cf else 0}_r{r}"
                if name in P:
                    continue
                kept[name] = run(name, L=L15 if Lf else None, recall=r, c=C_BEL if cf else 0.0)
        for name in (f"L15_c{C_BEL}_r1.0", f"Lbase_c{C_BEL}_r1.0", "L15_c0_r1.0"):
            if name not in P:
                kept[name] = run(name, L=L15 if name.startswith("L15") else None, recall=1.0,
                                 c=C_BEL if f"c{C_BEL}" in name else 0.0)
        # ---- Shapley partition per recall value, per variant, whole and sup slice
        part = {}
        for r in R_BEL:
            corners = {}
            for Lf, cf, rf in itertools.product((0, 1), repeat=3):
                name = f"L{'15' if Lf else 'base'}_c{C_BEL if cf else 0}_r{r if rf else 1.0}"
                name = name if name in P else "base"
                rec = P[name] if name != "base" else P["base"]
                corners[(Lf, cf, rf)] = {"emb": rec["emb"]["auroc"], "lex": rec["lex"]["auroc"],
                                         "emb_sup": rec["emb"]["auroc_superseded"], "lex_sup": rec["lex"]["auroc_superseded"]}
            part[str(r)] = {"corners": {f"L{k[0]}c{k[1]}r{k[2]}": v for k, v in corners.items()}}
            for v in ("emb", "lex", "emb_sup", "lex_sup"):
                full, b0 = corners[(1, 1, 1)][v], corners[(0, 0, 0)][v]
                singles = {"L": corners[(1, 0, 0)][v] - b0, "c": corners[(0, 1, 0)][v] - b0, "r": corners[(0, 0, 1)][v] - b0}
                sh = shapley(corners, v)
                part[str(r)][v] = {"base": b0, "full": full, "total_gap": full - b0, "single_factor_deltas": singles,
                                   "sum_of_singles": sum(singles.values()), "interaction": (full - b0) - sum(singles.values()),
                                   "shapley": sh, "shapley_share": {k: (x / (full - b0) if full != b0 else None) for k, x in sh.items()}}
            e = part[str(r)]["emb"]
            print(f"  partition r={r} emb: base {e['base']:.4f} -> full {e['full']:.4f} gap {e['total_gap']:+.4f}; "
                  f"singles L {e['single_factor_deltas']['L']:+.4f} c {e['single_factor_deltas']['c']:+.4f} r {e['single_factor_deltas']['r']:+.4f} "
                  f"(sum {e['sum_of_singles']:+.4f}, interaction {e['interaction']:+.4f}); Shapley L {e['shapley']['L']:+.4f} c {e['shapley']['c']:+.4f} r {e['shapley']['r']:+.4f}")
        P["partition"] = part

        # ---- reconstruction check against the measured BELIEVED list (661 only)
        if pop == "661":
            bel_lists = {x["key"]: list(x["believed"]) for x in rows}
            bel = score_cell(rows, bel_lists)
            P["believed_measured"] = strip_scores(bel)
            rec_chk = {}
            for r in R_BEL:
                for cname in (f"L15_c0_r{r}", f"L15_c{C_BEL}_r{r}"):
                    cell = kept.get(cname)
                    if cell is None:
                        lists, _ = make_cell(rows, own_pool, dis_pool, L=L15, recall=r, c=0.0)
                        cell = score_cell(rows, lists)
                    pv = paired_vs(rows, cell["_scores"], bel["_scores"])
                    rec_chk[cname] = {"vs_believed": pv, "within_0.05_emb": bool(abs(pv["emb"]["delta"]) <= 0.05),
                                      "census": P[cname]["census"]}
                    print(f"  reconstruction {cname:>18s}: emb {pv['emb']['cell']:.4f} vs BELIEVED {pv['emb']['ref']:.4f} "
                          f"d {pv['emb']['delta']:+.4f} {ci(pv['emb'])}  lex {pv['lex']['cell']:.4f} vs {pv['lex']['ref']:.4f} d {pv['lex']['delta']:+.4f} {ci(pv['lex'])}")
            P["reconstruction"] = rec_chk

        # ---- the second operating point: uncapped BELIEVED (S2-U) as a composite of its own measured
        #      store properties (L 32 ~ 32.55, TRUE-name recall 0.8010, contamination 0.400), vs the measured S2-U list
        if pop == "661" and all(x.get("s2u") is not None for x in rows):
            s2u_lists = {x["key"]: list(x["s2u"]) for x in rows}
            s2u = score_cell(rows, s2u_lists)
            P["s2u_measured"] = strip_scores(s2u)
            comp = run("composite_S2U_L32_c0.4_r0.801", L=32, recall=0.8010, c=0.400)
            pv = paired_vs(rows, comp["_scores"], s2u["_scores"])
            P["composite_s2u"] = {"vs_s2u": pv, "census_s2u_measured": P["s2u_measured"]["census"],
                                  "within_0.05_emb": bool(abs(pv["emb"]["delta"]) <= 0.05)}
            print(f"  composite S2-U: emb {pv['emb']['cell']:.4f} vs measured S2-U {pv['emb']['ref']:.4f} d {pv['emb']['delta']:+.4f} {ci(pv['emb'])}  "
                  f"lex {pv['lex']['cell']:.4f} vs {pv['lex']['ref']:.4f} d {pv['lex']['delta']:+.4f} {ci(pv['lex'])}")

        # ---- seed robustness (descriptive)
        spread = {}
        for cname, kw in (("L15_c0_r1.0", dict(L=L15)),
                          (f"L15_c0_r0.3604", dict(L=L15, recall=0.3604)), (f"L15_c0_r0.2996", dict(L=L15, recall=0.2996)),
                          (f"L15_c{C_BEL}_r0.3604", dict(L=L15, recall=0.3604, c=C_BEL)), (f"L15_c{C_BEL}_r0.2996", dict(L=L15, recall=0.2996, c=C_BEL)),
                          ("composite_S2U_L32_c0.4_r0.801", dict(L=32, recall=0.8010, c=0.400))):
            if cname not in P:
                continue
            spread[cname] = []
            for sd in EXTRA_SEEDS:
                lists, meta = make_cell(rows, own_pool, dis_pool, seed=sd, **kw)
                cell = score_cell(rows, lists)
                cs = cell["census"]
                spread[cname].append({"seed": sd, "emb": cell["emb"]["auroc"], "emb_sup": cell["emb"]["auroc_superseded"],
                                      "lex": cell["lex"]["auroc"], "recall": cs["true_recall_item_weighted"],
                                      "pos_named": cs["pos_own_named"], "neg_named": cs["neg_own_named_all"]})
            print(f"  seeds 43-46 {cname:>18s}: emb " + ", ".join(f"{x['emb']:.4f}" for x in spread[cname])
                  + f"  (seed 42: {P[cname]['emb']['auroc']:.4f})")
        P["seed_spread"] = spread
    jdump(res, OUT / "step4_recall.json")
    print(f"\nwrote {OUT / 'step4_recall.json'}")


if __name__ == "__main__":
    main()
