"""resp_common.py -- shared loaders and the frozen censuses for the review-response lanes
(registrations/ADDENDUM_RESP.md, frozen 17e6328). NO API CALLS. Deterministic.

Consumers: verify_resp.py (every §C pin), build_l1.py (the V2-OWN texts, §L1), build_l2.py (the
TRUE lifecycle flags and the retrieved-line renderer, §L2), run_resp.py (the cell and the scorer).

What is here, and where each rule comes from:
  population        the 661 / 104 obligation cell and the 307 / 35 coverage cell, joined exactly as
                    common_e1r.assemble joins them (R-NOK-FRB / R-FOK-FRB); index_key per item
  section lock      §C.2: the superseded-names section of every committed TRUE index re-rendered
                    from its parsed names through name_block's rule (index_v3._name_block, which is
                    v2's flat-case rule verbatim) and compared byte for byte; the section is the tail
  own-name census   §C.1, keyed by (persona, entry id): pn_members slots against the section names
  L1 census         §C.2: T(q), tau = p99 of the token-disjoint name-name null under NB-6's encoder,
                    the removed set per item (own names and neighbours at cosine >= tau), the counts;
                    reviews/RESP_REG_REPORT.md appendix (census_l1.py), moved here verbatim in effect
  V2-OWN surgery    §L1: prefix up to the section header untouched; body re-rendered over the names
                    that remain; (none) when empty
  TRUE flags        §L2: index_v2.true_lifecycle per persona (variant-invariant); ages per index_v2 R3
  line renderer     §L2: "[r] lifecycle: ... | category: ... | attribute: ... | age: N days | text: ..."
"""
from __future__ import annotations

import collections
import hashlib
import io
import json
import os
import pathlib
import sys

import numpy as np

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

ROOT = pathlib.Path(__file__).resolve().parents[2]
for _p in ("e0_metamemory/tools", "e1_metamemory/tools", "e1r_robustness/tools", "r82_counterfactual"):
    if str(ROOT / _p) not in sys.path:
        sys.path.insert(0, str(ROOT / _p))

import index_v2 as IX                                                        # noqa: E402
from index_v2 import scrub, true_lifecycle, parse_dt, toks as e0_toks         # noqa: E402
from index_v3 import _name_block                                             # noqa: E402
from e0_common import load_joins                                             # noqa: E402
from backends import load_backend                                            # noqa: E402
from common_e1r import load_e1, POPULATIONS, auroc                           # noqa: E402
from index_features import index_key, indexes, parse, toks as if_toks        # noqa: E402
from nb6_composition import AV_STATE                                         # noqa: E402

E1 = ROOT / "e1_metamemory"
RESP = ROOT / "resp_review"
L1, L2, RUN, CACHE = RESP / "l1", RESP / "l2", RESP / "run", RESP / "cache"
LEDGER = RESP / "NUMBERS_RESP.md"
FREEZE = "17e6328"
BASELINE = "2a943d7"
TAU_HI = 0.80
HDR2 = "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT  (value-scrubbed)"
STATE3 = {"superseded": "sup", "expired": "exp", "retracted": "ret"}

# sha256 pins on the frozen lineage (values at the freeze commit; every file unchanged since)
PINS = {
    "e1_metamemory/tools/index_v2.py": "baeaab11e1b5e94d",
    "e1r_robustness/tools/index_features.py": "4a2e634d1ec108e1",
    "e1r_robustness/tools/common_e1r.py": "ab3581f5b6ec2db2",
    "e1r_robustness/tools/run_nb6.py": "3474120eaa4b7755",
    "e1r_robustness/tools/nb6_composition.py": "70dd1f11fe12e65c",
    "e0_metamemory/tools/e0_common.py": "2fcbbc88d78e1df9",
    "lifecycle_bank.py": "2db34a317149a5d6",
    "e1_metamemory/tools/prompts_e1.py": "337d37d3414c0482",
    "r82_counterfactual/index_v3.py": "e4ea6193f6adfa19",
    "e1_metamemory/elicitation_main.json": "3e1f3940a63504eb",
    "e1_metamemory/indexes_v2.json": "a54152bf3698cfbf",
    "r74/x4/cell_661.json": "01ed4c05fc57c0b2",
}
PIN_PROMPTS = {"file": "337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84",
               "texts": "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"}


def J(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(obj, p):
    pathlib.Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, sort_keys=True, default=float)
        f.write("\n")


def sha(p, n=16):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:n]


def sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


_API = {}


def e1_api():
    """e1_metamemory/tools/api.py loaded by file path (the shared sys.path resolves `api` to E0's
    module); it wraps E0's client under `_e0` with prompts_e1's decoding parameters."""
    if "m" not in _API:
        import importlib.util as ilu
        spec = ilu.spec_from_file_location("api_e1", ROOT / "e1_metamemory" / "tools" / "api.py")
        m = ilu.module_from_spec(spec)
        sys.modules["api_e1"] = m
        spec.loader.exec_module(m)
        _API["m"] = m
    return _API["m"]


# ------------------------------------------------------------------ population
def load_cell():
    """The 661 obligation items with the committed rows attached; asserted 661 / 104 / 307 / 35."""
    items, blind, idxT, idxB = load_e1()
    sub = []
    for it in items:
        if not POPULATIONS["R-NOK-FRB"]["filt"](it):
            continue
        q, tag = it["question"], it["item_id"]
        if q not in blind or tag not in idxT or blind[q].get("nok") is None or idxT[tag].get("nok") is None:
            continue
        it = dict(it)
        lab = it.get("label", it["label_pre"])
        it["label"] = lab
        it["y_nok"] = 1 if lab == "PRESENT-NEGATIVE" else 0
        it["y_fok"] = 0 if lab == "ABSENT" else 1
        it["state"] = STATE3[AV_STATE[it["attack_vector"]]] if lab == "PRESENT-NEGATIVE" else "-"
        it["index_key"] = index_key(it, "TRUE")
        it["true"] = idxT[tag]
        it["blind"] = blind[q]
        sub.append(it)
    c661 = J(ROOT / "r74/x4/cell_661.json")
    assert (len(sub), sum(i["y_nok"] for i in sub)) == (661, 104), (len(sub), sum(i["y_nok"] for i in sub))
    assert {i["item_id"] for i in sub} == {i["item_id"] for i in c661["items"]}
    ck = {i["item_id"]: i for i in c661["items"]}
    assert all(ck[i["item_id"]]["index_key"] == i["index_key"] for i in sub), "index_key mismatch against cell_661"
    hard = [i for i in sub if i["tier"] == "hard"]
    assert (len(hard), sum(i["y_fok"] for i in hard)) == (307, 35), (len(hard), sum(i["y_fok"] for i in hard))
    assert collections.Counter(i["state"] for i in sub if i["y_nok"]) == {"sup": 63, "ret": 26, "exp": 15}
    return sub


def slot_map_persona():
    return {(e["persona"], e["entry_id"]): e["slot"] for e in J(E1 / "backend_entries" / "frbank.json")}


# ------------------------------------------------------------------ the section and its lock
def section_names(text):
    """The parsed superseded-names of an index text through index_features.parse (the committed
    parser; '(none)' is returned as a name because _names does not special-case it)."""
    return list(parse(text)["superseded_attrs"])


def split_section(text):
    i = text.index(HDR2)
    return text[:i], text[i:]


def render_section(names):
    """name_block's flat-case rule: sorted set, cap 15, wrap 150, indents '  ' / '    ', (none) when empty."""
    real = [n for n in names if n != "(none)"]
    return "\n".join(_name_block(real, HDR2))


def section_lock(keys=None):
    idx = indexes()
    keys = keys or sorted(k for k in idx if k.startswith("frbank:") and k.endswith(":TRUE"))
    ok, bad = 0, []
    for k in keys:
        prefix, tail = split_section(idx[k])
        if render_section(section_names(idx[k])) == tail:
            ok += 1
        else:
            bad.append(k)
    return ok, bad


def own_text(committed, remaining):
    """§L1 V2-OWN: every byte before the section header untouched; body re-rendered over `remaining`."""
    prefix, _ = split_section(committed)
    return prefix + render_section(remaining)


# ------------------------------------------------------------------ §C.1 own-name census
def own_name_census(sub, provenance):
    slots = slot_map_persona()
    out = collections.Counter()
    for it in sub:
        if not it["y_nok"]:
            continue
        sec = {s.strip().lower() for s in section_names(indexes()[index_key(it, provenance)])}
        mine = {scrub(slots[(it["persona"], m)]) for m in it["pn_members"] if slots.get((it["persona"], m))}
        if mine & sec:
            out[it["state"]] += 1
            out["all"] += 1
    return dict(out)


# ------------------------------------------------------------------ §C.2 L1 census (census_l1.py)
_ENC = {}


def encoder():
    if "m" not in _ENC:
        from run_baselines import encoder as _e
        _ENC["m"] = _e()
    return _ENC["m"]


def l1_census(sub):
    """T(q), tau, the removed set per item. Returns (tau, null_stats, rows, name_vocab_size, pairs)."""
    joins = load_joins()
    slot = slot_map_persona()
    keys = sorted({it["index_key"] for it in sub})
    idx = indexes()
    sec = {k: [n for n in section_names(idx[k]) if n != "(none)"] for k in keys}
    names = sorted({n for k in keys for n in sec[k]})
    enc = encoder()
    V = enc.encode([n.replace("_", " ") for n in names], normalize_embeddings=True)
    S = V @ V.T
    ix = {n: i for i, n in enumerate(names)}
    tk = {n: if_toks(n.replace("_", " ")) for n in names}
    null = [float(S[i, j]) for i in range(len(names)) for j in range(i + 1, len(names)) if not (tk[names[i]] & tk[names[j]])]
    tau = float(np.percentile(null, 99))
    null_stats = {"n_pairs": len(null), "median": float(np.median(null)), "p90": float(np.percentile(null, 90)),
                  "p95": float(np.percentile(null, 95)), "p99": tau, "max": float(max(null))}
    pairs = {tuple(sorted(p)) for k in keys for p in __import__("itertools").combinations(sec[k], 2)}
    vo_cache = {}

    def targets(it):
        p, Jp, qid = it["persona"], joins[it["persona"]], it["question_id"]
        own = set()
        for m in it.get("pn_members") or []:
            if slot.get((p, m)):
                own.add(scrub(slot[(p, m)]))
        has_join = qid in Jp.gold
        if has_join:
            g = Jp.gold[qid] or set()
            f = {i for i, s in (Jp.fires[qid] or {}).items() if s >= TAU_HI}
            x = Jp.expired_neg[qid] or set()
            for e in g | f | x:
                if slot.get((p, e)):
                    own.add(scrub(slot[(p, e)]))
        return own, has_join

    rows = []
    for it in sub:
        s = sec[it["index_key"]]
        own, has_join = targets(it)
        own_in = {n for n in s if n in own}
        nb = {n for n in s if n not in own and any(S[ix[n], ix[o]] >= tau for o in own if o in ix)}
        for o in own:
            if o in ix:
                continue
            if o not in vo_cache:
                vo_cache[o] = enc.encode([o.replace("_", " ")], normalize_embeddings=True)[0]
            for n in s:
                if n not in own and float(V[ix[n]] @ vo_cache[o]) >= tau:
                    nb.add(n)
        removed = own_in | nb
        rows.append({"item_id": it["item_id"], "index_key": it["index_key"], "variant": it["variant"], "label": it["label"],
                     "state": it["state"], "natural": it.get("absent_mechanism") == "natural",
                     "n_sec": len(s), "n_own": len(own), "own": sorted(own), "section": s,
                     "removed": sorted(removed), "reason": {n: ("own" if n in own_in else "neighbour") for n in sorted(removed)},
                     "changed": bool(removed), "emptied": bool(s) and len(removed) == len(s), "has_join": has_join,
                     "remaining": [n for n in s if n not in removed]})
    return tau, null_stats, rows, names, pairs


def census_counts(rows):
    c = {}
    c["changed"] = sum(r["changed"] for r in rows)
    for lab, key in (("PRESENT-NEGATIVE", "pn"), ("PRESENT", "present"), ("ABSENT", "absent")):
        c[key] = (sum(1 for r in rows if r["label"] == lab), sum(1 for r in rows if r["label"] == lab and r["changed"]))
    c["absent_natural_changed"] = sum(1 for r in rows if r["label"] == "ABSENT" and r["natural"] and r["changed"])
    for st in ("sup", "ret", "exp"):
        c[st] = (sum(1 for r in rows if r["state"] == st), sum(1 for r in rows if r["state"] == st and r["changed"]),
                 sum(1 for r in rows if r["state"] == st and r["emptied"]))
    for v in ("FULL", "CAT-ABLATED", "SLOT-ABLATED"):
        c[v] = (sum(1 for r in rows if r["variant"] == v), sum(1 for r in rows if r["variant"] == v and r["changed"]))
    c["emptied"] = sum(1 for r in rows if r["emptied"])
    c["neighbour_items"] = sum(1 for r in rows if any(v == "neighbour" for v in r["reason"].values()))
    c["T_sizes"] = dict(collections.Counter(min(r["n_own"], 5) for r in rows))
    c["unchanged"] = sum(1 for r in rows if not r["changed"])
    c["keys_none"] = len({r["index_key"] for r in rows if r["n_sec"] == 0})
    c["items_none"] = sum(1 for r in rows if r["n_sec"] == 0)
    return c


EXPECT_C2 = {"changed": 102, "pn": (104, 74), "present": (174, 16), "absent": (383, 12), "absent_natural_changed": 0,
             "sup": (63, 63, 30), "ret": (26, 11, 4), "exp": (15, 0, 0),
             "FULL": (323, 46), "CAT-ABLATED": (176, 16), "SLOT-ABLATED": (162, 40),
             "emptied": 41, "neighbour_items": 6, "T_sizes": {0: 145, 1: 219, 2: 152, 3: 83, 4: 42, 5: 20},
             "unchanged": 559, "keys_none": 63, "items_none": 195}
EXPECT_TAU = 0.503637


# ------------------------------------------------------------------ §C.4 blind census, §C.5 markers
def blind_census(sub):
    vals = collections.Counter(it["blind"]["nok"] for it in sub)
    ncf = collections.Counter(bool(it["blind"].get("nok_candidates_found")) for it in sub)
    pn0 = sum(1 for it in sub if it["y_nok"] and it["blind"]["nok"] == 0.0)
    a = auroc([it["blind"]["nok"] for it in sub], [it["y_nok"] for it in sub])
    return {"values": dict(vals), "ncf_true": ncf[True], "pn_at_zero": pn0, "auroc": a}


def marker_fractions():
    import tiktoken
    enc = tiktoken.get_encoding("o200k_base")
    idx = indexes()
    out = {}
    for b in ("mem0", "amem"):
        for prov in ("TRUE", "BELIEVED"):
            rows = []
            for k, t in idx.items():
                if k.startswith(f"{b}:") and k.endswith(f":FULL:{prov}"):
                    lines = t.split("\n")
                    occ = t.count(IX.MARKER)
                    rows.append((len(lines), len(enc.encode(t)), occ, sum(1 for ln in lines if IX.MARKER in ln)))
            assert len(set(rows)) == 1, (b, prov, set(rows))
            n_lines, n_tok, occ, m_lines = rows[0]
            out[f"{b}:{prov}"] = {"indexes": len(rows), "lines": n_lines, "tokens": n_tok, "marker_occurrences": occ,
                                  "marker_lines": m_lines, "marker_tokens": occ * 6, "fraction": round(occ * 6 / n_tok, 3)}
    return out


EXPECT_Q4 = {"mem0:TRUE": (37, 31, 216, 3, 3, 18, 0.083), "amem:TRUE": (40, 31, 216, 3, 3, 18, 0.083),
             "mem0:BELIEVED": (37, 31, 232, 7, 7, 42, 0.181), "amem:BELIEVED": (40, 31, 236, 8, 8, 48, 0.203)}


# ------------------------------------------------------------------ §L2 TRUE flags, variants, line renderer
_FLAGS = {}


def true_flags():
    """Per persona: {entry_id: {superseded, retracted, expired, slot, category, age, text}} under the
    TRUE join, computed over all rows as index_v2.main does (variant-invariant), ages per R3."""
    if _FLAGS:
        return _FLAGS
    joins = load_joins()
    raw = collections.defaultdict(list)
    for r in load_backend("frbank"):
        raw[r["persona"]].append(r)
    for name in sorted(joins):
        Jp = joins[name]
        rows = sorted(raw[name], key=lambda r: r["entry_id"])
        etoks = {r["entry_id"]: e0_toks(r["text"], Jp.drop) for r in rows}
        sup, ret, exp, ev = true_lifecycle(Jp, etoks)
        d = {}
        for r in rows:
            dt = parse_dt(r["recency_time"])
            age = None if dt is None else max(0, (Jp.t_now - dt).days)
            d[r["entry_id"]] = {"superseded": r["entry_id"] in sup, "retracted": r["entry_id"] in ret,
                                "expired": r["entry_id"] in exp, "slot": scrub(r["slot"]), "category": r["category"],
                                "age": age, "text": r["text"]}
        _FLAGS[name] = d
    return _FLAGS


def variant_ids(it):
    """The entry set index_v2.main renders the committed index from (FULL; CAT-ABLATED; SLOT-ABLATED)."""
    fl = true_flags()[it["persona"]]
    if it["variant"] == "FULL":
        return sorted(fl)
    if it["variant"] == "CAT-ABLATED":
        cats = set(J(IX.BUILD / "variant_plan.json")["cat_ablation"][it["persona"]]["categories"])
        return sorted(e for e in fl if fl[e]["category"] not in cats)
    rm = set(J(IX.BUILD / "slot_ablations.json")[f"{it['persona']}:{it['question_id']}"])
    return sorted(e for e in fl if e not in rm)


def lifecycle_tag(f):
    tags = [k for k in ("retracted", "superseded", "expired") if f[k]]
    return ", ".join(tags) if tags else "active"


def render_line(rank, f):
    age = "unknown" if f["age"] is None else f"{f['age']} days"
    return (f"[{rank}] lifecycle: {lifecycle_tag(f)} | category: {f['category']} | attribute: {f['slot'] or '(none)'} "
            f"| age: {age} | text: {f['text']}")
