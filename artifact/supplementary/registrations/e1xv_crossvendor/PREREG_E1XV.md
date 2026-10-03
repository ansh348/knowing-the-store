# PREREG — E1-XV, cross-vendor replication of the ladder separation

**FROZEN.** Written after SP-0 rulings 1–6, **before any elicitation call on any of the three
lanes**. Every parameter below is either carried unchanged from E1's frozen artifacts or is a
numbered deviation whose measured basis is on the record in `DEVIATIONS_E1XV.md` and
`STEP0_LANES.md`.

No elicitation has run. The 84-item cell has never been elicited on any of these three models;
the only calls made are lane verification and the parse/cost pilots itemised in §7.

---

## 1. Cell

The **matched FR-Bank cell** that produced `NUMBERS.md` §9 (the capability table of record),
reconstructed by `tools/cell_e1xv.py` from committed artifacts using `score_ladder.py`'s own
definition and cross-checked against **both** committed k=5 files.

| | value |
|---|---|
| items | **84** |
| composition | **30 ABSENT · 14 PRESENT · 40 PRESENT-NEGATIVE** |
| FOK label vector | positive = **non-ABSENT**, **54** positives |
| NOK label vector | positive = **PRESENT-NEGATIVE**, **40** positives |
| arms | **BLIND** and **INDEXED-TRUE** (TRUE index only; no believed-state arm) |
| draws | **k = 5**, `MIN_DRAWS = 3`, per-item **mean over surviving draws** |
| calls | 84 × 2 × 5 = **840 per model**, **2,520 total** |

**54 + 40 = 94 > 84 is expected, not an error:** these are two label vectors over one item set,
not two subsets. FOK scores non-ABSENT (14 + 40), NOK scores PRESENT-NEGATIVE (40).

**Cache key:** `(item, arm, model, draw, prompt_hash)`. Resume is by that key, so an
interrupted run never repeats completed work and never double-counts — the resume discipline of
`redraw_frontier.py`, carried.

**Prompt module:** `prompts_e1.py`, imported not copied, with **both digests asserted before
use**; a drifted module raises rather than silently porting different wording.

```
file  sha256 337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84
texts sha256 35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2
```

`SYSTEM`, `USER_BLIND`, `USER_INDEXED` are **byte-unchanged** and slot only `{question}` and
`{index}`. **All three lanes use the system-role assembly form** (`elicit_e1.py:111–116`), which
differs from the concatenated form `redraw_frontier.py` used because `codex exec` has no system
channel — disclosed per ruling 5 and carried into §4's XV-4 statement (**D88**).

## 2. Lanes — pinned IDs and registered decoding

| | **Anthropic frontier** | **Anthropic cheap** | **Kimi K3** |
|---|---|---|---|
| **model ID, as served** | `claude-opus-5` | `claude-haiku-4-5-20251001` | `kimi-k3` |
| **provider** | Anthropic first-party | Anthropic first-party | **Moonshot direct**, `api.moonshot.ai` (**D90**) |
| **temperature** | **omitted** — provider default (**D86**) | **0** — frozen value honoured | **1** — sole permitted value (**D86**) |
| **max_tokens** | **1024** (**D91**, measured raise) | **200** — E1 value retained | **4096** (**D87**) |
| **reasoning effort** | default (thinking off) | n/a | **default `max`**, not forced |
| **submission path** | **Batch API** | **Batch API** | synchronous (no batch offered) |
| **$/Mtok in / out** | $5 / $25 | $1 / $5 | $3 / $15 |

**Temperature is a provider default wherever `T=0` is unsendable, recorded per lane** (ruling 3).
The three lanes therefore run at three effective sampling settings, and the write-up says so
rather than implying uniformity.

**Kimi K3, the two records carried to the paper:**

- **License — "open weights under Moonshot's custom K3 license."** Verified at the model card:
  *"Both the code repository and the model weights are released under the Kimi K3 License."*
  Open-weights release, 2.8T total / 104B active MoE, natively MXFP4.
- **Effort.** Vendor documentation: *"Kimi K3 always reasons and uses the top-level
  `reasoning_effort` field (`"low"`, `"high"`, or `"max"`; default `"max"`)."* **Effort IS
  controllable on this lane** — `low` cuts reasoning tokens 1,027 → 167 and cost 2.7× — and
  **the run uses the default, `max`.** Nothing is forced, so no effort deviation is logged.
  This is also the only setting that can answer XV-5, which is a claim *about* always-on
  reasoning.

**Batch path verified, not assumed** (ruling 1). 8 requests submitted through the Batch API
with contemporaneous synchronous references for the identical requests:

- **all 8 returned the exact model ID requested**;
- on the temperature-pinned lane (Haiku 4.5), **all 4 scored values `(fok, nok)` are identical
  across paths**; 2 of 4 are byte-identical and the other 2 diverge only in prose *after* the
  JSON, at character 799 of 815, in text the frozen parser discards;
- **the pass criterion is the scored value**, not the raw text, because `(fok, nok)` is what
  any AUROC consumes. This is stated rather than assumed: requiring byte-equality would test a
  quantity the study does not use.
- Opus 5's scored values differ across paths, and a **sync-vs-sync control settles the
  attribution**: two synchronous calls to the same endpoint disagree on **3 of 4** pairs, the
  same rate. **The variance is D86, not the batch path** — which is exactly what ruling 1 kept
  k=5 to absorb.

## 3. Parse rule — frozen

The **frozen E1 parse path**, unchanged: tolerant final-JSON extraction (`last_json`), then
`clamp` to [0,100] and divide by 100. `MAX_TOKENS` is a **lane parameter, not prompt content**
(ruling 4); no prompt text varies by lane.

**Reasoning-wrapped outputs (K3):** the bands parse **the final elicited value**. Reasoning
text is **stored with the raw row and never scored** — it is not concatenated into the parse
input, and no judgment is read out of it.

**Parse failures are counted, per lane per arm.** **> 5% in any arm flags the lane**, and that
lane's rows are **reported with the flag, not silently excluded.** Items falling below
`MIN_DRAWS = 3` surviving draws are excluded and counted, per the frozen protocol.

**Measured at freeze time** (pilot, §7), so the registered ceilings are not guesses:

| lane @ registered ceiling | blind parsed | indexed parsed |
|---|---|---|
| `claude-opus-5` @ **1024** | **10/10** | **10/10** |
| `claude-haiku-4-5-20251001` @ **200** | **10/10** | **10/10** |
| `kimi-k3` @ **4096** | **6/6** | **6/6** |

Haiku's indexed arm truncates at 200 on **10/10** calls while parsing **10/10**, because its
JSON precedes the discarded prose. It keeps E1's value because ruling 4 raises only on a
*measured parse failure* and there is none — the >5% rule stands as the live guard.

## 4. Registered predictions, per lineage

Reference values, `NUMBERS.md` §9, the OpenAI lineage at k=5 on this same cell:

| | `gpt-4.1-mini` | `gpt-5.6-luna` | `gpt-5.6-sol` |
|---|---|---|---|
| FOK blind / indexed | 0.4488 / 0.7090 | 0.5735 / 0.7417 | 0.7099 / 0.7463 |
| NOK blind / indexed | 0.5000 ⚠ᵈ / 0.7139 | 0.5585 / 0.8526 | 0.5290 / 0.8588 |
| NOK delta | +0.2139 | +0.2940 | +0.3298 |

⚠ᵈ mini's blind NOK is **tie-degenerate, not a measurement** (constant 0.0 on all 84 items).
That annotation travels with the cell (D23-E1) and is repeated wherever the value is cited.

> ### XV-1 — blind NOK at chance on every new model
> For **each** of `claude-opus-5`, `claude-haiku-4-5-20251001`, `kimi-k3`: the one-sample
> bootstrap 95% CI on **blind NOK AUROC includes 0.50**.

> ### XV-2 — the index restores obligation discrimination on each frontier lineage
> For **each frontier-class model** (`claude-opus-5`, `kimi-k3`): **indexed − blind NOK delta
> > 0** with the paired bootstrap 95% CI **excluding 0**.

> ### XV-3 — blind FOK orders by tier within the Anthropic pair *(descriptive, directional)*
> **blind FOK(`claude-opus-5`) > blind FOK(`claude-haiku-4-5-20251001`)**.
> **This pair is cross-generation** (Opus 5, 2026-07-24; Haiku 4.5, 2025-10-15), so **XV-3
> reads as a price/capability ordering, not a within-generation ladder** (ruling 2). No CI
> gate; reported with both point estimates and their one-sample CIs.

> ### XV-4 — indexed FOK lands in the OpenAI band *(descriptive)*
> The OpenAI indexed-FOK band on this cell is **[0.7090, 0.7463]**. XV-4 holds for a lineage
> whose indexed FOK falls within **±0.05** of that band, i.e. in **[0.6590, 0.7963]**.
> **This comparison crosses the D88 assembly-form difference** — the OpenAI k=5 rows were
> elicited with `SYSTEM` and `USER` concatenated, these lanes use the system role — and is
> reported as a band comparison across that difference, not as a matched contrast.

> ### XV-5 — reasoning does not manufacture the missing information *(descriptive, K3 only)*
> **Conditional on XV-1 holding on `kimi-k3`:** report that **blind NOK remains at chance
> despite always-on reasoning at default `max` effort** — deliberation cannot supply
> information absent from the monitor's view (Proposition 1, demonstrated on a reasoning
> model). If XV-1 fails on K3, XV-5 does not report; the XV-1 failure text governs.

## 5. FAILS texts — frozen, one per prediction

> **XV-1 FAILS on `<lineage>`.** Blind NOK discriminates above chance on `<lineage>` without
> the index; the claim that obligation awareness is absent from the model's prior is not
> general across vendors, and **the separation does not replicate on `<lineage>`; the ladder
> claim remains single-family.**

> **XV-2 FAILS on `<lineage>`.** The index does not restore obligation discrimination on
> `<lineage>`: the NOK delta CI includes 0. **The separation does not replicate on
> `<lineage>`; the ladder claim remains single-family.**

> **XV-3 FAILS.** Blind FOK does not order by tier within the Anthropic pair; coverage
> discrimination does not track capability tier off the OpenAI lineage, and the ordering
> reported in `NUMBERS.md` §9 is not reproduced across vendors.

> **XV-4 FAILS on `<lineage>`.** Indexed FOK on `<lineage>` falls outside [0.6590, 0.7963];
> the indexed operating point is lineage-specific rather than a property of the index.

> **XV-5 does not report.** XV-1 did not hold on `kimi-k3`, so no claim is made about
> reasoning and the monitor's view; the XV-1 failure text governs.

**A lineage that fails is reported, never dropped.** No lineage is removed from the table for
failing, no prediction is re-scoped after the fact, and the FAILS text ships in these words.

## 6. Scoring

**Estimator:** the committed scorers, imported not reimplemented — `score_e1.auroc`,
`score_e1.boot` for the paired delta, `score_ladder.auroc_ci` for the single-arm CI that XV-1
requires.

**Bootstrap:** the paper's committed procedure (`paper.tex:834`) — **1,000 item-level
resamples with replacement, fixed seed 42, paired-arm scores moving together**, percentile
interval.

**Draw-stability report (ruling 3), descriptive, reported beside every AUROC:** per lane and
per arm — per-item **SD across surviving draws** (mean, median, max), **count of items whose 5
draws are identical**, and the **blind → indexed dispersion ratio**, mirroring `NUMBERS.md` §10
so sampling noise is visible next to the point estimates rather than buried. This exists
because D86 leaves two of three lanes without temperature pinning, and the reader is entitled
to see how much of the spread is sampling.

**Reported per lineage:** blind and indexed FOK and NOK AUROC with CIs, the deltas with paired
CIs, the five registered items adjudicated **in their own frozen words**, parse-failure counts
per arm, and excluded-item counts.

**Outputs:** raw rows committed **as rows** before scoring; `NUMBERS.md` extended; verifier over
the new rows; `RESULTS_E1XV.md`.

## 7. Projection — measured, against the $28 cap

Per-call costs are measured on **real cell prompts at the registered lane parameters**, not
estimated: n=20 for each Anthropic lane, n=12 for K3.

| lane | in/call | out/call | $/call | ×840, batch applied |
|---|---|---|---|---|
| `claude-opus-5` @1024, batch | 1,486 | 181 | $0.01197 | **$5.03** |
| `claude-haiku-4-5-20251001` @200, batch | 1,068 | 119 | $0.00167 | **$0.70** |
| `kimi-k3` @4096, default `max` effort | 1,115 | **1,070** | $0.01940 | **$16.29** |
| | | | **TOTAL** | **$22.02** |

**The K3 line is itemised under max-effort assumptions, as required:** 96% of its output is
reasoning tokens (mean 1,027, min 170, max 2,426). Under a chat-model assumption the lane would
have been projected at roughly $1.10 and **under-costed 15×**.

| | |
|---|---|
| projected run | **$22.02** |
| billed to date (lane verification + pilots + batch verification) | **$1.1220** |
| **projected total** | **$23.14 of $28.00** — headroom **$4.86 (17%)** |

`k=3 + batch` would cost $13.21 and was **rejected at SP-0**: it sits exactly at `MIN_DRAWS`,
converting one lost draw into item exclusion on an 84-item cell, and D86 removes temperature
pinning on two of three lanes, so draw-averaging carries *more* variance here than in the
OpenAI lanes where k=5 was already required. **The slack is the protocol.**

## 8. Scope fence

No frozen E1 artifact is edited; the three lanes are **new registrations**. No paper text is
written in this run. **Results enter the paper only via a later Codex delta pass** — if the
cell is not scored by paper freeze, **v0.8 ships as-is and this becomes rebuttal material.**

**Paper pre-commitment, executed only in that delta pass:** if **XV-1 and XV-2 both hold on
both new lineages**, the limitations sentence *"one closed model family supplies the primary
capability comparison"* is replaced by the measured three-lineage statement — with K3 described
as **"open weights under Moonshot's custom K3 license"** — and one appendix table is added.
**Any failure leaves the sentence standing** and reports the result as-is.

## 9. Deviations at freeze

**D86** temperature unsendable on Opus 5 / forced to 1 on K3 · **D87** `MAX_TOKENS=200` fatal on
K3, raised to 4096 · **D88** system-role assembly form on all three lanes · **D89** the two
Anthropic lanes tokenise the same text 32–41% apart, **economics row only** · **D90** K3 served
by Moonshot direct, not OpenRouter routing · **D91** Opus 5 ceiling raised 200 → 1024 on a
measured 40% parse failure · **D92** batch path verified against a contemporaneous synchronous
reference, with the scored value as the pass criterion.

Full text, measured basis, and the diffs printed before use: `DEVIATIONS_E1XV.md`.
