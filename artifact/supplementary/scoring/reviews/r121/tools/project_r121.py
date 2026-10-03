# -*- coding: utf-8 -*-
"""project_r121.py -- program R121 (the intent crossover): the Phase 0 cost projection. NO MODEL CALL.

Per-call bases are the recorded CF-2 rows of each reader on the same prompts (cf2/rows/rows_{MINI,H45,OP5,LUNA}.jsonl,
arms INDEXED-V2 and INDEXED-V3; the Anthropic rows carry the Batch 0.5 multiplier in their usd; Luna's are E5's raw-API
rows with the cache engaged on draws 2-5). Design D0 is the brief; the options are the ones the Phase 0 report puts to
the author. Writes reviews/r121/results/projection_r121.json and prints the table.

Units: population A = 88 supersession pairs on the v2 summary, B = 30 expiry pairs on the v3 summary.
  P0 new: cells 3 and 4                       -> 2 units per pair
  P1 new: cells 1, 2, 3, 4                    -> 4 units per pair
  Luna only: P0 cells 1 and 2 on B (v3), not recorded -> 2 units per B pair
P1 adds 113 o200k tokens to the system text (prompts_p1.py); the Anthropic count is scaled by each reader's recorded
input-token ratio to the OpenAI count on the same prompts.
"""
from __future__ import annotations

import io
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
ROWS = ROOT / "r82_counterfactual" / "cf2" / "rows"
OUT = ROOT / "reviews" / "r121" / "results" / "projection_r121.json"
N_A, N_B = 88, 30
P1_DELTA_O200K = 113
MINI_IN_V2 = 1615.6          # the OpenAI tokenizer's count of the v2 prompts (mini rows)
CAP_ANTHROPIC, CAP_OPENAI = 16.0, 4.0

PRICE = {  # $/M input, $/M output, multiplier (Batch 0.5 for the Anthropic lanes, as the recorded rows)
    "MINI": (0.40, 1.60, 1.0), "H45": (1.00, 5.00, 0.5), "OP5": (5.00, 25.00, 0.5),
}


def rows(code):
    return [json.loads(l) for l in io.open(ROWS / f"rows_{code}.jsonl", encoding="utf-8") if l.strip()]


def basis(code, arm):
    ok = [r for r in rows(code) if r.get("status") == "OK" and r.get("arm") == arm and "tok_in" in r]
    tin = np.array([r["tok_in"] for r in ok], float); tout = np.array([r["tok_out"] for r in ok], float)
    usd = np.array([r.get("usd", 0.0) for r in ok], float)
    return {"n": len(ok), "in_mean": float(tin.mean()), "out_mean": float(tout.mean()), "out_p95": float(np.percentile(tout, 95)),
            "usd_mean": float(usd.mean())}


def per_call(code, arm, p1, high=False):
    """usd per call: the recorded mean, plus P1's system-text delta, at the recorded mean output (or p95 when high)."""
    b = BASIS[code][arm]
    if code == "LUNA":
        # E5's rows: draw 1 a cache write, draws 2-5 cache reads; usd from the rows per draw (AUX-CF2-OAI-DRAWS)
        d1, dn = LUNA_DRAW1, LUNA_DRAWN
        extra = P1_DELTA_O200K / 1e6 * 0.20 * (1.25 if high else 1.0) if p1 else 0.0
        return {"draw1": d1 + extra, "drawn": dn + extra * 0.1, "nocache": d1 + extra}
    pin, pout, mult = PRICE[code]
    scale = b["in_mean"] / MINI_IN_V2 if code != "MINI" else 1.0
    tin = b["in_mean"] + (P1_DELTA_O200K * scale if p1 else 0.0)
    tout = b["out_p95"] if high else b["out_mean"]
    return (tin / 1e6 * pin + tout / 1e6 * pout) * mult


BASIS = {code: {arm: basis(code, arm) for arm in ("INDEXED-V2", "INDEXED-V3")} for code in ("MINI", "H45", "OP5")}
BASIS["LUNA"] = {"INDEXED-V2": basis("LUNA", "INDEXED-V2")}
BASIS["LUNA"]["INDEXED-V3"] = dict(BASIS["LUNA"]["INDEXED-V2"], note="v3 not recorded for Luna; v2 basis + 52 tokens")
_luna = [r for r in rows("LUNA") if r.get("status") == "OK"]
LUNA_DRAW1 = float(np.mean([r["usd"] for r in _luna if int(r["draw"]) == 1]))
LUNA_DRAWN = float(np.mean([r["usd"] for r in _luna if int(r["draw"]) >= 2]))


def lane_cost(code, k, units_A, units_B, p1_units_A, p1_units_B, high=False, luna_cache=True):
    """units_*: (P0 new units, P1 new units) per population; returns usd."""
    if code == "LUNA":
        tot = 0.0
        for arm, (u0, u1) in (("INDEXED-V2", (units_A, p1_units_A)), ("INDEXED-V3", (units_B, p1_units_B))):
            for p1, u in ((False, u0), (True, u1)):
                pc = per_call(code, arm, p1, high)
                tot += u * (pc["draw1"] + (k - 1) * pc["drawn"]) if luna_cache else u * k * pc["nocache"]
        return tot
    tot = 0.0
    for arm, (u0, u1) in (("INDEXED-V2", (units_A, p1_units_A)), ("INDEXED-V3", (units_B, p1_units_B))):
        tot += k * (u0 * per_call(code, arm, False, high) + u1 * per_call(code, arm, True, high))
    return tot


def design(name, k_opus, opus_units=None, haiku_k=5, note=""):
    """Default units: P0 new 2 per pair, P1 new 4 per pair, on both populations."""
    u = {"A0": 2 * N_A, "A1": 4 * N_A, "B0": 2 * N_B, "B1": 4 * N_B}
    ou = opus_units or u
    d = {"name": name, "note": note, "k_opus": k_opus, "k_haiku": haiku_k}
    for high in (False, True):
        tag = "high" if high else "expected"
        mini = lane_cost("MINI", 1, u["A0"], u["B0"], u["A1"], u["B1"], high)
        haiku = lane_cost("H45", haiku_k, u["A0"], u["B0"], u["A1"], u["B1"], high)
        opus = lane_cost("OP5", k_opus, ou["A0"], ou["B0"], ou["A1"], ou["B1"], high) if k_opus else 0.0
        luna_c = lane_cost("LUNA", 5, u["A0"], u["B0"] + 2 * N_B, u["A1"], u["B1"], high, luna_cache=True)
        luna_n = lane_cost("LUNA", 5, u["A0"], u["B0"] + 2 * N_B, u["A1"], u["B1"], high, luna_cache=False)
        gen = 2 * (N_A + N_B) * (330 / 1e6 * 0.40 + 30 / 1e6 * 1.60)        # two seeds per pair, the renderer's prompt ~330 tokens
        leak = 2 * 30 * (1700 / 1e6 * 0.40 + 25 / 1e6 * 1.60)                 # the summary-leakage screen on the crossed questions, v2 and v3
        d[tag] = {"mini": round(mini, 3), "haiku": round(haiku, 3), "opus": round(opus, 3), "luna_cache": round(luna_c, 3), "luna_nocache": round(luna_n, 3),
                  "generation": round(gen, 3), "leakscreen": round(leak, 3),
                  "anthropic": round(haiku + opus, 3), "anthropic_x1.3": round(1.3 * (haiku + opus), 3),
                  "openai_cache": round(mini + luna_c + gen + leak, 3), "openai_nocache": round(mini + luna_n + gen + leak, 3),
                  "openai_nocache_x1.3": round(1.3 * (mini + luna_n + gen + leak), 3),
                  "calls": {"mini": u["A0"] + u["A1"] + u["B0"] + u["B1"], "haiku": haiku_k * (u["A0"] + u["A1"] + u["B0"] + u["B1"]),
                            "opus": k_opus * (ou["A0"] + ou["A1"] + ou["B0"] + ou["B1"]), "luna": 5 * (u["A0"] + u["A1"] + u["B0"] + 2 * N_B + u["B1"])}}
    d["fits_anthropic_cap_x1.3"] = d["expected"]["anthropic_x1.3"] <= CAP_ANTHROPIC
    d["fits_openai_cap_x1.3"] = d["expected"]["openai_nocache_x1.3"] <= CAP_OPENAI
    return d


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    designs = [
        design("D0: the brief (Opus k=3, Haiku k=5, all cells, both populations)", 3),
        design("O2: Opus k=1 on every new cell (the V2R-CAT draw-1 precedent), Haiku k=5", 1),
        design("O9: Opus k=3 on population A, P0 cell 3 + P1 cells 1 and 3 only; Haiku k=5 full", 3,
               opus_units={"A0": N_A, "A1": 2 * N_A, "B0": 0, "B1": 0}, note="Opus gets the primary estimand on A under both arms; no B, no interaction, no pooled AUROC"),
        design("O6: no Opus; Haiku k=5 full", 0),
        design("O4: Opus k=3 on population A only, all cells; Haiku k=5 full", 3, opus_units={"A0": 2 * N_A, "A1": 4 * N_A, "B0": 0, "B1": 0}),
    ]
    res = {"basis": BASIS, "luna_per_call": {"draw1": LUNA_DRAW1, "drawn": LUNA_DRAWN}, "p1_delta_o200k": P1_DELTA_O200K,
           "caps": {"anthropic": CAP_ANTHROPIC, "openai": CAP_OPENAI}, "designs": designs}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1, sort_keys=True) + "\n")
    print("per-call bases (recorded rows):")
    for code, arms in BASIS.items():
        for arm, b in arms.items():
            print(f"  {code:5s} {arm:11s} n={b['n']:5d} in {b['in_mean']:7.1f} out {b['out_mean']:6.1f} p95 {b['out_p95']:6.1f} usd {b['usd_mean']:.6f}")
    print(f"  LUNA per call: draw 1 ${LUNA_DRAW1:.6f} (cache write), draws 2-5 ${LUNA_DRAWN:.6f} (cache read)")
    print(f"\n{'design':90s} {'calls O/H/M/L':>22s} {'Anth exp':>9s} {'x1.3':>7s} {'high':>7s} {'OpenAI exp(cache/no)':>21s} {'x1.3 no':>8s} fits")
    for d in designs:
        e, h = d["expected"], d["high"]; c = e["calls"]
        print(f"{d['name'][:90]:90s} {c['opus']:5d}/{c['haiku']:5d}/{c['mini']:4d}/{c['luna']:5d} {e['anthropic']:9.2f} {e['anthropic_x1.3']:7.2f} {h['anthropic']:7.2f} "
              f"{e['openai_cache']:9.2f}/{e['openai_nocache']:6.2f} {e['openai_nocache_x1.3']:8.2f} {'A' if d['fits_anthropic_cap_x1.3'] else '-'}{'O' if d['fits_openai_cap_x1.3'] else '-'}")
    print(f"\ncaps: Anthropic ${CAP_ANTHROPIC:.0f}, OpenAI ${CAP_OPENAI:.0f}; fits = at x1.3 of the expected reading\n-> {OUT}")


if __name__ == "__main__":
    main()
