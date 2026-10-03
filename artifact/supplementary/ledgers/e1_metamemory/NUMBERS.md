# NUMBERS — the canonical record

**One canonical value per figure. Anything not in this file does not go in a draft.**

Every number here is traceable to a committed artifact, named in the last column of its section.
Where a figure was measured more than once, the superseding chain is resolved here and the
superseded value is listed in **§13 — do not use**, with what replaced it.

Some numbers must never travel alone. Those carry a **⚠** and the annotation that must accompany
them; the annotation is part of the number.

---

## 1. Corpus and construction

| figure | value | source |
|---|---|---|
| personas | 40 | `build/items_final.json` |
| distinct questions (incl. probes) | 631 | ” |
| LifecycleBench base questions | 516 | ” |
| items built (question × backend × variant) | 2,653 | ” |
| **scoreable items** | **1,183** | ” |
| labels: PRESENT / ABSENT / PRESENT-NEGATIVE | 394 / 685 / 104 | ” |
| labels: UNRESOLVED / OUT-OF-SCOPE | 1,065 / 405 | ” |
| items by backend (all labels) | FR-Bank 1,378 · A-MEM 661 · Mem0 614 | ” |
| easy tier (scoreable) | 595 (463 positive) | `results/scores_e1.json` |
| **hard tier (scoreable)** | **588 (35 positive)** | ” |
| hard tier composition | 145 FR-Bank natural + 127 FR-Bank slot-ABSENT + 35 FR-Bank PN + 145 A-MEM natural + 136 Mem0 natural | `build/items_final.json` |
| PN subtypes | with-replacement 48 · without-replacement 56 | ” |
| ABSENT mechanism split | natural 426 · ablation 238 · ingestion-loss-attributed 19 · sweep-negative 2 | `results/scores_e1.json` |

## 2. Backends

| figure | FR-Bank | Mem0 | A-MEM | source |
|---|---|---|---|---|
| entries | 18,936 | 10,074 | 11,319 | `backend_census.json` |
| entries per persona (min–max) | 262–622 | — | 203–333 | ” |
| personas | 40 | 37 ⚠ | 40 | ” |
| carries `category` | 18,936 | 0 | 0 ⚠ | ” |
| carries `slot` | 18,708 | 0 | 0 | ” |
| carries a believed lifecycle field | 18,936 | `updated_at` only | **0** | ” |

⚠ **Mem0 excludes `alex`, `thanh`, `aisha`** — under 20 sessions each, excluded at Phase 0
resolution B2, before any elicitation.
⚠ **A-MEM's `category` is present on every note but constant at `'Uncategorized'`**, and its 23,403
`links` references resolve to **0** note ids. Both are reported, never repaired.

## 3. Instruments

| figure | value | source |
|---|---|---|
| two-channel presence: lexical recall | 0.697 | `two_channel_control.json` |
| two-channel presence: embedding recall | 0.965 | ” |
| **two-channel presence: combined recall** | **0.995 (ε = 0.005, equivalently a 0.5% miss probability)** | ” |
| embedding threshold (cosine) | 0.295, `text-embedding-3-small` | ” |
| lexical-only false-negative rate (the reason for the second channel) | 30.3% | `DEVIATIONS.md` D5 |
| natural-absent probes drafted / survived | 279 / **145 (52%)** | `natural_absent_summary.json` |
| probes needing a human read after the two instrument tightenings | 127 → 114 → **3** | `DEVIATIONS.md` D15 |
| PN verification: membership reads / members confirmed | 192 / 179 | `verify_results.json` |
| PN verification: semantic reads / obligation confirmed | 56 / 48 | ” |
| membership exclusions outside the three named patterns | 6 (tagged, reported) | ” |
| total verification reads | 393 | `DEVIATIONS.md` D8 |
| index v2: indexes built | 716 | `indexes_v2.json` |
| index v2: line count min / mean / max | 31 / 55.7 / 71 | ” |
| **index-leakage control (ladder L0)** | **0 leaks in every cell**, 180 calls, threshold >3/30 | `ladder_L0.json` |
| τ_lo / τ_hi / τ_gold | 0.20 / 0.80 / 0.50 | `PREREG_E1.md` |

## 4. E0 — feasibility probe (prior study, not prompt-comparable to E1)

| figure | value | source |
|---|---|---|
| blind FOK AUROC | 0.5087 | `e0_metamemory/RESULTS_E0.md` |
| indexed FOK AUROC | 0.8176 | ” |
| delta | +0.3088, CI [+0.2051, +0.4090] | ” |
| n (non-ABSENT / ABSENT) | 210 (141 / 69) | ” |
| blind-deduplicated sensitivity row | blind 0.5429, delta +0.2747 | ” |
| NOK (E0's null) | blind 0.4909 → indexed 0.5320, +0.0411, CI [−0.0569, +0.1255] | ” |

⚠ **E0 numbers are not prompt-level comparable to E1's** (D2): E0's system text asserts store
structure that Mem0 and A-MEM do not have, so E1 froze a different prompt module.

## 5. E1 headline — FOK

| row | n | blind | indexed-TRUE | delta | 95% CI | source |
|---|---|---|---|---|---|---|
| **hard tier (HEADLINE)** | 588 | **0.5258** | **0.7530** | **+0.2272** | **[+0.1177, +0.3504]** | `results/scores_e1.json` |
| hard tier, FR-Bank only | 307 | 0.4966 | 0.7003 | +0.2037 | [+0.0935, +0.3191] | ” |
| easy tier | 595 | 0.4422 | 0.6336 | +0.1914 | — | ” |

**Gates:** H1-hard (blind < 0.75) **HOLDS** at 0.5258. H2-hard (delta ≥ +0.10, CI excludes 0)
**HOLDS**; band **"> +0.15 — stands alone"**.

⚠ **H2-hard's FOK gain comes from recognising genuine absence, not from detecting slot ablation.**
Decomposition (E1.8): PN vs natural-absent = 0.5517 → **0.8782**; PN vs slot-ablated-ABSENT =
0.4336 → **0.4972, at chance**. The PN-vs-ablation separation is carried by NOK, not FOK. This
annotation must travel with the +0.2272. Source `results/mechanism_scores.json`.

## 6. E1 — NOK (FR-Bank only by construction)

| figure | value | source |
|---|---|---|
| blind NOK AUROC | 0.4946 | `results/scores_e1.json` |
| **indexed-TRUE NOK AUROC** | **0.7339** | ” |
| delta | **+0.2393**, CI [+0.1801, +0.2949] | ” |
| n / positives | 661 / 104 | ” |
| gate (≥ 0.65, delta ≥ +0.10, CI excludes 0) | **HOLDS** | ” |
| `nok_candidates_found` on PN items | 56 true / 48 false | ” |
| `nok_candidates_found` on ABSENT items | 10 true / 373 false | ” |
| `nok_candidates_found` on PRESENT items | 9 true / 165 false | ” |

**Scope, by construction:** the PN cell is empty on erase-mode backends, so H-NOK is FR-Bank-only.
That is a finding about the backends, not a subsetting choice (Amendment 1 §5).

## 7. E1 — believed-state axis

| backend | blind | TRUE indexed | TRUE delta | BELIEVED indexed | BELIEVED delta | retention |
|---|---|---|---|---|---|---|
| **FR-Bank** (n=661) | 0.5056 | 0.7442 | **+0.2386** | 0.7476 | **+0.2420** | **101.4%** ✓ |
| Mem0 (n=238) | 0.5746 | 0.4777 | **−0.0969** | 0.5741 | −0.0005 | n/a |
| A-MEM (n=284) | 0.5591 | 0.4526 | **−0.1065** | 0.5278 | −0.0313 | n/a |

**H-BELIEVED (retention ≥ 60%) holds on FR-Bank only.** On the erase-mode backends the TRUE index
is actively harmful: both deltas are negative with CIs excluding zero (Mem0 [−0.169, −0.025];
A-MEM [−0.173, −0.040]). Retention is undefined where the TRUE delta is not positive.

## 8. E1 — supporting measurements

| figure | value | source |
|---|---|---|
| Phase-C elicitation | 2,698 calls, **2,698 parsed, 0 failures** | `elicitation_main.json` |
| arms | 332 blind / 1,183 INDEXED-TRUE / 1,183 INDEXED-BELIEVED | ” |
| k=3 blind stability | **46/50 identical**, mean spread 0.012, max 0.20 | `results/scores_e1.json` |
| staircase (quantisation control) | AUROC 0.7516, n=150, 5 distinct values | ” |
| skip-rate at FOK < 0.20 | 280/588 hard items skipped, **97.5% of them ABSENT** | ” |
| skip-rate at FOK < 0.10 | 36/588 skipped, **100% ABSENT** | ” |

## 9. Capability ladder — **the capability table of record** (E1.7, k=5)

Matched FR-Bank cells, n = 84 (54 FOK-positive, 40 PN).

| | `gpt-4.1-mini` | `gpt-5.6-luna` | `gpt-5.6-sol` |
|---|---|---|---|
| **FOK** blind | 0.4488 | 0.5735 | 0.7099 |
| **FOK** indexed | 0.7090 | 0.7417 | 0.7463 |
| **FOK** delta | **+0.2602** | **+0.1682** | **+0.0364** |
| **NOK** blind | **0.5000 ⚠ᵈ** | 0.5585 | 0.5290 |
| **NOK** indexed | 0.7139 | 0.8526 | 0.8588 |
| **NOK** delta | **+0.2139** | **+0.2940** | **+0.3298** |

⚠ᵈ **`gpt-4.1-mini`'s blind NOK of 0.5000 is tie-degenerate, not a measurement** — its blind NOK is
**constant at 0.0 on all 84 items**, so every pair ties and the AUROC is 0.5 by arithmetic. Luna's
spans 48 distinct values and still fails to discriminate. This annotation must travel with that
cell (D23-E1).

**Headline: "scale buys coverage discrimination, not obligation awareness" — SUPPORTED**
(rule: P1 and P4 both hold; both do).

| prediction | observed | verdict |
|---|---|---|
| **P1** Luna blind NOK at chance | 0.5585, CI [0.4299, 0.6869], includes 0.50 | **HOLDS** |
| **P2** blind FOK mini < luna < sol | 0.5267 < 0.6745 < 0.8131 | **HOLDS** |
| **P3** FOK delta sol < luna < mini | +0.0364 < +0.1682 < +0.2602 | **HOLDS** |
| **P4** Luna NOK delta > 0, CI excludes 0 | +0.2940, CI [+0.1696, +0.4172] | **HOLDS** |

Source: `results/ladder_scores.json`, `RESULTS_E1_7.md`.

## 10. Frontier cells and reproducibility (E1.6 k=5 — supersedes all single-draw figures)

| cell | n | blind | indexed | delta | 95% CI |
|---|---|---|---|---|---|
| sol · FR-Bank FOK | 84 | 0.7099 | 0.7463 | +0.0364 | [−0.0930, +0.1600] |
| sol · FR-Bank NOK | 84 | 0.5290 | 0.8588 | **+0.3298** | [+0.1994, +0.4470] |
| sol · all 150 FOK | 150 | 0.8131 | 0.7697 | −0.0433 | [−0.1151, +0.0231] |
| **sol · external FOK** | 66 | 0.9130 | 0.8083 | **−0.1046** | **[−0.2024, −0.0174]** |
| luna · FR-Bank FOK | 84 | 0.5735 | 0.7417 | +0.1682 | [+0.0340, +0.3033] |
| luna · FR-Bank NOK | 84 | 0.5585 | 0.8526 | +0.2940 | [+0.1696, +0.4172] |
| luna · all 150 FOK | 150 | 0.6745 | 0.6652 | −0.0094 | [−0.1177, +0.0900] |
| **luna · external FOK** | 66 | 0.7894 | 0.4514 | **−0.3380** | **[−0.4896, −0.1811]** |

**H1 does not hold at the frontier**: sol's blind FOK on all 150 is 0.8131, above the 0.75 bar.
**The largest inversion in the study is luna's external −0.3380.**

| reproducibility | sol | luna | mini |
|---|---|---|---|
| cells identical across 5 draws | 3/300 (1%) | **1/300 (0%)** | — |
| per-item FOK SD (mean) | 0.0946 | **0.1372** | 0.0069 ⚠ᵐ |
| blind → indexed dispersion ratio | 0.589 | 0.562 | not computable |
| codex duplicate-pair disagreement (D19) | **98/129** | — | — |

⚠ᵐ mini has multi-draw data on the **blind arm only** (k=3, 50 questions); its 0.0069 reflects a
near-constant response, not stability, and is not comparable to the frontier figures.
**Exploratory:** the index cuts draw-to-draw dispersion ~44% on both frontier models. Two models is
not a trend.

## 11. E1.5 mechanism runs

**Run A** — frontier indexed cell, decider between two frozen rules: **rule (b) fired, "cheap-model
equalizer"**, on both the single-draw and the k=5 redraw (`rule.reversed = false`).

**Run B** — marker mechanism, **UNRESOLVED**; the paper stays agnostic, as pre-registered.

| hypothesis | result | source |
|---|---|---|
| **H-b** omission vs marking, A-MEM | marked −0.1065 → nomarker −0.0378, CI [−0.1024, +0.0260] **includes 0** | `results/run_b_hb.json` |
| **H-b** omission vs marking, Mem0 | marked −0.0969 → nomarker −0.0865, CI [−0.1508, −0.0254] excludes 0 | ” |
| **H-a** index shifts FOK by label | FR-Bank PRESENT +0.264, PN +0.255, ABSENT +0.032; external all negative | `results/run_b_ha_hc.json` |
| **H-c** FOK ~ entry count (Spearman) | FR-Bank +0.142, Mem0 +0.006, A-MEM −0.094 | ” |

## 12. E1.8 mechanism probe — what channel carries the index effect

Pooled hard tier, n = 588. Each arm is the intact TRUE index with one manipulation to **counts
only**; ages, marker and all names byte-identical.

| arm | AUROC | Δ vs intact | 95% CI | ECE |
|---|---|---|---|---|
| blind | 0.5258 | — | — | 0.1596 |
| intact index | 0.7530 | — | — | 0.1741 |
| A1 counts-jittered | 0.7697 | +0.0167 | [−0.0174, +0.0552] | 0.1720 |
| A2 counts-coarsened | 0.7625 | +0.0095 | [−0.0390, +0.0657] | 0.1668 |
| **A3 names-only** | **0.8516** | **+0.0985** | **[+0.0426, +0.1577]** | **0.0583** |

FR-Bank row (n=307): intact 0.7003 · A1 **0.7018** · A2 0.7015 · A3 0.7283 — **all three within
0.05, all CIs include zero.**

**Verdict:** the FR-Bank row fires the frozen *"the signal is the category-coverage map ×
question-specificity, counts not load-bearing — this ANSWERS the 'reading a table you built'
objection"* clause. The pooled row reads MIXED mechanically **only because A3 is above the
reference**, a direction the frozen rules did not cover. **Nothing collapsed toward blind**; A3 −
blind = +0.3257, CI [+0.2414, +0.4143].

A3's pooled gain is entirely external: mean FOK on the all-ABSENT external hard tiers falls to
**0.0259** (A-MEM) and **0.0206** (Mem0), from 0.1645 / 0.1669 intact. Source
`results/mechanism_scores.json`, `RESULTS_E1_8.md`.

## 13. Economics (prices dated 2026-08-11; see `ECONOMICS.md` for provenance)

| figure | value |
|---|---|
| **mini blind gate** | **$234 / 1M calls** (480 in, 26.0 out, measured) |
| **mini indexed gate** | **$519 / 1M calls** (1,201 in, 24.0 out, measured) |
| **the index costs** | **+$285 / 1M calls** |
| mini indexed, prefix-cached as-run | $322 / 1M ⚠ list-price arithmetic, not billed |
| mini indexed, prefix-cached asymptotic | **$207 / 1M — below the blind arm** ⚠ same caveat |
| luna indexed, prompt text only | $236 / 1M ⚠ counted offline, lower bound |
| sol indexed, prompt text only | $5,898 / 1M ⚠ same |
| luna / sol indexed, probe-anchored ceiling | $14,275 / $100,218 per 1M ⚠ n=1 anchor |
| E1 Phase-C measured spend | **$1.4329** |
| E1.8 Step 2 measured spend | **$0.9040** |
| metered-equivalent of all frontier runs | **$7.67 – $198.39, computed-not-paid** (actually $0) |
| **mini indexed latency (measured)** | **mean 1.831 s, median 1.653 s, p95 2.952 s** (12 workers, n=653) |
| frontier latency (throughput-derived) | sol 8.94 s/call · luna 8.64 s/call (5 workers) |
| run wall clock | sol redraw 44.7 min · luna ladder 43.2 min (1,500 calls each) |

## 13A. Monitoring-paper auxiliary keys (v0.6 writing pass)

These rows promote values already present in committed monitoring artifacts or in the locked v0.5
source into the canonical record. They do not report new runs or recomputed intervals. `AUX-*` is a
stable source key for the v0.6 traceability ledger.

| key | figure | canonical value and annotation | source |
|---|---|---|---|
| **AUX-INTENT** | intent-conditioning audit | **20% precision** for the intent-blind expiry route; **110 of 413 (26.6%)** in-scope questions are structurally barred from PN | `FoK_working_draft_v0_5.tex` §2; `INTENT_RULES.md` lines 141--147 |
| **AUX-RETRACT** | inherited retrieval premise | retraction-record retrieval pass **5%** on AV7; this is a retrieval result, not an end-to-end monitoring result | `neuripsv14.tex` §3.2 / AV7 table; quoted in `FoK_working_draft_v0_5.tex` §2 |
| **AUX-E0CAL** | E0 non-forced calibration | mean blind FOK **approximately 0.26** against a **67%** non-ABSENT base rate; ECE **0.4155** | `e0_metamemory/RESULTS_E0.md` lines 132--138; `FoK_working_draft_v0_5.tex` §3.1 |
| **AUX-PNREADS** | PN verification total | **248** constituent judgments = 192 membership reads + 56 semantic reads | `DEVIATIONS.md` D8-E1, lines 371 and 404 |
| **AUX-ELICIT** | primary elicitation setting | `gpt-4.1-mini`, temperature **0** | `PREREG_E1.md` §7; `E1_DESIGN.md` §5 |
| **AUX-MECHDELTA** | FR-Bank jitter delta | randomizing every count changes AUROC by printed delta **+0.0015** | `RESULTS_E1_8.md` lines 63--68; `results/mechanism_scores.json` |
| **AUX-M1** | M1 monitoring-side factorial | **2^3** design; E1-config reproduction **0.7344** versus E1 **0.7339** | `e2_metamemory/modules/M1_NOK_FACTORIAL.md`; `e2_metamemory/RESULTS_E2.md` lines 124--131; M1 is the monitoring-side scope exception |
| **AUX-CACHEMIN** | cacheability condition | minimum cacheable prefix **1,024** input tokens | `ECONOMICS.md` lines 149 and 175; `tools/economics.py` constant |
| **AUX-PRICE-SPREAD** | frontier input-token list-price range | on **11 August 2026**, author-supplied list prices were **$0.20** per 1M input tokens for `gpt-5.6-luna` and **$5.00** for `gpt-5.6-sol`, a **25× per-input-token list-price range**; this is not a per-call or total-cost ratio | `ECONOMICS.md` lines 7--18 |
| **AUX-BELIEVED-FR** | E1 FR-Bank believed state | **5,968** entries marked inactive versus **approximately 102** explained by ground truth (**approximately 60x** overstatement); **78/109 (72%)** supersession events retain an active obsolete assertion at the recorded discriminator band | `BELIEVED_STATE.md` lines 14--44; `PHASE0_CENSUS.md` lines 106--110 |
| **AUX-BELIEVED-MEM0** | E1 Mem0 believed state | **1,276 (12.7%)** points carry `updated_at` | `BELIEVED_STATE.md` lines 49--62 |
| **AUX-PNSPOT** | PN membership instrument | pre-verification membership spot-check precision **69--86%** across backends | `E1_DESIGN.md` line 18; `RESOLUTIONS_APPLIED.md` line 88 |
| **AUX-TABLE-POS** | Table 1 backend FOK positive classes | Mem0 TRUE row: **94 non-ABSENT positives of n=238**; A-MEM TRUE row: **126 non-ABSENT positives of n=284** | `results/scores_e1.json`, `by_backend.mem0.TRUE` and `by_backend.amem.TRUE` |
| **AUX-REG** | monitoring-paper registration record | frozen artifacts (short commit hash; freeze date; prediction outcome): E0 prereg **0f2fde2c3b, 2026-08-10, held**; E0 Amendment 1 **d4ef3bee6a, 2026-08-10, N-A**; E0 Amendment 2 **c603f4a5ce, 2026-08-10, N-A**; E1 prereg **875f726fab, 2026-08-10, held**; E1 Amendment 1 **307865f414, 2026-08-10, N-A**; frontier addendum **3c3ef7dd6d, 2026-08-10, N-A**; redraw addendum **c92deefd44, 2026-08-10, N-A**; capability-ladder addendum **6860ad0a8c, 2026-08-11, held**; count-destruction addendum **281c410293, 2026-08-11, N-A**; NOK-factorial mini-registration **8597caa2dd, 2026-08-11, held/failed** (mixed registered predictions) | commits containing the ten named monitoring-side frozen artifacts; outcomes in `RESULTS_E0.md`, NUMBERS sections 5--12 and 15's monitoring-side M1 exception, and the corresponding results records |
| **AUX-REGDEV** | Appendix-E deviation index | ledger mappings: item **1** to E0 **D16**; item **2** to registered Phase-**0** resolution; item **3** to E1 **D2**; item **4** to E1 **D5--D6**; item **5** to E1 **D13**; item **6** to E1 **D15**; item **7** to E1 **D19/D21**; item **8** to E1 **D21**; item **9** to E1 **D24**; item **10** to E1 **D25**; Preventive to the E1.7 exact-model-id check | `e0_metamemory/DEVIATIONS.md`; `e1_metamemory/DEVIATIONS.md`; `E1_DESIGN.md`; `RESOLUTIONS_APPLIED.md`; `E1_7_ADDENDUM.md` |
| **AUX-INDEX-EXCERPT** | printed value-scrubbed counting-index excerpt | David FR-Bank FULL BELIEVED index: **575** entries; HOBBIES_RECREATION **29** entries, **18** active, **11** superseded, **0** retracted, **2** expired; PREFERENCES_HABITS **46** entries, **37** active, **9** superseded, **0** retracted, **1** expired; PROJECTS_ENDEAVORS **61** entries, **54** active, **7** superseded, **0** retracted, **18** expired. David Mem0 FULL BELIEVED index: **286** entries; per-category breakdown **not expressible by this backend** | committed `indexes_v2.json`, keys `indexes["frbank:david:FULL:BELIEVED"]` and `indexes["mem0:david:FULL:BELIEVED"]`, blob `b513eff8d25ceee087989a21af956c80a4dcac0e` |
| **AUX-SOURCED-OBJECTS** | printed prompt and example-item objects | frozen user prompt templates: blind **`Question: {question}`**; indexed preface and serialized index followed by **`Question: {question}`**. Exact elicitation wording begins **`FOK (feeling of knowing): the probability, 0 to 100`**. David examples: **`What's David's family background?`**, CURRENT-STATE, PRESENT; **`What was the name of your favorite childhood pet and what breed was it?`**, CURRENT-STATE, ABSENT; **`Does David have any upcoming exams to prepare students for?`**, UPCOMING, PRESENT-NEGATIVE | committed `tools/prompts_e1.py` lines 50--105; committed `build/items_final.json` item IDs `frbank:david:david_q08:FULL`, `probe:frbank:david:58071555`, and `frbank:david:david_q06:FULL`; question text also in committed `LifeMemEval/lifemembench_questions.json` |
| **AUX-CI** | reported monitoring CIs | paired percentile bootstrap with **1,000** item-level resamples, fixed seed **42**, and **2.5th/97.5th** percentiles; paired arm scores move together and single-class draws are discarded | `e0_metamemory/tools/score.py` lines 92--108; `e1_metamemory/tools/score_e1.py` lines 80--92; preregistrations confirm item resampling |
| **AUX-THEORY** | non-empirical formal constants | probability/trust domains **[0,1]**; uniform two-store error **1/2**; Appendix-A witness scores **0.95**, **0.85--0.90**, below **0.80**, and **0.70**; scalar example **tau_A=0.9**, **tau_B=0.4** | `FoK_working_draft_v0_5.tex` §2 and Appendix proof witness |
| **AUX-META** | format and bibliography numerals | the ICLR **2027** format identifier plus publication years, volumes, pages, and arXiv identifiers are bibliographic metadata inherited verbatim from the official style or the v0.5 bibliography, not scientific measurements | official ICLR 2027 style; `FoK_working_draft_v0_5.tex` bibliography |

## 13B. Monitoring-paper auxiliary keys (v0.9 cross-lineage and question-prior pass)

These keys transcribe committed, independently verified monitoring cells into the central record.
They do not recompute any result. The E1-XV and E1-QP two-direction verifiers respectively pass
**92/92** and **74/74** checks with no unaccounted numeric figure.

| Key | Scope | Canonical value | Committed source |
|---|---|---|---|
| **AUX-E1XV-CELL** | cross-lineage cell and new-lane protocol | matched FR-Bank cell **n=84**: **30 ABSENT**, **14 PRESENT**, **40 PN**; FOK positive = non-ABSENT (**54**), NOK positive = PN (**40**). The three new lineages use blind and indexed-TRUE arms, **k=5**, and minimum **3** surviving draws | `e1xv_crossvendor/NUMBERS_E1XV.md`; `PREREG_E1XV.md` |
| **AUX-E1XV-GATES** | registered cross-lineage items | **XV-1 failed** on **2 of 3** new lineages: Opus 5 blind NOK **0.6994**, CI **[0.5712,0.8135]**, above **0.50**; Haiku 4.5 **0.3688**, CI **[0.2571,0.4789]**, below **0.50**; K3 **0.5983**, CI **[0.4629,0.7160]**, includes **0.50**. **XV-2 held** on both registered frontier lineages: Opus 5 delta **+0.1528**, CI **[+0.0659,+0.2509]**; K3 **+0.2605**, CI **[+0.1456,+0.3866]**. **XV-3 held**: Opus 5 blind FOK **0.5855** exceeds Haiku 4.5 **0.3136**, a cross-generation price/capability ordering. **XV-4 held** on all **3**: window **[0.6590,0.7963]**, observed indexed FOK **0.7068**, **0.7287**, **0.7222** | `e1xv_crossvendor/NUMBERS_E1XV.md` registered-predictions table; `RESULTS_E1XV.md`; D93 |
| **AUX-E1XV-CONVERGENCE** | unregistered cross-lineage observation | across the **5** models with varying blind NOK, explicitly excluding mini from both endpoints, blind span **0.3307** and indexed span **0.0389**, an **8.50x** tightening; indexed range **0.8199--0.8588**. Across all **6** models, indexed NOK instead spans **0.7139--0.8588** (**0.1449**), because mini indexed NOK is **0.7139** | `e1xv_crossvendor/NUMBERS_E1XV.md` cross-vendor convergence; `results/e1xv_scores.json` |
| **AUX-E1XV-K3-PILOT** | K3 reasoning-effort provenance | **12-call** projection-basis pilot at default effort and a **4,096-token** ceiling: reasoning-token mean **1,027**, minimum **170**, maximum **2,426**; these are pilot figures, not full-run reasoning-token telemetry | `e1xv_crossvendor/manifests/calibration.json`; `PREREG_E1XV.md` |
| **AUX-E1QP-PROBES** | question-only prior audit | supervised persona-grouped TF--IDF: P1 full **n=84**, **40** PN, AUROC **0.7972**, CI **[0.6949,0.8927]**; P2 hard **n=307**, **35** PN, AUROC **0.9199**, CI **[0.8869,0.9472]**; powered P2 matched slice **n=162**, **35** PN and **127** slot-ablated ABSENT, AUROC **0.8436**, CI **[0.7813,0.8990]**, so QP-2 failed. Separate zero-shot mini probe on P1 full: **n=84**, **40** PN, AUROC **0.4804**, CI **[0.3587,0.5935]**, includes **0.50**. TF--IDF is label-supervised: it establishes extractable question-text signal, not monitor use of that cue; its leading coefficients are generator-specific template stems, so the matched slice is a second population rather than prior-controlled evidence | `e1qp_questionprior/NUMBERS_E1QP.md`; `results/e1qp_scores.json`; `tools/verify_e1qp.py` |
| **AUX-E1NS-DISPOSITIONS** | human-review accounting for AI-use disclosure only | **33** candidate PN rows received human dispositions: **12** confirmed PN, **11** finalized rejections, and **10** routed for further review; no E1-NS monitor call or scored result exists | `e1ns_neutralslice/build/post_removal_census.json`; `CENSUS_AND_PRICES.md` |
| **AUX-REG-XVQP** | v0.9 monitoring registrations | E1-XV preregistration short commit **776bce07b3**, frozen **2026-08-14**, mixed outcome **held/failed**; E1-QP preregistration short commit **10b3d4bff8**, frozen **2026-08-14**, mixed outcome **held/failed** | git commits containing `e1xv_crossvendor/PREREG_E1XV.md` and `e1qp_questionprior/PREREG_E1QP.md`; registered verdicts in the corresponding results records |

### E1-XV six-row table of record (new lineages; every row n=84)

| Lineage | Judgment / positive | Blind (95% CI) | Indexed (95% CI) | Delta (95% CI) |
|---|---|---|---|---|
| Opus 5 | FOK / **54** | **0.5855 [0.4492,0.7168]** | **0.7068 [0.5692,0.8222]** | **+0.1213 [+0.0047,+0.2449]** |
| Opus 5 | NOK / **40** | **0.6994 [0.5712,0.8135]** | **0.8523 [0.7501,0.9330]** | **+0.1528 [+0.0659,+0.2509]** |
| Haiku 4.5 | FOK / **54** | **0.3136 [0.2051,0.4383]** | **0.7287 [0.6041,0.8361]** | **+0.4151 [+0.2336,+0.5712]** |
| Haiku 4.5 | NOK / **40** | **0.3688 [0.2571,0.4789]** | **0.8199 [0.7251,0.9023]** | **+0.4511 [+0.3265,+0.5741]** |
| K3 | FOK / **54** | **0.6651 [0.5326,0.7912]** | **0.7222 [0.5967,0.8358]** | **+0.0571 [-0.0954,+0.2052]** |
| K3 | NOK / **40** | **0.5983 [0.4629,0.7160]** | **0.8588 [0.7636,0.9307]** | **+0.2605 [+0.1456,+0.3866]** |

## 13C. Monitoring-paper auxiliary keys (v1.0 $0 robustness pass, E1-R)

These keys transcribe the offline robustness pass into the central record. Analysis rules
were frozen in `e1r_robustness/SPEC_E1R.md` at commit **9ac91a2** before any figure here was
computed. No inference API was called; every figure is derived from committed artifacts.
The two-direction verifier `e1r_robustness/tools/verify_e1r.py` passes **346 checks, 0
failures, 0 unaccounted numerals**. The cell ledger of record is
`e1r_robustness/NUMBERS_E1R.md`; deviations are in `e1r_robustness/DEVIATIONS_E1R.md`.

Reproduction gates re-derived the published values first: **6/6** E1 calibration rows,
**12/12** matched-cell rows, **5/5** calibration arms, all to 4 decimals on n, blind,
indexed, delta, ECE, and AUROC.

| Key | Scope | Canonical value | Committed source |
|---|---|---|---|
| **AUX-E1R-CLUSTER** | persona-clustered sensitivity, E1 calibration rows | Point estimates unchanged; primary endpoint remains the preregistered item-level interval. Clustered CIs: hard headline **[+0.1552,+0.2996]**; FR-Bank hard **[+0.1259,+0.2767]**; easy contrast **[+0.1327,+0.2433]**; NOK FR-Bank **[+0.1552,+0.3237]**; Mem0 **[−0.1638,−0.0286]**; A-MEM **[−0.1654,−0.0446]**. **Every row excludes zero.** New figure: the easy-contrast item-level CI is **[+0.1179,+0.2596]**, previously unprinted | `e1r_robustness/results/clustered.json`; `tools/run_clustered.py` |
| **AUX-E1R-LOPO** | leave-one-persona-out fragility | **0 sign changes** on all six E1 rows; delta ranges hard **[+0.2148,+0.2441]**, FR-Bank hard **[+0.1876,+0.2199]**, easy **[+0.1811,+0.2011]**, NOK **[+0.2204,+0.2564]**, Mem0 **[−0.1133,−0.0854]**, A-MEM **[−0.1180,−0.0977]**. No E1 row depends on a single persona | `results/clustered.json` |
| **AUX-E1R-ICC** | why clustering does not inflate | Measured intracluster correlation of the paired indexed−blind contribution spans **[−0.0544,+0.0870]** — effectively zero. Clustered-bootstrap width ÷ cluster-jackknife width is **0.95–0.99** on all six rows, so two independent cluster-level variance estimators agree. Four of six clustered intervals are **narrower** than item-level. Pre-derived ρ\* thresholds frozen before computation: **0.205 / 0.339 / 1.055 / 0.164 / 0.257**; the NOK value exceeds 1 and was therefore unreachable by construction | `results/clustered_validation.json`; `tools/validate_clustered.py` |
| **AUX-E1R-CLUSTER-CELL** | persona-clustered sensitivity, 84-item matched cell (33 personas) | 11 of 12 rows keep intervals excluding zero. **One STOP row: Opus 5 FOK**, item-level **[+0.0047,+0.2449]** → clustered **[−0.0136,+0.2368]**. Every NOK row survives, including Opus 5 **[+0.0923,+0.2392]**, Haiku 4.5 **[+0.2925,+0.5981]**, K3 **[+0.1653,+0.3933]**. mini NOK carries the standing all-tie flag | `results/clustered_ladder.json`; `tools/run_clustered_ladder.py` |
| **AUX-E1R-BELIEVED-NOK** | BELIEVED-index NOK, previously uncomputed | Coverage **661/661** under both provenances; no new monitor call required. NOK FR-Bank BELIEVED: blind **0.4946**, indexed **0.5959**, delta **+0.1012**, CI **[+0.0458,+0.1543]**, clustered **[+0.0217,+0.1744]**, LOPO **[+0.0890,+0.1141]** with 0 sign changes. **NOK believed-index retention 42.3%**, against **FOK retention 101.4%** which reproduces the published figure. The frozen 60% gate is met for FOK and **not met** for NOK | `results/believed_nok.json`; `tools/run_believed_nok.py` |
| **AUX-E1R-BASELINES** | non-LLM readers of the same serialized indexes | On the FR-Bank populations the monitor beats every mechanical index reader: FOK **+0.0817** (TRUE) and **+0.0819** (BELIEVED), NOK **+0.1365** (TRUE). The exception is NOK-BELIEVED, where the monitor **0.5959** is indistinguishable from a local embedding matcher **0.5974** (difference −0.0015, inside the inherited ±0.05 tolerance). On the structureless backends every reader including the monitor sits at chance | `results/baselines_final.json`; `tools/run_baselines.py`, `tools/finalize_baselines.py` |
| **AUX-E1R-BACKEND-CONFOUND** | pooled hard-tier interpretation limit | All **35** pooled-hard positives are FR-Bank, so the one-bit rule "this item is FR-Bank" attains AUROC **0.7541**, above the monitor's pooled indexed **0.7530**. Pooled **absolute levels** are therefore not coverage discrimination for any reader. **Paired deltas are unaffected**: a score constant across arms cannot produce a delta, and the blind arm on the identical population is **0.5258** | `tools/verify_e1r.py`; D-E1R-4 |
| **AUX-E1R-ECE** | calibration intervals | Pooled hard tier, n **588**, base rate **0.0595**. ECE CIs: blind **[0.1349,0.1826]**, intact **[0.1529,0.1954]**, jittered **[0.1509,0.1935]**, coarsened **[0.1453,0.1882]**, names-only **[0.0418,0.0772]**. Paired vs blind: intact **+0.0145 [−0.0037,+0.0345] includes zero**; names-only **−0.1013 [−0.1171,−0.0815] excludes zero**. The intact index leaves calibration statistically unchanged, so "unimproved" is exact and may not be upgraded to "worse" | `results/ece.json`; `tools/run_ece.py` |
| **AUX-E1R-RELIABILITY** | ranker versus probability | Bins with n ≥ 10. Spearman ρ between mean predicted FOK and observed frequency: blind **0.1026** (p **0.8696**), intact **0.9000** (p **0.0374**), names-only **1.0000** (p **0.0000**). Indexed arms rank well and scale badly: mean predicted **0.217** against observed **0.056**, about **3.9×** over-confident. The blind arm neither ranks nor calibrates. Figure `results/reliability.pdf` | `results/reliability.json`; `tools/make_reliability.py` |

### E1-R do-not-use

| value | why |
|---|---|
| NB-3 index+question AUROCs **0.7024–0.9625** | reads question templates, not the store; index-only ablation is **0.4464–0.6909** while question-only is **0.8707–0.9667**. This is the D94 authorship confound reappearing inside a baseline built for this pass (D-E1R-2) |
| pooled hard-tier absolute AUROCs as coverage discrimination | backend indicator alone reaches **0.7541** (D-E1R-4) |
| any clustered interval for mini NOK | blind arm constant at 0.0; all-tie artifact |
| "persona clustering widens these intervals" | false here: ρ ≈ 0 and four of six narrow |

## 14. Do not use — superseded or wrong values

| value | where it came from | replaced by |
|---|---|---|
| sol blind FOK **0.7154** (all 150) | `results/strong_model_scores.json`, single draw pre-dedup | **0.8131** (E1.6, k=5). The intermediate post-dedup single draw was 0.7192; neither is canonical. |
| sol FR-Bank FOK single-draw **0.6318 → 0.7340, +0.1022** | E1.5 Run A | **0.7099 → 0.7463, +0.0364** (E1.6, k=5) |
| sol external single-draw **0.7843 → 0.8079, +0.0236** | E1.5 Run A | **0.9130 → 0.8083, −0.1046** (E1.6, k=5) |
| sol NOK single-draw **0.5463 → 0.8497, +0.3034** | E1.5 | **0.5290 → 0.8588, +0.3298** (E1.6, k=5) |
| sol all-150 single-draw **0.7192 → 0.7497, +0.0306** | E1.5 Run A | **0.8131 → 0.7697, −0.0433** (E1.6, k=5) |
| luna run "took ~80 minutes rather than ~45" | D22-E1 as first written | **43.2 min vs sol's 44.7** (D24-E1) |
| "~11,700 **reasoning** tokens" / "~3,157 **reasoning** tokens" | D22-E1 as first written | **turn totals** 11,712 / 3,157, n=1 per model (D24-E1) |
| mini per-call latency "~1.2 s" | `HEADLINE.md`, estimate | **1.831 s mean, 1.653 s median** (E1.8, measured) |
| `ABSENT-by-ingestion-loss` on 207 external labels | pre-D5 labelling | `sweep-negative`, then re-routed by the two-channel instrument (D6): **Mem0 8, A-MEM 13 ABSENT; 186 to UNRESOLVED** |

**Single-draw frontier figures remain committed** as the nondeterminism measurement (D19-E1, D21-E1).
They are not to be quoted as effect estimates.

---

## Rule of use

1. **A figure not in this file does not go in a draft.** If a draft needs one, it is added here
   first, with its source.
2. **Every ⚠ annotation travels with its number.** Dropping the annotation changes what the number
   claims.
3. **Superseded values are in §14 and are never quoted as estimates**, including in appendices.
4. Deviations are indexed in `DEVIATIONS.md`; registered-but-unrun work is in `E2_BACKLOG.md`.

---

# E2 AND E3 — added 2026-08-11

**Same rule of use.** One canonical value per figure; a figure not in this file does not go in a
draft; every **⚠** annotation is part of the number and travels with it. Sources are E2's and E3's
committed artifacts, named per row. Superseding chains are resolved in place, and superseded values
are listed in §14.

## 15. E2 — the control loop (verdicts as scored)

| figure | canonical value | source |
|---|---|---|
| n_eval | **529** items, 32 personas | `e2_metamemory/results/e2_scores.json` |
| **H-C2 — HOLDS** ⚠ | confabulation **-0.0579** adjusted (5.79pp), 95% CI **[-0.0874, -0.0307]**, unadjusted -0.0548 | `e2_scores.json` gates[0] |
| H-C2 credit side | **+0.0303** adjusted, one-sided 95% LB **+0.0115** | same |
| **H-C1a — HOLDS** | retrieval rate **0.684**; credit delta vs always-retrieve **+0.0197** adjusted, one-sided 95% LB **+0.0033** | `e2_scores.json` gates[1] |
| **H-C1b — VOID (unmatched)** | no rival row met the ±0.02 matching tolerance; (iii) realised 0.573, (iv) 0.543 against (v)'s 0.684 | `e2_scores.json` gates[2] |
| never-retrieve credit | **0.5822** — the highest of any E2 policy | `e2_scores.json` policy_table |
| attribution, (v) vs rate-matched random — credit | **+0.0522**, CI **[+0.0214, +0.0868]** | `e2_scores.json` attribution_vii |
| attribution, (v) vs rate-matched random — confabulation | **+0.0073**, CI **[-0.0155, +0.0278]**, includes zero | same |
| M1 best cell | **L1W0D0, AUROC 0.7958**, Δ over blind **+0.3012**; main effects L **+0.1980** · W +0.0134 · D -0.0193 | `e2_scores.json` M1 |
| M2 | minimal is the **worst** cell on both external backends (-0.1652, -0.1630) | `e2_scores.json` M2 |
| believed obligation map | **0.615** entry-level recall (61.5%) · **0.783** event-level recall (78.3%) | `e2_metamemory/believed_recall.json` |
| **⚠ H-C2's mix condition — part of the value** | **36.0% of E2's primary eval set is absence manufactured by the ablation.** E2's caution effect is **-10.16pp** on ablation-induced absence and **-0.83pp** on natural absence; the pooled -5.79pp is a weighted average of the two at E2's mix. **The number may not be quoted without this sentence.** | `e3_metamemory/results/q1_figure_data.json` |

## 16. E2 — economics, D44-corrected

**⚠ The published §3.11 dollar column is superseded.** `RESULTS_E2.md` §3.11-R is canonical.

| figure | canonical value | source |
|---|---|---|
| verified list prices, 2026-08-11 | gpt-5.4 **$2.50 / $0.25 / $15.00**; gpt-4.1-mini **$0.40 / $0.10 / $1.60** per 1M | developers.openai.com/api/docs/pricing |
| (v) FOK, $/1M turns | **1466** uncached · **1060** cached | `e3_metamemory/probes/p4_d44_price_fix.json` |
| (i) always-retrieve, $/1M turns | **959** | same |
| (ii) never-retrieve, $/1M turns | **421** | same |
| (v) vs always-retrieve | **1.5×** uncached · **1.1×** cached | same |

## 17. E3 — the policy inside a running agent (verdicts as scored)

| figure | canonical value | source |
|---|---|---|
| design | Design A snapshot ladder, rungs **{14, 20, 24, 32}**, **1021** cells = **834** eval + 187 calibration | `e3_metamemory/CELLS_E3.json` |
| derived operating points | **τ_FOK = 0.00**, **τ_NOK = 0.00**, p\* **0.2011**, L **0.1042** | `THRESHOLDS_E3_FROZEN.json` |
| **H-E3a — FAILS** | confabulation reduction **0.91pp** (adjusted -0.0091), 95% CI **[-0.0299, +0.0143]**, includes zero, against a ≥3pp band | `e3_metamemory/results/e3_scores.json` |
| H-E3b — EXPLORATORY | sequence broken at H-E3a; credit **+0.0135**, one-sided LB -0.0071, derived margin 0.02 | same |
| H-E3d — EXPLORATORY | (a) vs (a′) confabulation **+0.0094**, CI [-0.0123, +0.0295] — **the wrong direction** | same |
| H-E3c — VOID BY DERIVATION | τ_FOK = 0.00 makes arm (d) byte-identical to (a) on **0/834** differing prompts | same |
| arm confabulation | (b) **0.0971** · (a) **0.0851** · (a′) **0.0827** · **(a″) 0.0767** · (c) 0.0000 | same |
| arm credit | (b) 0.7512 · (a) 0.7632 · (a′) 0.7644 · (a″) 0.7560 · (c) **0.5815** | same |
| staleness trajectory | **non-monotone**: +0.86 / +0.28 / -0.12 / +2.09 pp; every rung's CI contains zero | same |
| index maintenance | **mean 1.11 µs/write** (median **1.00**) write-driven **and** one clock pass per serve — **two columns, never averaged**; $0 marginal LLM cost | `probes/p3_index_maintenance.json` |
| judge reliability ⚠ | confabulation flag **0.880** population-weighted (88.0%; FR reference 88%); four-way typing **0.715** (71.5%; FR 85%), PARTIAL-concentrated. **Credit-based figures inherit the second number.** | `judge_spotcheck_e3.json` |

## 18. E3 forensic — EXPLORATORY

**⚠ Every figure in this section is EXPLORATORY.** None is a gate; none may be described as
confirming or refuting a registered hypothesis; `RESULTS_E3.md` is unchanged by all of it.

| figure | canonical value | source |
|---|---|---|
| **Q1 mix model — predicted** | **-3.09pp**, 95% CI **[-5.56, -0.79]**, re-weighting E2's per-stratum caution effects to E3's mix | `results/q1_figure_data.json` |
| **Q1 — observed**, (a″) vs (b) | **-2.31pp**, 95% CI **[-4.59, +0.08]** — each interval contains the other's point estimate | same |
| Q1 — observed, (a) vs (b) | -0.91pp; residual vs predicted **+2.18pp** | same |
| Q1 — E2 per-stratum caution effect | PN -10.98 · ablation-absent -10.16 · PRESENT -4.32 · **natural-absent -0.83** pp | same |
| Q1 — mixes | ablation-absent **0.353** → 0.001 (35.3% → 0.1%); natural-absent 0.229 → **0.580** (22.9% → 58.0%) | same |
| Q3 habitat | **18 of 834 cells (2.2%)**; confabulation there ~4× the all-cell rate; **n < 20, not interpreted** | `results/forensic_e3.json` Q3 |
| **⚠ Q4 caution tax** | **+0.0909** on PN, CI [+0.0392, +0.1584]; **-0.0400** on PRESENT, CI [-0.0878, +0.0052] — **and -0.0345 on the calibration split, CI [-0.0707, -0.0048].** **Both intervals exclude zero in opposite directions. The two numbers travel together or neither is quoted.** | `forensic_e3.json` Q4 + `results/i2_precondition.json` |
| Q6 aging | contamination **0.0064** at peak (0.64%), **0 at rung 14**; store size **2.22×**; raw confabulation ratio **2.78×**, mix-standardised **2.06×** | `forensic_e3.json` Q6 |
| I1 | digest-name join **55.0%** of facts / **95.4%** of cells, recall **18/18**; slot-successor join **1.0%**, recall **0/18** | `DEVIATIONS_E3.md` D64 |
| I2 precondition | NOK AUROC for PN vs rest **0.7775** (bar 0.65) — **passes**; derived threshold **none exists**, calibration PN precision peaks **0.2660** against q\* **0.3796** | `results/i2_precondition.json` |

## 19. Do not use — E2/E3 additions

| value | where it came from | replaced by |
|---|---|---|
| (v) FOK **786** / **379** $/1M | `RESULTS_E2.md` §3.11 as published, answer component mini-priced | **1,466 / 1,060** (§3.11-R, D44 corrected) |
| "(v) is **6×** never-retrieve" | `RESULTS_E2.md` §3.11 prose | **13.4×** under the published column, **3.5×** corrected (D45) |
| E3 PN mass **110** eval cells | `PREREG_E3.md` §2, computed before the intent gate | **99** (D54) |
| H-E3d's SP1 FAILS text | written against the per-fact annotation | retired at Amendment 1; the annotation was empty by construction (D56) |
| I2's frozen answer to "why not selective caution" | `PREREG_I2.md` §4 | **the monitor CAN select (AUROC 0.7775); what it selects for does not replicate across splits** |

## 12. ADDENDUM_MARKER_ABLATION (E3, program R117): the inexpressibility marker omitted and neutralized (registered text sha256 `6d3afee82f2364b8...`, frozen at `177697a`; `tools/marker_arms.py`, `tools/marker_score.py`; `marker/`; scored 2026-09-19)

### AUX-MARKER-LOCK

Registration sha256 holds; the frozen prompt texts verified; the Omitted rendering (`run_b.strip_markers`, taken from the committed source by ast) reproduces the recorded E1.5 Run B cache keys on 522 of 522 items; the Neutral text is the ruling's, three lines replaced per key (77 keys), the wrapper `USER_INDEXED` with its quoted marker string replaced by the same text and nothing else (sha256 `8b68205ed47371c0...`). GPT-4.1 mini NEUTRAL: 522 calls, temperature 0, seed 42, max_tokens 200, a fresh cache namespace (`marker/cache`). GPT-5.6 Luna: four arms x 66 x 5 draws, raw Chat Completions, effort and temperature unset, `max_completion_tokens` 2048, served ['gpt-5.6-luna'].

### AUX-MARKER-OMITTED-MINI (the recorded E1.5 Run B rows, a recorded result), AUX-MARKER-NEUTRAL-MINI, AUX-MARKER-MODAL

| reader | backend | n / pos | arm | FOK AUROC [persona CI] | minus blind (item; persona) | minus structural (item; persona) | modal share | distinct | mean FOK |
|---|---|---|---|---|---|---|---:|---:|---:|
| GPT-4.1 mini | mem0 | 238 / 94 | BLIND | 0.5746 [0.5141, 0.6327] | - | - | 0.4202 | 6 | 0.2183 |
| GPT-4.1 mini | mem0 | 238 / 94 | STRUCTURAL | 0.4777 [0.4238, 0.5378] | -0.0969 ([-0.1686, -0.0250]; [-0.1638, -0.0286]) | - | 0.4622 | 5 | 0.1660 |
| GPT-4.1 mini | mem0 | 238 / 94 | OMITTED | 0.4881 [0.4206, 0.5475] | -0.0865 ([-0.1508, -0.0254]; [-0.1501, -0.0254]) | +0.0105 ([-0.0558, +0.0787]; [-0.0682, +0.0810]) | 0.6176 | 7 | 0.1542 |
| GPT-4.1 mini | mem0 | 238 / 94 | NEUTRAL | 0.5024 [0.4387, 0.5590] | -0.0722 ([-0.1391, -0.0046]; [-0.1311, -0.0121]) | +0.0247 ([-0.0394, +0.0940]; [-0.0439, +0.0862]) | 0.4664 | 5 | 0.1569 |
| GPT-4.1 mini | amem | 284 / 126 | BLIND | 0.5591 [0.5072, 0.6136] | - | - | 0.4014 | 6 | 0.2234 |
| GPT-4.1 mini | amem | 284 / 126 | STRUCTURAL | 0.4526 [0.3951, 0.5083] | -0.1065 ([-0.1726, -0.0403]; [-0.1654, -0.0446]) | - | 0.4648 | 5 | 0.1607 |
| GPT-4.1 mini | amem | 284 / 126 | OMITTED | 0.5213 [0.4652, 0.5773] | -0.0378 ([-0.1024, +0.0260]; [-0.0956, +0.0163]) | +0.0687 ([+0.0010, +0.1330]; [+0.0137, +0.1226]) | 0.6162 | 6 | 0.1548 |
| GPT-4.1 mini | amem | 284 / 126 | NEUTRAL | 0.5319 [0.4725, 0.5925] | -0.0272 ([-0.0890, +0.0354]; [-0.0708, +0.0251]) | +0.0793 ([+0.0148, +0.1443]; [+0.0140, +0.1437]) | 0.5282 | 5 | 0.1745 |

### AUX-MARKER-LUNA-66 (raw API; the recorded harness rows beside)

| reader | arm | FOK AUROC [persona CI] | minus blind (item; persona) | minus structural (item; persona) | modal share | distinct |
|---|---|---|---|---|---:|---:|
| GPT-5.6 Luna (raw API, k = 5) | BLIND | 0.6454 [0.5121, 0.7657] | - | - | 0.0909 | 31 |
| GPT-5.6 Luna (raw API, k = 5) | STRUCTURAL | 0.3528 [0.2259, 0.4948] | -0.2926 ([-0.4261, -0.1590]; [-0.4344, -0.1359]) | - | 0.0606 | 49 |
| GPT-5.6 Luna (raw API, k = 5) | OMITTED | 0.3088 [0.2005, 0.4250] | -0.3366 ([-0.4859, -0.1824]; [-0.4588, -0.2106]) | -0.0440 ([-0.1519, +0.0703]; [-0.1334, +0.0464]) | 0.0606 | 45 |
| GPT-5.6 Luna (raw API, k = 5) | NEUTRAL | 0.3782 [0.2595, 0.5126] | -0.2671 ([-0.4127, -0.1232]; [-0.3951, -0.1267]) | +0.0255 ([-0.0931, +0.1620]; [-0.0932, +0.1638]) | 0.0606 | 46 |
| GPT-5.6 Luna (harness rows, recorded, marked as Appendix B marks them) | BLIND / STRUCTURAL | 0.7894 / 0.4514 | -0.3380 | | | |

Draw census (Luna): draws per item-arm {5: 264}; rows not OK 0. The Omitted arm for GPT-4.1 mini shrinks the loss by at least half on A-MEM and not on Mem0 (a recorded result, not a prediction: mem0 {'delta_vs_blind': -0.0865, 'structural_delta': -0.0969, 'shrinks_by_at_least_half': False}; amem {'delta_vs_blind': -0.0378, 'structural_delta': -0.1065, 'shrinks_by_at_least_half': True}).

### AUX-MARKER-P-X2

**P-X2 FAILS on mem0: under the neutral wording the coverage loss against blind is mem0 -0.0722 with intervals [-0.1391, -0.0046] and [-0.1311, -0.0121], outside tolerance.**

### AUX-MARKER-P-X3 (descriptive)

The modal-score share falls against STRUCTURAL: {"mini": {"mem0": {"OMITTED": false, "NEUTRAL": false}, "amem": {"OMITTED": false, "NEUTRAL": false}}, "luna66": {"OMITTED": false, "NEUTRAL": false}}.

### AUX-MARKER-SPEND

GPT-4.1 mini NEUTRAL $0.1837; GPT-5.6 Luna $0.5231 (token-metered at the page prices); against the cap of $5.

