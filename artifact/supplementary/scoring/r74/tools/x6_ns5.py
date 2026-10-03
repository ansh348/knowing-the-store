"""R76 NS-5 -- Haiku 4.5 lane on the authorship-matched E1-NS cell (n=36).

Registration: ADDENDUM_R76 §A3 @ the R76-A freeze (692e379bdc), branch sentences
amended pre-launch per D-R74-14. This is the third lane on the SAME cell the R75 X5
run measured: the ruling-(a) renders in r74/x5/x5_render.json, byte-unchanged. No
re-render, no re-check -- the runner refuses to launch unless the committed transfer
gate still reads PASS at 36/36.

Lane (committed X4 configuration, verbatim):
  claude-haiku-4-5-20251001   E1-XV protocol: temperature 0.0 (D86 -- Haiku accepts the
                              frozen temperature), max_tokens 200, k=5, Batch API (D92),
                              system-role assembly (D88), price (1.00, 5.00) x 0.5 batch.
Arms: BLIND and INDEXED-TRUE, index = the persona's committed frbank:{p}:FULL:TRUE.
Prompts byte-unchanged from frozen prompts_e1 (both digests asserted). Parse: frozen E1
path (last JSON object; fok/nok clamped to [0,1]).

Subcommands: probe | project | submit | poll
Rows: r74/x6/rows_H45.jsonl
"""
import json, os, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import prompts_e1 as P
import api as _api
_api.load_env()

X4 = ROOT / "r74" / "x4"
X5 = ROOT / "r74" / "x5"
X6 = ROOT / "r74" / "x6"
X6.mkdir(parents=True, exist_ok=True)

# frozen-prompt digests: the same values the X4 and X5 runners asserted
_c661 = json.load(open(X4 / "cell_661.json", encoding="utf-8"))
assert P.file_sha256() == _c661["prompts_file_sha256"], "prompts_e1 file digest drift"
assert P.texts_sha256() == _c661["prompts_texts_sha256"], "prompts_e1 texts digest drift"

# the cell is the committed X5 cell, unchanged; gate must still read PASS
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

LANE = "claude-haiku-4-5-20251001"
CFG = dict(code="H45", temp=0.0, max_tokens=200, price=(1.00, 5.00), mult=0.5,
           draws=(1, 2, 3, 4, 5))
PROBES = X6 / "ns5_probes.json"
BATCH = X6 / "batch_H45.json"


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


def make_row(it, arm, draw, text, tin, tout, served, mult):
    j = last_json(text) or {}
    fok, nok = clamp(j.get("fok")), clamp(j.get("nok"))
    return {"item_id": it["item_id"], "arm": arm, "model": LANE, "draw": draw,
            "label": it["label"], "y_fok": it["y_fok"], "y_nok": it["y_nok"],
            "fok": fok, "nok": nok, "status": "OK" if fok is not None else "PARSE_FAIL",
            "served_model": served, "tok_in": tin, "tok_out": tout,
            "usd": (tin / 1e6 * CFG["price"][0] + tout / 1e6 * CFG["price"][1]) * mult,
            "text": (text or "")[:4000]}


def anthropic_client():
    import anthropic
    return anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def cmd_probe():
    """Two sync calls (blind + indexed) on item 0; E1.7 identifier check before launch."""
    cl = anthropic_client()
    rows = []
    for arm in ("BLIND", "INDEXED-TRUE"):
        sysm, user = prompts_for(ITEMS[0], arm)
        r = cl.messages.create(model=LANE, max_tokens=CFG["max_tokens"],
                               temperature=CFG["temp"], system=sysm,
                               messages=[{"role": "user", "content": user}])
        text = "".join(b.text for b in r.content if b.type == "text")
        rows.append(make_row(ITEMS[0], arm, 0, text, r.usage.input_tokens,
                             r.usage.output_tokens, r.model, 1.0))
    ok_id = all(LANE in r["served_model"] or r["served_model"].startswith(LANE)
                for r in rows)
    rec = {"lane": LANE, "served": rows[0]["served_model"], "identifier_ok": ok_id,
           "blind_in": rows[0]["tok_in"], "indexed_in": rows[1]["tok_in"],
           "out": [rows[0]["tok_out"], rows[1]["tok_out"]],
           "parsed": [r["status"] for r in rows],
           "probe_usd": round(sum(r["usd"] for r in rows), 6),
           "sample": rows[1]["text"][:200]}
    json.dump(rec, open(PROBES, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(rec, indent=1))
    if not ok_id:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")
    if any(s != "OK" for s in rec["parsed"]):
        sys.exit("PROBE PARSE FAILURE -- do not launch; this needs a D-entry, not a retry")


def cmd_project():
    """Report the projection BEFORE submission (ADDENDUM_R76 §A3 projection rule)."""
    rec = json.load(open(PROBES, encoding="utf-8"))
    k = len(CFG["draws"])
    calls = len(ITEMS) * 2 * k
    tin = len(ITEMS) * k * (rec["blind_in"] + rec["indexed_in"])
    mean_out = max(1.0, sum(rec["out"]) / len(rec["out"]))
    print(f"lane            : {LANE}")
    print(f"served (probe)  : {rec['served']}   identifier_ok={rec['identifier_ok']}")
    print(f"calls           : {calls}  ({len(ITEMS)} items x 2 arms x k={k})")
    print(f"projected input : {tin:,} tok   (blind {rec['blind_in']} + indexed "
          f"{rec['indexed_in']} per item-draw)")
    for label, mo in (("probe mean", mean_out), ("max_tokens ceiling",
                                                 float(CFG["max_tokens"]))):
        tout = calls * mo
        usd = (tin / 1e6 * CFG["price"][0] + tout / 1e6 * CFG["price"][1]) * CFG["mult"]
        print(f"  out@{label:<19s} {mo:6.1f} tok/call -> {tout:9,.0f} tok  ${usd:.4f}")
    print(f"registered ceiling for this lane: $0.47   pass budget: <= $0.47")


def cmd_submit():
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    assert not BATCH.exists(), f"{BATCH} exists -- a batch was already submitted"
    reqs = []
    for i, it in enumerate(ITEMS):
        for arm, tag in (("BLIND", "B"), ("INDEXED-TRUE", "I")):
            sysm, user = prompts_for(it, arm)
            for d in CFG["draws"]:
                reqs.append(Request(
                    custom_id=f"NS5-{tag}-{i:02d}-d{d}",
                    params=MessageCreateParamsNonStreaming(
                        model=LANE, max_tokens=CFG["max_tokens"],
                        temperature=CFG["temp"], system=sysm,
                        messages=[{"role": "user", "content": user}])))
    b = anthropic_client().messages.batches.create(requests=reqs)
    BATCH.write_text(json.dumps({"id": b.id, "lane": LANE, "n_requests": len(reqs)}))
    print("submitted", b.id, len(reqs), "requests")


def cmd_poll():
    meta = json.loads(BATCH.read_text())
    cl = anthropic_client()
    b = cl.messages.batches.retrieve(meta["id"])
    print(meta["id"], b.processing_status, b.request_counts)
    if b.processing_status != "ended":
        return
    n_ok, spend = 0, 0.0
    with open(X6 / "rows_H45.jsonl", "w", encoding="utf-8") as f:
        for res in cl.messages.batches.results(meta["id"]):
            _, tag, i, d = res.custom_id.split("-")
            it = ITEMS[int(i)]
            arm = "BLIND" if tag == "B" else "INDEXED-TRUE"
            if res.result.type == "succeeded":
                m = res.result.message
                text = "".join(bl.text for bl in m.content if bl.type == "text")
                row = make_row(it, arm, int(d[1:]), text, m.usage.input_tokens,
                               m.usage.output_tokens, m.model, CFG["mult"])
                n_ok += 1
                spend += row["usd"]
            else:
                row = {"item_id": it["item_id"], "arm": arm, "model": LANE,
                       "draw": int(d[1:]), "status": "BATCH_" + res.result.type.upper()}
            f.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"collected; ok: {n_ok}/{meta['n_requests']}  billed ${spend:.4f}")


if __name__ == "__main__":
    globals()["cmd_" + sys.argv[1]]()
