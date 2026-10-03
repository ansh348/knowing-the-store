"""
build_e1.py -- E1 Phase B: store variants and pre-verification labels.

NO API CALLS. Executes PREREG_E1.md; makes no design decisions.

Variants are represented as (base store, removed entry-id set) rather than as 201
materialised bank copies. FULL and CAT-ABLATED are written out as files for
inspection; SLOT-ABLATED is a per-(persona, question) removal set in
slot_ablations.json, because materialising ~200 near-identical 400-entry banks per
backend would add nothing an assertion cannot check. The index builder applies
removals on the fly. Logged as D4.

Labels emitted here are PRE-VERIFICATION: PN admission is by detector only.
Nothing carries a final PN label until verify_e1.py has run both halves.

Usage:  python e1_metamemory/tools/build_e1.py
"""

from __future__ import annotations

import collections
import hashlib
import io
import itertools
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(PROJECT_ROOT / "analysis" / "ontology_validation"))

from e0_common import CATEGORIES, load_joins, parse_dt, EXPIRY_WINDOW  # noqa: E402
from exp4_witnesses import supports_correct  # noqa: E402
from backends import BACKENDS, load_backend  # noqa: E402

OUT = E1 / "build"
TAU_LO, TAU_HI = 0.20, 0.80
MEM0_EXCLUDE = {"alex", "thanh", "aisha"}
NEG_ELIGIBLE = {"CURRENT-STATE", "UPCOMING"}
IN_SCOPE = NEG_ELIGIBLE | {"PAST-EVENT", "CHANGE-AWARE"}

INTENTS = {r["id"]: r["intent"]
           for r in json.load(io.open(E1 / "intents.json", encoding="utf-8"))}


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def slot_of(e):
    sk = e.get("slot_key")
    return tuple(sk) if isinstance(sk, list) and len(sk) >= 2 else None


def slot_closure(J, gold_ids):
    slots = {slot_of(J.by_id[i]) for i in gold_ids}
    slots.discard(None)
    return {e["id"] for e in J.entries if slot_of(e) in slots} | set(gold_ids)


def cat_ablation(J):
    """E0's rule: the k in {2,3} category set maximising questions fully covered.

    Deterministic; reused verbatim so the CAT-ABLATED tier carries the E0 bridge.
    """
    qs = [q for q in J.questions if INTENTS[q["id"]] in IN_SCOPE and J.gold[q["id"]]]
    best = None
    for k in (2, 3):
        for combo in itertools.combinations(CATEGORIES, k):
            s = set(combo)
            cov = sum(1 for q in qs
                      if {J.by_id[i]["category"] for i in J.gold[q["id"]]} <= s)
            key = (-cov, k, combo)
            if best is None or key < best[0]:
                best = (key, combo, cov)
    return sorted(best[1]), best[2]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    joins = load_joins()
    backend_rows = {b: collections.defaultdict(list) for b in BACKENDS}
    for b in BACKENDS:
        for r in load_backend(b):
            backend_rows[b][r["persona"]].append(r)

    variants, slot_abl, items = {}, {}, []
    cat_choice = {}

    for name in sorted(joins):
        J = joins[name]
        # ---------------- FR-Bank CAT-ABLATED choice (E0 rule, deterministic)
        combo, cov = cat_ablation(J)
        cat_choice[name] = {"categories": combo, "questions_fully_covered": cov}
        cat_removed = {e["id"] for e in J.entries if e["category"] in set(combo)}
        variants[f"frbank:{name}:CAT-ABLATED"] = sorted(cat_removed)

        # ---------------- SLOT-ABLATED, one removal set per resolvable question
        for q in J.questions:
            if INTENTS[q["id"]] not in IN_SCOPE or not J.gold[q["id"]]:
                continue
            cl = slot_closure(J, J.gold[q["id"]])
            slot_abl[f"{name}:{q['id']}"] = sorted(cl)

    # ---------------- labels, pre-verification
    def label(J, q, removed, backend, entries_by_id):
        qid, intent = q["id"], INTENTS[q["id"]]
        if intent not in IN_SCOPE:
            return "OUT-OF-SCOPE", None, {}
        if J.gold[qid] is None:
            return "UNRESOLVED", "join-unresolved", {}
        surv = lambda ids: {i for i in ids if i not in removed}
        G = surv(J.gold[qid] or set())
        exp = surv(J.expired_neg[qid] or set())
        fired = {i: s for i, s in (J.fires[qid] or {}).items() if i not in removed}

        # intent gates the negative obligation entirely (design doc 3)
        if intent in ("PAST-EVENT", "CHANGE-AWARE"):
            hi, lo = set(), set()
            if intent == "PAST-EVENT":
                G = G | exp                      # expired content is PRESENT here
        else:
            hi = {i for i, s in fired.items() if s >= TAU_HI} | exp
            lo = {i for i, s in fired.items() if s >= TAU_LO}

        if hi:
            return ("PN-CANDIDATE",
                    "with-replacement" if G else "without-replacement",
                    {i: round(fired.get(i, 1.0), 4) for i in hi})
        if lo:
            return "UNRESOLVED", "between-thresholds", {}
        return ("PRESENT", None, {}) if G else ("ABSENT", None, {})

    for name in sorted(joins):
        J = joins[name]
        ebi = {e["id"]: e for e in J.entries}
        for q in J.questions:
            qid = q["id"]
            # ---- FR-Bank: FULL, CAT-ABLATED, SLOT-ABLATED
            plan = [("FULL", set(), "easy"),
                    ("CAT-ABLATED", set(variants[f"frbank:{name}:CAT-ABLATED"]), "easy")]
            key = f"{name}:{qid}"
            if key in slot_abl:
                plan.append(("SLOT-ABLATED", set(slot_abl[key]), "hard"))
            for vname, removed, tier in plan:
                lab, sub, ev = label(J, q, removed, "frbank", ebi)
                mech = None
                if lab == "ABSENT":
                    mech = ("ablation" if vname != "FULL" else "expiry")
                    if vname == "SLOT-ABLATED":
                        mech = "ablation"
                items.append({
                    "item_id": f"frbank:{name}:{qid}:{vname}",
                    "backend": "frbank", "persona": name, "question_id": qid,
                    "variant": vname, "tier": tier,
                    "intent": INTENTS[qid], "attack_vector": q["attack_vector"],
                    "label_pre": lab, "subtype": sub, "pn_evidence": ev,
                    "absent_mechanism": mech,
                    "n_removed": len(removed),
                })
            # ---- external backends: FULL only (NATURAL-ABSENT handled separately)
            for b in ("mem0", "amem"):
                if b == "mem0" and name in MEM0_EXCLUDE:
                    continue
                rows = backend_rows[b].get(name, [])
                if not rows:
                    continue
                # PRESENT on an external backend requires sweep-verified presence
                ans = q.get("correct_answer", "")
                present = any(supports_correct(r["text"], ans) for r in rows)
                intent = INTENTS[qid]
                if intent not in IN_SCOPE:
                    lab, mech = "OUT-OF-SCOPE", None
                elif J.gold[qid] is None:
                    lab, mech = "UNRESOLVED", None
                elif present:
                    lab, mech = "PRESENT", None
                else:
                    lab, mech = "ABSENT", "ingestion-loss"
                items.append({
                    "item_id": f"{b}:{name}:{qid}:FULL",
                    "backend": b, "persona": name, "question_id": qid,
                    "variant": "FULL", "tier": "easy",
                    "intent": intent, "attack_vector": q["attack_vector"],
                    "label_pre": lab, "subtype": None, "pn_evidence": {},
                    "absent_mechanism": mech, "n_removed": 0,
                })

    jdump({"cat_ablation": cat_choice,
           "n_slot_ablations": len(slot_abl),
           "note": "SLOT-ABLATED stored as removal sets, not materialised banks (D4)"},
          OUT / "variant_plan.json")
    jdump(slot_abl, OUT / "slot_ablations.json")
    jdump(items, OUT / "items_pre.json")

    # ---------------- census
    c = collections.Counter((i["backend"], i["variant"], i["label_pre"]) for i in items)
    print("=" * 96)
    print("PRE-VERIFICATION CENSUS  (PN-CANDIDATE is not yet a label)")
    print("=" * 96)
    print(f"{'backend':8s} {'variant':14s} {'PRESENT':>8s} {'ABSENT':>7s} {'PN-CAND':>8s} "
          f"{'UNRES':>7s} {'OOS':>6s}")
    for b, v in sorted({(k[0], k[1]) for k in c}):
        print(f"{b:8s} {v:14s} {c[(b,v,'PRESENT')]:8d} {c[(b,v,'ABSENT')]:7d} "
              f"{c[(b,v,'PN-CANDIDATE')]:8d} {c[(b,v,'UNRESOLVED')]:7d} "
              f"{c[(b,v,'OUT-OF-SCOPE')]:6d}")
    hard = [i for i in items if i["tier"] == "hard"]
    print(f"\n  hard-tier items from SLOT-ABLATED: {len(hard)}  "
          f"(ABSENT {sum(1 for i in hard if i['label_pre']=='ABSENT')})")
    print(f"  slot-ablation removal sets: {len(slot_abl)}")
    print(f"  PN candidates awaiting verification: "
          f"{sum(1 for i in items if i['label_pre']=='PN-CANDIDATE')}")
    ing = [i for i in items if i["absent_mechanism"] == "ingestion-loss"]
    print(f"  ABSENT-by-ingestion-loss (external backends): {len(ing)} "
          f"(mem0 {sum(1 for i in ing if i['backend']=='mem0')}, "
          f"amem {sum(1 for i in ing if i['backend']=='amem')})")
    print(f"\nwrote {OUT}/items_pre.json, slot_ablations.json, variant_plan.json")


if __name__ == "__main__":
    main()
