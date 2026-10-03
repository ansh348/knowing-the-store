# -*- coding: utf-8 -*-
"""marker_score.py -- ADDENDUM_MARKER_ABLATION (E3): the scorer. No model call. FOK AUROC per arm (positives = non-ABSENT) on Mem0 and A-MEM
for GPT-4.1 mini (blind and structural from the recorded elicitation_main.json; omitted from the recorded E1.5 Run B rows; neutral from
marker/rows_MINI_neutral.jsonl) and on the pooled 66 for GPT-5.6 Luna (four raw-API arms, marker/rows_LUNA.jsonl, mean over >= 3 draws;
the recorded harness rows of ladder_gpt-5.6-luna.json beside). Paired differences with item-level and persona-grouped intervals
(cf2_score.paired: 1,000 draws, seed 42); the modal-score share per arm; P-X2 and P-X3. Writes marker/scores_marker.json and appends
section 12 to e1_metamemory/NUMBERS.md.
"""
from __future__ import annotations

import collections
import datetime as dt
import io
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"
for p in ("e1_metamemory/tools", "e1r_robustness/tools", "r82_counterfactual/tools"):
    sys.path.insert(0, str(ROOT / p))
import marker_arms as M  # noqa: E402
from common_e1r import auroc, boot_cluster_single  # noqa: E402
from cf2_score import paired  # noqa: E402

TOL = 0.05
MIN_DRAWS = 3
GATES = {"mem0": (0.5746, 0.4777, -0.0969), "amem": (0.5591, 0.4526, -0.1065)}      # tab:inversion, the recorded rows
RUNB = {"mem0": (0.4881, -0.0865), "amem": (0.5213, -0.0378)}                          # results/run_b_hb.json (indexed_nomarker, delta_nomarker)
LUNA_HARNESS = (0.7894, 0.4514, -0.3380)                                              # NUMBERS.md section 9, luna external pooled 66


def r4(x):
    return round(float(x), 4)


def modal_share(v):
    c = collections.Counter(np.round(v, 6)); return r4(max(c.values()) / len(v))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    items, idx, qmap, ext66 = M.load()
    lock = json.load(io.open(M.LOCK, encoding="utf-8"))
    y_of = {it["item_id"]: int(it.get("label", it["label_pre"]) != "ABSENT") for it in items}
    main_rows = json.load(io.open(E1 / "elicitation_main.json", encoding="utf-8"))
    blind = {r["question"]: float(r["fok"]) for r in main_rows if r["arm"] == "BLIND" and r["status"] == "OK" and r["fok"] is not None}
    struct = {r["tag"]: float(r["fok"]) for r in main_rows if r["arm"] == "INDEXED-TRUE" and r["status"] == "OK" and r["fok"] is not None}
    runb = {r["item_id"]: float(r["fok"]) for r in json.load(io.open(E1 / "run_b_nomarker.json", encoding="utf-8"))["rows"] if r["status"] == "OK" and r["fok"] is not None}
    neutral = {}
    for l in io.open(M.OUT / "rows_MINI_neutral.jsonl", encoding="utf-8"):
        r = json.loads(l)
        if r["status"] == "OK" and r["fok"] is not None:
            neutral[r["item_id"]] = float(r["fok"])
    res = {"registration_sha256": M.REG_SHA, "frozen_at": M.FROZEN_AT, "lock": {k: v for k, v in lock.items() if k != "build"}, "mini": {}, "luna66": {}, "when": dt.datetime.now().isoformat(timespec="seconds")}
    # ---- GPT-4.1 mini per backend
    px2 = {}
    for be in ("mem0", "amem"):
        its = [it for it in items if it["backend"] == be]
        y = np.array([y_of[it["item_id"]] for it in its], int); g = np.array([it["persona"] for it in its])
        arms = {"BLIND": np.array([blind[qmap[it["item_id"]]] for it in its]), "STRUCTURAL": np.array([struct[it["item_id"]] for it in its]),
                "OMITTED": np.array([runb[it["item_id"]] for it in its]), "NEUTRAL": np.array([neutral[it["item_id"]] for it in its])}
        b, s = r4(auroc(arms["BLIND"], y)), r4(auroc(arms["STRUCTURAL"], y))
        assert (b, s, r4(s - b)) == GATES[be], ("GATE tab:inversion", be, b, s)
        o = r4(auroc(arms["OMITTED"], y)); assert (o, r4(o - b)) == RUNB[be], ("GATE run_b_hb", be, o)
        row = {"n": len(its), "pos": int(y.sum()), "arms": {}}
        for arm, v in arms.items():
            row["arms"][arm] = {"auroc": r4(auroc(v, y)), "ci_persona": boot_cluster_single(v, y, g), "modal_share": modal_share(v), "distinct": int(len(np.unique(np.round(v, 6)))), "mean_fok": r4(v.mean()),
                                "vs_blind": (paired(arms["BLIND"], v, y, g) if arm != "BLIND" else None), "vs_structural": (paired(arms["STRUCTURAL"], v, y, g) if arm not in ("BLIND", "STRUCTURAL") else None)}
        row["omitted_recorded_result"] = {"delta_vs_blind": row["arms"]["OMITTED"]["vs_blind"]["delta"], "structural_delta": r4(s - b), "shrinks_by_at_least_half": bool(abs(row["arms"]["OMITTED"]["vs_blind"]["delta"]) <= 0.5 * abs(s - b))}
        px2[be] = bool(abs(row["arms"]["NEUTRAL"]["vs_blind"]["delta"]) <= TOL)
        row["modal_share_falls"] = {arm: bool(row["arms"][arm]["modal_share"] < row["arms"]["STRUCTURAL"]["modal_share"]) for arm in ("OMITTED", "NEUTRAL")}
        res["mini"][be] = row
    # ---- Luna on the 66 (raw API, four arms)
    per = collections.defaultdict(dict); usd = 0.0; n_bad = 0; served = set()
    for l in io.open(M.OUT / "rows_LUNA.jsonl", encoding="utf-8"):
        r = json.loads(l); usd += r.get("usd", 0.0)
        if r.get("status") == "OK" and r.get("fok") is not None:
            per[(r["item_id"], r["arm"])][int(r["draw"])] = float(r["fok"]); served.add(r.get("served_model"))
        else:
            n_bad += 1
    col = {k: float(np.mean(list(d.values()))) for k, d in per.items() if len(d) >= MIN_DRAWS}
    y = np.array([y_of[it["item_id"]] for it in ext66], int); g = np.array([it["persona"] for it in ext66])
    L = {"n": 66, "pos": int(y.sum()), "rows_not_ok": n_bad, "served": sorted(served), "usd": r4(usd), "arms": {}, "draws_census": dict(collections.Counter(len(d) for d in per.values()))}
    vec = {}
    for arm in ("BLIND", "STRUCTURAL", "OMITTED", "NEUTRAL"):
        v = np.array([col.get((it["item_id"], arm), np.nan) for it in ext66], float); assert not np.isnan(v).any(), (arm, int(np.isnan(v).sum())); vec[arm] = v
    for arm, v in vec.items():
        L["arms"][arm] = {"auroc": r4(auroc(v, y)), "ci_persona": boot_cluster_single(v, y, g), "modal_share": modal_share(v), "distinct": int(len(np.unique(np.round(v, 6)))),
                          "vs_blind": (paired(vec["BLIND"], v, y, g) if arm != "BLIND" else None), "vs_structural": (paired(vec["STRUCTURAL"], v, y, g) if arm not in ("BLIND", "STRUCTURAL") else None)}
    ladder = json.load(io.open(E1 / "ladder_gpt-5.6-luna.json", encoding="utf-8"))["rows"]
    hb = {r["item_id"]: r["fok"] for r in ladder if r["arm"] == "BLIND"}; hi = {r["item_id"]: r["fok"] for r in ladder if r["arm"] == "INDEXED-TRUE"}
    vb = np.array([hb[it["item_id"]] for it in ext66]); vi = np.array([hi[it["item_id"]] for it in ext66])
    L["harness_recorded"] = {"blind": r4(auroc(vb, y)), "structural": r4(auroc(vi, y)), "delta": r4(auroc(vi, y) - auroc(vb, y)), "gate": LUNA_HARNESS}
    assert (L["harness_recorded"]["blind"], L["harness_recorded"]["structural"], L["harness_recorded"]["delta"]) == LUNA_HARNESS, ("GATE harness 66", L["harness_recorded"])
    L["modal_share_falls"] = {arm: bool(L["arms"][arm]["modal_share"] < L["arms"]["STRUCTURAL"]["modal_share"]) for arm in ("OMITTED", "NEUTRAL")}
    res["luna66"] = L
    # ---- predictions
    res["P-X2"] = {"per_backend": px2, "holds": all(px2.values()),
                   "text": ("P-X2 HOLDS: under the neutral wording coverage is within tolerance of blind on both backends for GPT-4.1 mini (" + "; ".join(f"{be} {res['mini'][be]['arms']['NEUTRAL']['vs_blind']['delta']:+.4f}" for be in ("mem0", "amem")) + ")." if all(px2.values()) else
                            "P-X2 FAILS on " + " and ".join(be for be, ok in px2.items() if not ok) + ": under the neutral wording the coverage loss against blind is " + "; ".join(f"{be} {res['mini'][be]['arms']['NEUTRAL']['vs_blind']['delta']:+.4f} with intervals [{res['mini'][be]['arms']['NEUTRAL']['vs_blind']['item_ci']['ci_lo']:+.4f}, {res['mini'][be]['arms']['NEUTRAL']['vs_blind']['item_ci']['ci_hi']:+.4f}] and [{res['mini'][be]['arms']['NEUTRAL']['vs_blind']['persona_ci']['ci_lo']:+.4f}, {res['mini'][be]['arms']['NEUTRAL']['vs_blind']['persona_ci']['ci_hi']:+.4f}]" for be, ok in px2.items() if not ok) + ", outside tolerance.")}
    falls = {"mini": {be: res["mini"][be]["modal_share_falls"] for be in ("mem0", "amem")}, "luna66": L["modal_share_falls"]}
    res["P-X3"] = {"descriptive": True, "falls": falls}
    mini_spend = json.load(io.open(M.OUT / "cache" / "cost_ledger.json", encoding="utf-8"))["usd"]
    res["spend"] = {"mini_neutral": r4(mini_spend), "luna": r4(usd), "cap": M.CAP}
    io.open(M.OUT / "scores_marker.json", "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1, sort_keys=True, default=float) + "\n")
    # ---- ledger
    def fp(p):
        return "-" if p is None else f"{p['delta']:+.4f} ([{p['item_ci']['ci_lo']:+.4f}, {p['item_ci']['ci_hi']:+.4f}]; [{p['persona_ci']['ci_lo']:+.4f}, {p['persona_ci']['ci_hi']:+.4f}])"
    T = [f"\n## 12. ADDENDUM_MARKER_ABLATION (E3, program R117): the inexpressibility marker omitted and neutralized (registered text sha256 `{M.REG_SHA[:16]}...`, frozen at `{M.FROZEN_AT}`; `tools/marker_arms.py`, `tools/marker_score.py`; `marker/`; scored {dt.date.today().isoformat()})\n",
         "### AUX-MARKER-LOCK\n",
         f"Registration sha256 holds; the frozen prompt texts verified; the Omitted rendering (`run_b.strip_markers`, taken from the committed source by ast) reproduces the recorded E1.5 Run B cache keys on 522 of 522 items; the Neutral text is the ruling's, three lines replaced per key (77 keys), the wrapper `USER_INDEXED` with its quoted marker string replaced by the same text and nothing else (sha256 `{lock['build']['wrapper_neutral_sha256'][:16]}...`). GPT-4.1 mini NEUTRAL: 522 calls, temperature 0, seed 42, max_tokens 200, a fresh cache namespace (`marker/cache`). GPT-5.6 Luna: four arms x 66 x 5 draws, raw Chat Completions, effort and temperature unset, `max_completion_tokens` 2048, served {L['served']}.\n",
         "### AUX-MARKER-OMITTED-MINI (the recorded E1.5 Run B rows, a recorded result), AUX-MARKER-NEUTRAL-MINI, AUX-MARKER-MODAL\n",
         "| reader | backend | n / pos | arm | FOK AUROC [persona CI] | minus blind (item; persona) | minus structural (item; persona) | modal share | distinct | mean FOK |", "|---|---|---|---|---|---|---|---:|---:|---:|"]
    for be, row in res["mini"].items():
        for arm, a in row["arms"].items():
            T.append(f"| GPT-4.1 mini | {be} | {row['n']} / {row['pos']} | {arm} | {a['auroc']:.4f} [{a['ci_persona']['ci_lo']:.4f}, {a['ci_persona']['ci_hi']:.4f}] | {fp(a['vs_blind'])} | {fp(a['vs_structural'])} | {a['modal_share']:.4f} | {a['distinct']} | {a['mean_fok']:.4f} |")
    T += ["\n### AUX-MARKER-LUNA-66 (raw API; the recorded harness rows beside)\n", "| reader | arm | FOK AUROC [persona CI] | minus blind (item; persona) | minus structural (item; persona) | modal share | distinct |", "|---|---|---|---|---|---:|---:|"]
    for arm, a in L["arms"].items():
        T.append(f"| GPT-5.6 Luna (raw API, k = 5) | {arm} | {a['auroc']:.4f} [{a['ci_persona']['ci_lo']:.4f}, {a['ci_persona']['ci_hi']:.4f}] | {fp(a['vs_blind'])} | {fp(a['vs_structural'])} | {a['modal_share']:.4f} | {a['distinct']} |")
    T.append(f"| GPT-5.6 Luna (harness rows, recorded, marked as Appendix B marks them) | BLIND / STRUCTURAL | {L['harness_recorded']['blind']:.4f} / {L['harness_recorded']['structural']:.4f} | {L['harness_recorded']['delta']:+.4f} | | | |")
    T.append(f"\nDraw census (Luna): draws per item-arm {L['draws_census']}; rows not OK {L['rows_not_ok']}. The Omitted arm for GPT-4.1 mini shrinks the loss by at least half on A-MEM and not on Mem0 (a recorded result, not a prediction: " + "; ".join(f"{be} {res['mini'][be]['omitted_recorded_result']}" for be in ("mem0", "amem")) + ").\n")
    T += [f"### AUX-MARKER-P-X2\n\n**{res['P-X2']['text']}**\n", f"### AUX-MARKER-P-X3 (descriptive)\n\nThe modal-score share falls against STRUCTURAL: {json.dumps(falls)}.\n",
          f"### AUX-MARKER-SPEND\n\nGPT-4.1 mini NEUTRAL ${res['spend']['mini_neutral']:.4f}; GPT-5.6 Luna ${res['spend']['luna']:.4f} (token-metered at the page prices); against the cap of ${M.CAP:.0f}.\n"]
    with io.open(E1 / "NUMBERS.md", "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(T) + "\n")
    print("\n".join(T))


if __name__ == "__main__":
    main()
