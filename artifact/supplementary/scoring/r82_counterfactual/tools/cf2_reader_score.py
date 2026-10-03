# -*- coding: utf-8 -*-
"""cf2_reader_score.py -- program R117 (E2, E5): score a reader's rows on the 444-item counterfactual set with the CF-2 conventions,
unchanged: the X4 collapse (mean over >= 3 OK draws; k = 1 lanes their single draw; score_cf.load_lane's rule), the whole-set and per-state
AUROC against y_nok, the paired difference against the recorded embedding name lookup on the v2 lists (cf2_score.paired: item-level and
persona-grouped bootstrap, 1,000 draws, seed 42; model minus lookup), and the post-hoc PN-versus-PRESENT block with W/T/L
(reviews/v19/tools/posthoc_b_pnpresent.py's definitions). No model call.
"""
from __future__ import annotations

import collections
import io
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "reviews/v19/tools", "reviews/v18/tools"):
    sys.path.insert(0, str(ROOT / p))
from common_e1r import auroc, boot_cluster_single  # noqa: E402
from index_v3 import named_sections  # noqa: E402
import score_cf as S  # noqa: E402
from cf2_score import paired  # noqa: E402
from posthoc_b_pnpresent import boot_fraction_cluster, load_wilson  # noqa: E402

CF2 = ROOT / "r82_counterfactual" / "cf2"
STATES = ("SUPERSESSION", "RETRACTION", "EXPIRY")
LOOKUP_GATE = 0.7663


def r4(x):
    return round(float(x), 4)


def cell():
    items = json.load(io.open(CF2 / "cf_cell.json", encoding="utf-8"))["items"]
    idx = json.load(io.open(CF2 / "cf_indexes.json", encoding="utf-8"))["indexes"]
    assert len(items) == 444
    return items, idx


def lookup_v2(items, idx):
    look = np.asarray(S.matcher([it["question"] for it in items], [named_sections(idx[it["item_id"]]["v2"])["superseded"] for it in items]), float)
    y = np.array([it["y_nok"] for it in items], int)
    assert r4(auroc(look, y)) == LOOKUP_GATE, ("GATE: the recorded lookup", r4(auroc(look, y)))
    return look


def collapse(path, arm, key="unit_id"):
    """{unit: mean nok over >= MIN_DRAWS OK draws (or the single draw)}; the draw census beside."""
    per = collections.defaultdict(dict); usd = 0.0; n_rows = n_bad = 0
    for line in io.open(path, encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("arm") != arm:
            continue
        n_rows += 1; usd += r.get("usd", 0.0)
        if r.get("status") == "OK" and r.get("nok") is not None:
            per[r[key]][int(r["draw"])] = float(r["nok"])
        else:
            n_bad += 1
    out = {u: float(np.mean(list(d.values()))) for u, d in per.items() if len(d) >= S.MIN_DRAWS or len(d) == 1}
    draws = collections.Counter(len(d) for d in per.values())
    ident = sum(1 for d in per.values() if len(d) >= 2 and len(set(d.values())) == 1)
    rng = [max(d.values()) - min(d.values()) for d in per.values() if len(d) >= 2]
    return out, {"rows": n_rows, "not_ok": n_bad, "usd": round(usd, 4), "draws_per_unit": dict(draws), "units": len(per), "units_collapsed": len(out),
                 "identical_across_draws": ident, "median_range": r4(np.median(rng)) if rng else None}


def score_vector(v, items, look):
    y = np.array([it["y_nok"] for it in items], int); g = np.array([it["persona"] for it in items]); st = np.array([it["state"] for it in items])
    ver = np.array([it["version"] for it in items])
    m_cnt = st != "SUPERSESSION"
    out = {"whole": r4(auroc(v, y)), "whole_ci_persona": boot_cluster_single(v, y, g), "vs_lookup": paired(look, v, y, g), "lookup": r4(auroc(look, y)),
           "per_state": {s_: {"n": int((st == s_).sum()), "pos": int(y[st == s_].sum()), "auroc": r4(auroc(v[st == s_], y[st == s_])), "lookup": r4(auroc(look[st == s_], y[st == s_])),
                              "vs_lookup": paired(look[st == s_], v[st == s_], y[st == s_], g[st == s_])} for s_ in STATES},
           "counted_pooled": r4(auroc(v[m_cnt], y[m_cnt])), "distinct_values": int(len(np.unique(np.round(v, 6))))}
    # the post-hoc block: PN vs PRESENT, PN vs ABSENT, W/T/L over the triples
    pairs = sorted({it["pair_id"] for it in items}); pos = {(it["pair_id"], it["version"]): k for k, it in enumerate(items)}
    wilson = load_wilson()

    def block(mask):
        m_pn = mask & (ver == "PN"); m_pr = mask & (ver == "PRESENT"); m_ab = mask & (ver == "ABSENT")
        sel_pp, sel_pa = m_pn | m_pr, m_pn | m_ab
        pids = [p for p in pairs if mask[pos[(p, "PN")]]]
        w = np.array([1.0 if v[pos[(p, "PN")]] > v[pos[(p, "PRESENT")]] else 0.0 for p in pids])
        t = np.array([1.0 if v[pos[(p, "PN")]] == v[pos[(p, "PRESENT")]] else 0.0 for p in pids])
        gp = np.array([items[pos[(p, "PN")]]["persona"] for p in pids])
        wins, ties = int(w.sum()), int(t.sum()); losses = len(pids) - wins - ties; wl = wilson(wins, len(pids))
        return {"n_pairs": len(pids), "pn_vs_present": r4(auroc(v[sel_pp], y[sel_pp])), "pn_vs_absent": r4(auroc(v[sel_pa], y[sel_pa])),
                "pn_vs_present_ci_persona": boot_cluster_single(v[sel_pp], y[sel_pp], g[sel_pp]),
                "ordering": {"wins": wins, "ties": ties, "losses": losses, "strict_win_fraction": r4(wins / len(pids)), "ci_persona": boot_fraction_cluster(w, gp), "wilson": [r4(wl[0]), r4(wl[1])]}}
    out["posthoc"] = {"whole": block(np.ones(len(items), bool)), "per_state": {s_: block(st == s_) for s_ in STATES}}
    return out


def score_lane(path, arm, items, look, key="unit_id"):
    col, census = collapse(path, arm, key)
    v = np.array([col.get(it["item_id"], np.nan) for it in items], float)
    missing = int(np.isnan(v).sum())
    res = {"census": census, "missing_items": missing}
    if missing:
        res["note"] = f"{missing} items without a collapsed score; scored on the covered items only"
        m = ~np.isnan(v)
        sub = [it for it, ok in zip(items, m) if ok]
        res.update(score_vector(v[m], sub, look[m]))
    else:
        res.update(score_vector(v, items, look))
    return res


def fmt_paired(p):
    return f"{p['delta']:+.4f} ([{p['item_ci']['ci_lo']:+.4f}, {p['item_ci']['ci_hi']:+.4f}]; [{p['persona_ci']['ci_lo']:+.4f}, {p['persona_ci']['ci_hi']:+.4f}])"
