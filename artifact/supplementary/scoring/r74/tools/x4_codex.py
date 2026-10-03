"""R74 X4 -- sol-lane continuation on the committed codex subscription transport
(PI budget directive 2026-08-24; D-R74-6). Invocation mirrors the committed
ladder_luna.py lane: codex exec, ephemeral, reasoning effort low, both API keys
stripped so nothing can route to metered billing. Rows append to rows_SOL.jsonl in the
lane schema with usd=0.0 and path="codex".
Usage: python r74/tools/x4_codex.py gpt-5.6-sol [--probe]
"""
import concurrent.futures, json, os, pathlib, shutil, subprocess, sys, tempfile, threading

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import prompts_e1 as P

EXPECTED_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"
assert P.texts_sha256() == EXPECTED_TEXTS_SHA, "FROZEN PROMPT MODULE HAS DRIFTED"

MODEL = sys.argv[1]
CODE = {"gpt-5.6-sol": "SOL", "gpt-5.6-luna": "LUNA"}[MODEL]
X4 = ROOT / "r74" / "x4"
CELL = json.load(open(X4 / "cell_661.json", encoding="utf-8"))["items"]
IDX = json.load(open(ROOT / "e1_metamemory" / "indexes_v2.json", encoding="utf-8"))["indexes"]
CODEX = shutil.which("codex")
assert CODEX, "codex not found"
ENV = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")}
K = 5
ROWS = X4 / f"rows_{CODE}.jsonl"

def last_json(text):
    depth, start, best, ins, esc = 0, None, None, False, False
    for i, ch in enumerate(text or ""):
        if ins:
            ins = not (ch == '"' and not esc); esc = (ch == "\\" and not esc); continue
        if ch == '"': ins, esc = True, False
        elif ch == "{":
            if depth == 0: start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None: best = text[start:i + 1]
    try: return json.loads(best) if best else None
    except Exception: return None

def clamp(v):
    try: v = float(v)
    except (TypeError, ValueError): return None
    if v > 1: v /= 100.0
    return max(0.0, min(1.0, v))

WRAP_HEAD = ("Complete the following monitoring request now. Everything needed is "
             "included below; do not ask for more input. Reply with ONLY the JSON "
             "object the instructions specify.\n\n")
WRAP_TAIL = "\n\nReply with only the JSON object now."

def call(it, arm, draw):
    q = it["question"]
    user = (P.USER_INDEXED.format(index=IDX[it["index_key"]], question=q)
            if arm == "INDEXED-TRUE" else P.USER_BLIND.format(question=q))
    # D-R74 lane disclosure: codex-cli 0.147.0 drifted from the committed Aug-13 CLI --
    # the bare flattened prompt is treated as a role description and the model waits for
    # input. The PI-authorized transport wrapper below is the one fix attempt; the frozen
    # SYSTEM and USER texts are embedded byte-verbatim.
    prompt = WRAP_HEAD + P.SYSTEM + "\n\n" + user + WRAP_TAIL
    with tempfile.TemporaryDirectory() as td:
        out = pathlib.Path(td) / "o.txt"
        r = subprocess.run([CODEX, "exec", "-m", MODEL, "--cd", td, "--skip-git-repo-check",
                            "--ephemeral", "--ignore-user-config", "--ignore-rules",
                            "-s", "read-only", "--color", "never",
                            "-c", "model_reasoning_effort=low", "-o", str(out), prompt],
                           capture_output=True, text=True, timeout=600, env=ENV,
                           shell=False)
        text = out.read_text(encoding="utf-8", errors="replace") if out.exists() else (r.stdout or "")
    j = last_json(text) or {}
    fok, nok = clamp(j.get("fok")), clamp(j.get("nok"))
    return {"item_id": it["item_id"], "arm": arm, "model": MODEL, "draw": draw,
            "label": it["label"], "y_fok": it["y_fok"], "y_nok": it["y_nok"],
            "fok": fok, "nok": nok, "status": "OK" if fok is not None else "PARSE_FAIL",
            "served_model": MODEL + " (codex-subscription)", "tok_in": None, "tok_out": None,
            "usd": 0.0, "path": "codex", "text": (text or "")[:2000]}

done = set()
if ROWS.exists():
    for line in open(ROWS, encoding="utf-8"):
        r = json.loads(line)
        if r.get("status") == "OK":
            done.add((r["item_id"], r["arm"], r["draw"]))
jobs = [(it, arm, d) for it in CELL for arm in ("BLIND", "INDEXED-TRUE")
        for d in range(1, K + 1) if (it["item_id"], arm, d) not in done]

if "--probe" in sys.argv:
    row = call(*jobs[0])
    print("PROBE:", {k: row[k] for k in ("item_id", "arm", "fok", "nok", "status")})
    print(row["text"][:200])
    sys.exit(0)

if "--probegate" in sys.argv:
    # PI probe gate: 12 calls (6 blind, 6 indexed, spread over items), >=11/12 valid JSON.
    import itertools
    picks = [j for j in itertools.islice(
        ((it, arm, 1) for i, it in enumerate(CELL) if i % 110 == 0
         for arm in ("BLIND", "INDEXED-TRUE")), 12)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        rows = list(ex.map(lambda j: call(*j), picks))
    ok = sum(1 for r in rows if r["status"] == "OK")
    for r in rows:
        print(f"  {r['status']:10s} {r['arm']:12s} fok={r['fok']} | {r['text'][:80]!r}")
    print(f"PROBE GATE: {ok}/12 valid ->", "PASS" if ok >= 11 else "FAIL")
    sys.exit(0 if ok >= 11 else 2)

print(f"{MODEL} via codex: {len(jobs)} calls to go (resumed past {len(done)})")
lock = threading.Lock()
def work(j):
    try:
        row = call(*j)
    except Exception as e:
        it, arm, d = j
        row = {"item_id": it["item_id"], "arm": arm, "model": MODEL, "draw": d,
               "status": f"ERROR:{type(e).__name__}", "usd": 0.0, "path": "codex"}
    with lock:
        with open(ROWS, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, sort_keys=True) + "\n")
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
    n = 0
    for _ in ex.map(work, jobs):
        n += 1
        if n % 250 == 0:
            print(n, "/", len(jobs), flush=True)
print("DONE (codex lane, $0 billed)")
