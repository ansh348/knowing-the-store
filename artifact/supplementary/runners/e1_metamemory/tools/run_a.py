"""E1.5 Run A -- frontier INDEXED cell, gpt-5.6-sol via codex exec, TRUE index."""
from __future__ import annotations
import collections, concurrent.futures as cf, io, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
E1 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prompts_e1 as P
# NOTE: strong_model.py has no __main__ guard -- importing it re-executes the whole
# 150-item blind arm. Duplicating the two helpers is the correct fix here; editing
# strong_model.py would change a file whose output is already committed. (D19-E1)
import shutil as _sh
CODEX = _sh.which("codex") or _sh.which("codex.cmd") or "codex"

def last_json(s):
    d, st, esc, start = 0, False, False, -1
    for i, c in enumerate(s):
        if esc: esc = False; continue
        if c == "\\": esc = True; continue
        if c == chr(34): st = not st; continue
        if st: continue
        if c == "{":
            if d == 0: start = i
            d += 1
        elif c == "}":
            d -= 1
            if d == 0 and start >= 0:
                try: return json.loads(s[start:i+1])
                except Exception: pass
    return None
MODEL, WORKERS = P.STRONG_MODEL, 5
OUT = E1 / "run_a_frontier_indexed.json"

items = {i["item_id"]: i for i in json.load(io.open(E1/"build"/"items_final.json", encoding="utf-8"))}
idx = json.load(io.open(E1/"indexes_v2.json", encoding="utf-8"))["indexes"]
blind = json.load(io.open(E1/"strong_model.json", encoding="utf-8"))["rows"]

def index_key(it):
    b, p, v = it["backend"], it["persona"], it["variant"]
    return f"{b}:{p}:SLOT:{it['question_id']}" if v == "SLOT-ABLATED" else f"{b}:{p}:{v}"

jobs = []
for r in blind:
    it = items[r["item_id"]]
    k = f"{index_key(it)}:TRUE"
    if k in idx:
        jobs.append((r["item_id"], r["question"], idx[k]))
print(f"Run A: {len(jobs)} items, {MODEL}, TRUE index", flush=True)

def one(job):
    tag, q, index = job
    sb = Path(tempfile.mkdtemp(prefix="e15a_"))
    try:
        prompt = P.SYSTEM + "\n\n" + P.USER_INDEXED.format(index=index, question=q)
        env = {k: v for k, v in os.environ.items()
               if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")}
        o = sb / "o.txt"
        r = subprocess.run(
            [CODEX, "exec", "-m", MODEL, "--cd", str(sb), "--skip-git-repo-check",
             "--ephemeral", "--ignore-user-config", "--ignore-rules", "-s", "read-only",
             "--color", "never", "-c", "model_reasoning_effort=low", "-o", str(o)],
            input=prompt, text=True, capture_output=True, timeout=240, env=env)
        raw = o.read_text(encoding="utf-8", errors="replace") if o.exists() else ""
        obj = last_json(raw) or last_json(r.stdout) or {}
        f = obj.get("fok"); n = obj.get("nok")
        return {"item_id": tag,
                "fok": (min(100.,max(0.,float(f)))/100.) if f is not None else None,
                "nok": (min(100.,max(0.,float(n)))/100.) if n is not None else None,
                "nok_candidates_found": obj.get("nok_candidates_found"),
                "status": "OK" if f is not None else "PARSE_FAIL"}
    except Exception as e:
        return {"item_id": tag, "fok": None, "nok": None,
                "nok_candidates_found": None, "status": f"ERROR:{type(e).__name__}"}
    finally:
        shutil.rmtree(sb, ignore_errors=True)

# resume-by-id: an interrupted run does not redo completed items
PART = E1 / "run_a_partial.jsonl"
done = set()
if PART.exists():
    for ln in io.open(PART, encoding="utf-8"):
        try: done.add(json.loads(ln)["item_id"])
        except Exception: pass
jobs = [j for j in jobs if j[0] not in done]
print(f"  resuming: {len(done)} already done, {len(jobs)} to go", flush=True)
NL = chr(10)
with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
    ph = io.open(PART, "a", encoding="utf-8", newline=NL)
    try:
        for n, r in enumerate(ex.map(one, jobs), 1):
            ph.write(json.dumps(r, ensure_ascii=False) + NL)
            ph.flush()
            if n % 20 == 0:
                print(f"  {n}/{len(jobs)}", flush=True)
    finally:
        ph.close()
rows = [json.loads(ln) for ln in io.open(PART, encoding="utf-8") if ln.strip()]
for r in rows:
    it = items[r["item_id"]]
    r["backend"] = it["backend"]; r["label"] = it.get("label", it["label_pre"])
json.dump({"model": MODEL, "n": len(rows),
           "ok": sum(1 for r in rows if r["status"] == "OK"), "rows": rows},
          io.open(OUT, "w", encoding="utf-8", newline="\n"),
          ensure_ascii=False, indent=2, sort_keys=True)
print(f"OK {sum(1 for r in rows if r['status']=='OK')}/{len(rows)} -> {OUT}")
