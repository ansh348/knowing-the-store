# R85-GRAPHITI — Phase 0 freeze

Everything below is frozen at the R85-0 commit, before any Graphiti graph exists and before
any billed call. A dump that contradicts a rule below is a Phase 1 finding with its own
deviation entry, never a reason to edit the rule.

## Frozen rules

| Rule | Where it lives | One line |
|---|---|---|
| Lifecycle derivation | `graphiti_index.py` RULE 1 | ACTIVE / SUPERSEDED / EXPIRED from the edge temporal fields; RETRACTED emits the marker |
| Attribute naming | `graphiti_index.py` RULE 2 | relation type joined with the target node's label; never a node name, never the fact |
| Stock defaults | `graphiti_index.py` RULE 3 | no custom entity types, no custom edge types, no custom prompts |
| Episode rendering | `render_episodes.py` | one episode per session, reference time is `created_at`, no injected dates, no labels |
| Ground truth | `PERSONAS.md` | the persona manifest, never FR-Bank's own `supersedes` links |

The clause "or Graphiti's own contradiction pointer targets this edge" is **struck**.
Graphiti stores no such pointer: the superseding edge's identifier is discarded and a search
of the whole upstream package for `superseded_by`, `invalidated_by` and `contradicted_by`
returns nothing.

## The exit gate

Evaluated once, on the three personas jointly.

- (a) At least one attribute name lands on a superseded-names list derived from Graphiti's
  own fields.
- (b) Supersession recall ≥ 0.50 against the manifest denominator.

**Denominator: 10 manifest supersession events** (elena 3, tom 3, yoli 4), all of which
survive the `MIN_DISCR` filter that the published census uses. Granularity is 1/10, so the
bar is **5 of 10 recovered**. Both the count and the granularity print whichever way the
gate fires.

**Within-session share: 0 of 109, 0.0%.** Graphiti invalidates only on a strict `valid_at`
ordering, so a same-session event would be unexpressible here. No manifest event is
same-session, so the schema limit does not reach the gate.

Branches, as registered: PASS proceeds; fields populated with recall below 0.50 is the
erase-or-overstate branch and also proceeds, because a lifecycle-bearing backend that fails
to describe itself is what the thesis predicts; degenerate stops the program and sends it
to the October card.

## Corpus, measured

| | Value |
|---|---|
| Personas | 40 |
| Records | 18,936 |
| Episodes at one per session | 1,365 |
| Mean episode body | 1,073 characters, about 268 tokens |
| Spike episodes | 206 |
| Rendered-corpus hashes | elena `b775dc2aef488669`, tom `3f83065049944f5d`, yoli `307a40d478b43def` |

The leak guard passes on all 40 banks: no bank field name, no record identifier, and no
lifecycle state token reaches any rendered episode.

## Itemised spike price, ceiling $8

Two independent anchors agree. The repository's own measured figure is $0.014 per session
(`r82_counterfactual/PLAN.md:419-426`); a bottom-up estimate at `gpt-4.1-mini` over
Graphiti's extract, dedupe and invalidate chain gives about $0.017 per episode.

| Arm | Episodes | At $0.017 |
|---|---|---|
| elena, unmodified, mini | 34 | $0.58 |
| elena, unmodified, nano | 34 | $0.15 |
| tom, unmodified, mini | 35 | $0.60 |
| yoli, unmodified, mini | 34 | $0.58 |
| elena and tom, modified, mini | 69 | $1.17 |
| Embeddings | | under $0.05 |
| **Total** | **206** | **about $3.10** |

$8 is a ceiling and not a target. The projection comes in near $3, which is stated here so
that the ceiling is not read as a budget to spend.

## Re-partitioned full-run budget, ceiling $45

The original $17 ingestion sub-ceiling predated both anchors. The 40-persona projection is
1,365 episodes: about $19 at the repository anchor, about $23 bottom-up.

| Line | Amount |
|---|---|
| Ingestion sub-ceiling | $24 |
| Ingestion stop rule | $28 |
| Monitors | $15 |
| Opus 5 at k=5 | registered as dropped, **$60.13** measured |

Monitor lanes, with call counts corrected: the FOK hard tier (n=307) is a **subset** of the
NOK population (n=661) and both judgments score from the same elicitation, so a lane costs
661 calls per provenance, not 968. `gpt-4.1-mini` on both provenances is 1,322 calls at
$0.91; Haiku 4.5 at k=5 on BELIEVED only is 3,305 calls at $4.44. Haiku on TRUE-projected is
added only if billed ingestion leaves room under $45. See the billing table below for the
per-arm breakdown.

## Extractor, priced rather than chosen

`gpt-4.1-mini-2025-04-14` is pinned for the full run unless **both** hold: nano's
entity-level recall against the manifest is within 0.05 of mini's on elena, **and** mini's
measured 40-persona projection exceeds $24. With the sub-ceiling re-partitioned to $24 the
second condition is unlikely to fire, so nano's elena run prints as a cost and quality line
rather than as a hinge. The deviation from the registered "cheapest configured model" is
recorded either way.

## Billing paths, per arm

Emitted by `tools/billing_table.py` from measured per-call and per-episode figures held in
committed artifacts. The Anthropic rows reconcile against list price with the Batches 50%
discount, and the tool asserts that reconciliation.

| Arm | Provider | Exact model identifier | Billing path | Key name in `.env` | USD | Ceiling |
|---|---|---|---|---|---|---|
| Graphiti ingestion, extractor | OpenAI | `gpt-4.1-mini-2025-04-14` | metered API key | `OPENAI_API_KEY` | 10.14 | $28 ingestion stop |
| Graphiti ingestion, embedder | OpenAI | `text-embedding-3-small` | metered API key | `OPENAI_API_KEY` | 0.01 | $28 ingestion stop |
| Monitor, mini, BELIEVED | OpenAI | `gpt-4.1-mini-2025-04-14` | metered API key | `OPENAI_API_KEY` | 0.45 | $15 monitors |
| Monitor, mini, TRUE-projected | OpenAI | `gpt-4.1-mini-2025-04-14` | metered API key | `OPENAI_API_KEY` | 0.45 | $15 monitors |
| Monitor, Haiku 4.5 k=5, BELIEVED | Anthropic | `claude-haiku-4-5-20251001` | Batch API, metered | `ANTHROPIC_API_KEY` | 4.44 | $15 monitors |
| Monitor, Haiku 4.5 k=5, TRUE-projected | Anthropic | `claude-haiku-4-5-20251001` | Batch API, metered | `ANTHROPIC_API_KEY` | 4.44 | $15 monitors, conditional |
| Reader NB-5 | local | `all-MiniLM-L6-v2` | local, offline | none | 0.00 | none |
| Reader NB-6 | local | `all-MiniLM-L6-v2` | local, offline | none | 0.00 | none |
| Monitor, Opus 5 k=5, both provenances | Anthropic | `claude-opus-5` | Batch API, metered | `ANTHROPIC_API_KEY` | 60.13 | **DROPPED** |

| Account | Expected | Worst case |
|---|---|---|
| `OPENAI_API_KEY` | $11.06 | $14.11 |
| `ANTHROPIC_API_KEY` | $4.44 | $8.88 |
| **Both, against $45** | **$15.50** | **$22.99** |

The mini lane bills the metered key rather than the installed `codex-cli 0.147.0`, because
R82 billed it that way and that path emits per-call `tok_in`, `tok_out` and `usd` while a
subscription route emits none. The lane costs $0.91; the ledger is worth more than that.
Ingestion has no subscription route at all, since `graphiti-core` calls the API from inside
the library.

**Probes, 2026-08-30T11:59:30Z, artifact `billing_probe.json`:** `OPENAI_API_KEY` PASS, one
call, served `gpt-4.1-mini-2025-04-14`. `ANTHROPIC_API_KEY` PASS, one call, served
`claude-haiku-4-5-20251001`; a zero-balance organization returns `400 credit_balance_too_low`
on that path, so the succeeding call is the confirmation that the Batch submission is funded.

**Correction carried into this table.** An earlier pre-flight priced Opus 5 at about $180 by
applying a $15 per MTok input rate. The rate is $5 in and $25 out, and R82's own rows measure
$0.009096 per call. Opus 5 at k = 5 over both provenances is **$60.13**, which still does not
fit $45, so it stays registered as dropped.

## Cutoffs

Spike report by 1 September. Full run scored by 10 September 12:00 local, integrated by
12 September. Missing either sends every committed artifact to the October rebuttal card
verbatim under the R85 name, and releases the reserved main-text lines.
