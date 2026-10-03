"""
dryrun.py -- E1 Phase 0 item 4: construction dry-run and 40-persona cell projection.

NO API CALLS.

Builds one persona end-to-end through the FR-Bank variants (FULL, CAT-ABLATED,
SLOT-ABLATED) under the intent-conditional taxonomy, measures the slot-ablation
blast radius and the post-ablation lexical contamination sweep, then projects cell
counts for the full 40-persona build.

SLOT-ABLATED, as specified in Phase B: remove the question's gold-supporting
entries AND their sibling slot-key copies. The sibling closure is required because
E0 measured that the extractor emits 3-5 near-duplicate entries per fact, so
removing the resolved gold set alone leaves the content behind.

Usage:  python e1_metamemory/tools/dryrun.py [persona]
"""

from __future__ import annotations

import collections
import io
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(PROJECT_ROOT / "analysis" / "ontology_validation"))

from e0_common import CATEGORIES, jdump, jload, load_joins  # noqa: E402
from exp4_witnesses import supports_correct  # noqa: E402

INTENTS = {r["id"]: r["intent"] for r in jload(E1 / "intents.json")}
NEG_ELIGIBLE = {"CURRENT-STATE", "UPCOMING"}
IN_SCOPE = NEG_ELIGIBLE | {"PAST-EVENT", "CHANGE-AWARE"}


def slot_of(e):
    sk = e.get("slot_key")
    return tuple(sk) if isinstance(sk, list) and len(sk) >= 2 else None


def slot_closure(J, gold_ids):
    """gold entries + every sibling sharing any of their slot_keys."""
    slots = {slot_of(J.by_id[i]) for i in gold_ids}
    slots.discard(None)
    return {e["id"] for e in J.entries if slot_of(e) in slots} | set(gold_ids)


def main():
    persona = sys.argv[1] if len(sys.argv) > 1 else "priya"
    joins = load_joins()
    J = joins[persona]
    qs = {q["id"]: q for q in J.questions}

    print("=" * 94)
    print(f"CONSTRUCTION DRY-RUN — {persona} (FR-Bank)")
    print("=" * 94)
    print(f"  bank entries: {len(J.entries)}   questions: {len(J.questions)}")

    resolved = [q for q in J.questions
                if INTENTS[q["id"]] in IN_SCOPE and J.gold[q["id"]]]
    print(f"  in-scope questions: {sum(1 for q in J.questions if INTENTS[q['id']] in IN_SCOPE)}"
          f"   with resolvable gold: {len(resolved)}")

    # ---- slot-ablation blast radius
    rows, tot_gold, tot_closure = [], 0, 0
    contaminated = 0
    for q in resolved:
        g = J.gold[q["id"]]
        cl = slot_closure(J, g)
        tot_gold += len(g); tot_closure += len(cl)
        survivors = [e for e in J.entries if e["id"] not in cl]
        lex = [e["id"] for e in survivors
               if supports_correct(e.get("text", ""), q.get("correct_answer", ""))]
        if lex:
            contaminated += 1
        rows.append({"qid": q["id"], "intent": INTENTS[q["id"]],
                     "gold": len(g), "closure": len(cl),
                     "ratio": round(len(cl) / len(g), 2),
                     "lex_survivors": len(lex)})
    print(f"\n  SLOT-ABLATION blast radius over {len(resolved)} questions:")
    print(f"    gold entries total {tot_gold}, slot-closure total {tot_closure}, "
          f"mean ratio {tot_closure/max(tot_gold,1):.2f}x")
    print(f"    mean entries removed per question: {tot_closure/max(len(resolved),1):.1f} "
          f"of {len(J.entries)} ({tot_closure/max(len(resolved),1)/len(J.entries):.1%})")
    print(f"\n  CONSTRUCTION-TIME CONTAMINATION SWEEP (the E1 build rule):")
    print(f"    questions where content survives slot-ablation by the lexical proxy: "
          f"{contaminated}/{len(resolved)} ({contaminated/max(len(resolved),1):.0%})")
    print(f"    -> these route to UNRESOLVED by construction rule, not to a sensitivity row")

    print(f"\n  {'qid':16s} {'intent':14s} {'gold':>5s} {'closure':>8s} {'x':>5s} {'lex':>4s}")
    for r in rows[:10]:
        print(f"  {r['qid']:16s} {r['intent']:14s} {r['gold']:5d} {r['closure']:8d} "
              f"{r['ratio']:5.2f} {r['lex_survivors']:4d}")

    # ---- category ablation comparison
    cat_best = None
    for c in CATEGORIES:
        n = sum(1 for e in J.entries if e["category"] == c)
        if n and (cat_best is None or n > cat_best[1]):
            cat_best = (c, n)
    print(f"\n  CAT-ABLATED for contrast: largest category {cat_best[0]} removes {cat_best[1]} "
          f"entries ({cat_best[1]/len(J.entries):.0%} of the bank) for ALL questions at once;")
    print(f"  SLOT-ABLATED removes {tot_closure/max(len(resolved),1):.0f} entries per question. "
          f"Slot ablation is the hard tier because the store stays otherwise intact.")

    # ---- 40-persona projection
    print("\n" + "=" * 94)
    print("40-PERSONA PROJECTION (FR-Bank)")
    print("=" * 94)
    tot_res = tot_inscope = tot_negelig = 0
    for name, JJ in sorted(joins.items()):
        for q in JJ.questions:
            it = INTENTS[q["id"]]
            if it in IN_SCOPE:
                tot_inscope += 1
                if JJ.gold[q["id"]]:
                    tot_res += 1
                    if it in NEG_ELIGIBLE:
                        tot_negelig += 1
    print(f"  in-scope questions           {tot_inscope}")
    print(f"  with resolvable YAML gold    {tot_res}   <- SLOT-ABLATED ABSENT ceiling")
    print(f"  of those, neg-obligation eligible (CURRENT-STATE/UPCOMING)  {tot_negelig}")
    est_contam = round(tot_res * contaminated / max(len(resolved), 1))
    print(f"  minus projected contamination routing ({contaminated/max(len(resolved),1):.0%})"
          f"  ~{tot_res - est_contam}")
    print(f"  NATURAL-ABSENT probes @5/persona x 40                        ~200")
    print(f"  HARD TIER (SLOT-ABLATED + NATURAL-ABSENT pooled)             "
          f"~{tot_res - est_contam + 200}")

    jdump({"persona": persona, "n_entries": len(J.entries),
           "n_questions": len(J.questions), "n_resolved_in_scope": len(resolved),
           "slot_ablation": {"gold_total": tot_gold, "closure_total": tot_closure,
                             "mean_ratio": tot_closure / max(tot_gold, 1),
                             "mean_removed_per_question": tot_closure / max(len(resolved), 1)},
           "contamination_rate": contaminated / max(len(resolved), 1),
           "per_question": rows,
           "projection_40": {"in_scope": tot_inscope, "resolvable_gold": tot_res,
                             "neg_eligible": tot_negelig,
                             "slot_absent_after_contam": tot_res - est_contam,
                             "natural_absent_est": 200,
                             "hard_tier_est": tot_res - est_contam + 200},
           "no_api_calls": True}, E1 / f"dryrun_{persona}.json")
    print(f"\nwrote {E1/f'dryrun_{persona}.json'}")


if __name__ == "__main__":
    main()
