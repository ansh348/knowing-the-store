"""
derive_thresholds.py -- E2 Amendment 4 STEP 2: operating points by DERIVATION.

No argmax anywhere. Every thresholded policy takes the LOWEST grid threshold whose
calibration precision for non-ABSENT clears the break-even p* derived from the
measured per-label gains/losses and base rates under the pinned answerer. Same
formula, same inputs, every policy.

Writes THRESHOLDS_FROZEN.json (superseding the argmaxed version) and
calibration_report_v4.json.

Usage:  python e2_metamemory/tools/derive_thresholds.py
"""

from __future__ import annotations

import collections
import statistics as st
import sys
from pathlib import Path

import numpy as np
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e2_common import E2, S0, S1, S2, jdump, jload, load_items, usd   # noqa: E402

GRID = [round(x * 0.05, 2) for x in range(21)]
N_EVAL = 529


def credit_of(label, c):
    if c is None:
        return None
    if label == "ABSENT":
        return 1.0 if c == "ABSTAIN" else 0.0
    return {"CORRECT": 1.0, "PARTIAL": 0.5, "WRONG": 0.0, "ABSTAIN": 0.0}.get(c, 0.0)


def main():
    items = {i["item_id"]: i for i in load_items() if i["split"] == "calibration"}
    gates = {g["item_id"]: g for g in jload(E2 / "gates_calibration.json")["rows"]}
    answers = jload(E2 / "answers_calibration.json")["rows"]
    judg = jload(E2 / "cache" / "judgments_calibration.json")
    answerer = jload(E2 / "ANSWERER_FROZEN.json")["answerer_model"]
    tags = sorted(items)

    cell, tok = collections.defaultdict(list), collections.defaultdict(list)
    for a in answers:
        v = judg.get(f"{a['item_id']}|{a['response_sha'][:24]}", {})
        c = credit_of(items[a["item_id"]]["label_final"], v.get("correctness"))
        if c is None:
            continue
        cell[(a["item_id"], a["state"])].append((c, bool(v.get("confabulation"))))
        tok[a["state"]].append((a["prompt_tokens"] or 0, a["completion_tokens"] or 0))

    def cr(t, s):
        v = cell.get((t, s))
        return (sum(x[0] for x in v) / len(v)) if v else None

    def cf(t, s):
        v = cell.get((t, s))
        return (sum(1 for x in v if x[1]) / len(v)) if v else None

    def lab_mean(f, label, s):
        v = [f(t, s) for t in tags if items[t]["label_final"] == label
             and f(t, s) is not None]
        return sum(v) / len(v) if v else None

    # ---------------- the derivation (Amendment 4 section 1) -----------------
    base = collections.Counter(items[t]["label_final"] for t in tags)
    n = len(tags)
    wP, wN, wA = base["PRESENT"] / n, base["PRESENT-NEGATIVE"] / n, base["ABSENT"] / n
    gP = lab_mean(cr, "PRESENT", S1) - lab_mean(cr, "PRESENT", S0)
    gN = lab_mean(cr, "PRESENT-NEGATIVE", S1) - lab_mean(cr, "PRESENT-NEGATIVE", S0)
    lA = lab_mean(cr, "ABSENT", S0) - lab_mean(cr, "ABSENT", S1)
    G = (wP * gP + wN * gN) / (wP + wN)
    p_star = lA / (G + lA)

    nonabs = {t for t in tags if items[t]["label_final"] != "ABSENT"}

    def signal(policy, t):
        g = gates[t]
        ix = g["indexed"].get("1") or g["indexed"].get(1) or {}
        vb = g["verbal"].get("1") or g["verbal"].get(1) or {}
        if policy == "iii":
            return g["sim_max_blended"]
        if policy == "iv":
            return vb.get("p_store_has_relevant")
        return ix.get("fok")

    def derive(policy):
        rows = []
        for tau in GRID:
            fired = [t for t in tags
                     if (signal(policy, t) is not None and signal(policy, t) >= tau)]
            prec = (sum(1 for t in fired if t in nonabs) / len(fired)) if fired else None
            rows.append({"tau": tau, "n_fired": len(fired),
                         "rate": len(fired) / len(tags), "precision": prec})
        clearing = [r for r in rows if r["precision"] is not None
                    and r["precision"] >= p_star]
        return (clearing[0]["tau"] if clearing else None), rows

    derived = {}
    sweeps = {}
    for pol in ("iii", "iv", "v"):
        tau, rows = derive(pol)
        derived[pol] = tau
        sweeps[pol] = rows

    # ---------------- suppression side: q* and tau_NOK -----------------------
    pn = [t for t in tags if items[t]["label_final"] == "PRESENT-NEGATIVE"]
    other = [t for t in tags if items[t]["label_final"] != "PRESENT-NEGATIVE"]

    def dconf(sub):
        v = [(cf(t, S2) - cf(t, S1)) for t in sub
             if cf(t, S2) is not None and cf(t, S1) is not None]
        return sum(v) / len(v) if v else 0.0

    B = -dconf(pn)                       # benefit on PN: confab reduction
    C = dconf(other)                     # cost elsewhere: confab increase
    if C <= 0:
        q_star, tau_nok, qnote = 0.0, GRID[0], (
            "C <= 0: the caution instruction does no harm off-target, so every "
            "threshold clears and tau_NOK is the grid minimum. Recorded, not hidden.")
    else:
        q_star = C / (B + C)
        rows = []
        for tau in GRID:
            fired = [t for t in tags
                     if (gates[t]["indexed"].get("1") or {}).get("nok", 0) >= tau]
            prec = (sum(1 for t in fired if t in pn) / len(fired)) if fired else None
            rows.append((tau, prec))
        clearing = [t for t, p in rows if p is not None and p >= q_star]
        tau_nok = clearing[0] if clearing else None
        qnote = "lowest threshold clearing q*"

    # ---------------- simulate at the derived points -------------------------
    gate_tok = collections.defaultdict(list)
    for r in jload(E2 / "cache" / "responses.json").values():
        a = str(r.get("arm", ""))
        if a.startswith("gate-"):
            gate_tok[a.split("-d")[0]].append((r["prompt_tokens"], r["completion_tokens"]))
    c_gate = {k: usd(sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v))
              for k, v in gate_tok.items()}
    c_ans = {s: usd(sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v))
             for s, v in tok.items()}

    def decide(policy, t):
        if policy == "i":
            return True
        if policy == "ii":
            return False
        if policy == "vii":
            import hashlib
            h = int(hashlib.sha256(f"42|{t}".encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
            return h < derived_rate_v
        pol = "v" if policy in ("v", "vi") else policy
        tau = derived[pol]
        s = signal(pol, t)
        return tau is not None and s is not None and s >= tau

    def state_of(policy, t):
        if not decide(policy, t):
            return S0
        if policy == "vi" and tau_nok is not None:
            nk = (gates[t]["indexed"].get("1") or {}).get("nok")
            if nk is not None and nk >= tau_nok:
                return S2
        return S1

    derived_rate_v = sum(1 for t in tags if decide("v", t)) / len(tags)

    sim = {}
    for pol in ("i", "ii", "iii", "iv", "v", "vi", "vii"):
        crs, cfs, cost, nret = [], [], [], 0
        for t in tags:
            s = state_of(pol, t)
            c, f = cr(t, s), cf(t, s)
            if c is None:
                continue
            crs.append(c); cfs.append(f)
            gc = (c_gate.get("gate-verbal", 0) if pol == "iv"
                  else c_gate.get("gate-indexed", 0) if pol in ("v", "vi") else 0.0)
            cost.append(gc + c_ans.get(s, 0))
            nret += 1 if s != S0 else 0
        sim[pol] = {"credit": float(np.mean(crs)), "confab": float(np.mean(cfs)),
                    "cost": float(np.mean(cost)), "rate": nret / len(tags),
                    "tau": derived.get("v" if pol in ("v", "vi") else pol)}

    # ---------------- power on the NEW primary, H-C2 -------------------------
    d = []
    for t in tags:
        a, b = cf(t, state_of("vi", t)), cf(t, state_of("v", t))
        if a is not None and b is not None:
            d.append(a - b)
    sd = float(np.std(d, ddof=1)) if len(d) > 1 else 0.0
    se_eval = (sd / (len(d) ** 0.5)) * ((len(d) / N_EVAL) ** 0.5) if d else 0.0
    se_eval = sd / (N_EVAL ** 0.5) if d else 0.0
    Nd = NormalDist()
    power_hc2 = (1 - Nd.cdf((1.96 * se_eval - 0.03) / se_eval)) if se_eval > 0 else None
    n_fire = sum(1 for t in tags if state_of("vi", t) == S2)

    frozen = {
        "frozen_at": "SP2 round 4 (Amendment 4)", "method": "DERIVED, no argmax",
        "answerer": answerer,
        "derivation": {"gain_PRESENT": gP, "gain_PN": gN, "loss_ABSENT": lA,
                       "base_PRESENT": wP, "base_PN": wN, "base_ABSENT": wA,
                       "G_mean_gain_nonabsent": G, "L": lA, "p_star": p_star,
                       "rule": "lowest grid threshold with calibration precision "
                               "for non-ABSENT >= p*"},
        "tau_sim": derived["iii"], "tau_verb": derived["iv"], "tau_FOK": derived["v"],
        "tau_NOK": tau_nok, "q_star": q_star, "B_pn_confab_reduction": B,
        "C_offtarget_confab_change": C, "q_note": qnote,
        "calibration_rates": {k: v["rate"] for k, v in sim.items()},
        "retrieval_artifact_sha256": jload(E2 / "retrieval_frozen.json")["artifact_sha256"],
        "hierarchy": ["H-C2", "H-C1a", "H-C1b"],
        "cost_model": {"c_gate": c_gate, "c_answer": c_ans},
    }
    jdump(frozen, E2 / "THRESHOLDS_FROZEN.json")
    jdump({"derivation": frozen["derivation"], "sweeps": sweeps, "sim": sim,
           "hc2_power": {"paired_sd": sd, "n": len(d), "se_eval": se_eval,
                         "power_at_3pp": power_hc2, "n_caution_fires": n_fire},
           "thresholds": frozen}, E2 / "calibration_report_v4.json")

    print("=" * 96)
    print(f"DERIVATION (answerer {answerer}, calibration n={len(tags)})")
    print("=" * 96)
    print(f"  gains: PRESENT +{gP:.4f}  PN +{gN:.4f}   loss: ABSENT -{lA:.4f}")
    print(f"  base rates: P {wP:.3f}  PN {wN:.3f}  ABSENT {wA:.3f}")
    print(f"  G = {G:.4f}   L = {lA:.4f}   ->   p* = L/(G+L) = {p_star:.4f}")
    print(f"  suppression: B (PN confab reduction) = {B:+.4f}  C (off-target) = {C:+.4f}")
    print(f"               q* = {q_star:.4f}  ->  tau_NOK = {tau_nok}   [{qnote}]")
    print("\n" + "=" * 96)
    print("DERIVED OPERATING POINTS (lowest threshold clearing p*)")
    print("=" * 96)
    for pol in ("iii", "iv", "v"):
        t = derived[pol]
        row = next((r for r in sweeps[pol] if r["tau"] == t), None)
        if t is None:
            print(f"  ({pol:3s}) NO PROFITABLE OPERATING POINT — precision never reaches p*")
        else:
            print(f"  ({pol:3s}) tau {t:.2f}  precision {row['precision']:.3f}  "
                  f"rate {row['rate']:.3f}")
    print("\n" + "=" * 96)
    print("POLICIES AT THEIR DERIVED POINTS")
    print("=" * 96)
    print(f"{'policy':8s}{'tau':>7s}{'rate':>8s}{'credit':>9s}{'confab':>9s}{'cost':>11s}")
    for pol in ("i", "ii", "iii", "iv", "v", "vi", "vii"):
        v = sim[pol]
        tt = f"{v['tau']:.2f}" if v["tau"] is not None else "--"
        print(f"({pol:5s}){tt:>7s}{v['rate']:8.3f}{v['credit']:9.4f}"
              f"{v['confab']:9.4f}{v['cost']:11.6f}")
    print("\n" + "=" * 96)
    print("H-C2 POWER (new primary; bands untouched)")
    print("=" * 96)
    print(f"  caution fires on {n_fire}/{len(tags)} calibration items")
    print(f"  paired SD {sd:.4f} over n={len(d)}  ->  SE_eval {se_eval:.5f}")
    print(f"  power at the frozen 3pp band: "
          f"{('%.1f%%' % (100*power_hc2)) if power_hc2 is not None else 'n/a'}")
    print("\nwrote THRESHOLDS_FROZEN.json and calibration_report_v4.json")


if __name__ == "__main__":
    main()
