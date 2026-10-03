# -*- coding: utf-8 -*-
"""r130_common.py -- program R130 (KtS: a stronger answerer, and a judge the human labels can validate; exploratory).

Paths, the registration assertion, the pinned inputs, the population loaders and the judge-unit renderer that every tool of the
program shares. NO API CALL is made here. Fenced: writes only under reviews/r130/ and ds_downstream/run/*r130* (rows, probes, lock,
projection, batch records) and one appended section of ds_downstream/NUMBERS_DS.md; never reviews/v22/, reviews/r125/ or
human_validation/.

Population (read from the recorded artifacts, never re-answered):
  the 231 distinct (obligation, view) pairs the E.10 answer stage called under the seven DS policies with the Amendment 4 header
  (rows_ds_amend4_{mini,h45}.jsonl, label PRESENT-NEGATIVE), and the 74 views the reference-assisted retag changed
  (views_amend5.json; rows_ds_amend5_{mini,h45}.jsonl): 305 views over the 104 obligations (99 reached by some policy).
Judge units: one per recorded answer of GPT-4.1 mini and Claude Haiku 4.5 on those 305 views (610) plus one per Luna answer (305).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
R130 = ROOT / "reviews" / "r130"
BUILD, RES, REGS = R130 / "build", R130 / "results", R130 / "registrations"
REG = REGS / "REGISTRATION_R130.md"
FREEZE = R130 / "FREEZE_R130.md"
DEVIATIONS = R130 / "DEVIATIONS_R130.md"
DS = ROOT / "ds_downstream"
RUN = DS / "run"
LEDGER = DS / "NUMBERS_DS.md"
HV1 = ROOT / "human_validation" / "hv1"
for p in ("ds_downstream/tools", "e0_metamemory/tools", "e1_metamemory/tools", "r82_counterfactual", "r82_counterfactual/tools",
          "e1r_robustness/tools", "resp_review/tools"):
    sys.path.insert(0, str(ROOT / p))

PROGRAM = "R130"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
LABELS = ["ASSERTS", "MENTIONS", "CLEAN", "ABSTAINS", "UNSURE"]
ANSWERERS = ("MINI", "H45", "LUNA")
ANSWERER_NAME = {"MINI": "GPT-4.1 mini", "H45": "Claude Haiku 4.5", "LUNA": "GPT-5.6 Luna"}
POLICIES = ("ALWAYS", "MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT", "ORACLE")
NAMED_POLICIES = ("ALWAYS", "LOOKUP", "MODEL", "ORACLE")          # the brief's named policies with recorded answers
POLICY_NAME = {"ALWAYS": "Top-five retrieval", "MODEL": "Model rule", "LOOKUP": "Lookup rule", "MODEL-ALL": "Model rule, all states",
               "LOOKUP-ALL": "Lookup rule, all states", "LOOKUP-LIT": "Literal lookup rule", "ORACLE": "Oracle", "RETAG": "Retag variant (diagnostic)"}
CAP = {"openai": 4.00, "anthropic": 8.00}
N_BOOT, SEED_BOOT = 10000, 42
EXPECT = {"views_a4_pn": 231, "views_a5": 74, "views_total": 305, "obligations": 104, "obligations_reached": 99, "units_recorded": 610,
          "lookup_answered": 70, "oracle_answered": 99, "pl1_pairs": 82, "pl1b_pairs": 61, "pl2_pairs": 40, "pl2_same_view": 24,
          "pl3_active": 35, "pl3_without": 50, "pl3b_active": 17, "pl3b_without": 41, "hv_key_items": 248}
UNSURE_MODES = ("primary", "drop")     # primary: UNSURE is not ASSERTS and not MENTIONS; drop: a unit labelled UNSURE leaves every pairing it enters (the sensitivity row)

# pinned inputs: path -> sha256 of the working bytes (HV1's pins where HV1 pinned the file; the others pinned here at Phase 0)
INPUTS = {
    "ds_downstream/run/rows_ds_amend4_mini.jsonl": "9ddc9f2638b6a29759c0aa5f7c34b27a3a6a95bb7da56d5d97620dd92af58b24",
    "ds_downstream/run/rows_ds_amend4_h45.jsonl": "2f26e9332c7594cdb92f19af303f157f2608a83a3ea12f664524976b63008ec8",
    "ds_downstream/run/rows_ds_amend5_merged_mini.jsonl": "b96ddcb2c52256e69ecbe0e87f0dd130075e2559408dbc289e3d35d86f8f65c9",
    "ds_downstream/run/rows_ds_amend5_merged_h45.jsonl": "4d34ad8f53c51a1e2618ad87dcefb31593f86ce3ad43c95e723ab82985b68d37",
    "ds_downstream/run/scores_amend4.json": "a28a58595d8de7f47db93f91c30e8b73be1a1569c2a5d81645a7f12ce042b661",
    "ds_downstream/run/scores_amend5.json": "64cfb720d5a8dee158d216abfabdefd96eb6caa65bec7357a9f831b1225dd443",
    "ds_downstream/run/views_amend5.json": "db120fef3cb452d13eb8bfc1e175b9dc580f42298b3196048199f560acc17d1d",
    "human_validation/hv1/key/key_hv1.json": "e8ea5bc1e38365a8b433ac801f0b1aafe7c809a78236b5d7a6aeb3602fd0f1c8",   # pinned at Phase 0 (2026-09-20)
    "human_validation/hv1/inputs/hva_rows.json": "f0ba8ec949b14b08a8077d5317711670ab65d3d24f45f73e9271b71e1dbbfb1d",
    "ds_downstream/run/rows_ds_amend5_mini.jsonl": "fdfa2ca33a33df2b79060764f7d71dad2866ae25c69340fe6af3dc3cd7f78517",
    "ds_downstream/run/rows_ds_amend5_h45.jsonl": "ee05348247656bf57506651e7a86e9782d044093cc079ec0b2eada3040887e5d",
    "ds_downstream/stage1.json": "6691654d3dfd23595d077e717cf30fb4c76880275e0115996a4b1b3dabb29a8f",
    "ds_downstream/views.json": "6d3cb6c7b863c4815a2af71af9cfaef00b8334ca3e4f25886f204d9af1d17d48",
    "ds_downstream/run/cell_ds.json": "e46d7b95da2a4e53ce85a9a5abeeceb72129df906298ec77112081ea7b641c0e",
}


# ------------------------------------------------------------------ hashing and assertions
def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_text(s: str) -> str:
    return sha_bytes(s.encode("utf-8"))


def sha_file(p) -> str:
    return sha_bytes(pathlib.Path(p).read_bytes())


def reg_sha(path=REG) -> str:
    b = pathlib.Path(path).read_bytes(); i = b.find(FROZEN_END)
    assert i > 0, f"no marker line in {path}"
    return sha_bytes(b[:i])


def freeze_table():
    """{file: registered-text sha256} from FREEZE_R130.md (the registration row)."""
    out = {}
    if not FREEZE.exists():
        return out
    for ln in io.open(FREEZE, encoding="utf-8"):
        if ln.startswith("| ") and "`REGISTRATION_R130.md`" in ln:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            out["REGISTRATION_R130.md"] = cells[1].strip("`")
    return out


def assert_frozen():
    """The registration's registered text matches FREEZE_R130.md; called by every tool that calls an API or scores."""
    tab = freeze_table(); got = reg_sha()
    assert "REGISTRATION_R130.md" in tab, "FREEZE_R130.md carries no registration row -- STOP (no call before the freeze)"
    assert got == tab["REGISTRATION_R130.md"], f"REGISTRATION SHA MISMATCH {got} -- STOP"
    return got


def assert_inputs(pins=None):
    """Every pinned input's working bytes hash as pinned. pins: {path: sha} to check (default: the non-None entries of INPUTS)."""
    pins = pins or {k: v for k, v in INPUTS.items() if v}
    bad = []
    for rel, want in pins.items():
        got = sha_file(ROOT / rel)
        if got != want:
            bad.append((rel, got[:16], want[:16]))
    assert not bad, f"INPUT DIGEST MISMATCH -- STOP: {bad}"
    return {k: v for k, v in pins.items()}


def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def J(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(obj, p):
    pathlib.Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")


def read_rows(p):
    out = {}
    for l in io.open(p, encoding="utf-8"):
        if l.strip():
            r = json.loads(l); out[r["key"]] = r
    return out


def append_rows(p, rows):
    pathlib.Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "a", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")


def append_ledger(title, text):
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"\n### {title}\n\n{text}\n")


def append_deviation(text):
    DEVIATIONS.parent.mkdir(parents=True, exist_ok=True)
    new = not DEVIATIONS.exists()
    with io.open(DEVIATIONS, "a", encoding="utf-8", newline="\n") as f:
        if new:
            f.write("# DEVIATIONS_R130 -- program R130, dated entries (the registration's section 9)\n")
        f.write(f"\n- **{now()}** {text}\n")


# ------------------------------------------------------------------ the recorded population
def load_ds():
    """The DS cell, the per-item records (stale / gold fields), stage 1, the recorded views, the 452 Amendment 4 jobs with view text."""
    import amend4_header as A4  # noqa: E402  (imports run_ds, ds_common; asserts prompts_e1 / prompts_ds digests at use)
    import run_ds as RD  # noqa: E402
    import ds_common as DC  # noqa: E402
    sub = DC.load_cell(); rec = RD.records(sub)
    st1 = J(DS / "stage1.json")["per_item"]; views = J(DS / "views.json")["items"]
    sub_, hj = A4.jobs()
    return {"sub": sub, "byid": {it["item_id"]: it for it in sub}, "rec": rec, "st1": st1, "views": views, "jobs": hj, "A4": A4, "RD": RD}


def reference_for(it, rec):
    """(old value no longer true, true now) as the HV1 workbook printed them: stale_field / gold_field for supersession and retraction;
    for expiry the event as the old value and 'date passed' (build_hv1.practice_candidates' rule)."""
    if it["state"] == "exp":
        return rec["gold_field"], "date passed"
    return rec["stale_field"], rec["gold_field"]


def luna_jobs(D=None):
    """The 305 views: the 231 PRESENT-NEGATIVE views of the Amendment 4 population (source 'a4') and the 74 retag views (source 'a5')."""
    D = D or load_ds()
    pn = [j for j in D["jobs"] if j["label"] == "PRESENT-NEGATIVE"]
    assert len(pn) == EXPECT["views_a4_pn"], len(pn)
    # the same set derived from stage 1: reached and not abstained under some policy
    want = set()
    for it in D["sub"]:
        if it["label"] != "PRESENT-NEGATIVE":
            continue
        for p in POLICIES:
            s = D["st1"][it["item_id"]][p]
            if s["reach"] and not s["abstain"]:
                want.add(f"{it['item_id']}|{D['views'][it['item_id']][p]['sha']}")
    assert want == {j["key"] for j in pn}, "the 231 PN views differ from stage 1's reached-and-answered set -- STOP"
    out = []
    for j in pn:
        out.append({**{k: j[k] for k in ("key", "item_id", "persona", "question", "label", "state", "view", "view_sha", "n_lines", "policies")}, "source": "a4", "key_a4": j["key"]})
    ch = J(RUN / "views_amend5.json")["changed"]
    assert len(ch) == EXPECT["views_a5"], len(ch)
    for k, c in ch.items():
        assert c["key_a4"] == k and c["key"] == f"{c['item_id']}|{c['view_sha']}" and c["label"] == "PRESENT-NEGATIVE"   # the dict is keyed by the Amendment 4 key
        out.append({**{kk: c[kk] for kk in ("key", "item_id", "persona", "question", "label", "state", "view", "view_sha", "n_lines", "policies", "key_a4", "view_sha_a4", "ranks_tagged", "tag")}, "source": "a5"})
    assert len(out) == EXPECT["views_total"] and len({j["key"] for j in out}) == EXPECT["views_total"]
    return out


def recorded_answers():
    """{(answerer, source, key): row} for GPT-4.1 mini and Haiku 4.5 on the 305 views, from the recorded rows files."""
    out = {}
    for code, fa4, fa5 in (("MINI", "rows_ds_amend4_mini.jsonl", "rows_ds_amend5_mini.jsonl"), ("H45", "rows_ds_amend4_h45.jsonl", "rows_ds_amend5_h45.jsonl")):
        a4 = read_rows(RUN / fa4); a5 = read_rows(RUN / fa5)
        merged = read_rows(RUN / fa4.replace("amend4", "amend5_merged"))
        for k, r in a4.items():
            if r["label"] == "PRESENT-NEGATIVE":
                out[(code, "a4", k)] = r
        for k, r in a5.items():
            m = merged.get(r["key_a4"])   # the merged file keeps the Amendment 4 key on the changed views
            assert m is not None and m["answer"] == r["answer"] and m.get("source") == "amend5 call (changed view)" and m["view_sha"] == r["view_sha"], ("merged file differs from the Amendment 5 rows", code, k)
            out[(code, "a5", k)] = r
    return out


def judge_units(D=None, luna_rows=None):
    """One unit per recorded answer: the 610 mini / Haiku units, plus one per Luna row when given. Units carry the reference strings
    the judge sees and nothing the judge must not see is passed to the prompt (policy, answerer, flag stay in the unit record only)."""
    D = D or load_ds(); jobs = {j["key"]: j for j in luna_jobs(D)}; rec_rows = recorded_answers()
    units = []
    for (code, src, key), r in sorted(rec_rows.items()):
        j = jobs[key]; it = D["byid"][j["item_id"]]; rc = D["rec"][j["item_id"]]
        stale, gold = reference_for(it, rc)
        units.append({"unit_id": f"{code}|{src}|{key}", "answerer": code, "source": src, "key": key, "key_a4": j["key_a4"], "item_id": j["item_id"], "persona": j["persona"],
                      "state": j["state"], "policies": list(j["policies"]), "question": j["question"], "stale": stale, "gold": gold, "answer": r["answer"], "status": r["status"]})
    if luna_rows is not None:
        for key, r in sorted(luna_rows.items()):
            j = jobs[key]; it = D["byid"][j["item_id"]]; rc = D["rec"][j["item_id"]]
            stale, gold = reference_for(it, rc)
            units.append({"unit_id": f"LUNA|{j['source']}|{key}", "answerer": "LUNA", "source": j["source"], "key": key, "key_a4": j["key_a4"], "item_id": j["item_id"], "persona": j["persona"],
                          "state": j["state"], "policies": list(j["policies"]), "question": j["question"], "stale": stale, "gold": gold, "answer": r.get("answer"), "status": r["status"]})
    return units


def lock_against_hv1_key(units):
    """Every HV-A key item (248: 148 primary + 50 controls + 50 Haiku block) maps to exactly one unit whose question / old value / true now /
    answer strings equal the key's; returns {hv uid: unit_id}. A mismatch is a STOP: the judge and the human must have seen the same text."""
    key = J(HV1 / "key" / "key_hv1.json"); items = key["hva"]["items"]
    assert len(items) == EXPECT["hv_key_items"], len(items)
    by_a4 = {(u["answerer"], u["source"], u["key_a4"]): u for u in units if u["answerer"] in ("MINI", "H45")}
    out, bad = {}, []
    for uid, x in items.items():
        src = "a5" if x["cond"] == "after" else "a4"          # before and control answers are Amendment 4 rows; after answers Amendment 5 rows
        u = by_a4.get((x["model"], src, x["key"]))
        if u is None:
            bad.append((uid, "no unit")); continue
        if (u["question"], u["stale"], u["gold"], u["answer"]) != (x["question"], x["stale"], x["gold"], x["answer"]):
            bad.append((uid, "strings differ")); continue
        out[uid] = u["unit_id"]
    assert not bad, f"HV1 KEY LOCK FAILS -- STOP: {bad[:5]} ({len(bad)})"
    return out


# ------------------------------------------------------------------ the judge prompt (frozen in the registration; asserted there)
JUDGE_SYSTEM = (
    "You label an answer that an assistant wrote to a question a user asked about themselves. Each item has the question, an old value that "
    "is no longer true, the value that is true now, and the answer. Pick exactly one label:\n"
    "- ASSERTS: the answer treats the old value as true now. Example: the user cancelled a trip, and the answer tells them what to pack for it.\n"
    "- MENTIONS: the old value appears, but the answer says it is in the past, changed or cancelled, or explains why it no longer holds. "
    "Example: \"You used to prefer tea, and now you prefer coffee.\"\n"
    "- CLEAN: the old value does not appear at all, and the answer does answer the question.\n"
    "- ABSTAINS: the answer refuses, says it does not know, or gives nothing usable. Example: \"I don't have enough information about that.\"\n"
    "- UNSURE: you really cannot decide. Use this rarely and say why in the reason.\n"
    "Judge only what the answer says. Do not judge whether the answer is polite, complete or well written.\n"
    "\n"
    "Return JSON only, the reason first: {\"reason\": \"<one sentence>\", \"label\": \"<ASSERTS or MENTIONS or CLEAN or ABSTAINS or UNSURE>\"}"
)
JUDGE_USER = (
    "Question: {question}\n"
    "Old value (no longer true): {stale}\n"
    "True now: {gold}\n"
    "Answer: {answer}"
)


def judge_messages(u):
    return JUDGE_SYSTEM, JUDGE_USER.format(question=u["question"], stale=u["stale"], gold=u["gold"], answer=u["answer"])


def judge_digests():
    return {"JUDGE_SYSTEM": sha_text(JUDGE_SYSTEM), "JUDGE_USER": sha_text(JUDGE_USER)}


def registered_judge_texts(path=REG):
    """The two judge texts as the registration prints them (its fenced blocks), for the assertion at lock and before any judge call."""
    s = io.open(path, encoding="utf-8").read()
    i = s.index("`JUDGE_SYSTEM`:\n```\n") + len("`JUDGE_SYSTEM`:\n```\n"); j = s.index("\n```\n\n`JUDGE_USER`:", i)
    k = s.index("`JUDGE_USER`:\n```\n") + len("`JUDGE_USER`:\n```\n"); l = s.index("\n```\n", k)
    return {"JUDGE_SYSTEM": s[i:j], "JUDGE_USER": s[k:l]}


def assert_judge_prompt():
    got = registered_judge_texts()
    assert got["JUDGE_SYSTEM"] == JUDGE_SYSTEM and got["JUDGE_USER"] == JUDGE_USER, "the judge prompt differs from the frozen registration -- STOP"


# ------------------------------------------------------------------ statistics
def wilson(k, n, z=1.959964):
    import math
    if not n:
        return None
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 4), round(c + h, 4)]


def mcnemar_exact(b, c):
    """Two-sided exact McNemar: the binomial test of b against b + c at 0.5 (b, c the two discordant counts)."""
    from scipy.stats import binomtest
    n = b + c
    if n == 0:
        return 1.0
    return float(binomtest(b, n, 0.5).pvalue)


def fisher(a, b, c, d):
    from scipy.stats import fisher_exact
    return float(fisher_exact([[a, b], [c, d]])[1])


def boot_paired(a, b, personas, n_boot=N_BOOT, seed=SEED_BOOT):
    """mean(b - a) over paired items; item-level and persona-grouped percentile bootstraps (amend4_header.boot_paired's construction)."""
    import collections
    import numpy as np
    a = np.asarray(a, float); b = np.asarray(b, float); d = b - a; n = len(d)
    if n == 0:
        return {"delta": None, "item": None, "cluster": None, "n": 0, "n_clusters": 0}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n)); item = d[idx].mean(axis=1)
    groups = collections.defaultdict(list)
    for i, p in enumerate(personas):
        groups[p].append(i)
    keys = sorted(groups); G = len(keys)
    rng2 = np.random.default_rng(seed); cl = np.empty(n_boot)
    for t in range(n_boot):
        pick = rng2.integers(0, G, size=G)
        ids = np.concatenate([groups[keys[g]] for g in pick])
        cl[t] = d[ids].mean()
    return {"delta": round(float(d.mean()), 4), "item": [round(float(np.percentile(item, 2.5)), 4), round(float(np.percentile(item, 97.5)), 4)],
            "cluster": [round(float(np.percentile(cl, 2.5)), 4), round(float(np.percentile(cl, 97.5)), 4)], "n": n, "n_clusters": G, "n_boot": n_boot, "seed": seed}


def boot_two_group(y1, p1, y0, p0, n_boot=N_BOOT, seed=SEED_BOOT):
    """rate(y1) - rate(y0) for two groups of items; item-level (each group resampled) and persona-grouped (personas resampled over the
    union, the difference of the two group rates on the resample) percentile bootstraps."""
    import collections
    import numpy as np
    y1 = np.asarray(y1, float); y0 = np.asarray(y0, float)
    if len(y1) == 0 or len(y0) == 0:
        return {"delta": None, "item": None, "cluster": None, "n1": len(y1), "n0": len(y0)}
    rng = np.random.default_rng(seed)
    i1 = rng.integers(0, len(y1), size=(n_boot, len(y1))); i0 = rng.integers(0, len(y0), size=(n_boot, len(y0)))
    item = y1[i1].mean(axis=1) - y0[i0].mean(axis=1)
    g1 = collections.defaultdict(list); g0 = collections.defaultdict(list)
    for i, p in enumerate(p1):
        g1[p].append(i)
    for i, p in enumerate(p0):
        g0[p].append(i)
    keys = sorted(set(g1) | set(g0)); G = len(keys)
    rng2 = np.random.default_rng(seed); cl = []
    for t in range(n_boot):
        pick = rng2.integers(0, G, size=G)
        a = [i for g in pick for i in g1.get(keys[g], [])]; b = [i for g in pick for i in g0.get(keys[g], [])]
        if a and b:
            cl.append(y1[a].mean() - y0[b].mean())
    cl = np.asarray(cl)
    return {"delta": round(float(y1.mean() - y0.mean()), 4), "item": [round(float(np.percentile(item, 2.5)), 4), round(float(np.percentile(item, 97.5)), 4)],
            "cluster": [round(float(np.percentile(cl, 2.5)), 4), round(float(np.percentile(cl, 97.5)), 4)], "n1": int(len(y1)), "n0": int(len(y0)), "n_clusters": G,
            "n_boot": n_boot, "seed": seed, "cluster_draws_kept": int(len(cl))}


def kappa(pairs, cats):
    """Cohen's unweighted kappa over (a, b) label pairs restricted to cats."""
    import collections
    pairs = [(a, b) for a, b in pairs if a in cats and b in cats]
    n = len(pairs)
    if n == 0:
        return None, 0
    po = sum(1 for a, b in pairs if a == b) / n
    ca = collections.Counter(a for a, _ in pairs); cb = collections.Counter(b for _, b in pairs)
    pe = sum(ca[c] * cb[c] for c in cats) / (n * n)
    return (None if pe == 1 else round((po - pe) / (1 - pe), 4)), n
