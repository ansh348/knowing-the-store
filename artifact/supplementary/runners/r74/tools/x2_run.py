"""R74 X2 -- elicit mini on the ablation arms (ADDENDUM_R74 SX2 @ 35f8416a55).

522 external-store items x 3 live arms (X2b is byte-identical to intact: not elicited,
recorded as intact by construction). mini, frozen prompts_e1 (digest asserted),
temperature 0, k=1, E1 protocol. Fresh cache namespace r74/x2/cache/. Cap $30 (registered).
Usage: python r74/tools/x2_run.py [--probe]   (--probe: one call, then stop)
"""
import json, pathlib, sys, concurrent.futures, hashlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import api                    # E1 shim -> loads e0 impl as _e0_api
import prompts_e1 as P

EXPECTED_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"
assert P.texts_sha256() == EXPECTED_TEXTS_SHA, "FROZEN PROMPT MODULE HAS DRIFTED"

_e0 = sys.modules["_e0_api"]
X2 = ROOT / "r74" / "x2"
(X2 / "cache").mkdir(parents=True, exist_ok=True)
_e0.CACHE_PATH = X2 / "cache" / "responses.json"
_e0.LEDGER_PATH = X2 / "cache" / "cost_ledger.json"
_e0._cache = None
_e0._load_cache()
_e0.HARD_CAP_USD = 30.00
api.load_env()

ARMS = ("X2a-count-removed", "X2c-markers-removed", "X2d-count-markers-removed")
SC = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}
vidx = json.load(open(X2 / "x2_indexes.json", encoding="utf-8"))["indexes"]
items = json.load(open(ROOT / "e1_metamemory" / "build" / "items_final.json", encoding="utf-8"))
rows_main = json.load(open(ROOT / "e1_metamemory" / "elicitation_main.json", encoding="utf-8"))
qmap = {r["tag"]: r["question"] for r in rows_main if r["arm"] != "BLIND"}
ext = [i for i in items if i.get("label", i["label_pre"]) in SC and i["backend"] in ("mem0", "amem")]

def ikey(it):
    b, p, v = it["backend"], it["persona"], it["variant"]
    return (f"{b}:{p}:SLOT:{it['question_id']}" if v == "SLOT-ABLATED" else f"{b}:{p}:{v}") + ":TRUE"

def clamp(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    if v > 1:
        v = v / 100.0
    return max(0.0, min(1.0, v))

def one(it, arm):
    q = qmap[it["item_id"]]
    index = vidx[ikey(it)][arm]
    msgs = [{"role": "system", "content": P.SYSTEM},
            {"role": "user", "content": P.USER_INDEXED.format(index=index, question=q)}]
    r = api.call(it["item_id"], arm, msgs)
    j = api.parse_json(r["content"]) or {}
    fok, nok = clamp(j.get("fok")), clamp(j.get("nok"))
    if fok is None:
        r = api.call(it["item_id"], arm + "#retry", msgs)
        j = api.parse_json(r["content"]) or {}
        fok, nok = clamp(j.get("fok")), clamp(j.get("nok"))
    return {"tag": it["item_id"], "arm": arm, "backend": it["backend"],
            "label": it.get("label", it["label_pre"]), "question": q,
            "fok": fok, "nok": nok, "cached": r["cached"],
            "status": "OK" if fok is not None else "ELICITATION_FAILED"}

probe = "--probe" in sys.argv
jobs = [(it, arm) for it in ext for arm in ARMS]
if probe:
    row = one(*jobs[0])
    api.flush()
    print("PROBE:", row, "meter:", api.meter())
    sys.exit(0)

out, done = [], 0
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
    futs = [ex.submit(one, it, arm) for it, arm in jobs]
    for f in concurrent.futures.as_completed(futs):
        out.append(f.result())
        done += 1
        if done % 400 == 0:
            api.flush()
            print(done, "/", len(jobs), api.meter())
api.flush()
json.dump(sorted(out, key=lambda r: (r["arm"], r["tag"])),
          open(X2 / "x2_elicitation.json", "w", encoding="utf-8"), indent=1, sort_keys=True)
m = api.meter()
print("DONE", len(out), "rows; failed:", sum(1 for r in out if r["status"] != "OK"), "; meter:", m)
