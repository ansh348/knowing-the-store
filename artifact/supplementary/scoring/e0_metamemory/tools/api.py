"""
api.py -- cached, metered OpenAI calls for E0.

Every response is cached to disk keyed by (item_id, arm, model, prompt_hash), as
the pre-registration requires, so a re-run costs nothing and the raw responses are
committable. Spend is metered against the $10 hard cap with an $8 escalation
threshold; exceeding the cap raises rather than silently continuing.

Decoding parameters come from tools/prompts.py and are not overridable here --
temperature 0, seed 42 -- so the harness cannot drift from the frozen spec.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import threading
import time
from pathlib import Path

from e0_common import E0, jdump

import prompts

CACHE_PATH = E0 / "cache" / "responses.json"
LEDGER_PATH = E0 / "cache" / "cost_ledger.json"

# cost_analysis/compute_token_costs.py:42 -- USD per 1M tokens (in, out)
PRICE_IN, PRICE_OUT = 0.40, 1.60
HARD_CAP_USD = 10.00
ESCALATE_USD = 8.00

_lock = threading.Lock()
_cache = None
_meter = {"calls": 0, "cached": 0, "in": 0, "out": 0, "usd": 0.0}


class CapExceeded(RuntimeError):
    pass


def _load_env():
    env = Path(__file__).resolve().parents[2] / ".env"
    for line in io.open(env, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _client():
    _load_env()
    from openai import OpenAI
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def prompt_hash(messages) -> str:
    return hashlib.sha256(
        json.dumps(messages, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]


def cache_key(item_id, arm, model, phash) -> str:
    return hashlib.sha256(f"{item_id}||{arm}||{model}||{phash}".encode()).hexdigest()[:24]


def _load_cache():
    global _cache
    if _cache is None:
        _cache = json.load(io.open(CACHE_PATH, encoding="utf-8")) if CACHE_PATH.exists() else {}
    return _cache


def call(item_id, arm, messages, model=None, max_tokens=None):
    """Cached chat completion. Returns {content, usage, cached, key}."""
    model = model or prompts.MODEL
    max_tokens = max_tokens or prompts.MAX_TOKENS
    ph = prompt_hash(messages)
    key = cache_key(item_id, arm, model, ph)
    c = _load_cache()
    with _lock:
        if key in c:
            _meter["cached"] += 1
            return {**c[key], "cached": True, "key": key}

    last = None
    for attempt in range(4):
        try:
            r = _client().chat.completions.create(
                model=model, temperature=prompts.TEMPERATURE, seed=prompts.SEED,
                max_tokens=max_tokens, messages=messages,
                response_format={"type": "json_object"})
            break
        except Exception as e:                                   # noqa: BLE001
            last = e
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    else:                                                        # pragma: no cover
        raise last

    rec = {"content": r.choices[0].message.content,
           "prompt_tokens": r.usage.prompt_tokens,
           "completion_tokens": r.usage.completion_tokens,
           "model": model, "item_id": item_id, "arm": arm, "prompt_hash": ph}
    with _lock:
        _meter["calls"] += 1
        _meter["in"] += rec["prompt_tokens"]
        _meter["out"] += rec["completion_tokens"]
        _meter["usd"] = (_meter["in"] / 1e6) * PRICE_IN + (_meter["out"] / 1e6) * PRICE_OUT
        c[key] = rec
        if _meter["usd"] > HARD_CAP_USD:
            flush()
            raise CapExceeded(f"spend ${_meter['usd']:.2f} exceeded the ${HARD_CAP_USD} cap")
    return {**rec, "cached": False, "key": key}


def flush():
    with _lock:
        if _cache is not None:
            jdump(_cache, CACHE_PATH)
        jdump({**_meter, "price_in_per_mtok": PRICE_IN, "price_out_per_mtok": PRICE_OUT,
               "hard_cap_usd": HARD_CAP_USD}, LEDGER_PATH)


def meter():
    return dict(_meter)


def parse_json(content):
    """Tolerant JSON extraction; returns None if it cannot be parsed."""
    if not content:
        return None
    try:
        return json.loads(content)
    except Exception:                                            # noqa: BLE001
        i, j = content.find("{"), content.rfind("}")
        if i >= 0 and j > i:
            try:
                return json.loads(content[i:j + 1])
            except Exception:                                    # noqa: BLE001
                return None
        return None
