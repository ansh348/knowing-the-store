"""
economics.py -- E1.8 STEP 1: the economics table, from measured telemetry only.

NO MODEL CALLS. Everything here is read off records the study already wrote.

WHAT IS MEASURED AND WHAT IS NOT
--------------------------------
metered lane (gpt-4.1-mini, OpenAI API)
    input and output tokens are recorded PER CALL by tools/api.py, which stores
    `prompt_tokens` / `completion_tokens` on every cached response. Exact.

    The E1 Phase-C records live in e0_metamemory/cache/responses.json, not E1's:
    elicit_e1.py inserts E0's tools dir onto sys.path AFTER E1's, so E0's dir ends
    up FIRST and `import api` resolves to E0's module. Recorded as D25-E1. The
    records themselves are intact and carry arm + item_id, so the split below is
    exact; only their location is wrong. E1 arms are identified by arm name, and
    the E1 blind arm additionally by item_id == "blind" (E0's blind arm keys on
    the item id, so the two never collide).

subscription lane (gpt-5.6-sol, gpt-5.6-luna, via `codex exec`)
    NO per-call token telemetry was persisted. `--ephemeral` suppresses the
    rollout file, ~/.codex/log is empty, and logs_2.sqlite covers 2026-08-03..05
    only -- before every frontier run. The harness captured stdout but stored only
    the parsed JSON.

    So input tokens here are COUNTED OFFLINE from the frozen prompt texts with
    tiktoken o200k_base -- exact for the prompt, and a LOWER BOUND on what was
    actually sent, because `codex exec` prepends its own system prompt and tool
    schemas. The size of that overhead is anchored by the only two measurements
    that exist: codex's own "tokens used" line on a trivial probe, 3,157 for sol
    and 11,712 for luna. Those are TURN TOTALS (harness prompt + user prompt +
    reasoning + output), n=1 each, and are used only as an anchor, never as a
    reasoning-token figure.

latency
    Not instrumented per call anywhere. Run wall-clock is taken from the session
    transcript's tool-use / completion timestamps (ids recorded in WALL below) and
    divided into a mean per-call latency using the run's worker count. This is
    harness throughput, not server latency: it includes process start, retry
    backoff and file I/O.

Usage:  python e1_metamemory/tools/economics.py
"""

from __future__ import annotations

import collections
import io
import json
import statistics as st
import sys
from pathlib import Path

import tiktoken

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
E0 = PROJECT_ROOT / "e0_metamemory"
OUT = E1 / "results" / "economics.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prompts_e1 as P  # noqa: E402

ENC = tiktoken.get_encoding("o200k_base")

# --------------------------------------------------------------------------- #
# PRICES. Author-supplied in the E1.8 instruction, date-stamped 2026-08-11.
# --------------------------------------------------------------------------- #
PRICE_DATE = "2026-08-11"
PRICE_SOURCE = "https://platform.openai.com/docs/pricing"
PRICES = {                                   # USD per 1M tokens (input, output)
    "gpt-4.1-mini": (0.40, 1.60),            # study's own constant, e0 api.py:31
    "gpt-5.6-luna": (0.20, 1.20),
    "gpt-5.6-sol": (5.00, 30.00),
}
CACHED_INPUT_DISCOUNT = 0.10                 # cached input billed at 10% of list
MIN_CACHEABLE_PREFIX_TOKENS = 1024           # OpenAI's minimum cacheable prefix

# --------------------------------------------------------------------------- #
# WALL CLOCK. Session-transcript timestamps; tool-use ids given so each row can
# be re-derived from the transcript. Seconds.
# --------------------------------------------------------------------------- #
WALL = {
    "mini / E1 Phase C (main + k3 + staircase)": {
        "tool_use_id": "toolu_01QzWX58FkDTYs2icExDbPV5",
        "start": "2026-08-10T14:11:30.154Z", "end": "2026-08-10T14:43:19.250Z",
        "seconds": 1909.1, "workers": 12, "calls": 2997, "model": "gpt-4.1-mini",
        "arms": "BLIND + INDEXED-TRUE + INDEXED-BELIEVED + BLIND-K + STAIRCASE"},
    "sol / E1.6 frontier redraw": {
        "tool_use_id": "toolu_01KT7qBPnkKBUKw61mfiZY6p",
        "start": "2026-08-10T17:42:49.842Z", "end": "2026-08-10T18:27:31.109Z",
        "seconds": 2681.3, "workers": 5, "calls": 1500, "model": "gpt-5.6-sol",
        "arms": "BLIND + INDEXED-TRUE, k=5"},
    "luna / E1.7 capability ladder": {
        "tool_use_id": "toolu_01QoNvUYZe8iMbWEgU9AT8EP",
        "start": "2026-08-10T18:43:34.229Z", "end": "2026-08-10T19:26:46.360Z",
        "seconds": 2592.1, "workers": 5, "calls": 1500, "model": "gpt-5.6-luna",
        "arms": "BLIND + INDEXED-TRUE, k=5"},
}

# codex's own "tokens used" line, trivial probe, n=1 per model. Turn TOTALS.
CODEX_PROBE_TURN_TOTAL = {"gpt-5.6-sol": 3157, "gpt-5.6-luna": 11712}
CODEX_PROBE_PROMPT = {           # the probe's own user text, so overhead = total - this
    "gpt-5.6-sol": 'Reply with only this JSON and nothing else: {"fok":42}',
    "gpt-5.6-luna": 'Reply with only this JSON and nothing else: {"fok":42}',
}


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True, default=float)
        f.write("\n")


def ntok(s):
    return len(ENC.encode(s))


def stats(v):
    v = sorted(v)
    return {"n": len(v), "mean": (sum(v) / len(v)) if v else None,
            "median": st.median(v) if v else None,
            "min": v[0] if v else None, "max": v[-1] if v else None}


def usd(tin, tout, model):
    pi, po = PRICES[model]
    return tin / 1e6 * pi + tout / 1e6 * po


# ------------------------------------------------------------------ metered lane
def metered_rows():
    """Per-arm token telemetry for the mini lane, straight off the caches."""
    recs = []
    for tag, path in (("e0-cache", E0 / "cache" / "responses.json"),
                      ("e1-cache", E1 / "cache" / "responses.json")):
        for r in jload(path).values():
            recs.append({**r, "_cache": tag})

    def is_e1(r):
        a = r.get("arm") or ""
        if a in ("INDEXED-TRUE", "INDEXED-BELIEVED", "BLIND-K", "STAIRCASE",
                 "INDEXED-TRUE-NOMARKER"):
            return True
        # `draft` is the natural-absent PROBE drafting arm, which is E1's: probes
        # were an E1 addition (PROBE_SYSTEM lives in prompts_e1), and there are
        # exactly 40 records -- one per E1 persona. E0 ran 20 personas and had no
        # drafting step. Originally filed under E0 here; corrected.
        if a == "draft":
            return True
        if a.startswith(("A1-", "A2-", "A3-")):      # E1.8 mechanism arms
            return True
        if a == "BLIND":
            return r.get("item_id") == "blind"     # E1 keys blind on the constant
        return a.startswith("leakage_L0:")         # E1's ladder; E0's is bare
    lanes = collections.defaultdict(list)
    for r in recs:
        if r.get("prompt_tokens") is None:
            continue
        a = r.get("arm") or "?"
        if is_e1(r):
            lane = ("E1", "leakage_L0" if a.startswith("leakage_L0:") else a)
        else:
            lane = ("E0", a)
        lanes[lane].append(r)

    out = {}
    for (study, arm), rs in sorted(lanes.items()):
        tin = [r["prompt_tokens"] for r in rs]
        tout = [r["completion_tokens"] for r in rs]
        model = rs[0].get("model", "gpt-4.1-mini")
        tot_in, tot_out = sum(tin), sum(tout)
        out[f"{study}:{arm}"] = {
            "study": study, "arm": arm, "model": model, "calls": len(rs),
            "input_tokens": stats(tin), "output_tokens": stats(tout),
            "total_input": tot_in, "total_output": tot_out,
            "usd_total": usd(tot_in, tot_out, model),
            "usd_per_call": usd(tot_in, tot_out, model) / len(rs),
            "usd_per_1M_calls": usd(tot_in, tot_out, model) / len(rs) * 1e6,
            "source": "measured: usage recorded per call by tools/api.py",
        }
    return out


# ---------------------------------------------------- tokenizer cross-validation
def tokenizer_check(n=200):
    """Compare tiktoken over the reconstructed prompt against the recorded usage.

    The gap is the chat-template overhead the API adds per message; measuring it
    is what licenses using tiktoken on the frontier lane, where nothing recorded
    a token count. Uses the leakage_L0 arm because its (index, question) pair is
    exactly reconstructible from committed artifacts.
    """
    idx = jload(E1 / "indexes_v2.json")["indexes"]
    lad = jload(E1 / "ladder_L0.json")
    cells = lad["cells"] if isinstance(lad.get("cells"), list) else []
    cache = jload(E1 / "cache" / "responses.json")
    by_key = {}
    for r in cache.values():
        if str(r.get("arm", "")).startswith("leakage_L0:"):
            by_key[(r["item_id"], r["arm"])] = r
    deltas = []
    for c in cells[:n] if cells else []:
        k = c.get("index_key")
        if k not in idx:
            continue
        msgs = P.LEAKAGE_SYSTEM + "\n" + P.LEAKAGE_USER.format(
            index=idx[k], question=c.get("question", ""))
        rec = None
        for (iid, arm), r in by_key.items():
            if iid == c.get("item_id"):
                rec = r
                break
        if rec:
            deltas.append(rec["prompt_tokens"] - ntok(msgs))
    return {"n": len(deltas), "delta_stats": stats(deltas) if deltas else None,
            "note": "recorded prompt_tokens minus tiktoken(o200k_base) over the "
                    "reconstructed text; the residue is the chat-template overhead"}


def tokenizer_check_direct():
    """Direct check on the E1 Run-B arm: prompt is reconstructible per item."""
    idx = jload(E1 / "indexes_v2.json")["indexes"]
    items = {i["item_id"]: i for i in jload(E1 / "build" / "items_final.json")}
    rows = jload(E1 / "run_b_nomarker.json")["rows"]
    main = {r["tag"]: r["question"] for r in jload(E1 / "elicitation_main.json")
            if r["arm"] != "BLIND"}
    cache = {(r["item_id"], r["arm"]): r for r in
             jload(E1 / "cache" / "responses.json").values()}
    deltas = []
    for r in rows:
        tag = r["item_id"]
        rec = cache.get((tag, "INDEXED-TRUE-NOMARKER"))
        it, q = items.get(tag), main.get(tag)
        if not (rec and it and q):
            continue
        b, p, v = it["backend"], it["persona"], it["variant"]
        k = (f"{b}:{p}:SLOT:{it['question_id']}:TRUE" if v == "SLOT-ABLATED"
             else f"{b}:{p}:{v}:TRUE")
        if k not in idx:
            continue
        deltas.append(rec["prompt_tokens"]
                      - ntok(P.SYSTEM) - ntok(P.USER_INDEXED_NOMARKER.format(
                          index=idx[k], question=q)))
    return {"n": len(deltas), "delta_stats": stats(deltas) if deltas else None,
            "arm": "E1:INDEXED-TRUE-NOMARKER (Run B)",
            "note": "recorded prompt_tokens minus tiktoken over system+user text; "
                    "residue is the per-message chat-template overhead"}


# ----------------------------------------------------------- subscription lane
def frontier_prompt_tokens():
    """Exact token counts over the frozen prompt TEXT for every frontier call."""
    idx = jload(E1 / "indexes_v2.json")["indexes"]
    items = {i["item_id"]: i for i in jload(E1 / "build" / "items_final.json")}
    subset = jload(E1 / "strong_model.json")["rows"]

    def ikey(it):
        b, p, v = it["backend"], it["persona"], it["variant"]
        return (f"{b}:{p}:SLOT:{it['question_id']}:TRUE" if v == "SLOT-ABLATED"
                else f"{b}:{p}:{v}:TRUE")

    blind, indexed, prefixes = [], [], collections.defaultdict(list)
    for r in subset:
        q = r["question"]
        blind.append(ntok(P.SYSTEM + "\n\n" + P.USER_BLIND.format(question=q)))
        k = ikey(items[r["item_id"]])
        if k in idx:
            full = P.SYSTEM + "\n\n" + P.USER_INDEXED.format(index=idx[k], question=q)
            pre = P.SYSTEM + "\n\n" + P.USER_INDEXED.split("{question}")[0].format(
                index=idx[k])
            indexed.append(ntok(full))
            prefixes[k].append((ntok(pre), ntok(full)))
    return {"blind": stats(blind), "indexed": stats(indexed),
            "n_indexed_items": len(indexed), "n_blind_items": len(blind),
            "_prefixes": {k: v for k, v in prefixes.items()}}


def frontier_runs(fp):
    """Metered-equivalent cost of the subscription-billed runs. COMPUTED, NOT PAID."""
    b, i = fp["blind"]["mean"], fp["indexed"]["mean"]
    runs = {
        "E1 strong-model check (sol, blind, k=1)": ("gpt-5.6-sol", 150, b, 0),
        "E1.5 Run A (sol, indexed-TRUE, k=1)": ("gpt-5.6-sol", 150, 0, i),
        "E1.6 frontier redraw (sol, both arms, k=5)": ("gpt-5.6-sol", 1500, b, i),
        "E1.7 capability ladder (luna, both arms, k=5)": ("gpt-5.6-luna", 1500, b, i),
    }
    out = {}
    for name, (model, calls, mb, mi) in runs.items():
        if mb and mi:                       # half blind, half indexed
            tin = calls / 2 * mb + calls / 2 * mi
        else:
            tin = calls * (mb or mi)
        overhead = (CODEX_PROBE_TURN_TOTAL[model]
                    - ntok(CODEX_PROBE_PROMPT[model])) * calls
        lo = usd(tin, 0, model)                       # prompt text only, no output
        mid = usd(tin + overhead, 0, model)           # overhead priced as input
        hi = usd(tin, overhead, model)                # overhead priced as output
        out[name] = {"model": model, "calls": calls,
                     "prompt_text_tokens": tin,
                     "codex_overhead_tokens_anchored": overhead,
                     "usd_lower_bound_prompt_text_only": lo,
                     "usd_mid_overhead_as_input": mid,
                     "usd_upper_overhead_as_output": hi,
                     "label": "computed-not-paid; subscription lane, $0 billed"}
    out["_total"] = {
        "usd_lower_bound": sum(v["usd_lower_bound_prompt_text_only"]
                               for v in out.values() if isinstance(v, dict) and "model" in v),
        "usd_mid": sum(v["usd_mid_overhead_as_input"]
                       for v in out.values() if isinstance(v, dict) and "model" in v),
        "usd_upper": sum(v["usd_upper_overhead_as_output"]
                         for v in out.values() if isinstance(v, dict) and "model" in v),
        "actually_paid_usd": 0.0}
    return out


# ------------------------------------------------------- cache-adjusted indexed
def full_indexed_prefixes():
    """(prefix_tokens, full_tokens) per call for the WHOLE E1 indexed-TRUE arm."""
    idx = jload(E1 / "indexes_v2.json")["indexes"]
    items = {i["item_id"]: i for i in jload(E1 / "build" / "items_final.json")}
    main = [r for r in jload(E1 / "elicitation_main.json")
            if r["arm"] == "INDEXED-TRUE" and r["status"] == "OK"]
    groups = collections.defaultdict(list)
    for r in main:
        it = items.get(r["tag"])
        if not it:
            continue
        b, p, v = it["backend"], it["persona"], it["variant"]
        k = (f"{b}:{p}:SLOT:{it['question_id']}:TRUE" if v == "SLOT-ABLATED"
             else f"{b}:{p}:{v}:TRUE")
        if k not in idx:
            continue
        q = r["question"]
        full = ntok(P.SYSTEM + "\n\n" + P.USER_INDEXED.format(index=idx[k], question=q))
        pre = ntok(P.SYSTEM + "\n\n"
                   + P.USER_INDEXED.split("{question}")[0].format(index=idx[k]))
        groups[k].append((pre, full))
    return groups


def cache_adjusted(groups, label):
    """List-price arithmetic for a cached byte-stable index prefix. NOT BILLED.

    The frozen USER_INDEXED puts the index BEFORE the question, so every item
    sharing an index key shares a byte-identical prefix: system text + index
    block + "Question: ". Only the question varies. Under prefix caching the
    first call in a group pays list; the rest pay CACHED_INPUT_DISCOUNT on the
    prefix and list on the remainder.

    Two columns are reported. AS-RUN uses the group sizes this study actually
    had, which are small (an index is re-used only across the questions asked of
    that one persona-variant). ASYMPTOTIC is the n -> infinity limit within a
    group -- every call after the first pays the discount -- which is the
    deployment-relevant figure: in service, one user's index prefix is reused
    across every gate call that user ever makes.
    """
    out = {}
    for model in ("gpt-4.1-mini", "gpt-5.6-luna", "gpt-5.6-sol"):
        full_in = cached_in = uncached_in = 0
        asym_cached = asym_uncached = 0
        ngroups = qualifying = 0
        sizes = []
        for _k, calls in groups.items():
            ngroups += 1
            sizes.append(len(calls))
            pre = calls[0][0]
            ok = pre >= MIN_CACHEABLE_PREFIX_TOKENS
            qualifying += 1 if ok else 0
            for n, (p, full) in enumerate(calls):
                full_in += full
                if ok and n > 0:
                    cached_in += p
                    uncached_in += full - p
                else:
                    uncached_in += full
                if ok:
                    asym_cached += p
                    asym_uncached += full - p
                else:
                    asym_uncached += full
        pi = PRICES[model][0]
        listed = full_in / 1e6 * pi
        adj = uncached_in / 1e6 * pi + cached_in / 1e6 * pi * CACHED_INPUT_DISCOUNT
        asym = asym_uncached / 1e6 * pi + asym_cached / 1e6 * pi * CACHED_INPUT_DISCOUNT
        out[model] = {
            "scope": label,
            "groups": ngroups, "groups_meeting_min_prefix": qualifying,
            "mean_calls_per_group": (sum(sizes) / ngroups) if ngroups else None,
            "max_calls_per_group": max(sizes) if sizes else None,
            "calls": sum(sizes),
            "input_tokens_list": full_in,
            "input_tokens_cached": cached_in, "input_tokens_uncached": uncached_in,
            "usd_input_list": listed,
            "usd_input_cache_adjusted_as_run": adj,
            "usd_input_cache_adjusted_asymptotic": asym,
            "saving_pct_as_run": 100 * (1 - adj / max(listed, 1e-12)),
            "saving_pct_asymptotic": 100 * (1 - asym / max(listed, 1e-12)),
        }
    return out


def main():
    fp = frontier_prompt_tokens()
    res = {
        "no_api_calls": True,
        "prices_usd_per_1m_tokens": PRICES,
        "price_date": PRICE_DATE,
        "price_source_url": PRICE_SOURCE,
        "price_provenance": (
            "luna and sol list prices are as supplied by the study author in the "
            "E1.8 instruction, date-stamped 2026-08-11 (post-2026-07-30 cut); they "
            "were NOT independently re-fetched from the URL. gpt-4.1-mini's pair is "
            "the study's own constant (e0_metamemory/tools/api.py:31), the same "
            "constant that priced every metered call actually made."),
        "metered_lane": metered_rows(),
        "metered_ledger_totals": {
            "e1_phase_c_meter": jload(E0 / "cache" / "cost_ledger.json"),
            "e1_cache_meter": jload(E1 / "cache" / "cost_ledger.json"),
            "note": "the Phase-C meter sits in E0's ledger file; see D25-E1"},
        "tokenizer_crossvalidation": tokenizer_check_direct(),
        "frontier_prompt_tokens": {k: v for k, v in fp.items() if not k.startswith("_")},
        "frontier_runs_metered_equivalent": frontier_runs(fp),
        "cache_adjusted_indexed_arm": cache_adjusted(
            full_indexed_prefixes(), "full E1 INDEXED-TRUE arm (mini lane items)"),
        "cache_adjusted_frontier_subset": cache_adjusted(
            fp["_prefixes"], "150-item frontier subset"),
        "wall_clock": {k: {**v, "seconds_per_call_mean":
                           v["seconds"] * v["workers"] / v["calls"]}
                       for k, v in WALL.items()},
        "wall_clock_caveat": (
            "harness throughput, not server latency: wall-clock x workers / calls, "
            "including process start, retry backoff and file I/O. No per-call timing "
            "was instrumented in any E1 run."),
    }
    jdump(res, OUT)

    print("=" * 96)
    print("METERED LANE (gpt-4.1-mini) -- measured per call")
    print("=" * 96)
    print(f"{'lane':38s}{'calls':>7s}{'in/mean':>9s}{'in/med':>8s}"
          f"{'out/mean':>9s}{'out/med':>8s}{'$/call':>10s}{'$/1M':>12s}")
    for k, v in res["metered_lane"].items():
        print(f"{k:38s}{v['calls']:7d}{v['input_tokens']['mean']:9.0f}"
              f"{v['input_tokens']['median']:8.0f}{v['output_tokens']['mean']:9.1f}"
              f"{v['output_tokens']['median']:8.0f}{v['usd_per_call']:10.6f}"
              f"{v['usd_per_1M_calls']:12,.0f}")

    print("\n" + "=" * 96)
    print("TOKENIZER CROSS-VALIDATION (licenses tiktoken on the frontier lane)")
    print("=" * 96)
    t = res["tokenizer_crossvalidation"]
    print(f"  {t['arm']}: n={t['n']}  delta {t['delta_stats']}")

    print("\n" + "=" * 96)
    print("FRONTIER PROMPT TEXT TOKENS (tiktoken o200k_base; lower bound on sent)")
    print("=" * 96)
    for k in ("blind", "indexed"):
        s = res["frontier_prompt_tokens"][k]
        print(f"  {k:9s} n={s['n']:4d}  mean {s['mean']:8.0f}  median {s['median']:8.0f}"
              f"  min {s['min']:6d}  max {s['max']:6d}")

    print("\n" + "=" * 96)
    print("WALL CLOCK")
    print("=" * 96)
    for k, v in res["wall_clock"].items():
        print(f"  {k:42s} {v['seconds']:8.0f}s / {v['calls']:5d} calls / "
              f"{v['workers']:2d} workers = {v['seconds_per_call_mean']:6.2f} s/call")

    print("\n" + "=" * 96)
    print("METERED-EQUIVALENT OF THE SUBSCRIPTION RUNS (computed-not-paid)")
    print("=" * 96)
    for k, v in res["frontier_runs_metered_equivalent"].items():
        if k == "_total":
            continue
        print(f"  {k:46s} ${v['usd_lower_bound_prompt_text_only']:8.2f} .. "
              f"${v['usd_upper_overhead_as_output']:8.2f}")
    t = res["frontier_runs_metered_equivalent"]["_total"]
    print(f"  {'TOTAL':46s} ${t['usd_lower_bound']:8.2f} .. ${t['usd_upper']:8.2f}"
          f"   (actually paid ${t['actually_paid_usd']:.2f})")

    print("\n" + "=" * 96)
    print("CACHE-ADJUSTED INDEXED ARM (list-price arithmetic, NOT billed)")
    print("=" * 96)
    for key in ("cache_adjusted_indexed_arm", "cache_adjusted_frontier_subset"):
        v0 = next(iter(res[key].values()))
        print(f"  -- {v0['scope']}: {v0['calls']} calls over {v0['groups']} index "
              f"prefixes ({v0['groups_meeting_min_prefix']} >= "
              f"{MIN_CACHEABLE_PREFIX_TOKENS} tok), mean "
              f"{v0['mean_calls_per_group']:.2f} calls/prefix, max "
              f"{v0['max_calls_per_group']}")
        for m, v in res[key].items():
            print(f"     {m:14s} list ${v['usd_input_list']:8.4f} -> as-run "
                  f"${v['usd_input_cache_adjusted_as_run']:8.4f} "
                  f"({v['saving_pct_as_run']:5.1f}%) -> asymptotic "
                  f"${v['usd_input_cache_adjusted_asymptotic']:8.4f} "
                  f"({v['saving_pct_asymptotic']:5.1f}%)")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
