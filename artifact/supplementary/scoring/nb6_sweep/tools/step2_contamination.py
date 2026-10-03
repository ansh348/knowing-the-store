"""Step 2: contamination sweep. Length and TRUE-name recall held at the base list; a negative's
own scrubbed attribute name is injected into the summary that negative reads, at target rates
0.00 / 0.10 / 0.232 / 0.40 / 0.49 of ALL negatives (0.232 is BELIEVED's measured rate over all 661
negatives; 0.49 its rate on the PRESENT negatives, 85 of 174, added after the first run so the
realistic operating point is inside the measured range).

Store-faithful injection. A store-derived summary can only name attributes the store holds, so
a negative is eligible when one of its own names is a real name of its store version (PRESENT
items always; ablation-ABSENT items when a same-named entry survives the ablation; natural-absent
probes never). One own name per chosen negative (BELIEVED-named negatives carry 1.09 on
average), chosen at random among the eligible ones. Lists are per summary, so on the 661 an
injection into a shared summary can name a second negative that reads it; the achieved rate is
the census figure and injection stops when it is as close to the target as one more step allows.
Seed 42 is the reading of record; seeds 43-46 print for the 0.232 cell as descriptive spread.

Both lookup variants, whole population and per-state slices (each ledger's own convention),
paired item-level and persona-clustered bootstrap against the base list, wider interval governs.

Usage: python nb6_sweep/tools/step2_contamination.py
Writes nb6_sweep/results/step2_contamination.json
"""
from __future__ import annotations

import collections
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sweep_common import (OUT, SEED, inject, jdump, load_661, load_cf2, pools,  # noqa: E402
                          prime_embeddings, score_cell, store_names, strip_scores)

RATES = (0.0, 0.10, 0.232, 0.40, 0.49)      # 0.49: BELIEVED's rate on PRESENT negatives (85 of 174)
EXTRA_SEEDS = (43, 44, 45, 46)


def main():
    r661, rcf2 = load_661(), load_cf2()
    own_pool, dis_pool, _ = pools(r661 + rcf2)
    prime_embeddings(r661 + rcf2, own_pool, dis_pool)
    res = {"design": __doc__, "rates": RATES, "seed": SEED, "cells": {}}
    for pop, rows in (("cf2", rcf2), ("661", r661)):
        base_lists = {r["key"]: list(r["base"]) for r in rows}
        base = score_cell(rows, base_lists)
        base_scores = base["_scores"]
        res["cells"][pop] = {"base": strip_scores(base)}
        n_neg = sum(1 for r in rows if r["y"] == 0)
        n_elig = sum(1 for r in rows if r["y"] == 0 and set(r["own"]) & store_names(r))
        res["cells"][pop]["n_neg"], res["cells"][pop]["n_eligible_negatives"] = n_neg, n_elig
        print(f"\n=== {pop}: n {len(rows)}, negatives {n_neg}, eligible for injection {n_elig} "
              f"(max rate {n_elig / n_neg:.3f}); base emb {base['emb']['auroc']:.4f} lex {base['lex']['auroc']:.4f}, "
              f"sup slice emb {base['emb']['auroc_superseded']:.4f} lex {base['lex']['auroc_superseded']:.4f}")
        print(f"{'rate':>6s} {'achieved':>9s} {'n_inj':>5s} {'len':>5s} | {'emb':>7s} {'sup':>7s} {'d':>8s} {'CI(wider)':>20s} | "
              f"{'lex':>7s} {'sup':>7s} {'d':>8s} {'CI(wider)':>20s} | pos_named neg_named")
        for rate in RATES:
            lists, meta = inject(rows, base_lists, rate, SEED)
            cell = score_cell(rows, lists, base_scores, boot=(rate > 0))
            rec = strip_scores(cell)
            rec["injection"] = meta
            res["cells"][pop][f"rate_{rate}"] = rec
            c = rec["census"]
            e, l = rec["emb"], rec["lex"]

            def ci(v):
                g = v.get("ci_governing")
                return f"[{g['ci_lo']:+.4f},{g['ci_hi']:+.4f}]{'*' if g['excludes_zero'] else ' '}" if g else " " * 20

            print(f"{rate:6.3f} {meta['achieved_rate']:9.3f} {meta['n_injected']:5d} {c['mean_len']:5.2f} | "
                  f"{e['auroc']:7.4f} {e['auroc_superseded']:7.4f} {e.get('delta_vs_base', 0):+8.4f} {ci(e):>20s} | "
                  f"{l['auroc']:7.4f} {l['auroc_superseded']:7.4f} {l.get('delta_vs_base', 0):+8.4f} {ci(l):>20s} | "
                  f"{c['pos_own_named']:.3f}     {c['neg_own_named_all']:.3f}")
            if rate > 0:
                print(f"{'':6s} sup-slice paired d: emb {e['sup_delta_vs_base']:+.4f} {ci({'ci_governing': e['sup_ci_governing']})}  "
                      f"lex {l['sup_delta_vs_base']:+.4f} {ci({'ci_governing': l['sup_ci_governing']})}")
        # descriptive spread at BELIEVED's rate
        spread = []
        for sd in EXTRA_SEEDS:
            lists, meta = inject(rows, base_lists, 0.232, sd)
            cell = score_cell(rows, lists)
            spread.append({"seed": sd, "achieved_rate": meta["achieved_rate"],
                           "emb": cell["emb"]["auroc"], "emb_sup": cell["emb"]["auroc_superseded"],
                           "lex": cell["lex"]["auroc"], "lex_sup": cell["lex"]["auroc_superseded"]})
        res["cells"][pop]["rate_0.232_extra_seeds"] = spread
        print(f"  seeds 43-46 at 0.232 (descriptive): emb " + ", ".join(f"{x['emb']:.4f}" for x in spread)
              + "; sup " + ", ".join(f"{x['emb_sup']:.4f}" for x in spread)
              + "; lex " + ", ".join(f"{x['lex']:.4f}" for x in spread))
    jdump(res, OUT / "step2_contamination.json")
    print(f"\nwrote {OUT / 'step2_contamination.json'}")


if __name__ == "__main__":
    main()
