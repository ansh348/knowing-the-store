# ADDENDUM_CF2_NAMES_COUNTS: names against counts, a two-by-two on the counterfactual set (E2)

Registration for the author's freeze (program R117; drafted 2026-09-18 BEFORE any call, the author's rulings of 2026-09-19 folded in: names only by line removal is the primary form for both readers, the committed A3 dash rule a secondary arm for GPT-4.1 mini only, counts only by line removal). Carries two predictions (P-N1, P-N2) with failure texts and one descriptive reading (P-N3). Frozen by its sha256, recorded in `r82_counterfactual/cf2/NUMBERS_CF2.md` before the first call; the runner writes `cf2/rows/lock_nc.json` with that hash at start. Nothing here re-adjudicates a CF-2 row; the recorded intact (v2) and blind rows are read and never re-run.

## §1: Why

The paper's claim is that the models draw their signal from the summary's attribute names, not its counts (Section 5; the own-name ablation; the moved-count control). The direct test on the counterfactual set removes one ingredient at a time and scores the same 444 items.

## §2: Population and the recorded rows

The counterfactual set, 444 store versions in 148 triples (`cf2/cf_cell.json`), the superseded-only ground-truth summary v2 of each (`cf2/cf_indexes.json`, key `v2`). Recorded rows read: `cf2/rows/rows_MINI.jsonl` (`INDEXED-V2`, k = 1; AUX-CF2-MINI-V2 0.7167) and `cf2/rows/rows_H45.jsonl` (`INDEXED-V2`, k = 5, X4 collapse; AUX-CF2-H45-V2 0.7566); blind is 0.5 by identity (ADDENDUM_R82 §6). Opus 5 is out of scope for cost.

## §3: The two renderings (pure functions of the recorded v2 text; committed before the run as `r82_counterfactual/tools/cf2_names_counts.py`; every output asserted)

- **NAMES-ONLY.** The v2 text with every count line removed: the `entries in this store` line; the whole `LIFECYCLE TOTALS` block; the whole `PER-CATEGORY BREAKDOWN` block (header, column header, every category row); the whole `AGE DISTRIBUTION` block; and the `(+N more)` overflow markers inside the name blocks. Kept byte-identical: the title line, the ages sentence, the `RECENCY` block (ages are not counts, the E1.8 rule), `ATTRIBUTE NAMES BY CATEGORY`, `ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT`. This line-removal form is the **primary** names-only arm (the author's ruling). **NAMES-DASH (secondary, GPT-4.1 mini only):** the committed E1.8 A3 rule (`e1_metamemory/tools/mechanism_arms.py`, `rewrite` with `a3`: every count replaced by `-`, structure kept), the rendering the paper already calls names-only on the pooled hard tier (0.8516, Table 28), applied unchanged to the v2 text; it prints beside the primary arm and carries no prediction.
- **COUNTS-ONLY.** The v2 text with the `ATTRIBUTE NAMES BY CATEGORY` block and the `ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT` block removed; everything else byte-identical (the category names of the count table stay, being the table's row labels).
- Identity to disclose at the freeze: on the 30 retraction and 30 expiry pairs the PN and PRESENT versions differ in v2 only in count cells (the superseded-names list names supersession only), so under NAMES-ONLY those two versions are byte-identical and every reader's PN-versus-PRESENT on the counted states is 0.5 by construction, as the name lookup's is; under COUNTS-ONLY the supersession pairs' PN and PRESENT versions differ only in the `SUPRSD` cell.
- Locks asserted per version before any call: NAMES-ONLY carries no digit outside the RECENCY block and the age sentence; NAMES-DASH reproduces `mechanism_arms`' own assertions (only counts moved, every count a dash, ages byte-identical); NAMES-DASH reproduces `mechanism_arms`' own assertions (only counts moved, every count a dash, ages byte-identical); COUNTS-ONLY carries no `ATTRIBUTE NAMES` header; every kept line is byte-identical to its v2 line. The leakage screen of ADDENDUM_CF2 §5 is not re-run: both renderings are subsets of the screened v2 text.

## §4: Lanes

Arms `INDEXED-NAMES` and `INDEXED-COUNTS`, 444 items each, for both readers; `INDEXED-NAMES-DASH`, 444 items, GPT-4.1 mini only. GPT-4.1 mini: k = 1, temperature 0, max_tokens 200, synchronous, list price (the CF-2 protocol). Haiku 4.5 (`claude-haiku-4-5-20251001`): k = 5, temperature 0, max_tokens 200, Message Batches, X4 collapse. Prompts `prompts_e1.SYSTEM` / `USER_INDEXED` verbatim, digests asserted at import. Served identifiers probed before each lane. Rows under `cf2/rows/rows_MINI_nc.jsonl`, `rows_H45_nc.jsonl`.

## §5: Estimands and predictions

Per reader and arm: AUROC on the whole set (PN versus the rest) and per state, persona-grouped interval printed first on this set (Section 4's rule), item-level beside; paired differences (arm minus the recorded v2 row; COUNTS-ONLY minus NAMES-ONLY) with both intervals (1,000 draws, seed 42, `cf2_score.paired`); the name lookup on the NAMES-ONLY list prints beside (its list is v2's, so it is the recorded 0.7663); PN-versus-PRESENT and W/T/L as for the other readers (the post-hoc definitions of `reviews/integration/POSTHOC_SPEC_R112.md`).

- **P-N1.** NAMES-ONLY is within tolerance of the recorded v2 row on the whole set, $|\Delta| \le 0.05$, for GPT-4.1 mini and for Haiku 4.5.
- **P-N2.** COUNTS-ONLY is below NAMES-ONLY on the whole set and the difference is reliable, both intervals excluding zero, for GPT-4.1 mini and for Haiku 4.5.
- **P-N3 (descriptive, no bar).** Per state, COUNTS-ONLY on retraction and on expiry against the reader's recorded v2 row on that state (AUX-CF2-PERSTATE: GPT-4.1 mini 0.5283 / 0.5489; Haiku 4.5 0.5433 / 0.5794): the difference and both intervals print, read against the 0.05 band.

Failure texts, frozen: "P-N1 FAILS on [model]: the names-only summary moves the whole-set AUROC by $\Delta$ from the intact summary, outside tolerance." / "P-N2 FAILS on [model]: counts only is not reliably below names only ($\Delta$, $I_{item}$, $I_{persona}$)."

## §6: Held texts, both branches (Phase 3, by ruling)

- Both hold: one Section 5 sentence after the own-name ablation: "Removing every count from the summary leaves both readers within tolerance of the intact summary, and removing the names instead lowers both reliably (Appendix C.2)." The appendix table in C.2 (`tab:cf-names-counts`): per reader the four rows intact / names only / counts only / blind with whole-set and per-state AUROC and the two paired differences.
- P-N1 fails on a model: the sentence names the model whose names-only row moved and the direction; P-N2 fails: the sentence says counts only was not reliably below names only for that model, with the number. The table prints in every branch.

## §7: Budget, order, STOP

Projected from the recorded CF-2 rows and the offline token count of the renderings (o200k_base plus the constant 11-token template offset; NAMES-ONLY 1,181 tokens mean, COUNTS-ONLY 1,009, NAMES-DASH about 1,616, against v2's 1,616): GPT-4.1 mini 1,332 calls **$0.74**; Haiku 4.5 4,440 Batch calls (input scaled by the recorded Anthropic/OpenAI token ratio 1.06, output 183 tokens as recorded) **$4.61**; probes $0.02; **$5.37 against the $10 cap (×1.3: $7.0)**. Order: renderer (no call) → locks → probes → mini → Haiku 4.5. STOP: registration sha256 mismatch; a lock failure; served-identifier mismatch; more than 2% of a lane's rows not OK after the retry; a projection over the cap.

## §8: Ledger and paper site

`cf2/NUMBERS_CF2.md` section 12: `AUX-CF2-NC-LOCK`, `-NC-TOKENS`, `-NC-MINI-NAMES`, `-NC-MINI-NAMES-DASH`, `-NC-MINI-COUNTS`, `-NC-H45-NAMES`, `-NC-H45-COUNTS`, `-NC-PERSTATE`, `-NC-P-N1`, `-NC-P-N2`, `-NC-P-N3`, `-NC-SPEND`. Paper: one sentence in Section 5, `tab:cf-names-counts` in Appendix C.2.

## Registration mechanics

Frozen by sha256 before the first call. Copied to `iclr2027_monitoring_submission/ARTIFACT/registrations/`. Amendments, if any, are appended as dated sections below the marker line and never edit the text above. The run proceeds on the author's freeze commit; nothing runs before it exists.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
