# -*- coding: utf-8 -*-
"""op5_sync_remaining.py -- D-V2RCAT-4: the 51 Opus 5 units still unanswered after two canceled batches, run synchronously and in parallel
(6 workers) through the Messages API with the identical request (run_cf.call_once: k = 1, temperature unset, max_tokens 1024), at list
price. The rows replace the BATCH_CANCELED rows in rows/rows_OP5.jsonl, each with batch_id 'sync-2026-09-17'. Nothing else is touched."""
from __future__ import annotations
import concurrent.futures as cf, io, json, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "r114" / "tools")); sys.path.insert(0, str(ROOT / "r82_counterfactual" / "v2rcat" / "tools"))
from r114_common import assert_spec
import v2rcat as V, run_cf as RC
LANE, CODE = "claude-opus-5", "OP5"
ROWS_P = V.ROWS / f"rows_{CODE}.jsonl"
assert_spec(); assert V.registration_ok(); V.point(); RC.LANES[LANE]["k"] = 1; RC.load_env()
assert "D-V2RCAT-4" in (V.V2C / "DEVIATIONS_V2RCAT.md").read_text(encoding="utf-8")
rows = [json.loads(l) for l in io.open(ROWS_P, encoding="utf-8")]
bad = {r["unit_id"] for r in rows if r["status"] != "OK"}; assert len(rows) == 444 and len(bad) == 51, len(bad)
units = [u for u in V.units(V.ARM) if u["unit_id"] in bad]
def one(u):
    for attempt in range(4):
        try:
            r = RC.call_once(LANE, u, V.ARM, 1); r["batch_id"] = "sync-2026-09-17"; return r
        except Exception as e:  # noqa: BLE001
            if attempt == 3: raise
            time.sleep(2 ** attempt)
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    new = {r["unit_id"]: r for r in ex.map(one, units)}
assert set(new) == bad
out = [new[r["unit_id"]] if r["unit_id"] in bad else r for r in rows]
with io.open(ROWS_P, "w", encoding="utf-8", newline="\n") as f:
    for r in out: f.write(json.dumps(r, sort_keys=True) + "\n")
ok = [r for r in new.values() if r["status"] == "OK"]
print(f"sync done: {len(ok)} of {len(new)} OK, served {sorted({r['served_model'] for r in new.values()})}, ${sum(r['usd'] for r in new.values()):.4f}; lane OK {sum(1 for r in out if r['status']=='OK')} of 444")
