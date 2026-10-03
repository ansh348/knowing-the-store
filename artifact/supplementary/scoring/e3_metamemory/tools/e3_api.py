"""
e3_api.py -- cached, metered OpenAI calls for E3, in E3's OWN write scope.

Same device E1 and E2 used: E0's client implementation is loaded BY FILE PATH
under a private module name, so there is one request path across all four studies
and it cannot drift, while the cache and ledger land inside E3's write scope.
Decoding parameters come from E1's FROZEN prompts_e1 -- gpt-4.1-mini,
temperature 0, seed 42 -- so E3's gate calls are byte-comparable to E1's and E2's.

WHY THIS FILE EXISTS RATHER THAN REUSING e2_api (D55-E3). e2_api points the cache
at `e2_metamemory/cache/responses.json` and caps at E2's $25. Importing it from an
E3 tool writes E3 rows into a committed E2 artifact -- a scope-fence violation --
and makes E3's spend unseparable from E2's, so E3's own $40 cap and $15 projection
gate could not be read at all. E3 gets its own cache, its own ledger and its own
cap; nothing else changes.

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
E3 = PROJECT_ROOT / "e3_metamemory"
_E0_TOOLS = PROJECT_ROOT / "e0_metamemory" / "tools"
_E1_TOOLS = PROJECT_ROOT / "e1_metamemory" / "tools"

for _p in (str(_E0_TOOLS), str(_E1_TOOLS), str(Path(__file__).resolve().parent)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

_spec = _ilu.spec_from_file_location("_e0_api_for_e3", _E0_TOOLS / "api.py")
_e0 = _ilu.module_from_spec(_spec)
sys.modules["_e0_api_for_e3"] = _e0
_spec.loader.exec_module(_e0)

import prompts_e1 as _prompts                                   # noqa: E402

_e0.prompts = _prompts
_e0.CACHE_PATH = E3 / "cache" / "responses.json"
_e0.LEDGER_PATH = E3 / "cache" / "cost_ledger.json"
_e0.CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
_e0._load_cache()                                               # noqa: SLF001

CACHE_PATH, LEDGER_PATH = _e0.CACHE_PATH, _e0.LEDGER_PATH
PRICE_IN, PRICE_OUT = _e0.PRICE_IN, _e0.PRICE_OUT
call, flush, meter, parse_json = _e0.call, _e0.flush, _e0.meter, _e0.parse_json
prompt_hash, cache_key = _e0.prompt_hash, _e0.cache_key

E3_CAP_USD = 40.00
E3_PROJECTION_GATE_USD = 15.00

# D44-corrected list prices, verified 2026-08-11.
PRICE = {"gpt-4.1-mini": (0.40, 1.60), "gpt-5.4": (2.50, 15.00)}


class CapExceededE3(RuntimeError):
    pass


def _price_for(model):
    for k, v in PRICE.items():
        if str(model).startswith(k):
            return v
    return PRICE["gpt-4.1-mini"]


def spend(prefixes=None):
    """Cumulative E3 spend, summed over E3's own cache, priced per model."""
    if not CACHE_PATH.exists():
        return 0.0, 0
    usd, n = 0.0, 0
    for r in json.load(io.open(CACHE_PATH, encoding="utf-8")).values():
        arm = str(r.get("arm", ""))
        if prefixes and not arm.startswith(tuple(prefixes)):
            continue
        pi, po = _price_for(r.get("model", "gpt-4.1-mini"))
        usd += r.get("prompt_tokens", 0) / 1e6 * pi
        usd += r.get("completion_tokens", 0) / 1e6 * po
        n += 1
    return usd, n


def check_cap():
    total, n = spend()
    if total > E3_CAP_USD:
        flush()
        raise CapExceededE3(f"${total:.2f} over the ${E3_CAP_USD} E3 cap ({n} calls)")
    return total


def call_text_model(item_id, arm, messages, model, max_tokens=None, temperature=0,
                    seed=42):
    """Free-text completion against an arbitrary model, params-tolerant.

    Lifted from e2_api.call_text_model unchanged except for the module state it
    binds to. E0's `call` hard-codes JSON response format, which is right for the
    gate and wrong for the ANSWERER, whose prompt is FR's GENERATION_SYSTEM_PROMPT
    verbatim and contains no mention of JSON.
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
                if ("Unsupported" in msg or "unsupported" in msg
                        or "not supported" in msg or "max_tokens" in msg):
                    break
                time.sleep(2 ** attempt)
    raise last
