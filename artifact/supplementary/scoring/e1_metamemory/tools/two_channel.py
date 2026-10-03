"""
two_channel.py -- Amendment 1: the two-channel presence instrument, its required
FR-Bank known-present control, and the routing of external-backend labels.

Construction-side embeddings only; NO elicitation call.

Channels:
  lexical    exp4_witnesses.supports_correct(entry_text, correct_answer)
  embedding  max cosine(question, entry) >= 0.295, text-embedding-3-small

The 0.295 threshold is carried unchanged from the natural-absent screen, where it
was calibrated on the 516 real questions before any probe existed. It is not
retuned here against anything.

Control (Amendment 1 section 3): run the instrument on FR-Bank FULL over the 201
in-scope questions the YAML join establishes ARE answerable there. Combined recall
is measured; epsilon = 1 - recall is published as the residual false-negative rate
attached to every external ABSENT claim.

Usage:  python e1_metamemory/tools/two_channel.py
"""

from __future__ import annotations

import collections
import io
import json
import os
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(PROJECT_ROOT / "analysis" / "ontology_validation"))

from e0_common import BANKS, load_joins  # noqa: E402
from exp4_witnesses import supports_correct  # noqa: E402
from backends import load_backend  # noqa: E402
import api  # noqa: E402

QCACHE = PROJECT_ROOT / "artifacts" / "theory" / "query_emb_cache.npz"
EMB_CACHE = E1 / "backend_embeddings"
THRESH = 0.295                     # carried unchanged; never retuned
EMBED_MODEL = "text-embedding-3-small"
MEM0_EXCLUDE = {"alex", "thanh", "aisha"}
IN_SCOPE = {"CURRENT-STATE", "UPCOMING", "PAST-EVENT", "CHANGE-AWARE"}

INTENTS = {r["id"]: r["intent"]
           for r in json.load(io.open(E1 / "intents.json", encoding="utf-8"))}


def unit(v):
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-12)


def embed_backend(name, rows):
    """Embed a backend's entry texts once, cached to disk. ~$0.005 per backend."""
    EMB_CACHE.mkdir(parents=True, exist_ok=True)
    p = EMB_CACHE / f"{name}.npz"
    if p.exists():
        z = np.load(p, allow_pickle=True)
        return list(z["keys"]), unit(z["emb"].astype(np.float32))
    api._load_env()                                          # noqa: SLF001
    from openai import OpenAI                                # noqa: PLC0415
    cli = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    keys = [f"{r['persona']}||{r['entry_id']}" for r in rows]
    texts = [(r["text"] or " ")[:2000] for r in rows]
    out = []
    B = 512
    for i in range(0, len(texts), B):
        r = cli.embeddings.create(model=EMBED_MODEL, input=texts[i:i + B])
        out += [d.embedding for d in r.data]
        print(f"    {name}: embedded {min(i+B, len(texts))}/{len(texts)}", flush=True)
    emb = np.asarray(out, dtype=np.float32)
    np.savez_compressed(p, keys=np.asarray(keys, dtype=object), emb=emb)
    return keys, unit(emb)


def main():
    joins = load_joins()
    z = np.load(QCACHE, allow_pickle=True)
    qemb = {qid: e for qid, e in zip(list(z["ids"]),
                                     unit(z["embeddings"].astype(np.float32)))}

    # ---------------- per-backend entry embeddings
    per = {}
    for b in ("frbank", "mem0", "amem"):
        rows = load_backend(b)
        if b == "frbank":                       # already cached in the bank npz
            keys, mats = [], []
            for p in sorted(BANKS.glob("*_embeddings.npz")):
                persona = p.name.replace("_embeddings.npz", "")
                zz = np.load(p, allow_pickle=True)
                keys += [f"{persona}||{i}" for i in zz["ids"]]
                mats.append(zz["embeddings"].astype(np.float32))
            emb = unit(np.vstack(mats))
        else:
            keys, emb = embed_backend(b, rows)
        idx = collections.defaultdict(list)
        for n, k in enumerate(keys):
            idx[k.split("||", 1)[0]].append(n)
        per[b] = {"keys": keys, "emb": emb, "idx": idx,
                  "text": {f"{r['persona']}||{r['entry_id']}": r["text"] for r in rows}}
        print(f"  {b}: {len(keys)} entry embeddings")

    def channels(b, persona, q):
        rows_idx = per[b]["idx"].get(persona, [])
        if not rows_idx:
            return False, False, 0.0
        lex = any(supports_correct(per[b]["text"][per[b]["keys"][n]],
                                   q.get("correct_answer", "")) for n in rows_idx)
        v = qemb.get(q["id"])
        if v is None:
            return lex, False, 0.0
        cos = float((per[b]["emb"][rows_idx] @ v).max())
        return lex, cos >= THRESH, cos

    # ---------------- CONTROL on FR-Bank known-present content
    lex_hit = emb_hit = both = either = tot = 0
    for name, J in sorted(joins.items()):
        for q in J.questions:
            if INTENTS[q["id"]] not in IN_SCOPE or not J.gold[q["id"]]:
                continue
            tot += 1
            l, e, _ = channels("frbank", name, q)
            lex_hit += l; emb_hit += e; both += (l and e); either += (l or e)
    rec_l, rec_e, rec_c = lex_hit / tot, emb_hit / tot, either / tot
    eps = 1 - rec_c
    print("\n" + "=" * 84)
    print("CONTROL — two-channel instrument on FR-Bank FULL, YAML-established gold")
    print("=" * 84)
    print(f"  questions              {tot}")
    print(f"  lexical channel        {lex_hit:4d}  recall {rec_l:.3f}")
    print(f"  embedding channel      {emb_hit:4d}  recall {rec_e:.3f}")
    print(f"  both channels          {both:4d}")
    print(f"  COMBINED (either)      {either:4d}  recall {rec_c:.3f}")
    print(f"\n  epsilon = 1 - combined recall = {eps:.4f}  "
          f"({eps:.1%} residual false-negative rate)")
    print("  epsilon attaches to every external ABSENT claim in the study.")

    # ---------------- route external labels
    items = json.load(io.open(E1 / "build" / "items_pre.json", encoding="utf-8"))
    by_id = {i["item_id"]: i for i in items}
    counts = collections.Counter()
    for name, J in sorted(joins.items()):
        for q in J.questions:
            qid = q["id"]
            if INTENTS[qid] not in IN_SCOPE:
                continue
            for b in ("mem0", "amem"):
                if b == "mem0" and name in MEM0_EXCLUDE:
                    continue
                it = by_id.get(f"{b}:{name}:{qid}:FULL")
                if it is None:
                    continue
                l, e, cos = channels(b, name, q)
                it["lex_channel"], it["emb_channel"] = bool(l), bool(e)
                it["emb_max_cosine"] = round(cos, 4)
                if J.gold[qid] is None:
                    lab, sub = "UNRESOLVED", "join-unresolved"
                elif l:
                    lab, sub = "PRESENT", None
                elif e:
                    lab, sub = "UNRESOLVED", "lexical-negative-embedding-positive"
                elif J.gold[qid]:
                    lab, sub = "ABSENT", "ingestion-loss-attributed"
                else:
                    lab, sub = "ABSENT", "sweep-negative"
                it["label_pre"], it["absent_mechanism"] = lab, (sub if lab == "ABSENT" else None)
                it["subtype"] = sub
                it["epsilon"] = round(eps, 4)
                counts[(b, lab, sub)] += 1

    with io.open(E1 / "build" / "items_pre.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(items, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print("\n" + "=" * 84)
    print("EXTERNAL BACKEND RE-ROUTING under Amendment 1 section 4")
    print("=" * 84)
    for k in sorted(counts):
        print(f"  {k[0]:6s} {k[1]:11s} {str(k[2]):38s} {counts[k]:4d}")

    with io.open(E1 / "two_channel_control.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump({"threshold": THRESH, "embed_model": EMBED_MODEL,
                   "control": {"n": tot, "lexical_recall": rec_l,
                               "embedding_recall": rec_e, "both": both,
                               "combined_recall": rec_c, "epsilon": eps},
                   "routing_counts": {f"{a}|{b}|{c}": v for (a, b, c), v in counts.items()},
                   "no_elicitation_call": True}, f,
                  ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    api.flush()
    print(f"\n  construction spend so far ${api.meter()['usd']:.4f}")
    print(f"wrote {E1/'two_channel_control.json'} and updated build/items_pre.json")


if __name__ == "__main__":
    main()
