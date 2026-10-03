# -*- coding: utf-8 -*-
"""length_r139.py -- R139 Phase 1.2 (post hoc; 2026-09-22; $0, no model call): the length-only reader.

A deterministic reader whose score is the number of names in the superseded-names section of the summary text the models saw, as rendered, and
nothing else. Scored exactly as the count readers are: pooled AUROC over the items with the persona-grouped interval (common_e1r.boot_cluster_single,
1,000 draws, seed 42), matched W/T/L and the matched score over the triples with the triple-level and persona-grouped intervals
(r125_common.matched_block), per state and on the whole set.

Three summaries:
  (a) padded   the long-list check's texts (cf_pad/build/texts.json; sha256 under the lock's method asserted equal to cf_pad/build/lock.json texts_sha256)
  (b) unpadded the default summary (r82_counterfactual/cf2/cf_indexes.json, the 'v2' text of each item)
  (c) SB       the sibling-name control (reviews/r125/build/build_t4_sibling.json 'texts', 88 SIBLING items): PN against the SIBLING version, pooled over
               the 176 items (the 88 PN positives, the 88 SIBLING negatives) and matched over the 88 supersession triples
The section is the tail of every text, opened by the header line HDR2 ('(none)' is an empty list). The length histogram (PN minus sibling) is written
beside. Branch texts were fixed in reviews/r139/BRANCHES_R139.md before this script ran (the 5.2 text uses no number from it).
Writes reviews/r139/results/length_r139.json. Usage: python reviews/r139/tools/length_r139.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews" / "r139" / "results" / "length_r139.json"
for p in ("e1r_robustness/tools", "reviews/r125/tools"):
    sys.path.insert(0, str(ROOT / p))

import numpy as np  # noqa: E402
import common_e1r as E  # noqa: E402
import r125_common as C  # noqa: E402

HDR2 = "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT  (value-scrubbed)"


def J(rel):
    return json.load(open(ROOT / rel, encoding="utf-8"))


def n_names(text):
    assert text.count(HDR2) == 1
    body = []
    for ln in text[text.index(HDR2) + len(HDR2):].split("\n")[1:]:
        if not ln.strip():
            break
        body.append(ln.strip())
    s = " ".join(body)
    if s == "(none)":
        return 0
    names = [x.strip() for x in s.split(", ")]
    assert not any(x.startswith("(+") for x in names) and len(names) == len(set(names)), text[-300:]
    return len(names)


def ci(d):
    return [round(d["ci_lo"], 4), round(d["ci_hi"], 4)]


def score(cell, v, label, states=("SUPERSESSION", "RETRACTION", "EXPIRY")):
    out = {}
    for scope in ("whole",) + states:
        st = None if scope == "whole" else scope
        pids = cell.pids(st)
        m = np.array([cell.pair_state[it["pair_id"]] in ((st,) if st else C.STATES) for it in cell.items]) & ~np.isnan(v)
        pooled = float(E.auroc(v[m], cell.y[m]))
        pci = E.boot_cluster_single(v[m], cell.y[m], cell.g[m])
        mb = C.matched_block(cell, v, "PRESENT", st)
        out[scope.lower()] = {"n_items": int(m.sum()), "n_triples": len(pids), "pooled": round(pooled, 4), "pooled_persona_ci": ci(pci),
                              "W": mb["W"], "T": mb["T"], "L": mb["L"], "matched": mb["matched"], "matched_triple_ci": ci(mb["ci_triple"]), "matched_persona_ci": ci(mb["ci_persona"])}
    return out


def main():
    cell = C.Cell()
    pad = J("cf_pad/build/texts.json")
    lock = J("cf_pad/build/lock.json")
    assert hashlib.sha256("\x1f".join(pad[k] for k in sorted(pad)).encode("utf-8")).hexdigest() == lock["texts_sha256"]
    idx = J("r82_counterfactual/cf2/cf_indexes.json")["indexes"]
    sib = J("reviews/r125/build/build_t4_sibling.json")["texts"]
    L_pad = {k: n_names(t) for k, t in pad.items()}
    L_unp = {k: n_names(idx[k]["v2"]) for k in cell.ids}
    L_sib = {k: n_names(t) for k, t in sib.items()}
    assert len(L_pad) == 444 and len(L_sib) == 88
    res = {"reader": "length-only: the number of names in the superseded-names section of the text the reader saw", "post_hoc": True}
    res["padded"] = score(cell, cell.vector(L_pad), "padded")
    res["unpadded"] = score(cell, cell.vector(L_unp), "unpadded")
    # (c) SB: PN against SIBLING (88 supersession triples; pooled over 176 items; matched: PN outscores SIBLING, ties half)
    sup = cell.pids("SUPERSESSION")
    pn = np.array([L_unp[f"{p}|PN"] for p in sup], float)
    sb = np.array([L_sib[f"{p}|SIBLING"] for p in sup], float)
    gp = np.array([cell.pair_persona[p] for p in sup])
    y = np.r_[np.ones(len(sup), int), np.zeros(len(sup), int)]
    s = np.r_[pn, sb]; g = np.r_[gp, gp]
    pooled = float(E.auroc(s, y)); pci = E.boot_cluster_single(s, y, g)
    o = np.where(pn > sb, 1.0, np.where(pn == sb, 0.5, 0.0))
    res["sibling"] = {"supersession": {"n_items": int(len(s)), "n_triples": len(sup), "pooled": round(pooled, 4), "pooled_persona_ci": ci(pci),
                                        "W": int((o == 1).sum()), "T": int((o == 0.5).sum()), "L": int((o == 0).sum()), "matched": round(float(o.mean()), 4),
                                        "matched_triple_ci": ci(C.boot_triple(o)), "matched_persona_ci": ci(C.boot_persona(o, gp))}}
    # the length histograms: PN minus each sibling, per triple
    hist = {}
    for name, L, sibs in (("padded", L_pad, ("PRESENT", "ABSENT")), ("unpadded", L_unp, ("PRESENT", "ABSENT")), ("sibling", {**L_unp, **L_sib}, ("SIBLING",))):
        for scope, pids in (("supersession", sup), ("whole", cell.pids())):
            if name == "sibling" and scope == "whole":
                continue
            h = collections.Counter()
            for p in pids:
                for v in sibs:
                    h[L[f"{p}|PN"] - L[f"{p}|{v}"]] += 1
            hist[f"{name}|{scope}"] = {str(k): h[k] for k in sorted(h)}
    res["hist_pn_minus_sibling"] = hist
    pnl = [L_unp[f"{p}|PN"] for p in sup]
    prl = [L_unp[f"{p}|PRESENT"] for p in sup]
    res["unpadded_supersession_lists"] = {"pn_mean": round(float(np.mean(pnl)), 4), "pn_max": int(max(pnl)), "present_empty": int(sum(1 for x in prl if x == 0)), "n": len(sup)}
    res["padded_lengths"] = {"pn_min": min(L_pad[f"{p}|PN"] for p in cell.pids()), "pn_max": max(L_pad[f"{p}|PN"] for p in cell.pids()),
                             "sib_min": min(L_pad[f"{p}|{v}"] for p in cell.pids() for v in ("PRESENT", "ABSENT")), "sib_max": max(L_pad[f"{p}|{v}"] for p in cell.pids() for v in ("PRESENT", "ABSENT"))}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
