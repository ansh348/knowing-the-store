"""
e2_common.py -- shared loaders, retrieval and the cost model for E2. NO API CALLS.

Everything E2 reads is an E1 artifact committed at tag `e1-complete`; nothing here
rebuilds a store, relabels an item, or re-renders an index. The renderer lock
(PREREG_E2 section 5) is enforced here: `index_text()` returns index_v2's committed
BELIEVED rendering and there is no code path to any other rendering.

Usage: imported. Running it prints a census and asserts the split.
"""

from __future__ import annotations

import collections
import hashlib
import io
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"
E2 = ROOT / "e2_metamemory"

SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}
BACKEND = "frbank"
TOP_K = 5                       # retrieval depth, identical for every policy
EMB_PATH = E2 / "frbank_embeddings.npz"

# ---- the three context states, and nothing else (PREREG_E2 section 3) ---------
S0, S1, S2 = "S0-nofacts", "S1-facts", "S2-facts-caution"

# FR's GENERATION_SYSTEM_PROMPT, verbatim from LifeMemEval/evaluate_e2e.py:108.
GENERATION_SYSTEM_PROMPT = (
    "You are a personal AI assistant with memory about the user. "
    "Answer the user's question based ONLY on the following facts about them. "
    "Do not make up information beyond what the facts state. "
    "If the facts don't contain enough information to answer confidently, "
    'say "I don\'t have enough information about that." '
    "Keep your response concise — 1-3 sentences."
)

# FROZEN at SP1. Appended to the system prompt in state S2 and nowhere else.
CAUTION_INSTRUCTION = (
    " Some of the facts you have been given may be OUT OF DATE: the store is "
    "believed to hold content on this topic that was later superseded, retracted, "
    "or has expired. Before answering, check whether any fact you are about to "
    "use has been replaced by a later one, and prefer the later value. If you "
    "cannot tell which value is current, say so rather than stating an outdated "
    "value as fact."
)

NO_FACTS = "(no facts retrieved)"


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True, default=float)
        f.write("\n")


def sha(*parts) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(str(p).encode("utf-8"))
        h.update(b"\x1f")
    return h.hexdigest()


# --------------------------------------------------------------------- items
def load_items():
    """FR-Bank scoreable items, with question text and the split tag attached."""
    items = [i for i in jload(E1 / "build" / "items_final.json")
             if i["backend"] == BACKEND
             and i.get("label", i["label_pre"]) in SCOREABLE]
    qmap = {r["tag"]: r["question"] for r in jload(E1 / "elicitation_main.json")
            if r["arm"] != "BLIND"}
    split = jload(E2 / "CALIBRATION_SPLIT.json")
    cal = set(split["calibration_personas"])
    out = []
    for it in items:
        q = qmap.get(it["item_id"])
        assert q, f"no question text for {it['item_id']}"
        out.append({**it, "question": q,
                    "label_final": it.get("label", it["label_pre"]),
                    "split": "calibration" if it["persona"] in cal else "eval"})
    return out


def index_key(it, provenance="BELIEVED"):
    b, p, v = it["backend"], it["persona"], it["variant"]
    stem = (f"{b}:{p}:SLOT:{it['question_id']}" if v == "SLOT-ABLATED"
            else f"{b}:{p}:{v}")
    return f"{stem}:{provenance}"


class Indexes:
    """RENDERER LOCK. index_v2's committed rendering; no other path exists."""

    def __init__(self):
        self._d = jload(E1 / "indexes_v2.json")["indexes"]

    def text(self, it, provenance="BELIEVED"):
        k = index_key(it, provenance)
        assert k in self._d, f"missing index {k}"
        return self._d[k]


# ----------------------------------------------------------------- retrieval
class Retriever:
    """Top-5 cosine over the persona's own entries, variant removals applied.

    Identical for every policy: same retriever, same k, same store. The only
    thing a policy controls is WHETHER this runs.
    """

    def __init__(self):
        sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
        from backends import load_backend                       # noqa: E402
        z = np.load(EMB_PATH, allow_pickle=True)
        self.eid = list(z["entry_ids"])
        self.mat = z["vectors"].astype(np.float32)
        self.mat /= (np.linalg.norm(self.mat, axis=1, keepdims=True) + 1e-12)
        self.qtext = {str(k): v for k, v in zip(z["q_ids"], z["q_vectors"])}
        self.qmat = z["q_vectors"].astype(np.float32)
        self.qids = list(z["q_ids"])
        self.qmat /= (np.linalg.norm(self.qmat, axis=1, keepdims=True) + 1e-12)
        self.qrow = {q: i for i, q in enumerate(self.qids)}
        self.row = {e: i for i, e in enumerate(self.eid)}
        by_p = collections.defaultdict(list)
        self.text = {}
        for r in load_backend(BACKEND):
            by_p[r["persona"]].append(r["entry_id"])
            self.text[r["entry_id"]] = r["text"]
        self.by_persona = {p: sorted(v) for p, v in by_p.items()}
        self.cat_plan = jload(E1 / "build" / "variant_plan.json")["cat_ablation"]
        self.slot_abl = jload(E1 / "build" / "slot_ablations.json")
        self._cats = {r["entry_id"]: r for r in []}

    def removed(self, it):
        v = it["variant"]
        if v == "FULL":
            return set()
        if v == "SLOT-ABLATED":
            return set(self.slot_abl[f"{it['persona']}:{it['question_id']}"])
        sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
        from backends import load_backend                       # noqa: E402
        if not hasattr(self, "_catmap"):
            self._catmap = {r["entry_id"]: r["category"]
                            for r in load_backend(BACKEND)}
        cats = set(self.cat_plan[it["persona"]]["categories"])
        return {e for e in self.by_persona[it["persona"]]
                if self._catmap.get(e) in cats}

    def search(self, it):
        """Returns (facts, max_cos, entry_ids). Deterministic."""
        pool = [e for e in self.by_persona[it["persona"]]
                if e not in self.removed(it)]
        if not pool:
            return [], 0.0, []
        rows = np.array([self.row[e] for e in pool])
        q = self.qmat[self.qrow[it["question_id"]]]
        sims = self.mat[rows] @ q
        order = np.argsort(-sims, kind="mergesort")[:TOP_K]
        ids = [pool[int(i)] for i in order]
        return ([self.text[e] for e in ids], float(sims.max()), ids)


# ------------------------------------------------------------- answer prompts
def answer_messages(facts, question, state):
    facts_block = ("\n".join(f"{i+1}. {f}" for i, f in enumerate(facts))
                   if facts else NO_FACTS)
    sysmsg = GENERATION_SYSTEM_PROMPT + (CAUTION_INSTRUCTION if state == S2 else "")
    return [{"role": "system", "content": sysmsg},
            {"role": "user", "content":
             f"Here are the facts I know about you:\n\n{facts_block}\n\n"
             f"Question: {question}"}]


# ---------------------------------------------------------------- cost model
PRICE = {"gpt-4.1-mini": (0.40, 1.60)}


def usd(tin, tout, model="gpt-4.1-mini"):
    pi, po = PRICE[model]
    return tin / 1e6 * pi + tout / 1e6 * po


def main():
    items = load_items()
    c = collections.Counter((i["split"], i["label_final"]) for i in items)
    print(f"FR-Bank scoreable items: {len(items)}")
    for k in sorted(c):
        print(f"  {k[0]:12s} {k[1]:18s} {c[k]}")
    for s in ("calibration", "eval"):
        n = sum(v for k, v in c.items() if k[0] == s)
        print(f"  {s}: {n} items")
    split = jload(E2 / "CALIBRATION_SPLIT.json")
    assert sum(v for k, v in c.items() if k[0] == "calibration") == split["calibration"]["items"]
    assert sum(v for k, v in c.items() if k[0] == "eval") == split["eval"]["items"]
    print("  split matches CALIBRATION_SPLIT.json")


if __name__ == "__main__":
    main()
