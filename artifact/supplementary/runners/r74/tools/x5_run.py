"""R75 X5 -- monitor elicitation on the authorship-matched E1-NS cell (n=36).

Registration: ADDENDUM_R74 SX5 @ 35f8416a55 (incorporating PREREG_E1NS_DRAFT.md);
launch approved by [AUTHOR-1]'s registered in-session R75 ruling (D-R74-10 logged before
any call). Question surfaces are the ruling-(a) renders from r74/x5/x5_render.json
(transfer 36/36); the runner refuses to launch unless that gate reads PASS.

Lanes (prereg SS2 verbatim):
  gpt-4.1-mini   E1 protocol: temperature 0, seed 42, max_tokens 200; k=1 primary
                 plus a min(50,n)-item k=3 stability sample (n=36 -> all items,
                 draws 2 and 3); synchronous.
  claude-opus-5  E1-XV protocol: temperature omitted (D86), max_tokens 1024 (D91),
                 k=5, Batch API (D92); system-role assembly (D88).
Arms: BLIND and INDEXED-TRUE, index = the persona's committed frbank:{p}:FULL:TRUE.
Prompts byte-unchanged from frozen prompts_e1 (digests asserted). Parse: frozen E1
path (last JSON object; fok/nok clamped to [0,1]).

Subcommands: probe <lane> | project | submit | poll | sync | oracle
Rows: r74/x5/rows_{MINI,OP5}.jsonl, resume-keyed on (item_id, arm, draw).
"""
import json, os, pathlib, sys, time, threading, concurrent.futures

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import prompts_e1 as P
import api as _api
_api.load_env()

X5 = ROOT / "r74" / "x5"
X4 = ROOT / "r74" / "x4"

# frozen-prompt digests: same values the X4 cell file asserted
_c661 = json.load(open(X4 / "cell_661.json", encoding="utf-8"))
assert P.file_sha256() == _c661["prompts_file_sha256"], "prompts_e1 file digest drift"
assert P.texts_sha256() == _c661["prompts_texts_sha256"], "prompts_e1 texts digest drift"

R = json.load(open(X5 / "x5_render.json", encoding="utf-8"))
assert R["spot_check"]["verdict"] == "PASS" and R["spot_check"]["transfer_accuracy"] == 1.0, \
    "label-transfer gate not PASS -- monitor launch forbidden"
assert R["cell"]["n"] == 36 and R["cell"]["composition"] == {"ABSENT": 7, "PN": 12, "PRESENT": 17}

ITEMS = sorted(R["rows"], key=lambda r: r["item_id"])
for it in ITEMS:
    it["question"] = it["rendered_question"]
    it["y_fok"] = 0 if it["label"] == "ABSENT" else 1
    it["y_nok"] = 1 if it["label"] == "PN" else 0
    it["index_key"] = f"frbank:{it['persona']}:FULL:TRUE"

IDX = json.load(open(ROOT / "e1_metamemory" / "indexes_v2.json", encoding="utf-8"))["indexes"]
missing = [it["index_key"] for it in ITEMS if it["index_key"] not in IDX]
assert not missing, f"missing committed indexes: {missing}"

LANES = {
    "gpt-4.1-mini":  dict(vendor="openai_mini", code="MINI", max_tokens=P.MAX_TOKENS,
                          draws=(1, 2, 3), price=(0.40, 1.60), mult=1.0),
    "claude-opus-5": dict(vendor="anthropic", code="OP5", max_tokens=1024,
                          draws=(1, 2, 3, 4, 5), price=(5.00, 25.00), mult=0.5),
}

def prompts_for(it, arm):
    user = (P.USER_INDEXED.format(index=IDX[it["index_key"]], question=it["question"])
            if arm == "INDEXED-TRUE" else P.USER_BLIND.format(question=it["question"]))
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

def call_once(lane, it, arm, draw):
    cfg = LANES[lane]
    sysm, user = prompts_for(it, arm)
    if cfg["vendor"] == "anthropic":
        cl = anthropic_client()
        r = cl.messages.create(model=lane, max_tokens=cfg["max_tokens"], system=sysm,
                               messages=[{"role": "user", "content": user}])
        text = "".join(b.text for b in r.content if b.type == "text")
        return make_row(it, arm, lane, draw, text, r.usage.input_tokens,
                        r.usage.output_tokens, cfg["price"], 1.0, r.model)
    from openai import OpenAI
    cl = OpenAI()
    r = cl.chat.completions.create(model=lane, temperature=P.TEMPERATURE, seed=P.SEED,
                                   max_tokens=cfg["max_tokens"],
                                   messages=[{"role": "system", "content": sysm},
                                             {"role": "user", "content": user}])
    text = r.choices[0].message.content
    return make_row(it, arm, lane, draw, text, r.usage.prompt_tokens,
                    r.usage.completion_tokens, cfg["price"], 1.0, r.model)

PROBES = X5 / "x5_probes.json"

def cmd_probe(lane):
    it = ITEMS[0]
    rows = [call_once(lane, it, "BLIND", 0), call_once(lane, it, "INDEXED-TRUE", 0)]
    ok_id = all(lane in r["served_model"] or r["served_model"].startswith(lane)
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
        k = len(cfg["draws"])
        n = len(ITEMS) * 2 * k
        tin = len(ITEMS) * k * (rec["blind_in"] + rec["indexed_in"])
        tout = n * max(1, sum(rec["out"]) / len(rec["out"]))
        usd = (tin / 1e6 * cfg["price"][0] + tout / 1e6 * cfg["price"][1]) * cfg["mult"]
        total += usd
        print(f"{lane:16s} calls={n} proj_in={tin/1e3:.1f}k proj_out={tout/1e3:.2f}k "
              f"batch_mult={cfg['mult']} -> ${usd:,.2f}")
    print(f"TOTAL projected: ${total:,.2f}")

def rows_path(lane):
    return X5 / f"rows_{LANES[lane]['code']}.jsonl"

def done_keys(lane):
    pth = rows_path(lane)
    ks = set()
    if pth.exists():
        for line in open(pth, encoding="utf-8"):
            r = json.loads(line)
            ks.add((r["item_id"], r["arm"], r["draw"]))
    return ks

def cmd_submit(lane="claude-opus-5"):
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    cfg = LANES[lane]
    reqs = []
    for i, it in enumerate(ITEMS):
        for arm, tag in (("BLIND", "B"), ("INDEXED-TRUE", "I")):
            sysm, user = prompts_for(it, arm)
            for d in cfg["draws"]:
                reqs.append(Request(
                    custom_id=f"X5-{tag}-{i:02d}-d{d}",
                    params=MessageCreateParamsNonStreaming(
                        model=lane, max_tokens=cfg["max_tokens"], system=sysm,
                        messages=[{"role": "user", "content": user}])))
    b = anthropic_client().messages.batches.create(requests=reqs)
    (X5 / "batch_OP5.json").write_text(json.dumps({"id": b.id, "lane": lane}))
    print("submitted", b.id, len(reqs), "requests")

def cmd_poll(lane="claude-opus-5"):
    cfg = LANES[lane]
    meta = json.loads((X5 / "batch_OP5.json").read_text())
    cl = anthropic_client()
    b = cl.messages.batches.retrieve(meta["id"])
    print(meta["id"], b.processing_status, b.request_counts)
    if b.processing_status != "ended":
        return
    n_ok = 0
    with open(rows_path(lane), "w", encoding="utf-8") as f:
        for res in cl.messages.batches.results(meta["id"]):
            _, tag, i, d = res.custom_id.split("-")
            it = ITEMS[int(i)]
            arm = "BLIND" if tag == "B" else "INDEXED-TRUE"
            if res.result.type == "succeeded":
                m = res.result.message
                text = "".join(bl.text for bl in m.content if bl.type == "text")
                row = make_row(it, arm, lane, int(d[1:]), text, m.usage.input_tokens,
                               m.usage.output_tokens, cfg["price"], cfg["mult"], m.model)
                n_ok += 1
            else:
                row = {"item_id": it["item_id"], "arm": arm, "model": lane,
                       "draw": int(d[1:]), "status": "BATCH_" + res.result.type.upper()}
            f.write(json.dumps(row, sort_keys=True) + "\n")
    print("collected; ok:", n_ok)

def cmd_sync(lane="gpt-4.1-mini"):
    cfg = LANES[lane]
    done = done_keys(lane)
    jobs = [(it, arm, d) for it in ITEMS for arm in ("BLIND", "INDEXED-TRUE")
            for d in cfg["draws"] if (it["item_id"], arm, d) not in done]
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
                    row = {"item_id": it["item_id"], "arm": arm, "model": lane,
                           "draw": d, "status": f"ERROR:{type(e).__name__}"}
                else:
                    time.sleep(5 * attempt)
        with lock:
            spend[0] += row.get("usd", 0.0)
            with open(rows_path(lane), "a", encoding="utf-8") as f:
                f.write(json.dumps(row, sort_keys=True) + "\n")
        return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(work, jobs))
    print(f"{lane} DONE; session spend ${spend[0]:.4f}")

def cmd_oracle(_=None):
    """Index-oracle disclosure re-derived on the definite n=36 cell: does the
    persona's index name the question's slot under ATTRIBUTE NAMES CARRYING
    SUPERSEDED CONTENT? (prereg SS2 disclosure; registered 99-cell value 0.5379)."""
    sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
    from score_e1 import auroc
    hits, scores, y = [], [], []
    for it in ITEMS:
        txt = IDX[it["index_key"]]
        tail = txt.split("ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT")[-1]
        hit = it["slot"] in tail
        hits.append((it["item_id"], it["label"], hit))
        scores.append(1.0 if hit else 0.0)
        y.append(it["y_nok"])
    a = auroc(scores, y)
    npn = sum(1 for _, lab, h in hits if lab == "PN" and h)
    print(f"oracle AUROC on n=36: {a:.4f}; PN slots named: {npn}/12; "
          f"total named: {sum(1 for *_, h in hits if h)}/36")
    json.dump({"auroc": a, "pn_named": npn, "rows": hits},
              open(X5 / "x5_oracle.json", "w", encoding="utf-8"), indent=1)

if __name__ == "__main__":
    cmd = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    fn = globals()["cmd_" + cmd]
    fn(arg) if arg or cmd in ("probe",) else fn()
