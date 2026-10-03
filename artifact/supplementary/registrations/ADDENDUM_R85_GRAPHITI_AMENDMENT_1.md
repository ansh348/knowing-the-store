# ADDENDUM R85-GRAPHITI — Amendment 1: the forty-persona run and the tag route

**DRAFT until frozen by commit before the first billed call.** Written 2026-09-15 from the
author's decisions of the same day on the "G10" design, after that design was corrected
against the R85 record (`r85_graphiti/SPIKE_REPORT.md`, `FREEZE.md`, `PERSONAS.md`). Nothing
below has been ingested, retrieved or scored. The registration this amends is
`registrations/ADDENDUM_R85_GRAPHITI.md` (frozen `ca522b0`; spike `1ec6184`; billing `f2d7688`).

Deviations continue the `D-R85-n` series in `r85_graphiti/DEVIATIONS_R85.md`, from `D-R85-12`.
Ledger keys are `AUX-R85-G10-*` in `r85_graphiti/NUMBERS_R85.md` (new file). No edit to
`CLAIMS.md` happens before integration; the R85 block is prepared as a diff, as the addendum said.

---

## §1 Disposition of the lapsed cutoff

The addendum's §9 set scoring by 10 September 12:00 local and integration by 12 September, and
said a miss "sends every committed artifact to the October rebuttal card verbatim under the R85
name, and releases the reserved main-text lines." Both dates were missed. The reason is recorded
plainly: the writing pass (program R111, Phases 0 to 4c, 15 September) took the window, and no
R85 step was attempted between `f2d7688` (30 August) and this amendment.

What that clause did and did not do:

- The reserved main-text lines **were released.** The v19 base ends its main text at page census
  reading 485, the boundary (`reviews/v19/gates_v19_base.txt`). The one §7 sentence this
  amendment lands is therefore a swap inside §7, not slack (§10).
- **No artifact changed.** `r85_graphiti/` is unchanged since `f2d7688`; the freeze commit of this
  amendment records the tree hash so that statement is checkable rather than asserted.
- The rebuttal-card routing is **superseded by this amendment.** The program re-registers with
  the cutoffs in §9 below and stays under the R85 name. It is neither a fresh program nor
  rebuttal-only material.

## §2 Inherited verbatim

Everything the addendum froze that this amendment does not name is inherited unchanged. Named
because the G10 design as first proposed would have contradicted them:

| Inherited | Where | What the proposal had, and why it is not adopted |
|---|---|---|
| RULE 1, lifecycle derivation | `graphiti_index.py` RULE 1 | The proposal mapped "invalidated, no successor" to RETRACTED. RULE 1 puts it under EXPIRED and freezes RETRACTED as inexpressible, emitting the marker, and Appendix E.9 already prints "Retraction and category are inexpressible under its stock defaults" with the 13 / 63 superseded / expired split. **No retraction proxy is added, not even as a secondary reading**; the inexpressibility of retraction is the finding. |
| RULE 2, attribute naming | `graphiti_index.py` RULE 2 | Unchanged. Names are relation type joined with the target label; every stock node carries the default label, so names reduce to relation types, and that prints as the naming-granularity finding. |
| RULE 3, stock defaults | `graphiti_index.py` RULE 3 | The proposal specified "embedding-only search, no LLM reranker." Stock `Graphiti.search()` in the pinned 0.28.1 is `EDGE_HYBRID_SEARCH_RRF` (BM25 + cosine, reciprocal-rank fusion, no reranker, `graphiti_core/graphiti.py:1332`, `search/search_config_recipes.py:111`). **Retrieval is the stock hybrid**, because a non-default search configuration would be co-design of the second backend. |
| Episode rendering, one per session, reference time `created_at`, no labels | `render_episodes.py`, D-R85-1 | Unchanged. |
| Ground truth is the persona manifest | `PERSONAS.md`, D-R85-2 | Unchanged. |
| Environment and pins | `ENVIRONMENT.md`, D-R85-3, D-R85-7, D-R85-8 | Unchanged: stock venv `AppData\Local\r85_stock_venv`, `graphiti-core==0.28.1`, `openai==2.24.0`, `neo4j==6.1.0`, container `neo4j-r85` on bolt 7688. The venv is present on 15 September; the container's state is Step 1's first check, Docker Desktop being down at the time of writing. |
| Extractor `gpt-4.1-mini-2025-04-14`, embedder `text-embedding-3-small` | D-R85-6, `SPIKE_REPORT.md` | Unchanged; mini pinned on the spike's measurements. |
| Frozen readings GR-1 to GR-5 with their hold and fail texts | addendum §7 | Inherited and read at forty personas. GR-1 (the paired NOK difference on BELIEVED excludes zero) is a statement of existence; P2 below is a statement of magnitude; both print. |
| Leakage threshold, more than 3 of 30 PRESENT items answered from the index alone | `leakage.py` | Inherited; the 30-item screen the spike could not draw runs at forty personas (§4 D). |
| Opus 5 registered as dropped at $60.13 | addendum §6 | Unchanged. |
| The ten-persona subset and the "most obligations" rule | proposal only | **Not adopted.** All forty personas run, as the addendum registered. The top ten by obligation count would carry 53 of the 104 obligations at a 27% base rate against 16% on the 661, and 12 personas carry none; a subset control becomes unnecessary once the population is the registered one. |

## §3 Population and ingestion

**Questions, labels and clock: the committed FR-Bank population, byte-identical.** NOK n = 661
(104 PRESENT-NEGATIVE, 383 ABSENT, 174 PRESENT) over 40 personas; FOK hard tier n = 307, a
subset scored from the same elicitation. Per-persona counts from `e1_metamemory/build/items_final.json`:
28 personas carry at least one obligation, 12 carry none; the largest is elena at 8.

**The forbidding records.** Each obligation's `pn_members` are FR-Bank record identifiers whose
ground-truth state is read from the join (`index_v2.true_lifecycle`), never from the attack
vector. The attack-vector split of the 104 is 38 `AV1_superseded_preference`, 25
`AV4_multi_version_fact`, 15 `AV2_expired_logistics`, 26 `AV7_selective_forgetting`; the expected
state split is therefore **78 superseded-or-expired and 26 retracted**, and the build asserts the
join agrees with that or records the difference as `D-R85-12`. The 26 retracted print the marker on
every Graphiti row; recall and precision in §4 A(ii) are over the 78.

**Persona clock.** `t_now` per persona is the pinned constant of `e0_common.PersonaJoin` (the
latest active record plus 24 hours, from the full bank). Graphiti states are read from the dump
after the whole session stream, which is the state at the clock; the count of edges whose
`valid_at` or `invalid_at` lies after `t_now` prints beside the census.

**Ingestion.** All forty personas, fresh, into group identifiers `r85g10_<persona>` on the
`neo4j-r85` instance, with the three spike graphs (`r85stock_<persona>`) left untouched. 1,365
episodes at one per session (`FREEZE.md` corpus table). Eight-way persona parallelism, falling
back to four-way on rate limiting; the fallback is logistics and is logged, not a deviation.
`ingest.py` unchanged except for the group tag it already accepts.

Fresh ingestion of the three spike personas is the author's ruling of 15 September and is
`D-R85-13`: it costs $0.77 more than reusing the spike graphs (103 episodes at the anchor rate),
and buys a second graph for elena, tom and yoli, so their forty-persona census rows print beside
their trial rows as a descriptive extraction-repeatability check the paper can cite, no bar.
Reuse is not adopted. The trial paragraph in E.9 stays the trial record.

### Deviations registered by this amendment

Entered into `r85_graphiti/DEVIATIONS_R85.md` verbatim at Step 1, after the freeze commit (which
is this file alone) and before any billed call other than the identifier probe.

- **D-R85-12** (conditional): the forbidding-record state split is expected to be 78
  superseded-or-expired and 26 retracted from the attack vectors; the build reads the join and,
  if it disagrees, records the join's split here and uses it.
- **D-R85-13**: the three spike personas are re-ingested under new group identifiers rather than
  reused, at $0.77, for the repeatability rows; the author's ruling.
- **D-R85-14**: an FR-Bank VIEW-UNTAGGED lane is added to the tag route (§4 C) so the two stores'
  tag routes stand on the same footing; the author's ruling, about $0.23.

## §4 Measurements

### A. Census at forty personas (no API call)

(i) **The R85 census as frozen**, `census.py` per persona over the 109 MIN_DISCR-filtered
manifest supersession events: buckets RECOVERED / STALE_ACTIVE / EXTRACTION_MISS, recall at the
frozen τ = 0.80 with the 0.75 and 0.50 bands, precision as explained-invalidated over all
invalidated edges, the entity-fragmentation and undated-edge counts. No new bar: the frozen gate
was the spike's. The trial's 0.20 is the reference figure and GR-5 names the failure mode from
this census.

(ii) **The forbidding-record census**, new (`g10/census_forbidding.py`): for each of the 78
superseded-or-expired obligations, the study's own detector (`e0_common.PersonaJoin.detector`
transposed onto edge facts, as `census.py` does) fires on the Graphiti edges at τ = 0.80 against
the forbidding record's text; RECOVERED if any firing edge is non-active under RULE 1,
STALE_ACTIVE if edges fire and all are active, EXTRACTION_MISS if none fires. Recall =
RECOVERED / 78. Precision = the share of Graphiti's non-active edges, over all forty graphs, that
fire on a record the join marks non-active. Both denominators print. Retraction's 26 print the
marker.

### B. Summary route

Three indexes per persona, all through `index_v2.render` under `AVAIL_GRAPHITI`, marker on
category and retracted:

- **BELIEVED-capped**, Graphiti's own fields under RULES 1 and 2, `SLOT_CAP = 15` (the renderer as
  frozen);
- **BELIEVED-lifted**, the same rows with the cap lifted to 100 as `side_experiments/tools/build_s2u.py`
  does for FR-Bank's S2-U rendering, so no `(+N more)` truncation; the largest list prints;
- **TRUE-projected**, the ground-truth join's rows projected onto what Graphiti's schema expresses
  (`AVAIL_GRAPHITI`), addendum §3. The cap is asserted not to bind on it, and if it does the lifted
  form is added and recorded.

**Monitor:** GPT-4.1 mini, the main-study protocol (`prompts_e1`, temperature 0, seed 42,
`max_tokens` 200, one call), on the 661 under each of the three indexes: 1,983 calls. **The blind
row and the ground-truth-summary row are reused from the record, not re-run**; blind does not
depend on the backend, and the FR-Bank TRUE row is the comparator.

**Readers, $0:** the superseded-names matcher (NB-6, embedding variant, `run_nb6`'s committed
functions) over Graphiti's superseded list under both renderings; the whole-map matcher (NB-5).

### C. Tag route (new module, `r85_graphiti/g10/`)

**Retrieval.** Per item, stock `Graphiti.search(question, group_ids=["r85g10_<persona>"],
num_results=10)`: `EDGE_HYBRID_SEARCH_RRF`, default `SearchFilters()`, so invalidated and expired
edges are returned; top 10 taken, top 5 used, mirroring `resp_review/tools/build_l2.py`. The
query embedding is Graphiti's own `text-embedding-3-small` call.

**Line format**, one line per edge in rank order, the FR-Bank format of `build_l2.py` with the
backend's own fields:

```
[r] lifecycle: <superseded | expired | active> | category: not expressible by this backend | attribute: <RULE 2 name> | age: <days before t_now from valid_at, D-R85-10> | text: <edge.fact>
```

The lifecycle field is the RULE 1 state. RETRACTED never appears, by RULE 1. The **untagged**
line is the same line with the `lifecycle:` field removed and nothing else changed, so the two
views differ in exactly the tag.

**Lanes, GPT-4.1 mini, one call each, 661 items:**

| Lane | View | Summary | Prompt |
|---|---|---|---|
| VIEW-UNTAGGED | five lines, no lifecycle field | none | `prompts_resp.SYSTEM_RETRIEVED` / `USER_RETRIEVED` with the phrase "each with the lifecycle metadata the store records" replaced by "each with the metadata the store records", constructed by one asserted `str.replace` and hashed (`AUX-R85-G10-PROMPTS`) |
| VIEW-TAGGED | five lines with the lifecycle field | none | `prompts_resp.SYSTEM_RETRIEVED` / `USER_RETRIEVED`, unchanged |
| HYBRID | five tagged lines | BELIEVED-capped | `prompts_resp.SYSTEM_RETRIEVED` / `USER_HYBRID`, unchanged |

**Reach, descriptive:** the share of the 104 obligations whose forbidding record is asserted by
one of the five retrieved edges (detector at τ = 0.80 on the fact string), the analogue of
`AUX-RESP-L2-REACH` (FR-Bank k = 5), per state; and over the forbidding records in view, the
store's non-active mark against the join's (tp / fp / fn / tn), the analogue of `AUX-RESP-A1-TAGS`.
No bar.

**FR-Bank VIEW-UNTAGGED, registered (D-R85-14):** the same lane on FR-Bank, 661 mini calls on
`resp_review/l2/retrieval.json`'s recorded `top5_ids` re-rendered with the `lifecycle:` field
removed and nothing else changed, under the same untagged prompt variant. It is paired against
the recorded RETRIEVED row (the join's tags, $0.6851$) and the recorded RETRIEVED-BELIEVED row
(FR-Bank's own marks, $0.8144$). Without it P4 is a within-Graphiti statement; with it the paper
can say whether FR-Bank's tags carry signal over its own untagged view, which is the sentence the
tags-not-masks recommendation rests on. Descriptive on FR-Bank, no bar; it prints in the same
table.

**Build checkpoint (22 September):** before any tag-route monitor call, five rendered Graphiti
views and five FR-Bank untagged views, chosen by a seeded draw, are checked by eye against the
FR-Bank view format of `build_l2.py` (field order, the marker on category, the age arithmetic, the
untagged line differing from the tagged in exactly the `lifecycle:` field) and the check is
recorded. A rendering fault is found here, before it costs 2,644 calls.

### D. Leakage screen (the 30-item screen, inherited)

`leakage.py` at forty personas: 30 PRESENT items drawn by the frozen rule, the monitor asked to
answer from the BELIEVED-capped index alone; the frozen threshold is more than 3 of 30 correct.
A failure stops the summary-route lanes until the leak is located and recorded.

### E. Haiku 4.5 at k = 5, conditional (§7)

The summary route only, BELIEVED-capped only, Message Batches API, `claude-haiku-4-5-20251001`,
temperature 0, five draws, the addendum's lane. It runs last and only under the rule in §7.
"Does a larger model rescue Graphiti's metadata" is the number to drop if money runs out.

## §5 Registered predictions

Written before the first ingestion call. Each holds or fails on the forty-persona figures; the
placeholders resolve to `AUX-R85-G10-*` keys at print time. Tolerance is ±0.05 throughout, the
study's count-destruction tolerance (`ADDENDUM_RESP.md`).

**P1, census.** On the 78 superseded-or-expired forbidding records, Graphiti's recall is at or
below 0.25 and its precision at or below 0.10, the direction of the three-persona trial (0.20 and
0.00 to 0.04 on the manifest events).
> HOLDS: Over the forty personas Graphiti marks $R$ of the $78$ forbidding records non-active, and
> $P$ of the edges it marks non-active correspond to a record the ground truth marks non-active.
> FAILS: Over the forty personas Graphiti reaches $R$ of the $78$ forbidding records, above the
> registered quarter, at precision $P$.

**P2, summary route.** A comparison of two indexed rows on the same 661 questions: GPT-4.1 mini
under the BELIEVED-capped Graphiti summary against GPT-4.1 mini under the ground-truth summary
(the recorded INDEXED-TRUE row, $0.7339$). The criterion is the paired difference: the Graphiti
row falls below the ground-truth row by more than the tolerance, with the item-level paired
interval excluding zero. **The blind row is not in the criterion.** It prints beside the two
indexed rows from the record, with the paper's caveat that GPT-4.1 mini's blind score is one value
on 604 of the 661, so Section 4 does not report an indexed-minus-blind difference as a gain for
this model. GR-4's descriptive fraction of $+0.2393$ prints on its own row under that caveat. The
lifted rendering and the TRUE-projected index print beside the capped row, no bar. The
name-lookup clause is P3's value, printed in the same sentence.
> HOLDS: Under Graphiti's store-written summary GPT-4.1 mini reads $G$ against $T$ under the
> ground-truth summary on the same questions, $D$ below with interval $I$; a matcher reading
> Graphiti's own list of superseded names reads $Y$.
> FAILS: Under Graphiti's store-written summary GPT-4.1 mini reads $G$ against $T$ under the
> ground-truth summary on the same questions, within tolerance or above it, interval $I$; a
> matcher reading Graphiti's own list of superseded names reads $Y$.

**P3, lookup.** The superseded-names matcher over Graphiti's superseded list is within ±0.05 of
0.50, under both renderings.
> HOLDS: A matcher reading Graphiti's own list of superseded names reaches $Y$, within tolerance
> of chance.
> FAILS: A matcher reading Graphiti's own list of superseded names reaches $Y$, $D$ from chance.

**P4, tag route.** GPT-4.1 mini on VIEW-TAGGED is within ±0.05 of GPT-4.1 mini on VIEW-UNTAGGED
on the 661, because the recall in P1 is too low for the tags to carry anything.
> HOLDS: Shown the five retrieved edges with Graphiti's own states, GPT-4.1 mini reads $T$ against
> $U$ without them, within tolerance: the states this store writes do not reach the records that
> forbid use.
> FAILS: Shown the five retrieved edges with Graphiti's own states, GPT-4.1 mini reads $T$ against
> $U$ without them, $D$ apart with interval $I$.

HYBRID prints descriptively against VIEW-TAGGED and against the BELIEVED-capped summary alone, as
`L2-P2` does for FR-Bank; no bar. GR-1 to GR-5 print under their frozen texts.

**Not-applicable convention**, inherited: a row that cannot be computed prints a dash with a
footnote; an empty row is never left to be read as zero.

## §6 Analysis

AUROC over the 661 (positives the 104), and over the state subsets as the record does
(supersession 620 / 63, expiry 572 / 15; retraction's 583 / 26 prints the marker). Paired
bootstrap, 1,000 draws, seed 42, item-level and persona-clustered with forty clusters, the
`score_cf.py` / `verify_resp.py` functions. Two-decimal print forms ledgered in
`r85_graphiti/NUMBERS_R85.md` beside their four-decimal sources, `AUX-R85-G10-PRINTED`. Every
deviation from this text is a `D-R85-n` entry before the number it affects prints.

## §7 Budget, from measured anchors

Every expected figure below is a measured per-unit rate in a committed artifact times a count
in this registration. Worst case applies 1.3× to each G10 line.

| Line | Units | Anchor | Where measured | Expected | Worst |
|---|---|---|---|---|---|
| Ingestion, all forty, mini + embedder | 1,365 episodes | $0.00745 / episode | `SPIKE_REPORT.md`, three stock mini arms, 103 episodes | **$10.17** | $13.22 |
| Summary route, mini, 3 indexes | 1,983 calls | $0.45 / 661 calls | addendum §5 (R82 per-call) | $1.36 | $1.77 |
| Tag route, mini: VIEW-UNTAGGED, VIEW-TAGGED | 1,322 calls | $0.2310 / 661 | `AUX-RESP-A1-BELIEVED` (754 in / 26 out) | $0.46 | $0.60 |
| Tag route, mini: HYBRID | 661 calls | $0.45 + $0.23, an upper bound | the two anchors above | $0.68 | $0.88 |
| Tag route, mini: FR-Bank VIEW-UNTAGGED (D-R85-14) | 661 calls | $0.2310 / 661 | `AUX-RESP-A1-BELIEVED` | $0.23 | $0.30 |
| Leakage screen, probes, query embeddings | 30 + ~5 calls; 661 embeddings | list price | — | $0.03 | $0.04 |
| Readers NB-5, NB-6 | — | local, offline | — | $0.00 | $0.00 |
| **G10 subtotal** | | | | **$12.93** | **$16.81** |
| X3 and X1, outside this registration | | the author's figure, not measured here | — | $5.00 | $5.00 |
| **Running total before Haiku** | | | | **$17.93** | **$21.81** |
| Haiku 4.5, k = 5, BELIEVED-capped, Batch | 3,305 rows | $4.44 | addendum §5, list price with the Batches discount | $4.44 | $4.44 |
| **Total if Haiku runs** | | | | **$22.37** | **$26.25** |

**The Haiku rule, as the author set it and confirmed on 15 September:** Haiku runs if and only
if the billed total at that point plus $4.44 is at or under $20.00, i.e. the billed total is at or
under **$15.56**. At the measured anchors it is **not** met: it requires G10 and X1/X3 together to
under-run their expected figures by $2.37 (for instance X1 and X3 at $2.63 or less). The rule is
arithmetic on billed rows, evaluated once, after X1 and X3; it is not re-partitioned to make
Haiku fit, and the expected outcome is that Haiku is dropped and recorded with its price. The
author was told which row the cap costs: FR-Bank's Haiku retention of 72 percent is the most-cited
figure of the own-metadata result, and its Graphiti counterpart is the row that would make "a
larger model rescues thin metadata" a two-store claim. Raising the cap to $26 before the freeze
would admit it; the author did not, and that is the correct outcome under a $20 cap.

**Stop rules.** Ingestion stop at $13.22 (1.3× the anchor); the addendum's $28 stop is not
approached and is retained as the outer bound. A running total prints after every step in §8.

**Billing paths**, unchanged from `f2d7688`: OpenAI metered key for ingestion, embeddings and
every mini call (the path that emits `tok_in`, `tok_out`, `usd` per row); Anthropic metered key for
Haiku through Batches. Identifier probes run once before the first billed call of each provider
and the served identifier is recorded beside every cost line.

## §8 Order of execution

Each numbered step ends with a report and a hard stop for the author's go-ahead; the running
billed total prints at every stop.

0. **Freeze.** Commit this file (pathspec only, this file and nothing else), record its sha256 and
   the `r85_graphiti/` tree hash in `r85_graphiti/NUMBERS_R85.md` (`AUX-R85-G10-FREEZE`). No call.
1. **Environment.** Start Docker Desktop; report `neo4j-r85`'s state and whether the three spike
   groups are present (node counts per `r85stock_*` group). Identifier probe on the OpenAI key.
   Under $0.01.
2. **Ingest all forty** into `r85g10_<persona>`; per-persona cost and wall rows to
   `ingest_runs/g10_*.json`; running total. Expected $10.17, stop at $13.22.
3. **Census** (i) and (ii), the future-dated-edge count, the repeatability rows for the three
   spike personas. No call. P1 reads.
4. **Indexes and the summary route**: the three indexes, the leakage screen (§4 D) first, then the
   1,983 mini calls, then NB-5 / NB-6. P2, P3, GR-1 to GR-5 read.
5. **Tag route build**: retrieval for the 661, the three Graphiti blocks and the FR-Bank untagged
   block, the prompt variant and its digest, reach; no monitor call yet. Report the reach, the tag
   census, and the **22 September checkpoint**: ten rendered views checked by eye (§4 C) and the
   check recorded, before Step 6 is asked for.
6. **Tag route lanes**: the 2,644 mini calls (three Graphiti lanes and the FR-Bank untagged lane).
   P4 reads; HYBRID and the FR-Bank lane print.
7. **X3 and X1** run under their own registrations; their billed rows enter the running total.
8. **Haiku**, if and only if §7's rule holds on the billed total.
9. **Ruling and paper** (§10). Nothing touches `paper_v19.tex` before the author's ruling on
   the results.

## §9 Cutoffs

| Milestone | By (local) | If missed |
|---|---|---|
| Steps 1 to 3: ingestion and census | 21 September 23:59 | the whole amendment goes to the October rebuttal card under the R85 name |
| Step 4: summary route scored | 22 September 23:59 | as above |
| Step 5 checkpoint: ten views checked by eye, recorded | 22 September 23:59 | Step 6 does not start until it is |
| Steps 5 to 6: tag route built and scored | **23 September 23:59** | **the tag route alone goes to the rebuttal card; census and summary route still land** |
| Step 8: Haiku | 23 September 23:59 | dropped, recorded with its price |
| Integration | on the author's ruling | — |

## §10 Paper

One sentence in Section 7's census paragraph, of the form the author gave: "On Graphiti, whose
validity intervals are the closest thing to lifecycle tags in a shipped store, forty personas
give the same picture (Appendix G.x): ...", with the numbers filled from the ledger. The main text
sits at reading 485, the boundary, so the sentence is a swap inside Section 7 and the report
names the line that went.

One table in Appendix G with the mapping (RULE 1) stated in full above it and rows: census
recall and precision on the 78 with the manifest-event census beside it; the summary route
(BELIEVED-capped, BELIEVED-lifted, TRUE-projected, the lookup under both renderings, the blind
and ground-truth comparators from the record); the tag route (VIEW-UNTAGGED, VIEW-TAGGED, HYBRID,
reach); Haiku's row or its dash. Each with item-level and persona-grouped intervals.

E.9's trial paragraph stays as the trial record. Its last sentence, "Its tag route at trial scale
is left for the discussion period," is no longer true once §4 C lands. The rule, the author's
ruling: `frozen_diff.py` decides at integration whether the sentence sits inside a registered
block. If it does not, the sentence is replaced with the result and a pointer to Appendix G. If it
does, it stays verbatim and the result is appended immediately after it in "since run" wording,
so the appendix never prints a deferral that the same page contradicts without saying so.

The table also carries the FR-Bank VIEW-UNTAGGED row (D-R85-14) beside the recorded RETRIEVED
and RETRIEVED-BELIEVED rows, so the tag routes of the two stores print on the same footing.

## §11 Files

- `r85_graphiti/g10/`: `census_forbidding.py`, `build_indexes.py`, `run_summary.py`,
  `retrieve.py`, `run_view.py`, `score_g10.py`, `leakage30.py`, `README.md`. The R85 Phase 0 and
  Phase 1 tools (`render_episodes.py`, `ingest.py`, `census.py`, `leakage.py`,
  `graphiti_index.py`) are imported, not copied or edited, except the group tag `ingest.py`
  already takes.
- Ledgers: `r85_graphiti/NUMBERS_R85.md` (new), `r85_graphiti/DEVIATIONS_R85.md` (continues from
  D-R85-12), `r85_graphiti/DISCLOSURE.md` (unchanged).
- Review mapping: the single-backend objection, the names-only reading under NOK, and the
  inexpressibility-marker ablation are the items this amendment answers in the second mock review
  of the 4c build, to be filed as `reviews/v18/REVIEW_MOCK.md`; until it is filed they are mapped by
  content, not by number (the in-repo `REVIEW_10_v17.md` numbers the single-backend objection W4).
- Phase 5 of the writing pass is untouched; G10 runs beside it in `r85_graphiti/`.
