"""cf_pad_common.py -- ADDENDUM_CF_PAD (R136, the long-list check): the counterfactual set's 444 superseded-only
summaries with the superseded-names list padded to 60 names, one pad per triple.

Registration: registrations/ADDENDUM_CF_PAD.md; REG_SHA is filled in at the freeze (Phase 0 leaves it None and
every subcommand that can spend or score asserts it). Deterministic; no model call anywhere in this module.

Reuses verbatim (nothing re-implemented):
  pad_probe/tools/pad_common          render_section_lifted / padded_text (index_v3._name_block with SLOT_CAP lifted to
                                      100, the PAD renderer), committed_names, map_names (D-PAD-3), poolable,
                                      targeted_slots (the 661-cell targets, D-PAD-2's wide reading)
  nb6_sweep/tools/sweep_common        load_cf2 (the 444 rows), frbank (the store's scrubbed slot names), emb_cached /
                                      lex_cached (the two lookups, NB-6's estimators), auroc, boot_item, boot_cluster,
                                      state_mask (the CF-2 per-state convention)
  reviews/r122/tools/enc_lookup       random_token (the random-token control, TOKEN_SEED 42)
  r82_counterfactual/tools/score_cf   matcher (the embedding lookup as Table 1 scores it)
  reviews/r125/tools/r125_common      Cell, outcomes, wtl, boot_triple, boot_persona (the matched metric)

The padding rule for a triple (registration section 3; the differences from ADDENDUM_PAD section 3 are listed there
and in cf_pad/DEVIATIONS_CF_PAD.md):
  pool A   the names printed in the per-category map of ALL THREE versions' v2 texts (the intersection), less
           (i) every name in any version's committed superseded section, (ii) every slot a scored question of the
           persona targets (its CF-2 pairs' target slots and the slots of the entries their PN versions add; the
           661-cell targets under D-PAD-2), (iii) names with ':' or whitespace and overflow fragments, (iv) the change
           set (the symmetric difference of the three printed maps, the PN version's pn_members slots, the target)
  pool B   other personas' FULL:TRUE map names less this persona's maps, committed names and (ii)-(iii); unused when
           pool A holds 60 (it does on every triple: min 71)
  draw     random.Random(f"42:{pair_id}"): pool A shuffled, pool B shuffled, concatenated, taken in order
  pad      the first (60 - |committed(PN)|) names of the draw, the same names in the same draw order for the three
           versions; every version's list = its own committed names + the pad
  render   the v2 text's superseded section (its tail) re-rendered by index_v3._name_block with the per-bucket cap
           lifted to 100: sorted set, wrap 150, indents two and four spaces; the text above the header byte-identical
"""
from __future__ import annotations

import collections
import hashlib
import io
import json
import os
import random
import sys
from pathlib import Path

import numpy as np

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

ROOT = Path(__file__).resolve().parents[2]
for p in ("pad_probe/tools", "nb6_sweep/tools", "e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools",
          "e1_metamemory/tools", "e0_metamemory/tools", "resp_review/tools", "ds_downstream/tools", "reviews/r122/tools",
          "reviews/r125/tools"):
    sys.path.insert(0, str(ROOT / p))

import pad_common as PC  # noqa: E402
from pad_common import committed_names, map_names, padded_text, poolable, targeted_slots  # noqa: E402
from sweep_common import auroc, boot_cluster, boot_item, emb_cached, frbank, lex_cached, load_cf2, state_mask  # noqa: E402
from index_features import indexes, parse  # noqa: E402

CF2 = ROOT / "r82_counterfactual" / "cf2"
CFP = ROOT / "cf_pad"
R136 = ROOT / "reviews" / "r136"
BUILD, ROWS, RES = CFP / "build", CFP / "rows", CFP / "results"
REG = ROOT / "registrations" / "ADDENDUM_CF_PAD.md"
REG_SHA = "a84dac1abc2f604b171b4ab838daba4bbdb440d124ef9f050387bd0a716eba21"   # the author's GO of 2026-09-22 quotes it; frozen
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
L = 60
SEED_PREFIX = "42"
SLOT_CAP_LIFTED = PC.SLOT_CAP_LIFTED            # 100, as ADDENDUM_PAD section 3 and the SIDE S2-U build
VERSIONS = ("PN", "PRESENT", "ABSENT")
STATES = ("superseded", "retracted", "expired")
ARM = "INDEXED-V2-PAD60"
# the recorded Table 1 rows (reviews/r125/results/r125_vectors.json, gated there at four decimals)
RECORDED = {"LOOKUP_v2": 0.7663, "RANDTOK_v2": 0.5954, "MINI5_v2": 0.7648, "H45_v2": 0.7566, "LUNA_v2": 0.8417, "SOL_v2": 0.8500,
            "OP5_v2": 0.8405}
LEX_V2 = 0.6698                                # AUX-CF2-NB6-V2 lexical (tab:pad, lower block)


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True, default=_default)
        f.write("\n")


def _default(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, set):
        return sorted(o)
    return float(o)


def sha256_frozen(p=REG):
    b = io.open(p, "rb").read()
    i = b.find(FROZEN_END)
    return hashlib.sha256(b if i < 0 else b[:i]).hexdigest()


def registration_ok():
    return REG_SHA is not None and REG.exists() and sha256_frozen() == REG_SHA


# ------------------------------------------------------------------ population (section 2)
class Pop:
    """The 444 rows (sweep_common.load_cf2: pop 'cf2', key = item_id, base = committed v2 superseded names,
    own = [target]) with the triple structure, the v2 texts and the individuation record."""

    def __init__(self):
        self.rows = load_cf2()
        assert len(self.rows) == 444 and sum(r["y"] for r in self.rows) == 148
        cell = jload(CF2 / "cf_cell.json")
        self.cell_items = {it["item_id"]: it for it in cell["items"]}
        self.ind = cell["meta"]["individuation"]
        self.idx = jload(CF2 / "cf_indexes.json")["indexes"]
        self.idx_sha = jload(CF2 / "cf_indexes.json")["meta"]["sha256"]
        self.text = {r["key"]: self.idx[r["key"]]["v2"] for r in self.rows}
        self.by_pair = collections.defaultdict(dict)
        for r in self.rows:
            self.by_pair[r["pair_id"]][r["version"]] = r
        assert len(self.by_pair) == 148 and all(set(v) == set(VERSIONS) for v in self.by_pair.values())
        self.pairs = sorted(self.by_pair)
        self.y = np.array([r["y"] for r in self.rows], int)
        self.g = np.array([r["persona"] for r in self.rows])
        self.pos = {r["key"]: k for k, r in enumerate(self.rows)}

    def target(self, pid):
        return self.ind[pid]["slot_scrubbed"]

    def state(self, pid):
        return self.by_pair[pid]["PN"]["state"]

    def persona(self, pid):
        return self.by_pair[pid]["PN"]["persona"]

    def pn_member_slots(self, pid):
        """The scrubbed slots of the entries the PN version adds: frbank entries by id; the six authored entries
        (lb_r82_<persona>, cf2/cf_pn_texts_cf2.json) carry the pair's own target slot."""
        _, by_id = frbank()
        p = self.persona(pid)
        out = set()
        for e in self.cell_items[self.by_pair[pid]["PN"]["key"]]["pn_members"]:
            s = by_id.get((p, e))
            if s is None:
                assert e == f"lb_r82_{p}", (pid, e)
                s = self.target(pid)
            out.add(s)
        return out


# ------------------------------------------------------------------ exclusion (ii): the persona's targets
_EX = {}


def persona_targets(pop):
    """persona -> {cf2_targets, cf2_pn_slots, e1_wide, all}. cf2_targets: every pair's target slot; cf2_pn_slots: every
    slot of the entries any pair's PN version adds; e1_wide: pad_common.targeted_slots()[p]['wide'] (D-PAD-2)."""
    if _EX:
        return _EX
    ex661 = targeted_slots()
    for pid in pop.pairs:
        p = pop.persona(pid)
        d = _EX.setdefault(p, {"cf2_targets": set(), "cf2_pn_slots": set(), "e1_wide": set(ex661.get(p, {}).get("wide", set()))})
        d["cf2_targets"].add(pop.target(pid))
        d["cf2_pn_slots"] |= pop.pn_member_slots(pid)
    for p, d in _EX.items():
        d["all"] = d["cf2_targets"] | d["cf2_pn_slots"] | d["e1_wide"]
    return _EX


# ------------------------------------------------------------------ pools and pads (section 3)
def build_pools(pop):
    """pair_id -> {persona, target, state, committed{v}, change, pool_a, pool_b, census}."""
    ex = persona_targets(pop)
    e1 = indexes()
    personas = sorted({pop.persona(pid) for pid in pop.pairs})
    full_map = {p: set(map_names(e1[f"frbank:{p}:FULL:TRUE"])) for p in personas}
    uni, _ = frbank()
    out = {}
    for pid in pop.pairs:
        p, t = pop.persona(pid), pop.target(pid)
        maps = {v: set(map_names(pop.text[pop.by_pair[pid][v]["key"]])) for v in VERSIONS}
        com = {v: committed_names(pop.text[pop.by_pair[pid][v]["key"]]) for v in VERSIONS}
        for v in VERSIONS:
            assert len(com[v]) == len(set(com[v])), (pid, v)
        inter = maps["PN"] & maps["PRESENT"] & maps["ABSENT"]
        union = maps["PN"] | maps["PRESENT"] | maps["ABSENT"]
        com_all = set(com["PN"]) | set(com["PRESENT"]) | set(com["ABSENT"])
        com_int = set(com["PN"]) & set(com["PRESENT"]) & set(com["ABSENT"])
        change = (union - inter) | (com_all - com_int) | pop.pn_member_slots(pid) | {t}
        excl = com_all | ex[p]["all"] | change
        a = sorted(n for n in inter - excl if poolable(n))
        own_maps = union | full_map[p]
        others = set()
        for p2 in personas:
            if p2 != p:
                others |= full_map[p2]
        b = sorted(n for n in others - own_maps - excl if poolable(n))
        assert all(n in uni[p] for n in a), (pid, [n for n in a if n not in uni[p]])   # pool A names are the store's own scrubbed slot names
        out[pid] = {"persona": p, "target": t, "state": pop.state(pid), "committed": com, "change": sorted(change),
                    "pool_a": a, "pool_b": b,
                    "census": {"map_pn": len(maps["PN"]), "map_present": len(maps["PRESENT"]), "map_absent": len(maps["ABSENT"]),
                               "map_intersection": len(inter), "map_union": len(union), "map_symdiff": len(union - inter),
                               "committed_pn": len(com["PN"]), "committed_present": len(com["PRESENT"]), "committed_absent": len(com["ABSENT"]),
                               "change_set": len(change), "excluded_by_ii_from_intersection": len(inter & ex[p]["all"]),
                               "excluded_by_ii_cf2_only": len(inter & (ex[p]["cf2_targets"] | ex[p]["cf2_pn_slots"])),
                               "excluded_by_ii_e1_only": len(inter & (ex[p]["e1_wide"] - ex[p]["cf2_targets"] - ex[p]["cf2_pn_slots"])),
                               "pool_a": len(a), "pool_b": len(b)}}
    return out


def draw_order(pid, P):
    rng = random.Random(f"{SEED_PREFIX}:{pid}")
    a = list(P["pool_a"]); rng.shuffle(a)
    b = list(P["pool_b"]); rng.shuffle(b)
    return a + b, len(a)


def build_pads(pop, pools):
    """pair_id -> {pad (list, draw order), n_pad, from_pool_a, from_pool_b, lists{v}} with the section-3 assertions."""
    ex = persona_targets(pop)
    out = {}
    for pid, P in pools.items():
        order, n_a = draw_order(pid, P)
        com = P["committed"]
        n_pad = L - len(com["PN"])
        assert 0 < n_pad <= L, (pid, n_pad)
        pad = order[:n_pad]
        assert len(pad) == n_pad, f"STOP: pools exhausted on {pid}: {len(order)} < {n_pad}"
        lists = {v: list(com[v]) + pad for v in VERSIONS}
        t = P["target"]
        assert len(lists["PN"]) == L and len(set(lists["PN"])) == L, pid
        for v in VERSIONS:
            lst = lists[v]
            assert len(lst) == len(set(lst)), (pid, v)
            assert not any((":" in n) or (" " in n) for n in lst), (pid, v)
            assert set(com[v]) <= set(lst), (pid, v)
        assert not (set(pad) & set(P["change"])), (pid, set(pad) & set(P["change"]))
        assert not (set(pad) & ex[P["persona"]]["all"]), (pid, set(pad) & ex[P["persona"]]["all"])
        assert t not in pad
        for v in ("PRESENT", "ABSENT"):
            assert (t in lists[v]) == (t in com[v]), (pid, v)   # the target is in a sibling's list only where the committed text already lists it
        out[pid] = {"pad": pad, "n_pad": n_pad, "from_pool_a": min(n_pad, n_a), "from_pool_b": max(0, n_pad - n_a), "lists": lists,
                    "len": {v: len(lists[v]) for v in VERSIONS}}
    return out


def render_all(pop, pads):
    """key -> padded v2 text; asserts the re-parsed list equals the padded list, the prefix is byte-identical, no overflow."""
    out = {}
    for pid, R in pads.items():
        for v in VERSIONS:
            key = pop.by_pair[pid][v]["key"]
            text = pop.text[key]
            t = padded_text(text, R["lists"][v])
            got = committed_names(t)
            assert sorted(got) == sorted(R["lists"][v]), (pid, v)
            assert PC.split_section(t)[0] == PC.split_section(text)[0], (pid, v)
            assert "(+" not in PC.split_section(t)[1]
            out[key] = t
    return out


def renderer_lock(pop):
    """The section re-rendered over the committed names alone reproduces the committed v2 text byte for byte (444 of 444 or STOP)."""
    bad = [r["key"] for r in pop.rows if padded_text(pop.text[r["key"]], committed_names(pop.text[r["key"]])) != pop.text[r["key"]]]
    return 444 - len(bad), bad


def rendered_lists(texts, pop):
    """key -> the superseded names as the padded text prints them, in printed (sorted) order."""
    return {k: committed_names(texts[k]) for k in pop.text}


def target_positions(pop, pads):
    """The PN version's target rank (1-based) in its rendered, sorted 60-name list, per supersession triple."""
    pos = {}
    for pid, R in pads.items():
        if pop.state(pid) != "superseded":
            continue
        lst = sorted(set(R["lists"]["PN"]))
        pos[pid] = lst.index(pop.target(pid)) + 1
    return pos


# ------------------------------------------------------------------ the leak scan (registration section 3; a STOP at run time)
def leak_scan(pop, pools, pads, texts):
    """Fails (a STOP): a pad name that is not a scrubbed slot name of the persona's store (the value-free attribute
    names the map prints), a pad name carrying ':' (the slot path's value separator) or whitespace, a pad name equal
    to a stored entry's text, the target (or a slot the PN version adds) in a sibling's list where the committed text
    does not list it, pads differing across a triple's versions, an overflow marker in a rendered section.
    Descriptive (printed, not a STOP): pad names appearing verbatim in a PN-added entry's text; pad names equal to
    another entry's slot-path suffix (a qualifier such as financial_concern:rent beside the attribute rent)."""
    uni, _ = frbank()
    ents = jload(ROOT / "e1_metamemory" / "backend_entries" / "frbank.json")
    texts_by_p, suffix_by_p, ent_text = {}, {}, {}
    for e in ents:
        texts_by_p.setdefault(e["persona"], set()).add((e.get("text") or "").strip().casefold())
        s = e.get("slot") or ""
        if ":" in s:
            suffix_by_p.setdefault(e["persona"], set()).add(s.split(":", 1)[1].strip().casefold())
        ent_text[(e["persona"], e["entry_id"])] = e.get("text") or ""
    fails, notes = [], collections.Counter()
    for pid, R in pads.items():
        p, t = pools[pid]["persona"], pools[pid]["target"]
        pad = R["pad"]
        for n in pad:
            if n not in uni[p]:
                fails.append(("pad name not a scrubbed slot name of the store", pid, n))
            if ":" in n or " " in n:
                fails.append(("pad name carries a value separator or whitespace", pid, n))
            if n.casefold() in texts_by_p.get(p, set()) or n.replace("_", " ").casefold() in texts_by_p.get(p, set()):
                fails.append(("pad name equals a stored entry text", pid, n))
            if n.casefold() in suffix_by_p.get(p, set()) or n.replace("_", " ").casefold() in suffix_by_p.get(p, set()):
                notes["pad name equal to a slot-path suffix of another entry (a qualifier that is also an attribute name; descriptive)"] += 1
        for v in ("PRESENT", "ABSENT"):
            lst = R["lists"][v]
            com = pools[pid]["committed"][v]
            if t in lst and t not in com:
                fails.append(("target in a sibling's list", pid, v))
            for s in pop.pn_member_slots(pid):
                if s in lst and s not in com:
                    fails.append(("a PN-added slot in a sibling's list", pid, v, s))
        if not (R["lists"]["PN"][len(pools[pid]["committed"]["PN"]):] == R["lists"]["PRESENT"][len(pools[pid]["committed"]["PRESENT"]):] == R["lists"]["ABSENT"][len(pools[pid]["committed"]["ABSENT"]):]):
            fails.append(("pads differ across versions", pid))
        for e in pop.cell_items[pop.by_pair[pid]["PN"]["key"]]["pn_members"]:
            g = ent_text.get((p, e), "").casefold()
            for n in pad:
                if n.replace("_", " ").casefold() in g:
                    notes["pad name appearing verbatim in a PN-added entry's text (descriptive)"] += 1
    for k, t in texts.items():
        if "(+" in PC.split_section(t)[1]:
            fails.append(("overflow marker in a padded section", k))
    return fails, dict(notes)


# ------------------------------------------------------------------ the lookups ($0)
def lookup_scores(pop, lists_by_key):
    """The three no-model readers on the given name lists: embedding (NB-6, MiniLM max cosine), lexical (Jaccard),
    random-token (enc_lookup.random_token per distinct name, then the embedding lookup on the tokens)."""
    import enc_lookup as E
    import score_cf as S
    names = sorted({n for lst in lists_by_key.values() for n in lst})
    tok = {n: E.random_token(n) for n in names}
    assert len(set(tok.values())) == len(tok)
    tok_lists = [[tok[n] for n in lists_by_key[r["key"]]] for r in pop.rows]
    # the random-token control through score_cf.matcher, as reviews/r125/tools/r125_readers.py built it (its gate 0.5954)
    return {"emb": emb_cached(pop.rows, lists_by_key), "lex": lex_cached(pop.rows, lists_by_key),
            "randtok": np.asarray(S.matcher([r["question"] for r in pop.rows], tok_lists), float)}


def recorded_vectors():
    """The recorded Table 1 vectors on the 444 (reviews/r125/results/r125_vectors.json; every gate held there)."""
    d = jload(ROOT / "reviews" / "r125" / "results" / "r125_vectors.json")["readers"]
    return {k: d[k]["vector"] for k in RECORDED}


def texts_sha256(texts):
    return hashlib.sha256("\x1f".join(texts[k] for k in sorted(texts)).encode("utf-8")).hexdigest()
