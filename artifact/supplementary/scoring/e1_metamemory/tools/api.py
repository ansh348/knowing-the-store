"""
api.py -- cached, metered OpenAI calls for E1.

This module did not exist: E1's Phase-0 scripts reached across and imported E0's
`api` off `sys.path`, which wrote E1's responses into E0's cache. That is now
fixed without duplicating a request path that must not drift between the two
studies. The client implementation is E0's, loaded by file path under a private
module name (`_e0_api`) so it can never be confused with this module: same disk
cache keyed by (item_id, arm, model, prompt_hash), same $10 hard cap with an $8
escalation threshold, same retry ladder, same tolerant JSON extraction.

Two things are re-pointed, and nothing else:

  * the cache and the ledger land under `e1_metamemory/cache/`, so E1 artifacts
    stay inside E1's write scope;
  * decoding parameters come from the FROZEN `prompts_e1` module -- gpt-4.1-mini,
    temperature 0, seed 42, max_tokens 200 (PREREG_E1.md section 7) -- rather
    than E0's `prompts.py`, whose values are E0's to change.

`.env` is loaded by the underlying client on first call; nothing here reads a key.
"""

from __future__ import annotations

import importlib.util as _ilu
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
_E0_TOOLS = PROJECT_ROOT / "e0_metamemory" / "tools"

for _p in (str(_E0_TOOLS), str(Path(__file__).resolve().parent)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Load E0's client under a private name. Importing it as `api` would be
# ambiguous with this file; spec_from_file_location removes the ambiguity.
_spec = _ilu.spec_from_file_location("_e0_api", _E0_TOOLS / "api.py")
_e0 = _ilu.module_from_spec(_spec)
sys.modules["_e0_api"] = _e0
_spec.loader.exec_module(_e0)

import prompts_e1 as _prompts  # noqa: E402  (frozen decoding parameters)

# --- the only redirections -------------------------------------------------- #
_e0.prompts = _prompts
_e0.CACHE_PATH = E1 / "cache" / "responses.json"
_e0.LEDGER_PATH = E1 / "cache" / "cost_ledger.json"

# Warm the cache on the importing thread. E0's `_load_cache()` runs OUTSIDE its
# lock, so with a cold cache several worker threads can each build a fresh dict;
# only the last assignment survives as the module global and the losers write
# their records into an orphan. Observed exactly once on the first E1 ladder run
# (180 calls, 179 cached records). Warming here single-threaded means every
# worker finds `_cache` already populated and the racing branch is never taken.
# Costs one file read; fixes nothing about E0, whose own runs are already spent.
_e0._load_cache()  # noqa: SLF001

CACHE_PATH = _e0.CACHE_PATH
LEDGER_PATH = _e0.LEDGER_PATH
PRICE_IN, PRICE_OUT = _e0.PRICE_IN, _e0.PRICE_OUT
HARD_CAP_USD, ESCALATE_USD = _e0.HARD_CAP_USD, _e0.ESCALATE_USD

CapExceeded = _e0.CapExceeded
call = _e0.call
flush = _e0.flush
meter = _e0.meter
parse_json = _e0.parse_json
prompt_hash = _e0.prompt_hash
cache_key = _e0.cache_key


def load_env() -> None:
    """Public alias for the client's .env loader (E0 spells it `_load_env`)."""
    _e0._load_env()  # noqa: SLF001


__all__ = ["CACHE_PATH", "LEDGER_PATH", "PRICE_IN", "PRICE_OUT", "HARD_CAP_USD",
           "ESCALATE_USD", "CapExceeded", "call", "flush", "meter", "parse_json",
           "prompt_hash", "cache_key", "load_env"]
