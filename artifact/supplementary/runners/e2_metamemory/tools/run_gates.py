"""
run_gates.py -- collect every policy's gate SIGNAL for one split.

Signals, not decisions: thresholds are applied later, by the fitter and the eval
scorer. This script never compares a signal to a threshold.

  (iii) similarity   max cosine over the persona's surviving entries. No model
                     call at all -- computed from the committed embeddings.
  (iv)  verbalized   NEW elicitation, prompts_e2 (provisional answer, then
                     confidence, then p_store_has_relevant), NO index.
  (v)/(vi) indexed   prompts_e1.SYSTEM + USER_INDEXED over the BELIEVED index.
                     THIS IS E1'S `INDEXED-BELIEVED` ARM EXACTLY -- same prompt,
                     same model, same decoding -- so draw 1 is READ FROM E1's
                     committed elicitation and costs nothing. Draws 2..k are new.

Only draw 1 is needed for the policies themselves; k>1 exists solely for H-C3, the
exploratory stability comparison.

Output: e2_metamemory/gates_<split>.json -- signals only, no decisions, no scores.

Usage:  python e2_metamemory/tools/run_gates.py --split calibration [--k 1]
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
import prompts_e1 as P1                                         # noqa: E402
import prompts_e2 as P2                                         # noqa: E402
from e2_common import E1, E2, Indexes, jdump, jload, load_items  # noqa: E402

WORKERS = 12
E1_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"


def clamp(v):
    try:
        return min(100.0, max(0.0, float(v))) / 100.0
    except (TypeError, ValueError):
        return None


def main():
    split = sys.argv[sys.argv.index("--split") + 1]
    k = int(sys.argv[sys.argv.index("--k") + 1]) if "--k" in sys.argv else 1
    assert split in ("calibration", "eval")

    got = P1.texts_sha256()
    assert got == E1_TEXTS_SHA, f"E1 frozen prompts changed: {got}"
    print(f"E1 prompt texts sha verified {got[:16]}...")
    print(f"E2 verbal prompt sha        {P2.texts_sha256()[:16]}...")

    items = [i for i in load_items() if i["split"] == split]
    print(f"split={split}  items={len(items)}  k={k}")

    # ---------------- (iii): the SUBSTRATE's own max blended score -------------
    # Amendment 2 section 4: baseline (iii) is redefined on lifecycle_search's own
    # ranking score, read from the frozen retrieval artifact. No model call, and
    # no second retriever -- the gate reads exactly what the retriever ranked by.
    fr = jload(E2 / "retrieval_frozen.json")
    assert fr["validation"]["v1_zero_leak"] and fr["validation"]["v2_pass"],         "retrieval artifact did not pass v1/v2; refusing to gate on it"
    frozen = {r["item_id"]: r for r in fr["rows"]}
    sim, facts_cache = {}, {}
    for it in items:
        r = frozen[it["item_id"]]
        sim[it["item_id"]] = r["max_blended"]
        facts_cache[it["item_id"]] = {"facts": r["facts"], "entry_ids": r["entry_ids"],
                                      "max_blended": r["max_blended"],
                                      "facts_sha256": r["facts_sha256"]}
    print(f"  (iii) max blended read from frozen artifact "
          f"{fr['artifact_sha256'][:16]}... for {len(sim)} items, no model call")

    # ---------------- (v)/(vi) draw 1: read from E1 --------------------------
    e1rows = {r["tag"]: r for r in jload(E1 / "elicitation_main.json")
              if r["arm"] == "INDEXED-BELIEVED" and r["status"] == "OK"}
    idx_sig = collections.defaultdict(dict)
    reused = 0
    for it in items:
        r = e1rows.get(it["item_id"])
        if r and r.get("fok") is not None:
            idx_sig[it["item_id"]][1] = {
                "fok": r["fok"], "nok": r["nok"],
                "nok_candidates_found": r.get("nok_candidates_found"),
                "source": "E1 INDEXED-BELIEVED (committed)"}
            reused += 1
    print(f"  (v)/(vi) draw 1 reused from E1: {reused}/{len(items)} at $0")

    # ---------------- new elicitation: (iv) all draws, (v) draws 2..k ---------
    IX = Indexes()
    jobs = []
    for it in items:
        for d in range(1, k + 1):
            jobs.append(("verbal", it, d))
        for d in range(2, k + 1):
            jobs.append(("indexed", it, d))
        if it["item_id"] not in idx_sig:
            jobs.append(("indexed", it, 1))

    def run(job):
        kind, it, d = job
        tag = it["item_id"]
        if kind == "verbal":
            msgs = [{"role": "system", "content": P2.VERBAL_SYSTEM},
                    {"role": "user", "content":
                     P2.VERBAL_USER.format(question=it["question"])}]
            arm = f"gate-verbal-d{d}"
        else:
            msgs = [{"role": "system", "content": P1.SYSTEM},
                    {"role": "user", "content": P1.USER_INDEXED.format(
                        index=IX.text(it, "BELIEVED"), question=it["question"])}]
            arm = f"gate-indexed-d{d}"
        r = api.call(tag, arm, msgs)
        o = api.parse_json(r["content"]) or {}
        api.check_cap()
        return (kind, tag, d, o, r["cached"])

    if jobs:
        print(f"  eliciting {len(jobs)} new gate calls...", flush=True)
        verbal = collections.defaultdict(dict)
        try:
            with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
                for n, (kind, tag, d, o, cached) in enumerate(ex.map(run, jobs), 1):
                    if kind == "verbal":
                        verbal[tag][d] = {
                            "p_store_has_relevant": clamp(o.get("p_store_has_relevant")),
                            "confidence_without_store":
                                clamp(o.get("confidence_without_store")),
                            "has_provisional": bool(
                                str(o.get("provisional_answer", "")).strip().lower()
                                not in ("", "none")),
                        }
                    else:
                        idx_sig[tag][d] = {"fok": clamp(o.get("fok")),
                                           "nok": clamp(o.get("nok")),
                                           "nok_candidates_found":
                                               bool(o.get("nok_candidates_found")),
                                           "source": "E2 elicitation"}
                    if n % 200 == 0:
                        api.flush()
                        print(f"    {n}/{len(jobs)}  ${api.spend()[0]:.4f}", flush=True)
        finally:
            api.flush()
    else:
        verbal = collections.defaultdict(dict)

    rows = []
    for it in items:
        t = it["item_id"]
        rows.append({
            "item_id": t, "persona": it["persona"], "question_id": it["question_id"],
            "variant": it["variant"], "label": it["label_final"], "split": split,
            "sim_max_blended": sim[t],
            "verbal": verbal.get(t, {}),
            "indexed": idx_sig.get(t, {}),
            "retrieval": facts_cache[t],
        })
    jdump({"split": split, "k": k, "n": len(rows),
           "e1_texts_sha256": got, "e2_verbal_texts_sha256": P2.texts_sha256(),
           "reused_from_e1": reused, "new_calls": len(jobs),
           "rows": rows}, E2 / f"gates_{split}.json")

    total, ncalls = api.spend()
    miss_v = sum(1 for r in rows if not r["verbal"].get(1, {}).get("p_store_has_relevant") is not None)
    miss_i = sum(1 for r in rows if r["indexed"].get(1, {}).get("fok") is None)
    print(f"  parsed: verbal missing {miss_v}, indexed missing {miss_i}")
    print(f"  E2 cumulative spend ${total:.4f} over {ncalls} cached calls "
          f"(cap ${api.E2_CAP_USD})")
    print(f"wrote gates_{split}.json")


if __name__ == "__main__":
    main()
