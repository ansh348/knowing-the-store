"""
mechanism_run.py -- E1.8 STEP 2: elicit the A1/A2/A3 mechanism arms.

Per E1_8_ADDENDUM.md (281c410), committed before any A1/A2/A3 call.

  lane      gpt-4.1-mini only. No frontier call.
  prompt    frozen prompts_e1.USER_INDEXED, UNCHANGED. Only the index text
            differs between arms. The texts sha is verified at start.
  decoding  temperature 0, seed 42, max_tokens 200 (frozen).
  draws     k = 1, licensed by the lane's measured k=3 stability (46/50
            identical, mean spread 0.012).
  cache     (item_id, arm, model, prompt_hash) -- E1's cache, not E0's.
  cap       $5 for this step; checked live, raises rather than continuing.

Per-call wall time is recorded here. E1 instrumented no per-call timing
anywhere (see ECONOMICS.md section 4); this run closes that gap for the mini
indexed arm at 12 workers.

Usage:  python e1_metamemory/tools/mechanism_run.py
"""

from __future__ import annotations

import collections
import concurrent.futures as cf
import io
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"

# ORDER MATTERS. elicit_e1.py inserts E0's tools dir last and so imports E0's
# `api` by accident (D25-E1). E1's dir goes in last here, so it wins.
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import api                       # noqa: E402  (E1's adapter)
import prompts_e1 as P           # noqa: E402

EXPECTED_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"
ARMS = ("A1-counts-jittered", "A2-counts-coarsened", "A3-names-only")
SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}
WORKERS = 12
STEP_CAP_USD = 5.00
OUT = E1 / "mechanism_elicitation.json"


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def clamp(v):
    try:
        return min(100.0, max(0.0, float(v))) / 100.0
    except (TypeError, ValueError):
        return None


class StepCapExceeded(RuntimeError):
    pass


def arm_spend_from_cache():
    """Cumulative spend on the three arms, summed over cached responses.

    The ledger holds ONE process's meter and is overwritten on every flush, so
    it cannot bound a resumed run. Summing the cache is re-run invariant and is
    the same device `ladder_L0.json` uses for `ladder_cost`. Needed because a
    DNS drop killed the first attempt at 1,111/1,764 calls (D27-E1).
    """
    p = E1 / "cache" / "responses.json"
    if not p.exists():
        return 0.0, 0
    tin = tout = n = 0
    for r in jload(p).values():
        if str(r.get("arm", "")).split("#")[0] in ARMS:
            tin += r.get("prompt_tokens", 0)
            tout += r.get("completion_tokens", 0)
            n += 1
    return tin / 1e6 * api.PRICE_IN + tout / 1e6 * api.PRICE_OUT, n


def main():
    got = P.texts_sha256()
    if got != EXPECTED_TEXTS_SHA:
        raise SystemExit(f"FROZEN PROMPT MISMATCH: {got} != {EXPECTED_TEXTS_SHA}")
    print(f"frozen prompt texts sha verified: {got[:16]}...")
    prior_usd, prior_n = arm_spend_from_cache()
    if prior_n:
        print(f"resuming: {prior_n} arm responses already cached, ${prior_usd:.4f} "
              f"already spent on this step")

    mech = jload(E1 / "mechanism_indexes.json")["indexes"]
    items = [i for i in jload(E1 / "build" / "items_final.json")
             if i["tier"] == "hard" and i.get("label", i["label_pre"]) in SCOREABLE]
    qmap = {r["tag"]: r["question"] for r in jload(E1 / "elicitation_main.json")
            if r["arm"] != "BLIND"}

    def ikey(it):
        b, p, v = it["backend"], it["persona"], it["variant"]
        return (f"{b}:{p}:SLOT:{it['question_id']}:TRUE" if v == "SLOT-ABLATED"
                else f"{b}:{p}:{v}:TRUE")

    jobs = []
    for it in items:
        q = qmap.get(it["item_id"])
        k = ikey(it)
        assert q, f"no question text for {it['item_id']}"
        assert k in mech, f"no mechanism index for {k}"
        for arm in ARMS:
            jobs.append((it["item_id"], arm, mech[k][arm], q,
                         it.get("label", it["label_pre"]), it["backend"], it["variant"]))
    print(f"{len(items)} hard-tier items x {len(ARMS)} arms = {len(jobs)} calls")

    def run(job):
        tag, arm, index, q, label, backend, variant = job
        msgs = [{"role": "system", "content": P.SYSTEM},
                {"role": "user", "content": P.USER_INDEXED.format(index=index,
                                                                 question=q)}]
        t0 = time.perf_counter()
        r = api.call(tag, arm, msgs)
        dt = time.perf_counter() - t0
        o = api.parse_json(r["content"])
        failed = False
        if o is None or clamp(o.get("fok")) is None:
            r = api.call(tag, arm + "#retry", msgs)
            o = api.parse_json(r["content"])
            if o is None or clamp(o.get("fok")) is None:
                failed, o = True, {}
        if prior_usd + api.meter()["usd"] > STEP_CAP_USD:
            raise StepCapExceeded(
                f"${prior_usd + api.meter()['usd']:.2f} cumulative over the "
                f"${STEP_CAP_USD} E1.8 step cap")
        return {"item_id": tag, "arm": arm, "label": label, "backend": backend,
                "variant": variant, "question": q,
                "fok": clamp(o.get("fok")), "nok": clamp(o.get("nok")),
                "nok_candidates_found": (bool(o.get("nok_candidates_found"))
                                         if not failed else None),
                "status": "ELICITATION_FAILED" if failed else "OK",
                "cached": r["cached"],
                "seconds": (None if r["cached"] else round(dt, 4)),
                "prompt_tokens": r.get("prompt_tokens"),
                "completion_tokens": r.get("completion_tokens")}

    out = []
    try:
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
            for n, rec in enumerate(ex.map(run, jobs), 1):
                out.append(rec)
                if n % 300 == 0:
                    api.flush()
                    print(f"  {n}/{len(jobs)}  ${api.meter()['usd']:.4f}", flush=True)
    finally:
        api.flush()

    jdump(out, OUT)
    m = api.meter()
    ok = collections.Counter((r["arm"], r["status"]) for r in out)
    lat = sorted(r["seconds"] for r in out if r["seconds"] is not None)
    print("\n" + "=" * 88)
    for arm in ARMS:
        print(f"  {arm:22s} OK {ok[(arm, 'OK')]:4d}  "
              f"FAILED {ok[(arm, 'ELICITATION_FAILED')]:3d}")
    total_usd, total_n = arm_spend_from_cache()
    print(f"  this process: live {m['calls']} / cached {m['cached']}; "
          f"tokens {m['in']} in / {m['out']} out; ${m['usd']:.4f}")
    print(f"  STEP TOTAL (summed over {total_n} cached arm responses, re-run "
          f"invariant): ${total_usd:.4f}  (cap ${STEP_CAP_USD})")
    if lat:
        print(f"  measured per-call latency, {WORKERS} workers: n={len(lat)} "
              f"mean {sum(lat)/len(lat):.3f}s  median {lat[len(lat)//2]:.3f}s  "
              f"p95 {lat[int(len(lat)*0.95)]:.3f}s  max {lat[-1]:.3f}s")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
