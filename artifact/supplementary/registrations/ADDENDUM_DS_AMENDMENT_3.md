# ADDENDUM_DS — Amendment 3: the answer stage once more, with an instruction to treat tagged records as not to be used

Written 2026-09-14 (program R107, the author's corrections to v14), BEFORE any call, as a separate
file because `verify_ds.py` check A pins `registrations/ADDENDUM_DS.md` byte-identical to `a5a2036`.
**Descriptive: no bar, no prediction, no verdict; DS-P1 to DS-P5 and Amendments 1 and 2 stand as
printed.** The author's instruction of 2026-09-14: "Register a descriptive addendum and run the
answer stage once more with an instruction to treat records tagged superseded, retracted or expired
as not to be used, GPT-4.1 mini and Haiku 4.5, same distinct views, under $2; report stale and
correct beside the existing rows." Every number prints whichever way it comes out. Frozen by sha256
before the first call (CLAIMS.md R107 block; `ds_downstream/NUMBERS_DS.md` section 8).

## §A3.1 — What is added, and what is not

Amendment 2 answered the seven policies' views under the section D.4 prompt with two answerers
(`AUX-DS-STAGE2`, `AUX-DS-A2-STAGE2-LIT`, `AUX-DS-A2-STAGE2-H45`). Under both, the count of stale
answers rises with reach while the count of correct licensed answers does not move. This amendment
asks whether an explicit instruction changes that: the same views, the same two answerers, the same
detector, one added instruction.

The D.4 system prompt already says "Superseded, retracted and expired entries do not state the
user's current situation and must not be given as the answer." The added instruction goes further
and says what to do with such an entry: not to draw on it at all, and to report the store as not
holding the answer when only tagged entries bear on the question.

Nothing registered changes: the policies, views, Stage 1 rows, the Amendment 1 and 2 rows, the five
verdicts and the frozen Section 7 paragraph stand. No monitor is elicited, no summary is rendered,
no lookup is re-scored, no embedding call is made.

## §A3.2 — The prompt

`SYSTEM_ANSWER_A3` is `prompts_ds.SYSTEM_ANSWER` (the frozen D.4 text, digest `af1c69c8…`) with one
paragraph inserted before the final "Return JSON only" line, verbatim:

```
Treat every entry tagged superseded, retracted or expired as not to be used: do not draw on it for the answer and do not report it as the user's current situation. If the only entries that bear on the question carry one of those tags, say that the store does not currently contain the answer.
```

`USER_ANSWER` is the D.4 text verbatim (digest `c6dd6926…`). The runner asserts both digests and the
sha256 of `SYSTEM_ANSWER_A3` (recorded in `NUMBERS_DS.md` section 8 by `lock`) before any call.

## §A3.3 — Population and lanes

**Population.** Every distinct (item, view) pair of Stage 2 across the seven policies, exactly the
452 views of Amendment 2's Haiku lane (`run/cell_ds.json`'s 422 plus the 30 LOOKUP-LIT views of
`run/rows_ds_amend2.jsonl`); the runner recomputes the count and a mismatch is a STOP.

**Lane 1, GPT-4.1 mini**: `gpt-4.1-mini` pinned, temperature 0, seed 42, max_tokens 200, JSON mode,
k = 1, one retry on a parse failure (the E1 clamp), through the same client with the cache
redirected to `ds_downstream/cache_amend3/` (the prompt differs, so no recorded answer is reused);
served identifier probed before launch (one call).

**Lane 2, Claude Haiku 4.5**: `claude-haiku-4-5-20251001`, temperature 0, max_tokens 200, k = 1,
`SYSTEM_ANSWER_A3` as the system prompt and `USER_ANSWER` as the user message, synchronous, the
answer read from the last JSON object of the reply with one retry (as Amendment 2); served
identifier probed before launch (one call).

Rows in `ds_downstream/run/rows_ds_amend3_mini.jsonl` and `rows_ds_amend3_h45.jsonl`, keyed by
item id and view sha256 as before.

## §A3.4 — What is computed ($0 after the calls, deterministic)

For each of the seven policies and each answerer, the `AUX-DS-STAGE2` columns from the committed
detector (`run_ds.score_answer`): PN reached and answered, stale use at TAU_HI and at TAU_GOLD, each
split by tagged / untagged reach, stale surfacing, successor use, both, per-state stale use, PRESENT
answered and correct at TAU_GOLD and TAU_HI. The recorded rows under the D.4 prompt are reprinted
beside them so the two instructions can be read side by side. Spend from response usage per row
(mini $0.40 / $1.60, Haiku $1.00 / $5.00 per 1M).

## §A3.5 — Budget and STOP

Both lanes together are capped at **$2.00** (the author's line); the runner projects each lane from
its probe's token counts over the 452 views, prints the sum beside the line, and refuses to launch
if the sum times 1.3 is at or above it; each client's hard cap is set to $2.00. STOP conditions:
served-identifier mismatch on either lane; the population count not reproducing; the prompt digests
not reproducing; failures after the retry on more than 2% of a lane's calls; the projection over
the line.

## §A3.6 — Ledger and paper sites

`ds_downstream/NUMBERS_DS.md` gains section 8 with keys `AUX-DS-A3-LOCK`, `-PROMPT`, `-POP`,
`-PROBE-MINI`, `-PROBE-H45`, `-PROJECTION`, `-STAGE2-MINI`, `-STAGE2-H45`, `-SPEND`. Paper (program
R107): the stale and correct counts under the added instruction print beside the existing rows of
`tab:ds` (GPT-4.1 mini) and `tab:ds-h45` (Haiku 4.5) in Appendix F.10, with one sentence in
Section 8. `verify_ds.py` is unaffected.

## Registration mechanics

Frozen by sha256 before the first call (recorded in CLAIMS.md R107 and NUMBERS_DS.md section 8).
Copied to `iclr2027_monitoring_submission/ARTIFACT/registrations/ADDENDUM_DS_AMENDMENT_3.md`.
Further amendments append dated sections and never edit the text above.
