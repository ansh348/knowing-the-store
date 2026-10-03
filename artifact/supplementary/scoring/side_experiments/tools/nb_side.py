"""nb_side.py -- SIDE-BUILD-1 step 4: NB-4 and NB-5 on every S1 GT index (ADDENDUM_SIDE.md section S1
step 4, ruling #7; frozen e8b2630). NO API CALLS; local, $0. NB-6 does not run on the GT indexes.

As e1r_robustness/SPEC_E1R.md (b) defines them and run_baselines.py implements them, over the
committed FOK populations (Mem0 238 / 94 positive, A-MEM 284 / 126), the item joined to its blind
and INDEXED-TRUE rows exactly as common_e1r.assemble joins them, the index text being the GT
index of the item's persona and backend (side_experiments/s1/indexes_gt.json):
  NB-4  max content-token Jaccard between the question and each attribute name the index exposes
        (index_features.parse -> attr_by_cat; toks; '_' -> ' ');
  NB-5  max cosine between the question and each attribute-name string under
        sentence-transformers/all-MiniLM-L6-v2 from the local HuggingFace cache (offline).
Scored directly (unsupervised, no fold) by common_e1r.auroc; the persona-clustered single-arm
bootstrap (common_e1r.boot_cluster_single, 1,000 draws, seed 42) prints beside as descriptive.
Beside each: the committed NB-4 / NB-5 on the paper's TRUE index of the same backend
(e1r_robustness/results/baselines_final.json; 0.5, attribute names inexpressible there) and the
committed monitor blind / INDEXED-TRUE AUROC.

Writes side_experiments/s1/nb_side.json.   Usage:  python side_experiments/tools/nb_side.py
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys

import numpy as np

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import side_common as SC                                         # noqa: E402
from side_common import ROOT, J, jdump                           # noqa: E402
from common_e1r import POPULATIONS, auroc, boot_cluster_single, load_e1   # noqa: E402
from index_features import parse, toks                           # noqa: E402

FREEZE = "e8b2630"
ENCODER = "sentence-transformers/all-MiniLM-L6-v2"
POP = {"mem0": ("R-FOK-MEM0", 238, 94), "amem": ("R-FOK-AMEM", 284, 126)}
FAILS: list[str] = []


def gate(name, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'} {name}" + (f": {detail}" if detail and not ok else ""))
    if not ok:
        FAILS.append(f"{name}: {detail}")


def jac(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0.0


def rows_for(b, items, blind, idxT, gt):
    """The committed FOK population of backend b, joined as common_e1r.assemble / run_baselines.build join it."""
    spec = POPULATIONS[POP[b][0]]
    out = []
    for it in items:
        if not spec["filt"](it):
            continue
        q, tag = it["question"], it["item_id"]
        if q not in blind or tag not in idxT:
            continue
        bv, iv = blind[q].get("fok"), idxT[tag].get("fok")
        if bv is None or iv is None:
            continue
        lab = it.get("label", it["label_pre"])
        p = parse(gt[SC.gt_key(b, it["persona"])])
        attrs = [a for v in p["attr_by_cat"].values() for a in v]
        qt = toks(q)
        out.append({"item_id": tag, "persona": it["persona"], "y": 0 if lab == "ABSENT" else 1, "question": q,
                    "monitor_blind": bv, "monitor_true": iv, "attrs": attrs,
                    "nb4": max((jac(qt, toks(a.replace("_", " "))) for a in attrs), default=0.0)})
    return out


def nb5(rows):
    """run_baselines.embed_scores, verbatim in effect: unique questions and names encoded once, max cosine."""
    from sentence_transformers import SentenceTransformer
    enc = SentenceTransformer(ENCODER, device="cpu")
    uniq_q = sorted({r["question"] for r in rows}); uniq_a = sorted({a for r in rows for a in r["attrs"]})
    qv = enc.encode(uniq_q, normalize_embeddings=True, batch_size=128, show_progress_bar=False)
    av = enc.encode([a.replace("_", " ") for a in uniq_a], normalize_embeddings=True, batch_size=256, show_progress_bar=False)
    qi = {q: k for k, q in enumerate(uniq_q)}; ai = {a: k for k, a in enumerate(uniq_a)}
    for r in rows:
        r["nb5"] = float(np.max(av[[ai[a] for a in r["attrs"]]] @ qv[qi[r["question"]]])) if r["attrs"] else 0.0


def main():
    print(f"nb_side -- SIDE-BUILD-1 step 4, NB-4 / NB-5 on the GT indexes (frozen {FREEZE}); local, no API call")
    rc = subprocess.run([sys.executable, str(SC.SIDE / "tools" / "verify_side.py")], capture_output=True, text=True).returncode
    gate("verify_side.py passes", rc == 0, f"exit {rc}")
    items, blind, idxT, _ = load_e1()
    gt = J(SC.S1 / "indexes_gt.json")["indexes"]
    committed = J(ROOT / "e1r_robustness/results/baselines_final.json")["rows"]
    out = {"registration": "registrations/ADDENDUM_SIDE.md", "frozen": FREEZE, "no_api_calls": True, "encoder": ENCODER + " (local, offline)",
           "spec": "e1r_robustness/SPEC_E1R.md (b) NB-4, NB-5; scored directly by common_e1r.auroc; NB-6 not run on the GT indexes",
           "gt_indexes_sha256": hashlib.sha256((SC.S1 / "indexes_gt.json").read_bytes()).hexdigest(), "rows": {}}
    for b, (rid, n, npos) in POP.items():
        rows = rows_for(b, items, blind, idxT, gt)
        y = np.array([r["y"] for r in rows], int); g = np.array([r["persona"] for r in rows])
        gate(f"{b}: population {n} with {npos} positives, every item's GT index present", (len(rows), int(y.sum())) == (n, npos) and all(r["attrs"] for r in rows),
             f"{len(rows)} {int(y.sum())}")
        nb5(rows)
        c = committed[f"{rid}|TRUE"]
        gate(f"{b}: committed monitor blind / INDEXED-TRUE reproduced from the committed rows ({c['monitor_blind']:.4f} / {c['monitor_indexed']:.4f})",
             abs(auroc([r["monitor_blind"] for r in rows], y) - c["monitor_blind"]) < 1e-9 and abs(auroc([r["monitor_true"] for r in rows], y) - c["monitor_indexed"]) < 1e-9)
        res = {"population": rid, "n": len(rows), "n_pos": int(y.sum()), "n_personas": len(set(g.tolist())),
               "mean_attrs_per_index": float(np.mean([len(r["attrs"]) for r in rows]))}
        for k, name in (("nb4", "NB-4 lexical match"), ("nb5", "NB-5 embedding match")):
            s = [r[k] for r in rows]
            res[k] = {"auroc": auroc(s, y), "clustered": boot_cluster_single(s, y, g), "score_mean": float(np.mean(s)),
                      "score_zero_share": float(np.mean([v == 0.0 for v in s])),
                      "committed_on_paper_TRUE_index": c["legitimate_baselines"][name]}
        res["committed_monitor"] = {"blind": c["monitor_blind"], "indexed_true": c["monitor_indexed"], "gain": c["monitor_indexed"] - c["monitor_blind"]}
        res["items"] = [{"item_id": r["item_id"], "y": r["y"], "nb4": r["nb4"], "nb5": r["nb5"]} for r in rows]
        out["rows"][b] = res
        print(f"  {b}: n={len(rows)} pos={int(y.sum())}  NB-4 {res['nb4']['auroc']:.4f} [{res['nb4']['clustered']['ci_lo']:.4f}, {res['nb4']['clustered']['ci_hi']:.4f}]"
              f"  NB-5 {res['nb5']['auroc']:.4f} [{res['nb5']['clustered']['ci_lo']:.4f}, {res['nb5']['clustered']['ci_hi']:.4f}]"
              f"  (committed on the paper's TRUE index: {c['legitimate_baselines']['NB-4 lexical match']:.2f} / {c['legitimate_baselines']['NB-5 embedding match']:.2f};"
              f" monitor blind {c['monitor_blind']:.4f}, INDEXED-TRUE {c['monitor_indexed']:.4f}); mean names per index {res['mean_attrs_per_index']:.1f}")
    if FAILS:
        print(f"\nnb_side: {len(FAILS)} FAIL -- STOP; nothing written"); return 1
    jdump(out, SC.S1 / "nb_side.json")
    print(f"\nwrote {SC.S1 / 'nb_side.json'}\nnb_side: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
