"""score_e1xv.py -- E1-XV STEP 2 scoring, per PREREG_E1XV.md (386d334...) and nothing else.

NO new calls. Reads the committed raw rows and produces:
  * per-lineage blind/indexed FOK and NOK AUROC with the paper's bootstrap CIs
  * the five registered items, adjudicated mechanically
  * draw-stability descriptives beside every AUROC (prereg section 6, ruling 3)
  * parse-failure counts per lane per arm, and MIN_DRAWS exclusions

Estimators are IMPORTED from the committed scorers, not reimplemented, so these CIs
come from the same code that produced NUMBERS.md section 9.
"""
from __future__ import annotations

import io
import json
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
XV = ROOT / "e1xv_crossvendor"
E1 = ROOT / "e1_metamemory"
sys.path.insert(0, str(E1 / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from score_e1 import auroc, boot        # noqa: E402  committed estimators
from score_ladder import auroc_ci       # noqa: E402  one-sample CI, XV-1 needs it

MIN_DRAWS = 3                            # frozen protocol
K = 5
MODELS = ["claude-opus-5", "claude-haiku-4-5-20251001", "kimi-k3"]
FRONTIER = ["claude-opus-5", "kimi-k3"]
ARMS = ["BLIND", "INDEXED-TRUE"]
OPENAI_BAND = (0.7090, 0.7463)           # NUMBERS.md section 9 indexed FOK
XV4_LO, XV4_HI = OPENAI_BAND[0] - 0.05, OPENAI_BAND[1] + 0.05


def load(model):
    p = XV / "rows" / f"elicitation_{model}.jsonl"
    seen, rows = set(), []
    for ln in io.open(p, encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        r = json.loads(ln)
        k = (r["item_id"], r["arm"], r["draw"], r["prompt_hash"])
        if k in seen:                    # dedup by cache key, first wins
            continue
        seen.add(k); rows.append(r)
    return rows


def collapse(rows):
    """Per-item mean over SURVIVING draws, per arm. Frozen protocol."""
    acc, meta = {}, {}
    for r in rows:
        meta[r["item_id"]] = {"y_fok": r["y_fok"], "y_nok": r["y_nok"],
                              "label": r["label"]}
        if not r["parsed"] or r["fok"] is None:
            continue
        acc.setdefault((r["item_id"], r["arm"]), []).append(r)
    out, excluded = {}, []
    for (tag, arm), rs in acc.items():
        if len(rs) < MIN_DRAWS:
            excluded.append({"item_id": tag, "arm": arm, "surviving": len(rs)})
            continue
        out[(tag, arm)] = {
            "fok": st.mean(x["fok"] for x in rs),
            "nok": st.mean(x["nok"] for x in rs if x["nok"] is not None)
            if any(x["nok"] is not None for x in rs) else None,
            "n_draws": len(rs),
            "fok_sd": st.stdev([x["fok"] for x in rs]) if len(rs) > 1 else 0.0,
            "nok_sd": st.stdev([x["nok"] for x in rs if x["nok"] is not None])
            if sum(1 for x in rs if x["nok"] is not None) > 1 else 0.0,
            "identical": len({(x["fok"], x["nok"]) for x in rs}) == 1 and len(rs) == K,
        }
    # items whose arm never appeared at all
    for tag in meta:
        for arm in ARMS:
            if (tag, arm) not in out and not any(e["item_id"] == tag and e["arm"] == arm
                                                 for e in excluded):
                excluded.append({"item_id": tag, "arm": arm, "surviving": 0})
    return out, meta, excluded


def parse_stats(rows):
    s = {}
    for arm in ARMS:
        rs = [r for r in rows if r["arm"] == arm]
        n = len(rs)
        fail = sum(1 for r in rs if not r["parsed"])
        err = sum(1 for r in rs if r["status"].startswith("ERROR"))
        trunc = sum(1 for r in rs if r["finish_reason"] in ("max_tokens", "length"))
        s[arm] = {"n": n, "parse_fail": fail, "errors": err, "truncated": trunc,
                  "fail_rate": fail / n if n else None,
                  "FLAGGED": (fail / n > 0.05) if n else False}
    return s


def cell(coll, meta, judgment):
    """One lineage-judgment cell: blind vs indexed AUROC, delta, CIs."""
    ykey = "y_fok" if judgment == "fok" else "y_nok"
    tags = sorted({t for (t, a) in coll
                   if (t, "BLIND") in coll and (t, "INDEXED-TRUE") in coll
                   and coll[(t, "BLIND")][judgment] is not None
                   and coll[(t, "INDEXED-TRUE")][judgment] is not None})
    y = [meta[t][ykey] for t in tags]
    if len(set(y)) < 2:
        return {"n": len(tags), "note": "single-class"}
    b = [coll[(t, "BLIND")][judgment] for t in tags]
    i = [coll[(t, "INDEXED-TRUE")][judgment] for t in tags]
    bci, ici = auroc_ci(b, y), auroc_ci(i, y)
    bs = boot(b, i, y)
    return {"n": len(tags), "n_pos": int(sum(y)),
            "blind": auroc(b, y), "indexed": auroc(i, y),
            "delta": auroc(i, y) - auroc(b, y),
            "blind_ci": [bci["ci_lo"], bci["ci_hi"]],
            "blind_includes_0.50": bci["includes_0.50"],
            "indexed_ci": [ici["ci_lo"], ici["ci_hi"]],
            "delta_ci": [bs["ci_lo"], bs["ci_hi"]],
            "delta_excludes_zero": bs["excludes_zero"],
            "mean_blind": st.mean(b), "mean_indexed": st.mean(i),
            "distinct_blind": len(set(b)), "distinct_indexed": len(set(i)),
            "tie_degenerate": len(set(b)) == 1}


def stability(coll, judgment):
    out = {}
    for arm in ARMS:
        sds = [v[f"{judgment}_sd"] for (t, a), v in coll.items() if a == arm]
        ident = [v["identical"] for (t, a), v in coll.items() if a == arm]
        if not sds:
            continue
        out[arm] = {"n_items": len(sds), "sd_mean": st.mean(sds),
                    "sd_median": st.median(sds), "sd_max": max(sds),
                    "identical_across_5": sum(1 for x in ident if x)}
    if len(out) == 2 and out["BLIND"]["sd_mean"]:
        out["dispersion_ratio_indexed_over_blind"] = (
            out["INDEXED-TRUE"]["sd_mean"] / out["BLIND"]["sd_mean"])
    return out


def main():
    R = {"prereg_sha256": "386d334319bdfeebf1cb38eafe934eb3164f11bf6e692dca44f7fd4ad07ab61e",
         "min_draws": MIN_DRAWS, "k": K, "openai_indexed_fok_band": list(OPENAI_BAND),
         "xv4_window": [XV4_LO, XV4_HI], "lineages": {}}

    for model in MODELS:
        rows = load(model)
        coll, meta, excl = collapse(rows)
        ps = parse_stats(rows)
        R["lineages"][model] = {
            "n_rows": len(rows),
            "usd": round(sum(r.get("usd", 0) for r in rows), 4),
            "served_models": sorted({r["served_model"] for r in rows if r["served_model"]}),
            "parse": ps,
            "excluded_below_min_draws": excl,
            "n_excluded": len(excl),
            "FOK": cell(coll, meta, "fok"), "NOK": cell(coll, meta, "nok"),
            "stability_fok": stability(coll, "fok"),
            "stability_nok": stability(coll, "nok"),
        }

    # ---------------- registered predictions, adjudicated mechanically
    L = R["lineages"]
    xv1 = {m: bool(L[m]["NOK"].get("blind_includes_0.50")) for m in MODELS}
    xv2 = {m: bool(L[m]["NOK"].get("delta", 0) > 0
                   and L[m]["NOK"].get("delta_excludes_zero")) for m in FRONTIER}
    xv3 = (L["claude-opus-5"]["FOK"]["blind"]
           > L["claude-haiku-4-5-20251001"]["FOK"]["blind"])
    xv4 = {m: bool(XV4_LO <= L[m]["FOK"]["indexed"] <= XV4_HI) for m in MODELS}
    R["predictions"] = {
        "XV-1": {"per_model": xv1, "HOLDS": all(xv1.values())},
        "XV-2": {"per_model": xv2, "HOLDS": all(xv2.values())},
        "XV-3": {"opus5_blind_fok": L["claude-opus-5"]["FOK"]["blind"],
                 "haiku_blind_fok": L["claude-haiku-4-5-20251001"]["FOK"]["blind"],
                 "HOLDS": bool(xv3)},
        "XV-4": {"per_model": xv4, "window": [XV4_LO, XV4_HI],
                 "HOLDS": all(xv4.values())},
        "XV-5": {"reports": bool(xv1["kimi-k3"]),
                 "note": ("blind NOK at chance on kimi-k3 despite always-on reasoning"
                          if xv1["kimi-k3"] else
                          "does not report -- XV-1 failed on kimi-k3")},
    }
    R["paper_precommitment_met"] = bool(
        all(xv1[m] for m in FRONTIER) and all(xv2.values()))
    # XV-1's registered form is "every new model"; the pre-commitment says "both new
    # lineages". Both readings are recorded so the verdict cannot turn on the choice.
    R["precommitment_reading_all_three"] = bool(all(xv1.values()) and all(xv2.values()))

    # ---- cross-vendor convergence, computed so the write-up asserts nothing by hand.
    # E1 values are cited constants from NUMBERS.md section 9, not recomputed here.
    E1_REF = {"gpt-4.1-mini": {"fok": (0.4488, 0.7090), "nok": (0.5000, 0.7139),
                               "tie_degenerate_blind_nok": True},
              "gpt-5.6-luna": {"fok": (0.5735, 0.7417), "nok": (0.5585, 0.8526)},
              "gpt-5.6-sol": {"fok": (0.7099, 0.7463), "nok": (0.5290, 0.8588)}}
    conv = {}
    for j in ("fok", "nok"):
        blind = {m: R["lineages"][m][j.upper()]["blind"] for m in MODELS}
        idx = {m: R["lineages"][m][j.upper()]["indexed"] for m in MODELS}
        for m, v in E1_REF.items():
            blind[m], idx[m] = v[j][0], v[j][1]
        nondeg = [m for m in blind if not E1_REF.get(m, {}).get("tie_degenerate_blind_nok")
                  or j == "fok"]
        conv[j] = {
            "n_models": len(blind), "blind": blind, "indexed": idx,
            "blind_span": max(blind.values()) - min(blind.values()),
            "indexed_span": max(idx.values()) - min(idx.values()),
            "blind_span_nondegenerate": max(blind[m] for m in nondeg) - min(blind[m] for m in nondeg),
            "indexed_span_nondegenerate": max(idx[m] for m in nondeg) - min(idx[m] for m in nondeg),
        }
        conv[j]["tightening_ratio"] = (conv[j]["blind_span"] / conv[j]["indexed_span"]
                                       if conv[j]["indexed_span"] else None)
        conv[j]["tightening_ratio_nondegenerate"] = (
            conv[j]["blind_span_nondegenerate"] / conv[j]["indexed_span_nondegenerate"]
            if conv[j]["indexed_span_nondegenerate"] else None)
    R["convergence"] = conv

    # spend, so the write-up cites no figure the scoring did not produce
    elic = {m: R["lineages"][m]["usd"] for m in MODELS}
    prior = json.load(io.open(XV / "manifests" / "projection.json",
                              encoding="utf-8"))["spent_to_date_usd"]
    R["spend"] = {"per_lineage": elic,
                  "elicitation_total": round(sum(elic.values()), 4),
                  "prior_step0_and_pilots": round(prior, 4),
                  "grand_total": round(sum(elic.values()) + prior, 4),
                  "cap": 28.00,
                  "registered_projection": {"claude-opus-5": 5.03,
                                            "claude-haiku-4-5-20251001": 0.70,
                                            "kimi-k3": 16.29, "run_total": 22.02}}

    out = XV / "results" / "e1xv_scores.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    io.open(out, "w", encoding="utf-8").write(json.dumps(R, indent=2, ensure_ascii=False))

    # ---------------- console report
    for m in MODELS:
        d = L[m]
        print(f"\n=== {m}  ({d['n_rows']} rows, ${d['usd']}, "
              f"served {d['served_models']})")
        for arm in ARMS:
            p = d["parse"][arm]
            print(f"  parse {arm:13s} n={p['n']:4d} fail={p['parse_fail']:3d} "
                  f"({p['fail_rate'] * 100:5.1f}%) err={p['errors']:3d} "
                  f"trunc={p['truncated']:4d}  {'*** LANE FLAGGED' if p['FLAGGED'] else ''}")
        print(f"  excluded below MIN_DRAWS: {d['n_excluded']}")
        for j in ("FOK", "NOK"):
            c = d[j]
            if "note" in c:
                print(f"  {j}: {c['note']}")
                continue
            print(f"  {j}  n={c['n']:3d} pos={c['n_pos']:3d}  "
                  f"blind {c['blind']:.4f} {fmt(c['blind_ci'])}  "
                  f"indexed {c['indexed']:.4f} {fmt(c['indexed_ci'])}  "
                  f"delta {c['delta']:+.4f} {fmt(c['delta_ci'])}"
                  + ("  TIE-DEGENERATE" if c["tie_degenerate"] else ""))
            s = d[f"stability_{j.lower()}"]
            for arm in ARMS:
                if arm in s:
                    print(f"      draw-stability {arm:13s} SD mean {s[arm]['sd_mean']:.4f} "
                          f"median {s[arm]['sd_median']:.4f} max {s[arm]['sd_max']:.4f}  "
                          f"identical-across-5 {s[arm]['identical_across_5']}/{s[arm]['n_items']}")

    print("\n=== REGISTERED PREDICTIONS")
    for k, v in R["predictions"].items():
        print(f"  {k}: {json.dumps(v, default=str)}")
    print(f"\n  paper pre-commitment met: {R['paper_precommitment_met']}")
    print(f"  written: {out.relative_to(ROOT)}")


def fmt(ci):
    return f"[{ci[0]:+.4f}, {ci[1]:+.4f}]"


if __name__ == "__main__":
    main()
