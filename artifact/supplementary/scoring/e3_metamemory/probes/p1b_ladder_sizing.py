"""p1b_ladder_sizing.py -- E3 design arithmetic: what does each rung actually contain?

READ-ONLY. NO API CALLS. Derived from p1 + p2's committed outputs plus E2's split,
so the design's counts are measured rather than assumed.

Reports, per candidate rung and restricted to E2's 32 EVAL personas:
  - the label mix (the absence share moves along the ladder, and that is a confound
    the covariate adjustment has to carry)
  - how many authored questions have a VALID authored answer key at that rung
  - the two candidate item sets: KEY-REBUILD (all questions, keys rebuilt) and
    KEY-VALID-ONLY (ask a question only from the rung its key becomes valid)

Usage:  python e3_metamemory/probes/p1b_ladder_sizing.py
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
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e0_common import load_joins, parse_dt                      # noqa: E402
from p2_labels_at_t import (                                    # noqa: E402
    OLD_FIELD, RESOLVING_FIELD, TimeAnchored, as_int, session_dates,
)

OUT = Path(__file__).resolve().parent / "p1b_ladder_sizing.json"
RUNGS = (7, 10, 14, 17, 20, 24, 28, 32, 35)


def main():
    split = json.load(io.open(ROOT / "e2_metamemory" / "CALIBRATION_SPLIT.json",
                              encoding="utf-8"))
    cal = set(split["calibration_personas"])
    joins = load_joins()
    dates = session_dates()
    qs = {q["id"]: q for J in joins.values() for q in J.questions}
    TA = {p: TimeAnchored(joins[p], dates[p]) for p in joins}

    items = [i for i in json.load(io.open(ROOT / "e1_metamemory" / "build" /
                                          "items_final.json", encoding="utf-8"))
             if i["backend"] == "frbank" and i["variant"] == "FULL"
             and i.get("label", i["label_pre"]) in
             ("PRESENT", "ABSENT", "PRESENT-NEGATIVE")]
    authored = [(i["persona"], i["question_id"]) for i in items if i["question_id"] in qs]
    probes = [(i["persona"], i["question_id"]) for i in items if i["question_id"] not in qs]
    ev_auth = [x for x in authored if x[0] not in cal]
    ev_prob = [x for x in probes if x[0] not in cal]
    print(f"  eval personas {40 - len(cal)}   authored questions {len(ev_auth)}   "
          f"natural-absent probes {len(ev_prob)}")

    def key_valid(p, qid, s):
        sec, rec = TA[p].record(qid)
        if sec in ("supersession_events", "contradictions", "retractions"):
            ke = as_int(rec.get(RESOLVING_FIELD[sec]))
            return ke is None or s >= ke
        if sec == "ambiguous":
            ke = as_int(rec.get("tentative_session"))
            return ke is None or s >= ke
        if sec == "expiring_logistics":
            ed = parse_dt(str(rec.get("event_date") or "") or None)
            tn = TA[p].t_now(s)
            return not (ed is not None and tn is not None and tn < ed)
        return True

    rows = {}
    print("\n" + "=" * 100)
    print("PER-RUNG CONTENT, E2 EVAL SPLIT (32 personas)")
    print("=" * 100)
    print(f"  {'rung':>5s} {'PRESENT':>8s} {'PN':>5s} {'ABSENT':>7s} {'UNRES':>6s} "
          f"{'probes':>7s} {'n(all)':>7s} {'absence':>8s} | {'key-valid Q':>12s} "
          f"{'n(key-valid)':>13s}")
    for s in RUNGS:
        c = collections.Counter()
        kv = 0
        kv_lab = collections.Counter()
        for p, qid in ev_auth:
            lab = TA[p].label_at(qs[qid], s)[0]
            c[lab] += 1
            if key_valid(p, qid, s):
                kv += 1
                kv_lab[lab] += 1
        n_all = sum(c.values()) + len(ev_prob)
        absent = (c["ABSENT"] + len(ev_prob)) / n_all
        n_kv = kv + len(ev_prob)
        rows[s] = {"labels": dict(c), "probes": len(ev_prob), "n_all": n_all,
                   "absence_share": absent, "key_valid_questions": kv,
                   "n_key_valid": n_kv, "key_valid_labels": dict(kv_lab)}
        print(f"  {s:>5d} {c['PRESENT']:>8d} {c['PRESENT-NEGATIVE']:>5d} "
              f"{c['ABSENT']:>7d} {c['UNRESOLVED']:>6d} {len(ev_prob):>7d} "
              f"{n_all:>7d} {absent:>7.1%} | {kv:>12d} {n_kv:>13d}")

    print("\n  Reading: the absence share FALLS along the ladder as the store fills, from")
    print("  the early rungs down to the terminal one. That is a real property of a")
    print("  growing store and a confound for any rung-to-rung comparison, which is why")
    print("  the label fixed effect in the estimator is load-bearing here and was merely")
    print("  prudent in E2.")

    # ------------------------------------------------ candidate ladders, costed
    print("\n" + "=" * 100)
    print("CANDIDATE LADDERS")
    print("=" * 100)
    for name, ladder in (("R=3  (14, 22, 32) staleness", (14, 24, 32)),
                         ("R=4  (14, 20, 24, 32) staleness", (14, 20, 24, 32)),
                         ("R=4  (10, 17, 24, 32) staleness+", (10, 17, 24, 32)),
                         ("R=5  (7, 14, 20, 24, 32)", (7, 14, 20, 24, 32))):
        tot_all = sum(rows[s]["n_all"] for s in ladder if s in rows)
        tot_kv = sum(rows[s]["n_key_valid"] for s in ladder if s in rows)
        miss = tot_all - tot_kv
        if any(s not in rows for s in ladder):
            continue
        print(f"  {name:26s} n(key-rebuild) {tot_all:5d}   n(key-valid-only) {tot_kv:5d}"
              f"   keys needing rebuild {miss:5d} ({miss / tot_all:.1%})")

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"rungs": {str(k): v for k, v in rows.items()},
                   "eval_authored": len(ev_auth), "eval_probes": len(ev_prob)},
                  f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print(f"\n  written: {OUT}")


if __name__ == "__main__":
    main()
