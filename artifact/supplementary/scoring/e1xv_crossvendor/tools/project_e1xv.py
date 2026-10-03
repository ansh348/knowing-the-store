"""project_e1xv.py -- E1-XV STEP 0(e): the itemised projection against the $15 cap.

Every figure is computed from `manifests/calibration.json` (measured token usage on
REAL cell prompts) and `manifests/lane_pings.json`. Nothing is typed by hand, and
no chat-model assumption is applied to the reasoning lane: the K3 line is itemised
from its measured reasoning-token consumption at DEFAULT effort.

Run: python project_e1xv.py
"""
from __future__ import annotations

import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
XV = ROOT / "e1xv_crossvendor"
MAN = XV / "manifests"

CAP = 28.00          # raised at SP-0 ruling 1 (was $15)
N_ITEMS, N_ARMS = 84, 2
K = 5                # SP-0 ruling 1: k=5 retained; the slack IS the protocol

# USD per 1M tokens (input, output), list price at run date 2026-08-13.
# Anthropic: platform.claude.com/docs/en/about-claude/pricing
# Moonshot : platform.kimi.ai/docs/pricing/chat-k3  ($0.30 cache-hit input NOT assumed)
PRICES = {"claude-opus-5": (5.00, 25.00),
          "claude-opus-4-5-20251101": (5.00, 25.00),
          "claude-haiku-4-5-20251001": (1.00, 5.00),
          "kimi-k3": (3.00, 15.00)}

# The three pinned lanes, keyed to the calibration run that measures each.
LANES = [
    ("Anthropic frontier", "claude-opus-5",
     "PILOT Opus 5 at raised ceiling 1024 -- natural length", True),
    ("Anthropic cheap", "claude-haiku-4-5-20251001",
     "PILOT Haiku 4.5 parse rate at frozen ceiling 200", True),
    ("Kimi K3 (Moonshot direct)", "kimi-k3",
     "K3 default effort, n=6 both arms -- projection basis", False),
]
K3_LOW = "K3 effort-controllability probe: reasoning_effort=low"


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def runs():
    return {r["tag"]: r for r in jload(MAN / "calibration.json")["runs"] if r.get("tag")}


def per_call(run):
    pin, pout = PRICES[run["model"]]
    n = run["n_calls"]
    ti, to = run["tok_in"] / n, run["tok_out"] / n
    return ti, to, ti / 1e6 * pin + to / 1e6 * pout


def spent():
    """Everything E1-XV has actually billed so far: pings + calibration."""
    total, rows = 0.0, []
    for r in jload(MAN / "calibration.json")["runs"]:
        pin, pout = PRICES[r["model"]]
        usd = r["tok_in"] / 1e6 * pin + r["tok_out"] / 1e6 * pout
        total += usd
        rows.append((f"calib {r['model']} {r.get('tag', '')[:44]}", r["n_calls"], usd))
    # ---- SP-0 ruling 1 verification: batch vs sync, and the sync-repeat control.
    # Token counts are read from the saved payloads, not estimated.
    ref = jload(MAN / "batch_sync_reference.json")
    for cid, r in ref.items():
        pin, pout = PRICES[r["served_model"]]
        usd = r["in"] / 1e6 * pin + r["out"] / 1e6 * pout
        total += usd
    rows.append(("batch verification -- synchronous reference", len(ref),
                 sum(ref[c]["in"] / 1e6 * PRICES[ref[c]["served_model"]][0]
                     + ref[c]["out"] / 1e6 * PRICES[ref[c]["served_model"]][1] for c in ref)))

    bv = jload(MAN / "batch_verification.json")["results"]
    bcost = sum(v["in"] / 1e6 * PRICES[v["served_model"]][0] * 0.5
                + v["out"] / 1e6 * PRICES[v["served_model"]][1] * 0.5
                for v in bv.values() if v.get("ok"))
    total += bcost
    rows.append(("batch verification -- batch path (50% rate)",
                 sum(1 for v in bv.values() if v.get("ok")), bcost))

    ctl = jload(MAN / "sync_repeat_control.json")
    pin, pout = PRICES[ctl["model"]]
    # identical prompts to the batch verification, so inputs come from that reference
    ctl_in = {c.split("-", 2)[2]: ref[c]["in"] for c in ref if c.startswith("OP5-")}
    cc, cn = 0.0, 0
    for key, v in ctl["pairs"].items():
        tag, arm = key.split("|")
        t = "".join(ch if (ch.isalnum() or ch in "_-") else "_" for ch in tag)
        ti = ctl_in.get(t, 0)
        for call in ("call1", "call2"):
            cc += ti / 1e6 * pin + v[call][2] / 1e6 * pout
            cn += 1
    total += cc
    rows.append((f"sync-repeat control ({ctl['model']}, D86 attribution)", cn, cc))

    for p in jload(MAN / "lane_pings.json")["pings"]:
        if not p.get("ok"):
            rows.append((f"ping  {p['asked']} (rejected, unbilled)", 0, 0.0))
            continue
        m = p["asked"].split("/")[-1]
        pin, pout = PRICES.get(m, PRICES.get(p["asked"], (3.00, 15.00)))
        usd = p["in"] / 1e6 * pin + p["out"] / 1e6 * pout
        total += usd
        rows.append((f"ping  {p['asked']}", 1, usd))
    return total, rows


def main():
    R = runs()
    print(f"E1-XV PROJECTION -- cell {N_ITEMS} items x {N_ARMS} arms, cap ${CAP:.2f} absolute\n")

    print("MEASURED PER-CALL COST, on real cell prompts (not estimated)")
    print(f"  {'lane':28s} {'model':26s} {'n':>3s} {'in':>6s} {'out':>6s} {'$/call':>9s}")
    base = {}
    for lane, model, tag, batchable in LANES:
        r = R[tag]
        ti, to, usd = per_call(r)
        base[model] = (usd, batchable)
        print(f"  {lane:28s} {model:26s} {r['n_calls']:3d} {ti:6.0f} {to:6.0f} {usd:9.5f}")
    lo = R[K3_LOW]
    lti, lto, lusd = per_call(lo)
    print(f"  {'(K3 at effort=low, for ref)':28s} {'kimi-k3':26s} {lo['n_calls']:3d} "
          f"{lti:6.0f} {lto:6.0f} {lusd:9.5f}")

    k3 = R["K3 default effort, n=6 both arms -- projection basis"]
    print(f"\n  K3 reasoning tokens at DEFAULT effort: min {k3['reasoning_tokens']['min']}, "
          f"mean {k3['reasoning_tokens']['mean']}, max {k3['reasoning_tokens']['max']}"
          f"  ({k3['reasoning_tokens']['mean'] / (k3['tok_out'] / k3['n_calls']) * 100:.0f}% of output)")
    print(f"  K3 reasoning tokens at effort=low   : min {lo['reasoning_tokens']['min']}, "
          f"mean {lo['reasoning_tokens']['mean']}, max {lo['reasoning_tokens']['max']}"
          f"   -- effort IS controllable on this lane")

    print("\nSCENARIOS  (batch = Anthropic Batch API, 50% off both directions, "
          "zero scientific cost)")
    hdr = f"  {'scenario':46s} {'calls/model':>11s} " + " ".join(
        f"{m.split('-2025')[0][:14]:>14s}" for _, m, _, _ in LANES) + f" {'TOTAL':>9s}  verdict"
    print(hdr)

    def row(name, k, batch):
        calls = N_ITEMS * N_ARMS * k
        parts, tot = [], 0.0
        for _, model, _, batchable in LANES:
            usd, _ = base[model]
            c = usd * (0.5 if (batch and batchable) else 1.0) * calls
            parts.append(c); tot += c
        v = "FITS" if tot <= CAP else f"OVER by ${tot - CAP:.2f}"
        print(f"  {name:46s} {calls:11d} " + " ".join(f"{p:14.2f}" for p in parts)
              + f" {tot:9.2f}  {v}")
        return tot

    reg = row("** REGISTERED: k=5 + Anthropic batch **", K, True)
    row("k=5, no batch (reference)", K, False)
    row("k=3 + batch (REJECTED at SP-0: sits at MIN_DRAWS)", 3, True)
    print(f"\n  REGISTERED TOTAL ${reg:.2f} of ${CAP:.2f} cap "
          f"-- headroom ${CAP - reg:.2f} ({(CAP - reg) / CAP * 100:.0f}%)")

    print("\n  Every scenario keeps all three lineages, the same 84 items, both arms,")
    print("  and K3 at its DEFAULT (max) effort. Lowering K3 effort is NOT costed as an")
    print("  option here: XV-5 is a claim ABOUT always-on reasoning, so running that lane")
    print("  at reduced effort would answer a different question.")

    tot, rows = spent()
    print(f"\nSPEND TO DATE -- STEP 0 lane verification")
    for name, n, usd in rows:
        print(f"  {name:64s} {n:3d} calls  ${usd:.5f}")
    print(f"  {'TOTAL BILLED SO FAR':64s} {'':3s}         ${tot:.4f}  "
          f"of ${CAP:.2f} cap ({tot / CAP * 100:.1f}%)")

    out = MAN / "projection.json"
    io.open(out, "w", encoding="utf-8").write(json.dumps({
        "cap_usd": CAP, "n_items": N_ITEMS, "n_arms": N_ARMS,
        "per_call": {m: {"usd": base[m][0]} for _, m, _, _ in LANES},
        "k3_effort_low_usd_per_call": lusd,
        "scenarios": {
            "k5_default": N_ITEMS * N_ARMS * 5 * sum(base[m][0] for _, m, _, _ in LANES),
        },
        "spent_to_date_usd": tot}, indent=2))
    print(f"\n  written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
