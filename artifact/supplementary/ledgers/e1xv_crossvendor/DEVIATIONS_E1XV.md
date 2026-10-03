# Deviation ledger — E1-XV

Continues the counter from **D85** (E1-B).

**D86–D92 are pre-elicitation**, recorded before any call on the 84-item cell as the brief
requires: D86–D90 at STEP 0, D91–D92 at SP-0 under rulings 1 and 4. Each is a *decoding
parameter* or *routing* deviation — **no prompt wording is altered on any lane**, and the
frozen module's two digests are asserted at import (`cell_e1xv.py`) rather than trusted.

**D93 is post-scoring**, and is not a protocol departure at all: it records that two clauses of
a frozen FAILS text do not describe the outcome that occurred. It is filed here so the
correction travels with the registration instead of only with the write-up.

**D94 comes from E1-QP** (`e1qp_questionprior/`), not from this cell, and is likewise not a
protocol departure: it records an **instrument defect** — the benchmark's question text leaks
the PN label — that bears directly on every blind-arm number in E1-XV. It is filed here so a
reader of this ledger cannot reach the E1-XV blind results without meeting it.

**D95 comes from E1-NS** (`e1ns_neutralslice/`) and **is** a real protocol departure — the only
one in this ledger: an acceptance gate was amended after it failed. The full sequence is
recorded there in order (frozen → failed → mechanism proven → amended before any monitor call
and before any outcome), together with the unbiased safeguard the amendment was made to answer
to. It is filed here because it governs how any E1-NS number may be read.

---

## D86 — `TEMPERATURE = 0` cannot be sent on two of the three lanes

**Frozen:** `prompts_e1.py` sets `TEMPERATURE = 0`.

**Measured, one call each:**

| model | request | response |
|---|---|---|
| `claude-haiku-4-5-20251001` | `temperature=0` | **200 OK** — honoured |
| `claude-opus-5` | `temperature=0` | **400** `{'type': 'invalid_request_error', 'message': '`temperature` is deprecated for this model.'}` |
| `claude-sonnet-5` | `temperature=0` | **400**, same message — the whole current Anthropic generation |
| `claude-opus-4-5-20251101` | `temperature=0` | **200 OK** — honoured |
| `kimi-k3` (Moonshot direct) | `temperature=0` | **400** `{'message': 'invalid temperature: only 1 is allowed for this model'}` |
| `kimi-k3` (Moonshot direct) | `temperature=1` | **200 OK** |

**Diff, before use:**

```
  Haiku 4.5  temperature = 0        (frozen value, unchanged)
  Opus 5     temperature omitted    (parameter rejected; provider default applies)
  Kimi K3    temperature = 1        (only value the API permits)
```

**Disposition.** The parameter is omitted where it is rejected and set to the sole permitted
value where one is forced. It is **not** substituted with a near-value to look uniform: three
lanes run at three effective sampling settings and the write-up says so.

**Why this is tolerable rather than fatal.** The instrument for this cell is the frozen k=5
redraw protocol, whose score is the **per-item mean over surviving draws** — E1 adopted it in
E1.6 precisely because frontier lanes were not reproducible draw-to-draw (`cells identical
across 5 draws: sol 3/300, luna 1/300`). A protocol built to absorb sampling variation is the
right one to carry into lanes that cannot be pinned to temperature 0. **This raises the stakes
on the draw count**, which is why the cap ruling in `STEP0_LANES.md` is not a bookkeeping
question.

## D87 — `MAX_TOKENS = 200` is fatal on the K3 lane

**Frozen:** `MAX_TOKENS = 200`.

**Measured on real cell prompts, both arms:**

| ceiling | parsed | truncated | reasoning tokens | note |
|---|---|---|---|---|
| **200** | **0 / 4** | 4 / 4 | 197 of 200 output tokens | every call `finish=length`; JSON never reached |
| **4096** | **12 / 12** | 0 / 12 | mean 1,027, min 170, max 2,426 | 96% of output is reasoning |

Moonshot's own documentation: *"Kimi K3 always reasons and uses the top-level
`reasoning_effort` field (`"low"`, `"high"`, or `"max"`; default `"max"`)."* The frozen ceiling
was set for a non-reasoning chat model and does not survive contact with one that thinks before
every answer.

**Diff, before use:**

```
  Opus 5     max_tokens = 200       (frozen value at the time of this entry -- SUPERSEDED by D91)
  Haiku 4.5  max_tokens = 200       (frozen value, unchanged)
  Kimi K3    max_tokens = 4096      (200 yields 0% parse)
```

**Superseded in part.** This entry was written before the Opus 5 parse pilot. Opus 5's ceiling
was subsequently raised to 1024 on its own measured failure — see **D91**, which governs that
lane. K3's raise, the subject of this entry, is unaffected.

**Disposition.** The frozen ceiling is retained on the Haiku lane and raised on the K3 lane
here, and on the Opus 5 lane under D91. **The parse rule is unchanged** — E1's tolerant final-JSON extraction, applied to
the final elicited value, with reasoning text stored on the raw row and never scored.

**What this would have cost if missed.** A prereg pinning 200 across lanes would have
registered a lineage guaranteed to return nothing, and the brief's own ">5% parse failures
flags the lane" rule would have fired at 100% — reading as a *finding about K3* when it was an
artefact of a ported ceiling.

## D88 — system-message handling: the primary form ports, the redraw precedent did not use it

E1 has **two** committed prompt-assembly forms:

- `elicit_e1.py:111–116` — a genuine system role: `[{"role": "system", "content": P.SYSTEM},
  {"role": "user", ...}]`. This is E1's primary elicitation.
- `redraw_frontier.py:main` — `P.SYSTEM + "\n\n" + P.USER_*`, concatenated into one prompt,
  because `codex exec` takes stdin and offers no system channel.

E1-XV replicates the **k=5 redraw** numbers, so the concatenated form is the immediate
precedent; but all three E1-XV lanes expose a real system role, and the primary form is the
better-supported one. **All three lanes use the system-role form.** Wording is byte-identical
under either assembly; only the channel differs. Recorded so the difference from the
immediately-preceding protocol is visible rather than discovered later.

## D89 — the two Anthropic lanes do not tokenise the same text identically

Anthropic's pricing documentation: *"Claude 4.7 and later models … use a newer tokenizer that
contributes to their improved performance … This tokenizer produces approximately 30% more
tokens for the same text."*

**Measured on identical prompts:**

| prompt | Opus 5 | Haiku 4.5 | delta |
|---|---|---|---|
| blind (`aroha_q05`) | 691 | 522 | **+32%** |
| indexed (`aroha_q05`) | 2,227 | 1,580 | **+41%** |

**Disposition.** Affects the **economics appendix row only** — the two Anthropic lanes are not
counting the same units, and a naive per-token comparison between them would misstate the cost
ratio. **No effect on any AUROC**, which is computed over elicited values, not tokens. Recorded
because the economics row is a paper artefact and would otherwise imply a false equivalence.

## D90 — K3 is served by Moonshot direct, not by OpenRouter default routing

OpenRouter lists **14 endpoints** for `moonshotai/kimi-k3` (Morph, DeepInfra, Fireworks,
Together, Chutes, BaseTen, Modal, Phala, Wafer, Sail Research, DigitalOcean, Moonshot AI) at
**fp4, mxfp4, fp8 and bf16**, with per-provider differences in supported parameters. Default
routing across 840 calls would sample a rotating mixture, and the lineage label "Kimi K3"
would name that mixture rather than a model.

**Evidence this was a live risk, not a hypothetical.** OpenRouter **accepted `temperature=0`**
for `moonshotai/kimi-k3` and returned 200, while Moonshot's own API rejects any value but 1
— so that call demonstrably did not land on the vendor's endpoint. K3's weights are **natively
MXFP4**; Moonshot's own endpoint serves MXFP4, while several OpenRouter providers serve upcast
bf16/fp8.

**Disposition.** `kimi-k3` via `https://api.moonshot.ai/v1`. One vendor, one endpoint, one
quantisation, authoritative defaults. **Cost is identical** ($3/$15 per Mtok on both routes),
so the choice is free. OpenRouter remains verified-live as a fallback and its key is recorded.

**Standing lesson (ledger-class).** *An aggregator's model ID names a routing policy, not a
model.* When a lineage claim depends on which weights answered, pin the vendor endpoint — and
check a parameter the vendor is known to reject, because acceptance of an impossible parameter
is a cheap tell that the call went somewhere else.

---

**Not a deviation, a stop condition — since RESOLVED at SP-0.** The briefed cell projected to
**$27.36 against the original $15 cap**, with the K3 lane alone at $16.29. That was put to the
user rather than absorbed by quietly re-registering a parameter. **SP-0 ruling 1 raised the cap
to $28 and retained k=5 with the Anthropic Batch API**, explicitly rejecting the k=3 option
because it sits at `MIN_DRAWS` and because D86 leaves two of three lanes without temperature
pinning — *the slack is the protocol*. The registered projection is **$22.02**; see
`PREREG_E1XV.md` §7. Entries D91–D92 below post-date that ruling.

## D91 — Opus 5's output ceiling raised 200 → 1024 on a measured parse failure

**Ruling 4:** *"Per-lane ceilings set by the measured pilot (K3 = 4,096; others keep the E1
value unless a measured parse failure forces a logged raise)."* Opus 5 forced the raise.

**Pilot, 10 items × 2 arms per ceiling, same items both times:**

| `claude-opus-5` | blind parsed | indexed parsed | truncated | out max |
|---|---|---|---|---|
| **@ 200** (E1 value) | 8/10 — **20% failure** | 4/10 — **60% failure** | 8/20 | 200 (capped) |
| **@ 1024** | **10/10** | **10/10** | **0/20** | 321 |

Both arms blow the brief's 5% flag threshold at the frozen ceiling; the indexed arm by 12×.
The mechanism is ordering, not verbosity: **Opus 5 writes prose first and the JSON last**, so
a ceiling that cuts the tail removes the entire measurement. `gpt-4.1-mini`, for which 200 was
set, emits bare JSON.

**Diff, before use:**

```
  Opus 5     max_tokens 200 -> 1024   (measured 40% parse failure at 200, 0% at 1024)
  Haiku 4.5  max_tokens 200           (E1 value retained -- no measured parse failure)
  Kimi K3    max_tokens 4096          (D87)
```

**The raise costs essentially nothing.** $0.01167 → $0.01197 per call, **+$0.0003**, because
the model stops naturally at a mean of 181 tokens; the ceiling only removes the guillotine.
**The frozen ceiling was never costing money on this lane, it was costing data** — and it
would have cost it silently, as a 40% exclusion rate attributed to the lineage.

**Observation carried, not a departure: Haiku 4.5's indexed arm truncates on 10/10 calls at
200 and parses on 10/10**, because its JSON *precedes* the discarded prose. It keeps E1's value
because ruling 4 raises only on measured parse failure and there is none. Recorded because the
lane is running at its edge and the >5% flag is the live guard, not a formality.

**Standing lesson (ledger-class).** *A generation ceiling frozen against one model's output
shape is a silent filter on another's.* Before porting a max-token budget across vendors, check
where each model puts the payload — a ceiling that truncates commentary on one lane truncates
the measurement on another, and the failure presents as a property of the model.

## D92 — the batch path is verified against a contemporaneous synchronous reference

**Ruling 1:** *"Confirm the batch path serves identical model and params."* 8 requests were
submitted through the Anthropic Batch API, with the **identical requests** run synchronously in
the same session for comparison.

| check | result |
|---|---|
| served model ID equals requested ID | **8/8** |
| scored `(fok, nok)` identical across paths, temperature-pinned lane (Haiku 4.5) | **4/4** |
| byte-identical raw text, temperature-pinned lane | 2/4 |
| scored values identical across paths, Opus 5 | 1/4 — **not required, T unpinned** |

**The pass criterion is the scored value, not the raw text.** What this study elicits is
`(fok, nok)`; trailing prose after the JSON is discarded by the frozen parser and cannot reach
any AUROC. Where the two Haiku indexed calls diverge, they diverge at **character 799 of 815**,
in the discarded tail — a capitalisation difference in commentary. Requiring byte-equality
would have failed the check on a quantity the study never uses; the criterion is stated here
rather than quietly relaxed.

**Opus 5's cross-path disagreement is D86, not the batch path, and this was tested rather than
asserted.** A sync-vs-sync control — two synchronous calls to the same endpoint, same prompts,
back to back — disagrees on **3 of 4** pairs, the same rate as batch-vs-sync
(`manifests/sync_repeat_control.json`). With temperature unsendable there is no pinned draw to
reproduce, on either path.

**This is the empirical case for ruling 1's k=5.** Opus 5 disagrees with itself on the scored
value across repeat calls; the per-item mean over 5 draws is what makes that tractable, and
k=3 at `MIN_DRAWS` would have spent the protocol's entire tolerance on it.

**Batch is registered for both Anthropic lanes** and is not available on the Moonshot lane,
which is why the K3 column carries no discount.

## D93 — two clauses of the frozen XV-1 FAILS text do not describe the outcome

**Not a departure from the protocol — a defect in the registered prose, reported rather than
reworded.** The frozen text shipped verbatim in `RESULTS_E1XV.md`; this entry records what it
asserts and what the data show.

The registered XV-1 FAILS text reads: *"Blind NOK discriminates above chance on `<lineage>`
without the index; … and the separation does not replicate on `<lineage>`; the ladder claim
remains single-family."*

**Clause 1 — "discriminates above chance" — is false on one of the two failing lineages.**

| lineage | blind NOK | 95% CI | direction of failure |
|---|---|---|---|
| `claude-opus-5` | 0.6994 | [0.5712, 0.8135] | above chance — clause true |
| `claude-haiku-4-5-20251001` | 0.3688 | [0.2571, 0.4789] | **below chance — clause false** |

XV-1's gate is *"the CI includes 0.50"*. A CI can miss 0.50 from either side, and the prose
assumed only one. Haiku 4.5 is **anti-informative** blind, not over-informative.

**Clause 2 — "the separation does not replicate" — is false on both failing lineages.** The
separation is the indexed-minus-blind delta, and it replicated everywhere:

| lineage | NOK delta | 95% CI | excludes 0 |
|---|---|---|---|
| `claude-opus-5` | +0.1528 | [+0.0659, +0.2509] | yes |
| `claude-haiku-4-5-20251001` | **+0.4511** | [+0.3265, +0.5741] | yes — the largest in the study |
| `kimi-k3` | +0.2605 | [+0.1456, +0.3866] | yes |

**Cause.** The brief specified one sentence to ship *"if XV-1 or XV-2 breaks"*, and XV-1 and
XV-2 test different things — a baseline level and a paired difference. Bundling one conclusion
across both gates makes that sentence wrong in exactly the case that occurred: **XV-1 broke
while XV-2 held.**

**Disposition.** The frozen text ships **verbatim and unedited**, because a registration is
worth nothing if its failure text is rewritten once the failure arrives. The correction is
placed **beside** it, not in place of it, and the gate verdicts themselves are unaffected —
they were read mechanically from the CIs and independently reverified.

**Standing lesson (ledger-class).** *Freeze the gate and the verdict, not the explanation.*
A FAILS text should state which registered condition was not met and stop. When it also asserts
a mechanism ("above chance") or a downstream conclusion ("does not replicate"), it stakes the
registration on a prediction about *how* the failure will arrive — and a directional test that
can fail from either side will eventually falsify its own failure text.

## D94 — the benchmark leaks the PN label through question templating, and slot ablation does not fix it

**Not a protocol departure — an instrument defect, found by a check registered to be capable of
failing.** Recorded here because it bears on every blind-arm number in E1-XV.

`PREREG_E1QP.md` §4 registered **QP-2** as a falsifiable check rather than an assumption: re-fit
the text-only probe **on the matched slice itself** and require its CI to include 0.50. It
failed on the population with power.

| population | n | TF-IDF AUROC, question strings only | 95% CI |
|---|---|---|---|
| P1 matched | 49 | 0.4944 | [0.1777, 0.7874] — 9 negatives, no power |
| **P2 matched** | **162** | **0.8436** | **[0.7813, 0.8990]** |

**Whole-population leakage is worse:** PN-vs-rest from question text alone is **0.7972** on the
84-item cell and **0.9199** on the FR-Bank hard row.

**Mechanism — question generation, not topic.** The probe's weight is on template stems:
`have any`, `health conditions`, `family background`, `any upcoming` toward the negatives;
`who does`, `exercise does`, `planning`, `work` toward PN. The slot-ablated negatives are a
small pool of generic attribute templates replayed across personas — *"What health conditions
does X have?"*, *"What's X's family background?"* — while PN questions are bespoke — *"What team
is Aisha on at PwC?"*. The decisive pair is *"Where does Alex live?"* (negative) against
*"Who does Aisha live with?"* (positive): **same topic, opposite label, separable by template.**

CV is **grouped by persona**, so persona names cannot carry this; the stems generalise to unseen
personas, which is what makes it a property of the instrument.

**Why slot ablation could never have fixed it.** Slot ablation is a **store** operation: it
removes content so a question becomes unanswerable. It does not touch the question, and the
questions on the two sides of the contrast came from different generators. **Matching the store
operation does not match the text.**

**Consequences, stated rather than softened.**

- E1-QP's §5 prior-controlled reading is **withdrawn**, per its own frozen FAILS text.
- **This study has no prior-controlled slice**, so the index effect — positive with CIs
  excluding zero across six models — is demonstrated only on ground where the label is partly
  legible from phrasing.
- E1-XV's `claude-opus-5` blind NOK of 0.6994 **cannot be presented as store-independent
  obligation awareness**: the text-only ceiling on that cell is 0.7972, above it.
- A neutralised slice must be **built, not selected**: questions matched at authorship — same
  template, same generator — differing only in whether the store's content was later superseded.

**Standing lesson (ledger-class).** *Check that your control is a control.* "Topic-matched by
construction" was a plausible claim about a store operation that had never been tested against
the text it was supposed to neutralise; one supervised probe on the slice itself falsified it in
seconds and for $0. Any contrast asserted to neutralise a confound should be required to
demonstrate it on the slice that will actually be used.

## D95 — E1-NS's acceptance gate was amended after it failed, before any monitor call

**This is the move preregistration exists to prevent, so the full sequence is recorded in
order, and the reader is entitled to judge it on that sequence rather than on the outcome.**

**1. Frozen.** `SP_NS1.md` §2 registered the acceptance gate before any label was trusted: the
E1-QP TF-IDF probe (identical pipeline, persona-grouped 5-fold CV, seed 42) must return a CI
including 0.50 **and** a point estimate ≤ 0.55.

**2. Failed.** Three mechanical construction iterations, each revising **token admission** over
the whole vocabulary and never touching a question:

| iteration | tokens | n | PN | gate AUROC | 95% CI | verdict |
|---|---|---|---|---|---|---|
| C | 98 | 342 | 114 | 0.0415 | [0.0244, 0.0610] | FAIL |
| B | 12 | 99 | 33 | 0.2376 | [0.1369, 0.3419] | FAIL |
| A | 2 | 33 | 11 | 0.3326 | [0.1574, 0.5517] | pass, but n=33 |

**3. Mechanism proven, not asserted.** Under leave-a-persona-out CV a token's PN rate *in
training* is `(P−1)/(3P−1)` when the held-out item is PN and `P/(3P−1)` when it is not, where P
is the token's PN-persona count. **The held-out PN item always sits in a token just depleted of
one PN**, so PN items score low and the probe inverts. The gap is `1/(3P−1)`:

| variant | mean P | mean depletion gap | observed gate AUROC |
|---|---|---|---|
| C | 1.163 | **0.4602** | **0.0415** |
| B | 2.75 | **0.1650** | **0.2376** |
| A | 5.5 | **0.0651** | **0.3326** |

Monotone across a 7× range. **The gate was measuring its own estimator's finite-sample bias on
a slice whose population property is exact.**

**4. Amended — before any elicitation call, before any outcome observed.** SP-NS1 ruling 1
replaced the criterion with the exact population property:

> `P(PN | slot token) = 1/3` for **every** admitted token, verified as an exact rational
> equality and committed, with per-persona PN rates reported in the census.

**Verified:** 12 tokens, distinct rates `{1/3}`, no offender. `build/neutrality_report.json`.

**5. Safeguard added by the same ruling, and it is what makes the amendment testable.** An
*unbiased* estimator, in which held-out items share no informative feature with training:

| design | n | AUROC | 95% CI | includes 0.50 |
|---|---|---|---|---|
| token-grouped CV | 99 | **0.4922** | [0.3753, 0.6178] | yes |
| token + persona blocked CV | 34 | **0.4862** | [0.2979, 0.6779] | yes |

Both land on chance. **Had either excluded 0.50 the run would have stopped before the prereg**,
which is the condition the ruling set. The biased and unbiased estimators disagree by ~0.25 on
the same slice, in the direction and magnitude the depletion arithmetic predicts.

**Disclosure that ships with any E1-NS number.** The persona-grouped CV probe is reported as a
**descriptive** figure with its depletion arithmetic beside it, never as an acceptance result.

**Census caveat, reported not smoothed:** per-persona PN rates are not uniform — 14 of 40
personas contribute no PN item, and one (`david`) contributes only PN, 2 of 2. Persona identity
is not a feature the slice controls by construction; it is controlled by the grouped CV and by
the blocked safeguard above, both of which land on chance.

**Standing lesson (ledger-class).** *A gate inherited from another cell carries that cell's
assumptions.* E1-QP's probe was built to ask "does authored text carry the label?", where any
departure from 0.50 is leakage. Ported to a slice built to an exact ratio, the same estimator
measures its own bias. Before reusing an acceptance criterion on a differently-constructed
population, check that its null still holds there — ideally by running it on a population you
have constructed to be neutral, which is exactly what happened here by accident.

## D96 — two thirds of the benchmark's authored supersessions leave no trace in the store

**Ledger candidate. Not a departure — a measured property of the instrument, and it reaches
further than E1-NS.**

Every `supersession_events` record carrying a slot, across all 40 personas, tested with the
**frozen detector** (`index_v2.detect`, coverage ≥ `TAU_HI` = 0.80, cross-guarded) over the
persona's full store:

| | |
|---|---|
| authored supersessions with a slot | **121** |
| **store-retained** | **41 — 33.9%** |
| **no store trace** | **80 — 66.1%** |

**Why it matters beyond this cell.** That detector is not an E1-NS invention: it is the same
rule `true_lifecycle` uses to assign TRUE-provenance `superseded`. So a supersession the store
does not retain **cannot become a `superseded` entry under TRUE provenance either** — the gap is
inherited by E1's own lifecycle ground truth, not introduced by this construction.

**The number is an upper bound on non-retention, and the proof is in this cell.** Row 25
(`marcus/hobby`) reports "no trace" while the store holds eleven poker entries, including
`lb_00171` *"used to play poker on Thursday nights"* (inactive) and `lb_00186` *"quit playing
poker"* (active). The detector misses it on **morphology**: discriminative old tokens
`{plays, thursday, night, friends}` against a store that says *play* and *nights*, and `toks()`
does not stem, so coverage lands at 0.25. **A demonstrated false negative in the frozen
instrument.**

**Disposition.** Reported, not repaired. Stemming the detector would change a frozen threshold's
meaning across E0, E1 and every cell that has used it. The honest statement is that retention is
**at least** 33.9% and that the detector's recall on this task is unmeasured.

## D97 — the E1-NS construction miss: three failures of one assumption

**Mine, and it cost a human pass.** Enumeration admitted a (persona, slot) pair as PN whenever
the YAML authored a supersession for that slot. Three things followed from the single unchecked
assumption that *the YAML's slot vocabulary and the store's slot-key vocabulary are the same
vocabulary*. **They are not.**

**1. The retention conjunction was missing.** E1-B2 established that a lifecycle claim needs the
store to actually retain the material; the enumeration never asked. Of 33 dispositioned rows,
only 12 have detector-visible retention — and of the 12 the human confirmed as PN, only **3**.

**2. The key spaces do not match, so "0 entries under this slot" meant nothing.** `jerome/truck`
showed zero entries under `truck` while the store held *"drives a 2019 Freightliner Cascadia"* at
coverage 1.0; `samuel/fitness_routine` showed zero while the store held *"swims laps three
mornings a week at the YMCA"*; `saga/team` showed two irrelevant entries while the superseded
*"works on the podcast analytics team at Spotify"* sat under `employer`.

**3. The workbook inherited the same filter, so the human dispositioned on partial evidence.**
It printed entries under the slot key only. **Eighteen of 33 rows displayed "0 store entries"**,
and NOT-PN was the right call *on what was shown*. **Eight of those nineteen NOT-PN dispositions
are contradicted by the full-store detector** and have been routed back — human time spent
because of a filter I chose.

**Disposition.** The evidence addendum now runs the frozen detector over the full store for every
row and attaches the hits. Any future workbook shows full-store evidence, not slot-key evidence.

**Standing lesson (ledger-class).** *Two identifiers that share a name do not share a namespace.*
Before joining ground truth to a store on a key, verify the join produces non-empty results at
the expected rate — a join that silently returns nothing looks exactly like a true negative, and
if it feeds a human workbook it converts a schema mismatch into confident wrong labels.

## D98 — a permutation p was reported to four decimals with a Monte Carlo SE of 0.009

**From E2-AUDIT. Not a departure — a precision defect in a reported figure, found by an
independent re-derivation that was pre-committed to report either outcome.**

`RESULTS_E2OP.md` reports the H-OP1 permutation reference as **p = 0.8931**, from 893 of 1,000
random draws at or below the targeted rate. An independent implementation returned **0.92008**
from 920 of 1,000.

**Root cause, decomposed:**

| | |
|---|---|
| TRUE p, 100,000-draw reference | **0.90430** |
| MC standard error of any 1,000-draw estimate | **0.00930** |
| original (893/1000) deviation from true | −0.01119, **1.20 SE** |
| audit (920/1000) deviation from true | +0.01578, **1.70 SE** |
| gap between them, in SE of the difference | **2.05 SE** |

**Both are ordinary draws from the same sampling distribution.** The instability is structural:
the endpoint is a count over 529 items, so the permutation distribution has only **28 distinct
values** and **6.09% of draws land exactly on the targeted rate** — tie mass sitting on the
comparison boundary.

A second, genuine but negligible component: the original uses the Davison–Hinkley add-one form
`(n_le+1)/(N+1)` (`score_e2op.py:147`); the audit's first pass used the plain proportion. Worth
**+0.00008** here. The original's form is the more standard one.

**Effect on any verdict: none, and it reinforces rather than weakens.** H-OP1 failed on the
adjusted delta's CI including zero, not on the permutation. The better estimate of p is 0.9043,
placing the targeted arm *higher* in the random distribution than reported.

**Disposition.** `RESULTS_E2OP.md` is not edited; `E2_AUDIT.md` carries the second derivation and
both values. The figure should be read as **≈0.90 ± 0.03**.

**Standing lesson (ledger-class).** *Print a Monte Carlo quantity with its Monte Carlo error, or
print fewer digits.* Four decimals on a number whose SE is 0.009 asserts a precision the
estimator does not have, and invites a later re-run to look like a contradiction when it is a
second sample. Where the endpoint is discrete and ties fall on the decision boundary, raise the
draw count until the SE is small against the claim being made.

## D99 — the local E2-OP2 preregistration was frozen after reusable outcomes were visible

**Governance classification: draft, not registration.** The local file
`e2_metamemory/PREREG_E2OP2.md` first appears in commit
`e36a79f5f4564f9b3c8aca48a68c02eb13f4723a`, committed on 2026-08-14 at
04:48:22 +05:30. It was created in Claude Code session
`893c097c-9350-48e6-8d27-0a61678430b5` in response to the instruction to derive a threshold from
monitoring data, freeze an E2-OP2 protocol before its aggregate, and stop. The feasibility script,
its threshold output, and the preregistration were added in the same commit.

The E2-OP2-specific ungated contrast had not been assembled or scored, and no imported CC result
was visible before that commit. However, the clone already contained the reusable per-item S1/S2
judgments and earlier E2/E2-OP aggregates. The same session had accessed their outcome fields while
auditing E2-OP immediately before writing the local file. This fails the stricter requirement that
a registration predate any outcome knowledge in the clone. The local threshold is therefore not
scored and is not treated as a registered sensitivity point. CC's provenance-pinned registration
governs any later import.

**Local derivation.** The population was all 529 `split == "eval"` rows in
`e2_metamemory/gates_eval.json`, with no FOK gate: 308 ABSENT, 139 PRESENT, and 82
PRESENT-NEGATIVE rows. The positive class was PRESENT-NEGATIVE, the base rate was 82/529, and the
score column was `row["indexed"]["1"]["nok"]`. The inclusive selection rule was `nok >= tau` on
the grid 0.00, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70. The corresponding
`selected / true-positive / precision` rows were 529/82/0.1550094518,
285/57/0.2000000000, 216/46/0.2129629630, 199/45/0.2261306533,
197/44/0.2233502538, 144/32/0.2222222222, 42/8/0.1904761905,
41/8/0.1951219512, and 2/1/0.5000000000. The blanket point was ineligible; the first strict subset
meeting the exact base rate was the local draft threshold, 0.05.

**Root-cause clause.** The ambiguous rule text is: *“the lowest grid tau whose PN precision clears
that population's base rate.”* “Clears” does not specify strict `>` versus inclusive `>=`, whether
precision is rounded before comparison, or whether a nonzero clearance margin is required. The
prose also leaves the score draw and threshold-boundary convention unstated. The local code resolved
those choices as full-precision `>=`, draw 1, and `nok >= tau`. This ambiguity is already visible in
the carried precedent: applying the literal rule to the earlier gated population would admit a
lower grid point than the one previously frozen.

**Convergence status: open.** No provenance-pinned CC bundle is present in this clone. When it
lands, compare population, positive class, score column, grid, boundary, comparison/rounding rule,
and every precision row before importing any result. Record the exact divergent clause and amend
this entry with the artifact-to-artifact disposition; do not infer it from relayed numbers.
