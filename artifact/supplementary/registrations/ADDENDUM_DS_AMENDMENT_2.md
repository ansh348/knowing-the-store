# ADDENDUM_DS — Amendment 2: the answer stage of the literal-threshold lookup rule (LOOKUP-LIT), and a second answerer

Written 2026-09-14 (program R106, the pass on v13 from the eighth review), BEFORE any call, as a
separate file because `verify_ds.py` check A pins `registrations/ADDENDUM_DS.md` byte-identical to
`a5a2036`. **Descriptive: no bar, no prediction, no verdict; DS-P1 to DS-P5 are never
re-adjudicated.** The author's instruction of 2026-09-14: "add the literal-threshold lookup
(LOOKUP-LIT) row to Table 5 with fires / reach / mean view / coverage; run its answer stage (GPT-4.1
mini, one call per distinct view, temperature 0) after registering a descriptive addendum; Section 10's
deployment rule becomes fetch-on-match without coverage abstention, with the gated rules as the
registered comparison; add the tagged-versus-untagged stale rates under retrieval alone (2 of 35
against 7 of 19); second registered lane if under $5: Haiku 4.5 as answerer on the same views."
Every number prints whichever way it comes out. Frozen by sha256 before the first call (CLAIMS.md
R106 block; `ds_downstream/NUMBERS_DS.md` section 7).

## §A2.1 — What is added, and what is not

ADDENDUM_DS §C.5 defines the literal rule, `LOOKUP-LIT`: fetch the lifecycle records of the
superseded names (the N2 fetch set, as MODEL and LOOKUP) whenever the superseded-names lookup's cosine
on the question is at or above the base rate θ_NOK = 104 / 661 = 0.157337, and abstain on coverage
whenever the whole-map cosine is below θ_FOK = 35 / 307 = 0.114007, which no item is, so the rule
never abstains. §C.5 (ruling R2) made the matched-budget LOOKUP the registered reading and left
`LOOKUP-LIT` a descriptive Stage 1 row with no Stage 2. Stage 1 for it is already computed and
ledgered (`AUX-DS-POLICIES`, `-REACH`, `-PRESENT`, `-ABSTAIN`, `-VIEWSIZE`: fires 184 of 661, no
abstention, forbidding record in view for 94 of the 104 obligations, 75 of them printed non-active,
mean view 6.02 over the 661 and 7.42 over the 104, coverage 65 of 174 as under retrieval alone) and
its views are assembled in `ds_downstream/views.json` under the same rule as every other policy's
(the five L2 lines byte-identical, then the fetched non-active records in ascending (slot, entry id)
order, ranks continuing).

This amendment adds two things and changes nothing registered:

1. **Stage 2 for `LOOKUP-LIT`** under the protocol of §D.4, so that its stale-use and correctness
   counts print beside the six registered policies' in Table 5 (`tab:ds-body`) and `tab:ds`.
2. **A second answerer, Claude Haiku 4.5**, on every distinct (item, view) pair of Stage 2 across
   the seven policies, so that each policy's stale-use and correctness counts are read by two
   answerers from one vendor each.

The six registered policies, their views, their Stage 1 and Stage 2 rows, the five verdicts, the
frozen Section 7 paragraph and Amendment 1's rows stand as printed. No monitor is elicited, no
summary is rendered, no lookup is re-scored, no embedding call is made.

## §A2.2 — Population (deterministic, from the committed Stage 1; $0)

The Stage 2 population rule of §D.4, applied to `LOOKUP-LIT` exactly as `run_ds.build_cell` applies
it to the registered policies: PRESENT-NEGATIVE items whose view holds the forbidding record
(`stage1.json` reach, 94 of 104) and PRESENT items not abstained (174 of 174; the rule never
abstains); no ABSENT item. That is **268 nominal (item, view) pairs**. The cache key is the item id
plus the view's sha256, as in `run_ds.py`: a `LOOKUP-LIT` view byte-identical to a view already
answered under a registered policy reuses the recorded answer from `ds_downstream/run/rows_ds.jsonl`
and makes no call. Computed before this file was frozen: **238 pairs reuse a recorded answer and 30
are new calls (6 PRESENT-NEGATIVE, 24 PRESENT)**; the runner recomputes both counts and prints them
before launch, and a mismatch is a STOP.

## §A2.3 — Lane 1: GPT-4.1 mini, the §D.4 protocol

`gpt-4.1-mini` pinned (`prompts_e1.MODEL`), `prompts_ds.SYSTEM_ANSWER` and `USER_ANSWER` verbatim
(digests `af1c69c8…` / `c6dd6926…` as `AUX-DS-PROMPT`, asserted against the frozen §D.4 at import),
temperature 0, seed 42, max_tokens 200, JSON mode, k = 1, one retry on a parse failure (the E1
clamp), through `run_ds.answer`; the cache redirected to `ds_downstream/cache_amend2/` and seeded
read-only from the DS cache, as Amendment 1 did. Served identifier probed before launch (one call;
E1.7 rule). Rows in `ds_downstream/run/rows_ds_amend2.jsonl`: every one of the 268 pairs, the 238
reused rows copied with `source = ds_downstream/run/rows_ds.jsonl` and `usd = 0`, the 30 new ones
with `source = amend2 call`.

## §A2.4 — Lane 2: Claude Haiku 4.5 as the answerer

`claude-haiku-4-5-20251001` (the Haiku 4.5 identifier every other lane of this program uses),
**temperature 0, max_tokens 200, k = 1**, the same two texts: `SYSTEM_ANSWER` as the system prompt
and `USER_ANSWER` formatted with the view and the question as the one user message, through the
Anthropic Messages API synchronously (no Batch; the lane is small). Anthropic offers no JSON mode,
so the answer is read from the last JSON object in the reply (`run_cf.last_json`'s rule, the one
the Haiku monitor lanes use), with one retry on a parse failure; a reply with no parseable
`{"answer": ...}` after the retry is `ELICITATION_FAILED` and is reported, never scored. Served
identifier probed before launch (three calls on three recorded views, a PRESENT-NEGATIVE, a PRESENT and
the longest; E1.7 rule). **Population: every distinct (item, view) pair of Stage 2 across the seven
policies** — the 422 recorded pairs of `rows_ds.jsonl` plus the 30 new `LOOKUP-LIT` pairs, 452 in all
(the runner recomputes the count) — so that Haiku's counts are comparable across policies. Rows in
`ds_downstream/run/rows_ds_amend2_h45.jsonl`, keyed as Lane 1.

## §A2.5 — What is computed ($0 after the calls, deterministic)

- **Stage 2 for `LOOKUP-LIT`, Lane 1**, scored by the committed detector exactly as
  `run_ds.score_answer` (`AUX-DS-STAGE2`'s columns): PN reached and answered, PN abstained (0), stale
  use at TAU_HI and at TAU_GOLD, each split by tagged / untagged reach, stale surfacing, successor
  use, both, per-state stale use, PRESENT answered and correct at TAU_GOLD and TAU_HI.
- **Stage 2 under Haiku 4.5, Lane 2**, the same columns for each of the seven policies, from the Haiku
  rows keyed by (item, view); the mini row of each policy is reprinted beside it from the recorded
  scores so the two answerers can be read side by side. Nothing recorded is re-scored.
- **The ALWAYS tagged / untagged split at TAU_GOLD** the paper will print (2 of 35 against 7 of 19
  under mini; `AUX-DS-STAGE2`) is a recorded value; this amendment reads it and adds Haiku's beside it.
- **Spend**: Lane 1 from response usage at $0.40 / $1.60 per 1M; Lane 2 at $1.00 / $5.00 per 1M
  (list, synchronous), each recorded per row and summed.

## §A2.6 — Budget and STOP

Lane 1 is projected from the DS probe's token figure per line (`run/probes_ds.json`, as Amendment 1's
`stage2-project`) over the 30 new views; it runs under the DS $4 rule, against which $0.1093 (DS)
and Amendment 1's Stage 2 spend are already billed. Lane 2 is projected from its own probe's token
counts over the 452 views; **it runs only if that projection times 1.3 is under the author's $5.00
line**, and the client's hard cap for the lane is set to $5.00. STOP conditions: served-identifier
mismatch on either lane; the population counts of §A2.2 or §A2.4 not reproducing; failures after
the retry on more than 2% of a lane's calls; a projection over its line.

## §A2.7 — Ledger and paper sites

`ds_downstream/NUMBERS_DS.md` gains section 7 with keys `AUX-DS-A2-LOCK`, `-POP`, `-PROBE-MINI`,
`-PROBE-H45`, `-PROJECTION`, `-STAGE2-LIT` (Lane 1), `-STAGE2-H45` (Lane 2, all seven policies),
`-SPEND`. Paper (program R106): one row in Table 5 (`tab:ds-body`) for the literal rule with its
fires, reach, mean view, tagged reach, coverage, stale use and correctness, and a coverage column for
every row (`AUX-DS-PRESENT`; the matched-budget retrieval rows of `AUX-R104-REACH` carry a dash,
since coverage under them was not scored); the tagged / untagged stale rates under retrieval alone in
Section 8; Section 10's deployment rule stated as fetch-on-match without coverage abstention, with
the gated rules as the registered comparison; the account and the Haiku table in Appendix F.10.
`verify_ds.py` is unaffected (it checks the registered artifacts and does not read the amendment's
files).

## Registration mechanics

Frozen by sha256 before the first call (recorded in CLAIMS.md R106 and NUMBERS_DS.md section 7).
Copied to `iclr2027_monitoring_submission/ARTIFACT/registrations/ADDENDUM_DS_AMENDMENT_2.md`.
Further amendments append dated sections and never edit the text above.
