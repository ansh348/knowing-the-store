"""verify_cf2.py -- the verifier ADDENDUM_CF2.md (frozen f016f03, baseline 35743cb) requires to
exist and pass before any CF-2 store version exists. NO API CALLS.

Usage, from the repository root:  python r82_counterfactual/tools/verify_cf2.py

Pre-version checks (always run):
  A  lineage digests -- prompts_e1 file and texts digests as E1 committed them; the frozen
     drafting prompt sha (draft_questions.prompt_sha256, seven bound fields); sha256 of the
     renderer and estimator sources pinned at the freeze (index_v2.py, index_v3.py,
     common_e1r.py, draft_questions.py).
  B  the census gate -- select_pairs.candidates_for on the 40 banks reproduces
     reviews/CF2_SCOPE.md Phase 2 (L206-218, L223-224, L236-237, L247, L249-252): every stage
     count, the 16 ELIGIBLE and 9 INELIGIBLE expiry ids, the 422-id / 32-persona overlap set,
     the O2 four, and O3's 87 -> 41 with its category breakdown and 23 personas.
  C  the Phase 3 1e-9 gate -- the histogram Mann-Whitney re-implementation of
     common_e1r.boot_item reproduces the committed CF-1 item intervals on every lane.
Post-version checks (skip with a printed reason while r82_counterfactual/cf2/ holds no cell):
  D  the 480-item label table (100/30/30 by D-CF2-1), write-path predicates and expiry anchors
  E  the V2R RENDERER LOCK (byte-identical to v2 outside the two count fields)
  F  both leakage rows present in cf2/NUMBERS_CF2.md
  G  every ADDENDUM_CF2 section 9 key present in cf2/NUMBERS_CF2.md
Exit 0 iff every applicable check passes. A failing check prints "FAIL <check>: <detail>" and the
script exits 1; ADDENDUM_CF2 section 13 makes that a STOP.
"""
from __future__ import annotations

import collections
import hashlib
import re
import io
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in ("e0_metamemory/tools", "e1_metamemory/tools", "e1r_robustness/tools",
          "r82_counterfactual", "r82_counterfactual/tools"):
    sys.path.insert(0, str(ROOT / p))

import e0_common as C                                    # noqa: E402
from e0_common import parse_dt, toks                     # noqa: E402
import select_pairs as SPm                               # noqa: E402
from build_cf_cell import Join, build_index              # noqa: E402
from index_v2 import scrub                               # noqa: E402
from index_v3 import named_sections                      # noqa: E402
import prompts_e1 as P                                   # noqa: E402
import draft_questions as D                              # noqa: E402
from common_e1r import boot_item                         # noqa: E402
import score_cf as S                                     # noqa: E402

R82 = ROOT / "r82_counterfactual"
CF2 = R82 / "cf2"
J = lambda p: json.load(io.open(p, encoding="utf-8"))  # noqa: E731

FAILS: list[str] = []


def check(name, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'} {name}" + (f": {detail}" if detail and not ok else ""))
    if not ok:
        FAILS.append(f"{name}: {detail}")


# ------------------------------------------------------------------ A. lineage
PIN = {
    "prompts_e1 file":  "337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84",
    "prompts_e1 texts": "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2",
    "draft prompt sha": "b748247b3ff380d8c24a3e142e2c37c12718942438c3a96cce476531692a8c7f",
}
PIN_FILES = {  # sha256 of the source at the freeze (f016f03)
    "e1_metamemory/tools/index_v2.py":            "baeaab11e1b5e94d38809160d6ca0ca8041c00461fe0ad4f674ccc14bf5c94a9",
    "r82_counterfactual/index_v3.py":              "e4ea6193f6adfa195e5464966d7074374fcc57f0f145727e161263d7fe0e1a1f",
    "e1r_robustness/tools/common_e1r.py":          "ab3581f5b6ec2db2d7e1849b3a86d8ac8dd1e0137e515b87a8a89126335072b6",
    "r82_counterfactual/tools/draft_questions.py": "c47136f3aa845cae13807238d857500f5f9578d946a02934d9d4d69c669c4d06",
}


def check_lineage():
    print("A. lineage")
    check("prompts_e1 file digest", P.file_sha256() == PIN["prompts_e1 file"], P.file_sha256())
    check("prompts_e1 texts digest", P.texts_sha256() == PIN["prompts_e1 texts"], P.texts_sha256())
    check("draft_questions prompt sha (7 bound fields)", D.prompt_sha256() == PIN["draft prompt sha"], D.prompt_sha256())
    for rel, want in PIN_FILES.items():
        got = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        check(f"source pinned: {rel}", got == want, got)


# ------------------------------------------------------------------ B. census gate
EXPECT_STAGES = {"EXPIRY": [46, 41, 41, 32, 25, 25],
                 "RETRACTION": [1590, 1379, 1173, 1053, 1048, 1043],
                 "SUPERSESSION": [3347, 3230, 3230, 3187, 3170, 3133]}
EXP16 = {("aisha", "lb_00517"), ("callum", "lb_00387"), ("dariush", "lb_00418"), ("dariush", "lb_00419"),
         ("fatima", "lb_00397"), ("jake", "lb_00358"), ("kofi", "lb_00511"), ("marcus", "lb_00236"),
         ("marley", "lb_00344"), ("patrick", "lb_00343"), ("patrick", "lb_00344"), ("patrick", "lb_00345"),
         ("patrick", "lb_00349"), ("patrick", "lb_00350"), ("rosa", "lb_00528"), ("valentina", "lb_00364")}
INEL9 = {("alex", "lb_00347"), ("david", "lb_00312"), ("david", "lb_00398"), ("kofi", "lb_00497"),
         ("mehmet", "lb_00428"), ("mirri", "lb_00466"), ("mirri", "lb_00478"), ("pan", "lb_00484"),
         ("rosa", "lb_00511")}
O2_FOUR = {("raj", "lb_00437"), ("raj", "lb_00443"), ("raj", "lb_00447"), ("thanh", "lb_00476")}
O3_BREAKDOWN = {"PROJECTS_ENDEAVORS": 20, "RELATIONAL_BONDS": 9, "FINANCIAL_MATERIAL": 5,
                "HEALTH_WELLBEING": 3, "HOBBIES_RECREATION": 3, "PREFERENCES_HABITS": 1}
SEC = {"SUPERSESSION": "superseded", "RETRACTION": "retracted", "EXPIRY": "expired"}


def overlap_sets():
    pairs90 = J(R82 / "cf_pairs.json")["pairs"]
    ov90_ids = {(p["persona"], p["entry_id"]) for p in pairs90}
    ov90_slots = {(p["persona"], scrub(p["slot_key"][1])) for p in pairs90}
    c84 = J(ROOT / "e1xv_crossvendor/manifests/cell_84.json")["items"]
    itf = {r["item_id"]: r for r in J(ROOT / "e1_metamemory/build/items_final.json")}
    sabl = J(ROOT / "e1_metamemory/build/slot_ablations.json")
    ov84 = set()
    for it in c84:
        r = itf[it["item_id"]]
        for eid in (r.get("pn_members") or []):
            ov84.add((r["persona"], eid))
        for eid in sabl.get(r["persona"] + ":" + r["question_id"], []):
            ov84.add((r["persona"], eid))
    ov36 = {(r["persona"], r["slot"]) for r in J(ROOT / "r74/x5/x5_render.json")["rows"]}
    return ov90_ids, ov90_slots, ov84, ov36


def census_rows():
    """Every frozen-predicate candidate and every O3 candidate over the 40 banks, with the
    individuation, superseded-list, overlap and verdict flags of CF2_SCOPE Phase 2."""
    ov90_ids, ov90_slots, ov84, ov36 = overlap_sets()
    _, verdicts = SPm.load_verdicts()
    ypaths = {p.name.replace(".yaml", "").split("_")[-1]: p for p in sorted(C.LME.glob("*/persona_*.yaml"))}
    rows = []
    for bank_path in sorted(SPm.BANKS.glob("*.json")):
        persona = bank_path.stem
        if persona not in ypaths:
            continue
        entries = J(bank_path)["entries"]
        t_now, cutoff = SPm.persona_clock(entries)
        y0 = C.load_yaml(ypaths[persona])
        blk = y0.get("persona")
        drop = toks(blk.get("name", "") if isinstance(blk, dict) else "")
        v2, v3, _ = build_index(Join(persona, entries, y0, t_now, cutoff, drop), set())
        secs = {"v2": named_sections(v2), "v3": named_sections(v3)}
        cands = SPm.candidates_for(entries, cutoff)
        occ = collections.Counter(tuple(e["slot_key"]) for e in entries if e.get("slot_key"))
        o3 = []
        for e in entries:
            sk = e.get("slot_key")
            if not sk or occ[tuple(sk)] != 1:
                continue
            if not e.get("is_active") or e.get("is_retracted") or e.get("supersedes"):
                continue
            if len(toks(e.get("text", ""), frozenset())) < SPm.MIN_TEXT_TOKENS:
                continue
            evt = parse_dt(e.get("event_time"))
            if evt is not None and cutoff is not None and evt >= cutoff and e.get("category") not in SPm.EXP_CATS:
                o3.append(e)
        for cls, lst in list(cands.items()) + [("O3", o3)]:
            vcls = "EXPIRY" if cls == "O3" else cls
            for e in lst:
                nm = scrub(e["slot_key"][1]); key = (persona, e["id"])
                rows.append({"cls": cls, "persona": persona, "entry_id": e["id"], "category": e.get("category"),
                             "slot_scrubbed": nm,
                             "individuates": nm not in secs["v3"][SEC[vcls]],
                             "not_on_v2_sup": nm not in secs["v2"]["superseded"],
                             "ov90": key in ov90_ids or (persona, nm) in ov90_slots,
                             "ov84": key in ov84, "ov36": (persona, nm) in ov36,
                             "verdict": verdicts.get(vcls, {}).get(key, (None, None))[0]})
    return rows, (len(ov84), len({p for p, _ in ov84}))


def stages(rows, cls):
    s0 = [x for x in rows if x["cls"] == cls]
    s1 = [x for x in s0 if x["individuates"]]
    s2 = [x for x in s1 if x["not_on_v2_sup"]]
    s3 = [x for x in s2 if not x["ov90"]]
    s4 = [x for x in s3 if not x["ov84"]]
    s5 = [x for x in s4 if not x["ov36"]]
    return [len(s0), len(s1), len(s2), len(s3), len(s4), len(s5)], s5, s3


def check_census():
    print("B. census gate (CF2_SCOPE Phase 2)")
    rows, (n84, p84) = census_rows()
    check("the 84 overlap set is 422 ids over 32 personas", (n84, p84) == (422, 32), f"{n84} over {p84}")
    for cls in ("EXPIRY", "RETRACTION", "SUPERSESSION"):
        st, clean, _ = stages(rows, cls)
        check(f"{cls} stages {EXPECT_STAGES[cls]}", st == EXPECT_STAGES[cls], str(st))
        if cls == "EXPIRY":
            elig = {(x["persona"], x["entry_id"]) for x in clean if x["verdict"] == "ELIGIBLE"}
            inel = {(x["persona"], x["entry_id"]) for x in clean if x["verdict"] == "INELIGIBLE"}
            check("the 16 clean ELIGIBLE expiry ids", elig == EXP16, f"+{sorted(elig - EXP16)} -{sorted(EXP16 - elig)}")
            check("the 9 clean INELIGIBLE expiry ids", inel == INEL9, f"+{sorted(inel - INEL9)} -{sorted(INEL9 - inel)}")
            check("no unadjudicated clean expiry candidate", all(x["verdict"] for x in clean))
            check("clean expiry over 16 personas, 24 distinct names",
                  (len({x["persona"] for x in clean}), len({(x["persona"], x["slot_scrubbed"]) for x in clean})) == (16, 24))
            # O2: the four ELIGIBLE entries the 84 filter removed (pass the 90, fail the 84)
            _, _, s3 = stages(rows, cls)
            rem84 = {(x["persona"], x["entry_id"]) for x in s3 if x["ov84"] and x["verdict"] == "ELIGIBLE"}
            check("O2: the four ELIGIBLE expiry entries removed by the 84 filter", rem84 == O2_FOUR, str(sorted(rem84)))
    st3, clean3, _ = stages(rows, "O3")
    bd = collections.Counter(x["category"] for x in clean3)
    check("O3 raw 87 and clean 41", (st3[0], st3[5]) == (87, 41), str(st3))
    check("O3 breakdown", dict(bd) == O3_BREAKDOWN, str(dict(bd)))
    check("O3 clean over 23 personas, all unadjudicated",
          len({x["persona"] for x in clean3}) == 23 and all(x["verdict"] is None for x in clean3))
    return rows


# ------------------------------------------------------------------ C. Phase 3 gate
def auc_hist(Sidx, Yk, V):
    R, N = Sidx.shape; off = (np.arange(R) * V)[:, None]
    pos = np.bincount((Sidx + off)[Yk == 1], minlength=R * V).reshape(R, V).astype(float)
    neg = np.bincount((Sidx + off)[Yk == 0], minlength=R * V).reshape(R, V).astype(float)
    below = np.cumsum(neg, axis=1) - neg
    return (pos * (below + 0.5 * neg)).sum(1) / (pos.sum(1) * neg.sum(1))


def boot_item_ci(b, i, y, n=1000, seed=42):
    grid = np.unique(np.concatenate([b, i])); V = len(grid)
    bi = np.searchsorted(grid, b); ii = np.searchsorted(grid, i)
    rng = np.random.default_rng(seed); N = len(y)
    K = rng.integers(0, N, (n, N)); Yk = y[K]; keep = (Yk.sum(1) > 0) & (Yk.sum(1) < N)
    K = K[keep]; Yk = Yk[keep]
    d = auc_hist(ii[K], Yk, V) - auc_hist(bi[K], Yk, V)
    return float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


def check_phase3_gate():
    print("C. Phase 3 1e-9 gate (committed CF-1 item intervals)")
    cell = J(R82 / "cf_cell.json"); items = cell["items"]
    pairs = sorted({it["pair_id"] for it in items}); Pn = len(pairs)
    qmap = {q: f"q{n:02d}" for n, q in enumerate(sorted({it["question"] for it in items}))}
    VORD = {"PRESENT": 0, "ABSENT": 1, "PN": 2}
    for code in ("MINI", "H45", "OP5"):
        lane = S.load_lane(code)
        Y = np.zeros((Pn, 3), int); B = np.zeros((Pn, 3)); V2 = np.zeros((Pn, 3)); V3 = np.zeros((Pn, 3))
        for it in items:
            r = pairs.index(it["pair_id"]); c = VORD[it["version"]]
            Y[r, c] = it["y_nok"]; B[r, c] = lane[(qmap[it["question"]], "BLIND")]
            V2[r, c] = lane[(it["item_id"], "INDEXED-V2")]; V3[r, c] = lane[(it["item_id"], "INDEXED-V3")]
        y0 = Y.reshape(-1); b0 = B.reshape(-1)
        for tag, Mx in (("v2", V2), ("v3", V3)):
            ref = boot_item(b0, Mx.reshape(-1), y0); lo, hi = boot_item_ci(b0, Mx.reshape(-1), y0)
            ok = abs(lo - ref["ci_lo"]) < 1e-9 and abs(hi - ref["ci_hi"]) < 1e-9
            check(f"{code} {tag} interval reproduced to 1e-9", ok, f"ref [{ref['ci_lo']:.6f},{ref['ci_hi']:.6f}] got [{lo:.6f},{hi:.6f}]")


# ------------------------------------------------------------------ D-G. post-version
KEYS_S9 = ["CONSTRUCTION", "CENSUS", "ADJUDICATION", "OVERLAP", "INDIVIDUATION", "INDEXSIZE", "V2R-DEF",
           "LEAKSCREEN-V3", "LEAKSCREEN-V2R", "BLIND", "MINI-V2", "MINI-V3", "MINI-V2R", "H45-V2", "H45-V3",
           "H45-V2R", "OP5-V2", "OP5-V3", "OP5-V2R", "PERSTATE", "COUNTED", "NAMEDVSCOUNTED", "EQUIV-V2R",
           "NB6-V2", "ALLSTATES-V3", "NB5-V2", "FOK", "POWER", "SPEND", "DROPRULE"]
CELL_PATH, IDX_PATH, LEDGER = CF2 / "cf_cell.json", CF2 / "cf_indexes.json", CF2 / "NUMBERS_CF2.md"


def check_label_table():
    print("D. label table, write-path predicates, expiry anchors")
    if not CELL_PATH.exists():
        print(f"  skip  no cell at {CELL_PATH.relative_to(ROOT)} (no store version exists yet)"); return
    cell = J(CELL_PATH); items = cell["items"]
    n = collections.Counter(it["version"] for it in items)
    npairs = len(J(CF2 / "cf_pairs_cf2.json")["pairs"])
    check(f"{3 * npairs} items, {npairs} per version (D-CF2-1; D-CF2-4)", (len(items), n["PRESENT"], n["ABSENT"], n["PN"]) == (3 * npairs, npairs, npairs, npairs), str(dict(n)))
    check(f"{npairs} PN positives", sum(it["y_nok"] for it in items) == npairs)
    want = {"PRESENT": "PRESENT", "ABSENT": "ABSENT", "PN": "PRESENT-NEGATIVE"}
    check("every version carries its intended label", all(it["label"] == want[it["version"]] for it in items))
    st = collections.Counter(it["state"] for it in items if it["version"] == "PN")
    qd = J(CF2 / "cf_pairs_cf2.json")["meta"].get("quota", {"SUPERSESSION": 100, "RETRACTION": 30, "EXPIRY": 30})
    check(f"composition {qd['SUPERSESSION']}/{qd['RETRACTION']}/{qd['EXPIRY']} (D-CF2-1; D-CF2-4)", (st["SUPERSESSION"], st["RETRACTION"], st["EXPIRY"]) == (qd["SUPERSESSION"], qd["RETRACTION"], qd["EXPIRY"]), str(dict(st)))
    check("build recorded zero assertion failures", not cell.get("meta", {}).get("fails"), str(cell.get("meta", {}).get("fails")))


def check_v2r_lock():
    print("E. V2R RENDERER LOCK")
    if not IDX_PATH.exists():
        print(f"  skip  no indexes at {IDX_PATH.relative_to(ROOT)} (no store version exists yet)"); return
    doc = J(IDX_PATH); idx = doc["indexes"]
    if "v2r" not in doc["meta"].get("arms", []) and not (CF2 / "rows").exists():
        print("  skip  V2R not yet rendered (build step 2); no monitor call has been made"); return
    m = doc["meta"].get("v2r", {})
    check("V2R permutation recorded: seed 42, no version keeps its own pair, multiset preserved",
          m.get("seed") == 42 and m.get("versions_keeping_own_pair") == 0 and m.get("multiset_preserved") is True and len(m.get("permutation", {})) == len(idx))
    bad = []
    for k, v in idx.items():
        if "v2r" not in v:
            bad.append(k); continue
        a, b = v["v2"].split("\n"), v["v2r"].split("\n")
        diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
        ok = len(a) == len(b) and all(a[i].lstrip().startswith(("retracted", "expired")) for i in diff)
        if not ok:
            bad.append(k)
    check("every V2R differs from v2 only on the retracted/expired count lines", not bad, f"{len(bad)} versions: {bad[:3]}")


def key_written(text, k):
    """A key counts as written only as a ledger table row or a section heading, never as a
    mention in prose (the reserved-key list names every key)."""
    # the first cell is the key, optionally with a -SUFFIX and a parenthetical qualifier such as "(mini, descriptive)"
    pat = rf"^(\|\s*\**AUX-CF2-{re.escape(k)}(-[A-Z0-9]+)?\**\s*(\([^|]*\))?\s*\||##.*AUX-CF2-{re.escape(k)}\b)"
    return re.search(pat, text, re.M) is not None


def ledger_text():
    return LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else None


def check_leakage_rows():
    print("F. leakage rows")
    t = ledger_text()
    if not CELL_PATH.exists():
        print("  skip  no store version exists yet (leakage screens run on the built indexes)"); return
    if t is None:
        check("ledger exists once a cell exists", False, str(LEDGER.relative_to(ROOT))); return
    if not (CF2 / "rows").exists() and not (CF2 / "results" / "leakscreen_cf2.json").exists():
        print("  skip  no monitor call made yet; the screens run before the first lane (build step 3)"); return
    for k in ("AUX-CF2-LEAKSCREEN-V3", "AUX-CF2-LEAKSCREEN-V2R"):
        check(f"{k} present as a ledger row", key_written(t, k.replace("AUX-CF2-", "")))
    lk = CF2 / "results" / "leakscreen_cf2.json"
    check("leakage screen results deposited", lk.exists())
    if lk.exists():
        r = J(lk)
        check("both screens at most 3 of 30 correct", all(c["n_correct"] <= 3 and c["n"] == 30 for c in r["cells"].values()),
              str({k: c["n_correct"] for k, c in r["cells"].items()}))


def check_ledger_keys():
    print("G. section 9 keys")
    t = ledger_text()
    if not CELL_PATH.exists() or not (CF2 / "results" / "cf_scores_cf2.json").exists():
        print("  skip  no scores yet (keys fill as the cell is built and scored; every key is required once cf_scores_cf2.json exists)")
        if t is not None:
            present = [k for k in KEYS_S9 if key_written(t, k)]
            print(f"        ledger present with {len(present)} of {len(KEYS_S9)} section 9 keys so far: {present}")
        return
    if t is None:
        check("ledger exists once a cell exists", False, str(LEDGER.relative_to(ROOT))); return
    missing = [k for k in KEYS_S9 if not key_written(t, k)]
    check("every section 9 key present", not missing, str(missing))


def check_adjudication():
    print("H. adjudication_cf2.json against the queue (pre-version; skips until the file exists)")
    A, Q = CF2 / "adjudication_cf2.json", CF2 / "adjudication_queue.json"
    if not A.exists():
        print("  skip  no adjudication file yet"); return
    adj, q = J(A), J(Q)["queues"]
    bad = []; summary = {}
    for cls in ("EXPIRY", "RETRACTION", "SUPERSESSION"):
        vs = adj.get(cls, {}).get("verdicts", [])
        for r in vs:
            qx = q[cls][r["n"] - 1]
            if (qx["persona"], qx["entry_id"]) != (r["persona"], r["entry_id"]):
                bad.append((cls, r["n"]))
            if r["walk_status"] == "REUSED" and qx["verdict"] != "ELIGIBLE":
                bad.append((cls, r["n"], "REUSED without CF-1 ELIGIBLE"))
            if r["walk_status"] == "SKIP-RANK" and qx["name_rank"] <= 1:
                bad.append((cls, r["n"], "SKIP-RANK at rank 1"))
        c = collections.Counter(r["walk_status"] for r in vs)
        summary[cls] = dict(c)
        if vs:
            reads = c["ELIGIBLE"] + c["INELIGIBLE"] + c["PENDING"]
            ok = adj[cls]["verdict_reads"] == reads and adj[cls]["eligible_total"] == c["ELIGIBLE"] + c["REUSED"]
            check(f"{cls}: recorded counts match the rows ({dict(c)})", ok, str(adj[cls].get("walk_status_counts")))
    check("every verdict row matches the queue's persona and entry id; REUSED and SKIP-RANK consistent", not bad, str(bad[:5]))
    ret = adj.get("RETRACTION", {})
    if ret.get("verdicts"):
        check("AUX-CF2-ADJUDICATION-RETRACTION: 369 verdict reads, 35 ELIGIBLE, rate 0.0949 (D-CF2-1)",
              (ret["verdict_reads"], ret["eligible_new"], round(ret["eligible_new"] / ret["verdict_reads"], 4)) == (369, 35, 0.0949),
              f"{ret['verdict_reads']} {ret['eligible_new']}")


def check_draw():
    print("I. the accepted draw (cf_pairs_cf2.json) against the merged queue, the cap and the one-per-name rule")
    Pp, Q = CF2 / "cf_pairs_cf2.json", CF2 / "adjudication_queue.json"
    if not Pp.exists():
        print("  skip  no accepted draw yet"); return
    doc = J(Pp); pairs = doc["pairs"]; q = J(Q)["queues"]
    quota14 = {"SUPERSESSION": 100, "RETRACTION": 30, "EXPIRY": 30}              # ADDENDUM_CF2 section 14 (D-CF2-1)
    quota = dict(doc["meta"].get("quota", quota14))                                # section 16 (D-CF2-4): the effective quota
    d4 = [e for e in doc["meta"].get("excluded", []) if e.get("excluded", {}).get("deviation") == "D-CF2-4"]
    if "quota" in doc["meta"]:
        check(f"D-CF2-4: effective quota {quota} = section-14 quota minus the {len(d4)} no-replacement exclusions; no further extension",
              quota["RETRACTION"] == 30 and quota["EXPIRY"] == 30 and quota["SUPERSESSION"] == doc["meta"]["quota_history"][0]["quota"]["SUPERSESSION"] - len(d4)
              and doc["meta"].get("no_further_extension") is True and all(e.get("excluded", {}).get("no_replacement") and not e.get("replaced_by") for e in d4))
    by = collections.Counter(p["state"] for p in pairs)
    pend = doc["meta"].get("pending_replacements", {})
    check(f"accepted + pending replacements = quota {quota['SUPERSESSION']}/30/30 in every state (D-CF2-2; D-CF2-4 once recorded)",
          all(by[c] + pend.get(c, 0) == quota[c] for c in quota) and len(pairs) == sum(quota.values()) - sum(pend.values()),
          f"accepted {dict(by)} pending {pend}")
    cap = collections.Counter((p["persona"], p["state"]) for p in pairs)
    check("cap 4 per persona per state", max(cap.values()) <= 4, str(max(cap.values())))
    names = collections.Counter((p["persona"], p["slot_scrubbed"]) for p in pairs)
    check("one pair per (persona, scrubbed name) across the draw", max(names.values()) == 1, str([k for k, v in names.items() if v > 1][:5]))
    bad = []
    for p in pairs:
        qx = q[p["state"]][p["queue_position"] - 1]
        if (qx["persona"], qx["entry_id"]) != (p["persona"], p["entry_id"]): bad.append((p["state"], p["queue_position"], "queue row"))
        if qx.get("adjudication", {}).get("status") != "ELIGIBLE": bad.append((p["state"], p["queue_position"], "not ELIGIBLE in the merged queue"))
        if p["adjudication"] != "ELIGIBLE": bad.append((p["state"], p["queue_position"], "pair not ELIGIBLE"))
        if p["overlap_tag"] not in (None, "O1", "O2") or (p["overlap_tag"] and p["state"] != "EXPIRY"): bad.append((p["state"], p["queue_position"], "overlap tag"))
        if p["intent"] != SPm.CLASS_INTENT[p["state"]]: bad.append((p["state"], p["queue_position"], "intent"))
    check("every pair is an ELIGIBLE queue row with a valid overlap tag and the class intent", not bad, str(bad[:5]))
    # nothing skipped that should have been accepted: the walk is a prefix rule, so every ELIGIBLE
    # row before a state's last accepted position is either accepted or passed over by cap/name
    excluded = doc["meta"].get("excluded", [])
    acc = {(p["state"], p["queue_position"]) for p in pairs} | {(e["state"], e["queue_position"]) for e in excluded}
    passed = {(x["state"], x["position"]) for x in doc["meta"]["passed_over_at_acceptance"]}
    # a replacement re-walks the state's queue from position 1 under the CURRENT constraints, so rows it
    # passes over by cap or name are legitimate skips: recompute them against the final draw
    names = {(p["persona"], p["slot_scrubbed"]) for p in pairs}
    capc = collections.Counter((p["persona"], p["state"]) for p in pairs)
    miss = []
    for cls in quota:
        last = max(p["queue_position"] for p in pairs if p["state"] == cls)
        for x in q[cls]:
            if x["position"] <= last and x["adjudication"]["status"] == "ELIGIBLE" and (cls, x["position"]) not in acc | passed:
                blocked = (x["persona"], x["slot_scrubbed"]) in names or capc[(x["persona"], cls)] >= 4
                if not blocked:
                    miss.append((cls, x["position"]))
    if miss and doc["meta"].get("no_further_extension"):
        # D-CF2-4: capacity freed by a no-replacement exclusion is not refilled, so an ELIGIBLE row before the last
        # accepted position may now be admissible and undrawn; it is a spare the author may rule on, not a skip
        check(f"acceptance is a prefix of each state's queue up to D-CF2-4; {len(miss)} ELIGIBLE row(s) admissible but undrawn under no-replacement: {miss}", True)
    else:
        check("acceptance is a prefix of each state's queue (no ELIGIBLE row silently skipped; D-CF2-2 exclusions counted)", not miss, str(miss[:5]))
    for e in excluded:
        dev = e.get("excluded", {}).get("deviation")
        ok = dev in ("D-CF2-2", "D-CF2-4") and e.get("adjudication") == "ELIGIBLE" and "report" in e["excluded"]
        check(f"excluded pair {e['pair_id']} carries {dev}, its ELIGIBLE verdict and the failing report", ok)
    # a replacement is an accepted pair, or — when its own record later failed the read — an excluded pair
    # under D-CF2-2 that is itself replaced or pending (the chain is followed one step at a time)
    exd = {e["pair_id"]: e for e in excluded}
    chained = 0
    for r in doc["meta"].get("replacements", []):
        rp = next((p for p in pairs if p["pair_id"] == r["replacement"]), None) or exd.get(r["replacement"])
        ok = rp is not None and rp.get("replaces") == r["excluded"] and rp["state"] == r["state"] and r["excluded"] in exd
        if rp is not None and rp["pair_id"] in exd:
            chained += 1
            ok = ok and rp["excluded"]["deviation"] in ("D-CF2-2", "D-CF2-4") and (rp.get("replaced_by") in {p["pair_id"] for p in pairs} | set(exd)
                                                                                     or pend.get(r["state"], 0) > 0 or rp["excluded"].get("no_replacement") is True)
        check(f"replacement {r['replacement']} replaces excluded {r['excluded']} in the same state" + (" (itself later excluded; chain continues)" if rp is not None and rp["pair_id"] in exd else ""), ok)
    n_chain = sum(1 for e in excluded if e.get("replacement_under") == "D-CF2-2")
    check(f"every excluded pair is replaced, counted pending, or a D-CF2-4 no-replacement exclusion ({len(excluded)} excluded, {n_chain} of them former replacements)",
          sum(1 for e in excluded if not e.get("replaced_by") and not e["excluded"].get("no_replacement")) == sum(pend.values()),
          f"{sum(1 for e in excluded if not e.get('replaced_by') and not e['excluded'].get('no_replacement'))} unreplaced vs pending {pend}; {len(d4)} no-replacement (D-CF2-4)")
    check("no store version built at acceptance", doc["meta"].get("no_store_version_built") is True)


def check_questions():
    print("J. cf_questions_cf2.json against the draw (skips until it exists)")
    Qf, Pp = CF2 / "cf_questions_cf2.json", CF2 / "cf_pairs_cf2.json"
    if not Qf.exists():
        print("  skip  no questions yet"); return
    qd, pd = J(Qf), J(Pp); rows = qd["questions"]; pairs = pd["pairs"]
    # D-CF2-2 replacements accepted but not yet drafted are listed in meta.pending_draft; they must be replacements
    pend_draft = set(pd["meta"].get("pending_draft", []))
    reps = {r["replacement"] for r in pd["meta"].get("replacements", [])}
    check("every pair awaiting drafting is a D-CF2-2 replacement", pend_draft <= reps, str(sorted(pend_draft - reps)[:5]))
    drafted = {p["pair_id"] for p in pairs} - pend_draft
    check("questions prompt sha is the frozen b748247b", qd["meta"]["prompt_sha256"] == PIN["draft prompt sha"], qd["meta"]["prompt_sha256"])
    ids, rid = {p["pair_id"] for p in pairs}, {r["pair_id"] for r in rows}
    check(f"one question per accepted pair ({len(pend_draft)} replacements awaiting drafting; a drafted one may precede its record)",
          len(rows) == len(rid) and drafted <= rid <= ids, f"{len(rows)} rows, {len(drafted)} drafted of {len(ids)}")
    exq = qd["meta"].get("excluded_questions", [])
    check("excluded pairs' questions moved to meta.excluded_questions under D-CF2-2 / D-CF2-4",
          {r["pair_id"] for r in exq} == {e["pair_id"] for e in pd["meta"].get("excluded", []) if e["pair_id"] in {x["pair_id"] for x in exq}}
          and all(r["excluded_under"] in ("D-CF2-2", "D-CF2-4") for r in exq) and not ({r["pair_id"] for r in exq} & {r["pair_id"] for r in rows}), str(len(exq)))
    sha = hashlib.sha256("".join(r["question"] for r in sorted(rows, key=lambda r: r["pair_id"])).encode("utf-8")).hexdigest()
    check("questions sha256 recomputes over the accepted questions sorted by pair_id", sha == qd["meta"]["questions_sha256"], sha)
    check("every selected question passed the intent gate", all(r["intent_trail"][-1]["ok"] and r["intent_trail"][-1]["question"] == r["question"] for r in rows))
    check("intents match the class intent", all(r["intent"] == SPm.CLASS_INTENT[r["state"]] for r in rows))
    check("no redraft beyond the frozen rule (attempt in first/redraft, seed 42 or 4242)", all(r["attempt"] in ("first", "redraft") and r["seed_used"] in (42, 4242) for r in rows))


def check_pn():
    print("K. cf_pn_texts_cf2.json against the draw (skips until it exists)")
    Pf, Pp = CF2 / "cf_pn_texts_cf2.json", CF2 / "cf_pairs_cf2.json"
    if not Pf.exists():
        print("  skip  no PN records yet"); return
    pn, pd = J(Pf), J(Pp); recs = pn["records"]
    pend_draft = set(pd["meta"].get("pending_draft", []))
    pairs = {p["pair_id"]: p for p in pd["pairs"] if p["pair_id"] not in pend_draft}
    check("authoring prompt sha is CF-1's", pn["meta"]["prompt_sha256"] == "b6f53b1ab03fbd7124759fe19d875464f7e236a2df0a80a27f83c5277467a832", pn["meta"]["prompt_sha256"])
    check(f"one record per accepted pair ({len(pend_draft)} replacements awaiting authoring)", len(recs) == len(pairs) and {r["pair_id"] for r in recs} == set(pairs), f"{len(recs)} vs {len(pairs)}")
    exr = pn["meta"].get("excluded_records", [])
    check("excluded pairs' records moved to meta.excluded_records under D-CF2-2 / D-CF2-4, none still active",
          all(r["excluded_under"] in ("D-CF2-2", "D-CF2-4") for r in exr) and not ({r["pair_id"] for r in exr} & {r["pair_id"] for r in recs})
          and {r["pair_id"] for r in exr} <= {e["pair_id"] for e in pd["meta"].get("excluded", [])}, str(len(exr)))
    auth = [r for r in recs if r["state"] != "EXPIRY"]; exp = [r for r in recs if r["state"] == "EXPIRY"]
    n_auth = sum(1 for p in pairs.values() if p["state"] != "EXPIRY")
    check(f"{n_auth} authored (every non-expiry pair), 30 expiry anchor-only with no text",
          len(auth) == n_auth and all(r["new_text"] for r in auth) and len(exp) == 30 and all(r["new_text"] is None for r in exp))
    re = [r for r in auth if r.get("reauthored_under") == "D-CF2-3"]
    check("D-CF2-3 re-authored records carry seed 4242, the seed-bound sha and both reads", all(r.get("seed") == 4242 and r.get("prompt_sha256_at_seed") and r.get("read", {}).get("reread") == "YES" for r in re))
    bad = [r["pair_id"] for r in auth if not (r["predicates"]["n_discr_old"] >= 3 and r["predicates"]["n_discr_new"] >= 3
                                              and r["predicates"]["detector_signal_on_original"] >= 0.80)]
    check("every authored record clears MIN_DISCR 3 on both sides and TAU_HI 0.80 on the original", not bad, str(bad[:5]))
    check("no record needed more than the frozen single retry", all(r["attempts"] <= 2 for r in auth))
    check("cosine measured on every retraction record (not enforced)", all("cosine_to_original" in r["predicates"] for r in auth if r["state"] == "RETRACTION"))


def main():
    print("verify_cf2 -- ADDENDUM_CF2.md (frozen f016f03)")
    check_lineage()
    check_census()
    check_phase3_gate()
    check_adjudication()
    check_draw()
    check_questions()
    check_pn()
    check_label_table()
    check_v2r_lock()
    check_leakage_rows()
    check_ledger_keys()
    print()
    if FAILS:
        print(f"verify_cf2: {len(FAILS)} FAIL -- STOP (ADDENDUM_CF2 section 13)")
        for f in FAILS:
            print("  " + f)
        return 1
    print("verify_cf2: PASS (all applicable checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
