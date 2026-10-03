# -*- coding: utf-8 -*-
"""marker_arms.py -- ADDENDUM_MARKER_ABLATION (E3, program R117): the inexpressibility marker on Mem0 and A-MEM, omitted and neutralized.

Arms (pure functions of the recorded TRUE constrained rendering, e1_metamemory/indexes_v2.json key <backend>:<persona>:<variant>:TRUE):
  STRUCTURAL  the recorded text; wrapper prompts_e1.USER_INDEXED (the recorded arm INDEXED-TRUE)
  OMITTED     run_b.strip_markers (the three inexpressible sections left out, header and body); wrapper prompts_e1.USER_INDEXED_NOMARKER
              (E1.5 Run B, H-b; the GPT-4.1 mini rows are the recorded run_b_nomarker.json, never re-run)
  NEUTRAL     each marker body "not expressible by this backend" -> "This store does not record this. Judge it from the question alone."
              (three lines, nothing else); wrapper prompts_e1.USER_INDEXED with its quoted marker string replaced by the same text and
              nothing else changed (the author's ruling of 2026-09-19)
  BLIND       prompts_e1.USER_BLIND
Lanes: GPT-4.1 mini NEUTRAL on the 522 external coverage items (the E1 protocol: temperature 0, seed 42, max_tokens 200, JSON mode, a fresh
cache namespace under e1_metamemory/marker/cache); GPT-5.6 Luna on the pooled 66 (the external items of the 150-item frontier subset),
four arms, k = 5, raw Chat Completions, effort and temperature unset, max_completion_tokens 2048 (the R74 X4 settings).
Registration registrations/ADDENDUM_MARKER_ABLATION.md, registered-text sha256 6d3afee8..., frozen at 177697a. Cap 5 USD.

Subcommands:  build | lock | mini | luna [--draws 1,2,3,4,5]
"""
from __future__ import annotations

import concurrent.futures as cf
import datetime as dt
import hashlib
import importlib.util as ilu
import io
import json
import os
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"
sys.path.insert(0, str(E1 / "tools"))
import prompts_e1 as P  # noqa: E402

# run_b.py is a script (its module body runs the recorded elicitation through the cache), so its two builders are taken from its
# source by ast, not by import: strip_markers (the recorded Omitted rendering) and index_key, byte-for-byte the committed definitions.
import ast as _ast  # noqa: E402
_RUNB = (E1 / "tools" / "run_b.py").read_text(encoding="utf-8")
_tree = _ast.parse(_RUNB)
_defs = [n for n in _tree.body if isinstance(n, _ast.FunctionDef) and n.name in ("strip_markers", "index_key")]
assert {n.name for n in _defs} == {"strip_markers", "index_key"}
_ns = {"MARKER": "not expressible by this backend"}      # run_b.MARKER, the constant the builder closes over
exec(compile(_ast.Module(body=_defs, type_ignores=[]), str(E1 / "tools" / "run_b.py"), "exec"), _ns)  # noqa: S102
strip_markers, index_key = _ns["strip_markers"], _ns["index_key"]
SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}
RUNB_SHA256 = hashlib.sha256(_RUNB.encode("utf-8")).hexdigest()

REG = ROOT / "registrations" / "ADDENDUM_MARKER_ABLATION.md"
REG_SHA = "6d3afee82f2364b8d441ac097cae7917d3d0ec5f5b773317a8fd9a215e926d48"
FROZEN_AT = "177697a"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
MARKER = "not expressible by this backend"
NEUTRAL_TEXT = "This store does not record this. Judge it from the question alone."
USER_INDEXED_NEUTRAL = P.USER_INDEXED.replace(f'"{MARKER}"', f'"{NEUTRAL_TEXT}"')
assert USER_INDEXED_NEUTRAL != P.USER_INDEXED and USER_INDEXED_NEUTRAL.count(NEUTRAL_TEXT) == 1 and MARKER not in USER_INDEXED_NEUTRAL
OUT = E1 / "marker"
LOCK = OUT / "lock_marker.json"
BUILD = OUT / "build_marker.json"
CAP = 5.00
LUNA = "gpt-5.6-luna"
LUNA_PRICE = dict(inp=0.20, cached=0.02, out=1.20, write_mult=1.25)
K = 5
WORKERS = 8
EXPECTED_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"


def neutral(txt):
    lines = txt.split("\n")
    hits = [i for i, ln in enumerate(lines) if ln.strip() == MARKER]
    assert len(hits) == 3, ("expected exactly three marker lines", len(hits))
    out = list(lines)
    for i in hits:
        out[i] = lines[i].replace(MARKER, NEUTRAL_TEXT)
    r = "\n".join(out)
    assert MARKER not in r and r.count(NEUTRAL_TEXT) == 3 and len(out) == len(lines)
    assert all(a == b for j, (a, b) in enumerate(zip(lines, out)) if j not in hits)
    return r


def reg_sha():
    b = REG.read_bytes(); i = b.find(FROZEN_END); assert i > 0
    return hashlib.sha256(b[:i]).hexdigest()


def load():
    assert reg_sha() == REG_SHA, "REGISTRATION SHA MISMATCH -- STOP"
    assert P.texts_sha256() == EXPECTED_TEXTS_SHA, "frozen prompt texts changed -- STOP"
    items = [i for i in json.load(io.open(E1 / "build" / "items_final.json", encoding="utf-8"))
             if i.get("label", i["label_pre"]) in SCOREABLE and i["backend"] in ("mem0", "amem")]
    idx = json.load(io.open(E1 / "indexes_v2.json", encoding="utf-8"))["indexes"]
    main = json.load(io.open(E1 / "elicitation_main.json", encoding="utf-8"))
    qmap = {r["tag"]: r["question"] for r in main if r["arm"] != "BLIND"}
    sub = {r["item_id"]: r["question"] for r in json.load(io.open(E1 / "strong_model.json", encoding="utf-8"))["rows"]}
    ext66 = [i for i in items if i["item_id"] in sub]
    assert len(items) == 522 and len(ext66) == 66, (len(items), len(ext66))
    return items, idx, qmap, ext66


def texts_for(it, idx):
    k = f"{index_key(it)}:TRUE"
    t = idx[k]
    return {"STRUCTURAL": (P.USER_INDEXED, t), "OMITTED": (P.USER_INDEXED_NOMARKER, strip_markers(t)), "NEUTRAL": (USER_INDEXED_NEUTRAL, neutral(t))}


def messages(arm, it, idx, q):
    if arm == "BLIND":
        return [{"role": "system", "content": P.SYSTEM}, {"role": "user", "content": P.USER_BLIND.format(question=q)}]
    wrapper, text = texts_for(it, idx)[arm]
    return [{"role": "system", "content": P.SYSTEM}, {"role": "user", "content": wrapper.format(index=text, question=q)}]


def cmd_build():
    items, idx, qmap, ext66 = load()
    OUT.mkdir(exist_ok=True)
    keys = sorted({f"{index_key(it)}:TRUE" for it in items})
    shas = {}
    for k in keys:
        t = idx[k]; n = neutral(t); o = strip_markers(t)
        assert MARKER not in o
        shas[k] = {"structural": hashlib.sha256(t.encode()).hexdigest()[:16], "omitted": hashlib.sha256(o.encode()).hexdigest()[:16], "neutral": hashlib.sha256(n.encode()).hexdigest()[:16]}
    # the recorded Run B inputs reproduce: run_b.strip_markers on the same keys is the recorded arm's builder (asserted by construction)
    rec = {"registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "prompts_texts_sha256": P.texts_sha256(), "n_items": len(items), "n_ext66": len(ext66), "n_keys": len(keys),
           "neutral_text": NEUTRAL_TEXT, "wrapper_neutral_sha256": hashlib.sha256(USER_INDEXED_NEUTRAL.encode()).hexdigest(), "wrapper_nomarker_sha256": hashlib.sha256(P.USER_INDEXED_NOMARKER.encode()).hexdigest(),
           "texts": shas, "when": dt.datetime.now().isoformat(timespec="seconds")}
    io.open(BUILD, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    print(f"built: {len(keys)} keys, 3 texts each; neutral wrapper sha {rec['wrapper_neutral_sha256'][:16]}")


def cmd_lock():
    load(); assert BUILD.exists()
    b = json.load(io.open(BUILD, encoding="utf-8"))
    rec = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "build": {k: v for k, v in b.items() if k != "texts"},
           "mini": {"arm": "NEUTRAL", "model": P.MODEL, "temperature": P.TEMPERATURE, "seed": P.SEED, "max_tokens": P.MAX_TOKENS, "cache": "e1_metamemory/marker/cache (fresh namespace)"},
           "luna": {"arms": ["BLIND", "STRUCTURAL", "OMITTED", "NEUTRAL"], "model": LUNA, "k": K, "reasoning_effort": None, "temperature": None, "max_completion_tokens": 2048, "prices": LUNA_PRICE},
           "cap_usd": CAP, "when": dt.datetime.now().isoformat(timespec="seconds")}
    io.open(LOCK, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    print("lock written")


def e0_api():
    """E0's metered client under a private name, cache and ledger re-pointed to the fresh marker namespace (the E1 api.py recipe)."""
    sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))          # e0_common, as e1_metamemory/tools/api.py does
    spec = ilu.spec_from_file_location("_e0_api_marker", ROOT / "e0_metamemory" / "tools" / "api.py")
    m = ilu.module_from_spec(spec); sys.modules["_e0_api_marker"] = m; spec.loader.exec_module(m)
    m.prompts = P
    (OUT / "cache").mkdir(parents=True, exist_ok=True)
    m.CACHE_PATH = OUT / "cache" / "responses.json"; m.LEDGER_PATH = OUT / "cache" / "cost_ledger.json"
    m._load_cache()  # noqa: SLF001
    return m


def cmd_mini():
    items, idx, qmap, _ = load(); assert LOCK.exists()
    api = e0_api()
    jobs = [(it, qmap.get(it["item_id"], it.get("question", ""))) for it in items]
    assert all(q for _, q in jobs)
    rows_p = OUT / "rows_MINI_neutral.jsonl"
    done = {json.loads(l)["item_id"] for l in io.open(rows_p, encoding="utf-8")} if rows_p.exists() else set()
    jobs = [j for j in jobs if j[0]["item_id"] not in done]
    print(f"mini NEUTRAL: {len(jobs)} calls to go", flush=True)
    lock = threading.Lock()

    def one(job):
        it, q = job
        r = api.call(it["item_id"], "INDEXED-TRUE-NEUTRAL", messages("NEUTRAL", it, idx, q))
        o = api.parse_json(r["content"]) or {}
        f = o.get("fok")
        row = {"item_id": it["item_id"], "backend": it["backend"], "label": it.get("label", it["label_pre"]), "arm": "NEUTRAL", "model": r.get("model", P.MODEL),
               "fok": (min(100., max(0., float(f))) / 100.) if f is not None else None, "nok": (min(100., max(0., float(o["nok"]))) / 100. if o.get("nok") is not None else None),
               "status": "OK" if f is not None else "PARSE_FAIL", "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "cached": r.get("cached", False), "text": (r.get("content") or "")[:300]}
        with lock:
            with io.open(rows_p, "a", encoding="utf-8", newline="\n") as fh:
                fh.write(json.dumps(row, sort_keys=True) + "\n")
        return row

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for n, _ in enumerate(ex.map(one, jobs), 1):
            if n % 100 == 0:
                print(f"  {n}/{len(jobs)}", flush=True); api.flush()
    api.flush()
    print("mini NEUTRAL done;", json.dumps(api.meter()), flush=True)


def luna_price(usage):
    pt = usage.get("prompt_tokens", 0); ct = usage.get("completion_tokens", 0)
    det = usage.get("prompt_tokens_details") or {}
    cached = det.get("cached_tokens", 0) or 0; write = det.get("cache_write_tokens", 0) or 0
    plain = max(0, pt - cached - write)
    return (plain * LUNA_PRICE["inp"] + write * LUNA_PRICE["inp"] * LUNA_PRICE["write_mult"] + cached * LUNA_PRICE["cached"] + ct * LUNA_PRICE["out"]) / 1e6, cached, write, ((usage.get("completion_tokens_details") or {}).get("reasoning_tokens", 0) or 0)


def cmd_luna(draws):
    items, idx, qmap, ext66 = load(); assert LOCK.exists()
    from openai import OpenAI
    for line in io.open(ROOT / ".env", encoding="utf-8"):
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
    from run_cf import last_json, clamp  # noqa: E402  (the same parser as every raw-API lane)
    rows_p = OUT / "rows_LUNA.jsonl"
    done = set()
    if rows_p.exists():
        for l in io.open(rows_p, encoding="utf-8"):
            r = json.loads(l); done.add((r["item_id"], r["arm"], int(r["draw"])))
    spend = [sum(json.loads(l).get("usd", 0.0) for l in io.open(rows_p, encoding="utf-8"))] if rows_p.exists() else [0.0]
    lock = threading.Lock()
    arms = ("BLIND", "STRUCTURAL", "OMITTED", "NEUTRAL")

    def one(job):
        it, arm, d = job
        q = qmap.get(it["item_id"], it.get("question", ""))
        row = None
        for attempt in (1, 2, 3):
            try:
                cl = OpenAI(max_retries=2, timeout=120)
                r = cl.chat.completions.create(model=LUNA, max_completion_tokens=2048, messages=messages(arm, it, idx, q))
                usage = r.model_dump(mode="json").get("usage") or {}
                text = r.choices[0].message.content or ""
                usd, cached, write, reasoning = luna_price(usage)
                j = last_json(text) or {}
                fok, nok = clamp(j.get("fok")), clamp(j.get("nok"))
                row = {"item_id": it["item_id"], "backend": it["backend"], "label": it.get("label", it["label_pre"]), "arm": arm, "draw": d, "model": LUNA, "served_model": r.model,
                       "fok": fok, "nok": nok, "status": "OK" if fok is not None else "PARSE_FAIL", "tok_in": usage.get("prompt_tokens"), "tok_out": usage.get("completion_tokens"),
                       "tok_cached": cached, "tok_cache_write": write, "tok_reasoning": reasoning, "usd": usd, "finish_reason": r.choices[0].finish_reason, "text": text[:400],
                       "when": dt.datetime.now().isoformat(timespec="seconds")}
                assert LUNA in r.model, "SERVED IDENTIFIER MISMATCH -- STOP"
                break
            except AssertionError:
                raise
            except Exception as e:  # noqa: BLE001
                if attempt == 3:
                    row = {"item_id": it["item_id"], "arm": arm, "draw": d, "model": LUNA, "status": f"ERROR:{type(e).__name__}"}
                else:
                    time.sleep(5 * attempt)
        with lock:
            spend[0] += row.get("usd", 0.0)
            assert spend[0] <= CAP, "CAP"
            with io.open(rows_p, "a", encoding="utf-8", newline="\n") as fh:
                fh.write(json.dumps(row, sort_keys=True) + "\n")
        return row

    for d in draws:
        jobs = [(it, arm, d) for arm in arms for it in ext66 if (it["item_id"], arm, d) not in done]
        print(f"luna draw {d}: {len(jobs)} calls", flush=True)
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
            list(ex.map(one, jobs))
        print(f"luna draw {d} done; spend ${spend[0]:.4f}", flush=True)
    print(f"luna DONE; spend ${spend[0]:.4f}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "luna":
        cmd_luna([int(x) for x in sys.argv[sys.argv.index("--draws") + 1].split(",")] if "--draws" in sys.argv else list(range(1, K + 1)))
    else:
        globals()["cmd_" + cmd]()
