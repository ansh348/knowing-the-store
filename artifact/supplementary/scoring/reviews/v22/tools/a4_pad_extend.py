# -*- coding: utf-8 -*-
"""a4_pad_extend.py -- CC_PASS_v18 A4: the superseded-names lookup at 100 and 200 padded names on the 661 TRUE lists.
NO MODEL CALL. $0. Extends the recorded padding check (ADDENDUM_PAD section 3; Table 16 at 15 / 30 / 60 names) to 100
and 200 correct names no scored question targets, both lookup variants (run_nb6's embedding and lexical scorers through
sweep_common.committed_scores), no model.

Two pool readings, both computed (the author's amendment 4 of 2026-09-14):
  (ii) pool A only: the store's own printed map names less the committed section, the persona's targeted slots and
       colon names (pad_common.build_pools pool_a). These are "correct names for this store". A key whose pool A holds
       fewer than L - |committed| names is padded to the maximum available; the per-key N and its distribution print.
       This reading carries the Section 5 and box sentence.
  (i)  the registered draw order (pool A, then pool B = other personas' names; pad_common.draw_order) to exactly 100 and
       200 names, printing how many keys spill into pool B. This reading extends Table 16's rows (15 / 30 / 60 were drawn
       the same way; three keys spilled at 60) and is reported there with the spill count, not in prose.

pad_common.padded_lists is fixed to LENGTHS = (15, 30, 60), so the nesting is re-implemented here on top of draw_order and
asserted byte-identical to pad_probe/build/padded_lists.json at those three lengths before 100 and 200 are drawn.
Gates: embedding 0.7298 / 0.7191 / 0.6696 and lexical 0.5772 / 0.5817 / 0.5825 at 15 / 30 / 60 (pad_scores.json), the
committed-list gate 0.7484 / 0.5738, the renderer lock 242 of 242.
Intervals: item-level and persona-clustered single-arm bootstraps (1000 draws, seed 42); the paired difference against
the committed (base) lists by cf2_score.paired (padded minus base).

Usage: python reviews/v18/tools/a4_pad_extend.py
Writes: reviews/v18/results/a4_pad_extend.json, reviews/v18/results/a4_table16_rows.tex
"""
from __future__ import annotations

import io
import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "resp_review/tools", "ds_downstream/tools", "pad_probe/tools", "nb6_sweep/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from common_e1r import N_BOOT, SEED, auroc, boot_cluster_single  # noqa: E402
import pad_common as PC  # noqa: E402
from sweep_common import committed_scores  # noqa: E402
from cf2_score import paired  # noqa: E402
sys.path.insert(0, str(ROOT / "reviews" / "v18" / "tools"))
from a1_count_readers import boot_item_single, r4  # noqa: E402

OUT = ROOT / "reviews" / "v18" / "results" / "a4_pad_extend.json"
TEX = ROOT / "reviews" / "v18" / "results" / "a4_table16_rows.tex"
RECORDED = {"emb": {15: 0.7298, 30: 0.7191, 60: 0.6696}, "lex": {15: 0.5772, 30: 0.5817, 60: 0.5825}, "base": {"emb": 0.7484, "lex": 0.5738}}
NEW = (100, 200)
STATES = ("superseded", "retracted", "expired")


def nested_lists(pools, L, pool_a_only):
    """(key -> list, key -> meta) for one L: committed names, then the draw order (pool A then B, or pool A alone)."""
    lists, meta = {}, {}
    for k, P in pools.items():
        order, n_a = PC.draw_order(k, P)
        com = list(P["committed"]); need = L - len(com)
        avail = order[:n_a] if pool_a_only else order
        pad = avail[:need]
        lst = com + pad
        assert len(set(lst)) == len(lst) and not any(":" in n for n in lst)
        lists[k] = lst
        meta[k] = {"N": len(lst), "from_pool_a": min(len(pad), n_a), "from_pool_b": max(0, len(pad) - n_a), "pool_a_size": n_a, "short_of_L": L - len(lst)}
    return lists, meta


def score(rows, lists, y, g, st):
    lx, em = committed_scores(rows, lists)
    out = {}
    for name, s in (("emb", em), ("lex", lx)):
        d = {"auroc": r4(auroc(s, y)), "item_ci": boot_item_single(s, y), "persona_ci": boot_cluster_single(s, y, g), "per_state": {}}
        for s_ in STATES:
            m = (st == s_) | (y == 0)
            d["per_state"][s_] = {"n": int(m.sum()), "pos": int(y[m].sum()), "auroc": r4(auroc(s[m], y[m]))}
        out[name] = d
    return out, {"emb": em, "lex": lx}


def main():
    assert PC.registration_ok(), "STOP: ADDENDUM_PAD registration sha256 mismatch"
    rows = PC.rows_661(); pools = PC.build_pools(rows)
    ok, bad = PC.renderer_lock(pools); assert ok == len(pools) == 242 and not bad, ("renderer lock", ok, bad)
    y = np.array([r["y"] for r in rows], int); g = np.array([r["persona"] for r in rows]); st = np.array([r["state"] or "" for r in rows])
    res = {"meta": {"script": "reviews/v18/tools/a4_pad_extend.py", "model_calls": 0, "n_boot": N_BOOT, "seed": SEED, "n_rows": len(rows), "n_keys": len(pools),
                    "per_state_convention": "this state's positives against all negatives (AUX-E1R-NB6-COMPOSITION)", "paired_sign": "padded minus base"},
           "gates": {"renderer_lock": ok}, "readings": {}}

    # base (committed lists, marker included), gated
    base_lists = {r["key"]: r["base_marker"] for r in rows}
    base, base_vec = score(rows, base_lists, y, g, st)
    for name in ("emb", "lex"):
        assert base[name]["auroc"] == RECORDED["base"][name], ("GATE base", name, base[name]["auroc"])
    res["gates"]["base"] = {n: base[n]["auroc"] for n in ("emb", "lex")}; res["base"] = base

    # byte-identity with the recorded lists at 15 / 30 / 60, then the recorded scores
    rec = json.load(io.open(PC.PAD / "build" / "padded_lists.json", encoding="utf-8"))
    for L in PC.LENGTHS:
        lists, _ = nested_lists(pools, L, pool_a_only=False)
        for k in pools:
            assert lists[k] == rec[f"{k}|{L}"], ("GATE list identity", k, L)
        sc, _ = score(rows, {r["key"]: lists[r["key"]] for r in rows}, y, g, st)
        for name in ("emb", "lex"):
            assert sc[name]["auroc"] == RECORDED[name][L], ("GATE recorded", name, L, sc[name]["auroc"])
        res["gates"][f"L{L}"] = {n: sc[n]["auroc"] for n in ("emb", "lex")}
    res["gates"]["list_identity_15_30_60"] = True

    # the two readings at 100 and 200
    for reading, pool_a_only in (("ii_pool_a_only", True), ("i_registered_order", False)):
        R = {}
        for L in NEW:
            lists, meta = nested_lists(pools, L, pool_a_only)
            sc, vec = score(rows, {r["key"]: lists[r["key"]] for r in rows}, y, g, st)
            Ns = np.array([meta[r["key"]]["N"] for r in rows]); keysN = np.array([meta[k]["N"] for k in pools])
            R[str(L)] = {"L": L, "lookups": sc,
                         "paired_vs_base": {n: paired(base_vec[n], vec[n], y, g) for n in ("emb", "lex")},
                         "names_per_item": {"mean": r4(Ns.mean()), "min": int(Ns.min()), "median": float(np.median(Ns)), "max": int(Ns.max()), "at_L": int((Ns == L).sum()), "n_rows": len(rows)},
                         "names_per_key": {"mean": r4(keysN.mean()), "min": int(keysN.min()), "median": float(np.median(keysN)), "max": int(keysN.max()), "at_L": int((keysN == L).sum()), "n_keys": len(pools)},
                         "keys_spilling_into_pool_b": int(sum(1 for k in pools if meta[k]["from_pool_b"] > 0)),
                         "names_from_pool_b_total": int(sum(meta[k]["from_pool_b"] for k in pools))}
        res["readings"][reading] = R
    res["pool_a_census"] = {"min": int(min(P["census"]["pool_a"] for P in pools.values())), "median": float(np.median([P["census"]["pool_a"] for P in pools.values()])),
                            "max": int(max(P["census"]["pool_a"] for P in pools.values())), "keys_under_100_minus_committed": int(sum(1 for P in pools.values() if P["census"]["pool_a"] + len(P["committed"]) < 100))}

    # the Table 16 rows (reading i) and the Section 5 / box sentence (reading ii)
    ii = res["readings"]["ii_pool_a_only"]; i_ = res["readings"]["i_registered_order"]
    n100, n200 = ii["100"]["names_per_item"], ii["200"]["names_per_item"]
    sentence = (f"Padded with the store's own untargeted names, the lookup reads the list at a mean of {n100['mean']:.0f} names per summary at "
                f"{ii['100']['lookups']['emb']['auroc']:.2f} and at a mean of {n200['mean']:.0f} names (every store's own pool exhausted; at most {n200['max']} names) at "
                f"{ii['200']['lookups']['emb']['auroc']:.2f}; beyond that it is untested.")
    res["section5_box_sentence"] = sentence
    tex = ["% reviews/v18/results/a4_table16_rows.tex -- A4 rows for Table 16 (tab:pad), reading (i), the registered draw order.",
           "% Columns as in Table 16: names; embedding lookup; lexical lookup. The model column is a dash (no model at these lengths).",
           f"% Caption note to add: at 100 names {i_['100']['keys_spilling_into_pool_b']} of 242 keys draw from other personas' names (pool B); at 200 every key does ({i_['200']['names_from_pool_b_total']} names in all)."]
    for L in NEW:
        e, l = i_[str(L)]["lookups"]["emb"], i_[str(L)]["lookups"]["lex"]
        tex.append(f"${L}$ & ${e['auroc']:.4f}$ & ${l['auroc']:.4f}$ & --- \\\\  % emb item [{e['item_ci']['ci_lo']:.4f},{e['item_ci']['ci_hi']:.4f}] persona [{e['persona_ci']['ci_lo']:.4f},{e['persona_ci']['ci_hi']:.4f}]")
    tex.append("% reading (ii), pool A only (the prose sentence): " + sentence)
    for L in NEW:
        e, l = ii[str(L)]["lookups"]["emb"], ii[str(L)]["lookups"]["lex"]
        tex.append(f"% pool A only, L={L}: mean N {ii[str(L)]['names_per_item']['mean']}, emb {e['auroc']:.4f}, lex {l['auroc']:.4f}")
    io.open(TEX, "w", encoding="utf-8", newline="\n").write("\n".join(tex) + "\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=1, sort_keys=True, default=float); f.write("\n")

    print("A4 pad extend -- gates:", json.dumps(res["gates"]))
    print("pool A census:", res["pool_a_census"])
    print(f"base: emb {base['emb']['auroc']} lex {base['lex']['auroc']}")
    for reading, R in res["readings"].items():
        print(f"\n== reading {reading} ==")
        for L, r in R.items():
            e, l = r["lookups"]["emb"], r["lookups"]["lex"]; pe = r["paired_vs_base"]["emb"]
            print(f"  L={L}: names/item mean {r['names_per_item']['mean']} (min {r['names_per_item']['min']}, max {r['names_per_item']['max']}, at L: {r['names_per_item']['at_L']} of {r['names_per_item']['n_rows']} rows);"
                  f" keys spilling into pool B: {r['keys_spilling_into_pool_b']} ({r['names_from_pool_b_total']} names)")
            print(f"        emb {e['auroc']:.4f} item [{e['item_ci']['ci_lo']:.4f},{e['item_ci']['ci_hi']:.4f}] persona [{e['persona_ci']['ci_lo']:.4f},{e['persona_ci']['ci_hi']:.4f}]"
                  f"  per state sup {e['per_state']['superseded']['auroc']} ret {e['per_state']['retracted']['auroc']} exp {e['per_state']['expired']['auroc']}"
                  f"  minus base {pe['delta']:+.4f} item [{pe['item_ci']['ci_lo']:+.4f},{pe['item_ci']['ci_hi']:+.4f}] persona [{pe['persona_ci']['ci_lo']:+.4f},{pe['persona_ci']['ci_hi']:+.4f}]")
            print(f"        lex {l['auroc']:.4f} item [{l['item_ci']['ci_lo']:.4f},{l['item_ci']['ci_hi']:.4f}] persona [{l['persona_ci']['ci_lo']:.4f},{l['persona_ci']['ci_hi']:.4f}]")
    print("\nsentence:", sentence)
    print("wrote", OUT.relative_to(ROOT), "and", TEX.relative_to(ROOT))


if __name__ == "__main__":
    main()
