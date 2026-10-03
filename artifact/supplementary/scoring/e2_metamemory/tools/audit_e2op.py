"""audit_e2op.py -- E2-AUDIT: symmetric re-derivation of E2-OP's three headline numbers.

PRE-COMMITMENT, made before the first number was computed: **the outcome of this
audit is reported whether it confirms E2-OP's null or breaks it.** A divergence
that overturns H-OP1's failure is as publishable here as a clean confirmation, and
neither result changes what gets written down about the other.

INDEPENDENCE. This file shares NO code with the original scorer. It does not import
`score_e2`, `score_e2op`, `verify_e2op`, or `e2_common`, and it does not reuse their
join. Specifically:

  * ROW JOIN -- the eval item set is taken from `gates_eval.json`'s own rows, not
    rebuilt from `items_final.json` through the calibration-split filter that
    `e2_common.load_items` applies. Two different sources for the same 529 items.
  * ENDPOINT -- confabulation counted directly off the judge cache by (item, state),
    with the policy state chosen per item here, not via `state5`/`credit_of`.
  * PERMUTATION -- its own RNG, its own draw loop. A Monte Carlo quantity computed
    twice will not agree to the digit; the audit reports the gap against Monte Carlo
    standard error rather than pretending otherwise.

    python audit_e2op.py
"""
from __future__ import annotations

import io
import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E2 = ROOT / "e2_metamemory"

TAU_FOK = 0.20        # PREREG_E2OP section 1, carried
TAU_OP = 0.20         # PREREG_E2OP section 1, carried
N_SEEDS = 1000

REPORTED = {"targeted_endpoint": 0.259,
            "random_arm_mean": 0.2519,
            "permutation_p": 0.8931}


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def main():
    # ---------- independent row join ------------------------------------------
    gates = jload(E2 / "gates_eval.json")["rows"]
    items = [g for g in gates if g.get("split") == "eval"]
    tags = sorted(g["item_id"] for g in items)
    by_tag = {g["item_id"]: g for g in items}

    ans = jload(E2 / "answers_eval.json")["rows"]
    sha = {}
    for a in ans:
        sha[(a["item_id"], a["state"])] = a["response_sha"]

    J = jload(E2 / "cache" / "judgments_eval.json")
    confab = {}
    missing = []
    for (tag, state), s in sha.items():
        v = J.get(f"{tag}|{s[:24]}")
        if v is None:
            missing.append((tag, state))
            continue
        confab[(tag, state)] = 1 if v.get("confabulation") else 0

    print("INDEPENDENT ROW JOIN")
    print(f"  eval items from gates_eval.json rows : {len(tags)}")
    print(f"  answer rows                          : {len(ans)}  "
          f"({len(ans) // max(1, len(tags))} states per item)")
    print(f"  judge verdicts resolved              : {len(confab)} / {len(sha)}"
          f"   missing {len(missing)}")
    if missing:
        print(f"    MISSING -> {missing[:5]}")

    # ---------- independent policy construction --------------------------------
    def fok(t):
        return by_tag[t]["indexed"]["1"]["fok"] or 0.0

    def nok(t):
        return by_tag[t]["indexed"]["1"]["nok"] or 0.0

    retrieved = [t for t in tags if fok(t) >= TAU_FOK]
    selected = [t for t in retrieved if nok(t) >= TAU_OP]
    rset, sset = set(retrieved), set(selected)
    print(f"\n  retrieved (fok >= {TAU_FOK})            : {len(retrieved)}")
    print(f"  selected  (nok >= {TAU_OP}, retrieved)  : {len(selected)}"
          f"   fraction of retrieved {len(selected) / len(retrieved):.4f}")

    N = len(tags)

    def rate(state_of):
        return sum(confab[(t, state_of(t))] for t in tags) / N

    v_rate = rate(lambda t: "S1-facts" if t in rset else "S0-nofacts")
    vi_rate = rate(lambda t: "S2-facts-caution" if t in rset else "S0-nofacts")
    op_rate = rate(lambda t: ("S2-facts-caution" if t in sset else "S1-facts")
                   if t in rset else "S0-nofacts")

    # ---------- independent permutation ---------------------------------------
    rng = random.Random(20260814)          # this audit's own stream, not the scorer's
    k = len(selected)
    draws = []
    for _ in range(N_SEEDS):
        pick = set(rng.sample(retrieved, k))
        draws.append(sum(confab[(t, ("S2-facts-caution" if t in pick else "S1-facts")
                                 if t in rset else "S0-nofacts")] for t in tags) / N)
    draws.sort()
    rnd_mean = sum(draws) / len(draws)
    rnd_sd = (sum((d - rnd_mean) ** 2 for d in draws) / (len(draws) - 1)) ** 0.5
    n_le = sum(1 for d in draws if d <= op_rate + 1e-12)
    p_plain = n_le / N_SEEDS
    p_addone = (n_le + 1) / (N_SEEDS + 1)      # Davison-Hinkley; the original's form
    mc_se_mean = rnd_sd / math.sqrt(N_SEEDS)
    mc_se_p = math.sqrt(p_plain * (1 - p_plain) / N_SEEDS)

    # high-M reference: pins the TRUE p so both 1,000-draw estimates can be placed
    # against it rather than only against each other.
    rng2 = random.Random(987654321)
    M = 100_000
    hi_le = hi_eq = 0
    base = sum(confab[(t, "S0-nofacts")] for t in tags if t not in rset)
    s1 = {t: confab[(t, "S1-facts")] for t in retrieved}
    s2 = {t: confab[(t, "S2-facts-caution")] for t in retrieved}
    tot_s1 = sum(s1.values())
    seen = set()
    for _ in range(M):
        pick = rng2.sample(retrieved, k)
        r = (base + tot_s1 + sum(s2[t] - s1[t] for t in pick)) / N
        seen.add(round(r, 9))
        if r <= op_rate + 1e-12:
            hi_le += 1
        if abs(r - op_rate) <= 1e-12:
            hi_eq += 1
    p_true = hi_le / M
    tie_share = hi_eq / M

    # analytic expectation of the random arm -- exact, no RNG at all
    p_sel = k / len(retrieved)
    analytic = sum((p_sel * confab[(t, "S2-facts-caution")]
                    + (1 - p_sel) * confab[(t, "S1-facts")]) if t in rset
                   else confab[(t, "S0-nofacts")] for t in tags) / N

    # ---------- convergence diff ----------------------------------------------
    print("\nCONVERGENCE DIFF -- audit vs RESULTS_E2OP.md")
    rows = [
        ("targeted endpoint (vi-OP)", op_rate, REPORTED["targeted_endpoint"], 5e-4, None),
        ("random-arm mean (vii-NOK)", rnd_mean, REPORTED["random_arm_mean"],
         3 * mc_se_mean, f"Monte Carlo, +/-3 SE = {3 * mc_se_mean:.5f}"),
        ("permutation p, one-sided", p_addone, REPORTED["permutation_p"],
         3 * mc_se_p, f"Monte Carlo, +/-3 SE = {3 * mc_se_p:.5f}"),
    ]
    out = {"pre_commitment": ("reported whether it confirms or breaks the null; "
                              "stated before the first number was computed"),
           "independence": ("no import of score_e2 / score_e2op / verify_e2op / "
                            "e2_common; item set from gates_eval.json rows"),
           "join": {"n_eval": len(tags), "n_answer_rows": len(ans),
                    "verdicts_resolved": len(confab), "verdicts_missing": len(missing),
                    "n_retrieved": len(retrieved), "n_selected": len(selected)},
           "audit": {"v_rate": v_rate, "vi_rate": vi_rate, "op_rate": op_rate,
                     "random_mean": rnd_mean, "random_sd": rnd_sd,
                     "n_le": n_le, "permutation_p_plain": p_plain,
                     "permutation_p_addone": p_addone,
                     "analytic_random": analytic},
           "high_M_reference": {"draws": M, "p_true": p_true,
                                "tie_share": tie_share,
                                "distinct_endpoint_values": len(seen),
                                "mc_se_at_1000": math.sqrt(p_true*(1-p_true)/N_SEEDS)},
           "diff": []}
    verdict_all = True
    for name, got, want, tol, note in rows:
        agree = abs(got - want) <= tol
        verdict_all &= agree
        out["diff"].append({"quantity": name, "audit": got, "reported": want,
                            "delta": got - want, "tolerance": tol,
                            "verdict": "AGREE" if agree else "DIVERGE", "note": note})
        print(f"  {'AGREE  ' if agree else 'DIVERGE'} {name:28s} "
              f"audit {got:.5f}   reported {want:.5f}   delta {got - want:+.5f}"
              + (f"   [{note}]" if note else ""))

    se = math.sqrt(p_true * (1 - p_true) / N_SEEDS)
    orig_addone = 894 / 1001          # the original's n_le = 893, add-one applied
    print(f"\n  ROOT CAUSE of the permutation divergence")
    print(f"    high-M reference ({M:,} draws): TRUE p = {p_true:.5f}"
          f"   tie mass {tie_share * 100:.2f}%"
          f"   distinct endpoint values {len(seen)}")
    print(f"    MC SE of any 1,000-draw estimate: {se:.5f}")
    print(f"    original  n_le=893 -> {orig_addone:.5f}   "
          f"deviation from true {orig_addone - p_true:+.5f}  "
          f"({abs(orig_addone - p_true) / se:.2f} SE)")
    print(f"    audit     n_le={n_le} -> {p_addone:.5f}   "
          f"deviation from true {p_addone - p_true:+.5f}  "
          f"({abs(p_addone - p_true) / se:.2f} SE)")
    print(f"    estimator-definition component: plain {p_plain:.5f} vs add-one "
          f"{p_addone:.5f} = {p_addone - p_plain:+.5f}  (negligible at this magnitude)")
    print(f"    SE of the DIFFERENCE between two 1,000-draw estimates: "
          f"{se * math.sqrt(2):.5f}  -> observed gap is "
          f"{abs(p_addone - orig_addone) / (se * math.sqrt(2)):.2f} SE")
    out["root_cause"] = {
        "dominant": "Monte Carlo noise at N_SEEDS=1000",
        "secondary": "estimator definition: plain n/N vs add-one (n+1)/(N+1)",
        "true_p_100k": p_true, "tie_share": tie_share,
        "distinct_endpoint_values": len(seen), "mc_se_at_1000": se,
        "original_addone": orig_addone, "audit_addone": p_addone,
        "original_deviation_se": abs(orig_addone - p_true) / se,
        "audit_deviation_se": abs(p_addone - p_true) / se,
        "gap_in_se_of_difference": abs(p_addone - orig_addone) / (se * math.sqrt(2))}

    print(f"\n  cross-check, analytic random arm (no RNG): {analytic:.5f}  "
          f"vs simulated {rnd_mean:.5f}   delta {analytic - rnd_mean:+.5f}")
    print(f"  supporting: (v) gate-only {v_rate:.5f}   (vi) blanket {vi_rate:.5f}")
    print(f"\n  VERDICT: {'ALL THREE CONVERGE' if verdict_all else 'DIVERGENCE FOUND'}")
    out["verdict"] = "ALL THREE CONVERGE" if verdict_all else "DIVERGENCE FOUND"

    io.open(E2 / "results" / "e2_audit.json", "w", encoding="utf-8").write(
        json.dumps(out, indent=2))
    print("  written: results/e2_audit.json")


if __name__ == "__main__":
    main()
