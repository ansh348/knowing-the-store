"""
feasibility.py -- E0 metamemory probe, Step 1 feasibility analysis.

NO API CALLS. Read-only over LifecycleBench assets. Written BEFORE pre-registration
because it produces no scoreable observation -- it only measures whether the
pre-registered design is constructible at the prescribed scale.

Question under test: for a choice of N personas and a per-persona ablation of k
behavioral categories, how large are the three label cells (PRESENT, ABSENT,
PRESENT-NEGATIVE) under a strictly deterministic labelling rule, and how many
(question, variant) pairs fall to UNRESOLVED?

Label rule (verbatim from the E0 prompt):
  ABSENT           every gold supporting edge for the question is missing from the
                   variant AND no superseded/retracted/expired content bearing on
                   the question remains in the variant.
  PRESENT-NEGATIVE the variant contains superseded / retracted / expired content
                   bearing on the question. Takes precedence over PRESENT.
  PRESENT          licensed gold supporting content present, no negative obligation.
  UNRESOLVED       the join cannot settle it. Here: the question has no resolvable
                   gold edge anywhere in the FULL bank, so "all gold edges are
                   missing" is unfalsifiable and ABSENT cannot be established.

LifecycleBench has NO per-question gold-edge annotation -- the project states this
itself (analysis/ontology_validation/noise_study/pkwc_q2_common.py:26-30,
MEMAUDIT_EVIDENCE_REPORT.md:252-255). Three substitutes exist, and this script
measures the design under each so the choice is made on numbers, not taste:

  LEX    exp4_witnesses.supports_correct scanned over the WHOLE bank.
         Exhaustive over the bank; documented false negatives on morphology.
  JUDGE  LifeMemEval/artifacts/fr_bank_judge_cache.json inverted on
         (question_id, edge_uuid). Claude-judged per candidate. High precision,
         but RETRIEVAL-CONDITIONED: only edges some FR-Bank run ranked top-10 were
         ever judged, so its recall over the bank is unknown and certainly < 1.
  UNION  LEX | JUDGE. The only variant that is SOUND for ABSENT: over-approximating
         the gold set can only make "no gold survives the ablation" harder to
         satisfy, never easier, so an ABSENT label issued under UNION also holds
         under either component rule.

Run:  python e0_metamemory/tools/feasibility.py
"""

from __future__ import annotations

import collections
import csv
import datetime as dt
import io
import itertools
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "analysis" / "ontology_validation"))

from exp4_witnesses import supports_correct, supports_wrong  # noqa: E402

QUESTIONS = PROJECT_ROOT / "LifeMemEval" / "lifemembench_questions.json"
BANKS = PROJECT_ROOT / "LifeMemEval" / "artifacts" / "lifecycle_banks"
JUDGE_CACHE = PROJECT_ROOT / "LifeMemEval" / "artifacts" / "fr_bank_judge_cache.json"
AV7_DIR = PROJECT_ROOT / "audit" / "postreview_prep" / "av7_reconciliation"
AV2_GOLD = PROJECT_ROOT / "audit" / "e3_attribution" / "gold_expired_facts.json"

# Reference "now" for expiry. The benchmark timeline runs Jan 2025 - Jun 2026
# (session_plan.time_span), so a reference just after the last session makes every
# in-timeline dated event decidable. Declared in advance, not tuned.
REF_NOW = dt.datetime(2026, 7, 1, tzinfo=dt.timezone.utc)

CATEGORIES = [
    "PROJECTS_ENDEAVORS", "RELATIONAL_BONDS", "OBLIGATIONS", "HOBBIES_RECREATION",
    "LOGISTICAL_CONTEXT", "HEALTH_WELLBEING", "IDENTITY_SELF_CONCEPT",
    "PREFERENCES_HABITS", "INTELLECTUAL_INTERESTS", "FINANCIAL_MATERIAL", "OTHER",
]


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def is_expired(entry) -> bool:
    v = entry.get("event_time")
    if not v:
        return False
    try:
        d = dt.datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except Exception:
        return False
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d < REF_NOW


def load_judge_cache():
    """(question_id -> supports_correct ids), (question_id -> wrong-indicator ids)."""
    pos, wrong = collections.defaultdict(set), collections.defaultdict(set)
    for v in jload(JUDGE_CACHE).values():
        if not (isinstance(v, dict) and "question_id" in v and "edge_uuid" in v):
            continue
        if v.get("supports_correct"):
            pos[v["question_id"]].add(v["edge_uuid"])
        if v.get("contains_wrong_indicator"):
            wrong[v["question_id"]].add(v["edge_uuid"])
    return pos, wrong


def load_av7_edges():
    """Hand-audited AV7 leak edges, per persona (attribution != SPURIOUS)."""
    edges = collections.defaultdict(set)
    for r in csv.DictReader(io.open(AV7_DIR / "av7_edge_attribution.csv", encoding="utf-8")):
        if (r.get("attribution") or "").strip().upper() != "SPURIOUS":
            edges[r["persona"]].add(r["edge_id"])
    return edges


def load_av2_gold():
    """Curated AV2 gold-expired ids per question. Self-declared provisional."""
    out = {}
    for r in jload(AV2_GOLD)["labels"]:
        out[r["question_id"]] = set(r.get("gold_expired_ids") or [])
    return out


class Persona:
    def __init__(self, name, questions, jpos, jwrong, av7_edges, av2_gold, gold_mode):
        self.name = name
        self.questions = questions
        self.entries = jload(BANKS / f"{name}.json")["entries"]
        self.by_id = {e["id"]: e for e in self.entries}
        self.gold, self.neg = {}, {}
        for q in questions:
            qid = q["id"]
            lex = {e["id"] for e in self.entries
                   if supports_correct(e.get("text", ""), q.get("correct_answer", ""))}
            jud = {i for i in jpos.get(qid, set()) if i in self.by_id}
            self.gold[qid] = {"LEX": lex, "JUDGE": jud, "UNION": lex | jud}[gold_mode]

            wrong = {e["id"] for e in self.entries
                     if supports_wrong(e.get("text", ""), q.get("wrong_answer_indicators"))}
            wrong |= {i for i in jwrong.get(qid, set()) if i in self.by_id}
            neg = {i for i in wrong
                   if (not self.by_id[i]["is_active"])
                   or is_expired(self.by_id[i])
                   or self.by_id[i]["is_retracted"]}
            if q["attack_vector"] == "AV7_selective_forgetting":
                neg |= {i for i in av7_edges.get(name, set()) if i in self.by_id}
            neg |= {i for i in av2_gold.get(qid, set()) if i in self.by_id}
            self.neg[qid] = neg

    def cat(self, eid):
        return self.by_id[eid]["category"]

    def label(self, q, ablated):
        qid = q["id"]
        if not self.gold[qid]:
            return "UNRESOLVED", None
        gold = {i for i in self.gold[qid] if self.cat(i) not in ablated}
        neg = {i for i in self.neg[qid] if self.cat(i) not in ablated}
        if neg:
            return "PRESENT-NEGATIVE", ("with-replacement" if gold else "without-replacement")
        if not gold:
            return "ABSENT", None
        return "PRESENT", None

    def census(self, ablated):
        c = collections.Counter()
        for q in self.questions:
            for variant in (frozenset(), ablated):
                c[self.label(q, variant)[0]] += 1
        return c


def build(gold_mode):
    qs = jload(QUESTIONS)
    jpos, jwrong = load_judge_cache()
    av7, av2 = load_av7_edges(), load_av2_gold()
    byp = collections.defaultdict(list)
    for q in qs:
        byp[q["persona"]].append(q)
    return {p: Persona(p, ql, jpos, jwrong, av7, av2, gold_mode) for p, ql in sorted(byp.items())}


def best_ablation(personas, kmax):
    """Per persona: the k<=kmax ablation maximising ABSENT, tie-break PRESENT-NEGATIVE."""
    best = {}
    for name, P in personas.items():
        cand = []
        for k in range(2, kmax + 1):
            for combo in itertools.combinations(CATEGORIES, k):
                c = P.census(frozenset(combo))
                cand.append((c["ABSENT"], c["PRESENT-NEGATIVE"], c["PRESENT"], combo, c))
        cand.sort(key=lambda t: (-t[0], -t[1], -t[2], len(t[3])))
        best[name] = cand[0]
    return best


def pick(best, n):
    """Greedy + local search over persona subsets, maximising the smallest cell."""
    def totals(sel):
        t = collections.Counter()
        for x in sel:
            t.update(best[x][4])
        return t

    def score(t):
        return (min(t["PRESENT"], t["ABSENT"], t["PRESENT-NEGATIVE"]),
                t["PRESENT"] + t["ABSENT"] + t["PRESENT-NEGATIVE"])

    sel, pool = [], list(best)
    while len(sel) < n:
        c = max(pool, key=lambda x: score(totals(sel + [x])))
        sel.append(c); pool.remove(c)
    improved = True
    while improved:
        improved = False
        for i in range(len(sel)):
            for x in list(pool):
                trial = sel[:i] + [x] + sel[i + 1:]
                if score(totals(trial)) > score(totals(sel)):
                    pool.append(sel[i]); pool.remove(x); sel = trial; improved = True
                    break
    return sorted(sel), totals(sel)


def report(tag, best, sel, t):
    tot = t["PRESENT"] + t["ABSENT"] + t["PRESENT-NEGATIVE"]
    caps = []
    for cell in ("PRESENT", "ABSENT", "PRESENT-NEGATIVE"):
        worst = max(best[n][4][cell] for n in sel) if sel else 0
        caps.append(worst / t[cell] if t[cell] else 0.0)
    mincell = min(t["PRESENT"], t["ABSENT"], t["PRESENT-NEGATIVE"])
    comp = (f"{t['PRESENT']/tot:.0%}/{t['ABSENT']/tot:.0%}/{t['PRESENT-NEGATIVE']/tot:.0%}"
            if tot else "-")
    print(f"  {tag:34s} PRES={t['PRESENT']:4d} ABS={t['ABSENT']:4d} PNEG={t['PRESENT-NEGATIVE']:4d} "
          f"UNRES={t['UNRESOLVED']:4d} | n={tot:4d} min={mincell:3d} "
          f"{'PASS' if mincell >= 60 else 'FAIL'} | {comp:12s} | maxshare={max(caps):.0%}")
    return mincell, tot


def main():
    print("=" * 128)
    print("E0 FEASIBILITY -- cells over BOTH variants; 'min>=60' is the pre-registered floor; "
          "target composition 40/35/25")
    print("=" * 128)

    cache = {}
    for gold_mode in ("LEX", "JUDGE", "UNION"):
        personas = build(gold_mode)
        cache[gold_mode] = personas
        print(f"\n--- gold rule = {gold_mode} "
              f"(questions with a resolvable gold set: "
              f"{sum(1 for P in personas.values() for q in P.questions if P.gold[q['id']])}/516)")
        for kmax in (3, 5):
            best = best_ablation(personas, kmax)
            for n in (10, 20, 40):
                sel, t = pick(best, n)
                report(f"k<={kmax}, {n} personas", best, sel, t)

    # ---- detail for the single most defensible configuration
    print()
    print("=" * 128)
    print("DETAIL -- gold rule UNION (sound for ABSENT), k<=3, all 40 personas")
    print("=" * 128)
    personas = cache["UNION"]
    best = best_ablation(personas, 3)
    sel, t = pick(best, 40)
    print(f"{'persona':12s} {'PRES':>5s} {'ABS':>4s} {'PNEG':>5s} {'UNRES':>6s}  ablated categories")
    for n in sel:
        c = best[n][4]
        print(f"{n:12s} {c['PRESENT']:5d} {c['ABSENT']:4d} {c['PRESENT-NEGATIVE']:5d} "
              f"{c['UNRESOLVED']:6d}  {', '.join(best[n][3])}")
    tot = t["PRESENT"] + t["ABSENT"] + t["PRESENT-NEGATIVE"]
    print(f"\n  CELLS  PRESENT={t['PRESENT']}  ABSENT={t['ABSENT']}  "
          f"PRESENT-NEGATIVE={t['PRESENT-NEGATIVE']}  UNRESOLVED={t['UNRESOLVED']}")
    print(f"  scoreable = {tot};  UNRESOLVED = {t['UNRESOLVED']/(tot+t['UNRESOLVED']):.1%} of all pairs")
    for cell in ("PRESENT", "ABSENT", "PRESENT-NEGATIVE"):
        worst = max(best[n][4][cell] for n in sel)
        print(f"  max single-persona share of {cell:16s} = {worst/t[cell]:.1%} "
              f"[{'OK' if worst/t[cell] <= 0.15 else 'VIOLATES 15% cap'}]")


if __name__ == "__main__":
    main()
