"""
e2_api.py -- cached, metered OpenAI calls for E2.

Same device E1 used: E0's client implementation is loaded BY FILE PATH under a
private module name, so there is one request path across all three studies and it
cannot drift, while the cache and ledger land inside E2's write scope. Decoding
parameters come from E1's FROZEN prompts_e1 -- gpt-4.1-mini, temperature 0,
seed 42 -- so E2's gate calls are byte-comparable to E1's.

Path order matters and is the opposite of elicit_e1.py's (D25-E1): E0's tools dir
goes on sys.path FIRST so its own imports resolve, then E2's, so `import e2_api`
can never be shadowed.

Cumulative cap accounting (D27-E1): `spend()` sums over the cache rather than
reading a single process's meter, so a resumed run cannot restart its cap at zero.
"""

from __future__ import annotations

import importlib.util as _ilu
import io
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E2 = PROJECT_ROOT / "e2_metamemory"
_E0_TOOLS = PROJECT_ROOT / "e0_metamemory" / "tools"
_E1_TOOLS = PROJECT_ROOT / "e1_metamemory" / "tools"

for _p in (str(_E0_TOOLS), str(_E1_TOOLS), str(Path(__file__).resolve().parent)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

_spec = _ilu.spec_from_file_location("_e0_api_for_e2", _E0_TOOLS / "api.py")
_e0 = _ilu.module_from_spec(_spec)
sys.modules["_e0_api_for_e2"] = _e0
_spec.loader.exec_module(_e0)

import prompts_e1 as _prompts                                   # noqa: E402

_e0.prompts = _prompts
_e0.CACHE_PATH = E2 / "cache" / "responses.json"
_e0.LEDGER_PATH = E2 / "cache" / "cost_ledger.json"
_e0.CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
_e0._load_cache()                                               # noqa: SLF001

CACHE_PATH, LEDGER_PATH = _e0.CACHE_PATH, _e0.LEDGER_PATH
PRICE_IN, PRICE_OUT = _e0.PRICE_IN, _e0.PRICE_OUT
CapExceeded = _e0.CapExceeded
call, flush, meter, parse_json = _e0.call, _e0.flush, _e0.meter, _e0.parse_json
prompt_hash, cache_key = _e0.prompt_hash, _e0.cache_key

E2_CAP_USD = 25.00
E2_PROJECTION_GATE_USD = 15.00


def call_text(item_id, arm, messages, model=None, max_tokens=None):
    """Free-text completion. Same cache, meter, lock and retry ladder as `call`.

    E0's `call` hard-codes `response_format={"type": "json_object"}`, which is
    right for every judgment arm in E0, E1 and E2's gates -- and wrong for the
    ANSWERER, whose prompt is FR's `GENERATION_SYSTEM_PROMPT` verbatim and
    contains no mention of JSON. Rather than bend FR's frozen prompt to satisfy
    the client, the client gets a text path. It reuses E0's module state
    directly, so cache keys, spend accounting and the cap behave identically and
    cannot drift. Logged as D31-E2.
    """
    import time
    model = model or _prompts.MODEL
    max_tokens = max_tokens or _prompts.MAX_TOKENS
    ph = _e0.prompt_hash(messages)
    key = _e0.cache_key(item_id, arm, model, ph)
    c = _e0._load_cache()                                        # noqa: SLF001
    with _e0._lock:                                              # noqa: SLF001
        if key in c:
            _e0._meter["cached"] += 1                            # noqa: SLF001
            return {**c[key], "cached": True, "key": key}

    last = None
    for attempt in range(4):
        try:
            r = _e0._client().chat.completions.create(            # noqa: SLF001
                model=model, temperature=_prompts.TEMPERATURE,
                seed=_prompts.SEED, max_tokens=max_tokens, messages=messages)
            break
        except Exception as e:                                    # noqa: BLE001
            last = e
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    else:                                                         # pragma: no cover
        raise last

    rec = {"content": r.choices[0].message.content,
           "prompt_tokens": r.usage.prompt_tokens,
           "completion_tokens": r.usage.completion_tokens,
           "model": model, "item_id": item_id, "arm": arm, "prompt_hash": ph}
    with _e0._lock:                                               # noqa: SLF001
        m = _e0._meter                                            # noqa: SLF001
        m["calls"] += 1
        m["in"] += rec["prompt_tokens"]
        m["out"] += rec["completion_tokens"]
        m["usd"] = m["in"] / 1e6 * PRICE_IN + m["out"] / 1e6 * PRICE_OUT
        c[key] = rec
    return {**rec, "cached": False, "key": key}


class CapExceededE2(RuntimeError):
    pass


def spend(prefixes=None):
    """Cumulative E2 spend, summed over the cache. Re-run invariant (D27-E1)."""
    if not CACHE_PATH.exists():
        return 0.0, 0
    tin = tout = n = 0
    for r in json.load(io.open(CACHE_PATH, encoding="utf-8")).values():
        arm = str(r.get("arm", ""))
        if prefixes and not arm.startswith(tuple(prefixes)):
            continue
        tin += r.get("prompt_tokens", 0)
        tout += r.get("completion_tokens", 0)
        n += 1
    return tin / 1e6 * PRICE_IN + tout / 1e6 * PRICE_OUT, n


def check_cap():
    total, n = spend()
    if total > E2_CAP_USD:
        flush()
        raise CapExceededE2(f"${total:.2f} over the ${E2_CAP_USD} E2 cap ({n} calls)")
    return total


def call_text_model(item_id, arm, messages, model, max_tokens=None, temperature=0,
                    seed=42):
    """Free-text completion against an ARBITRARY model, params-tolerant.

    Added for the Amendment 3 bake-off. Reasoning-family models reject
    `temperature`/`seed` and rename `max_tokens` to `max_completion_tokens`; a
    candidate must not be excluded for an API-surface difference. The fallback
    ladder is tried in order and the surviving parameter set is RETURNED with the
    record, so the bake-off table can state which candidates were temperature-0
    comparable to the incumbent and which were not.

    Same cache, lock, meter and retry ladder as `call_text`.
    """
    import time
    max_tokens = max_tokens or _prompts.MAX_TOKENS
    ph = _e0.prompt_hash(messages)
    key = _e0.cache_key(item_id, arm, model, ph)
    c = _e0._load_cache()                                        # noqa: SLF001
    with _e0._lock:                                              # noqa: SLF001
        if key in c:
            _e0._meter["cached"] += 1                            # noqa: SLF001
            return {**c[key], "cached": True, "key": key}

    variants = [
        {"temperature": temperature, "seed": seed, "max_tokens": max_tokens},
        {"temperature": temperature, "max_completion_tokens": max_tokens},
        {"max_completion_tokens": max_tokens},
    ]
    last = None
    for kw in variants:
        for attempt in range(3):
            try:
                r = _e0._client().chat.completions.create(         # noqa: SLF001
                    model=model, messages=messages, **kw)
                rec = {"content": r.choices[0].message.content,
                       "prompt_tokens": r.usage.prompt_tokens,
                       "completion_tokens": r.usage.completion_tokens,
                       "reasoning_tokens": getattr(
                           getattr(r.usage, "completion_tokens_details", None),
                           "reasoning_tokens", 0) or 0,
                       "model": model, "item_id": item_id, "arm": arm,
                       "prompt_hash": ph, "params": sorted(kw)}
                with _e0._lock:                                   # noqa: SLF001
                    m = _e0._meter                                # noqa: SLF001
                    m["calls"] += 1
                    m["in"] += rec["prompt_tokens"]
                    m["out"] += rec["completion_tokens"]
                    c[key] = rec
                return {**rec, "cached": False, "key": key}
            except Exception as e:                                # noqa: BLE001
                last = e
                msg = str(e)
                if "Unsupported" in msg or "unsupported" in msg or \
                        "not supported" in msg or "max_tokens" in msg:
                    break                                         # try next variant
                time.sleep(2 ** attempt)
    raise last
