"""R74 X5 -- PI ruling (a): re-render ONLY the two S1-failing relationship items under a
slot-disambiguated instruction (relationship-status slot, not partner identity);
authorship-matching constraints identical (same voice instruction skeleton, one
generator, claude -p subscription, keys stripped). Re-check with the fixed checker.
36/36 -> stage exhibits and PAUSE for [AUTHOR-1]'s in-session approval. Any failure ->
stage branch (b) drop-arithmetic beside the exhibits. No monitor calls either way.
"""
import json, os, pathlib, shutil, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
X5 = ROOT / "r74" / "x5"
CLAUDE = shutil.which("claude")
ENV = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")}
TARGETS = {"ns:saga:relationship", "ns:zara:relationship"}

d = json.load(open(X5 / "x5_render.json", encoding="utf-8"))
SLOTS = sorted({r["slot"] for r in d["rows"]} | {"apartment", "coaching", "fitness_routine",
               "hobby", "housing", "partner", "relationship", "research_focus", "sport",
               "team", "truck", "vehicle"})

def cp(prompt):
    r = subprocess.run([CLAUDE, "-p", prompt], capture_output=True, text=True,
                       timeout=300, env=ENV)
    return (r.stdout or "").strip()

RENDER2 = ("You are rendering questions for a memory study in one consistent voice. "
           "Write exactly one natural, conversational question asking what {entity}'s "
           "current relationship status is, as of today --- the status itself (for "
           "example single, dating, engaged, married), NOT who the partner is. Present "
           "tense, current state only, one sentence, end with a question mark. "
           "Output only the question.")

EXTRACT = ("From this question alone, output JSON only, no prose: "
           '{{"entity": "<first name>", "slot": "<one of: ' + ", ".join(SLOTS) + '>", '
           '"intent": "<CURRENT or PAST or UPCOMING or CHANGE>"}}. Question: {q}')

def extract(q):
    out = cp(EXTRACT.format(q=q))
    i, j = out.find("{"), out.rfind("}")
    try:
        return json.loads(out[i:j + 1])
    except Exception:
        return {"_raw": out[:200]}

for r in d["rows"]:
    if r["item_id"] not in TARGETS:
        continue
    q = cp(RENDER2.format(entity=r["entity"]))
    ex = extract(q)
    r["rendered_question"] = q
    r["extracted"] = ex
    r["rerendered_under"] = "PI ruling (a): slot-disambiguated relationship-status instruction"
    r["transfer_ok"] = bool(ex.get("entity", "").strip().lower() == r["entity"].strip().lower()
                            and ex.get("slot") == r["slot"] and ex.get("intent") == "CURRENT")
    print(r["item_id"], "->", q, "|", ex, "| ok:", r["transfer_ok"])

acc = sum(r["transfer_ok"] for r in d["rows"]) / len(d["rows"])
d["spot_check"] = {"n": len(d["rows"]), "transfer_accuracy": acc, "bar": 0.95,
                   "verdict": "PASS" if acc >= 0.95 else "HARD-STOP-S1",
                   "ruling_a_note": "two relationship items re-rendered slot-disambiguated per PI ruling (a); all other renders untouched"}
json.dump(d, open(X5 / "x5_render.json", "w", encoding="utf-8"), indent=1, sort_keys=True)
print("transfer accuracy:", acc, "->", d["spot_check"]["verdict"])
