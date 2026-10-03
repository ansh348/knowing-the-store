"""contam.py -- ADDENDUM_PAD Amendment 1 (2026-09-14, author-instructed): the contaminated lists on the 444.

The nb6 sweep's contamination lists (sweep_common.inject: negatives' own scrubbed names injected into
the v2 summary they read, store-faithful, seed 42) at target rates 0.232 and 0.40, rendered into the
committed v2 texts of the CF-2 cell (the superseded section re-rendered under the lifted cap, the
text above the header byte-identical), scored by both lookups and by gpt-4.1-mini (k = 1) and Haiku
4.5 (k = 5, Batch) under the CF-2 lane protocols (run_cf, called), paired against the recorded CF-2
INDEXED-V2 rows. Descriptive: no prediction, no bar, no verdict.

Subcommands, in order:
  build                  lists, gate against nb6_sweep/results/step2_contamination.json (four decimals or
                         STOP), rendered texts, renderer lock (444 / 444 or STOP) -> pad_probe/build/contam_*.json
  probe <lane>           one call per arm on the first unit; served identifier (E1.7); projection against
                         the combined headroom -> pad_probe/build/contam_probes.json
  sync gpt-4.1-mini      the mini lane, synchronous, jsonl resume -> pad_probe/rows/rows_MINI.jsonl
  submit / poll claude-haiku-4-5-20251001     the Haiku lane as one Batch -> pad_probe/rows/rows_H45.jsonl
  score                  AUROC whole and per state, paired differences vs the recorded rows, model minus
                         lookup on the same lists -> pad_probe/results/contam_scores.json
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pad_common as PC  # noqa: E402
from pad_common import PAD, jdump, jload  # noqa: E402
from sweep_common import (SEED, auroc, boot_cluster, boot_item, emb_cached, inject, lex_cached, load_cf2,  # noqa: E402
                          state_mask)

sys.path.insert(0, str(PC.ROOT / "r82_counterfactual" / "tools"))
import run_cf as RC  # noqa: E402  (asserts the prompts_e1 digests at import)
import score_cf as S  # noqa: E402

CF2 = PC.ROOT / "r82_counterfactual" / "cf2"
BUILD, ROWS, RES = PAD / "build", PAD / "rows", PAD / "results"
RATES = (0.232, 0.40)
ARMS = ("INDEXED-V2-C0.232", "INDEXED-V2-C0.40")
ARM_RATE = dict(zip(ARMS, RATES))
COMBINED_CAP = 15.00
STATES = ("superseded", "retracted", "expired")
SWEEP = jload(PC.ROOT / "nb6_sweep" / "results" / "step2_contamination.json")["cells"]["cf2"]

# re-point run_cf to this amendment's cell: the same 444 items, the contaminated v2 texts, rows here
_CELL = jload(CF2 / "cf_cell.json")["items"]
RC.CELL = _CELL
RC.ROWS = ROWS
RC.PROBES = BUILD / "contam_probes.json"
RC.ARMS = ARMS
S.R82 = CF2                         # load_lane reads the RECORDED rows from cf2/rows


def _texts():
    d = jload(BUILD / "contam_texts.json")
    return {(k.rsplit("|", 1)[0], k.rsplit("|", 1)[1]): v for k, v in d.items()}


def units(arm):
    T = _texts()
    return [{"unit_id": it["item_id"], "question": it["question"], "index": T[(it["item_id"], arm)]} for it in _CELL]


RC.units = units


# ------------------------------------------------------------------ build
def cmd_build():
    assert PC.registration_ok(), "STOP: registration sha256 mismatch"
    rows = load_cf2()
    assert len(rows) == 444 and sum(r["y"] for r in rows) == 148
    idx = jload(CF2 / "cf_indexes.json")["indexes"]
    base = {r["key"]: list(r["base"]) for r in rows}
    y = np.array([r["y"] for r in rows], int)
    # renderer lock on the committed names alone
    bad = [r["key"] for r in rows if PC.padded_text(idx[r["key"]]["v2"], base[r["key"]]) != idx[r["key"]]["v2"]]
    print(f"renderer lock: {444 - len(bad)} of 444" + (f"  BAD {bad[:3]}" if bad else ""))
    if bad:
        raise SystemExit("STOP: renderer lock failed")
    out, texts, gate_ok = {}, {}, True
    for rate, arm in zip(RATES, ARMS):
        lists, meta = inject(rows, base, rate, SEED)
        e, l = emb_cached(rows, lists), lex_cached(rows, lists)
        got = {"emb": float(auroc(e, y)), "emb_sup": float(auroc(e[state_mask(rows, "superseded")], y[state_mask(rows, "superseded")])),
               "lex": float(auroc(l, y)), "lex_sup": float(auroc(l[state_mask(rows, "superseded")], y[state_mask(rows, "superseded")]))}
        ref = SWEEP[f"rate_{rate}" if rate != 0.40 else "rate_0.4"]
        want = {"emb": ref["emb"]["auroc"], "emb_sup": ref["emb"]["auroc_superseded"], "lex": ref["lex"]["auroc"], "lex_sup": ref["lex"]["auroc_superseded"]}
        ok = all(round(got[k], 4) == round(want[k], 4) for k in want)
        gate_ok &= ok
        print(f"rate {rate}: injected {meta['n_injected']} achieved {meta['achieved_rate']:.4f}; emb {got['emb']:.4f} (sweep {want['emb']:.4f}) sup {got['emb_sup']:.4f} "
              f"(sweep {want['emb_sup']:.4f}); lex {got['lex']:.4f} (sweep {want['lex']:.4f}) sup {got['lex_sup']:.4f} (sweep {want['lex_sup']:.4f})  {'PASS' if ok else 'FAIL'}")
        for r in rows:
            t = PC.padded_text(idx[r["key"]]["v2"], lists[r["key"]])
            got_names = PC.committed_names(t)
            assert sorted(got_names) == sorted(set(lists[r["key"]])), r["key"]
            assert not any(":" in n for n in lists[r["key"]]) and len(lists[r["key"]]) == len(set(lists[r["key"]]))
            texts[f"{r['key']}|{arm}"] = t
        out[arm] = {"rate": rate, "injection": meta, "gate": {"got": got, "sweep": want, "ok": ok},
                    "lists": {k: v for k, v in lists.items()},
                    "census": {"mean_len": float(np.mean([len(lists[r["key"]]) for r in rows])),
                               "neg_own_named": int(sum(1 for r in rows if r["y"] == 0 and set(r["own"]) & set(lists[r["key"]]))),
                               "pos_own_named": int(sum(1 for r in rows if r["y"] == 1 and set(r["own"]) & set(lists[r["key"]])))},
                    "scores": {"emb": e.tolist(), "lex": l.tolist()}}
    if not gate_ok:
        raise SystemExit("STOP: the regenerated lists do not reproduce the sweep at four decimals")
    eb, lb = emb_cached(rows, base), lex_cached(rows, base)
    jdump({"registration_sha256": PC.REG_SHA, "n": 444, "renderer_lock_ok": 444, "arms": out,
           "base": {"emb": float(auroc(eb, y)), "lex": float(auroc(lb, y)), "scores": {"emb": eb.tolist(), "lex": lb.tolist()}},
           "rows": [{k: r[k] for k in ("item_id", "persona", "question", "y", "state", "label", "version", "pair_id", "key", "base", "own")} for r in rows]},
          BUILD / "contam_build.json")
    jdump(texts, BUILD / "contam_texts.json")
    print(f"wrote {BUILD / 'contam_build.json'}, {BUILD / 'contam_texts.json'}")


# ------------------------------------------------------------------ probe and projection
def cmd_probe(lane):
    RC.load_env()
    cfg = RC.LANES[lane]
    rows = [RC.call_once(lane, units(arm)[0], arm, 0) for arm in ARMS]
    ok = all(lane.split("-2025")[0] in r["served_model"] or lane in r["served_model"] for r in rows)
    n = cfg["k"] * len(ARMS) * len(_CELL)
    tin = cfg["k"] * len(_CELL) * sum(r["tok_in"] for r in rows)
    tout = n * max(1, sum(r["tok_out"] for r in rows) / len(rows))
    usd = (tin / 1e6 * cfg["price"][0] + tout / 1e6 * cfg["price"][1]) * cfg["mult"]
    rec = {"lane": lane, "served": [r["served_model"] for r in rows], "identifier_ok": ok, "in": [r["tok_in"] for r in rows],
           "out": [r["tok_out"] for r in rows], "parsed": [r["status"] for r in rows], "probe_usd": sum(r["usd"] for r in rows),
           "projection": {"calls": n, "input_tokens": tin, "output_tokens": tout, "usd": round(usd, 4), "usd_x1.3": round(usd * 1.3, 4)},
           "sample": rows[0]["text"][:200]}
    d = jload(RC.PROBES) if RC.PROBES.exists() else {}
    d[lane] = rec
    jdump(d, RC.PROBES)
    print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")


# ------------------------------------------------------------------ scoring
def load_new(code):
    """(unit_id, arm) -> mean nok on this amendment's rows (X4 collapse, as score_cf.load_lane)."""
    path = ROWS / f"rows_{code}.jsonl"
    if not path.exists():
        return None
    import collections
    per = collections.defaultdict(dict)
    n_bad = 0
    for line in io.open(path, encoding="utf-8"):
        r = json.loads(line)
        if r.get("status") != "OK":
            n_bad += 1
            continue
        per[(r["unit_id"], r["arm"])][r["draw"]] = r
    out = {}
    for k, draws in per.items():
        rs = list(draws.values())
        if len(rs) < S.MIN_DRAWS and len(rs) != 1:
            continue
        noks = [x["nok"] for x in rs if x["nok"] is not None]
        if noks:
            out[k] = float(np.mean(noks))
    return out, n_bad


def paired(base, new, y, g):
    it, cl = boot_item(base, new, y), boot_cluster(base, new, y, g)
    d = float(auroc(new, y) - auroc(base, y))
    wide = it if (it.get("ci_hi", 0) - it.get("ci_lo", 0)) >= (cl.get("ci_hi", 0) - cl.get("ci_lo", 0)) else cl
    return {"delta": d, "ci_item": it, "ci_persona": cl, "both_exclude_zero": bool(it.get("excludes_zero") and cl.get("excludes_zero")),
            "weaker": {"which": "item" if wide is it else "persona", "ci_lo": wide.get("ci_lo"), "ci_hi": wide.get("ci_hi"), "excludes_zero": wide.get("excludes_zero")}}


def cmd_score():
    B = jload(BUILD / "contam_build.json")
    rows = B["rows"]
    for r in rows:
        r["pop"] = "cf2"                      # state_mask's convention switch
    y = np.array([r["y"] for r in rows], int)
    g = np.array([r["persona"] for r in rows])
    res = {"registration_sha256": PC.REG_SHA, "n": 444, "readers": {}}
    lookups = {"emb": {"base": np.array(B["base"]["scores"]["emb"], float)}, "lex": {"base": np.array(B["base"]["scores"]["lex"], float)}}
    for arm in ARMS:
        lookups["emb"][arm] = np.array(B["arms"][arm]["scores"]["emb"], float)
        lookups["lex"][arm] = np.array(B["arms"][arm]["scores"]["lex"], float)
    models = {}
    for code in ("MINI", "H45"):
        rec = S.load_lane(code)                 # the RECORDED CF-2 rows
        new = load_new(code)
        if rec is None or new is None:
            res["readers"][code] = {"status": "lane not run" if new is None else "recorded rows missing"}
            continue
        newd, n_bad = new
        base = np.array([rec.get((r["item_id"], "INDEXED-V2"), np.nan) for r in rows], float)
        models[code] = {"base": base, "n_bad_rows": n_bad}
        for arm in ARMS:
            models[code][arm] = np.array([newd.get((r["item_id"], arm), np.nan) for r in rows], float)
    for name, Sx in list(lookups.items()) + list(models.items()):
        R = {}
        base = Sx["base"]
        for lab in ("base",) + ARMS:
            arr = Sx[lab]
            ok = ~np.isnan(base) & ~np.isnan(arr)
            rec = {"n_scored": int(ok.sum()), "auroc": float(auroc(arr[ok], y[ok]))}
            for st in STATES:
                m = state_mask(rows, st) & ok
                rec[f"auroc_{st}"] = float(auroc(arr[m], y[m]))
            if lab != "base":
                rec["paired_vs_recorded"] = paired(base[ok], arr[ok], y[ok], g[ok])
                for st in STATES:
                    m = state_mask(rows, st) & ok
                    rec[f"paired_vs_recorded_{st}"] = paired(base[m], arr[m], y[m], g[m])
                if name in models:
                    for lk in ("emb", "lex"):
                        rec[f"model_minus_{lk}"] = paired(lookups[lk][lab][ok], arr[ok], y[ok], g[ok])
            R[lab] = rec
        if name in models:
            R["n_bad_rows"] = Sx["n_bad_rows"]
        res["readers"][name] = R
        print(f"\n{name}: recorded/base {R['base']['auroc']:.4f}  " + "  ".join(f"{arm[-6:]} {R[arm]['auroc']:.4f} (d {R[arm]['paired_vs_recorded']['delta']:+.4f} weaker "
              f"[{R[arm]['paired_vs_recorded']['weaker']['ci_lo']:+.4f},{R[arm]['paired_vs_recorded']['weaker']['ci_hi']:+.4f}])" for arm in ARMS))
        for st in STATES:
            print(f"   {st:10s} base {R['base'][f'auroc_{st}']:.4f}  " + "  ".join(f"{arm[-6:]} {R[arm][f'auroc_{st}']:.4f} (d {R[arm][f'paired_vs_recorded_{st}']['delta']:+.4f})" for arm in ARMS))
        if name in models:
            for arm in ARMS:
                print(f"   {arm}: model - emb {R[arm]['model_minus_emb']['delta']:+.4f} weaker [{R[arm]['model_minus_emb']['weaker']['ci_lo']:+.4f},{R[arm]['model_minus_emb']['weaker']['ci_hi']:+.4f}]; "
                      f"model - lex {R[arm]['model_minus_lex']['delta']:+.4f} weaker [{R[arm]['model_minus_lex']['weaker']['ci_lo']:+.4f},{R[arm]['model_minus_lex']['weaker']['ci_hi']:+.4f}]")
    jdump(res, RES / "contam_scores.json")
    print(f"\nwrote {RES / 'contam_scores.json'}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        cmd_build()
    elif cmd == "probe":
        cmd_probe(sys.argv[2])
    elif cmd == "score":
        cmd_score()
    else:
        getattr(RC, "cmd_" + cmd)(sys.argv[2])
