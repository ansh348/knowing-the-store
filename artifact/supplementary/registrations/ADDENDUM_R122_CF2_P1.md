# ADDENDUM_R122_CF2_P1: the counterfactual set under the intent-explicit rubric (T4)

Registration of program R122 (the no-human batch; the author's brief of 2026-09-19), written BEFORE any call. Two OpenAI lanes; no Anthropic call. Carries three predictions (P-R1, P-R2, P-R3) with failure texts; held texts for both branches. Frozen by the sha256 of the bytes above the marker line, recorded in `reviews/r122/FREEZE_R122.md`; the runner and the scorer assert it at start and the runner writes `reviews/r122/rows/lock_r122_oai.json`. The recorded P0 rows are read and never re-run. Lives under `reviews/r122/registrations/` by the brief's fence.

**Disclosure (registered).** This task was added by the author's brief after interim reads of the intent crossover (program R121: `cf2/results/cf_scores_ix_interim_draw1.json`, `cf_scores_ix_interim_3lanes.json`, `cf_scores_ix_interim_sol.json`, ledger section 14d-interim of `cf2/NUMBERS_CF2.md`). R121's held texts leave "rerunning the counterfactual set under the intent-explicit rubric" to the rebuttal period; this registration is that rerun. This session has not read the interim results or R121's scored outcome; the predictions below are the brief's, encoded without them.

## §1: Why

R121 asks whether the monitor's obligation judgment is intent-sensitive: under the frozen rubric P0 the same store scores a crossed question (one that may properly use the superseded content) as it scores the original, and P1, the intent-conditional rubric, is the rubric under which it should not. What P1 does to the original task, the counterfactual set's discrimination between store versions, is the other half: a rubric that lets a model separate intents is only usable if it keeps the model's counterfactual discrimination. R121 reads that on its 113 pairs (P-I5, descriptive); this registration reads it on the full 444 with the registered contrasts.

## §2: Population and the recorded rows

The 444 store versions in 148 triples (`r82_counterfactual/cf2/cf_cell.json`), the default summary only: `INDEXED-V2` (`cf2/cf_indexes.json` key `v2`), the texts byte-identical to the recorded arm. Never subset. Recorded P0 rows read: `cf2/rows/rows_LUNA.jsonl` (`INDEXED-V2`, k = 5; AUX-CF2-OAI-LUNA-V2 **0.8417**, supersession 0.9426 / retraction 0.5458 / expiry 0.6167, minus the lookup +0.0754 with both intervals excluding zero) and `cf2/rows/rows_MINI.jsonl` (`INDEXED-V2`, k = 1; AUX-CF2-MINI-V2 **0.7167**, 0.8308 / 0.5283 / 0.5489, minus the lookup −0.0496); the superseded-names lookup on v2 (AUX-CF2-NB6-V2 0.7663), gated at four decimals before scoring. Blind is 0.5 by identity: no blind call.

## §3: The prompt and the lanes

The P1 system text is imported from `reviews/r121/tools/prompts_p1.py` (`SYSTEM_P1`), whose sha256 **`c3c9a8e2b9798b50aa5a8f091f382b550e296f973f0c9af09d7fa38442cc7ce4`** (R121's registered value) is asserted at import by the runner and the scorer; the module itself asserts P1 is P0 with exactly its three registered substitutions and that the P0 digests are E1's. The user text is P0's `USER_INDEXED` with the v2 text as `{index}`, unchanged. No other system text.

- **Lane P1LUNA.** `gpt-5.6-luna`, raw OpenAI Chat Completions, **k = 5**, E5's settings exactly (reasoning effort and temperature unset, the provider default; `max_completion_tokens` 2048), draw-major over the 444 with eight workers (the E5 cache order), the X4 collapse at scoring (MIN_DRAWS 3). 2,220 calls. Rows `reviews/r122/rows/rows_P1LUNA.jsonl`.
- **Lane P1MINI.** `gpt-4.1-mini`, **k = 1**, temperature 0, `max_tokens` 200 (the recorded mini lane's settings, as in R121's MINI lane). 444 calls. Rows `reviews/r122/rows/rows_P1MINI.jsonl`.

Served identifier asserted on every row (E1.7 rule); `prompt_tokens_details` and `completion_tokens_details` kept (cached and reasoning tokens). Resume key (`unit_id`, arm, draw). Lane order within the batch: P1MINI, then P1LUNA, then T3's lane.

## §4: Estimands and predictions

Per reader: the P1 row scored with the CF-2 conventions unchanged (`cf2_reader_score`: whole-set and per-state AUROC against `y_nok`, the persona-grouped interval, the paired difference against the lookup with item-level and persona-grouped intervals, PN versus PRESENT, W/T/L, distinct values, the per-draw census); the recorded P0 row scored the same way beside it; the paired difference P1 minus P0 on the whole set and per state, both intervals (1,000 draws, seed 42); tied triples for both rows.

- **P-R1.** Each reader's whole-set AUROC under P1 is within 0.05 of its recorded P0 value at the point estimate (Luna: 0.8417; mini: 0.7167). HOLDS iff both readers satisfy it.
- **P-R2.** The per-state ordering is unchanged: for each reader, the three per-state AUROCs under P1, ordered by value, give the same order of states as the recorded P0 row (Luna and mini both: supersession > expiry > retraction). HOLDS iff both readers' orders are unchanged.
- **P-R3.** Luna's margin over the name lookup keeps its sign with both intervals excluding zero: Luna under P1 minus the lookup (0.7663) is positive and both the item-level and the persona-grouped interval exclude zero.

Failure texts, frozen: "P-R1 FAILS: `<reader>` reads $A_{P1}$ under the intent-explicit rubric against its recorded $A_{P0}$, difference $D$ with intervals $I_{item}$ and $I_{persona}$." / "P-R2 FAILS: under the intent-explicit rubric `<reader>`'s per-state order is `<order>` against the recorded `<order>`, with the moved state at $A$ against $B$." / "P-R3 FAILS: GPT-5.6 Luna under the intent-explicit rubric minus the lookup is $D$ with intervals $I_{item}$ and $I_{persona}$, not reliably positive."

## §5: Held texts, both branches (land only by the author's ruling)

- All three hold: Limitations' sentence "The main study was not rerun under the intent-explicit rubric." (R121's held text, if landed) is replaced by "Under the intent-explicit rubric the counterfactual set reads within $0.05$ of the frozen rubric for GPT-5.6 Luna and GPT-4.1 mini, with the same per-state order, and Luna keeps a reliable margin over the name lookup (Appendix C.2)."; if R121's sentence is not landed, the new sentence goes to Appendix C.2 after the intent-crossover paragraph. One table `tab:cf-p1` in Appendix C.2: per reader the P0 and P1 rows (whole set with the persona-grouped interval, per state, minus the lookup with both intervals, PN versus PRESENT, W/T/L, distinct values, tied triples) and the P1-minus-P0 difference with both intervals.
- P-R1 fails: the sentence states the reader and the move with the number, "moves `<reader>` by $D$ on the counterfactual set"; P-R2 fails: the sentence names the state whose rank moves and its two values; P-R3 fails: the sentence reads "and Luna's margin over the name lookup is $D$, not reliable, under it", and Section 5's "exceed it by $0.07$ to $0.08$" sentence gains the clause "under the frozen rubric". The table prints in every branch.

## §6: Budget, order, STOP

Prices, OpenAI's model pages as read 2026-09-18 (E5) and 2026-09-19: Luna $0.20 input / $0.02 cached / $1.20 output per million, cache writes 1.25×; mini $0.40 / $0.10 / $1.60. Recorded bases: the v2 prompt 1,616 tokens mean under P0 (`rows_MINI`, `rows_LUNA`); P1 adds 113 tokens to the system text (o200k: P0 457, P1 570), so **1,729** per prompt; Luna's output 192 tokens mean including reasoning, 327 at p95 (`rows_LUNA`); mini's 25. Projection: **P1LUNA** draw 1 (444 × 1,729 at the write rate $0.25) $0.192 + output $0.102; draws 2 to 5 at the cached rate $0.061 + output $0.409; expected **$0.76** with the cache engaging, $1.28 if no draw is cached, $1.64 at p95 output with no cache. **P1MINI** $0.31 + $0.02 = **$0.33**. Probes about $0.002. T4 expected **$1.09**, $1.60 without the cache. The runner meters spend from every R122 rows file at these prices before every call against **the batch cap of 5.00 USD shared with T3** (batch expected $2.43; $4.70 with no cache anywhere). STOP: registration sha256 mismatch; P1 sha256 mismatch; served-identifier mismatch on a probe; a probe whose per-call cost exceeds $0.0010 (Luna) or $0.0015 (mini); the cap (Luna's completed whole draws scored if at least three; a partial draw discarded and disclosed); more than 2% of a lane's rows not OK after the client's retries.

Order: lock → probes (one call per lane on the first v2 unit) → projection printed (refuse if the batch's expected spend plus spend so far exceeds the cap) → P1MINI → P1LUNA draws 1 … 5 → T3's lane → `oai_score.py T4` → ledger.

## §7: Ledger and paper site

`reviews/r122/NUMBERS_R122.md` section T4: `AUX-R122-P1-ROWS`, `-P1-DELTA`, `-P1-P-R1`, `-P1-P-R2`, `-P1-P-R3`, and `AUX-R122-OAI-SPEND`. Paper: Appendix C.2 (`tab:cf-p1`); Limitations or Appendix C.2 as §5 states; Section 5 only on the P-R3 failure branch.

## Registration mechanics

Frozen by sha256 before the first call, in one commit with the other R122 registrations (`FREEZE_R122.md`). Amendments, if any, are appended as dated sections below the marker line and never edit the text above.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
