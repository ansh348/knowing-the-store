"""
run_answers.py -- generate downstream answers for one split. Counts only on stdout.

An answer is a function of (question, context, draw), NOT of policy, so answers are
generated once per context state and every policy shares them. Three states exist
and no more (PREREG_E2 section 3):

  S0  no facts        -- what (ii) sees, and what any gating policy sees when it skips
  S1  retrieved facts -- what (i) sees, and what any gating policy sees when it retrieves
  S2  S1 + CAUTION_INSTRUCTION -- what (vi) sees when NOK >= tau_NOK

That is why a seven-policy comparison needs ~1,141 answer calls rather than 3,703,
and why the attribution control (vii) costs nothing.

ANSWERER: gpt-4.1-mini, temperature 0, seed 42, metered. The frozen prereg pins
the answer PROMPT (FR's GENERATION_SYSTEM_PROMPT, verbatim) but left the answerer
MODEL unspecified; it is pinned here at the calibration boundary and logged as
D31-E2. The judge is unaffected -- it remains FR's pinned claude-sonnet-4-6.

EVAL HYGIENE: this script prints counts, costs and hashes. It never prints an
answer, and it computes no score of any kind.

Usage:  python e2_metamemory/tools/run_answers.py --split calibration --k 3
        python e2_metamemory/tools/run_answers.py --split eval --k 1 [--s2-all]
"""

from __future__ import annotations

import collections
import concurrent.futures as cf
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import e2_api as api                                            # noqa: E402
from e2_common import (E2, S0, S1, S2, answer_messages, jdump,  # noqa: E402
                       jload, load_items, sha)

WORKERS = 12
MAX_ANSWER_TOKENS = 220


def main():
    split = sys.argv[sys.argv.index("--split") + 1]
    k = int(sys.argv[sys.argv.index("--k") + 1]) if "--k" in sys.argv else 1
    s2_all = "--s2-all" in sys.argv or split == "calibration"
    assert split in ("calibration", "eval")

    items = {i["item_id"]: i for i in load_items() if i["split"] == split}
    gates = jload(E2 / f"gates_{split}.json")["rows"]
    gmap = {g["item_id"]: g for g in gates}
    # Facts come from the FROZEN retrieval artifact, never from a live retriever:
    # all seven policies must see byte-identical facts (E2_AMENDMENT_2 section 1).
    fr = jload(E2 / "retrieval_frozen.json")
    frozen = {r["item_id"]: r for r in fr["rows"]}
    print(f"facts from frozen artifact {fr['artifact_sha256'][:16]}...")
    # Answerer pinned by the Amendment 3 bake-off, not chosen here.
    ANSWERER = jload(E2 / "ANSWERER_FROZEN.json")["answerer_model"]
    print(f"answerer pinned by bake-off: {ANSWERER}")

    tau_nok = None
    if not s2_all:
        # NOT `frozen` -- that name holds the retrieval artifact above. The
        # collision was invisible on the calibration split, where s2_all is True
        # and this branch never runs, and fatal on eval. D39-E2.
        thr = jload(E2 / "THRESHOLDS_FROZEN.json")
        tau_nok = thr["tau_NOK"]
        print(f"S2 restricted to NOK >= tau_NOK = {tau_nok}")

    jobs = []
    for tag, it in sorted(items.items()):
        g = gmap[tag]
        facts = frozen[tag]["facts"]
        states = [(S0, []), (S1, facts)]
        nok = (g["indexed"].get("1") or g["indexed"].get(1) or {}).get("nok")
        if s2_all or (nok is not None and tau_nok is not None and nok >= tau_nok):
            states.append((S2, facts))
        for state, f in states:
            ctx = sha(state, *f)
            for d in range(1, k + 1):
                jobs.append((tag, it["question"], state, tuple(f), ctx, d))

    print(f"split={split} items={len(items)} k={k} s2_all={s2_all} "
          f"-> {len(jobs)} answer calls")

    def run(job):
        tag, q, state, facts, ctx, d = job
        msgs = answer_messages(list(facts), q, state)
        r = api.call_text_model(f"{tag}|{ctx[:16]}|d{d}", f"answer-{state}",
                                msgs, model=ANSWERER,
                                max_tokens=MAX_ANSWER_TOKENS)
        api.check_cap()
        txt = (r["content"] or "").strip()
        return {"item_id": tag, "state": state, "draw": d, "context_sha": ctx,
                "n_facts": len(facts), "response": txt,
                "response_sha": sha(tag, txt), "cached": r["cached"],
                "prompt_tokens": r.get("prompt_tokens"),
                "completion_tokens": r.get("completion_tokens")}

    out = []
    try:
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
            for n, rec in enumerate(ex.map(run, jobs), 1):
                out.append(rec)
                if n % 300 == 0:
                    api.flush()
                    print(f"  {n}/{len(jobs)}  ${api.spend()[0]:.4f}", flush=True)
    finally:
        api.flush()

    jdump({"split": split, "k": k, "s2_all": s2_all, "n": len(out),
           "answerer_model": ANSWERER, "temperature": 0, "seed": 42,
           "rows": out}, E2 / f"answers_{split}.json")

    per_state = collections.Counter(r["state"] for r in out)
    empty = sum(1 for r in out if not r["response"])
    uniq = len({(r["item_id"], r["response_sha"]) for r in out})
    total, ncalls = api.spend()
    print(f"  by state: {dict(per_state)}")
    print(f"  empty responses: {empty}")
    print(f"  distinct (item, response) pairs to judge: {uniq}")
    print(f"  E2 cumulative ${total:.4f} over {ncalls} calls (cap ${api.E2_CAP_USD})")
    print(f"wrote answers_{split}.json  -- no answer text printed, no score computed")


if __name__ == "__main__":
    main()
