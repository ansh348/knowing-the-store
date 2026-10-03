"""
e0_common.py -- shared machinery for the E0 metamemory probe.

NO API CALLS anywhere in this module. No model in the loop at any point. Every
function here is a pure function of committed LifecycleBench artifacts, so every
label is recomputable by re-running the code.

Design basis: e0_metamemory/FINDINGS_E0_STEP0.md (commit d51f12d).

Contents
  - tokenisation + coverage (the one normalisation used everywhere)
  - YAML loading with the parenthetical repair that rescues 40/40 persona files
  - PersonaJoin: Stage A (question -> YAML section record) and Stage B (record ->
    bank entry ids), the negative-obligation detector, pinned t_now, and the
    label rule with the asymmetric threshold pair
  - ablation planning and persona selection (deterministic, no randomness)

THRESHOLDS. Three named constants, deliberately distinct:

  TAU_GOLD  0.50   Stage B lexical resolution of a YAML fact to bank entry ids.
                   Governs the GOLD set only.
  TAU_LO    set by calibrate_tau.py -- high recall. ANY detector signal at or
                   above TAU_LO disqualifies an item from ABSENT. Protects the
                   gate-critical cell.
  TAU_HI    set by calibrate_tau.py -- high precision. Admits an item to
                   PRESENT-NEGATIVE. Smallest threshold reaching >=95% precision
                   on the 30-fire hand audit.

  Signal strictly between TAU_LO and TAU_HI  ->  UNRESOLVED.

Frozen values are read from thresholds.json so that the calibration is a
committed artifact rather than a literal buried in code.
"""

from __future__ import annotations

import collections
import datetime as dt
import io
import itertools
import json
import re
import unicodedata
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LME = PROJECT_ROOT / "LifeMemEval"
BANKS = LME / "artifacts" / "lifecycle_banks"
QUESTIONS = LME / "lifemembench_questions.json"
E0 = PROJECT_ROOT / "e0_metamemory"
THRESHOLDS = E0 / "thresholds.json"

TAU_GOLD = 0.50
MIN_SHARED = 2        # minimum shared content tokens for any lexical match
MIN_MARGIN = 2        # Stage A argmax margin to the runner-up
CROSS_GUARD = 0.34    # an entry asserting the OTHER value is not a detector fire
MIN_DISCR = 3         # discriminative token sets smaller than this cannot separate
EXPIRY_WINDOW = dt.timedelta(days=14)   # lifecycle_bank.py:1055

SEED = 42

CATEGORIES = [
    "PROJECTS_ENDEAVORS", "RELATIONAL_BONDS", "OBLIGATIONS", "HOBBIES_RECREATION",
    "LOGISTICAL_CONTEXT", "HEALTH_WELLBEING", "IDENTITY_SELF_CONCEPT",
    "PREFERENCES_HABITS", "INTELLECTUAL_INTERESTS", "FINANCIAL_MATERIAL", "OTHER",
]

STOP = set("""a an the is are was were be been being has have had do does did of in on at to for
with and or but not no as by from that this these those it its user users they them their he
she his her him about again still now then there here some any more most other such own so than too
very can will just should would could""".split())

# Which YAML section each attack vector draws from. AV5 (broad query) and AV8
# (numeric preservation) have no source section by construction -- they are out of
# E0 scope, which is coverage judgments over single-fact-supported questions.
AV_SECTION = {
    "AV1_superseded_preference": "supersession_events",
    "AV4_multi_version_fact": "supersession_events",
    "AV2_expired_logistics": "expiring_logistics",
    "AV3_stable_identity": "stable_identity",
    "AV6_cross_session_contradiction": "contradictions",
    "AV7_selective_forgetting": "retractions",
    "AV9_soft_supersession": "ambiguous",
}
OUT_OF_SCOPE_AV = {"AV5_broad_query", "AV8_numeric_preservation"}

# (current-value field, its session, superseded-value field, its session)
SECTION_FIELDS = {
    "supersession_events": ("new_fact", "new_session", "old_fact", "old_session"),
    "contradictions":      ("new_fact", "new_session", "old_fact", "old_session"),
    "retractions":         ("retraction", "retraction_session", "original_fact", "original_session"),
    "expiring_logistics":  ("fact", "session", None, None),
    "stable_identity":     ("fact", "session", None, None),
    "ambiguous":           ("existing_fact", "existing_session", None, None),
}

_YAML_FIX = re.compile(
    r'^(\s*wrong_if_surfaced:\s*)"((?:[^"\\]|\\.)*?)"\s+(\(.*\))\s*$', re.MULTILINE)


# --------------------------------------------------------------------------- io
def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(obj, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def load_yaml(path):
    """persona YAML; 26/40 files need the parenthetical repair to parse at all."""
    raw = io.open(path, encoding="utf-8").read()
    return yaml.safe_load(_YAML_FIX.sub(r'\1"\2 \3"', raw))


def load_thresholds():
    if not THRESHOLDS.exists():
        raise SystemExit("thresholds.json missing -- run calibrate_tau.py first")
    t = jload(THRESHOLDS)
    return float(t["tau_lo"]), float(t["tau_hi"])


# ------------------------------------------------------------------- text rules
def toks(s, drop=frozenset()):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c)).casefold()
    s = re.sub(r"(?<=[a-z])(?=\d)|(?<=\d)(?=[a-z])", " ", s)   # "4x" -> "4 x"
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return {w for w in s.split() if w not in STOP and len(w) > 1} - drop


def cov(target: set, text_tokens: set) -> float:
    return len(target & text_tokens) / len(target) if target else 0.0


def parse_dt(v):
    if not v:
        return None
    try:
        d = dt.datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except Exception:
        return None
    return d.replace(tzinfo=dt.timezone.utc) if d.tzinfo is None else d


# ------------------------------------------------------------------ persona join
class PersonaJoin:
    """All per-persona ground truth, resolved once against the FULL bank.

    t_now is computed from the FULL bank ONLY and stored as an explicit constant.
    It is never recomputed for the ABLATED variant -- deleting the newest active
    entries would otherwise slide the expiry cutoff and silently re-label expiry
    for reasons unrelated to the ablation.
    """

    def __init__(self, name, yaml_path, questions):
        self.name = name
        self.questions = questions
        self.y = load_yaml(yaml_path)
        bank = jload(BANKS / f"{name}.json")
        self.next_id = bank["next_id"]
        self.entries = bank["entries"]
        self.by_id = {e["id"]: e for e in self.entries}
        persona_blk = self.y.get("persona")
        self.drop = toks(persona_blk.get("name", "") if isinstance(persona_blk, dict) else "")
        self.etoks = {e["id"]: toks(e.get("text", ""), self.drop) for e in self.entries}
        self.by_session = collections.defaultdict(list)
        for e in self.entries:
            self.by_session[e.get("source_session")].append(e["id"])

        # --- t_now PINNED from the FULL bank (evaluate_lifecycle_bank.py:168-174)
        act = [parse_dt(e["created_at"]) for e in self.entries if e["is_active"]]
        act = [x for x in act if x]
        self.t_now = (max(act) + dt.timedelta(hours=24)) if act else None
        self.cutoff = (self.t_now - EXPIRY_WINDOW) if self.t_now else None

        self.reasons = collections.Counter()
        self.gold, self.fires, self.expired_neg, self.rec_of = {}, {}, {}, {}
        for q in questions:
            g, fires, exp, rec, why = self._resolve(q)
            qid = q["id"]
            self.gold[qid] = g
            self.fires[qid] = fires          # {entry_id: signal} lexical detector
            self.expired_neg[qid] = exp      # date-derived, exact, no threshold
            self.rec_of[qid] = rec
            if why:
                self.reasons[why] += 1

    # ---- Stage A: question -> YAML section record
    def _section_record(self, q):
        if q["attack_vector"] in OUT_OF_SCOPE_AV:
            return None, "A_out_of_scope_av"
        sec = AV_SECTION.get(q["attack_vector"])
        if sec is None:
            return None, "A_no_source_section"
        recs = [r for r in (self.y.get(sec) or []) if isinstance(r, dict)]
        if not recs:
            return None, "A_empty_section"
        probe = toks(" ".join([q["question"], q.get("correct_answer") or ""]
                              + list(q.get("wrong_answer_indicators") or [])), self.drop)
        scored = sorted(
            ((len(probe & toks(" ".join(str(v) for v in r.values()), self.drop)), i, r)
             for i, r in enumerate(recs)), key=lambda t: -t[0])
        if scored[0][0] == 0:
            return None, "A_zero_overlap"
        if len(scored) > 1 and scored[0][0] - scored[1][0] < MIN_MARGIN:
            return None, "A_tie"
        return (sec, scored[0][1], scored[0][2]), None

    # ---- Stage B: YAML record -> bank entry ids
    def _b1_event_date(self, rec):
        d = str(rec.get("event_date") or "")[:10]
        if not d:
            return None
        hits = {e["id"] for e in self.entries if str(e.get("event_time") or "")[:10] == d}
        return hits or None

    def _b2_session(self, fact, session):
        tf = toks(fact, self.drop)
        if len(tf) < 3:
            return None, "B_degenerate_fact"
        cands = self.by_session.get(session) or []
        if not cands:
            return None, "B_no_such_session"
        hits = {i for i in cands
                if len(tf & self.etoks[i]) >= MIN_SHARED and cov(tf, self.etoks[i]) >= TAU_GOLD}
        return (hits, None) if hits else (None, "B_no_session_anchor")

    # ---- negative-obligation detector: signal per entry, bank-wide
    def detector(self, old_fact, new_fact):
        """{entry_id: signal in [0,1]} for entries asserting the SUPERSEDED value.

        Signal is coverage of the tokens unique to the old value. Entries that
        instead assert the new value are excluded by CROSS_GUARD. Returns None
        when the two values are too similar to separate at all.
        """
        ot, nt = toks(old_fact, self.drop), toks(new_fact, self.drop)
        do, dn = ot - nt, nt - ot
        if len(do) < MIN_DISCR or len(dn) < MIN_DISCR:
            return None
        out = {}
        for i, t in self.etoks.items():
            if len(do & t) >= MIN_SHARED and cov(dn, t) < CROSS_GUARD:
                out[i] = cov(do, t)
        return out

    def is_expired(self, eid):
        d = parse_dt(self.by_id[eid].get("event_time"))
        return bool(d and self.cutoff and d < self.cutoff)

    def _resolve(self, q):
        sr, why = self._section_record(q)
        if sr is None:
            return None, None, None, None, why
        sec, ridx, rec = sr
        gf, gs, sf, ss = SECTION_FIELDS[sec]

        # gold
        if sec == "expiring_logistics":
            gold = self._b1_event_date(rec)
            if gold is None:
                gold, why = self._b2_session(rec.get(gf), rec.get(gs))
        else:
            gold, why = self._b2_session(rec.get(gf), rec.get(gs))
        if gold is None:
            return None, None, None, None, why

        # negative obligation
        fires, expired = {}, set()
        if sec == "expiring_logistics":
            expired = {i for i in gold if self.is_expired(i)}
            gold = gold - expired
        elif sf:
            d = self.detector(rec.get(sf), rec.get(gf))
            if d is None:
                return None, None, None, None, "N_weak_discriminator"
            fires = d
            if sec == "retractions":
                anchored, _ = self._b2_session(rec.get(sf), rec.get(ss))
                for i in (anchored or set()):
                    fires[i] = max(fires.get(i, 0.0), 1.0)
                for e in self.entries:
                    if e["is_retracted"] and cov(toks(rec.get(sf), self.drop),
                                                 self.etoks[e["id"]]) >= TAU_GOLD:
                        fires[e["id"]] = max(fires.get(e["id"], 0.0), 1.0)
        if not gold and not fires and not expired:
            return None, None, None, None, "B_empty_after_split"
        return gold, fires, expired, (sec, ridx), None

    # ---- the label rule
    def label(self, q, ablated, tau_lo, tau_hi):
        """One of PRESENT / ABSENT / PRESENT-NEGATIVE / UNRESOLVED, plus subtype."""
        qid = q["id"]
        if self.gold[qid] is None:
            return "UNRESOLVED", None
        surv = lambda ids: {i for i in ids if self.by_id[i]["category"] not in ablated}
        G = surv(self.gold[qid])
        exp = surv(self.expired_neg[qid] or set())
        fired = {i: s for i, s in (self.fires[qid] or {}).items()
                 if self.by_id[i]["category"] not in ablated}
        hi = {i for i, s in fired.items() if s >= tau_hi} | exp
        lo = {i for i, s in fired.items() if s >= tau_lo}

        if hi:
            # with-replacement iff the current value also survives in the variant
            return "PRESENT-NEGATIVE", ("with-replacement" if G else "without-replacement")
        if lo:
            # signal strictly between the thresholds: cannot settle either way
            return "UNRESOLVED", "between-thresholds"
        return ("PRESENT", None) if G else ("ABSENT", None)

    def census(self, ablated, tau_lo, tau_hi):
        c = collections.Counter()
        for q in self.questions:
            for v in (frozenset(), ablated):
                c[self.label(q, v, tau_lo, tau_hi)[0]] += 1
        return c


# ------------------------------------------------------------------- assembly
def load_joins():
    qs = jload(QUESTIONS)
    byp = collections.defaultdict(list)
    for q in qs:
        byp[q["persona"]].append(q)
    ypaths = {p.name.replace(".yaml", "").split("_")[-1]: p
              for p in sorted(LME.glob("*/persona_*.yaml"))}
    return {n: PersonaJoin(n, ypaths[n], ql) for n, ql in sorted(byp.items())}


def best_ablation(J, tau_lo, tau_hi, kmax=3):
    """Per persona: the k<=kmax category set maximising ABSENT, then PRESENT-NEGATIVE.

    Deterministic. Ties broken by (more PRESENT, fewer categories, alphabetical),
    so the choice does not depend on dict or iteration order.
    """
    cand = []
    for k in range(2, kmax + 1):
        for combo in itertools.combinations(CATEGORIES, k):
            c = J.census(frozenset(combo), tau_lo, tau_hi)
            cand.append((-c["ABSENT"], -c["PRESENT-NEGATIVE"], -c["PRESENT"],
                         len(combo), combo, c))
    cand.sort()
    return cand[0][4], cand[0][5]


def select_personas(best, n):
    """Greedy then local search, maximising (smallest cell, total scoreable).

    Fully deterministic: candidates are scanned in sorted name order and only a
    strict improvement is accepted, so no seed is required.
    """
    def totals(sel):
        t = collections.Counter()
        for x in sel:
            t.update(best[x][1])
        return t

    def score(t):
        return (min(t["PRESENT"], t["ABSENT"], t["PRESENT-NEGATIVE"]),
                t["PRESENT"] + t["ABSENT"] + t["PRESENT-NEGATIVE"])

    sel, pool = [], sorted(best)
    while len(sel) < n and pool:
        c = max(pool, key=lambda x: (score(totals(sel + [x])), [-ord(ch) for ch in x]))
        sel.append(c); pool.remove(c)
    improved = True
    while improved:
        improved = False
        for i in range(len(sel)):
            for x in sorted(pool):
                trial = sel[:i] + [x] + sel[i + 1:]
                if score(totals(trial)) > score(totals(sel)):
                    pool.append(sel[i]); pool.remove(x); sel = trial
                    improved = True
                    break
            if improved:
                break
    return sorted(sel), totals(sel)
