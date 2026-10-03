# ADDENDUM_R81 — registration freeze for NB-6, the superseded-names matcher

Frozen against baseline HEAD `2bb7fd9`, 2026-08-29, **BEFORE any NB-6 score is computed**.
Spec: the R81 program instruction plus the three GO riders of 2026-08-29. Rules inherited
from R74/R75/R76/R77 and from `e1r_robustness/SPEC_E1R.md`: nothing unregistered may be
reported; no committed value is recomputed; registered verdicts are never re-adjudicated;
**publish-regardless** — every result prints under its frozen text, including the ones that
go against the paper.

Budget: **$0**. No API call. The embedding variant reuses the local encoder already used by
the E1-R baseline suite, offline from the on-disk cache.

Ledger: `e1r_robustness/NUMBERS_E1R.md`, new section `AUX-E1R-NB6`.
Verifier: `e1r_robustness/tools/verify_e1r.py`, extended.
Deviations: `e1r_robustness/DEVIATIONS_E1R.md`, continued numbering (D-E1R-7).

---

## §1 — Why this baseline exists

The paper's largest unexamined exposure is that under the `TRUE` index, the NOK judgment may
be close to reading the answer off one section of the index it is shown: the flat list under
`ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT`. The existing baseline suite does not test this.
NB-4 and NB-5 match the question against the **whole** per-category name map, which dilutes
exactly the signal at issue. `paper_v2.tex:1235-1237` already records, as an unregistered
note, that the SHUFFLED control leaves that flat section untouched and is therefore consistent
with a flat-lookup reading. This addendum registers the direct test of it.

## §2 — Definition (frozen)

NB-6 reads the same serialized index strings the monitor read
(`e1_metamemory/indexes_v2.json`), resolved per item by the existing
`index_features.index_key`, under both `TRUE` and `BELIEVED` provenance. It is **unsupervised
and intent-blind**: no gold intent, no gold label, no tier, and no category ground truth is
read at any point.

**NOK-6 score** — `max` over the names in that index's superseded-names section of
`sim(question, name)`. If the section is absent or empty, the score is `0`. If
`index_features.parse(...)["expressible"]` is False, the score is `0`; this guards the literal
string `not expressible by this backend`, which the parser would otherwise admit as a name.

**FOK-6 score** — `max` over all names in the per-category name map (`attr_by_cat`) of
`sim(question, name)`. Names absent, score `0`.

**Two similarity variants, both scored and both reported:**

| Variant | Definition | Reuse |
|---|---|---|
| lexical | Jaccard over content-token sets, `name.replace("_"," ")` before tokenizing | `index_features.toks` (NB-4's tokenizer, `index_features.py:38-39`) and `run_baselines.jac` |
| embedding | max cosine, `normalize_embeddings=True` | `run_baselines.encoder()`, `sentence-transformers/all-MiniLM-L6-v2`, CPU, `HF_HUB_OFFLINE=1` |

"Best NB-6" on a row is the higher of the two.

Estimator: the preregistered Mann-Whitney rank AUROC, ties at 0.5 (`common_e1r.auroc`), the
same function the monitor's own rows use. Tolerance **±0.05**, inherited from the
count-destruction probe, identical to the tolerance the existing baseline suite uses.

## §3 — Declared identity of the coverage arm (rider 1)

**FOK-6 lexical is definitionally NB-4, and FOK-6 embedding is definitionally NB-5.** Same
name list, same tokenizer, same encoder, same estimator. This is recorded here rather than
discovered later, because it changes what the coverage arm can be claimed to be:

- FOK-6 is **not** an independent measurement and is **not** registered as a prediction.
- It is a **reproduction check** with a known outcome: FOK-6 must reproduce the committed
  NB-4 and NB-5 values on `R-FOK-FRB` TRUE and BELIEVED **at four decimal places**. A
  difference in the fifth decimal arising from float summation order is not a failure. A
  four-decimal mismatch is a STOP, because it would mean one of the two paths is wrong.
- **Table 18 prints the NB-6 column on the NOK rows only**, with a dash on every FOK row and
  a footnote stating that the coverage arm of this matcher coincides with the two existing
  name-matching readers by construction. `finalize_nb6` does not recompute `best` or the
  monitor delta on any FOK row.

## §4 — Populations (frozen)

| Row | n | Provenance | Status |
|---|---|---|---|
| `R-NOK-FRB` | 661 | TRUE, BELIEVED | registered |
| `R-FOK-FRB` | 307 | TRUE, BELIEVED | reproduction check only |
| matched-84 | 84 | TRUE, BELIEVED | **descriptive**, for the ladder comparison; carries no prediction |

Row sets: `r74/x4/cell_661.json` (carries `question`, `index_key`, `y_fok`, `y_nok`;
`expect = {"n":661,"n_hard":307,...}`) and `e1xv_crossvendor/manifests/cell_84.json`.

**No external-backend rows.** On Mem0 and A-MEM the superseded-names section contains the
single literal `not expressible by this backend`. That marker is the finding those backends
carry, and scoring a name matcher against it would measure the marker rather than the store.
One sentence in F.8 records this.

## §5 — Registered predictions (two)

Tolerance ±0.05 throughout.

- **NB6-1.** Monitor NOK-TRUE (`0.7339`) exceeds best NB-6 NOK-TRUE by **more than** the
  tolerance. Equivalently, best NB-6 NOK-TRUE is below `0.6839`.
- **NB6-2.** Monitor NOK-BELIEVED (`0.5959`) and best NB-6 NOK-BELIEVED are **within** the
  tolerance of each other.

NB6-3 as issued in the R81 order (a prediction on FOK-TRUE) is **withdrawn before scoring**
and replaced by the §3 reproduction check, per rider 1 of 2026-08-29. Recorded as D-E1R-7.

**NB6-1 is a genuine coin flip and is registered as one.** The whole-index embedding matcher
already reaches `0.5974` on a NOK row. A matcher aimed at the superseded list alone should
land above that, and `0.6839` is the line at which the monitor's margin falls inside
tolerance. Neither direction is the expected one.

## §6 — Frozen branch text

Every sentence below is frozen before scoring. Sentences marked **[MAIN]** are destined for
main text and therefore contain no internal program vocabulary: they never say "NB-6",
"baseline", "registered", "branch", or a code name, and they describe the reader in plain
words. Sentences marked **[APPX]** may use the instrument's name. `$X$`, `$D$` and `$Y$` are
placeholders that resolve to `AUX-E1R-NB6-*` ledger keys at print time; no number enters the
manuscript except through such a key.

### NB6-1 HOLDS — the monitor stays ahead under a truthful summary

**[MAIN] §4.3, two sentences:**

> A matcher that scores each question directly against the store's list of names marked
> superseded reaches $X$ on the same $661$ questions. The monitor exceeds it by $D$, so under
> a truthful summary the obligation judgment rests on more than that one list.

**[MAIN] abstract, move 2, number-free:**

> With a truthful summary of the store, obligation judgment becomes visible on every model
> tested, and it stays ahead of a direct match against the store's own list of superseded
> names.

Disposition: `TRUE` stays in the abstract as the perfect-self-description ceiling. The
margin $D$ is the number printed at §4.3 and in F.8.

### NB6-1 FAILS — a name matcher reaches the truthful-summary result

**[MAIN] §4.3, two sentences:**

> A matcher that scores each question directly against the store's list of names marked
> superseded reaches $X$ on the same $661$ questions, against the monitor's $0.7339$. Under a
> truthful summary the obligation judgment is available to a direct lookup on that one list.

**[MAIN] abstract, move 2, number-free:**

> With a truthful summary of the store, obligation judgment is available to a direct match
> against the store's own list of superseded names, which makes the truthful case a lookup
> ceiling. The result that carries the paper is what the judgment does under the summaries
> real backends expose.

Disposition, binding on Phase 2:

1. The abstract **leads with BELIEVED**. Move 2 above states the ceiling and hands the lead
   to move 3.
2. `TRUE` is described as a lookup ceiling that a name matcher reaches, with $X$ printed
   beside the monitor's `0.7339` wherever the TRUE result appears.
3. The word **metamemory** is confined to the construct definition in §3. It does not
   describe the `TRUE` result anywhere in the paper.

### NB6-2 — prints either way, and says which way it went

**HOLDS (within tolerance) — [MAIN], amended 2026-08-29 before scoring, see Amendment 1.**

This branch is the paper's finding, and its landing text says so in plain words. The words
"tie" and "within tolerance" stay in Table 18 and in this addendum; they do not appear in
main-text prose.

§6 centrepiece, two sentences:

> Under the metadata the backend actually exposes, the monitor's obligation judgment is no
> better than a matcher that reads the store's list of superseded names directly. The monitor
> scores $0.5959$ on that row and the matcher $Y$.

Abstract, move 3, two sentences, **deliberately unjoined** (see §7):

> Under the metadata real backends expose, coverage judgment survives and obligation judgment
> keeps $42.3\%$ of its truthful-summary gain. On that row the monitor's obligation judgment
> is no better than a matcher that reads the store's list of superseded names directly.

**FAILS in the monitor's favour (monitor exceeds it by more than tolerance) — [MAIN] §4.3,
two sentences:**

> Under the believed summary the same matcher reaches $Y$, and the monitor exceeds it by $D$.
> The obligation judgment keeps a margin over that list once the summary is the one the
> backend actually produces.

**FAILS against the monitor (the matcher exceeds the monitor by more than tolerance) —
[MAIN] §4.3, two sentences:**

> Under the believed summary the same matcher reaches $Y$, above the monitor's $0.5959$ by
> $D$. On that row a direct lookup on the superseded list does the obligation judgment better
> than the monitor does.

### Reproduction check — [APPX] F.8, one sentence

> On the coverage rows NB-6 scores the whole per-category name map and reproduces NB-4 and
> NB-5 to four decimals, so the coverage cells print a dash rather than repeating them.

### Adverse branch (overrides the above wherever it fires)

If **any** NB-6 variant exceeds the monitor on **any** FR-Bank row, that row prints its NB-6
value in Table 18 and the accompanying sentence says so in plain words. **No row is dropped,
no variant is dropped, and the higher of the two variants is the one reported as best.**

### Not-applicable convention

Branch sentences that do not fire are marked not-applicable in the R81 report under the
**D-R74-11** convention: the frozen text is recorded in this addendum and is **not** printed,
because printing it would state something the measurement did not find.

## §7 — U9 firewall (binding)

U9 remains in force for the whole pass. The link between the BELIEVED NOK retention
(`42.3%`) and the flat-lookup mechanism bound (SW-2) stays **undrawn**.

- The two findings **may** appear in adjacent sentences.
- No sentence anywhere may assert, imply, or invite the inference that one explains the
  other. No "because", "which is why", "consistent with", "suggests", or "reflects" may join
  them.
- This applies to the NB-6 sentences above in particular, since NB-6 is the instrument that
  would make that link tempting.

A drawn U9 is a STOP for the pass, not a fixable defect.

## §8 — Ledger keys reserved

Written to `e1r_robustness/NUMBERS_E1R.md` §8 `AUX-E1R-NB6` after scoring. Reserved now so no
number can enter the manuscript without one:

```
AUX-E1R-NB6-NOK-TRUE-LEX          AUX-E1R-NB6-NOK-TRUE-EMB          AUX-E1R-NB6-NOK-TRUE-BEST
AUX-E1R-NB6-NOK-BELIEVED-LEX      AUX-E1R-NB6-NOK-BELIEVED-EMB      AUX-E1R-NB6-NOK-BELIEVED-BEST
AUX-E1R-NB6-FOK-TRUE-LEX          AUX-E1R-NB6-FOK-TRUE-EMB
AUX-E1R-NB6-FOK-BELIEVED-LEX      AUX-E1R-NB6-FOK-BELIEVED-EMB
AUX-E1R-NB6-MARGIN-NOK-TRUE       AUX-E1R-NB6-MARGIN-NOK-BELIEVED
AUX-E1R-NB6-M84-NOK-TRUE          AUX-E1R-NB6-M84-NOK-BELIEVED       (descriptive)
```

## §9A — Amendment 1, dated 2026-08-29, BEFORE any score was computed

Precedent: D-R74-14 (NS-5 branch sentences amended before launch). The amendment is recorded
with its reason so it cannot later be read as a response to a result.

**What changed.** The NB6-2 HOLDS branch originally landed as one sentence reporting that the
monitor and the matcher sit within $0.05$ of each other. That wording describes the
measurement and hides the finding: on the believed row a baseline already beats the monitor
in the published table ($0.5959$ against $0.5974$, delta $-0.0015$), so a sentence built on
the word "within" would have read as a technicality on a row the monitor has already lost.

**What it says now.** The branch states the finding directly: under the metadata a backend
actually exposes, the monitor's obligation judgment is no better than a matcher reading the
superseded-names list. It lands twice, as the §6 centrepiece and as abstract move 3.

**Direction.** Against the paper's interest. The amended text is a stronger negative statement
about the monitor than the text it replaces, and it promotes that negative statement from a
measurement note to the paper's headline. No number changes.

## §9B — Line-ending convention for the Phase 5 instruments

This clone runs `core.autocrlf=true`. Working copies are CRLF; git blobs are LF. The
consequences, measured 2026-08-29:

| Object | On-disk (CRLF) | LF-normalized |
|---|---|---|
| `paper.tex` | `4bf99071bfbd79d7584ebf5e9f841ebeeb2336c478f3258237e5133d415b9f12`, 107,320 B | `5320aec294ddd3770e1c0d5c4c66946a928aee21b7ce902d93768a04f42c3c67`, 105,897 B |
| `paper_v2.tex` (pre-R81) | `98939c799587f02cde7410c880cc1c09c33c36e506c4937fc4bdadc6a9d3fd62`, 112,263 B | `4c9314874113cf083a25f809dda5fa21e73d59a72479461ead69d9b8606b072f`, 110,785 B |

**The frozen hash of record in `CLAIMS.md` L4 is the CRLF on-disk form.** Both forms are
recorded here so the check is reproducible on a clone that checks out LF.

`core.autocrlf` is **left at `true`**. Setting it to `false` was considered and rejected:
every CRLF working file would then differ from its LF blob, and the frozen lineage would
report as modified for a reason with no content in it. That is the same false failure the
config change was meant to prevent, moved one step earlier.

**Binding on both Phase 5 instruments.** The frozen-lineage check and
`tools/appendix_identity.py` both normalize CRLF to LF before hashing or comparing, so a
line-ending difference between the working copy and a git blob can never be reported as a
content difference. Each instrument states this in its own docstring.

## §10 — Phase 1c registration, frozen 2026-08-29 BEFORE any interval or lane split exists

Ordered after `003818b`. Nothing in this section had been computed when it was written, and no
results file named here existed at freeze time.

### §10.1 Estimators (frozen)

**Stratified paired item-level bootstrap.** 1,000 draws, seed 42, the committed constants.
Within a draw, positives are resampled with replacement from that lifecycle state's positives
and negatives are resampled with replacement from the shared negative pool, both at their
observed counts. The statistic is `auroc(reader A) - auroc(reader B)` on the resample, both
readers scored on the identical resampled index set. Single-class draws are discarded.
Interval is the 2.5/97.5 percentile.

**One-sample interval against 0.5.** The same stratified resampling, a single reader's AUROC
per draw, 2.5/97.5 percentiles, draw-and-discard on single-class draws.

### §10.2 Item 2 — per-state intervals on the mini census. Branch text frozen.

Three paired differences (monitor minus matcher), one per lifecycle state, plus one-sample
intervals for both readers on all three states. All print in the appendix table.

**Retraction, difference interval EXCLUDES zero:**

> The monitor exceeds the matcher on retraction-derived obligations at $n=26$, by $D$ $[lo,hi]$.

**Retraction, difference interval INCLUDES zero:**

> On retraction-derived obligations the two readers are not separated at $n=26$, difference
> $D$ $[lo,hi]$.

**Expiry, either way:**

> The index counts expired content, and neither reader recovers it.

None of these sentences carries a superlative or an emphatic adverb asserting that the
comparison is decisive; that class of word is barred from every draft and report line here.
Item 2 enters main text nowhere.

### §10.3 Item 3 — frontier per-state split. Readings frozen.

**Question.** Does the frontier margin over the matcher come from the count-only states or
from supersession?

**Population.** The three completed n=661 lanes of `r74/x4`, INDEXED-TRUE arm, per-item scores
collapsed by the committed scorer (`r74/tools/x4_score.py` `load_lane`: dedup on draw, mean
over draws, MIN_DRAWS=3). The same 104 obligations split by originating state, the same shared
negative pool. **sol and K3 are excluded because the budget directive stopped them and they
were never scored as cells on this population (D-R74-6).**

**Rows.** Per lane, per state: AUROC point, one-sample interval against 0.5, and the paired
lane-minus-matcher difference with interval. Twelve rows, beside the mini rows.

**Reading (i) fires when BOTH hold:**
1. On retraction AND on expiry, at least two of the three lanes exceed the matcher with a
   paired difference interval excluding zero on the positive side.
2. On supersession, no lane exceeds the matcher by more than the $0.05$ tolerance.

> **[MAIN] §4.3, one sentence:** Larger models recover part of the obligation the index only
> counts.

Abstract move 2 may then say that the smallest monitor is matched by a name lookup and larger
models are not, with the reason in one clause.

**Reading (ii) fires on anything else, mixed outcomes included:**

> **[MAIN] §4.3, one sentence:** Larger models exceed the lookup on the same population, and
> the split by lifecycle state does not attribute that margin.

Abstract move 2 then names the smallest monitor only and says nothing about why larger models
differ.

**No third reading is written after the numbers exist.** The fired sentence replaces the
post-hoc frontier sentence landed at `003818b` if the two would say the same thing; main text
carries one sentence, not two.

### §10.4 Item 4 — one design sentence, scope-limit strength

> **[MAIN] §7.2:** The index names superseded content and only counts retracted and expired
> content; naming all three is the natural next index, and the per-state rows show that counts
> alone do not carry the obligation.

Classed in CLAIMS.md as scope-limit / future-work, not a positive claim. No experiment, no
number beyond a table pointer.

### §10.5 Budget

Main text grows by at most **two review lines** across §10.3 and §10.4 combined. The appendix
is uncounted against the page gate.

### §10.6 STOP conditions for Phase 1c

- Any per-state interval computed before this section existed.
- Any main-text sentence attributing the frontier margin without reading (i) having fired.
- Any superlative or emphatic adverb asserting a comparison is decisive, surviving anywhere
  in the tree (the class barred under section 10.2).
- Main text over the two-line budget.

## §11 — Phase 1d registration, frozen 2026-08-29 BEFORE any number in it exists

Ordered after `fff012e`. Nothing here had been computed when it was written.

### §11.1 Why this pass exists

The §4.3 sentence landed at `fff012e` says larger models "recover part of the obligation the
index only counts." That attributes the expiry and retraction gains to the index. The
lane-versus-matcher comparison **cannot establish it**: the matcher is intent-blind, the lanes
see the question, and this paper's own question-prior audit shows question text carries
state-flavoured signal. Opus 5's blind NOK on this population is $0.6429$. The
prior-controlled quantity, by this paper's own methodology, is the paired
indexed-minus-blind delta. Phase 1d computes it and lets it decide the sentence.

### §11.2 Item 1 — the attribution gate

**Rows.** Per lane (luna, Opus 5, Haiku 4.5) and per originating state (supersession 63,
expiry 15, retraction 26), on the same n=661 rows with the shared negatives: blind AUROC
point, indexed AUROC point, and the paired indexed-minus-blind difference with interval.
**Nine rows.**

**Estimator.** The §10.1 stratified paired item-level bootstrap, unchanged: 1,000 draws, seed
42, positives resampled with replacement within their state, negatives from the shared pool,
both arms scored on the identical resampled index set, single-class draws discarded, 2.5/97.5
percentiles. Points computed on the same subset the bootstrap resamples.

**Mini is excluded.** Its blind NOK arm is constant, the standing all-tie degeneracy already
recorded at `NUMBERS_E1R.md` §1 and §10, so no paired delta on it is a calibrated quantity.
One sentence in the appendix says so.

**The supersession column prints for completeness and carries no reading.**

**Reading (i) fires when:** on expiry AND on retraction, the paired indexed-minus-blind delta
excludes zero on at least two of the three lanes.

> The `fff012e` §4.3 sentence stands unchanged: *That matcher reaches the smallest model
> tested. Larger models recover part of the obligation the index only counts.*

The abstract move-2 clause may then state the reason as frozen in Phase 1c.

**Reading (ii) fires on anything else**, including a split where one state confirms and the
other does not. Mixed outcomes fall to (ii).

> **[MAIN] §4.3 becomes, verbatim:** That matcher reaches the smallest model tested. Larger
> models score higher on the states the index only counts (Table~\ref{tab:nb6-frontier}).

No "recover", no attribution. The abstract move-2 clause then names the smallest monitor only
and says nothing about why larger models differ.

**No third reading is written after the numbers exist.**

### §11.3 Item 2 — the §7.2 design sentence, both versions frozen

The sentence landed at `fff012e` says counts alone do not carry the obligation. After Phase 1c
that is true of the lookup and of the smallest reader, and its status for larger models is
exactly what item 1 decides. Both replacements are frozen here; the one matching the fired
reading lands, and the CLAIMS.md entry text is updated to the landed version. Same strength
class as before: scope limit / future work, not a positive claim.

**Under (i):**

> The index names superseded content and only counts retracted and expired content; the lookup
> and the smallest reader recover nothing from the counts, larger models recover part, and
> naming all three states is the natural next index (Table~\ref{tab:nb6-frontier}).

**Under (ii):**

> The index names superseded content and only counts retracted and expired content; the lookup
> and the smallest reader recover nothing from the counts, and naming all three states is the
> natural next index (Table~\ref{tab:nb6-frontier}).

### §11.4 Item 3 — persona-clustered intervals on the mini per-state rows

Print the persona-clustered interval beside the item-level interval for **all three** mini
per-state paired differences (monitor minus matcher), so no row is singled out. Estimator: the
clustered draw-and-discard rule this paper already uses for its clustered columns
(`common_e1r.boot_cluster`), applied to the subset of that state's positives plus the shared
negatives: draw as many personas with replacement as the subset contains, take every item in
each drawn persona, discard single-class draws, 2.5/97.5 percentiles.

**Retraction row, clustered interval INCLUDES zero:**

> The retraction row is marginal at item level (lower bound $+0.0002$) and not separated under
> persona clustering.

**Retraction row, clustered interval EXCLUDES zero:**

> The retraction row is marginal at item level (lower bound $+0.0002$) and survives persona
> clustering.

Either way the word "marginal" stays and the bound prints.

### §11.5 Item 4 — hybrid monitor, queue only

The crossover implies a monitor using the lookup on the named state and the model on the
counted states would outperform both readers. **It is not computed in this pass.** One line
goes to the R-DS queue describing it as post-fence with no registration. Nothing in the paper
references it. Computing it is a STOP for Phase 1d.

### §11.6 Budget and STOP conditions

Main text budget is **+0 lines**: every main-text change is a sentence replacing a sentence.

- Any of the nine rows computed before this section is committed.
- The word "recover" surviving in main text after reading (ii) fires.
- Main text over +0 lines.
- Any computation of the hybrid monitor.

## §9 — STOP conditions specific to this registration

- The superseded-names section missing from any FR-Bank serialized index. *(Pre-checked
  2026-08-29 against all 562 FR-Bank keys: present and non-empty on every one. Recorded so
  the check is not claimed twice.)*
- FOK-6 failing to reproduce NB-4 or NB-5 at four decimal places.
- `verify_e1r.py` exiting non-zero after the NB-6 keys are added.
- Any number reaching the manuscript without an `AUX-E1R-NB6-*` key.
- U9 drawn anywhere.
