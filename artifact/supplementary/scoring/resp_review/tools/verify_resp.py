"""verify_resp.py -- the verifier of registrations/ADDENDUM_RESP.md section L (frozen 17e6328).

NO API CALLS. Exit 0 only if every check that applies passes. Checks A-C run always (the empty
cell); D-G run as their artifacts exist. Usage: python resp_review/tools/verify_resp.py

  A  lineage: sha256 pins on the frozen modules and data; prompts_e1 file and texts digests;
     ADDENDUM_RESP.md byte-identical to its state at the freeze commit
  B  populations: 661 / 104 (63 / 26 / 15), 307 / 35, 302 distinct questions, 187 cached question
     vectors, bank vectors covering every entry of the 40 personas
  C  the frozen censuses: section renderer lock on the 242 keys; §C.2 (tau and every count);
     §C.1 own-name census (TRUE 74 / 63 / 11 / 0; BELIEVED 31 / 24 / 3 / 4); §C.4 blind census;
     §C.5 marker fractions
  D  prompts_resp.py carries exactly the §L2 / §L3 texts (constructed from prompts_e1 by the
     stated replacements) and the ledgered hashes
  E  l1/indexes_own.json: every V2-OWN text re-derived and byte-identical; census flags; no marker,
     no ':' in a name; the 559 unchanged texts equal the committed texts
  F  l2/question_emb.npz + retrieval.json: matrix sha256 as ledgered; every top-5 / top-10 re-derived
     from the pinned vectors through LifecycleBank.cosine_search_all; every line byte-identical;
     reach flags re-derived
  G  run/rows_resp.jsonl + scores_resp.json: every score, interval and verdict re-derived with the
     committed estimators; spend under $4; every §L key present in NUMBERS_RESP.md
"""
from __future__ import annotations

import io
import json
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import resp_common as RC                                                     # noqa: E402
from resp_common import ROOT, RESP, L1, L2, RUN, J                           # noqa: E402

FAIL = []


def check(cond, msg):
    print(("  ok    " if cond else "  FAIL  ") + msg)
    if not cond:
        FAIL.append(msg)


# ------------------------------------------------------------------ A lineage
def check_a():
    print("A  lineage")
    for rel, pin in RC.PINS.items():
        check(RC.sha(ROOT / rel) == pin, f"{rel} sha256 {pin}")
    import prompts_e1 as P
    check(P.file_sha256() == RC.PIN_PROMPTS["file"], "prompts_e1 file digest 337d37d3…")
    check(P.texts_sha256() == RC.PIN_PROMPTS["texts"], "prompts_e1 texts digest 35d9b968…")
    check((P.MODEL, P.TEMPERATURE, P.SEED, P.MAX_TOKENS) == ("gpt-4.1-mini", 0, 42, 200), "lane gpt-4.1-mini / 0 / 42 / 200")
    frozen = subprocess.run(["git", "show", f"{RC.FREEZE}:registrations/ADDENDUM_RESP.md"], cwd=ROOT,
                            capture_output=True).stdout
    now = (ROOT / "registrations/ADDENDUM_RESP.md").read_bytes()
    check(frozen.replace(b"\r\n", b"\n") == now.replace(b"\r\n", b"\n"), f"ADDENDUM_RESP.md byte-identical to {RC.FREEZE}")


# ------------------------------------------------------------------ B populations
def check_b(sub):
    print("B  populations")
    check(len(sub) == 661 and sum(i["y_nok"] for i in sub) == 104, "661 items / 104 PN")
    qs = sorted({i["question"] for i in sub})
    check(len(qs) == 302, f"302 distinct questions ({len(qs)})")
    z = np.load(ROOT / "artifacts/theory/query_emb_cache.npz", allow_pickle=True)
    cached = set(map(str, z["ids"]))
    qids = {i["question_id"] for i in sub}
    check(sum(1 for q in qids if q in cached) == 187, f"187 question ids with a cached vector ({sum(1 for q in qids if q in cached)})")
    n_ent, n_cov, n_p = 0, 0, 0
    fe = {}
    for e in J(RC.E1 / "backend_entries" / "frbank.json"):
        fe.setdefault(e["persona"], set()).add(e["entry_id"])
    for name in sorted(fe):
        bank = J(ROOT / f"LifeMemEval/artifacts/lifecycle_banks/{name}.json")
        ids = {e["id"] for e in bank["entries"]}
        emb = np.load(ROOT / f"LifeMemEval/artifacts/lifecycle_banks/{name}_embeddings.npz", allow_pickle=True)
        eids = set(map(str, emb["ids"]))
        n_p += 1; n_ent += len(ids); n_cov += len(ids & eids)
        if ids != fe[name]:
            check(False, f"{name}: bank entries differ from backend_entries/frbank.json")
    check(n_p == 40 and n_ent == 18936 and n_cov == 18936, f"bank vectors cover {n_cov} of {n_ent} entries of {n_p} personas")


# ------------------------------------------------------------------ C censuses
def check_c(sub):
    print("C  frozen censuses")
    keys = sorted({i["index_key"] for i in sub})
    ok, bad = RC.section_lock(keys)
    check(len(keys) == 242 and ok == 242, f"section renderer lock {ok} / {len(keys)}")
    own_t = RC.own_name_census(sub, "TRUE"); own_b = RC.own_name_census(sub, "BELIEVED")
    check((own_t.get("all"), own_t.get("sup"), own_t.get("ret"), own_t.get("exp", 0)) == (74, 63, 11, 0), f"own-name TRUE {own_t}")
    check((own_b.get("all"), own_b.get("sup"), own_b.get("ret"), own_b.get("exp")) == (31, 24, 3, 4), f"own-name BELIEVED {own_b}")
    tau, null, rows, names, pairs = RC.l1_census(sub)
    check(round(tau, 6) == RC.EXPECT_TAU and null["n_pairs"] == 577, f"tau {tau:.6f} on {null['n_pairs']} token-disjoint pairs")
    check(len(names) == 35 and len(pairs) == 47, f"35 names / 47 within-section pairs ({len(names)} / {len(pairs)})")
    c = RC.census_counts(rows)
    for k, v in RC.EXPECT_C2.items():
        check(c[k] == v, f"§C.2 {k} = {v}" + ("" if c[k] == v else f" (got {c[k]})"))
    bc = RC.blind_census(sub)
    check(bc["values"] == {0.0: 655, 0.1: 6} and bc["ncf_true"] == 0 and bc["pn_at_zero"] == 104 and round(bc["auroc"], 4) == 0.4946,
          f"§C.4 blind census {bc['values']}, ncf true {bc['ncf_true']}, PN at 0 {bc['pn_at_zero']}, AUROC {bc['auroc']:.4f}")
    mf = RC.marker_fractions()
    for k, v in RC.EXPECT_Q4.items():
        got = mf[k]
        t = (got["indexes"], got["lines"], got["tokens"], got["marker_occurrences"], got["marker_lines"], got["marker_tokens"], got["fraction"])
        check(t == v, f"§C.5 {k} {t}")
    return tau, rows


# ------------------------------------------------------------------ D prompts
def check_d():
    p = RESP / "tools" / "prompts_resp.py"
    if not p.exists():
        print("D  prompts_resp.py absent (not yet built)"); return
    print("D  prompts")
    import prompts_resp as PR
    import prompts_e1 as P
    check(PR.SYSTEM_RETRIEVED == P.SYSTEM.replace(PR.FROZEN_PASSAGE, PR.VARIANT_PASSAGE) and PR.SYSTEM_RETRIEVED != P.SYSTEM
          and P.SYSTEM.count(PR.FROZEN_PASSAGE) == 1, "SYSTEM_RETRIEVED = SYSTEM with exactly the one passage replaced")
    check(PR.USER_RETRIEVED == PR.USER_RETRIEVED_TEXT and PR.USER_HYBRID == PR.USER_HYBRID_TEXT, "USER_RETRIEVED / USER_HYBRID as §L2")
    check(PR.USER_HYBRID.startswith(P.USER_INDEXED.split("Question:")[0]), "USER_HYBRID carries USER_INDEXED's paragraph and fence unchanged")
    ng = PR.SYSTEM_NOGATE
    check("Judge this in two steps." not in ng and "Step 1" not in ng and "Step 2" not in ng and "nok_candidates_found" not in ng,
          "SYSTEM_NOGATE: gate sentences, Step 1, Step 2 labels and the field removed")
    check(PR.NOGATE_LINE in ng and "nok = 5." in ng and "nok = 85." in ng and PR.NOGATE_SCHEMA in ng, "SYSTEM_NOGATE: folded line, examples, schema")
    check(ng == PR.nogate_from_frozen(P.SYSTEM), "SYSTEM_NOGATE re-derived from frozen SYSTEM by the listed edits")
    led = (RESP / "NUMBERS_RESP.md").read_text(encoding="utf-8")
    for nm, txt in (("SYSTEM_RETRIEVED", PR.SYSTEM_RETRIEVED), ("USER_RETRIEVED", PR.USER_RETRIEVED),
                    ("USER_HYBRID", PR.USER_HYBRID), ("SYSTEM_NOGATE", PR.SYSTEM_NOGATE)):
        h = RC.sha_text(txt)
        check(h in led, f"{nm} sha256 {h[:16]}… ledgered")


# ------------------------------------------------------------------ E V2-OWN
def check_e(sub, rows):
    p = L1 / "indexes_own.json"
    if not p.exists():
        print("E  l1/indexes_own.json absent (not yet built)"); return
    print("E  V2-OWN texts")
    own = J(p)["items"]
    idx = RC.indexes()
    byid = {r["item_id"]: r for r in rows}
    n_ok, n_bad, n_unch = 0, 0, 0
    for it in sub:
        r, o = byid[it["item_id"]], own[it["item_id"]]
        exp = RC.own_text(idx[it["index_key"]], r["remaining"]) if r["changed"] else idx[it["index_key"]]
        if o["text"] == exp and o["changed"] == r["changed"] and sorted(o["removed"]) == r["removed"]:
            n_ok += 1
        else:
            n_bad += 1
        n_unch += (not r["changed"]) and o["text"] == idx[it["index_key"]]
        pre, _ = RC.split_section(o["text"]); pre_c, _ = RC.split_section(idx[it["index_key"]])
        if pre != pre_c:
            check(False, f"{it['item_id']}: bytes before the section header changed")
        if RC.IX.MARKER in o["text"] or any(":" in n for n in RC.section_names(o["text"]) if n != "(none)"):
            check(False, f"{it['item_id']}: marker or ':' name in a V2-OWN text")
    check(n_ok == 661 and n_bad == 0, f"V2-OWN texts re-derived byte-identical {n_ok} / 661")
    check(n_unch == 559, f"559 unchanged texts equal the committed texts ({n_unch})")


# ------------------------------------------------------------------ F retrieval
def check_f(sub):
    if not (L2 / "retrieval.json").exists() or not (L2 / "question_emb.npz").exists():
        print("F  l2 artifacts absent (not yet built)"); return
    print("F  retrieval")
    import build_l2 as BL
    led = (RESP / "NUMBERS_RESP.md").read_text(encoding="utf-8")
    msha = RC.sha(L2 / "question_emb.npz", 64)
    check(msha in led, f"question_emb.npz sha256 {msha[:16]}… ledgered")
    art = J(L2 / "retrieval.json")
    qemb = BL.load_question_vectors()
    n_ok, n_line, n_reach = 0, 0, 0
    for it in sub:
        rec = art["items"][it["item_id"]]
        top, block = BL.retrieve(it, qemb[it["question"]])
        if [t[0] for t in top[:10]] == rec["top10_ids"] and [t[0] for t in top[:5]] == rec["top5_ids"]:
            n_ok += 1
        if block == rec["block"]:
            n_line += 1
        if it["y_nok"]:
            reach = bool(set(it["pn_members"]) & set(rec["top5_ids"]))
            n_reach += reach == rec["reach_k5"]
    check(n_ok == 661, f"top-5 / top-10 re-derived from the pinned vectors {n_ok} / 661")
    check(n_line == 661, f"rendered blocks byte-identical {n_line} / 661")
    check(n_reach == 104, f"reach flags re-derived {n_reach} / 104")


# ------------------------------------------------------------------ G scores
def check_g(sub):
    if not (RUN / "rows_resp.jsonl").exists() or not (RUN / "scores_resp.json").exists():
        print("G  run artifacts absent (not yet run / scored)"); return
    print("G  scores")
    import run_resp as RR
    saved = J(RUN / "scores_resp.json")
    fresh = RR.score_all(write=False)
    diff = RR.compare_scores(saved, fresh)
    check(not diff, "every score, interval and verdict re-derived from rows_resp.jsonl" + ("" if not diff else f" ({len(diff)} differ: {diff[:3]})"))
    spend = RR.billed_so_far()["total"]
    check(spend < 4.0, f"spend ${spend:.4f} under $4")
    led = (RESP / "NUMBERS_RESP.md").read_text(encoding="utf-8")
    for k in RR.LEDGER_KEYS:
        check(k in led, f"{k} present in NUMBERS_RESP.md")


def main():
    check_a()
    sub = RC.load_cell()
    check_b(sub)
    tau, rows = check_c(sub)
    check_d()
    check_e(sub, rows)
    check_f(sub)
    check_g(sub)
    print("\nverify_resp:", "PASS" if not FAIL else f"FAIL ({len(FAIL)}): " + "; ".join(FAIL[:5]))
    sys.exit(0 if not FAIL else 1)


if __name__ == "__main__":
    main()
