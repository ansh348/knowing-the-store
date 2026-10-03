"""probe.py -- R85 Amendment 1, Step 1. ONE identifier probe on the OpenAI key. BILLED (a few tokens).

Confirms that the metered key serves the pinned extractor identifier before ingestion, the way the
30 August pre-flight did (r85_graphiti/billing_probe.json). One chat call, max_tokens 1; the served
model string and the usage are recorded to r85_graphiti/g10/probe_g10.json.

Runs in the stock venv (graphiti-core's own openai 2.24.0):
  /c/Users/[AUTHOR-1]/AppData/Local/r85_stock_venv/Scripts/python.exe r85_graphiti/g10/probe.py
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

MODEL = "gpt-4.1-mini-2025-04-14"
PRICE_IN, PRICE_OUT = 0.40, 1.60  # USD per 1M tokens, r85_graphiti/ingest.py PRICES


def main():
    from openai import OpenAI

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY not set")
    client = OpenAI(api_key=key)
    r = client.chat.completions.create(
        model=MODEL, max_tokens=1, temperature=0,
        messages=[{"role": "user", "content": "Reply with the single word OK."}],
    )
    usage = r.usage
    usd = usage.prompt_tokens / 1e6 * PRICE_IN + usage.completion_tokens / 1e6 * PRICE_OUT
    out = {
        "probe_utc": datetime.now(timezone.utc).isoformat(),
        "step": "Amendment 1, Step 1",
        "openai": {
            "status": "PASS" if r.model == MODEL else "MISMATCH",
            "key_name": "OPENAI_API_KEY",
            "key_prefix": key[:3] + "...",
            "requested_model": MODEL,
            "served_model": r.model,
            "in": usage.prompt_tokens,
            "out": usage.completion_tokens,
            "usd": round(usd, 8),
        },
    }
    (HERE / "probe_g10.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    if r.model != MODEL:
        sys.exit(f"served identifier {r.model!r} is not the pinned {MODEL!r}")


if __name__ == "__main__":
    main()
