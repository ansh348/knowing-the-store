# -*- coding: utf-8 -*-
"""posthoc_b_pnpresent.py -- B1, B2, B3 of reviews/integration/POSTHOC_SPEC_R112.md (program R112, 2026-09-16).
NO MODEL CALL. $0. Post-hoc analyses on recorded rows, specified before recomputation; every input is a recorded
artifact and every estimator an imported, unedited function (common_e1r, score_cf, cf2_score, a1_count_readers).

B1  per reader, summary and state: AUROC of the PN versions against the PRESENT versions only, against the ABSENT
    versions only, and pooled (asserted equal to the mean of the two to four decimals); persona-clustered interval
    of the PN-vs-PRESENT AUROC.
B2  per triple: win (s(PN) > s(PRESENT)), tie, loss; the strict-win fraction with the persona-clustered bootstrap
    interval (interpreted) and the Wilson interval (beside); the tie count printed with it.
B3  the coverage-only reference (1 on PN and PRESENT, 0 on ABSENT), whole and per state.

Reproduction gates (the script stops on a mismatch): lookup v2 0.7663, all-states v3 0.8756, mini v2 0.7167,
Haiku 4.5 v2 0.7566, Opus 5 v2 0.8405 (AUX-CF2-*).
Usage: python reviews/v19/tools/posthoc_b_pnpresent.py       Writes reviews/v19/results/posthoc_b.json
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "reviews/v19/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from common_e1r import N_BOOT, SEED, auroc, boot_cluster_single, _summarise  # noqa: E402
from index_features import parse as parse_index  # noqa: E402
from index_v3 import named_sections  # noqa: E402
import score_cf as S  # noqa: E402
import cf2_score  # noqa: E402,F401  (sets S.R82 = cf2 at import)
from a1_count_readers import reader_scores  # noqa: E402
from wilson_a7 import load_wilson  # noqa: E402

SPEC = ROOT / "reviews" / "integration" / "POSTHOC_SPEC_R112.md"
SPEC_SHA = "ae2600fcf39cf2d626c449835dbbf4dde308cc2e1b07d3e1991d566f920564a6"
CF2 = ROOT / "r82_counterfactual" / "cf2"
OUT = ROOT / "reviews" / "v19" / "results" / "posthoc_b.json"
LANES = {"MINI": "gpt-4.1-mini", "H45": "claude-haiku-4-5-20251001", "OP5": "claude-opus-5"}
STATES = ("SUPERSESSION", "RETRACTION", "EXPIRY")
GATES = {"lookup_v2": 0.7663, "allstates_v3": 0.8756, "mini_v2": 0.7167, "h45_v2": 0.7566, "op5_v2": 0.8405}


def r4(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)


def boot_fraction_cluster(wins, g, n=N_BOOT, seed=SEED):
    """Persona-clustered bootstrap of a fraction over pairs: personas resampled with replacement, the fraction recomputed."""
    rng = np.random.default_rng(seed)
    wins, g = np.asarray(wins, float), np.asarray(g)
    groups = np.unique(g); idx = {u: np.flatnonzero(g == u) for u in groups}
    d = []
    for _ in range(n):
        drawn = rng.integers(0, len(groups), len(groups))
        k = np.concatenate([idx[groups[t]] for t in drawn])
        d.append(float(wins[k].mean()))
    return _summarise(d)


def main():
    assert hashlib.sha256(SPEC.read_bytes()).hexdigest() == SPEC_SHA, "the spec file changed after its hash was ledgered"
    wilson = load_wilson()
    cell = json.load(io.open(CF2 / "cf_cell.json", encoding="utf-8")); items = cell["items"]
    pairs = {p["pair_id"]: p for p in json.load(io.open(CF2 / "cf_pairs_cf2.json", encoding="utf-8"))["pairs"]}
    idx = json.load(io.open(CF2 / "cf_indexes.json", encoding="utf-8"))["indexes"]
    assert len(items) == 444
    y = np.array([it["y_nok"] for it in items], int); g = np.array([it["persona"] for it in items])
    st = np.array([it["state"] for it in items]); ver = np.array([it["version"] for it in items])
    qs = [it["question"] for it in items]; cats = [pairs[it["pair_id"]]["category"] for it in items]
    pair_ids = sorted({it["pair_id"] for it in items})
    pos_of = {}
    for k, it in enumerate(items):
        pos_of[(it["pair_id"], it["version"])] = k
    assert len(pair_ids) == 148 and all((p, v) in pos_of for p in pair_ids for v in ("PN", "PRESENT", "ABSENT"))

    res = {"meta": {"script": "reviews/v19/tools/posthoc_b_pnpresent.py", "spec": str(SPEC.relative_to(ROOT)), "spec_sha256": SPEC_SHA,
                    "model_calls": 0, "n_boot": N_BOOT, "seed": SEED, "status": "post hoc, specified before recomputation"},
           "gates": {}, "readers": {}, "coverage_only": {}, "notes": []}

    # ---- reader score vectors (444 each)
    scores = {}
    sup2 = [named_sections(idx[it["item_id"]]["v2"])["superseded"] for it in items]
    s3 = [named_sections(idx[it["item_id"]]["v3"]) for it in items]
    all3 = [s["superseded"] + s["retracted"] + s["expired"] for s in s3]
    scores[("name lookup", "v2")] = np.asarray(S.matcher(qs, sup2), float)
    scores[("all-states lookup", "v3")] = np.asarray(S.matcher(qs, all3), float)
    for tag in ("v2",):
        cr = {"CR-nb1": np.zeros(444), "CR-oracle-a": np.zeros(444)}
        for k, it in enumerate(items):
            d = reader_scores(idx[it["item_id"]][tag], it["question"], cats[k], it["state"])
            cr["CR-nb1"][k] = d["CR-nb1"]; cr["CR-oracle-a"][k] = d["CR-oracle-a"]
        scores[("category-guessing count reader", tag)] = cr["CR-nb1"]
        scores[("category-aware count reader", tag)] = cr["CR-oracle-a"]
    for code, model in LANES.items():
        lane = S.load_lane(code)
        for arm, tag in (("INDEXED-V2", "v2"), ("INDEXED-V3", "v3")):
            v = np.array([lane.get((it["item_id"], arm), np.nan) for it in items], float)
            assert not np.isnan(v).any(), f"{code} {arm} has missing items"
            scores[(model, tag)] = v
    gates = {"lookup_v2": r4(auroc(scores[("name lookup", "v2")], y)), "allstates_v3": r4(auroc(scores[("all-states lookup", "v3")], y)),
             "mini_v2": r4(auroc(scores[("gpt-4.1-mini", "v2")], y)), "h45_v2": r4(auroc(scores[("claude-haiku-4-5-20251001", "v2")], y)),
             "op5_v2": r4(auroc(scores[("claude-opus-5", "v2")], y))}
    for k_, v_ in GATES.items():
        assert gates[k_] == v_, f"GATE {k_}: {gates[k_]} != {v_}"
    res["gates"] = gates

    # ---- B3 the coverage-only reference
    cov = np.where(ver == "ABSENT", 0.0, 1.0)
    res["coverage_only"] = {"whole": r4(auroc(cov, y)), "per_state": {s_: r4(auroc(cov[st == s_], y[st == s_])) for s_ in STATES},
                            "definition": "s = 1 on PN and PRESENT versions, 0 on ABSENT versions; pooled AUROC against both negative groups"}

    # ---- B1 and B2 per reader
    def block(s, mask, label):
        m_pn = mask & (ver == "PN"); m_pr = mask & (ver == "PRESENT"); m_ab = mask & (ver == "ABSENT")
        sel_pp = m_pn | m_pr; sel_pa = m_pn | m_ab; sel_all = mask
        a_pp = auroc(s[sel_pp], y[sel_pp]); a_pa = auroc(s[sel_pa], y[sel_pa]); a_pool = auroc(s[sel_all], y[sel_all])
        assert abs(round(a_pool, 4) - round(0.5 * (a_pp + a_pa), 4)) <= 0.0001, f"identity fails for {label}: {a_pool} vs {0.5*(a_pp+a_pa)}"
        # B2 over the triples in the mask
        pids = [p for p in pair_ids if mask[pos_of[(p, "PN")]]]
        w = np.array([1.0 if s[pos_of[(p, "PN")]] > s[pos_of[(p, "PRESENT")]] else 0.0 for p in pids])
        t = np.array([1.0 if s[pos_of[(p, "PN")]] == s[pos_of[(p, "PRESENT")]] else 0.0 for p in pids])
        gp = np.array([items[pos_of[(p, "PN")]]["persona"] for p in pids])
        wins, ties, losses = int(w.sum()), int(t.sum()), int(len(pids) - w.sum() - t.sum())
        wl = wilson(wins, len(pids))
        return {"n_pairs": len(pids), "pn_vs_present": r4(a_pp), "pn_vs_absent": r4(a_pa), "pooled": r4(a_pool),
                "identity_pooled_equals_mean": True,
                "pn_vs_present_ci_persona": boot_cluster_single(s[sel_pp], y[sel_pp], g[sel_pp]),
                "ordering": {"wins": wins, "ties": ties, "losses": losses, "strict_win_fraction": r4(wins / len(pids)),
                             "ci_persona": boot_fraction_cluster(w, gp), "wilson": [r4(wl[0]), r4(wl[1])],
                             "note": "ties counted as failures; not a tie-adjusted ranking accuracy; chance reference is not 0.50 when ties occur"}}

    for (reader, tag), s in scores.items():
        row = {"summary": tag, "whole": block(s, np.ones(444, bool), f"{reader}/{tag}/whole"), "per_state": {}}
        for s_ in STATES:
            row["per_state"][s_] = block(s, st == s_, f"{reader}/{tag}/{s_}")
        res["readers"][f"{reader} | {tag}"] = row

    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1, ensure_ascii=False))
    # ---- print
    print(f"spec {SPEC_SHA[:16]}  gates {gates}")
    print(f"coverage-only reference: whole {res['coverage_only']['whole']}  per state {res['coverage_only']['per_state']}")
    print(f"{'reader | summary':44s} {'scope':12s} {'PNvPR':>7s} {'PNvAB':>7s} {'pooled':>7s}  {'persona CI (PNvPR)':22s}  wins/ties/losses  frac  persona CI  Wilson")
    for key, row in res["readers"].items():
        for scope, b in (("whole", row["whole"]),) + tuple((s_, row["per_state"][s_]) for s_ in STATES):
            o = b["ordering"]; c = b["pn_vs_present_ci_persona"]; oc = o["ci_persona"]
            print(f"{key:44s} {scope:12s} {b['pn_vs_present']:7.4f} {b['pn_vs_absent']:7.4f} {b['pooled']:7.4f}  [{c['ci_lo']:+.4f},{c['ci_hi']:+.4f}]  "
                  f"{o['wins']:3d}/{o['ties']:3d}/{o['losses']:3d}  {o['strict_win_fraction']:.4f}  [{oc['ci_lo']:.4f},{oc['ci_hi']:.4f}]  [{o['wilson'][0]:.4f},{o['wilson'][1]:.4f}]")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
