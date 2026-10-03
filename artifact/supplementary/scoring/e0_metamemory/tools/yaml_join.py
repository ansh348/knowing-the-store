"""
yaml_join.py -- E0 metamemory probe: the YAML-NATIVE provenance join.

NO API CALLS. Read-only. No model in the loop at any point.

This implements the join the E0 prompt actually specifies -- "computable by
provenance join against YAML ground truth (supersession chains, expiry dates,
retraction events)" -- as opposed to the LLM-judged or lexical-proxy substitutes
measured in feasibility.py. It exists to answer one question: at the prescribed
scale (10 personas, 2-3 ablated categories), how many (question, variant) items
does the specified join actually resolve, per label cell?

Two stages.

  Stage A  question -> YAML ground-truth SECTION RECORD.
           The question id is positional: idx = int(qid.split('_q')[1]) - 1 indexes
           the persona's draft_questions list (verified 500/516 exact). But the
           label needs the *section* record, not the draft question, and
           convert_draft_questions.py retains no pointer to it. So: route by
           attack_vector to a section, then take the token-overlap argmax over that
           section's records, requiring a margin of >=2 tokens to the runner-up.
           AV5 (broad query) and AV8 (numeric) have no source section by
           construction -> UNRESOLVED.

  Stage B  YAML record -> bank entry ids.
           B1  expiring_logistics: event_date equality against entry.event_time.
           B2  everything else: session-anchored lexical resolution -- candidates
               restricted to entries with source_session == the record's session,
               then >=2 shared content tokens and >=50% coverage of the fact's
               tokens.
           Pure structural alternatives were measured and rejected: YAML `slot`
           vs bank slot_key matches 26/121 verbatim; slot-chain spanning
           old_session..new_session is unique for only 44/121.

Negative obligation is text-anchored against the YAML OLD value and deliberately
does NOT trust is_active. Reason: the ingest pipeline failed to supersede in most
YAML-declared cases, so is_active=False is not a reliable stale marker relative to
YAML ground truth. Expiry uses the operational cutoff the system itself applies
(t_now - 14d, lifecycle_bank.py:1055), with t_now pinned from the FULL bank so the
ablation cannot move it.

Run:  python e0_metamemory/tools/yaml_join.py
"""

from __future__ import annotations

import collections
import datetime as dt
import io
import itertools
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LME = PROJECT_ROOT / "LifeMemEval"
BANKS = LME / "artifacts" / "lifecycle_banks"
QUESTIONS = LME / "lifemembench_questions.json"

TAU = 0.50          # token-coverage threshold for lexical resolution
MIN_SHARED = 2      # minimum shared content tokens
MIN_MARGIN = 2      # Stage A argmax margin to runner-up
EXPIRY_WINDOW = dt.timedelta(days=14)   # lifecycle_bank.py:1055

CATEGORIES = [
    "PROJECTS_ENDEAVORS", "RELATIONAL_BONDS", "OBLIGATIONS", "HOBBIES_RECREATION",
    "LOGISTICAL_CONTEXT", "HEALTH_WELLBEING", "IDENTITY_SELF_CONCEPT",
    "PREFERENCES_HABITS", "INTELLECTUAL_INTERESTS", "FINANCIAL_MATERIAL", "OTHER",
]

STOP = set("""a an the is are was were be been being has have had do does did of in on at to for
with and and or but not no as by from that this these those it its user users they them their he
she his her him about again still now then there here some any more most other such own so than too
very can will just should would could""".split())

# Which YAML section each attack vector draws from. Verified empirically by
# lexical argmax over all sections: AV1/AV2/AV4/AV6/AV7/AV9 100%, AV3 97.9%.
AV_SECTION = {
    "AV1_superseded_preference": "supersession_events",
    "AV4_multi_version_fact": "supersession_events",
    "AV2_expired_logistics": "expiring_logistics",
    "AV3_stable_identity": "stable_identity",
    "AV6_cross_session_contradiction": "contradictions",
    "AV7_selective_forgetting": "retractions",
    "AV9_soft_supersession": "ambiguous",
    # AV5_broad_query and AV8_numeric_preservation: no source section, by design.
}

# (gold fact field, gold session field, stale fact field, stale session field)
SECTION_FIELDS = {
    "supersession_events": ("new_fact", "new_session", "old_fact", "old_session"),
    "contradictions":      ("new_fact", "new_session", None, None),
    "retractions":         ("retraction", "retraction_session", "original_fact", "original_session"),
    "expiring_logistics":  ("fact", "session", None, None),
    "stable_identity":     ("fact", "session", None, None),
    "ambiguous":           ("existing_fact", "existing_session", None, None),
}

_YAML_FIX = re.compile(
    r'^(\s*wrong_if_surfaced:\s*)"((?:[^"\\]|\\.)*?)"\s+(\(.*\))\s*$', re.MULTILINE)


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def toks(s, drop=frozenset()):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c)).casefold()
    s = re.sub(r"(?<=[a-z])(?=\d)|(?<=\d)(?=[a-z])", " ", s)   # "4x" -> "4 x"
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return {w for w in s.split() if w not in STOP and len(w) > 1} - drop


def cov(target: set, text_tokens: set) -> float:
    return len(target & text_tokens) / len(target) if target else 0.0


def load_yaml(path):
    raw = io.open(path, encoding="utf-8").read()
    return yaml.safe_load(_YAML_FIX.sub(r'\1"\2 \3"', raw))


def parse_event_time(v):
    if not v:
        return None
    try:
        d = dt.datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except Exception:
        return None
    return d.replace(tzinfo=dt.timezone.utc) if d.tzinfo is None else d


class PersonaJoin:
    def __init__(self, name, yaml_path, questions):
        self.name = name
        self.q = questions
        self.y = load_yaml(yaml_path)
        self.entries = jload(BANKS / f"{name}.json")["entries"]
        self.by_id = {e["id"]: e for e in self.entries}
        self.drop = toks(self.y.get("persona", {}).get("name", "") if isinstance(
            self.y.get("persona"), dict) else "")
        self.etoks = {e["id"]: toks(e.get("text", ""), self.drop) for e in self.entries}
        self.by_session = collections.defaultdict(list)
        for e in self.entries:
            self.by_session[e.get("source_session")].append(e["id"])

        # t_now pinned from the FULL bank: max created_at over ACTIVE entries + 24h
        act = [parse_event_time(e["created_at"]) for e in self.entries if e["is_active"]]
        act = [x for x in act if x]
        self.t_now = (max(act) + dt.timedelta(hours=24)) if act else None
        self.cutoff = (self.t_now - EXPIRY_WINDOW) if self.t_now else None

        self.reasons = collections.Counter()
        self.gold, self.neg = {}, {}
        for q in questions:
            g, n, why = self._resolve(q)
            self.gold[q["id"]], self.neg[q["id"]] = g, n
            if why:
                self.reasons[why] += 1

    # ---------- Stage A ----------
    def _section_record(self, q):
        sec = AV_SECTION.get(q["attack_vector"])
        if sec is None:
            return None, "A_no_source_section"
        recs = self.y.get(sec) or []
        recs = [r for r in recs if isinstance(r, dict)]
        if not recs:
            return None, "A_empty_section"
        probe = toks(" ".join([q["question"], q.get("correct_answer") or ""]
                              + list(q.get("wrong_answer_indicators") or [])), self.drop)
        scored = sorted(
            ((len(probe & toks(" ".join(str(v) for v in r.values()), self.drop)), i, r)
             for i, r in enumerate(recs)), key=lambda t: -t[0])
        if not scored or scored[0][0] == 0:
            return None, "A_zero_overlap"
        if len(scored) > 1 and scored[0][0] - scored[1][0] < MIN_MARGIN:
            return None, "A_tie"
        return (sec, scored[0][2]), None

    # ---------- Stage B ----------
    def _b1_event_date(self, rec):
        d = str(rec.get("event_date") or "")[:10]
        if not d:
            return None
        hits = {e["id"] for e in self.entries
                if str(e.get("event_time") or "")[:10] == d}
        return hits or None

    def _b2_session(self, fact, session):
        tf = toks(fact, self.drop)
        if len(tf) < 3:
            return None, "B_degenerate_fact"
        cands = self.by_session.get(session) or []
        if not cands:
            return None, "B_no_such_session"
        hits = {i for i in cands
                if len(tf & self.etoks[i]) >= MIN_SHARED and cov(tf, self.etoks[i]) >= TAU}
        return (hits, None) if hits else (None, "B_no_session_anchor")

    def _asserts(self, discr_own, discr_other):
        """Entries asserting the value characterised by discr_own, bank-wide."""
        if len(discr_own) < 3 or len(discr_other) < 3:
            return None
        return {i for i, t in self.etoks.items()
                if len(discr_own & t) >= MIN_SHARED
                and cov(discr_own, t) >= TAU and cov(discr_other, t) < 0.34}

    def _expired(self, eid):
        d = parse_event_time(self.by_id[eid].get("event_time"))
        return bool(d and self.cutoff and d < self.cutoff)

    def _resolve(self, q):
        sr, why = self._section_record(q)
        if sr is None:
            return None, None, why
        sec, rec = sr
        gf, gs, sf, ss = SECTION_FIELDS[sec]

        # ---- gold
        if sec == "expiring_logistics":
            gold = self._b1_event_date(rec)
            if gold is None:
                gold, why = self._b2_session(rec.get(gf), rec.get(gs))
                if gold is None:
                    return None, None, why
        else:
            gold, why = self._b2_session(rec.get(gf), rec.get(gs))
            if gold is None:
                return None, None, why

        # ---- negative obligation
        neg = set()
        if sec == "expiring_logistics":
            neg = {i for i in gold if self._expired(i)}
            if neg:
                gold = gold - neg
        elif sf:
            old_t = toks(rec.get(sf), self.drop)
            new_t = toks(rec.get(gf), self.drop)
            a = self._asserts(old_t - new_t, new_t - old_t)
            if a is None:
                return None, None, "N_weak_discriminator"
            neg = a
            if sec == "retractions":
                anchored, _ = self._b2_session(rec.get(sf), rec.get(ss))
                neg |= (anchored or set())
                neg |= {e["id"] for e in self.entries if e["is_retracted"]
                        and cov(old_t, self.etoks[e["id"]]) >= TAU}
        if not gold and not neg:
            return None, None, "B_empty_after_split"
        return gold, neg, None

    # ---------- labelling ----------
    def label(self, q, ablated):
        qid = q["id"]
        g, n = self.gold[qid], self.neg[qid]
        if g is None:
            return "UNRESOLVED"
        G = {i for i in g if self.by_id[i]["category"] not in ablated}
        N = {i for i in (n or set()) if self.by_id[i]["category"] not in ablated}
        if N:
            return "PRESENT-NEGATIVE"
        return "PRESENT" if G else "ABSENT"

    def census(self, ablated):
        c = collections.Counter()
        for q in self.q:
            for v in (frozenset(), ablated):
                c[self.label(q, v)] += 1
        return c


def main():
    qs = jload(QUESTIONS)
    byp = collections.defaultdict(list)
    for q in qs:
        byp[q["persona"]].append(q)
    ypaths = {p.name.replace(".yaml", "").split("_")[-1]: p
              for p in sorted(LME.glob("*/persona_*.yaml"))}

    joins, reasons = {}, collections.Counter()
    for name, ql in sorted(byp.items()):
        try:
            J = PersonaJoin(name, ypaths[name], ql)
        except Exception as ex:
            print(f"  !! {name}: {type(ex).__name__}: {ex}")
            continue
        joins[name] = J
        reasons.update(J.reasons)

    tot_q = sum(len(J.q) for J in joins.values())
    res = sum(1 for J in joins.values() for q in J.q if J.gold[q["id"]] is not None)
    print("=" * 96)
    print("YAML-NATIVE JOIN -- resolution")
    print("=" * 96)
    print(f"  personas parsed            : {len(joins)}/40")
    print(f"  questions                  : {tot_q}")
    print(f"  RESOLVED (gold established): {res}  ({res/tot_q:.1%})")
    print(f"  UNRESOLVED                 : {tot_q-res}  ({1-res/tot_q:.1%})")
    print("\n  UNRESOLVED reasons:")
    for k, v in reasons.most_common():
        print(f"    {k:26s} {v:4d}")

    print("\n  resolved questions by attack vector:")
    per_av = collections.Counter()
    tot_av = collections.Counter()
    for J in joins.values():
        for q in J.q:
            tot_av[q["attack_vector"]] += 1
            if J.gold[q["id"]] is not None:
                per_av[q["attack_vector"]] += 1
    for av in sorted(tot_av):
        print(f"    {av:34s} {per_av[av]:3d}/{tot_av[av]:3d}")

    # ---- cell sizes at the prescribed scale and beyond
    print()
    print("=" * 96)
    print("CELL SIZES under the YAML-native join (counts over BOTH variants)")
    print("=" * 96)
    for kmax in (3, 5):
        best = {}
        for name, J in joins.items():
            cand = []
            for k in range(2, kmax + 1):
                for combo in itertools.combinations(CATEGORIES, k):
                    c = J.census(frozenset(combo))
                    cand.append((c["ABSENT"], c["PRESENT-NEGATIVE"], c["PRESENT"], combo, c))
            cand.sort(key=lambda t: (-t[0], -t[1], -t[2], len(t[3])))
            best[name] = cand[0]

        def totals(sel):
            t = collections.Counter()
            for x in sel:
                t.update(best[x][4])
            return t

        def score(t):
            return (min(t["PRESENT"], t["ABSENT"], t["PRESENT-NEGATIVE"]),
                    t["PRESENT"] + t["ABSENT"] + t["PRESENT-NEGATIVE"])

        for n in (10, 20, 40):
            sel, pool = [], list(best)
            while len(sel) < min(n, len(pool) + len(sel)) and pool:
                c = max(pool, key=lambda x: score(totals(sel + [x])))
                sel.append(c); pool.remove(c)
            t = totals(sel)
            scoreable = t["PRESENT"] + t["ABSENT"] + t["PRESENT-NEGATIVE"]
            mn = min(t["PRESENT"], t["ABSENT"], t["PRESENT-NEGATIVE"])
            comp = (f"{t['PRESENT']/scoreable:.0%}/{t['ABSENT']/scoreable:.0%}/"
                    f"{t['PRESENT-NEGATIVE']/scoreable:.0%}" if scoreable else "-")
            print(f"  k<={kmax}, {n:2d} personas   PRES={t['PRESENT']:4d} ABS={t['ABSENT']:4d} "
                  f"PNEG={t['PRESENT-NEGATIVE']:4d} UNRES={t['UNRESOLVED']:4d} | n={scoreable:4d} "
                  f"min={mn:3d} {'PASS' if mn >= 60 else 'FAIL'} | {comp}")


if __name__ == "__main__":
    main()
