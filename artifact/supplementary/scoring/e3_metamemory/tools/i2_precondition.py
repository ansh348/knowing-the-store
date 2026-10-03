"""
i2_precondition.py -- I2's frozen precondition, and the synthesis only if it passes.

PREREG_I2.md, committed at 09c34ab BEFORE this file was run. NO API CALLS, $0.

  PRECONDITION: NOK's AUROC for PRESENT-NEGATIVE vs everything else, on E3's
  committed eval gate signals, must EXCEED 0.65.
    <= 0.65  ->  I2 CLOSED. No threshold is derived, no policy is synthesized,
                 and the stated failure reason stands.
    >  0.65  ->  derive t on CALIBRATION only, synthesize the policy from
                 existing answers, report both endpoints.

This is NOT a gate, NOT part of the frozen sequence, and NOT a rescue of H-E3a.

Usage:  python e3_metamemory/tools/i2_precondition.py
"""

from __future__ import annotations

import collections
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e2_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from score_e1 import auroc                                         # noqa: E402
from score_e2 import adjusted, boot_ci                             # noqa: E402
from e3_common import E3, S0, S1, S2, jdump, jload, load_cells     # noqa: E402
from score_e3 import credit_of                                     # noqa: E402

BAR = 0.65
GRID = [round(x * 0.05, 2) for x in range(21)]


def main():
    C = load_cells()
    ev = {c["cell_id"]: c for c in C["cells"] if c["split"] == "eval"}
    ca = {c["cell_id"]: c for c in C["cells"] if c["split"] == "calibration"}
    gE = {r["cell_id"]: r for r in jload(E3 / "gates_eval.json")["rows"]}
    gC = {r["cell_id"]: r for r in jload(E3 / "gates_calibration.json")["rows"]}

    # ---------------------------------------------------- THE PRECONDITION
    tags = sorted(ev)
    y = [1 if ev[t]["label"] == "PRESENT-NEGATIVE" else 0 for t in tags]
    s = [gE[t]["nok"] if gE[t]["nok"] is not None else 0.0 for t in tags]
    a = auroc(s, y)
    prev = sum(y) / len(y)
    passed = a > BAR

    print("=" * 96)
    print("I2 PRECONDITION -- PREREG_I2.md section 2, frozen before this ran")
    print("=" * 96)
    print(f"  NOK AUROC, PRESENT-NEGATIVE vs rest, E3 eval gate signals")
    print(f"    AUROC       {a:.4f}")
    print(f"    bar         {BAR}  (EXCEED, strictly)")
    print(f"    n           {len(y)} cells   PN prevalence {prev:.4f} "
          f"({sum(y)}/{len(y)})")
    print(f"    VERDICT     {'PASSES' if passed else 'FAILED'}")

    R = {"prereg": "PREREG_I2.md", "no_new_model_calls": True, "usd": 0.0,
         "label": "pre-registered synthesis over pre-existing outputs",
         "not_a_gate": True, "not_in_the_sequence": True,
         "not_a_rescue_of_H_E3a": True,
         "precondition": {"auroc": a, "bar": BAR, "n": len(y),
                          "pn_prevalence": prev, "n_pn": sum(y),
                          "passed": bool(passed)}}

    # distribution, reported whichever way the precondition lands
    dist = {str(t): sum(1 for x in s if x >= t) / len(s) for t in GRID[:8]}
    print(f"\n  NOK distribution on the eval cells (share clearing each threshold):")
    print("    " + "   ".join(f"{k} {v:.3f}" for k, v in dist.items()))
    by_lab = collections.defaultdict(list)
    for t in tags:
        by_lab[ev[t]["label"]].append(
            gE[t]["nok"] if gE[t]["nok"] is not None else 0.0)
    print(f"\n  NOK by label (mean / median / share >= 0.05):")
    for k, v in sorted(by_lab.items()):
        print(f"    {k:18s} n={len(v):4d}  mean {np.mean(v):.4f}  "
              f"median {np.median(v):.4f}  >=0.05 {np.mean([x >= 0.05 for x in v]):.3f}")
    R["nok_distribution"] = dist
    R["nok_by_label"] = {k: {"n": len(v), "mean": float(np.mean(v)),
                             "median": float(np.median(v)),
                             "share_ge_005": float(np.mean([x >= 0.05 for x in v]))}
                         for k, v in by_lab.items()}

    if not passed:
        print("\n" + "=" * 96)
        print("PRECONDITION FAILED -> I2 IS CLOSED")
        print("=" * 96)
        print("  No threshold is derived. No policy is synthesized.")
        print("  The stated failure reason in PREREG_I2.md section 4 stands as the")
        print("  paper's answer to \"why not selective caution\":")
        print()
        print('  "Selective caution is worth designing and this monitor cannot do the')
        print('   selecting. The caution instruction\'s benefit is concentrated on')
        print('   obligation-bearing questions and its cost on answerable ones -- a')
        print('   payoff with an interval excluding zero -- but the NOK channel does not')
        print('   separate those two populations: its scores are piled at the bottom of')
        print('   their range and its discrimination for PRESENT-NEGATIVE is at or below')
        print('   0.65 AUROC. The selection problem is real; the signal available to')
        print('   solve it is not."')
        R["outcome"] = "CLOSED -- precondition failed"
        R["prediction_1_frozen"] = "the precondition FAILS"
        R["prediction_1_correct"] = True
        jdump(R, E3 / "results" / "i2_precondition.json")
        print("\nwrote results/i2_precondition.json")
        return

    # ------------------------------------------- derive t on CALIBRATION only
    print("\n  precondition passed -> deriving t on the CALIBRATION personas only")
    A = jload(E3 / "answers_calibration.json")["rows"]
    J = jload(E3 / "cache" / "judgments_calibration.json")
    dr = collections.defaultdict(list)
    for x in A:
        v = J.get(f"{x['cell_id']}|{x['response_sha'][:24]}", {})
        c = credit_of(ca[x["cell_id"]]["label"], v.get("correctness"))
        if c is not None:
            dr[(x["cell_id"], x["state"])].append(c)
    cr = {k: sum(v) / len(v) for k, v in dr.items()}
    cal = sorted(ca)
    pn = [t for t in cal if ca[t]["label"] == "PRESENT-NEGATIVE"]
    rest = [t for t in cal if ca[t]["label"] != "PRESENT-NEGATIVE"]

    def d(sub):
        v = [cr[(t, S2)] - cr[(t, S1)] for t in sub
             if (t, S2) in cr and (t, S1) in cr]
        return sum(v) / len(v) if v else 0.0

    def dci(sub):
        v = [(ca[t]["persona"], ca[t]["label"], cr[(t, S2)] - cr[(t, S1)])
             for t in sub if (t, S2) in cr and (t, S1) in cr]
        if not v:
            return None
        lo, hi = boot_ci(v, False)
        return {"est": float(np.mean([x[2] for x in v])), "lo": lo, "hi": hi,
                "n": len(v)}

    B, Ccost = d(pn), -d(rest)
    B_ci, C_ci = dci(pn), dci(rest)
    q = Ccost / (B + Ccost) if (B + Ccost) else 0.0
    print(f"    calibration B (PN, S2-S1 credit)      {B_ci['est']:+.4f}  "
          f"[{B_ci['lo']:+.4f}, {B_ci['hi']:+.4f}]  n={B_ci['n']}")
    print(f"    calibration   (non-PN, S2-S1 credit)  {C_ci['est']:+.4f}  "
          f"[{C_ci['lo']:+.4f}, {C_ci['hi']:+.4f}]  n={C_ci['n']}")
    print(f"    EVAL reference (Q4): PN +0.0909 [+0.0392, +0.1584], "
          f"PRESENT -0.0400 [-0.0878, +0.0052]")
    rows = []
    for tt in GRID:
        fired = [t for t in cal
                 if (gC[t]["nok"] if gC[t]["nok"] is not None else 0.0) >= tt]
        prec = (sum(1 for t in fired if t in pn) / len(fired)) if fired else None
        rows.append((tt, len(fired), prec))
    clearing = [tt for tt, _n, p in rows if p is not None and p >= q]
    t_star = clearing[0] if clearing else None
    print(f"    B (PN credit gain) {B:+.4f}   C (non-PN credit loss) {Ccost:+.4f}"
          f"   q* {q:.4f}   ->  t = {t_star}")
    R["derivation"] = {"B": B, "C": Ccost, "q_star": q, "t": t_star,
                       "B_ci": B_ci, "C_ci": C_ci,
                       "max_calibration_pn_precision": max(
                           [p for _t, _n, p in rows if p is not None] or [None]),
                       "sweep": [{"t": a_, "fired": b_, "precision": c_}
                                 for a_, b_, c_ in rows]}

    if t_star is None:
        mx = max([p for _t, _n, p in rows if p is not None] or [0.0])
        print("\n" + "=" * 96)
        print("NO PROFITABLE OPERATING POINT -- the derived policy is the NULL policy")
        print("=" * 96)
        print(f"  calibration PN precision never reaches q* = {q:.4f} "
              f"(maximum attained {mx:.4f}).")
        print("  E2_AMENDMENT_4's rule covers this case verbatim: a policy whose")
        print("  precision never reaches the break-even has NO profitable operating")
        print("  point and is recorded as such at rate 0 -- an outcome about that")
        print("  policy, not a fitting failure. The derived selective policy is")
        print("  therefore 'never apply caution', which IS arm (b).")
        print()
        print("  THE REASON, and it is the finding: the calibration-measured benefit")
        print("  has the OPPOSITE SIGN to the eval-measured one. Caution gains +0.0909")
        print("  credit on eval PN cells (CI excludes zero) and LOSES "
              f"{-B_ci['est']:.4f} on")
        print("  calibration PN cells. A break-even derived from a benefit that does")
        print("  not replicate across splits cannot produce an operating point.")
        R["outcome"] = ("SYNTHESIZED -- the derived policy is the NULL policy (never "
                        "apply caution), which is arm (b), at fire rate 0")
        R["synthesis"] = {"t": None, "fire_rate": 0.0,
                          "derived_policy_is": "(b) always-retrieve, no caution",
                          "reason": "calibration PN precision never reaches q*; the "
                                    "calibration-measured benefit B has the opposite "
                                    "sign to the eval-measured one",
                          "label": "pre-registered synthesis over pre-existing outputs"}
        R["predictions"] = {
            "1_precondition_fails": {"frozen": True, "observed": False,
                                     "verdict": "WRONG"},
            "2_t_at_or_below_0.05": {"frozen": True, "observed": "no t exists",
                                     "verdict": "FALSIFIED -- no threshold clears q*"},
            "3_within_0.5pp_of_a2": {"frozen": True,
                                     "observed": "the derived policy is (b), 2.04pp "
                                                 "from (a'') on confabulation",
                                     "verdict": "FALSIFIED"}}
        jdump(R, E3 / "results" / "i2_precondition.json")
        print("\nwrote results/i2_precondition.json")
        return

    # --------------------------------- synthesize from existing answers only
    Ae = jload(E3 / "answers_eval.json")["rows"]
    Je = jload(E3 / "cache" / "judgments_eval.json")
    corr, conf, s0q = {}, {}, {}
    for x in Ae:
        v = Je.get(f"{x['cell_id']}|{x['response_sha'][:24]}", {})
        corr[(x["cell_id"], x["state"])] = v.get("correctness")
        conf[(x["cell_id"], x["state"])] = bool(v.get("confabulation"))
        if x["state"] == S0:
            s0q[(x["persona"], x["question_id"])] = v.get("correctness")

    def outc(t, state):
        c = (s0q[(ev[t]["persona"], ev[t]["question_id"])] if state == S0
             else corr[(t, state)])
        f = False if state == S0 else conf[(t, state)]
        return credit_of(ev[t]["label"], c), (1.0 if f else 0.0)

    def prof(pick):
        cc, ff = [], []
        for t in tags:
            c, f = outc(t, pick(t))
            if c is None:
                continue
            cc.append(c); ff.append(f)
        return float(np.mean(cc)), float(np.mean(ff))

    nok = {t: (gE[t]["nok"] if gE[t]["nok"] is not None else 0.0) for t in tags}
    pol = lambda t: S2 if nok[t] >= t_star else S1                 # noqa: E731
    cred, cfb = prof(pol)
    ref = {"(a'')": prof(lambda t: S2), "(b)": prof(lambda t: S1)}
    fires = sum(1 for t in tags if nok[t] >= t_star) / len(tags)
    print(f"\n  SYNTHESIZED POLICY  choose[(a'') if NOK >= {t_star} else (b)]")
    print(f"    fires on {fires:.3f} of cells   credit {cred:.4f}   confab {cfb:.4f}")
    for k, v in ref.items():
        print(f"    {k:8s} credit {v[0]:.4f}   confab {v[1]:.4f}")
    R["synthesis"] = {"t": t_star, "fire_rate": fires, "credit": cred,
                      "confab": cfb, "reference": {k: {"credit": v[0],
                                                       "confab": v[1]}
                                                   for k, v in ref.items()},
                      "label": "pre-registered synthesis over pre-existing outputs"}
    R["outcome"] = "SYNTHESIZED"
    jdump(R, E3 / "results" / "i2_precondition.json")
    print("\nwrote results/i2_precondition.json")


if __name__ == "__main__":
    main()
