# PREREG — E3, THE POLICY INSIDE A RUNNING AGENT

# ⚠ DRAFT — **EXPLICITLY NOT FROZEN**

**Nothing in this file is registered.** It is a draft for [AUTHOR-1] to amend and freeze at SP1. No E3
elicitation of any kind has occurred; no store has been written; no snapshot artifact exists; no
threshold has been derived on E3 data. **The bracketed decisions marked `⟨OPEN⟩` are the ones
`OPEN_DECISIONS_E3.md` puts to the operator, and they must be resolved before this file can be
frozen.**

Design of record: `E3_DESIGN.md`. Evidence base: `PROBE_REPORT.md`, `probes/`. Deviation ledger:
`DEVIATIONS_E3.md`, from **D45**. Predecessors: `e1_metamemory/` at `e1-complete`, `e2_metamemory/`
at `c4bd3e1`.

---

## 0. The calendar gate — written now, so no deadline can bend a band later

> **CLAUSE C-1, to be frozen at SP1 with everything else.**
>
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

## 1. Testing procedure — fixed sequence, full α at every step

```
  H-E3a  confabulation vs always-retrieve
     │  HOLDS ────────────► H-E3b  credit non-inferiority
     │                         │  HOLDS ────────────► H-E3c  attribution
     │                         │                         │
     └── not HOLDS ────────────┴─────────────────────────┴──► SEQUENCE BROKEN
```

The three gates are **ordered and gated**, so no multiplicity correction is applied and none is
needed. Each runs at **full α = 0.05** and only if its predecessor **HOLDS**.

**Stopping rule, exactly.** The sequence advances **only on HOLDS**. A **FAILS** or an
**INDETERMINATE** breaks it. Once broken, every downstream result is computed and reported in full
but labelled `EXPLORATORY (sequence broken at <step>)`, carries no inferential claim, and **may not
be described as confirmed, supported or significant** anywhere — main text, appendix or abstract.
Suppression is not the remedy for a broken sequence.

**Rationale, recorded so it is not re-litigated.** The ordering is by survivability, as in E2.
A null H-E3a says the policy does not survive an evolving store, which is E3's whole subject. A null
H-E3c says the payoff is the scaffold rather than the monitor — bad for one sentence of the paper,
survivable for the line. **H-E3c is placed last deliberately, because `E3_DESIGN.md` §4 predicts it
fails**, and a predicted failure must not be allowed to break the sequence above the claims it has
no bearing on.

---

## 2. Hypotheses and bands

| test | band |
|---|---|
| **H-E3a** (primary) | FULL reduces session-level confabulation vs always-retrieve by **≥ 3pp**, covariate-adjusted (persona + label fixed effects), 95% persona-clustered bootstrap CI **excluding zero** |
| **H-E3b** | FULL's credit is non-inferior to always-retrieve at margin **0.03**: one-sided 95% lower bound on the adjusted paired delta **> −0.03** |
| **H-E3c** | ⟨OPEN — see `OPEN_DECISIONS_E3.md` (d)⟩ **Drafted at: FULL's confabulation advantage over SHUFFLED is > 0 with 95% CI excluding zero**, and the fraction of FULL's advantage-over-always that it represents is reported as a number, not as a gate |

**CONSTANT is reported descriptively** wherever it appears and gates nothing.

### 2.1 Power at these bands, computed before the data exists

Derivations in `E3_DESIGN.md` §4. E2's measured SEs on the same contrasts, inflated ×1.33 for E3's
smaller per-rung item count and its cross-rung correlation:

| test | SE used | binding value | power at E2's measured effect |
|---|---|---|---|
| H-E3a | 0.0225 | 4.41pp | **≈ 99.9%** at the measured 11.5pp |
| H-E3b | 0.0181 | margin 0.03 | **99.7%** at the measured +0.0500 — but only **50.5%** against a true null |
| H-E3c | 0.0225 | +0.0370 | **9.3%** at the no-interaction prior |

**These three numbers are registered as stated, including the two that are bad.** H-E3b is a coin
flip if the credit advantage collapses; H-E3c is predicted to fail. Both are recorded here so that
the outcome cannot later be presented as a surprise.

### 2.2 Freeze rule

Bands are frozen at SP1 on E2-derived SEs. At **SP2** the calibration split yields measured
paired-difference SDs and **the implied power is recomputed and reported**. **The bands are not
touched.** Adjusting a band to match observed variance is the failure this rule exists to prevent.
E2's rule, carried verbatim.

### 2.3 The one pre-registered variance lever — k-draw answer trigger

Carried from `PREREG_E2.md` §2.1 with the same arithmetic and the same numeric trigger:

> **If the measured mean per-item σ_a on the E3 calibration split exceeds `0.065`, the eval phase
> runs `k = 3` answer draws per (question, rung, context) and uses the per-item mean credit.
> Otherwise `k = 1`.** Evaluated at SP2, on calibration data only, before any eval-cell contact. The
> measured σ_a and the resulting decision are recorded with the number, whichever way it goes.

---

## 3. The store, the ladder, and the labels

### 3.1 Design and ladder

⟨OPEN (a)⟩ **Drafted at DESIGN A — snapshot ladder.** ⟨OPEN (b)⟩ **Drafted at R = 4 rungs,
s ∈ {14, 20, 24, 32}**, chosen to be equally spaced in *accumulated supersessions* (1% / 36% / 75% /
100% of the eval personas' 165 dated change events) rather than in session index.

**Snapshot definition, frozen:** the store at rung *s* is `{entries : source_session ≤ s}` and
nothing else. `t_now(s)` is session *s*'s own date + 24 h, per persona. **Replay is ordered by
`session_id`, never by date** (D46-E3). Two assertions run at artifact build and fail the boundary:
session ids monotone 1..35 on all 40 personas; **`alive(s₁) ⊂ alive(s₂)` for every s₁ < s₂**.

### 3.2 The label rule at *t*

E1's `PersonaJoin.label` with three changes and no others:

1. **survival by session** — `{i : source_session(i) ≤ s}` replaces the category filter;
2. **the expiry cutoff moves with the rung** — `t_now(s) − 14 d`, rather than a globally pinned
   `t_now`;
3. **event activation** — before a YAML record's resolving session (`new_session`,
   `retraction_session`; `event_date` for expiries), the record creates **no negative obligation**,
   and the entries asserting the **old** value are the gold ones.

**Validity anchor, frozen as a stop condition:** at the terminal rung the rule must reproduce
`PersonaJoin.label(q, ablated = ∅)` on **178/178** authored questions. It does today
(`probes/p2_labels_at_t.py`). **If it does not at build time, the run stops and reports** — a
labeller that disagrees with E1's at the terminal rung is not a generalisation of it.

**PN verification.** E1's hand-adjudicated verdicts are reused unchanged, keyed as they already are.
The recommended ladder needs **6 decisions E1 does not hold** (1 membership, 5 semantic), enumerated
in `PROBE_REPORT.md`; a 5-rung ladder would need 7. They are adjudicated
by hand **before SP1 freezes**, by E1's frozen criterion verbatim, and committed with their
reasoning — never by a model, and never after eval data exists.

### 3.3 Items — key-valid-only

⟨OPEN (b)⟩ **Drafted at KEY-VALID-ONLY.** A question enters the ladder only from the rung at which
its authored `correct_answer` / `wrong_answer_indicators` become valid: at or after its resolving
session for the two-sided sections, at or after `tentative_session` for AV9, and at or after
`event_date` for expiries.

This drops **214 of 1,048 eval cells (20.4%)**, leaving **834**. Every dropped cell is a pre-event
cell in which nothing is stale, and **every PRESENT-NEGATIVE cell is key-valid by construction**, so
the drop costs the primary claim nothing. **No answer key is rebuilt and no key-building instrument
enters the measurement path** (D48-E3).

Item base: the **FULL-variant scoreable set** — 262 eval (141 authored + 121 natural-absent probes),
61 calibration. **No category or slot ablation variants**: E3's store variation is time.

### 3.4 Arms

| arm | rule |
|---|---|
| **(a) FULL** | retrieve iff `FOK ≥ τ_FOK`; append `CAUTION_INSTRUCTION` iff `NOK ≥ τ_NOK`. Gate on the **L1W0D0** prompt over the **BELIEVED** index, index maintained incrementally per write |
| **(b) always-retrieve** | retrieve every turn |
| **(c) no-memory floor** | never retrieve |
| **(d) SHUFFLED** | (a)'s code with FOK and NOK **permuted across items within (persona, rung)**, seed 42; the permutation is drawn once and committed, and retrieval rate is matched to (a)'s realised rate at that rung within ±0.02 |
| **(e) CONSTANT** | ⟨OPEN (c)⟩ (a)'s code with FOK and NOK fixed at 0.50. **Drafted as CUT**, with its reduction to *always-retrieve + always-caution* reported analytically |

**(d) and (e) consume no new gate calls** — both derive from (a)'s elicited scores.
**(a) changes exactly one thing relative to (b)**: whether facts are in the prompt and whether the
caution string is appended. No re-ranking, no re-retrieval, no filtering.

**Retrieval is identical wherever it happens:** top-5 cosine over the persona's own entries
*surviving the rung* (`text-embedding-3-small`), same retriever, same k, same store for every arm at
that rung. **One frozen retrieval-and-store artifact** keyed `(persona, rung, item)`, sha256 recorded
in the SP2 freeze commit; **the eval harness asserts that sha at startup and exits on mismatch.**

**Three context states exist in the whole design and no more:** `S0` no facts, `S1` retrieved facts,
`S2` retrieved facts + `CAUTION_INSTRUCTION`. Answers keyed
`sha256(question_id ‖ rung ‖ context ‖ draw)`, judgments `sha256(question_id ‖ response)`. **`S0` is
rung-invariant** and is elicited once per question for the whole ladder.

**Answerer** `gpt-5.4` at the E2 pin, **judge** `claude-sonnet-4-6` via `claude -p` at temperature 0
under the unmodified `LifeMemEval/evaluate_e2e.py` rubric. **Answer prompt, judge prompt and credit
rule are E2's, byte-identical.** One **20-item judge validity spot-check on session-context
outputs**, on E2's protocol: blinded items, selection using only the pinned judge's own output.

### 3.5 Operating points

⟨OPEN (f)⟩ **Drafted as: the Amendment-4 derivation rule ships frozen and is applied once.** τ_FOK
is set to the lowest grid threshold whose **calibration** precision for non-ABSENT reaches
`p* = L/(G+L)`, with `G` and `L` measured on the E3 calibration split under the pinned answerer.
τ_NOK is set by the same break-even logic on the confabulation axis. **The formula, the grid, the
tie-break and the objective are frozen verbatim from `E2_AMENDMENT_4.md`; only the calibration
inputs are E3's.**

**Why not carry E2's numbers verbatim.** τ_FOK = 0.20 was derived on the **L1W1D1** gate's FOK
distribution. The L1W0D0 prompt changes the gate's scale, and M1 measured W and D on **NOK AUROC
only** — their effect on FOK is unmeasured. Applying a frozen number to a scale it was not derived
on is not "shipping frozen"; applying the frozen **rule** is. **No threshold is fitted on E3 eval
data, ever.**

**If the operator instead rules that the L1W1D1 prompt is kept**, τ_FOK = 0.20 and τ_NOK = 0.00 carry
verbatim with no derivation step at all, and this section reduces to one line. That is
`OPEN_DECISIONS_E3.md` (f).

### 3.6 Calibration split

**Reuse E2's split unchanged:** calibration = `aisha, chenoa, dariush, david, patrick, samuel,
thanh, valentina` (8 personas); eval = the remaining 32. **Disjoint from eval, identical to E2's, so
no persona that trained a threshold ever appears in an E3 eval figure.**

Calibration is used for **exactly two things**: measuring σ_a for the k-draw trigger, and supplying
the `G`/`L`/`B`/`C` inputs to the frozen derivation rule. **No threshold is fitted, no band is
tuned, and no E3 eval item is touched at any point before the SP3 go.**

---

## 4. Descriptives registered

Registered now so none of them can be selected after the fact:

1. **Cost per session including index maintenance**, cached and uncached serving columns, at the
   **D44-corrected** prices (`RESULTS_E2.md` §3.11-R): gpt-5.4 $2.50/$15.00, gpt-4.1-mini
   $0.40/$1.60 per 1M. Maintenance reported as **two numbers** — µs per write and ms per serve —
   because p3 established that `recency`, the age distribution and `expired` are clock-driven and
   cannot be charged per write.
2. **Staleness trajectory.** FULL's advantage over always-retrieve at each rung against that rung's
   measured accumulated-supersession count (**2 / 59 / 123 / 165** on the eval personas).
   **Registered prediction: the advantage is non-decreasing across the four rungs.** Reported as
   observed, in whichever direction it lands. No gate.
3. **Near-miss vs off-topic split at session scale.** E3 has **no ablation-induced absence**, so this
   is natural-absent probes against not-yet-written content.
4. **Absence-mix trajectory** — 59.5% / 59.2% / 57.6% / 46.6% across the ladder, reported because it
   is the design's largest confound.
5. **Index maintenance measured on the eval replay**, extending p3's single-persona figures to all
   32 eval personas.

---

## 5. Stop points

| | when | reports | blocks |
|---|---|---|---|
| **SP1** | at freeze | this file frozen with the ⟨OPEN⟩ decisions resolved; the 7 new PN verdicts committed; tag `e3-sp1` | any elicitation |
| **SP2** | post-calibration, pre-eval | derived operating points, power recomputation, k-trigger decision **with its number**, retrieval-and-store artifact sha, seven-item checklist | any eval-cell call |
| **SP3** | post-eval, pre-scoring | census, failures, deviations, cost — **no metric** | any gate being read |

**SP2 mechanical checklist (conditional go).** 1 — every policy parameter derived on calibration data
only and committed as frozen constants. 2 — power recomputation reported, bands untouched.
3 — k-draw trigger evaluated, decision recorded with the number. 4 — cost projection **< $15**
including every riding arm. 5 — `git status` clean and every file a committed artifact reads from is
tracked. 6 — **zero eval-cell contact to date.** 7 — **snapshot nesting and the terminal-rung label
anchor both assert clean** (`alive(s₁) ⊂ alive(s₂)`; 178/178 against `PersonaJoin.label`). **All
seven pass → proceed through the eval phase to SP3. Any failure, or any non-routine deviation, stops
the run and reports.**

---

## 6. Eval hygiene

> **No eval-cell answer text and no eval-cell score is to be observed before the SP3 go — not by me,
> not by any script's stdout, not in a log tail.**

Enforced, not merely intended: the eval runner prints **counts, statuses, costs and hashes only**; it
holds no scoring code and imports none; answers and judgments are written straight to disk. **No
scoring script may be executed against eval outputs before the SP3 go.** SP3 reports census,
deviations and cost — and nothing else.

**One E3-specific hazard, named:** the staleness trajectory is tempting to look at during the run
because it is a *descriptive*. It is computed from eval outcomes and is therefore **inside the
hygiene fence like everything else.**

---

## 7. Budget

⟨OPEN (e)⟩ **Drafted at cap $40, projection gate $15.** Derivation in `E3_DESIGN.md` §6: base
projection **$2.89** for arms (a)–(d) at k=1; **$7.1** if the k=3 trigger fires; the binding line is
the **metered-fallback reserve** of **$15–20** if the `claude -p` subscription judge lane fails, as
the xAI lane did. Realistic worst case ≈ **$25**; the cap covers that plus one full re-run after a
stop point.

The cap check is **cumulative across processes**, summed over cached responses per arm, not read
from a single process's meter (D27-E1). Projection recomputed at every stop point; above the gate
stops the run.

---

## 8. Deviations, amendments, and the phase-boundary assertion

Numbered continuously from **D45-E3** in `DEVIATIONS_E3.md` with dispositions. Amendments are dated
committed files; **a frozen prereg is never edited**. Cache keyed
`(item_id, rung, arm, model, prompt_hash)`. Seed 42, temperature 0. Persona-clustered bootstrap,
1,000 resamples, items resampled within persona. Persona + label fixed effects, sum-to-zero,
intercept as the estimate — E2's estimator, imported rather than re-implemented.
`tools/assert_clean.py` at **every** phase boundary; **an untracked file that a committed artifact
reads from is a stop condition**, not a warning.

---

## 9. Scope fence

No paper-text edits. No renderer changes — **L is an index factor and L1 is E1's intact index; the
E2 renderer lock is honoured.** No E1 or E2 artifact modifications. No re-ingestion, no relabelling,
no rubric edit, no new probe round, no new store. No FR repo changes. No scoring code executed
against eval outputs before the SP3 go. **Any non-routine deviation stops the run before scoring.**

---

## 10. The FAILS texts, written before the data

House rule: the sentence that gets written if a gate fails is drafted now, when it costs nothing.

**H-E3a FAILS:**
> *"The policy does not survive an evolving store. Its confabulation advantage over always-retrieve,
> established on a static store in E2, does not reproduce when the store is replayed in steps, and
> the paper may not claim a deployment result for it."*

**H-E3b FAILS:**
> *"The policy's cost saving is bought with quality on an evolving store. The abstention it produces
> is not free, and the operating point derived on a static store is the wrong one for a moving one."*

**H-E3c FAILS:**
> *"The payoff is the policy scaffold, not the monitor's information. A monitor whose judgments are
> permuted performs indistinguishably from one whose judgments are informative, so the mechanism the
> paper attributes the result to is not the mechanism producing it. The causal sentence is withdrawn
> and the result is reported as a property of the retrieve-then-caution policy, whatever drives its
> gate."*

**This third text is the one most likely to be needed** — `E3_DESIGN.md` §4 puts its power at 9.3%.
It is written here, in advance, so that the finding can be reported in one sentence rather than
negotiated.
