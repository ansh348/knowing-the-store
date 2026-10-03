"""
embed_frbank.py -- embed the FR-Bank store and the question set. ONE-OFF BUILD.

E1 computed embeddings for the external backends only (`backend_embeddings/` holds
amem.npz and mem0.npz); FR-Bank was never embedded because E1's two-channel
instrument did not need it. E2 does: the retriever and the similarity-gate
baseline (iii) both run over cosine similarity on FR-Bank.

  model        text-embedding-3-small  -- the same model E1's two-channel
               instrument used, so the representation is continuous with E1
  scope        every FR-Bank entry, and every question text E2 can ask
  cost         ~19k entries at ~30 tokens is ~570k tokens = ~$0.011

This is a build step over STORE CONTENT, not eval-item elicitation: no judgment
is asked of any model, and the same vectors serve calibration and eval.

Usage:  python e2_metamemory/tools/embed_frbank.py
"""

from __future__ import annotations

import io
import os
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))

from e2_common import EMB_PATH, load_items                      # noqa: E402
from backends import load_backend                               # noqa: E402

MODEL = "text-embedding-3-small"
BATCH = 256
PRICE_PER_MTOK = 0.02


def client():
    env = ROOT / ".env"
    if env.exists():
        for line in io.open(env, encoding="utf-8", errors="replace"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    from openai import OpenAI
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def embed(cl, texts):
    out, ntok = [], 0
    for i in range(0, len(texts), BATCH):
        chunk = [t if t.strip() else " " for t in texts[i:i + BATCH]]
        for attempt in range(4):
            try:
                r = cl.embeddings.create(model=MODEL, input=chunk)
                break
            except Exception:                                   # noqa: BLE001
                if attempt == 3:
                    raise
                time.sleep(2 ** attempt)
        out.extend([d.embedding for d in r.data])
        ntok += r.usage.total_tokens
        print(f"  {min(i+BATCH, len(texts))}/{len(texts)}", flush=True)
    return np.asarray(out, dtype=np.float32), ntok


def main():
    if EMB_PATH.exists():
        print(f"{EMB_PATH.name} exists; nothing to do (delete to rebuild)")
        return
    rows = sorted(load_backend("frbank"), key=lambda r: r["entry_id"])
    items = load_items()
    qs = {}
    for it in items:
        qs[it["question_id"]] = it["question"]
    qid = sorted(qs)
    print(f"embedding {len(rows)} FR-Bank entries and {len(qid)} questions "
          f"with {MODEL}")

    cl = client()
    vecs, t1 = embed(cl, [r["text"] for r in rows])
    qvecs, t2 = embed(cl, [qs[q] for q in qid])
    cost = (t1 + t2) / 1e6 * PRICE_PER_MTOK

    np.savez_compressed(
        EMB_PATH,
        entry_ids=np.array([r["entry_id"] for r in rows], dtype=object),
        vectors=vecs,
        q_ids=np.array(qid, dtype=object),
        q_vectors=qvecs,
        model=np.array([MODEL], dtype=object),
    )
    print(f"tokens {t1 + t2:,} -> ${cost:.4f}")
    print(f"wrote {EMB_PATH}  ({EMB_PATH.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
