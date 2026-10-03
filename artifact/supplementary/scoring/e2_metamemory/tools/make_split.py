"""
make_split.py -- E2: derive the calibration/eval persona split. NO API CALLS.

Defining the split is permitted in the design phase; eliciting on it is not.
This script reads only E1's committed `build/items_final.json` and writes
`e2_metamemory/CALIBRATION_SPLIT.json`. It touches no store and no model.

Procedure (deterministic, no RNG -- there is nothing to seed):

  1. score every persona by PN rate over its FR-Bank scoreable items;
  2. sort by PN rate ascending, persona name as tiebreak;
  3. cut into 8 strata of 5;
  4. from each stratum take the persona whose item count is nearest that
     stratum's median count, alphabetical on ties.

Stratifying on PN density is the choice that matters: tau_NOK is fitted against
PN items, so a calibration split that under-samples PN personas would fit it on
almost nothing. Backend stratification is degenerate at the persona level -- all
40 personas exist in FR-Bank and A-MEM, 37 in Mem0 -- so it is reported as a
consequence rather than imposed as a constraint.

Usage:  python e2_metamemory/tools/make_split.py
"""

from __future__ import annotations

import collections
import io
import json
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"
E2 = ROOT / "e2_metamemory"
OUT = E2 / "CALIBRATION_SPLIT.json"

SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}
N_CAL = 8
MEM0_EXCLUDED = {"alex", "thanh", "aisha"}


def main():
    items = json.load(io.open(E1 / "build" / "items_final.json", encoding="utf-8"))
    lab = lambda i: i.get("label", i["label_pre"])                     # noqa: E731
    fr = [i for i in items if i["backend"] == "frbank" and lab(i) in SCOREABLE]

    per = collections.defaultdict(collections.Counter)
    for i in fr:
        per[i["persona"]][lab(i)] += 1

    rows = []
    for p, c in per.items():
        n = sum(c.values())
        rows.append({"persona": p, "n_items": n, "n_pn": c["PRESENT-NEGATIVE"],
                     "n_present": c["PRESENT"], "n_absent": c["ABSENT"],
                     "pn_rate": c["PRESENT-NEGATIVE"] / n})
    rows.sort(key=lambda r: (r["pn_rate"], r["persona"]))
    assert len(rows) == 40, f"expected 40 personas, got {len(rows)}"

    stride = len(rows) // N_CAL
    cal = []
    for s in range(N_CAL):
        stratum = rows[s * stride:(s + 1) * stride]
        med = st.median([r["n_items"] for r in stratum])
        cal.append(min(stratum, key=lambda r: (abs(r["n_items"] - med), r["persona"])))
    cal_names = sorted(r["persona"] for r in cal)
    eva = [r for r in rows if r["persona"] not in set(cal_names)]

    def agg(rs):
        return {"personas": len(rs), "items": sum(r["n_items"] for r in rs),
                "pn": sum(r["n_pn"] for r in rs),
                "present": sum(r["n_present"] for r in rs),
                "absent": sum(r["n_absent"] for r in rs)}

    c, e = agg(cal), agg(eva)
    tot_items, tot_pn = c["items"] + e["items"], c["pn"] + e["pn"]
    out = {
        "no_api_calls": True,
        "derived_from": "e1_metamemory/build/items_final.json @ tag e1-complete",
        "scope": "FR-Bank scoreable items, all variants",
        "procedure": ("sort personas by PN rate asc (name tiebreak); cut into 8 strata "
                      "of 5; from each stratum take the persona whose item count is "
                      "nearest the stratum median, alphabetical on ties. No RNG."),
        "stratified_on": "PN density (drives tau_NOK) and item count (drives tau_FOK)",
        "backend_stratification": (
            "degenerate at the persona level: all 40 personas exist in FR-Bank and "
            "A-MEM, 37 in Mem0. Reported as a consequence, not imposed."),
        "calibration_personas": cal_names,
        "eval_personas": sorted(r["persona"] for r in eva),
        "calibration": c, "eval": e,
        "balance": {"calibration_item_share": c["items"] / tot_items,
                    "calibration_pn_share": c["pn"] / tot_pn,
                    "share_gap_pp": abs(c["items"] / tot_items - c["pn"] / tot_pn) * 100},
        "mem0_excluded_in_calibration": sorted(set(cal_names) & MEM0_EXCLUDED),
        "mem0_consequence": None,
        "per_persona": rows,
    }
    n_mex = len(out["mem0_excluded_in_calibration"])
    out["mem0_consequence"] = (
        f"{n_mex} of the 3 Mem0-excluded personas fall in calibration, so a Mem0 "
        f"secondary arm would calibrate on {N_CAL - n_mex} personas and evaluate on "
        f"{40 - N_CAL - (3 - n_mex)}. Costs calibration, not eval.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print(f"calibration ({c['personas']}): {', '.join(cal_names)}")
    print(f"  items {c['items']} ({c['items']/tot_items:.1%})  PN {c['pn']} "
          f"({c['pn']/tot_pn:.1%})  share gap {out['balance']['share_gap_pp']:.2f}pp")
    print(f"eval ({e['personas']}): items {e['items']}, PN {e['pn']}, "
          f"PRESENT {e['present']}, ABSENT {e['absent']}")
    print(f"  {out['mem0_consequence']}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
