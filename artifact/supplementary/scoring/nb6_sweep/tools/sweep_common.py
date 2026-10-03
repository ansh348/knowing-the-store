"""Shared loaders, list builders, census and scorers for the NB-6 length x recall sweep.

POST HOC, UNREGISTERED (nb6_sweep/REPORT.md section 0). No model call, no ledger write.

Reuses, verbatim and unmodified:
  e1r_robustness/tools/common_e1r.py      auroc, boot_item, boot_cluster, load_e1, POPULATIONS
  e1r_robustness/tools/index_features.py  parse, index_key, toks
  e1r_robustness/tools/run_nb6.py         name_lists, lex_scores, emb_scores  (the committed NB-6)
  e1r_robustness/tools/run_baselines.py   encoder, jac
  e1r_robustness/tools/nb6_composition.py AV_STATE (attack vector -> lifecycle state, 661)

Two populations, one row shape:
  pop        "661" (R-NOK-FRB, TRUE index) or "cf2" (444, v2 summary)
  item_id, persona, question, y (NOK label), state (positives' lifecycle state)
  key        the summary the item reads: the TRUE index key (661) or the item_id (cf2).
             Lists are built PER SUMMARY, so items that share a summary see the same list.
  base       the committed superseded-names list of that summary (all TRUE-superseded names)
  own        the item's own scrubbed attribute name(s): the slot names of the entries the
             question resolves to (661: slot_ablations closure + pn_members, persona-keyed;
             cf2: the pair's slot_scrubbed). Empty for natural-absent probes.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys
from pathlib import Path

import numpy as np

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

ROOT = Path(__file__).resolve().parents[2]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools"):
    sys.path.insert(0, str(ROOT / p))

from common_e1r import POPULATIONS, auroc, boot_cluster, boot_item, jdump, jload, load_e1  # noqa: E402
from index_features import index_key, indexes, parse, toks  # noqa: E402
from nb6_composition import AV_STATE  # noqa: E402
from run_baselines import encoder, jac  # noqa: E402
from run_nb6 import emb_scores, lex_scores, name_lists  # noqa: E402

E1 = ROOT / "e1_metamemory"
CF2 = ROOT / "r82_counterfactual" / "cf2"
S2U = ROOT / "side_experiments" / "s2" / "indexes_s2u.json"
OUT = ROOT / "nb6_sweep" / "results"
SEED = 42
LENGTHS = (5, 10, 15, 30, 32, 60)      # 15 = FR-Bank's renderer cap, 32 ~ BELIEVED uncapped (32.55), 60 = the registered stress condition
RECALLS = (1.0, 0.70, 0.50, 0.30, 0.10)
RECALL_TARGET = 0.2996          # BELIEVED rendered micro-recall, NUMBERS_SIDE AUX-SIDE-S2-CENSUS


MARKER = "(none)"       # index_v2 prints this for an empty section; index_features.parse returns
                        # it as a name, index_v3.named_sections does not (see step1_reproduce.py)


def clean(names):
    """Attribute names only: drop the empty-section marker."""
    return [n for n in names if n.strip() != MARKER]


def scrub(slot):
    """index_v2.scrub, verbatim: attribute path in, value out."""
    if not slot:
        return None
    name = str(slot).split(":", 1)[0].strip()
    return name or None


# ------------------------------------------------------------------ the store
_FB = {}


def frbank():
    """(persona -> set of scrubbed slot names, (persona, entry_id) -> scrubbed slot)."""
    if not _FB:
        uni, by_id = {}, {}
        for e in jload(E1 / "backend_entries" / "frbank.json"):
            s = scrub(e.get("slot"))
            by_id[(e["persona"], e["entry_id"])] = s
            if s:
                uni.setdefault(e["persona"], set()).add(s)
        _FB["uni"], _FB["by_id"] = uni, by_id
    return _FB["uni"], _FB["by_id"]


# ------------------------------------------------------------------ populations
def load_661():
    """The R-NOK-FRB rows, joined exactly as run_nb6.build joins them (n = 661)."""
    items, blind, idxT, idxB = load_e1()
    uni, by_id = frbank()
    sa = jload(E1 / "build" / "slot_ablations.json")
    s2u = jload(S2U)["indexes"] if S2U.exists() else {}
    rows = []
    for it in items:
        if not POPULATIONS["R-NOK-FRB"]["filt"](it):
            continue
        q, tag = it["question"], it["item_id"]
        if q not in blind or tag not in idxT:
            continue
        if blind[q].get("nok") is None or idxT[tag].get("nok") is None:
            continue
        lab = it.get("label", it["label_pre"])
        y = 1 if lab == "PRESENT-NEGATIVE" else 0
        p = it["persona"]
        own, pn_own = set(), set()
        for eid in sa.get(f"{p}:{it['question_id']}", []):
            s = by_id.get((p, eid))
            if s:
                own.add(s)
        for eid in it.get("pn_members") or []:
            s = by_id.get((p, eid))
            if s:
                own.add(s)
                pn_own.add(s)
        kT = index_key(it, "TRUE")
        base, _ = name_lists(it, "TRUE")
        bel, _ = name_lists(it, "BELIEVED")
        kS = kT[: -len(":TRUE")] + ":S2U"
        su = list(parse(s2u[kS])["superseded_attrs"]) if kS in s2u else None
        rows.append({"pop": "661", "item_id": tag, "persona": p, "question": q, "y": y,
                     "state": (AV_STATE.get(it.get("attack_vector")) or "unmapped") if y else None,
                     "label": lab, "variant": it["variant"], "key": kT,
                     "base": clean(base), "base_marker": list(base),      # base_marker: as committed
                     "believed": clean(bel), "s2u": clean(su) if su is not None else None,
                     "own": sorted(own), "pn_own": sorted(pn_own), "monitor": idxT[tag]["nok"]})
    return rows


def load_cf2():
    """The 444-item CF-2 cell under the v2 (superseded-only) summary."""
    cell = jload(CF2 / "cf_cell.json")
    idx = jload(CF2 / "cf_indexes.json")["indexes"]
    ind = cell["meta"]["individuation"]
    rows = []
    for it in cell["items"]:
        own = ind[it["pair_id"]]["slot_scrubbed"]
        rows.append({"pop": "cf2", "item_id": it["item_id"], "persona": it["persona"],
                     "question": it["question"], "y": int(it["y_nok"]),
                     "state": it["state"].lower().replace("supersession", "superseded")
                              .replace("retraction", "retracted").replace("expiry", "expired"),
                     "label": it["label"], "version": it["version"], "pair_id": it["pair_id"],
                     "key": it["item_id"], "base": clean(parse(idx[it["item_id"]]["v2"])["superseded_attrs"]),
                     "own": [own] if own else []})
    return rows


# ------------------------------------------------------------------ pools
def pools(rows_all):
    """Per persona: own-store fillers (real names of this store that no scored question of
    this persona targets, in either population) and distractors (names real in some OTHER
    store and absent from this one)."""
    uni, _ = frbank()
    targets = {}
    for r in rows_all:
        targets.setdefault(r["persona"], set()).update(r["own"])
    everything = set().union(*uni.values())
    own_pool, dis_pool = {}, {}
    for p, names in uni.items():
        t = targets.get(p, set())
        own_pool[p] = sorted(names - t)
        dis_pool[p] = sorted(everything - names - t)
    return own_pool, dis_pool, targets


# ------------------------------------------------------------------ list builders
def _rng(*parts, seed=SEED):
    h = hashlib.sha256("|".join(str(x) for x in parts).encode("utf-8")).hexdigest()
    return np.random.default_rng([seed, int(h[:8], 16)])


def summaries(rows):
    """key -> {persona, base, n_items}; the unit lists are built on."""
    out = {}
    for r in rows:
        s = out.setdefault(r["key"], {"persona": r["persona"], "base": list(r["base"]), "n_items": 0})
        s["n_items"] += 1
    return out


def drop_to_recall(rows, target, seed=SEED):
    """Drop (summary, TRUE-name) pairs at random until the ITEM-weighted micro-recall of TRUE
    names, sum_items |kept_i ∩ base_i| / sum_items |base_i| (the ledger's definition), is as
    close to `target` as one more drop allows. Returns key -> kept list. target 1.0: no drop."""
    S = summaries(rows)
    kept = {k: set(s["base"]) for k, s in S.items()}
    if target >= 1.0:
        return {k: sorted(v) for k, v in kept.items()}
    pairs = [(k, n) for k, s in S.items() for n in s["base"]]
    w = {k: s["n_items"] for k, s in S.items()}
    total = sum(w[k] for k, _ in pairs)
    rng = _rng("recall", rows[0]["pop"], seed=seed)
    rng.shuffle(pairs)
    have = total
    for k, n in pairs:
        nxt = have - w[k]
        if abs(nxt / total - target) <= abs(have / total - target):
            kept[k].discard(n)
            have = nxt
        else:
            break
    return {k: sorted(v) for k, v in kept.items()}


# ------------------------------------------------------------------ contamination
_ST = {}


def store_names(row):
    """Scrubbed slot names present in the store version this item reads."""
    p = row["persona"]
    if row["pop"] == "cf2":
        return frbank()[0][p]                       # the persona bank; all 148 pair slots are in it
    if "plan" not in _ST:
        by_p = {}
        for e in jload(E1 / "backend_entries" / "frbank.json"):
            by_p.setdefault(e["persona"], []).append(e)
        _ST["by_p"] = by_p
        _ST["plan"] = jload(E1 / "build" / "variant_plan.json")["cat_ablation"]
        _ST["sa"] = jload(E1 / "build" / "slot_ablations.json")
        _ST["cache"] = {}
    key = row["key"]
    if key not in _ST["cache"]:
        ents = _ST["by_p"][p]
        if row["variant"] == "CAT-ABLATED":
            cats = set(_ST["plan"][p]["categories"])
            ents = [e for e in ents if e["category"] not in cats]
        elif row["variant"] == "SLOT-ABLATED":
            rm = set(_ST["sa"][f"{p}:{row['item_id'].split(':')[2]}"])
            ents = [e for e in ents if e["entry_id"] not in rm]
        _ST["cache"][key] = {scrub(e["slot"]) for e in ents if scrub(e["slot"])}
    return _ST["cache"][key]


def _hash_tag(s):
    return int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)


def inject(rows, start_lists, rate, seed=SEED):
    """key -> list with negatives' own names injected until `rate` of ALL negatives are named.
    Store-faithful: a negative is eligible when one of its own names is a real name of its store
    version; one such name per chosen negative. Nested across rates (one permutation per seed).
    Stops when the achieved census count is as close to the target as one more step allows."""
    lists = {k: list(v) for k, v in start_lists.items()}
    neg = [r for r in rows if r["y"] == 0]
    target = rate * len(neg)
    elig = []
    for r in neg:
        cands = sorted(set(r["own"]) & store_names(r))
        if cands:
            elig.append((r, cands))
    rng = np.random.default_rng([seed, _hash_tag(rows[0]["pop"])])
    order = rng.permutation(len(elig))

    def named_count():
        return sum(1 for r in neg if set(r["own"]) & set(lists[r["key"]]))

    have = named_count()
    n_inj = 0
    for i in order:
        if have >= target:
            break
        r, cands = elig[i]
        if set(r["own"]) & set(lists[r["key"]]):
            continue                                # already named through a shared summary
        name = cands[rng.integers(0, len(cands))]
        trial = named_count()
        lists[r["key"]].append(name)
        nxt = named_count()
        if abs(nxt - target) <= abs(trial - target):
            have = nxt
            n_inj += 1
        else:
            lists[r["key"]].pop()
            break
    return lists, {"target_rate": rate, "target_count": target, "n_injected": n_inj,
                   "n_eligible": len(elig), "achieved_count": have, "achieved_rate": have / len(neg)}


# ------------------------------------------------------------------ padding
def pad_lists(rows, start_lists, own_pool, dis_pool, L, distractor_share=0.0, seed=SEED):
    """key -> list padded to L with fillers from a per-summary seeded permutation of the
    persona's untargeted own-store names (nested across L), never re-adding a TRUE name of that
    summary or a name already listed; a distractor_share of the fillers comes instead from other
    personas' stores. Final order shuffled under the same seed. L None: no padding."""
    S = summaries(rows)
    out = {}
    for k, s in S.items():
        p, base = s["persona"], set(s["base"])
        lst = list(start_lists[k])
        if L is not None and len(lst) < L:
            need = L - len(lst)
            present = base | set(lst)
            rng = _rng("fill", k, seed=seed)
            own_perm = [n for n in rng.permutation(own_pool[p]) if n not in present]
            n_dis = int(round(need * distractor_share))
            fill = list(own_perm[:need - n_dis])
            if n_dis:
                dis_perm = [n for n in rng.permutation(dis_pool[p]) if n not in present]
                fill += list(dis_perm[:n_dis])
            assert len(fill) == need, (k, len(fill), need)
            lst = lst + fill
            _rng("order", k, L, seed=seed).shuffle(lst)
        out[k] = lst
    return out


def make_cell(rows, own_pool, dis_pool, L=None, recall=1.0, c=0.0, distractor_share=0.0, seed=SEED):
    """One cell's lists: recall drop, then contamination injection, then padding to L (so length
    is held at L when L is set). Returns (lists, meta)."""
    kept = drop_to_recall(rows, recall, seed=seed)
    meta = {"L": L, "recall": recall, "c": c, "distractor_share": distractor_share, "seed": seed}
    if c > 0:
        kept, inj = inject(rows, kept, c, seed=seed)
        meta["injection"] = inj
    lists = pad_lists(rows, kept, own_pool, dis_pool, L, distractor_share, seed=seed)
    return lists, meta


# ------------------------------------------------------------------ census
def census(rows, lists):
    """Deterministic counts on one cell. No resampling."""
    pos = [r for r in rows if r["y"] == 1]
    neg = [r for r in rows if r["y"] == 0]
    neg_own = [r for r in neg if r["own"]]

    def named(r):
        return bool(set(r["own"]) & set(lists[r["key"]]))

    tb = sum(len(r["base"]) for r in rows)
    tk = sum(len(set(r["base"]) & set(lists[r["key"]])) for r in rows)
    tl = sum(len(lists[r["key"]]) for r in rows)
    return {
        "n": len(rows), "n_pos": len(pos), "n_neg": len(neg),
        "mean_len": tl / len(rows),
        "true_recall_item_weighted": tk / tb if tb else None,
        "precision_vs_true": tk / tl if tl else None,
        "pos_own_named": sum(named(r) for r in pos) / len(pos),
        "neg_own_named_all": sum(named(r) for r in neg) / len(neg),
        "neg_own_named_of_those_with_own": (sum(named(r) for r in neg_own) / len(neg_own)) if neg_own else None,
        "n_neg_with_own": len(neg_own),
        # the PRESENT-label negatives only (BELIEVED names 85 of 174 = 0.49 on the 661)
        "neg_own_named_present": (sum(named(r) for r in neg if r["label"] == "PRESENT") / max(1, sum(1 for r in neg if r["label"] == "PRESENT"))),
        "pos_own_named_by_state": {st: (sum(named(r) for r in pos if r["state"] == st), sum(1 for r in pos if r["state"] == st))
                                   for st in ("superseded", "retracted", "expired")},
        # E1R's narrower definition (AUX-E1R-NB6-COMPOSITION): the PN members' own slots only
        "pos_pn_member_named": (sum(bool(set(r.get("pn_own", r["own"])) & set(lists[r["key"]])) for r in pos) / len(pos)),
    }


# ------------------------------------------------------------------ scoring
_EMB = {"q": {}, "n": {}}


def _vecs(texts, kind):
    cache = _EMB[kind]
    miss = sorted({t for t in texts if t not in cache})
    if miss:
        enc = encoder()
        src = miss if kind == "q" else [m.replace("_", " ") for m in miss]
        bs = 128 if kind == "q" else 256
        v = enc.encode(src, normalize_embeddings=True, batch_size=bs, show_progress_bar=False)
        for t, x in zip(miss, v):
            cache[t] = x
    return cache


def emb_cached(rows, lists):
    """Max cosine, same encoder and call parameters as run_nb6.emb_scores, cached per string."""
    qv = _vecs([r["question"] for r in rows], "q")
    nv = _vecs([n for r in rows for n in lists[r["key"]]], "n")
    out = []
    for r in rows:
        lst = lists[r["key"]]
        if not lst:
            out.append(0.0)
            continue
        M = np.stack([nv[n] for n in lst])
        out.append(float(np.max(M @ qv[r["question"]])))
    return np.array(out, float)


def lex_cached(rows, lists):
    """run_nb6.lex_scores over the same lists (Jaccard on index_features.toks)."""
    out = []
    for r in rows:
        qt = toks(r["question"])
        out.append(max((jac(qt, toks(a.replace("_", " "))) for a in lists[r["key"]]), default=0.0))
    return np.array(out, float)


def committed_scores(rows, lists):
    """The committed NB-6 functions, byte for byte (run_nb6.lex_scores / emb_scores)."""
    rr = [{"question": r["question"], "names": lists[r["key"]]} for r in rows]
    return np.array(lex_scores(rr, "names"), float), np.array(emb_scores(rr, "names"), float)


def state_mask(rows, state):
    """The per-state slice, in each ledger's own convention.
    661 (NUMBERS_E1R AUX-E1R-NB6-COMPOSITION): this state's positives against ALL negatives.
    cf2 (NUMBERS_CF2 AUX-CF2-NB6-V2): the items of that state only -- the pairs' three versions,
    positives and negatives alike (supersession slice = 264 items, 88 positive)."""
    y = np.array([r["y"] for r in rows], int)
    st = np.array([r["state"] or "" for r in rows])
    if rows and rows[0]["pop"] == "cf2":
        return st == state
    return (y == 0) | (st == state)


def prime_embeddings(rows_all, own_pool, dis_pool, extra=()):
    """Encode every question and every name any cell can contain, once, in one sorted batch
    run, so every cell is scored from identical vectors (batch composition perturbs the encoder
    at ~1e-7, enough to flip a near-tied pair between separately encoded cells)."""
    names = set(extra)
    for r in rows_all:
        for f in ("base", "base_marker", "believed", "s2u"):
            if r.get(f):
                names.update(r[f])
    for pool in (own_pool, dis_pool):
        for v in pool.values():
            names.update(v)
    _vecs(sorted({r["question"] for r in rows_all}), "q")
    _vecs(sorted(names), "n")
    return len(names)


def score_cell(rows, lists, base_scores=None, boot=False):
    """AUROC per variant, whole population and per state slice; optional paired bootstrap
    against base_scores = {"lex": arr, "emb": arr} (both intervals; wider governs)."""
    y = np.array([r["y"] for r in rows], int)
    g = np.array([r["persona"] for r in rows])
    st = np.array([r["state"] or "" for r in rows])
    s = {"lex": lex_cached(rows, lists), "emb": emb_cached(rows, lists)}
    out = {"census": census(rows, lists)}
    for v, arr in s.items():
        rec = {"auroc": float(auroc(arr, y))}
        for state in ("superseded", "retracted", "expired"):
            m = state_mask(rows, state)
            rec[f"auroc_{state}"] = float(auroc(arr[m], y[m])) if y[m].sum() else None
        if boot and base_scores is not None:
            b = base_scores[v]
            rec["delta_vs_base"] = float(auroc(arr, y) - auroc(b, y))
            it, cl = boot_item(b, arr, y), boot_cluster(b, arr, y, g)
            rec["ci_item"], rec["ci_persona"] = it, cl
            wide = it if (it["ci_hi"] - it["ci_lo"]) >= (cl["ci_hi"] - cl["ci_lo"]) else cl
            rec["ci_governing"] = {"which": "item" if wide is it else "persona",
                                   "ci_lo": wide["ci_lo"], "ci_hi": wide["ci_hi"],
                                   "excludes_zero": wide["excludes_zero"]}
            m = state_mask(rows, "superseded")
            rec["sup_delta_vs_base"] = float(auroc(arr[m], y[m]) - auroc(b[m], y[m]))
            it2, cl2 = boot_item(b[m], arr[m], y[m]), boot_cluster(b[m], arr[m], y[m], g[m])
            wide2 = it2 if (it2["ci_hi"] - it2["ci_lo"]) >= (cl2["ci_hi"] - cl2["ci_lo"]) else cl2
            rec["sup_ci_item"], rec["sup_ci_persona"] = it2, cl2
            rec["sup_ci_governing"] = {"which": "item" if wide2 is it2 else "persona",
                                       "ci_lo": wide2["ci_lo"], "ci_hi": wide2["ci_hi"],
                                       "excludes_zero": wide2["excludes_zero"]}
        out[v] = rec
    out["_scores"] = s
    return out


def strip_scores(cell):
    return {k: v for k, v in cell.items() if k != "_scores"}
