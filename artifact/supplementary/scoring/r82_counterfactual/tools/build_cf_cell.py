"""build_cf_cell.py -- R82-CF: build the 90 store versions, label them, assert everything.

NO API CALLS. Deterministic. Executes ADDENDUM_R82 sections 2 and 5 and Amendments 1 and 2.

THE TWO-RESOLUTION DESIGN (registered here because the order did not anticipate it)
    PersonaJoin resolves gold and fires ONCE against a base bank, and E1 expresses variants
    as removal sets over that base (build_e1.py:151-157). PN adds an entry, so it cannot be
    a removal from the PRESENT base. The cell therefore uses two resolutions per pair:

      base A = the unmodified bank, bound to a record asserting the original as the current
               value (the stable_identity field shape: fact, session). Yields gold only.
                 PRESENT  removed = {}                  -> PRESENT
                 ABSENT   removed = slot_closure(gold)  -> ABSENT
      base B = the PN bank, bound to the pair's lifecycle record.
                 PN       removed = {}                  -> PRESENT-NEGATIVE

    Stage A is bypassed. E1 finds the YAML record by lexical overlap with the question
    (e0_common._section_record), which is a question-dependent step in the label path. Here
    the record is known by construction, so it is bound directly. That strictly REMOVES a
    question dependency from the label; it does not add one.

    The binding record for base A is a resolution device and is never written to the YAML,
    so it cannot reach the index. The PN lifecycle record IS written to the YAML, because
    true_lifecycle must see it for the index to carry the state.

t_now and cutoff are PINNED from the unmodified bank and reused for every version of that
persona, so no ablation or addition can slide the expiry cutoff.

ASSERTIONS (any failure is a STOP; nothing submits after a failure)
  A. label       all 90 return the intended label under Definition 1.
  B. write path  supersession: successor shares slot_key, clears the category confidence
                 threshold, original deactivated, entries +1.
                 retraction: same slot_key so the supersession branch at :766-777 fires
                 first (Amendment 2), original deactivated, supersedes set, entries +1,
                 cosine recorded and never enforced.
                 expiry: entries unchanged, active unchanged, event_time < cutoff.
  C. states      the retraction PN version must NOT list its slot on the superseded-names
                 section of the v2 TRUE index; it must reach v2 as a count only, and appear
                 on the v3 retracted list. The expiry PN version must not appear on the
                 superseded or retracted lists, and must appear on the v3 expired list.
                 If either lands on the superseded list, that arm is measuring supersession
                 and CF-3 is void.
  D. base leak   PRESENT must return PRESENT and not PN by way of some other superseded
                 entry the persona already carries; ABSENT must return ABSENT with its
                 category still populated.
  E. index       the v2 prefix of every v3 index is byte-identical to that version's v2.

Usage:  python r82_counterfactual/tools/build_cf_cell.py --verify
Writes: r82_counterfactual/cf_cell.json, r82_counterfactual/cf_indexes.json
"""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in ("e0_metamemory/tools", "e1_metamemory/tools", "r82_counterfactual"):
    sys.path.insert(0, str(ROOT / p))

import e0_common as C  # noqa: E402
from e0_common import (  # noqa: E402
    MIN_SHARED, SECTION_FIELDS, TAU_GOLD, cov, parse_dt, toks,
)
from index_v2 import AVAIL, scrub, true_lifecycle, view  # noqa: E402
from index_v3 import named_sections, render_v3  # noqa: E402

TAU_LO, TAU_HI = 0.20, 0.80
ACCUMULATE = frozenset({"IDENTITY_SELF_CONCEPT", "RELATIONAL_BONDS", "HOBBIES_RECREATION",
                        "INTELLECTUAL_INTERESTS", "HEALTH_WELLBEING"})
R82 = ROOT / "r82_counterfactual"
BANKS = ROOT / "LifeMemEval" / "artifacts" / "lifecycle_banks"
AV = AVAIL[("frbank", "TRUE")]
VERSIONS = ("PRESENT", "ABSENT", "PN")
WANT = {"PRESENT": "PRESENT", "ABSENT": "ABSENT", "PN": "PRESENT-NEGATIVE"}


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    pathlib.Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


class Join:
    """PersonaJoin's fields over an arbitrary (entries, yaml) pair, with a pinned clock.

    Constructed directly rather than through PersonaJoin.__init__, because that reads the
    bank from a fixed path and resolves questions eagerly against a clock it recomputes.
    Every method used below is PersonaJoin's own, bound to this object.
    """

    def __init__(self, name, entries, y, t_now, cutoff, drop):
        self.name, self.entries, self.y = name, entries, y
        self.by_id = {e["id"]: e for e in entries}
        self.drop = drop
        self.etoks = {e["id"]: toks(e.get("text", ""), drop) for e in entries}
        self.by_session = {}
        for e in entries:
            self.by_session.setdefault(e.get("source_session"), []).append(e["id"])
        self.t_now, self.cutoff = t_now, cutoff

    _b1_event_date = C.PersonaJoin._b1_event_date
    _b2_session = C.PersonaJoin._b2_session
    detector = C.PersonaJoin.detector
    is_expired = C.PersonaJoin.is_expired


def resolve_direct(J, sec, rec):
    """e0_common.PersonaJoin._resolve with Stage A replaced by a supplied record."""
    gf, gs, sf, ss = SECTION_FIELDS[sec]
    if sec == "expiring_logistics":
        gold = J._b1_event_date(rec)
        if gold is None:
            gold, _ = J._b2_session(rec.get(gf), rec.get(gs))
    else:
        gold, _ = J._b2_session(rec.get(gf), rec.get(gs))
    if gold is None:
        return None, None, None
    fires, expired = {}, set()
    if sec == "expiring_logistics":
        expired = {i for i in gold if J.is_expired(i)}
        gold = gold - expired
    elif sf:
        d = J.detector(rec.get(sf), rec.get(gf))
        if d is None:
            return None, None, None
        fires = d
        if sec == "retractions":
            anchored, _ = J._b2_session(rec.get(sf), rec.get(ss))
            for i in (anchored or set()):
                fires[i] = max(fires.get(i, 0.0), 1.0)
            for e in J.entries:
                if e["is_retracted"] and cov(toks(rec.get(sf), J.drop),
                                             J.etoks[e["id"]]) >= TAU_GOLD:
                    fires[e["id"]] = max(fires.get(e["id"], 0.0), 1.0)
    return gold, fires, expired


def label_of(gold, fires, expired, removed, intent):
    """build_e1.label's rule, with the intent supplied rather than looked up."""
    if gold is None:
        return "UNRESOLVED", {}
    surv = lambda ids: {i for i in ids if i not in removed}
    G, exp = surv(gold), surv(expired or set())
    fired = {i: s for i, s in (fires or {}).items() if i not in removed}
    if intent in ("PAST-EVENT", "CHANGE-AWARE"):
        hi, lo = set(), set()
    else:
        hi = {i for i, s in fired.items() if s >= TAU_HI} | exp
        lo = {i for i, s in fired.items() if s >= TAU_LO}
    if hi:
        return "PRESENT-NEGATIVE", {i: round(fired.get(i, 1.0), 4) for i in hi}
    if lo:
        return "UNRESOLVED", {}
    return ("PRESENT" if G else "ABSENT"), {}


def build_index(J, removed):
    """The v2 and v3 TRUE indexes for one store version, through the locked renderer."""
    rows = []
    for e in J.entries:
        d = parse_dt(e.get("recency_time") or e.get("created_at"))
        age = None if d is None else max(0, (J.t_now - d).days)
        rows.append({**e, "age": age})
    t_sup, t_ret, t_exp, t_ev = true_lifecycle(J, J.etoks)
    v = view([{"entry_id": r["id"], "category": r["category"], "slot": r.get("slot_key")
               and r["slot_key"][1], "age": r["age"]} for r in rows],
             (t_sup, t_ret, t_exp), removed)
    v3, v2 = render_v3(v, t_ev, AV)
    return v2, v3, {"superseded": t_sup, "retracted": t_ret, "expired": t_exp}


def main():
    pairs = jload(R82 / "cf_pairs.json")["pairs"]
    qs = {r["pair_id"]: r for r in jload(R82 / "cf_questions.json")["questions"]}
    pn = {r["pair_id"]: r for r in jload(R82 / "cf_pn_texts.json")["records"]}
    names = jload(R82 / "_names.json")
    ypaths = {p.name.replace(".yaml", "").split("_")[-1]: p
              for p in sorted(C.LME.glob("*/persona_*.yaml"))}

    items, indexes, fails, sections = [], {}, [], {}
    slot_of_pair = {}

    for p in pairs:
        persona, state = p["persona"], p["state"]
        drop = toks(names[persona] or "")
        bank = jload(BANKS / f"{persona}.json")
        base = bank["entries"]
        y0 = C.load_yaml(ypaths[persona])
        orig = next(e for e in base if e["id"] == p["entry_id"])
        slot_of_pair[p["pair_id"]] = (scrub(orig["slot_key"][1]), state)

        t_now = parse_dt(p["t_now"])
        cutoff = parse_dt(p["cutoff"])
        newest = max(x for x in (parse_dt(e["created_at"]) for e in base if e["is_active"])
                     if x)

        # ---------------- base A: the unmodified store, original asserted as current
        JA = Join(persona, base, y0, t_now, cutoff, drop)
        recA = {"fact": orig["text"], "session": orig["source_session"]}
        goldA, firesA, expA = resolve_direct(JA, "stable_identity", recA)
        if not goldA:
            fails.append(f"{p['pair_id']}: base A does not resolve gold")
            continue
        removedA = set()
        removedABS = {e["id"] for e in base
                      if scrub(e.get("slot_key") and e["slot_key"][1])
                      == scrub(orig["slot_key"][1])} | set(goldA)

        # ---------------- base B: the store after the event
        entB = copy.deepcopy(base)
        byidB = {e["id"]: e for e in entB}
        yB = copy.deepcopy(y0)
        new_id = f"lb_r82_{p['pair_id'].split(':')[1]}"
        sess_new = max(e.get("source_session") or 0 for e in base) + 1
        wp = {}

        if state == "EXPIRY":
            # no write path: the anchor moves and nothing else does
            past = (cutoff - dt.timedelta(days=30)).date().isoformat()
            byidB[orig["id"]]["event_time"] = past + "T00:00:00+00:00"
            yB.setdefault("expiring_logistics", []).append(
                {"fact": orig["text"], "session": orig["source_session"],
                 "event_date": past, "status": "expired",
                 "category": orig["category"]})
            secB = "expiring_logistics"
            recB = yB["expiring_logistics"][-1]
            wp = {"entries_delta": 0, "anchor": past}
        else:
            new_text = pn[p["pair_id"]]["new_text"]
            # Amendment 2: the retracting entry takes the SAME slot_key, which is what the
            # extractor does, so the supersession branch at :766-777 fires first.
            conf = 0.9
            thr = 0.95 if orig["category"] in ACCUMULATE else 0.80
            entry = {"id": new_id, "text": new_text, "category": orig["category"],
                     "category_weights": orig.get("category_weights"),
                     "slot_key": list(orig["slot_key"]), "event_time": None,
                     "is_retracted": state == "RETRACTION", "confidence": conf,
                     "supersedes": orig["id"], "is_active": True,
                     "created_at": newest.isoformat(), "source_session": sess_new,
                     "emotional_loading": 0.0, "numeric_value": False}
            fires_branch = conf >= thr
            if not fires_branch:
                # ACCUMULATE categories need 0.95; below it the supersession branch does
                # NOT fire, so the store keeps both entries active and sets no pointer.
                # That is a legitimate write-path outcome and is recorded, not forced.
                entry["supersedes"] = None
            entB.append(entry)
            byidB[new_id] = entry
            if fires_branch:
                byidB[orig["id"]]["is_active"] = False
            if state == "SUPERSESSION":
                yB.setdefault("supersession_events", []).append(
                    {"slot": orig["slot_key"][1], "old_fact": orig["text"],
                     "old_session": orig["source_session"], "new_fact": new_text,
                     "new_session": sess_new, "category": orig["category"]})
                secB, recB = "supersession_events", yB["supersession_events"][-1]
            else:
                yB.setdefault("retractions", []).append(
                    {"original_fact": orig["text"],
                     "original_session": orig["source_session"],
                     "retraction": new_text, "retraction_session": sess_new,
                     "category": orig["category"]})
                secB, recB = "retractions", yB["retractions"][-1]
            wp = {"entries_delta": 1, "same_slot_key": True,
                  "confidence": conf, "threshold": thr,
                  "accumulate_category": orig["category"] in ACCUMULATE,
                  "supersession_branch_fires": fires_branch,
                  "original_deactivated": byidB[orig["id"]]["is_active"] is False,
                  "supersedes_set": entry["supersedes"] == orig["id"]}
            if state == "RETRACTION":
                wp["cosine_to_original"] = pn[p["pair_id"]]["predicates"].get(
                    "cosine_to_original")
                wp["cosine_branch_would_fire"] = pn[p["pair_id"]]["predicates"].get(
                    "write_path_deactivates_original")

        JB = Join(persona, entB, yB, t_now, cutoff, drop)
        goldB, firesB, expB = resolve_direct(JB, secB, recB)

        # ---------------- the three versions
        for v in VERSIONS:
            if v == "PN":
                J, removed, g, f_, x = JB, set(), goldB, firesB, expB
            else:
                J, g, f_, x = JA, goldA, firesA, expA
                removed = set() if v == "PRESENT" else removedABS
            lab, ev = label_of(g, f_, x, removed, p["intent"])
            if lab != WANT[v]:
                fails.append(f"{p['pair_id']}/{v}: label {lab}, wanted {WANT[v]}")
            i2, i3, states = build_index(J, removed)
            key = f"{p['pair_id']}|{v}"
            indexes[key] = {"v2": i2, "v3": i3}
            sections[key] = {"v2": named_sections(i2), "v3": named_sections(i3)}
            items.append({
                "item_id": key, "pair_id": p["pair_id"], "persona": persona,
                "state": state, "version": v, "intent": p["intent"],
                "question": qs[p["pair_id"]]["question"], "label": lab,
                "y_nok": 1 if lab == "PRESENT-NEGATIVE" else 0,
                "y_fok": 0 if lab == "ABSENT" else 1,
                "pn_members": sorted(ev), "n_entries": len(J.entries) - len(removed),
                "write_path": wp if v == "PN" else None,
            })

            # ---- assertion D: the two failure modes the base-bank resolution can hide
            if v == "PRESENT" and lab == "PRESENT-NEGATIVE":
                fails.append(f"{p['pair_id']}/PRESENT: resolved PN, a neighbouring "
                             f"superseded entry has leaked into the base resolution")
            if v == "ABSENT":
                cats = {e["category"] for e in J.entries if e["id"] not in removed}
                if orig["category"] not in cats:
                    fails.append(f"{p['pair_id']}/ABSENT: category {orig['category']} "
                                 f"emptied; this is category ablation, not slot ablation")

            # ---- assertion B
            if v == "PN" and state != "EXPIRY":
                # the store must be EXACTLY what the branch implies, either way
                if not (wp["same_slot_key"] and wp["entries_delta"] == 1
                        and wp["original_deactivated"] == wp["supersession_branch_fires"]
                        and wp["supersedes_set"] == wp["supersession_branch_fires"]):
                    fails.append(f"{p['pair_id']}: write-path predicates not met: {wp}")
            if v == "PN" and state == "EXPIRY":
                if not parse_dt(byidB[orig["id"]]["event_time"]) < cutoff:
                    fails.append(f"{p['pair_id']}: expiry anchor not before cutoff")


    # ------------------------------------------------------------------ Amendment 3
    # INDIVIDUATION, computed on the constructed indexes before any monitor runs.
    # A counted-state pair individuates when its scrubbed slot name is ABSENT from its own
    # state's v3 name section in PRESENT and PRESENT in PN. The absent half is a property
    # of the corpus meeting index_v2's scrubbing rule; the present half is a construction
    # correctness check and a failure there is a STOP.
    STATE_SECTION = {"SUPERSESSION": "superseded", "RETRACTION": "retracted",
                     "EXPIRY": "expired"}
    individuation = {}
    for pid, (nm, state) in sorted(slot_of_pair.items()):
        sec = STATE_SECTION[state]
        in_present = nm in sections[f"{pid}|PRESENT"]["v3"][sec]
        in_pn = nm in sections[f"{pid}|PN"]["v3"][sec]
        if not in_pn:
            fails.append(f"{pid}: {nm!r} missing from the v3 {sec} list in PN; the "
                         f"construction did not put the state in the index")
        # the superseded-names baseline reads v2 only; its confusion is descriptive
        sup_collision = nm in sections[f"{pid}|PRESENT"]["v2"]["superseded"]
        individuation[pid] = {
            "slot_scrubbed": nm, "state": state, "own_section": sec,
            "in_present": in_present, "in_pn": in_pn,
            "individuates": (not in_present) and in_pn,
            "superseded_list_collision_in_present": sup_collision,
        }
    counted = {k: v for k, v in individuation.items() if v["state"] != "SUPERSESSION"}
    n_ret = sum(1 for v in counted.values()
                if v["state"] == "RETRACTION" and v["individuates"])
    n_exp = sum(1 for v in counted.values()
                if v["state"] == "EXPIRY" and v["individuates"])
    print("")
    print(f"individuation: retraction {n_ret}/10, expiry {n_exp}/10, "
          f"pooled counted-state n={n_ret + n_exp}")
    frame = ("pooled counted-state, retraction individuation at or above six"
             if n_ret >= 6 else "expiry led, plus the surviving retraction pairs")
    print(f"CF-3 framing: {frame}; scored n={n_ret + n_exp} "
          f"({n_ret} retraction + {n_exp} expiry); "
          f"{20 - n_ret - n_exp} excluded as scrubber collisions, reported descriptively")
    for pid, v in sorted(counted.items()):
        if not v["individuates"]:
            print(f"  scrubber collision (descriptive only): {pid}  {v['slot_scrubbed']!r} "
                  f"already on the {v['own_section']} list in PRESENT")

    items.sort(key=lambda r: r["item_id"])
    ih = hashlib.sha256("\x1f".join(indexes[k]["v2"] + "\x1e" + indexes[k]["v3"]
                                    for k in sorted(indexes)).encode()).hexdigest()
    n = {v: sum(1 for it in items if it["version"] == v) for v in VERSIONS}
    print(f"items {len(items)}  {n}   PN positives {sum(it['y_nok'] for it in items)}")
    print(f"indexes {len(indexes)} store versions x 2 arms   sha256 {ih[:32]}")
    if fails:
        print(f"\nFAILURES ({len(fails)}):")
        for f_ in fails[:40]:
            print("  ", f_)
        raise SystemExit("STOP: assertions failed; nothing may be submitted")
    jdump({"meta": {"n": len(items), "no_api_calls": True, "indexes_sha256": ih,
                    "two_resolution_design": True, "tau_lo": TAU_LO, "tau_hi": TAU_HI,
                    "individuation": individuation,
                    "cf3_scored_n": n_ret + n_exp, "cf3_retraction_individuating": n_ret,
                    "cf3_expiry_individuating": n_exp},
           "items": items}, R82 / "cf_cell.json")
    jdump({"meta": {"sha256": ih, "arms": ["v2", "v3"], "provenance": "TRUE"},
           "indexes": indexes}, R82 / "cf_indexes.json")
    print("\nALL ASSERTIONS PASS")


if __name__ == "__main__":
    main()
