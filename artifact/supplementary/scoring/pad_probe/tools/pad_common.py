"""pad_common.py -- ADDENDUM_PAD §2-§3: population, pools, padded lists, padded texts, locks.

Registration: registrations/ADDENDUM_PAD.md, registered text sha256
93e330225eba5168bd129df565c2c7594883ec830dd1a4ab0f23123520ee32fe (the bytes above the
FROZEN_END marker; dated sections are appended below it). Frozen at dab8956 before any call.

Deterministic; no model call. Reuses verbatim:
  nb6_sweep/tools/sweep_common.load_661     the 661 R-NOK-FRB rows joined as run_nb6.build joins them
                                            (key = TRUE index key; base = committed superseded names,
                                            marker-cleaned; base_marker = as committed, '(none)' included)
  e1r_robustness/tools/index_features       indexes, parse (attr_by_cat, superseded_attrs)
  resp_review/tools/resp_common             split_section (the section is the tail of every TRUE text),
                                            HDR2, true_flags (entry -> scrubbed slot)
  r82_counterfactual/index_v3._name_block   the v2 name-block grammar; the cap is lifted to 100 here
                                            (SLOT_CAP_LIFTED, as side_experiments/tools/build_s2u.py)
  ds_downstream/tools/ds_common             load_cell (gold entry ids per item), pn_slots

Settled readings, disclosed in pad_probe/DEVIATIONS_PAD.md before the first call:
  D-PAD-1  the draw order is seeded per key (random.Random(f"42:{key}")), not per key and length,
           because §3 also requires the 15-name list to be a prefix of the 30- and 60-name lists
           and a seed carrying L cannot give that; the prefix property is the stated purpose.
  D-PAD-2  exclusion (ii) is applied as the rule states it ("every scrubbed slot that any of the
           persona's 661-cell items targets"): the PN items' pn_members slots and the gold slots of
           every item that has gold entries, PRESENT and ABSENT alike; the literal operationalisation
           (PRESENT gold only) is a subset, and the names the wider reading removes are ledgered.
  D-PAD-3  the '(+N more)' overflow marker of the per-category map, split by the wrap into '(+N' and
           'more)' on 104 TRUE keys, is returned by index_features.parse as two names; neither is an
           attribute name and both are dropped from the pools (the same family as D-E1R-11); the one
           map name containing a space is dropped too, because the wrap breaks it into two names.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import random
import re
import sys
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

ROOT = Path(__file__).resolve().parents[2]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "nb6_sweep/tools",
          "e1_metamemory/tools", "e0_metamemory/tools", "resp_review/tools", "ds_downstream/tools"):
    sys.path.insert(0, str(ROOT / p))

import index_v3  # noqa: E402
from index_features import indexes, parse  # noqa: E402
from resp_common import HDR2, split_section, true_flags  # noqa: E402
from sweep_common import load_661  # noqa: E402

PAD = ROOT / "pad_probe"
REG = ROOT / "registrations" / "ADDENDUM_PAD.md"
REG_SHA = "93e330225eba5168bd129df565c2c7594883ec830dd1a4ab0f23123520ee32fe"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
LENGTHS = (15, 30, 60)
SLOT_CAP_LIFTED = 100
MARKER = "(none)"
GATE = {"emb": 0.7484, "lex": 0.5738}          # AUX-E1R-NB6, the committed superseded-names lookup on the 661
RECORDED = {"mini": 0.7339}                    # AUX: mini INDEXED-TRUE nok AUROC on the 661
BELIEVED = {"emb": 0.5858, "lex": 0.4718, "mini": 0.5959}


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True, default=float)
        f.write("\n")


def sha256_frozen(p=REG):
    b = io.open(p, "rb").read()
    i = b.find(FROZEN_END)
    return hashlib.sha256(b if i < 0 else b[:i]).hexdigest()


def registration_ok():
    return sha256_frozen() == REG_SHA


# ------------------------------------------------------------------ the renderer with the cap lifted
def render_section_lifted(names):
    """index_v3._name_block over the flat superseded section with SLOT_CAP lifted to 100: sorted set,
    wrap 150, indents two and four spaces, '(none)' when empty. The marker is never a name."""
    real = [n for n in names if n.strip() != MARKER]
    old = index_v3.SLOT_CAP
    index_v3.SLOT_CAP = SLOT_CAP_LIFTED
    try:
        return "\n".join(index_v3._name_block(real, HDR2))
    finally:
        index_v3.SLOT_CAP = old


def committed_names(text):
    """The committed superseded names of one TRUE text, marker-cleaned (index_features.parse)."""
    return [n for n in parse(text)["superseded_attrs"] if n.strip() != MARKER]


WS = re.compile(r"\s")
OVERFLOW = re.compile(r"^\(\+\d+$|^more\)$")     # the '(+N more)' marker split across a wrapped line (D-PAD-3)


def map_names(text):
    """Every attribute name printed in the per-category name map (all buckets). The '(+N more)' overflow
    marker is not a name: index_features._names strips it only when it sits on one line, and the wrap
    splits it into '(+N' / 'more)' on 104 TRUE keys; both fragments are dropped here (D-PAD-3)."""
    p = parse(text)
    return [n for lst in p["attr_by_cat"].values() for n in lst if not OVERFLOW.match(n.strip())]


def poolable(n):
    """A padding name must survive the render-parse round trip as one name: no ':' (§3 iii), no overflow
    fragment, and no whitespace (the wrap breaks a name at a space; one such name exists,
    'profession_related_to_Salone del Mobile', fatima; D-PAD-3)."""
    return ":" not in n and not OVERFLOW.match(n.strip()) and not WS.search(n)


# ------------------------------------------------------------------ population (§2)
def rows_661():
    rows = load_661()
    assert len(rows) == 661 and sum(r["y"] for r in rows) == 104, (len(rows), sum(r["y"] for r in rows))
    return rows


def keys_of(rows):
    return sorted({r["key"] for r in rows})


# ------------------------------------------------------------------ exclusion (ii): targeted slots per persona
_EX = {}


def targeted_slots():
    """persona -> {literal: set, wide: set, wide_only: set}. literal = PN items' pn_members slots u PRESENT
    items' gold slots (§3 as operationalised); wide = u gold slots of every item with gold (D-PAD-2)."""
    if _EX:
        return _EX
    from ds_common import load_cell, pn_slots
    fl = true_flags()
    for it in load_cell():
        p = it["persona"]
        d = _EX.setdefault(p, {"literal": set(), "wide": set(), "n_items": 0, "n_pn": 0, "n_present": 0, "n_absent": 0})
        d["n_items"] += 1
        gold = {fl[p][e]["slot"] for e in it.get("gold") or [] if e in fl[p] and fl[p][e]["slot"]}
        if it["label"] == "PRESENT-NEGATIVE":
            d["n_pn"] += 1
            s = pn_slots(it)
            d["literal"] |= s
            d["wide"] |= s | gold
        elif it["label"] == "PRESENT":
            d["n_present"] += 1
            d["literal"] |= gold
            d["wide"] |= gold
        else:
            d["n_absent"] += 1
            d["wide"] |= gold
    for p, d in _EX.items():
        d["wide_only"] = d["wide"] - d["literal"]
    return _EX


# ------------------------------------------------------------------ pools and padded lists (§3)
def build_pools(rows):
    """key -> {persona, committed, pool_a, pool_b, census}. Pool A: the key's own printed map names less
    the committed section, the persona's targeted slots (wide) and names containing ':'. Pool B: every
    other persona's FULL:TRUE map names less anything in this persona's own maps (the key's and the
    FULL:TRUE map) or committed section, the targeted slots and ':'; deduplicated, sorted."""
    idx = indexes()
    ex = targeted_slots()
    personas = sorted({r["persona"] for r in rows})
    full_map = {p: set(map_names(idx[f"frbank:{p}:FULL:TRUE"])) for p in personas}
    out = {}
    for k in keys_of(rows):
        persona = next(r["persona"] for r in rows if r["key"] == k)
        text = idx[k]
        com = committed_names(text)
        assert len(com) == len(set(com)), k
        own_map = set(map_names(text))
        excl = ex[persona]["wide"]
        a = sorted(n for n in own_map - set(com) - excl if poolable(n))
        others = set()
        for p2 in personas:
            if p2 != persona:
                others |= full_map[p2]
        b = sorted(n for n in others - own_map - full_map[persona] - set(com) - excl if poolable(n))
        out[k] = {"persona": persona, "committed": com, "pool_a": a, "pool_b": b,
                  "census": {"map_names": len(own_map), "committed": len(com), "pool_a": len(a), "pool_b": len(b),
                             "excluded_from_map_by_ii": len(own_map & excl), "excluded_from_map_by_ii_wide_only": len(own_map & ex[persona]["wide_only"]),
                             "excluded_from_map_by_i": len(own_map & set(com)), "colon_names": sum(1 for n in own_map if ":" in n), "unpoolable_names": sum(1 for n in own_map if not poolable(n))}}
    return out


def draw_order(key, pools):
    """D-PAD-1: one shuffle per key (random.Random(f"42:{key}")), pool A then pool B, taken in order, so
    the three lengths are nested."""
    rng = random.Random(f"42:{key}")
    a = list(pools["pool_a"]); rng.shuffle(a)
    b = list(pools["pool_b"]); rng.shuffle(b)
    return a + b, len(a)


def padded_lists(rows, pools):
    """(key, L) -> list of exactly L names (committed names kept; the padding in draw order). Asserts §3."""
    ex = targeted_slots()
    out, meta = {}, {}
    for k, P in pools.items():
        order, n_a = draw_order(k, P)
        com = list(P["committed"])
        assert len(com) <= min(LENGTHS), f"STOP: committed list longer than L on {k}: {len(com)}"
        for L in LENGTHS:
            need = L - len(com)
            pad = order[:need]
            assert len(pad) == need, f"STOP: pools exhausted on {k} at L={L}: {len(order)} < {need}"
            lst = com + pad
            assert len(lst) == L and len(set(lst)) == L, (k, L)
            assert not any(":" in n for n in lst), (k, L)
            assert not (set(pad) & ex[P["persona"]]["wide"]), (k, L, set(pad) & ex[P["persona"]]["wide"])   # the padding; a committed name may be a target (the item's own)
            assert set(com) <= set(lst)
            out[(k, L)] = lst
            meta[(k, L)] = {"from_pool_a": min(need, n_a), "from_pool_b": max(0, need - n_a)}
        # nesting
        assert out[(k, 15)] == out[(k, 30)][:15] and out[(k, 30)] == out[(k, 60)][:30], k
    return out, meta


def padded_text(text, names):
    """The committed text with its superseded section (the tail) re-rendered over `names` under the lifted cap."""
    prefix, _ = split_section(text)
    tail = render_section_lifted(names)
    assert "(+" not in tail
    return prefix + tail


def renderer_lock(pools):
    """§3: the section re-rendered over the committed names alone reproduces the committed text byte for byte."""
    idx = indexes()
    ok, bad = 0, []
    for k, P in pools.items():
        text = idx[k]
        if padded_text(text, P["committed"]) == text:
            ok += 1
        else:
            bad.append(k)
    return ok, bad


def padded_texts(pools, lists):
    idx = indexes()
    out = {}
    for (k, L), lst in lists.items():
        t = padded_text(idx[k], lst)
        # the re-parsed list must be exactly the padded list
        got = [n for n in parse(t)["superseded_attrs"] if n.strip() != MARKER]
        assert sorted(got) == sorted(lst), (k, L)
        assert split_section(t)[0] == split_section(idx[k])[0]
        out[(k, L)] = t
    return out


def prompts_digests_ok():
    import prompts_e1 as P
    return (P.file_sha256() == "337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84"
            and P.texts_sha256() == "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2")
