"""R74 X4 -- expansion cell builder (ADDENDUM_R74 SX4 @ 35f8416a55).

NOK population: all committed FR-Bank scoreable items (expect n=661, 104 PN).
FOK population: the FR-Bank hard subset (expect n=307, 35 non-ABSENT) -- a subset of the
NOK population, so one elicitation covers both. Emits r74/x4/cell_661.json with prompts
digests; prompts themselves are rebuilt on demand, never cached to disk.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import prompts_e1 as P

EXPECTED_FILE_SHA = "337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84"
EXPECTED_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"
assert P.file_sha256() == EXPECTED_FILE_SHA and P.texts_sha256() == EXPECTED_TEXTS_SHA, \
    "FROZEN PROMPT MODULE HAS DRIFTED -- refusing to build"

SC = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}
E1 = ROOT / "e1_metamemory"
items = json.load(open(E1 / "build" / "items_final.json", encoding="utf-8"))
main = json.load(open(E1 / "elicitation_main.json", encoding="utf-8"))
qmap = {r["tag"]: r["question"] for r in main if r["arm"] != "BLIND"}
idx = json.load(open(E1 / "indexes_v2.json", encoding="utf-8"))["indexes"]

def ikey(it):
    p, v = it["persona"], it["variant"]
    return (f"frbank:{p}:SLOT:{it['question_id']}" if v == "SLOT-ABLATED" else f"frbank:{p}:{v}") + ":TRUE"

cell = []
for it in sorted(items, key=lambda i: i["item_id"]):
    lab = it.get("label", it["label_pre"])
    if lab not in SC or it["backend"] != "frbank":
        continue
    assert it["item_id"] in qmap and ikey(it) in idx, it["item_id"]
    cell.append({"item_id": it["item_id"], "persona": it["persona"], "variant": it["variant"],
                 "tier": it["tier"], "label": lab, "question": qmap[it["item_id"]],
                 "index_key": ikey(it),
                 "y_fok": 0 if lab == "ABSENT" else 1,
                 "y_nok": 1 if lab == "PRESENT-NEGATIVE" else 0})

n_pn = sum(c["y_nok"] for c in cell)
hard = [c for c in cell if c["tier"] == "hard"]
n_hard_pos = sum(c["y_fok"] for c in hard)
expect = {"n": 661, "n_pn": 104, "n_hard": 307, "n_hard_fok_pos": 35}
got = {"n": len(cell), "n_pn": n_pn, "n_hard": len(hard), "n_hard_fok_pos": n_hard_pos}
assert got == expect, (got, expect)

out = ROOT / "r74" / "x4"
out.mkdir(parents=True, exist_ok=True)
json.dump({"expect": expect, "got": got,
           "prompts_file_sha256": EXPECTED_FILE_SHA, "prompts_texts_sha256": EXPECTED_TEXTS_SHA,
           "items": cell},
          open(out / "cell_661.json", "w", encoding="utf-8"), indent=1, sort_keys=True)
print("cell:", got, "-> written", out / "cell_661.json")
