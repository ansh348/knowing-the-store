"""
score_e1.py -- E1 Phase D: scoring, exactly per PREREG_E1 section 8.

NO interpretive additions. Metrics, gates and the bootstrap are as frozen.

  FOK AUROC   positive class = NON-ABSENT, score = FOK. Ties contribute 0.5
              (rank-based Mann-Whitney), load-bearing given E0's D20 quantisation.
  NOK AUROC   positive class = PRESENT-NEGATIVE, score = NOK. The two-step
              intermediate (nok_candidates_found rate) is reported alongside.
  ECE         10 equal-width bins; Brier; reliability diagrams.
  bootstrap   1000 paired resamples of items, seed 42, both arms moving together.

Gates read mechanically. No recommendation is produced anywhere in this file.
"""

from __future__ import annotations

import collections
import io
import json
import statistics as st
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
OUT = E1 / "results"
N_BOOT, BINS, SEED = 1000, 10, 42
SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True, default=float)
        f.write("\n")


def auroc(s, y):
    s, y = np.asarray(s, float), np.asarray(y, int)
    n1, n0 = int(y.sum()), int((1 - y).sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    o = np.argsort(s, kind="mergesort")
    r = np.empty(len(s), float)
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[o[j + 1]] == s[o[i]]:
            j += 1
        r[o[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def ece(p, y, bins=BINS):
    p, y = np.asarray(p, float), np.asarray(y, int)
    if not len(p):
        return float("nan")
    e = np.linspace(0, 1, bins + 1)
    t = 0.0
    for b in range(bins):
        m = (p >= e[b]) & ((p < e[b + 1]) if b < bins - 1 else (p <= e[b + 1]))
        if m.sum():
            t += (m.sum() / len(p)) * abs(y[m].mean() - p[m].mean())
    return float(t)


def brier(p, y):
    p, y = np.asarray(p, float), np.asarray(y, int)
    return float(np.mean((p - y) ** 2)) if len(p) else float("nan")


def boot(b, i, y, n=N_BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    b, i, y = np.asarray(b), np.asarray(i), np.asarray(y)
    d = []
    for _ in range(n):
        k = rng.integers(0, len(y), len(y))
        if y[k].sum() in (0, len(k)):
            continue
        d.append(auroc(i[k], y[k]) - auroc(b[k], y[k]))
    d = np.asarray(d)
    lo, hi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    return {"n": int(len(d)), "mean": float(d.mean()), "ci_lo": lo, "ci_hi": hi,
            "excludes_zero": bool(lo > 0 or hi < 0)}


def row(items, blind, indexed, name, judgment="fok"):
    """One gate row. items: list of item dicts. blind/indexed: {key: value}."""
    keys, y, b, i = [], [], [], []
    for it in items:
        q, tag = it["question"], it["item_id"]
        if q not in blind or tag not in indexed:
            continue
        bv, iv = blind[q].get(judgment), indexed[tag].get(judgment)
        if bv is None or iv is None:
            continue
        lab = it.get("label", it["label_pre"])
        keys.append(tag)
        y.append((0 if lab == "ABSENT" else 1) if judgment == "fok"
                 else (1 if lab == "PRESENT-NEGATIVE" else 0))
        b.append(bv); i.append(iv)
    if len(set(y)) < 2:
        return {"row": name, "n": len(y), "note": "single-class; AUROC undefined"}
    ab, ai = auroc(b, y), auroc(i, y)
    return {"row": name, "n": len(y), "n_pos": int(sum(y)),
            "blind_auroc": ab, "indexed_auroc": ai, "delta": ai - ab,
            "bootstrap": boot(b, i, y),
            "blind_ece": ece(b, y), "indexed_ece": ece(i, y),
            "blind_brier": brier(b, y), "indexed_brier": brier(i, y)}


def band(d):
    if d < 0.10:
        return "< +0.10 — re-scope"
    if d <= 0.15:
        return "+0.10 to +0.15 — modest, carried by NOK and control"
    return "> +0.15 — stands alone"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    items = [i for i in jload(E1 / "build" / "items_final.json")
             if i.get("label", i["label_pre"]) in SCOREABLE]
    joins_q = {}
    main_rows = jload(E1 / "elicitation_main.json")
    blind = {r["question"]: r for r in main_rows if r["arm"] == "BLIND" and r["status"] == "OK"}
    idxT = {r["tag"]: r for r in main_rows if r["arm"] == "INDEXED-TRUE" and r["status"] == "OK"}
    idxB = {r["tag"]: r for r in main_rows
            if r["arm"] == "INDEXED-BELIEVED" and r["status"] == "OK"}
    for it in items:
        it.setdefault("question", "")
    qmap = {r["tag"]: r["question"] for r in main_rows if r["arm"] != "BLIND"}
    for it in items:
        if not it["question"]:
            it["question"] = qmap.get(it["item_id"], "")

    res = {"n_items": len(items), "n_blind_prompts": len(blind),
           "n_indexed_true": len(idxT), "n_indexed_believed": len(idxB),
           "n_failed": sum(1 for r in main_rows if r["status"] != "OK")}

    hard = [i for i in items if i["tier"] == "hard"]
    frb_hard = [i for i in hard if i["backend"] == "frbank"]

    # ---------------- HEADLINE: H1-hard / H2-hard on the pooled hard tier
    res["H2_hard"] = row(hard, blind, idxT, "HEADLINE hard tier, indexed-TRUE")
    res["H2_hard_frbank"] = row(frb_hard, blind, idxT, "hard tier, FR-Bank only")
    h = res["H2_hard"]
    res["gates"] = {
        "H1_hard": {"threshold": "< 0.75", "observed": h.get("blind_auroc"),
                    "holds": bool(h.get("blind_auroc", 1) < 0.75)},
        "H2_hard": {"threshold": ">= +0.10 with CI excluding 0",
                    "delta": h.get("delta"),
                    "ci": [h["bootstrap"]["ci_lo"], h["bootstrap"]["ci_hi"]],
                    "holds": bool(h.get("delta", 0) >= 0.10
                                  and h["bootstrap"]["excludes_zero"]),
                    "band": band(h.get("delta", 0))},
    }

    # ---------------- per tier / backend / provenance
    res["by_tier"] = {t: row([i for i in items if i["tier"] == t], blind, idxT, f"tier={t}")
                      for t in ("easy", "hard")}
    res["by_backend"] = {}
    for b in ("frbank", "mem0", "amem"):
        sub = [i for i in items if i["backend"] == b]
        res["by_backend"][b] = {
            "TRUE": row(sub, blind, idxT, f"{b}:TRUE"),
            "BELIEVED": row(sub, blind, idxB, f"{b}:BELIEVED"),
        }

    # ---------------- H-BELIEVED: retention of the TRUE delta, per backend
    res["H_BELIEVED"] = {}
    for b, d in res["by_backend"].items():
        dt, db = d["TRUE"].get("delta"), d["BELIEVED"].get("delta")
        ret = (db / dt) if (dt and dt > 0) else None
        res["H_BELIEVED"][b] = {"true_delta": dt, "believed_delta": db,
                                "retention": ret,
                                "holds_ge_60pct": bool(ret is not None and ret >= 0.60)}

    # ---------------- lifecycle-ablation decomposition (named analysis)
    res["lifecycle_decomposition"] = {
        "amem_believed": res["by_backend"]["amem"]["BELIEVED"].get("delta"),
        "frbank_believed": res["by_backend"]["frbank"]["BELIEVED"].get("delta"),
        "frbank_true": res["by_backend"]["frbank"]["TRUE"].get("delta"),
        "reading": ("A-MEM believed carries counts and recency only, so its delta is the "
                    "count-and-recency component; FR-Bank believed adds corrupted lifecycle "
                    "signal; TRUE adds correct lifecycle signal."),
    }

    # ---------------- NOK, FR-Bank only by construction (Amendment 1 section 5)
    frb = [i for i in items if i["backend"] == "frbank"]
    nok = row(frb, blind, idxT, "NOK FR-Bank indexed-TRUE", judgment="nok")
    res["H_NOK"] = {"row": nok,
                    "gate": {"auroc_threshold": ">= 0.65",
                             "observed_indexed_auroc": nok.get("indexed_auroc"),
                             "delta": nok.get("delta"),
                             "ci": ([nok["bootstrap"]["ci_lo"], nok["bootstrap"]["ci_hi"]]
                                    if "bootstrap" in nok else None),
                             "holds": bool(nok.get("indexed_auroc", 0) >= 0.65
                                           and nok.get("delta", 0) >= 0.10
                                           and nok.get("bootstrap", {}).get("excludes_zero"))},
                    "scope": "FR-Bank only by construction; PN cell is empty on erase-mode backends"}
    cand = collections.Counter()
    for it in frb:
        r = idxT.get(it["item_id"])
        if r and r.get("nok_candidates_found") is not None:
            cand[(it.get("label", it["label_pre"]), r["nok_candidates_found"])] += 1
    res["nok_candidates_found_rate"] = {f"{k[0]}|{k[1]}": v for k, v in cand.items()}

    # ---------------- ABSENT mechanism split
    res["absent_mechanism"] = collections.Counter(
        i.get("absent_mechanism") for i in items
        if i.get("label", i["label_pre"]) == "ABSENT")

    # ---------------- k=3 noise, staircase
    k3 = jload(E1 / "elicitation_k3.json")
    byq = collections.defaultdict(list)
    for r in k3:
        if r["fok"] is not None:
            byq[r["question"]].append(r["fok"])
    sp = [max(v) - min(v) for v in byq.values() if len(v) == 3]
    res["k3_noise"] = {"n_questions": len(sp),
                       "identical_across_3": int(sum(1 for s in sp if s == 0)),
                       "mean_spread": (st.mean(sp) if sp else None),
                       "max_spread": (max(sp) if sp else None)}
    sc = jload(E1 / "elicitation_staircase.json")
    y = [0 if r["label"] == "ABSENT" else 1 for r in sc]
    res["staircase"] = ({"n": len(sc), "auroc": auroc([r["fok_staircase"] for r in sc], y),
                         "distinct_values": len({r["fok_staircase"] for r in sc})}
                        if len(set(y)) > 1 else {"n": len(sc), "note": "single-class"})

    # ---------------- skip-rate curves (descriptive)
    res["skip_rate"] = []
    for thr in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7):
        sk = [it for it in hard if it["item_id"] in idxT
              and idxT[it["item_id"]]["fok"] is not None
              and idxT[it["item_id"]]["fok"] < thr]
        good = sum(1 for it in sk if it.get("label", it["label_pre"]) == "ABSENT")
        res["skip_rate"].append({"threshold": thr, "n_skipped": len(sk),
                                 "frac_of_hard": len(sk) / max(len(hard), 1),
                                 "precision_skipping_absent": (good / len(sk)) if sk else None})

    jdump(res, OUT / "scores_e1.json")

    print("=" * 96)
    print("E1 GATES")
    print("=" * 96)
    g = res["gates"]
    print(f"  H1-hard  blind FOK AUROC {g['H1_hard']['observed']:.4f} < 0.75 : "
          f"{'HOLDS' if g['H1_hard']['holds'] else 'does not hold'}")
    print(f"  H2-hard  delta {g['H2_hard']['delta']:+.4f}  CI "
          f"[{g['H2_hard']['ci'][0]:+.4f}, {g['H2_hard']['ci'][1]:+.4f}] : "
          f"{'HOLDS' if g['H2_hard']['holds'] else 'does not hold'}")
    print(f"           band: {g['H2_hard']['band']}")
    n = res["H_NOK"]["gate"]
    print(f"  H-NOK    indexed AUROC {n['observed_indexed_auroc']:.4f} (>=0.65), "
          f"delta {n['delta']:+.4f} : {'HOLDS' if n['holds'] else 'does not hold'}")
    for b, v in res["H_BELIEVED"].items():
        r = v["retention"]
        print(f"  H-BELIEVED {b:8s} true {v['true_delta']:+.4f} believed {v['believed_delta']:+.4f}"
              f"  retention {('%.1f%%' % (100*r)) if r is not None else 'n/a':>8s} : "
              f"{'>=60%' if v['holds_ge_60pct'] else '<60%'}")
    print(f"\n  hard tier n={res['H2_hard']['n']}  blind {res['H2_hard']['blind_auroc']:.4f} "
          f"indexed {res['H2_hard']['indexed_auroc']:.4f}")
    print(f"  k=3 noise: identical on {res['k3_noise']['identical_across_3']}/"
          f"{res['k3_noise']['n_questions']}, mean spread {res['k3_noise']['mean_spread']:.3f}")
    print(f"\nwrote {OUT/'scores_e1.json'}")


if __name__ == "__main__":
    main()
