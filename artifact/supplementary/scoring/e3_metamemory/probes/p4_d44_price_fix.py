"""p4_d44_price_fix.py -- D44 rider: reprice the ANSWER component of RESULTS_E2 §3.11.

READ-ONLY over every E2 artifact. NO API CALLS. Recomputes the two cost columns of
the §3.11 economics table with the answerer priced at its own verified list rate
instead of gpt-4.1-mini's, and prints old vs new side by side.

D44-E2 recorded that `e2_common.usd()` prices every token at gpt-4.1-mini's
$0.40/$1.60 while the answerer, after Amendment 3, is gpt-5.4. The GATE is
gpt-4.1-mini and was priced correctly; only the answer component was wrong.

VERIFIED LIST PRICE, 2026-08-11, developers.openai.com/api/docs/pricing
("Prices per 1M tokens", short-context columns, model row "gpt-5.4 (<272K context
length)"):

    gpt-5.4       input $2.50   cached input $0.25   output $15.00
    gpt-4.1-mini  input $0.40   cached input $0.10   output $1.60

Corroborated independently at openrouter.ai/openai/gpt-5.4 ($2.50 in / $15.00 out).

NOTHING ELSE IN THE COST MODEL IS TOUCHED. The gate's cached-input multiplier stays
at E1.8's measured asymptotic 0.399 rather than the list 0.10 ratio, because that
is what E2 froze and this rider corrects a price, not a method.

Usage:  python e3_metamemory/probes/p4_d44_price_fix.py
"""

from __future__ import annotations

import collections
import hashlib
import io
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E2 = PROJECT_ROOT / "e2_metamemory"
sys.path.insert(0, str(E2 / "tools"))

from e2_common import S0, S1, S2, jload, load_items  # noqa: E402

OUT = Path(__file__).resolve().parent / "p4_d44_price_fix.json"

PRICE_OLD = {"gate": (0.40, 1.60), "answer": (0.40, 1.60)}     # what E2 shipped
PRICE_NEW = {"gate": (0.40, 1.60), "answer": (2.50, 15.00)}    # verified 2026-08-11
GATE_CACHE_MULT = 0.399           # E1.8 asymptotic, frozen -- not re-derived here
POLICIES = ("i", "ii", "iii", "iv", "v", "vi", "vii")


def usd(tin, tout, price):
    return tin / 1e6 * price[0] + tout / 1e6 * price[1]


def main():
    items = {i["item_id"]: i for i in load_items()}
    tags = sorted(i["item_id"] for i in load_items() if i["split"] == "eval")
    thr = jload(E2 / "THRESHOLDS_FROZEN.json")
    g = {r["item_id"]: r for r in jload(E2 / "gates_eval.json")["rows"]}
    ans = jload(E2 / "answers_eval.json")["rows"]

    tok = collections.defaultdict(list)
    for a in ans:
        tok[a["state"]].append((a["prompt_tokens"] or 0, a["completion_tokens"] or 0))
    gate_tok = collections.defaultdict(list)
    for r in jload(E2 / "cache" / "responses.json").values():
        arm = str(r.get("arm", ""))
        if arm.startswith("gate-"):
            gate_tok[arm.split("-d")[0]].append((r["prompt_tokens"], r["completion_tokens"]))

    def costs(price):
        cg = {k: usd(sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v),
                     price["gate"]) for k, v in gate_tok.items()}
        ca = {s: usd(sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v),
                     price["answer"]) for s, v in tok.items()}
        cgc = dict(cg)
        cgc["gate-indexed"] = cg.get("gate-indexed", 0) * GATE_CACHE_MULT
        return cg, cgc, ca

    def sig(pol, t):
        r = g[t]
        ix = r["indexed"].get("1") or {}
        vb = r["verbal"].get("1") or {}
        if pol == "iii":
            return r["sim_max_blended"]
        if pol == "iv":
            return vb.get("p_store_has_relevant")
        return ix.get("fok")

    TAU = {"iii": thr["tau_sim"], "iv": thr["tau_verb"], "v": thr["tau_FOK"],
           "vi": thr["tau_FOK"]}

    def retrieves(pol, t, rate_v):
        if pol == "i":
            return True
        if pol == "ii":
            return False
        if pol == "vii":
            h = int(hashlib.sha256(f"42|{t}".encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
            return h < rate_v
        tau = TAU[pol]
        if tau is None:
            return False
        s = sig("v" if pol == "vi" else pol, t)
        return s is not None and s >= tau

    def state_of(pol, t, rate_v):
        if not retrieves(pol, t, rate_v):
            return S0
        if pol == "vi":
            nk = (g[t]["indexed"].get("1") or {}).get("nok")
            if thr["tau_NOK"] is not None and nk is not None and nk >= thr["tau_NOK"]:
                return S2
        return S1

    rate_v = sum(1 for t in tags if retrieves("v", t, 0)) / len(tags)

    def table(price):
        cg, cgc, ca = costs(price)
        out = {}
        for pol in POLICIES:
            c, cc = [], []
            for t in tags:
                s = state_of(pol, t, rate_v)
                gc = (cg.get("gate-verbal", 0) if pol == "iv"
                      else cg.get("gate-indexed", 0) if pol in ("v", "vi") else 0.0)
                gcc = (cgc.get("gate-verbal", 0) if pol == "iv"
                       else cgc.get("gate-indexed", 0) if pol in ("v", "vi") else 0.0)
                c.append(gc + ca.get(s, 0))
                cc.append(gcc + ca.get(s, 0))
            out[pol] = {"cost": sum(c) / len(c), "cost_cached": sum(cc) / len(cc),
                        "gate_component": (cg.get("gate-verbal", 0) if pol == "iv"
                                           else cg.get("gate-indexed", 0)
                                           if pol in ("v", "vi") else 0.0)}
        return out, cg, cgc, ca

    old, cg_o, cgc_o, ca_o = table(PRICE_OLD)
    new, cg_n, cgc_n, ca_n = table(PRICE_NEW)

    stored = jload(E2 / "results" / "e2_scores.json")["policy_table"]

    print("=" * 100)
    print("p4 / D44 RIDER -- §3.11 answer component repriced at the VERIFIED gpt-5.4 rate")
    print("=" * 100)
    print("  verified 2026-08-11, developers.openai.com/api/docs/pricing, per 1M tokens:")
    print("    gpt-5.4       short-context input $2.50   cached input $0.25   output $15.00")
    print("    gpt-4.1-mini  input $0.40   cached input $0.10   output $1.60   (gate: unchanged)")
    print()
    print("  mean tokens per call, by context state (exact; these were never in doubt):")
    for s in (S0, S1, S2):
        v = tok.get(s) or []
        if v:
            print(f"    {s:>3s}  n={len(v):5d}  in {sum(x[0] for x in v) / len(v):8.1f}  "
                  f"out {sum(x[1] for x in v) / len(v):6.1f}   "
                  f"${ca_o[s] * 1e6:7.1f}/1M -> ${ca_n[s] * 1e6:7.1f}/1M")
    for k, v in sorted(gate_tok.items()):
        print(f"    {k:>13s}  n={len(v):5d}  in {sum(x[0] for x in v) / len(v):8.1f}  "
              f"out {sum(x[1] for x in v) / len(v):6.1f}   ${cg_o[k] * 1e6:7.1f}/1M "
              "(gate, unchanged)")

    print("\n  §3.11 ECONOMICS TABLE -- $ per 1M turns")
    print(f"  {'policy':26s}{'OLD $/1M':>10s}{'NEW $/1M':>10s}{'OLD cached':>12s}"
          f"{'NEW cached':>12s}{'gate share NEW':>16s}")
    NAMES = {"i": "(i) always", "ii": "(ii) never", "iii": "(iii) similarity",
             "iv": "(iv) verbalized", "v": "(v) FOK", "vi": "(vi) FOK+NOK",
             "vii": "(vii) rate-matched random"}
    for pol in POLICIES:
        share = (new[pol]["gate_component"] / new[pol]["cost"]) if new[pol]["cost"] else 0
        print(f"  {NAMES[pol]:26s}{old[pol]['cost'] * 1e6:10.0f}"
              f"{new[pol]['cost'] * 1e6:10.0f}{old[pol]['cost_cached'] * 1e6:12.0f}"
              f"{new[pol]['cost_cached'] * 1e6:12.0f}{share:15.1%}")

    # reproduction check against the committed scores
    bad = [p for p in POLICIES
           if abs(old[p]["cost"] - stored[p]["cost"]) > 5e-7
           or abs(old[p]["cost_cached"] - stored[p]["cost_cached"]) > 5e-7]
    print(f"\n  reproduction check vs committed e2_scores.json (OLD prices): "
          f"{'PASS -- all 7 policies match' if not bad else 'FAIL: ' + str(bad)}")

    print("\n  What the correction does to the paper's sentence:")
    r_old_v = old["v"]["cost"] / old["ii"]["cost"]
    r_new_v = new["v"]["cost"] / new["ii"]["cost"]
    r_old_ia = old["v"]["cost"] / old["i"]["cost"]
    r_new_ia = new["v"]["cost"] / new["i"]["cost"]
    print(f"    (v) vs never-retrieve   : {r_old_v:.1f}x  ->  {r_new_v:.1f}x")
    print(f"    (v) vs always-retrieve  : {r_old_ia:.1f}x  ->  {r_new_ia:.1f}x")
    print(f"    (v) cached vs always    : "
          f"{old['v']['cost_cached'] / old['i']['cost']:.1f}x  ->  "
          f"{new['v']['cost_cached'] / new['i']['cost']:.1f}x")
    print("    Direction is exactly the one D44 predicted: pricing the answer correctly")
    print("    raises every policy's answer component, so the GATE's share of the total")
    print("    falls and the gate's relative cost disadvantage shrinks.")

    payload = {
        "verified_on": "2026-08-11",
        "source": "https://developers.openai.com/api/docs/pricing",
        "corroboration": "https://openrouter.ai/openai/gpt-5.4",
        "price_gpt_5_4_per_1m": {"input": 2.50, "cached_input": 0.25, "output": 15.00,
                                 "context_tier": "<272K"},
        "price_gpt_4_1_mini_per_1m": {"input": 0.40, "cached_input": 0.10, "output": 1.60},
        "gate_cache_multiplier": GATE_CACHE_MULT,
        "reproduction_of_committed_old_table": not bad,
        "old": {p: {k: v for k, v in old[p].items()} for p in POLICIES},
        "new": {p: {k: v for k, v in new[p].items()} for p in POLICIES},
        "answer_cost_per_1m_by_state_old": {s: ca_o[s] * 1e6 for s in ca_o},
        "answer_cost_per_1m_by_state_new": {s: ca_n[s] * 1e6 for s in ca_n},
    }
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print(f"\n  written: {OUT}")


if __name__ == "__main__":
    main()
