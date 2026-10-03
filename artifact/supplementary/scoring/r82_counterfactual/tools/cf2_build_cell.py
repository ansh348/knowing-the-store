"""cf2_build_cell.py -- CF-2: build the store versions, label them, render v2 / v3 / V2R, assert.

NO API CALLS. Deterministic. Executes ADDENDUM_CF2.md sections 2 and 5 on the closed draw
cf2/cf_pairs_cf2.json (section 16: 88 / 30 / 30, 148 pairs, 444 items).

The construction is build_cf_cell.py's, CALLED: Join, resolve_direct, label_of and build_index
are imported from that module and the per-pair loop below is its loop with the CF-2 paths;
assertion families A-E are carried over unchanged. Two things are added, both registered:

  * the draw-time predicates are RE-ASSERTED at build (section 13): for every pair, in PRESENT,
    the scrubbed slot name is absent from its own state's v3 name section and from the v2
    superseded-names list; a failure is an instrument bug and a STOP;
  * assertion C is made explicit on the emitted text: the retraction PN version's name is on
    the v3 retracted list and NOT on the v2 superseded list; the expiry PN version's name is on
    the v3 expired list and on neither of the others; the supersession PN version's name is on
    the superseded list. Individuation (absent in PRESENT, present in PN) therefore holds for
    all 148 pairs by construction and is asserted, not counted.

Step 1   python cf2_build_cell.py            -> cf2/cf_cell.json, cf2/cf_indexes.json (v2, v3)
Step 2   python cf2_build_cell.py --v2r      -> adds "v2r" to every store version of cf_indexes
         under index_v2r (seed-42 value-level derangement of the (retracted, expired) pairs,
         RENDERER LOCK asserted per version), and records the permutation in the file's meta.
"""
from __future__ import annotations

import collections
import copy
import datetime as dt
import hashlib
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in ("e0_metamemory/tools", "e1_metamemory/tools", "r82_counterfactual", "r82_counterfactual/tools"):
    sys.path.insert(0, str(ROOT / p))

import build_cf_cell as B  # noqa: E402  -- CF-1's construction, called
import e0_common as C  # noqa: E402
import index_v2r as V2R  # noqa: E402
from e0_common import parse_dt, toks  # noqa: E402
from index_v2 import scrub  # noqa: E402
from index_v3 import named_sections  # noqa: E402

CF2 = ROOT / "r82_counterfactual" / "cf2"
BANKS = B.BANKS
VERSIONS, WANT, ACCUMULATE = B.VERSIONS, B.WANT, B.ACCUMULATE
STATE_SECTION = {"SUPERSESSION": "superseded", "RETRACTION": "retracted", "EXPIRY": "expired"}
jload, jdump = B.jload, B.jdump


def build():
    pdoc = jload(CF2 / "cf_pairs_cf2.json"); pairs = pdoc["pairs"]
    quota = pdoc["meta"]["quota"]
    qs = {r["pair_id"]: r for r in jload(CF2 / "cf_questions_cf2.json")["questions"]}
    pn = {r["pair_id"]: r for r in jload(CF2 / "cf_pn_texts_cf2.json")["records"]}
    names = jload(CF2 / "_names_cf2.json")
    ypaths = {p.name.replace(".yaml", "").split("_")[-1]: p for p in sorted(C.LME.glob("*/persona_*.yaml"))}
    assert {r["pair_id"] for r in qs.values()} >= {p["pair_id"] for p in pairs}
    assert {r["pair_id"] for r in pn.values()} >= {p["pair_id"] for p in pairs}

    items, indexes, fails, sections = [], {}, [], {}
    slot_of_pair = {}
    for p in pairs:
        persona, state = p["persona"], p["state"]
        drop = toks(names[persona] or "")
        bank = jload(BANKS / f"{persona}.json"); base = bank["entries"]
        y0 = C.load_yaml(ypaths[persona])
        orig = next(e for e in base if e["id"] == p["entry_id"])
        slot_of_pair[p["pair_id"]] = (scrub(orig["slot_key"][1]), state)
        t_now, cutoff = parse_dt(p["t_now"]), parse_dt(p["cutoff"])
        newest = max(x for x in (parse_dt(e["created_at"]) for e in base if e["is_active"]) if x)

        # ---------------- base A: the unmodified store, original asserted as current
        JA = B.Join(persona, base, y0, t_now, cutoff, drop)
        recA = {"fact": orig["text"], "session": orig["source_session"]}
        goldA, firesA, expA = B.resolve_direct(JA, "stable_identity", recA)
        if not goldA:
            fails.append(f"{p['pair_id']}: base A does not resolve gold"); continue
        removedABS = {e["id"] for e in base if scrub(e.get("slot_key") and e["slot_key"][1]) == scrub(orig["slot_key"][1])} | set(goldA)

        # ---------------- base B: the store after the event
        entB = copy.deepcopy(base); byidB = {e["id"]: e for e in entB}; yB = copy.deepcopy(y0)
        new_id = f"lb_r82_{p['pair_id'].split(':')[1]}"
        sess_new = max(e.get("source_session") or 0 for e in base) + 1
        wp = {}
        if state == "EXPIRY":
            past = (cutoff - dt.timedelta(days=30)).date().isoformat()
            byidB[orig["id"]]["event_time"] = past + "T00:00:00+00:00"
            yB.setdefault("expiring_logistics", []).append(
                {"fact": orig["text"], "session": orig["source_session"], "event_date": past, "status": "expired", "category": orig["category"]})
            secB, recB = "expiring_logistics", yB["expiring_logistics"][-1]
            wp = {"entries_delta": 0, "anchor": past}
        else:
            new_text = pn[p["pair_id"]]["new_text"]
            conf = 0.9; thr = 0.95 if orig["category"] in ACCUMULATE else 0.80
            entry = {"id": new_id, "text": new_text, "category": orig["category"], "category_weights": orig.get("category_weights"),
                     "slot_key": list(orig["slot_key"]), "event_time": None, "is_retracted": state == "RETRACTION", "confidence": conf,
                     "supersedes": orig["id"], "is_active": True, "created_at": newest.isoformat(), "source_session": sess_new,
                     "emotional_loading": 0.0, "numeric_value": False}
            fires_branch = conf >= thr
            if not fires_branch:
                entry["supersedes"] = None
            entB.append(entry); byidB[new_id] = entry
            if fires_branch:
                byidB[orig["id"]]["is_active"] = False
            if state == "SUPERSESSION":
                yB.setdefault("supersession_events", []).append(
                    {"slot": orig["slot_key"][1], "old_fact": orig["text"], "old_session": orig["source_session"], "new_fact": new_text,
                     "new_session": sess_new, "category": orig["category"]})
                secB, recB = "supersession_events", yB["supersession_events"][-1]
            else:
                yB.setdefault("retractions", []).append(
                    {"original_fact": orig["text"], "original_session": orig["source_session"], "retraction": new_text,
                     "retraction_session": sess_new, "category": orig["category"]})
                secB, recB = "retractions", yB["retractions"][-1]
            wp = {"entries_delta": 1, "same_slot_key": True, "confidence": conf, "threshold": thr,
                  "accumulate_category": orig["category"] in ACCUMULATE, "supersession_branch_fires": fires_branch,
                  "original_deactivated": byidB[orig["id"]]["is_active"] is False, "supersedes_set": entry["supersedes"] == orig["id"]}
            if state == "RETRACTION":
                wp["cosine_to_original"] = pn[p["pair_id"]]["predicates"].get("cosine_to_original")
                wp["cosine_branch_would_fire"] = pn[p["pair_id"]]["predicates"].get("write_path_deactivates_original")
        JB = B.Join(persona, entB, yB, t_now, cutoff, drop)
        goldB, firesB, expB = B.resolve_direct(JB, secB, recB)

        # ---------------- the three versions
        for v in VERSIONS:
            if v == "PN":
                J, removed, g, f_, x = JB, set(), goldB, firesB, expB
            else:
                J, g, f_, x = JA, goldA, firesA, expA
                removed = set() if v == "PRESENT" else removedABS
            lab, ev = B.label_of(g, f_, x, removed, p["intent"])
            if lab != WANT[v]:
                fails.append(f"{p['pair_id']}/{v}: label {lab}, wanted {WANT[v]}")           # A
            i2, i3, _states = B.build_index(J, removed)
            key = f"{p['pair_id']}|{v}"
            indexes[key] = {"v2": i2, "v3": i3}
            sections[key] = {"v2": named_sections(i2), "v3": named_sections(i3)}
            items.append({"item_id": key, "pair_id": p["pair_id"], "persona": persona, "state": state, "version": v, "intent": p["intent"],
                          "question": qs[p["pair_id"]]["question"], "label": lab, "y_nok": 1 if lab == "PRESENT-NEGATIVE" else 0,
                          "y_fok": 0 if lab == "ABSENT" else 1, "pn_members": sorted(ev), "n_entries": len(J.entries) - len(removed),
                          "write_path": wp if v == "PN" else None})
            if v == "PRESENT" and lab == "PRESENT-NEGATIVE":                                      # D
                fails.append(f"{p['pair_id']}/PRESENT: resolved PN, a neighbouring superseded entry has leaked into the base resolution")
            if v == "ABSENT":
                cats = {e["category"] for e in J.entries if e["id"] not in removed}
                if orig["category"] not in cats:
                    fails.append(f"{p['pair_id']}/ABSENT: category {orig['category']} emptied; this is category ablation, not slot ablation")
            if v == "PN" and state != "EXPIRY":                                                   # B
                if not (wp["same_slot_key"] and wp["entries_delta"] == 1 and wp["original_deactivated"] == wp["supersession_branch_fires"]
                        and wp["supersedes_set"] == wp["supersession_branch_fires"]):
                    fails.append(f"{p['pair_id']}: write-path predicates not met: {wp}")
            if v == "PN" and state == "EXPIRY":
                if not parse_dt(byidB[orig["id"]]["event_time"]) < cutoff:
                    fails.append(f"{p['pair_id']}: expiry anchor not before cutoff")
            if not i3.startswith(i2):                                                             # E
                fails.append(f"{key}: v3 does not extend v2 byte-identically")

    # ---------------- the draw-time predicates, re-asserted; assertion C on the emitted text
    individuation = {}
    for pid, (nm, state) in sorted(slot_of_pair.items()):
        sec = STATE_SECTION[state]
        pres, pnv = sections[f"{pid}|PRESENT"], sections[f"{pid}|PN"]
        in_present = nm in pres["v3"][sec]; on_sup_present = nm in pres["v2"]["superseded"]
        in_pn = nm in pnv["v3"][sec]
        if in_present:
            fails.append(f"{pid}: draw-time individuation predicate violated at build: {nm!r} on the {sec} list in PRESENT")
        if on_sup_present:
            fails.append(f"{pid}: draw-time superseded-list exclusion violated at build: {nm!r} on the v2 superseded list in PRESENT")
        if not in_pn:
            fails.append(f"{pid}: {nm!r} missing from the v3 {sec} list in PN; the construction did not put the state in the index")
        c_ok = True
        if state == "RETRACTION":
            c_ok = nm not in pnv["v2"]["superseded"] and nm in pnv["v3"]["retracted"]
        elif state == "EXPIRY":
            c_ok = nm not in pnv["v2"]["superseded"] and nm not in pnv["v3"]["retracted"] and nm in pnv["v3"]["expired"]
        else:
            c_ok = nm in pnv["v2"]["superseded"]
        if not c_ok:
            fails.append(f"{pid}: assertion C: {state} PN version lands on the wrong name section ({ {k: nm in v for k, v in pnv['v3'].items()} })")
        individuation[pid] = {"slot_scrubbed": nm, "state": state, "own_section": sec, "in_present": in_present, "in_pn": in_pn,
                              "individuates": (not in_present) and in_pn, "superseded_list_collision_in_present": on_sup_present,
                              "assertion_c": c_ok}
    n_ind = sum(1 for v in individuation.values() if v["individuates"])

    items.sort(key=lambda r: r["item_id"])
    ih = hashlib.sha256("\x1f".join(indexes[k]["v2"] + "\x1e" + indexes[k]["v3"] for k in sorted(indexes)).encode()).hexdigest()
    n = {v: sum(1 for it in items if it["version"] == v) for v in VERSIONS}
    st = collections.Counter(it["state"] for it in items if it["version"] == "PN")
    size = {arm: {"lines_min": min(t.count("\n") + 1 for t in (x[arm] for x in indexes.values())),
                  "lines_max": max(t.count("\n") + 1 for t in (x[arm] for x in indexes.values())),
                  "chars_mean": round(sum(len(x[arm]) for x in indexes.values()) / len(indexes), 1)} for arm in ("v2", "v3")}
    print(f"items {len(items)}  {n}  composition {dict(st)}  PN positives {sum(it['y_nok'] for it in items)}")
    print(f"individuating {n_ind}/{len(individuation)}; assertion C holds on {sum(v['assertion_c'] for v in individuation.values())}/{len(individuation)}")
    print(f"indexes {len(indexes)} store versions x 2 arms   sha256 {ih[:32]}   size {size}")
    if fails:
        print(f"\nFAILURES ({len(fails)}):")
        for f_ in fails[:40]:
            print("  ", f_)
        raise SystemExit("STOP: assertions failed; nothing may be submitted")
    assert (st["SUPERSESSION"], st["RETRACTION"], st["EXPIRY"]) == (quota["SUPERSESSION"], quota["RETRACTION"], quota["EXPIRY"])
    assert n_ind == len(individuation) == len(pairs)
    jdump({"meta": {"n": len(items), "no_api_calls": True, "indexes_sha256": ih, "two_resolution_design": True,
                    "tau_lo": B.TAU_LO, "tau_hi": B.TAU_HI, "quota": quota, "composition": f"{st['SUPERSESSION']}/{st['RETRACTION']}/{st['EXPIRY']}",
                    "individuation": individuation, "individuating": n_ind, "fails": [], "index_size": size,
                    "registration": "registrations/ADDENDUM_CF2.md (frozen f016f03; sections 14-16)", "built": "2026-09-13",
                    "construction": "build_cf_cell.py functions called; assertions A-E unchanged; draw-time predicates and assertion C re-asserted"},
           "items": items}, CF2 / "cf_cell.json")
    jdump({"meta": {"sha256": ih, "arms": ["v2", "v3"], "provenance": "TRUE"}, "indexes": indexes}, CF2 / "cf_indexes.json")
    print("\nALL ASSERTIONS PASS  ->", CF2 / "cf_cell.json", CF2 / "cf_indexes.json")


def add_v2r():
    doc = jload(CF2 / "cf_indexes.json"); idx = doc["indexes"]
    assert "v2r" not in doc["meta"]["arms"], "V2R already built"
    keys = sorted(idx)
    counts = [V2R.counts_of(idx[k]["v2"]) for k in keys]
    perm, k_rot = V2R.derangement(counts, seed=V2R.SEED)
    for i, key in enumerate(keys):
        ret, exp = counts[perm[i]]
        idx[key]["v2r"] = V2R.render_v2r(idx[key]["v2"], ret, exp)      # asserts the lock per version
        V2R.assert_lock(idx[key]["v2"], idx[key]["v2r"])
        assert V2R.counts_of(idx[key]["v2r"]) == (ret, exp) != counts[i]
    own = sum(1 for i in range(len(keys)) if counts[perm[i]] == counts[i]); assert own == 0
    multiset_ok = collections.Counter(counts) == collections.Counter(counts[perm[i]] for i in range(len(keys)))
    assert multiset_ok
    changed = sum(1 for i, key in enumerate(keys) if idx[key]["v2r"] != idx[key]["v2"])
    doc["meta"]["arms"] = ["v2", "v3", "v2r"]
    doc["meta"]["v2r"] = {"seed": V2R.SEED, "method": "value-level derangement of the (retracted, expired) totals across the store versions: "
                          "positions grouped by value, shuffled within and across groups, rotated by k",
                          "rotation_k": k_rot, "n_versions": len(keys), "distinct_values": len(set(counts)),
                          "largest_value_group": max(collections.Counter(counts).values()),
                          "versions_keeping_own_pair": own, "multiset_preserved": multiset_ok, "versions_changed": changed,
                          "fields": ["LIFECYCLE TOTALS: retracted", "LIFECYCLE TOTALS: expired"],
                          "disclosed": "PER-CATEGORY BREAKDOWN RETRACT/EXPIRED columns unchanged (registration names exactly two fields)",
                          "permutation": {keys[i]: keys[perm[i]] for i in range(len(keys))},
                          "counts_true": {keys[i]: list(counts[i]) for i in range(len(keys))}}
    doc["meta"]["sha256_v2r"] = hashlib.sha256("\x1f".join(idx[k]["v2r"] for k in keys).encode()).hexdigest()
    jdump(doc, CF2 / "cf_indexes.json")
    print(f"V2R: {len(keys)} versions, rotation k={k_rot}, distinct (retracted, expired) values {len(set(counts))}, largest group "
          f"{doc['meta']['v2r']['largest_value_group']}, versions keeping own pair {own}, multiset preserved {multiset_ok}, "
          f"lock asserted on every version; sha256 {doc['meta']['sha256_v2r'][:32]}")


if __name__ == "__main__":
    add_v2r() if "--v2r" in sys.argv else build()
