"""R74 X5 -- label-transfer extraction re-run (checker-instrument fix, D-R74 entry).

The first pass's renders are kept verbatim (r74/x5/x5_render.json); only the extraction
checker re-runs. Root cause: subprocess shell=True on Windows mangled prompts containing
quotes, so every extraction returned empty while every quote-free render succeeded.
Fix: spawn the claude executable directly (shutil.which, shell=False).
"""
import concurrent.futures, json, os, pathlib, shutil, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
X5 = ROOT / "r74" / "x5"
CLAUDE = shutil.which("claude")
assert CLAUDE and CLAUDE.lower().endswith(".exe"), CLAUDE
ENV = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")}

d = json.load(open(X5 / "x5_render.json", encoding="utf-8"))
SLOTS = sorted({r["slot"] for r in d["rows"]} | {"apartment", "coaching", "fitness_routine",
               "hobby", "housing", "partner", "relationship", "research_focus", "sport",
               "team", "truck", "vehicle"})
EXTRACT = ("From this question alone, output JSON only, no prose: "
           '{{"entity": "<first name>", "slot": "<one of: ' + ", ".join(SLOTS) + '>", '
           '"intent": "<CURRENT or PAST or UPCOMING or CHANGE>"}}. Question: {q}')

def cp(prompt):
    r = subprocess.run([CLAUDE, "-p", prompt], capture_output=True, text=True,
                       timeout=300, env=ENV)
    return (r.stdout or "").strip()

def extract(q):
    out = cp(EXTRACT.format(q=q))
    i, j = out.find("{"), out.rfind("}")
    try:
        return json.loads(out[i:j + 1])
    except Exception:
        return {"_raw": out[:200]}

def work(r):
    ex = extract(r["rendered_question"])
    r["extracted"] = ex
    r["transfer_ok"] = bool(ex.get("entity", "").strip().lower() == r["entity"].strip().lower()
                            and ex.get("slot") == r["slot"] and ex.get("intent") == "CURRENT")
    return r

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    rows = list(ex.map(work, d["rows"]))
rows.sort(key=lambda r: r["item_id"])
acc = sum(r["transfer_ok"] for r in rows) / len(rows)
d["rows"] = rows
d["spot_check"] = {"n": len(rows), "transfer_accuracy": acc, "bar": 0.95,
                   "verdict": "PASS" if acc >= 0.95 else "HARD-STOP-S1",
                   "checker_note": "extraction re-run after shell-quoting instrument fix; renders unchanged"}
json.dump(d, open(X5 / "x5_render.json", "w", encoding="utf-8"), indent=1, sort_keys=True)
print("transfer accuracy:", acc, "->", d["spot_check"]["verdict"])
for r in rows:
    if not r["transfer_ok"]:
        print("  FAIL", r["item_id"], "|", r["rendered_question"][:70], "|", r["extracted"])
