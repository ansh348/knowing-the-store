"""E1.5 Run B -- H-b: external items re-elicited with marker lines OMITTED."""
from __future__ import annotations
import collections, concurrent.futures as cf, io, json, sys
from pathlib import Path
E1 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import api, prompts_e1 as P

MARKER = "not expressible by this backend"
SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}

def strip_markers(txt):
    """Drop every line whose value is the marker; drop a section header left empty."""
    out, lines = [], txt.split("\n")
    for i, ln in enumerate(lines):
        if MARKER in ln:
            continue
        out.append(ln)
    # collapse a header immediately followed by blank/EOF (its only row was a marker)
    cleaned = []
    for i, ln in enumerate(out):
        nxt = out[i + 1].strip() if i + 1 < len(out) else ""
        if ln.strip() and ln.strip() == ln.strip().upper() and not nxt and ln.strip() != "":
            if not any(c.islower() for c in ln) and len(ln.strip()) > 3:
                continue
        cleaned.append(ln)
    return "\n".join(cleaned)

items = [i for i in json.load(io.open(E1/"build"/"items_final.json", encoding="utf-8"))
         if i.get("label", i["label_pre"]) in SCOREABLE and i["backend"] in ("mem0", "amem")]
idx = json.load(io.open(E1/"indexes_v2.json", encoding="utf-8"))["indexes"]
main = json.load(io.open(E1/"elicitation_main.json", encoding="utf-8"))
qmap = {r["tag"]: r["question"] for r in main if r["arm"] != "BLIND"}

def index_key(it):
    b, p, v = it["backend"], it["persona"], it["variant"]
    return f"{b}:{p}:SLOT:{it['question_id']}" if v == "SLOT-ABLATED" else f"{b}:{p}:{v}"

jobs = []
for it in items:
    k = f"{index_key(it)}:TRUE"
    q = qmap.get(it["item_id"], it.get("question", ""))
    if k in idx and q:
        jobs.append((it["item_id"], q, strip_markers(idx[k])))
print(f"Run B H-b: {len(jobs)} external items, marker lines omitted", flush=True)
sample = jobs[0][2]
print("--- sample stripped index ---")
print(sample[:600])
print("--- marker present in any stripped index? ---",
      any(MARKER in j[2] for j in jobs))

def one(job):
    tag, q, index = job
    msgs = [{"role": "system", "content": P.SYSTEM},
            {"role": "user", "content": P.USER_INDEXED_NOMARKER.format(index=index, question=q)}]
    r = api.call(tag, "INDEXED-TRUE-NOMARKER", msgs)
    o = api.parse_json(r["content"]) or {}
    f = o.get("fok")
    return {"item_id": tag, "fok": (min(100.,max(0.,float(f)))/100.) if f is not None else None,
            "nok": (min(100.,max(0.,float(o["nok"])))/100. if o.get("nok") is not None else None),
            "status": "OK" if f is not None else "PARSE_FAIL"}

rows = []
with cf.ThreadPoolExecutor(max_workers=12) as ex:
    for n, r in enumerate(ex.map(one, jobs), 1):
        rows.append(r)
        if n % 150 == 0:
            api.flush(); print(f"  {n}/{len(jobs)}  ${api.meter()['usd']:.4f}", flush=True)
api.flush()
by = {i["item_id"]: i for i in items}
for r in rows:
    r["backend"] = by[r["item_id"]]["backend"]
    r["label"] = by[r["item_id"]].get("label", by[r["item_id"]]["label_pre"])
json.dump({"n": len(rows), "ok": sum(1 for r in rows if r["status"] == "OK"), "rows": rows},
          io.open(E1/"run_b_nomarker.json", "w", encoding="utf-8", newline="\n"),
          ensure_ascii=False, indent=2, sort_keys=True)
print(f"OK {sum(1 for r in rows if r['status']=='OK')}/{len(rows)}  ${api.meter()['usd']:.4f}")
