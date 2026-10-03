# PREREG — E3, THE POLICY INSIDE A RUNNING AGENT

# ✅ FROZEN AT SP1 — 2026-08-11

**Ratified by [AUTHOR-1] at SP1 with the attribution redesign encoded below.** Superseded draft:
`PREREG_E3_DRAFT.md` at commit `f5c58f1`. Design of record: `E3_DESIGN.md`. Evidence base:
`PROBE_REPORT.md` and `probes/`. Deviation ledger: `DEVIATIONS_E3.md`; **E3's new deviations are
numbered from D49** (D45–D48 were opened by the STEP-0 probes). Predecessors: `e1_metamemory/` at
tag `e1-complete`, `e2_metamemory/` at `c4bd3e1`.

**Statement of data contact at freeze time.** No E3 elicitation of any kind has occurred. No
threshold has been derived on E3 data. No snapshot or retrieval artifact exists. No store has been
written. The four STEP-0 probes were read-only and made no model call. **Everything below is frozen
in advance of the numbers it governs.**

**Budget: cap $40 absolute, projection gate $15.** Cumulative across processes, summed over cached
responses, never read from a single process's meter (D27-E1).

---

## 0. CLAUSE C-1 — the calendar gate

> **If the eval phase is not complete by 8 September 2026 AoE, E3 exits the ICLR submission and
> completes for the rebuttal or camera-ready.** Completeness means: every registered
> (item, rung, arm) cell has an answer and a judgment on disk, and SP3's census reports zero gaps.
>
> On that date, whatever is on disk is reported in whatever venue it reaches. **No band, margin,
> sequence, ladder, arm, split or stopping rule may be changed on or after 1 September 2026 for any
> reason connected to the deadline.** A design change after that date is admissible only as a dated
> amendment that states, in its first line, that it is not deadline-driven and why.
>
> **This clause exists because the failure it prevents is invisible after the fact.** A band widened
> in the last week reads identically to a band that was always that wide.

---

## 1. Design — Design A, snapshot ladder

**R = 4 rungs at sessions {14, 20, 24, 32}**, placed by **accumulated staleness** rather than by
session index. On the 32 eval personas the 165 dated change events resolve as **2 / 59 / 123 / 165 —
1% / 36% / 75% / 100%**. The naive equal-spacing ladder {14, 21, 28, 35} would reach 98% by its third
rung and spend its fourth measuring nothing.

**Snapshot definition, frozen.** The store at rung *s* is `{entries : source_session ≤ s}` and
nothing else. `t_now(s)` is session *s*'s own date **+ 24 h**, per persona — E1's pinning convention
with the pin moved to the rung.

**Replay is ordered by `session_id`, never by date (D46-E3).** `callum` session 15 is dated
2025-06-05 and session 16 is dated 2025-06-04; a date-ordered replay would silently reorder that one
persona's writes against every other's.

**Two assertions run at artifact build and fail the boundary on violation:**
1. session ids contiguous and monotone 1..35 on all 40 personas;
2. **nesting: `alive(s₁) ⊂ alive(s₂)` for every s₁ < s₂ in the ladder, per persona.** A snapshot
   ladder that is not nested is not a timeline.

**Store state is rebuilt per rung**, and both maintenance costs measured in p3 are recorded **as
separate columns, never averaged into one**: the **write-driven** component (counters, per-category
breakdown, attribute-name sets — measured at **1.11 µs/write**) and the **clock-driven** component
(recency, age distribution, `expired` — which change with `t_now` and no write, and cost one pass per
serve). E2's single 1.3 ms/store figure was a *rebuild*, which is the cost of not having maintenance.

---

## 2. Cell policy — key-valid-only

A question enters the ladder **only from the rung at which its authored answer key becomes valid**:
at or after its resolving session for `supersession_events` / `contradictions` / `retractions`, at or
after `tentative_session` for `ambiguous` (AV9), and at or after `event_date` for
`expiring_logistics`.

**Why.** 39.3% of (question, rung) cells carry an authored `correct_answer` describing a state the
rung has not reached, and for the two-sided sections the `wrong_answer_indicators` **name what is
correct there** (D48-E3). `elena_q02` at rung 7 is the clean case: correct answer "Mediterranean
diet", wrong indicator "keto", and at that rung the store contains keto and nothing else because the
switch happens at session 22. **D48 is resolved by rung placement rather than by building a key
generator**, which keeps a hand-built instrument out of the measurement path — the same reasoning
that barred a classifier from E1's label path.

**Excluded cells, enumerated.** Over the eval split, **214 of 1,048 cells (20.4%)** are excluded:

| rung | authored questions key-valid | excluded | probes (always valid) | n (eval cells) |
|---|---|---|---|---|
| 14 | 59 / 141 | 82 | 121 | **180** |
| 20 | 79 / 141 | 62 | 121 | **200** |
| 24 | 93 / 141 | 48 | 121 | **214** |
| 32 | 119 / 141 | 22 | 121 | **240** |
| **total** | | **214** | | **834** |

Calibration adds **187** cells (37 / 45 / 49 / 56). **Total registered cells: 1,021.**

> **PRE-EVENT NOTE, frozen.** **Every excluded cell is a pre-event cell — one in which nothing in the
> store is stale yet.** The exclusion therefore removes no obligation-bearing item and costs the
> deployment-aging claim nothing.
>
> **Every PRESENT-NEGATIVE cell is key-valid by construction**, because a PN label requires the
> resolving event to have happened, which is exactly the condition the authored key needs. This is a
> property of the rules, not an empirical observation, and it holds at every rung.

**Item base.** The **FULL-variant scoreable set** — 262 eval items (141 authored questions + 121
natural-absent probes) and 61 calibration items. **No category or slot ablation variants**: E3's
store variation is time. This is `PREREG_E2.md`'s pre-registered "deployment-realistic slice", the
slice on which E2's policy was the best and never-retrieve the worst.

**Resulting obligation mass:** PN cells **7 / 25 / 37 / 41 = 110** across the ladder, against E2's 82.

---

## 3. The label instrument of record — the D47 predicate

E1's `PersonaJoin.label` with **three** changes and no others:

1. **survival by session** — `{i : source_session(i) ≤ s}` replaces the category filter;
2. **the expiry cutoff moves with the rung** — `t_now(s) − 14 d` rather than a globally pinned
   `t_now`;
3. **event activation (D47)** — before a YAML record's resolving session (`new_session`,
   `retraction_session`) the record creates **no negative obligation**, and the entries asserting the
   **old** value are the gold ones.

**Validity anchor, frozen as a stop condition.** At the terminal rung the rule must reproduce
`PersonaJoin.label(q, ablated = ∅)` on **178/178** authored questions. It does today
(`probes/p2_labels_at_t.py`). **If it does not at build time the run stops and reports** — a
labeller that disagrees with E1's at the terminal rung is not a generalisation of it.

**PN verification.** E1's hand-adjudicated verdicts are reused unchanged. The ladder needs **6
decisions E1 does not hold** (1 membership, 5 semantic), enumerated in `PROBE_REPORT.md`. They are
adjudicated by hand under E1's frozen criterion **before any eval-cell contact**, committed with
their reasoning, **never by a model**.

### D47 as LEDGER ITEM 14

> **The distinguishing property, named.** The naive instrument — filter entries by session and
> nothing else — is **wrong in the direction that flatters the study's own hypothesis**. It invents
> negative obligations the timeline has not yet produced: at rung 7 it reports **29
> PRESENT-NEGATIVE items against a true count of 1**, and across an illustrative 5-rung ladder it
> mislabels 82 of 890 cells, every one of them by asserting an obligation that does not exist.
> Since E3's central endpoint is an obligation-aware policy's advantage, the error would have
> **inflated the effect the study exists to measure**.
>
> **It was caught before any data existed**, by a feasibility probe that compared the naive rule
> against the corrected one rather than assuming the substitution was sound.
>
> **Standing lesson:** *a filter over the store's contents is not a model of the store's history.* A
> time-anchored evaluation over a lifecycle store needs two clocks — one for what has been written,
> one for what has been **decided**. A design carrying only the first reports obligations that do not
> exist yet, in the direction that flatters an obligation-aware policy.

Filed in `audit/postreview_prep/R2_INCIDENTS.md`. **Numbering note:** that ledger holds Incidents
1–8; the SP1 instruction calls this "ledger item 14". It is recorded there as **Incident 9** rather
than inventing items 10–13, with the discrepancy noted so the instruction's reference resolves —
the same convention Incident 8 used for the E2 instruction's "ledger item 11".

---

## 4. Arms

**One frozen retrieval-and-store artifact per rung**, retrieval-as-data. Retrieval is FR's
`lifecycle_search` over the rung's own bank at that rung's `t_now`, run **once** per (item, rung) and
written to an immutable hashed artifact that every arm reads. **The eval harness asserts the
artifact's sha256 at startup and exits on mismatch.**

| arm | policy | gate calls | application state |
|---|---|---|---|
| **(a) FULL** | retrieve iff `FOK ≥ τ_FOK`; apply the lifecycle-caution step iff `NOK ≥ τ_NOK` | 1 per cell | `S3` |
| **(a′) CONTENT-LOBOTOMY** | **byte-identical policy, byte-identical prompts**; only the lifecycle annotation passed to the application step is destroyed | **0 — same gate as (a)** | `S3′` |
| **(a″) CAUTION-ONLY** — *descriptive, gates nothing* | (a)'s policy with the annotation **removed** rather than scrambled; this is E2's `S2` exactly | 0 | `S2` |
| **(b) always-retrieve** | retrieve every turn, no gate, no caution | 0 | `S1` |
| **(c) no-memory floor** | never retrieve | 0 | `S0` |
| **(d) SHUFFLED-FOK** | (a)'s code with **FOK permuted across items within (persona, rung)** by frozen seed; retrieval rate matched to (a)'s realised rate at that rung | **0 — derived from (a)'s scores** | `S3` |

**Arm (e) CONSTANT is CUT.** Recorded reason: at τ_FOK and τ_NOK = 0.00 a constant mid-scale monitor
clears both thresholds on every item, so the arm reduces exactly to *always-retrieve plus caution* — a
fixed policy whose behaviour is determined before it runs. **It is not an experiment, and its
reduction is stated here rather than purchased.**

### 4.1 The always-on property, disclosed verbatim

> **τ_NOK = 0.00.** E2's Amendment-4 derivation measured the off-target cost of the caution step at
> `C ≤ 0` — the instruction does no harm where there is nothing to suppress — so the break-even
> `q* = C/(B+C)` is 0 and the derived operating point is the grid minimum. **The consequence, stated
> plainly: the application step fires on EVERY retrieval. It is not selective. Its trigger carries no
> NOK information, and permuting NOK cannot change any decision E3 makes.**
>
> This is why **arm (d) SHUFFLED-FOK destroys FOK information only**, and why the NOK channel is
> tested by **arm (a′), which attacks the application step's CONTENT rather than its trigger.**

### 4.2 Context states — four, and no more

| state | contents |
|---|---|
| `S0` | no facts |
| `S1` | retrieved facts |
| `S2` | retrieved facts + frozen `CAUTION_INSTRUCTION` — **E2's S2, byte-identical** |
| `S3` | `S2` **+ a per-fact lifecycle annotation from the BELIEVED store state at that rung** |
| `S3′` | `S3` with the annotation **scrambled** (§4.4) |

`S0` contains no store content and is therefore **rung-invariant**: it is elicited once per question
for the whole ladder. Answers are keyed `sha256(question_id ‖ rung ‖ state ‖ context ‖ draw)`;
judgments `sha256(question_id ‖ response)`.

### 4.3 The lifecycle annotation — D49-E3, disclosed as a departure

**`S3` is new. E2 had no state like it, and this is a deliberate, disclosed departure from "prompts
unchanged from E2".** It exists because **H-E3d has nothing to destroy without it**: at τ_NOK = 0 the
caution string is a fixed text carrying no per-item lifecycle content, so a "content lobotomy"
applied to E2's `S2` would be a no-op.

Each retrieved fact is rendered with exactly one annotation, from the **BELIEVED** store state at
that rung, by this precedence:

| annotation | rule, rung-correct |
|---|---|
| `[expired]` | `event_time < t_now(s) − 14 d` |
| `[superseded]` | ∃ an entry `e′` with `source_session(e′) ≤ s` and `e′.supersedes == e.id` |
| `[active]` | otherwise |

**Rendering, frozen:** each fact line becomes `N. <annotation> <fact text>`, and one sentence is
appended to `CAUTION_INSTRUCTION` in `S3`/`S3′` and nowhere else:
*"Each fact is tagged with what the store believes about its lifecycle state: [active], [superseded]
(a later value for it exists), or [expired] (its date has passed)."*

**`[retracted]` is deliberately NOT in the vocabulary**, and the reason is recorded rather than
absorbed: the store's `is_retracted` flag **carries no date**, so a rung-correct believed retraction
is not derivable from store-own fields. It affects **31 of 18,936 entries (0.16%)**, which are
annotated by the rules above. Using a YAML retraction date would put TRUE provenance into a BELIEVED
arm and is barred.

**Believed-superseded is computed from the `supersedes` pointer**, which is date-correct because the
pointer lives on the *newer* entry and that entry has a `source_session`. All 5,725 pointers resolve
within their own bank. `is_active` is **not** used: it reflects the store's final state and would
mark an entry superseded at rung 14 for an event occurring at session 30.

### 4.4 The scramble, specified

Deterministic, marginal-preserving, and computed once at artifact build:

1. For each **(persona, rung)**, collect the annotation of every retrieved fact occurrence across all
   of that persona-rung's registered cells, in ascending `(item_id, fact_position)` order.
2. Seed `numpy.random.default_rng(int(sha256("E3-LOBOTOMY|" + persona + "|" + str(rung))
   .hexdigest()[:16], 16))`.
3. Apply `rng.permutation` to the annotation vector and reassign it to the same positions.

**The multiset of annotations within each (persona, rung) is exactly preserved**, so `S3′` prompts are
statistically identical to `S3` prompts in annotation composition; only the fact↔annotation
association is destroyed. The **destruction rate** — the fraction of fact occurrences whose
annotation changed — is computed per (persona, rung) and **reported at SP3 as a census quantity, not
as a gate**. Persona-rungs whose annotation vector is constant yield a destruction rate of 0 by
construction; they are counted and reported rather than resampled.

### 4.5 Pinned instruments

**Answerer** `gpt-5.4`, temperature 0, seed 42, max 220 answer tokens — E2's Amendment-3 pin,
unchanged. **Gate** `gpt-4.1-mini`, temperature 0, seed 42 — E1's frozen lane, unchanged.
**Judge** `claude-sonnet-4-6` via `claude -p`, temperature 0, under the **unmodified**
`LifeMemEval/evaluate_e2e.py` rubric imported by AST rather than copied. `GENERATION_SYSTEM_PROMPT`
and `CAUTION_INSTRUCTION` are E2's, byte-identical. Credit rule, five-state typing and fixed
denominators are E2's, byte-identical.

**Gate prompt: L1W0D0.** L is an **index** factor, so `L1` is E1's intact index and **the E2 renderer
lock is honoured**. `W0` deletes the two worked-example paragraphs from `prompts_e1.SYSTEM`; `D0`
collapses the two-step decomposition into a single `nok` judgment and drops
`nok_candidates_found` from the schema. Both realisations are `m1_factorial.system_variant(W=False,
D=False)` **reused verbatim**, not re-implemented. Justification: M1 measured
**L +0.1980 · W +0.0134 · D −0.0193** and the best cell in the design, L1W0D0 at AUROC 0.7958, drops
both prompt fixes — `PREREG_E2.md` §5 pre-registered exactly this as *a recommendation for E3*.

---

## 5. Operating point — the derivation rule ships frozen

> **The frozen object is the RULE, not the number.**

**Rule, carried verbatim from `E2_AMENDMENT_4.md` §1:** on the calibration split, under the pinned
answerer, measure per-label credit when retrieving (`S1`) against skipping (`S0`); form
`G = (w_P·g_P + w_N·g_N)/(w_P + w_N)` and `L = loss on ABSENT`; set `p* = L/(G+L)`; and take
**τ_FOK = the LOWEST threshold on the uniform grid {0.00, 0.05, …, 1.00} whose calibration precision
for non-ABSENT is ≥ p\***. Ties to lower cost. **No argmax anywhere.** τ_NOK is set by the same
break-even logic on the confabulation axis: `q* = C/(B+C)`, and if `C ≤ 0` every threshold clears and
τ_NOK is the grid minimum — **which is what E2 measured, and it is recorded, not hidden.**

**Why the number is re-derived and not copied.** τ_FOK = 0.20 was derived on the **L1W1D1** FOK
distribution. E3's gate is **L1W0D0**, and M1 measured W and D on **NOK AUROC only** — their effect
on the FOK channel is unmeasured. Applying a frozen *number* to a scale it was not derived on is not
shipping frozen; applying the frozen *rule* is. **What ships frozen is the derivation, because that
is what makes the claim reproducible.**

**Applied exactly once**, on the 8 calibration personas, at ≈ $0.13. The resulting τ is committed as
a frozen constant in `THRESHOLDS_E3_FROZEN.json` **with its derivation shown**, its sha256 recorded
in the SP2 commit, and **the eval harness asserts that sha at startup and exits on mismatch**.

**No other fitting on E3 data, ever.** The calibration personas serve **variance measurement and this
one application, and nothing else.** Calibration personas appear in no eval-split figure.

**Split, frozen and identical to E2's:** calibration = `aisha, chenoa, dariush, david, patrick,
samuel, thanh, valentina`; eval = the remaining 32. Disjoint, so no persona that informed a threshold
appears in an eval figure.

---

## 6. Gates — fixed sequence, full α at every step

```
  H-E3a  confabulation vs always-retrieve
     │  HOLDS ──► H-E3b  credit non-inferiority
     │               │  HOLDS ──► H-E3c  credit attribution (SHUFFLED-FOK)
     │               │               │  HOLDS ──► H-E3d  NOK-information attribution
     └── not HOLDS ──┴───────────────┴───────────────┴──► SEQUENCE BROKEN
```

Ordered and gated, so **no multiplicity correction is applied and none is needed**. Each test runs at
**full α = 0.05** and only if its predecessor **HOLDS**.

**Stopping rule, exactly.** The sequence advances **only on HOLDS**. A **FAILS** or an
**INDETERMINATE** breaks it. Once broken, every downstream result is computed and reported in full
but labelled `EXPLORATORY (sequence broken at <step>)`, carries no inferential claim, and **may not
be described as confirmed, supported or significant** anywhere — main text, appendix or abstract.
Suppression is not the remedy for a broken sequence.

**Ordering rationale, recorded so it is not re-litigated.** By survivability. A null H-E3a says the
policy does not survive an evolving store, which is E3's whole subject. A null H-E3d says generic
caution suffices — a mechanism result, bad for one sentence, survivable for the line. The two
attribution tests are placed last because `E3_DESIGN.md` §4 predicts the *confabulation* attribution
is the hardest, and a predicted difficulty must not break the sequence above claims it has no bearing
on.

**Estimator, identical for every test:** OLS of the paired per-cell difference on **persona + label
fixed effects**, sum-to-zero, intercept as the estimate; **persona-clustered bootstrap, 1,000
resamples, seed 42**, cells resampled within persona. E2's `score_e2.adjusted` and `score_e2.boot_ci`
**imported, not re-implemented**. The unadjusted estimate is reported alongside every adjusted one.

### 6.1 The bands, numeric at commit

| test | contrast | band |
|---|---|---|
| **H-E3a** | (a) FULL vs (b) always-retrieve, **confabulation** | reduction **≥ 3pp** AND 95% CI **excludes zero** |
| **H-E3b** | (a) FULL vs (b) always-retrieve, **credit** | one-sided 95% lower bound on the adjusted paired delta **> −m**, with **m fixed by §6.2** |
| **H-E3c** | (a) FULL vs (d) SHUFFLED-FOK, **credit** | adjusted delta **> 0** with 95% CI **excluding zero** |
| **H-E3d** | (a) FULL vs (a′) CONTENT-LOBOTOMY, **confabulation** | reduction **> 0** with 95% CI **excluding zero** |

### 6.2 H-E3b's margin — derived, not assumed

The margin is **not** set at 0.03. It is fixed by a rule frozen here and evaluated once on the
calibration split at SP2:

> **m = the smallest multiple of 0.005 that is ≥ 2.4866 · SE**, where `SE` is the calibration-measured
> paired-difference SD of behaviour-typed credit between (a) and (b), scaled to the eval cell count.
> The constant **2.4866 = z₀.₉₅ + z₀.₈₀ = 1.645 + 0.8416** is exactly the value at which the
> non-inferiority test declares non-inferiority with **80% probability when the two policies are
> truly equal**. A margin below it buys a claim the test cannot reliably make.
>
> **Cap: m ≤ 0.05.** If the rule demands more than 0.05, **H-E3b is declared
> INDETERMINATE-BY-DESIGN, the sequence breaks there**, and the reason is reported: at more than 10%
> of the credit scale, "non-inferior" is not a claim worth making.

**At E2's measured SE (0.0136, inflated ×1.33 to 0.0181) the rule returns m = 0.045.** For the
record, at that SE: margin 0.03 → 50.5% and margin 0.045 → 80.0% when the policies are truly equal;
at E2's measured **+0.0500** credit advantage every margin from 0.03 up declares non-inferiority
≥ 99.7% of the time. **The rule is frozen; the number it returns is whatever the calibration split
gives.**

### 6.3 Power, computed before the data exists

E2's measured SEs on the corresponding contrasts, inflated **×1.33** for E3's smaller per-rung cell
count and its cross-rung correlation (derivation: `E3_DESIGN.md` §4).

| test | SE used | binding value | power |
|---|---|---|---|
| **H-E3a** | 0.0225 | **4.41pp** (1.96·SE exceeds the 3pp floor) | **99.9%** at E2's measured 11.5pp · 87.6% at 7pp · 60.4% at 5pp |
| **H-E3b** | 0.0181 | m by §6.2 | 80.0% against a true null by construction; ≥99.7% at E2's measured +0.0500 |
| **H-E3c** | 0.0237 | **+0.0464** | **59.7%** at E2's (v)–(vii) analog **+0.0522**; 93.6% at E2's (vi)–(vii) **+0.0825** |
| **H-E3d** | unknown — **no prior exists**; E2 never ran this contrast | 1.96·SE | **80%-power MDE ≈ 5.0pp** at SE 0.018; ≈ 3.4pp if the tight pairing gives SE 0.012 |

**These four rows are registered as stated, including the weak ones.** H-E3c is a coin flip at its own
best prior, because E2's credit attribution was measured with a *rate-matched random gate* and E3's
SHUFFLED-FOK is a permutation, which is not the same comparator. **H-E3d has no prior at all**: (a)
and (a′) differ only in the annotation and retrieve the same items, so the pairing is unusually tight
and the SE may be smaller than the table assumes — **which is a reason the MDE is registered as a
range rather than a point, not a licence to pick the favourable end after the fact.**

### 6.4 Frozen interpretations

**H-E3d, both directions, frozen verbatim:**

> **HOLDS →** *"The confabulation payoff requires lifecycle CONTENT, not caution alone. A policy given
> the same caution instruction over the same retrieved facts, with only the per-fact lifecycle
> annotation scrambled, confabulates measurably more — so the mechanism is the store's lifecycle
> information reaching the answer step, not the instruction's tone. This resolves the mechanism E2
> could not separate, because E2's τ_NOK = 0.00 made its caution step unconditional."*
>
> **FAILS →** *"Generic always-on caution suffices. Scrambling the lifecycle annotation does not
> measurably change confabulation, so the payoff we attribute to obligation monitoring is obtained by
> telling the model to be careful. The paper says so in those words, and the NOK channel is reported
> as a monitoring result with no demonstrated control payoff."*

**H-E3a FAILS →** *"The policy does not survive an evolving store. Its confabulation advantage over
always-retrieve, established on a static store in E2, does not reproduce when the store is replayed
in steps, and the paper may not claim a deployment result for it."*

**H-E3b FAILS →** *"The policy's cost saving is bought with quality on an evolving store. The
abstention it produces is not free, and the operating point derived on a static store is the wrong
one for a moving one."*

**H-E3c FAILS →** *"The credit advantage is the policy scaffold, not the monitor's information. A
monitor whose FOK judgments are permuted performs indistinguishably from one whose judgments are
informative, and E2's +0.0522 does not reproduce against a permutation comparator on an evolving
store."*

---

## 7. Registered descriptives

Registered now so none can be selected after the fact. **None gates anything.**

1. **Staleness trajectory.** FULL's advantage over always-retrieve at each rung, against that rung's
   measured accumulated-supersession count (**2 / 59 / 123 / 165** on the eval personas). The pre/post
   window is real and is the reason the ladder is informative: **all 206 dated change events in the
   corpus resolve at session ≥ 11**, so rung 14 sits at 1% of accumulated staleness and rung 32 at
   100%. **Registered prediction: the advantage is non-decreasing across the four rungs.** Reported
   as observed, in whichever direction it lands.
2. **Per-session serving cost**, cached and uncached, at the **D44-corrected** prices
   (`RESULTS_E2.md` §3.11-R: gpt-5.4 $2.50/$15.00, gpt-4.1-mini $0.40/$0.10/$1.60 per 1M),
   **including both index-maintenance columns separately** — write-driven µs/write and clock-driven
   ms/serve. The published §3.11 dollar figures are superseded; E3 quotes only §3.11-R.
3. **Near-miss vs off-topic split at session scale.** E3 has **no ablation-induced absence**, so this
   is natural-absent probes against genuinely-not-yet-written content — the deployment version of
   E2's split.
4. **τ_NOK = 0.00 and its consequences**, reported as a finding in its own right: the derived
   operating point makes the application step unconditional, which is why the NOK channel needed a
   content lobotomy rather than a trigger permutation to test at all.
5. **Absence-mix trajectory** — the eval absence share falls 59.5% → 59.2% → 57.6% → 46.6% across the
   ladder as the store fills. Reported because it is the design's largest confound and because the
   label fixed effect is load-bearing against it.
6. **Arm (a″) CAUTION-ONLY**, descriptive: E2's `S2` on (a)'s retrieved set, giving the three-point
   mechanism ladder *no caution → caution only → caution + annotation*. **Added so that H-E3d's
   frozen HOLDS text — which says "not caution alone" — is licensed by an observed caution-alone arm
   rather than inferred from a scrambled one. It gates nothing and cannot bias any test.**
7. **Scramble destruction rate** per (persona, rung), and the count of degenerate persona-rungs.

---

## 8. Stop points

| | when | reports | blocks |
|---|---|---|---|
| **SP1** | now | this file, frozen; tag `e3-sp1` | any build, any elicitation |
| **SP2** | post-calibration, pre-eval | derived τ with its derivation, power recomputation, k decision, artifact shas, six-item checklist | any eval-cell call |
| **SP3** | post-eval, pre-scoring | raw outputs committed, census, deviations, cost, `SCORING_MANIFEST_E3.md` — **NO METRIC** | any gate being read |

**SP2 mechanical checklist (conditional go), six items.**
1. every policy parameter **derived and frozen** as a committed constant, on calibration data only;
2. **power reported, bands untouched**;
3. **k per lane precedent** — E2 ran k=1 on the eval split under the same answerer and lane; k is
   recorded with the precedent it rests on;
4. **cost projection < $15** including every riding arm;
5. **`assert_clean` passes** at the boundary — `git status` clean over the guarded trees and every
   path a committed tool reads from tracked or hash-accounted;
6. **zero eval-cell contact to date.**

**All six pass → proceed through the eval phase to SP3 under the standing conditional go. Any
failure, or any non-routine deviation, stops the run and reports.**

**Judge validity spot-check:** 20 rung-context items on E2's protocol — blinded, selected using only
the pinned judge's own output. **Reported, no bar**, gating nothing.

---

## 9. Eval hygiene

> **No eval-cell answer text and no eval-cell score is to be observed before the SP3 go — not by me,
> not by any script's stdout, not in a log tail.**

Enforced, not merely intended: the eval runner prints **counts, statuses, costs and hashes only**; it
holds no scoring code and imports none; answers and judgments are written straight to disk. **No
scoring script may be executed against eval outputs before the SP3 go.** SP3 reports census,
deviations, cost and the scoring manifest — and nothing else.

**One E3-specific hazard, named:** the staleness trajectory is tempting to inspect mid-run because it
is a *descriptive*. It is computed from eval outcomes and is **inside the hygiene fence like
everything else.**

---

## 10. Deviations, amendments, and the phase-boundary assertion

Numbered continuously from **D49-E3** in `DEVIATIONS_E3.md` with dispositions (D45–D48 were opened by
the STEP-0 probes). Amendments are dated committed files; **a frozen prereg is never edited**. Cache
keyed `(item_id, rung, arm, model, prompt_hash)`. Seed 42, temperature 0. `assert_clean.py` at
**every** phase boundary; **an untracked file that a committed artifact reads from is a stop
condition**, not a warning. A non-routine deviation stops the run before scoring.

---

## 11. Scope fence

No paper-text edits. No E2 artifact modifications. No FR repo changes. No renderer changes — L1 is
E1's intact index. No re-ingestion, no relabelling, no rubric edit, no new probe round, no new store.
**No band, margin or design edit after this commit except by dated amendment.** Calibration-only
contact until the SP2 checklist passes. No scoring code executed against eval outputs before the SP3
go.
