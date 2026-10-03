"""audit_ds.py -- forensic audit of the downstream (DS) pipeline, ds_downstream/ (registration ADDENDUM_DS.md
frozen a5a2036; Amendments 1-3). Plan: ~/.claude/plans/forensic-audit-of-the-abundant-bonbon.md.

READ-ONLY on every input. NO API CALLS (no OpenAI, no Anthropic, no embedding call over the network; the
MiniLM encoder of step 5 is the local sentence-transformers model the lookup gates already used, offline).
No subprocess, no git. Writes only reviews/downstream_audit/* and (step 8, later) reviews/DOWNSTREAM_AUDIT.md.

Gates first (abort on failure):
  detector   a verbatim replica of run_ds.records / score_answer reproduces every registered per-row score in
             scores_ds / scores_amend1 / scores_amend2 / scores_amend3 and every registered per-policy aggregate
  retrieval  LifecycleBank.cosine_search_all over the pinned vectors reproduces the ALWAYS top-5 and L2 top-10
  views      every view line parses; n_lines == len(ids); the text field equals the TRUE-flags entry text
  prompts    SYSTEM_ANSWER / USER_ANSWER digests as ledgered (AUX-DS-PROMPT); the A3 prompt as locked
Steps 1-7 of the brief follow; step 8 (verdicts) and the report are written after the author's read (cadence).

The 15 expiry obligations are UNSCORABLE for every stale diagnostic (the YAML gold field IS the expired fact,
so the gold string equals the stale string); the registered column is left as registered, the diagnostic
columns run on the scorable (supersession + retraction) reached set.

Never import run_ds / amend* (module-level API object), run_cf (module-level asserts) or build_l2.
"""
from __future__ import annotations

import argparse
import collections
import copy
import datetime as dt
import hashlib
import io
import json
import math
import os
import pathlib
import re
import sys
import unicodedata

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np                                                            # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                                             # noqa: BLE001
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
DS, RUN = ROOT / "ds_downstream", ROOT / "ds_downstream" / "run"
OUT = ROOT / "reviews" / "downstream_audit"
REPORT = ROOT / "reviews" / "DOWNSTREAM_AUDIT.md"
L2 = ROOT / "resp_review" / "l2"
BANKS = ROOT / "LifeMemEval" / "artifacts" / "lifecycle_banks"

sys.path.insert(0, str(DS / "tools"))
import ds_common as DC                                                        # noqa: E402  (no API; inserts the tool paths)
import prompts_ds as PD                                                       # noqa: E402
from e0_common import load_joins, toks, cov, SECTION_FIELDS, MIN_SHARED, MIN_DISCR, CROSS_GUARD, TAU_GOLD   # noqa: E402
from index_v2 import detect, TAU_HI                                           # noqa: E402
sys.path.insert(0, str(ROOT))
import lifecycle_bank as LB                                                   # noqa: E402

ABST = "The store does not currently contain the answer."
POLICIES7 = list(DC.POLICIES)
STAGE2 = list(DC.STAGE2_POLICIES)
K_TAKE, K_USE = 10, 5
TAUS_EMB = (0.80, 0.90, 0.95)

# the A3 prompt exactly as amend3_instruct.py builds it (replicated; that module constructs the API object on import)
ADDED = ("Treat every entry tagged superseded, retracted or expired as not to be used: do not draw on it for the answer and do not "
         "report it as the user's current situation. If the only entries that bear on the question carry one of those tags, say that "
         "the store does not currently contain the answer.")
TAIL = "Return JSON only: {\"answer\": \"<your answer>\"}"
assert PD.SYSTEM_ANSWER.endswith(TAIL)
SYSTEM_ANSWER_A3 = PD.SYSTEM_ANSWER[:-len(TAIL)] + ADDED + "\n\n" + TAIL

LINE_RE = re.compile(r"^\[(\d+)\] lifecycle: (.*?) \| category: (.*?) \| attribute: (.*?) \| age: (.*?) \| text: (.*)$")
SENT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")
SUPERSEDE_RE = re.compile(r"\b(cancel\w*|scrapp\w*|no longer|dropped|off the table|however|but\b|previously|formerly|was planning|"
                          r"had planned|withdrawn|retract\w*|supersed\w*|expired|already passed|not current|used to|earlier|"
                          r"instead|though|although|originally|initially|past\b|old\b|replaced|changed|switched|moved)", re.I)
TIME_RE = re.compile(r"\b(today|now|current date|as of|\d{4}-\d{2}-\d{2}|t_now|pinned)\b", re.I)


# ------------------------------------------------------------------ io helpers
def J(p):
    return json.load(io.open(p, encoding="utf-8"))


def jl(p):
    return [json.loads(l) for l in io.open(p, encoding="utf-8") if l.strip()]


def _default(x):
    if isinstance(x, np.floating):
        return float(x)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, (set, frozenset)):
        return sorted(x)
    if isinstance(x, np.ndarray):
        return x.tolist()
    raise TypeError(type(x))


def jdump(o, p):
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(o, indent=1, sort_keys=True, ensure_ascii=False, default=_default) + "\n")


def wtext(p, s):
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def sha_t(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha_f(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def wilson(k, n, z=1.959964):
    if not n:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 4), round(c + h, 4)]


def rate(k, n):
    return {"k": int(k), "n": int(n), "rate": (round(k / n, 4) if n else None), "wilson": wilson(k, n)}


def r4(x):
    return None if x is None else round(float(x), 4)


def quart(xs):
    xs = [float(x) for x in xs]
    if not xs:
        return {"n": 0}
    a = np.asarray(xs)
    return {"n": len(xs), "median": r4(np.median(a)), "q25": r4(np.percentile(a, 25)), "q75": r4(np.percentile(a, 75)),
            "mean": r4(a.mean()), "min": r4(a.min()), "max": r4(a.max())}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def is_abst(answer):
    a = norm(answer)
    return a.startswith("the store does not currently contain") or a == norm(ABST) or ("store does not currently contain the answer" in a)


def sentences(s):
    s = (s or "").strip()
    return [x for x in SENT_RE.split(s) if x] if s else []


# ------------------------------------------------------------------ replicas (verbatim; never "improved")
def records(sub):
    """run_ds.py:204-217 -- per item: the YAML record's stale / successor / gold fields and the persona drop set."""
    joins = load_joins(); out = {}
    for it in sub:
        if it["label"] == "ABSENT":
            continue
        Jp = joins[it["persona"]]; qid = it["question_id"]
        if qid not in Jp.rec_of or Jp.rec_of[qid] is None:
            out[it["item_id"]] = None; continue
        sec, ridx = Jp.rec_of[qid]
        rec = [r for r in (Jp.y.get(sec) or []) if isinstance(r, dict)][ridx]
        gf, gs, sf, ss = SECTION_FIELDS[sec]
        out[it["item_id"]] = {"section": sec, "gold_field": rec.get(gf), "stale_field": rec.get(sf) if sf else None, "drop": Jp.drop}
    return out


def score_answer(it, rec, text):
    """run_ds.py:220-244 -- section D.4: the committed detector on the answer as the one text."""
    A = toks(text or "", rec["drop"])
    return score_tokens(it, rec, A)


def score_tokens(it, rec, A):
    """score_answer's body on a pre-built token set (identical output; asserted in the detector gate)."""
    out = {}
    if it["label"] == "PRESENT-NEGATIVE":
        if rec["section"] == "expiring_logistics":
            ft = toks(rec["gold_field"], rec["drop"])
            c = cov(ft, A); shared = len(ft & A) >= MIN_SHARED
            out.update({"stale_use": bool(shared and c >= TAU_HI), "stale_surface": bool(shared and c >= TAU_HI), "stale_cov": c,
                        "stale_use_tau_gold": bool(shared and c >= TAU_GOLD), "successor_use": None, "both": None})
        else:
            old, new = rec["stale_field"], rec["gold_field"]
            d_old = detect(old, new, {"a": A}, rec["drop"]); d_new = detect(new, old, {"a": A}, rec["drop"])
            ot, nt = toks(old, rec["drop"]), toks(new, rec["drop"]); do, dn = ot - nt, nt - ot
            c_old, c_new = cov(do, A), cov(dn, A)
            out.update({"stale_use": bool(d_old is not None and d_old.get("a", 0.0) >= TAU_HI),
                        "stale_surface": bool(len(do & A) >= MIN_SHARED and c_old >= TAU_HI), "stale_cov": c_old,
                        "stale_use_tau_gold": bool(d_old is not None and d_old.get("a", 0.0) >= TAU_GOLD),
                        "successor_use": (bool(d_new is not None and d_new.get("a", 0.0) >= TAU_HI) if rec["section"] == "supersession_events" else None),
                        "successor_cov": c_new,
                        "both": bool(c_old >= TAU_HI and c_new >= TAU_HI and len(do & A) >= MIN_SHARED and len(dn & A) >= MIN_SHARED)})
    else:
        gt = toks(rec["gold_field"], rec["drop"]); c = cov(gt, A); shared = len(gt & A) >= MIN_SHARED
        out.update({"correct": bool(shared and c >= TAU_GOLD), "correct_tau_hi": bool(shared and c >= TAU_HI), "gold_cov": c})
    return out


def parse_json(content):
    """e0_metamemory/tools/api.py:132-145 -- tolerant JSON extraction (the mini lane)."""
    if not content:
        return None
    try:
        return json.loads(content)
    except Exception:                                                         # noqa: BLE001
        i, j = content.find("{"), content.rfind("}")
        if i >= 0 and j > i:
            try:
                return json.loads(content[i:j + 1])
            except Exception:                                                 # noqa: BLE001
                return None
        return None


def last_json(text):
    """r82_counterfactual/tools/run_cf.py:81-101 -- the last top-level {...} of the reply (the Haiku lane)."""
    depth, start, best, ins, esc = 0, None, None, False, False
    for i, ch in enumerate(text or ""):
        if ins:
            ins = not (ch == '"' and not esc)
            esc = (ch == "\\" and not esc)
            continue
        if ch == '"':
            ins, esc = True, False
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None:
                best = text[start:i + 1]
    try:
        return json.loads(best) if best else None
    except Exception:                                                         # noqa: BLE001
        return None


_BANKS = {}


def bank_for(it):
    """resp_review/tools/build_l2.py:96-106 -- the persona's bank restricted to the item's store variant."""
    name = it["persona"]
    if name not in _BANKS:
        _BANKS[name] = LB.LifecycleBank.load(BANKS / f"{name}.json")
    b = _BANKS[name]
    ids = set(DC.variant_ids(it))
    vb = copy.copy(b)
    vb.entries = {k: v for k, v in b.entries.items() if k in ids}
    assert len(vb.entries) == len(ids)
    return vb


def load_question_vectors():
    """build_l2.py:90-92."""
    z = np.load(L2 / "question_emb.npz", allow_pickle=True)
    return {str(q): v for q, v in zip(z["questions"], z["embeddings"])}


def registered_added():
    """amend3_instruct.py:68-72 -- the added paragraph as the frozen amendment prints it."""
    s = (ROOT / "registrations" / "ADDENDUM_DS_AMENDMENT_3.md").read_text(encoding="utf-8")
    i = s.index("verbatim:\n\n```\n") + len("verbatim:\n\n```\n"); j = s.index("\n```\n", i)
    return s[i:j]


# ------------------------------------------------------------------ context and lanes
class Lane:
    def __init__(self, lid, model, prompt, rows, reg, polmap, tagged, rows_file, reg_file):
        self.id, self.model, self.prompt, self.rows, self.reg, self.polmap, self.tagged = lid, model, prompt, rows, reg, polmap, tagged
        self.rows_file, self.reg_file = rows_file, reg_file

    def policies_of(self, key):
        return self.polmap[key]


def build_lanes(C):
    rows_ds = {r["key"]: r for r in jl(RUN / "rows_ds.jsonl")}
    sd, s1, s2, s3 = J(RUN / "scores_ds.json"), J(RUN / "scores_amend1.json"), J(RUN / "scores_amend2.json"), J(RUN / "scores_amend3.json")
    C.reg_tables = {"scores_ds": sd, "scores_amend1": s1, "scores_amend2": s2, "scores_amend3": s3}
    tag7 = lambda k, p, item: C.st1[item][p]["tagged_reach"]                 # noqa: E731
    tag_v3 = lambda k, p, item: C.st1_v3[item]["tagged_reach"]               # noqa: E731

    rows, reg, polmap = dict(rows_ds), dict(sd["per_row"]), {k: set(r["policies"]) for k, r in rows_ds.items()}
    C.amend2_reuse = {"reused": 0, "answer_mismatch": [], "score_mismatch": [], "new": 0}
    for r in jl(RUN / "rows_ds_amend2.jsonl"):
        k = r["key"]
        if r.get("source") == "amend2 call":
            rows[k] = r; reg[k] = s2["per_row_mini"][k]; polmap.setdefault(k, set()).add("LOOKUP-LIT"); C.amend2_reuse["new"] += 1
        else:
            C.amend2_reuse["reused"] += 1
            if rows_ds[k]["answer"] != r["answer"]:
                C.amend2_reuse["answer_mismatch"].append(k)
            a = {kk: v for kk, v in sd["per_row"][k].items() if kk not in ("policies",)}
            b = {kk: v for kk, v in s2["per_row_mini"][k].items() if kk not in ("policies",)}
            if a != b:
                C.amend2_reuse["score_mismatch"].append(k)
            polmap[k].add("LOOKUP-LIT")
    lanes = {"mini-D4": Lane("mini-D4", "gpt-4.1-mini", "D4", rows, reg, polmap, tag7, "run/rows_ds.jsonl + run/rows_ds_amend2.jsonl (new)",
                             "scores_ds.per_row + scores_amend2.per_row_mini")}
    h = {r["key"]: r for r in jl(RUN / "rows_ds_amend2_h45.jsonl")}
    lanes["h45-D4"] = Lane("h45-D4", "claude-haiku-4-5-20251001", "D4", h, s2["per_row_h45"], {k: set(r["policies"]) for k, r in h.items()}, tag7,
                           "run/rows_ds_amend2_h45.jsonl", "scores_amend2.per_row_h45")
    m3 = {r["key"]: r for r in jl(RUN / "rows_ds_amend3_mini.jsonl")}
    lanes["mini-A3"] = Lane("mini-A3", "gpt-4.1-mini", "A3", m3, s3["per_row"]["MINI"], {k: set(r["policies"]) for k, r in m3.items()}, tag7,
                            "run/rows_ds_amend3_mini.jsonl", "scores_amend3.per_row.MINI")
    h3 = {r["key"]: r for r in jl(RUN / "rows_ds_amend3_h45.jsonl")}
    lanes["h45-A3"] = Lane("h45-A3", "claude-haiku-4-5-20251001", "A3", h3, s3["per_row"]["H45"], {k: set(r["policies"]) for k, r in h3.items()}, tag7,
                           "run/rows_ds_amend3_h45.jsonl", "scores_amend3.per_row.H45")
    v3 = {r["key"]: r for r in jl(RUN / "rows_ds_amend1.jsonl")}
    lanes["mini-D4-V3"] = Lane("mini-D4-V3", "gpt-4.1-mini", "D4", v3, s1["per_row"], {k: {"MODEL-ALL-V3"} for k in v3}, tag_v3,
                               "run/rows_ds_amend1.jsonl", "scores_amend1.per_row")
    return lanes


def lane_policies(L):
    return ["MODEL-ALL-V3"] if L.id == "mini-D4-V3" else POLICIES7


class Ctx:
    pass


def load_ctx():
    C = Ctx()
    C.sub = DC.load_cell(); C.byid = {it["item_id"]: it for it in C.sub}
    C.rec = records(C.sub)
    C.fl = DC.true_flags()
    C.views = J(DS / "views.json")["items"]; C.pol = J(DS / "policies.json")["items"]; C.st1 = J(DS / "stage1.json")["per_item"]
    C.st1_v3 = J(RUN / "stage1_amend1.json")["per_item"]
    C.cell = J(RUN / "cell_ds.json")
    C.R = J(L2 / "retrieval.json")["items"]
    C.view_by_key = {}
    for iid, d in C.views.items():
        for p, v in d.items():
            e = C.view_by_key.setdefault(f"{iid}|{v['sha']}", {"item_id": iid, "policies": set(), "text": v["text"], "ids": v["ids"], "sha": v["sha"]})
            e["policies"].add(p)
    C.lanes = build_lanes(C)
    C.pn = [it for it in C.sub if it["label"] == "PRESENT-NEGATIVE"]
    C.present = [it for it in C.sub if it["label"] == "PRESENT"]
    C.exp_ids = {it["item_id"] for it in C.pn if it["state"] == "exp"}
    C.scorable = lambda key, L: C.byid[L.rows[key]["item_id"]]["state"] != "exp"    # noqa: E731
    C.checks = []
    return C


def check(C, ok, msg):
    C.checks.append({"ok": bool(ok), "check": msg}); print(("PASS  " if ok else "FAIL  ") + msg)
    return bool(ok)


# ------------------------------------------------------------------ the aggregation primitive
def agg(C, L, policy, label, flag, flags=None, pred=None, keys=None):
    """Count over rows carrying `policy` in their policies list (one row may serve several policies)."""
    sel = [k for k, r in L.rows.items() if policy in L.policies_of(k) and r["label"] == label
           and (pred is None or pred(k)) and (keys is None or k in keys)]
    src = flags if flags is not None else L.reg
    return rate(sum(1 for k in sel if (src.get(k) or {}).get(flag)), len(sel))


def pn_pred(C, L, split, p):
    if split == "all":
        return None
    if split == "tagged":
        return lambda k: L.tagged(k, p, L.rows[k]["item_id"])
    if split == "untagged":
        return lambda k: not L.tagged(k, p, L.rows[k]["item_id"])
    if split in ("sup", "ret", "exp"):
        return lambda k: C.byid[L.rows[k]["item_id"]]["state"] == split
    raise KeyError(split)


def tagged_of(C, L, k, p):
    return L.tagged(k, p, L.rows[k]["item_id"])


def same(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if a is None or b is None:
        return a is b
    if isinstance(a, float) or isinstance(b, float):
        return abs(float(a) - float(b)) <= 1e-9
    return a == b


# ------------------------------------------------------------------ gates
def gate_detector(C):
    out = {"lanes": {}, "aggregates": {}, "records_none": [k for k, v in C.rec.items() if v is None], "amend2_reuse": C.amend2_reuse}
    total_rows = total_mism = 0
    for lid, L in C.lanes.items():
        mism, n = [], 0
        for k, r in L.rows.items():
            it = C.byid[r["item_id"]]; rec = C.rec.get(r["item_id"])
            if rec is None:
                mism.append({"key": k, "field": "records", "replica": None}); continue
            rep = score_answer(it, rec, r["answer"])
            regd = {kk: v for kk, v in L.reg[k].items() if kk not in ("status", "policies", "scored")}
            if set(rep) != set(regd):
                mism.append({"key": k, "field": "keys", "replica": sorted(rep), "registered": sorted(regd)}); continue
            for f in rep:
                if not same(rep[f], regd[f]):
                    mism.append({"key": k, "field": f, "replica": rep[f], "registered": regd[f]})
            if score_tokens(it, rec, toks(r["answer"] or "", rec["drop"])) != rep:
                mism.append({"key": k, "field": "score_tokens"})
            n += 1
        out["lanes"][lid] = {"rows_file": L.rows_file, "reg_file": L.reg_file, "n_rows": len(L.rows), "n_compared": n, "n_mismatch": len(mism), "mismatches": mism[:50]}
        total_rows += len(L.rows); total_mism += len(mism)
    # registered per-policy aggregates
    T = C.reg_tables
    reg_tab = {"mini-D4": {**{p: T["scores_ds"]["per_policy"][p] for p in STAGE2}, "LOOKUP-LIT": T["scores_amend2"]["stage2_lit_mini"]},
               "h45-D4": T["scores_amend2"]["stage2_h45"],
               "mini-A3": {p: T["scores_amend3"]["stage2"]["MINI"][p] for p in POLICIES7},
               "h45-A3": {p: T["scores_amend3"]["stage2"]["H45"][p] for p in POLICIES7},
               "mini-D4-V3": {"MODEL-ALL-V3": T["scores_amend1"]["stage2"]}}
    n_agg = n_bad = 0; bad = []
    for lid, L in C.lanes.items():
        out["aggregates"][lid] = {}
        for p in lane_policies(L):
            R = reg_tab[lid][p]; mine = {}
            for split in ("all", "tagged", "untagged"):
                pr = pn_pred(C, L, split, p)
                blk = {"n": agg(C, L, p, "PRESENT-NEGATIVE", "stale_use", pred=pr)["n"]}
                for f in ("stale_use", "stale_use_tau_gold", "stale_surface", "successor_use", "both"):
                    blk[f] = agg(C, L, p, "PRESENT-NEGATIVE", f, pred=pr)["k"]
                mine[f"pn_{split}"] = blk
            for st in ("sup", "ret", "exp"):
                pr = pn_pred(C, L, st, p)
                mine[f"pn_state_{st}"] = {"n": agg(C, L, p, "PRESENT-NEGATIVE", "stale_use", pred=pr)["n"],
                                         "stale_use": agg(C, L, p, "PRESENT-NEGATIVE", "stale_use", pred=pr)["k"],
                                         "stale_use_tau_gold": agg(C, L, p, "PRESENT-NEGATIVE", "stale_use_tau_gold", pred=pr)["k"]}
            mine["present"] = {"n": agg(C, L, p, "PRESENT", "correct")["n"], "correct": agg(C, L, p, "PRESENT", "correct")["k"],
                               "correct_tau_hi": agg(C, L, p, "PRESENT", "correct_tau_hi")["k"]}
            diffs = []
            for blk, d in mine.items():
                if blk not in R:
                    continue
                for f, v in d.items():
                    if f in R[blk] and isinstance(R[blk][f], (int, float)) and not isinstance(R[blk][f], bool):
                        n_agg += 1
                        if int(R[blk][f]) != int(v):
                            diffs.append({"block": blk, "field": f, "replica": v, "registered": R[blk][f]}); n_bad += 1
            out["aggregates"][lid][p] = {"replica": mine, "diffs": diffs}
            if diffs:
                bad.append((lid, p))
    out["summary"] = {"rows_total": total_rows, "row_mismatches": total_mism, "aggregate_cells": n_agg, "aggregate_mismatches": n_bad,
                      "aggregate_bad": bad}
    ok = total_mism == 0 and n_bad == 0 and not out["records_none"] and not C.amend2_reuse["answer_mismatch"] and not C.amend2_reuse["score_mismatch"]
    check(C, ok, f"detector replica: {total_mism} row mismatches over {total_rows} rows; {n_bad} of {n_agg} aggregate cells differ; "
                 f"records None {len(out['records_none'])}; amend2 reuse mismatches {len(C.amend2_reuse['answer_mismatch'])}/{len(C.amend2_reuse['score_mismatch'])}")
    out["ok"] = ok
    jdump(out, OUT / "gate_detector.json")
    return ok


def gate_retrieval(C):
    qvec = load_question_vectors()
    C.ranks, bad, sizes, n_ok = {}, [], [], 0
    for it in C.sub:
        qv = qvec[it["question"]]
        vb = bank_for(it)
        top = vb.cosine_search_all(np.asarray(qv, np.float32), k=len(vb.entries))
        ids = [e.id for e, _ in top]; cs = [float(s) for _, s in top]
        R = C.R[it["item_id"]]
        ok5 = ids[:K_USE] == C.views[it["item_id"]]["ALWAYS"]["ids"]
        ok10 = ids[:K_TAKE] == R["top10_ids"] and all(abs(a - b) <= 1e-5 for a, b in zip(cs[:K_TAKE], R["top10_cos"]))
        if ok5 and ok10:
            n_ok += 1
        else:
            bad.append({"item_id": it["item_id"], "ok5": ok5, "ok10": ok10})
        C.ranks[it["item_id"]] = {e: (r + 1, c) for r, (e, c) in enumerate(zip(ids, cs))}
        sizes.append(len(ids))
    out = {"n_items": len(C.sub), "n_ok": n_ok, "bad": bad, "store_size": {"min": min(sizes), "max": max(sizes)},
           "config": {"retriever": "LifecycleBank.cosine_search_all (lifecycle_bank.py:402-414) over the item's store variant (resp_common.variant_ids), every entry active or not",
                      "lifecycle_mask": "none (unmasked; TRUE lifecycle metadata printed on every line)",
                      "query": "the item's question text, embedded once with text-embedding-3-small (1536-d), pinned in resp_review/l2/question_emb.npz",
                      "question_matrix_sha256": sha_f(L2 / "question_emb.npz"), "bank_vectors": "LifeMemEval/artifacts/lifecycle_banks/<persona>_embeddings.npz",
                      "k_take": K_TAKE, "k_use": K_USE, "ranking": "np.argsort(-cosine) (non-stable; ties beyond rank 10 could permute; the gate covers ranks 1-10)"}}
    ok = check(C, n_ok == len(C.sub), f"retrieval replay: top-5 == ALWAYS ids and top-10 == L2 for {n_ok}/{len(C.sub)} items")
    out["ok"] = ok
    jdump(out, OUT / "gate_retrieval.json")
    return ok


def parse_view(text):
    out = []
    for ln in (text.split("\n") if text else []):
        m = LINE_RE.match(ln)
        out.append(None if not m else {"rank": int(m.group(1)), "tag": m.group(2), "cat": m.group(3), "slot": m.group(4), "age": m.group(5), "text": m.group(6)})
    return out


def gate_views(C):
    C.parsed = {}
    n_lines = n_bad_parse = n_bad_len = n_bad_lock = 0; tags = collections.Counter(); ages_unknown = 0; plus_frag = 0
    for iid, d in C.views.items():
        for p, v in d.items():
            P = parse_view(v["text"]); C.parsed[(iid, p)] = P
            n_lines += len(P)
            if any(x is None for x in P):
                n_bad_parse += 1; continue
            if not (len(P) == len(v["ids"]) == v["n_lines"]):
                n_bad_len += 1
            fl = C.fl[C.byid[iid]["persona"]]
            for x, e in zip(P, v["ids"]):
                tags[x["tag"]] += 1
                if x["text"] != fl[e]["text"]:
                    n_bad_lock += 1
                if x["age"] == "unknown":
                    ages_unknown += 1
                if "(+" in x["text"] and "more)" in x["text"]:
                    plus_frag += 1
    pres_same = sum(1 for it in C.present if C.views[it["item_id"]]["ORACLE"]["sha"] == C.views[it["item_id"]]["ALWAYS"]["sha"])
    differ = {p: sum(1 for it in C.present if C.views[it["item_id"]][p]["sha"] != C.views[it["item_id"]]["ALWAYS"]["sha"]) for p in POLICIES7}
    out = {"n_views": len(C.parsed), "n_lines": n_lines, "bad_parse": n_bad_parse, "bad_len": n_bad_len, "render_lock_failures": n_bad_lock,
           "tag_vocabulary": dict(tags), "age_unknown": ages_unknown, "plus_more_fragments": plus_frag,
           "present_view_identity": {"oracle_sha_equals_always": pres_same, "n_present": len(C.present), "present_views_differing_from_always_by_policy": differ}}
    ok = check(C, n_bad_parse == 0 and n_bad_len == 0 and n_bad_lock == 0, f"views: {n_lines} lines parse, lengths agree, render lock holds ({n_bad_parse}/{n_bad_len}/{n_bad_lock} failures)")
    ok &= check(C, pres_same == len(C.present), f"PRESENT view identity: ORACLE sha == ALWAYS sha for {pres_same}/{len(C.present)} PRESENT items (by construction)")
    out["ok"] = bool(ok)
    jdump(out, OUT / "gate_views.json")
    return ok


def gate_prompts(C):
    lock3 = J(RUN / "lock_amend3.json"); lock2 = J(RUN / "lock_amend2.json")
    d = PD.digests()
    reg = PD.from_registration(ROOT / "registrations" / "ADDENDUM_DS.md")
    out = {"SYSTEM_ANSWER": d["SYSTEM_ANSWER"], "USER_ANSWER": d["USER_ANSWER"], "locked": lock2["prompts_ds"],
           "registration_equal": reg == PD.TEXTS, "SYSTEM_ANSWER_A3": sha_t(SYSTEM_ANSWER_A3), "locked_a3": lock3["system_answer_a3_sha256"],
           "ADDED": sha_t(ADDED), "locked_added": lock3["added_paragraph_sha256"], "added_equals_registration": registered_added() == ADDED}
    ok = (d == lock2["prompts_ds"] and out["registration_equal"] and out["SYSTEM_ANSWER_A3"] == out["locked_a3"] and out["ADDED"] == out["locked_added"]
          and out["added_equals_registration"])
    check(C, ok, f"prompts: SYSTEM_ANSWER {d['SYSTEM_ANSWER'][:8]}, USER_ANSWER {d['USER_ANSWER'][:8]} as ledgered; A3 {out['SYSTEM_ANSWER_A3'][:8]} as locked")
    out["ok"] = ok
    jdump(out, OUT / "gate_prompts.json")
    return ok


# ------------------------------------------------------------------ step 1
def why_pn(rec, A):
    ot, nt = toks(rec["stale_field"], rec["drop"]), toks(rec["gold_field"], rec["drop"]); do, dn = ot - nt, nt - ot
    return {"section": rec["section"], "n_do": len(do), "n_dn": len(dn), "matched_do": sorted(do & A), "missing_do": sorted(do - A),
            "cov_do": r4(cov(do, A)), "matched_dn": sorted(dn & A), "cov_dn": r4(cov(dn, A)), "structurally_none": len(do) < MIN_DISCR or len(dn) < MIN_DISCR}


def why_present(rec, A):
    gt = toks(rec["gold_field"], rec["drop"])
    return {"section": rec["section"], "n_gold": len(gt), "matched": sorted(gt & A), "missing": sorted(gt - A), "cov": r4(cov(gt, A))}


def step1(C):
    cnt = collections.Counter(); fails = []; unscorable = []; info = collections.Counter()
    B = {"present": {"n_with_gold": 0, "any_pass": 0, "all_pass": 0, "no_pass": [], "partial": [], "no_licensed_id": [], "line_with_metadata_flips": 0},
         "pn": {"n_scorable": 0, "any_tg": 0, "all_tg": 0, "any_hi": 0, "all_hi": 0, "none_tg": [], "partial_tg": [], "successor_text_fires": [],
                "line_with_metadata_flips": 0, "n_successor_texts": 0}}
    for it in C.sub:
        iid = it["item_id"]
        if it["label"] == "ABSENT":
            continue
        rec = C.rec[iid]; fl = C.fl[it["persona"]]
        if it["label"] == "PRESENT":
            g = score_answer(it, rec, rec["gold_field"]); a = score_answer(it, rec, ABST)
            cnt["present.gold->correct"] += g["correct"]; cnt["present.abst->correct"] += a["correct"]; cnt["present.n"] += 1
            if not g["correct"]:
                fails.append({"item_id": iid, "panel": "A", "input": "gold", "expected": "correct True", "got": g, "why": why_present(rec, toks(rec["gold_field"], rec["drop"]))})
            if a["correct"]:
                fails.append({"item_id": iid, "panel": "A", "input": "abstention", "expected": "correct False", "got": a, "why": why_present(rec, toks(ABST, rec["drop"]))})
            if rec["stale_field"]:
                info["present.has_old_fact"] += 1
                info["present.old_fact->correct"] += score_answer(it, rec, rec["stale_field"])["correct"]
            # panel B: the rendered entry texts of the licensed records
            if not it["gold"]:
                B["present"]["no_licensed_id"].append({"item_id": iid, "section": rec["section"], "gold_field": rec["gold_field"]}); continue
            B["present"]["n_with_gold"] += 1
            res = {e: score_answer(it, rec, fl[e]["text"]) for e in it["gold"]}
            ok = [e for e, s in res.items() if s["correct"]]
            B["present"]["any_pass"] += bool(ok); B["present"]["all_pass"] += (len(ok) == len(res))
            if not ok:
                B["present"]["no_pass"].append({"item_id": iid, "gold_field": rec["gold_field"], "entries": {e: {"text": fl[e]["text"], **why_present(rec, toks(fl[e]["text"], rec["drop"]))} for e in it["gold"]}})
            elif len(ok) < len(res):
                B["present"]["partial"].append({"item_id": iid, "gold_field": rec["gold_field"], "failing": {e: {"text": fl[e]["text"], **why_present(rec, toks(fl[e]["text"], rec["drop"]))} for e in it["gold"] if e not in ok}})
            for e in it["gold"]:
                if score_answer(it, rec, DC.render_line(1, fl[e]))["correct"] != res[e]["correct"]:
                    B["present"]["line_with_metadata_flips"] += 1
        else:
            if it["state"] == "exp":
                unscorable.append({"item_id": iid, "reason": "expiring_logistics: SECTION_FIELDS gold field is the expired fact itself; gold string == stale string; correct behaviour is abstention",
                                   "gold_field": rec["gold_field"]}); cnt["pn.unscorable_expiry"] += 1; continue
            cnt["pn.n_scorable"] += 1
            s = score_answer(it, rec, rec["stale_field"]); g = score_answer(it, rec, rec["gold_field"]); a = score_answer(it, rec, ABST)
            cnt["pn.stale->stale_tg"] += s["stale_use_tau_gold"]; cnt["pn.stale->stale_hi"] += s["stale_use"]
            cnt["pn.gold->stale_tg"] += g["stale_use_tau_gold"]; cnt["pn.abst->stale_tg"] += a["stale_use_tau_gold"]
            cnt["pn.abst->any_flag"] += any(bool(v) for k, v in a.items() if isinstance(v, bool))
            if not s["stale_use_tau_gold"] or not s["stale_use"]:
                fails.append({"item_id": iid, "panel": "A", "input": "stale", "expected": "stale True at both thresholds", "got": s, "why": why_pn(rec, toks(rec["stale_field"], rec["drop"]))})
            if g["stale_use_tau_gold"]:
                fails.append({"item_id": iid, "panel": "A", "input": "gold", "expected": "stale False", "got": g, "why": why_pn(rec, toks(rec["gold_field"], rec["drop"]))})
            if any(bool(v) for k, v in a.items() if isinstance(v, bool)):
                fails.append({"item_id": iid, "panel": "A", "input": "abstention", "expected": "all flags False", "got": a, "why": why_pn(rec, toks(ABST, rec["drop"]))})
            # panel B
            B["pn"]["n_scorable"] += 1
            res = {e: score_answer(it, rec, fl[e]["text"]) for e in (it.get("pn_members") or [])}
            tg = [e for e, s2 in res.items() if s2["stale_use_tau_gold"]]; hi = [e for e, s2 in res.items() if s2["stale_use"]]
            B["pn"]["any_tg"] += bool(tg); B["pn"]["all_tg"] += (len(tg) == len(res) and bool(res)); B["pn"]["any_hi"] += bool(hi); B["pn"]["all_hi"] += (len(hi) == len(res) and bool(res))
            if not tg:
                B["pn"]["none_tg"].append({"item_id": iid, "state": it["state"], "stale_field": rec["stale_field"], "gold_field": rec["gold_field"],
                                           "entries": {e: {"text": fl[e]["text"], "tag": DC.lifecycle_tag(fl[e]), **why_pn(rec, toks(fl[e]["text"], rec["drop"]))} for e in res}})
            elif len(tg) < len(res):
                B["pn"]["partial_tg"].append({"item_id": iid, "state": it["state"], "failing": {e: {"text": fl[e]["text"], "tag": DC.lifecycle_tag(fl[e]), **why_pn(rec, toks(fl[e]["text"], rec["drop"]))} for e in res if e not in tg}})
            for e in res:
                if score_answer(it, rec, DC.render_line(1, fl[e]))["stale_use_tau_gold"] != res[e]["stale_use_tau_gold"]:
                    B["pn"]["line_with_metadata_flips"] += 1
            for e in it["gold"]:
                B["pn"]["n_successor_texts"] += 1
                s3 = score_answer(it, rec, fl[e]["text"])
                if s3["stale_use_tau_gold"]:
                    B["pn"]["successor_text_fires"].append({"item_id": iid, "state": it["state"], "entry": e, "text": fl[e]["text"], **why_pn(rec, toks(fl[e]["text"], rec["drop"]))})
    out = {"abstention_string": ABST, "panel_a": {"counts": dict(cnt), "informational": dict(info),
                                                  "expected": {"present.gold->correct": "174 of 174", "present.abst->correct": "0", "pn.stale->stale_tg": "89 of 89 scorable (104 minus 15 unscorable expiry)",
                                                               "pn.gold->stale_tg": "0", "pn.abst->any_flag": "0"},
                                                  "failures": fails, "unscorable_expiry": unscorable},
           "panel_b": B,
           "note": "Panel A feeds the YAML strings the detector uses as reference; Panel B feeds the rendered entry texts the model can actually echo from the view."}
    check(C, cnt["present.gold->correct"] == cnt["present.n"] and cnt["present.abst->correct"] == 0 and cnt["pn.stale->stale_tg"] == cnt["pn.n_scorable"]
          and cnt["pn.stale->stale_hi"] == cnt["pn.n_scorable"] and cnt["pn.gold->stale_tg"] == 0 and cnt["pn.abst->any_flag"] == 0,
          f"step 1A: gold->correct {cnt['present.gold->correct']}/{cnt['present.n']}, abst->correct {cnt['present.abst->correct']}, stale->stale {cnt['pn.stale->stale_tg']}/{cnt['pn.n_scorable']} "
          f"(TAU_HI {cnt['pn.stale->stale_hi']}), gold->stale {cnt['pn.gold->stale_tg']}, abst->flag {cnt['pn.abst->any_flag']}; unscorable expiry {cnt['pn.unscorable_expiry']}")
    print(f"      step 1B: PRESENT any gold entry text correct {B['present']['any_pass']}/{B['present']['n_with_gold']} (all {B['present']['all_pass']}; no licensed id {len(B['present']['no_licensed_id'])}); "
          f"PN any member text fires {B['pn']['any_tg']}/{B['pn']['n_scorable']} at TAU_GOLD, {B['pn']['any_hi']} at TAU_HI; successor texts firing {len(B['pn']['successor_text_fires'])}/{B['pn']['n_successor_texts']}")
    jdump(out, OUT / "step1_synthetic.json")
    C.step1 = out
    return out


# ------------------------------------------------------------------ step 2
def step2(C):
    per = {}
    for it in C.pn:
        iid = it["item_id"]; rec = C.rec[iid]
        if it["state"] == "exp":
            per[iid] = {"state": "exp", "overlap": None, "unscorable": True, "reason": "no distinct successor string (gold field is the expired fact)"}; continue
        ot, nt = toks(rec["stale_field"], rec["drop"]), toks(rec["gold_field"], rec["drop"]); do, dn = ot - nt, nt - ot; sh = ot & nt
        q = toks(it["question"], rec["drop"]); qd = q & do
        mtg, mhi = max(MIN_SHARED, math.ceil(TAU_GOLD * len(do))), max(MIN_SHARED, math.ceil(TAU_HI * len(do)))
        per[iid] = {"state": it["state"], "persona": it["persona"], "fwd": r4(cov(nt, ot)), "rev": r4(cov(ot, nt)), "jaccard": r4(len(sh) / len(ot | nt) if (ot | nt) else 0.0),
                    "n_shared": len(sh), "n_old": len(ot), "n_new": len(nt), "n_do": len(do), "n_dn": len(dn), "detect_structurally_none": len(do) < MIN_DISCR or len(dn) < MIN_DISCR,
                    "min_do_hits_tg": mtg, "min_do_hits_hi": mhi, "q_do": sorted(qd), "q_do_n": len(qd), "q_do_fires": len(qd) >= mtg,
                    "abst_do_n": len(toks(ABST, rec["drop"]) & do), "do": sorted(do), "dn": sorted(dn),
                    "stale_field": rec["stale_field"], "gold_field": rec["gold_field"], "question": it["question"]}
    sc = {k: v for k, v in per.items() if not v.get("unscorable")}
    E = {"E_fwd": sorted(k for k, v in sc.items() if v["fwd"] >= 0.50), "E_q": sorted(k for k, v in sc.items() if v["q_do_fires"]),
         "E_small": sorted(k for k, v in sc.items() if v["n_do"] == MIN_DISCR), "E_none": sorted(k for k, v in sc.items() if v["detect_structurally_none"])}
    E["E_union"] = sorted(set(E["E_fwd"]) | set(E["E_q"]) | set(E["E_small"]))
    dist = {"fwd": quart([v["fwd"] for v in sc.values()]), "rev": quart([v["rev"] for v in sc.values()]), "n_do": quart([v["n_do"] for v in sc.values()]),
            "n_dn": quart([v["n_dn"] for v in sc.values()]), "q_do_n": collections.Counter(v["q_do_n"] for v in sc.values())}
    over = {"per_item": per, "n_scorable": len(sc), "n_unscorable_expiry": len(per) - len(sc), "exclusion_sets": E, "set_sizes": {k: len(v) for k, v in E.items()},
            "distributions": dist,
            "framing": "fwd = cov(toks(gold), toks(stale)): the share of the successor's tokens the stale string carries (would the stale string read as 'correct' under the PRESENT rule). "
                       "Because the stale flag is computed on old-only tokens with a cross-guard on new-only tokens, a high fwd does not itself make a gold answer fire (step 1: 0 of 89); "
                       "the false-positive mechanism the sheets show is a small old-only set whose members are question tokens (E_q). Both are re-scored beside the registered column."}
    jdump(over, OUT / "step2_overlap.json")
    # re-score tables
    tabs = {}
    for lid, L in C.lanes.items():
        tabs[lid] = {}
        for p in lane_policies(L):
            tabs[lid][p] = {}
            for split in ("all", "tagged", "untagged", "sup", "ret"):
                pr = pn_pred(C, L, split, p); blk = {}
                for flag in ("stale_use_tau_gold", "stale_use"):
                    reg_all = agg(C, L, p, "PRESENT-NEGATIVE", flag, pred=pr)
                    scor = agg(C, L, p, "PRESENT-NEGATIVE", flag, pred=lambda k, pr=pr: (pr is None or pr(k)) and C.scorable(k, L))
                    b = {"registered": reg_all, "scorable": scor}
                    for en, ids in E.items():
                        ids = set(ids)
                        b[en] = agg(C, L, p, "PRESENT-NEGATIVE", flag, pred=lambda k, pr=pr, ids=ids: (pr is None or pr(k)) and C.scorable(k, L) and L.rows[k]["item_id"] not in ids)
                        b[en]["excluded_n"] = scor["n"] - b[en]["n"]
                        b[en]["removed_flags"] = sorted(k for k, r in L.rows.items() if p in L.policies_of(k) and r["label"] == "PRESENT-NEGATIVE" and (pr is None or pr(k))
                                                        and C.scorable(k, L) and r["item_id"] in ids and L.reg[k].get(flag))
                    blk[flag] = b
                tabs[lid][p][split] = blk
    jdump({"tables": tabs, "exclusion_sets": E, "set_sizes": over["set_sizes"],
           "reading": "registered = as ledgered (all states incl. expiry); scorable = expiry removed (unscorable); E_* = scorable minus the exclusion set; rates with Wilson 95% intervals on the reached set."},
          OUT / "step2_rescore.json")
    print(f"      step 2: scorable {len(sc)}; E_fwd {len(E['E_fwd'])}, E_q {len(E['E_q'])}, E_small {len(E['E_small'])}, structurally none {len(E['E_none'])}")
    C.step2 = over; C.step2_tabs = tabs
    return over


# ------------------------------------------------------------------ step 3
def first_sentence(s):
    ss = sentences(s); return ss[0] if ss else (s or "")


def last_sentence(s):
    ss = sentences(s); return ss[-1] if ss else (s or "")


def step3(C):
    proto = {"scored_text": "the extracted JSON field answer -- run_ds.py:259 score_answer(it, rec, r['answer']); r['answer'] = parse_json(content)['answer'] (run_ds.py:157-170, JSON mode) for gpt-4.1-mini; "
                            "last_json(full reply)['answer'] (amend2_lit.py, run_cf.last_json) for Haiku 4.5; the reply itself is stored as raw[:400] and never scored",
             "full_output_scored": False, "final_answer_extraction_needed": False,
             "note": "the brief's 'extract the final answer line' branch does not apply (the answer field is already the model's answer object); the diagnostics below re-score sub-strings of it and, for the complete raws, the raw reply itself"}
    per_lane, diag, tabs, both, nsent = {}, {}, {}, {}, {}
    for lid, L in C.lanes.items():
        d = collections.Counter(); diag[lid] = {"first_sentence": {}, "last_sentence": {}, "minus_question": {}, "raw_full": {}}
        ns = collections.Counter()
        parser = last_json if "h45" in lid else parse_json
        for k, r in L.rows.items():
            it = C.byid[r["item_id"]]; rec = C.rec[r["item_id"]]; raw = r.get("raw") or ""
            d["n"] += 1; d["raw_complete"] += len(raw) < 400; d["fenced"] += raw.lstrip().startswith("```"); d["preamble"] += not raw.lstrip().startswith(("{", "```"))
            d["hit_max_tokens"] += (r.get("tok_out") or 0) >= 200; d["retries"] += (r.get("n_calls") or 1) > 1; d["status_not_ok"] += r.get("status") != "OK"; d["answer_none"] += r.get("answer") is None
            if len(raw) < 400:
                o = parser(raw); d["reparse_equal"] += bool(o and o.get("answer") == r["answer"]); d["reparse_fail"] += not (o and isinstance(o.get("answer"), str))
                diag[lid]["raw_full"][k] = score_answer(it, rec, raw)
            else:
                pref = json.dumps({"answer": r["answer"]}, ensure_ascii=False)
                d["truncated_prefix_consistent"] += (pref[:len(raw)] in raw) or raw.replace("```json\n", "").replace("```json", "").startswith(pref[:max(1, len(raw) - 10)][:40])
            ans = r["answer"] or ""
            ss = sentences(ans); ns[len(ss)] += 1
            diag[lid]["first_sentence"][k] = score_answer(it, rec, first_sentence(ans))
            diag[lid]["last_sentence"][k] = score_answer(it, rec, last_sentence(ans))
            diag[lid]["minus_question"][k] = score_tokens(it, rec, toks(ans, rec["drop"]) - toks(it["question"], rec["drop"]))
        per_lane[lid] = dict(d); nsent[lid] = dict(sorted(ns.items()))
        tabs[lid] = {}; both[lid] = {}
        for p in lane_policies(L):
            t = {"pn": {}, "present": {}}
            for flag in ("stale_use_tau_gold", "stale_use"):
                t["pn"][flag] = {"registered": agg(C, L, p, "PRESENT-NEGATIVE", flag), "scorable": agg(C, L, p, "PRESENT-NEGATIVE", flag, pred=lambda k: C.scorable(k, L))}
                for v in ("first_sentence", "last_sentence", "minus_question"):
                    t["pn"][flag][v] = agg(C, L, p, "PRESENT-NEGATIVE", flag, flags=diag[lid][v], pred=lambda k: C.scorable(k, L))
                t["pn"][flag]["raw_full"] = agg(C, L, p, "PRESENT-NEGATIVE", flag, flags=diag[lid]["raw_full"], pred=lambda k: C.scorable(k, L) and k in diag[lid]["raw_full"])
            for flag in ("correct", "correct_tau_hi"):
                t["present"][flag] = {"registered": agg(C, L, p, "PRESENT", flag)}
                for v in ("first_sentence", "last_sentence", "minus_question"):
                    t["present"][flag][v] = agg(C, L, p, "PRESENT", flag, flags=diag[lid][v])
                t["present"][flag]["raw_full"] = agg(C, L, p, "PRESENT", flag, flags=diag[lid]["raw_full"], pred=lambda k: k in diag[lid]["raw_full"])
            tabs[lid][p] = t
            # both-values cross-tab on scorable sup/ret rows: stale flag x successor coverage band
            xt = collections.Counter()
            for k, r in L.rows.items():
                if p not in L.policies_of(k) or r["label"] != "PRESENT-NEGATIVE" or not C.scorable(k, L):
                    continue
                s = L.reg[k]; sc = s.get("successor_cov")
                band = "succ=0" if not sc else ("0<succ<0.34" if sc < CROSS_GUARD else "succ>=0.34")
                xt[f"stale_tg={bool(s.get('stale_use_tau_gold'))}|{band}"] += 1
            both[lid][p] = dict(xt)
    out = {"protocol": proto, "per_lane": per_lane, "n_sentences": nsent, "rescore": tabs, "both_values": both,
           "sentence_split": "re.split(r\"(?<=[.!?])\\s+(?=[A-Z\\\"'(])\") -- heuristic; abbreviations such as 'Dr.' or '8th.' may over-split"}
    jdump(out, OUT / "step3_scored_text.json")
    C.diag = diag; C.step3 = out
    for lid in per_lane:
        d = per_lane[lid]
        print(f"      step 3 {lid}: raws complete {d['raw_complete']}/{d['n']}, reparse equal {d.get('reparse_equal', 0)}, fenced {d['fenced']}, preamble {d['preamble']}, max-token hits {d['hit_max_tokens']}, retries {d['retries']}")
    return out


# ------------------------------------------------------------------ step 4
def licensed_lines(C, it, key, ids):
    """Per licensed record: tag, rank in the view (or absent), entry text."""
    fl = C.fl[it["persona"]]; out = {}
    for e in ids:
        out[e] = {"tag": DC.lifecycle_tag(fl[e]), "rank": (C.view_by_key[key]["ids"].index(e) + 1) if e in C.view_by_key[key]["ids"] else None, "text": fl[e]["text"]}
    return out


def auto_label_stale(C, it, rec, r, s):
    A = toks(r["answer"] or "", rec["drop"]); q = toks(it["question"], rec["drop"])
    ot, nt = toks(rec["stale_field"], rec["drop"]), toks(rec["gold_field"], rec["drop"]); do, dn = ot - nt, nt - ot
    ev = {"do_A": sorted(do & A), "dn_A": sorted(dn & A), "q_do_A": sorted(q & do & A), "do_A_subset_of_question": (do & A) <= q, "phrase": None, "is_abstention": is_abst(r["answer"])}
    m = SUPERSEDE_RE.search(r["answer"] or "")
    ev["phrase"] = m.group(0) if m else None
    if ev["dn_A"] or m:
        lab = "mentions_but_superseded"
    elif ev["do_A_subset_of_question"] or ev["is_abstention"]:
        lab = "partial_overlap_artifact"
    else:
        lab = "gives_stale_value"
    return lab, ev


def auto_label_present(C, it, rec, r, key):
    A = toks(r["answer"] or "", rec["drop"]); fl = C.fl[it["persona"]]
    inview = [e for e in it["gold"] if e in C.view_by_key[key]["ids"]]
    ev = {"is_abstention": is_abst(r["answer"]), "gold_in_view_ids": inview,
          "entry_passes_detector": {e: score_answer(it, rec, fl[e]["text"])["correct"] for e in it["gold"]},
          "answer_covers_entry": {e: r4(cov(toks(fl[e]["text"], rec["drop"]), A)) for e in inview}}
    if ev["is_abstention"]:
        lab = "abstained"
    elif any(v >= TAU_GOLD for v in ev["answer_covers_entry"].values()) or not any(ev["entry_passes_detector"].get(e) for e in inview):
        lab = "correct_different_format"
    elif not inview:
        lab = "truncated_in_view"
    else:
        lab = "wrong_value"
    return lab, ev


def fence(s):
    return "````\n" + (s or "") + "\n````\n"


def step4(C):
    LAB = {"stale": ["gives_stale_value", "mentions_but_superseded", "partial_overlap_artifact", "other"],
           "present": ["wrong_value", "correct_different_format", "abstained", "truncated_in_view", "other"]}
    tmpl = {"label_sets": LAB, "sheets_sha256": {}, "stale": {}, "present": {},
            "instructions": "Copy to step4_labels.json; fill `label` for every entry from label_sets (and `note`). Expiry rows are unscorable and carry label null."}
    md_s = ["# Step 4 -- answers the detector marked stale under ORACLE (registered stale_use_tau_gold)", "",
            "Lanes: mini-D4 (gpt-4.1-mini, D.4 prompt), h45-D4 (Haiku 4.5, D.4 prompt); appendix: the A3-prompt lanes. Expiry rows are UNSCORABLE (gold field is the expired fact) and excluded from the classification counts.", ""]
    md_p = ["# Step 4 -- PRESENT answers marked incorrect with the licensed record in view (ORACLE view = ALWAYS view)", "",
            "Lanes: mini-D4 (required: the 28), h45-D4 (beside); appendix: the A3-prompt lanes.", ""]
    order = ["mini-D4", "h45-D4", "mini-A3", "h45-A3"]
    for lid in order:
        L = C.lanes[lid]; tmpl["stale"][lid] = {}; tmpl["present"][lid] = {}
        head = f"## {'Appendix -- ' if lid.endswith('A3') else ''}{lid} ({L.model}, prompt {L.prompt})"
        md_s += [head, ""]; md_p += [head, ""]
        keys_s = sorted(k for k, r in L.rows.items() if "ORACLE" in L.policies_of(k) and r["label"] == "PRESENT-NEGATIVE" and L.reg[k].get("stale_use_tau_gold"))
        keys_p = sorted(k for k, r in L.rows.items() if "ORACLE" in L.policies_of(k) and r["label"] == "PRESENT" and C.st1[r["item_id"]]["ORACLE"]["gold_in_view"] and not L.reg[k].get("correct"))
        md_s += [f"{len(keys_s)} answers flagged ({sum(1 for k in keys_s if C.byid[L.rows[k]['item_id']]['state'] == 'exp')} expiry, unscorable).", ""]
        md_p += [f"{len(keys_p)} answers.", ""]
        for k in keys_s:
            r = L.rows[k]; it = C.byid[r["item_id"]]; rec = C.rec[r["item_id"]]; s = L.reg[k]; st = C.st1[r["item_id"]]["ORACLE"]
            unsc = it["state"] == "exp"
            lic = licensed_lines(C, it, k, it.get("pn_members") or [])
            if unsc:
                lab, ev = None, {"unscorable": True}
            else:
                lab, ev = auto_label_stale(C, it, rec, r, s)
            tmpl["stale"][lid][k] = {"item_id": it["item_id"], "state": it["state"], "unscorable": unsc, "auto_label": lab, "auto_evidence": ev, "label": None, "note": ""}
            md_s += [f"### [{lid}] {it['item_id']} -- state {it['state']}{' (UNSCORABLE: expiry)' if unsc else ''}, tagged_reach {st['tagged_reach']}, successor_in_view {st['successor_in_view']}",
                     f"- key: `{k}`", f"- question: {it['question']}",
                     f"- gold (YAML `{SECTION_FIELDS[rec['section']][0]}`): {rec['gold_field']}",
                     f"- stale (YAML `{SECTION_FIELDS[rec['section']][2] or 'fact (expiry: = gold)'}`): {rec['stale_field'] if rec['stale_field'] else rec['gold_field']}",
                     "- licensed (forbidding) records: " + "; ".join(f"{e} [{v['tag']}] rank {v['rank'] if v['rank'] else 'absent'}: \"{v['text']}\"" for e, v in lic.items()),
                     f"- detector: stale_cov {r4(s.get('stale_cov'))}, stale_use(0.80) {s.get('stale_use')}, successor_cov {r4(s.get('successor_cov'))}"
                     + ("" if unsc else f", do∩A {ev['do_A']}, dn∩A {ev['dn_A']}, (do∩A)⊆question {ev['do_A_subset_of_question']}, phrase {ev['phrase']!r}"),
                     f"- **answer**: {r['answer']}", f"- raw[:400]: `{(r.get('raw') or '')[:400]}`",
                     f"- auto_label: {lab}", "- label: (step4_labels.json)", "", "view (ORACLE):", fence(C.view_by_key[k]["text"]), ""]
        for k in keys_p:
            r = L.rows[k]; it = C.byid[r["item_id"]]; rec = C.rec[r["item_id"]]; s = L.reg[k]
            lab, ev = auto_label_present(C, it, rec, r, k)
            lic = licensed_lines(C, it, k, it["gold"])
            tmpl["present"][lid][k] = {"item_id": it["item_id"], "auto_label": lab, "auto_evidence": ev, "label": None, "note": ""}
            md_p += [f"### [{lid}] {it['item_id']} -- PRESENT, section {rec['section']}", f"- key: `{k}`", f"- question: {it['question']}",
                     f"- gold (YAML `{SECTION_FIELDS[rec['section']][0]}`): {rec['gold_field']}",
                     "- licensed (gold) records: " + "; ".join(f"{e} [{v['tag']}] rank {v['rank'] if v['rank'] else 'absent'}: \"{v['text']}\" (entry passes detector: {ev['entry_passes_detector'][e]})" for e, v in lic.items()),
                     f"- detector: gold_cov {r4(s.get('gold_cov'))}; answer covers in-view entry text: {ev['answer_covers_entry']}; is_abstention {ev['is_abstention']}",
                     f"- **answer**: {r['answer']}", f"- raw[:400]: `{(r.get('raw') or '')[:400]}`",
                     f"- auto_label: {lab}", "- label: (step4_labels.json)", "", "view (ORACLE = ALWAYS):", fence(C.view_by_key[k]["text"]), ""]
    wtext(OUT / "step4_sheets_stale.md", "\n".join(md_s)); wtext(OUT / "step4_sheets_present.md", "\n".join(md_p))
    tmpl["sheets_sha256"] = {"step4_sheets_stale.md": sha_f(OUT / "step4_sheets_stale.md"), "step4_sheets_present.md": sha_f(OUT / "step4_sheets_present.md")}
    jdump(tmpl, OUT / "step4_labels.template.json")
    counts = step4_counts(C, tmpl)
    print(f"      step 4: stale sheet {sum(len(v) for v in tmpl['stale'].values())} answers, present sheet {sum(len(v) for v in tmpl['present'].values())}; counts source {counts['source']}")
    C.step4 = tmpl
    return tmpl


def step4_counts(C, tmpl):
    lab_p = OUT / "step4_labels.json"
    if lab_p.exists():
        labs = J(lab_p); src = f"manual (auditor's read; step4_labels.json sha256 {sha_f(lab_p)})"
        for kind in ("stale", "present"):
            assert set(labs[kind]) == set(tmpl[kind]), kind
            for lid in labs[kind]:
                assert set(labs[kind][lid]) == set(tmpl[kind][lid]), (kind, lid)
                for k, e in labs[kind][lid].items():
                    if kind == "stale" and tmpl[kind][lid][k]["unscorable"]:
                        continue
                    assert e.get("label") in tmpl["label_sets"][kind], (kind, lid, k, e.get("label"))
        get = lambda kind, lid, k: labs[kind][lid][k].get("label")        # noqa: E731
    else:
        labs = tmpl; src = "auto (unreviewed heuristic labels; step4_labels.json absent)"
        get = lambda kind, lid, k: tmpl[kind][lid][k]["auto_label"]      # noqa: E731
    out = {"source": src, "stale": {}, "present": {}, "cross": {}}
    for lid in tmpl["stale"]:
        c = collections.Counter(); c_state = collections.Counter(); c_tag = collections.Counter(); c_succ = collections.Counter(); unsc = 0
        for k, e in tmpl["stale"][lid].items():
            if e["unscorable"]:
                unsc += 1; continue
            lab = get("stale", lid, k); it = C.byid[e["item_id"]]; st = C.st1[e["item_id"]]["ORACLE"]
            c[lab] += 1; c_state[f"{lab}|{it['state']}"] += 1; c_tag[f"{lab}|tagged={st['tagged_reach']}"] += 1; c_succ[f"{lab}|successor_in_view={st['successor_in_view']}"] += 1
        out["stale"][lid] = {"n_flagged": len(tmpl["stale"][lid]), "n_unscorable_expiry": unsc, "n_classified": len(tmpl["stale"][lid]) - unsc, "labels": dict(c),
                             "by_state": dict(c_state), "by_tagged": dict(c_tag), "by_successor_in_view": dict(c_succ)}
    for lid in tmpl["present"]:
        c = collections.Counter(get("present", lid, k) for k in tmpl["present"][lid])
        out["present"][lid] = {"n": len(tmpl["present"][lid]), "labels": dict(c)}
    # mini vs Haiku on the same keys (D4 lanes)
    ks = set(tmpl["stale"]["mini-D4"]) | set(tmpl["stale"]["h45-D4"])
    cross = collections.Counter()
    for k in ks:
        a = get("stale", "mini-D4", k) if k in tmpl["stale"]["mini-D4"] and not tmpl["stale"]["mini-D4"][k]["unscorable"] else ("unscorable" if k in tmpl["stale"]["mini-D4"] else "not_flagged")
        b = get("stale", "h45-D4", k) if k in tmpl["stale"]["h45-D4"] and not tmpl["stale"]["h45-D4"][k]["unscorable"] else ("unscorable" if k in tmpl["stale"]["h45-D4"] else "not_flagged")
        cross[f"mini={a}|h45={b}"] += 1
    out["cross"]["stale_mini_vs_h45_same_keys"] = dict(cross)
    jdump(out, OUT / "step4_counts.json")
    return out


# ------------------------------------------------------------------ step 4b: what the view itself asserts; identity binding
IDENT_RE = re.compile(r"(identif|named|not\s+\w+'s|do(es)? not (mention|contain information about|refer to)|someone named|as ['\"]?[A-Z][a-z]+|about a user named|are about|is not specified as|belong to)", re.I)


def step4b(C):
    """(i) Per PN scorable item x policy view: lines whose TEXT fires the item's stale detector (TAU_GOLD), split by the
    line's lifecycle tag; lines asserting the successor, split the same way. Then per lane x policy the stale flag
    cross-tabbed with 'an ACTIVE line in the view asserts the stale value'. (ii) PRESENT abstentions and the
    identity-mismatch reason; whether the persona's name ever appears in a view line."""
    lines_out = {}
    for it in C.pn:
        iid = it["item_id"]
        if it["state"] == "exp":
            continue
        rec = C.rec[iid]; drop = rec["drop"]
        ot, nt = toks(rec["stale_field"], drop), toks(rec["gold_field"], drop); do, dn = ot - nt, nt - ot
        for p in POLICIES7:
            P = C.parsed[(iid, p)]; pm = set(it.get("pn_members") or []); ids = C.views[iid][p]["ids"]
            d = {"active_stale": [], "tagged_stale": [], "active_successor": [], "tagged_successor": [], "tagged_member_not_stale": []}
            for x, e in zip(P, ids):
                A = toks(x["text"], drop)
                stale = len(do & A) >= MIN_SHARED and cov(dn, A) < CROSS_GUARD and cov(do, A) >= TAU_GOLD
                succ = len(dn & A) >= MIN_SHARED and cov(do, A) < CROSS_GUARD and cov(dn, A) >= TAU_GOLD
                act = x["tag"] == "active"
                if stale:
                    d["active_stale" if act else "tagged_stale"].append(x["rank"])
                if succ:
                    d["active_successor" if act else "tagged_successor"].append(x["rank"])
                if not act and e in pm and not stale:
                    d["tagged_member_not_stale"].append(x["rank"])
            d["any_active_stale"] = bool(d["active_stale"]); d["any_tagged_successor"] = bool(d["tagged_successor"])
            d["stale_only_tagged"] = bool(d["tagged_stale"]) and not d["active_stale"]
            lines_out[f"{iid}|{p}"] = d
    # cross-tabs per lane x policy on scorable PN rows
    xt = {}
    for lid, L in C.lanes.items():
        if lid == "mini-D4-V3":
            continue
        xt[lid] = {}
        for p in POLICIES7:
            c = collections.Counter(); c2 = collections.Counter()
            for k, r in L.rows.items():
                if p not in L.policies_of(k) or r["label"] != "PRESENT-NEGATIVE" or not C.scorable(k, L):
                    continue
                d = lines_out[f"{r['item_id']}|{p}"]; f = bool(L.reg[k].get("stale_use_tau_gold")); tg = bool(tagged_of(C, L, k, p))
                c[f"stale={f}|active_stale_line={d['any_active_stale']}"] += 1
                c2[f"tagged_reach={tg}|active_stale_line={d['any_active_stale']}|stale={f}"] += 1
            xt[lid][p] = {"stale_x_active_stale_line": dict(c), "tagged_x_active_stale_line_x_stale": dict(c2)}
    # items whose ORACLE view has an active stale line / a tagged successor line
    orc = {"n_scorable": sum(1 for it in C.pn if it["state"] != "exp"),
           "oracle_any_active_stale": sum(1 for it in C.pn if it["state"] != "exp" and lines_out[f"{it['item_id']}|ORACLE"]["any_active_stale"]),
           "oracle_any_tagged_successor": sum(1 for it in C.pn if it["state"] != "exp" and lines_out[f"{it['item_id']}|ORACLE"]["any_tagged_successor"]),
           "oracle_tagged_successor_items": sorted(it["item_id"] for it in C.pn if it["state"] != "exp" and lines_out[f"{it['item_id']}|ORACLE"]["any_tagged_successor"]),
           "always_any_active_stale": sum(1 for it in C.pn if it["state"] != "exp" and lines_out[f"{it['item_id']}|ALWAYS"]["any_active_stale"]),
           "by_state_oracle_active_stale": {st: sum(1 for it in C.pn if it["state"] == st and lines_out[f"{it['item_id']}|ORACLE"]["any_active_stale"]) for st in ("sup", "ret")}}
    # (ii) identity binding
    ident = {}
    for lid, L in C.lanes.items():
        c = collections.Counter()
        for k, r in L.rows.items():
            if r["label"] != "PRESENT":
                continue
            it = C.byid[r["item_id"]]; a = r["answer"] or ""; ab = is_abst(a); inview = bool(C.st1[r["item_id"]]["ORACLE"]["gold_in_view"])
            name = it["persona"].capitalize()
            reason = bool(ab and (IDENT_RE.search(a) and name.lower() in a.lower()))
            c["present_rows"] += 1; c["abstained"] += ab; c["abstained_in_view"] += (ab and inview)
            c["abstained_identity_reason"] += reason; c["abstained_in_view_identity_reason"] += (reason and inview)
            c["abstained_bare_phrase_only"] += (ab and norm(a) == norm(ABST))
        ident[lid] = dict(c)
    name_in_view = {"present_views_with_persona_name": 0, "present_views": 0, "pn_views_with_persona_name": 0, "pn_views": 0}
    for it in C.sub:
        if it["label"] == "ABSENT":
            continue
        name = it["persona"].capitalize(); txt = C.views[it["item_id"]]["ORACLE"]["text"]
        key = "present" if it["label"] == "PRESENT" else "pn"
        name_in_view[f"{key}_views"] += 1; name_in_view[f"{key}_views_with_persona_name"] += (re.search(r"\b" + re.escape(name) + r"\b", txt) is not None)
    q_names = sum(1 for it in C.present if re.search(r"\b" + re.escape(it["persona"].capitalize()) + r"\b", it["question"]))
    out = {"view_lines": lines_out, "crosstabs": xt, "oracle_summary": orc,
           "identity": {"per_lane": ident, "persona_name_in_view": name_in_view, "present_questions_naming_persona": {"k": q_names, "n": len(C.present)},
                        "note": "entries print 'User ...' (or a third party's name); the prompt says 'a question about a user from a view of the user's memory store' and never binds the persona's name to 'User'"}}
    jdump(out, OUT / "step4b_view_lines.json")
    print(f"      step 4b: ORACLE views with an ACTIVE line asserting the stale value {orc['oracle_any_active_stale']}/{orc['n_scorable']} (ALWAYS {orc['always_any_active_stale']}); "
          f"tagged line asserting the successor {orc['oracle_any_tagged_successor']}; persona name in PRESENT views {name_in_view['present_views_with_persona_name']}/{name_in_view['present_views']}; "
          f"identity-reason abstentions h45-D4 {ident['h45-D4'].get('abstained_identity_reason', 0)} of {ident['h45-D4'].get('abstained', 0)}")
    C.step4b = out
    return out


# ------------------------------------------------------------------ step 5
def _encoder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")


def embed_texts(texts, skip):
    """MiniLM (local, offline) over unique texts, cached in step5_minilm_cache.npz keyed by exact text."""
    cache_p = OUT / "step5_minilm_cache.npz"
    have = {}
    if cache_p.exists():
        z = np.load(cache_p, allow_pickle=True)
        have = {str(t): v for t, v in zip(z["texts"], z["emb"])}
    need = [t for t in texts if t not in have]
    if need and not skip:
        enc = _encoder()
        vecs = enc.encode(need, normalize_embeddings=True, batch_size=128, show_progress_bar=False)
        for t, v in zip(need, vecs):
            have[t] = np.asarray(v, np.float32)
        ts = sorted(have); np.savez_compressed(cache_p, texts=np.asarray(ts, dtype=object), emb=np.stack([have[t] for t in ts]))
    return have if not need or not skip else None


def step5(C, skip_embed=False):
    # licensed texts and view line texts
    lic_text = {}
    for it in C.sub:
        if it["label"] == "PRESENT":
            lic_text[it["item_id"]] = {e: C.fl[it["persona"]][e]["text"] for e in it["gold"]}
        elif it["label"] == "PRESENT-NEGATIVE":
            lic_text[it["item_id"]] = {e: C.fl[it["persona"]][e]["text"] for e in (it.get("pn_members") or [])}
    texts = set()
    for (iid, p), P in C.parsed.items():
        for x in P:
            texts.add(x["text"])
    for d in lic_text.values():
        texts.update(d.values())
    no_lic = [it for it in C.present if not it["gold"]]
    for it in no_lic:
        texts.add(C.rec[it["item_id"]]["gold_field"])
    emb = embed_texts(sorted(texts), skip_embed)
    ok_id = 0; bad_id = []
    mem = {}                                                            # (item, policy) -> {id, text, emb_0.80, emb_0.90, emb_0.95, max_cos}
    absent_maxcos = {"PRESENT": [], "PRESENT-NEGATIVE": []}
    for it in C.sub:
        if it["label"] == "ABSENT":
            continue
        iid = it["item_id"]; lic = lic_text[iid]
        for p in POLICIES7:
            ids = C.views[iid][p]["ids"]; lines = [x["text"] for x in C.parsed[(iid, p)]]; nl = {norm(t) for t in lines}
            by_id = any(e in ids for e in lic) if lic else None
            by_text = any(norm(t) in nl for t in lic.values()) if lic else None
            mx = None
            if emb is not None and lic and lines:
                M = np.stack([emb[t] for t in lines])
                mx = {e: float(np.max(M @ emb[t])) for e, t in lic.items()}
                for e, t in lic.items():
                    if e not in ids:
                        absent_maxcos[it["label"]].append(mx[e])
            rec = {"id": by_id, "text": by_text, "max_cos": mx, "best_cos": (max(mx.values()) if mx else None)}
            for tau in TAUS_EMB:
                rec[f"emb_{tau:.2f}"] = (max(mx.values()) >= tau) if mx else None
            mem[(iid, p)] = rec
            s1 = C.st1[iid][p]
            regv = s1["gold_in_view"] if it["label"] == "PRESENT" else s1["reach"]
            if lic:
                if bool(by_id) == bool(regv):
                    ok_id += 1
                else:
                    bad_id.append({"item_id": iid, "policy": p, "by_id": by_id, "stage1": regv})
            elif regv in (False, None):
                ok_id += 1
            else:
                bad_id.append({"item_id": iid, "policy": p, "by_id": None, "stage1": regv})
    defs = ["id", "text"] + [f"emb_{t:.2f}" for t in TAUS_EMB]
    cover = {"present": {}, "pn_reach": {}}
    for p in POLICIES7:
        cover["present"][p] = {d: rate(sum(1 for it in C.present if mem[(it["item_id"], p)][d]), len(C.present)) for d in defs}
        cover["present"][p]["n_no_licensed_id"] = len(no_lic)
        cover["pn_reach"][p] = {d: rate(sum(1 for it in C.pn if mem[(it["item_id"], p)][d]), len(C.pn)) for d in defs}
        for st in ("sup", "ret", "exp"):
            cover["pn_reach"][p][f"id_{st}"] = rate(sum(1 for it in C.pn if it["state"] == st and mem[(it["item_id"], p)]["id"]), sum(1 for it in C.pn if it["state"] == st))
    # in-view correct rate per lane under each definition (PRESENT rows; ALWAYS and ORACLE views are identical for PRESENT)
    corr = {}
    for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3"):
        L = C.lanes[lid]; corr[lid] = {}
        for p in ("ALWAYS", "MODEL", "LOOKUP"):
            corr[lid][p] = {}
            for d in defs:
                inv = lambda k, d=d, p=p: mem[(L.rows[k]["item_id"], p)][d] is True                 # noqa: E731
                out_ = lambda k, d=d, p=p: mem[(L.rows[k]["item_id"], p)][d] is not True           # noqa: E731
                corr[lid][p][d] = {"in_view": agg(C, L, p, "PRESENT", "correct", pred=inv), "not_in_view": agg(C, L, p, "PRESENT", "correct", pred=out_)}
    nl_rows = []
    for it in no_lic:
        iid = it["item_id"]; gf = C.rec[iid]["gold_field"]; lines = [x["text"] for x in C.parsed[(iid, "ALWAYS")]]
        mx = float(np.max(np.stack([emb[t] for t in lines]) @ emb[gf])) if emb is not None and lines else None
        rows_ = {lid: (C.lanes[lid].rows.get(f"{iid}|{C.views[iid]['ALWAYS']['sha']}") or {}).get("answer") for lid in ("mini-D4", "h45-D4")}
        nl_rows.append({"item_id": iid, "section": C.rec[iid]["section"], "gold_field": gf, "max_cos_gold_field_vs_view": r4(mx), "answers": rows_})
    hist = {}
    for lab, xs in absent_maxcos.items():
        h = collections.Counter(f"{math.floor(x * 20) / 20:.2f}" for x in xs)
        hist[lab] = {"n_absent_licensed_records": len(xs), "bins_0.05": dict(sorted(h.items())), "share_ge_0.90": (round(sum(1 for x in xs if x >= 0.90) / len(xs), 4) if xs else None)}
    out = {"definitions": {"id": "licensed entry id in the view's id list (the registered quantity)", "text": "normalized text equality (NFKD, casefold, non-alphanumerics to space) with any view line's text field",
                           **{f"emb_{t:.2f}": f"MiniLM all-MiniLM-L6-v2 cosine >= {t:.2f} between the licensed record's text and any view line's text" for t in TAUS_EMB}},
           "embedding": None if emb is None else {"model": "sentence-transformers/all-MiniLM-L6-v2 (local, offline)", "n_unique_texts": len(texts), "cache": "step5_minilm_cache.npz"},
           "id_vs_stage1": {"agree": ok_id, "disagree": bad_id}, "coverage": cover, "in_view_correct": corr, "no_licensed_id": nl_rows, "absent_record_max_cosine": hist,
           "per_item_policy": {f"{iid}|{p}": v for (iid, p), v in mem.items()}}
    check(C, not bad_id, f"step 5: id-based membership equals stage1 for {ok_id} item x policy cells ({len(bad_id)} disagree)")
    jdump(out, OUT / "step5_coverage.json")
    C.step5 = out
    step5_ranks(C, lic_text)
    return out


def step5_ranks(C, lic_text):
    per = {}; pooled = collections.defaultdict(list); best = collections.defaultdict(list); not_in_store = []
    for it in C.sub:
        if it["label"] == "ABSENT":
            continue
        iid = it["item_id"]; rk = C.ranks[iid]; lic = lic_text[iid]; fl = C.fl[it["persona"]]
        if not lic:
            per[iid] = {"label": it["label"], "state": it["state"], "variant": it["variant"], "n_licensed": 0}; continue
        recs = {e: ({"rank": rk[e][0], "cos": r4(rk[e][1]), "tag": DC.lifecycle_tag(fl[e])} if e in rk else {"rank": None, "cos": None, "tag": DC.lifecycle_tag(fl[e]), "not_in_store_variant": True}) for e in lic}
        ranks = [v["rank"] for v in recs.values() if v["rank"] is not None]
        # any store entry with the same normalized text as a licensed record
        ntexts = {norm(t) for t in lic.values()}
        dup = min((rk[e][0] for e in rk if norm(fl[e]["text"]) in ntexts), default=None)
        d = {"label": it["label"], "state": it["state"], "variant": it["variant"], "n_licensed": len(lic), "n_licensed_in_store": len(ranks), "records": recs,
             "best_rank": (min(ranks) if ranks else None), "worst_rank": (max(ranks) if ranks else None),
             "n_in_top5": sum(1 for r in ranks if r <= K_USE), "best_rank_text_dup": dup, "store_size": len(rk)}
        if not ranks:
            not_in_store.append({"item_id": iid, "label": it["label"], "state": it["state"], "variant": it["variant"], "licensed": sorted(lic)})
            per[iid] = d; continue
        if it["label"] == "PRESENT-NEGATIVE" and it["gold"]:
            sr = [rk[e][0] for e in it["gold"] if e in rk]
            d["successor_best_rank"] = min(sr) if sr else None; d["successor_above_stale"] = (min(sr) < min(ranks)) if sr else None
        per[iid] = d
        grp = [("label", it["label"]), ("state", f"{it['label']}|{it['state']}"), ("variant", f"{it['label']}|{it['variant']}")]
        for g, key in grp:
            best[key].append(min(ranks)); pooled[key].extend(ranks)

    def stats(xs):
        a = np.asarray(xs, float); q = quart(xs)
        h = collections.Counter("1-5" if x <= 5 else "6-10" if x <= 10 else "11-20" if x <= 20 else "21-50" if x <= 50 else ">50" for x in xs)
        return {**q, "share_le5": r4((a <= 5).mean()), "share_le10": r4((a <= 10).mean()), "share_gt10": r4((a > 10).mean()), "hist": dict(h), "median_gt5": bool(np.median(a) > 5)}
    out = {"config": J(OUT / "gate_retrieval.json")["config"], "best_rank_per_item": {k: stats(v) for k, v in best.items()}, "pooled_ranks": {k: stats(v) for k, v in pooled.items()},
           "sanity": {"present_share_le5_equals_65_of_164": None, "pn_share_le5_equals_54_of_104": None}, "per_item": per,
           "licensed_records_not_in_store_variant": {"n_items_with_no_licensed_record_in_store": len(not_in_store), "items": not_in_store,
                                                     "n_records": sum(1 for v in per.values() for r in (v.get("records") or {}).values() if r.get("not_in_store_variant"))},
           "successor_above_stale": {st: rate(sum(1 for v in per.values() if v.get("state") == st and v.get("successor_above_stale")), sum(1 for v in per.values() if v.get("state") == st and v.get("successor_above_stale") is not None)) for st in ("sup", "ret")}}
    pres = [v["best_rank"] for v in per.values() if v["label"] == "PRESENT" and v.get("best_rank") is not None]; pn = [v["best_rank"] for v in per.values() if v["label"] == "PRESENT-NEGATIVE" and v.get("best_rank") is not None]
    out["sanity"]["present_share_le5_equals_65_of_164"] = {"k": sum(1 for x in pres if x <= 5), "n": len(pres)}
    out["sanity"]["pn_share_le5_equals_54_of_104"] = {"k": sum(1 for x in pn if x <= 5), "n": len(pn)}
    check(C, out["sanity"]["present_share_le5_equals_65_of_164"]["k"] == 65 and out["sanity"]["pn_share_le5_equals_54_of_104"]["k"] == 54,
          f"step 5 ranks: best-rank<=5 for PRESENT {out['sanity']['present_share_le5_equals_65_of_164']} and PN {out['sanity']['pn_share_le5_equals_54_of_104']} (expected 65 / 54)")
    for k, v in out["best_rank_per_item"].items():
        print(f"      ranks {k}: n {v['n']} median {v['median']} q25 {v['q25']} q75 {v['q75']} <=5 {v['share_le5']} >10 {v['share_gt10']}")
    jdump(out, OUT / "step5_ranks.json")
    C.step5_ranks = out
    return out


# ------------------------------------------------------------------ step 6
def step6(C):
    def first(pred):
        for it in sorted(C.sub, key=lambda x: x["item_id"]):
            if pred(it):
                return it
        return None
    v = C.views
    i1 = first(lambda it: it["label"] == "PRESENT-NEGATIVE" and it["state"] == "sup" and len({v[it["item_id"]][p]["sha"] for p in ("ALWAYS", "MODEL", "ORACLE")}) == 3
                and C.pol[it["item_id"]]["policies"]["MODEL"]["gate"] and not C.pol[it["item_id"]]["policies"]["MODEL"]["abstain"])
    i2 = first(lambda it: it["label"] == "PRESENT-NEGATIVE" and it["state"] in ("ret", "exp") and C.st1[it["item_id"]]["ALWAYS"]["reach"] and not C.st1[it["item_id"]]["ALWAYS"]["tagged_reach"])
    i3 = first(lambda it: it["label"] == "PRESENT" and C.st1[it["item_id"]]["ALWAYS"]["gold_in_view"])
    md = ["# Step 6 -- render check: three complete prompts as the answerer received them", "",
          "System message (`SYSTEM_ANSWER`, D.4; identical under every policy):", fence(PD.SYSTEM_ANSWER),
          "Amendment 3 system message (`SYSTEM_ANSWER_A3`; the paragraph before `Return JSON only` is the addition):", fence(SYSTEM_ANSWER_A3), ""]
    sel = {}
    for tag, it in (("PN supersession, three distinct views", i1), ("PN untagged reached record (retraction/expiry printed active)", i2), ("PRESENT, licensed record in view", i3)):
        if it is None:
            md += [f"## {tag}: no item matched", ""]; continue
        iid = it["item_id"]; sel[tag] = iid
        md += [f"## {tag}: `{iid}` (state {it['state']})", ""]
        for p in ("ALWAYS", "MODEL", "ORACLE"):
            vv = v[iid][p]; key = f"{iid}|{vv['sha']}"
            md += [f"### policy {p} -- {vv['n_lines']} lines, view sha {vv['sha']}, abstain {C.st1[iid][p]['abstain']}", "", "User message:",
                   fence(PD.USER_ANSWER.format(view=vv["text"], question=it["question"]))]
            for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3"):
                r = C.lanes[lid].rows.get(key)
                if r is not None:
                    s = C.lanes[lid].reg[key]; fl_ = {k2: s.get(k2) for k2 in ("correct", "stale_use_tau_gold", "stale_use", "stale_cov", "gold_cov") if k2 in s}
                    md += [f"- recorded answer [{lid}]: {r['answer']}  ← {fl_}"]
                else:
                    md += [f"- recorded answer [{lid}]: (no call: abstained or record not reached under this policy)"]
            md += [""]
    tags = J(OUT / "gate_views.json")["tag_vocabulary"]
    both = PD.SYSTEM_ANSWER + "\n" + PD.USER_ANSWER
    per_lane_tok = {lid: {"max_tok_in": max(r.get("tok_in") or 0 for r in L.rows.values()), "max_tok_out": max(r.get("tok_out") or 0 for r in L.rows.values()),
                          "n_tok_out_ge_200": sum(1 for r in L.rows.values() if (r.get("tok_out") or 0) >= 200), "status_not_ok": sum(1 for r in L.rows.values() if r.get("status") != "OK"),
                          "answer_none": sum(1 for r in L.rows.values() if r.get("answer") is None), "retries": sum(1 for r in L.rows.values() if (r.get("n_calls") or 1) > 1)} for lid, L in C.lanes.items()}
    qmatch = all(r["question"] == C.byid[r["item_id"]]["question"] for L in C.lanes.values() for r in L.rows.values())
    chk = {"selected_items": sel, "tags_present_in_views": tags, "tags_explained_in_system_prompt": all(w in PD.SYSTEM_ANSWER for w in ("active", "superseded", "retracted", "expired")),
           "tag_format": "inline field `lifecycle: <tag>` per line; multi-tag entries print a comma list",
           "pinned_time_or_current_date_given": bool(TIME_RE.search(both)), "time_information_per_line": "relative `age: N days` only (no absolute date, no t_now)",
           "truncation": {"views_n_lines_equals_ids": J(OUT / "gate_views.json")["bad_len"] == 0, "max_view_lines": max(v[i][p]["n_lines"] for i in v for p in v[i]),
                          "plus_more_fragments": J(OUT / "gate_views.json")["plus_more_fragments"], "per_lane_tokens": per_lane_tok},
           "question_present": PD.USER_ANSWER.endswith("Question: {question}") and qmatch,
           "answer_format": "JSON object {\"answer\": ...}; mini in JSON mode; Haiku fenced ```json blocks parsed by last_json",
           "parse_failures_total": sum(x["status_not_ok"] + x["answer_none"] for x in per_lane_tok.values()),
           "final_answer_rerun_triggered": False, "final_answer_rerun_note": "not triggered: 0 parse failures, 0 retries, no max-token hit; a re-run would need a model call and this script has no API path"}
    md += ["## Checklist (computed)", "", "```json", json.dumps(chk, indent=1, ensure_ascii=False, default=_default), "```", ""]
    wtext(OUT / "step6_render.md", "\n".join(md)); jdump(chk, OUT / "step6_render.json")
    print(f"      step 6: items {sel}; tags explained {chk['tags_explained_in_system_prompt']}; pinned time given {chk['pinned_time_or_current_date_given']}; parse failures {chk['parse_failures_total']}")
    C.step6 = chk
    return chk


# ------------------------------------------------------------------ step 7
def logistic(X, y, ridge=1e-8, iters=50):
    """Newton-Raphson logistic regression; returns coefficients, Wald SE, converged flag."""
    X = np.asarray(X, float); y = np.asarray(y, float); w = np.zeros(X.shape[1])
    if y.sum() == 0 or y.sum() == len(y):
        return {"coef": None, "se": None, "converged": False, "note": "no variation in y"}
    conv = False
    for _ in range(iters):
        z = X @ w; p = 1 / (1 + np.exp(-z)); g = X.T @ (y - p); H = -(X.T * (p * (1 - p))) @ X - ridge * np.eye(X.shape[1])
        step = np.linalg.solve(H, g); w = w - step
        if not np.all(np.isfinite(w)):
            return {"coef": None, "se": None, "converged": False, "note": "diverged"}
        if np.max(np.abs(step)) < 1e-8:
            conv = True; break
    z = X @ w; p = 1 / (1 + np.exp(-z)); H = -(X.T * (p * (1 - p))) @ X - ridge * np.eye(X.shape[1])
    try:
        se = np.sqrt(np.diag(np.linalg.inv(-H)))
    except np.linalg.LinAlgError:
        se = np.full(X.shape[1], np.nan)
    return {"coef": [r4(x) for x in w], "se": [r4(x) for x in se], "z": [r4(a / b) if b and np.isfinite(b) else None for a, b in zip(w, se)], "converged": conv}


def step7(C):
    from scipy import stats as SS
    per_row = {}
    for lid, L in C.lanes.items():
        for k, r in L.rows.items():
            rec = C.rec[r["item_id"]]; a = r["answer"] or ""
            per_row[(lid, k)] = {"chars": len(a), "ntoks": len(toks(a, rec["drop"])), "tok_out": r.get("tok_out"), "n_sent": len(sentences(a)), "is_abst": is_abst(a)}
    by = {}
    for lid, L in C.lanes.items():
        by[lid] = {}
        for p in lane_policies(L):
            by[lid][p] = {}
            for lab in ("PRESENT-NEGATIVE", "PRESENT"):
                ks = [k for k, r in L.rows.items() if p in L.policies_of(k) and r["label"] == lab and (lab == "PRESENT" or C.scorable(k, L))]
                by[lid][p][lab] = {m: quart([per_row[(lid, k)][m] for k in ks if per_row[(lid, k)][m] is not None]) for m in ("chars", "ntoks", "tok_out", "n_sent")}
                by[lid][p][lab]["abstention_rate"] = rate(sum(1 for k in ks if per_row[(lid, k)]["is_abst"]), len(ks))
    paired = {}
    for a, b in (("mini-D4", "h45-D4"), ("mini-A3", "h45-A3")):
        ks = set(C.lanes[a].rows) & set(C.lanes[b].rows)
        paired[f"{b}/{a}"] = {"n": len(ks), "median_char_ratio": r4(np.median([per_row[(b, k)]["chars"] / max(1, per_row[(a, k)]["chars"]) for k in ks])),
                              "median_chars": {a: r4(np.median([per_row[(a, k)]["chars"] for k in ks])), b: r4(np.median([per_row[(b, k)]["chars"] for k in ks]))}}
    corr = {}
    for lid, L in C.lanes.items():
        corr[lid] = {}
        for lab, flags in (("PRESENT-NEGATIVE", ("stale_use_tau_gold", "stale_use")), ("PRESENT", ("correct",))):
            ks = [k for k, r in L.rows.items() if r["label"] == lab and (lab == "PRESENT" or C.scorable(k, L))]      # distinct rows
            for flag in flags:
                y = np.array([1.0 if L.reg[k].get(flag) else 0.0 for k in ks]); lc = np.log(np.array([max(1, per_row[(lid, k)]["chars"]) for k in ks]))
                lt = np.log1p(np.array([per_row[(lid, k)]["ntoks"] for k in ks], float))
                d = {"n_rows": len(ks), "n_flagged": int(y.sum())}
                if 0 < y.sum() < len(y):
                    r1 = SS.pearsonr(y, lc); r2 = SS.pearsonr(y, lt)
                    d["pointbiserial_log_chars"] = {"r": r4(r1[0]), "p": r4(r1[1])}; d["pointbiserial_log_toks"] = {"r": r4(r2[0]), "p": r4(r2[1])}
                    u = SS.mannwhitneyu(np.exp(lc)[y == 1], np.exp(lc)[y == 0], alternative="two-sided")
                    d["mannwhitney_chars"] = {"U": r4(u[0]), "p": r4(u[1]), "median_flagged": r4(np.median(np.exp(lc)[y == 1])), "median_unflagged": r4(np.median(np.exp(lc)[y == 0]))}
                    lg = logistic(np.column_stack([np.ones(len(ks)), lc]), y); d["logistic_log_chars"] = lg
                    if lg.get("coef"):
                        d["logistic_log_chars"]["OR_per_doubling"] = r4(math.exp(lg["coef"][1] * math.log(2)))
                else:
                    d["note"] = "no variation in the flag"
                corr[lid][f"{lab}|{flag}"] = d
    # pooled mini-D4 + h45-D4 PN rows: logit = b0 + b1 log chars + b2 is_haiku
    pooled = {}
    for flag in ("stale_use_tau_gold", "stale_use"):
        X, y = [], []
        for lid in ("mini-D4", "h45-D4"):
            L = C.lanes[lid]
            for k, r in L.rows.items():
                if r["label"] == "PRESENT-NEGATIVE" and C.scorable(k, L):
                    X.append([1.0, math.log(max(1, per_row[(lid, k)]["chars"])), 1.0 if lid == "h45-D4" else 0.0]); y.append(1.0 if L.reg[k].get(flag) else 0.0)
        pooled[flag] = {"n": len(y), "n_flagged": int(sum(y)), "model": "logit P(flag) = b0 + b1*log(chars) + b2*is_haiku", "fit": logistic(np.array(X), np.array(y))}
        Xh = [[x[0], x[2]] for x in X]; pooled[flag]["fit_haiku_only"] = logistic(np.array(Xh), np.array(y))
    # length controls for Haiku: first sentence (step 3) and truncation to the paired mini answer's length
    controls = {}
    for hl, ml in (("h45-D4", "mini-D4"), ("h45-A3", "mini-A3")):
        H, M = C.lanes[hl], C.lanes[ml]; trunc = {}
        for k, r in H.rows.items():
            if k not in M.rows:
                continue
            it = C.byid[r["item_id"]]; rec = C.rec[r["item_id"]]; a = r["answer"] or ""; n = len(M.rows[k]["answer"] or "")
            cut = a if len(a) <= n else a[:n].rsplit(" ", 1)[0]
            trunc[k] = score_answer(it, rec, cut)
        controls[hl] = {}
        for p in POLICIES7:
            controls[hl][p] = {}
            for flag in ("stale_use_tau_gold", "stale_use"):
                controls[hl][p][flag] = {"registered_haiku": agg(C, H, p, "PRESENT-NEGATIVE", flag, pred=lambda k: C.scorable(k, H)),
                                         "haiku_first_sentence": agg(C, H, p, "PRESENT-NEGATIVE", flag, flags=C.diag[hl]["first_sentence"], pred=lambda k: C.scorable(k, H)),
                                         "haiku_trunc_to_mini_len": agg(C, H, p, "PRESENT-NEGATIVE", flag, flags=trunc, pred=lambda k: C.scorable(k, H) and k in trunc),
                                         "registered_mini": agg(C, M, p, "PRESENT-NEGATIVE", flag, pred=lambda k: C.scorable(k, M))}
            controls[hl][p]["correct"] = {"registered_haiku": agg(C, H, p, "PRESENT", "correct"), "haiku_first_sentence": agg(C, H, p, "PRESENT", "correct", flags=C.diag[hl]["first_sentence"]),
                                          "haiku_trunc_to_mini_len": agg(C, H, p, "PRESENT", "correct", flags=trunc, pred=lambda k: k in trunc), "registered_mini": agg(C, M, p, "PRESENT", "correct")}
        C.diag[hl]["trunc_to_mini_len"] = trunc
    out = {"by_lane_policy_label": by, "paired_lanes": paired, "correlation": corr, "pooled_logistic": pooled, "length_controls": controls,
           "note": "stale diagnostics on the scorable (sup+ret) rows; correlations on distinct rows (one per view), not on policy-weighted rows"}
    jdump(out, OUT / "step7_length.json")
    C.per_row_len = per_row; C.step7 = out
    for lid in ("mini-D4", "h45-D4"):
        b = by[lid]["ORACLE"]["PRESENT-NEGATIVE"]; c = corr[lid]["PRESENT-NEGATIVE|stale_use_tau_gold"]
        print(f"      step 7 {lid}: PN ORACLE median chars {b['chars']['median']}, sentences {b['n_sent']['median']}; r(log chars, stale_tg) {c.get('pointbiserial_log_chars')}")
    return out


# ------------------------------------------------------------------ master rows and manifest
def write_master(C):
    with io.open(OUT / "rows_master.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for lid, L in C.lanes.items():
            for k in sorted(L.rows):
                r = L.rows[k]; it = C.byid[r["item_id"]]
                d = {"lane": lid, "key": k, "item_id": r["item_id"], "label": r["label"], "state": it["state"], "policies": sorted(L.policies_of(k)), "answer": r["answer"],
                     "unscorable_expiry": it["state"] == "exp", **{f"len_{m}": v for m, v in C.per_row_len[(lid, k)].items()},
                     "registered": {kk: v for kk, v in L.reg[k].items() if kk not in ("status", "policies", "scored")},
                     "diag": {v: C.diag[lid][v].get(k) for v in C.diag[lid]}}
                f.write(json.dumps(d, ensure_ascii=False, sort_keys=True, default=_default) + "\n")


def write_manifest(C):
    inputs = [DS / "views.json", DS / "policies.json", DS / "stage1.json", RUN / "cell_ds.json", RUN / "stage1_amend1.json", RUN / "lock_amend2.json", RUN / "lock_amend3.json",
              RUN / "rows_ds.jsonl", RUN / "rows_ds_amend1.jsonl", RUN / "rows_ds_amend2.jsonl", RUN / "rows_ds_amend2_h45.jsonl", RUN / "rows_ds_amend3_mini.jsonl", RUN / "rows_ds_amend3_h45.jsonl",
              RUN / "scores_ds.json", RUN / "scores_amend1.json", RUN / "scores_amend2.json", RUN / "scores_amend3.json", L2 / "question_emb.npz", L2 / "retrieval.json",
              DS / "tools" / "run_ds.py", DS / "tools" / "ds_common.py", DS / "tools" / "prompts_ds.py", ROOT / "registrations" / "ADDENDUM_DS.md", ROOT / "registrations" / "ADDENDUM_DS_AMENDMENT_3.md"]
    vers = {"python": sys.version.split()[0], "numpy": np.__version__}
    try:
        import scipy, sentence_transformers, torch                            # noqa: E401
        vers.update({"scipy": scipy.__version__, "sentence_transformers": sentence_transformers.__version__, "torch": torch.__version__})
    except Exception:                                                         # noqa: BLE001
        pass
    man = {"when": dt.datetime.now().isoformat(timespec="seconds"), "script_sha256": sha_f(__file__), "inputs_sha256": {str(p.relative_to(ROOT)).replace("\\", "/"): sha_f(p) for p in inputs},
           "outputs_sha256": {p.name: sha_f(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name not in ("manifest.json",)},
           "versions": vers, "checks": C.checks, "constants": {"TAU_GOLD": TAU_GOLD, "TAU_HI": TAU_HI, "MIN_SHARED": MIN_SHARED, "MIN_DISCR": MIN_DISCR, "CROSS_GUARD": CROSS_GUARD},
           "no_api_calls": True, "writes": ["reviews/downstream_audit/*"]}
    jdump(man, OUT / "manifest.json")
    return man


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", default="1,2,3,4,5,6,7")
    ap.add_argument("--skip-embed", action="store_true")
    ap.add_argument("--force-gates", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    C = load_ctx()
    ok = gate_detector(C) & gate_retrieval(C) & gate_views(C) & gate_prompts(C)
    if not ok and not a.force_gates:
        print("GATES FAILED -- STOP"); sys.exit(2)
    steps = {int(s) for s in a.steps.split(",") if s.strip()}
    if 1 in steps:
        step1(C)
    if 2 in steps:
        step2(C)
    if 3 in steps or 7 in steps:
        step3(C)
    if 4 in steps:
        step4(C)
        step4b(C)
    if 5 in steps:
        step5(C, a.skip_embed)
    if 6 in steps:
        step6(C)
    if 7 in steps:
        step7(C)
        write_master(C)
    write_manifest(C)
    print("checks:", sum(1 for c in C.checks if c["ok"]), "PASS,", sum(1 for c in C.checks if not c["ok"]), "FAIL")


if __name__ == "__main__":
    main()
