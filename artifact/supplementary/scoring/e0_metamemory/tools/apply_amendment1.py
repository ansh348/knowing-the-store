"""
apply_amendment1.py -- apply Amendment 1 to the item set.

NO API CALLS. Run before any elicitation call.

Three changes, all additive to the item records; nothing is destroyed:

  1. Sensitivity set. The 3 ABSENT items flagged by the independent lexical check
     are tagged `lex_flagged`. Their labels do NOT change. Gate metrics will be
     reported a second time with these excluded.
  2. ABSENT mechanism split. Each ABSENT item is tagged `absent_mechanism`:
     "ablation" (the gold was ablated away) or "expiry" (an AV2 question whose gold
     answer is itself a negative and whose expired content was ablated away).
     Descriptive; no pass/fail reads on the subsets.
  3. PRESENT-NEGATIVE verification. Items failing per-item verification are
     relabelled UNRESOLVED. `label_step1` preserves the pre-amendment label.
"""

from __future__ import annotations

import collections

from e0_common import E0, jdump, jload, load_joins

ITEMS = E0 / "items.json"


def main():
    items = jload(ITEMS)
    ver = {r["item_id"]: r for r in jload(E0 / "pn_verification.json")["items"]}
    lex_flagged = {r["item_id"] for r in jload(E0 / "step1_census.json")["absent_lex_leak"]}
    joins = load_joins()

    moved = 0
    for it in items:
        it.setdefault("label_step1", it["label"])

        # ---- change 3: PN verification
        if it["label_step1"] == "PRESENT-NEGATIVE":
            v = ver[it["item_id"]]
            it["pn_verified"] = v["verified"]
            it["pn_n_admitting"] = v["n_admitting"]
            it["pn_n_verified_true"] = v["n_verified_true"]
            if not v["verified"]:
                it["label"] = "UNRESOLVED"
                it["subtype"] = "pn-verification-failed"
                moved += 1

        # ---- change 1: sensitivity set
        it["lex_flagged"] = it["item_id"] in lex_flagged

        # ---- change 2: ABSENT mechanism
        if it["label"] == "ABSENT":
            J = joins[it["persona"]]
            gold_full = J.gold[it["question_id"]]
            it["absent_mechanism"] = "expiry" if not gold_full else "ablation"
        else:
            it["absent_mechanism"] = None

    jdump(items, ITEMS)

    cen = collections.Counter(i["label"] for i in items)
    was = collections.Counter(i["label_step1"] for i in items)
    scoreable = cen["PRESENT"] + cen["ABSENT"] + cen["PRESENT-NEGATIVE"]

    print("=" * 74)
    print("AMENDMENT 1 APPLIED")
    print("=" * 74)
    print(f"{'cell':20s} {'Step 1':>8s} {'now':>8s}")
    for k in ("PRESENT", "ABSENT", "PRESENT-NEGATIVE", "UNRESOLVED"):
        print(f"{k:20s} {was[k]:8d} {cen[k]:8d}")
    print(f"{'scoreable':20s} {was['PRESENT']+was['ABSENT']+was['PRESENT-NEGATIVE']:8d} {scoreable:8d}")
    print(f"\n  PN items relabelled to UNRESOLVED: {moved}")

    mech = collections.Counter(i["absent_mechanism"] for i in items if i["label"] == "ABSENT")
    print(f"  ABSENT mechanism split: {dict(mech)}")
    print(f"  lex-flagged ABSENT items (sensitivity set): "
          f"{sum(1 for i in items if i['lex_flagged'])}")

    sub = collections.Counter(i["subtype"] for i in items if i["label"] == "PRESENT-NEGATIVE")
    print(f"  PRESENT-NEGATIVE subtypes now: {dict(sub)}")

    per_av = collections.defaultdict(collections.Counter)
    for i in items:
        per_av[i["attack_vector"]][i["label"]] += 1

    gates = {"ABSENT>=60": cen["ABSENT"] >= 60,
             "PRESENT>=60": cen["PRESENT"] >= 60,
             "PRESENT-NEGATIVE>=60": cen["PRESENT-NEGATIVE"] >= 60}
    print("\n  gates:")
    for k, v in gates.items():
        note = "" if v else ("  (accepted -- NOK exploratory and ungated)"
                             if "NEGATIVE" in k else "  <-- ESCALATE")
        print(f"    {k:24s} {'PASS' if v else 'FAIL'}{note}")

    jdump({
        "census": dict(cen), "census_step1": dict(was), "scoreable": scoreable,
        "pn_relabelled_to_unresolved": moved,
        "absent_mechanism": dict(mech),
        "lex_flagged_items": sorted(lex_flagged),
        "pn_subtypes": dict(sub),
        "per_attack_vector": {k: dict(v) for k, v in sorted(per_av.items())},
        "gates": gates,
        "no_api_calls": True,
    }, E0 / "amendment1_census.json")
    print(f"\nwrote {ITEMS} and {E0/'amendment1_census.json'}")


if __name__ == "__main__":
    main()
