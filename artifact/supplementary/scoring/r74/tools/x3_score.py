"""R74 X3 aggregator (ADDENDUM_R74 SX3 @ 35f8416a55). Telemetry only.

Emits the as-billed per-million-call figures for Table 2 and the ordering verdict:
the billed sentence replaces the projection sentence ONLY if billed indexed-cached <
billed blind (registered replacement, S2 exemption); otherwise both print.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
X3 = ROOT / "r74" / "x3"
rows = [json.loads(l) for l in open(X3 / "telemetry.jsonl", encoding="utf-8")]
out = {"registration": "ADDENDUM_R74 SX3 @ 35f8416a55",
       "prices_pinned": {"input": 0.40, "cached_input": 0.10, "output": 1.60,
                         "source": "developers.openai.com/api/docs/pricing, 2026-08-24"}}
for kind in ("INDEXED", "BLIND"):
    rs = [r for r in rows if r["kind"] == kind]
    n = len(rs)
    tp = sum(r["prompt_tokens"] for r in rs)
    tc = sum(r["cached_tokens"] for r in rs)
    to = sum(r["completion_tokens"] for r in rs)
    usd = sum(r["usd_billed"] for r in rs)
    out[kind] = {"calls": n,
                 "mean_prompt_tokens": tp / n, "mean_cached_tokens": tc / n,
                 "mean_completion_tokens": to / n,
                 "cache_hit_token_share": tc / tp if tp else 0.0,
                 "usd_billed_total": usd,
                 "usd_billed_per_call": usd / n,
                 "usd_billed_per_1M_calls": usd / n * 1e6}
i, b = out["INDEXED"]["usd_billed_per_1M_calls"], out["BLIND"]["usd_billed_per_1M_calls"]
out["ordering_confirmed_indexed_lt_blind"] = bool(i < b)
json.dump(out, open(X3 / "x3_billed.json", "w", encoding="utf-8"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1))
