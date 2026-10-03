# ADDENDUM_R122_MINI_K5: GPT-4.1 mini at five draws on the counterfactual set (T3)

Registration of program R122 (the no-human batch; the author's brief of 2026-09-19), written BEFORE any call. One OpenAI lane; no Anthropic call. Carries one prediction (P-K1) with a failure text; held texts for both branches. Frozen by the sha256 of the bytes above the marker line, recorded in `reviews/r122/FREEZE_R122.md`; the runner and the scorer assert it at start and the runner writes `reviews/r122/rows/lock_r122_oai.json`. The recorded one-draw rows are read and never re-run. Lives under `reviews/r122/registrations/` by the brief's fence.

## §1: Why

GPT-4.1 mini's counterfactual row is the one reader run once per item at temperature 0 (`rows_MINI.jsonl`, k = 1), while Haiku 4.5, Opus 5, GPT-5.6 Sol and GPT-5.6 Luna are five-draw means under the X4 collapse. Its scores take few distinct values, so many triples tie (PN, PRESENT and ABSENT versions at one score), which is where its low PN-versus-PRESENT and W/T/L sit. Five draws say whether the one-draw row is the reader or the protocol: whether averaging moves the whole-set AUROC, and whether the ties break.

## §2: Population and the recorded rows

The 444 store versions in 148 triples (`r82_counterfactual/cf2/cf_cell.json`), both summaries: `INDEXED-V2` (the superseded-only ground-truth summary, `cf2/cf_indexes.json` key `v2`) and `INDEXED-V3` (the all-states summary, key `v3`), the texts byte-identical to the recorded arms (the `cf2_run` units). Never subset. Recorded rows read: `cf2/rows/rows_MINI.jsonl`, arms `INDEXED-V2` (AUX-CF2-MINI-V2 0.7167) and `INDEXED-V3` (0.7967), k = 1; the lookups for the contrast columns, superseded-names on v2 (AUX-CF2-NB6-V2 0.7663) and all-states on v3 (AUX-CF2-ALLSTATES-V3 0.8756), gated at four decimals before scoring. Blind is 0.5 by identity (ADDENDUM_R82 §6): no blind call.

## §3: The run

Model `gpt-4.1-mini`, the frozen P0 texts (`prompts_e1.SYSTEM` / `USER_INDEXED`, file sha `337d37d3…`, texts sha `35d9b968…`, asserted by `run_cf` at import), raw OpenAI Chat Completions, no other system text; **k = 5** draws per (item, arm) unit, 888 units, 4,440 calls; `max_tokens` 200 (the recorded mini lane's and the Haiku 4.5 lane's value); **temperature unset, the provider default** (deviation D-R122-1, below); the X4 collapse at scoring (per item the mean over its OK draws, MIN_DRAWS 3; an item with fewer than three OK draws is excluded and counted). Served identifier asserted on every row (E1.7 rule). Rows `reviews/r122/rows/rows_MINI5.jsonl`, resume key (`unit_id`, arm, draw); `prompt_tokens_details` kept (cached tokens).

**D-R122-1 (recorded here, before any call).** The brief fixes "temperature and other settings as the Haiku 4.5 and Opus 5 lanes used (provider default where they left it unset)". The two lanes disagree on temperature: Haiku 4.5 ran at 0, Opus 5 left it unset (`run_cf.LANES`; `max_tokens` 200 and 1,024). The parenthetical names the case that applies to Opus 5 only, and the nearest recorded precedent for an OpenAI five-draw lane on this set, E5 (GPT-5.6 Luna and Sol, ADDENDUM_CF2_OPENAI), left temperature unset; at temperature 0 the five draws of a non-reasoning model would be near-identical and the tied-triple clause of P-K1 could not move. Temperature is therefore unset (the provider default) and `max_tokens` is 200; the five-draw row is read beside the recorded one-draw row with this difference stated wherever it prints. The alternative (temperature 0 at five draws) is not run.

**Sending order (registered).** Draw-major: draw 1 for all 888 units, then draw 2, and so on, eight workers, no pass started while the previous pass has calls in flight, so a repeated prompt falls inside OpenAI's cache window (draws 2 to 5 billed at the cached input rate on the prompt when the cache engages). Lane order within the batch: this lane runs LAST (after the two T4 lanes), so that the batch cap, if it bites, cuts this lane's last draw and the completed whole draws are scored under the multi-draw rule.

## §4: Estimands and prediction

Per summary: the five-draw row scored with the CF-2 conventions unchanged (`cf2_reader_score`: whole-set and per-state AUROC against `y_nok`, the persona-grouped interval, the paired difference against the summary's lookup with item-level and persona-grouped intervals, PN versus PRESENT, W/T/L over the 148 triples, the count of distinct collapsed score values, the per-draw census); the recorded one-draw row scored the same way beside it; the paired difference five-draw minus one-draw on the whole set and per state, both intervals (1,000 draws, seed 42); and **tied triples**: the number of the 148 triples whose PN, PRESENT and ABSENT versions receive the same (collapsed) score, for both rows.

- **P-K1.** Per summary, the five-draw whole-set AUROC is within 0.05 of the recorded one-draw row at the point estimate, and the tied-triple count falls (five-draw count strictly below the one-draw count). HOLDS iff both summaries satisfy both clauses.

Failure text, frozen: "P-K1 FAILS on `<summary>`: the five-draw row reads $A_5$ against the recorded $A_1$, difference $D$ with intervals $I_{item}$ and $I_{persona}$, and the tied triples move from $T_1$ to $T_5$."

## §5: Held texts, both branches (land only by the author's ruling)

- P-K1 holds: Appendix C.2, one sentence after the single-draw note: "At five draws with the provider's default temperature GPT-4.1 mini reads $A_5$ under the superseded-only summary and $B_5$ under the all-states summary, within $0.05$ of its one-draw rows, with the tied triples falling from $T_1$ to $T_5$ (Table~\ref{tab:mini-k5})." One table `tab:mini-k5` in Appendix C.2: the one-draw and five-draw rows per summary (whole set with the persona-grouped interval, per state, minus the lookup, PN versus PRESENT, W/T/L, distinct values, tied triples). The single-draw qualification in `tab:runs` and the body's "run once per item" phrase for mini stand, with the five-draw row cited beside them.
- P-K1 fails on the AUROC clause: the same appendix sentence states the move with the number ("moves by $D$ at five draws"), and the body's Table 1 note on mini's single draw gains "a five-draw run moves it by $D$ (Appendix C.2)". Fails on the tie clause only: the appendix sentence says the ties do not fall ($T_1$ to $T_5$) and nothing in the body changes. The table prints in every branch.

## §6: Budget, order, STOP

Prices, OpenAI's model page for `gpt-4.1-mini` as read 2026-09-19: $0.40 input / $0.10 cached input / $1.60 output per million (the recorded lane's `price=(0.40, 1.60)`; the cached rate is this file's addition). Recorded bases from `rows_MINI.jsonl`: prompt 1,616 tokens mean (v2), 1,668 (v3); output 25 mean, 26 at p95. Projection: draw 1 (888 calls, 1,458,096 prompt tokens at $0.40) $0.583 + output $0.036; draws 2 to 5 at the cached rate $0.583 + output $0.142; **expected $1.34** with the cache engaging; **$3.09** if no draw is cached; $3.10 at p95 output. The runner meters spend from the rows at these prices before every call against **the batch cap of 5.00 USD shared with T4** (T4's projection: $1.09 expected, $1.60 without the cache; the batch's expected total $2.43, $4.70 with no cache anywhere). STOP: registration sha256 mismatch; served-identifier mismatch on the probe; a probe whose per-call cost exceeds $0.0015; the cap (the completed whole draws are scored if at least three are complete, a partial draw discarded and disclosed with its row count; fewer than three whole draws is a FAIL to run, reported); more than 2% of the lane's rows not OK after the client's retries.

Order: lock → probe (one call on the first v2 unit; served identifier; per-call cost) → projection printed from the probes (refuse if the batch's expected spend plus what is already spent exceeds the cap) → T4's two lanes → this lane, draw 1 … draw 5 → `oai_score.py T3` → ledger.

## §7: Ledger and paper site

`reviews/r122/NUMBERS_R122.md` section T3: `AUX-R122-K5-ROWS`, `-K5-DELTA`, `-K5-P-K1`, and `AUX-R122-OAI-SPEND` (token-metered from the rows; not an invoice). Paper: Appendix C.2 (`tab:mini-k5`); the body only on the failure branch, as §5 states.

## Registration mechanics

Frozen by sha256 before the first call, in one commit with the other R122 registrations (`FREEZE_R122.md`). Amendments, if any, are appended as dated sections below the marker line and never edit the text above.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
