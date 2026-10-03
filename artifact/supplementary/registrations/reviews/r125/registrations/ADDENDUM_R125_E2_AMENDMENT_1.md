# ADDENDUM_R125_E2_AMENDMENT_1: names-only and counts-only on the three strong models (E2 Amendment 1; Task 5 of R125)

Amendment 1 to `registrations/ADDENDUM_CF2_NAMES_COUNTS.md` (E2; registered text sha256 `6cd4cb94c3a3a4dc…`, frozen at `177697a`), registered by program R125 (the brief of 2026-09-20) BEFORE any call on these items and frozen by the sha256 of the bytes above the marker line, recorded in `reviews/r125/FREEZE_R125.md`; the runner and the scorer assert it at start. It lives under `reviews/r125/registrations/` (the brief's fence); the main session appends it below E2's marker line at landing if the author so rules. E2's registered text is not edited. Three predictions (P-N3, P-N4, P-N5; E2's own P-N3 was a descriptive reading and keeps its name there), outcome vocabulary HELD / FAILED / NOT EVALUABLE.

## §1: Why

E2 ran the names-only and counts-only renderings on GPT-4.1 mini and Haiku 4.5 alone (Opus 5 out of scope for cost). Two mock reviews of the 6e73cc4 build ask for the same ablation on the three strong models, whose supersession scores sit at or above the lookup's (Task 1: Luna 0.9602, Sol 0.9602, Opus 5 0.9773 matched on supersession) and whose counted-state scores are the ones the moved-count control moved (Task 1, item 8).

## §2: Population and the recorded rows (read, never re-run)

The 444 items of the counterfactual set (`r82_counterfactual/cf2/cf_cell.json`), the superseded-only summary v2 (`cf_indexes.json`). Recorded intact rows read: Opus 5 (`cf2/rows/rows_OP5.jsonl`, `INDEXED-V2`: draw 1 alone, AUX-R110-A3 0.8400, the comparator for its one-draw run; the five-draw row 0.8405 beside), GPT-5.6 Sol (`cf2/rows/rows_SOL.jsonl`: draw 1 alone 0.8277, `r125_vectors.json` SOL_v2_d1; the five-draw row 0.8500 beside), GPT-5.6 Luna (`cf2/rows/rows_LUNA.jsonl`: the five-draw row 0.8417 for its five-draw run; its draw 1 alone 0.8265 beside, the comparable column), the name lookup 0.7663; each reproduced at four decimals by `r125_readers.py`.

## §3: The renderings (E2's, byte-checked; `reviews/r125/tools/r125_t5_build.py`)

`cf2_names_counts.names_only` and `counts_only`, E2's primary line-removal forms, applied to the recorded v2 text of every item, E2's locks (`cf2_names_counts.locks`) asserted on every version and the per-arm texts' sha256 asserted equal to E2's build (`cf2/build_nc.json`: INDEXED-NAMES `d901ebefef3b1e6b…`, INDEXED-COUNTS `1187e126d7671768…`; built and asserted 2026-09-20): the three models read the very texts GPT-4.1 mini and Haiku 4.5 read in E2. The dash rule is not run. E2's identity holds here too: under names-only the counted-state pairs' PN and PRESENT versions are byte-identical, so every reader's matched PN-vs-PRESENT on retraction and expiry is 0.50 by construction; under counts-only the supersession pairs differ only in the SUPRSD cell. The leakage screen is not re-run (both renderings are subsets of the screened v2 text; E2 §3).

## §4: Lanes (`reviews/r125/tools/r125_run.py`)

Prompts `prompts_e1.SYSTEM` / `USER_INDEXED` verbatim (digests asserted); served identifier asserted on every row (E1.7); the 888 (item, arm) units of `INDEXED-NAMES` and `INDEXED-COUNTS`; rows under `r82_counterfactual/cf2/rows/rows_r125_<LANE>.jsonl`.

| lane | model | settings (the analogue copied) |
|---|---|---|
| NC-OP5 | claude-opus-5 | k = 1, temperature unset, max_tokens 1024, Message Batches (E1's settings, one draw) |
| NC-SOL | gpt-5.6-sol | k = 1, raw Chat Completions, reasoning effort and temperature unset, max_completion_tokens 2048 (E5's settings); **run only under §6's rule** |
| NC-LUNA | gpt-5.6-luna | k = 5, raw Chat Completions, E5's settings, draw-major over the 888 units, eight workers; the draw-1 column is the comparable one |

## §5: Estimands and predictions (`reviews/r125/tools/r125_t45_score.py t5`)

Per model and rendering: the pooled AUROC on the whole set and per state (within the state's own items) with the persona-grouped interval; the paired difference against the recorded intact row (`cf2_score.paired`: item-level and persona-grouped bootstrap, 1,000 draws, seed 42; draw 1 against draw 1 for Opus 5 and Sol, the five-draw row against the five-draw row for Luna with its draw-1 row beside) and against the name lookup; counts-only minus names-only; the matched AUROC of PN against PRESENT (Task 1's metric, `r125_common.matched_block`) on the whole set and per state with the triple-level and the persona-grouped interval, and counts-only minus names-only under it.

- **P-N3.** Names-only is within tolerance of the intact row on the whole set: |Δ| ≤ 0.05 at the point (E2's P-N1 rule), for each of Opus 5, Sol and Luna. HELD iff all three; a model whose lane did not run is NOT EVALUABLE and the verdict is stated on the models run.
- **P-N4.** Counts-only is below names-only on the whole set and the difference is reliable, both intervals excluding zero (E2's P-N2 rule), for each of the three.
- **P-N5.** Counts-only is above 0.50 on retraction and on expiry under the matched metric, the persona interval excluding 0.50 (the lower bound above 0.50), for each of the three.

Failure texts are the numbers: "P-Nk FAILS on [model]: [quantity] reads [value] with intervals [item] and [persona]." No paper text is written by this session.

## §6: Budget, order, STOP

Caps as in ADDENDUM_R125_SIBLING §6 (Anthropic $10.00, OpenAI $10.00, enforced in the runner; neither API exposes a balance, the month's metered spend printed in the freeze record). Projection from one probe per lane (`probe`, `project`; E5's cost rule for the OpenAI draws, Batch at 0.5 for Anthropic). **The brief's rule, registered here:** if the OpenAI projection for Tasks 4 and 5 together (SB-MINI5 + SB-LUNA + SB-SOL + NC-LUNA + NC-SOL, plus the leak screen and the probes) exceeds the $10.00 cap, Task 4 runs in full first, then Task 5 with Luna and Opus 5, and NC-SOL is dropped as a registered outcome (its rows print NOT EVALUABLE; Sol's moved-count response is covered by E9). The runner refuses NC-SOL unless the recorded projection fits. Order: after Task 4's lanes → NC-LUNA draw-major (whole draws scored, a partial draw at the cap discarded), NC-OP5 submitted as a Batch, NC-SOL if it fits → poll → score. STOP: a registration sha256 mismatch; a texts sha256 mismatch against E2's build; a served-identifier mismatch; a projection over a cap; more than 2 percent of a lane's rows not OK after the retry.

## §7: Ledger and paper site

`r82_counterfactual/cf2/NUMBERS_CF2.md` section 15e: `AUX-CF2-R125-NC-LOCK`, `-NC-PROBES`, `-NC-PROJECTION`, `-NC-<MODEL>-NAMES`, `-NC-<MODEL>-COUNTS`, `-NC-MATCHED`, `-NC-P-N3`, `-NC-P-N4`, `-NC-P-N5`, `-NC-SPEND`. Paper site: the main session's (`tab:cf-names-counts` gains rows; nothing lands from here).

## §8: Disclosures

Registered after E2's two-model result, after E9 and E1 Amendment 1 (the moved-count rows of the same three models) and after Task 1's matched rows on the same items were known; no confirmatory design is claimed. The scorer's pre-freeze dry run found no lane and computed no value for this task.

<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
