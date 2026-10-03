"""build_s2u.py -- SIDE-BUILD-1 step 2: the S2-U index (ADDENDUM_SIDE.md section S2, frozen e8b2630).
NO API CALLS. Deterministic. Idempotent.

S2-U is the committed BELIEVED store version of each of the 661 obligation items rendered by the
frozen index_v2.render with the per-bucket cap of 15 lifted, so every name block -- the
per-category attribute names and the superseded-names section -- prints in full with no
"(+N more)". Nothing else in the renderer or the states changes.

SETTLED READING (disclosed, not a deviation). index_v2.render is pinned by sha256 (verify_side
check A) and is parametric in exactly one knob, the module constant SLOT_CAP, which both slices
each bucket and prints the header note "names only, max N per category, alphabetical". Lifting
the cap therefore means setting SLOT_CAP to a value that never binds; the header follows it.
SLOT_CAP_LIFTED = 100, the smallest power of ten above the largest bucket on the 661 items (86
names; the largest superseded-names set is 50). The build asserts that no S2-U text carries a
"(+N more)" and that the same render at SLOT_CAP = 15 reproduces the committed BELIEVED text
byte for byte on 661 / 661 (the RENDERER LOCK of section S2; a mismatch is a STOP).

Gates, in order, each a STOP on failure:
  0  verify_side.py passes (subprocess, before any index is written);
  1  RENDERER LOCK: cap-15 render == committed BELIEVED text, 661 / 661;
  2  no S2-U text carries "(+N more)", the inexpressibility marker, or a name containing ':';
  3  the rendered superseded list under S2-U, parsed by index_features.parse (NB-6's parser),
     reproduces the UNCAPPED columns of section C.2: 32.55 names / item, precision 0.0357,
     recall 0.6658; the cap-15 list reproduces the rendered columns 15.0378 / 0.0348 / 0.2996;
  4  the section C.2 store facts recomputed from the banks: 5,968 inactive, 5,725 supersedes
     pointers, 104 TRUE-superseded of which 40 active; a same-slot successor pointing at every
     one of the 64 inactive TRUE-superseded entries and at 5,661 of the 5,904 other inactive ones.

Writes side_experiments/s2/:
  indexes_s2u.json   {"meta", "indexes": {"<index key with :S2U>": text}, "items": [{item_id, index_key_s2u, ...}]}
  build_s2u.json     the census, sizes, gate outcomes, the ledger values

Usage, from the repository root:  python side_experiments/tools/build_s2u.py
"""
from __future__ import annotations

import collections
import statistics
import subprocess
import sys

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import side_common as SC                                         # noqa: E402
from side_common import ROOT, E1, IX, J, C, parse_dt, ENC        # noqa: E402
from index_features import parse as nb6_parse                    # noqa: E402

S2 = SC.SIDE / "s2"
FREEZE = "e8b2630"
SLOT_CAP_LIFTED = 100
PIN_C2 = {"S2-U (uncapped)": (32.55, 0.0357, 0.6658), "BELIEVED (cap 15)": (15.0378214826, 0.0348, 0.2996), "TRUE": (1.7473524962, 1.0, 1.0)}
PIN_STORE = {"inactive": 5968, "pointers": 5725, "true_superseded": 104, "true_superseded_active": 40,
             "inactive_true_sup_pointed_same_slot": "all", "other_pointed_same_slot": (5661, 5904)}
FAILS: list[str] = []


def gate(name, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'} {name}" + (f": {detail}" if detail and not ok else ""))
    if not ok:
        FAILS.append(f"{name}: {detail}")


def believed_per_persona(rows_by, joins):
    cat_plan = J(E1 / "build/variant_plan.json")["cat_ablation"]
    per = {}
    for persona, Jn in joins.items():
        rows = sorted(rows_by["frbank"][persona], key=lambda r: r["entry_id"]); SC.ages(rows, Jn.t_now)
        b_sup, b_ret, b_exp, b_ev = IX.believed_lifecycle("frbank", rows, Jn.cutoff)
        per[persona] = (rows, ((b_sup, b_ret, b_exp), b_ev), set(cat_plan[persona]["categories"]))
    return per


def removed_set(it, rows, cats, slot_abl):
    v = it["variant"]
    if v == "FULL":
        return None
    if v == "CAT-ABLATED":
        return {r["entry_id"] for r in rows if r["category"] in cats}
    return set(slot_abl[f"{it['persona']}:{it['item_id'].split(':')[2]}"])


def render_at(cap, rows, states, events, removed):
    old = IX.SLOT_CAP
    IX.SLOT_CAP = cap
    try:
        return IX.render(IX.view(rows, states, removed), events, IX.AVAIL[("frbank", "BELIEVED")])
    finally:
        IX.SLOT_CAP = old


def names(t):
    p = nb6_parse(t)
    return list(p["superseded_attrs"]) if p["expressible"] else []


def list_metrics(texts_by_item, true_by_item):
    acc = collections.Counter()
    for iid, t in texts_by_item.items():
        R, T = set(names(t)), true_by_item[iid]
        acc["names"] += len(names(t)); acc["inter"] += len(R & T); acc["R"] += len(R); acc["T"] += len(T)
    n = len(texts_by_item)
    return acc["names"] / n, (acc["inter"] / acc["R"] if acc["R"] else 1.0), acc["inter"] / acc["T"]


def store_facts(rows_by, joins):
    """Section C.2's store facts, recomputed from the banks and the TRUE join (no manifest read for
    the rule side; the TRUE side is index_v2.true_lifecycle as everywhere)."""
    n_inactive = n_ptr = n_true = n_true_active = 0
    same_slot = {"true_inactive": [0, 0], "other": [0, 0]}
    for persona in sorted(joins):
        bank = {e["id"]: e for e in J(C.BANKS / f"{persona}.json")["entries"]}
        _, (t_sup, _, _, _) = SC.fr_states(joins, rows_by, persona)
        pointed = collections.defaultdict(list)
        for e in bank.values():
            if e.get("supersedes") and e["supersedes"] in bank:
                pointed[e["supersedes"]].append(e)
        n_ptr += sum(1 for e in bank.values() if e.get("supersedes"))
        for fid, f in bank.items():
            if not f.get("is_active"):
                n_inactive += 1
            if fid in t_sup:
                n_true += 1; n_true_active += bool(f.get("is_active"))
            if f.get("is_active"):
                continue
            # section C.2: "every inactive TRUE-superseded entry is pointed at by a same-slot successor, as
            # are 5,661 of the 5,904 others" -- denominators are ALL inactive entries, split by TRUE state
            key = "true_inactive" if fid in t_sup else "other"
            same_slot[key][1] += 1
            same_slot[key][0] += any(tuple(g.get("slot_key") or ()) == tuple(f.get("slot_key") or ()) for g in pointed.get(fid, []))
    return {"inactive": n_inactive, "pointers": n_ptr, "true_superseded": n_true, "true_superseded_active": n_true_active,
            "true_inactive_pointed_same_slot": same_slot["true_inactive"], "other_pointed_same_slot": same_slot["other"]}


def main():
    print(f"build_s2u -- SIDE-BUILD-1 step 2, ADDENDUM_SIDE.md section S2 (frozen {FREEZE}); no API call")
    print("0. verify_side.py before any index is written")
    rc = subprocess.run([sys.executable, str(SC.SIDE / "tools" / "verify_side.py")], capture_output=True, text=True).returncode
    gate("verify_side.py passes", rc == 0, f"exit {rc}")
    if FAILS:
        print("build_s2u: STOP -- verify_side failed; no index written"); return 1

    committed, rows_by, joins = SC.load_state()
    cell = J(ROOT / "r74/x4/cell_661.json")["items"]; slot_abl = J(E1 / "build/slot_ablations.json")
    gate("population 661 items, 104 PN", len(cell) == 661 and sum(i["y_nok"] for i in cell) == 104)
    per = believed_per_persona(rows_by, joins)

    print("1. RENDERER LOCK (cap 15) and the S2-U render (cap lifted)")
    s2u, items, nbad, n_more, n_marker, n_colon, sizes = {}, [], 0, 0, 0, 0, collections.defaultdict(list)
    largest_bucket = largest_sup = 0
    for it in cell:
        rows, (bst, bev), cats = per[it["persona"]]
        removed = removed_set(it, rows, cats, slot_abl)
        key_b = it["index_key"].replace(":TRUE", ":BELIEVED"); key_u = it["index_key"].replace(":TRUE", ":S2U")
        t15 = render_at(15, rows, bst, bev, removed)[0]
        nbad += t15 != committed[key_b]
        if key_u not in s2u:
            tu, _, nm = render_at(SLOT_CAP_LIFTED, rows, bst, bev, removed)
            s2u[key_u] = tu
            n_more += "(+" in tu; n_marker += IX.MARKER in tu; n_colon += sum(":" in n for n in nm)
            vw = IX.view(rows, bst, removed); by_cat = collections.defaultdict(set)
            for r in vw:
                if r["slot"]: by_cat[r["category"]].add(r["slot"])
            largest_bucket = max(largest_bucket, max(len(s) for s in by_cat.values()))
            largest_sup = max(largest_sup, len({r["slot"] for r in vw if r["superseded"] and r["slot"]}))
        items.append({"item_id": it["item_id"], "persona": it["persona"], "variant": it["variant"], "index_key_s2u": key_u,
                      "index_key_believed": key_b, "index_key_true": it["index_key"]})
        sizes["s2u_tokens"].append(len(ENC.encode(s2u[key_u]))); sizes["believed_tokens"].append(len(ENC.encode(committed[key_b])))
        sizes["s2u_lines"].append(s2u[key_u].count("\n") + 1); sizes["believed_lines"].append(committed[key_b].count("\n") + 1)
    gate("cap-15 render reproduces the committed BELIEVED text byte for byte on 661/661 items", nbad == 0, f"{nbad} differ")
    gate(f"S2-U: {len(s2u)} distinct texts over 661 items (40 FULL + 40 CAT-ABLATED + 162 SLOT-ABLATED)", len(s2u) == 242, str(len(s2u)))
    gate(f"SLOT_CAP_LIFTED = {SLOT_CAP_LIFTED} never binds: largest bucket {largest_bucket}, largest superseded set {largest_sup}; no '(+N more)' in any S2-U text",
         largest_bucket < SLOT_CAP_LIFTED and largest_sup < SLOT_CAP_LIFTED and n_more == 0, f"{largest_bucket} {largest_sup} {n_more}")
    gate("no S2-U text carries the inexpressibility marker or a name containing ':'", n_marker == 0 and n_colon == 0, f"{n_marker} {n_colon}")

    print("2. the rendered superseded list under S2-U against the section C.2 columns (index_features.parse)")
    true_by = {it["item_id"]: set(names(committed[it["index_key"]])) for it in cell}
    m = {"S2-U (uncapped)": list_metrics({i["item_id"]: s2u[i["index_key_s2u"]] for i in items}, true_by),
         "BELIEVED (cap 15)": list_metrics({i["item_id"]: committed[i["index_key_believed"]] for i in items}, true_by),
         "TRUE": list_metrics({i["item_id"]: committed[i["index_key_true"]] for i in items}, true_by)}
    for k, (pn, pp, pr) in PIN_C2.items():
        npi, prec, rec = m[k]
        tol = 5e-3 if k == "S2-U (uncapped)" else 1e-9      # section C.2 printed the uncapped names/item to two decimals
        gate(f"{k}: names/item {pn}, P {pp}, R {pr}", abs(npi - pn) < tol and abs(prec - pp) < 5e-5 and abs(rec - pr) < 5e-5,
             f"{npi:.4f} {prec:.4f} {rec:.4f}")

    print("3. section C.2 store facts recomputed from the banks")
    sf = store_facts(rows_by, joins)
    gate(f"inactive {PIN_STORE['inactive']:,}; supersedes pointers {PIN_STORE['pointers']:,}; TRUE-superseded {PIN_STORE['true_superseded']}, of which active {PIN_STORE['true_superseded_active']}",
         (sf["inactive"], sf["pointers"], sf["true_superseded"], sf["true_superseded_active"]) ==
         (PIN_STORE["inactive"], PIN_STORE["pointers"], PIN_STORE["true_superseded"], PIN_STORE["true_superseded_active"]), str(sf))
    gate(f"same-slot successor on every inactive TRUE-superseded pointed entry and on {PIN_STORE['other_pointed_same_slot'][0]:,} of {PIN_STORE['other_pointed_same_slot'][1]:,} others",
         sf["true_inactive_pointed_same_slot"][0] == sf["true_inactive_pointed_same_slot"][1]
         and tuple(sf["other_pointed_same_slot"]) == PIN_STORE["other_pointed_same_slot"], str(sf))

    if FAILS:
        print(f"\nbuild_s2u: {len(FAILS)} FAIL -- STOP (ADDENDUM_SIDE section STOP); nothing written")
        for f in FAILS:
            print("  " + f)
        return 1

    meta = {"registration": "registrations/ADDENDUM_SIDE.md", "frozen": FREEZE, "no_api_calls": True, "arm": "S2-U",
            "n_items": len(items), "n_texts": len(s2u), "key_format": "<backend>:<persona>:<variant>:S2U (SLOT-ABLATED per question)",
            "renderer": "index_v2.view -> index_v2.render under AVAIL[('frbank','BELIEVED')], SLOT_CAP lifted",
            "slot_cap_lifted": SLOT_CAP_LIFTED, "largest_bucket": largest_bucket, "largest_superseded_set": largest_sup,
            "renderer_lock": "cap-15 render == committed BELIEVED text, 661/661",
            "settled_reading": "SLOT_CAP is the frozen renderer's only knob and also prints the header note; lifted to 100, the smallest power of ten above the largest bucket (86)"}
    SC.jdump({"meta": meta, "indexes": s2u, "items": items}, S2 / "indexes_s2u.json")
    summary = {"meta": meta,
               "superseded_list": {k: {"names_per_item": v[0], "precision": v[1], "recall": v[2]} for k, v in m.items()},
               "store_facts": sf,
               "size": {k: {"mean": float(np.mean(v)), "median": float(statistics.median(v)), "max": int(max(v))} for k, v in sizes.items()},
               "gates": "all passed (see build log)"}
    SC.jdump(summary, S2 / "build_s2u.json")
    print(f"\nwrote {S2 / 'indexes_s2u.json'}, build_s2u.json")
    print("\nledger values (NUMBERS_SIDE.md section 5)")
    for k, v in m.items():
        print(f"  {k}: names/item {v[0]:.4f}, precision {v[1]:.4f}, recall {v[2]:.4f}")
    print(f"  store facts: {sf}")
    print(f"  size: S2-U {np.mean(sizes['s2u_tokens']):.1f} o200k tokens / {np.mean(sizes['s2u_lines']):.1f} lines per item vs committed BELIEVED "
          f"{np.mean(sizes['believed_tokens']):.1f} / {np.mean(sizes['believed_lines']):.1f}; max S2-U {max(sizes['s2u_tokens'])} tokens")
    print("\nbuild_s2u: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
