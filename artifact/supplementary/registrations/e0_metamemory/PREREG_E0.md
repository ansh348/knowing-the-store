# PRE-REGISTRATION — E0 FEASIBILITY PROBE
## Metamemory over external agent memory stores: calibrated pre-retrieval coverage judgments

**Frozen:** 2026-08-10 · **Branch:** `[BRANCH]`
**Design basis:** `e0_metamemory/FINDINGS_E0_STEP0.md`, introduced at commit **`d51f12d`**.
**Threshold calibration:** `e0_metamemory/thresholds.json`, `e0_metamemory/tau_audit_sample.json`.
**Item plan:** `e0_metamemory/plan.json`.

**Statement of prior data contact.** No elicitation observation existed before this freeze.
Zero API calls have been made in `e0_metamemory/` at any point. Everything that informed this
document — the Step-0 census, the τ calibration, the persona selection, the item census — is a
pure function of committed LifecycleBench artifacts, computed with no model in the loop. No FOK
or NOK judgment, from any model, has been observed. The elicitation harness has not been run.

These are original pre-registration decisions informed by the Step-0 census, not amendments to
an earlier registration. No earlier registration exists.

---

## 0. Decisions of record

Four parameters were left open by the Step-0 report and are fixed here.

| # | Parameter | Decision |
|---|---|---|
| 1 | Persona count | **20**, with 2–3 ablated categories per persona |
| 2 | Gold resolver | **YAML-native only** for all gate metrics. The lexical proxy runs as a pre-registered sensitivity arm, reported side by side, gating nothing. The Claude-judged cache is **excluded from labels entirely** and may appear only as an appendix diagnostic cross-check. |
| 3 | UNRESOLVED | **Accepted.** Exclusion rule fixed pre-elicitation, system-independent, census published per attack vector and per category. |
| 4 | Detector threshold | **Asymmetric pair** replacing the single τ: `TAU_LO = 0.20`, `TAU_HI = 0.80` |

**Rationale for (2), recorded because it constrains what E0 can claim.** Label observability is
the paper's central claim. Judged labels in a calibration study are disqualifying: an AUROC
computed against labels a model produced measures agreement between two models, not calibration
against ground truth. The Claude-judged cache has higher coverage (480/516 vs 222/516) and it is
being given up deliberately.

**Scope of E0.** E0 tests **coverage judgments over single-fact-supported questions**. Two
attack vectors are out of scope by construction and are excluded before any elicitation:
`AV5_broad_query` (40 questions corpus-wide) and `AV8_numeric_preservation` (63), neither of
which has a source YAML section — AV5 by design ("the system must synthesize across records"),
AV8 because its questions draw numbers from across sections and 16 of them were hand-appended
with no YAML counterpart at all. **Aggregation-FOK — the feeling of knowing over a set of facts
that must be combined — is deferred to E1.**

---

## 1. Hypotheses

**H1 (blind miscalibration).** Without an index, FOK discriminates ABSENT from non-ABSENT
coverage near chance.
> Operationalized: **blind FOK AUROC < 0.75.**

**H2 (index-conditioned calibration).** A metadata-only index improves discrimination.
> Operationalized: **indexed FOK AUROC − blind FOK AUROC ≥ +0.10**, with a paired bootstrap 95%
> CI excluding 0.

---

## 2. Gate logic (verbatim)

- **GO:** H1 holds AND H2 holds.
- **KILL-A (no problem):** blind FOK AUROC ≥ 0.80. The problem the paper claims may not exist.
- **KILL-B (mechanism fails):** indexed minus blind < +0.10 or CI includes 0.
- **AMBER:** blind AUROC in [0.75, 0.80) with H2 holding, or any other mixed outcome. One
  pre-registered index-design revision is then permitted (Step 6), after which the gate is final.
- **NOK is exploratory in E0:** report AUROC/ECE for both arms, gate nothing on it.

`RESULTS_E0.md` will state what these gates say, mechanically, with no recommendation about
whether the paper should proceed.

---

## 3. The provenance join

LifecycleBench has **no per-question gold-edge annotation** — the project documents this itself
(`pkwc_q2_common.py:26-30`, `MEMAUDIT_EVIDENCE_REPORT.md:252-255`). The join below is built from
scratch, entirely from YAML ground truth plus bank structural fields. Implementation:
`tools/e0_common.py`.

### Stage A — question → YAML section record

Route by `attack_vector` to a YAML section, then take the token-overlap argmax over that
section's records, requiring a **margin of ≥2 tokens** to the runner-up.

| Attack vector | YAML section |
|---|---|
| AV1, AV4 | `supersession_events` |
| AV2 | `expiring_logistics` |
| AV3 | `stable_identity` |
| AV6 | `contradictions` |
| AV7 | `retractions` |
| AV9 | `ambiguous` |
| AV5, AV8 | none — out of scope |

`attack_vector` is read from the question JSON, never from the YAML: 21 `draft_questions` in
personas 1–20 carry `attack_vector: null`.

### Stage B — YAML record → bank entry ids

- **B1 (`expiring_logistics` only):** `event_date` equality against `entry.event_time[:10]`.
  Resolves 116/126 records with zero cross-session collisions.
- **B2 (everything else):** session-anchored lexical resolution. Candidates are restricted to
  entries whose `source_session` equals the record's session; a candidate is gold iff it shares
  **≥2** content tokens with the fact and covers **≥ TAU_GOLD = 0.50** of the fact's tokens.

Pure structural alternatives were measured and rejected: YAML `slot` vs bank `slot_key` matches
26/121 verbatim; slot-chains spanning `old_session`..`new_session` are unique for only 44/121.

### Negative obligation

`is_active` is **not** used to find superseded content. Of 109 supersession events with a
well-defined discriminator, 78 still have an `is_active=True` entry asserting the superseded
value; the ingest pipeline did not supersede in most YAML-declared cases, so `is_active` would
measure the pipeline rather than the ground truth.

Instead, for a record with a superseded value *O* and a current value *N*, let `DO = toks(O) −
toks(N)` and `DN = toks(N) − toks(O)`. If either has fewer than 3 tokens the record is
UNRESOLVED (`N_weak_discriminator`). Otherwise an entry *e* **fires** with signal
`cov(DO, toks(e))`, subject to `|DO ∩ toks(e)| ≥ 2` and a cross-guard `cov(DN, toks(e)) < 0.34`.
The detector scans the **whole persona bank**, not only the declared session.

Expiry is date-derived and exact, with no threshold: an entry is expired iff
`event_time < t_now − 14 days`.

### Reference time

`t_now = max(created_at over ACTIVE entries of the FULL bank) + 24h`, the operational value the
system itself computes (`evaluate_lifecycle_bank.py:168-174`), with the 14-day cutoff from
`lifecycle_bank.py:1055`.

**`t_now` is pinned per persona as an explicit constant, recorded in `plan.json`, and shared
byte-identically between the FULL and ABLATED variants.** It is never recomputed from the
ablated bank. Deleting the newest active entries would otherwise slide the expiry cutoff
backwards and silently re-label expiry for reasons unrelated to the ablation. Measured spread
across the 20 selected personas: 2026-02-07 (kenji) to 2026-05-26 (aisha) — it is not a global
constant, so this pinning is load-bearing rather than cosmetic.

---

## 4. Thresholds

| Constant | Value | Governs |
|---|---|---|
| `TAU_GOLD` | 0.50 | Stage B lexical resolution of the **gold** set |
| `TAU_LO` | **0.20** | any detector signal ≥ this **disqualifies an item from ABSENT** |
| `TAU_HI` | **0.80** | admits an item to **PRESENT-NEGATIVE** |

Signal **strictly between** `TAU_LO` and `TAU_HI` → **UNRESOLVED**.

**`TAU_LO` rule (declared before computation):** the largest value on the grid
`{0.00, 0.05, …, 1.00}` at which the set of ABSENT-disqualified items is identical to the set at
the structural floor. That is the plateau: maximum recall, expressed as the largest threshold
that gives up nothing. **Computed: 0.20**, at which point all 810 detector fires are retained
and 84 (persona, question) items are disqualified from ABSENT.

**`TAU_HI` rule (declared before the audit was read):** the smallest value on the same grid
whose hand-audited precision is ≥95%. The audit is **30 detector fires sampled uniformly without
replacement, seed 42**, from every fire attached to a resolved question across all 40 personas,
each read directly against the YAML record that produced it. No LLM judging: the audit is a
committed table of (entry text, YAML superseded value, YAML current value, verdict, reason) in
`tau_audit_sample.json`, checkable line by line.

Audited precision, from `thresholds.json`:

| threshold | n ≥ thr | true | precision |
|---|---|---|---|
| 0.20 | 30 | 12 | 0.400 |
| 0.50 | 17 | 11 | 0.647 |
| 0.60 | 12 | 10 | 0.833 |
| 0.70 | 9 | 8 | 0.889 |
| 0.75 | 8 | 7 | 0.875 |
| **0.80** | **5** | **5** | **1.000** |
| 1.00 | 3 | 3 | 1.000 |

**Two caveats recorded in advance.** (i) The denominator at `TAU_HI` is **n=5**. Precision 1.000
on five audited fires is weak evidence, and the true precision could plausibly be well below 1
while still above 0.95. (ii) The cliff between 0.75 (0.875) and 0.80 (1.000) rests on a single
reclassified item. Both are why PRESENT-NEGATIVE is exploratory and gates nothing.

The audit also retires the single-threshold design: at the τ=0.50 originally proposed, precision
would have been **0.647**, i.e. roughly a third of PRESENT-NEGATIVE labels would have been wrong.
The four recurring false-positive patterns, named in `apply_audit_verdicts.py`, are: (a) the
entry states the transition itself and so carries the *current* value; (b) the entry is already
past-tense marked, so nothing needs suppressing; (c) the supersession changed only part of the
record and the entry asserts the unchanged part; (d) pure token collision across unrelated facts.

---

## 5. Label rule

For an item = (question, store variant), with `G` = gold entries surviving in the variant,
`hi` = fires ≥ `TAU_HI` plus expired gold, `lo` = fires ≥ `TAU_LO`:

```
if gold could not be established in the FULL bank : UNRESOLVED
elif hi is non-empty                             : PRESENT-NEGATIVE
                                                     with-replacement    if G non-empty
                                                     without-replacement otherwise
elif lo is non-empty                             : UNRESOLVED (between-thresholds)
elif G is non-empty                              : PRESENT
else                                             : ABSENT
```

PRESENT-NEGATIVE takes precedence over PRESENT, as specified. A mid-strength signal makes the
item UNRESOLVED rather than PRESENT or ABSENT — this protects both cells, not only ABSENT.

**Labels are never imputed.** Every label is recomputable by re-running `tools/e0_common.py`
over the committed artifacts.

---

## 6. Items, personas and ablation

**Selection rule.** (a) Per persona, the ablation is the k ∈ {2,3} subset of the 11 categories
maximising ABSENT, tie-broken by more PRESENT-NEGATIVE, then more PRESENT, then fewer
categories, then alphabetical. (b) Personas are chosen by greedy addition then local search
maximising (smallest gate cell, total scoreable items), scanning candidates in sorted name order
and accepting only strict improvements. **Both steps are fully deterministic; no seed is
required and none is used.**

| persona | PRESENT | ABSENT | PRES-NEG | UNRES | t_now (pinned) | ablated categories |
|---|---|---|---|---|---|---|
| aisha | 3 | 3 | 4 | 14 | 2026-05-26 | HEALTH_WELLBEING, HOBBIES_RECREATION, LOGISTICAL_CONTEXT |
| bruna | 6 | 3 | 3 | 12 | 2026-05-11 | HEALTH_WELLBEING, OBLIGATIONS, PROJECTS_ENDEAVORS |
| chenoa | 4 | 4 | 2 | 14 | 2026-04-29 | IDENTITY_SELF_CONCEPT, OBLIGATIONS |
| david | 6 | 4 | 2 | 16 | 2026-04-06 | HEALTH_WELLBEING, IDENTITY_SELF_CONCEPT, OBLIGATIONS |
| elena | 2 | 5 | 6 | 15 | 2026-04-03 | LOGISTICAL_CONTEXT, OBLIGATIONS, RELATIONAL_BONDS |
| fatima | 5 | 3 | 4 | 12 | 2026-03-01 | HEALTH_WELLBEING, INTELLECTUAL_INTERESTS, RELATIONAL_BONDS |
| ingrid | 4 | 3 | 4 | 15 | 2026-04-21 | HEALTH_WELLBEING, HOBBIES_RECREATION, RELATIONAL_BONDS |
| jerome | 5 | 3 | 3 | 17 | 2026-05-02 | IDENTITY_SELF_CONCEPT, LOGISTICAL_CONTEXT, RELATIONAL_BONDS |
| kenji | 4 | 3 | 2 | 15 | 2026-02-07 | PREFERENCES_HABITS, PROJECTS_ENDEAVORS, RELATIONAL_BONDS |
| leila | 4 | 4 | 2 | 16 | 2026-05-09 | HEALTH_WELLBEING, LOGISTICAL_CONTEXT, PROJECTS_ENDEAVORS |
| lily | 7 | 3 | 6 | 8 | 2026-04-02 | IDENTITY_SELF_CONCEPT, PREFERENCES_HABITS, RELATIONAL_BONDS |
| mehmet | 6 | 3 | 2 | 15 | 2026-05-06 | FINANCIAL_MATERIAL, OBLIGATIONS, PROJECTS_ENDEAVORS |
| mirri | 2 | 2 | 4 | 18 | 2026-05-11 | HEALTH_WELLBEING, PROJECTS_ENDEAVORS, RELATIONAL_BONDS |
| pan | 7 | 4 | 3 | 12 | 2026-03-01 | LOGISTICAL_CONTEXT, PROJECTS_ENDEAVORS, RELATIONAL_BONDS |
| raj | 7 | 4 | 3 | 10 | 2026-04-23 | HEALTH_WELLBEING, INTELLECTUAL_INTERESTS, RELATIONAL_BONDS |
| rosa | 3 | 3 | 4 | 14 | 2026-05-20 | HEALTH_WELLBEING, IDENTITY_SELF_CONCEPT |
| samuel | 3 | 3 | 4 | 14 | 2026-02-20 | HEALTH_WELLBEING, IDENTITY_SELF_CONCEPT, RELATIONAL_BONDS |
| tom | 6 | 4 | 3 | 15 | 2026-03-24 | HEALTH_WELLBEING, IDENTITY_SELF_CONCEPT, PROJECTS_ENDEAVORS |
| valentina | 4 | 4 | 4 | 14 | 2026-05-09 | HEALTH_WELLBEING, OBLIGATIONS, PROJECTS_ENDEAVORS |
| zara | 1 | 4 | 4 | 17 | 2026-05-10 | OBLIGATIONS, PROJECTS_ENDEAVORS, RELATIONAL_BONDS |

**Committed census.**

| cell | n |
|---|---|
| PRESENT | **89** |
| ABSENT | **69** |
| PRESENT-NEGATIVE | **69** |
| UNRESOLVED | 283 |
| **scoreable** | **227** |
| total (question, variant) pairs | 510 |

Composition **39 / 30 / 30** against the 40/35/25 target. Maximum single-persona share:
PRESENT 7.9% (lily), ABSENT 7.2% (elena), PRESENT-NEGATIVE 8.7% (elena) — all inside the 15% cap.

**Relation to the 99/85/86 target census.** That figure came from the Step-0 measurement at a
single τ=0.50. Applying the asymmetric pair moves mid-strength detector fires into UNRESOLVED,
which costs ~16 items in each of ABSENT and PRESENT-NEGATIVE. **ABSENT = 69 ≥ 60**, so the plan
stays at 20 personas; escalation to 30 is not triggered. PRESENT-NEGATIVE = 69 also clears 60,
though it was not required to.

**UNRESOLVED census** (question level, FULL variant, 20 personas):

| reason | n |
|---|---|
| `B_no_session_anchor` — fact text clears no entry from its own session | 55 |
| `A_out_of_scope_av` — AV5 / AV8 | 48 |
| `A_tie` — two YAML records within 2 tokens | 15 |
| `N_weak_discriminator` — old and new values too similar to separate | 5 |

Resolution by attack vector: AV3 38/46 · AV2 27/39 · AV1 22/37 · AV4 16/23 · AV9 14/20 ·
AV7 9/20 · AV6 6/22 · AV5 0/20 (out of scope) · AV8 0/28 (out of scope).

Gold-edge categories: PROJECTS_ENDEAVORS 90, RELATIONAL_BONDS 67, HEALTH_WELLBEING 64,
OBLIGATIONS 54, LOGISTICAL_CONTEXT 38, IDENTITY_SELF_CONCEPT 31, INTELLECTUAL_INTERESTS 14,
PREFERENCES_HABITS 8, HOBBIES_RECREATION 7, FINANCIAL_MATERIAL 7.

---

## 7. Store variants and build-integrity checks

Two variants per persona, both written to a **new** directory `e0_metamemory/stores/`, never
into `LifeMemEval/artifacts/lifecycle_banks/`.

- **FULL** — the bank as-is, copied.
- **ABLATED** — every entry, **active and inactive**, whose `category` is in that persona's
  ablated set is deleted. Nothing else changes.

The builder asserts each of the following and aborts on failure. Each corresponds to a hazard
identified in the Step-0 report.

1. **Composite keys.** `lb_` ids restart at `lb_00001` in all 40 banks (18,936 entries, 622
   distinct id strings). Every item record is keyed on `(persona, entry_id)`. Assert: no bare
   `entry_id` is ever used as a global key.
2. **No renumbering.** Ids are preserved verbatim; only deletion occurs. Assert:
   `ablated_ids ⊆ full_ids` and every surviving entry is byte-identical to its FULL counterpart.
3. **`next_id` preserved** at its original value, never recomputed as `len(entries)`.
4. **No dot in any bank stem.** `LifecycleBank.load` does `path.with_suffix(".json")`, so
   `priya.v2` silently resolves to `priya.json`. Assert: every written stem matches
   `^[a-z]+_(full|ablated)$`.
5. **Sibling directory.** Assert `LifeMemEval/artifacts/lifecycle_banks/` is unmodified —
   compare its sha256 manifest before and after the build.
6. **`*_embeddings.npz` copied byte-for-byte**, never rewritten via `LifecycleBank.save()`.
7. **`t_now` identical across variants.** Assert the pinned value in the ABLATED record equals
   the FULL record's, byte for byte.
8. **Dangling `supersedes` pointers** created by deletion are recorded, not silently left:
   the count is reported in `RESULTS_E0.md`.
9. **Monotonicity.** ABLATED ⊂ FULL, so no question may gain gold or gain a detector fire under
   ablation. Assert `gold(ABLATED) ⊆ gold(FULL)` and `fires(ABLATED) ⊆ fires(FULL)` for every
   question.

**Sanity checks published in the report appendix**, as specified: (a) for 10 randomly sampled
ABSENT items (seed 42), print the gold edges and grep the variant to confirm absence; (b) for 10
sampled PRESENT-NEGATIVE items, print the YAML event establishing the negative obligation.

**Additional verification statistic, not a labelling rule.** For every ABSENT item, count the
entries in the variant that pass the independent lexical proxy `supports_correct` against
`correct_answer`. This should be 0. A non-zero count is a finding to report, not a relabelling
trigger — using the proxy as a rule would contaminate the YAML-native arm.

---

## 8. The index M(S)

Deterministic, metadata-only, same renderer for every variant, rendered as a fenced block of
roughly 40–60 lines.

**Allowed:** per-category entry counts (active and inactive separately); per-category
supersession counts; retraction counts; expiry counts; ingest-time recency statistics (newest
and oldest entry age per category); slot-key **names** per category, capped at 15 per category,
alphabetically.

**Forbidden:** fact values; entry text; numeric values from facts; event dates drawn from fact
content; anything from which the answer to a question could be read off.

**Pre-registered tightening ladder.** Slot-key names are LLM-generated at ingest and some are
highly specific (`project:golden_retriever_puppy`, `hobby:dog_ownership_interest`), so the
leakage control may well fire. The ladder is fixed in advance so that tightening is not a
post-hoc choice:

- **Level 0** — full slot-key names, capped at 15 per category, alphabetical.
- **Level 1** — strip everything after the first `:`, keeping only the generic attribute type
  (`project`, `hobby`, `family_member`), deduplicated.
- **Level 2** — drop slot-key names entirely; counts and recency only.

---

## 9. Index-leakage control (Step 3)

Before the main run: sample **30 PRESENT items** (seed 42), show the model **only** the index
and the question, and instruct it to answer. Scored by a simple string check against
`correct_answer` and its `wrong_answer_indicators`.

**Threshold: if more than 3 of 30 are answered correctly, the index leaks answer content.** Stop,
descend one level of the tightening ladder, re-run the control, and log the change in
`DEVIATIONS.md`.

**The control failing twice is a stop condition** — report and wait, do not descend to Level 2
and continue silently.

---

## 10. Elicitation

**Model:** `gpt-4.1-mini` · **temperature:** 0 · **seed:** 42 · **max_tokens:** 120 ·
one call per item per arm.

Responses are cached to disk keyed by `(item_id, arm, model, prompt_hash)`. All raw responses
are committed.

Two arms, identical except for the index block:

- **BLIND** — system prompt + the question.
- **INDEXED** — system prompt + the fenced index for that item's store variant + the question.

Prompt texts are frozen in `tools/prompts.py`.
**file sha256:** `3783175ff2ca42930a97888a9b475db3bf9f09f8c965c8c68debb23d0c9dd79e`
**frozen-texts sha256:** `671ff7550a84e8be527113a5e7514cb128c6a429fb41053aad9ad3cc92302f71`

### System prompt (both arms, verbatim)

```
You are assessing a personal long-term memory store that belongs to one user.

The store is a structured collection of atomic facts extracted from that user's past conversations with an assistant. Each fact carries a behavioral category, an ingest timestamp, and lifecycle metadata.

You will be shown a question that the user has just asked. Before any retrieval is performed, give two probability judgments about what the store contains.

FOK (feeling of knowing): the probability, from 0 to 100, that the store contains content relevant to this question -- anything that should shape the answer.

NOK (negative-obligation knowledge): the probability, from 0 to 100, that the store contains superseded, retracted, or expired content bearing on this question -- content whose correct influence on the answer is suppression rather than use.

FOK and NOK are independent judgments. NOK is not a subset of FOK and the two need not sum to anything in particular.

Do not attempt to answer the question. Do not speculate about what the answer would be. Judge only what the store is likely to contain.

Respond with a single JSON object and nothing else:
{"fok": <0-100>, "nok": <0-100>, "would_search": <true|false>}
```

### User message — BLIND

```
Question: {question}
```

### User message — INDEXED

```
Metadata index of this user's memory store (counts and structure only -- no fact content):

```
{index}
```

Question: {question}
```

### Leakage-control prompts

```
You are shown a metadata index of a personal memory store belonging to one user, and a question that user has asked. Answer the question as well as you can from the index alone. If the index does not let you determine the answer, reply exactly UNKNOWN.

Respond with a single JSON object and nothing else:
{"answer": "<your answer, or UNKNOWN>"}
```

```
```
{index}
```

Question: {question}
```

`would_search` is recorded but **not scored** in E0.

### Cost

510 (question, variant) pairs × 2 arms = **1,020 calls**, plus 30 for the leakage control.
At `gpt-4.1-mini` list prices $0.40 / $1.60 per MTok (`cost_analysis/compute_token_costs.py:42`),
with ~600 input tokens blind, ~1,500 indexed, ~40 output: **≈ $0.52 projected**, against a $10
hard cap and an $8 pre-launch escalation threshold. Actual spend is metered and reported.

---

## 11. Metrics

Computed for each arm, on the **scoreable subset only** (UNRESOLVED items excluded from every
metric and counted in the report).

- **FOK AUROC**, ABSENT vs non-ABSENT. **Primary — the gates read from this.**
- **NOK AUROC**, PRESENT-NEGATIVE vs rest. **Exploratory; gates nothing.**
- **ECE** with **10 equal-width bins** on [0,1], for both judgments and both arms:
  `ECE = Σ_b (n_b/N) · |acc(b) − conf(b)|`.
- **Brier score**, for both judgments and both arms: `(1/N) Σ (p_i − y_i)²`.
- **Paired bootstrap** for the indexed-minus-blind AUROC delta: **1,000 resamples**, resampling
  **items** (both arms move together, preserving the pairing), **seed 42**, percentile 95% CI.

Probabilities are the model's 0–100 outputs divided by 100. Responses that fail to parse as the
required JSON are retried once at temperature 0; a second failure marks the item
`ELICITATION_FAILED`, excludes it from metrics, and is counted in the report.

**Breakdowns reported:** PRESENT-NEGATIVE with- vs without-replacement; per persona; per attack
vector; ablation-manufactured ABSENT vs any other ABSENT; reliability diagrams (matplotlib, PNG).

**Sensitivity arm.** All of the above is recomputed with the gold set resolved by the lexical
proxy instead of the YAML-native join, reported side by side. It gates nothing.

---

## 12. Amber path (Step 6)

Taken **only** on an AMBER verdict, never on a KILL. Exactly one revision: amend this
pre-registration with a dated amendment preserving the original, describing a **single**
index-design change; re-run the **INDEXED arm only**; report original and revised results side
by side. The revised gate is final.

---

## 13. Stop conditions

Report and wait, rather than continuing:

- LifecycleBench artifacts not found or their schema does not match expectations.
- Fewer than 60 items achievable in any label cell. *(ABSENT and PRESENT-NEGATIVE at 69 each;
  ABSENT falling below 60 escalates to 30 personas, per the decisions of record.)*
- Index-leakage control fails twice.
- Projected or actual spend approaching the $10 cap.
- Any situation requiring modification of a frozen artifact.

---

## 14. Out of scope, recorded elsewhere

The finding that 78/109 supersession events leave an `is_active=True` entry asserting the
superseded value is a property of the FR ingest pipeline, not of this probe. It is recorded in
`e0_metamemory/NOTE_supersession_leak.md` for the FR revision correction list and **alters no E0
rule**. E0's only use of it is negative: it is why the detector ignores `is_active`.
