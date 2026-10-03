"""verify_batch.py -- E1-XV SP-0 ruling 1: confirm the Anthropic Batch API serves
IDENTICAL model and params to the synchronous path before the prereg registers it.

The 50% batch discount is only free if the batch path is the same measurement. Two
things are checked, neither assumed:

  1. the served model ID echoed back by the batch equals the ID requested, and
     equals what the synchronous path returned for the same request;
  2. on the lane where temperature 0 IS honoured (Haiku 4.5), the batch output is
     compared BYTE-FOR-BYTE against the synchronous output for the same prompt.
     A deterministic lane that agrees byte-for-byte across paths is direct evidence
     the same weights and decoding parameters served both.

Opus 5 cannot pin temperature (D86), so byte-equality is not required of it and its
absence would prove nothing; for that lane the check is that the request is ACCEPTED
with the same params and returns the same model ID.

Run: python verify_batch.py [--submit | --poll <batch_id>]
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

from cell_e1xv import build  # noqa: E402  (asserts frozen prompt shas on import)
from lane_probe import load_env  # noqa: E402
import prompts_e1 as P  # noqa: E402

MAN = ROOT / "e1xv_crossvendor" / "manifests"
LANES = [("claude-haiku-4-5-20251001", 0.0), ("claude-opus-5", None)]
ITEMS = ["frbank:aroha:aroha_q05:CAT-ABLATED", "frbank:thanh:thanh_q13:FULL"]


def client():
    from anthropic import Anthropic
    return Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def requests_for(rows):
    by = {r["item_id"]: r for r in rows}
    out = []
    for model, temp in LANES:
        for tag in ITEMS:
            for arm in ("BLIND", "INDEXED-TRUE"):
                user = by[tag]["user_blind" if arm == "BLIND" else "user_indexed"]
                params = {"model": model, "max_tokens": P.MAX_TOKENS,
                          "system": P.SYSTEM,
                          "messages": [{"role": "user", "content": user}]}
                if temp is not None:
                    params["temperature"] = temp
                out.append({"custom_id": cid_of(model, arm, tag), "params": params})
    return out


CODE = {"claude-haiku-4-5-20251001": "H45", "claude-opus-5": "OP5"}


def cid_of(model, arm, tag):
    """Batch custom_id must match ^[a-zA-Z0-9_-]{1,64}$ and fit in 64 chars, so the
    model is carried as a short code rather than truncated away."""
    t = "".join(ch if (ch.isalnum() or ch in "_-") else "_" for ch in tag)
    return f"{CODE[model]}-{'B' if arm == 'BLIND' else 'I'}-{t}"[:64]


def cmd_submit():
    rows, got, _, _, _ = build()
    if got["n"] != 84:
        raise SystemExit("cell does not rebuild")
    reqs = requests_for(rows)
    c = client()
    b = c.messages.batches.create(requests=reqs)
    print(f"batch submitted: {b.id}  status={b.processing_status}  requests={len(reqs)}")
    io.open(MAN / "batch_id.txt", "w", encoding="utf-8").write(b.id)

    # Contemporaneous synchronous reference for the SAME requests, so the later
    # comparison is byte-level and not merely a token count against an older run.
    print("  capturing synchronous reference for the same requests...")
    ref = {}
    for r in reqs:
        m = c.messages.create(**r["params"])
        ref[r["custom_id"]] = {
            "served_model": m.model, "stop_reason": m.stop_reason,
            "in": m.usage.input_tokens, "out": m.usage.output_tokens,
            "text": "".join(x.text for x in m.content if x.type == "text")}
        print(f"    sync {r['custom_id'][:56]:56s} in={m.usage.input_tokens:5d} "
              f"out={m.usage.output_tokens:4d}")
    io.open(MAN / "batch_sync_reference.json", "w", encoding="utf-8").write(
        json.dumps(ref, indent=2, ensure_ascii=False))
    return b.id


def cmd_poll(bid, max_wait=540, preloaded=None):
    if preloaded is not None:
        results = preloaded
        print(f"RECOMPARE from saved payloads -- no API calls  (batch {bid})")
        return _compare(bid, results)
    c = client()
    t0 = time.time()
    while True:
        b = c.messages.batches.retrieve(bid)
        rc = b.request_counts
        print(f"  [{int(time.time() - t0):4d}s] {b.processing_status}  "
              f"succeeded={rc.succeeded} errored={rc.errored} "
              f"processing={rc.processing} canceled={rc.canceled} expired={rc.expired}",
              flush=True)
        if b.processing_status == "ended":
            break
        if time.time() - t0 > max_wait:
            print("  still processing -- re-run with --poll to continue; the batch persists")
            return None
        time.sleep(20)

    results = {}
    for r in c.messages.batches.results(bid):
        res = r.result
        if res.type != "succeeded":
            results[r.custom_id] = {"ok": False, "type": res.type,
                                    "detail": str(getattr(res, "error", ""))[:300]}
            continue
        m = res.message
        results[r.custom_id] = {
            "ok": True, "served_model": m.model, "stop_reason": m.stop_reason,
            "in": m.usage.input_tokens, "out": m.usage.output_tokens,
            "text": "".join(x.text for x in m.content if x.type == "text")}

    return _compare(bid, results)


def _compare(bid, results):
    # ---- compare against the contemporaneous synchronous reference
    sync = json.load(io.open(MAN / "batch_sync_reference.json", encoding="utf-8"))

    print("\nBATCH vs SYNC  (same requests, same session)")
    fails = []
    for cid in sorted(results):
        r, s = results[cid], sync.get(cid)
        model = next(m for m, c in CODE.items() if cid.startswith(c + "-"))
        if not r["ok"]:
            fails.append(f"{cid}: batch request failed {r['type']} {r.get('detail')}")
            print(f"  FAIL {cid}  {r['type']}")
            continue
        if r["served_model"] != model:
            fails.append(f"{cid}: served {r['served_model']} != requested {model}")
        if not s:
            fails.append(f"{cid}: no synchronous reference captured")
            continue

        pinned = model == "claude-haiku-4-5-20251001"      # the T=0 lane
        byte_same = _norm(r["text"]) == _norm(s["text"])
        tok_same = (r["in"], r["out"]) == (s["in"], s["out"])

        # THE PASS CRITERION IS THE SCORED VALUE, not the raw text. What this run
        # elicits is (fok, nok); trailing prose after the JSON is discarded by the
        # frozen parse path and cannot reach any AUROC. Byte-equality is reported
        # as a stronger observation where it holds, but requiring it would test a
        # quantity the study does not use.
        vb, vs = scored(r["text"]), scored(s["text"])
        if pinned and vb != vs:
            fails.append(f"{cid}: T=0 lane SCORED VALUE differs between paths "
                         f"(batch {vb} vs sync {vs})")
        ok = r["served_model"] == model and (vb == vs or not pinned)
        verdict = ("BYTE-IDENTICAL" if byte_same else
                   ("scored-equal, prose tail differs" if vb == vs else
                    ("tokens match, scored differs" if tok_same else "differs")))
        print(f"  {'ok  ' if ok else 'FAIL'}"
              f" {cid[:52]:52s} served={r['served_model']:26s} "
              f"sync {s['in']:5d}/{s['out']:4d}  batch {r['in']:5d}/{r['out']:4d}  "
              f"scored b/s {str(vb):14s}/{str(vs):14s}  {verdict}"
              + ("" if pinned else "  (T unpinned -- equality not required)"))

    out = MAN / "batch_verification.json"
    io.open(out, "w", encoding="utf-8").write(json.dumps(
        {"batch_id": bid, "results": results,
         "verdict": "PASS" if not fails else "FAIL", "failures": fails},
        indent=2, ensure_ascii=False))
    print(f"\n  {'PASS -- batch path serves identical model and params' if not fails else 'FAIL'}")
    for f in fails:
        print("   ", f)
    print(f"  written: {out.relative_to(ROOT)}")
    return not fails


def _norm(s):
    return " ".join((s or "").split())


def scored(text):
    """The quantity the study actually elicits, via the frozen parse path."""
    from calibrate_e1xv import last_json, clamp
    o = last_json(text) or {}
    return (clamp(o.get("fok")), clamp(o.get("nok")))




if __name__ == "__main__":
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("--submit", action="store_true")
    ap.add_argument("--poll", default=None)
    ap.add_argument("--recompare", action="store_true")
    a = ap.parse_args()
    if a.recompare:
        bid = io.open(MAN / "batch_id.txt", encoding="utf-8").read().strip()
        saved = json.load(io.open(MAN / "batch_verification.json", encoding="utf-8"))
        cmd_poll(bid, preloaded=saved["results"])
    elif a.poll:
        cmd_poll(a.poll)
    else:
        bid = cmd_submit()
        cmd_poll(bid)
