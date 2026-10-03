# ADDENDUM_CF2 — registration for the powered store-counterfactual cell

Frozen against baseline HEAD `35743cb`, 2026-09-12 (branch `[BRANCH]`), **BEFORE any
store version, index, label, monitor score or baseline score exists**. Spec:
`reviews/CF2_SCOPE.md` (the read-only scoping pass of 2026-09-11) plus the eight rulings
R1–R8 of 2026-09-12 and the two rulings that followed them the same day (composition fixed at
100/60/30; draw-time individuation on all three states). Rules inherited from
R74/R76/R77/R81/R82 and from `e1r_robustness/SPEC_E1R.md`: nothing unregistered may be
reported; no committed value is recomputed; registered verdicts are never re-adjudicated;
**publish-regardless** — every result prints under its frozen text, including the ones that
go against the paper.

Budget: metered, two keys, itemised in §10. Anthropic key **$130** held, ceiling **$121**
(Haiku 4.5 $16; Opus 5 $105, the Opus line conditional on §11). OpenAI key **$22** held,
ceiling **$2**. Construction spend to date **$0**.

Ledger: `r82_counterfactual/cf2/NUMBERS_CF2.md`, section `AUX-CF2`. Every reserved key is
named in §9 and every one of them is written, including the ones that print a dash.
Verifier: `r82_counterfactual/tools/verify_cf2.py`. **It must exist and pass on the empty
cell before any store version exists**; R82 named `verify_r82.py` at `ADDENDUM_R82.md:15`
and never wrote it (`reviews/CF2_SCOPE.md:75-76`), and this registration does not repeat
that.
Deviations: `r82_counterfactual/cf2/DEVIATIONS_CF2.md`, own numbering from **D-CF2-1**. CF-2
writes into no other deviation file.

---

## §1 — Why this cell exists

CF-1 (`ADDENDUM_R82.md` §7, item CF-1) was the load-bearing test that the obligation gain
survives on questions that cannot carry the label. It **failed**: `gpt-4.1-mini` on v2
reached indexed NOK 0.5939 against the 0.5 identity, item-level interval
[−0.0345, +0.2315] including zero (`r82_counterfactual/NUMBERS_R82.md` §6; the
question-clustered interval excluded zero and the weaker reading governed). D-R82-4
(`r82_counterfactual/DEVIATIONS_R82.md:55-58`) diagnosed the design rather than the effect:
twenty of the thirty positives were states the v2 index only counts, so a third of the
positives carried the aggregate and the test was low-powered by construction.

This cell is the powered replication. **190 (persona, slot) pairs — 100 supersession, 60
retraction, 30 expiry — each asked of three versions of its own store, n = 570, 190
positives, 100 of them in the state the v2 summary names.** The construction rule, the
renderer, the readers and the estimators are CF-1's; what changes is size, the draw-time
admission predicates that CF-1 applied after the fact, and one added index arm.

The added arm tests the second claim directly. The paper says the lookup and the smallest
reader take nothing from the retracted and expired **counts** in the superseded-only summary
(`paper_v4.tex:653`). **V2R** keeps every byte of v2 except those two count fields, which are
permuted across the store versions of the cell; if a reader's judgment moves under V2R, the
reader was reading the counts.

Power, from the Phase 3 script of `reviews/CF2_SCOPE.md` re-run at the ruled composition on
the committed CF-1 rows (`reviews/CF2_REG_REPORT.md` Step A): **P1** clears 0.80 on every composition of the grid (share of draws whose item-level interval excludes chance: 1.000, 1.000, **0.999** at 100/60/30); **P2 on Haiku 4.5** clears on every composition (0.999, 1.000, **0.998**) and on Opus 5 (1.000 throughout); **P3 on Haiku 4.5** clears on every composition (1.000 throughout). The `gpt-4.1-mini` named-minus-counted reading clears on none (0.401, 0.395, 0.313), which is why it is descriptive in §7. What the ruled composition gives up against 100 retraction pairs is one descriptive row: the per-state retraction reading under v2 falls from 0.902 to 0.517 on `gpt-4.1-mini` and from 0.858 to 0.378 on Haiku 4.5. All nine runs reproduced the committed CF-1 item intervals to 1e-9 before simulating. The persona-clustered interval of §6 was not simulated (the scope's caveat 3); this is item-level power.

## §2 — The construction rule (frozen)

**The PN version is what the store would contain after that event**, produced by replaying
FR-Bank's own write path (`lifecycle_bank.py:766-787`), exactly as `ADDENDUM_R82.md` §2 and
`r82_counterfactual/tools/build_cf_cell.py` (`ef351e9`) do it. Supersession appends a
successor on the same `slot_key` at confidence 0.9 and the branch at `:766-777` deactivates
the original when 0.9 clears the category threshold; retraction appends a retracting entry
the same way with `is_retracted=True` (Amendment 2); expiry adds no entry, moves the
original's `event_time` to `cutoff − 30 d`, and appends an `expiring_logistics` record with
`status: expired` so that the label path (date arithmetic, `e0_common.py:252-254`) and the
index path (YAML status, `index_v2.py:240-249`) record the same event and are asserted to
agree. PRESENT is the store as it stands; ABSENT removes the slot through scrubbed-slot
closure with the category left populated. Assertion families A–E of `build_cf_cell.py` are
carried over unchanged; any failure is a STOP.

**Two admission predicates move from build time to draw time**, for all three states:

1. **Individuation.** For each candidate, the unmodified bank is rendered through
   `true_lifecycle → view → render_v3 → named_sections` and the candidate is rejected when
   its scrubbed slot name (`index_v2.scrub`, the path up to the first colon) is already on
   its own state's name section in PRESENT. CF-1 computed this after the questions were
   frozen (Amendment 3) and lost 5 of 20 counted-state pairs to it
   (`reviews/CF2_SCOPE.md:176-191`); here a pair that would not individuate is never drawn.
2. **Superseded-list exclusion.** The candidate is also rejected when its scrubbed name is on
   the v2 superseded-names list in PRESENT, so the superseded-names matcher (§6) reads a
   clean list for every pair, supersession pairs included.

Because both are candidate predicates, the pooled counted-state population is all
individuating by construction and no collision row prints. The scrubber itself is unchanged.

**The expiry class widens to every category (O3).** The check recorded in
`reviews/CF2_REG_REPORT.md` Step B established that the EXPIRED state and the PN label under
UPCOMING intent are assigned by the same rule regardless of category: `is_expired` reads
only `event_time` and the pinned `cutoff` (`e0_metamemory/tools/e0_common.py:252-254`,
`:176-180`); `build_e1.label` unions the whole expired set into the obligation set with no
category test (`e1_metamemory/tools/build_e1.py:129`, `:133`); the (state, intent) → label
table is a two-key lookup with `EXPIRED ∈ OBLIGATION_TABLE["UPCOMING"]`
(`smb/smbgen/labels.py:48`, `:101-102`). The two-category look of CF-1's expiry pool was a
selection choice, not a rule. The widened candidates take the same PN construction: the
anchor moves and the YAML `status: expired` record is appended, so the index-path agreement
in the paragraph above holds for them by the same assertion.

## §3 — Population (frozen)

**190 pairs: 100 supersession, 60 retraction, 30 expiry**, drawn by the amended
`r82_counterfactual/tools/select_pairs.py` at seed 42. The R1 sizing of 100/100/30 (230
pairs, n = 690) was superseded by ruling on 2026-09-12: at k = 5 on Opus 5 it exceeds the
Anthropic key at 1.3× the expected spend (§10), and the retraction pool at 100 eligible
needs about 565 candidate reads against 339 at 60 (§3.2).

**Allocation.** Up to **four pairs per persona per state** (R2); at most one pair per
(persona, scrubbed slot name), so that two pairs of one persona never share a name section
entry; classes offered in scarcity order recomputed from the census immediately before the
draw (expected EXPIRY, RETRACTION, SUPERSESSION); within a class the lexicographically
smallest eligible entry id wins, as in CF-1. **The clustering unit is the persona.** With
more than one pair per persona, persona-, question- and pair-clustering are no longer the
same partition, so the choice is made here: the clustered interval in §6 groups by persona.

**Candidate predicate** (CF-1's, `select_pairs.candidates_for`): the entry carries a
`slot_key`; that `slot_key` occurs exactly once in the whole bank; the entry is active, not
retracted, supersedes nothing; its text holds at least six content tokens; **and** it passes
both §2 draw-time predicates. **Class predicate:** supersession takes a null `event_time` in
an attribute or preference category; retraction takes a null `event_time` in
`PROJECTS_ENDEAVORS`; **expiry takes a non-null `event_time` at or after the persona's pinned
cutoff in any category** (O3). `t_now` = newest active `created_at` + 24 h and
`cutoff = t_now − 14 d`, pinned from the unmodified bank.

**Supply**, from the census of `reviews/CF2_SCOPE.md` Phase 2, reproduced exactly on
2026-09-12 (`reviews/CF2_REG_REPORT.md` Step B: every stage count, the 16 eligible ids and
the 9 ineligible ids match):

| Class | CLEAN under zero overlap | Adjudicated ELIGIBLE | Unadjudicated | Expected eligible **[est]** |
|---|---:|---:|---:|---|
| Expiry, frozen two-category predicate | 25 | **16** | 0 | — |
| Expiry, O1 (CF-1's ten re-admitted) | 10 | 10 (9 individuate) | 0 | — |
| Expiry, O2 (four removed by the 84 overlap) | 4 | 4 | 0 | — |
| Expiry, O3 (widened class) | **41** | 0 | 41 | ≈ 30 at 0.739 |
| Retraction | 1,043 | 1 | 1,017 | ≈ 180 at 0.177 |
| Supersession | 3,133 | 0 | 3,130 | ≈ 2,400 at 0.769 |

The adjudicated, individuating expiry supply is therefore **29**, not 30: `rosa lb_00522`
(`event:toast_planning`) is one of CF-1's ten and fails the draw-time individuation check,
because `event` was already on rosa's expired list in PRESENT. The thirtieth expiry pair and
any slack come from the 41 O3 candidates after adjudication. The R2 cap bites on `patrick`
(five clean eligible under the frozen predicate, all one conference) and on `diane` (five O3
candidates); the one-per-scrubbed-name rule bites on `david`, `diane`, `marcus` and `priya`
(41 O3 candidates over 35 distinct names).

**Overlap, disclosed.** O1 re-admits CF-1's ten expiry pairs, overlap with the 90 by
`(persona, entry_id)`; O2 re-admits four entries that the zero-overlap filter against the 84
(the cross-model question set, `e1xv_crossvendor/manifests/cell_84.json`, overlap by
`pn_members` and slot-ablation ids) had removed. Both lists print in §12.2. No other pair
overlaps the 90, the 84, or the 36 (`r74/x5/x5_render.json`) at the id level named for each.

### §3.1 — Eligibility criteria, written before any verdict

Verbatim from `ADDENDUM_R82.md` §3.1, frozen:

- **Expiry.** An expiry obligation exists only when a one-off event with a fixed date has
  passed and nothing in the record renews, recurs, or persists past that date. Recurring
  events, standing policies, and open-ended provisions are not expiry candidates under any
  intent.
- **Retraction.** A retraction obligation exists only when the record states a specific,
  cancellable plan or commitment held by the user, such that a later cancellation of that
  plan makes the record wrong to surface under UPCOMING intent. Recurring commitments,
  completed history, third-party facts, and standing dispositions are not retraction
  candidates.
- **Supersession.** A supersession obligation exists only when the record asserts a single
  current value of a single-valued attribute of the user or their immediate circle, such
  that a later replacement value makes the old value no longer licensed under CURRENT-STATE
  intent. Multi-valued or accumulating attributes, historical statements, and records
  asserting an absence are not supersession candidates.

**Adjudication protocol.** The author reads. The 41 O3 expiry candidates are adjudicated
**exhaustively, in persona order, before the draw and blind to it**, as CF-1 adjudicated its
46. Retraction and supersession are adjudicated on every drawn candidate under the
seed-ordered walk, stopping at the sixtieth and hundredth eligible respectively. Existing
CF-1 verdicts are reused, never re-adjudicated. **The plan-marker pre-filter is triage, not
selection**: it may order the retraction reads so that likely-eligible records are read
first, but every drawn candidate receives a verdict under the criterion above and no
candidate is rejected by the filter. Every verdict, including every rejection, is recorded
in `r82_counterfactual/cf2/adjudication_cf2.json` before any question is drafted.

**Adjudication notes, 2026-09-12 (amendment text under §14; the criteria above are unchanged).**
Recorded by the author while reading `reviews/CF2_ADJUDICATION_READ.md`; the verdicts are in
`r82_counterfactual/cf2/adjudication_cf2.json` and merged into the queue by (state, entry_id).
The method and read telemetry are ledgered as `AUX-CF2-ADJUDICATION-{EXPIRY,RETRACTION,SUPERSESSION}`.

- EXPIRY: a plan for one dated edition of a yearly event is a one-off (E); a standing yearly practice is not (I). Applied to 0009, 0044, 0070 (E) and 0062 (I). Consistent with CF-1's battalion_chiefs_conference_2026 verdict.
- EXPIRY: an attribute of a one-off dated event (a budget, a role, a guest count) expires with it (E), consistent with CF-1's event_space_capacity verdict.
- EXPIRY 0051 (six-week Saturday class): author's call E, 'weak E': a bounded course ends; the weekly sessions sit inside one enrolment.
- RETRACTION: 'considering', 'interested in', 'wants to', 'aims to' are dispositions, not commitments (I). 'plans to', 'intends to', 'is planning', 'is organizing' are commitments (E). Recurring commitments (monthly, weekly) are I. Savings horizons are I. Offers received and suggestions by others are I. Already-cancelled plans are history (I). Ongoing activity ('is pursuing', 'is implementing') is I.
- RETRACTION 0120 (chenoa, project, rank 3) was read and judged ELIGIBLE by an ordering error: chenoa's 0040 (project) was already ELIGIBLE, so 0120 should have been skipped. Verdict recorded; the one-per-(persona, scrubbed name) rule excludes it at the draw.
- SUPERSESSION: preferences, habits, routines, current statuses, amounts and prices are single current values (E). Lists and accumulating attributes (tools used, genres produced, years of experience), history ('grew up', 'received at 34', 'spent 35 years at'), fixed identity facts (clan, native language), and plans are I. Author read 0037 (truck currently in the shop) as an event rather than a status: I.

### §3.2 — Adjudication

Filled at freeze. The table below is the skeleton; the retraction rate is a fact about the
corpus and prints beside the per-state rows.

| Class | Adjudicated | Eligible | Rate | Reads to reach the target **[est]** |
|---|---:|---:|---:|---:|
| Expiry, O3 (exhaustive) | 41 | — | — | 41 |
| Retraction | — | — | — | ≈ 339 at 0.177 |
| Supersession | — | — | — | ≈ 130 at 0.769 |

## §4 — The questions (frozen renderer)

**CF-1's renderer, unchanged (R3).** `r82_counterfactual/tools/draft_questions.py`:
`gpt-4.1-mini`, temperature 0, seed 42, `max_tokens` 400, three paraphrases, the frozen
SYSTEM and USER prompts; the prompt sees the persona's display name, the slot attribute path
verbatim, and the intent word, and nothing else. Frozen prompt sha256
**`b748247b3ff380d8c24a3e142e2c37c12718942438c3a96cce476531692a8c7f`**. That digest binds
the two prompt texts together with the model id, temperature, seed, `max_tokens` and
paraphrase count (`draft_questions.py:128-131`); all seven are unchanged, so it must
reproduce at drafting time or the draft stops. The questions sha256 over the 190 selected
strings is recorded at freeze. The intent gate is unchanged: `intent.type_question` under
AV2, text-only Rule 2; UPCOMING must type UPCOMING, CURRENT-STATE must return no marker; on
failure the next paraphrase, then one redraft at seed 4242, then STOP. The question is
drafted before any store version exists.

The R74 X5 one-voice renderer is not used, for one reason: on a counterfactual cell the
question is fixed across the three versions, so authorship cannot carry the label and blind
is 0.5 by identity (§6); the one-voice control answers a coupling this cell has already
removed by construction.

## §5 — Index arms (frozen)

- **v2** is the committed renderer under TRUE provenance, `index_v2.render` unchanged.
- **v3** is `r82_counterfactual/index_v3.py`, unchanged: it wraps `index_v2.render` and
  appends the retracted and expired name sections; the v2 prefix of every v3 index is
  asserted byte-identical.
- **V2R** is the count-randomized arm, new: `r82_counterfactual/index_v2r.py` wraps
  `index_v2.render` and rewrites exactly two fields, the retracted-content count and the
  expired-content count, with values **permuted across the store versions of the cell** under
  a recorded seed-42 permutation, so that every count value that appears in the cell appears
  the same number of times and no version keeps its own. Outside those two fields V2R is
  asserted byte-identical to v2 for that version (the RENDERER LOCK, as `index_v3.py:61`).
  The permutation, the field offsets and the assertion are defined **before any index
  exists** and recorded under `AUX-CF2-V2R-DEF`.

Serialization is byte-stable. The existing leakage screen (`ladder_e1.py`, 30 items,
threshold 3, seed 42) runs on a sample of the **v3** indexes and on a sample of the **V2R**
indexes; each must return at most 3 of 30 correct, and both results are ledgered
(`AUX-CF2-LEAKSCREEN-V3`, `-LEAKSCREEN-V2R`). R82 reserved `AUX-R82-CF-LEAKSCREEN` and never
wrote it (`reviews/CF2_SCOPE.md:84-87`); a missing leakage row is a STOP here.

## §6 — Monitors, estimators, and the blind identity

**Readers (R4).** `gpt-4.1-mini` at temperature 0, one call; Haiku 4.5 at k = 5,
temperature 0, under the X4 protocol; Opus 5 at k = 5, temperature unset, **conditional on
§11**. Draw collapse is `score_cf.load_lane` with `MIN_DRAWS` 3 and the arithmetic mean,
unchanged. Prompts are `prompts_e1` verbatim, digests asserted at import (`run_cf.py:43-46`).

**Arms (R5).** BLIND, one unit per question reused across that question's three versions;
INDEXED-V2; INDEXED-V3; INDEXED-V2R. **Blind AUROC is 0.5 as an identity**, for the reason
`ADDENDUM_R82.md` §6 gives: the blind score is constant across a question's versions, so
every within-question pair ties and every cross-question pair contributes exactly one win.
It prints rather than being suppressed; the paired gain is the indexed value minus 0.5.

**Estimators (R2).** Mann-Whitney rank AUROC with ties at 0.5 (`common_e1r.auroc`). The
**item-level paired bootstrap** (`common_e1r.boot_item`, 1000 draws, seed 42, single-class
draws discarded) is **primary**. The **persona-clustered paired bootstrap**
(`common_e1r.boot_cluster` with the group vector set to persona, replacing `pair_id` at
`score_cf.py:120`) prints beside it. **A prediction holds only when both intervals agree;
when they disagree the weaker reading governs** (the D.2 rule). Tolerance **±0.05**
throughout. Two further estimators are registered here because R82 made per-state rows
descriptive only: the **per-state paired interval** (the same `boot_item` restricted to one
state), and the **two-subset difference bootstrap** `boot_subset_diff_ci` (the function of
that name in the Phase 3 script at `reviews/CF2_SCOPE.md:431-437`, ported into
`score_cf.py` unchanged), which resamples two disjoint item sets within themselves and
returns the percentile interval of the AUROC difference; it is the estimator for P2. P5 is
an **equivalence reading**: the paired interval of the V2R-minus-V2 difference must lie
inside [−0.05, +0.05].

**Baselines** on the same 570: the superseded-names embedding matcher on v2; the all-states
matcher over the three named sections on v3; the whole-map matcher on v2. Any baseline
exceeding a reader on any row prints, and no row is dropped.

NOK AUROC, PN against the rest, is primary. FOK is **descriptive only and labelled so**.

## §7 — Registered predictions (five)

Tolerance ±0.05. "Interval" is the item-level paired bootstrap, read together with the
persona-clustered interval under the D.2 rule of §6.

- **P1.** Under the superseded-only summary (v2), `gpt-4.1-mini`'s obligation judgment on
  the whole cell exceeds the 0.5 that a question-only reader attains here, with the interval
  excluding zero.
- **P2.** Under the same summary, on **Haiku 4.5**, the judgment on the state the summary
  names (supersession, 100 pairs) exceeds the judgment on the two states it only counts
  (retraction and expiry pooled, 90 pairs) by more than tolerance, with the two-subset
  interval of the difference excluding zero. **Opus 5 is a conditional branch** of the same
  prediction: it prints HELD or FAILED if the lane runs under §11 and a dash if the lane is
  dropped. The same reading on `gpt-4.1-mini` is **descriptive** and carries no prediction:
  the Phase 3 simulation does not bring it to 0.80 at any size on the grid.
- **P3.** Under the all-three-named summary (v3), Haiku 4.5's judgment on the pooled counted
  states (90 pairs, all individuating by construction) exceeds its value under v2 on the same
  90 by more than tolerance, with the paired v3-minus-v2 interval excluding zero.
- **P4.** Under v2 the superseded-names matcher is within tolerance of `gpt-4.1-mini` on the
  whole cell; under v3 the all-states matcher is within tolerance of Haiku 4.5 on the whole
  cell. Prints either way.
- **P5.** Randomizing the retracted and expired counts moves no reader: on `gpt-4.1-mini`
  and on Haiku 4.5 the paired V2R-minus-V2 interval on the whole cell lies inside
  [−0.05, +0.05]. **Opus 5 conditional** as in P2. Prints either way.

P1 is the load-bearing replication. P5 is the direct test of the count-blindness claim at
`paper_v4.tex:653`.

## §8 — Frozen branch text

These texts were drafted before §7 was written down, in the order the instruction required,
and each clause is a fact the cell itself establishes (the D-R82-4 rule: no clause about a
population this cell did not measure). `$X$`, `$D$`, `$I$`, `$Y$` and `$N$` resolve to
`AUX-CF2-*` ledger keys at print time; no number enters the manuscript except through such
a key. Sentences marked **[MAIN]** carry no internal program vocabulary.

### P1 HOLDS — the obligation gain survives on questions that cannot carry the label

**[MAIN] two sentences:**

> On $N$ questions written before any version of the store existed, and asked of three
> versions of the same store that differ in one attribute each, the smallest model's
> obligation judgment reaches $X$ against the 0.5 a question-only reader attains here, with
> an interval of $I$. The gain survives where the question cannot carry the label.

### P1 FAILS — the gain does not survive at item level

**[MAIN] two sentences:**

> On $N$ questions written before any version of the store existed, the smallest model's
> obligation judgment under the summary that names only superseded content reaches $X$
> against the 0.5 a question-only reader attains here, with an interval of $I$ that includes
> zero. On this cell the gain is not established for that reader.

**Disposition, binding and written now:** the sentence carries no clause about the main
population; the second failure clause that D-R82-4 struck from CF-1 is not reintroduced.
`paper_v4.tex:703` is rewritten to say the powered replication also failed, and the
limitation stands.

### P2 HOLDS — the summary's boundary between named and counted states is the reader's

**[MAIN] one sentence, Haiku 4.5; Opus 5 appended in the same form if the lane runs:**

> Under the summary that names only superseded content, Haiku 4.5's judgment on the named
> state exceeds its judgment on the two counted states by $D$, interval $I$.

### P2 FAILS — the boundary is not the reader's

> Under that summary Haiku 4.5's judgment on the named state exceeds the judgment on the
> counted states by $D$, interval $I$, which is inside tolerance or includes zero; the
> boundary between named and counted states is not established on this cell for that reader.

The `gpt-4.1-mini` row prints beside either branch as descriptive, labelled so. If Opus 5 is
dropped under §11 its row prints a dash with the reason.

### P3 HOLDS — naming the counted states makes them visible

**[MAIN] one sentence:**

> Naming retracted and expired content lifts Haiku 4.5's judgment on those states from $X$
> to $Y$ on the store-counterfactual set ($N$ questions), a paired gain of $D$ with interval
> $I$.

### P3 FAILS — naming does not recover them

> Naming retracted and expired content raises Haiku 4.5's judgment on those states by $D$,
> interval $I$, which does not clear tolerance with an interval excluding zero; the counted
> states are not recovered by naming alone on this cell.

**Disposition:** `paper_v4.tex:656` and the boxed sentence at `:735` are rewritten to the
CF-2 numbers under either branch; under FAILS the builder paragraph loses its last sentence's
number and keeps its claim only as far as the n = 90 cell supports it, labelled n = 90.

### P4 — prints either way

> On this cell the superseded-names lookup reaches $Y$ against the smallest reader's $X$
> under the superseded-only summary, and the all-states lookup reaches $Y$ against Haiku
> 4.5's $X$ under the all-three-named summary.

**Within tolerance** on a pair: the sentence adds "within tolerance". **Outside tolerance**
in either direction: "a margin of $D$ outside tolerance, in the [lookup's / reader's]
favour", and the adverse branch below applies.

### P5 — prints either way

> Randomizing the retracted and expired counts in the superseded-only summary moves
> `gpt-4.1-mini`'s whole-cell judgment by $D$ and Haiku 4.5's by $D$, intervals $I$.

**Inside the band** on both: the sentence adds "both inside the tolerance band; on this cell
neither reader takes anything from the counts". **Outside the band** on either: "which is not
inside the tolerance band; on this cell that reader takes something from the counts", and
`paper_v4.tex:653` is rewritten to name the reader. Opus 5 appended in the same form if the
lane runs, dash otherwise.

### Adverse branch, overriding the above wherever it fires

Any baseline exceeding a reader on any row prints in the table and is named in the text of
the row it affects. No row is dropped for being unflattering.

### Not-applicable convention

A row that cannot be computed prints a dash with a footnote giving the reason. An empty row
is never left to be read as zero. An Opus 5 row dropped under §11 prints a dash with "lane
not run under the drop rule of §11, evaluated 2026-09-19".

## §9 — Ledger keys reserved

`AUX-CF2-CONSTRUCTION`, `-CENSUS`, `-ADJUDICATION`, `-OVERLAP`, `-INDIVIDUATION`,
`-INDEXSIZE`, `-V2R-DEF`, `-LEAKSCREEN-V3`, `-LEAKSCREEN-V2R`, `-BLIND`, `-MINI-V2`,
`-MINI-V3`, `-MINI-V2R`, `-H45-V2`, `-H45-V3`, `-H45-V2R`, `-OP5-V2`, `-OP5-V3`, `-OP5-V2R`,
`-PERSTATE`, `-COUNTED`, `-NAMEDVSCOUNTED`, `-EQUIV-V2R`, `-NB6-V2`, `-ALLSTATES-V3`,
`-NB5-V2`, `-FOK`, `-POWER`, `-SPEND`, `-DROPRULE`. Every key is written; a key that cannot
be computed carries a dash and its reason.

## §10 — Budget and ceiling (R8)

Per-call costs are CF-1's own telemetry over the 2,310 committed rows
(`reviews/CF2_SCOPE.md:487-497`, Batch as billed on the Anthropic lanes, list on mini); V2R
is priced at v2's figure; calls per lane = k × (190 + 3 × 570). Prices were **not re-fetched**
since 2026-08-30 and are re-probed on the launch date (`run_cf.py probe`, three calls per
lane, asserting the served model identifier under the E1.7 rule) before any batch is
submitted. `run_cf.py project` runs and reports against the ceiling below before any
submission; **the run stops at the ceiling.**

| Lane | Calls | Expected | ×1.3 | Ceiling line |
|---|---:|---:|---:|---|
| `gpt-4.1-mini`, k=1, list, `OPENAI_API_KEY` ($22 held) | 1,900 | $1.23 | $1.60 | **$2** |
| Haiku 4.5, k=5, Batch, `ANTHROPIC_API_KEY` ($130 held) | 9,500 | $11.84 | $15.39 | **$16** |
| Opus 5, k=5, Batch, same key, **conditional on §11** | 9,500 | $80.45 | $104.59 | **$105** |
| Construction: 190 question drafts + up to 160 PN records on mini, embeddings | ≈ 350 | < $0.10 | — | **$1** (from the OpenAI line's headroom) |
| **Anthropic total** | | **$92.29** | **$119.98** | **$121 of $130** |

For the record, the two compositions the R1 grid also carried: 100/100/30 projects to
$111.72 on the Anthropic key ($145.24 at 1.3×, over); 100/100/60 to $126.29 ($164.18 at 1.3×,
over). Only the ruled composition fits at 1.3× with Opus 5 at k = 5. Without Opus 5 every
composition is under $22 at 1.3×.

`run_cf.py:197-199` hardcodes the R82 ceiling of $12 and must be raised to the lines above
before the first `project` (build item 9); a `project` run against the old constant is not a
valid pre-submission check.

## §11 — Drop rule for Opus 5 (R7), evaluated on 2026-09-19

Verbatim from `reviews/CF2_SCOPE.md:640-647`. Opus 5 is submitted last, after the mini and
Haiku 4.5 lanes are scored and ledgered, and only if all of: (i) metered spend after those
two lanes is under their combined itemised lines; (ii) the Opus probe (three calls) projects
the lane under its own line; (iii) at least one registered prediction names Opus 5 (P2 or P5
as written), otherwise the lane cannot change a verdict and is dropped before submission. If
dropped, every Opus row prints a dash with the reason and Table 9's Opus rows stay at
n = 90, labelled so. If run, k stays at 5 (Amendment 4's reason: comparability with Tables 20
and 21). A lane that is dropped is never resubmitted after any score exists. **The rule is
evaluated once, on 2026-09-19, and the evaluation is ledgered under `AUX-CF2-DROPRULE`
before the Opus batch is created or the lane is declared dropped.**

## §12 — Candidate and overlap tables

### §12.1 — The 41 O3 expiry candidates, by (persona, entry_id), verdicts to be written

Enumerated on 2026-09-12 by reproducing the Phase 2 census (`reviews/CF2_REG_REPORT.md`
Step B; every stage count of `reviews/CF2_SCOPE.md:206-218` matched before this list was
read). Category, scrubbed slot name and `event_time` date beside each. Verdict column blank
until §3.1 is applied.

| Persona | Entry | Category | Scrubbed name | Event | Verdict |
|---|---|---|---|---|---|
| aisha | lb_00518 | PROJECTS_ENDEAVORS | preparation_for_meeting | 2026-05-18 | |
| aroha | lb_00516 | RELATIONAL_BONDS | professional_backup_relationship | 2026-05-21 | |
| bruna | lb_00529 | PROJECTS_ENDEAVORS | project | 2026-04-29 | |
| callum | lb_00382 | RELATIONAL_BONDS | accommodation_option | 2026-05-07 | |
| callum | lb_00434 | PREFERENCES_HABITS | vehicle_retention_plan | 2045-01-01 | |
| dariush | lb_00233 | PROJECTS_ENDEAVORS | annual_event | 2026-03-20 | |
| david | lb_00423 | PROJECTS_ENDEAVORS | project | 2026-06-01 | |
| david | lb_00477 | PROJECTS_ENDEAVORS | project | 2026-05-09 | |
| david | lb_00486 | PROJECTS_ENDEAVORS | project | 2026-05-09 | |
| diane | lb_00401 | PROJECTS_ENDEAVORS | relationship | 2026-07-12 | |
| diane | lb_00403 | PROJECTS_ENDEAVORS | relationship | 2026-07-12 | |
| diane | lb_00412 | RELATIONAL_BONDS | emotional_state | 2026-07-12 | |
| diane | lb_00416 | RELATIONAL_BONDS | partner | 2026-07-12 | |
| diane | lb_00454 | RELATIONAL_BONDS | birthday | 2026-03-14 | |
| elena | lb_00476 | PROJECTS_ENDEAVORS | wedding_date | 2026-10-01 | |
| elena | lb_00554 | HEALTH_WELLBEING | health_aid | 2026-03-21 | |
| elena | lb_00561 | HEALTH_WELLBEING | mental_state | 2026-04-02 | |
| fatima | lb_00394 | HOBBIES_RECREATION | personal_day_activity | 2026-04-12 | |
| jake | lb_00357 | PROJECTS_ENDEAVORS | project | 2026-02-17 | |
| jake | lb_00361 | PROJECTS_ENDEAVORS | project_role | 2026-02-17 | |
| jerome | lb_00505 | FINANCIAL_MATERIAL | project_savings | 2026-09-14 | |
| jerome | lb_00507 | PROJECTS_ENDEAVORS | project | 2026-09-14 | |
| kofi | lb_00499 | RELATIONAL_BONDS | collaborator | 2026-10-03 | |
| kofi | lb_00582 | RELATIONAL_BONDS | family_member | 2026-05-09 | |
| marcus | lb_00232 | FINANCIAL_MATERIAL | budget | 2026-06-01 | |
| marcus | lb_00237 | FINANCIAL_MATERIAL | budget | 2026-06-01 | |
| mehmet | lb_00443 | PROJECTS_ENDEAVORS | project | 2026-06-01 | |
| pan | lb_00295 | PROJECTS_ENDEAVORS | product_plan_songkran | 2026-04-13 | |
| pan | lb_00485 | FINANCIAL_MATERIAL | vendor_license_fee | 2026-07-15 | |
| patrick | lb_00376 | HOBBIES_RECREATION | class | 2026-05-09 | |
| priya | lb_00322 | PROJECTS_ENDEAVORS | project | 2026-06-01 | |
| priya | lb_00380 | PROJECTS_ENDEAVORS | project | 2026-06-04 | |
| priya | lb_00381 | PROJECTS_ENDEAVORS | project | 2026-06-04 | |
| priya | lb_00389 | HOBBIES_RECREATION | hobby | 2026-05-28 | |
| raj | lb_00512 | PROJECTS_ENDEAVORS | business_job_type | 2026-04-22 | |
| raj | lb_00515 | PROJECTS_ENDEAVORS | upcoming_job | 2026-05-22 | |
| rosa | lb_00512 | RELATIONAL_BONDS | holiday_celebration | 2026-07-28 | |
| saga | lb_00411 | HEALTH_WELLBEING | health_hypothesis | 2026-12-01 | |
| thanh | lb_00563 | FINANCIAL_MATERIAL | shrimp_price_increase_percentage | 2026-05-01 | |
| valentina | lb_00362 | PROJECTS_ENDEAVORS | trip_plan_rioclaro | 2026-05-26 | |
| yoli | lb_00418 | RELATIONAL_BONDS | event | 2026-07-31 | |

Breakdown: PROJECTS_ENDEAVORS 20, RELATIONAL_BONDS 9, FINANCIAL_MATERIAL 5, HEALTH_WELLBEING
3, HOBBIES_RECREATION 3, PREFERENCES_HABITS 1; 23 personas; 35 distinct (persona, scrubbed
name). `callum lb_00434` carries an `event_time` of 2045-01-01 and is listed because the
rule admits it; the criterion decides it.

### §12.2 — Overlap disclosed by (persona, entry_id)

**O1, CF-1's ten expiry pairs, overlap with the 90** (`r82_counterfactual/cf_pairs.json`):
(billy, lb_00273) `project_aircraft:aerial_wildlife_survey`; (david, lb_00496)
`coaching_event_date`; (elena, lb_00488) `event:wedding_timeline`; (fatima, lb_00393)
`trip_schedule:salone_del_mobile_2026`; (marcus, lb_00235) `event:Kayla_graduation_party`;
(marley, lb_00343) `event_transportation`; (mehmet, lb_00429)
`preparation:barber_trade_guild_annual_meeting`; (priya, lb_00324)
`project_deadline:NeurIPS_paper`; **(rosa, lb_00522) `event:toast_planning` — fails the
draw-time individuation check and is not admitted**; (thanh, lb_00468)
`event_guest_count:duc_wedding`. Nine admitted.

**O2, the four ELIGIBLE expiry entries the 84 overlap removed** (`reviews/CF2_SCOPE.md:247`):
(raj, lb_00437), (raj, lb_00443), (raj, lb_00447), (thanh, lb_00476). Four admitted.

### §12.3 — The 16 clean ELIGIBLE expiry candidates under the frozen predicate

(`reviews/CF2_SCOPE.md:223-224`, reproduced 2026-09-12): aisha 517; callum 387; dariush 418,
419; fatima 397; jake 358; kofi 511; marcus 236; marley 344; patrick 343, 344, 345, 349, 350;
rosa 528; valentina 364. Five of the sixteen are patrick's one conference and two are
dariush's one trip; the R2 cap admits at most four of patrick's.

### §12.4 — Table 9 supersession

CF-2 rows print beside the n = 90 rows of `paper_v4.tex` Table 9 (`tab:counterfactual`,
`:1159-1206`) rather than replacing them: the whole-cell rows, the matcher rows, the
per-state block and the counted-state block each gain a CF-2 column labelled n = 570. Opus 5
rows depend on §11. The struck-clause paragraph of Appendix D.2 stays as history. Every
frozen string the change touches (`0.5000 as an identity`, `0.5656 to 0.8489`, `0.7886`,
`0.5939`, the boxed sentence at `:735`) needs its own `CLAIMS.md` authorization block and
passes `frozen_diff.py`.

## §14 — Amendment 1 (D-CF2-1), dated 2026-09-12, BEFORE any acceptance, store version, index, label or score exists

**Retraction quota 60 → 30. Composition 100 supersession / 30 retraction / 30 expiry; 160
pairs; n = 480.** Entered on the measured retraction eligibility rate of the CF-2 walk
(`reviews/CF2_ADJUDICATION_READ.md`, seed-42 round-robin, 440 rows walked): **35 ELIGIBLE
verdicts in 369 verdict reads, rate 0.0949**, 35 usable under the one-pair-per-(persona,
scrubbed name) rule together with the one CF-1 verdict reused, against the 0.177 that §3.2
assumed from CF-1's 62-candidate walk. Filling 60 would have needed roughly 330 further human
reads. The count and rate are ledgered as `AUX-CF2-ADJUDICATION-RETRACTION` from the deposited
`r82_counterfactual/cf2/adjudication_cf2.json`; the deviation is
`r82_counterfactual/cf2/DEVIATIONS_CF2.md` D-CF2-1.

What this amendment supersedes, and nothing else:
- §1 and §3: "190 pairs, n = 570, 100 named-state positives" read **160 pairs, n = 480, 100
  named-state positives**; the retraction quota in §3.2's table is 30 and its read count is the
  measured 369 (439 with rank-skips).
- §7 P3: the pooled counted states are **60 pairs, 30 retraction and 30 expiry positives**,
  all individuating by construction.
- §10: the lines are **mini $2** (expected $1.04), **Haiku 4.5 $13** (expected $9.97), **Opus 5
  $89** (expected $67.75, conditional on §11) — **Anthropic $102 of $130**, expected $77.72,
  $101.03 at 1.3×; calls per lane k × (160 + 3 × 480). The R7 drop rule of §11 stands, evaluated
  on 2026-09-19.
- Power: the Phase 3 script re-run at 100/30/30 on the committed CF-1 rows (gate to 1e-9 on
  all three lanes) gives **P1 0.997, P2 on Haiku 4.5 1.000 (Opus 5 1.000), P3 on Haiku 4.5
  1.000**, ledgered under `AUX-CF2-POWER` beside the three grid points of
  `reviews/CF2_REG_REPORT.md` Step A; P1's whole cell stays above the 450 items at which the grid
  first clears 0.80 on the smallest reader. Descriptive rows that fall: mini's counted paired
  reading (0.828) and every reader's retraction-v2 row.

Unchanged: the candidate and class predicates, the draw-time individuation and superseded-list
exclusion, the cap of four per persona per state, the renderer and the sha, the four arms,
the readers, the estimators and the D.2 rule, the five predictions and every frozen branch text
in §8, the STOP conditions of §13. The retraction per-state rows were descriptive before this
amendment and remain so. No pair had been accepted and no store version, index, label or score
existed when this amendment was entered.

## §15 — Amendment 2 (D-CF2-3), dated 2026-09-12, BEFORE any store version, index, label or score exists

**PN records are read by the author before any store version is built, and a record that fails
the read is re-authored once at seed 4242.** The read asks, of every authored record: *is this a
plausible successor value (supersession) or a plausible cancellation of this specific plan
(retraction), in this person's voice?* — YES / NO-paraphrase / NO-implausible. A record judged NO
is re-authored once with `author_pn.py` unchanged (prompt sha `b6f53b1a…`, predicates, retry) at
**seed 4242**, the question redraft's alternate seed, and re-read under the same question. A
record that fails the second read is handled by D-CF2-2 (§14 rule set): the pair is replaced by
the next ELIGIBLE candidate of its state in walk order under the cap and the one-per-name rule,
its question drafted under §4's frozen renderer, its record authored and read. When a state's
spares are exhausted, that state's quota drops by the shortfall under a further deviation.

The first read (`AUX-CF2-PNREAD`): supersession 69 YES / 21 NO-paraphrase / 10 NO-implausible,
retraction 29 YES / 1 NO-implausible; 32 records re-authored. The 160 questions were read for
value tokens the same day (`AUX-CF2-QUESTIONREAD`: 90 of 160 flagged, against CF-1's 3 of 30;
CF-2's retraction and expiry slots are named after their events, so the question names the
plan) — a disclosure, not a gate, since the question is identical across the three versions and
cannot carry the label.

**What this read guards.** The monitor's input is value-scrubbed: no authored text reaches an
index or a prompt. The read therefore guards **label honesty under Definition 1** — a
paraphrased successor would leave the PN label semantically hollow — and not the measurement.
Nothing else in the registration moves.

## §16 — Amendment 3 (D-CF2-4), dated 2026-09-13, BEFORE any store version, index, label or score exists

**The supersession queue is not extended beyond position 272, and the supersession quota
becomes the count the last D-CF2-2 walk reached, less one for every record that fails its read
from this date on, with no replacement.** Two extensions of the seed-42 walk (positions
166–228 and 229–272; `reviews/CF2_ADJUDICATION_READ_EXT.md`, `_EXT2.md`) and three author's reads
(`AUX-CF2-PNREAD`, `AUX-CF2-PNREREAD`) replaced 45 pairs under §14's D-CF2-2 rule; eligibility on
the walk fell 0.667 → 0.500 → 0.433, the read pass on replacements ran 0.71 and 0.50, the §15 retry
restored 1 record in 50, and the §3 cap of 4 binds on 12 of 40 personas. The walk over 229–272
reached **100 / 30 / 30** (residual shortfall 0). From here: a record that fails its read — one of
the 11 replacements accepted at positions 230–263, or one of the 5 re-authored records awaiting
their last read — is **excluded under D-CF2-4 and the supersession quota drops by one**; the
composition is **(N_sup) / 30 / 30**, n = 3 × (N_sup + 60), recorded in `cf_pairs_cf2.json`
`meta.quota` and `NUMBERS_CF2.md` `AUX-CF2-CONSTRUCTION`. Nothing else in the registration moves:
predicates, renderer, arms, readers, estimators and the five predictions stand.

**Power, conditional.** §14's figures were simulated at n = 480. The Phase 3 grid first clears
0.80 on the smallest reader at n = 450 (150 pairs; N_sup ≥ 90). Should N_sup fall below 90, the
Phase 3 script is re-run at the final composition and its shares ledgered under `AUX-CF2-POWER`
before any store version is built; a P1 share below 0.80 is a STOP under §13.

**Applied, 2026-09-13.** The final read (`AUX-CF2-PNREAD` 164–174, `AUX-CF2-PNREREAD` 39/41/42/47/48)
failed 12 of the 16: the 12 are excluded with no replacement. **N_sup = 88; composition 88 / 30 / 30;
148 pairs; n = 444.** The author's ruling: no spare — the three ELIGIBLE rows admissible after the
exclusions (0215 elena `mental_transition_routine`, 0264 patrick `communication_preference:trauma`,
0272 omar `income_pattern`) stay undrawn and are listed as such in `NUMBERS_CF2.md`. The conditional
power clause fired (12 > 10) and was run at 89/30/30 (n = 447): P1 0.994, P2 1.000, P3 1.000
(`AUX-CF2-POWER`, §3a of the ledger); the 88/30/30 cell lies within three items of that run and is
covered by it — no further re-run. Every §9 key referring to "100 pairs" or "90 pairs" reads 88 and 60.

## §17 — Amendment 4 (D-CF2-5), dated 2026-09-13, BEFORE any Opus 5 batch exists

**The §11 drop rule is evaluated on 2026-09-13 rather than on 2026-09-19.** The date stood for an
ordering — Opus 5 last, after the mini and Haiku 4.5 lanes are scored and ledgered — and that
ordering is met on 2026-09-13. The three checks are unchanged and evaluated once: (i) spend after
the two lanes $10.02 against $18; (ii) the Opus 5 probe projects $56.01 (×1.3 $72.81) against
$105; (iii) P2 and P5 name Opus 5. All pass; the lane runs at k = 5 (`AUX-CF2-DROPRULE`). The row is
not re-evaluated on the 19th. Nothing else in the registration moves.

## §13 — STOP conditions specific to this registration

- Any monitor or baseline call before this file is frozen by the author's commit and GO is
  given at the ceiling.
- `r82_counterfactual/tools/verify_cf2.py` absent or failing when the first store version is
  about to be written.
- Any label mismatch in the 570-item cell, or any write-path predicate that does not fire on
  a PN version, or any expiry anchor not strictly before its persona's cutoff.
- Any pair failing individuation or the superseded-list exclusion at build time: both are
  draw-time predicates, so a failure is an instrument bug, not a corpus fact.
- Any V2R index differing from its v2 outside the two count fields, or any leakage screen
  (v3 or V2R) returning more than 3 of 30, or either screen missing from the ledger.
- Any number printed without a key in `NUMBERS_CF2.md`.
- Any reading written after its numbers exist, or any third reading beyond the branches of
  §8.
- Any lane submitted before `run_cf.py probe` and `project` have run against the §10 lines,
  or the Opus 5 batch created before the §11 rule is evaluated and ledgered on 2026-09-19.
- The Phase 3 script's 1e-9 gate failing on any lane at any re-run, or the census
  reproduction of §3 failing on any stage count.
- The frozen lineage — `draft_questions.py` sha `b748247b…`, `prompts_e1` digests,
  `index_v2.render`, `index_v3.py` — changing by one byte.
- Spend reaching the ceiling with the cell unscored; the run stops and reports rather than
  continuing.
- Any edit to this file after the freeze other than a dated amendment appended in the R82
  form, entered before the numbers it touches exist.

---

## Deviations

`D-CF2-1` — 2026-09-12, the retraction quota 60 → 30 on the measured eligibility rate; §14 above.
`D-CF2-2` — 2026-09-12, a pair failing the authoring predicate after the frozen retry is replaced in walk order.
`D-CF2-3` — 2026-09-12, a PN record failing the author's read is re-authored once at seed 4242; §15 above.
`D-CF2-4` — 2026-09-13, no further queue extension; the supersession quota is what the last walk reached, less one per record failing its read, no replacement; §16 above.
`D-CF2-5` — 2026-09-13, the §11 drop rule evaluated on the 13th rather than the 19th, once; §17 above.
All in `r82_counterfactual/cf2/DEVIATIONS_CF2.md`.
