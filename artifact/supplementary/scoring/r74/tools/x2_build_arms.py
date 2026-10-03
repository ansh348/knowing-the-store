"""R74 X2 -- build the four registered index-ablation arms (ADDENDUM_R74 SX2 @ 35f8416a55).

Pure text ablation of the committed external-store indexes (indexes_v2.json), all else
byte-identical. Arms:
  X2a-count-removed    : the "entries in this store: N" line deleted
  X2b-names-removed    : category-name lines deleted -- NO SITE EXISTS on these stores
                         (every name section's body is exactly the marker line);
                         emitted byte-identical to intact and recorded as such
  X2c-markers-removed  : every line whose content is exactly the marker deleted
  X2d-count-markers-removed : X2a + X2c
Build-time assertions: the diff against intact is exactly the intended lines.
"""
import hashlib, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
MARK = "not expressible by this backend"
SC = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}

idx = json.load(open(ROOT / "e1_metamemory" / "indexes_v2.json", encoding="utf-8"))["indexes"]
items = json.load(open(ROOT / "e1_metamemory" / "build" / "items_final.json", encoding="utf-8"))
ext = [i for i in items if i.get("label", i["label_pre"]) in SC and i["backend"] in ("mem0", "amem")]

def ikey(it):
    b, p, v = it["backend"], it["persona"], it["variant"]
    return (f"{b}:{p}:SLOT:{it['question_id']}" if v == "SLOT-ABLATED" else f"{b}:{p}:{v}") + ":TRUE"

keys = sorted({ikey(i) for i in ext})

def drop(text, pred):
    kept, dropped = [], []
    for line in text.splitlines():
        (dropped if pred(line) else kept).append(line)
    return "\n".join(kept), dropped

def build(text):
    a, da = drop(text, lambda l: l.strip().startswith("entries in this store:"))
    c, dc = drop(text, lambda l: l.strip() == MARK)
    d, _ = drop(a, lambda l: l.strip() == MARK)
    assert len(da) == 1, da
    assert len(dc) == 3, dc
    assert d == drop(c, lambda l: l.strip().startswith("entries in this store:"))[0]
    return {"TRUE": text, "X2a-count-removed": a, "X2b-names-removed": text,
            "X2c-markers-removed": c, "X2d-count-markers-removed": d}

out = {"meta": {"registration": "ADDENDUM_R74 SX2 @ 35f8416a55", "marker": MARK,
                "n_keys": len(keys), "x2b_note": "no category-name site exists on any of the "
                f"{len(keys)} external keys; X2b is byte-identical to intact by construction",
                "sha256_by_key": {}},
       "indexes": {}}
for k in keys:
    arms = build(idx[k])
    out["indexes"][k] = arms
    out["meta"]["sha256_by_key"][k] = {a: hashlib.sha256(t.encode()).hexdigest()[:16]
                                       for a, t in arms.items()}
    assert arms["X2b-names-removed"] == arms["TRUE"]

dst = ROOT / "r74" / "x2"
dst.mkdir(parents=True, exist_ok=True)
json.dump(out, open(dst / "x2_indexes.json", "w", encoding="utf-8"), indent=1, sort_keys=True)
print("keys:", len(keys), "-> written", dst / "x2_indexes.json")
