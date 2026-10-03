"""R74 X5 -- authorship-matched question rendering + label-transfer spot-check
(ADDENDUM_R74 SX5 @ 35f8416a55). NO MONITOR CALLS -- rendering and check only; the
monitor launch waits for [AUTHOR-1]'s exhibit pause.

Cell: the definite post-removal E1-NS variant-B cell (routed-back treated as removed),
reconstructed with the registered removal rule verbatim (census_and_price.apply_removal
logic). Rendering: one matched voice for every label via `claude -p` (subscription;
ANTHROPIC_API_KEY stripped so the CLI cannot route to metered billing). Check: an
independent `claude -p` extraction re-derives (entity, slot, intent) from the rendered
question alone; transfer holds iff entity and slot match and intent is CURRENT.
Bar: accuracy >= 0.95 on min(40, n) items, else HARD-STOP S1.
"""
import collections, concurrent.futures, json, os, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
NS = ROOT / "e1ns_neutralslice"
X5 = ROOT / "r74" / "x5"
X5.mkdir(parents=True, exist_ok=True)

S = json.load(open(NS / "build" / "slice_candidate.json", encoding="utf-8"))
A = json.load(open(NS / "build" / "WORKBOOK_EVIDENCE_ADDENDUM.json", encoding="utf-8"))
key = {(r["persona"], r["slot"]): r for r in A["rows"]}
confirmed = {k for k, r in key.items() if r["disposition"] == "PN"}

bytok = collections.defaultdict(lambda: {"PN": [], "non": []})
for r in S["items"]:
    bytok[r["slot"]]["PN" if r["label"] == "PN" else "non"].append(r)
cell = []
for tok, d in bytok.items():
    keep_pn = [r for r in d["PN"] if (r["persona"], r["slot"]) in confirmed]
    if not keep_pn:
        continue
    cell.extend(keep_pn)
    cell.extend(sorted(d["non"], key=lambda r: r["item_id"])[:2 * len(keep_pn)])
cell = sorted(cell, key=lambda r: r["item_id"])
comp = collections.Counter(r["label"] for r in cell)
assert len(cell) == 36 and comp == {"PN": 12, "PRESENT": 17, "ABSENT": 7}, (len(cell), comp)

SLOTS = sorted(bytok)
ENV = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")}

def cp(prompt):
    r = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True,
                       timeout=300, env=ENV, shell=(os.name == "nt"))
    return (r.stdout or "").strip()

RENDER = ("You are rendering questions for a memory study in one consistent voice. "
          "Write exactly one natural, conversational question asking what {entity}'s "
          "current {slot_phrase} is, as of today. Present tense, current state only, "
          "one sentence, end with a question mark. Output only the question.")
SLOT_PHRASE = {"fitness_routine": "fitness routine", "research_focus": "research focus"}

def render(it):
    return cp(RENDER.format(entity=it["entity"],
                            slot_phrase=SLOT_PHRASE.get(it["slot"], it["slot"])))

EXTRACT = ("From this question alone, output JSON only, no prose: "
           '{{"entity": "<first name>", "slot": "<one of: ' + ", ".join(SLOTS) + '>", '
           '"intent": "<CURRENT or PAST or UPCOMING or CHANGE>"}}. Question: {q}')

def extract(q):
    out = cp(EXTRACT.format(q=q))
    i, j = out.find("{"), out.rfind("}")
    try:
        return json.loads(out[i:j + 1])
    except Exception:
        return {}

def work(it):
    q = render(it)
    ex = extract(q)
    ok = (ex.get("entity", "").strip().lower() == it["entity"].strip().lower()
          and ex.get("slot") == it["slot"] and ex.get("intent") == "CURRENT")
    return {"item_id": it["item_id"], "persona": it["persona"], "slot": it["slot"],
            "entity": it["entity"], "label": it["label"],
            "template_question": it["question"], "rendered_question": q,
            "extracted": ex, "transfer_ok": bool(ok)}

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    rows = list(ex.map(work, cell))
rows.sort(key=lambda r: r["item_id"])
acc = sum(r["transfer_ok"] for r in rows) / len(rows)
out = {"registration": "ADDENDUM_R74 SX5 @ 35f8416a55",
       "cell": {"n": len(cell), "composition": dict(comp),
                "personas": len({r['persona'] for r in cell})},
       "spot_check": {"n": len(rows), "transfer_accuracy": acc, "bar": 0.95,
                      "verdict": "PASS" if acc >= 0.95 else "HARD-STOP-S1"},
       "rows": rows}
json.dump(out, open(X5 / "x5_render.json", "w", encoding="utf-8"), indent=1, sort_keys=True)
print("cell n=36; transfer accuracy:", acc, "->", out["spot_check"]["verdict"])
for r in rows[:6]:
    print(f"  [{r['label']:8s}] {r['rendered_question'][:90]}  ok={r['transfer_ok']}")
