"""
run_elicitation.py -- E0 Step 4: elicit FOK / NOK in the BLIND and INDEXED arms.

Per PREREG_E0.md §10: gpt-4.1-mini, temperature 0, seed 42, one call per item per
arm, all 510 items in both arms. Responses cached to disk keyed by
(item_id, arm, model, prompt_hash). Prompt texts come from the frozen prompts
module and are not constructed here.

Parse-failure policy, pre-registered: a response that does not parse as the
required JSON is retried once (the retry uses a distinct cache key so it is a
genuinely fresh call); a second failure marks the item ELICITATION_FAILED, which
excludes it from metrics and is counted in the report.

Usage:  python e0_metamemory/tools/run_elicitation.py [--limit N]
"""

from __future__ import annotations

import concurrent.futures as cf
import sys

import api
import prompts
from e0_common import E0, jdump, jload, load_joins


def clamp(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return min(100.0, max(0.0, f)) / 100.0


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    idx = jload(E0 / "indexes.json")
    level = idx["meta"]["tightening_level"]
    indexes = idx["indexes"]
    items = jload(E0 / "items.json")
    if limit:
        items = items[:limit]
    joins = load_joins()
    qs = {q["id"]: q for J in joins.values() for q in J.questions}

    jobs = []
    for it in items:
        q = qs[it["question_id"]]["question"]
        jobs.append((it, "BLIND", [
            {"role": "system", "content": prompts.SYSTEM},
            {"role": "user", "content": prompts.USER_BLIND.format(question=q)}]))
        jobs.append((it, "INDEXED", [
            {"role": "system", "content": prompts.SYSTEM},
            {"role": "user", "content": prompts.USER_INDEXED.format(
                index=indexes[f"{it['persona']}:{it['variant']}"], question=q)}]))

    def one(job):
        it, arm, msgs = job
        r = api.call(it["item_id"], arm, msgs)
        obj = api.parse_json(r["content"])
        failed = False
        if obj is None or clamp(obj.get("fok")) is None or clamp(obj.get("nok")) is None:
            r = api.call(it["item_id"], arm + "#retry", msgs)
            obj = api.parse_json(r["content"])
            if obj is None or clamp(obj.get("fok")) is None or clamp(obj.get("nok")) is None:
                failed = True
                obj = {}
        return {"item_id": it["item_id"], "arm": arm,
                "persona": it["persona"], "question_id": it["question_id"],
                "variant": it["variant"], "label": it["label"],
                "subtype": it["subtype"], "attack_vector": it["attack_vector"],
                "lex_flagged": it["lex_flagged"],
                "absent_mechanism": it["absent_mechanism"],
                "fok": clamp(obj.get("fok")), "nok": clamp(obj.get("nok")),
                "would_search": bool(obj.get("would_search")) if not failed else None,
                "status": "ELICITATION_FAILED" if failed else "OK",
                "cached": r["cached"], "index_level": level}

    print(f"eliciting {len(jobs)} calls ({len(items)} items x 2 arms), index level {level}")
    out = []
    try:
        with cf.ThreadPoolExecutor(max_workers=12) as ex:
            for n, rec in enumerate(ex.map(one, jobs), 1):
                out.append(rec)
                if n % 200 == 0:
                    api.flush()
                    print(f"  {n}/{len(jobs)}  ${api.meter()['usd']:.4f}")
    finally:
        api.flush()

    jdump(out, E0 / "elicitation.json")
    m = api.meter()
    ok = sum(1 for r in out if r["status"] == "OK")
    print(f"\n  parsed OK: {ok}/{len(out)};  ELICITATION_FAILED: {len(out)-ok}")
    print(f"  calls {m['calls']} live, {m['cached']} cached; "
          f"tokens {m['in']} in / {m['out']} out;  spend ${m['usd']:.4f}")
    if m["usd"] > api.ESCALATE_USD:
        print("  *** spend past the $8 escalation threshold ***")
    print(f"wrote {E0/'elicitation.json'}")


if __name__ == "__main__":
    main()
