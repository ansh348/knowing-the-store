# ADDENDUM_R82 — registration freeze for the leak-free counterfactual cell

Frozen against baseline HEAD `3147a05`, 2026-08-29, **BEFORE any store version, index,
label, monitor score or baseline score exists**. Spec: the R82 program instruction of
2026-08-29 plus the four rulings and the three GO riders of the same date. Rules inherited
from R74/R76/R77/R81 and from `e1r_robustness/SPEC_E1R.md`: nothing unregistered may be
reported; no committed value is recomputed; registered verdicts are never re-adjudicated;
**publish-regardless** — every result prints under its frozen text, including the ones that
go against the paper.

Budget: **$12 metered ceiling**, itemised in §10. Construction spend to date **$0.0060**
(question drafting, §4), made under the GO of 2026-08-29 before any store version existed.

Ledger: `r82_counterfactual/NUMBERS_R82.md`, new section `AUX-R82-CF`.
Verifier: `r82_counterfactual/tools/verify_r82.py`.
Deviations: `r82_counterfactual/DEVIATIONS_R82.md`, own numbering from **D-R82-1**. R82
writes into no other deviation file.

---

## §1 — Why this cell exists

The paper's largest measurement exposure is that on its main population the question text
alone predicts the label at AUROC 0.92 to 0.97, because the item-construction taxonomy
determines the label. Blind levels there are contaminated and only paired gains are clean.
The existing authorship-matched control holds 36 items and is underpowered.

This cell removes the coupling by construction rather than by rewriting: **the question is
fixed and the store varies.** One question per pair is asked of three versions of that
pair's store, which differ in exactly one slot. The label is therefore a property of the
store and cannot be a property of the question, and the blind monitor's AUROC is 0.5 as an
identity (§6).

It also tests the second exposure. The summary names superseded content and only counts
retracted and expired content, and discrimination follows that line exactly. A second index
arm names all three states, so the question of whether naming recovers the counted states
becomes measurable rather than inferred.

## §2 — The construction rule (frozen)

**The PN version is what the store would contain after that event.** Each PN version is
produced by replaying FR-Bank's own write path, not by annotating a label onto an unchanged
store. The write path is `lifecycle_bank.py:766-787` and it differs per state, so one rule
has three faithful consequences.

| State | Write path | Net effect on the store |
|---|---|---|
| Supersession | `:766-777`. A new entry with the same `slot_key` and `confidence` at or above 0.80 (0.95 for `ACCUMULATE_CATEGORIES`, `:623-626`) sets `entry.supersedes` to the prior id and `deactivate()`s every active entry on that slot | entries **+1**, active **net 0**, superseded **+1**, and the slot name enters the superseded-names section |
| Retraction | `:779-784`. The retracting entry is added with `is_retracted=True` and `is_active=True`, and every entry at cosine **above 0.85** to it is `deactivate()`d | entries **+1**, active **net 0**, the original goes inactive. The YAML `retractions` record is what makes TRUE call it retracted rather than superseded |
| Expiry | **There is no expiry write path.** Nothing in ingestion deactivates on `event_time`; the extractor only records it (`:724-732`, `:755`) | entries **unchanged**, active **unchanged**; the **event-time anchor** moves and nothing else |

PRESENT is the store as it stands. ABSENT removes the slot's records through the existing
`slot_closure` removal set (`build_e1.py:104-109`), leaving the category populated, so the
manipulation is slot ablation by construction.

**Both label and index paths must agree, and they read different fields.** The label path
takes expiry from date arithmetic, `expired = {i in gold if event_time < cutoff}` via
`PersonaJoin.is_expired`. The index path takes expiry from the YAML `status` field
(`index_v2.py:240-249`), because `PREREG_E1.md` section 3 has YAML status override derived
cutoffs. The expiry PN version therefore moves the anchor **and** records the same event as
`status: expired`, and the two are asserted to agree. This is one event recorded twice, once
by the store and once by the ground truth, not two manipulations.

**Construction predicates, asserted per pair rather than assumed.** Supersession successors
carry the same `slot_key` and clear the confidence threshold for their category. Retraction
entries reach cosine above 0.85 against the original under `text-embedding-3-small`, the
encoder the write path itself uses. Expiry anchors place `event_time` before the persona's
pinned `cutoff`. In addition the TRUE annotation must agree with the store, so `old_fact` is
authored near-verbatim from the existing entry and the lexical detector fires at or above
`TAU_HI` 0.80 with at least `MIN_DISCR` 3 discriminative tokens while the successor stays
under `CROSS_GUARD` 0.34.

**`t_now` and `cutoff` are pinned from the unmodified PRESENT bank** and reused
byte-identically for all three versions of that persona, as `PersonaJoin` requires. A
successor entry is dated at or before `t_now` so no version carries a negative age.

**Registered asymmetry.** The three states do not move the summary equally: supersession
and retraction each add an entry and a name, expiry moves neither. That is a property of
the write path, it is recorded before any number exists, and it is what CF-3 tests.

## §3 — Population (frozen)

Thirty (persona, slot) pairs, ten per state, **one pair per persona over thirty distinct
personas**, drawn by `r82_counterfactual/tools/select_pairs.py` at seed 42. One pair per
persona makes persona-clustering and question-clustering the same partition, which settles
the sensitivity estimator without a choice being made after the fact.

Candidate predicate: the entry carries a `slot_key`; that `slot_key` occurs exactly once in
the whole bank, so the slot carries no lifecycle history of its own; the entry is active,
not retracted, and supersedes nothing; its text holds at least six content tokens. Class
predicate: supersession takes a null `event_time` in an attribute or preference category;
retraction takes a null `event_time` in `PROJECTS_ENDEAVORS`; expiry takes a non-null
`event_time` at or after the persona's pinned cutoff in `OBLIGATIONS` or
`LOGISTICAL_CONTEXT`. Classes are offered in measured scarcity order, expiry first.

### §3.1 — Eligibility criteria, written before any verdict

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

This is the failure mode the paper already documents. Appendix E's ledger row records that
the non-intent-conditional expiry route ran at 20 percent precision, which forced the
intent-conditioned definition (`paper_v2.tex:1046`, table row at `:1137`). The same failure
mode is handled here before freeze rather than after.

### §3.2 — Adjudication

Expiry was adjudicated **exhaustively over all 46 candidates**, in persona order, blind to
which members of the first draw survived. Retraction and supersession pools are far larger,
1590 and 3347, and were adjudicated on every drawn candidate under a bounded seed-ordered
walk, stopping at the tenth eligible item. That asymmetry is disclosed rather than hidden;
its reason is that the expiry pool is both small and the pool in which the failure mode was
found.

| Class | Adjudicated | Eligible | Rate |
|---|---:|---:|---:|
| Expiry (exhaustive) | 46 | 34 | 0.739 |
| Retraction | 62 | 11 | 0.177 |
| Supersession | 13 | 10 | 0.769 |

**The retraction rate is a fact about the corpus and prints beside the per-state rows.**
One candidate in six in `PROJECTS_ENDEAVORS` is a cancellable plan; the rest are standing
practices, completed history, and third-party facts. That is the same reason the main
population carries only 26 retraction obligations out of 104. The class predicate was not
widened to compensate; the walk went deeper under the unchanged rule, 62 candidates against
an 80 cap.

Every verdict, including every rejection, is recorded in
`r82_counterfactual/adjudication.json` and reproduced in §12.

**Descriptive only, never used for selection.** A forward-looking plan-marker pre-filter
over the adjudicated retraction set scores precision 1.000 (6 of its 6 catches are eligible)
and recall 0.545 (it misses 5 of 11), missing the "is considering", "wants to", "is writing"
and "is preparing" commitment forms. This is measured for the October build and enters no
selection here.

## §4 — The thirty questions (frozen)

One question per pair, drafted by `r82_counterfactual/tools/draft_questions.py` before any
store version existed.

**The drafting prompt sees the entity, the slot attribute path, and the intent, and nothing
else.** It never sees the entry's text or value, its category, the other candidates, any
store content, or any label. `slot_key` is store metadata, an attribute path; the value
lives in the entry text, which never enters the prompt.

- Frozen prompt sha256 **`b748247b3ff380d8c24a3e142e2c37c12718942438c3a96cce476531692a8c7f`**
- Frozen questions sha256 **`adec4c831571e409130d5c38282d0f3a56124e659506803c216857f430e9c035`**
- `gpt-4.1-mini`, temperature 0, seed 42, three paraphrases per pair, one selected by a
  seeded index. 30 calls, 9,399 input and 1,430 output tokens, **$0.0060**.

**Intent gate.** Every selected paraphrase is typed by the frozen
`e1_metamemory/tools/intent.py` `type_question`, driven through its text-only Rule 2 path,
and must agree with the pair's registered intent: an UPCOMING pair must return UPCOMING
under Rule 2.2, and a CURRENT-STATE pair must return "no marker fired" under Rule 2.3,
which is the signature of a present-tense coverage question. A past marker firing fails in
both cases. A paraphrase reading as past or change-aware would break the PN label under
Definition 1 whatever the store contains, because `build_e1.label` gates the negative
obligation on intent and exempts PAST-EVENT and CHANGE-AWARE structurally. On failure the
next of the three is taken in order and the substitution recorded; if all three fail the
pair is redrafted once at seed 4242; a pair still failing is a STOP. This is a construction
rule and carries no deviation entry.

Outcome: **30 of 30 pass, all 30 distinct, two substitutions, no redrafts.** Both
substitutions were UPCOMING pairs whose seeded pick carried no forward marker
(`cf:diane:project:chaplain_book`, `cf:fatima:trip_schedule:salone_del_mobile_2026`).

**Disclosed.** A question about a slot necessarily names that slot's topic, so 23 of 30
questions share a content token with their entry text. In three of those the topic word is
also the stored value (`valentina` Excel, `aisha` fatigue, `amara` endometriosis). **None of
this can leak the label**, because the same question is asked of all three versions of that
pair's store; the only quantity it can affect is how easy coverage is to judge, and coverage
is descriptive here (§6). The questions are first-person, where the main population's are
third-person; the cell is compared only within itself, so voice is a disclosure and not a
confound.

## §5 — Index arms (frozen)

- **v2** is the committed renderer under TRUE provenance, `index_v2.render` unchanged.
- **v3** is `r82_counterfactual/index_v3.py`, which **wraps rather than forks** the
  renderer: it calls `index_v2.render` and appends two further flat name sections, for
  attribute names carrying retracted content and for attribute names carrying expired
  content, in the same `name_block` grammar under the same `SLOT_CAP` of 15. The v2 prefix
  of every v3 index is asserted byte-identical to the v2 index for that version. This
  follows the RENDERER LOCK precedent of `e3_metamemory/tools/build_indexes.py:59`.

Serialization is byte-stable and re-running reproduces every index string exactly. The
existing leakage screen (`ladder_e1.py`, 30 items, threshold 3, seed 42) runs on a sample of
the 90 v3 indexes and must return at most 3 of 30 correct.

## §6 — Monitors, estimators, and the blind identity

Monitors: `gpt-4.1-mini` at temperature 0 with one call, as in E1; Haiku 4.5 at k=5 under
the X4 protocol; Opus 5 at k=5, priced separately. Draw collapse is `x4_score.load_lane`
with `MIN_DRAWS` 3 and the arithmetic mean, unchanged. Blind is scored once per question and
reused across that question's three versions, since the input is identical.

**Blind AUROC is exactly 0.5, as an identity and not an approximation.** The blind score is
constant across a question's three versions. Within a question every positive-negative pair
ties. Across any two questions the two cross pairs contribute exactly one win between them.
The value is therefore 0.5 by construction; it is printed rather than suppressed, and the
paired gain is the indexed value minus 0.5.

Estimators are the committed ones: Mann-Whitney rank AUROC with ties at 0.5
(`common_e1r.auroc`); the preregistered item-level paired bootstrap, 1000 draws, seed 42,
single-class draws discarded (`common_e1r.boot_item`), which is **primary**; and the
clustered paired bootstrap (`common_e1r.boot_cluster`) grouped by question, printed beside
it. The clustered variant is the one that preserves the blind identity in every draw,
because a question's three versions move together; that reason is recorded here, before any
interval exists, and does not make it primary. Tolerance **±0.05** throughout. Mixed
outcomes fall to the weaker reading.

Baselines on the same 90: the superseded-names embedding matcher on v2; an all-states
matcher over the three named sections on v3; the whole-map matcher on both. Any baseline
exceeding a monitor on any row prints, and no row is dropped.

NOK AUROC, PN against the rest, is primary. FOK AUROC, non-absent against absent, is
**descriptive only and is labelled so wherever it appears**.

## §7 — Registered predictions (four)

Tolerance ±0.05 throughout.

- **CF-1.** On v2, the `gpt-4.1-mini` indexed NOK exceeds 0.5 with an interval excluding
  0.5.
- **CF-2.** On v2, the superseded-names matcher is within tolerance of the `gpt-4.1-mini`
  monitor on NOK.
- **CF-3.** On v3, for the Haiku 4.5 monitor, NOK on the **pooled twenty counted-state
  items** (ten expiry and ten retraction together) exceeds that monitor's v2 value on the
  same twenty by more than tolerance, with the paired v3-minus-v2 interval excluding zero.
  **Per-state rows at ten positives each are descriptive and carry no prediction.**
- **CF-4.** On v3, the all-states matcher is within tolerance of the Haiku 4.5 monitor on
  NOK.

CF-1 is the load-bearing one and is registered as a genuine test. If it fails, the paired
gain the paper reports on its main population is not free of question signal, and that is
the most important adverse finding the paper would carry.

## §8 — Frozen branch text

Sentences marked **[MAIN]** carry no internal program vocabulary and satisfy S8 to S10.
`$X$`, `$D$`, `$I$` and `$Y$` are placeholders resolving to `AUX-R82-CF-*` ledger keys at
print time; no number enters the manuscript except through such a key.

### CF-1 HOLDS — the obligation gain survives on questions that cannot carry the label

**[MAIN] §4.3 or §7.1, two sentences:**

> Thirty questions written before any version of the store existed were asked of three
> versions of the same store, which differ in one attribute each. The obligation judgment
> reaches $X$ against the $0.5$ that a question-only reader can attain here, an interval of
> $I$, so the gain survives where the question cannot carry the label.

### CF-1 FAILS — the gain does not survive, and the main-population gain is not clean

**[MAIN] §4.3 or §7.1, two sentences:**

> Thirty questions written before any version of the store existed were asked of three
> versions of the same store, which differ in one attribute each. The obligation judgment
> reaches $X$ against the $0.5$ a question-only reader attains here, so the gain measured on
> the larger population is not free of what the question alone gives away.

Disposition, binding and written now: this becomes the paper's most important adverse
finding. The proposed abstract reopens, the obligation-gain claim in §4 is reduced to the
population it was measured on, and the reduction is recorded in the R82 authorization block
as a strength change with this section as its authority.

### CF-2 — prints either way

**HOLDS (within tolerance), [MAIN] one sentence:**

> On these questions a matcher that reads the store's list of superseded names directly
> reaches $Y$ against the monitor's $X$, so the obligation judgment stays close to that
> lookup once the question carries no label signal.

**FAILS in the monitor's favour, [MAIN] one sentence:**

> On these questions the monitor exceeds a direct match against the store's list of
> superseded names by $D$, which is a margin the larger population does not show.

**FAILS against the monitor, [MAIN] one sentence:**

> On these questions a matcher that reads the store's list of superseded names directly
> exceeds the monitor by $D$.

### CF-3 HOLDS — naming the counted states makes them visible

**[MAIN] one sentence:**

> When the summary names retracted and expired content instead of only counting it, the
> obligation judgment on those twenty questions rises by $D$, interval $I$.

### CF-3 FAILS — naming does not recover them

**[MAIN] one sentence:**

> Naming retracted and expired content in the summary does not raise the obligation
> judgment on those twenty questions beyond $D$, so the gap between the state the summary
> names and the two it counts is not closed by naming alone.

### CF-4 — prints either way

**HOLDS (within tolerance), [MAIN] one sentence:**

> Under a summary that names all three states, a matcher over those name lists reaches $Y$
> against the monitor's $X$, so the obligation judgment is available to a lookup there too.

**FAILS in either direction, [APPX] one sentence, naming the direction and the margin
$D$.**

### Adverse branch, overriding the above wherever it fires

Any baseline exceeding a monitor on any row prints in the table and is named in the text of
the row it affects. No row is dropped for being unflattering.

### Not-applicable convention

A row that cannot be computed prints a dash with a footnote giving the reason. An empty row
is never left to be read as zero.

## §9 — Ledger keys reserved

`AUX-R82-CF-BLIND`, `-MINI-V2`, `-MINI-V3`, `-H45-V2`, `-H45-V3`, `-OP5-V2`, `-OP5-V3`,
`-NB6-V2`, `-ALLSTATES-V3`, `-NB5-V2`, `-NB5-V3`, `-PERSTATE`, `-COUNTED20`, `-FOK`,
`-CONSTRUCTION`, `-ADJUDICATION`, `-LEAKSCREEN`.

## §10 — Budget and ceiling

Projection from `ECONOMICS.md` section 1 measured means and the `x4_run.LANES` price table,
with v3 indexes assumed 200 tokens larger than v2's measured 1,201.

| Lane | Calls | Input tok | Output tok | Rate in/out per 1M | Batch | Projected |
|---|---:|---:|---:|---|---|---:|
| `gpt-4.1-mini`, k=1 | 210 | 248,490 | 5,460 | 0.40 / 1.60 | — | $0.11 |
| Haiku 4.5, k=5 | 1,050 | 1,242,450 | 31,500 | 1.00 / 5.00 | x0.5 | $0.70 |
| Opus 5, k=5 | 1,050 | 1,242,450 | 157,500 | 5.00 / 25.00 | x0.5 | $5.07 |
| Construction, already spent | 30 | 9,399 | 1,430 | 0.40 / 1.60 | — | $0.0060 |
| Write-path predicate check, embeddings | 60 | ~3,000 | — | 0.02 | — | <$0.01 |
| | | | | | **Projected** | **$5.92** |

**Ceiling: $12**, itemised `gpt-4.1-mini` $1, Haiku 4.5 $2, Opus 5 $8, construction $1.
`x4_run.py probe <lane>`, which asserts the served model identifier under the E1.7 rule, and
then `x4_run.py project`, both run and report before any batch is submitted. The run stops
at the ceiling.

Main-text budget for the counterfactual result: **one review line**, with a named yield
source. Appendix material is uncounted. Under the standing cut order, if R81 Phase 4 does
not free enough review lines, calibration is cut first, related work second, and **this
result is cut last**.

## §11 — D-R82-1 (recorded here, entered in `DEVIATIONS_R82.md`)

Three items, one sequence.

**What happened.** The frozen selection rule filled ten per state on the first draw, and
inspection of the expiry arm showed that three of ten positives were not obligations at all
and a fourth was borderline: a passed date does not forbid a recurring obligation or a
standing policy. Separately, two bookkeeping errors surfaced during adjudication. Verdicts
were keyed on `entry_id` alone, but entry ids repeat across personas, so `kofi lb_00511`
(eligible) collided with `rosa lb_00511` (ineligible). And one batch of nine verdicts was
adjudicated and never written to the verdict file.

**What changed.** Eligibility criteria were written for all three states, applied to every
expiry candidate exhaustively and to every drawn candidate in the other two classes, and the
population was redrawn under the same seed over the surviving pool. Verdict keys became
`(persona, entry_id)`.

**Why this is admissible.** No label, index, or monitor score existed at any point in this
sequence, so it is construction and not a post-hoc change; the thing that would make it post
hoc is doing it after a prediction fires. The direction is against convenience: the expiry
pool shrank from 46 to 34 eligible, the retraction walk had to go to 62 candidates to find
ten, and no class predicate was widened to compensate. Both bookkeeping errors were caught
by the instrument rather than by inspection, the collision by the persona-keyed rewrite and
the unwritten batch by the selector re-proposing the nine records it had no verdicts for.

**Disposition.** Every verdict, including every rejection, is registered in §12 and in
`r82_counterfactual/adjudication.json`. The retraction eligibility rate of 0.177 prints
beside the per-state rows at integration.

## §12 — Verdict tables

### §12.1 — The thirty frozen questions

Ordered by `pair_id`. Every one passes the §4 intent gate.

| # | state | persona | intent | slot | question |
|---:|---|---|---|---|---|
| 1 | SUPERSESSION | aisha | CURRENT-STATE | `health_condition:fatigue` | Can you tell me the current level of my fatigue? |
| 2 | SUPERSESSION | amara | CURRENT-STATE | `health_condition:endometriosis_flare_season` | How severe is my endometriosis flare season right now? |
| 3 | RETRACTION | aroha | UPCOMING | `project:postgraduate_study` | Can you tell me the next steps I have planned for my postgraduate study? |
| 4 | EXPIRY | billy | UPCOMING | `project_aircraft:aerial_wildlife_survey` | What preparations are planned for the coming aerial wildlife survey in the project aircraft? |
| 5 | EXPIRY | david | UPCOMING | `coaching_event_date` | When is my next coaching event scheduled, David Park? |
| 6 | RETRACTION | diane | UPCOMING | `project:chaplain_book` | What are the upcoming deadlines for my chaplain book project? |
| 7 | RETRACTION | dmitri | UPCOMING | `project:client_portal` | What tasks are planned next for the client_portal project? |
| 8 | EXPIRY | elena | UPCOMING | `event:wedding_timeline` | What events are on my wedding timeline coming up? |
| 9 | EXPIRY | fatima | UPCOMING | `trip_schedule:salone_del_mobile_2026` | What plans do I have for Salone del Mobile 2026 coming up? |
| 10 | SUPERSESSION | jerome | CURRENT-STATE | `vehicle_name` | What vehicle am I driving right now? |
| 11 | RETRACTION | kenji | UPCOMING | `project:case_studies` | What case studies are coming up in my projects? |
| 12 | SUPERSESSION | kofi | CURRENT-STATE | `price_per_bag` | At this moment, what's the price I'm paying per bag? |
| 13 | SUPERSESSION | leila | CURRENT-STATE | `work_passion_discrepancy` | Right now, what aspects of my job don't align with my passions? |
| 14 | RETRACTION | lily | UPCOMING | `project:honours_thesis_microplastics` | What tasks are scheduled next for my honours thesis about microplastics? |
| 15 | EXPIRY | marcus | UPCOMING | `event:Kayla_graduation_party` | Who is invited to Kayla's graduation party that's scheduled soon? |
| 16 | EXPIRY | marley | UPCOMING | `event_transportation` | What travel plans do I have for the events coming up soon? |
| 17 | EXPIRY | mehmet | UPCOMING | `preparation:barber_trade_guild_annual_meeting` | What tasks are scheduled for me before the coming barber trade guild annual meeting? |
| 18 | RETRACTION | mirri | UPCOMING | `project:patrol_schedule_reorganization` | What tasks are included in my upcoming patrol schedule reorganization project? |
| 19 | RETRACTION | nadia | UPCOMING | `project:winter_menu_sauce` | Can you tell me the status of the winter menu sauce project that's coming up? |
| 20 | RETRACTION | pan | UPCOMING | `project:instagram_post_idea` | What is the next Instagram post idea I have planned? |
| 21 | SUPERSESSION | patrick | CURRENT-STATE | `partner_preference:kitchen_cabinets_style` | Can you tell me the current kitchen cabinet style my partner likes? |
| 22 | EXPIRY | priya | UPCOMING | `project_deadline:NeurIPS_paper` | What’s the scheduled deadline for my NeurIPS paper project? |
| 23 | SUPERSESSION | raj | CURRENT-STATE | `budget:arjun_birthday_gift` | Can you tell me the amount set aside currently for Arjun's birthday gift? |
| 24 | EXPIRY | rosa | UPCOMING | `event:toast_planning` | What’s planned for the toast event I have coming up? |
| 25 | SUPERSESSION | saga | CURRENT-STATE | `gift_budget` | Can you tell me the amount I can spend on gifts at the moment? |
| 26 | RETRACTION | samuel | UPCOMING | `project:cranial_approaches_textbook_chapter` | Can you tell me the upcoming tasks I have for the cranial approaches textbook chapter? |
| 27 | EXPIRY | thanh | UPCOMING | `event_guest_count:duc_wedding` | How many guests are expected at Duc's wedding coming up? |
| 28 | RETRACTION | tom | UPCOMING | `membership:gloucestershire_beekeepers` | What upcoming events do I have with the Gloucestershire Beekeepers? |
| 29 | SUPERSESSION | valentina | CURRENT-STATE | `software_preference:excel` | How am I currently using Excel in my projects? |
| 30 | SUPERSESSION | zara | CURRENT-STATE | `design_philosophy_inspiration` | Can you tell me what influences my design approach at the moment? |

### §12.2.1 — Expiry verdicts

exhaustive over the whole pool. Adjudicated **46**, eligible **34**, rate **0.739**. A dot in the last column marks the item the draw took.

| # | persona | entry | verdict | reason | drawn |
|---:|---|---|---|---|:-:|
| 1 | aisha | `lb_00517` | ELIGIBLE | A single meeting on a fixed date; once it is held nothing in the record survives it. |  |
| 2 | alex | `lb_00347` | INELIGIBLE | A standing consideration about vets, not a dated event; the anchor corresponds to nothing in the text and the disposition persists past it. |  |
| 3 | billy | `lb_00273` | ELIGIBLE | One survey flight on 4 June 2026; the assignment does not recur. | • |
| 4 | bruna | `lb_00456` | ELIGIBLE | One conference presentation on a stated date. |  |
| 5 | callum | `lb_00387` | ELIGIBLE | A single dated travel and accommodation plan for one conference. |  |
| 6 | chenoa | `lb_00395` | INELIGIBLE | A certification renewal; the record explicitly renews, so the obligation returns on the next cycle. |  |
| 7 | chenoa | `lb_00396` | INELIGIBLE | The module requirement attaches to that same renewal cycle and recurs with it. |  |
| 8 | dariush | `lb_00418` | ELIGIBLE | One trip to Isfahan on stated dates; Nowruz recurs but the trip in the record does not. |  |
| 9 | dariush | `lb_00419` | ELIGIBLE | The duration of that same one-off trip. |  |
| 10 | david | `lb_00312` | INELIGIBLE | An open-ended deliberation about next year rather than a dated event; it persists past the anchor. |  |
| 11 | david | `lb_00398` | INELIGIBLE | A move contemplated within two to three years; open-ended and persists well past the anchor. |  |
| 12 | david | `lb_00496` | ELIGIBLE | One coaching responsibility for a tournament on a stated date. | • |
| 13 | elena | `lb_00488` | ELIGIBLE | A single wedding in a stated window; it does not recur. | • |
| 14 | fatima | `lb_00393` | ELIGIBLE | Named supplier meetings on stated April dates during one trade fair. | • |
| 15 | fatima | `lb_00397` | ELIGIBLE | One Milan trip with stated start and end dates. |  |
| 16 | jake | `lb_00358` | ELIGIBLE | One dated cabin stay. |  |
| 17 | kofi | `lb_00497` | INELIGIBLE | Presenting the accounts at the annual general meeting is a recurring role stated in the habitual present. |  |
| 18 | kofi | `lb_00511` | ELIGIBLE | Preparation for the specific 3 October meeting; the preparation is one-off even though the meeting series is annual. |  |
| 19 | marcus | `lb_00235` | ELIGIBLE | One graduation party being planned for a stated month. | • |
| 20 | marcus | `lb_00236` | ELIGIBLE | A venue booking for that same one-off party. |  |
| 21 | marcus | `lb_00238` | ELIGIBLE | A guest count for that same one-off party. |  |
| 22 | marcus | `lb_00239` | ELIGIBLE | The same one-off party, stated with month and guest count. |  |
| 23 | marley | `lb_00343` | ELIGIBLE | Transport arrangements for one graduation ceremony on a stated date. | • |
| 24 | marley | `lb_00344` | ELIGIBLE | Guest-ticket allocation for that same one-off ceremony. |  |
| 25 | mehmet | `lb_00428` | INELIGIBLE | Committee membership is a standing role and the meeting is annual; neither ends when the 2026 sitting passes. |  |
| 26 | mehmet | `lb_00429` | ELIGIBLE | Preparation for the specific 12 September 2026 sitting; that preparation does not survive the date. | • |
| 27 | mirri | `lb_00466` | INELIGIBLE | A workplace leave provision is a standing policy; it persists after the August ceremony. |  |
| 28 | mirri | `lb_00478` | INELIGIBLE | The same standing provision stated from the user side; still a policy, not an event. |  |
| 29 | pan | `lb_00484` | INELIGIBLE | An annual licence renewal; the record renews by its own terms. |  |
| 30 | patrick | `lb_00343` | ELIGIBLE | One dated arrival for one conference. |  |
| 31 | patrick | `lb_00344` | ELIGIBLE | One dated inbound flight. |  |
| 32 | patrick | `lb_00345` | ELIGIBLE | One dated outbound flight. |  |
| 33 | patrick | `lb_00349` | ELIGIBLE | One conference attendance across stated dates. |  |
| 34 | patrick | `lb_00350` | ELIGIBLE | A hotel booking for that same one-off conference. |  |
| 35 | priya | `lb_00324` | ELIGIBLE | One submission deadline in early June 2026; it does not recur within the record. | • |
| 36 | raj | `lb_00437` | ELIGIBLE | One booked one-day course on a stated date. |  |
| 37 | raj | `lb_00440` | INELIGIBLE | An open requirement to complete a course, with no date in the record; it persists until completed. |  |
| 38 | raj | `lb_00443` | ELIGIBLE | The same one-off booked course, stated with date, place and price. |  |
| 39 | raj | `lb_00447` | ELIGIBLE | The same one-off booked course stated in full. |  |
| 40 | rosa | `lb_00511` | INELIGIBLE | An annual celebration stated as every year; the fact stays true after 28 July. |  |
| 41 | rosa | `lb_00522` | ELIGIBLE | A toast planned for one dated family gathering. | • |
| 42 | rosa | `lb_00528` | ELIGIBLE | That same one-off gathering on a stated date. |  |
| 43 | thanh | `lb_00468` | ELIGIBLE | A guest count for one wedding on a stated date. | • |
| 44 | thanh | `lb_00469` | ELIGIBLE | One wedding being planned for a stated date. |  |
| 45 | thanh | `lb_00476` | ELIGIBLE | The menu for that same one-off wedding. |  |
| 46 | valentina | `lb_00364` | ELIGIBLE | One five-day trip in a stated window. |  |

### §12.2.2 — Retraction verdicts

every drawn candidate, bounded seed-ordered walk. Adjudicated **62**, eligible **11**, rate **0.177**. A dot in the last column marks the item the draw took.

| # | persona | entry | verdict | reason | drawn |
|---:|---|---|---|---|:-:|
| 1 | aroha | `lb_00008` | INELIGIBLE | A standing advocacy disposition, not a specific cancellable plan; withdrawing it is a change of values rather than a cancellation. |  |
| 2 | diane | `lb_00025` | INELIGIBLE | Completed history: why the user went to divinity school. Nothing about it can be cancelled. |  |
| 3 | tom | `lb_00005` | INELIGIBLE | A standing business practice describing what the user sells, not a plan with a cancellation point. |  |
| 4 | mirri | `lb_00009` | ELIGIBLE | A specific planned reorganisation of the patrol schedule; abandoning it makes the record wrong to surface as upcoming. | • |
| 5 | dmitri | `lb_00019` | INELIGIBLE | A completed artifact the user has already built; there is no future commitment to cancel. |  |
| 6 | lily | `lb_00001` | ELIGIBLE | A specific ongoing honours thesis that can be abandoned, which would make the topic wrong to surface as current work. | • |
| 7 | pan | `lb_00009` | INELIGIBLE | A recurring daily cost figure, not a cancellable plan. |  |
| 8 | kenji | `lb_00001` | INELIGIBLE | A standing three-year workflow disposition; a move off Figma is a replacement, which is supersession rather than retraction. |  |
| 9 | samuel | `lb_00010` | ELIGIBLE | A specific invitation the user has accepted and can withdraw from, which would make the chapter wrong to surface as upcoming. | • |
| 10 | nadia | `lb_00021` | INELIGIBLE | Completed career history from age 16; nothing in it is cancellable. |  |
| 11 | aroha | `lb_00125` | ELIGIBLE | A specific prospective enrolment in a named postgraduate diploma; abandoning it makes the study plan wrong to surface as upcoming. | • |
| 12 | aroha | `lb_00128` | INELIGIBLE | A fact about the programme's structure, not the user's own commitment. |  |
| 13 | aroha | `lb_00131` | INELIGIBLE | A standing professional aspiration with no cancellation point. |  |
| 14 | aroha | `lb_00149` | INELIGIBLE | Completed history: a module already finished. |  |
| 15 | aroha | `lb_00150` | INELIGIBLE | Completed history: a session already attended. |  |
| 16 | diane | `lb_00053` | INELIGIBLE | Third-party completed history about the husband's career change. |  |
| 17 | diane | `lb_00056` | INELIGIBLE | Third-party standing disposition about Greg's business. |  |
| 18 | diane | `lb_00131` | INELIGIBLE | A possession in the refrigerator, not a plan. |  |
| 19 | diane | `lb_00143` | INELIGIBLE | Twenty years of accumulated experience; completed history. |  |
| 20 | diane | `lb_00146` | INELIGIBLE | A standing authorial stance toward the book rather than a commitment with a cancellation point. |  |
| 21 | tom | `lb_00008` | INELIGIBLE | A three-year standing design practice. |  |
| 22 | tom | `lb_00010` | INELIGIBLE | A standing packaging practice describing what the user sells. |  |
| 23 | tom | `lb_00011` | INELIGIBLE | A standing supplier arrangement; switching suppliers is replacement, not cancellation. |  |
| 24 | tom | `lb_00071` | INELIGIBLE | A standing fact about where the apiary sites are. |  |
| 25 | tom | `lb_00091` | INELIGIBLE | Completed history: a membership already allowed to lapse. |  |
| 26 | dmitri | `lb_00023` | INELIGIBLE | A standing tooling practice already in place. |  |
| 27 | dmitri | `lb_00027` | ELIGIBLE | A specific prospective client-portal project; abandoning it makes the plan wrong to surface as upcoming. | • |
| 28 | dmitri | `lb_00058` | ELIGIBLE | A specific stated plan to use the certification as negotiating leverage, which can be dropped. |  |
| 29 | dmitri | `lb_00091` | INELIGIBLE | A standing network configuration already in place. |  |
| 30 | dmitri | `lb_00104` | INELIGIBLE | An undecided choice between two publishing routes, not a commitment that can be cancelled. |  |
| 31 | pan | `lb_00012` | INELIGIBLE | A recurring daily purchase, not a cancellable plan. |  |
| 32 | pan | `lb_00015` | INELIGIBLE | Recurring daily costs. |  |
| 33 | pan | `lb_00016` | INELIGIBLE | A recurring daily sales figure. |  |
| 34 | pan | `lb_00024` | INELIGIBLE | The same recurring daily rice purchase. |  |
| 35 | pan | `lb_00026` | INELIGIBLE | Family history about the recipe's provenance. |  |
| 36 | kenji | `lb_00014` | INELIGIBLE | A possession that is overdue for work, with no stated plan to cancel. |  |
| 37 | kenji | `lb_00027` | INELIGIBLE | Completed history: a deck already delivered. |  |
| 38 | kenji | `lb_00028` | INELIGIBLE | A standing daily work habit. |  |
| 39 | kenji | `lb_00032` | INELIGIBLE | A standing daily work habit. |  |
| 40 | kenji | `lb_00054` | INELIGIBLE | A standing accessibility tool already in use. |  |
| 41 | nadia | `lb_00061` | INELIGIBLE | A diffuse creative inclination rather than a discrete commitment with a cancellation point. |  |
| 42 | nadia | `lb_00063` | INELIGIBLE | The same inclination restated; still not a discrete commitment. |  |
| 43 | nadia | `lb_00069` | INELIGIBLE | Third-party completed history about the instructor. |  |
| 44 | aroha | `lb_00010` | INELIGIBLE | A standing professional-identity disposition, not a cancellable plan. |  |
| 45 | diane | `lb_00047` | INELIGIBLE | Third-party standing practice about Greg's wood finish. |  |
| 46 | tom | `lb_00006` | INELIGIBLE | A standing supplier arrangement; changing supplier is replacement, not cancellation. |  |
| 47 | dmitri | `lb_00020` | INELIGIBLE | A standing tooling practice already in place. |  |
| 48 | pan | `lb_00010` | INELIGIBLE | A recurring daily charcoal cost, not a cancellable plan. |  |
| 49 | kenji | `lb_00006` | INELIGIBLE | A multi-valued standing description of the kinds of work the user does. |  |
| 50 | nadia | `lb_00039` | INELIGIBLE | A standing culinary practice rather than a commitment with a cancellation point. |  |
| 51 | diane | `lb_00154` | INELIGIBLE | A statement of motivation for the book, not a commitment with a cancellation point. |  |
| 52 | diane | `lb_00156` | ELIGIBLE | A specific book project underway; abandoning it makes the project wrong to surface as current work. | • |
| 53 | tom | `lb_00098` | ELIGIBLE | States a specific plan to rejoin the association, which can be dropped. | • |
| 54 | pan | `lb_00033` | INELIGIBLE | A standing description of the business as currently operated. |  |
| 55 | pan | `lb_00034` | INELIGIBLE | Third-party family history about the grandmother. |  |
| 56 | pan | `lb_00035` | INELIGIBLE | Third-party family history about the mother. |  |
| 57 | pan | `lb_00036` | INELIGIBLE | A possession, a set of photographs, not a plan. |  |
| 58 | pan | `lb_00037` | ELIGIBLE | A specific prospective post with a stated title; dropping it makes the plan wrong to surface as upcoming. | • |
| 59 | kenji | `lb_00062` | INELIGIBLE | A system already developed; completed rather than prospective. |  |
| 60 | kenji | `lb_00112` | INELIGIBLE | A standing fact about where new work comes from. |  |
| 61 | kenji | `lb_00120` | ELIGIBLE | A specific preparation task underway for subcontractor work, which can be abandoned. | • |
| 62 | nadia | `lb_00161` | ELIGIBLE | A specific prospective sauce for a named dish; dropping it makes the plan wrong to surface as upcoming. | • |

### §12.2.3 — Supersession verdicts

every drawn candidate, bounded seed-ordered walk. Adjudicated **13**, eligible **10**, rate **0.769**. A dot in the last column marks the item the draw took.

| # | persona | entry | verdict | reason | drawn |
|---:|---|---|---|---|:-:|
| 1 | leila | `lb_00003` | ELIGIBLE | Asserts a single current felt state about the user's work, which a later statement of alignment replaces. | • |
| 2 | raj | `lb_00009` | INELIGIBLE | A compound record asserting two values at once, club support and playing position, so it is not a single-valued attribute. |  |
| 3 | valentina | `lb_00003` | ELIGIBLE | A single-valued software preference that a later tool switch replaces. | • |
| 4 | patrick | `lb_00017` | ELIGIBLE | A single-valued cabinet-style preference held by the partner, an immediate-circle member. | • |
| 5 | kofi | `lb_00010` | ELIGIBLE | A single-valued price per bag that a later price replaces. | • |
| 6 | jerome | `lb_00006` | ELIGIBLE | The vehicle carries one name; a later renaming replaces it. | • |
| 7 | zara | `lb_00013` | INELIGIBLE | Asserts an absence, that the user does not speak the dialect and has never visited, which the criterion excludes. |  |
| 8 | saga | `lb_00014` | ELIGIBLE | A single-valued gift budget that a later figure replaces. | • |
| 9 | amara | `lb_00015` | ELIGIBLE | Asserts one current seasonal flare pattern, which a later change in that pattern replaces. | • |
| 10 | aisha | `lb_00007` | ELIGIBLE | Asserts a current transient health state, explicitly marked current, which a later resolution replaces. | • |
| 11 | raj | `lb_00012` | ELIGIBLE | A single-valued gift budget agreed for one occasion, which a later figure replaces. | • |
| 12 | zara | `lb_00015` | INELIGIBLE | A multi-valued enumeration of home cultural practices, not a single-valued attribute. |  |
| 13 | zara | `lb_00044` | ELIGIBLE | Asserts one namesake for the user's design philosophy, a single-valued attribute a later renaming replaces. | • |


## §14 — Amendment 1, dated 2026-08-29, BEFORE any store version, label or score exists

**The registration mis-stated what FR-Bank's retraction write path does, and §2 is corrected
here.** §2 listed, among the construction predicates, that "retraction entries reach cosine
above 0.85 against the original under `text-embedding-3-small`". That reads the 0.85 as a
requirement the authored text must satisfy. It is not. `lifecycle_bank.py:781-784` applies
deactivation **conditionally**:

```
if is_retracted:
    results = bank.cosine_search(fact_emb, k=10)
    for related_entry, sim in results:
        if sim > 0.85:
            bank.deactivate(related_entry.id)
```

Below the threshold the original simply stays active, and the store still holds exactly what
the write path produces: the retracting entry with `is_retracted=True`, and the original
untouched. Forcing the authored text above 0.85 would have produced a store the write path
does **not** produce, which is the opposite of this cell's governing rule.

**Corrected predicate.** Cosine is measured per pair and recorded together with whether it
crosses the deactivation branch. It is never enforced, and no pair is rejected for missing
it.

**Measured on the ten retraction pairs**, `text-embedding-3-small`, authored text against
original: minimum 0.551, median 0.775, maximum 0.867. **One of ten crosses 0.85.** In the
other nine the write path leaves the cancelled plan ACTIVE in the store alongside its own
cancellation.

**Consequence for this cell: none on the arms it runs, and it is stated so no reader assumes
otherwise.** Both index arms are TRUE provenance, and `index_v2.view` derives the active
flag from the ground-truth superseded and retracted sets rather than from the store's
`is_active` field, so the TRUE index shows retracted plus one and active minus one whichever
branch the write path took. The store's `is_active` would matter under BELIEVED provenance,
which this cell does not run.

**This is reported as a finding rather than absorbed as a detail.** On realistic retractions
FR-Bank's own deactivation rule fires once in ten, because a cancellation restates its
subject and reverses its polarity, which embedding cosine scores near 0.75 rather than near
0.9. A store whose retraction handling under-deactivates is precisely the condition the
obligation judgment exists to detect, measured here from the store's own code rather than
asserted. It carries no prediction and prints whichever way a reader takes it.

## §15 — Amendment 2, dated 2026-08-29, BEFORE any store version, label or score exists

**Amendment 1 overreached, and its finding is withdrawn and replaced here.** Amendment 1
reported that in nine of ten retraction pairs the write path leaves the cancelled plan
active. That reasoning looked only at the retraction branch and ignored the branch that runs
before it. `lifecycle_bank.py:766-777` tests supersession **first**: a new entry sharing the
`slot_key` of an active entry, at confidence at or above the category threshold, sets
`supersedes` and deactivates every active entry on that slot. The retraction branch at
`:779-784` runs afterwards and only adds to that.

**What the extractor actually does, measured on the committed banks.** Of the 31 entries
carrying `is_retracted` across the 40 personas, **31 carry a `slot_key`**, **22 share that
`slot_key` with another entry**, and **16 of those carry a `supersedes` pointer**, with the
prior entries left inactive. The extraction prompt states the rule directly
(`lifecycle_bank.py:604`): facts about the same real-world attribute must use the same key.

**Corrected construction.** The retracting entry is given the **same `slot_key`** as the
original, which is what the extractor does. The supersession branch therefore fires, the
original is deactivated, and `supersedes` is set. The cell's retraction stores are what the
write path produces, and the original does **not** stay active.

**What survives as a finding, at the strength the evidence supports.** At the store level a
retraction is recorded through the same mechanism as a supersession: a `supersedes` pointer
plus deactivation of the prior entry. The retraction-specific cosine rule is largely
redundant, firing on one of the ten authored pairs where the slot branch fires on all ten.
The consequence is about BELIEVED provenance rather than about this cell: a store that
records retraction and supersession through one mechanism cannot distinguish them in its own
metadata, which is consistent with the paper's existing account of what BELIEVED loses. This
carries no prediction and is reported whichever way a reader takes it.

**Cosine remains measured and never enforced**, as Amendment 1 established; that part stands.
Measured over the ten pairs: minimum 0.551, median 0.775, maximum 0.867.

## §16 — Amendment 3, dated 2026-08-29, BEFORE any monitor or baseline runs

**A scrubber collision is a property of the instrument, and it is registered as a criterion
here rather than discovered as a verdict later.**

`index_v2.scrub` keeps the attribute path up to the first colon, so
`project:honours_thesis_microplastics` and every other `project:*` slot in a persona reduce
to the single name `project`. Where a persona already carries lifecycle content on another
slot with the same scrubbed name, that name is on the corresponding list before this cell
changes anything, and the pair's own state is then not individuated by the index.

**Individuation, defined mechanically and computed before any monitor runs.** A
counted-state pair individuates when its scrubbed slot name is ABSENT from its own state's
v3 name section in the PRESENT version and PRESENT in the PN version. The second half is a
construction check and a failure is a STOP. The first half is the corpus meeting the
scrubbing rule, and it decides scoring eligibility.

| Pair | State | Scrubbed name | Individuates | On v2 superseded list in PRESENT |
|---|---|---|:-:|:-:|
| `cf:aroha:project:postgraduate_study` | Retraction | `project` | **no** | no |
| `cf:billy:project_aircraft:aerial_wildlife_survey` | Expiry | `project_aircraft` | yes | no |
| `cf:david:coaching_event_date` | Expiry | `coaching_event_date` | yes | no |
| `cf:diane:project:chaplain_book` | Retraction | `project` | yes | no |
| `cf:dmitri:project:client_portal` | Retraction | `project` | yes | no |
| `cf:elena:event:wedding_timeline` | Expiry | `event` | yes | no |
| `cf:fatima:trip_schedule:salone_del_mobile_2026` | Expiry | `trip_schedule` | yes | no |
| `cf:kenji:project:case_studies` | Retraction | `project` | yes | no |
| `cf:lily:project:honours_thesis_microplastics` | Retraction | `project` | **no** | yes |
| `cf:marcus:event:Kayla_graduation_party` | Expiry | `event` | yes | no |
| `cf:marley:event_transportation` | Expiry | `event_transportation` | yes | no |
| `cf:mehmet:preparation:barber_trade_guild_annual_meeting` | Expiry | `preparation` | yes | no |
| `cf:mirri:project:patrol_schedule_reorganization` | Retraction | `project` | **no** | no |
| `cf:nadia:project:winter_menu_sauce` | Retraction | `project` | **no** | no |
| `cf:pan:project:instagram_post_idea` | Retraction | `project` | yes | yes |
| `cf:priya:project_deadline:NeurIPS_paper` | Expiry | `project_deadline` | yes | no |
| `cf:rosa:event:toast_planning` | Expiry | `event` | **no** | no |
| `cf:samuel:project:cranial_approaches_textbook_chapter` | Retraction | `project` | yes | no |
| `cf:thanh:event_guest_count:duc_wedding` | Expiry | `event_guest_count` | yes | no |
| `cf:tom:membership:gloucestershire_beekeepers` | Retraction | `membership` | yes | no |

**Result: retraction 6 of 10, expiry
9 of 10, pooled counted-state scored n =
15.**

**CF-3 scoring rule, frozen.** Pairs whose own-state section individuates are scored toward
the prediction. Pairs whose scrubbed name already sits on that state's list in PRESENT are
**reported descriptively as scrubber collisions and never scored toward CF-3**. Retraction
individuation is at or above six, so CF-3 remains the pooled counted-state prediction over
retraction and expiry together, scored on 15 items, with the
5 collisions printed beside it. Had it fallen below six, CF-3 would
have been re-described as expiry led plus the surviving retraction pairs, with the count
stated. Per-state rows remain descriptive throughout.

**The superseded-list collision is separate and prints as itself.** The superseded-names
matcher reads v2 only, so a name already on the v2 superseded list confuses that baseline
whatever the monitor does. That confusion is a property of the baseline and prints in its
row; it does not remove a pair from CF-3, whose sections are the v3 retracted and expired
lists.

**The scrubber is not changed.** Keeping the second path segment would put the project's
identity into the index, and that identity is a value. The paper rests on the index being
value-scrubbed. A finer scrubbing rule is an October design question that would need its own
leakage screen, and it is not a fix applied here.

**The finding, registered now so it cannot be said to have been written after the result.**
It holds whichever way CF-3 fires, and it supplies a second reason for a number the paper
already carries: on the main population retraction sits at chance for both readers, which
the paper attributes to the index only counting retraction. Naming is necessary and it is
not sufficient, because a v3 index that names retracted content can still only name what the
scrubbing rule individuates.

**[MAIN] §7.2, beside the naming sentence, two sentences.** The wording below departs from
the sentence as dictated, which contained a contrastive of the form barred by STYLE_SPEC S9;
the content is unchanged.

> A self-description can only name what its scrubbing rule individuates. Naming granularity
> is a design parameter of the summary, and it bounds what any reader can recover from it.

**Accumulating categories, recorded under the same principle as Amendment 1.** Five
supersession pairs sit in `ACCUMULATE_CATEGORIES`, where the supersession branch needs
confidence at or above 0.95 rather than 0.80. At the ordinary 0.9 of a definitive statement
the branch does not fire, so the store keeps both values active and sets no pointer. The
build records that branch and asserts the store matches whatever it implies, in both
directions, rather than forcing it. This is the behaviour the believed-state census already
attributes to FR-Bank at `paper_v2.tex:1524`, which records that it retains an active
obsolete assertion after 72 percent of supersession events, appearing here in miniature and
from the write path rather than from the census.

## §24 — Amendment 4, dated 2026-08-30, BEFORE the Opus 5 lane is submitted

**The cell ceiling rises from $12 to $15, and the reason is a mis-projection rather than an
overspend.** Nothing has exceeded any line. Metered spend at the time of this amendment is
**$0.1444**, which is 1.2 percent of the original ceiling.

**What was mis-projected.** §10 built its projection on `ECONOMICS.md` §1, whose
INDEXED-TRUE mean input is 1,201 tokens. That mean pools E1's FULL, CAT-ABLATED and
SLOT-ABLATED variants across all 40 personas. This cell uses 30 personas' FULL stores, which
sit at the larger end, and its indexes render at 63.2 lines on average against `index_v2`'s
40 to 60 design target. Measured like for like on the shared lane, the counterfactual prompt
runs **1,682 input tokens against E1's 1,201, a factor of 1.40** (`AUX-R82-CF-INDEXSIZE`).
The remainder of the gap between the registered $5.92 and the measured $10.63 is Opus 5's
rate card and output length rather than index size.

**A correction carried here so it does not propagate.** An earlier report of the index
running "about twice" the E1 size compared Opus 5's 2,475 tokens against E1's `gpt-4.1-mini`
figure of 1,201, which is two different tokenizers. The factor on the shared lane is 1.40.

**Why the third lane is worth three dollars.** Opus 5 carries no registered prediction, and
that is exactly why the question is whether to run it at all. It is the lane with the
strongest question priors, and this is the one cell in the paper where blind is 0.5 by
construction, so its per-state rows here are the cleanest available replication of the
per-state crossover recorded in `ADDENDUM_R81` §11. **It runs at k=5.** Reducing it to k=3
would save about three dollars and make those rows non-comparable with Tables 20 and 21,
which are k=5, which removes the only reason to run the lane.

**Revised ceiling and itemisation.** Ceiling **$15**: `gpt-4.1-mini` $1, Haiku 4.5 $2,
Opus 5 $11, construction $1. The measured projection is $10.63 against $15, leaving $4.37 of
headroom for retries, the v3 leakage screen, and any re-poll. The run still stops at the
ceiling, and the standing STOP condition on spend is unchanged.

**Nothing else in the registration changes.** No prediction, no population, no branch text,
no estimator.

## §13 — STOP conditions specific to this registration

- Any monitor or baseline call before this file is committed and GO is given at the ceiling.
- Any label mismatch in the 90-item cell, or any write-path predicate that does not fire on
  a PN version.
- Any number printed without a key in `NUMBERS_R82.md`.
- Any reading written after its numbers exist, or any third reading beyond the branches
  above.
- Any edit to a file R81 owns before a commit titled R81-5 exists.
- The frozen lineage changing by one byte.
- Computing the hybrid monitor, which `ADDENDUM_R81.md:473` makes a STOP until registered.
- Spend reaching the ceiling with the cell unscored; the run stops and reports rather than
  continuing.

---

# Part 2 — ADDENDUM_R82-CAL: registration freeze for post-hoc calibration

Frozen against HEAD `ef351e9`, 2026-08-30, **BEFORE any calibration number is computed**.
Budget **$0**: no API call is made, and every score is re-derived from committed artifacts.
Ledger section `AUX-R82-CAL`. Same inherited rules and the same publish-regardless
discipline as Part 1.

## §17 — Populations (frozen, and verified to reproduce)

| Row | n | positives | personas | Arms |
|---|---:|---:|---:|---|
| `P-FOK-HARD` | 588 | 35 | 40 | blind, intact index, names-only |
| `P-NOK-FRB` | 661 | 104 | 40 | blind, indexed TRUE, indexed BELIEVED |

**No committed per-item score matrix exists**; every `e1r_robustness/results/*.json` is
arm-level. Both matrices are re-derived at read time, and the assemblies are the committed
ones rather than new code. `P-FOK-HARD` follows `verify_e1r.py:139-167`, whose requirement
that a tag be present in all three mechanism arms is what makes it 588 rather than 595; the
names-only arm is `A3-names-only` from `e1_metamemory/mechanism_elicitation.json`.
`P-NOK-FRB` follows `common_e1r.assemble` under `POPULATIONS["R-NOK-FRB"]`. Both reproduce
exactly, and the BELIEVED arm joins 661 of 661.

**Disclosed before fitting: the elicited score is heavily quantised.** The intact-index FOK
score takes **12 distinct values** across the 588. An isotonic fit on a 12-valued score is
close to a lookup table over those values, which is why every fit is scored out of fold and
never in sample.

## §18 — Method (frozen)

Three monotone maps: **Platt** (logistic regression on the raw score), **isotonic**
(non-decreasing step fit), and **temperature scaling** (a single scalar on the logit). Every
map is fitted and evaluated under **leave-one-persona-out cross-validation**, 40 folds,
grouped by the persona field the populations already carry, reusing the grouping
`common_e1r.lopo` uses. No item contributes to the fit that predicts it.

Metrics before and after, per arm: **ECE** (`common_e1r.ece`, 10 equal-width bins,
mass-weighted, the committed definition), **Brier**, and risk-coverage **AURC** with
**excess AURC** measured against the oracle ordering on the same labels.

**AUROC is unchanged by a monotone map, and this is asserted rather than assumed.** The run
recomputes AUROC before and after each map and requires agreement to four decimal places. A
disagreement means the fitted map is not monotone on the observed support and is a STOP.

## §19 — Registered readings (two)

- **CAL-1.** Under leave-one-persona-out cross-validation, isotonic brings the intact-index
  ECE on `P-FOK-HARD` **below 0.05**.
- **CAL-2.** The recalibrated crossing threshold differs between the intact-index arm and the
  names-only arm by **more than 0.10 in raw-score space**.

**The crossing threshold is defined now, including the case where it does not exist.** The
primary definition is the smallest raw score whose calibrated probability reaches **0.50**.
Both populations sit well below that rate, 35 of 588 and 104 of 661, so a calibrated
probability may never reach 0.50 on either arm. **If the 0.50 crossing is undefined on either
arm, CAL-2 is reported as undefined by base rate**, and the comparison is repeated at the
crossing where the calibrated probability first reaches that population's own base rate,
printed as a descriptive substitute that carries no prediction. This substitution is
registered before any fit exists and is not chosen after seeing one.

## §20 — Frozen branch text

**CAL-1 HOLDS. [MAIN] §4.3, one sentence.**

> The elicited score can be made calibrated after the fact, reaching an expected calibration
> error of $X$ under cross-validation, so its ranking carries information a probability can
> be recovered from.

**CAL-1 FAILS. [MAIN] §4.3, one sentence.**

> Rescaling the elicited score after the fact leaves its expected calibration error at $X$
> under cross-validation, so the score ranks items without becoming a probability.

**CAL-2 HOLDS. [APPX] Appendix H, one sentence.**

> The threshold at which the recalibrated score crosses its decision point moves by $D$
> between the intact summary and the names-only summary, so a deployed monitor needs a
> threshold fitted to the summary it will actually see.

**CAL-2 FAILS. [APPX] Appendix H, one sentence.**

> The recalibrated crossing threshold moves by $D$ between the two summaries, which is inside
> the registered margin, so one threshold serves both on this population.

**CAL-2 UNDEFINED. [APPX] Appendix H, one sentence.**

> The calibrated probability does not reach the decision point on either summary at these
> base rates, so the threshold comparison is reported at each population's own base rate
> instead and carries no registered claim.

## §21 — Framing (frozen)

The result is reported as **resolution without calibration**, the classical distinction from
the metamemory literature: a judgment can order items correctly while its absolute level is
miscalibrated. Nelson and Narens on the monitoring framework, and Koriat on the accessibility
account of feeling-of-knowing, are the anchors. Neither is currently in the manuscript's
bibliography, so landing either in main text requires a `refcheck_v11` registry entry and a
verified record. Until then the framing sentence names the distinction without the citation.

## §22 — Ledger keys and home

Keys `AUX-R82-CAL-ECE`, `-BRIER`, `-AURC`, `-EXCESS`, `-THRESHOLD`, `-AUROC-INVARIANCE`,
`-QUANTISATION`. The table lands in **Appendix H**, created by R82 as the standing post-hoc
section whose opening sentence states that everything in it is post hoc and unregistered. One
main-text sentence goes to §4.3's calibration paragraph (`paper_v2.tex:421-428`). Under the
standing cut order calibration is cut first if the census yield does not arrive.

## §23 — STOP conditions for Part 2

- Any calibration number computed before this part is committed.
- Any fit scored in sample, or any fold that shares a persona between fit and evaluation.
- AUROC moving by more than 0.0001 across a monotone map.
- A reading written after its numbers exist, or a third reading beyond the branches above.
