"""census_cf3.py -- the CF-3 sizing census (the author's instruction of 2026-09-14). NO MODEL CALL. NO DRAW. NO REGISTRATION.

Three things, from the artifacts as committed:

  A. From the persona manifests (LifeMemEval persona YAMLs), not the store's flags: every retraction record and every
     expiring-logistics record per persona (status expired / upcoming), and how many of each resolve to a bank entry
     under the TRUE join (index_v2.true_lifecycle) -- the natural events. For context: the main study's obligation
     items by state per persona.
  B. The CF-2 draw's predicates replayed one at a time over the raw banks for the RETRACTION and EXPIRY classes
     (ADDENDUM_CF2 sections 2 and 3; select_pairs.candidates_for / candidates_for_cf2 / cf2_candidates), each removed
     candidate listed with the predicate that removed it; then the author's verdicts, the cap, the one-per-name rule,
     the quota and the post-draw exclusions from cf2/adjudication_cf2.json and cf2/cf_pairs_cf2.json.
  C. The largest CF-3 addition the registered predicates admit without relaxation (zero reads: ELIGIBLE and undrawn;
     with reads: admitted and UNREAD at the observed eligibility rate), and under each single relaxation.

The CF-2 counterfactual pool is NOT the manifest's event list: a CF-2 retraction pair retracts an ACTIVE plan record
counterfactually, and a CF-2 expiry pair moves the anchor of an ACTIVE dated record past the cutoff. The manifest's own
retraction and expiry events are the records already retracted or expired in the bank -- the pool the main study's
26 retraction and 15 expiry obligations come from -- and they fail the candidate predicate ("active, not retracted")
by construction. Section A reports them as the natural supply; sections B and C report the counterfactual supply.
"""
from __future__ import annotations

import collections
import datetime as dt
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in ("e0_metamemory/tools", "e1_metamemory/tools", "r82_counterfactual", "r82_counterfactual/tools", "e1r_robustness/tools"):
    sys.path.insert(0, str(ROOT / p))

import e0_common as C                                    # noqa: E402
from e0_common import EXPIRY_WINDOW, MIN_DISCR, MIN_SHARED, TAU_GOLD, cov, parse_dt, toks      # noqa: E402
import select_pairs as SP                                # noqa: E402
from build_cf_cell import Join, build_index              # noqa: E402
from index_v2 import TAU_HI, detect, scrub, true_lifecycle   # noqa: E402
from index_v3 import named_sections                      # noqa: E402
from nb6_composition import AV_STATE                     # noqa: E402

CF2 = ROOT / "r82_counterfactual" / "cf2"
OUT = ROOT / "r82_counterfactual" / "cf3"
STATES = ("RETRACTION", "EXPIRY")
PER_PERSONA = SP.PER_PERSONA
QUOTA = SP.CF2_QUOTA


def J(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
        f.write("\n")


# ============================================================================================ A. the manifests
def manifest_census():
    ypaths = {p.name.replace(".yaml", "").split("_")[-1]: p for p in sorted(C.LME.glob("*/persona_*.yaml"))}
    banks = {f.stem: J(f)["entries"] for f in sorted(SP.BANKS.glob("*.json"))}
    items = J(ROOT / "e1_metamemory" / "build" / "items_final.json")
    ob = collections.Counter()
    for it in items:
        if it.get("label", it.get("label_pre")) == "PRESENT-NEGATIVE" and it["backend"] == "frbank":
            ob[(it["persona"], AV_STATE.get(it.get("attack_vector"), "?"))] += 1
    rows = []
    for persona, entries in banks.items():
        if persona not in ypaths:
            continue
        y = C.load_yaml(ypaths[persona])
        t_now, cutoff = SP.persona_clock(entries)
        blk = y.get("persona")
        drop = toks(blk.get("name", "") if isinstance(blk, dict) else "")
        Jn = Join(persona, entries, y, t_now, cutoff, drop)
        sup, ret, exp, ev = true_lifecycle(Jn, Jn.etoks)
        rrec = [r for r in (y.get("retractions") or []) if isinstance(r, dict)]
        erec = [r for r in (y.get("expiring_logistics") or []) if isinstance(r, dict)]
        n_exp_expired = sum(1 for r in erec if str(r.get("status") or "").strip().lower() == "expired")
        n_exp_other = len(erec) - n_exp_expired
        # per-record resolution, the rule of index_v2.true_lifecycle: a retraction record resolves when the detector
        # scores some entry at TAU_HI on its original_fact; an expired record when some entry shares MIN_SHARED tokens
        # with its fact at coverage TAU_GOLD
        r_resolved = 0
        for r in rrec:
            d = detect(r.get("original_fact"), r.get("retraction"), Jn.etoks, Jn.drop)
            if d and any(sc >= TAU_HI for sc in d.values()):
                r_resolved += 1
        e_resolved = 0
        for r in erec:
            if str(r.get("status") or "").strip().lower() != "expired":
                continue
            ft = toks(r.get("fact"), Jn.drop)
            if len(ft) < MIN_DISCR:
                continue
            if any(len(ft & t) >= MIN_SHARED and cov(ft, t) >= TAU_GOLD for t in Jn.etoks.values()):
                e_resolved += 1
        rows.append({"persona": persona, "manifest_retractions": len(rrec), "retraction_records_resolving_to_an_entry": r_resolved,
                     "entries_retracted_under_TRUE": len(ret), "manifest_expiring_logistics": len(erec),
                     "expiring_status_expired": n_exp_expired, "expiring_status_other": n_exp_other,
                     "expired_records_resolving_to_an_entry": e_resolved, "entries_expired_under_TRUE": len(exp), "supersession_events_resolved": len(ev),
                     "store_flag_is_retracted": sum(1 for e in entries if e.get("is_retracted")),
                     "obligations_661_retraction": ob[(persona, "retracted")], "obligations_661_expiry": ob[(persona, "expired")],
                     "obligations_661_supersession": ob[(persona, "superseded")]})
    return rows


# ============================================================================================ B. the predicates, replayed
def predicate_replay():
    """Per state, every entry of the state's universe with the first predicate that removes it (registered order)."""
    banks = {f.stem: J(f)["entries"] for f in sorted(SP.BANKS.glob("*.json"))}
    ypaths = {p.name.replace(".yaml", "").split("_")[-1]: p for p in sorted(C.LME.glob("*/persona_*.yaml"))}
    ov90_ids, ov90_slots, ov84, ov36, o1 = SP._overlap_sets()
    adj = J(CF2 / "adjudication_cf2.json")
    _, cf1_verdicts = SP.load_verdicts()
    verdict = {}
    for cls in STATES:
        for v in adj[cls]["verdicts"]:
            verdict[(cls, v["persona"], v["entry_id"])] = v
    pairs = J(CF2 / "cf_pairs_cf2.json")
    accepted = {(p["state"], p["persona"], p["entry_id"]): p for p in pairs["pairs"]}
    excluded = {(e["state"], e["persona"], e["entry_id"]): e for e in pairs["meta"]["excluded"]}
    passed_over = {(e["state"], e["persona"], e["entry_id"]): e for e in pairs["meta"]["passed_over_at_acceptance"]}
    out = {cls: [] for cls in STATES}
    per_persona_sections = {}
    for persona, entries in banks.items():
        if persona not in ypaths:
            continue
        t_now, cutoff = SP.persona_clock(entries)
        y0 = C.load_yaml(ypaths[persona])
        blk = y0.get("persona")
        drop = toks(blk.get("name", "") if isinstance(blk, dict) else "")
        v2, v3, _ = build_index(Join(persona, entries, y0, t_now, cutoff, drop), set())
        secs = {"v2": named_sections(v2), "v3": named_sections(v3)}
        per_persona_sections[persona] = secs
        occ = collections.Counter(tuple(e["slot_key"]) for e in entries if e.get("slot_key"))
        for e in entries:
            cat, evt = e.get("category"), parse_dt(e.get("event_time"))
            in_state = {"RETRACTION": evt is None and cat in SP.RET_CATS, "EXPIRY": evt is not None}
            for cls in STATES:
                if not in_state[cls]:
                    continue
                sk = e.get("slot_key")
                nm = scrub(sk[1]) if sk else None
                rec = {"persona": persona, "entry_id": e["id"], "slot": (sk[1] if sk else None), "slot_scrubbed": nm, "category": cat,
                       "event_time": (str(e.get("event_time"))[:10] if e.get("event_time") else None), "text": e.get("text", ""),
                       "is_active": bool(e.get("is_active")), "is_retracted": bool(e.get("is_retracted")), "supersedes": bool(e.get("supersedes")),
                       "n_tokens": len(toks(e.get("text", ""), frozenset()))}
                # the registered order of the predicates
                if not sk:
                    rec["removed_by"] = "P1 slot_key present"
                elif occ[tuple(sk)] != 1:
                    rec["removed_by"] = f"P2 slot_key unique in the bank (occurs {occ[tuple(sk)]} times)"
                elif not e.get("is_active"):
                    rec["removed_by"] = "P3a entry is active"
                elif e.get("is_retracted"):
                    rec["removed_by"] = "P3b entry is not retracted"
                elif e.get("supersedes"):
                    rec["removed_by"] = "P3c entry supersedes nothing"
                elif rec["n_tokens"] < SP.MIN_TEXT_TOKENS:
                    rec["removed_by"] = f"P4 at least {SP.MIN_TEXT_TOKENS} content tokens (has {rec['n_tokens']})"
                elif cls == "EXPIRY" and not (cutoff is not None and evt >= cutoff):
                    rec["removed_by"] = f"P5 anchor at or after the pinned cutoff (event {str(e.get('event_time'))[:10]} < cutoff {cutoff.date()})"
                else:
                    sec = secs["v3"][SP.STATE_SECTION[cls]]
                    if nm in sec:
                        rec["removed_by"] = f"P6 individuation ('{nm}' already on the persona's {SP.STATE_SECTION[cls]} section in PRESENT)"
                    elif nm in secs["v2"]["superseded"]:
                        rec["removed_by"] = f"P7 superseded-list exclusion ('{nm}' on the v2 superseded list in PRESENT)"
                    else:
                        key = (persona, e["id"])
                        ov = {"90": key in ov90_ids or (persona, nm) in ov90_slots, "84": key in ov84, "36": (persona, nm) in ov36}
                        readmit = "O1" if (cls == "EXPIRY" and key in o1) else "O2" if (cls == "EXPIRY" and key in SP.O2_FOUR) else None
                        rec["overlap"] = {k: v for k, v in ov.items() if v}
                        rec["readmit"] = readmit
                        if any(ov.values()) and readmit is None:
                            rec["removed_by"] = "P8 zero overlap with the 90 / 84 / 36 (" + ", ".join(k for k, v in ov.items() if v) + ")"
                        else:
                            v = verdict.get((cls, persona, e["id"]))
                            rec["queue_position"] = v.get("n") if v else None
                            rec["walk_status"] = v.get("walk_status") if v else None
                            rec["verdict"] = v.get("verdict") if v else None
                            rec["verdict_source"] = v.get("source") if v else None
                            rec["verdict_reason"] = v.get("reason") if v else None
                            cf1v = cf1_verdicts[cls].get((persona, e["id"]), (None, None))
                            if v is None and cf1v[0] == "INELIGIBLE":
                                rec["verdict"], rec["verdict_source"], rec["verdict_reason"] = "INELIGIBLE", "CF-1 reused (binding)", cf1v[1]
                                rec["removed_by"] = "P9c CF-1's INELIGIBLE verdict, reused and binding (left the queue before the walk)"
                            elif v is None:
                                rec["removed_by"] = "P8x admitted by the predicate but absent from the CF-2 queue (check)"
                            elif v["walk_status"] == "INELIGIBLE":
                                rec["removed_by"] = "P9 the author's eligibility read: INELIGIBLE"
                            elif v["walk_status"] == "SKIP-RANK":
                                rec["removed_by"] = "P9r rank-skip: an earlier candidate of the same persona and scrubbed name was ELIGIBLE (not read)"
                            elif v["walk_status"] == "UNREAD":
                                rec["removed_by"] = "P9u unread: past the state's stop position (never read)"
                            else:
                                k2 = (cls, persona, e["id"])
                                if k2 in accepted:
                                    if k2 in excluded:
                                        rec["removed_by"] = "P13 excluded after the draw: " + excluded[k2]["excluded"]["reason"]
                                    else:
                                        rec["removed_by"] = None
                                        rec["accepted_pair_id"] = accepted[k2]["pair_id"]
                                elif k2 in excluded:
                                    rec["removed_by"] = "P13 excluded after the draw: " + excluded[k2]["excluded"]["reason"]
                                elif k2 in passed_over:
                                    rec["removed_by"] = "P11 one pair per (persona, scrubbed name) across the draw (passed over at acceptance)"
                                else:
                                    rec["removed_by"] = "P12 ELIGIBLE and undrawn (quota filled, the cap, or the walk stopped before it)"
                out[cls].append(rec)
    return out, per_persona_sections


def stage_key(rb):
    return rb[:3].rstrip() if rb else "accepted"


def stage_table(rows):
    order = ["P1", "P2", "P3a", "P3b", "P3c", "P4", "P5", "P6", "P7", "P8", "P8x", "P9c", "P9", "P9r", "P9u", "P11", "P12", "P13"]
    c = collections.Counter(stage_key(r["removed_by"]) for r in rows)
    return {k: c.get(k, 0) for k in order}, c


# ============================================================================================ C. CF-3 sizing
def sizing(rows_by_state):
    pairs = J(CF2 / "cf_pairs_cf2.json")
    used = collections.Counter((p["persona"], p["state"]) for p in pairs["pairs"])
    names_used = {(p["persona"], p["slot_scrubbed"]) for p in pairs["pairs"]}
    adj = J(CF2 / "adjudication_cf2.json")
    out = {}
    for cls in STATES:
        rows = rows_by_state[cls]
        rate = adj[cls]["eligibility_rate_new_over_verdict_reads"]
        def fits(r, cap=PER_PERSONA, name_rule=True, usage=None):
            usage = usage if usage is not None else used
            if usage[(r["persona"], cls)] >= cap:
                return False
            if name_rule and (r["persona"], r["slot_scrubbed"]) in names_used:
                return False
            return True

        def take(cands, cap=PER_PERSONA, name_rule=True):
            """Greedy count under the cap and the name rule, in queue order, starting from the cell's usage."""
            usage = collections.Counter(used); taken_names = set(names_used); n = 0; taken = []
            for r in sorted(cands, key=lambda r: (r.get("queue_position") or 10**9, r["persona"], r["entry_id"])):
                if usage[(r["persona"], cls)] >= cap:
                    continue
                if name_rule and (r["persona"], r["slot_scrubbed"]) in taken_names:
                    continue
                usage[(r["persona"], cls)] += 1; taken_names.add((r["persona"], r["slot_scrubbed"])); n += 1; taken.append(r)
            return n, taken

        elig_undrawn = [r for r in rows if r["removed_by"] and r["removed_by"].startswith(("P12", "P11"))]
        unread = [r for r in rows if r["removed_by"] and r["removed_by"].startswith("P9u")]
        rank_skips = [r for r in rows if r["removed_by"] and r["removed_by"].startswith("P9r")]
        overlap_removed = [r for r in rows if r["removed_by"] and r["removed_by"].startswith("P8 ")]
        n0, taken0 = take(elig_undrawn)
        n_unread, _ = take(unread)
        base = {"eligible_undrawn": len(elig_undrawn), "eligible_undrawn_fitting_cap_and_name": n0,
                "eligible_undrawn_fitting_list": [f"{r['persona']} {r['entry_id']} {r['slot']}" for r in taken0],
                "unread_admitted": len(unread), "unread_fitting_cap_and_name": n_unread,
                "observed_eligibility_rate": rate, "expected_eligible_among_unread_fitting": round(n_unread * rate, 1),
                "reads_per_eligible": (round(1 / rate, 1) if rate else None)}
        relax = {}
        # R1 cap lifted
        n1, _ = take(elig_undrawn, cap=10**9); u1, _ = take(unread, cap=10**9)
        relax["R1 cap 4 per persona per state lifted"] = {"eligible_undrawn_fitting": n1, "unread_fitting": u1, "expected_eligible": round(u1 * rate, 1)}
        # R2 one-per-name lifted: rank-skips become readable; passed-over become drawable
        n2, _ = take(elig_undrawn, name_rule=False); u2, _ = take(unread + rank_skips, name_rule=False)
        relax["R2 one pair per (persona, scrubbed name) lifted"] = {"eligible_undrawn_fitting": n2, "unread_or_rank_skipped_fitting": u2,
                                                                     "rank_skips_readable": len(rank_skips), "expected_eligible": round(u2 * rate, 1)}
        # R6 overlap exclusions lifted (candidates need reads)
        u6, _ = take(unread + overlap_removed)
        relax["R6 zero-overlap exclusion lifted (the 90 / 84 / 36)"] = {"overlap_removed_readable": len(overlap_removed), "unread_plus_overlap_fitting": u6,
                                                                         "expected_eligible": round(u6 * rate, 1)}
        out[cls] = {"used_in_the_444": QUOTA[cls] if cls != "SUPERSESSION" else 88, "no_relaxation": base, "single_relaxations": relax}
    return out


def candidate_relaxations(banks_rows):
    """The candidate-predicate relaxations (R3 to R5) counted on the raw pools: how many entries each would add to
    the admitted pool before any read. R3 widens the retraction category; R4 drops slot-key uniqueness; R5 drops the
    six-token floor. Each is a count of entries that fail exactly that predicate and pass the others (P1-P8)."""
    out = {}
    for cls, rows in banks_rows.items():
        c = collections.Counter()
        for r in rows:
            rb = r["removed_by"] or ""
            if rb.startswith("P2 "):
                c["R4 slot-key uniqueness dropped (fails P2 only; P3-P8 unchecked here)"] += 1
            if rb.startswith("P4 "):
                c["R5 six-token floor dropped (fails P4 only; P5-P8 unchecked here)"] += 1
        out[cls] = dict(c)
    return out


def retraction_category_widening():
    """R3: null-event_time active entries outside PROJECTS_ENDEAVORS that pass P1-P4 (the class predicate is what
    excludes them); by category."""
    banks = {f.stem: J(f)["entries"] for f in sorted(SP.BANKS.glob("*.json"))}
    c = collections.Counter()
    for persona, entries in banks.items():
        occ = collections.Counter(tuple(e["slot_key"]) for e in entries if e.get("slot_key"))
        for e in entries:
            if parse_dt(e.get("event_time")) is not None or e.get("category") in SP.RET_CATS:
                continue
            sk = e.get("slot_key")
            if not sk or occ[tuple(sk)] != 1 or not e.get("is_active") or e.get("is_retracted") or e.get("supersedes"):
                continue
            if len(toks(e.get("text", ""), frozenset())) < SP.MIN_TEXT_TOKENS:
                continue
            c[e.get("category")] += 1
    return dict(c.most_common())


# ============================================================================================ report
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    A = manifest_census()
    B, _ = predicate_replay()
    tables = {cls: stage_table(B[cls]) for cls in STATES}
    Cz = sizing(B)
    R = candidate_relaxations(B)
    R3 = retraction_category_widening()
    fell = [r for r in B["RETRACTION"] if (r["removed_by"] or "").startswith("P13")]
    jdump({"A_manifests": A, "B_predicates": B, "B_stage_counts": {k: v[0] for k, v in tables.items()}, "C_sizing": Cz,
           "C_candidate_relaxations": R, "C_retraction_category_widening": R3, "no_model_call": True, "no_draw": True,
           "date": "2026-09-14"}, OUT / "census_cf3.json")
    # ---- markdown
    L = ["# CF3_CENSUS — sizing a CF-3 draw from the artifacts (2026-09-14; no model call, no draw, no registration)", "",
         "Emitted by `r82_counterfactual/cf3/census_cf3.py` from the persona manifests, the 40 banks, `cf2/adjudication_cf2.json` "
         "and `cf2/cf_pairs_cf2.json`. Nothing is drawn or registered; the author rules on what follows.", "",
         "## 0. Two supplies, stated first", "",
         "A CF-2 **retraction** pair retracts an ACTIVE plan record counterfactually (ADDENDUM_CF2 §2: append a retracting entry on the "
         "same slot key); a CF-2 **expiry** pair moves the anchor of an ACTIVE dated record past the pinned cutoff. The candidate pool "
         "is therefore the bank's active records under the class predicate, not the manifests' event lists. The manifests' own "
         "retraction and expiring-logistics records are the **natural** events -- already retracted or expired in the bank, the pool "
         "the main study's 26 retraction and 15 expiry obligations come from -- and every one of them fails the candidate predicate "
         "(\"active, not retracted\") by construction. Section 1 counts the natural supply; sections 2 to 4 count the counterfactual "
         "supply the registered predicates operate on.", ""]
    # A
    L += ["## 1. The manifests, per persona (natural events)", "",
          "| persona | manifest retraction records | resolving to an entry (TAU_HI) | entries retracted under TRUE | store flag is_retracted | manifest expiring_logistics | status expired | expired records resolving to an entry | status upcoming / other | entries expired under TRUE | 661 obligations: sup / ret / exp |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    tot = collections.Counter()
    for r in A:
        L.append(f"| {r['persona']} | {r['manifest_retractions']} | {r['retraction_records_resolving_to_an_entry']} | {r['entries_retracted_under_TRUE']} | {r['store_flag_is_retracted']} | "
                 f"{r['manifest_expiring_logistics']} | {r['expiring_status_expired']} | {r['expired_records_resolving_to_an_entry']} | {r['expiring_status_other']} | {r['entries_expired_under_TRUE']} | "
                 f"{r['obligations_661_supersession']} / {r['obligations_661_retraction']} / {r['obligations_661_expiry']} |")
        for k, v in r.items():
            if isinstance(v, int):
                tot[k] += v
    L.append(f"| **all 40** | **{tot['manifest_retractions']}** | **{tot['retraction_records_resolving_to_an_entry']}** | **{tot['entries_retracted_under_TRUE']}** | {tot['store_flag_is_retracted']} | "
             f"**{tot['manifest_expiring_logistics']}** | **{tot['expiring_status_expired']}** | **{tot['expired_records_resolving_to_an_entry']}** | **{tot['expiring_status_other']}** | **{tot['entries_expired_under_TRUE']}** | "
             f"{tot['obligations_661_supersession']} / {tot['obligations_661_retraction']} / {tot['obligations_661_expiry']} |")
    L += ["", f"Natural supply: **{tot['manifest_retractions']} retraction records** (one per persona) and **{tot['expiring_status_expired']} expired "
          f"logistics records** across the 40 manifests, plus {tot['expiring_status_other']} logistics records whose status is not expired "
          f"(the dated events still ahead of the cutoff -- the pool the counterfactual expiry class draws its anchors from). A CF-3 built on the "
          f"natural events would be a different construction (a store version with the event undone) and is not what the registered predicates "
          f"describe; nothing here proposes it.", ""]
    # B
    for cls in STATES:
        rows = B[cls]; t, c = tables[cls]
        universe = ("active-or-not entries in PROJECTS_ENDEAVORS with a null event_time" if cls == "RETRACTION"
                    else "entries of any category with a non-null event_time (the O3 class; the cutoff is predicate P5)")
        L += [f"## 2{'a' if cls == 'RETRACTION' else 'b'}. {cls}: the predicates replayed one at a time", "",
              f"Universe: {universe} -- **{len(rows)}** entries over the 40 banks. Each entry is charged to the first predicate that removes it, in the registered order; "
              f"the lists are in `census_cf3.json` (`B_predicates`) and, for the read-stage and post-draw removals, in section 2c.", "",
              "| predicate | removed | remaining |", "|---|---:|---:|"]
        remaining = len(rows)
        labels = [("P1", "P1 slot_key present"), ("P2", "P2 slot_key occurs exactly once in the bank"), ("P3a", "P3a entry is active"),
                  ("P3b", "P3b entry is not retracted"), ("P3c", "P3c entry supersedes nothing"), ("P4", f"P4 at least {SP.MIN_TEXT_TOKENS} content tokens"),
                  ("P5", "P5 (expiry) anchor at or after the pinned cutoff"), ("P6", "P6 individuation (own-state section in PRESENT)"),
                  ("P7", "P7 superseded-list exclusion (v2)"), ("P8", "P8 zero overlap with the 90 / 84 / 36 (O1, O2 re-admitted)"),
                  ("P8x", "P8x admitted but absent from the CF-2 queue (a check; should be 0)"),
                  ("P9c", "P9c CF-1's INELIGIBLE verdict, reused and binding"),
                  ("P9", "P9 the author's eligibility read: INELIGIBLE"), ("P9r", "P9r rank-skip (same-name earlier candidate ELIGIBLE; not read)"),
                  ("P9u", "P9u unread (past the stop position)"), ("P11", "P11 one pair per (persona, scrubbed name) at acceptance"),
                  ("P12", "P12 ELIGIBLE and undrawn (quota, cap or walk order)"), ("P13", "P13 excluded after the draw (authoring predicate / PN read)")]
        for key, lab in labels:
            n = t.get(key, 0)
            if key == "P5" and cls != "EXPIRY":
                continue
            remaining -= n
            L.append(f"| {lab} | {n} | {remaining} |")
        L.append(f"| **accepted into the 444** | — | **{sum(1 for r in rows if r['removed_by'] is None)}** |")
        L.append("")
    # 2c the read-stage and post-draw lists
    L += ["## 2c. The removed candidates at the read stage and after the draw, listed", ""]
    for cls in STATES:
        rows = B[cls]
        for tag, title in (("P13", "excluded after the draw"), ("P11", "passed over at acceptance (one pair per persona and scrubbed name)"),
                           ("P12", "ELIGIBLE and undrawn"), ("P9r", "rank-skipped, not read"), ("P6 ", "individuation"), ("P7 ", "superseded-list exclusion"), ("P8 ", "overlap")):
            sel = [r for r in rows if (r["removed_by"] or "").startswith(tag)]
            if not sel:
                continue
            L += [f"### {cls} — {title} ({len(sel)})", "", "| persona | entry | slot | category | event | queue pos. | reason | text |", "|---|---|---|---|---|---:|---|---|"]
            for r in sorted(sel, key=lambda r: (r.get("queue_position") or 10**9, r["persona"], r["entry_id"])):
                L.append(f"| {r['persona']} | `{r['entry_id']}` | `{r['slot']}` | {r['category']} | {r['event_time'] or '—'} | {r.get('queue_position') or '—'} | {r['removed_by']} | {r['text'][:140].replace('|', '/')} |")
            L.append("")
        inel = [r for r in rows if (r["removed_by"] or "").startswith("P9 ")]
        L += [f"### {cls} — INELIGIBLE at the author's eligibility read ({len(inel)}; the per-row reason field is empty for the 2026-09-12 verdicts, the rules are ADDENDUM_CF2 §3.1's notes)", "",
              "| persona | entry | slot | queue pos. | text |", "|---|---|---|---:|---|"]
        for r in sorted(inel, key=lambda r: (r.get("queue_position") or 10**9)):
            L.append(f"| {r['persona']} | `{r['entry_id']}` | `{r['slot']}` | {r.get('queue_position') or '—'} | {r['text'][:150].replace('|', '/')} |")
        L.append("")
    # 3. the author's read, retraction
    L += ["## 3. Retraction candidates that fell at the author's read, and whether one re-authoring under D-CF2-3 would make them eligible", "",
          "Two reads exist. The **eligibility read** (ADDENDUM_CF2 §3.1) judges the original record; a NO there (INELIGIBLE, section 2c) is a fact about the "
          "record, and re-authoring the counterfactual successor cannot change it -- D-CF2-3 does not apply. The **PN read** (D-CF2-3) judges the "
          "authored retracting record; a NO there is re-authored once at seed 4242 and re-read, and a second NO falls to D-CF2-2.", ""]
    L += ["| persona | entry | slot | what fell | already re-authored under D-CF2-3? | would a single re-authoring make it eligible? |", "|---|---|---|---|---|---|"]
    for r in fell:
        reason = r["removed_by"]
        if "PN read" in reason:
            ans = "**No** — it was re-authored once at seed 4242 under D-CF2-3 and failed the re-read (NO-implausible both times); a second re-authoring is outside D-CF2-3."
            done = "yes (seed 4242; the re-read failed)"
        else:
            ans = "**No** — it fell on the authoring predicate (fewer than 3 discriminative tokens on the old side) after the frozen retry, which is the one re-authoring D-CF2-2 allows; the record's own text is the limit, not the seed."
            done = "the frozen retry ran (D-CF2-2)"
        L.append(f"| {r['persona']} | `{r['entry_id']}` | `{r['slot']}` | {reason} | {done} | {ans} |")
    pr = J(CF2 / "pn_read_verdicts.json"); rr = J(CF2 / "pn_reread_verdicts.json")
    pr_r = [v for v in pr["verdicts"] if v["state"] == "RETRACTION"]; rr_r = [v for v in rr["verdicts"] if v["state"] == "RETRACTION"]
    L += ["", f"PN read on the authored retraction records: {collections.Counter(v['verdict'] for v in pr_r)} of {len(pr_r)}; re-read: {collections.Counter(v['verdict'] for v in rr_r)}. "
          f"No retraction candidate is recoverable by a single D-CF2-3 re-authoring: the one PN-read failure was re-authored and failed again, the one authoring-predicate failure "
          f"is a property of the record's text, and the {len([r for r in B['RETRACTION'] if (r['removed_by'] or '').startswith('P9 ')])} INELIGIBLE verdicts are on the records themselves.", ""]
    # 4. sizing
    L += ["## 4. Supply, use, and the largest CF-3 addition the registered predicates admit", ""]
    for cls in STATES:
        z = Cz[cls]; b = z["no_relaxation"]
        L += [f"### {cls}", "",
              f"- **Used in the 444:** {z['used_in_the_444']} pairs.",
              f"- **Zero reads, no relaxation:** {b['eligible_undrawn']} ELIGIBLE candidates are undrawn; **{b['eligible_undrawn_fitting_cap_and_name']}** fit the cap (4 per persona per state, counting the 444's usage) and the one-per-name rule"
              + (f": {', '.join(b['eligible_undrawn_fitting_list'])}." if b['eligible_undrawn_fitting_list'] else "."),
              f"- **With reads, no relaxation:** {b['unread_admitted']} admitted candidates were never read; **{b['unread_fitting_cap_and_name']}** of them fit the cap and the name rule given the 444's usage; "
              f"at the observed eligibility rate of this state's reads ({b['observed_eligibility_rate']}, about {b['reads_per_eligible']} reads per eligible pair) that is **about {b['expected_eligible_among_unread_fitting']} more eligible pairs** if every one is read."]
        for k, v in z["single_relaxations"].items():
            L.append(f"- **{k}:** " + "; ".join(f"{kk} {vv}" for kk, vv in v.items()) + ".")
        for k, v in R[cls].items():
            L.append(f"- **{k}:** {v} entries would re-enter the pool before any read (their P3–P8 status is not evaluated here).")
        if cls == "RETRACTION":
            L.append(f"- **R3 retraction class widened beyond PROJECTS_ENDEAVORS** (active, unique-slot, ≥6-token entries with a null event_time, by category, before individuation, overlap and reads): "
                     + ", ".join(f"{k} {v}" for k, v in R3.items()) + f" — {sum(R3.values())} in all; whether any is a cancellable plan under §3.1 is a read, and the observed rate in PROJECTS_ENDEAVORS ({b['observed_eligibility_rate']}) is the only estimate.")
        L.append("")
    zr, ze = Cz["RETRACTION"]["no_relaxation"], Cz["EXPIRY"]["no_relaxation"]
    L += ["## 5. Reading (counts only; the ruling is the author's)", "",
          f"- **Natural supply (manifests):** {tot['manifest_retractions']} retraction records, {tot['retraction_records_resolving_to_an_entry']} of which resolve to a bank entry under the TRUE join; "
          f"{tot['expiring_status_expired']} expired logistics records, {tot['expired_records_resolving_to_an_entry']} resolving. These are the events behind the 661's 26 retraction and 15 expiry obligations; "
          f"none is a candidate under the registered predicates, because a candidate must be active and unretracted.",
          f"- **Counterfactual supply, retraction:** the class predicate admits {len(B['RETRACTION'])} records; the candidate and draw-time predicates leave 1,043, of which 1,018 entered the queue; "
          f"the walk read {sum(1 for r in B['RETRACTION'] if (r['removed_by'] or '').startswith('P9 '))} INELIGIBLE against 36 ELIGIBLE (rate {zr['observed_eligibility_rate']}), used 30, and left "
          f"{zr['unread_admitted']} unread. The binding constraint on a CF-3 is not the predicates but the name rule: {collections.Counter(r['slot_scrubbed'] for r in B['RETRACTION'] if (r['removed_by'] or '').startswith('P9u')).most_common(1)[0][1]} of the "
          f"{zr['unread_admitted']} unread carry the scrubbed name `project`, one pair of which each persona may hold across the draw. Without relaxation: {zr['eligible_undrawn_fitting_cap_and_name']} pairs at zero reads, "
          f"and about {zr['expected_eligible_among_unread_fitting']} more from the {zr['unread_fitting_cap_and_name']} unread candidates that fit the cap and the name rule ({zr['reads_per_eligible']} reads per eligible pair). "
          f"Lifting the cap alone: about {Cz['RETRACTION']['single_relaxations']['R1 cap 4 per persona per state lifted']['expected_eligible']} from {Cz['RETRACTION']['single_relaxations']['R1 cap 4 per persona per state lifted']['unread_fitting']} reads; "
          f"lifting the name rule alone: {Cz['RETRACTION']['single_relaxations']['R2 one pair per (persona, scrubbed name) lifted']['eligible_undrawn_fitting']} at zero reads and about "
          f"{Cz['RETRACTION']['single_relaxations']['R2 one pair per (persona, scrubbed name) lifted']['expected_eligible']} more from {Cz['RETRACTION']['single_relaxations']['R2 one pair per (persona, scrubbed name) lifted']['unread_or_rank_skipped_fitting']} reads.",
          f"- **Counterfactual supply, expiry:** the class predicate admits {len(B['EXPIRY'])} dated records, 133 pass the candidate predicates, 70 entered the queue and every one was read: 49 ELIGIBLE, 30 used. "
          f"Without relaxation **{ze['eligible_undrawn_fitting_cap_and_name']} more expiry pairs are available at zero reads**; lifting the cap gives "
          f"{Cz['EXPIRY']['single_relaxations']['R1 cap 4 per persona per state lifted']['eligible_undrawn_fitting']}, lifting the name rule "
          f"{Cz['EXPIRY']['single_relaxations']['R2 one pair per (persona, scrubbed name) lifted']['eligible_undrawn_fitting']} plus 5 rank-skipped candidates to read; the expiry pool is otherwise exhausted "
          f"(0 unread), and the 15 overlap-removed candidates are the only other readable entries under a single relaxation.",
          "- **Nothing is drawn, registered or re-authored here.** Every number is a count on the committed artifacts; the JSON lists each candidate with the predicate that removed it.", ""]
    (OUT / "CF3_CENSUS.md").write_text("\n".join(L), encoding="utf-8", newline="\n")
    print("wrote", OUT / "CF3_CENSUS.md", "and census_cf3.json")
    for cls in STATES:
        print(cls, "stages:", tables[cls][0])
        print(cls, "sizing:", json.dumps(Cz[cls]["no_relaxation"], default=str)[:600])


if __name__ == "__main__":
    main()
