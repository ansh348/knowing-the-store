"""
elicit_e1.py -- E1 Phase C: elicitation across all arms.

Frozen plan (PREREG_E1 section 7):
  BLIND            one draw per UNIQUE PROMPT HASH, shared across variants and
                   backends (E0 D19: keying on item_id paid twice and got two
                   different answers on a byte-identical prompt).
  INDEXED-TRUE     per backend, per item.
  INDEXED-BELIEVED per backend, per item.
  k=3 subsample    ~50 questions, three independent blind draws, to quantify the
                   residual nondeterminism the prompt-hash cache cannot remove.
  staircase        ~150 items, FR-Bank TRUE only, four binary thresholds instead
                   of a number, to break the D20 quantisation.

Elicitation runs on SCOREABLE items only. UNRESOLVED items are excluded from every
metric by pre-elicitation rule, so eliciting them would buy nothing. Logged as D16.

Transient faults (parse failure, timeout, rate limit) are retried with backoff,
cached and logged -- routine, per the continuation instruction. A second parse
failure marks the item ELICITATION_FAILED and it is counted, never imputed.

Usage:  python e1_metamemory/tools/elicit_e1.py [--limit N]
"""

from __future__ import annotations

import collections
import concurrent.futures as cf
import io
import json
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))

import api                       # noqa: E402  (E1's adapter: E1 cache, frozen params)
import prompts_e1 as P           # noqa: E402
from e0_common import load_joins  # noqa: E402

SEED = 42
K_QUESTIONS = 50
STAIRCASE_N = 150
SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def clamp(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return min(100.0, max(0.0, f)) / 100.0


def index_key(it):
    """Key into indexes_v2.json. SLOT-ABLATED is per-question."""
    b, p, v = it["backend"], it["persona"], it["variant"]
    if v == "SLOT-ABLATED":
        return f"{b}:{p}:SLOT:{it['question_id']}"
    return f"{b}:{p}:{v}"


def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    idx = jload(E1 / "indexes_v2.json")["indexes"]
    items = [i for i in jload(E1 / "build" / "items_final.json")
             if i.get("label", i["label_pre"]) in SCOREABLE]
    if limit:
        items = items[:limit]
    joins = load_joins()
    qtext = {q["id"]: q["question"] for J in joins.values() for q in J.questions}
    for i in items:
        if i.get("is_probe"):
            qtext[i["question_id"]] = i["question"]

    print(f"scoreable items {len(items)}; unique questions "
          f"{len({i['question_id'] for i in items})}")

    jobs = []
    seen_blind = set()
    for it in items:
        q = qtext[it["question_id"]]
        if q not in seen_blind:                      # BLIND: one draw per unique prompt
            seen_blind.add(q)
            jobs.append(("BLIND", q, None, q))
        k = index_key(it)
        for prov in ("TRUE", "BELIEVED"):
            key = f"{k}:{prov}"
            if key in idx:
                jobs.append((f"INDEXED-{prov}", q, idx[key], it["item_id"]))
    print(f"main-arm calls: {len(jobs)} "
          f"(blind {sum(1 for j in jobs if j[0]=='BLIND')}, "
          f"indexed {sum(1 for j in jobs if j[0]!='BLIND')})")

    def run(job):
        arm, q, index, tag = job
        if arm == "BLIND":
            msgs = [{"role": "system", "content": P.SYSTEM},
                    {"role": "user", "content": P.USER_BLIND.format(question=q)}]
            cache_id = "blind"                       # prompt-hash carries the identity
        else:
            msgs = [{"role": "system", "content": P.SYSTEM},
                    {"role": "user", "content": P.USER_INDEXED.format(index=index, question=q)}]
            cache_id = tag
        r = api.call(cache_id, arm, msgs)
        o = api.parse_json(r["content"])
        failed = False
        if o is None or clamp(o.get("fok")) is None:
            r = api.call(cache_id, arm + "#retry", msgs)
            o = api.parse_json(r["content"])
            if o is None or clamp(o.get("fok")) is None:
                failed, o = True, {}
        return {"arm": arm, "tag": tag, "question": q,
                "fok": clamp(o.get("fok")), "nok": clamp(o.get("nok")),
                "nok_candidates_found": (bool(o.get("nok_candidates_found"))
                                         if not failed else None),
                "would_search": bool(o.get("would_search")) if not failed else None,
                "status": "ELICITATION_FAILED" if failed else "OK",
                "cached": r["cached"]}

    out = []
    try:
        with cf.ThreadPoolExecutor(max_workers=12) as ex:
            for n, rec in enumerate(ex.map(run, jobs), 1):
                out.append(rec)
                if n % 400 == 0:
                    api.flush()
                    print(f"  {n}/{len(jobs)}  ${api.meter()['usd']:.4f}", flush=True)
    finally:
        api.flush()
    jdump(out, E1 / "elicitation_main.json")
    ok = sum(1 for r in out if r["status"] == "OK")
    print(f"  main arms parsed {ok}/{len(out)};  ${api.meter()['usd']:.4f}")

    # ---------------- k=3 blind noise subsample
    rng = random.Random(SEED)
    uq = sorted(seen_blind)
    ksample = rng.sample(uq, min(K_QUESTIONS, len(uq)))
    kjobs = [(q, k) for q in ksample for k in (1, 2, 3)]

    def runk(job):
        q, k = job
        msgs = [{"role": "system", "content": P.SYSTEM},
                {"role": "user", "content": P.USER_BLIND.format(question=q)}]
        r = api.call(f"k{k}", "BLIND-K", msgs)
        o = api.parse_json(r["content"]) or {}
        return {"question": q, "draw": k, "fok": clamp(o.get("fok")),
                "nok": clamp(o.get("nok"))}

    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        krows = list(ex.map(runk, kjobs))
    api.flush()
    jdump(krows, E1 / "elicitation_k3.json")
    byq = collections.defaultdict(list)
    for r in krows:
        if r["fok"] is not None:
            byq[r["question"]].append(r["fok"])
    spread = [max(v) - min(v) for v in byq.values() if len(v) == 3]
    print(f"  k=3: {len(byq)} questions; identical across 3 draws "
          f"{sum(1 for s in spread if s == 0)}/{len(spread)}; "
          f"mean spread {sum(spread)/max(len(spread),1):.3f}")

    # ---------------- staircase, FR-Bank TRUE only
    frb = [i for i in items if i["backend"] == "frbank"]
    ssample = rng.sample(frb, min(STAIRCASE_N, len(frb)))

    def runs(it):
        k = f"{index_key(it)}:TRUE"
        if k not in idx:
            return None
        msgs = [{"role": "system", "content": P.STAIRCASE_SYSTEM},
                {"role": "user", "content": P.STAIRCASE_USER.format(
                    index=idx[k], question=qtext[it["question_id"]])}]
        r = api.call(it["item_id"], "STAIRCASE", msgs)
        o = api.parse_json(r["content"]) or {}
        th = [(0.10, o.get("gt_10")), (0.30, o.get("gt_30")),
              (0.50, o.get("gt_50")), (0.70, o.get("gt_70"))]
        yes = [t for t, v in th if v is True]
        # interval midpoint from the highest threshold answered yes
        val = (max(yes) + 0.20) if yes else 0.05
        return {"item_id": it["item_id"], "label": it.get("label", it["label_pre"]),
                "raw": {k2: o.get(k2) for k2 in ("gt_10", "gt_30", "gt_50", "gt_70")},
                "fok_staircase": min(val, 0.95)}

    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        srows = [r for r in ex.map(runs, ssample) if r]
    api.flush()
    jdump(srows, E1 / "elicitation_staircase.json")
    m = api.meter()
    print(f"  staircase: {len(srows)} items")
    print(f"\nPHASE C TOTAL  calls {m['calls']} live / {m['cached']} cached; "
          f"tokens {m['in']} in / {m['out']} out;  spend ${m['usd']:.4f}")
    if m["usd"] > 35:
        print("  *** OVER THE $35 GATE ***")


if __name__ == "__main__":
    main()
