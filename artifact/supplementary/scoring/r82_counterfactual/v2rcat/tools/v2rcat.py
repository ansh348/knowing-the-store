# -*- coding: utf-8 -*-
"""v2rcat.py -- ADDENDUM_V2R_CAT: does any model read the per-category tally? The increment moved within the triple.
Registration: registrations/ADDENDUM_V2R_CAT.md, registered text sha256 de2dd0ba... (the bytes above the marker), frozen at
257a090 on 2026-09-14. Descriptive: no prediction, no bar, no verdict; the two branches of its section 5 print as they come out.
run_cf's module globals are re-pointed (the contam.py / cf3_run.py recipe); run_cf, score_cf, index_v2r, cf2_leakscreen and
prompts_e1 are not edited.

Subcommands, in the registered order:
  build      locks (registration sha256; cf_indexes.json meta sha256 and sha256_v2r recomputed); for each counted-state pair the
             state's column of the pair's category row asserted b, b, b+k across PRESENT, ABSENT, PN on the recorded v2 texts;
             under seed 42 one non-PN sibling takes b+k and the PN version takes b, every other line as in v2r (the recorded
             v2r text, totals already permuted); RENDERER LOCK per version; the reference readers ($0): CR-oracle at the
             state's cell, CR-totals, the superseded-names lookup -> v2rcat/build/build_v2rcat.json, texts_v2rcat.json
  leak       the CF-2 leakage screen reproduced on the V2R-CAT texts (30 PRESENT items, the CF-2 sample rule, gpt-4.1-mini,
             leaks iff more than 3 of 30 score correct; a leak is a STOP) -> v2rcat/results/leakscreen_v2rcat.json
  probe <lane>   one call on the first item (served identifier, E1.7) and the projection against the $4 cap
  sync gpt-4.1-mini | submit claude-haiku-4-5-20251001 | poll claude-haiku-4-5-20251001
  score      after the lanes return (a later step)
"""
from __future__ import annotations

import concurrent.futures as cf
import hashlib
import io
import json
import os
import random
import sys
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[3]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "e1_metamemory/tools", "reviews/v18/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from common_e1r import auroc, boot_cluster_single  # noqa: E402
from index_features import parse  # noqa: E402
from index_v2r import counts_of  # noqa: E402
from index_v3 import named_sections  # noqa: E402
import run_cf as RC  # noqa: E402  (asserts the prompts_e1 digests at import)
import score_cf as S  # noqa: E402
import prompts_e1 as P  # noqa: E402
from cf2_leakscreen import plausible_lines, N as LEAK_N, THRESHOLD as LEAK_T, D18_BAND, SEED as LEAK_SEED, PRICE_IN, PRICE_OUT  # noqa: E402
from exp4_witnesses import supports_correct  # noqa: E402
from a1_count_readers import boot_item_single, r4  # noqa: E402

CF2 = ROOT / "r82_counterfactual" / "cf2"
V2C = ROOT / "r82_counterfactual" / "v2rcat"
BUILD, ROWS, RES = V2C / "build", V2C / "rows", V2C / "results"
REG = ROOT / "registrations" / "ADDENDUM_V2R_CAT.md"
REG_SHA = "de2dd0baaf33ccb3dcf1c2b0c10b01cc6f76f851e4057946dc03f477a584b18f"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
ARM = "INDEXED-V2R-CAT"
SEED = 42
CAP = 4.00
COL = {"RETRACTION": ("retract", slice(50, 59)), "EXPIRY": ("expired", slice(59, 68))}
STATES = ("SUPERSESSION", "RETRACTION", "EXPIRY")

CELL = json.load(io.open(CF2 / "cf_cell.json", encoding="utf-8"))["items"]
PAIRS = {p["pair_id"]: p for p in json.load(io.open(CF2 / "cf_pairs_cf2.json", encoding="utf-8"))["pairs"]}
IDXDOC = json.load(io.open(CF2 / "cf_indexes.json", encoding="utf-8"))
IDX = IDXDOC["indexes"]


def registration_ok():
    b = REG.read_bytes(); i = b.find(FROZEN_END)
    return i > 0 and hashlib.sha256(b[:i]).hexdigest() == REG_SHA


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=1, sort_keys=True, default=float); f.write("\n")


def locks_ok():
    keys = sorted(IDX)
    v23 = hashlib.sha256("\x1f".join(IDX[k]["v2"] + "\x1e" + IDX[k]["v3"] for k in keys).encode()).hexdigest()
    v2r = hashlib.sha256("\x1f".join(IDX[k]["v2r"] for k in keys).encode()).hexdigest()
    return {"registration": registration_ok(), "indexes_v2_v3": v23 == IDXDOC["meta"]["sha256"], "indexes_v2r": v2r == IDXDOC["meta"]["sha256_v2r"],
            "sha_v2_v3": v23, "sha_v2r": v2r}


def cat_row(text, cat):
    """(line index, line) of the category's row in the PER-CATEGORY BREAKDOWN; asserted exactly one."""
    lines = text.split("\n"); hits = [i for i, l in enumerate(lines) if l.startswith(f"{cat:<24s}") and l[24:32].strip().isdigit()]
    assert len(hits) == 1, (cat, hits)
    return hits[0], lines[hits[0]]


def texts_v2rcat():
    return {k.rsplit("|", 1)[0]: v for k, v in jload(BUILD / "texts_v2rcat.json").items()}


def units(arm):
    T = texts_v2rcat()
    return [{"unit_id": it["item_id"], "question": it["question"], "index": T[it["item_id"]]} for it in CELL]


def point():
    RC.CELL = CELL; RC.ARMS = (ARM,); RC.units = units; RC.ROWS = ROWS; RC.PROBES = BUILD / "probes.json"
    S.R82 = CF2


# ------------------------------------------------------------------ build
def cmd_build():
    L = locks_ok(); assert all(L[k] for k in ("registration", "indexes_v2_v3", "indexes_v2r")), f"STOP: lock failure {L}"
    by = {}
    for it in CELL:
        by.setdefault(it["pair_id"], {})[it["version"]] = it["item_id"]
    rng = np.random.default_rng(SEED)
    texts = {k: IDX[k]["v2r"] for k in IDX}          # start from the recorded v2r text
    moves, k_census = [], {"RETRACTION": {}, "EXPIRY": {}}
    for pid in sorted(by):
        st = PAIRS[pid]["state"]
        if st == "SUPERSESSION":
            continue
        cat = PAIRS[pid]["category"]; col, sl = COL[st]
        vals = {}
        for v in ("PRESENT", "ABSENT", "PN"):
            _, line = cat_row(IDX[by[pid][v]]["v2"], cat)
            vals[v] = int(line[sl].strip())
        b, k = vals["PRESENT"], vals["PN"] - vals["PRESENT"]
        assert vals["ABSENT"] == b and k >= 1, ("STOP: not b, b, b+k", pid, vals)
        k_census[st][k] = k_census[st].get(k, 0) + 1
        sib = ("PRESENT", "ABSENT")[int(rng.integers(0, 2))]
        new = {"PN": b, sib: b + k}
        for v, val in new.items():
            key = by[pid][v]; i, line = cat_row(texts[key], cat)
            assert int(line[sl].strip()) == (b + k if v == "PN" else b), ("v2r cell differs from v2 in the moved column", key)
            nl = line[:sl.start] + f"{val:>9d}" + line[sl.stop:]
            assert len(nl) == len(line)
            ls = texts[key].split("\n"); ls[i] = nl; texts[key] = "\n".join(ls)
        moves.append({"pair_id": pid, "state": st, "category": cat, "b": b, "k": k, "sibling_took_increment": sib})
    # RENDERER LOCK against v2r
    n_diff = 0
    for k_, t in texts.items():
        a, c = IDX[k_]["v2r"].split("\n"), t.split("\n")
        assert len(a) == len(c), k_
        d = [i for i, (x, y_) in enumerate(zip(a, c)) if x != y_]
        pid = next(it["pair_id"] for it in CELL if it["item_id"] == k_)
        if PAIRS[pid]["state"] == "SUPERSESSION":
            assert not d, ("supersession text changed", k_)
        else:
            assert len(d) <= 1, ("more than one line differs", k_, d)
            if d:
                i = d[0]; col, sl = COL[PAIRS[pid]["state"]]
                assert a[i][:sl.start] == c[i][:sl.start] and a[i][sl.stop:] == c[i][sl.stop:], ("a field outside the state's column differs", k_)
                n_diff += 1
        assert named_sections(t) == named_sections(IDX[k_]["v2"]), ("name sections changed", k_)
    # reference readers at build ($0)
    y = np.array([it["y_nok"] for it in CELL], int); g = np.array([it["persona"] for it in CELL]); st_ = np.array([it["state"] for it in CELL])
    def cell_reader(text_of):
        out = np.zeros(len(CELL))
        for n, it in enumerate(CELL):
            stt = it["state"]
            if stt == "SUPERSESSION":
                continue
            col, _ = COL[stt]; c = parse(text_of(it["item_id"]))["categories"][PAIRS[it["pair_id"]]["category"]]
            out[n] = float(c.get(col, 0))
        return out
    cr_new, cr_v2 = cell_reader(lambda k: texts[k]), cell_reader(lambda k: IDX[k]["v2"])
    tot_new = np.array([sum(counts_of(texts[it["item_id"]])) for it in CELL], float)
    tot_v2r = np.array([sum(counts_of(IDX[it["item_id"]]["v2r"])) for it in CELL], float)
    assert np.array_equal(tot_new, tot_v2r)
    look = S.matcher([it["question"] for it in CELL], [named_sections(texts[it["item_id"]])["superseded"] for it in CELL])
    lk = r4(auroc(look, y)); assert lk == 0.7663, ("GATE: lookup", lk)
    ref = {}
    for name, s_ in (("CR-oracle-state-cell under V2R-CAT", cr_new), ("CR-oracle-state-cell under v2", cr_v2), ("CR-totals under V2R-CAT (= v2r)", tot_new)):
        ref[name] = {"whole": r4(auroc(s_, y)), "per_state": {}}
        for stt in ("RETRACTION", "EXPIRY"):
            m = st_ == stt
            ref[name]["per_state"][stt] = {"auroc": r4(auroc(s_[m], y[m])), "item_ci": boot_item_single(s_[m], y[m]), "persona_ci": boot_cluster_single(s_[m], y[m], g[m])}
    tsha = hashlib.sha256("\x1f".join(texts[k] for k in sorted(texts)).encode()).hexdigest()
    jdump({f"{k}|{ARM}": v for k, v in texts.items()}, BUILD / "texts_v2rcat.json")
    jdump({"registration_sha256": REG_SHA, "frozen_at": "257a090", "locks": L, "seed": SEED, "construction": "within-triple: the PN version takes b, one non-PN sibling takes b+k, every other line as in v2r",
           "moves": moves, "k_census": k_census, "n_pairs_moved": len(moves), "n_texts_changed_vs_v2r": n_diff, "texts_sha256": tsha, "renderer_lock": "asserted on every version",
           "reference_readers": ref, "lookup_gate": {"got": lk, "expected": 0.7663}, "arm": ARM, "cap_usd": CAP}, BUILD / "build_v2rcat.json")
    print(f"locks {L['registration']}/{L['indexes_v2_v3']}/{L['indexes_v2r']}; {len(moves)} pairs moved (k census {k_census}); {n_diff} texts differ from v2r; texts sha256 {tsha[:16]}; lookup gate {lk}")
    for name, r in ref.items():
        print(f"  {name}: whole {r['whole']}; RET {r['per_state']['RETRACTION']['auroc']} EXP {r['per_state']['EXPIRY']['auroc']}")
    write_ledger()


# ------------------------------------------------------------------ the leakage screen, reproduced on the V2R-CAT texts
def cmd_leak():
    assert registration_ok()
    RC.load_env()
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    T = texts_v2rcat()
    gold = {p["pair_id"]: p["entry_text"] for p in PAIRS.values()}
    pool = sorted((it for it in CELL if it["version"] == "PRESENT"), key=lambda i: i["item_id"])
    sample = sorted(random.Random(LEAK_SEED).sample(pool, LEAK_N), key=lambda i: i["item_id"])
    rec_sample = jload(CF2 / "results" / "leakscreen_cf2.json")["meta"]["sample"]
    assert [it["item_id"] for it in sample] == rec_sample, "the sample differs from CF-2's"

    def one(it):
        msgs = [{"role": "system", "content": P.LEAKAGE_SYSTEM}, {"role": "user", "content": P.LEAKAGE_USER.format(index=T[it["item_id"]], question=it["question"])}]
        r = client.chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS, messages=msgs)
        text = r.choices[0].message.content or ""
        obj = RC.last_json(text); ans = "" if obj is None else str(obj.get("answer", "")).strip()
        non_unknown = bool(ans) and ans.upper() != "UNKNOWN"
        gl = gold[it["pair_id"]]; correct = non_unknown and supports_correct(ans, gl)
        return {"item_id": it["item_id"], "pair_id": it["pair_id"], "persona": it["persona"], "state": it["state"], "question": it["question"], "gold_entry_text": gl,
                "response": ans, "raw_response": text[:600], "parse_ok": obj is not None, "non_unknown": non_unknown, "correct": bool(correct),
                "served_model": r.model, "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens}
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        rows = sorted(ex.map(one, sample), key=lambda r: r["item_id"])
    n_correct = sum(r["correct"] for r in rows); leaked = n_correct > LEAK_T
    d18 = (not leaked) and n_correct >= LEAK_T - D18_BAND + 1
    if d18:
        for r in rows:
            if r["correct"] or r["non_unknown"]:
                r["d18_index_lines"] = plausible_lines(T[r["item_id"]], r["gold_entry_text"], r["response"])
    cell = {"arm": ARM, "n": LEAK_N, "n_correct": n_correct, "threshold": LEAK_T, "leaked": leaked, "verdict": "LEAKS -- STOP" if leaked else "PASS", "d18_triggered": bool(d18),
            "n_non_unknown": sum(r["non_unknown"] for r in rows), "n_parse_failures": sum(not r["parse_ok"] for r in rows),
            "usd": round(sum(r["tok_in"] for r in rows) / 1e6 * PRICE_IN + sum(r["tok_out"] for r in rows) / 1e6 * PRICE_OUT, 6), "rows": rows,
            "served_models": sorted({r["served_model"] for r in rows}), "prompts_e1_file_sha256": P.file_sha256(), "prompts_e1_texts_sha256": P.texts_sha256()}
    jdump(cell, RES / "leakscreen_v2rcat.json")
    print(f"{ARM}: {n_correct}/{LEAK_N} correct  non-UNKNOWN {cell['n_non_unknown']}  parse-fail {cell['n_parse_failures']}  {cell['verdict']}  ${cell['usd']:.4f}  served {cell['served_models']}")
    write_ledger()
    if leaked:
        raise SystemExit("STOP: the V2R-CAT arm leaks (ADDENDUM_V2R_CAT section 4)")


# ------------------------------------------------------------------ probe, lanes
def billed_so_far():
    usd = 0.0
    if (RES / "leakscreen_v2rcat.json").exists():
        usd += jload(RES / "leakscreen_v2rcat.json")["usd"]
    pr = jload(BUILD / "probes.json") if (BUILD / "probes.json").exists() else {}
    for lane, cfg in RC.LANES.items():
        p = ROWS / f"rows_{cfg['code']}.jsonl"
        if p.exists():
            usd += sum(json.loads(l).get("usd", 0.0) for l in io.open(p, encoding="utf-8"))
        elif (ROWS / f"batch_{cfg['code']}.json").exists() and lane in pr:
            usd += pr[lane]["projection"]["usd"]
    usd += sum(v.get("probe_usd", 0.0) for v in pr.values())
    return usd


def cmd_probe(lane):
    assert registration_ok(); point(); RC.load_env()
    assert (RES / "leakscreen_v2rcat.json").exists() and not jload(RES / "leakscreen_v2rcat.json")["leaked"], "STOP: run the leakage screen first"
    cfg = RC.LANES[lane]
    r = RC.call_once(lane, units(ARM)[0], ARM, 0)
    ok = lane.split("-2025")[0] in r["served_model"] or lane in r["served_model"]
    n = cfg["k"] * len(CELL)
    ratio = r["tok_in"] / max(1, len(units(ARM)[0]["index"]))
    tin = sum(int(len(u["index"]) * ratio) for u in units(ARM)) * cfg["k"]; tout = n * max(1, r["tok_out"])
    usd = (tin / 1e6 * cfg["price"][0] + tout / 1e6 * cfg["price"][1]) * cfg["mult"]
    billed = billed_so_far() + r["usd"]; headroom = CAP - billed
    rec = {"lane": lane, "served": r["served_model"], "identifier_ok": ok, "in": r["tok_in"], "out": r["tok_out"], "parsed": r["status"], "probe_usd": r["usd"],
           "projection": {"calls": n, "input_tokens": tin, "output_tokens": tout, "usd": round(usd, 4), "usd_x1.3": round(usd * 1.3, 4)},
           "billed_before": round(billed, 4), "headroom": round(headroom, 4), "fits": bool(ok and usd * 1.3 <= headroom), "sample": r["text"][:200]}
    d = jload(RC.PROBES) if RC.PROBES.exists() else {}
    d[lane] = rec; jdump(d, RC.PROBES)
    print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")
    if not rec["fits"]:
        print(f"DASH: the x1.3 projection ${usd * 1.3:.2f} exceeds the headroom ${headroom:.2f} under the ${CAP:.2f} cap")
    write_ledger()


def lane_cmd(cmd, lane):
    assert registration_ok(); point()
    pr = jload(RC.PROBES).get(lane) if RC.PROBES.exists() else None
    assert pr and pr["identifier_ok"], "STOP: probe this lane first"
    if cmd in ("sync", "submit"):
        assert pr["fits"], "STOP: the lane's x1.3 projection exceeds the headroom; it prints a dash"
    getattr(RC, "cmd_" + cmd)(lane)
    write_ledger()


# ------------------------------------------------------------------ score
def load_new(code):
    """(item_id -> mean nok over the collapse) for the V2R-CAT arm of one lane; k = 1 lanes are their single draw."""
    import collections
    per = collections.defaultdict(dict); n_bad = 0; usd = 0.0
    p = ROWS / f"rows_{code}.jsonl"
    for line in io.open(p, encoding="utf-8"):
        r = json.loads(line); usd += r.get("usd", 0.0)
        if r.get("status") == "OK" and r.get("nok") is not None and r["arm"] == ARM:
            per[r["unit_id"]][int(r["draw"])] = float(r["nok"])
        else:
            n_bad += 1
    out = {u: float(np.mean(list(d.values()))) for u, d in per.items() if len(d) >= S.MIN_DRAWS or len(d) == 1}
    return out, n_bad, usd


def cmd_score():
    assert registration_ok(); point()
    from cf2_score import paired  # noqa: E402
    TOL = 0.05
    b = jload(BUILD / "build_v2rcat.json"); ref = b["reference_readers"]
    y = np.array([it["y_nok"] for it in CELL], int); g = np.array([it["persona"] for it in CELL]); st = np.array([it["state"] for it in CELL])
    res = {"registration_sha256": REG_SHA, "frozen_at": "257a090", "n": 444, "pos": 148, "tol": TOL, "models": {}, "branch": {}, "spend": {}}
    gates = {"MINI": 0.7167, "H45": 0.7566}
    for code, lane in (("MINI", "gpt-4.1-mini"), ("H45", "claude-haiku-4-5-20251001"), ("OP5", "claude-opus-5")):
        if not (ROWS / f"rows_{code}.jsonl").exists():
            res["models"][lane] = {"status": "dash: optional lane not run" if code == "OP5" else "dash: lane not run"}; continue
        rec = S.load_lane(code)                       # the recorded CF-2 rows (S.R82 = cf2)
        v2 = np.array([rec[(it["item_id"], "INDEXED-V2")] for it in CELL], float)
        a2 = round(float(auroc(v2, y)), 4); assert a2 == gates[code], ("GATE: recorded v2 row", code, a2)
        newd, n_bad, usd = load_new(code)
        nv = np.array([newd.get(it["item_id"], np.nan) for it in CELL], float); assert not np.isnan(nv).any(), (code, "items without a score")
        M = {"n_rows_bad": n_bad, "usd": round(usd, 4), "k": RC.LANES[lane]["k"], "v2_recorded": a2, "v2rcat": round(float(auroc(nv, y)), 4),
             "minus_v2": paired(v2, nv, y, g), "per_state": {}, "vs_reference": {}}
        for s_ in STATES:
            m = st == s_
            pd = paired(v2[m], nv[m], y[m], g[m])
            inside = bool(-TOL <= pd["item_ci"]["ci_lo"] and pd["item_ci"]["ci_hi"] <= TOL and -TOL <= pd["persona_ci"]["ci_lo"] and pd["persona_ci"]["ci_hi"] <= TOL)
            beyond = bool(abs(pd["delta"]) > TOL and ((pd["item_ci"]["ci_hi"] < -TOL and pd["persona_ci"]["ci_hi"] < -TOL) or (pd["item_ci"]["ci_lo"] > TOL and pd["persona_ci"]["ci_lo"] > TOL)))
            M["per_state"][s_] = {"n": int(m.sum()), "pos": int(y[m].sum()), "v2": round(float(auroc(v2[m], y[m])), 4), "v2rcat": round(float(auroc(nv[m], y[m])), 4),
                                  **pd, "inside_band_both": inside, "beyond_band_both": beyond}
        cr = ref["CR-oracle-state-cell under V2R-CAT"]
        for s_ in ("RETRACTION", "EXPIRY"):
            M["vs_reference"][s_] = {"model": M["per_state"][s_]["v2rcat"], "CR-oracle-state-cell": cr["per_state"][s_]["auroc"], "CR-totals": ref["CR-totals under V2R-CAT (= v2r)"]["per_state"][s_]["auroc"]}
        res["models"][lane] = M; res["spend"][lane] = round(usd, 4)
    lk = jload(RES / "leakscreen_v2rcat.json"); pr = jload(BUILD / "probes.json")
    res["spend"]["leakage_screen"] = lk["usd"]; res["spend"]["probes"] = round(sum(v["probe_usd"] for v in pr.values()), 4)
    res["spend"]["total"] = round(sum(v for v in res["spend"].values()), 4); res["spend"]["cap"] = CAP
    # the section 5 branches
    verdicts = {}
    for lane, M in res["models"].items():
        if "status" in M:
            continue
        moved = [s_ for s_ in ("RETRACTION", "EXPIRY") if M["per_state"][s_]["beyond_band_both"]]
        within = all(M["per_state"][s_]["inside_band_both"] for s_ in ("RETRACTION", "EXPIRY"))
        verdicts[lane] = {"within_band_both_states": within, "moved_beyond_band": moved,
                          "reading": ("stays within 0.05 of its v2 row on both counted states (both intervals inside the band)" if within else
                                      ("reads the per-category tally on " + ", ".join(moved) if moved else "neither inside the band on both states nor beyond it with both intervals: printed as it came out"))}
    every_within = all(v["within_band_both_states"] for v in verdicts.values()) and verdicts
    any_moved = any(v["moved_beyond_band"] for v in verdicts.values())
    res["branch"] = {"per_model": verdicts, "fires": ("every model within 0.05: the tally claim stands as tested" if every_within else ("a model reads the per-category tally" if any_moved else "mixed: printed per model")),
                     "section5": ("the counted states' tallies were in view, individuated the version, and moved no model whether the totals or the per-category cells were randomized; the thesis says 'randomizing the tallies'" if every_within else
                                  "Section 5 says which model reads the per-category tally and on which state, with the number; the reader claim narrows to the models that did not move")}
    jdump(res, RES / "scores_v2rcat.json")
    for lane, M in res["models"].items():
        if "status" in M:
            print(lane, M["status"]); continue
        print(f"{lane} (k={M['k']}): v2 {M['v2_recorded']:.4f} -> V2R-CAT {M['v2rcat']:.4f}; whole minus v2 {M['minus_v2']['delta']:+.4f} item [{M['minus_v2']['item_ci']['ci_lo']:+.4f},{M['minus_v2']['item_ci']['ci_hi']:+.4f}] persona [{M['minus_v2']['persona_ci']['ci_lo']:+.4f},{M['minus_v2']['persona_ci']['ci_hi']:+.4f}]; bad rows {M['n_rows_bad']}; ${M['usd']:.4f}")
        for s_ in STATES:
            d = M["per_state"][s_]
            print(f"    {s_:12s} v2 {d['v2']:.4f} -> {d['v2rcat']:.4f}  d {d['delta']:+.4f} item [{d['item_ci']['ci_lo']:+.4f},{d['item_ci']['ci_hi']:+.4f}] persona [{d['persona_ci']['ci_lo']:+.4f},{d['persona_ci']['ci_hi']:+.4f}] inside band {d['inside_band_both']} beyond {d['beyond_band_both']}")
    print("branch:", json.dumps(res["branch"], indent=1)); print("spend:", json.dumps(res["spend"]))
    write_ledger()


# ------------------------------------------------------------------ ledger
def write_ledger():
    L = []; w = L.append
    b = jload(BUILD / "build_v2rcat.json") if (BUILD / "build_v2rcat.json").exists() else None
    lk = jload(RES / "leakscreen_v2rcat.json") if (RES / "leakscreen_v2rcat.json").exists() else None
    pr = jload(BUILD / "probes.json") if (BUILD / "probes.json").exists() else {}
    w("# NUMBERS_V2RCAT.md: ADDENDUM_V2R_CAT, the increment moved within the triple")
    w("")
    w(f"Registration `registrations/ADDENDUM_V2R_CAT.md`, registered text sha256 `{REG_SHA}` (the bytes above the marker line), frozen at `257a090` on 2026-09-14. Descriptive: no prediction, no bar, no verdict. Every number for this addendum enters the manuscript through a key in this file and no other way. Written by `r82_counterfactual/v2rcat/tools/v2rcat.py`; sections 1 to 3 before the first model call on the arm.")
    w("")
    if b:
        w("## 1. AUX-V2RCAT-LOCK: the construction")
        w("")
        kc = b["k_census"]
        w(f"Locks: registration {b['locks']['registration']}; `cf_indexes.json` meta sha256 (v2 + v3) and sha256_v2r recomputed and equal ({b['locks']['indexes_v2_v3']}, {b['locks']['indexes_v2r']}). Start text: the recorded v2r of every store version (totals permuted). For each of the {b['n_pairs_moved']} counted-state pairs the state's column of the pair's category row reads b, b, b+k across PRESENT, ABSENT and PN on the recorded v2 texts (asserted; k census: retraction {json.dumps({str(k): v for k, v in sorted(kc['RETRACTION'].items())})}, expiry {json.dumps({str(k): v for k, v in sorted(kc['EXPIRY'].items())})}); under seed {b['seed']} one non-PN sibling takes b+k and the PN version takes b (the sibling per pair is recorded in `build/build_v2rcat.json` moves). RENDERER LOCK asserted on every version: {b['n_texts_changed_vs_v2r']} texts differ from their v2r on exactly one line, the category row, and on that line only in the state's column; every supersession text is byte-identical to its v2r; every name section equals its v2's. Texts sha256 `{b['texts_sha256'][:16]}...`; the superseded-names lookup on the texts reproduces the recorded {b['lookup_gate']['expected']} (got {b['lookup_gate']['got']}).")
        w("")
        w("## 2. AUX-V2RCAT-REF: the reference readers ($0; within the state's own items, the CF-2 convention)")
        w("")
        w("| reader | whole | retraction | item 95% | persona 95% | expiry | item 95% | persona 95% |")
        w("|---|---:|---:|---|---|---:|---|---|")
        for name, r in b["reference_readers"].items():
            R, E = r["per_state"]["RETRACTION"], r["per_state"]["EXPIRY"]
            w(f"| {name} | {r['whole']:.4f} | {R['auroc']:.4f} | [{R['item_ci']['ci_lo']:.4f}, {R['item_ci']['ci_hi']:.4f}] | [{R['persona_ci']['ci_lo']:.4f}, {R['persona_ci']['ci_hi']:.4f}] | {E['auroc']:.4f} | [{E['item_ci']['ci_lo']:.4f}, {E['item_ci']['ci_hi']:.4f}] | [{E['persona_ci']['ci_lo']:.4f}, {E['persona_ci']['ci_hi']:.4f}] |")
        w("")
    if lk:
        w("## 3. AUX-V2RCAT-LEAK: the CF-2 leakage screen on the V2R-CAT texts")
        w("")
        w(f"{lk['n_correct']} of {lk['n']} PRESENT items score correct (leaks iff more than {lk['threshold']}): **{lk['verdict']}**; non-UNKNOWN {lk['n_non_unknown']}, parse failures {lk['n_parse_failures']}; served {lk['served_models']}; ${lk['usd']:.4f}. The same 30-item sample as CF-2's screen (asserted).")
        w("")
    if pr:
        w("## 4. AUX-V2RCAT-PROBE and AUX-V2RCAT-PROJECTION (E1.7 rule; printed before submission)")
        w("")
        w("| lane | served | identifier ok | probe in / out | calls | projected $ | x1.3 | billed before | headroom | fits |")
        w("|---|---|---|---|---:|---:|---:|---:|---:|---|")
        for lane, p in pr.items():
            w(f"| {lane} | `{p['served']}` | {p['identifier_ok']} | {p['in']} / {p['out']} | {p['projection']['calls']} | {p['projection']['usd']:.4f} | {p['projection']['usd_x1.3']:.4f} | {p['billed_before']:.4f} | {p['headroom']:.4f} | {p['fits']} |")
        w("")
    subs = []
    for lane, cfg in RC.LANES.items():
        bp = ROWS / f"batch_{cfg['code']}.json"; rp = ROWS / f"rows_{cfg['code']}.jsonl"
        if bp.exists():
            m = jload(bp); subs.append(f"{lane}: Batch `{m['id']}`, {m['n']} requests")
        elif rp.exists():
            n = sum(1 for _ in io.open(rp, encoding="utf-8")); subs.append(f"{lane}: {n} synchronous rows in `rows_{cfg['code']}.jsonl`")
    if subs:
        w("## 5. AUX-V2RCAT-SUBMISSION")
        w("")
        w("; ".join(subs) + f". Cap ${CAP:.2f}; committed so far ${billed_so_far():.4f}. AUX-V2RCAT-MINI, -H45, -BRANCH and -SPEND fill at `score`.")
        w("")
    sc = jload(RES / "scores_v2rcat.json") if (RES / "scores_v2rcat.json").exists() else None
    if sc:
        w("## 6. AUX-V2RCAT-MINI, AUX-V2RCAT-H45, AUX-V2RCAT-OP5: the readers under V2R-CAT against their recorded v2 rows (paired; both intervals; band 0.05)")
        w("")
        w("| reader | k | v2 (recorded) | V2R-CAT | whole minus v2 (item; persona) | SUP v2 -> V2R-CAT, delta | RET v2 -> V2R-CAT, delta (item; persona), inside band | EXP v2 -> V2R-CAT, delta (item; persona), inside band | bad rows | $ |")
        w("|---|---:|---:|---:|---|---|---|---|---:|---:|")
        for lane, M in sc["models"].items():
            if "status" in M:
                w(f"| {lane} | | | {M['status']} | | | | | | |"); continue
            ps = M["per_state"]; mv = M["minus_v2"]
            def cell(s_):
                d = ps[s_]
                return f"{d['v2']:.4f} -> {d['v2rcat']:.4f}, {d['delta']:+.4f} ([{d['item_ci']['ci_lo']:+.4f}, {d['item_ci']['ci_hi']:+.4f}]; [{d['persona_ci']['ci_lo']:+.4f}, {d['persona_ci']['ci_hi']:+.4f}]), {'inside' if d['inside_band_both'] else ('beyond' if d['beyond_band_both'] else 'neither')}"
            w(f"| {lane} | {M['k']} | {M['v2_recorded']:.4f} | **{M['v2rcat']:.4f}** | {mv['delta']:+.4f} ([{mv['item_ci']['ci_lo']:+.4f}, {mv['item_ci']['ci_hi']:+.4f}]; [{mv['persona_ci']['ci_lo']:+.4f}, {mv['persona_ci']['ci_hi']:+.4f}]) | {ps['SUPERSESSION']['v2']:.4f} -> {ps['SUPERSESSION']['v2rcat']:.4f}, {ps['SUPERSESSION']['delta']:+.4f} | {cell('RETRACTION')} | {cell('EXPIRY')} | {M['n_rows_bad']} | {M['usd']:.4f} |")
        w("")
        w("The reference readers under the same text (AUX-V2RCAT-REF): the state-cell reader retraction %.4f / expiry %.4f; CR-totals %.4f / %.4f." % (
            sc["models"][next(l for l in sc["models"] if "status" not in sc["models"][l])]["vs_reference"]["RETRACTION"]["CR-oracle-state-cell"],
            sc["models"][next(l for l in sc["models"] if "status" not in sc["models"][l])]["vs_reference"]["EXPIRY"]["CR-oracle-state-cell"],
            sc["models"][next(l for l in sc["models"] if "status" not in sc["models"][l])]["vs_reference"]["RETRACTION"]["CR-totals"],
            sc["models"][next(l for l in sc["models"] if "status" not in sc["models"][l])]["vs_reference"]["EXPIRY"]["CR-totals"]))
        w("")
        br = sc["branch"]
        w(f"### AUX-V2RCAT-BRANCH: **{br['fires']}**. " + "; ".join(f"{l}: {v['reading']}" for l, v in br["per_model"].items()) + f". Section 5: {br['section5']}.")
        w("")
        # the post-hoc direction reading (the author's ruling of 2026-09-15; NOT registered; labelled as such)
        ref = b["reference_readers"]["CR-oracle-state-cell under V2R-CAT"]["per_state"] if b else None
        parts = []
        for lane, M in sc["models"].items():
            if "status" in M:
                continue
            for s_ in ("RETRACTION", "EXPIRY"):
                d = M["per_state"][s_]
                parts.append(f"{lane} on {s_.lower()} {d['delta']:+.4f} ({'up' if d['delta'] > 0 else 'down'}; item [{d['item_ci']['ci_lo']:+.4f}, {d['item_ci']['ci_hi']:+.4f}], persona [{d['persona_ci']['ci_lo']:+.4f}, {d['persona_ci']['ci_hi']:+.4f}]; "
                             f"the reader of the moved cell {ref[s_]['auroc']:.4f})")
        w("### AUX-V2RCAT-POSTHOC: the direction reading (POST HOC; the author's ruling of 2026-09-15; not a registered branch)")
        w("")
        w("A reader that follows the moved tally falls below 0.50 on that state (the state-cell reader: retraction %.4f, expiry %.4f). Every model's move is read against that direction: %s. GPT-4.1 mini's +0.0611 on expiry is upward with both intervals including zero, so no model followed the tally. Section 5 reports the registered branch as it fired (AUX-V2RCAT-BRANCH) and then this reading, labelled post hoc; the thesis sentence says 'no model follows the tallies', carrying the totals run (AUX-CF2-EQUIV-V2R) and this run with their numbers." % (ref["RETRACTION"]["auroc"], ref["EXPIRY"]["auroc"], "; ".join(parts)))
        w("")
        w(f"### AUX-V2RCAT-SPEND: {json.dumps(sc['spend'])}")
        w("")
    io.open(V2C / "NUMBERS_V2RCAT.md", "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        cmd_build()
    elif cmd == "leak":
        cmd_leak()
    elif cmd == "probe":
        cmd_probe(sys.argv[2])
    elif cmd in ("sync", "submit", "poll"):
        lane_cmd(cmd, sys.argv[2])
    elif cmd == "score":
        cmd_score()
    elif cmd == "ledger":
        write_ledger()
    else:
        raise SystemExit("usage: v2rcat.py build | leak | probe <lane> | sync gpt-4.1-mini | submit <lane> | poll <lane>")
