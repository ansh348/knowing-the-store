"""lane_probe.py -- E1-XV STEP 0(a): lane verification.

Two subcommands, deliberately separated so that *listing* what a provider serves
costs nothing and is not confused with *pinging* it:

    list   GET each provider's model catalogue and the key-status endpoint where
           one exists. Read-only, no tokens billed, no completion generated.
    ping   ONE minimal completion per pinned lane. Records the model ID the
           provider echoes back (which is the servable ID, not the alias we
           asked for), token usage, latency, and measured cost.

Nothing here imports E0's or E1's metered client: those carry E0/E1's own caps
and ledgers, and E1-XV's spend must be countable on its own. Keys are read from
the repo `.env` and never printed.
"""
from __future__ import annotations

import io
import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
XV = ROOT / "e1xv_crossvendor"
OUT = XV / "manifests"


def load_env() -> None:
    env = ROOT / ".env"
    for line in io.open(env, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def key(name: str) -> str | None:
    v = os.environ.get(name)
    return v if v else None


def get(url, headers, timeout=45):
    t0 = time.time()
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        return {"url": url, "status": r.status_code, "ms": int((time.time() - t0) * 1000),
                "body": r.json() if r.headers.get("content-type", "").startswith("application/json")
                else r.text[:400]}
    except Exception as e:  # network / DNS / TLS
        return {"url": url, "status": None, "ms": int((time.time() - t0) * 1000),
                "error": f"{type(e).__name__}: {e}"}


# --------------------------------------------------------------------------- #
# list
# --------------------------------------------------------------------------- #
def cmd_list():
    load_env()
    rec = {"probed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "lanes": {}}

    print("KEY PRESENCE (names only; values never read into the record)")
    for k in ("ANTHROPIC_API_KEY", "OPENROUTER_API_KEY", "MOONSHOT_API_KEY",
              "TOGETHER_API_KEY", "OPENAI_API_KEY"):
        v = key(k)
        print(f"  {k:22s} {'present' if v else 'ABSENT':>7s}"
              + (f"  len={len(v)}" if v else ""))
        rec.setdefault("keys", {})[k] = bool(v)

    # ---- Anthropic ---------------------------------------------------------
    print("\nANTHROPIC  GET /v1/models")
    if key("ANTHROPIC_API_KEY"):
        r = get("https://api.anthropic.com/v1/models?limit=100",
                {"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                 "anthropic-version": "2023-06-01"})
        rec["lanes"]["anthropic"] = {"status": r["status"], "ms": r["ms"]}
        print(f"  HTTP {r['status']}  {r['ms']}ms")
        if r["status"] == 200:
            ids = [(m["id"], m.get("display_name", ""), m.get("created_at", "")[:10])
                   for m in r["body"].get("data", [])]
            rec["lanes"]["anthropic"]["models"] = [i[0] for i in ids]
            for i, d, c in ids:
                print(f"    {i:44s} {c:12s} {d}")
        else:
            print("   ", json.dumps(r.get("body", r.get("error")))[:400])
    else:
        print("  key absent")

    # ---- OpenRouter --------------------------------------------------------
    print("\nOPENROUTER  GET /v1/key  (liveness + credit state)")
    if key("OPENROUTER_API_KEY"):
        h = {"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}
        r = get("https://openrouter.ai/api/v1/key", h)
        print(f"  HTTP {r['status']}  {r['ms']}ms")
        if r["status"] == 200:
            d = r["body"].get("data", {})
            print(f"    label={d.get('label')!r} usage={d.get('usage')} "
                  f"limit={d.get('limit')} limit_remaining={d.get('limit_remaining')} "
                  f"is_free_tier={d.get('is_free_tier')}")
            rec["lanes"]["openrouter"] = {"key_status": 200, "usage": d.get("usage"),
                                          "limit": d.get("limit"),
                                          "limit_remaining": d.get("limit_remaining")}
        else:
            print("   ", json.dumps(r.get("body", r.get("error")))[:400])
            rec["lanes"]["openrouter"] = {"key_status": r["status"]}

        print("\nOPENROUTER  GET /v1/models  (filtered: moonshot / kimi)")
        r = get("https://openrouter.ai/api/v1/models", h, timeout=90)
        if r["status"] == 200:
            data = r["body"].get("data", [])
            print(f"  catalogue size {len(data)}")
            hits = [m for m in data
                    if "moonshot" in m["id"].lower() or "kimi" in m["id"].lower()]
            rec["lanes"]["openrouter"]["kimi_models"] = []
            for m in sorted(hits, key=lambda x: x["id"]):
                p = m.get("pricing", {})
                row = {"id": m["id"], "name": m.get("name"),
                       "context": m.get("context_length"),
                       "prompt_per_tok": p.get("prompt"),
                       "completion_per_tok": p.get("completion"),
                       "created": m.get("created")}
                rec["lanes"]["openrouter"]["kimi_models"].append(row)
                pin = float(p.get("prompt") or 0) * 1e6
                pout = float(p.get("completion") or 0) * 1e6
                print(f"    {m['id']:46s} ctx={str(m.get('context_length')):>8s} "
                      f"${pin:.3f}/${pout:.3f} per Mtok   {m.get('name')}")
            if not hits:
                print("    NO moonshot/kimi entries in the catalogue")
        else:
            print(f"  HTTP {r['status']}", json.dumps(r.get("body", r.get("error")))[:300])
    else:
        print("  key absent")

    # ---- Moonshot direct ---------------------------------------------------
    for host in ("https://api.moonshot.ai", "https://api.moonshot.cn"):
        print(f"\nMOONSHOT DIRECT  GET {host}/v1/models")
        if not key("MOONSHOT_API_KEY"):
            print("  key absent")
            break
        r = get(f"{host}/v1/models",
                {"Authorization": f"Bearer {os.environ['MOONSHOT_API_KEY']}"})
        tag = "moonshot_" + host.rsplit(".", 1)[-1]
        rec["lanes"][tag] = {"status": r["status"], "ms": r["ms"]}
        print(f"  HTTP {r['status']}  {r['ms']}ms")
        if r["status"] == 200:
            ids = sorted(m["id"] for m in r["body"].get("data", []))
            rec["lanes"][tag]["models"] = ids
            for i in ids:
                print(f"    {i}")
        else:
            print("   ", json.dumps(r.get("body", r.get("error")))[:400])

    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "lane_catalogue.json"
    io.open(p, "w", encoding="utf-8").write(json.dumps(rec, indent=2, ensure_ascii=False))
    print(f"\nwritten: {p.relative_to(ROOT)}")


# --------------------------------------------------------------------------- #
# ping -- ONE completion per lane
# --------------------------------------------------------------------------- #
PING_SYSTEM = "Reply with the single word OK and nothing else."
PING_USER = "ping"


def ping_anthropic(model, max_tokens=16, extra=None, temp=0):
    from anthropic import Anthropic
    c = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    t0 = time.time()
    kw = dict(model=model, max_tokens=max_tokens, system=PING_SYSTEM,
              messages=[{"role": "user", "content": PING_USER}])
    if temp is not None:
        kw["temperature"] = temp
    if extra:
        kw.update(extra)
    r = c.messages.create(**kw)
    return {"asked": model, "served_model": r.model, "ms": int((time.time() - t0) * 1000),
            "in": r.usage.input_tokens, "out": r.usage.output_tokens,
            "stop_reason": r.stop_reason,
            "text": "".join(b.text for b in r.content if b.type == "text")[:80]}


def ping_openai_compat(model, base_url, api_key, extra=None, max_tokens=16, temp=0):
    from openai import OpenAI
    c = OpenAI(api_key=api_key, base_url=base_url)
    t0 = time.time()
    kw = dict(model=model, max_tokens=max_tokens,
              messages=[{"role": "system", "content": PING_SYSTEM},
                        {"role": "user", "content": PING_USER}])
    if temp is not None:
        kw["temperature"] = temp
    if extra:
        kw["extra_body"] = extra
    r = c.chat.completions.create(**kw)
    ch = r.choices[0]
    msg = ch.message
    reasoning = getattr(msg, "reasoning", None) or getattr(msg, "reasoning_content", None)
    u = r.usage
    return {"asked": model, "served_model": r.model, "ms": int((time.time() - t0) * 1000),
            "in": u.prompt_tokens, "out": u.completion_tokens,
            "reasoning_tokens": (getattr(getattr(u, "completion_tokens_details", None),
                                         "reasoning_tokens", None)),
            "finish_reason": ch.finish_reason,
            "reasoning_present": bool(reasoning),
            "reasoning_len": len(reasoning or ""),
            "text": (msg.content or "")[:80]}


def cmd_ping(targets):
    load_env()
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "lane_pings.json"
    rec = json.load(io.open(p, encoding="utf-8")) if p.exists() else {"pings": []}
    for spec in targets:
        # lane=model[@temp][:max_tokens][#json-extra-body]   @none omits temperature
        extra, mt, temp = None, 16, 0
        if "#" in spec:
            spec, blob = spec.split("#", 1)
            extra = json.loads(blob)
        if ":" in spec.split("=", 1)[1]:
            spec, mtxt = spec.rsplit(":", 1)
            mt = int(mtxt)
        if "@" in spec:
            spec, ttxt = spec.rsplit("@", 1)
            temp = None if ttxt == "none" else float(ttxt)
        lane, model = spec.split("=", 1)
        print(f"\nPING  lane={lane}  model={model}  temp={temp}  max_tokens={mt}  extra={extra}")
        try:
            if lane == "anthropic":
                r = ping_anthropic(model, max_tokens=mt, extra=extra, temp=temp)
            elif lane == "openrouter":
                r = ping_openai_compat(model, "https://openrouter.ai/api/v1",
                                       os.environ["OPENROUTER_API_KEY"],
                                       extra=extra, max_tokens=mt, temp=temp)
            elif lane == "moonshot":
                r = ping_openai_compat(model, "https://api.moonshot.ai/v1",
                                       os.environ["MOONSHOT_API_KEY"],
                                       extra=extra, max_tokens=mt, temp=temp)
            else:
                raise SystemExit(f"unknown lane {lane}")
            r["lane"], r["max_tokens"], r["extra_body"], r["temperature"] = lane, mt, extra, temp
            r["ok"] = True
        except Exception as e:
            r = {"lane": lane, "asked": model, "max_tokens": mt, "extra_body": extra,
                 "temperature": temp, "ok": False,
                 "error": f"{type(e).__name__}: {str(e)[:600]}"}
        r["probed_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        rec["pings"].append(r)
        for k, v in r.items():
            print(f"    {k:20s} {v}")
    io.open(p, "w", encoding="utf-8").write(json.dumps(rec, indent=2, ensure_ascii=False))
    print(f"\nwritten: {p.relative_to(ROOT)}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "list":
        cmd_list()
    elif sys.argv[1] == "ping":
        cmd_ping(sys.argv[2:])
    else:
        raise SystemExit("usage: lane_probe.py [list | ping lane=model ...]")
