# -*- coding: utf-8 -*-
"""r125_common.py -- program R125 (matched metric, sibling-name control, store-relative labels, strong-model ablations): paths,
the cell loader, the recorded-row loaders and the matched-metric estimators. NO API CALL in this module.

Fence (the brief of 2026-09-20): every R125 file lives under reviews/r125/ (tools, results, registrations, build, the reports); the
ledger rows go to r82_counterfactual/cf2/NUMBERS_CF2.md in one new section (section 15, written between markers by r125_ledger.py);
API rows to r82_counterfactual/cf2/rows/ with an r125 prefix. reviews/v21/, reviews/r124/ and human_validation/ are never touched.

The matched metric (Task 1). The counterfactual set fixes the question and varies the store, so the design-matched comparison is
within a triple: for each of the 148 triples, the reader's score on the PN version against its score on the PRESENT version (or
the ABSENT version): a win (PN scored strictly higher), a tie (equal), a loss. The matched AUROC is (W + T/2) / n over the triples
scored. Intervals: the triple-level bootstrap (triples resampled with replacement) and the persona-grouped bootstrap (personas
resampled with replacement, each persona's triples kept intact); 1,000 draws, seed 42, 2.5 / 97.5 percentiles -- the committed
conventions of common_e1r (N_BOOT, SEED, _summarise). A paired difference between two readers is the mean over triples of the
per-triple outcome difference, with the same two bootstraps; "reliable" = both intervals exclude zero. Ties are exact equality of
the collapsed scores, as posthoc_b_pnpresent.py counts them (the printed W/T/L of Table 1 come from that rule).

The collapse of a lane's rows is score_cf.load_lane's rule, through cf2_reader_score.collapse (mean over >= 3 OK draws; a k = 1
lane its single draw); a draw-1 row takes draw 1 alone (a3_single_draw.py's convention).
"""
from __future__ import annotations

import collections
import hashlib
import io
import json
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
R125 = ROOT / "reviews" / "r125"
TOOLS, RESULTS, REGS, BUILD = R125 / "tools", R125 / "results", R125 / "registrations", R125 / "build"
CF2 = ROOT / "r82_counterfactual" / "cf2"
V2C = ROOT / "r82_counterfactual" / "v2rcat"
R122 = ROOT / "reviews" / "r122"
LEDGER = CF2 / "NUMBERS_CF2.md"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."

for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "reviews/v19/tools", "reviews/v18/tools",
          "e1_metamemory/tools", "reviews/r122/tools"):
    sys.path.insert(0, str(ROOT / p))

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

N_BOOT, SEED = 1000, 42
STATES = ("SUPERSESSION", "RETRACTION", "EXPIRY")
VERSIONS = ("PN", "PRESENT", "ABSENT")
TOL = 0.05
MIN_DRAWS = 3


# ---------------------------------------------------------------- files
def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def _default(o):
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, set):
        return sorted(o)
    raise TypeError(type(o))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=1, sort_keys=True, default=_default)
        f.write("\n")


def sha_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def reg_sha(p) -> str:
    b = Path(p).read_bytes(); i = b.find(FROZEN_END); assert i > 0, f"no marker in {p}"
    return hashlib.sha256(b[:i]).hexdigest()


def r4(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)


def ci(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"


def load_env():
    for line in io.open(ROOT / ".env", encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


# ---------------------------------------------------------------- the cell
class Cell:
    """The 444-item counterfactual cell with its triple structure."""

    def __init__(self):
        doc = jload(CF2 / "cf_cell.json")
        self.items = doc["items"]; self.meta = doc["meta"]
        self.pairs = {p["pair_id"]: p for p in jload(CF2 / "cf_pairs_cf2.json")["pairs"]}
        self.idx = jload(CF2 / "cf_indexes.json")["indexes"]
        assert len(self.items) == 444 and sum(it["y_nok"] for it in self.items) == 148
        self.y = np.array([it["y_nok"] for it in self.items], int)
        self.g = np.array([it["persona"] for it in self.items])
        self.st = np.array([it["state"] for it in self.items])
        self.ver = np.array([it["version"] for it in self.items])
        self.qs = [it["question"] for it in self.items]
        self.cats = [self.pairs[it["pair_id"]]["category"] for it in self.items]
        self.ids = [it["item_id"] for it in self.items]
        self.pair_ids = sorted({it["pair_id"] for it in self.items})
        self.pos_of = {(it["pair_id"], it["version"]): k for k, it in enumerate(self.items)}
        assert len(self.pair_ids) == 148 and all((p, v) in self.pos_of for p in self.pair_ids for v in VERSIONS)
        self.pair_state = {p: self.st[self.pos_of[(p, "PN")]] for p in self.pair_ids}
        self.pair_persona = {p: self.g[self.pos_of[(p, "PN")]] for p in self.pair_ids}
        self.n_persona = len(set(self.g))

    def pids(self, state=None):
        """The triples of one state, of a tuple of states ('RETRACTION', 'EXPIRY' = the counted states), or all 148."""
        if state is None:
            return list(self.pair_ids)
        states = (state,) if isinstance(state, str) else tuple(state)
        return [p for p in self.pair_ids if self.pair_state[p] in states]

    def vector(self, by_unit: dict) -> np.ndarray:
        """A 444-vector aligned to the items from {item_id: score}; NaN where missing."""
        return np.array([by_unit.get(i, np.nan) for i in self.ids], float)


# ---------------------------------------------------------------- rows
def collapse(path, arm, key="unit_id"):
    """{unit: mean nok over >= MIN_DRAWS OK draws (or the single draw)}; the census beside (cf2_reader_score.collapse's rule)."""
    per = collections.defaultdict(dict); usd = 0.0; n_rows = n_bad = 0
    for line in io.open(path, encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("arm") != arm:
            continue
        n_rows += 1; usd += float(r.get("usd", 0.0) or 0.0)
        if r.get("status") == "OK" and r.get("nok") is not None:
            per[r[key]][int(r["draw"])] = float(r["nok"])
        else:
            n_bad += 1
    out = {u: float(np.mean(list(d.values()))) for u, d in per.items() if len(d) >= MIN_DRAWS or len(d) == 1}
    draws = collections.Counter(len(d) for d in per.values())
    return out, {"rows": n_rows, "not_ok": n_bad, "usd": round(usd, 4), "draws_per_unit": {str(k): v for k, v in draws.items()},
                 "units": len(per), "units_collapsed": len(out)}


def draw_k(path, arm, k=1, key="unit_id"):
    """{unit: nok of draw k alone} over OK rows."""
    out = {}
    for line in io.open(path, encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("arm") == arm and int(r["draw"]) == k and r.get("status") == "OK" and r.get("nok") is not None:
            out[r[key]] = float(r["nok"])
    return out


# ---------------------------------------------------------------- the matched metric
def outcomes(cell: Cell, v: np.ndarray, neg: str, pids=None) -> np.ndarray:
    """Per-triple outcome of PN against `neg` ('PRESENT' or 'ABSENT'): 1 win, 0.5 tie, 0 loss; NaN where either score is missing."""
    pids = cell.pair_ids if pids is None else pids
    a = np.array([v[cell.pos_of[(p, "PN")]] for p in pids], float)
    b = np.array([v[cell.pos_of[(p, neg)]] for p in pids], float)
    out = np.where(a > b, 1.0, np.where(a == b, 0.5, 0.0))
    out[np.isnan(a) | np.isnan(b)] = np.nan
    return out


def wtl(out: np.ndarray) -> dict:
    o = out[~np.isnan(out)]
    w, t, l = int((o == 1.0).sum()), int((o == 0.5).sum()), int((o == 0.0).sum())
    n = len(o)
    return {"W": w, "T": t, "L": l, "n": n, "n_missing": int(np.isnan(out).sum()), "matched": r4((w + t / 2.0) / n) if n else None}


def _summarise(d):
    d = np.asarray(d, float)
    if not len(d):
        return {"n_draws": 0, "note": "no draw"}
    lo, hi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    return {"n_draws": int(len(d)), "mean": float(d.mean()), "ci_lo": lo, "ci_hi": hi, "excludes_zero": bool(lo > 0 or hi < 0)}


def boot_triple(x: np.ndarray, n=N_BOOT, seed=SEED) -> dict:
    """Triple-level bootstrap of a mean over triples (NaN triples dropped first)."""
    x = np.asarray(x, float); x = x[~np.isnan(x)]
    rng = np.random.default_rng(seed); m = len(x)
    if m == 0:
        return _summarise([])
    k = rng.integers(0, m, (n, m))
    return _summarise(x[k].mean(axis=1))


def boot_persona(x: np.ndarray, gp: np.ndarray, n=N_BOOT, seed=SEED) -> dict:
    """Persona-grouped bootstrap of a mean over triples: personas resampled with replacement, each persona's triples kept intact."""
    x = np.asarray(x, float); gp = np.asarray(gp)
    keep = ~np.isnan(x); x, gp = x[keep], gp[keep]
    if len(x) == 0:
        return _summarise([])
    groups = np.unique(gp); G = len(groups)
    sums = np.array([x[gp == u].sum() for u in groups]); cnts = np.array([(gp == u).sum() for u in groups], float)
    rng = np.random.default_rng(seed)
    drawn = rng.integers(0, G, (n, G))    # the same stream as n sequential draws of G (asserted at build time); triples of a drawn persona enter whole
    return _summarise(sums[drawn].sum(axis=1) / cnts[drawn].sum(axis=1))


def matched_block(cell: Cell, v: np.ndarray, neg: str, state=None) -> dict:
    pids = cell.pids(state)
    out = outcomes(cell, v, neg, pids)
    gp = np.array([cell.pair_persona[p] for p in pids])
    res = wtl(out)
    res["ci_triple"] = boot_triple(out); res["ci_persona"] = boot_persona(out, gp)
    return res


def paired_matched(cell: Cell, va: np.ndarray, vb: np.ndarray, neg: str, state=None) -> dict:
    """Reader A minus reader B under the matched metric: mean over triples of (outcome_A - outcome_B), both bootstraps."""
    pids = cell.pids(state)
    oa, ob = outcomes(cell, va, neg, pids), outcomes(cell, vb, neg, pids)
    d = oa - ob
    gp = np.array([cell.pair_persona[p] for p in pids])
    keep = ~np.isnan(d)
    it, cl = boot_triple(d), boot_persona(d, gp)
    return {"delta": r4(d[keep].mean()) if keep.any() else None, "n": int(keep.sum()), "a_matched": r4(oa[keep].mean()) if keep.any() else None,
            "b_matched": r4(ob[keep].mean()) if keep.any() else None, "ci_triple": it, "ci_persona": cl,
            "both_exclude_zero": bool(it.get("excludes_zero") and cl.get("excludes_zero")),
            "agree": bool(it.get("excludes_zero") == cl.get("excludes_zero"))}


# ---------------------------------------------------------------- the pooled AUROC and its pair classes
def auroc(s, y):
    """Mann-Whitney rank AUROC, ties at 0.5 (common_e1r.auroc, transcribed)."""
    s, y = np.asarray(s, float), np.asarray(y, int)
    n1, n0 = int(y.sum()), int((1 - y).sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    o = np.argsort(s, kind="mergesort"); r = np.empty(len(s), float); i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[o[j + 1]] == s[o[i]]:
            j += 1
        r[o[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def pair_classes(cell: Cell, v: np.ndarray, mask=None) -> dict:
    """The pooled AUROC decomposed over (positive, negative) pairs into three classes: within-triple, same-state across questions,
    across states. Each class's AUROC is the mean of the pair outcome (1 / 0.5 / 0); the pooled AUROC is their pair-count-weighted
    mean (asserted). Items with a missing score are excluded from both sides."""
    mask = np.ones(len(v), bool) if mask is None else mask
    ok = mask & ~np.isnan(v)
    pos = np.flatnonzero(ok & (cell.y == 1)); neg = np.flatnonzero(ok & (cell.y == 0))
    pid = np.array([it["pair_id"] for it in cell.items])
    sp, sn = v[pos][:, None], v[neg][None, :]
    outc = np.where(sp > sn, 1.0, np.where(sp == sn, 0.5, 0.0))
    same_triple = pid[pos][:, None] == pid[neg][None, :]
    same_state = cell.st[pos][:, None] == cell.st[neg][None, :]
    cls = {"within_triple": same_triple, "same_state_across_questions": same_state & ~same_triple, "across_states": ~same_state}
    res = {}
    total = outc.size
    for name, m in cls.items():
        n = int(m.sum())
        res[name] = {"pairs": n, "share": r4(n / total), "auroc": r4(outc[m].mean()) if n else None}
    pooled = float(outc.mean())
    weighted = sum(res[k]["pairs"] * (outc[cls[k]].mean() if res[k]["pairs"] else 0.0) for k in cls) / total
    assert abs(weighted - pooled) < 1e-9
    res["pooled"] = r4(pooled); res["pairs_total"] = int(total)
    res["pooled_check"] = r4(auroc(v[ok], cell.y[ok]))
    assert abs(float(res["pooled"]) - float(res["pooled_check"])) <= 0.0001, (res["pooled"], res["pooled_check"])
    return res


def per_state_pooled(cell: Cell, v: np.ndarray) -> dict:
    """The pooled AUROC within each state's own items (the paper's per-state convention) and their mean, the state-balanced pooled AUROC."""
    ok = ~np.isnan(v)
    ps = {s: r4(auroc(v[ok & (cell.st == s)], cell.y[ok & (cell.st == s)])) for s in STATES}
    return {"per_state": ps, "state_balanced": r4(np.mean([ps[s] for s in STATES])), "whole": r4(auroc(v[ok], cell.y[ok]))}
