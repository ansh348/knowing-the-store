# ADDENDUM_CF2_OPENAI: a second vendor's small and large model on the counterfactual set (E5)

Registration for the author's freeze (program R117; drafted 2026-09-18 BEFORE any call; accepted as drafted by the author's ruling of 2026-09-19). Carries two predictions (P-S1, P-S2) with failure texts. Frozen by its sha256, recorded in `r82_counterfactual/cf2/NUMBERS_CF2.md` before the first call; the runner writes `cf2/rows/lock_openai.json` with that hash at start. Nothing here re-adjudicates a CF-2 row; the recorded lookup, mini, Haiku 4.5 and Opus 5 rows are read and never re-run.

## §1: Why

On the counterfactual set only Opus 5 exceeds the name lookup (Table 1: lookup 0.77; GPT-4.1 mini 0.72, Haiku 4.5 0.76, Opus 5 0.84), and Limitations concedes that one closed model family supplies the capability comparison. Two models of a second vendor, its small and its largest, test whether the advantage belongs to the largest models or to one vendor. Cost report: `scratch/e5_cost/REPORT_E5_COST.md` (2026-09-18).

## §2: Population and the recorded rows

The 444 store versions in 148 triples (`cf2/cf_cell.json`), the superseded-only ground-truth summary v2 of each (`cf2/cf_indexes.json` key `v2`; the arm `INDEXED-V2`). Never subset. Recorded rows read: the embedding name lookup on the v2 lists (AUX-CF2-NB6-V2 0.7663); `rows_MINI.jsonl`, `rows_H45.jsonl`, `rows_OP5.jsonl` (`INDEXED-V2`) for the table beside. Blind is 0.5 by identity (ADDENDUM_R82 §6): no blind call.

## §3: The run

Models `gpt-5.6-luna` and `gpt-5.6-sol`, raw OpenAI Chat Completions API (`api.openai.com`), messages `[system: prompts_e1.SYSTEM, user: prompts_e1.USER_INDEXED]` with the v2 text as `{index}`, digests asserted at import (`run_cf.py`), **no other system text** (no agent harness); settings **exactly the R74 X4 raw-API rows'**: reasoning effort and temperature unset (the provider default, medium), `max_completion_tokens` 2048; five draws per item (k = 5), MIN_DRAWS 3 at scoring, the X4 collapse. Served identifier asserted on every row (E1.7 rule); `prompt_tokens_details` and `completion_tokens_details` kept in every row (cached, cache-write and reasoning tokens, which X4 did not record). Rows `cf2/rows/rows_LUNA.jsonl`, `rows_SOL.jsonl`, resume key (`unit_id`, arm, draw).

**Sending order (registered).** Draw-major: draw 1 for all 444 items and both models, then draw 2, and so on, each pass with eight workers, so that a repeated prompt falls inside OpenAI's 30-minute cache window (a first send of these 1,482 to 1,727-token prompts bills as a cache write at 1.25× the input rate; a repeat within the window at 0.1×). No pass is started while the previous pass of the same model has calls in flight.

**Stopping rule (registered; the only one).** A hard cap of **30 USD** in the runner, metered from the rows at the page prices below, both models together. If the cap halts the run, the completed whole draws are scored under the multi-draw rule provided at least three are complete; a partial draw is discarded and disclosed with its row count. There is no other stopping rule.

## §4: Estimands and predictions

The registered counterfactual contrasts of CF-2: each model's whole-set AUROC (PN versus the rest) and per state under v2; each model minus the embedding lookup on the whole set, item-level and persona-grouped intervals (1,000 draws, seed 42, `cf2_score.paired`), the persona-grouped interval printed first on this set; PN versus PRESENT and W/T/L as for the other readers (`reviews/integration/POSTHOC_SPEC_R112.md`); the per-draw census (identical draws, median range) as R107 reports it.

- **P-S1.** GPT-5.6 Sol exceeds the embedding lookup on the whole set, reliably: both intervals exclude zero.
- **P-S2.** GPT-5.6 Luna does not: its difference from the lookup is not reliable (at least one interval includes zero) or is negative.

Failure texts, frozen: "P-S1 FAILS: GPT-5.6 Sol reads $A$ against the lookup's 0.7663, difference $D$ with intervals $I_{item}$ and $I_{persona}$." / "P-S2 FAILS: GPT-5.6 Luna exceeds the lookup reliably, $D$ with intervals $I_{item}$ and $I_{persona}$."

## §5: Held texts, both branches (Phase 3, by ruling; wording modest: "the largest model from each vendor", never a threshold or emergence claim)

- Both hold: Table 1 gains the two rows; Section 5's comparison sentence reads "GPT-4.1 mini, Haiku 4.5 and GPT-5.6 Luna do not exceed a similarity lookup over the list; Opus 5 and GPT-5.6 Sol, the largest model from each vendor, exceed it by $D_{O}$ and $D_{S}$."; the abstract's comparison sentence takes the same form; Conclusion sentence 1 names "the largest model from each vendor"; the Limitations clause on one closed model family is deleted.
- P-S1 fails: Section 5 and the abstract read "of five models only Opus 5 exceeds the lookup"; the Limitations clause becomes "one model of five exceeds the lookup, and the second vendor's largest model does not".
- P-S2 fails (Luna exceeds the lookup): the sentences say so with the number; the "largest model" phrase is not used.
- In every branch Table 1, `tab:cf-main`'s W/T/L and PN-versus-PRESENT rows, `fig:perstate` and Appendix C.2 gain the two readers, and `tab:runs`' counterfactual column reads "ran" for both (raw API, provider default).

## §6: Budget, order, STOP

Prices, OpenAI's model pages read 2026-09-18: Sol $4 input / $0.40 cached / $20 output per million, cache writes 1.25× ($5); Luna $0.20 / $0.02 / $1.20, writes $0.25. Recorded bases: prompt 1,615.6 tokens mean (the mini rows on the same prompts; X4's probes show the same count for all three OpenAI models), output at the X4 indexed means (Sol 132, Luna 197; p95 227 / 315). Projection (`scratch/e5_cost/REPORT_E5_COST.md` §5): draw-major with the cache engaging on draws 2 to 5, **$11.4**; every send a cache write (the cache not engaging), **$25.2**; every send a write at p95 tokens, **$30.7**, which the cap would cut inside draw 5 (four whole draws scored). Cap **$30** for both models together; the registration's own stopping rule replaces the ×1.3 launch test. Order: lock → probes (one call per model on the first item, served identifier, projection printed) → draw 1 both models → draw 2 → … → draw 5 → score. STOP: registration sha256 mismatch; served-identifier mismatch; a probe whose per-call cost exceeds $0.0135 (Sol) or $0.0008 (Luna), the p95 line; more than 2% of a lane's rows not OK after the retry; the cap.

## §7: Ledger and paper site

`cf2/NUMBERS_CF2.md` section 13: `AUX-CF2-OAI-LOCK`, `-OAI-PROBES`, `-OAI-LUNA-V2`, `-OAI-SOL-V2` (whole set, per state, both intervals, the lookup contrast), `-OAI-PNPRESENT`, `-OAI-DRAWS` (the per-draw census and the cache and reasoning token means), `-OAI-P-S1`, `-OAI-P-S2`, `-OAI-SPEND` (list-metered from the rows, cache-write and cache-read tokens priced at their rates; not an invoice). Paper: Table 1, Section 5, the abstract, the Conclusion, Limitations, `tab:runs`, Appendix C.2.

## Registration mechanics

Frozen by sha256 before the first call. Copied to `iclr2027_monitoring_submission/ARTIFACT/registrations/`. Amendments, if any, are appended as dated sections below the marker line and never edit the text above. The run proceeds on the author's freeze commit; nothing runs before it exists.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
