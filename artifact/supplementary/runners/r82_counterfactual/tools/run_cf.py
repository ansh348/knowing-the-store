"""run_cf.py -- R82-CF: elicitation on the 90-item counterfactual cell.

Frozen: prompts_e1 verbatim, digests asserted against the values E1 committed. k=5 on the
Anthropic lanes with MIN_DRAWS=3 at scoring, as in the X4 protocol. mini is k=1 temperature
0, as in E1.

ARMS
    BLIND         30 calls, one per question, reused across that question's three versions
                  because the input is identical. Blind AUROC is 0.5 by the identity
                  registered in ADDENDUM_R82 section 6.
    INDEXED-V2    90 calls, the committed renderer under TRUE provenance
    INDEXED-V3    90 calls, v2 plus the retracted and expired name sections

Subcommands
    probe <lane>    one blind and one indexed call; assert the served model id (E1.7 rule)
    project         per-lane projection from probes.json, reported BEFORE launch
    submit <lane>   Anthropic lanes: one Batch
    poll <lane>     Anthropic lanes: poll, and collect rows when ended
    sync <lane>     mini: synchronous run with jsonl resume

Ceiling $15 (ADDENDUM_R82 section 10 as amended by section 24). The run stops at the ceiling.
"""
from __future__ import annotations

import concurrent.futures
import io
import json
import os
import pathlib
import sys
import threading
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import prompts_e1 as P  # noqa: E402

R82 = ROOT / "r82_counterfactual"
ROWS = R82 / "rows"
PROBES = R82 / "probes.json"

# the digests E1 committed for the frozen prompt module (r74/x4/cell_661.json)
E1_FILE_SHA = "337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84"
E1_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"
assert P.file_sha256() == E1_FILE_SHA, "prompts_e1.py has changed since E1 froze it"
assert P.texts_sha256() == E1_TEXTS_SHA, "prompts_e1 frozen texts have changed"

CELL = json.load(io.open(R82 / "cf_cell.json", encoding="utf-8"))["items"]
IDX = json.load(io.open(R82 / "cf_indexes.json", encoding="utf-8"))["indexes"]
K = 5
ARMS = ("BLIND", "INDEXED-V2", "INDEXED-V3")

LANES = {
    "gpt-4.1-mini": dict(vendor="openai", code="MINI", temp=0.0, max_tokens=200,
                         price=(0.40, 1.60), mult=1.0, k=1),
    "claude-haiku-4-5-20251001": dict(vendor="anthropic", code="H45", temp=0.0,
                                      max_tokens=200, price=(1.00, 5.00), mult=0.5, k=K),
    "claude-opus-5": dict(vendor="anthropic", code="OP5", temp=None, max_tokens=1024,
                          price=(5.00, 25.00), mult=0.5, k=K),
}

# BLIND is one call per QUESTION; the indexed arms are one call per ITEM.
QUESTIONS = sorted({it["question"]: it for it in CELL}.items())
BLIND_UNITS = [{"unit_id": f"q{n:02d}", "question": q} for n, (q, _) in enumerate(QUESTIONS)]


def units(arm):
    if arm == "BLIND":
        return BLIND_UNITS
    return [{"unit_id": it["item_id"], "question": it["question"],
             "index": IDX[it["item_id"]]["v2" if arm == "INDEXED-V2" else "v3"]}
            for it in CELL]


def prompts_for(u, arm):
    if arm == "BLIND":
        return P.SYSTEM, P.USER_BLIND.format(question=u["question"])
    return P.SYSTEM, P.USER_INDEXED.format(index=u["index"], question=u["question"])


def last_json(text):
    depth, start, best, ins, esc = 0, None, None, False, False
    for i, ch in enumerate(text or ""):
        if ins:
            ins = not (ch == '"' and not esc)
            esc = (ch == "\\" and not esc)
            continue
        if ch == '"':
            ins, esc = True, False
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None:
                best = text[start:i + 1]
    try:
        return json.loads(best) if best else None
    except Exception:
        return None


def clamp(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    if v > 1:
        v /= 100.0
    return max(0.0, min(1.0, v))


def make_row(u, arm, model, draw, text, tin, tout, price, mult, served):
    j = last_json(text) or {}
    fok, nok = clamp(j.get("fok")), clamp(j.get("nok"))
    return {"unit_id": u["unit_id"], "arm": arm, "model": model, "draw": draw,
            "fok": fok, "nok": nok,
            "status": "OK" if fok is not None else "PARSE_FAIL",
            "served_model": served, "tok_in": tin, "tok_out": tout,
            "usd": (tin / 1e6 * price[0] + tout / 1e6 * price[1]) * mult,
            "text": (text or "")[:2000]}


def load_env():
    for line in io.open(ROOT / ".env", encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def anthropic_client():
    import anthropic
    return anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def call_once(lane, u, arm, draw):
    cfg = LANES[lane]
    sysm, user = prompts_for(u, arm)
    if cfg["vendor"] == "anthropic":
        kw = dict(model=lane, max_tokens=cfg["max_tokens"], system=sysm,
                  messages=[{"role": "user", "content": user}])
        if cfg["temp"] is not None:
            kw["temperature"] = cfg["temp"]
        r = anthropic_client().messages.create(**kw)
        text = "".join(b.text for b in r.content if b.type == "text")
        return make_row(u, arm, lane, draw, text, r.usage.input_tokens,
                        r.usage.output_tokens, cfg["price"], 1.0, r.model)
    from openai import OpenAI
    r = OpenAI().chat.completions.create(
        model=lane, temperature=cfg["temp"], max_tokens=cfg["max_tokens"],
        messages=[{"role": "system", "content": sysm}, {"role": "user", "content": user}])
    return make_row(u, arm, lane, draw, r.choices[0].message.content,
                    r.usage.prompt_tokens, r.usage.completion_tokens,
                    cfg["price"], 1.0, r.model)


def cmd_probe(lane):
    load_env()
    rows = [call_once(lane, units("BLIND")[0], "BLIND", 0),
            call_once(lane, units("INDEXED-V2")[0], "INDEXED-V2", 0),
            call_once(lane, units("INDEXED-V3")[0], "INDEXED-V3", 0)]
    ok = all(lane.split("-2025")[0] in r["served_model"] or lane in r["served_model"]
             for r in rows)
    rec = {"lane": lane, "served": rows[0]["served_model"], "identifier_ok": ok,
           "blind_in": rows[0]["tok_in"], "v2_in": rows[1]["tok_in"],
           "v3_in": rows[2]["tok_in"],
           "out": [r["tok_out"] for r in rows],
           "parsed": [r["status"] for r in rows],
           "sample": rows[1]["text"][:200]}
    d = json.load(io.open(PROBES, encoding="utf-8")) if PROBES.exists() else {}
    d[lane] = rec
    PROBES.parent.mkdir(parents=True, exist_ok=True)
    json.dump(d, io.open(PROBES, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(rec, indent=1))
    if not ok:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")


def cmd_project():
    d = json.load(io.open(PROBES, encoding="utf-8"))
    total = 0.0
    print(f"{'lane':30s} {'calls':>6s} {'in(M)':>7s} {'out(M)':>7s} {'batch':>6s} {'usd':>8s}")
    for lane, rec in sorted(d.items()):
        cfg = LANES[lane]
        k = cfg["k"]
        n = k * (len(BLIND_UNITS) + 2 * len(CELL))
        tin = k * (len(BLIND_UNITS) * rec["blind_in"]
                   + len(CELL) * (rec["v2_in"] + rec["v3_in"]))
        tout = n * max(1, sum(rec["out"]) / len(rec["out"]))
        usd = (tin / 1e6 * cfg["price"][0] + tout / 1e6 * cfg["price"][1]) * cfg["mult"]
        total += usd
        print(f"{lane:30s} {n:6d} {tin/1e6:7.3f} {tout/1e6:7.3f} "
              f"{cfg['mult']:6.1f} {usd:8.2f}")
    print(f"{'TOTAL projected':30s} {'':6s} {'':7s} {'':7s} {'':6s} {total:8.2f}")
    print(f"\nceiling $12.00   headroom ${12.0 - total:.2f}")
    if total > 12.0:
        sys.exit("PROJECTION EXCEEDS CEILING -- do not launch")


def rows_path(lane):
    return ROWS / f"rows_{LANES[lane]['code']}.jsonl"


def cmd_submit(lane):
    load_env()
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    cfg = LANES[lane]
    reqs = []
    for ai, arm in enumerate(ARMS):
        for i, u in enumerate(units(arm)):
            sysm, user = prompts_for(u, arm)
            for d in range(1, cfg["k"] + 1):
                kw = dict(model=lane, max_tokens=cfg["max_tokens"], system=sysm,
                          messages=[{"role": "user", "content": user}])
                if cfg["temp"] is not None:
                    kw["temperature"] = cfg["temp"]
                reqs.append(Request(custom_id=f"{cfg['code']}-{ai}-{i:04d}-d{d}",
                                    params=MessageCreateParamsNonStreaming(**kw)))
    b = anthropic_client().messages.batches.create(requests=reqs)
    ROWS.mkdir(parents=True, exist_ok=True)
    (ROWS / f"batch_{cfg['code']}.json").write_text(
        json.dumps({"id": b.id, "lane": lane, "n": len(reqs)}))
    print("submitted", b.id, len(reqs), "requests")


def cmd_poll(lane):
    load_env()
    cfg = LANES[lane]
    meta = json.loads((ROWS / f"batch_{cfg['code']}.json").read_text())
    cl = anthropic_client()
    b = cl.messages.batches.retrieve(meta["id"])
    print(meta["id"], b.processing_status, b.request_counts)
    if b.processing_status != "ended":
        return
    by = {ai: units(arm) for ai, arm in enumerate(ARMS)}
    n_ok = 0
    with io.open(rows_path(lane), "w", encoding="utf-8", newline="\n") as f:
        for res in cl.messages.batches.results(meta["id"]):
            code, ai, i, d = res.custom_id.split("-")
            arm = ARMS[int(ai)]
            u = by[int(ai)][int(i)]
            if res.result.type == "succeeded":
                m = res.result.message
                text = "".join(bl.text for bl in m.content if bl.type == "text")
                row = make_row(u, arm, lane, int(d[1:]), text, m.usage.input_tokens,
                               m.usage.output_tokens, cfg["price"], cfg["mult"], m.model)
                n_ok += 1
            else:
                row = {"unit_id": u["unit_id"], "arm": arm, "model": lane,
                       "draw": int(d[1:]), "status": "BATCH_" + res.result.type.upper()}
            f.write(json.dumps(row, sort_keys=True) + "\n")
    print("collected; ok:", n_ok)


def cmd_sync(lane):
    load_env()
    cfg = LANES[lane]
    ROWS.mkdir(parents=True, exist_ok=True)
    done = set()
    if rows_path(lane).exists():
        for line in io.open(rows_path(lane), encoding="utf-8"):
            r = json.loads(line)
            done.add((r["unit_id"], r["arm"], r["draw"]))
    jobs = [(u, arm, d) for arm in ARMS for u in units(arm)
            for d in range(1, cfg["k"] + 1) if (u["unit_id"], arm, d) not in done]
    print(f"{lane}: {len(jobs)} calls to go (resumed past {len(done)})")
    lock, spend = threading.Lock(), [0.0]

    def work(j):
        u, arm, d = j
        for attempt in (1, 2, 3):
            try:
                row = call_once(lane, u, arm, d)
                break
            except Exception as e:
                if attempt == 3:
                    row = {"unit_id": u["unit_id"], "arm": arm, "model": lane, "draw": d,
                           "status": f"ERROR:{type(e).__name__}"}
                else:
                    time.sleep(5 * attempt)
        with lock:
            spend[0] += row.get("usd", 0.0)
            with io.open(rows_path(lane), "a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(row, sort_keys=True) + "\n")
        return row

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for n, _ in enumerate(ex.map(work, jobs), 1):
            if n % 100 == 0:
                print(n, "/", len(jobs), f"lane-spend ${spend[0]:.4f}")
    print(f"{lane} DONE; session spend ${spend[0]:.4f}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "project":
        cmd_project()
    else:
        globals()["cmd_" + cmd](sys.argv[2])
