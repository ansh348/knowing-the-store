"""cf3_run.py -- ADDENDUM_CF3 §4: the lanes on the 42-item expiry cell through run_cf.py, CALLED (cf2_run's pattern).

run_cf.py is imported unchanged (its prompts_e1 digest assertions run at import) and its module globals are re-pointed
to the CF-3 cell: items from cf3/cf_cell.json, indexes from cf3/cf_indexes.json (v2, v3, v2r), rows under cf3/rows/,
probes at cf3/probes.json. Arms BLIND, INDEXED-V2, INDEXED-V3, INDEXED-V2R. Opus 5 at k = 1 (the author's
instruction; §4); mini k = 1 synchronous; Haiku 4.5 k = 5 Batch.

Subcommands (as run_cf): probe <lane> | project | sync <lane> | submit <lane> | poll <lane>
"""
from __future__ import annotations

import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
import run_cf as RC  # noqa: E402  (asserts prompts_e1 digests at import)

CF3 = ROOT / "r82_counterfactual" / "cf3"
RC.CELL = json.load(io.open(CF3 / "cf_cell.json", encoding="utf-8"))["items"]
RC.IDX = json.load(io.open(CF3 / "cf_indexes.json", encoding="utf-8"))["indexes"]
RC.ROWS = CF3 / "rows"
RC.PROBES = CF3 / "probes.json"
RC.ARMS = ("BLIND", "INDEXED-V2", "INDEXED-V3", "INDEXED-V2R")
RC.QUESTIONS = sorted({it["question"]: it for it in RC.CELL}.items())
RC.BLIND_UNITS = [{"unit_id": f"q{n:03d}", "question": q} for n, (q, _) in enumerate(RC.QUESTIONS)]
RC.LANES["claude-opus-5"]["k"] = 1              # §4: Opus 5 once
ARM_KEY = {"INDEXED-V2": "v2", "INDEXED-V3": "v3", "INDEXED-V2R": "v2r"}
LINE = 5.00                                     # §6
assert len(RC.CELL) == 42 and len(RC.BLIND_UNITS) == 14, (len(RC.CELL), len(RC.BLIND_UNITS))
assert all("v2r" in v for v in RC.IDX.values())


def units(arm):
    if arm == "BLIND":
        return RC.BLIND_UNITS
    return [{"unit_id": it["item_id"], "question": it["question"], "index": RC.IDX[it["item_id"]][ARM_KEY[arm]]} for it in RC.CELL]


RC.units = units


def cmd_project():
    d = json.load(io.open(RC.PROBES, encoding="utf-8"))
    total = 0.0
    print(f"{'lane':30s} {'calls':>6s} {'in(M)':>7s} {'out(M)':>7s} {'batch':>6s} {'usd':>8s} {'x1.3':>8s}")
    for lane, rec in sorted(d.items()):
        cfg = RC.LANES[lane]; k = cfg["k"]
        n = k * (len(RC.BLIND_UNITS) + 3 * len(RC.CELL))
        tin = k * (len(RC.BLIND_UNITS) * rec["blind_in"] + len(RC.CELL) * (rec["v2_in"] + rec["v3_in"] + rec["v2_in"]))
        tout = n * max(1, sum(rec["out"]) / len(rec["out"]))
        usd = (tin / 1e6 * cfg["price"][0] + tout / 1e6 * cfg["price"][1]) * cfg["mult"]
        total += usd
        print(f"{lane:30s} {n:6d} {tin/1e6:7.3f} {tout/1e6:7.3f} {cfg['mult']:6.1f} {usd:8.2f} {usd*1.3:8.2f}")
    print(f"{'TOTAL projected':30s} {'':6s} {'':7s} {'':7s} {'':6s} {total:8.2f} {total*1.3:8.2f}   line ${LINE:.2f}")
    if total * 1.3 > LINE:
        sys.exit("PROJECTION EXCEEDS THE LINE AT 1.3x -- do not launch")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "project":
        cmd_project()
    else:
        getattr(RC, "cmd_" + cmd)(sys.argv[2])
