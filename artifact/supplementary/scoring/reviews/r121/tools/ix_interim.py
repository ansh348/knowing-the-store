# -*- coding: utf-8 -*-
"""ix_interim.py -- program R121: the author's interim read of the three completed lanes (GPT-4.1 mini, Haiku 4.5, GPT-5.6 Luna)
and the offline lookups, taken while the Opus 5 batch was still in progress (the author's instruction of 2026-09-19: the batch is
submitted, the registration frozen, no analysis choice open, so the early look can influence nothing). Uses ix_score's functions
unchanged; does not touch the Opus lane; writes cf2/results/cf_scores_ix_interim_3lanes.json and one ledger note. NO MODEL CALL."""
from __future__ import annotations

import datetime as dt
import io
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "r121" / "tools"))
import ix_score as S  # noqa: E402
from common_e1r import auroc, boot_cluster  # noqa: E402

READERS = ("MINI", "H45", "LUNA")
OUT = S.CF2 / "results" / "cf_scores_ix_interim_3lanes.json"
LEDGER = S.CF2 / "NUMBERS_CF2.md"
TOL = S.TOL


def r4(x):
    return round(float(x), 4)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    S.R.setup()
    U = S.R.units_all(); wilson = S.load_wilson()
    meta = json.loads((S.ROWS / "batch_IX_OP5.json").read_text())
    res = {"interim": True, "note": "three completed lanes; Opus 5 batch in progress at the time of the read", "opus_batch": meta["id"], "when": dt.datetime.now().isoformat(timespec="seconds"),
           "readers": {}, "lookups": {}, "provisional": {}}
    L = {}
    for pop in ("A", "B"):
        up = {arm: [u for u in U if u["population"] == pop and u["arm"] == arm] for arm in ("P0", "P1")}
        lk = S.lookups(up["P0"]); L[pop] = {}
        for name in ("name", "keyword", "oracle"):
            e = S.estimands(lk[name], up["P0"], wilson); L[pop][name] = e; res["lookups"].setdefault(pop, {})[name] = S.strip(e)
        res["lookups"][pop]["question_length"] = S.qlen(up["P0"])
        for lane in READERS:
            rd = res["readers"].setdefault(lane, {"name": S.NAMES[lane]}); rd[pop] = {}; vec = {}
            for arm in ("P0", "P1"):
                v = S.scores_for(lane, up[arm]); assert not np.isnan(v).any(), (lane, pop, arm)
                e = S.estimands(v, up[arm], wilson); vec[arm] = e; rd[pop][arm] = S.strip(e)
            b = vec["P0"]["_vectors"]["orig"]; i = vec["P1"]["_vectors"]["orig"]
            rd[pop]["p1_minus_p0_cell1_vs_cell2"] = {"p0": vec["P0"]["cell1_vs_cell2"]["auroc"], "p1": vec["P1"]["cell1_vs_cell2"]["auroc"], "delta": r4(auroc(i[0], i[1]) - auroc(b[0], b[1])),
                                                    "ci_pair": boot_cluster(b[0], i[0], b[1], b[2]), "ci_persona": boot_cluster(b[0], i[0], b[1], b[3])}
    P = res["provisional"]
    P["P-I1 (three of four models)"] = {lane: {"auroc": res["readers"][lane]["A"]["P0"]["same_store"]["auroc"], "within_tol": res["readers"][lane]["A"]["P0"]["same_store"]["within_tolerance_of_half"]} for lane in READERS}
    h = res["readers"]["H45"]["A"]["P1"]["same_store"]
    P["P-I2 (Haiku part)"] = {"auroc": h["auroc"], "ci_persona": [r4(h["ci_persona"]["ci_lo"]), r4(h["ci_persona"]["ci_hi"])], "ci_pair": [r4(h["ci_pair"]["ci_lo"]), r4(h["ci_pair"]["ci_hi"])],
                              "separates": bool(h["auroc"] > 0.5 and h["ci_pair"]["ci_lo"] > 0.5 and h["ci_persona"]["ci_lo"] > 0.5)}
    P["P-I3"] = {pop: {"auroc": res["lookups"][pop]["name"]["same_store"]["auroc"], "within_tol": res["lookups"][pop]["name"]["same_store"]["within_tolerance_of_half"]} for pop in ("A", "B")}
    P["P-I5 (three of four models)"] = {lane: {pop: res["readers"][lane][pop]["p1_minus_p0_cell1_vs_cell2"]["delta"] for pop in ("A", "B")} for lane in READERS}
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1, sort_keys=True, default=float) + "\n")
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"\n### 14d-interim — the author's interim read ({res['when']}): `ix_interim.py` scored the three completed lanes (MINI, H45, LUNA) and the offline lookups while the Opus 5 batch `{meta['id']}` was still in progress; the registration was frozen and no analysis choice was open, so the read could influence nothing. Written to `results/cf_scores_ix_interim_3lanes.json`; the Opus lane untouched; the full scoring (§14d) follows when it ends.\n")

    def ci(c): return f"[{c['ci_lo']:.3f}, {c['ci_hi']:.3f}]"
    print(f"\nINTERIM READ ({res['when']}) — three lanes + lookups; Opus 5 batch in progress\n")
    print(f"{'reader':13s} {'pop':3s} {'arm':3s} | {'same-store':>10s} {'W/T/L':>9s} {'[persona]':>16s} | {'interaction':>11s} {'[persona]':>16s} {'[pair]':>16s} | {'pooled':>6s} {'[persona]':>16s} | {'c1v2':>6s}")
    for lane in READERS + ("name", "keyword", "oracle"):
        for pop in ("A", "B"):
            for arm in (("P0", "P1") if lane in READERS else ("--",)):
                e = res["readers"][lane][pop][arm] if lane in READERS else res["lookups"][pop][lane]
                s, it, pl = e["same_store"], e["interaction"], e["pooled"]
                print(f"{(S.NAMES[lane] if lane in READERS else lane + ' lookup'):13s} {pop:3s} {arm:3s} | {s['auroc']:10.4f} {'/'.join(map(str, s['wtl'])):>9s} {ci(s['ci_persona']):>16s} | {it['mean']:+11.4f} {ci(it['ci_persona']):>16s} {ci(it['ci_pair']):>16s} | {pl['auroc']:6.4f} {ci(pl['ci_persona']):>16s} | {e['cell1_vs_cell2']['auroc']:6.4f}")
    print("\nprovisional:")
    for k, v in P.items():
        print(" ", k, json.dumps(v))
    print(f"\n-> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
