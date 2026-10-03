"""
run_answers_e3.py -- downstream answers for one split. Counts only on stdout.

An answer is a function of (question, rung, context state, draw), NOT of arm, so
answers are generated once per (cell, state) and every arm shares them. Five
states exist and no more (PREREG_E3 4.2 + E3_AMENDMENT_1 2.4):

  S0   no facts                     -- arm (c), and any gating arm when it skips
  S1   retrieved facts              -- arm (b)
  S2   S1 + CAUTION                 -- arm (a''), descriptive, E2's S2 byte-identical
  S3   S2 + per-fact annotation + TRUE store supersession digest      -- arms (a), (d)
  S3'  S3 with the digest SCRAMBLED, everything else byte-identical   -- arm (a')

`S0` contains no store content and is RUNG-INVARIANT: it is elicited once per
question for the whole ladder, not once per cell.

CALIBRATION runs every state on every cell. k=3 on S0/S1/S3 -- the states the
derivation and the PREREG_E3 2.3 sigma_a trigger read -- and k=1 on S2/S3', which
no derivation uses. EVAL runs k per the SP2 decision, over the states the frozen
operating point actually calls for.

ANSWERER: gpt-5.4 at the E2 Amendment-3 pin, temperature 0, seed 42, metered.

EVAL HYGIENE: this script prints counts, costs and hashes. It never prints an
answer, and it computes no score of any kind.

Usage:  python e3_metamemory/tools/run_answers_e3.py --split calibration
        python e3_metamemory/tools/run_answers_e3.py --split eval --k 1
"""

from __future__ import annotations

import collections
import concurrent.futures as cf
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e2_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import e3_api as api                                               # noqa: E402
from e3_common import (E3, S0, S1, S2, S3, S3P, answer_messages,   # noqa: E402
                       jdump, jload, load_cells, sha)

WORKERS = 12
MAX_ANSWER_TOKENS = 220
K_STATES = (S0, S1, S3)          # states the derivation and sigma_a read


def main():
    split = sys.argv[sys.argv.index("--split") + 1]
    k = int(sys.argv[sys.argv.index("--k") + 1]) if "--k" in sys.argv else 3
    assert split in ("calibration", "eval")

    cells = [c for c in load_cells()["cells"] if c["split"] == split]
    fr = jload(E3 / "retrieval_frozen_e3.json")
    ret = {r["cell_id"]: r for r in fr["rows"]}
    ann = jload(E3 / "annotations_e3.json")
    IX = jload(E3 / "indexes_e3.json")
    ANSWERER = jload(ROOT / "e2_metamemory" / "ANSWERER_FROZEN.json")["answerer_model"]
    print(f"facts from frozen artifact {fr['artifact_sha256'][:16]}...")
    print(f"digests: TRUE {IX['artifact_sha256'][:16]}...  "
          f"LOBOTOMY {IX['artifact_sha256_lobotomy'][:16]}...")
    print(f"answerer pinned by the E2 bake-off: {ANSWERER}")

    # ---- which (cell, state) pairs this split needs
    if split == "calibration":
        plan = {c["cell_id"]: [S0, S1, S2, S3, S3P] for c in cells}
        print("calibration: every state on every cell "
              f"(k={k} on {[s for s in K_STATES]}, k=1 on the rest)")
    else:
        thr = jload(E3 / "THRESHOLDS_E3_FROZEN.json")
        tau = thr["tau_FOK"]
        gT = {r["cell_id"]: r for r in jload(E3 / "gates_eval.json")["rows"]}
        gL = {r["cell_id"]: r
              for r in jload(E3 / "gates_eval_lobotomy.json")["rows"]}
        rate_a = sum(1 for c in cells
                     if (gT[c["cell_id"]]["fok"] if gT[c["cell_id"]]["fok"] is not None else -1) >= tau) / len(cells)
        import hashlib
        plan = {}
        for c in cells:
            t = c["cell_id"]
            st = [S0]                                    # arm (c), free everywhere
            a_ret = (gT[t]["fok"] if gT[t]["fok"] is not None else -1) >= tau          # arm (a)
            l_ret = (gL[t]["fok"] if gL[t]["fok"] is not None else -1) >= tau          # arm (a')
            st.append(S1)                                # arm (b), every cell
            if a_ret:
                # arm (a); arm (d) is retired by E3_AMENDMENT_2 and shares this
                # answer exactly, being byte-identical to (a) at tau_FOK = 0.00
                st.append(S3)
            if a_ret:
                st.append(S2)                            # arm (a''), descriptive
            if l_ret:
                st.append(S3P)
            plan[t] = st
        # ---- NON-VACUITY GATE, E3_AMENDMENT_1 section 3, on the EVAL cells and
        # BEFORE a single answer call is bought. Structurally impossible to skip:
        # it lives inside the runner, not beside it. The surviving gated pairs
        # after E3_AMENDMENT_2 are (a)/(b) and (a)/(a').
        from e3_common import answer_messages as _am                # noqa: PLC0415
        IXf = IX
        def _app(c, state, retrieved):
            if not retrieved:
                state = S0
            key = f"frbank:{c['persona']}:R{c['rung']}:BELIEVED"
            dg = (IXf["digests"][key] if state == S3
                  else IXf["digests_lobotomy"][key] if state == S3P else None)
            an = ann["true"][c["cell_id"]] if state in (S3, S3P) else None
            m = _am(ret[c["cell_id"]]["facts"], an, dg, c["question"], state)
            return m[0]["content"] + "" + m[1]["content"]
        nb = nl = 0
        for c in cells:
            t = c["cell_id"]
            ar = (gT[t]["fok"] if gT[t]["fok"] is not None else -1) >= tau
            lr = (gL[t]["fok"] if gL[t]["fok"] is not None else -1) >= tau
            if _app(c, S3, ar) != _app(c, S1, True):
                nb += 1
            if _app(c, S3, ar) != _app(c, S3P, lr):
                nl += 1
        n = len(cells)
        print(f"NON-VACUITY on {n} EVAL cells, before any answer call:")
        print(f"  (a) vs (b)  {nb}/{n}  {nb/n:.1%}")
        print(f"  (a) vs (a') {nl}/{n}  {nl/n:.1%}")
        if nb / n < 0.95 or nl / n < 0.95:
            raise SystemExit("STOP: a gated arm pair is vacuous on the eval cells "
                             "(< 95% differing prompts). E3_AMENDMENT_1 section 3.")
        print("  both surviving gated pairs clear the 95% band   PASS")
        print(f"eval: tau_FOK={tau}  arm(a) rate {rate_a:.3f}  "
              f"arm(a') rate {sum(1 for c in cells if (gL[c['cell_id']]['fok'] if gL[c['cell_id']]['fok'] is not None else -1) >= tau)/len(cells):.3f}")

    jobs, seen_s0 = [], set()
    for c in cells:
        t = c["cell_id"]
        r = ret[t]
        for state in plan[t]:
            facts = r["facts"]
            if state == S0:
                # rung-invariant: keyed on the question, elicited once
                qkey = f"{c['persona']}:{c['question_id']}"
                if qkey in seen_s0:
                    continue
                seen_s0.add(qkey)
                a, dg, f = None, None, []
            elif state in (S3, S3P):
                key = f"frbank:{c['persona']}:R{c['rung']}:BELIEVED"
                a = ann["true"][t]
                dg = (IX["digests"][key] if state == S3
                      else IX["digests_lobotomy"][key])
                f = facts
            else:
                a, dg, f = None, None, facts
            draws = k if state in K_STATES else 1
            ctx = sha(state, dg or "", *(a or []), *f)
            for d in range(1, draws + 1):
                jobs.append((t, c["question"], state, tuple(f),
                             tuple(a) if a is not None else None, dg, ctx, d,
                             c["persona"], c["question_id"], c["rung"]))

    print(f"split={split} cells={len(cells)} -> {len(jobs)} answer calls")

    def run(job):
        t, q, state, facts, anns, dg, ctx, d, p, qid, rung = job
        msgs = answer_messages(list(facts),
                               list(anns) if anns is not None else None,
                               dg, q, state)
        cache_id = (f"{p}:{qid}|{ctx[:16]}|d{d}" if state == S0
                    else f"{t}|{ctx[:16]}|d{d}")
        r = api.call_text_model(cache_id, f"e3answer-{state}", msgs,
                                model=ANSWERER, max_tokens=MAX_ANSWER_TOKENS)
        api.check_cap()
        txt = (r["content"] or "").strip()
        return {"cell_id": t, "persona": p, "question_id": qid, "rung": rung,
                "state": state, "draw": d, "context_sha": ctx,
                "n_facts": len(facts), "response": txt,
                "response_sha": sha(t, txt), "cached": r["cached"],
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

    jdump({"split": split, "k": k, "k_states": list(K_STATES),
           "answerer_model": ANSWERER, "temperature": 0, "seed": 42,
           "retrieval_artifact_sha256": fr["artifact_sha256"],
           "index_artifact_sha256": IX["artifact_sha256"],
           "index_artifact_sha256_lobotomy": IX["artifact_sha256_lobotomy"],
           "n": len(out), "rows": out}, E3 / f"answers_{split}.json")

    per_state = collections.Counter(r["state"] for r in out)
    empty = sum(1 for r in out if not r["response"])
    uniq = len({(r["cell_id"], r["response_sha"]) for r in out})
    total, ncalls = api.spend()
    print(f"  by state: {dict(per_state)}")
    print(f"  empty responses: {empty}")
    print(f"  distinct (cell, response) pairs to judge: {uniq}")
    print(f"  E3 cumulative ${total:.4f} over {ncalls} calls (cap ${api.E3_CAP_USD})")
    print(f"wrote answers_{split}.json -- no answer text printed, no score computed")


if __name__ == "__main__":
    main()
