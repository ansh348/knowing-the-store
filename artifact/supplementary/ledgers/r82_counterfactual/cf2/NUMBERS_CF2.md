# NUMBERS_CF2 — ledger for the CF-2 cell (ADDENDUM_CF2.md, frozen f016f03; Amendment 1 at §14)

Every number CF-2 prints enters the manuscript through a key in this file and no other way.
Keys are reserved in the registration's §9 and written as the build proceeds; a key that cannot
be computed carries a dash and its reason. No store version, index, label, monitor score or
baseline score exists at the time of the entries below. Verifier: `tools/verify_cf2.py`.

---

## 1. AUX-CF2-CENSUS — the census under the CF-2 predicate (2026-09-12, `select_pairs.py --cf2 --census`, `cf2/census_cf2.json`)

Stages: raw → individuates in PRESENT → not on the v2 superseded list → zero overlap with the
90 / the 84 / the 36, or re-admitted (O1, O2). Beside each, `reviews/CF2_SCOPE.md` Phase 2.

| Class | CF-2 | Scope | Admitted | Verdicts before the CF-2 read | Admissible | Personas | Distinct (persona, scrubbed name) |
|---|---|---|---:|---|---:|---:|---:|
| EXPIRY, frozen two-category predicate | 46 → 41 → 41 → 41 → 38 → 38 | 46 → 41 → 41 → 32 → 25 → 25 | 38 (25 zero-overlap, 9 O1, 4 O2) | 29 ELIGIBLE, 9 INELIGIBLE | 29 | — | — |
| EXPIRY, O3 widened | 87 → 59 → 53 → 45 → 41 → 41 | 87 → 41 | 41 | 41 unadjudicated | 41 | — | — |
| EXPIRY, all | | | **79** | 29 / 9 / 41 | **70** | 25 | 62 |
| RETRACTION | 1,590 → 1,379 → 1,173 → 1,053 → 1,048 → 1,043 | identical | 1,043 | 1 ELIGIBLE, 25 INELIGIBLE, 1,017 unadjudicated | **1,018** | 40 | 509 |
| SUPERSESSION | 3,347 → 3,230 → 3,230 → 3,187 → 3,170 → 3,133 | identical | 3,133 | 3 INELIGIBLE, 3,130 unadjudicated | **3,130** | 40 | 2,399 |

Scarcity order: EXPIRY > RETRACTION > SUPERSESSION (unchanged from CF-1). The only movement
against the scope is the two registered re-admissions (+9 at the 90 stage, +4 at the 84 stage);
`rosa lb_00522` falls at individuation and is not admitted.

## 2. AUX-CF2-ADJUDICATION — the CF-2 read, complete (12 Sep 2026; `cf2/verdicts_12sep.json`, sha256 `48112523bded3ffe…`, merged into `cf2/adjudication_queue.json` by (state, entry_id) and regenerated as `cf2/adjudication_cf2.json`; every row checked against the queue)

Criteria: `ADDENDUM_R82.md` §3.1 verbatim; the author's dated notes are in `ADDENDUM_CF2.md` §3.1
(amendment text under §14). Walk statuses: ELIGIBLE / INELIGIBLE (author's verdicts, 12 Sep);
REUSED (CF-1 ELIGIBLE carried, not re-read); SKIP-RANK (not read — an earlier same-name candidate
for the persona was ELIGIBLE; recorded as not adjudicated with that reason); UNREAD (past the
state's stop; stays unread).

**Method (author's line, verbatim).** Method: entries presented by a language model in walk order, triaged within each batch (plan-like first, plain records grouped) for retraction, plain tables for expiry and supersession; every entry shown; verdicts typed by the author; the model flagged disagreements only after the author's verdict. Disclosed under the AI-use line.

**Read telemetry (author's line, verbatim).** Read telemetry, 12 Sep 2026, one session: expiry 41 verdicts in about 25 minutes; retraction about 367 reads (verdicts plus rank-skips) in 8 batches, measured eligibility 35/367 = 0.095 (34 usable); supersession 165 reads in 4 batches, 106 ELIGIBLE, 53 INELIGIBLE, 6 rank-skips, rate 106/159 = 0.667.

| Key | Value |
|---|---|
| **AUX-CF2-ADJUDICATION-EXPIRY** | 70 rows in the queue; stop at position **70**. Walk statuses: ELIGIBLE 20, INELIGIBLE 16, REUSED 29, SKIP-RANK 5. **Verdict reads 36** (41 with rank-skips); ELIGIBLE **49** (20 new + 29 reused); new-candidate eligibility **0.5556**. |
| **AUX-CF2-ADJUDICATION-RETRACTION** | 1018 rows in the queue; stop at position **440**. Walk statuses: ELIGIBLE 35, INELIGIBLE 334, REUSED 1, SKIP-RANK 70, UNREAD 578. **Verdict reads 369** (439 with rank-skips); ELIGIBLE **36** (35 new + 1 reused); new-candidate eligibility **0.0949**. |
| **AUX-CF2-ADJUDICATION-SUPERSESSION** | 3130 rows in the queue; stop at position **165**. Walk statuses: ELIGIBLE 106, INELIGIBLE 53, SKIP-RANK 6, UNREAD 2965. **Verdict reads 159** (165 with rank-skips); ELIGIBLE **106** (106 new + 0 reused); new-candidate eligibility **0.6667**. |

Counted against the author's telemetry line: retraction verdict reads are 369 by the file
(the line says "about 367"), and "34 usable" is the author's within-walk count; the acceptance
walk below finds 33 usable under the one-per-name rule applied across states (three retraction
`project` candidates yield to same-name pairs: chenoa `lb_00029`, jake `lb_00110`, jerome
`lb_00184`). Supersession: 106 / 159 = 0.667 against the 0.769 §3.2 assumed. Expiry `patrick
lb_00376` (six-week class), PENDING in the first deposit, is ELIGIBLE by the author's call
("weak E").

## 2a. AUX-CF2-CONSTRUCTION and AUX-CF2-OVERLAP — the acceptance walk (12 Sep 2026; `cf2/cf_pairs_cf2.json`; no question drafted, no store version built)

`select_pairs.py --cf2 --accept`: ELIGIBLE rows only, in queue order, states in scarcity order
EXPIRY > RETRACTION > SUPERSESSION, cap 4 per persona per state, one pair per (persona,
scrubbed name) across the whole draw; stop at the quota. Quotas per §14: 100 / 30 / 30.

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (draw) | **160 pairs accepted: SUPERSESSION 100, RETRACTION 30, EXPIRY 30**, over **40 personas**; cap never binding (max 4 per persona per state, reached by elena, kenji, kofi, marcus, mirri, omar, priya, thanh in supersession). Last accepted queue position: expiry **44** of 70, retraction **404** of 440 read, supersession **152** of 165 read. Sources: expiry 15 CF-1 reused + 15 author; retraction 1 reused + 29 author; supersession 100 author. Expiry by class: 15 under the frozen two-category predicate (OBLIGATIONS 7, LOGISTICAL_CONTEXT 8), **15 O3** (PROJECTS_ENDEAVORS 10, RELATIONAL_BONDS 2, HEALTH_WELLBEING 1, HOBBIES_RECREATION 1, FINANCIAL_MATERIAL 1). Passed over at acceptance, all by the one-per-name rule, none by the cap: EXPIRY 0029 jake `lb_00358` (project); RETRACTION 0077 jake `lb_00110` (project); RETRACTION 0120 chenoa `lb_00029` (project); RETRACTION 0224 jerome `lb_00184` (project). ELIGIBLE but unreached: expiry 18 (positions 45–70, among them patrick's five conference entries, priya's two, raj's four, rosa, thanh's two, valentina's two, yoli), retraction 3, supersession 6. |
| **AUX-CF2-OVERLAP** | Accepted pairs carrying an overlap tag, by (persona, entry_id): **O1 (CF-1's expiry pairs re-admitted): 7** — (billy, lb_00273), (david, lb_00496), (elena, lb_00488), (fatima, lb_00393), (marcus, lb_00235), (marley, lb_00343), (mehmet, lb_00429). **O2 (the four ELIGIBLE entries the 84 filter removed): 0** — none reached: raj `lb_00437`, `lb_00443`, `lb_00447` and thanh `lb_00476` sit at expiry positions 57–59 and 66, past the position (44) at which the quota filled in persona order. No other accepted pair overlaps the 90, the 84 or the 36. |
| accepted per persona (SUP / RET / EXP) | aisha 3/3/2, alex 3/1/0, amara 3/0/0, aroha 1/1/0, billy 1/1/1, bruna 3/1/0, callum 2/1/2, chenoa 1/1/0, dariush 0/0/3, david 1/0/2, diane 1/0/2, dmitri 3/1/0, elena 4/1/3, fatima 3/0/3, ingrid 3/1/0, jake 2/1/2, jerome 3/0/1, joonho 3/0/0, kenji 4/0/0, kofi 4/1/1, leila 2/1/0, lily 2/1/0, marcus 4/1/3, marley 1/2/2, mehmet 2/0/2, mirri 4/0/0, nadia 2/0/0, omar 4/1/0, pan 2/1/1, patrick 1/1/0, priya 4/2/0, raj 3/2/0, rosa 2/1/0, saga 3/1/0, samuel 2/0/0, thanh 4/0/0, tom 2/0/0, valentina 3/0/0, yoli 3/1/0, zara 2/1/0 |

## 2b. AUX-CF2-CONSTRUCTION — questions and PN records (CF2-BUILD-2, 12 Sep 2026; gpt-4.1-mini and text-embedding-3-small only; nothing on the Anthropic key)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (D-CF2-2 replacement) | `cf2:zara:project:AA_application` (RETRACTION, queue position 225, ELIGIBLE by the author) **excluded: authoring predicate** — `author_pn.py` failed twice on MIN_DISCR (n_discr_old 2 < 3; the cancellation must name "AA SED program application"); the verdict stands. Replaced by **`cf2:pan:family_member:beam_role_in_business`** (position 414, zero-overlap, not O3); mehmet `lb_00156` at 410 was passed over by the one-per-name rule (mehmet's `project` is an accepted expiry pair). Composition unchanged 100 / 30 / 30. |
| **AUX-CF2-CONSTRUCTION** (questions) | `cf2/cf_questions_cf2.json`: **160 questions**, frozen renderer sha `b748247b…` (seven fields unchanged), seed 42, three paraphrases, seeded pick, intent gate under AV2. **Substitutions 3** (elena `event:wedding_timeline`, fatima `trip_schedule:salone_del_mobile_2026`, marcus `morning_phone_usage_duration` — the seeded paraphrase failed the gate, the next in order passed), **redrafts 0**; the D-CF2-2 replacement drafted and appended with its own trail (first pick, index 1). **Questions sha256 `871c353762e8065fff141039cd452e73df34cca8cd61cb21712324ff53645b0e`**. First-person voice 141 of 160 (CF-1: 25 of 30). Tokens 50,234 in / 7,374 out; **$0.0319**. |
| **AUX-CF2-CONSTRUCTION** (PN records) | `cf2/cf_pn_texts_cf2.json`: **130 records authored** (100 supersession, 30 retraction) through `author_pn.py` unchanged (prompt sha `b6f53b1a…` = CF-1's), seed 42; 30 expiry pairs anchor-only. Predicates on every record: n_discr ≥ 3 both sides, detector on the original ≥ TAU_HI 0.80 (all 130 at 1.00), cross-guard, gold cover at TAU_GOLD. **Retries 1** (cf2:zara:medication:vitamin D supplement dosage — passed on the frozen second attempt). **Retraction cosine** to the original under text-embedding-3-small, measured not enforced (n = 30): min 0.463, p25 0.623, median 0.675, p75 0.729, max 0.789; **0 of 30 at or above 0.85** (CF-1: 1 of 10; the store's slot branch fires regardless, Amendment 2). Tokens 42,668 in / 3,184 out / 1,177 embed; **$0.0222**. Aborted first run (stopped at the 21st authored pair, no meter reached): ≈ $0.004 **[est]**. |

## 2c. AUX-CF2-PNREAD and AUX-CF2-QUESTIONREAD — the author's two reads (12 Sep 2026; `cf2/cf2_reads_12sep.json`, sha256 `ae207a01f39b7a94…`, merged by (state, persona, entry_id) into `cf2/pn_read_verdicts.json` and `cf2/question_read_flags.json`; every row checked against the read documents' order)

Merge key: (state, persona, entry_id) — (state, entry_id) alone is ambiguous, entry ids repeat
across personas (52 collisions among the 130 authored pairs).

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** | Three-way read of the 130 authored records (`reviews/CF2_PN_READ.md`): **supersession 69 YES / 21 NO-paraphrase / 10 NO-implausible; retraction 29 YES / 1 NO-implausible** (record 104, alex `project_release_strategy`: half-reverses rather than cancels). **32 NO in all**, every one re-authored once at seed 4242 under D-CF2-3 (§2d). **Failure pattern, as observed by the author:** paraphrases concentrate on attitude, feeling and philosophy slots; implausible successors on identity-adjacent slots (career, family history, trauma). **What the read guards:** the monitor's input is value-scrubbed — no authored text reaches any index or prompt — so this read guards **label honesty under Definition 1** (a paraphrase would make the PN label semantically hollow), not the measurement. |
| AUX-CF2-PNREAD, author's notes verbatim | (1) Three-way read: YES (a different value or a real cancellation this person could plausibly come to), NO-paraphrase (same fact reworded; under Definition 1 the old value would not make the answer wrong, so the PN label would be semantically hollow), NO-implausible (contradicts the persona or cancels something other than the plan). (2) Result: supersession 69 YES / 21 NO-paraphrase / 10 NO-implausible; retraction 29 YES / 1 NO-implausible (104: half-reverses rather than cancels). (3) Pattern: paraphrases concentrate on attitude, feeling and philosophy slots; implausible successors on identity-adjacent slots (career, family history, trauma). (4) The monitor's input is value-scrubbed; the read guards label honesty, not the measurement. (5) Method: records presented by a language model with a look-twice flag on some rows; verdicts typed by the author; disclosed under the AI-use line. Author caught 004 (Series A to seed is a rewind, not a successor) unflagged. |
| **AUX-CF2-QUESTIONREAD** | Value-token read of the 160 questions (`reviews/CF2_QUESTION_READ.md`): **90 of 160 flagged** — by the file, supersession 47 of 100, retraction 21 of 30, expiry 22 of 30 (the author's note gives the split as 43 / 19 / 28 "after the four consistency additions"; the per-row file governs and sums to the same 90). CF-1 found 3 of 30. **Construction explains the rise:** CF-2's retraction and expiry slots are named after their events, so the question names the plan. **Disclosure, not a gate:** the question is identical across the three store versions and cannot carry the label. Rendering note: item 119's raw slot name `msc_sports_rehabilitation` appears verbatim in the question. 83 distinct tokens; the most frequent appear twice (vaping, malaria, tea, vitamin D, CIMA, Isfahan, wedding). |
| AUX-CF2-QUESTIONREAD, author's notes verbatim | (1) Rule applied by the author: flag YES when the question names any specific condition, method, item, place, person (other than the persona's own name), date or event; NO when it names only the slot's topic. Persona's own name is not a value. (2) Result: 90 of 160 flagged (supersession 43 of 100 after the four consistency additions, retraction 19 of 30, expiry 28 of 30). CF-1 found 3 of 30. The difference is construction: CF-2's retraction and expiry slots are named after their events, so the question names the plan. The question is identical across the three versions and cannot carry the label; this is a disclosure, not a gate. (3) 119: the raw slot name msc_sports_rehabilitation rendered verbatim in the question; flagged and recorded as a rendering note. |

## 2d. AUX-CF2-PNREAD — the D-CF2-3 re-authoring (12 Sep 2026; `cf2/cf_pn_texts_cf2_reauthor_4242.json`; gpt-4.1-mini + text-embedding-3-small)

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** (re-authoring) | **32 records re-authored once** through `author_pn.py` unchanged at **seed 4242** (`tools/cf2_reauthor_pn.py`; the only patched constant is the seed). The tool's digest binds the seed: the file records prompt sha `3b5c9c236b6783e2f306bd80ace8fb3b67311bd5643cbe8b20cc7eaf6d796c5a` = the frozen prompt `b6f53b1a…` at seed 4242 (asserted before patching). All 32 pass the write-path predicates; **retries 0**. **15 of 32 are byte-identical to the first attempt** — supersession 9 paraphrase + 5 implausible, retraction 1 — so at temperature 0 the alternate seed moved 17 outputs; the identical ones fall to D-CF2-2 unless the author reads them differently. Re-read document `reviews/CF2_PN_REREAD.md`; verdicts pending in `cf2/pn_reread_verdicts.json`. Tokens 10,441 in / 807 out / 51 embed; **$0.0055**. |
| supersession spares, for the D-CF2-2 consequence | 106 ELIGIBLE − 100 accepted = **6 spare** in walk order (positions 153–165); every failure beyond six drops the supersession quota by the shortfall under a further deviation, unless the author extends the supersession read past position 165 (2,965 UNREAD, rate 0.667 so far). Retraction: 3 spare ELIGIBLE; expiry: 18 unreached ELIGIBLE. |

## 2e. AUX-CF2-PNREREAD — the re-read of the 32 re-authored records (13 Sep 2026; `cf2/cf2_pn_reread_13sep.json`, sha256 `07212b1d529a7c84…`, merged by (state, persona, entry_id) into `cf2/pn_reread_verdicts.json`; every row checked against `reviews/CF2_PN_REREAD.md`'s order and identity flags)

| Key | Value |
|---|---|
| **AUX-CF2-PNREREAD** | Of the 32 re-authored at seed 4242: **17 re-read** (the ones the seed changed) → **1 YES** (re-read 20, omar `budget_allocation`, "a real change of value") and 16 the same failure in new words (13 paraphrase, 3 implausible); **15 kept the first verdict by identity** (byte-identical text; 9 paraphrase + 5 implausible supersession, 1 implausible retraction). **Outcome: 30 supersession and 1 retraction records fail after the frozen retry and fall to D-CF2-2**; the YES record replaces its first attempt in `cf2/cf_pn_texts_cf2.json` (`reauthored_under: D-CF2-3`, seed 4242). Supersession spares in walk order 6 (positions 153–165); **shortfall 24 before authoring losses**. |
| **Instrument note** (author's, for the ledger and for CF-3) | At temperature 0 an alternate seed changed 17 of 32 outputs and fixed 1; "one frozen retry" is nearly a no-op for this tool. A retry that varies the sampling temperature or uses a disclosed second prompt lineage should be registered next time. |
| author's notes verbatim | (1) Re-read of the 17 records the seed-4242 re-authoring changed: 1 YES (20, omar budget_allocation: a real change of value), 16 the same failure in new words (13 paraphrase, 3 implausible). The 15 byte-identical records keep the first verdict by identity and were not re-read. (2) Outcome: 30 supersession and 1 retraction records fail after the frozen retry and fall to D-CF2-2 replacement. Supersession spares in walk order: 6 (positions 153-165); shortfall 24 before authoring losses. (3) Instrument note for the ledger and for CF-3: at temperature 0 an alternate seed changed 17 of 32 outputs and fixed 1; 'one frozen retry' is nearly a no-op for this tool. A retry that varies the sampling temperature or uses a disclosed second prompt lineage should be registered next time. (4) Method as before: records presented by a language model, verdicts typed by the author, disclosed under the AI-use line. |

## 2f. AUX-CF2-CONSTRUCTION — D-CF2-2 applied to the 31 records that fail the re-read (13 Sep 2026; `select_pairs.py --cf2 --exclude-batch`; `cf2/cf_pairs_cf2.json`; no store version built)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (D-CF2-2 batch) | **31 pairs excluded: PN read** — 30 supersession (queue positions 3, 10, 18, 28, 30, 32, 39, 40, 45, 46, 52, 56, 63, 66, 68, 73, 81, 85, 87, 103, 105, 110, 112, 116, 125, 127, 128, 135, 146, 150) and 1 retraction (alex:project_release_strategy `cf2:alex:project_release_strategy`, position 158); every one keeps its ELIGIBLE verdict (`eligibility_verdict_stands: true`) and carries the failing read (`AUX-CF2-PNREREAD`) in `meta.excluded`; their question rows and PN records moved to `meta.excluded_questions` / `meta.excluded_records` of their files, the questions sha256 recomputed over the 129 remaining. None of the 31 carried an overlap tag or O3 (`AUX-CF2-OVERLAP` unchanged: O1 7, O2 0, O3 15). |
| **AUX-CF2-CONSTRUCTION** (refill, walk order) | Each short state re-walked from position 1 under the cap and the one-per-name rule across states, using the freed cap slots and names. **Retraction: 1 replacement**, `cf2:nadia:project_pitch:spring_menu` (position 419, `lb_00470`, PROJECTS_ENDEAVORS, zero-overlap) for `cf2:alex:project_release_strategy`. **Supersession: 6 replacements — every ELIGIBLE spare in the 165 rows read** — `cf2:nadia:project_pitch:spring_menu` (pos 419) for `cf2:alex:project_release_strategy`; `cf2:callum:communication_style` (pos 154) for `cf2:aisha:career_progress`; `cf2:jake:habit:juul_use_intensity` (pos 157) for `cf2:aisha:emotional_state:family_expectations`; `cf2:david:reading_preferences_narrative_nonfiction` (pos 161) for `cf2:aisha:medication:ferrous_sulfate`; `cf2:aroha:personal_time_value` (pos 162) for `cf2:alex:company_stage`; `cf2:tom:vehicle_use` (pos 164) for `cf2:bruna:professional_style`; `cf2:mirri:learning_source:aunties_and_elders` (pos 165) for `cf2:chenoa:personal_commitment`; all zero-overlap, not O3. **Shortfall: 24 supersession pairs pending**; the supersession queue is extended from position 166 by a further adjudication read (`reviews/CF2_ADJUDICATION_READ_EXT.md`, §2g) rather than the quota dropping — the author's ruling of 13 Sep 2026. |
| **AUX-CF2-CONSTRUCTION** (state of the draw) | **136 pairs accepted: SUPERSESSION 76, RETRACTION 30, EXPIRY 30; pending {'SUPERSESSION': 24}**; 40 personas; cap 4 reached in supersession by kenji, marcus, thanh only. Last accepted queue position: expiry 44, retraction **419**, supersession **165** (all 106 ELIGIBLE rows of the 165 read are used: 76 accepted, 30 excluded). Supersession eligibility on the 165 read: 106 ELIGIBLE / 159 verdict reads = **0.667** (6 NOT-ADJUDICATED); PN authoring-and-read pass on the 100 first-drawn supersession records: 70 of 100 (69 first read + 1 re-read) = 0.70; the extension is sized at the author's 0.75. `meta.pending_draft` lists the 7 replacements awaiting their question and record. |
| accepted per persona (SUP / RET / EXP), after the batch | aisha 0/3/2, alex 2/0/0, amara 3/0/0, aroha 2/1/0, billy 1/1/1, bruna 2/1/0, callum 3/1/2, chenoa 0/1/0, dariush 0/0/3, david 1/0/2, diane 0/0/2, dmitri 2/1/0, elena 3/1/3, fatima 3/0/3, ingrid 2/1/0, jake 3/1/2, jerome 1/0/1, joonho 3/0/0, kenji 4/0/0, kofi 3/1/1, leila 2/1/0, lily 2/1/0, marcus 4/1/3, marley 1/2/2, mehmet 1/0/2, mirri 2/0/0, nadia 1/1/0, omar 2/1/0, pan 1/2/1, patrick 1/1/0, priya 2/2/0, raj 3/2/0, rosa 1/1/0, saga 1/1/0, samuel 1/0/0, thanh 4/0/0, tom 3/0/0, valentina 1/0/0, yoli 3/1/0, zara 2/0/0 |

## 2g. AUX-CF2-CONSTRUCTION — the 7 replacements drafted and authored; the supersession queue extended (13 Sep 2026; gpt-4.1-mini and text-embedding-3-small only; nothing on the Anthropic key)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (replacement questions) | `cf2_draft_questions.py --only` through the frozen renderer (sha `b748247b…`, seed 42): **7 questions, all first pick, 0 substitutions, 0 redrafts**, every one through the intent gate; **$0.0014**. `cf_questions_cf2.json` now **136 rows**, questions sha256 `27777fbdac37cb0eea323b93728abbb73d0e801654cb8465f6bfdc6c94ae8947`; cumulative drafting spend $0.0333. |
| **AUX-CF2-CONSTRUCTION** (replacement PN records) | `cf2_author_pn.py --only` through `author_pn.py` unchanged (sha `b6f53b1a…`, seed 42): **7 records, 0 retries**, every one clears MIN_DISCR 3 both sides (old side 5–9, new side 7–11) and detector 1.00 on the original; nadia's retraction cosine 0.726 (measured, not enforced); **$0.0012**. `cf_pn_texts_cf2.json` now **136 records** (106 authored, 30 anchor-only); cumulative authoring spend $0.0234. `meta.pending_draft` is empty. The 7 records and 7 questions await the author's read: `reviews/CF2_PN_READ_EXT.md` (Part A three-way, Part B value token). |
| **AUX-CF2-ADJUDICATION** (supersession extension, ruling of 13 Sep) | `select_pairs.py --cf2 --extend SUPERSESSION --n 55`: the seed-42 walk continued from **position 166 to 228** — **55 readable candidates** printed in `reviews/CF2_ADJUDICATION_READ_EXT.md` (criteria verbatim at top), **8 skipped** as unreadable under the current draw (kenji ×2, marcus ×2, thanh ×2 at the cap; kofi `project` and joonho `hobby` names already accepted). Sizing from the observed rates, not assumed: eligibility on positions 1–165 = **106 / 159 = 0.6667**; authoring-and-read pass **0.75** (the author's figure; the observed pass on the first 100 supersession records was 0.70); expected reads to fill 24 = **48.0**, marker printed at 48. Nothing accepted from the extension until the verdicts exist; `adjudication_queue.json` `meta.extensions` records the extension. |
| Spend today (13 Sep) | re-read merge $0; batch exclusion $0; questions $0.0014; PN $0.0012; extension $0 — **$0.0025**, OpenAI only. CF-2 OpenAI construction spend to date: questions $0.0333 + PN $0.0234 + re-authoring $0.0055 = **$0.0621** of the $22 line. |

## 2h. AUX-CF2-PNREAD, AUX-CF2-QUESTIONREAD, AUX-CF2-ADJUDICATION — the author's reads of 13 Sep 2026 (`cf2/cf2_ext_13sep.json`, sha256 `92608882d41fe0e1…`; PN and question rows merged by (state, persona, entry_id), adjudication rows by printed position, every row checked against `reviews/CF2_PN_READ_EXT.md` and `reviews/CF2_ADJUDICATION_READ_EXT.md`)

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** (replacements 131–137) | Three-way read of the 7 replacement records: **2 YES** (134 jake `habit:juul_use_intensity`, 137 nadia `project_pitch:spring_menu`), **3 NO-paraphrase** (131 aroha `personal_time_value`, 133 david `reading_preferences_narrative_nonfiction`, 135 mirri `learning_source:aunties_and_elders`), **2 NO-implausible** (132 callum `communication_style`, 136 tom `vehicle_use`). Disclosed by the author: the paraphrase/implausible letters were assigned by a language model from the author's bare NO; the YES/NO is the author's. The 5 NO go to D-CF2-3 (§2i). Cumulative first reads: 137 records — supersession 70 YES / 24 NO-paraphrase / 12 NO-implausible, retraction 30 YES / 1 NO-implausible (`cf2/pn_read_verdicts.json` `meta.counts`). |
| **AUX-CF2-QUESTIONREAD** (161–167) | Value-token read of the 7 replacement questions: **3 flagged** — 164 jake ("Juul"), 165 mirri ("aunties and elders"), 167 nadia ("spring menu pitch"); 161–163, 166 NO. Cumulative: **93 of 167** flagged. Disclosure, not a gate. |
| **AUX-CF2-ADJUDICATION** (supersession extension, positions 166–228) | The 55 readable candidates read: **27 ELIGIBLE, 27 INELIGIBLE, 1 rank-skip** (0212 pan `medication:antacid_gaviscon` behind 0172 `medication:omeprazole_dose`, ELIGIBLE); the 8 pre-skipped (cap/name) recorded as NOT-ADJUDICATED (`SKIP-CAP` 6, `SKIP-NAME` 2). **The author's note gives 26 ELIGIBLE / 28 INELIGIBLE; the per-row file governs** — both sum to 54 verdict reads; the row-level split is 27/27 and is what the walk uses. Supersession to date: **213 verdict reads, 133 ELIGIBLE, rate 0.6244** (extension alone 27/54 = 0.500, below the 0.667 the sizing assumed); stop at 228. |
| author's notes verbatim | (1) 13 Sep 2026: replacement records 131-137 read under the three-way question; 134 and 137 YES; 131/133/135 NO-paraphrase, 132/136 NO-implausible (letters assigned by the model from the author's NO, disclosed). Questions 161-167 flagged 164, 165, 167. Extension read positions 166-228: 26 ELIGIBLE, 28 INELIGIBLE, 1 rank-skip (0212 behind 0172), 8 pre-skipped by cap or name. Verdicts typed by the author; records presented by a language model; disclosed under the AI-use line. |

## 2i. AUX-CF2-PNREAD and AUX-CF2-CONSTRUCTION — D-CF2-3 on the 5 replacement NOs; the acceptance walk over positions 166–228 (13 Sep 2026; `cf2_reauthor_pn.py --only`, `select_pairs.py --cf2 --exclude-batch`)

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** (D-CF2-3, second round) | The 5 NO replacement records re-authored once at seed 4242 (`author_pn` unchanged, retries 0, $0.0008; `cf_pn_texts_cf2_reauthor_4242.json` now 37 records): **3 byte-identical** to the first attempt — 131 aroha `personal_time_value`, 132 callum `communication_style`, 135 mirri `learning_source:aunties_and_elders` — the NO **stands by identity without a re-read** (ruling of 13 Sep) and the pairs fall to D-CF2-2; **2 changed** — 133 david `reading_preferences_narrative_nonfiction`, 136 tom `vehicle_use` — join the next read (`reviews/CF2_PN_READ_EXT2.md` Part A); their first attempts stay in `cf_pn_texts_cf2.json` until a YES. Identity rate for the tool at temperature 0 across both rounds: **18 of 37**. |
| **AUX-CF2-CONSTRUCTION** (D-CF2-2, third batch) | 3 pairs excluded "PN read: NO stands by identity", verdicts standing (the excluded rows carry both reads); **pending rises to 27**; the supersession walk resumed at position 166 under the cap and the one-per-name rule: **26 replacements accepted, positions 166–226** (mehmet:shop_equipment_preference (166), priya:cognitive_style (167), dmitri:client_facing_name_usage (168), lily:healthcare_provider:gp (171), pan:medication:omeprazole_dose (172), elena:work_stress_carryover (175), fatima:health_care:physiotherapy (179), valentina:therapy_method (183), saga:health_observation:stress_correlation (188), yoli:profession_or_hobby:music_production (191), omar:value_system (192), bruna:breakfast_habit (193), callum:privacy_preference:health_condition (194), jake:preference:juul_flavor (197), chenoa:perspective:chronic_condition_management (200), aroha:health_habit:blood_sugar_monitoring (202), tom:preference:routine (204), mirri:work_vehicle_condition (205), mehmet:barbering_method_preference (206), priya:morning_routine (207), lily:health_management:eczema_cotton_gloves (211), raj:website_hosting_budget (222), valentina:hobby:history_podcasts (223), patrick:mental_health_care (224), kofi:health_condition:tiredness (225), jerome:health_condition:trauma_flashbacks (226)); all zero-overlap, none O3. **One ELIGIBLE row passed over: 0215 elena `mental_transition_routine` — elena reached the cap at 0175.** **Pending: 1 supersession pair** (for mirri `learning_source:aunties_and_elders`). |
| **AUX-CF2-CONSTRUCTION** (state of the draw) | **159 pairs accepted: SUPERSESSION 99, RETRACTION 30, EXPIRY 30; pending {'SUPERSESSION': 1}**; 40 personas; at the cap in supersession: elena, fatima, jake, kenji, kofi, lily, marcus, priya, raj, thanh, tom, yoli. Last accepted position: expiry 44, retraction 419, supersession **226**. 35 excluded in all (1 authoring predicate, 31 PN read after re-read, 3 PN read by identity), 3 of them former replacements (chains followed in `verify_cf2.py` check I). `meta.pending_draft`: the 26 new replacements, awaiting question and record (§2j). |
| accepted per persona (SUP / RET / EXP), after the walk | aisha 0/3/2, alex 2/0/0, amara 3/0/0, aroha 2/1/0, billy 1/1/1, bruna 3/1/0, callum 3/1/2, chenoa 1/1/0, dariush 0/0/3, david 1/0/2, diane 0/0/2, dmitri 3/1/0, elena 4/1/3, fatima 4/0/3, ingrid 2/1/0, jake 4/1/2, jerome 2/0/1, joonho 3/0/0, kenji 4/0/0, kofi 4/1/1, leila 2/1/0, lily 4/1/0, marcus 4/1/3, marley 1/2/2, mehmet 3/0/2, mirri 2/0/0, nadia 1/1/0, omar 3/1/0, pan 2/2/1, patrick 2/1/0, priya 4/2/0, raj 4/2/0, rosa 1/1/0, saga 2/1/0, samuel 1/0/0, thanh 4/0/0, tom 4/0/0, valentina 3/0/0, yoli 4/1/0, zara 2/0/0 |

## 2j. AUX-CF2-CONSTRUCTION and AUX-CF2-ADJUDICATION — the 26 replacements drafted and authored; the supersession queue extended a second time (13 Sep 2026; gpt-4.1-mini and text-embedding-3-small only; nothing on the Anthropic key)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (replacement questions, batch 2) | `cf2_draft_questions.py --only` × 26 through the frozen renderer (sha `b748247b…`, seed 42): **26 questions, all first pick, 0 substitutions, 0 redrafts**, all through the intent gate; **$0.0050**. `cf_questions_cf2.json` now **159 rows**, questions sha256 `afe3747d5f1e0894fa7c3a03941d4c61e12d09b32f0ab52cfa9c1bf9be053e70`; cumulative drafting spend $0.0383. |
| **AUX-CF2-CONSTRUCTION** (replacement PN records, batch 2) | `cf2_author_pn.py --only` × 26 through `author_pn.py` unchanged (sha `b6f53b1a…`, seed 42): **26 records, 0 retries, no predicate STOP**; n_discr old 5–16, new 7–16; detector 1.00 on every original; **$0.0043**. `cf_pn_texts_cf2.json` now **159 records** (129 authored: 99 supersession + 30 retraction; 30 anchor-only); cumulative authoring spend $0.0277. `meta.pending_draft` empty. |
| **AUX-CF2-ADJUDICATION** (supersession extension 2) | `select_pairs.py --cf2 --extend SUPERSESSION --n 30`: the walk continued from **position 229 to 272** — **30 readable candidates**, **14 skipped** (12 personas at the cap — elena, fatima, jake, kenji, kofi, lily, marcus, priya, raj, thanh, tom, yoli — and joonho `hobby` by name). Sizing: pending 1 + expected read failures **7.0** of the 28 records awaiting the author's read (26 first reads + 2 re-reads, at 1 − 0.75) = shortfall 8.0; eligibility observed **133 / 213 = 0.6244** (positions 1–228); expected reads **17.08**; 30 printed. **The cap now binds on 12 of 40 personas**: 14 of the 44 positions walked were unreadable. |
| Read file | `reviews/CF2_PN_READ_EXT2.md`: Part A the 26 records (138–163) + re-reads 35 (david `reading_preferences_narrative_nonfiction`) and 37 (tom `vehicle_use`); Part B the 26 questions (168–193); Part C = `reviews/CF2_ADJUDICATION_READ_EXT2.md` from its criteria heading, verbatim (positions 229–272). |
| Spend today (13 Sep, all steps) | re-read merge $0; batch exclusions $0; questions $0.0064; PN $0.0055; re-authoring $0.0008; extensions $0 — **$0.0128**, OpenAI only. CF-2 OpenAI construction spend to date: questions $0.0383 + PN $0.0277 + re-authoring $0.0063 = **$0.0723** of the $22 line. |

## 2k. AUX-CF2-PNREAD, AUX-CF2-QUESTIONREAD, AUX-CF2-ADJUDICATION — the author's third read (13 Sep 2026; `cf2/cf2_ext2_13sep.json`, sha256 `f6b5dd3d100bb1bf…`; PN and question rows merged by (state, persona, entry_id), adjudication rows by printed position; every row checked against `reviews/CF2_PN_READ_EXT2.md`)

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** (records 138–163) | Three-way read of the 26 batch-2 replacement records: **13 YES** (138, 139, 144, 145, 149, 152, 154, 155, 157, 158, 159, 161, 163), **13 NO** — 3 paraphrase (141 chenoa `perspective:chronic_condition_management`, 147 kofi `health_condition:tiredness`, 148 lily `health_management:eczema_cotton_gloves`), 10 implausible (140 callum, 142 dmitri, 143 elena, 146 jerome, 150 mehmet, 151 mehmet, 153 omar, 156 priya, 160 tom, 162 valentina). Letters model-assigned from the author's bare NO (disclosed). Pass rate on this batch **0.50**, against the 0.75 the sizing assumed and 0.70 / 0.29 on the two earlier batches. Cumulative first reads: 163 records — supersession 83 YES / 27 NO-paraphrase / 22 NO-implausible, retraction 30 YES / 1 NO-implausible. |
| **AUX-CF2-PNREREAD** (re-reads 35, 37) | david `reading_preferences_narrative_nonfiction` NO-paraphrase; tom `vehicle_use` NO-implausible — **both fail the re-read and fall to D-CF2-2**. Re-read tally across the run: 37 re-authored, 1 YES, 36 fail (18 by identity, 18 on re-read). |
| **AUX-CF2-QUESTIONREAD** (168–193) | **14 of 26 flagged** (168, 170, 174–179, 182, 184, 188, 189, 191, 192); cumulative **107 of 193**. Disclosure, not a gate. |
| **AUX-CF2-ADJUDICATION** (supersession extension 2, positions 229–272) | The 30 readable candidates: **13 ELIGIBLE, 17 INELIGIBLE**, no rank-skip; the 14 pre-skipped recorded (`SKIP-CAP` 13, `SKIP-NAME` 1). Note and rows agree. Supersession to date: **243 verdict reads, 146 ELIGIBLE, rate 0.6008** (extension 2 alone 13/30 = 0.433); stop at 272. |
| author's notes verbatim | (1) 13 Sep 2026, third read: records 138-163 and re-reads 35/37: 13 YES, 15 NO (4 paraphrase, 11 implausible; letters model-assigned from the author's bare NO, disclosed). Questions 168-193: 14 flagged. Extension 229-272: 13 ELIGIBLE, 17 INELIGIBLE of 30 readable. (2) Author's ruling: with 16 replacements needed (15 failures plus 1 pending) against 13 eligible in reserve and the persona cap binding on 12 of 40 personas, the supersession quota drops by the residual shortfall after the D-CF2-3 retry and the walk over 229-272, under a deviation stating the reason (authoring failure rate on attitude slots, cap saturation, queue thinning). No further extension. n remains above 470. (3) Method as before: records presented by a language model, verdicts typed by the author, disclosed. |

## 2l. AUX-CF2-PNREAD and AUX-CF2-CONSTRUCTION — D-CF2-3 third round; the last D-CF2-2 walk (positions 229–272); D-CF2-4 recorded (13 Sep 2026)

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** (D-CF2-3, third round) | The 13 first-read NOs of `CF2_PN_READ_EXT2.md` re-authored once at seed 4242 (`author_pn` unchanged, retries 0, $0.0021; `cf_pn_texts_cf2_reauthor_4242.json` now 50 records): **8 byte-identical** → NO stands by identity → excluded; **5 changed** → one last read (`CF2_PN_READ_EXT3.md`). The 2 re-reads (35 david, 37 tom) failed → excluded. Identity across the run: **26 of 50**; the retry has restored **1 record in 50**. |
| **AUX-CF2-CONSTRUCTION** (D-CF2-2, last walk) | 10 excluded (8 identity, 2 re-read), pending 11; the walk over 229–272 accepted **11 replacements, positions 230–263** (aisha:skill_development:soft_skills (230), omar:clothing_habit (232), bruna:marital_status (233), chenoa:health_belief:traditional healing (240), david:reading_volume (241), aroha:health_metric:fasting_blood_sugar (242), diane:favorite_scents_combination (243), mirri:health_condition:back_discomfort (245), pan:business_preference (252), leila:work_style_preference (261), valentina:job_attitude (263)); all zero-overlap, none O3. **Supersession 100, pending 0.** Beyond the fill point: 0264 patrick `communication_preference:trauma` (admissible, unused), 0272 omar `income_pattern` (omar at the cap). |
| **AUX-CF2-CONSTRUCTION** (D-CF2-4) | **Quota fixed at 100 / 30 / 30 (residual 0); no further extension.** From here a record failing its read is excluded with no replacement and N_sup drops by one. **16 records await a read** (11 new + 5 changed re-authors); at the last batch's pass 0.50 the expectation is N_sup ≈ 92, n ≈ 456; **if more than 10 of the 16 fail, n < 450 and the §14 power figures must be re-run** (D-CF2-4, §16). Replacements accepted in the run: **45**; excluded in all: **45** (1 authoring predicate, 33 read failures after the frozen retry, 11 NOs standing by identity), **13 of them former replacements** (chains followed in check I). |
| **AUX-CF2-CONSTRUCTION** (state of the draw) | **160 pairs accepted: SUPERSESSION 100, RETRACTION 30, EXPIRY 30**; 40 personas; at the cap in supersession: bruna, elena, fatima, jake, kenji, marcus, omar, priya, raj, thanh, yoli. Last accepted position: expiry 44, retraction 419, supersession **263**. Supersession queue read to 272: 243 verdict reads, 146 ELIGIBLE (rate 0.6008), of which 100 accepted, 43 excluded, 3 not drawn (0215 elena at the cap, 0264 patrick beyond the fill point, 0272 omar at the cap). `meta.pending_draft`: the 11 new replacements (§2m). |
| accepted per persona (SUP / RET / EXP) | aisha 1/3/2, alex 2/0/0, amara 3/0/0, aroha 3/1/0, billy 1/1/1, bruna 4/1/0, callum 2/1/2, chenoa 2/1/0, dariush 0/0/3, david 1/0/2, diane 1/0/2, dmitri 2/1/0, elena 4/1/3, fatima 4/0/3, ingrid 2/1/0, jake 4/1/2, jerome 2/0/1, joonho 3/0/0, kenji 4/0/0, kofi 3/1/1, leila 3/1/0, lily 3/1/0, marcus 4/1/3, marley 1/2/2, mehmet 1/0/2, mirri 3/0/0, nadia 1/1/0, omar 4/1/0, pan 3/2/1, patrick 2/1/0, priya 4/2/0, raj 4/2/0, rosa 1/1/0, saga 2/1/0, samuel 1/0/0, thanh 4/0/0, tom 2/0/0, valentina 3/0/0, yoli 4/1/0, zara 2/0/0 |

## 2m. AUX-CF2-CONSTRUCTION — the 11 replacements of the last walk drafted and authored; the last read file (13 Sep 2026; gpt-4.1-mini and text-embedding-3-small only; nothing on the Anthropic key)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (replacement questions, batch 3) | `cf2_draft_questions.py --only` × 11 (frozen renderer, seed 42): **11 questions, all first pick, 0 substitutions, 0 redrafts**, all through the intent gate; **$0.0021**. `cf_questions_cf2.json`: **160 rows**, questions sha256 `e20facf6e7fb44b53b2616f8c407c381c7a1b63a76d99f3521fb4c1a76ba0097`; cumulative $0.0404. |
| **AUX-CF2-CONSTRUCTION** (replacement PN records, batch 3) | `cf2_author_pn.py --only` × 11 (`author_pn.py` unchanged, seed 42): **11 records, 0 retries, no predicate STOP**; n_discr old 6–12, new 6–15; detector 1.00 on every original; **$0.0018**. `cf_pn_texts_cf2.json`: **160 records** (130 authored: 100 supersession + 30 retraction; 30 anchor-only); cumulative $0.0295. `meta.pending_draft` empty. |
| Read file | `reviews/CF2_PN_READ_EXT3.md`: Part A the 11 records (164–174) + re-reads 39 chenoa, 41 elena, 42 jerome, 47 omar, 48 priya (last reads); Part B the 11 questions (194–204); **no Part C** (D-CF2-4). A NO anywhere in the file excludes the pair with no replacement; N_sup ∈ [84, 100] after this read. |
| Spend today (13 Sep, all steps) | questions $0.0085; PN $0.0073; re-authoring $0.0029; merges, walks, extensions $0 — **$0.0187**, OpenAI only. CF-2 OpenAI construction spend to date: questions $0.0404 + PN $0.0295 + re-authoring $0.0084 = **$0.0783** of the $22 line. |

## 2n. AUX-CF2-PNREAD, AUX-CF2-PNREREAD, AUX-CF2-QUESTIONREAD — the author's final read (13 Sep 2026; `cf2/cf2_ext3_13sep.json`, sha256 `9bf72390f1793223…`; merged by (state, persona, entry_id), every row checked against `reviews/CF2_PN_READ_EXT3.md`)

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** (records 164–174) | **4 YES** (165 aroha `health_metric:fasting_blood_sugar`, 166 bruna `marital_status`, 168 david `reading_volume`, 174 valentina `job_attitude`), **7 NO** — 2 paraphrase (164 aisha `skill_development:soft_skills`, 167 chenoa `health_belief:traditional healing`), 5 implausible (169 diane, 170 leila, 171 mirri, 172 omar `clothing_habit`, 173 pan). Letters model-assigned from the author's bare NO (disclosed). Pass on this batch **0.36**. **Cumulative first reads, closed: 174 records — supersession 87 YES / 29 NO-paraphrase / 27 NO-implausible; retraction 30 YES / 1 NO-implausible** (`meta.counts`: {'RETRACTION|NO-implausible': 1, 'RETRACTION|YES': 30, 'SUPERSESSION|NO-implausible': 27, 'SUPERSESSION|NO-paraphrase': 29, 'SUPERSESSION|YES': 87}). |
| **AUX-CF2-PNREREAD** (re-reads 39, 41, 42, 47, 48) | All five NO (RE39 chenoa paraphrase; RE41 elena, RE42 jerome, RE47 omar `value_system`, RE48 priya implausible). **Re-read tally, closed: 50 re-authored at seed 4242 — 1 YES, 49 fail (26 by identity, 23 on re-read).** |
| **AUX-CF2-QUESTIONREAD** (194–204) | **4 of 11 flagged** (195, 197, 201, 202); **cumulative 111 of 204**. Disclosure, not a gate. |
| **Failures under D-CF2-4** | **12 of the 16 records awaiting a read failed** (7 first reads + 5 last re-reads) — above the 10 at which §16's conditional power re-run fires. Disposition in §2o. |
| **Construction telemetry, author's summary** (verbatim, note 3) | Construction telemetry across CF-2: PN read pass rate on supersession records 0.59 (first 100: 0.69; replacements: 0.42 to 0.50); the frozen seed-4242 retry restored 1 of 50; supersession eligibility 0.60 over 273 walked positions with the cap binding on 12 of 40 personas by position 272. |
| author's notes verbatim | (1) 13 Sep 2026, final read: records 164-174: 4 YES (165, 166, 168, 174), 7 NO; re-reads 39, 41, 42, 47, 48: all NO. Letters model-assigned from the author's bare NO (164, 167, RE39 paraphrase; the rest implausible), disclosed. Questions 194-204: 4 flagged. (2) Consequence under D-CF2-4: 12 failures; patrick 0264 fills one as the last spare (author's ruling); the supersession quota drops by the residual 11 to N_sup = 89, composition 89/30/30, n = 447. More than 10 of the 16 failed, so the conditional power re-run at the final composition fires before any store version; P1 below 0.80 is a STOP. (3) Construction telemetry across CF-2: PN read pass rate on supersession records 0.59 (first 100: 0.69; replacements: 0.42 to 0.50); the frozen seed-4242 retry restored 1 of 50; supersession eligibility 0.60 over 273 walked positions with the cap binding on 12 of 40 personas by position 272. (4) Method as before: entries presented by a language model, verdicts typed by the author, disclosed under the AI-use line. |

## 2o. AUX-CF2-CONSTRUCTION — D-CF2-4 applied to the 12 failures of the final read (13 Sep 2026; `select_pairs.py --cf2 --exclude-d4`; `cf_pairs_cf2.json` `meta.quota`, `meta.quota_history`)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (D-CF2-4 exclusions) | **12 pairs excluded with no replacement**, in walk order: priya:cognitive_style (167), elena:work_stress_carryover (175), omar:value_system (192), chenoa:perspective:chronic_condition_management (200), jerome:health_condition:trauma_flashbacks (226), aisha:skill_development:soft_skills (230), omar:clothing_habit (232), chenoa:health_belief:traditional healing (240), diane:favorite_scents_combination (243), mirri:health_condition:back_discomfort (245), pan:business_preference (252), leila:work_style_preference (261) — 7 first-read NOs (no retry: D-CF2-4 forecloses replacement) and 5 last-read NOs after the seed-4242 retry; every one keeps its ELIGIBLE verdict and carries both reads. Question rows and PN records moved to `meta.excluded_*`. **Quota now 88 / 30 / 30; accepted 88 / 30 / 30; n = 444.** |
| **AUX-CF2-CONSTRUCTION** (the spare — awaiting the author's ruling) | The author ruled "patrick 0264 is the one spare" on the report that 0264 was the only admissible ELIGIBLE row beyond the fill point. **The 12 exclusions freed two more:** elena (`work_stress_carryover` excluded → 3 in supersession) makes **0215 elena `mental_transition_routine` admissible — and it precedes 0264 in walk order**; omar (`value_system`, `clothing_habit` excluded → 2) makes **0272 omar `income_pattern`** admissible. Three admissible spares: 0215 elena, 0264 patrick, 0272 omar. Under D-CF2-2's walk-order rule one spare = 0215 elena; the author named patrick; taking all three would give N_sup = 91. **No spare drawn, nothing drafted, until the author rules**; `verify_cf2.py` check I lists 0215 as "admissible but undrawn under no-replacement". |
| **AUX-CF2-CONSTRUCTION** (state of the draw) | **148 pairs accepted: SUPERSESSION 88, RETRACTION 30, EXPIRY 30**; 40 personas; at the cap in supersession: bruna, fatima, jake, kenji, marcus, raj, thanh, yoli. Excluded in all: **57** (1 authoring predicate, 33 read failures after retry, 11 by identity, 12 under D-CF2-4), 25 of them former replacements. Reads closed: 174 first reads, 50 re-reads; `meta.pending_draft` empty; nothing awaits a read. |
| **Power** | §16 conditional fired (12 > 10 failures): the Phase 3 script re-run at 89/30/30 — **P1 0.994, P2 (Haiku) 1.000, P3 (Haiku) 1.000** (§3a). |

## 2p. AUX-CF2-CONSTRUCTION — the draw closed (13 Sep 2026; author's ruling: no spare)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (final) | **148 pairs: SUPERSESSION 88, RETRACTION 30, EXPIRY 30; composition 88 / 30 / 30; n = 444 items.** `meta.quota` 88/30/30, `meta.quota_history` closed with `final: true`. 40 personas; cluster unit persona. Undrawn ELIGIBLE rows, listed as the ruling requires: **0215 elena `mental_transition_routine`, 0264 patrick `communication_preference:trauma`, 0272 omar `income_pattern`** — admissible after the D-CF2-4 exclusions, not drawn (no spare). Supersession queue read to position 272: 243 verdict reads, 146 ELIGIBLE, of which 88 accepted, 55 excluded, 3 undrawn. Retraction: 30 of 35 ELIGIBLE accepted (last position 419); expiry: 30 (last position 44). |
| **AUX-CF2-OVERLAP** (final) | O1 7 (billy, david, elena, fatima, marcus, marley, mehmet expiry pairs), O2 0, O3 15 expiry pairs from the widened class; none of the 45 D-CF2-2 replacements carried a tag. |
| Reads closed | first reads 174 (supersession 87 YES / 29 paraphrase / 27 implausible; retraction 30 / 1), re-reads 50 (1 YES), question flags 111 of 204. PN read pass on supersession records, overall **87 / 143 = 0.61**. |
| Power | 89/30/30 run covers 88/30/30 within three items (§3a): P1 0.994, P2 1.000, P3 1.000. No re-run (ruling). |

## 3. AUX-CF2-POWER — the Phase 3 script at the registered and amended compositions

`reviews/CF2_SCOPE.md` Phase 3 script (md5 `a40d810f…`), per-state draw counts set to the
composition, 1,000 outer draws, seed 42, gate to 1e-9 passed on every run. Share of draws whose
item-level interval lower bound exceeds zero / excludes zero either side. Full grid tables in
`reviews/CF2_REG_REPORT.md` Step A; the 100/30/30 run added 2026-09-12 for D-CF2-1.

| Reading | 100/100/30 (n=690) | 100/100/60 (n=780) | 100/60/30 (n=570, frozen §3) | **100/30/30 (n=480, §14)** |
|---|---:|---:|---:|---:|
| P1 — mini whole cell v2 | 1.000 | 1.000 | 0.999 | **0.997** |
| P2 — Haiku 4.5 named − counted, v2 | 0.999 | 1.000 | 0.998 | **1.000** |
| P2 conditional — Opus 5 named − counted, v2 | 1.000 | 1.000 | 1.000 | 1.000 |
| P3 — Haiku 4.5 counted paired v3 − v2 | 1.000 | 1.000 | 1.000 | **1.000** |
| mini descriptive — supersession v2 | 0.990 | 0.993 | 0.998 | 0.995 |
| mini descriptive — retraction v2 | 0.902 | 0.887 | 0.517 | 0.107 |
| mini descriptive — expiry v2 | 0.055 | 0.241 | 0.047 | 0.044 |
| mini descriptive — named − counted v2 | 0.401 | 0.395 | 0.313 | 0.200 |
| mini descriptive — counted paired v3 − v2 | 1.000 | 1.000 | 0.993 | 0.828 |
| Haiku descriptive — retraction v2 / v3 | 0.858 / 1.000 | 0.848 / 1.000 | 0.378 / 1.000 | 0.044 / 0.885 |
| Opus descriptive — retraction v2 / v3 | 0.319 / 1.000 | 0.322 / 1.000 | 0.034 / 1.000 | 0.003 / 0.841 |

At 100/30/30 all three registered readings clear 0.80 (P1 0.997, P2 1.000, P3 1.000). What the
amendment gives up is confined to descriptive rows: mini's counted paired reading falls to 0.828
and every reader's retraction-v2 row is unpowered. Persona-clustered power is not simulated
(caveat 3 of the scope).

### 3a. AUX-CF2-POWER at 89/30/30 (n = 447) — the §16 conditional re-run, 13 Sep 2026

Fired because 12 of the 16 records awaiting a read failed (> 10). Same script (`cf2/power/power_sim_comp.py`, md5 `55ce5637…`, the Phase 3 script with the composition edit of `CF2_REG_REPORT.md` Step A), outer 1000 × inner 1000, seed 42; all three lanes reproduced the committed CF-1 item intervals to 1e-9 before drawing; outputs deposited in `cf2/power/out_*_89-30-30.jsonl` (elapsed MINI 127.7s, H45 128.1s, OP5 135.1s). Share of draws with the item-level 95% interval above zero:

| Reading | 89/30/30 (n=447) | 100/30/30 (n=480, §14) |
|---|---:|---:|
| P1 — mini whole cell v2 | **0.994** | see §3 |
| P2 — Haiku supersession − counted, v2 | **1.000** | see §3 |
| P3 — Haiku counted paired v3 − v2 | **1.000** | see §3 |
| P2 / P3 — Opus (conditional) | **1.000 / 1.000** | see §3 |
| mini descriptive — supersession v2 | **0.982** | see §3 |
| mini descriptive — retraction v2 | **0.103** | see §3 |
| mini descriptive — expiry v2 | **0.049** | see §3 |
| mini descriptive — named − counted v2 | **0.161** | see §3 |
| mini descriptive — counted paired v3 − v2 | **0.852** | see §3 |
| Haiku descriptive — retraction v2 / v3 | **0.044 / 0.903** | see §3 |
| Opus descriptive — retraction v2 / v3 | **0.000 / 0.847** | see §3 |

**P1 = 0.994 ≥ 0.80: the §16 conditional clears; P2 and P3 on Haiku 1.000.** Composition 89/30/30 assumes the one spare is accepted and passes its read; at 88/30/30 (n = 444) the reading would move by at most the three items and is not separately simulated — if the spare fails, the script is re-run at 88/30/30 before any store version. Persona-clustered power not simulated (scope caveat 3 stands). The 100/30/30 outputs are deposited beside these (`cf2/power/out_*_100-30-30.jsonl`).

## 4. Keys reserved and not yet written

`AUX-CF2-INDIVIDUATION`, `-INDEXSIZE`, `-V2R-DEF`, `-LEAKSCREEN-V3`,
`-LEAKSCREEN-V2R`, `-BLIND`, `-MINI-V2`, `-MINI-V3`, `-MINI-V2R`, `-H45-V2`, `-H45-V3`, `-H45-V2R`,
`-OP5-V2`, `-OP5-V3`, `-OP5-V2R`, `-PERSTATE`, `-COUNTED`, `-NAMEDVSCOUNTED`, `-EQUIV-V2R`,
`-NB6-V2`, `-ALLSTATES-V3`, `-NB5-V2`, `-FOK`, `-SPEND`, `-DROPRULE` (evaluated 2026-09-19).

## 5. CF2-BUILD-3 — the build (13 Sep 2026; `registrations/ADDENDUM_CF2.md` §2, §5; `cf2_build_cell.py`, `index_v2r.py`)

### 5a. AUX-CF2-V2R-DEF — written BEFORE any index exists

| Key | Value |
|---|---|
| **AUX-CF2-V2R-DEF** | `r82_counterfactual/index_v2r.py` (sha256 `ea4a7e4c1b196bf9…`) wraps the OUTPUT of `index_v2.render` (called upstream, never edited or copied) and rewrites **exactly two fields**: the `LIFECYCLE TOTALS` lines `  retracted             N` and `  expired               N`, located by label (asserted exactly one each), the label's 24-character prefix preserved. **Permutation:** the cell's (retracted, expired) pairs — one per store version, 444 — are permuted across versions by a **value-level derangement under seed 42**: positions grouped by value, shuffled within and across groups (`numpy.random.default_rng(42)`), laid out in a line and rotated by k drawn uniformly from [largest group, n − largest group]; a rotation in that band moves every position out of its own value group, so **no version keeps its own pair and every value keeps its multiplicity** (exists iff the largest group ≤ n/2; asserted). The realized k and the version→version map are recorded in `cf2/cf_indexes.json` `meta.v2r` at build. **Assertion (RENDERER LOCK, `index_v2r.assert_lock`):** same line count, every differing line is one of the two count lines, the labels unchanged — asserted per version at render and again by `verify_cf2.py` check E. **Disclosed:** the `PER-CATEGORY BREAKDOWN` keeps its RETRACT / EXPIRED columns, so a reader summing a column recovers the true totals; §5 names exactly two fields and that is what moves. |

### 5b. AUX-CF2-CONSTRUCTION (store versions), AUX-CF2-INDIVIDUATION, AUX-CF2-INDEXSIZE — build step 1 (`cf2_build_cell.py`, sha256 `f99c090196f0bc4f…`; no model call)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (store versions) | **444 items = 148 pairs × 3 versions (PRESENT / ABSENT / PN), composition 88 / 30 / 30; 148 PN positives**; every version returns its intended label under Definition 1 (assertion A: 444/444). Write path (B): 118 non-expiry PN versions append the successor on the same `slot_key` at confidence 0.9; the supersession branch fires where 0.9 clears the category threshold — 65 non-ACCUMULATE pairs (threshold 0.80, original deactivated, `supersedes` set) and **53 ACCUMULATE-category pairs where 0.9 < 0.95 and the branch does not fire** (both entries stay active, no pointer — a legitimate write-path outcome, recorded not forced, as CF-1); 30 expiry PN versions move the anchor to cutoff − 30 d (all strictly before cutoff) and append `status: expired`. Assertion C on the emitted text: 148/148 (retraction PN names on the v3 retracted list and off the v2 superseded list; expiry PN on the v3 expired list only; supersession PN on the superseded list). D (base leak / category ablation) and E (v3 extends v2 byte-identically): 444/444. `cf2/cf_cell.json`, `cf2/cf_indexes.json` (v2, v3), indexes sha256 `b423c34ed6b16c3d…`. **`meta.fails` = []**. |
| **AUX-CF2-INDIVIDUATION** | Draw-time predicates re-asserted at build: **148 / 148 pairs individuate** (scrubbed name absent from its own state's v3 section in PRESENT, present in PN) and **0 / 148 collide with the v2 superseded list in PRESENT** — no collision row prints; the pooled counted-state population is the full 60 pairs (30 retraction + 30 expiry, 180 items). |
| **AUX-CF2-INDEXSIZE** | v2: 58–69 lines, mean 4257.4 chars; v3: 64–75 lines, mean 4445.4 chars (V2R = v2's size by the lock). Entries per store version 223–623. |

### 5c. AUX-CF2-V2R-DEF (realized) — build step 2 (`cf2_build_cell.py --v2r`; no model call)

| Key | Value |
|---|---|
| **AUX-CF2-V2R-DEF** (realized permutation) | 444 store versions; **42 distinct (retracted, expired) pairs**, largest value group 47 (≤ 222, so a value-level derangement exists); rotation **k = 390** under seed 42; **0 versions keep their own pair; the multiset of pairs is preserved**; **444 of 444 V2R texts differ from their v2** (every version differs on at least one of the two lines by construction). RENDERER LOCK asserted on every version at render (`index_v2r.assert_lock`) and by `verify_cf2.py` check E: **every V2R differs from its v2 only on the two count lines**. `cf2/cf_indexes.json` `meta.arms` = [v2, v3, v2r]; `meta.v2r.permutation` is the version → source-version map; V2R sha256 `c2238bd6b90346d8…`. |

### 5d. AUX-CF2-LEAKSCREEN-V3, AUX-CF2-LEAKSCREEN-V2R — build step 3 (`cf2_leakscreen.py`; gpt-4.1-mini, served `gpt-4.1-mini-2025-04-14`; `cf2/results/leakscreen_cf2.json`)

ladder_e1's screen reproduced on the CF-2 cell: the 30 PRESENT items drawn by `random.Random(42).sample` from the 148 sorted by item_id, `prompts_e1` LEAKAGE prompts (file sha `337d37d3414c…`, texts sha `35d9b968ffc0…`), temperature 0, seed 42, max_tokens 200; scorer `supports_correct` against the pair's `entry_text`; a cell leaks iff more than 3 of 30 score correct.

| Key | Value |
|---|---|
| **AUX-CF2-LEAKSCREEN-V3** | **0 of 30 correct — PASS** (6 non-UNKNOWN answers, none matching the gold at the scorer's threshold; 0 parse failures). $0.0157. |
| **AUX-CF2-LEAKSCREEN-V2R** | **0 of 30 correct — PASS** (5 non-UNKNOWN, 0 parse failures). $0.0150. |
| v2 beside (not a registered screen) | 1 of 30 correct — PASS (cf2:jake:project:lake_trip_presidents_day_weekend|PRESENT: the answer "You have an entry related to a friend group lake trip under the RELATI" shares content tokens with the gold at the threshold; the index carries attribute names, so a name-shaped answer can overlap the stored value). $0.0150. |
| Spend | $0.0456, OpenAI; the 90 calls are the screen's, not a lane's. |

### 5e. The mini lane — build step 4 (`cf2_run.py` through `run_cf.py`; `cf2_score.py`; `cf2/rows/rows_MINI.jsonl`, `cf2/results/cf_scores_cf2.json`)

Probe (E1.7 rule): served `gpt-4.1-mini-2025-04-14`, identifier ok; blind 481 / v2 1684 / v3 1740 input tokens. Projection against §10 before launch: 1,480 calls, $0.99 expected, $1.29 at ×1.3 against the **$2** line — under. Run: BLIND 148 (one per question), INDEXED-V2 / -V3 / -V2R 444 each, k = 1, temperature 0, synchronous, `prompts_e1` digests asserted at import; **1,480 rows, 1,480 OK, 0 parse failures**; served `gpt-4.1-mini-2025-04-14` on every row. Estimators: item-level paired bootstrap primary, persona-clustered beside (cluster unit persona, 40 clusters), D.2 rule; tolerance 0.05.

| Key | Value |
|---|---|
| **AUX-CF2-BLIND** | 0.5000 on every lane and arm, by the §6 identity (one blind call per question, reused across its three versions). Printed, not suppressed. |
| **AUX-CF2-MINI-V2** | **0.7167** (blind 0.5000 by identity; Δ +0.2167); item [+0.1494, +0.2846]*, persona-clustered [+0.1663, +0.2649]* — agree; indexed persona-clustered [+0.6663, +0.7649]; 1000 draws each, seed 42 |
| **AUX-CF2-MINI-V3** | **0.7967** (blind 0.5000 by identity; Δ +0.2967); item [+0.2314, +0.3568]*, persona-clustered [+0.2438, +0.3478]* — agree; indexed persona-clustered [+0.7438, +0.8478]; 1000 draws each, seed 42 |
| **AUX-CF2-MINI-V2R** | **0.7179** (blind 0.5000 by identity; Δ +0.2179); item [+0.1479, +0.2857]*, persona-clustered [+0.1691, +0.2638]* — agree; indexed persona-clustered [+0.6691, +0.7638]; 1000 draws each, seed 42 |
| **AUX-CF2-H45-V2** | — Haiku 4.5 batch submitted (step 5), not yet collected; row fills when the lane is scored |
| **AUX-CF2-H45-V3** | — Haiku 4.5 batch submitted (step 5), not yet collected; row fills when the lane is scored |
| **AUX-CF2-H45-V2R** | — Haiku 4.5 batch submitted (step 5), not yet collected; row fills when the lane is scored |
| **AUX-CF2-OP5-V2** | — lane not run: the drop rule of §11 is evaluated on 2026-09-19, after the Haiku 4.5 lane is scored (AUX-CF2-DROPRULE) |
| **AUX-CF2-OP5-V3** | — lane not run: the drop rule of §11 is evaluated on 2026-09-19, after the Haiku 4.5 lane is scored (AUX-CF2-DROPRULE) |
| **AUX-CF2-OP5-V2R** | — lane not run: the drop rule of §11 is evaluated on 2026-09-19, after the Haiku 4.5 lane is scored (AUX-CF2-DROPRULE) |
| **AUX-CF2-PERSTATE** (mini, descriptive) | v2: EXPIRY (n 90, pos 30) indexed **0.5489**, paired item [-0.1022, +0.1893], persona [-0.0200, +0.1293]; RETRACTION (n 90, pos 30) indexed **0.5283**, paired item [-0.1204, +0.1577], persona [-0.0583, +0.1228]; SUPERSESSION (n 264, pos 88) indexed **0.8308**, paired item [+0.2480, +0.4070]*, persona [+0.2666, +0.3988]*. v3: EXPIRY (n 90, pos 30) indexed **0.5869**, paired item [-0.0524, +0.2230], persona [+0.0127, +0.1684]*; RETRACTION (n 90, pos 30) indexed **0.8725**, paired item [+0.2573, +0.4926]*, persona [+0.2971, +0.4307]*; SUPERSESSION (n 264, pos 88) indexed **0.8444**, paired item [+0.2610, +0.4256]*, persona [+0.2729, +0.4111]*. v2r: EXPIRY (n 90, pos 30) indexed **0.5144**, paired item [-0.1317, +0.1534], persona [-0.0576, +0.0840]; RETRACTION (n 90, pos 30) indexed **0.4950**, paired item [-0.1552, +0.1359], persona [-0.0775, +0.0788]; SUPERSESSION (n 264, pos 88) indexed **0.8500**, paired item [+0.2726, +0.4242]*, persona [+0.2886, +0.4147]*. Haiku / Opus rows: dash, as above. |
| **AUX-CF2-COUNTED** (mini, descriptive; P3's reading on the smallest reader) | Pooled counted states, 60 pairs / 180 items (all individuating by construction): v2 **0.5360** → v3 **0.7214**, paired Δ **+0.1854**, item [+0.1007, +0.2689]*, persona [+0.1000, +0.2734]*. Haiku 4.5 (the registered reader): dash, pending. |
| **AUX-CF2-NAMEDVSCOUNTED** (mini, descriptive; P2's reading on the smallest reader) | v2: named (supersession, 264 items) **0.8308** − counted (180 items) **0.5360** = **+0.2948**, two-subset interval [+0.1875, +0.3905]. v3: 0.8444 − 0.7214 = +0.1230, [+0.0204, +0.2210]. Haiku 4.5 (P2's reader): dash, pending. |
| **AUX-CF2-EQUIV-V2R** (mini; P5) | V2R − v2 on the whole cell: Δ **+0.0011**, item [-0.0282, +0.0297], persona [-0.0210, +0.0230] — **both inside [−0.05, +0.05]**. Haiku 4.5: dash, pending; Opus 5: dash (§11). |
| **AUX-CF2-NB6-V2** | Superseded-names matcher on v2 (all-MiniLM-L6-v2 max cosine, NB-6's estimator): **0.7663**, persona-clustered [+0.7226, +0.8051]; per state {'EXPIRY': 0.5, 'RETRACTION': 0.5, 'SUPERSESSION': 0.9223}. **Exceeds gpt-4.1-mini v2 (0.7167) by +0.0496 — within tolerance (P4), adverse branch prints.** |
| **AUX-CF2-ALLSTATES-V3** | All-states matcher over the three named sections of v3: **0.8756**, persona-clustered [+0.8391, +0.9111]; per state {'EXPIRY': 0.8711, 'RETRACTION': 0.7975, 'SUPERSESSION': 0.8995}. Exceeds gpt-4.1-mini on every arm and whole cell (adverse branch); P4's v3 comparison is against Haiku 4.5 — dash, pending. |
| **AUX-CF2-NB5-V2** | Whole-map matcher on v2: **0.5776**, persona-clustered [+0.5587, +0.5981]; per state {'EXPIRY': 0.5919, 'RETRACTION': 0.5758, 'SUPERSESSION': 0.5728}. Exceeds mini's counted-state rows under v2 / v2r (adverse branch). |
| **AUX-CF2-FOK** (descriptive only) | gpt-4.1-mini FOK AUROC against y_fok: v2 0.6357, v3 0.6436, v2r 0.6371. Not a registered reading. |
| **AUX-CF2-SPEND** (so far) | OpenAI, token-metered at list price from the rows (the dashboard's billed figure is not exposed by the API): mini lane **$0.9568** (2,246,659 in / 36,366 out tokens), probe ≈ $0.002, leakage screens $0.0456, construction $0.0783 → **$1.0828 of the $22 line**. Anthropic: $0 so far (Haiku batch submitted at step 5; its cost is metered at collection). |
| **AUX-CF2-DROPRULE** | — not yet evaluated: §11 fixes the evaluation to 2026-09-19, after the Haiku 4.5 lane is scored and ledgered; the Opus 5 batch is not created before then. |

**Mini verdicts (§8 texts, numbers filled):**

- **P1 — HOLDS.** On 148 questions written before any version of the store existed, and asked of three versions of the same store that differ in one attribute each, the smallest model's obligation judgment reaches 0.717 against the 0.5 a question-only reader attains here, with an interval of [+0.1494, +0.2846] (persona-clustered [+0.1663, +0.2649]). The gain survives where the question cannot carry the label.
- **P2** — Haiku 4.5: dash, pending. `gpt-4.1-mini` descriptive beside it: named − counted +0.295, two-subset [+0.1875, +0.3905] (carries no prediction, §7). Opus 5: dash (§11).
- **P3** — Haiku 4.5: dash, pending. `gpt-4.1-mini` descriptive: 0.536 → 0.721, paired +0.185, item [+0.1007, +0.2689], persona [+0.1000, +0.2734].
- **P4 (v2 half)** — On this cell the superseded-names lookup reaches 0.766 against the smallest reader's 0.717 under the superseded-only summary, within tolerance; the all-states lookup against Haiku 4.5 under the all-three-named summary prints when that lane is scored.
- **P5 (mini)** — Randomizing the retracted and expired counts in the superseded-only summary moves gpt-4.1-mini's whole-cell judgment by +0.001, intervals [-0.0282, +0.0297] (persona-clustered [-0.0210, +0.0230]), inside the tolerance band; on this cell that reader takes nothing from the counts; Haiku 4.5's row prints when that lane is scored.
- **Adverse branch (§8):** the superseded-names lookup exceeds the smallest reader on the whole cell under v2 (0.766 vs 0.717) and on supersession (0.922 vs 0.831); the all-states lookup exceeds it everywhere (0.876 whole cell); the whole-map lookup exceeds it on the counted states under v2 / v2r. Every flag is in `cf_scores_cf2.json` `flags` (22 rows) and prints in the table; no row is dropped.

### 5f. The Haiku 4.5 lane — build step 5, submitted (`cf2_run.py probe / project / submit`; `cf2/rows/batch_H45.json`)

| Key | Value |
|---|---|
| **AUX-CF2-H45-V2 / -V3 / -V2R** (submission record) | Probe (E1.7 rule, 3 calls): served **`claude-haiku-4-5-20251001`**, identifier ok; input tokens blind 525 / v2 1782 / v3 1845; output 39 / 200 / 200 (the indexed answers reach `max_tokens` 200 after the JSON object, which `last_json` parses — as CF-1). **Projection against §10 before submission: 7,400 calls, $8.91 expected, $11.58 at ×1.3 against the $16 line — under**; Anthropic total projected $8.91 of $121. **Batch `msgbatch_01Hu8kYryhnSkB8JqfcxsbhT`, 7400 requests** (BLIND 148 + 3 × 444 items, k = 5, temperature 0, `max_tokens` 200, Batch pricing ×0.5), submitted 2026-09-13; status at submission `in_progress`, 7,400 processing. Rows collect to `cf2/rows/rows_H45.jsonl` on `poll`; the three keys fill when the lane is scored. |
| **AUX-CF2-OP5-V2 / -V3 / -V2R** | Not submitted. The §11 drop rule is evaluated once, on 2026-09-19, after the Haiku 4.5 lane is scored and ledgered (`AUX-CF2-DROPRULE`); the Opus 5 probe is run then. |
| **AUX-CF2-SPEND** (Anthropic, at submission) | Probe 3 calls ≈ $0.006 (metered from tokens at list); batch cost metered at collection (expected $8.91). |

**STOP** at the end of step 5 (CF2-BUILD-3): the Haiku 4.5 batch is in flight; nothing else is submitted.

### 5g. The Haiku 4.5 lane, scored (`cf2_score.py`; `cf2/rows/rows_H45.jsonl`, `cf2/results/cf_scores_cf2.json`; 13 Sep 2026)

Batch `msgbatch_01Hu8kYryhnSkB8JqfcxsbhT` ended: **7,400 / 7,400 succeeded, 0 errored, 0 expired; every row parsed OK; 5 draws in each of the 1,480 (unit, arm) cells**; served `claude-haiku-4-5-20251001` on every row. P2's estimator is the registered two-subset difference bootstrap; the persona-clustered two-subset difference (personas drawn with replacement, both subsets moving together) prints beside it under the D.2 rule — it is not the registered estimator and is labelled so.

| Key | Value |
|---|---|
| **AUX-CF2-H45-V2** | **0.7566** (blind 0.5000 by identity; Δ +0.2566); item [+0.1942, +0.3189]*, persona-clustered [+0.2102, +0.3035]* — agree; indexed persona-clustered [+0.7102, +0.8035]; k = 5 collapsed by the X4 mean, 1000 draws, seed 42 |
| **AUX-CF2-H45-V3** | **0.8773** (blind 0.5000 by identity; Δ +0.3773); item [+0.3174, +0.4395]*, persona-clustered [+0.3362, +0.4124]* — agree; indexed persona-clustered [+0.8362, +0.9124]; k = 5 collapsed by the X4 mean, 1000 draws, seed 42 |
| **AUX-CF2-H45-V2R** | **0.7638** (blind 0.5000 by identity; Δ +0.2638); item [+0.2003, +0.3254]*, persona-clustered [+0.2193, +0.3071]* — agree; indexed persona-clustered [+0.7193, +0.8071]; k = 5 collapsed by the X4 mean, 1000 draws, seed 42 |
| **AUX-CF2-PERSTATE** (Haiku 4.5, descriptive) | v2: EXPIRY (n 90, pos 30) indexed **0.5794**, paired item [-0.0626, +0.2182], persona [+0.0234, +0.1457]*; RETRACTION (n 90, pos 30) indexed **0.5433**, paired item [-0.0799, +0.1701], persona [-0.0057, +0.0963]; SUPERSESSION (n 264, pos 88) indexed **0.8876**, paired item [+0.3072, +0.4676]*, persona [+0.3379, +0.4365]*. v3: EXPIRY (n 90, pos 30) indexed **0.8269**, paired item [+0.1935, +0.4675]*, persona [+0.2388, +0.4156]*; RETRACTION (n 90, pos 30) indexed **0.9042**, paired item [+0.2639, +0.5519]*, persona [+0.3524, +0.4545]*; SUPERSESSION (n 264, pos 88) indexed **0.8852**, paired item [+0.3050, +0.4634]*, persona [+0.3343, +0.4351]*. v2r: EXPIRY (n 90, pos 30) indexed **0.5847**, paired item [-0.0594, +0.2188], persona [+0.0351, +0.1414]*; RETRACTION (n 90, pos 30) indexed **0.5844**, paired item [-0.0564, +0.2279], persona [+0.0193, +0.1453]*; SUPERSESSION (n 264, pos 88) indexed **0.8874**, paired item [+0.3065, +0.4655]*, persona [+0.3382, +0.4339]*. |
| **AUX-CF2-COUNTED** (Haiku 4.5; **P3**) | Pooled counted states, 60 pairs / 180 items: v2 **0.5638** → v3 **0.8649**, paired Δ **+0.3010**, item [+0.2268, +0.3721]*, persona [+0.2247, +0.3591]* — both exclude zero, Δ clears tolerance: **P3 HOLDS**. |
| **AUX-CF2-NAMEDVSCOUNTED** (Haiku 4.5; **P2**) | v2: named (supersession, 264 items) **0.8876** − counted (180 items) **0.5638** = **+0.3237**, two-subset [+0.2319, +0.4011], persona-clustered [+0.2612, +0.3851] — both exclude zero, Δ clears tolerance: **P2 HOLDS**. v3 (descriptive): 0.8852 − 0.8649 = +0.0203, [-0.0570, +0.0907], persona [-0.0547, +0.0925] — naming the counted states closes the boundary. Opus 5: dash (§11). |
| **AUX-CF2-EQUIV-V2R** (Haiku 4.5; **P5**) | V2R − v2 on the whole cell: Δ **+0.0072**, item [-0.0079, +0.0229], persona [-0.0103, +0.0248] — **both inside [−0.05, +0.05]**; with mini's row (+0.0011) **P5: both readers inside the band**. Opus 5: dash (§11). |
| **AUX-CF2-ALLSTATES-V3** (P4's v3 half) | All-states lookup **0.8756** against Haiku 4.5 v3 **0.8773**: D = -0.0017, **within tolerance**, in the reader's favour by 0.0017. |
| **AUX-CF2-FOK** (Haiku 4.5, descriptive only) | v2 0.6168, v3 0.6133, v2r 0.6050. |
| **AUX-CF2-SPEND** (after the mini and Haiku lanes) | **Haiku 4.5 lane $9.0623** (Batch-priced from the returned tokens: 11,929,785 in / 1,238,972 out at $1.00 / $5.00 per M × 0.5) against the $16 line; probe ≈ $0.006. **Mini lane $0.9568** against $2. Lanes combined **$10.0192 of $18**. OpenAI to date $1.0828 of $22 (lane + probe + screens + construction); Anthropic to date $9.0683 of $130. |

**Verdicts with the Haiku lane (§8 texts):**

- **P1 — HOLDS** (mini, above).
- **P2 — HOLDS.** Under the summary that names only superseded content, Haiku 4.5's judgment on the named state exceeds its judgment on the two counted states by +0.324, interval [+0.2319, +0.4011] (persona-clustered [+0.2612, +0.3851]). `gpt-4.1-mini` descriptive beside it: +0.295, two-subset [+0.1875, +0.3905]. Opus 5: dash (§11).
- **P3 — HOLDS.** Naming retracted and expired content lifts Haiku 4.5's judgment on those states from 0.564 to 0.865 on the store-counterfactual set (60 questions), a paired gain of +0.301 with interval [+0.2268, +0.3721] (persona-clustered [+0.2247, +0.3591]). `gpt-4.1-mini` descriptive: 0.536 → 0.721, +0.185, item [+0.1007, +0.2689].
- **P4 — prints either way.** On this cell the superseded-names lookup reaches 0.766 against the smallest reader's 0.717 under the superseded-only summary, within tolerance, and the all-states lookup reaches 0.876 against Haiku 4.5's 0.877 under the all-three-named summary, within tolerance.
- **P5 — both inside the band.** Randomizing the retracted and expired counts in the superseded-only summary moves gpt-4.1-mini's whole-cell judgment by +0.001 and Haiku 4.5's by +0.007, intervals [-0.0282, +0.0297] (persona-clustered [-0.0210, +0.0230]) and [-0.0079, +0.0229] (persona-clustered [-0.0103, +0.0248]), both inside the tolerance band; on this cell neither reader takes anything from the counts. Opus 5: dash (§11).
- **Adverse branch (§8), Haiku rows:** 18 flags — the superseded-names lookup exceeds Haiku on the whole cell under v2 (0.766 vs 0.757) and v2r (0.766 vs 0.764) and on supersession under every arm (0.922 vs 0.885–0.888); the all-states lookup exceeds Haiku's v2 / v2r rows everywhere and its v3 row on supersession (0.900 vs 0.885) and expiry (0.871 vs 0.827); the whole-map lookup exceeds Haiku's counted-state rows under v2 (retraction 0.576 vs 0.543; expiry 0.592 vs 0.579) and v2r expiry. All 40 flags are in `cf_scores_cf2.json` `flags`; no row is dropped.

### 5h. AUX-CF2-DROPRULE — the §11 drop rule, evaluated 2026-09-13 by the author's ruling (D-CF2-5); `cf2/results/droprule_cf2.json`

| Key | Value |
|---|---|
| **AUX-CF2-DROPRULE** | Evaluated **once, on 2026-09-13** (the registration fixed 2026-09-19; the author moved the date forward after the Haiku lane was scored and ledgered — D-CF2-5; the once-only property is kept: this row is not re-evaluated on the 19th). **(i) Metered spend after the mini and Haiku 4.5 lanes: $0.9568 + $9.0623 = $10.0192 against their combined lines $2 + $16 = $18 — PASS.** **(ii) Opus 5 probe, three calls: served `claude-opus-5`, identifier ok; input tokens blind 693 / v2 2483 / v3 2595, output [144, 136, 134]; projection at k = 5, 7,400 calls, 17.298 M in / 1.021 M out, Batch ×0.5: $56.01, ×1.3 $72.81 against the $105 line — PASS**; Anthropic total (Haiku actual + Opus projected) $65.07, ×1.3 $84.59 against $121. **(iii) P2 and P5 name Opus 5 as a conditional branch (§7) — PASS.** **Verdict: the Opus 5 lane RUNS at k = 5** (§11: comparability with Tables 20 and 21). **Not submitted: STOP before submission on the author's instruction; the batch is created only on GO.** |

### 5i. The Opus 5 lane — submitted on the author's GO (13 Sep 2026; `cf2_run.py submit claude-opus-5`; `cf2/rows/batch_OP5.json`)

| Key | Value |
|---|---|
| **AUX-CF2-OP5-V2 / -V3 / -V2R** (submission record) | The §11 rule evaluated and ledgered first (`AUX-CF2-DROPRULE`, §5h: RUN). **Batch `msgbatch_014ADrDKGmyQuxCdzzrJjg6c`, 7,400 requests** (BLIND 148 + 3 × 444 items, **k = 5**, temperature unset, `max_tokens` 1024, Batch pricing ×0.5), submitted 2026-09-13 after the mini and Haiku 4.5 lanes were scored; status at submission `in_progress`, 7,400 processing. Projected $56.01 against the $105 line. The three keys fill when the lane is scored; P2 and P5's Opus branches print HELD / FAILED then. |

### 5j. The Opus 5 lane, scored (`cf2_score.py`; `cf2/rows/rows_OP5.jsonl`, `cf2/results/cf_scores_cf2.json`; 13 Sep 2026)

Batch `msgbatch_014ADrDKGmyQuxCdzzrJjg6c` ended: **7,400 / 7,400 succeeded**, 0 errored, 0 expired; **7,398 parsed OK, 2 PARSE_FAIL** (cf2:kofi:project:cocoa_farm_replanting_schedule|PRESENT INDEXED-V2R draw 1, cf2:kofi:project:cocoa_farm_replanting_schedule|PRESENT INDEXED-V2R draw 4 — one cell collapses on 3 draws, at MIN_DRAWS); served `claude-opus-5` on every row; temperature unset, `max_tokens` 1024, k = 5. Opus 5 carries the conditional branches of P2 and P5 only (§7); its other rows are descriptive.

| Key | Value |
|---|---|
| **AUX-CF2-OP5-V2** | **0.8405** (blind 0.5000 by identity; Δ +0.3405); item [+0.2882, +0.3913]*, persona-clustered [+0.2996, +0.3817]* — agree; indexed persona-clustered [+0.7996, +0.8817]; k = 5 collapsed by the X4 mean, 1000 draws, seed 42 |
| **AUX-CF2-OP5-V3** | **0.9079** (blind 0.5000 by identity; Δ +0.4079); item [+0.3508, +0.4628]*, persona-clustered [+0.3769, +0.4377]* — agree; indexed persona-clustered [+0.8769, +0.9377]; k = 5 collapsed by the X4 mean, 1000 draws, seed 42 |
| **AUX-CF2-OP5-V2R** | **0.8353** (blind 0.5000 by identity; Δ +0.3353); item [+0.2825, +0.3870]*, persona-clustered [+0.2937, +0.3768]* — agree; indexed persona-clustered [+0.7937, +0.8768]; k = 5 collapsed by the X4 mean, 1000 draws, seed 42 |
| **AUX-CF2-PERSTATE** (Opus 5, descriptive) | v2: EXPIRY (n 90, pos 30) indexed **0.6150**, paired item [+0.0077, +0.2282]*, persona [+0.0443, +0.2008]*; RETRACTION (n 90, pos 30) indexed **0.5872**, paired item [-0.0331, +0.2026], persona [+0.0427, +0.1581]*; SUPERSESSION (n 264, pos 88) indexed **0.9325**, paired item [+0.3598, +0.5068]*, persona [+0.3949, +0.4688]*. v3: EXPIRY (n 90, pos 30) indexed **0.9267**, paired item [+0.2974, +0.5637]*, persona [+0.3576, +0.4787]*; RETRACTION (n 90, pos 30) indexed **0.8100**, paired item [+0.1550, +0.4597]*, persona [+0.2245, +0.3922]*; SUPERSESSION (n 264, pos 88) indexed **0.9319**, paired item [+0.3584, +0.5079]*, persona [+0.3939, +0.4687]*. v2r: EXPIRY (n 90, pos 30) indexed **0.6092**, paired item [+0.0008, +0.2140]*, persona [+0.0401, +0.1985]*; RETRACTION (n 90, pos 30) indexed **0.5681**, paired item [-0.0548, +0.1820], persona [+0.0264, +0.1306]*; SUPERSESSION (n 264, pos 88) indexed **0.9322**, paired item [+0.3603, +0.5044]*, persona [+0.3934, +0.4690]*. |
| **AUX-CF2-COUNTED** (Opus 5, descriptive — P3 is Haiku's) | Pooled counted states, 60 pairs / 180 items: v2 **0.6030** → v3 **0.8536**, paired Δ **+0.2506**, item [+0.1784, +0.3349]*, persona [+0.1941, +0.3019]*. |
| **AUX-CF2-NAMEDVSCOUNTED** (Opus 5; **P2's conditional branch**) | v2: named **0.9325** − counted **0.6030** = **+0.3295**, two-subset [+0.2420, +0.4181], persona-clustered [+0.2556, +0.3875] — both exclude zero, Δ clears tolerance: **P2 (Opus 5) HELD**. v3 (descriptive): 0.9319 − 0.8536 = +0.0783, [+0.0140, +0.1443], persona [+0.0147, +0.1385] — a residual boundary survives naming on this reader (Haiku's closed to +0.020). |
| **AUX-CF2-EQUIV-V2R** (Opus 5; **P5's conditional branch**) | V2R − v2 on the whole cell: Δ **-0.0052**, item [-0.0130, +0.0026], persona [-0.0122, +0.0020] — **both inside [−0.05, +0.05]**: **P5 (Opus 5) inside the band**; all three readers inside. |
| **AUX-CF2-FOK** (Opus 5, descriptive only) | v2 0.6922, v3 0.7098, v2r 0.6894. |
| **AUX-CF2-SPEND** (final) | **Opus 5 lane $63.3783** (Batch-priced from the returned tokens: 16,831,465 in / 1,703,969 out at $5 / $25 per M × 0.5) against the **$105** line — under; the probe projected $56.01 (output ran 1.70 M tokens against 1.02 M projected). **Anthropic total: Haiku $9.0623 + Opus $63.3783 + probes ≈ $0.06 = $72.50 of $130** (ceiling line $121). **OpenAI total: $1.0828 of $22** (mini lane $0.9568, probe, screens $0.0456, construction $0.0783). Every figure is metered from the rows at list / Batch prices; the vendors' billed totals are not exposed by the APIs. |
| **AUX-CF2-DROPRULE** (closed) | Evaluated once on 2026-09-13 (D-CF2-5): RUN; lane submitted on the author's GO and scored the same day; actual $63.38 against the $105 line. |

**Opus 5 conditional branches (§8 texts):**

- **P2 (Opus 5) — HELD.** Under the summary that names only superseded content, Opus 5's judgment on the named state exceeds its judgment on the two counted states by +0.330, interval [+0.2420, +0.4181] (persona-clustered [+0.2556, +0.3875]).
- **P5 — all three readers inside the band.** Randomizing the retracted and expired counts in the superseded-only summary moves gpt-4.1-mini's whole-cell judgment by +0.001 and Haiku 4.5's by +0.007, intervals [-0.0282, +0.0297] (persona-clustered [-0.0210, +0.0230]) and [-0.0079, +0.0229] (persona-clustered [-0.0103, +0.0248]), both inside the tolerance band; on this cell neither reader takes anything from the counts. Opus 5, run under the §11 rule: -0.005, intervals [-0.0130, +0.0026] (persona-clustered [-0.0122, +0.0020]), inside the band.
- **Descriptive (no prediction):** Opus 5 whole cell v2 0.841, v3 0.908, v2r 0.835; counted states 0.603 → 0.854 (+0.251).
- **Adverse branch (§8), Opus rows:** 7 flags — the all-states lookup (0.876) exceeds Opus 5's v2 (0.841) and v2r (0.835) rows on the whole cell and on the counted states; the whole-map lookup edges Opus's v2r retraction row (0.576 vs 0.568). No baseline exceeds Opus 5 under v3 on any row, and none exceeds it on supersession. All 47 flags across the three readers are in `cf_scores_cf2.json` `flags`; no row is dropped.

### 5k. Derived margins for the manuscript (R98, 13 Sep 2026; differences of ledgered values, `cf_scores_cf2.json`)

Whole-cell rows where a lookup exceeds a reader (§8 adverse branch), lookup AUROC minus reader AUROC under the reader's summary; the lookups are scored once each on their own summary (superseded-names on v2 `AUX-CF2-NB6-V2` 0.7663, all-states on v3 `AUX-CF2-ALLSTATES-V3` 0.8756, whole-map on v2 `AUX-CF2-NB5-V2` 0.5776):

| Lookup | Reader, summary | lookup − reader (whole cell) | beyond ±0.05 |
|---|---|---:|---|
| superseded-names (v2) | Haiku 4.5, v2 | **+0.0097** | no |
| superseded-names (v2) | Haiku 4.5, v2r | **+0.0025** | no |
| superseded-names (v2) | GPT-4.1 mini, v2 | **+0.0496** | no |
| superseded-names (v2) | GPT-4.1 mini, v2r | **+0.0484** | no |
| all-states (v3) | Haiku 4.5, v2 | **+0.1190** | yes |
| all-states (v3) | Haiku 4.5, v2r | **+0.1118** | yes |
| all-states (v3) | Opus 5, v2 | **+0.0351** | no |
| all-states (v3) | Opus 5, v2r | **+0.0403** | no |
| all-states (v3) | GPT-4.1 mini, v2 | **+0.1589** | yes |
| all-states (v3) | GPT-4.1 mini, v3 | **+0.0789** | yes |
| all-states (v3) | GPT-4.1 mini, v2r | **+0.1577** | yes |

Per-state rows where a lookup exceeds a reader: superseded-names (v2) over Haiku 4.5 v2 supersession **+0.0347**; superseded-names (v2) over Haiku 4.5 v3 supersession **+0.0371**; superseded-names (v2) over Haiku 4.5 v2r supersession **+0.0349**; superseded-names (v2) over GPT-4.1 mini v2 supersession **+0.0915**; superseded-names (v2) over GPT-4.1 mini v3 supersession **+0.0779**; superseded-names (v2) over GPT-4.1 mini v2r supersession **+0.0723**; superseded-names (v2) over GPT-4.1 mini v2r retraction **+0.0050**; all-states (v3) over Haiku 4.5 v2 supersession **+0.0119**; all-states (v3) over Haiku 4.5 v2 retraction **+0.2542**; all-states (v3) over Haiku 4.5 v2 expiry **+0.2917**; all-states (v3) over Haiku 4.5 v3 supersession **+0.0143**; all-states (v3) over Haiku 4.5 v3 expiry **+0.0442**; all-states (v3) over Haiku 4.5 v2r supersession **+0.0121**; all-states (v3) over Haiku 4.5 v2r retraction **+0.2131**; all-states (v3) over Haiku 4.5 v2r expiry **+0.2864**; all-states (v3) over Opus 5 v2 retraction **+0.2103**; all-states (v3) over Opus 5 v2 expiry **+0.2561**; all-states (v3) over Opus 5 v2r retraction **+0.2294**; all-states (v3) over Opus 5 v2r expiry **+0.2619**; all-states (v3) over GPT-4.1 mini v2 supersession **+0.0687**; all-states (v3) over GPT-4.1 mini v2 retraction **+0.2692**; all-states (v3) over GPT-4.1 mini v2 expiry **+0.3222**; all-states (v3) over GPT-4.1 mini v3 supersession **+0.0551**; all-states (v3) over GPT-4.1 mini v3 expiry **+0.2842**; all-states (v3) over GPT-4.1 mini v2r supersession **+0.0495**; all-states (v3) over GPT-4.1 mini v2r retraction **+0.3025**; all-states (v3) over GPT-4.1 mini v2r expiry **+0.3567**; whole-map (v2) over Haiku 4.5 v2 retraction **+0.0325**; whole-map (v2) over Haiku 4.5 v2 expiry **+0.0125**; whole-map (v2) over Haiku 4.5 v2r expiry **+0.0072**; whole-map (v2) over Opus 5 v2r retraction **+0.0077**; whole-map (v2) over GPT-4.1 mini v2 retraction **+0.0475**; whole-map (v2) over GPT-4.1 mini v2 expiry **+0.0430**; whole-map (v2) over GPT-4.1 mini v3 expiry **+0.0050**; whole-map (v2) over GPT-4.1 mini v2r retraction **+0.0808**; whole-map (v2) over GPT-4.1 mini v2r expiry **+0.0775**.

Other derived figures printed: P4 margins **+0.0496** (superseded-names 0.7663 − GPT-4.1 mini v2 0.7167) and **−0.0017** (all-states 0.8756 − Haiku 4.5 v3 0.8773), both within ±0.05; counted-state pooled items **180** (60 pairs × 3), named-state items **264** (88 × 3); preregistered predictions across the registration record **47** (the manuscript's 42 + CF-2's 5), of which **8** did not hold (unchanged: CF-1's aggregate replication remains a failed registered prediction in its own row); questions asked of each summary **148**; PN read passes on the final draw's supersession records **87 of 88** authored first-read YES plus 1 D-CF2-3 YES — all 148 records in the cell passed the author's read (a construction fact, not a result).

Named-minus-counted, persona-clustered two-subset intervals not yet printed above (from `cf_scores_cf2.json` `two_subset_ci_persona`): GPT-4.1 mini v2 **[+0.2099, +0.3838]** (item-level two-subset [+0.1875, +0.3905], difference +0.2948, named 0.8308, counted 0.5360); GPT-4.1 mini v3 +0.1230, [+0.0204, +0.2210], persona [+0.0132, +0.2323]; Opus 5 v2r counted 0.5865, difference +0.3457, [+0.2528, +0.4411], persona [+0.2737, +0.4001]; GPT-4.1 mini v2r counted 0.5025, difference +0.3475, [+0.2496, +0.4425], persona [+0.2741, +0.4152]; Haiku 4.5 v2r counted 0.5847, difference +0.3026, [+0.2055, +0.3910], persona [+0.2453, +0.3669]. Whole-cell gains (AUROC − 0.5000) print at four decimals as the ledger's Δ values above (e.g. GPT-4.1 mini v2 +0.2167, Haiku 4.5 v3 +0.3773, Opus 5 v3 +0.4079).

Printed forms of the frozen §8 texts as they land in the manuscript (R98; placeholders filled at four decimals; the model identifier in the manuscript's name form), each on one line:

- P1 HOLDS [MAIN]: On $148$ questions written before any version of the store existed, and asked of three versions of the same store that differ in one attribute each, the smallest model's obligation judgment reaches $0.7167$ against the $0.5$ a question-only reader attains here, with an interval of $[+0.1494,+0.2846]$. The gain survives where the question cannot carry the label.
- P3 HOLDS [MAIN]: Naming retracted and expired content lifts Haiku 4.5's judgment on those states from $0.5638$ to $0.8649$ on the store-counterfactual set ($60$ questions), a paired gain of $+0.3010$ with interval $[+0.2268,+0.3721]$.

## 12. ADDENDUM_CF2_NAMES_COUNTS (E2, program R117): names against counts on the 444 (registered text sha256 `6cd4cb94c3a3a4dc...`, frozen at `177697a`; `tools/cf2_names_counts.py`, `tools/cf2_names_counts_score.py`; `rows/rows_MINI_nc.jsonl`, `rows/rows_H45_nc.jsonl`, `rows/batch_H45_nc.json`, `rows/lock_nc.json`, `build_nc.json`; `results/cf_scores_nc.json`; scored 2026-09-19)

### AUX-CF2-NC-LOCK, AUX-CF2-NC-TOKENS

Registration sha256 holds. Renderings, pure functions of the recorded v2 text, locks asserted on every version: `INDEXED-COUNTS` 1009.0 prompt tokens mean (max 1034), texts sha256 `1187e126d7671768...`; `INDEXED-NAMES` 1178.8 prompt tokens mean (max 1290), texts sha256 `d901ebefef3b1e6b...`; `INDEXED-NAMES-DASH` 1542.4 prompt tokens mean (max 1655), texts sha256 `f895e8817ef7ef25...`. D-NC-1: the registered lock wording (no digit outside the RECENCY block and the age sentence) is over-strict as written, because the name-block header reads max 15 per category and attribute names carry digits; the lock enforced is its intent: every kept line is a v2 line, byte-identical or with its overflow marker removed (the marker also when the 150-column wrap splits it), and no count line survives.

### AUX-CF2-NC-MINI-NAMES, -MINI-NAMES-DASH, -MINI-COUNTS, -H45-NAMES, -H45-COUNTS

| reader | arm | rows (not OK) | whole AUROC [persona CI] | minus recorded v2 (item; persona) | minus lookup (item; persona) | SUP | RET | EXP | distinct values |
|---|---|---|---|---|---|---|---|---|---:|
| gpt-4.1-mini | INDEXED-NAMES | 444 (0) | **0.7103** [0.6644, 0.7524] | -0.0064 ([-0.0484, +0.0338]; [-0.0439, +0.0290]) | -0.0560 ([-0.1007, -0.0146]; [-0.0913, -0.0226]) | 0.8564 | 0.5344 | 0.5006 | 11 |
| gpt-4.1-mini | INDEXED-COUNTS | 444 (0) | **0.5862** [0.5416, 0.6322] | -0.1306 ([-0.2025, -0.0524]; [-0.1835, -0.0801]) | -0.1802 ([-0.2494, -0.1097]; [-0.2301, -0.1319]) | 0.6107 | 0.6053 | 0.4933 | 9 |
| gpt-4.1-mini | INDEXED-NAMES-DASH | 444 (0) | **0.6891** [0.6371, 0.7356] | -0.0276 ([-0.0679, +0.0086]; [-0.0694, +0.0120]) | -0.0772 ([-0.1214, -0.0340]; [-0.1079, -0.0449]) | 0.8432 | 0.4500 | 0.4764 | 11 |
| gpt-4.1-mini | COUNTS minus NAMES | | | -0.1242 ([-0.1981, -0.0525]; [-0.1814, -0.0698]) | | | | | |
| gpt-4.1-mini | NAMES-DASH minus NAMES | | | -0.0212 ([-0.0538, +0.0106]; [-0.0531, +0.0104]) | | | | | |
| claude-haiku-4-5-20251001 | INDEXED-NAMES | 2220 (0) | **0.7507** [0.7114, 0.7891] | -0.0059 ([-0.0370, +0.0237]; [-0.0365, +0.0216]) | -0.0157 ([-0.0678, +0.0293]; [-0.0421, +0.0140]) | 0.9010 | 0.5631 | 0.5642 | 50 |
| claude-haiku-4-5-20251001 | INDEXED-COUNTS | 2220 (0) | **0.5945** [0.5514, 0.6460] | -0.1621 ([-0.2187, -0.1024]; [-0.1941, -0.1278]) | -0.1719 ([-0.2290, -0.1099]; [-0.2155, -0.1196]) | 0.6315 | 0.5553 | 0.5189 | 62 |
| claude-haiku-4-5-20251001 | COUNTS minus NAMES | | | -0.1562 ([-0.2175, -0.0889]; [-0.2007, -0.1126]) | | | | | |

### AUX-CF2-NC-PERSTATE (counts only on the counted states against the reader's recorded v2 row; P-N3, descriptive)

| reader | state | recorded v2 | counts only | difference (item; persona) | within tolerance |
|---|---|---|---|---|---|
| gpt-4.1-mini | RETRACTION | 0.5283 | 0.6053 | +0.0769 ([-0.0798, +0.2247]; [-0.0579, +0.1964]) | False |
| gpt-4.1-mini | EXPIRY | 0.5489 | 0.4933 | -0.0556 ([-0.2017, +0.0868]; [-0.1427, +0.0378]) | False |
| claude-haiku-4-5-20251001 | RETRACTION | 0.5433 | 0.5553 | +0.0119 ([-0.1052, +0.1390]; [-0.0679, +0.1038]) | True |
| claude-haiku-4-5-20251001 | EXPIRY | 0.5794 | 0.5189 | -0.0606 ([-0.2005, +0.0811]; [-0.1237, +0.0000]) | False |

Identity (disclosed at the freeze): under NAMES-ONLY the retraction and expiry PN and PRESENT versions are byte-identical, so PN versus PRESENT on those states is 0.5 by construction: gpt-4.1-mini {'RETRACTION': 0.5506, 'EXPIRY': 0.4844}; claude-haiku-4-5-20251001 {'RETRACTION': 0.5039, 'EXPIRY': 0.5161}.

### AUX-CF2-NC-P-N1

**P-N1 HOLDS: names only is within tolerance of the intact summary on the whole set for both readers (gpt-4.1-mini -0.0064; claude-haiku-4-5-20251001 -0.0059).**

### AUX-CF2-NC-P-N2

**P-N2 HOLDS: counts only is reliably below names only on the whole set for both readers (gpt-4.1-mini -0.1242 ([-0.1981, -0.0525]; [-0.1814, -0.0698]); claude-haiku-4-5-20251001 -0.1562 ([-0.2175, -0.0889]; [-0.2007, -0.1126])).**

### AUX-CF2-NC-SPEND

mini $0.7142 (1,332 calls), Haiku 4.5 $4.5454 (4,440 Batch calls), probes $0.0061, against the cap of $10.


### AUX-CF2-NC-IDENTITY (correction, computed after scoring; no call)

The freeze-time identity holds on 58 of the 60 counted-state pairs (28 of 30 retraction, 30 of 30 expiry): their NAMES-ONLY PN and PRESENT texts are byte-identical. Two retraction pairs differ in the RECENCY block (the retraction record shifts the median entry age), so PN versus PRESENT on the counted states is 0.5 by construction on the 58 tied pairs and moves with the two others; the observed values (GPT-4.1 mini 0.5506 / 0.4844, Haiku 4.5 0.5039 / 0.5161) are that, not a signal. The supersession pairs differ in the superseded-names list as intended (88 of 88).

## 13. ADDENDUM_CF2_OPENAI (E5, program R117): GPT-5.6 Luna and GPT-5.6 Sol on the 444 under the superseded-only summary (registered text sha256 `230df444e3d5f028...`, frozen at `177697a`; `tools/cf2_openai.py`; `rows/rows_LUNA.jsonl`, `rows/rows_SOL.jsonl`, `rows/lock_openai.json`, `rows/probes_openai.json`; `results/cf_scores_openai.json`; scored 2026-09-19)

### AUX-CF2-OAI-LOCK, AUX-CF2-OAI-PROBES

Registration sha256 holds; raw Chat Completions with the frozen `prompts_e1` texts and no other system text; reasoning effort and temperature unset, `max_completion_tokens` 2048 (the R74 X4 settings); draw-major per model, eight workers; the cap of $30 for both models. Probes (E1.7 rule): `gpt-5.6-luna` served `gpt-5.6-luna`, 1683 in / 192 out (162 reasoning, 1680 cache-write), $0.000651; `gpt-5.6-sol` served `gpt-5.6-sol`, 1683 in / 125 out (95 reasoning, 1680 cache-write), $0.010912.

### AUX-CF2-OAI-LUNA-V2, AUX-CF2-OAI-SOL-V2

| reader | k | rows (not OK) | whole AUROC [persona CI] | minus lookup (item; persona) | SUP | RET | EXP | counted pooled | distinct values | identical across draws / median range |
|---|---:|---|---|---|---|---|---|---|---:|---|
| gpt-5.6-luna | 5 | 2220 (1) | **0.8417** [0.7999, 0.8835] | +0.0754 ([+0.0339, +0.1216]; [+0.0450, +0.1090]) | 0.9426 | 0.5458 | 0.6167 | 0.5785 | 239 | 9 of 444 / 0.12 |
| gpt-5.6-sol | 5 | 2220 (0) | **0.8500** [0.8125, 0.8838] | +0.0836 ([+0.0401, +0.1315]; [+0.0544, +0.1163]) | 0.9383 | 0.5322 | 0.6403 | 0.5929 | 241 | 35 of 444 / 0.1 |

### AUX-CF2-OAI-PNPRESENT (the post-hoc block of POSTHOC_SPEC_R112, the same definitions)

| reader | scope | PN vs PRESENT [persona CI] | PN vs ABSENT | W/T/L | strict-win fraction [persona CI] |
|---|---|---|---|---|---|
| gpt-5.6-luna | whole | 0.8544 [0.8151, 0.8958] | 0.8291 | 129/2/17 | 0.8716 [0.8027, 0.9324] |
| gpt-5.6-luna | SUPERSESSION | 0.9474 [0.9116, 0.9782] | 0.9379 | 84/1/3 | 0.9545 [0.9069, 0.9894] |
| gpt-5.6-luna | RETRACTION | 0.5550 [0.4885, 0.6314] | 0.5367 | 19/1/10 | 0.6333 [0.4286, 0.8125] |
| gpt-5.6-luna | EXPIRY | 0.6633 [0.6067, 0.7634] | 0.5700 | 26/0/4 | 0.8667 [0.7586, 0.9677] |
| gpt-5.6-sol | whole | 0.8522 [0.8155, 0.8872] | 0.8477 | 126/2/20 | 0.8514 [0.8038, 0.8951] |
| gpt-5.6-sol | SUPERSESSION | 0.9426 [0.9110, 0.9738] | 0.9341 | 84/1/3 | 0.9545 [0.9140, 0.9889] |
| gpt-5.6-sol | RETRACTION | 0.5206 [0.4483, 0.5928] | 0.5439 | 17/1/12 | 0.5667 [0.3871, 0.7333] |
| gpt-5.6-sol | EXPIRY | 0.6572 [0.5789, 0.7511] | 0.6233 | 25/0/5 | 0.8333 [0.7000, 0.9394] |

### AUX-CF2-OAI-DRAWS (tokens per call, means over OK rows; the cache and reasoning columns X4 did not record)

| reader | prompt | completion | reasoning | cached | cache-write | usd per draw | cached share per draw |
|---|---:|---:|---:|---:|---:|---|---|
| gpt-5.6-luna | 1614.6174 | 191.6539 | 161.6539 | 1289.9072 | 321.7102 | {1: 0.2785, 2: 0.1167, 3: 0.1183, 4: 0.1156, 5: 0.1183} | {1: 0.0023, 2: 0.9981, 3: 0.9981, 4: 0.9981, 5: 0.9981} |
| gpt-5.6-sol | 1614.6104 | 153.7608 | 123.4973 | 1290.045 | 321.5653 | {1: 4.9475, 2: 1.6626, 3: 1.6429, 4: 1.6556, 5: 1.6599} | {1: 0.0023, 2: 0.9981, 3: 0.9981, 4: 0.9981, 5: 0.9981} |

### AUX-CF2-OAI-P-S1

**P-S1 HOLDS: GPT-5.6 Sol reads 0.8500 against the lookup's 0.7663, difference +0.0836 ([+0.0401, +0.1315]; [+0.0544, +0.1163]), both intervals excluding zero.**

### AUX-CF2-OAI-P-S2

**P-S2 FAILS: GPT-5.6 Luna exceeds the lookup reliably, +0.0754 ([+0.0339, +0.1216]; [+0.0450, +0.1090]).**

### AUX-CF2-OAI-SPEND

Token-metered from the rows at OpenAI's page prices of 2026-09-18 (input, cache-write at 1.25x, cached at the cached rate, output): Luna $0.7478, Sol $11.5686, both $12.3164, probes $0.0116, against the cap of $30; not an invoice.


## 14. ADDENDUM_CF2_INTENT_CROSSOVER (program R121): the same store under two intents (registration draft `reviews/r121/registrations_draft/ADDENDUM_CF2_INTENT_CROSSOVER.md`, NOT YET FROZEN; Phase 1 construction rows, 2026-09-19; `reviews/r121/tools/cross_questions.py`, `build_workbook_r121.py`, `ix_leakscreen.py`, `cue_list.py`, `prompts_p1.py`; gpt-4.1-mini only; nothing on the Anthropic key)

Phase 0 report `reviews/r121/PHASE0_REPORT.md` and the author's nine rulings of 2026-09-19 (design O2: Opus 5 one draw on every new cell; caps Anthropic 15 USD, OpenAI 4 USD; the recorded Opus draw 1 for the primary P0 reading; the cue list untuned; one workbook, two tabs; the leak screen on 30 of A and all of B; ledger and rows here).

| Key | Value |
|---|---|
| **AUX-CF2-IX-P1** | The P1 monitor prompt (`prompts_p1.py`): P0 with the negative-obligation block replaced, one worked example added and "Two" → "Three worked examples." (ruling 2); system-text sha256 `c3c9a8e2b9798b50aa5a8f091f382b550e296f973f0c9af09d7fa38442cc7ce4` (2590 chars) against P0's `f60fee2aeb9f3fdd…` (2081 chars); the module asserts the construction at import. |
| **AUX-CF2-IX-CUES** | The keyword-intent lookup's cue list (`cue_list.py`, sha256 `bf063a8eb9830a78b9a0d061714aa1736e287fe63a8d6805336396735cf39d4f`): 30 patterns (12 frozen PAST markers of `intent.py`, 10 CHANGE, 8 PAST), proposed from the instruction texts before any question existed and kept untuned (ruling 4). **On the 148 recorded original questions 2 fire**: `cf2:kofi:preparation_for_meeting` (`\bbefore\b`: "What tasks are scheduled for me to complete before the coming meeting?"); `cf2:valentina:hobby:history_podcasts` (`\bhistory\b`: "Which history podcast episodes have I been following recently?"). **On the crossed questions the coverage is complete**: seed 42 A 88 of 88, B 30 of 30; seed 4242 A 88 of 88, B 30 of 30 (the renderer's instruction offers the cue wordings and the model used them on every question), so the keyword-intent lookup zeroes every crossed question and coincides with the oracle-intent lookup on cells 3 and 4; see the Phase 1 report for the consequence for P-I4. |
| **AUX-CF2-IX-QUESTIONS** | `reviews/r121/build/cross_questions.json`: **118 pairs** (A 88 supersession → CHANGE, B 30 expiry → PAST; retraction out of scope), renderer prompt sha256 `5c15f5ba3ecf27eed22e315de031b6ae766b81d104ac67e413b04d28c82fd81d`, model `gpt-4.1-mini` served `gpt-4.1-mini-2025-04-14`, temperature 0, seeds 42 (primary) and 4242 (fallback), max_tokens 200, one question per call, both seeds drafted for every pair (236 calls). Prompt saw entity, slot attribute path, crossed time-sense; never entry text or value, category, the original question, any store content, any label. Automatic gate (G1 no frozen future marker, G2 not identical to the original, G3 non-empty): **primary failures 0, fallback failures 0**. **Fallback byte-identical to the primary: 98 of 118** (temperature 0; the CF-2 record saw 15 of 32), so the second seed offers a different question on 20 pairs only. Questions sha256 seed 42 `8be56a563fc977f54c123bd69ada74d071f6df0a9e3e401eade84ab356bd5b37`, seed 4242 `024c65d0990b54447e33bb799e86b1f08f2249dfd61df1ec3050e8d018961a8e`. First-person voice 44 of 118 (the recorded originals: 141 of 160). Tokens 92852 in / 3958 out; **$0.0435**. |
| **AUX-CF2-IX-CHECK** (as built) | `reviews/r121/build/AUTHOR_CHECK_R121.xlsx`, **sha256 as built `e2e6de67bbbaf619e492da5232446aa3857ac496b0620a511efc3bf784b5bdce`** (2026-09-19T12:14:35); tabs `seed42` (all 118 rows, four YES/NO columns and Notes), `seed4242` (consulted only for rows failed on `seed42`, said at its top; 98 rows marked IDENTICAL with their verdict cells locked), `CRITERIA`; 2979 locked cells hashed in `build/workbook_lock_r121.json`. The returned workbook's sha256 and the verdict counts fill this row at Phase 2. Not yet sent. |
| **AUX-CF2-IX-LEAK** | `results/leakscreen_ix.json` (`ix_leakscreen.py`; cf2_leakscreen's protocol; `prompts_e1` file sha `337d37d3414c…`, texts sha `35d9b968ffc0…`; served `gpt-4.1-mini-2025-04-14`): **A_fallback** 0 of 4 correct, 0 non-UNKNOWN, 0 parse failures, **0 of 4 correct (cover)**; **A_primary** 0 of 30 correct, 0 non-UNKNOWN, 0 parse failures, **PASS**; **B_fallback** 0 of 5 correct, 0 non-UNKNOWN, 0 parse failures, **0 of 5 correct (cover)**; **B_primary** 0 of 30 correct, 1 non-UNKNOWN, 0 parse failures, **PASS**. Registered cells A (seed-42 questions, 30 PRESENT versions by seed 42 under v2) and B (all 30 PRESENT versions under v3) both PASS; the fallback cover cells screen the differing seed-4242 questions in the samples. $0.0341. |
| **AUX-CF2-IX-SPEND** (Phase 1) | OpenAI, token-metered at list price: drafting $0.0435 + leak screen $0.0341 = **$0.0776** of the 4 USD cap; Anthropic $0. Not an invoice. |

### 14b. Phase 1b — the author's three rulings on `reviews/r121/PHASE1_REPORT.md` (2026-09-19): P-I4 demoted to descriptive (the cue list identifies the intent of every crossed question by construction; a registered descriptive row adds each model under P1 beside the keyword-intent lookup on the pooled estimand); a registered second lineage replaces the temperature-0 fallback; a cue-free population is an open item for the rebuttal period, not an experiment here. Rows below from `cross_questions.py draft2`, `ix_leakscreen.py --lineage2`, `build_workbook_r121.py`.

| Key | Value |
|---|---|
| **AUX-CF2-IX-QUESTIONS** (lineage 2) | The registered second lineage: the same instruction and model (`gpt-4.1-mini`, served `gpt-4.1-mini-2025-04-14`, system fingerprints `fp_0beb2287bb`, `fp_f58ab5bba3`), **temperature 0.7, seed 4242**, one question per pair, 118 calls; lineage sha256 `3fd41897587ce1d7c082027939f6169bba1edc584645d8781a37311b505c574e` (the renderer's seven fields with the temperature 0.7); questions sha256 `79fe7994e2d304e1294dbd461b9befca503a057c5140c014f09fb93c2a0b339a`. Gate failures **0**. **Byte-identical to the seed-42 primary: 64 of 118** (A 48 of 88, B 16 of 30; the temperature-0 fallback it supersedes was identical on 98), so the fallback offers a different question on 54 pairs; a failed primary with an identical fallback is a drop by rule. Cue coverage of the lineage: A 88 of 88, B 30 of 30 (cue-bearing on purpose; the population stays homogeneous). The superseded temperature-0 rows stay in `cross_questions.json` as `fallback_t0_superseded`. Tokens 46426 in / 2029 out; **$0.0218**. |
| **AUX-CF2-IX-CHECK** (rebuilt) | `reviews/r121/build/AUTHOR_CHECK_R121.xlsx` **rebuilt: sha256 as built `b21445f6b6d8b7fc0c1b204187d69f539677cd5f48d173871127edfdc5de4cd4`** (2026-09-19T12:34:15); the earlier build (`e2e6de67…`, 98 IDENTICAL rows greyed) is superseded and not sent. Tab `seed4242` now carries lineage 2 for all 118 rows, no greying, the header kept (consult only for rows failed on `seed42`); 2587 locked cells hashed in `build/workbook_lock_r121.json`. The returned workbook's sha256, the verdict counts, the rows that used the second seed and the drops fill this row at Phase 2. |
| **AUX-CF2-IX-LEAK** (lineage 2) | `results/leakscreen_ix.json` (`--lineage2`): the registered cells carried unchanged from the first run (**A_primary 0 of 30, PASS; B_primary 0 of 30, PASS**); the lineage-2 cover cells on the sampled items whose fallback differs from the primary: **A_fallback** 0 of 16 correct, 2 non-UNKNOWN, 0 parse failures; **B_fallback** 0 of 14 correct, 0 non-UNKNOWN, 0 parse failures. The temperature-0 cover cells (A_fallback 0 of 4, B_fallback 0 of 5) moved to `cells_superseded`. $0.0446 this file ($0.0491 with the superseded cells). |
| **AUX-CF2-IX-SPEND** (Phase 1, cumulative) | OpenAI, token-metered at list price: drafting $0.0435 + lineage 2 $0.0218 + leak screens $0.0491 = **$0.1143** of the 4 USD cap; Anthropic $0. Not an invoice. |

### 14c. Phase 1c — deviation **D-IX-1** (`reviews/r121/DEVIATIONS_R121.md`, 2026-09-19): the crossed-question instruction amended after the author's check of the version-1 workbook found, before any verdict and before any monitor call, that about half the questions were second-person or addressed the persona by name (A 41 of 88 "your"; B 26 of 30 not first person), every population-B question asked how the event went, and several population-A questions invented a time window. Version 2 requires the first person, forbids "your", names and invented windows, and asks B what the event was or when it took place; the gate gained G4–G6; the cue list was re-derived from the amended text before any generation; both lineages regenerated; the superseded material kept in `reviews/r121/build/superseded/` and `results/leakscreen_ix_v1_superseded.json`. Sections 14 and 14b stand as the version-1 record.

| Key | Value |
|---|---|
| **AUX-CF2-IX-INSTRUCTION** (v2) | Instruction version 2 (`cross_questions.py` `SYSTEM`): **prompt sha256 `ee92835120c2f76891e02cdbde2fadc8976bc1258d1fcfca7aa8d20d31b809f9`; lineage-2 sha256 `090d796e05ff5bc215809cca560aef89135407c699bf3541e72871546b48ee92`**; version 1 (`SYSTEM_V1`, kept) `5c15f5ba3ecf27eed22e315de031b6ae766b81d104ac67e413b04d28c82fd81d` / `3fd41897587ce1d7c082027939f6169bba1edc584645d8781a37311b505c574e`, reproduced from the kept text. Gate G4 (second person), G5 (persona-name token), G6 (time-window phrase; `TIME_WINDOW`, 8 patterns) added to G1–G3. |
| **AUX-CF2-IX-CUES** (v2) | `cue_list.py` version 2, **sha256 `a63461d09d5c60c44009c05b004657394a854ab10d468f80bf9377625f8fb9a8`**, 26 cues (12 frozen PAST markers, 10 CHANGE, 4 PAST: `\bhappened?\b`, `\bwhen was\b`, `\bwhat was\b`, `\b(have|had) planned\b`), re-derived from the version-2 instruction before any version-2 question existed; version 1 (`bf063a8eb9830a78…`) reproduces from the module. On the 148 recorded original questions 3 fire: `cf2:kofi:preparation_for_meeting` (`\bbefore\b`); `cf2:rosa:project:colada_taste_test` (`\b(have|had) planned\b`); `cf2:valentina:hobby:history_podcasts` (`\bhistory\b`) (rosa's is a retraction pair, outside the populations). Coverage of the version-2 crossed questions: primary A 88 of 88, B 29 of 30; lineage 2 A 88 of 88, B 28 of 30. |
| **AUX-CF2-IX-QUESTIONS** (v2) | `reviews/r121/build/cross_questions.json` (instruction version 2): **primary** seed 42, temperature 0, served `gpt-4.1-mini-2025-04-14`, fingerprints `fp_2a126b9d98`, `fp_6f31bfbb14`, `fp_a2374ad346`, `fp_eb9b0343ec`, questions sha256 `efa8eeee63db25674d68a1e1067cdc5d3e9ea837d2ce2c8f68d063ba5dee195e`, gate rejected 1 (G1 1, G2 0, G3 0, G4 0, G5 0, G6 0), tokens 54450 in / 1878 out, $0.0248; **lineage 2** seed 4242, temperature 0.7, fingerprints `fp_2a126b9d98`, `fp_6f31bfbb14`, `fp_8f74a54150`, `fp_a2374ad346`, `fp_eb9b0343ec`, questions sha256 `c488db0c316d8bd7f5f8deeb1f459cf3ef65fd6aa4c8ad7357cdadaf6bf1128b`, gate rejected 1 (G1 1, G2 0, G3 0, G4 0, G5 0, G6 0), **byte-identical to the primary on 90 of 118**, $0.0248. Rejections: primary `cf2:elena:event:wedding_timeline`; lineage 2 `cf2:aisha:upcoming_meeting` (both G1, "scheduled"). First person 118 of 118 (primary) and 118 of 118 (lineage 2); second person 0 and 0. |
| **AUX-CF2-IX-CHECK** (v2, as built; the reduced design) | `reviews/r121/build/AUTHOR_CHECK_R121.xlsx` **sha256 as built `47292556696c2911cb7441cb183f2ae55008a480d730d4580d020f039568575c`** (2026-09-19T12:55:20); the version-1 builds (`e2e6de67…`, `b21445f6…`) superseded, never judged, kept in `build/superseded/`. Reduced design: modal template of A `How has my … changed over time?` (85 of 88); checked set 53 = B 30 + off-template A 3 (`cf2:kenji:health_condition_cause:insomnia`, `cf2:raj:work_safety_equipment:FFP3_mask`, `cf2:thanh:communication_preference:old_times`) + a seeded 20 of the conforming A (seed 42); reserve 65 conforming A rows, checked in full only if a sampled row fails. Tabs `seed42`, `seed4242`, `reserve_seed42`, `reserve_seed4242`, `CRITERIA`; the AI-assisted line at the top of every tab ("This check is AI-assisted: the rows were prepared by a language model. Every verdict is the author's."); 2633 locked cells hashed in `build/workbook_lock_r121.json`. The returned workbook's sha256, verdict counts, second-seed rows and drops fill this row at Phase 2. |
| **AUX-CF2-IX-LEAK** (v2) | `results/leakscreen_ix.json` (served `gpt-4.1-mini-2025-04-14`): **A_fallback** 0 of 5 correct, 0 non-UNKNOWN, 0 parse failures, **0 of 5 correct (cover)**; **A_primary** 0 of 30 correct, 1 non-UNKNOWN, 0 parse failures, **PASS**; **B_fallback** 0 of 15 correct, 2 non-UNKNOWN, 0 parse failures, **0 of 15 correct (cover)**; **B_primary** 0 of 30 correct, 5 non-UNKNOWN, 0 parse failures, **PASS**. Registered cells A (v2 summary) and B (v3 summary) both PASS. $0.0405. The version-1 screen kept as `results/leakscreen_ix_v1_superseded.json`. |
| **AUX-CF2-IX-SPEND** (Phase 1, cumulative) | OpenAI, token-metered at list price: version 1 (drafting $0.0435 + lineage 2 $0.0218 + screens $0.0491) $0.1144 + version 2 (primary $0.0248 + lineage 2 $0.0248 + screen $0.0405) $0.0900 = **$0.2044** of the 4 USD cap; Anthropic $0. Not an invoice. |

### 14d-interim — the author's interim read (2026-09-19T14:09:30): `ix_interim.py` scored the three completed lanes (MINI, H45, LUNA) and the offline lookups while the Opus 5 batch `msgbatch_0113JM6ujusorRXbgGrU53hT` was still in progress; the registration was frozen and no analysis choice was open, so the read could influence nothing. Written to `results/cf_scores_ix_interim_3lanes.json`; the Opus lane untouched; the full scoring (§14d) follows when it ends.

### 14d-interim-2 — the author's second interim read (2026-09-19T14:32:43): the Sol lane alone (Amendment 1) scored with `ix_score`'s functions while the Opus 5 batch `msgbatch_0113JM6ujusorRXbgGrU53hT` was still in progress; the registration and the amendment frozen and no analysis choice open, so the read could influence nothing. Written to `results/cf_scores_ix_interim_sol.json`; the Opus lane untouched; the full five-lane scoring (§14d) follows when it ends.

### 14d-interim-3 — descriptive, offline, no call (2026-09-19T14:35:16): the one-draw analogue (draw 1 alone in every cell) for GPT-5.6 Luna and Haiku 4.5 beside their five-draw means, and the eleven population-A pairs GPT-5.6 Sol loses under P1 (`results/cf_scores_ix_interim_draw1.json`); the Opus 5 batch still in progress.

### 14d-interim-3, the author's correction (2026-09-19T14:41:09): of GPT-5.6 Sol's eleven population-A losses under P1 (within-pair counts 76/0/11), nine have both questions scored 0.96 or higher. A CHANGE question licenses the old value, so a correct reading is low: those nine are failures to apply the intent rule, not ceiling ties (the session's first reading, withdrawn); they are not reversals, because the two scores are nearly equal, but they are intent errors. The held text and the appendix say so in those words. The draw-1 rows of §14d-interim-3 are accepted as the comparable column for the five-model table: both columns print in the appendix, and the body uses the one-draw column wherever Sol or Opus 5 appears beside the others.

### 14d. Phase 2 — the run and the scores (registered text sha256 `9480d6bbcfef47d2…`, frozen at `648d671`; `reviews/r121/tools/ix_run.py`, `ix_score.py`; `rows/rows_IX_MINI.jsonl`, `rows_IX_LUNA.jsonl`, `rows_IX_H45.jsonl`, `rows_IX_OP5.jsonl`, `rows/lock_ix.json`, `rows/probes_ix.json`, `rows/batch_IX_H45.json`, `batch_IX_OP5.json`; `results/cf_scores_ix.json`; scored 2026-09-19)

### AUX-CF2-IX-LOCK, AUX-CF2-IX-PROBES

Registration sha256 holds; P0 digests, P1 sha256 `c3c9a8e2b9798b50…`, cue list `a63461d09d5c60c4…`, questions `efa8eeee63db2567…` / `c488db0c316d8bd7…`, returned workbook `be79963e0a328761…` asserted at start; 113 pairs, 904 units of the design, new units per lane {"H45": 678, "LUNA": 730, "MINI": 678, "OP5": 678}. Probes (E1.7 rule): `MINI` served `gpt-4.1-mini-2025-04-14`, P0 1742 / P1 1858 in, out [21, 21], $0.001507; `H45` served `claude-haiku-4-5-20251001`, P0 1845 / P1 1969 in, out [39, 200], $0.005009; `LUNA` served `gpt-5.6-luna`, P0 1744 / P1 1857 in, out [173, 135], $0.001270; `OP5` served `claude-opus-5`, P0 2596 / P1 2743 in, out [354, 150], $0.039295; `SOL` served `gpt-5.6-sol`, P0 1744 / P1 1857 in, out [81, 164], $0.022899.

### AUX-CF2-IX-CENSUS

| lane | rows | not OK | units | draws per unit | identical across draws | median range | usd |
|---|---:|---:|---:|---|---:|---|---:|
| MINI | 678 | 0 | 678 | {'1': 678} | 0 | None | $0.4876 |
| H45 | 3390 | 0 | 678 | {'5': 678} | 533 | 0.0 | $4.7303 |
| LUNA | 3650 | 0 | 730 | {'5': 730} | 43 | 0.05 | $1.1479 |
| OP5 | 678 | 0 | 678 | {'1': 678} | 0 | None | $6.1912 |
| SOL | 730 | 0 | 730 | {'1': 730} | 0 | None | $8.1237 |

### AUX-CF2-IX-<READER>-<A|B>-<P0|P1> — the primary and secondary estimands (same-store AUROC of cell 1 against cell 3 with the persona-grouped then the pair-clustered interval, W/T/L; the interaction mean with both intervals; the pooled AUROC of cell 1 against cells 2 to 4 with both intervals)

| reader | pop | arm | same-store AUROC [persona] [pair] · W/T/L | interaction | pooled | cells 1 vs 2 |
|---|---|---|---|---|---|---|
| GPT-4.1 mini | A | P0 | **0.3973** [0.3447, 0.4455] [0.3460, 0.4426] · 16/26/45 | -0.0695 [-0.1149, -0.0268] [-0.1161, -0.0276] | 0.6821 [0.6367, 0.7236] [0.6424, 0.7256] | 0.8240 |
| GPT-4.1 mini | A | P1 | **0.4789** [0.4169, 0.5413] [0.4261, 0.5279] · 22/34/31 | -0.0259 [-0.0899, 0.0300] [-0.0822, 0.0242] | 0.7275 [0.6698, 0.7809] [0.6830, 0.7699] | 0.8456 |
| GPT-4.1 mini | B | P0 | **0.3388** [0.2385, 0.4297] [0.2411, 0.4157] · 0/13/13 | -0.1058 [-0.1655, -0.0444] [-0.1731, -0.0365] | 0.4497 [0.3469, 0.5405] [0.3612, 0.5360] | 0.5459 |
| GPT-4.1 mini | B | P1 | **0.4238** [0.3264, 0.5236] [0.3262, 0.5297] · 7/5/14 | -0.0538 [-0.1340, 0.0310] [-0.1635, 0.0520] | 0.6146 [0.5101, 0.7219] [0.5118, 0.7205] | 0.7175 |
| Haiku 4.5 | A | P0 | **0.3765** [0.3183, 0.4257] [0.3239, 0.4203] · 18/16/53 | -0.0218 [-0.0683, 0.0204] [-0.0609, 0.0160] | 0.7035 [0.6593, 0.7406] [0.6620, 0.7401] | 0.8835 |
| Haiku 4.5 (draw 1 only, the comparable column) | A | P0 | **0.3872** [0.3302, 0.4367] [0.3350, 0.4318] · 16/22/49 | -0.0195 [-0.0634, 0.0223] [-0.0609, 0.0209] | 0.7028 [0.6578, 0.7427] [0.6611, 0.7399] | 0.8802 |
| Haiku 4.5 | A | P1 | **0.5483** [0.4793, 0.6135] [0.4819, 0.6152] · 42/10/35 | -0.0456 [-0.1046, 0.0202] [-0.1005, 0.0130] | 0.7572 [0.6992, 0.8094] [0.7090, 0.8093] | 0.8377 |
| Haiku 4.5 (draw 1 only, the comparable column) | A | P1 | **0.5464** [0.4770, 0.6073] [0.4792, 0.6115] · 37/16/34 | -0.0438 [-0.1043, 0.0252] [-0.1047, 0.0185] | 0.7549 [0.6986, 0.8067] [0.7042, 0.8067] | 0.8376 |
| Haiku 4.5 | B | P0 | **0.4238** [0.3179, 0.5136] [0.3461, 0.5022] · 8/2/16 | -0.0592 [-0.1406, 0.0427] [-0.1252, 0.0197] | 0.7064 [0.6278, 0.7725] [0.6376, 0.7695] | 0.8476 |
| Haiku 4.5 (draw 1 only, the comparable column) | B | P0 | **0.4120** [0.3202, 0.4863] [0.3395, 0.4712] · 4/6/16 | -0.0504 [-0.1284, 0.0447] [-0.1289, 0.0392] | 0.6970 [0.6280, 0.7520] [0.6328, 0.7562] | 0.8462 |
| Haiku 4.5 | B | P1 | **0.5333** [0.4437, 0.6206] [0.4378, 0.6331] · 13/5/8 | -0.0255 [-0.1114, 0.0539] [-0.1024, 0.0403] | 0.7470 [0.6891, 0.8183] [0.6800, 0.8200] | 0.8543 |
| Haiku 4.5 (draw 1 only, the comparable column) | B | P1 | **0.5377** [0.4442, 0.6278] [0.4393, 0.6442] · 12/6/8 | -0.0250 [-0.1229, 0.0622] [-0.1073, 0.0439] | 0.7465 [0.6744, 0.8221] [0.6716, 0.8237] | 0.8513 |
| GPT-5.6 Luna | A | P0 | **0.3467** [0.2944, 0.3847] [0.2994, 0.3827] · 10/1/76 | -0.0626 [-0.0957, -0.0290] [-0.1014, -0.0211] | 0.7460 [0.7179, 0.7659] [0.7211, 0.7661] | 0.9466 |
| GPT-5.6 Luna (draw 1 only, the comparable column) | A | P0 | **0.3484** [0.3121, 0.3773] [0.3027, 0.3876] · 15/8/64 | -0.0963 [-0.1389, -0.0544] [-0.1509, -0.0454] | 0.7317 [0.7018, 0.7577] [0.7009, 0.7592] | 0.9149 |
| GPT-5.6 Luna | A | P1 | **0.9836** [0.9558, 1.0000] [0.9564, 1.0000] · 85/0/2 | +0.6098 [0.5405, 0.6829] [0.5413, 0.6778] | 0.9714 [0.9464, 0.9894] [0.9477, 0.9900] | 0.9446 |
| GPT-5.6 Luna (draw 1 only, the comparable column) | A | P1 | **0.9640** [0.9238, 0.9935] [0.9252, 0.9940] · 82/2/3 | +0.5997 [0.5233, 0.6751] [0.5291, 0.6704] | 0.9523 [0.9189, 0.9816] [0.9174, 0.9815] | 0.9238 |
| GPT-5.6 Luna | B | P0 | **0.4172** [0.3497, 0.4664] [0.3328, 0.4786] · 8/0/18 | -0.0825 [-0.1464, -0.0281] [-0.1309, -0.0369] | 0.7690 [0.7215, 0.8063] [0.7234, 0.8060] | 0.9364 |
| GPT-5.6 Luna (draw 1 only, the comparable column) | B | P0 | **0.4800** [0.4058, 0.5608] [0.3972, 0.5703] · 13/2/11 | -0.0500 [-0.1297, 0.0208] [-0.1165, 0.0142] | 0.7840 [0.7248, 0.8386] [0.7283, 0.8351] | 0.9260 |
| GPT-5.6 Luna | B | P1 | **0.9793** [0.9401, 1.0000] [0.9356, 1.0000] · 26/0/0 | +0.4975 [0.3965, 0.6067] [0.3810, 0.6120] | 0.9588 [0.9049, 0.9968] [0.9016, 0.9961] | 0.9135 |
| GPT-5.6 Luna (draw 1 only, the comparable column) | B | P1 | **0.9808** [0.9424, 1.0000] [0.9423, 1.0000] · 26/0/0 | +0.5192 [0.4327, 0.6150] [0.4023, 0.6282] | 0.9608 [0.9137, 0.9945] [0.9073, 0.9956] | 0.9231 |
| Opus 5 | A | P0 | **0.8966** [0.8471, 0.9477] [0.8428, 0.9453] · 78/3/6 | +0.2208 [0.1588, 0.2880] [0.1648, 0.2784] | 0.9342 [0.9042, 0.9667] [0.9011, 0.9667] | 0.9322 |
| Opus 5 | A | P1 | **0.9885** [0.9634, 1.0000] [0.9655, 1.0000] · 86/0/1 | +0.4437 [0.3834, 0.5009] [0.3934, 0.4976] | 0.9672 [0.9424, 0.9881] [0.9392, 0.9880] | 0.9247 |
| Opus 5 (sensitivity: recorded five-draw means for cells 1, 2) | A | P0 | **0.9008** [0.8540, 0.9473] [0.8516, 0.9477] · 78/0/9 | +0.2128 [0.1498, 0.2825] [0.1563, 0.2698] | 0.9365 [0.9071, 0.9666] [0.9045, 0.9668] | 0.9320 |
| Opus 5 | B | P0 | **0.8484** [0.7434, 0.9407] [0.7559, 0.9334] · 23/0/3 | -0.0127 [-0.0743, 0.0540] [-0.0762, 0.0515] | 0.9241 [0.8729, 0.9705] [0.8752, 0.9692] | 0.9305 |
| Opus 5 | B | P1 | **1.0000** [1.0000, 1.0000] [1.0000, 1.0000] · 26/0/0 | +0.2508 [0.1770, 0.3271] [0.1892, 0.3108] | 0.9753 [0.9524, 0.9943] [0.9544, 0.9929] | 0.9260 |
| Opus 5 (sensitivity: recorded five-draw means for cells 1, 2) | B | P0 | **0.8410** [0.7263, 0.9394] [0.7389, 0.9298] · 23/0/3 | -0.0082 [-0.0704, 0.0608] [-0.0733, 0.0568] | 0.9223 [0.8647, 0.9729] [0.8703, 0.9685] | 0.9349 |
| GPT-5.6 Sol (Amendment 1) | A | P0 | **0.4406** [0.3798, 0.5042] [0.3853, 0.4934] · 15/32/40 | -0.1197 [-0.1828, -0.0559] [-0.1910, -0.0473] | 0.7731 [0.7475, 0.7969] [0.7440, 0.7989] | 0.9213 |
| GPT-5.6 Sol (Amendment 1) | A | P1 | **0.8815** [0.8200, 0.9349] [0.8131, 0.9449] · 76/0/11 | +0.5205 [0.4153, 0.6366] [0.4146, 0.6375] | 0.9226 [0.8973, 0.9477] [0.8942, 0.9501] | 0.9036 |
| GPT-5.6 Sol (Amendment 1) (sensitivity: recorded five-draw means for cells 1, 2) | A | P0 | **0.4060** [0.3445, 0.4638] [0.3496, 0.4609] · 18/18/51 | -0.1059 [-0.1661, -0.0487] [-0.1731, -0.0374] | 0.7683 [0.7412, 0.7935] [0.7403, 0.7934] | 0.9414 |
| GPT-5.6 Sol (Amendment 1) | B | P0 | **0.6354** [0.5261, 0.7378] [0.5318, 0.7478] · 15/4/7 | +0.0465 [-0.1434, 0.2313] [-0.1231, 0.2185] | 0.8378 [0.7921, 0.8771] [0.7909, 0.8846] | 0.9209 |
| GPT-5.6 Sol (Amendment 1) | B | P1 | **0.9179** [0.7917, 1.0000] [0.8077, 1.0000] · 23/0/3 | +0.4050 [0.2065, 0.5793] [0.2500, 0.5477] | 0.9475 [0.8985, 0.9879] [0.8994, 0.9872] | 0.9283 |

GPT-5.6 Sol on population A under P1, within-pair counts 76/0/11: of its 11 losses, **9 have both questions scored 0.96 or higher**; a CHANGE question licenses the old value, so a correct reading is low, and those pairs are failures to apply the intent rule (the author's reading, 14d-interim-3). Pairs: `cf2:alex:work_preference` (0.97 / 1.00); `cf2:amara:habit:desk_posture` (0.03 / 0.06); `cf2:bruna:breakfast_habit` (0.99 / 1.00); `cf2:callum:family_member:fiona_hobby_running` (0.48 / 1.00); `cf2:elena:decompression_method:phone_scrolling` (0.96 / 1.00); `cf2:jake:health_belief_vaping_vs_smoking` (0.99 / 1.00); `cf2:marcus:health_monitoring:blood sugar check` (0.96 / 1.00); `cf2:mirri:work_vehicle_condition` (0.99 / 1.00); `cf2:omar:budget_allocation` (0.99 / 1.00); `cf2:saga:health_management_method` (0.96 / 1.00); `cf2:thanh:sleep_schedule` (0.99 / 1.00).

### AUX-CF2-IX-LOOKUPS (no model call; the name lookup, the keyword-intent lookup, the oracle-intent lookup; the cue share by cell; the question-length difference of ruling 8)

| lookup | pop | same-store AUROC [persona] [pair] · W/T/L | interaction | pooled |
|---|---|---|---|---|
| name | A | **0.4739** [0.4413, 0.5079] [0.4336, 0.5143] · 46/0/41 | -0.0435 [-0.0650, -0.0204] [-0.0737, -0.0148] | 0.7770 [0.7481, 0.8036] [0.7491, 0.8045] |
| keyword | A | **0.9943** [0.9817, 1.0000] [0.9828, 1.0000] · 86/1/0 | +0.4041 [0.3405, 0.4736] [0.3476, 0.4642] | 0.9679 [0.9489, 0.9837] [0.9505, 0.9840] |
| oracle | A | **1.0000** [1.0000, 1.0000] [1.0000, 1.0000] · 87/0/0 | +0.4047 [0.3406, 0.4742] [0.3486, 0.4645] | 0.9735 [0.9593, 0.9855] [0.9614, 0.9850] |
| name | B | **0.4527** [0.3888, 0.4912] [0.3905, 0.5015] · 10/0/16 | -0.0528 [-0.0822, -0.0290] [-0.0854, -0.0241] | 0.7567 [0.7156, 0.7961] [0.7078, 0.7991] |
| keyword | B | **0.9460** [0.8535, 1.0000] [0.8654, 1.0000] · 25/1/0 | +0.2561 [0.1848, 0.3352] [0.1806, 0.3348] | 0.9290 [0.8651, 0.9729] [0.8718, 0.9751] |
| oracle | B | **1.0000** [1.0000, 1.0000] [1.0000, 1.0000] · 26/0/0 | +0.2973 [0.2312, 0.3820] [0.2184, 0.3761] | 0.9662 [0.9438, 0.9918] [0.9401, 0.9899] |

Population A: cue share by cell {"1": 0.0115, "2": 0.0115, "3": 1.0, "4": 1.0}; crossed minus original question length **+0.97 content tokens** (original 7.08, crossed 8.05) and -0.8 characters on average.

Population B: cue share by cell {"1": 0.0385, "2": 0.0385, "3": 0.9615, "4": 0.9615}; crossed minus original question length **-2.00 content tokens** (original 7.81, crossed 5.81) and -17.1 characters on average.

### AUX-CF2-IX-P-I4 (descriptive): each model under P1 minus the keyword-intent lookup, same-store and pooled, [persona] [pair]

| reader | pop | same-store Δ | pooled Δ |
|---|---|---|---|
| GPT-4.1 mini | A | -0.5153 [-0.5773, -0.4547] [-0.5710, -0.4636] | -0.2405 [-0.2896, -0.1963] [-0.2794, -0.2040] |
| GPT-4.1 mini | B | -0.5222 [-0.6439, -0.3771] [-0.6457, -0.3854] | -0.3143 [-0.4318, -0.1934] [-0.4275, -0.1999] |
| Haiku 4.5 | A | -0.4460 [-0.5137, -0.3840] [-0.5153, -0.3803] | -0.2107 [-0.2573, -0.1681] [-0.2565, -0.1666] |
| Haiku 4.5 | B | -0.4127 [-0.5036, -0.3029] [-0.5178, -0.2973] | -0.1820 [-0.2468, -0.1102] [-0.2505, -0.1107] |
| GPT-5.6 Luna | A | -0.0107 [-0.0387, 0.0101] [-0.0395, 0.0112] | +0.0034 [-0.0215, 0.0240] [-0.0212, 0.0246] |
| GPT-5.6 Luna | B | +0.0333 [-0.0422, 0.1350] [-0.0429, 0.1287] | +0.0298 [-0.0397, 0.1008] [-0.0385, 0.0999] |
| Opus 5 | A | -0.0057 [-0.0341, 0.0167] [-0.0345, 0.0172] | -0.0007 [-0.0275, 0.0223] [-0.0315, 0.0229] |
| Opus 5 | B | +0.0540 [0.0000, 0.1465] [0.0000, 0.1346] | +0.0464 [-0.0040, 0.1122] [-0.0015, 0.1095] |
| GPT-5.6 Sol (Amendment 1) | A | -0.1128 [-0.1754, -0.0576] [-0.1833, -0.0472] | -0.0453 [-0.0788, -0.0113] [-0.0776, -0.0124] |
| GPT-5.6 Sol (Amendment 1) | B | -0.0281 [-0.1708, 0.0960] [-0.1673, 0.0917] | +0.0185 [-0.0533, 0.0996] [-0.0523, 0.0925] |

### AUX-CF2-IX-P-I5 (descriptive): cells 1 vs 2 on the original questions, P1 minus P0, [persona] [pair]

| reader | pop | P0 | P1 | Δ |
|---|---|---|---|---|
| GPT-4.1 mini | A | 0.8240 | 0.8456 | +0.0215 [-0.0212, 0.0581] [-0.0217, 0.0634] |
| GPT-4.1 mini | B | 0.5459 | 0.7175 | +0.1716 [0.0608, 0.2982] [0.0510, 0.2892] |
| Haiku 4.5 | A | 0.8835 | 0.8377 | -0.0458 [-0.0814, -0.0141] [-0.0791, -0.0179] |
| Haiku 4.5 | B | 0.8476 | 0.8543 | +0.0067 [-0.0460, 0.0844] [-0.0533, 0.0725] |
| GPT-5.6 Luna | A | 0.9466 | 0.9446 | -0.0020 [-0.0168, 0.0140] [-0.0166, 0.0127] |
| GPT-5.6 Luna | B | 0.9364 | 0.9135 | -0.0229 [-0.0880, 0.0204] [-0.0895, 0.0192] |
| Opus 5 | A | 0.9322 | 0.9247 | -0.0075 [-0.0190, 0.0025] [-0.0184, 0.0026] |
| Opus 5 | B | 0.9305 | 0.9260 | -0.0044 [-0.0415, 0.0237] [-0.0377, 0.0281] |
| GPT-5.6 Sol (Amendment 1) | A | 0.9213 | 0.9036 | -0.0178 [-0.0597, 0.0221] [-0.0745, 0.0383] |
| GPT-5.6 Sol (Amendment 1) | B | 0.9209 | 0.9283 | +0.0074 [-0.0518, 0.0583] [-0.0843, 0.0851] |

No model lowered by more than 0.05: **True**.

### AUX-CF2-IX-P-I1

**P-I1 FAILS: under the frozen rubric GPT-4.1 mini reads 0.3973 on population A, outside the band [0.45, 0.55]. P-I1 FAILS: under the frozen rubric Haiku 4.5 reads 0.3765 on population A, outside the band [0.45, 0.55]. P-I1 FAILS: under the frozen rubric GPT-5.6 Luna reads 0.3467 on population A, outside the band [0.45, 0.55]. P-I1 FAILS: under the frozen rubric Opus 5 reads 0.8966 on population A, outside the band [0.45, 0.55]. P-I1 FAILS: under the frozen rubric GPT-5.6 Sol reads 0.4406 on population A, outside the band [0.45, 0.55].**

### AUX-CF2-IX-P-I2

**P-I2 FAILS: told that the obligation depends on the question, Haiku 4.5 reads 0.5483 with intervals [0.4819, 0.6152] and [0.4793, 0.6135].**

### AUX-CF2-IX-P-I2B (Amendment 1; a prediction made after the interim read)

**P-I2b HOLDS (a prediction made after the interim read of three lanes): told that the obligation depends on the question, GPT-5.6 Sol separates the intents on population A, 0.8815 with intervals [0.8131, 0.9449] and [0.8200, 0.9349], both excluding 0.50.**

### AUX-CF2-IX-P-I3

**P-I3 HOLDS: the name lookup reads 0.4739 on population A and 0.4527 on population B, within tolerance of 0.50.**

### AUX-CF2-IX-SPEND

Token-metered from the rows (Anthropic Batch at the 0.5 multiplier; OpenAI at the page prices of 2026-09-18 with the cache fields): MINI $0.4876, LUNA $1.1479, H45 $4.7303, OP5 $6.1912; probes {"H45": 0.005009, "LUNA": 0.00127, "MINI": 0.001507, "OP5": 0.039295, "SOL": 0.022899}; **Anthropic $10.9658 of the 15 USD cap; OpenAI $1.6383 for the run, $1.8427 with Phase 1, of the 4 USD cap; the Sol lane (Amendment 1) $8.1466 of its own 12 USD cap.** Not an invoice.

### 14e. E10, the hybrid reader (registrations/ADDENDUM_CF2_HYBRID_READER.md, frozen 2026-09-19 at fe6ff84, sha256 `0cfe92f5762406c1…`; scorer r82_counterfactual/tools/cf2_hybrid.py, sha256 `1b4fef953def9f34…`; results/cf_scores_hybrid.json; no model call)

### AUX-CF2-HYB-LOCK

Gates before fitting: the name lookup on v2 0.7663 (AUX-CF2-NB6-V2), CR-nb1 0.6623 (AUX-R110-A1-CR); a category assigned on 341 of 444 items. Model: LogisticRegression(C=1.0, penalty=l2, solver=lbfgs, max_iter=1000) on standardized f1, f2 and f3; leave-persona-out over 40 personas.

### AUX-CF2-HYB-WHOLE, AUX-CF2-HYB-PERSTATE

Whole set **0.7865**, persona interval [0.7488, 0.8234]; per state SUPERSESSION **0.9070** (lookup 0.9223, minus the lookup -0.0153 ([-0.0293, -0.0029]; [-0.0306, -0.0018])), RETRACTION **0.5889** (lookup 0.5000, minus the lookup +0.0889 ([+0.0120, +0.1673]; [+0.0477, +0.1483])), EXPIRY **0.5942** (lookup 0.5000, minus the lookup +0.0942 ([+0.0165, +0.1717]; [+0.0517, +0.1635])); counted states pooled 0.5897; PN vs PRESENT 0.7821, W/T/L 114/34/0; distinct values 288.

### AUX-CF2-HYB-VS-LOOKUP, AUX-CF2-HYB-VS-NB1, AUX-CF2-HYB-VS-MODELS (paired, item-level; persona-grouped)

Hybrid minus the name lookup +0.0201 ([-0.0016, +0.0410]; [+0.0039, +0.0409]); hybrid minus CR-nb1 +0.1242 ([+0.0668, +0.1816]; [+0.0825, +0.1656]).

- GPT-4.1 mini (0.7167) minus the hybrid: -0.0698 ([-0.1187, -0.0192]; [-0.1094, -0.0316])
- Haiku 4.5 (0.7566) minus the hybrid: -0.0299 ([-0.0862, +0.0210]; [-0.0694, +0.0093])
- Opus 5 (0.8405) minus the hybrid: +0.0540 ([+0.0061, +0.1004]; [+0.0188, +0.0888])
- GPT-5.6 Sol (0.8500) minus the hybrid: +0.0635 ([+0.0214, +0.1108]; [+0.0346, +0.0913])
- GPT-5.6 Luna (0.8417) minus the hybrid: +0.0553 ([+0.0169, +0.0987]; [+0.0245, +0.0864])

### AUX-CF2-HYB-COEF (the leave-persona-out fits: 40 folds; the range over folds)

| coefficient | min | max |
|---|---:|---:|
| f1_lookup | +1.1293 | +1.2915 |
| f2_share | +0.3852 | +0.5263 |
| f3_assigned | -0.4956 | -0.3770 |
| intercept | -0.4768 | -0.3961 |

### AUX-CF2-HYB-P-H1, AUX-CF2-HYB-P-H2

**P-H1 FAILS: the hybrid reads 0.7865 against the lookup's 0.7663, difference +0.0201 with intervals [-0.0016, +0.0410] and [+0.0039, +0.0409].**

**P-H2 HOLDS: GPT-5.6 Sol minus the hybrid is +0.0635 with intervals [+0.0214, +0.1108] and [+0.0346, +0.0913], reliably positive.**

<!-- R125-T1 BEGIN (written by reviews/r125/tools/r125_t1_report.py; do not edit by hand) -->

## 15. AUX-CF2-R125-T1 — the matched metric (program R125, Task 1; 2026-09-20; post hoc, offline, no model call; `reviews/r125/tools/r125_readers.py`, `r125_matched.py`, `r125_t1_report.py`; `reviews/r125/results/r125_vectors.json`, `r125_matched.json`; tables `reviews/r125/T1_TABLES.md`; Figure 3 data on the matched metric `reviews/r125/results/fig3_data_matched.tex`)

Matched AUROC = (W + T/2) / n within the triple (PN against PRESENT, the primary; PN against ABSENT beside), ties exact equality of the collapsed scores; the triple-level and the persona-grouped bootstrap (1,000 draws, seed 42); reliable = both intervals exclude zero. Every gated reader reproduced its recorded pooled row at four decimals before scoring. Every row here is post hoc and labelled so.

### AUX-CF2-R125-SANITY — the printed W/T/L of Table 1 (tab:cf-main, v22 sha f0549e2a) and of the appendix reproduce from the rows: **PASS** (every row)

| row | where | printed W/T/L | computed W/T/L | (W + T/2) / 148 | ok |
|---|---|---|---|---:|---|
| ALLSTATES_v3 | Table 1 | 121/27/0 | 121/27/0 | 0.9088 | yes |
| CR-nb1_v2 | Table 1 | 65/83/0 | 65/83/0 | 0.7196 | yes |
| CR-oracle-a_v2 | Table 1 | 60/88/0 | 60/88/0 | 0.7027 | yes |
| H45_v2 | Table 1 | 89/52/7 | 89/52/7 | 0.7770 | yes |
| H45_v3 | Table 1 | 125/18/5 | 125/18/5 | 0.9054 | yes |
| LOOKUP_v2 | Table 1 | 82/66/0 | 82/66/0 | 0.7770 | yes |
| LUNA5_P1_v2 | appendix (tab:pnpresent / tab:cf-p1) | 125/1/22 | 125/1/22 | 0.8480 | yes |
| LUNA_v2 | Table 1 | 129/2/17 | 129/2/17 | 0.8784 | yes |
| MINI1_P1_v2 | appendix (tab:pnpresent / tab:cf-p1) | 80/52/16 | 80/52/16 | 0.7162 | yes |
| MINI1_v2 | appendix (tab:pnpresent / tab:cf-p1) | 81/57/10 | 81/57/10 | 0.7399 | yes |
| MINI1_v3 | appendix (tab:pnpresent / tab:cf-p1) | 105/32/11 | 105/32/11 | 0.8176 | yes |
| MINI5_v2 | Table 1 | 100/15/33 | 100/15/33 | 0.7264 | yes |
| MINI5_v3 | Table 1 | 130/5/13 | 130/5/13 | 0.8953 | yes |
| OP5_v2 | Table 1 | 128/3/17 | 128/3/17 | 0.8750 | yes |
| OP5_v3 | Table 1 | 139/0/9 | 139/0/9 | 0.9392 | yes |
| SOL_v2 | Table 1 | 126/2/20 | 126/2/20 | 0.8581 | yes |
| CR-oracle-state_v2rcat/EXPIRY | AUX-V2RCAT-REF | pooled 0.3611 | computed 0.3611 | | yes |
| CR-oracle-state_v2rcat/RETRACTION | AUX-V2RCAT-REF | pooled 0.3028 | computed 0.3028 | | yes |
| CR-totals-a_v2rcat/EXPIRY | AUX-V2RCAT-REF | pooled 0.3894 | computed 0.3894 | | yes |
| CR-totals-a_v2rcat/RETRACTION | AUX-V2RCAT-REF | pooled 0.4044 | computed 0.4044 | | yes |

### AUX-CF2-R125-MATCHED-V2, -V3, -V2R, -V2RCAT — every reader under the matched metric (whole set and per state; the pooled row and the state-balanced pooled row beside)

### AUX-CF2-R125-MATCHED-V2 — the superseded-only summary and the readers of its texts

| reader | pooled (whole) | pooled sup / ret / exp | state-balanced | PN vs PRESENT W/T/L | matched (whole) | triple interval | persona interval | matched sup / ret / exp | PN vs ABSENT W/T/L | matched (whole) | matched sup / ret / exp |
|---|---:|---|---:|---|---:|---|---|---|---|---:|---|
| Name lookup | 0.7663 | 0.9223 / 0.5000 / 0.5000 | 0.6408 | 82/66/0 | 0.7770 | [0.7365, 0.8176] | [0.7346, 0.8188] | 0.9659 / 0.5000 / 0.5000 | 82/66/0 | 0.7770 | 0.9659 / 0.5000 / 0.5000 |
| GPT-4.1 mini, one draw (t = 0) | 0.7167 | 0.8308 / 0.5283 / 0.5489 | 0.6360 | 81/57/10 | 0.7399 | [0.6858, 0.7872] | [0.6916, 0.7911] | 0.8807 / 0.5500 / 0.5167 | 78/63/7 | 0.7399 | 0.8693 / 0.5500 / 0.5500 |
| GPT-4.1 mini, five draws (Table 1's row) | 0.7648 | 0.8793 / 0.5761 / 0.5594 | 0.6716 | 100/15/33 | 0.7264 | [0.6520, 0.7973] | [0.6646, 0.7871] | 0.8920 / 0.5667 / 0.4000 | 119/14/15 | 0.8514 | 0.9205 / 0.8000 / 0.7000 |
| Haiku 4.5 | 0.7566 | 0.8876 / 0.5433 / 0.5794 | 0.6701 | 89/52/7 | 0.7770 | [0.7264, 0.8243] | [0.7175, 0.8321] | 0.9148 / 0.5667 / 0.5833 | 98/46/4 | 0.8176 | 0.9375 / 0.6333 / 0.6500 |
| GPT-5.6 Luna | 0.8417 | 0.9426 / 0.5458 / 0.6167 | 0.7017 | 129/2/17 | 0.8784 | [0.8209, 0.9291] | [0.8134, 0.9363] | 0.9602 / 0.6500 / 0.8667 | 121/0/27 | 0.8176 | 0.9659 / 0.5667 / 0.6333 |
| GPT-5.6 Sol | 0.8500 | 0.9383 / 0.5322 / 0.6403 | 0.7036 | 126/2/20 | 0.8581 | [0.8040, 0.9122] | [0.8109, 0.9008] | 0.9602 / 0.5833 / 0.8333 | 122/2/24 | 0.8311 | 0.9432 / 0.5667 / 0.7667 |
| Opus 5 | 0.8405 | 0.9325 / 0.5872 / 0.6150 | 0.7116 | 128/3/17 | 0.8750 | [0.8209, 0.9257] | [0.8176, 0.9317] | 0.9773 / 0.7667 / 0.6833 | 131/2/15 | 0.8919 | 0.9716 / 0.7833 / 0.7667 |
| Haiku 4.5, draw 1 | 0.7555 | 0.8837 / 0.5606 / 0.5814 | 0.6752 | 83/60/5 | 0.7635 | [0.7162, 0.8108] | [0.7157, 0.8085] | 0.9034 / 0.5833 / 0.5333 | 90/55/3 | 0.7939 | 0.9148 / 0.6167 / 0.6167 |
| GPT-5.6 Luna, draw 1 | 0.8265 | 0.9165 / 0.5589 / 0.5872 | 0.6875 | 121/7/20 | 0.8412 | [0.7871, 0.8953] | [0.8016, 0.8869] | 0.9318 / 0.7000 / 0.7167 | 118/8/22 | 0.8243 | 0.9659 / 0.5500 / 0.6833 |
| GPT-5.6 Sol, draw 1 | 0.8277 | 0.9018 / 0.5689 / 0.5931 | 0.6879 | 115/10/23 | 0.8108 | [0.7466, 0.8682] | [0.7481, 0.8650] | 0.9489 / 0.5667 / 0.6500 | 114/9/25 | 0.8007 | 0.8920 / 0.6833 / 0.6500 |
| Opus 5, draw 1 | 0.8400 | 0.9317 / 0.5858 / 0.6169 | 0.7115 | 122/13/13 | 0.8682 | [0.8176, 0.9122] | [0.8066, 0.9201] | 0.9716 / 0.7333 / 0.7000 | 127/8/13 | 0.8851 | 0.9602 / 0.7833 / 0.7667 |
| GPT-4.1 mini, draw 1 of five | 0.7257 | 0.8488 / 0.5278 / 0.5431 | 0.6399 | 90/34/24 | 0.7230 | [0.6622, 0.7838] | [0.6667, 0.7835] | 0.8807 / 0.5500 / 0.4333 | 94/41/13 | 0.7736 | 0.8920 / 0.6000 / 0.6000 |
| Count reader, guessed category | 0.6623 | 0.6573 / 0.6669 / 0.6872 | 0.6705 | 65/83/0 | 0.7196 | [0.6791, 0.7635] | [0.6788, 0.7567] | 0.6932 / 0.7667 / 0.7500 | 66/72/10 | 0.6892 | 0.6875 / 0.7333 / 0.6500 |
| Count reader, given category | 0.6043 | 0.5000 / 0.7306 / 0.7778 | 0.6695 | 60/88/0 | 0.7027 | [0.6622, 0.7432] | [0.6596, 0.7448] | 0.5000 / 1.0000 / 1.0000 | 60/88/0 | 0.7027 | 0.5000 / 1.0000 / 1.0000 |
| State-aware count reader | 0.8580 | 0.9006 / 0.8944 / 0.7778 | 0.8576 | 148/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] | 1.0000 / 1.0000 / 1.0000 | 148/0/0 | 1.0000 | 1.0000 / 1.0000 / 1.0000 |
| Totals reader | 0.5603 | 0.5028 / 0.6347 / 0.6922 | 0.6099 | 60/88/0 | 0.7027 | [0.6622, 0.7432] | [0.6596, 0.7448] | 0.5000 / 1.0000 / 1.0000 | 62/86/0 | 0.7095 | 0.5114 / 1.0000 / 1.0000 |
| Category-given share reader (privileged) | 0.8473 | 0.8981 / 0.7336 / 0.8528 | 0.8282 | 148/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] | 1.0000 / 1.0000 / 1.0000 | 146/0/2 | 0.9865 | 0.9886 / 1.0000 / 0.9667 |
| Whole name-map lookup | 0.5776 | 0.5728 / 0.5758 / 0.5919 | 0.5802 | 0/148/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] | 0.5000 / 0.5000 / 0.5000 | 62/85/1 | 0.7061 | 0.7102 / 0.6833 / 0.7167 |
| Hybrid reader (E10) | 0.7865 | 0.9070 / 0.5889 / 0.5942 | 0.6967 | 114/34/0 | 0.8851 | [0.8514, 0.9189] | [0.8504, 0.9167] | 0.9716 / 0.7667 / 0.7500 | 114/24/10 | 0.8514 | 0.9716 / 0.7000 / 0.6500 |
| Random-token lookup | 0.5954 | 0.6651 / 0.5000 / 0.5000 | 0.5550 | 45/101/2 | 0.6453 | [0.6081, 0.6858] | [0.6014, 0.6926] | 0.7443 / 0.5000 / 0.5000 | 45/101/2 | 0.6453 | 0.7443 / 0.5000 / 0.5000 |
| Name lookup, all-mpnet-base-v2 | 0.7605 | 0.9156 / 0.5000 / 0.5000 | 0.6385 | 81/67/0 | 0.7736 | [0.7331, 0.8176] | [0.7310, 0.8140] | 0.9602 / 0.5000 / 0.5000 | 81/67/0 | 0.7736 | 0.9602 / 0.5000 / 0.5000 |
| Name lookup, bge-small-en-v1.5 | 0.7584 | 0.9203 / 0.5000 / 0.5000 | 0.6401 | 83/65/0 | 0.7804 | [0.7399, 0.8209] | [0.7381, 0.8217] | 0.9716 / 0.5000 / 0.5000 | 83/65/0 | 0.7804 | 0.9716 / 0.5000 / 0.5000 |
| GPT-5.6 Luna, intent-explicit rubric | 0.8531 | 0.9470 / 0.5997 / 0.6347 | 0.7271 | 125/1/22 | 0.8480 | [0.7939, 0.9054] | [0.7925, 0.8921] | 0.9489 / 0.6333 / 0.7667 | 129/0/19 | 0.8716 | 0.9432 / 0.7000 / 0.8333 |
| GPT-4.1 mini, intent-explicit rubric | 0.7253 | 0.8591 / 0.5456 / 0.4758 | 0.6268 | 80/52/16 | 0.7162 | [0.6622, 0.7670] | [0.6554, 0.7737] | 0.8750 / 0.5333 / 0.4333 | 80/59/9 | 0.7399 | 0.8807 / 0.5833 / 0.4833 |
| Haiku 4.5, names only (E2) | 0.7507 | 0.9010 / 0.5631 / 0.5642 | 0.6761 | 85/59/4 | 0.7736 | [0.7297, 0.8176] | [0.7279, 0.8172] | 0.9318 / 0.5167 / 0.5667 | 98/44/6 | 0.8108 | 0.9148 / 0.6667 / 0.6500 |
| Haiku 4.5, counts only (E2) | 0.5945 | 0.6315 / 0.5553 / 0.5189 | 0.5686 | 61/66/21 | 0.6351 | [0.5743, 0.6927] | [0.5647, 0.7044] | 0.7159 / 0.5833 / 0.4500 | 63/67/18 | 0.6520 | 0.6932 / 0.6167 / 0.5667 |
| GPT-4.1 mini, names only (E2) | 0.7103 | 0.8564 / 0.5344 / 0.5006 | 0.6305 | 75/69/4 | 0.7399 | [0.6993, 0.7804] | [0.6966, 0.7789] | 0.8864 / 0.5500 / 0.5000 | 73/70/5 | 0.7297 | 0.8693 / 0.5167 / 0.5333 |
| GPT-4.1 mini, names only, dash rule (E2) | 0.6891 | 0.8432 / 0.4500 / 0.4764 | 0.5899 | 69/66/13 | 0.6892 | [0.6385, 0.7399] | [0.6266, 0.7483] | 0.8523 / 0.4500 / 0.4500 | 72/67/9 | 0.7128 | 0.8693 / 0.4333 / 0.5333 |
| GPT-4.1 mini, counts only (E2) | 0.5862 | 0.6107 / 0.6053 / 0.4933 | 0.5698 | 48/83/17 | 0.6047 | [0.5541, 0.6554] | [0.5497, 0.6560] | 0.6534 / 0.6167 / 0.4500 | 42/86/20 | 0.5743 | 0.6080 / 0.5667 / 0.4833 |

### AUX-CF2-R125-MATCHED-V3 — the all-states summary

| reader | pooled (whole) | pooled sup / ret / exp | state-balanced | PN vs PRESENT W/T/L | matched (whole) | triple interval | persona interval | matched sup / ret / exp | PN vs ABSENT W/T/L | matched (whole) | matched sup / ret / exp |
|---|---:|---|---:|---|---:|---|---|---|---|---:|---|
| All-states lookup | 0.8756 | 0.8995 / 0.7975 / 0.8711 | 0.8560 | 121/27/0 | 0.9088 | [0.8783, 0.9392] | [0.8785, 0.9379] | 0.9432 / 0.8167 / 0.9000 | 125/23/0 | 0.9223 | 0.9489 / 0.8667 / 0.9000 |
| GPT-4.1 mini, one draw (t = 0) | 0.7967 | 0.8444 / 0.8725 / 0.5869 | 0.7679 | 105/32/11 | 0.8176 | [0.7669, 0.8649] | [0.7516, 0.8767] | 0.8750 / 0.9333 / 0.5333 | 105/40/3 | 0.8446 | 0.8750 / 0.9500 / 0.6500 |
| GPT-4.1 mini, five draws (Table 1's row) | 0.8323 | 0.8829 / 0.8433 / 0.6719 | 0.7994 | 130/5/13 | 0.8953 | [0.8446, 0.9358] | [0.8449, 0.9403] | 0.9205 / 0.9333 / 0.7833 | 128/4/16 | 0.8784 | 0.9261 / 0.9333 / 0.6833 |
| Haiku 4.5 | 0.8773 | 0.8852 / 0.9042 / 0.8269 | 0.8721 | 125/18/5 | 0.9054 | [0.8682, 0.9393] | [0.8636, 0.9399] | 0.8920 / 0.9333 / 0.9167 | 128/15/5 | 0.9155 | 0.9034 / 0.9500 / 0.9167 |
| Opus 5 | 0.9079 | 0.9319 / 0.8100 / 0.9267 | 0.8895 | 139/0/9 | 0.9392 | [0.8919, 0.9730] | [0.8944, 0.9750] | 0.9659 / 0.8333 / 0.9667 | 142/0/6 | 0.9595 | 0.9773 / 0.9000 / 0.9667 |
| Opus 5, draw 1 | 0.9029 | 0.9279 / 0.7856 / 0.9231 | 0.8789 | 138/4/6 | 0.9459 | [0.9088, 0.9764] | [0.9130, 0.9755] | 0.9830 / 0.8167 / 0.9667 | 140/4/4 | 0.9595 | 0.9716 / 0.9333 / 0.9500 |
| GPT-4.1 mini, draw 1 of five | 0.8029 | 0.8533 / 0.7811 / 0.6683 | 0.7676 | 113/22/13 | 0.8378 | [0.7872, 0.8851] | [0.7810, 0.8873] | 0.8636 / 0.8500 / 0.7500 | 115/12/21 | 0.8176 | 0.8750 / 0.8000 / 0.6667 |
| Random-token lookup | 0.5479 | 0.5385 / 0.5697 / 0.5694 | 0.5592 | 31/117/0 | 0.6047 | [0.5777, 0.6385] | [0.5680, 0.6460] | 0.5966 / 0.5500 / 0.6833 | 32/116/0 | 0.6081 | 0.5966 / 0.5667 / 0.6833 |
| All-states lookup, all-mpnet-base-v2 | 0.8646 | 0.8814 / 0.8019 / 0.8717 | 0.8517 | 122/26/0 | 0.9122 | [0.8784, 0.9426] | [0.8852, 0.9380] | 0.9432 / 0.8167 / 0.9167 | 126/22/0 | 0.9257 | 0.9489 / 0.8667 / 0.9167 |
| All-states lookup, bge-small-en-v1.5 | 0.8690 | 0.8802 / 0.8172 / 0.8878 | 0.8617 | 123/25/0 | 0.9155 | [0.8851, 0.9427] | [0.8892, 0.9414] | 0.9432 / 0.8167 / 0.9333 | 129/19/0 | 0.9358 | 0.9545 / 0.8833 / 0.9333 |

### AUX-CF2-R125-MATCHED-V2R — the totals-randomized summary

| reader | pooled (whole) | pooled sup / ret / exp | state-balanced | PN vs PRESENT W/T/L | matched (whole) | triple interval | persona interval | matched sup / ret / exp | PN vs ABSENT W/T/L | matched (whole) | matched sup / ret / exp |
|---|---:|---|---:|---|---:|---|---|---|---|---:|---|
| GPT-4.1 mini, one draw (t = 0) | 0.7179 | 0.8500 / 0.4950 / 0.5144 | 0.6198 | 78/50/20 | 0.6959 | [0.6385, 0.7500] | [0.6490, 0.7429] | 0.8750 / 0.4000 / 0.4667 | 85/56/7 | 0.7635 | 0.8864 / 0.5833 / 0.5833 |
| Haiku 4.5 | 0.7638 | 0.8874 / 0.5844 / 0.5847 | 0.6855 | 89/50/9 | 0.7703 | [0.7196, 0.8176] | [0.7177, 0.8212] | 0.8977 / 0.6167 / 0.5500 | 100/42/6 | 0.8176 | 0.9261 / 0.6500 / 0.6667 |
| Opus 5 | 0.8353 | 0.9322 / 0.5681 / 0.6092 | 0.7032 | 128/0/20 | 0.8649 | [0.8108, 0.9189] | [0.8029, 0.9241] | 0.9659 / 0.6667 / 0.7667 | 131/1/16 | 0.8885 | 0.9773 / 0.8000 / 0.7167 |
| Totals reader (the permuted lines) | 0.4472 | 0.4775 / 0.4044 / 0.3894 | 0.4238 | 31/58/59 | 0.4054 | [0.3446, 0.4662] | [0.3415, 0.4692] | 0.4602 / 0.3667 / 0.2833 | 33/61/54 | 0.4291 | 0.4716 / 0.3833 / 0.3500 |
| Count reader, given category (unchanged) | 0.6043 | 0.5000 / 0.7306 / 0.7778 | 0.6695 | 60/88/0 | 0.7027 | [0.6622, 0.7432] | [0.6596, 0.7448] | 0.5000 / 1.0000 / 1.0000 | 60/88/0 | 0.7027 | 0.5000 / 1.0000 / 1.0000 |
| Count reader, guessed category (unchanged) | 0.6623 | 0.6573 / 0.6669 / 0.6872 | 0.6705 | 65/83/0 | 0.7196 | [0.6791, 0.7635] | [0.6788, 0.7567] | 0.6932 / 0.7667 / 0.7500 | 66/72/10 | 0.6892 | 0.6875 / 0.7333 / 0.6500 |

### AUX-CF2-R125-MATCHED-V2RCAT — the moved-count control

| reader | pooled (whole) | pooled sup / ret / exp | state-balanced | PN vs PRESENT W/T/L | matched (whole) | triple interval | persona interval | matched sup / ret / exp | PN vs ABSENT W/T/L | matched (whole) | matched sup / ret / exp |
|---|---:|---|---:|---|---:|---|---|---|---|---:|---|
| GPT-4.1 mini, one draw | 0.7410 | 0.8388 / 0.5553 / 0.6100 | 0.6680 | 80/58/10 | 0.7365 | [0.6858, 0.7838] | [0.6803, 0.7875] | 0.8636 / 0.5500 / 0.5500 | 86/54/8 | 0.7635 | 0.8580 / 0.5500 / 0.7000 |
| Haiku 4.5, five draws | 0.7525 | 0.8873 / 0.5361 / 0.5342 | 0.6525 | 84/53/11 | 0.7466 | [0.6959, 0.7940] | [0.6905, 0.7968] | 0.8977 / 0.5667 / 0.4833 | 99/36/13 | 0.7905 | 0.9375 / 0.5833 / 0.5667 |
| Opus 5, five draws (E1 Amendment 1) | 0.8075 | 0.9312 / 0.4869 / 0.4869 | 0.6350 | 108/3/37 | 0.7399 | [0.6655, 0.8108] | [0.6786, 0.8052] | 0.9432 / 0.4000 / 0.4833 | 120/2/26 | 0.8176 | 0.9773 / 0.6000 / 0.5667 |
| Opus 5, draw 1 | 0.8049 | 0.9303 / 0.4861 / 0.4914 | 0.6359 | 105/12/31 | 0.7500 | [0.6858, 0.8143] | [0.6931, 0.8099] | 0.9261 / 0.4333 / 0.5500 | 108/12/28 | 0.7703 | 0.9602 / 0.5333 / 0.4500 |
| GPT-5.6 Luna, five draws (E9) | 0.8121 | 0.9416 / 0.4794 / 0.5008 | 0.6406 | 113/1/34 | 0.7669 | [0.6993, 0.8412] | [0.7044, 0.8263] | 0.9716 / 0.3333 / 0.6000 | 110/1/37 | 0.7466 | 0.9375 / 0.4000 / 0.5333 |
| GPT-5.6 Luna, draw 1 | 0.8150 | 0.9294 / 0.4894 / 0.5794 | 0.6661 | 112/10/26 | 0.7905 | [0.7264, 0.8514] | [0.7230, 0.8533] | 0.9375 / 0.5333 / 0.6167 | 109/11/28 | 0.7736 | 0.9375 / 0.3667 / 0.7000 |
| GPT-5.6 Sol, five draws (E9) | 0.8172 | 0.9373 / 0.5000 / 0.4489 | 0.6287 | 107/1/40 | 0.7264 | [0.6554, 0.8007] | [0.6552, 0.7946] | 0.9602 / 0.4000 / 0.3667 | 116/1/31 | 0.7872 | 0.9489 / 0.6667 / 0.4333 |
| GPT-5.6 Sol, draw 1 | 0.8024 | 0.9176 / 0.5000 / 0.4039 | 0.6072 | 103/9/36 | 0.7264 | [0.6554, 0.7940] | [0.6511, 0.7978] | 0.9375 / 0.4667 / 0.3667 | 106/6/36 | 0.7365 | 0.9148 / 0.6167 / 0.3333 |
| State-aware count reader | 0.6520 | 0.9006 / 0.3028 / 0.3611 | 0.5215 | 88/33/27 | 0.7061 | [0.6385, 0.7703] | [0.6415, 0.7714] | 1.0000 / 0.2667 / 0.2833 | 88/27/33 | 0.6858 | 1.0000 / 0.2333 / 0.2167 |
| Totals reader | 0.4472 | 0.4775 / 0.4044 / 0.3894 | 0.4238 | 31/58/59 | 0.4054 | [0.3446, 0.4662] | [0.3415, 0.4692] | 0.4602 / 0.3667 / 0.2833 | 33/61/54 | 0.4291 | 0.4716 / 0.3833 / 0.3500 |
| Count reader, given category | 0.4585 | 0.5000 / 0.4539 / 0.3611 | 0.4383 | 0/121/27 | 0.4088 | [0.3784, 0.4392] | [0.3784, 0.4385] | 0.5000 / 0.2667 / 0.2833 | 6/112/30 | 0.4189 | 0.5000 / 0.3833 / 0.2167 |
| Count reader, guessed category | 0.5914 | 0.6573 / 0.4892 / 0.4853 | 0.5439 | 35/95/18 | 0.5574 | [0.5101, 0.6047] | [0.5101, 0.6085] | 0.6932 / 0.2667 / 0.4500 | 48/82/18 | 0.6014 | 0.6875 / 0.5000 / 0.4500 |
| Category-given share reader | 0.6741 | 0.8981 / 0.3944 / 0.3122 | 0.5349 | 88/22/38 | 0.6689 | [0.5980, 0.7399] | [0.6018, 0.7363] | 1.0000 / 0.0833 / 0.2833 | 91/14/43 | 0.6622 | 0.9886 / 0.2833 / 0.0833 |

### AUX-CF2-R125-PERSTATE — per-state matched PN vs PRESENT with both intervals

### v2: per-state matched PN vs PRESENT with both intervals (W/T/L per state)

| reader | sup W/T/L | sup matched | triple | persona | ret W/T/L | ret matched | triple | persona | exp W/T/L | exp matched | triple | persona |
|---|---|---:|---|---|---|---:|---|---|---|---:|---|---|
| Name lookup | 82/6/0 | 0.9659 | [0.9375, 0.9886] | [0.9286, 0.9944] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] |
| GPT-4.1 mini, one draw (t = 0) | 68/19/1 | 0.8807 | [0.8352, 0.9261] | [0.8274, 0.9321] | 9/15/6 | 0.5500 | [0.4333, 0.6667] | [0.4400, 0.6552] | 4/23/3 | 0.5167 | [0.4333, 0.6000] | [0.4107, 0.6452] |
| GPT-4.1 mini, five draws (Table 1's row) | 76/5/7 | 0.8920 | [0.8295, 0.9489] | [0.8228, 0.9487] | 15/4/11 | 0.5667 | [0.4000, 0.7333] | [0.3906, 0.7414] | 9/6/15 | 0.4000 | [0.2500, 0.5500] | [0.2857, 0.5143] |
| Haiku 4.5 | 76/9/3 | 0.9148 | [0.8580, 0.9602] | [0.8631, 0.9615] | 6/22/2 | 0.5667 | [0.4833, 0.6500] | [0.4825, 0.6607] | 7/21/2 | 0.5833 | [0.4996, 0.6833] | [0.4688, 0.7116] |
| GPT-5.6 Luna | 84/1/3 | 0.9602 | [0.9205, 0.9943] | [0.9175, 0.9937] | 19/1/10 | 0.6500 | [0.4833, 0.8167] | [0.4515, 0.8214] | 26/0/4 | 0.8667 | [0.7333, 0.9667] | [0.7586, 0.9677] |
| GPT-5.6 Sol | 84/1/3 | 0.9602 | [0.9148, 0.9943] | [0.9231, 0.9895] | 17/1/12 | 0.5833 | [0.4167, 0.7500] | [0.4107, 0.7500] | 25/0/5 | 0.8333 | [0.7000, 0.9667] | [0.7000, 0.9394] |
| Opus 5 | 86/0/2 | 0.9773 | [0.9432, 1.0000] | [0.9432, 1.0000] | 22/2/6 | 0.7667 | [0.6167, 0.9000] | [0.6111, 0.9118] | 20/1/9 | 0.6833 | [0.5167, 0.8333] | [0.5000, 0.8750] |
| Haiku 4.5, draw 1 | 73/13/2 | 0.9034 | [0.8523, 0.9489] | [0.8512, 0.9494] | 5/25/0 | 0.5833 | [0.5167, 0.6504] | [0.5263, 0.6600] | 5/22/3 | 0.5333 | [0.4333, 0.6333] | [0.4697, 0.6000] |
| GPT-5.6 Luna, draw 1 | 81/2/5 | 0.9318 | [0.8807, 0.9773] | [0.8736, 0.9817] | 21/0/9 | 0.7000 | [0.5333, 0.8667] | [0.5172, 0.8622] | 19/5/6 | 0.7167 | [0.5667, 0.8504] | [0.6249, 0.8182] |
| GPT-5.6 Sol, draw 1 | 82/3/3 | 0.9489 | [0.9034, 0.9830] | [0.8990, 0.9880] | 14/6/10 | 0.5667 | [0.4000, 0.7167] | [0.4038, 0.7414] | 19/1/10 | 0.6500 | [0.4833, 0.8167] | [0.4821, 0.8065] |
| Opus 5, draw 1 | 85/1/2 | 0.9716 | [0.9375, 1.0000] | [0.9375, 1.0000] | 19/6/5 | 0.7333 | [0.5833, 0.8500] | [0.5962, 0.8594] | 18/6/6 | 0.7000 | [0.5500, 0.8500] | [0.5333, 0.8600] |
| GPT-4.1 mini, draw 1 of five | 73/9/6 | 0.8807 | [0.8239, 0.9375] | [0.8139, 0.9360] | 10/13/7 | 0.5500 | [0.4167, 0.6833] | [0.4137, 0.6765] | 7/12/11 | 0.4333 | [0.3000, 0.5667] | [0.2777, 0.6001] |
| Count reader, guessed category | 34/54/0 | 0.6932 | [0.6420, 0.7386] | [0.6288, 0.7566] | 16/14/0 | 0.7667 | [0.6833, 0.8500] | [0.6897, 0.8519] | 15/15/0 | 0.7500 | [0.6667, 0.8333] | [0.6613, 0.8261] |
| Count reader, given category | 0/88/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] | 30/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] | 30/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] |
| State-aware count reader | 88/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] | 30/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] | 30/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] |
| Totals reader | 0/88/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] | 30/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] | 30/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] |
| Category-given share reader (privileged) | 88/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] | 30/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] | 30/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] |
| Whole name-map lookup | 0/88/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] |
| Hybrid reader (E10) | 83/5/0 | 0.9716 | [0.9489, 0.9943] | [0.9323, 1.0000] | 16/14/0 | 0.7667 | [0.6833, 0.8500] | [0.6897, 0.8519] | 15/15/0 | 0.7500 | [0.6667, 0.8333] | [0.6613, 0.8261] |
| Random-token lookup | 45/41/2 | 0.7443 | [0.6874, 0.8011] | [0.6802, 0.8148] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] |
| Name lookup, all-mpnet-base-v2 | 81/7/0 | 0.9602 | [0.9318, 0.9830] | [0.9221, 0.9890] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] |
| Name lookup, bge-small-en-v1.5 | 83/5/0 | 0.9716 | [0.9432, 0.9943] | [0.9360, 1.0000] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] |
| GPT-5.6 Luna, intent-explicit rubric | 83/1/4 | 0.9489 | [0.9034, 0.9886] | [0.9111, 0.9868] | 19/0/11 | 0.6333 | [0.4667, 0.8000] | [0.4643, 0.7880] | 23/0/7 | 0.7667 | [0.6000, 0.9000] | [0.6000, 0.9000] |
| GPT-4.1 mini, intent-explicit rubric | 68/18/2 | 0.8750 | [0.8239, 0.9205] | [0.8218, 0.9286] | 9/14/7 | 0.5333 | [0.4000, 0.6667] | [0.4037, 0.6552] | 3/20/7 | 0.4333 | [0.3333, 0.5333] | [0.3448, 0.5179] |
| Haiku 4.5, names only (E2) | 77/10/1 | 0.9318 | [0.8977, 0.9659] | [0.8871, 0.9702] | 3/25/2 | 0.5167 | [0.4500, 0.6000] | [0.4444, 0.5926] | 5/24/1 | 0.5667 | [0.5000, 0.6500] | [0.4828, 0.6607] |
| Haiku 4.5, counts only (E2) | 48/30/10 | 0.7159 | [0.6419, 0.7841] | [0.6264, 0.8023] | 8/19/3 | 0.5833 | [0.4833, 0.6833] | [0.4997, 0.6924] | 5/17/8 | 0.4500 | [0.3333, 0.5667] | [0.3333, 0.5517] |
| GPT-4.1 mini, names only (E2) | 69/18/1 | 0.8864 | [0.8408, 0.9318] | [0.8414, 0.9333] | 4/25/1 | 0.5500 | [0.4833, 0.6167] | [0.4667, 0.6364] | 2/26/2 | 0.5000 | [0.4333, 0.5667] | [0.4374, 0.5715] |
| GPT-4.1 mini, names only, dash rule (E2) | 65/20/3 | 0.8523 | [0.8010, 0.9034] | [0.7977, 0.9056] | 3/21/6 | 0.4500 | [0.3663, 0.5500] | [0.3667, 0.5323] | 1/25/4 | 0.4500 | [0.3833, 0.5167] | [0.3571, 0.5312] |
| GPT-4.1 mini, counts only (E2) | 34/47/7 | 0.6534 | [0.5909, 0.7159] | [0.5904, 0.7108] | 11/15/4 | 0.6167 | [0.5000, 0.7333] | [0.5000, 0.7414] | 3/21/6 | 0.4500 | [0.3663, 0.5500] | [0.3281, 0.5517] |

### v3: per-state matched PN vs PRESENT with both intervals (W/T/L per state)

| reader | sup W/T/L | sup matched | triple | persona | ret W/T/L | ret matched | triple | persona | exp W/T/L | exp matched | triple | persona |
|---|---|---:|---|---|---|---:|---|---|---|---:|---|---|
| All-states lookup | 78/10/0 | 0.9432 | [0.9091, 0.9716] | [0.9022, 0.9810] | 19/11/0 | 0.8167 | [0.7333, 0.9000] | [0.7321, 0.8940] | 24/6/0 | 0.9000 | [0.8333, 0.9667] | [0.8333, 0.9545] |
| GPT-4.1 mini, one draw (t = 0) | 71/12/5 | 0.8750 | [0.8182, 0.9261] | [0.7981, 0.9396] | 27/2/1 | 0.9333 | [0.8500, 1.0000] | [0.8391, 1.0000] | 7/18/5 | 0.5333 | [0.4167, 0.6500] | [0.3966, 0.6786] |
| GPT-4.1 mini, five draws (Table 1's row) | 80/2/6 | 0.9205 | [0.8693, 0.9716] | [0.8636, 0.9670] | 28/0/2 | 0.9333 | [0.8333, 1.0000] | [0.8214, 1.0000] | 22/3/5 | 0.7833 | [0.6333, 0.9167] | [0.6429, 0.9107] |
| Haiku 4.5 | 73/11/4 | 0.8920 | [0.8409, 0.9432] | [0.8367, 0.9412] | 27/2/1 | 0.9333 | [0.8500, 1.0000] | [0.8676, 1.0000] | 25/5/0 | 0.9167 | [0.8500, 0.9833] | [0.8387, 0.9828] |
| Opus 5 | 85/0/3 | 0.9659 | [0.9318, 1.0000] | [0.9140, 1.0000] | 25/0/5 | 0.8333 | [0.7000, 0.9667] | [0.7000, 0.9432] | 29/0/1 | 0.9667 | [0.9000, 1.0000] | [0.8929, 1.0000] |
| Opus 5, draw 1 | 85/3/0 | 0.9830 | [0.9602, 1.0000] | [0.9591, 1.0000] | 24/1/5 | 0.8167 | [0.6667, 0.9333] | [0.6800, 0.9355] | 29/0/1 | 0.9667 | [0.9000, 1.0000] | [0.8929, 1.0000] |
| GPT-4.1 mini, draw 1 of five | 71/10/7 | 0.8636 | [0.8011, 0.9205] | [0.7903, 0.9294] | 24/3/3 | 0.8500 | [0.7333, 0.9500] | [0.7306, 0.9500] | 18/9/3 | 0.7500 | [0.6333, 0.8667] | [0.6289, 0.8751] |
| Random-token lookup | 17/71/0 | 0.5966 | [0.5568, 0.6364] | [0.5588, 0.6437] | 3/27/0 | 0.5500 | [0.5000, 0.6004] | [0.5000, 0.6111] | 11/19/0 | 0.6833 | [0.6000, 0.7667] | [0.6034, 0.7759] |
| All-states lookup, all-mpnet-base-v2 | 78/10/0 | 0.9432 | [0.9091, 0.9716] | [0.9023, 0.9770] | 19/11/0 | 0.8167 | [0.7333, 0.9000] | [0.7321, 0.8906] | 25/5/0 | 0.9167 | [0.8500, 0.9671] | [0.8500, 0.9697] |
| All-states lookup, bge-small-en-v1.5 | 78/10/0 | 0.9432 | [0.9091, 0.9773] | [0.9032, 0.9765] | 19/11/0 | 0.8167 | [0.7333, 0.9000] | [0.7321, 0.8906] | 26/4/0 | 0.9333 | [0.8667, 0.9833] | [0.8654, 0.9839] |

### v2r: per-state matched PN vs PRESENT with both intervals (W/T/L per state)

| reader | sup W/T/L | sup matched | triple | persona | ret W/T/L | ret matched | triple | persona | exp W/T/L | exp matched | triple | persona |
|---|---|---:|---|---|---|---:|---|---|---|---:|---|---|
| GPT-4.1 mini, one draw (t = 0) | 69/16/3 | 0.8750 | [0.8182, 0.9261] | [0.8235, 0.9311] | 4/16/10 | 0.4000 | [0.2833, 0.5167] | [0.2679, 0.5143] | 5/18/7 | 0.4667 | [0.3500, 0.5833] | [0.3571, 0.5715] |
| Haiku 4.5 | 74/10/4 | 0.8977 | [0.8409, 0.9489] | [0.8483, 0.9412] | 9/19/2 | 0.6167 | [0.5167, 0.7004] | [0.5000, 0.7258] | 6/21/3 | 0.5500 | [0.4500, 0.6500] | [0.4667, 0.6379] |
| Opus 5 | 85/0/3 | 0.9659 | [0.9205, 1.0000] | [0.9139, 1.0000] | 20/0/10 | 0.6667 | [0.4667, 0.8333] | [0.4796, 0.8235] | 23/0/7 | 0.7667 | [0.6000, 0.9000] | [0.6129, 0.9001] |
| Totals reader (the permuted lines) | 15/51/22 | 0.4602 | [0.3977, 0.5227] | [0.3953, 0.5230] | 9/4/17 | 0.3667 | [0.2167, 0.5333] | [0.2321, 0.5188] | 7/3/20 | 0.2833 | [0.1500, 0.4500] | [0.1060, 0.4822] |
| Count reader, given category (unchanged) | 0/88/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] | 30/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] | 30/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] |
| Count reader, guessed category (unchanged) | 34/54/0 | 0.6932 | [0.6420, 0.7386] | [0.6288, 0.7566] | 16/14/0 | 0.7667 | [0.6833, 0.8500] | [0.6897, 0.8519] | 15/15/0 | 0.7500 | [0.6667, 0.8333] | [0.6613, 0.8261] |

### v2rcat: per-state matched PN vs PRESENT with both intervals (W/T/L per state)

| reader | sup W/T/L | sup matched | triple | persona | ret W/T/L | ret matched | triple | persona | exp W/T/L | exp matched | triple | persona |
|---|---|---:|---|---|---|---:|---|---|---|---:|---|---|
| GPT-4.1 mini, one draw | 67/18/3 | 0.8636 | [0.8125, 0.9148] | [0.7975, 0.9303] | 6/21/3 | 0.5500 | [0.4667, 0.6333] | [0.4571, 0.6552] | 7/19/4 | 0.5500 | [0.4500, 0.6667] | [0.4615, 0.6167] |
| Haiku 4.5, five draws | 74/10/4 | 0.8977 | [0.8409, 0.9489] | [0.8494, 0.9425] | 7/20/3 | 0.5667 | [0.4667, 0.6667] | [0.4655, 0.6774] | 3/23/4 | 0.4833 | [0.4000, 0.5667] | [0.4062, 0.5714] |
| Opus 5, five draws (E1 Amendment 1) | 83/0/5 | 0.9432 | [0.8864, 0.9886] | [0.8889, 0.9884] | 11/2/17 | 0.4000 | [0.2333, 0.5667] | [0.2167, 0.5938] | 14/1/15 | 0.4833 | [0.3167, 0.6671] | [0.3103, 0.6538] |
| Opus 5, draw 1 | 81/1/6 | 0.9261 | [0.8693, 0.9773] | [0.8693, 0.9747] | 11/4/15 | 0.4333 | [0.2667, 0.6000] | [0.2498, 0.6252] | 13/7/10 | 0.5500 | [0.4000, 0.7000] | [0.4102, 0.6964] |
| GPT-5.6 Luna, five draws (E9) | 85/1/2 | 0.9716 | [0.9318, 1.0000] | [0.9326, 1.0000] | 10/0/20 | 0.3333 | [0.1667, 0.5000] | [0.1667, 0.5000] | 18/0/12 | 0.6000 | [0.4333, 0.7667] | [0.4286, 0.7857] |
| GPT-5.6 Luna, draw 1 | 81/3/4 | 0.9375 | [0.8864, 0.9830] | [0.8830, 0.9833] | 14/4/12 | 0.5333 | [0.3667, 0.7000] | [0.3666, 0.7039] | 17/3/10 | 0.6167 | [0.4500, 0.7833] | [0.4333, 0.7970] |
| GPT-5.6 Sol, five draws (E9) | 84/1/3 | 0.9602 | [0.9205, 0.9943] | [0.9242, 0.9941] | 12/0/18 | 0.4000 | [0.2333, 0.6000] | [0.2057, 0.5926] | 11/0/19 | 0.3667 | [0.2000, 0.5333] | [0.2142, 0.5185] |
| GPT-5.6 Sol, draw 1 | 81/3/4 | 0.9375 | [0.8920, 0.9773] | [0.8988, 0.9768] | 13/2/15 | 0.4667 | [0.3000, 0.6333] | [0.2968, 0.6429] | 9/4/17 | 0.3667 | [0.2167, 0.5333] | [0.1911, 0.5500] |
| State-aware count reader | 88/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] | 0/16/14 | 0.2667 | [0.1833, 0.3667] | [0.1912, 0.3519] | 0/17/13 | 0.2833 | [0.1996, 0.3667] | [0.2115, 0.3542] |
| Totals reader | 15/51/22 | 0.4602 | [0.3977, 0.5227] | [0.3953, 0.5230] | 9/4/17 | 0.3667 | [0.2167, 0.5333] | [0.2321, 0.5188] | 7/3/20 | 0.2833 | [0.1500, 0.4500] | [0.1060, 0.4822] |
| Count reader, given category | 0/88/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] | 0/16/14 | 0.2667 | [0.1833, 0.3667] | [0.1912, 0.3519] | 0/17/13 | 0.2833 | [0.1996, 0.3667] | [0.2115, 0.3542] |
| Count reader, guessed category | 34/54/0 | 0.6932 | [0.6420, 0.7386] | [0.6288, 0.7566] | 0/16/14 | 0.2667 | [0.1833, 0.3667] | [0.1897, 0.3335] | 1/25/4 | 0.4500 | [0.3833, 0.5167] | [0.3871, 0.5167] |
| Category-given share reader | 88/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] | 0/5/25 | 0.0833 | [0.0167, 0.1500] | [0.0192, 0.1429] | 0/17/13 | 0.2833 | [0.1996, 0.3667] | [0.2115, 0.3542] |

### AUX-CF2-R125-CLASSES — the pooled AUROC by pair class

### v2: the pooled AUROC decomposed by pair class (whole set; pair counts within-triple 296, same-state across questions 18,792, across states 24,720 of 43,808)

| reader | pooled | within-triple (296) | same state, across questions (18,792) | across states (24,720) | state-balanced pooled |
|---|---:|---:|---:|---:|---:|
| Name lookup | 0.7663 | 0.7770 | 0.8437 | 0.7074 | 0.6408 |
| GPT-4.1 mini, one draw (t = 0) | 0.7167 | 0.7399 | 0.7763 | 0.6712 | 0.6360 |
| GPT-4.1 mini, five draws (Table 1's row) | 0.7648 | 0.7889 | 0.8211 | 0.7217 | 0.6716 |
| Haiku 4.5 | 0.7566 | 0.7973 | 0.8265 | 0.7029 | 0.6701 |
| GPT-5.6 Luna | 0.8417 | 0.8480 | 0.8749 | 0.8165 | 0.7017 |
| GPT-5.6 Sol | 0.8500 | 0.8446 | 0.8724 | 0.8330 | 0.7036 |
| Opus 5 | 0.8405 | 0.8834 | 0.8698 | 0.8178 | 0.7116 |
| Haiku 4.5, draw 1 | 0.7555 | 0.7787 | 0.8254 | 0.7021 | 0.6752 |
| GPT-5.6 Luna, draw 1 | 0.8265 | 0.8328 | 0.8520 | 0.8071 | 0.6875 |
| GPT-5.6 Sol, draw 1 | 0.8277 | 0.8057 | 0.8418 | 0.8171 | 0.6879 |
| Opus 5, draw 1 | 0.8400 | 0.8767 | 0.8693 | 0.8173 | 0.7115 |
| GPT-4.1 mini, draw 1 of five | 0.7257 | 0.7483 | 0.7903 | 0.6762 | 0.6399 |
| Count reader, guessed category | 0.6623 | 0.7044 | 0.6603 | 0.6633 | 0.6705 |
| Count reader, given category | 0.6043 | 0.7027 | 0.5455 | 0.6478 | 0.6695 |
| State-aware count reader | 0.8580 | 1.0000 | 0.8867 | 0.8344 | 0.8576 |
| Totals reader | 0.5603 | 0.7061 | 0.5304 | 0.5813 | 0.6099 |
| Category-given share reader (privileged) | 0.8473 | 0.9932 | 0.8765 | 0.8234 | 0.8282 |
| Whole name-map lookup | 0.5776 | 0.6030 | 0.5744 | 0.5797 | 0.5802 |
| Hybrid reader (E10) | 0.7865 | 0.8682 | 0.8471 | 0.7394 | 0.6967 |
| Random-token lookup | 0.5954 | 0.6453 | 0.6338 | 0.5657 | 0.5550 |
| Name lookup, all-mpnet-base-v2 | 0.7605 | 0.7736 | 0.8382 | 0.7012 | 0.6385 |
| Name lookup, bge-small-en-v1.5 | 0.7584 | 0.7804 | 0.8420 | 0.6946 | 0.6401 |
| GPT-5.6 Luna, intent-explicit rubric | 0.8531 | 0.8598 | 0.8852 | 0.8286 | 0.7271 |
| GPT-4.1 mini, intent-explicit rubric | 0.7253 | 0.7280 | 0.7944 | 0.6727 | 0.6268 |
| Haiku 4.5, names only (E2) | 0.7507 | 0.7922 | 0.8380 | 0.6838 | 0.6761 |
| Haiku 4.5, counts only (E2) | 0.5945 | 0.6436 | 0.6132 | 0.5796 | 0.5686 |
| GPT-4.1 mini, names only (E2) | 0.7103 | 0.7348 | 0.7934 | 0.6469 | 0.6305 |
| GPT-4.1 mini, names only, dash rule (E2) | 0.6891 | 0.7010 | 0.7726 | 0.6255 | 0.5899 |
| GPT-4.1 mini, counts only (E2) | 0.5862 | 0.5895 | 0.5993 | 0.5762 | 0.5698 |

### v3: the pooled AUROC decomposed by pair class (whole set; pair counts within-triple 296, same-state across questions 18,792, across states 24,720 of 43,808)

| reader | pooled | within-triple (296) | same state, across questions (18,792) | across states (24,720) | state-balanced pooled |
|---|---:|---:|---:|---:|---:|
| All-states lookup | 0.8756 | 0.9155 | 0.8868 | 0.8667 | 0.8560 |
| GPT-4.1 mini, one draw (t = 0) | 0.7967 | 0.8311 | 0.8227 | 0.7766 | 0.7679 |
| GPT-4.1 mini, five draws (Table 1's row) | 0.8323 | 0.8868 | 0.8589 | 0.8115 | 0.7994 |
| Haiku 4.5 | 0.8773 | 0.9105 | 0.8810 | 0.8742 | 0.8721 |
| Opus 5 | 0.9079 | 0.9493 | 0.9195 | 0.8986 | 0.8895 |
| Opus 5, draw 1 | 0.9029 | 0.9527 | 0.9134 | 0.8943 | 0.8789 |
| GPT-4.1 mini, draw 1 of five | 0.8029 | 0.8277 | 0.8290 | 0.7826 | 0.7676 |
| Random-token lookup | 0.5479 | 0.6064 | 0.5434 | 0.5506 | 0.5592 |
| All-states lookup, all-mpnet-base-v2 | 0.8646 | 0.9189 | 0.8723 | 0.8582 | 0.8517 |
| All-states lookup, bge-small-en-v1.5 | 0.8690 | 0.9257 | 0.8742 | 0.8644 | 0.8617 |

### v2r: the pooled AUROC decomposed by pair class (whole set; pair counts within-triple 296, same-state across questions 18,792, across states 24,720 of 43,808)

| reader | pooled | within-triple (296) | same state, across questions (18,792) | across states (24,720) | state-balanced pooled |
|---|---:|---:|---:|---:|---:|
| GPT-4.1 mini, one draw (t = 0) | 0.7179 | 0.7297 | 0.7857 | 0.6661 | 0.6198 |
| Haiku 4.5 | 0.7638 | 0.7939 | 0.8308 | 0.7124 | 0.6855 |
| Opus 5 | 0.8353 | 0.8767 | 0.8673 | 0.8106 | 0.7032 |
| Totals reader (the permuted lines) | 0.4472 | 0.4172 | 0.4630 | 0.4354 | 0.4238 |
| Count reader, given category (unchanged) | 0.6043 | 0.7027 | 0.5455 | 0.6478 | 0.6695 |
| Count reader, guessed category (unchanged) | 0.6623 | 0.7044 | 0.6603 | 0.6633 | 0.6705 |

### v2rcat: the pooled AUROC decomposed by pair class (whole set; pair counts within-triple 296, same-state across questions 18,792, across states 24,720 of 43,808)

| reader | pooled | within-triple (296) | same state, across questions (18,792) | across states (24,720) | state-balanced pooled |
|---|---:|---:|---:|---:|---:|
| GPT-4.1 mini, one draw | 0.7410 | 0.7500 | 0.7911 | 0.7027 | 0.6680 |
| Haiku 4.5, five draws | 0.7525 | 0.7686 | 0.8217 | 0.6996 | 0.6525 |
| Opus 5, five draws (E1 Amendment 1) | 0.8075 | 0.7787 | 0.8485 | 0.7767 | 0.6350 |
| Opus 5, draw 1 | 0.8049 | 0.7601 | 0.8484 | 0.7723 | 0.6359 |
| GPT-5.6 Luna, five draws (E9) | 0.8121 | 0.7568 | 0.8580 | 0.7778 | 0.6406 |
| GPT-5.6 Luna, draw 1 | 0.8150 | 0.7821 | 0.8561 | 0.7841 | 0.6661 |
| GPT-5.6 Sol, five draws (E9) | 0.8172 | 0.7568 | 0.8515 | 0.7919 | 0.6287 |
| GPT-5.6 Sol, draw 1 | 0.8024 | 0.7314 | 0.8313 | 0.7812 | 0.6072 |
| State-aware count reader | 0.6520 | 0.6959 | 0.7949 | 0.5429 | 0.5215 |
| Totals reader | 0.4472 | 0.4172 | 0.4630 | 0.4354 | 0.4238 |
| Count reader, given category | 0.4585 | 0.4139 | 0.4836 | 0.4400 | 0.4383 |
| Count reader, guessed category | 0.5914 | 0.5794 | 0.6259 | 0.5654 | 0.5439 |
| Category-given share reader | 0.6741 | 0.6655 | 0.7974 | 0.5804 | 0.5349 |

### AUX-CF2-R125-VS-LOOKUP — each reader minus its summary's lookup

### all summaries: each reader minus its summary's lookup under the matched metric, PN vs PRESENT (whole set; supersession only; the counted states beside), triple and persona intervals

| reader | lookup | whole Δ | triple | persona | reliable | sup Δ | triple | persona | reliable | ret Δ | exp Δ | PN vs ABSENT whole Δ | triple | persona | reliable |
|---|---|---:|---|---|---|---:|---|---|---|---:|---:|---:|---|---|---|
| GPT-4.1 mini, one draw (t = 0) | LOOKUP_v2 | -0.0372 | [-0.0811, +0.0068] | [-0.0877, +0.0146] | no | -0.0852 | [-0.1307, -0.0398] | [-0.1420, -0.0294] | **reliable** | +0.0500 | +0.0167 | -0.0372 | [-0.0744, +0.0034] | [-0.0775, +0.0036] | no |
| GPT-4.1 mini, five draws (Table 1's row) | LOOKUP_v2 | -0.0507 | [-0.1115, +0.0101] | [-0.1069, +0.0000] | no | -0.0739 | [-0.1307, -0.0227] | [-0.1393, -0.0214] | **reliable** | +0.0667 | -0.1000 | +0.0743 | [+0.0169, +0.1318] | [+0.0288, +0.1179] | **reliable** |
| Haiku 4.5 | LOOKUP_v2 | +0.0000 | [-0.0439, +0.0372] | [-0.0528, +0.0483] | no | -0.0511 | [-0.1136, +0.0000] | [-0.1084, +0.0000] | no | +0.0667 | +0.0833 | +0.0405 | [+0.0000, +0.0777] | [-0.0065, +0.0859] | no |
| GPT-5.6 Luna | LOOKUP_v2 | +0.1014 | [+0.0473, +0.1554] | [+0.0442, +0.1533] | **reliable** | -0.0057 | [-0.0341, +0.0227] | [-0.0321, +0.0174] | no | +0.1500 | +0.3667* | +0.0405 | [-0.0102, +0.0946] | [-0.0194, +0.0987] | no |
| GPT-5.6 Sol | LOOKUP_v2 | +0.0811 | [+0.0270, +0.1351] | [+0.0283, +0.1319] | **reliable** | -0.0057 | [-0.0511, +0.0341] | [-0.0417, +0.0287] | no | +0.0833 | +0.3333* | +0.0541 | [+0.0000, +0.1081] | [-0.0032, +0.1130] | no |
| Opus 5 | LOOKUP_v2 | +0.0980 | [+0.0472, +0.1454] | [+0.0435, +0.1503] | **reliable** | +0.0114 | [-0.0227, +0.0455] | [-0.0284, +0.0579] | no | +0.2667* | +0.1833 | +0.1149 | [+0.0642, +0.1622] | [+0.0588, +0.1648] | **reliable** |
| Haiku 4.5, draw 1 | LOOKUP_v2 | -0.0135 | [-0.0507, +0.0236] | [-0.0560, +0.0198] | no | -0.0625 | [-0.1136, -0.0170] | [-0.1183, -0.0163] | **reliable** | +0.0833* | +0.0333 | +0.0169 | [-0.0203, +0.0541] | [-0.0262, +0.0552] | no |
| GPT-5.6 Luna, draw 1 | LOOKUP_v2 | +0.0642 | [+0.0135, +0.1182] | [+0.0292, +0.1040] | **reliable** | -0.0341 | [-0.0625, -0.0057] | [-0.0581, -0.0118] | **reliable** | +0.2000* | +0.2167* | +0.0473 | [-0.0034, +0.0980] | [-0.0033, +0.0921] | no |
| GPT-5.6 Sol, draw 1 | LOOKUP_v2 | +0.0338 | [-0.0236, +0.0878] | [-0.0203, +0.0828] | no | -0.0170 | [-0.0625, +0.0170] | [-0.0538, +0.0172] | no | +0.0667 | +0.1500 | +0.0236 | [-0.0338, +0.0812] | [-0.0280, +0.0745] | no |
| Opus 5, draw 1 | LOOKUP_v2 | +0.0912 | [+0.0439, +0.1385] | [+0.0273, +0.1485] | **reliable** | +0.0057 | [-0.0284, +0.0341] | [-0.0298, +0.0413] | no | +0.2333* | +0.2000* | +0.1081 | [+0.0574, +0.1588] | [+0.0658, +0.1548] | **reliable** |
| GPT-4.1 mini, draw 1 of five | LOOKUP_v2 | -0.0541 | [-0.1014, +0.0000] | [-0.1051, -0.0034] | disagree | -0.0852 | [-0.1420, -0.0284] | [-0.1505, -0.0303] | **reliable** | +0.0500 | -0.0667 | -0.0034 | [-0.0507, +0.0439] | [-0.0526, +0.0448] | no |
| Count reader, guessed category | LOOKUP_v2 | -0.0574 | [-0.1149, +0.0034] | [-0.1186, +0.0001] | no | -0.2727 | [-0.3240, -0.2159] | [-0.3350, -0.2088] | **reliable** | +0.2667* | +0.2500* | -0.0878 | [-0.1486, -0.0270] | [-0.1446, -0.0294] | **reliable** |
| Count reader, given category | LOOKUP_v2 | -0.0743 | [-0.1554, +0.0034] | [-0.1550, +0.0074] | no | -0.4659 | [-0.4886, -0.4375] | [-0.4944, -0.4286] | **reliable** | +0.5000* | +0.5000* | -0.0743 | [-0.1554, +0.0034] | [-0.1550, +0.0074] | no |
| State-aware count reader | LOOKUP_v2 | +0.2230 | [+0.1824, +0.2635] | [+0.1812, +0.2654] | **reliable** | +0.0341 | [+0.0114, +0.0625] | [+0.0056, +0.0714] | **reliable** | +0.5000* | +0.5000* | +0.2230 | [+0.1824, +0.2635] | [+0.1812, +0.2654] | **reliable** |
| Totals reader | LOOKUP_v2 | -0.0743 | [-0.1554, +0.0034] | [-0.1550, +0.0074] | no | -0.4659 | [-0.4886, -0.4375] | [-0.4944, -0.4286] | **reliable** | +0.5000* | +0.5000* | -0.0676 | [-0.1486, +0.0101] | [-0.1484, +0.0180] | no |
| Category-given share reader (privileged) | LOOKUP_v2 | +0.2230 | [+0.1824, +0.2635] | [+0.1812, +0.2654] | **reliable** | +0.0341 | [+0.0114, +0.0625] | [+0.0056, +0.0714] | **reliable** | +0.5000* | +0.5000* | +0.2095 | [+0.1622, +0.2534] | [+0.1606, +0.2543] | **reliable** |
| Whole name-map lookup | LOOKUP_v2 | -0.2770 | [-0.3176, -0.2365] | [-0.3188, -0.2346] | **reliable** | -0.4659 | [-0.4886, -0.4375] | [-0.4944, -0.4286] | **reliable** | +0.0000 | +0.0000 | -0.0709 | [-0.1284, -0.0168] | [-0.1316, -0.0097] | **reliable** |
| Hybrid reader (E10) | LOOKUP_v2 | +0.1081 | [+0.0777, +0.1419] | [+0.0741, +0.1419] | **reliable** | +0.0057 | [+0.0000, +0.0170] | [+0.0000, +0.0179] | no | +0.2667* | +0.2500* | +0.0743 | [+0.0338, +0.1149] | [+0.0357, +0.1149] | **reliable** |
| Random-token lookup | LOOKUP_v2 | -0.1318 | [-0.1724, -0.0912] | [-0.1786, -0.0854] | **reliable** | -0.2216 | [-0.2841, -0.1646] | [-0.2889, -0.1506] | **reliable** | +0.0000 | +0.0000 | -0.1318 | [-0.1724, -0.0912] | [-0.1786, -0.0854] | **reliable** |
| Name lookup, all-mpnet-base-v2 | LOOKUP_v2 | -0.0034 | [-0.0101, +0.0000] | [-0.0115, +0.0000] | no | -0.0057 | [-0.0170, +0.0000] | [-0.0185, +0.0000] | no | +0.0000 | +0.0000 | -0.0034 | [-0.0101, +0.0000] | [-0.0115, +0.0000] | no |
| Name lookup, bge-small-en-v1.5 | LOOKUP_v2 | +0.0034 | [+0.0000, +0.0101] | [+0.0000, +0.0106] | no | +0.0057 | [+0.0000, +0.0170] | [+0.0000, +0.0206] | no | +0.0000 | +0.0000 | +0.0034 | [+0.0000, +0.0101] | [+0.0000, +0.0106] | no |
| GPT-5.6 Luna, intent-explicit rubric | LOOKUP_v2 | +0.0709 | [+0.0169, +0.1250] | [+0.0103, +0.1258] | **reliable** | -0.0170 | [-0.0513, +0.0114] | [-0.0465, +0.0108] | no | +0.1333 | +0.2667* | +0.0946 | [+0.0405, +0.1486] | [+0.0374, +0.1460] | **reliable** |
| GPT-4.1 mini, intent-explicit rubric | LOOKUP_v2 | -0.0608 | [-0.1047, -0.0169] | [-0.1129, -0.0171] | **reliable** | -0.0909 | [-0.1422, -0.0455] | [-0.1471, -0.0353] | **reliable** | +0.0333 | -0.0667 | -0.0372 | [-0.0743, +0.0034] | [-0.0803, +0.0035] | no |
| Haiku 4.5, names only (E2) | LOOKUP_v2 | -0.0034 | [-0.0304, +0.0270] | [-0.0381, +0.0281] | no | -0.0341 | [-0.0625, +0.0000] | [-0.0698, -0.0052] | disagree | +0.0167 | +0.0667 | +0.0338 | [-0.0034, +0.0743] | [-0.0039, +0.0671] | no |
| Haiku 4.5, counts only (E2) | LOOKUP_v2 | -0.1419 | [-0.2028, -0.0811] | [-0.2094, -0.0769] | **reliable** | -0.2500 | [-0.3352, -0.1705] | [-0.3517, -0.1500] | **reliable** | +0.0833 | -0.0500 | -0.1250 | [-0.1858, -0.0641] | [-0.1759, -0.0653] | **reliable** |
| GPT-4.1 mini, names only (E2) | LOOKUP_v2 | -0.0372 | [-0.0676, -0.0068] | [-0.0704, -0.0033] | **reliable** | -0.0795 | [-0.1250, -0.0341] | [-0.1235, -0.0368] | **reliable** | +0.0500 | +0.0000 | -0.0473 | [-0.0845, -0.0135] | [-0.0867, -0.0130] | **reliable** |
| GPT-4.1 mini, names only, dash rule (E2) | LOOKUP_v2 | -0.0878 | [-0.1250, -0.0473] | [-0.1299, -0.0458] | **reliable** | -0.1136 | [-0.1705, -0.0625] | [-0.1582, -0.0707] | **reliable** | -0.0500 | -0.0500 | -0.0642 | [-0.1014, -0.0303] | [-0.0940, -0.0333] | **reliable** |
| GPT-4.1 mini, counts only (E2) | LOOKUP_v2 | -0.1723 | [-0.2331, -0.1149] | [-0.2230, -0.1250] | **reliable** | -0.3125 | [-0.3807, -0.2500] | [-0.3766, -0.2500] | **reliable** | +0.1167 | -0.0500 | -0.2027 | [-0.2635, -0.1453] | [-0.2724, -0.1363] | **reliable** |
| GPT-4.1 mini, one draw (t = 0) | ALLSTATES_v3 | -0.0912 | [-0.1454, -0.0439] | [-0.1654, -0.0246] | **reliable** | -0.0682 | [-0.1250, -0.0226] | [-0.1478, -0.0105] | **reliable** | +0.1167 | -0.3667* | -0.0777 | [-0.1216, -0.0372] | [-0.1314, -0.0290] | **reliable** |
| GPT-4.1 mini, five draws (Table 1's row) | ALLSTATES_v3 | -0.0135 | [-0.0642, +0.0338] | [-0.0698, +0.0375] | no | -0.0227 | [-0.0795, +0.0342] | [-0.0886, +0.0337] | no | +0.1167 | -0.1167 | -0.0439 | [-0.0980, +0.0068] | [-0.1049, +0.0035] | no |
| Haiku 4.5 | ALLSTATES_v3 | -0.0034 | [-0.0439, +0.0372] | [-0.0476, +0.0333] | no | -0.0511 | [-0.1080, +0.0000] | [-0.1123, +0.0054] | no | +0.1167* | +0.0167 | -0.0068 | [-0.0507, +0.0372] | [-0.0517, +0.0350] | no |
| Opus 5 | ALLSTATES_v3 | +0.0304 | [-0.0068, +0.0643] | [-0.0038, +0.0648] | no | +0.0227 | [-0.0114, +0.0568] | [-0.0105, +0.0550] | no | +0.0167 | +0.0667 | +0.0372 | [+0.0034, +0.0709] | [+0.0000, +0.0750] | disagree |
| Opus 5, draw 1 | ALLSTATES_v3 | +0.0372 | [+0.0033, +0.0709] | [+0.0076, +0.0662] | **reliable** | +0.0398 | [+0.0170, +0.0682] | [+0.0118, +0.0714] | **reliable** | +0.0000 | +0.0667 | +0.0372 | [+0.0000, +0.0743] | [-0.0036, +0.0761] | no |
| GPT-4.1 mini, draw 1 of five | ALLSTATES_v3 | -0.0709 | [-0.1216, -0.0236] | [-0.1267, -0.0250] | **reliable** | -0.0795 | [-0.1364, -0.0227] | [-0.1530, -0.0222] | **reliable** | +0.0333 | -0.1500* | -0.1047 | [-0.1588, -0.0541] | [-0.1528, -0.0604] | **reliable** |
| Random-token lookup | ALLSTATES_v3 | -0.3041 | [-0.3447, -0.2568] | [-0.3493, -0.2516] | **reliable** | -0.3466 | [-0.3977, -0.2955] | [-0.3987, -0.2903] | **reliable** | -0.2667* | -0.2167* | -0.3142 | [-0.3581, -0.2669] | [-0.3611, -0.2601] | **reliable** |
| All-states lookup, all-mpnet-base-v2 | ALLSTATES_v3 | +0.0034 | [-0.0101, +0.0169] | [-0.0126, +0.0179] | no | +0.0000 | [-0.0170, +0.0170] | [-0.0174, +0.0167] | no | +0.0000 | +0.0167 | +0.0034 | [-0.0135, +0.0203] | [-0.0159, +0.0206] | no |
| All-states lookup, bge-small-en-v1.5 | ALLSTATES_v3 | +0.0068 | [-0.0101, +0.0236] | [-0.0075, +0.0234] | no | +0.0000 | [-0.0227, +0.0227] | [-0.0241, +0.0222] | no | +0.0000 | +0.0333 | +0.0135 | [-0.0068, +0.0338] | [-0.0035, +0.0318] | no |
| GPT-4.1 mini, one draw (t = 0) | LOOKUP_v2 | -0.0811 | [-0.1250, -0.0405] | [-0.1266, -0.0387] | **reliable** | -0.0909 | [-0.1420, -0.0398] | [-0.1364, -0.0455] | **reliable** | -0.1000 | -0.0333 | -0.0135 | [-0.0574, +0.0270] | [-0.0567, +0.0284] | no |
| Haiku 4.5 | LOOKUP_v2 | -0.0068 | [-0.0474, +0.0339] | [-0.0549, +0.0411] | no | -0.0682 | [-0.1250, -0.0170] | [-0.1193, -0.0220] | **reliable** | +0.1167 | +0.0500 | +0.0405 | [+0.0000, +0.0812] | [-0.0034, +0.0860] | no |
| Opus 5 | LOOKUP_v2 | +0.0878 | [+0.0372, +0.1419] | [+0.0345, +0.1471] | **reliable** | +0.0000 | [-0.0398, +0.0341] | [-0.0313, +0.0298] | no | +0.1667 | +0.2667* | +0.1115 | [+0.0574, +0.1622] | [+0.0625, +0.1635] | **reliable** |
| Totals reader (the permuted lines) | LOOKUP_v2 | -0.3716 | [-0.4359, -0.3073] | [-0.4354, -0.3070] | **reliable** | -0.5057 | [-0.5682, -0.4432] | [-0.5625, -0.4529] | **reliable** | -0.1333 | -0.2167* | -0.3480 | [-0.4189, -0.2804] | [-0.4291, -0.2685] | **reliable** |
| Count reader, given category (unchanged) | LOOKUP_v2 | -0.0743 | [-0.1554, +0.0034] | [-0.1550, +0.0074] | no | -0.4659 | [-0.4886, -0.4375] | [-0.4944, -0.4286] | **reliable** | +0.5000* | +0.5000* | -0.0743 | [-0.1554, +0.0034] | [-0.1550, +0.0074] | no |
| Count reader, guessed category (unchanged) | LOOKUP_v2 | -0.0574 | [-0.1149, +0.0034] | [-0.1186, +0.0001] | no | -0.2727 | [-0.3240, -0.2159] | [-0.3350, -0.2088] | **reliable** | +0.2667* | +0.2500* | -0.0878 | [-0.1486, -0.0270] | [-0.1446, -0.0294] | **reliable** |
| GPT-4.1 mini, one draw | LOOKUP_v2 | -0.0405 | [-0.0845, +0.0034] | [-0.0856, +0.0032] | no | -0.1023 | [-0.1534, -0.0511] | [-0.1611, -0.0460] | **reliable** | +0.0500 | +0.0500 | -0.0135 | [-0.0609, +0.0271] | [-0.0714, +0.0417] | no |
| Haiku 4.5, five draws | LOOKUP_v2 | -0.0304 | [-0.0743, +0.0101] | [-0.0769, +0.0172] | no | -0.0682 | [-0.1307, -0.0170] | [-0.1221, -0.0170] | **reliable** | +0.0667 | -0.0167 | +0.0135 | [-0.0304, +0.0574] | [-0.0282, +0.0625] | no |
| Opus 5, five draws (E1 Amendment 1) | LOOKUP_v2 | -0.0372 | [-0.0913, +0.0203] | [-0.0985, +0.0253] | no | -0.0227 | [-0.0682, +0.0114] | [-0.0606, +0.0114] | no | -0.1000 | -0.0167 | +0.0405 | [-0.0169, +0.0946] | [-0.0082, +0.0940] | no |
| Opus 5, draw 1 | LOOKUP_v2 | -0.0270 | [-0.0845, +0.0270] | [-0.0822, +0.0263] | no | -0.0398 | [-0.0854, +0.0057] | [-0.0852, +0.0000] | no | -0.0667 | +0.0500 | -0.0068 | [-0.0574, +0.0473] | [-0.0458, +0.0306] | no |
| GPT-5.6 Luna, five draws (E9) | LOOKUP_v2 | -0.0101 | [-0.0608, +0.0439] | [-0.0559, +0.0380] | no | +0.0057 | [-0.0170, +0.0284] | [-0.0116, +0.0281] | no | -0.1667 | +0.1000 | -0.0304 | [-0.0912, +0.0236] | [-0.0891, +0.0240] | no |
| GPT-5.6 Luna, draw 1 | LOOKUP_v2 | +0.0135 | [-0.0439, +0.0676] | [-0.0442, +0.0710] | no | -0.0284 | [-0.0682, +0.0057] | [-0.0598, +0.0000] | no | +0.0333 | +0.1167 | -0.0034 | [-0.0608, +0.0507] | [-0.0584, +0.0493] | no |
| GPT-5.6 Sol, five draws (E9) | LOOKUP_v2 | -0.0507 | [-0.1047, +0.0034] | [-0.1067, +0.0077] | no | -0.0057 | [-0.0398, +0.0284] | [-0.0376, +0.0220] | no | -0.1000 | -0.1333 | +0.0101 | [-0.0439, +0.0676] | [-0.0438, +0.0544] | no |
| GPT-5.6 Sol, draw 1 | LOOKUP_v2 | -0.0507 | [-0.1047, +0.0068] | [-0.1119, +0.0069] | no | -0.0284 | [-0.0739, +0.0114] | [-0.0729, +0.0171] | no | -0.0333 | -0.1333 | -0.0405 | [-0.0946, +0.0203] | [-0.0979, +0.0133] | no |
| State-aware count reader | LOOKUP_v2 | -0.0709 | [-0.1081, -0.0372] | [-0.1092, -0.0274] | **reliable** | +0.0341 | [+0.0114, +0.0625] | [+0.0056, +0.0714] | **reliable** | -0.2333* | -0.2167* | -0.0912 | [-0.1318, -0.0541] | [-0.1284, -0.0510] | **reliable** |
| Totals reader | LOOKUP_v2 | -0.3716 | [-0.4359, -0.3073] | [-0.4354, -0.3070] | **reliable** | -0.5057 | [-0.5682, -0.4432] | [-0.5625, -0.4529] | **reliable** | -0.1333 | -0.2167* | -0.3480 | [-0.4189, -0.2804] | [-0.4291, -0.2685] | **reliable** |
| Count reader, given category | LOOKUP_v2 | -0.3682 | [-0.4054, -0.3311] | [-0.4040, -0.3312] | **reliable** | -0.4659 | [-0.4886, -0.4375] | [-0.4944, -0.4286] | **reliable** | -0.2333* | -0.2167* | -0.3581 | [-0.4020, -0.3176] | [-0.3958, -0.3206] | **reliable** |
| Count reader, guessed category | LOOKUP_v2 | -0.2196 | [-0.2602, -0.1791] | [-0.2700, -0.1720] | **reliable** | -0.2727 | [-0.3240, -0.2159] | [-0.3350, -0.2088] | **reliable** | -0.2333* | -0.0500 | -0.1757 | [-0.2297, -0.1250] | [-0.2295, -0.1250] | **reliable** |
| Category-given share reader | LOOKUP_v2 | -0.1081 | [-0.1520, -0.0709] | [-0.1429, -0.0669] | **reliable** | +0.0341 | [+0.0114, +0.0625] | [+0.0056, +0.0714] | **reliable** | -0.4167* | -0.2167* | -0.1149 | [-0.1622, -0.0676] | [-0.1618, -0.0667] | **reliable** |

### AUX-CF2-R125-VS-COUNT — each reader minus each count reader on the counted states

### all summaries: each reader minus each count reader on retraction and on expiry, matched PN vs PRESENT (Δ; triple interval; persona interval; * = both intervals exclude zero)

| reader | minus guessed category: ret | exp | minus given category: ret | exp | minus state-aware: ret | exp | minus totals: ret | exp | minus given share: ret | exp |
|---|---|---|---|---|---|---|---|---|---|---|
| Name lookup | -0.2667* [-0.3500, -0.1833] [-0.3519, -0.1897] | -0.2500* [-0.3333, -0.1667] [-0.3261, -0.1613] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] |
| GPT-4.1 mini, one draw (t = 0) | -0.2167* [-0.3833, -0.0500] [-0.3750, -0.0625] | -0.2333* [-0.3504, -0.1167] [-0.3462, -0.1199] | -0.4500* [-0.5667, -0.3333] [-0.5600, -0.3448] | -0.4833* [-0.5667, -0.4000] [-0.5893, -0.3548] | -0.4500* [-0.5667, -0.3333] [-0.5600, -0.3448] | -0.4833* [-0.5667, -0.4000] [-0.5893, -0.3548] | -0.4500* [-0.5667, -0.3333] [-0.5600, -0.3448] | -0.4833* [-0.5667, -0.4000] [-0.5893, -0.3548] | -0.4500* [-0.5667, -0.3333] [-0.5600, -0.3448] | -0.4833* [-0.5667, -0.4000] [-0.5893, -0.3548] |
| GPT-4.1 mini, five draws (Table 1's row) | -0.2000* [-0.3671, -0.0167] [-0.4194, -0.0139] | -0.3500* [-0.5167, -0.1833] [-0.5167, -0.2069] | -0.4333* [-0.6000, -0.2667] [-0.6094, -0.2586] | -0.6000* [-0.7500, -0.4500] [-0.7143, -0.4857] | -0.4333* [-0.6000, -0.2667] [-0.6094, -0.2586] | -0.6000* [-0.7500, -0.4500] [-0.7143, -0.4857] | -0.4333* [-0.6000, -0.2667] [-0.6094, -0.2586] | -0.6000* [-0.7500, -0.4500] [-0.7143, -0.4857] | -0.4333* [-0.6000, -0.2667] [-0.6094, -0.2586] | -0.6000* [-0.7500, -0.4500] [-0.7143, -0.4857] |
| Haiku 4.5 | -0.2000* [-0.3167, -0.0667] [-0.3089, -0.0769] | -0.1667* [-0.3000, -0.0500] [-0.2904, -0.0151] | -0.4333* [-0.5167, -0.3500] [-0.5175, -0.3393] | -0.4167* [-0.5004, -0.3167] [-0.5312, -0.2884] | -0.4333* [-0.5167, -0.3500] [-0.5175, -0.3393] | -0.4167* [-0.5004, -0.3167] [-0.5312, -0.2884] | -0.4333* [-0.5167, -0.3500] [-0.5175, -0.3393] | -0.4167* [-0.5004, -0.3167] [-0.5312, -0.2884] | -0.4333* [-0.5167, -0.3500] [-0.5175, -0.3393] | -0.4167* [-0.5004, -0.3167] [-0.5312, -0.2884] |
| GPT-5.6 Luna | -0.1167 [-0.3333, +0.1167] [-0.3336, +0.0770] | +0.1167 [-0.0333, +0.2500] [-0.0156, +0.2586] | -0.3500* [-0.5167, -0.1833] [-0.5485, -0.1786] | -0.1333* [-0.2667, -0.0333] [-0.2414, -0.0323] | -0.3500* [-0.5167, -0.1833] [-0.5485, -0.1786] | -0.1333* [-0.2667, -0.0333] [-0.2414, -0.0323] | -0.3500* [-0.5167, -0.1833] [-0.5485, -0.1786] | -0.1333* [-0.2667, -0.0333] [-0.2414, -0.0323] | -0.3500* [-0.5167, -0.1833] [-0.5485, -0.1786] | -0.1333* [-0.2667, -0.0333] [-0.2414, -0.0323] |
| GPT-5.6 Sol | -0.1833 [-0.3500, +0.0000] [-0.3519, -0.0284] | +0.0833 [-0.0504, +0.2167] [-0.0653, +0.2143] | -0.4167* [-0.5833, -0.2500] [-0.5893, -0.2500] | -0.1667* [-0.3000, -0.0333] [-0.3000, -0.0606] | -0.4167* [-0.5833, -0.2500] [-0.5893, -0.2500] | -0.1667* [-0.3000, -0.0333] [-0.3000, -0.0606] | -0.4167* [-0.5833, -0.2500] [-0.5893, -0.2500] | -0.1667* [-0.3000, -0.0333] [-0.3000, -0.0606] | -0.4167* [-0.5833, -0.2500] [-0.5893, -0.2500] | -0.1667* [-0.3000, -0.0333] [-0.3000, -0.0606] |
| Opus 5 | +0.0000 [-0.1833, +0.1833] [-0.1966, +0.1757] | -0.0667 [-0.2504, +0.1167] [-0.2834, +0.1379] | -0.2333* [-0.3833, -0.1000] [-0.3889, -0.0882] | -0.3167* [-0.4833, -0.1667] [-0.5000, -0.1250] | -0.2333* [-0.3833, -0.1000] [-0.3889, -0.0882] | -0.3167* [-0.4833, -0.1667] [-0.5000, -0.1250] | -0.2333* [-0.3833, -0.1000] [-0.3889, -0.0882] | -0.3167* [-0.4833, -0.1667] [-0.5000, -0.1250] | -0.2333* [-0.3833, -0.1000] [-0.3889, -0.0882] | -0.3167* [-0.4833, -0.1667] [-0.5000, -0.1250] |
| Haiku 4.5, draw 1 | -0.1833* [-0.2833, -0.0667] [-0.2778, -0.0893] | -0.2167* [-0.3167, -0.1000] [-0.3088, -0.1154] | -0.4167* [-0.4833, -0.3496] [-0.4737, -0.3400] | -0.4667* [-0.5667, -0.3667] [-0.5303, -0.4000] | -0.4167* [-0.4833, -0.3496] [-0.4737, -0.3400] | -0.4667* [-0.5667, -0.3667] [-0.5303, -0.4000] | -0.4167* [-0.4833, -0.3496] [-0.4737, -0.3400] | -0.4667* [-0.5667, -0.3667] [-0.5303, -0.4000] | -0.4167* [-0.4833, -0.3496] [-0.4737, -0.3400] | -0.4667* [-0.5667, -0.3667] [-0.5303, -0.4000] |
| GPT-5.6 Luna, draw 1 | -0.0667 [-0.2837, +0.1333] [-0.2858, +0.1291] | -0.0333 [-0.2000, +0.1167] [-0.1552, +0.0926] | -0.3000* [-0.4667, -0.1333] [-0.4828, -0.1378] | -0.2833* [-0.4333, -0.1496] [-0.3751, -0.1818] | -0.3000* [-0.4667, -0.1333] [-0.4828, -0.1378] | -0.2833* [-0.4333, -0.1496] [-0.3751, -0.1818] | -0.3000* [-0.4667, -0.1333] [-0.4828, -0.1378] | -0.2833* [-0.4333, -0.1496] [-0.3751, -0.1818] | -0.3000* [-0.4667, -0.1333] [-0.4828, -0.1378] | -0.2833* [-0.4333, -0.1496] [-0.3751, -0.1818] |
| GPT-5.6 Sol, draw 1 | -0.2000 [-0.3833, -0.0167] [-0.3826, +0.0000] | -0.1000 [-0.2667, +0.0667] [-0.2693, +0.0782] | -0.4333* [-0.6000, -0.2833] [-0.5962, -0.2586] | -0.3500* [-0.5167, -0.1833] [-0.5179, -0.1935] | -0.4333* [-0.6000, -0.2833] [-0.5962, -0.2586] | -0.3500* [-0.5167, -0.1833] [-0.5179, -0.1935] | -0.4333* [-0.6000, -0.2833] [-0.5962, -0.2586] | -0.3500* [-0.5167, -0.1833] [-0.5179, -0.1935] | -0.4333* [-0.6000, -0.2833] [-0.5962, -0.2586] | -0.3500* [-0.5167, -0.1833] [-0.5179, -0.1935] |
| Opus 5, draw 1 | -0.0333 [-0.2000, +0.1333] [-0.2222, +0.1286] | -0.0500 [-0.2167, +0.1167] [-0.2258, +0.1167] | -0.2667* [-0.4167, -0.1500] [-0.4038, -0.1406] | -0.3000* [-0.4500, -0.1500] [-0.4667, -0.1400] | -0.2667* [-0.4167, -0.1500] [-0.4038, -0.1406] | -0.3000* [-0.4500, -0.1500] [-0.4667, -0.1400] | -0.2667* [-0.4167, -0.1500] [-0.4038, -0.1406] | -0.3000* [-0.4500, -0.1500] [-0.4667, -0.1400] | -0.2667* [-0.4167, -0.1500] [-0.4038, -0.1406] | -0.3000* [-0.4500, -0.1500] [-0.4667, -0.1400] |
| GPT-4.1 mini, draw 1 of five | -0.2167* [-0.4000, -0.0667] [-0.3889, -0.0689] | -0.3167* [-0.4500, -0.1833] [-0.4808, -0.1714] | -0.4500* [-0.5833, -0.3167] [-0.5863, -0.3235] | -0.5667* [-0.7000, -0.4333] [-0.7223, -0.3999] | -0.4500* [-0.5833, -0.3167] [-0.5863, -0.3235] | -0.5667* [-0.7000, -0.4333] [-0.7223, -0.3999] | -0.4500* [-0.5833, -0.3167] [-0.5863, -0.3235] | -0.5667* [-0.7000, -0.4333] [-0.7223, -0.3999] | -0.4500* [-0.5833, -0.3167] [-0.5863, -0.3235] | -0.5667* [-0.7000, -0.4333] [-0.7223, -0.3999] |
| Whole name-map lookup | -0.2667* [-0.3500, -0.1833] [-0.3519, -0.1897] | -0.2500* [-0.3333, -0.1667] [-0.3261, -0.1613] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] |
| Hybrid reader (E10) | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | -0.2333* [-0.3167, -0.1500] [-0.3103, -0.1481] | -0.2500* [-0.3333, -0.1667] [-0.3387, -0.1739] | -0.2333* [-0.3167, -0.1500] [-0.3103, -0.1481] | -0.2500* [-0.3333, -0.1667] [-0.3387, -0.1739] | -0.2333* [-0.3167, -0.1500] [-0.3103, -0.1481] | -0.2500* [-0.3333, -0.1667] [-0.3387, -0.1739] | -0.2333* [-0.3167, -0.1500] [-0.3103, -0.1481] | -0.2500* [-0.3333, -0.1667] [-0.3387, -0.1739] |
| Random-token lookup | -0.2667* [-0.3500, -0.1833] [-0.3519, -0.1897] | -0.2500* [-0.3333, -0.1667] [-0.3261, -0.1613] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] |
| Name lookup, all-mpnet-base-v2 | -0.2667* [-0.3500, -0.1833] [-0.3519, -0.1897] | -0.2500* [-0.3333, -0.1667] [-0.3261, -0.1613] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] |
| Name lookup, bge-small-en-v1.5 | -0.2667* [-0.3500, -0.1833] [-0.3519, -0.1897] | -0.2500* [-0.3333, -0.1667] [-0.3261, -0.1613] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] | -0.5000* [-0.5000, -0.5000] [-0.5000, -0.5000] |
| GPT-5.6 Luna, intent-explicit rubric | -0.1333 [-0.3167, +0.0333] [-0.2931, +0.0161] | +0.0167 [-0.1833, +0.1667] [-0.1667, +0.1740] | -0.3667* [-0.5333, -0.2000] [-0.5357, -0.2120] | -0.2333* [-0.4000, -0.1000] [-0.4000, -0.1000] | -0.3667* [-0.5333, -0.2000] [-0.5357, -0.2120] | -0.2333* [-0.4000, -0.1000] [-0.4000, -0.1000] | -0.3667* [-0.5333, -0.2000] [-0.5357, -0.2120] | -0.2333* [-0.4000, -0.1000] [-0.4000, -0.1000] | -0.3667* [-0.5333, -0.2000] [-0.5357, -0.2120] | -0.2333* [-0.4000, -0.1000] [-0.4000, -0.1000] |
| GPT-4.1 mini, intent-explicit rubric | -0.2333* [-0.3667, -0.0833] [-0.3871, -0.0833] | -0.3167* [-0.4667, -0.1667] [-0.4517, -0.1538] | -0.4667* [-0.6000, -0.3333] [-0.5962, -0.3448] | -0.5667* [-0.6667, -0.4667] [-0.6552, -0.4821] | -0.4667* [-0.6000, -0.3333] [-0.5962, -0.3448] | -0.5667* [-0.6667, -0.4667] [-0.6552, -0.4821] | -0.4667* [-0.6000, -0.3333] [-0.5962, -0.3448] | -0.5667* [-0.6667, -0.4667] [-0.6552, -0.4821] | -0.4667* [-0.6000, -0.3333] [-0.5962, -0.3448] | -0.5667* [-0.6667, -0.4667] [-0.6552, -0.4821] |
| Haiku 4.5, names only (E2) | -0.2500* [-0.3667, -0.1333] [-0.3654, -0.1471] | -0.1833* [-0.3000, -0.0667] [-0.2904, -0.0714] | -0.4833* [-0.5500, -0.4000] [-0.5556, -0.4074] | -0.4333* [-0.5000, -0.3500] [-0.5172, -0.3393] | -0.4833* [-0.5500, -0.4000] [-0.5556, -0.4074] | -0.4333* [-0.5000, -0.3500] [-0.5172, -0.3393] | -0.4833* [-0.5500, -0.4000] [-0.5556, -0.4074] | -0.4333* [-0.5000, -0.3500] [-0.5172, -0.3393] | -0.4833* [-0.5500, -0.4000] [-0.5556, -0.4074] | -0.4333* [-0.5000, -0.3500] [-0.5172, -0.3393] |
| Haiku 4.5, counts only (E2) | -0.1833* [-0.3167, -0.0500] [-0.3056, -0.0370] | -0.3000* [-0.4500, -0.1500] [-0.4445, -0.1552] | -0.4167* [-0.5167, -0.3167] [-0.5003, -0.3076] | -0.5500* [-0.6667, -0.4333] [-0.6667, -0.4483] | -0.4167* [-0.5167, -0.3167] [-0.5003, -0.3076] | -0.5500* [-0.6667, -0.4333] [-0.6667, -0.4483] | -0.4167* [-0.5167, -0.3167] [-0.5003, -0.3076] | -0.5500* [-0.6667, -0.4333] [-0.6667, -0.4483] | -0.4167* [-0.5167, -0.3167] [-0.5003, -0.3076] | -0.5500* [-0.6667, -0.4333] [-0.6667, -0.4483] |
| GPT-4.1 mini, names only (E2) | -0.2167* [-0.3333, -0.1000] [-0.3485, -0.0999] | -0.2500* [-0.3667, -0.1333] [-0.3710, -0.1166] | -0.4500* [-0.5167, -0.3833] [-0.5333, -0.3636] | -0.5000* [-0.5667, -0.4333] [-0.5626, -0.4285] | -0.4500* [-0.5167, -0.3833] [-0.5333, -0.3636] | -0.5000* [-0.5667, -0.4333] [-0.5626, -0.4285] | -0.4500* [-0.5167, -0.3833] [-0.5333, -0.3636] | -0.5000* [-0.5667, -0.4333] [-0.5626, -0.4285] | -0.4500* [-0.5167, -0.3833] [-0.5333, -0.3636] | -0.5000* [-0.5667, -0.4333] [-0.5626, -0.4285] |
| GPT-4.1 mini, names only, dash rule (E2) | -0.3167* [-0.4504, -0.1667] [-0.4423, -0.2026] | -0.3000* [-0.4167, -0.1833] [-0.4334, -0.1613] | -0.5500* [-0.6337, -0.4500] [-0.6333, -0.4677] | -0.5500* [-0.6167, -0.4833] [-0.6429, -0.4688] | -0.5500* [-0.6337, -0.4500] [-0.6333, -0.4677] | -0.5500* [-0.6167, -0.4833] [-0.6429, -0.4688] | -0.5500* [-0.6337, -0.4500] [-0.6333, -0.4677] | -0.5500* [-0.6167, -0.4833] [-0.6429, -0.4688] | -0.5500* [-0.6337, -0.4500] [-0.6333, -0.4677] | -0.5500* [-0.6167, -0.4833] [-0.6429, -0.4688] |
| GPT-4.1 mini, counts only (E2) | -0.1500 [-0.3167, +0.0167] [-0.3030, +0.0000] | -0.3000* [-0.4167, -0.1833] [-0.4460, -0.1607] | -0.3833* [-0.5000, -0.2667] [-0.5000, -0.2586] | -0.5500* [-0.6337, -0.4500] [-0.6719, -0.4483] | -0.3833* [-0.5000, -0.2667] [-0.5000, -0.2586] | -0.5500* [-0.6337, -0.4500] [-0.6719, -0.4483] | -0.3833* [-0.5000, -0.2667] [-0.5000, -0.2586] | -0.5500* [-0.6337, -0.4500] [-0.6719, -0.4483] | -0.3833* [-0.5000, -0.2667] [-0.5000, -0.2586] | -0.5500* [-0.6337, -0.4500] [-0.6719, -0.4483] |
| All-states lookup | +0.0500 [-0.0500, +0.1500] [-0.0517, +0.1452] | +0.1500* [+0.0667, +0.2500] [+0.0781, +0.2344] | -0.1833* [-0.2667, -0.1000] [-0.2679, -0.1060] | -0.1000* [-0.1667, -0.0333] [-0.1667, -0.0455] | -0.1833* [-0.2667, -0.1000] [-0.2679, -0.1060] | -0.1000* [-0.1667, -0.0333] [-0.1667, -0.0455] | -0.1833* [-0.2667, -0.1000] [-0.2679, -0.1060] | -0.1000* [-0.1667, -0.0333] [-0.1667, -0.0455] | -0.1833* [-0.2667, -0.1000] [-0.2679, -0.1060] | -0.1000* [-0.1667, -0.0333] [-0.1667, -0.0455] |
| GPT-4.1 mini, one draw (t = 0) | +0.1667* [+0.0333, +0.2833] [+0.0344, +0.2759] | -0.2167* [-0.3333, -0.1000] [-0.3283, -0.0861] | -0.0667 [-0.1500, +0.0000] [-0.1609, +0.0000] | -0.4667* [-0.5833, -0.3500] [-0.6034, -0.3214] | -0.0667 [-0.1500, +0.0000] [-0.1609, +0.0000] | -0.4667* [-0.5833, -0.3500] [-0.6034, -0.3214] | -0.0667 [-0.1500, +0.0000] [-0.1609, +0.0000] | -0.4667* [-0.5833, -0.3500] [-0.6034, -0.3214] | -0.0667 [-0.1500, +0.0000] [-0.1609, +0.0000] | -0.4667* [-0.5833, -0.3500] [-0.6034, -0.3214] |
| GPT-4.1 mini, five draws (Table 1's row) | +0.1667* [+0.0333, +0.2833] [+0.0333, +0.2742] | +0.0333 [-0.1333, +0.1833] [-0.1251, +0.1897] | -0.0667 [-0.1667, +0.0000] [-0.1786, +0.0000] | -0.2167* [-0.3667, -0.0833] [-0.3571, -0.0893] | -0.0667 [-0.1667, +0.0000] [-0.1786, +0.0000] | -0.2167* [-0.3667, -0.0833] [-0.3571, -0.0893] | -0.0667 [-0.1667, +0.0000] [-0.1786, +0.0000] | -0.2167* [-0.3667, -0.0833] [-0.3571, -0.0893] | -0.0667 [-0.1667, +0.0000] [-0.1786, +0.0000] | -0.2167* [-0.3667, -0.0833] [-0.3571, -0.0893] |
| Haiku 4.5 | +0.1667* [+0.0667, +0.2667] [+0.0811, +0.2502] | +0.1667* [+0.0667, +0.2667] [+0.0555, +0.2931] | -0.0667 [-0.1500, +0.0000] [-0.1324, +0.0000] | -0.0833* [-0.1500, -0.0167] [-0.1613, -0.0172] | -0.0667 [-0.1500, +0.0000] [-0.1324, +0.0000] | -0.0833* [-0.1500, -0.0167] [-0.1613, -0.0172] | -0.0667 [-0.1500, +0.0000] [-0.1324, +0.0000] | -0.0833* [-0.1500, -0.0167] [-0.1613, -0.0172] | -0.0667 [-0.1500, +0.0000] [-0.1324, +0.0000] | -0.0833* [-0.1500, -0.0167] [-0.1613, -0.0172] |
| Opus 5 | +0.0667 [-0.0833, +0.2000] [-0.0741, +0.1936] | +0.2167* [+0.1167, +0.3167] [+0.1452, +0.2963] | -0.1667* [-0.3000, -0.0333] [-0.3000, -0.0568] | -0.0333 [-0.1000, +0.0000] [-0.1071, +0.0000] | -0.1667* [-0.3000, -0.0333] [-0.3000, -0.0568] | -0.0333 [-0.1000, +0.0000] [-0.1071, +0.0000] | -0.1667* [-0.3000, -0.0333] [-0.3000, -0.0568] | -0.0333 [-0.1000, +0.0000] [-0.1071, +0.0000] | -0.1667* [-0.3000, -0.0333] [-0.3000, -0.0568] | -0.0333 [-0.1000, +0.0000] [-0.1071, +0.0000] |
| Opus 5, draw 1 | +0.0500 [-0.1000, +0.2000] [-0.1034, +0.1834] | +0.2167* [+0.1167, +0.3167] [+0.1452, +0.2963] | -0.1833* [-0.3333, -0.0667] [-0.3200, -0.0645] | -0.0333 [-0.1000, +0.0000] [-0.1071, +0.0000] | -0.1833* [-0.3333, -0.0667] [-0.3200, -0.0645] | -0.0333 [-0.1000, +0.0000] [-0.1071, +0.0000] | -0.1833* [-0.3333, -0.0667] [-0.3200, -0.0645] | -0.0333 [-0.1000, +0.0000] [-0.1071, +0.0000] | -0.1833* [-0.3333, -0.0667] [-0.3200, -0.0645] | -0.0333 [-0.1000, +0.0000] [-0.1071, +0.0000] |
| GPT-4.1 mini, draw 1 of five | +0.0833 [-0.0500, +0.2167] [-0.0518, +0.1936] | +0.0000 [-0.1337, +0.1333] [-0.1213, +0.1429] | -0.1500* [-0.2667, -0.0500] [-0.2694, -0.0500] | -0.2500* [-0.3667, -0.1333] [-0.3711, -0.1249] | -0.1500* [-0.2667, -0.0500] [-0.2694, -0.0500] | -0.2500* [-0.3667, -0.1333] [-0.3711, -0.1249] | -0.1500* [-0.2667, -0.0500] [-0.2694, -0.0500] | -0.2500* [-0.3667, -0.1333] [-0.3711, -0.1249] | -0.1500* [-0.2667, -0.0500] [-0.2694, -0.0500] | -0.2500* [-0.3667, -0.1333] [-0.3711, -0.1249] |
| Random-token lookup | -0.2167* [-0.3000, -0.1333] [-0.3030, -0.1346] | -0.0667 [-0.1667, +0.0333] [-0.1564, +0.0484] | -0.4500* [-0.5000, -0.3996] [-0.5000, -0.3889] | -0.3167* [-0.4000, -0.2333] [-0.3966, -0.2241] | -0.4500* [-0.5000, -0.3996] [-0.5000, -0.3889] | -0.3167* [-0.4000, -0.2333] [-0.3966, -0.2241] | -0.4500* [-0.5000, -0.3996] [-0.5000, -0.3889] | -0.3167* [-0.4000, -0.2333] [-0.3966, -0.2241] | -0.4500* [-0.5000, -0.3996] [-0.5000, -0.3889] | -0.3167* [-0.4000, -0.2333] [-0.3966, -0.2241] |
| All-states lookup, all-mpnet-base-v2 | +0.0500 [-0.0667, +0.1504] [-0.0667, +0.1501] | +0.1667* [+0.0667, +0.2667] [+0.1000, +0.2500] | -0.1833* [-0.2667, -0.1000] [-0.2679, -0.1094] | -0.0833* [-0.1500, -0.0329] [-0.1500, -0.0303] | -0.1833* [-0.2667, -0.1000] [-0.2679, -0.1094] | -0.0833* [-0.1500, -0.0329] [-0.1500, -0.0303] | -0.1833* [-0.2667, -0.1000] [-0.2679, -0.1094] | -0.0833* [-0.1500, -0.0329] [-0.1500, -0.0303] | -0.1833* [-0.2667, -0.1000] [-0.2679, -0.1094] | -0.0833* [-0.1500, -0.0329] [-0.1500, -0.0303] |
| All-states lookup, bge-small-en-v1.5 | +0.0500 [-0.0500, +0.1667] [-0.0625, +0.1482] | +0.1833* [+0.0833, +0.2833] [+0.0862, +0.2857] | -0.1833* [-0.2667, -0.1000] [-0.2679, -0.1094] | -0.0667* [-0.1333, -0.0167] [-0.1346, -0.0161] | -0.1833* [-0.2667, -0.1000] [-0.2679, -0.1094] | -0.0667* [-0.1333, -0.0167] [-0.1346, -0.0161] | -0.1833* [-0.2667, -0.1000] [-0.2679, -0.1094] | -0.0667* [-0.1333, -0.0167] [-0.1346, -0.0161] | -0.1833* [-0.2667, -0.1000] [-0.2679, -0.1094] | -0.0667* [-0.1333, -0.0167] [-0.1346, -0.0161] |
| GPT-4.1 mini, one draw (t = 0) | -0.3667* [-0.5333, -0.2000] [-0.5536, -0.2096] | -0.2833* [-0.4167, -0.1500] [-0.3789, -0.1717] | -0.6000* [-0.7167, -0.4833] [-0.7321, -0.4857] | -0.5333* [-0.6500, -0.4167] [-0.6429, -0.4285] | -0.6000* [-0.7167, -0.4833] [-0.7321, -0.4857] | -0.5333* [-0.6500, -0.4167] [-0.6429, -0.4285] | +0.0333 [-0.1500, +0.2167] [-0.1481, +0.1786] | +0.1833 [+0.0000, +0.3667] [-0.0441, +0.3846] | -0.6000* [-0.7167, -0.4833] [-0.7321, -0.4857] | -0.5333* [-0.6500, -0.4167] [-0.6429, -0.4285] |
| Haiku 4.5 | -0.1500 [-0.3000, +0.0000] [-0.3036, +0.0000] | -0.2000* [-0.3171, -0.0667] [-0.3276, -0.0600] | -0.3833* [-0.4833, -0.2996] [-0.5000, -0.2742] | -0.4500* [-0.5500, -0.3500] [-0.5333, -0.3621] | -0.3833* [-0.4833, -0.2996] [-0.5000, -0.2742] | -0.4500* [-0.5500, -0.3500] [-0.5333, -0.3621] | +0.2500* [+0.0333, +0.4333] [+0.0208, +0.4465] | +0.2667* [+0.0667, +0.4333] [+0.0536, +0.4600] | -0.3833* [-0.4833, -0.2996] [-0.5000, -0.2742] | -0.4500* [-0.5500, -0.3500] [-0.5333, -0.3621] |
| Opus 5 | -0.1000 [-0.3333, +0.1004] [-0.3277, +0.0834] | +0.0167 [-0.1667, +0.1667] [-0.1552, +0.1724] | -0.3333* [-0.5333, -0.1667] [-0.5204, -0.1765] | -0.2333* [-0.4000, -0.1000] [-0.3871, -0.0999] | -0.3333* [-0.5333, -0.1667] [-0.5204, -0.1765] | -0.2333* [-0.4000, -0.1000] [-0.3871, -0.0999] | +0.3000* [+0.1333, +0.4833] [+0.1154, +0.4732] | +0.4833* [+0.3000, +0.6500] [+0.2969, +0.6971] | -0.3333* [-0.5333, -0.1667] [-0.5204, -0.1765] | -0.2333* [-0.4000, -0.1000] [-0.3871, -0.0999] |
| GPT-4.1 mini, one draw | +0.2833* [+0.1500, +0.4000] [+0.1607, +0.4286] | +0.1000 [-0.0333, +0.2333] [-0.0179, +0.2097] | +0.2833* [+0.1667, +0.4000] [+0.1785, +0.3940] | +0.2667* [+0.1167, +0.4167] [+0.1450, +0.3793] | +0.2833* [+0.1667, +0.4000] [+0.1785, +0.3940] | +0.2667* [+0.1167, +0.4167] [+0.1450, +0.3793] | +0.1833 [-0.0167, +0.3667] [+0.0303, +0.3500] | +0.2667* [+0.0667, +0.4333] [+0.0651, +0.4516] | +0.4667* [+0.3500, +0.5833] [+0.3529, +0.5926] | +0.2667* [+0.1167, +0.4167] [+0.1450, +0.3793] |
| Haiku 4.5, five draws | +0.3000* [+0.2000, +0.4000] [+0.2083, +0.4107] | +0.0333 [-0.0667, +0.1333] [-0.0357, +0.1200] | +0.3000* [+0.1667, +0.4167] [+0.1667, +0.4219] | +0.2000* [+0.0667, +0.3333] [+0.1034, +0.3276] | +0.3000* [+0.1667, +0.4167] [+0.1667, +0.4219] | +0.2000* [+0.0667, +0.3333] [+0.1034, +0.3276] | +0.2000 [+0.0000, +0.4000] [+0.0000, +0.3929] | +0.2000* [+0.0500, +0.3333] [+0.0135, +0.3751] | +0.4833* [+0.3667, +0.5837] [+0.3750, +0.6034] | +0.2000* [+0.0667, +0.3333] [+0.1034, +0.3276] |
| Opus 5, five draws (E1 Amendment 1) | +0.1333 [-0.0667, +0.3333] [-0.0667, +0.3335] | +0.0333 [-0.1667, +0.2500] [-0.1774, +0.2500] | +0.1333 [-0.0500, +0.3167] [-0.0517, +0.3226] | +0.2000* [+0.0167, +0.3837] [+0.0323, +0.3750] | +0.1333 [-0.0500, +0.3167] [-0.0517, +0.3226] | +0.2000* [+0.0167, +0.3837] [+0.0323, +0.3750] | +0.0333 [-0.1833, +0.2500] [-0.1834, +0.2647] | +0.2000 [-0.0333, +0.4333] [-0.1030, +0.4792] | +0.3167* [+0.1333, +0.5000] [+0.1167, +0.5179] | +0.2000* [+0.0167, +0.3837] [+0.0323, +0.3750] |
| Opus 5, draw 1 | +0.1667 [+0.0000, +0.3333] [-0.0185, +0.3751] | +0.1000 [-0.0667, +0.2667] [-0.0469, +0.2500] | +0.1667 [+0.0167, +0.3167] [+0.0000, +0.3485] | +0.2667* [+0.1000, +0.4333] [+0.1094, +0.4311] | +0.1667 [+0.0167, +0.3167] [+0.0000, +0.3485] | +0.2667* [+0.1000, +0.4333] [+0.1094, +0.4311] | +0.0667 [-0.1667, +0.3004] [-0.1801, +0.3037] | +0.2667* [+0.0833, +0.4500] [+0.0570, +0.4655] | +0.3500* [+0.2167, +0.5000] [+0.1895, +0.5185] | +0.2667* [+0.1000, +0.4333] [+0.1094, +0.4311] |
| GPT-5.6 Luna, five draws (E9) | +0.0667 [-0.1167, +0.2667] [-0.1168, +0.2593] | +0.1500 [-0.0333, +0.3167] [-0.0173, +0.3271] | +0.0667 [-0.1167, +0.2667] [-0.1346, +0.2502] | +0.3167* [+0.1167, +0.4833] [+0.1093, +0.5357] | +0.0667 [-0.1167, +0.2667] [-0.1346, +0.2502] | +0.3167* [+0.1167, +0.4833] [+0.1093, +0.5357] | -0.0333 [-0.2333, +0.1833] [-0.2500, +0.1852] | +0.3167* [+0.0996, +0.5167] [+0.0606, +0.5357] | +0.2500* [+0.0833, +0.4167] [+0.0769, +0.4139] | +0.3167* [+0.1167, +0.4833] [+0.1093, +0.5357] |
| GPT-5.6 Luna, draw 1 | +0.2667* [+0.0833, +0.4500] [+0.0833, +0.4483] | +0.1667 [-0.0167, +0.3333] [-0.0625, +0.3794] | +0.2667* [+0.1000, +0.4500] [+0.0806, +0.4286] | +0.3333* [+0.1500, +0.5000] [+0.1250, +0.5371] | +0.2667* [+0.1000, +0.4500] [+0.0806, +0.4286] | +0.3333* [+0.1500, +0.5000] [+0.1250, +0.5371] | +0.1667 [-0.0333, +0.3833] [-0.0387, +0.3594] | +0.3333* [+0.1000, +0.5500] [+0.0156, +0.6002] | +0.4500* [+0.2667, +0.6333] [+0.2584, +0.6482] | +0.3333* [+0.1500, +0.5000] [+0.1250, +0.5371] |
| GPT-5.6 Sol, five draws (E9) | +0.1333 [-0.0333, +0.3333] [-0.0500, +0.3333] | -0.0833 [-0.2333, +0.0833] [-0.2333, +0.0557] | +0.1333 [-0.0333, +0.3333] [-0.0537, +0.3276] | +0.0833 [-0.0833, +0.2504] [-0.0676, +0.2500] | +0.1333 [-0.0333, +0.3333] [-0.0537, +0.3276] | +0.0833 [-0.0833, +0.2504] [-0.0676, +0.2500] | +0.0333 [-0.1833, +0.2833] [-0.1614, +0.2344] | +0.0833 [-0.1167, +0.2667] [-0.1381, +0.3077] | +0.3167* [+0.1333, +0.5333] [+0.1176, +0.5185] | +0.0833 [-0.0833, +0.2504] [-0.0676, +0.2500] |
| GPT-5.6 Sol, draw 1 | +0.2000 [+0.0000, +0.4167] [+0.0167, +0.4074] | -0.0833 [-0.2500, +0.1000] [-0.2426, +0.0969] | +0.2000* [+0.0167, +0.3833] [+0.0192, +0.3751] | +0.0833 [-0.0833, +0.2667] [-0.0716, +0.2586] | +0.2000* [+0.0167, +0.3833] [+0.0192, +0.3751] | +0.0833 [-0.0833, +0.2667] [-0.0716, +0.2586] | +0.1000 [-0.1500, +0.3667] [-0.1501, +0.3387] | +0.0833 [-0.1000, +0.2667] [-0.1252, +0.3077] | +0.3833* [+0.2000, +0.5667] [+0.2068, +0.5741] | +0.0833 [-0.0833, +0.2667] [-0.0716, +0.2586] |

### AUX-CF2-R125-OP5-V3 — Opus 5 under the all-states summary minus the all-states lookup

### Opus 5 under the all-states summary minus the all-states lookup, matched PN vs PRESENT (and PN vs ABSENT), whole set and per state

| row | comparison | whole Δ | triple | persona | reliable | sup Δ | triple | persona | ret Δ | triple | persona | exp Δ | triple | persona |
|---|---|---:|---|---|---|---:|---|---|---:|---|---|---:|---|---|
| Opus 5, five draws | pn vs present | +0.0304 | [-0.0068, +0.0643] | [-0.0038, +0.0648] | no | +0.0227 | [-0.0114, +0.0568] | [-0.0105, +0.0550] | +0.0167 | [-0.0833, +0.1333] | [-0.0800, +0.1207] | +0.0667 | [-0.0333, +0.1667] | [+0.0000, +0.1407] |
| Opus 5, five draws | pn vs absent | +0.0372 | [+0.0034, +0.0709] | [+0.0000, +0.0750] | disagree | +0.0284 | [-0.0114, +0.0682] | [-0.0179, +0.0769] | +0.0333 | [-0.0500, +0.1167] | [-0.0357, +0.1208] | +0.0667 | [+0.0000, +0.1337] | [+0.0000, +0.1379] |
| Opus 5, draw 1 | pn vs present | +0.0372 | [+0.0033, +0.0709] | [+0.0076, +0.0662] | **reliable** | +0.0398* | [+0.0170, +0.0682] | [+0.0118, +0.0714] | +0.0000 | [-0.1000, +0.1004] | [-0.0962, +0.0968] | +0.0667 | [-0.0333, +0.1667] | [+0.0000, +0.1407] |
| Opus 5, draw 1 | pn vs absent | +0.0372 | [+0.0000, +0.0743] | [-0.0036, +0.0761] | no | +0.0227 | [-0.0170, +0.0568] | [-0.0260, +0.0670] | +0.0667 | [-0.0500, +0.1667] | [-0.0333, +0.1724] | +0.0500 | [-0.0333, +0.1333] | [-0.0345, +0.1333] |

### AUX-CF2-R125-CONTRASTS — the named contrasts

### The named contrasts (A minus B) under the matched metric, PN vs PRESENT: Δ with the triple and the persona interval per scope; * = both intervals exclude zero

| contrast | whole | sup | ret | exp | counted (ret + exp, 60 triples) |
|---|---|---|---|---|---|
| E2 Haiku counts-only minus intact | -0.1419* [-0.2095, -0.0743] [-0.2007, -0.0856] | -0.1989* [-0.2898, -0.1080] [-0.2903, -0.1067] | +0.0167 [-0.1000, +0.1333] [-0.1000, +0.1407] | -0.1333 [-0.2833, +0.0167] [-0.2932, +0.0000] | -0.0583 [-0.1667, +0.0333] [-0.1379, +0.0250] |
| E2 Haiku counts-only minus names-only | -0.1385* [-0.2095, -0.0776] [-0.2113, -0.0640] | -0.2159* [-0.3068, -0.1364] [-0.3193, -0.1111] | +0.0667 [-0.0500, +0.1833] [-0.0429, +0.1923] | -0.1167 [-0.2500, +0.0167] [-0.2667, +0.0179] | -0.0250 [-0.1167, +0.0669] [-0.1215, +0.0715] |
| E2 Haiku names-only minus intact | -0.0034 [-0.0507, +0.0473] [-0.0671, +0.0578] | +0.0170 [-0.0341, +0.0739] [-0.0353, +0.0787] | -0.0500 [-0.1833, +0.0667] [-0.1876, +0.0645] | -0.0167 [-0.1333, +0.1000] [-0.2000, +0.1250] | -0.0333 [-0.1333, +0.0500] [-0.1392, +0.0741] |
| E2 mini counts-only minus intact | -0.1351* [-0.2027, -0.0675] [-0.1944, -0.0772] | -0.2273* [-0.3125, -0.1477] [-0.3021, -0.1521] | +0.0667 [-0.1333, +0.2333] [-0.1000, +0.2424] | -0.0667 [-0.1667, +0.0500] [-0.1819, +0.0690] | +0.0000 [-0.1085, +0.1083] [-0.1045, +0.1230] |
| E2 mini counts-only minus names-only | -0.1351* [-0.2027, -0.0743] [-0.1943, -0.0827] | -0.2330* [-0.3125, -0.1533] [-0.3133, -0.1522] | +0.0667 [-0.0833, +0.2000] [-0.0758, +0.2223] | -0.0500 [-0.1500, +0.0667] [-0.1923, +0.0781] | +0.0083 [-0.0833, +0.1000] [-0.0970, +0.1226] |
| E2 mini names-only dash minus intact | -0.0507 [-0.1014, +0.0000] [-0.1168, +0.0065] | -0.0284 [-0.0909, +0.0341] [-0.0977, +0.0309] | -0.1000 [-0.2500, +0.0500] [-0.2421, +0.0278] | -0.0667 [-0.1833, +0.0500] [-0.2333, +0.0862] | -0.0833 [-0.1833, +0.0083] [-0.1985, +0.0197] |
| E2 mini names-only minus intact | +0.0000 [-0.0439, +0.0473] [-0.0440, +0.0426] | +0.0057 [-0.0398, +0.0511] [-0.0349, +0.0533] | +0.0000 [-0.1333, +0.1333] [-0.1296, +0.1212] | -0.0167 [-0.1333, +0.1000] [-0.1515, +0.1154] | -0.0083 [-0.1083, +0.0750] [-0.1059, +0.0819] |
| Haiku draw 1 minus five draws (v2) | -0.0135 [-0.0405, +0.0101] [-0.0417, +0.0129] | -0.0114 [-0.0341, +0.0114] [-0.0341, +0.0110] | +0.0167 [-0.0333, +0.0667] [-0.0385, +0.0676] | -0.0500 [-0.1500, +0.0167] [-0.1613, +0.0333] | -0.0167 [-0.0669, +0.0333] [-0.0820, +0.0373] |
| Haiku minus guessed-category count reader | +0.0574 [-0.0068, +0.1182] [-0.0145, +0.1303] | +0.2216* [+0.1534, +0.2898] [+0.1500, +0.2917] | -0.2000* [-0.3167, -0.0667] [-0.3089, -0.0769] | -0.1667* [-0.3000, -0.0500] [-0.2904, -0.0151] | -0.1833* [-0.2667, -0.0917] [-0.2721, -0.0781] |
| Haiku minus hybrid | -0.1081* [-0.1555, -0.0642] [-0.1644, -0.0479] | -0.0568* [-0.1136, -0.0114] [-0.1105, -0.0106] | -0.2000* [-0.3167, -0.0667] [-0.3089, -0.0769] | -0.1667* [-0.3000, -0.0500] [-0.2904, -0.0151] | -0.1833* [-0.2667, -0.0917] [-0.2721, -0.0781] |
| Luna draw 1 minus five draws (v2) | -0.0372 [-0.0912, +0.0203] [-0.0906, +0.0265] | -0.0284 [-0.0682, +0.0000] [-0.0591, +0.0000] | +0.0500 [-0.1667, +0.2333] [-0.1786, +0.2667] | -0.1500 [-0.3004, +0.0000] [-0.3056, -0.0135] | -0.0500 [-0.1752, +0.0917] [-0.1834, +0.1112] |
| Luna minus guessed-category count reader | +0.1588* [+0.0845, +0.2264] [+0.0880, +0.2279] | +0.2670* [+0.2045, +0.3239] [+0.2011, +0.3314] | -0.1167 [-0.3333, +0.1167] [-0.3336, +0.0770] | +0.1167 [-0.0333, +0.2500] [-0.0156, +0.2586] | +0.0000 [-0.1333, +0.1169] [-0.1339, +0.1508] |
| Luna minus hybrid | -0.0068 [-0.0642, +0.0507] [-0.0659, +0.0536] | -0.0114 [-0.0341, +0.0114] [-0.0353, +0.0106] | -0.1167 [-0.3333, +0.1167] [-0.3336, +0.0770] | +0.1167 [-0.0333, +0.2500] [-0.0156, +0.2586] | +0.0000 [-0.1333, +0.1169] [-0.1339, +0.1508] |
| Opus draw 1 minus five draws (v2) | -0.0068 [-0.0439, +0.0304] [-0.0490, +0.0357] | -0.0057 [-0.0170, +0.0000] [-0.0172, +0.0000] | -0.0333 [-0.1667, +0.0837] [-0.1786, +0.0969] | +0.0167 [-0.1167, +0.1667] [-0.1167, +0.1452] | -0.0083 [-0.1000, +0.0917] [-0.1173, +0.0949] |
| Opus minus guessed-category count reader | +0.1554* [+0.0811, +0.2230] [+0.0828, +0.2347] | +0.2841* [+0.2273, +0.3409] [+0.2151, +0.3571] | +0.0000 [-0.1833, +0.1833] [-0.1966, +0.1757] | -0.0667 [-0.2504, +0.1167] [-0.2834, +0.1379] | -0.0333 [-0.1667, +0.0835] [-0.1699, +0.0982] |
| Opus minus hybrid | -0.0101 [-0.0676, +0.0439] [-0.0733, +0.0563] | +0.0057 [-0.0284, +0.0341] [-0.0330, +0.0523] | +0.0000 [-0.1833, +0.1833] [-0.1966, +0.1757] | -0.0667 [-0.2504, +0.1167] [-0.2834, +0.1379] | -0.0333 [-0.1667, +0.0835] [-0.1699, +0.0982] |
| Sol draw 1 minus five draws (v2) | -0.0473 [-0.0980, +0.0068] [-0.0909, -0.0070] | -0.0114 [-0.0682, +0.0398] [-0.0530, +0.0321] | -0.0167 [-0.2000, +0.1500] [-0.1858, +0.1579] | -0.1833* [-0.3167, -0.0667] [-0.2904, -0.0769] | -0.1000 [-0.2083, +0.0000] [-0.1818, -0.0091] |
| Sol minus guessed-category count reader | +0.1385* [+0.0742, +0.1959] [+0.0869, +0.1900] | +0.2670* [+0.2102, +0.3239] [+0.1988, +0.3352] | -0.1833 [-0.3500, +0.0000] [-0.3519, -0.0284] | +0.0833 [-0.0504, +0.2167] [-0.0653, +0.2143] | -0.0500 [-0.1667, +0.0667] [-0.1518, +0.0536] |
| Sol minus hybrid (P-H2) | -0.0270 [-0.0812, +0.0203] [-0.0737, +0.0175] | -0.0114 [-0.0568, +0.0227] [-0.0460, +0.0206] | -0.1833 [-0.3500, +0.0000] [-0.3519, -0.0284] | +0.0833 [-0.0504, +0.2167] [-0.0653, +0.2143] | -0.0500 [-0.1667, +0.0667] [-0.1518, +0.0536] |
| all-states Haiku minus sup-only | +0.1284* [+0.0743, +0.1824] [+0.0625, +0.1930] | -0.0227 [-0.0739, +0.0284] [-0.0783, +0.0353] | +0.3667* [+0.2500, +0.4500] [+0.2857, +0.4375] | +0.3333* [+0.2167, +0.4500] [+0.1851, +0.4691] | +0.3500* [+0.2667, +0.4333] [+0.2659, +0.4310] |
| all-states Opus minus sup-only | +0.0642 [+0.0068, +0.1182] [-0.0037, +0.1234] | -0.0114 [-0.0455, +0.0227] [-0.0674, +0.0263] | +0.0667 [-0.0833, +0.2167] [-0.0863, +0.2223] | +0.2833* [+0.1000, +0.4667] [+0.0690, +0.4844] | +0.1750* [+0.0667, +0.3000] [+0.0614, +0.2924] |
| all-states lookup minus name lookup | +0.1318* [+0.0945, +0.1724] [+0.0906, +0.1690] | -0.0227* [-0.0511, -0.0057] [-0.0449, -0.0053] | +0.3167* [+0.2333, +0.4000] [+0.2321, +0.3940] | +0.4000* [+0.3333, +0.4667] [+0.3333, +0.4545] | +0.3583* [+0.3000, +0.4167] [+0.3071, +0.4105] |
| all-states mini k1 minus sup-only | +0.0777* [+0.0203, +0.1351] [+0.0133, +0.1391] | -0.0057 [-0.0568, +0.0455] [-0.0677, +0.0488] | +0.3833* [+0.2667, +0.5000] [+0.2592, +0.4868] | +0.0167 [-0.1004, +0.1500] [-0.1406, +0.1731] | +0.2000* [+0.0833, +0.3000] [+0.0821, +0.3158] |
| all-states mini k5 minus sup-only | +0.1689* [+0.0946, +0.2432] [+0.1114, +0.2293] | +0.0284 [-0.0398, +0.1080] [-0.0334, +0.0893] | +0.3667* [+0.2167, +0.5167] [+0.2037, +0.5345] | +0.3833* [+0.2000, +0.5833] [+0.2361, +0.5370] | +0.3750* [+0.2500, +0.5002] [+0.2755, +0.4828] |
| bge-small minus MiniLM (v2) | +0.0034 [+0.0000, +0.0101] [+0.0000, +0.0106] | +0.0057 [+0.0000, +0.0170] [+0.0000, +0.0206] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] |
| hybrid minus guessed-category count reader | +0.1655* [+0.1283, +0.2027] [+0.1257, +0.2100] | +0.2784* [+0.2273, +0.3295] [+0.2157, +0.3391] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] |
| hybrid minus name lookup (P-H1) | +0.1081* [+0.0777, +0.1419] [+0.0741, +0.1419] | +0.0057 [+0.0000, +0.0170] [+0.0000, +0.0179] | +0.2667* [+0.1833, +0.3500] [+0.1897, +0.3519] | +0.2500* [+0.1667, +0.3333] [+0.1613, +0.3261] | +0.2583* [+0.1917, +0.3250] [+0.2018, +0.3125] |
| intent-explicit Luna minus main-study | -0.0304 [-0.0946, +0.0372] [-0.1019, +0.0395] | -0.0114 [-0.0625, +0.0284] [-0.0459, +0.0209] | -0.0167 [-0.2500, +0.2167] [-0.2593, +0.2002] | -0.1000 [-0.2667, +0.0667] [-0.3103, +0.0690] | -0.0583 [-0.2083, +0.0833] [-0.2453, +0.1035] |
| intent-explicit mini minus main-study | -0.0236 [-0.0743, +0.0271] [-0.0850, +0.0272] | -0.0057 [-0.0568, +0.0455] [-0.0465, +0.0303] | -0.0167 [-0.1833, +0.1500] [-0.1765, +0.1364] | -0.0833 [-0.2000, +0.0337] [-0.2223, +0.0589] | -0.0500 [-0.1583, +0.0583] [-0.1438, +0.0546] |
| mini five draws minus one draw (v2) | -0.0135 [-0.0777, +0.0541] [-0.0709, +0.0414] | +0.0114 [-0.0455, +0.0739] [-0.0426, +0.0602] | +0.0167 [-0.1833, +0.2167] [-0.1965, +0.2322] | -0.1167 [-0.3000, +0.0500] [-0.2858, +0.0323] | -0.0500 [-0.2000, +0.0750] [-0.1735, +0.0697] |
| mini five draws minus one draw (v3) | +0.0777* [+0.0203, +0.1318] [+0.0162, +0.1361] | +0.0455 [-0.0170, +0.1136] [-0.0179, +0.1087] | +0.0000 [-0.0833, +0.0667] [-0.0926, +0.0758] | +0.2500* [+0.0833, +0.4167] [+0.0833, +0.4286] | +0.1250* [+0.0250, +0.2250] [+0.0208, +0.2308] |
| mini k1 minus guessed-category count reader | +0.0203 [-0.0473, +0.0845] [-0.0380, +0.0833] | +0.1875* [+0.1307, +0.2500] [+0.1200, +0.2600] | -0.2167* [-0.3833, -0.0500] [-0.3750, -0.0625] | -0.2333* [-0.3504, -0.1167] [-0.3462, -0.1199] | -0.2250* [-0.3333, -0.1167] [-0.3365, -0.1226] |
| mini k1 minus hybrid | -0.1453* [-0.1993, -0.0946] [-0.1985, -0.0871] | -0.0909* [-0.1365, -0.0455] [-0.1495, -0.0330] | -0.2167* [-0.3833, -0.0500] [-0.3750, -0.0625] | -0.2333* [-0.3504, -0.1167] [-0.3462, -0.1199] | -0.2250* [-0.3333, -0.1167] [-0.3365, -0.1226] |
| mini k5 minus guessed-category count reader | +0.0068 [-0.0743, +0.0845] [-0.0560, +0.0704] | +0.1989* [+0.1250, +0.2670] [+0.1304, +0.2701] | -0.2000* [-0.3671, -0.0167] [-0.4194, -0.0139] | -0.3500* [-0.5167, -0.1833] [-0.5167, -0.2069] | -0.2750* [-0.4083, -0.1500] [-0.4036, -0.1525] |
| mini k5 minus hybrid | -0.1588* [-0.2264, -0.0979] [-0.2244, -0.0965] | -0.0795* [-0.1364, -0.0227] [-0.1467, -0.0260] | -0.2000* [-0.3671, -0.0167] [-0.4194, -0.0139] | -0.3500* [-0.5167, -0.1833] [-0.5167, -0.2069] | -0.2750* [-0.4083, -0.1500] [-0.4036, -0.1525] |
| moved count Haiku minus sup-only | -0.0304 [-0.0743, +0.0101] [-0.0756, +0.0245] | -0.0170 [-0.0625, +0.0227] [-0.0575, +0.0235] | +0.0000 [-0.1333, +0.1333] [-0.1613, +0.1481] | -0.1000 [-0.2000, +0.0000] [-0.2000, +0.0000] | -0.0500 [-0.1417, +0.0250] [-0.1455, +0.0704] |
| moved count Luna draw 1 minus sup-only draw 1 | -0.0507 [-0.1284, +0.0270] [-0.1215, +0.0086] | +0.0057 [-0.0399, +0.0568] [-0.0298, +0.0465] | -0.1667 [-0.4167, +0.0833] [-0.4334, +0.1071] | -0.1000 [-0.3167, +0.1167] [-0.2778, +0.0893] | -0.1333 [-0.3000, +0.0250] [-0.2885, +0.0159] |
| moved count Luna k5 minus sup-only k5 (E9) | -0.1115* [-0.1824, -0.0338] [-0.1793, -0.0392] | +0.0114 [-0.0398, +0.0625] [-0.0275, +0.0588] | -0.3167* [-0.5667, -0.0667] [-0.5758, -0.0333] | -0.2667* [-0.4667, -0.0667] [-0.4571, -0.0714] | -0.2917* [-0.4500, -0.1250] [-0.4630, -0.1231] |
| moved count Opus draw 1 minus sup-only draw 1 | -0.1182* [-0.1893, -0.0473] [-0.1981, -0.0359] | -0.0455* [-0.0852, -0.0114] [-0.0914, -0.0060] | -0.3000* [-0.5000, -0.0833] [-0.5345, -0.0806] | -0.1500 [-0.4167, +0.1167] [-0.4143, +0.1071] | -0.2250* [-0.3917, -0.0333] [-0.3982, -0.0545] |
| moved count Opus draw 1 minus sup-only k5 (registered) | -0.1250* [-0.1926, -0.0507] [-0.2096, -0.0483] | -0.0511* [-0.0966, -0.0114] [-0.1053, -0.0060] | -0.3333* [-0.5833, -0.0996] [-0.5807, -0.1034] | -0.1333 [-0.3667, +0.1004] [-0.3940, +0.1251] | -0.2333* [-0.4000, -0.0415] [-0.4167, -0.0454] |
| moved count Opus k5 minus sup-only k5 | -0.1351* [-0.2162, -0.0608] [-0.2169, -0.0577] | -0.0341 [-0.0795, +0.0000] [-0.0817, +0.0000] | -0.3667* [-0.6167, -0.1167] [-0.5962, -0.1296] | -0.2000 [-0.4171, +0.0500] [-0.4501, +0.0371] | -0.2833* [-0.4417, -0.0915] [-0.4818, -0.0895] |
| moved count Sol draw 1 minus sup-only draw 1 | -0.0845* [-0.1588, -0.0101] [-0.1433, -0.0229] | -0.0114 [-0.0682, +0.0398] [-0.0638, +0.0407] | -0.1000 [-0.3167, +0.1167] [-0.3227, +0.1143] | -0.2833* [-0.5000, -0.0500] [-0.4808, -0.0667] | -0.1917* [-0.3419, -0.0417] [-0.3281, -0.0410] |
| moved count Sol k5 minus sup-only k5 (E9) | -0.1318* [-0.2163, -0.0507] [-0.2169, -0.0419] | +0.0000 [-0.0568, +0.0568] [-0.0440, +0.0465] | -0.1833 [-0.4500, +0.1000] [-0.4483, +0.1347] | -0.4667* [-0.7000, -0.2000] [-0.6452, -0.2496] | -0.3250* [-0.5000, -0.1333] [-0.4825, -0.1344] |
| moved count mini minus sup-only | -0.0034 [-0.0541, +0.0473] [-0.0537, +0.0472] | -0.0170 [-0.0625, +0.0284] [-0.0577, +0.0177] | +0.0000 [-0.1500, +0.1337] [-0.1452, +0.1452] | +0.0333 [-0.1000, +0.1833] [-0.0962, +0.1667] | +0.0167 [-0.0750, +0.1083] [-0.0896, +0.1334] |
| mpnet minus MiniLM (v2) | -0.0034 [-0.0101, +0.0000] [-0.0115, +0.0000] | -0.0057 [-0.0170, +0.0000] [-0.0185, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] |
| name lookup minus guessed-category count reader | +0.0574 [-0.0034, +0.1149] [-0.0001, +0.1186] | +0.2727* [+0.2159, +0.3240] [+0.2088, +0.3350] | -0.2667* [-0.3500, -0.1833] [-0.3519, -0.1897] | -0.2500* [-0.3333, -0.1667] [-0.3261, -0.1613] | -0.2583* [-0.3250, -0.1917] [-0.3125, -0.2018] |
| random-token minus all-states lookup (v3) | -0.3041* [-0.3447, -0.2568] [-0.3493, -0.2516] | -0.3466* [-0.3977, -0.2955] [-0.3987, -0.2903] | -0.2667* [-0.3500, -0.1667] [-0.3542, -0.1724] | -0.2167* [-0.3171, -0.1000] [-0.3167, -0.0967] | -0.2417* [-0.3167, -0.1750] [-0.3115, -0.1692] |
| random-token minus name lookup (v2) | -0.1318* [-0.1724, -0.0912] [-0.1786, -0.0854] | -0.2216* [-0.2841, -0.1646] [-0.2889, -0.1506] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] |
| totals rand. Haiku minus sup-only | -0.0068 [-0.0508, +0.0338] [-0.0580, +0.0520] | -0.0170 [-0.0568, +0.0227] [-0.0568, +0.0225] | +0.0500 [-0.0833, +0.1833] [-0.1094, +0.2001] | -0.0333 [-0.1667, +0.0833] [-0.1935, +0.1001] | +0.0083 [-0.0917, +0.0917] [-0.1038, +0.1316] |
| totals rand. Opus minus sup-only | -0.0101 [-0.0777, +0.0575] [-0.0725, +0.0548] | -0.0114 [-0.0568, +0.0227] [-0.0652, +0.0337] | -0.1000 [-0.3000, +0.1000] [-0.3149, +0.0782] | +0.0833 [-0.1504, +0.3167] [-0.0806, +0.2778] | -0.0083 [-0.1500, +0.1419] [-0.1482, +0.1321] |
| totals rand. mini minus sup-only | -0.0439 [-0.1014, +0.0135] [-0.0893, +0.0000] | -0.0057 [-0.0625, +0.0455] [-0.0444, +0.0404] | -0.1500 [-0.3167, +0.0000] [-0.3270, +0.0000] | -0.0500 [-0.1833, +0.0833] [-0.1719, +0.0926] | -0.1000 [-0.2085, +0.0083] [-0.2122, +0.0000] |

The same contrasts, PN vs ABSENT:

| contrast | whole | sup | ret | exp | counted |
|---|---|---|---|---|---|
| E2 Haiku counts-only minus intact | -0.1655* [-0.2264, -0.1013] [-0.2177, -0.1083] | -0.2443* [-0.3125, -0.1705] [-0.3387, -0.1644] | -0.0167 [-0.1667, +0.1500] [-0.1613, +0.1290] | -0.0833 [-0.2004, +0.0500] [-0.2121, +0.0345] | -0.0500 [-0.1500, +0.0583] [-0.1415, +0.0435] |
| E2 Haiku counts-only minus names-only | -0.1588* [-0.2230, -0.0945] [-0.2165, -0.0935] | -0.2216* [-0.3011, -0.1420] [-0.3210, -0.1368] | -0.0500 [-0.1667, +0.0833] [-0.1515, +0.0741] | -0.0833 [-0.2167, +0.0833] [-0.2322, +0.0690] | -0.0667 [-0.1667, +0.0335] [-0.1500, +0.0182] |
| E2 Haiku names-only minus intact | -0.0068 [-0.0507, +0.0405] [-0.0556, +0.0336] | -0.0227 [-0.0682, +0.0227] [-0.0685, +0.0233] | +0.0333 [-0.1000, +0.1504] [-0.1111, +0.1563] | +0.0000 [-0.1333, +0.1167] [-0.1207, +0.0927] | +0.0167 [-0.0750, +0.1083] [-0.0693, +0.0965] |
| E2 mini counts-only minus intact | -0.1655* [-0.2264, -0.0980] [-0.2349, -0.1013] | -0.2614* [-0.3409, -0.1875] [-0.3483, -0.1826] | +0.0167 [-0.1500, +0.1667] [-0.1667, +0.1786] | -0.0667 [-0.2000, +0.0667] [-0.1936, +0.0518] | -0.0250 [-0.1250, +0.0750] [-0.1167, +0.0741] |
| E2 mini counts-only minus names-only | -0.1554* [-0.2196, -0.0911] [-0.2318, -0.0839] | -0.2614* [-0.3354, -0.1818] [-0.3489, -0.1741] | +0.0500 [-0.0833, +0.1833] [-0.0857, +0.2000] | -0.0500 [-0.1833, +0.0833] [-0.2241, +0.0883] | +0.0000 [-0.1000, +0.0917] [-0.1154, +0.1111] |
| E2 mini names-only dash minus intact | -0.0270 [-0.0743, +0.0169] [-0.0686, +0.0159] | +0.0000 [-0.0511, +0.0511] [-0.0556, +0.0573] | -0.1167 [-0.2500, +0.0000] [-0.2500, +0.0000] | -0.0167 [-0.1000, +0.0833] [-0.1168, +0.0962] | -0.0667 [-0.1417, +0.0167] [-0.1482, +0.0089] |
| E2 mini names-only minus intact | -0.0101 [-0.0541, +0.0338] [-0.0516, +0.0292] | +0.0000 [-0.0511, +0.0511] [-0.0402, +0.0430] | -0.0333 [-0.1667, +0.1000] [-0.1613, +0.1000] | -0.0167 [-0.1000, +0.0833] [-0.1168, +0.0962] | -0.0250 [-0.1002, +0.0583] [-0.1032, +0.0606] |
| Haiku draw 1 minus five draws (v2) | -0.0236* [-0.0439, -0.0034] [-0.0411, -0.0068] | -0.0227* [-0.0455, -0.0057] [-0.0449, -0.0056] | -0.0167 [-0.0833, +0.0333] [-0.0781, +0.0333] | -0.0333 [-0.0833, +0.0000] [-0.0833, +0.0000] | -0.0250 [-0.0667, +0.0083] [-0.0603, +0.0082] |
| Haiku minus guessed-category count reader | +0.1284* [+0.0608, +0.1959] [+0.0700, +0.1871] | +0.2500* [+0.1875, +0.3125] [+0.1774, +0.3247] | -0.1000 [-0.2667, +0.0667] [-0.2500, +0.0589] | +0.0000 [-0.1500, +0.1500] [-0.1667, +0.1724] | -0.0500 [-0.1667, +0.0667] [-0.1635, +0.0703] |
| Haiku minus hybrid | -0.0338 [-0.0845, +0.0169] [-0.0928, +0.0224] | -0.0341 [-0.0795, +0.0057] [-0.0769, +0.0103] | -0.0667 [-0.2333, +0.1000] [-0.2344, +0.1000] | +0.0000 [-0.1500, +0.1500] [-0.1667, +0.1724] | -0.0333 [-0.1502, +0.0833] [-0.1531, +0.0873] |
| Luna draw 1 minus five draws (v2) | +0.0068 [-0.0473, +0.0608] [-0.0493, +0.0640] | +0.0000 [-0.0227, +0.0286] [-0.0238, +0.0352] | -0.0167 [-0.1833, +0.1500] [-0.1724, +0.1500] | +0.0500 [-0.1167, +0.2333] [-0.1452, +0.2931] | +0.0167 [-0.0917, +0.1417] [-0.1250, +0.1520] |
| Luna minus guessed-category count reader | +0.1284* [+0.0506, +0.2061] [+0.0685, +0.1973] | +0.2784* [+0.2214, +0.3409] [+0.2111, +0.3395] | -0.1667 [-0.4167, +0.0500] [-0.3393, +0.0167] | -0.0167 [-0.2167, +0.1504] [-0.2344, +0.2037] | -0.0917 [-0.2333, +0.0583] [-0.2500, +0.0784] |
| Luna minus hybrid | -0.0338 [-0.0912, +0.0270] [-0.0973, +0.0315] | -0.0057 [-0.0284, +0.0170] [-0.0284, +0.0115] | -0.1333 [-0.3667, +0.0833] [-0.3333, +0.0626] | -0.0167 [-0.2167, +0.1504] [-0.2344, +0.2037] | -0.0750 [-0.2167, +0.0667] [-0.2427, +0.1021] |
| Opus draw 1 minus five draws (v2) | -0.0068 [-0.0473, +0.0338] [-0.0568, +0.0552] | -0.0114 [-0.0284, +0.0000] [-0.0278, +0.0000] | +0.0000 [-0.1500, +0.1333] [-0.1800, +0.1820] | +0.0000 [-0.1333, +0.1333] [-0.1251, +0.1250] | +0.0000 [-0.0919, +0.1002] [-0.1269, +0.1172] |
| Opus minus guessed-category count reader | +0.2027* [+0.1284, +0.2669] [+0.1319, +0.2742] | +0.2841* [+0.2216, +0.3466] [+0.2184, +0.3466] | +0.0500 [-0.1333, +0.2333] [-0.1034, +0.1936] | +0.1167 [-0.0833, +0.3004] [-0.1071, +0.3393] | +0.0833 [-0.0583, +0.2167] [-0.0597, +0.2289] |
| Opus minus hybrid | +0.0405 [-0.0169, +0.0980] [-0.0226, +0.1007] | +0.0000 [-0.0341, +0.0284] [-0.0284, +0.0244] | +0.0833 [-0.1167, +0.2667] [-0.0926, +0.2759] | +0.1167 [-0.0833, +0.3004] [-0.1071, +0.3393] | +0.1000 [-0.0500, +0.2333] [-0.0492, +0.2501] |
| Sol draw 1 minus five draws (v2) | -0.0304 [-0.1014, +0.0439] [-0.0844, +0.0197] | -0.0511 [-0.1080, -0.0057] [-0.1104, +0.0000] | +0.1167 [-0.1500, +0.3504] [-0.0894, +0.3500] | -0.1167 [-0.2833, +0.0500] [-0.2362, +0.0192] | +0.0000 [-0.1333, +0.1500] [-0.1466, +0.1408] |
| Sol minus guessed-category count reader | +0.1419* [+0.0642, +0.2162] [+0.0897, +0.1954] | +0.2557* [+0.1932, +0.3239] [+0.1848, +0.3248] | -0.1667 [-0.4167, +0.0337] [-0.4108, +0.0469] | +0.1167 [-0.0500, +0.3000] [-0.1061, +0.3065] | -0.0250 [-0.1669, +0.1252] [-0.1553, +0.1016] |
| Sol minus hybrid (P-H2) | -0.0203 [-0.0811, +0.0405] [-0.0813, +0.0382] | -0.0284 [-0.0682, +0.0057] [-0.0645, +0.0066] | -0.1333 [-0.3667, +0.0833] [-0.4038, +0.0968] | +0.1167 [-0.0500, +0.3000] [-0.1061, +0.3065] | -0.0083 [-0.1502, +0.1417] [-0.1471, +0.1191] |
| all-states Haiku minus sup-only | +0.0980* [+0.0507, +0.1486] [+0.0410, +0.1447] | -0.0341 [-0.0795, +0.0057] [-0.0798, +0.0051] | +0.3167* [+0.2000, +0.4333] [+0.1851, +0.4310] | +0.2667* [+0.1500, +0.3833] [+0.1250, +0.4001] | +0.2917* [+0.2083, +0.3750] [+0.2000, +0.3796] |
| all-states Opus minus sup-only | +0.0676* [+0.0236, +0.1149] [+0.0199, +0.1319] | +0.0057 [-0.0114, +0.0341] [-0.0169, +0.0326] | +0.1167 [-0.0167, +0.2667] [+0.0000, +0.2576] | +0.2000* [+0.0667, +0.3667] [+0.0357, +0.3667] | +0.1583* [+0.0583, +0.2750] [+0.0447, +0.2762] |
| all-states lookup minus name lookup | +0.1453* [+0.1081, +0.1859] [+0.1064, +0.1809] | -0.0170 [-0.0398, +0.0000] [-0.0354, +0.0000] | +0.3667* [+0.2833, +0.4333] [+0.2812, +0.4483] | +0.4000* [+0.3333, +0.4667] [+0.3333, +0.4545] | +0.3833* [+0.3333, +0.4335] [+0.3333, +0.4340] |
| all-states mini k1 minus sup-only | +0.1047* [+0.0574, +0.1554] [+0.0594, +0.1523] | +0.0057 [-0.0398, +0.0513] [-0.0380, +0.0529] | +0.4000* [+0.2833, +0.5167] [+0.2903, +0.5000] | +0.1000 [+0.0000, +0.2000] [+0.0143, +0.2097] | +0.2500* [+0.1583, +0.3333] [+0.1639, +0.3396] |
| all-states mini k5 minus sup-only | +0.0270 [-0.0304, +0.0845] [-0.0346, +0.0799] | +0.0057 [-0.0341, +0.0455] [-0.0319, +0.0568] | +0.1333 [-0.0004, +0.3000] [+0.0000, +0.2905] | -0.0167 [-0.2167, +0.1833] [-0.1970, +0.1833] | +0.0583 [-0.0583, +0.1833] [-0.0492, +0.1750] |
| bge-small minus MiniLM (v2) | +0.0034 [+0.0000, +0.0101] [+0.0000, +0.0106] | +0.0057 [+0.0000, +0.0170] [+0.0000, +0.0206] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] |
| hybrid minus guessed-category count reader | +0.1622* [+0.1182, +0.2061] [+0.1194, +0.2118] | +0.2841* [+0.2330, +0.3409] [+0.2184, +0.3457] | -0.0333 [-0.1000, +0.0000] [-0.1034, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | -0.0167 [-0.0500, +0.0000] [-0.0545, +0.0000] |
| hybrid minus name lookup (P-H1) | +0.0743* [+0.0338, +0.1149] [+0.0357, +0.1149] | +0.0057 [+0.0000, +0.0170] [+0.0000, +0.0179] | +0.2000* [+0.0667, +0.3333] [+0.0483, +0.3572] | +0.1500* [+0.0167, +0.2833] [+0.0370, +0.2581] | +0.1750* [+0.0750, +0.2750] [+0.0873, +0.2673] |
| intent-explicit Luna minus main-study | +0.0541 [-0.0068, +0.1149] [+0.0000, +0.1111] | -0.0227 [-0.0568, +0.0000] [-0.0544, +0.0000] | +0.1333 [-0.0342, +0.3333] [-0.0391, +0.3078] | +0.2000 [-0.0008, +0.4333] [+0.0312, +0.3824] | +0.1667* [+0.0167, +0.3000] [+0.0416, +0.2951] |
| intent-explicit mini minus main-study | +0.0000 [-0.0372, +0.0439] [-0.0385, +0.0363] | +0.0114 [-0.0341, +0.0568] [-0.0272, +0.0521] | +0.0333 [-0.0667, +0.1500] [-0.0893, +0.1564] | -0.0667 [-0.1833, +0.0333] [-0.1667, +0.0385] | -0.0167 [-0.0919, +0.0502] [-0.0866, +0.0588] |
| mini five draws minus one draw (v2) | +0.1115* [+0.0574, +0.1689] [+0.0657, +0.1558] | +0.0511 [+0.0000, +0.1080] [+0.0056, +0.1022] | +0.2500* [+0.0667, +0.4000] [+0.0667, +0.4062] | +0.1500* [+0.0167, +0.3000] [+0.0310, +0.2647] | +0.2000* [+0.0750, +0.3000] [+0.0982, +0.2885] |
| mini five draws minus one draw (v3) | +0.0338 [-0.0135, +0.0744] [-0.0104, +0.0769] | +0.0511 [+0.0000, +0.0967] [+0.0000, +0.1000] | -0.0167 [-0.1167, +0.0667] [-0.1200, +0.0577] | +0.0333 [-0.1167, +0.1833] [-0.1168, +0.1731] | +0.0083 [-0.0750, +0.0917] [-0.0794, +0.0900] |
| mini k1 minus guessed-category count reader | +0.0507 [-0.0203, +0.1116] [-0.0035, +0.1071] | +0.1818* [+0.1193, +0.2443] [+0.1111, +0.2500] | -0.1833 [-0.3667, +0.0000] [-0.3549, +0.0156] | -0.1000 [-0.2500, +0.0500] [-0.2334, +0.0345] | -0.1417* [-0.2583, -0.0248] [-0.2467, -0.0444] |
| mini k1 minus hybrid | -0.1115* [-0.1690, -0.0574] [-0.1689, -0.0533] | -0.1023* [-0.1477, -0.0511] [-0.1559, -0.0494] | -0.1500 [-0.3167, +0.0171] [-0.3462, +0.0385] | -0.1000 [-0.2500, +0.0500] [-0.2334, +0.0345] | -0.1250* [-0.2417, -0.0083] [-0.2322, -0.0278] |
| mini k5 minus guessed-category count reader | +0.1622* [+0.0946, +0.2297] [+0.1032, +0.2181] | +0.2330* [+0.1591, +0.3011] [+0.1628, +0.3012] | +0.0667 [-0.1500, +0.2667] [-0.1429, +0.2273] | +0.0500 [-0.1167, +0.1833] [-0.1035, +0.1667] | +0.0583 [-0.0752, +0.1917] [-0.0589, +0.1591] |
| mini k5 minus hybrid | +0.0000 [-0.0608, +0.0677] [-0.0576, +0.0571] | -0.0511* [-0.1023, -0.0057] [-0.1118, -0.0059] | +0.1000 [-0.1167, +0.3167] [-0.1380, +0.2969] | +0.0500 [-0.1167, +0.1833] [-0.1035, +0.1667] | +0.0750 [-0.0750, +0.2085] [-0.0521, +0.1910] |
| moved count Haiku minus sup-only | -0.0270 [-0.0677, +0.0102] [-0.0658, +0.0222] | +0.0000 [-0.0227, +0.0227] [-0.0227, +0.0230] | -0.0500 [-0.2000, +0.1000] [-0.2258, +0.1379] | -0.0833 [-0.1833, +0.0000] [-0.1400, -0.0303] | -0.0667 [-0.1583, +0.0169] [-0.1618, +0.0263] |
| moved count Luna draw 1 minus sup-only draw 1 | -0.0507 [-0.1284, +0.0170] [-0.1166, +0.0069] | -0.0284 [-0.0795, +0.0170] [-0.0756, +0.0115] | -0.1833 [-0.4167, +0.0667] [-0.4038, +0.0000] | +0.0167 [-0.2333, +0.2500] [-0.1482, +0.1668] | -0.0833 [-0.2500, +0.0667] [-0.2245, +0.0472] |
| moved count Luna k5 minus sup-only k5 (E9) | -0.0709* [-0.1453, -0.0068] [-0.1443, -0.0106] | -0.0284 [-0.0909, +0.0227] [-0.0714, +0.0130] | -0.1667 [-0.3667, +0.0333] [-0.3929, +0.0333] | -0.1000 [-0.3000, +0.1000] [-0.2904, +0.0770] | -0.1333 [-0.2671, +0.0000] [-0.3051, +0.0299] |
| moved count Opus draw 1 minus sup-only draw 1 | -0.1149* [-0.1791, -0.0574] [-0.1897, -0.0507] | +0.0000 [-0.0227, +0.0227] [-0.0169, +0.0167] | -0.2500* [-0.4333, -0.0500] [-0.3939, -0.0861] | -0.3167* [-0.5333, -0.1167] [-0.5517, -0.0937] | -0.2833* [-0.4250, -0.1415] [-0.4238, -0.1333] |
| moved count Opus draw 1 minus sup-only k5 (registered) | -0.1216* [-0.1859, -0.0574] [-0.1921, -0.0504] | -0.0114 [-0.0284, +0.0000] [-0.0275, +0.0000] | -0.2500 [-0.4667, +0.0000] [-0.4630, -0.0255] | -0.3167* [-0.5167, -0.1167] [-0.5173, -0.1060] | -0.2833* [-0.4252, -0.1083] [-0.4465, -0.1249] |
| moved count Opus k5 minus sup-only k5 | -0.0743 [-0.1351, -0.0101] [-0.1418, +0.0037] | +0.0057 [-0.0114, +0.0341] [-0.0169, +0.0326] | -0.1833 [-0.4004, +0.0333] [-0.4355, +0.0676] | -0.2000 [-0.4000, +0.0000] [-0.4138, +0.0556] | -0.1917* [-0.3333, -0.0417] [-0.3645, -0.0172] |
| moved count Sol draw 1 minus sup-only draw 1 | -0.0642 [-0.1385, +0.0068] [-0.1397, +0.0108] | +0.0227 [-0.0227, +0.0740] [-0.0266, +0.0750] | -0.0667 [-0.2667, +0.1333] [-0.2694, +0.1130] | -0.3167* [-0.5333, -0.0667] [-0.5484, -0.0781] | -0.1917* [-0.3502, -0.0498] [-0.3585, -0.0249] |
| moved count Sol k5 minus sup-only k5 (E9) | -0.0439 [-0.1149, +0.0270] [-0.1045, +0.0180] | +0.0057 [+0.0000, +0.0170] [+0.0000, +0.0172] | +0.1000 [-0.1333, +0.3333] [-0.1381, +0.3462] | -0.3333* [-0.5333, -0.1333] [-0.4667, -0.1538] | -0.1167 [-0.3000, +0.0500] [-0.2712, +0.0417] |
| moved count mini minus sup-only | +0.0236 [-0.0204, +0.0676] [-0.0229, +0.0714] | -0.0114 [-0.0511, +0.0284] [-0.0536, +0.0238] | +0.0000 [-0.1167, +0.1167] [-0.1129, +0.1406] | +0.1500* [+0.0333, +0.2667] [+0.0625, +0.2426] | +0.0750 [-0.0083, +0.1583] [-0.0094, +0.1667] |
| mpnet minus MiniLM (v2) | -0.0034 [-0.0101, +0.0000] [-0.0115, +0.0000] | -0.0057 [-0.0170, +0.0000] [-0.0185, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] |
| name lookup minus guessed-category count reader | +0.0878* [+0.0270, +0.1486] [+0.0294, +0.1446] | +0.2784* [+0.2273, +0.3352] [+0.2126, +0.3418] | -0.2333* [-0.3500, -0.1000] [-0.3621, -0.1061] | -0.1500* [-0.2833, -0.0167] [-0.2581, -0.0370] | -0.1917* [-0.2917, -0.0917] [-0.2740, -0.1111] |
| random-token minus all-states lookup (v3) | -0.3142* [-0.3581, -0.2669] [-0.3611, -0.2601] | -0.3523* [-0.3977, -0.3011] [-0.4000, -0.2980] | -0.3000* [-0.4000, -0.1996] [-0.3871, -0.2031] | -0.2167* [-0.3171, -0.1000] [-0.3167, -0.0967] | -0.2583* [-0.3333, -0.1833] [-0.3333, -0.1838] |
| random-token minus name lookup (v2) | -0.1318* [-0.1724, -0.0912] [-0.1786, -0.0854] | -0.2216* [-0.2841, -0.1646] [-0.2889, -0.1506] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] |
| totals rand. Haiku minus sup-only | +0.0000 [-0.0339, +0.0372] [-0.0328, +0.0393] | -0.0114 [-0.0341, +0.0114] [-0.0345, +0.0112] | +0.0167 [-0.1167, +0.1500] [-0.1482, +0.1515] | +0.0167 [-0.0333, +0.0667] [-0.0345, +0.0741] | +0.0167 [-0.0583, +0.0917] [-0.0546, +0.0916] |
| totals rand. Opus minus sup-only | -0.0034 [-0.0507, +0.0439] [-0.0584, +0.0748] | +0.0057 [+0.0000, +0.0170] [+0.0000, +0.0183] | +0.0167 [-0.1667, +0.2000] [-0.2143, +0.2500] | -0.0500 [-0.2000, +0.1000] [-0.2308, +0.1034] | -0.0167 [-0.1333, +0.1083] [-0.1667, +0.1324] |
| totals rand. mini minus sup-only | +0.0236 [-0.0203, +0.0642] [-0.0038, +0.0544] | +0.0170 [-0.0284, +0.0568] [-0.0155, +0.0562] | +0.0333 [-0.0833, +0.1500] [-0.0862, +0.1539] | +0.0333 [-0.0833, +0.1500] [-0.0536, +0.1250] | +0.0333 [-0.0500, +0.1083] [-0.0300, +0.1066] |

### AUX-CF2-R125-FIG3 — Figure 3's data on the matched metric (`reviews/r125/results/fig3_data_matched.tex`)

```
%% fig3_data_matched.tex -- Figure 3's data ON THE MATCHED METRIC, written by reviews/r125/tools/r125_t1_report.py from reviews/r125/results/r125_matched.json (R125, Task 1); do not edit by hand.
%% The same schema as reviews/v22/src/fig3_data.tex (\figthreeSup, \figthreeAll; x: 0 supersession, 1 retraction, 2 expiry). Every value is the within-triple matched AUROC (W + T/2) / n of the
%% PN version against the PRESENT version, over the state's own triples (88 / 30 / 30), four decimals. Post hoc. Sources (reader keys of r125_matched.json 'readers'):
%%   mini                   MINI5_v2: supersession 0.8920 (76/5/7), retraction 0.5667 (15/4/11), expiry 0.4000 (9/6/15)
%%   haiku                  H45_v2: supersession 0.9148 (76/9/3), retraction 0.5667 (6/22/2), expiry 0.5833 (7/21/2)
%%   luna                   LUNA_v2: supersession 0.9602 (84/1/3), retraction 0.6500 (19/1/10), expiry 0.8667 (26/0/4)
%%   sol                    SOL_v2: supersession 0.9602 (84/1/3), retraction 0.5833 (17/1/12), expiry 0.8333 (25/0/5)
%%   opus                   OP5_v2: supersession 0.9773 (86/0/2), retraction 0.7667 (22/2/6), expiry 0.6833 (20/1/9)
%%   lookup                 LOOKUP_v2: supersession 0.9659 (82/6/0), retraction 0.5000 (0/30/0), expiry 0.5000 (0/30/0)
%%   count                  CR-nb1_v2: supersession 0.6932 (34/54/0), retraction 0.7667 (16/14/0), expiry 0.7500 (15/15/0)
%%   mini (all states)      MINI5_v3: supersession 0.9205 (80/2/6), retraction 0.9333 (28/0/2), expiry 0.7833 (22/3/5)
%%   haiku (all states)     H45_v3: supersession 0.8920 (73/11/4), retraction 0.9333 (27/2/1), expiry 0.9167 (25/5/0)
%%   opus (all states)      OP5_v3: supersession 0.9659 (85/0/3), retraction 0.8333 (25/0/5), expiry 0.9667 (29/0/1)
%%   lookup (all states)    ALLSTATES_v3: supersession 0.9432 (78/10/0), retraction 0.8167 (19/11/0), expiry 0.9000 (24/6/0)
\pgfplotstableread[col sep=comma]{
x,state,mini,haiku,luna,sol,opus,lookup,count
0,Supersession,0.8920,0.9148,0.9602,0.9602,0.9773,0.9659,0.6932
1,Retraction,0.5667,0.5667,0.6500,0.5833,0.7667,0.5000,0.7667
2,Expiry,0.4000,0.5833,0.8667,0.8333,0.6833,0.5000,0.7500
}\figthreeSup
\pgfplotstableread[col sep=comma]{
x,state,mini,haiku,opus,lookup
0,Supersession,0.9205,0.8920,0.9659,0.9432
1,Retraction,0.9333,0.9333,0.8333,0.8167
2,Expiry,0.7833,0.9167,0.9667,0.9000
}\figthreeAll
```

<!-- R125-T1 END -->

<!-- R125-T2 BEGIN (written by reviews/r125/tools/r125_t23_report.py; do not edit by hand) -->

## 15b. AUX-CF2-R125-T2 — how much of the lookup is list emptiness (program R125, Task 2; 2026-09-20; post hoc, offline, no model call; `reviews/r125/tools/r125_t2_emptiness.py`; `reviews/r125/results/r125_t2_emptiness.json`)

### AUX-CF2-R125-T2-CENSUS — the superseded-names list per version (v2; the all-states lists under v3)

| pairs | version | empty lists | length histogram | mean length |
|---|---|---:|---|---:|
| SUPERSESSION (88) | PN | 0 | {'1': 23, '2': 17, '3': 25, '4': 17, '5': 5, '6': 1} | 2.6250 |
| SUPERSESSION (88) | PRESENT | 24 | {'0': 24, '1': 16, '2': 31, '3': 12, '4': 4, '5': 1} | 1.5341 |
| SUPERSESSION (88) | ABSENT | 24 | {'0': 24, '1': 16, '2': 31, '3': 12, '4': 4, '5': 1} | 1.5341 |
| SUPERSESSION (88) | PN minus PRESENT | | {'1': 81, '2': 6, '3': 1} | pairs with PRESENT empty and PN not: 24 |
| RETRACTION (30) | PN | 6 | {'0': 6, '1': 7, '2': 11, '3': 2, '4': 4} | 1.7000 |
| RETRACTION (30) | PRESENT | 6 | {'0': 6, '1': 7, '2': 11, '3': 2, '4': 4} | 1.7000 |
| RETRACTION (30) | ABSENT | 6 | {'0': 6, '1': 7, '2': 11, '3': 2, '4': 4} | 1.7000 |
| RETRACTION (30) | PN minus PRESENT | | {'0': 30} | pairs with PRESENT empty and PN not: 0 |
| EXPIRY (30) | PN | 10 | {'0': 10, '1': 5, '2': 9, '3': 4, '4': 2} | 1.4333 |
| EXPIRY (30) | PRESENT | 10 | {'0': 10, '1': 5, '2': 9, '3': 4, '4': 2} | 1.4333 |
| EXPIRY (30) | ABSENT | 10 | {'0': 10, '1': 5, '2': 9, '3': 4, '4': 2} | 1.4333 |
| EXPIRY (30) | PN minus PRESENT | | {'0': 30} | pairs with PRESENT empty and PN not: 0 |
| ALL (148) | PN | 16 | {'0': 16, '1': 35, '2': 37, '3': 31, '4': 23, '5': 5, '6': 1} | 2.1959 |
| ALL (148) | PRESENT | 40 | {'0': 40, '1': 28, '2': 51, '3': 18, '4': 10, '5': 1} | 1.5473 |
| ALL (148) | ABSENT | 40 | {'0': 40, '1': 28, '2': 51, '3': 18, '4': 10, '5': 1} | 1.5473 |
| ALL (148) | PN minus PRESENT | | {'0': 60, '1': 81, '2': 6, '3': 1} | pairs with PRESENT empty and PN not: 24 |

Under the all-states summary (v3), the counted-state pairs' own lists:

| pairs | section | version | empty | length histogram |
|---|---|---|---:|---|
| RETRACTION | retracted | PN | 0 | {'1': 24, '2': 6} |
| RETRACTION | retracted | PRESENT | 26 | {'0': 26, '1': 4} |
| RETRACTION | retracted | ABSENT | 26 | {'0': 26, '1': 4} |
| EXPIRY | expired | PN | 0 | {'10': 1, '2': 1, '3': 2, '4': 9, '5': 3, '6': 4, '7': 5, '8': 4, '9': 1} |
| EXPIRY | expired | PRESENT | 0 | {'1': 1, '2': 5, '3': 9, '4': 3, '5': 4, '6': 6, '8': 2} |
| EXPIRY | expired | ABSENT | 0 | {'1': 1, '2': 5, '3': 9, '4': 3, '5': 4, '6': 6, '8': 2} |
| SUPERSESSION | superseded | PN | 0 | {'1': 23, '2': 17, '3': 25, '4': 17, '5': 5, '6': 1} |
| SUPERSESSION | superseded | PRESENT | 24 | {'0': 24, '1': 16, '2': 31, '3': 12, '4': 4, '5': 1} |
| SUPERSESSION | superseded | ABSENT | 24 | {'0': 24, '1': 16, '2': 31, '3': 12, '4': 4, '5': 1} |

### AUX-CF2-R125-T2-RANDOM — the random-token control per state and under the matched metric (444), per state on the 661

| population | reader | pooled whole | pooled sup / ret / exp | matched PN vs PRESENT whole (W/T/L) | triple | persona | matched sup / ret / exp | matched PN vs ABSENT whole |
|---|---|---:|---|---|---|---|---|---:|
| 444 v2 | random token | 0.5954 | 0.6651 / 0.5000 / 0.5000 | 0.6453 (45/101/2) | [0.6081, 0.6858] | [0.6014, 0.6926] | 0.7443 / 0.5000 / 0.5000 | 0.6453 |
| 444 v2 | lookup | 0.7663 | 0.9223 / 0.5000 / 0.5000 | 0.7770 (82/66/0) | [0.7365, 0.8176] | [0.7346, 0.8188] | 0.9659 / 0.5000 / 0.5000 | — |
| 444 v3 | random token | 0.5479 | 0.5385 / 0.5697 / 0.5694 | 0.6047 (31/117/0) | [0.5777, 0.6385] | [0.5680, 0.6460] | 0.5966 / 0.5500 / 0.6833 | 0.6081 |
| 444 v3 | lookup | 0.8756 | 0.8995 / 0.7975 / 0.8711 | 0.9088 (121/27/0) | [0.8783, 0.9392] | [0.8785, 0.9379] | 0.9432 / 0.8167 / 0.9000 | — |
| 661 committed | random token | 0.6654 | 0.7389 / 0.6032 / 0.4647 (positives of one state against all 557 negatives) | not defined (no triples) | | | | |
| 661 committed | lookup | 0.7484 | 0.9534 / 0.4053 / 0.4823 (positives of one state against all 557 negatives) | not defined (no triples) | | | | |
| 661 committed | census | empty lists 0 of 661 (0 positives); mean length 1.7474 | | | | | | |
| 661 marker_free | random token | 0.6627 | 0.7764 / 0.6134 / 0.2706 (positives of one state against all 557 negatives) | not defined (no triples) | | | | |
| 661 marker_free | lookup | 0.7442 | 0.9599 / 0.5026 / 0.2570 (positives of one state against all 557 negatives) | not defined (no triples) | | | | |
| 661 marker_free | census | empty lists 195 of 661 (17 positives); mean length 1.4523 | | | | | | |

### AUX-CF2-R125-T2-DIFF — the name lookup minus the random-token control, paired, both intervals, under both metrics

| population | scope | pooled Δ (item; persona) | matched PN vs PRESENT Δ (triple; persona) | matched PN vs ABSENT Δ |
|---|---|---|---|---|
| 444 v2 | whole | +0.1709 [+0.1218, +0.2218] [+0.1284, +0.2132] **reliable** | +0.1318 [+0.0912, +0.1724] [+0.0854, +0.1786] **reliable** | +0.1318 [+0.0912, +0.1724] [+0.0854, +0.1786] **reliable** |
| 444 v2 | supersession | +0.2572 [+0.1894, +0.3244] [+0.1993, +0.3081] **reliable** | +0.2216 [+0.1646, +0.2841] [+0.1506, +0.2889] **reliable** | +0.2216 [+0.1646, +0.2841] [+0.1506, +0.2889] **reliable** |
| 444 v2 | retraction | +0.0000 [-0.1348, +0.1401] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] |
| 444 v2 | expiry | +0.0000 [-0.0835, +0.0775] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] [+0.0000, +0.0000] |
| 444 v3 | whole | +0.3277 [+0.2576, +0.3925] [+0.2928, +0.3631] **reliable** | +0.3041 [+0.2568, +0.3447] [+0.2516, +0.3493] **reliable** | +0.3142 [+0.2669, +0.3581] [+0.2601, +0.3611] **reliable** |
| 444 v3 | supersession | +0.3610 [+0.2775, +0.4424] [+0.3157, +0.4052] **reliable** | +0.3466 [+0.2955, +0.3977] [+0.2903, +0.3987] **reliable** | +0.3523 [+0.3011, +0.3977] [+0.2980, +0.4000] **reliable** |
| 444 v3 | retraction | +0.2278 [+0.0631, +0.3722] [+0.1206, +0.3278] **reliable** | +0.2667 [+0.1667, +0.3500] [+0.1724, +0.3542] **reliable** | +0.3000 [+0.1996, +0.4000] [+0.2031, +0.3871] **reliable** |
| 444 v3 | expiry | +0.3017 [+0.1476, +0.4480] [+0.2218, +0.3746] **reliable** | +0.2167 [+0.1000, +0.3171] [+0.0967, +0.3167] **reliable** | +0.2167 [+0.1000, +0.3171] [+0.0967, +0.3167] **reliable** |
| 661 committed | whole | +0.0830 [+0.0076, +0.1654] [-0.0097, +0.1826] | not defined | |
| 661 committed | supersession | +0.2146 [+0.1452, +0.2915] [+0.1166, +0.3383] **reliable** | | |
| 661 committed | retraction | -0.1980 [-0.3256, -0.0591] [-0.3908, +0.0126] | | |
| 661 committed | expiry | +0.0176 [-0.2133, +0.2621] [-0.3800, +0.4269] | | |
| 661 marker_free | whole | +0.0815 [+0.0270, +0.1438] [+0.0164, +0.1603] **reliable** | not defined | |
| 661 marker_free | supersession | +0.1835 [+0.1212, +0.2560] [+0.0954, +0.2958] **reliable** | | |
| 661 marker_free | retraction | -0.1108 [-0.2082, -0.0048] [-0.2552, +0.0420] | | |
| 661 marker_free | expiry | -0.0135 [-0.0671, +0.0352] [-0.0910, +0.0475] | | |

<!-- R125-T2 END -->

<!-- R125-T3 BEGIN (written by reviews/r125/tools/r125_t23_report.py; do not edit by hand) -->

## 15c. AUX-CF2-R125-T3 — labels relative to what each backend retains (program R125, Task 3; 2026-09-20; post hoc, offline, no model call; `reviews/r125/tools/r125_t3_frbank.py`, `r125_t3_graphiti.py`, `r125_t3_sheet.py`; `reviews/r125/results/r125_t3_*.json`; the Graphiti edges exported once from the local neo4j-r85 container to `reviews/r125/build/graphiti_edges_g10.json`)

### AUX-CF2-R125-T3-FRBANK — FR-Bank's 104 obligations relative to what the store retains (the join at three bars; the store's own marks)

Members stored for 104 of 104 (by construction). Join-marked: 0.50: 95 {'exp': 11, 'ret': 21, 'sup': 63}; 0.75: 84 {'exp': 11, 'ret': 10, 'sup': 63}; 0.80: 82 {'exp': 11, 'ret': 8, 'sup': 63}. Own-marked (FR-Bank's own non-active mark on a member): 73 {'exp': 5, 'ret': 20, 'sup': 48}. Cross (join at 0.80, own): {'join=False,own=False': 5, 'join=False,own=True': 17, 'join=True,own=False': 26, 'join=True,own=True': 56}.

| stratum (positives; the 557 negatives unchanged) | n_pos | by state | mini GT | mini capped | mini lifted | Haiku GT | Haiku capped | Haiku lifted | lookup GT | lookup capped | lookup lifted | mini blind |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all_104 (manifest-relative, the printed rows) | 104 | {'exp': 15, 'ret': 26, 'sup': 63} | 0.7339 | 0.5959 | 0.6513 | 0.8210 | 0.7069 | 0.7364 | 0.7484 | 0.5858 | 0.6588 | 0.4946 |
| join_marked_0.50 | 95 | {'exp': 11, 'ret': 21, 'sup': 63} | 0.7571 | 0.6193 | 0.6750 | 0.8358 | 0.7156 | 0.7473 | 0.7766 | 0.5942 | 0.6640 | 0.4946 |
| join_marked_0.75 | 84 | {'exp': 11, 'ret': 10, 'sup': 63} | 0.7866 | 0.6573 | 0.7180 | 0.8468 | 0.7235 | 0.7738 | 0.8177 | 0.6261 | 0.6986 | 0.4946 |
| join_marked_0.80 | 82 | {'exp': 11, 'ret': 8, 'sup': 63} | 0.7910 | 0.6636 | 0.7297 | 0.8515 | 0.7258 | 0.7821 | 0.8346 | 0.6319 | 0.7061 | 0.4946 |
| join_marked_0.80_and_own_active | 26 | {'exp': 9, 'ret': 2, 'sup': 15} | 0.7970 | 0.6411 | 0.6872 | 0.8196 | 0.7247 | 0.7037 | 0.6991 | 0.6068 | 0.6373 | 0.4946 |
| join_marked_0.80_and_own_marked | 56 | {'exp': 2, 'ret': 6, 'sup': 48} | 0.7883 | 0.6741 | 0.7494 | 0.8664 | 0.7262 | 0.8185 | 0.8975 | 0.6436 | 0.7381 | 0.4946 |
| join_unmarked_0.80 (the 22) | 22 | {'exp': 4, 'ret': 18} | 0.5210 | 0.3433 | 0.3591 | 0.7074 | 0.6368 | 0.5659 | 0.4272 | 0.4138 | 0.4822 | 0.4946 |
| own_active (no store mark on any member) | 31 | {'exp': 10, 'ret': 6, 'sup': 15} | 0.7276 | 0.5871 | 0.6244 | 0.7992 | 0.6919 | 0.6755 | 0.6324 | 0.6011 | 0.6175 | 0.4946 |
| own_marked | 73 | {'exp': 5, 'ret': 20, 'sup': 48} | 0.7366 | 0.5996 | 0.6627 | 0.8303 | 0.7133 | 0.7622 | 0.7977 | 0.5793 | 0.6763 | 0.4946 |
| state_exp_join_marked_0.80 | 11 | {'exp': 11} | 0.5633 | 0.5340 | 0.6669 | 0.7002 | 0.6787 | 0.6782 | 0.4683 | 0.4862 | 0.4981 | 0.4946 |
| state_exp_own_marked | 5 | {'exp': 5} | 0.3671 | 0.5804 | 0.7041 | 0.5526 | 0.7573 | 0.7147 | 0.6510 | 0.8352 | 0.7645 | 0.4946 |
| state_ret_join_marked_0.80 | 8 | {'ret': 8} | 0.5831 | 0.5477 | 0.5692 | 0.7588 | 0.7279 | 0.4933 | 0.4026 | 0.6246 | 0.5263 | 0.4946 |
| state_ret_own_marked | 20 | {'ret': 20} | 0.5601 | 0.3681 | 0.3791 | 0.7399 | 0.6779 | 0.5171 | 0.4588 | 0.3605 | 0.4292 | 0.4946 |
| state_sup_join_marked_0.80 | 63 | {'sup': 63} | 0.8572 | 0.7010 | 0.7610 | 0.8897 | 0.7337 | 0.8369 | 0.9534 | 0.6583 | 0.7653 | 0.4946 |
| state_sup_own_marked | 48 | {'sup': 48} | 0.8486 | 0.6980 | 0.7766 | 0.8969 | 0.7235 | 0.8693 | 0.9542 | 0.6437 | 0.7701 | 0.4946 |

The same rows with both single-arm intervals (item; persona) and, for the store-written rows, the paired store-written-minus-ground-truth difference (item; persona):

| stratum | reader | AUROC | item interval | persona interval | minus ground truth |
|---|---|---:|---|---|---|
| all_104 (manifest-relative, the printed rows) | GPT-4.1 mini, ground truth | 0.7339 | [0.6748, 0.7895] | [0.6502, 0.8186] |  |
| all_104 (manifest-relative, the printed rows) | GPT-4.1 mini, store-written capped | 0.5959 | [0.5404, 0.6501] | [0.5193, 0.6678] | -0.1380 [-0.1847, -0.0860] [-0.2244, -0.0654] **reliable** |
| all_104 (manifest-relative, the printed rows) | GPT-4.1 mini, store-written lifted | 0.6513 | [0.5903, 0.7105] | [0.5510, 0.7446] | -0.0826 [-0.1343, -0.0286] [-0.1657, -0.0150] **reliable** |
| all_104 (manifest-relative, the printed rows) | Haiku 4.5, ground truth | 0.8210 | [0.7747, 0.8635] | [0.7598, 0.8774] |  |
| all_104 (manifest-relative, the printed rows) | Haiku 4.5, store-written capped | 0.7069 | [0.6636, 0.7469] | [0.6620, 0.7541] | -0.1141 [-0.1646, -0.0597] [-0.1821, -0.0479] **reliable** |
| all_104 (manifest-relative, the printed rows) | Haiku 4.5, store-written lifted | 0.7364 | [0.6879, 0.7840] | [0.6665, 0.8024] | -0.0847 [-0.1340, -0.0307] [-0.1480, -0.0268] **reliable** |
| all_104 (manifest-relative, the printed rows) | Name lookup, ground-truth list | 0.7484 | [0.6842, 0.8108] | [0.6636, 0.8298] |  |
| all_104 (manifest-relative, the printed rows) | Name lookup, store-written capped list | 0.5858 | [0.5293, 0.6384] | [0.5002, 0.6653] | -0.1626 [-0.2307, -0.0996] [-0.2511, -0.0808] **reliable** |
| all_104 (manifest-relative, the printed rows) | Name lookup, store-written lifted list | 0.6588 | [0.6037, 0.7104] | [0.5777, 0.7319] | -0.0897 [-0.1498, -0.0383] [-0.1695, -0.0121] **reliable** |
| all_104 (manifest-relative, the printed rows) | GPT-4.1 mini, question only | 0.4946 | [0.4895, 0.4982] | [0.4858, 0.5000] |  |
| join_marked_0.50 | GPT-4.1 mini, ground truth | 0.7571 | [0.6956, 0.8153] | [0.6740, 0.8385] |  |
| join_marked_0.50 | GPT-4.1 mini, store-written capped | 0.6193 | [0.5609, 0.6755] | [0.5431, 0.6907] | -0.1378 [-0.1874, -0.0883] [-0.2220, -0.0633] **reliable** |
| join_marked_0.50 | GPT-4.1 mini, store-written lifted | 0.6750 | [0.6139, 0.7335] | [0.5785, 0.7656] | -0.0821 [-0.1311, -0.0323] [-0.1591, -0.0179] **reliable** |
| join_marked_0.50 | Haiku 4.5, ground truth | 0.8358 | [0.7902, 0.8772] | [0.7794, 0.8886] |  |
| join_marked_0.50 | Haiku 4.5, store-written capped | 0.7156 | [0.6700, 0.7598] | [0.6663, 0.7650] | -0.1202 [-0.1735, -0.0674] [-0.1886, -0.0529] **reliable** |
| join_marked_0.50 | Haiku 4.5, store-written lifted | 0.7473 | [0.6956, 0.7953] | [0.6793, 0.8136] | -0.0886 [-0.1362, -0.0407] [-0.1535, -0.0298] **reliable** |
| join_marked_0.50 | Name lookup, ground-truth list | 0.7766 | [0.7096, 0.8394] | [0.6965, 0.8564] |  |
| join_marked_0.50 | Name lookup, store-written capped list | 0.5942 | [0.5386, 0.6463] | [0.5120, 0.6680] | -0.1824 [-0.2482, -0.1128] [-0.2721, -0.1021] **reliable** |
| join_marked_0.50 | Name lookup, store-written lifted list | 0.6640 | [0.6097, 0.7168] | [0.5812, 0.7357] | -0.1126 [-0.1703, -0.0548] [-0.1953, -0.0377] **reliable** |
| join_marked_0.50 | GPT-4.1 mini, question only | 0.4946 | [0.4899, 0.4982] | [0.4858, 0.5000] |  |
| join_marked_0.75 | GPT-4.1 mini, ground truth | 0.7866 | [0.7289, 0.8488] | [0.7084, 0.8596] |  |
| join_marked_0.75 | GPT-4.1 mini, store-written capped | 0.6573 | [0.5970, 0.7202] | [0.5808, 0.7290] | -0.1292 [-0.1828, -0.0753] [-0.2040, -0.0520] **reliable** |
| join_marked_0.75 | GPT-4.1 mini, store-written lifted | 0.7180 | [0.6585, 0.7802] | [0.6224, 0.8017] | -0.0686 [-0.1219, -0.0121] [-0.1502, +0.0034] |
| join_marked_0.75 | Haiku 4.5, ground truth | 0.8468 | [0.8010, 0.8854] | [0.7876, 0.8962] |  |
| join_marked_0.75 | Haiku 4.5, store-written capped | 0.7235 | [0.6743, 0.7690] | [0.6687, 0.7760] | -0.1233 [-0.1738, -0.0676] [-0.1891, -0.0575] **reliable** |
| join_marked_0.75 | Haiku 4.5, store-written lifted | 0.7738 | [0.7234, 0.8237] | [0.7029, 0.8372] | -0.0730 [-0.1214, -0.0240] [-0.1423, -0.0103] **reliable** |
| join_marked_0.75 | Name lookup, ground-truth list | 0.8177 | [0.7526, 0.8785] | [0.7510, 0.8865] |  |
| join_marked_0.75 | Name lookup, store-written capped list | 0.6261 | [0.5713, 0.6790] | [0.5467, 0.7008] | -0.1916 [-0.2570, -0.1236] [-0.2723, -0.1192] **reliable** |
| join_marked_0.75 | Name lookup, store-written lifted list | 0.6986 | [0.6402, 0.7555] | [0.6175, 0.7717] | -0.1191 [-0.1789, -0.0598] [-0.1945, -0.0476] **reliable** |
| join_marked_0.75 | GPT-4.1 mini, question only | 0.4946 | [0.4901, 0.4982] | [0.4858, 0.5000] |  |
| join_marked_0.80 | GPT-4.1 mini, ground truth | 0.7910 | [0.7268, 0.8529] | [0.7108, 0.8653] |  |
| join_marked_0.80 | GPT-4.1 mini, store-written capped | 0.6636 | [0.6033, 0.7197] | [0.5845, 0.7341] | -0.1274 [-0.1813, -0.0731] [-0.2036, -0.0485] **reliable** |
| join_marked_0.80 | GPT-4.1 mini, store-written lifted | 0.7297 | [0.6751, 0.7877] | [0.6297, 0.8103] | -0.0614 [-0.1149, -0.0053] [-0.1425, +0.0099] |
| join_marked_0.80 | Haiku 4.5, ground truth | 0.8515 | [0.8044, 0.8938] | [0.7915, 0.9034] |  |
| join_marked_0.80 | Haiku 4.5, store-written capped | 0.7258 | [0.6771, 0.7720] | [0.6693, 0.7789] | -0.1258 [-0.1795, -0.0701] [-0.1913, -0.0600] **reliable** |
| join_marked_0.80 | Haiku 4.5, store-written lifted | 0.7821 | [0.7322, 0.8299] | [0.7125, 0.8460] | -0.0694 [-0.1185, -0.0204] [-0.1401, -0.0060] **reliable** |
| join_marked_0.80 | Name lookup, ground-truth list | 0.8346 | [0.7727, 0.8917] | [0.7674, 0.9045] |  |
| join_marked_0.80 | Name lookup, store-written capped list | 0.6319 | [0.5747, 0.6873] | [0.5548, 0.7039] | -0.2027 [-0.2721, -0.1319] [-0.2866, -0.1270] **reliable** |
| join_marked_0.80 | Name lookup, store-written lifted list | 0.7061 | [0.6481, 0.7576] | [0.6206, 0.7790] | -0.1285 [-0.1842, -0.0716] [-0.1993, -0.0615] **reliable** |
| join_marked_0.80 | GPT-4.1 mini, question only | 0.4946 | [0.4900, 0.4982] | [0.4858, 0.5000] |  |
| join_marked_0.80_and_own_active | GPT-4.1 mini, ground truth | 0.7970 | [0.6847, 0.8959] | [0.6288, 0.9179] |  |
| join_marked_0.80_and_own_active | GPT-4.1 mini, store-written capped | 0.6411 | [0.5195, 0.7535] | [0.4827, 0.7717] | -0.1559 [-0.2728, -0.0534] [-0.3386, +0.0235] |
| join_marked_0.80_and_own_active | GPT-4.1 mini, store-written lifted | 0.6872 | [0.5638, 0.7980] | [0.5059, 0.8418] | -0.1098 [-0.2079, -0.0224] [-0.2958, +0.0200] |
| join_marked_0.80_and_own_active | Haiku 4.5, ground truth | 0.8196 | [0.7521, 0.8764] | [0.7536, 0.8815] |  |
| join_marked_0.80_and_own_active | Haiku 4.5, store-written capped | 0.7247 | [0.6488, 0.7880] | [0.6399, 0.8045] | -0.0949 [-0.1784, -0.0207] [-0.2085, +0.0230] |
| join_marked_0.80_and_own_active | Haiku 4.5, store-written lifted | 0.7037 | [0.6114, 0.7853] | [0.5707, 0.8001] | -0.1159 [-0.2203, -0.0238] [-0.2949, +0.0070] |
| join_marked_0.80_and_own_active | Name lookup, ground-truth list | 0.6991 | [0.5686, 0.8271] | [0.5016, 0.8641] |  |
| join_marked_0.80_and_own_active | Name lookup, store-written capped list | 0.6068 | [0.5080, 0.7098] | [0.4472, 0.7548] | -0.0923 [-0.2070, +0.0356] [-0.2299, +0.0617] |
| join_marked_0.80_and_own_active | Name lookup, store-written lifted list | 0.6373 | [0.5343, 0.7380] | [0.4562, 0.7690] | -0.0618 [-0.1712, +0.0607] [-0.1887, +0.0533] |
| join_marked_0.80_and_own_active | GPT-4.1 mini, question only | 0.4946 | [0.4900, 0.4982] | [0.4858, 0.5000] |  |
| join_marked_0.80_and_own_marked | GPT-4.1 mini, ground truth | 0.7883 | [0.7081, 0.8628] | [0.6893, 0.8794] |  |
| join_marked_0.80_and_own_marked | GPT-4.1 mini, store-written capped | 0.6741 | [0.6037, 0.7405] | [0.5695, 0.7672] | -0.1142 [-0.1787, -0.0554] [-0.1910, -0.0284] **reliable** |
| join_marked_0.80_and_own_marked | GPT-4.1 mini, store-written lifted | 0.7494 | [0.6847, 0.8115] | [0.6377, 0.8404] | -0.0389 [-0.1064, +0.0301] [-0.1209, +0.0375] |
| join_marked_0.80_and_own_marked | Haiku 4.5, ground truth | 0.8664 | [0.8024, 0.9181] | [0.7782, 0.9315] |  |
| join_marked_0.80_and_own_marked | Haiku 4.5, store-written capped | 0.7262 | [0.6694, 0.7789] | [0.6546, 0.8005] | -0.1401 [-0.2063, -0.0727] [-0.2129, -0.0592] **reliable** |
| join_marked_0.80_and_own_marked | Haiku 4.5, store-written lifted | 0.8185 | [0.7628, 0.8710] | [0.7336, 0.8887] | -0.0478 [-0.1056, +0.0104] [-0.1171, +0.0188] |
| join_marked_0.80_and_own_marked | Name lookup, ground-truth list | 0.8975 | [0.8389, 0.9481] | [0.8240, 0.9617] |  |
| join_marked_0.80_and_own_marked | Name lookup, store-written capped list | 0.6436 | [0.5800, 0.7070] | [0.5655, 0.7249] | -0.2539 [-0.3244, -0.1769] [-0.3380, -0.1595] **reliable** |
| join_marked_0.80_and_own_marked | Name lookup, store-written lifted list | 0.7381 | [0.6759, 0.7949] | [0.6454, 0.8191] | -0.1594 [-0.2209, -0.0976] [-0.2478, -0.0748] **reliable** |
| join_marked_0.80_and_own_marked | GPT-4.1 mini, question only | 0.4946 | [0.4894, 0.4991] | [0.4858, 0.5000] |  |
| join_unmarked_0.80 (the 22) | GPT-4.1 mini, ground truth | 0.5210 | [0.4155, 0.6296] | [0.4012, 0.6827] |  |
| join_unmarked_0.80 (the 22) | GPT-4.1 mini, store-written capped | 0.3433 | [0.2808, 0.4126] | [0.2770, 0.4143] | -0.1777 [-0.2928, -0.0474] [-0.3685, -0.0312] **reliable** |
| join_unmarked_0.80 (the 22) | GPT-4.1 mini, store-written lifted | 0.3591 | [0.2769, 0.4553] | [0.2784, 0.4804] | -0.1618 [-0.3063, -0.0101] [-0.3418, +0.0234] |
| join_unmarked_0.80 (the 22) | Haiku 4.5, ground truth | 0.7074 | [0.5868, 0.8194] | [0.5655, 0.8483] |  |
| join_unmarked_0.80 (the 22) | Haiku 4.5, store-written capped | 0.6368 | [0.5600, 0.7083] | [0.5600, 0.7102] | -0.0706 [-0.2042, +0.0746] [-0.2419, +0.1198] |
| join_unmarked_0.80 (the 22) | Haiku 4.5, store-written lifted | 0.5659 | [0.4839, 0.6474] | [0.4706, 0.6769] | -0.1415 [-0.2659, +0.0026] [-0.3101, +0.0403] |
| join_unmarked_0.80 (the 22) | Name lookup, ground-truth list | 0.4272 | [0.2949, 0.5641] | [0.2576, 0.6703] |  |
| join_unmarked_0.80 (the 22) | Name lookup, store-written capped list | 0.4138 | [0.3011, 0.5462] | [0.2393, 0.6210] | -0.0134 [-0.1772, +0.1524] [-0.2640, +0.2366] |
| join_unmarked_0.80 (the 22) | Name lookup, store-written lifted list | 0.4822 | [0.3998, 0.5708] | [0.3520, 0.6385] | +0.0550 [-0.0894, +0.1958] [-0.1677, +0.2567] |
| join_unmarked_0.80 (the 22) | GPT-4.1 mini, question only | 0.4946 | [0.4901, 0.4982] | [0.4858, 0.5000] |  |
| own_active (no store mark on any member) | GPT-4.1 mini, ground truth | 0.7276 | [0.6199, 0.8284] | [0.5679, 0.8648] |  |
| own_active (no store mark on any member) | GPT-4.1 mini, store-written capped | 0.5871 | [0.4797, 0.6891] | [0.4443, 0.7105] | -0.1405 [-0.2452, -0.0509] [-0.2937, +0.0034] |
| own_active (no store mark on any member) | GPT-4.1 mini, store-written lifted | 0.6244 | [0.5021, 0.7363] | [0.4563, 0.7921] | -0.1033 [-0.1888, -0.0246] [-0.2570, +0.0050] |
| own_active (no store mark on any member) | Haiku 4.5, ground truth | 0.7992 | [0.7353, 0.8595] | [0.7334, 0.8545] |  |
| own_active (no store mark on any member) | Haiku 4.5, store-written capped | 0.6919 | [0.6217, 0.7640] | [0.6085, 0.7727] | -0.1073 [-0.1834, -0.0368] [-0.2134, +0.0017] |
| own_active (no store mark on any member) | Haiku 4.5, store-written lifted | 0.6755 | [0.5881, 0.7586] | [0.5602, 0.7697] | -0.1236 [-0.2180, -0.0439] [-0.2711, -0.0083] **reliable** |
| own_active (no store mark on any member) | Name lookup, ground-truth list | 0.6324 | [0.5076, 0.7551] | [0.4499, 0.8009] |  |
| own_active (no store mark on any member) | Name lookup, store-written capped list | 0.6011 | [0.5052, 0.6896] | [0.4636, 0.7439] | -0.0312 [-0.1433, +0.0924] [-0.1608, +0.1132] |
| own_active (no store mark on any member) | Name lookup, store-written lifted list | 0.6175 | [0.5253, 0.7064] | [0.4692, 0.7463] | -0.0149 [-0.1150, +0.0921] [-0.1297, +0.0984] |
| own_active (no store mark on any member) | GPT-4.1 mini, question only | 0.4946 | [0.4901, 0.4982] | [0.4858, 0.5000] |  |
| own_marked | GPT-4.1 mini, ground truth | 0.7366 | [0.6628, 0.8057] | [0.6387, 0.8334] |  |
| own_marked | GPT-4.1 mini, store-written capped | 0.5996 | [0.5302, 0.6655] | [0.5018, 0.6900] | -0.1370 [-0.2009, -0.0776] [-0.2259, -0.0560] **reliable** |
| own_marked | GPT-4.1 mini, store-written lifted | 0.6627 | [0.5996, 0.7316] | [0.5472, 0.7687] | -0.0738 [-0.1372, +0.0029] [-0.1656, +0.0060] |
| own_marked | Haiku 4.5, ground truth | 0.8303 | [0.7708, 0.8823] | [0.7401, 0.9088] |  |
| own_marked | Haiku 4.5, store-written capped | 0.7133 | [0.6633, 0.7626] | [0.6489, 0.7684] | -0.1170 [-0.1858, -0.0488] [-0.1966, -0.0210] **reliable** |
| own_marked | Haiku 4.5, store-written lifted | 0.7622 | [0.7074, 0.8170] | [0.6704, 0.8407] | -0.0681 [-0.1256, -0.0068] [-0.1422, -0.0000] **reliable** |
| own_marked | Name lookup, ground-truth list | 0.7977 | [0.7223, 0.8636] | [0.6900, 0.8968] |  |
| own_marked | Name lookup, store-written capped list | 0.5793 | [0.5204, 0.6431] | [0.4903, 0.6717] | -0.2184 [-0.2902, -0.1452] [-0.3052, -0.1277] **reliable** |
| own_marked | Name lookup, store-written lifted list | 0.6763 | [0.6164, 0.7305] | [0.5857, 0.7674] | -0.1214 [-0.1893, -0.0558] [-0.2103, -0.0271] **reliable** |
| own_marked | GPT-4.1 mini, question only | 0.4946 | [0.4902, 0.4982] | [0.4858, 0.5000] |  |
| state_exp_join_marked_0.80 | GPT-4.1 mini, ground truth | 0.5633 | [0.4152, 0.7425] | [0.3519, 0.7943] |  |
| state_exp_join_marked_0.80 | GPT-4.1 mini, store-written capped | 0.5340 | [0.3598, 0.6819] | [0.3511, 0.7052] | -0.0293 [-0.2540, +0.1625] [-0.2571, +0.2543] |
| state_exp_join_marked_0.80 | GPT-4.1 mini, store-written lifted | 0.6669 | [0.4726, 0.8548] | [0.3400, 0.9078] | +0.1036 [-0.0348, +0.2503] [-0.0683, +0.2853] |
| state_exp_join_marked_0.80 | Haiku 4.5, ground truth | 0.7002 | [0.5832, 0.8169] | [0.5847, 0.8055] |  |
| state_exp_join_marked_0.80 | Haiku 4.5, store-written capped | 0.6787 | [0.5807, 0.7798] | [0.5546, 0.7963] | -0.0215 [-0.1759, +0.1671] [-0.2263, +0.1850] |
| state_exp_join_marked_0.80 | Haiku 4.5, store-written lifted | 0.6782 | [0.5635, 0.7934] | [0.6217, 0.7363] | -0.0220 [-0.1541, +0.1175] [-0.1454, +0.0878] |
| state_exp_join_marked_0.80 | Name lookup, ground-truth list | 0.4683 | [0.3108, 0.6312] | [0.2533, 0.7264] |  |
| state_exp_join_marked_0.80 | Name lookup, store-written capped list | 0.4862 | [0.3273, 0.6529] | [0.2033, 0.6837] | +0.0179 [-0.0957, +0.1376] [-0.1293, +0.1552] |
| state_exp_join_marked_0.80 | Name lookup, store-written lifted list | 0.4981 | [0.3296, 0.6590] | [0.1788, 0.6898] | +0.0298 [-0.1110, +0.1928] [-0.1721, +0.2776] |
| state_exp_join_marked_0.80 | GPT-4.1 mini, question only | 0.4946 | [0.4901, 0.4982] | [0.4858, 0.5000] |  |
| state_exp_own_marked | GPT-4.1 mini, ground truth | 0.3671 | [0.3482, 0.3849] | [0.3429, 0.3933] |  |
| state_exp_own_marked | GPT-4.1 mini, store-written capped | 0.5804 | [0.3636, 0.7617] | [0.2402, 0.7831] | +0.2133 [+0.0016, +0.3947] [-0.1252, +0.4143] |
| state_exp_own_marked | GPT-4.1 mini, store-written lifted | 0.7041 | [0.3881, 0.8930] | [0.2346, 0.8458] | +0.3370 [+0.0306, +0.5251] [-0.1302, +0.4822] |
| state_exp_own_marked | Haiku 4.5, ground truth | 0.5526 | [0.1989, 0.8588] | [0.4090, 0.9007] |  |
| state_exp_own_marked | Haiku 4.5, store-written capped | 0.7573 | [0.5685, 0.9203] | [0.5375, 0.9118] | +0.2047 [-0.1948, +0.5901] [-0.3627, +0.4155] |
| state_exp_own_marked | Haiku 4.5, store-written lifted | 0.7147 | [0.5021, 0.8765] | [0.4203, 0.8854] | +0.1621 [-0.2441, +0.5649] [-0.4735, +0.4704] |
| state_exp_own_marked | Name lookup, ground-truth list | 0.6510 | [0.4386, 0.7660] | [0.2955, 0.7795] |  |
| state_exp_own_marked | Name lookup, store-written capped list | 0.8352 | [0.7482, 0.9213] | [0.7329, 0.9346] | +0.1842 [+0.0126, +0.4226] [-0.0075, +0.5451] |
| state_exp_own_marked | Name lookup, store-written lifted list | 0.7645 | [0.6565, 0.8695] | [0.6350, 0.8960] | +0.1135 [-0.0804, +0.3562] [-0.1042, +0.4832] |
| state_exp_own_marked | GPT-4.1 mini, question only | 0.4946 | [0.4901, 0.4982] | [0.4860, 0.5000] |  |
| state_ret_join_marked_0.80 | GPT-4.1 mini, ground truth | 0.5831 | [0.3667, 0.8264] | [0.3582, 0.8927] |  |
| state_ret_join_marked_0.80 | GPT-4.1 mini, store-written capped | 0.5477 | [0.3554, 0.7578] | [0.2631, 0.8008] | -0.0355 [-0.1472, +0.1048] [-0.1468, +0.0907] |
| state_ret_join_marked_0.80 | GPT-4.1 mini, store-written lifted | 0.5692 | [0.3980, 0.7254] | [0.2598, 0.7312] | -0.0139 [-0.1844, +0.1603] [-0.2218, +0.2129] |
| state_ret_join_marked_0.80 | Haiku 4.5, ground truth | 0.7588 | [0.6778, 0.8523] | [0.6690, 0.8470] |  |
| state_ret_join_marked_0.80 | Haiku 4.5, store-written capped | 0.7279 | [0.6069, 0.8567] | [0.5676, 0.8767] | -0.0309 [-0.1425, +0.0778] [-0.1601, +0.0594] |
| state_ret_join_marked_0.80 | Haiku 4.5, store-written lifted | 0.4933 | [0.4025, 0.5917] | [0.3990, 0.6092] | -0.2655 [-0.3775, -0.1476] [-0.4013, -0.1350] **reliable** |
| state_ret_join_marked_0.80 | Name lookup, ground-truth list | 0.4026 | [0.1296, 0.6752] | [0.0206, 0.8815] |  |
| state_ret_join_marked_0.80 | Name lookup, store-written capped list | 0.6246 | [0.4735, 0.7472] | [0.3421, 0.7612] | +0.2219 [-0.0881, +0.5401] [-0.2147, +0.6899] |
| state_ret_join_marked_0.80 | Name lookup, store-written lifted list | 0.5263 | [0.3722, 0.6515] | [0.2532, 0.6709] | +0.1237 [-0.1820, +0.4373] [-0.3157, +0.5908] |
| state_ret_join_marked_0.80 | GPT-4.1 mini, question only | 0.4946 | [0.4901, 0.4982] | [0.4859, 0.5000] |  |
| state_ret_own_marked | GPT-4.1 mini, ground truth | 0.5601 | [0.4403, 0.6858] | [0.4331, 0.7408] |  |
| state_ret_own_marked | GPT-4.1 mini, store-written capped | 0.3681 | [0.2887, 0.4524] | [0.2917, 0.4626] | -0.1920 [-0.3379, -0.0496] [-0.3989, -0.0340] **reliable** |
| state_ret_own_marked | GPT-4.1 mini, store-written lifted | 0.3791 | [0.2988, 0.4660] | [0.2972, 0.4860] | -0.1810 [-0.3232, -0.0421] [-0.3790, -0.0119] **reliable** |
| state_ret_own_marked | Haiku 4.5, ground truth | 0.7399 | [0.6289, 0.8408] | [0.5922, 0.8848] |  |
| state_ret_own_marked | Haiku 4.5, store-written capped | 0.6779 | [0.6050, 0.7417] | [0.6103, 0.7413] | -0.0620 [-0.1845, +0.0713] [-0.2280, +0.1157] |
| state_ret_own_marked | Haiku 4.5, store-written lifted | 0.5171 | [0.4464, 0.5971] | [0.4299, 0.6058] | -0.2228 [-0.3363, -0.1011] [-0.3806, -0.0943] **reliable** |
| state_ret_own_marked | Name lookup, ground-truth list | 0.4588 | [0.2980, 0.6340] | [0.2397, 0.7439] |  |
| state_ret_own_marked | Name lookup, store-written capped list | 0.3605 | [0.2526, 0.4697] | [0.2062, 0.5411] | -0.0983 [-0.2709, +0.0980] [-0.3738, +0.1913] |
| state_ret_own_marked | Name lookup, store-written lifted list | 0.4292 | [0.3525, 0.5053] | [0.3165, 0.5401] | -0.0296 [-0.2034, +0.1396] [-0.3110, +0.2291] |
| state_ret_own_marked | GPT-4.1 mini, question only | 0.4946 | [0.4901, 0.4982] | [0.4858, 0.5000] |  |
| state_sup_join_marked_0.80 | GPT-4.1 mini, ground truth | 0.8572 | [0.7882, 0.9201] | [0.7706, 0.9438] |  |
| state_sup_join_marked_0.80 | GPT-4.1 mini, store-written capped | 0.7010 | [0.6307, 0.7652] | [0.6039, 0.7912] | -0.1562 [-0.2226, -0.1009] [-0.2548, -0.0669] **reliable** |
| state_sup_join_marked_0.80 | GPT-4.1 mini, store-written lifted | 0.7610 | [0.6965, 0.8222] | [0.6556, 0.8485] | -0.0962 [-0.1619, -0.0347] [-0.2057, -0.0081] **reliable** |
| state_sup_join_marked_0.80 | Haiku 4.5, ground truth | 0.8897 | [0.8427, 0.9336] | [0.8114, 0.9509] |  |
| state_sup_join_marked_0.80 | Haiku 4.5, store-written capped | 0.7337 | [0.6770, 0.7863] | [0.6616, 0.8031] | -0.1561 [-0.2146, -0.1017] [-0.2320, -0.0793] **reliable** |
| state_sup_join_marked_0.80 | Haiku 4.5, store-written lifted | 0.8369 | [0.7832, 0.8894] | [0.7573, 0.9026] | -0.0528 [-0.1081, -0.0017] [-0.1445, +0.0214] |
| state_sup_join_marked_0.80 | Name lookup, ground-truth list | 0.9534 | [0.9276, 0.9767] | [0.9168, 0.9857] |  |
| state_sup_join_marked_0.80 | Name lookup, store-written capped list | 0.6583 | [0.5928, 0.7201] | [0.5680, 0.7355] | -0.2951 [-0.3494, -0.2427] [-0.3679, -0.2314] **reliable** |
| state_sup_join_marked_0.80 | Name lookup, store-written lifted list | 0.7653 | [0.7120, 0.8167] | [0.6867, 0.8363] | -0.1881 [-0.2394, -0.1397] [-0.2612, -0.1290] **reliable** |
| state_sup_join_marked_0.80 | GPT-4.1 mini, question only | 0.4946 | [0.4901, 0.4982] | [0.4858, 0.5000] |  |
| state_sup_own_marked | GPT-4.1 mini, ground truth | 0.8486 | [0.7737, 0.9162] | [0.7377, 0.9502] |  |
| state_sup_own_marked | GPT-4.1 mini, store-written capped | 0.6980 | [0.6281, 0.7567] | [0.5807, 0.8013] | -0.1506 [-0.2075, -0.0932] [-0.2372, -0.0617] **reliable** |
| state_sup_own_marked | GPT-4.1 mini, store-written lifted | 0.7766 | [0.7038, 0.8415] | [0.6476, 0.8699] | -0.0720 [-0.1397, -0.0049] [-0.1668, +0.0173] |
| state_sup_own_marked | Haiku 4.5, ground truth | 0.8969 | [0.8379, 0.9497] | [0.7958, 0.9746] |  |
| state_sup_own_marked | Haiku 4.5, store-written capped | 0.7235 | [0.6646, 0.7813] | [0.6336, 0.8105] | -0.1735 [-0.2348, -0.1049] [-0.2518, -0.0925] **reliable** |
| state_sup_own_marked | Haiku 4.5, store-written lifted | 0.8693 | [0.8175, 0.9166] | [0.7842, 0.9300] | -0.0276 [-0.0783, +0.0223] [-0.0943, +0.0345] |
| state_sup_own_marked | Name lookup, ground-truth list | 0.9542 | [0.9222, 0.9804] | [0.9139, 0.9920] |  |
| state_sup_own_marked | Name lookup, store-written capped list | 0.6437 | [0.5819, 0.7108] | [0.5578, 0.7309] | -0.3104 [-0.3637, -0.2535] [-0.3841, -0.2426] **reliable** |
| state_sup_own_marked | Name lookup, store-written lifted list | 0.7701 | [0.7124, 0.8275] | [0.6921, 0.8461] | -0.1841 [-0.2350, -0.1329] [-0.2561, -0.1277] **reliable** |
| state_sup_own_marked | GPT-4.1 mini, question only | 0.4946 | [0.4894, 0.4982] | [0.4858, 0.5000] |  |

### AUX-CF2-R125-T3-GRAPHITI — Graphiti's 47 full-store obligations relative to what the graph retains (the census join at three bars)

Recorded buckets at 0.80 reproduced from the edge export: {'EXTRACTION_MISS': 11, 'RECOVERED': 13, 'STALE_ACTIVE': 10, 'retracted': 4, 'unflagged': 9}. Per band, the 34 join-marked superseded-or-expired obligations: 0.50: {'EXTRACTION_MISS': 2, 'RECOVERED': 21, 'STALE_ACTIVE': 11} (retained 32; the 4 join-retracted, content retained 4); 0.75: {'EXTRACTION_MISS': 6, 'RECOVERED': 16, 'STALE_ACTIVE': 12} (retained 28; the 4 join-retracted, content retained 3); 0.80: {'EXTRACTION_MISS': 11, 'RECOVERED': 13, 'STALE_ACTIVE': 10} (retained 23; the 4 join-retracted, content retained 3).

| stratum (positives; the 276 negatives unchanged) | n_pos | by state | store-written capped | lifted | GT on Graphiti's schema | schema lifted | store's superseded-name lookup | whole-map lookup capped | lifted | five edges untagged | native tags | tagged + summary | FR-Bank top-5 untagged | FR-Bank GT summary | question only |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all_47 (manifest-relative, the printed rows) | 47 | {'exp': 9, 'ret': 11, 'sup': 27} | 0.5765 | 0.6511 | 0.7556 | 0.6958 | 0.6780 | 0.6994 | 0.7959 | 0.6995 | 0.6854 | 0.7741 | 0.6991 | 0.7424 | 0.4964 |
| extraction_miss_0.50 | 2 | {'exp': 2} | 0.3569 | 0.4275 | 0.4076 | 0.4764 | 0.5634 | 0.6793 | 0.7935 | 0.4565 | 0.4348 | 0.3841 | 0.7056 | 0.6730 | 0.4964 |
| extraction_miss_0.75 | 6 | {'exp': 3, 'sup': 3} | 0.4601 | 0.6745 | 0.6863 | 0.6482 | 0.7186 | 0.8134 | 0.8382 | 0.5356 | 0.5205 | 0.6682 | 0.7002 | 0.6787 | 0.4964 |
| extraction_miss_0.80 | 11 | {'exp': 3, 'sup': 8} | 0.4559 | 0.7574 | 0.7731 | 0.7120 | 0.6574 | 0.8337 | 0.8610 | 0.6354 | 0.6313 | 0.7413 | 0.7724 | 0.7624 | 0.4964 |
| join_retracted_4 (inexpressible) | 4 | {'ret': 4} | 0.6209 | 0.4275 | 0.6771 | 0.4764 | 0.6984 | 0.8795 | 0.8342 | 0.8619 | 0.9792 | 0.9624 | 0.6920 | 0.5258 | 0.4964 |
| join_unflagged_9 | 9 | {'exp': 2, 'ret': 7} | 0.4090 | 0.4847 | 0.6349 | 0.4764 | 0.5481 | 0.7134 | 0.8233 | 0.8682 | 0.7987 | 0.8416 | 0.8251 | 0.5564 | 0.4964 |
| not_retained_0.80 (extraction miss + retracted + unflagged) | 24 | {'exp': 5, 'ret': 11, 'sup': 8} | 0.4658 | 0.6002 | 0.7052 | 0.5844 | 0.6233 | 0.7962 | 0.8424 | 0.7604 | 0.7520 | 0.8157 | 0.7788 | 0.6457 | 0.4964 |
| recovered_0.50 (non-active mark on a firing edge) | 21 | {'exp': 1, 'sup': 20} | 0.6713 | 0.7601 | 0.8191 | 0.7962 | 0.7755 | 0.6751 | 0.8069 | 0.6523 | 0.6855 | 0.8704 | 0.6980 | 0.8364 | 0.4964 |
| recovered_0.75 (non-active mark on a firing edge) | 16 | {'exp': 1, 'sup': 15} | 0.6897 | 0.7263 | 0.8063 | 0.7999 | 0.7568 | 0.6630 | 0.8227 | 0.6541 | 0.7295 | 0.8443 | 0.6891 | 0.8642 | 0.4964 |
| recovered_0.80 (non-active mark on a firing edge) | 13 | {'exp': 1, 'sup': 12} | 0.7304 | 0.7156 | 0.7632 | 0.7949 | 0.7776 | 0.5923 | 0.7868 | 0.6579 | 0.7131 | 0.8625 | 0.6211 | 0.8350 | 0.4964 |
| retained_0.50 (recovered + stale-active, of the 34) | 32 | {'exp': 5, 'sup': 27} | 0.6318 | 0.7399 | 0.8211 | 0.7986 | 0.7191 | 0.6741 | 0.7836 | 0.6470 | 0.6325 | 0.7560 | 0.6642 | 0.8261 | 0.4964 |
| retained_0.75 (recovered + stale-active, of the 34) | 28 | {'exp': 4, 'sup': 24} | 0.6489 | 0.7316 | 0.8205 | 0.8078 | 0.7081 | 0.6447 | 0.7726 | 0.6573 | 0.6424 | 0.7483 | 0.6594 | 0.8467 | 0.4964 |
| retained_0.80 (recovered + stale-active, of the 34) | 23 | {'exp': 4, 'sup': 19} | 0.6920 | 0.7043 | 0.8081 | 0.8121 | 0.7350 | 0.5983 | 0.7475 | 0.6360 | 0.6159 | 0.7307 | 0.6160 | 0.8433 | 0.4964 |
| stale_active_0.50 | 11 | {'exp': 4, 'sup': 7} | 0.5563 | 0.7013 | 0.8249 | 0.8034 | 0.6113 | 0.6723 | 0.7391 | 0.6370 | 0.5315 | 0.5375 | 0.5996 | 0.8065 | 0.4964 |
| stale_active_0.75 | 12 | {'exp': 3, 'sup': 9} | 0.5947 | 0.7385 | 0.8394 | 0.8184 | 0.6431 | 0.6202 | 0.7059 | 0.6615 | 0.5263 | 0.6202 | 0.6199 | 0.8234 | 0.4964 |
| stale_active_0.80 | 10 | {'exp': 3, 'sup': 7} | 0.6422 | 0.6897 | 0.8665 | 0.8344 | 0.6797 | 0.6062 | 0.6964 | 0.6076 | 0.4897 | 0.5594 | 0.6094 | 0.8540 | 0.4964 |

The same rows with both single-arm intervals and the paired difference against the FR-Bank ground-truth summary on the same items (item; persona):

| stratum | reader | AUROC | item interval | persona interval | minus ground-truth summary |
|---|---|---:|---|---|---|
| all_47 (manifest-relative, the printed rows) | G10-BELIEVED | 0.5765 | [0.4945, 0.6560] | [0.4998, 0.6593] | -0.1659 [-0.2593, -0.0764] [-0.2533, -0.0876] **reliable** |
| all_47 (manifest-relative, the printed rows) | G10-LIFTED | 0.6511 | [0.5779, 0.7286] | [0.5786, 0.7203] | -0.0912 [-0.1869, +0.0098] [-0.1738, -0.0068] |
| all_47 (manifest-relative, the printed rows) | G10-TRUEPROJ | 0.7556 | [0.6724, 0.8341] | [0.6685, 0.8355] | +0.0132 [-0.0560, +0.0804] [-0.0565, +0.0803] |
| all_47 (manifest-relative, the printed rows) | G10-TRUEPROJ-LIFTED | 0.6958 | [0.6231, 0.7720] | [0.6227, 0.7663] | -0.0466 [-0.1068, +0.0128] [-0.1207, +0.0157] |
| all_47 (manifest-relative, the printed rows) | NB6-emb-capped | 0.6780 | [0.5955, 0.7589] | [0.6000, 0.7578] | -0.0644 [-0.1653, +0.0506] [-0.1607, +0.0398] |
| all_47 (manifest-relative, the printed rows) | NB5-emb-capped | 0.6994 | [0.6139, 0.7798] | [0.6314, 0.7719] | -0.0430 [-0.1680, +0.0804] [-0.1618, +0.0792] |
| all_47 (manifest-relative, the printed rows) | NB5-emb-lifted | 0.7959 | [0.7321, 0.8550] | [0.7287, 0.8533] | +0.0536 [-0.0540, +0.1643] [-0.0767, +0.1773] |
| all_47 (manifest-relative, the printed rows) | G10-VIEW-UNTAGGED | 0.6995 | [0.6230, 0.7698] | [0.6226, 0.7786] | -0.0428 [-0.1616, +0.0818] [-0.1757, +0.0896] |
| all_47 (manifest-relative, the printed rows) | G10-VIEW-TAGGED | 0.6854 | [0.6113, 0.7573] | [0.6130, 0.7631] | -0.0569 [-0.1739, +0.0655] [-0.1725, +0.0601] |
| all_47 (manifest-relative, the printed rows) | G10-HYBRID | 0.7741 | [0.6944, 0.8529] | [0.6833, 0.8592] | +0.0318 [-0.0859, +0.1541] [-0.0886, +0.1478] |
| all_47 (manifest-relative, the printed rows) | FRB-VIEW-UNTAGGED | 0.6991 | [0.6166, 0.7747] | [0.6231, 0.7726] | -0.0432 [-0.1634, +0.0680] [-0.1427, +0.0575] |
| all_47 (manifest-relative, the printed rows) | TRUE | 0.7424 | [0.6500, 0.8225] | [0.6517, 0.8353] |  |
| all_47 (manifest-relative, the printed rows) | BLIND | 0.4964 | [0.4907, 0.5000] | [0.4907, 0.5000] |  |
| extraction_miss_0.50 | G10-BELIEVED | 0.3569 | [0.3307, 0.3841] | [0.3281, 0.3818] | -0.3161 [-0.6435, +0.0145] [-0.6378, +0.0157] |
| extraction_miss_0.50 | G10-LIFTED | 0.4275 | [0.4060, 0.4477] | [0.4000, 0.4527] | -0.2455 [-0.5653, +0.0796] [-0.5672, +0.0842] |
| extraction_miss_0.50 | G10-TRUEPROJ | 0.4076 | [0.3845, 0.4311] | [0.3786, 0.4377] | -0.2654 [-0.5866, +0.0634] [-0.5914, +0.0640] |
| extraction_miss_0.50 | G10-TRUEPROJ-LIFTED | 0.4764 | [0.4636, 0.4891] | [0.4647, 0.4874] | -0.1966 [-0.5126, +0.1257] [-0.5125, +0.1236] |
| extraction_miss_0.50 | NB6-emb-capped | 0.5634 | [0.3800, 0.7373] | [0.3796, 0.7500] | -0.1096 [-0.3105, +0.0939] [-0.3287, +0.1213] |
| extraction_miss_0.50 | NB5-emb-capped | 0.6793 | [0.5054, 0.8421] | [0.5150, 0.8368] | +0.0063 [-0.4734, +0.4806] [-0.4610, +0.4737] |
| extraction_miss_0.50 | NB5-emb-lifted | 0.7935 | [0.7357, 0.8416] | [0.7470, 0.8346] | +0.1205 [-0.2373, +0.4711] [-0.2311, +0.4667] |
| extraction_miss_0.50 | G10-VIEW-UNTAGGED | 0.4565 | [0.4402, 0.4716] | [0.4399, 0.4728] | -0.2165 [-0.5343, +0.1084] [-0.5370, +0.1047] |
| extraction_miss_0.50 | G10-VIEW-TAGGED | 0.4348 | [0.4163, 0.4541] | [0.4164, 0.4534] | -0.2382 [-0.5584, +0.0874] [-0.5587, +0.0819] |
| extraction_miss_0.50 | G10-HYBRID | 0.3841 | [0.3594, 0.4074] | [0.3616, 0.4073] | -0.2889 [-0.6137, +0.0379] [-0.6153, +0.0388] |
| extraction_miss_0.50 | FRB-VIEW-UNTAGGED | 0.7056 | [0.4097, 0.9933] | [0.4091, 0.9962] | +0.0326 [-0.0036, +0.0740] [-0.0053, +0.0746] |
| extraction_miss_0.50 | TRUE | 0.6730 | [0.3511, 0.9874] | [0.3507, 0.9891] |  |
| extraction_miss_0.50 | BLIND | 0.4964 | [0.4909, 0.5000] | [0.4907, 0.5000] |  |
| extraction_miss_0.75 | G10-BELIEVED | 0.4601 | [0.3375, 0.6845] | [0.3445, 0.7162] | -0.2186 [-0.5058, -0.0004] [-0.5224, +0.0012] |
| extraction_miss_0.75 | G10-LIFTED | 0.6745 | [0.4267, 0.9217] | [0.4285, 0.9228] | -0.0042 [-0.4321, +0.4102] [-0.4549, +0.4379] |
| extraction_miss_0.75 | G10-TRUEPROJ | 0.6863 | [0.4048, 0.9609] | [0.4185, 0.9504] | +0.0075 [-0.2885, +0.2616] [-0.2806, +0.2715] |
| extraction_miss_0.75 | G10-TRUEPROJ-LIFTED | 0.6482 | [0.4695, 0.8872] | [0.4729, 0.8731] | -0.0305 [-0.2598, +0.1080] [-0.2497, +0.1088] |
| extraction_miss_0.75 | NB6-emb-capped | 0.7186 | [0.5584, 0.8745] | [0.5595, 0.8865] | +0.0399 [-0.2172, +0.2941] [-0.2672, +0.3198] |
| extraction_miss_0.75 | NB5-emb-capped | 0.8134 | [0.6597, 0.9427] | [0.6562, 0.9523] | +0.1347 [-0.2727, +0.5204] [-0.2773, +0.5531] |
| extraction_miss_0.75 | NB5-emb-lifted | 0.8382 | [0.7188, 0.9451] | [0.7190, 0.9514] | +0.1594 [-0.2280, +0.5540] [-0.2333, +0.5742] |
| extraction_miss_0.75 | G10-VIEW-UNTAGGED | 0.5356 | [0.4436, 0.7053] | [0.4418, 0.7003] | -0.1431 [-0.5332, +0.2160] [-0.5358, +0.2482] |
| extraction_miss_0.75 | G10-VIEW-TAGGED | 0.5205 | [0.4175, 0.7081] | [0.4209, 0.7243] | -0.1582 [-0.4301, +0.0650] [-0.4527, +0.0617] |
| extraction_miss_0.75 | G10-HYBRID | 0.6682 | [0.3816, 0.9534] | [0.3891, 0.9293] | -0.0106 [-0.3414, +0.2873] [-0.3193, +0.2977] |
| extraction_miss_0.75 | FRB-VIEW-UNTAGGED | 0.7002 | [0.4259, 0.9768] | [0.4338, 0.9706] | +0.0214 [-0.2876, +0.3189] [-0.3034, +0.3247] |
| extraction_miss_0.75 | TRUE | 0.6787 | [0.3708, 0.9885] | [0.3685, 0.9890] |  |
| extraction_miss_0.75 | BLIND | 0.4964 | [0.4909, 0.5000] | [0.4907, 0.5000] |  |
| extraction_miss_0.80 | G10-BELIEVED | 0.4559 | [0.3448, 0.6105] | [0.3516, 0.6155] | -0.3065 [-0.5058, -0.1204] [-0.4931, -0.1173] **reliable** |
| extraction_miss_0.80 | G10-LIFTED | 0.7574 | [0.6011, 0.9056] | [0.6500, 0.9020] | -0.0049 [-0.2608, +0.2511] [-0.1579, +0.1785] |
| extraction_miss_0.80 | G10-TRUEPROJ | 0.7731 | [0.5969, 0.9383] | [0.6219, 0.9095] | +0.0107 [-0.1239, +0.1423] [-0.1306, +0.1366] |
| extraction_miss_0.80 | G10-TRUEPROJ-LIFTED | 0.7120 | [0.5540, 0.8784] | [0.5886, 0.8262] | -0.0504 [-0.1997, +0.0621] [-0.1951, +0.0679] |
| extraction_miss_0.80 | NB6-emb-capped | 0.6574 | [0.5193, 0.7928] | [0.5025, 0.8115] | -0.1049 [-0.3559, +0.1420] [-0.3344, +0.0971] |
| extraction_miss_0.80 | NB5-emb-capped | 0.8337 | [0.7154, 0.9332] | [0.7225, 0.9451] | +0.0713 [-0.1230, +0.2783] [-0.1129, +0.2967] |
| extraction_miss_0.80 | NB5-emb-lifted | 0.8610 | [0.7512, 0.9484] | [0.7339, 0.9615] | +0.0986 [-0.0986, +0.2978] [-0.0762, +0.3137] |
| extraction_miss_0.80 | G10-VIEW-UNTAGGED | 0.6354 | [0.4939, 0.7689] | [0.5143, 0.7311] | -0.1270 [-0.3913, +0.1235] [-0.2966, +0.0229] |
| extraction_miss_0.80 | G10-VIEW-TAGGED | 0.6313 | [0.4830, 0.8048] | [0.5013, 0.7338] | -0.1311 [-0.3436, +0.0916] [-0.3100, +0.0092] |
| extraction_miss_0.80 | G10-HYBRID | 0.7413 | [0.5774, 0.9045] | [0.5292, 0.9404] | -0.0211 [-0.2599, +0.2264] [-0.3054, +0.1812] |
| extraction_miss_0.80 | FRB-VIEW-UNTAGGED | 0.7724 | [0.6079, 0.9316] | [0.5778, 0.9153] | +0.0100 [-0.2153, +0.2314] [-0.1661, +0.1381] |
| extraction_miss_0.80 | TRUE | 0.7624 | [0.5600, 0.9405] | [0.5911, 0.9185] |  |
| extraction_miss_0.80 | BLIND | 0.4964 | [0.4909, 0.5000] | [0.4907, 0.5000] |  |
| join_retracted_4 (inexpressible) | G10-BELIEVED | 0.6209 | [0.3457, 0.9324] | [0.3494, 0.9247] | +0.0951 [-0.0585, +0.4519] [-0.0537, +0.3827] |
| join_retracted_4 (inexpressible) | G10-LIFTED | 0.4275 | [0.4064, 0.4475] | [0.4000, 0.4537] | -0.0983 [-0.5683, +0.0809] [-0.4567, +0.0941] |
| join_retracted_4 (inexpressible) | G10-TRUEPROJ | 0.6771 | [0.3978, 0.9964] | [0.4029, 0.9732] | +0.1513 [-0.0018, +0.5059] [-0.0010, +0.5246] |
| join_retracted_4 (inexpressible) | G10-TRUEPROJ-LIFTED | 0.4764 | [0.4623, 0.4874] | [0.4647, 0.4873] | -0.0494 [-0.5215, +0.1275] [-0.4072, +0.1332] |
| join_retracted_4 (inexpressible) | NB6-emb-capped | 0.6984 | [0.5031, 0.9138] | [0.4850, 0.9000] | +0.1726 [-0.0753, +0.4458] [-0.0430, +0.4207] |
| join_retracted_4 (inexpressible) | NB5-emb-capped | 0.8795 | [0.7309, 0.9651] | [0.7602, 0.9668] | +0.3537 [-0.0647, +0.5906] [+0.0339, +0.5960] |
| join_retracted_4 (inexpressible) | NB5-emb-lifted | 0.8342 | [0.7809, 0.8819] | [0.7837, 0.8796] | +0.3084 [-0.1556, +0.5131] [-0.0414, +0.5149] |
| join_retracted_4 (inexpressible) | G10-VIEW-UNTAGGED | 0.8619 | [0.4677, 1.0000] | [0.4717, 1.0000] | +0.3361 [-0.0072, +0.6416] [+0.0063, +0.6408] |
| join_retracted_4 (inexpressible) | G10-VIEW-TAGGED | 0.9792 | [0.9479, 1.0000] | [0.9516, 0.9970] | +0.4534 [+0.0000, +0.6269] [+0.1199, +0.6347] |
| join_retracted_4 (inexpressible) | G10-HYBRID | 0.9624 | [0.9144, 0.9946] | [0.9153, 0.9946] | +0.4366 [-0.0054, +0.6250] [+0.1029, +0.6239] |
| join_retracted_4 (inexpressible) | FRB-VIEW-UNTAGGED | 0.6920 | [0.4153, 1.0000] | [0.4146, 0.9914] | +0.1662 [-0.5695, +0.6293] [-0.4286, +0.6143] |
| join_retracted_4 (inexpressible) | TRUE | 0.5258 | [0.3503, 1.0000] | [0.3444, 0.8756] |  |
| join_retracted_4 (inexpressible) | BLIND | 0.4964 | [0.4909, 0.5000] | [0.4907, 0.5000] |  |
| join_unflagged_9 | G10-BELIEVED | 0.4090 | [0.3370, 0.5366] | [0.3364, 0.5341] | -0.1473 [-0.3160, -0.0053] [-0.3112, -0.0222] **reliable** |
| join_unflagged_9 | G10-LIFTED | 0.4847 | [0.4139, 0.6306] | [0.4117, 0.6089] | -0.0717 [-0.3252, +0.2041] [-0.2973, +0.1316] |
| join_unflagged_9 | G10-TRUEPROJ | 0.6349 | [0.4510, 0.8259] | [0.4565, 0.8159] | +0.0785 [-0.0085, +0.2116] [-0.0109, +0.2051] |
| join_unflagged_9 | G10-TRUEPROJ-LIFTED | 0.4764 | [0.4630, 0.4874] | [0.4647, 0.4873] | -0.0799 [-0.2926, +0.1123] [-0.2683, +0.0938] |
| join_unflagged_9 | NB6-emb-capped | 0.5481 | [0.3739, 0.7392] | [0.4008, 0.7394] | -0.0083 [-0.2695, +0.2698] [-0.2692, +0.2589] |
| join_unflagged_9 | NB5-emb-capped | 0.7134 | [0.5351, 0.8759] | [0.5378, 0.8660] | +0.1570 [-0.0247, +0.3600] [-0.0206, +0.3339] |
| join_unflagged_9 | NB5-emb-lifted | 0.8233 | [0.7156, 0.9217] | [0.7166, 0.9225] | +0.2669 [-0.0138, +0.5258] [+0.0023, +0.4977] |
| join_unflagged_9 | G10-VIEW-UNTAGGED | 0.8682 | [0.6950, 0.9961] | [0.7122, 0.9953] | +0.3118 [+0.1372, +0.5222] [+0.1340, +0.4936] **reliable** |
| join_unflagged_9 | G10-VIEW-TAGGED | 0.7987 | [0.5920, 0.9821] | [0.6226, 0.9798] | +0.2424 [+0.0696, +0.4349] [+0.0645, +0.4253] **reliable** |
| join_unflagged_9 | G10-HYBRID | 0.8416 | [0.6467, 0.9876] | [0.6651, 0.9832] | +0.2852 [+0.1035, +0.4930] [+0.1020, +0.4688] **reliable** |
| join_unflagged_9 | FRB-VIEW-UNTAGGED | 0.8251 | [0.6631, 0.9615] | [0.6537, 0.9534] | +0.2687 [+0.0702, +0.4723] [+0.0659, +0.4389] **reliable** |
| join_unflagged_9 | TRUE | 0.5564 | [0.3625, 0.7642] | [0.3858, 0.7435] |  |
| join_unflagged_9 | BLIND | 0.4964 | [0.4910, 0.5000] | [0.4907, 0.5000] |  |
| not_retained_0.80 (extraction miss + retracted + unflagged) | G10-BELIEVED | 0.4658 | [0.3822, 0.5598] | [0.3866, 0.5552] | -0.1799 [-0.3138, -0.0572] [-0.2885, -0.0673] **reliable** |
| not_retained_0.80 (extraction miss + retracted + unflagged) | G10-LIFTED | 0.6002 | [0.4951, 0.6998] | [0.5144, 0.6830] | -0.0455 [-0.2115, +0.1038] [-0.1652, +0.0824] |
| not_retained_0.80 (extraction miss + retracted + unflagged) | G10-TRUEPROJ | 0.7052 | [0.5824, 0.8162] | [0.5887, 0.8159] | +0.0596 [-0.0334, +0.1458] [-0.0298, +0.1476] |
| not_retained_0.80 (extraction miss + retracted + unflagged) | G10-TRUEPROJ-LIFTED | 0.5844 | [0.5002, 0.6796] | [0.5086, 0.6608] | -0.0613 [-0.1642, +0.0355] [-0.1840, +0.0397] |
| not_retained_0.80 (extraction miss + retracted + unflagged) | NB6-emb-capped | 0.6233 | [0.5201, 0.7291] | [0.5134, 0.7362] | -0.0224 [-0.1892, +0.1326] [-0.1576, +0.1107] |
| not_retained_0.80 (extraction miss + retracted + unflagged) | NB5-emb-capped | 0.7962 | [0.6920, 0.8739] | [0.7089, 0.8725] | +0.1505 [+0.0172, +0.2849] [+0.0289, +0.2809] **reliable** |
| not_retained_0.80 (extraction miss + retracted + unflagged) | NB5-emb-lifted | 0.8424 | [0.7723, 0.8981] | [0.7618, 0.9015] | +0.1967 [+0.0502, +0.3378] [+0.0510, +0.3430] **reliable** |
| not_retained_0.80 (extraction miss + retracted + unflagged) | G10-VIEW-UNTAGGED | 0.7604 | [0.6538, 0.8707] | [0.6816, 0.8397] | +0.1147 [-0.0559, +0.2909] [-0.0299, +0.2641] |
| not_retained_0.80 (extraction miss + retracted + unflagged) | G10-VIEW-TAGGED | 0.7520 | [0.6427, 0.8607] | [0.6646, 0.8431] | +0.1064 [-0.0562, +0.2610] [-0.0147, +0.2407] |
| not_retained_0.80 (extraction miss + retracted + unflagged) | G10-HYBRID | 0.8157 | [0.6961, 0.9219] | [0.6964, 0.9209] | +0.1701 [+0.0143, +0.3209] [+0.0111, +0.3095] **reliable** |
| not_retained_0.80 (extraction miss + retracted + unflagged) | FRB-VIEW-UNTAGGED | 0.7788 | [0.6742, 0.8777] | [0.6801, 0.8723] | +0.1331 [-0.0262, +0.2927] [-0.0019, +0.2694] |
| not_retained_0.80 (extraction miss + retracted + unflagged) | TRUE | 0.6457 | [0.5175, 0.7751] | [0.5243, 0.7626] |  |
| not_retained_0.80 (extraction miss + retracted + unflagged) | BLIND | 0.4964 | [0.4910, 0.5000] | [0.4907, 0.5000] |  |
| recovered_0.50 (non-active mark on a firing edge) | G10-BELIEVED | 0.6713 | [0.5373, 0.8142] | [0.5492, 0.7954] | -0.1650 [-0.3147, -0.0233] [-0.2854, -0.0336] **reliable** |
| recovered_0.50 (non-active mark on a firing edge) | G10-LIFTED | 0.7601 | [0.6400, 0.8775] | [0.6334, 0.8661] | -0.0763 [-0.2290, +0.0720] [-0.1804, +0.0066] |
| recovered_0.50 (non-active mark on a firing edge) | G10-TRUEPROJ | 0.8191 | [0.7003, 0.9313] | [0.6941, 0.9221] | -0.0173 [-0.1272, +0.0955] [-0.1415, +0.0921] |
| recovered_0.50 (non-active mark on a firing edge) | G10-TRUEPROJ-LIFTED | 0.7962 | [0.6862, 0.9182] | [0.6790, 0.8954] | -0.0402 [-0.1254, +0.0298] [-0.1367, +0.0300] |
| recovered_0.50 (non-active mark on a firing edge) | NB6-emb-capped | 0.7755 | [0.6709, 0.8698] | [0.6850, 0.8625] | -0.0608 [-0.2086, +0.0851] [-0.1801, +0.0715] |
| recovered_0.50 (non-active mark on a firing edge) | NB5-emb-capped | 0.6751 | [0.5423, 0.7985] | [0.5464, 0.8037] | -0.1612 [-0.3417, +0.0027] [-0.3275, +0.0134] |
| recovered_0.50 (non-active mark on a firing edge) | NB5-emb-lifted | 0.8069 | [0.7124, 0.8934] | [0.7166, 0.8922] | -0.0294 [-0.1763, +0.1337] [-0.1778, +0.1274] |
| recovered_0.50 (non-active mark on a firing edge) | G10-VIEW-UNTAGGED | 0.6523 | [0.5406, 0.7633] | [0.5539, 0.7688] | -0.1841 [-0.3673, -0.0092] [-0.3284, -0.0315] **reliable** |
| recovered_0.50 (non-active mark on a firing edge) | G10-VIEW-TAGGED | 0.6855 | [0.5688, 0.8003] | [0.5771, 0.7936] | -0.1509 [-0.3344, +0.0288] [-0.3081, +0.0222] |
| recovered_0.50 (non-active mark on a firing edge) | G10-HYBRID | 0.8704 | [0.7709, 0.9546] | [0.7723, 0.9439] | +0.0341 [-0.1393, +0.1991] [-0.1211, +0.1854] |
| recovered_0.50 (non-active mark on a firing edge) | FRB-VIEW-UNTAGGED | 0.6980 | [0.5708, 0.8087] | [0.5864, 0.8128] | -0.1384 [-0.3142, +0.0036] [-0.2728, -0.0042] |
| recovered_0.50 (non-active mark on a firing edge) | TRUE | 0.8364 | [0.7125, 0.9485] | [0.7234, 0.9349] |  |
| recovered_0.50 (non-active mark on a firing edge) | BLIND | 0.4964 | [0.4907, 0.5000] | [0.4907, 0.5000] |  |
| recovered_0.75 (non-active mark on a firing edge) | G10-BELIEVED | 0.6897 | [0.5335, 0.8436] | [0.5403, 0.8180] | -0.1746 [-0.3431, +0.0011] [-0.3222, -0.0143] |
| recovered_0.75 (non-active mark on a firing edge) | G10-LIFTED | 0.7263 | [0.5863, 0.8480] | [0.5837, 0.8612] | -0.1379 [-0.2719, -0.0244] [-0.2677, -0.0136] **reliable** |
| recovered_0.75 (non-active mark on a firing edge) | G10-TRUEPROJ | 0.8063 | [0.6613, 0.9273] | [0.6657, 0.9428] | -0.0580 [-0.1935, +0.0715] [-0.1931, +0.0811] |
| recovered_0.75 (non-active mark on a firing edge) | G10-TRUEPROJ-LIFTED | 0.7999 | [0.6675, 0.9243] | [0.6532, 0.9287] | -0.0643 [-0.1717, +0.0245] [-0.1761, +0.0250] |
| recovered_0.75 (non-active mark on a firing edge) | NB6-emb-capped | 0.7568 | [0.6353, 0.8627] | [0.6493, 0.8607] | -0.1075 [-0.2581, +0.0728] [-0.2498, +0.0698] |
| recovered_0.75 (non-active mark on a firing edge) | NB5-emb-capped | 0.6630 | [0.5022, 0.8141] | [0.5222, 0.8036] | -0.2012 [-0.3987, -0.0022] [-0.3782, +0.0087] |
| recovered_0.75 (non-active mark on a firing edge) | NB5-emb-lifted | 0.8227 | [0.7132, 0.9234] | [0.7337, 0.9069] | -0.0416 [-0.2126, +0.1308] [-0.2043, +0.1375] |
| recovered_0.75 (non-active mark on a firing edge) | G10-VIEW-UNTAGGED | 0.6541 | [0.5327, 0.7884] | [0.5336, 0.7835] | -0.2101 [-0.3826, -0.0348] [-0.3694, -0.0294] **reliable** |
| recovered_0.75 (non-active mark on a firing edge) | G10-VIEW-TAGGED | 0.7295 | [0.5994, 0.8649] | [0.6008, 0.8518] | -0.1347 [-0.3191, +0.0717] [-0.3136, +0.0636] |
| recovered_0.75 (non-active mark on a firing edge) | G10-HYBRID | 0.8443 | [0.7200, 0.9544] | [0.7373, 0.9417] | -0.0199 [-0.2119, +0.1734] [-0.1966, +0.1829] |
| recovered_0.75 (non-active mark on a firing edge) | FRB-VIEW-UNTAGGED | 0.6891 | [0.5448, 0.8272] | [0.5643, 0.8154] | -0.1752 [-0.3294, -0.0362] [-0.3136, -0.0465] **reliable** |
| recovered_0.75 (non-active mark on a firing edge) | TRUE | 0.8642 | [0.7283, 0.9803] | [0.7236, 0.9779] |  |
| recovered_0.75 (non-active mark on a firing edge) | BLIND | 0.4964 | [0.4910, 0.5000] | [0.4907, 0.5000] |  |
| recovered_0.80 (non-active mark on a firing edge) | G10-BELIEVED | 0.7304 | [0.5534, 0.8982] | [0.5400, 0.8960] | -0.1047 [-0.2913, +0.0921] [-0.2905, +0.0803] |
| recovered_0.80 (non-active mark on a firing edge) | G10-LIFTED | 0.7156 | [0.5565, 0.8753] | [0.5548, 0.8608] | -0.1194 [-0.2797, +0.0098] [-0.2654, +0.0184] |
| recovered_0.80 (non-active mark on a firing edge) | G10-TRUEPROJ | 0.7632 | [0.5930, 0.9220] | [0.6029, 0.9242] | -0.0718 [-0.2484, +0.0914] [-0.2389, +0.0915] |
| recovered_0.80 (non-active mark on a firing edge) | G10-TRUEPROJ-LIFTED | 0.7949 | [0.6584, 0.9337] | [0.6481, 0.9301] | -0.0401 [-0.1491, +0.0464] [-0.1494, +0.0448] |
| recovered_0.80 (non-active mark on a firing edge) | NB6-emb-capped | 0.7776 | [0.6459, 0.9012] | [0.6468, 0.8972] | -0.0574 [-0.2289, +0.1303] [-0.2154, +0.1303] |
| recovered_0.80 (non-active mark on a firing edge) | NB5-emb-capped | 0.5923 | [0.4097, 0.7491] | [0.4308, 0.7584] | -0.2428 [-0.5056, -0.0071] [-0.4670, +0.0113] |
| recovered_0.80 (non-active mark on a firing edge) | NB5-emb-lifted | 0.7868 | [0.6397, 0.8967] | [0.6583, 0.8961] | -0.0482 [-0.2825, +0.1695] [-0.2672, +0.1726] |
| recovered_0.80 (non-active mark on a firing edge) | G10-VIEW-UNTAGGED | 0.6579 | [0.5189, 0.8097] | [0.5154, 0.8144] | -0.1771 [-0.3930, +0.0414] [-0.3715, +0.0322] |
| recovered_0.80 (non-active mark on a firing edge) | G10-VIEW-TAGGED | 0.7131 | [0.5595, 0.8666] | [0.5567, 0.8479] | -0.1219 [-0.3551, +0.1224] [-0.3489, +0.1072] |
| recovered_0.80 (non-active mark on a firing edge) | G10-HYBRID | 0.8625 | [0.7244, 0.9631] | [0.7277, 0.9629] | +0.0275 [-0.1858, +0.2258] [-0.1772, +0.2464] |
| recovered_0.80 (non-active mark on a firing edge) | FRB-VIEW-UNTAGGED | 0.6211 | [0.4811, 0.7850] | [0.4824, 0.7758] | -0.2139 [-0.3901, -0.0395] [-0.3931, -0.0616] **reliable** |
| recovered_0.80 (non-active mark on a firing edge) | TRUE | 0.8350 | [0.6817, 0.9740] | [0.6711, 0.9731] |  |
| recovered_0.80 (non-active mark on a firing edge) | BLIND | 0.4964 | [0.4909, 0.5000] | [0.4907, 0.5000] |  |
| retained_0.50 (recovered + stale-active, of the 34) | G10-BELIEVED | 0.6318 | [0.5270, 0.7442] | [0.5383, 0.7286] | -0.1943 [-0.3135, -0.0824] [-0.3008, -0.0903] **reliable** |
| retained_0.50 (recovered + stale-active, of the 34) | G10-LIFTED | 0.7399 | [0.6433, 0.8224] | [0.6476, 0.8348] | -0.0862 [-0.1983, +0.0237] [-0.1752, -0.0049] |
| retained_0.50 (recovered + stale-active, of the 34) | G10-TRUEPROJ | 0.8211 | [0.7261, 0.9001] | [0.7331, 0.9030] | -0.0050 [-0.0825, +0.0725] [-0.0873, +0.0681] |
| retained_0.50 (recovered + stale-active, of the 34) | G10-TRUEPROJ-LIFTED | 0.7986 | [0.7111, 0.8826] | [0.7072, 0.8828] | -0.0275 [-0.0922, +0.0258] [-0.0936, +0.0284] |
| retained_0.50 (recovered + stale-active, of the 34) | NB6-emb-capped | 0.7191 | [0.6225, 0.8108] | [0.6312, 0.8052] | -0.1070 [-0.2359, +0.0149] [-0.2006, +0.0007] |
| retained_0.50 (recovered + stale-active, of the 34) | NB5-emb-capped | 0.6741 | [0.5752, 0.7805] | [0.5742, 0.7734] | -0.1519 [-0.2852, -0.0052] [-0.2918, -0.0115] **reliable** |
| retained_0.50 (recovered + stale-active, of the 34) | NB5-emb-lifted | 0.7836 | [0.7014, 0.8566] | [0.6999, 0.8619] | -0.0425 [-0.1579, +0.0853] [-0.1670, +0.0832] |
| retained_0.50 (recovered + stale-active, of the 34) | G10-VIEW-UNTAGGED | 0.6470 | [0.5606, 0.7385] | [0.5656, 0.7316] | -0.1791 [-0.3096, -0.0457] [-0.2901, -0.0500] **reliable** |
| retained_0.50 (recovered + stale-active, of the 34) | G10-VIEW-TAGGED | 0.6325 | [0.5480, 0.7250] | [0.5511, 0.7150] | -0.1936 [-0.3131, -0.0611] [-0.3051, -0.0811] **reliable** |
| retained_0.50 (recovered + stale-active, of the 34) | G10-HYBRID | 0.7560 | [0.6608, 0.8457] | [0.6616, 0.8461] | -0.0701 [-0.2037, +0.0618] [-0.1860, +0.0459] |
| retained_0.50 (recovered + stale-active, of the 34) | FRB-VIEW-UNTAGGED | 0.6642 | [0.5711, 0.7580] | [0.5629, 0.7575] | -0.1619 [-0.2845, -0.0309] [-0.2771, -0.0494] **reliable** |
| retained_0.50 (recovered + stale-active, of the 34) | TRUE | 0.8261 | [0.7317, 0.9122] | [0.7339, 0.9124] |  |
| retained_0.50 (recovered + stale-active, of the 34) | BLIND | 0.4964 | [0.4908, 0.5000] | [0.4907, 0.5000] |  |
| retained_0.75 (recovered + stale-active, of the 34) | G10-BELIEVED | 0.6489 | [0.5401, 0.7677] | [0.5423, 0.7534] | -0.1978 [-0.3166, -0.0728] [-0.3186, -0.0793] **reliable** |
| retained_0.75 (recovered + stale-active, of the 34) | G10-LIFTED | 0.7316 | [0.6305, 0.8312] | [0.6210, 0.8385] | -0.1152 [-0.2282, -0.0078] [-0.2238, -0.0049] **reliable** |
| retained_0.75 (recovered + stale-active, of the 34) | G10-TRUEPROJ | 0.8205 | [0.7153, 0.9145] | [0.7284, 0.9099] | -0.0263 [-0.1111, +0.0470] [-0.1101, +0.0509] |
| retained_0.75 (recovered + stale-active, of the 34) | G10-TRUEPROJ-LIFTED | 0.8078 | [0.7179, 0.8982] | [0.7056, 0.9052] | -0.0389 [-0.1145, +0.0300] [-0.1130, +0.0241] |
| retained_0.75 (recovered + stale-active, of the 34) | NB6-emb-capped | 0.7081 | [0.5892, 0.8263] | [0.6152, 0.8014] | -0.1387 [-0.2795, +0.0126] [-0.2374, -0.0303] |
| retained_0.75 (recovered + stale-active, of the 34) | NB5-emb-capped | 0.6447 | [0.5227, 0.7505] | [0.5367, 0.7486] | -0.2021 [-0.3562, -0.0624] [-0.3351, -0.0728] **reliable** |
| retained_0.75 (recovered + stale-active, of the 34) | NB5-emb-lifted | 0.7726 | [0.6864, 0.8533] | [0.6863, 0.8515] | -0.0741 [-0.1993, +0.0512] [-0.2067, +0.0493] |
| retained_0.75 (recovered + stale-active, of the 34) | G10-VIEW-UNTAGGED | 0.6573 | [0.5621, 0.7481] | [0.5740, 0.7526] | -0.1894 [-0.3281, -0.0501] [-0.3087, -0.0489] **reliable** |
| retained_0.75 (recovered + stale-active, of the 34) | G10-VIEW-TAGGED | 0.6424 | [0.5493, 0.7380] | [0.5498, 0.7385] | -0.2043 [-0.3445, -0.0489] [-0.3259, -0.0785] **reliable** |
| retained_0.75 (recovered + stale-active, of the 34) | G10-HYBRID | 0.7483 | [0.6347, 0.8541] | [0.6539, 0.8433] | -0.0985 [-0.2432, +0.0541] [-0.2198, +0.0292] |
| retained_0.75 (recovered + stale-active, of the 34) | FRB-VIEW-UNTAGGED | 0.6594 | [0.5680, 0.7537] | [0.5560, 0.7525] | -0.1873 [-0.3166, -0.0670] [-0.3178, -0.0802] **reliable** |
| retained_0.75 (recovered + stale-active, of the 34) | TRUE | 0.8467 | [0.7386, 0.9351] | [0.7477, 0.9315] |  |
| retained_0.75 (recovered + stale-active, of the 34) | BLIND | 0.4964 | [0.4909, 0.5000] | [0.4907, 0.5000] |  |
| retained_0.80 (recovered + stale-active, of the 34) | G10-BELIEVED | 0.6920 | [0.5669, 0.8245] | [0.5680, 0.8153] | -0.1512 [-0.2866, -0.0160] [-0.2807, -0.0274] **reliable** |
| retained_0.80 (recovered + stale-active, of the 34) | G10-LIFTED | 0.7043 | [0.5916, 0.8223] | [0.5866, 0.8191] | -0.1389 [-0.2576, -0.0415] [-0.2521, -0.0393] **reliable** |
| retained_0.80 (recovered + stale-active, of the 34) | G10-TRUEPROJ | 0.8081 | [0.6917, 0.9166] | [0.6959, 0.9117] | -0.0351 [-0.1388, +0.0504] [-0.1311, +0.0557] |
| retained_0.80 (recovered + stale-active, of the 34) | G10-TRUEPROJ-LIFTED | 0.8121 | [0.7089, 0.9146] | [0.7008, 0.9181] | -0.0312 [-0.1138, +0.0403] [-0.1034, +0.0318] |
| retained_0.80 (recovered + stale-active, of the 34) | NB6-emb-capped | 0.7350 | [0.6016, 0.8464] | [0.6284, 0.8418] | -0.1082 [-0.2383, +0.0369] [-0.1947, +0.0007] |
| retained_0.80 (recovered + stale-active, of the 34) | NB5-emb-capped | 0.5983 | [0.4665, 0.7276] | [0.4665, 0.7247] | -0.2450 [-0.4167, -0.0699] [-0.4157, -0.0823] **reliable** |
| retained_0.80 (recovered + stale-active, of the 34) | NB5-emb-lifted | 0.7475 | [0.6462, 0.8474] | [0.6381, 0.8386] | -0.0958 [-0.2442, +0.0530] [-0.2613, +0.0530] |
| retained_0.80 (recovered + stale-active, of the 34) | G10-VIEW-UNTAGGED | 0.6360 | [0.5340, 0.7450] | [0.5385, 0.7550] | -0.2072 [-0.3531, -0.0457] [-0.3517, -0.0336] **reliable** |
| retained_0.80 (recovered + stale-active, of the 34) | G10-VIEW-TAGGED | 0.6159 | [0.5105, 0.7290] | [0.5125, 0.7314] | -0.2273 [-0.3704, -0.0532] [-0.3699, -0.0704] **reliable** |
| retained_0.80 (recovered + stale-active, of the 34) | G10-HYBRID | 0.7307 | [0.6109, 0.8442] | [0.6225, 0.8363] | -0.1126 [-0.2673, +0.0471] [-0.2319, +0.0093] |
| retained_0.80 (recovered + stale-active, of the 34) | FRB-VIEW-UNTAGGED | 0.6160 | [0.5127, 0.7217] | [0.5116, 0.7198] | -0.2272 [-0.3651, -0.0957] [-0.3719, -0.0960] **reliable** |
| retained_0.80 (recovered + stale-active, of the 34) | TRUE | 0.8433 | [0.7266, 0.9475] | [0.7287, 0.9413] |  |
| retained_0.80 (recovered + stale-active, of the 34) | BLIND | 0.4964 | [0.4908, 0.5000] | [0.4907, 0.5000] |  |
| stale_active_0.50 | G10-BELIEVED | 0.5563 | [0.3973, 0.7319] | [0.4139, 0.7291] | -0.2502 [-0.4299, -0.0721] [-0.4209, -0.0869] **reliable** |
| stale_active_0.50 | G10-LIFTED | 0.7013 | [0.5431, 0.8623] | [0.5397, 0.8706] | -0.1052 [-0.3146, +0.1025] [-0.3061, +0.0966] |
| stale_active_0.50 | G10-TRUEPROJ | 0.8249 | [0.6654, 0.9778] | [0.6612, 0.9781] | +0.0184 [-0.0164, +0.0532] [-0.0186, +0.0559] |
| stale_active_0.50 | G10-TRUEPROJ-LIFTED | 0.8034 | [0.6504, 0.9461] | [0.6441, 0.9390] | -0.0031 [-0.1415, +0.0747] [-0.1363, +0.0704] |
| stale_active_0.50 | NB6-emb-capped | 0.6113 | [0.3780, 0.8083] | [0.4093, 0.8121] | -0.1952 [-0.4506, +0.0455] [-0.4176, +0.0382] |
| stale_active_0.50 | NB5-emb-capped | 0.6723 | [0.4776, 0.8654] | [0.4812, 0.8424] | -0.1342 [-0.3684, +0.1142] [-0.3655, +0.1082] |
| stale_active_0.50 | NB5-emb-lifted | 0.7391 | [0.5887, 0.8883] | [0.5813, 0.8759] | -0.0674 [-0.2625, +0.1600] [-0.2737, +0.1330] |
| stale_active_0.50 | G10-VIEW-UNTAGGED | 0.6370 | [0.5033, 0.7984] | [0.5023, 0.7852] | -0.1695 [-0.3466, +0.0646] [-0.3754, +0.0385] |
| stale_active_0.50 | G10-VIEW-TAGGED | 0.5315 | [0.4281, 0.6751] | [0.4333, 0.6911] | -0.2750 [-0.4519, -0.0936] [-0.4317, -0.1006] **reliable** |
| stale_active_0.50 | G10-HYBRID | 0.5375 | [0.3903, 0.7112] | [0.3869, 0.7150] | -0.2689 [-0.4490, -0.0816] [-0.4369, -0.1007] **reliable** |
| stale_active_0.50 | FRB-VIEW-UNTAGGED | 0.5996 | [0.4592, 0.7596] | [0.4643, 0.7449] | -0.2069 [-0.4095, -0.0107] [-0.3931, -0.0004] **reliable** |
| stale_active_0.50 | TRUE | 0.8065 | [0.6437, 0.9687] | [0.6340, 0.9707] |  |
| stale_active_0.50 | BLIND | 0.4964 | [0.4909, 0.5000] | [0.4907, 0.5000] |  |
| stale_active_0.75 | G10-BELIEVED | 0.5947 | [0.4380, 0.7737] | [0.4429, 0.7578] | -0.2287 [-0.4025, -0.0664] [-0.4120, -0.0623] **reliable** |
| stale_active_0.75 | G10-LIFTED | 0.7385 | [0.5699, 0.8888] | [0.5695, 0.9005] | -0.0848 [-0.2739, +0.0881] [-0.2899, +0.0916] |
| stale_active_0.75 | G10-TRUEPROJ | 0.8394 | [0.6832, 0.9840] | [0.6997, 0.9780] | +0.0160 [-0.0158, +0.0498] [-0.0162, +0.0500] |
| stale_active_0.75 | G10-TRUEPROJ-LIFTED | 0.8184 | [0.6752, 0.9485] | [0.6827, 0.9420] | -0.0050 [-0.1189, +0.0662] [-0.1235, +0.0664] |
| stale_active_0.75 | NB6-emb-capped | 0.6431 | [0.4344, 0.8251] | [0.4313, 0.8252] | -0.1803 [-0.4173, +0.0334] [-0.4165, +0.0150] |
| stale_active_0.75 | NB5-emb-capped | 0.6202 | [0.4707, 0.7985] | [0.4549, 0.7928] | -0.2032 [-0.3898, +0.0088] [-0.3813, -0.0144] |
| stale_active_0.75 | NB5-emb-lifted | 0.7059 | [0.5690, 0.8356] | [0.5644, 0.8451] | -0.1175 [-0.2769, +0.0329] [-0.2798, +0.0332] |
| stale_active_0.75 | G10-VIEW-UNTAGGED | 0.6615 | [0.5259, 0.8174] | [0.5310, 0.8010] | -0.1618 [-0.3747, +0.0903] [-0.3668, +0.0389] |
| stale_active_0.75 | G10-VIEW-TAGGED | 0.5263 | [0.4273, 0.6563] | [0.4298, 0.6450] | -0.2971 [-0.4954, -0.0712] [-0.4886, -0.1308] **reliable** |
| stale_active_0.75 | G10-HYBRID | 0.6202 | [0.4512, 0.8003] | [0.4438, 0.8035] | -0.2032 [-0.4114, +0.0013] [-0.4240, +0.0107] |
| stale_active_0.75 | FRB-VIEW-UNTAGGED | 0.6199 | [0.4833, 0.7672] | [0.4856, 0.7422] | -0.2035 [-0.4229, +0.0287] [-0.4073, -0.0193] |
| stale_active_0.75 | TRUE | 0.8234 | [0.6600, 0.9744] | [0.6848, 0.9720] |  |
| stale_active_0.75 | BLIND | 0.4964 | [0.4909, 0.5000] | [0.4907, 0.5000] |  |
| stale_active_0.80 | G10-BELIEVED | 0.6422 | [0.4575, 0.8488] | [0.4624, 0.8396] | -0.2118 [-0.3966, -0.0255] [-0.3898, -0.0404] **reliable** |
| stale_active_0.80 | G10-LIFTED | 0.6897 | [0.5135, 0.8745] | [0.5242, 0.8723] | -0.1643 [-0.3462, +0.0071] [-0.3491, +0.0018] |
| stale_active_0.80 | G10-TRUEPROJ | 0.8665 | [0.7061, 0.9940] | [0.7005, 0.9919] | +0.0125 [-0.0231, +0.0556] [-0.0231, +0.0527] |
| stale_active_0.80 | G10-TRUEPROJ-LIFTED | 0.8344 | [0.6757, 0.9876] | [0.6709, 0.9889] | -0.0196 [-0.1581, +0.0634] [-0.1556, +0.0636] |
| stale_active_0.80 | NB6-emb-capped | 0.6797 | [0.4480, 0.8902] | [0.4347, 0.8864] | -0.1743 [-0.4072, +0.0243] [-0.3812, +0.0433] |
| stale_active_0.80 | NB5-emb-capped | 0.6062 | [0.4190, 0.7878] | [0.4014, 0.7927] | -0.2478 [-0.4519, -0.0086] [-0.4677, -0.0108] **reliable** |
| stale_active_0.80 | NB5-emb-lifted | 0.6964 | [0.5445, 0.8524] | [0.5520, 0.8418] | -0.1576 [-0.3292, +0.0272] [-0.3382, +0.0275] |
| stale_active_0.80 | G10-VIEW-UNTAGGED | 0.6076 | [0.4609, 0.7774] | [0.4631, 0.7680] | -0.2464 [-0.4622, +0.0092] [-0.4585, +0.0174] |
| stale_active_0.80 | G10-VIEW-TAGGED | 0.4897 | [0.4194, 0.6298] | [0.4253, 0.6227] | -0.3643 [-0.5341, -0.1816] [-0.5264, -0.1757] **reliable** |
| stale_active_0.80 | G10-HYBRID | 0.5594 | [0.3885, 0.7604] | [0.3925, 0.7555] | -0.2946 [-0.4690, -0.0990] [-0.4729, -0.1107] **reliable** |
| stale_active_0.80 | FRB-VIEW-UNTAGGED | 0.6094 | [0.4636, 0.7640] | [0.4703, 0.7653] | -0.2446 [-0.4588, -0.0168] [-0.4512, +0.0019] |
| stale_active_0.80 | TRUE | 0.8540 | [0.6835, 0.9947] | [0.6848, 0.9958] |  |
| stale_active_0.80 | BLIND | 0.4964 | [0.4909, 0.5000] | [0.4907, 0.5000] |  |

### AUX-CF2-R125-T3-SHEET — the author's read sheet

`reviews\r125\build\AUTHOR_SHEET_R125_T3.xlsx` sha256 `97ba2d2591f91d5d06f1080090c09655ab70e05be6c29c9fcd65a15fd74a9852`; key `reviews\r125\build\AUTHOR_SHEET_R125_T3_key.json` sha256 `9c57c5c7548730a82e362228f240702dcd0711224add71652a080ab0e30174b3`; 42 rows = 22 unmarked + 20 controls (seed 42; pool 79); sheet protection on (password r125); columns J (verdict, data-validated to YES / NO / NOT STORED) and K (notes) unlocked; every other cell locked.

| unmarked obligation | state | nearest stored record (within its store variant) | overlap | a member of the label's records | the store's own mark |
|---|---|---|---:|---|---|
| frbank:bruna:bruna_q06:FULL | ret | lb_00174 | 0.5714 | yes | superseded (not active) |
| frbank:bruna:bruna_q06:CAT-ABLATED | ret | lb_00185 | 0.4286 | yes | superseded (not active) |
| frbank:bruna:bruna_q06:SLOT-ABLATED | ret | lb_00174 | 0.5714 | yes | superseded (not active) |
| frbank:dariush:dariush_q04:FULL | ret | lb_00162 | 0.6667 | yes | active |
| frbank:dariush:dariush_q04:SLOT-ABLATED | ret | lb_00162 | 0.6667 | yes | active |
| frbank:david:david_q06:FULL | exp | lb_00173 | 0.4286 | yes | superseded (not active) |
| frbank:david:david_q06:CAT-ABLATED | exp | lb_00173 | 0.4286 | yes | superseded (not active) |
| frbank:fatima:fatima_q06:FULL | ret | lb_00263 | 0.8000 | no | superseded (not active) |
| frbank:fatima:fatima_q06:SLOT-ABLATED | ret | lb_00188 | 0.6000 | no | active |
| frbank:ingrid:ingrid_q04:FULL | ret | lb_00230 | 0.6000 | no | superseded (not active) |
| frbank:ingrid:ingrid_q04:CAT-ABLATED | ret | lb_00230 | 0.6000 | no | superseded (not active) |
| frbank:ingrid:ingrid_q04:SLOT-ABLATED | ret | lb_00230 | 0.6000 | no | superseded (not active) |
| frbank:joonho:joonho_q04:FULL | ret | lb_00145 | 0.5714 | yes | active |
| frbank:joonho:joonho_q04:SLOT-ABLATED | ret | lb_00145 | 0.5714 | yes | active |
| frbank:marcus:marcus_q10:FULL | exp | lb_00132 | 0.4000 | yes | active |
| frbank:marcus:marcus_q10:CAT-ABLATED | exp | lb_00132 | 0.4000 | yes | active |
| frbank:mirri:mirri_q04:CAT-ABLATED | ret | lb_00160 | 0.5714 | yes | active |
| frbank:rosa:rosa_q06:FULL | ret | lb_00233 | 0.3333 | yes | superseded (not active) |
| frbank:rosa:rosa_q06:CAT-ABLATED | ret | lb_00233 | 0.3333 | yes | superseded (not active) |
| frbank:rosa:rosa_q06:SLOT-ABLATED | ret | lb_00233 | 0.3333 | yes | superseded (not active) |
| frbank:valentina:valentina_q04:FULL | ret | lb_00115 | 0.7500 | yes | superseded (not active) |
| frbank:valentina:valentina_q04:SLOT-ABLATED | ret | lb_00115 | 0.7500 | yes | superseded (not active) |

<!-- R125-T3 END -->

<!-- R125-T4 BEGIN (written by reviews/r125/tools/r125_t45_report.py; do not edit by hand) -->

## 15d. AUX-CF2-R125-SB — the sibling-name control (program R125, Task 4; registered `reviews/r125/registrations/ADDENDUM_R125_SIBLING.md`, frozen 5cd8f80, sha `62078c878a165437…`; `reviews/r125/tools/r125_run.py`, `r125_t45_score.py`; rows `cf2/rows/rows_r125_SB-*.jsonl`; `reviews/r125/results/r125_t4_sibling.json`; scored at 8760b86)

### AUX-CF2-R125-SB-LOCK, -PROBES, -PROJECTION, -LEAK

Registrations `{'ADDENDUM_R125_E2_AMENDMENT_1.md': '41182fa7697dc402914aecea57a8bdf504b832c86f83fab136d96e5f2541462e', 'ADDENDUM_R125_SIBLING.md': '62078c878a1654377a3a36bab0883f6e15914bdb96454eb09961c3c54ee7c350'}` asserted against `reviews\r125\FREEZE_R125.md`; prompts_e1 file `337d37d3414c0482…` / texts `35d9b968ffc0b008…`; SIBLING texts sha256 `f54a7527d37d1a55…` (88 items); caps {'anthropic': 10.0, 'openai': 10.0}; runner sha256 `2be150f2ed0c4357…`; lock written 2026-09-20T12:03:19.

Leak screen on the SIBLING texts: **PASS**, 0 of 30 correct (threshold 3), non-UNKNOWN 6, parse failures 0, served ['gpt-4.1-mini-2025-04-14'], $0.0150.

| lane | served | identifier | probe in / out | probe $ | projected calls | projected $ | ×1.3 | rows | OK | not OK | draws | in / out mean | metered $ |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---:|
| SB-MINI5 | gpt-4.1-mini-2025-04-14 | ok | 1682 / 24 | 0.0007 | 440 | 0.1259 | 0.1637 | 440 | 440 | 0 | [1, 2, 3, 4, 5] | 1614.7 / 23.6 | 0.2292 |
| SB-H45 | claude-haiku-4-5-20251001 | ok | 1791 / 200 | 0.0028 | 440 | 0.5828 | 0.7577 | 440 | 440 | 0 | [1, 2, 3, 4, 5] | 1712.8 / 189.4 | 0.5851 |
| SB-LUNA | gpt-5.6-luna | ok | 1681 / 113 | 0.0006 | 440 | 0.1046 | 0.136 | 440 | 440 | 0 | [1, 2, 3, 4, 5] | 1613.7 / 173.5 | 0.1383 |
| SB-OP5 | claude-opus-5 | ok | 2524 / 414 | 0.0230 | 88 | 0.9668 | 1.2568 | 88 | 88 | 0 | [1] | 2415.2 / 253.4 | 0.8101 |
| SB-SOL | gpt-5.6-sol | ok | 1681 / 210 | 0.0126 | 88 | 1.0507 | 1.3659 | 88 | 88 | 0 | [1] | 1613.7 / 133.7 | 0.9374 |

Projection at the freeze's probes: Anthropic $7.349 (fits the cap: True), OpenAI $8.556 (fits: True); OpenAI without NC-SOL $2.324.

### AUX-CF2-R125-SB-<READER> — the matched AUROC of PN against SIBLING within the pair (88 pairs; dropped 0); PN vs PRESENT on the same pairs; SIBLING vs PRESENT (descriptive)

| reader | PN vs SIBLING W/T/L | **matched** | triple interval | persona interval | pooled PN vs SIBLING | PN vs PRESENT matched (same pairs) | SIBLING vs PRESENT W/T/L | matched | SIBLING minus PRESENT mean score (triple; persona) | minus the name lookup, matched (triple; persona) |
|---|---|---:|---|---|---:|---:|---|---:|---|---|
| Count reader, guessed category | 0/88/0 | **0.5000** | [0.5000, 0.5000] | [0.5000, 0.5000] | 0.5000 | 0.6932 | 34/54/0 | 0.6932 | +0.0149 [+0.0101, +0.0200] [+0.0092, +0.0213] **reliable** | -0.4489 [-0.4830, -0.4034] [-0.4831, -0.4070] **reliable** |
| GPT-4.1 mini (five draws) | 78/3/7 | **0.9034** | [0.8409, 0.9602] | [0.8409, 0.9551] | 0.8151 | 0.8920 | 55/12/21 | 0.6932 | +0.0759 [+0.0469, +0.1043] [+0.0410, +0.1073] **reliable** | -0.0455 [-0.1136, +0.0170] [-0.1112, +0.0115] |
| GPT-5.6 Luna (five draws) | 80/1/7 | **0.9148** | [0.8523, 0.9659] | [0.8351, 0.9767] | 0.9225 | 0.9602 | 60/3/25 | 0.6989 | +0.0644 [+0.0295, +0.1057] [+0.0238, +0.1055] **reliable** | -0.0341 [-0.0854, +0.0227] [-0.1075, +0.0294] |
| GPT-5.6 Sol (draw 1) | 78/5/5 | **0.9148** | [0.8636, 0.9602] | [0.8681, 0.9620] | 0.8917 | 0.9489 | 44/19/25 | 0.6080 | +0.0656 [-0.0024, +0.1331] [-0.0018, +0.1373] | -0.0341 [-0.0966, +0.0286] [-0.0905, +0.0253] |
| Haiku 4.5 (five draws) | 73/9/6 | **0.8807** | [0.8182, 0.9375] | [0.8274, 0.9318] | 0.8434 | 0.9148 | 46/32/10 | 0.7045 | +0.0859 [+0.0556, +0.1167] [+0.0499, +0.1201] **reliable** | -0.0682 [-0.1364, +0.0000] [-0.1266, +0.0000] |
| Name lookup | 82/3/3 | **0.9489** | [0.9034, 0.9830] | [0.9070, 0.9831] | 0.8769 | 0.9659 | 62/9/17 | 0.7557 | +0.0689 [+0.0500, +0.0901] [+0.0438, +0.0988] **reliable** |  |
| Opus 5 (draw 1) | 85/1/2 | **0.9716** | [0.9375, 1.0000] | [0.9387, 1.0000] | 0.9197 | 0.9716 | 43/7/38 | 0.5284 | +0.0376 [-0.0007, +0.0812] [-0.0183, +0.0844] | +0.0227 [-0.0170, +0.0682] [-0.0114, +0.0632] |
| Random-token lookup | 25/33/30 | **0.4716** | [0.3864, 0.5511] | [0.4011, 0.5402] | 0.4735 | 0.7443 | 48/36/4 | 0.7500 | +0.0334 [+0.0242, +0.0437] [+0.0218, +0.0459] **reliable** | -0.4773 [-0.5682, -0.3919] [-0.5476, -0.4107] **reliable** |

Mean scores per version (PN / PRESENT / SIBLING): Count reader, guessed category 0.0294 / 0.0145 / 0.0294; GPT-4.1 mini (five draws) 0.4634 / 0.0876 / 0.1635; GPT-5.6 Luna (five draws) 0.7791 / 0.1421 / 0.2065; GPT-5.6 Sol (draw 1) 0.8903 / 0.2376 / 0.3032; Haiku 4.5 (five draws) 0.5519 / 0.1427 / 0.2287; Name lookup 0.5324 / 0.1246 / 0.1935; Opus 5 (draw 1) 0.7797 / 0.2911 / 0.3287; Random-token lookup 0.0897 / 0.0594 / 0.0927.

### AUX-CF2-R125-SB-P-SB1 — **HELD** (the name lookup's matched PN-vs-SIBLING AUROC at or above 0.90)

The name lookup reads 0.9489 (a recorded value, ADDENDUM_R125_SIBLING §8).

### AUX-CF2-R125-SB-P-SB2 — **HELD** (every model at or above 0.80 with the persona interval excluding 0.50)

GPT-4.1 mini (five draws): 0.9034 (persona lower bound 0.8409; ok); GPT-5.6 Luna (five draws): 0.9148 (persona lower bound 0.8351; ok); GPT-5.6 Sol (draw 1): 0.9148 (persona lower bound 0.8681; ok); Haiku 4.5 (five draws): 0.8807 (persona lower bound 0.8274; ok); Opus 5 (draw 1): 0.9716 (persona lower bound 0.9387; ok).

### AUX-CF2-R125-SB-P-SB3 — **HELD** (the random-token lookup and the count reader within 0.05 of 0.50)

The random-token lookup 0.4716, the count reader 0.5000 (recorded values, §8).

### AUX-CF2-R125-SB-P-SB4 — **HELD** (no model reliably exceeds the name lookup (matched, paired, both intervals above zero))

Reliably above the lookup: none.

### AUX-CF2-R125-SB-SPEND

Task 4 metered: SB-H45 $0.5851; SB-OP5 $0.8101; SB-MINI5 $0.2292; SB-LUNA $0.1383; SB-SOL $0.9374.


<!-- R125-T4 END -->

<!-- R125-T5 BEGIN (written by reviews/r125/tools/r125_t45_report.py; do not edit by hand) -->

## 15e. AUX-CF2-R125-NC — E2 Amendment 1, names-only and counts-only on the three strong models (program R125, Task 5; registered `reviews/r125/registrations/ADDENDUM_R125_E2_AMENDMENT_1.md`, frozen 5cd8f80, sha `41182fa7697dc402…`; rows `cf2/rows/rows_r125_NC-*.jsonl`; `reviews/r125/results/r125_t5_nc.json`; scored at 8760b86)

### AUX-CF2-R125-NC-LOCK, -PROBES, -PROJECTION

Registrations `{'ADDENDUM_R125_E2_AMENDMENT_1.md': '41182fa7697dc402914aecea57a8bdf504b832c86f83fab136d96e5f2541462e', 'ADDENDUM_R125_SIBLING.md': '62078c878a1654377a3a36bab0883f6e15914bdb96454eb09961c3c54ee7c350'}` asserted against `reviews\r125\FREEZE_R125.md`; prompts_e1 file `337d37d3414c0482…` / texts `35d9b968ffc0b008…`; E2's texts sha256 asserted: {'INDEXED-COUNTS': '1187e126d7671768d5848059e8c7eb93c0194f64100209a6054636f45f1eb0e8', 'INDEXED-NAMES': 'd901ebefef3b1e6ba9d9cdc1ab008bb8e08988a413154bd125674e55e2c993db'}; caps {'anthropic': 10.0, 'openai': 10.0}; runner sha256 `2be150f2ed0c4357…`; lock written 2026-09-20T12:03:19.

| lane | served | identifier | probe in / out | probe $ | projected calls | projected $ | ×1.3 | rows | OK | not OK | draws | in / out mean | metered $ |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---:|
| NC-OP5 | claude-opus-5 | ok | 1957 / 229 | 0.0155 | 888 | 5.7991 | 7.5388 | 888 | 888 | 0 | [1] | 1614.6 / 239.2 | 6.2395 |
| NC-LUNA | gpt-5.6-luna | ok | 1232 / 145 | 0.0005 | 4440 | 1.0432 | 1.3561 | 4440 | 4440 | 0 | [1, 2, 3, 4, 5] | 1092.9 / 193.9 | 1.5995 |
| NC-SOL | gpt-5.6-sol | ok | 1232 / 120 | 0.0086 | 888 | 6.2316 | 8.1011 | not run | | | | | |

Projection at the freeze's probes: Anthropic $7.349 (fits the cap: True), OpenAI $8.556 (fits: True); OpenAI without NC-SOL $2.324.

### AUX-CF2-R125-NC-<MODEL>-NAMES, -COUNTS — names-only and counts-only on the 444 (pooled AUROC; persona interval; minus the recorded intact row, minus the name lookup, both intervals; per state)

| model | rendering | pooled | persona interval | sup / ret / exp | minus intact (item; persona) | minus the other intact row | minus the name lookup | matched PN vs PRESENT whole (W/T/L) | matched sup / ret / exp | matched PN vs ABSENT |
|---|---|---:|---|---|---|---|---|---|---|---:|
| GPT-5.6 Luna (draw 1) (intact LUNA_v2_d1 0.8265) | names only | 0.7534 | [0.7013, 0.8011] | 0.9347 / 0.4050 / 0.4653 | -0.0732 [-0.1147, -0.0327] [-0.1108, -0.0367] **reliable** | -0.0884 (LUNA_v2) | -0.0130 [-0.0559, +0.0305] [-0.0428, +0.0159] | 0.7162 (97/18/33) [0.6486, 0.7838] [0.6469, 0.7826] | 0.9318 / 0.3667 / 0.4333 | 0.7601 |
| GPT-5.6 Luna (draw 1) (intact LUNA_v2_d1 0.8265) | counts only | 0.6803 | [0.6292, 0.7332] | 0.7248 / 0.6250 / 0.6106 | -0.1462 [-0.1997, -0.0877] [-0.1884, -0.1009] **reliable** | -0.1614 (LUNA_v2) | -0.0860 [-0.1542, -0.0127] [-0.1321, -0.0359] | 0.7297 (101/14/33) [0.6588, 0.7939] [0.6622, 0.7993] | 0.7727 / 0.5833 / 0.7500 | 0.7399 |
| GPT-5.6 Luna (draw 1) | counts only minus names only | pooled -0.0730 [-0.1440, -0.0010] [-0.1274, -0.0170] **reliable** | | | | | | matched +0.0135 [-0.0811, +0.1047] [-0.0600, +0.0855] | | |
| GPT-5.6 Luna (five draws) (intact LUNA_v2 0.8417) | names only | 0.7819 | [0.7337, 0.8260] | 0.9503 / 0.4772 / 0.5222 | -0.0598 [-0.0967, -0.0270] [-0.0965, -0.0295] **reliable** | -0.0446 (LUNA_v2_d1) | +0.0156 [-0.0215, +0.0538] [-0.0107, +0.0455] | 0.7939 (117/1/30) [0.7195, 0.8649] [0.7273, 0.8581] | 0.9773 / 0.5333 / 0.5167 | 0.7872 |
| GPT-5.6 Luna (five draws) (intact LUNA_v2 0.8417) | counts only | 0.6889 | [0.6448, 0.7362] | 0.7492 / 0.6292 / 0.5742 | -0.1528 [-0.1991, -0.1033] [-0.1844, -0.1211] **reliable** | -0.1376 (LUNA_v2_d1) | -0.0775 [-0.1385, -0.0085] [-0.1157, -0.0322] | 0.8108 (120/0/28) [0.7432, 0.8718] [0.7381, 0.8750] | 0.8977 / 0.7000 / 0.6667 | 0.7432 |
| GPT-5.6 Luna (five draws) | counts only minus names only | pooled -0.0930 [-0.1536, -0.0264] [-0.1424, -0.0422] **reliable** | | | | | | matched +0.0169 [-0.0709, +0.1182] [-0.0772, +0.1013] | | |
| GPT-5.6 Sol (draw 1) | NOT EVALUABLE: lane not run (NC-SOL is dropped when the OpenAI projection for Tasks 4 and 5 exceeds the cap) | | | | | | | | | |
| Opus 5 (draw 1) (intact OP5_v2_d1 0.8400) | names only | 0.7974 | [0.7595, 0.8345] | 0.9356 / 0.4925 / 0.5253 | -0.0426 [-0.0692, -0.0168] [-0.0705, -0.0171] **reliable** | -0.0431 (OP5_v2) | +0.0310 [-0.0108, +0.0747] [+0.0048, +0.0560] | 0.7635 (105/16/27) [0.6993, 0.8244] [0.6993, 0.8244] | 0.9716 / 0.4333 / 0.4833 | 0.8108 |
| Opus 5 (draw 1) (intact OP5_v2_d1 0.8400) | counts only | 0.6486 | [0.5994, 0.7012] | 0.7026 / 0.5081 / 0.6014 | -0.1914 [-0.2347, -0.1453] [-0.2317, -0.1513] **reliable** | -0.1920 (OP5_v2) | -0.1178 [-0.1822, -0.0551] [-0.1704, -0.0579] | 0.7162 (101/10/37) [0.6486, 0.7838] [0.6474, 0.7848] | 0.7784 / 0.4833 / 0.7667 | 0.7162 |
| Opus 5 (draw 1) | counts only minus names only | pooled -0.1488 [-0.2023, -0.0929] [-0.2015, -0.0942] **reliable** | | | | | | matched -0.0473 [-0.1351, +0.0406] [-0.1268, +0.0315] | | |

### AUX-CF2-R125-NC-MATCHED — counts-only per state under the matched metric with both intervals (the P-N5 quantities)

| model | retraction W/T/L | matched | triple | persona | expiry W/T/L | matched | triple | persona |
|---|---|---:|---|---|---|---:|---|---|
| GPT-5.6 Luna (draw 1) | 17/1/12 | 0.5833 | [0.4000, 0.7667] | [0.4285, 0.7308] | 20/5/5 | 0.7500 | [0.6000, 0.8833] | [0.5861, 0.8889] |
| GPT-5.6 Luna (five draws) | 21/0/9 | 0.7000 | [0.5333, 0.8667] | [0.5152, 0.8621] | 20/0/10 | 0.6667 | [0.4667, 0.8333] | [0.4615, 0.8333] |
| Opus 5 (draw 1) | 13/3/14 | 0.4833 | [0.3163, 0.6500] | [0.3166, 0.6607] | 21/4/5 | 0.7667 | [0.6167, 0.8833] | [0.6176, 0.9131] |

### AUX-CF2-R125-NC-P-N3 — **FAILED (on the models run)** (names-only within 0.05 of the intact row at the point, whole set, each of the three)

- GPT-5.6 Luna (five draws): FAILED; Δ -0.0598, intervals [-0.0967, -0.0270] and [-0.0965, -0.0295]
- GPT-5.6 Sol (draw 1): NOT EVALUABLE (the lane did not run: the registered budget rule)
- Opus 5 (draw 1): HELD; Δ -0.0426, intervals [-0.0692, -0.0168] and [-0.0705, -0.0171]

### AUX-CF2-R125-NC-P-N4 — **HELD (on the models run)** (counts-only reliably below names-only, whole set, both intervals excluding zero, each of the three)

- GPT-5.6 Luna (five draws): HELD; Δ -0.0930, intervals [-0.1536, -0.0264] and [-0.1424, -0.0422]
- GPT-5.6 Sol (draw 1): NOT EVALUABLE (the lane did not run: the registered budget rule)
- Opus 5 (draw 1): HELD; Δ -0.1488, intervals [-0.2023, -0.0929] and [-0.2015, -0.0942]

### AUX-CF2-R125-NC-P-N5 — **FAILED (on the models run)** (counts-only above 0.50 on retraction and on expiry under the matched metric with the persona interval excluding 0.50, each of the three)

- GPT-5.6 Luna (five draws): FAILED; retraction 0.7000 (persona lower bound 0.5152), expiry 0.6667 (lower bound 0.4615)
- GPT-5.6 Sol (draw 1): NOT EVALUABLE (the lane did not run: the registered budget rule)
- Opus 5 (draw 1): FAILED; retraction 0.4833 (persona lower bound 0.3166), expiry 0.7667 (lower bound 0.6176)

### AUX-CF2-R125-NC-SPEND

Task 5 metered: NC-OP5 $6.2395; NC-LUNA $1.5995.

**Program spend (token-metered from the rows; not an invoice):** Anthropic $7.6760 of the $10.00 cap (lanes {'SB-H45': 0.5851, 'SB-OP5': 0.8101, 'NC-OP5': 6.2395}, probes $0.0413); OpenAI $2.9423 of the $10.00 cap (lanes {'SB-MINI5': 0.2292, 'SB-LUNA': 0.1383, 'SB-SOL': 0.9374, 'NC-LUNA': 1.5995}, probes $0.0229, leak screen $0.0150).


<!-- R125-T5 END -->
