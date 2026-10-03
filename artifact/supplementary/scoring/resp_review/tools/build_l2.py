"""build_l2.py -- RESP Phase B step 4: the retriever of ADDENDUM_RESP.md sections C.3 / L2.

ONE API CALL PATH: the 302 question vectors with text-embedding-3-small (the one non-gpt-4.1-mini
call, ruling (1) of 2026-09-12; OpenAI key; about 4,500 input tokens). No chat call.

  embed     all 302 distinct question texts of the 661, fresh; assert the 187 cached vectors
            (artifacts/theory/query_emb_cache.npz, by question id) reproduce the fresh ones at
            cosine >= 0.99 each (a failure is a STOP); pin the matrix by sha256 -> l2/question_emb.npz
  retrieve  per item: LifecycleBank.cosine_search_all over the item's store variant (every entry the
            variant holds, active or not; the bank's cached text-embedding-3-small vectors), top 10
            taken, top 5 used; the rendered block (TRUE lifecycle flags from index_v2.true_lifecycle,
            category, scrubbed attribute, age before pinned t_now, text; one line per entry, rank
            order); for PN items the reach flag at k = 5, the best rank, reach at k = 10
            -> l2/retrieval.json
  ledger    AUX-RESP-L2-RETRIEVER, AUX-RESP-L2-REACH (L2-P3 verdict under its frozen text)

BM25, category forcing, multi-hop, distillation, the lifecycle filters and blended scoring are not
applied (section C.3). BELIEVED flags are not used.
"""
from __future__ import annotations

import collections
import copy
import datetime as dt
import io
import math
import sys

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import resp_common as RC                                                     # noqa: E402
from resp_common import ROOT, L2, LEDGER, J, jdump                           # noqa: E402
sys.path.insert(0, str(ROOT))
import lifecycle_bank as LB                                                  # noqa: E402

EMBED_MODEL = "text-embedding-3-small"
EMBED_PRICE = 0.02          # $ per 1M input tokens
BANKS = ROOT / "LifeMemEval" / "artifacts" / "lifecycle_banks"
K_TAKE, K_USE = 10, 5
_BANKS = {}


def unit(m):
    m = np.asarray(m, np.float32)
    return m / (np.linalg.norm(m, axis=-1, keepdims=True) + 1e-12)


# ------------------------------------------------------------------ question vectors
def question_table(sub):
    """question text -> question_id (one id per text, asserted)."""
    qmap = {}
    for it in sub:
        qmap.setdefault(it["question"], set()).add(it["question_id"])
    assert all(len(v) == 1 for v in qmap.values()), "a question text maps to two ids"
    return {q: next(iter(v)) for q, v in sorted(qmap.items())}


def embed_questions(sub):
    qmap = question_table(sub)
    texts = list(qmap)
    assert len(texts) == 302
    api = RC.e1_api()                                                        # e1_metamemory/tools/api.py (wraps the E0 client)
    cli = api._e0._client()                                                  # noqa: SLF001
    r = cli.embeddings.create(model=EMBED_MODEL, input=texts)
    emb = np.asarray([d.embedding for d in r.data], np.float32)
    assert emb.shape == (302, 1536)
    usage = {"model": r.model, "input_tokens": r.usage.prompt_tokens, "total_tokens": r.usage.total_tokens,
             "usd": r.usage.prompt_tokens / 1e6 * EMBED_PRICE, "n_inputs": len(texts), "when": dt.datetime.now().isoformat(timespec="seconds")}
    # cached-vector check
    z = np.load(ROOT / "artifacts/theory/query_emb_cache.npz", allow_pickle=True)
    cached = {str(i): v for i, v in zip(z["ids"], unit(z["embeddings"]))}
    cos = []
    for q, v in zip(texts, unit(emb)):
        qid = qmap[q]
        if qid in cached:
            cos.append((qid, float(cached[qid] @ v)))
    assert len(cos) == 187, len(cos)
    worst = min(c for _, c in cos)
    check = {"n_cached": len(cos), "min_cosine": worst, "n_below_0.99": sum(1 for _, c in cos if c < 0.99)}
    np.savez_compressed(L2 / "question_emb.npz", questions=np.asarray(texts, dtype=object),
                        question_ids=np.asarray([qmap[q] for q in texts], dtype=object), embeddings=emb)
    jdump({"usage": usage, "cached_check": check, "matrix_sha256": RC.sha(L2 / "question_emb.npz", 64)}, L2 / "embedding_call.json")
    print(f"embedded {len(texts)} questions: {usage['input_tokens']} tokens, ${usage['usd']:.6f}; cached check: {len(cos)} vectors, min cosine {worst:.6f}, below 0.99: {check['n_below_0.99']}")
    if check["n_below_0.99"]:
        sys.exit("CACHED-VECTOR CHECK FAILED -- STOP (ADDENDUM_RESP section STOP)")
    return {q: v for q, v in zip(texts, emb)}


def load_question_vectors():
    z = np.load(L2 / "question_emb.npz", allow_pickle=True)
    return {str(q): v for q, v in zip(z["questions"], z["embeddings"])}


# ------------------------------------------------------------------ retrieval
def bank_for(it):
    """The persona's bank restricted to the item's store variant (entries the committed index renders from)."""
    name = it["persona"]
    if name not in _BANKS:
        _BANKS[name] = LB.LifecycleBank.load(BANKS / f"{name}.json")
    b = _BANKS[name]
    ids = set(RC.variant_ids(it))
    vb = copy.copy(b)
    vb.entries = {k: v for k, v in b.entries.items() if k in ids}
    assert len(vb.entries) == len(ids)
    return vb


def retrieve(it, qv):
    vb = bank_for(it)
    top = [(e.id, float(s)) for e, s in vb.cosine_search_all(np.asarray(qv, np.float32), k=K_TAKE)]
    fl = RC.true_flags()[it["persona"]]
    block = "\n".join(RC.render_line(r + 1, fl[eid]) for r, (eid, _) in enumerate(top[:K_USE]))
    return top, block


def wilson(k, n, z=1.959964):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def main():
    sub = RC.load_cell()
    L2.mkdir(parents=True, exist_ok=True)
    qemb = embed_questions(sub) if not (L2 / "question_emb.npz").exists() else load_question_vectors()
    items, stats = {}, collections.Counter()
    for it in sub:
        top, block = retrieve(it, qemb[it["question"]])
        rec = {"persona": it["persona"], "variant": it["variant"], "label": it["label"], "state": it["state"],
               "n_store": len(RC.variant_ids(it)), "top10_ids": [t[0] for t in top], "top10_cos": [round(t[1], 6) for t in top],
               "top5_ids": [t[0] for t in top[:K_USE]], "block": block}
        if it["y_nok"]:
            pm = set(it["pn_members"])
            ranks = [r + 1 for r, (eid, _) in enumerate(top) if eid in pm]
            rec.update({"pn_members": sorted(pm), "reach_k5": bool(ranks and ranks[0] <= K_USE), "reach_k10": bool(ranks),
                        "best_rank": (ranks[0] if ranks else None),
                        "flags_of_reached": [RC.lifecycle_tag(RC.true_flags()[it["persona"]][eid]) for eid in rec["top5_ids"] if eid in pm]})
            stats[("k5", it["state"], rec["reach_k5"])] += 1
            stats[("k10", it["state"], rec["reach_k10"])] += 1
        items[it["item_id"]] = rec
    ec = J(L2 / "embedding_call.json")
    meta = {"registration": "registrations/ADDENDUM_RESP.md", "frozen": RC.FREEZE, "section": "C.3 / L2", "retriever": "LifecycleBank.cosine_search_all (lifecycle_bank.py:402-414) over the item's store variant, all entries active or not; top 10 taken, top 5 used",
            "bank_vectors": "LifeMemEval/artifacts/lifecycle_banks/<persona>_embeddings.npz (text-embedding-3-small, 1536-d)",
            "question_vectors": {"file": "l2/question_emb.npz", "sha256": ec["matrix_sha256"], "model": EMBED_MODEL, **ec["usage"], "cached_check": ec["cached_check"]},
            "line_format": "[r] lifecycle: <retracted, superseded, expired in that order | active> | category: <cat> | attribute: <scrubbed slot> | age: <days> days | text: <entry text>",
            "flags": "TRUE join (index_v2.true_lifecycle), the same as the committed TRUE index; BELIEVED flags not used",
            "no_filters": "no lifecycle mask, BM25, category forcing, multi-hop or distillation applied", "built": dt.date.today().isoformat()}
    jdump({"meta": meta, "items": items}, L2 / "retrieval.json")

    # ---- reach
    pn = [i for i in sub if i["y_nok"]]
    def rate(k, st=None):
        sel = [i for i in pn if st is None or i["state"] == st]
        n = len(sel); f = sum(1 for i in sel if items[i["item_id"]][f"reach_{k}"])
        return f, n, f / n
    f5, n5, r5 = rate("k5"); lo, hi = wilson(f5, n5)
    f10, n10, r10 = rate("k10")
    per_state = {st: rate("k5", st) for st in ("sup", "ret", "exp")}
    per_state10 = {st: rate("k10", st) for st in ("sup", "ret", "exp")}
    ranks = collections.Counter(items[i["item_id"]]["best_rank"] for i in pn)
    tags = collections.Counter(t for i in pn for t in items[i["item_id"]]["flags_of_reached"])
    verdict = r5 < 0.20
    txt_hold = (f"On this population a five-item similarity view contains the record that forbids use for {f5} of 104 obligations "
                f"({r5:.4f}), re-measuring the below-cutoff premise on the monitoring population.")
    txt_fail = (f"Over every entry the store holds, a five-item similarity view contains the record that forbids use for {f5} of the 104 "
                f"obligations, a reach rate of {r5:.4f}. The record does not rank below the cutoff on this population for a retriever that "
                f"does not mask inactive entries; the 5% figure the manuscript cites is FR-Bank's AV7 retrieval-pass rate under its lifecycle "
                f"mask, a different quantity, and the premise sentence is to be restated as a mask effect.")
    reach = {"k5": {"reached": f5, "n": n5, "rate": r5, "wilson95": [lo, hi]}, "k10": {"reached": f10, "n": n10, "rate": r10},
             "per_state_k5": {s: {"reached": v[0], "n": v[1], "rate": v[2]} for s, v in per_state.items()},
             "per_state_k10": {s: {"reached": v[0], "n": v[1], "rate": v[2]} for s, v in per_state10.items()},
             "best_rank_distribution": {str(k): v for k, v in sorted(ranks.items(), key=lambda kv: (kv[0] is None, kv[0] or 0))},
             "flags_printed_on_reached_records_k5": dict(tags),
             "L2-P3": {"bar": "reach at k = 5 < 0.20", "value": r5, "verdict": "HOLDS" if verdict else "FAILS",
                       "text": txt_hold if verdict else txt_fail}}
    jdump(reach, L2 / "reach.json")
    print(f"reach k=5: {f5}/104 = {r5:.4f} [{lo:.4f},{hi:.4f}]; per state " + ", ".join(f"{s} {v[0]}/{v[1]}" for s, v in per_state.items())
          + f"; k=10: {f10}/104 = {r10:.4f}; best-rank {dict(ranks)}; L2-P3 {'HOLDS' if verdict else 'FAILS'}")
    print("tags on reached records (k=5):", dict(tags))

    today = dt.date.today().isoformat()
    led = f"""
---

## 4. Step 4 — the retriever and the reach row (written {today}; one embedding call, no chat call)

### AUX-RESP-L2-RETRIEVER — the retriever spec and the question vectors

Retriever: `LifecycleBank.cosine_search_all` (`lifecycle_bank.py:402-414`), cosine over **every entry the
item's store variant holds, active or not** (FULL; CAT-ABLATED minus the persona's planned categories;
SLOT-ABLATED minus `slot_ablations[persona:qid]` — the entry sets `index_v2.main` renders the committed
index from), on the bank's cached `text-embedding-3-small` vectors; top 10 taken, **top 5 used**. No
lifecycle mask, BM25, category forcing, multi-hop or distillation. Per retrieved entry the block carries
the store's **TRUE** lifecycle flags (`index_v2.true_lifecycle`, the join the TRUE index is rendered
from), category, scrubbed attribute, age in days before the persona's pinned `t_now`, and the text, one
line per entry in rank order (`retrieval.json` `meta.line_format`).

**Question vectors (the one non-`gpt-4.1-mini` call, ruling (1)).** All 302 distinct question texts
embedded fresh with `{EMBED_MODEL}` in one call: {ec['usage']['input_tokens']} input tokens,
**${ec['usage']['usd']:.6f}** ({ec['usage']['when']}). The **187** LifecycleBench questions with a cached vector
(`artifacts/theory/query_emb_cache.npz`) reproduce the fresh ones at cosine ≥ 0.99 each: minimum
{ec['cached_check']['min_cosine']:.6f}, {ec['cached_check']['n_below_0.99']} below 0.99 — **check PASS**. Matrix `l2/question_emb.npz`,
sha256 `{ec['matrix_sha256']}`. Artifact: `l2/retrieval.json` (per item the ten ids with cosines, the
five used, the rendered block; per PN item the reach flags and best rank); `verify_resp.py` check F
re-derives every top-10 from the pinned vectors and every block byte for byte.

### AUX-RESP-L2-REACH — reach of the forbidding record (the L2 baseline row; DS's ALWAYS row)

Census over the 104 PN items (no sampling interval; Wilson 95% beside, descriptive).

| | reached at k = 5 | of | rate | reached at k = 10 | rate |
|---|---:|---:|---:|---:|---:|
| **all PN** | **{f5}** | 104 | **{r5:.4f}** (Wilson [{lo:.4f}, {hi:.4f}]) | {f10} | {r10:.4f} |
| supersession-derived | {per_state['sup'][0]} | 63 | {per_state['sup'][2]:.4f} | {per_state10['sup'][0]} | {per_state10['sup'][2]:.4f} |
| retraction-derived | {per_state['ret'][0]} | 26 | {per_state['ret'][2]:.4f} | {per_state10['ret'][0]} | {per_state10['ret'][2]:.4f} |
| expiry-derived | {per_state['exp'][0]} | 15 | {per_state['exp'][2]:.4f} | {per_state10['exp'][0]} | {per_state10['exp'][2]:.4f} |

Best rank of a `pn_members` entry within the top 10 (None = not in the ten): {dict(sorted(((str(k), v) for k, v in ranks.items()), key=lambda kv: kv[0]))}.
Flags printed on the reached records at k = 5: {dict(tags)} (D-DS-1 of the DS registration: 22 forbidding
records carry no TRUE flag and print `active` when retrieved).

**L2-P3 (reach at k = 5 < 0.20): {r5:.4f} → {'HOLDS' if verdict else 'FAILS'}.** Frozen text, printed with its numbers:
> {txt_hold if verdict else txt_fail}

The retraction reach ({per_state['ret'][0]} of 26) is the row the 5% sentence is about. Rendered blocks and the reach
flags are DS's ALWAYS view and row (`registrations/ADDENDUM_DS.md` §C.1).
"""
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(led)
    print("ledger appended: AUX-RESP-L2-RETRIEVER, AUX-RESP-L2-REACH")


if __name__ == "__main__":
    main()
