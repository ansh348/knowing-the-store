"""billing_table.py -- R85. Emits the billing-path table. NO API CALLS.

Every cost below is derived from a measured per-call or per-episode figure held in a
committed artifact, never from a list price applied to a guessed token count:

  ingestion        r85_graphiti/ingest_runs/stock_gpt-4.1-mini-*.json  (this program)
  monitor lanes    r82_counterfactual/rows/rows_{MINI,H45,OP5}.jsonl   (R82, measured)

The R82 rows carry tok_in, tok_out and usd per call, and their usd already includes the
Message Batches 50% discount on the Anthropic lanes. Reconciliation against list price
(Haiku 4.5 $1/$5, Opus 5 $5/$25 per MTok) is asserted below, so a silent price change
breaks this script rather than the registration.

Usage:  python r85_graphiti/tools/billing_table.py
"""

from __future__ import annotations

import collections
import glob
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R85 = ROOT / "r85_graphiti"

# Populations. n=307 (FOK hard tier) is a SUBSET of n=661 (NOK), and both judgments are
# scored from the same elicitation, so a lane costs 661 calls per provenance, not 968.
N_ITEMS = 661
PROVENANCES = ("BELIEVED", "TRUE-projected")
K_HAIKU = 5
EPISODES_40 = 1365
INGEST_MARGIN = 1.3   # the addendum's worst-case margin on ingestion

LIST = {"claude-haiku-4-5": (1.00, 5.00), "claude-opus-5": (5.00, 25.00)}
BATCH_MULT = 0.5


def measured_ingest():
    tot_usd = tot_ep = tot_embed = 0
    for f in glob.glob(str(R85 / "ingest_runs" / "stock_gpt-4.1-mini*.json")):
        d = json.loads(Path(f).read_text("utf-8"))
        tot_usd += d["usd"]; tot_ep += d["episodes"]; tot_embed += d["embed_tokens"]
    embed_usd = tot_embed * 0.02 / 1e6
    return (tot_usd - embed_usd) / tot_ep, tot_embed / tot_ep, tot_ep


def measured_lane(fname, arm="INDEXED-V2"):
    ins, outs, usd = [], [], []
    for line in (ROOT / "r82_counterfactual" / "rows" / fname).read_text("utf-8").splitlines():
        r = json.loads(line)
        if r["arm"] != arm:
            continue
        ins.append(r["tok_in"]); outs.append(r["tok_out"]); usd.append(r.get("usd") or 0)
    return statistics.mean(ins), statistics.mean(outs), statistics.mean(usd)


def reconcile(model, mean_in, mean_out, mean_usd):
    pin, pout = LIST[model]
    expect = (mean_in * pin + mean_out * pout) / 1e6 * BATCH_MULT
    assert abs(expect - mean_usd) / mean_usd < 0.01, (
        f"{model}: measured ${mean_usd:.6f}/call does not reconcile against list "
        f"{pin}/{pout} with batch {BATCH_MULT} (expected ${expect:.6f})")
    return expect


def main():
    ing_per_ep, embed_per_ep, n_ep = measured_ingest()
    mini = measured_lane("rows_MINI.jsonl")
    haiku = measured_lane("rows_H45.jsonl")
    opus = measured_lane("rows_OP5.jsonl")
    reconcile("claude-haiku-4-5", *haiku)
    reconcile("claude-opus-5", *opus)

    ingest_usd = ing_per_ep * EPISODES_40
    embed_usd = embed_per_ep * EPISODES_40 * 0.02 / 1e6
    mini_per_prov = N_ITEMS * mini[2]
    haiku_per_prov = N_ITEMS * K_HAIKU * haiku[2]
    opus_both = N_ITEMS * K_HAIKU * len(PROVENANCES) * opus[2]

    rows = [
        ("Graphiti ingestion, extractor", "OpenAI", "gpt-4.1-mini-2025-04-14",
         "metered API key", "OPENAI_API_KEY", ingest_usd, "$28 ingestion stop"),
        ("Graphiti ingestion, embedder", "OpenAI", "text-embedding-3-small",
         "metered API key", "OPENAI_API_KEY", embed_usd, "$28 ingestion stop"),
        ("Monitor, mini, BELIEVED", "OpenAI", "gpt-4.1-mini-2025-04-14",
         "metered API key", "OPENAI_API_KEY", mini_per_prov, "$15 monitors"),
        ("Monitor, mini, TRUE-projected", "OpenAI", "gpt-4.1-mini-2025-04-14",
         "metered API key", "OPENAI_API_KEY", mini_per_prov, "$15 monitors"),
        ("Monitor, Haiku 4.5 k=5, BELIEVED", "Anthropic", "claude-haiku-4-5-20251001",
         "Batch API, metered", "ANTHROPIC_API_KEY", haiku_per_prov, "$15 monitors"),
        ("Monitor, Haiku 4.5 k=5, TRUE-projected", "Anthropic", "claude-haiku-4-5-20251001",
         "Batch API, metered", "ANTHROPIC_API_KEY", haiku_per_prov,
         "$15 monitors, conditional"),
        ("Reader NB-5, whole-map embedding", "local", "all-MiniLM-L6-v2",
         "local, offline", "none", 0.0, "none"),
        ("Reader NB-6, superseded-names", "local", "all-MiniLM-L6-v2",
         "local, offline", "none", 0.0, "none"),
        ("Monitor, Opus 5 k=5, both provenances", "Anthropic", "claude-opus-5",
         "Batch API, metered", "ANTHROPIC_API_KEY", opus_both, "DROPPED, cannot fit $45"),
    ]

    print("measured inputs")
    print(f"  ingestion      ${ing_per_ep:.5f}/episode LLM + {embed_per_ep:.0f} embed tok/episode "
          f"over {n_ep} episodes")
    print(f"  mini indexed   {mini[0]:.0f} in / {mini[1]:.0f} out = ${mini[2]:.6f}/call")
    print(f"  haiku indexed  {haiku[0]:.0f} in / {haiku[1]:.0f} out = ${haiku[2]:.6f}/call (batch)")
    print(f"  opus5 indexed  {opus[0]:.0f} in / {opus[1]:.0f} out = ${opus[2]:.6f}/call (batch)")
    print("  list-price reconciliation: PASS for both Anthropic lanes\n")

    w = "| {:<38} | {:<9} | {:<26} | {:<18} | {:<17} | {:>7} | {} |"
    print(w.format("Arm", "Provider", "Exact model identifier", "Billing path",
                   "Key name in .env", "USD", "Ceiling"))
    print(w.format("-" * 38, "-" * 9, "-" * 26, "-" * 18, "-" * 17, "-" * 7, "-" * 26))
    for name, prov, model, path, key, usd, ceil in rows:
        print(w.format(name, prov, model, path, key, f"{usd:.2f}", ceil))

    oa_exp = ingest_usd + embed_usd + 2 * mini_per_prov
    oa_worst = (ingest_usd + embed_usd) * INGEST_MARGIN + 2 * mini_per_prov
    an_exp = haiku_per_prov
    an_worst = 2 * haiku_per_prov
    print(f"\nOpenAI key OPENAI_API_KEY       expected ${oa_exp:.2f}   worst case ${oa_worst:.2f}"
          f"   (worst applies the {INGEST_MARGIN}x ingestion margin)")
    print(f"Anthropic account ANTHROPIC_API_KEY expected ${an_exp:.2f}   worst case ${an_worst:.2f}"
          f"   (worst adds the conditional TRUE-projected lane)")
    print(f"BOTH                            expected ${oa_exp + an_exp:.2f}   "
          f"worst case ${oa_worst + an_worst:.2f}   against the $45 total")
    print(f"\nOpus 5 at the registered k=5 over both provenances would add ${opus_both:.2f}, "
          f"which does not fit $45 under any partition.")


def cf2():
    """CF-2's billing table.

    SHAPE ASSUMED FROM THE R82-CF CELL, and the assumption is stated because
    R81_R82_AFTER_62D_PROMPT.md is not in this repository: no file of that name exists
    under reviews/, registrations/ or the root. The call counts below are R82-CF's own
    (30 pairs x 3 store versions, k=1 on mini and k=5 on the two Anthropic lanes) and the
    ceiling is the $15 that Amendment 4 set at ADDENDUM_R82.md sections 10 and 24. If CF-2
    differs in shape, only the call counts change; the per-call costs are measured and hold.
    """
    counts = {"mini": (30, 90, 90), "haiku": (150, 450, 450), "opus5": (150, 450, 450)}
    lanes = []
    for fname, lane, model, provider, path, key in (
            ("rows_MINI.jsonl", "mini", "gpt-4.1-mini-2025-04-14", "OpenAI",
             "metered API key", "OPENAI_API_KEY"),
            ("rows_H45.jsonl", "haiku", "claude-haiku-4-5-20251001", "Anthropic",
             "Batch API, metered", "ANTHROPIC_API_KEY"),
            ("rows_OP5.jsonl", "opus5", "claude-opus-5", "Anthropic",
             "Batch API, metered", "ANTHROPIC_API_KEY")):
        tot = 0.0
        for arm, n in zip(("BLIND", "INDEXED-V2", "INDEXED-V3"), counts[lane]):
            tot += n * measured_lane(fname, arm)[2]
        lanes.append((lane, provider, model, path, key, tot))

    print("\n\n=== CF-2 billing table (shape assumed from R82-CF; see docstring) ===\n")
    w = "| {:<26} | {:<9} | {:<26} | {:<18} | {:<17} | {:>7} | {} |"
    print(w.format("Lane", "Provider", "Exact model identifier", "Billing path",
                   "Key name in .env", "USD", "Ceiling"))
    print(w.format("-" * 26, "-" * 9, "-" * 26, "-" * 18, "-" * 17, "-" * 7, "-" * 18))
    budget = {"mini": "$1 of $15", "haiku": "$2 of $15", "opus5": "$11 of $15"}
    for lane, provider, model, path, key, tot in lanes:
        print(w.format(lane + " (k=1)" if lane == "mini" else lane + " (k=5)",
                       provider, model, path, key, f"{tot:.2f}", budget[lane]))
    oa = sum(t for l, p, m, pa, k, t in lanes if p == "OpenAI")
    an = sum(t for l, p, m, pa, k, t in lanes if p == "Anthropic")
    print(f"\nOpenAI key OPENAI_API_KEY         expected ${oa:.2f}   worst case ${oa * 1.3:.2f}")
    print(f"Anthropic account ANTHROPIC_API_KEY expected ${an:.2f}   worst case ${an * 1.3:.2f}")
    print(f"BOTH                              expected ${oa + an:.2f}   "
          f"worst case ${(oa + an) * 1.3:.2f}   against the $15 ceiling")
    if (oa + an) * 1.3 > 15:
        print("  WORST CASE EXCEEDS THE $15 CEILING -- the margin must be ruled on before freeze.")


if __name__ == "__main__":
    import sys
    main()
    if "--cf2" in sys.argv:
        cf2()
