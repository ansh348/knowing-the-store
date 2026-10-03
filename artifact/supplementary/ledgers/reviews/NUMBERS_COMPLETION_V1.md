# NUMBERS_COMPLETION_V1 — exploratory completion ledger

Source: `analysis/submission_completion_v1/REPORT.md` and linked JSON. Original ledgers are immutable.

## AUX-COMPLETION-REPAIR

| Answerer | Condition | Strict correct /31 | Partial | Incorrect | Stale endorsement /31 | Abstentions /31 |
|---|---|---:|---:|---:|---:|---:|
| MINI | R: repaired top five | 9 | 5 | 17 | 5 | 10 |
| MINI | A: NOK-gated stale fetch | 8 | 5 | 18 | 5 | 10 |
| MINI | B: NOK-gated successor assembly | 9 | 5 | 17 | 5 | 10 |
| MINI | C: successor assembly without NOK | 10 | 5 | 16 | 4 | 10 |
| MINI | D: matched-depth retrieval | 7 | 7 | 17 | 6 | 10 |
| H45 | R: repaired top five | 11 | 3 | 17 | 5 | 11 |
| H45 | A: NOK-gated stale fetch | 10 | 4 | 17 | 3 | 12 |
| H45 | B: NOK-gated successor assembly | 11 | 3 | 17 | 5 | 11 |
| H45 | C: successor assembly without NOK | 12 | 3 | 16 | 4 | 11 |
| H45 | D: matched-depth retrieval | 11 | 3 | 17 | 5 | 11 |

No primary correctness or stale label was indeterminate in the repaired sample. Nevertheless, 14 unique judgments give a determinate truth label alongside reference insufficiency/conflict, and three quotes fail exact-substring checks. These are flagged in `judge_integrity_flags.json`; the broad sensitivity treats uncertain references as unknown. There are no contradictory semantic labels for identical question/date/answer inputs. Sol shares a provider with MINI; this is not independent human validation.

| Answerer | Contrast | Correct gains / losses | Correct difference, pp [95% persona interval] | Stale difference, pp [95% persona interval] |
|---|---|---:|---|---|
| MINI | B-A | 1 / 0 | +3.23 [+0.00, +11.11] | +0.00 [+0.00, +0.00] |
| MINI | C-A | 2 / 0 | +6.45 [+0.00, +16.67] | -3.23 [-10.01, +0.00] |
| MINI | B-C | 0 / 1 | -3.23 [-10.01, +0.00] | +3.23 [+0.00, +10.01] |
| MINI | C-D | 3 / 0 | +9.68 [+0.00, +18.92] | -6.45 [-16.13, +0.00] |
| MINI | A-R | 0 / 1 | -3.23 [-11.11, +0.00] | +0.00 [+0.00, +0.00] |
| MINI | B-R | 0 / 0 | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] |
| MINI | C-R | 1 / 0 | +3.23 [+0.00, +10.01] | -3.23 [-10.01, +0.00] |
| MINI | D-R | 0 / 2 | -6.45 [-14.81, +0.00] | +3.23 [+0.00, +11.11] |
| H45 | B-A | 1 / 0 | +3.23 [+0.00, +8.57] | +6.45 [+0.00, +14.81] |
| H45 | C-A | 2 / 0 | +6.45 [+0.00, +13.89] | +3.23 [-7.14, +13.51] |
| H45 | B-C | 0 / 1 | -3.23 [-10.01, +0.00] | +3.23 [+0.00, +10.01] |
| H45 | C-D | 1 / 0 | +3.23 [+0.00, +10.01] | -3.23 [-10.01, +0.00] |
| H45 | A-R | 0 / 1 | -3.23 [-8.57, +0.00] | -6.45 [-14.81, +0.00] |
| H45 | B-R | 0 / 0 | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] |
| H45 | C-R | 1 / 0 | +3.23 [+0.00, +10.01] | -3.23 [-10.01, +0.00] |
| H45 | D-R | 0 / 0 | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] |

These are paired differences on 31 questions, using 10,000 persona-bootstrap draws, seed 20260917. Positive stale differences are harms. The one C−R correctness gain and stale reduction for each answerer is Fatima’s cancellation; B−C reverses it, so the NOK gate does not earn a selection-value claim. C−D is +3/31 correct for MINI and +1/31 for H45; intervals touch zero. A−R loses one correct answer for each answerer; H45’s two fewer stale endorsements come with an additional abstention. Full transition lists retain every adverse case, not only highlighted gains.
Uncertain-reference identification bounds for C−R remain [+1/31,+1/31] for both answerers and for C−D [+3/31,+3/31] / [+1/31,+1/31], because disputed labels are common or identical-answer cases for these contrasts. Their sampling intervals still include zero; this sensitivity is not human adjudication. Full-178 bounds retain the 147 unjudged questions. Historical controls, licensed/obligation breakdowns and every registered contrast remain in the JSON.
The engineering mechanism remains narrow: designated replacement IDs were present in 10/38 baseline cases, 14/38 before gates, 10/38 after the coverage gate, and 7/38 after the obligation gate. Reference-ID reach is not semantic reach; source spot checks found both useful undesignated evidence and misleading nominated IDs. The final cap dropped no first correction. Delivery, gating and answerer behavior remain separate. No new successor experiment was run.


## AUX-COMPLETION-DEPTH-COST

## Cached depth: fixed budget, missing outcomes retained

Frozen population: 557 questions, 174 licensed and 383 absent, two answerers, 2,228 answer cells. Deduplication yields 1,289 semantic inputs. Completed: 203 inputs across 8 personas, covering both depths on 100 questions per answerer (26 licensed, 74 absent). Pending: 1,086 inputs in 32 persona packets. These are not a substitute 100-question experiment.
The FOK selector ranks descending original FOK; NB-5 ranks descending cached whole-name-map similarity. Each allocates exactly 139 expansions. A boundary tie is uniformly averaged; random inclusion is 139/557. Always-five/ten have 0/557 expansions and are reference policies. All selectors use the same cached answers. Original reference-derived summaries/name maps are not native deployment inputs. No new thresholds or budgets were chosen.
The semantic endpoint applies strict source correctness to licensed questions and abstention to absent-store questions; an accidentally true factual answer to an absent variant is still inappropriate for the memory-only task. Missing outcomes are unknown. We withhold full-population semantic point estimates and confidence intervals; identification bounds below allow every unresolved differing answer to help or harm, while an identical answer has exactly zero paired effect. These bounds are not confidence intervals. The JSON includes the observed contribution, licensed gains/losses, absent inappropriate-answer bounds, and broad reference sensitivity without projecting the observed personas to the remainder.

| Answerer | Policy | Expansion expectation | Full net-resolution identification bounds vs five | Recorded answer-cost expectation | Allowance for all selector overhead vs ten |
|---|---|---:|---|---:|---:|
| MINI | always5 | 0 | [+0.000, +0.000] /557 | $0.124038 | $0.050794 |
| MINI | FOK | 139 | [-90.083, +88.139] /557 | $0.136574 | $0.038258 |
| MINI | NB5 | 139 | [-86.000, +78.000] /557 | $0.136706 | $0.038126 |
| MINI | random | 139 | [-57.147, +54.652] /557 | $0.136714 | $0.038118 |
| MINI | always10 | 557 | [-229.000, +219.000] /557 | $0.174832 | $-0.000000 |
| H45 | always5 | 0 | [+0.000, +0.000] /557 | $0.410226 | $0.145695 |
| H45 | FOK | 139 | [-111.556, +113.500] /557 | $0.449085 | $0.106836 |
| H45 | NB5 | 139 | [-107.000, +103.000] /557 | $0.449173 | $0.106748 |
| H45 | random | 139 | [-82.102, +81.104] /557 | $0.446584 | $0.109337 |
| H45 | always10 | 557 | [-329.000, +325.000] /557 | $0.555921 | $0.000000 |

Budget and tie values are expectations, including fractional gains and losses, not observed integer counts. No superiority or quality-retention claim is supportable from these missing outcomes. The prespecified retention criterion is a lower 95% bound above −1 percentage point against always-ten, plus lower total cost; it is unmet/unresolved, not inferred from similar points.
The old full-cohort mechanical results reproduce, but remain a separate proxy: at 139 expansions, net licensed gains were 6.833 versus 7.000 for FOK/NB-5 on MINI and 5.833 versus 6.000 on H45. Absent abstention losses were −5.861 versus −11.000 on MINI and −5.861 versus −9.000 on H45. These are exploratory expected counts, not source-validated semantic results. They cannot fill missing Sol judgments.
Recorded answer costs above price a single final answer at the selected depth, not a five-record answer followed by another ten-record answer. Original collection of both answers is research cost. FOK incurs an additional online monitor call per question (557); NB-5 needs local query embeddings, stored name embeddings and refresh/selection compute. No local inference was run here. Latency, hardware dollars, summary construction and refresh, name-vector maintenance, and retrieval compute are unmeasured and not assumed zero.
Measured historical E1 monitoring averaged $0.000519 per indexed-TRUE query; transferring that mean as a scenario costs $0.289083 for 557 questions. FOK then costs at least $0.425657 for MINI and $0.738168 for H45 before unmeasured work, exceeding always-ten’s $0.174832/$0.555921. At 139 expansions the monitor must cost below $0.000068686 or $0.000191806 per query, respectively, to save money. Amortizing the historical monitor cost would require at least 8 or 3 uses of the same valid score, respectively, before other overhead; query-conditioned scores cannot be amortized across unrelated questions. NB-5 may fit the allowance, but unmeasured costs and missing quality evidence prevent a savings claim.


## AUX-COMPLETION-SPEND

## Spend and delivery boundary

Before this continuation: measured list-rate cumulative $8.6320478; conservative cumulative $8.9960738. New completed semantic calls: 107 repair + 8 depth = 115, list-rate $13.393288, conservative cache-write allowance $16.541870. New usage: 3,148,582 input, 39,948 output, 0 cached tokens. No retrieval or task-answer generation calls.
Cumulative measured list-rate cost: **$22.025336**. Conservative charges plus both unresolved HTTP-429 byte-bound reservations ($1.287250) total **$26.825194**, leaving **$13.174806** under $40. These are token-accounted estimates, not provider invoices. Both old Opus batches were checked terminal, zero processing; all old repair/Sol attempts reconciled. A local single-writer lock guarded this continuation. Process command-line enumeration was unavailable; ordinary process enumeration showed this worker and the app, and the recorded ledgers held no competing reservation.
The remaining 32 frozen persona calls project to $9.817531 conservatively at their maximum outputs, within the remaining authorization. Execution is blocked by **provider credit_balance_exhausted**, not the research ceiling. One disclosed identical 429 recovery was attempted after cooldown; it returned the credit error and stopped. Both reservations remain held. No billing setting was changed or credit purchased. `DEVIATION_429.md`, `failures.jsonl`, `cost_ledger.json` and `pending_manifest.json` make this boundary reviewable.
Pricing was checked against [the official Sol model page](https://developers.openai.com/api/docs/models/gpt-5.6-sol); the recovery followed [official 429 guidance](https://help.openai.com/en/articles/5955604). The OpenAI Docs skill was used for that check.


## AUX-COMPLETION-PRINTED

Manuscript rounding: +3.23 [0.00,+10.01] pp = 100 times +1/31 and [0,0.10006410256410164]; +9.68 [0.00,+18.92] pp = 100 times +3/31 and [0,0.1891891891891892]. Correct/stale cells print paired counts 9/5, 11/5, 8/5, 10/3, 10/4, 12/4, 7/6. 203 / 1,289 semantic inputs observed; 1,086 pending. 0.136574, 0.449085, 0.174832, 0.555921 are six-decimal cost expectations from depth/costs.json; 0.038258 and 0.106836 are break-even selector budgets; 0.289083 = 557 × 0.000519. These are not quality-retention findings.
