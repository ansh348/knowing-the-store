"""R74 X4 -- multi-lane elicitation on the 661-item expansion cell (ADDENDUM_R74 SX4).

Subcommands:
  probe <lane>    one blind+one indexed call; assert served model id (E1.7 rule); record tokens
  project         per-lane cost projection from probes.json (report BEFORE launch)
  submit <lane>   Anthropic lanes: submit one Batch (661 items x 2 arms x k=5)
  poll <lane>     Anthropic lanes: poll batch; when ended, collect rows
  sync <lane>     K3 / luna / sol: synchronous run with jsonl resume
Frozen: prompts_e1 verbatim (digests asserted via cell file), k=5, MIN_DRAWS=3 at scoring.
Lane disclosures: Opus 5 omits temperature (D86), Haiku temp 0, K3 temp 1.0 +
max_tokens 4096 (D87), Moonshot direct (D90), Opus ceiling 1024 (D91).
"""
import json, os, pathlib, sys, time, threading, concurrent.futures

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import prompts_e1 as P
import api as _api
_api.load_env()

X4 = ROOT / "r74" / "x4"
CELL = json.load(open(X4 / "cell_661.json", encoding="utf-8"))
assert P.file_sha256() == CELL["prompts_file_sha256"] and P.texts_sha256() == CELL["prompts_texts_sha256"]
ITEMS = CELL["items"]
IDX = json.load(open(ROOT / "e1_metamemory" / "indexes_v2.json", encoding="utf-8"))["indexes"]
K = 5

LANES = {
    "claude-opus-5":             dict(vendor="anthropic", code="OP5", temp=None, max_tokens=1024, price=(5.00, 25.00), mult=0.5),
    "claude-haiku-4-5-20251001": dict(vendor="anthropic", code="H45", temp=0.0,  max_tokens=200,  price=(1.00, 5.00),  mult=0.5),
    "kimi-k3":                   dict(vendor="moonshot",  code="K3",  temp=1.0,  max_tokens=4096, price=(3.00, 15.00), mult=1.0),
    "gpt-5.6-luna":              dict(vendor="openai",    code="LUNA", temp=None, max_tokens=2048, price=(0.20, 1.20), mult=1.0),
    "gpt-5.6-sol":               dict(vendor="openai",    code="SOL",  temp=None, max_tokens=2048, price=(5.00, 30.00), mult=1.0),
}

def prompts_for(it, arm):
    q = it["question"]
    user = (P.USER_INDEXED.format(index=IDX[it["index_key"]], question=q)
            if arm == "INDEXED-TRUE" else P.USER_BLIND.format(question=q))
    return P.SYSTEM, user

def last_json(text):
    depth, start, best, ins, esc = 0, None, None, False, False
    for i, ch in enumerate(text or ""):
        if ins:
            ins = not (ch == '"' and not esc); esc = (ch == "\\" and not esc)
            continue
        if ch == '"': ins, esc = True, False
        elif ch == "{":
            if depth == 0: start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None: best = text[start:i + 1]
    try:
        return json.loads(best) if best else None
    except Exception:
        return None

def clamp(v):
    try: v = float(v)
    except (TypeError, ValueError): return None
    if v > 1: v /= 100.0
    return max(0.0, min(1.0, v))

def make_row(it, arm, model, draw, text, tin, tout, price, mult, served):
    j = last_json(text) or {}
    fok, nok = clamp(j.get("fok")), clamp(j.get("nok"))
    return {"item_id": it["item_id"], "arm": arm, "model": model, "draw": draw,
            "label": it["label"], "y_fok": it["y_fok"], "y_nok": it["y_nok"],
            "fok": fok, "nok": nok, "status": "OK" if fok is not None else "PARSE_FAIL",
            "served_model": served, "tok_in": tin, "tok_out": tout,
            "usd": (tin / 1e6 * price[0] + tout / 1e6 * price[1]) * mult,
            "text": (text or "")[:4000]}

def anthropic_client():
    import anthropic
    return anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def openai_client(vendor):
    from openai import OpenAI
    if vendor == "moonshot":
        return OpenAI(api_key=os.environ["MOONSHOT_API_KEY"], base_url="https://api.moonshot.ai/v1")
    return OpenAI()

def call_once(lane, it, arm, draw):
    cfg = LANES[lane]
    sysm, user = prompts_for(it, arm)
    if cfg["vendor"] == "anthropic":
        cl = anthropic_client()
        kw = dict(model=lane, max_tokens=cfg["max_tokens"], system=sysm,
                  messages=[{"role": "user", "content": user}])
        if cfg["temp"] is not None: kw["temperature"] = cfg["temp"]
        r = cl.messages.create(**kw)
        text = "".join(b.text for b in r.content if b.type == "text")
        return make_row(it, arm, lane, draw, text, r.usage.input_tokens, r.usage.output_tokens,
                        cfg["price"], 1.0, r.model)
    cl = openai_client(cfg["vendor"])
    kw = dict(model=lane, messages=[{"role": "system", "content": sysm},
                                    {"role": "user", "content": user}])
    if cfg["vendor"] == "moonshot":
        kw.update(temperature=cfg["temp"], max_tokens=cfg["max_tokens"])
    else:
        kw.update(max_completion_tokens=cfg["max_tokens"])
    r = cl.chat.completions.create(**kw)
    text = r.choices[0].message.content
    return make_row(it, arm, lane, draw, text, r.usage.prompt_tokens, r.usage.completion_tokens,
                    cfg["price"], 1.0, r.model)

PROBES = X4 / "probes.json"

def cmd_probe(lane):
    it = ITEMS[0]
    rows = [call_once(lane, it, "BLIND", 0), call_once(lane, it, "INDEXED-TRUE", 0)]
    ok_id = all(r["served_model"].startswith(lane.split("-2025")[0]) or lane in r["served_model"]
                for r in rows)
    rec = {"lane": lane, "served": rows[0]["served_model"], "identifier_ok": ok_id,
           "blind_in": rows[0]["tok_in"], "indexed_in": rows[1]["tok_in"],
           "out": [rows[0]["tok_out"], rows[1]["tok_out"]],
           "parsed": [r["status"] for r in rows],
           "sample": rows[1]["text"][:200]}
    d = json.load(open(PROBES, encoding="utf-8")) if PROBES.exists() else {}
    d[lane] = rec
    json.dump(d, open(PROBES, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(rec, indent=1))
    if not ok_id: sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")

def cmd_project():
    d = json.load(open(PROBES, encoding="utf-8"))
    total = 0.0
    for lane, rec in d.items():
        cfg = LANES[lane]
        n = len(ITEMS) * 2 * K
        tin = len(ITEMS) * K * (rec["blind_in"] + rec["indexed_in"])
        tout = n * max(1, sum(rec["out"]) / len(rec["out"]))
        usd = (tin / 1e6 * cfg["price"][0] + tout / 1e6 * cfg["price"][1]) * cfg["mult"]
        total += usd
        print(f"{lane:28s} calls={n} proj_in={tin/1e6:.1f}M proj_out={tout/1e6:.2f}M "
              f"batch_mult={cfg['mult']} -> ${usd:,.2f}")
    print(f"TOTAL projected: ${total:,.2f}")

def rows_path(lane):
    return X4 / f"rows_{LANES[lane]['code']}.jsonl"

def done_keys(lane):
    pth = rows_path(lane)
    ks = set()
    if pth.exists():
        for line in open(pth, encoding="utf-8"):
            r = json.loads(line)
            ks.add((r["item_id"], r["arm"], r["draw"]))
    return ks

def cmd_submit(lane):
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    cfg = LANES[lane]
    reqs = []
    for i, it in enumerate(ITEMS):
        for arm, tag in (("BLIND", "B"), ("INDEXED-TRUE", "I")):
            sysm, user = prompts_for(it, arm)
            for d in range(1, K + 1):
                kw = dict(model=lane, max_tokens=cfg["max_tokens"], system=sysm,
                          messages=[{"role": "user", "content": user}])
                if cfg["temp"] is not None: kw["temperature"] = cfg["temp"]
                reqs.append(Request(custom_id=f"{cfg['code']}-{tag}-{i:04d}-d{d}",
                                    params=MessageCreateParamsNonStreaming(**kw)))
    b = anthropic_client().messages.batches.create(requests=reqs)
    (X4 / f"batch_{cfg['code']}.json").write_text(json.dumps({"id": b.id, "lane": lane}))
    print("submitted", b.id, len(reqs), "requests")

def cmd_poll(lane):
    cfg = LANES[lane]
    meta = json.loads((X4 / f"batch_{cfg['code']}.json").read_text())
    cl = anthropic_client()
    b = cl.messages.batches.retrieve(meta["id"])
    print(meta["id"], b.processing_status, b.request_counts)
    if b.processing_status != "ended":
        return
    by_i = {i: it for i, it in enumerate(ITEMS)}
    n_ok = 0
    with open(rows_path(lane), "w", encoding="utf-8") as f:
        for res in cl.messages.batches.results(meta["id"]):
            code, tag, i, d = res.custom_id.split("-")
            it = by_i[int(i)]
            arm = "BLIND" if tag == "B" else "INDEXED-TRUE"
            if res.result.type == "succeeded":
                m = res.result.message
                text = "".join(bl.text for bl in m.content if bl.type == "text")
                row = make_row(it, arm, lane, int(d[1:]), text, m.usage.input_tokens,
                               m.usage.output_tokens, cfg["price"], cfg["mult"], m.model)
                n_ok += 1
            else:
                row = {"item_id": it["item_id"], "arm": arm, "model": lane, "draw": int(d[1:]),
                       "status": "BATCH_" + res.result.type.upper()}
            f.write(json.dumps(row, sort_keys=True) + "\n")
    print("collected; ok:", n_ok)

def cmd_sync(lane):
    cfg = LANES[lane]
    done = done_keys(lane)
    jobs = [(it, arm, d) for it in ITEMS for arm in ("BLIND", "INDEXED-TRUE")
            for d in range(1, K + 1) if (it["item_id"], arm, d) not in done]
    print(f"{lane}: {len(jobs)} calls to go (resumed past {len(done)})")
    lock = threading.Lock()
    spend = [0.0]
    def work(j):
        it, arm, d = j
        for attempt in (1, 2, 3):
            try:
                row = call_once(lane, it, arm, d)
                break
            except Exception as e:
                if attempt == 3:
                    row = {"item_id": it["item_id"], "arm": arm, "model": lane, "draw": d,
                           "status": f"ERROR:{type(e).__name__}"}
                else:
                    time.sleep(5 * attempt)
        with lock:
            spend[0] += row.get("usd", 0.0)
            with open(rows_path(lane), "a", encoding="utf-8") as f:
                f.write(json.dumps(row, sort_keys=True) + "\n")
        return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        n = 0
        for _ in ex.map(work, jobs):
            n += 1
            if n % 500 == 0:
                print(n, "/", len(jobs), f"lane-spend ${spend[0]:.2f}")
    print(f"{lane} DONE; session spend ${spend[0]:.2f}")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "project": cmd_project()
    else: globals()["cmd_" + cmd](sys.argv[2])
