"""p2_labels_at_t.py -- E3 feasibility probe 2: are Definition-1 labels derivable at t?

READ-ONLY. NO API CALLS. NO WRITES to any store, index or E1/E2 artifact.

E1/E2 label an item by asking, of a store VARIANT, which ground-truth entry ids
survive it:

    label(q, ablated) : survive = {i : category(i) not in ablated}

A store-state-at-t is another survival set, so the same rule should run with

    survive = {i : source_session(i) <= s}

This probe tests whether that substitution is sufficient, and reports exactly what
it is NOT sufficient for. Three things are checked:

  C1  MECHANICAL SUBSTITUTION. Does the existing PersonaJoin label rule accept a
      session-survival set and terminate on every (question, snapshot)?
  C2  EVENT ACTIVATION. A negative obligation exists only after the event that
      creates it. Filtering entries alone leaves pre-event snapshots claiming an
      obligation the timeline has not yet produced. Measured, not assumed.
  C3  ANSWER-KEY VALIDITY. The authored `correct_answer` / `wrong_answer_indicators`
      describe the END state. At a pre-resolution snapshot they are inverted --
      the wrong indicator IS the correct answer. Counted per (question, snapshot).

  C4  VERDICT REUSE. E1's PN verification is hand-adjudicated and keyed on
      (persona, question, entry). Snapshots only REMOVE entries, so every pair a
      snapshot needs should already be adjudicated. Checked, not assumed.

Also emits a hand-verification worksheet of 10 sampled (question, timepoint)
labels with all their evidence, for adjudication by reading.

Usage:  python e3_metamemory/probes/p2_labels_at_t.py
"""

from __future__ import annotations

import collections
import datetime as dt
import io
import json
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LME = PROJECT_ROOT / "LifeMemEval"
E1 = PROJECT_ROOT / "e1_metamemory"
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(PROJECT_ROOT / "e1_metamemory" / "tools"))

from e0_common import (  # noqa: E402
    EXPIRY_WINDOW, SECTION_FIELDS, TAU_GOLD, cov, load_joins, parse_dt, toks,
)

OUT = Path(__file__).resolve().parent / "p2_labels_at_t.json"
SHEET = Path(__file__).resolve().parent / "p2_handcheck.md"

TAU_LO, TAU_HI = 0.20, 0.80          # build_e1.py, unchanged
LADDER = (7, 14, 21, 28, 35)         # illustrative only; the real ladder is a design call
SEED = 42

# resolving-side session field per section: the event does not exist before it.
RESOLVING_FIELD = {
    "supersession_events": "new_session",
    "contradictions":      "new_session",
    "retractions":         "retraction_session",
    "expiring_logistics":  None,       # time-driven, not write-driven
    "stable_identity":     None,
    "ambiguous":           None,       # no dated resolving side (p1: 0/40)
}
OLD_FIELD = {
    "supersession_events": ("old_fact", "old_session"),
    "contradictions":      ("old_fact", "old_session"),
    "retractions":         ("original_fact", "original_session"),
}


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def as_int(v):
    import re
    if v is None:
        return None
    if isinstance(v, int):
        return v
    m = re.search(r"\d+", str(v))
    return int(m.group()) if m else None


def session_dates():
    """persona -> {session_id: date}, from the session files themselves."""
    out = {}
    for ypath in sorted(LME.glob("*/persona_*.yaml")):
        name = ypath.name.replace(".yaml", "").split("_")[-1]
        d = {}
        for f in sorted((ypath.parent / "sessions").glob("session_*.json")):
            j = jload(f)
            d[int(j["session_id"])] = str(j["date"])
        out[name] = d
    return out


class TimeAnchored:
    """The label rule of e0_common.PersonaJoin, re-anchored on a snapshot.

    Exactly three things change relative to PersonaJoin.label:
      (a) survival is by source_session, not by category;
      (b) the expiry cutoff moves with the snapshot's own t_now;
      (c) an event's negative obligation is inert before its resolving session,
          and the OLD side is the gold side in that window.
    Nothing else is touched: gold / fires / expired_neg are PersonaJoin's, verbatim.
    """

    def __init__(self, J, dates):
        self.J = J
        self.dates = dates
        self.rec_cache = {}

    def t_now(self, s):
        d = self.dates.get(s)
        if not d:
            return None
        return parse_dt(d) + dt.timedelta(hours=24)

    def record(self, qid):
        if qid in self.rec_cache:
            return self.rec_cache[qid]
        r = self.J.rec_of.get(qid)
        out = (None, None)
        if r:
            sec, ridx = r
            recs = [x for x in (self.J.y.get(sec) or []) if isinstance(x, dict)]
            out = (sec, recs[ridx])
        self.rec_cache[qid] = out
        return out

    def resolving_session(self, qid):
        sec, rec = self.record(qid)
        if sec is None:
            return None
        f = RESOLVING_FIELD.get(sec)
        return as_int(rec.get(f)) if f else None

    def alive(self, s):
        return {e["id"] for e in self.J.entries if (e.get("source_session") or 0) <= s}

    def expired_at(self, ids, s):
        cutoff = self.t_now(s)
        if cutoff is None:
            return set()
        cutoff = cutoff - EXPIRY_WINDOW
        out = set()
        for i in ids:
            d = parse_dt(self.J.by_id[i].get("event_time"))
            if d is not None and d < cutoff:
                out.add(i)
        return out

    def label_at(self, q, s, activate_events=True, role_swap=True):
        """Returns (label, subtype, evidence dict)."""
        qid = q["id"]
        ev = {"snapshot": s}
        if self.J.gold.get(qid) is None:
            return "UNRESOLVED", None, ev
        A = self.alive(s)
        sec, rec = self.record(qid)
        G = {i for i in self.J.gold[qid] if i in A}
        fired = {i: v for i, v in (self.J.fires[qid] or {}).items() if i in A}
        # (b) expiry is recomputed against the snapshot's own t_now
        exp = self.expired_at({i for i in (self.J.expired_neg[qid] or set())} | G, s) \
            if sec == "expiring_logistics" else set()
        G = G - exp
        rs = self.resolving_session(qid)
        ev.update({"section": sec, "resolving_session": rs,
                   "n_gold_alive": len(G), "n_fired_alive": len(fired),
                   "n_expired": len(exp), "t_now": str(self.t_now(s))})

        # (c) the event has not happened yet: no obligation, and the OLD side is gold
        pre_event = activate_events and rs is not None and s < rs
        ev["pre_event"] = pre_event
        if pre_event:
            hi_pre = {i for i, v in fired.items() if v >= TAU_HI}
            ev["n_old_side_alive"] = len(hi_pre)
            if role_swap:
                # before the change, the entries asserting the OLD value ARE current
                return ("PRESENT" if hi_pre else "ABSENT"), "pre-event", ev
            return ("PRESENT" if G else "ABSENT"), "pre-event-noswap", ev

        hi = {i for i, v in fired.items() if v >= TAU_HI} | exp
        lo = {i for i, v in fired.items() if v >= TAU_LO}
        if hi:
            return "PRESENT-NEGATIVE", ("with-replacement" if G else
                                        "without-replacement"), ev
        if lo:
            return "UNRESOLVED", "between-thresholds", ev
        return ("PRESENT" if G else "ABSENT"), None, ev


def main():
    print("loading joins (40 personas, ~19k entries)...", flush=True)
    joins = load_joins()
    dates = session_dates()
    qs = {q["id"]: q for J in joins.values() for q in J.questions}

    items = [i for i in jload(E1 / "build" / "items_final.json")
             if i["backend"] == "frbank" and i["variant"] == "FULL"
             and i.get("label", i["label_pre"]) in
             ("PRESENT", "ABSENT", "PRESENT-NEGATIVE")]
    allq = sorted({(i["persona"], i["question_id"]) for i in items})
    scope = [x for x in allq if x[1] in qs]
    probes = [x for x in allq if x[1] not in qs]
    final = {(i["persona"], i["question_id"]): i.get("label", i["label_pre"])
             for i in items}
    print(f"scoreable FULL-variant items: {len(allq)}  "
          f"= {len(scope)} authored questions + {len(probes)} natural-absent probes")
    print(f"  probe labels at FULL: "
          f"{collections.Counter(final[x] for x in probes)}  "
          "(no YAML record; ABSENT by construction at every t)")

    TA = {p: TimeAnchored(joins[p], dates[p]) for p in joins}

    # ---------------------------------------------------- C1 + C2: trajectories
    traj, cens, cens_noact = {}, collections.Counter(), collections.Counter()
    for p, qid in scope:
        q = qs[qid]
        row = []
        for s in LADDER:
            lab, sub, ev = TA[p].label_at(q, s)
            lab0, _, _ = TA[p].label_at(q, s, activate_events=False)
            row.append({"s": s, "label": lab, "subtype": sub,
                        "label_no_activation": lab0, "ev": ev})
            cens[(s, lab)] += 1
            cens_noact[(s, lab0)] += 1
        traj[f"{p}:{qid}"] = row

    print("\n" + "=" * 100)
    print("C1/C2 -- LABEL CENSUS BY SNAPSHOT   (FULL-variant scoreable questions)")
    print("=" * 100)
    labs = ("PRESENT", "PRESENT-NEGATIVE", "ABSENT", "UNRESOLVED")
    print(f"  {'snapshot':>9s} " + "".join(f"{l:>19s}" for l in labs))
    for s in LADDER:
        print(f"  s={s:<7d} " + "".join(f"{cens[(s, l)]:>19d}" for l in labs))
    print(f"\n  same, WITHOUT event activation (entry filter alone) -- the C2 error:")
    print(f"  {'snapshot':>9s} " + "".join(f"{l:>19s}" for l in labs))
    for s in LADDER:
        print(f"  s={s:<7d} " + "".join(f"{cens_noact[(s, l)]:>19d}" for l in labs))
    dis = sum(1 for r in traj.values() for x in r
              if x["label"] != x["label_no_activation"])
    tot = len(traj) * len(LADDER)
    print(f"\n  (question, snapshot) cells where event activation CHANGES the label: "
          f"{dis} / {tot}  ({dis / tot:.1%})")
    print("  -> the entry filter alone is NOT sufficient. C2 is real instrument work.")

    # final-rung agreement with E1's own FULL label
    agree = sum(1 for k, r in traj.items() if r[-1]["label"] == final[tuple(k.split(":"))])
    print(f"\n  ANCHOR CHECK: label at the last rung (s=35) vs E1's FULL-variant label: "
          f"{agree}/{len(traj)} agree ({agree / len(traj):.1%})")
    mism = collections.Counter((r[-1]["label"], final[tuple(k.split(":"))])
                               for k, r in traj.items()
                               if r[-1]["label"] != final[tuple(k.split(":"))])
    for (a, b), n in mism.most_common():
        print(f"      s=35 says {a:18s} E1 FULL says {b:18s} {n}")
    print("  NOTE: the rule above is E1's PRE-VERIFICATION rule. E1's committed label is")
    print("  post-verification: the hand verdicts in verify_verdicts.py demote PN candidates")
    print("  that do not assert the superseded value as current, and settle the")
    print("  between-thresholds band. Applying those verdicts at s=35:")
    from verify_verdicts import MEMBERSHIP, SEMANTIC  # noqa: PLC0415, F811

    def verified_label(p, qid, s):
        """label_at with E1's frozen hand verdicts applied, exactly as verify_e1 does."""
        q = qs[qid]
        lab, sub, ev = TA[p].label_at(q, s)
        if lab not in ("PRESENT-NEGATIVE", "UNRESOLVED"):
            return lab
        sem = SEMANTIC.get((p, qid))
        if lab == "PRESENT-NEGATIVE" and (sem is None or sem[0] != "OBLIGATION"):
            return "PRESENT" if ev["n_gold_alive"] else "ABSENT"
        A = TA[p].alive(s)
        members = [i for i, v in (joins[p].fires[qid] or {}).items()
                   if i in A and v >= TAU_LO
                   and MEMBERSHIP.get((p, qid, i), (None,))[0] == "MEMBER"]
        if members:
            return "PRESENT-NEGATIVE"
        return "PRESENT" if ev["n_gold_alive"] else "ABSENT"

    agree_v = sum(1 for p, qid in scope if verified_label(p, qid, LADDER[-1]) == final[(p, qid)])
    print(f"      verdict-applied label at s=35 vs E1's FULL label: "
          f"{agree_v}/{len(scope)} agree ({agree_v / len(scope):.1%})")
    mv = collections.Counter((verified_label(p, qid, LADDER[-1]), final[(p, qid)])
                             for p, qid in scope
                             if verified_label(p, qid, LADDER[-1]) != final[(p, qid)])
    for (a, b), n in mv.most_common():
        print(f"        s=35 {a:18s} vs E1 FULL {b:18s} {n}")

    # ------------------------------------------- expiry: labels that move with t alone
    exp_traj = collections.Counter()
    exp_qs = [(p, qid) for p, qid in scope
              if TA[p].record(qid)[0] == "expiring_logistics"]
    for p, qid in exp_qs:
        for s in LADDER:
            exp_traj[(s, TA[p].label_at(qs[qid], s)[0])] += 1
    print(f"\n  EXPIRY-DRIVEN questions ({len(exp_qs)}): labels move with t_now alone, "
          "with no write involved")
    print(f"  {'snapshot':>9s} " + "".join(f"{l:>19s}" for l in labs))
    for s in LADDER:
        print(f"  s={s:<7d} " + "".join(f"{exp_traj[(s, l)]:>19d}" for l in labs))

    # ------------------------------------------------------- C3: answer-key validity
    print("\n" + "=" * 100)
    print("C3 -- ANSWER-KEY VALIDITY AT t")
    print("=" * 100)
    pre_cells = [(k, x) for k, r in traj.items() for x in r if x["ev"].get("pre_event")]
    swappable = 0
    for k, x in pre_cells:
        p, qid = k.split(":")
        sec, rec = TA[p].record(qid)
        of = OLD_FIELD.get(sec, (None, None))[0]
        if of and rec.get(of):
            swappable += 1
    print(f"  (question, snapshot) cells BEFORE their resolving event : {len(pre_cells)}")
    print(f"  of those, the YAML carries an explicit OLD-side fact    : {swappable} "
          f"({swappable / max(1, len(pre_cells)):.1%})")

    # the wider key-validity question: the authored key describes the END state, so it
    # is invalid at every snapshot BEFORE the event the key describes -- including the
    # sections that never produce a negative obligation and so never set pre_event.
    def key_event_session(p, qid):
        sec, rec = TA[p].record(qid)
        if sec in ("supersession_events", "contradictions", "retractions"):
            return as_int(rec.get(RESOLVING_FIELD[sec]))
        if sec == "ambiguous":
            return as_int(rec.get("tentative_session"))
        return None                          # expiring / stable: handled by date below

    invalid = collections.Counter()
    for p, qid in scope:
        sec, rec = TA[p].record(qid)
        ke = key_event_session(p, qid)
        for s in LADDER:
            if ke is not None and s < ke:
                invalid[sec] += 1
            elif sec == "expiring_logistics":
                ed = parse_dt(str(rec.get("event_date") or "") or None)
                tn = TA[p].t_now(s)
                if ed is not None and tn is not None and tn < ed:
                    invalid[sec] += 1
    print("\n  Cells whose AUTHORED answer key describes a state the snapshot has not "
          "reached,\n  by YAML section (the key is not merely incomplete -- for the "
          "two-sided sections\n  its `wrong_answer_indicators` name what is CORRECT there):")
    for sec, n in invalid.most_common():
        print(f"    {sec:22s} {n:4d}")
    print(f"    {'TOTAL':22s} {sum(invalid.values()):4d} of {tot} cells "
          f"({sum(invalid.values()) / tot:.1%})")
    print("  For every one of these the authored correct_answer describes the END state,")
    print("  and its wrong_answer_indicators name what is CORRECT at that snapshot.")
    print("  => a per-(question, snapshot) answer key must be built. Mechanical from the")
    print("     YAML record fields, but it is new instrument code and needs its own check.")

    # ---------------------------------------------------------- C4: verdict reuse
    print("\n" + "=" * 100)
    print("C4 -- HAND-ADJUDICATED PN VERDICT REUSE")
    print("=" * 100)
    from verify_verdicts import MEMBERSHIP, SEMANTIC  # noqa: PLC0415, F811
    need_mem, need_sem = set(), set()
    for p, qid in scope:
        q = qs[qid]
        for s in LADDER:
            lab, sub, ev = TA[p].label_at(q, s)
            if lab != "PRESENT-NEGATIVE":
                continue
            need_sem.add((p, qid))
            A = TA[p].alive(s)
            for i, v in (joins[p].fires[qid] or {}).items():
                if i in A and v >= TAU_HI:
                    need_mem.add((p, qid, i))
    miss_m = sorted(need_mem - set(MEMBERSHIP))
    miss_s = sorted(need_sem - set(SEMANTIC))
    print(f"  (persona, question, entry) membership decisions needed across the ladder : "
          f"{len(need_mem)}")
    print(f"    already hand-adjudicated in verify_verdicts.MEMBERSHIP ({len(MEMBERSHIP)} held): "
          f"{len(need_mem) - len(miss_m)}   MISSING {len(miss_m)}")
    print(f"  (persona, question) semantic decisions needed                            : "
          f"{len(need_sem)}")
    print(f"    already hand-adjudicated in verify_verdicts.SEMANTIC ({len(SEMANTIC)} held): "
          f"{len(need_sem) - len(miss_s)}   MISSING {len(miss_s)}")
    if miss_m[:5]:
        print(f"    e.g. missing membership: {miss_m[:5]}")
    if miss_s[:5]:
        print(f"    e.g. missing semantic  : {miss_s[:5]}")

    # ------------------------------------------------------------- worksheet
    rng = random.Random(SEED)
    pool = [(k, x) for k, r in traj.items() for x in r if x["label"] != "UNRESOLVED"]
    sample = rng.sample(pool, 10)
    lines = ["# p2 HAND-VERIFICATION WORKSHEET — 10 sampled (question, timepoint) labels",
             "",
             f"Sampled with seed {SEED} from every (question, snapshot) cell whose derived "
             "label is not UNRESOLVED.",
             "Each block carries everything needed to adjudicate the label by reading, with "
             "no model in the path.", ""]
    for n, (k, x) in enumerate(sample, 1):
        p, qid = k.split(":")
        q, s = qs[qid], x["s"]
        sec, rec = TA[p].record(qid)
        J = joins[p]
        A = TA[p].alive(s)
        golds = sorted(i for i in (J.gold[qid] or set()) if i in A)
        fires = sorted((i for i, v in (J.fires[qid] or {}).items()
                        if i in A and v >= TAU_HI))
        lines += [
            f"## {n}. `{p}` / `{qid}` @ snapshot s={s}   ->  **{x['label']}**"
            f"{' (' + x['subtype'] + ')' if x['subtype'] else ''}", "",
            f"- **question**: {q['question']}",
            f"- authored `correct_answer` (END state): {q.get('correct_answer')}",
            f"- authored `wrong_answer_indicators`: {q.get('wrong_answer_indicators')}",
            f"- attack vector: `{q['attack_vector']}`   YAML section: `{sec}`",
            f"- resolving session: **{x['ev'].get('resolving_session')}**   "
            f"snapshot session: **{s}**   pre-event: **{x['ev'].get('pre_event')}**",
            f"- snapshot t_now: {x['ev'].get('t_now')}",
            f"- label WITHOUT event activation would be: **{x['label_no_activation']}**", ""]
        if rec:
            for f in ("old_fact", "new_fact", "original_fact", "retraction", "fact",
                      "existing_fact", "event_date", "status", "old_session",
                      "new_session", "original_session", "retraction_session", "session"):
                if rec.get(f) is not None:
                    lines.append(f"  - YAML `{f}`: {str(rec.get(f)).strip()[:220]}")
        lines += ["", f"  - gold entries alive at s={s} ({len(golds)}):"]
        for i in golds[:6]:
            e = J.by_id[i]
            lines.append(f"      - `{i}` (session {e['source_session']}, "
                         f"{str(e['created_at'])[:10]}): {e['text'][:150]}")
        lines += [f"  - obligation-fired entries alive at s={s}, signal>=0.80 ({len(fires)}):"]
        for i in fires[:6]:
            e = J.by_id[i]
            lines.append(f"      - `{i}` (session {e['source_session']}, "
                         f"{str(e['created_at'])[:10]}): {e['text'][:150]}")
        lines += ["", "  **verdict (filled in by hand):** ", ""]
    with io.open(SHEET, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\n  worksheet written: {SHEET}")

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"ladder": list(LADDER), "n_questions": len(scope),
                   "census": {f"{s}|{l}": cens[(s, l)] for s in LADDER for l in labs},
                   "census_no_activation": {f"{s}|{l}": cens_noact[(s, l)]
                                            for s in LADDER for l in labs},
                   "activation_changes_label_cells": dis, "total_cells": tot,
                   "anchor_agreement_s35": agree,
                   "pre_event_cells": len(pre_cells), "old_side_available": swappable,
                   "membership_needed": len(need_mem), "membership_missing": len(miss_m),
                   "semantic_needed": len(need_sem), "semantic_missing": len(miss_s),
                   "trajectories": traj}, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print(f"  written: {OUT}")


if __name__ == "__main__":
    main()
