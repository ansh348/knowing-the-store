"""
build_cells.py -- E3 STEP 2: the registered (item, rung) cells. NO API CALLS.

Executes PREREG_E3.md sections 1-3; makes no design decisions. Writes
CELLS_E3.json and nothing else.

FOUR ASSERTIONS, all fatal, all run before a single cell is written:

  A1  session ids contiguous and monotone 1..35 on all 40 personas
      (PREREG_E3 section 1 assertion 1; replay is by id, never by date -- D46)
  A2  NESTING: alive(s1) subset alive(s2) for every s1 < s2, per persona
      (PREREG_E3 section 1 assertion 2). A ladder that is not nested is not a
      timeline.
  A3  TERMINAL ANCHOR: at the FULL store the pipeline reproduces E1's committed
      FULL-variant label on 178/178 authored questions (PREREG_E3 section 3).
      Asserted at s=35, not at ladder rung 32 -- see D53-E3.
  A4  every hand verdict the ladder needs is already held in
      e1_metamemory/tools/verify_verdicts.py. Zero new adjudications (D52-E3).

Usage:  python e3_metamemory/tools/build_cells.py
"""

from __future__ import annotations

import collections
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e2_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e0_common import load_joins                                   # noqa: E402
from e3_common import (E1, E3, RUNGS, SCOREABLE, LabelAtT,         # noqa: E402
                       Snapshot, apply_verdicts, assert_replay_order,
                       jdump, jload, session_dates)
from verify_verdicts import MEMBERSHIP, SEMANTIC                   # noqa: E402

ANCHOR_RUNG = 35


def main():
    from e2_common import load_items                               # noqa: PLC0415
    split = jload(ROOT / "e2_metamemory" / "CALIBRATION_SPLIT.json")
    cal = set(split["calibration_personas"])

    joins = load_joins()
    dates = session_dates()
    assert_replay_order(dates)
    print(f"A1 session ids contiguous 1..35 on {len(dates)}/40 personas   PASS")

    snaps = {p: Snapshot(p, dates[p]) for p in joins}
    LA = {p: LabelAtT(joins[p], snaps[p]) for p in joins}

    # ---- A2 nesting
    ladder = sorted(set(RUNGS) | {ANCHOR_RUNG})
    for p, S in snaps.items():
        prev = None
        for r in ladder:
            a = S.alive(r)
            if prev is not None:
                assert prev <= a, f"{p}: alive({r}) does not contain alive(prev)"
            prev = a
    print(f"A2 nesting alive(s1) subset alive(s2) over {ladder}   PASS "
          f"({len(snaps)} personas)")

    # ---- the item base: FULL-variant scoreable, authored questions + probes
    base = [i for i in load_items() if i["variant"] == "FULL"]
    qtext = {(i["persona"], i["question_id"]): i["question"] for i in base}
    e1_label = {(i["persona"], i["question_id"]): i["label_final"] for i in base}
    authored = sorted(k for k in qtext if k[1] in
                      {q["id"] for J in joins.values() for q in J.questions})
    probes = sorted(k for k in qtext if k not in set(authored))
    print(f"item base: {len(base)} FULL items = {len(authored)} authored "
          f"+ {len(probes)} natural-absent probes")

    # ---- A3 terminal anchor
    agree, mism = 0, collections.Counter()
    for p, qid in authored:
        lab, sub, ev = LA[p].label(qid, ANCHOR_RUNG)
        lab, sub, _m = apply_verdicts(lab, sub, ev, p, qid, MEMBERSHIP, SEMANTIC)
        if lab == e1_label[(p, qid)]:
            agree += 1
        else:
            mism[(lab, e1_label[(p, qid)])] += 1
    assert agree == len(authored), (
        f"A3 TERMINAL ANCHOR FAILED: {agree}/{len(authored)}; {dict(mism)}")
    print(f"A3 terminal anchor at s={ANCHOR_RUNG} vs E1 committed FULL label: "
          f"{agree}/{len(authored)}   PASS")

    # ---- A4 verdict coverage over the ladder
    need_s, need_m = set(), set()
    for p, qid in authored:
        for r in RUNGS:
            lab, sub, ev = LA[p].label(qid, r)
            if lab != "PN-CANDIDATE":
                continue
            need_s.add((p, qid))
            need_m.update((p, qid, i) for i in ev["hi"])
    miss_s = sorted(need_s - set(SEMANTIC))
    miss_m = sorted(need_m - set(MEMBERSHIP))
    assert not miss_s and not miss_m, (
        f"A4 FAILED: {len(miss_s)} semantic, {len(miss_m)} membership unverified")
    print(f"A4 hand verdicts: needs {len(need_s)} semantic + {len(need_m)} "
          f"membership, all held   PASS  (zero new adjudications)")

    # ------------------------------------------------------------- the cells
    cells, excluded = [], []
    for r in RUNGS:
        for p, qid in authored:
            kv = LA[p].key_valid(qid, r)
            lab, sub, ev = LA[p].label(qid, r)
            lab, sub, members = apply_verdicts(lab, sub, ev, p, qid,
                                               MEMBERSHIP, SEMANTIC)
            rec = {"cell_id": f"{p}:{qid}:R{r}", "persona": p, "question_id": qid,
                   "rung": r, "question": qtext[(p, qid)], "kind": "authored",
                   "label": lab, "subtype": sub, "intent": ev["intent"],
                   "section": ev.get("section"), "pre_event": ev.get("pre_event"),
                   "resolving_session": ev.get("resolving_session"),
                   "pn_members": members,
                   "split": "calibration" if p in cal else "eval",
                   "e1_full_label": e1_label[(p, qid)]}
            if not kv:
                excluded.append({**rec, "reason": "key-not-yet-valid"})
                continue
            if lab not in SCOREABLE:
                excluded.append({**rec, "reason": f"not-scoreable:{lab}"})
                continue
            cells.append(rec)
        for p, qid in probes:
            cells.append({"cell_id": f"{p}:{qid}:R{r}", "persona": p,
                          "question_id": qid, "rung": r,
                          "question": qtext[(p, qid)], "kind": "probe",
                          "label": "ABSENT", "subtype": None, "intent": None,
                          "section": None, "pre_event": False,
                          "resolving_session": None, "pn_members": [],
                          "split": "calibration" if p in cal else "eval",
                          "e1_full_label": e1_label[(p, qid)]})

    # ---------------------------------------------------------------- report
    print("\n" + "=" * 96)
    print("REGISTERED CELLS")
    print("=" * 96)
    print(f"  {'rung':>5s} {'split':>12s} {'PRESENT':>9s} {'PN':>5s} {'ABSENT':>8s} "
          f"{'n':>6s} {'excl':>6s} {'absence':>9s}")
    for r in RUNGS:
        for sp in ("eval", "calibration"):
            rows = [c for c in cells if c["rung"] == r and c["split"] == sp]
            lab = collections.Counter(c["label"] for c in rows)
            ex = sum(1 for e in excluded if e["rung"] == r and e["split"] == sp)
            n = len(rows)
            print(f"  {r:>5d} {sp:>12s} {lab['PRESENT']:>9d} "
                  f"{lab['PRESENT-NEGATIVE']:>5d} {lab['ABSENT']:>8d} {n:>6d} "
                  f"{ex:>6d} {lab['ABSENT']/n:>8.1%}")
    ev_cells = [c for c in cells if c["split"] == "eval"]
    ca_cells = [c for c in cells if c["split"] == "calibration"]
    exr = collections.Counter(e["reason"] for e in excluded)
    print(f"\n  TOTAL registered: {len(cells)}  = eval {len(ev_cells)} "
          f"+ calibration {len(ca_cells)}")
    print(f"  excluded: {len(excluded)}  {dict(exr)}")
    pn_all = sum(1 for c in cells if c["label"] == "PRESENT-NEGATIVE")
    print(f"  obligation mass: {pn_all} PN cells "
          f"({sum(1 for c in ev_cells if c['label']=='PRESENT-NEGATIVE')} eval)")

    # PREREG section 2's frozen property, asserted rather than asserted-in-prose
    bad = [c for c in cells
           if c["label"] == "PRESENT-NEGATIVE" and c["kind"] == "authored"
           and not LA[c["persona"]].key_valid(c["question_id"], c["rung"])]
    assert not bad, f"a PN cell is key-invalid: {bad[:3]}"
    print(f"  every PN cell key-valid by construction   PASS")

    jdump({"prereg": "PREREG_E3.md", "rungs": list(RUNGS),
           "anchor_rung": ANCHOR_RUNG, "n_cells": len(cells),
           "n_excluded": len(excluded), "exclusion_reasons": dict(exr),
           "assertions": {"A1_session_ids": True, "A2_nesting": True,
                          "A3_terminal_anchor": f"{agree}/{len(authored)}",
                          "A4_verdicts_held": True},
           "cells": cells, "excluded": excluded}, E3 / "CELLS_E3.json")
    print("\nwrote CELLS_E3.json")


if __name__ == "__main__":
    main()
