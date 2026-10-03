# ADDENDUM_CF_PAD — the long-list check: five readers and three lookups on the counterfactual set with the superseded-names list padded to 60 names

Drafted 2026-09-22 (program R136, the one exception to the experiment freeze of 21 September), BEFORE any
call and before any score exists. It carries four predictions (§7), written here before any score; every
row prints whatever it shows. Frozen by the sha256 of the bytes above the marker line, committed alone before
the first paid call; the runner writes `cf_pad/build/lock.json` with the hash at start. The recorded Table 1
rows are read and never re-run. Ledger `cf_pad/NUMBERS_CF_PAD.md`; report `reviews/r136/REPORT_R136.md`.
Nothing lands in the paper from this file; the paper's home for the result is decided by the author after
the report.

## §1 — Why

The paper's second finding says that on the named state no model reliably beats a cosine lookup over the
names. Reviewers object that the ground-truth list is about two names long, so the comparison is easy. The
paper already shows the lookup falling to $0.67$ when the list is padded to 60 names
(`registrations/ADDENDUM_PAD.md`; `tab:pad`, AUX-PAD-LOOKUP-EMB: $0.7484 \to 0.6696$), but only on the full
obligation set of 661, and no model beyond GPT-4.1 mini and Haiku 4.5 has ever read a long list. This run puts
all five models beside the lookup on the counterfactual set with a 60-name list. Whatever comes out gets
printed.

## §2 — Population and the recorded rows

**Population.** The counterfactual set, all **444** items from **148** triples (88 supersession, 30
retraction, 30 expiry; 40 personas; `r82_counterfactual/cf2/cf_cell.json`, indexes `cf2/cf_indexes.json`
key `v2`, content sha256 as `cf_indexes.json` `meta.sha256` records it and `cf_cell.json` `meta.indexes_sha256`
repeats it, asserted at lock), the original questions, the default summary that names only superseded content
(`INDEXED-V2`), with the superseded-names list padded to 60 names by the rule of §3. Nothing else in the
summary changes. Never subset.

**The recorded rows this run is paired against**, read from `reviews/r125/results/r125_vectors.json` (every
vector gated there on its ledgered whole-set pooled AUROC at four decimals; the gate is re-asserted at lock)
and never re-run:

| reader | key | recorded rows | draws | whole-set pooled AUROC (gate) |
|---|---|---|---|---|
| GPT-4.1 mini, Table 1's five-draw row | `MINI5_v2` | `reviews/r122/rows/rows_MINI5.jsonl` `INDEXED-V2` | 5, provider-default temperature | 0.7648 |
| Haiku 4.5 | `H45_v2` | `r82_counterfactual/cf2/rows/rows_H45.jsonl` `INDEXED-V2` | 5, temperature 0, Batch | 0.7566 |
| GPT-5.6 Luna | `LUNA_v2` | `cf2/rows/rows_LUNA.jsonl` | 5, raw API | 0.8417 |
| GPT-5.6 Sol | `SOL_v2` | `cf2/rows/rows_SOL.jsonl` | 5, raw API | 0.8500 |
| Opus 5 | `OP5_v2` | `cf2/rows/rows_OP5.jsonl` `INDEXED-V2` | 5, Batch | 0.8405 |
| embedding name lookup | `LOOKUP_v2` | `score_cf.matcher` on the committed v2 lists | — | 0.7663 |
| random-token lookup | `RANDTOK_v2` | `enc_lookup.random_token` + `score_cf.matcher` | — | 0.5954 |
| word-matching (lexical) lookup | — | `run_nb6.lex_scores` on the committed v2 lists (AUX-CF2-NB6-V2) | — | 0.6698 |

The X4 collapse is unchanged: a five-draw reader's score per item is the mean `nok` over its OK draws,
MIN_DRAWS 3 (`score_cf.load_lane`); a one-draw reader's is its single draw. The supersession-slice pooled
AUROC and the matched score of every recorded row are recomputed from these gated vectors at lock and printed
there; they are the "unpadded" values of §6.

## §3 — Construction: the padding rule (deterministic, no model call)

The rule is `ADDENDUM_PAD` §3 carried to the counterfactual set with the triple as the unit; the differences
from the 661-item rule, and why each is forced, are stated at the end of this section. Code:
`cf_pad/tools/cf_pad_common.py` (reusing `pad_probe/tools/pad_common.py`'s renderer, parser and pool
functions verbatim).

**3.1 The padded section.** For every item, the superseded-names section of the committed `v2` text (the
section is the tail of every v2 text; `resp_common.split_section`) is re-rendered over its committed names
plus the triple's pad by `index_v3._name_block` under the v2 name-block grammar — the names printed as a
**sorted set**, wrapped at 150 columns, indents two and four spaces, `(none)` when empty — with the per-bucket
cap of 15 (`index_v2.SLOT_CAP`) **lifted to 100** exactly as `ADDENDUM_PAD` §3 and the SIDE S2-U build lifted
it (`pad_common.render_section_lifted`, `SLOT_CAP_LIFTED = 100`), so every name prints and no `(+N more)`
appears. The text above the section header is byte-identical to the committed text: the lifecycle totals, the
per-category counts and the per-category name map keep their committed values. The `superseded` total
therefore disagrees with the padded list length, as in `ADDENDUM_PAD` (the author's ruling of 2026-09-22, point 3).
**Renderer lock:** the section re-rendered over the committed names alone reproduces the committed v2 text
byte for byte on 444 of 444 items, or STOP (it did, in the dry run; `contam.py` established the same lock for
`ADDENDUM_PAD` Amendment 1).

**3.2 One pad per triple.** The pad is drawn once per triple, under `random.Random(f"42:{pair_id}")`, and
the three versions of the triple receive **the identical pad names in the identical draw order** (the
rendered section then prints them sorted). Every version's list is its own committed names plus the pad. The
pad has $60 - |\text{committed}(\text{PN})|$ names, so **the PN version's list has exactly 60 names**; a
sibling's list is shorter by exactly the names the PN version's committed section carries and the sibling's
does not (the target, and on 7 supersession triples one further name the PN version's added entries carry:
59 names on the siblings of 81 supersession triples, 58 on those of 6, 57 on those of 1, 60 on every counted-state item, where the three committed
lists coincide). The three versions' lists differ in length by the committed section only, as in the
unpadded set (the author's ruling of 2026-09-22, point 2). The versions therefore still differ only in what
the store's change adds, as the unpadded lists do (1 or 2 names against `(none)` or the persona's other
superseded names).

**3.3 Pools, in draw order.**

1. **Pool A, the persona's own attributes:** every attribute name printed in the per-category name map of
   **all three** versions' v2 texts (the intersection; `index_features.parse` `attr_by_cat`, all buckets;
   the `(+N more)` overflow fragments dropped, D-PAD-3), excluding
   (i) every name in **any** version's committed superseded section;
   (ii) every scrubbed slot that any scored question of the persona targets: in the counterfactual set, the
   target slot of each of the persona's pairs (`cf_cell.json` `meta.individuation[pair].slot_scrubbed`) and
   every slot of the entries any of its pairs' PN versions add (`pn_members`, resolved through
   `backend_entries/frbank.json`; the six authored entries `lb_r82_<persona>` carry the pair's own target
   slot); in the main study, the persona's 661-cell targets under `ADDENDUM_PAD`'s D-PAD-2 (wide reading,
   `pad_common.targeted_slots`) — the same "either population" exclusion `nb6_sweep`'s pools applied for the
   injection amendment;
   (iii) any name containing `:` or whitespace (`pad_common.poolable`);
   (iv) **the change set:** every name in the symmetric difference of the three versions' printed maps
   (the target, and names the 15-per-category cap displaces when the target enters a category), every slot
   of the PN version's added entries, and the target — implied by the intersection and (i), asserted
   explicitly.
2. **Pool B, other personas' attributes**, used only after pool A is exhausted: every attribute name printed
   in the per-category name map of every other persona's `frbank:<persona>:FULL:TRUE` text, excluding any name
   in this persona's own maps (the three versions' and its FULL:TRUE map), its committed sections, and the names
   excluded under (ii)–(iv); deduplicated, sorted before the shuffle.

Pool A is shuffled once, pool B once, under the triple's seed; the concatenation is taken in order. Pool A
holds at least 71 names on every triple (median 102, max 121), so **no pad draws on pool B**; every pad name is
a name the committed summary already prints in its map.

**3.4 Assertions at build (each a STOP):** every PN list has exactly 60 names; every list is free of
duplicates, `:` and whitespace and contains its committed names; the pad is identical across the triple's
versions; no pad name is in the change set or in the persona's (ii) set; the target (and any slot the PN
version adds) is in a sibling's list only where the sibling's committed section already lists it; the
re-parsed padded text yields exactly the padded list; the text above the header is byte-identical; no `(+`
in any rendered section; every pad name is a scrubbed slot name of the persona's store (value-free by
construction) and equals no stored entry's text. **The leak scan** is these last four checks plus the
target-in-sibling check, run again at run time before any paid call; descriptive counts print beside it
(pad names that equal another entry's slot-path qualifier, such as `rent` beside `financial_concern:rent`;
pad names that occur as substrings of a PN-added entry's text, such as `rent` inside `current`).

**3.5 The target's position** in the PN version's rendered list is its alphabetical rank among the 60 names.
Dry run over the 88 supersession triples: min 2, median 41.5, max 60; first position 0 times, last position
4 times; by tenths of the list (six positions each) 5 / 3 / 2 / 5 / 8 / 12 / 12 / 9 / 9 / 23 (the last tenth is heavier because
several targets begin with late letters, `t`–`w`). Full histogram (rank: triples): 2:1, 4:3, 5:1, 11:1, 12:2,
17:1, 18:1, 20:1, 24:4, 25:3, 26:1, 27:1, 28:2, 30:1, 31:1, 32:1, 33:2, 34:1, 35:3, 36:4, 38:2, 39:2, 40:1,
41:4, 42:3, 43:1, 44:4, 47:2, 48:2, 49:2, 50:1, 51:3, 52:2, 53:1, 55:3, 56:9, 57:1, 58:4, 59:2, 60:4
(`cf_pad/build/dryrun_build.json` `target_position`). The position is printed against each reader's score
as a descriptive row (§8).

**3.6 What differs from `ADDENDUM_PAD` §3, and why.**
- *Unit and seed:* per triple (`42:{pair_id}`), not per summary key, because the brief requires identical
  pads within a triple and the three versions are three keys.
- *Pool A from the intersection of the three versions' maps*, not one text's map, because the maps differ by
  the target and by names the category cap displaces; a name printed in one version and not another would
  make the pad differ across versions or put a changed name into the pad.
- *Exclusion (ii) over both populations* (the counterfactual pairs' targets and PN-added slots, and the
  661-cell targets), because the padded summaries are read by the counterfactual questions and the rule's
  purpose — no pad name is a name a scored question asks about — must hold for them; the 661 exclusion is kept
  so the pools match the injection amendment's.
- *Pad size fixed by the PN version* (60 − |committed(PN)|) and shared, rather than each list padded to 60,
  because a per-version fill would give the siblings one name the PN version lacks; the sibling lists are
  therefore 58–60 long.
- *No nesting across lengths:* only L = 60 is built (D-PAD-1's prefix property has nothing to nest).
- Everything else is unchanged: the renderer and the lifted cap, the sorted rendering, D-PAD-3's fragment
  rule, the byte-identical prefix, the counts left as committed.

## §4 — Readers and settings

**Lookups ($0; `cf_pad/tools/cf_pad_common.lookup_scores`).** On the padded lists as the padded text
prints them: the **embedding name lookup** (`sweep_common.emb_cached` = `run_nb6.emb_scores`,
`sentence-transformers/all-MiniLM-L6-v2`, local, max cosine of the question against the names, underscores
as spaces), the **word-matching lookup** (`sweep_common.lex_cached` = `run_nb6.lex_scores`, max Jaccard over
content tokens) and the **random-token lookup** (every distinct name replaced by `enc_lookup.random_token`'s
stable eight-letter pseudo-word, seed 42, then the embedding lookup on the tokens). Gate at lock: the three
on the committed lists reproduce 0.7663 / 0.6698 / 0.5954 at four decimals, or STOP.

**Models.** Prompts are `prompts_e1.SYSTEM` and `prompts_e1.USER_INDEXED` byte for byte (file digest
`337d37d3…`, texts digest `35d9b968…`, asserted by `run_cf` at import), the padded v2 text in place of the
summary, the recorded question; no other system text. Settings are the Table 1 rows' (the recorded lanes'
code paths, called, not copied):

| lane | model id | draws | settings | path |
|---|---|---|---|---|
| mini | `gpt-4.1-mini` | 5 | `max_tokens` 200, temperature **unset** (provider default, the five-draw row's D-R122-1), Chat Completions | `reviews/r122/tools/oai_run.py`'s MINI5 call shape |
| Haiku | `claude-haiku-4-5-20251001` | 5 | temperature 0, `max_tokens` 200, Batch | `run_cf.LANES` / `cmd_submit` |
| Luna | `gpt-5.6-luna` | 5 | reasoning effort and temperature unset, `max_completion_tokens` 2048, raw Chat Completions | `cf2_openai.call_once` |
| Sol | `gpt-5.6-sol` | 5 | as Luna | `cf2_openai.call_once` |
| Opus | `claude-opus-5` | **1** | temperature unset, `max_tokens` 1024, no thinking parameter (the recorded draws' kwargs), Batch | `run_cf.LANES` / `cmd_submit` |

Opus 5 runs at one draw through Batch with the settings of its recorded draws and is compared against its
recorded five-draw row; **this is stated wherever Opus's row prints** (the recorded draw 1 alone, 0.8400 on the
whole set, prints beside as descriptive). Arm name `INDEXED-V2-PAD60`; rows under `cf_pad/rows/`, resume key
(`unit_id`, arm, draw); OpenAI lanes draw-major (draw d for all 444 before d+1), eight workers; the Anthropic
lanes one Batch each.

**Served identifiers** are checked as in the paraphrase run: one probe call per lane before launch on the
first unit (`run_cf`-style lanes: `lane.split("-2025")[0] in served or lane in served`; raw OpenAI lanes:
`model in served`), the identifier recorded in `cf_pad/build/probes.json`, and every row's `served_model`
re-checked at scoring; a mismatch is a STOP for that lane. Probe rows are not scored.

## §5 — Endpoints, both fixed here

**Primary: pooled AUROC** (`common_e1r.auroc`, Mann–Whitney with ties at 0.5) of the reader's item scores
against `y_nok`. **Secondary: the matched within-triple score** $(W + T/2)/n$, the PN version against the
PRESENT version of the same triple (a win when PN's collapsed score is strictly higher, a tie when equal;
`r125_common.outcomes` / `wtl`). Both are reported for the whole set ($n = 444$ items; 148 triples) and for
**supersession alone** (the CF-2 per-state convention: the 264 items of the 88 supersession triples, positives
and negatives alike, `sweep_common.state_mask`; 88 triples).

**Intervals.** Pooled: the item-level paired bootstrap (`common_e1r.boot_item`) and the persona-grouped
paired bootstrap (`boot_cluster`, group = persona; triples enter whole because a triple's items share a
persona), 1,000 draws, seed 42, single-class draws discarded. Matched: the triple-level bootstrap
(`r125_common.boot_triple`) and the persona-grouped bootstrap (`boot_persona`) of the mean per-triple outcome
difference, 1,000 draws, seed 42. **A difference is reliable when both intervals exclude zero.** Tolerance
$\pm 0.05$ on point estimates. No multiplicity correction; the comparisons in §6 are the only ones called
registered.

## §6 — Registered comparisons, supersession only, 60-name list

- **each model minus the embedding lookup** on the same padded lists, pooled and matched;
- **each reader's padded score minus its own unpadded score** on the same triples, pooled and matched (the
  unpadded scores are the recorded Table 1 rows of §2, restricted to the supersession slice; for Opus the
  recorded five-draw row).

Each prints with both intervals, beside the same difference on the unpadded list (the recorded model minus
the recorded lookup).

## §7 — Predictions, written before any score exists

Each prediction is read on the primary endpoint (pooled AUROC, supersession slice); the matched reading
prints beside it and does not decide (the author's ruling of 2026-09-22, point 5: as drafted).

- **P-L1 (the author's):** each of Luna, Sol and Opus exceeds the embedding lookup on supersession with the
  60-name list, pooled AUROC, reliably (model minus lookup $> 0$ with both intervals above zero). HOLDS iff
  all three do.
- **P-L2:** neither mini nor Haiku reliably exceeds the embedding lookup there. HOLDS iff neither difference
  is reliably above zero.
- **P-L3:** the embedding lookup loses more than $0.05$ on supersession against its unpadded score, reliably
  (padded minus unpadded $< -0.05$ with both intervals below zero).
- **P-L4:** each of Luna, Sol and Opus loses less than the lookup does: each model's padded-minus-unpadded
  point estimate is greater than the lookup's (a gain counts as losing less). HOLDS iff all three do.

A prediction holds or fails as stated. Every row prints whatever it shows. Failure text, frozen: "P-Lk FAILS:
<the quantity> reads <value> with intervals <item> and <persona>."

## §8 — Descriptive, not registered

The whole-set rows (pooled and matched, every reader); the retraction and expiry rows (the list does not name
those states, so padding should matter little there; their three versions carry identical padded lists);
the random-token and word-matching lookups (pooled and matched, whole and per state, padded minus unpadded);
the position of the target in the PN list against each reader's per-triple outcome and PN score (Spearman
correlation and the matched score by tenths of the list); Opus's recorded draw 1; the per-lane census (rows,
not-OK rows, distinct collapsed values, tied triples); the seed spot-check 43–46 on the registered pooled
differences.

## §9 — Budget

Caps: **Anthropic $12, OpenAI $20** (the author's ruling of 2026-09-22, point 1: Sol at five draws), metered from the rows at the page prices below before every call
(OpenAI) and at submission from the probe projection (Anthropic Batch). Lanes are sent draw-major so a halt
leaves whole draws; a partial draw is discarded and disclosed with its row count. **If a cap would be
exceeded, drop draws in this order: Sol to three draws, then Haiku to three; never subset the 444.** Any such
drop is a dated deviation in `cf_pad/DEVIATIONS_CF_PAD.md`.

Prices (USD per million tokens): `gpt-4.1-mini` 0.40 / 0.10 cached / 1.60 out; `gpt-5.6-luna` 0.20 / 0.02 /
1.20, cache writes 1.25×; `gpt-5.6-sol` 4.00 / 0.40 / 20.00, writes 1.25× (OpenAI's pages as
`ADDENDUM_CF2_OPENAI.md` and `ADDENDUM_R122_MINI_K5.md` record them); `claude-haiku-4-5-20251001` 1.00 /
5.00 and `claude-opus-5` 5.00 / 25.00 at Batch's 50% (the model table read 2026-09-22).

Projection from the dry run (`cf_pad/build/projection.json`; prompt sizes measured on the padded texts,
o200k mean 1,835 tokens against 1,605 committed, ratio 1.144; each lane the larger of a price formula and the
recorded lane's own rows scaled by the per-item ratio; the recorded output means kept): mini $1.25, Luna
$0.78, Sol $12.25 (draw 1 uncached, draws 2–5 at the cached rate as the recorded lane ran); Haiku $3.19,
Opus $4.43. **Anthropic $7.62 (×1.3 $9.90) inside $12; OpenAI $14.28 (×1.3 $18.57) inside $20** (at the
brief's $18 the margin figure exceeded the cap by $0.57, which is why the cap was raised); Sol at three draws
projects $8.86 (OpenAI ×1.3 $14.16). Sol is the last OpenAI lane, so the cap rule above truncates Sol's later
draws and nothing else. Should the OpenAI cache not engage, Sol alone projects $23.23; the draw-major order is
what engages it, and the metering halts the lane at the cap.

**Order after the GO (§3 of the brief):** freeze and commit this file alone → lock → the lookups → probes
(one call per lane) → the Haiku and Opus Batches submitted → mini → Luna → Sol (draw-major, the OpenAI cap
metered across the three) → the Batches polled quietly → scoring once, when every lane is complete or a
registered halt rule has fired → ledger → report. No interim scoring for anyone.

## §10 — STOP list

Registration sha256 mismatch; the indexes' content hash differing from `cf_indexes.json` `meta.sha256`;
any recorded-row gate of §2 or lookup gate of §4 failing at four decimals; the renderer lock failing on any
item; any §3.4 assertion or the leak scan failing at run time; a served identifier that differs (that lane
does not launch, or its rows are not scored); more than 1% unparseable rows in a lane after the client's
retries (`status != OK`); a cap breach; any score computed before this file is frozen and committed.

## §11 — Ledger and report

`cf_pad/NUMBERS_CF_PAD.md`: `AUX-CFP-LOCK` (hashes, gates, pools, pads, leak scan, positions),
`AUX-CFP-PROBES`, `AUX-CFP-LOOKUP-{EMB,LEX,RANDTOK}`, `AUX-CFP-{MINI,H45,LUNA,SOL,OP5}` (whole and
supersession, pooled and matched, padded beside unpadded, both differences with both intervals, per state),
`AUX-CFP-P-L1` … `AUX-CFP-P-L4`, `AUX-CFP-POSITION`, `AUX-CFP-SPEND`. `cf_pad/results/cf_pad_printed.json`:
every two-decimal form a paper sentence might need, each with its four-decimal source key, in the style of
`cf2_paraphrase/results/para_printed.json`. `reviews/r136/REPORT_R136.md` as §4 of the brief.

## Registration mechanics

Frozen by the sha256 of the bytes above the marker line and committed alone before the first paid call (the
author's written GO quotes the sha256). `cf_pad/tools/cf_pad_common.REG_SHA` is set to it and every
subcommand that spends or scores asserts it. Amendments only as dated lines below the marker; the text above
never changes.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
