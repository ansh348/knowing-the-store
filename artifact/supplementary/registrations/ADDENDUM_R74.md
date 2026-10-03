# ADDENDUM_R74 — registration freeze for the R74 revision program

Frozen against baseline HEAD `67ded01b057770ffcc5fd0bb192d769c928e820c` (post-DESCOPE-7),
2026-08-24, BEFORE any R74 monitor call. Spec: the R74 program instructions. Governing
rules inherited from the DESCOPE pass. **Nothing unregistered may be reported.** Every
result below is keyed in `r74/NUMBERS_R74.md`, which this addendum declares the ledger of
record for R74 results; `iclr2027_monitoring_submission/tools/trace_scan_v12.py` (= v11 +
that ledger) is the operative manuscript scan from the first R74 integration onward, with
v10/v11 still run and their residuals reported. Bootstrap spec, all sections unless
overridden: the committed scorers' paired percentile bootstrap, 1,000 resamples, seed 42,
item-level primary + persona-clustered sensitivity, single-class draws discarded.
**Publish-regardless: every section's result prints under its frozen branch — nulls,
widened bands, and flipped directions included.**

API budget: $700 projected for the whole program; per-lane projections reported before
launch; the run stops at the cap. AM-slice question rendering uses `claude -p`
(subscription), never metered API.

---

## §X1 — FOK question-prior probe ($0, offline)

**Population.** (a) Hard tier, n=588 (35 non-\absent positives); (b) FR-Bank hard, n=307
(35 non-\absent positives). Items and labels from `e1_metamemory/build/items_final.json`
at baseline HEAD.

**Apparatus.** The committed E1-QP supervised TF–IDF probe
(`e1qp_questionprior/tools/`), unchanged except the target label: **non-ABSENT vs
ABSENT** (FOK's positive class) instead of PN vs non-PN. Persona-grouped CV identical to
E1-QP; same featurizer, same bootstrap (per-question, matching the committed E1-QP
scorer), seed 42.

**Arms.** Supervised TF–IDF only (the zero-shot arm is not rerun; $0 rule).

**Decision rule and frozen branches (verbatim from the program spec):**
- **LOW** — both populations' AUROC CI **upper bounds ≤ 0.65**: "report in App D that
  coverage-label signal in question text is limited, and add one §7.1 sentence stating
  the blind-FOK ladder ordering (P2) is measured on a population with limited text-side
  coverage signal."
- **HIGH** — either population's CI **lower bound ≥ 0.65**: "extend the App D table and
  the §7.1 caveat to cover FOK levels symmetrically with PN."
- **INDETERMINATE** (registered here to complete the branch set, D-E1R-5 precedent: an
  interval straddling 0.65 satisfies neither condition): report the row(s) in App D with
  one sentence stating the coverage-signal question is not classifiable against the 0.65
  threshold; §7.1 unchanged.

**Output cap.** One App D table row per population + at most two sentences. Paired deltas
untouched in every branch.

## §X2 — E1-INV Phase A: index-ablation mechanism probe (mini, ≈$30)

**Population.** The committed external-store items: Mem0 n=238 (94 positive), A-MEM n=284
(126 positive) — identical to the committed Table 1 / `tab:inversion` mini rows.

**Arms.** Four serialized-index variants per store, built from the committed
`indexes_v2.json` believed/true external-store index text by pure textual ablation,
holding all other content byte-identical: (a) global entry count removed; (b) category
names removed; (c) "not expressible by this backend" markers removed; (d) count and
markers both removed. Elicitation: mini (`gpt-4.1-mini` pinned), frozen `prompts_e1.py`
(digests asserted), temperature 0, k=1, E1 protocol, fresh cache namespace. The blind arm
and the intact-index arm are the **committed** E1 rows — not re-elicited.

**Decision rule (verbatim).** An arm "recovers" if its indexed AUROC minus blind has CI
excluding zero on the positive side OR the inversion delta shrinks by ≥50% with CI
excluding the intact delta (point value of the committed intact-arm delta).

**Frozen branches (verbatim):**
- (i) exactly one channel recovers → §5.3 rewrites its candidate-mechanism list into a
  measured attribution (bounded wording: "removing X eliminates/halves the inversion on
  these stores"; no causal story beyond the arm), §6's "remains open" updates to
  "localized to X on the tested stores", conclusion unchanged;
- (ii) multiple/partial → report all arms in a new appendix table, §5.3 keeps hypothesis
  framing with the measured arms cited;
- (iii) nothing separates → zero paper changes beyond an appendix table; disclosure
  stands.
The DESCOPE-untouchable inversion-disclosure ranges may be edited ONLY per these
branches.

## §X3 — Billed economics micro-run (≈$3)

**Runs.** 10,000 mini indexed monitor calls with prompt caching enabled and 2,000 blind
calls, items cycled in fixed seed-42 order from the committed FR-Bank population, frozen
prompts, temperature 0. **Telemetry only:** billed input/cached/output tokens and billed
cost are recorded from the provider usage fields; the calls' FOK/NOK outputs are neither
scored nor reported anywhere.

**Frozen rule (verbatim).** Table 2 gains an "as-billed" row per condition; §5.4's "a
projection from list prices, not a billed observation" is replaced by the billed sentence
ONLY if the billed indexed-cached figure confirms the ordering (indexed-cached < blind,
per-million-calls basis); otherwise both numbers print and the text states the
discrepancy. This is a registered replacement (S2 exemption).

## §X4 — Matched-cell expansion, 84 → full FR-Bank populations

**Populations.** NOK: the full FR-Bank NOK population, n=661 (104 PN). FOK: the full
FR-Bank hard population, n=307 (35 non-\absent). Items from the committed E1 universe.

**Lanes and protocol.** Six lineages, blind + indexed-\trueidx arms, frozen prompts with
digest assertion, pinned model identifiers re-verified per the E1.7 preventive rule
before any call; lane disclosures D86–D91 respected (Opus 5 omits temperature, Batch API
per D92 path; K3 Moonshot-direct per D90 with its provider-required parameters, output
ceiling per D87; Haiku accepts the frozen temperature).
- **mini**: the committed E1 elicitation IS this lane (identical population, protocol,
  prompts); its rows are reused, never re-elicited, and re-derived by the scorer as a
  reproduction gate. $0.
- **luna, sol, Opus 5, Haiku 4.5, K3**: k=5 repeated draws, averaged per the committed
  ladder estimator.

**Lane launch order (frozen; cheapest projected first, to maximize completed lanes under
the cap):** luna → Haiku 4.5 → K3 → Opus 5 → sol. Projected cost per lane is reported
BEFORE that lane launches; the program stops at the cap.

**Cap-stop branch (frozen).** The Table-4 primary swap happens only if all five new
lanes complete. If the cap stops the program earlier, completed lanes print in the new
expansion appendix table, the 84-item Table 4 stays primary, and §5.2 gains one sentence
citing the completed expanded lanes.

**Registered predictions (drafted from the committed 84-cell and E1 point estimates,
frozen before any call):**
- **XP-1**: each completed new lane's paired NOK delta on n=661 is positive with
  item-level CI excluding zero.
- **XP-2**: each completed new lane's paired FOK delta on n=307 is positive (directional;
  CI reported either way).
- **XP-3**: across the completed k=5 lanes plus mini's committed row, the indexed-NOK
  span is smaller than the blind-NOK span on the same lanes (information narrows
  between-model variation).
- **XP-4**: Haiku 4.5 blind NOK remains below chance and Opus 5 blind NOK remains above
  chance (direction persistence from the 84-cell).
- **XP-5** (reproduction gate, report-only): the committed mini values (NOK 661:
  0.4946/0.7339/+0.2393; FOK 307: 0.4966/0.7003/+0.2037) re-derive exactly from the
  committed rows.

**Integration templates (frozen).** Historical P1–P4 and XV-1–XV-5 verdicts are facts of
the 84-cell registration and are never re-adjudicated on the expanded cell. If all lanes
complete: the expanded cell becomes Table 4 primary; the 84-item table moves to the
appendix labeled as the original registration; Figure 1 and §5.1/§5.2 prose update to
expanded values with each registered-prediction outcome re-stated against its ORIGINAL
84-cell registration. Convergence/slogan sentences:
- *Confirming branch* (XP-3 holds and every XP-1 interval excludes zero): the band
  sentence updates to the expanded span with its lanes counted, and the slogan sentence
  is unchanged in form with expanded-cell numbers.
- *Non-confirming branch* (any XP-1 fails or XP-3 fails): the band sentence is replaced
  by: "On the expanded cell, the indexed separation [holds on N of M lanes /
  narrows/widens to the printed span]; the 84-item registered cell's result stands as
  registered." — with the slogan's convergence clause trimmed to the lanes where it is
  measured; the abstract candidates update identically. Blind-direction flips print in
  the table and are stated in one sentence without re-adjudicating XV-1.

## §X5 — Authorship-matched slice (E1-NS finalized; the one mid-program pause)

**Base registration.** `e1ns_neutralslice/PREREG_E1NS_DRAFT.md` is incorporated
**unchanged in substance**: variant B cell; acceptance criterion P(PN | slot token)=1/3
exact (amended at SP-NS1, D95); registered disposition-driven removal rule; lanes
mini (E1 protocol, temperature 0, k=1 + 50-item k=3 stability) and Opus 5 (XV protocol,
k=5, Batch API, D86/D91/D92); prompts byte-unchanged with digests asserted; predictions
NS-1 (blind NOK at chance per lane) and NS-2 (indexed−blind NOK delta > 0, CI excluding
zero, per lane) verbatim; the index-oracle disclosure reported beside results.
("Ladder lanes" in the program spec is read as the draft's two frozen lanes; the draft's
substance controls.)

**Cell state at freeze.** The 33 PN candidates are dispositioned 12 confirmed / 11
rejected / 10 routed-back (`e1ns_neutralslice/build/post_removal_census.json`). Applying
the registered removal rule with routed-back treated as removed gives the **definite
cell: n=36 (12 PN, 7 ABSENT, 17 PRESENT), 4 slot tokens, 29 personas, criterion exact,
both safeguard CIs include 0.50.** If [AUTHOR-1] completes any routed-back dispositions before
monitor launch, the cell re-expands strictly per the already-registered removal and
acceptance rules, re-verified; no other cell change is permitted.

**R74 additions (frozen).**
- Question surfaces are re-rendered under matched authorship: one generator voice for
  every label, produced via `claude -p` (subscription; never metered API) from each
  item's (entity, slot, intent) with no store-state information beyond what the E1-NS
  template exposes. Gold labels are carried, not regenerated: label = the registered
  function of intent + store state.
- **Label-transfer spot-check:** min(40, n) items sampled at seed 42; for each, the
  carried label is re-derived from the rendered question's intent + the store state;
  transfer accuracy reported. **< 0.95 → HARD-STOP S1.**
- **Pause:** the rendered-question and label-transfer exhibits go in the report for
  [AUTHOR-1]'s eyeball BEFORE any monitor call. X5 monitor calls do not launch in this run.

**Frozen branches (verbatim from the program):** (i) blind orderings survive → §7.1
upgrades from "not prior-controlled" to the measured statement and the slogan stands
with evidence; (ii) blind orderings collapse → the slogan's priors half demotes to
delta-only wording in the abstract candidates, §5.1, and conclusion; paired-delta claims
unchanged in both.

---

## Registration mechanics

One Table-15 (`tab:registrations`) row per section, added to the manuscript with this
file's freeze-commit hash after the freeze commit exists (the hash cannot cite itself);
each row's Outcome cell starts "pending" and is updated only per the frozen branches
above. The R74 deviations ledger is
`iclr2027_monitoring_submission/DEVIATIONS_R74.md`.
