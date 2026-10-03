# ADDENDUM_DS — Amendment 4: a view header that binds "User" to the persona and pins the current date

Written 2026-09-14 (program R109, from the forensic audit `reviews/DOWNSTREAM_AUDIT.md`), BEFORE any
call, as a separate file because `verify_ds.py` check A pins `registrations/ADDENDUM_DS.md`
byte-identical to `a5a2036`. **Two predictions with bars (A4-P1, A4-P2), written with their failure
texts before any call; everything else descriptive. DS-P1 to DS-P5 and Amendments 1 to 3 stand as
printed.** The author's instruction of 2026-09-14 (evening): "register DS Amendment 4 with a
prediction: view header with the persona's name and the pinned current date; re-run mini and Haiku
on the 452 views; in-view correct rises, abstentions fall; stale reported by first sentence and by
active-versus-tagged source beside the registered column; cap $8." Every number prints whichever way
it comes out. Frozen by sha256 before the first call (`ds_downstream/NUMBERS_DS.md` section 10;
CLAIMS.md R109 block).

## §A4.1 — Why: what the audit found

The audit (`reviews/downstream_audit/`, gated against every ledgered per-row score) traced the flat
correct count on the 174 licensed items to two things the view withholds from the answerer, not to
the policies. First, the view prints every entry as "User ..." and nothing binds that word to the
person the question names: the persona's name appears in 47 of the 174 licensed-item views while
172 of the 174 questions name the persona (`AUX-DS-AUDIT-IDENTITY`). Haiku 4.5 says so: of its 145
abstentions on the 221 licensed-item views it gives that reason in 94; on the 65 items whose licensed
record is in view under retrieval alone it abstains on 38, 34 of them for that reason, and GPT-4.1 mini
abstains on 15 of the same 65, 13 of them on a key where Haiku states the reason. Second, the view
gives each entry a relative age in days and no current date, so an answerer cannot judge "upcoming"
against "past" (Haiku says so on marcus_q10). This amendment adds the two missing facts to the user
message and re-answers the same views. It changes nothing else: the same 452 views byte for byte, the
same D.4 system prompt, the same two answerers, the same committed detector.

## §A4.2 — The prompt

`SYSTEM_ANSWER` is the frozen D.4 text verbatim (digest `af1c69c8…`). The Amendment 3 instruction is
not carried (the audit found it redundant for GPT-4.1 mini and mis-targeted for both answerers, so
the header's effect is measured against D.4 alone).

`USER_ANSWER_A4` is the D.4 user text with one header paragraph before the entries, verbatim:

```
The user is {name}. Every entry below that says "User" is about {name}. Today's date is {date}; each entry's age is counted back from today.

Entries from this user's memory store, each with the lifecycle metadata the store records for it:

```
{view}
```

Question: {question}
```

`{name}` is the persona's name as the persona YAML records it (`persona.name`, e.g. "Aisha Mohammed",
"William 'Billy' Kootook"); `{date}` is the persona's pinned present `t_now` printed as an ISO date
(e.g. 2026-05-26), the same instant from which every printed age is counted. Both are functions of
the item, so the population of distinct (item, view) pairs is unchanged. The runner asserts the two
D.4 digests and records the sha256 of `USER_ANSWER_A4` (`lock`) before any call.

## §A4.3 — Population and lanes

**Population.** The 452 distinct (item, view) pairs of Amendments 2 and 3 (`run/cell_ds.json`'s 422
plus the 30 LOOKUP-LIT views of `run/rows_ds_amend2.jsonl`); the runner recomputes the count and a
mismatch is a STOP. The prediction population is the **65 licensed items whose gold record is in the
retrieval view** (`stage1.json`, `gold_in_view` under ALWAYS, by entry id; the registered quantity;
29 personas, at most 7 items per persona), answered under the ALWAYS view (which is also the ORACLE
view for every licensed item).

**Lane 1, GPT-4.1 mini**: `gpt-4.1-mini` pinned, temperature 0, seed 42, max_tokens 200, JSON mode,
k = 1, one retry on a parse failure, the cache redirected to `ds_downstream/cache_amend4/`; served
identifier probed before launch (one call).

**Lane 2, Claude Haiku 4.5**: `claude-haiku-4-5-20251001`, temperature 0, max_tokens 200, k = 1,
`SYSTEM_ANSWER` as the system prompt and `USER_ANSWER_A4` as the user message, synchronous, the
answer read from the last JSON object of the reply with one retry (as Amendments 2 and 3); served
identifier probed before launch (one call).

Rows in `ds_downstream/run/rows_ds_amend4_mini.jsonl` and `rows_ds_amend4_h45.jsonl`, keyed by item
id and view sha256 as before. Runner `ds_downstream/tools/amend4_header.py` (lock / probe / project /
run / score), written from `amend3_instruct.py`.

## §A4.4 — Predictions (written before any call)

Base rates, D.4 prompt, the 65 in-view licensed items (`AUX-DS-AUDIT-IDENTITY`): GPT-4.1 mini
detector-correct 37, abstained 15, correct among the 50 answered 37; Haiku 4.5 detector-correct 38
(12 of them abstentions whose explanation restates the gold line), abstained 38, correct among the
27 answered 26.

**A4-P1 (in-view correct rises).** For each answerer, Δ₁ = (correct under A4 − correct under D.4) / 65
on the 65 items, `correct` being the committed detector's flag at TAU_GOLD, is **at least +0.10**
(seven items), and both 95% bootstrap intervals of Δ₁ (item-level and grouped by persona; 10,000
resamples, seed 42, percentile) **exclude zero**. The weaker reading governs.

*Derivation of the bar.* If the header removes the identity abstentions and the freed items are
answered at each answerer's observed correct-among-answered rate: GPT-4.1 mini 15 × (13/15) × (37/50)
≈ 9.6 more correct, Δ₁ ≈ +0.15; Haiku 4.5 38 × (34/38) × (26/27) ≈ 32.7 answered correctly, of
which 12 were already counted, net ≈ +20.7, Δ₁ ≈ +0.32. The bar of +0.10 is two thirds of the
smaller expectation and a third of the larger; it is set below the expectation because mini's
mechanism is inferred from the key overlap with Haiku's stated reason (13 of 15) and the conversion
rate is estimated on 50 items.

*Failure text.* "The header binding the entries to the persona and pinning the date raises the correct
count on the 65 licensed items in view by less than 0.10, or by an amount whose interval reaches zero,
for {answerer}: {k_D4} to {k_A4} of 65, Δ₁ = {d} with intervals {ci_item} and {ci_persona}."

**A4-P2 (in-view abstention falls).** For each answerer, the number of the 65 in-view items answered
with an abstention (the answer begins with, or contains, "store does not currently contain", the
D.4 wording) **falls by more than half**: GPT-4.1 mini 15 → 7 or fewer; Haiku 4.5 38 → 19 or fewer.

*Derivation of the bar.* The abstentions not carrying the identity reason (2 of mini's 15 by key
overlap; 4 of Haiku's 38 by its own text) are the expected residue; a few items are genuinely
ambiguous (a partner's event asked as the user's; a direct-sale question with no confirming record).
"More than half" leaves those and as many again.

*Failure text.* "The header leaves {answerer}'s abstentions on the 65 licensed items in view at
{k_A4} against {k_D4}, not less than half."

**Descriptive, no bar.** (i) Stale use at TAU_HI and TAU_GOLD per policy and answerer, the
`AUX-DS-STAGE2` columns, **with two columns beside the registered one**: stale on the first sentence
of the answer alone (split at sentence punctuation followed by a space and a capital, as
`reviews/downstream_audit/audit_ds.py` `first_sentence`), and stale split by the **source in the
view** — whether an active line of the view asserts the stale value (the item's own detector at
TAU_GOLD on the line's text: old-only coverage ≥ 0.50 with ≥ 2 shared tokens and new-only coverage
< 0.34) or only tagged lines do (`audit_ds.py` `step4b`). The 15 expiry obligations print in the
registered column as registered and are marked unscorable in the two new columns (their gold field
is the expired fact). (ii) PRESENT correct and abstention over all 174 and 221 views; the count of
answers both abstaining and detector-correct. (iii) The expiry rows' answers under the pinned date,
read as a list. (iv) Spend from response usage.

## §A4.5 — Budget and STOP

Both lanes together are capped at **$8.00** (the author's line). Projection from the D.4 rows' recorded
tokens plus 45 header tokens per call: GPT-4.1 mini ≈ $0.13, Haiku 4.5 ≈ $0.42, sum ≈ $0.55 (×1.3
≈ $0.71). The runner projects each lane from its probe over the 452 views, prints the sum beside the
line, and refuses to launch if the sum times 1.3 is at or above it; each client's hard cap is set to
$8.00. STOP conditions: served-identifier mismatch on either lane; the population count or the 65
not reproducing; the prompt digests not reproducing; any persona without a name or a `t_now`;
failures after the retry on more than 2% of a lane's calls; the projection over the line; any call
before this file's sha256 is recorded in `NUMBERS_DS.md` section 10.

## §A4.6 — Ledger and paper sites

`ds_downstream/NUMBERS_DS.md` gains section 10 with keys `AUX-DS-A4-REG` (this file's sha256, before
the first call), then `AUX-DS-A4-LOCK`, `-PROMPT`, `-POP`, `-PROBE-MINI`, `-PROBE-H45`, `-PROJECTION`,
`-P1`, `-P2`, `-STAGE2-MINI`, `-STAGE2-H45`, `-FIRSTSENT`, `-SOURCE`, `-PRESENT`, `-EXPIRY`, `-SPEND`.
Paper (program R109 registers; a later program lands the numbers): one sentence in Section 8 naming
the registration and its two predictions as pending; the rows print in Appendix F.10 beside the
registered rows once run; the registration record (Appendix G) gains the row. `verify_ds.py` is
unaffected.

## Registration mechanics

Frozen by sha256 before the first call (recorded in NUMBERS_DS.md section 10 and CLAIMS.md R109).
Copied to `iclr2027_monitoring_submission/ARTIFACT/registrations/ADDENDUM_DS_AMENDMENT_4.md`.
Further amendments append dated sections and never edit the text above.
