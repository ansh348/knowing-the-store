# -*- coding: utf-8 -*-
"""enc_lookup.py -- R122 T1: the name lookup under two further sentence encoders, and the random-token control. OFFLINE, no API call.

The lookup code is the committed one, unchanged: score_cf.matcher (max cosine of the question against the names of a list, names with
underscores replaced by spaces) on the 444 (v2 superseded-names list; v3 all-states list), and run_nb6.emb_scores on the 661 (the
committed NB-6 row, the superseded section of the TRUE index as run_nb6.build joins it, the empty-section marker included as the
committed function includes it; the marker-free form beside). Only the encoder object behind those functions is swapped
(score_cf._ENC["m"] and run_baselines._ENC["m"]); no query instruction or prefix is added for any encoder.

Gate at start (MiniLM-L6-v2, the recorded encoder): v2 0.7663, v3 0.8756, 661 committed 0.7484, 661 marker-free 0.7442, at four decimals.

Subcommands:  check          gates only (no encoder beyond MiniLM; nothing written)
              run            every encoder and the random-token control -> results/enc_lookup.json, ledger section
"""
from __future__ import annotations

import hashlib
import sys
import time

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r122_common as C  # noqa: E402
from common_e1r import POPULATIONS, auroc, boot_cluster_single, load_e1  # noqa: E402
from index_v3 import named_sections  # noqa: E402
import score_cf as S  # noqa: E402
import run_baselines as RB  # noqa: E402
from run_nb6 import build as nb6_build, emb_scores  # noqa: E402
from cf2_score import paired  # noqa: E402

REG = "ADDENDUM_R122_ENCODERS.md"
MINILM = "sentence-transformers/all-MiniLM-L6-v2"
ENCODERS = [("MPNET", "sentence-transformers/all-mpnet-base-v2"), ("BGE", "BAAI/bge-small-en-v1.5")]
FALLBACKS = [("E5S", "intfloat/e5-small-v2"), ("L12", "sentence-transformers/all-MiniLM-L12-v2")]
STATES = ("SUPERSESSION", "RETRACTION", "EXPIRY")
MARKER = "(none)"
TOKEN_SEED = 42


def boot_item_single(s, y, n=1000, seed=42):
    """Item-level bootstrap for a single-arm AUROC (the committed item draw scheme; single-class draws discarded)."""
    rng = np.random.default_rng(seed); s, y = np.asarray(s, float), np.asarray(y, int); d = []
    for _ in range(n):
        k = rng.integers(0, len(y), len(y))
        if y[k].sum() in (0, len(k)):
            continue
        d.append(auroc(s[k], y[k]))
    d = np.asarray(d)
    return {"n_draws": int(len(d)), "mean": float(d.mean()), "ci_lo": float(np.percentile(d, 2.5)), "ci_hi": float(np.percentile(d, 97.5))}


def set_encoder(model_id):
    from sentence_transformers import SentenceTransformer
    enc = SentenceTransformer(model_id, device="cpu")
    S._ENC["m"] = enc; RB._ENC["m"] = enc
    return enc


def random_token(name):
    """A stable pseudo-word per distinct attribute name: eight lowercase letters from a generator seeded by sha256(name) and TOKEN_SEED."""
    h = int(hashlib.sha256(f"{TOKEN_SEED}|{name}".encode("utf-8")).hexdigest()[:16], 16)
    rng = np.random.default_rng(h)
    return "".join(chr(97 + int(c)) for c in rng.integers(0, 26, 8))


# ------------------------------------------------------------------ populations
def pop_444():
    items, idx = C.cf2_cell()
    qs = [it["question"] for it in items]
    y = np.array([it["y_nok"] for it in items], int); g = np.array([it["persona"] for it in items]); st = np.array([it["state"] for it in items])
    v2 = [named_sections(idx[it["item_id"]]["v2"])["superseded"] for it in items]
    s3 = [named_sections(idx[it["item_id"]]["v3"]) for it in items]
    v3 = [s["superseded"] + s["retracted"] + s["expired"] for s in s3]
    return {"questions": qs, "y": y, "g": g, "state": st, "lists": {"v2": v2, "v3": v3}}


def pop_661():
    items, blind, idxT, idxB = load_e1()
    src = [it for it in items if POPULATIONS["R-NOK-FRB"]["filt"](it)]
    rows = nb6_build(src, blind, idxT, "nok", "TRUE")
    assert len(rows) == 661 and sum(r["y"] for r in rows) == 104
    return rows


def score_444(P, lists):
    return np.asarray(S.matcher(P["questions"], lists), float)


def score_661(rows, field="sup"):
    return np.asarray(emb_scores(rows, field), float)


def gates():
    set_encoder(MINILM)
    P = pop_444(); R = pop_661()
    got = {"v2": C.r4(auroc(score_444(P, P["lists"]["v2"]), P["y"])), "v3": C.r4(auroc(score_444(P, P["lists"]["v3"]), P["y"])),
           "661": C.r4(auroc(score_661(R, "sup"), np.array([r["y"] for r in R])))}
    for r in R:
        r["sup_clean"] = [n for n in r["sup"] if n.strip() != MARKER]
    got["661_clean"] = C.r4(auroc(score_661(R, "sup_clean"), np.array([r["y"] for r in R])))
    want = {"v2": C.LOOKUP_V2_GATE, "v3": C.LOOKUP_V3_GATE, "661": C.LOOKUP_661_GATE, "661_clean": C.LOOKUP_661_CLEAN}
    ok = all(got[k] == want[k] for k in want)
    print("gates", got, "PASS" if ok else "FAIL")
    assert ok, ("GATE MISMATCH -- STOP", got, want)
    return P, R, got


# ------------------------------------------------------------------ scoring
def block_444(P, v, base, tag):
    y, g, st = P["y"], P["g"], P["state"]
    out = {"whole": C.r4(auroc(v, y)), "ci_item": boot_item_single(v, y), "ci_persona": boot_cluster_single(v, y, g),
           "vs_minilm": paired(base, v, y, g), "minilm": C.r4(auroc(base, y)), "distinct_values": int(len(np.unique(np.round(v, 6)))),
           "per_state": {s: {"n": int((st == s).sum()), "auroc": C.r4(auroc(v[st == s], y[st == s])), "minilm": C.r4(auroc(base[st == s], y[st == s])),
                             "vs_minilm": paired(base[st == s], v[st == s], y[st == s], g[st == s])} for s in STATES}}
    out["within_tol_point"] = bool(abs(out["whole"] - out["minilm"]) <= C.TOL)
    return out


def block_661(R, v, base):
    y = np.array([r["y"] for r in R], int); g = np.array([r["persona"] for r in R])
    return {"whole": C.r4(auroc(v, y)), "ci_item": boot_item_single(v, y), "ci_persona": boot_cluster_single(v, y, g), "vs_minilm": paired(base, v, y, g),
            "minilm": C.r4(auroc(base, y)), "distinct_values": int(len(np.unique(np.round(v, 6))))}


def run():
    sha = C.assert_frozen(REG)
    P, R, got = gates()
    base = {"v2": score_444(P, P["lists"]["v2"]), "v3": score_444(P, P["lists"]["v3"]), "661": score_661(R, "sup"), "661_clean": score_661(R, "sup_clean")}
    # the random-token lists (stable per distinct name; the same token for the same name everywhere)
    names = sorted({n for k in ("v2", "v3") for lst in P["lists"][k] for n in lst} | {n for r in R for n in r["sup"]})
    tok = {n: random_token(n) for n in names}
    assert len(set(tok.values())) == len(tok), "token collision"
    tok_lists = {"v2": [[tok[n] for n in lst] for lst in P["lists"]["v2"]], "v3": [[tok[n] for n in lst] for lst in P["lists"]["v3"]]}
    for r in R:
        r["sup_tok"] = [tok[n] for n in r["sup"]]; r["sup_clean_tok"] = [tok[n] for n in r["sup_clean"]]
    res = {"meta": {"registration": REG, "registration_sha256": sha, "gates": got, "minilm": MINILM, "tolerance": C.TOL, "token_seed": TOKEN_SEED,
                    "n_distinct_names": len(names), "lookup_code": "score_cf.matcher (444) / run_nb6.emb_scores (661), the encoder object swapped, no prefix",
                    "when": time.strftime("%Y-%m-%dT%H:%M:%S")}, "encoders": {}, "random_token": {}, "loaded": [], "not_loaded": []}
    # MiniLM's own rows in the same block shape (the recorded rows, reproduced) so the table prints them beside
    res["encoders"]["MINILM"] = {"model": MINILM, "v2": block_444(P, base["v2"], base["v2"], "v2"), "v3": block_444(P, base["v3"], base["v3"], "v3"),
                                 "661": block_661(R, base["661"], base["661"]), "661_clean": block_661(R, base["661_clean"], base["661_clean"])}
    res["random_token"]["MINILM"] = {"v2": block_444(P, score_444(P, tok_lists["v2"]), base["v2"], "v2"), "v3": block_444(P, score_444(P, tok_lists["v3"]), base["v3"], "v3"),
                                     "661": block_661(R, score_661(R, "sup_tok"), base["661"]), "661_clean": block_661(R, score_661(R, "sup_clean_tok"), base["661_clean"])}
    queue = list(ENCODERS); fallbacks = list(FALLBACKS)
    while queue:
        code, model = queue.pop(0)
        try:
            set_encoder(model)
            t0 = time.time()
            v2 = score_444(P, P["lists"]["v2"]); v3 = score_444(P, P["lists"]["v3"]); s661 = score_661(R, "sup"); s661c = score_661(R, "sup_clean")
            res["encoders"][code] = {"model": model, "v2": block_444(P, v2, base["v2"], "v2"), "v3": block_444(P, v3, base["v3"], "v3"),
                                     "661": block_661(R, s661, base["661"]), "661_clean": block_661(R, s661c, base["661_clean"]), "seconds": round(time.time() - t0, 1)}
            res["random_token"][code] = {"v2": block_444(P, score_444(P, tok_lists["v2"]), base["v2"], "v2"), "v3": block_444(P, score_444(P, tok_lists["v3"]), base["v3"], "v3"),
                                         "661": block_661(R, score_661(R, "sup_tok"), base["661"]), "661_clean": block_661(R, score_661(R, "sup_clean_tok"), base["661_clean"])}
            res["loaded"].append({"code": code, "model": model})
            print(f"{code} {model}: v2 {res['encoders'][code]['v2']['whole']} v3 {res['encoders'][code]['v3']['whole']} 661 {res['encoders'][code]['661']['whole']}")
        except Exception as e:  # noqa: BLE001  -- the registered fallback rule: take the next of the fixed list and record it
            res["not_loaded"].append({"code": code, "model": model, "error": f"{type(e).__name__}: {str(e)[:300]}"})
            print(f"{code} {model}: NOT LOADED ({type(e).__name__}); taking the next of the fixed list")
            if fallbacks:
                queue.append(fallbacks.pop(0))
    # P-E1: both registered encoders (or their recorded substitutes) within 0.05 of MiniLM on the whole counterfactual set under v2, at the point
    used = [d["code"] for d in res["loaded"]]
    per = {c: {"whole_v2": res["encoders"][c]["v2"]["whole"], "delta": res["encoders"][c]["v2"]["vs_minilm"]["delta"], "within": res["encoders"][c]["v2"]["within_tol_point"],
               "ci_item": C.ci(res["encoders"][c]["v2"]["vs_minilm"]["item_ci"]), "ci_persona": C.ci(res["encoders"][c]["v2"]["vs_minilm"]["persona_ci"])} for c in used}
    holds = len(used) == 2 and all(per[c]["within"] for c in used)
    res["predictions"] = {"P-E1": {"verdict": "HOLDS" if holds else "FAILS", "encoders": per, "n_loaded": len(used)}}
    C.jdump(res, C.RESULTS / "enc_lookup.json")
    write_ledger(res)
    print("P-E1", res["predictions"]["P-E1"]["verdict"], per)


def fmt_p(p):
    return f"{p['delta']:+.4f} ({C.ci(p['item_ci'])}; {C.ci(p['persona_ci'])})"


def write_ledger(res):
    L = ["", "## T1. The name lookup under further sentence encoders (ADDENDUM_R122_ENCODERS.md)", "",
         f"### AUX-R122-ENC-LOCK", "",
         f"Registered text sha256 `{res['meta']['registration_sha256']}`; gates (MiniLM-L6-v2, the recorded encoder) {res['meta']['gates']} PASS; lookup code {res['meta']['lookup_code']}; "
         f"loaded {[d['model'] for d in res['loaded']]}; not loaded {res['not_loaded'] or 'none'}; {res['meta']['n_distinct_names']} distinct names; token seed {res['meta']['token_seed']}.", "",
         "### AUX-R122-ENC-ROWS — the lookup per encoder (AUROC; item-level and persona-grouped 95% intervals; the paired difference against MiniLM with both intervals)", "",
         "| encoder | population | whole | item CI | persona CI | minus MiniLM (item; persona) | SUP / RET / EXP |", "|---|---|---:|---|---|---|---|"]
    for code, E in res["encoders"].items():
        for pop in ("v2", "v3", "661", "661_clean"):
            B = E[pop]; ps = " / ".join(f"{B['per_state'][s]['auroc']:.4f}" for s in STATES) if "per_state" in B else "—"
            L.append(f"| {code} `{E['model']}` | {pop} | {B['whole']:.4f} | [{B['ci_item']['ci_lo']:.4f}, {B['ci_item']['ci_hi']:.4f}] | [{B['ci_persona']['ci_lo']:.4f}, {B['ci_persona']['ci_hi']:.4f}] | "
                     f"{fmt_p(B['vs_minilm']) if code != 'MINILM' else '(recorded row)'} | {ps} |")
    L += ["", "### AUX-R122-ENC-RANDOM — the random-token control (every attribute name replaced by a stable random token; descriptive)", "",
          "| encoder | population | whole | item CI | persona CI | minus the same encoder's name row | SUP / RET / EXP |", "|---|---|---:|---|---|---|---|"]
    for code, E in res["random_token"].items():
        for pop in ("v2", "v3", "661", "661_clean"):
            B = E[pop]; ps = " / ".join(f"{B['per_state'][s]['auroc']:.4f}" for s in STATES) if "per_state" in B else "—"
            own = res["encoders"][code][pop]["whole"]
            L.append(f"| {code} | {pop} | {B['whole']:.4f} | [{B['ci_item']['ci_lo']:.4f}, {B['ci_item']['ci_hi']:.4f}] | [{B['ci_persona']['ci_lo']:.4f}, {B['ci_persona']['ci_hi']:.4f}] | {B['whole'] - own:+.4f} | {ps} |")
    P = res["predictions"]["P-E1"]
    L += ["", f"### AUX-R122-ENC-P-E1 — **{P['verdict']}** (both encoders within 0.05 of MiniLM's 0.7663 on the whole counterfactual set under v2, at the point estimate)", ""]
    for c, d in P["encoders"].items():
        L.append(f"- {c}: {d['whole_v2']:.4f}, minus MiniLM {d['delta']:+.4f} (item {d['ci_item']}; persona {d['ci_persona']}); within tolerance: {d['within']}")
    C.append_ledger("\n".join(L) + "\n")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        gates()
    elif cmd == "run":
        run()
    else:
        raise SystemExit("usage: enc_lookup.py check|run")
