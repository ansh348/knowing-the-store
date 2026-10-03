# AMENDMENT 1 to PREREG_E1.md

**Dated:** 2026-08-10 · **Amends:** `PREREG_E1.md` frozen at `875f726`, preserved unchanged.
**Design basis:** `E1_DESIGN.md` v0.2 (sha256 `c9ca79e8…`) and the Phase-B.1 checkpoint (`1cc15bc`).

**Statement of prior data contact.** **No elicitation call has been made.** Total E1 spend is
$0.0009, both calls construction-side in the Phase-0 probe pipeline. No FOK, NOK,
`nok_candidates_found` or `would_search` value has been observed from any model on any E1 item.
The measurements this amendment ratifies are label-construction measurements over frozen stores.

---

## 1. The lexical sweep control, recorded

The lexical presence sweep that gates PRESENT on external backends was tested against **FR-Bank
FULL**, restricted to the 201 in-scope questions the YAML join establishes *are* answerable there:

| | |
|---|---|
| questions with YAML-established gold in FR-Bank FULL | 201 |
| lexical sweep detects presence | **140 (69.7%)** |
| lexical sweep misses presence | **61 (30.3%)** |

Sweep-negative rates on the external backends under the same instrument: Mem0 **111/205 (54%)**,
A-MEM **96/222 (43%)**.

**The `ingestion-loss` → `sweep-negative` rename is ratified as performed.** 207 labels were
renamed to what the measurement establishes, with the false-negative rate recorded per item. No
item was relabelled to PRESENT or UNRESOLVED and no new rule was invented at that point. Nothing
about that handling is revisited.

## 2. The two-channel presence instrument — adopted

Presence on any backend is decided by **two channels**:

- **Lexical channel**: `exp4_witnesses.supports_correct(entry_text, correct_answer)` — ≥2 shared
  content tokens and ≥50% coverage of the gold answer's content tokens. Unchanged.
- **Embedding channel**: max cosine between the **question** embedding and the backend's entry
  embeddings, `text-embedding-3-small`, **threshold 0.295**.

**The 0.295 threshold is carried unchanged from the natural-absent screen**, where it was
calibrated as p2.5 of the max-cosine distribution over the 516 real questions using cached
embeddings, before any probe existed. **It is not retuned against these labels, or against any
label.** Carrying a threshold calibrated on an independent population is the point; re-fitting it
here would destroy the property that makes it usable.

## 3. Required control on the two-channel instrument

The two-channel instrument **must run the same FR-Bank known-present control** — the 201 in-scope
questions the YAML join establishes are answerable in FR-Bank FULL. Its **combined recall** is
measured, and its complement

> **ε = 1 − combined recall**

is the **residual false-negative rate**, reported and **attached to every external ABSENT claim in
the study**. ε is measured, not assumed; whatever it comes to is published beside the numbers it
qualifies.

## 4. Routing rule

For an in-scope question with a resolvable YAML join, on an external backend:

| lexical | embedding | label |
|---|---|---|
| positive | — | **PRESENT** |
| negative | **positive** | **UNRESOLVED** — the store holds topically close content the lexical channel could not confirm; presence is unsettled, and unsettled is not absence |
| negative | negative, **and YAML establishes the fact** | **ABSENT, subtype `ingestion-loss-attributed`** (ε disclosed) |
| negative | negative, **and YAML establishes nothing** | **ABSENT, subtype `sweep-negative`** |

`ingestion-loss-attributed` names an attribution carrying a stated residual error rate, not a
certainty. Both subtypes remain **excluded from the hard tier**, which on external backends is
NATURAL-ABSENT only.

## 5. The external PN-candidate count is a believed-state datapoint

Phase B.1 produced **0 PN candidates on Mem0 and 0 on A-MEM**, against 122 on FR-Bank. This is
recorded as a **believed-state finding, not a construction shortfall**:

> On erase-mode backends, PRESENT-NEGATIVE structurally converges to ABSENT. Mem0 overwrites the
> superseded value in place and hard-deletes retracted content; A-MEM records no lifecycle state
> at all. Content that ought to carry a negative obligation is therefore not *mislabelled* on
> these backends — it is **not present to be labelled**. The store cannot hold a stale value
> because it did not keep one.

This is the same taxonomy as the believed-state deliverable (overstate / erase / invent), observed
now on the label side rather than the index side, and it is a substantive result about what an
erase-mode store can and cannot be asked.

**Consequence, registered: H-NOK is scoped FR-Bank-only by construction.** Not by choice, and not
because the external backends failed a threshold — because the cell does not exist on them. NOK on
Mem0 and A-MEM is reported as structurally empty with this explanation, and contributes no gate.

## 6. Unchanged

Hypotheses H1-hard, H2-hard and its publishability bands, H-BELIEVED, the integrity check, the
label taxonomy, the membership criterion, the intent rules, thresholds `TAU_GOLD`/`TAU_LO`/`TAU_HI`,
tier definitions, the hard-tier headline designation, index v2, the leakage ladder and its D18
inspection rule, elicitation prompts and their hashes, metric definitions, the bootstrap
specification, budget and stop conditions.
