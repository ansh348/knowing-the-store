# ADDENDUM R85-GRAPHITI — a second lifecycle-bearing backend

**DRAFT until Phase 3 freezes it.** Nothing below has been scored. The spike that licensed
it is `r85_graphiti/SPIKE_REPORT.md`; the rules it rests on were frozen in commit `ca522b0`
before any billed call, and the spike ran under `1ec6184`.

Deviations use `D-R85-n` and live in `r85_graphiti/DEVIATIONS_R85.md`. No edit to
`CLAIMS.md` happens before integration; the dated R85 block is prepared as a diff.

---

## §1 Why this exists

Two reviews record the same objection: the only backend on which the obligation gain
appears is the authors' own, and the two backends on which it inverts carry indexes that
are mostly inexpressibility markers. This addendum registers a test on a third backend,
Zep's Graphiti, which we did not build, which exists in the world, and which carries a
bi-temporal edge model with `valid_at`, `invalid_at`, `created_at` and `expired_at`.

## §2 Populations

The committed FR-Bank populations, questions and labels byte-identical:

- **NOK, n = 661** — `backend == frbank` intersected with the scoreable label set: 104
  PRESENT-NEGATIVE, 383 ABSENT, 174 PRESENT.
- **FOK hard tier, n = 307** — the same set intersected with `tier == hard`, 35 PN. It is a
  **subset** of the 661, and both judgments are scored from the same elicitation, so a lane
  costs 661 calls per provenance rather than 968.

The same deletions are applied to the ingestion stream, so ABSENT and PN labels stay valid.
**Labels are persona ground truth and do not depend on what Graphiti extracted.** Extraction
misses are what the BELIEVED index is for, and the spike measured them.

## §3 Index provenance

- **BELIEVED is primary.** Built from Graphiti's own fields on the 40 ingested personas
  under the rules frozen in `r85_graphiti/graphiti_index.py`.
- **TRUE-projected is secondary.** Ground truth projected onto what Graphiti's schema can
  express, so the gap between the two isolates the extractor from the schema.

Both emit in exactly `index_v2.py`'s serialization, through `index_v2.render` itself rather
than a fork, with the marker string `not expressible by this backend`. RETRACTED and
category carry the marker on both provenances: neither is a measurement, both are schema
facts established from unmodified source before any ingestion.

## §4 Lanes and readers

| Lane | Protocol |
|---|---|
| GPT-4.1 mini | main-study protocol, one call, temperature 0, both provenances |
| Haiku 4.5 | k = 5 via the Message Batches API, BELIEVED only |
| Opus 5 | **registered as dropped**, see §6 |

Readers: the superseded-names matcher (NB-6, embedding variant) over Graphiti's own
superseded list, and the whole-map embedding matcher (NB-5). Nothing else. Both run on a
local offline encoder and bill nothing.

## §5 Billing paths

Every row is derived from a measured per-call or per-episode figure in a committed
artifact, by `r85_graphiti/tools/billing_table.py`. The Anthropic rows reconcile against
list price (Haiku 4.5 $1/$5, Opus 5 $5/$25 per MTok) with the Batches 50% discount applied,
and the script asserts that reconciliation so a price change breaks the tool rather than
this registration.

| Arm | Provider | Exact model identifier | Billing path | Key name in `.env` | USD | Ceiling |
|---|---|---|---|---|---|---|
| Graphiti ingestion, extractor | OpenAI | `gpt-4.1-mini-2025-04-14` | metered API key | `OPENAI_API_KEY` | 10.14 | $28 ingestion stop |
| Graphiti ingestion, embedder | OpenAI | `text-embedding-3-small` | metered API key | `OPENAI_API_KEY` | 0.01 | $28 ingestion stop |
| Monitor, mini, BELIEVED | OpenAI | `gpt-4.1-mini-2025-04-14` | metered API key | `OPENAI_API_KEY` | 0.45 | $15 monitors |
| Monitor, mini, TRUE-projected | OpenAI | `gpt-4.1-mini-2025-04-14` | metered API key | `OPENAI_API_KEY` | 0.45 | $15 monitors |
| Monitor, Haiku 4.5 k=5, BELIEVED | Anthropic | `claude-haiku-4-5-20251001` | Batch API, metered | `ANTHROPIC_API_KEY` | 4.44 | $15 monitors |
| Monitor, Haiku 4.5 k=5, TRUE-projected | Anthropic | `claude-haiku-4-5-20251001` | Batch API, metered | `ANTHROPIC_API_KEY` | 4.44 | $15 monitors, conditional |
| Reader NB-5, whole-map embedding | local | `all-MiniLM-L6-v2` | local, offline | none | 0.00 | none |
| Reader NB-6, superseded-names | local | `all-MiniLM-L6-v2` | local, offline | none | 0.00 | none |
| Monitor, Opus 5 k=5, both provenances | Anthropic | `claude-opus-5` | Batch API, metered | `ANTHROPIC_API_KEY` | 60.13 | **DROPPED** |

**Totals.**

| Account | Expected | Worst case |
|---|---|---|
| `OPENAI_API_KEY` | $11.06 | $14.11 |
| `ANTHROPIC_API_KEY` | $4.44 | $8.88 |
| **Both, against the $45 total** | **$15.50** | **$22.99** |

Worst case applies the 1.3x margin to ingestion and adds the conditional Haiku
TRUE-projected lane. Both totals sit inside $45 with room.

**Two notes on the paths.**

The mini lane bills the metered OpenAI key, not a Codex subscription. `codex-cli 0.147.0`
is installed and a zero-dollar route therefore exists, but R82 billed this lane to the
metered key (`r82_counterfactual/tools/run_cf.py:150`) and that path emits `tok_in`,
`tok_out` and `usd` on every row. A subscription route emits none of those, and this
program requires every number to trace to an artifact. The lane costs $0.91 across both
provenances, which is not worth the loss of the ledger.

Ingestion cannot use a subscription route at all: `graphiti-core` calls the OpenAI API from
inside the library.

**Pre-flight probes, both run 2026-08-30T11:59:30Z, artifact
`r85_graphiti/billing_probe.json`:**

- `OPENAI_API_KEY` — **PASS**, one call, served `gpt-4.1-mini-2025-04-14`.
- `ANTHROPIC_API_KEY` — **PASS**, one call, served `claude-haiku-4-5-20251001`. A
  zero-balance organization returns `400 credit_balance_too_low` on this path, so a
  succeeding credit-bearing call is the confirmation that the Batch submission is funded.

## §6 Ceiling

$45 total, re-partitioned under `D-R85-5` on measurement rather than estimate: **ingestion
sub-ceiling $24, ingestion stop rule $28, monitors $15.** The spike measured ingestion at
$0.00743 per episode over 103 episodes, so the 40-persona figure is $10.14 and the stop rule
is not approached.

**Opus 5 is registered as dropped, with its price.** At the registered k = 5 over both
provenances it costs $60.13, computed from R82's own measured $0.009096 per call. It does
not fit $45 under any partition. It is recorded as dropped rather than left conditional, so
that no later reading can quietly reintroduce it.

**Stop rule.** If billed ingestion exceeds $28, stop before any monitor call.

**Time rule.** The spike measured 6.5 hours sequential for 40 personas and near-linear
two-way persona parallelism, so eight-way parallelism puts ingestion under an hour. The
48-hour clause is not triggered.

## §7 Frozen readings

Each carries its hold sentence and its fail sentence, written now, before scoring. Both
print. `$X$`, `$D$`, `$I$` and `$Y$` resolve to `AUX-R85-*` ledger keys at print time.

### GR-1. On Graphiti BELIEVED, the paired NOK gain on GPT-4.1 mini excludes zero

**HOLDS, [MAIN] one sentence:**

> On a second store that records when a fact stopped being true, one built by another group,
> the obligation judgment rises by $D$ when the summary is supplied, interval $I$.

**FAILS, [MAIN] one sentence:**

> On a second store that records when a fact stopped being true, the obligation judgment does
> not rise beyond $D$ when the summary is supplied, so the gain measured on our own store
> does not reproduce where the lifecycle record is thinner.

### GR-2. On Graphiti BELIEVED, the paired FOK gain on GPT-4.1 mini excludes zero

**HOLDS, [APPX] one sentence** giving $D$ and $I$.
**FAILS, [APPX] one sentence** giving $D$ and naming the population.

### GR-3. The superseded-names matcher sits within ±0.05 of the mini monitor, or above it

**HOLDS, [APPX] one sentence:**

> A matcher reading the store's own list of superseded names reaches $Y$ against the
> monitor's $X$ on this store as well.

**FAILS in the monitor's favour, [APPX] one sentence** giving the margin $D$.
**FAILS against the monitor, [APPX] one sentence** giving the margin $D$ and naming the
direction. Adverse rows print in the table and are named in the text of the row they affect.

### GR-4. Descriptive, no bar: NOK retention against FR-Bank's TRUE gain

Printed as a fraction of $+0.2393$, beside FR-Bank's own BELIEVED retention of $42.3\%$.
Carries no prediction and prints whichever way it reads.

### GR-5. Descriptive, no bar: Graphiti's Table 21 failure mode

Named from the 40-persona census as one of overstate, erase, invent, conflate, or none.
**The spike's three-persona reading is erase with overstatement in what survives**, and the
full census either confirms that or replaces it.

### Not-applicable convention

A row that cannot be computed prints a dash with a footnote giving the reason. An empty row
is never left to be read as zero.

## §8 Disclosure

The paragraph frozen at `r85_graphiti/DISCLOSURE.md`, which records that this project ran on
Graphiti from approximately 21 February 2026 to 15 March 2026, replaced it on 6 April 2026,
vendored version 0.28.1 under Apache-2.0, applied four documented numeric-preservation
modifications and one undocumented world-knowledge filter, and that no current code path
imports it. The measured behavioural delta between the unmodified release and the modified
copy is reported beside it: edge counts within 2.4% and supersession recall identical at the
frozen bar, so the modifications are near-inert on this corpus.

## §9 Cutoffs

Scored by 10 September 12:00 local, integrated by 12 September. Missing either sends every
committed artifact to the October rebuttal card verbatim under the R85 name, and releases the
reserved main-text lines.
