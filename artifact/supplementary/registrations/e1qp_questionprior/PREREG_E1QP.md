# PREREG — E1-QP, question-prior probe and matched-contrast recomputes

**FROZEN before any probe is fit, any classifier called, or any matched-contrast AUROC
computed.** Written after E1-XV returned `claude-opus-5` blind NOK **0.6994** with a CI entirely
above chance, which the E1 line does not predict. E1-QP asks the obvious hostile question:
**can that be read off the question string alone?**

**No store contact anywhere.** Every input is a question string or a committed elicitation row.
No memory store, no index, no retrieval, no persona metadata enters any probe.

---

## 1. Populations

| | definition | n | composition |
|---|---|---|---|
| **P1** | the matched FR-Bank 84-item cell (E1-XV's cell) | **84** | 30 ABSENT · 14 PRESENT · 40 PN |
| **P2** | the full FR-Bank **hard** row carrying a question string | **307** | 272 ABSENT · 35 PN |

**P2's 39 UNRESOLVED hard items are excluded because they carry no question string** — they
were never elicited, so no text exists to probe. This is a property of the committed artifacts,
recorded, not a choice made here. FR-Bank hard is 346 items; 346 − 39 = 307.

**A degeneracy to state up front:** on P2 the only non-ABSENT label is PN, so *PN-vs-rest* and
*non-ABSENT-vs-ABSENT* are **the same partition**. That probe is reported **once** on P2, not
twice under two names. On P1 they differ (40-vs-44 and 54-vs-30).

## 2. Probe (a)(i) — TF-IDF + logistic regression, question strings only

**Input is the question string and nothing else.** Frozen configuration:

```
TfidfVectorizer(lowercase=True, ngram_range=(1,2), min_df=1, sublinear_tf=True)
LogisticRegression(C=1.0, max_iter=2000, class_weight="balanced", solver="lbfgs")
StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42), groups = persona
```

Out-of-fold predictions are pooled into **one** AUROC per (population, target). **Grouping by
persona is what makes this a prior probe rather than a memorisation probe**: no persona appears
in both train and test, so the classifier cannot win by learning a persona's vocabulary.

Targets: **(A) PN-vs-rest** (`y_nok`) and **(B) non-ABSENT-vs-ABSENT** (`y_fok`).

## 3. Probe (a)(ii) — one LLM text-only classifier

`gpt-4.1-mini`, temperature 0, `max_tokens` 16, k=1, one call per item. **Frozen minimal
prompt, registered verbatim here:**

```
SYSTEM:
You are shown a single question that a user asked their assistant. You are shown
nothing else -- no memory store, no index, no context.

Judge only this: how likely is it that, if an assistant had a memory store for this
user, that store would contain content on this topic that is now STALE -- superseded
by a later value, retracted, or past its date -- so that surfacing it would mislead?

Respond with a single JSON object and nothing else:
{"pn_likelihood": <0-100>}

USER:
Question: {question}
```

Scored as AUROC of `pn_likelihood` against `y_nok` (primary) and against `y_fok`
(descriptive, free).

**The two probes bound different things and neither is a matched comparison to the models:**

- The TF-IDF probe is **fitted to these labels**. It sees supervision no elicited model ever
  had, so it is an **upper bound on what is extractable from question text**, not a competitor.
- The LLM probe is **zero-shot**, like the models, but text-only. It bounds what a strong
  reader extracts **without** label supervision.

**CEILING(pop) ≡ max(TF-IDF PN-vs-rest AUROC, LLM PN-likelihood AUROC) on that population.**

## 4. Registered predictions

> ### QP-1 — the prior interpretation is sufficient *(per model, on P1)*
> For each of the six models with committed rows on P1, **blind NOK AUROC ≤ CEILING(P1)**, or
> its 95% CI includes CEILING(P1). A model whose blind NOK sits **entirely above** the ceiling
> is not accounted for by the question prior.

> ### QP-2 — the matched slice neutralises the phrasing prior *(check, not assumption)*
> The TF-IDF probe re-fit **on the matched slice alone** returns AUROC whose CI includes 0.50.
> **If it does not, the slice is not neutralised and §5's reading is withdrawn** — this is
> registered as a falsifiable check precisely so "topic-matched by construction" is not taken
> on faith.

> ### QP-3 — the index effect survives on prior-controlled ground
> On the matched slice: **indexed NOK CI excludes 0.50** while **blind NOK CI includes 0.50**,
> for at least the powered lineage (`gpt-4.1-mini` on P2, n = 162).

## 5. Matched contrast (b) — computed on committed rows, $0

**Slice:** positives = **all PN**; negatives = **SLOT-ABLATED items with a non-PN label**.

| population | positives | negatives | n |
|---|---|---|---|
| **P2** (powered) | 35 PN | 127 slot-ablated ABSENT | **162** |
| **P1** | 40 PN | 9 slot-ablated ABSENT | **49** |

A slot-ablated negative is a question that **was** answerable until its slot was removed, so
its phrasing is drawn from the same distribution as answerable questions. The natural-absent
FULL negatives are not — they are generic lifestyle probes, and 14 of them are reused verbatim
across personas. That asymmetry is the suspected prior, and excluding the FULL negatives is
what neutralises it.

**Secondary, descriptive:** the strict all-slot-ablated slice on P1 (12 PN vs 9 ABSENT, n=21),
reported with its n stated in the same sentence as its CI, because 21 items cannot carry a
claim.

**Coverage.** `gpt-4.1-mini` has both arms on all 307 P2 items, so it is the only lineage with
the powered slice. `gpt-5.6-luna`, `gpt-5.6-sol`, `claude-opus-5`, `claude-haiku-4-5-20251001`
and `kimi-k3` have committed rows on P1 only; their matched slice is n=49 and their CIs will be
wide. **This is stated wherever those numbers appear.**

**Estimator:** the committed scorers, imported — `score_e1.auroc`, `score_e1.boot`,
`score_ladder.auroc_ci`. Bootstrap per the paper's committed procedure: 1,000 item-level
resamples, seed 42, paired arms moving together.

## 6. Sensitivity (c)

**Residualisation, descriptive.** Per model on P1: OLS-regress the per-item blind NOK score on
the probe scores (out-of-fold TF-IDF prediction and LLM likelihood), take residuals, and report
AUROC(residual, `y_nok`). This asks how much of a model's blind discrimination survives once
the text-predictable component is partialled out. **Descriptive only** — no gate depends on it.

**Restatement.** The E1-XV deltas are restated beside CEILING(P1) so the reader sees the
blind-arm ceiling and the index effect in one table.

## 7. FAILS text — frozen

> **QP-1 FAILS on `<lineage>`.** **The text-only ceiling does not account for blind
> performance** on `<lineage>`: its blind NOK sits entirely above what question text alone
> supports. **The prior interpretation is therefore insufficient**, and the E1-XV blind result
> on that lineage cannot be dismissed as phrasing. **The neutralised-slice cell (§5) becomes
> necessary rather than confirmatory** — it is then the only evidence in this study that
> separates an index effect from a question-text effect.

> **QP-2 FAILS.** The matched slice does not neutralise the phrasing prior: a text-only
> classifier still discriminates on it. §5's reading is withdrawn and the matched contrast is
> reported as a second population, not as prior-controlled ground.

> **QP-3 FAILS.** On prior-controlled ground the index effect is not demonstrated: `<detail>`.

## 8. Budget and scope

**LLM classifier arm only:** 84 + 307 = **391 calls**, `gpt-4.1-mini`, ~$0.05 projected against
a **$2 cap**. Everything else is $0 — TF-IDF is local, and every matched-contrast AUROC is
recomputed from rows already committed.

**No store contact. No frozen artifact edited. No paper text.** Deviations continue from
**D93**.
