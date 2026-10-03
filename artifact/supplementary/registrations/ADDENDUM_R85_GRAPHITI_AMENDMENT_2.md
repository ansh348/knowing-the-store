# ADDENDUM R85-GRAPHITI — Amendment 2: the answer stage under untagged, tagged and masked views, on both stores

**DRAFT until frozen by commit before the first billed call.** Written 2026-09-16 from the author's
decision of the same day (the full-population shape over the eight-persona pilot, with four
changes: a human-scored endpoint that can correct the conclusion; overall paired policy
differences primary, mechanism subsets secondary; query intent reported explicitly; the "three
decisive items" arithmetic treated as a warning, replaced by a direct count once the retrieval
exists) and revised the same day on three further points (the population a single Graphiti graph
can be scored against, §0 and §3; the separation of a structural bound from mechanism sets and
from statistical resolution, §5; the standing of the second reader, the licensed-answer audit and
the appropriateness of a decline, §6). Nothing below has been retrieved, answered, read or scored.
It amends `registrations/ADDENDUM_R85_GRAPHITI_AMENDMENT_1.md` (frozen `43132a3`) and inherits
`registrations/ADDENDUM_R85_GRAPHITI.md` (frozen `ca522b0`) through it. Amendment 1's Steps 4 to 6
and its predictions P1 to P4 are **not changed by this file**; §0 records a finding about their
population that is the author's to rule on before Step 4.

Deviations continue the `D-R85-n` series in `r85_graphiti/DEVIATIONS_R85.md`, from `D-R85-16`.
Ledger keys are `AUX-R85-A2-*` in `r85_graphiti/NUMBERS_R85.md`. No edit to `CLAIMS.md` before
integration.

---

## §0 A finding that reaches Amendment 1, recorded here before anything runs

The 661 items are 332 questions under three **store variants** (`resp_review/tools/resp_common.py`
`variant_ids`): FULL is the persona's whole bank; CAT-ABLATED removes every entry of a drawn set of
categories (`variant_plan.json`); SLOT-ABLATED removes the entries named for that question
(`slot_ablations.json`). On FR-Bank each variant is a different store and each item's retrieval is
taken from its own reduced bank (`build_l2.py` `bank_for`). **Graphiti is one graph per persona,
ingested from the whole bank** (`r85_graphiti/render_episodes.py` reads
`lifecycle_banks/<persona>.json` entire; 18,936 records, 1,365 episodes, `FREEZE.md`). The graph
is therefore the FULL store for every item, and an item's label describes the graph only if it is
the FULL variant's label.

Counted from `r74/x4/cell_661.json` and `e1_metamemory/build/items_final.json`, no output seen:

| Over the 661 | items |
|---|---:|
| FULL variant (145 ABSENT, 131 PRESENT, 47 PRESENT-NEGATIVE) | 323 |
| non-FULL whose NOK/FOK labels equal the FULL sibling's | 99 |
| **non-FULL whose NOK/FOK labels the full store contradicts**: 229 ABSENT-by-ablation items whose FULL sibling is PRESENT (215) or PRESENT-NEGATIVE (14), the record being in the graph; and `aisha_q03` CAT-ABLATED, PRESENT because its forbidding records' category was removed | **230** |
| non-FULL with no FULL sibling in the cell (unverifiable against the graph) | 9 |

Amendment 1's summary route (P2, P3, GR-1 to GR-5) and tag route (P4) are registered on the 661.
On Graphiti, 230 of those items carry a label the store it reads from contradicts. This file does
not amend Amendment 1; it records the count so the author can rule before Step 4. The obvious
repair costs nothing: read every Graphiti row of Amendment 1 on the 323 FULL items (positives 47),
with the FR-Bank comparators (the recorded INDEXED-TRUE, blind, RETRIEVED and RETRIEVED-BELIEVED
rows) re-scored on the same 323 from their recorded per-item rows, and print the 661 figure beside
it as the registered form with this note. Whatever the ruling, it is a `D-R85-n` entry before any
Amendment 1 number prints.

For this amendment the consequence is settled in §3: the primary population is the FULL variant on
both stores.

## §1 What this measures, and what it does not

**The registered tag route is the NOK lane** (Amendment 1 §4 C; P4): GPT-4.1 mini's obligation
discrimination under VIEW-UNTAGGED, VIEW-TAGGED and HYBRID. It asks whether the monitor *knows*
it must not use the record. It stays as registered.

**This amendment is the answer stage**: the downstream protocol of `registrations/ADDENDUM_DS.md`
§D.4 in the form its Amendment 4 fixed (`ADDENDUM_DS_AMENDMENT_4.md`, run and ledgered as
`AUX-DS-A4-*`), under three views of the same retrieval per store. It asks what the model *does*
with the evidence: gives the current value, endorses the obsolete one, reports the cancellation or
expiry, or declines. The central question, in the author's words: does the extra lifecycle
evidence improve behaviour, harm it, or create a trade-off. Both lanes print; neither substitutes
for the other, and a disagreement between them (a tag that lifts NOK and lowers answer
correctness, or the reverse) is itself a result the paper reports.

**Why now.** P1 failed on recall at Step 3 (`AUX-R85-G10-CENSUS-FORBIDDING`, commit `50e4429`):
Graphiti marks 30 of the 74 superseded-or-expired forbidding records non-active, recall 0.4054,
above the registered quarter, at precision 0.0669 (54 of its 807 non-active edges fall on a record
the join marks non-active). So Graphiti's tags reach some of the records that matter and most of
its non-active marks fall elsewhere. FR-Bank's own marks are the mirror image on the recorded
five-line views (`AUX-RESP-A1-TAGS`): over the forbidding records in view, recall 0.7833 and
precision 0.6714; over all 3,305 lines, 1,389 marked non-active, 1,201 of them on records the join
calls active, precision 0.1353. A mask built on each store's own marks therefore removes very
different things: on Graphiti, few of the forbidding records; on FR-Bank, most of them and two
fifths of everything else. That is the pair of mechanisms the three views separate.

## §2 Inherited verbatim, and what is not adopted

Everything Amendment 1 froze or inherited is unchanged: RULES 1 to 3, the episode rendering, the
manifest as ground truth (never an input to any view), the pinned environment, the persona clock
`t_now`, GR-1 to GR-5, P1 to P4, the §7 budget and **the §7 Haiku rule, which is evaluated exactly
as written and is not touched by anything here** (§8 below). From the DS lineage this amendment
inherits, by import and not by copy:

| Inherited | Where | Note |
|---|---|---|
| `SYSTEM_ANSWER` (D.4) and `USER_ANSWER_A4` (D.4 user text with the persona-and-date header) | `ds_downstream/tools/prompts_ds.py`, `amend4_header.py` (`HEADER`, `persona_fields`) | The A4 form, not bare D.4: A4-P1 held (+0.1692 on the 65 licensed items in view, `AUX-DS-A4-P1-MINI`), so bare D.4 would reintroduce the persona-binding gap the audit found. Date = the join's `t_now`, as A4 renders it. |
| Decoding | DS §D.4 | GPT-4.1 mini, temperature 0, seed 42, `max_tokens` 200, JSON mode, one retry on a parse failure; **one call per distinct complete input** (system prompt, user prompt with header, view), keyed by sha256; identical inputs share the answer (`run_ds.py`'s rule). This is the answer-reuse protocol §5 refers to. |
| The line format | `resp_review/tools/build_l2.py`, `resp_common.render_line` | `[r] lifecycle: … \| category: … \| attribute: … \| age: … \| text: …`; on Graphiti `category: not expressible by this backend` and the RULE 2 attribute name (Amendment 1 §4 C). |
| The committed detector rows | `run_ds.py` `score_answer`, `records`; `amend4_header.is_abst`; `amend7_reported.reports_obligation` (rule sha256 `835329c6…`) | Stale use at TAU_HI 0.80 and TAU_GOLD 0.50, stale surfacing, successor use, obligation reported, abstention (`"store does not currently contain"`), PRESENT correct at TAU_GOLD and TAU_HI. The DS forensic finding stands: expiry obligations are unscorable for stale use by the detector; on them the human read is the only endpoint (§6). |
| The human-read lineage | `reviews/v16/SECOND_ANNOTATOR_SHEET.md` section C (Q1 to Q4), `reviews/v18/annotator_agreement.py` | The rubric questions are inherited verbatim and extended by one (§6); the agreement script is extended, not replaced. |
| Tolerance ±0.05; paired bootstrap 1,000 draws, seed 42, item-level and persona-clustered; the weaker interval governs | Amendment 1 §5, §6; `ADDENDUM_RESP.md` | Unchanged; clusters are the personas present in the population read (28 for the obligation rows, 40 for the licensed rows). |

**Not adopted, and why:**

- *The eight-persona pilot with thirty-two reserved for confirmation.* From the same two files,
  2,000 seeded eight-persona draws carry a mean of 20.6 obligation items (p10 to p90: 13 to 28)
  and 35.1 licensed items (28 to 42) of the 278; expiry-derived obligations sit in 6 of the 40
  personas and 29% of draws miss the four-stratum requirement. The census split (RECOVERED 30 /
  STALE_ACTIVE 21 / EXTRACTION_MISS 23 of 74) suggested that a pilot would hold only a handful of
  items on which tagged and masked views can differ; that was a warning, not a power analysis (§5),
  and the author chose the full population on it. The claim is chosen by the ruling table (§9),
  written now.
- *Intent-aware masking on Graphiti.* FR-Bank's `lifecycle_search` filter is intent-dependent
  (its temporal route bypasses expiry). Transplanting an intent rule onto Graphiti is the co-design
  RULE 3 forbids. The mask here is the one thing both stores can express, **active-only filtering of
  the recorded top-10, returning up to five records**, and is described as that and nothing more.
  Intent is handled in the analysis (§7), not in the retrieval.
- *An LLM judge.* DS §D.4 registered "no LLM judge" and this amendment keeps it: the human read is
  a person, the detector rows are the committed functions.
- *A retraction proxy.* RULE 1; retraction-derived obligations print the marker on every Graphiti
  row and are answered and read like the rest (their Graphiti tags read superseded, expired or
  active, never retracted).
- *Scoring one Graphiti answer under two variants' requirements.* §0 and §3: an item is scored only
  against the label of the store its view came from.

## §3 Population

**Primary population, both stores: the 178 FULL-variant non-ABSENT items** of
`r74/x4/cell_661.json` (sha256 `01ed4c05fc57c0b2…`): **47 obligation** (38 with-replacement, all
CURRENT-STATE; 9 without-replacement, all UPCOMING, the expiry-derived) and **131 licensed**
(CURRENT-STATE 65, UPCOMING 26, CHANGE-AWARE 35, PAST-EVENT 5). Attack vectors of the 47: AV1 16,
AV4 11, AV7 11, AV2 9; their join states print from `index_v2.true_lifecycle` at build. The 47
obligation items lie in 28 personas, the 131 licensed in all 40. Every item is one question: no
question appears twice in this population, so no answer is scored against two requirements, on
either store. Ground truth per item is DS's: the manifest record's gold field, stale field and
successor (`run_ds.py` `records`), never shown to any model.

**Why the FULL variant and not the 278.** On Graphiti the graph is the FULL store (§0). Of the 100
ablated-variant items among the 278, 58 carry the FULL sibling's label and subtype and would be
duplicates of it on Graphiti (same graph, same question, same requirement); 42 carry a requirement
the full store contradicts: the 35 SLOT-ABLATED and 6 CAT-ABLATED obligations labelled
"without-replacement" are so labelled *because the successor was removed from FR-Bank's bank*, and
the graph holds it, so "decline" would be the wrong correct answer there; and `aisha_q03`
CAT-ABLATED is labelled licensed because its forbidding records' category was removed, and the
graph holds them. None of the 42 can be scored on Graphiti against its own label. The FR-Bank
side of the primary population is the same 178 so that the two stores stand on one footing: same
questions, same full store, same requirements.

**FR-Bank-only block, descriptive: the 100 ablated-variant non-ABSENT items** (CAT-ABLATED 43
licensed + 22 obligation; SLOT-ABLATED 35 obligation; the 57 obligations being 41 constructed
without-replacement, 10 with-replacement and 6 expiry). Each retrieves from its own reduced bank
(`retrieval.json` is already per variant), so on FR-Bank every one is valid against its label. They
run under the same three conditions and print in their own table, never pooled with the 178: they
are the only place a current-state obligation whose successor is absent can be read ("correct
handling of a cancellation" on CURRENT-STATE), and that reading is FR-Bank-only and says so. No
Graphiti call is made for them.

**Historical intents** (CHANGE-AWARE and PAST-EVENT, 40 of the 131) are all licensed: no
obligation item asks about the past. The place an active-only mask can remove legitimate evidence
is the licensed population, and §7 reads it there by intent.

## §4 The views: three conditions per store, the same procedure on both

**Source retrieval, recorded before any view is built.**

- *Graphiti*: Amendment 1 Step 5's per-item stock `Graphiti.search(question, group_ids=[…],
  num_results=10)` on the `r85stock_<persona>_g10` groups, `EDGE_HYBRID_SEARCH_RRF`, default
  `SearchFilters()`. Amendment 1 registers "top 10 taken, top 5 used"; this amendment states the
  build requirement that makes the mask computable: **Step 5's record stores all ten rendered lines
  per item with each edge's RULE 1 state**, not the five alone. If the record as built holds fewer,
  the ten are re-rendered from the same cached search results and `D-R85-16` records it (no new
  search call).
- *FR-Bank*: `resp_review/l2/retrieval.json` `top10_ids` (recorded 13 September), with
  **FR-Bank's own marks** from `resp_review/tools/amend1_resp.believed_flags()` (the A1 rule:
  `believed_superseded`, `believed_retracted`, `event_time` before the persona's cutoff as
  expired), rendered by `resp_common.render_line`. The join's TRUE flags are used in no view.

**The three conditions.** Per store, per item, from the same ten ranked lines:

| Condition | Lines | Lifecycle field | System prompt | User prompt |
|---|---|---|---|---|
| **U, untagged** | ranks 1 to 5 | removed from every line, nothing else changed | `SYSTEM_ANSWER_U`: `SYSTEM_ANSWER` with its first paragraph's lifecycle sentences replaced by "The view lists entries; each entry carries the metadata the store records for it." (the sentences from "An entry marked active" to "must not be given as the answer." removed), constructed by asserted `str.replace` calls and hashed | `USER_ANSWER_A4` with "each with the lifecycle metadata the store records for it" replaced by "each with the metadata the store records for it", the one replace Amendment 1 §4 C uses; header unchanged |
| **T, tagged** | ranks 1 to 5 | the store's own state | `SYSTEM_ANSWER` verbatim | `USER_ANSWER_A4` verbatim |
| **M, masked** | of ranks 1 to 10, the lines whose store-own state is `active`, in rank order, the first five; fewer than five if fewer remain (the count of short views prints; no line is added from beyond rank 10) | present, reading `active` on every line | `SYSTEM_ANSWER` verbatim | `USER_ANSWER_A4` verbatim |

U and T share their five identifiers and differ in exactly the `lifecycle:` field and the two
prompt sentences that name it. T and M share their prompts and differ in exactly the lines the
mask removes and the lines from ranks 6 to 10 that replace them; **where ranks 1 to 5 hold no
non-active line, M's complete input is T's and the answer is shared by the protocol.** M keeps the
field, reading `active` throughout, so that T→M isolates the mask and not the prompt; that every M
line reads `active` is stated wherever M prints. The abstention instruction ("If no entry in the
view answers the question as it stands, say that the store does not currently contain the
answer") stays in all three system prompts. The four prompt texts and their sha256 are
`AUX-R85-A2-PROMPTS`.

**Cells and rows.** Primary: {Graphiti, FR-Bank} × {U, T, M} on the 178, nominal 1,068 rows.
FR-Bank-only block: 3 × 100 = 300 rows. Nominal total 1,368; distinct inputs fewer by the shared
T = M cases, the per-cell count printing as `AUX-R85-A2-VIEWS`.

**Reference row from the record, printed beside FR-Bank T and never re-run**: DS Amendment 4's
ALWAYS row under GPT-4.1 mini with the header (`AUX-DS-A4-STAGE2-MINI`, `AUX-DS-A4-PRESENT-MINI`,
`run/scores_amend4.json`), restricted at $0 to the 178 from its per-item rows: the same prompt,
the same top-5, the **join's** tags. It covers the reached obligations and every licensed item,
not every obligation, and says so; it is the reference for how much of FR-Bank's T row is the
accuracy of its own marks.

**Build checkpoint, by eye, before any call**: ten views drawn by seed 42, five per store, at least
one per condition, checked against the line format (field order, the marker on category on
Graphiti, the age arithmetic against `t_now`, U differing from T in exactly the field, M
containing no non-active line, M's lines in rank order), and the check recorded
(`AUX-R85-A2-CHECK`). It sits beside Amendment 1's 22 September checkpoint and is its own record.

## §5 Three quantities that are not the same thing, counted before any call

The exchange of 16 September estimated "about three decisive items" in a pilot and "about fifteen"
on the full population from the census split. That was a warning about resolution, not a power
analysis, and it is not used: 8.8% non-active edges does not give the share of licensed questions
whose evidence a mask removes, because rank, relevance and invalidation are not independent, and
the number of correctly marked forbidding records does not bound the number of answers that
change, because tags on other lines change how a view is read and a mask changes the distractors
and admits lines from ranks 6 to 10. Three quantities print separately (`AUX-R85-A2-RESOLUTION`),
each with the standing stated:

**(i) The structural bound, from the answer-reuse protocol.** Two conditions are answered by the
same call whenever their complete inputs are identical (§2). On a population of n items the paired
difference between conditions X and Y in any endpoint therefore cannot exceed n_XY / n, where n_XY
is the number of items whose complete inputs differ between X and Y. This is a hard bound and the
only one derived here. For U against T and for U against M, n_XY = n (the system and user prompts
differ on every item): **no structural bound.** For T against M, n_TM = the number of items whose
ranks 1 to 5 hold at least one line the store marks non-active; it prints per store, per
population, with the bound n_TM / n beside A2-P2.

**(ii) Mechanism sets, descriptive, bounding nothing.** Per store and per population, the sets
that name where a difference would come from if the hypothesised mechanism is the one at work:

| Set | Definition |
|---|---|
| (a) reached | obligation items with a forbidding record among ranks 1 to 5 (by identifier on FR-Bank; on Graphiti by the detector at τ = 0.80 on the edge fact, as `census_forbidding.py` matches) |
| (b) reached, marked | of (a), a forbidding line the store marks non-active: T shows a correct tag, M removes the line |
| (c) reached, unmarked | of (a), every forbidding line in view marked `active`: T presents an incorrect active label and M retains the record; whether other evidence in the view lets the answerer recover is measured, not assumed |
| (e) imported | obligation items where M's replacement lines (ranks 6 to 10) bring in a forbidding record marked `active` |
| (f) evidence removed | licensed items where a line among ranks 1 to 5 covering the gold field at TAU_GOLD is marked non-active, so M drops it; by intent |
| (g) unreached | obligation items with no forbidding record among ranks 1 to 10 |

These print beside the transition tables (§7) as the explanation the data support or do not; no
reading is decided by them.

**(iii) Statistical resolution: the intervals.** Item-level and persona-clustered paired bootstrap
as inherited; the weaker governs.

**Reading rules, fixed now, per prediction and per store.**

- A prediction of a difference *beyond* the tolerance: **HOLDS** if the point estimate is beyond
  ±0.05 in the predicted direction and the governing interval excludes zero; **INCONCLUSIVE** if
  the point estimate is beyond the tolerance in the predicted direction but the governing interval
  includes zero (the data do not separate no effect from the registered effect; the interval
  prints and no verdict does); **FAILS** otherwise. If the structural bound (i) is below 0.05 the
  prediction prints **"structurally unable to meet the registered magnitude (bound b)"** in place of
  a verdict, and the observed difference prints beside it.
- A prediction of a difference *within* the tolerance: **HOLDS** if the point estimate lies within
  ±0.05, **FAILS** otherwise (the study's L2-P2 convention), the interval beside. If the structural
  bound is below 0.05 it holds *by construction* and prints **"HOLDS structurally (bound b)"**, so the
  paper never presents a difference the protocol could not have produced as an empirical finding.

## §6 Scoring: the human-scored endpoint and the detector rows

**The rubric, frozen with this file and not revised after any answer is read.** Section C of
`reviews/v16/SECOND_ANNOTATOR_SHEET.md` asks, per answer, Q1 (gives the stale value as the answer,
in substance, even if paraphrased), Q2 (mentions or surfaces the stale value at all, including to
say it changed), Q3 (licensed only: correct against the gold value), Q4 (obligation only:
correctly reports the obligation, that the stale content is superseded, withdrawn or expired).
Those four are inherited verbatim. One is added: **Q5, declines**: the answer gives no value and
says the store has no current answer, or that the arrangement is over, or otherwise declines to
state a value. Q1 and Q2 are distinct by construction: an answer that names the obsolete value in
order to reject it is Q2 yes, Q1 no. For with-replacement obligations the reader also marks
whether the answer gives the successor (**Q6**, the human counterpart of the detector's
`successor_use`).

**Whether a decline was appropriate is not the reader's judgment; it is computed from the inputs.**
The reader is blind to the view and cannot know what it held. For each answer the build records an
*evidence-in-view* flag from the view the model actually saw: for a licensed item, whether any line
covers the gold field at TAU_GOLD; for a with-replacement obligation, whether any line covers the
successor at TAU_GOLD. A decline (Q5 yes) is then **unnecessary** if the evidence was in view and
**appropriate** if it was not (under M because the mask removed it, under U and T because retrieval
did not reach it); the two print separately and the flag's rule is part of this freeze. For the
9 expiry obligations without a successor, a decline is correct handling by construction.

| Population | Category (one per answer) | Rule |
|---|---|---|
| obligation, with-replacement (38) | correct current | Q6 yes and Q1 no |
| obligation, without-replacement (9) | correct handling | Q4 yes or Q5 yes, and Q1 no |
| obligation (47) | **stale endorsement** | Q1 yes |
| obligation (47) | other error | none of the above; a with-replacement item declined with the successor in view is counted here and printed as *unnecessary decline* |
| licensed (131) | correct | Q3 yes |
| licensed (131) | unnecessary decline / appropriate decline | Q5 yes, split by the evidence-in-view flag |
| licensed (131) | wrong | neither |

The FR-Bank-only block uses the same rules with its own counts (41 constructed without-replacement
under "correct handling").

**Blinding.** The sheet shows the persona, the question, its intent and subtype, the stale value,
the successor where one exists, the gold value, and the answer. It shows **no store, no condition,
no view, no tag, no evidence-in-view flag**; rows are in a seeded shuffle (seed 42) over every
distinct answer, and the key (row → store, condition, item) is written to
`r85_graphiti/a2/sheet_key.json` with its sha256 in the ledger (`AUX-R85-A2-SEAL`) before the
sheet is opened. A distinct answer appears once and its category propagates to every row that
shares the input.

**What the first reader reads.**

1. **Every obligation answer**: the 47 × 6 = 282 of the primary population and the 57 × 3 = 171 of
   the FR-Bank-only block, 453 nominal, distinct fewer by the shared T = M cases. Complete, not
   sampled, so the obligation comparisons in §7 are human-scored end to end.
2. **Licensed items, a random audit**: 120 answers, 20 per primary cell, seed 42, for detector
   agreement on Q3 and Q5.
3. **Licensed items, targeted**: every licensed item on which the detector's correct-or-declined
   verdict differs between any two conditions within a store, all six of its answers.

The random and targeted licensed samples are reported separately; no error rate is computed from
their mixture.

**The licensed audit has a registered consequence.** On the random 120 the detector's verdict
(correct at TAU_GOLD; declined by `is_abst`) is compared with the reader's Q3 and Q5. **Material
error** is a disagreement rate above 20% on either question, or Cohen's kappa below 0.60 on Q3. If
the audit shows material error, the licensed endpoint is no longer the detector's: the human read
is extended to **every licensed answer** (131 × 6 = 786 nominal, plus the block's 43 × 3) before
A2-P3 is read, and C3 prints under human labels. If that extension is not complete by the Step 4
date, A2-P3 prints "not read: the detector failed its audit at rate r" and the ruling table (§9)
is entered on A2-P1 and A2-P2 alone; the licensed rows still print, detector-scored, with the audit
rate in their caption and no claim on them. The targeted read (item 3) catches the flips the
detector reports; the random audit is the protection against the flips it does not, and this
paragraph is what happens when it finds them.

**The second annotation.** (i) Every obligation item on which the first reader's category differs
between any two conditions within a store, all of its answers (the decisive obligation set);
(ii) 40 of the 120 random licensed answers, seed 43. **The registered second reader is an
independent person**; the author names one at freeze or records that none is available. Raw
agreement and Cohen's kappa per question through `reviews/v18/annotator_agreement.py` extended for
Q5 and Q6. Disagreements are resolved by the first reader's label; the count prints, and every §7
reading prints once more under the independent reader's labels on the decisive set, so the reader
can see whether the verdict depends on who read. **If no independent reader is available**, the
author re-reads the same two samples on a re-shuffled sheet (seed 44) opened no sooner than 48
hours after the first read is sealed (`AUX-R85-A2-SEAL-1`); that figure prints as *intra-rater
consistency*, is labelled so wherever it appears, is not presented as validation of the
interpretation, and the paper's sentence stays the one it already carries: that the labels are one
person's. The two are not interchangeable and the ledger key differs (`AUX-R85-A2-AGREEMENT-INDEP`
or `-INTRA`, never both filled from one person).

**The rule between the two scorers.** On obligation answers the human category is the endpoint;
where it and the detector's stale flag disagree, the human category governs and the detector row
prints beside it with agreement, precision and recall against the human label. On licensed
answers the detector's TAU_GOLD row is the endpoint unless the audit paragraph above moves it.
Nothing in the rubric is chosen after an answer is seen.

**Detector rows, every answer, secondary**: stale use at TAU_HI and TAU_GOLD, stale surfacing,
successor use, obligation reported (A7), abstention (`is_abst`), PRESENT correct at TAU_GOLD and
TAU_HI, the evidence-in-view flag; by cell, by state, by intent; `AUX-R85-A2-DETECTOR`.

**Time.** About 450 obligation answers plus 120 plus the targeted set, at 30 to 45 seconds each:
six to eight hours for the first read; two to three for the second; the full licensed extension,
if the audit triggers it, eight to ten more.

## §7 Comparisons and predictions

**Primary: overall paired differences on the fixed populations, every item included** (unreached
obligations and extraction misses among them), per store, per answerer, on the 178:

- **C1, tags carry**: stale endorsement, T − U, on the 47.
- **C2, masks against tags on obligations**: stale endorsement, M − T, on the 47; correct
  current-or-handling, M − T, on the 47.
- **C3, the cost on licensed items**: correct, M − U and T − U, on the 131; unnecessary decline,
  M − U, on the 131; each also by intent (CURRENT-STATE 65, UPCOMING 26, CHANGE-AWARE 35,
  PAST-EVENT 5) as descriptive rows with intervals, no bar per intent.

**Secondary, descriptive**: the per-item transition tables U→T and T→M (stale→correct,
correct→stale, correct→declined, declined→correct, unchanged), by state and by the §5 (ii) sets,
as counts of wins, losses and ties separately for obligation and licensed items; the FR-Bank-only
block's three rows in their own table; the "reached and marked" subset (b) as an explanation of
C1 and C2, never as a substitute for them.

**Predictions**, written before any view is built, read per store under §5's rules.

**A2-P1, tags carry (C1).** T's stale endorsement rate is below U's by more than the tolerance,
with the interval excluding zero, on both stores. On FR-Bank because its own marks reach 0.7833 of
the forbidding records in view; on Graphiti because P1's recall of 0.4054 puts a correct tag on
roughly three of every five forbidding records it extracted, and the DS record shows the model
obeys a correct tag (stale use at TAU_GOLD 0.0571 on tagged reach against 0.4737 on untagged
reach, `AUX-DS-A4-STAGE2-MINI`, ALWAYS). No structural bound applies.
> HOLDS: Shown the same five records with the store's own lifecycle states, GPT-4.1 mini endorses
> the obsolete value on $T$ of the 47 obligations against $U$ without them, $D$ fewer with
> interval $I$.
> FAILS: Shown the same five records with the store's own lifecycle states, GPT-4.1 mini endorses
> the obsolete value on $T$ of the 47 obligations against $U$ without them, within tolerance or
> above (interval $I$): on this store the tags do not reach the answer.
> INCONCLUSIVE: the HOLDS sentence with "with interval $I$ that includes zero; the population does
> not resolve the comparison" in place of the verdict.

**A2-P2, masks equal tags on obligations (C2).** |M − T| on stale endorsement is within the
tolerance on both stores: the mask removes exactly the lines the tag marks, and the model already
declines to use a marked line. The mechanism that would break it is set (e), a stale record marked
`active` imported from ranks 6 to 10. The structural bound n_TM / 47 prints beside it and decides
whether the reading is empirical or by construction.
> HOLDS: Dropping the marked records instead of showing them marked changes GPT-4.1 mini's stale
> endorsement from $T$ to $M$ of 47, within tolerance (interval $I$; the two views differed on $n$
> of the 47): on obligations the mask and the tag do the same work.
> HOLDS structurally: the two views differed on $n$ of the 47, so no difference beyond the
> tolerance was possible; the observed difference is $D$.
> FAILS (M below T): Dropping the marked records lowers stale endorsement from $T$ to $M$ of 47, $D$
> with interval $I$: a marked stale record in view is still used; the mask does work the tag does
> not.
> FAILS (M above T): Dropping the marked records raises stale endorsement from $T$ to $M$ of 47, $D$
> with interval $I$, with $E$ of the difference on records the mask imported from ranks 6 to 10.

**A2-P3, masks cost licensed answers (C3).** On FR-Bank, M's correct rate on the 131 is below U's
by more than the tolerance (its own marks call 1,389 of 3,305 lines non-active, so the mask
removes about two fifths of every view). On Graphiti, M's correct rate is within tolerance of U's.
On both stores the loss, where there is one, is expected to concentrate in CHANGE-AWARE and
PAST-EVENT, printed per intent. No structural bound applies (U and M differ on every item).
> HOLDS (FR-Bank): Filtering FR-Bank's view to its own active records lowers GPT-4.1 mini's
> correct rate on the 131 licensed questions from $U$ to $M$, $D$ with interval $I$; $F$ of the loss
> falls on the 40 questions about the past or a change.
> HOLDS (Graphiti): Filtering Graphiti's view to its active edges leaves the correct rate on the
> 131 licensed questions at $M$ against $U$, within tolerance (interval $I$).
> FAILS and INCONCLUSIVE: the same sentences with the direction and the interval the numbers give.

HYBRID-style rows are not run here; the summary route is Amendment 1's. GR-1 to GR-5 and P1 to P4
are unaffected by this file (§0 is the author's).

## §8 Budget, from measured anchors

| Line | Units | Anchor | Where measured | Expected | Worst (1.3×) |
|---|---|---|---|---|---|
| GPT-4.1 mini, primary six cells | ≤ 1,068 rows | $0.1091 / 422 rows = $0.000259 / row | `AUX-DS-SPEND` | $0.28 | $0.36 |
| GPT-4.1 mini, FR-Bank-only block | ≤ 300 rows | the same | | $0.08 | $0.10 |
| Probes | 1 mini (+ 1 Haiku if (b)) | list | — | < $0.01 | < $0.01 |
| Retrieval | none: Graphiti's is Amendment 1 Step 5's, FR-Bank's is recorded | — | — | $0.00 | $0.00 |
| Human read | — | the author's time, §6 | — | — | — |
| **Amendment 2 subtotal, mini** | ≤ 1,368 rows | | | **$0.36** | **$0.47** |
| (b) Claude Haiku 4.5, the same inputs, k = 1, synchronous, the answer read from the last JSON object (A4 Lane 2) | ≤ 1,368 rows | $0.4023 / 452 = $0.00089 / row | `AUX-DS-A2-SPEND` | $1.22 | $1.58 |

**Standing of the two lines.** The mini line is registered and runs. **The Haiku line is an
extension the author authorizes or declines at freeze, by ticking one box below**; it is not
covered by Amendment 1 §7's Haiku rule and does not enter that rule's arithmetic: that rule (billed
total at or under $15.56 after X1 and X3, evaluated once) is unchanged in text and in evaluation,
and its expected outcome (Haiku dropped on the summary route) is unchanged by anything here. The
R85 running total at this writing is $11.8770 (`AUX-R85-G10-INGEST`); Amendment 1's remaining
expected lines are $2.76; this amendment adds $0.36 expected, $0.47 worst, and $1.22 more if (b) is
authorized. The addendum's outer $28 stop is not approached.

- [ ] Haiku 4.5 on the six cells and the block is **authorized** at $1.22 expected (runs at Step 6,
      after the mini readings are reported).
- [ ] Haiku 4.5 is **declined**; the row prints a dash with its price in the footnote.

Billing paths unchanged: the OpenAI metered key for mini (the path that emits `tok_in`, `tok_out`,
`usd` per row); the Anthropic metered key for Haiku. Identifier probes before the first call of
each provider, the served identifier beside every cost line.

## §9 The ruling table: which sentence the paper prints, fixed before the numbers

Per store, from the three readings. The two-store sentence prints only when both stores fall in
the same row; otherwise the paper prints the two rows and names the difference.

| A2-P1 | A2-P2 | A2-P3 | The sentence |
|---|---|---|---|
| holds | holds (empirically or structurally) | holds (a loss on FR-Bank; none on Graphiti) | Shown tagged, the model declines the obsolete value about as often as when the record is masked, and keeps the licensed answers the mask removes: at answer time the tag does the mask's work at a cost the mask pays and the tag does not. Where P2 held structurally, the sentence adds that the two views rarely differed on this store. |
| holds | fails, M below T | any | Tags help, and exposing a marked stale record still costs: the mask does work the tag does not on obligations, at the licensed cost §7 C3 prints. The recommendation is conditional (masks for current-state obligations, tags where the past is asked about), and the paper says so. |
| holds | fails, M above T | any | The mask imports stale records the tag had marked; a mask over a store whose marks are this precise is worse than its tags. |
| fails | any | any | The store's tags do not reach the answer. On Graphiti this is the census's extraction finding at answer time; on FR-Bank it would contradict the NOK row (`AUX-RESP-A1-BELIEVED`, +0.1292) and prints as a gap between knowing and doing that the paper reports as such. |
| inconclusive | any | any | The population does not resolve whether the tags reach the answer; the intervals print, the transition tables print, and no recommendation is drawn from this store at answer time. |
| any | any | not read (the licensed audit failed and the extension did not complete) | The obligation sentence of the matching row prints; nothing is said about licensed cost, and the audit rate prints where the licensed rows would be cited. |

No sentence outside this table is written from these numbers. The transition tables, the §5 (ii)
sets and the per-intent rows print in the appendix under every row; the FR-Bank-only block prints
in its own table with no sentence in the main text.

## §10 Order of execution

Each step ends with a report and a hard stop for the author's go-ahead; the running billed total
prints at every stop.

0. **Freeze.** The author rules on §0 (a `D-R85-n` entry for Amendment 1's population, before its
   Step 4), names the independent reader or records that none is available, ticks the Haiku box,
   fills the §11 dates; commit this file (pathspec only); record its sha256 in
   `r85_graphiti/NUMBERS_R85.md` as `AUX-R85-A2-FREEZE`. No call.
1. **Views** (after Amendment 1 Step 5 has landed its retrieval): the cells, the prompt texts and
   digests (`AUX-R85-A2-PROMPTS`), the view census (`AUX-R85-A2-VIEWS`: distinct inputs per cell,
   the shared T = M count, M's short views, lines changed U→T, lines removed T→M), the three §5
   quantities (`AUX-R85-A2-RESOLUTION`: the structural bound per store, the mechanism sets, and
   which reading rule each prediction will meet), the evidence-in-view flags, and the by-eye check
   of ten views (`AUX-R85-A2-CHECK`). No call.
2. **Mini**: probe, projection against the $0.47 worst line, the run (cache
   `r85_graphiti/a2/cache_mini/`), the served identifier and the billed row
   (`AUX-R85-A2-SPEND`).
3. **Detector rows and the sheet**: every answer scored by the committed functions
   (`AUX-R85-A2-DETECTOR`); the transition tables; the blind sheet built, its key sealed
   (`AUX-R85-A2-SEAL`). No answer read at this step.
4. **The human read**: the first pass (§6, items 1 to 3), sealed (`AUX-R85-A2-SEAL-1`); the
   licensed audit and its consequence if triggered; the second annotation; agreement and kappa
   (`AUX-R85-A2-AGREEMENT-INDEP` or `-INTRA`).
5. **Readings**: A2-P1 to A2-P3 per store under §5's rules, the human endpoint where §6 puts it,
   the detector endpoint beside, the second reader's labels on the decisive set; the ruling table
   row per store (`AUX-R85-A2-P1..P3`, `AUX-R85-A2-RULING`); the FR-Bank-only block's table.
   Nothing touches `paper_v19.tex` before the author's ruling on this report.
6. **Haiku**, if and only if the box in §8 is ticked at freeze: the same inputs, its own rows, its
   own reading of A2-P1 to A2-P3 printed beside mini's.
7. **Paper** (§11), on the author's ruling.

## §11 Cutoffs and paper

**Cutoffs follow the submission schedule, not a date of this amendment's own.** The author fills
the dates at freeze:

| Milestone | By (local) | If missed |
|---|---|---|
| Steps 1 to 3 | the day after Amendment 1's Step 6 close (registered 23 September), i.e. **24 September 23:59**, unless the author sets another date here: ______ | the amendment goes to the October rebuttal card under the R85 name |
| Step 4 complete (both reads sealed; the licensed extension if triggered) | the author's date from the submission schedule: ______ | the human endpoint prints on the cells whose reads are complete and says which; the detector rows print in full; no pooling of a partial read with the detector; A2-P3 under the audit paragraph's rule |
| Step 6 (Haiku, if authorized) | the same date as Step 4 | dropped, recorded with its price |
| Integration | on the author's ruling | — |

**Paper.** Appendix G gains a second table (the answer stage on the 178: six cells × {stale
endorsement, correct current-or-handling, other error} on the 47 and {correct, unnecessary
decline, appropriate decline, wrong} on the 131, human-scored where §6 says so, the detector rows
beside, per-intent rows for the licensed population, the three §5 quantities above it, the DS A4
ALWAYS reference row beside FR-Bank T with its coverage stated) and a third, smaller table for the
FR-Bank-only block. The kappa sentence of Section 4 (v19) gains the A2 agreement figure under its
correct label. One sentence in Section 8's downstream chain, of the ruling-table row's form, as a
swap (the main text sits at reading 485, the boundary; the report names the line that goes). E.9
and the Amendment 1 placements are unchanged; if the author's §0 ruling restricts Amendment 1's
Graphiti rows to the 323, Appendix G's first table says so in its caption.

## §12 Files

- `r85_graphiti/a2/`: `build_views_a2.py` (the cells, the prompt variants, the census, the three
  §5 quantities, the evidence-in-view flags, the by-eye draw), `run_a2.py` (probe, projection, run,
  cache; the Haiku lane behind the §8 box), `score_a2.py` (the detector rows, the transition
  tables, the sheet and its key, the readings under §5's rules and the ruling row),
  `agreement_a2.py` (the second-annotation draw, the licensed audit and its trigger, kappa, calling
  `reviews/v18/annotator_agreement.py`), `sheet_a2.md` (generated), `sheet_key.json`, `README.md`.
- **Imported, not copied or edited**: `ds_downstream/tools/prompts_ds.py`,
  `amend4_header.py` (`HEADER`, `persona_fields`, `is_abst`, `first_sentence`), `run_ds.py`
  (`records`, `score_answer`), `amend7_reported.py` (`reports_obligation`);
  `resp_review/tools/amend1_resp.py` (`believed_flags`), `resp_common.py` (`render_line`,
  `lifecycle_tag`, `load_cell`, `variant_ids`); `r85_graphiti/g10/retrieve.py`'s record (Amendment
  1 Step 5); `r85_graphiti/g10/census_forbidding.py`'s matcher for set (a) on Graphiti. Nothing
  under `ds_downstream/`, `resp_review/` or `reviews/` is modified except the one extension of
  `annotator_agreement.py` for Q5 and Q6, additive and asserted not to change its existing output
  on the section C sheet.
- Ledgers: `r85_graphiti/NUMBERS_R85.md` (`AUX-R85-A2-*`), `r85_graphiti/DEVIATIONS_R85.md` (from
  `D-R85-16`; the author's §0 ruling takes the first free number; `D-R85-16` or the next is
  reserved for the ten-line re-render of §4 if Step 5's record needs it), `r85_graphiti/DISCLOSURE.md`
  unchanged.
- Review mapping: the same items as Amendment 1 §11, plus the mock reviewer's "intermediate
  metrics can mislead" point, which this amendment answers by content until
  `reviews/v18/REVIEW_MOCK.md` is filed.

<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended at the freeze; the draft's sha256 2e7715d1… is taken over the bytes above this line and the freeze sha256 (AUX-R85-A2-FREEZE) over the whole file. -->

## Freeze decisions (2026-09-17; program R114; recorded before any Phase 3 call; D-R85-18)

The section 10 step 0 decisions, as the author's instruction of 2026-09-17 settles them or leaves them:

1. **The §0 ruling.** Amendment 1 Steps 4 to 6 ran on the 323 FULL-variant items (D-R85-17, the author's instruction of
   2026-09-17: "Graphiti monitoring on the 323 FULL items; the matched primary answer-stage comparison on the 178 FULL
   non-ABSENT items"). This amendment's primary population is the 178 as §3 states; the FR-Bank-only block the 100.
2. **The independent second reader.** Not named at this freeze. Step 4 (the human read) does not run in program R114; the
   author names a reader, or records that none is available (the §6 intra-rater path), before Step 4 opens. No annotator
   identity is invented; no model label stands in for a human one.
3. **The Haiku 4.5 box (§8).** Not authorized in this pass (the instruction: "defer optional Haiku extensions"). The row
   prints a dash with its price ($1.22 expected) unless the author ticks the box later; the mini line runs.
4. **The §11 dates.** Steps 1 to 3: the draft's own default, 24 September 23:59 (met on 17 September). Step 4 and Step 6:
   the author's, not set here.
5. **The M line rule (R113 REPORT item 3).** Confirmed as §4 states it and as R113 built it: M = the lines of ranks 1 to 10
   whose store-own state is `active`, in rank order, the first five, **renumbered from [1]**; every M line reads `active`;
   where ranks 1 to 5 hold no non-active line M's complete input is T's and the answer is shared. Short M views (fewer
   than five lines) are counted and printed, as §4 provides; no line is added from beyond rank 10.
6. **Step 5's record.** `r85_graphiti/g10/retrieval_g10.json` holds all ten rendered lines per item with each edge's RULE 1
   state (built 2026-09-17, AUX-R85-G10-RETRIEVE); no re-render is needed and D-R85-16's reserved number is not used for
   it. Three of the 323 items returned fewer than ten edges under the stock search (D-R85-20); of the 178, one
   (`frbank:billy:billy_q05:FULL`, six edges) is affected: M draws from six lines.
7. **Freeze mechanics.** By sha256 of this file recorded as `AUX-R85-A2-FREEZE` in `r85_graphiti/NUMBERS_R85.md` before the
   first Phase 3 call, the file left uncommitted at the author's instruction (D-R85-18); the scripts assert the hash.
8. **What runs in program R114.** Steps 1 to 3 (the views, the mini run, the detector rows, the transition tables, the blind
   sheet and its sealed key). Steps 4 and 5 (the human read; A2-P1 to A2-P3 read under §5's rules with the human
   endpoint) and Step 7 (the paper) wait on the author. The detector rows print as secondary and provisional; no ruling-
   table row is entered from them.
