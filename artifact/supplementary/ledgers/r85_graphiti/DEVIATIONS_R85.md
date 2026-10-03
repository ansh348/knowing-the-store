# R85-GRAPHITI — deviations

Numbered `D-R85-n`. Every entry below is a departure from the program text as written, taken
at Phase 0 before any billed call, and each is recorded with what was written, what is done
instead, and why.

---

## D-R85-1 — the episode reference timestamp is `created_at`, not `event_time`

**Written.** "Each FR-Bank record is rendered as the user would have stated it at its event
time, with the record's event time as the episode reference timestamp. Records sharing an
event time may share an episode; records with different event times may not."

**Done.** The reference timestamp is `created_at`, the session date, for every episode,
including the 1,912 records that do carry an `event_time`. Episodes are cut one per
(persona, `created_at`), ordered by `created_at`, with records inside an episode ordered by
`id`.

**Why.** `event_time` is null on **17,024 of 18,936 records**, so the rule as written
collapses ninety percent of the corpus onto a single undefined timestamp and the
may-not-share clause becomes unreadable. `created_at` is populated on every record and is
the session date, giving 34.1 sessions per persona and 1,365 episodes across the forty. An
event time is also the date of the event rather than the date the user stated it, and
Graphiti's extractor is specified to infer validity and expiry from content and reference
time on its own, so handing it the event date as a reference timestamp would supply an
anchor the user never gave. No absolute date is injected into the rendered text: the records
already carry the user's own relative wording, which resolves against the reference
timestamp.

---

## D-R85-2 — ground truth is the persona manifest, not FR-Bank's `supersedes` links

**Written.** The census and the gate were to be scored against recovered supersession
events without naming the source of the event set.

**Done.** The denominator for the census, for the gate, and for the TRUE-projected index is
the persona manifest: the supersession events surviving the `MIN_DISCR` filter that
`e1_metamemory/tools/believed_frbank.py:56-58` applies, the expiry anchors, and the
retraction records. The selection tool re-derives the published figure and reaches 109 over
the forty personas.

**Why.** Scoring Graphiti against FR-Bank's `supersedes` links would measure one backend's
belief against another's. The paper already reports those links overstating staleness by
about sixty times. A measured consequence: 4,111 of 5,725 links join records from the same
session and 372 join byte-identical texts, so a large part of that link set records
extraction restatement rather than lifecycle change. That census is reported as a
descriptive finding in its own right.

---

## D-R85-3 — the supersession-pointer clause is struck

**Written.** "SUPERSEDED: `invalid_at` set and a later edge exists on the same (subject,
predicate), or Graphiti's own contradiction pointer targets this edge."

**Done.** The second disjunct is struck. SUPERSEDED is derived from `invalid_at` together
with a later edge on the same slot.

**Why.** Graphiti has no contradiction pointer. `resolve_edge_contradictions` sets
`invalid_at` to the superseding edge's `valid_at`, sets `expired_at` to the current time,
and discards the superseding edge's identifier. Searching the whole unmodified package for
`superseded_by`, `invalidated_by` and `contradicted_by` returns nothing. The clause named a
field that does not exist.

---

## D-R85-4 — the persona rider is read jointly, and a third persona is added

**Written.** "If persona A carries fewer than four manifest supersession events, take the
next persona under the same rule, so the gate has something to count."

**Done.** Read as applying to the personas jointly, and `yoli` is added as persona C under
the rule "most manifest supersession events", on the unmodified arm and `gpt-4.1-mini`
only. The gate denominator is 10 events across elena, tom and yoli.

**Why.** Read per persona the rider cannot be satisfied. Exactly one persona in the
population, `yoli`, carries four filtered manifest supersession events; every other carries
three or fewer; and `yoli` carries zero PRESENT-NEGATIVE items, so the persona A rule can
never reach it. No persona satisfies both conditions. The joint reading is what "so the gate
has something to count" means and what the gate's own "on both personas" wording implies.
The third persona costs about $0.60 against roughly $5 of unspent spike headroom.

---

## D-R85-5 — the full-run budget is re-partitioned

**Written.** Ingestion no more than $17, stop before any monitor call if billed ingestion
exceeds $22, monitors no more than $15, Opus 5 at k=5 if the ceiling allows.

**Done.** Ingestion sub-ceiling $24, stop rule $28, monitors $15, Opus 5 registered as
dropped. The overall $45 ceiling is unchanged.

**Why.** The $17 figure predated any measurement. Two independent anchors now put the
40-persona ingestion at $19 to $23, so the original sub-ceiling would have forced the
cheaper extractor for a reason unrelated to extraction quality. Opus 5 at k=5 over both
provenances prices at about $180 and cannot fit $45 under any partition, so it is recorded
as dropped with its price rather than left as a conditional.

---

## D-R85-6 — the extractor deviates from "the cheapest configured model"

**Written.** "The extractor is the cheapest configured OpenAI model that supports structured
output."

**Done.** `gpt-4.1-mini-2025-04-14` is pinned for the full run unless nano's entity-level
recall against the manifest is within 0.05 of mini's on persona A **and** mini's measured
40-persona projection exceeds $24. Persona A runs on both models in the spike so the choice
is priced rather than argued.

**Why.** The vendored library's own guidance records that its structured-output pipeline
fails more often on smaller models. Choosing the cheapest model by rule would confound "this
backend's self-description erases lifecycle" with "we chose a weak extractor", and an
adverse census row would then be uninterpretable. Mini is also Graphiti's documented default
tier and the model the study's own extractor uses, which makes the comparison like for like.

---

## D-R85-7 — a second Neo4j instance replaces a new database name

**Written.** "Start Neo4j (or FalkorDB) fresh, under a database name FR-Bank never used."

**Done.** A second container, `neo4j-r85`, on ports 7475 and 7688 with its own volume. The
database name inside it remains `neo4j`. Isolation is the fresh instance plus one group
identifier per persona per arm, `r85stock_<persona>` and `r85fork_<persona>`.

**Why.** The image is Neo4j Community edition, which serves exactly one user database, so a
different database name cannot be created. The requirement is met more strongly by a fresh
instance: the existing default database holds the earlier `full_234` and `lifemembench_*`
graphs, carries `fr_*` property overlays, and is additionally reachable by a vendored
third-party benchmark that issues unscoped whole-database mutations.

---

## D-R85-8 — the client stack is pinned below the library's declared floor

**Written.** "A clean venv for stock `graphiti-core`. Pin the exact version."

**Done.** `graphiti-core==0.28.1` as written, plus `openai==2.24.0` and `neo4j==6.1.0`.

**Why.** `graphiti-core 0.28.1` declares `openai>=1.91.0` with no upper bound. A fresh
resolve takes `openai 3.6.0`, which has dropped `httpx`, and the library imports `httpx` at
module scope, so the pinned version cannot be imported at all as resolved. The two pins
match the versions the modified arm already runs, so the arms differ only in Graphiti's own
code, which is the comparison the program exists to make.

---

## D-R85-9 — the program is relabelled from R83 to R85

**Written.** The program was queued as R83-GRAPHITI with `D-R83-n` numbering and
`registrations/ADDENDUM_R83_GRAPHITI.md`.

**Done.** R85-GRAPHITI, `D-R85-n`, `registrations/ADDENDUM_R85_GRAPHITI.md`, fence directory
`r85_graphiti/`, commit prefix `R85-`.

**Why.** R83 already names a completed prose and citation pass: about twenty `R83-*` commits
landed on 2026-08-30, `D-R83-1` and `D-R83-2` exist in
`iclr2027_monitoring_submission/DEVIATIONS_R74.md:584` and `:618`, and `CLAIMS.md` carries
three authorizations tagged R83. R84 is likewise taken. R85 is the first free label, and the
registration table needs one program per name.

---

## D-R85-10 — the recency axis reads `valid_at`, not `created_at`

**Written.** The frozen rules cover lifecycle derivation (RULE 1) and attribute naming
(RULE 2). Neither covers how the index's recency axis maps onto Graphiti's fields.

**Done.** Edge age is taken against `valid_at`, falling back to `created_at` where the
extractor left `valid_at` null.

**Why.** This is a gap being filled rather than a frozen rule being edited, and it is
recorded here because the choice was made after the first dump was read. Graphiti's
`created_at` is transaction time, the wall clock at ingestion, exactly as the upstream field
description says. Taking age against it makes every edge zero days old and turns the recency
axis into a description of when the run happened rather than of what the store holds. The
first partial dump showed precisely that: all 86 edges in the 0-30 band with newest, oldest
and median all zero. `valid_at` is the semantic analogue of FR-Bank's `recency_time`, which
is the record's own session date, so it is the mapping that makes the axis mean the same
thing on both backends. The count of edges whose `valid_at` the extractor left null is
reported beside the axis, because that count is the extractor's failure to date its own
facts and it belongs in the census rather than hidden in a fallback.

---

## D-R85-11 — the modified-fork arm was stopped externally and is cut to one persona

**Written.** Phase 1 ingests personas A and B on the locally modified vendored tree, for one
patch-delta line.

**Done.** Both fork ingests were stopped externally partway through, elena at 25 of 34
episodes and tom at 15 of 35. The arm is cut to persona A only, re-run clean from a wiped
group. The patch-delta line rests on elena.

**Why.** No number in the paper comes from the modified arm; ruling R82-D4 already names it
as the arm to cut when the spike is squeezed. One persona carries a one-line delta, and the
disclosure paragraph rests on the static source diff, which is complete and independent of
any run.

**What the stop cost.** Less than first appeared. The tom process survived the stop, ran
through all 35 episodes, and reached its own completion path, so it **wrote a full ledger**:
$0.2595, measured, not estimated. Only the elena partial was wasted, 25 episodes at roughly
**$0.19 estimated at the measured rate of $0.00745**, discarded when the group was wiped for
the clean re-run. That $0.19 is the sole unrecoverable figure, and it is an estimate because
the pre-checkpoint code wrote its cost record only on completion. Their per-episode logs were pipe-buffered and did not survive either. The four
stock arms that the gate reads were verified intact before any further spend: elena mini
34/34, tom mini 35/35, yoli mini 34/34, elena nano 34/34, each with a full per-episode row
set and a positive recorded cost.

**Cause.** Not environmental. The only sleep and resume events on the machine predate the
runs by two hours, both containers ran continuously, and exactly the three background tasks
alive at that moment stopped together while nothing else was disturbed. That is a
stop-all-background-tasks action rather than a machine or terminal failure, so a resume does
not fail the same way at the same episode.

**Two consequences, both handled.** The ingest harness now checkpoints its ledger after
every episode, so a stopped run can still say what it spent. And the fork-tom process turned
out to have survived the stop as an orphan, its shell wrapper killed but the interpreter
still ingesting and still billing outside any ledger; it was at 31 of 35 episodes when
found, so it was allowed to finish rather than killed. It completed, wrote its ledger, and both its
graph and its cost are on the same footing as every other arm.

**The patch-delta line reports four patches, not five.** The fifth, undocumented
world-knowledge filter routes every non-speaker edge to xAI, whose credential has returned
403 since 2026-07-31, and the filter fails open on exception. It is inert on this run. The
delta therefore measures the four documented numeric-preservation patches with the fifth
disabled, and the report says so rather than implying the modified arm is the arm that ran
in February and March.

---

## D-R85-12 — the forbidding-record state split is read from the join, not the attack vector

**Written.** `ADDENDUM_R85_GRAPHITI_AMENDMENT_1.md` §3 expects 78 superseded-or-expired and
26 retracted forbidding records among the 104 obligations, from the attack-vector counts
(38 `AV1_superseded_preference`, 25 `AV4_multi_version_fact`, 15 `AV2_expired_logistics`,
26 `AV7_selective_forgetting`).

**Closed at Step 3 (2026-09-16).** The join disagrees with the attack-vector split: of the 104, the join marks **74 superseded-or-expired**, **8 retracted** and **22 unflagged** (no member marked non-active: 18 of the 26 AV7 retraction obligations and 4 of the 15 AV2 expiry obligations, the same 22 the downstream study reports as out of reach of any policy that acts on the metadata). The join's split is used: recall in AUX-R85-G10-CENSUS-FORBIDDING is over the 74, with the figure over the attack-vector 78 printed beside it; the 22 unflagged are outside both denominators and the 8 join-retracted print the marker. The unflagged items: frbank:bruna:bruna_q06:FULL, frbank:bruna:bruna_q06:CAT-ABLATED, frbank:bruna:bruna_q06:SLOT-ABLATED, frbank:dariush:dariush_q04:FULL, frbank:dariush:dariush_q04:SLOT-ABLATED, frbank:david:david_q06:FULL, frbank:david:david_q06:CAT-ABLATED, frbank:fatima:fatima_q06:FULL, frbank:fatima:fatima_q06:SLOT-ABLATED, frbank:ingrid:ingrid_q04:FULL, frbank:ingrid:ingrid_q04:CAT-ABLATED, frbank:ingrid:ingrid_q04:SLOT-ABLATED, frbank:joonho:joonho_q04:FULL, frbank:joonho:joonho_q04:SLOT-ABLATED, frbank:marcus:marcus_q10:FULL, frbank:marcus:marcus_q10:CAT-ABLATED, frbank:mirri:mirri_q04:CAT-ABLATED, frbank:rosa:rosa_q06:FULL, frbank:rosa:rosa_q06:CAT-ABLATED, frbank:rosa:rosa_q06:SLOT-ABLATED, frbank:valentina:valentina_q04:FULL, frbank:valentina:valentina_q04:SLOT-ABLATED.

**Done.** The build reads each obligation's `pn_members` state from the join
(`index_v2.true_lifecycle`) and asserts the 78 / 26 split. If the join disagrees, the join's
split is recorded here with the differing items, and it is the join's split that the census
and the table use. Conditional: this entry is closed at Step 3 either way, with the count.

**Why.** The paper's ground-truth tags are the join's, never the attack vector's; a denominator
the paper prints must come from the same source as the tags it is compared against.

---

## D-R85-13 — the three spike personas are re-ingested, not reused

**Written.** The G10 design offered reuse of the spike graphs (`r85stock_elena`, `r85stock_tom`,
`r85stock_yoli`, intact on `neo4j-r85` at Step 1 with 242, 221 and 222 edges, the spike's own
counts) as a $0.77 saving.

**Done.** All forty personas are ingested fresh under `r85g10_<persona>`, the three included.
The spike graphs are left untouched.

**Why.** The author's ruling of 15 September. The $0.77 buys a second graph for each spike
persona under the same pinned environment, so the forty-persona census prints their new rows
beside their trial rows as a descriptive extraction-repeatability check the paper can cite;
and the forty-persona run is then one run, on one day, under one version, with no persona
carried in from an earlier run. E.9's trial paragraph stays the trial record.

---

## D-R85-14 — an FR-Bank VIEW-UNTAGGED lane is added to the tag route

**Written.** The addendum registered no tag route; the amendment's tag route (§4 C) has three
Graphiti lanes, VIEW-UNTAGGED, VIEW-TAGGED and HYBRID. The main study has no untagged view on
FR-Bank: its recorded rows are RETRIEVED (the join's tags, 0.6851) and RETRIEVED-BELIEVED
(FR-Bank's own marks, 0.8144), both tagged.

**Done.** A fourth mini lane, 661 calls: the recorded `top5_ids` of `resp_review/l2/retrieval.json`
re-rendered with the `lifecycle:` field removed and nothing else changed, under the same untagged
prompt variant the Graphiti lane uses. Paired against the two recorded FR-Bank rows. Descriptive
on FR-Bank; P4's bar is on Graphiti. About $0.23 at the measured `AUX-RESP-A1-BELIEVED` rate.

**Why.** The author's ruling of 15 September. Without it P4 is a within-Graphiti statement and
the two stores' tag routes are not on the same footing; with it the paper can say whether
FR-Bank's tags carry signal over its own untagged view, which is the sentence the
tags-not-masks recommendation rests on.

---

## D-R85-15 — the group identifiers take the ingest script's own form

**Written.** Amendment 1 section 3 and section 8 step 2 name the group identifiers
`r85g10_<persona>`, section 4 C's retrieval call reads `group_ids=["r85g10_<persona>"]`, and
the amendment says `ingest.py` is "unchanged except for the group tag it already accepts".

**Done.** `ingest.py`'s tag mechanism builds the identifier as `f"r85{arm}_{persona}"` plus
`f"_{group_tag}"`, so `--arm stock --group-tag g10` yields `r85stock_<persona>_g10`, not
`r85g10_<persona>`. That form is adopted for all forty personas; `ingest.py` stays
byte-identical; wherever the amendment writes `r85g10_<persona>`, including section 4 C's
`group_ids`, it reads `r85stock_<persona>_g10`. The three spike graphs (`r85stock_<persona>`,
no tag) are distinct identifiers and are untouched (D-R85-13). The amendment file itself is
frozen (AUX-R85-G10-FREEZE) and is not edited; this entry amends it by reference. Step 1's
check of the namespace (AUX-R85-G10-ENV, "no `r85g10_*` groups") holds for the adopted form
too: no `*_g10` group exists on `neo4j-r85` before Step 2.

`ingest.py` also names its run record by `{arm}_{model}_{persona}` without the tag, so a
forty-persona run would write `stock_gpt-4.1-mini-2025-04-14_<persona>.json` and, for elena,
tom and yoli, overwrite the spike's committed records. The Step 2 runner
(`r85_graphiti/g10/ingest_all.py`) therefore moves each finished record to
`ingest_runs/g10_<persona>.json` (the amendment's name) and restores the three spike records
from `HEAD` after those personas; `ingest.py` is not changed for this either.

**Why.** The author's ruling of 15 September: "unchanged" is the independence argument, the
forty-persona run using the ingestion code the spike used byte for byte, and a cosmetic
identifier form is not worth spending it on.

## D-R85-16 — the forbidding-record census counts store-variant rows on a single graph; the FULL-variant reading prints first

**Written.** Amendment 1 section 4 A(ii) and P1 count the forbidding records over "the 78" (the
104 obligations of the committed 661, the attack-vector split), and the paper placement of
section 10 fills P1's text from that count.

**Found (2026-09-16, at integration; Amendment 2 section 0 records the same fact for the
summary and tag routes).** The 661 are 332 questions under three FR-Bank store variants (FULL,
CAT-ABLATED, SLOT-ABLATED), each variant a different FR-Bank store; every Graphiti graph is one
store per persona ingested from the whole bank (`render_episodes.py`), so it is the FULL store
for every item. Of the 104 obligation rows, 47 are FULL and 57 are variant rows of those same
47 questions; 48 of the 57 carry the FULL sibling's `pn_members` exactly, so the census counted
the same forbidding records on the same graph two or three times.

**Done.** `census_forbidding.py` and its record are unchanged. `g10/census_full_variant.py`
re-aggregates the recorded per-obligation rows on the 47 FULL-variant obligations (34
superseded-or-expired under the join: RECOVERED 13, STALE_ACTIVE 10, EXTRACTION_MISS 11, recall
0.3824) and, as a sensitivity, on the 56 distinct (persona, member-set) pairs (16 of 39, 0.4103);
bucket assignments agree across every shared member set. The paper's main text prints the
FULL-variant reading with its denominator stated; Appendix G.4 prints the registered 104-row
reading (30 of 74, 0.4054; 30 of 78) with the registered P1 FAILS text verbatim, the
FULL-variant reading and the distinct-member-set sensitivity beside it. P1's verdict is the same
under all three (recall above the registered quarter; precision 0.0669 holds). Precision is
over edges and is unaffected.

**Pending, the author's.** Amendment 2 section 0's count (230 of the 661 carry a label the full
store contradicts) bears on Steps 4 to 6 of Amendment 1, which have not run; the population
ruling for those steps is the author's and is not made here. This entry is recorded at the
integration pass for the author's ratification.


## D-R85-17 — Amendment 1 Steps 4 to 6 run on the 323 FULL-variant items; the 661 figure is not produced

**Written.** Amendment 1 registers the summary route (P2, P3, GR-1 to GR-5) and the tag route (P4)
on the 661 (section 4 B, section 4 C, section 5), and Amendment 2 section 0 records, before any
of those steps ran, that 230 of the 661 carry a NOK / FOK label the full store contradicts
(every Graphiti graph being the FULL store, D-R85-16). The population ruling was left the
author's.

**Done (the author's instruction of 2026-09-17, program R114).** Steps 4 to 6 run on the
**323 FULL-variant items** (145 ABSENT, 131 PRESENT, 47 obligations; positives 47; 28 personas
carry an obligation, 40 a licensed item), and every Graphiti row of Amendment 1 is read on the
323 with the FR-Bank comparators re-scored on the same 323 from their recorded per-item rows
(`AUX-R113-Z3-ROWS`, `-PAIRED`: INDEXED-TRUE 0.7424, BLIND 0.4964, RETRIEVED 0.6980, HYBRID 0.8855,
RETRIEVED-BELIEVED 0.8504; the embedding lookup 0.7434). P2's comparator is therefore the
recorded INDEXED-TRUE row on the 323, 0.7424, not the 661's 0.7339; P4's tolerance and P3's
0.50 are unchanged. The 661 figure (the registered form) is **not produced**: 338 of its items
are variant rows of the same questions on the same graph, of which 230 carry a label the graph
contradicts, and the instruction is explicit that the old 661-based call estimates are not
inherited. The tag route's FR-Bank VIEW-UNTAGGED lane (D-R85-14) runs on the same 323, from the
FULL items' recorded `top5_ids`. Where the paper prints an Amendment 1 number it states the
denominator (323 / 47) and this entry.

**Why.** A Graphiti row scored against a label the graph never saw would be a measurement of the
label, not the store; the 323 is the largest population on which the graph and the label agree,
and the FR-Bank comparators exist on it at $0 from recorded rows.

---

## D-R85-18 — Amendment 2 is frozen by sha256 in the ledger, not by commit

**Written.** Amendment 2's own text says "DRAFT until frozen by commit before the first billed
call" and its section 10 step 0 commits the file (pathspec only).

**Done.** The author's instruction of 2026-09-17 leaves every change of program R114
uncommitted for review. The amendment's freeze decisions (section 0 ruling per D-R85-17; the
second reader not named; the Haiku box not authorized in this pass; the section 11 dates; the M
line rule confirmed) are appended below a marker line in the amendment file, and the sha256 of
the whole file is recorded as `AUX-R85-A2-FREEZE` in `r85_graphiti/NUMBERS_R85.md` before any
Phase 3 call; the scripts assert that hash. The author's commit of the file as it stands closes
the freeze; an edit before that commit changes the hash and is a STOP.

**Why.** The hash gives the same integrity check a commit gives, without a commit the author has
not asked for.


## D-R85-19 — the lifted cap is 1,000, not 100; the readers' name lists are read by a section reader

**Written.** Amendment 1 section 4 B renders BELIEVED-lifted "with the cap lifted to 100 as
`side_experiments/tools/build_s2u.py` does for FR-Bank's S2-U rendering, so no `(+N more)`
truncation", and names NB-5 and NB-6 as "`run_nb6`'s committed functions".

**Found at Step 4 (2026-09-17).** (i) The forty Graphiti stores carry 100 to 211 distinct
attribute names in one bucket (category is inexpressible, so the whole map is one list), and
100 binds on every one of them; 1,000, the next power of ten, never binds, and is the cap
used for BELIEVED-lifted and TRUE-projected-lifted (`AUX-R85-G10-INDEXES`). The mechanism is
build_s2u's (the module constant `SLOT_CAP`), the value differs. (ii) The cap of 15 binds on
TRUE-projected's whole map in all forty personas (FR-Bank's slot names fall into one bucket
under `AVAIL_GRAPHITI`), so TRUE-projected-lifted is added as section 4 B itself provides.
(iii) `index_features.parse`, the parser `run_nb6.name_lists` reads through, marks any text
containing the marker string inexpressible and reads names only under an `ATTRIBUTE NAMES BY
CATEGORY` header; on a Graphiti rendering (marker on category and retracted; a single
`ATTRIBUTE NAMES` list) it returns two empty lists. The name lists are therefore read by
`g10/build_indexes.read_names`, a section reader over the same two headers `index_v2.render`
emits, asserted on every text to equal the slot sets the text was rendered from and, for the
capped superseded section, the census record's `superseded_names`. The similarity and
estimator functions (`run_nb6.emb_scores`, `lex_scores`, the encoder, `common_e1r.auroc`) are the
committed ones, unchanged.

**Why.** A reader that returned empty lists would print 0.50 for every persona and read as a
finding about the store; the lists exist and the registered readers are meant to read them.


## D-R85-20 — the stock search returns fewer than ten edges on three of the 323 items, none on one

**Written.** Amendment 1 section 4 C: "top 10 taken, top 5 used".

**Found at Step 5 (2026-09-17).** `EDGE_HYBRID_SEARCH_RRF` as shipped in 0.28.1 carries `sim_min_score` 0.6 on its cosine leg and
BM25 may match nothing, so the union can hold fewer than ten edges: 320 of 323 items return ten, `frbank:billy:billy_q05:FULL` six,
`probe:frbank:pan:72345311` nine and `probe:frbank:kofi:38156792` none (deterministic on a repeat search; the persona's graph holds
229 edges). RULE 3 keeps the stock configuration, so the view is the lines returned: the two ABSENT probe items carry a nine-line
and an empty retrieval, the PRESENT item six lines (five used). The empty view runs through every lane as an empty fenced block;
the population is not changed. Amendment 2's views on the 178 are unaffected except billy_q05 (M draws from six lines).

**Why.** The registration's "ten" describes the request, not a guarantee the store makes; a store that returns nothing is a
store output, and the item stays in the denominator.
