# ADDENDUM_PARA — descriptive probe on the portability of the counterfactual result: the 148 questions paraphrased away from every name the summary prints

Written 2026-09-13 (program R104, the v11-to-v12 pass), BEFORE any call. Descriptive: this
addendum carries **no prediction, no bar and no verdict**; the branches of §7 are enumerated in
advance and every number prints whichever way it comes out, in Appendix D.2 beside the
counterfactual table and in one sentence of Section 5 (the portability paragraph). It is frozen by
its sha256, recorded in `iclr2027_monitoring_submission/CLAIMS.md` (R104 block) and in
`cf2_paraphrase/NUMBERS_PARA.md` before the first call. Nothing here re-adjudicates CF-2's five
predictions, the R81 or SIDE items, or any registered verdict; the CF-2 rows are read and never
re-run.

## §1 — Question

On the counterfactual set the superseded-names lookup reads the superseded state at 0.92 and the
whole set at 0.77 (`AUX-CF2-NB6-V2`), and 89 of the 148 questions name the plan or value their
attribute is about (`AUX-CF2-QUESTIONREAD`, `AUX-R103-FLAGSPLIT`). A reviewer asked how far the
lookup's score rides on the wording of the question. The probe asks each of the 148 questions
again in a wording that shares **no content token** with the attribute's slot path or with any
attribute name the summary prints, and scores the same readers on the same three store versions
under the same two summaries. What a lookup can still match is then whatever similarity survives
the removal of every shared token; what a model can still read is the question's meaning.

## §2 — Population

The **148 questions** of the CF-2 cell (`r82_counterfactual/cf2/cf_questions_cf2.json`, questions
sha256 as ledgered in `AUX-CF2-CONSTRUCTION`), each with its pair (`pair_id`, persona, display
name, slot path `slot`, intent, state) and its **three store versions** (`cf2/cf_cell.json`,
n = 444, 148 PN = 88 supersession / 30 retraction / 30 expiry) with their committed **v2**
(superseded-only) and **v3** (all-states) summaries (`cf2/cf_indexes.json`, sha256 as ledgered).
Store versions, summaries and labels are unchanged; only the question text changes. The recorded
rows this probe is paired against, read and never re-run: `cf2/rows/rows_MINI.jsonl`,
`rows_H45.jsonl`, `rows_OP5.jsonl` (X4 collapse through `score_cf.load_lane`) and the two lookups
recomputed on the original questions as the gate (`AUX-CF2-NB6-V2` 0.7663, `AUX-CF2-ALLSTATES-V3`
0.8756 at four decimals, or STOP).

## §3 — The forbidden set and the screen (deterministic)

For each pair, **F(pair)** is the union of the content tokens of (a) the slot path, split on `:`
and `_`, and (b) every attribute name printed in the **v3 summaries of the pair's three versions**
— the per-category name map (`index_features.parse` `attr_by_cat`, all buckets, `(+N more)`
overflow excluded because it is not printed) and the three state sections (`index_v3.named_sections`),
underscores replaced by spaces — tokenized by `index_features.toks` (lowercase, split on
non-alphanumerics, the module's stopword list, tokens of one character dropped) and closed under
`index_features._sing` (singular forms). The v3 text contains the v2 text as its prefix, so v3 alone
covers both summaries.

**Screen.** A candidate paraphrase passes when `{_sing(t) for t in toks(candidate)} ∩ F(pair) = ∅`
and the candidate differs from the original question after case-folding. The screen is a pure
function of the two strings and the committed summaries; it is re-run at scoring time on every
accepted paraphrase and any overlap then is a STOP.

## §4 — Drafting (gpt-4.1-mini, construction only)

**Prompt, frozen here** (sha256 over SYSTEM ⊕ USER ⊕ model ⊕ temperature ⊕ max_tokens ⊕ N, recorded
in `AUX-PARA-DRAFT` at the first call and asserted before every later one):

SYSTEM:
```
You rewrite questions a person might ask their own AI assistant about themselves.

You are given the person's name, one question they asked, the time-sense the question carries,
and a list of forbidden words. Write three different questions that ask for exactly the same
thing as the given question, for that person, without using any forbidden word or any singular,
plural or hyphenated form of a forbidden word.

Rules.
Ask for the same specific detail the given question asks for; do not broaden or narrow it.
Write the question the way that person would actually type it to an assistant.
Do not invent or state any value or fact. You do not know what the assistant remembers.
Do not mention memory, stores, records, metadata, or the assistant's knowledge.
Each of the three must be a genuinely different wording, not a light edit of another.
Never use a forbidden word, even as part of a longer word.

Time-sense.
CURRENT-STATE: ask about how things stand now, in the present tense. Do not use words like
upcoming, coming up, scheduled, planning, plans to, going to, will, next, or future, and do not
ask about the past.
UPCOMING: ask about something ahead of the person. Use a forward-looking word such as upcoming,
coming up, scheduled, planning, or next. Do not ask about the past and do not use past-tense
phrasing such as did, was, already, used to, or finished.

Respond with a single JSON object and nothing else:
{"questions": ["...", "...", "..."]}
```

USER:
```
Person: {entity}
Question: {question}
Time-sense: {intent}
Forbidden words: {forbidden}
```

`{forbidden}` is F(pair) sorted, space-separated. Model `gpt-4.1-mini` pinned, temperature 0,
max_tokens 400, three candidates per draft, seed 42; on failure a second draft at seed 4242 and a
third at seed 424242, each with the tokens that failed the screen appended to the forbidden list.
**Selection**, per draft: the start index is `random.Random(f"42:{pair_id}")`'s choice of three (the
CF-1 rule), then in order the first candidate that passes (1) the §3 screen and (2) the CF-1 intent
gate (`draft_questions.intent_ok`: UPCOMING must type UPCOMING; CURRENT-STATE must return no
marker). A pair with no passing candidate after three drafts is **excluded** from the paraphrase
set, listed with its nine candidates and the token each failed on; the set's size prints. If fewer
than **120** of 148 pairs pass, the draft STOPs for the author's ruling before any sheet is written.
Every draft, candidate, screen result and intent-gate trail is recorded in
`cf2_paraphrase/para_questions.json`.

## §5 — The author's read (before any scoring call)

Every accepted paraphrase is written to `reviews/v12/PARAPHRASE_SHEET.md`, one row per pair:
`pair_id | state | intent | original question | paraphrase | asks the same thing under the same
intent? (YES / NO) | names the value or plan? (YES / NO)`. The author fills the two verdict columns.
A **NO** on the first column excludes the pair (no re-draft); a YES transfers the pair's labels: the
three versions keep `y_nok`, `y_fok` and `state` because the store versions are unchanged and the
intent gate held, which is the same label logic CF-2 used for its own three paraphrases. The second
column is a disclosure only, so the attribute-naming split of Appendix H.2 can be recomputed on the
paraphrase set (`AUX-PARA-FLAGS`); it excludes nothing. The returned sheet's sha256 is ledgered
(`AUX-PARA-SHEET`) and no scoring call is made before it is.

## §6 — Readers, protocol, estimands (descriptive)

**Items.** The accepted pairs × their three store versions (n = 3 × accepted). **Arms:** INDEXED-V2
and INDEXED-V3 with the committed summaries of `cf2/cf_indexes.json`; no BLIND arm, because the
paraphrase is one string per pair asked of all three versions, so blind AUROC is 0.5 by the CF-2
identity and every reader's AUROC is also its gain.

**Lookups ($0), four rows:** the embedding lookup (`score_cf.matcher`, `sentence-transformers/all-MiniLM-L6-v2`,
max cosine) and the lexical lookup (`run_nb6.lex_scores`' Jaccard over content tokens) on the
superseded section of v2 and on the three sections of v3 (`index_v3.named_sections`), exactly as
`cf2_score.py` builds the name lists.

**Models.** `prompts_e1.SYSTEM` / `USER_INDEXED` verbatim (digests asserted at import), the paraphrase
as the question. `gpt-4.1-mini` k = 1, temperature 0, seed 42, max_tokens 200 (the CF-2 mini lane,
synchronous, list price). Haiku 4.5 (`claude-haiku-4-5-20251001`) k = 5, temperature 0, max_tokens
200, Batch (the CF-2 Haiku lane; X4 collapse, MIN_DRAWS 3, arithmetic mean). Opus 5
(`claude-opus-5`) **k = 1**, temperature unset, max_tokens 1024, Batch: one call by the author's
instruction, against k = 5 on the recorded CF-2 rows, so its paired row carries a draw-count
difference that is disclosed beside it and is not a registered comparison. Served identifiers
probed before each lane (E1.7 rule). Rows under `cf2_paraphrase/rows/`.

**Estimands, per reader × summary:**
- AUROC on the paraphrase set, whole and per state (88 / 30 / 30 positives, or the accepted
  subset's counts), Mann-Whitney with ties at 0.5;
- the **paired difference paraphrase − original** on the same items (the original's recorded score
  from the CF-2 rows; for a lookup its deterministic score on the original question), item-level
  paired bootstrap (1,000 draws, seed 42, single-class draws discarded) and persona-clustered
  paired bootstrap, both printed; where they disagree the weaker reading is stated;
- the model-minus-lookup difference on the paraphrase set under the same summary, with both
  intervals (the `AUX-R103-MARGIN` construction), for the embedding lookup and the lexical lookup;
- the screen census: tokens per paraphrase, the size of F(pair), and how many paraphrases share a
  token with the **value** the author flagged (`question_read_flags.json`, disclosure only).

## §7 — Branches (enumerated in advance; no pass bar; every one prints as it comes out)

Read on the whole paraphrase set with tolerance ±0.05 on the point estimate. A reader **holds**
when its paired difference paraphrase − original lies inside ±0.05; it **collapses** when the
difference is below −0.05 with both intervals excluding zero. Per summary (v2 with its superseded
section; v3 with its three sections):

- **A.** The lexical lookup collapses and the embedding lookup holds.
- **B.** Both lookups hold.
- **C.** Both lookups collapse.
- **D.** A model holds where a lookup collapses: for each model, the lookups that collapse while
  that model holds are named.

A difference beyond tolerance whose intervals include zero, a rise beyond tolerance, or a reader
that neither holds nor collapses prints as described under the heading it falls nearest, with the
numbers. The per-state rows are descriptive and print beside; no branch reads them. Under branch D
the sentence in Section 5 names the model and the lookup; under A, B or C it states the two lookups'
differences and the models' differences in one sentence each.

## §8 — Budget, lane order and STOP

The two new jobs of this pass (`ADDENDUM_PAD`, this addendum) share a combined **$15** cap set by
the author. From the CF-2 rows' recorded token means (`AUX-CF2-SPEND`; 444 items × two summaries):

| lane | calls | projected | ×1.3 | line |
|---|---:|---:|---:|---|
| drafting, `gpt-4.1-mini` (≈ 2 drafts per pair) | ≈ 300 | $0.12 | $0.16 | OpenAI $3 (shared with the mini lane and `ADDENDUM_PAD`) |
| `gpt-4.1-mini`, k = 1, list | 888 | $0.62 | $0.80 | OpenAI $3 |
| Haiku 4.5, k = 5, Batch | 4,440 | $5.88 | $7.64 | Anthropic $8 |
| Opus 5, k = 1, Batch | 888 | $8.06 | $10.48 | Anthropic $11, **conditional** |
| `ADDENDUM_PAD` (runs first) | 1,983 | $1.46 | $1.90 | OpenAI $2.50 |
| **combined, all lanes** | | **$16.14** | **$20.98** | **$15 cap: over** |
| combined without Opus 5 | | $8.08 | $10.50 | under |

**Lane order and the headroom rule.** Lanes run in this order: `ADDENDUM_PAD`; drafting; the
author's read; `gpt-4.1-mini`; Haiku 4.5; Opus 5. Before each lane the runner projects it from its
own three-call probe and prints the projection beside the combined headroom (the cap less every
lane already billed and every earlier lane's projection). **A lane whose ×1.3 projection exceeds the
remaining headroom is not submitted and prints a dash with the reason.** At the $15 cap that rule
drops Opus 5 (the combined ×1.3 projection is $20.98). **The author's ruling at the freeze decides
Opus 5:** (i) keep the $15 cap, so Opus 5 prints a dash and the paraphrase result rests on the two
lookups, GPT-4.1 mini and Haiku 4.5; or (ii) raise the combined cap to **$21**, so every lane runs.
The ruling is written into this file as a dated line under Registration mechanics before the first
call, and the Opus line is submitted only under (ii). No lane is ever re-run to fit a cap.

STOP: registration sha256 mismatch; prompts_e1 digests or the CF-2 questions and indexes sha256
differing from the ledgered values; served-identifier mismatch on any lane; the lookup gate on the
original questions failing at four decimals; any accepted paraphrase failing the screen at scoring
time; fewer than 120 pairs accepted after drafting or after the author's read; any scoring call
before `AUX-PARA-SHEET` is ledgered; elicitation failures after the retry on more than 2% of a
lane's rows; a lane submitted before its probe and projection; projection over the headroom.

## §9 — Ledger and paper site

`cf2_paraphrase/NUMBERS_PARA.md` carries `AUX-PARA-DRAFT` (prompt sha256, drafts, candidates,
screen and gate counts, exclusions with reasons, the paraphrase set's sha256), `AUX-PARA-SHEET`
(the author's verdicts, sha256, accepted count), `AUX-PARA-LOCK` (screen re-run at scoring, index
and question sha256 checks, lookup gate), `AUX-PARA-PROBE-*` and `AUX-PARA-PROJECTION-*` per lane,
`AUX-PARA-LOOKUP-EMB-V2`, `-LOOKUP-LEX-V2`, `-LOOKUP-EMB-V3`, `-LOOKUP-LEX-V3`, `-MINI-V2`,
`-MINI-V3`, `-H45-V2`, `-H45-V3`, `-OP5-V2`, `-OP5-V3` (each: AUROC whole and per state, the paired
difference with both intervals, the model-minus-lookup rows), `AUX-PARA-FLAGS`, `AUX-PARA-BRANCH`,
`AUX-PARA-SPEND`; a lane not run carries a dash and its reason. Paper: one table in Appendix D.2
(whole-set and per-state AUROC on the paraphrase set beside the original for every reader, with the
paired intervals) and one sentence of Section 5, two-decimal forms in the body. No frozen number
changes; no frozen text changes.

## Registration mechanics

Frozen by sha256 before the first call (recorded in CLAIMS.md R104 and NUMBERS_PARA.md). Copied to
`iclr2027_monitoring_submission/ARTIFACT/registrations/ADDENDUM_PARA.md`. Amendments, if any, are
appended as dated sections and never edit the text above. The author's freeze is the author's
commit of this file, or the author's written GO quoting its sha256, together with the Opus 5 ruling
of §8 written as a dated line here.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->

## Author's rulings (dated; appended after the freeze)

**2026-09-14 — the §8 Opus 5 ruling, recorded from the author's instruction of that date.** The
author's words: "Run them now, in this order, under the $15 cap" and, for the paraphrase lanes,
"score both lookups, then mini once, Haiku 4.5 five calls, Opus 5 once, under both summaries, paired
against the originals." Recorded as ruling **(i): the combined cap stays at $15.** The Opus 5 lane is
the last lane of the order (§8, as extended by `ADDENDUM_PAD` Amendment 1) and is submitted only if its
×1.3 projection fits the headroom remaining at its turn; at the registered projections it does not
(combined ×1.3 projection $20.98 against $15), so under this ruling it prints a dash with that reason.
The author may raise the combined cap to $21 (ruling ii) in the morning GO, before that lane is
reached; a raise is appended here as a further dated line and affects no other lane. Every earlier
lane runs unchanged under either ruling.

**2026-09-14 — the §5 sheet's name.** The author's instruction names the sheet `PARAPHRASE_READ.md`;
it is written as `reviews/v12/PARAPHRASE_READ.md` with the columns of §5 unchanged.

**2026-09-14 (evening) — the author's ruling on the §4 STOP of the drafting lane, and the cap rulings.** The
author reviewed freeze `dab8956` and adopted it as the author's registration. Trigger, stated as it was: the
drafting lane ran as registered (prompt sha256 `b1cf08a2…`, 289 calls, $0.08) and accepted **87 of 148** pairs,
below the 120 floor of §4, so no sheet was written and nothing was scored; 533 of the excluded pairs' 549
candidates failed the §3 screen, and 48 of the 61 exclusions were blocked by a content token of the slot path's
**value part** (after the first `:`) — a token no summary prints, because the summaries print the scrubbed name
only (`cf2_paraphrase/DRAFT_STOP.md`). **Ruling: option (2).** The 87 accepted paraphrases stand as drafted.
**§3(a) is narrowed to the content tokens of the scrubbed slot name** (the part before the first `:`, split on
`_`), for the redraft of the 61 excluded pairs and for the scoring-time re-run of the screen on the whole set (the
87 pass the narrowed screen a fortiori); **§3(b) — every attribute name printed in the pair's three v3
summaries — is unchanged**, and so are the drafter (`gpt-4.1-mini`, the frozen prompt of §4 at sha256
`b1cf08a2…`, temperature 0, max_tokens 400, three candidates), the seeds 42 / 4242 / 424242, the selection rule
and the CF-1 intent gate. Only the 61 excluded pairs are redrafted; the 120 floor still applies to the resulting
set. **Value-naming is not a redraft criterion**: it becomes a tracked disclosure — the sheet's second column
and `AUX-PARA-FLAGS` — reported as a flagged-versus-unflagged split for every reader under both summaries,
exactly as the attribute-naming split of the original questions was reported (`AUX-R103-FLAGSPLIT`), so the
paper can say whether the paraphrase result depends on the question naming the value. Why (2) and not a
stronger drafter: swapping the drafter after seeing the outputs is a protocol change mid-lane; the
experiment's value is that its protocol was fixed before the questions existed. Why not the 87 alone: a known
confound in the load-bearing experiment. **Cap rulings:** the §8 Opus 5 ruling is **(ii) — the combined cap is
raised to $21 and Opus 5 runs, once (k = 1)**, superseding the (i) line above; the `ADDENDUM_PAD` Amendment 1
Haiku 4.5 lane (k = 5) runs **regardless of the ×1.3 headroom rule**, under an **overall cap of $28** for
everything in this pass; registered lanes are never displaced.

## Dated note, 21 Sep 2026 (before the author's read; no scoring call made)
The author's read of section 5 is carried out with an AI assistant (Claude,
Anthropic). The assistant reads the exported sheet
reviews/para/PARA_APPROVAL_SHEET.csv (sha256 f309bb54...) and flags rows for
the author's attention with a one-line reason. It sees no reader output and
no score. The author reads every row, and every verdict in both columns is
decided and entered by the author. The flags are kept at
reviews/para/PARA_AI_FLAGS.md and released with the artifact. Rows are
decided on their merits before the accepted count is computed; if fewer than
120 pairs are accepted, the section 8 STOP applies and no verdict is
revisited.

"21 Sep 2026, same read: for rows the assistant flagged, the repository's
coding session printed persona evidence (manifest events and source
snippets) for the author. It gave no verdict and ran no reader. The
evidence file is reviews/para/PARA_PERSONA_EVIDENCE.md, released with the
artifact."

"21 Sep 2026, same read: after the persona evidence the assistant wrote a
second file, reviews/para/PARA_AI_FLAGS_ADDENDUM.md (sha256 254ded08...),
revising its view of nine rows and stating the rule it applied (wrong
referent against vaguer wording of the same referent). The session wrote
reviews/para/PARA_COL2_TOKEN_CHECK.md (sha256 4172918f...), a token check
for the second column using the registered tokenizer, as an aid only. Both
are released with the artifact. No verdict in either file is the author's;
the author's verdicts are only those in reviews/v12/PARAPHRASE_READ.md."

"21 Sep 2026, amendment before any scoring call. The author's read
excluded 9 of the 124 screen-passing pairs (rows 11, 28, 30, 40, 46, 68,
77, 79, 82), leaving 115, below the registered floor of 120. No verdict
was revisited. The floor is amended to the 115 accepted pairs; the
registered predictions, readers, prompts, draws and budget are unchanged.
Because excluding paraphrases judged unfaithful could favour a reader
that matches on meaning, one sensitivity analysis is added and labelled
as not registered: the same scoring on all 124 screen-passing pairs,
reported beside the 115. The second column was filled to Appendix H.2's
sentence (62 YES); the token operationalization of the earlier read gives
33. The AUX-PARA-FLAGS split is reported both ways."

"21 Sep 2026, added readers, not registered. Declared after the lookup
result on the paraphrase set and before any model result was seen. GPT-5.6
Luna and GPT-5.6 Sol are scored on the same 124 screen-passing pairs
(reported on the 115 and on the 124) with the prompts, summaries and
metrics of the registered lanes, five draws each, through the raw API
with the settings of their Table 1 rows. No prediction is attached to
them. They are reported beside the registered readers and labelled not
registered. OpenAI cap for this lane: $14."
