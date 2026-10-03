"""qp_common.py -- E1-QP shared loading. READ-ONLY over committed artifacts.

Builds the two registered populations and the per-item committed model scores.
NO STORE CONTACT: the only text that ever leaves here is a question string.
"""
from __future__ import annotations

import io
import json
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"
XV = ROOT / "e1xv_crossvendor"
QP = ROOT / "e1qp_questionprior"
MIN_DRAWS = 3

XV_MODELS = ["claude-opus-5", "claude-haiku-4-5-20251001", "kimi-k3"]


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def _items():
    return {i["item_id"]: i for i in jload(E1 / "build" / "items_final.json")}


def label(it):
    return it.get("label", it["label_pre"])


def _main_rows():
    m = jload(E1 / "elicitation_main.json")
    return m["rows"] if isinstance(m, dict) else m


def questions():
    """item_id -> question string, from the committed elicitation record."""
    return {r["tag"]: r["question"] for r in _main_rows()
            if r.get("tag") and r.get("question")}


def population(which):
    """P1 = the matched FR-Bank 84 cell. P2 = FR-Bank hard row with a question."""
    items, q = _items(), questions()
    if which == "P1":
        ids = [x["item_id"] for x in jload(XV / "manifests" / "cell_84.json")["items"]]
    elif which == "P2":
        ids = sorted(k for k, i in items.items()
                     if i["backend"] == "frbank" and i["tier"] == "hard" and k in q)
    else:
        raise SystemExit(which)
    out = []
    for k in ids:
        it = items[k]
        lab = label(it)
        out.append({"item_id": k, "persona": it["persona"], "variant": it["variant"],
                    "label": lab, "question": q[k],
                    "y_nok": 1 if lab == "PRESENT-NEGATIVE" else 0,
                    "y_fok": 0 if lab == "ABSENT" else 1})
    return out


# --------------------------------------------------------------------------- #
# committed per-item model scores
# --------------------------------------------------------------------------- #
def _collapse_jsonl(path):
    """E1-XV rows -> per-item mean over surviving draws, per arm. Frozen protocol."""
    seen, acc = set(), {}
    for ln in io.open(path, encoding="utf-8"):
        if not ln.strip():
            continue
        r = json.loads(ln)
        k = (r["item_id"], r["arm"], r["draw"], r["prompt_hash"])
        if k in seen or not r["parsed"]:
            continue
        seen.add(k)
        acc.setdefault((r["item_id"], r["arm"]), []).append(r)
    out = {}
    for (tag, arm), rs in acc.items():
        if len(rs) < MIN_DRAWS:
            continue
        nk = [x["nok"] for x in rs if x["nok"] is not None]
        fk = [x["fok"] for x in rs if x["fok"] is not None]
        out[(tag, arm)] = {"nok": st.mean(nk) if nk else None,
                           "fok": st.mean(fk) if fk else None}
    return out


def _collapse_k5(path):
    """E1's committed k=5 ladder/redraw files, already per-item."""
    d = jload(path)
    return {(r["item_id"], r["arm"]): {"nok": r.get("nok"), "fok": r.get("fok")}
            for r in d["rows"]}


def model_scores():
    """{model: {(item_id, arm): {'nok':…, 'fok':…}}} for every lineage with rows."""
    S = {}
    for m in XV_MODELS:
        S[m] = _collapse_jsonl(XV / "rows" / f"elicitation_{m}.jsonl")
    S["gpt-5.6-luna"] = _collapse_k5(E1 / "ladder_gpt-5.6-luna.json")
    S["gpt-5.6-sol"] = _collapse_k5(E1 / "redraw_frontier.json")

    # gpt-4.1-mini: blind is keyed by QUESTION in the committed record (identical
    # blind prompts were deduplicated), indexed by tag. Carried as committed.
    rows = _main_rows()
    bq = {r["question"]: r for r in rows if r["arm"] == "BLIND" and r["status"] == "OK"}
    ind = {r["tag"]: r for r in rows if r["arm"] == "INDEXED-TRUE" and r["status"] == "OK"}
    q = questions()
    mini = {}
    for tag, qq in q.items():
        if qq in bq:
            mini[(tag, "BLIND")] = {"nok": bq[qq].get("nok"), "fok": bq[qq].get("fok")}
        if tag in ind:
            mini[(tag, "INDEXED-TRUE")] = {"nok": ind[tag].get("nok"),
                                           "fok": ind[tag].get("fok")}
    S["gpt-4.1-mini"] = mini
    return S


def matched_slice(pop):
    """Registered slice: positives = all PN; negatives = SLOT-ABLATED non-PN."""
    return [r for r in pop
            if r["y_nok"] == 1 or (r["variant"] == "SLOT-ABLATED" and r["y_nok"] == 0)]


def strict_slice(pop):
    """Secondary: everything slot-ablated, positives and negatives alike."""
    return [r for r in pop if r["variant"] == "SLOT-ABLATED"]
