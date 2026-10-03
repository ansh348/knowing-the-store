"""R74 X3 -- billed economics micro-run (ADDENDUM_R74 SX3 @ 35f8416a55).

TELEMETRY ONLY: 10,000 mini INDEXED-TRUE calls (prompt caching automatic) + 2,000 BLIND
calls; items cycled in fixed seed-42 shuffled order over the committed FR-Bank scoreable
population; frozen prompts (digest asserted); temperature 0. Per-call usage recorded:
prompt_tokens, cached_tokens (usage.prompt_tokens_details.cached_tokens), completion
tokens. FOK/NOK outputs are NEVER parsed, scored, or written (registered do-not-use).
Prices pinned at run date (developers.openai.com/api/docs/pricing, fetched 2026-08-24):
gpt-4.1-mini input $0.40 / cached input $0.10 / output $1.60 per 1M tokens.
Usage: python r74/tools/x3_run.py [--probe]
"""
import json, pathlib, random, sys, threading, concurrent.futures

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import prompts_e1 as P

EXPECTED_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"
assert P.texts_sha256() == EXPECTED_TEXTS_SHA, "FROZEN PROMPT MODULE HAS DRIFTED"

import api  # noqa: E402  (for load_env only)
api.load_env()
from openai import OpenAI  # noqa: E402
client = OpenAI()

PRICE_IN, PRICE_CACHED, PRICE_OUT = 0.40, 0.10, 1.60   # USD per 1M tok, pinned 2026-08-24
N_INDEXED, N_BLIND, WORKERS, CAP_USD = 10_000, 2_000, 12, 8.00
SC = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}

idx = json.load(open(ROOT / "e1_metamemory" / "indexes_v2.json", encoding="utf-8"))["indexes"]
items = json.load(open(ROOT / "e1_metamemory" / "build" / "items_final.json", encoding="utf-8"))
rows_main = json.load(open(ROOT / "e1_metamemory" / "elicitation_main.json", encoding="utf-8"))
qmap = {r["tag"]: r["question"] for r in rows_main if r["arm"] != "BLIND"}
frb = [i for i in items if i.get("label", i["label_pre"]) in SC and i["backend"] == "frbank"
       and i["item_id"] in qmap]

def ikey(it):
    p, v = it["persona"], it["variant"]
    return (f"frbank:{p}:SLOT:{it['question_id']}" if v == "SLOT-ABLATED" else f"frbank:{p}:{v}") + ":TRUE"

rng = random.Random(42)
pool = sorted(frb, key=lambda i: i["item_id"])
rng.shuffle(pool)
indexed_seq = [pool[i % len(pool)] for i in range(N_INDEXED)]
blind_seq = [pool[i % len(pool)] for i in range(N_BLIND)]

X3 = ROOT / "r74" / "x3"
X3.mkdir(parents=True, exist_ok=True)
LOG = X3 / "telemetry.jsonl"
_lock = threading.Lock()
_spend = [0.0]

def call(kind, i, it):
    q = qmap[it["item_id"]]
    user = (P.USER_INDEXED.format(index=idx[ikey(it)], question=q) if kind == "INDEXED"
            else P.USER_BLIND.format(question=q))
    r = client.chat.completions.create(
        model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": P.SYSTEM}, {"role": "user", "content": user}])
    u = r.usage
    cached = getattr(getattr(u, "prompt_tokens_details", None), "cached_tokens", 0) or 0
    usd = ((u.prompt_tokens - cached) / 1e6 * PRICE_IN + cached / 1e6 * PRICE_CACHED
           + u.completion_tokens / 1e6 * PRICE_OUT)
    rec = {"kind": kind, "n": i, "item_id": it["item_id"], "model": r.model,
           "prompt_tokens": u.prompt_tokens, "cached_tokens": cached,
           "completion_tokens": u.completion_tokens, "usd_billed": round(usd, 8)}
    with _lock:
        _spend[0] += usd
        if _spend[0] > CAP_USD:
            raise RuntimeError(f"X3 cap {CAP_USD} exceeded")
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec

if "--probe" in sys.argv:
    print("PROBE:", call("INDEXED", 0, indexed_seq[0]))
    sys.exit(0)

done = set()
if LOG.exists():
    for line in open(LOG, encoding="utf-8"):
        r = json.loads(line)
        done.add((r["kind"], r["n"]))
jobs = ([("INDEXED", i, it) for i, it in enumerate(indexed_seq) if ("INDEXED", i) not in done]
        + [("BLIND", i, it) for i, it in enumerate(blind_seq) if ("BLIND", i) not in done])
print(f"jobs: {len(jobs)} (resumed past {len(done)})")
with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
    n = 0
    for _ in ex.map(lambda j: call(*j), jobs):
        n += 1
        if n % 1000 == 0:
            print(n, "/", len(jobs), f"spend ${_spend[0]:.2f}")
print(f"DONE session-spend ${_spend[0]:.4f} (resume-safe log at {LOG})")
