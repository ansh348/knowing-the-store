# -*- coding: utf-8 -*-
"""r130_dryrun.py -- program R130, Phase 0: a synthetic fill to exercise build-judge, the scorer and the validator without any call.
Writes ONLY under the directory given (the scratchpad); the numbers are meaningless and are never committed.

    python r130_dryrun.py <dir>
"""
from __future__ import annotations

import json
import pathlib
import random
import subprocess
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r130_common as C  # noqa: E402

out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
rng = random.Random(130)
b = C.J(C.BUILD / "build_r130.json")
# synthetic Luna rows: a mix of abstentions, stale restatements and clean answers
luna = {}
for j in b["jobs"]:
    r = rng.random()
    ans = "The store does not currently contain the answer." if r < 0.2 else ("Synthetic answer restating the old value." if r < 0.5 else "Synthetic clean answer.")
    luna[j["key"]] = {**{k: j[k] for k in ("key", "item_id", "persona", "question", "label", "state", "view_sha", "n_lines", "policies", "source", "key_a4")}, "model": "gpt-5.6-luna",
                      "answer": ans, "status": "OK", "n_calls": 1, "usd": 0.0004, "served_model": "gpt-5.6-luna", "tok_in": 900, "tok_out": 150, "tok_reasoning": 100, "when": C.now()}
with open(out / "rows_ds_r130_luna.jsonl", "w", encoding="utf-8", newline="\n") as f:
    for r in luna.values():
        f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
D = C.load_ds(); units = C.judge_units(D, luna_rows=luna)
C.jdump({"meta": {"n_units": len(units), "synthetic": True}, "units": units}, out / "judge_units_r130.json")
# synthetic judge rows: the label leans on the answer text so the tables are not uniform
rows = []
for u in units:
    a = u["answer"].casefold()
    if "does not currently contain" in a or "don't have" in a:
        lab = "ABSTAINS"
    elif rng.random() < (0.5 if "old value" in a else 0.2):
        lab = "ASSERTS"
    else:
        lab = rng.choice(["MENTIONS", "CLEAN", "CLEAN", "UNSURE"] if rng.random() < 0.1 else ["MENTIONS", "CLEAN", "CLEAN"])
    rows.append({"key": u["unit_id"], "unit_id": u["unit_id"], "answerer": u["answerer"], "source": u["source"], "view_key": u["key"], "key_a4": u["key_a4"], "item_id": u["item_id"],
                 "persona": u["persona"], "state": u["state"], "policies": u["policies"], "label": lab, "reason": "synthetic", "status": "OK", "served_model": "claude-opus-5",
                 "tok_in": 600, "tok_out": 60, "usd": 0.002, "n_calls": 1, "model": "claude-opus-5"})
with open(out / "rows_ds_r130_judge.jsonl", "w", encoding="utf-8", newline="\n") as f:
    for r in rows:
        f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
# a synthetic A1 label file in HV1's shape
key = C.J(C.HV1 / "key" / "key_hv1.json"); items = key["hva"]["items"]
labs = {}
jr = {r["unit_id"]: r["label"] for r in rows}; lock = b["hv1_lock"]
for uid, x in items.items():
    if x["block"] != "primary" and rng.random() < 0.5:
        continue
    jl = jr[lock[uid]]
    labs[uid] = {"uid": uid, "label": jl if rng.random() < 0.85 else rng.choice(C.LABELS), "note": ""}
C.jdump({"meta": {"annotator": "A1", "problems": [], "synthetic": True}, "labels": {"ANSWERS": labs, "TRIPLES": {}}}, out / "labels_A1.json")
print("synthetic rows written under", out)
# the scorer and the validator in dry-run mode, the build file's units replaced by the synthetic units for this run
here = pathlib.Path(__file__).parent
for tool, args in (("r130_score.py", ["--dry-run", str(out)]), ("r130_validate.py", ["--dry-run", str(out)])):
    print("\n=== ", tool)
    rc = subprocess.run([sys.executable, str(here / tool), *args, "--units", str(out / "judge_units_r130.json")], cwd=C.ROOT, capture_output=True, text=True, encoding="utf-8")
    print(rc.stdout[-6000:]); print(rc.stderr[-3000:])
