# STOP POINT 2 — RE-EVALUATED · ALL FOUR CHECKLIST ITEMS PASS

Committed at the moment of pass-through, per instruction. **No elicitation call has been made at
the time of this evaluation.** E1 spend to date **≈ $0.10**, all construction-side.

**Authorization:** the conditional GO stands as issued — **pre-census, conditional, logged**. It
narrows discretion; it does not waive the stop. All four items are now mechanically verified.

---

## The checklist

| # | check | result |
|---|---|---|
| 1 | every gate-relevant cell ≥ 50 on the hard tier, per backend | **PASS** — frbank 272, mem0 136, amem 145 |
| 2 | ladder clean (0/30, no unresolved D18) for every (backend, provenance) | **PASS** — 6/6 cells 0/30, 0 triggers |
| 3 | PN cell intact; edge cases tagged-only; no frozen rule extended | **PASS** — 104 PN, 6 edge cases tagged |
| 4 | cost projection under $35; no standing stop condition fired | **PASS** — ~$0.10 spent, ~$2.50 projected |

### 1 — hard tier

| backend | hard ABSENT | slot | natural | ≥50 |
|---|---|---|---|---|
| FR-Bank | **272** | 127 | 145 | PASS |
| Mem0 | **136** | — | 136 | PASS |
| A-MEM | **145** | — | 145 | PASS |

**All 145 probes verified ABSENT; 0 routed to UNRESOLVED.** 142 returned zero hits on every
content term and are verified by their transcripts; 3 produced a ≥2-term co-occurrence and were
read individually — all three generic co-occurrence on unrelated content (`attended`+`meeting` on
a municipal heritage meeting, not a book club; `brand`+`preferred` on Bonsoy oat milk, not running
shoes; `favorite`+`meal` on another person's birthday meal). Mem0's 136 excludes the probes of its
three dropped personas. Full table: `PROBE_VERIFICATION.md`.

### 2 — leakage ladder, level 0

| backend | provenance | correct | verdict | D18 |
|---|---|---|---|---|
| frbank | TRUE / BELIEVED | 0/30 · 0/30 | PASS | no |
| mem0 | TRUE / BELIEVED | 0/30 · 0/30 | PASS | no |
| amem | TRUE / BELIEVED | 0/30 · 0/30 | PASS | no |

Every cell sits 3 items clear of the nearest D18 trigger band {2,3}. 180 calls, $0.0463. The same
30 items run under both provenances, so TRUE-vs-BELIEVED is paired.

**One caveat recorded rather than buried:** Mem0 and A-MEM returned literal `UNKNOWN` on 60/60
each. Their indexes are 31 lines of which most are the inexpressibility marker, so a floor of 0
there is close to structurally guaranteed and is **weaker evidence of a well-scrubbed renderer
than FR-Bank's 0/60 across a 60-line index**. The single non-UNKNOWN response in the whole ladder
(`valentina_q13`, both frbank cells) named attribute *names* — "event, important_meeting_date,
meeting_date" — with no date and no event name. That is the scrubber working exactly as designed.

### 3 — PN cell

104 PRESENT-NEGATIVE from 122 candidates; 18 → UNRESOLVED. 248 judgments read individually.
13 membership exclusions: 7 under the named patterns, **6 outside them, all tagged, none folded
into the criterion** (`MEMBERSHIP_EDGE_CASES.md`). No frozen rule was interpreted or extended.

### 4 — cost

Spend ≈$0.10 (ladder $0.046, probe drafting $0.039, embeddings ≈$0.01, Phase-0 $0.001).
Projection ~$2.50 against the $35 gate. No standing stop condition fired.

---

## Final census

| backend | variant | PRESENT | ABSENT | PRESENT-NEG | UNRESOLVED |
|---|---|---|---|---|---|
| frbank | FULL | 131 | 145 | 47 | 235 |
| frbank | CAT-ABLATED | 43 | 111 | 22 | 237 |
| **frbank** | **SLOT-ABLATED** | 0 | **127** | 35 | 39 |
| mem0 | FULL | 94 | 144 ᵋ | 0 | 280 |
| amem | FULL | 126 | 158 ᵋ | 0 | 274 |

**1,183 scoreable items.** ᵋ external ABSENT of the `ingestion-loss-attributed` and
`sweep-negative` subtypes carries **ε = 0.005**; the `natural` subtype does not, being
YAML-verified rather than sweep-inferred.

PN 104, all FR-Bank — the registered believed-state finding that PN structurally converges to
ABSENT on erase-mode stores.

## Build-instrument deviation: `recency_time` (documented per instruction)

The index renderer originally took entry age from `ingest_time`. On FR-Bank that is `created_at`,
the LifecycleBench **session date** — correct. On Mem0 and A-MEM it is the **ingest wall-clock**:
a single afternoon in 2026-05 for the entire corpus.

**What that would have done.** Ages are measured against a per-persona `t_now` pinned from the
FULL FR-Bank bank, a session date in 2026-02..2026-05. Every Mem0 and A-MEM entry would have
reported an age of roughly zero — a constant. `newest`, `oldest`, `median` and the entire age
distribution would have collapsed to one value per backend. **A-MEM's believed index is counts and
recency and nothing else**, so recency collapsing to a constant would have reduced it to a bare
entry count — and the pre-registered lifecycle-ablation decomposition, which reads exactly the
count-and-recency structure A-MEM uniquely isolates, would have measured a degenerate cell and
reported it as a finding about lifecycle signal. An instrument error would have been published as
a result.

**The fix.** `backends.py` gained a normalized `recency_time` carrying each store's own *content*
date — FR-Bank `created_at`, Mem0 payload `date`, A-MEM `timestamp`, all the session date — plus
`believed_supersedes` for FR-Bank's supersession-event count. Additive; every pre-existing field
verified byte-identical after the cache rebuild (18,936 / 10,074 / 11,319 unchanged).

## Index v2

716 indexes over (backend, variant, provenance). Assertions all pass: no `:` in any of 4,712
scrubbed attribute names; 656 field-checks confirm every inexpressible field emits the marker and
never a digit; count 716 = 40×2 FULL + 40×2 CAT + 201×2 SLOT + 37×2 mem0 + 40×2 amem.
Cross-check against frozen numbers reproduces FR-Bank believed superseded 5,968, retracted 31,
events 5,725, and the ~60× overstatement against TRUE's 104.

## Probe cluster-size distribution

279 drafted, 145 survived (52%), **145/145 verified**. Per persona: 6→2, 5→7, 4→12, 3→14, 2→4,
0→1. A uniform second round remains available and is not run; if ever drafted, the drafter must
not be shown round-one outcomes.

---

## VERDICT: all four pass. Proceeding to Phase C, then Phase D, per the frozen plan.
