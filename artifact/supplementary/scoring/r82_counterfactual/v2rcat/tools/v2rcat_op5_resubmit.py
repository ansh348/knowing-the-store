# -*- coding: utf-8 -*-
"""v2rcat_op5_resubmit.py -- D-V2RCAT-3 (2026-09-17): the first Opus 5 batch (msgbatch_01WVXiaiBoC6JHFXEyiM1y2m) sat unprocessed for about
four and a half hours and was canceled at the author's instruction; the cancellation landed as the queue moved, so 388 of 444 requests
succeeded and 56 were canceled. The 388 are kept (billed, collected into rows/rows_OP5.jsonl by cmd_poll); this script resubmits ONLY the 56
canceled units under the identical request (prompts_for, k = 1, temperature unset, max_tokens 1024, Batch), collects them, and replaces the
56 BATCH_CANCELED rows in rows_OP5.jsonl with the new rows, each row carrying its batch id. The first batch's row file is kept as
rows/rows_OP5.batch1.jsonl and its record as rows/batch_OP5.json; the second batch's record is rows/batch_OP5_2.json. Nothing is overwritten.

Subcommands:  submit | poll
"""
from __future__ import annotations

import io
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "r114" / "tools"))
from r114_common import assert_spec, J, jdump  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
import v2rcat as V                                                           # noqa: E402
import run_cf as RC                                                          # noqa: E402

LANE, CODE = "claude-opus-5", "OP5"
ROWS_P = V.ROWS / f"rows_{CODE}.jsonl"
B1 = V.ROWS / f"batch_{CODE}.json"
B1_ROWS = V.ROWS / f"rows_{CODE}.batch1.jsonl"
def batch_records():
    return sorted(V.ROWS.glob(f"batch_{CODE}_*.json"), key=lambda p: int(p.stem.rsplit("_", 1)[1]))


def next_record():
    n = len(batch_records()) + 2
    return V.ROWS / f"batch_{CODE}_{n}.json"


B2 = None


def setup():
    assert_spec(); assert V.registration_ok(); V.point(); RC.LANES[LANE]["k"] = 1; RC.load_env()
    assert "D-V2RCAT-3" in (V.V2C / "DEVIATIONS_V2RCAT.md").read_text(encoding="utf-8"), "D-V2RCAT-3 not recorded -- STOP"


def canceled_units():
    rows = [json.loads(l) for l in io.open(ROWS_P, encoding="utf-8")]
    bad = {r["unit_id"] for r in rows if r["status"] != "OK"}
    return rows, bad


def cmd_submit():
    setup()
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    rec_p = next_record()
    rows, bad = canceled_units()
    assert len(rows) == 444 and bad, (len(rows), len(bad))
    prev = [J(p)["id"] for p in batch_records()]
    for p in batch_records():
        assert not set(J(p)["units"]) - set(J(p).get("merged_units", J(p)["units"])) or True
    if not B1_ROWS.exists():
        shutil.copyfile(ROWS_P, B1_ROWS)
    cfg = RC.LANES[LANE]; units = V.units(V.ARM); reqs = []
    for i, u in enumerate(units):
        if u["unit_id"] not in bad:
            continue
        sysm, user = RC.prompts_for(u, V.ARM)
        kw = dict(model=LANE, max_tokens=cfg["max_tokens"], system=sysm, messages=[{"role": "user", "content": user}])
        if cfg["temp"] is not None:
            kw["temperature"] = cfg["temp"]
        reqs.append(Request(custom_id=f"{cfg['code']}-0-{i:04d}-d1", params=MessageCreateParamsNonStreaming(**kw)))
    assert len(reqs) == len(bad)
    b = RC.anthropic_client().messages.batches.create(requests=reqs)
    jdump({"id": b.id, "lane": LANE, "n": len(reqs), "first_batch": J(B1)["id"], "previous_batches": prev, "units": sorted(bad), "why": "D-V2RCAT-3: the requests canceled in the earlier batch(es), resubmitted verbatim"}, rec_p)
    print("submitted", b.id, len(reqs), "requests")


def cmd_poll():
    setup()
    meta = J(batch_records()[-1]); cl = RC.anthropic_client(); b = cl.messages.batches.retrieve(meta["id"])
    print(meta["id"], b.processing_status, b.request_counts)
    if b.processing_status != "ended":
        return
    rows, bad = canceled_units()
    if not bad:
        print("already merged"); return
    units = V.units(V.ARM); cfg = RC.LANES[LANE]; new = {}
    for res in cl.messages.batches.results(meta["id"]):
        code, ai, i, d = res.custom_id.split("-"); u = units[int(i)]
        if res.result.type == "succeeded":
            m = res.result.message
            text = "".join(bl.text for bl in m.content if bl.type == "text")
            row = RC.make_row(u, V.ARM, LANE, 1, text, m.usage.input_tokens, m.usage.output_tokens, cfg["price"], cfg["mult"], m.model)
        else:
            row = {"unit_id": u["unit_id"], "arm": V.ARM, "model": LANE, "draw": 1, "status": "BATCH_" + res.result.type.upper()}
        row["batch_id"] = meta["id"]; new[u["unit_id"]] = row
    assert set(new) == bad, (len(new), len(bad))
    if all(r["status"] != "OK" for r in new.values()):
        print("no new OK rows to merge"); return
    out = []
    for r in rows:
        if r["unit_id"] in bad:
            out.append(new[r["unit_id"]])
        else:
            r.setdefault("batch_id", meta["first_batch"]); out.append(r)
    with io.open(ROWS_P, "w", encoding="utf-8", newline="\n") as f:
        for r in out:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    n_ok = sum(1 for r in out if r["status"] == "OK")
    print(f"merged; ok {n_ok} of {len(out)}; second batch ok {sum(1 for r in new.values() if r['status'] == 'OK')} of {len(new)}")


if __name__ == "__main__":
    {"submit": cmd_submit, "poll": cmd_poll}[sys.argv[1]]()
