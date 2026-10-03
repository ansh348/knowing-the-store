"""
e3_common.py -- the snapshot, the label rule at t, the annotation, and the scramble.

NO API CALLS. Executes PREREG_E3.md; makes no design decisions.

Everything E3 reads is a committed E1/E2/LifeMemEval artifact. Nothing here
re-ingests, relabels or re-renders anything outside E3's own write scope.

FOUR THINGS LIVE HERE AND NOWHERE ELSE.

  1. SNAPSHOT           alive(persona, rung) = {e : source_session(e) <= rung}
                        plus the RUNG-CORRECT believed lifecycle state, which is
                        NOT the bank's own is_active (D51-E3).
  2. LABEL AT t         E1's PersonaJoin.label with the three PREREG_E3 section 3
                        changes: session survival, moving expiry cutoff, and the
                        D47 event-activation predicate.
  3. ANNOTATION         the per-fact lifecycle tag rendered into S3 (D49-E3).
  4. SCRAMBLE           the marginal-preserving frozen permutation of S3 -> S3'.

Cost model is D44-corrected: gpt-5.4 $2.50/$15.00, gpt-4.1-mini $0.40/$1.60.

Usage: imported. Running it prints the registered-cell census.
"""

from __future__ import annotations

import collections
import datetime as dt
import hashlib
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"
E2 = ROOT / "e2_metamemory"
E3 = ROOT / "e3_metamemory"
LME = ROOT / "LifeMemEval"
BANKS = LME / "artifacts" / "lifecycle_banks"

sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(E2 / "tools"))

from e0_common import EXPIRY_WINDOW, parse_dt   # noqa: E402

# --------------------------------------------------------------- frozen design
RUNGS = (14, 20, 24, 32)                 # PREREG_E3 section 1
N_SESSIONS = 35
SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}
TAU_LO, TAU_HI = 0.20, 0.80              # build_e1.py, unchanged
SEED = 42

# the four context states, and no more (PREREG_E3 section 4.2)
S0 = "S0-nofacts"
S1 = "S1-facts"
S2 = "S2-facts-caution"                  # E2's S2, byte-identical
S3 = "S3-facts-caution-annotated"
S3P = "S3p-facts-caution-scrambled"

# resolving-side session field per YAML section (D47 event activation)
RESOLVING_FIELD = {
    "supersession_events": "new_session",
    "contradictions":      "new_session",
    "retractions":         "retraction_session",
    "expiring_logistics":  None,          # time-driven, not write-driven
    "stable_identity":     None,
    "ambiguous":           None,          # never resolves, by design
}
# field whose session makes the AUTHORED answer key valid (PREREG_E3 section 2)
KEY_FIELD = {
    "supersession_events": "new_session",
    "contradictions":      "new_session",
    "retractions":         "retraction_session",
    "ambiguous":           "tentative_session",
    "stable_identity":     None,          # always valid
    "expiring_logistics":  None,          # handled by event_date vs t_now
}

# ---- the annotation vocabulary. `[retracted]` is deliberately absent: the
# store's is_retracted flag carries no date, so a rung-correct believed
# retraction is not derivable from store-own fields (PREREG_E3 section 4.3).
ANN_ACTIVE, ANN_SUPERSEDED, ANN_EXPIRED = "[active]", "[superseded]", "[expired]"

ANNOTATION_NOTE = (
    " Each fact is tagged with what the store believes about its lifecycle "
    "state: [active], [superseded] (a later value for it exists), or [expired] "
    "(its date has passed).")

# E3_AMENDMENT_1 section 2.4, frozen. Appended in S3/S3' and nowhere else.
DIGEST_NOTE = (
    " Below the facts is a record of what the store believes it holds in "
    "superseded form -- how many such entries there are, in which categories, "
    "and which attribute names carry them. Facts you have been given on those "
    "attributes are the ones most likely to be out of date.")


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True, default=float)
        f.write("\n")


def sha(*parts) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(str(p).encode("utf-8"))
        h.update(b"\x1f")
    return h.hexdigest()


def as_int(v):
    if v is None:
        return None
    if isinstance(v, int):
        return v
    m = re.search(r"\d+", str(v))
    return int(m.group()) if m else None


# ------------------------------------------------------------------ session map
def session_dates():
    """persona -> {session_id: 'YYYY-MM-DD'}, read from the session files."""
    out = {}
    for ypath in sorted(LME.glob("*/persona_*.yaml")):
        name = ypath.name.replace(".yaml", "").split("_")[-1]
        d = {}
        for f in sorted((ypath.parent / "sessions").glob("session_*.json")):
            j = jload(f)
            d[int(j["session_id"])] = str(j["date"])
        out[name] = d
    return out


def assert_replay_order(dates):
    """PREREG_E3 section 1 assertion 1. Ordering is by session_id, never date."""
    for p, d in sorted(dates.items()):
        ids = sorted(d)
        assert ids == list(range(1, N_SESSIONS + 1)), \
            f"{p}: session ids not contiguous 1..{N_SESSIONS}"
    return True


# ---------------------------------------------------------------- the snapshot
class Snapshot:
    """One persona's store, replayed. Rung-correct believed lifecycle state.

    D51-E3. The bank's own `is_active` records the store's FINAL state: an entry
    superseded at session 30 carries is_active=False in the committed bank, so a
    snapshot that reuses it would treat that entry as superseded at rung 14 --
    future information leaking backwards into a past store. The rung-correct
    rule uses the `supersedes` POINTER, which lives on the NEWER entry and
    therefore carries a source_session:

        superseded_at(e, s)  iff  exists e' with source_session(e') <= s
                                  and e'.supersedes == e.id

    All 5,725 pointers in the corpus resolve within their own bank.
    """

    def __init__(self, persona, dates):
        self.persona = persona
        self.dates = dates
        self.entries = jload(BANKS / f"{persona}.json")["entries"]
        self.by_id = {e["id"]: e for e in self.entries}
        self.sess = {e["id"]: int(e.get("source_session") or 0) for e in self.entries}
        # newer -> older pointer, inverted: older -> [session of each superseder]
        self.superseded_by = collections.defaultdict(list)
        for e in self.entries:
            tgt = e.get("supersedes")
            if tgt:
                assert tgt in self.by_id, f"{persona}: dangling supersedes {tgt}"
                self.superseded_by[tgt].append(self.sess[e["id"]])

    def t_now(self, rung):
        return parse_dt(self.dates[rung]) + dt.timedelta(hours=24)

    def cutoff(self, rung):
        return self.t_now(rung) - EXPIRY_WINDOW

    def alive(self, rung):
        return {i for i, s in self.sess.items() if s <= rung}

    def is_superseded_at(self, eid, rung):
        return any(s <= rung for s in self.superseded_by.get(eid, ()))

    def is_expired_at(self, eid, rung):
        d = parse_dt(self.by_id[eid].get("event_time"))
        return bool(d is not None and d < self.cutoff(rung))

    def is_active_at(self, eid, rung):
        e = self.by_id[eid]
        return not (e["is_retracted"] or self.is_superseded_at(eid, rung))

    def annotate(self, eid, rung):
        """PREREG_E3 section 4.3 precedence: expired > superseded > active."""
        if self.is_expired_at(eid, rung):
            return ANN_EXPIRED
        if self.is_superseded_at(eid, rung):
            return ANN_SUPERSEDED
        return ANN_ACTIVE


# ------------------------------------------------------------ the label at t
INTENTS = {r["id"]: r["intent"]
           for r in jload(E1 / "intents.json")}
NEG_ELIGIBLE = {"CURRENT-STATE", "UPCOMING"}          # build_e1.py:42, verbatim
IN_SCOPE = NEG_ELIGIBLE | {"PAST-EVENT", "CHANGE-AWARE"}


class LabelAtT:
    """E1's label rule, re-anchored on a rung.

    Two layers, exactly as E1 has them:
      JOIN LAYER   e0_common.PersonaJoin.label -- gold/fires/expired sets and the
                   tau_lo / tau_hi bands.
      BUILD LAYER  build_e1.label -- the INTENT GATE (D52-E3). PAST-EVENT and
                   CHANGE-AWARE questions cannot carry a negative obligation at
                   all, and for PAST-EVENT expired content is folded back into
                   gold rather than being an obligation.

    Plus the three E3 changes (PREREG_E3 section 3): session survival, a moving
    expiry cutoff, and the D47 event-activation predicate.
    """

    def __init__(self, join, snap):
        self.J = join
        self.snap = snap
        self._rec = {}

    def record(self, qid):
        if qid in self._rec:
            return self._rec[qid]
        r = self.J.rec_of.get(qid)
        out = (None, None)
        if r:
            sec, ridx = r
            recs = [x for x in (self.J.y.get(sec) or []) if isinstance(x, dict)]
            out = (sec, recs[ridx])
        self._rec[qid] = out
        return out

    def resolving_session(self, qid):
        sec, rec = self.record(qid)
        if sec is None:
            return None
        f = RESOLVING_FIELD.get(sec)
        return as_int(rec.get(f)) if f else None

    def key_valid(self, qid, rung):
        """PREREG_E3 section 2. Probes and unresolved questions are always valid."""
        sec, rec = self.record(qid)
        if sec is None:
            return True
        f = KEY_FIELD.get(sec)
        if f:
            ke = as_int(rec.get(f))
            return ke is None or rung >= ke
        if sec == "expiring_logistics":
            ed = parse_dt(str(rec.get("event_date") or "") or None)
            tn = self.snap.t_now(rung)
            return not (ed is not None and tn is not None and tn < ed)
        return True

    def label(self, qid, rung):
        """(label, subtype, evidence). PN-CANDIDATE is pre-verification, as in E1."""
        intent = INTENTS[qid]
        ev = {"rung": rung, "intent": intent, "hi": []}
        if intent not in IN_SCOPE:
            return "OUT-OF-SCOPE", None, ev
        if self.J.gold.get(qid) is None:
            return "UNRESOLVED", "join-unresolved", ev
        A = self.snap.alive(rung)
        sec, _rec = self.record(qid)
        G = {i for i in self.J.gold[qid] if i in A}
        fired = {i: v for i, v in (self.J.fires[qid] or {}).items() if i in A}
        exp = set()
        if sec == "expiring_logistics":
            cand = ({i for i in (self.J.expired_neg[qid] or set())} | G) & A
            exp = {i for i in cand if self.snap.is_expired_at(i, rung)}
            G = G - exp
        rs = self.resolving_session(qid)
        ev.update({"section": sec, "resolving_session": rs,
                   "n_fired": len(fired), "n_expired": len(exp)})

        # ---- D47: before the resolving event there is no obligation, and the
        # entries asserting the OLD value are the gold ones.
        if rs is not None and rung < rs:
            hi_pre = sorted(i for i, v in fired.items() if v >= TAU_HI)
            ev.update({"pre_event": True, "n_old_side": len(hi_pre),
                       "n_gold": len(hi_pre)})
            return ("PRESENT" if hi_pre else "ABSENT"), "pre-event", ev
        ev["pre_event"] = False

        # ---- BUILD LAYER: the intent gate (build_e1.label, verbatim)
        if intent in ("PAST-EVENT", "CHANGE-AWARE"):
            hi, lo = set(), set()
            if intent == "PAST-EVENT":
                G = G | exp                  # expired content is PRESENT here
        else:
            hi = {i for i, v in fired.items() if v >= TAU_HI} | exp
            lo = {i for i, v in fired.items() if v >= TAU_LO}
        ev["n_gold"] = len(G)
        ev["hi"] = sorted(hi)

        if hi:
            return "PN-CANDIDATE", ("with-replacement" if G else
                                    "without-replacement"), ev
        if lo:
            return "UNRESOLVED", "between-thresholds", ev
        return ("PRESENT" if G else "ABSENT"), None, ev


def apply_verdicts(lab, sub, ev, persona, qid, membership, semantic):
    """E1's hand verdicts, applied exactly as verify_e1.cmd_apply does.

    Detector proposes, hand verdict disposes. A PN candidate survives only if the
    SEMANTIC verdict says the question carries an obligation under its intent AND
    at least one entry in `hi` has a MEMBER membership verdict. A demoted
    candidate becomes UNRESOLVED -- never PRESENT or ABSENT, which would silently
    move it into a scoreable cell.
    """
    if lab != "PN-CANDIDATE":
        return lab, sub, []
    if semantic.get((persona, qid), (None,))[0] != "OBLIGATION":
        return "UNRESOLVED", "semantic-not-an-obligation", []
    surviving = [i for i in ev["hi"]
                 if membership.get((persona, qid, i), (None,))[0] == "MEMBER"]
    if surviving:
        return "PRESENT-NEGATIVE", sub, surviving
    return "UNRESOLVED", "no-member-survived", []


# ------------------------------------------------------------------- the scramble
def scramble_map(pairs, persona, rung):
    """PREREG_E3 section 4.4. Marginal-preserving frozen permutation.

    pairs: [(item_id, fact_position, annotation)] in ascending (item_id, pos).
    Returns {(item_id, pos): scrambled_annotation} and the destruction rate.
    """
    import numpy as np
    pairs = sorted(pairs, key=lambda t: (t[0], t[1]))
    ann = [p[2] for p in pairs]
    if not ann:
        return {}, 0.0
    seed = int(sha("E3-LOBOTOMY", persona, rung)[:16], 16)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(ann))
    out = {(pairs[i][0], pairs[i][1]): ann[int(perm[i])] for i in range(len(ann))}
    changed = sum(1 for i in range(len(ann)) if ann[i] != ann[int(perm[i])])
    return out, changed / len(ann)


# ------------------------------------------------------------- answer prompts
def _e2_prompts():
    from e2_common import (CAUTION_INSTRUCTION, GENERATION_SYSTEM_PROMPT,  # noqa: PLC0415
                           NO_FACTS)
    return GENERATION_SYSTEM_PROMPT, CAUTION_INSTRUCTION, NO_FACTS


def answer_messages(facts, annotations, digest, question, state):
    """The five states.

    S0/S1/S2 are E2's, byte-identical. S3 adds the per-fact lifecycle tag
    (PREREG_E3 4.3) AND the store supersession digest (E3_AMENDMENT_1 2.4).
    S3' is S3 with the DIGEST scrambled and nothing else changed.
    """
    GEN, CAUTION, NOFACTS = _e2_prompts()
    if state in (S3, S3P):
        assert annotations is not None and len(annotations) == len(facts)
        assert digest is not None
        body = "\n".join(f"{i+1}. {a} {f}"
                         for i, (f, a) in enumerate(zip(facts, annotations)))
    else:
        body = "\n".join(f"{i+1}. {f}" for i, f in enumerate(facts))
    facts_block = body if facts else NOFACTS
    sysmsg = GEN
    if state in (S2, S3, S3P):
        sysmsg += CAUTION
    if state in (S3, S3P):
        sysmsg += ANNOTATION_NOTE + DIGEST_NOTE
    user = f"Here are the facts I know about you:\n\n{facts_block}\n\n"
    if state in (S3, S3P):
        user += f"{digest}\n\n"
    return [{"role": "system", "content": sysmsg},
            {"role": "user", "content": user + f"Question: {question}"}]


# ---------------------------------------------------------------- cost model
# D44-corrected, verified 2026-08-11 from developers.openai.com/api/docs/pricing.
PRICE = {"gpt-4.1-mini": (0.40, 1.60), "gpt-5.4": (2.50, 15.00)}


def usd(tin, tout, model):
    pi, po = PRICE[model]
    return tin / 1e6 * pi + tout / 1e6 * po


# ------------------------------------------------------------------- the cells
def load_cells():
    """The registered (item, rung) cells. Reads CELLS_E3.json; build_cells writes it."""
    return jload(E3 / "CELLS_E3.json")


def main():
    c = load_cells()
    print(f"registered cells: {c['n_cells']}  rungs {c['rungs']}")
    for r in c["rungs"]:
        rows = [x for x in c["cells"] if x["rung"] == r]
        lab = collections.Counter(x["label"] for x in rows)
        sp = collections.Counter(x["split"] for x in rows)
        print(f"  rung {r:2d}: n={len(rows):4d}  {dict(sp)}  {dict(lab)}")


if __name__ == "__main__":
    main()
