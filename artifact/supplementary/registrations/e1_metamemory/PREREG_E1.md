# PRE-REGISTRATION — E1 FULL CALIBRATION STUDY
## Metamemory over external agent memory stores: calibrated pre-retrieval judgments

**Frozen:** 2026-08-10 · **Branch:** `[BRANCH]`

| | |
|---|---|
| Design authority | `e1_metamemory/E1_DESIGN.md` **v0.2**, sha256 `c9ca79e8274b009a33bd8caa89a849aada8d7e41d872631fbc95725850d88d8d` |
| Phase-0 basis | `PHASE0_CENSUS.md` (`426efb4`), `RESOLUTIONS_APPLIED.md` (`783b1bc`), `INTENT_RULES.md` (`0f48a69`) |
| Predecessor | E0, GO at `77a4dfd` — blind FOK 0.5087 / indexed 0.8176, dedup delta +0.2747 CI [+0.1712, +0.3787], NOK null, $0.342 |
| Frozen prompts | `tools/prompts_e1.py` — file sha256 `ce5911e68bac60f86d265d7fdf25635b374d66ebd3832d90a05cbaf4f72dbd47`, texts sha256 `f6a97e459a9d67d236db6e04055e024718d2c88bf14be3468a9cfe578f5dae1b` |

**Statement of prior data contact.** No E1 elicitation observation exists. Total E1 spend to date
is **$0.0009** — one probe-drafting call and one embedding call, both construction, in the Phase-0
natural-absent pipeline test. No FOK, NOK, `nok_candidates_found` or `would_search` value has been
observed from any model on any E1 item.

**Provenance note on the design doc.** `E1_DESIGN.md` was not present in the repository at the
time Phase A began, although it had been reported as committed. Its v0.2 text was supplied
verbatim by the principal investigator and committed by me from that text without alteration.
This pre-registration freezes from that file. Logged as **D1**.

---

## 1. Universe, and what is excluded before any label

**Backends:** FR-Bank, Mem0, A-MEM. **Personas:** 40, except Mem0 which runs **37** — `alex`
(5/35 sessions), `thanh` (8), `aisha` (18) are excluded for ingestion incompleteness. Mem0 retains
9,736 of 10,074 entries; per-persona session coverage (min 22, median 31, max 35) is reported as a
**covariate on every Mem0 cell**, not applied and forgotten.

**Out of scope by rule, before any store is opened:** `AV5_broad_query` (40 questions) and
`AV8_numeric_preservation` (63). Neither has a source YAML section; AV5 requires synthesis across
records by design and 16 AV8 questions were hand-appended with no YAML counterpart. **103 of 516
questions**, excluded from every cell of every tier. E1's scope is coverage judgments over
single-fact-supported questions.

**Excluded artifacts:** `amem_banks/priya.canary/` (broken: sidecar claims 293 notes, store holds
101) and `mem0_nano_banks/` (collection exists, 0 points).

## 2. Intent typing — frozen

Typed under `INTENT_RULES.md` from **question text and attack-vector structure only**; never the
gold answer, never a label, never store contents. All 516 typed, **0 UNRESOLVED**.

| intent | n | negative obligation |
|---|---|---|
| CURRENT-STATE | 253 | applies |
| UPCOMING | 50 | applies |
| PAST-EVENT | 25 | **exempt** |
| CHANGE-AWARE | 85 | **exempt** |
| in scope | **413** | 303 may carry PN |
| out of scope | 103 | — |

**110 of 413 in-scope questions (26.6%) are structurally barred from PRESENT-NEGATIVE by rule.**

## 3. Label rules — verbatim from design doc §3

Labels are functions of **(store variant, question, intent)**. No label exists without an intent
type.

> - **PRESENT**: variant contains licensed content answering the question under its intent, no
>   negative obligation load-bearing. On external backends, PRESENT additionally requires
>   sweep-verified presence in the actual store.
> - **PRESENT-NEGATIVE**: variant contains content that, under this intent, must be suppressed
>   (superseded value for CURRENT-STATE; retracted plan for CURRENT-STATE or UPCOMING; expired
>   event for CURRENT-STATE or UPCOMING). **Expired content under PAST-EVENT intent is PRESENT,
>   not PN. YAML status fields override derived cutoffs.**
> - **ABSENT**: no licensed content and no obligation bears, under the `tau_lo` screen carried
>   from E0.
> - **UNRESOLVED**: everything the joins cannot settle.

**CHANGE-AWARE** questions can be PRESENT or ABSENT but **never** PRESENT-NEGATIVE: the superseded
value is licensed content that must be surfaced alongside the current one.

Thresholds carried from E0 unchanged: `TAU_GOLD` 0.50 (gold resolution), `TAU_LO` **0.20**
(any detector signal at or above disqualifies from ABSENT), `TAU_HI` **0.80** (admits to the
membership pass). Signal strictly between `TAU_LO` and `TAU_HI` → UNRESOLVED.

### 3.1 PN verification — full coverage of both halves, registered from the outset

The Phase-0 spot-check escalated all three backends (FR-Bank 85.7%, A-MEM 76.9%, Mem0 69.2%
membership precision against a 90% bar). **The escalation rule is retired and replaced by full
coverage.** Measured burden ~341 judgments, against a 500 stop threshold.

- **Semantic half**, once per **(question, YAML-record)** pair (~166): does this record constitute
  a negative obligation for this question **under its intent**? Backend-independent.
- **Membership half**, per **(entry, record)** pair at `TAU_HI` (~175: FR-Bank 125, A-MEM 33,
  Mem0 17).

**Membership criterion, verbatim from design doc §3:**

> does this entry assert the superseded value **AS CURRENT**. Exclusions: entries stating the
> decision-against ("considered X but decided against it") are **NOT** members; entries with
> explicit historical framing ("the previous focus was X", "used to") are **NOT** members; token
> collisions are **NOT** members.

The first two exclusion classes are **recorded as tagged subtype counts** during the pass —
`decision-against` and `historically-framed` — and reported as weak-generator hazards.

All verification tables committed. Detector-proposes, YAML-disposes.

## 4. Variants and difficulty tiers

| backend | variants |
|---|---|
| FR-Bank | FULL · CAT-ABLATED (easy, E0 comparability) · **SLOT-ABLATED** (hard) · **NATURAL-ABSENT** |
| Mem0 (37 personas) | FULL · **NATURAL-ABSENT** |
| A-MEM | FULL · **NATURAL-ABSENT** |

**SLOT-ABLATED** removes a question's gold-supporting entries **and their sibling slot-key
copies**. Phase-0 closure factor **2.59× gold** (median 1.50×, max 20.3×), mean 7.5 entries
removed per question against a 432-entry bank — versus CAT-ABLATED's 35% of the bank at once.

**CAT-ABLATED is inexpressible on Mem0 and A-MEM** and is not attempted. **No classifier enters
the label path under any circumstances.** Reported as a finding: a category ablation is a
*regional* probe and presupposes region structure the store can name; a store without region
structure cannot be probed regionally. Session-ablation may exist only as an **unpooled
exploratory cell**.

**NATURAL-ABSENT**: 7 probes drafted per persona, machine pre-screened at the fixed **0.295**
embedding threshold (p2.5 of the max-cosine distribution over the 516 real questions, calibrated
from cached embeddings before any probe existed), survivors verified by direct YAML reading with
committed per-probe tables including the search transcript. Phase-0 survival 5/6. Probes carry an
`adjacent_content` flag where topically related but non-answering content exists.

**HARD TIER = SLOT-ABLATED + NATURAL-ABSENT, pooled. The pre-registered headline reads the hard
tier.**

`t_now` pinned per persona, byte-identical across variants. The **construction-stage lexical
contamination sweep runs before label freeze**; flagged items route to **UNRESOLVED by build
rule** (Phase 0: 59/201, 29%) — not to a sensitivity row as in E0.

**ABSENT mechanism split** (four named subtypes, never pooled across): `ablation` · `expiry` ·
`natural` · **`ingestion-loss`** (gold the YAML places in a session the backend never ingested;
reported, **never pooled into the hard tier**).

## 5. Index v2 and the provenance axis

Value-scrubbed renderer — **attribute paths kept, values never**. Lifecycle fields: per-category
active / superseded / retracted / expired counts, supersession-event counts, scrubbed superseded
slot names, recency statistics. **An inexpressible field emits `not expressible by this backend`,
never `0`** — `0` asserts "there are none", which is false for A-MEM supersession and unknowable
for Mem0.

Two provenances per variant, **both primary**: **TRUE** (from YAML ground truth) and **BELIEVED**
(from the backend's own metadata, only from fields that actually resolve).

Believed-state characterization, frozen from `BELIEVED_STATE.md`: FR-Bank **overstates** staleness
~60× while recalling 61% of genuine supersessions; Mem0 **erases** history (12.7% carry
`updated_at` and nothing else); A-MEM can express **no** lifecycle signal — its believed index
builds from `timestamp` and `last_accessed` only, and the **23,403 unresolvable links are reported,
never repaired**.

**Named analysis — the lifecycle-ablation decomposition.** Because A-MEM's believed index is
structurally limited to counts and recency, the three-way comparison
**A-MEM-believed vs FR-Bank-believed vs TRUE** decomposes the indexed benefit into bare
count-and-recency structure versus lifecycle signal, without a dedicated ablation arm. Registered
here as a named analysis with its own table in the report.

**Named deliverable — the believed-state failure taxonomy** (overstate / erase / invent), with all
Phase-0 numbers preserved; candidate Figure 1.

**Leakage ladder** runs **per backend per provenance**, levels 0 → 1 → 2 as in E0. Threshold: more
than 3 of 30 sampled PRESENT items answered correctly from the index alone. **D18 inspection rule
(codified):** a nominal pass **within 2 items of threshold** triggers manual inspection of the
index, and descent if inspection shows the scorer masked leakage. Ladder exhausted without a pass
is a stop condition.

## 6. Hypotheses and gates

- **H1-hard**: blind FOK AUROC **< 0.75** on the hard tier.
- **H2-hard (headline)**: indexed-TRUE minus blind FOK AUROC **≥ +0.10** on the hard tier, paired
  bootstrap 95% CI excluding 0.
  **Publishability bands, frozen now:** **< +0.10** re-scope · **+0.10 to +0.15** modest, carried
  by NOK and control · **> +0.15** stands alone.
- **H-NOK**: indexed-TRUE NOK AUROC **≥ 0.65** **AND** indexed minus blind **≥ +0.10** with CI
  excluding 0, on the intent-conditional taxonomy with the lifecycle-bearing index.
  **Pre-committed failure consequence: NOK demotes to a reported negative result and the paper
  re-scopes to coverage-FOK plus control.** Believed-state NOK reports but does not gate; on A-MEM
  it is expected to fail **by construction**, which is itself the decomposition datapoint.
- **H-BELIEVED (report-only, no kill)**: believed-state indexed FOK retains **≥ 60%** of the
  TRUE-state delta, per backend. The A-MEM cell is the decomposition read.
- **Integrity check**: strong-model blind arm, ~150 stratified items, `gpt-5.6-sol` via
  `codex exec`. Report AUROC, ECE, and mean FOK against base rate. **Both outcomes reportable** —
  the E0 pessimistic-prior finding (mean blind FOK 0.26 against a 0.67 base rate) either
  generalizes to the frontier class or is bounded to small models.

Gate verdicts are reported **mechanically, with no recommendation.**

## 7. Elicitation

`gpt-4.1-mini`, temperature 0, seed 42, max_tokens 200. JSON per item:
`{"fok": 0-100, "nok_candidates_found": true/false, "nok": 0-100, "would_search": true/false}`.

**Blind arm caches on PROMPT HASH — one draw per unique prompt, shared across variants** (E0 D19:
90/255 byte-identical pairs disagreed, 14.6% of blind FOK variance). A **k=3 multi-draw
subsample (~50 questions)** quantifies residual noise; the retry path uses an explicit attempt
counter so a cached failure cannot be silently returned.

Arms: BLIND · INDEXED-TRUE per backend · INDEXED-BELIEVED per backend · **staircase subsample
(~150 items, FR-Bank TRUE only)** · **strong-model blind (~150 stratified)**.

Prompt texts frozen in `tools/prompts_e1.py` and quoted there verbatim. E0's `prompts.py` is **not**
reused: its system text asserts "Each fact carries a behavioral category, an ingest timestamp, and
lifecycle metadata", which is false for both external backends and would confound the very axis E1
measures. NOK's two worked examples are drawn from **AV8 questions, which are out of scope and
appear in no cell**, so they cannot leak scoreable material.

**Parse-failure policy:** one retry at temperature 0 with a distinct cache key; a second failure
marks the item `ELICITATION_FAILED`, excluded from metrics and counted.

## 8. Metrics

Computed on the scoreable subset only; UNRESOLVED excluded by pre-elicitation rule with published
census.

- **FOK AUROC**, positive class = non-ABSENT, score = FOK. Ties contribute 0.5 (rank-based
  Mann-Whitney) — load-bearing given E0's D20 quantisation.
- **NOK AUROC**, positive class = PRESENT-NEGATIVE, score = NOK. The two-step intermediate
  (`nok_candidates_found` rate) is **reported alongside** the probability AUROC.
- **ECE**, 10 equal-width bins on [0,1]; **Brier**; reliability diagrams — per tier, arm, backend,
  provenance.
- **Paired bootstrap**: 1,000 resamples of items, seed 42, both arms moving together, percentile
  95% CI.
- **Staircase** responses map to an interval midpoint from the four thresholds; reported as its
  own arm, never pooled with the numeric arm.
- Descriptive skip-rate curves from FOK thresholds (no new calls; control proper is E2).

**Standard rows, every gate table:** the **dedup row** (blind draws averaged per unique prompt);
a sensitivity row for **every** construction-stage exclusion; the ABSENT mechanism split; per-tier,
per-backend, per-provenance breakdowns.

## 9. Budget and stop conditions

Projection **~$2.50**, cap **$50**, escalation threshold **$35** — projected at the
pre-elicitation checkpoint. The strong-model lane is subscription-billed and metered in wall-clock,
not dollars.

Stop and report: any gate-relevant cell **under 50** on the hard tier after construction · leakage
ladder exhausted on any backend/provenance · verification burden materially exceeding the measured
~341 · projection over $35 · anything touching a frozen artifact · any label rule the design doc
does not settle (conservative reading plus `DEVIATIONS.md` if minor, **stop if load-bearing**).

All amendments dated and pre-observation.
