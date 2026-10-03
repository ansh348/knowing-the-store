# DEVIATIONS — E3

Numbering continues the consolidated ledger in `e1_metamemory/DEVIATIONS.md`, which ends at
**D44-E2**. E3's entries begin at **D45**. The E1/E2 ledger is not edited; this file is the E3
continuation and is referenced from `E3_DESIGN.md`.

Same conventions as E1/E2: every entry states what happened, what was done about it, and its
disposition. A **ledger-class** entry is one whose lesson is wider than the incident.

| # | what | disposition |
|---|---|---|
| **D45** | the published §3.11 prose mis-stated the never-retrieve multiple, independently of D44's pricing bug | **Corrected in `RESULTS_E2.md` §3.11-R.** |
| **D46** | one persona's session dates are not monotone in session id | **Logged as an instrument constraint on any replay.** |
| **D47** | **ledger-class** — a store snapshot cannot be built from an entry filter alone | **Logged; it is the design's central instrument requirement.** |
| **D48** | the authored answer keys describe the end state and are invalid at 39.3% of ladder cells | **Logged and costed; it is the long pole named in `E3_DESIGN.md` §4.** |
| **D49** | E3's application step carries a per-fact lifecycle annotation E2 had no state for | **Adopted and disclosed at SP1.** Without it the ratified arm (a′) is a no-op. |
| **D50** | a descriptive CAUTION-ONLY arm was added beyond the ratified arm list | **Adopted at SP1, gates nothing.** It is what licenses H-E3d's own frozen wording. |
| **D51** | the bank's `is_active` is the store's FINAL state and leaks backwards into a snapshot | **Fixed in the instrument.** Rung-correct state comes from the `supersedes` pointer. |
| **D52** | E1's INTENT GATE is a second label layer and had to be carried | **Carried.** Terminal anchor 178/178, and the 6 predicted new hand verdicts fell to ZERO. |
| **D53** | the terminal anchor is asserted at s=35, not at ladder rung 32 | **Adopted.** Rung 32 is not the store E1 labelled; s=35 is. |
| **D54** | the frozen prereg's PN-mass figure (110) predates the intent gate and hand verdicts | **Registered build gives 99 eval PN cells.** No band depends on it. |
| **D55** | E3 tools importing `e2_api` wrote E3 rows into a committed E2 cache | **Fixed and reverted.** E3 has its own `e3_api`, cache, ledger and $40 cap. |
| **D56** | **STOP** — the S3 annotation is empty by construction, so arm (a′) has nothing to destroy | **Run stopped at the build boundary. `SP2_STOP.md` reports; four options costed.** |
| **D57** | a persona-scoped entry id used as a global key produced a wrong diagnosis | **Caught before it entered a claim.** Re-keyed per persona. |
| **D58** | `(fok or -1)` treats a legitimate FOK of 0.0 as missing | **Fixed in three tools.** Surfaced by the non-vacuity assertion, not by reading code. |
| **D59** | **STOP 2** — H-E3c is vacuous at the derived operating point (τ_FOK = 0.00) | **Caught by checklist item 7 before any eval answer. `SP2_STOP_2.md` reports.** |
| **D60** | the answer plan was simplified when arm (d) was retired | **Routine.** No cell's state set changed. |
| **D61** | the non-vacuity assertion was moved INSIDE the eval runner | **Routine strengthening.** A check that must be remembered is the failure it prevents. |
| **D62** | the forensic phase: forking paths fenced by freezing Q1-Q6 before any slicing ran | **Questions frozen at e610b03; every table traces to a listed Qn.** |
| **D63** | two AD HOC quantities declared, both needed to cost the improvement candidates | **Labelled AD HOC wherever they appear; neither changes a verdict.** |
| **D64** | I1 RETIRED; its $0 impossibility measurement is the registered finding | **Filed as the design law's instance-level corollary: believed state cannot target its own omissions.** |
| **D65** | I2's precondition PASSED and all three frozen predictions were WRONG; the derivation still returns the null policy | **Reported. The reason — a sign reversal across splits — is the finding.** |
| **D66** | the two-direction verifier caught a mean quoted where the artifact stores a median | **Fixed in the canonical record; both statistics now printed and checked.** |
| **D67** | five spec ambiguities in the frozen questions, found by the independent replication | **Tightened by dated amendment; BOTH values reported in every case.** |
| **D68** | two over-claims in the forensic report, both corrected on the independent reading | **Withdrawn/corrected. Neither changes a number; both changed a sentence.** |
| **D69** | the independent report arrived mid-turn and was swept into a commit | **Incident-7 class. Nothing lost; the standing rule refined to named files.** |

---

### D45-E3 — the published §3.11 prose mis-stated the never-retrieve multiple

`RESULTS_E2.md` §3.11 said *"Uncached, (v) is 6× never-retrieve and 6× always-retrieve."* Against
its own published column — (v) 786, (ii) never 59, (i) always 132 — those ratios are **13.4× and
6.0×**. The always-retrieve figure was right; the never-retrieve figure was the always-retrieve
figure repeated.

Found while executing the D44 rider, which required recomputing the ratios from the stored token
counts. Independent of the pricing bug: it was wrong under the old prices too.

**Status:** corrected in `RESULTS_E2.md` §3.11-R, which carries both the published and the corrected
ratios so the change is visible rather than silent. **No verdict, band or hypothesis is affected** —
§3.11 is a descriptive economics section and gates nothing.

**Standing lesson:** *a ratio quoted in prose is a number with no test on it.* Every figure in the
tables of this line is produced by a script and asserted; the ratios in the sentences beside them
were typed. The durable fix is to emit prose-facing ratios from the same script that emits the
table, which `p4_d44_price_fix.py` now does.

---

### D46-E3 — one persona's session dates are not monotone in session id

`callum` session 15 is dated **2025-06-05** and session 16 **2025-06-04**: a one-day inversion. All
other 39 personas are non-decreasing across all 35 sessions (p1: 39/40).

**Why it matters for E3 and for nothing before it.** No E1 or E2 quantity is ordered by session
date; both pin a single `t_now` per persona and never walk the timeline. A replay does walk it, and
a replay ordered by **date** would visit callum's session 16 before session 15 — silently
reordering one persona's writes relative to every other persona's.

**Disposition:** E3 orders replay by **`session_id`**, never by date, and asserts monotonicity of
session id at replay start. `t_now` at rung *s* is taken from session *s*'s own date, so callum's
rung-15 and rung-16 clocks differ by −1 day; the store contents are still correctly nested because
nesting is by id. Recorded so the one-day non-monotonicity is not later mistaken for a bug in the
replay.

---

### D47-E3 — LEDGER-CLASS: a store snapshot cannot be built from an entry filter alone

E1 and E2 represent every store variant as *(base store, removed entry-id set)*, and the label rule
is a survival predicate over entry ids. It is natural to assume a store-state-at-*t* is just another
survival set — `source_session(i) <= s` — and it is **not**.

Measured (p2, 178 authored questions × 5 rungs = 890 cells): filtering entries alone changes the
label on **110 of 890 cells (12.4%)**, and the changes are one-directional in a way that matters:

| entry filter alone says | the correct rule says | cells |
|---|---|---|
| PRESENT-NEGATIVE | PRESENT | **82** |
| UNRESOLVED (between-thresholds) | ABSENT | 28 |

**All 82 of the first kind assert a negative obligation the timeline has not yet produced** — the
error runs in exactly the direction that flatters an obligation-aware policy. At rung *s* = 7 the
entry filter alone reports **29 PRESENT-NEGATIVE** items; the correct count is **1**. The reason is
that the obligation is created by an *event*, and the event's resolving side is dated independently
of which entries survive the filter. Before it, the superseded value is not superseded — it is the
current answer.

**Standing lesson, wider than this study:** *a filter over the store's contents is not a model of
the store's history.* Any time-anchored evaluation over a lifecycle store needs two clocks — one for
what has been written, one for what has been **decided** — and a design that carries only the first
will report obligations that do not exist yet, in the direction that flatters an obligation-aware
policy.

**Disposition:** the event-activation rule is a required component of E3's labeller, specified in
`E3_DESIGN.md` §4 and pre-registered in `PREREG_E3_DRAFT.md` §3. It is derived entirely from fields
already in the persona YAML; it costs no elicitation.

---

### D48-E3 — the authored answer keys are invalid at 39.3% of ladder cells

Every question's `correct_answer` and `wrong_answer_indicators` were authored against the **end
state** of the timeline. At a rung before the event the key describes, the key is not merely
incomplete — for the two-sided sections its `wrong_answer_indicators` **name what is correct there**.
`elena_q02` at rung 7 is the clean case: correct answer "Mediterranean diet", wrong indicator
"keto", and at rung 7 the store contains keto and nothing else, because the switch happens at
session 22.

Measured over 178 authored questions × 5 rungs = 890 cells:

| YAML section | cells whose key describes a state the rung has not reached |
|---|---|
| expiring_logistics | 149 |
| supersession_events | 73 |
| ambiguous (AV9) | 68 |
| contradictions | 38 |
| retractions | 22 |
| **total** | **350 / 890 (39.3%)** |

The old-side fact needed to rebuild the key is present in the YAML for **133/133** of the cells that
sit before a two-sided event, so the rebuild is mechanical and needs no model. It is still new
instrument code with its own verification burden, and it is **the long pole of E3**.

**Disposition:** costed in `E3_DESIGN.md` §4 and driven to zero by Design A's rung placement rule,
which is the reason Design A is recommended. Not a deviation from a frozen plan — E3 has none yet —
but logged here because it is the fact most likely to be forgotten between the design and the build.

---

### D49-E3 — E3's application step carries a per-fact lifecycle annotation, which E2 had no state for

**The instruction and E2's actual machinery do not fit together, and the gap is load-bearing.**

The SP1 ratification defines arm (a) as running the NOK-informed application *"exactly as E2 ran it
(τ_NOK = 0.00, always-on, lifecycle content carried into the application step)"*, and arm (a′) as
byte-identical *"except the lifecycle content passed to the application step is destroyed (labels
scrambled by frozen seed)"*.

**In E2 there is no lifecycle content in the application step to destroy.** E2's `S2` is
`S1` facts plus a *fixed* `CAUTION_INSTRUCTION` string. It carries no per-item lifecycle
information, and at τ_NOK = 0.00 its trigger carries none either, because it fires on every
retrieval. Scrambling anything in E2's `S2` is a no-op, and **arm (a′) as literally specified would
be byte-identical to arm (a)** — the test would compare a policy with itself.

**Resolution adopted, and disclosed rather than absorbed.** E3's `S3` is E2's `S2` plus a per-fact
lifecycle annotation (`[active]` / `[superseded]` / `[expired]`) read from the BELIEVED store state
at that rung, with one added sentence of `CAUTION_INSTRUCTION` explaining the tags. `S3′` is `S3`
with the annotation scrambled by a marginal-preserving frozen permutation. Full specification:
`PREREG_E3.md` §4.3–§4.4.

**What this costs, stated plainly.** Arm (a) is **no longer E2's policy (vi)**. H-E3a therefore
measures a related but not identical contrast to E2's, and the two numbers are not
interchangeable. The prereg says so at the point of use. **What it buys** is that H-E3d becomes a
real test of the thing the ratification asked to test: whether the confabulation payoff needs
lifecycle *information* or only a caution instruction.

**Two smaller decisions inside it, both recorded rather than defaulted:**
* `[retracted]` is **not** in the annotation vocabulary. The store's `is_retracted` flag carries no
  date, so a rung-correct believed retraction cannot be derived from store-own fields, and taking the
  date from the persona YAML would put TRUE provenance inside a BELIEVED arm. It affects **31 of
  18,936 entries (0.16%)**, which fall through to the remaining rules.
* believed-superseded is computed from the **`supersedes` pointer**, not from `is_active`.
  `is_active` records the store's *final* state and would mark an entry superseded at rung 14 for an
  event that happens at session 30. The pointer lives on the newer entry, which carries a
  `source_session`, so it is date-correct. All **5,725** pointers resolve within their own bank.

**Status:** adopted at SP1, before any build, and written into the frozen prereg rather than applied
at run time.

---

### D50-E3 — a descriptive CAUTION-ONLY arm was added beyond the ratified arm list

The ratified arms are (a), (a′), (b), (c), (d). **A sixth, (a″) CAUTION-ONLY — E2's `S2` exactly, on
arm (a)'s retrieved set — was added as a registered descriptive.**

**Why, in one sentence:** H-E3d's frozen HOLDS text says the payoff requires lifecycle content
*"not caution alone"*, and **a scrambled annotation is not the same thing as an absent one.**
Scrambled labels are actively misleading; absent labels are merely uninformative. Without an observed
caution-alone arm, a positive H-E3d would license "content beats *wrong* content" and not the
sentence the ratification froze.

**It gates nothing**, appears in no test, and cannot bias any result. It costs ≈ **$0.82** and turns
the mechanism comparison into a three-point ladder: *no caution → caution only → caution + true
annotation*, with the lobotomy as the fourth point.

**Status:** adopted at SP1 as a descriptive. **Struck by a one-line amendment if the operator does
not want it**; nothing else in the design depends on it.

---

### D51-E3 — the bank's `is_active` is the store's FINAL state and leaks backwards into a snapshot

`LifecycleEntry.is_active` records where the store ended up, not where it was. An entry superseded
at session 30 carries `is_active=False` in the committed bank, so a rung-14 snapshot that reused it
would treat that entry as superseded fourteen sessions before the supersession happened — **future
information changing a past store's behaviour**, in both the index and the retriever.

**Fix, in the instrument rather than in a note:** rung-correct state is derived from the
`supersedes` POINTER, which lives on the *newer* entry and therefore carries a `source_session`:

    superseded_at(e, s)  iff  exists e' with source_session(e') <= s and e'.supersedes == e.id

All **5,725** pointers in the corpus resolve within their own bank. Entries handed to
`lifecycle_search` are rebuilt with `dataclasses.replace`, so the committed bank objects are never
mutated. **Status:** implemented in `e3_common.Snapshot`, used by `build_indexes.py` and
`build_retrieval_e3.py`, and validated by the artifact's v1 check (zero future leak, 0/1,021 cells).

---

### D52-E3 — E1's INTENT GATE is a second label layer, and carrying it removed all six predicted hand verdicts

`E3_DESIGN.md` and `PREREG_E3.md` §3 describe the label rule as `PersonaJoin.label` plus three
changes. That is the **join layer** only. E1 has a **build layer** on top of it —
`build_e1.label` — which does two more things:

* **PAST-EVENT and CHANGE-AWARE questions cannot carry a negative obligation at all**
  (`NEG_ELIGIBLE = {CURRENT-STATE, UPCOMING}`); and
* for **PAST-EVENT**, expired content is folded back into gold (`G = G | exp`) rather than being an
  obligation.

Without that layer the time-anchored labeller manufactures PN labels on structurally barred
intents. **With it, the terminal anchor is 178/178 against E1's committed FULL-variant labels** —
including the hand-verification layer, which is stronger than the anchor the prereg required.

**The consequence worth recording.** `PROBE_REPORT.md` predicted **6 new hand adjudications** for the
recommended ladder. Carrying the intent gate takes that to **zero**: all six are questions whose
committed intent is PAST-EVENT (4) or CHANGE-AWARE (1), both structurally barred, so E1 never needed
a verdict for them and neither does E3. The build asserts coverage (A4) rather than assuming it:
47 semantic and 143 membership decisions needed, all held.

**Standing lesson:** *a label rule spread across two files is one rule.* Reading only the layer that
looks like the labeller reproduced 163/178 and looked close enough to ship.

---

### D53-E3 — the terminal anchor is asserted at s=35, not at ladder rung 32

`PREREG_E3.md` §3 requires the rule to reproduce `PersonaJoin.label(q, ∅)` "at the terminal rung".
The terminal *ladder* rung is 32, and the store at rung 32 is missing sessions 33–35 — it is not the
store E1 labelled. Asserting there would compare the labeller against a different store and would
fail for a correct reason (one item's gold entry is written in session 33+).

**Disposition:** the anchor is asserted at **s = 35**, the full store, which is the state E1's
committed labels describe. It is a build-time assertion over no data cell, so it costs nothing and
changes no registered quantity. Rung 32 remains the terminal *data* rung.

---

### D54-E3 — the frozen prereg's PN-mass figure predates the intent gate and the hand verdicts

`PREREG_E3.md` §2 states the obligation mass as "PN cells 7 / 25 / 37 / 41 = 110". That figure comes
from `PROBE_REPORT.md`, which used the join layer alone. The registered build, with the intent gate
(D52) and E1's hand verdicts applied, gives **5 / 23 / 34 / 37 = 99 eval PN cells** (128 including
calibration).

**No band, margin, sequence or arm depends on it** — it is a descriptive count quoted for context,
and 99 is still above E2's 82. Recorded so the discrepancy between the frozen text and the artifact
is on the record rather than discovered later.

---

### D55-E3 — E3 tools importing `e2_api` wrote E3 rows into a committed E2 cache

`run_gates_e3.py` initially imported `e2_api`, whose cache path is
`e2_metamemory/cache/responses.json` and whose cap is E2's $25. The first calibration gate run
therefore wrote **187 E3 rows into a committed E2 artifact** — a scope-fence violation ("no E2
artifact modifications") — and made E3's spend unseparable from E2's, so **E3's own $40 cap and $15
projection gate could not be read at all**.

**Disposition, same session, before any further call:** `e3_api.py` was written with E3's own cache,
ledger and cap; the 187 rows were **moved** (not re-called, so nothing was re-spent) into
`e3_metamemory/cache/responses.json`; `e2_metamemory/cache/` was restored to its committed state and
verified clean by `git status`. E3's meter now reads **$0.112 over 187 calls**.

**Standing lesson:** *a shared cache is a shared write scope.* Reusing a sibling study's API wrapper
inherits its cache path, its cap and its ledger — three pieces of state a new study must own, and
none of which the import statement mentions.

---

### D56-E3 — STOP: the S3 annotation is empty by construction, so arm (a′) has nothing to destroy

**Full report: `SP2_STOP.md`.** In brief: `PREREG_E3.md` §4.3's annotation vocabulary is
`[active]` / `[superseded]` / `[expired]`, and over **8,280 retrieved fact occurrences the
`[superseded]` count is ZERO**. FR's `lifecycle_search` filters believed-superseded entries at
stage 5a, before every other lifecycle rule — **the retriever filters on exactly the predicate the
annotation reads.** The same holds in E2: 0 of 4,306.

The lobotomy therefore leaves the S3′ prompt **byte-identical to S3 on 64.5% of eval cells**, and
H-E3d would return an uninterpretable null that its own frozen FAILS text would license the paper to
read as "lifecycle content does not matter".

**Status: run stopped at the build boundary**, before the SP2 checklist, before any calibration
answer, before any eval contact, at **$0.97 of $40**. Four options are costed in `SP2_STOP.md`;
**that document proposes and does not amend.** H-E3a, H-E3b and H-E3c are unaffected.

**The corollary that survives whatever is decided:** E2's H-C2 payoff cannot be about
correctly-flagged stale content, because none reaches the answerer. It must act on the entries the
store **wrongly believes active** — the 38.5% the BELIEVED map misses.

---

### D57-E3 — a persona-scoped entry id used as a global key produced a wrong diagnosis

The first E2 cross-check for D56 reported **23.8%** of E2's retrieved facts as believed-superseded,
which contradicted the code path and would have sent the diagnosis somewhere else entirely. The
check had built one `id -> entry` map across all 40 banks, but FR-Bank ids (`lb_00080`) are
**persona-scoped, not globally unique**, so every lookup returned whichever persona was loaded last.
Re-keyed per persona the answer is **0.00%**, matching the code.

Caught by noticing the number contradicted the code path, not by re-reading the script.
**Standing lesson:** *an id that is unique within a shard is not unique across shards, and a dict
keyed on it fails silently and plausibly.* The same id space is shared by 40 banks in this corpus;
any cross-persona map over it must be keyed `(persona, id)`.

---

### D58-E3 — a falsy-zero comparison, surfaced by the non-vacuity assertion itself

Three tools wrote `(row["fok"] or -1) >= tau` to default a missing gate score. The idiom is wrong
whenever the value can be legitimately **zero**: at the derived `tau_FOK = 0.00`, a cell whose FOK is
exactly `0.0` evaluates `0.0 or -1` to **-1**, and is read as NOT retrieving.

**Effect.** The first SP2 checklist run reported arm (a)'s realised calibration rate as **0.995**
instead of **1.000**, which made the (a)/(d) vacuity test return an indeterminate `n/a` rather than a
clean `0.0%`. It never reached a claim; it reached a checklist line that did not parse.

**How it was caught, and this is D57's class exactly.** Not by re-reading the code, and not by a type
error — **by the number contradicting the code path.** A retrieval rate of 0.995 at `tau = 0.00` is
impossible for a score bounded in [0, 1]: every value must clear a threshold of zero. The assertion
printed the threshold and the rate side by side, and the pair could not both be true.

**The class, named:** *a silent, plausible-looking failure detected only because a reported number was
inconsistent with what the code must do.* D57 was the same shape — a persona-scoped id used as a
global key returned 23.8% where the filter at stage 5a made 0% the only possible answer. In both
cases the wrong number was well inside the range a reader would accept; what betrayed it was that the
code could not have produced it. **Reporting a quantity next to the rule that constrains it is
therefore not redundancy — it is the detector**, and it is why both bugs died before reaching a claim.

**Fixed** to `fok if fok is not None else -1` in `sp2_checklist.py`, `run_answers_e3.py` and
`derive_tau_e3.py`; no other site in E3 uses the idiom.

**Standing lesson, and it is the same shape as D57:** *`x or default` is a null check only for values
that cannot legitimately be falsy.* Zero, empty string and empty list are all real values in this
codebase -- FOK of 0.0 is a confident "the store has nothing", not a missing score -- and the idiom
silently converts them into the default. Use an explicit `is None`.

---

### D59-E3 — H-E3c is VACUOUS at the derived operating point, and the assertion caught it

**Full report: `SP2_STOP_2.md`.** The Amendment-4 derivation, applied once on E3's calibration split,
returned **tau_FOK = 0.00** -- the grid minimum -- because the loss from retrieving on an ABSENT cell
is only **0.1042** in E3 against **0.5467** in E2. The cause is structural and pre-registered:
**E3's item base has no ablation-induced absence**, and the ablation-induced cells were the near-miss
ones where retrieval hands the model plausible wrong context (E2 measured 70.1% confabulation on
them against 8.3% on natural probes).

At `tau_FOK = 0.00` arm (a) retrieves on **100%** of cells, and arm (d) SHUFFLED-FOK is defined as
"FOK permuted, retrieval rate matched to (a)". **At a matched rate of 1.000 a permutation cannot move
a decision**, so (d) is byte-identical to (a) on every cell and H-E3c would compare a policy with
itself.

**Caught by checklist item 7 before any eval answer call**, at $2.53 of $40 -- the structural fix
Amendment 1 installed for the (a)/(a') pair, applied as Incident 10's standing lesson requires to
**every pair a gate compares**. It fired on the pair nobody was watching.

**The number is itself the finding, and it is reportable:** on the deployment-realistic absence mix
the FOK gate has **no non-trivial profitable operating point** -- its derived threshold is the grid
minimum and its derived policy is always-retrieve. E2's gate looked valuable in part because 36% of
E2's absence was manufactured by our own ablation, which `E2_DESIGN.md` section 6 pre-registered as
the headline's biggest lever. E3 removes it and the gating claim does not survive the removal.

**H-E3a, H-E3b and H-E3d are unaffected** -- all three compare arms differing in the APPLICATION step,
and both surviving pairs clear the non-vacuity band at 100%. **Recommended disposition: H-E3c
VOID-BY-DERIVATION**, the disposition E2 used for H-C1b, with the cause reported rather than hidden.

**Status: run stopped at the SP2 checklist.** `SP2_STOP_2.md` proposes; it does not amend.

---

### D60-E3 — the answer plan was simplified when arm (d) was retired

`run_answers_e3.py` originally computed a seeded rate-matched hash to decide which cells arm (d)
would retrieve for, and added `S3` if either (a) or (d) fired. E3_AMENDMENT_2 retired (d), and at
tau_FOK = 0.00 (a) fires everywhere, so the hash was dead code that could only ever agree with (a).
It was removed and the comment records why.

**No cell's state set changed as a result**, and arm (d)'s descriptive row is served from (a)'s
answers, which is what byte-identical means. **Status:** routine, recorded for completeness.

---

### D61-E3 — the non-vacuity assertion was moved INSIDE the eval runner

E3_AMENDMENT_1 section 3 requires the (a)/(a') prompt pair to be verified byte-wise on the eval cells
"before any answer call". That could have been a separate script run beforehand. It is instead
embedded in `run_answers_e3.py`, executes unconditionally before the first eval job is built, and
raises `SystemExit` if either surviving gated pair falls below 95%.

**Why the placement is the point.** D56 was not caused by a missing check but by a missing
*obligation* to check. A verification that has to be remembered is the same failure class it exists
to prevent. Realised on the eval cells: **(a)/(b) 834/834, (a')/(a) 834/834, both 100.0%.**

**Status:** routine strengthening, recorded because the placement is load-bearing.

---

### D62-E3 — the forensic phase, and how its forking paths are fenced

`RESULTS_E3.md` is immutable and unchanged. The forensic phase re-slices already-committed raw
outputs at **$0** and re-evaluates no gate. Its exposure is not cost and not contamination — it is
**forking paths**: a decomposition run after the headline is known can find a story in noise, and a
reader has no way to see how many slices were tried.

**Fence, in force before any slicing ran.** `FORENSIC_E3.md` was committed at `e610b03` with Q1-Q6
stated verbatim, plus the method constraints — the same imported estimator, uncertainty on every
effect including the null ones, and a rule that strata below n = 20 report their interval and do not
interpret their point. **Every table in `FORENSIC_E3_REPORT.md` traces to a listed Qn**; the two
quantities that emerged outside them are labelled AD HOC in the report and logged as D63.

**Status:** the questions were frozen, the answers were not. Every output carries an EXPLORATORY
label in the artifact, in the report and in this ledger.

---

### D63-E3 — two AD HOC quantities, declared

Neither is covered by a frozen question. Both were required to cost
`IMPROVEMENT_CANDIDATES.md`, and both are labelled AD HOC wherever they appear.

**AD HOC-1 — I1 join fire rates.** Two candidate instance-level joins were costed against the
committed artifacts. Warning a retrieved fact when its slot name appears in the supersession digest
fires on **55.0%** of retrieved facts and stamps **95.4%** of eval cells, with recall **18/18** on
the Q3 habitat. The tighter join -- warn iff a strictly newer alive entry shares the `slot_key` --
fires on **1.0%** of facts and has recall **0/18** on the habitat.

> **The finding that came out of the costing is worth more than the cost estimate: the believed store
> carries no instance-level signal that identifies the Q3 habitat.** One join is indiscriminate, the
> other is blind to exactly the cells that matter, and the reason is the 61.5% entry-level recall
> `PREREG_E2.md` section 4 already measured -- the habitat IS the set of entries the store failed to
> mark. **I1 is not buildable from believed state alone at any useful precision**, and that was
> established for $0 before anyone registered it.

**AD HOC-2 — E2's published H-C2 decomposed by stratum.** Q1 asks for "E2's H-C2 effect by stratum".
E3's (a)/(b) pair both retrieve on 100% of cells, so the unselected `S2 - S1` is the matching
quantity and is what the re-weighting uses; the published `(vi) - (v)` carries E2's 68% gating
decision and is a different quantity. Both are reported so the choice is visible rather than
assumed. The published contrast reproduces **-5.79pp exactly**, which also validates the
reconstruction of E2's outcome layer from its committed artifacts.

**Status:** declared, labelled, and reported. Neither changes a verdict, and neither is offered as a
test.

---

### D64-E3 — I1 RETIRED; the impossibility measurement is the registered finding

I1 (targeted caution) is **not run and is not to be run as specified**. Two candidate
instance-level joins were costed against committed artifacts at **$0**:

| join | fires on | eval cells stamped | recall on the Q3 habitat |
|---|---|---|---|
| digest-name match | **55.0%** of retrieved facts | **95.4%** | **18/18**, precision useless |
| slot-successor, strictly newer alive entry on the same `slot_key` | **1.0%** | 6.7% | **0/18** |

**One join reaches the habitat only by being indiscriminate; the other is discriminative and cannot
see it at all.** There is no third setting of the dial, because the discriminating signal is the one
the store does not have: **the habitat IS the set of entries the store failed to mark**, which is
`PREREG_E2.md` section 4's **61.5% entry-level recall** seen from the other side.

**Filed as the design law's instance-level corollary.** D47-E3 established *a filter over the store's
contents is not a model of the store's history.* Its instance-level form, registered here:

> **BELIEVED STATE CANNOT TARGET ITS OWN OMISSIONS.** A store's metadata can report what it knows it
> holds in superseded form, and that report is useful in aggregate. It cannot point at the individual
> facts it **wrongly believes are current**, because those are exactly the entries its own lifecycle
> bookkeeping missed. Any instance-level warning derived from believed state has recall on the marked
> entries -- which the retriever has already filtered out -- and no recall on the unmarked ones,
> which are the only ones that reach the answerer.

**Consequence:** an instance-level staleness warning needs a **second opinion** on supersession, not
a re-projection of the first. That is an E4 construction question, not a prompt-engineering one.

**Status:** the I1 mini-prereg in `IMPROVEMENT_CANDIDATES.md` is retired with this reason and
preserved as written beneath its disposition. **Nothing was spent, and the negative is stronger than
the experiment would have been.**

---

### D65-E3 — I2's precondition PASSED, all three frozen predictions were WRONG, and the derivation still returns the null policy

`PREREG_I2.md` was committed at `09c34ab` before the precondition ran. Every prediction in it is
wrong, and the reason is worth more than any of them would have been.

| frozen prediction | observed | verdict |
|---|---|---|
| 1. the precondition FAILS (NOK PN-vs-rest AUROC ≤ 0.65) | **AUROC 0.7775** on 834 cells, PN prevalence 11.9% | **WRONG** |
| 2. the derived `t` lands at or below 0.05 | **no `t` exists** | **FALSIFIED** |
| 3. any synthesized policy lands within 0.5pp of (a″) | the derived policy **is (b)**, 2.04pp away | **FALSIFIED** |

**The monitor can select.** NOK discriminates PRESENT-NEGATIVE at 0.7775 AUROC, comfortably above a
bar set before the value was known. **What it would select for does not replicate.** The break-even
needs a measured benefit, and the caution step's credit gain on PN cells is

* **eval, 32 personas, n = 99: +0.0909, CI [+0.0392, +0.1584]**
* **calibration, 8 personas, n = 29: −0.0345, CI [−0.0707, −0.0048]**

**Both intervals exclude zero, in opposite directions, for the same contrast under the same states on
disjoint persona sets.** Calibration PN precision peaks at **0.2660** against `q*` = **0.3796**, so no
grid threshold clears, and `E2_AMENDMENT_4`'s rule applies verbatim: **no profitable operating point,
recorded at rate 0, an outcome about the policy rather than a fitting failure.** The derived
selective policy is *never apply caution*, which is arm (b).

**Consequence for the record:** `PREREG_I2.md` §4's frozen answer to *"why not selective caution"* is
**superseded by the data** and is listed in `NUMBERS.md` §19. The replacement is sharper and less
comfortable: *the monitor can select; what it selects for is not stable enough to derive a threshold
from.*

**Consequence for a placement already made:** `FORENSIC_E3_REPORT.md`'s Q4 recommendation was
**revised from unqualified MAIN TEXT to "main text only if the calibration counterpart travels in the
same sentence, else appendix."** Quoting +0.0909 without −0.0345 beside it is the failure this ledger
exists to prevent.

**Status:** reported. Not a gate, not in the sequence, not a rescue of H-E3a. $0.

---

### D66-E3 — the two-direction verifier caught a mean quoted where the artifact stores a median

The first canonical row for E3's index maintenance cited `probes/p3_index_maintenance.json` for
**1.11 µs/write**. The artifact's per-write field is `maintain_us_per_write_median` = **1.00**;
1.11 is the **mean**, `maintain_us_total / writes` = 434.30 / 390.

**Direction 1 of the verifier fired**: *artifact 1.00000761 rounds to 1.0, NUMBERS.md prints 1.11.*
Nothing in `RESULTS_E3.md` was wrong — it uses 1.11 consistently as a mean and derives 19.4 ms for
the corpus from it — but the canonical row attributed a mean to a field holding a median, which is
exactly the drift the two-direction check exists to stop.

**Fixed:** the canonical row now prints **mean 1.11 (median 1.00)** and the verifier checks **both**
statistics against the artifact.

**Standing lesson:** *a citation is a claim about where a number came from, and it can be wrong while
the number is right.* Direction 1 checks the value; only naming the exact field checks the
provenance. Every added row now cites a field, not just a file.

**Status:** fixed and verified. **63/63 E2/E3 figures and mandatory annotations pass both
directions**, with the E1 verifier run first and unchanged.

---

### D67-E3 — five spec ambiguities in the frozen questions, tightened by dated amendment

The independent replication (`FORENSIC_E3_INDEPENDENT.md`) and `FORENSIC_E3_REPORT.md` agree to four
decimal places on **every quantity computed from the same estimand** — 14 of 14 in Q2, 3 of 3 in Q4,
every fire count and raw arm coordinate in Q5, the per-rung confabulation series in Q6, and all four
per-stratum effects in Q1. **Five divergences remain and all five are wording, not arithmetic:**

| frozen phrase | reading A (mine) | reading B (independent) | spread |
|---|---|---|---|
| Q1 *"E2's H-C2 effect"* | unselected `S2 − S1` | `(vi) − (v)`, the published contrast | predicted 0.0309 vs 0.0224 |
| Q1 *"observed (0.91pp)"* | (a″)−(b) primary, (a)−(b) second | (a)−(b), the literal 0.91pp | comparator |
| Q3 *"truly-superseded"* | supersession **+ contradictions** | supersessions only (retractions as a sensitivity) | 18 vs 15 vs 39 cells |
| Q6 mean store size | averaged **per cell** | averaged **per persona** | 2.22x vs 2.19x |
| Q5 frontier scale | raw means | adjusted estimates | same conclusion |

**Remedy, per the pre-committed triage:** `FORENSIC_E3.md` is amended (dated) to state which reading
each question means, **and both values are reported in every case.** Neither is deleted, and no
number in either report was changed to match the other.

**Standing lesson:** *freezing a question does not freeze an estimand.* The forking-paths fence
worked — every table traced to a listed Qn — but a question can be frozen and still admit two
defensible computations. **A frozen question needs its estimand written in the same sentence**, and
the cheapest way to find out that it does not is a second analyst.

---

### D68-E3 — two over-claims in FORENSIC_E3_REPORT.md, both corrected on the independent analyst's reading

**Q1.** I wrote that the predicted and observed intervals mutually containing each other's point
estimate makes E3 *"an out-of-sample confirmation of a mix model fitted to nothing."* The
independent objection is correct: *"its interval includes zero, so no difference is detected;
because no equivalence margin was frozen, agreement is not established."*

> **A failure to detect a difference is not a demonstration of equivalence.** No equivalence margin
> was pre-specified in `FORENSIC_E3.md`, so the confirmation wording is not licensed. **Withdrawn.**

What survives is a **consistency** statement, and it is still the strongest thing the forensic phase
produced: the caution effect is concentrated in exactly the strata E3 lacks -- ablation-induced
absence at **35.3% of E2 and 0.1% of E3** carries -10.16pp (unselected) / -8.56pp (gated), against
approximately zero on natural absence at **22.9% of E2 and 58.0% of E3** -- and predicted and
observed reductions are of the same order with overlapping intervals.

**Q6.** I wrote *"store size carries the tripling"* from a label-mix standardisation. The independent
analysis standardises on a **fixed cohort of the 180 rung-14 questions** and decomposes the total
change **45.1% fixed-cohort aging / 54.9% later-entering question mix**, with **zero contamination at
every rung on that cohort**. **Store size remains the strongest aggregate tracker (Pearson r 0.9730
against contamination's 0.6617) and contamination remains ruled out, but no unique carrier is
identifiable.** Corrected to that wording.

**Neither correction changes a number.** Both change a sentence, and both changed a placement
recommendation. **`RESULTS_E3.md` and every gate are untouched.**

**Standing lesson:** *the arithmetic was right both times and the sentence was wrong both times.* Two
analysts agreeing to four decimals still disagreed about what the agreement licensed. **Verification
of values does not verify claims**, and the second reader is the only instrument that catches the
difference.

---

### D69-E3 — the independent report arrived mid-turn and was swept into a commit

`FORENSIC_E3_INDEPENDENT.md` was **absent** when the convergence step was first reached; the first
version of `CONVERGENCE_E3.md` recorded the diff as *pending* on that basis. The file appeared during
the same working turn and was absorbed into commit `8c57a38` by a `git add` over the study tree,
alongside unrelated closeout work.

**Incident-7 class, exactly:** *in a clone with more than one agent, `git add` followed later by
`git commit` is not atomic and the window is not yours.* The standing remedy -- commit with an
explicit pathspec -- was followed (`git commit -- e3_metamemory/ ...`), but the pathspec was a
**directory**, which is wide enough to absorb another session's new file.

**Nothing was lost or altered.** The file is byte-identical to what the other session wrote, its
frozen-question sha matches on both sides, and the superseded *pending* version of
`CONVERGENCE_E3.md` remains in history rather than being deleted.

**Refinement to the standing rule:** a directory pathspec is not a pathspec for this purpose.
**Where a concurrent session may be writing into the same tree, commit named files.**
