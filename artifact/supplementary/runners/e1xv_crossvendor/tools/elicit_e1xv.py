"""elicit_e1xv.py -- E1-XV STEP 2 elicitation, per PREREG_E1XV.md (386d334...) only.

Three lanes, registered parameters, no deviation from the freeze:

    claude-opus-5              T omitted (D86)  max_tokens 1024 (D91)  Batch API
    claude-haiku-4-5-20251001  T = 0            max_tokens  200        Batch API
    kimi-k3  (Moonshot direct) T = 1 (D86)      max_tokens 4096 (D87)  synchronous

Cache key is (item, arm, model, draw, prompt_hash), as registered. Rows are appended
to a JSONL as they land, so an interrupted run resumes without repeating completed
work and without double-counting. Raw rows are committed AS ROWS before any scoring.

Reasoning text is stored on the row and NEVER fed to the parser (prereg section 3).

    python elicit_e1xv.py k3
    python elicit_e1xv.py batch-submit  <model>
    python elicit_e1xv.py batch-collect <model>
    python elicit_e1xv.py status
"""
from __future__ import annotations

import concurrent.futures as cf
import hashlib
import io
import json
import os
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
XV = ROOT / "e1xv_crossvendor"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from cell_e1xv import build           # noqa: E402  asserts frozen prompt shas
from lane_probe import load_env       # noqa: E402
from calibrate_e1xv import last_json, clamp, PRICES   # noqa: E402
import prompts_e1 as P                # noqa: E402

ROWS = XV / "rows"
MAN = XV / "manifests"
K = 5                                  # prereg section 1
CAP = 28.00
ABORT_AT = 26.50                       # leave margin; raises rather than overruns

LANES = {
    "claude-opus-5": {"code": "OP5", "temp": None, "max_tokens": 1024, "path": "batch"},
    "claude-haiku-4-5-20251001": {"code": "H45", "temp": 0.0, "max_tokens": 200,
                                  "path": "batch"},
    "kimi-k3": {"code": "K3", "temp": 1.0, "max_tokens": 4096, "path": "sync"},
}

_lock = threading.Lock()
_meter = {"in": 0, "out": 0, "usd": 0.0, "calls": 0}


def prompt_hash(msgs) -> str:
    return hashlib.sha256(json.dumps(msgs, sort_keys=True,
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


def messages(row, arm):
    return [{"role": "system", "content": P.SYSTEM},
            {"role": "user", "content": row["user_blind"] if arm == "BLIND"
             else row["user_indexed"]}]


def jobs_for(model):
    """The 840 registered jobs for one lane, in a fixed deterministic order."""
    rows, got, _, _, _ = build()
    if got != {"n": 84, "n_fok_pos": 54, "n_nok_pos": 40}:
        raise SystemExit("cell does not rebuild -- refusing to elicit")
    code = LANES[model]["code"]
    out = []
    for idx, row in enumerate(rows):                 # rows are sorted by item_id
        for arm in ("BLIND", "INDEXED-TRUE"):
            msgs = messages(row, arm)
            ph = prompt_hash(msgs)
            for d in range(1, K + 1):
                out.append({
                    "item_id": row["item_id"], "arm": arm, "model": model, "draw": d,
                    "prompt_hash": ph, "messages": msgs, "label": row["label"],
                    "y_fok": row["y_fok"], "y_nok": row["y_nok"],
                    "cid": f"{code}-{'B' if arm == 'BLIND' else 'I'}-{idx:03d}-d{d}"})
    return out


def rowpath(model):
    return ROWS / f"elicitation_{model}.jsonl"


def done_keys(model):
    p, done = rowpath(model), {}
    if p.exists():
        for ln in io.open(p, encoding="utf-8"):
            ln = ln.strip()
            if not ln:
                continue
            try:
                r = json.loads(ln)
            except Exception:                        # noqa: BLE001
                continue
            done[(r["item_id"], r["arm"], r["model"], r["draw"], r["prompt_hash"])] = r
    return done


def key_of(j):
    return (j["item_id"], j["arm"], j["model"], j["draw"], j["prompt_hash"])


def bill(model, tin, tout, batch=False):
    pin, pout = PRICES[model]
    m = 0.5 if batch else 1.0
    usd = (tin / 1e6 * pin + tout / 1e6 * pout) * m
    with _lock:
        _meter["in"] += tin; _meter["out"] += tout
        _meter["usd"] += usd; _meter["calls"] += 1
    return usd


def prior_spend():
    """Everything E1-XV has billed before this run, from the committed ledger."""
    p = MAN / "projection.json"
    return json.load(io.open(p, encoding="utf-8")).get("spent_to_date_usd", 0.0) \
        if p.exists() else 0.0


def make_row(j, *, ok, text="", reasoning="", tin=0, tout=0, finish=None,
             served=None, err=None, usd=0.0, path="sync"):
    obj = last_json(text) if ok else None            # reasoning NEVER parsed
    return {"item_id": j["item_id"], "arm": j["arm"], "model": j["model"],
            "draw": j["draw"], "prompt_hash": j["prompt_hash"], "cid": j["cid"],
            "label": j["label"], "y_fok": j["y_fok"], "y_nok": j["y_nok"],
            "fok": clamp((obj or {}).get("fok")), "nok": clamp((obj or {}).get("nok")),
            "nok_candidates_found": (obj or {}).get("nok_candidates_found"),
            "would_search": (obj or {}).get("would_search"),
            "status": ("OK" if (ok and obj is not None) else
                       ("PARSE_FAIL" if ok else f"ERROR:{err}")),
            "parsed": obj is not None, "finish_reason": finish, "served_model": served,
            "tok_in": tin, "tok_out": tout, "usd": round(usd, 6), "path": path,
            "text": text, "reasoning": reasoning,
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


# --------------------------------------------------------------------------- #
# synchronous lane (K3)
# --------------------------------------------------------------------------- #
def run_sync(model, workers=8):
    from openai import OpenAI
    cfg = LANES[model]
    c = OpenAI(api_key=os.environ["MOONSHOT_API_KEY"],
               base_url="https://api.moonshot.ai/v1")
    todo = [j for j in jobs_for(model) if key_of(j) not in done_keys(model)]
    print(f"{model}: {len(todo)} calls to make "
          f"({840 - len(todo)} already on disk)", flush=True)
    if not todo:
        return
    ROWS.mkdir(parents=True, exist_ok=True)
    fh = io.open(rowpath(model), "a", encoding="utf-8", newline="\n")
    base = prior_spend()

    def one(j):
        for attempt in range(4):
            try:
                r = c.chat.completions.create(
                    model=model, messages=j["messages"], temperature=cfg["temp"],
                    max_tokens=cfg["max_tokens"])
                ch, u = r.choices[0], r.usage
                msg = ch.message
                reason = (getattr(msg, "reasoning", None)
                          or getattr(msg, "reasoning_content", None) or "")
                usd = bill(model, u.prompt_tokens, u.completion_tokens)
                return make_row(j, ok=True, text=msg.content or "", reasoning=reason,
                                tin=u.prompt_tokens, tout=u.completion_tokens,
                                finish=ch.finish_reason, served=r.model, usd=usd)
            except Exception as e:                    # noqa: BLE001
                if attempt == 3:
                    return make_row(j, ok=False, err=f"{type(e).__name__}:{str(e)[:160]}")
                time.sleep(2 * (attempt + 1))

    n = 0
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for row in ex.map(one, todo):
            fh.write(json.dumps(row, ensure_ascii=False) + "\n"); fh.flush()
            n += 1
            if base + _meter["usd"] > ABORT_AT:
                fh.close()
                raise SystemExit(f"SPEND ABORT at ${base + _meter['usd']:.2f} "
                                 f"(limit ${ABORT_AT}); {n} rows written, resume is safe")
            if n % 40 == 0:
                print(f"  {n}/{len(todo)}  ${base + _meter['usd']:.2f} cumulative",
                      flush=True)
    fh.close()
    print(f"  done {n} calls, ${_meter['usd']:.4f} this run", flush=True)


# --------------------------------------------------------------------------- #
# batch lane (Anthropic)
# --------------------------------------------------------------------------- #
def anth():
    from anthropic import Anthropic
    return Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def batch_submit(model):
    cfg = LANES[model]
    todo = [j for j in jobs_for(model) if key_of(j) not in done_keys(model)]
    print(f"{model}: {len(todo)} requests to submit")
    if not todo:
        return None
    reqs = []
    for j in todo:
        params = {"model": model, "max_tokens": cfg["max_tokens"],
                  "system": P.SYSTEM,
                  "messages": [m for m in j["messages"] if m["role"] != "system"]}
        if cfg["temp"] is not None:
            params["temperature"] = cfg["temp"]
        reqs.append({"custom_id": j["cid"], "params": params})
    b = anth().messages.batches.create(requests=reqs)
    MAN.mkdir(parents=True, exist_ok=True)
    io.open(MAN / f"batch_{cfg['code']}.txt", "w", encoding="utf-8").write(b.id)
    print(f"  submitted {b.id}  status={b.processing_status}  n={len(reqs)}")
    return b.id


def batch_collect(model, max_wait=5400):
    cfg = LANES[model]
    bid = io.open(MAN / f"batch_{cfg['code']}.txt", encoding="utf-8").read().strip()
    c = anth()
    t0 = time.time()
    while True:
        b = c.messages.batches.retrieve(bid)
        rc = b.request_counts
        print(f"  [{int(time.time() - t0):5d}s] {b.processing_status}  ok={rc.succeeded} "
              f"err={rc.errored} proc={rc.processing}", flush=True)
        if b.processing_status == "ended":
            break
        if time.time() - t0 > max_wait:
            print("  still processing -- re-run batch-collect; the batch persists")
            return False
        time.sleep(30)

    byc = {j["cid"]: j for j in jobs_for(model)}
    have = done_keys(model)
    ROWS.mkdir(parents=True, exist_ok=True)
    fh = io.open(rowpath(model), "a", encoding="utf-8", newline="\n")
    n = 0
    for r in c.messages.batches.results(bid):
        j = byc.get(r.custom_id)
        if j is None or key_of(j) in have:
            continue
        res = r.result
        if res.type != "succeeded":
            row = make_row(j, ok=False, err=f"batch:{res.type}", path="batch")
        else:
            m = res.message
            txt = "".join(x.text for x in m.content if x.type == "text")
            usd = bill(model, m.usage.input_tokens, m.usage.output_tokens, batch=True)
            row = make_row(j, ok=True, text=txt, tin=m.usage.input_tokens,
                           tout=m.usage.output_tokens, finish=m.stop_reason,
                           served=m.model, usd=usd, path="batch")
        fh.write(json.dumps(row, ensure_ascii=False) + "\n"); fh.flush()
        n += 1
    fh.close()
    print(f"  collected {n} rows, ${_meter['usd']:.4f} billed (batch rate)")
    return True


def status():
    tot = 0.0
    print(f"{'model':28s} {'rows':>5s} {'/840':>5s} {'parsed':>7s} {'errors':>7s} {'$':>9s}")
    for model in LANES:
        d = done_keys(model)
        rows = list(d.values())
        p = sum(1 for r in rows if r["parsed"])
        e = sum(1 for r in rows if r["status"].startswith("ERROR"))
        usd = sum(r.get("usd", 0) for r in rows)
        tot += usd
        print(f"{model:28s} {len(rows):5d} {840:5d} {p:7d} {e:7d} {usd:9.4f}")
    print(f"{'TOTAL':28s} {'':5s} {2520:5d} {'':7s} {'':7s} {tot:9.4f}")
    print(f"  prior (STEP 0 + pilots): ${prior_spend():.4f}   "
          f"grand total ${prior_spend() + tot:.4f} of ${CAP:.2f}")


if __name__ == "__main__":
    load_env()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "k3":
        run_sync("kimi-k3")
    elif cmd == "batch-submit":
        batch_submit(sys.argv[2])
    elif cmd == "batch-collect":
        batch_collect(sys.argv[2])
    elif cmd == "status":
        status()
    else:
        raise SystemExit(__doc__)
