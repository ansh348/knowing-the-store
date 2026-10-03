# -*- coding: utf-8 -*-
"""e3_intent_table.py -- program R126, Phase 4.6 (2026-09-20): the state-by-intent-by-label count table for the 661 questions of the full obligation
set, from the manifests and the ground-truth join, so Appendix E.3's sentence ("a staleness judgment and an obligation judgment coincide") can be
corrected to what the table shows. NO MODEL CALL. Reads the recorded objects reviews/v19/tools/posthoc_b4_intent.py reads: ds_common.load_cell
(the 661 with intent, label, the manifest's obligation state and the gold entries) and resp_common.true_flags / variant_ids (the ground-truth
join's lifecycle marks on every FR-Bank entry, restricted to the store version the question was asked of).

Per question: intent (the constructed intent); label (PRESENT-NEGATIVE, PRESENT, ABSENT); state:
  PN        the manifest's obligation state (the item's `state`: sup / ret / exp), the forbidding record's state;
  PRESENT   whether the question's own slot(s), in its store version, also hold a non-active record: superseded / retracted / expired (the first of
            retracted, superseded, expired when several marks are present, as Definition 1 labels a record), else 'active only';
  ABSENT    'none' (the gold entry is not in the store version; asserted); PRESENT questions the join aligns no gold entry to read 'unaligned'.
Writes reviews/v22/results/e3_intent_table.json (the table, the per-intent PN counts, the PRESENT-with-a-non-active-own-slot counts, and the
non-exclusive per-mark counts for PRESENT so the C.2 reading of 4 CHANGE-intent licensed questions with a superseded own slot can be checked).
Usage: python reviews/v22/tools/e3_intent_table.py
"""
from __future__ import annotations

import collections
import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "resp_review/tools", "ds_downstream/tools", "r74/tools"):
    sys.path.insert(0, str(ROOT / p))
from ds_common import load_cell  # noqa: E402
from resp_common import true_flags, variant_ids  # noqa: E402

OUT = ROOT / "reviews" / "v22" / "results" / "e3_intent_table.json"
INTENTS = ["CURRENT-STATE", "UPCOMING", "PAST-EVENT", "CHANGE-AWARE"]
LABELS = ["PRESENT-NEGATIVE", "PRESENT", "ABSENT"]
STATES = ["superseded", "retracted", "expired", "active only", "unaligned", "none"]
PN_STATE = {"sup": "superseded", "ret": "retracted", "exp": "expired"}


def own_slot_marks(it, fl):
    """The non-active marks carried by any entry in the question's own slot(s), in the store version the question was asked of."""
    present = set(variant_ids(it))
    fp = {e: d for e, d in fl[it["persona"]].items() if e in present}
    gold = it.get("gold") or []
    ents = [fp[e] for e in gold if e in fp]
    if not ents:
        return None
    slots = {d["slot"] for d in ents}
    marks = set()
    for d in fp.values():
        if d["slot"] in slots:
            for m in ("retracted", "superseded", "expired"):
                if d[m]:
                    marks.add(m)
    return marks


def main():
    items = load_cell(); assert len(items) == 661, len(items)
    fl = true_flags()
    assert {it["intent"] for it in items} <= set(INTENTS) and {it["label"] for it in items} <= set(LABELS)
    counts = collections.Counter()
    present_marks = collections.Counter()   # (intent, mark), non-exclusive, PRESENT questions
    for it in items:
        if it["label"] == "PRESENT-NEGATIVE":
            st = PN_STATE[it["state"]]
        elif it["label"] == "PRESENT":
            marks = own_slot_marks(it, fl)
            if marks is None:        # the join aligns no gold entry (the ten PAST-EVENT questions answered by an expired event, AV2)
                st = "unaligned"
            else:
                for m in marks:
                    present_marks[(it["intent"], m)] += 1
                st = next((m for m in ("retracted", "superseded", "expired") if m in marks), "active only")
        else:
            assert own_slot_marks(it, fl) is None, it["item_id"]
            st = "none"
        counts[(it["intent"], it["label"], st)] += 1
    assert sum(counts.values()) == 661
    pn_by_intent = {i: sum(n for (ii, l, s), n in counts.items() if ii == i and l == "PRESENT-NEGATIVE") for i in INTENTS}
    present_nonactive = {i: sum(n for (ii, l, s), n in counts.items() if ii == i and l == "PRESENT" and s not in ("active only", "unaligned")) for i in INTENTS}
    res = {"n": 661, "intents": INTENTS, "labels": LABELS, "states": STATES,
           "counts": {f"{i}|{l}|{s}": n for (i, l, s), n in sorted(counts.items())},
           "pn_by_intent": pn_by_intent,
           "present_with_a_non_active_own_slot_by_intent": present_nonactive,
           "present_own_slot_marks_non_exclusive": {f"{i}|{m}": n for (i, m), n in sorted(present_marks.items())},
           "method": "PN: the manifest's obligation state (item.state). PRESENT: the marks the ground-truth join puts on any entry of the question's own "
                     "slot(s) in its store version (resp_common.true_flags restricted to variant_ids); the first of retracted, superseded, expired when "
                     "several, else 'active only'. ABSENT: no gold entry in the store version (asserted)."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(f"{'intent':14s} {'label':17s} " + " ".join(f"{s:>12s}" for s in STATES) + "   total")
    for i in INTENTS:
        for l in LABELS:
            row = [counts.get((i, l, s), 0) for s in STATES]
            if sum(row):
                print(f"{i:14s} {l:17s} " + " ".join(f"{n:12d}" for n in row) + f"   {sum(row)}")
    print("PN by intent:", pn_by_intent)
    print("PRESENT questions whose own slot also holds a non-active record, by intent:", present_nonactive)
    print("PRESENT own-slot marks, non-exclusive:", dict(sorted(present_marks.items())))
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
