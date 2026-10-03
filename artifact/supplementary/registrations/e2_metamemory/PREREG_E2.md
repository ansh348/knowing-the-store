# PREREG — E2, THE CONTROL LOOP

# ✅ FROZEN AT SP1 — 2026-08-11

**Ratified by [AUTHOR-1] at SP1 with modifications, all encoded below.** Superseded draft: the
`NOT FROZEN` version at commit `1a7cc40`. **Design of record:** `E2_DESIGN.md`. **Predecessor:**
`e1_metamemory/` at tag `e1-complete`; canonical figures `e1_metamemory/NUMBERS.md`.

**Statement of data contact at freeze time.** No E2 elicitation of any kind has occurred. No
threshold has been fitted. No store has been written. The calibration split was *defined*
(`CALIBRATION_SPLIT.json`) from E1's committed item file. **Everything below is frozen in advance
of the numbers it governs.**

---

## 1. Testing procedure — fixed-sequence hierarchical, full α at every step

The three gates are **ordered and gated**, so no multiplicity correction is applied and none is
needed. Each test runs at **full α = 0.05** and only if its predecessor **HOLDS**.

```
  H-C1a  non-inferiority vs always-retrieve
     │  HOLDS ────────────► H-C1b  superiority vs the tuned baselines
     │                         │  HOLDS ────────────► H-C2  confabulation
     │                         │                         │
     └── not HOLDS ────────────┴─────────────────────────┴──► SEQUENCE BROKEN
```

**Stopping rule, exactly.** The sequence advances **only on HOLDS**. A **FAILS** or an
**INDETERMINATE** breaks it. Once broken, **every downstream result is computed and reported but
labelled `EXPLORATORY (sequence broken at <step>)`**, carries no inferential claim, and **may not
be described as confirmed, supported, or significant** anywhere — main text, appendix, or abstract.
Downstream results are still reported in full; suppression is not the remedy for a broken sequence.

**Rationale, recorded so it is not re-litigated:** the two failures are not equally survivable. A
null H-C1b says the construct has no engineering value. A null H-C2 says obligation monitoring does
not transfer downstream — bad, but FR already owns the post-retrieval confabulation result, so the
line survives. Ordering by survivability spends α where it buys the most.

## 2. Bands — frozen, never re-tuned

| test | band |
|---|---|
| **H-C1a** | eval retrieval rate at frozen τ_FOK **≤ 0.80** AND one-sided 95% lower bound on credit delta vs always-retrieve **> −0.03** |
| **H-C1b** | credit delta **≥ +0.03**, 95% CI excluding 0, against **both** (iii) and (iv), at retrieval rates matched within ±0.02 |
| **H-C2** | confabulation reduction **≥ 3pp**, CI excluding 0, AND credit non-inferior at margin 0.03 |

**Power at these bands, computed before the data exists:** H-C1a margin 0.03 → **74.4%** when the
policies are truly equal; H-C1b +0.03 → **63.3%** at a true +0.03; H-C2 3pp → ≈80% only while
discordance b+c ≲ 35, ≈50% by b+c ≈ 60. Derivations in `E2_DESIGN.md` §2.

**Freeze rule.** At **SP2** the calibration split yields a measured paired-difference SD; the
implied power is **recomputed and reported** as information for the stop/go call. **The bands are
not touched.** Adjusting a band to match observed variance is the failure this rule exists to
prevent.

### 2.1 The one pre-registered variance lever — k-draw answer trigger

The bands above assume answer generation contributes negligible noise. That assumption is tested at
SP2 on calibration data only, and the response is **frozen now, numerically**.

**Derivation.** Let σ_a be the per-item SD of behaviour-typed credit across independent answer
draws. Two policies drawing independently inflate the paired-difference variance by 2σ_a²:

```
SD_total² = SD_signal² + 2·σ_a²        with SD_signal = 0.20 (assumed, §2 of the design)
```

Tolerating at most a **10% inflation** of SD_total, i.e. SD_total ≤ 0.22:

```
2σ_a² ≤ 0.22² − 0.20² = 0.0084   →   σ_a ≤ 0.0648
```

> **TRIGGER, FROZEN: if the measured mean per-item σ_a on the calibration split exceeds `0.065`,
> the eval phase runs `k = 3` answer draws per (question, context) and uses the per-item mean
> credit. Otherwise `k = 1`.**

k=3 restores the same 10% tolerance up to σ_a ≈ 0.112 (noise term becomes 2σ_a²/3). σ_a is measured
from **3 answer draws on every calibration item**, which the calibration phase runs regardless.
**Evaluated at SP2, on calibration data only, before any eval-item contact. The measured σ_a and
the resulting decision are recorded with the number, whichever way it goes.**

## 3. Policies and decision rules

Frozen; never chosen at runtime. τ values are filled in at the SP2 freeze commit.

| # | policy | gate call | decision rule |
|---|---|---|---|
| (i) | always-retrieve | none | retrieve |
| (ii) | never-retrieve | none | do not retrieve — floor |
| (iii) | similarity gate | none | retrieve iff `max_j cos(q, e_j) ≥ τ_sim` |
| (iv) | verbalized confidence, **no index** | 1 mini call | retrieve iff `p_verbal ≥ τ_verb` |
| (v) | FOK-gated, **BELIEVED index** | 1 mini call | retrieve iff `FOK ≥ τ_FOK` |
| (vi) | FOK + NOK | shares (v)'s call | (v)'s rule; **and** if `NOK ≥ τ_NOK`, append `CAUTION_INSTRUCTION` to the answer system prompt |
| (vii) | **rate-matched random** — attribution control | none | retrieve iff `H(seed=42, item_id) ≥ r`, r = (v)'s realised eval retrieval rate |

**Policy (vi) changes exactly one thing** relative to (v): a frozen instruction string. No
re-ranking, no re-retrieval, no filtering. **Policy (vii) costs zero new calls** — both of its
context states already exist for every item from (i) and (ii).

**Retrieval is identical wherever it happens:** top-5 cosine over the persona's own store entries
(`text-embedding-3-small`), variant removal sets applied first. Same retriever, same k, same store
for every policy.

**Three context states exist in the whole design**, and no more:
`S0` no facts · `S1` retrieved facts · `S2` retrieved facts + `CAUTION_INSTRUCTION`.
Answers are keyed `sha256(question_id ‖ context ‖ draw)`; judgments `sha256(question_id ‖ response)`.
Nominal 7 × 529 = 3,703 answer calls collapse to **~1,141** at k=1.

**Answerer:** FR's `GENERATION_SYSTEM_PROMPT` verbatim (`LifeMemEval/evaluate_e2e.py:108`). The
`S0` rendering shows the facts block as `(no facts retrieved)`; that is the only addition, and it is
recorded here rather than improvised.

## 4. BELIEVED index is primary — and why that makes H-C2 harder, not easier

The TRUE index reads lifecycle state from the persona ground-truth YAML. **No deployed system has
that**, so a control loop built on TRUE would be unfalsifiable in deployment. E1 measured the price
of dropping the oracle on FR-Bank and it is zero: believed delta **+0.2420** against TRUE's
**+0.2386**, retention **101.4%**.

But retention of *discrimination* is not fidelity of *content*. Measured from E1's committed
artifacts, with no API call:

> **FR-Bank's believed metadata marks only 64 of 104 genuinely superseded entries inactive —
> a recall of 61.5%.** At the event level, 36 of 46 resolvable supersession events have at least
> one side marked: 78.3%.

**So policy (vi) inherits a corrupted obligation map.** Roughly two in five genuinely superseded
entries are invisible to it. H-C2 is therefore **the strictest deployable form of the FR bridge**:
FR's typed-layer result had ground-truth lifecycle state, and this one does not.

> **If H-C2 holds under a 61.5%-recall obligation map, it means more, not less** — the payoff
> survives the corruption a real store actually has. **This framing is frozen and is to be stated
> in those terms, not softened into "we used store metadata."**

**TRUE runs as a labelled ceiling arm**, reported as `oracle ceiling` wherever it appears, and it
gates nothing.

## 5. RENDERER LOCK

> **E1's intact operating renderer is E2's index rendering. Period.**

`index_v2.py`'s output as committed at `e1-complete` — markers shown, counts shown — is the only
rendering any E2 policy sees. **A3 / names-only appears ONLY inside M2's 2×2 and touches no E2
policy.** No mid-study renderer swap, **regardless of what M2 finds**. If M2's minimal cell wins,
that is a **recommendation for E3**, not a change to E2. Swapping the renderer on M2's result would
be selecting the instrument on an outcome measured in the same study.

## 6. Calibration protocol

**Split (frozen):** calibration = `aisha, chenoa, dariush, david, patrick, samuel, thanh,
valentina` — 132 items, 22 PN. Eval = 32 personas — **529 items, 82 PN, 139 PRESENT, 308 ABSENT**.
Derivation `tools/make_split.py`; balance gap 1.18pp.

**Fitting, identical for every thresholded policy.** Uniform grid **{0.00, 0.05, …, 1.00}**
(uniform because E1's D10 recorded a narrow grid falling through to a fallback). Objective:
maximise `behaviour-typed credit ÷ expected serving cost per turn`, ties to **lower cost**.

- **(iii)** τ_sim swept over the same grid on the cosine scale; best-case reported.
- **(iv)** fitted per the mirrored **arXiv 2607.25600** protocol: elicit a structured provisional
  judgment plus a confidence, then select a **model-specific threshold on held-out calibration
  data**. Same grid, same objective — the baseline gets the literature's own best version of itself.
- **(v)/(vi)** τ_FOK on the same grid and objective; **τ_NOK** against `confabulation ÷ cost` on
  calibration PN items only.
- Each rival additionally records the threshold reproducing **(v)'s calibration retrieval rate**,
  for H-C1b's matched row — fixed before eval, never tuned to match afterwards.

**Freeze mechanics.** All fitted values → `THRESHOLDS_FROZEN.json`, sha256 in the SP2 commit
message; **the eval harness asserts that sha at startup and exits on mismatch** (the `ladder_luna.py`
device). No eval-split call may precede that commit. **Calibration personas appear in no eval-split
figure, ever.**

## 7. Frontier spot-check — P5, frozen before any spot-check call

150-item E1.7 subset, codex lane, **k=5** (E1.7 measured 1/300 cells reproducing across 5 draws).
Policies (i), (iv), (v), (vi) only.

**P5a — ATTENUATION.** Cost payoff = `credit(v) − credit(i)` on the subset.

> **HOLDS iff `payoff_frontier ≤ 0.5 × payoff_mini`.**

A point-estimate rule, deliberately loose: the ladder's own FOK index-delta ratio is
`0.0364 / 0.2602 = 0.14`, so ≤0.5× is a generous band. **At n=150 a spot-check cannot support a
tight one**, and pretending otherwise would be false precision. CI reported alongside, for
information.

**P5b — PRESERVATION.** Obligation payoff = confabulation rate `(vi) − (v)`.

> **HOLDS iff the point estimate is negative (a reduction), i.e. direction preserved.**

**Direction-only and explicitly under-powered**: the subset has ~40 PN items and the layer fires on
a subset of those, so the expected event count is order 10–20. **P5b is a sign check, not a test,
and is reported in those words.** The ladder predicts the obligation payoff *grows* with capability
(NOK delta 0.2139 mini → 0.3298 sol), so preservation is the conservative call.

**Cost columns for the spot-check are reconstructed-input bounds**, computed offline from the frozen
prompt texts with `tiktoken`, **labelled exactly as in E1.8 §2 — counted, not measured — and never
presented as measured.** The codex lane persists no per-call token telemetry (D24-E1/E1.8).

## 8. Budget

**Cap $25. Projection gate $15.** The cap check is **cumulative across processes**, summed over
cached responses per arm, not read from a single process's meter (D27-E1). Projection recomputed at
every stop point; above the gate stops the run.

## 9. Ride-along modules

**M1** (`modules/M1_NOK_FACTORIAL.md`) and **M2** (`modules/M2_RENDERER_AXIS.md`) **ride**, frozen at
this commit. M2's frozen prediction: **minimal / names-only wins on the structureless backends**,
per two convergent E1 results (E1.5 Run B markers, E1.8 A3 counts). Fourth cell ≈ $0.55.

**M3 is formally deferred to the cross-vendor API addendum**, recorded in `e1_metamemory/E2_BACKLOG.md`.

## 10. Eval hygiene

> **No eval-split answer text and no eval-split score is to be observed before the SP3 go — not by
> me, not by any script's stdout, not in a log tail.**

Enforced, not merely intended: the eval runner prints **counts, statuses, costs and hashes only**;
it holds no scoring code and imports none; answers and judgments are written straight to disk. **No
scoring script may be executed against eval outputs before the SP3 go.** SP3 reports census,
deviations and cost — and nothing else.

## 11. Stop points

| | when | reports | blocks |
|---|---|---|---|
| **SP1** | now | this file, frozen; tag `e2-sp1` | any elicitation |
| **SP2** | post-calibration, pre-eval | fitted thresholds, power recomputation, k-trigger decision with its number, six-item checklist | any eval-split call |
| **SP3** | post-eval, pre-scoring | census, failures, deviations, cost — **no metric** | any gate being read |

**SP2 mechanical checklist (conditional go).** 1 — every policy parameter fitted on calibration data
only and committed as frozen constants. 2 — power recomputation reported, bands untouched. 3 —
k-draw trigger evaluated, decision recorded with the number. 4 — cost projection < $15 including
ride-alongs and spot-check. 5 — `git status` clean and every file a committed artifact reads from is
tracked. 6 — zero eval-item contact to date. **All six pass → proceed through the eval phase to
SP3. Any failure, or any non-routine deviation, stops the run and reports.**

## 12. Deviations, amendments, and the phase-boundary assertion

Numbered continuously from **D28-E2** in one table with dispositions. Amendments are dated committed
files; **a frozen prereg is never edited**. Cache keyed `(item_id, policy, model, prompt_hash)`.
Seed 42, temperature 0. Persona-clustered bootstrap, 1,000 resamples.

**New structural control, from ledger item 11.** `tools/assert_clean.py` runs at **every phase
boundary** and fails the boundary if `git status` is not clean or if any file a committed artifact
reads from is untracked. **An untracked file that a committed artifact reads from is a stop
condition**, not a warning.

## 13. Scope fence

No paper-text edits. No renderer changes. No E3 content. No scoring code executed against eval
outputs before the SP3 go. No new stores, no re-ingestion, no relabelling, no rubric edit. Any
non-routine deviation stops the run before scoring.
