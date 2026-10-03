"""
plan_dataset.py -- fix the persona selection and per-persona ablation, and emit
the census that the pre-registration commits to.

NO API CALLS. Deterministic: no randomness anywhere, so the plan is a pure
function of the committed artifacts plus thresholds.json.

Selection rule (pre-registered):
  1. For each of the 40 personas, choose the ablation as the k in {2,3} subset of
     the 11 categories maximising ABSENT, tie-broken by (more PRESENT-NEGATIVE,
     more PRESENT, fewer categories, alphabetical). Deterministic.
  2. Choose N personas by greedy addition then local search, maximising
     (smallest gate cell, total scoreable items). Candidates are scanned in
     sorted name order and only a strict improvement is accepted.

Gate on the plan, from the decisions of record:
  ABSENT >= 60           required. If it fails at N=20, escalate to N=30.
  PRESENT-NEGATIVE < 60  acceptable (NOK is exploratory in E0).

Usage:  python e0_metamemory/tools/plan_dataset.py [N]
"""

from __future__ import annotations

import collections
import sys

from e0_common import (
    E0, PROJECT_ROOT, best_ablation, jdump, load_joins, load_thresholds,
    OUT_OF_SCOPE_AV,
)

PLAN_PATH = E0 / "plan.json"


def main():
    want = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    tau_lo, tau_hi = load_thresholds()
    joins = load_joins()
    print(f"thresholds: tau_lo={tau_lo:.2f}  tau_hi={tau_hi:.2f}\n")

    best = {n: best_ablation(J, tau_lo, tau_hi, kmax=3) for n, J in sorted(joins.items())}

    from e0_common import select_personas
    for N in (want, 30, 40):
        sel, t = select_personas(best, N)
        scoreable = t["PRESENT"] + t["ABSENT"] + t["PRESENT-NEGATIVE"]
        comp = (f"{t['PRESENT']/scoreable:.0%}/{t['ABSENT']/scoreable:.0%}/"
                f"{t['PRESENT-NEGATIVE']/scoreable:.0%}") if scoreable else "-"
        print(f"  N={N:2d}  PRES={t['PRESENT']:4d} ABS={t['ABSENT']:4d} "
              f"PNEG={t['PRESENT-NEGATIVE']:4d} UNRES={t['UNRESOLVED']:4d} | "
              f"n={scoreable:4d} | {comp} | ABSENT>=60 "
              f"{'PASS' if t['ABSENT'] >= 60 else 'FAIL'}")
        if N == want and t["ABSENT"] >= 60:
            chosen, totals = sel, t
            chosen_n = N
            break
    else:
        raise SystemExit("ABSENT >= 60 not reached at N in {want,30,40}")

    print(f"\nselected N={chosen_n}\n")
    print(f"{'persona':12s} {'PRES':>5s} {'ABS':>4s} {'PNEG':>5s} {'UNRES':>6s}  "
          f"{'t_now (pinned)':20s} ablated categories")
    plan = {}
    for n in chosen:
        combo, c = best[n]
        J = joins[n]
        plan[n] = {
            "ablated_categories": sorted(combo),
            "t_now": J.t_now.isoformat(),
            "expiry_cutoff": J.cutoff.isoformat(),
            "n_questions": len(J.questions),
            "n_entries_full": len(J.entries),
            "next_id": J.next_id,
            "census": dict(c),
        }
        print(f"{n:12s} {c['PRESENT']:5d} {c['ABSENT']:4d} {c['PRESENT-NEGATIVE']:5d} "
              f"{c['UNRESOLVED']:6d}  {J.t_now.date()!s:20s} {', '.join(sorted(combo))}")

    scoreable = totals["PRESENT"] + totals["ABSENT"] + totals["PRESENT-NEGATIVE"]
    print(f"\n  CELLS  PRESENT={totals['PRESENT']}  ABSENT={totals['ABSENT']}  "
          f"PRESENT-NEGATIVE={totals['PRESENT-NEGATIVE']}  UNRESOLVED={totals['UNRESOLVED']}")
    print(f"  scoreable items = {scoreable};  total (question,variant) pairs = "
          f"{scoreable + totals['UNRESOLVED']}")
    caps = {}
    for cell in ("PRESENT", "ABSENT", "PRESENT-NEGATIVE"):
        worst_p = max(chosen, key=lambda n: best[n][1][cell])
        worst = best[worst_p][1][cell]
        share = worst / totals[cell] if totals[cell] else 0.0
        caps[cell] = {"max_persona": worst_p, "max_count": worst, "share": round(share, 4)}
        print(f"  max single-persona share of {cell:16s} = {share:6.1%} "
              f"({worst_p}, {worst}) [{'OK' if share <= 0.15 else 'OVER 15% cap'}]")

    # UNRESOLVED census, published per the decisions of record
    by_reason = collections.Counter()
    by_av = collections.Counter()
    by_av_tot = collections.Counter()
    by_cat = collections.Counter()
    for n in chosen:
        J = joins[n]
        by_reason.update(J.reasons)
        for q in J.questions:
            by_av_tot[q["attack_vector"]] += 1
            if J.gold[q["id"]] is None:
                by_av[q["attack_vector"]] += 1
            else:
                for i in J.gold[q["id"]]:
                    by_cat[J.by_id[i]["category"]] += 1
    print("\n  UNRESOLVED by reason (question level, FULL variant):")
    for k, v in by_reason.most_common():
        print(f"    {k:26s} {v:4d}")
    print("\n  question resolution by attack vector:")
    for av in sorted(by_av_tot):
        r = by_av_tot[av] - by_av[av]
        tag = "  [out of E0 scope]" if av in OUT_OF_SCOPE_AV else ""
        print(f"    {av:34s} resolved {r:3d}/{by_av_tot[av]:3d}{tag}")
    print("\n  gold-edge categories (resolved questions):")
    for k, v in by_cat.most_common():
        print(f"    {k:26s} {v:5d}")

    jdump({
        "meta": {
            "design_basis": "e0_metamemory/FINDINGS_E0_STEP0.md @ d51f12d",
            "tau_lo": tau_lo, "tau_hi": tau_hi,
            "n_personas": chosen_n,
            "ablation_k_range": [2, 3],
            "selection_rule": "per-persona ablation maximising ABSENT (deterministic "
                              "tie-break); personas by greedy + local search maximising "
                              "(smallest gate cell, total scoreable). No randomness.",
            "no_api_calls": True,
            "gold_resolver": "YAML-native only (gate metrics); lexical proxy is a "
                             "sensitivity arm; judged cache excluded from labels.",
            "out_of_scope_attack_vectors": sorted(OUT_OF_SCOPE_AV),
        },
        "personas": plan,
        "totals": dict(totals),
        "scoreable": scoreable,
        "per_persona_cap": caps,
        "unresolved_by_reason": dict(by_reason),
        "unresolved_by_attack_vector": dict(by_av),
        "questions_by_attack_vector": dict(by_av_tot),
        "gold_categories": dict(by_cat),
    }, PLAN_PATH)
    print(f"\nwrote {PLAN_PATH}")


if __name__ == "__main__":
    main()
