"""select_pairs.py -- R82-CF: the frozen selection of 30 (persona, slot) pairs.

NO API CALLS. Deterministic. Seed 42.

Selects the 30 (persona, slot) pairs of the leak-free counterfactual cell, ten per
lifecycle state, one pair per persona from 30 distinct personas. One pair per persona
makes persona-clustering and question-clustering the same partition, which removes an
otherwise ambiguous choice of sensitivity estimator.

The rule is registered in registrations/ADDENDUM_R82.md section 3 and is applied here
without a tuning knob. Nothing about a question, a label, or a monitor score is read.

CANDIDATE PREDICATE (all four must hold)
    1. the entry carries a slot_key;
    2. that slot_key occurs EXACTLY ONCE in the whole bank, so the slot carries no
       lifecycle history of its own before the counterfactual event;
    3. the entry is is_active, not is_retracted, and supersedes nothing;
    4. its text has at least 6 content tokens, so both sides of a supersession can
       clear MIN_DISCR = 3 discriminative tokens.

CLASS PREDICATE
    SUPERSESSION  event_time is null and category is an attribute/preference category
    RETRACTION    event_time is null and category is PROJECTS_ENDEAVORS
    EXPIRY        event_time is non-null and NOT already before the persona's pinned
                  cutoff, and category is OBLIGATIONS or LOGISTICAL_CONTEXT

    The expiry class requires an unexpired anchor because the PRESENT version of an
    expiry pair must label PRESENT: the counterfactual event is the anchor passing.

ALLOCATION
    Personas are shuffled with Random(42). Classes are offered in scarcity order
    EXPIRY, RETRACTION, SUPERSESSION -- measured, not assumed: 23 of 40 personas carry
    an expiry candidate against 40 of 40 for each of the other two. Each persona takes
    the first offered class that still needs pairs and for which it has a candidate,
    then is retired. Within a (persona, class) the candidate with the lexicographically
    smallest entry id wins.

    If any class cannot fill, the script exits non-zero rather than relaxing the rule.

t_now is PINNED per persona from the unmodified bank, exactly as
e0_common.PersonaJoin does it (newest ACTIVE created_at + 24h), and cutoff is
t_now - EXPIRY_WINDOW. Both are carried into the cell file so every store version of
that persona is aged against the same clock.

Usage:  python r82_counterfactual/tools/select_pairs.py
Writes: r82_counterfactual/cf_pairs.json
"""
from __future__ import annotations

import collections
import math
import datetime as dt
import io
import json
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))

from e0_common import EXPIRY_WINDOW, parse_dt, toks  # noqa: E402

BANKS = ROOT / "LifeMemEval" / "artifacts" / "lifecycle_banks"
OUT = ROOT / "r82_counterfactual" / "cf_pairs.json"
ADJ = ROOT / "r82_counterfactual" / "adjudication.json"

SEED = 42
PER_CLASS = 10
MIN_TEXT_TOKENS = 6

SUP_CATS = frozenset({"PREFERENCES_HABITS", "IDENTITY_SELF_CONCEPT", "HEALTH_WELLBEING",
                      "HOBBIES_RECREATION", "INTELLECTUAL_INTERESTS", "FINANCIAL_MATERIAL"})
RET_CATS = frozenset({"PROJECTS_ENDEAVORS"})
EXP_CATS = frozenset({"OBLIGATIONS", "LOGISTICAL_CONTEXT"})

# Offered in measured scarcity order; see the docstring.
CLASS_ORDER = ("EXPIRY", "RETRACTION", "SUPERSESSION")

# The intent each class is questioned under. Only CURRENT-STATE and UPCOMING carry a
# negative obligation at all (build_e1.NEG_ELIGIBLE); PAST-EVENT and CHANGE-AWARE are
# structurally exempt and are never used here.
CLASS_INTENT = {
    "SUPERSESSION": "CURRENT-STATE",
    "RETRACTION": "UPCOMING",
    "EXPIRY": "UPCOMING",
}


def jdump(obj, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def persona_clock(entries):
    """t_now pinned from the FULL bank, byte-identical to PersonaJoin."""
    act = [parse_dt(e["created_at"]) for e in entries if e["is_active"]]
    act = [x for x in act if x]
    if not act:
        return None, None
    t_now = max(act) + dt.timedelta(hours=24)
    return t_now, t_now - EXPIRY_WINDOW


def candidates_for(entries, cutoff):
    """Every entry passing the candidate predicate, bucketed by class."""
    occurrences = collections.Counter()
    for e in entries:
        if e.get("slot_key"):
            occurrences[tuple(e["slot_key"])] += 1

    out = collections.defaultdict(list)
    for e in entries:
        sk = e.get("slot_key")
        if not sk or occurrences[tuple(sk)] != 1:
            continue
        if not e.get("is_active") or e.get("is_retracted") or e.get("supersedes"):
            continue
        if len(toks(e.get("text", ""), frozenset())) < MIN_TEXT_TOKENS:
            continue
        cat, evt = e.get("category"), parse_dt(e.get("event_time"))
        if evt is None and cat in SUP_CATS:
            out["SUPERSESSION"].append(e)
        if evt is None and cat in RET_CATS:
            out["RETRACTION"].append(e)
        if evt is not None and cutoff is not None and evt >= cutoff and cat in EXP_CATS:
            out["EXPIRY"].append(e)
    return out


def load_verdicts():
    """{class: {entry_id: (verdict, reason)}} from the registered adjudication."""
    d = json.load(io.open(ADJ, encoding="utf-8"))
    out = {}
    for cls in CLASS_ORDER:
        blk = d.get(cls, {})
        # keyed on (persona, entry_id): entry ids are only unique WITHIN a persona
        # (kofi lb_00511 and rosa lb_00511 are different records with different verdicts)
        out[cls] = {(v["persona"], v["entry_id"]): (v["verdict"], v["reason"])
                    for v in blk.get("verdicts", [])}
    return d["meta"], out


def main():
    propose = "--propose" in sys.argv
    kdeep = 1
    if "--k" in sys.argv:
        kdeep = int(sys.argv[sys.argv.index("--k") + 1])
    adj_meta, verdicts = load_verdicts()
    banks = {}
    for f in sorted(BANKS.glob("*.json")):
        banks[f.stem] = json.load(io.open(f, encoding="utf-8"))["entries"]

    clocks, cands = {}, {}
    for p, entries in banks.items():
        t_now, cutoff = persona_clock(entries)
        clocks[p] = (t_now, cutoff)
        cands[p] = candidates_for(entries, cutoff)

    census = {c: {"personas_with_candidate": sum(1 for p in cands if cands[p][c]),
                  "total_candidates": sum(len(cands[p][c]) for p in cands)}
              for c in CLASS_ORDER}

    rng = random.Random(SEED)
    personas = sorted(banks)
    rng.shuffle(personas)

    need = {c: PER_CLASS for c in CLASS_ORDER}
    pairs, pending = [], []

    def admissible(cls, entry, persona):
        """ELIGIBLE by registered verdict. In --propose mode an unadjudicated
        candidate is provisionally admitted so the draw can be identified and
        then adjudicated; an INELIGIBLE verdict is binding in both modes."""
        v = verdicts[cls].get((persona, entry["id"]), (None, None))[0]
        if v == "ELIGIBLE":
            return True
        if v == "INELIGIBLE":
            return False
        return propose

    for p in personas:
        if not any(need.values()):
            break
        for cls in CLASS_ORDER:
            if need[cls] <= 0 or not cands[p][cls]:
                continue
            ok = [r for r in sorted(cands[p][cls], key=lambda r: r["id"])
                  if admissible(cls, r, p)]
            if not ok:
                continue
            e = ok[0]
            if verdicts[cls].get((p, e["id"]), (None,))[0] != "ELIGIBLE":
                undone = [r for r in sorted(cands[p][cls], key=lambda r: r["id"])
                          if (p, r["id"]) not in verdicts[cls]][:kdeep]
                for r in undone:
                    pending.append({"class": cls, "persona": p, "entry_id": r["id"],
                                    "category": r["category"],
                                    "slot": r["slot_key"][1], "text": r["text"],
                                    "event_time": r.get("event_time")})
            t_now, cutoff = clocks[p]
            pairs.append({
                "pair_id": f"cf:{p}:{e['slot_key'][1]}",
                "persona": p,
                "state": cls,
                "intent": CLASS_INTENT[cls],
                "slot_key": list(e["slot_key"]),
                "entry_id": e["id"],
                "entry_text": e["text"],
                "category": e["category"],
                "source_session": e["source_session"],
                "created_at": e["created_at"],
                "event_time": e.get("event_time"),
                "t_now": t_now.isoformat(),
                "cutoff": cutoff.isoformat(),
                "n_candidates_this_persona_class": len(cands[p][cls]),
                "adjudication": verdicts[cls].get((p, e["id"]), ("", ""))[0],
                "adjudication_reason": verdicts[cls].get((p, e["id"]), ("", ""))[1],
            })
            need[cls] -= 1
            break

    if propose:
        print(f"PROPOSE mode: {len(pending)} drawn candidate(s) awaiting adjudication\n")
        for r in pending:
            print(f'--- {r["class"]}  {r["persona"]}  {r["entry_id"]}  [{r["category"]}]'
                  f'  evt={(r["event_time"] or "-")[:10]}')
            print(f'    slot: {r["slot"]}')
            print(f'    {r["text"]}')
        raise SystemExit(0)

    short = {c: n for c, n in need.items() if n > 0}
    if short:
        print(json.dumps({"census": census, "short": short}, indent=2))
        raise SystemExit(f"STOP: selection cannot fill {short} under the frozen rule and the "
                         f"registered adjudication; relaxing either requires an amendment")

    pairs.sort(key=lambda r: (r["state"], r["persona"]))
    by_state = collections.Counter(r["state"] for r in pairs)
    assert len(pairs) == 3 * PER_CLASS, len(pairs)
    assert len({r["persona"] for r in pairs}) == len(pairs), "a persona was used twice"
    assert all(by_state[c] == PER_CLASS for c in CLASS_ORDER), by_state

    jdump({"meta": {"no_api_calls": True, "seed": SEED, "per_class": PER_CLASS,
                    "min_text_tokens": MIN_TEXT_TOKENS,
                    "class_order_scarcity_first": list(CLASS_ORDER),
                    "class_intent": CLASS_INTENT,
                    "candidate_census": census,
                    "adjudication": adj_meta,
                    "sup_cats": sorted(SUP_CATS), "ret_cats": sorted(RET_CATS),
                    "exp_cats": sorted(EXP_CATS)},
            "pairs": pairs}, OUT)

    print(f"{len(pairs)} pairs over {len({r['persona'] for r in pairs})} personas -> {OUT}")
    for c in CLASS_ORDER:
        print(f"  {c:14s} {by_state[c]:2d}   candidate pool: "
              f"{census[c]['total_candidates']} over "
              f"{census[c]['personas_with_candidate']}/40 personas")




# =============================================================================================
# CF-2 (ADDENDUM_CF2.md, frozen f016f03). A NEW ENTRY POINT: nothing above this line changes,
# and `python select_pairs.py` with no flag still runs the CF-1 selection byte-identically.
# Invoke with `--cf2 --census` (Step 3: the census under the CF-2 predicate, printed beside the
# scope's) or `--cf2 --queue` (Step 4: the adjudication queue; nothing is accepted).
#
# The three registered changes (ADDENDUM_CF2 sections 2 and 3):
#   (a) draw-time individuation for all three states -- the unmodified bank is rendered through
#       true_lifecycle -> view -> render_v3 -> named_sections (build_cf_cell.build_index, the
#       locked renderer) and a candidate is rejected when its scrubbed slot name is on its
#       own-state v3 section or on the v2 superseded-names list; one pair per (persona,
#       scrubbed name);
#   (b) PER_PERSONA = 4 pairs per persona per state with a round-robin walk over the seed-42
#       persona order, replacing the single-pass `break` and the one-persona assertion;
#   (c) admission -- the expiry class widened to every category (O3); CF-1's ten expiry pairs
#       (O1) and the four ELIGIBLE expiry entries the 84 filter removed (O2) re-admitted and
#       tagged overlap by (persona, entry_id); otherwise zero overlap with the 90 (by
#       (persona, entry_id) and (persona, scrubbed slot)), the 84 (pn_members and slot-ablation
#       ids) and the 36 (persona, slot token).
# =============================================================================================
CF2_QUOTA = {"SUPERSESSION": 100, "RETRACTION": 30, "EXPIRY": 30}       # ruling of 2026-09-12; retraction 60 -> 30 by D-CF2-1 (ADDENDUM_CF2 section 14)
PER_PERSONA = 4                                                            # R2
CF2_DIR = ROOT / "r82_counterfactual" / "cf2"
CF2_QUEUE = CF2_DIR / "adjudication_queue.json"
CF2_CENSUS = CF2_DIR / "census_cf2.json"
CF2_READ = ROOT / "reviews" / "CF2_ADJUDICATION_READ.md"
O2_FOUR = frozenset({("raj", "lb_00437"), ("raj", "lb_00443"), ("raj", "lb_00447"), ("thanh", "lb_00476")})
CF1_RATES = {"EXPIRY": 0.739, "RETRACTION": 0.177, "SUPERSESSION": 0.769}   # ADDENDUM_R82 section 3.2
SCOPE_CENSUS = {"EXPIRY": [46, 41, 41, 32, 25, 25], "RETRACTION": [1590, 1379, 1173, 1053, 1048, 1043],
                "SUPERSESSION": [3347, 3230, 3230, 3187, 3170, 3133], "O3": [87, None, None, None, None, 41]}
STATE_SECTION = {"SUPERSESSION": "superseded", "RETRACTION": "retracted", "EXPIRY": "expired"}


def candidates_for_cf2(entries, cutoff):
    """The CF-1 candidate predicate unchanged; the expiry class widened to every category (O3)."""
    out = candidates_for(entries, cutoff)
    occurrences = collections.Counter(tuple(e["slot_key"]) for e in entries if e.get("slot_key"))
    for e in entries:
        sk = e.get("slot_key")
        if not sk or occurrences[tuple(sk)] != 1:
            continue
        if not e.get("is_active") or e.get("is_retracted") or e.get("supersedes"):
            continue
        if len(toks(e.get("text", ""), frozenset())) < MIN_TEXT_TOKENS:
            continue
        evt = parse_dt(e.get("event_time"))
        if evt is not None and cutoff is not None and evt >= cutoff and e.get("category") not in EXP_CATS:
            out["EXPIRY"].append(e)
    return out


def _overlap_sets():
    from index_v2 import scrub  # noqa: PLC0415  (e1_metamemory/tools is on the path via build_cf_cell)
    pairs90 = json.load(io.open(ROOT / "r82_counterfactual" / "cf_pairs.json", encoding="utf-8"))["pairs"]
    ov90_ids = {(p["persona"], p["entry_id"]) for p in pairs90}
    ov90_slots = {(p["persona"], scrub(p["slot_key"][1])) for p in pairs90}
    o1 = {(p["persona"], p["entry_id"]) for p in pairs90 if p["state"] == "EXPIRY"}
    c84 = json.load(io.open(ROOT / "e1xv_crossvendor/manifests/cell_84.json", encoding="utf-8"))["items"]
    itf = {r["item_id"]: r for r in json.load(io.open(ROOT / "e1_metamemory/build/items_final.json", encoding="utf-8"))}
    sabl = json.load(io.open(ROOT / "e1_metamemory/build/slot_ablations.json", encoding="utf-8"))
    ov84 = set()
    for it in c84:
        r = itf[it["item_id"]]
        for eid in (r.get("pn_members") or []):
            ov84.add((r["persona"], eid))
        for eid in sabl.get(r["persona"] + ":" + r["question_id"], []):
            ov84.add((r["persona"], eid))
    ov36 = {(r["persona"], r["slot"]) for r in json.load(io.open(ROOT / "r74/x5/x5_render.json", encoding="utf-8"))["rows"]}
    return ov90_ids, ov90_slots, ov84, ov36, o1


def cf2_candidates():
    """Every CF-2 candidate over the 40 banks with the draw-time flags of change (a) and the
    admission flags of change (c). Returns (rows, clocks, personas)."""
    sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
    from build_cf_cell import Join, build_index          # noqa: PLC0415  the locked renderer path
    from index_v2 import scrub                           # noqa: PLC0415
    from index_v3 import named_sections                  # noqa: PLC0415
    import e0_common as C                                # noqa: PLC0415
    ov90_ids, ov90_slots, ov84, ov36, o1 = _overlap_sets()
    _, verdicts = load_verdicts()
    ypaths = {p.name.replace(".yaml", "").split("_")[-1]: p for p in sorted(C.LME.glob("*/persona_*.yaml"))}
    rows, clocks = [], {}
    for f in sorted(BANKS.glob("*.json")):
        persona = f.stem
        if persona not in ypaths:
            continue
        entries = json.load(io.open(f, encoding="utf-8"))["entries"]
        t_now, cutoff = persona_clock(entries)
        clocks[persona] = (t_now, cutoff)
        y0 = C.load_yaml(ypaths[persona])
        blk = y0.get("persona")
        drop = toks(blk.get("name", "") if isinstance(blk, dict) else "")
        v2, v3, _ = build_index(Join(persona, entries, y0, t_now, cutoff, drop), set())
        secs = {"v2": named_sections(v2), "v3": named_sections(v3)}
        for cls, lst in candidates_for_cf2(entries, cutoff).items():
            for e in lst:
                nm = scrub(e["slot_key"][1]); key = (persona, e["id"])
                individuates = nm not in secs["v3"][STATE_SECTION[cls]]
                not_on_v2_sup = nm not in secs["v2"]["superseded"]
                ov = {"90": key in ov90_ids or (persona, nm) in ov90_slots, "84": key in ov84, "36": (persona, nm) in ov36}
                readmit = "O1" if (cls == "EXPIRY" and key in o1) else "O2" if (cls == "EXPIRY" and key in O2_FOUR) else None
                zero_overlap = not any(ov.values())
                verdict = verdicts[cls].get(key, (None, None))
                rows.append({"cls": cls, "persona": persona, "entry_id": e["id"], "slot_key": list(e["slot_key"]),
                             "slot_scrubbed": nm, "category": e["category"], "text": e["text"],
                             "event_time": e.get("event_time"), "source_session": e.get("source_session"),
                             "created_at": e.get("created_at"),
                             "o3": cls == "EXPIRY" and e["category"] not in EXP_CATS,
                             "individuates": individuates, "not_on_v2_sup": not_on_v2_sup,
                             "ov90": ov["90"], "ov84": ov["84"], "ov36": ov["36"], "overlap_tag": readmit,
                             "admitted": individuates and not_on_v2_sup and (zero_overlap or readmit is not None),
                             "verdict": verdict[0], "verdict_reason": verdict[1]})
    return rows, clocks, sorted(clocks)


def cf2_census(rows):
    """Stage counts under the CF-2 predicate, printed beside CF2_SCOPE Phase 2."""
    out = {}
    for cls in CLASS_ORDER:
        r0 = [x for x in rows if x["cls"] == cls and not x["o3"]]
        r3 = [x for x in rows if x["cls"] == cls and x["o3"]]
        def st(rs):
            s1 = [x for x in rs if x["individuates"]]; s2 = [x for x in s1 if x["not_on_v2_sup"]]
            s3 = [x for x in s2 if not x["ov90"] or x["overlap_tag"] == "O1"]
            s4 = [x for x in s3 if not x["ov84"] or x["overlap_tag"] in ("O1", "O2")]
            s5 = [x for x in s4 if not x["ov36"] or x["overlap_tag"] is not None]
            return [len(rs), len(s1), len(s2), len(s3), len(s4), len(s5)]
        adm = [x for x in rows if x["cls"] == cls and x["admitted"]]
        out[cls] = {
            "frozen_predicate_stages_cf2": st(r0), "scope_stages": SCOPE_CENSUS[cls],
            "o3_stages_cf2": st(r3) if r3 else None, "scope_o3": SCOPE_CENSUS["O3"] if cls == "EXPIRY" else None,
            "admitted": len(adm),
            "admitted_by_overlap_tag": dict(collections.Counter(x["overlap_tag"] or "zero-overlap" for x in adm)),
            "admitted_verdicts": dict(collections.Counter(x["verdict"] or "unadjudicated" for x in adm)),
            "admissible_not_ineligible": sum(1 for x in adm if x["verdict"] != "INELIGIBLE"),
            "distinct_persona_scrubbed": len({(x["persona"], x["slot_scrubbed"]) for x in adm if x["verdict"] != "INELIGIBLE"}),
            "personas": len({x["persona"] for x in adm if x["verdict"] != "INELIGIBLE"}),
        }
    order = sorted(CLASS_ORDER, key=lambda c: out[c]["admissible_not_ineligible"])
    return out, tuple(order)


def cf2_walk(rows, order, personas):
    """Change (b): the round-robin walk. Retraction and supersession follow the seed-42 persona
    order, round r offering each persona's r-th admissible candidate (by entry id) in each class
    of `order`; expiry follows ADDENDUM_CF2 section 3.1 -- persona order, exhaustive. INELIGIBLE
    verdicts are binding and leave the queue. Nothing is accepted here; acceptance, the cap of
    PER_PERSONA per persona per state and one pair per (persona, scrubbed name) apply when verdicts
    exist. `name_rank` > 1 marks a candidate that shares a scrubbed name with an earlier one of
    the same persona and class: read it only if the earlier one was INELIGIBLE."""
    rng = random.Random(SEED)
    shuffled = list(personas); rng.shuffle(shuffled)
    per = collections.defaultdict(list)          # (cls, persona) -> admissible candidates by id
    for x in sorted(rows, key=lambda r: (r["persona"], r["entry_id"])):
        if x["admitted"] and x["verdict"] != "INELIGIBLE":
            per[(x["cls"], x["persona"])].append(x)
    for lst in per.values():
        seen = collections.Counter()
        for x in lst:
            seen[x["slot_scrubbed"]] += 1; x["name_rank"] = seen[x["slot_scrubbed"]]
    queues = {}
    for cls in order:
        if cls == "EXPIRY":
            q = [x for p in personas for x in per.get((cls, p), [])]
        else:
            q, r = [], 0
            while True:
                offered = False
                for p in shuffled:
                    lst = per.get((cls, p), [])
                    if r < len(lst):
                        q.append(lst[r]); offered = True
                if not offered:
                    break
                r += 1
        queues[cls] = q
    return queues, shuffled


def cf2_estimates(queues, census):
    est = {}
    for cls in CLASS_ORDER:
        have = sum(1 for x in queues[cls] if x["verdict"] == "ELIGIBLE")
        unread = sum(1 for x in queues[cls] if x["verdict"] is None)
        need = max(0, CF2_QUOTA[cls] - have)
        reads = unread if cls == "EXPIRY" else int(round(need / CF1_RATES[cls]))
        est[cls] = {"quota": CF2_QUOTA[cls], "eligible_already": have, "still_needed": need,
                    "unadjudicated_in_queue": unread, "cf1_rate": CF1_RATES[cls],
                    "estimated_reads": min(reads, unread) if cls != "EXPIRY" else reads,
                    "rule": "exhaustive over the O3 candidates (section 3.1)" if cls == "EXPIRY" else "still_needed / CF-1 rate"}
    return est


def write_read_md(queues, order, est, shuffled):
    reg = (ROOT / "registrations" / "ADDENDUM_R82.md").read_text(encoding="utf-8").split("\n")
    i0 = next(i for i, ln in enumerate(reg) if ln.startswith("### §3.1 — Eligibility criteria"))
    i1 = next(i for i in range(i0 + 1, len(reg)) if reg[i].startswith("This is the failure mode"))
    criteria = "\n".join(reg[i0 + 1:i1]).strip()
    L = ["# CF2_ADJUDICATION_READ — the adjudication queue for the CF-2 draw, in reading order", "",
         "Emitted by `select_pairs.py --cf2 --queue` (ADDENDUM_CF2.md, frozen f016f03; composition "
         f"{CF2_QUOTA['SUPERSESSION']}/{CF2_QUOTA['RETRACTION']}/{CF2_QUOTA['EXPIRY']}, seed {SEED}, cap {PER_PERSONA} per persona per state, "
         f"scarcity order {' > '.join(order)}). Nothing has been accepted: every candidate below awaits a verdict "
         "or carries the one CF-1 recorded. Read in order; stop when the quota is filled under the cap and the "
         "one-pair-per-(persona, scrubbed name) rule. A candidate marked `name rank 2+` shares its scrubbed name with "
         "an earlier candidate of the same persona and class: read it only if that one was INELIGIBLE.", "",
         "## The criteria, verbatim from ADDENDUM_R82.md §3.1 (frozen; ADDENDUM_CF2.md §3.1 carries them unchanged)", "",
         criteria, "",
         "## Reads to fill each quota at CF-1's rates", "",
         "| State | Quota | ELIGIBLE already | Still needed | Unadjudicated in queue | CF-1 rate | Estimated reads |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    for cls in order:
        e = est[cls]
        L.append(f"| {cls} | {e['quota']} | {e['eligible_already']} | {e['still_needed']} | {e['unadjudicated_in_queue']} | {e['cf1_rate']} | **{e['estimated_reads']}** ({e['rule']}) |")
    L += ["", f"Seed-42 persona order for the retraction and supersession walks: {', '.join(shuffled)}.", ""]
    for cls in order:
        q = queues[cls]; e = est[cls]
        L += [f"## {cls} — {len(q)} candidates in the queue", ""]
        marker = None if cls == "EXPIRY" else e["estimated_reads"]
        n_unread = 0
        for x in q:
            pos = x["position"]
            L.append(f"### {cls} {pos:04d} — {x['persona']} `{x['entry_id']}` — `{x['slot_key'][1]}` [{x['category']}]"
                     + (f" — overlap {x['overlap_tag']}" if x["overlap_tag"] else "")
                     + (f" — name rank {x['name_rank']}" if x["name_rank"] > 1 else ""))
            if x["event_time"]:
                L.append(f"event_time {str(x['event_time'])[:10]} · session {x['source_session']}")
            L.append(f"> {x['text']}")
            if x["verdict"]:
                L.append(f"Verdict: **{x['verdict']}** (CF-1, reused){(' — ' + x['verdict_reason']) if x['verdict_reason'] else ''}")
            else:
                L.append("Verdict: ")
                n_unread += 1
                if marker is not None and n_unread == marker:
                    L.append(""); L.append(f"— expected reads at CF-1's rate reached here ({marker}); continue only if the quota is not yet filled —")
            L.append("")
    CF2_READ.write_text("\n".join(L), encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------------------------
# CF-2 verdict merge and acceptance walk (ADDENDUM_CF2 sections 3 and 3.1; D-CF2-1 quota).
#   --cf2 --merge    merge cf2/verdicts_12sep.json into cf2/adjudication_queue.json by
#                    (state, entry_id) and regenerate cf2/adjudication_cf2.json
#   --cf2 --accept   the acceptance walk over the merged queue: ELIGIBLE rows only, in queue
#                    order, under PER_PERSONA per persona per state and one pair per
#                    (persona, scrubbed name) across the whole draw; stops at the quota;
#                    exits non-zero on a shortfall rather than relaxing anything.
# Nothing here drafts a question or builds a store version.
# ---------------------------------------------------------------------------------------------
CF2_VERDICTS = CF2_DIR / "verdicts_12sep.json"
CF2_ADJ = CF2_DIR / "adjudication_cf2.json"
CF2_PAIRS = CF2_DIR / "cf_pairs_cf2.json"
VERDICT_DATE = "2026-09-12"


def _sha256_file(p):
    import hashlib  # noqa: PLC0415
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def cf2_merge_verdicts():
    """Merge the author's verdict file into the queue by (state, entry_id); regenerate the
    adjudication file. REUSED keeps CF-1's verdict; ELIGIBLE / INELIGIBLE are the author's of
    VERDICT_DATE; SKIP-RANK rows were not read because an earlier same-name candidate for that
    persona was ELIGIBLE and are recorded as not adjudicated with that reason; UNREAD rows lie
    past each state's stop and stay unread."""
    import pathlib as _pl  # noqa: PLC0415
    qdoc = json.load(io.open(CF2_QUEUE, encoding="utf-8"))
    vdoc = json.load(io.open(CF2_VERDICTS, encoding="utf-8"))
    cf1 = json.load(io.open(ADJ, encoding="utf-8"))
    cf1_reason = {(v["persona"], v["entry_id"]): v.get("reason", "")
                  for cls in CLASS_ORDER for v in cf1[cls]["verdicts"]}
    by_state = collections.defaultdict(dict)
    for r in vdoc["verdicts"]:
        by_state[r["state"]][r["entry_id"], r["persona"]] = r
    stops, counts, out_adj = {}, {}, {}
    for cls, q in qdoc["queues"].items():
        rows = by_state[cls]
        read_pos = [x["position"] for x in q if rows[(x["entry_id"], x["persona"])]["verdict"] not in ("UNREAD", "")]
        stops[cls] = max(read_pos) if read_pos else 0
        c = collections.Counter()
        first_elig_name = {}          # (persona, scrubbed) -> position of the earliest ELIGIBLE / REUSED
        verdict_rows = []
        for x in q:
            r = rows[(x["entry_id"], x["persona"])]
            assert r["slot"] == x["slot_key"][1], (cls, x["position"], "slot mismatch")
            st = r["verdict"]; key = (x["persona"], x["slot_scrubbed"])
            if st == "REUSED":
                assert x["verdict"] == "ELIGIBLE", (cls, x["position"], "REUSED without a CF-1 ELIGIBLE")
                adj = {"status": "ELIGIBLE", "verdict": "ELIGIBLE", "source": "CF-1 reused",
                       "reason": cf1_reason.get((x["persona"], x["entry_id"]), "")}
            elif st in ("ELIGIBLE", "INELIGIBLE"):
                adj = {"status": st, "verdict": st, "source": f"author {VERDICT_DATE}", "reason": ""}
            elif st == "SKIP-RANK":
                assert x["name_rank"] > 1, (cls, x["position"], "SKIP-RANK at rank 1")
                p0 = first_elig_name.get(key)
                assert p0 is not None, (cls, x["position"], "SKIP-RANK without an earlier ELIGIBLE same-name candidate")
                adj = {"status": "NOT-ADJUDICATED", "verdict": None, "source": None,
                       "reason": f"not read: an earlier same-name candidate for this persona was ELIGIBLE (position {p0})"}
            elif st == "UNREAD":
                assert x["position"] > stops[cls], (cls, x["position"], "UNREAD before the state's stop")
                adj = {"status": "UNREAD", "verdict": None, "source": None,
                       "reason": f"past the state's stop (position {stops[cls]})"}
            else:
                raise SystemExit(f"STOP: unknown walk status {st!r} at {cls} {x['position']}")
            if adj["status"] == "ELIGIBLE" and key not in first_elig_name:
                first_elig_name[key] = x["position"]
            x["adjudication"] = {**adj, "walk_status": st}
            c[st] += 1
            verdict_rows.append({"n": x["position"], "persona": x["persona"], "entry_id": x["entry_id"],
                                 "slot": x["slot_key"][1], "slot_scrubbed": x["slot_scrubbed"], "category": x["category"],
                                 "name_rank": x["name_rank"], "overlap_tag": x["overlap_tag"], "walk_status": st,
                                 "verdict": adj["verdict"], "status": adj["status"], "source": adj["source"], "reason": adj["reason"]})
        reads = c["ELIGIBLE"] + c["INELIGIBLE"]
        counts[cls] = {"rows": len(q), "walk_status_counts": dict(c), "stop_position": stops[cls],
                       "verdict_reads": reads, "reads_including_rank_skips": reads + c["SKIP-RANK"],
                       "eligible_new": c["ELIGIBLE"], "eligible_reused": c["REUSED"],
                       "eligible_total": c["ELIGIBLE"] + c["REUSED"],
                       "eligibility_rate_new_over_verdict_reads": round(c["ELIGIBLE"] / reads, 4) if reads else None}
        out_adj[cls] = {**counts[cls], "verdicts": verdict_rows}
    qdoc["meta"]["adjudication"] = {"source_file": str(CF2_VERDICTS.relative_to(ROOT)).replace("\\", "/"),
                                    "source_sha256": _sha256_file(CF2_VERDICTS), "date": VERDICT_DATE,
                                    "merged_by": "(state, entry_id)", "stops": stops, "counts": counts}
    jdump(qdoc, CF2_QUEUE)
    notes = vdoc.get("notes", [])
    adj_doc = {"meta": {"no_api_calls": True,
                        "registration": "registrations/ADDENDUM_CF2.md (frozen f016f03; Amendment 1 / D-CF2-1 at section 14)",
                        "written_before_any_acceptance_store_version_index_label_or_score": True, "date": VERDICT_DATE,
                        "criteria": "ADDENDUM_R82.md section 3.1, verbatim, carried unchanged by ADDENDUM_CF2.md section 3.1",
                        "source_file": qdoc["meta"]["adjudication"]["source_file"], "source_sha256": qdoc["meta"]["adjudication"]["source_sha256"],
                        "queue": "r82_counterfactual/cf2/adjudication_queue.json (positions are its positions; every row checked)",
                        "walk_status_values": {"ELIGIBLE": "author's verdict", "INELIGIBLE": "author's verdict",
                                               "REUSED": "CF-1 verdict ELIGIBLE carried, not re-read",
                                               "SKIP-RANK": "not read: an earlier same-name candidate for the persona was ELIGIBLE; recorded as not adjudicated",
                                               "UNREAD": "past the state's stop; stays unread"},
                        "author_notes": notes, "stops": stops}, **out_adj}
    jdump(adj_doc, CF2_ADJ)
    print(f"merged {sum(v['rows'] for v in counts.values())} rows from {CF2_VERDICTS.name} (sha256 {qdoc['meta']['adjudication']['source_sha256'][:12]}...)")
    for cls in CLASS_ORDER:
        c = counts[cls]
        print(f"  {cls:12s} {c['walk_status_counts']}  stop {c['stop_position']}  verdict reads {c['verdict_reads']}  "
              f"eligible {c['eligible_total']} ({c['eligible_new']} new + {c['eligible_reused']} reused)  rate {c['eligibility_rate_new_over_verdict_reads']}")
    print(f"  -> {CF2_QUEUE}\n  -> {CF2_ADJ}")
    return 0


def cf2_accept():
    """The acceptance walk. ELIGIBLE rows only (author's or CF-1 reused), in queue order, states
    in scarcity order, PER_PERSONA per persona per state, one pair per (persona, scrubbed name)
    across the whole draw; stops at CF2_QUOTA. A shortfall is a STOP (exit 3)."""
    qdoc = json.load(io.open(CF2_QUEUE, encoding="utf-8"))
    if "adjudication" not in qdoc["meta"]:
        raise SystemExit("STOP: run --cf2 --merge first; the queue carries no verdicts")
    order = tuple(qdoc["meta"]["scarcity_order"])
    banks = {}
    clocks = {}
    for f in sorted(BANKS.glob("*.json")):
        ents = json.load(io.open(f, encoding="utf-8"))["entries"]
        banks[f.stem] = {e["id"]: e for e in ents}
        clocks[f.stem] = persona_clock(ents)
    used_names = set()
    cap = collections.defaultdict(collections.Counter)      # persona -> state -> accepted
    pairs, passed_over, short = [], [], {}
    for cls in order:
        n = 0
        for x in qdoc["queues"][cls]:
            if n >= CF2_QUOTA[cls]:
                break
            a = x["adjudication"]
            if a["status"] != "ELIGIBLE":
                continue
            key = (x["persona"], x["slot_scrubbed"])
            if cap[x["persona"]][cls] >= PER_PERSONA:
                passed_over.append({"state": cls, "position": x["position"], "persona": x["persona"], "entry_id": x["entry_id"],
                                    "slot_scrubbed": x["slot_scrubbed"], "why": f"cap {PER_PERSONA} per persona per state"}); continue
            if key in used_names:
                passed_over.append({"state": cls, "position": x["position"], "persona": x["persona"], "entry_id": x["entry_id"],
                                    "slot_scrubbed": x["slot_scrubbed"], "why": "one pair per (persona, scrubbed name) across the draw"}); continue
            e = banks[x["persona"]][x["entry_id"]]
            t_now, cutoff = clocks[x["persona"]]
            pairs.append({"pair_id": f"cf2:{x['persona']}:{e['slot_key'][1]}", "persona": x["persona"], "state": cls,
                          "intent": CLASS_INTENT[cls], "slot_key": list(e["slot_key"]), "slot_scrubbed": x["slot_scrubbed"],
                          "entry_id": e["id"], "entry_text": e["text"], "category": e["category"],
                          "source_session": e.get("source_session"), "created_at": e.get("created_at"),
                          "event_time": e.get("event_time"), "t_now": t_now.isoformat(), "cutoff": cutoff.isoformat(),
                          "queue_position": x["position"], "overlap_tag": x["overlap_tag"], "o3": x["o3"],
                          "adjudication": a["verdict"], "adjudication_source": a["source"], "adjudication_reason": a["reason"]})
            used_names.add(key); cap[x["persona"]][cls] += 1; n += 1
        if n < CF2_QUOTA[cls]:
            short[cls] = CF2_QUOTA[cls] - n
    by_state = collections.Counter(p["state"] for p in pairs)
    per_persona = {p: dict(c) for p, c in sorted(cap.items())}
    print("acceptance walk (ELIGIBLE only; scarcity order " + " > ".join(order) + f"; cap {PER_PERSONA}; one pair per (persona, scrubbed name))")
    for cls in order:
        print(f"  {cls:12s} accepted {by_state[cls]:3d} / quota {CF2_QUOTA[cls]}" + (f"   SHORT by {short[cls]}" if cls in short else ""))
    print(f"  personas used {len(per_persona)}; max per persona per state {max((max(c.values()) for c in cap.values()), default=0)}; "
          f"passed over at acceptance {len(passed_over)} ({collections.Counter(p['why'].split()[0] for p in passed_over)})")
    print("  per persona (SUP/RET/EXP):", ", ".join(f"{p} {c.get('SUPERSESSION', 0)}/{c.get('RETRACTION', 0)}/{c.get('EXPIRY', 0)}" for p, c in per_persona.items()))
    if short:
        print(json.dumps({"short": short}, indent=2))
        raise SystemExit(3)
    assert len(pairs) == sum(CF2_QUOTA.values()), len(pairs)
    assert len({(p["persona"], p["slot_scrubbed"]) for p in pairs}) == len(pairs), "a (persona, scrubbed name) was used twice"
    assert all(v <= PER_PERSONA for c in cap.values() for v in c.values()), "cap exceeded"
    assert all(p["adjudication"] == "ELIGIBLE" for p in pairs)
    pairs.sort(key=lambda r: (r["state"], r["queue_position"]))
    jdump({"meta": {"no_api_calls": True, "registration": "registrations/ADDENDUM_CF2.md (frozen f016f03; Amendment 1 / D-CF2-1)",
                    "date": VERDICT_DATE, "seed": SEED, "quota": CF2_QUOTA, "per_persona": PER_PERSONA,
                    "scarcity_order": list(order), "one_pair_per_persona_scrubbed_name": "across the whole draw",
                    "verdicts": qdoc["meta"]["adjudication"], "accepted_by_state": dict(by_state),
                    "accepted_per_persona": per_persona, "passed_over_at_acceptance": passed_over,
                    "class_intent": CLASS_INTENT, "no_question_drafted": True, "no_store_version_built": True},
           "pairs": pairs}, CF2_PAIRS)
    print(f"  -> {CF2_PAIRS}")
    return 0


# ---------------------------------------------------------------------------------------------
# D-CF2-2 (ruling of 2026-09-12): exclude a pair whose original record cannot satisfy
# author_pn.py's write-path predicates after the frozen retry, and replace it by the next
# ELIGIBLE candidate of the same state in walk order under the cap and the one-per-name rule
# across states. The excluded pair keeps its ELIGIBLE verdict and carries the failing report.
#   --cf2 --exclude <pair_id> --reason "<text>" --report <path to the tool's JSON report>
# ---------------------------------------------------------------------------------------------
def cf2_exclude_and_replace(pair_id, reason, report_path):
    doc = json.load(io.open(CF2_PAIRS, encoding="utf-8"))
    qdoc = json.load(io.open(CF2_QUEUE, encoding="utf-8"))
    report = json.load(io.open(report_path, encoding="utf-8"))
    pairs = doc["pairs"]
    idx = next((i for i, p in enumerate(pairs) if p["pair_id"] == pair_id), None)
    if idx is None:
        raise SystemExit(f"STOP: {pair_id} is not an accepted pair")
    ex = pairs.pop(idx)
    ex["excluded"] = {"reason": reason, "deviation": "D-CF2-2", "date": VERDICT_DATE, "report": report,
                      "eligibility_verdict_stands": ex["adjudication"] == "ELIGIBLE"}
    doc["meta"].setdefault("excluded", []).append(ex)
    cls = ex["state"]
    # current constraints from the remaining accepted pairs
    used_names = {(p["persona"], p["slot_scrubbed"]) for p in pairs}
    cap = collections.Counter((p["persona"], p["state"]) for p in pairs)
    taken = {(p["state"], p["queue_position"]) for p in pairs} | {(e["state"], e["queue_position"]) for e in doc["meta"]["excluded"]}
    banks, clocks = {}, {}
    rep = None
    for x in qdoc["queues"][cls]:                     # walk order, from position 1
        if (cls, x["position"]) in taken or x["adjudication"]["status"] != "ELIGIBLE":
            continue
        if cap[(x["persona"], cls)] >= PER_PERSONA or (x["persona"], x["slot_scrubbed"]) in used_names:
            continue
        if x["persona"] not in banks:
            ents = json.load(io.open(BANKS / f"{x['persona']}.json", encoding="utf-8"))["entries"]
            banks[x["persona"]] = {e["id"]: e for e in ents}; clocks[x["persona"]] = persona_clock(ents)
        e = banks[x["persona"]][x["entry_id"]]; t_now, cutoff = clocks[x["persona"]]
        rep = {"pair_id": f"cf2:{x['persona']}:{e['slot_key'][1]}", "persona": x["persona"], "state": cls,
               "intent": CLASS_INTENT[cls], "slot_key": list(e["slot_key"]), "slot_scrubbed": x["slot_scrubbed"],
               "entry_id": e["id"], "entry_text": e["text"], "category": e["category"],
               "source_session": e.get("source_session"), "created_at": e.get("created_at"),
               "event_time": e.get("event_time"), "t_now": t_now.isoformat(), "cutoff": cutoff.isoformat(),
               "queue_position": x["position"], "overlap_tag": x["overlap_tag"], "o3": x["o3"],
               "adjudication": x["adjudication"]["verdict"], "adjudication_source": x["adjudication"]["source"],
               "adjudication_reason": x["adjudication"]["reason"],
               "replaces": pair_id, "replacement_under": "D-CF2-2"}
        break
    if rep is None:
        doc["meta"]["quota_shortfall"] = doc["meta"].get("quota_shortfall", []) + [{"state": cls, "excluded": pair_id}]
        jdump(doc, CF2_PAIRS)
        raise SystemExit(f"STOP: no ELIGIBLE {cls} candidate remains in walk order under the cap and the "
                         f"one-per-name rule; {cls}'s quota drops by one under a further deviation")
    pairs.append(rep)
    pairs.sort(key=lambda r: (r["state"], r["queue_position"]))
    by_state = collections.Counter(p["state"] for p in pairs)
    assert dict(by_state) == CF2_QUOTA, by_state
    assert len({(p["persona"], p["slot_scrubbed"]) for p in pairs}) == len(pairs)
    assert max(collections.Counter((p["persona"], p["state"]) for p in pairs).values()) <= PER_PERSONA
    doc["meta"]["accepted_by_state"] = dict(by_state)
    doc["meta"]["accepted_per_persona"] = {p: dict(c) for p, c in sorted(
        {pp: collections.Counter(q["state"] for q in pairs if q["persona"] == pp) for pp in {q["persona"] for q in pairs}}.items())}
    doc["meta"].setdefault("replacements", []).append({"excluded": pair_id, "replacement": rep["pair_id"],
                                                        "state": cls, "queue_position": rep["queue_position"],
                                                        "overlap_tag": rep["overlap_tag"], "o3": rep["o3"], "deviation": "D-CF2-2"})
    jdump(doc, CF2_PAIRS)
    print(f"excluded  {pair_id}  ({cls}, position {ex['queue_position']}): {reason}; verdict {ex['adjudication']} stands")
    print(f"replaced by {rep['pair_id']}  (position {rep['queue_position']}, tag {rep['overlap_tag']}, o3 {rep['o3']})")
    print(f"  composition {dict(by_state)}; -> {CF2_PAIRS}")
    return 0


# ---------------------------------------------------------------------------------------------
# D-CF2-2 batch (ruling of 2026-09-13): exclude a list of pairs, then refill each state's quota by
# the walk under the cap and the one-per-name rule across states, using every freed name and cap
# slot. Where a state's ELIGIBLE spares run out the shortfall is recorded as PENDING (the queue is
# extended by an adjudication read, reviews/CF2_ADJUDICATION_READ_EXT.md) rather than dropped.
#   --cf2 --exclude-batch <spec.json>    spec: [{"pair_id", "reason", "report"}, ...]
# The excluded pairs' question rows and PN records move to meta.excluded_* of their files.
# ---------------------------------------------------------------------------------------------
def _pair_from_queue_row(x, cls, banks, clocks, replaces):
    if x["persona"] not in banks:
        ents = json.load(io.open(BANKS / f"{x['persona']}.json", encoding="utf-8"))["entries"]
        banks[x["persona"]] = {e["id"]: e for e in ents}; clocks[x["persona"]] = persona_clock(ents)
    e = banks[x["persona"]][x["entry_id"]]; t_now, cutoff = clocks[x["persona"]]
    return {"pair_id": f"cf2:{x['persona']}:{e['slot_key'][1]}", "persona": x["persona"], "state": cls,
            "intent": CLASS_INTENT[cls], "slot_key": list(e["slot_key"]), "slot_scrubbed": x["slot_scrubbed"],
            "entry_id": e["id"], "entry_text": e["text"], "category": e["category"],
            "source_session": e.get("source_session"), "created_at": e.get("created_at"),
            "event_time": e.get("event_time"), "t_now": t_now.isoformat(), "cutoff": cutoff.isoformat(),
            "queue_position": x["position"], "overlap_tag": x["overlap_tag"], "o3": x["o3"],
            "adjudication": x["adjudication"]["verdict"], "adjudication_source": x["adjudication"]["source"],
            "adjudication_reason": x["adjudication"]["reason"], "replaces": replaces, "replacement_under": "D-CF2-2"}


def cf2_refill(doc, qdoc, banks, clocks):
    """Walk each short state from position 1 under the current constraints; return new pairs."""
    pairs = doc["pairs"]
    taken = {(p["state"], p["queue_position"]) for p in pairs} | {(e["state"], e["queue_position"]) for e in doc["meta"].get("excluded", [])}
    used_names = {(p["persona"], p["slot_scrubbed"]) for p in pairs}
    cap = collections.Counter((p["persona"], p["state"]) for p in pairs)
    new, pending = [], {}
    for cls in qdoc["meta"]["scarcity_order"]:
        have = sum(1 for p in pairs if p["state"] == cls)
        waiting = [e["pair_id"] for e in doc["meta"].get("excluded", []) if e["state"] == cls and not e.get("replaced_by")]
        for x in qdoc["queues"][cls]:
            if have >= effective_quota(doc)[cls]:
                break
            if (cls, x["position"]) in taken or x["adjudication"]["status"] != "ELIGIBLE":
                continue
            if cap[(x["persona"], cls)] >= PER_PERSONA or (x["persona"], x["slot_scrubbed"]) in used_names:
                continue
            rep = _pair_from_queue_row(x, cls, banks, clocks, waiting.pop(0) if waiting else None)
            pairs.append(rep); new.append(rep); have += 1
            taken.add((cls, x["position"])); used_names.add((x["persona"], x["slot_scrubbed"])); cap[(x["persona"], cls)] += 1
            for e in doc["meta"].get("excluded", []):
                if e["pair_id"] == rep["replaces"]:
                    e["replaced_by"] = rep["pair_id"]
        if have < effective_quota(doc)[cls]:
            pending[cls] = effective_quota(doc)[cls] - have
    return new, pending


def cf2_exclude_batch(spec_path):
    """--exclude-batch <spec.json>; --refill runs the same walk with an empty exclusion list."""
    spec = json.load(io.open(spec_path, encoding="utf-8")) if spec_path else []
    doc = json.load(io.open(CF2_PAIRS, encoding="utf-8")); qdoc = json.load(io.open(CF2_QUEUE, encoding="utf-8"))
    qfile = CF2_DIR / "cf_questions_cf2.json"; pnfile = CF2_DIR / "cf_pn_texts_cf2.json"
    qd = json.load(io.open(qfile, encoding="utf-8")) if qfile.exists() else None
    pn = json.load(io.open(pnfile, encoding="utf-8")) if pnfile.exists() else None
    by_id = {p["pair_id"]: p for p in doc["pairs"]}
    for s in spec:
        ex = by_id.get(s["pair_id"])
        if ex is None:
            raise SystemExit(f"STOP: {s['pair_id']} is not an accepted pair")
        doc["pairs"].remove(ex)
        ex["excluded"] = {"reason": s["reason"], "deviation": "D-CF2-2", "date": s.get("date", VERDICT_DATE), "report": s.get("report"),
                          "eligibility_verdict_stands": ex["adjudication"] == "ELIGIBLE"}
        doc["meta"].setdefault("excluded", []).append(ex)
        if qd is not None:
            rows = [r for r in qd["questions"] if r["pair_id"] == s["pair_id"]]
            qd["questions"] = [r for r in qd["questions"] if r["pair_id"] != s["pair_id"]]
            qd["meta"].setdefault("excluded_questions", []).extend({**r, "excluded_under": "D-CF2-2", "reason": s["reason"]} for r in rows)
        if pn is not None:
            recs = [r for r in pn["records"] if r["pair_id"] == s["pair_id"]]
            pn["records"] = [r for r in pn["records"] if r["pair_id"] != s["pair_id"]]
            pn["meta"].setdefault("excluded_records", []).extend({**r, "excluded_under": "D-CF2-2", "reason": s["reason"]} for r in recs)
    banks, clocks = {}, {}
    new, pending = cf2_refill(doc, qdoc, banks, clocks)
    doc["pairs"].sort(key=lambda r: (r["state"], r["queue_position"]))
    by_state = collections.Counter(p["state"] for p in doc["pairs"])
    assert len({(p["persona"], p["slot_scrubbed"]) for p in doc["pairs"]}) == len(doc["pairs"])
    assert max(collections.Counter((p["persona"], p["state"]) for p in doc["pairs"]).values()) <= PER_PERSONA
    for cls in CF2_QUOTA:
        assert by_state[cls] + pending.get(cls, 0) == effective_quota(doc)[cls], (cls, by_state[cls], pending)
    doc["meta"]["accepted_by_state"] = dict(by_state)
    doc["meta"]["accepted_per_persona"] = {pp: dict(collections.Counter(q["state"] for q in doc["pairs"] if q["persona"] == pp))
                                           for pp in sorted({q["persona"] for q in doc["pairs"]})}
    doc["meta"]["pending_replacements"] = pending
    doc["meta"]["pending_draft"] = sorted(set(doc["meta"].get("pending_draft", [])) | {r["pair_id"] for r in new})
    doc["meta"].setdefault("replacements", []).extend({"excluded": r["replaces"], "replacement": r["pair_id"], "state": r["state"],
                                                        "queue_position": r["queue_position"], "overlap_tag": r["overlap_tag"],
                                                        "o3": r["o3"], "deviation": "D-CF2-2"} for r in new)
    jdump(doc, CF2_PAIRS)
    if qd is not None:
        import hashlib  # noqa: PLC0415
        qd["questions"].sort(key=lambda r: r["pair_id"]); qd["meta"]["n"] = len(qd["questions"])
        qd["meta"]["questions_sha256"] = hashlib.sha256("\x1f".join(r["question"] for r in qd["questions"]).encode("utf-8")).hexdigest()
        jdump(qd, qfile)
    if pn is not None:
        pn["records"].sort(key=lambda r: r["pair_id"]); jdump(pn, pnfile)
    print(f"excluded {len(spec)} pairs; accepted now {dict(by_state)}; pending {pending}")
    for r in new:
        print(f"  replacement {r['pair_id']}  (pos {r['queue_position']}, tag {r['overlap_tag']}, o3 {r['o3']})  for {r['replaces']}")
    return 0


# ---------------------------------------------------------------------------------------------
# Queue extension (ruling of 2026-09-13, D-CF2-2 disposition): when a state's ELIGIBLE spares are
# exhausted by replacements, the adjudication read continues down the SAME walk order from the
# first unread position. Nothing is re-walked and nothing is re-ordered; the extension prints the
# next admissible candidates in the original read file's format for the author's verdicts.
#   --cf2 --extend <STATE> --n <candidates>       -> reviews/CF2_ADJUDICATION_READ_EXT.md
# Sizing rule (the author's): shortfall / (eligibility rate x authoring-and-read pass rate), with
# margin; the rates are the observed ones on this state's read so far and are printed, not assumed.
# A candidate whose persona already holds PER_PERSONA accepted pairs in the state, or whose
# (persona, scrubbed name) is already an accepted pair's, is printed as SKIPPED (not readable) and
# does not count toward n. Its verdicts are merged by --merge like any other row.
# ---------------------------------------------------------------------------------------------
VERDICT_DATE_EXT = "2026-09-13"
CF2_READ_EXT = ROOT / "reviews" / "CF2_ADJUDICATION_READ_EXT.md"


def cf2_extend(cls, n_read, pass_rate):
    doc = json.load(io.open(CF2_PAIRS, encoding="utf-8")); qdoc = json.load(io.open(CF2_QUEUE, encoding="utf-8"))
    q = qdoc["queues"][cls]
    pend = doc["meta"].get("pending_replacements", {}).get(cls, 0)
    # records of this state authored but not yet read by the author fail the read at (1 - pass_rate) in expectation;
    # the extension is sized on pending + those expected failures so the next read can close them
    pnf = CF2_DIR / "cf_pn_texts_cf2.json"
    pn = json.load(io.open(pnf, encoding="utf-8"))["records"] if pnf.exists() else []
    prf = CF2_DIR / "pn_read_verdicts.json"
    read_ids = {v["pair_id"] for v in json.load(io.open(prf, encoding="utf-8"))["verdicts"]} if prf.exists() else set()
    unread = [r for r in pn if r["state"] == cls and r["new_text"] and r["pair_id"] not in read_ids]
    pvf = CF2_DIR / "pn_reread_verdicts.json"
    pv = json.load(io.open(pvf, encoding="utf-8"))["verdicts"] if pvf.exists() else []
    awaiting_reread = [v for v in pv if v["state"] == cls and v.get("pass") is None]
    n_unread = len(unread) + len(awaiting_reread)
    exp_fail = n_unread * (1 - pass_rate)
    shortfall = pend + exp_fail
    assert shortfall > 0, f"STOP: {cls} has nothing pending and nothing awaiting a read"
    n_ext = len([e for e in qdoc["meta"].get("extensions", []) if e["state"] == cls]) + 1
    out = CF2_READ_EXT if n_ext == 1 else ROOT / "reviews" / f"CF2_ADJUDICATION_READ_EXT{n_ext}.md"
    read = [x for x in q if x["adjudication"]["status"] != "UNREAD"]
    first_unread = max(x["position"] for x in read) + 1
    assert all(x["adjudication"]["status"] == "UNREAD" for x in q if x["position"] >= first_unread), "STOP: a read row lies past the first unread position"
    n_elig = sum(1 for x in read if x["adjudication"]["status"] == "ELIGIBLE")
    n_verdict = sum(1 for x in read if x["adjudication"]["status"] in ("ELIGIBLE", "INELIGIBLE"))
    elig_rate = n_elig / n_verdict
    expected_needed = shortfall / (elig_rate * pass_rate)
    pairs = doc["pairs"]
    cap = collections.Counter(p["persona"] for p in pairs if p["state"] == cls)
    used_names = {(p["persona"], p["slot_scrubbed"]): p["pair_id"] for p in pairs}
    reg = (ROOT / "registrations" / "ADDENDUM_R82.md").read_text(encoding="utf-8").split("\n")
    i0 = next(i for i, ln in enumerate(reg) if ln.startswith("### §3.1 — Eligibility criteria"))
    i1 = next(i for i in range(i0 + 1, len(reg)) if reg[i].startswith("This is the failure mode"))
    criteria = "\n".join(reg[i0 + 1:i1]).strip()
    at_cap = sorted(p for p, c in cap.items() if c >= PER_PERSONA)
    L = [f"# {out.stem} — the {cls} queue continued from position {first_unread}, in reading order", "",
         f"Emitted by `select_pairs.py --cf2 --extend {cls} --n {n_read}` (ADDENDUM_CF2.md, frozen f016f03; §14 D-CF2-1, D-CF2-2, §15 D-CF2-3); extension {n_ext} of this state's queue. "
         f"The same seed-{SEED} round-robin walk as `reviews/CF2_ADJUDICATION_READ.md`, continued: positions 1–{first_unread - 1} are read "
         f"({n_elig} ELIGIBLE, {n_verdict - n_elig} INELIGIBLE, {len(read) - n_verdict} not adjudicated); every ELIGIBLE row among them is "
         f"accepted, excluded under D-CF2-2, or passed over at the cap. **{pend} {cls.lower()} pair(s) pending** and **{n_unread} records awaiting "
         f"the author's read** (expected failures {exp_fail:.1f} at pass {pass_rate}) as of 13 Sep 2026. "
         "Read in order; a candidate is accepted in walk order on an ELIGIBLE verdict under the cap and the one-pair-per-(persona, scrubbed name) "
         "rule, then its question is drafted, its record authored and read like the others. Stop when the pending count is filled. "
         "A candidate marked `name rank 2+` shares its scrubbed name with an earlier candidate of the same persona and class: read it only if "
         "that one was INELIGIBLE. A candidate marked SKIPPED is not readable under the current draw (its persona is at the cap, or its "
         "scrubbed name is already an accepted pair's) and is listed only so the walk is auditable.", "",
         "## The criteria, verbatim from ADDENDUM_R82.md §3.1 (frozen; ADDENDUM_CF2.md §3.1 carries them unchanged)", "",
         criteria, "",
         "## Sizing, from the observed rates on this state's read", "",
         "| State | Pending | Records awaiting the author's read | Expected read failures at 1 − pass | Shortfall basis | Eligibility observed (ELIGIBLE / verdict reads, positions 1–{}) | Pass assumed | Expected reads needed | Printed |".format(first_unread - 1),
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
         f"| {cls} | {pend} | {n_unread} ({len(unread)} first reads + {len(awaiting_reread)} re-reads) | {exp_fail:.1f} | {shortfall:.1f} | {n_elig} / {n_verdict} = **{elig_rate:.3f}** | {pass_rate} | {shortfall:.1f} / ({elig_rate:.3f} × {pass_rate}) = **{expected_needed:.1f}** | **{n_read}** readable candidates |", "",
         f"Personas at the cap ({PER_PERSONA}) in {cls}, whose candidates are SKIPPED: {', '.join(at_cap) if at_cap else 'none'}. "
         f"Accepted {cls.lower()} pairs per persona now: " + ", ".join(f"{p} {c}" for p, c in sorted(cap.items())) + ". "
         "A persona reaching the cap through acceptances from this file makes its later candidates unreadable in turn.", ""]
    printed, skipped, rows_out = 0, 0, []
    for x in q:
        if x["position"] < first_unread:
            continue
        if printed >= n_read:
            break
        skip = None
        if cap[x["persona"]] >= PER_PERSONA:
            skip = f"SKIPPED — {x['persona']} holds {PER_PERSONA} accepted {cls.lower()} pairs (cap)"
        elif (x["persona"], x["slot_scrubbed"]) in used_names:
            skip = f"SKIPPED — scrubbed name `{x['slot_scrubbed']}` is already accepted as `{used_names[(x['persona'], x['slot_scrubbed'])]}`"
        head = (f"### {cls} {x['position']:04d} — {x['persona']} `{x['entry_id']}` — `{x['slot_key'][1]}` [{x['category']}]"
                + (f" — overlap {x['overlap_tag']}" if x["overlap_tag"] else "")
                + (f" — name rank {x['name_rank']}" if x["name_rank"] > 1 else ""))
        if skip:
            L += [head + " — " + skip, ""]; skipped += 1
            rows_out.append({"position": x["position"], "persona": x["persona"], "entry_id": x["entry_id"], "readable": False, "skip": skip})
            continue
        L.append(head)
        if x["event_time"]:
            L.append(f"event_time {str(x['event_time'])[:10]} · session {x['source_session']}")
        L += [f"> {x['text']}", "Verdict: "]
        printed += 1
        rows_out.append({"position": x["position"], "persona": x["persona"], "entry_id": x["entry_id"], "readable": True})
        if printed == math.ceil(expected_needed):
            L += ["", f"— expected reads at the observed rates reached here ({math.ceil(expected_needed)}); continue only if the pending count is not yet filled —"]
        L.append("")
    last = rows_out[-1]["position"] if rows_out else first_unread - 1
    L += [f"— end of the extension: {printed} readable candidates (positions {first_unread}–{last}), {skipped} skipped —", ""]
    out.write_text("\n".join(L), encoding="utf-8", newline="\n")
    ext = {"date": VERDICT_DATE_EXT, "state": cls, "from_position": first_unread, "to_position": last, "readable": printed, "skipped": skipped,
           "pending": pend, "records_awaiting_read": n_unread, "expected_read_failures": round(exp_fail, 2), "shortfall_basis": round(shortfall, 2), "eligibility_observed": round(elig_rate, 4), "eligible": n_elig, "verdict_reads": n_verdict,
           "pass_rate_assumed": pass_rate, "expected_reads_needed": round(expected_needed, 2), "rows": rows_out,
           "read_document": str(out.relative_to(ROOT)).replace("\\", "/")}
    qdoc["meta"].setdefault("extensions", []).append(ext)
    jdump(qdoc, CF2_QUEUE)
    print(f"{cls}: {printed} readable candidates printed from position {first_unread} to {last} ({skipped} skipped: cap/name); "
          f"pending {pend} + expected read failures {exp_fail:.1f} of {n_unread} unread = shortfall {shortfall:.1f}; "
          f"eligibility {n_elig}/{n_verdict} = {elig_rate:.3f}; expected reads {expected_needed:.1f} at pass {pass_rate}")
    print(f"  -> {out}")
    return 0


# ---------------------------------------------------------------------------------------------
# Extension merge: the author's verdicts on an extension read (reviews/CF2_ADJUDICATION_READ_EXT*.md)
# into the queue, then adjudication_cf2.json regenerated from the queue. Rows are addressed by the
# printed position ("num") and checked against the extension's recorded readable rows; the eight
# SKIPPED rows (cap or name at extension time) are recorded as NOT-ADJUDICATED with that reason;
# the state's stop moves to the last extension position and later rows stay UNREAD.
#   --cf2 --merge-ext <verdicts.json> [--key adjudication_ext]
# ---------------------------------------------------------------------------------------------
def cf2_merge_ext(spec_path, key="adjudication_ext", date=VERDICT_DATE_EXT):
    qdoc = json.load(io.open(CF2_QUEUE, encoding="utf-8")); vdoc = json.load(io.open(spec_path, encoding="utf-8"))
    rows = vdoc[key]
    cls = {r["state"] for r in rows}; assert len(cls) == 1, cls
    cls = cls.pop(); q = qdoc["queues"][cls]; byp = {x["position"]: x for x in q}
    exts = [e for e in qdoc["meta"].get("extensions", []) if e["state"] == cls and not e.get("merged")]
    assert len(exts) == 1, "STOP: exactly one unmerged extension expected for this state"
    ext = exts[0]
    readable = {r["position"] for r in ext["rows"] if r["readable"]}; skipped = {r["position"]: r["skip"] for r in ext["rows"] if not r["readable"]}
    got = {int(r["num"]) for r in rows}
    assert got == readable, f"STOP: verdict positions differ from the extension's readable rows: missing {sorted(readable - got)[:5]}, extra {sorted(got - readable)[:5]}"
    first_elig_name = {}
    for x in q:
        if x["adjudication"]["status"] == "ELIGIBLE":
            first_elig_name.setdefault((x["persona"], x["slot_scrubbed"]), x["position"])
    c = collections.Counter()
    for r in sorted(rows, key=lambda r: int(r["num"])):
        x = byp[int(r["num"])]; st = r["verdict"]
        assert x["adjudication"]["status"] == "UNREAD", (cls, x["position"], "already read")
        key_ = (x["persona"], x["slot_scrubbed"])
        if st in ("ELIGIBLE", "INELIGIBLE"):
            adj = {"status": st, "verdict": st, "source": f"author {date}", "reason": ""}
        elif st == "SKIP-RANK":
            assert x["name_rank"] > 1, (cls, x["position"], "SKIP-RANK at rank 1")
            p0 = min((p for (pp, ss), p in first_elig_name.items() if (pp, ss) == key_ and p < x["position"]), default=None)
            assert p0 is not None, (cls, x["position"], "SKIP-RANK without an earlier ELIGIBLE same-name candidate")
            adj = {"status": "NOT-ADJUDICATED", "verdict": None, "source": None,
                   "reason": f"not read: an earlier same-name candidate for this persona was ELIGIBLE (position {p0})"}
        else:
            raise SystemExit(f"STOP: unknown walk status {st!r} at {cls} {x['position']}")
        if adj["status"] == "ELIGIBLE" and key_ not in first_elig_name:
            first_elig_name[key_] = x["position"]
        x["adjudication"] = {**adj, "walk_status": st, "extension": ext["read_document"]}
        c[st] += 1
    for pos, why in skipped.items():
        x = byp[pos]; assert x["adjudication"]["status"] == "UNREAD"
        tag = "SKIP-CAP" if "(cap)" in why else "SKIP-NAME"
        x["adjudication"] = {"status": "NOT-ADJUDICATED", "verdict": None, "source": None, "walk_status": tag,
                             "reason": f"not read at the extension: {why}", "extension": ext["read_document"]}
        c[tag] += 1
    stop = ext["to_position"]
    for x in q:
        if x["adjudication"]["status"] == "UNREAD":
            assert x["position"] > stop, (cls, x["position"], "UNREAD before the new stop")
            x["adjudication"]["reason"] = f"past the state's stop (position {stop})"
    ext["merged"] = {"source_file": str(pathlib.Path(spec_path).resolve().relative_to(ROOT)).replace("\\", "/"),
                     "source_sha256": _sha256_file(pathlib.Path(spec_path)), "date": date, "key": key, "walk_status_counts": dict(c)}
    qdoc["meta"]["adjudication"]["stops"][cls] = stop
    # regenerate the state's section of adjudication_cf2.json from the queue
    adj_doc = json.load(io.open(CF2_ADJ, encoding="utf-8"))
    cc = collections.Counter(x["adjudication"]["walk_status"] for x in q)
    verdict_rows = [{"n": x["position"], "persona": x["persona"], "entry_id": x["entry_id"], "slot": x["slot_key"][1],
                     "slot_scrubbed": x["slot_scrubbed"], "category": x["category"], "name_rank": x["name_rank"], "overlap_tag": x["overlap_tag"],
                     "walk_status": x["adjudication"]["walk_status"], "verdict": x["adjudication"]["verdict"], "status": x["adjudication"]["status"],
                     "source": x["adjudication"]["source"], "reason": x["adjudication"]["reason"]} for x in q]
    reads = cc["ELIGIBLE"] + cc["INELIGIBLE"]
    counts = {"rows": len(q), "walk_status_counts": dict(cc), "stop_position": stop, "verdict_reads": reads,
              "reads_including_rank_skips": reads + cc["SKIP-RANK"], "eligible_new": cc["ELIGIBLE"], "eligible_reused": cc["REUSED"],
              "eligible_total": cc["ELIGIBLE"] + cc["REUSED"], "eligibility_rate_new_over_verdict_reads": round(cc["ELIGIBLE"] / reads, 4) if reads else None}
    qdoc["meta"]["adjudication"]["counts"][cls] = counts
    adj_doc[cls] = {**counts, "verdicts": verdict_rows}
    adj_doc["meta"].setdefault("extension_sources", []).append({**ext["merged"], "state": cls, "positions": [ext["from_position"], stop],
                                                                "read_document": ext["read_document"], "author_notes": vdoc.get("notes", [])})
    adj_doc["meta"]["walk_status_values"]["SKIP-CAP"] = "not read at an extension: the persona held the cap in the state; recorded as not adjudicated"
    adj_doc["meta"]["walk_status_values"]["SKIP-NAME"] = "not read at an extension: the scrubbed name was already an accepted pair's; recorded as not adjudicated"
    adj_doc["meta"]["stops"][cls] = stop
    jdump(qdoc, CF2_QUEUE); jdump(adj_doc, CF2_ADJ)
    print(f"merged {len(rows)} extension verdicts for {cls} (positions {ext['from_position']}-{stop}; sha256 {ext['merged']['source_sha256'][:12]}...): {dict(c)}")
    print(f"  {cls} now: {dict(cc)}  stop {stop}  verdict reads {reads}  eligible {counts['eligible_total']}  rate {counts['eligibility_rate_new_over_verdict_reads']}")
    print(f"  -> {CF2_QUEUE}\n  -> {CF2_ADJ}")
    return 0


# ---------------------------------------------------------------------------------------------
# D-CF2-4 (ruling of 2026-09-13; ADDENDUM_CF2 section 16): the supersession queue is not extended
# again. The quota is fixed at what the walk over positions 229-272 reached, and a record that fails
# its read from here on is excluded under D-CF2-4 with NO replacement: the quota drops by one and
# the composition is (N_sup)/30/30. The effective quota lives in cf_pairs_cf2.json meta.quota;
# CF2_QUOTA above is the section-14 figure the walk started from.
#   --cf2 --record-d4                 fix meta.quota at the current accepted counts (pending must be empty)
#   --cf2 --exclude-d4 <spec.json>    spec: [{"pair_id", "reason", "report"}]; no refill; quota -= 1 each
# ---------------------------------------------------------------------------------------------
def effective_quota(doc):
    return dict(doc["meta"].get("quota", CF2_QUOTA))


def cf2_record_d4():
    doc = json.load(io.open(CF2_PAIRS, encoding="utf-8"))
    by_state = collections.Counter(p["state"] for p in doc["pairs"])
    pend = doc["meta"].get("pending_replacements", {})
    assert not any(pend.values()), f"STOP: pending replacements remain {pend}; D-CF2-4 fixes the quota only once the walk has stopped"
    residual = {c: CF2_QUOTA[c] - by_state[c] for c in CF2_QUOTA}
    doc["meta"]["quota"] = dict(by_state)
    doc["meta"]["quota_history"] = doc["meta"].get("quota_history", []) + [
        {"date": VERDICT_DATE_EXT, "deviation": "D-CF2-4", "quota": dict(by_state), "section14_quota": dict(CF2_QUOTA),
         "residual_shortfall_at_recording": residual, "no_further_extension": True,
         "rule": "a record failing its read from here on is excluded under D-CF2-4, no replacement; the state's quota drops by one"}]
    doc["meta"]["no_further_extension"] = True
    jdump(doc, CF2_PAIRS)
    print(f"D-CF2-4 recorded: quota fixed at {dict(by_state)} (section 14 {dict(CF2_QUOTA)}; residual {residual}); no further extension")
    return 0


def cf2_exclude_d4(spec_path):
    spec = json.load(io.open(spec_path, encoding="utf-8"))
    doc = json.load(io.open(CF2_PAIRS, encoding="utf-8"))
    assert "quota" in doc["meta"], "STOP: run --record-d4 first"
    qfile = CF2_DIR / "cf_questions_cf2.json"; pnfile = CF2_DIR / "cf_pn_texts_cf2.json"
    qd = json.load(io.open(qfile, encoding="utf-8")) if qfile.exists() else None
    pn = json.load(io.open(pnfile, encoding="utf-8")) if pnfile.exists() else None
    by_id = {p["pair_id"]: p for p in doc["pairs"]}
    for s in spec:
        ex = by_id.get(s["pair_id"])
        if ex is None:
            raise SystemExit(f"STOP: {s['pair_id']} is not an accepted pair")
        doc["pairs"].remove(ex)
        ex["excluded"] = {"reason": s["reason"], "deviation": "D-CF2-4", "date": s.get("date", VERDICT_DATE_EXT), "report": s.get("report"),
                          "eligibility_verdict_stands": ex["adjudication"] == "ELIGIBLE", "no_replacement": True}
        doc["meta"].setdefault("excluded", []).append(ex)
        doc["meta"]["quota"][ex["state"]] -= 1
        if qd is not None:
            rows = [r for r in qd["questions"] if r["pair_id"] == s["pair_id"]]
            qd["questions"] = [r for r in qd["questions"] if r["pair_id"] != s["pair_id"]]
            qd["meta"].setdefault("excluded_questions", []).extend({**r, "excluded_under": "D-CF2-4", "reason": s["reason"]} for r in rows)
        if pn is not None:
            recs = [r for r in pn["records"] if r["pair_id"] == s["pair_id"]]
            pn["records"] = [r for r in pn["records"] if r["pair_id"] != s["pair_id"]]
            pn["meta"].setdefault("excluded_records", []).extend({**r, "excluded_under": "D-CF2-4", "reason": s["reason"]} for r in recs)
    by_state = collections.Counter(p["state"] for p in doc["pairs"])
    for cls in CF2_QUOTA:
        assert by_state[cls] == doc["meta"]["quota"][cls], (cls, by_state[cls], doc["meta"]["quota"])
    doc["meta"]["accepted_by_state"] = dict(by_state)
    doc["meta"]["accepted_per_persona"] = {pp: dict(collections.Counter(q["state"] for q in doc["pairs"] if q["persona"] == pp))
                                           for pp in sorted({q["persona"] for q in doc["pairs"]})}
    doc["meta"]["quota_history"].append({"date": VERDICT_DATE_EXT, "deviation": "D-CF2-4", "quota": dict(doc["meta"]["quota"]),
                                         "excluded_no_replacement": [s["pair_id"] for s in spec]})
    jdump(doc, CF2_PAIRS)
    if qd is not None:
        import hashlib  # noqa: PLC0415
        qd["questions"].sort(key=lambda r: r["pair_id"]); qd["meta"]["n"] = len(qd["questions"])
        qd["meta"]["questions_sha256"] = hashlib.sha256("\x1f".join(r["question"] for r in qd["questions"]).encode("utf-8")).hexdigest()
        jdump(qd, qfile)
    if pn is not None:
        pn["records"].sort(key=lambda r: r["pair_id"]); jdump(pn, pnfile)
    print(f"D-CF2-4: excluded {len(spec)} pair(s) with no replacement; quota now {doc['meta']['quota']}; accepted {dict(by_state)}")
    return 0


def main_cf2():
    if "--record-d4" in sys.argv:
        return cf2_record_d4()
    if "--exclude-d4" in sys.argv:
        return cf2_exclude_d4(sys.argv[sys.argv.index("--exclude-d4") + 1])
    if "--merge-ext" in sys.argv:
        a = sys.argv
        return cf2_merge_ext(a[a.index("--merge-ext") + 1], a[a.index("--key") + 1] if "--key" in a else "adjudication_ext")
    if "--extend" in sys.argv:
        a = sys.argv
        return cf2_extend(a[a.index("--extend") + 1], int(a[a.index("--n") + 1]), float(a[a.index("--pass") + 1]) if "--pass" in a else 0.75)
    if "--exclude-batch" in sys.argv:
        return cf2_exclude_batch(sys.argv[sys.argv.index("--exclude-batch") + 1])
    if "--refill" in sys.argv:
        return cf2_exclude_batch(None)
    if "--exclude" in sys.argv:
        a = sys.argv
        return cf2_exclude_and_replace(a[a.index("--exclude") + 1], a[a.index("--reason") + 1], a[a.index("--report") + 1])
    if "--merge" in sys.argv:
        return cf2_merge_verdicts()
    if "--accept" in sys.argv:
        return cf2_accept()
    rows, clocks, personas = cf2_candidates()
    census, order = cf2_census(rows)
    CF2_DIR.mkdir(parents=True, exist_ok=True)
    print("CF-2 census under the registered predicate (ADDENDUM_CF2 sections 2-3), beside CF2_SCOPE Phase 2")
    print(f"  stages: raw -> individuates -> not on v2 superseded list -> zero-overlap-or-readmitted (90, 84, 36) = CLEAN")
    for cls in CLASS_ORDER:
        c = census[cls]
        print(f"  {cls:12s} frozen predicate  cf2 {c['frozen_predicate_stages_cf2']}   scope {c['scope_stages']}")
        if c["o3_stages_cf2"]:
            print(f"  {'':12s} O3 (widened)      cf2 {c['o3_stages_cf2']}   scope raw {c['scope_o3'][0]} -> clean {c['scope_o3'][5]}")
        print(f"  {'':12s} admitted {c['admitted']} by tag {c['admitted_by_overlap_tag']}; verdicts {c['admitted_verdicts']}; "
              f"admissible (not INELIGIBLE) {c['admissible_not_ineligible']} over {c['personas']} personas, "
              f"{c['distinct_persona_scrubbed']} distinct (persona, scrubbed name)")
    print(f"  scarcity order (ascending admissible): {' > '.join(order)}")
    jdump({"no_api_calls": True, "seed": SEED, "quota": CF2_QUOTA, "per_persona": PER_PERSONA,
           "scarcity_order": list(order), "census": census}, CF2_CENSUS)
    print(f"  -> {CF2_CENSUS}")
    if "--queue" not in sys.argv:
        return 0
    queues, shuffled = cf2_walk(rows, order, personas)
    for cls in order:
        for n, x in enumerate(queues[cls], 1):
            x["position"] = n
    est = cf2_estimates(queues, census)
    keep = ("position", "persona", "entry_id", "slot_key", "slot_scrubbed", "category", "text", "event_time",
            "source_session", "created_at", "o3", "overlap_tag", "name_rank", "verdict", "verdict_reason")
    jdump({"meta": {"no_api_calls": True, "registration": "registrations/ADDENDUM_CF2.md (frozen f016f03)",
                    "seed": SEED, "quota": CF2_QUOTA, "per_persona": PER_PERSONA, "scarcity_order": list(order),
                    "persona_order_seed42": shuffled, "nothing_accepted": True,
                    "walk": {"EXPIRY": "persona order, exhaustive (section 3.1)",
                             "RETRACTION": "seed-42 round-robin, round r offers each persona's r-th admissible candidate",
                             "SUPERSESSION": "same"},
                    "ineligible_excluded": {cls: sum(1 for x in rows if x["cls"] == cls and x["admitted"] and x["verdict"] == "INELIGIBLE") for cls in CLASS_ORDER},
                    "estimates": est, "census": census},
           "queues": {cls: [{k: x[k] for k in keep} for x in queues[cls]] for cls in order}}, CF2_QUEUE)
    write_read_md(queues, order, est, shuffled)
    print("\nadjudication queue (nothing accepted):")
    for cls in order:
        e = est[cls]
        print(f"  {cls:12s} queue {len(queues[cls]):5d}   ELIGIBLE already {e['eligible_already']:3d}   unadjudicated {e['unadjudicated_in_queue']:5d}   "
              f"quota {e['quota']:3d}   estimated reads {e['estimated_reads']:4d}   ({e['rule']})")
    print(f"  -> {CF2_QUEUE}\n  -> {CF2_READ}")
    return 0


if __name__ == "__main__":
    if "--cf2" in sys.argv:
        raise SystemExit(main_cf2())
    main()
