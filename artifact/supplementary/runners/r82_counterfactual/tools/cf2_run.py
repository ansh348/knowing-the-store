"""cf2_run.py -- CF-2: elicitation on the 444-item cell through run_cf.py, CALLED.

run_cf.py is imported unchanged (its prompts_e1 digest assertions run at import) and its module
globals are re-pointed to the CF-2 cell: items from cf2/cf_cell.json, indexes from
cf2/cf_indexes.json (v2, v3, V2R), rows under cf2/rows/, probes at cf2/probes.json. The arm list
gains INDEXED-V2R (ADDENDUM_CF2 section 5); make_row, call_once, cmd_probe, cmd_submit, cmd_poll
and cmd_sync are run_cf's own. Two things are this file's:

  * units(): the V2R arm reads the "v2r" index of the item (run_cf knows only v2 / v3);
  * project: the section-10 ceiling lines (mini $2, Haiku 4.5 $16, Opus 5 $105, Anthropic $121
    of $130) replace run_cf's hard-coded $12; calls per lane = k x (questions + 3 x items x 4/3)
    i.e. k x (148 + 4 x 444) with four arms; V2R priced at v2's probe figure.

Subcommands (as run_cf): probe <lane> | project | sync <lane> | submit <lane> | poll <lane>
mini is k=1 temperature 0 synchronous (8 workers, jsonl resume); Anthropic lanes k=5 via Batch.
"""
from __future__ import annotations

import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
import run_cf as RC  # noqa: E402  (asserts prompts_e1 digests at import)

CF2 = ROOT / "r82_counterfactual" / "cf2"
RC.CELL = json.load(io.open(CF2 / "cf_cell.json", encoding="utf-8"))["items"]
RC.IDX = json.load(io.open(CF2 / "cf_indexes.json", encoding="utf-8"))["indexes"]
RC.ROWS = CF2 / "rows"
RC.PROBES = CF2 / "probes.json"
RC.ARMS = ("BLIND", "INDEXED-V2", "INDEXED-V3", "INDEXED-V2R")
RC.QUESTIONS = sorted({it["question"]: it for it in RC.CELL}.items())
RC.BLIND_UNITS = [{"unit_id": f"q{n:03d}", "question": q} for n, (q, _) in enumerate(RC.QUESTIONS)]
ARM_KEY = {"INDEXED-V2": "v2", "INDEXED-V3": "v3", "INDEXED-V2R": "v2r"}
CEILING = {"gpt-4.1-mini": 2.00, "claude-haiku-4-5-20251001": 16.00, "claude-opus-5": 105.00}
ANTHROPIC_TOTAL = 121.00
assert len(RC.CELL) == 444 and len(RC.BLIND_UNITS) == 148, (len(RC.CELL), len(RC.BLIND_UNITS))
assert all("v2r" in v for v in RC.IDX.values())


def units(arm):
    if arm == "BLIND":
        return RC.BLIND_UNITS
    return [{"unit_id": it["item_id"], "question": it["question"], "index": RC.IDX[it["item_id"]][ARM_KEY[arm]]} for it in RC.CELL]


RC.units = units          # run_cf's functions resolve `units` through their module globals


def cmd_project():
    d = json.load(io.open(RC.PROBES, encoding="utf-8"))
    total_anthropic = 0.0
    print(f"{'lane':30s} {'calls':>6s} {'in(M)':>7s} {'out(M)':>7s} {'batch':>6s} {'usd':>8s} {'x1.3':>8s} {'line':>7s}")
    over = []
    for lane, rec in sorted(d.items()):
        cfg = RC.LANES[lane]; k = cfg["k"]
        n = k * (len(RC.BLIND_UNITS) + 3 * len(RC.CELL))
        tin = k * (len(RC.BLIND_UNITS) * rec["blind_in"] + len(RC.CELL) * (rec["v2_in"] + rec["v3_in"] + rec["v2_in"]))   # V2R at v2's figure
        tout = n * max(1, sum(rec["out"]) / len(rec["out"]))
        usd = (tin / 1e6 * cfg["price"][0] + tout / 1e6 * cfg["price"][1]) * cfg["mult"]
        line = CEILING[lane]
        if cfg["vendor"] == "anthropic":
            total_anthropic += usd
        flag = "" if usd * 1.3 <= line else "  OVER"
        if flag:
            over.append(lane)
        print(f"{lane:30s} {n:6d} {tin/1e6:7.3f} {tout/1e6:7.3f} {cfg['mult']:6.1f} {usd:8.2f} {usd*1.3:8.2f} {line:7.2f}{flag}")
    print(f"{'Anthropic lanes projected':30s} {'':6s} {'':7s} {'':7s} {'':6s} {total_anthropic:8.2f} {total_anthropic*1.3:8.2f} {ANTHROPIC_TOTAL:7.2f}")
    if over:
        sys.exit(f"PROJECTION EXCEEDS A SECTION-10 LINE AT 1.3x: {over} -- do not launch")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "project":
        cmd_project()
    else:
        getattr(RC, "cmd_" + cmd)(sys.argv[2])
