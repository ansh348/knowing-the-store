"""calibrate_e1xv.py -- E1-XV STEP 0: measure, on REAL cell prompts, what each lane
actually costs and whether the frozen decoding spec survives the port.

This exists because a projection built from chat-model assumptions would be wrong
for a reasoning model that thinks by default. The K3 line in particular must be
itemised from measured reasoning-token consumption, not guessed.

Deliberately small: a handful of items per lane, reported per call, never scored.
Elicited values ARE printed so that a parse-rate can be computed, but no AUROC,
no arm comparison, and no aggregate over the cell is produced here -- that is
STEP 2's job and it is gated.

    python calibrate_e1xv.py <lane> <model> [--n 3] [--arm both|blind|indexed]
                             [--max-tokens 200] [--temp 0|1|none] [--extra '{...}']
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from cell_e1xv import build  # noqa: E402  (asserts the frozen prompt shas on import)
from lane_probe import load_env  # noqa: E402
import prompts_e1 as P  # noqa: E402

# USD per 1M tokens, list price at run date 2026-08-13. Sources recorded in
# STEP0_LANES.md; cache-hit pricing is NOT assumed anywhere.
PRICES = {
    "claude-opus-5": (5.00, 25.00),
    "claude-opus-4-5-20251101": (5.00, 25.00),
    "claude-sonnet-5": (2.00, 10.00),
    "claude-haiku-4-5-20251001": (1.00, 5.00),
    "kimi-k3": (3.00, 15.00),
    "moonshotai/kimi-k3": (3.00, 15.00),
}


def last_json(s):
    """Tolerant final-JSON extraction, verbatim in behaviour from
    e1_metamemory/tools/redraw_frontier.py:last_json -- the frozen parse path."""
    d, st, esc, start = 0, False, False, -1
    for i, c in enumerate(s):
        if esc:
            esc = False; continue
        if c == "\\":
            esc = True; continue
        if c == chr(34):
            st = not st; continue
        if st:
            continue
        if c == "{":
            if d == 0:
                start = i
            d += 1
        elif c == "}":
            d -= 1
            if d == 0 and start >= 0:
                try:
                    return json.loads(s[start:i + 1])
                except Exception:                              # noqa: BLE001
                    pass
    return None


def clamp(v):
    try:
        return min(100.0, max(0.0, float(v))) / 100.0
    except (TypeError, ValueError):
        return None


def call_anthropic(model, system, user, max_tokens, temp, extra):
    from anthropic import Anthropic
    c = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    kw = dict(model=model, max_tokens=max_tokens, system=system,
              messages=[{"role": "user", "content": user}])
    if temp is not None:
        kw["temperature"] = temp
    if extra:
        kw.update(extra)
    r = c.messages.create(**kw)
    txt = "".join(b.text for b in r.content if b.type == "text")
    think = "".join(getattr(b, "thinking", "") for b in r.content if b.type == "thinking")
    return {"in": r.usage.input_tokens, "out": r.usage.output_tokens,
            "reasoning_tokens": None, "reasoning_len": len(think),
            "finish": r.stop_reason, "text": txt, "served": r.model}


def call_oai(model, system, user, max_tokens, temp, extra, base, key):
    from openai import OpenAI
    c = OpenAI(api_key=key, base_url=base)
    kw = dict(model=model, max_tokens=max_tokens,
              messages=[{"role": "system", "content": system},
                        {"role": "user", "content": user}])
    if temp is not None:
        kw["temperature"] = temp
    if extra:
        kw["extra_body"] = extra
    r = c.chat.completions.create(**kw)
    ch, u = r.choices[0], r.usage
    msg = ch.message
    reason = getattr(msg, "reasoning", None) or getattr(msg, "reasoning_content", None) or ""
    rt = getattr(getattr(u, "completion_tokens_details", None), "reasoning_tokens", None)
    return {"in": u.prompt_tokens, "out": u.completion_tokens,
            "reasoning_tokens": rt, "reasoning_len": len(reason),
            "finish": ch.finish_reason, "text": msg.content or "", "served": r.model}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lane"); ap.add_argument("model")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--arm", default="both", choices=["both", "blind", "indexed"])
    ap.add_argument("--max-tokens", type=int, default=P.MAX_TOKENS)
    ap.add_argument("--temp", default="0")
    ap.add_argument("--extra", default=None)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()

    load_env()
    temp = None if a.temp == "none" else float(a.temp)
    extra = json.loads(a.extra) if a.extra else None
    rows, got, _, _, _ = build()
    if got != {"n": 84, "n_fok_pos": 54, "n_nok_pos": 40}:
        raise SystemExit("cell does not rebuild")

    # deterministic, spread across labels so the sample is not all one class
    by = sorted(rows, key=lambda r: (r["label"], r["item_id"]))
    pick, step = [], max(1, len(by) // a.n)
    for i in range(0, len(by), step):
        if len(pick) < a.n:
            pick.append(by[i])

    arms = ["BLIND", "INDEXED-TRUE"] if a.arm == "both" else \
           (["BLIND"] if a.arm == "blind" else ["INDEXED-TRUE"])

    print(f"CALIBRATION  lane={a.lane}  model={a.model}  temp={temp}  "
          f"max_tokens={a.max_tokens}  extra={extra}")
    print(f"  {a.n} items x {len(arms)} arm(s) = {a.n * len(arms)} calls; "
          f"parse path = frozen last_json\n")

    pin, pout = PRICES.get(a.model, (None, None))
    recs, tin, tout = [], 0, 0
    for it in pick:
        for arm in arms:
            user = it["user_blind"] if arm == "BLIND" else it["user_indexed"]
            t0 = time.time()
            try:
                if a.lane == "anthropic":
                    r = call_anthropic(a.model, P.SYSTEM, user, a.max_tokens, temp, extra)
                elif a.lane == "moonshot":
                    r = call_oai(a.model, P.SYSTEM, user, a.max_tokens, temp, extra,
                                 "https://api.moonshot.ai/v1", os.environ["MOONSHOT_API_KEY"])
                elif a.lane == "openrouter":
                    r = call_oai(a.model, P.SYSTEM, user, a.max_tokens, temp, extra,
                                 "https://openrouter.ai/api/v1", os.environ["OPENROUTER_API_KEY"])
                else:
                    raise SystemExit(f"unknown lane {a.lane}")
                r["ok"] = True
            except Exception as e:                              # noqa: BLE001
                r = {"ok": False, "error": f"{type(e).__name__}: {str(e)[:300]}",
                     "in": 0, "out": 0, "reasoning_tokens": None, "reasoning_len": 0,
                     "finish": None, "text": "", "served": None}
            r["ms"] = int((time.time() - t0) * 1000)
            obj = last_json(r["text"]) if r["ok"] else None
            r.update(item_id=it["item_id"], arm=arm, label=it["label"],
                     parsed=obj is not None,
                     fok=clamp((obj or {}).get("fok")), nok=clamp((obj or {}).get("nok")))
            tin += r["in"]; tout += r["out"]
            recs.append(r)
            rt = r["reasoning_tokens"]
            print(f"  {it['item_id'][:34]:34s} {arm:13s} in={r['in']:6d} out={r['out']:5d} "
                  f"reas={str(rt if rt is not None else r['reasoning_len'] and '~chars'):>6s} "
                  f"finish={str(r['finish']):12s} parsed={'Y' if r['parsed'] else 'N'} "
                  f"fok={r['fok']} nok={r['nok']}"
                  + ("" if r["ok"] else f"\n      ERROR {r['error']}"))

    n = len(recs)
    ok = sum(1 for r in recs if r["ok"])
    parsed = sum(1 for r in recs if r["parsed"])
    rts = [r["reasoning_tokens"] for r in recs if r["reasoning_tokens"]]
    print(f"\n  calls {n}   http-ok {ok}   parsed {parsed}/{n} "
          f"({parsed / n * 100:.0f}%)   truncated "
          f"{sum(1 for r in recs if r['finish'] in ('length', 'max_tokens'))}")
    print(f"  tokens  in {tin}  out {tout}   mean/call  in {tin // n}  out {tout // n}")
    if rts:
        print(f"  reasoning tokens  min {min(rts)}  mean {sum(rts) // len(rts)}  max {max(rts)}"
              f"   share of output {sum(rts) / max(1, tout) * 100:.0f}%")
    if pin:
        usd = tin / 1e6 * pin + tout / 1e6 * pout
        print(f"  measured cost ${usd:.4f} at ${pin}/${pout} per Mtok "
              f"-> ${usd / n:.5f} per call")

    out = Path(__file__).resolve().parents[1] / "manifests" / "calibration.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    prev = json.load(io.open(out, encoding="utf-8")) if out.exists() else {"runs": []}
    prev["runs"].append({
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "lane": a.lane, "model": a.model, "temp": temp, "max_tokens": a.max_tokens,
        "extra": extra, "tag": a.tag, "n_calls": n, "http_ok": ok, "parsed": parsed,
        "tok_in": tin, "tok_out": tout,
        "reasoning_tokens": {"min": min(rts), "mean": sum(rts) // len(rts), "max": max(rts)}
        if rts else None,
        "rows": [{k: r[k] for k in ("item_id", "arm", "label", "in", "out",
                                    "reasoning_tokens", "finish", "parsed", "fok", "nok",
                                    "ok", "served")} for r in recs]})
    io.open(out, "w", encoding="utf-8").write(json.dumps(prev, indent=2, ensure_ascii=False))
    print(f"  written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
