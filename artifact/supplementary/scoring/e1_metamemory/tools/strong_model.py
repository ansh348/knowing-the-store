"""Strong-model blind arm: gpt-5.6-sol via codex exec, ~150 stratified items."""
from __future__ import annotations
import collections, concurrent.futures as cf, io, json, os, random, re, shutil, subprocess, sys, tempfile
from pathlib import Path
E1 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prompts_e1 as P
SEED, N, MODEL, WORKERS = 42, 150, "gpt-5.6-sol", 5
# Windows: `codex` is an npm .CMD shim. subprocess cannot resolve a bare name to a
# .CMD without a shell, so `["codex", ...]` raises FileNotFoundError even though
# `codex` resolves fine in bash. Resolve the real path once.
CODEX = shutil.which("codex") or shutil.which("codex.cmd") or "codex"
OUT = E1 / "strong_model.json"
SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}

def last_json(s):
    d, st, esc, start = 0, False, False, -1
    for i, c in enumerate(s):
        if esc: esc = False; continue
        if c == "\\": esc = True; continue
        if c == '"': st = not st; continue
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

def one(job):
    tag, q = job
    sb = Path(tempfile.mkdtemp(prefix="e1cx_"))
    try:
        prompt = P.SYSTEM + "\n\n" + P.USER_BLIND.format(question=q)
        env = {k: v for k, v in os.environ.items()
               if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")}   # cost-routing guard
        o = sb / "o.txt"
        r = subprocess.run(
            [CODEX, "exec", "-m", MODEL, "--cd", str(sb), "--skip-git-repo-check",
             "--ephemeral", "--ignore-user-config", "--ignore-rules", "-s", "read-only",
             "--color", "never", "-c", "model_reasoning_effort=low", "-o", str(o)],
            input=prompt, text=True, capture_output=True, timeout=180, env=env)
        raw = o.read_text(encoding="utf-8", errors="replace") if o.exists() else ""
        obj = last_json(raw) or last_json(r.stdout) or {}
        f = obj.get("fok")
        return {"item_id": tag, "question": q,
                "fok": (min(100.0, max(0.0, float(f))) / 100.0) if f is not None else None,
                "nok": (min(100.0, max(0.0, float(obj["nok"]))) / 100.0
                        if obj.get("nok") is not None else None),
                "status": "OK" if f is not None else "PARSE_FAIL"}
    except Exception as e:
        return {"item_id": tag, "question": q, "fok": None, "nok": None,
                "status": f"ERROR:{type(e).__name__}"}
    finally:
        shutil.rmtree(sb, ignore_errors=True)

items = [i for i in json.load(io.open(E1/"build"/"items_final.json", encoding="utf-8"))
         if i.get("label", i["label_pre"]) in SCOREABLE]
main = json.load(io.open(E1/"elicitation_main.json", encoding="utf-8"))
qmap = {r["tag"]: r["question"] for r in main if r["arm"] != "BLIND"}
strata = collections.defaultdict(list)
for it in items:
    strata[it.get("label", it["label_pre"])].append(it)
rng = random.Random(SEED)
sample, quota = [], {"PRESENT": 50, "ABSENT": 60, "PRESENT-NEGATIVE": 40}
for k, v in quota.items():
    pool = sorted(strata.get(k, []), key=lambda i: i["item_id"])
    sample += rng.sample(pool, min(v, len(pool)))
jobs = [(i["item_id"], qmap.get(i["item_id"], i.get("question", ""))) for i in sample]
jobs = [(t, q) for t, q in jobs if q]
print(f"strong-model blind: {len(jobs)} items, model {MODEL}", flush=True)
rows = []
with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
    for n, r in enumerate(ex.map(one, jobs), 1):
        rows.append(r)
        if n % 25 == 0: print(f"  {n}/{len(jobs)}", flush=True)
lab = {i["item_id"]: i.get("label", i["label_pre"]) for i in sample}
for r in rows: r["label"] = lab.get(r["item_id"])
json.dump({"model": MODEL, "n": len(rows),
           "ok": sum(1 for r in rows if r["status"] == "OK"), "rows": rows},
          io.open(OUT, "w", encoding="utf-8", newline="\n"),
          ensure_ascii=False, indent=2, sort_keys=True)
print(f"OK {sum(1 for r in rows if r['status']=='OK')}/{len(rows)} -> {OUT}")
