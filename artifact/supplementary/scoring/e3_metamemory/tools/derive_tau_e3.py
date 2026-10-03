"""
derive_tau_e3.py -- the operating point, by DERIVATION. NO NEW API CALLS.

PREREG_E3 section 5: the frozen object is the RULE, carried verbatim from
E2_AMENDMENT_4 section 1, and it is applied ONCE on the 8 calibration personas
under the L1W0D0 FOK scale. No argmax anywhere.

  G  = (w_P*g_P + w_N*g_N) / (w_P + w_N)     mean credit gain on a non-ABSENT cell
  L  = loss on an ABSENT cell
  p* = L / (G + L)
  tau_FOK = LOWEST grid threshold whose calibration precision for non-ABSENT >= p*

  suppression side, same logic on the confabulation axis:
  B  = confabulation reduction on PN cells from the application step
  C  = confabulation change elsewhere
  q* = C / (B + C);  if C <= 0 every threshold clears and tau_NOK is the grid
       minimum -- recorded, not hidden.

Gains and losses are measured S1 vs S0, exactly as E2 measured them: the FOK gate
decides whether to RETRIEVE, and the application step is a separate decision whose
break-even is the q* line. The application step in E3 is S3 (E3_AMENDMENT_1), so
B and C are measured S3 vs S1.

Also reported here and nowhere else before SP2: the sigma_a k-draw trigger
(PREREG_E3 2.3) and the power recomputation on H-E3a's measured variance
(PREREG_E3 2.2 -- reported, bands untouched).

Writes THRESHOLDS_E3_FROZEN.json and calibration_report_e3.json.

Usage:  python e3_metamemory/tools/derive_tau_e3.py
"""

from __future__ import annotations

import collections
import statistics as st
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e3_common import (E3, S0, S1, S2, S3, S3P, jdump, jload,      # noqa: E402
                       load_cells, sha)

GRID = [round(x * 0.05, 2) for x in range(21)]
SIGMA_A_TRIGGER = 0.065          # PREREG_E3 2.3, frozen
N_EVAL_CELLS = 834


def credit_of(label, c):
    if c is None:
        return None
    if label == "ABSENT":
        return 1.0 if c == "ABSTAIN" else 0.0
    return {"CORRECT": 1.0, "PARTIAL": 0.5, "WRONG": 0.0, "ABSTAIN": 0.0}.get(c, 0.0)


def main():
    cells = {c["cell_id"]: c for c in load_cells()["cells"]
             if c["split"] == "calibration"}
    tags = sorted(cells)
    gT = {r["cell_id"]: r for r in jload(E3 / "gates_calibration.json")["rows"]}
    ans = jload(E3 / "answers_calibration.json")["rows"]
    judg = jload(E3 / "cache" / "judgments_calibration.json")

    draws = collections.defaultdict(list)
    for a in ans:
        v = judg.get(f"{a['cell_id']}|{a['response_sha'][:24]}", {})
        c = credit_of(cells[a["cell_id"]]["label"], v.get("correctness"))
        if c is None:
            continue
        draws[(a["cell_id"], a["state"])].append((c, bool(v.get("confabulation"))))

    def cr(t, s):
        v = draws.get((t, s))
        return (sum(x[0] for x in v) / len(v)) if v else None

    def cf(t, s):
        v = draws.get((t, s))
        return (sum(1 for x in v if x[1]) / len(v)) if v else None

    def lab_mean(f, label, s):
        v = [f(t, s) for t in tags if cells[t]["label"] == label
             and f(t, s) is not None]
        return sum(v) / len(v) if v else None

    # ------------------------------------------------- the derivation
    base = collections.Counter(cells[t]["label"] for t in tags)
    n = len(tags)
    wP, wN, wA = (base["PRESENT"] / n, base["PRESENT-NEGATIVE"] / n,
                  base["ABSENT"] / n)
    gP = lab_mean(cr, "PRESENT", S1) - lab_mean(cr, "PRESENT", S0)
    gN = lab_mean(cr, "PRESENT-NEGATIVE", S1) - lab_mean(cr, "PRESENT-NEGATIVE", S0)
    lA = lab_mean(cr, "ABSENT", S0) - lab_mean(cr, "ABSENT", S1)
    G = (wP * gP + wN * gN) / (wP + wN)
    p_star = lA / (G + lA)

    nonabs = {t for t in tags if cells[t]["label"] != "ABSENT"}
    rows = []
    for tau in GRID:
        fired = [t for t in tags
                 if gT[t]["fok"] is not None and gT[t]["fok"] >= tau]
        prec = (sum(1 for t in fired if t in nonabs) / len(fired)) if fired else None
        rows.append({"tau": tau, "n_fired": len(fired),
                     "rate": len(fired) / len(tags), "precision": prec})
    clearing = [r for r in rows if r["precision"] is not None
                and r["precision"] >= p_star]
    tau_fok = clearing[0]["tau"] if clearing else None

    # ------------------------------------------------- suppression side
    pn = [t for t in tags if cells[t]["label"] == "PRESENT-NEGATIVE"]
    other = [t for t in tags if cells[t]["label"] != "PRESENT-NEGATIVE"]

    def dconf(sub):
        v = [(cf(t, S3) - cf(t, S1)) for t in sub
             if cf(t, S3) is not None and cf(t, S1) is not None]
        return sum(v) / len(v) if v else 0.0

    B, C = -dconf(pn), dconf(other)
    if C <= 0:
        q_star, tau_nok = 0.0, GRID[0]
        qnote = ("C <= 0: the application step does no harm off-target, so every "
                 "threshold clears and tau_NOK is the grid minimum. Recorded, not "
                 "hidden -- and it is the property that made the SP1 lobotomy a "
                 "no-op (D56) and forced E3_AMENDMENT_1.")
    else:
        q_star = C / (B + C)
        srows = []
        for tau in GRID:
            fired = [t for t in tags if (gT[t]["nok"] or 0) >= tau]
            prec = (sum(1 for t in fired if t in pn) / len(fired)) if fired else None
            srows.append((tau, prec))
        cl = [t for t, p in srows if p is not None and p >= q_star]
        tau_nok = cl[0] if cl else None
        qnote = "lowest threshold clearing q*"

    # ------------------------------------------------- sigma_a, the k trigger
    sig = []
    for (t, s), v in draws.items():
        if s in (S0, S1, S3) and len(v) >= 2:
            sig.append(st.stdev([x[0] for x in v]))
    sigma_a = sum(sig) / len(sig) if sig else 0.0
    k_decision = 3 if sigma_a > SIGMA_A_TRIGGER else 1

    # ------------------------------------------------- power recomputation
    def state_a(t):
        return S3 if (gT[t]["fok"] if gT[t]["fok"] is not None else -1) >= (tau_fok if tau_fok is not None else 2) else S0

    d = []
    for t in tags:
        a, b = cf(t, state_a(t)), cf(t, S1)
        if a is not None and b is not None:
            d.append(a - b)
    sd = float(np.std(d, ddof=1)) if len(d) > 1 else 0.0
    se_eval = sd / (N_EVAL_CELLS ** 0.5) if d else 0.0
    from statistics import NormalDist
    Nd = NormalDist()
    binding = max(0.03, 1.96 * se_eval) if se_eval > 0 else None
    power = {f"{int(x*100)}pp": (Nd.cdf((x - binding) / se_eval) if se_eval > 0 else None)
             for x in (0.03, 0.05, 0.07, 0.10, 0.115)}

    # H-E3b's margin, by the frozen rule (PREREG_E3 6.2)
    dk = []
    for t in tags:
        a, b = cr(t, state_a(t)), cr(t, S1)
        if a is not None and b is not None:
            dk.append(a - b)
    sd_credit = float(np.std(dk, ddof=1)) if len(dk) > 1 else 0.0
    se_credit = sd_credit / (N_EVAL_CELLS ** 0.5) if dk else 0.0
    raw_m = 2.4866 * se_credit
    margin = round((int(raw_m / 0.005) + 1) * 0.005, 3)
    margin_indeterminate = margin > 0.05

    frozen = {
        "frozen_at": "SP2, E3", "method": "DERIVED, no argmax",
        "rule_source": "E2_AMENDMENT_4 section 1, carried verbatim",
        "gate_prompt_cell": "L1W0D0",
        "answerer": jload(ROOT / "e2_metamemory" / "ANSWERER_FROZEN.json")["answerer_model"],
        "derivation": {"gain_PRESENT": gP, "gain_PN": gN, "loss_ABSENT": lA,
                       "base_PRESENT": wP, "base_PN": wN, "base_ABSENT": wA,
                       "G_mean_gain_nonabsent": G, "L": lA, "p_star": p_star,
                       "rule": "lowest grid threshold with calibration precision "
                               "for non-ABSENT >= p*"},
        "tau_FOK": tau_fok, "tau_NOK": tau_nok, "q_star": q_star,
        "B_pn_confab_reduction": B, "C_offtarget_confab_change": C,
        "q_note": qnote,
        "sigma_a": sigma_a, "sigma_a_trigger": SIGMA_A_TRIGGER, "k_decision": k_decision,
        "hE3b_margin": margin, "hE3b_margin_raw": raw_m,
        "hE3b_indeterminate_by_design": margin_indeterminate,
        "power_recomputation": {"paired_sd_confab": sd, "se_eval": se_eval,
                                "binding": binding, "power": power,
                                "bands_untouched": True},
        "calibration_rate_at_tau": next((r["rate"] for r in rows
                                         if r["tau"] == tau_fok), None),
        "retrieval_artifact_sha256": jload(E3 / "retrieval_frozen_e3.json")["artifact_sha256"],
        "index_artifact_sha256": jload(E3 / "indexes_e3.json")["artifact_sha256"],
        "index_artifact_sha256_lobotomy": jload(E3 / "indexes_e3.json")["artifact_sha256_lobotomy"],
        "hierarchy": ["H-E3a", "H-E3b", "H-E3c", "H-E3d"],
    }
    jdump(frozen, E3 / "THRESHOLDS_E3_FROZEN.json")
    jdump({"derivation": frozen["derivation"], "sweep": rows, "thresholds": frozen},
          E3 / "calibration_report_e3.json")

    print("=" * 96)
    print(f"DERIVATION (L1W0D0 gate, calibration n={n})")
    print("=" * 96)
    print(f"  gains: PRESENT +{gP:.4f}  PN +{gN:.4f}   loss: ABSENT -{lA:.4f}")
    print(f"  base rates: P {wP:.3f}  PN {wN:.3f}  ABSENT {wA:.3f}")
    print(f"  G = {G:.4f}   L = {lA:.4f}   ->   p* = L/(G+L) = {p_star:.4f}")
    print(f"  suppression: B (PN confab reduction) = {B:+.4f}  C (off-target) = {C:+.4f}")
    print(f"               q* = {q_star:.4f}  ->  tau_NOK = {tau_nok}")
    print(f"               [{qnote}]")
    print(f"\n  tau_FOK = {tau_fok}   "
          f"calibration precision {next((r['precision'] for r in rows if r['tau']==tau_fok), None)}"
          f"   rate {frozen['calibration_rate_at_tau']}")
    print("\n  grid sweep (tau, rate, precision vs p*):")
    for r in rows:
        if r["precision"] is None:
            continue
        mark = "  <- derived" if r["tau"] == tau_fok else ""
        print(f"    {r['tau']:.2f}  rate {r['rate']:.3f}  precision {r['precision']:.4f}"
              f"  {'>= p*' if r['precision'] >= p_star else '<  p*'}{mark}")

    print("\n" + "=" * 96)
    print("SP2 REPORTS -- bands untouched")
    print("=" * 96)
    print(f"  sigma_a measured {sigma_a:.4f} against the frozen trigger "
          f"{SIGMA_A_TRIGGER}  ->  k = {k_decision}")
    print(f"  H-E3a paired SD {sd:.4f}  ->  SE at n={N_EVAL_CELLS}: {se_eval:.5f}")
    print(f"    binding value {binding:.4f}; power at "
          + "  ".join(f"{k} {v:.1%}" for k, v in power.items() if v is not None))
    print(f"  H-E3b margin by the frozen rule: 2.4866 x {se_credit:.5f} = "
          f"{raw_m:.4f}  ->  m = {margin}"
          + ("   INDETERMINATE-BY-DESIGN (> 0.05)" if margin_indeterminate else ""))
    print("\nwrote THRESHOLDS_E3_FROZEN.json and calibration_report_e3.json")


if __name__ == "__main__":
    main()
