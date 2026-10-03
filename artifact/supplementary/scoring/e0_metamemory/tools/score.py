"""
score.py -- E0 Step 5: scoring, per PREREG_E0.md §11 as amended.

NO API CALLS. Deterministic given elicitation.json; seed 42 for the bootstrap.

Metric definitions, stated explicitly because the prereg fixes the metrics but not
every operationalisation detail:

  FOK AUROC   positive class = NON-ABSENT (the store does hold relevant content),
              score = FOK. Higher FOK should mean more likely non-ABSENT, so a
              discriminating judge scores > 0.5 and chance is 0.5. Ties contribute
              0.5, via the rank-based Mann-Whitney formulation -- this matters here
              because the responses are coarsely quantised (D20).
  NOK AUROC   positive class = PRESENT-NEGATIVE, score = NOK. Exploratory.
  ECE         10 equal-width bins on [0,1]; outcome for FOK is non-ABSENT, for NOK
              is PRESENT-NEGATIVE; ECE = sum_b (n_b/N) * |acc(b) - conf(b)|.
  Brier       mean (p - y)^2 on the same pairing.
  bootstrap   1000 resamples of ITEMS with replacement, seed 42, both arms moving
              together so the pairing is preserved; percentile 95% CI on the
              indexed-minus-blind AUROC delta.

Gates are read mechanically from the PRIMARY row. Sensitivity rows gate nothing.
"""

from __future__ import annotations

import collections
import statistics as st

import numpy as np

from e0_common import E0, SEED, jdump, jload

OUT = E0 / "results"
N_BOOT = 1000
BINS = 10


# --------------------------------------------------------------------- metrics
def auroc(scores, labels):
    """Mann-Whitney AUROC with proper tie handling. labels: 1 = positive."""
    s = np.asarray(scores, dtype=float)
    y = np.asarray(labels, dtype=int)
    n1, n0 = int(y.sum()), int((1 - y).sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s), dtype=float)
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[order[j + 1]] == s[order[i]]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def ece(p, y, bins=BINS):
    p = np.asarray(p, float)
    y = np.asarray(y, int)
    if len(p) == 0:
        return float("nan")
    edges = np.linspace(0.0, 1.0, bins + 1)
    total = 0.0
    for b in range(bins):
        lo, hi = edges[b], edges[b + 1]
        m = (p >= lo) & (p < hi) if b < bins - 1 else (p >= lo) & (p <= hi)
        if m.sum():
            total += (m.sum() / len(p)) * abs(y[m].mean() - p[m].mean())
    return float(total)


def brier(p, y):
    p, y = np.asarray(p, float), np.asarray(y, int)
    return float(np.mean((p - y) ** 2)) if len(p) else float("nan")


def reliability(p, y, bins=BINS):
    p, y = np.asarray(p, float), np.asarray(y, int)
    edges = np.linspace(0.0, 1.0, bins + 1)
    out = []
    for b in range(bins):
        lo, hi = edges[b], edges[b + 1]
        m = (p >= lo) & (p < hi) if b < bins - 1 else (p >= lo) & (p <= hi)
        out.append({"bin": b, "lo": float(lo), "hi": float(hi), "n": int(m.sum()),
                    "conf": float(p[m].mean()) if m.sum() else None,
                    "acc": float(y[m].mean()) if m.sum() else None})
    return out


def paired_bootstrap(blind, indexed, y, n_boot=N_BOOT, seed=SEED):
    """Resample ITEMS; both arms move together so the pairing is preserved."""
    rng = np.random.default_rng(seed)
    n = len(y)
    b, i, yy = np.asarray(blind), np.asarray(indexed), np.asarray(y)
    deltas = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        if yy[idx].sum() in (0, len(idx)):
            continue
        deltas.append(auroc(i[idx], yy[idx]) - auroc(b[idx], yy[idx]))
    d = np.asarray(deltas, float)
    return {"n_resamples": int(len(d)),
            "mean": float(d.mean()), "sd": float(d.std(ddof=1)),
            "ci_lo": float(np.percentile(d, 2.5)),
            "ci_hi": float(np.percentile(d, 97.5)),
            "excludes_zero": bool(np.percentile(d, 2.5) > 0 or np.percentile(d, 97.5) < 0)}


# ------------------------------------------------------------------ assembly
def build(rows):
    """item_id -> {blind, indexed, meta}; only OK records."""
    by = collections.defaultdict(dict)
    for r in rows:
        if r["status"] != "OK":
            continue
        by[r["item_id"]][r["arm"]] = r
    out = {}
    for k, v in by.items():
        if "BLIND" in v and "INDEXED" in v:
            out[k] = v
    return out


def dedup_blind(items, all_rows):
    """Amendment 2: replace each blind draw with the mean over a question's variants."""
    draws = collections.defaultdict(list)
    for r in all_rows:
        if r["arm"] == "BLIND" and r["status"] == "OK":
            draws[(r["persona"], r["question_id"])].append(r)
    mean = {k: (st.mean([x["fok"] for x in v]), st.mean([x["nok"] for x in v]))
            for k, v in draws.items()}
    n_two = sum(1 for v in draws.values() if len(v) == 2)
    n_one = sum(1 for v in draws.values() if len(v) == 1)
    out = {}
    for k, v in items.items():
        b = dict(v["BLIND"])
        f, n = mean[(b["persona"], b["question_id"])]
        b["fok"], b["nok"] = f, n
        out[k] = {"BLIND": b, "INDEXED": v["INDEXED"]}
    return out, n_two, n_one


def gate_row(items, name, judgment="fok", positive="non-ABSENT"):
    keys = sorted(items)
    if judgment == "fok":
        y = [0 if items[k]["BLIND"]["label"] == "ABSENT" else 1 for k in keys]
    else:
        y = [1 if items[k]["BLIND"]["label"] == "PRESENT-NEGATIVE" else 0 for k in keys]
    b = [items[k]["BLIND"][judgment] for k in keys]
    i = [items[k]["INDEXED"][judgment] for k in keys]
    ab, ai = auroc(b, y), auroc(i, y)
    return {
        "row": name, "judgment": judgment, "positive_class": positive,
        "n": len(keys), "n_pos": int(sum(y)), "n_neg": int(len(y) - sum(y)),
        "blind_auroc": ab, "indexed_auroc": ai, "delta": ai - ab,
        "bootstrap": paired_bootstrap(b, i, y),
        "blind_ece": ece(b, y), "indexed_ece": ece(i, y),
        "blind_brier": brier(b, y), "indexed_brier": brier(i, y),
    }


def verdict(row):
    """Mechanical read of the pre-registered gates. No judgement applied."""
    blind, delta, ci = row["blind_auroc"], row["delta"], row["bootstrap"]
    h1 = blind < 0.75
    h2 = (delta >= 0.10) and ci["excludes_zero"]
    if blind >= 0.80:
        v = "KILL-A"
    elif not h2:
        v = "KILL-B"
    elif h1 and h2:
        v = "GO"
    elif 0.75 <= blind < 0.80 and h2:
        v = "AMBER"
    else:
        v = "AMBER"
    return {"H1_blind_auroc_lt_0.75": h1, "H1_observed": blind,
            "H2_delta_ge_0.10": delta >= 0.10, "H2_observed_delta": delta,
            "H2_ci_excludes_zero": ci["excludes_zero"],
            "H2_ci": [ci["ci_lo"], ci["ci_hi"]],
            "KILL_A_blind_auroc_ge_0.80": blind >= 0.80,
            "verdict": v}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = jload(E0 / "elicitation.json")
    scoreable = [r for r in rows if r["label"] in ("PRESENT", "ABSENT", "PRESENT-NEGATIVE")]
    items = build(scoreable)
    res = {"n_elicited_records": len(rows),
           "n_scoreable_records": len(scoreable),
           "n_items_scored": len(items),
           "n_elicitation_failed": sum(1 for r in rows if r["status"] != "OK")}

    # ---------------- PRIMARY
    primary = gate_row(items, "PRIMARY (as frozen)")
    res["primary"] = primary
    res["gate"] = verdict(primary)

    # ---------------- Amendment 2: blind-deduplicated
    ded, n_two, n_one = dedup_blind(items, rows)
    a2 = gate_row(ded, "Amendment 2: blind-deduplicated")
    a2["questions_with_two_draws"] = n_two
    a2["questions_with_one_draw"] = n_one
    res["amendment2_blind_dedup"] = a2
    res["amendment2_gate_if_read"] = verdict(a2)

    # ---------------- Amendment 1 row 1: drop lex-flagged ABSENT
    excl = {k: v for k, v in items.items() if not v["BLIND"]["lex_flagged"]}
    res["amendment1_lex_excluded"] = gate_row(excl, "Amendment 1: 3 lex-flagged ABSENT excluded")
    res["amendment1_lex_excluded"]["n_excluded"] = len(items) - len(excl)

    # ---------------- Amendment 1 row 2: ABSENT mechanism split (descriptive)
    split = {}
    for mech in ("ablation", "expiry"):
        sub = {k: v for k, v in items.items()
               if v["BLIND"]["label"] != "ABSENT" or v["BLIND"]["absent_mechanism"] == mech}
        split[mech] = gate_row(sub, f"ABSENT subset: {mech} only (descriptive)")
    res["amendment1_absent_mechanism"] = split

    # ---------------- NOK, exploratory
    nok = gate_row(items, "NOK (exploratory, ungated)", judgment="nok",
                   positive="PRESENT-NEGATIVE")
    nok_d = gate_row(ded, "NOK blind-deduplicated (exploratory)", judgment="nok",
                     positive="PRESENT-NEGATIVE")
    blind_nok = [items[k]["BLIND"]["nok"] for k in items]
    all_blind_nok = [r["nok"] for r in rows if r["arm"] == "BLIND"]
    res["nok"] = {"primary": nok, "blind_dedup": nok_d,
                  "blind_nok_zero_scoreable": int(sum(1 for x in blind_nok if x == 0.0)),
                  "blind_nok_n_scoreable": len(blind_nok),
                  "blind_nok_zero_all_items": int(sum(1 for x in all_blind_nok if x == 0.0)),
                  "blind_nok_n_all_items": len(all_blind_nok),
                  "blind_nok_distinct_values": sorted(set(all_blind_nok))}

    # ---------------- breakdowns
    def sub_auroc(pred):
        ks = [k for k in sorted(items) if pred(items[k]["BLIND"])]
        if not ks:
            return None
        y = [0 if items[k]["BLIND"]["label"] == "ABSENT" else 1 for k in ks]
        if sum(y) in (0, len(y)):
            return {"n": len(ks), "n_pos": int(sum(y)), "note": "single-class, AUROC undefined"}
        return {"n": len(ks), "n_pos": int(sum(y)),
                "blind_auroc": auroc([items[k]["BLIND"]["fok"] for k in ks], y),
                "indexed_auroc": auroc([items[k]["INDEXED"]["fok"] for k in ks], y)}

    res["breakdowns"] = {
        "pn_subtype": {s: {"n": sum(1 for v in items.values()
                                    if v["BLIND"]["label"] == "PRESENT-NEGATIVE"
                                    and v["BLIND"]["subtype"] == s),
                           "mean_blind_nok": st.mean([v["BLIND"]["nok"] for v in items.values()
                                                      if v["BLIND"]["label"] == "PRESENT-NEGATIVE"
                                                      and v["BLIND"]["subtype"] == s] or [0]),
                           "mean_indexed_nok": st.mean([v["INDEXED"]["nok"] for v in items.values()
                                                        if v["BLIND"]["label"] == "PRESENT-NEGATIVE"
                                                        and v["BLIND"]["subtype"] == s] or [0])}
                       for s in ("with-replacement", "without-replacement")},
        "per_persona": {p: sub_auroc(lambda r, p=p: r["persona"] == p)
                        for p in sorted({v["BLIND"]["persona"] for v in items.values()})},
        "per_attack_vector": {a: sub_auroc(lambda r, a=a: r["attack_vector"] == a)
                              for a in sorted({v["BLIND"]["attack_vector"] for v in items.values()})},
        "mean_fok_by_label": {
            lab: {"blind": st.mean([v["BLIND"]["fok"] for v in items.values()
                                    if v["BLIND"]["label"] == lab]),
                  "indexed": st.mean([v["INDEXED"]["fok"] for v in items.values()
                                      if v["BLIND"]["label"] == lab])}
            for lab in ("PRESENT", "ABSENT", "PRESENT-NEGATIVE")},
        "would_search": {
            arm: {lab: st.mean([1.0 if items[k][arm]["would_search"] else 0.0
                                for k in items if items[k]["BLIND"]["label"] == lab])
                  for lab in ("PRESENT", "ABSENT", "PRESENT-NEGATIVE")}
            for arm in ("BLIND", "INDEXED")},
    }

    # ---------------- reliability curves
    keys = sorted(items)
    y_fok = [0 if items[k]["BLIND"]["label"] == "ABSENT" else 1 for k in keys]
    y_nok = [1 if items[k]["BLIND"]["label"] == "PRESENT-NEGATIVE" else 0 for k in keys]
    res["reliability"] = {
        f"{arm}_{j}": reliability([items[k][arm][j] for k in keys],
                                  y_fok if j == "fok" else y_nok)
        for arm in ("BLIND", "INDEXED") for j in ("fok", "nok")}

    jdump(res, OUT / "scores.json")
    plot(res)

    # ---------------- console
    def line(r):
        ci = r["bootstrap"]
        print(f"  {r['row']:42s} n={r['n']:3d}  blind {r['blind_auroc']:.4f}  "
              f"indexed {r['indexed_auroc']:.4f}  delta {r['delta']:+.4f}  "
              f"CI [{ci['ci_lo']:+.4f}, {ci['ci_hi']:+.4f}]")

    print("=" * 108)
    print("FOK AUROC — positive class = non-ABSENT")
    print("=" * 108)
    line(primary)
    line(a2)
    line(res["amendment1_lex_excluded"])
    for m in ("ablation", "expiry"):
        line(split[m])
    g = res["gate"]
    print(f"\n  H1 blind AUROC < 0.75          : {g['H1_observed']:.4f}  "
          f"{'HOLDS' if g['H1_blind_auroc_lt_0.75'] else 'does not hold'}")
    print(f"  H2 delta >= +0.10              : {g['H2_observed_delta']:+.4f}  "
          f"{'HOLDS' if g['H2_delta_ge_0.10'] else 'does not hold'}")
    print(f"  H2 bootstrap CI excludes 0     : {g['H2_ci'][0]:+.4f}..{g['H2_ci'][1]:+.4f}  "
          f"{'YES' if g['H2_ci_excludes_zero'] else 'NO'}")
    print(f"  KILL-A blind AUROC >= 0.80     : {'YES' if g['KILL_A_blind_auroc_ge_0.80'] else 'no'}")
    print(f"\n  PRE-REGISTERED VERDICT: {g['verdict']}")
    print(f"  (Amendment 2 row, if the gate were read from it: {res['amendment2_gate_if_read']['verdict']})")
    print("\n  NOK (exploratory):")
    line(nok)
    line(nok_d)
    print(f"    blind NOK = 0.00 on {res['nok']['blind_nok_zero_all_items']}/"
          f"{res['nok']['blind_nok_n_all_items']} items; distinct blind NOK values "
          f"{res['nok']['blind_nok_distinct_values']}")
    print(f"\n  ECE/Brier  BLIND fok  ECE {primary['blind_ece']:.4f}  Brier {primary['blind_brier']:.4f}")
    print(f"             INDEXED fok ECE {primary['indexed_ece']:.4f}  Brier {primary['indexed_brier']:.4f}")
    print(f"             BLIND nok  ECE {nok['blind_ece']:.4f}  Brier {nok['blind_brier']:.4f}")
    print(f"             INDEXED nok ECE {nok['indexed_ece']:.4f}  Brier {nok['indexed_brier']:.4f}")
    print(f"\nwrote {OUT/'scores.json'} and reliability figures")


def plot(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    for j, title in (("fok", "FOK — outcome: store holds relevant content (non-ABSENT)"),
                     ("nok", "NOK — outcome: store holds a negative obligation")):
        fig, ax = plt.subplots(figsize=(6.2, 5.4))
        ax.plot([0, 1], [0, 1], ls="--", lw=1, color="#888", label="perfect calibration")
        for arm, colour, marker in (("BLIND", "#B4413C", "o"), ("INDEXED", "#1F6F8B", "s")):
            pts = [(b["conf"], b["acc"], b["n"]) for b in res["reliability"][f"{arm}_{j}"]
                   if b["n"]]
            if not pts:
                continue
            xs, ys, ns = zip(*pts)
            ax.plot(xs, ys, marker=marker, color=colour, lw=1.8, ms=5, label=arm)
            for x, y_, n in pts:
                ax.annotate(str(n), (x, y_), textcoords="offset points", xytext=(4, -10),
                            fontsize=7, color=colour)
        ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02)
        ax.set_xlabel("mean predicted probability (bin)")
        ax.set_ylabel("observed frequency")
        ax.set_title(title, fontsize=10)
        ax.legend(fontsize=8, loc="upper left")
        ax.grid(alpha=0.25, lw=0.5)
        fig.tight_layout()
        fig.savefig(OUT / f"reliability_{j}.png", dpi=170)
        plt.close(fig)


if __name__ == "__main__":
    main()
