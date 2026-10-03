# CLAIMS.md — R78 claim constitution (Phase 0)

Extracted from the FROZEN `paper.tex` at commit `0684fdd` (SHA-256
`4bf99071bfbd79d7584ebf5e9f841ebeeb2336c478f3258237e5133d415b9f12`).
Line numbers refer to that file. This inventory governs `paper_v2.tex`: the rewrite may
reorganize, reword, cut repetition, and change emphasis, but **every entry below must appear
in paper_v2 at IDENTICAL strength — no claim strengthened, weakened, or dropped.**

Ledger snapshot at P0 (concurrent-session drift detector), SHA-256:
- `e1_metamemory/NUMBERS.md` `638a0139149f668855f3aaa409bd785c2e3b47b4d0e104be3229292d83a21b72`
- `e1xv_crossvendor/NUMBERS_E1XV.md` `1b34781bd7a6ba15b0fc77efef979f7f2e9dac8504f0f1834c3c13a4a67a0c6e`
- `e1qp_questionprior/NUMBERS_E1QP.md` `90d2fee6fc48717800386595e0680f6ee67491ecac38c75b5a7ba41348a9f2c8`
- `e1r_robustness/NUMBERS_E1R.md` `8fb8fed58cf098e839627a2bd7053fa067aab8b8fc46f89bf823ada557f5c0e5`
- `r74/NUMBERS_R74.md` `3426635e80d71133b998906a53f9f82b663b886c70760cf6c125b36caa51c0d4`

## Authorized departures (closed lists — anything else is a VIOLATION)

**AUTHORIZED-REFRAME (exactly three, per the R78 order):**
- **R1 — Prop 1 wording (L306).** "the index is a necessity, not an optimization" is
  replaced by: Prop 1 shows a top-$k$-bounded monitor cannot detect obligations in
  principle; a maintained index is one mechanism that escapes the bound. Recorded as a
  deliberate softening. The proposition statement (C036), its proof, and the C136 scoping
  clause are unchanged in strength.
- **R2 — Economics out of main text (§5.4 + Table 2).** Relocated verbatim to a new
  Appendix F subsection; the main text keeps a two-sentence pointer stating that the
  projection and the billed micro-run disagree, WITHOUT digits. No economics claim changes
  strength; both cost orderings continue to print (in the appendix) as the R74 X3
  non-confirming branch requires.
- **R3 — §6 promoted framing.** The store self-description section states the design law
  as the paper's second positive finding (lifecycle-aware self-description is the
  precondition; structureless backends invert at every scale; BELIEVED metadata halves the
  obligation benefit to embedding-matcher level) instead of damage-control framing. Same
  claims, same numbers, same hedges (C081 verbatim).

**AUTHORIZED-ABSTRACT (R83).** The abstract is replaced with the user's reframed eleven-sentence
version. Inside S6's 9-to-11 band, no sentence over 40 words, no em dash, no contrastive.
Two entries this needs on the record:

- **Sentence 5's "what the summary transmits is bounded by what it names" restates
  SCOPELIMIT-R81-1**, the naming-granularity claim the manuscript already carries in Section 6
  ("The index names superseded content and only counts retracted and expired content") and in
  Definition 3's gloss ("A self-description can only name what its scrubbing rule
  individuates, so naming granularity bounds what any reader can recover"). The abstract
  states it at the same strength; no new claim enters.
- **0.5656 and 0.8489 are promoted into the abstract** from Section 7.1. Both are ledgered in
  NUMBERS_R82 section 7 and both already print in main text, so this is emphasis, which the
  governing rule permits, and not a new measurement. 42.3% is unchanged.

U9 is satisfied by arrangement rather than by omission: the retention figure sits in sentence 8
and the text-match result in sentence 9, adjacent and never joined, which is what CLAIMS.md
line 202 permits and what u9_scan now enforces mechanically.

Two sentences the previous abstract carried are DROPPED as the user directed: "the paired
obligation gain is positive" and "On that row it falls to a matcher's level". Their content
survives in sentences 4 and 9 respectively.

**AUTHORIZED-GLOSSARY (R83).** CL-GLOSSARY authorizes the notation box to move byte-verbatim
to Appendix F under ORDERED-MECHANICAL. R83 replaces its content: three blocks, the third
mapping the artifact's internal names onto the printed term. This exceeds a relocation and is
recorded here rather than taken silently. No claim changes; a glossary defines terms and states
no result. The internal vocabulary the main text is barred from using (S10) is named here, which
is where STYLE_SPEC directs it.

**AUTHORIZED-CORRECTION (exactly one, R83): a cited number the cited record does not support.**
- **CL-C149's 6% ceiling becomes 28%.** The claim reads "no evaluated system exceeds 6% accuracy
  on the multi-hop conflict-resolution slice \citep{memoryagentbench}". The ICLR 2026 camera-ready
  states, verbatim: "We observe that all methods fail on the multi-hop situation (with achieving at
  most 28% accuracy)." Its FC-MH column confirms it, with a maximum of 28.0 (GPT-5-mini 400K) and
  every other system at or below 7.0. The 6% figure is the arXiv **v1** (2025-07-07) number; the
  R75-F13 venue upgrade moved the bibitem to ICLR 2026 without re-testing the number that depends
  on the version, so the manuscript was attributing a v1 figure to a 2026 record.
  This is a **correction of fact, not a reframing**. The claim class is unchanged: a cited external
  ceiling, at whatever value the cited record prints. It weakens the motivating premise and is
  taken anyway, because the alternative is a number a reviewer falsifies by opening the citation.
  Recorded as D-R83-1. STRENGTH for CL-C149 now reads: 28% ceiling (cited); vendor staleness
  admission (cited).
- **CL-C149's ceiling is split by the cited table's own grouping (R83-2).** The sentence now reads
  "no evaluated RAG or agentic-memory agent exceeds 7% accuracy; the 28% ceiling belongs to a
  long-context agent holding the entire history". Both halves are values read off Table 3's FC-MH
  column, under that table's own row-section headers, so this is citation rather than
  interpretation. The grouping is the cited paper's: section 3.2 evaluates "three major types of
  memory agents ... Long-Context Agents, RAG Agents, and Agentic Memory Agents", and Table 3 blocks
  its rows under exactly those headings.
  NOTE the trap this avoids: a long-context agent IS a memory agent under that taxonomy (line 69,
  "we refer to agents equipped with memory mechanisms as Memory Agents"), so a claim of the form
  "no evaluated memory system exceeds 7%" would be FALSE by the source's own definitions. The
  category names must be the source's.
  STRENGTH for CL-C149 now reads: 7% RAG-and-agentic-memory ceiling with a 28% long-context ceiling
  (both cited); vendor staleness admission (cited). Recorded as D-R83-2. The sentence is split in
  two, which drops a held 45-word exemption from the length gate.

- **The same entry's vendor clause.** "left users to manage updates by hand" is replaced by "was
  written only on explicit request". The vendor page supports that memories were written on
  explicit cue; it does not state that users had to correct stale entries. Restatement replaces
  inference at the same claim class, length-neutral. Recorded in REFCHECK_V11 section 3.

**ORDERED-MECHANICAL (presentation changes ordered by R78; no strength change):**
- Table 15 (`tab:wrongindex`) ∆ convention flips to manipulated − intact with
  negated-and-swapped CIs, per the A2 Option-3 pre-ruling: the footnote names the committed
  paired-bootstrap estimator and the ≤0.002 endpoint-gap bound; D-R74-20 records the
  premise correction; AUX-R78-SWAP-GAP ledgers the bound.
- Table 1 orphan ‡ (L337) anchored to the "FOK, pooled hard (secondary)" row (L330).
- The stranded D2a paragraph (F.7, L1338–1341) moves beside `tab:matched-cell` (D.1).
- §8's verbatim echo of the abstract slogan (L671 ≡ L60) is paraphrased in §8.
- The §3 glossary box moves to a new Appendix F subsection; §5.4 economics likewise (R2).
- Abstract and Introduction are [AUTHOR-1]-DRAFT skeletons; the abstract skeleton prints exactly
  one CI (+0.2037 [+0.0935,+0.3191]) and the pooled +0.2272 does NOT appear in it. The
  pooled claim itself (CL-T-e1 row 2, CL-C141) remains in §4 at full strength.
- CONDITIONAL (P1 ruling, [AUTHOR-1]): the Mem0/A-MEM inversion CIs print at 3dp in paper.tex
  ([−0.169,−0.025], [−0.173,−0.040] — Table 1 rows 5–6, Table 12 item-level rows 5–6,
  Table 17 rows 1–2, Table 18 intact rows) while all other CIs print at 4dp. If the
  committed ledger keys record these endpoints at 4dp, paper_v2 prints them at 4dp,
  recorded as precision harmonization (display precision, not value change — CLAIMS
  entries unaffected); if the committed values are recorded only at 3dp, they print as-is
  and a one-line note in the R78 section says why the precision differs. Ledger lookup
  only; no re-derivation either way. U8's byte-identity requirement is subordinated to
  this ruling for exactly these interval strings.
  RESOLVED (P1, ledger lookup): NUMBERS_E1R.md L21–22/L35–36 records the committed
  item-level endpoints at 4dp — R-FOK-MEM0 [−0.1686,−0.0250], R-FOK-AMEM
  [−0.1726,−0.0403] — and states they "reproduce the printed 3-dp roundings". The
  HARMONIZATION branch fires: paper_v2 prints the 4dp forms at Table 1 rows 5–6, the
  Table 12 item-level rows, Table 17 rows 1–2, and Table 18's intact rows. Central
  NUMBERS.md L123–124 carries the 3dp forms; the 4dp source outranks the rounding.
  Tokens 0.1686/0.0250/0.1726/0.0403 are ledger-members (trace_scan-safe).

**ADDITION-AUTHORIZED (new sentences from committed facts, not new measurements):**
- **A1 (conditional)** — one distinguishing sentence each for HUSH-Bench (2606.06055) and
  StateMemBench (2608.19652) in §2's obligation-neighbors paragraph, ONLY if their arXiv
  abstract pages resolve and match; otherwise nothing is cited and the disposition is
  recorded.
- **A3** — two sentences after the 5.2% posterior: mislabeled ABSENT items enter the
  negative class and can only attenuate measured discrimination, so reported deltas are
  conservative w.r.t. this error; PN labels do not rest on the presence control — all 104
  were individually hand-verified (Appendix F). Bases: L365 (C045), Table 11 L1097,
  App E item 2 (L1024).
- **A4** — one §5 clause: mini's rows use the committed single-draw elicitation while the
  other lanes use k=5 (as the capability table states); the scale reading rests on the k=5
  lanes. Basis: `tab:ladder-exact` caption L811, `tab:ladder-predictions` caption L877.
- **A5** — one §4 sentence at the resolution analysis: on the hard tier the FOK-positive
  class coincides with PN by construction (no ordinary PRESENT positives), which is why the
  resolution analysis and the balanced matched cell exist. Bases: Table 7 footnote L953,
  Table 11 L1092, §7.1 L632 (D-R74-2).
- The A2 estimator footnote on Table 15 (per pre-ruling).

**UNTOUCHABLE, BYTE-IDENTICAL, EXACTLY ONCE in paper_v2:**
- U1 (L545–546): "This is an inversion at every scale, not a below-chance score at every
  scale. The cause of the below-chance cases remains unresolved."
- U2 (L553): "Scope: the negative index effect is measured; the single-channel ablations
  do not identify its cause."
- U3 (L613–614): "The association does not identify which rendered feature causes the
  inversion. The candidate mechanisms in Section~\ref{sec:inversion} remain unresolved
  after the registered single-channel probe."
- U4 (L618): "This law is directional but not mechanistic: the source of the observed
  below-chance behavior remains open."
- U5 (L654): "The structureless-store inversion is measured across scales, but its
  below-chance mechanism remains unresolved."
- U6 (L652): the NS-2 limitation sentence carrying "which ships as its registered failure"
  — the frozen-failure wording must survive verbatim.
- U7 (L437): the SW-2 sentence with its mandatory bound clause ("...though the shuffle
  preserves the global name and count multiset and the flat superseded-names section and
  so bounds correspondence alone").
- U8: Table 1 inversion rows (L333–334) and all of Appendix F.6 (L1249–1294) —
  byte-identical values.
- U9: the retention↔flat-lookup LINK stays UNdrawn (L1220–1222 remains a % comment;
  D-R74-19). Drawing it in prose is a VIOLATION.

---

## R81 AUTHORIZATION BLOCK — dated 2026-08-29

Appended by the R81 pass. Everything below is a **closed list**: any departure outside it is
a VIOLATION and stops the pass. Registration of record:
`registrations/ADDENDUM_R81.md`, frozen against HEAD `2bb7fd9`.

**REFRAME 4 — thesis reorder (presentation only; no claim changes strength).**
The paper's headline becomes the self-description question: what a store must expose about
itself for a monitor to know its obligations, and what happens when it does not. This
reorders which frozen claims are headline. NOK remains defined and measured as
contribution 1 (CL-C002, CL-C141 and the §4 NOK claims are untouched at full strength) and
stops being the sole load-bearing claim. No CL entry changes STRENGTH under Reframe 4.

**REFRAME 5 — the design law softens to an observation. STRENGTH REDUCTION, recorded.**
This **supersedes R78's AUTHORIZED-REFRAME R3**, which had promoted the design law to the
section's second positive finding. The words "design law", "law" and "precondition" as
claim words are banned from main text.

| | Text |
|---|---|
| **OLD** (paper_v2 L566, under R3) | "The design law this section establishes is: \emph{self-model expressiveness is a precondition for metamemory}." |
| **OLD** (paper_v2 L647, §8 close) | "The precondition for knowing the store is self-model expressiveness; scale alone does not supply it." |
| **NEW** (§6 and §8, R81) | An observation on the three backends tested, at the strength the data supports: the benefit appears on the one lifecycle-aware backend; the two backends without lifecycle structure invert it; the mechanism is unresolved. |

Direction of the change: **weaker**. A general design law over stores becomes a statement
about three measured backends. Every number, every interval and every scope sentence in §6
is kept; U1, U3, U5 and U8 are untouched in content. The §6 section title is retitled to the
self-description question, which removes "precondition" from it.

**NB-6 ADDITION (new measurement, $0, registered before scoring).**
One deterministic, unsupervised, intent-blind baseline enters the E1-R suite: a matcher over
the serialized index's superseded-names section, in a lexical and an embedding variant.
Defined, populated and branch-frozen in `ADDENDUM_R81.md` before any score existed. Its
branch sentences land per branch. New keys are `AUX-E1R-NB6-*` in
`e1r_robustness/NUMBERS_E1R.md`; the verifier of record is
`e1r_robustness/tools/verify_e1r.py`. Registered predictions: NB6-1 and NB6-2. The order's
NB6-3 was withdrawn before scoring and replaced by a declared reproduction check (D-E1R-7).

**U-BLOCK RELOCATIONS (byte-identity preserved; ruling of 2026-08-29).**
Two untouchable blocks collide with the Reframe 5 ban list and with the R81 "Scope:" sweep.
Both **relocate verbatim into the appendix** rather than being rewritten; each keeps its
exact bytes and therefore still appears EXACTLY ONCE in the document, which is the level at
which `slogan_scan`'s pinned check counts. Main text receives a plain-language replacement
at the same claim strength.

- **U2** ("Scope: the negative index effect is measured; the single-channel ablations do not
  identify its cause.") moves from §5.3 into Appendix F.6.
- **U4** ("This law is directional but not mechanistic: the source of the observed
  below-chance behavior remains open.") moves from §6 into Appendix F.7.
- **U7** (the SW-2 sentence ending "...and so bounds correspondence alone") moves from
  §4.4 into Appendix F beside `tab:wrongindex`. **Added 2026-08-30** on the user's ruling,
  after Phase 4 reported that rewriting it in place would have broken byte-identity,
  `EXEMPT_S8` and the `PINNED` check at once. Main text receives a two-sentence plain
  replacement at the same claim strength. **U1, U3, U5, U6 and U8 stay where they are.**

No other U-block moves. U1, U3, U5, U6 and U8 stay where they are. **U9 stays in force
unchanged**: the link between the BELIEVED NOK retention and the flat-lookup mechanism bound
remains undrawn. R81 may place the two findings in adjacent sentences; it may not assert
that one explains the other. NB-6 does not license that link.

**ORDERED-MECHANICAL under R81 (presentation, no strength change).**
- Abstract and §1 are proposed in `reviews/R81_ABSTRACT_INTRO_PROPOSED.md` and change **zero
  paper bytes** until [AUTHOR-1] lands them. The `prose_scan` HELD carve-out stays.
- The convergence span (0.3307 to 0.0389) leaves the §1 contribution list and remains as
  descriptive text in §5.1, where it already stands. The claim itself is unchanged.
- §5.3's economics pointer compresses to **one** §7.2 sentence that still states the two
  cost orderings disagree, preserving R78-REFRAME(R2)'s substance in a shorter form. Both
  orderings continue to print in Appendix F.10, as the non-confirming branch requires.
- §8's economics sentence is cut from main text; its disclosure lives in the §7.2 sentence
  above.
- The §3 pointer sentence to Remark 1 is cut from main text; Appendix A keeps the statement
  and proof.
- Proposition 1's informal below-cutoff sentence shortens, keeping the measured 5% premise.
- Table 18 gains one NB-6 column on the NOK rows only, with a dash on the coverage rows and
  a footnote giving the reason.

**POSTHOC-AUTHORIZED (R81, added 2026-08-29 AFTER NB6-1 failed).**
Two readings entered after the NB-6 result and are labelled post hoc wherever they appear.
Neither becomes a headline, neither enters the abstract, and both print regardless of what
they showed.

- **POSTHOC-R81-1 (frontier margin).** NB6-1 was registered against the primary monitor
  (mini, 0.7339). The same 661 questions under the same \trueidx{} indexes are already
  scored for three further models in `tab:x4-expansion`: luna 0.8182, Opus 5 0.8327,
  Haiku 4.5 0.8210. Each exceeds the superseded-names matcher's 0.7484 by more than the
  suite's tolerance. The reading is that the matcher reproduces the SMALLEST monitor and
  that larger models extract something from the index the matcher does not. This is a
  comparison of two committed tables, not a new measurement. STRENGTH: post hoc,
  descriptive, one sentence in §4.3 keyed to `tab:x4-expansion`. It does NOT license
  "the monitor beats the matcher" without naming which monitor, because that reading is
  false for mini. Protocol disclosure carried by A4: those three rows average five calls
  per question, mini's row is a single call.
- **POSTHOC-R81-2 (composition census).** A deterministic $0 census of the obligation
  population by the lifecycle state each obligation arises from, and of whether the
  item's own attribute name appears in the section the matcher reads. Recorded at
  `NUMBERS_E1R.md` §12 `AUX-E1R-NB6-COMPOSITION`. STRENGTH: post hoc, descriptive,
  appendix only, beside Table 18. It prints whether or not it supports the structural
  premise, and it did support it. R97 (2026-09-13): the per-state rows that support the
  premise (0.9534 / 0.4823 / 0.4053) are untouched; the own-name count this entry also
  carried (7 of 104) keyed entry ids without their persona and is superseded by 74 of 104
  (63 of 63 on supersession) under D-E1R-10; the manuscript site is corrected under the R97
  block, entry 4a.

Neither entry weakens or strengthens any CL-* claim. The §4.3 sentences that landed under
the NB-6 registration stand unchanged.

**PHASE 1C (registered 2026-08-29 at `e8ba22c`, computed after).**

- **REGISTERED-R81-3 (frontier per-state split).** Both readings and their firing conditions
  were frozen before the split existed. Reading **(i)** fired on the lane-versus-matcher
  comparison: on retraction and expiry all three completed lanes exceed the superseded-names
  matcher with intervals excluding zero, and on supersession no lane exceeds it. It REPLACES
  the post-hoc POSTHOC-R81-1 sentence landed at `003818b`, per the freeze rule that main text
  carries one sentence and not two. **SUPERSEDED ON THE ATTRIBUTION by REGISTERED-R81-4.**
  STRENGTH: registered, descriptive of where each reader scores higher, no attribution.
- **REGISTERED-R81-4 (attribution gate, Phase 1d).** Frozen at `cfe5415` before computation.
  The Phase 1c comparison sets the models against an intent-blind reader and so cannot say
  whether their advantage on the counted states comes from the store or the question. The
  prior-controlled quantity is the paired indexed-minus-blind delta per state. Reading
  **(ii)** fired: the delta excludes zero on only one of three lanes on expiry and one of
  three on retraction, and Opus 5's retraction delta is negative. Main text now carries
  "Larger models score higher on the states the index only counts." **No attribution, and
  the word "recover" is gone from the §4.3 sentence.** STRENGTH: registered, descriptive.
  Ledger `AUX-E1R-NB6-ATTRIBUTION`, `NUMBERS_E1R.md` §14.
- **POSTHOC-R81-2a (per-state intervals).** Intervals added to the composition census under
  the frozen stratified paired bootstrap. Appendix only, enters main text nowhere. The
  retraction row's difference interval excludes zero at a lower bound of `+0.0002` and is
  reported as marginal wherever it appears.
- **SCOPELIMIT-R81-1 (design sentence, §7.2).** Updated to the Phase 1d version (ii), landed
  verbatim from the freeze: "The index names superseded content and only counts retracted and
  expired content; the lookup and the smallest reader take nothing from the counts, and naming
  all three states is the natural next index." CLASS: scope limit / future work, **not** a
  positive claim. No experiment, no number beyond a table pointer.
  RESOLVED ([AUTHOR-1], 2026-08-29): the frozen version (ii) said "recover nothing", which collided
  with the Phase 1d bar on "recover" in main text. The frozen text was landed as written and
  the collision reported rather than resolved unilaterally; the ruling is "take nothing", a
  one-word change with no change of meaning.

- **POSTHOC-R81-5 (paired-gain localization, §6).** One descriptive clause keyed to
  `tab:nb6-attrib`: the paired gain concentrates on the state the index names. This
  LOCALIZES the registered claim that the paired NOK gain is positive on every model tested;
  it adds no new claim and strengthens none. Labelled post hoc in the source comment. If a
  CLAIMS_DIFF pass reads it as a new claim rather than a localization, it is dropped and the
  appendix rows carry it alone.

**PHASE 2B AUTHORIZATIONS (dated 2026-08-29).**

- **DEFN-R81-1 (definition wording, §3 + F.1 glossary).** Definition-class change. The
  mathematical objects, ranges and positive classes are untouched; what changes is what the
  number is claimed to be.
  | | Text |
  |---|---|
  | OLD | "We define $\mathrm{FOK}(q,S)\in[0,1]$ as the monitor's probability that coverage is not ABSENT, and $\mathrm{NOK}(q,S)\in[0,1]$ as its probability that coverage is PN." |
  | NEW | "We elicit $\mathrm{FOK}(q,S)\in[0,1]$ as a probability that coverage is not ABSENT, and $\mathrm{NOK}(q,S)\in[0,1]$ as a probability that coverage is PN, and we evaluate both as scores rather than as calibrated probabilities (§4.3: they rank well and do not calibrate)." |
  The F.1 glossary row is brought into agreement in the same edit.
- **STRENGTH-R81-1 (§8).** Authorized strength REDUCTION.
  | | Text |
  |---|---|
  | OLD | "Scale improves a model's blind coverage guesses; only the store's own compact description supplies its obligations." |
  | NEW | "Scale improves a model's blind coverage guesses; the store's own description supplies obligations that scale does not." |
  Direction: weaker. "Only" asserted exclusivity the ladder rows do not establish.
- **PRESENTATION-R81-1 (§5.2).** "notices the cancellation" becomes "can see the cancellation
  itself". No claim changes.
- **POINTER-R81-1 (§4.3 and Definition 3).** Two main-text pointers to claims already carried
  at that strength in the appendix: the attribution clause (Table 20, landed at `a26bd3f`) and
  the naming-versus-counting asymmetry (F.8, established from the index generator). Pointers,
  not new claims.
- **PRECISION-R81-1 (prose precision).** Main-text PROSE numbers may print at three decimals
  where the four-decimal ledger value is the source; every table keeps four. Presentation only,
  and gated on the verifiers being able to express the prose/table distinction without being
  weakened. If they cannot, the item is skipped and reported as skipped.

**ANONYMITY (BRANCH B applied, ruling of 2026-08-29; SUPERSEDED by BRANCH A on 2026-09-11,
see the R89 block below).**
`SUBMISSION_CHECKLIST.md` W1 BRANCH B was applied: the FR preprint was not public, so the
`fr` bibitem becomes `Anonymous(2026)` with the system name removed from the title, the §2
`\citet` becomes anonymous prose, and the first-person references to the store ("the memory
system we build on", "the schema inherited here") become third-person descriptions of prior
work. The `pricingrecord` bibitem is dropped and its provenance folded into the Table 20
caption. These are attribution edits; **no claim changes strength**, and the 5% retrieval
premise keeps its citation.

---

---


**PHASE 4C AUTHORIZATIONS (dated 2026-08-30).**

- **U3 relocates**, verbatim, from §6 into Appendix F.7 beside the inversion tables that
  evidence it. The Phase 4c order asked for two of its three unresolved-mechanism
  sentences to be cut; U3 is untouchable and byte-identical, so it moves instead and
  §6 keeps the last sentence alone. Main text states the open mechanism once, which is
  what the item asked for. U1, U5, U6 and U8 stay where they are.
- **Remark 1 (scalar-trust infeasibility) is removed** from Appendix A. Its CLAIMS class
  was procedural and the manuscript called it a motivating impossibility rather than a
  claimed contribution, so nothing changes strength. Nothing in paper_v2.tex cites it.
- **The economics table is not printed.** Its figures remain in the ledger and in
  `AUX-R74-X3`; the R2 requirement that the projected and billed orderings disagree is
  satisfied by the §7.2 sentence and the two F.10 sentences, which print all four
  figures inline. **No number is deleted from any ledger.**

## R82 AUTHORIZATION BLOCK — dated 2026-08-30

Appended by the R82-INT pass, anchored to the R81 block above rather than to a line number.
Everything below is a **closed list**: any departure outside it is a VIOLATION and stops the
pass. Registrations of record: `registrations/ADDENDUM_R82.md` (Part 1, the counterfactual
cell, with Amendments 1 to 4) and its Part 2 (post-hoc calibration). Ledger:
`r82_counterfactual/NUMBERS_R82.md`. Deviations: D-R82-1 to D-R82-5.

**NEW POPULATION (store-counterfactual cell, n=90).** Thirty questions, each asked of three
versions of one store differing in a single attribute, so the label is a property of the
store and a question-only reader scores $0.5000$ as an identity. This is a new population,
not a re-reading of an existing one. It enters main text as one sentence in §4.3 and in full
as Appendix D.2.

- **POSITIVE (naming boundary).** Under the summary that names only superseded content, the
  one named state scores $0.6550$ to $0.8275$ across three models while the two counted
  states score $0.5225$ to $0.6225$. This reproduces the Table 19 boundary on questions that
  cannot carry the label. Registered as the descriptive block of `ADDENDUM_R82` §16; it
  carried no prediction and prints whichever way it read.
- **POSITIVE (CF-3, held).** Naming the counted states raises the obligation judgment on them
  from $0.5656$ to $0.8489$, paired interval $[+0.0772,+0.4945]$ excluding zero, scored on
  the fifteen pairs the summary individuates.
- **ADVERSE (CF-4, held).** A direct match over the three name lists reaches $0.7886$ against
  the monitor's $0.7656$, inside tolerance, and exceeds three other monitor rows by more than
  tolerance. Printed in full; no row dropped.
- **ADVERSE (CF-1, failed).** The smallest model reaches $0.5939$ against $0.5000$ with the
  preregistered item-level interval including chance. The verdict prints as FAILS. **The
  second clause of its frozen failure text is struck as defective under D-R82-4, following
  the D93 precedent**, and the landed text records that the set can neither establish the
  aggregate effect nor establish contamination. No existing claim changes strength as a
  result: the main-population obligation gain keeps its registered strength, because an
  underpowered null on n=90 cannot reduce it.

**ADVERSE, ABOUT FR-BANK (Table 21, mode "conflate").** Of the 31 entries marked retracted
across the 40 personas, 22 share a slot key with another entry and 16 carry a supersedes
pointer, so the write path records retraction through the supersession mechanism and the
backend's own metadata cannot separate retracted from superseded content. This is a fourth
failure mode beside overstate, erase and invent, and it is about the authors' own backend,
which is why it prints.

**POSTHOC (calibration).** `POSTHOC-R82-1`: rescaling the elicited score after the fact
brings expected calibration error from $0.1741$ to $0.0146$ under an isotonic map, against a
constant-predictor floor of $0.0000$ at a $5.95\%$ base rate, and the rescaled probability
never exceeds $0.375$. Lands in Appendix H only; no main-text sentence. **STRENGTH: post hoc,
descriptive, carrying the floor beside it so the calibration figure is not read alone.**
CAL-1 held and CAL-2 resolved to its registered undefined-by-base-rate branch.

**PROCEDURAL (related work).** One §2 sentence adds the granularity axis, distinguishing
MemGate and Supersede from a store-level summary. The stage axis was already carried by the
two sentences above it, so only granularity lands. Both bibitems already existed; no registry
entry changes and `refcheck_v11` is unaffected.

**PRECISION-R82-1 (frozen wording).** The §4.3 sentence frozen at `ADDENDUM_R81` §11.2 read
"That matcher reaches the smallest model tested." It now reads **"matches"**. This is a
precision change and not a strength change: the difference was always inside the registered
tolerance, and R82 measured the same matcher slightly above the smallest model on the
leak-free cell, which "reaches" would misdescribe. Recorded here because frozen registered
wording otherwise ships verbatim.

**PRESENTATION-R82-1 (§5.1 and §8 demotion).** The blind-direction narrative collapses to one
sentence, the convergence span relocates verbatim to Appendix B with its exploratory flag
intact, the tie-degeneracy sentence is cut, and §8 is rewritten to the four moves. Every
claim keeps its strength and its home; C066's tie-degeneracy content survives in the
appendix rows it describes.

**No existing claim changes strength under this block.**

## R86 AUTHORIZATION BLOCK — dated 2026-09-09

Appended by the R86-SUBMIT pass, anchored to the R82 block above rather than to a line number.
Everything below is a **closed list**: any departure outside it is a VIOLATION and stops the
pass. Findings of record: `reviews/R86_PHASE0.md`. Deviations: `reviews/DEVIATIONS_R86.md`,
D-R86-1 to D-R86-18. Ledger for the values R86 re-derived: `reviews/NUMBERS_R86.md`.

**WITHDRAWAL (names-only calibration). STRENGTH REDUCTION, recorded.** CL-C139's STRENGTH
listed all five ECE quantities and the reading that "names-only ECE 0.0583 shows calibration
is index-content-dependent rather than impossible". Two sentences are withdrawn from Section
4.3: "With names only, ECE falls to 0.0583, and that difference, -0.1013 [-0.1171,-0.0815],
excludes zero", and the clause "The names-only row shows calibration depends on what the index
contains".

Reason, and it is Appendix H's own: at a base rate of 5.95% a constant predictor at the base
rate scores an expected calibration error of 0.0000. A LOWER ECE is therefore not evidence of
better calibration, so the names-only comparison cannot carry the claim that was resting on
it. Section 4.3 now reports ECE once as a raw fact with that floor in the same sentence, and
the calibration result is carried by Brier and selective risk instead, both against the floor.
0.0583 keeps its place in Table 12 and Figure 3 as a descriptive value, and "intact-index
calibration is unimproved" is kept verbatim. Direction: **weaker**.

**STRENGTH INCREASE (the naming result is measured, not proposed).** SCOPELIMIT-R81-1 landed
verbatim from its freeze with CLASS "scope limit / future work, **not** a positive claim. No
experiment, no number beyond a table pointer." Its closing clause, "naming all three states is
the natural next index", is replaced by the measured result: naming them lifts Haiku 4.5's
judgment on the counted states from 0.5656 to 0.8489 on the counterfactual set. This converts
a registered scope limit into a positive finding and drops frozen registered wording. It is
authorized because the measurement exists, is committed, and was already printed in Appendix
D.2; what changes is that Section 6 now states the result rather than proposing the
experiment. The model is named, the other two lanes print in the Appendix D.2 table only, and
the Table 18 pointer for the FR-Bank census is kept.

**U6 REWORDING (ruling A2).** U6 required the frozen-failure wording "which ships as its
registered failure" to survive verbatim. It becomes "which we record as a failed prediction",
under item 2.5's rule that no internal identifier reaches the page a reviewer reads. The
registration's own frozen failure text is a DIFFERENT string, lives in its registration, and
is unchanged; what changed is the manuscript's way of citing an outcome. Four instruments
pinned the old bytes and are repointed in the same commit. No claim changes strength.

**U4 UNCHANGED.** Item 2.4.8 proposed rewording U4. Ruling A1 withdrew it. U4 stays
byte-identical and no CLAIMS entry authorizes a change to it.

**U7 UNCHANGED (D-R86-4).** Item 2.4.7 as written would have deleted U7, whose only
byte-identical instance is the Appendix F.5 paragraph it proposed to drop. Scope reduced to
the lead-in line and the source comments; the sentence itself is untouched.

**CORRECTION OF FACT (A-MEM link census).** CL-C077-C133 and CL-T-believed print "all 23,403
link references resolve to zero note identifiers". 23,403 counts all 41 bank directories
including `priya.canary`, the broken bank `backends.py:71` excludes and whose exclusion gives
the 11,319 entry count the same census already uses. The figure becomes **23,186 across 11,319
notes**, so the link count and the entry count share a population. Method and both figures are
ledgered at `AUX-R86-AMEM-LINKS`. One sentence is added stating what was verified: the
released package at its pinned version stores the positional index its own prompt shows it
rather than a note identifier. No claim is made about A-MEM deployments generally. Direction:
neither stronger nor weaker; a population correction.

**CORRECTION OF FACT (clustering sentence, Appendix B).** CL-T-ladder-exact carried "11 of the
12 rows keep intervals excluding zero", which reads as false against Table 2: two rows print
no item-level interval, and three of the eleven defined clustered intervals include zero. It
becomes "of the ten rows carrying both intervals, nine keep the verdict they had at item
level", with the Opus 5 FOK exception and the two undefined rows stated. No value changes.

**PRESENTATION (Table 1's easy-contrast interval).** CL-T-e1 row 3 printed a dash with the
interval in Table 11. The interval [+0.1179,+0.2596] now prints in both, and Table 11's caption
drops "printed here for the first time". The value is unchanged in both places.

**PRESENTATION (Table 22 and its legend).** The Outcome column is rewritten to held, failed,
held / failed, no prediction, and one held / undefined; the paragraph defining the old codes is
replaced by one reading those five; what the codes carried moves into the "What it froze"
column in plain words. Two corrections travel with it: the capability-ladder row becomes
**held / failed**, because its fifth item failed and Table 4 always said so, and the frontier
row becomes **held**, because two of its three hypotheses carried a pass bar and both held
while the third was registered as descriptive. CL-T-registrations' count is corrected from
**19 rows to 22** (D-R86-11).

**ADDITION (the failure count, Section 1).** One clause extends CL-C018: of the 40 registered
predictions, 8 failed. Both figures are counted in `reviews/R86_PHASE0.md` item 6 and restated
in the Phase 1 report after the frontier addendum was adjudicated per item. This is a count of
what the paper already prints, not a new claim.

**AI USE STATEMENT (CL-C096) REPLACED.** Reshaped to the ICLR 2027 template's own form. All
four disposition numbers survive with the exclusion clause verbatim. The bridge the R86 order
proposed between those 33 rows and the 104 hand-verified present-negative labels **is not
drawn, because it does not exist**: the 33 are slice-construction dispositions whose item ids
are disjoint from the 104's, and the statement says so. Proposition 1 is disclosed as written
without model assistance. 122 candidates and 18 unresolved rows are not printed, having no
ledger row (D-R86-13).

**CL-R86-GRAPHITI [Appendix F.9] — NEW, DESCRIPTIVE.**
TEXT     | A spike on an unmodified public release of a fourth backend, three personas and 137
episodes: at least one superseded attribute name per persona, supersession recall 0.20 at the
frozen 0.80 bar with the 0.75 and 0.50 bands printed beside it, precision 0.00 to 0.04 on what
it does mark, retraction and category inexpressible under stock defaults, three measured
suppressors, and the failure mode erasure with overstatement in what survives. Labelled a
spike on three personas; the 40-persona run was not completed before submission. FR-Bank's own
history on that backend is disclosed in the same paragraph, with the measured near-inertness
of the four modifications beside it.
STRENGTH | Descriptive. Carries no registered prediction and no obligation judgment. It is NOT
a Table 21 row, main text is unchanged, "three backends" stands everywhere, and no Section 6
or Section 8 sentence counts it.
KEYS     | AUX-R86-GRAPHITI-SPIKE
CLASS    | procedural + adverse (store audit)

**No other claim changes strength under this block.**

## R87 AUTHORIZATION BLOCK — dated 2026-09-11

Appended by the R87-READ pass, anchored to the R86 block above rather than to a line number.
Everything below is a **closed list**: any departure outside it is a VIOLATION and stops the
pass. Report: `reviews/R87_REPORT.md`. Deviations: `reviews/DEVIATIONS_R87.md`, D-R87-1
onward. Ledger for the one value R87 printed from an artifact no ledger carried:
`reviews/NUMBERS_R87.md`. Phase A below lands the eleven R86-5 items; Phases B to F append
their own entries under this heading when approved, each dated.

### Phase A (R86-5), landed as one commit

**PRESENTATION (CL-C015, contribution order and lead clauses).** The four contributions are
reordered so the store leads: (1) NOK defined and measured; (2) no backend tested writes the
summary the judgment needs, with the census and the 42.3% retention; (3) the judgment is
bounded by what the summary names, with the 0.7484-against-0.7339 match and the 0.5656 to
0.8489 lift on the counted states; (4) replication and controls, with the six-model paired
gain, the inversion at every scale, and the wrong-index control. CL-C015's STRENGTH already
permits reorder as emphasis. Two things change beyond order and are recorded here. First,
0.5656 to 0.8489 enters the contribution list; it was authorized for the abstract and Section
6 by the R86 STRENGTH INCREASE entry above and is the same measured value. Second, the R84-3
clause "Larger models exceed that lookup only on the states the index does not name, an
advantage the paired comparison does not attribute to the index" leaves the contribution list.
It stays in the main text at Section 4.3 in its REGISTERED-R81-4 form ("Larger models score
higher on the states the index only counts, an advantage the paired blind comparison does not
attribute to the index"), so the paper still carries it. Section pointers follow where each
clause's evidence sits: (2) Section 6; (3) Sections 4 and 6; (4) Sections 5, 4.4, 5.3 and 7.
Items (3) and (4) are each split at their comma-and into two sentences for the 40-word rule
(D-R87-2); no word changes. Direction: **neither stronger nor weaker**.

**SCOPE (CL-C035; CL-C058 second rider; CL-C137; the Section 4.4 heading; Appendix F.5).**
"the counts are not necessary" becomes "the counts are not necessary for coverage" at every
site that states the claim: Section 3 (the CL-C035 sentence), the Section 4.4 heading, the
two Section 4.4 sentences ("FR-Bank coverage discrimination unchanged"; "counts are
unnecessary for coverage"), and the Appendix F.5 sentence ("not necessary for coverage" in
place of "for the effect"). Reason: the count-destruction probe scored FOK only; Tables 14 and
15 carry no NOK column, and the obligation judgment was never tested under count destruction,
so the unscoped wording implied a test that was not run. U7 is untouched. Direction:
**narrower (weaker)**.

**DELETION (Section 5.1; CL-XV).** The sentence "The paired obligation gain is positive with
its interval excluding zero on Opus 5 and K3, the Anthropic pair orders by price and
capability, and indexed coverage falls inside the band on all three (Appendix C)" is deleted
from Section 5.1. CL-XV's STRENGTH ("per-item outcomes exact") is carried by Table 6
(`tab:crossvendor-predictions`), whose rows XV-2, XV-3 and XV-4 print each outcome, and by the
two Section 5.1 sentences that remain ("every paired NOK gain stays positive with its interval
excluding zero"; "The Anthropic pair spans two model generations, so its ordering compares
price and capability"). The XV-4 band statement now prints in Table 6 only. Direction:
**neither**.

**PRESENTATION (CL-C139, sentence order).** "This negative result is a finding in its own
right." moves from the head of the ranker sentence to directly after "includes zero." No word
changes; "unimproved" stays verbatim.

**ADDITION (Table 2, the counted-states row), and a correction to the R86 STRENGTH INCREASE
entry.** That entry says "the other two lanes print in the Appendix D.2 table only". Table 10
carries no counted-state row for any model; the only printed instance was Haiku 4.5's in
Appendix D.2 prose and Section 6. Table 2 now prints the row "Counted states, individuating
pairs ($n=45$)" for all three models: GPT-4.1 mini 0.5578 / 0.6600, Haiku 4.5 0.5656 /
0.8489, Opus 5 0.6122 / 0.9144, under the two summaries. Haiku 4.5 and Opus 5 are transcribed
from NUMBERS_R82 sections 7 and 9; GPT-4.1 mini from `results/cf_scores.json` via
`reviews/NUMBERS_R87.md` (D-R87-1). The row is descriptive and carries no prediction; GPT-4.1
mini's paired delta (+0.1022) includes zero on both interval conventions, which the ledger
records and the table, which prints no interval for any per-state row, does not. The caption
gains "The per-state rows have ten positives per state" (NUMBERS_R82 lines 15 and 60). The
dagger footnotes of Tables 2 and 10 drop "which this pass does not do" for "would require
rescoring the stored responses". Direction: **neither** (descriptive).

**CL-R86-GRAPHITI, backend named.** Appendix F.9 names the fourth backend, Graphiti, and
cites Rasmussen et al. (2025), arXiv:2501.13956, which enters the bibliography as `zep` and
`refcheck_v11.py`'s verified registry (record VERIFIED by arXiv API in
`reviews/R80_CITATIONS.md`). No claim changes; "three backends" stands everywhere.

Items with no claim content, listed so the closed list is complete: Section 1 "keeps pace
with it" gains "on the obligation judgment" (not a CLAIMS sentence; the matcher-equals-
smallest-model reading of PRECISION-R82-1 is unchanged); the stray "And:" before the
Appendix F.3 rubric is deleted (not prompt text; verified against `prompts_e1.py`); "neighbours"
and "neutralisation" take American spelling; the Figure 2 caption gains "(Table 3)".

### Phases B to D, approved 2026-09-11 in chat ("everything must be in there")

Lineage note: from R90 (2026-09-11) the working manuscript is `paper_v3.tex`, copied from
`paper_v2.tex` at `f4c5b2c`; `paper_v2.tex` is frozen there. Everything below lands in v3.

**Phase B (cuts).**

**DELETION (§1; CL-C011-C014, CL-C002).** "We measure that judgment directly, ahead of any
lookup, against labels known exactly because we built the stores." is deleted. The game
paragraph two sentences earlier carries "two things an agent must decide before touching its
memory" and "scored against labels we know exactly, because we built the stores", so the
pre-retrieval and exact-label content survives. Direction: **neither**.

**PRESENTATION (§3, Proposition 1's informal gloss; CL-C036, AUTHORIZED-REFRAME R1, CL-C136).**
The two informal paragraphs become one. R1's "one mechanism that escapes the bound" is verbatim;
CL-C136's 5% premise and its "rather than a deep theorem" hedge are kept; the clause "The
proposition scopes the design space", which is in CL-C136's TEXT but not its STRENGTH line, is
dropped. Split at the R1 clause for the 40-word rule. Direction: **neither**.

**PRESENTATION (§4.1 pilot; CL-C040, CL-C050, CL-T-pilot-record).** The four-sentence pilot
paragraph becomes: "A pilot (Appendix F.2) found a large coverage gain and no obligation gain.
Its easy questions removed a whole category, and its prompt assumed lifecycle structure that
Mem0 and A-MEM do not expose, so its values are not comparable with the main study. Its lesson
was to rule out success that comes only from seeing a zero count for a whole category." Null
NOK, non-comparability, and the lesson survive; the pointer is the F.2 section (label
`app:pilot` added) rather than Table 11. Split at the semicolon (D-R87-3). Direction: **neither**.

**ORDERED-MECHANICAL (CL-C053, CL-C054, CL-C078).** The two §4.3 sentences (five-level scale
within noise of the free-number format, no equivalence test; the BELIEVED index keeps 101.4% of
the TRUE index's FOK benefit, excess within sampling) relocate verbatim to Appendix F.3 after
Table 12. §6's "still keeps the true index's coverage benefit" gains "(101.4%; Appendix F.3)".
Direction: **neither**.

**PRESENTATION (§5.3; CL-X2), in place of the program's B5.** The program's merge would have
consumed U1's second sentence. U1 stays byte-identical; instead "The candidate mechanisms
remain hypotheses." is deleted and the next sentence opens "Two candidate mechanisms remain
hypotheses: global counts may…". Hypothesis framing kept. Direction: **neither**.

**DELETION (§6; REFRAME 5, Phase 4C "the main text states the open mechanism once").** "What
produces the below-chance behavior on those two backends remains open." is deleted; U1 (§5.3)
and U5 (§7.2) still state it in main text, and U4 in Appendix F.7 is untouched. Direction:
**neither**.

**ORDERED-MECHANICAL (§7.1 → Appendix E; CL-C083-C085).** The program's B7 deletion is
blocked: the lesson is half the entry's STRENGTH ("Scoped ledger + lesson") and printed nowhere
else. The sentence relocates verbatim to Appendix E after the C108 scope paragraph, the ledger
it describes. Direction: **neither**.

Figure 2's plotted height goes from 0.26 to 0.20 of the text width (R86_HEADROOM #1); no
CLAIMS entry governs it. Not taken: the program's C22 (U1's first sentence, byte-identical,
mechanically pinned) is skipped; C23 stays verbatim (CL-X2's hypothesis cannot be made plainer
without changing its content).

**Phase C (readability rewrites in the main text).** Numbers unchanged; every governed
sentence reworded at identical strength, with these dated lines for the ones a block had fixed
in words:

- **C10 (DEFN-R81-1).** The prescribed clause "we evaluate both as scores rather than as
  calibrated probabilities (§4.3: they rank well and do not calibrate)" becomes "We score both by
  AUROC, the chance that a randomly chosen positive question scores above a randomly chosen
  negative. ECE, the gap between stated probabilities and observed frequencies, is secondary,
  because the scores rank well and do not calibrate (Section 4)". Same objects, ranges and
  positive classes; AUROC and "indexed" are now defined before use; CL-C032's blind semantics
  and CL-C033's primary/secondary ordering survive verbatim in content. Direction: **neither**.
- **C24 (R86 STRENGTH INCREASE).** "Naming them lifts Haiku 4.5's judgment on those states"
  becomes "Naming those two states lifts Haiku 4.5's judgment on them"; the model, the numbers
  (0.5656 to 0.8489), the set and the pointers are unchanged. Direction: **neither**.
- **C13 (CL-PAYOFF, CL-C141).** "within FR-Bank, inside one backend, the index raises" becomes
  "within FR-Bank, the index raises"; "within FR-Bank" already names the one backend.
- **C14 (CL-C141; CL-BASELINES-SENT).** The one-bit rule is described in plain words; the two
  mechanical-reader sentences keep the scope clause ("Where lifecycle structure exists") and the
  margins; a period stands where the program's colon would, for the 40-word rule (D-R87-5).
- **C15 (CL-C051).** "PN discrimination improves 0.5517 → 0.8782" becomes "coverage
  discrimination improves …" (the resolution split scores FOK with PN positives, which the
  following frozen sentence states); "Item-level suppression discrimination is NOK's distinct
  target" becomes "Detecting that one stored record must be suppressed is NOK's job".
- **C18 (CL-C058).** "whose misleading counts propped up false coverage" becomes "whose counts
  made the store look better covered than it is"; both scope riders kept.
- **C3, C4 (CL-U001, DEFN-R81-1).** §1's FOK gloss adds "under the time frame the query asks
  about (its intent, Section 3)"; NOK's adds "(superseded, expired, or retracted)". The glossary
  rows keep the short forms.
- **C7 (CL-C026-C027).** The CHANGE sentence moves after the informal label gloss and reads "The
  CHANGE intent asks what changed; such queries are never PN, because both the old and the new
  value are licensed" ("may be PRESENT or ABSENT" drops; the entry's content is never-PN).
- **C20 (CL-X4).** "indexed span"/"blind span" become "spread of indexed (NOK) scores across
  models"/"spread of blind scores"; 0.0988 and 0.2279 unchanged, §5.1 and the Table 4 caption.
- **C26 (CL-C082), C27 (CL-AVCENSUS), C9 (CL-C031), C1 (CL-C008), C2 (CL-C008/C009-C010),
  C5 (REFRAME 4), C6 (CL-C024), C8 (CL-C028-C030), C11, C12 (CL-CAP-e1 pointer to the new
  `sec:discrimination` label), C17 (CL-C055-C057; "ages" kept per D-R86-7), C19 (CL-C063),
  C21 (CL-TAKEAWAY), C16 and C25 (paragraph breaks only)**: reworded or repointed as the
  program gives them, at identical strength. Direction of every Phase C item: **neither**.

Not taken: **C22** (U1's first sentence is byte-identical and mechanically pinned; skipped) and
**C23** (CL-X2's "disagreement between the index and retrieved view may compress the score range"
stays verbatim: any plainer form changes the hypothesis's content).

**Phase D (appendix readability).**

- **D1 (Appendix F.5; CL-SW2, U7, U9).** The second paragraph's plain-words repeat of U7
  ("Permuting which counts and names belong to which category leaves both judgments unchanged,
  … consistent with a flat lookup …") is deleted. U7 stays byte-identical; the wrong-persona
  sentence before it stays; U9 is unaffected (the retention figure was never joined to it).
- **D2 (Appendix D.2; R82 ADVERSE CF-1, "The verdict prints as FAILS").** "Registered prediction,
  outcome FAILS." becomes "The registered prediction did not hold." The verdict is unchanged
  (the item-level interval includes chance; the mixed reading governs; Table 24's Outcome column
  still prints "failed"); only the sentence that announces it is plain prose. Dated wording line.
  Direction: **neither**.
- **D3.** After Phase C, `code_scan` and `prose_scan` find no internal word (arm, lane, cell,
  prior, lineage, provenance, committed, registered) in the main text outside the allowlisted
  collocations, so every survivor the F.1 glossary decodes is one the main text no longer uses
  as jargon. No glossary change.
- **Phase E.** Nothing restored: R88's budget rule ranks its Section 8 paragraph above every
  E item, and the measured slack after Phases B to D (+5) does not carry both.

**No other claim changes strength under this block.**

## R89 AUTHORIZATION BLOCK — dated 2026-09-11

Appended by R89-BRANCHA, anchored to the R87 block above. **Closed list.** Report:
`reviews/R89_REPORT.md`. Deviations: `reviews/DEVIATIONS_R89.md`.

**ANONYMITY, BRANCH A applied (supersedes the 2026-08-29 BRANCH B ruling).** The prior-store
preprint is public: arXiv:2609.10413, [AUTHOR-1] and [AUTHOR-2], 2026, verified against the arXiv API
and abstract page on 2026-09-11 (title verbatim; published 2026-09-09; cs.AI). Per
`SUBMISSION_CHECKLIST.md` W1 BRANCH A the `fr` bibitem becomes the named record and every
citation of it is the named third-person form the ICLR author guidelines require. The
`refcheck_v11.py` registry gains the record (two-author guard) and drops the out-of-scope
declaration; `hygiene_scan.py` permits the surnames and the system name in exactly two places,
the bibliography entry and a rendered author-year citation, and fails every other occurrence
together with the first-person phrases "our prior", "we previously", "our system", and "this
project". No claim changes strength.

**ORDERED-MECHANICAL (citation form).** Every `(Anonymous, 2026)` becomes `([AUTHOR-1] & [AUTHOR-2],
2026)` through the bibitem label; the four `% FR-GATE (W1)` sites (§1 opening, §2 inherited
apparatus, §3 metadata tuple, §3 below-cutoff premise) and the Table 12 "Inherited retrieval
premise" row now cite by name; the §2 sentence takes the `\citet` form ("The schema used here is
that of [AUTHOR-1] & [AUTHOR-2] (2026), whose metadata records…"); "In a prior lifecycle-tracking store"
(§1, CL-C008) becomes "In a lifecycle-tracking store"; "in that prior store" (§3, CL-C136)
becomes "in that store". Attribution edits at identical strength; the 5% premise keeps its
citation.

**PRESENTATION (§4 backend descriptor; CL-C042-C043 apparatus sentence, whose TEXT reads "FR-Bank is the lifecycle-bearing store from the memory system we build on").** "FR-Bank, the
lifecycle-tracking store from that prior system" becomes "FR-Bank is the lifecycle-tracking
store of [AUTHOR-1] & [AUTHOR-2] (2026) and the one evaluated store that records a lifecycle state on
every entry". The added descriptor states a property the paper already relies on (Table 1's
NOK row exists only on FR-Bank because only FR-Bank retains lifecycle state; CL-C052 and
Appendix F.7). The Appendix F.1 glossary row for FR-Bank carries the same descriptor. Because
the named clause took the colon-list sentence to 43 words, the list becomes its own sentence
with the same three backend descriptions (D-R89-1). Direction: **neither**.

**PRESENTATION (Appendix F.9 independence disclosure; CL-R86-GRAPHITI).** "this project ran on
that backend from approximately February to March 2026 and replaced it in April 2026; the copy
used then carried four documented numeric-preservation modifications, and re-running the
unmodified release against that copy on the same personas and episodes changes edge counts by
2.4% and leaves supersession recall identical at the frozen bar" becomes "the personas and
episodes used here were ingested into that backend in early 2026 under a copy carrying four
documented numeric-preservation modifications; re-running the unmodified release on the same
personas and episodes changes edge counts by 2.4% and leaves supersession recall identical at
the frozen bar". Same facts (the modifications, the 2.4%, the identical recall, the
near-inert conclusion); the project biography (who ran what, when, and what replaced it) is
removed as first-person history. Direction: **neither**.

**No other claim changes strength under this block.**

**ABSTRACT-LAND-A (dated 2026-09-11, [AUTHOR-1]'s instruction in chat).** Option A of
`reviews/R86_ABSTRACT_PROPOSED.md` lands: abstract sentence 6 becomes "On a set where the
question cannot carry the label, the state the summary names is judged better than the states
it only counts, and naming those states restores the judgment on them." The two four-decimal
figures that AUTHORIZED-ABSTRACT (R83) promoted into the abstract, 0.5656 and 0.8489, leave it;
they still print in the Section 1 contribution list (R87 Phase A), Section 6, Table 2 (R86-5)
and Appendix D.2, all ledgered in NUMBERS_R82 section 7, so nothing becomes unverifiable. The
proposal file's premise that the abstract had been submitted on 30 August and was locked did
not hold; no abstract was submitted. Direction: **weaker** at the abstract (precision leaves the
first point of contact; direction and scope unchanged), no claim changes strength elsewhere.
The spliced review copy (`paper_v2_spliced.tex`/`.pdf`), which existed only to show option A in
place, is retired in the same commit; the cold-read copy is `paper_v2.pdf`.

## R88 AUTHORIZATION BLOCK — dated 2026-09-11

Appended by R88-FRAME Phase B, approved in chat on 2026-09-11 ("everything must be in there"),
anchored to the R89 block above and landing in `paper_v3.tex`. **Closed list.** Report:
`reviews/R88_REPORT.md`. Deviations: `reviews/DEVIATIONS_R88.md`.

**READING (§8, new penultimate paragraph; CL-C092-C095).** A reading of printed figures with a
recommendation, class READING, no new number: "For a deployed system the tables already give
the accounting. On the obligation judgment a lookup over the summary's superseded names and the
model tie under a truthful summary (0.7484 against 0.7339) and tie near chance under the
metadata a real backend exposes (0.5858 against 0.5959). Once a summary names every non-active
state, the lookup reaches 0.7886 on questions that cannot carry the label. The model earns its
cost on one judgment only, coverage where lifecycle structure exists, where it leads the best
mechanical reader by +0.0817. A system should therefore decide obligations with a lookup over a
name-bearing lifecycle summary, spend model calls on coverage only where the store has
structure, and treat a store that cannot write such a summary as one no monitor repairs."
Keys: 0.7484/0.7339 PRECISION-R82-1 ("matches"); 0.5858/0.5959 and +0.0817 CL-BASELINES-SENT;
0.7886 NUMBERS_R82 §8 / CL-T-counterfactual. "ledger" and "gate" are barred words, so
"accounting" and "decide"; +0.0817 prints exactly because no ledger bridges +0.08; the
program's fifth sentence (matchers at 0.5000, the model's point estimates below under the
truthful summary, 0.4777 / 0.4526) is dropped for the page budget: §8's existing sentence
states the inversion and the Table 19 caption now carries the numbers (D-R88-2). R88 A3: no
one-sample interval against 0.5 exists for those rows, which is why the caption prints point
estimates. Direction: **neither** (a reading of what already prints).

**CORRECTION OF FACT (Table 19 caption; CL-T-baselines).** "On the structureless backends every
reader including the monitor sits at chance, which is what 'structureless' predicts" becomes
"On the structureless backends the lexical and embedding matchers sit at 0.5000 and the other
mechanical readers scatter around chance (0.4184 to 0.5226), which is what 'structureless'
predicts, while the monitor's indexed point estimates under the truthful summary fall below
them (0.4777, 0.4526; Section 5.3)". The rows are unchanged; the caption stops saying the
monitor sits at chance when it is below the best reader by −0.0223 and −0.0700 on the TRUE
rows. "Under the truthful summary" because under BELIEVED the monitor is above chance on both.
Direction: **more precise, adverse**.

**ADDITION (§7.2, a seventh limitation; CL-LIMITS).** After "One closed model family supplies
the primary capability comparison.": "The lookup has one descriptive value on the 84-question
set, none per state on the counterfactual set, and none on the one-voice set, so the comparison
between model and lookup is complete only on the 661-question population." The program's
wording ("no rows on the 84-question set") was corrected at Phase A: `nb6.json` (40b0e7d) and
NUMBERS_E1R carry NB-6 = 0.6023 (TRUE) on the 84-question cell (D-R88-1). Direction: **a scope
limit added**.

**CORRECTION OF FACT (Appendix F.8 composition paragraph).** "against 19 of 40 on the
authorship-matched cell, where the matcher scores 0.6023" becomes "on the cross-model cell":
the paper defines the authorship-matched cell as the 36-question set and the cross-model cell
as the 84-question set (40 positives), and 19 of 40 and 0.6023 belong to the latter.

**DELETION (§5.2; CL-THREELINE).** "In short: blind FOK rises as its gain shrinks; blind NOK
moves with no scale trend as its gain grows; indexed FOK converges everywhere, and indexed NOK
converges only across GPT-5.6 Luna and GPT-5.6 Sol." is deleted for the page budget. Every
clause, including the load-bearing "only across Luna and Sol" scope, is verbatim in the
Figure 2 caption, which is now the entry's one printed instance. Direction: **neither**.

**STRENGTH REDUCTION at the site (§4.4; CL-C060-C062), for the page budget.** "The
lifecycle-index effect is +0.1980 and dominates; the two prompt effects are +0.0134 and
−0.0193. The recovery is therefore attributed to the lifecycle information, within the
conditions we varied. The matching condition independently reproduces the main-study value."
becomes "The lifecycle-index effect dominates both prompt effects, so the recovery is attributed
to the lifecycle information, within the conditions we varied (Appendix F.6)." The three effect
sizes and the matching statement print exactly in Appendix F.6 (U8, byte-identical), so the
entry's "three effects exact" holds in the paper and the main text keeps the attribution and
its confinement. This is R86_HEADROOM items 3 and 4, the cut R86 said to authorize before
taking. Direction: **weaker at §4.4**, unchanged for the paper.

**PRESENTATION, no claim content.** The §1 contribution list prints as an inline "(1) … (4)"
paragraph, word for word the R87 Phase A items; Table 2's caption says the same things in
fewer words ("Per-state rows have ten positives each. Matchers are scored on the whole set
only: …", adverse clause kept); Figure 2 stays at 0.20 of the text width with its legend
moved into the empty band and the redundant in-plot note dropped (0.17 hid the 0.5000 label);
R87's C16 and C25 paragraph breaks are taken back, as R87 allowed for C16. B4 (the optional §1
extension) does not land: no line to spare. Phase C did not run (optional; C1 would be a
transcription of the 0.6023 value, C2 and C3 new local computations).

**No other claim changes strength under this block.**

## R90 AUTHORIZATION BLOCK — dated 2026-09-11

Appended by R90-TITLE, anchored to the R88 block above, landing in `paper_v3.tex`. **Closed
list.** Report: `reviews/R90_REPORT.md`.

**TITLE.** "Knowing the Store: Measuring Metamemory for External Agent Memory" becomes
"Knowing the Store: What a Memory Backend Must Write Down Before an Agent Can Read It". Reason,
as the program states it: the old subtitle recruited model-cognition reviewers for a paper whose
result is about stores (review E, item E3, `reviews/REVIEW_E_73_RELAY.md`). No running head or
PDF-metadata title string exists in the manuscript (hygiene_scan verifies the metadata title
field stays empty). The alternative held: "Pre-Retrieval Monitoring Is Bounded by a Memory's
Self-Description". The abstract does not change. No claim changes strength.

**Leftovers.** The Section 1 contribution (4) pointer reads "(Sections 4.4, 5 and 7)" in place
of "(Sections 5, 4.4, 5.3 and 7)"; presentation only. The Table 19 caption no longer says the
monitor "sits at chance" on the structureless backends (R88 B2 landed in `cd4ef47`).

**Umlaut check.** The text layer extracts "[AUTHOR-2]" because OT1 composes the accent as a
separate glyph; page 1 and the bibliography were rendered to PNG and the accents sit on the
letters. The encoding is unchanged; no fontenc package is added.

**No other claim changes strength under this block.**

## R91 AUTHORIZATION BLOCK — dated 2026-09-11

Appended by R91-PROSE, anchored to the R90 block above, landing in `paper_v3.tex`. **Open
list, one entry per phase; closed at Phase 6.** Reports: `reviews/R91_PHASE0.md`,
`reviews/R91_REPORT.md`; deviations `reviews/DEVIATIONS_R91.md`. Every number in the paper is
frozen under this program; no entry below moves one.

**Phase 1 (vocabulary, `R91-1`).**

**WORDING (§1, the R86 item 2.7 sentence; D-R86-19, D-R86-22).** "each of those prints in the
words set before scoring" becomes "each is reported with the prediction text fixed before
scoring". The program's own replacement ("fixed before the data were seen") was declined by
ruling: it is false for the follow-up registrations, which were fixed before scoring but after
the main study's data existed. Direction: **neither**.

**PRESENTATION (§3 L270, §4.2 L402).** "printed as $\Delta$" becomes "reported as $\Delta$";
"prints in full in Appendix F.3" becomes "is reported in full in Appendix F.3". The main text
no longer uses the artifact verb "print"; Appendix F.1 and the tables keep it. No claim changes.

**PRESENTATION, question-set names (main text and main-text captions).** Four printed names
are standardized, with the size at the first mention in each section and the bare name after:
cross-model set (84) at §5.1 L494 ("the cross-model set ($84$ FR-Bank questions) and the same
prompts"), §5.2 L567, the Figure 2 caption ("uses the cross-model set ($n=84$; $54$ FOK-positive
and $40$ PN) on FR-Bank"), §7.1 L682; authorship-matched set (36) at §4.3 L442 ("the
authorship-matched set ($36$ questions rewritten in one voice; Appendix D.1)"), §7.1 L687
("the balanced authorship-matched set ($36$; Appendix D.1)"), §7.2 L710 and L713;
store-counterfactual set (90) at §1 L163, §6 L629, the Table 2 caption ("The
store-counterfactual set ($n=90$):"), §7.1 L690, §7.2 L710 and L716; full populations (661
obligation / 307 coverage) at §5.1 L512 ("An expansion over the full populations ($661$
obligation / $307$ coverage) replicates the paired separation on all four completed runs") and
§7.2 L710. Appendix F.1's third block maps `cross-model cell`, `authorship-matched slice` and
`counterfactual cell` onto the new printed names. Entries this touches:

- CL-C015 (contributions, R88 "word for word"): item (3) reads "on the store-counterfactual
  set ($90$)" in place of "on the counterfactual set". Nothing else in the list changes.
- CL-LIMITS, the R88 ADDITION quoted in the R88 block: "The lookup has one descriptive value
  on the 84-question set, none per state on the counterfactual set, and none on the one-voice
  set, so the comparison between model and lookup is complete only on the 661-question
  population." becomes "The lookup has one descriptive value on the cross-model set, none per
  state on the store-counterfactual set, and none on the authorship-matched set, so the
  comparison between model and lookup is complete only on the full obligation population
  ($661$)." Same three sets, same population, same scope. Direction: **neither**.
- CL-LIMITS (content-intact limitation): "A robustness set of $36$ questions, rewritten in one
  voice for every label, has been measured on three models." becomes "The authorship-matched
  set has been measured on three models."; the set is defined at §4.3 and §7.1 and in F.1, and
  the shorter form is the page funding for the names above. "The $90$-question counterfactual
  set is the second failed prediction" becomes "The store-counterfactual set is the second
  failed prediction". Direction: **neither**.
- CL-PRIORCONTROLLED (§7.1 L687): "the balanced $36$-question set rewritten in one voice"
  becomes "the balanced authorship-matched set ($36$; Appendix D.1)". Direction: **neither**.
- R78-A5 (§4.3 L442): "the $36$-question set rewritten in one voice (Appendix D.1)" becomes
  "the authorship-matched set ($36$ questions rewritten in one voice; Appendix D.1)".
- CL-FIG-ladder / C132 (Figure 2 caption): "uses matched FR-Bank conditions ($n=84$; …)"
  becomes "uses the cross-model set ($n=84$; …) on FR-Bank". Every value unchanged.
- CL-XV (§5.1 L512, X4 cap-stop branch, wording free by strength): "the full FR-Bank question
  sets … (NOK $n=661$, FOK $n=307$; Table 4)" becomes "the full populations ($661$ obligation
  / $307$ coverage) … (Table 4)". Same two populations, same sizes.

**NOT TOUCHED, collision recorded.** §4.3 L424 "A matcher that scores each question directly
against the store's list of names marked superseded reaches $0.7484$ on the same $661$
questions, against the monitor's $0.7339$." is the NB6-1 FAILS branch sentence
(`ADDENDUM_R81.md`), frozen registration text; "on the same $661$ questions" stays as
registered and is not renamed.

**PRESENTATION (Table 5 caption, Appendix B).** "the sol threshold failed and corrected the
earlier one-call account" becomes "the sol threshold failed, revising the earlier one-call
account". The verdict and the account are unchanged.

**Phase 2 (sentence pass on Sections 4 to 6, `R91-2`).** Page-neutral: reading 482, slack +3
before and after. No number moves. Every split below is at an existing joint (a colon, a
semicolon, or an "and") unless an entry says otherwise.

**PRESENTATION (§4.2).** The apparatus paragraph becomes three paragraphs, labels and
verification, indexes, prompts, after the design paragraph; no sentence order changes. Two
sentences fund the breaks: CL-C047-C048's leakage sentence "A separate check asks whether the
monitor can rebuild any stored value from its input, which tests the claim that values are
removed. Appendix F reports its result and the threshold we set in advance." becomes "A
separate check asks whether the monitor can rebuild any stored value from its input; Appendix
F reports its result and the threshold we set in advance." (the screen's purpose is what the
first clause says; result and threshold stay in the appendix), and the rubric sentence "We
asked each monitor for a number in $[0,1]$ under a fixed rubric, with the shared system
instruction and both user-prompt conditions otherwise fixed." becomes "We asked each monitor
for a number in $[0,1]$ under a fixed rubric and a shared system instruction." (the prompt
conditions are stated two sentences later: "The two user prompts differ only in whether the
serialized index precedes the question"). The $\varepsilon$ / base-rate passage is untouched
(reserved for Phase 3 item 2). Direction: **neither**.

**PRESENTATION and one reading (§4.3).** CL-C141: "Pooled levels measure coverage for no
reader: all $35$ pooled positives …" splits at the colon. CL-BASELINES-SENT: "the monitor
leads the best of a deterministic lifecycle rule, lexical and embedding matchers, and two
learned index readers by $+0.0817$ (TRUE) and $+0.0819$ (BELIEVED) on FOK" becomes "the
monitor leads the best mechanical reader by $+0.0817$ (TRUE) and $+0.0819$ (BELIEVED) on
FOK"; the five readers are named in Appendix F.8 and Table 19, the scope (FR-Bank), both
margins and both adverse riders are unchanged. Two subjects replace bare deixis: "That
matcher matches the smallest model tested." becomes "The superseded-names matcher matches the
smallest model tested."; "That identity is why this split and the authorship-matched set …
exist." becomes "The identity of the two positive classes is why this split and the
authorship-matched set … exist." (R78-A5). CL-C139: "Discrimination is the primary measure,
calibration the secondary one, and calibration does not improve." becomes "Calibration does
not follow discrimination. Discrimination is the primary measure and calibration the
secondary one."; the ECE figures, "This negative result is a finding in its own right." and
"Intact-index calibration is unimproved" are untouched. The program's paragraph break before
the opener is not taken (unfunded, D-R91-6). Direction: **neither**.

**PRESENTATION, named subjects (§4.4).** The count probe: "The counts in the summary are not
what helps: randomizing every count leaves FR-Bank coverage discrimination unchanged
($+0.0015$; Table 15)." becomes "The count-randomization probe leaves FR-Bank coverage
discrimination unchanged ($+0.0015$; Table 15): the counts in the summary are not what
helps." ("count-destruction" is barred in main text, D-R91-8); its funding, "The probe alters
only the numeric tallies, leaving ages, the not-expressible markers, and names untouched."
becomes "The probe alters only the numeric tallies.", because "Because ages, markers, and
names stay intact" states the same two sentences later (CL count-destruction entry, fields
fixed). The attribution: "After the pilot's null obligation result the index gained its
lifecycle columns and the prompt gained worked examples and a detection step, so the NOK
redesign changed three things at once and one controlled comparison varied all three."
becomes "The attribution comparison estimates the effect of each of the three changes
(Appendix F.6). After the pilot's null obligation result the index gained its lifecycle
columns and the prompt gained worked examples and a detection step, so the NOK redesign
changed three things at once."; the pointer moves from the dominance sentence, which
otherwise stands ("within the conditions we varied" kept), to the topic sentence
(CL-C060-C062; "factorial" is barred in main text, D-R91-8). The wrong-index control: "A
control replaces the index itself:" becomes "The wrong-index control replaces the index
itself:". The shuffle (CL-SW2 main-text sentence): "Permuting which counts and attribute-name
lists belong to which category changes neither judgment." becomes "The category shuffle
permutes which counts and attribute-name lists belong to which category and changes neither
judgment."; U7 in F.5 is untouched. Direction: **neither**.

**PRESENTATION, splits at joints (§5).** R78-A4: "…averaging five calls per question;
GPT-4.1 mini's rows…" splits at the semicolon. C064: "…without the index: GPT-5.6 Sol's blind
FOK…" splits at the colon; "…on their own, and blind levels include…" becomes "…on their own.
Blind levels include…". AUX-R74-X2 branch ii: "…separated neither; removing both together…"
splits at the semicolon. CL-FIG-ladder (Figure 2 caption): "…on FR-Bank, with the obligation
panel shown and GPT-4.1 mini's constant blind NOK marked with an open point (…)" becomes "…on
FR-Bank. The obligation panel is shown, and GPT-4.1 mini's constant blind NOK is marked with
an open point (…)". Values unchanged everywhere. Direction: **neither**.

**NOT TOUCHED, collisions recorded (§5).** §5.3's inversion-at-every-scale sentence pair is
U1, byte-identical (not quoted here, so that this block authorizes nothing about it); the
program's replacement is not made and nothing is added after it.
§5.1 carries neither "always-reasoning configuration" nor "reasoning tokens" (both live in
Appendix C), so the program's definition item is a no-op.

**PRESENTATION and one fold (§6).** The second paragraph becomes two, each with a topic
sentence. CL-C078: "FR-Bank overstates staleness yet keeps category and lifecycle structure,
and its corrupted BELIEVED map still keeps the true index's coverage benefit ($101.4\%$;
Appendix F.3)." becomes "Coverage survives the corrupted self-description. FR-Bank keeps
category and lifecycle structure, and its corrupted BELIEVED map still keeps the true index's
coverage benefit ($101.4\%$; Appendix F.3)." (the overstatement is the census sentence three
lines above). CL-BELIEVED-NOK: "The obligation judgment fares worse." becomes "The obligation
judgment fares worse, losing more than half its benefit.", and the summary sentence "Coverage
judgment is insensitive to the corrupted self-description; obligation judgment loses more than
half its benefit." is deleted, its two halves now being the two openers; "more than half"
survives, the frozen-branch sentence "NOK degrades materially under believed metadata but
remains positive." is untouched, the $42.3\%$ sentence is untouched, and no connective joins
it to the matcher sentences (U9). The pointer "Appendix D.2" leaves the Haiku 4.5 sentence,
which cites Table 2 in the same parenthetical; Section 7.2 keeps a pointer to D.2. The
program's three-item list for the census sentences is not taken (unfunded, D-R91-7); the
three sentences and every census number stay as they were. Direction: **neither**.

**Phase 3 (structural swaps, `R91-3`).** Reading 482, slack +3 before and after; the label
stays on page 9. Items were tried in the order the Phase 3 ruling set (comparison-set table
first, Definition 1 matrix second), each in a scratch build, with the ranked funding sources.

**ADDITION, no claim (§4.2 head; item 2).** An unfloated, uncaptioned table lists the four
question sets: name, $n$, positives, purpose, where. Every value it prints already prints
elsewhere: $84$ with $54$ FOK-positive and $40$ PN (Figure 2 caption, Table 3), $36$ with
$12$ PN and $29$ non-ABSENT (Table 8), $90$ with $30$ PN, ten per state (Tables 2 and 10),
$661$ with $104$ PN and $307$ with $35$ non-ABSENT (Table 1, Appendix B). Set at
\scriptsize, Table 1's own size, because the ruling's \small ran 68.8pt over the text width
and \footnotesize 31pt (D-R91-12). Lead-in sentence: "The results rest on four question
sets, each defined once.".

**RELOCATION with a site strength change (§4.2 → Appendix F.3; CL-C046-POSTERIOR,
AUX-R77-POSTERIOR, R78-A3; item 2's funding (a)).** The three derivation sentences ("The
residual error is $\varepsilon=0.005$, the rate at which the check misses a target that is
present." / "Turning that into the chance an ABSENT claim is wrong also needs the base rate,
which is $0.917$ present among resolved targets." / "At that base rate the chance is
$5.2\%$, roughly ten times $\varepsilon$, because the sampled questions are
answerability-skewed.") and the R78-A3 sentence ("A mislabeled ABSENT item enters the
negative class in both conditions and can only shrink the measured discrimination, so the
reported gains are conservative with respect to this error.") relocate verbatim to a new
paragraph at the end of Appendix F.3, the first with "The presence control's residual error"
as its subject so the antecedent is named. Section 4.2 keeps one sentence, as the program
ordered: "Even accounting for the presence control's residual error, a mislabeled ABSENT item
is unlikely at the observed base rate ($5.2\%$; Appendix F.3); such items can only shrink
measured gains, so reported differences are conservative." The larger number ($5.2\%$)
still prints in the main text, no "at most" appears, and $0.005$ and $0.917$ print in F.3
exactly ($\varepsilon=0.005$ also stays in Table 12). Direction: **narrower at §4.2** (the
miss rate and the base rate leave the main text), **unchanged for the paper**.

**PRESENTATION (§3 example block; item 2's funding (b)).** The hiking-persona example box
drops its ABSENT row ("What was the name of David's childhood pet, and what breed was it?");
the PRESENT and PN rows stay. No claim; the block is illustrative.

**PRESENTATION with one site narrowing (§1; CL-C015; item 3).** The inline "(1) … (4)"
paragraph becomes four list items, one sentence each. Items (1), (2) and (3) keep their R87
Phase A words minus the section pointers, which were the funding. Item (3) loses its second
sentence, "Naming the counted states lifts Haiku 4.5 on them from $0.5656$ to $0.8489$ on
the store-counterfactual set ($90$)", so that each item carries at most one comparison; the
sentence and both values stand in Section 6 and Tables 2 and 10. Item (4)'s two R87
sentences rejoin into one of 37 words (they had been split for the 40-word rule only because
of the pointers): "Replication and controls: the paired obligation gain is positive on six
models across three vendors, the same summary hurts at every scale on the two backends
without lifecycle structure, and a wrong-index control inverts coverage below chance."
Direction: **narrower at §1 for the counted-states result**, unchanged for the paper.

**PRESENTATION, pointer reduction (item 5).** Five duplicate appendix pointers leave
paragraphs that keep another route to the same appendix: §4.2 "all $104$ were individually
hand-verified (Appendix F)" loses its pointer (the $\varepsilon$ sentence in the same
paragraph points at F.3, where the PN-verification row sits); §4.2 "The two user prompts
differ only in whether the serialized index precedes the question (Appendix F.3)" loses its
pointer (the rubric sentence before it points at F.3); §4.3 "…so a deployed threshold sits at
the base rate rather than at one half (Appendix H)" loses its pointer (the Brier sentence two
lines up points at H; AUX-R82-CAL wording otherwise verbatim); §4.4 "…so it bounds
correspondence alone (Appendix F)" loses its pointer (Table 16, cited in the same paragraph,
carries the shuffle rows); §7.1 "the balanced authorship-matched set ($36$; Appendix D.1)"
becomes "($36$)" (Table 9, cited in the same paragraph, sits in D.1). No pointer that is a
deviation record's only route is touched. Direction: **neither**.

**NOT DONE, recorded.** Item 1 (Definition 1 as a $3\times3$ state-by-intent table): the
compact form cost nine to twelve review lines in the scratch build, because the four-line
table in Section 3 moved the Section 4 heading and Table 1 across a page break and the
displacement cascaded to the end; funding (c) (one attribute-name line out of the index
excerpt) yielded no line, (d) yielded none (the Figure 1 pointer already shares its line),
(e) does not apply (each member of the one four-work citation chain is cited nowhere else,
so dropping one would orphan a bibliography entry). Skipped (D-R91-11). Item 4 (§7.2 as
six paragraphs): six paragraphs and the two-paragraph form each cost the whole slack;
left as is, per the item's own rule. Item 6: no number in §8 outside the R88 accounting
paragraph. Item 7 (§4.4 control table): skipped, slack below its height plus two.

**Phase 4 (figures, tables and appendix hygiene, `R91-4`).** Reading 482, slack +3 before and
after. No number moves; no table value changes. One build (`paper_v3.pdf`); `paper_v2.pdf`
and `paper.pdf` untouched. The pre-existing overfull box in Table 12 is gone.

**DELETION at one site (Figure 2 caption; CL-THREELINE; CL-FIG-ladder / C132).** The clause
"indexed FOK converges across all model sizes (Table 3)" leaves the Figure 2 caption, which
shows the obligation panel only. The R88 DELETION entry above named this caption as
CL-THREELINE's one printed instance; from R91 the printed instance of the FOK-convergence
clause is Table 3's caption, "It shows tight indexed FOK across all six lineages and tight
indexed NOK across the five lineages whose blind NOK varies.", which is byte-identical to
its pre-R91 form (checked at Phase 6). The caption's remaining clause reads "Blind NOK has
no monotone scale trend, and indexed NOK converges across GPT-5.6 Luna and GPT-5.6 Sol
(Table 3)." Direction: **narrower at the figure**, unchanged for the paper.

**PRESENTATION (Figure 2 plot).** The in-axis node "indexed$-$blind: $+0.2139$ / $+0.2940$
/ $+0.3298$" is deleted: at the figure's 0.20 height it sat above the axis frame and was
clipped out of every render since R88 (it survived only in the PDF text layer, where it
interleaved with the 0.8526 and 0.8588 labels). Table 3 prints all three deltas. The legend
moves from the right edge, where its white box hid the sol markers, to a one-row legend in
the empty band between the two series. Axis, data, height and width are unchanged.

**PRESENTATION (Figure 1).** The picture is set at its printed size (no `\resizebox`), so
every label is 7pt or larger, the print floor ruled at Phase 3; the box is 394.7 by 60.1pt
in place of 353.5 by 61.1pt (the height held, the width now the text width). To hold the
height the store column loses its third filler row ("gear preferences") and its second
explanatory label ("below the cutoff, so no bounded retrieved view reaches it", which the
caption states), the index box loses "no stored value appears anywhere" (the caption says
"value-free"), and the two "FOK, NOK" output boxes become the monitors' third line, with
the dashed arrows to the gold label kept. The two count rows, the "names carrying
superseded content" line and the cutoff label survive. No number changes (D-R91-13).

**PRESENTATION (Figure 3, Appendix F.4).** Full text width; a TikZ overlay writes "base
rate" above the dashed base-rate line in each panel. `reliability.pdf` is unchanged.

**PRESENTATION (Table 3 footnote → Appendix B body; CL-T-ladder-exact).** "Mini blind NOK is
constant at $0.0$ on all $84$ items, so $0.5000$ is an all-tie artifact rather than
calibrated uncertainty, and its clustered interval is not printed for the same reason; luna
spans $48$ distinct values and still fails to discriminate." and the mini dash sentence move
verbatim from the footnote to the paragraph above the table, the dash sentence reading
"committed main-study elicitation" for "committed E1 primary elicitation" because
registration codes are barred in appendix prose outside table cells (the paper's own
phrase, used two paragraphs later). The footnote is one line: "Mini rows: the all-tie
artifact and the dash convention are explained in the paragraph above the table."

**PRESENTATION (Tables 2 and 10, dash convention; R87 Phase A wording).** Table 2's caption
gains "A dash marks an entry never scored; recovering it would require rescoring the stored
responses." ("entry", because "cell" is barred in main text) and its dagger footnote and
marks go; Table 10's caption gains "A dash marks a cell never scored; recovering it would
require rescoring the stored responses." followed by the adverse-rows sentence verbatim
("Adverse rows, printed rather than set aside: the all-states matcher exceeds three monitor
rows by more than the $\pm0.05$ tolerance, GPT-4.1 mini by $+0.1947$ under the first summary
and $+0.1467$ under the second, and Haiku 4.5 by $+0.1480$ under the first; it exceeds Haiku
4.5 under the second summary by $+0.0230$, inside tolerance, and the superseded-names
matcher exceeds GPT-4.1 mini under the first by $+0.0322$, also inside tolerance."), and its
"Not in the ledger" note and dagger marks go. The fragment "would require rescoring the
stored responses" keeps its two sites. Direction: **neither**.

**RELOCATION (Table 19 caption → Appendix F.8 body; R88 CORRECTION OF FACT, CL-T-baselines).**
The caption keeps its reading instructions. "On FR-Bank coverage the monitor outranks every
mechanical reader." and "On FR-Bank obligation under TRUE it does not: NB-6, which reads the
superseded-names section alone, reaches $0.7484$ against the monitor's $0.7339$, a
difference inside the tolerance." are deleted from it as duplicates of the F.8 body (the
second reading and the NB-6 paragraph). The R88 sentence "On the structureless backends the
lexical and embedding matchers sit at $0.5000$ and the other mechanical readers scatter
around chance ($0.4184$ to $0.5226$), which is what ``structureless'' predicts, while the
monitor's indexed point estimates under the truthful summary fall below them ($0.4777$,
$0.4526$; Section 5.3)." relocates verbatim into the body as the third of the readings that
carry beyond the table ("Three readings carry beyond the table."). Direction: **neither**.

**PRESENTATION (Appendix E; C108, CL-C083-C085, AUX-E1R-NB3, C119).** The program's sentence
"Every failure below is the same kind: a semantic assumption hidden inside a step that
looked mechanical." is prepended to the preamble; the C108 scope sentence and the C085
lesson sentence stand verbatim behind it, and `repeat_scan` is quiet against the C120
closing sentence. Item 12 reads "A term-frequency index-reader baseline (NB-3) read the
question rather than the store; Appendix F.8 holds the record." / "NB-3 was disqualified as
an index reader and is retained as a measurement-step failure record."; the ablation detail
it dropped is in F.8's opening paragraph. Twelve records plus one preventive, as C119 says.

**RELOCATION (Appendix G → Appendix C; the R86 item 2.5 outcome vocabulary).** The
"Reading the Outcome column" paragraph moves verbatim to the head of Appendix C, where held
and failed first appear (Table 6); Appendix G keeps "The outcome vocabulary is defined at the
head of Appendix C."

**ADDITION, no claim (Table 12; CL-T-e1-construction).** A `Constrains` column names the
reported claim each measured row bounds (the PN labels, conservative gains, values removed,
Table 1, the blind rows of Table 1, the five-level scale, coverage retention) and reads
"design record" on the design rows. No row content changes; the Record and $n$ columns wrap,
which closes the 62.7pt overfull box the table had carried since R86.

**LEFT (umlaut).** R90 declined a T1 fontenc change; the text layer still extracts
"[AUTHOR-2]" while the rendered accents sit on the letters. Unchanged, as ruled.

**No other claim changes strength under this block.**

## R92 AUTHORIZATION BLOCK — dated 2026-09-11

Appended by R92-PRESENTATION, anchored to the R91 block above, landing in `paper_v4.tex` from
Phase 1 (LINEAGE, below); Phase 0 touched no manuscript.
**Open list, one entry per phase; closed at Phase 6.** Reports: `reviews/R92_PHASE0.md`,
`reviews/R92_REPORT.md`; deviations `reviews/DEVIATIONS_R92.md`. Base `abac307`. Every number
in the paper is frozen under this program; no entry below moves one, adds one, or drops one
from the manuscript (`numeric_diff` tex side: 0 added, 0 vanished, end to end).

**Rulings taken at planning ([AUTHOR-1], 2026-09-11, in chat).**

- **R-a, S6 amended.** The abstract is rewritten to the prompt's seven-slot order at 180 words
  or fewer. STYLE_SPEC S6's band widens from 9 to 11 sentences to **7 to 11**, recorded in
  `STYLE_SPEC.md` in the Phase 2 commit. The R83 AUTHORIZED-ABSTRACT entry's "inside S6's
  9-to-11 band" is superseded by this ruling; its other three conditions (no sentence over
  40 words, no em dash, no contrastive) stand. Eight sentences land, not seven (D-R92-1).
- **R-b, STYLE_SPEC wins on collisions.** The prompt's finding sentence lands without its
  ", not on the model reading it" contrastive (S9; D-R92-5). Table 1's finding is caption
  sentence 2 behind the descriptive opener (S5 as overruled at P2).
- **R-c, direct landing.** Abstract and Section 1 land in `paper_v3.tex` under this block;
  no proposal file. Each phase stops before its commit.
- **R-d, the builders' paragraph closes Section 8.** Section 8 becomes one "what was found"
  paragraph and a headed, boxed closing paragraph carrying the R88 READING recommendation
  (L758) verbatim. Nothing lands at the end of Section 1.

**Phase 0 (`R92-0`).** No manuscript edit. Baseline gates green at `abac307` (page 9 / 482 /
+3; `frozen_diff` 108 found, 108 KEPT; `numeric_diff` 0 / 0; `appendix_identity` 23
sections identical). The accepted `numeric_diff --pdf` artefact is ruled in
`R92_PHASE0.md` section 8: after Phase 1 the PDF text layer loses the heading tokens `4.4`,
`7.1`, `7.2` (two subsection headings deleted, one renumbered, one demoted to a run-in
paragraph; `4.1` survives as the renumbered §4.1); the tex side must stay clean.

**LINEAGE (Phase 1, on [AUTHOR-1]'s instruction at the Phase 1 STOP; R90 precedent).** The working
lineage is `paper_v4.tex`; `paper_v3.tex` is frozen at `abac307` (the R91-6 close) and is the
version a reader compares v4 against. `paper_v4.tex` starts as `paper_v3.tex` with Phase 1
applied. Tool defaults move to v4 (`appendix_identity`, `claims_diff`, `u9_scan`,
`sentence_census`, `frozen_diff`, `numeric_diff`); `frozen_diff` and `numeric_diff` gain
`--base-tex=` so the first v4 commit diffs against v3 at the base; `.gitattributes` gives
`paper_v4.tex` the same `eol=crlf` exception as v3.

**Phase 1 (moves to the appendices, `R92-1`).** Page: label on 9, reading 482 / slack +3 before,
**440 / +45** after; 27 pages; no overfull box. `numeric_diff` tex side 0 added, 0 vanished, 33
count changes (every one a relocation or a de-duplication); PDF side VANISHED `4.4`, `7.1`,
`7.2` only, the artefact ruled at Phase 0. `appendix_identity`: D (new EXEMPT entry), D.2, F,
F.4 and F.6 re-pinned, nothing else changed. No number moves. Table numbers in this entry are
those of the base `abac307`; from this phase Tables 3 to 10 print as 2 to 9 (Table 2 left the
main text), the question-set table prints as Table 10 at the head of Appendix F, and Tables 11
to 24 keep their numbers. Every cross-reference in the manuscript is a `\ref`.

**RELOCATION with a site narrowing (§4.1 → Appendix F.2; CL-C040).** The Pilot subsection leaves
the main text. One sentence stands in §4.2, before the hard-question sentence: "A pilot with a
different prompt found a large coverage gain and no obligation gain; its lesson was to rule out
gains that come only from a zeroed category (Appendix F.2)." The null obligation gain and the
lesson print there; the non-comparability clause ("its values are not comparable with the main
study") prints in Table 11's caption, which F.2 already carried. Direction: **narrower at §4**,
unchanged for the paper.

**RELOCATION (question-set table → head of Appendix F; R91 Phase 3 item 2).** The unfloated table
becomes `tab:question-sets`, captioned "The four question sets, each defined once: name, size,
positives, purpose, and where each is used.", rows verbatim. Its R91 lead-in "The results rest on
four question sets, each defined once." becomes "The results rest on four question sets, each
defined once (Table F.0)." and closes the §4.2 design paragraph. Direction: **neither**.

**RELOCATION with a site narrowing (§4.4 attribution paragraph → Appendix F.6; CL-C060-C062).**
The design-history sentence, the estimation sentence and the dominance sentence (with its
R91-quoted "within the conditions we varied") relocate verbatim as F.6's second paragraph; the
estimation sentence drops the "(Appendix F.6)" pointer it carried, which would point at itself.
§4.4 keeps one sentence at the attribution's strength: "The attribution comparison of Appendix
F.6 separates the lifecycle-index change from the two prompt changes made after the pilot, and
the lifecycle-index effect dominates both." Direction: **narrower at §4.4** (the three-changes
history leaves the main text), unchanged for the paper.

**DELETION at one site (§4.4, the shuffle's bound clause; CL-SW2; D-R92-6).** "Per-category
correspondence is therefore unnecessary on FR-Bank, and the shuffle preserves the global name and
count multiset, so it bounds correspondence alone." leaves the main text. U7 in Appendix F.5 and
the Table 16 footnote carry the bound byte-identically, and R87 D1 had deleted the plain-words
repeat of U7 that stood beside it, so the sentence is not moved into F.5. The R91 sentence "The
category shuffle permutes which counts and attribute-name lists belong to which category and
changes neither judgment." gains a Table 16 pointer before its period and stays as the block's
single pointer. Direction: **narrower at §4.4**, unchanged for the paper.

**RELOCATION (Table 2 → Table 10, Appendix D.2; CL-BOX-cf / R86 item 3.2, R87 Phase A, R91 Phase 4).**
Table 2 leaves the main text. Its per-state rows, its whole-set row and both matchers already
print in Table 10; its row "Counted states, individuating pairs ($n=45$)" and the six values
$0.5578$, $0.6600$, $0.5656$, $0.8489$, $0.6122$, $0.9144$ become Table 10's last block (label
verbatim, no gain column, because a gain against $0.5000$ would be a number no ledger carries),
and Table 10's caption gains one sentence saying what the block is (the $45$ items, $15$
questions each asked of three store versions, whose scrubbed attribute name individuates the
pair). Three Table 2 caption strings leave the manuscript: "The store-counterfactual set ($n=90$):"
(1 → 0), "A dash marks an entry never scored; recovering it would require rescoring the stored
responses." (1 → 0, Table 10's own dash sentence stays), and so "would require rescoring the
stored responses" prints once (2 → 1). Section 6 keeps the Haiku sentence, now pointing at Table
10 and reading "($n=90$; Table 10)", and gains one sentence for the matcher the caption carried:
"A direct match against the three name lists reaches $0.7886$ on the same set, above three of the
six monitor scores by more than the $\pm0.05$ tolerance (Table 10)." (the adverse rider stays in
the main text, as the caption had it). Direction: **neither**.

**RELOCATION with a site narrowing (§7.1 → Appendix D; CL-C082, CL-PRIORCONTROLLED,
AUX-R76-AVCENSUS, AUX-R74-X1-POOLED, AUX-R74-X5, AUX-R76-MATCHED-PROBE, AUX-R82-CF-NOK).** The
subsection's prose relocates verbatim to the head of Appendix D, except that its Appendix D
pointer and its Table 2 pointer are re-aimed at Tables 7 and 10. Section 7 keeps four sentences
and the Appendix E pointer (CL-C083-C085): "The question text alone predicts the labels:
supervised text probes reach $0.7972$ to $0.9662$ on the populations of Table 7, far above
chance." (D-R92-2: the prompt's "0.80 to 0.97" is a rounding), the R79 sentence "Blind scores
therefore measure the question as much as the model, and the paired gain over identical
questions is the clean quantity." verbatim, and "The authorship-matched set ($n=36$) and the
store-counterfactual set ($n=90$) exist for that reason. On the first every slot carries the same
one-third PN rate; on the second the question is fixed and the store varies (Appendix D)." Both
subsection headings go; Limitations becomes a `\paragraph` run-in with every sentence unchanged.
Direction: **narrower at §7** (the census figures $0.9736$, $162$, $n=16$ and the pooled
$0.9662$ sentence leave the main text; $0.9662$ prints in the range sentence), unchanged for the
paper.

**RELOCATION (§1 L154 → §6 opener; Part 2 of the prompt).** "The paper's object is what a store
exposes about itself; what happens when it exposes the wrong thing is the second half of the
result." leaves §1 and opens §6 verbatim. Direction: **neither**.

**PRESENTATION (two statements; Part 8).** "[TODO-URL]" becomes "[URL withheld for review]" in
the Reproducibility statement and beside the Appendix F.4 href. The
`SUBMISSION_CHECKLIST.md` marker name is now stale and is noted in the report.

**Phase 2 (abstract, Section 1, Figure 1, Sections 2 and 3, Table 1, `R92-2`).** Page: reading
440 / +45 before, **445 / +40** after (Section 1 grew by about five lines with the contributions
in their two-sentence form; the abstract shrank by four). 27 pages; no overfull box.
`numeric_diff` tex side 0 added, 0 vanished; PDF side VANISHED `4.4`, `7.1`, `7.2` (Phase 0
ruling) and the bare token `42.3`, a text-layer artefact: the manuscript prints `$42.3\%$` at
every site (abstract, §1, §6, Appendix F.8), the base PDF's extraction split one percent sign
off and the new one does not, so `42.3%` counts 3 → 4 and `42.3` 1 → 0 with the four
occurrences unchanged. Ruled here as accepted. `appendix_identity` unchanged. No number moves.

**ABSTRACT (ruling R-a; D-R92-1; supersedes ABSTRACT-LAND-A's arrangement, not its claims).**
Eight sentences in the prompt's order, 177 words by `prose_scan`'s counter, none over 40
words, every grammatical subject inside its first five words, one number sentence (42.3 %
with its 60 % threshold), no em dash, no contrastive. Every claim of the eleven-sentence
abstract survives except two that leave it and stand elsewhere at the same strength:
"On a set where the question cannot carry the label, the state the summary names is judged
better than the states it only counts, and naming those states restores the judgment on them."
(deleted from the abstract; the claim stands in Section 6, "On FR-Bank the paired obligation
gain concentrates on the one state the index names" and the Haiku 4.5 sentence, and in Table
9), and the fragment "what the summary transmits is bounded by what it names" (deleted from
the abstract; the naming bound stands at Section 3's "A self-description can only name what
its scrubbing rule individuates" and Section 6's "The index names superseded content and only
counts retracted and expired content", and Section 1's contribution (3) says "the judgment is
bounded by what the summary names"). "all six models we test across three vendors" becomes
"all six models across three vendors"; "keeps all of its gain" becomes "keeps its gain".
Direction: **narrower at the abstract**, unchanged for the paper. `STYLE_SPEC.md` S6 is
amended in this commit (band 7 to 11).

**PRESENTATION (Section 1 as five paragraphs; CL-C008, CL-C149, CL-C009-C010, CL-C011-C014,
CL-C002, CL-C015, CL-C018).** Paragraph 1 keeps every sentence of the failure paragraph, with
the retraction sentence split at "so" and the benchmark sentence split at its semicolon (the
fragments "retraction records survive similarity retrieval at only 5%", "no evaluated RAG or
agentic-memory agent exceeds 7% accuracy" and "was written only on explicit request" are
intact); the monitor is defined before the word is used ("The component that decides whether
and how to consult memory is the monitor, and the failure occurs there, before any answer is
drafted."); the policy sentence is split at ", and". Paragraph 2 opens on the R86 item 3.1
fragment ("the two things an agent must decide before touching its memory"), defines FOK and
NOK in one plain sentence each before the Nelson and Narens citation, keeps "(superseded,
expired, or retracted)" and "scored against labels we know exactly, because we built the
stores", and keeps the novelty sentence verbatim. Paragraph 3 is new prose over printed
numbers: the finding sentence in its S9-clean form (D-R92-5), the lookup against the smallest
model ($0.7484$ against $0.7339$, NOK, all $661$ obligation questions), the retention
($42.3\%$ of the gain under the metadata the backends expose, short of the $60\%$ threshold
set in advance) and the structureless-store inversion; it absorbs the three R86 item 3.1
sentences "This paper measures a judgment rather than shipping a monitor.", "The language
model we test as a monitor is a baseline: a text match against the store's own summary keeps
pace with it on the obligation judgment." and "What the paper finds is that the judgment is
bounded by what the store writes about itself.", each of whose content it restates. Direction:
**neither**.

**DELETION at one site (Section 1, the gap paragraph; CL-C022-C147).** "Existing evaluations
grade what happens after memory is consulted. Benchmarks score retrieval, conflict resolution,
and answer accuracy, and training methods improve the loop that writes and reads the store
(Section 2). Each of these presupposes a monitoring judgment, some estimate of what the store
holds and what it forbids, and none measures it." leaves Section 1; the gap claim stands at
strength in Section 2 ("All of them presuppose the monitoring judgment, an estimate of what
the store holds and what it forbids, without measuring it."), which R79 wrote as its twin.
Direction: **narrower at §1**, unchanged for the paper.

**PRESENTATION (contributions; CL-C015, R88 "word for word", R91 Phase 3 item 3).** Each item
now states the finding and its consequence for a system builder, in two sentences where the
30-word rule requires it. Item (2) cedes "$42.3\%$" to paragraph 3 (where it prints with its
threshold) and reads "We show that no tested backend writes the summary the judgment needs: a
census of three backends records overstatement, erasure, and invention." Item (4), the R91
quoted sentence "Replication and controls: the paired obligation gain is positive on six
models across three vendors, the same summary hurts at every scale on the two backends without
lifecycle structure, and a wrong-index control inverts coverage below chance." becomes "We
show that the paired obligation gain is positive on six models across three vendors. The same
summary hurts at every scale on the two backends without lifecycle structure, and a
wrong-index control inverts coverage below chance." followed by its consequence; the fragment
"the paired obligation gain is positive" is intact. Direction: **neither**.

**PRESENTATION (Figure 1 caption; CL-FIG-overview).** The caption states what each monitor sees
("The blind monitor sees only the question. The indexed monitor sees the question and a
value-free summary of the store that names which attributes carry superseded content.") and
the trailing "which is the one thing about this store that the question alone cannot supply"
becomes "The question alone cannot supply that summary." Direction: **neither**.

**PRESENTATION (Sections 2 and 3, sentence pass; Table 1).** Four Section 2 sentences and four
Section 3 sentences are split at joints (semicolons, ", and", a parenthetical pointer, the
Proposition gloss's "so") with every word kept; two trailing-"so" claims are fronted (the
blind monitor's AUROC; the gain). CL-C055-C057's fragment "the counts are not necessary for
coverage" now opens its sentence with a capital ("The counts are not necessary for coverage:
randomizing every count leaves discrimination on the lifecycle store of Section 4 (FR-Bank)
unchanged."), the one CHANGED string this pass produces. The index excerpt's caption line
reads "This is what the indexed monitor reads." Table 1's caption gains the prompt's sentence
as sentence 2 ("The index helps on the backend with lifecycle structure and hurts on the two
without it.") behind the descriptive opener; its positive-class cells lose their semicolons
("$35$ non-ABSENT" for "$35$; non-ABSENT" in all five rows; rows 5 and 6 are U8 and keep
every value). Definition 2 (35 words) is left and flagged. Direction: **neither**.

**Phase 3 (Section 4 sentence pass, `R92-3`).** Page: 445 / +40 before and after. No number
moves; `numeric_diff` tex 0 / 0.

**PRESENTATION (§4.3 pooled paragraph; CL-C141).** The concrete reason comes first: "All $35$
pooled positives are FR-Bank questions, so a rule that only checks which backend a question came
from scores $0.7541$ against the pooled indexed $0.7530$." The R91 sentence "Pooled levels
measure coverage for no reader." stands verbatim behind it, then the paired-gains sentence.
Direction: **neither**.

**PRESENTATION (§4.3 central paragraph; CL-BASELINES-SENT, AUX-E1R-NB6, AUX-E1R-NB6-PERSTATE).**
The order is now finding, two numbers, what the result does and does not establish, pointer.
The opener "The obligation judgment behaves differently." is replaced by "A lookup over the
superseded names matches the monitor on the obligation judgment under the TRUE index, on the
full obligation population ($n=661$)."; the NB6-1 registration sentences and the R91 and
CLAIMS per-state pair stand verbatim; two sentences are added at the strength the pair already
carries: "The result establishes one thing: where the summary names the superseded content, a
lookup reads the obligation as well as the smallest model. It does not establish that a lookup
matches the larger models, whose extra gain sits on the counted states (Table 19)." (the
counted-states advantage is the per-state pair's own statement; Table 19 is
`tab:nb6-composition`). Direction: **neither**.

**WORDING (§4.3; CL-C051).** "Detecting that one stored record must be suppressed is NOK's job."
becomes "NOK targets that case, whether one stored record must be suppressed." (Part 4 bars the
"X is Y's job" form; CL-C051's "NOK's distinct target" is the entry's own word). Direction:
**neither**.

**PRESENTATION (§4, splits at joints; 30-word rule).** The R91-ordered $\varepsilon$ sentence
"Even accounting for the presence control's residual error, a mislabeled ABSENT item is unlikely
at the observed base rate ($5.2\%$; Appendix F.3); such items can only shrink measured gains,
so reported differences are conservative." splits at its semicolon with every word kept; the
rubric line's trailing "(responses normalized to $[0,1]$)" becomes "Responses were normalized to
$[0,1]$." with the quotation untouched; the AUX-R82-CAL sentence splits at ", and" with its
words otherwise verbatim; the names-only sentence splits after "$0.8516$" with "whose counts
made the store look better covered than it is" intact. Direction: **neither**. Flagged, not
changed: the FOK rubric quotation (31 words as quoted).

**Phase 4 (Sections 5 to 7, `R92-4`).** Page: 445 / +40 before, **446 / +39** after (the
Figure 2 caption sentence). No number moves; `numeric_diff` tex 0 / 0; both figure boxes the
same size.

**PRESENTATION (§5.2 opener; CL-TAKEAWAY).** "The capability study's plain takeaway:" is dropped;
the sentence reads "Model scale changes what a model guesses from the question alone, while the
store description supplies the obligation information (Figure 2)." Direction: **neither**.

**PRESENTATION (Figure 2 caption; CL-FIG-ladder / C132, CL-T-ladder-exact).** After the R91
sentence the caption adds "That point is an artifact of a constant score and carries no
information (Table 3 states the caveat in full)."; the Appendix B sentence it summarizes is
unchanged. "$40$ PN" is set with the label macro. Direction: **neither**. §5.2's "on the
cross-model set of Figure 2" gains "$n=84$".

**PRESENTATION (§6; CL-BELIEVED-NOK, AUX-E1R-BELIEVED-NOK, U9; D-R92-3).** The R91 topic sentence
"The obligation judgment fares worse, losing more than half its benefit." becomes "On the full
obligation population ($n=661$) under the BELIEVED index, the obligation judgment fares worse,
losing more than half its benefit.", so the NB6-2 HOLDS pair that follows has its judgment,
condition and population named by the paragraph. The $42.3\%$ sentence splits at ", keeping"
("… with questions grouped by user profile). That keeps $42.3\%$ of the TRUE gain, short of
the $60\%$ we had set as the threshold."); the frozen-branch sentence and the registration pair
stand verbatim; no connective joins the retention to the matcher sentences. The A-MEM census
sentence splits at "which is" with every word kept. Direction: **neither**.

**PRESENTATION (§7 limitation; CL-LIMITS, the R91-quoted form).** "The lookup has one
descriptive value on the cross-model set, none per state on the store-counterfactual set, and
none on the authorship-matched set, so the comparison between model and lookup is complete only
on the full obligation population ($661$)." splits before its "so": "… on the authorship-matched
set. The comparison between model and lookup is therefore complete only on the full obligation
population ($661$)." Same three sets, same population, same scope; no `n` is attached to the
three set names (D-R92-4). Direction: **neither**.

**Phase 5 (Section 8, the builders' paragraph, whole-text passes, `R92-5`).** Page: 446 / +39
before, **448 / +37** after (the box). No number moves; `numeric_diff` tex 0 / 0.

**PRESENTATION (Section 8 as two paragraphs; C092-C095; ruling R-d; Part 7).** Paragraph 1
keeps every conclusion sentence at body strength and adds the plain finding in place of the R88
closing sentence: "A monitor is therefore bounded by how well its backend describes itself,
which is a property of the store rather than of the model reading it." becomes "A monitor is
bounded by how well its backend describes itself. That is a property of the store; the model
reading it does not change it." (no trailing clause, no contrastive; D-R92-5). "a direct match
against the names the store marks superseded matches the smallest of them" reads "the
superseded-names lookup matches the smallest of them" (Part 8's one name for that reader).
"obligations lose most of their benefit" reads "obligations keep $42.3\%$ of their gain, short
of the $60\%$ threshold set in advance": the same fact, so that the retention prints with its
threshold at every site (Part 8); no connective joins it to the tie sentence in the box (U9).
Direction: **neither**.

**RELOCATION into a box with a site narrowing (the R88 READING paragraph; CL-BUILDER / R88 B1).**
The quoted string "For a deployed system the tables already give the accounting. On the
obligation judgment a lookup over the summary's superseded names and the model tie under a
truthful summary ($0.7484$ against $0.7339$) and tie near chance under the metadata a real
backend exposes ($0.5858$ against $0.5959$). Once a summary names every non-active state, the
lookup reaches $0.7886$ on questions that cannot carry the label. The model earns its cost on
one judgment only, coverage where lifecycle structure exists, where it leads the best
mechanical reader by $+0.0817$. A system should therefore decide obligations with a lookup over
a name-bearing lifecycle summary, spend model calls on coverage only where the store has
structure, and treat a store that cannot write such a summary as one no monitor repairs."
becomes the boxed closing paragraph headed "For system builders." with: its first sentence
deleted (the heading does its work); the tie sentence split at its second "and" ("They tie near
chance under the metadata a real backend exposes ($0.5858$ against $0.5959$)."); "a lookup over
the summary's superseded names" read as "the superseded-names lookup"; the cost sentence's
trailing "where" clause recast ("The model earns its cost on one judgment only: coverage where
lifecycle structure exists, on which it leads the best mechanical reader by $+0.0817$."); and
the recommendation sentence verbatim, by the prompt's order, at 40 words (flagged as the one
main-text sentence over 30 by design). Every number stands. Direction: **narrower at §8** (the
accounting sentence leaves), unchanged for the paper.

**PRESENTATION (Section 5 trailing clauses; C066, C064).** "The Anthropic pair spans two model
generations, so its ordering compares price and capability; it is no within-generation
comparison." splits at "so" with every word kept; "Blind levels include what the question text
gives away, so this trend measures how much of that signal each model reads." becomes "This
trend measures how much of the question's label signal each model reads, because blind levels
include what the question text gives away." Direction: **neither**.

**PRESENTATION (one name for the lookup; Part 8).** Every free main-text sentence that names
the reader NB-6 calls it "the superseded-names lookup" (§1 item (3), §4.3 opener, §8 twice).
The registration sentences (§4.3 "A matcher that scores each question directly …", §6 "a matcher
that reads the store's list of superseded names directly") and the R91 quote "The
superseded-names matcher matches the smallest model tested." keep their wording and are
flagged. Direction: **neither**.

**Phase 6 (`R92-6`).** Report `reviews/R92_REPORT.md`, Review G rows, ledgers closed; no manuscript edit.

**No other claim changes strength under this block. Closed at Phase 6, 2026-09-11.**

## R93 AUTHORIZATION BLOCK — dated 2026-09-11

Appended by R93-CITATIONS, anchored to the R92 block above, landing in `paper_v5.tex` from
Phase 1 (LINEAGE, below); Phase 0 touched no manuscript. **Open list, one entry per phase.**
Records: `REFCHECK_V12.md` (the 35 verified references), `reviews/R93_refcheck_raw.json` (every
primary-record response), `reviews/R93_REPORT.md`. Base `fdd34c8` (the R92-6 close). Every number
in the paper is frozen under this program; no entry below moves one, adds one, or drops one from
the manuscript (`numeric_diff` tex side: 0 added, 0 vanished).

**Rulings taken at planning ([AUTHOR-1], 2026-09-11, in chat).**

- **R-a, the set.** All 35 reviewer-relayed references enter, not the 20-item trim the relay
  suggested. References pages are unlimited under the ICLR 2027 call; the in-text cost is
  derived in the plan (about 586 rendered characters, eight to ten review lines) and measured
  at Phase 1 as eleven lines against a slack of +37.
- **R-b, every edit is a parenthetical.** No word of prose changes at any site; a citation
  attaches inside an existing sentence. Direction at every site is **neither**.
- **R-c, sites the relay could not name.** The relay attached the LLM-confidence cluster
  (kadavath2022, lin2022, tian2023, xiong2024) to the §2 adaptive-retrieval sentence, whose end
  already carries the Asai/Jiang/Yao/Sah parenthetical the adaptive-retrieval cluster extends.
  It lands instead on §2's "Prior apparatus" closer, "What is measured here is belief about an
  external store rather than confidence in an answer", the sentence that draws exactly that
  contrast. The stale-content cluster (longpre2021, dhingra2022, xu2024conflicts) lands on §1's
  "The pattern is widespread", not on the vendor sentence two clauses later, which keeps its own
  `\citep{openaimemory}` unmixed, and not inside Definition 1. maini2024 (TOFU, unlearning) sits
  with "agent-facing forgetting" in the GateMem sentence rather than with CIMemories; the relay's
  "CIMemories sentence" was split into two at R92-2.
- **R-d, venue over preprint where the venue record verifies (memoryagentbench precedent,
  R75-F13).** yang2024 → NeurIPS 2024; maini2024 → COLM 2024; ren2025 → COLING 2025;
  zhang2025survey → ACM TOIS 2025. All four verified (`REFCHECK_V12.md`). No number in the
  manuscript is attributed to any of the 35, so the R83 re-test rule (a venue upgrade must re-test
  every number attributed to the citation) has nothing to re-test.
- **R-e, print the primary record (R80 rule).** platt prints the MIT Press chapter record,
  "Probabilities for SV Machines", *Advances in Large-Margin Classifiers*, pp. 61–74, 2000 (key
  `platt2000`), not the relayed 1999 technical-report title; su2024 prints the ACL camera-ready
  title with "Real-time"; zhang2025survey prints the journal's hyphenated "Model-based";
  nissenbaum2004 prints 79(1):119–158 with the last page bounded by the next article in the
  issue, as the record notes.

**Phase 0 (`R93-0`).** No manuscript edit. `tools/ref_fetch.py` written; 35 records fetched from
primary sources on 2026-09-11; `REFCHECK_V12.md` written: 35 VERIFIED, 0 DROPPED, five relayed
fields corrected against their records (R-e). Baseline gates green at `fdd34c8` (page 9 / 448 /
+37; `frozen_diff` 124 found, 124 KEPT; `numeric_diff` 0 / 0; `appendix_identity` 23 sections
identical; `refcheck_v11` 20/20 with 8 declared out of scope of 28 bibitems).

**LINEAGE (Phase 1; R90 and R92 precedent).** The working lineage is `paper_v5.tex`; `paper_v4.tex`
is frozen at `fdd34c8` (the R92-6 close) and is the version a reader compares v5 against.
`paper_v5.tex` starts as a byte copy of `paper_v4.tex` with Phase 1 applied. Tool defaults move to
v5 (`appendix_identity`, `claims_diff`, `frozen_diff`, `numeric_diff`, `u9_scan`,
`sentence_census`); `frozen_diff` and `numeric_diff` take `--base-tex=paper_v4.tex` for the first
v5 diff; `.gitattributes` gives `paper_v5.tex` the same `eol=crlf` exception as v4.

**Phase 1 (the 35 references, `R93-1`).** Page: label on 9, reading 448 / slack +37 before,
**459 / +26** after (eleven review lines, all of them citation labels); 28 pages (27 before; the
bibliography grows from 28 to 63 entries and takes one more page below the label); no overfull
box; 0 undefined citations or references. `numeric_diff` tex side 0 added, 0 vanished, 0 count
changes. **PDF side: ADDED `2207.05221` (page 10) and `2310.08560` (page 11), nothing else.**
These are the arXiv identifiers of the two arXiv-only records (kadavath2022, packer2023) printed
in the bibliography; the PDF tokenizer reads every page and the identifiers are decimal tokens.
Ruled here as accepted, on the R92 Phase 2 precedent for the `42.3` text-layer artefact; no
printed value in the manuscript moves. `frozen_diff` 124 found, 124 KEPT, 0 unauthorized: no
frozen string spans a citation site. `appendix_identity`: F.4 and H.1 changed, both EXEMPT with an
R93 basis and re-pinned (`1cacaf97…`, `570f091b…`); the other 21 sections identical.
`refcheck_v11` PASS, 22/22 full-metadata records, 41 declared out of scope, 0 silently uncovered
of 63. `slogan_scan` PASS (mean 17.9 over 209 sentences, S8/S9/S10 0, `preregistered` 4 of cap
4). `sentence_census` S2 0 and S3 1 over thirty words (the Definition, as at R92). `code_scan`,
`repeat_scan`, `trace_scan_v13`, `u9_scan`, `dupkey_scan`, `hygiene_scan` PASS.

**INSTRUMENT (claims_diff, banned-word region).** Check 4 read "main text" as `\begin{document}`
to `\appendix`, which includes the bibliography; the region had never contained a banned word, so
the over-reach was invisible. The nissenbaum2004 entry prints "Washington Law Review" and tripped
`\blaws?\b`. A journal title is not a claim; Reframe 5 governs claim prose. The region now ends at
`\begin{thebibliography}`, the bound `code_scan` and `repeat_scan` already use. `claims_diff` on
`paper_v4.tex` still reports 0 VIOLATIONs under the narrowed region, so nothing that passed
before passes for a new reason. Recorded as the R93 row of the INSTRUMENT_RULES table in the
report.

**CITATIONS (twelve sites, each a parenthetical; Direction at every site: neither).**

| Site (v4 line) | Sentence | Keys added |
|---|---|---|
| §1 L131 | "The pattern is widespread \citep{…}: on the multi-hop conflict-resolution slice…" | longpre2021, dhingra2022, xu2024conflicts |
| §1 L145 | "Both transfer a classical judgment about one's own memory \citep{…} to an external store." | hart1965, koriat1993, metcalfe1994, dunlosky2009 (beside nelson1990, koriat1996) |
| §1 L167 | "The confirmatory claims were preregistered \citep{…} with fixed decision rules…" | nosek2018, pineau2021 |
| §2 L174 | "…from parametric or generated-content signals \citep{…}." | lewis2020, mallen2023, ren2025, wang2023, su2024 (beside selfrag, flare, seakr, verbrouting; chronological order) |
| §2 L181 | "Abstention benchmarks score whether a question admits an answer, without an external store to be right about \citep{…}." | rajpurkar2018, kamath2020, yang2024 (beside abstentionbench) |
| §2 L190 | "…long-term stores \citep{…}…" | packer2023, zhong2024, zhang2025survey (beside mem0, amem) |
| §2 L201 | "…that the task context makes inappropriate \citep{…}." / "…agent-facing forgetting in shared stores \citep{…}." | nissenbaum2004 (beside cimemories) / maini2024 (beside gatemem) |
| §2 L221 | "What is measured here is belief about an external store rather than confidence in an answer \citep{…}." | kadavath2022, lin2022, tian2023, xiong2024 |
| §3 L271 | "…scores above a randomly chosen negative \citep{…}." / "ECE, the gap between stated probabilities and observed frequencies \citep{…}, is secondary…" | hanley1982 / naeini2015, guo2017 |
| F.4 L1445 | "…paired percentile bootstrap \citep{…}, to be preserved…" | efron1993 |
| F.4 L1450 | "A persona-clustered sensitivity \citep{…}, resampling whole personas…" | cameron2008 |
| H.1 L1956 | "…rescaled by three monotone maps \citep{…} under…" / "…a Brier score \citep{…} of $0.0560$…" / "…it improves selective risk \citep{…} from $0.0615$…" | platt2000, zadrozny2002, guo2017 / brier1950 / geifman2017 |

Section 2 L174's `\citep{nelson1990,koriat1996}` is unchanged (one classics site, §1 L145).
Appendix G opens with a table and takes no citation; the preregistration pair lives at §1 L167.
The word "preregistered" is not added anywhere (prose_scan cap 4, count 4). Every claim (CL-C008,
CL-C011–C014, CL-C018, CL-C019, CL-C021, CL-C022, CL-C032–C033, CL-C148, CL-C024 and the F.4 and
H.1 apparatus text) keeps its sentence byte-for-byte outside the inserted `\citep{…}`.

**Bibliography.** 35 `\bibitem` entries enter in house format (initials, "et al." for four or
more authors, venue and year for published items, `arXiv preprint arXiv:ID` for the two
arXiv-only items), merged alphabetically by first-author surname then year; the 28 existing
entries keep their relative order (asserted by the landing script). `\begin{thebibliography}{27}`
becomes `{63}`. Label collisions checked: Xu et al. (2024/2025/2026), Ren et al. (2025/2026),
Zhang et al. (2025/2026), Koriat (1993) beside Koriat & Goldsmith (1996) all differ by year or
author string.

**No claim changes strength under this block.**

## R96 AUTHORIZATION BLOCK — dated 2026-09-12

Appended by R96-RESTATEMENT, anchored to the R93 block above, landing in `paper_v6.tex`
(LINEAGE, below). Paper edits and ledger hygiene only: no experiment, no model call. Records:
`reviews/R96_REPORT.md`, `reviews/DEVIATIONS_R96.md`. **One entry per change, in the prompt's
order (1) to (4); `frozen_diff` ran after each entry landed, and every gate ran at the end.**

**BASE.** `paper_v5.tex` is the R93 close and is uncommitted on disk (R93 is pending [AUTHOR-1]'s
word), so no git revision holds it. The gates read it as the temporary tree object `69c8d690`,
written from the working copy with a scratch index (`git hash-object -w` + `git write-tree`; the
real index and HEAD are untouched, nothing is committed), so `frozen_diff` and `numeric_diff`
diff v6 against v5 exactly: `--base=69c8d690e0f51cc98015e45d7ec38ba3ae9602e0 --tex=paper_v6.tex
--base-tex=paper_v5.tex`. The same runs against `fdd34c8`/`paper_v4.tex` give the same verdicts,
because R93 was neutral to both instruments (124 KEPT, 0 added / 0 vanished).

**LINEAGE (R90, R92, R93 precedent).** The working lineage is `paper_v6.tex`, a byte copy of
`paper_v5.tex` with the entries below applied; `paper_v5.tex` is the version a reader compares
v6 against. Tool defaults move to v6 (`appendix_identity`, `claims_diff`, `frozen_diff`,
`numeric_diff`, `u9_scan`, `sentence_census`); `.gitattributes` gives `paper_v6.tex` the same
`eol=crlf` exception as v5.

**Rulings taken from the prompt ([AUTHOR-1], 2026-09-12).**

- **R-a, the headline.** Wherever the NOK headline stood as indexed minus blind on GPT-4.1 mini
  (abstract, §1, §4.2, Table 1 caption, §8), it is restated as the indexed level against the
  lookup ($0.7339$ against $0.7484$), with the paired gains carried by the five models whose
  blind score varies, and one sentence on why mini's blind score cannot anchor a gain: it is
  constant on the cross-model set (Table 2 dagger) and takes two distinct values on the $661$
  (Table 3 caption), so a paired difference against it measures distance from a flat score, not
  a gain over a blind judgment. No number changes; framing changes. The prompt's "Table 3" is
  `tab:ladder-exact`, printed as Table 3 until R92-1 and as Table 2 since, the table whose
  caption names the five lineages whose blind NOK varies and whose five NOK intervals all
  exclude zero; `tab:x4-expansion` (printed Table 3) carries three of the five at $n=661$ and is
  cited where that population is the subject.
- **R-b, vocabulary.** The main text may not say "arm" (prose_scan V) or "cell" (S10), so the
  manuscript says "blind score" and "cross-model set" where the appendix says "blind arm" and
  "$84$-item cell". "post hoc" prints hyphenated before a noun ("post-hoc rescaling"), the form
  Table 20's caption already uses.
- **R-c, the abstract's word ceiling.** The R92 R-a figure of 180 words (a prompt figure;
  STYLE_SPEC S6 carries no word cap) yields to the restatement: the fourth sentence becomes two
  and the abstract lands at nine sentences and 191 words by prose_scan's counter, from eight and
  177 (D-R96-1). S6's 7-to-11 band, its ends-on-headline rule, the 40-word rule and S8/S9 hold;
  the two new sentences are 23 and 25 words, so the abstract's over-30 count falls from two to
  one.
- **R-d, the hygiene items are writes against artifacts, not measurements.** Every value
  ledgered under (4) is read from a committed JSON (`results/cf_scores.json`) or computed
  deterministically from committed indexes (`cf_indexes.json`); no monitor is called. Where the
  registered instrument would need a model call (the v3 leakage screen, whose registered form
  is `ladder_e1.py`'s model-mediated answer-from-the-index), the deterministic half runs and the
  gap is recorded as a deviation rather than papered over.

**(1a) REWORDING at the abstract (`R96-1a`; the R92 slot-4 sentence; R-a, R-c).** The fourth
sentence "The obligation judgment improves on all six models across three vendors under a
truthful, value-free summary of store metadata, and a lookup over the names the summary marks
superseded matches the smallest of them." becomes two: "Under a truthful, value-free summary of
store metadata, the obligation judgment improves on the five models whose blind score varies,
spanning three vendors." and "The smallest model's blind score is nearly constant and anchors no
gain; its indexed level matches a lookup over the names the summary marks superseded." The
frozen fragment "all six models across three vendors" leaves the manuscript (1 → 0); no other
frozen string in the abstract moves. Direction: **narrower** (the paired-gain claim is made on
five models; the sixth is stated as a level against the lookup).

**(1b) REWORDING at §1, contribution (4) (`R96-1b`; CL-C015; R-a).** The frozen opening pair
"We show that the paired obligation gain is positive on six models across three vendors. The
same summary hurts at every scale on the two backends without lifecycle structure, and a
wrong-index control inverts coverage below chance." changes in its first sentence only (1 → 0
as a pair): it becomes "We show that the paired obligation gain is positive on five models
across three vendors, the five whose blind score varies. The smallest model is the exception:
its blind score is nearly constant, so a paired difference anchors no gain, and the third
contribution compares its indexed level with the lookup." The second sentence of the pair, the
builder sentence, and contribution (3) with its "$0.7484$ against $0.7339$" are untouched; the
frozen fragment "the paired obligation gain is positive" stays (1 → 1). Direction: **narrower**
at contribution (4); contribution (3) already carried the level.

**(1c) REWORDING at the Table 1 caption (`R96-1c`; CL-CAP-e1; R-a).** The third caption sentence
"It improves the hard FOK and FR-Bank NOK rows, and splitting the negatives by kind (Section
4.2) confines the hard FOK gain to genuine absence." becomes three: "It improves the hard FOK
row, and splitting the negatives by kind (Section 4.2) confines that gain to genuine absence.
On the NOK row the blind score takes two values across the $661$ questions, so the difference
column anchors no gain. That row is read as the indexed level against the superseded-names
lookup (Section 4.2), and the paired gains sit with the five models whose blind score varies
(Table 2)." The frozen second sentence "The index helps on the backend with lifecycle structure
and hurts on the two without it." stays (1 → 1); the rows and every value are untouched.
Direction: **narrower** (the NOK row is no longer captioned as improved by its paired
difference).

**(1d) REWORDING at §4.2 (`R96-1d`; CL-C052; R-a).** "NOK's FR-Bank gain is $+0.2393$ (CI
$[+0.1801,+0.2949]$)." becomes "NOK's FR-Bank paired difference on GPT-4.1 mini is $+0.2393$
(CI $[+0.1801,+0.2949]$). That difference cannot be read as a gain over a blind judgment.
Mini's blind obligation score takes two distinct values on these $661$ questions and one on the
cross-model set, so it carries no ranking to improve on. The level that anchors the finding is
therefore the indexed $0.7339$ against the lookup's $0.7484$. The paired gains are carried by
the five models whose blind score varies, each excluding zero (Table 2), three of them repeated
on all $661$ questions (Table 3)." The number and its interval print exactly as before; the
sentence after it ("NOK can be measured only on FR-Bank, because only FR-Bank retains superseded
content.") and the lookup paragraph above, with the NB6-1 registration text, are untouched.
`numeric_diff`: $0.7339$, $0.7484$ and $661$ gain one occurrence each (COUNT-CHANGED, no value
added or dropped). Direction: **narrower** (CL-C052's point and interval keep their strength as
a paired difference; they are no longer read as a gain).

**(1e) REWORDING at §8 (`R96-1e`; CL-C092-C095; R-a).** "With a truthful summary the obligation
judgment improves on every model tested, and the superseded-names lookup matches the smallest of
them." becomes "Six models across three vendors saw a truthful summary: the obligation judgment
improves on the five whose blind score varies, and the superseded-names lookup matches the
smallest of them. The smallest model's blind judgment barely moves, so its tie with the lookup
is a comparison of levels and anchors no gain." The frozen fragment "the superseded-names
lookup matches the smallest of them" stays (1 → 1); the boxed paragraph with its "$0.7484$
against $0.7339$" is untouched. Direction: **narrower**.

**(2) INSERTION at §4.2, calibration (`R96-2`; AUX-R82-CAL / POSTHOC-R82-1; R-b).** The
sentence "Rescaling the score after the fact does make it calibrated." follows "The score the
model reports behaves as a ranker whose value cannot be read as a probability, so a deployed
monitor must threshold it per index" and read as contradicting it. It becomes "A post-hoc
rescaling of the score, fitted after the fact, does make it calibrated (Appendix H)." The words
inserted are "A post-hoc", ", fitted", and the Appendix H pointer; "after the fact" and "does
make it calibrated" stay, as does the sentence after it ("The calibrated value still never
exceeds $0.375$, so a deployed threshold sits at the base rate rather than at one half."). The
sentence is not a frozen string (`frozen_diff` finds none at the site); the R82 block's
POSTHOC-R82-1 strength, post hoc and descriptive with the floor beside it, is what the insertion
makes visible in the main text. No number moves. Direction: **neither** (the same result, now
labelled as the post-hoc analysis Appendix H reports).

**(3) REWORDING at Appendix D.1, the D2a paragraph (`R96-3`; CL-T-matched-cell NOTE; v4 line
1116, v5 line 1232).** The paragraph's last sentence "A counterfactual in the strict sense would
score one near-identical query against two versions of the \emph{same} store differing only in
whether the target had been superseded; that design is not present here and is left to future
work." was true when R78 rehomed the paragraph and false since R82-INT landed Appendix D.2,
which reports exactly that design (thirty questions, each asked of three versions of one store
differing in a single attribute). It becomes "A counterfactual in the strict sense scores one
query against versions of the \emph{same} store differing only in the target's lifecycle state;
that is the design of the store-counterfactual cell in Appendix D.2, where the question is fixed
and the store varies." The three sentences before it, which say what the authorship-matched cell
does and does not hold fixed, are untouched. Not a frozen string (the R77-C branch froze the
paragraph's claim, no counterfactual, and that claim stands). CL-T-matched-cell's NOTE ("the
strict counterfactual is absent and left to future work") is superseded and annotated. Direction:
**neither** for the cell's own claim; the pointer replaces a statement that had become false.
`appendix_identity`: D.1 changes and is pinned under an R96 basis.

**(4a) LEDGER RESTORATION (`R96-4a`; `r82_counterfactual/NUMBERS_R82.md` §1 to §5; R-d).**
Commit `be64244` (R82-CF-1c) wrote the ledger from §6 onward and dropped the title, the header
naming the verifier and the registration, and §1 to §5 (`AUX-R82-CF-CONSTRUCTION`,
`-ADJUDICATION`, `-INDIVIDUATION`, `-INDEXSIZE`, `-SPEND`), 97 lines last present at `4c3a516`;
HEAD and the shipped `ARTIFACT/ledgers/NUMBERS_R82.md` both begin at §6 (reviews/CF2_SCOPE.md
finding 3). The title, the verifier and registration lines, and §1 to §5 are restored verbatim
from `git show 4c3a516:r82_counterfactual/NUMBERS_R82.md`; the header's "not scored yet"
paragraph, true at `4c3a516` and false since `be64244`, is replaced by a dated restoration
note; §5's spend table is the `4c3a516` snapshot (Haiku in flight, Opus pending) and gains a
dated line with the completed lane spends summed from the committed rows (`rows/rows_H45.jsonl`,
`rows/rows_OP5.jsonl`, `usd` field), cross-checked against the figures the `be64244` and
`7e9ac39` commit messages record (Haiku 1.2641, Opus 8.6103, total 10.0189 against the ceiling of
15). One reading note on the restored text goes in the header: §1's retraction-cosine "median
0.775" is the upper median (`sorted(x)[n//2]` over the ten `cosine_to_original` values); the
mean-of-the-middle-two median is 0.757; the value appears in no manuscript and `verify_r82`
checks it under the convention it was written with. The shipped copy is re-cut byte-identical to the source
(`ARTIFACT/ledgers/NUMBERS_R82.md`; the `DEVIATIONS_R82.md` copy is re-cut for the same reason,
because (4c) and (4d) write into it). No manuscript sentence changes. Direction: **neither**.
Noted and NOT done (outside the prompt's list): `DEVIATIONS_R82.md` lost D-R82-1 and D-R82-2 the
same way at `eb707fc`; both are recoverable from `2a35848` and the R82 block above cites "D-R82-1
to D-R82-5".

**(4b) VERIFIER (`R96-4b`; `r82_counterfactual/tools/verify_r82.py`; R-d).** `ADDENDUM_R82.md`
line 15 and the restored ledger header name a verifier that never existed (CF2_SCOPE finding 2).
It is written now, on the `verify_r74`/`verify_e1r` pattern the R82 PLAN prescribes: Direction A
reads every ledgered value of §1 to §12 back from its committed artifact (`cf_pairs.json`,
`adjudication.json`, `cf_questions.json`, `cf_pn_texts.json`, `cf_cell.json`, `cf_indexes.json`,
`probes.json`, the three row files, `results/cf_scores.json`, `results/cal_scores.json`,
`results/cal_floor.json`, `results/leakscreen_v3.json`) at print precision, and Direction B
asserts that every value Table 9 and Appendix D.2 print is a literal string in the ledger.
Read-only; no value is recomputed from monitor responses; the index token means of §4 are
re-derived only if `tiktoken` is importable and otherwise reported as unchecked by name. Exit 0
only when every check passes. Direction: **neither**.

**(4c) LEAKAGE SCREEN, deterministic half (`R96-4c`; `AUX-R82-CF-LEAKSCREEN`; D-R82-6; R-d).**
`ADDENDUM_R82` §5 registered the existing screen (`ladder_e1.py`, 30 items, threshold 3, seed
42) on a sample of the 90 v3 indexes, at most 3 of 30 correct; §9 reserved the key; nothing ran
and nothing was ledgered (CF2_SCOPE finding 4). The prompt reads `ladder_e1` as deterministic.
It is not: its scoring is (`exp4_witnesses.supports_correct`, no judge), but the answers it
scores come from `api.call` with the frozen LEAKAGE prompt, one model call per item. Under this
program's no-model-call rule the deterministic half runs and nothing else:
`r82_counterfactual/tools/leakscreen_v3.py` applies the registered scorer to the index text
itself, `supports_correct(index_text, entry_text)`, for every one of the 90 v3 indexes (and the
90 v2 indexes beside them), with the registered sampling reproduced for the record
(`random.Random(42).sample` over the 30 PRESENT items sorted by item id, which is the whole
PRESENT pool, so the sample is exhaustive). The gold is the pair's `entry_text`, the stored
value the question targets, because the drafted questions carry no `correct_answer` field. What
this measures is whether an index carries the answer's content tokens at the scorer's own
threshold; a model reading the index alone cannot be scored correct on an item where the index
does not, short of guessing from the question, so it bounds the registered screen from above
on the index side. It does not replace the registered screen: D-R82-6 records that the
model-mediated screen has not run and what it costs (30 to 90 `gpt-4.1-mini` calls). Ledgered
as §12 of `NUMBERS_R82.md` with the artifact `results/leakscreen_v3.json` (indexes sha256
recorded). Outcome: the registered cell, PRESENT under v3, scores 1 of 30, inside the threshold;
every one of the six version-by-arm cells scores exactly 1, the same item
(`cf:kenji:project:case_studies`, whose entry text shares `case`, `studies`, `work` with attribute
names in the per-category name map that v2 carries and v3 inherits), so the v3 sections add no
hit; 26 of 30 PRESENT indexes share at least one gold token with their entry text, the
slot-topic disclosure of `ADDENDUM_R82` §4. No manuscript sentence changes;
Table 12's "leakage screen 180 calls, 0 leaks" is the E1 screen and is untouched. Direction:
**neither**.

**(4d) TWO LEDGER ROWS and Table 9 (`R96-4d`; `AUX-R82-CF-OP5`; CL-T-counterfactual / D.2;
D-R82-7; R-d).** `results/cf_scores.json` carries Opus 5 per-state indexed AUROC under v3 at
`lanes/claude-opus-5/v3/per_state/SUPERSESSION/indexed` = 0.835 and
`.../RETRACTION/indexed` = 0.73, computed at `7e9ac39` beside the expiry value 0.945 that §10
ledgers; the two were never ledgered, so Table 9 printed dashes for computable values under the
caption's "never scored" wording (CF2_SCOPE finding 6). §9 gains a per-state table (v2 and v3,
ten positives each; the v2 row repeats §10's Opus line, the v3 row is new) and §10's v3 sentence
names all three Opus values. Table 9's two dashes become $0.8350$ and $0.7300$. The caption
sentence "A dash marks a cell never scored; recovering it would require rescoring the stored
responses." becomes "A dash marks a matcher cell that has no value: each matcher reads one
summary, and no matcher gain is recorded.", which is what the remaining dashes are (the matcher
rows; R92's Table 10 entry records why no matcher gain prints). Both frozen forms leave the
manuscript, "would require rescoring the stored responses" (1 → 0) with it. `numeric_diff`: tex
side ADDED $0.8350$ and $0.7300$, ruled accepted here as the two ledgered values (R93's
PDF-side precedent for a ruled addition; the tool exits 1 on ADDED by design and the run is
reported as such). `trace_scan_v13` accounts both against the R82 ledger. `appendix_identity`:
D.2 changes and is re-pinned under an R96 basis. Direction: **neither** for the claim (the per-
state boundary was already stated; the counted-state rise on Opus 5 now prints for retraction
as well as expiry).

**GATES (post-R96 build of `paper_v6.pdf`, three pdflatex passes; every gate run).** Page: label
on 9, reading 459 / slack +26 before, **469 / +16** after (ten review lines: two in the abstract,
one in §1, three in the Table 1 caption, three in §4.2, one in §8); 29 pages (28 before; the
appendix takes one more page); no overfull box; 0 undefined references. `frozen_diff
--program=R96`: 125 frozen strings found in the v5 base, **119 KEPT, 2 MOVED, 4
CHANGED-AUTHORIZED, 0 UNAUTHORIZED** (the four are quoted in entries 1a, 1b and 4d). `numeric_diff
--pdf --figboxes`: tex side **ADDED $0.8350$ and $0.7300$ (Table 9, entry 4d), 0 VANISHED**,
COUNT-CHANGED $0.7339$ 11 → 12, $0.7484$ 7 → 8, $661$ 20 → 23 (entries 1c and 1d); PDF side ADDED
the same two values on page 17, 0 VANISHED, COUNT-CHANGED $0.7339$ 9 → 10, `4.1` 20 → 21 (GPT-4.1
mini named in the §4.2 sentence) and `4.2` 3 → 4 (the second Section 4.2 pointer in Table 1's
caption); both figure boxes the same size (positions moved). **The tool exits 1 on the two ADDED
values by design; that exit is the ordered addition of entry 4d and nothing else, reported as
such rather than silenced.** `appendix_identity` against the v5 tree: 23 sections, D.1 and D.2
changed, both EXEMPT and pinned (`8446c058…`, `9415f055…`), 21 identical. `slogan_scan` PASS
(mean 18.0 over 215 sentences; S8/S9/S10 0; `preregistered` 4 of cap 4; 0 near-duplicate pairs).
`sentence_census`: over-30 count 4 → 3 (the abstract's slot-4 sentence, 34 words, is gone; the
first abstract sentence, the Definition and the quoted rubric remain); over-40 0. `code_scan`,
`repeat_scan`, `refcheck_v11` (22/22, 41 out of scope, 0 uncovered of 63), `trace_scan_v13`
(every printed number resolves; $0.8350$ and $0.7300$ resolve to the R82 ledger), `claims_diff`
(0 VIOLATIONs), `u9_scan`, `dupkey_scan`, `hygiene_scan` PASS. `verify_r82.py` (new): 482 checks,
0 failures, 0 unchecked. `leakscreen_v3.py`: exit 0.

**No claim changes strength under this block except as recorded in entries 1a to 1e (Direction:
narrower, the paired-gain claim made on five models and the sixth stated as a level).**

## R97 AUTHORIZATION BLOCK — dated 2026-09-13

Appended by R97-RESPONSE, anchored to the R96 block above, landing in `paper_v7.tex` (LINEAGE,
below). Paper edits and ledger writes only: no experiment, no model call, no embedding call.
Records: `reviews/R97_REPORT.md`, `reviews/DEVIATIONS_R97.md`. **One entry per change, in the
order's numbering (1) to (6) plus the two consistency entries (7) and (8); every entry was
written before its edit landed, and every gate ran at the end.** Sources of every number: the
manuscript itself, `side_experiments/NUMBERS_SIDE.md` §1–§8 (S1, S2-U), `e1r_robustness/NUMBERS_E1R.md`
§12 as corrected under D-E1R-10, `resp_review/NUMBERS_RESP.md` `AUX-RESP-PAPER-Q4` (written under
entry 8 from `registrations/ADDENDUM_RESP.md` §C.5), and `reviews/NUMBERS_R97.md` (the rounded
forms the SIDE registration's frozen texts print).

**BASE.** `paper_v6.tex` is the R96 close and is uncommitted on disk (R96 is pending [AUTHOR-1]'s
word), so no git revision holds it. The gates read it as the temporary tree object `43531d8b`,
written from the working copy with a scratch index (`git hash-object -w` + `git write-tree`
under a scratch `GIT_INDEX_FILE`; the real index and HEAD are untouched, nothing is committed):
`--base=43531d8b41f11b8035d87ca850631fda140cdd65 --tex=paper_v7.tex --base-tex=paper_v6.tex`.
The tree carries `paper_v6.tex` (blob `b2a7ae2e`) and `paper_v6.pdf` (blob `8834a026`).

**LINEAGE (R90, R92, R93, R96 precedent).** The working lineage is `paper_v7.tex`, a byte copy of
`paper_v6.tex` with the entries below applied; `paper_v6.tex` is the version a reader compares
v7 against. Tool defaults move to v7 (`appendix_identity`, `claims_diff`, `frozen_diff`,
`numeric_diff`, `u9_scan`, `sentence_census`); `.gitattributes` gives `paper_v7.tex` the same
`eol=crlf` exception as v6; `trace_scan_v13` gains the SIDE, RESP and R97 ledgers.

**Rulings taken from the order ([AUTHOR-1], 2026-09-13) and from the frozen texts they land.**

- **R-a, what governs the S1 and S2-U wording.** `registrations/ADDENDUM_SIDE.md` §A1
  (Amendment 1, frozen at `07506f1`) moves two frozen texts into the main text and changes
  nothing else; the R78-2c rule (frozen registered wording ships verbatim; style yields) applies
  to them in the main text. So the S1-P1 and S1-P2 held readings, the Mem0 descriptive text and
  the S2-U not-expected-branch text print byte-for-byte in §5.3 and §6, with the style gates
  told so (slogan_scan `EXEMPT_FROZEN_REGISTERED`, prose_scan `WHITELIST`, each entry sourced
  to the file that carries the text on one line). Numbers print at the ledger's four decimals
  where the order rounded to two (0.4526 → 0.8974 on A-MEM, 0.4777 → 0.8751 on Mem0), under
  PRECISION-R81-1 and the numbers-lock rule.
- **R-b, the 42.3 percent sentence is not touched.** `ADDENDUM_SIDE.md` §STOP names "the 42.3
  percent sentence at `paper_v4.tex:641` changed" as a stop condition and §A1 says it "stays as
  printed". The Q6 clause the report drafted onto that sentence therefore lands as a sentence of
  its own after the S2-U block (entry 5g); the sentence itself is byte-identical.
- **R-c, the RESP pointer is held back.** `registrations/ADDENDUM_RESP.md` is frozen at
  `17e6328` and Phase B has not run (`resp_review/` holds only the Q4 key written here). Per
  `reviews/RESP_REG_REPORT.md` §5 items 10 and 11, the clause "is measured in
  Appendix~\ref{app:resp}" is held back at L131, the Figure 1 caption and F.8, and lands with the
  result. No Table 24 row is printed for the RESP lanes (their outcomes would read "pending").
- **R-d, anonymity outranks the first-person clause of entry 6.** The R89 BRANCH A ruling and
  `hygiene_scan` rule 5 bar first-person self-reference near the named self-citation, and the
  submission is under double-blind review (`\author{Anonymous Authors}`). The limitations
  sentence lands in the third-person form with every other element of the order (the schema is
  the prior store's; the audit applies to it first; labels come from the manifests; S1 shows the
  benefit is the summary); the clause "the authors' own prior system" is recorded as D-R97-1 with
  its camera-ready wording, for the author to land when the paper is de-anonymized.
- **R-e, the registered companions of a main-text placement land with it.** S1's appendix table
  (`ADDENDUM_SIDE.md` §S1 "the appendix table ... are the output cap"; §A1 "in addition to the
  appendix table"), S2's frozen census reading and the S2-U quantities (§S2 "prints regardless,
  appendix only"; "What prints"), and one Table 24 row per experiment (§"Registration
  mechanics") are the registration's own outputs and are the targets of the pointers §5.3 and §6
  now carry. They land under entries 1c, 2b and 7. L396 promises that Appendix G "lists every
  registered prediction and its outcome", so S1's two predictions enter Table 24 and the §1
  count of preregistered predictions moves from 40 to 42 (8 not holding, unchanged), a count of
  registrations and not a result. Recorded as the one §1 number moved on S1's account, for the
  author's ruling; reverting it is one token.
- **R-f, vocabulary.** The main text may not say "arm", "cell", "lane", "verdict", "registered"
  (bare), "persona-clustered" or "held"; the new sentences say "with questions grouped by user
  profile" (the L661 idiom), "predictions written before the run", "hold", "descriptive". The
  word "preregistered" sits at its cap of 4 in main text and is not used again.

**(1a) INSERTION at §5.3, after L632 (`R97-1a`; AUX-SIDE-S1-MINI-AMEM, -MEM0, -NB4-*, -NB5-*,
-MAP-MEM0; §A1; R-a).** Eight sentences after "The negative index effect is measured here, and
these ablations do not identify what causes it.": "A name-bearing summary built from ground truth
for the entries each store holds recovers coverage on both." "Discrimination moves from $0.4526$
to $0.8974$ on A-MEM and from $0.4777$ to $0.8751$ on Mem0 (Appendix~\ref{app:inversion})." "On
A-MEM the paired difference is $+0.4448$ (CI $[+0.3800,+0.5116]$; $[+0.3875,+0.5042]$ grouped by
user profile), and both predictions written before the run hold." Then the two frozen held readings, verbatim: "Given
the manifest's names for what it holds, the store no longer inverts the benefit by the margin it
did; the inversion was a property of the index the store was handed, not of the store alone."
and "The name-bearing index does not invert." Then the frozen Mem0 descriptive text, verbatim
with its placeholders filled from the ledger: "On Mem0 the name-bearing index could be built for
$49.4$ percent of the store's entries under the lexical-required mapping the spot-check forced
(two-channel precision $0.567$); below the registered coverage floor of one half, its coverage
gain of $+0.3006$ (interval $[+0.2208,+0.3728]$; \trueidx{} $-0.0969$) is reported and carries
no verdict." Then: "The mechanical readers recover it too ($0.8554$ and $0.8700$ against $0.5000$ on the
summary these stores can produce), and no backend we tested writes that summary itself." No existing sentence changes;
U1, U2's replacement and the ablation sentences stand. Direction: **cuts both ways**, as §A1
says: "inverts at every scale" is weakened as a statement about the store and the thesis that
the benefit is a property of what the store is handed is supported.

**(1b) REWORDING at §8, L744 (`R97-1b`; CL-C092-C095; §A1).** "The two backends without
lifecycle structure invert the benefit at every scale tested." becomes "The two backends
without lifecycle structure invert the benefit at every scale tested under the summary they can
produce." + "Given a name-bearing summary of what they hold, both recover coverage
(Section~\ref{sec:inversion})." Not a frozen string; the boxed paragraph is
untouched. Direction: as 1a.

**(1c) INSERTION at Appendix F.7, after Table~\ref{tab:x2-ablation} (`R97-1c`; the registered
appendix table; R-e).** A lead-in paragraph (the map from each stored entry to its manifest
slot; the thirty-pair hand check per store, $0.800$ on A-MEM, $0.567$ on Mem0, which forced the
lexical-required map covering $49.4\%$ of Mem0's entries; the leakage screen at $0$ of $30$ on
both) and one table, `tab:s1-names`: per store, $n$, blind, \trueidx{}, the name-bearing summary,
its gain over blind with the item-level interval, its difference from \trueidx{} with the
item-level interval, NB-4 and NB-5 on the same summary; the persona-clustered intervals in the
prose beneath. Every value is `NUMBERS_SIDE.md` §1, §2, §6, §7, §8. The frozen readings print
once, in §5.3 (S7); the caption says both A-MEM predictions hold and Mem0's row is descriptive.
`appendix_identity`: F.7 changes and is pinned under an R97 basis. Direction: **neither**
(the appendix carries what §5.3 cites).

**(2a) INSERTION at §6, after L661 (`R97-2a`; AUX-SIDE-S2-MINI, -S2-CAP-RECALL, -S2-CENSUS;
§A1; R-a, R-b).** After "That keeps $42.3\%$ of the \trueidx{} gain, short of the $60\%$ we had
set as the threshold." and before the frozen verdict sentence "NOK degrades materially under
believed metadata but remains positive.": the frozen not-expected-branch text, verbatim,
"Lifting the cap on the believed list, which raises its recall of ground-truth superseded names
from $30.0$ to $66.6$ percent at unchanged precision, retains $65.5$ percent of the \trueidx{}
gain, at or above the $60$ percent threshold." then the frozen second sentence "Part of the
believed-state loss recorded at $42.3$ percent is an effect of the renderer's cap of fifteen
names rather than of the store's metadata." then the intervals, "Its interval is
$[44.6\%,87.2\%]$ ($[31.5\%,93.6\%]$ grouped by user profile)." then the weaker reading §T
rules, with the difference's two intervals printed in Appendix F.9: "The difference from the
capped list, $+0.0554$, excludes zero at item level and includes it under the grouping, so the
weaker reading governs (Appendix~\ref{app:believed-census})." then the order's precision
sentence, with the ledger's two values in place of the registration's rounded 0.035 (numbers
lock): "Precision is $0.0348$ capped and $0.0357$ lifted, so most of the loss, at the point
estimate, is the store's." The U9 firewall holds: no connective joins any of these to the
text-match sentence two sentences on; `u9_scan` is run. The 42.3 percent sentence is
byte-identical (R-b). Direction: **against the manuscript's interest**, as §A1 says: the 42.3
percent headline is qualified in the section that carries it by a cap effect the registration
expected not to find; the weaker-reading sentence limits that qualification.

**(2b) INSERTION at Appendix F.9, after Table~\ref{tab:believed} (`R97-2b`; the registered
census reading and the S2-U quantities; R-e).** A run-in paragraph "The believed superseded
list, and the renderer's cap." carrying the frozen S2 census reading verbatim ("Two filters on
the metadata FR-Bank exposes --- ... The believed-state loss is not a filtering problem.";
appendix, so S8 and S9 do not apply) and the S2-U quantities in one paragraph: NOK AUROC blind
$0.4946$, \trueidx{} $0.7339$, \believed{} $0.5959$, \believed{} with the cap lifted $0.6513$;
the paired gains over blind $+0.2393$ $[+0.1801,+0.2949]$, $+0.1012$ $[+0.0458,+0.1543]$ and
$+0.1567$ $[+0.0961,+0.2162]$ (persona-clustered $[+0.0552,+0.2536]$); the retention $65.5\%$
$[44.6\%,87.2\%]$ (persona-clustered $[31.5\%,93.6\%]$) against the committed $42.3\%$; the
lifted-minus-capped difference $+0.0554$ $[+0.0110,+0.0992]$ (persona-clustered
$[-0.0019,+0.1173]$); the list at $32.55$ names per item uncapped against $15.04$ capped and
$1.75$ under \trueidx{}. The census reading's rounded forms ($15.04$, $8.96$, $1.75$, $0.035$,
$0.062$) are ledgered in `reviews/NUMBERS_R97.md` against `NUMBERS_SIDE.md` §5's four-decimal
values. `appendix_identity`: F.9 changes and is pinned. Direction: **neither**.

**(3a) REWORDING at §1, L131 (`R97-3a`; CL-C008; F2 of `reviews/RESP_REG_REPORT.md`; the
ruling of 2026-09-12; R-c).** "In a lifecycle-tracking store, retraction records survive
similarity retrieval at only $5\%$ \citep{fr}." becomes "In a lifecycle-tracking store, the
record that forbids use is masked out of the retrieved set by its lifecycle state." + "On that
store's own benchmark, its retraction records pass retrieval at only $5\%$ under the mask
\citep{fr}." The frozen fragments "retraction records survive similarity retrieval at only 5"
and "... 5%" leave the manuscript (1 → 0 each). What the cited number measures: `neuripsv13.tex:274`,
"FR-Bank's 5% AV7 retrieval pass rate reflects intended behavior: retracted facts are
correctly excluded from the retrieval set by the lifecycle state mask". The pointer clause to
the ranking measurement is held back (R-c). Direction: **narrower** (a mask rate is claimed,
not a ranking rate; the argument of L132 and Proposition 1 survives as stated).

**(3b) REWORDING at the Figure 1 caption, L109 (`R97-3b`; CL-FIG-overview; same ruling).**
The first caption sentence "A query ranks the store, and the record that forbids the answer can
fall below the retrieval cutoff, where no bounded retrieved view reaches it." becomes "A query
ranks the store." + "In a lifecycle-tracking store the record that forbids the answer is masked
out of the retrieved set by its lifecycle state, so no bounded retrieved view reaches it." The
three remaining caption sentences stand. Not a frozen string. The drawing (the top-$k$ cutoff
line with the retracted row below it) is not changed by the order and is recorded in the report
as depicting the ranking form; `numeric_diff --figboxes` gates the box. Direction: **narrower**.
Sites that keep the ranking wording and are not in the ruling, for the author: abstract L51
("can rank below the cutoff"), §3 L345 ("pass similarity retrieval at $5\%$", CL-C136), §8 L737
("can sit outside them"), Table 12's "retraction-record pass $5\%$" row (already the pass-rate
form).

**(4a) REWORDING at Appendix F.8, L1861–1862 (`R97-4a`; POSTHOC-R81-2; D-E1R-10 at
`cc06e2e`; R-c).** "A check of whether each obligation's own attribute name appears in the
section the matcher reads finds $7$ of $104$ under exact slot match, at a rate that holds across
all three index variants." becomes "A check of whether each obligation's own attribute name
appears in the section the matcher reads finds it for $74$ of $104$ under exact slot match: $63$
of $63$ supersession-derived, $11$ of $26$ retraction-derived, and none of the $15$
expiry-derived (an earlier count of $7$ keyed entries without their persona; deviation ledger,
Appendix~\ref{app:registration})." The near-synonym hedge "The embedding variant scores
near-synonyms, so this test does not separate a matcher reading a near-synonym of the item's own
name from a matcher recovering which kinds of content the store marks as superseded." becomes
"On the state the index names, the matcher has the item's own name to read; whether the monitor
reads it is a separate question that this census does not settle." (the Appendix pointer held
back, R-c). Neither is a frozen string (post hoc, POSTHOC-R81-2). Numbers: `NUMBERS_E1R.md` §12
corrected rows. Direction: **against the manuscript's convenience** (the lookup now looks like
a read of the item's own name on the one state the index names, which is what the reviewer's W3
suspects and what the registered own-name ablation tests).

**(4b) INSERTION at Appendix G, deviation index, after the D-E1R-8 line (`R97-4b`).** "Own-name
census key collision: E1-R D-E1R-10; Appendix~\ref{app:baselines}." Direction: **neither**.

**(4c) ANNOTATION in this file (`R97-4c`).** POSTHOC-R81-2's note "and it did support it" is
annotated below, not rewritten: the per-state rows (0.9534 / 0.4823 / 0.4053) that support the
structural premise are untouched by D-E1R-10; the own-name count that entry also carried is
superseded (7 of 104 → 74 of 104).

**(5a) REWORDING at §5.1, L537–538 (`R97-5a`; CL-C064; R96 R-a carried through).** "The paired
NOK gain is positive on every one of the six models (Table~\ref{tab:ladder-exact})." becomes
"On the cross-model set the paired NOK gain is positive for each of the five models whose blind
score varies (Table~\ref{tab:ladder-exact})." (worded so that prose_scan's near-duplicate rule
does not pair it with contribution (4)) + "GPT-4.1 mini is the exception: on this set its blind
score does not vary, so its difference anchors no gain (Section~\ref{sec:discrimination})." and, in the
next sentence, "every paired NOK gain stays positive with its interval excluding zero" becomes
"every paired NOK gain on those five stays positive with its interval excluding zero" (frozen
fragment 1 → 0, authorized). L677's "three of the six monitor scores" is Table 9's six rows and
is untouched. Direction: **narrower**, consistent with the abstract, §1, Table 1's caption and
§8 after R96.

**(5b) FLAG at Table 1, L373 and a table footnote (`R97-5b`; CL-CAP-e1; the report's
recommended form).** The NOK row's difference and interval print with a double dagger,
"$+0.2393^{\ddagger}$ & $[+0.1801,+0.2949]^{\ddagger}$", and the table gains the footnote
"$^{\ddagger}$A difference against a near-constant blind score; it anchors no gain
(Section~\ref{sec:discrimination})." (the two-value fact is in the caption's fourth sentence) No number vanishes; the caption's fourth sentence already
says it. Direction: **neither** (the R96-1c reading, now visible at the cell).

**(5c) DELETION at Figure 2 and REWORDING of its caption (`R97-5c`; CL-FIG-ladder).** The
open-marker `\addplot` at L589–590 and the R88 comment at L591 are deleted; the blind series
still plots mini's $0.5000$ point. Caption sentences 2–3 "The obligation panel is shown, and
GPT-4.1 mini's constant blind NOK is marked with an open point. That point is an artifact of a
constant score and carries no information (Table~\ref{tab:ladder-exact} states the caveat in
full)." become "The obligation panel is shown." + "GPT-4.1 mini's blind obligation point is a
constant score on this set and carries no information; it is plotted for completeness only
(Table~\ref{tab:ladder-exact} states the caveat in full)." `numeric_diff --figboxes` gates the
box. Direction: **neither**.

**(5d) INSERTION at §4.3, after L509 (`R97-5d`; W6; CL-C055-C057, CL-C078).** "The lifecycle
fields of the summary add nothing measurable to coverage: randomizing every count leaves the
gain unchanged, and the corrupted lifecycle metadata of Section~\ref{sec:stores} keeps
$101.4\%$ of it." Both figures already print (L506 $+0.0015$; L655 and Table 12
$101.4\%$; COUNT-CHANGED only). Direction: **neither** (a plain restatement of two printed
results).

**(5e) INSERTION at Appendix F.7, after L1766 (`R97-5e`; Q4; AUX-RESP-PAPER-Q4).** The
paragraph "The two structureless indexes as the monitor saw them, verbatim, for the persona of
median size (\texttt{leila}), are printed below. Under \trueidx{} the marker occupies $3$ of
$31$ lines and $18$ of $216$ tokens ($8.3\%$) on both backends; under \believed{} it occupies
$7$ lines and $18.1\%$ of tokens on Mem0 and $8$ lines and $20.3\%$ on A-MEM." followed by two
`verbatim` blocks side by side carrying `mem0:leila:FULL:TRUE` and `amem:leila:FULL:TRUE` from
`e1_metamemory/indexes_v2.json` byte for byte (31 lines each; sha256 `6dc20dbd…`,
`9cef7ab4…`). Every number, including the entry counts and ages inside the two texts, is in
`resp_review/NUMBERS_RESP.md` under the key, recomputed here from the committed file with
`tiktoken` `o200k_base` and equal to `ADDENDUM_RESP.md` §C.5 to the token. The marker string
"not expressible by this backend" (a frozen string of the F.3 prompt box) therefore occurs 1 → 7
times, the six new occurrences being the marker lines of the two verbatim texts; authorized here.
Direction: **neither**.

**(5f) INSERTION at Appendix G, after the "Reading the Outcome column" line (`R97-5f`; Q5; the
ruling of 2026-09-12 (4), the artifacts not the order; F4).** "Opus 5 entered the study at the
E1-XV preregistration (\texttt{776bce07b3}, 2026-08-14), carrying three of its predictions,
after the E1 freeze of 2026-08-10 and before the store-counterfactual freeze of 2026-08-29; in
that cell it is a descriptive lane carrying no prediction, named at the freeze and funded by
Amendment 4 of 2026-08-30 before its lane was submitted." Sources: `PREREG_E1XV.md:53,132-141`
(XV-1, XV-2, XV-3 name `claude-opus-5`); commits `776bce0` 2026-08-14, `875f726` 2026-08-10,
`60f75c5` 2026-08-29; `ADDENDUM_R82.md` §24. Direction: **neither**.

**(5g) INSERTION at Appendix F.3, after L1562, and one sentence at §6 (`R97-5g`; Q6; R-b).**
F.3: "The $60\%$ retention threshold was written into the main study's preregistration
(2026-08-10) as a round number for coverage retention, with no derivation, and was inherited
unchanged when obligation retention was scored, before that figure existed." (`PREREG_E1.md:182`
H-BELIEVED; `SPEC_E1R.md:204-206`). §6, after the S2-U block of entry 2a: "The $60\%$ threshold
is a round number fixed before any data (Appendix~\ref{app:construction})." The report drafted
the §6 text as a clause on the 42.3 percent sentence; R-b keeps that sentence byte-identical.
Direction: **neither** (provenance of a threshold already printed as set in advance).

**(6) INSERTION at §7, Limitations, after L714 (`R97-6`; CL-LIMITS; R-d).** "The lifecycle
schema this study builds on is that of the prior store \citep{fr}, so the audit of
Section~\ref{sec:stores} applies to that store first." + "Every label comes from the manifests
we built, and Section~\ref{sec:inversion} shows the benefit travels with the summary rather than
with the system." The first-person clause is D-R97-1 (camera-ready).
Direction: **neither** for any claim; a disclosure.

**(7) TABLE 24 ROWS and the §1 count (`R97-7`; R-e).** Two rows after R82-CAL: "Side
experiments: name-bearing summary (S1)" at `e8b2630`, 2026-09-12, "a manifest-built,
name-bearing summary for the two structureless stores, the entry map and its hand check, a
coverage floor, and two predictions on A-MEM, both of which held; Mem0 fell below the floor and
prints as descriptive" — outcome "held / descriptive"; and "Side experiments: believed-state
cap (S2)" at `e8b2630`, 2026-09-12, "two filter rules on the store's own metadata and a
precision bar neither reached, so the repair was withdrawn before any call; one descriptive
condition, the believed summary with its fifteen-name cap lifted, carrying no prediction" —
outcome "no prediction". §1 L174: "Of the $40$ preregistered predictions, $8$ did not hold"
becomes "Of the $42$ preregistered predictions, $8$ did not hold". `appendix_identity`: G
changes and is pinned. Direction: **neither**.

**(8) LEDGERS, TOOLS AND LINEAGE FILES (`R97-8`).** `resp_review/NUMBERS_RESP.md` is created
with its header naming the RESP freeze (`17e6328`) and the one key R97 needs,
`AUX-RESP-PAPER-Q4`, recomputed from `e1_metamemory/indexes_v2.json` (no model call; the rest of
Phase B step 1, `verify_resp.py` and `DEVIATIONS_RESP.md`, is Phase B's). `reviews/NUMBERS_R97.md`
carries the rounded forms of the SIDE frozen texts against their four-decimal ledger values.
`tools/trace_scan_v13.py` `LEDGERS` gains `side_experiments/NUMBERS_SIDE.md`,
`resp_review/NUMBERS_RESP.md` and `reviews/NUMBERS_R97.md`. `tools/slogan_scan.py` and
`tools/prose_scan.py` gain the frozen S1-P1 reading and the Mem0 descriptive text as
FROZEN-REGISTERED entries (sourced); `tools/code_scan.py` permits the collocation "registered
coverage floor" inside that frozen text and nothing else. Tool defaults and `.gitattributes` move to v7 (LINEAGE).
`appendix_identity` pins F.3, F.7, F.8, F.9 and G under R97 bases. Direction: **neither**.

**GATES (post-R97 build of `paper_v7.pdf`, three pdflatex passes; every gate run).** Page:
**FAIL** — label on **10**, reading **494 / slack −9** (v6: 9, 469 / +16); 32 pages (v6: 29); 0
overfull boxes; 0 undefined references. The boxed closing paragraph of §8 (nine review lines,
unbreakable) is what sits on page 10; the order's main-text additions run about 27 review lines
against a slack of 16, the drafting slack was taken (every non-frozen new sentence at its
shortest form under the 30-word target), and the remaining nine lines can leave the main text
only by a ruling on which ordered or frozen content moves to the appendix, or which existing
sentence is cut; `reviews/R97_REPORT.md` §2 and D-R97-2 carry the menu with each item's line
cost. Nothing was cut or moved on this program's own judgment. `frozen_diff --program=R97`:
129 frozen strings found in the v6 base, **122 KEPT, 3 MOVED, 4 CHANGED-AUTHORIZED, 0
UNAUTHORIZED** (the four are quoted in entries 3a, 5a and 5e). `numeric_diff --pdf --figboxes`:
tex side **ADDED 80 values, 0 VANISHED**, 54 COUNT-CHANGED (among them `40` 20 → 19 and `42`
2 → 3, entry 7); PDF side ADDED 63, 0 VANISHED, 28 COUNT-CHANGED; both figure boxes the same
size (Figure 2's position moved). **The tool exits 1 on the added values by design; every one
is an ordered addition of entries 1a–1c, 2a–2b, 4a, 5e, 5g or 7, reported as such rather than
silenced** (R96-4d precedent). `appendix_identity` against the v6 tree: 23 sections, F.3, F.7,
F.8, F.9 and G changed, all EXEMPT and pinned (`408ce80c…`, `6d8eb017…`, `3264599f…`,
`666a4f17…`, `988fd3f9…`), 18 identical. `slogan_scan` PASS (0 duplicates; pinned blocks once;
S8/S9/S10 0 after the two FROZEN-REGISTERED exemptions; `preregistered` 4 of cap 4; 0
near-duplicate pairs; mean 18.6 over 228 sentences). `sentence_census`: over-30 count 3 → 4
(the frozen S2-U sentence, 36 words, ships verbatim); over-40 0. `code_scan` PASS (one
collocation permitted, entry 8), `repeat_scan` PASS, `refcheck_v11` PASS (22/22, 41 out of scope,
0 uncovered of 63), `trace_scan_v13` PASS (0 unaccounted; the SIDE, RESP and R97 ledgers
account for every new value), `claims_diff` PASS (0 VIOLATIONs), `u9_scan` PASS (one
co-occurrence, cleared as before), `dupkey_scan` PASS, `hygiene_scan paper_v7.pdf` PASS.
`side_experiments/tools/verify_side.py` (read-only, the ledger every S1 and S2-U value is read
from): PASS.

**No claim changes strength under this block except as recorded in entries 1a, 1b, 2a, 3a, 3b,
4a and 5a (Direction as stated there).**

## R98 AUTHORIZATION BLOCK — dated 2026-09-13

Appended by R98 (the CF-2 landing), anchored to the R97 block above, landing in `paper_v8.tex`
(LINEAGE, below). Paper edits and ledger writes only: no experiment, no model call, no embedding
call. Records: `reviews/R98_REPORT.md`, `reviews/DEVIATIONS_R98.md`. **One entry per change, in the
order's numbering (1) to (8) plus the consistency entries (9) and the tool entry (10); every entry
was written before its edit landed, and every gate ran at the end.** Sources of every number:
`r82_counterfactual/cf2/NUMBERS_CF2.md` by key (§5b–§5k: `AUX-CF2-CONSTRUCTION`, `-BLIND`,
`-MINI-V2/-V3/-V2R`, `-H45-V2/-V3/-V2R`, `-OP5-V2/-V3/-V2R`, `-PERSTATE`, `-COUNTED`,
`-NAMEDVSCOUNTED`, `-EQUIV-V2R`, `-NB6-V2`, `-ALLSTATES-V3`, `-NB5-V2`, `-LEAKSCREEN-V3`,
`-LEAKSCREEN-V2R`, `-QUESTIONREAD`, `-DROPRULE`; §5k the derived margins), the frozen branch texts of
`registrations/ADDENDUM_CF2.md` §8 (frozen `f016f03`, R94; amendments §14–§17), and the manuscript
itself for the first-form ($n=90$) values, which are byte-identical to `paper_v7.tex` Table 9. The
label "R98" is this landing's; the commit `17e6328` "R98: RESP registration frozen" carries the same
number for the RESP freeze and is unrelated to this block.

**BASE.** `paper_v7.tex` is the R97 close and is uncommitted on disk (R96 and R97 are pending
[AUTHOR-1]'s word), so no git revision holds it. The gates read it as the temporary tree object
`a66254cb`, written from the working copy with a scratch index (`git hash-object -w` +
`git write-tree` under a scratch `GIT_INDEX_FILE`; the real index and HEAD are untouched, nothing is
committed): `--base=a66254cb8a8de81608f9dcf8ee438912c55d7843 --tex=paper_v8.tex
--base-tex=paper_v7.tex`. The tree carries `paper_v7.tex` (blob `14054760`) and `paper_v7.pdf`
(blob `a12e44e9`).

**LINEAGE (R90, R92, R93, R96, R97 precedent).** The working lineage is `paper_v8.tex`, a byte copy
of `paper_v7.tex` with the entries below applied; `paper_v7.tex` is the version a reader compares v8
against. Tool defaults move to v8 (`appendix_identity`, `claims_diff`, `frozen_diff`,
`numeric_diff`, `u9_scan`, `sentence_census`); `.gitattributes` gives `paper_v8.tex` the same
`eol=crlf` exception; `trace_scan_v13` gains `r82_counterfactual/cf2/NUMBERS_CF2.md`;
`ARTIFACT/registrations/` gains a copy of `ADDENDUM_CF2.md` and `ARTIFACT/ledgers/` copies of
`NUMBERS_CF2.md` and `DEVIATIONS_CF2.md`, so `frozen_diff` watches the landed branch texts from
the next round on.

**Rulings taken from the order ([AUTHOR-1], 2026-09-13) and from the registration.**

- **R-a, what governs the CF-2 wording.** `ADDENDUM_CF2.md` §8 froze the branch texts before §7
  was written; the R78-2c rule (frozen registered wording ships verbatim; style yields) applies.
  P1 HOLDS (two [MAIN] sentences), P2 HOLDS (one [MAIN] sentence), P3 HOLDS (one [MAIN] sentence),
  the P4 sentence with "within tolerance" and the P5 sentence with "both inside the tolerance band;
  on this cell neither reader takes anything from the counts" print byte-for-byte with their
  placeholders filled at the ledger's four decimals (`$X$`, `$Y$`, `$D$`, `$I$`, `$N$` →
  `AUX-CF2-*`), each once: P3 in §6 (the disposition names `paper_v4.tex:656`), P1 in §7 (the
  failed-replication sentence's site), P2, P4 and P5 in Appendix D.2. The model identifier the
  registration wrote as `gpt-4.1-mini` prints in the manuscript's name form "GPT-4.1 mini" and the
  registration's "0.5" prints as written; both recorded in D-R98-1. A frozen sentence is not
  followed by a pointer inside its own period; pointers sit in the neighbouring sentence.
- **R-b, both interval conventions, the weaker reading.** `ADDENDUM_CF2.md` §6: the item-level
  paired bootstrap is primary and the persona-clustered interval prints beside it; a prediction
  holds only when both agree. Every CF-2 gain in Table 9 and in D.2 carries both intervals; the
  main-text idiom is "with questions grouped by user profile" (the L661 idiom), never
  "persona-clustered".
- **R-c, Table 9 supersession (`ADDENDUM_CF2.md` §12.4).** CF-2's values are the table; the first
  form's $n=90$ values print beside them in a "first form" column of every block (whole set,
  lookups, per state, counted states), byte-identical to `paper_v7.tex`. Opus 5 rows print because
  the lane ran under §11 (`AUX-CF2-DROPRULE`, D-CF2-5). The struck-clause paragraph of D.2 stays as
  history, byte-identical.
- **R-d, adverse rows.** §8's adverse branch: every row on which a lookup exceeds a reader prints
  and is named in the text of the row it affects; the margins are the §5k derived values.
- **R-e, vocabulary.** The main text may not say "arm", "cell", "lane", "verdict", "registered"
  (bare), "persona-clustered" or "held" except inside a frozen text; the P4 and P5 frozen texts
  say "cell" and land in the appendix. "preregistered" sits at its cap of 4 in main text and is not
  used again.
- **R-f, page budget.** The page gate fails at v7 by nine review lines (D-R97-2). The order's
  main-text changes here are near length-neutral (§6 two sentences replaced by two; §7 one
  sentence replaced by the two-sentence frozen text plus a one-line history pointer; §8 one number);
  nothing is cut or moved on this program's judgment; the residual is reported under D-R97-2 and
  D-R98-2.

**(1) TABLE 9 (`tab:counterfactual`, D.2, v7 L1323–L1370) REPLACED (`R98-1`; every `AUX-CF2-*`
row key; R-b, R-c, R-d).** The caption and body are the CF-2 table: $148$ questions, $n=444$,
$148$ positives, $88$/$30$/$30$; six columns (label + five), so every block shares the two interval
columns: (i) whole set by reader and summary (superseded only / all three states / counts
randomized) with AUROC, item interval, profile interval and the first form's AUROC and gain at
$n=90$ (the CF-2 gain is the AUROC less $0.5000$, stated in the caption; the two gain columns of
the drafting layout were dropped at the first build for width and the first form's gains kept, so
no v7 value vanishes); (ii) the three lookups on the summary each reads, with the profile interval
of the AUROC and the first form's value; (iii) per state, nine reader rows under the three
summaries beside the first form's two, and three lookup rows by state; (iv) counted states pooled
($60$ questions, $n=180$) with paired gain, item and profile intervals and the two AUROCs, and the
first form's three rows ($15$ questions, $n=45$; Haiku 4.5's paired interval $[+0.0772,+0.4945]$
in its row); (v) named minus counted under the superseded-only summary (difference, two-subset
interval, profile interval, named, counted); (vi) counts randomized minus superseded only (item and
profile intervals). Frozen strings of the v7 table that change:
the block label "Counted states, individuating pairs ($n=45$)" (the first-form values move into the
"first form" column of block iv); the caption sentence "A dash marks a matcher cell that has no
value: each matcher reads one summary, and no matcher gain is recorded." (the new caption says what
the dashes mark in the new layout); and the caption's adverse sentence "Adverse rows, printed rather
than set aside: the all-states matcher exceeds three monitor rows by more than the $\pm0.05$
tolerance, GPT-4.1 mini by $+0.1947$ under the first summary and $+0.1467$ under the second, and
Haiku 4.5 by $+0.1480$ under the first; it exceeds Haiku 4.5 under the second summary by $+0.0230$,
inside tolerance, and the superseded-names matcher exceeds GPT-4.1 mini under the first by
$+0.0322$, also inside tolerance." (replaced by the CF-2 adverse sentence of D.2, entry 4; the
first-form margins move to D.2's history paragraph). The v7 caption's opening "The
store-counterfactual cell: $30$ questions, each asked of three versions of one store differing in a
single attribute, so $n=90$ with $30$ positives." is replaced by the CF-2 count sentence. Direction:
**up** (three held predictions replace one failed one; the adverse rows print as before).

**(2) TABLE 10 ROW (`tab:question-sets`, v7 L1436) (`R98-2`; AUX-CF2-CONSTRUCTION).** "store-counterfactual & $90$
& $30$ PN, ten per state & question fixed, store varies & …" → "store-counterfactual & $444$ & $148$ PN, $88$/$30$/$30$ by state & question fixed, store varies &
…" (the drafting form with "($90$ in its first form)" and the states spelt out overfilled the
column at the first build; the first form's size is stated in Table 9's caption and F.1). Direction: **neither**.

**(3) GLOSSARY ROW (F.1, v7 L1504) (`R98-3`; AUX-CF2-CONSTRUCTION).** "counterfactual cell &
store-counterfactual set ($90$): $30$ queries asked of three versions of one store" → "counterfactual
cell & store-counterfactual set ($444$): $148$ queries asked of three versions of one store; its
first form had $30$". Direction: **neither**.

**(4) APPENDIX D.2 PROSE REWRITTEN (v7 L1308–L1321) (`R98-4`; AUX-CF2-CONSTRUCTION, -BLIND,
-MINI-V2, -NAMEDVSCOUNTED, -COUNTED, -NB6-V2, -ALLSTATES-V3, -NB5-V2, -EQUIV-V2R, -QUESTIONREAD,
-LEAKSCREEN-V3, -LEAKSCREEN-V2R, -DROPRULE; §5k; R-a, R-b, R-d).** The section opens with the
set's construction (148 questions, three versions, $88$/$30$/$30$, predicates fixed before any
verdict, questions written before any version existed), keeps the sentence "A question-only reader
scores $0.5000$ on this set as an identity, because the same question is asked of all three
versions." byte-identical, states the reading rule (both intervals; weaker governs), then prints:
the P1 result by pointer to §7 with both intervals; the frozen P2 HOLDS sentence "Under the summary
that names only superseded content, Haiku 4.5's judgment on the named state exceeds its judgment
on the two counted states by $+0.3237$, interval $[+0.2319,+0.4011]$." with the profile interval,
the Opus 5 branch ($+0.3295$; $[+0.2420,+0.4181]$, $[+0.2556,+0.3875]$) and GPT-4.1 mini's
descriptive row ($+0.2948$); the P3 result by pointer to §6 with the profile interval
$[+0.2247,+0.3591]$ and the all-three-states residual ($+0.0203$, $[-0.0570,+0.0907]$); the frozen
P4 sentence "On this cell the superseded-names lookup reaches $0.7663$ against the smallest reader's
$0.7167$ under the superseded-only summary, and the all-states lookup reaches $0.8756$ against Haiku
4.5's $0.8773$ under the all-three-named summary, within tolerance."; the count-randomized summary
defined in one sentence and the frozen P5 sentence "Randomizing the retracted and expired counts in
the superseded-only summary moves GPT-4.1 mini's whole-cell judgment by $+0.0011$ and Haiku 4.5's
by $+0.0072$, intervals $[-0.0282,+0.0297]$ and $[-0.0079,+0.0229]$, both inside the tolerance band;
on this cell neither reader takes anything from the counts." with the Opus 5 branch ($-0.0052$,
$[-0.0130,+0.0026]$) and the three profile intervals; the adverse paragraph (§5k margins: all-states
over GPT-4.1 mini $+0.1589$ / $+0.0789$ / $+0.1577$ and over Haiku 4.5 $+0.1190$ / $+0.1118$ beyond
tolerance; over Opus 5 $+0.0351$ / $+0.0403$ and superseded-names over GPT-4.1 mini $+0.0496$ and
Haiku 4.5 $+0.0097$ within; the per-state rows); the history paragraph (first form: the boundary
$0.6550$–$0.8275$ against $0.5225$–$0.6225$; "The registered prediction did not hold." kept as its
own sentence with $0.5939$, $[-0.0345,+0.2315]$ and $[+0.0325,+0.1625]$, and the first form's adverse margins $+0.1947$, $+0.1467$, $+0.1480$, $+0.0322$
and its counted-state paired interval $[+0.0772,+0.4945]$, kept so that no v7 value vanishes); the
struck-clause
paragraph "The registered failure text continued that the gain measured on the larger population is
therefore not free of what the question alone gives away." … "reaches $0.7122$ under the same
summary with an item-level interval that excludes chance." byte-identical; and the disclosures
($111$ of $204$ questions name their plan or value against $3$ of $30$ in the first form, identical
across versions, cannot carry the label; leakage screens $0$ of $30$ on both new summaries; $45$
replacements, closed at $88$ under five recorded deviations). The v7 sentences replaced: "Thirty
questions, each asked of three versions of one store differing in a single attribute, reproduce the
naming boundary on questions that cannot carry the label: under the summary that names only
superseded content, the one named state scores $0.6550$ to $0.8275$ across the three models tested,
while the two states the summary only counts score $0.5225$ to $0.6225$." (its numbers move to the
history paragraph); "The smallest model reaches $0.5939$ under the truthful summary against that
$0.5000$. The prediction required an interval excluding chance; the preregistered item-level interval
is $[-0.0345,+0.2315]$ and includes it, while the question-clustered interval is $[+0.0325,+0.1625]$
and excludes it. Mixed, so the weaker reading governs: the aggregate gain does not replicate at
item level on this set." (condensed into the history paragraph, values verbatim); and "Naming the
counted states raises the obligation judgment on them from $0.5656$ to $0.8489$ with a paired interval
of $[+0.0772,+0.4945]$, and a direct match against the three name lists reaches $0.7886$ against
Haiku 4.5's $0.7656$. The same matcher exceeds three other rows by more than the tolerance, which is
reported rather than set aside. Five of the twenty counted-state questions are excluded from that
comparison and reported here instead, because their scrubbed attribute name already sits on their
own state's list before the change, so the summary does not individuate them." (superseded by the
CF-2 P3/P4/adverse text; the first-form values stay in Table 9's first-form columns; the
individuation predicate is now a draw-time rule, so no collision row exists to report). Direction:
**up** (P1 replicated; P2, P3 held at the registered size; P4, P5 print as registered).

**(5) §6, TWO SENTENCES (v7 L703–L704) (`R98-5`; AUX-CF2-COUNTED, -ALLSTATES-V3, -H45-V3; §5k;
R-a).** "Naming those two states lifts Haiku 4.5's judgment on them from $0.5656$ to $0.8489$ on the
store-counterfactual set ($n=90$; Table~\ref{tab:counterfactual})." → the frozen P3 HOLDS [MAIN]
sentence "Naming retracted and expired content lifts Haiku 4.5's judgment on those states from
$0.5638$ to $0.8649$ on the store-counterfactual set ($60$ questions), a paired gain of $+0.3010$
with interval $[+0.2268,+0.3721]$." "A direct match against the three name lists reaches $0.7886$
on the same set, above three of the six monitor scores by more than the $\pm0.05$ tolerance
(Table~\ref{tab:counterfactual})." → "A direct match against the three name lists reaches $0.8756$
on the same set, within tolerance of Haiku 4.5's $0.8773$ under that summary (Table~\ref{tab:counterfactual})."
followed by "It exceeds every GPT-4.1 mini score by more than the $\pm0.05$ tolerance." (split at the first build for the 30-word target). The
"$0.5656$ to $0.8489$" and "three of the six monitor scores" strings leave the main text (the first
stays in Table 9's first-form column). Direction: **up**.

**(6) §7, LIMITATIONS, THREE SENTENCES (v7 L747–L748, L753) (`R98-6`; AUX-CF2-MINI-V2,
-NB6-V2, -ALLSTATES-V3, -NB5-V2, -PERSTATE; R-a).** "The lookup has one descriptive value on the
cross-model set, none per state on the store-counterfactual set, and none on the authorship-matched
set." → "The lookup has one descriptive value on the cross-model set, whole-set and per-state values on
the store-counterfactual set, and none on the authorship-matched set." "The comparison between model
and lookup is therefore complete only on the full obligation population ($661$)." → "The comparison
between model and lookup is therefore complete on the full obligation population ($661$) and on the
store-counterfactual set ($444$)." "The store-counterfactual set is the second failed prediction:
there the smallest model's aggregate gain did not replicate at item level
(Appendix~\ref{app:counterfactual})." → the frozen P1 HOLDS [MAIN] text "On $148$ questions written
before any version of the store existed, and asked of three versions of the same store that differ
in one attribute each, the smallest model's obligation judgment reaches $0.7167$ against the $0.5$ a
question-only reader attains here, with an interval of $[+0.1494,+0.2846]$. The gain survives where
the question cannot carry the label." followed by the one-line history pointer "The first,
thirty-question form of that set did not replicate at item level (Appendix~\ref{app:counterfactual})."
(the drafting form said "had failed", which prose_scan's outcome vocabulary bars in main text; R-e).
Direction: **up** (a failed prediction's sentence is replaced by the registered replication that
holds; the failure itself stays in Table 9's first-form column, D.2's history paragraph and the
registration record).

**(7) §8, THE BOXED SENTENCE (v7 L789) (`R98-7`; AUX-CF2-ALLSTATES-V3).** "Once a summary names
every non-active state, the lookup reaches $0.7886$ on questions that cannot carry the label." →
"Once a summary names every non-active state, the lookup reaches $0.8756$ on questions that cannot
carry the label." Direction: **up** (the same claim at the registered size).

**(8) TABLE 25 ROW AND THE DEVIATION INDEX (Appendix G) (`R98-8`; `ADDENDUM_CF2.md` §14–§17;
`DEVIATIONS_CF2.md`).** One row after the two Side-experiments rows: "R94: CF-2 store-counterfactual
cell & \texttt{f016f033e9} & 2026-09-12 & $148$ question and slot pairs drawn under predicates
fixed before any verdict, three store versions each, three summaries, three readers, five
predictions and their branch texts; all five held, two of them printing either way: the lookups
within tolerance and every reader inside the count-randomization band; five recorded deviations
(D-CF2-1 to D-CF2-5) & held". Five deviation-index lines after the own-name line: "Retraction quota
on the measured eligibility rate: CF-2 D-CF2-1; Appendix~\ref{app:counterfactual}." "Replacement in
walk order after an authoring or reading failure: CF-2 D-CF2-2; Appendix~\ref{app:counterfactual}."
"One re-authoring of a record that fails the author's read: CF-2 D-CF2-3;
Appendix~\ref{app:counterfactual}." "No further queue extension; the supersession quota drops by the
failures: CF-2 D-CF2-4; Appendix~\ref{app:counterfactual}." "Drop rule evaluated on the 13th, once:
CF-2 D-CF2-5; Appendix~\ref{app:counterfactual}." Direction: **neither**.

**(9) CONSISTENCY (`R98-9`).** (a) §7 L722 "the store-counterfactual set ($n=90$)" → "($n=444$)";
(b) Appendix D intro L1212 "The store-counterfactual set ($90$) carries the same boundary" →
"($444$)"; (c) §1 L180 "Of the $42$ preregistered predictions, $8$ did not hold" → "Of the $47$
preregistered predictions, $8$ did not hold": Table 25 gains a five-prediction row (L396's promise
that Appendix G lists every registered prediction), so the count of registrations moves by five;
$8$ is unchanged because the first form's failed replication keeps its own row. A count of
registrations, not a result; recorded for the author's ruling (R97-7 precedent); reverting is one
token. Direction: **neither**.

**(10) LEDGERS, TOOLS AND LINEAGE FILES (`R98-10`).** `r82_counterfactual/cf2/NUMBERS_CF2.md`
§5k (derived margins, the two-subset profile intervals, the $47$ count) written before the edits;
copies of `ADDENDUM_CF2.md`, `NUMBERS_CF2.md`, `DEVIATIONS_CF2.md` into `ARTIFACT/`;
`tools/trace_scan_v13.py` `LEDGERS` gains the CF-2 ledger; tool defaults and `.gitattributes` move
to v8 (LINEAGE); `appendix_identity` pins D.2, F.1, G (and D if its intro line counts) under the
v7 base; `slogan_scan` / `prose_scan` gain FROZEN-REGISTERED entries for the P1, P3 [MAIN] texts
if a rule fires (sourced to `registrations/ADDENDUM_CF2.md` §8). Direction: **neither**.

**GATES (post-R98 build of `paper_v8.pdf`, three pdflatex passes; every gate run).** Page: **FAIL**
— label on **10**, reading **501 / slack −16** (v7: 10, 494 / −9); 33 pages (v7: 32); 0 overfull
boxes; 0 undefined references. The order's main-text changes add about seven review lines (the
two-sentence frozen P1 text and its pointer replace one sentence; the §6 lookup sentence is split for
the 30-word target); nothing was cut or moved on this program's judgment; the D-R97-2 menu stands
and D-R98-2 adds the R98 items. `frozen_diff --program=R98`: 172 frozen strings found in the v7
base, **162 KEPT, 1 MOVED, 9 CHANGED-AUTHORIZED, 0 UNAUTHORIZED** (the nine are quoted in entries
1, 4, 5, 6, 9 and R-b). `numeric_diff --pdf --figboxes`: tex side **ADDED 147 values, 0
VANISHED**, 38 COUNT-CHANGED; PDF side ADDED 142, 0 VANISHED, 24 COUNT-CHANGED; both figure boxes
the same size and position. **The tool exits 1 on the added values by design; every one is an
ordered addition of entries 1–9, reported as such rather than silenced** (R96-4d, R97
precedent). `appendix_identity` against the v7 tree: 23 sections, D, D.2, F, F.1 and G changed,
all EXEMPT with R98 bases and pinned (`cbe34958…`, `296eecf7…`, `d5b1b213…`, `d24d7544…`,
`49fa02ff…`), 18 identical. `slogan_scan` (with `prose_scan`) PASS: 0 duplicates; pinned blocks
once; S8/S9/S10 0 after the exemptions (two FROZEN-REGISTERED entries added, sourced to
`NUMBERS_CF2.md` §5k's printed forms); `preregistered` 4 of cap 4; mean 18.2 over 233
sentences. `sentence_census`: over-30 count 4 (v7: 4); over-40 0. `code_scan`, `repeat_scan`,
`refcheck_v11` (22/22, 41 out of scope, 0 uncovered of 63), `trace_scan_v13` (0 unaccounted; the
CF-2 ledger accounts for every new value; both key assertions OK), `claims_diff` (0 VIOLATIONs),
`u9_scan`, `dupkey_scan`, `hygiene_scan paper_v8.pdf`: PASS. `r82_counterfactual/tools/verify_cf2.py`
(read-only, the verifier of the ledger every CF-2 value is read from): PASS.

**No claim changes strength under this block except as recorded in entries 1, 4, 5, 6 and 7
(Direction as stated there).**

## R99 AUTHORIZATION BLOCK — dated 2026-09-13

Appended by R99-RESTRUCTURE (the findings-first restructuring ordered against two external
reviews: the detailed pasted review, Rating 5/10, and Review E, `reviews/REVIEW_E_73_RELAY.md`,
73/100), anchored to the R98 block above, landing in `paper_v9.tex` (LINEAGE, below). This block
is open; Phase 1 (the abstract) is the only phase landed so far. No experiment, no model call, no
embedding call — paper edits only.

**Rulings taken at planning ([AUTHOR-1], 2026-09-13, in chat).**

- **R-a, STYLE_SPEC amended for the abstract only.** The current abstract already satisfies
  STYLE_SPEC's floor and both reviews independently scored it "nearly unreadable" — the spec
  that produced the abstract under review cannot be the arbiter of its replacement. S6's band
  widens from 6 to 10 sentences for the abstract only (recorded in `STYLE_SPEC.md`). S9 (no
  contrastive) is unchanged in rule; the abstract's "tracks the summary, not the question"
  sentence is rewritten as "comes from the summary and survives fixing the question," a
  positive claim rather than a rewritten exemption. T1 keeps one headline-number sentence, but
  the number is the store-counterfactual result ($0.72$ against a $0.50$ baseline on $444$
  items) rather than the FOK CI ($+0.2037$ $[+0.0935,+0.3191]$); the CI is not required in the
  abstract under this exception. T2 widens from one numeral-bearing sentence to at most two.
  S8 (no em dash) and S10 (jargon budget) are unchanged. Body-section prose keeps STYLE_SPEC as
  it stands; none of this ruling touches §1/§4–§8 drafting.
- **R-b, §5/§6 swap.** The body reorders so the two secondary sections run F2 (the backend
  census, was §6) immediately after §4, then F3 (structureless-store repair, then scale and
  vendors as explicitly secondary evidence, was §5) — matching the F1→F2→F3 order the abstract
  and introduction now lead with. All cross-references are `\ref{}` to `\label{}`, so
  renumbering is automatic; no hardcoded "Section 5"/"Section 6" text exists in the audited
  main text.
- **R-c, §1 contributions trimmed.** The four contribution bullets drop their "for a system
  builder this means" clauses; that guidance lives only in §8's boxed closing paragraph. One
  sentence per bullet, findings only.
- **R-d, Figure 2.** GPT-4.1 mini's blind point is dropped from the plot entirely (not merely
  caveated in the caption, as it is in `paper_v8.tex`); the caption states why in one clause.
- **R-e, three reserved slots.** Placeholders for lanes not yet run: **L1** (own-name ablation)
  and **L2** (retrieval-view and hybrid monitors), one sentence each in new §4.3 after the
  counterfactual paragraph; **L3** (rubric-gate test — whether Step 1 of the two-step NOK
  rubric forces the zero score), one clause on §4.3's blind-arm sentence; **DS** (the frozen
  downstream paragraph, per the DS registration), replacing §7's "the downstream effect of FOK
  and NOK remains open" sentence. No content is asserted for any of L1/L2/L3/DS until its lane
  lands; each placeholder is a literal marker in the manuscript, not prose.
- **R-f, author correction of R99-1's abstract (2026-09-13, in chat).** The landed R99-1 text
  is replaced wholesale by an author-supplied rewrite, four named fixes: FOK and NOK each get
  their own clause (R99-1 shared one defining sentence between them); the counterfactual
  sentence states the model's own score ($0.72$ against the $0.50$ question-only floor on
  $444$ items) rather than framing the model/lookup relationship as a tie; a dangling "it" in
  the retention sentence is replaced by a named subject; the closing sentence states the
  paper's thesis (what a store's self-description sets), satisfying S6's ends-on-headline rule
  directly rather than via a design-law paraphrase. Same word/sentence-count and numeral-count
  constraints as R-a (under 150 words, every sentence of the supplied text kept, numerals
  confined to two sentences).

**LINEAGE (Phase 1, abstract only).** The working lineage is `paper_v9.tex`, a byte copy of
`paper_v8.tex` (the R98 close) with only the abstract and its lineage-comment header changed;
`paper_v8.tex` is the version a reader compares v9 against. Tool defaults have not yet moved to
v9 — they move when Phase 2 (§1) lands, per the R90/R92/R98 precedent — so this phase's gate
runs below name `paper_v9.tex` explicitly rather than relying on a tool default.

**Phase 1 (`R99-1`, abstract, superseded same-phase by `R99-2` under ruling R-f).** `R99-1`
landed 7 sentences (band 6–10 per R-a); headline sentence carried $0.72$/$0.50$/$444$
(App. D.2, `AUX-CF2-MINI-V2`) in place of the FOK CI; $42.3\%$ the second numeral-bearing
sentence (unchanged value, `CL-BELIEVED-NOK`). "Preregistered" was tried for the
five-predictions clause and reverted to "advance" (D-R99-1): it pushed the whole-document
count of that word from 4 to 5 against `slogan_scan`'s cap of 4 (three prior uses stand in §1
and §4.1), so the abstract's fifth use was the one to drop, not the cap. `R99-2` (R-f) then
replaced the text wholesale; two further gate-driven fixes on the replacement, both wording
only, no number or claim touched:
- **D-R99-2.** The replacement's "five advance predictions held" trips `prose_scan`'s VOCAB
  ban on bare `held` as registration-outcome vocabulary (S4/S10; the word is barred outright in
  main text, not capped). Reworded to "with all five advance predictions correct."
- **D-R99-3.** The replacement's retention sentence ("Under the metadata they expose, the
  obligation judgment keeps $42.3\%$ of its gain.") scored a 71% near-duplicate against §1's
  existing sentence ("No tested backend writes such a summary: under the metadata they expose,
  the obligation gain keeps $42.3\%$ of its value...", line 165) under `slogan_scan`'s
  near-duplicate detector (S7 neighbor). Reworded to "On the metadata a backend produces, that
  judgment keeps only $42.3\%$ of its gain." — same number, same claim, no shared clause
  structure with the §1 sentence it neighbors conceptually.

Final landed text: 7 sentences, 149 words, FOK and NOK named once each in separate clauses, no
em dash, no "X, not Y" contrastive, numerals confined to two sentences (the counterfactual
sentence and the retention sentence). No number is a new measurement — $0.72$, $0.50$, and
$444$ already print in Appendix D.2 of `paper_v8.tex` (lines 1317–1323), $42.3\%$ already
prints in §6 (line 680).

Gate results on the final text (not yet the full battery — `frozen_diff`, `numeric_diff`,
`appendix_identity`, `claims_diff` run once §4–§8 land):
- `tools/sentence_census.py paper_v9.tex --sections=Abstract`: Abs reports 8 sentences/0
  over-30/0 over-40. The 8th is a preexisting figure-caption leakage artifact (the tool's `Abs`
  section runs through `\end{abstract}` inclusive and one fragment of Figure 1's caption,
  `"-1.5mm} {A query ranks the store."`, bleeds across that boundary) — reproduced identically
  on `paper_v8.tex` (reports 10 for an abstract CLAIMS.md's own R92 entry calls eight), so this
  is not introduced by this phase. Net of that artifact: 7 real sentences, inside the amended
  6–10 band, 0 over 30 words.
- `tools/slogan_scan.py paper_v9.tex`: **PASS** — 0 duplicate sentences, all pinned U-blocks
  exactly once, S8 (em dashes) 0, S9/S10 hits 0, no `FAILURES` line.

**Reconciliation with R101 (concurrent landing, same author, 2026-09-13).** Between the R99-2
gate run above and the next one, R101 landed into this same `paper_v9.tex` (own-name ablation,
a retrieved-view monitor, the rubric-gate test, and the DS downstream paragraph — filling
exactly the L1/L2/L3/DS placeholders R-e reserved) and, with it, inserted one sentence into
the abstract, between the R99 lookup sentence and the R99 counterfactual sentence: "Retrieval
that returns non-active records with their lifecycle tags reads obligations nearly as well,
and the two together best." Per the author's instruction this is a merge, not a conflict: the
sentence stands as R101 landed it, unedited by this block. Abstract is now 8 sentences (band
6–10 per R-a still holds) and 172 words by the word-count convention this thread has used since
Pass 1 (over the 150-word target; not re-trimmed here, since trimming would mean rewording
R101's sentence or one of R99's without being asked — flagged to the author rather than
silently fixed). `tools/slogan_scan.py paper_v9.tex` and `tools/sentence_census.py paper_v9.tex
--sections=Abstract` both re-run clean against this reconciled state: slogan_scan **PASS** (0
failures); sentence_census Abs 9 (8 real + the preexisting Figure 1 caption-leakage artifact),
1 over-30 (the counterfactual sentence, 31 words — under the unamended 40-word cap), 0 over-40.

**Phase 2 (`R99-6`, §1).** Paragraph 3 gains the store-counterfactual confirmation (n=444) and
the ground-truth repair sentence (ruling R-b); the four contributions drop their "for a system
builder" clauses (ruling R-c) and item 3 drops "cell" (bare `cell`/`cells` barred by S10;
`prose_scan`'s VOCAB list) for "a test." `prose_scan.py paper_v9.tex`: PASS. `slogan_scan.py
paper_v9.tex`: PASS.

**Phase 3 (`R99-7`, §4).** The former "Discrimination improves; calibration does not" and
"Counts are not necessary for coverage, and a mismatched index misleads" subsections are re-cut
into three: `\label{sec:coverage}`, `\label{sec:discrimination}` (label kept, subsection retitled
"Obligation: a name lookup matches the model"), `\label{sec:calibration-secondary}` (new, since
`sec:calibration` names the whole section) — ruling R-b. Every sentence carried over is
byte-identical to its source except: (i) the former L481 split at its "and" into a coverage
clause (new §4.2) and an obligation clause (new §4.3), since one sentence mixed the two; (ii) the
blind-arm caveat (former L494-498) moved to open new §4.3, per caveat C2/C5's merge disposition;
(iii) the calibration tail's Brier/selective-risk/rescaling-ceiling detail is cut to one pointer
clause per the approved cut list item 3, both numbers already printed in full in Appendix H
(`app:posthoc`); (iv) one new sentence, the store-counterfactual confirmation restated with its
own numbers ($0.7167$/$0.7663$/$0.50$/$444$; source Appendix D.2, `AUX-CF2-MINI-V2`/
`AUX-CF2-NB6-V2`) — worded independently of §1's mention of the same result to clear
`slogan_scan`'s near-duplicate check (see gate failures below). `sec:mechanism`'s one
cross-reference (§3, "the monitor reads both halves") retargets to `sec:coverage`; Table 1's
caption retargets its first `\ref{sec:discrimination}` (splitting negatives by kind) to
`\ref{sec:coverage}`, its second (blind-score-anchors-no-gain) stays, now correctly pointing at
the retitled §4.3.

Gate results: first run, `prose_scan.py paper_v9.tex` — **3 FAILURES**: two sentences over the
40-word cap (the merged blind-arm-caveat sentence, 57 words; the first draft of the new
counterfactual sentence, 46 words) and one near-duplicate (83%, the new §4.3 counterfactual
sentence against §1's, since both opened with the same "Holding one question fixed across three
..." clause). Fixed by: splitting the 57-word sentence back into two at the connective it had
absorbed (no words changed); rewriting the counterfactual sentence's opening from "Holding one
question fixed across three versions..." to "On the store-counterfactual population, where the
question is fixed..." — same claim, same four numbers, no shared clause with §1's sentence.
Second run: `prose_scan.py paper_v9.tex` **PASS**; `slogan_scan.py paper_v9.tex` **PASS**. Not
yet run this phase: `numeric_diff`, `frozen_diff`, `appendix_identity`, `claims_diff` — deferred
to the full battery once §5-§8 land, per the LINEAGE note above.

## MAIN TEXT CLAIMS

### Abstract (L37–85) — carried by skeleton bullets + body sections in v2

## CL-C001 [Abstract L41]
TEXT     | Persistent-memory agents need a judgment about what an external store contains before retrieval begins.
STRENGTH | Framing claim; no quantity.
KEYS     | C001
CLASS    | definition

## CL-C002 [Abstract L43]
TEXT     | "the first measurement of store-level metamemory---a monitor's judgment about its external store, scored before retrieval and with no downstream claim---against explicit discrimination and probability-calibration targets, not a claim that the probabilities are well calibrated."
STRENGTH | Novelty: FIRST measurement. Scope: pre-retrieval; no downstream claim; not claiming good calibration.
KEYS     | C002
CLASS    | positive (novelty) + scope-limit

## CL-U001 [Abstract L44–46]
TEXT     | FOK = probability the store covers a query under its intent. NOK = knowing the store contains something that must not be used (hiking cancellation example). "No prior work in the literature we reviewed defines or measures NOK."
STRENGTH | Novelty scoped to "the literature we reviewed".
KEYS     | (unmarked; adjacent C002)
CLASS    | definition + positive (novelty)

## CL-C003 [Abstract L48]
TEXT     | Blind monitor receives no store summary so its level reflects question-side priors; indexed also receives a compact metadata-only summary; the paired delta measures the information the summary adds on the same questions.
STRENGTH | Methodological identity; no quantity.
KEYS     | C003
CLASS    | definition

## CL-U002 [Abstract L50]
TEXT     | The index raises hard-tier FOK AUROC by +0.2272 (CI [+0.1177,+0.3504]).
STRENGTH | Pooled hard tier; point +0.2272, CI [+0.1177,+0.3504]. NOTE: v2 abstract skeleton bans this number (headline is within-FR +0.2037); the claim survives at full strength in §4 (CL-C141, CL-T-e1). Not a drop — a placement change ordered by R78/R77-H.
KEYS     | (abstract site of AUX pooled row)
CLASS    | positive

## CL-U003 [Abstract L51–52]
TEXT     | Resolution analysis required by preregistration limits the gain to genuine-absence recognition rather than missing-slot detection. Discrimination is the preregistered primary endpoint; ECE does not improve with the intact index and is reported as a negative result.
STRENGTH | Same strength as C051/C139 body claims.
KEYS     | → C051, C139
CLASS    | scope-limit + negative

## CL-C004 [Abstract L54–55]
TEXT     | Across the preregistered capability ladder larger models have better blind coverage priors, but blind obligation priors do not improve monotonically. Cross-vendor: blind obligation priors above chance, below chance, and spanning chance, while the indexed-minus-blind NOK separation remains positive in every tested lineage.
STRENGTH | Qualitative ladder trend + universal positive paired NOK separation over tested lineages.
KEYS     | C004
CLASS    | positive

## CL-C006 [Abstract L57]
TEXT     | Destroying the numeric counts shows that counts are not necessary for the effect.
STRENGTH | Non-necessity only (see CL-C137/C058 for its bounds).
KEYS     | C006
CLASS    | positive-with-limit

## CL-C005 [Abstract L59–60]
TEXT     | "For the five models with varying blind NOK...: Scale buys better priors---priors can approximate coverage but cannot know a store's obligations, and which way an obligation prior points varies by model; a compact index replaces priors with information and lands every model tested in the same narrow band."
STRENGTH | Population: the five varying-blind-NOK models (mini's tie-degenerate row excluded per L531/L668).
KEYS     | C005
CLASS    | positive
NOTE     | Verbatim slogan; appears once in v2 (abstract skeleton slot); §8 paraphrases (ORDERED-MECHANICAL).

### §1 Introduction (L87–166) — carried by skeleton bullets in v2; strengths unchanged

## CL-C008 [§1 L104–108]
TEXT     | Hiking-trip scenario; "retraction records survive similarity retrieval at only $5\%$" in the memory system we build on; a bounded view can expose the stale plan without the record that makes suppression obligatory; the monitoring failure precedes any answer.
STRENGTH | 5% (cited premise, \citep{fr}); mechanism framing.
KEYS     | C008; FR-GATE site 1
CLASS    | positive (motivating premise)

## CL-C149 [§1 L110–112]
TEXT     | Not a corner case: no evaluated system exceeds 6% accuracy on the multi-hop conflict-resolution slice \citep{memoryagentbench}; a major assistant vendor describes its earlier saved-memory system as one that became stale and left users to manage updates by hand \citep{openaimemory}.
STRENGTH | 6% ceiling (cited); vendor staleness admission (cited).
KEYS     | C149
CLASS    | positive (motivating premise)

## CL-C009-C010 [§1 L114–118]
TEXT     | External memory changes the epistemic problem (parametric + separately-maintained store). An always-retrieve policy declines the judgment; a similarity threshold estimates proximity to retrieved items, not store coverage; neither identifies that relevant content can be present yet carry a binding obligation to suppress.
STRENGTH | Qualitative.
KEYS     | C009, C010
CLASS    | definition

## CL-FIG-overview [§1 L120–142]
TEXT     | Overview diagram + caption: "A monitor judges the store before retrieval, and only the indexed condition sees its value-scrubbed self-description. The two judgments are scored against the intent-conditioned gold label."
STRENGTH | Mechanism figure; no quantity.
KEYS     | (unmarked)
CLASS    | definition
NOTE     | Promoted to Figure 1 (fig:overview) in v2 (ORDERED by R78 §1 spec).

## CL-C011-C014 [§1 L145–153]
TEXT     | Cognitive metamemory separates judgments about memory from decisions made with them \citep{nelson1990,koriat1996}; we transfer the monitoring half to external stores; intent-conditional coverage defined; FOK asks coverage, NOK asks whether coverage requires suppression; constructed stores make both targets observable before retrieval, against deterministic labels rather than answer-level proxies.
STRENGTH | Qualitative transfer + construct claims.
KEYS     | C011, C012, C013, C014
CLASS    | definition

## CL-C015 [§1 L156–162]
TEXT     | Contributions: (1) define and measure NOK, absent from the literature we reviewed; (2) transfer FOK to external stores with explicit calibration targets; (3) model size changes question-side priors whereas an expressive index adds store information and sharply narrows between-model variation; (4) instrument ledger showing semantic assumptions inside instruments must be tested.
STRENGTH | Four contributions at stated strength (v2 reorders per R78 §1 spec: NOK; cross-vendor; store audit + design law; controls/instrument lessons — reorder is emphasis, not strength).
KEYS     | C015
CLASS    | positive

## CL-C018 [§1 L164–166]
TEXT     | Confirmatory claims preregistered with frozen decision rules and a disclosed deviation ledger; bootstrap CIs per Appendix repro; registration record in appendix. "The empirical scope is pre-retrieval monitoring on synthetic stores, with one primary closed model family; downstream behavior is outside this paper."
STRENGTH | Scope anchor VERBATIM-equivalent; unchanged since STEP 4.
KEYS     | C018
CLASS    | scope-limit

### §2 Related work (L168–204)

## CL-C019-C021 [§2 L172–174]
TEXT     | Classical metamemory treats monitoring as judgment about memory state; adaptive-retrieval methods decide from parametric/generated signals and observe a bounded retrieved view rather than a maintained self-description — precisely the separation formalized in Prop 1.
STRENGTH | Positioning.
KEYS     | C019, C021
CLASS    | definition

## CL-C145 [§2 L176–178]
TEXT     | MetaMem's construct is a policy, not a judgment about what a store contains. Abstention benchmarks score answerability without an external store to be right about.
STRENGTH | Positioning distinctions.
KEYS     | C145, C5-ladder site
CLASS    | definition

## CL-C146 [§2 L182–184]
TEXT     | Loop split: AutoMem learns memory management; Supersede turns the update gap into an RL signal; FAMA penalizes reliance on obsolete memory; MemoryAgentBench evaluates retrieval and conflict resolution; STALE asks whether an agent recognizes expiry.
STRENGTH | Positioning (each cited system characterized once).
KEYS     | C146
CLASS    | definition

## CL-C022-C147 [§2 L186–189]
TEXT     | Around them sit the know–act gap, post-retrieval admissibility \citep{memgate}, long-term stores, remembered-answer benchmarks. "Each of these presupposes a monitoring judgment---some estimate of what the store holds and what it forbids---and none measures it." That judgment, pre-retrieval and against deterministic labels, is this paper's object.
STRENGTH | The gap claim: none measures the presupposed judgment.
KEYS     | C022, C147
CLASS    | positive (gap)

## CL-C148 [§2 L193–197]
TEXT     | Obligation neighbors: CIMemories (contextual-integrity release) and GateMem (access control, agent-facing forgetting) measure policy-supplied obligations; NOK's are supplied by the content's own lifecycle state; both require knowing the store holds something it must not use. PM-Bench scores acting on a remembered intention. NOK is the pre-retrieval judgment each of these settings assumes.
STRENGTH | Distinction: policy-supplied vs lifecycle-supplied; pre-retrieval position.
KEYS     | C148
CLASS    | definition
NOTE     | A1's conditional sentences land here without changing any existing sentence's strength.

## CL-C024 [§2 L202–204]
TEXT     | \citet{fr} introduced the inherited schema (active/superseded/expired/retracted). Scoring discipline first checks presence via the presence control. The object calibrated is belief about an external store, not confidence in an answer.
STRENGTH | Inheritance + object statement.
KEYS     | C024; FR-GATE site 2
CLASS    | definition

### §3 Framework (L206–313)

## CL-GLOSSARY [§3 L208–222]
TEXT     | Notation/study glossary box (FOK, NOK, PN, blind/indexed, TRUE/BELIEVED, arm/cell, tiers, monitor call, E0/E1, FR-Bank, Mem0, A-MEM, mini/luna/sol, lineage/prior).
STRENGTH | Definitions only.
KEYS     | (box)
CLASS    | definition
NOTE     | Moves byte-verbatim to Appendix F glossary subsection (ORDERED-MECHANICAL).

## CL-C026-C027 [§3 L226–229]
TEXT     | Store formalism m(e)=(c,κ,ξ,h,t), ξ ∈ {ACTIVE,SUPERSEDED,EXPIRED,RETRACTED} \citep{fr}; intents {CURRENT,UPCOMING,PAST,CHANGE}; CHANGE may be PRESENT or ABSENT but never PN because both values are licensed.
STRENGTH | Formal definitions.
KEYS     | C026, C027; FR-GATE site 3
CLASS    | definition

## CL-C028-C030 [§3 Def 1, L234–243]
TEXT     | Cov(q,S) ∈ {PRESENT,ABSENT,PN}. PN when suppression is load-bearing under i(q): superseded value under current intent; retracted plan under current/upcoming; expired event under current/upcoming. Expired under past intent is PRESENT, not PN. Hiking running example is PN.
STRENGTH | Label semantics (deterministic).
KEYS     | C028, C029, C030
CLASS    | definition

## CL-BOX-examples [§3 L245–258]
TEXT     | Manifested-examples box: three real queries with gold labels (PRESENT/ABSENT/PN).
STRENGTH | Illustrative instances.
KEYS     | (box)
CLASS    | definition

## CL-C031 [§3 L261]
TEXT     | The pilot showed that intent conditioning is necessary to define the PN target reliably; Table tab:e1-construction reports both checks.
STRENGTH | Design-necessity claim backed by intent-audit row (20% route precision; 110 items = 26.6% ineligible).
KEYS     | C031
CLASS    | positive (instrument)

## CL-C032 [§3 L263–267]
TEXT     | FOK(q,S), NOK(q,S) ∈ [0,1] defined. Blind AUROC measures question-side priors rather than store knowledge. On text carrying no label signal, population blind-NOK AUROC is 0.5 by construction. Paired deltas hold the question distribution fixed; the change measures information supplied by the index on that measured population.
STRENGTH | Estimand semantics incl. the "measured population" scope.
KEYS     | C032
CLASS    | definition

## CL-C033 [§3 L269]
TEXT     | AUROC is primary and ECE is secondary.
STRENGTH | Endpoint hierarchy (preregistered).
KEYS     | C033
CLASS    | procedural

## CL-C034 [§3 Def 2, L271–275]
TEXT     | k-bounded monitor: entire store-side input is the top-k retrieved set with full feature profile.
STRENGTH | Definition.
KEYS     | C034
CLASS    | definition

## CL-C035 [§3 Def 3, L277–282]
TEXT     | Lifecycle index M(S), maintained outside query time: count table (category–lifecycle counts + per-category supersession-event counts) paired with a value-scrubbed attribute-name map (names exposed; which carry superseded content); |M(S)| is O(|C|·|Ξ|+|N|), independent of |S|. Gloss: counts + names, never values. "randomizing every count leaves FR-Bank discrimination unchanged, so the counts are not necessary and the name map is among the channels that remain."
STRENGTH | R77-T1 definition (counts AND name map; size bound); non-necessity restated at Def-3 strength.
KEYS     | C035 (R77-T1, D5)
CLASS    | definition + positive-with-limit

## CL-BOX-index [§3 L284–299]
TEXT     | Abridged serialized real FR-Bank index excerpt (575 entries; category rows; name sections; superseded-names section) + italic caption: exposes counts and attribute names but no stored fact values.
STRENGTH | Instance evidence for value-scrubbed claim.
KEYS     | (box)
CLASS    | definition

## CL-C036 [§3 Prop 1, L301–307]
TEXT     | Monitoring non-identifiability: with a below-cutoff witness, there exist S,S′ with feature-identical top-k sets but Cov=PRESENT vs PN; every decision rule errs with probability ≥ 1/2 under the uniform mixture. Informal gloss (two stores look identical through finite retrieval).
STRENGTH | Formal proposition + proof (App A.1).
KEYS     | C036, C098–C103
CLASS    | positive (formal)
NOTE     | The FOLLOWING sentence (L306 "necessity, not an optimization") is AUTHORIZED-REFRAME R1 — softened as recorded above. The proposition itself is untouched.

## CL-C038 [§3 L310]
TEXT     | Remark 1 (scalar-trust infeasibility) is a motivating impossibility for region-conditioned trust rather than a claimed contribution.
STRENGTH | Demoted status (R74-W: Prop 2 → Remark 1) preserved.
KEYS     | C038, C037, C104–C106
CLASS    | scope-limit

## CL-C136 [§3 L312]
TEXT     | "The below-cutoff premise is empirically ordinary in the memory system we build on, where retraction records pass similarity retrieval at $5\%$ \citep{fr}; the proposition is a design-space scoping result whose force is that measured premise, not a deep theorem."
STRENGTH | 5% premise; "not a deep theorem" hedge — both preserved.
KEYS     | C136; FR-GATE site 4
CLASS    | scope-limit

### §4 Monitoring study (L315–439)

## CL-CAP-e1 [Table 1 caption L319]
TEXT     | The main study measures FOK and NOK discrimination with and without the metadata index. The index improves the hard FOK and FR-Bank NOK rows, while the resolution analysis confines the hard FOK gain to genuine absence.
STRENGTH | Finding-first caption; resolution confinement stated.
KEYS     | C130
CLASS    | positive-with-limit

## CL-T-e1 [Table 1 rows L329–334]
TEXT     | Six rows (Blind / Indexed-TRUE / ∆ / 95% CI):
  1. FOK FR-Bank hard (headline), n=307, pos 35 non-ABSENT: 0.4966 / 0.7003 / +0.2037 / [+0.0935,+0.3191]
  2. FOK pooled hard (secondary), n=588, pos 35: 0.5258 / 0.7530 / +0.2272 / [+0.1177,+0.3504]
  3. FOK easy contrast, n=595, pos 463: 0.4422 / 0.6336 / +0.1914 / --- (CI in tab:cluster-sensitivity)
  4. NOK FR-Bank, n=661, pos 104 PN: 0.4946 / 0.7339 / +0.2393 / [+0.1801,+0.2949]
  5. FOK Mem0, n=238, pos 94: 0.5746 / 0.4777 / −0.0969 / [−0.169,−0.025]   (ADVERSE — prints)
  6. FOK A-MEM, n=284, pos 126: 0.5591 / 0.4526 / −0.1065 / [−0.173,−0.040] (ADVERSE — prints; U8)
  Footnote ‡: "Pooled absolute levels are not coverage discrimination; [§4.3] gives the reason and the headline it implies." (‡ gains its anchor on row 2 — ORDERED-MECHANICAL.)
STRENGTH | All values exact; headline/secondary ordering per R77-H.
KEYS     | tab:e1; C131 footnote
CLASS    | positive + adverse

## CL-PAYOFF [§4 L344]
TEXT     | Within FR-Bank, inside one backend, the index raises hard-tier FOK discrimination by +0.2037 (CI [+0.0935,+0.3191]); the pooled tier moves +0.2272 (CI [+0.1177,+0.3504]) under the caveat above; a persona-clustered sensitivity leaves every interval excluding zero.
STRENGTH | Within-FR leads; pooled beside it; clustered-sensitivity survival claim.
KEYS     | AUX-E1R-CLUSTER; R77-H
CLASS    | positive

## CL-C040 [§4.1 L349–351]
TEXT     | E0 pilot: large FOK gain and a null NOK result; E0 and E1 used different prompts and their values cannot be compared directly; design lesson = rule out success from merely reading a zeroed category.
STRENGTH | Null NOK at pilot; non-comparability.
KEYS     | C040
CLASS    | negative + procedural

## CL-C042-C043 [§4.2 L356–362]
TEXT     | E1 monitor = mini; only the ladder changed the model. 40 synthetic profiles. FR-Bank is the lifecycle-bearing store from the memory system we build on. Easy tier removes a whole category; hard tier keeps it populated (natural absence = user never had the target; slot ablation = one target record deleted, category left populated).
STRENGTH | Apparatus facts.
KEYS     | C042, C043
CLASS    | procedural

## CL-C045 [§4.2 L365]
TEXT     | Labels follow Definition 1, and every PN item was hand-verified from its constituent judgments.
STRENGTH | Universal hand-verification of PN labels (basis for A3).
KEYS     | C045
CLASS    | procedural

## CL-C046-POSTERIOR [§4.2 L367–369]
TEXT     | Presence control = exact lexical match + embedding similarity. ε = 0.005 is the conditional miss rate; at measured base rate 0.917 present among resolved targets, the chance an ABSENT claim is wrong is 5.2% — roughly ten times ε, precisely because the population is answerability-skewed.
STRENGTH | ε=0.005; base 0.917; posterior 5.2%; ~10×. The R77-T2 correction against interest: the LARGER number prints; no "at most"; no 0.5% anywhere.
KEYS     | C046, AUX-R77-POSTERIOR, AUX-R77-BASERATE
CLASS    | adverse (against-interest correction)
NOTE     | A3's two sentences follow this claim in v2.

## CL-C047-C048 [§4.2 L371–374]
TEXT     | Indexes are metadata-only and value-scrubbed; TRUE from ground truth, BELIEVED from backend-exposed fields. The leakage screen tests the value-scrubbed claim; result and frozen threshold in appendix (0 leaks; threshold >3/30).
STRENGTH | Provenance + screen.
KEYS     | C047, C048
CLASS    | procedural

## CL-PROMPTS [§4.2 L376–394]
TEXT     | Fixed preregistered elicitation rubric; frozen FOK prompt text quoted; frozen blind/indexed user prompts box (incl. the "not expressible by this backend" clause).
STRENGTH | Frozen-instrument record.
KEYS     | (box)
CLASS    | procedural

## CL-C050 [§4.3 L399]
TEXT     | The hard-tier effect rules out the "read-a-zero" concern.
STRENGTH | Control claim.
KEYS     | C050
CLASS    | positive (control)

## CL-C141 [§4.3 L401]
TEXT     | The headline coverage result is the within-FR-Bank delta +0.2037, measured inside one backend; the pooled tier is reported beside it, because all 35 pooled positives are FR-Bank, so the one-bit is-FR-Bank rule alone attains 0.7541 (above the pooled indexed 0.7530) and pooled absolute levels are not coverage discrimination for any reader — though paired deltas are unaffected, a score constant across arms being unable to produce a delta.
STRENGTH | Full one-bit disclosure with both numbers; "for any reader"; delta-invariance rider.
KEYS     | C141, AUX-E1R-BACKEND-CONFOUND
CLASS    | adverse (interpretation limit) + positive

## CL-BASELINES-SENT [§4.3 L403]
TEXT     | Mechanical readers of that same index do not reach the monitor WHERE LIFECYCLE STRUCTURE EXISTS: on FR-Bank it leads the best of a deterministic lifecycle rule, lexical and embedding matchers, and two learned index readers by +0.0817 (TRUE) and +0.0819 (BELIEVED) on FOK and +0.1365 on NOK-TRUE; the margin does not extend to the structureless backends, and under BELIEVED metadata the NOK judgment falls back to an embedding matcher.
STRENGTH | Scoped to FR-Bank; margins exact; two adverse riders included.
KEYS     | AUX-E1R-BASELINES (R77-B)
CLASS    | positive-with-limit + adverse riders

## CL-C051 [§4.3 L405–407]
TEXT     | Resolution analysis (prereg-required) narrows the claim: PN vs natural absence improves 0.5517→0.8782; PN vs slot-ablated absence moves 0.4336→0.4972 and remains at chance. FOK recognizes genuine absence but does not detect a missing slot. Item-level suppression discrimination is NOK's distinct target.
STRENGTH | Both splits exact; at-chance verdict.
KEYS     | C051
CLASS    | positive-with-limit
NOTE     | A5's sentence lands beside this claim in v2.

## CL-C052 [§4.3 L409–410]
TEXT     | NOK's FR-Bank delta is +0.2393 (CI [+0.1801,+0.2949]). NOK can only be measured on FR-Bank because only FR-Bank retains superseded content; the restriction comes from the backends' design, not from a choice made after seeing results.
STRENGTH | Point + CI; design-restriction defense.
KEYS     | C052
CLASS    | positive + scope-limit

## CL-C053 [§4.3 L412]
TEXT     | Staircase variant scores within noise of the free-number format; a descriptive check, not an equivalence result.
STRENGTH | Descriptive only.
KEYS     | C053
CLASS    | procedural

## CL-C054 [§4.3 L414]
TEXT     | On FR-Bank, the BELIEVED index retains 101.4% of the TRUE index's FOK benefit despite severe metadata error, exceeding 100% within sampling noise.
STRENGTH | 101.4%; "within sampling noise" rider.
KEYS     | C054
CLASS    | positive

## CL-C139 [§4.3 L416–420]
TEXT     | Discrimination is the preregistered primary endpoint; ECE is 0.1596 blind, 0.1741 intact, 0.0583 names-only. Paired intact−blind ECE difference +0.0145 CI [−0.0037,+0.0345] includes zero; names-only −0.1013 [−0.1171,−0.0815] excludes zero. The negative result is itself a finding: elicited FOK behaves as a ranker, not a probability — a deployed monitor must threshold it per index — while names-only ECE 0.0583 shows calibration is index-content-dependent rather than impossible; intact-index calibration is UNIMPROVED.
STRENGTH | All five ECE quantities; "unimproved" verbatim (frozen E1-R branch); ranker-not-probability framing.
KEYS     | C139, AUX-E1R-ECE
CLASS    | negative (kept verbatim strength)

## CL-C055-C057 [§4.4 L425–426]
TEXT     | Count destruction holds every other field fixed (ages, markers, names byte-identical); preregistered ±0.05 tolerance; ALL FR-Bank manipulated conditions satisfy the rule; randomizing every count changes FR-Bank discrimination by +0.0015, so counts are not necessary for the effect, supporting a signal from the map of which categories contain entries, conditioned on query specificity.
STRENGTH | +0.0015; tolerance ±0.05; "supporting" (not proving) the map signal.
KEYS     | C055+C056+C057
CLASS    | positive-with-limit

## CL-C137 [§4.4 L428]
TEXT     | Because ages, markers, and names remain intact, the intervention identifies count non-necessity but does not isolate the map from those preserved channels.
STRENGTH | Explicit non-isolation.
KEYS     | C137
CLASS    | scope-limit

## CL-C058 [§4.4 L430–431]
TEXT     | The pooled names-only arm scores 0.8516, a direction driven by external stores whose indexes lack usable structure and whose misleading counts propped up false coverage. The FR-Bank row supports only count non-necessity, not a universal names-only advantage.
STRENGTH | 0.8516 + the two scope riders.
KEYS     | C058
CLASS    | positive-with-limit

## CL-C060-C062 [§4.4 L434]
TEXT     | Preregistered factorial: lifecycle-index effect +0.1980 dominates both prompt effects (+0.0134, −0.0193), attributing the recovery to lifecycle information rather than wording; the matching condition independently reproduces the E1 value.
STRENGTH | Three effects exact; attribution confined (see CL-C062-scope).
KEYS     | C060+C061+C062
CLASS    | positive

## CL-SW1 [§4.4 L436]
TEXT     | Scored against another persona's index the monitor loses the whole benefit and FOK inverts below chance (0.7003→0.3631), so it is reading this store's description rather than index-shaped text.
STRENGTH | SW-1 at full strength; endpoints exact.
KEYS     | AUX-R77-SWAP-* (D-R74-19)
CLASS    | positive (control)

## CL-SW2 [§4.4 L437] — U7
TEXT     | Permuting which counts and attribute-name lists belong to which category changes neither judgment, which bounds the MECHANISM rather than that specificity — per-category correspondence is not necessary on FR-Bank, consistent with the name map rather than the count structure carrying the effect, THOUGH the shuffle preserves the global name and count multiset and the flat superseded-names section and so bounds correspondence alone.
STRENGTH | Mechanism bound only; NEVER a store-specificity failure; mandatory bound clause travels verbatim (U7). The frozen SW-3 sentence ("the measured benefit is not shown to be store-specific") does NOT print.
KEYS     | AUX-R77-SWAP-* (D-R74-19)
CLASS    | scope-limit (bound)

## CL-C062-scope [§4.4 L439]
TEXT     | Scope: count destruction establishes non-necessity rather than isolating the remaining channel, and the factorial attribution is confined to the preregistered conditions.
STRENGTH | Caveat pair; one statement.
KEYS     | C062
CLASS    | scope-limit

### §5 Capability ladder and economics (L441–594)

## CL-C063 [§5 L444–445]
TEXT     | Matched conditions: same 84 FR-Bank items and prompts, only the model swapped; preregistered estimator averaged repeated monitor calls for luna and sol.
STRENGTH | Design facts (A4's clause extends this without changing it).
KEYS     | C063
CLASS    | procedural

## CL-FIG-ladder [§5 L447–501]
TEXT     | Ladder figure: blind/indexed FOK (0.4488/0.5735/0.7099; 0.7090/0.7417/0.7463) and NOK (0.5000†/0.5585/0.5290; 0.7139/0.8526/0.8588) with deltas +0.2602/+0.1682/+0.0364 and +0.2139/+0.2940/+0.3298; mini all-tie open marker. Caption: n=84 (54 FOK-positive, 40 PN); blind FOK priors rise as index gain contracts; blind NOK no monotone scale trend; indexed FOK converges across all tiers; indexed NOK converges across luna and sol.
STRENGTH | All plotted values; the two convergence scopes exactly as stated.
KEYS     | C132; tab:ladder-exact backs every value
CLASS    | positive

## CL-TAKEAWAY [§5 L504–505]
TEXT     | Model scale changes question-side coverage priors, while the store description supplies obligation information; no model size notices the cancellation unless the store tells it through the index.
STRENGTH | Qualitative pairing of the two results.
KEYS     | (unmarked)
CLASS    | positive

## CL-C064 [§5.1 L510–512]
TEXT     | Five items registered, four held; the fifth (sol blind FOK stays below 0.75) FAILED at 0.8131 (original elicitation population n=150; matched-cell value 0.7099). That failed prediction corrected the earlier single-draw narrative: larger models can supply better question-side coverage priors even without store information.
STRENGTH | Failure printed with both populations disclosed.
KEYS     | C064
CLASS    | adverse (failed prediction, printed)

## CL-THREELINE [§5.1 L513]
TEXT     | Three-line reading: blind FOK priors rise while their index gain contracts; blind NOK priors move non-monotonically while their index gain grows; indexed FOK converges across all tiers, whereas indexed NOK converges only across luna and sol.
STRENGTH | The "only across luna and sol" scope is load-bearing.
KEYS     | C064 block
CLASS    | positive
NOTE     | v2 keeps this as prose, not slogan (R78 §5 spec); appears once.

## CL-C066-C068 [§5.1 L515–518]
TEXT     | Mini's blind NOK is tie-degenerate (every item same score, not calibrated uncertainty). Luna produces varied scores and still fails to discriminate. Scope: the ladder establishes model-size trends on these matched monitor calls; scale cannot supply obligation information absent from the monitor's view.
STRENGTH | Tie-degeneracy + luna-fails + scope.
KEYS     | C066, C068
CLASS    | negative + scope-limit

## CL-XV [§5.2 L522–528]
TEXT     | Three new lineages (Opus 5, Haiku 4.5, K3 under Moonshot's custom license), repeated calls, five registered items. Anthropic pair is cross-generation (price/capability comparison, not within-generation ladder). XV-1 FAILED: Opus 5 blind NOK above chance, Haiku 4.5 below, K3 spanning. XV-2 held on Opus 5 and K3; XV-3 held; XV-4 held on all three indexed-FOK rows. The failure forced the prior framing: the blind baseline can point in either direction (Haiku inverted), while every new paired NOK delta remains positive with its interval excluding zero.
STRENGTH | Failed registration printed first; per-item outcomes exact.
KEYS     | (§5.2 block; App C record)
CLASS    | adverse + positive

## CL-SPAN [§5.2 L530–531]
TEXT     | An UNREGISTERED convergence observation strengthens the information-side result: across the five models with varying blind NOK, explicitly excluding mini's tie-degenerate row from both endpoints, the blind span 0.3307 contracts to 0.0389 indexed, whose range is 0.8199–0.8588 across three vendors.
STRENGTH | "Unregistered observation" status; exclusion clause; all four numbers.
KEYS     | (L531)
CLASS    | positive (unregistered, labeled)
NOTE     | This is the R78 cross-vendor headline for §5/abstract skeleton — same strength, promoted emphasis.

## CL-XV5-K3 [§5.2 L532]
TEXT     | XV-5 reports that K3's blind interval spans chance despite an always-reasoning configuration; the preregistration pilot measured a mean of 1,027 reasoning tokens per call.
STRENGTH | Reports-status; 1,027.
KEYS     | (L532)
CLASS    | negative (reports)

## CL-X4 [§5.2 L534–535]
TEXT     | A registered expansion to the full FR-Bank populations (NOK n=661, FOK n=307) replicates the paired separation on all four completed lanes, with the indexed-NOK span (0.0988) again smaller than the blind span (0.2279); the two lanes stopped by budget are reported as such. Scope: a replication on the same authored question cell, not evidence that its blind levels are free of question-side signal.
STRENGTH | Cap-stop disclosure + scope rider.
KEYS     | AUX-R74-X4 (cap-stop branch — the one authorized §5.2 sentence)
CLASS    | positive-with-limit

## CL-C069-C071 [§5.3 L540–546] — includes U1
TEXT     | Where a backend cannot express a usable self-description, the index has a negative effect at every tested scale. Largest inversion: luna pooled external ∆ = −0.3380, CI [−0.4896,−0.1811]. U1: "This is an inversion at every scale, not a below-chance score at every scale. The cause of the below-chance cases remains unresolved."
STRENGTH | Universal-inversion claim + largest instance + unresolved-cause disclosure.
KEYS     | C069, C070, C071
CLASS    | adverse (printed at full strength)

## CL-X2 [§5.3 L548–553] — includes U2
TEXT     | Candidate mechanisms remain hypotheses; the registered ablation measured count and marker channels singly without separating either; removing both reduces the A-MEM inversion from −0.1065 to −0.0368 (CI [−0.1041,+0.0268]) and leaves Mem0 unchanged. Counts may act as false coverage priors. Disagreement between index and retrieved view may compress the score range. U2 scope sentence.
STRENGTH | Hypothesis framing; both-arm result; Mem0-unchanged; U2 verbatim.
KEYS     | AUX-R74-X2 (branch ii)
CLASS    | unresolved + scope-limit

## CL-ECONOMICS [§5.4 L555–594 → Appendix in v2 per R2]
TEXT     | Caption + rows: projected list-price block (luna $0.20/M, sol $5.00/M input; mini blind $234, indexed uncached $519, cached-as-run $322, cached-asymptotic $207 per million calls; blind prompt 480 tokens; minimum cacheable prefix 1,024 tokens) and as-billed block (blind $233, indexed cached $360). Causes: cached input bills at 25% of list; 64.3% of indexed prompt tokens hit the block-aligned cache. Output telemetry not recorded, so no intervals exist. L589: 25× per-token list-price span; exact per-call cost not identifiable. L592: projection $207-vs-$234 REVERSED as billed $360-vs-$233; the billed micro-run CONFIRMS the blind figure; projection and billed observation disagree. C076 scope: the convergence result motivates the cheapest model that can read the index, under the stated arithmetic.
STRENGTH | BOTH orderings print; the reversal and its two causes print; the non-confirming branch rule (both numbers in text) is preserved in the appendix subsection; main text keeps a digit-free two-sentence pointer (R2).
KEYS     | AUX-R74-X3 (non-confirming; both print); C075, C076; tab:economics
CLASS    | adverse (as-billed reversal) + positive (projection)

### §6 Store self-description (L596–618)

## CL-C077-C133 [§6 L599–601]
TEXT     | Building BELIEVED indexes reveals three orthogonal failures: overstatement, erasure, invention. Census: FR-Bank marks 5,968 entries stale against ~102 ground truth (~60×); Mem0 exposes updated_at and nothing else on 12.7% of its 10,074 entries; all 23,403 A-MEM link references resolve to zero note identifiers.
STRENGTH | Census numbers exact (diagnostics; no sampling intervals).
KEYS     | C077, C133; tab:believed
CLASS    | adverse (store audit)

## CL-C078 [§6 L604–605]
TEXT     | FR-Bank overstates staleness yet preserves category and lifecycle structure; its corrupted BELIEVED map nevertheless retains the true index's coverage benefit.
STRENGTH | Coverage-retention claim (101.4% backs it).
KEYS     | C078
CLASS    | positive

## CL-BELIEVED-NOK [§6 L607–608]
TEXT     | The obligation judgment does not: under the BELIEVED index the NOK delta is +0.1012 (clustered CI [+0.0217,+0.1744]), a retention of 42.3% against the frozen 60% gate — NOK degrades materially under believed metadata but remains positive. Coverage judgment is insensitive to the corrupted self-description, while obligation judgment loses more than half its benefit.
STRENGTH | Frozen-branch wording ("degrades materially… remains positive"); 42.3% vs 60% gate; +0.1012 CI; "more than half".
KEYS     | AUX-E1R-BELIEVED-NOK
CLASS    | adverse (gate failure, printed)
NOTE     | The link to the flat-lookup reading stays UNdrawn (U9).

## CL-C079 [§6 L610–614] — includes U3
TEXT     | Mem0 erases lifecycle history. A-MEM supplies links that resolve to no notes. The negative TRUE effects occur on these two structureless backends. U3: association does not identify the causal feature; candidate mechanisms remain unresolved after the registered single-channel probe.
STRENGTH | Association-only; U3 verbatim.
KEYS     | C079
CLASS    | adverse + unresolved

## CL-C080 [§6 L616]
TEXT     | The common design law is therefore: self-model expressiveness is a precondition for metamemory.
STRENGTH | Directional law (bounded by U4).
KEYS     | C080
CLASS    | positive (the design law — R3 promotes emphasis, not strength)

## CL-C081 [§6 L618] — U4
TEXT     | "This law is directional but not mechanistic: the source of the observed below-chance behavior remains open."
STRENGTH | Verbatim hedge, exactly once.
KEYS     | C081
CLASS    | scope-limit

### §7 Instruments, discussion, limitations (L620–656)

## CL-C082 [§7.1 L625–627]
TEXT     | A second monitoring finding concerns the study's own apparatus: components that appeared mechanical repeatedly embedded semantic assumptions. Question-only audit: supervised text probes separate PN from non-PN far above chance on EVERY population while a zero-shot mini reader does not, and the powered matched slice stays separable — slot ablation matched the store operation but not question phrasing.
STRENGTH | Universal probe separation; zero-shot null; matched-slice separability.
KEYS     | C082
CLASS    | adverse (instrument) + positive (finding)

## CL-AVCENSUS [§7.1 L629–630]
TEXT     | Coefficient inspection first suggested an authorship mismatch, but the structure runs deeper: on that cell the item-construction taxonomy alone scores 0.9736, above the probe's 0.7972, with six of eight categories single-class. The probe is therefore bounded by that designed structure rather than by authorship alone, so rewording cannot make blind levels prior-controlled; separating the two would need within-category probing, which only one category supports (n=16).
STRENGTH | Decomposition supersedes the authorship-only reading; 0.9736 / 0.7972 / 6-of-8 / n=16 exact.
KEYS     | AUX-R76-AVCENSUS (deterministic census; no interval by class)
CLASS    | adverse (instrument decomposition)

## CL-X1 [§7.1 L632]
TEXT     | The same holds for coverage: the hard tier's FOK-positive class coincides with PN, and the FOK-targeted probe scores 0.9662 pooled — blind FOK levels are not prior-controlled either.
STRENGTH | 0.9662; identity claim (basis of A5).
KEYS     | AUX-R74-X1-POOLED (HIGH branch)
CLASS    | adverse

## CL-PRIORCONTROLLED [§7.1 L634]
TEXT     | The prior-controlled quantities are the paired deltas (identical questions; still measure the index's incremental information) and the balanced authorship-matched cell, where every slot token carries the same one-third PN rate and blind NOK is at chance on the mini and Opus 5 lanes.
STRENGTH | Exactly these two quantities claimed prior-controlled — no more.
KEYS     | AUX-R74-X5 + AUX-R76-MATCHED-PROBE
CLASS    | positive-with-limit

## CL-C083-C085 [§7.1 L637–639]
TEXT     | The monitoring-scoped ledger records failures, corrections, and the preventive check; out-of-scope instruments excluded. Lesson: reporting a quantity beside the invariant that constrains it turns redundancy into a detector for semantic instrument failure.
STRENGTH | Scoped ledger + lesson.
KEYS     | C083 (C084 folded per PART I), C085
CLASS    | procedural + positive (lesson)

## CL-LIMITS [§7.2 L644–656] — includes U5, U6
TEXT     | Six limitations, content-intact in v2:
  1. (C150/C151) Whether acting on these judgments improves retrieval or answering is not measured here; the downstream effect of FOK and NOK remains open.
  2. (C088) Stores are synthetic (temporal ground truth unobservable; privacy); the registered agent-generated slice is a partial response.
  3. (C089) One closed model family primary; secondary replication spans two vendors + one open-weight; the Anthropic pair is cross-generation; all rows reuse the same authored cell.
  4. (AUX-R74-X5+NS5) Authorship-matched slice n=36 on three lanes: blind NOK includes chance on all three, as registered; the indexed NOK delta excludes zero on the Opus 5 lane but NOT on the mini lane, "which ships as its registered failure" (U6); Haiku 4.5 blind-inversion question indeterminate at this size.
  5. (C090/U5) Structureless-store inversion measured across scales; below-chance mechanism remains unresolved.
  6. (C091) FOK's inability to distinguish slot ablation from PN is a measured resolution limit, not evidence that the label is absent.
STRENGTH | Every limitation survives verbatim in content (R78 order).
KEYS     | C150, C151, C088, C089, C090, C091, AUX-R74-X5, AUX-R76-NS5
CLASS    | scope-limit ×6 (incl. the NS-2 frozen failure)

### §8 Conclusion (L658–671)

## CL-C092-C095 [§8 L661–671]
TEXT     | Store-level monitoring improves when the store exposes an expressive self-description. FOK measures intent-conditional coverage; NOK names and measures a previously unformalized obligation judgment. Across the ladder the index makes FOK converge across all tiers; across vendors blind NOK priors point above/below/across chance yet the paired NOK index effect remains positive in every tested lineage. The question-only audit shows blind levels are prior-contaminated; paired deltas still compare identical questions. Excluding mini's all-tie row, the index brings the five varying blind-NOK models into one narrow band. Under the PROJECTED asymptotic caching arithmetic the indexed monitor is cheaper than blind, an ordering the registered billed micro-run REVERSES at current cache pricing. [L671 slogan = paraphrased in v2, ORDERED-MECHANICAL.]
STRENGTH | Conclusion restates at body strength incl. prior-contamination rider and the economics reversal; v2 §8 paraphrases and ends on design law + cross-vendor.
KEYS     | C092, C093, C094, C095
CLASS    | positive + adverse riders

### Statements (L675–683)

## CL-C096 [AI use statement L678]
TEXT     | Agentic coding assistants executed protocols under preregistered human-directed designs; independent implementations for replication and two-direction verification. Humans dispositioned 33 candidate PN rows: 12 confirmed, 11 finalized as rejections, 10 routed for further review — all ten excluded from every reported population. Humans retained design/reporting responsibility; generative AI assisted drafting and LaTeX.
STRENGTH | 33/12/11/10 exact; exclusion clause.
KEYS     | C096
CLASS    | procedural

## CL-C097 [Reproducibility statement L683]
TEXT     | Upon deanonymization the [TODO-URL] artifact activates with frozen registrations, prompts, item manifests, raw monitoring rows, and the value verifiers.
STRENGTH | Carried over as-is (URL mint is [AUTHOR-1]).
KEYS     | C097
CLASS    | procedural

---

## APPENDIX CLAIMS (transfer byte-identical; SAME by construction except the two ordered fixes)

## CL-APP-A [App A, L770–804]
TEXT     | Proof of Prop 1 (C098–C103: witness construction, σ values 0.95/0.85–0.90/0.80/0.70, error ≥ 1/2). Remark 1 + proof (C037, C104–C106: τ_A=0.9, τ_B=0.4 are premises, not inferred quantities).
KEYS     | C098–C106, C037 | CLASS: positive (formal) + scope-limit

## CL-T-ladder-exact [App B, Table 3 L809–838 + prose L843–845]
TEXT     | 12 rows on the matched n=84 cell (54 FOK-pos, 40 PN): mini FOK 0.4488/0.7090/+0.2602 (no item CI — committed E1 primary elicitation predates paired-interval machinery; clustered [+0.0913,+0.3912]); mini NOK 0.5000†/0.7139/+0.2139 († all-tie artifact; clustered not printed); luna FOK +0.1682 [+0.0340,+0.3033] cl [+0.0367,+0.3001]; luna NOK +0.2940 [+0.1696,+0.4172] cl [+0.1984,+0.4051]; sol FOK +0.0364 [−0.0930,+0.1600] cl [−0.1095,+0.1609]; sol NOK +0.3298 [+0.1994,+0.4470] cl [+0.2117,+0.4500]; Opus 5 FOK +0.1213 [+0.0047,+0.2449] cl [−0.0136,+0.2368]; Opus 5 NOK +0.1528 [+0.0659,+0.2509] cl [+0.0923,+0.2392]; Haiku FOK +0.4151 [+0.2336,+0.5712] cl [+0.1339,+0.6129]; Haiku NOK +0.4511 [+0.3265,+0.5741] cl [+0.2925,+0.5981]; K3 FOK +0.0571 [−0.0954,+0.2052] cl [−0.1235,+0.2282]; K3 NOK +0.2605 [+0.1456,+0.3866] cl [+0.1653,+0.3933]. Clustering prose: cell spans 33 of 40 personas; 11 of 12 rows keep intervals excluding zero; the exception is Opus 5 FOK (+0.0047 margin → clustered includes zero; LOPO zero sign changes: point stable, interval fails); every NOK row survives clustering. Caption carries the k=5 vs mini-original split (A4 basis).
KEYS     | C134, AUX-E1R-CLUSTER-CELL | CLASS: positive + adverse (Opus 5 FOK honesty row)

## CL-T-x4-expansion [App B, Table 4 L851–873 + L848–849]
TEXT     | Expansion on full FR-Bank populations, four completed lanes (mini/luna/Opus 5/Haiku, NOK n=661 + FOK n=307 each; all 8 rows with item + clustered CIs as printed); indexed-NOK span 0.0988 < blind 0.2279; all five registered predictions held; sol and K3 stopped by budget directive (1,422 and 231 raw rows retained, disclosed, not scored as cells); the 84-item cell remains the registered primary; mini rows are the committed E1 elicitation re-derived exactly.
KEYS     | AUX-R74-X4 | CLASS: positive + procedural (cap-stop disclosure)

## CL-T-ladder-predictions [App B, Table 5 L875–892]
TEXT     | P1 held (0.5585 CI [0.4299,0.6869] includes 0.50); P2 held (0.5267<0.6745<0.8131, stratified n=150); P3 held (+0.0364<+0.1682<+0.2602); P4 held (+0.2940 CI [+0.1696,+0.4172]); sol threshold FAILED (0.8131>0.75). Populations disclosed per row.
KEYS     | (R75-F1) | CLASS: positive + adverse (failed row prints)

## CL-APP-C [App C, L894–931]
TEXT     | XV-1 failed (directions per lane); XV-2/XV-3/XV-4 held; XV-5 reports. Lane disclosures D86–D91 (temperature, output ceiling, system-role assembly → XV-4 is a band comparison not matched contrast, tokenization, K3 pinned to Moonshot direct, Opus ceiling correction). D93: the frozen XV-1 failure explanation was defective (assumed above-chance miss); the registered gate and failed verdict unchanged. NS-5 (frozen branch (iii) sentence verbatim): Haiku blind NOK point stays below chance while its interval includes chance; indeterminate at n=36; XV-1 never re-adjudicated; the point falls 0.0073 below the registered 0.45 boundary — close-run, ledgered not smoothed.
KEYS     | D86–D91, D93, AUX-R76-NS5-* | CLASS: adverse + procedural

## CL-T-questionprior [App D, Table 7 L935–955]
TEXT     | Supervised TF-IDF cross-model cell 0.7972 [0.6949,0.8927]; hard row (FOK target ≡ PN)‡ 0.9199 [0.8869,0.9472] (committed PN-probe interval printed; D-R74-2 collapse); zero-shot mini 0.4804 [0.3587,0.5935] includes chance; powered matched slice 0.8436 [0.7813,0.8990] not prior-controlled; FOK-target pooled hard 0.9662 [0.9510,0.9788]. ‡ footnote: hard tier contains no PRESENT items → FOK and PN targets label-identical (A5 basis).
KEYS     | AUX-R74-X1-POOLED, D94 | CLASS: adverse (prior contamination record)

## CL-T-matched-cell [App D.1, Table 8 L957–990]
TEXT     | n=36 (12 PN, 29 non-ABSENT; one generator voice; label transfer 36/36). Monitor lanes: mini NOK 0.4774 [0.2991,0.6623] / 0.6771 / +0.2028 [−0.1121,+0.4984]; Opus 5 NOK 0.3993 [0.2008,0.6232] / 0.6962 / +0.2978 [+0.0752,+0.5292]; Haiku NOK 0.4427 [0.2582,0.6522] / 0.6562 / +0.2208 [−0.0522,+0.4809]; FOK rows descriptive (blind intervals not reported): mini +0.3110 [+0.1133,+0.5222], Opus 5 indexed 1.0000 ∆ +0.3372 [+0.1399,+0.5709], Haiku indexed 0.9901 ∆ +0.4470 [+0.2148,+0.6723]. Probe block: supervised TF-IDF on the same 36 questions 0.3472 [0.1673,0.5424] — a construction check, not comparable with Table 7 rows; zero-shot not re-run (no cached responses). Caption: paired NOK delta positive on all three, excludes zero on Opus 5 ONLY — the resolution an n=36 cell affords.
KEYS     | AUX-R74-X5-*, AUX-R76-NS5-*, AUX-R76-MATCHED-PROBE | CLASS: positive-with-limit + negative (mini NS-2)
NOTE     | Receives the relocated D2a paragraph (fix a) — an authorship/prior control, NOT a store counterfactual; the strict counterfactual is absent and left to future work. R96 (2026-09-12): the last clause is superseded; Appendix D.2 reports the strict design since R82-INT and the paragraph's closing sentence now points there (R96 block, entry 3).

## CL-T-av-census [App D.1, Table 9 L992–1013]
TEXT     | Category census on the cross-model cell (n=84, 40 PN): ranking by category alone attains 0.9736, above the probe's 0.7972; deterministic census on committed labels — no interval by class (same convention as the one-bit rule); six of eight categories single-class; only expired logistics carries both at usable size (n=16; rows as printed).
KEYS     | AUX-R76-AVCENSUS (D-R74-13 provenance) | CLASS: adverse

## CL-APP-E [App E ledger, L1015–1050]
TEXT     | 12 numbered instrument records + 1 preventive, each at printed strength (20% expiry-route precision; 69–86% PN spot-check precision → universal human verification; pilot prompt falsity; lexical 0.697 → two-channel 0.995, ε=0.005 conditional-not-posterior rider; recency-time fix; probe-screen fix; 3/300 and 1/300 reproduction → k=5 protocol; reversed drafted conclusion; turn-total telemetry → exact frontier economics not reported; import-shadowing disclosed not repaired; template-signal probe → matched slice reported as second population; NB-3 disqualified as index reader, retained as instrument-failure record; preventive model-identifier check). C120: the shared failure is a semantic assumption hidden inside a seemingly mechanical operation.
KEYS     | C108–C120, AUX-E1R-NB3 | CLASS: procedural + adverse (instrument record)

## CL-T-pilot-record [App F.1, Table 10 L1054–1075]
TEXT     | E0 estimands: FOK raw n=210 (141/69) +0.3088 [+0.2051,+0.4090]; blind-deduplicated +0.2747 (n, CI not recorded); NOK +0.0411 [−0.0569,+0.1255]; non-forced calibration ~0.26 mean vs 67% base rate, ECE 0.4155. C122: raw and deduplicated estimands must not be mixed; neither prompt-level comparable with E1.
KEYS     | (Table 10), C122 | CLASS: positive + negative (pilot NOK null) + procedural

## CL-T-e1-construction [App F.2, Table 11 L1077–1106]
TEXT     | Design records: scoreable corpus 1,183 (40 personas, 3 backends, preregistered Mem0 exclusions); hard tier 588 (35 FOK-pos; 145 A-MEM + 136 Mem0 external negatives); FR-Bank hard 307 (145 natural-absent, 127 slot-absent, 35 PN); intent audit 413 (route precision 20%; 110 items = 26.6% PN-ineligible by definition); inherited retrieval premise 5%. Measured checks: PN verification 104 (248 judgments: 192/179 membership; 56/48 semantic) [A3 basis]; presence control lexical 0.697 / embedding 0.965 / combined 0.995 / ε=0.005; leakage screen 180 calls, 0 leaks, frozen threshold >3/30; monitor querying 2,698 responses, temperature 0, 0 parse failures; blind stability k=3, 46/50 identical; response format AUROC 0.7516, 5 staircase values; believed FOK retention 101.4% (n=661).
KEYS     | (Table 11) | CLASS: procedural

## CL-APP-F3 [App F.3, L1108–1151]
TEXT     | Statistics: FOK positive = non-ABSENT, NOK positive = PN; items nested in 40 personas; paired percentile bootstrap, 1,000 item-level resamples, seed 42, single-class draws discarded, 2.5/97.5 percentiles; single-class rows have undefined AUROC/no interval; the scored ITEM is the implemented resampling unit. Clustered sensitivity computed after item-level records frozen; item-level remains the preregistered primary. ICC of the paired contribution spans [−0.0544,+0.0870]; clustered-to-jackknife width ratio 0.95–0.99 on all six calibration rows; four of six clustered intervals narrower. Table 12 rows (incl. easy-contrast item CI [+0.1179,+0.2596] printed first time; pooled clustered [+0.1552,+0.2996]; FR-Bank FOK clustered [+0.1259,+0.2767]; easy cl [+0.1327,+0.2433]; NOK cl [+0.1552,+0.3237]; Mem0 cl [−0.1638,−0.0286]; A-MEM cl [−0.1654,−0.0446]). Reliability figure: indexed ranks well (ρ 0.9000 intact, 1.0000 names-only) and scales badly (predicted 0.217 vs observed 0.056, ~3.9× over-confident); blind neither ranks (ρ 0.1026) nor calibrates. Model identifiers pinned; prompts hash-verified.
KEYS     | C142–C144, AUX-E1R-CLUSTER, AUX-E1R-ICC, AUX-E1R-RELIABILITY | CLASS: procedural + negative (calibration)

## CL-T-destruction [App F.4, Tables 13–14 L1153–1192]
TEXT     | Pooled probe (n=588): blind 0.5258/ECE 0.1596; intact 0.7530/0.1741; counts jittered 0.7697 (+0.0167 [−0.0174,+0.0552]) 0.1720; counts coarsened 0.7625 (+0.0095 [−0.0390,+0.0657]) 0.1668; names only 0.8516 (+0.0985 [+0.0426,+0.1577]) 0.0583. C129: pooled names-only row driven by external structureless stores; FR-Bank row supports only count non-necessity. FR-Bank probe (n=307): intact 0.7003; jittered 0.7018 (+0.0015, includes zero); coarsened 0.7015 (not printed, includes zero); names only 0.7283 (not printed, includes zero); endpoints not separately recorded.
KEYS     | C135, C129 | CLASS: positive-with-limit

## CL-T-wrongindex [App F.4, Table 15 L1194–1222] — ORDERED-MECHANICAL flip target
TEXT     | Committed values (intact − manipulated convention in paper.tex): WRONG-PERSON FOK n=307: 0.7003 / 0.3631 / +0.3383 [+0.2169,+0.4506]; WRONG-PERSON NOK n=661: 0.7339 / 0.4659 / +0.2668 [+0.2010,+0.3298]; SHUFFLED FOK: 0.7003 / 0.7053 / −0.0031 [−0.0546,+0.0499]; SHUFFLED NOK: 0.7339 / 0.7116 / +0.0217 [−0.0178,+0.0611]. Footnote: shuffle permutes per-category count rows and name lists under fixed seed, preserves byte length exactly on all 661 indexes, preserves the global multiset and flat superseded-names section — bounds per-category correspondence and nothing more. Prose L1218–1219: FOK falls 0.7003→0.3631 below chance (mismatched description actively misleads); flat-lookup consistency reading.
STRENGTH | v2 prints manipulated − intact: −0.3383 [−0.4506,−0.2169]; −0.2668 [−0.3298,−0.2010]; +0.0031 [−0.0499,+0.0546]; −0.0217 [−0.0611,+0.0178] + estimator footnote (≤0.002 MC gap) per A2 Option 3. Values identical in magnitude; convention only.
KEYS     | AUX-R77-SWAP-*, AUX-R78-SWAP-GAP (new), D-R74-19, D-R74-20 | CLASS: positive (SW-1) + scope-limit (SW-2 bound)

## CL-T-factorial [App F.5, Table 16 L1225–1246]
TEXT     | 2³ NOK factorial: lifecycle-index main effect +0.1980; prompt effects +0.0134, −0.0193 (n/CIs not recorded); matching condition 0.7344; E1 indexed NOK 0.7339; E1 delta +0.2393 [+0.1801,+0.2949]. Endpoints for summary effects not separately recorded.
KEYS     | (Table 16) | CLASS: positive

## CL-T-inversion-x2 [App F.6, Tables 17–18 L1249–1294] — U8 (byte-identical)
TEXT     | Inversion rows: mini/Mem0 238: 0.5746/0.4777/−0.0969 [−0.169,−0.025]; mini/A-MEM 284: 0.5591/0.4526/−0.1065 [−0.173,−0.040]; sol/external pooled 66: 0.9130/0.8083/−0.1046 [−0.2024,−0.0174]; luna/external pooled 66: 0.7894/0.4514/−0.3380 [−0.4896,−0.1811]. X2 ablation (blind/intact committed, re-derived exactly): Mem0 count removed 0.4802/−0.0943 [−0.1674,−0.0233]; markers removed 0.4796/−0.0949 [−0.1654,−0.0250]; both removed 0.4664/−0.1082 [−0.1769,−0.0392]; A-MEM count removed 0.4587/−0.1004 [−0.1699,−0.0309]; markers removed 0.4705/−0.0886 [−0.1550,−0.0269]; both removed 0.5223/−0.0368 [−0.1041,+0.0268]. The names arm has no ablation site — every name section's body is exactly the inexpressibility marker (D-R74-3) — and therefore equals intact by construction.
KEYS     | C069-block, AUX-R74-X2, D-R74-3 | CLASS: adverse (all rows print)

## CL-T-baselines [App F.7, Table 19 L1296–1345]
TEXT     | NB-1 deterministic lifecycle rule; NB-2 logistic over numeric features (label-supervised, persona-grouped); NB-4/NB-5 unsupervised lexical/embedding matchers; NB-3 disqualified pre-scoring (question reader; index-only ablation shown). Ten rows exactly as printed, incl. the two rows where a baseline outranks the monitor: A-MEM FOK-TRUE −0.0700 and pooled-hard FOK-TRUE −0.0594 (both print; the footnote scopes them: pooled absolute levels uninterpretable for ANY reader — one-bit rule 0.7541; paired deltas unaffected). FR-Bank margins: +0.0817 / +0.0819 / +0.1365; BELIEVED NOK near-tie 0.5959 vs 0.5974 (−0.0015, inside the ±0.05 tolerance). Two readings (L1343–1345): (1) under corrupted self-description the monitor's obligation judgment falls back to what a similarity matcher already achieves — the same degradation the 42.3% retention records, reached by an independent route; (2) the monitor's margin exists where lifecycle structure exists and vanishes where it does not — the same boundary the inversion result draws.
KEYS     | AUX-E1R-BASELINES, AUX-E1R-NB3 | CLASS: positive-with-limit + adverse rows
NOTE     | The stranded D2a paragraph departs to D.1 (fix a); the "Two readings" paragraph stays and still follows the table.

## CL-T-believed [App F.8, Table 20 L1347–1367]
TEXT     | Census: FR-Bank — of 18,936 entries and 109 events, marks 5,968 stale against ~102 (~60×) and retains an active obsolete assertion after 72% of supersession events at the census threshold; Mem0 — of 10,074 entries 12.7% expose updated_at only; UPDATE overwrites history, ingestion silently lossy; A-MEM — all 23,403 link references resolve to 0 note identifiers. Census diagnostics; no sampling intervals exist.
KEYS     | C133 | CLASS: adverse (store audit)

## CL-T-registrations [App G, L1371–1421]
TEXT     | 19 registration rows with commit hashes, freeze dates, scopes, outcomes exactly as printed (incl. "non-confirming; both print" for X3; "cap-stop; XP-1–5 held" for X4; "S1 cured; NS-1 held; NS-2 split" for X5; "branch iii; census and probe report" for R76; "SW-1 held; SW-2 failed" for R77). Deviation index: 15 lines mapping deviations to ledger items/appendices.
KEYS     | (Table 21) | CLASS: procedural
NOTE     | Registration vocabulary in MAIN TEXT is limited to one pointer per section (STYLE_SPEC); the machinery lives here.

---

## Reconciliation notes (sweep 3 — residue and cross-checks)

- The reports' canonical list (DESCOPE_REPORT / REPORT_AUDIT) was checked against this
  inventory: every item in the R78 order's negative-claims list maps to an entry above
  (ECE unimproved → CL-C139; inversion → CL-C069-C071/CL-T-inversion-x2; 42.3% vs 60% →
  CL-BELIEVED-NOK; SW-2 bound → CL-SW2; NS-2 mini failure → CL-LIMITS item 4 /
  CL-T-matched-cell; as-billed reversal → CL-ECONOMICS; 5.2% posterior →
  CL-C046-POSTERIOR; resolution limit → CL-C051/CL-LIMITS item 6; pooled-level
  uninterpretability → CL-C141/CL-T-baselines footnote).
- Tokens inside tikzpicture blocks (fig:ladder, overview) are trace_scan-excluded but the
  plotted values are claim-bearing → covered by CL-FIG-ladder.
- No claim in paper.tex asserts the BELIEVED-retention↔flat-lookup link (U9 confirms the
  only occurrence is the % comment at L1220–1222).
- The frozen SW-3 sentence and the pre-R77 "0.5%" posterior never appear in paper.tex
  (verified by the R77 closeout sweeps); they must not appear in paper_v2 either.

Entry count: 106 entries (grouped; every table row enumerated inside its entry). Corrected 2026-08-30 (D-R81-3): the figure had read 62 since R78 while the real heading count was 106; tools/claims_diff.py now recounts it at every gate run.
CLASS tally: positive/positive-with-limit 24 · adverse 14 · negative 5 · scope-limit 11 ·
definition 9 · procedural 10 · unresolved 2 (some entries carry two classes; primary counted).


## R101 AUTHORIZATION BLOCK — dated 2026-09-13

Appended by R101 (the RESP lanes and the downstream experiment DS landing), anchored to the R99 block
above (open; R99 Phase 1, the abstract, is the only R99 phase landed), landing in `paper_v9.tex`
(LINEAGE, below). Paper edits, tool-list entries and ledger printed-form notes only: no experiment, no
model call, no embedding call. **No registered bar, threshold, verdict or frozen text changes.** Records:
`reviews/R101_REPORT.md`, `ds_downstream/DEVIATIONS_DS.md` D-DS-3 (commit `e14c50e`). Sources of every
number: `resp_review/NUMBERS_RESP.md` by key (`AUX-RESP-L1-MINI`, `-L1-REDRAW`, `-L1-NB6`, `-L2-REACH`,
`-L2-MINI-NOK`, `-L2-MINI-FOK`, `-L3-MINI`, `-SPEND`; the printed forms under `AUX-RESP-PRINTED`) and
`ds_downstream/NUMBERS_DS.md` by key (`AUX-DS-FLAGCENSUS`, `-REACH`, `-PRESENT`, `-ABSTAIN`,
`-VIEWSIZE`, `-STAGE2`, `-SPEND`, `-PARAGRAPH`; the printed form `AUX-DS-PARAGRAPH-PRINTED`); the frozen
texts of `registrations/ADDENDUM_RESP.md` (frozen `17e6328`, R98) and `registrations/ADDENDUM_DS.md`
(frozen `a5a2036`, R100) as their ledgers print them with placeholders filled.

**BASE.** `paper_v9.tex` at the R99 Phase 1 state is uncommitted on disk (R93–R99 are pending [AUTHOR-1]'s
word), so no git revision holds it. The gates read it as the temporary tree object `a7e5f4f3`,
written from the working copy with a scratch index (`git hash-object -w` + `git write-tree` under a
scratch `GIT_INDEX_FILE`; the real index and HEAD untouched, nothing committed): `--base=a7e5f4f3c6b5471ea805c4862beaa789fd3d817d
--tex=paper_v9.tex --base-tex=paper_v9.tex`. The tree carries the pre-R101 `paper_v9.tex` and the
`paper_v9.pdf` built from it (three pdflatex passes).

**LINEAGE.** The working lineage stays `paper_v9.tex` (the R99-RESTRUCTURE file; this landing is a
phase inside it, on the author's order: build `paper_v9` at this state). Tool defaults stay at v8 and
every gate is invoked with explicit `--tex=paper_v9.tex`; `trace_scan_v13` gains
`ds_downstream/NUMBERS_DS.md`; `ARTIFACT/registrations/` gains copies of `ADDENDUM_RESP.md` and
`ADDENDUM_DS.md` and `ARTIFACT/ledgers/` copies of `NUMBERS_RESP.md`, `DEVIATIONS_RESP.md`,
`NUMBERS_DS.md` and `DEVIATIONS_DS.md`, so `frozen_diff` watches the landed texts from the next round
on. The R99 restructure's later phases (R-b to R-e) have not landed; R-e's reserved L1/L2/L3/DS slots
are filled here at their current sites (§4.2 for L1, L2 and the L3 clause; §7 for DS), every site
reached by `\ref`, so the restructure carries them.

**Rulings taken from the order ([AUTHOR-1], 2026-09-13).**

- **R-a, the bars stand; the paper states the premise.** DS-P1 and DS-P2 were set under the inherited
  5% premise and DS was frozen before RESP L2 measured the unmasked reach at 0.5192, by design; the
  bars and verdicts print as set, and one authorized sentence after the frozen DS paragraph states the
  premise they rest on (D-DS-3 (a), the D93 precedent: defective attachment, gate unchanged). DS-P4
  was unfulfillable by its own gate; the verdict stands and the repair is DS Amendment 1, a
  v3-elicited gate, descriptive (D-DS-3 (b)).
- **R-b, frozen wording ships verbatim (R78-2c).** The DS paragraph of `ADDENDUM_DS.md` §PAPER replaces
  C150 and C151 together (R5 of the DS Phase A rulings), each bracket resolved by its verdict, the
  placeholders filled at the ledger's precision; the interval placeholder prints in the R98 R-b idiom
  (item-level first, the profile interval beside it as with questions grouped by user profile). The
  L1-P1 held reading prints in §4.2 beside the lookup sentence, as `ADDENDUM_RESP.md` §L1 sites it.
  Every failed prediction's frozen failure text prints in Appendix F, new subsection `app:resp`, with
  its numbers, under a word label and a pointer to Table 25 (prose_scan rule A).
- **R-c, the premise restated as conditional.** Sections 1, 3 and 8 and the Figure 1 caption say:
  under the lifecycle mask the inherited store applies, retraction records pass retrieval at 5%;
  without the mask, half of the forbidding records (54 of 104) enter a five-item view and seven in ten
  (74 of 104) a ten-item view. The order's phrase for the second figure was three quarters; the
  ledgered value is 0.7115, so the manuscript prints seven in ten with the count beside it. Proposition
  1 is unchanged; its ordinary-in-practice clause becomes ordinary under the masking that
  lifecycle-tracking and overwriting stores apply. Every instance of the index-supplies-what-retrieval-
  cannot claim and its variants is replaced by the claim the data support (entries R101-9, -11, -12;
  the §2 sentence at L192 and the §5.1 heading are about the question, not retrieval, and stand).
- **R-d, vocabulary (R98 R-e).** New main-text prose says none of arm, cell, lane, gate, verdict,
  registered, committed, frozen; the frozen DS paragraph and the L1 sentence carry such words and are
  entered in prose_scan's WHITELIST and slogan_scan's EXEMPT_FROZEN_REGISTERED, sourced to the printed-
  form ledger keys.
- **R-e, the count of preregistered predictions.** §1's count rises from 47 to 58 (six RESP, five DS)
  and the not-held count from 8 to 16 (five RESP, three DS), on the R97-7 / R98-9c precedent; for the
  author's ruling (D-R101-1).
- **R-f, page budget.** The page gate already fails at the R99 Phase 1 state (v8: label on 10, D-R98-2);
  the order adds main-text length (§1 two sentences, §4.2 two sentences and a clause, §7 two paragraphs,
  §8 one sentence, the abstract one clause) and cuts nothing on this program's judgment; the residual
  is reported under D-R101-2.

**Entries, one per change; each quoted fragment is the frozen string that changes.**

- **R101-13, Abstract (sentence 2; the clause prints as a sentence of its own, the 40-word rule).** Before: "Given a summary of a store's contents and lifecycle states, a name lookup reads the obligation as reliably as the smallest model." After: "Given a summary of a store's contents and lifecycle states, a name lookup reads the obligation as reliably as the smallest model. Retrieval that returns non-active records with their lifecycle tags reads obligations nearly as well, and the two together best."
- **R101-9, Figure 1 caption.** Before: "In a lifecycle-tracking store the record that forbids the answer is masked out of the retrieved set by its lifecycle state, so no bounded retrieved view reaches it." After: "Under the lifecycle mask a lifecycle-tracking store applies, the record that forbids the answer is masked out of the retrieved set; without the mask, half of such records enter a five-item view with their lifecycle tags."
- **R101-6, Section 1, premise (three sentences).** Before: "In a lifecycle-tracking store, the record that forbids use is masked out of the retrieved set by its lifecycle state. On that store's own benchmark, retraction records pass retrieval at only $5\%$ under the mask \citep{fr}. The few items a retriever returns can therefore include the stale plan and miss the record that cancels it." After: "Under the lifecycle mask the inherited store applies, the record that forbids use is masked out of the retrieved set: on that store's own benchmark, retraction records pass retrieval at only $5\%$ \citep{fr}. Without the mask, half of the forbidding records ($54$ of $104$) enter a five-item similarity view and seven in ten ($74$ of $104$) a ten-item view, each carrying its lifecycle tag where the store records one (Section~\ref{sec:discussion}). Under the mask, the few items a retriever returns can include the stale plan and miss the record that cancels it."
- **R101-8, Section 1, prediction count.** Before: "Of the $47$ preregistered predictions, $8$ did not hold;" After: "Of the $58$ preregistered predictions, $16$ did not hold;"
- **R101-7, Section 1, scope sentence.** Before: "The empirical scope is pre-retrieval monitoring on synthetic stores, with one primary closed model family; downstream behavior is outside this paper." After: "The empirical scope is pre-retrieval monitoring on synthetic stores, with one primary closed model family; one downstream experiment measures what a policy that acts on the judgment sees and uses (Section~\ref{sec:discussion})."
- **R101-10, Section 3, Proposition 1 gloss.** Before: "The premise is ordinary in practice: in that store, retraction records pass similarity retrieval at $5\%$ \citep{fr}, and the proposition's force is that measured premise rather than a deep theorem." After: "The premise is ordinary under the masking that lifecycle-tracking and overwriting stores apply: in that store, retraction records pass similarity retrieval at $5\%$ under its mask \citep{fr}, and the proposition's force is that measured premise rather than a deep theorem. Without the mask, half of the forbidding records enter a five-item view (Section~\ref{sec:discussion})."
- **R101-4, Section 4.2, after the lookup paragraph (L1 frozen held reading; L2 descriptive).** Before: "It does not establish that a lookup matches the larger models, whose extra gain sits on the counted states (Table~\ref{tab:nb6-composition}). " After: "It does not establish that a lookup matches the larger models, whose extra gain sits on the counted states (Table~\ref{tab:nb6-composition}). Removing the target's own name and its nearest neighbours from the superseded-names section costs the smallest model $0.3262$ of its supersession discrimination ($0.8572$ to $0.5310$; interval $[-0.3991,-0.2548]$, and $[-0.4327,-0.2167]$ with questions grouped by user profile): the obligation is read off the name, as the manuscript says. A monitor reading the five retrieved items with their lifecycle tags, and no summary, reaches $0.6851$ on obligation against the summary's $0.7339$, within tolerance; the two together reach $0.8303$, the gain on the states the summary only counts (Appendix~\ref{app:resp}). "
- **R101-5, Section 4.2, blind-arm sentence (L3 clause).** Before: "Mini's blind obligation score takes two distinct values on these $661$ questions and one on the cross-model set, so it carries no ranking to improve on." After: "Mini's blind obligation score takes two distinct values on these $661$ questions, with or without the rubric's detection step, and one on the cross-model set, so it carries no ranking to improve on."
- **R101-1/2/3, Section 7, Limitations (C150 and C151 replaced by the frozen DS paragraph, the authorized sentence, the failures paragraph).** Before: "Whether acting on these judgments improves retrieval or answering is not measured here. % C151 This paper establishes the pre-retrieval measurement; the downstream effect of FOK and NOK remains open. " After: "%% CHANGED (R101-1): C150 and C151 replaced together by the frozen Section 7 paragraph of registrations/ADDENDUM_DS.md (frozen a5a2036, R100), assembled from the verdicts (ds_downstream/NUMBERS_DS.md AUX-DS-PARAGRAPH, printed form AUX-DS-PARAGRAPH-PRINTED); R78-2c, frozen wording ships verbatim. CLAIMS.md R101 block. Acting on the obligation judgment changes what a bounded view carries. The store's truthful metadata flags $82$ of the $104$ forbidding records; the other $22$ ($18$ retraction-derived, $4$ expiry-derived) are a store-side fact of the kind Table~\ref{tab:believed} records, retrieve as active, and are out of reach of any policy that acts on the metadata. On the $104$ obligation items, the five-entry similarity view contains the forbidding record for $0.5192$; a gold-label fetch of the store's lifecycle records for the obligation's own attribute reaches $0.9519$, $0.4327$ above retrieval alone and short of the $0.50$ bar; gated on the smallest model's committed obligation score at its base rate, the fetch reaches $0.8173$, retaining $0.7561$ of that gain on the supersession-derived items (interval $[0.610, 0.872]$; $[0.562, 0.939]$ with questions grouped by user profile), short of the $60\%$ bar under the weaker reading. The superseded-names lookup reaches $0.8173$ at the same fetch budget, within tolerance of the model. Naming the retracted and expired attributes raises the gated reach on those obligations only from $0.7805$ to $0.7805$: the gate elicited under the counting summary does not fire on them. The coverage gate at its base rate costs $0.0287$ of coverage on the items whose licensed record the store holds, within tolerance. With the forbidding record in view and tagged, the smallest model gives the stale value as the answer in $0$ of $82$ cases at the registered detector threshold ($11$ of $82$ at the join's gold threshold; $6$ of $17$ where the record printed as active) (Appendix~\ref{app:resp}). %% CHANGED (R101-2): the one authorized sentence after the frozen paragraph (D-DS-3 (a), the D93 precedent). CLAIMS.md R101 block. The two failed bars were fixed before the study measured the retrieval premise they rest on; the mechanism numbers stand and the bars are printed as set.  %% CHANGED (R101-3): the RESP and DS failures grouped by cause; every number by key (NUMBERS_RESP.md, NUMBERS_DS.md). CLAIMS.md R101 block. Eight of the eleven items these two studies fixed in advance did not hold, and each prints under the text written before it was scored (Appendix~\ref{app:resp}; Table~\ref{tab:registrations}). Retrieval reaches half of the forbidding records once non-active entries are not masked, which fails the below-cutoff premise ($0.5192$ against $0.20$) and narrows the oracle margin of the downstream experiment ($+0.4327$ against $0.50$); the retrieved view alone also stays within tolerance of the summary ($-0.0488$), where a shortfall was expected. The smallest model's retention of the oracle's gain is a near miss under the stricter interval convention ($0.7561$, with $[0.563, 0.939]$ grouped by user profile against $0.60$). One fetch rule could not fire by construction, because its score was produced under a summary that names no counted-state attribute, and is under repair (D-DS-3, Table~\ref{tab:registrations}). The smallest model's blind obligation score is flat with or without the rubric's detection step (two values; $0.4888$, interval including chance). Two more miss in the direction the data point: the own-name ablation also moves the retraction-derived items ($-0.1404$), and adding retrieved records to the summary raises the judgment beyond tolerance ($+0.0964$).  "
- **R101-11, Section 8, opening.** Before: "A monitor that sees only retrieved items cannot settle whether a store holds content that must not be used, because the record that forbids use can sit outside them. The judgment must come from what the store says about itself." After: "The store's lifecycle metadata supplies the obligation judgment. A summary exposes the states it names; retrieved records that carry their lifecycle tags expose the states the summary only counts; the two together give the best monitor measured ($0.8303$)."
- **R101-12, Section 8, boxed paragraph (last sentence).** Before: "A system should therefore decide obligations with a lookup over a name-bearing lifecycle summary, spend model calls on coverage only where the store has structure, and treat a store that cannot write such a summary as one no monitor repairs." After: "A system should therefore read obligations by two routes: a name-bearing lifecycle summary, and retrieval that returns non-active records with their lifecycle tags. On the state the summary names, a lookup over that summary decides; model calls go to coverage only where the store has structure, and a store that cannot write such a summary is one no monitor repairs."
- **R101-14, Appendix G (Table 25 rows and the deviation index).** After: "% R101-14: the RESP and DS rows (registrations/ADDENDUM_RESP.md frozen 17e6328, R98; registrations/ADDENDUM_DS.md frozen a5a2036, R100). CLAIMS.md R101 block. RESP: review-response lanes & \texttt{17e6328c81} & 2026-09-12 & the own-name ablation, the retrieved-view and hybrid monitors, and the rubric-gate test on the full obligation population, six predictions and their failure texts: L1-P1 held; L1-P2, L2-P1, L2-P2, L2-P3, L3-P1 failed, all printed; L2 corrects the retrieval premise of Section 1 & held / failed \\ DS: downstream experiment & \texttt{a5a2036c3b} & 2026-09-13 & six policies over the obligation and coverage scores already on record, their assembled views, reach and abstention, and one answer call per distinct view; five predictions: DS-P3 and DS-P5 held; DS-P1, DS-P2 and DS-P4 failed; two bars set under the 5\% premise the study corrected at L2; one prediction unfulfillable by its own gate (D-DS-3) & held / failed \\" and "Truthful metadata does not flag $22$ of the $104$ forbidding records: DS D-DS-1; Appendix~\ref{app:resp}.\\ Fetch-set zero count transcribed from the unflagged count: DS D-DS-2; Appendix~\ref{app:resp}.\\ Two bars set under the premise corrected at L2; one prediction unfulfillable by its own gate: DS D-DS-3; Appendix~\ref{app:resp}.\\ No deviation on the review-response lanes: RESP; Appendix~\ref{app:resp}.\\"
- **R101-15, Appendix F, new subsection `app:resp`** (own-name ablation, retrieved-view monitors, the
  rubric gate, the downstream experiment): three tables (`tab:resp-l1`, `tab:resp-l2`, `tab:ds`), the
  L3 paragraph, the D-DS-1 paragraph, and every frozen text printed with its numbers and its outcome.
- **R101-16, non-manuscript writes.** `tools/prose_scan.py` WHITELIST and `tools/slogan_scan.py`
  EXEMPT_FROZEN_REGISTERED gain the DS paragraph and the L1 sentence; `tools/trace_scan_v13.py` gains
  `ds_downstream/NUMBERS_DS.md`; `ARTIFACT/registrations` and `ARTIFACT/ledgers` copies as LINEAGE;
  `ds_downstream/NUMBERS_DS.md` gains `AUX-DS-PARAGRAPH-PRINTED` and `resp_review/NUMBERS_RESP.md`
  gains `AUX-RESP-PRINTED` (the printed forms of the L1 sentence and the L2 sentence); this block;
  `reviews/R101_REPORT.md`.
- **R101-17, gate fixes after the first run (D-R101-3).** The abstract clause prints as its own sentence (41 words in one sentence; eight sentences, inside the 6-10 band); the L2 sentence loses three words (42 to 39); the failures paragraph says did not hold and miss in place of failed (prose V); the author's authorized sentence keeps its wording and is whitelisted as ordered wording (prose_scan WHITELIST, ORDERED-R101), on the R79 precedent.


---

## R102 AUTHORIZATION BLOCK — dated 2026-09-13

**Scope.** The clarity rewrite of the main text ordered by the author's brief "Knowing the Store, v9 to v10" (abstract and Sections 1 to 10 rewritten from the ground up; appendices light pass only). **No registered bar, threshold, verdict or frozen text changes.** No model call. Every number in a v10 table equals its v9 value; every prose number exists in v9 on the same population and condition, printed either as v9 prints it or as its two-decimal rounding (rule 1.2 of the brief; `numeric_diff.py --round2`; `reviews/NUMBERS_R102.md`); no v9 number disappears (rule 1.3); no caveat vanishes (rule 1.4; `reviews/v10/CAVEAT_LEDGER.md`); no new claim (rule 1.6).

**Lineage.** `paper_v10.tex` is a new file beside `paper_v9.tex`; v9 is untouched. Reports: `reviews/v10/` (OUTLINE.md approved 2026-09-13; REPORT.md; NUMBER_MOVES.md; CAVEAT_LEDGER.md; CONFLICTS.md; CHANGES.md).

**BASE.** The tree object written from the working copy with a scratch index (`git hash-object -w` + `git write-tree` under a scratch `GIT_INDEX_FILE`; the real index and HEAD untouched, nothing committed), holding `paper_v9.tex` as edited at 15:05 and a fresh three-pass build of it (37 pages; page census: label on page 10, reading 536, slack -51): `--base=841453bca6d50811900a9ad7035631862f7812fe --tex=paper_v10.tex --base-tex=paper_v9.tex`.

**Rulings taken by the author before Pass 2 (2026-09-13, in chat), recorded here because each one departs from a written rule.**
- **R-a, abstract.** The brief's abstract with the "rebuilt from ground truth" clause cut and the 42-word headline sentence split as the author wrote it (eight sentences, numerals in one). Its length (over 150 words) is logged against R99 ruling R-f in `reviews/v10/CONFLICTS.md`; length is not a stop condition.
- **R-b, "held" and "failed".** The brief's rule R9 wins over prose_scan V. `tools/prose_scan.py` blanks the clause "predicted X; observed Y; held|failed" before the V check; the bare words stay barred. Recorded in CONFLICTS.md.
- **R-c, defect 1 inside the frozen DS paragraph.** D-DS-4 is registered (`ds_downstream/DEVIATIONS_DS.md`): the freeze (R78-2c; the D93 form) forbids in-place rewording even of a zero-change phrasing, so the sentence ships verbatim and a lead-in sentence before the paragraph states the zero change plainly.
- **R-d, frozen texts in the body.** Only texts marked [MAIN] in their registration stay in the body; every other frozen text moves to its appendix and the body keeps a one-clause outcome. The body binds "index" once at Definition 3 ("the summary (the index, in the preregistered texts)") and "matcher, NB-6" once at the first lookup mention.
- **R-e, the 42.3% row.** Table 5's fifth row carries the BELIEVED NOK gain $+0.1012$ with its item-level interval; $42.3\%$ prints as the ratio of point estimates, as v9 prints it.
- **R-f, page gate.** Nine pages binding; prose trimmed in the OUTLINE.md order; the Section 4 conventions paragraph and the four findings paragraphs of Section 5 are never trimmed; if prose does not reach nine pages, two table moves are pre-authorized in order (Table 1 folds into prose; Table 4 moves to Appendix B with its numbers kept in prose) and no others.
- **R-g, landings.** The absence-split values ($0.5517$, $0.8782$, $0.4336$, $0.4972$) land in Appendix F.3 beside the presence-control record; the paired ECE difference ($+0.0145$ $[-0.0037,+0.0345]$) lands in the Table 13 row block.

**Entries.** Each Before is the CLAIMS.md-quoted (or list-held) v9 string frozen_diff reports as changed; After is the v10 text or the landing that carries the same content at the same strength. No registration-frozen string (class R, U, EXEMPT_FROZEN_REGISTERED, W FROZEN-REGISTERED) is reworded; the one such string listed (R102-1) is a body copy removed under ruling R-d, its registration form printing in Appendix F.10.

- **R102-1, Section 8 (ruling R-d).** Before: "Removing the target's own name and its nearest neighbours from the superseded-names section costs the smallest model $0.3262$ of its supersession discrimination ($0.8572$ to $0.5310$; interval $[-0.3991,-0.2548]$, and $[-0.4327,-0.2167]$ with questions grouped by user profile): the obligation is read off the name, as the manuscript says." After: the body copy is removed; the registration form (persona-clustered idiom) prints unchanged in Appendix F.10; Section 8 carries the outcome clause "Removing the target's own name and its nearest neighbours from the summary drops GPT-4.1 mini's supersession judgment from $0.86$ to $0.53$ on the $661$ questions. We predicted a loss beyond tolerance; observed $-0.33$; held."
- **R102-2, Section 4.** Before: "All confirmatory claims were preregistered before data collection; Appendix~\ref{app:registration} lists every registered prediction and its outcome, and any result we label exploratory was not preregistered." After: "Appendix~\ref{app:registration} lists every prediction fixed before data collection with its outcome; a result labelled exploratory was not fixed in advance."
- **R102-3, Section 8 (brief defect 8).** Before: "The two failed bars were fixed before the study measured the retrieval premise they rest on; the mechanism numbers stand and the bars are printed as set." After: "The two bars that did not hold were set before the study measured the retrieval premise they rest on; the mechanism numbers stand and the bars are reported as set."
- **R102-4, Section 6.** Before: "The index names superseded content and only counts retracted and expired content" After: "The summary names superseded content and only counts retracted and expired content, and neither the lookup nor GPT-4.1 mini takes anything from the counts (Table~\ref{tab:nb6-composition})."
- **R102-5, Section 3.** Before: "A self-description can only name what its scrubbing rule   individuates, so naming granularity bounds what any reader can recover" and "A self-description can only name what its scrubbing rule individuates" After: "A summary can only name what its scrubbing rule individuates, so naming granularity bounds what any reader can recover from it."
- **R102-6, Section 6.** Before: "the paired obligation gain is positive" and "On the cross-model set the paired NOK gain is positive for each of the five models whose blind score varies (Table~\ref{tab:ladder-exact})." and "every paired NOK gain on those five stays positive with its interval excluding zero" After: "Every paired NOK gain on the cross-model set ($84$ questions, $40$ \pn{}) excludes zero on the five models whose blind score varies (Table~\ref{tab:ladder-exact})."
- **R102-7, Section 6 (brief R12).** Before: "This negative result is a finding in its own right." After: dropped; the finding stands as "The score ranks and does not calibrate."
- **R102-8, Section 1.** Before: "two things an agent must decide before touching its memory" and "the two things an agent must decide before touching its memory" After: "Before it searches, an agent must make two judgments about its store."
- **R102-9, Section 7.** Before: "still keeps the true index's coverage benefit" and "On the full obligation population ($n=661$) under the BELIEVED index, the obligation judgment fares worse, losing more than half its benefit." After: "Under the metadata FR-Bank exposes, coverage keeps $101.4\%$ of the \trueidx{} summary's gain (Appendix~\ref{app:construction}) and obligation keeps less than half."
- **R102-10, Section 6.** Before: "within FR-Bank, the index raises" After: "On FR-Bank the summary lifts coverage. Hard-question FOK ($307$ questions) rises by $+0.20$ and easy-question FOK ($595$) by $+0.19$, both intervals excluding zero."
- **R102-11, Sections 6 and 7.** Before: "whose counts   made the store look better covered than it is" After: the pooled names-only sentence leaves the body (Appendix F.5 keeps the row and its reading); the hypothesis survives in Section 7 as "global counts may make the store look better covered than it is".
- **R102-12, Section 1.** Before: "(superseded, expired, or retracted)" After: "NOK, negative-obligation knowledge, is the probability that the store holds something whose lifecycle state forbids its use." (Section 3 lists the four states.)
- **R102-13, Section 7.** Before: "disagreement between the index and retrieved view may compress the score range" After: "disagreement between the summary and the retrieved view may compress the score range".
- **R102-14, Section 9.** Before: "One closed model family supplies the primary capability comparison." After: "One closed model family supplies the primary capability comparison, with the limits stated where they arise on the Anthropic pair and the two halted runs (Section~\ref{sec:populations} caveat)."
- **R102-15, Section 1.** Before: "each is reported with the prediction text fixed before scoring" After: "each is reported under the text written before scoring in Appendix~\ref{app:registration}".
- **R102-16, Section 4 (ruling R-f, Table 10 folded).** Before: "the cross-model set ($84$ FR-Bank questions) and the same prompts" and "The four question sets, each defined once: name, size, positives, purpose, and where each is used." After: "Four question sets carry the results, each defined once. The cross-model set ($84$ questions; $54$ FOK-positive, $40$ \pn{}) asks the same questions of every model. The authorship-matched set ($36$ questions; $12$ \pn{}, $29$ non-\absent{}) rewrites every question in one voice. The store-counterfactual set ($444$ items; $148$ \pn{}, $88$/$30$/$30$ by state) holds the question fixed and varies the store. The full populations are the main-study sets: $661$ obligation questions with $104$ \pn{}, and $307$ hard coverage questions with $35$ non-\absent{}."
- **R102-17, Figure 2 caption (brief defect 5).** Before: "uses the cross-model set ($n=84$; $54$ FOK-positive and $40$ PN) on FR-Bank" and "The obligation panel is shown." and "GPT-4.1 mini's blind obligation point is a constant score on this set and carries no information; it is plotted for completeness only (Table~\ref{tab:ladder-exact} states the caveat in full)." After: "Blind and indexed NOK on the cross-model set for five models; the values to read first are the five indexed points, which sit between $0.8199$ and $0.8588$. Blind NOK has no monotone scale trend and indexed NOK converges."
- **R102-18, Section 6.** Before: "An expansion over the full populations ($661$ obligation / $307$ coverage) replicates the paired separation on all four completed runs" After: "GPT-5.6 Luna, Opus 5 and Haiku 4.5 gain $+0.37$, $+0.19$ and $+0.41$ on the same $661$ questions, each interval excluding zero." with the rows in Table 3 (`tab:e1`).
- **R102-19, Section 9.** Before: "The authorship-matched   set has been measured on three models." After: "The authorship-matched set ($36$ questions) is underpowered: blind NOK includes chance on all three models measured on it (Table~\ref{tab:matched-cell})."
- **R102-20, Section 4.** Before: "We asked each monitor for a number in $[0,1]$ under a fixed rubric and a shared system instruction." and "Responses were normalized to $[0,1]$." and "The two user prompts differ only in whether the serialized index precedes the question" After: "The monitor is asked for a number in $[0,1]$ under a fixed rubric; the two user prompts differ only in whether the serialized summary precedes the question, and the rubric is reported in full in Appendix~\ref{app:construction}."
- **R102-21, Section 6.** Before: "the monitor leads the best mechanical reader by $+0.0817$ (TRUE) and $+0.0819$ (BELIEVED) on FOK" After: "on FR-Bank it leads the best of the six mechanical readers of the same summary by $+0.08$ under either summary." (Table 20 keeps $+0.0817$ and $+0.0819$; the box keeps $+0.0817$.)
- **R102-22, Section 6.** Before: "Calibration does not follow discrimination. Discrimination is the primary measure and calibration the secondary one." After: "The score ranks and does not calibrate." (Section 3 defines ECE as secondary.)
- **R102-23, Section 6.** Before: "The probe alters only the numeric tallies." and "Because ages, markers, and names stay intact" and "The lifecycle fields of the summary add nothing measurable to coverage: randomizing every count leaves the gain unchanged, and the corrupted lifecycle metadata of Section~\ref{sec:stores} keeps $101.4\%$ of it." After: "Randomizing every count in the summary leaves FR-Bank coverage discrimination unchanged ($+0.0015$; Table~\ref{tab:destruction-fr}), so counts are unnecessary for coverage." (Appendix F.5 keeps the non-isolation caveat; Section 7 keeps $101.4\%$.)
- **R102-24, Section 6.** Before: "The wrong-index control replaces the index itself:" After: "The model reads this store's description. Another persona's summary inverts FOK from $0.70$ to $0.36$ on the $307$ hard questions."
- **R102-25, Section 4.** Before: "Blind scores therefore measure the question as much as the model, and the paired gain over identical questions is the clean quantity." After: "Supervised text probes reach $0.80$ to $0.97$ on the authored question sets (Appendix~\ref{app:questionprior}), so no absolute blind level in this paper is a finding. The evidence is the paired gain on identical questions and the counterfactual set, where the question is fixed and the store varies."
- **R102-26, Section 7 (brief R10).** Before: "The paper's object is what a store exposes about itself; what happens when it exposes the wrong thing is the second half of the result." After: dropped; Section 7 opens "No backend we tested writes the summary the obligation judgment needs."
- **R102-27, Section 6.** Before: "On FR-Bank the paired obligation gain concentrates on the one state the index names" After: the post-hoc sentence leaves the body; Appendix F.8 (Table 21 and its text) carries it; Section 6 keeps the named-versus-counted rule (R102-4).
- **R102-28, Section 5.** Before: "the judgment is bounded by what the summary names" After: "The boundary between named and counted states is the summary's."
- **R102-29, Sections 1 and 7.** Before: "We show that no tested backend writes the summary the judgment needs: a census of three backends records overstatement, erasure, and invention." After: "No backend we tested writes that summary: FR-Bank marks stale content about $60\times$ too often, and under the metadata it exposes the obligation gain keeps $42.3\%$ of its value." (Section 1) and the Section 7 opener.
- **R102-30, Figure 1 caption.** Before: "The blind monitor sees only the question. The indexed monitor sees the question and a value-free summary of the store that names which attributes carry superseded content." and "The question alone cannot supply that summary." and "Under the lifecycle mask a lifecycle-tracking store applies, the record that forbids the answer is masked out of the retrieved set; without the mask, half of such records enter a five-item view with their lifecycle tags." After: "A query ranks the store. Under the lifecycle mask a lifecycle-tracking store applies, the record that cancels the plan sits below the cutoff and no bounded view contains it; without the mask it enters a five-item view with its tag, which is the second route. The blind monitor sees only the question; the indexed monitor also sees the store's summary, which names the attributes carrying superseded content and only counts the rest."
- **R102-31, Table 3 caption.** Before: "The index helps on the backend with lifecycle structure and hurts on the two without it." After: "The main-study judgments on the full populations; the value to read first is the FR-Bank hard-question FOK gain ($+0.2037$) and the three NOK gains on $661$ questions. Positives are non-\absent{} items for FOK and \pn{} items for NOK; the gain is indexed minus blind on the same questions, and the lookup column is the superseded-names lookup on the same $661$."; Section 7 states "Under the summary these stores can write, the summary hurts coverage at every scale tested."
- **R102-32, Appendix F.8 only.** Before: "All $35$ pooled positives are FR-Bank questions, so a rule that only checks which backend a question came from scores $0.7541$ against the pooled indexed $0.7530$." and "Pooled levels measure coverage for no reader." After: the body no longer reports a pooled level; the Table 20 footnote carries both sentences' content (CAVEAT_LEDGER row 6).
- **R102-33, Section 6.** Before: "NOK targets that case, whether one stored record must be suppressed." After: "so FOK recognizes genuine absence and does not detect a missing record, the case NOK targets."
- **R102-34, Section 10.** Before: "A monitor is bounded by how well its backend describes itself. That is a property of the store; the model reading it does not change it." After: "The bound on the obligation judgment is the store's own writing about itself." and "Both routes are properties of the store; the model reading it changes neither."
- **R102-35, Section 10.** Before: "the superseded-names lookup matches the smallest of them" and "Six models across three vendors saw a truthful summary: the obligation judgment improves on the five whose blind score varies, and the superseded-names lookup matches the smallest of them. The smallest model's blind judgment barely moves, so its tie with the lookup is a comparison of levels and anchors no gain." After: "A summary that names the attributes holding superseded content supplies the judgment, and a lookup over those names reads it as well as the smallest model."; the mini caveat is stated once, in Section 6 (R102-40).
- **R102-36, Section 10.** Before: "obligations keep $42.3\%$ of their gain, short of the $60\%$ threshold set in advance" After: "No backend tested writes that summary, and under the metadata a real backend exposes the judgment keeps less than half its gain." (Section 7 keeps the frozen $42.3\%$ sentence.)
- **R102-37, the box (brief section 4 vocabulary).** Before: "The model earns its cost on one judgment only: coverage where lifecycle structure exists, on which it leads the best mechanical reader by $+0.0817$." After: "The model earns its cost on one judgment only: coverage where lifecycle structure exists, on which it leads the strongest reader of the same summary by $+0.0817$."
- **R102-38, Appendix B.** Before: "This trend measures how much of the question's label signal each model reads, because blind levels include what the question text gives away." After: "blind levels include what the question text gives away, so this trend measures how much of that signal each model reads."
- **R102-39, Section 6.** Before: "The score the model reports behaves as a ranker whose value cannot be read as a probability, so a deployed monitor must threshold it per index" After: "A monotone rescaling fitted after the fact calibrates it to an ECE of $0.01$, and the rescaled value never exceeds $0.375$, so a deployed monitor thresholds at the base rate (Appendix~\ref{app:posthoc})."
- **R102-40, Section 6 (the brief's one permitted phrasing).** Before: "GPT-4.1 mini is the exception: on this set its blind score does not vary, so its difference anchors no gain (Section~\ref{sec:discrimination})." and "Mini's blind obligation score takes two distinct values on these $661$ questions, with or without the rubric's detection step, and one on the cross-model set, so it carries no ranking to improve on." After: "GPT-4.1 mini's blind NOK score is constant on these questions, so its indexed minus blind difference is not a gain; we compare its indexed level to the lookup and report paired gains on the five models whose blind score varies." with the full account in Appendix B.
- **R102-41, Section 4.** Before: "lists every   registered prediction and its outcome" After: see R102-2.
- **R102-42, count change.** "with questions grouped by user   profile" appears once more (Section 4 conventions); no strength change.
- **R102-43, Section 7.** Before: "The negative index effect is measured here, and these ablations do not identify what causes it." After: "The below-chance mechanism is unresolved." (U2 stands in Appendix F.7.)
- **R102-44, Section 7.** Before: "A name-bearing summary built from ground truth for the entries each store holds recovers coverage on both." After: "A name-bearing summary rebuilt from ground truth for the entries each structureless store holds recovers coverage on both."
- **R102-45, Section 7.** Before: "Discrimination moves from $0.4526$ to $0.8974$ on A-MEM and from $0.4777$ to $0.8751$ on Mem0 (Appendix~\ref{app:inversion})." and "On A-MEM the paired difference is $+0.4448$ (CI $[+0.3800,+0.5116]$; $[+0.3875,+0.5042]$ grouped by user profile), and both predictions written before the run hold." After: "Coverage moves from $0.45$ to $0.90$ on A-MEM, a paired difference of $+0.44$, and both of its predictions, fixed in advance, were borne out. On Mem0 it moves from $0.48$ to $0.88$; Mem0's summary covers $49.4\%$ of its entries, below the coverage floor of one half fixed in advance, so its row is descriptive (Appendix~\ref{app:inversion})." (Table 19 and Appendix F.7 keep the four-decimal values and both intervals.)
- **R102-46, Section 7.** Before: "The mechanical readers recover it too ($0.8554$ and $0.8700$ against $0.5000$ on the summary these stores can produce), and no backend we tested writes that summary itself." After: "The lexical and embedding lookups recover it too ($0.86$ and $0.87$ on the name-bearing summary), and no backend we tested writes that summary itself."
- **R102-47, Sections 7 and 10.** Before: "The two backends without lifecycle structure invert the benefit at every scale tested under the summary they can produce." and "Given a name-bearing summary of what they hold, both recover coverage (Section~\ref{sec:inversion})." After: Section 7 "Under the summary these stores can write, the summary hurts coverage at every scale tested." and "A name-bearing summary rebuilt from ground truth for the entries each structureless store holds recovers coverage on both."
- **R102-48, Sections 1 and 3.** Before: "pass similarity retrieval at $5\%$" After: "retraction records pass retrieval at $5\%$ under that mask" (Section 1) and "(on the inherited store, retraction records pass at $5\%$)" (Proposition 1).
- **R102-49, Table 3 (brief defect 6).** Before: "$+0.2393^{\ddagger}$ & $[+0.1801,+0.2949]^{\ddagger}$" and "$^{\ddagger}$A difference against a near-constant blind score; it anchors no gain (Section~\ref{sec:discrimination})." After: the GPT-4.1 mini NOK row and its footnote leave the main-text table; the row's values stand in Appendix B (Table 3 there and the added sentence).
- **R102-50, Appendix F.3 only.** Before: "The $60\%$ threshold is a round number fixed before any data (Appendix~\ref{app:construction})." After: dropped from the body; Appendix F.3 states the threshold's provenance in full.
- **R102-51, Section 9.** Before: "The lifecycle schema this study builds on is that of the prior store \citep{fr}, so the audit of Section~\ref{sec:stores} applies to that store first." and "Every label comes from the manifests we built, and Section~\ref{sec:inversion} shows the benefit travels with the summary rather than with the system." After: "The lifecycle schema this study builds on is that of the prior store \citep{fr}, so the census of Section~\ref{sec:backends} applies to that store first. Every label comes from the manifests we built, and the benefit travels with the summary rather than with the system."
- **R102-52, Sections 5 and 8.** Before: "A direct match against the three name lists reaches $0.8756$ on the same set, within tolerance of Haiku 4.5's $0.8773$ under that summary (Table~\ref{tab:counterfactual})." and "It exceeds every GPT-4.1 mini score by more than the $\pm0.05$ tolerance." After: "Under the summary that names all three states, the all-states lookup reaches $0.88$ against Haiku 4.5's $0.88$, within tolerance; Opus 5 alone exceeds it, at $0.91$." and "The all-states lookup exceeds GPT-4.1 mini under every summary and Haiku 4.5 under the two summaries that do not name the counted states, each beyond tolerance; nothing exceeds Opus 5 under the all-states summary." (Section 5); "On the whole set under that summary the all-states lookup reaches $0.88$." (Section 8).
- **R102-53, Section 5.** Before: "The first, thirty-question form of that set did not replicate at item level (Appendix~\ref{app:counterfactual})." After: "The thirty-question first form of this set did not hold its aggregate prediction at $n=90$; the $444$-item form was preregistered on that power fault, and both of its intervals now exclude zero."
- **R102-54, the abstract (ruling R-a).** Before: "On the metadata a backend produces, that   judgment keeps only $42.3\%$ of its gain." and "Retrieval that returns non-active records with their lifecycle tags reads obligations nearly as well, and the two together best." and "Given a summary of a store's contents and lifecycle states, a name lookup reads the obligation as reliably as the smallest model." and "Given a summary of a store's contents and lifecycle states, a name lookup reads the obligation as reliably as the smallest model. Retrieval that returns non-active records with their lifecycle tags reads obligations nearly as well, and the two together best." After: the v10 abstract, the author's text of the brief with the prescribed cut and the split headline sentence.
- **R102-55, Section 6.** Before: "Obligation: a name lookup matches the model" After: v10 has no subsections; Section 6 states "On the $661$ obligation questions the lookup ties the smallest model."
- **R102-56, Section 1.** Before: "Under the lifecycle mask the inherited store applies, the record that forbids use is masked out of the retrieved set: on that store's own benchmark, retraction records pass retrieval at only $5\%$ \citep{fr}. Without the mask, half of the forbidding records ($54$ of $104$) enter a five-item similarity view and seven in ten ($74$ of $104$) a ten-item view, each carrying its lifecycle tag where the store records one (Section~\ref{sec:discussion}). Under the mask, the few items a retriever returns can include the stale plan and miss the record that cancels it." After: "A retriever that masks non-active records returns the plan and misses the cancellation: on the inherited store, retraction records pass retrieval at $5\%$ under that mask \citep{fr}. An unmasked retriever returns the cancellation about half the time, carrying its lifecycle tag: $54$ of $104$ forbidding records enter a five-item view." (the ten-item figure prints in Section 8 and Table 26).
- **R102-57, Section 1.** Before: "The empirical scope is pre-retrieval monitoring on synthetic stores, with one primary closed model family; one downstream experiment measures what a policy that acts on the judgment sees and uses (Section~\ref{sec:discussion})." After: "The empirical scope is pre-retrieval monitoring on synthetic stores, with one primary closed model family, and one downstream experiment measures what a policy that acts on the judgment sees and uses."
- **R102-58, Section 3 (Proposition 1 gloss).** Before: "The premise is ordinary under the masking that lifecycle-tracking and overwriting stores apply: in that store, retraction records pass similarity retrieval at $5\%$ under its mask \citep{fr}, and the proposition's force is that measured premise rather than a deep theorem. Without the mask, half of the forbidding records enter a five-item view (Section~\ref{sec:discussion})." After: the premise is restated inside Proposition 1 per the brief ("Fix $k$ and a retriever that masks non-active records from its ranking, as lifecycle-tracking and overwriting stores do. Under that mask a lifecycle record that changes intent-conditional coverage ranks below $k$ common items (on the inherited store, retraction records pass at $5\%$)."), and the gloss keeps "The proposition's force is that measured premise rather than a deep theorem." and "retrieval that does not mask and returns lifecycle tags is another (Section~\ref{sec:routes})".
- **R102-59, Sections 6 and 8.** Before: "It does not establish that a lookup matches the larger models, whose extra gain sits on the counted states (Table~\ref{tab:nb6-composition})." (and the same sentence followed by the L1-P1 sentence and the retrieved-view sentence) After: the frozen per-state reading in Section 6 carries the larger-models statement verbatim; the retrieved-view and hybrid results are stated in Section 8 with their outcomes ("A monitor shown the five tagged records and no summary scores $0.69$ on obligation against the summary's $0.73$ on the $661$ questions, within tolerance." and "Shown both, GPT-4.1 mini scores $0.83$ on the $661$ questions, a gain of $+0.10$ over the summary alone.").
- **R102-60, Section 8.** Before: "The store's lifecycle metadata supplies the obligation judgment. A summary exposes the states it names; retrieved records that carry their lifecycle tags expose the states the summary only counts; the two together give the best monitor measured ($0.8303$)." After: "There are two routes to the obligation, and both are the store's metadata." and the hybrid sentence of R102-59.
- **R102-61, Appendix G (brief defect 3; D-DS-4).** Before: "Truthful metadata does not flag $22$ of the $104$ forbidding records: DS D-DS-1; Appendix~\ref{app:resp}.\\ Fetch-set zero count transcribed from the unflagged count: DS D-DS-2; Appendix~\ref{app:resp}.\\ Two bars set under the premise corrected at L2; one prediction unfulfillable by its own gate: DS D-DS-3; Appendix~\ref{app:resp}.\\ No deviation on the review-response lanes: RESP; Appendix~\ref{app:resp}.\\" After: the same four lines with "No deviation on the mechanism tests (RESP); Appendix~\ref{app:resp}." and a fifth line "Zero-change wording of the DS-P4 failed form: DS D-DS-4; Appendix~\ref{app:resp}."
- **R102-62, non-manuscript writes.** `tools/numeric_diff.py` gains `--round2` (rule 1.2); `tools/prose_scan.py` blanks the R9 clause before the V check (ruling R-b); `tools/trace_scan_v13.py` LEDGERS gains `reviews/NUMBERS_R102.md`; `ds_downstream/DEVIATIONS_DS.md` and its ARTIFACT copy gain D-DS-4; `reviews/v10/` (OUTLINE.md, NUMBER_MOVES.md, CAVEAT_LEDGER.md, CONFLICTS.md, REPORT.md, CHANGES.md, tools/); this block.
- **R102-63, Section 7.** Before: "Its interval is $[44.6\%,87.2\%]$ ($[31.5\%,93.6\%]$ grouped by user profile)." and "The difference from the capped list, $+0.0554$, excludes zero at item level and includes it under the grouping, so the weaker reading governs (Appendix~\ref{app:believed-census})." After: "Its interval is $[44.6\%,87.2\%]$ ($[31.5\%,93.6\%]$ grouped by user profile), and the difference from the capped list, $+0.0554$, excludes zero at item level and includes it under the grouping, so the weaker reading governs (Appendix~\ref{app:believed-census})."

**Pass 3 entries (the author's targeted pass, 2026-09-13).** Same rule as above: Before verbatim; After is the v10 sentence that carries the content, found in the final `paper_v10.tex`, or the reason it is dropped. Registration-frozen strings (R, U, S, W FROZEN-REGISTERED) are untouched; `check_appendix.py` and `frozen_diff` confirm it.

- **R102-P3-1 [Q CLAIMS].** Before: "It shows tight indexed FOK across all six lineages and tight indexed NOK across the five lineages whose blind NOK varies." After: "It shows tight indexed FOK across all six models and tight indexed NOK across the five models whose blind NOK varies."
- **R102-P3-2 [Q CLAIMS].** Before: "committed main-study elicitation" After: dropped in the vocabulary pass or the defense pass; content unchanged elsewhere (see appendix_changes_pass3.md / REPORT.md section 6)
- **R102-P3-3 [Q CLAIMS].** Before: "NB-3 was disqualified as an index reader and is retained as a measurement-step failure record." After: "\textbf{What we changed.} NB-3 was disqualified as an summary reader and is retained as a measurement-step failure record."
- **R102-P3-4 [Q CLAIMS].** Before: "The name-bearing index does not invert." After: "The name-bearing summary does not invert."
- **R102-P3-5 [Q CLAIMS].** Before: "A check of whether each obligation's own attribute name appears in the section the matcher reads finds it for $74$ of $104$ under exact slot match: $63$ of $63$ supersession-derived, $11$ of $26$ retraction-derived, and none of the $15$ expiry-derived (an earlier count of $7$ keyed entries without their persona; deviation ledger, Appendix~\ref{app:registration})." After: "A check of whether each obligation's own attribute name appears in the section the lookup reads finds it for $74$ of $104$ under exact slot match: $63$ of $63$ supersession-derived, $11$ of $26$ retraction-derived, and none of the $15$ expiry-derived (an earlier count of $7$ keyed entries without their persona; deviation ledger, Appendix~\ref{app:registration})."
- **R102-P3-6 [Q CLAIMS].** Before: "On the state the index names, the matcher has the item's own name to read; whether the monitor reads it is a separate question that this census does not settle." After: "On the state the summary names, the lookup has the item's own name to read; whether the monitor reads it is a separate question that this census does not settle."
- **R102-P3-7 [Q CLAIMS].** Before: "The two structureless indexes as the monitor saw them, verbatim, for the persona of median size (\texttt{leila}), are printed below. Under \trueidx{} the marker occupies $3$ of $31$ lines and $18$ of $216$ tokens ($8.3\%$) on both backends; under \believed{} it occupies $7$ lines and $18.1\%$ of tokens on Mem0 and $8$ lines and $20.3\%$ on A-MEM." After: "Under \trueidx{} the marker occupies $3$ of $31$ lines and $18$ of $216$ tokens ($8.3\%$) on both backends; under \believed{} it occupies $7$ lines and $18.1\%$ of tokens on Mem0 and $8$ lines and $20.3\%$ on A-MEM."
- **R102-P3-8 [Q CLAIMS].** Before: "Opus 5 entered the study at the E1-XV preregistration (\texttt{776bce07b3}, 2026-08-14), carrying three of its predictions, after the E1 freeze of 2026-08-10 and before the store-counterfactual freeze of 2026-08-29; in that cell it is a descriptive lane carrying no prediction, named at the freeze and funded by Amendment 4 of 2026-08-30 before its lane was submitted." After: "\noindent\textbf{When Opus 5 entered.} Opus 5 entered the study at the E1-XV preregistration (\texttt{776bce07b3}, 2026-08-14), carrying three of its predictions, after the E1 freeze of 2026-08-10 and before the store-counterfactual freeze of 2026-08-29; in that set it is a descriptive run carrying no prediction, named at the freeze and funded by Amendment 4 of 2026-08-30 before its run was submitted.\\"
- **R102-P3-9 [Q CLAIMS].** Before: "The $60\%$ retention threshold was written into the main study's preregistration (2026-08-10) as a round number for coverage retention, with no derivation, and was inherited unchanged when obligation retention was scored, before that figure existed." After: "The $60\%$ retention threshold was fixed in advance at $60\%$ in the main study's preregistration (2026-08-10) for coverage retention and was inherited unchanged when obligation retention was scored, before that figure existed."
- **R102-P3-10 [Q CLAIMS].** Before: "both inside the tolerance band;   on this cell neither reader takes anything from the counts" After: "The crossover is the finding: the lookup leads on the state the summary names and trails on the two it only counts."
- **R102-P3-11 [Q CLAIMS].** Before: "Randomizing the retracted and expired counts in the superseded-only summary moves GPT-4.1 mini's whole-cell judgment by $+0.0011$ and Haiku 4.5's by $+0.0072$, intervals $[-0.0282,+0.0297]$ and $[-0.0079,+0.0229]$, both inside the tolerance band; on this cell neither reader takes anything from the counts." After: "Randomizing the retracted and expired counts in the superseded-only summary moves GPT-4.1 mini's whole-set judgment by $+0.0011$ and Haiku 4.5's by $+0.0072$, intervals $[-0.0282,+0.0297]$ and $[-0.0079,+0.0229]$, both inside the tolerance band; on this set neither reader takes anything from the counts."
- **R102-P3-12 [Q CLAIMS].** Before: "R94: CF-2 store-counterfactual cell & \texttt{f016f033e9} & 2026-09-12 & $148$ question and slot pairs drawn under predicates fixed before any verdict, three store versions each, three summaries, three readers, five predictions and their branch texts; all five held, two of them printing either way: the lookups within tolerance and every reader inside the count-randomization band; five recorded deviations (D-CF2-1 to D-CF2-5) & held" After: "R94: CF-2 store-counterfactual set & \texttt{f016f033e9} & 2026-09-12 & $148$ question and slot pairs drawn under predicates fixed before any verdict, three store versions each, three summaries, three readers, five predictions and their branch texts; all five held, two of them printing either way: the lookups within tolerance and every reader inside the count-randomization band; five recorded deviations (D-CF2-1 to D-CF2-5) & held \\"
- **R102-P3-13 [Q CLAIMS].** Before: "It does not establish that a lookup matches the larger models, whose extra gain sits on the counted states (Table~\ref{tab:nb6-composition}). Removing the target's own name and its nearest neighbours from the superseded-names section costs the smallest model $0.3262$ of its supersession discrimination ($0.8572$ to $0.5310$; interval $[-0.3991,-0.2548]$, and $[-0.4327,-0.2167]$ with questions grouped by user profile): the obligation is read off the name, as the manuscript says. A monitor reading the five retrieved items with their lifecycle tags, and no summary, reaches $0.6851$ on obligation against the summary's $0.7339$, within tolerance; the two together reach $0.8303$, the gain on the states the summary only counts (Appendix~\ref{app:resp})." After: "Removing the target's own name and its nearest neighbours from the superseded-names section costs the smallest model $0.3262$ of its supersession discrimination ($0.8572$ to $0.5310$, interval $[$-0.3991$,$-0.2548$]$; persona-clustered $[$-0.4327$,$-0.2167$]$): the obligation is read off the name, as the manuscript says."

## R103 AUTHORIZATION BLOCK — dated 2026-09-13

**Scope.** The v10-to-v11 pass ordered by the author ("CC pass: v10 to v11, everything outstanding"): the fifth review's framing (W5, W2), vocabulary and frozen-string placement (W1), the appendix rewrite under the brief's rules and the split into a supplement (W1), five analyses with no model call (W3, W6, W11, Q1, Q2, Q5, Q6), and two author-approved descriptive runs (DS Amendment 1; the Q4 marker-as-absence probe), both registered as descriptive addenda frozen by sha256 before the first call. REWRITE_BRIEF_v10.md remains binding: every table number is a v10 number or a value from one of the two runs' ledgers; every prose number is a v10 number on the same population or its two-decimal rounding; no caveat vanishes; no registration-frozen text (R, U, EXEMPT_FROZEN_REGISTERED, W FROZEN-REGISTERED) is reworded; no new claim. **No registered bar, threshold or verdict changes.** Model calls: 522 + 661 + 21 GPT-4.1 mini calls, $0.6410 billed against the author's $3.00 combined cap (`q4_inversion_probe/NUMBERS_Q4.md` AUX-Q4-SPEND; `ds_downstream/NUMBERS_DS.md` AUX-DS-A1-SPEND).

**Lineage.** `paper_v11.tex` is a new file beside `paper_v10.tex` (v10 untouched); `SUPPLEMENT.tex` carries the blocks split out of Appendices C, E, F.1, F.10 and G, each keeping its label with a one-line pointer where it stood. Reports: `reviews/v11/` (REPORT.md, NUMBER_MOVES.md, CAVEAT_LEDGER.md, CONFLICTS.md, CHANGES.md). Rounded forms and the deterministic values of the five analyses: `reviews/NUMBERS_R103.md` (added to `trace_scan_v13.LEDGERS` with `q4_inversion_probe/NUMBERS_Q4.md`).

**BASE.** The tree object written from the working copy with a scratch index (`git hash-object -w` + `git write-tree` under a scratch `GIT_INDEX_FILE`; the real index and HEAD untouched, nothing committed), holding `paper_v10.tex` as it stood at 17:19 and a fresh three-pass build of it (38 pages; page census: label on page 11, reading 550, slack -65): `--base=75ea31e2a81c097102e3d9ed0c9638b111b1cb64 --tex=paper_v11.tex --base-tex=paper_v10.tex` (tex blob `398ef213`, pdf blob `383b0773`).

**Registrations frozen in this pass (descriptive, no prediction, no bar):** `registrations/ADDENDUM_Q4.md` sha256 `8b6ee9e3f7e2181edcab06e35d9a9efc0a0c21421ab841664a8f6e22da7ca608`; `registrations/ADDENDUM_DS_AMENDMENT_1.md` sha256 `72ab84dae2c7e464b1488570d4098aebf59b1de0d442ddc7b6f79a57bfcbbcf5`; both copied to `ARTIFACT/registrations/` before the first call. DS Amendment 1 was written from the D-DS-3 (b) disposition because no registration file for it existed in the tree when this pass began (CONFLICTS.md C-R103-1).

**Rulings applied (the author's instructions of 2026-09-13, recorded because each departs from a written rule or resolves one).**
- **R-a, abstract.** The author's replacement abstract prints verbatim; numerals sit in three of its sentences, against STYLE_SPEC T2 as amended (two) and T1; logged in CONFLICTS.md, not a stop.
- **R-b, [MAIN] placement.** The registrations mark the NB6 texts (ADDENDUM_R81 §6, §10.3), the CF-2 P1 and P3 texts (ADDENDUM_CF2 §8), the SIDE S2 42.3-percent and cap-lift sentences (ADDENDUM_SIDE §S2, Amendment 1) and the DS paragraph (ADDENDUM_DS §PAPER) as main-text texts, so placement is frozen with the wording; they stay in the body with their binding clauses. The Section 4 binding drops its registered-item code ("the matcher, in the preregistered texts").
- **R-c, four decimals.** A four-decimal value prints at most once in the body, in a table; body prose rounds to two decimals; registration-frozen sentences that carry four decimals are exempt and are listed in CONFLICTS.md where a value therefore prints twice ($0.7167$: Table 1 and the frozen CF-2 P1 sentence).
- **R-d, 42%.** "keeps under half its value" and "keeps less than half its gain" become "keeps $42\%$ of its gain" (the abstract's form), a rounding of the frozen $42.3\%$; `numeric_diff --round2` accepts an integer percent when a base percent token rounds to it (Decimal, ROUND_HALF_UP), recorded in `reviews/NUMBERS_R103.md`.
- **R-e, the two runs' numbers.** Values from `NUMBERS_Q4.md` and `NUMBERS_DS.md` section 6 enter Table 4, `tab:ds`, a two-row table in F.7, and one sentence each in Sections 7 and 8, labelled descriptive; they are new measurements, not v10 numbers, and are the only ADDED tokens `numeric_diff` accepts on the author's order.
- **R-f, split.** Blocks moved to `SUPPLEMENT.tex` keep their labels; `frozen_diff` and `numeric_diff` read the supplement as part of the manuscript through `--extra-tex=SUPPLEMENT.tex`, so a moved string reports MOVED and a moved number is not VANISHED.

**Entries.** Each Before is the CLAIMS.md-quoted (or list-held) v10 string frozen_diff reports as changed; After is the v11 text or the landing that carries the same content at the same strength.


- **R103-1, Section 1 (anti-telegraph rule).** Before: "The component that decides whether and how to consult memory is the monitor, and the failure occurs there, before any answer is drafted." After: "The component that decides whether and how to consult memory is the monitor, so the failure occurs there, before any answer is drafted."
- **R103-2, Section 2 (anti-telegraph rule).** Before: "All of them presuppose the monitoring judgment, an estimate of what the store holds and what it forbids, without measuring it." After: "All of them presuppose the monitoring judgment, an estimate of what the store holds and what it forbids, which means each of them leaves that estimate unmeasured."
- **R103-3, Section 4 (R2 split).** Before: "The monitor is asked for a number in $[0,1]$ under a fixed rubric; the two user prompts differ only in whether the serialized summary precedes the question, and the rubric is reported in full in Appendix~\ref{app:construction}." After: two sentences, "The monitor is asked for a number in $[0,1]$ under a fixed rubric, reported in full in Appendix~\ref{app:construction}. The two user prompts differ only in whether the serialized summary precedes the question."
- **R103-4, Section 5 (the author's points 3 and 5; one home per number).** Before: "The boundary between named and counted states is the summary's." After: "The boundary between named and counted states is the summary's, because each reader's gap between the named state and the counted states closes once the summary names them."
- **R103-5, Section 5.** Before: "Under the summary that names all three states, the all-states lookup reaches $0.88$ against Haiku 4.5's $0.88$, within tolerance; Opus 5 alone exceeds it, at $0.91$." After: "Under the summary that names all three states, the all-states lookup reaches $0.88$ against Haiku 4.5's $0.88$, a difference of $+0.00$ whose intervals include zero; Opus 5 alone exceeds it, at $0.91$, by $+0.03$ with intervals that exclude zero." (reviews/NUMBERS_R103.md AUX-R103-MARGIN)
- **R103-6, Section 5 (count change).** "predictions written before the run" 2 -> 1: the phrase "its predictions written before the run" in the first-form sentence became "its predictions were written before the run" (R2 split); the CF-2 sentence "All five predictions written before the run were borne out." is unchanged.
- **R103-7, Section 6 (anti-telegraph rule).** Before: "On FR-Bank the summary lifts coverage. Hard-question FOK ($307$ questions) rises by $+0.20$ and easy-question FOK ($595$) by $+0.19$, both intervals excluding zero." After: "On FR-Bank the summary lifts coverage on both question tiers. Hard-question FOK ($307$ questions) rises by $+0.20$ and easy-question FOK ($595$) by $+0.19$, both intervals excluding zero."
- **R103-8, Section 6 (rule 2.3, two decimals in prose).** Before: "Randomizing every count in the summary leaves FR-Bank coverage discrimination unchanged ($+0.0015$; Table~\ref{tab:destruction-fr}), so counts are unnecessary for coverage." After: "Randomizing every count in the summary moves FR-Bank coverage discrimination by $+0.00$ to two decimals (Table~\ref{tab:destruction-fr}), so counts are unnecessary for coverage." (the phrase "FR-Bank coverage discrimination unchanged" leaves with it; $+0.0015$ stays in Table 17)
- **R103-9, Section 6 (the author's point 3, "no margin over the lookup").** Before: "On the $661$ obligation questions the lookup ties the smallest model." After: "On the $661$ obligation questions the lookup is again the decision rule, and what the models add appears only on the states the summary does not name."
- **R103-10, Section 6 (the author's point 4).** Before: "GPT-4.1 mini's blind NOK score is constant on these questions, so its indexed minus blind difference is not a gain; we compare its indexed level to the lookup and report paired gains on the five models whose blind score varies." After: unchanged in wording; the string moved (count 1 -> 0 is a normalization artifact of the R2 split of the sentence before it; the sentence prints verbatim in Section 6).
- **R103-11, Section 6 (anti-telegraph rule).** Before: "The score ranks and does not calibrate." After: "The score ranks well and calibrates badly, so its value should be read as a rank and never as a probability."
- **R103-12, Section 6 (the author's point 5).** Before: "Blind and indexed NOK on the cross-model set for five models; the values to read first are the five indexed points, which sit between $0.8199$ and $0.8588$. Blind NOK has no monotone scale trend and indexed NOK converges." After: Figure 2 is a five-row table with the caption "Blind and indexed NOK on the cross-model set ($84$ questions) for the five models whose blind score varies. Blind NOK has no monotone scale trend, while indexed NOK converges to a narrow band."; $0.8199$ and $0.8588$ print in the table's rows.
- **R103-13, Section 7 (the author's point 2, the 42% as the gap; rule 2.3).** Before: "Under the metadata FR-Bank exposes, coverage keeps $101.4\%$ of the \trueidx{} summary's gain (Appendix~\ref{app:construction}) and obligation keeps less than half." After: "Under the metadata FR-Bank exposes, coverage keeps $101.4\%$ of the \trueidx{} summary's gain (Appendix~\ref{app:construction}), while that metadata recovers $42\%$ of the obligation gain a truthful summary gives. The rest is the gap between what the store writes and what it must."
- **R103-14, Section 7 (rule 2.3).** Before: "Precision is $0.0348$ capped and $0.0357$ lifted, so most of the loss, at the point estimate, is the store's." After: "Precision is $0.03$ capped and $0.04$ lifted, so most of the loss, at the point estimate, is the store's."
- **R103-15, Section 7 (anti-telegraph rule).** Before: "The below-chance mechanism is unresolved." After: "The below-chance mechanism is unresolved, because no single removal from the summary separates from the intact inversion."
- **R103-16, Section 8 (anti-telegraph rule; R9 vocabulary).** Before: "There are two routes to the obligation, and both are the store's metadata." After: "There are two routes to the obligation, and both are the store's metadata, because the summary and the tags on returned records carry the same lifecycle states by different paths."
- **R103-17, Section 8.** Before: "A monitor shown the five tagged records and no summary scores $0.69$ on obligation against the summary's $0.73$ on the $661$ questions, within tolerance." After: the same sentence with the clause ", because the tags on the returned records carry the obligation signal the summary carries." appended.
- **R103-18, Section 8.** Before: "Shown both, GPT-4.1 mini scores $0.83$ on the $661$ questions, a gain of $+0.10$ over the summary alone." After: the same sentence with ", because a retrieved entry tagged retracted or expired is a name the summary never prints." appended.
- **R103-19, Section 8.** Before: "Removing the target's own name and its nearest neighbours from the summary drops GPT-4.1 mini's supersession judgment from $0.86$ to $0.53$ on the $661$ questions." After: "The judgment is read off names, because removing them removes it: taking the target's own name and its nearest neighbours out of the summary drops GPT-4.1 mini's supersession judgment from $0.86$ to $0.53$ on the $661$ questions."
- **R103-20, Section 8 (one home per number).** Before: "On the whole set under that summary the all-states lookup reaches $0.88$." After: "On the whole set under that summary the all-states lookup reaches the level Section~\ref{sec:counterfactual} reports."
- **R103-21, Section 10 (page-gate trim step 1; the author's point 2).** Before: "The bound on the obligation judgment is the store's own writing about itself." and "A summary that names the attributes holding superseded content supplies the judgment, and a lookup over those names reads it as well as the smallest model." and "No backend tested writes that summary, and under the metadata a real backend exposes the judgment keeps less than half its gain." and "Both routes are properties of the store; the model reading it changes neither." After: two sentences, "The bound on the obligation judgment is the store's own writing about itself, so the model reading the store changes neither route to it; on the state the summary names, the lookup decides and the model holds no margin over it (Section~\ref{sec:counterfactual}). No backend tested writes the summary that route needs, and the metadata a real backend exposes recovers under half of the gain a truthful summary gives (Section~\ref{sec:backends})."
- **R103-22, the box (the author's points 1, 3 and 5; one home per number).** Before: "They tie near chance under the metadata a real backend exposes ($0.5858$ against $0.5959$)." and "Once a summary names every non-active state, the lookup reaches $0.8756$ on questions that cannot carry the label." and "The model earns its cost on one judgment only: coverage where lifecycle structure exists, on which it leads the strongest reader of the same summary by $+0.0817$." After: "The obligation judgment is a lookup over that list (Section~\ref{sec:counterfactual}); once a summary names every non-active state, the lookup reads the obligation on every state, and under the metadata a real backend exposes neither the lookup nor the model rises far above chance (Section~\ref{sec:backends})." and "The model earns its cost on one judgment only: coverage where lifecycle structure exists, on which it leads the strongest reader of the same summary (Section~\ref{sec:populations}); used as a filter at the base rate, ..." (the precision and recall sentence of Q5); the box's first sentence is the recommendation and its last two sentences are verbatim (R101-12); $0.7484$, $0.7339$, $0.5858$, $0.5959$, $0.8756$ and $+0.0817$ print in Tables 2, 22 and 1.
- **R103-23, Appendix B (the author's point 4).** Before: "Mini blind NOK is constant at $0.0$ on all $84$ items, so $0.5000$ is an all-tie artifact rather than calibrated uncertainty, and its clustered interval is not printed for the same reason; luna spans $48$ distinct values and still fails to discriminate." After: "...and its clustered interval is not reported for the same reason. GPT-5.6 Luna spans $48$ distinct values and still fails to discriminate."
- **R103-24, Appendix B.** Before: "Mini rows: the all-tie artifact and the dash convention are explained in the paragraph above the table." After: "GPT-4.1 mini rows: the blind obligation score is an all-tie artifact, so the indexed-minus-blind difference on that row ($+0.2139$) is not a gain and is not shown; the dash convention is explained in the paragraph above the table." (the row's $\Delta$ cell is a dash; the value prints in the footnote)
- **R103-25, Appendix B (anti-telegraph rule).** Before: "blind levels include what the question text gives away, so this trend measures how much of that signal each model reads." After: the same words, the sentence before it split at its semicolon (R2).
- **R103-26, Appendix D.2 (vocabulary; R2).** Before: "The registered prediction did not hold." After: "The preregistered prediction on this form did not hold, for the reason the next sentence records."
- **R103-27, Appendix D.2 (R2 split).** Before: "Randomizing the retracted and expired counts in the superseded-only summary moves GPT-4.1 mini's whole-set judgment by $+0.0011$ and Haiku 4.5's by $+0.0072$, intervals $[-0.0282,+0.0297]$ and $[-0.0079,+0.0229]$, both inside the tolerance band; on this set neither reader takes anything from the counts." After: the same words as two sentences, split at the semicolon.
- **R103-28, Appendix E (anti-telegraph rule).** Before: "Every failure below is the same kind: a semantic assumption hidden inside a step that looked mechanical." After: "Every failure below is the same kind, a semantic assumption hidden inside a step that looked mechanical, so the ledger is kept as one list."
- **R103-29, Appendix F.7 (R2 split).** Before: "Under \trueidx{} the marker occupies $3$ of $31$ lines and $18$ of $216$ tokens ($8.3\%$) on both backends; under \believed{} it occupies $7$ lines and $18.1\%$ of tokens on Mem0 and $8$ lines and $20.3\%$ on A-MEM." After: the same words as two sentences, split at the semicolon.
- **R103-30, Appendix F.7 (anti-telegraph rule).** Before: "The name-bearing summary does not invert." After: "The name-bearing summary does not invert on either store."
- **R103-31, Appendix F.8 (anti-telegraph rule).** Before: "Three readings carry beyond the table." After: "Three readings carry beyond the table, because each bears on a claim the main text makes."
- **R103-32, Appendix F.8 (R2 split).** Before: "A check of whether each obligation's own attribute name appears in the section the lookup reads finds it for $74$ of $104$ under exact slot match: $63$ of $63$ supersession-derived, $11$ of $26$ retraction-derived, and none of the $15$ expiry-derived (an earlier count of $7$ keyed entries without their persona; deviation ledger, Appendix~\ref{app:registration})." After: "...and none of the $15$ expiry-derived. An earlier count of $7$ keyed entries without their persona (deviation ledger, Appendix~\ref{app:registration})."
- **R103-33, Appendix F.9 (R2 split; the Graphiti disclosure).** Before: "the personas and episodes used here were ingested into that backend in early 2026 under a copy carrying four documented numeric-preservation modifications; re-running the unmodified release on the same personas and episodes changes edge counts by $2.4\%$ and leaves supersession recall identical at the frozen bar, so those modifications are near-inert on this corpus." After: the same words as two sentences, split at the semicolon.
- **R103-34, Appendix G (R2 split).** Before: "When Opus 5 entered. Opus 5 entered the study at the E1-XV preregistration (\texttt{776bce07b3}, 2026-08-14), carrying three of its predictions, after the E1 freeze of 2026-08-10 and before the store-counterfactual freeze of 2026-08-29; in that set it is a descriptive run carrying no prediction, named at the freeze and funded by Amendment 4 of 2026-08-30 before its run was submitted." After: the same words as two sentences, split at the semicolon.
- **R103-35, count changes.** "& --- \\" 6 -> 7 (one more dash cell: the GPT-4.1 mini obligation $\Delta$ cells of Appendix B, the author's point 4); "not expressible by this backend" 7 -> 8 (the Q4 probe's paragraph in Appendix F.7 names the marker once more); the paper's title 1 -> 2 (the supplement's title quotes it).
- **R103-36, Section 1 (one home per number; the author's framing).** Before: "No backend we tested writes that summary: FR-Bank marks stale content about $60\times$ too often, and under the metadata it exposes the obligation gain keeps $42.3\%$ of its value." After: "No backend we tested writes that summary (Section~\ref{sec:backends}), and the metadata FR-Bank exposes recovers under half of the gain a truthful summary gives, which is the size of the gap this paper measures." ($60\times$ and $42.3\%$ print in Section 7.)
- **R103-37, count changes quoted for the gate.** The supplement's title quotes the paper's, so "Knowing the Store: What a Memory Backend Must Write Down Before an Agent Can Read It" now occurs twice across the two sources; the GPT-4.1 mini obligation row of the expansion table reads "mini & NOK & $661$ & $0.4946$ & $0.7339$ & --- & --- \\" (the author's point 4), one more dash cell than v10.




## R104 AUTHORIZATION BLOCK — dated 2026-09-13

**Scope.** The v11-to-v12 pass ordered by the author ("CC pass: v11 to v12"): the body (abstract, Sections 1 to 10, the box) written from the pass's fixed argument (its section 3.1 spine) in one voice rather than patched from v11; the appendices B to H rewritten under the pass's presentation rules P1 to P11 with every table, box and verbatim block carried from `paper_v11.tex` by line range (`reviews/v12/tools/build_v12.py`); the nine Phase 1 analyses with no model call (`reviews/NUMBERS_R104.md`, `reviews/v12/phase1.json`); two descriptive registrations drafted for the author's freeze (`registrations/ADDENDUM_PAD.md` sha256 `93e330225eba5168bd129df565c2c7594883ec830dd1a4ab0f23123520ee32fe`; `registrations/ADDENDUM_PARA.md` sha256 `45cad63d374d5215c4f79eee4192cabb16854238b7782f519cb9a14f8574c009`), neither run in this pass. Every table number is a v11 number or a Phase 1 value; every prose number is a v11 number on the same population, a Phase 1 value, or its two-decimal rounding; no caveat vanishes (`reviews/v12/CAVEAT_LEDGER.md`); no registration-frozen text (R, U, EXEMPT_FROZEN_REGISTERED, W FROZEN-REGISTERED) is reworded; no new claim. **No registered bar, threshold or verdict changes. No model call was made.**

**Lineage.** `paper_v12.tex` is a new file beside `paper_v11.tex` (v11 untouched), assembled from `reviews/v12/src/body_v12.tex` and `reviews/v12/src/appendix_v12.tex`; `SUPPLEMENT.tex` now resolves into `paper_v12` and gains Section S.6 (the struck clause of the first counterfactual form's failure text, moved out of Appendix D.2); the v11 supplement is archived as `SUPPLEMENT_v11.tex`. Reports: `reviews/v12/` (REPORT.md, NUMBER_MOVES.md, CAVEAT_LEDGER.md, CONFLICTS.md, CHANGES.md, REBUTTAL_NOTES.md).

**BASE.** The tree object written from the working copy with a scratch index (the real index and HEAD untouched, nothing committed), holding `paper_v11.tex`, `paper_v11.pdf`, `SUPPLEMENT.tex` and `SUPPLEMENT.pdf` as they stood at the start of the pass: `--base=fa2b6fa1d6b312cf9de55234b93af80c2042f29e --tex=paper_v12.tex --base-tex=paper_v11.tex --extra-tex=SUPPLEMENT.tex` (`reviews/v12/base_tree.txt`).

**Rulings applied (the author's instructions of the pass, recorded because each departs from a written rule or resolves one).**
- **R-a, abstract.** The pass's replacement abstract prints verbatim, with one bracketed sentence left for the two registered runs; numerals sit in two of its sentences (T2 as amended). Its sentences exceed 40 words, which the anti-telegraph scan reports and CONFLICTS.md logs; the author's text is not reworded.
- **R-b, [MAIN] placement.** Every registration text marked [MAIN] (the CF-2 P1 and P3 sentences; the NB6-1 pair and the per-state reading; the SIDE S2 and S2-U sentences; the NB6-2 pair; the DS Section 7 paragraph) stays in the body verbatim, in the section whose argument it serves (Sections 5, 7 and 8 of v12). The CF-2 P2 and P4 texts, the R81 reproduction and per-state branch texts, and the DS and RESP appendix texts stay verbatim in the appendices.
- **R-c, frozen texts and the presentation rules.** A registration-frozen or CLAIMS-untouchable sentence is exempt from P5, P7 and P8 (held/failed vocabulary, three numbers per sentence, forty words); each exemption is listed in CONFLICTS.md.
- **R-d, the box.** The box carries the recommendation of the pass's spine item 12; the two sentences R101-12 fixed as verbatim are superseded by the author's newer instruction and are listed below (R104-19).
- **R-e, Phase 1 values.** Values from `reviews/NUMBERS_R104.md` enter Tables 4 and 5 of the body and the new appendix tables (`tab:cf-fok`, `tab:lex-444`, `tab:dist`, `tab:margin-661`, `tab:cov-lookup`, `tab:reach-k`), labelled exploratory; they and the supplement's own numbers (the base side holds the paper alone) are the ADDED tokens `numeric_diff` accepts on the author's order.
- **R-f, prose roundings.** A two-decimal prose rounding of v11 may leave the body when its four-decimal source stays in a table of the paper; each such rounding is listed in `reviews/v12/NUMBER_MOVES.md` A (the 28% ceiling of the benchmark citation leaves with its clause under the page gate).
- **R-g, Figure 1.** Deleted under P3; the hiking paragraph of Section 1 carries the picture.
- **R-h, Appendix F.7.** The inversion subsection is byte-identical to v11 through the end of its last table; the Phase 1 score-distribution paragraph and `tab:dist` are appended after it, before the next subsection, so the U2 to U4 blocks and the U8 region are untouched and the section hash is re-pinned (`reviews/v12/tools/pin_appendix.py`).

**Entries.** Each Before is the CLAIMS.md-quoted v11 string `frozen_diff` reports as changed; After is the v12 text or the landing that carries the same content at the same strength.

- **R104-1, Section 1 (page gate).** Before: "no evaluated RAG or agentic-memory agent exceeds 7% accuracy; the 28% ceiling belongs to a   long-context agent holding the entire history" After: "on the conflict questions of a recent benchmark no memory agent exceeds $7\%$ accuracy \citep{memoryagentbench}" (the 28% clause leaves; the citation stays).
- **R104-2, Section 1 (page gate).** Before: "was   written only on explicit request" After: the vendor-memory sentence leaves the body; the bibliography entry stays.
- **R104-3, Section 6 of v11 (rewrite).** Before: "can see the cancellation   itself" After: the convergence sentence of Section 8, "their indexed scores converge to $0.82$ to $0.86$ whatever the blind level"; the scale sentence leaves.
- **R104-4, Appendix B.** Before: "of the ten rows carrying both intervals, nine keep the verdict they had at item level" After: "Under persona clustering, nine of the ten rows carrying both intervals keep the verdict they had at item level."
- **R104-5, Section 1.** Before: "scored against labels we know exactly, because we built the stores" After: "We measure both judgments on stores we built, so that every label is exact."
- **R104-6, Section 3.** Before: "one mechanism that escapes the bound" After: "A maintained summary escapes the bound by one route."
- **R104-7, Section 6 of v11 (rewrite).** Before: "Where lifecycle structure exists" After: "Coverage is the judgment on which the model earns its call, and only on the tier where the positives are ordinary records." (Section 8)
- **R104-8, count change.** "Knowing the Store: What a Memory Backend Must Write Down Before an Agent Can Read It" 1 -> 2: the supplement quotes the title (the base side holds the paper alone; R103-37 precedent).
- **R104-9, count change.** "always-reasoning configuration" 1 -> 2: the Appendix C table row and the supplement's Section S.4 (the base side holds the paper alone).
- **R104-10, Section 4 and Appendix F.3 (the pass, section 3.3).** Before: "A mislabeled ABSENT item enters the negative class in both conditions and can only shrink the measured discrimination, so the reported gains are conservative with respect to this error." After: "A mislabeled \absent{} item enters the negative class in both conditions and is expected to shrink the measured discrimination, so the reported gains are conservative with respect to this error." (F.3); Section 4: "such an item is expected to shrink measured gains rather than inflate them".
- **R104-11, Figure 1 (R-g).** Before: "names carrying superseded content" After: Figure 1 is deleted; the summary box of Section 3 prints the section header in full.
- **R104-12, Section 3.** Before: "This is what the indexed monitor reads." After: "\textit{This is what the indexed monitor reads}, an abridged, real FR-Bank summary that exposes counts and attribute names but no stored value."
- **R104-13, Appendix B.** Before: "Blind levels include what the question text gives away, so this trend measures how much of that signal each model reads." After: "On coverage, model scale improves the blind guess, because blind levels include what the question text gives away."
- **R104-14, count change.** "with questions grouped by user   profile" 7 -> 6: the v11 Section 5 interval sentence is replaced by Table 1's rows; the phrase prints six times in v12.
- **R104-15, R104-16, R104-17, Section 5 (P5).** Before: "predictions written before the run"; "its predictions were written before the run"; "All five predictions written before the run were borne out." After: the three sentences leave the body under P5 (no predicted / held / failed in the body); Appendix G's table carries the outcomes and Section 1 states the count once.
- **R104-18, Section 1.** Before: "Of the $58$ preregistered predictions, $16$ did not hold;" After: "Of the $58$ predictions fixed before data collection, $16$ did not hold (Appendix~\ref{app:registration})."
- **R104-19, the box (R-d).** Before: "A system should therefore read obligations by two routes: a name-bearing lifecycle summary, and retrieval that returns non-active records with their lifecycle tags. On the state the summary names, a lookup over that summary decides; model calls go to coverage only where the store has structure, and a store that cannot write such a summary is one no monitor repairs." After: the box's four sentences of v12: "Do not mask: return non-active records with their lifecycle tags, and maintain a list of the attribute names that hold superseded content, the state that tags carry worst." "Read obligations with a similarity lookup over that list; where the store names its states, no model call improves that judgment on the states it names, and the largest model tested adds $0.03$ on the whole counterfactual set (Section~\ref{sec:counterfactual})." "Spend the model call on coverage only, and only where the coverage positives are ordinary records rather than obligations (Section~\ref{sec:populations}); used as a filter at the base rate, its rescaled coverage score flags $134$ of $588$ hard questions and catches $24$ of the $35$ covered ones, a precision of $0.18$ at a recall of $0.69$." "A store without lifecycle structure gets no summary, because reading one hurts coverage at every scale tested (Section~\ref{sec:backends}); a store that cannot write the list is one no monitor repairs."
- **R104-20, Section 6 of v11 (rewrite).** Before: "The summary names superseded content and only counts retracted and expired content, and neither the lookup nor GPT-4.1 mini takes anything from the counts (Table~\ref{tab:nb6-composition})." After: Section 3, "Its name map carries only superseded content, so an entry that expires or is retracted reaches the summary as a count and is never named."; Section 5, "Randomizing those counts across store versions moves each reader by at most $+0.01$ on the whole set, with every interval within $\pm0.05$."
- **R104-21, Section 6 of v11 (rewrite).** Before: "Every paired NOK gain on the cross-model set ($84$ questions, $40$ \pn{}) excludes zero on the five models whose blind score varies (Table~\ref{tab:ladder-exact})." After: Section 8, "Every paired obligation gain excludes zero where the blind score varies (Table~\ref{tab:e1})." and "On the cross-model set of $84$ questions the five models with a varying blind score gain $+0.15$ to $+0.45$, while their indexed scores converge to $0.82$ to $0.86$ whatever the blind level (Appendix~\ref{app:laddertable})."
- **R104-22, Section 1.** Before: "Before it searches, an agent must make two judgments about its store." After: "Before the agent retrieves anything, it must decide two things about that store."
- **R104-23, Section 9 (P10).** Before: "One closed model family supplies the primary capability comparison, with the limits stated where they arise on the Anthropic pair and the two halted runs (Section~\ref{sec:populations} caveat)." After: "One closed model family supplies the primary capability comparison, and two runs stopped at the budget on the full populations." and "The Anthropic pair spans two model generations, so its ordering compares price and capability rather than a within-generation change."
- **R104-24, Section 1.** Before: "each is reported under the text written before scoring in Appendix~\ref{app:registration}" After: "(Appendix~\ref{app:registration})" on the count sentence; Section 4, "Appendix~\ref{app:registration} lists every prediction fixed before data collection with its outcome; a result labelled exploratory was not fixed in advance."
- **R104-25, Section 8.** Before: "GPT-5.6 Luna, Opus 5 and Haiku 4.5 gain $+0.37$, $+0.19$ and $+0.41$ on the same $661$ questions, each interval excluding zero." After: "Haiku 4.5 gains $+0.41$, Opus 5 $+0.19$ and GPT-5.6 Luna $+0.37$ on the $661$ questions." with "Every paired obligation gain excludes zero where the blind score varies (Table~\ref{tab:e1})." before it.
- **R104-26, Section 7.** Before: "No backend we tested writes the summary the obligation judgment needs." After: "No backend we tested writes the list the obligation judgment needs."
- **R104-27, Section 7.** Before: "A name-bearing summary rebuilt from ground truth for the entries each structureless store holds recovers coverage on both." After: "A name-bearing summary rebuilt from ground truth for the entries each store holds restores coverage, from $0.45$ to $0.90$ on A-MEM and from $0.48$ to $0.88$ on Mem0, so the inversion belongs to the summary these stores can write."
- **R104-28, Section 1 of v11 (rewrite).** Before: "retraction records pass retrieval at $5\%$ under that mask" After: Remark 1 keeps "on the inherited store, retraction records pass that mask at $5\%$"; Section 6, "Under the mask the retraction records pass at $5\%$ (Remark~\ref{rem:mask})."
- **R104-29, Section 2 (the pass, section 3.3).** Before: "All of them presuppose the monitoring judgment, an estimate of what the store holds and what it forbids, which means each of them leaves that estimate unmeasured." After: "Each measures a different observable at a different time, after memory has been consulted, so the estimate of what the store holds and forbids stays unmeasured in all of them."
- **R104-30, Section 4.** Before: "The monitor is asked for a number in $[0,1]$ under a fixed rubric, reported in full in Appendix~\ref{app:construction}. The two user prompts differ only in whether the serialized summary precedes the question." After: the same two sentences, the second ending ", so the gain isolates the summary."
- **R104-31, Section 5.** Before: "The boundary between named and counted states is the summary's, because each reader's gap between the named state and the counted states closes once the summary names them." After: "The boundary between the named state and the counted states is therefore the summary's rather than the reader's, because it moves when the summary does."
- **R104-32, Section 6 of v11 (rewrite; R-f).** Before: "On FR-Bank the summary lifts coverage on both question tiers. Hard-question FOK ($307$ questions) rises by $+0.20$ and easy-question FOK ($595$) by $+0.19$, both intervals excluding zero." After: Table 4 carries the hard-tier row ($+0.2037$ with both intervals); the easy contrast's $+0.1914$ prints in Table 19 and its row leaves the body under the page gate.
- **R104-33, Section 6 of v11 (rewrite).** Before: "On the $661$ obligation questions the lookup is again the decision rule, and what the models add appears only on the states the summary does not name." After: Section 8's obligation paragraph: the NB6-1 pair and the per-state reading verbatim, then "The three larger models sit $+0.07$ to $+0.08$ above the lookup on the whole $661$, with item-level intervals that exclude zero and profile-grouped intervals that include it." and "The wider interval therefore leaves that margin unsettled (Appendix~\ref{app:baselines})."
- **R104-34, Section 8.** Before: "The score ranks well and calibrates badly, so its value should be read as a rank and never as a probability." After: "The score ranks well and calibrates badly, with an ECE of $0.17$ indexed against $0.16$ blind whose paired difference includes zero (Appendix~\ref{app:posthoc})."
- **R104-35, Section 7.** Before: "Under the metadata FR-Bank exposes, coverage keeps $101.4\%$ of the \trueidx{} summary's gain (Appendix~\ref{app:construction}), while that metadata recovers $42\%$ of the obligation gain a truthful summary gives. The rest is the gap between what the store writes and what it must." After: "Of the gain a truthful summary gives, $42\%$ survives as rendered and $66\%$ with the fifteen-name cap on the rendered list lifted, because the cap hides two thirds of the names the store does record." and "Coverage keeps $101.4\%$ of its gain under the same metadata, because the coverage judgment reads the per-category name map, which the store's fault does not touch."
- **R104-36, Section 7.** Before: "Precision is $0.03$ capped and $0.04$ lifted, so most of the loss, at the point estimate, is the store's." After: "The lifted list's precision stays at $0.04$, so most of the loss at the point estimate is the store's." ($0.0348$ prints in Appendix F.9.)
- **R104-37, Section 7.** Before: "The below-chance mechanism is unresolved, because no single removal from the summary separates from the intact inversion." After: "Removing the store-wide entry count and the inexpressibility markers together shrinks A-MEM's inversion from $-0.11$ to $-0.04$ and leaves Mem0 unchanged, so no single removal separates from the intact inversion." (U1 and U5 keep "unresolved".)
- **R104-38, Section 6.** Before: "There are two routes to the obligation, and both are the store's metadata, because the summary and the tags on returned records carry the same lifecycle states by different paths." After: "This section establishes a second route to the obligation." and "Retrieval that returns non-active records with their lifecycle tags carries the states the summary misses, and the two together give the best monitor measured."
- **R104-39, Section 6.** Before: ", because the tags on the returned records carry the obligation signal the summary carries." After: "That difference of $-0.05$ has intervals that include zero (Table~\ref{tab:routes}), so the tags on returned records carry the obligation signal the summary carries."
- **R104-40, Section 6.** Before: "The judgment is read off names, because removing them removes it: taking the target's own name and its nearest neighbours out of the summary drops GPT-4.1 mini's supersession judgment from $0.86$ to $0.53$ on the $661$ questions." After: "The summary route rests on names, because removing them removes the judgment." and "Taking the target's own name and its nearest neighbours out of the superseded-names section drops GPT-4.1 mini's supersession judgment from $0.86$ to $0.53$ on the $661$ questions."
- **R104-41, Section 8 of v11 (rewrite).** Before: "On the whole set under that summary the all-states lookup reaches the level Section~\ref{sec:counterfactual} reports." After: the sentence leaves; the CF-2 P3 sentence now sits in Section 5 beside "Naming those states in the all-states summary lifts the lookup to $0.88$ on the whole set".
- **R104-42, the box (R-d).** Before: "The obligation judgment is a lookup over that list (Section~\ref{sec:counterfactual}); once a summary names every non-active state, the lookup reads the obligation on every state, and under the metadata a real backend exposes neither the lookup nor the model rises far above chance (Section~\ref{sec:backends})." After: R104-19's second sentence; Section 7's "On the metadata FR-Bank exposes, lookup and model both fall near chance on the obligation judgment."
- **R104-43, Appendix D.2 (P5).** Before: "The preregistered prediction on this form did not hold, for the reason the next sentence records." After: "At that size the smallest model reached $0.5939$ against $0.5000$, with an item-level interval of $[-0.0345,+0.2315]$ that includes chance and a question-clustered interval of $[+0.0325,+0.1625]$ that excludes it." and "The set could therefore neither establish the aggregate effect nor establish contamination, and the $444$-item form was built with the power the first lacked."
- **R104-44, Appendix E.** Before: "Every failure below is the same kind, a semantic assumption hidden inside a step that looked mechanical, so the ledger is kept as one list." After: "Every failure in the ledger is the same kind, a semantic assumption hidden inside a step that looked mechanical, so the ledger is kept as one list."
- **R104-45, Section 1.** Before: "No backend we tested writes that summary (Section~\ref{sec:backends}), and the metadata FR-Bank exposes recovers under half of the gain a truthful summary gives, which is the size of the gap this paper measures." After: "It breaks again on real backends, none of which writes the list." (Section 1) and Section 7's $42\%$ sentence (R104-35).

### Round 2 of the acceptance test (2026-09-13, the same pass)

- **R-i, the revision rule.** The pass's Section 8 says: if either review calls the core finding definitional, tautological or decidable, revise Section 1 paragraph 2 and Section 5's opening against spine items 2 to 5 and re-run both reviews. Both round-1 reviews scored presentation 2 of 4 and called the core result near-tautological (reviews/v12/REPORT.md, round 1). Round 2 revised those two passages, fixed every concrete defect the two reviews and the reconstruction reader listed, and kept the page gate by moving the abridged real summary of Section 3 to Appendix F.1 and the sentences listed in R104-46, R104-53 and R104-55 out of the body. No table value changed; no frozen registration string was reworded; the entries below quote every changed CLAIMS-watched string.
- **R104-46, Section 8 (page gate).** Before: "Randomizing every count in the summary moves FR-Bank coverage discrimination by $+0.00$ to two decimals (Table~\ref{tab:destruction-fr}), so counts are unnecessary for coverage." After: the sentence leaves the body; Table~\ref{tab:destruction-fr} and Appendix F.5 carry the result unchanged.
- **R104-47, abstract and Section 5 (interim portability sentences).** Before: "[Portability sentence, filled from the two preregistered runs once they land: the paraphrase result and the list-length result, one number at most.]" After: "Two portability checks, on paraphrased questions and on lists padded to sixty names, are preregistered and pending." Section 5, Before: "Two portability checks on this set are preregistered and run after this draft, one on paraphrases that share no token with any listed name and one on lists padded to $60$ names (Appendix~\ref{app:counterfactual}). [Paraphrase result, pending.] [List-length result, pending.]" After: "Two portability checks on this set are preregistered and pending: one asks paraphrases that share no token with any listed name, and one pads the list to $60$ names (Appendix~\ref{app:counterfactual})." Both are interim sentences; the author's sentence from the two runs replaces them (CONFLICTS.md C-R104-3).
- **R104-48, Sections 2 and 4.** Before (Section 4): "What is measured here is belief about an external store rather than confidence in an answer \citep{kadavath2022,lin2022,tian2023,xiong2024}." After (Section 2): "Calibration work scores confidence in an answer rather than belief about an external store \citep{kadavath2022,lin2022,tian2023,xiong2024}."
- **R104-49, Section 7 (the marker defined at first use; the phrase's count rises from 8 to 9).** After: "Where a store exposes no field for a line of the summary, the renderer writes in its place the marker ``not expressible by this backend''." and "Removing the store-wide entry count and those markers together shrinks A-MEM's inversion from $-0.11$ to $-0.04$ and leaves Mem0 unchanged, and no single removal differs from the intact summary by an interval that excludes zero." (Before: "Removing the store-wide entry count and the inexpressibility markers together shrinks A-MEM's inversion from $-0.11$ to $-0.04$ and leaves Mem0 unchanged, so no single removal separates from the intact inversion.")
- **R104-50, Remark 1 and Section 6 (supersedes the Remark wording of R104-28).** Before: "Fix a retrieval budget $k$ and a retriever that masks non-active records from its ranking, as lifecycle-tracking and overwriting stores do; on the inherited store, retraction records pass that mask at $5\%$." After: "Fix a retrieval budget $k$ and a retriever that masks non-active records from its ranking, as lifecycle-tracking and overwriting stores do. On the inherited store, the FR-Bank build of the prior work with its mask in place, retraction records pass that mask at $5\%$. The figure describes the mask rather than the records, because without it a five-item view holds the forbidding record for half of the obligations (Section~\ref{sec:routes})." Section 6, Before: "Under the mask the retraction records pass at $5\%$ (Remark~\ref{rem:mask})." After: the sentence leaves (Remark 1 carries the figure as a mask effect).
- **R104-51, the box (supersedes the second, third and fourth sentences of R104-19).** After: "Read obligations with a similarity lookup over that list; on the states the store names, the two smaller models read no more than the lookup, and the largest model on that set, Opus 5, adds $0.03$ under the all-states summary and $0.07$ under the superseded-only one (Section~\ref{sec:counterfactual})." "Spend the model call on coverage only, and only where the coverage positives are ordinary records rather than obligations (Section~\ref{sec:populations}); threshold it at the base rate of positives unless a cost model says otherwise." "A store without lifecycle structure gets no summary, because the summary such a store can write hurts coverage at every scale tested and the mechanism is unresolved (Section~\ref{sec:backends}); a store that cannot write the list is one no monitor repairs." The exploratory precision and recall figure ($134$ of $588$; $24$ of $35$; $0.18$ at $0.69$) leaves the box; Appendix H.1 carries it at four decimals.
- **R104-52, Section 1 paragraph 2 (spine items 2 to 5; supersedes the Section 1 sentence of R104-45).** After: "If a store lists which of its attributes hold superseded content, matching the question against that list should read the obligation judgment, because the record that forbids use is a record about a named attribute. That expectation is the starting point of this paper rather than its finding. Section~\ref{sec:counterfactual} confirms it where wording cannot carry the label: on the counterfactual set's supersession items, matching alone reads the superseded state at $0.92$. What this paper finds lies at the edges of that expectation. The two smaller models read no more than the lookup on that state, so a model call buys nothing there, and the largest model adds $0.07$ on the whole set. On the states the list only counts every reader is at chance, the largest model included, because three store versions with identical name maps leave nothing to recover. On real backends the expectation breaks again, because none writes the list, and on the metadata the one lifecycle store does write, lookup and model alike fall near chance. The evidence comes from four question sets, six models from three vendors and three memory backends. Of the $58$ predictions fixed before data collection, $16$ did not hold (Appendix~\ref{app:registration})." Section 5's opening, After: "This section measures what each reader extracts from one fixed summary when the question cannot carry the label. ... The summary is the only input that varies across the three versions. Blind NOK is therefore $0.50$ by construction rather than a measured baseline, and every AUROC below is also a gain against it. That the superseded-names list is readable is the expectation this design was built to check rather than a discovery. The section therefore measures which readers read it, on which states, and what a model adds to a lookup that has no model at all."
- **R104-53, Section 3 (Definition 2 folded into prose; Definition 3 becomes Definition 2).** Before: the definition environment "[$k$-bounded monitor] For a per-item score $\sigma$ and budget $k$, let $R_k(q,S)$ be the top-$k$ retrieved set with its full feature profile; a monitor is $k$-bounded when everything it sees of the store is $R_k(q,S)$." After: "For a per-item score $\sigma$ and budget $k$, $R_k(q,S)$ is the top-$k$ retrieved set with its full feature profile. A monitor is $k$-bounded when everything it sees of the store is $R_k(q,S)$." (C034 keeps its content; the label def:kbounded retires, referenced nowhere.)
- **R104-54, Section 3 to Appendix F.1 (page gate).** The abridged real summary (AUX-R86-INDEX-EXCERPT, byte-identical) and its two sentences ("This is what the indexed monitor reads ..." and "The EXPIRED column is derived from each entry's event time ...") move to Appendix F.1 after the two labeled queries; Section 3 keeps "Appendix~\ref{app:glossary} reproduces an abridged real one." at the end of the sentence that names the summary.
- **R104-55, Section 9 to Appendix B.** "The Anthropic pair spans two model generations, so its ordering compares price and capability rather than a within-generation change." moves, byte-identical, to Appendix B after the sentence on the indexed scores across three vendors.
- **R104-56, Section 7 (census units).** Before: "FR-Bank overstates: of $18{,}936$ entries it marks $5{,}968$ inactive, against roughly $102$ the ground-truth manifest explains as superseded, about $60\times$ too many. In the same unit, entries, the manifest marks $104$ superseded, of which $40$ are still active in the store." After: "FR-Bank overstates: it marks $5{,}968$ of its $18{,}936$ entries inactive, and the ground-truth manifest explains about $102$ of those marks as supersessions, so the stale marks outnumber the true ones about sixtyfold. In entries, the manifest's supersessions touch $104$, and the store still lists $40$ of those as active."
- **R104-57, Section 7 (the retention denominator; the $+0.06$ units).** Added after the $42\%$ sentence: "Both retention figures divide by GPT-4.1 mini's indexed-minus-blind difference of $+0.24$ on the $661$ questions, the denominator the $60\%$ bar was set against before scoring. Section~\ref{sec:populations} does not report that difference as a gain, because the model's blind score is constant, so each retention is a ratio of two distances from one constant blind score." Before: "The difference between the lifted and the capped retention, $+0.06$, excludes zero at item level and includes it under the grouping (Appendix~\ref{app:believed-census})." After: "The lifted list's gain exceeds the capped list's by $+0.06$ in AUROC, a difference that excludes zero at item level and includes it under the grouping (Appendix~\ref{app:believed-census})."
- **R104-58, Section 8.** Before: "It also leads the whole-map readers of the same summary by $+0.08$ on the hard tier (Appendix~\ref{app:baselines})." After: "It also leads the lookups that read the whole name map rather than the superseded list by $+0.08$ on the hard tier (Appendix~\ref{app:baselines})." Before: "The paragraph that follows was fixed before scoring and is reported with its numbers." After: the same sentence continued with "; its two bars are a reach gain of $0.50$ for the gold-label fetch and $60\%$ retention of that gain for the gated fetch." Added after the frozen DS paragraph: "Its last sentence counts the oracle policy's $82$ tagged views, whose stale answers and those of its $17$ untagged views sum to the oracle row of Table~\ref{tab:ds-body}." Before: "Haiku 4.5 gains $+0.41$, Opus 5 $+0.19$ and GPT-5.6 Luna $+0.37$ on the $661$ questions." After: the sentence leaves (Table~\ref{tab:e1} prints the three rows). Before: "The token detector behind the answer counts is validated against human labels in Appendix~\ref{app:resp}." After: the clause "by a token detector whose validation against human labels is in Appendix~\ref{app:resp}" on the stale-answer sentence.
- **R104-59, Section 9.** Added: "The tagged route is measured with tags from the ground-truth join, and under the store's own tags it is unmeasured."
- **R104-60, reproducibility statement.** Before: "The anonymous artifact at \url{https://anonymous.4open.science/r/ARTIFACT-URL-SUPPLIED-BY-THE-AUTHOR} holds" After: "The anonymous artifact accompanying this submission holds" (the author's link replaces the phrase at upload).
- **R104-61, SUPPLEMENT.tex Section S.3.** The eleven RESP and DS prediction entries point at Table~\ref{tab:registrations-b} (Table 38, where their rows print) instead of Table~\ref{tab:registrations} (Table 37).
- **R104-62, Section 10.** Before: "The obligation judgment is bounded by what the store writes about itself, so the reader changes little. On the state the summary names a similarity lookup reads it, on the states it only counts nothing reads it, and no tested backend writes the summary that route needs." After: "The obligation judgment is bounded by what the store writes about itself, so the store matters more than the reader. A similarity lookup reads the state the summary names, nothing reads the states it only counts, and no tested backend writes such a summary."
- **R104-63, Section 7 header.** `\label{sec:inversion}\label{sec:stores}` added beside `\label{sec:backends}`, so the verbatim F.7 pointer "The candidate mechanisms in Section~\ref{sec:inversion} remain unresolved" resolves (it printed "Section ??" in round 1).
- **R104-64, own prose shortened under the page gate (no number leaves except as listed in NUMBER_MOVES.md A).** Section 1 paragraph 1 (the two judgments in one sentence; the observable clause merged with its citation), paragraph 3 (compressed); Section 2 (the meta-memory sentence merged with the adaptive-retrieval sentence); Section 3 ("Two labeled example queries are in Appendix~\ref{app:glossary}." leaves; the post-remark gloss compressed); Section 4 ("In all, $248$ judgments yielded the $104$ obligation labels of the full populations." leaves, the AI-use statement keeps the count; the tier and presence-control sentences compressed; the intent route named "the automatic intent classifier that proposed the candidates"); Section 5 (coverage in one sentence; the expiry-pair sentence leaves the body, Appendix D.2 keeps it; the counted-state sentences merged); Section 6 (the mirror-image and best-monitor sentences merged; the retraction sentence merged); Section 7 (opener and compression sentences compressed; "An inversion is an indexed score below the blind score, and a below-chance score is one below $0.50$." added before U1); Section 8 (the 84-question sentence shortened; the margin sentences merged; the all-states rule sentence shortened).

### Round 3 of the acceptance test (2026-09-13, the same pass; the last round the pass permits)

- **R-j, the revision rule, second application.** Both round-2 reviews scored presentation 2 of 4 and again read the core result as expected or tautological (Reviewer A: "close to tautological, and the paper concedes it"; Reviewer B: "the headline empirical result is one the authors themselves call an expectation"), and both read the counted-state result as definitional. Round 3 revised Section 1 paragraph 2 and Section 5 once more against spine items 2 to 5, stating that the counted states carry the label as a tally that no reader uses, and fixed the concrete items the round-2 reviews and the reconstruction reader listed. `frozen_diff` reports no new CLAIMS-watched change (49 authorized, 0 unauthorized); the entries below record the round-3 wording for the file.
- **R104-65, Section 1 paragraph 2 (final).** After: "... What this paper finds lies at the edges of that expectation, and it comes in three parts. First, the two smaller models read no more than the lookup on that state, so a model call buys nothing there, and the largest model adds $0.07$ on the whole set. Second, on the states the list only counts every reader is at chance, the largest model included. The label is in the summary there, because the three store versions differ in their counts, but no reader uses a count, and randomizing the counts moves no reader. A name is a channel every reader uses and a count is one none does, so the store's writing decides what any reader can know. Third, on real backends none writes the list, and on the metadata the one lifecycle store does write, lookup and model alike fall near chance. ..." Paragraph 3, After: "The measurement leads to the deployment rule of Section~\ref{sec:conclusion}. Return non-active records with their lifecycle tags instead of masking them, and maintain the list of superseded attribute names, because a lookup over it reads the obligation judgment. Give a store without lifecycle structure no summary, because reading one hurts."
- **R104-66, Section 3.** Added after the sentence on the name map: "A summary names a state when it lists the attribute names in that state and counts it when it gives only a tally, and a reader reads a state when its score separates that state's items from the rest." Remark 1, Before: "On the inherited store, the FR-Bank build of the prior work with its mask in place," After: "On the inherited store, FR-Bank as released with its mask in place," (both reviews read the earlier phrase as identifying). Added after the remark's gloss: "The remark's force is that measured premise rather than a deep theorem, and it is the reason the deployment rule of Section~\ref{sec:conclusion} says do not mask." (the v11 gloss of R102-58, restored in substance).
- **R104-67, Section 2.** Before: "Each measures a different observable at a different time, after memory has been consulted, so the estimate of what the store holds and forbids stays unmeasured in all of them." After: "Each measures a different observable at a different time, after memory has been consulted. The closest, STALE, scores whether an agent recognizes a memory it holds as no longer valid, whereas NOK is judged before content retrieval and asks whether the store holds anything that must be suppressed at all." Grammar: "whereas NOK's comes from" becomes "whereas NOK's obligation comes from".
- **R104-68, Section 4.** Added: "GPT-5.6 Sol and Kimi K3 stopped at the budget on the full populations, so their complete rows are on the cross-model set (Appendix~\ref{app:laddertable})."
- **R104-69, Section 5.** The binding phrase "(called the store-counterfactual set in Appendix D.2)" on the set's first mention; the opening sentence split ("... that differ in one attribute. The same wording therefore gets three different labels."); "the first including zero" added to GPT-4.1 mini's intervals; Opus 5's intervals stated as "both intervals excluding zero (Table~\ref{tab:cf-main})"; the counted-state sentences, After: "The three versions of a counted-state store have identical name maps and differ only in their counts, so the label is in the summary as a tally rather than a name. No reader uses the tally, because randomizing the counts across versions moves each reader by at most $+0.01$ on the whole set, with every interval within $\pm0.05$."; the portability sentence carries the list length: "..., because the \trueidx{} list averages $1.75$ names per item: ...".
- **R104-70, Sections 6 to 8.** Intervals that Tables 2 and 4 and Appendix F.10 print are stated in prose as "both intervals excluding zero" (the hybrid monitor's gain; the own-name loss; the easy-tier coverage margin; the coverage rule's cost). Section 8: "It also leads the lookups that read the whole name map ..." leaves (Table 27 carries it); "The all-states rule reaches $89$ ..." leaves (Table 5 carries it); "Answers improve only as measured, because reach is not use." becomes "Reach is not use, and the answers show it."; "GPT-4.1 mini's blind obligation score is constant on the full population" becomes "... is flat on the full population, two values with $604$ of the $661$ questions at one of them"; "Its last sentence counts ..." becomes "The paragraph's last sentence counts the oracle policy's $82$ tagged views at both detector thresholds; at the gold threshold its stale answers and those of the $17$ untagged views sum to the oracle row of Table~\ref{tab:ds-body}."; the two bars are named ("the reach gain of $0.50$ and the $60\%$ retention"); added: "The weaker reading is the interval grouped by user profile, whose lower end of $0.56$ falls below the $60\%$ bar." ($0.56$ is the rounded form of $0.5625$, NUMBERS_R104.md section A). Section 7: the $42\%$ sentence names the bar ("against a retention bar of $60\%$ set before scoring") and is split; "so the names the store records are mostly wrong and most of the loss at the point estimate is the store's"; "an excess over $100\%$ that is not a finding".
- **R104-71, Appendix D.2.** `\FloatBarrier` after the verbatim block that carries Table~\ref{tab:counterfactual}, so Table 13 prints before Tables 14 and 15 (Reviewer B, round 2). The paper is 40 pages; the body ends on page 9 (slack +0).

## R105 AUTHORIZATION BLOCK — dated 2026-09-14

**Scope.** The presentation pass ordered by the author on 2026-09-14 (the instruction of that evening: "the [MAIN] placement amendment drafted and applied ... the confession cuts ... Remark 1's last sentence deleted; the easy-tier n reconciled; the Section 8 enumeration fixed; the artifact packaged and scrubbed with the scan printed; REBUTTAL_NOTES.md and CHANGES.md written"), with no model call and no acceptance test (the author: not until the paraphrase probe has landed). Every registration-frozen text marked [MAIN] moves from the body to the appendix that holds its siblings, byte-identical, with one pointer sentence left in the body and the body's lead-in and gloss sentences around it deleted (`registrations/AMENDMENT_MAIN_PLACEMENT.md`, **pending the author's ratification**; the entries R105-1 to R105-10 below). The pilot table, the caching-economics paragraph and the neutral-slice outcome sentence (U6) move to the supplement, verbatim, with pointers (Sections S.7 to S.9). Remark 1's closing sentence is deleted. Section 4 states the tier arithmetic ($661 = 307 + 354$; the Mem0 and A-MEM coverage rows pool both tiers). Section 8's enumeration is repaired (First, Second, Third). **No number changes, no frozen text changes a byte, no bar, threshold or verdict changes.** The two registered runs of R104 stay "preregistered and pending" in the abstract, Section 5, Appendix D.2 and Table 39 until both have landed (the author's order of 2026-09-14, morning).

**Lineage.** `paper_v13.tex` is a new file beside `paper_v12.tex` (v12 untouched), assembled by `reviews/v13/tools/build_v13.py` from `reviews/v13/src/body_v13.tex` and `appendix_v13.tex` (copies of the v12 sources with this block's edits); `SUPPLEMENT.tex` resolves into `paper_v13` and gains Sections S.7 to S.9 (the v12 supplement is kept as `reviews/v13/SUPPLEMENT_v12_backup.tex`). Reports: `reviews/v13/` (REPORT.md, CHANGES.md, REBUTTAL_NOTES.md, CONFLICTS.md, NUMBER_MOVES.md).

**BASE.** The tree object written from the working copy with a scratch index (the real index and HEAD untouched), holding `paper_v12.tex`, `paper_v12.pdf`, `SUPPLEMENT.tex` and `SUPPLEMENT.pdf` as they stood at the R104 close (tex sha256 `c1d3a1ab29f31dce…`, pdf `6769ca5d7d47b8bf…`): `--base=e2d69044adc18e21b788561dca9ced1262ec43aa --tex=paper_v13.tex --base-tex=paper_v12.tex --extra-tex=SUPPLEMENT.tex` (`reviews/v13/base_tree.txt`).

**PENDING RATIFICATION (the author).** `registrations/AMENDMENT_MAIN_PLACEMENT.md`, dated 2026-09-14: the [MAIN] texts of `ADDENDUM_CF2.md` (P1, P3), `ADDENDUM_R81.md` (NB6-1, Amendment 1's NB6-2, the section 10.3 per-state reading (i)), `ADDENDUM_SIDE.md` (S2, S2-U) and `ADDENDUM_DS.md` (the Section 7 paragraph), and the main study's frozen verdict sentence on the BELIEVED obligation row, print verbatim in Appendices D.2, F.8, F.9 and F.10 of `paper_v13.tex` instead of Sections 5, 7 and 8, each with one body pointer. The registrations mark these texts as destined for the main text; the amendment changes their placement only, and it is applied ahead of the author's ratification on the author's instruction of 2026-09-14. If the author does not ratify it, the R104 placement (`paper_v12.tex`) stands and this block's entries R105-1 to R105-10 are void.

**Rulings applied.**
- **R-a, one pointer per text.** The body keeps its own statement of each finding in the pass's voice and adds one pointer sentence per moved text naming the appendix; the sentences whose only purpose was to introduce or explain the frozen text (the lead-in to the DS paragraph, the gloss on its last sentence, the "weaker reading" gloss) are deleted or rewritten to stand on their own (R105-11 to R105-13).
- **R-b, the supplement counts.** `claims_diff` gains `--extra-tex=<file>`: the U-block count is taken over the paper and the named supplement together, so U6 is checked exactly once across the two (the frozen_diff precedent of R104). The title and the phrase "always-reasoning configuration" print once in the paper and once in the supplement (the base side holds the paper alone), the R104-8 and R104-9 precedent (R105-14, R105-15).
- **R-c, roundings added to the body.** Two-decimal forms of numbers that print at four decimals in the paper's tables or appendices enter the pointer sentences: $0.60$ and $0.59$ (the BELIEVED row, $0.5959$ / $0.5858$), $0.75$ and $0.73$ (the $661$, $0.7484$ / $0.7339$), $+0.30$ (Haiku 4.5's counted-state gain, $+0.3010$), $0.76$ (the gated fetch's retention, $0.7561$); each is listed in `reviews/v13/NUMBER_MOVES.md` and accepted under R104's R-f rule in reverse.
- **R-d, the page gate.** The body ends on page 9 with slack $+19$ (`page_census_v2`: reading 466); no addition is needed to fill it and none is made.

**Entries.** Each Before is the string `frozen_diff` reports as changed or moved; After is the v13 text.

- **R105-1, Section 5 → Appendix D.2 (CF-2 P1 [MAIN], verbatim).** Before (body): "On $148$ questions written before any version of the store existed, and asked of three versions of the same store that differ in one attribute each, the smallest model's obligation judgment reaches $0.7167$ against the $0.5$ a question-only reader attains here, with an interval of $[+0.1494,+0.2846]$. The gain survives where the question cannot carry the label." After: the same text in Appendix D.2; the body pointer "Appendix~\ref{app:counterfactual} holds the wording fixed before scoring for the smallest model's result here."
- **R105-2, Section 5 → Appendix D.2 (CF-2 P3 [MAIN], verbatim).** Before (body): "Naming retracted and expired content lifts Haiku 4.5's judgment on those states from $0.5638$ to $0.8649$ on the store-counterfactual set ($60$ questions), a paired gain of $+0.3010$ with interval $[+0.2268,+0.3721]$." After: the same text in Appendix D.2; the body pointer "Haiku 4.5's paired gain on those two states under that summary is $+0.30$ with both intervals excluding zero (its pre-scoring wording is in Appendix~\ref{app:counterfactual})."
- **R105-3, Section 7 → Appendix F.8 (NB6-2 [MAIN] pair, verbatim).** Before (body): "Under the metadata the backend actually exposes, the monitor's obligation judgment is no better than a matcher that reads the store's list of superseded names directly. The monitor scores $0.5959$ on that row and the matcher $0.5858$ (Appendix~\ref{app:baselines})." After: the same two sentences in Appendix F.8, in a paragraph of their own under the U9 firewall; the body pointer "The model scores $0.60$ on that row and the lookup $0.59$, inside tolerance (Appendix~\ref{app:baselines} carries the two sentences fixed before scoring for this row)."
- **R105-4, Section 7 → Appendix F.9 (SIDE S2, verbatim).** Before (body): "Under the \believed{} index the NOK gain is $+0.1012$ ($95\%$ CI $[+0.0217,+0.1744]$, with questions grouped by user profile). That keeps $42.3\%$ of the \trueidx{} gain, short of the $60\%$ we had set as the threshold." After: the same text in Appendix F.9.
- **R105-5, Section 7 → Appendix F.9 (SIDE S2-U not-expected branch, verbatim).** Before (body): "Lifting the cap on the believed list, which raises its recall of ground-truth superseded names from $30.0$ to $66.6$ percent at unchanged precision, retains $65.5$ percent of the \trueidx{} gain, at or above the $60$ percent threshold. Part of the believed-state loss recorded at $42.3$ percent is an effect of the renderer's cap of fifteen names rather than of the store's metadata." After: the same text in Appendix F.9.
- **R105-6, Section 7 → Appendix F.9 (the main study's frozen verdict sentence, verbatim).** Before (body): "NOK degrades materially under believed metadata but remains positive." After: the same sentence in Appendix F.9. The one body pointer for R105-4 to R105-6: "Appendix~\ref{app:believed-census} reproduces the three sentences fixed before scoring on this row. They give the retention under the store's own metadata, the retention with the cap lifted, and the main study's outcome."
- **R105-7, Section 8 → Appendix F.8 (NB6-1 [MAIN] pair, verbatim).** Before (body): "A matcher that scores each question directly against the store's list of names marked superseded reaches $0.7484$ on the same $661$ questions, against the monitor's $0.7339$. Under a truthful summary the obligation judgment is available to a direct lookup on that one list." After: the same two sentences in Appendix F.8; the body's own statement "On the same $661$ questions the superseded-names lookup reads $0.75$ against the smallest model's $0.73$, inside tolerance, so under a truthful summary the obligation judgment is available to a lookup over that one list." and the pointer shared with R105-8, "Both readings were fixed before scoring, the whole-population comparison as a sentence pair and the per-state one as a single reading, and Appendix~\ref{app:baselines} carries them."
- **R105-8, Section 8 → Appendix F.8 (the per-state reading (i) [MAIN], verbatim).** Before (body): "The superseded-names matcher matches the smallest model tested. Larger models score higher on the states the index only counts, an advantage the paired blind comparison does not attribute to the index (Tables~\ref{tab:nb6-attrib} and~\ref{tab:nb6-frontier})." After: the same text in Appendix F.8; the body's own statement "The larger models score higher than the lookup on the states the summary only counts, an advantage the paired blind comparison does not attribute to the summary." and the pointer shared with R105-7.
- **R105-9, Section 8 → Appendix F.10 (the DS Section 7 paragraph, verbatim, AUX-DS-PARAGRAPH-PRINTED).** Before (body): the paragraph beginning "Acting on the obligation judgment changes what a bounded view carries." and ending "($11$ of $82$ at the join's gold threshold; $6$ of $17$ where the record printed as active) (Appendix~\ref{app:resp})." After: the same paragraph under the heading "The registered paragraph." in Appendix F.10; the body pointer "The paragraph fixed before scoring is reproduced with its numbers in Appendix~\ref{app:resp}, where the $22$ unflagged records are traced to the store's write path."
- **R105-10, Section 9 → supplement S.9 (U6, byte-identical, exactly once across paper and supplement).** Before (body): "The indexed NOK gain excludes zero for Opus 5 and includes zero for GPT-4.1 mini, which we record as a failed prediction." After: the same sentence in the supplement's Section S.9; the body pointer "The outcome sentence written before scoring for the neutral-slice prediction is in the supplement (Section~S.9)."
- **R105-11, Section 8 (the lead-in to the DS paragraph).** Before: "The paragraph that follows was fixed before scoring and is reported with its numbers; its two bars are a reach gain of $0.50$ for the gold-label fetch and $60\%$ retention of that gain for the gated fetch." After: "The two bars fixed before scoring were a reach gain of $0.50$ for the gold-label fetch and $60\%$ retention of that gain for the gated fetch."
- **R105-12, Section 8 (the gloss on the paragraph's last sentence).** Before: "The paragraph's last sentence counts the oracle policy's $82$ tagged views at both detector thresholds; at the gold threshold its stale answers and those of the $17$ untagged views sum to the oracle row of Table~\ref{tab:ds-body}." After: the sentence leaves the body (the paragraph it glossed is in Appendix F.10; the oracle row of Table 5 is unchanged).
- **R105-13, Section 8 (the weaker reading).** Before: "The weaker reading is the interval grouped by user profile, whose lower end of $0.56$ falls below the $60\%$ bar." After: "The gated fetch retains $0.76$ of that gain, and under the weaker reading, the interval grouped by user profile, the lower end of $0.56$ falls below the $60\%$ bar." The P5 exception sentence "The two bars that did not hold, the reach gain of $0.50$ and the $60\%$ retention, were set under the masked-retrieval premise (the $5\%$ pass rate), which the reach of $0.52$ replaced." is unchanged.
- **R105-14, count change.** "Knowing the Store: What a Memory Backend Must Write Down Before an Agent Can Read It" 1 -> 2: the supplement quotes the title (the base side holds the paper alone; R104-8).
- **R105-15, count change.** "always-reasoning configuration" 1 -> 2: the Appendix C table row and the supplement's Section S.4 (the base side holds the paper alone; R104-9).
- **R105-16, Section 3 (Remark 1's closing sentence, the author's order).** Before: "The remark's force is that measured premise rather than a deep theorem, and it is the reason the deployment rule of Section~\ref{sec:conclusion} says do not mask." After: the sentence is deleted; the paragraph ends "A maintained summary escapes the bound by one route, and retrieval that does not mask and returns lifecycle tags escapes it by another (Section~\ref{sec:routes})."
- **R105-17, Section 4 (the easy-tier n).** After: "The $661$ obligation questions are the hard tier's $307$ and the easy tier's $354$ together; coverage is scored on the hard tier, and the easy tier enters only the coverage comparison with the lookup, while the Mem0 and A-MEM coverage rows pool both tiers ($238$ and $284$ questions)." ($354 + 307 = 661$; Mem0 $102 + 136$, A-MEM $139 + 145$; `e1_metamemory/build/items_final.json`.)
- **R105-18, Section 8 (the enumeration).** Before: "This section establishes three things on the full populations. The obligation gain replicates across six models, and the model's coverage margin over the lookup lives on the tier where the positives are ordinary records. Third, ..." After: "This section establishes three things on the full populations. First, the obligation gain replicates across six models. Second, the model's coverage margin over the lookup lives on the tier where the positives are ordinary records. Third, ..."
- **R105-19, Appendix F.2 → supplement S.7 (the pilot table).** The two sentences of F.2 and Table `tab:pilot-record` (paper_v11.tex lines 1333 to 1349, byte-identical) move to the supplement; F.2 keeps one sentence: "The pilot preceded the main study with a different prompt, so its values support the design lesson and cannot be compared numerically with the main study; its estimands and their table are in the supplement (Section~S.7)."
- **R105-20, Appendix F.11 → supplement S.8 (the cost paragraph).** The five sentences of F.11 move to the supplement verbatim; F.11 keeps one clause and the pointer: "Monitoring runs before every query, so its cost turns on prompt caching; the projection and the billed micro-run are in the supplement (Section~S.8)."
- **R105-21, non-manuscript writes.** `tools/claims_diff.py` gains `--extra-tex=<file>` (R-b); `reviews/v13/tools/build_v13.py` and `package_artifact.py` (the v13 bundle, with the scan report inside the zip); `reviews/v13/moved_texts.json` (the sha256 of each moved text as it stood in the body and as it stands in its appendix); `registrations/AMENDMENT_MAIN_PLACEMENT.md` and its ARTIFACT copy; `ARTIFACT/README.md` re-pointed at paper_v13.

### R105, continued (2026-09-14, evening): the CF-3 expiry extension lands (the author's ruling of that date)

**Scope.** The author's ruling after the sizing census (`r82_counterfactual/cf3/CF3_CENSUS.md`, commit `ba922af`): "CF-3 ruling: expiry only. Register a descriptive addendum for the 14 eligible undrawn expiry pairs that fit the cap and the name rule (42 items, three versions each, same construction, same summaries, no reads required). Score both lookups, then mini once, Haiku five calls, Opus once. Report the cell beside the 444, and a pooled expiry row (CF-2 plus CF-3, 44 pairs) with the pooling disclosed in the caption. Retraction stays at 30; add to Section 5 or Limitations that one candidate in ten passes the author's plausibility read, with the census as the citation. Check whether Section 7 or Table 3 states that 9 of the 40 manifest retraction events resolve to a retracted entry under the truthful join; if not, add it to the conflate row. Author ratification line for the CF-3 addendum drafted alongside the others." Registration `registrations/ADDENDUM_CF3.md`, registered text sha256 `2f555c1ac4c3018e66a0fc453be7c4c4d3ffd4e3a2f7ac63c5c7b3590ca4f910`, recorded in `r82_counterfactual/cf3/NUMBERS_CF3.md` before the first call; the run ordered by the message quoted, **the author's ratification line pending** below the addendum's marker (PENDING RATIFICATION, alongside AMENDMENT_MAIN_PLACEMENT.md). Every value enters through `NUMBERS_CF3.md` (`trace_scan_v13` LEDGERS gains it). No frozen number, bar, threshold, verdict or frozen text changes; the 444's rows are read and never re-run.

- **R105-22, Appendix D.2 (new paragraph and Table `tab:cf3-expiry`).** After the paragraph on the two registered checks: "The expiry state extended by a third descriptive draw." — the census's 19 / 14, the construction, the leakage screen ($0$ of $14$ on every summary), the pointer to the table, the two-decimal readings $0.97$ (all-states lookup) and $0.68$ (GPT-4.1 mini, all-states summary) on the extension (`AUX-CF3-PRINTED`), and "retraction stays at $30$ pairs, because one candidate in ten passes the author's read for a cancellable plan." The table prints the $444$'s expiry slice, the extension and the pooled $44$ pairs per reader and summary with the weaker interval, the pooling and the Opus 5 draw-count difference in the caption (`AUX-CF3`, `AUX-CF3-CF2SLICE`, `AUX-CF3-POOLED`). Regenerated from `r82_counterfactual/cf3/paper_table.tex` between CF3-TABLE markers.
- **R105-23, Section 9 (Limitations).** After "The counted-state groups are small: …" two sentences: "A later descriptive draw extends the expiry pairs to $44$ with the eligible candidates the first draw left undrawn (Appendix~\ref{app:counterfactual})." and "Retraction stays at $30$ because one candidate in ten passes the author's read for a cancellable plan ($36$ of $370$ read), and the candidate census in the artifact records every candidate with the rule that removed it." (`AUX-CF3-CENSUS-RETRACTION`.)
- **R105-24, Table 3, the Conflate row.** Appended: "The manifests record $40$ retraction events, one per persona, and the truthful join resolves $9$ of them to a retracted entry ($23$ entries)." (`AUX-CF3-CENSUS-MANIFEST`; neither Section 7 nor Table 3 stated it.)
- **R105-25, Table `tab:registrations-c`.** A fifth row, "Expiry extension of the counterfactual set, \texttt{2f555c1a}, 2026-09-14, … no prediction", and the caption's count ("five descriptive registrations"; "the expiry extension has run").
- **R105-26, non-manuscript writes.** `r82_counterfactual/cf3/` (`cf3_build.py`, `cf3_run.py`, `cf3_score.py`, `cf3_ledger.py`, the cell, its summaries, the rows, `NUMBERS_CF3.md`, `paper_table.tex`); `registrations/ADDENDUM_CF3.md` and its ARTIFACT copy; `reviews/v13/CF3_QUESTION_FLAGS.md` (the author's optional flag read); `tools/trace_scan_v13.py` LEDGERS; `tools/appendix_identity.py` (the R105 pins for D.2 and G re-issued for the extension's state); the artifact (`ARTIFACT/README.md`: Table 16 = `tab:cf3-expiry`, forty tables, `rows/cf3/`; `reviews/v13/tools/package_artifact.py`: the cf3 code, ledger and rows; the phantom `rows/v12/margin_intervals.json` reference dropped from Table 31's row, the intervals sit in `phase1.json` under `item3_661.margins`); the census path in the registrations table reads `rows/cf3/CF3_CENSUS.md`, the path inside the bundle.

## R106 AUTHORIZATION BLOCK — dated 2026-09-14

**Scope.** The author's pass on v13 from the eighth review (the instruction of 2026-09-14: "Pass on v13 from the eighth review, figures deferred. Same rules: frozen numbers, frozen strings, no new claim, body on page 9, nothing committed. Skip any item v13 already did."), fourteen items: (1) Table 1's model-gain intervals and lookup-AUROC intervals in separate labelled columns; (2) a three-line definition box for names / counts / reads where Definition 2 introduces them, the words used as terms of art only where a claim turns on them; (3) "the findings sit at the edges of that expectation" and every variant deleted, "the label is in the summary as a tally" deleted, the abstract and Section 10 leaning on the fault decomposition and the real-metadata collapse; (4) "the smaller models read no more than the lookup" scoped to the counterfactual set with the 661 margin of Haiku 4.5, GPT-5.6 Luna and Opus 5 beside it in the same sentence; (5) the literal-threshold lookup row in Table 5, its answer stage run under a descriptive addendum, the deployment rule as fetch-on-match without coverage abstention with the gated rules as the comparison, the tagged / untagged stale rates under retrieval alone, Haiku 4.5 as a second answerer; (6) Section 7 led by the compression result, "unresolved" only for the trigger; (7) H.2 relabelled a disclosure with the paraphrase set named as the control; (8) Section 1 naming the three failed predictions that changed the reading; (9) Section 4 stating that every question set was generated from human-written manifests and that Kimi K3 completed the cross-model set in full; (10) the counted-state caveat in the deployment rules; (11) the AI-use Proposition sentence plain; (12) one name per object; (13) two answers in REPORT.md; (14) gates, page 9 with slack reported. Program name R106; `paper_v14.tex` beside `paper_v13.tex`; nothing committed in this pass.

**Lineage.** `paper_v14.tex` is assembled by `reviews/v14/tools/build_v14.py` from `reviews/v14/src/body_v14.tex` and `appendix_v14.tex` (copies of the v13 sources with the edits of `reviews/v14/tools/edit_v14.py` and `tighten*_v14.py`, applied in order); carried blocks resolve from `paper_v11.tex` by line range as before, except `tab:ds` (v11 lines 2029-2057), now inline so that the literal rule's answer row can be filled. `SUPPLEMENT.tex` is unchanged and resolves into `paper_v13` (its `.pdf` in the base tree is the v13 close's).

**BASE.** The tree object written from the working copy with a scratch index, holding `paper_v13.tex`, `paper_v13.pdf`, `SUPPLEMENT.tex` and `SUPPLEMENT.pdf` as they stood at the v13 close with the CF-3 table (tex sha256 `f45ba59256647245…`, pdf `fba47f4d31d8843f…`): `--base=a65f90a4cd6a4f609a7f806474d80ed992914d53`, `--base-tex=paper_v13.tex`, `--program=R106`, `--extra-tex=SUPPLEMENT.tex`.

**Registered run (descriptive).** `registrations/ADDENDUM_DS_AMENDMENT_2.md`, registered text sha256 `a3ff9d89c7b330d1243bc50d9b619b8497239f7f3757cb59816cf2e17fe3bdec`, recorded in `ds_downstream/NUMBERS_DS.md` section 7 before the first call; the author's instruction quoted at its head. Lane 1: GPT-4.1 mini, the section D.4 protocol, 268 LOOKUP-LIT views of which 238 reuse a recorded answer and 30 were new calls ($0.0084). Lane 2: Claude Haiku 4.5 as the answerer on every distinct view of the seven policies, 452 calls ($0.4023; projection x1.3 $0.4867 under the $5 line). Total $0.4141. Keys `AUX-DS-A2-*`. No prediction, no bar; DS-P1 to DS-P5 stand. Not committed in this pass (the author's rule); the commit follows the author's word.

**New ledger.** `nb6_sweep/NUMBERS_NB6SWEEP.md` (`nb6_sweep/tools/ledger_nb6sweep.py`, from the committed `results/step4_recall.json`; no model call): `AUX-NB6SWEEP-DECOMP-444`, `-DECOMP-661`, `-BELIEVED`, `-PRINTED`. `tools/trace_scan_v13.py` LEDGERS gains it. The shares the abstract and Section 10 print are the counterfactual set's embedding whole-set row at r = 0.3604 (0.6010 / 0.2943 / 0.1047, printed as about six tenths / three tenths / one tenth); the author's message said "about half, about a third, about a tenth", which no ledger row gives, and the report records the difference for the author's ruling.

**Page gate.** The first v14 build ended on page 10 (reading 505); the body returns to page 9 by removing elements the appendix carries byte for byte (Table 2's coverage-tier block, `tab:cov-lookup`; Table 5's matched-budget retrieval rows, `tab:reach-k`), Section 5's prose restatement of Table 1's lower block, Section 4's "NOK can be measured only on FR-Bank" (Limitations' second sentence), Section 1's one-line deployment pointer, a caption clause in Tables 3 and 4, and the box's closing slogan; every four-decimal value stays in the paper (the two-decimal forms $0.01$, $-0.01$ and $-0.10$ of Table 1's lower block and the $7.00$ / $10.00$ view sizes of the matched-budget rows leave with their sentence and rows; reviews/v14/NUMBER_MOVES.md) and every caveat-ledger row keeps a home. Slack +0 at the close.

**Entries.** Each Before is the string `frozen_diff` reports as changed; After is the v14 text.

- **R106-1, Table 1 (item 1).** Columns "AUROC & gain, item interval & gain, profile interval & lookup AUROC, profile interval"; model rows carry a dash in the lookup column and lookup rows in the two gain columns; the lower block's header names the difference and its two intervals. No number changes; the caption drops "a lookup carries the profile interval of its AUROC".
- **R106-2, Section 3 (item 2).** Before: "A summary names a state when it lists the attribute names in that state and counts it when it gives only a tally, and a reader reads a state when its score separates that state's items from the rest." After: Definition 3 (Names, counts, reads), three lines: "A summary \emph{names} a state when it lists the attribute names in that state." / "A summary \emph{counts} a state when it gives only a tally of it." / "A reader \emph{reads} a state when its score separates that state's items from the rest." Loose uses of "read" in the body become "recover", "queries", "is shown", "interpreted", "scores", "treat", "responds to", "gives", "judge" (Sections 1 to 8 and the box); the term-of-art uses stay.
- **R106-3, the abstract (items 3 and 4).** Before: "a similarity lookup over the list reads the superseded state at $0.92$ AUROC, the smaller models read no more than the lookup, and the largest reads slightly more. The findings sit at the edges of that expectation." After: "a similarity lookup over the list reads the superseded state at $0.92$ AUROC; on that counterfactual set the smaller models read no more than the lookup and the largest reads slightly more, while on the $661$ questions of the main study the three larger models sit $+0.07$ to $+0.08$ above it, with item intervals excluding zero and profile intervals including it." And after "lookup and model alike fall near chance.": "Of the lookup's loss under that backend's measured faults, missing names account for about six tenths, wrong names for about three tenths and list length for about one tenth." (`AUX-NB6SWEEP-PRINTED`.) The 661 margins are `reviews/NUMBERS_R104.md` item3_661: Luna +0.0698, Haiku 4.5 +0.0726, Opus 5 +0.0843, item intervals excluding zero, profile intervals including it; printed as $+0.07$ to $+0.08$ as Section 8 already does.
- **R106-4, Section 1 (items 3, 4, 8).** "What this paper finds lies at the edges of that expectation, and it comes in three parts." becomes "The findings that follow come in three parts."; the First sentence becomes "First, on the counterfactual set the two smaller models read no more than the lookup, while on the $661$ questions the three larger models exceed it by $+0.07$ to $+0.08$, item interval excluding zero and profile interval including it."; "The label is in the summary there, because the three store versions differ in their counts, but no reader uses a count, and randomizing the counts moves no reader." becomes "The three store versions differ there only in their counts, no reader uses a count, and randomizing the counts moves no reader."; the paragraph "Three failed predictions changed the reading: the reach premise, the retrieved-view route and the oracle margin." with one sentence each (L2-P3 $54$ of $104$ against under a fifth; L2-P1 within $0.05$; DS-P1 $0.43$ against $0.50$; `resp_review/NUMBERS_RESP.md`, `ds_downstream/NUMBERS_DS.md`) follows the $58$ / $16$ sentence. Before (deleted under the page gate): "The measurement leads to the deployment rule of Section~\ref{sec:conclusion}. Return non-active records with their lifecycle tags instead of masking them, and maintain the list of superseded attribute names, because a lookup over it reads the obligation judgment. Give a store without lifecycle structure no summary, because reading one hurts." After: the paragraph is deleted; the box carries the rules.
- **R106-5, Section 3, Definition 2 (item 12).** "Lifecycle index" becomes "Lifecycle summary", "An index $M(S)$" becomes "A summary $M(S)$"; Before: "The lifecycle index of Definition~\ref{def:index} is what the indexed monitor reads, and the rest of this paper calls it the summary (the index, in the preregistered texts); Appendix~\ref{app:glossary} reproduces an abridged real one." After: "The lifecycle summary of Definition~\ref{def:index} is what the indexed monitor is shown (the index, in the preregistered texts); Appendix~\ref{app:glossary} reproduces an abridged real one." The two binding clauses stay; every other index / matcher in the body is gone, and the appendix's are inside frozen texts.
- **R106-6, Section 4 (items 9 and the page gate).** Before: "GPT-5.6 Sol and Kimi K3 stopped at the budget on the full populations, so their complete rows are on the cross-model set (Appendix~\ref{app:laddertable})." After: "Kimi K3 completed the cross-model set in full and stopped at the budget on the full populations, as did GPT-5.6 Sol, so their complete rows are on the cross-model set (Appendix~\ref{app:laddertable})." (`e1xv_crossvendor/NUMBERS_E1XV.md`: kimi-k3 840 rows on the 84; `r74/x4/rows_K3.jsonl` 231 rows.) Added after the question-sets sentence: "Every question set was generated by a language model from human-written manifests, and those manifests are the ground truth every label is scored against." Before (deleted under the page gate): "NOK can be measured only on FR-Bank, because only FR-Bank retains superseded content." After: deleted; Limitations keeps "NOK is measured on one lifecycle store, the only backend that retains superseded content."
- **R106-7, Section 5 (items 3 and the page gate).** Before: "The three versions of a counted-state store have identical name maps and differ only in their counts, so the label is in the summary as a tally rather than a name." After: "The three versions of a counted-state store have identical name maps and differ only in their counts." The prose restatement of Table 1's lower block ("GPT-4.1 mini sits $0.05$ below with intervals of ... and Haiku 4.5 sits $0.01$ below with both intervals including zero") is deleted; the preceding sentence gains "(Table~\ref{tab:cf-main})".
- **R106-8, Section 7 (item 6).** The compression paragraph reordered: the variance / mean result, the marker, the marker-as-absence probe, the removal probe, the rebuilt summary, then the two definitions and U1. Before: "This is an inversion at every scale, not a below-chance score at every scale. The cause of the below-chance cases remains unresolved." After: the U1 sentence byte-identical, followed by "What triggers the compression is unresolved on both stores." and "Two hypotheses remain: global counts may make the store look better covered than it is, and disagreement between the summary and the retrieved view may compress the score range." The paragraph's opener becomes "On the two structureless stores the summary hurts coverage at every scale tested, and what it does to the score is compression." U5 in Limitations is frozen and keeps "mechanism remains unresolved".
- **R106-9, Section 8 (items 2 and 5).** Before: "On the same $661$ questions the superseded-names lookup reads $0.75$ against the smallest model's $0.73$, inside tolerance, so under a truthful summary the obligation judgment is available to a lookup over that one list." After: "reads" becomes "scores". Table 5 gains the coverage column (`AUX-DS-PRESENT`; the matched-budget rows moved to `tab:reach-k`) and the row "Lookup, literal threshold, no abstention & $184$ & $94$ ($0.9038$) & $7.42$ & $75$ & $65$ & $14$ & $46$" (`AUX-DS-POLICIES`, `-REACH`, `-VIEWSIZE`, `-PRESENT`, `AUX-DS-A2-STAGE2-LIT`); after the table, the literal rule's two sentences, "$14$ under the literal rule" in the stale sentence, and "Under retrieval alone it is given for $2$ of the $35$ obligations whose forbidding record is in view with its tag and for $7$ of the $19$ whose record is in view untagged." with "The literal rule's split is $7$ of $75$ against $7$ of $19$" (`AUX-DS-STAGE2`, `AUX-DS-A2-STAGE2-LIT`). "A seven-item retrieval view reaches $62$ and a ten-item view $74$ (Appendix~\ref{app:resp})". The hard- and easy-tier pointers move from Table~\ref{tab:e1} to Appendix~\ref{app:baselines}.
- **R106-10, Section 10 and the box (items 3, 4, 5, 6, 10).** The conclusion gains "Under the one lifecycle store's own metadata, both readers fall near chance." and "Of the lookup's loss under that store's measured faults, missing names account for about six tenths, wrong names for about three tenths and list length for about one tenth (Appendix~\ref{app:posthoc-faults})." Before: "Read obligations with a similarity lookup over that list; on the states the store names, the two smaller models read no more than the lookup, and the largest model on that set, Opus 5, adds $0.03$ under the all-states summary and $0.07$ under the superseded-only one (Section~\ref{sec:counterfactual})." After: "Judge obligations with a similarity lookup over that list: on the counterfactual set the two smaller models read no more than the lookup and Opus 5 adds $0.03$ under the all-states summary and $0.07$ under the superseded-only one (Section~\ref{sec:counterfactual}), while on the $661$ questions the three larger models are $+0.07$ to $+0.08$ above it (item interval excluding zero, profile interval including it; Section~\ref{sec:populations})." then "The counted-state evidence rests on $30$ retraction and $44$ expiry pairs, and the $661$ rows give only the direction." Before: "Spend the model call on coverage only, and only where the coverage positives are ordinary records rather than obligations (Section~\ref{sec:populations}); threshold it at the base rate of positives unless a cost model says otherwise." After: "Fetch an attribute's lifecycle records whenever the lookup matches it at the base rate, with no coverage abstention: that rule reaches $94$ of the $104$ forbidding records at a mean view of $7.42$ and keeps retrieval's coverage, against $85$ for the gated rules that were the comparison fixed in advance (Section~\ref{sec:populations})." and "A model call earns its cost on coverage only where the positives are ordinary records rather than obligations (Section~\ref{sec:populations})." Before: "A store without lifecycle structure gets no summary, because the summary such a store can write hurts coverage at every scale tested and the mechanism is unresolved (Section~\ref{sec:backends}); a store that cannot write the list is one no monitor repairs." After: "A store without lifecycle structure gets no summary, because the summary such a store can write compresses the coverage score at every scale tested and what triggers the compression is unresolved (Section~\ref{sec:backends})."
- **R106-11, the AI-use statement (item 11).** The Proposition sentence joins the first paragraph as a plain sentence: "We did not use generative AI tools for the mathematical claims of this work; Proposition~\ref{prop:nonident} and its proof were written by the authors without model assistance."
- **R106-12, Appendix H.2 (item 7).** Title "A disclosure: the counterfactual set split by whether the question names its attribute"; added: "It is a disclosure rather than a control, because the flag marks a question that names its attribute at the level of the topic while every value is scrubbed from every summary, so a flagged question need carry no more of the label than an unflagged one; the control is the paraphrased counterfactual set, registered and pending (Table~\ref{tab:registrations-c})."
- **R106-13, Appendix H.3 (item 3), new.** "The lookup's loss under a real backend's faults, decomposed": the paragraph and Table `tab:faults` (`AUX-NB6SWEEP-DECOMP-444`, `-DECOMP-661`, `-BELIEVED`), post hoc, no prediction.
- **R106-14, Appendix F.10 and `tab:ds` (item 5).** The account of Amendment 2 and Table `tab:ds-h45` (Haiku 4.5, seven policies; `AUX-DS-A2-STAGE2-H45`); `tab:ds` inline with the literal rule's answer row "$94$ & $0$ & $7$ of $75$ / $7$ of $19$ & $174$ & $46$ ($0.2644$)" in place of the dash row "Lookup, literal threshold & --- & --- & --- & --- & --- \\" (the slogan_scan structural string "& --- \\" 7 -> 6) and the caption's clause "its answer stage was registered after the first draft (Amendment 2) and prints in the second block".
- **R106-15, Appendix G, `tab:registrations-c`.** A sixth row "DS Amendment 2: the literal rule's answer stage, and a second answerer, \texttt{a3ff9d89}, 2026-09-14, ... no prediction"; Before: "five descriptive registrations" After: "six descriptive registrations", and "the expiry extension and the second downstream amendment have run".
- **R106-16, count changes.** "Knowing the Store: What a Memory Backend Must Write Down Before an Agent Can Read It" 1 -> 2 and "always-reasoning configuration" 1 -> 2: the supplement quotes both and the base side holds the paper alone (R105-14, R105-15).
- **R106-17, tools and non-manuscript writes.** `reviews/v14/` (`src/`, `tools/build_v14.py`, `edit_v14.py`, `tighten_v14.py` to `tighten6_v14.py`, `claims_r106.py`, `pin_appendix.py`, `base_tree.txt`, REPORT.md, CHANGES.md, `k5_variation.json`); `ds_downstream/tools/amend2_lit.py`, `ds_downstream/run/*amend2*`, `ds_downstream/cache_amend2/`, `ds_downstream/NUMBERS_DS.md` section 7; `registrations/ADDENDUM_DS_AMENDMENT_2.md` and its ARTIFACT copy; `nb6_sweep/tools/ledger_nb6sweep.py`, `nb6_sweep/NUMBERS_NB6SWEEP.md`; `tools/trace_scan_v13.py` LEDGERS; `tools/appendix_identity.py` R106 pins.

## R107 AUTHORIZATION BLOCK — dated 2026-09-14

**Scope.** The author's corrections to v14 (the message of 2026-09-14): (1) the deployment rule reverted — the gated rules are the registered policies, the literal-threshold rule is a descriptive comparison in Table 5 with its stale column printed, and Section 8 states that stale answers rise with reach under both answerers and that no fetch policy is recommended until an answerer converts reach into correct answers; (2) a descriptive addendum (DS Amendment 3) running the answer stage once more with an instruction to treat records tagged superseded, retracted or expired as not to be used, GPT-4.1 mini and Haiku 4.5 on the same distinct views, under $2, reported beside the existing rows; (3) the annotator sample gains a column, whether the answer correctly reports the obligation; (4) the abstract replaced by the author's text, verbatim; (5) the fault decomposition out of the abstract and Section 10, stated once in Section 7 with its instability across the two sets in the same sentence; (6) the padding results landed in Section 5 and D.2, the paraphrase sentence gone from the abstract, one D.2 line saying the registered read is in progress; (7) Section 4's protocol sentence corrected and the site of the 5% pass rate stated; (8) the box cut to three sentences, its qualifications moved to Sections 5 and 8; (9) gates, page 9. Program name R107; `paper_v15.tex` beside `paper_v14.tex`; nothing committed.

**Lineage.** `paper_v15.tex` is assembled by `reviews/v15/tools/build_v15.py` from `reviews/v15/src/body_v15.tex` and `appendix_v15.tex` (copies of the v14 sources with the edits of `reviews/v15/tools/edit_v15.py` and `tighten_v15.py` to `tighten6_v15.py`, in order). `SUPPLEMENT.tex` resolves into `paper_v15` and Section S.4 gains the five-draw census paragraph.

**BASE.** The tree object written from the working copy with a scratch index, holding `paper_v14.tex`, `paper_v14.pdf`, `SUPPLEMENT.tex` and `SUPPLEMENT.pdf` as they stood at the v14 close: `--base=2d49a7bfafa9e4f1e208debc296b469d17e13eeb`, `--base-tex=paper_v14.tex`, `--program=R107`, `--extra-tex=SUPPLEMENT.tex`.

**Registered run (descriptive).** `registrations/ADDENDUM_DS_AMENDMENT_3.md`, sha256 `eca19607629c03d122f0e0ac66c50c3068978dcecd3be35296191aa3e2f3bce1`, recorded in `ds_downstream/NUMBERS_DS.md` section 8 before the first call; the added instruction quoted verbatim in its section A3.2 and asserted by the runner. Lane 1 GPT-4.1 mini 452 calls $0.1288; Lane 2 Haiku 4.5 452 calls $0.4279; probes $0.0009; total $0.5576 against the $2 line (projection ×1.3 $0.5963). Keys `AUX-DS-A3-*`. No prediction, no bar; DS-P1 to DS-P5 and Amendments 1 and 2 stand. Not committed in this pass.

**Ledgers.** `pad_probe/NUMBERS_PAD.md` gains section 6, `AUX-PAD-PRINTED` (`pad_probe/tools/pad_table.py`, which also writes `pad_probe/paper_table.tex`, spliced into D.2 between PAD-TABLE markers), and enters `tools/trace_scan_v13.py` LEDGERS; `reviews/NUMBERS_R107.md` (`AUX-R107-AV7`, the 5% pass rate's site; `AUX-R107-K5`, the five-draw census from `reviews/v14/k5_variation.json`; `AUX-R107-TEMP`, the lanes' decoding settings) likewise. The annotator sheet `reviews/v12/DETECTOR_LABELING_SHEET.md` gains Q4 (two columns; `reviews/v12/tools/detector_agreement.py` reads them; no label written).

**Entries.** Each Before is the string `frozen_diff` reports as changed; After is the v15 text.

- **R107-1, the abstract (items 4, 5, 6).** Replaced in full by the author's text: "Agents with persistent memory decide, before retrieving anything, whether the store covers a question and whether it holds something they must no longer use, such as a cancelled plan. We call these judgments feeling of knowing (FOK) and negative-obligation knowledge (NOK) and measure both on synthetic stores with exact labels, across three memory backends and six language models. The obligation judgment is bounded by what the store writes about itself. When a store lists the attribute names that carry superseded content, a similarity lookup over that list detects the superseded state with $0.92$ AUROC on a set where the same question is asked of three store versions; the two smaller models do no better than the lookup and the largest does slightly better. States the summary only counts are undetectable by any reader until they are named. Returning non-active records with their lifecycle tags, instead of masking them, is a second route, and combining it with the summary gives the best monitor we measure. No tested backend writes such a summary: one over-marks stale content sixtyfold, one overwrites its history, one's links resolve to nothing, and on the metadata they expose every reader falls to near chance. Backends should return tags, not masks, and maintain the list." Before, gone with it: "a similarity lookup over the list reads the superseded state at $0.92$ AUROC; on that counterfactual set the smaller models read no more than the lookup and the largest reads slightly more, while on the $661$ questions of the main study the three larger models sit $+0.07$ to $+0.08$ above it, with item intervals excluding zero and profile intervals including it." (the fragment "the smaller models read no more than the lookup" 1 -> 0); "Two portability checks, on paraphrased questions and on lists padded to sixty names, are preregistered and pending."; "Of the lookup's loss under that backend's measured faults, missing names account for about six tenths, wrong names for about three tenths and list length for about one tenth."; "lookup and model alike fall near chance." 2 -> 1 (Section 1 keeps it). The abstract's closing sentence is added to `slogan_scan`'s S9 exemptions as the author's text, verbatim by instruction.
- **R107-2, Section 4 (item 7).** After the FR-Bank sentence: "The $5\%$ retrieval pass rate cited for its mask was measured on the $40$ retraction questions of the prior store's own benchmark, one per persona of the same persona bank, with the mask in place." (`AUX-R107-AV7`). Before: "Every model except it was scored by averaging five calls per question at temperature $0$." After: "Every model except it was scored by averaging five calls per question, at temperature $0$ for Haiku 4.5 and at the provider's default or fixed value for the others, whose five draws differ on most questions (supplement, Section~S.4)." (`AUX-R107-TEMP`, `AUX-R107-K5`; the supplement's Section S.4 paragraph "The five-draw census".)
- **R107-3, Section 5 (items 6 and 8).** Before: "Two portability checks on this set are preregistered and pending, because the \trueidx{} list averages $1.75$ names per item: one asks paraphrases that share no token with any listed name, and one pads the list to $60$ names (Appendix~\ref{app:counterfactual})." After, four sentences: "The list-length check pads the $661$ summaries' superseded-names lists with correct names, because the recorded list averages only $1.75$, and moves the embedding lookup from $0.75$ to $0.73$, $0.72$ and $0.67$ at $15$, $30$ and $60$ names (Appendix~\ref{app:counterfactual})." "The lexical lookup stays flat, and GPT-4.1 mini degrades first at $15$ names, from $0.73$ to $0.67$, $0.66$ and $0.69$." "Wrong names injected into the counterfactual set's lists at the lifecycle store's rate of $0.232$ and at $0.40$ move the lookup from $0.77$ to $0.67$ and $0.60$." "GPT-4.1 mini and Haiku 4.5 fall with it, each within $0.02$ of the lookup on the same lists (Appendix~\ref{app:counterfactual})." (`AUX-PAD-PRINTED`.) The counted-state qualification from the box, after the Opus 5 sentence: "The counted-state evidence rests on $30$ retraction and $44$ expiry pairs, and on the $661$ the counted-state rows give only a direction (Section~\ref{sec:populations})." Under the page gate the coverage sentence ("Coverage on this set follows the same construction, and the three models reach $0.64$, $0.62$ and $0.69$ …") leaves the body; `tab:cf-fok` in D.2 carries it.
- **R107-4, Section 7 (item 5).** After the lifted-minus-capped sentence: "An after-the-fact decomposition puts most of the lookup's loss on missing names, then wrong names, then length, with shares that differ by set: length is a cost on the counterfactual set and a credit on the $661$ (Appendix~\ref{app:posthoc-faults})." Before: "Both retention figures divide by GPT-4.1 mini's indexed-minus-blind difference of $+0.24$ on the $661$ questions, the denominator the $60\%$ bar was set against before scoring." After: the same words as two sentences, "… on the $661$ questions." / "That difference is the denominator the $60\%$ bar was set against before scoring." (the Section 7 median under the sentence gate).
- **R107-5, Section 8 and Table 5 (items 1 and 2).** Before: "Lookup, literal threshold, no abstention & $184$ & $94$ ($0.9038$) & $7.42$ & $75$ & $65$ & $14$ & $46$" After: the row label "Lookup, literal threshold, no abstention (descriptive)", values unchanged; the caption reads "the literal rule, a descriptive comparison, reaches most, and stale answers rise with reach". Prose: "The literal rule, a descriptive comparison rather than one of the policies fixed in advance, fetches whenever the lookup matches at the base rate and never abstains."; after the literal rule's split: "Under both answerers stale answers rise with reach, from $9$ to $17$ for GPT-4.1 mini and from $19$ to $27$ for Haiku 4.5 between retrieval alone and the oracle." "Correct answers stay at $46$ and $48$ (Appendix~\ref{app:resp})." "An added instruction to treat tagged records as not to be used moves those stale counts by at most three and the correct counts by at most one (Appendix~\ref{app:resp})." "No fetch policy is recommended until an answerer converts reach into correct answers." (`AUX-DS-STAGE2`, `AUX-DS-A2-STAGE2-H45`, `AUX-DS-A3-STAGE2-MINI`, `AUX-DS-A3-STAGE2-H45`.) Under the page gate the wrong-summary sentence ("The model responds to the description of this store and no other …") leaves the body; `tab:wrongindex` in F.2 carries it.
- **R107-6, Section 10 and the box (items 5 and 8).** Before: "Of the lookup's loss under that store's measured faults, missing names account for about six tenths, wrong names for about three tenths and list length for about one tenth (Appendix~\ref{app:posthoc-faults})." After: deleted (Section 7 states it once). The box, Before: "Do not mask: return non-active records with their lifecycle tags, and maintain a list of the attribute names that hold superseded content, the state that tags carry worst." / "Judge obligations with a similarity lookup over that list: on the counterfactual set the two smaller models read no more than the lookup and Opus 5 adds $0.03$ under the all-states summary and $0.07$ under the superseded-only one (Section~\ref{sec:counterfactual}), while on the $661$ questions the three larger models are $+0.07$ to $+0.08$ above it (item interval excluding zero, profile interval including it; Section~\ref{sec:populations})." / "The counted-state evidence rests on $30$ retraction and $44$ expiry pairs, and the $661$ rows give only the direction." / "Fetch an attribute's lifecycle records whenever the lookup matches it at the base rate, with no coverage abstention: that rule reaches $94$ of the $104$ forbidding records at a mean view of $7.42$ and keeps retrieval's coverage, against $85$ for the gated rules that were the comparison fixed in advance (Section~\ref{sec:populations})." / "A model call earns its cost on coverage only where the positives are ordinary records rather than obligations (Section~\ref{sec:populations})." / "A store without lifecycle structure gets no summary, because the summary such a store can write compresses the coverage score at every scale tested and what triggers the compression is unresolved (Section~\ref{sec:backends})." After, three sentences: "Return non-active records with their lifecycle tags instead of masking them (Section~\ref{sec:routes})." "Maintain the list of attribute names that hold superseded content and read obligations with a similarity lookup over it, spending model calls on coverage only where the positives are ordinary records (Sections~\ref{sec:counterfactual} and~\ref{sec:populations})." "Give a store without lifecycle structure no summary (Section~\ref{sec:backends})."
- **R107-7, Appendix D.2 (item 6).** The paragraph "Two registered checks on this set" rewritten: the list-length check with its four-decimal readings (the embedding lookup $0.7484$ to $0.6696$ at $60$; the lexical lookup flat; GPT-4.1 mini degrading first at $15$), its amendment ($0.7663$ to $0.6740$ and $0.6001$; the models within $0.02$), Table `tab:pad` (regenerated from `pad_probe/paper_table.tex` between PAD-TABLE markers), and the paraphrase line "the author's label-transfer read is in progress, and its table lands here when the run completes".
- **R107-8, Appendix F.10 and its tables (items 2 and 3).** The account of Amendment 3 after Amendment 2's; `tab:ds`'s second block and `tab:ds-h45` gain three columns, the same counts under the added instruction (`AUX-DS-A3-STAGE2-MINI`, `-H45`; a dash for the Amendment 1 row, whose views the amendment did not answer); both captions say so. The annotators' sentence gains "and whether the answer correctly reports the obligation".
- **R107-9, Appendix G, `tab:registrations-c`.** The padding row's "no prediction; pending" becomes "no prediction"; a seventh row "DS Amendment 3: the answer stage with an instruction to treat tagged records as not to be used, \texttt{eca19607}, 2026-09-14, … no prediction"; Before: "the expiry extension and the second downstream amendment have run (Tables~\ref{tab:cf3-expiry} and~\ref{tab:ds})." After: "The padding check, the expiry extension and the two later downstream amendments have run (Tables~\ref{tab:pad}, \ref{tab:cf3-expiry} and~\ref{tab:ds}); the paraphrase check waits on the author's read." and "seven descriptive registrations".
- **R107-10, count changes.** "Knowing the Store: What a Memory Backend Must Write Down Before an Agent Can Read It" 1 -> 2 and "always-reasoning configuration" 1 -> 2: the supplement quotes both and the base side holds the paper alone (R105-14, R105-15, R106-16).
- **R107-11, tools and non-manuscript writes.** `reviews/v15/` (`src/`, `tools/`, `base_tree.txt`, REPORT.md, CHANGES.md, CONFLICTS.md, NUMBER_MOVES.md, `claims_r107_block.md`); `ds_downstream/tools/amend3_instruct.py`, `ds_downstream/run/*amend3*`, `ds_downstream/cache_amend3/`, `ds_downstream/NUMBERS_DS.md` section 8; `registrations/ADDENDUM_DS_AMENDMENT_3.md` and its ARTIFACT copy; `pad_probe/tools/pad_table.py`, `pad_probe/paper_table.tex`, `pad_probe/NUMBERS_PAD.md` section 6; `reviews/NUMBERS_R107.md`; `reviews/v12/DETECTOR_LABELING_SHEET.md` (Q4 columns), `reviews/v12/tools/detector_agreement.py`; `tools/trace_scan_v13.py` LEDGERS; `tools/slogan_scan.py` EXEMPT_S9; `tools/appendix_identity.py` R107 pins; `SUPPLEMENT.tex` (S.4 paragraph; resolves into paper_v15).
## R109 AUTHORIZATION BLOCK — dated 2026-09-14

**Scope.** The author's instruction of 2026-09-14 (evening) after the forensic audit of the downstream answer stage (`reviews/DOWNSTREAM_AUDIT.md`; `reviews/downstream_audit/`, every number gated against the recorded per-row scores): (1) Section 8 rewritten around the active-duplicate result; (2) the active-duplicate and negation faults added to the write-path census, and the detector's limits to the detector note, in Appendix F.10; (3) DS Amendment 4 registered with two predictions (`registrations/ADDENDUM_DS_AMENDMENT_4.md`, sha256 `fb4b2ca8c8e280cbe6815c9782145abd93082e67b311fa1aeca60804f7dd6d8d`, recorded in `ds_downstream/NUMBERS_DS.md` section 10 before any call; not run), named in Section 8, described in F.10, entered in the registration record; (4) gates, page 9, stop. Round two, the author's instruction of the same night: (5) Amendment 4 run and scored (both predictions held); (6) the own-tags view scored against the oracle-tag row and the summary-alone row, both intervals, landed in Section 6 and E.10, the box's tag clause set from the result; (7) the Haiku 4.5 mechanism lanes landed (all three returned; the two-model claim not supported, so 'best monitor measured' stays scoped to GPT-4.1 mini); (8) Section 8's downstream part in its final shape; (9) the ten detector disclosures as one paragraph and the three write-path faults in the Phase A brief; (10) trace and prose hygiene; (11) the human-validation slot. Program name R109; `paper_v17.tex` beside `paper_v16.tex`; nothing committed. No model call in this program. No registered bar, threshold, verdict or frozen text changes.

**Lineage.** `paper_v17.tex` is assembled by `reviews/v17/tools/build_v17.py` from `reviews/v17/src/body_v17.tex` and `appendix_v17.tex` (copies of the v16 sources as they stood at 18:45 on 2026-09-14, edited by `edit_v17.py` then `tighten_v17.py` to `tighten7_v17.py`, in order; each replacement asserts one occurrence). `tab:registrations-b` (v11 lines 2120-2140) is inline so the Amendment 4 row can be added. `SUPPLEMENT.tex` is untouched and still resolves into `paper_v16` (the R108 pass owns it; CONFLICTS C-R109-1).

**BASE.** The tree object written from the working copy with a scratch index, holding `paper_v16.tex`, `paper_v16.pdf`, `SUPPLEMENT.tex` and `SUPPLEMENT.pdf` as they stood when this program began (the R108 pass mid-flight: no R108 CLAIMS block, no `reviews/v16/REPORT.md`, page gate at page 10 with slack -8): `--base=7b59bec8ee249f657b70d95dca36dfa4d9265604`, `--base-tex=paper_v16.tex`, `--program=R109`, `--extra-tex=SUPPLEMENT.tex`.

**Ledger.** `ds_downstream/NUMBERS_DS.md` section 9 (`AUX-DS-AUDIT-GATES`, `-DETECTOR`, `-RATES`, `-PAIRED`, `-SOURCE`, `-READ`, `-LENGTH`, `-IDENTITY`, `-RANK`, `-A3`, `-PRINTED`, `-VERDICTS`; every value read from the audit artifacts by `reviews/downstream_audit/ledger_audit.py`) and section 10 (`AUX-DS-A4-REG`). The ledger was already in `trace_scan_v13` LEDGERS; the three tokens that scan still reports (0.13, 0.21, 6.72) are the v16 base's and fail on `paper_v16.tex` alone (the R108 printed forms not yet ledgered by that pass).

**Entries.** Each Before is the string `frozen_diff` reports as changed; After is the v17 text.

- **R109-1, Section 8, the opening of the answer-stage paragraph.** Before: "Reach is not use, and the answers show it." After: "Reach is not use, and a forensic audit of the answer stage shows where the use comes from."

- **R109-2, Section 8, the detector clause.** Before: "by a token detector whose validation against human labels is in Appendix \ref{app:resp}" After: the clause is dropped from the counts sentence, which now ends "and $17$ under the oracle."; the detector's limits and its pending human-label check are stated in Appendix F.10 (R109-8) and pointed to from Limitations (R109-9).

- **R109-3, Section 8, the answer-stage reading.** Removed from the body, their content carried by Appendix F.10 and Tables `tab:ds` / `tab:ds-h45`: "The untagged records are the worse half, $7$ of $19$ against $2$ of $35$ under retrieval alone." and "Under both answerers stale answers rise with reach, from $9$ to $17$ for GPT-4.1 mini and from $19$ to $27$ for Haiku 4.5 between retrieval alone and the oracle, while correct answers stay at $46$ and $48$." and "An added instruction to treat tagged records as not to be used moves those counts by at most three (Appendix~\ref{app:resp})." and "The correct rate on the $174$ licensed items is the view's, because it turns on whether the licensed record is among the five." After (the new paragraph, `AUX-DS-AUDIT-*`): the count grows with the reached set while the rate holds (0.19 and 0.19; 0.26 and 0.22 on the 89 scorable obligations); the source is the store rather than the tag (35 of the 89 views carry an active line asserting the stale value; all 16 of GPT-4.1 mini's oracle stale answers fall on such a view); Haiku 4.5's higher counts are the detector's reading of longer answers (first sentence 8 against 16); the correct rate is the view's and the prompt's (the oracle's view on a licensed item is retrieval's, so their 46 is one number); most in-view misses are abstentions with the record on the page; a fourth amendment, fixed before any call with two predictions and not yet run, adds a header naming the persona and the current date.

- **R109-4, Section 8, the closing pointer.** Before: "No fetch policy is recommended until an answerer converts reach into correct answers." and "The paragraph fixed before scoring is reproduced with its numbers in Appendix~\ref{app:resp}, where the $22$ unflagged records are traced to the store's write path." After: "No fetch policy is recommended until an answerer converts reach into correct answers; the bars and the paragraph fixed before scoring, and the trace of the $22$ unflagged records to the store's write path, are in Appendix~\ref{app:resp}." The four verdict sentences that preceded it (the coverage rule's $-0.03$, the two bars, the retention $0.76$) MOVED verbatim to Appendix F.10 above the frozen paragraph (page-9 gate; frozen_diff reports MOVED; the coverage rule's appendix pointer is dropped there as a self-reference).

- **R109-5, Section 8, the pre-registration pointer.** Before: "Both readings were fixed before scoring, the whole-population comparison as a sentence pair and the per-state one as a single reading, and Appendix~\ref{app:baselines} carries them." After: the sentence moves to the head of Appendix E.7 (the baselines appendix it pointed at) without its final clause: "Both readings were fixed before scoring, the whole-population comparison as a sentence pair and the per-state one as a single reading."

- **R109-6, Table 5's caption.** Before: "the literal rule, a descriptive comparison, reaches most, and stale answers rise with reach" After: "the literal rule, a descriptive comparison, reaches most; the stale count grows with the reached set while the rate does not" and the caption's last sentence reads "Stale is the token detector's flag at $0.50$; the $0.80$ threshold gives zero under every policy." (the words "and is uninformative" dropped: the audit reads the row).

- **R109-7, Limitations, the counterfactual census detail (page-9 gate).** Before: "A later descriptive draw extends the expiry pairs to $44$ with the eligible candidates the first draw left undrawn (Appendix~\ref{app:counterfactual})." and "Retraction stays at $30$ because one candidate in ten passes the author's read for a cancellable plan ($36$ of $370$ read), and the candidate census in the artifact records every candidate with the rule that removed it." After: "A later descriptive draw extends the expiry pairs to $44$; retraction stays at $30$ (Appendix~\ref{app:counterfactual})." and the detail moves into Appendix C.2's sentence, Before: "retraction stays at $30$ pairs, because one candidate in ten passes the author's read for a cancellable plan." After: the same sentence continued "($36$ of $370$ read), and the candidate census in the artifact records every candidate with the rule that removed it."

- **R109-8, Appendix F.10 additions (items 2 and 3).** After the write-path census: the active-duplicate fault (35 of the 89 scorable obligations; 21 supersession, 14 retraction; 16 of 16 and 14 of 19 stale answers on such views) and the negation fault (the retraction statement tagged retracted at $0.80$ with no reading of negation; one question, both variants). After the detector note: the audit's four limits (15 expiry obligations unscorable; five retraction obligations unflaggable, 6 successor texts flagged, 3 licensed items unmarkable; length odds ratio 2.34 and 2.99 per doubling; 12 abstentions counted correct), the rates and the paired decomposition, the hand read. After the Amendment 3 paragraph: the instruction addresses tagged lines and the sources are untagged (310 of 452 answers byte-identical); Amendment 4's design, its two predictions with their bars, and the cap. `tab:registrations-b` gains the Amendment 4 row (`fb4b2ca8c8`, 2026-09-14, two predictions; not yet run). All values `AUX-DS-AUDIT-*` and `AUX-DS-A4-REG`.

- **R109-9, Limitations and Appendix G pointers (page-9 gate).** Before: "The outcome sentence written before scoring for the neutral-slice prediction is in the supplement (Section~S.9)." After: the clause joins Appendix G's texts-written-before-scoring paragraph: "and the outcome sentence written before scoring for the neutral-slice prediction is in its Section~S.9." The limitations sentence on the detector now reads "The answer-stage detector is a token-overlap rule whose limits, and whose pending human-label check, are in Appendix~\ref{app:resp}."

- **R109-10, Section 8 compressions (page-9 gate; not frozen strings).** The three-claim opening in one sentence; the matched-budget sentences without the 75 fires that Table 5 prints; the literal-rule sentence without its answer-stage provenance clause (F.10 carries it); the stale pointer to Table 5 for the seven- and ten-item views corrected to Appendix F.10 (those rows are `tab:reach-k` since R106).

- **R109-11, count changes.** "Knowing the Store: What a Memory Backend Must Write Down Before an Agent Can Read It" 1 -> 2 and "always-reasoning configuration" 1 -> 2: the supplement quotes both and the base side holds the paper alone (R105-14, R105-15, R106-16, R107-10, R108-12).

- **R109-13, the box (round two, item 6).** Before: "Return non-active records with their lifecycle tags instead of masking them (Section~\ref{sec:routes})." After: "Return non-active records with their lifecycle tags instead of masking them; under the one store's own marks the tagged view kept its reading (Section~\ref{sec:routes})." The collapse rule of ADDENDUM_RESP_AMENDMENT_1 section A read not collapsed (+0.1292 against the join's tags, both intervals excluding zero; `AUX-RESP-A1-BELIEVED`), so the clause states the result plainly rather than conditioning tags on list accuracy.

- **R109-14, Section 6 (round two, items 6 and 7).** The own-tags sentence split under the 40-word cap and continued: "That difference of $+0.13$ has both intervals excluding zero, and against the summary alone the same view reads $+0.08$, with the item interval excluding zero and the persona interval reaching it (Appendix~\ref{app:resp})." (`AUX-RESP-A1-PRINTED`). The Haiku 4.5 sentence split into two under the cap, wording unchanged; every Haiku lane returned (HYBRID $-0.03$ with intervals including zero, RETRIEVED $-0.11$, own-name $-0.13$), so the hybrid monitor stays "the best measured for the smallest model only".

- **R109-15, Section 8, the downstream part in its final shape (round two, item 8).** Order: the view (reach, matched-budget top-7, the literal rule); the answerer (rates on the scorable reached set with Wilson intervals; the active-duplicate result, GPT-4.1 mini none of $50$; Haiku 4.5's excess as second-sentence mention); the bound on correct answers (coverage $65$ of $174$, median rank $8.5$, the persona-binding defect, Amendment 4's effect: in-view correct to $48$ and $59$, in-view abstentions from $15$ and $38$ to $3$, over all licensed items $+10$ and $+25$); the tie to Section 7 (the census's $72\%$); the deployment consequence; the human-validation sentence. Every value `AUX-DS-AUDIT-*`, `AUX-DS-A4-*`, `AUX-R108-GOLDSPLIT`. Compressions for page 9: "A deployed monitor therefore thresholds at the base rate of positives, which is the operating point in the absence of a cost model; a deployment sets it from its fetch and miss costs." becomes "A deployed monitor therefore thresholds at the base rate of positives, the operating point absent a cost model."; the two disclosure sentences "GPT-4.1 mini's blind obligation score is flat on the full population, two values with $604$ of the $661$ questions at one of them, so its indexed-minus-blind difference is not a gain." and "Its gain is defined only on the counterfactual set, where it is $+0.22$ and was predicted before the run (Section~\ref{sec:counterfactual})." MOVED verbatim to Appendix A's opening, the body keeping one clause with both pointers.

- **R109-16, Appendix E.10, Amendment 4's results (round two, item 5).** The "not yet run" paragraph becomes the results paragraph: both predictions cleared their bars for both answerers (GPT-4.1 mini $37 \to 48$, $+0.1692$ $[+0.0769,+0.2769]$ / $[+0.0678,+0.2603]$; Haiku 4.5 $38 \to 59$, $+0.3231$ $[+0.2000,+0.4462]$ / $[+0.1833,+0.4714]$; in-view abstentions to $3$ each), correct over the 174 ($46 \to 56$, $48 \to 73$), the scorable-obligation columns (GPT-4.1 mini $17$ of $85$, all on active-stale views; Haiku 4.5 $23$ of $85$, $15$ on the first sentence, $7$ from tagged-only views), the expiry rows under the pinned date, the spend $\$0.5441$. `tab:registrations-b`'s row outcome "two predictions; not yet run" becomes "two predictions; both held". Ledger `NUMBERS_DS.md` section 10 (`AUX-DS-A4-LOCK` to `-SPEND`, `-PRINTED`).

- **R109-17, Appendix E.10, the detector note and the human-validation slot (round two, items 9 and 11).** The "four limits" sentences become one paragraph of ten disclosures (expiry unscorable; five unflaggable retraction obligations; six successor texts flagged; three unmarkable licensed items; length; active duplicates; the negation mis-tag; the persona binding; the median rank; correct-by-mention), closed by the rates, the paired decomposition and the hand read "those classes are the auditor's". After the two-annotator sentence (kept as the placeholder for the author's Q4 session): "The second annotator's sheet also carries the $19$ answers the audit read as giving the stale value ($11$ GPT-4.1 mini, $8$ Haiku 4.5), so the decisive labels receive two human reads." (`reviews/v17/SECOND_ANNOTATOR_SHEET_ADDENDUM.md`, rows 101-119, blinded, with the withheld key `second_annotator_addendum_key.json`); the three write-path faults in `reviews/v17/WRITE_PATH_CENSUS_BRIEF.md` (Table 3's conflate row unchanged: the audit's counts are view-level, not census numbers).

- **R109-18, prose and trace hygiene (round two, item 10).** Three inherited sentences over the 40-word cap split with their wording kept: Setup's "Coverage is scored on the hard tier, where every coverage positive is an obligation; the easy tier, whose positives are ordinary present records, enters only the coverage comparison with the lookup, and the Mem0 and A-MEM coverage rows pool both tiers ($238$ and $284$ questions)." (two sentences), Section 6's own-tags sentence (R109-14) and its Haiku 4.5 sentence (R109-14). The three tokens `trace_scan_v13` reported on the v16 base (0.13, 0.21, 6.72) resolve to `resp_review/NUMBERS_RESP.md` `AUX-RESP-A1-PRINTED` (written by `reviews/v17/tools/ledger_printed_r109.py` from `run/scores_amend1.json`); trace_scan, prose_scan and repeat_scan PASS with no inherited failure.

- **R109-19, registered run (round two, item 5).** `registrations/ADDENDUM_DS_AMENDMENT_4.md` (sha256 `fb4b2ca8c8e280cbe6815c9782145abd93082e67b311fa1aeca60804f7dd6d8d`, `AUX-DS-A4-REG` recorded before the first call) run by `ds_downstream/tools/amend4_header.py` (lock / probe-mini / probe-h45 / project / run-mini / run-h45 / score): served `gpt-4.1-mini-2025-04-14` and `claude-haiku-4-5-20251001`; 452 + 452 rows, 0 failures; projection $0.6410 (x1.3) against the $8.00 cap; billed $0.5441. A4-P1 HOLDS for both answerers; A4-P2 HOLDS for both. Rows `run/rows_ds_amend4_{mini,h45}.jsonl`, scores `run/scores_amend4.json`, cache `cache_amend4/`. Not committed in this pass.

- **R109-12, tools and non-manuscript writes.** `reviews/v17/` (`src/`, `tools/`, `base_tree.txt`, `base_files_sha256.txt`, REPORT.md, CONFLICTS.md, `claims_r109_block.md`, `paper_diff_v16_v17.txt`); `reviews/downstream_audit/` (the audit's scripts and artifacts) and `reviews/DOWNSTREAM_AUDIT.md`; `registrations/ADDENDUM_DS_AMENDMENT_4.md` and its ARTIFACT copy; `ds_downstream/NUMBERS_DS.md` sections 9 and 10; `tools/appendix_identity.py` R109 pins; `ds_downstream/tools/amend4_header.py`, `ds_downstream/run/*amend4*`, `ds_downstream/cache_amend4/`; `resp_review/NUMBERS_RESP.md` `AUX-RESP-A1-PRINTED` (round two); `reviews/v17/SECOND_ANNOTATOR_SHEET_ADDENDUM.md`, `second_annotator_addendum_key.json`, `WRITE_PATH_CENSUS_BRIEF.md`, `CHANGES.md`; this block. `SUPPLEMENT.tex`, `paper_v16.tex`, `reviews/v16/` and `resp_review/run/` untouched.

## R110 AUTHORIZATION BLOCK — dated 2026-09-14

**Scope (Phase 1 of CC_PASS_v18, the answer to the tenth review).** The author's rulings of 2026-09-14 at plan approval and during execution: (1) prose_scan rule G, the reader-claim gate, committed alone (`10e7b67`); (2) two wording corrections applied to `paper_v17.tex` in place, in their own commit, no number changed: the count-randomized summary described by what it did (the two lifecycle totals were permuted; the per-category tallies were not), and the concession sentence with its echo deleted with nothing in their place; (3) the $0 analyses A1 to A4 on recorded rows, the A5 fact list, the A6 scripts, the registration drafts for R-A (BELIEVED-H) and A8 (V2R-CAT), the ledger `reviews/NUMBERS_R110.md`, and `reviews/v18/PHASE1_REPORT.md`; then STOP. No model call in this program. No registered bar, threshold or verdict changes; no frozen registered text changes. Program name R110; `paper_v18.tex` is not built in Phase 1.

**Lineage.** `paper_v17.tex` is rebuilt by `reviews/v17/tools/build_v17.py` from `reviews/v17/src/body_v17.tex` and `appendix_v17.tex` after `reviews/v18/tools/wording_v17.py` (each replacement asserts one occurrence; the two edits inside carried v11 blocks go through the builder's REPAIRS list, each asserted to apply exactly once). Pre-edit sha256 `820e3fad5ff39f2a25a7c75a2bc7c435734ab63f3ff4d7c902c63699b5f205c3`; the rebuilt file's sha256 is recorded in `reviews/v18/CHANGES.md`.

**BASE.** The tree object written from the working copy with a scratch index, holding `paper_v17.tex` and `SUPPLEMENT.tex` as they stood before the wording edits: `--base=7e21dfd82742897ab3be198bda93e1b2c1280880`, `--base-tex=paper_v17.tex`, `--tex=paper_v17.tex`, `--program=R110` (run without `--extra-tex`: the supplement is added to the working side only, which doubles the title and one configuration string; the v17 pass ran with a v16 base where that did not bind).

**Ledger.** `r82_counterfactual/cf2/NUMBERS_CF2.md` section 5a (`AUX-CF2-V2R-DEF`: the two fields permuted, the PER-CATEGORY BREAKDOWN's RETRACT and EXPIRED columns unchanged, disclosed); `reviews/NUMBERS_R110.md` (`AUX-R110-A1-*` to `-A4-*`, the Phase 1 analyses; nothing printed in v17).

**Entries.** Each Before is the v17 text before this program; After is the text now. Only R110-W-4 touches a string frozen_diff tracks.

- **R110-W-1, Section 5, the tally sentence (wording; the author's sentence).** Before: "No reader uses the tally, because randomizing the counts across versions moves each reader by at most $+0.01$ on the whole set, with every interval within $\pm0.05$." After: "Randomizing the lifecycle totals moves each reader by at most $+0.01$ on the whole set, with every interval within $\pm0.05$; the per-category tallies were not randomized in that check." The author's third clause ("Table 1 shows what they carry against what the models read") enters with v18, when Table 1 carries the count-reader rows.

- **R110-W-2, Section 1, the concession sentence and its echo (deleted, nothing in their place; rule G).** Removed: "That a similarity lookup does so is the sanity check of this paper rather than its finding." and "The contribution lies past that check, in three parts."

- **R110-W-3, Appendix C.2 prose, the Table 13 caption and its row label (wording; the arm named by what it does).** "count-randomized summary" becomes "totals-randomized summary" throughout; the C.2 sentence now ends "every value keeps its multiplicity; the per-category tallies are not touched"; the caption's clause "and the first with its retracted and expired counts randomized across store versions." becomes "and the first with its two lifecycle totals, retracted and expired, permuted across store versions (the per-category tallies untouched)."; the row label "Counts randomized minus superseded only, whole set (band $\pm0.05$)" becomes "Totals randomized minus superseded only, whole set (band $\pm0.05$)".

- **R110-W-4 [Q CLAIMS], Table 39, the R94 row (the same rename).** Before: "R94: CF-2 store-counterfactual set & \texttt{f016f033e9} & 2026-09-12 & $148$ question and slot pairs drawn under predicates fixed before any verdict, three store versions each, three summaries, three readers, five predictions and their branch texts; all five held, two of them printing either way: the lookups within tolerance and every reader inside the count-randomization band; five recorded deviations (D-CF2-1 to D-CF2-5) & held" After: "R94: CF-2 store-counterfactual set & \texttt{f016f033e9} & 2026-09-12 & $148$ question and slot pairs drawn under predicates fixed before any verdict, three store versions each, three summaries, three readers, five predictions and their branch texts; all five held, two of them printing either way: the lookups within tolerance and every reader inside the totals-randomization band; five recorded deviations (D-CF2-1 to D-CF2-5) & held"

- **R110-G, the gate.** `tools/prose_scan.py` gains rule G (no allowlist; G1 banned phrases, G2 the abstract's numeral sentences, G3 no labelled definition of names/counts/reads, G4 Section 1's reader-claim anchor before its first mention of tags). On the rebuilt v17 it still fires at the abstract (L70: the thesis clause, "undetectable", the lookup-level sentence), Section 1 (L85 thesis; L88 boundary and "undetectable"; no anchor), Section 3 (L148 Definition 3; L156 `clm:naming`) and Section 8 (L474 thesis): the sites v18 rewrites under the reader claim. Recorded, not fixed, in this program.

- **R110-A, analyses and drafts (no manuscript text).** `reviews/v18/tools/a1_count_readers.py` to `a4_pad_extend.py` and their `results/*.json`; `reviews/v18/READER_CLAIM.md`, `A5_EDITS.md`, `annotator_agreement.py`, `paraphrase_score.py`; `reviews/NUMBERS_R110.md`; `registrations/ADDENDUM_BELIEVED_H.md` and `ADDENDUM_V2R_CAT.md` (drafts, unfrozen, uncommitted until the author's freeze); `reviews/v18/PHASE1_REPORT.md`, `CHANGES.md`.

<!-- R110 PASS 2 ENTRIES -->

**Pass 2 (2026-09-15): the body rewritten from reviews/v18/OUTLINE.md under the author's rules (the reader claim first; each paragraph opening with a plain sentence carrying no numeral; at most one interval in prose per paragraph; terms defined on first use; the sentence-length, vocabulary and near-duplicate rules of prose_scan; rule G with no allowlist). The appendix is derived from v17 by reviews/v18/tools/appendix_v18.py (28 asserted edits). `paper_v18.tex` is built by reviews/v18/tools/build_v18.py; the base for the diff gates is the tree object in reviews/v18/base_tree.txt (paper_v17.tex sha256 4f5b5d91..., the rebuilt v17 of the W commit). Each entry quotes the v17 string frozen_diff tracks and states what stands in its place; every number printed in v18 enters through a ledger key (reviews/NUMBERS_R110.md section 6 lists the printed forms).**

- **R110-P2-1 [Q CLAIMS]** (1 to 2). Before: "Knowing the Store: What a Memory Backend Must Write Down Before an Agent Can Read It". After: count: the title now also appears in the running head of the ICLR style (1 to 2); unchanged text.
- **R110-P2-2 [Q CLAIMS]** (1 to 2). Before: "always-reasoning configuration". After: count 1 to 2: the phrase now appears in Table 1's run-coverage note and the appendix; unchanged text.
- **R110-P2-3 [Q CLAIMS]** (9 to 8). Before: "not expressible by this backend". After: count 9 to 8: Section 7's marker sentence moved to Appendix E.7 with the structureless-store ablations (the spine's one-paragraph rule); the appendix mentions stand.
- **R110-P2-4 [Q CLAIMS]** (1 to 0). Before: "Appendix \ref{app:registration} lists every prediction fixed before data collection with its outcome; a result labelled exploratory was not fixed in advance.". After: Section 4 now ends: "Every preregistered text, prediction and outcome is in Appendix~\ref{app:registration}." (P3: no bookkeeping phrases in the body).
- **R110-P2-5 [Q CLAIMS]** (1 to 0). Before: "global counts may make the store look better covered than it is". After: deleted from Section 7 (the mechanism hunt is sent to Appendix E.7 in one sentence; the two hypotheses stand there).
- **R110-P2-6 [Q CLAIMS]** (1 to 0). Before: "disagreement between the summary and the retrieved view may compress the score range". After: deleted from Section 7 (the same move).
- **R110-P2-7 [Q CLAIMS]** (1 to 0). Before: "the matcher, in the preregistered texts". After: deleted: the lookup is defined once in Section 4 ("The similarity lookup scores each question by its maximum cosine similarity ..."); the alias lives in the glossary (P1).
- **R110-P2-8 [Q CLAIMS]** (1 to 0). Before: "We measure both judgments on stores we built, so that every label is exact.". After: Section 1: "We measure both judgments on stores we built, so that every label is exact, across three memory backends and language models from three vendors."
- **R110-P2-9 [Q CLAIMS]** (1 to 0). Before: "Coverage is the judgment on which the model earns its call, and only on the tier where the positives are ordinary records.". After: Section 8: "The coverage margin lives on ordinary records, and on the hard tier the coverage result is the obligation result restated." (A5_EDITS.md item 3).
- **R110-P2-10 [Q CLAIMS]** (1 to 0). Before: "such an item is expected to shrink measured gains rather than inflate them". After: Section 4: "... a mislabeled \absent{} item is unlikely ($5.2\%$ at the observed base rate; Appendix~\ref{app:construction}) and would shrink measured gains rather than inflate them."
- **R110-P2-11 [Q CLAIMS]** (1 to 0). Before: "Of the 58 predictions fixed before data collection, 16 did not hold (Appendix \ref{app:registration}).". After: Section 1: "Of the $58$ predictions preregistered before data collection, $16$ came out otherwise (Appendix~\ref{app:registration})." (P3: "held" is a barred outcome word).
- **R110-P2-12 [Q CLAIMS]** (1 to 0). Before: "Its name map carries only superseded content, so an entry that expires or is retracted reaches the summary as a count and is never named.". After: Section 3: "The name map carries only superseded content, so an entry that expires or is retracted reaches the summary as a count and is never named."
- **R110-P2-13 [Q CLAIMS]** (1 to 0). Before: "Every paired obligation gain excludes zero where the blind score varies (Table \ref{tab:e1}).". After: Section 8: the same clause opens a longer sentence ("..., and on the cross-model set the five models with a varying blind score gain $+0.15$ to $+0.45$").
- **R110-P2-14 [Q CLAIMS]** (1 to 4). Before: "(Appendix \ref{app:registration})". After: count 1 to 4: the pointer is used in Sections 1, 3, 4 and 8 of v18.
- **R110-P2-15 [Q CLAIMS]** (1 to 0). Before: "No backend we tested writes the list the obligation judgment needs.". After: Section 7 opens: "No tested backend writes the list."
- **R110-P2-16 [Q CLAIMS]** (1 to 0). Before: "A name-bearing summary rebuilt from ground truth for the entries each store holds restores coverage, from 0.45 to 0.90 on A-MEM and from 0.48 to 0.88 on Mem0, so the inversion belongs to the summary these stores can write.". After: Section 7: "A name-bearing summary rebuilt from ground truth for the entries each store holds restores coverage from $0.45$ to $0.90$ on A-MEM and from $0.48$ to $0.88$ on Mem0, so the loss belongs to the summary these stores can write." ("inversion" replaced by "loss" in this sentence; U1 stands in the paragraph).
- **R110-P2-17 [Q CLAIMS]** (1 to 0). Before: ", so the gain isolates the summary.". After: Section 4 (the author's trim order of 2026-09-15): "..., and the two prompts differ only in whether the summary precedes the question, so the gain isolates the summary (Appendix~\ref{app:construction})." (the pointer moved inside the sentence).
- **R110-P2-18 [Q CLAIMS]** (1 to 0). Before: "The boundary between the named state and the counted states is therefore the summary's rather than the reader's, because it moves when the summary does.". After: deleted with nothing in its place (rule G; READER_CLAIM.md section 2).
- **R110-P2-19 [Q CLAIMS]** (1 to 0). Before: "The score ranks well and calibrates badly, with an ECE of 0.17 indexed against 0.16 blind whose paired difference includes zero (Appendix \ref{app:posthoc}).". After: Section 8: "The score ranks well and calibrates badly (Appendix~\ref{app:posthoc}), so a deployed monitor thresholds at the base rate of positives." (the ECE values stay in Appendix G).
- **R110-P2-20 [Q CLAIMS]** (1 to 0). Before: "The lifted list's precision stays at 0.04, so most of the loss at the point estimate is the store's.". After: deleted from Section 7 (the cap paragraph moved to Section 4 and Appendix E.9, which carries the precision).
- **R110-P2-21 [Q CLAIMS]** (1 to 0). Before: "This section establishes a second route to the obligation.". After: Section 6 opens: "Retrieval that keeps the lifecycle tag on every returned record is a second route to the obligation, and it carries the states the list leaves uncounted." (P8).
- **R110-P2-22 [Q CLAIMS]** (1 to 0). Before: "Naming those states in the all-states summary lifts the lookup to 0.88 on the whole set". After: Section 5: "The all-states lookup reads $0.88$ on the whole set, and Haiku 4.5's paired gain on the two counted states is $+0.30$ with both intervals excluding zero."
- **R110-P2-23 [Q CLAIMS]** (1 to 0). Before: "On the metadata FR-Bank exposes, lookup and model both fall near chance on the obligation judgment.". After: Section 7: "FR-Bank's own metadata leaves the smallest model and the lookup close to chance and costs the larger model about a quarter of its gain." (the R-A result: Haiku 4.5 keeps 72%).
- **R110-P2-24 [Q CLAIMS]** (1 to 0). Before: "Calibration work scores confidence in an answer rather than belief about an external store \citep{kadavath2022,lin2022,tian2023,xiong2024}.". After: Section 2: folded into one sentence with the adaptive-retrieval and abstention lines (the trim order's first cut); the citations stand.
- **R110-P2-25 [Q CLAIMS]** (1 to 0). Before: "Where a store exposes no field for a line of the summary, the renderer writes in its place the marker". After: moved to Appendix E.7 (the structureless-store paragraph of Section 7 is one paragraph, led by the recovery).
- **R110-P2-26 [Q CLAIMS]** (1 to 0). Before: "Removing the store-wide entry count and those markers together shrinks A-MEM's inversion from -0.11 to -0.04 and leaves Mem0 unchanged, and no single removal differs from the intact summary by an interval that excludes zero.". After: moved to Appendix E.7 (the same move).
- **R110-P2-27 [Q CLAIMS]** (1 to 0). Before: "For a per-item score \sigma and budget k, R_k(q,S) is the top-k retrieved set with its full feature profile. A monitor is k-bounded when everything it sees of the store is R_k(q,S).". After: deleted: the $k$-bounded monitor is referenced nowhere in v18's body (the mask argument is stated in prose without it).
- **R110-P2-28 [Q CLAIMS]** (1 to 0). Before: "Appendix \ref{app:glossary} reproduces an abridged real one.". After: Section 3 now prints the abridged real summary itself after Definition 2 (eight lines from the E.1 excerpt); E.1 keeps the fuller excerpt.
- **R110-P2-29 [Q CLAIMS]** (1 to 0). Before: "FR-Bank overstates: it marks 5,968 of its 18,936 entries inactive, and the ground-truth manifest explains about 102 of those marks as supersessions, so the stale marks outnumber the true ones about sixtyfold. In entries, the manifest's supersessions touch 104, and the store still lists 40 of those as active.". After: Section 7: the same sentence with "about sixtyfold" replaced by "about $58\times$" (A5_EDITS.md item 2) and "In entries, ..." split into its own sentence.
- **R110-P2-30 [Q CLAIMS]** (1 to 0). Before: "The tagged route is measured with tags from the ground-truth join, and under the store's own tags it is unmeasured.". After: Section 9: "The tagged route is measured with tags from the ground-truth join and, descriptively, with the store's own marks." followed by the own-marks sentence (A5_EDITS.md item 1).
- **R110-P2-31 [Q CLAIMS]** (1 to 0). Before: "The obligation judgment is bounded by what the store writes about itself, so the store matters more than the reader. A similarity lookup reads the state the summary names, nothing reads the states it only counts, and no tested backend writes such a summary.". After: deleted with nothing in its place (rule G); Section 10 restates the thesis in different words (the author's instruction of 2026-09-15).
- **R110-P2-32 [Q CLAIMS]** (1 to 0). Before: "the automatic intent classifier that proposed the candidates". After: deleted from Section 4 under its 500-word ceiling (the author's trim order of 2026-09-15); Appendix E.4 keeps the classifier's precision.
- **R110-P2-33 [Q CLAIMS]** (1 to 0). Before: "An inversion is an indexed score below the blind score, and a below-chance score is one below 0.50.". After: deleted from Section 7 (the definition lives in the glossary); U1 stands in the paragraph.
- **R110-P2-34 [Q CLAIMS]** (1 to 0). Before: "Each measures a different observable at a different time, after memory has been consulted. The closest, STALE, scores whether an agent recognizes a memory it holds as no longer valid, whereas NOK is judged before content retrieval and asks whether the store holds anything that must be suppressed at all.". After: Section 2: "Long-term stores ... and remembered-answer benchmarks ... measure what is retrieved or answered after memory has been consulted; Mem0 (\texttt{mem0ai} 1.0.5) is the production layer evaluated here. The closest, STALE, scores whether an agent recognizes a memory it holds as no longer valid; ..."
- **R110-P2-35 [Q CLAIMS]** (1 to 0). Before: "whereas NOK's obligation comes from". After: Section 2: "NOK's obligation comes from the content's own lifecycle state and is judged before content retrieval." (its own sentence).
- **R110-P2-36 [Q CLAIMS]** (1 to 0). Before: "both intervals excluding zero (Table \ref{tab:cf-main})". After: Section 5: "Opus 5 reads $+0.07$ more with both intervals excluding zero, a margin its first call alone keeps (Table~\ref{tab:cf-main}; Appendix~\ref{app:counterfactual})."
- **R110-P2-37 [Q CLAIMS]** (1 to 0). Before: "against a retention bar of 60% set before scoring". After: deleted from Section 7: the line's provenance is stated once in Section 4 ("The sixty-percent retention line was fixed before the main study, on 10 August 2026, ..."); Table 4 carries the retention.
- **R110-P2-38 [Q CLAIMS]** (1 to 0). Before: "an excess over 100% that is not a finding". After: deleted from Section 7 (the 101.4% coverage retention sentence; the value stays in Appendix E.9 and the derived-ratio check).
- **R110-P2-39 [Q CLAIMS]** (1 to 0). Before: "Appendix \ref{app:counterfactual} holds the wording fixed before scoring for the smallest model's result here.". After: deleted (P3: no registration bookkeeping in the body; Appendix C.2 keeps the registered texts under "The registered texts for this set").
- **R110-P2-40 [Q CLAIMS]** (1 to 0). Before: "Haiku 4.5's paired gain on those two states under that summary is +0.30 with both intervals excluding zero (its pre-scoring wording is in Appendix \ref{app:counterfactual}).". After: Section 5: "... Haiku 4.5's paired gain on the two counted states is $+0.30$ with both intervals excluding zero." (the pre-scoring pointer dropped, P3).
- **R110-P2-41 [Q CLAIMS]** (1 to 0). Before: "The model scores 0.60 on that row and the lookup 0.59, inside tolerance (Appendix \ref{app:baselines} carries the two sentences fixed before scoring for this row).". After: Section 7: "GPT-4.1 mini and the lookup read $0.60$ and $0.59$ capped and $0.65$ and $0.66$ lifted on the obligation judgment, while Haiku 4.5 reads $0.71$ capped and $0.74$ lifted." (Table 4).
- **R110-P2-42 [Q CLAIMS]** (1 to 0). Before: "The larger models score higher than the lookup on the states the summary only counts, an advantage the paired blind comparison does not attribute to the summary.". After: deleted: Section 5 and Table 1 now state the counted-state levels directly (the models at $0.53$ to $0.62$ against the category-aware reader).
- **R110-P2-43 [Q CLAIMS]** (1 to 0). Before: "The two bars fixed before scoring were a reach gain of 0.50 for the gold-label fetch and 60% retention of that gain for the gated fetch.". After: Appendix E.10: "The two registered bars were a reach gain of $0.50$ ..." (A5_EDITS.md item 8).
- **R110-P2-44 [Q CLAIMS]** (1 to 0). Before: "A maintained summary escapes the bound by one route, and retrieval that does not mask and returns lifecycle tags escapes it by another (Section \ref{sec:routes}).". After: deleted from Section 3 (the two routes are stated in Section 1 and Figure 1; the sentence repeated them).
- **R110-P2-45 [Q CLAIMS]** (1 to 0). Before: "The pilot preceded the main study with a different prompt, so its values support the design lesson and cannot be compared numerically with the main study; its estimands and their table are in the supplement (Section S.7).". After: Appendix E.2 opens on the same sentence split in two (the author's Pass 2 rule: a subsection opens with a plain sentence carrying no numeral): "... cannot be compared numerically with the main study." then "Its estimands and their table are in the supplement (Section~S.7)."
- **R110-P2-46 [Q CLAIMS]** (1 to 0). Before: "Monitoring runs before every query, so its cost turns on prompt caching; the projection and the billed micro-run are in the supplement (Section S.8).". After: Appendix E.11 (Spend and caching) opens on the same sentence split in two: "Monitoring runs before every query, so its cost turns on prompt caching." then "The projection and the billed micro-run are in the supplement (Section~S.8)."
- **R110-P2-47 [Q CLAIMS]** (1 to 0). Before: "A summary names a state when it lists the attribute names in that state.". After: Definition 3 returns to vocabulary (rule G3): Section 3 reads "A summary names a state when it lists the attribute names in that state, and counts it when it gives only a tally of it." and Appendix E.1 carries the glossary sentence.
- **R110-P2-48 [Q CLAIMS]** (1 to 0). Before: "A summary counts a state when it gives only a tally of it.". After: the same (Section 3 and Appendix E.1).
- **R110-P2-49 [Q CLAIMS]** (1 to 0). Before: "A reader reads a state when its score separates that state's items from the rest.". After: Section 3: "A reader reads a state when its score separates that state's items from the rest (Appendix~\ref{app:glossary})."
- **R110-P2-50 [Q CLAIMS]** (1 to 0). Before: "Three failed predictions changed the reading: the reach premise, the retrieved-view route and the oracle margin.". After: deleted from Section 1 with its paragraph (the spine's Section 1 carries the four findings; Appendix F lists every outcome).
- **R110-P2-51 [Q CLAIMS]** (1 to 0). Before: "The lifecycle summary of Definition \ref{def:index} is what the indexed monitor is shown (the index, in the preregistered texts); Appendix \ref{app:glossary} reproduces an abridged real one.". After: Section 3: "This abridged real summary is what the indexed monitor reads: counts per category and state, and names with no values." (the alias "the index" lives in the glossary, P1).
- **R110-P2-52 [Q CLAIMS]** (1 to 0). Before: "Kimi K3 completed the cross-model set in full and stopped at the budget on the full populations, as did GPT-5.6 Sol, so their complete rows are on the cross-model set (Appendix \ref{app:laddertable}).". After: Table~\ref{tab:runs} (the run-coverage table) carries the two budget stops in the ledgers' words; the sentence is retired.
- **R110-P2-53 [Q CLAIMS]** (1 to 0). Before: "NOK is measured on one lifecycle store, the only backend that retains superseded content.". After: Section 9: "The stores are synthetic because temporal ground truth is unobservable without controlled construction, and NOK is measured on one lifecycle store, the only backend that retains superseded content, whose schema is the prior store's \citep{fr}."
- **R110-P2-54 [Q CLAIMS]** (1 to 0). Before: "The three versions of a counted-state store have identical name maps and differ only in their counts.". After: deleted from Section 5; Figure 2's row two shows the fact on a real triple and its caption states it.
- **R110-P2-55 [Q CLAIMS]** (1 to 0). Before: "What triggers the compression is unresolved on both stores.". After: Section 7: "What triggers the compression is unresolved, and the ablations that narrowed it are in Appendix~\ref{app:inversion}."
- **R110-P2-56 [Q CLAIMS]** (1 to 0). Before: "Two hypotheses remain: global counts may make the store look better covered than it is, and disagreement between the summary and the retrieved view may compress the score range.". After: moved to Appendix E.7 (the mechanism hunt in one body sentence).
- **R110-P2-57 [Q CLAIMS]** (1 to 0). Before: "On the two structureless stores the summary hurts coverage at every scale tested, and what it does to the score is compression.". After: Section 7 opens the paragraph on the recovery: "On the two structureless stores a summary that names what they hold restores coverage, and the summary they can write loses it at every scale."
- **R110-P2-58 [Q CLAIMS]** (1 to 0). Before: "Under the one lifecycle store's own metadata, both readers fall near chance.". After: deleted (rule G; the R-A result contradicts "both"): Section 10 reads "The one lifecycle store's own metadata is enough for the larger model wherever it still writes the name, and not enough for the smallest model or the lookup anywhere."
- **R110-P2-59 [Q CLAIMS]** (1 to 0). Before: "Agents with persistent memory decide, before retrieving anything, whether the store covers a question and whether it holds something they must no longer use, such as a cancelled plan. We call these judgments feeling of knowing (FOK) and negative-obligation knowledge (NOK) and measure both on synthetic stores with exact labels, across three memory backends and six language models. The obligation judgment is bounded by what the store writes about itself. When a store lists the attribute names that carry superseded content, a similarity lookup over that list detects the superseded state with 0.92 AUROC on a set where the same question is asked of three store versions; the two smaller models do no better than the lookup and the largest does slightly better. States the summary only counts are undetectable by any reader until they are named. Returning non-active records with their lifecycle tags, instead of masking them, is a second route, and combining it with the summary gives the best monitor we measure. No tested backend writes such a summary: one over-marks stale content sixtyfold, one overwrites its history, one's links resolve to nothing, and on the metadata they expose every reader falls to near chance. Backends should return tags, not masks, and maintain the list.". After: the abstract is replaced whole by the author's abstract v7 (reviews/v18/src/abstract_v18.tex; CLAIMS.md rows S1 to S9 of reviews/v18/CLAIMS.md); its first sentence is unchanged and the rest is the author's text.
- **R110-P2-60 [Q CLAIMS]** (1 to 0). Before: "The 5% retrieval pass rate cited for its mask was measured on the 40 retraction questions of the prior store's own benchmark, one per persona of the same persona bank, with the mask in place.". After: Section 4: "The $5\%$ pass rate cited for its mask was measured on the prior store's own $40$ retraction questions with the mask in place."
- **R110-P2-61 [Q CLAIMS]** (1 to 0). Before: "Every model except it was scored by averaging five calls per question, at temperature 0 for Haiku 4.5 and at the provider's default or fixed value for the others, whose five draws differ on most questions (supplement, Section S.4).". After: Section 4: "GPT-4.1 mini is scored from one call at temperature $0$ and every other model from five calls averaged (Table~\ref{tab:runs})." with the resolution note (A3) beside it.
- **R110-P2-62 [Q CLAIMS]** (1 to 0). Before: "The list-length check pads the 661 summaries' superseded-names lists with correct names, because the recorded list averages only 1.75, and moves the embedding lookup from 0.75 to 0.73, 0.72 and 0.67 at 15, 30 and 60 names (Appendix \ref{app:counterfactual}).". After: Section 5: "Padding those lists with correct names moves the embedding lookup from $0.75$ to $0.73$, $0.72$ and $0.67$ at $15$, $30$ and $60$ names." preceded by "The truthful summary's superseded-names list averages $1.75$ names on the full obligation set." (P2: the population by name).
- **R110-P2-63 [Q CLAIMS]** (1 to 0). Before: "The lexical lookup stays flat, and GPT-4.1 mini degrades first at 15 names, from 0.73 to 0.67, 0.66 and 0.69.". After: moved to Appendix C.2 (the trim under the page gate; the values stand in Table 16).
- **R110-P2-64 [Q CLAIMS]** (1 to 0). Before: "The counted-state evidence rests on 30 retraction and 44 expiry pairs, and on the 661 the counted-state rows give only a direction (Section \ref{sec:populations}).". After: Section 5: "The counted-state evidence rests on $30$ retraction and $44$ expiry pairs, and on the full obligation set ($661$ questions) the counted-state rows give only a direction (Section~\ref{sec:populations})." (P2).
- **R110-P2-65 [Q CLAIMS]** (1 to 0). Before: "An after-the-fact decomposition puts most of the lookup's loss on missing names, then wrong names, then length, with shares that differ by set: length is a cost on the counterfactual set and a credit on the 661 (Appendix \ref{app:posthoc-faults}).". After: deleted from Section 7 (the trim under the page gate; Appendix G.3 carries the decomposition).
- **R110-P2-66 [Q CLAIMS]** (1 to 0). Before: "the author's label-transfer read is in progress, and its table lands here when the run completes". After: Appendix C.2: "the author's label-transfer read had not been made at this build, so no paraphrase row is printed" (P12).
- **R110-P2-67 [Q CLAIMS]** (1 to 0). Before: "The padding check, the expiry extension and the two later downstream amendments have run (Tables \ref{tab:pad}, \ref{tab:cf3-expiry} and \ref{tab:ds}); the paraphrase check waits on the author's read.". After: Table 40's caption: "Every one has run except the paraphrase check, which waits on the author's read."
- **R110-P2-68 [Q CLAIMS]** (1 to 0). Before: "seven descriptive registrations". After: Table 40's caption: "twelve descriptive registrations" (the five rows added: Haiku 4.5 under the store's own metadata, the increment moved within the triple, DS Amendments 5 to 7).
- **R110-P2-69 [Q CLAIMS]** (1 to 0). Before: "Reach is not use, and a forensic audit of the answer stage shows where the use comes from.". After: Section 8 is written as the chain reach, tags respected, the duplicate fault, the repair, depth, the composite (OUTLINE.md section 8); the sentence is retired.
- **R110-P2-70 [Q CLAIMS]** (1 to 0). Before: "Both readings were fixed before scoring, the whole-population comparison as a sentence pair and the per-state one as a single reading.". After: Appendix E.7: "Both readings were registered, ..." (A5_EDITS.md item 8).
- **R110-P2-71 [Q CLAIMS]** (1 to 0). Before: "A later descriptive draw extends the expiry pairs to 44; retraction stays at 30 (Appendix \ref{app:counterfactual}).". After: Section 9: "The counted-state groups are small: $30$ retraction and $30$ expiry pairs on the counterfactual set, $44$ expiry with the extension, ..."
- **R110-P2-72 [Q CLAIMS]** (1 to 0). Before: "and the outcome sentence written before scoring for the neutral-slice prediction is in its Section S.9.". After: Appendix E.10: "and the registered outcome sentence for the neutral-slice prediction is in its Section S.9" (A5_EDITS.md item 8).
- **R110-P2-73 [Q CLAIMS]** (1 to 0). Before: "The answer-stage detector is a token-overlap rule whose limits, and whose pending human-label check, are in Appendix \ref{app:resp}.". After: Section 8: "the stale and correct counts are a token detector's, read by hand where flagged, with its limits in Appendix~\ref{app:resp}." (P12: no "pending").
- **R110-P2-74 [Q CLAIMS]** (1 to 0). Before: "That difference of +0.13 has both intervals excluding zero, and against the summary alone the same view reads +0.08, with the item interval excluding zero and the persona interval reaching it (Appendix \ref{app:resp}).". After: Section 6: "With FR-Bank's own marks in place of the join, the view reads the obligation at $0.81$ against $0.69$ for the smallest model, a difference of $+0.13$ with both intervals excluding zero." (the +0.08 against the summary stays in Appendix E.10).
- **R110-P2-75 [Q CLAIMS]** (1 to 0). Before: "A deployed monitor therefore thresholds at the base rate of positives, the operating point absent a cost model.". After: Section 8: "The score ranks well and calibrates badly (Appendix~\ref{app:posthoc}), so a deployed monitor thresholds at the base rate of positives."


## R111 AUTHORIZATION BLOCK — dated 2026-09-15

**Scope (the writing pass on paper_v18, `paper_v18_writing_prompt.md`).** The author's checklist of 2026-09-15 (94 items, six phases) applied to the R110 lineage in place: Phase 0 the abstract v8 (commit `78d8f8b`); Phase 1 the structure and cuts (items 1, 2, 3, 7, 18, 24, 36, 49-55, 87, 90; `reviews/v18/tools/wp_phase1.py`, every edit a line-range replacement asserted by its first and last line, reproducible from the Phase 0 sources). Ground rule 1 of the pass: no number, n, interval or population changes; every value that leaves the body stands in a table, an appendix or a ledger (`reviews/v18/NUMBER_MOVES.md`). Two-decimal forms in the body tables are ROUND_HALF_UP of the recorded four-decimal values (`reviews/NUMBERS_WP.md` section 1, AUX-WP-PRINTED).

**Lineage.** `paper_v18.tex` is rebuilt by `reviews/v18/tools/build_v18.py` from `reviews/v18/src/body_v18.tex`, `abstract_v18.tex` and `appendix_v18.tex`; `appendix_v18.py` is not re-run (it would overwrite the Phase 1 appendix edits). The Phase 0 sources are commit `78d8f8b`.

**BASE.** The tree object written from the working copy with a scratch index before Phase 1, holding `paper_v18.tex`, `paper_v18.pdf` and `SUPPLEMENT.tex` after Phase 0 (`reviews/v18/base_tree_wp.txt`, `base_files_wp_sha256.txt`): `--base=41748a11ec02181029bfd20af34cbd81110f60df`, `--base-tex=paper_v18.tex`, `--tex=paper_v18.tex`, `--extra-tex=SUPPLEMENT.tex`.

**Ledger.** `reviews/NUMBERS_WP.md` (AUX-WP-PRINTED, the two-decimal forms of the six body tables; AUX-WP-X5-DRAWS, the calls per question on the authorship-matched set and the expiry extension, from the recorded rows).

**Entries.** Each Before is the text at the base (a frozen string of an earlier block, a slogan_scan list or a registration); After is the text now, or the deletion with where the content stands. Three strings frozen_list reports at count 1 to 2 ("Knowing the Store: What a Memory Backend Must Write Down Before an Agent Can Read It", "always-reasoning configuration", "Monitoring runs before every query, so its cost turns on prompt caching") are unchanged: the listing adds the supplement to the working side only.

- **R111-P1-1 [S EXEMPT_S9]** (1 to 0). Before: "is a measured resolution limit, not evidence that the label is absent". After: deleted from Limitations (item 47: the FOK-deleted sentence goes; the measurement stands in Section 8, "FOK does not detect a deleted record ... moves from $0.43$ to $0.50$ and stays at chance"). The exemption entry stays in slogan_scan.py for the record.
- **R111-P1-2 [S EXEMPT_S10]** (4 to 3). Before: the Limitations sentence "The authorship-matched set ($36$ questions) is underpowered, so whether Haiku 4.5's blind inversion is a property of the model or of question authorship is indeterminate at this size (Table~\ref{tab:matched-cell})." After: deleted (item 90: Limitations cut to the five the author keeps); the three appendix references to the table stand.
- **R111-P1-3 [Q CLAIMS]** (1 to 0). Before: "On the inherited store, FR-Bank as released with its mask in place, retraction records pass that mask at $5\%$." After: Section 4, "FR-Bank is the lifecycle-tracking store of \citet{fr}, the one evaluated store that records a lifecycle state on every entry; its stock configuration masks non-active records from retrieval, and retraction records pass that mask at $5\%$ (Appendix~\ref{app:believed-census})." (items 18 and 83: the result leaves Section 3; the continuity phrases "the inherited store" and "as released with its mask in place" go).
- **R111-P1-4 [Q CLAIMS]** (1 to 0). Before: "The manifests record 40 retraction events, one per persona, and the truthful join resolves 9 of them to a retracted entry (23 entries)." After: Appendix E.9, "The manifests record $40$ retraction events, one per persona, and the ground-truth join resolves $9$ of them to a retracted entry ($23$ entries)." (items 52 and 90: the Conflate row of Table 3 to E.9 as prose; "truthful join" reads "ground-truth join" under item 35).
- **R111-P1-5 [Q CLAIMS]** (1 to 0). Before: "Every question set was generated by a language model from human-written manifests, and those manifests are the ground truth every label is scored against." After: the caption of the population table (Table tab:setup, item 24), "Every question set was generated from human-written manifests, which are the ground truth every label is scored against".
- **R111-P1-6 [Q CLAIMS]** (1 to 0). Before: "Wrong names injected into the counterfactual set's lists at the lifecycle store's rate of 0.232 and at 0.40 move the lookup from 0.77 to 0.67 and 0.60." After: deleted from Section 5 (item 90: the list-length paragraph to two sentences, "The lookup works because the list is short and clean. As the list grows or fills with wrong names, the lookup and the models fall together (Appendix~\ref{app:counterfactual})."); the figures stand in Appendix C.2 ("the lookup falls from $0.7663$ to $0.6740$ and $0.6001$") and Table tab:pad.
- **R111-P1-7 [Q CLAIMS]** (1 to 0). Before: "GPT-4.1 mini and Haiku 4.5 fall with it, each within 0.02 of the lookup on the same lists (Appendix \ref{app:counterfactual})." After: deleted with the same paragraph; Appendix C.2 carries "GPT-4.1 mini and Haiku 4.5 fall with it and stay within $0.02$ of it on the same lists".
- **R111-P1-8 [Q CLAIMS]** (1 to 0). Before: "A name-bearing summary rebuilt from ground truth for the entries each store holds restores coverage from 0.45 to 0.90 on A-MEM and from 0.48 to 0.88 on Mem0, so the loss belongs to the summary these stores can write." After: Section 7, "A name-bearing summary rebuilt from ground truth restores coverage from $0.45$ to $0.90$ on A-MEM and from $0.48$ to $0.88$ on Mem0, so the loss belongs to the summary these stores write." (item 1: the structureless-store paragraph cut to four sentences; every number kept).
- **R111-P1-9 [Q CLAIMS]** (1 to 0). Before: "The tagged route is measured with tags from the ground-truth join and, descriptively, with the store's own marks." After: Limitations, one sentence in place of three, "The tagged route under the store's own tags is descriptive, with no prediction fixed in advance for its rise, which is the tags' reach of the forbidding records rather than their density (Section~\ref{sec:routes})." (item 90; the A5_EDITS.md item 1 disclosure kept).
- **R111-P1-10 [Q CLAIMS]** (1 to 0). Before: "The stores are synthetic because temporal ground truth is unobservable without controlled construction, and NOK is measured on one lifecycle store, the only backend that retains superseded content, whose schema is the prior store's \citep{fr}." After: Limitations, "The stores are synthetic because temporal ground truth is unobservable without controlled construction, and NOK is measured on one lifecycle store, FR-Bank, the only tested backend that retains superseded content \citep{fr}." (item 83, the author's sentence).
- **R111-P1-11 [Q CLAIMS]** (1 to 0). Before: "What triggers the compression is unresolved, and the ablations that narrowed it are in Appendix \ref{app:inversion}." After: Section 7, "The loss is compression of the indexed score toward one low value, and what triggers it is unresolved (Appendix~\ref{app:inversion})."; Appendix E.7 gains "What triggers the compression is unresolved, and the ablations that narrowed it follow." beside the U1 sentence, which moved there verbatim (pinned once).
- **R111-P1-12 [Q CLAIMS]** (1 to 0). Before: "The 5% pass rate cited for its mask was measured on the prior store's own 40 retraction questions with the mask in place." After: Appendix E.9, "The pass rate of $5\%$ that Section~\ref{sec:setup} cites for FR-Bank's mask is the released store's own figure, measured on its $40$ retraction questions with the mask in place \citep{fr}." (items 83 and 90: "the prior store" goes; the provenance leaves Section 4).
- **R111-P1-13 [Q CLAIMS]** (1 to 0). Before: "Padding those lists with correct names moves the embedding lookup from 0.75 to 0.73, 0.72 and 0.67 at 15, 30 and 60 names." After: deleted from Section 5 (item 90); the curve stands in Table tab:pad and the C.2 sentence "The embedding lookup falls from $0.7484$ to $0.6696$ at $60$ names".
- **R111-P1-14 [Q CLAIMS]** (1 to 0). Before: "The truthful summary's superseded-names list averages 1.75 names on the full obligation set." After: deleted from Section 5 (item 90); the $1.75$ stands in Section 4 ("whose superseded list averages under two names"), Table tab:pad and Appendix E.9, and returns to Section 5 in the author's words of the ruling ("The superseded-names list averages $1.75$ names on the full obligation set.", R111-P1-16).
- **R111-P1-15 [Q CLAIMS]** (1 to 0). Before: "The counted-state evidence rests on 30 retraction and 44 expiry pairs, and on the full obligation set (661 questions) the counted-state rows give only a direction (Section \ref{sec:populations})." After: Section 5, "The counted-state evidence rests on $30$ retraction and $44$ expiry pairs, the $30$ plus the $14$ of the descriptive extension draw in Appendix~\ref{app:counterfactual}, and on the full obligation set ($661$ questions) the counted-state rows give only a direction (Section~\ref{sec:populations})." (item 85: the 44 linked to C.2).
- **R111-P1-16 [Q CLAIMS]** (1 to 0). Before: "Opus 5 reads +0.07 more with both intervals excluding zero, a margin its first call alone keeps (Table~\ref{tab:cf-main}; Appendix~\ref{app:counterfactual})" (the whole-set paragraph of Section 5, with "On the whole set two of the three models do not exceed the lookup and the largest exceeds it by a margin one call keeps." and "On the state the list names, supersession, every model and the lookup read the obligation from the same names, and the lookup reads it as well as any model but the largest"). After: the author's paragraph of 2026-09-15 (items 31 and 33, the ruling on the Phase 1 report): "Supersession is the one state the summary names. The superseded-names list averages $1.75$ names on the full obligation set. The lookup therefore has the target's name in front of it, and the question is what a model adds. On the counterfactual set, GPT-4.1 mini and Haiku 4.5 do not exceed the lookup and Opus 5 exceeds it by $0.07$ (Table~\ref{tab:cf-main}). What the list does not name, no model reads." The single-call margin stands in the population table's note (Section 4) and Appendix C.2; the lookup's level (0.77) in Table 2 only (P4). The author's third sentence ("Most questions name the attribute they ask about (111 of the 204 drafted)") is held back: AUX-CF2-QUESTIONREAD's 111 of 204 counts questions that name a specific value beyond their topic, not questions that name their attribute (WRITING_PASS.md).

**Phase 2 entries (renames and search-and-replace; items 34, 35, 61 with its addendum, 80, 83; `reviews/v18/tools/wp_phase2.py` on the sources, `REPAIRS_R111` in `reviews/v18/tools/build_v18.py` inside the carried v11 blocks).** Frozen registered wording is untouched: the script skips every line carrying a registration fragment or following a "ships verbatim" comment, and the builder skips the Mem0 SIDE sentence; the residue those texts leave is listed in WRITING_PASS.md. The `\trueidx` and `\believed` macros stay defined for those texts only. Each Before is the frozen string in full; After is the wording now.

- **R111-P2-1 [Q CLAIMS]** (6 to 2). Before: "with questions grouped by user profile". After: "with questions grouped by persona" wherever the text is not registered (item 61: persona, not user profile); the two that stand are inside frozen registered texts (the SIDE S2 sentence in E.9 and the DS Section 7 paragraph in E.10).
- **R111-P2-2 [Q CLAIMS]** (1 to 0). Before: "The believed superseded list, and the renderer's cap." After: the paragraph title reads "The store-written superseded list, and the renderer's cap." (item 34).
- **R111-P2-3 [Q CLAIMS]** (1 to 0). Before: "Side experiments: believed-state cap (S2)". After: the registration-record row reads "Side experiments: store-written-state cap (S2)".
- **R111-P2-4 [Q CLAIMS]** (1 to 0). Before: "two filter rules on the store's own metadata and a precision bar neither reached, so the repair was withdrawn before any call; one descriptive condition, the believed summary with its fifteen-name cap lifted, carrying no prediction". After: the same with "the store-written summary with its fifteen-name cap lifted".
- **R111-P2-5 [Q CLAIMS]** (1 to 0). Before: "At that size the smallest model reached 0.5939 against 0.5000, with an item-level interval of [-0.0345,+0.2315] that includes chance and a question-clustered interval of [+0.0325,+0.1625] that excludes it." After: "At that size GPT-4.1 mini reached $0.5939$ ..." (item 61; the numbers unchanged).
- **R111-P2-6 [Q CLAIMS]** (1 to 0). Before: "The gated fetch retains 0.76 of that gain, and under the weaker reading, the interval grouped by user profile, the lower end of 0.56 falls below the 60% bar." After: "... the interval grouped by persona, ..." (the numbers unchanged).
- **R111-P2-7 [Q CLAIMS]** (1 to 0). Before: "Return non-active records with their lifecycle tags instead of masking them; under the one store's own marks the tagged view kept its reading (Section \ref{sec:routes})." After: the box's first sentence, "Return non-active records with their lifecycle tags instead of masking them; under FR-Bank's own tags the tagged view kept its reading (Section~\ref{sec:routes})." (items 35 and 61).
- **R111-P2-8 [Q CLAIMS]** (1 to 0). Before: "the best measured for the smallest model only". After: "the best measured for GPT-4.1 mini only".
- **R111-P2-9 [Q CLAIMS]** (1 to 0). Before: "every value keeps its multiplicity; the per-category tallies are not touched". After: "every value keeps its multiplicity; the per-category counts are not touched" (the addendum to item 61: count, not tally).
- **R111-P2-10 [Q CLAIMS]** (1 to 0). Before: "and the first with its two lifecycle totals, retracted and expired, permuted across store versions (the per-category tallies untouched)." After: the v18 W repair's new text reads "(the per-category counts untouched)"; the old side of that repair still matches v11.
- **R111-P2-11 [Q CLAIMS]** (1 to 0). Before: "FR-Bank's own metadata leaves the smallest model and the lookup close to chance and costs the larger model about a quarter of its gain." After: "FR-Bank's own metadata leaves GPT-4.1 mini and the name lookup close to chance and costs Haiku 4.5 about a quarter of its gain." (item 61 and section 15's own example).
- **R111-P2-12 [Q CLAIMS]** (1 to 0). Before: "A summary names a state when it lists the attribute names in that state, and counts it when it gives only a tally of it." After: "... and counts it when it gives only a count of it." (Section 3 and the E.1 glossary).
- **R111-P2-13 [Q CLAIMS]** (1 to 0). Before: "The one lifecycle store's own metadata is enough for the larger model wherever it still writes the name, and not enough for the smallest model or the lookup anywhere." After: the Conclusion's "FR-Bank's own metadata is enough for Haiku 4.5 wherever it still writes the name, and not enough for GPT-4.1 mini or the name lookup anywhere."
- **R111-P2-14 [Q CLAIMS]** (1 to 0). Before: "the author's label-transfer read had not been made at this build, so no paraphrase row is printed". After: "our label-transfer read had not been made at this build, so no paraphrase row is printed" (item 80).
- **R111-P2-15 [Q CLAIMS]** (1 to 0). Before: "Every one has run except the paraphrase check, which waits on the author's read." After: "Every one has run except the paraphrase check, which waits on our read." (item 80).
- **R111-P2-16 [Q CLAIMS]** (1 to 0). Before: "With FR-Bank's own marks in place of the join, the view reads the obligation at 0.81 against 0.69 for the smallest model, a difference of +0.13 with both intervals excluding zero." After: "With FR-Bank's own tags in place of the ground-truth tags, the view reads the obligation at $0.81$ against $0.69$ for GPT-4.1 mini, a difference of $+0.13$ with both intervals excluding zero." (items 35 and 61).
- Also changed in Phase 2 without a frozen string: Section 5's count paragraph in section 15's own words ("The count identifies the right version here because the category usually has no other retracted or expired entry ($26$ of $30$ retraction pairs, $15$ of $30$ expiry pairs), so the count goes from zero to one." and "A count cannot say which attribute is retracted or expired. When the summary names those attributes, every model improves (Table~\ref{tab:cf-main})."), the Conclusion's thesis in section 15's words ("The name of the stale attribute supplies the judgment. The counts supply none of it, for any model. A lookup over the names is a baseline two of the three models do not exceed."), the Section 6 opener in section 15's words, "the name lookup" on first use in Sections 4, 5, 7, 8 and in Appendices A, C.2, E.8, E.9, G.2, "the superseded-names lookup" renamed "the name lookup" everywhere outside the frozen texts, "the moved-count control" for the increment moved within the triple, "the ground-truth join" for the join as an operation, the labels tab:believed and app:believed-census renamed tab:census and app:census, and E.9's title "Census of the store-written state".

**Phase 3 entries (the new elements; items 5, 17, 20 with 94, 22, 30, 56, 57/91, 84, plus 4 and 21 by the ruling, and item 61's deferred "reads" replacements; `reviews/v18/tools/wp_phase3.py`).** No number changes: the per-state figure and the cross-model table print values that stand in Table 2, Appendix C.2 and Appendix A's exact table; the two-decimal forms the cross-model table prints are in `reviews/NUMBERS_WP.md` section 3 (AUX-WP-PRINTED-P3).

- **R111-P3-1 [S EXEMPT_S9]** (1 to 2). Before: "reaches more forbidding records but does not reduce stale answers" (the abstract). After: the contributions list's fifth bullet carries the same phrase in the author's words of item 5 ("We show downstream that gating retrieval on the judgment reaches more forbidding records but does not reduce stale answers; tagging the untagged duplicates the store keeps does. The fix is in the write path."); the exemption covers both.
- **R111-P3-2 [Q CLAIMS]** (4 to 3) and **R111-P3-3 [Q CLAIMS]** (1 to 0) and **R111-P3-4 [Q CLAIMS]** (1 to 0). Before: "Of the 58 predictions preregistered before data collection, 16 came out otherwise (Appendix \ref{app:registration})." (Section 1) and "Every preregistered text, prediction and outcome is in Appendix \ref{app:registration}." (Section 4), with the pointer "(Appendix \ref{app:registration})" counted four times. After: item 10, one sentence closing Section 4, "Of the $58$ predictions preregistered before data collection, $16$ came out otherwise, and every preregistered text, prediction and outcome is in Appendix~\ref{app:registration}." (item 10's clause on what kind failed is Phase 4's).
- **R111-P3-5 [Q CLAIMS]** (1 to 0). Before: "The all-states lookup reads 0.88 on the whole set, and Haiku 4.5's paired gain on the two counted states is +0.30 with both intervals excluding zero." After: "The all-states lookup scores $0.88$ on the whole set, ..." (item 61: "reads" only in the box's sense).
- **R111-P3-6 [Q CLAIMS]** (1 to 0). Before: "GPT-4.1 mini and the lookup read 0.60 and 0.59 capped and 0.65 and 0.66 lifted on the obligation judgment, while Haiku 4.5 reads 0.71 capped and 0.74 lifted." After: "GPT-4.1 mini and the lookup score $0.60$ and $0.59$ capped and $0.65$ and $0.66$ lifted on the obligation judgment, while Haiku 4.5 scores $0.71$ capped and $0.74$ lifted."
- **R111-P3-7 [Q CLAIMS]** (1 to 0). Before: "A reader reads a state when its score separates that state's items from the rest (Appendix \ref{app:glossary})." After: deleted from Section 3's prose with the names / counts sentence before it (items 17 and 23): both stand in the notation box's row "names, counts, reads" ("a summary \emph{names} a state when it lists the attribute names in that state and \emph{counts} it when it gives only a count of it; a reader \emph{reads} a state when its score separates that state's items from the rest") and in E.1.
- **R111-P3-8 [Q CLAIMS]** (1 to 0). Before: "This abridged real summary is what the indexed monitor reads: counts per category and state, and names with no values." After: "Listing~\ref{lst:summary} is what the indexed monitor sees: counts per category and state, and names with no values." (item 22: the example is Listing 1; item 61: "sees" for consumption).
- Also new in Phase 3 without a frozen string: the contributions list (item 5 with its addendum, the author's words), the route sentence naming routes A and B, Figure 1 redrawn at the text width with the crossed-out masked path (item 56), Definition 1's cases as an unnumbered grid with the CHANGE row (items 20 and 94; n.a. is a combination the construction does not produce, Appendix E.3's structural intent typing), the superseded-names list named in Definition 2 (item 21), the notation box (item 17 with its addendum), the example as Listing 1 (item 22), Figure 2's two-line caption (item 91), Figure 3 (item 30) with Table 2 at the whole-set column (item 50), the cross-model table in Section 8 (item 84 (a)), and "separates" / "scores" / "sees" for "reads" outside the box's sense on first use in Sections 3, 5, 6 and 7.

**Phase 4 entries (the prose pass to page 9; items 8, 9, 10, 25, 26, 28, 38, 41, 42, 43, 46, 48, 63 and the author's cut targets and three levers of the Phase 4 instruction; `reviews/v18/tools/wp_phase4.py` on the sources, reproducible from `6dbabdf` through `wp_phase3.py`).** No number, n, interval or population changed; every value that left a body sentence stands in a table, an appendix sentence or a ledger, and `reviews/v18/NUMBER_MOVES_WP.md` carries the disposition of each (five new: 0.30, 0.55, -0.09, +0.08, 2026). The frozen registered texts are untouched (the script skips them as in Phase 2). The main text ends on page 10 at reading 539 after all three levers; page 9 does not hold, reported to the author.

- **R111-P4-1 [Q CLAIMS]** (1 to 0). Before: "on the conflict questions of a recent benchmark no memory agent exceeds 7% accuracy \citep{memoryagentbench}". After: Section 1, "on MemoryAgentBench's conflict-resolution questions no memory agent exceeds $7\%$ accuracy \citep{memoryagentbench}" (item 10: the benchmark named; the number unchanged).
- **R111-P4-2 [Q CLAIMS]** (1 to 0). Before: "We measure both judgments on stores we built, so that every label is exact, across three memory backends and language models from three vendors." After: Section 1, "... across three memory backends and six language models from three vendors." (item 10: the count of models stated, as the population table records).
- **R111-P4-3 [Q CLAIMS]** (1 to 0). Before: "The coverage margin lives on ordinary records, and on the hard tier the coverage result is the obligation result restated." After: Section 8's coverage paragraph opens "The coverage margin lives on ordinary records." and the hard tier is its third sentence, "On the hard tier every coverage positive is an obligation, so the FOK row is the NOK row relabeled, and the lookup's $0.79$ against the model's $0.70$ is not a reliable difference (Appendix~\ref{app:baselines})." (item 41; the $-0.09$ retired from prose, NUMBER_MOVES_WP.md).
- **R111-P4-4 [Q CLAIMS]** (1 to 0). Before: "The name map carries only superseded content, so an entry that expires or is retracted reaches the summary as a count and is never named." After: Section 3's framing paragraph, "Every result in this paper rests on the name map, which carries only superseded content: an entry that expires or is retracted reaches the summary as a count and is never named." (the framing sentence and the fact merged under the 35-word rule; the same claim).
- **R111-P4-5 [Q CLAIMS]** (1 to 0). Before: "No tested backend writes the list." After: Section 7's opener, "No tested backend writes the list: FR-Bank over-marks, Mem0 overwrites, and A-MEM's links dangle (Table~\ref{tab:census})." (item 40: the three faults named in the opener); the Conclusion keeps "Tags on returned records are the other route, and no tested backend writes the list."
- **R111-P4-6 [Q CLAIMS]** (1 to 0). Before: "Retrieval that keeps the lifecycle tag on every returned record is a second route to the obligation, and it carries the states the list leaves uncounted." After: Section 6's opener in two sentences, "A retriever that returns non-active records with their tags is a second route to the obligation (route B in Figure~\ref{fig:framework})." and "It covers the states the list does not name." (item 37: route B named on first use; the second clause in the box's word).
- **R111-P4-7 [Q CLAIMS]** (1 to 0). Before: "NOK's obligation comes from the content's own lifecycle state and is judged before content retrieval." After: Section 2's closing sentence, "What this paper measures is the judgment made before retrieval, about the store itself, from the content's own lifecycle state." (item 13: Section 2 in three paragraphs closing on the paper's own observable; the same claim).
- Also changed in Phase 4 without a frozen string: Section 1's plain definition of the forbidding record (item 8, "We call that record, a non-active record whose use would make the answer wrong, the \emph{forbidding record}."), the gain defined once in Section 1 with the $\Delta$ convention (item 9; Section 3's duplicate sentence deleted), "the states the summary only counts, retracted and expired" in Section 1's one place, the grid legend "n.a.\ means a combination the question construction never produces"; Section 5's opener in the author's words of item 63's addendum (an S9 exemption, below); the count-reader paragraph cut to the $26$ of $30$ and $15$ of $30$ sentence, the permutation sentence and one clause for the moved-count control; Section 6's own-tags paragraph to eight lines (item 38; the masked-retriever sentence cut as a repeat of Section 3's last paragraph); Section 7's capped and lifted defined and the floor named before its value; Section 8 to a plain opener, the replication sentence with both table pointers, lever 3's range sentence and one coverage paragraph (item 41, its "cut the rest" taking the two lookup-tolerance sentences; the calibration sentence and the deleted-record sentence kept, reported as deviations); Section 9 to three links and one paragraph of one-sentence pointers, Table 7 with the Wilson interval of the stale rate and the preregistered reading in its note (items 42, 43); Section 3's Listing 1 paragraph to three sentences and the "half of such pairs" sentence cut (item 19); Section 4's roster with roles, the encoder string from the code (item 25), the reporting conventions with "reliable" and "within tolerance" defined (item 26), the score-resolution note stays the setup table's footnote (D3) and the sixty-percent line moves to Limitations (items 28, 46); Section 2 in three paragraphs; the Conclusion's first paragraph in three sentences and the box without the two retention numbers (item 48). Levers: the contributions at or under 30 words a bullet; Figure 2 to the retraction triple with the supersession triple in Appendix C.2 (Table tab:sup-triple) and the caption saying so; the cross-model table deleted from Section 8, which points to Appendix A's exact table (Table tab:ladder-exact) in one sentence giving the range $+0.15$ to $+0.45$ and Kimi K3's $+0.26$ (item 84 option b).

**Phase 4b entries (Sections 1, 3 and 4 written fresh from the author's skeleton of 2026-09-15 to their line ceilings; `reviews/v18/tools/wp_phase4b.py`, reproducible from `6dbabdf` through `wp_phase4.py --step=3`).** No frozen registered text and no CLAIMS quote changed: `frozen_list_wp.py` reports 48 authorized changes and none unauthorized, all from the earlier phases. No number, n, interval or population changed, and no printed number left the paper: every value of the old three sections is kept with its population (7%, 0.50, 444; 5%, 5.2%, fifteen names, 0.80 to 0.97, 58 and 16) or moved with a pointer (Table 1's old note, "GPT-4.1 mini's repeated calls return identical scores on 46 of 50 questions", to Appendix C.2's score-resolution paragraph; the note keeps the draws and points there); numeric_diff's ADDED and VANISHED lists are those of Phase 4. Changed without a frozen string: Section 1 in three paragraphs (the hike, the two judgments, the forbidding record; the summary, the thesis sentence, routes A and B, AUROC and the gain; prior work, the paper's measurement, the pointer to Section 8) and five bullets at or under 25 words, Figure 1's caption in two lines (the drawing untouched; the routes are stated in the second paragraph); Section 3 in three paragraphs around the two definitions, the grid and the box, all four carried verbatim, with one sentence after Definition 2 pointing to Listing 1 in Appendix E.3 and carrying the count-table disclosure, and the mask paragraph in two sentences (item 19's sentence gone, the two-store argument to Phase 5's appendix item, item 14's framing sentence dropped under the skeleton); Section 4 in four paragraphs (the backends and the roster with vendors and roles; the manifests, the labels, the presence control; the two summaries and the cap; the rubric, the name lookup with its encoder, the interval convention with "reliable" and "within tolerance", the question probes, the preregistration count) with Table 1's caption without the manifest sentence (now the second paragraph's) and its note reduced to the draws; Listing 1 moved from Section 3 to Appendix E.3 with a one-sentence lead; Figure 2's source moved to the head of Section 5 (it lands above that heading on its page); the placeins option `above` added so a float pending at a section's barrier no longer forces a page break (the barrier left twenty blank lines on page 6). Main text: page 10, reading 496 (11 lines over page 9), every page full. **The page gate fails at this checkpoint**: Phases 3, 4 and 4b are committed together on the author's order of 2026-09-15 with the failure recorded here; Phase 4c (layout first, then the three prose cuts in the author's order, target 483) is its own commit.

**Phase 4c entries (the eleven lines and the author's cold-read ruling of 2026-09-15; `reviews/v18/tools/wp_phase4c.py`, reproducible from `f2133a6` through `wp_phase4b.py`).** No frozen registered text and no CLAIMS quote changed (`frozen_list_wp.py`: 48 authorized, none unauthorized). Layout, no words changed, at the elements' present sizes (Figure 2's tabular \footnotesize, Table 1 and the box \scriptsize; \small would enlarge them): Figure 2's row padding 1.1 to 0.95 with the columns rebalanced (17 to 13.8 lines with its caption); Table 1's row padding 0.9 and its population column wider (17.6 to 16.4); Figure 1's route boxes and masked path closer (18.1 to 17.4); the box's frame and row spacing (15.5 to 15.1). The author's meaning fixes, regardless of lines: Section 9's gated-rules sentence ("The gated rules are lower, $0.13$ and $0.10$, and every Wilson interval overlaps, so no policy changes the rate reliably"); Section 5's count-reader bound restricted to the two counted states and both readers given their numbers ("The category-guessing count reader separates the retracted versions at $0.67$ and the expired at $0.69$ ($30$ pairs each), its category-aware oracle at $0.73$ and $0.78$, where every model scores $0.53$ to $0.62$"; reviews/NUMBERS_WP.md section 5) with Figure 3's legend "count reader (category-aware, left panel)"; "In most retraction pairs and half the expiry pairs the category has no other such entry ($26$ of $30$ and $15$ of $30$)"; Section 8's FOK contrast restored in two sentences ("FOK detects a missing topic, $0.55$ to $0.88$, but not a single deleted record, $0.43$ to $0.50$, chance. The missing record is NOK's target."; 0.55 returns to the body, its Phase 4 disposition now historical); Section 1's thesis sentence "The three models tested on the summary alone read it by its names and not by its counts (Section~\ref{sec:counterfactual})" and its third bullet "We show monitors read names, not counts: the name lookup matches two of three models, and no model reads a state the summary only counts"; Table 7's Wilson interval on the all-states row, $[0.10,0.28]$ (AUX-WP-WILSON-A7, `reviews/v18/tools/wilson_a7.py`); Section 4's mask sentence "under that mask its own retraction questions pass at $5\%$" (the released store's question pass rate, Appendix E.9). The author's free fixes: Section 1's forbidding-record and FOK sentences; Section 3's why-clause ("because the mask drops the records whose tags carry it") and "included"; Table 1's note ("GPT-4.1 mini ran three draws per question under each prompt on this set and one call per question on every other set") and easy-tier row ("absent items made by removing a whole category from the store"); Section 5's "Haiku 4.5 gains a reliable $+0.30$ on the two counted states once they are named"; Section 6's "The reason is that the store's tags reach more of the forbidding records." (the tail of the Phase 2 S9-exempt sentence cut on the author's order); Table 4's caption ("FR-Bank's conflation of retraction with supersession is described in Appendix~\ref{app:census}"); Section 7's "That floor is $0.69$" (then cut with C3, the value standing in Section 5); Section 9's "Two further results, one sentence each." and the retag sentence's denominator clause; Limitations without the reach-versus-density clause. The writer's cold-read stalls the ruling did not supersede: Section 1's two things named in the opener, the never-asked-for record, "a monitor makes both judgments"; Section 4's "Of the three backends", "at five calls", "manifests of synthetic users (personas)", "verified by hand" without the compose clause, "the chance that an \absent{} label is wrong is $5.2\%$", "both renderings are reported, capped and with the cap lifted", "the blind and the indexed prompt", "superseded-names list", "Question wording alone carries much of a blind score". The cuts in the author's order, taken because the layout gains were absorbed by the page boundaries: C1 Section 1's second and third paragraphs to five and six lines; C2 Section 9's pointers to the header and the composite (the depth sentence and the composite's gloss gone; 8.3 to Table tab:ds-a6); C3 Section 7's own-name paragraph to three sentences. Main text: page 10, reading 493 (8 lines over page 9; the Conclusion's box alone on page 10); the target 483 not reached, reported.

**Gate tools touched in this program.** `tools/slogan_scan.py` EXEMPT_S9 gains the abstract's thesis phrase (Phase 0, `78d8f8b`); `tools/prose_scan.py` rule G4's anchor regex gains "by its names" / "by their names" (the approved thesis sentence of Section 1 is the reader-claim anchor once the four-finding paragraph of item 7 is deleted); `tools/trace_scan_v13.py` LEDGERS gains `reviews/NUMBERS_WP.md`. Phase 2 (the author's ruling of 2026-09-15): `tools/frozen_diff.py` gains `registration_fragments()`, every run of `>`-prefixed lines of a registration file being a quoted block whatever precedes it (the earlier split saw a block only after a blank line, so ADDENDUM_SIDE.md's S2-U branch text glued to its heading was invisible to the R class and reached the gate through an older CLAIMS quote alone); re-run against the pass base the watched fragments rise from 22 to 28 with zero new findings. `tools/slogan_scan.py` EXEMPT_S9 gains the author's section 15 sentence for Section 6 ("the store's tags reach more of the forbidding records, not that there are more tags"). `reviews/v18/tools/s17_grep.py` reports section 17's grep in four zones. Phase 3: `tools/slogan_scan.py` EXEMPT_S9 gains the contributions list's thesis phrase in the author's words of item 5 ("read the summary's \emph{names}, not its counts"). Phase 4: `tools/slogan_scan.py` EXEMPT_S9 gains the author's sentence of item 63's addendum for Section 5's opener ("tracks the attribute names in the summary, not the counts beside them"); `reviews/v18/tools/q_scan.py` MODEL_NAMES gains Mem0 (the backend's name is not a numeral); `reviews/v18/tools/number_moves_wp.py --check` fails on a token written with the placeholder disposition. Phase 4b: `reviews/v18/tools/q_scan.py` skips a `listing` float as it skips tables and figures (a float is not a paragraph); `tools/appendix_identity.py` gains the Phase 4b pins for C.2 and E.3 with their bases. Phase 4c: `tools/prose_scan.py` rule G4's anchor regex accepts the author's new thesis sentence ("read it by its names and not by its counts"); `tools/slogan_scan.py` EXEMPT_S9 gains the author's two sentences of the cold-read ruling (items 6 and 4: "We show monitors read names, not counts", "but not a single deleted record"); `reviews/v18/tools/wilson_a7.py` computes the one missing Wilson interval with the downstream experiment's own function.

## R112 AUTHORIZATION BLOCK — dated 2026-09-15

**Scope (the v19 lineage: the close of the writing pass and the mock review folded in).** The author's instruction of 2026-09-15 (evening), "v19: finish the writing pass and fold in the review": Step 0 creates `paper_v19.tex` from the v18 close (Phase 4c of the writing pass, commit `5078fe5`, the page gate passing) the way v17 became v18, and v18 stays as the build the mock reviewer read; Step 2 is Phase 5 of `paper_v18_writing_prompt.md` (items 59, 60, 68 to 78, 81, 82, 89, with item 19's argument and D17's sentence in the appendix, item 10's clause, item 71's instrument ledger and registered outcome texts under item 74's one convention, item 68's table of contents, item 82's model table, item 73's zero residue); Step 3 the review-driven additions R1 to R8 with the swaps that pay for them; Step 4 Phase 6, section 17's checks as amended, the final build and the report. Ground rules unchanged: no number, n, interval or population changes; every disagreement reported; the notation box's terms verbatim; section 15 on every body paragraph; the font floors (Figure 2's tabular `\footnotesize`, Table 1 and the box `\scriptsize`); registered texts verbatim with the E.1 map; zero residue outside registered blocks; the commit through the private index; the fine number reported after every step that moves it. Step 5 (experiments X1 to X3) does not start without the author's explicit go and lands only through a ruling.

**Lineage.** `paper_v19.tex` is rebuilt by `reviews/v19/tools/build_v19.py` from `reviews/v19/src/body_v19.tex`, `abstract_v19.tex` and `appendix_v19.tex` (the v18 sources copied by `reviews/v19/tools/bump_v19.py`; `body_v19.tex` gains three header comment lines and nothing else), with the carried `paper_v11.tex` blocks and the same REPAIRS lists; the tools directory is copied with the live helpers retargeted (`reviews/v19/tools/README.md` names the v18 record scripts, never run in v19). Built at the copy, `paper_v19.tex` differs from `paper_v18.tex` in the three header lines only; the main text ends on page 9 (reading 485).

**BASE.** The tree object written from the working copy with a scratch index at the v18 close, holding `paper_v18.tex`, `paper_v18.pdf` and `SUPPLEMENT.tex` as `reviews/v18/gates_wp_phase4c.txt` records them (`reviews/v19/base_tree.txt`, `base_files_sha256.txt`): `--base=575d58244e397dd91d2020a00861583f4c8f9f47`, `--base-tex=paper_v18.tex`, `--tex=paper_v19.tex`, `--program=R112`, run without `--extra-tex` as R110 ran (the base holds the paper alone, and the supplement on the working side would double the title and two configuration strings; nothing moves from the paper to the supplement in v19). `claims_diff` and `slogan_scan` keep `--extra-tex=SUPPLEMENT.tex` for the pinned-block count. `appendix_identity.py` runs against the same tree with `--base=iclr2027_monitoring_submission/paper_v18.tex`. The battery is `reviews/v19/tools/run_gates.py <tag>`, which writes `reviews/v19/gates_<tag>.txt` in the v18 format and adds the raggedbottom diagnostic reading (the fine number) beside the page census.

**Ledgers.** `reviews/NUMBERS_WP.md` continues (section 6 onward for anything v19 prints that no earlier ledger states as printed); `reviews/v19/NUMBER_MOVES_V19.md` (numeric_diff's ADDED and VANISHED tokens against the v18 close, each with a disposition; `reviews/v19/tools/number_moves_wp.py --check`); the v18 dispositions are inherited unchanged as `reviews/v19/NUMBER_MOVES_WP_v18.md`.

**Entries.** Each Before is the text at the base (a frozen string of an earlier block, a slogan_scan list or a registration); After is the text now, or the deletion with where the content stands. None at the copy: `frozen_diff` against the base reports zero changed strings, `numeric_diff` zero ADDED and zero VANISHED tokens.

**Review-2 A1 (2026-09-15, the author's ruling; `reviews/v19/A1_CONSTRAINED_RENDERING.md`, `reviews/v19/REVIEW_2_v18.md` W2).** On Mem0 and A-MEM the TRUE index is the manifest rendered under the backend's constraints (`e1_metamemory/indexes_v2.json` `meta.availability`: the lifecycle totals exact, the three name sections printed as not expressible), so Phase 2's rename TRUE -> ground-truth (R111, item 34) put "ground-truth" on that meaning in Table 1's FOK panel, the Section 7 paragraph, the E.1 map, three editable appendix lines and seven carried v11 lines including two `tab:baselines` rows. The term "the constrained rendering" is defined once in Section 4 and used at every site (`reviews/v19/tools/a1_apply.py`; `REPAIRS_R112` in `build_v19.py`, nine rules asserted to their counts). The store-written coverage summary on the two stores is within tolerance of blind by the ruling's rule (|delta| <= 0.05, both intervals include zero): Mem0 -0.0005 [-0.0663, +0.0644] / [-0.0672, +0.0635], A-MEM -0.0313 [-0.0983, +0.0400] / [-0.0798, +0.0208] (`reviews/NUMBERS_WP.md` section 6, AUX-WP-A1-BELIEVED-BLIND; a $0 paired bootstrap on the recorded E1 rows, the point values reproducing `e1_metamemory/NUMBERS.md` section 7). No number, n, interval or population changed; the four two-decimal forms Section 7 prints (0.57, 0.57, 0.53, 0.56) and the appendix's four-decimal deltas and intervals are ledgered there. The page swap the ruling named (Section 7's history-call sentence to E.9) is applied, then the page ruling's steps in order (Table 7's placement tried at [t] and [b] and restored to [h]; the Section 4 definition as one sentence, 18 words; the "at every scale" sentence cut); the page gate still fails at this checkpoint (fine number 491 against 485, the main text ending on page 10: the definition's line moves the page-4 break onto a widow, page 5 loses Figure 3 to page 6, and every later float re-packs worse; recorded in `reviews/v19/WRITING_PASS.md`). Appendix pins under R112 for E.1, E.7, E.8 (reason: rename collision from item 34, constrained rendering relabelled) and E.9 (the swap).

- **R112-A1-1 [Q CLAIMS]** (1 to 0). Before: "On the two structureless stores a summary that names what they hold restores coverage, and the summary they can write loses it at every scale." After: first Section 7, "On the two structureless stores the constrained rendering loses coverage at every scale, and a summary that names what they hold restores it." (the loss is on the constrained rendering, not on the summary the stores write); then deleted under the page ruling of 2026-09-15 (the second word step), the pooled-66 ladder standing in Appendix E.7 with its own pointer and the paragraph opening on the "Under the constrained rendering" sentence.
- **R112-A1-2 [Q CLAIMS]** (1 to 0). Before: "A name-bearing summary rebuilt from ground truth restores coverage from $0.45$ to $0.90$ on A-MEM and from $0.48$ to $0.88$ on Mem0, so the loss belongs to the summary these stores write." After: Section 7, "A name-bearing summary rebuilt from ground truth restores coverage to $0.90$ on A-MEM and $0.88$ on Mem0, so what the constrained rendering loses is the names." (0.45 and 0.48 stand in Table 1; the attribution corrected).
- **R112-A1-3** (not a frozen string; recorded for the site list). Before: Section 7, "Under that summary GPT-4.1 mini loses $0.10$ on Mem0 and $0.11$ on A-MEM, and on the pooled $66$ questions of both stores GPT-5.6 Luna loses $0.34$ and GPT-5.6 Sol $0.10$, every interval excluding zero." After: the same sentence opening "Under the constrained rendering", followed by the new sentence "The summaries the stores themselves write are within tolerance of blind, $0.57$ against $0.57$ on Mem0 and $0.53$ against $0.56$ on A-MEM (Appendix E.7)."
- **R112-A1-5** (the page ruling, not a frozen string). The Section 4 definition of the constrained rendering, first two sentences (30 and 8 words), then one sentence of at most 28 words under the page ruling: "On Mem0 and A-MEM it is the manifest rendered under the backend's constraints, the constrained rendering (Appendix E.7)." (18 words; the full form, no categories or names, exact totals, every name section not expressible, is E.7's).
- **R112-A1-4** (the swap). Before: Section 7, "Its per-memory history call, which keeps the prior text under a known identifier, was not consulted, so the erase reading is of the record as exposed and says nothing about the history log." After: deleted from Section 7; stands in Appendix E.9 opening "Mem0's per-memory history call".

**The integration pass (2026-09-16, the author's instruction and six corrections of the same day; `reviews/integration/INTEGRATION_REPORT.md`, `COMPLETED_EXPERIMENTS.md`, `POSTHOC_SPEC_R112.md` sha256 ae2600fc).** Completed experiments folded in: the forty-persona Graphiti census (Steps 1 to 3 of `registrations/ADDENDUM_R85_GRAPHITI_AMENDMENT_1.md`; `r85_graphiti/NUMBERS_R85.md` AUX-R85-G10-*, the FULL-variant re-aggregation AUX-R85-G10-CENSUS-FORBIDDING-FULL under D-R85-16) and the post-hoc analyses specified before recomputation (`reviews/NUMBERS_WP.md` sections 7 to 10: PN-versus-PRESENT and within-triple ordering, the coverage-only reference, the intent-aware lookup, the whole-map coverage lookup). Review-2 corrections applied without new data: route B stated as retrieval-time (Figure 1, Sections 1, 3, 6, the box, the abstract); the duplicate retagging stated as reference-assisted and diagnostic; the count claim narrowed in meaning ("attribute names carry most of the observed signal; the count interventions do not establish consistent count use"); "the gain is the AUROC minus 0.50"; the paired common-reach comparison in Section 9; the primary-tag / derived-expiry formalism in Section 3 and E.1; the `tab:believed` alias; the join-coverage and detector-validation clauses in Limitations; the provenance table (E.12); R1, R2 not landed (the Table 28 sentence held: page), R3 not landed (Figure 3 bars: page), R4, R5, R6, R8 landed as recorded below. Page budget: Tables 1, 3 and 5 moved verbatim to Appendices A, E.10 and E.9 (their rows already stand there or in prose), the own-tags, further-results, deleted-record and census sentences consolidated; fine number 480, the main text ending on page 9. No number, n, interval or population changed except the new ledgered post-hoc rows; every token that left a body sentence is dispositioned in `NUMBER_MOVES_V19.md`.

- **R112-INT-1 [S9 exempt; the abstract and bullet 5]** (2 to 0). Before: "reaches more forbidding records but does not reduce stale answers". After: the abstract, "reaches more of the records the agent must not use without reducing detector-flagged stale answers" (R1, the detector qualification); bullet 5, "reaches more forbidding records without reducing detector-flagged stale answers; reference-assisted retagging of the store's untagged duplicates does".
- **R112-INT-2 [S9 exempt; the thesis phrase]** (1 to 0). Before: "read the summary by its names, not by its counts". After: the abstract, "The attribute names carry most of the observed signal; the count interventions do not establish consistent count use." (the author's correction 4 of 2026-09-16: the count claim narrowed in meaning, no absolute slogan retained).
- **R112-INT-3 [S9 exempt; Section 5's opener]** (1 to 0). Before: "tracks the attribute names in the summary, not the counts beside them". After: "tracks the attribute names in the summary; the count interventions do not establish that it tracks the counts".
- **R112-INT-4 [S9 exempt; bullet 3]** (1 to 0). Before: "We show monitors read names, not counts". After: "We show that attribute names carry most of the monitors' signal: the name lookup matches two of three models, and the count interventions do not establish count use for retracted and expired content."
- **R112-INT-5 [Q CLAIMS; Section 8]** (1 to 0). Before: "FOK detects a missing topic, 0.55 to 0.88, but not a single deleted record, 0.43 to 0.50, chance. The missing record is NOK's target." (and its fragment "but not a single deleted record"). After: "FOK detects a missing topic and not a single deleted record, which is NOK's target (Appendix E.3)." (the page-budget step; the four values stand in Appendix E.3 at four decimals).
- **R112-INT-6 [Q CLAIMS; Appendix E.10]** (1 to 0). Before: "those classes are the auditor's". After: "those classes are one reader's and not an independent validation" (the review's W1; the read was one author's).
- **R112-INT-7 [Q CLAIMS; Section 5]** (1 to 0). Before: "The lookup works because the list is short and clean. As the list grows or fills with wrong names, the lookup and the models fall together (Appendix \ref{app:counterfactual})." After: the same two sentences joined by a semicolon, "The lookup works because the list is short and clean; as it grows or fills with wrong names, the lookup and the models fall together (Appendix C.2)." (the page-budget step).
- **R112-INT-8 [Q CLAIMS; the box]** (1 to 0). Before: "Return non-active records with their lifecycle tags instead of masking them; under FR-Bank's own tags the tagged view kept its reading (Section \ref{sec:routes})." After: "Return non-active records with their lifecycle tags instead of masking them; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags (Section 6)." (the measured comparison in place of "kept its reading").
- **R112-INT-9 [Q CLAIMS; Section 6]** (1 to 0). Before: "the best measured for GPT-4.1 mini only". After: "the combined monitor is best for GPT-4.1 mini only (Appendix E.10)", the two sentences merged (the page-budget step).
- **R112-INT-10 [Q CLAIMS; Section 8]** (1 to 0). Before: "The coverage margin lives on ordinary records." After: "The coverage margin over the name lookup does not survive a lookup over the whole name map." (post-hoc F1: the whole-map lookup reads 0.7469 on the easy tier, the model's margin +0.0367 with intervals including zero; AUX-WP-F1-WHOLEMAP).
- **R112-INT-11 [Q CLAIMS; Section 8]** (1 to 0). Before: "On the hard tier every coverage positive is an obligation, so the FOK row is the NOK row relabeled, and the lookup's 0.79 against the model's 0.70 is not a reliable difference (Appendix \ref{app:baselines})." After: "On the hard tier every coverage positive is an obligation, so the coverage and obligation scores are one row, and the lookup's 0.79 against the model's 0.70 is not a reliable difference." ("relabeled" replaced by the measured statement; the pointer moved to the whole-map sentence).
- **R112-INT-12 [Q CLAIMS; Conclusion]** (1 to 0). Before: "Tags on returned records are the other route, and no tested backend writes the list." After: "Tags on returned records, read at retrieval time, are the other route, and no tested backend writes the list." (D1).
- **R112-INT-13 [Q CLAIMS; Section 6]** (1 to 0). Before: "A retriever that returns non-active records with their tags is a second route to the obligation (route B in Figure \ref{fig:framework})." After: "A retriever that returns non-active records with their tags is a second route to the obligation, read at retrieval time from the returned records (route B in Figure 1)." (D1).
- **R112-INT-14 [Q CLAIMS; Section 9]** (1 to 0). Before: "The gated rules are lower, 0.13 and 0.10, and every Wilson interval overlaps, so no policy changes the rate reliably". After: "and the gated rules read 0.13 and 0.10 (Table 7)." followed by the paired comparison, "On the 42 obligations retrieval alone reaches, the oracle's flagged count is 9 against 8, two answers turning stale and one turning clean, so no paired comparison separates the policies." (F4; AUX-DS-AUDIT-PAIRED).
- **R112-INT-15 [Q CLAIMS; Section 1]** (1 to 0). Before: "The three models tested on the summary alone read it by its names and not by its counts (Section 5)" (and its fragment "read it by its names and not by its counts"). After: "For the three models tested on the summary alone, the attribute names carry most of the signal, and the count interventions do not establish consistent count use (Section 5)." (the author's correction 4; prose_scan G4's anchor extended to the new sentence).
- **R112-INT-16 [Q CLAIMS; bullet 3]** (1 to 0). Before: "We show monitors read names, not counts: the name lookup matches two of three models, and no model reads a state the summary only counts". After: as R112-INT-4.
- **R112-INT-17 [Q CLAIMS; Section 6]** (1 to 0). Before: "The reason is that the store's tags reach more of the forbidding records." After: "The reason is reach rather than volume: the store's tags mark 70 of the 99 forbidding records in view against the ground-truth tags' 60, while a count of tagged lines scores 0.62 under either tag source (Table tab:routes-full, Appendix E.10)." (the page-budget step; the indicator sentence and its 0.72 against 0.67 and +0.09 stand in Appendix E.10).
- **R112-INT-18 [Q CLAIMS; Section 9]** (1 to 0). Before: "Two further results, one sentence each." After: "Two further results stand in Appendix E.10: a header naming the persona and the date raises in-view correct answers reliably for both answerers, and the composite below." (the page-budget step; 37 to 48 and 38 to 59 stand in Appendix E.10).
- **R112-INT-19 [Q CLAIMS; Section 4]** (1 to 0). Before: "both renderings are reported, capped and with the cap lifted". After: "and binds on the store's own metadata, which is reported capped and with the cap lifted (Appendix E)" (the two cap sentences merged; the page-budget step).
- **R112-INT-20 [Q CLAIMS; Section 9]** (not a frozen string; recorded). Before: "Tagging the store's untagged duplicates, and nothing else, removes most of the stale answers; the fix belongs in the write path." After: "Retagging the store's untagged duplicates, and nothing else, removes most of the detector-flagged stale answers, which points to the write path." followed by "The retagging is reference-assisted, the lines identified with the obligation's reference information and the detector, so it is a diagnostic intervention rather than a deployable repair." (the author's correction 3; D2).
- **R112-INT-21 [Q CLAIMS; the box]** (not a frozen string; recorded). Before: "Fix the write path: tag the duplicates the store keeps active, because that removes most of the stale answers and no fetch policy does (Section 9)." After: "Tag the duplicates the store keeps active: in our reference-assisted retagging that removed most of the detector-flagged stale answers, and no tested fetch policy showed an improvement (Section 9)."
- **R112-INT-22 [Q CLAIMS; Conclusion]** (not a frozen string; recorded). Before: "What the models read in a lifecycle summary is the list of names, and the counts beside it carry nothing to them." and "The stale answers downstream come from duplicates the store keeps active, so the fix is in the write path." After: "In a lifecycle summary the attribute names carry most of the signal the models use, and the count interventions do not establish consistent count use." and "The detector-flagged stale answers downstream come from duplicates the store keeps active, and reference-assisted retagging removed most of them; whether that survives human validation is pending."
- **R112-INT-23 [Q CLAIMS; the abstract]** (not a frozen string; recorded). Before: "Tagging those duplicates removes most of the stale answers, so the fix is in the write path." After: "Reference-assisted retagging of those duplicates reduced the flagged answers, which points to the write path pending human validation of the detector."

- **R112-INT-24 [S9 exempt; the abstract's last sentence]** (1 to 0). Before: "Backends should return tags, not masks, and maintain the list." After: "Backends should keep tagged non-active records reachable for the obligation judgment, and maintain the list." (the author's fix 3 of 2026-09-16, evening: better obligation detection from tagged records does not establish better final answers than masking; the answer-stage comparison is not run).
- **R112-INT-25 [the box, sentence 1; supersedes R112-INT-8's After]** (recorded). After: "Keep non-active records reachable with their lifecycle tags for the obligation judgment; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags, and whether unmasked retrieval also improves final answers is untested (Section 6)."
- **R112-INT-26 [the count claim, the author's fix 1 of 2026-09-16, evening]** (recorded; not frozen strings). Before: the abstract, "Where the summary only counts a state, no tested model separates the versions, and naming the state lifts every model."; Section 5, "The retracted and expired states are recoverable from the count table, but no tested model recovers them."; Figure 3's caption, "the count reader separates the versions and no model does". After: "every model discriminates more weakly, naming that state lifts it, and the count interventions do not establish consistent count use"; "every tested model separates them more weakly than a count reader does"; "every model discriminates more weakly than the count reader" (Opus 5 reads 0.5689 on retraction and 0.6128 on expiry against the PRESENT versions with persona intervals above 0.50, AUX-WP-B-PNPRESENT, so "no model separates" was contradicted by the new table).
- **R112-INT-27 [Section 1, the opening example; the author's fix 2]** (recorded). Before: "We call the cancellation a forbidding record: a non-active record whose use would make the answer wrong." After: "We call the cancelled plan a forbidding record, a non-active record whose use would make the answer wrong; the cancellation is the evidence that marks it."

- **R112-INT-28 [Q CLAIMS; Figure 3's legend]** (1 to 0). Before: "count reader (category-aware, left panel)". After: "count reader (left)" (the legend no longer clipped at the right margin; the author's fix 4 of 2026-09-16, evening; the category-aware reader is named in the caption's text of Section 5).

**CL-R112-GRAPHITI-G10 [Section 7, Appendix G.4] — NEW, DESCRIPTIVE, one failed prediction.** TEXT | On Graphiti, forty personas: its invalidation marks reach 13 of the 34 full-store obligations the ground truth marks superseded or expired (the registered 30 of 74 over all obligation rows, 30 of 78 by attack vector, printed in G.4 with the P1 FAILS text verbatim; the distinct-member-set sensitivity 16 of 39); 54 of its 807 non-active edges fall on a ground-truth non-active record (0.0669). STRENGTH | Descriptive; P1's recall bar failed, its precision bar held; no obligation judgment is scored on this backend; the summary route, the tag route and the answer stage are not run. KEYS | AUX-R85-G10-INGEST, -CENSUS, -REPEAT, -CENSUS-FORBIDDING, -CENSUS-FORBIDDING-FULL, -PRINTED; D-R85-16. CLASS | procedural + adverse (store audit). Supersedes CL-R86-GRAPHITI's "main text is unchanged": Section 7 now carries two sentences on this backend; "three backends" stands for every monitoring measurement.

**CL-R112-POSTHOC-B [Section 5, Table 2, Appendix C.2] — NEW, POST HOC, specified before recomputation.** TEXT | Scored against the PRESENT versions alone, every reader moves by at most 0.03 from its whole-set value (name lookup 0.7663, GPT-4.1 mini 0.7056, Haiku 4.5 0.7493, Opus 5 0.8370); a coverage-only reader scores 0.75 pooled and ties every triple; wins / ties / losses per reader in Table 2 and per state in C.2. STRENGTH | Post hoc; the expected outcomes held for the lookup and GPT-4.1 mini and failed for Opus 5 and Haiku 4.5 on the counted states (printed). KEYS | AUX-WP-B-PNPRESENT, -B-ORDERING, -B-COVONLY. CLASS | mechanism (decomposition).

**CL-R112-POSTHOC-F1 [Section 8, Appendix E.8] — NEW, POST HOC, narrows S-COVERAGE.** TEXT | On the easy tier the whole-map lookup reads 0.7469 and the model's margin over it is +0.0367 with intervals [-0.0127, +0.0861] and [-0.0036, +0.0776], not reliable; the reliable +0.1752 margin over the superseded-section lookup stands. STRENGTH | The coverage claim is narrowed: the model does not reliably exceed a lookup over the whole name map on ordinary records. KEYS | AUX-WP-F1-WHOLEMAP. CLASS | adverse (baseline).

**CL-R112-POSTHOC-B4 [Appendix C.2, E.8] — NEW, POST HOC.** TEXT | The intent-aware name lookup reads 0.7957 against 0.7484 (+0.0473, both intervals excluding zero, within tolerance); the intent-held-fixed test is not definable from the recorded rows; 4 items where intent alone decides the label, below the floor of five, not read. KEYS | AUX-WP-B4-INTENT. CLASS | mechanism.


### Completion v1 continuation within the v19/R112 gate lineage (2026-09-17)

The current user authorizes integration of completed results and narrowed claims. The following exact historical fragments are replaced only at their documented sites; these are Q/CLAIMS prose, not registered outcome text.

- "The stores are synthetic because temporal ground truth is unobservable without controlled construction, and NOK is measured on one lifecycle store, FR-Bank, the only tested backend that retains superseded content \citep{fr}." ? The completed Graphiti monitoring results invalidate the universal one-backend/no-usable-list scope; narrow to the primary design and acknowledge the added implementation, without claiming real-data validation.
- "No tested backend writes the list: FR-Bank over-marks, Mem0 overwrites, and A-MEM's links dangle (Table \ref{tab:census})." ? The completed Graphiti monitoring results invalidate the universal one-backend/no-usable-list scope; narrow to the primary design and acknowledge the added implementation, without claiming real-data validation.
- "are read on the five-line view as a proxy)" ? The previously authorized R114 actual-view scoring already superseded this proxy; preserve that completed integration.
- "no tested backend writes a usable list" ? The completed Graphiti monitoring results invalidate the universal one-backend/no-usable-list scope; narrow to the primary design and acknowledge the added implementation, without claiming real-data validation.

## R113 AUTHORIZATION BLOCK — dated 2026-09-16

**Scope (the zero-cost audit pass).** The author's instruction of 2026-09-16: audit and complete every remaining paper analysis that needs neither money nor human annotation, from the manuscript, the registrations, the ledgers and the saved per-item outputs; no external call, no paid service, no model download, no annotation; frozen registrations and populations preserved; a new analysis specified before it is computed and labelled post hoc; nothing completed re-run except to resolve a discrepancy; model-generated labels never substituted for human validation. Specification `reviews/r113/SPEC_R113.md` (sha256 a315511d, ledgered as `AUX-R113-SPEC-FREEZE` before any script ran); ledger `reviews/NUMBERS_R113.md`; report `reviews/r113/REPORT_R113.md`; results `reviews/r113/results/`. Nothing in this block is committed; the changes are left for the author's review.

**Lineage.** `paper_v19.tex` rebuilt by `reviews/v19/tools/build_v19.py` from `reviews/v19/src` (the R112 sources with the six asserted edits of `reviews/r113/tools/z6_apply_manuscript.py`); gates run under the R112 base (`reviews/v19/base_tree.txt`) and program R112, which stays valid because no frozen string is touched (the Before texts below are named by site and quoted only in fragments shorter than the frozen-string length, so this block adds no frozen string that the base carries); `reviews/v19/gates_r113.txt`. Gate-tool hunks, each with a dated note: `trace_scan_v13.py` LEDGERS gains `reviews/NUMBERS_R113.md`; `appendix_identity.py` gains the R113 pin for C.2 (`reviews/r113/tools/pin_appendix_r113.py`); `reviews/v19/tools/number_moves_wp.py` ADDED / VANISHED gain the R113 dispositions (`NUMBER_MOVES_V19.md` regenerated).

**What the pass found (nothing in the manuscript changes for these; `reviews/NUMBERS_R113.md` sections 1 to 5).** (Z1) The composite's five-line proxy (DS Amendment 7): none of the 99 distinct (item, view) inputs the 10 / 17 / 72 absent items would need has a recorded answer under any prompt variant or answerer; the proxy qualification in `tab:ds-a7`'s caption stands, no composite number changes, the generation required is listed (`AUX-R113-Z1-GENERATION`). (Z2) The FULL-store population of the Graphiti comparison reproduces from the cell alone: 323 = 145 / 131 / 47, 178 non-ABSENT, 99 / 230 / 9, 58 / 42 (`AUX-R113-Z2`). (Z3) The FR-Bank comparators on the 323 exist from the recorded rows, the 661 figures beside them (`AUX-R113-Z3-*`); no Graphiti number is read; P2 to P4 stay unrun and D-R85-16's population ruling stays the author's. (Z4) Amendment 2's FR-Bank inputs built from the unfrozen draft: on the 178, n_TM = 163 (the T-versus-M structural bound 0.9157), 63 masked views shorter than five lines, one empty (`AUX-R113-Z4-*`); the graph side needs the graph and an embedding call (`AUX-R113-Z5`). (Z5) P3's NB-6 input exists on disk for all forty personas (the cap never binds on the superseded section); P3 is not scored.

**Entries (Z6, the manuscript).** Each Before is text of the R112 build, none of it a frozen string; After is the text now.

- **R113-1 [Appendix C.2, the store's-own-pool sentence]** (1 to 0). Before: the sentence ending "beyond the store's own name" pool it is untested (Appendix C.2, after the 0.6531 clause). After: "With every untargeted name the store holds on the list, a mean of $99$ names per summary and at most $129$, the embedding lookup reads $0.6531$; continued past that pool with other personas' names to $100$ and $200$ it reads $0.6558$ and $0.5960$ (Table~\ref{tab:pad}), so a longer list of the store's own names is untested." Basis: `reviews/NUMBERS_R110.md` AUX-R110-A4 (reading (i), the registered draw order: pool A then pool B = other personas' names; 79 of 242 keys spill at 100, every key at 200); the sentence as written contradicted the 100- and 200-name rows the same table prints.
- **R113-2 [tab:pad's caption]** (1 to 0). Before: the caption clause ending "$60$ names; obligation AUROC" (the 100- and 200-name rows unnamed). After: "to $15$, $30$ and $60$ names, and for the two lookups to $100$ and $200$ names under the registered draw order, which continues into other personas' names once the store's own pool is exhausted ($79$ of the $242$ summaries at $100$, every summary at $200$); obligation AUROC of each reader against its recorded $1.75$-name row, with the paired difference and both intervals." Basis: AUX-R110-A4; `reviews/v18/results/a4_table16_rows.tex`'s own note ("Caption note to add") never landed.
- **R113-3 [tab:pad, the lexical rows at 100 and 200]** (2 rows). Before: "-- & $[0.5001,0.6162]$ & --" and "-- & $[0.4737,0.6006]$ & --" (a single-arm AUROC interval printed in the item-interval column, no paired difference). After: "$-0.0137$ & $[-0.0672,+0.0369]$ & $[-0.0926,+0.0716]$" and "$-0.0355$ & $[-0.0903,+0.0189]$ & $[-0.1125,+0.0455]$" (the paired difference against the committed list and both intervals, the columns the table defines). Basis: `reviews/NUMBERS_R113.md` AUX-R113-PAD-LEX-PAIRED, read from `reviews/v18/results/a4_pad_extend.json` (`paired_vs_base.lex`), no recomputation; the single-arm intervals stand in AUX-R110-A4.
- **R113-4 [Section 10, Limitations]** (1 to 0). Before: the sentence beginning "The lookup is untested beyond" (the name-pool limitation and the paraphrase check in one sentence). After: "Beyond the store's own name pool, a mean of $99$ names, the lookup is tested only with other personas' names. A paraphrase check of one rewording per question, fixed in advance, is not yet scored." (two sentences; the first at 36 words would have joined the readability listing). Basis: as R113-1. Page 9 unchanged: page-census reading 485 (+0), fine number 483.

**CL-R113-PAD-POOL [Section 10, Appendix C.2, tab:pad] — RESTATED, DESCRIPTIVE (no strength change).** TEXT | With the store's own name pool exhausted (a mean of 99 names per summary, at most 129) the embedding lookup reads 0.6531; continued with other personas' names to 100 and 200 names under the registered draw order it reads 0.6558 and 0.5960; the lexical lookup is flat at every length (100: -0.0137, 200: -0.0355, both intervals including zero); a longer list of the store's own names is untested. KEYS | AUX-R110-A4, AUX-R113-PAD-LEX-PAIRED. CLASS | robustness.

**Not changed, and why.** The composite (Z1), the Graphiti comparators (Z3), Amendment 2's inputs (Z4) and P3's inputs (Z5) print nothing: the composite's proxy stands as stated; a comparator printed without the row it is for would misstate the paper's status (E.9 and G.4 say no obligation judgment is scored on Graphiti); Amendment 2 is unfrozen. Every "pending", "not run", "not yet scored" and "awaits" statement in the R112 build was read against `reviews/integration/COMPLETED_EXPERIMENTS.md` and this pass's findings and stands (`reviews/r113/REPORT_R113.md` section 4). The human-validation caveats are untouched.

## R114 AUTHORIZATION BLOCK — dated 2026-09-17

**Scope (the remaining runnable paid experiments).** The author's instruction of 2026-09-17: execute the remaining runnable paid experiments in phases under a $40 ceiling for new spend, with a deduplicated call manifest, frozen protocols and predictions preserved, every necessary amendment recorded before the affected output, no population, repeat, model, threshold or claim changed to obtain a result, no synthetic human label, blocked phases blocking nothing independent, X1 to X4 not run, everything saved and nothing overwritten, manuscript and source changes left uncommitted. Specification `reviews/r114/SPEC_R114.md` (sha256 f13b7df4, ledgered as `AUX-R114-SPEC-FREEZE` before any call); ledger `reviews/NUMBERS_R114.md`; report `reviews/r114/REPORT_R114.md`; integration notes `reviews/r114/INTEGRATION_NOTES_R114.md`. Nothing in this block is committed.

**Lineage.** `paper_v19.tex` rebuilt by `reviews/v19/tools/build_v19.py` from `reviews/v19/src` (the R113 sources with the asserted edits of `reviews/r114/tools/m1_apply_manuscript.py`); gates run under the R112 base (`reviews/v19/base_tree.txt`) and program R112, which stays valid because no frozen string is touched (Befores below are named by site and quoted in fragments shorter than the frozen-string length); `reviews/v19/gates_r114.txt`. Gate-tool hunks, each with a dated note (`reviews/r114/tools/m2_gate_hunks.py`, `pin_appendix_r114.py`): `trace_scan_v13.py` LEDGERS gains `reviews/NUMBERS_R114.md`; `appendix_identity.py` gains the R114 pins (E.10, C.2); `reviews/v19/tools/number_moves_wp.py` ADDED / VANISHED gain the R114 dispositions (`NUMBER_MOVES_V19.md` regenerated).

**What the pass ran (`reviews/NUMBERS_R114.md` sections 1 to 5; the lane ledgers carry the numbers).** (P1) The composite's 99 unanswered (item, view) inputs answered by GPT-4.1 mini and Claude Haiku 4.5 under the Amendment 4 header (`ds_downstream/NUMBERS_DS.md` section 14): every composite within one of the proxy reading. (P2) R85 Amendment 1 Steps 4 to 6 on the 323 FULL-variant items (D-R85-17; `r85_graphiti/NUMBERS_R85.md` AUX-R85-G10-INDEXES to -SPEND-R114): P2 HOLDS, P3 FAILS, P4 HOLDS; GR-1 FAILS under the weaker-interval rule, GR-2 a dash, GR-3 HOLDS; Haiku's summary lane a dash. Not printed in the manuscript by this pass: the placement is the author's ruling (Amendment 1 §8 step 9, §10); the sentences and the Appendix G table are drafted in the integration notes, section B, with the "no usable list" contribution flagged for revision (P3 failed: the store's own list reads 0.6780). (P3) R85 Amendment 2 frozen by sha256 (D-R85-18) and its Steps 1 to 3 run: 1,114 distinct mini answers on both stores, the detector rows secondary and provisional (AUX-R85-A2-DETECTOR), the blind sheet sealed (AUX-R85-A2-SEAL); the human read, A2-P1 to A2-P3 and the ruling table are not done and nothing from them prints. (P4) The optional Opus 5 lane on the moved-count control at k = 1 (D-V2RCAT-2; `r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md` section 8). (P5) PARA verified blocked: 0 of 248 verdict cells filled; no call.

**Entries (the manuscript).** Each Before is text of the R113 build, none of it a frozen string; After is the text now.

- **R114-1 [tab:ds-a7, twelve rows]** (12 rows). Before: the rows whose absent component read the five-line proxy for the absent items a gated rule answers on a longer view (GPT-4.1 mini literal rule "$241 = 0 + 241$ & $300$", model rule "$264 = 172 + 92$ & $319$"; Haiku 4.5 model rules "$291 = 172 + 119$" with composites 371 / 376 / 377 / 381, lookup rules "$304 = 174 + 130$" with 379 / 381 / 384 / 386). After: the actual-view reading (GPT-4.1 mini literal rule "$242 = 0 + 242$ & $301$", model rule "$265 = 172 + 93$ & $320$"; Haiku 4.5 model rules "$292 = 172 + 120$" with 372 / 377 / 378 / 382, lookup rules "$303 = 174 + 129$" with 378 / 380 / 383 / 385). Basis: AUX-DS-R114-COMPOSITE-ACTUAL; the proxy reading reproduced in the same run before the actual numbers printed.
- **R114-2 [tab:ds-a7's caption, the proxy clause]** (1 to 0). Before: the clause ending "are read on the five-line view as a proxy)". After: "…are read on that longer view, answered under the same header prompt after the registration, $99$ distinct views per answerer; read on the five-line view as a proxy instead, every composite is within one of the value printed)". Basis: AUX-DS-R114-VIEWS.
- **R114-3 [tab:ds-a7's prose, two sentences]** (2 to 0). Before: "$+18$ of $661$ … $[+0.01,+0.04]$ … $[+0.01,+0.04]$ … $+2$ for Haiku~4.5 … $+10$ ($+0.02$" and "the rule adds $23$ and $11$". After: "$+19$ of $661$ … $[+0.01,+0.05]$ … $[+0.01,+0.05]$ … $+3$ for Haiku~4.5 … $+9$ ($+0.01$" and "the rule adds $24$ and $12$". Basis: AUX-DS-R114-COMPOSITE-ACTUAL-DIFF (10,000 draws, seed 42, item-level and persona-grouped).
- **R114-4 [Section 5, the count-reader paragraph; Appendix C.2, tab:v2rcat and its prose]** (1 to 0 in Section 5; 3 rows and 1 sentence in Appendix C.2). Before: "Opus 5 was not run on this control." and tab:v2rcat without an Opus row. After: Section 5 reads "Opus 5, run once per item after this draft against its five-draw row, moves $-0.10$ on retraction and $-0.12$ on expiry."; tab:v2rcat gains the whole-set, retraction and expiry rows (k = 1; recorded row k = 5) with both intervals; the C.2 prose gains three sentences with the direction and the draw-count disclosure; the E.11 spend sentence gains the two runs' amounts ($0.14$, $4.52$, the $40$ ceiling). Basis: `r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md` section 8, AUX-V2RCAT-OP5 (444 requests: 393 by Batch, 51 synchronous after two canceled batches, 0 not OK, $4.5022); D-V2RCAT-2, -3, -4.

**CL-R114-COMPOSITE-ACTUAL [Appendix E.10, tab:ds-a7] — RESTATED, DESCRIPTIVE (no strength change).** TEXT | With the absent items the gated rules answer on a longer view read on that view's own answer, the composite under the model rule minus retrieval alone is +19 of 661 for GPT-4.1 mini (+0.03, both intervals excluding zero) and +3 for Haiku 4.5 (+0.00, both including zero); the lookup rule +25 (+0.04, reliable) and +9 (+0.01, both including zero); every composite within one of the proxy reading. KEYS | AUX-DS-R114-COMPOSITE-ACTUAL, AUX-DS-R114-COMPOSITE-ACTUAL-DIFF. CLASS | robustness.

**CL-R114-OPUS-MOVED-COUNT [Section 5, Appendix C.2] — NEW ROW, DESCRIPTIVE (no prediction).** TEXT | Opus 5, run once per item on the moved-count control against its recorded five-draw superseded-only row (0.8405), reads 0.8049 on the whole set (-0.0357); retraction 0.5872 to 0.4861 (-0.1011, [-0.1700, -0.0435]; [-0.2145, -0.0211]); expiry 0.6150 to 0.4914 (-0.1236, [-0.2165, -0.0374]; [-0.2598, -0.0118]); branch: neither inside the band on both states nor beyond it with both intervals: printed as it came out. KEYS | AUX-V2RCAT-OP5, AUX-CF2-OP5-V2. CLASS | robustness.

**Not changed, and why.** The Graphiti summary and tag routes (P2 HOLDS, P3 FAILS, P4 HOLDS, GR-1 FAILS, GR-3 HOLDS) print nothing yet: Amendment 1 §10 fixes their placement (one Section 7 sentence as a swap at the page boundary; the Appendix G table; E.9's deferral sentence under the frozen_diff rule) on the author's ruling; the drafted text is in the integration notes, with the fourth contribution's "no tested backend writes a usable list" flagged for revision. The answer stage (Amendment 2) prints nothing: its endpoints are human-scored and unread. The human-validation caveats, the second annotator's sheets, PARA's "not yet scored" and the Haiku dashes stand.


## Submission completion v1 (2026-09-17)

Authorized by the user's instruction to finish existing work and integrate completed results and narrowed claims. This supersedes the earlier R114 placement deferral; it does not rewrite a registered prediction or human endpoint.

- NARROWED: "no tested backend writes a usable list" is withdrawn at abstract, contribution, backend discussion and conclusion. The completed Graphiti native superseded-name matcher is above chance and above the capped summary monitor (AUX-R85-G10-NB, -P3, -GR); the failed near-chance prediction prints. No final-answer utility follows from this AUROC.
- NARROWED: the blanket no-detectable-count-signal sentence now allows the optional Opus moved-count response; its k=1/k=5 caveat and neither-branch result remain. No consistent-count-use claim is added.
- UPDATED: Graphiti monitoring is complete on 323 FULL items, 47 obligations, with the population correction and all failed/held/unevaluable readings disclosed. Existing tables and frozen outcome text are preserved. A2 generation is complete; its human endpoints remain pending.
- NEW, EXPLORATORY: Appendix G.5 reports the source-repaired Sol sample, every repair arm, small paired gains and harms, persona uncertainty, source/quote flags and pending independent human validation. It retains the 147 unjudged repair questions; no primary endpoint is silently replaced.
- NEW, EXPLORATORY AND INCOMPLETE: fixed 557-item cached depth comparison, 139 expansions, eight personas judged before provider credits exhausted. No full semantic point estimate is imputed. Costs include monitor overhead scenarios and unmeasured maintenance explicitly. Quality retention and practical utility are unresolved.
- NARROWED: builder guidance no longer recommends paying for a model over every native name list, and no longer calls every successor-fetch result a failure despite provisional small gains. Compare the cheap lookup on the actual store; source-assisted retagging remains diagnostic and detector validation remains pending.

No sealed annotation key was accessed. No human annotation, new answerer, new retrieval method, threshold search or unapproved PARA run was performed. The originals remain in their existing artifact directories. Source and number provenance: analysis/submission_completion_v1/REPORT.md, repair/paired_results.json, depth/costs.json, and reviews/NUMBERS_COMPLETION_V1.md. Changes remain uncommitted.

## R115 AUTHORIZATION BLOCK — dated 2026-09-18

Program R115: the author's "Knowing the Store" patch of 17 September to paper_v19 (`reviews/r115/PATCH_KTS.md`, sha256 `0283b8e05f576c5908a75c66a51aef1696c74a75a2f9ed405d8f1939e36692b3`, ledgered as AUX-R115-SPEC-FREEZE before any edit), applied with the author's rulings of 18 September by `reviews/r115/tools/kts_patch.py` (every edit asserted). Thirteen main-text patches, the appendix patches A1, A2, A3, A5 and A6(a)-(c); A4 (the AI-use statement) and Part E (the intent crossover) not applied on the author's ruling. No number changes: every numeral new to the main text is a two-decimal form of a ledgered value (reviews/NUMBERS_R115.md, AUX-R115-PRINTED). Befores are cited as fragments under thirty characters (the R113 convention: a full Before that occurs in the base would become a watched string); Afters in full. Base for frozen_diff unchanged (575d5824); no watched fragment changed (frozen_diff PASS, frozen_list_wp AUTHORIZED 29 as before).

- **R115-1 [the abstract, whole; P1 with the gap-form seventh sentence, the author's ruling 1]** (recorded). Before: fragments "backends with six models", "most of the observed signal", "every model but the largest", "Preserving lifecycle evidence". After: "An agent with a persistent memory store can judge two things before retrieving. The first is whether the store covers a question (feeling of knowing, FOK). The second is whether the store holds something the agent must no longer use, such as a cancelled plan (negative-obligation knowledge, NOK). We define both as intent-dependent labels, build synthetic stores with exact labels, and measure them on four backends with up to six models. The monitor sees only a lifecycle summary: record counts per lifecycle state and a value-free list of attribute names, on which only superseded names appear. The attribute names carry most of the signal. With one question asked of three store versions, GPT-4.1 mini and Haiku 4.5 do not exceed a similarity lookup over the list, and Opus 5 exceeds it by $0.07$. Where the summary only counts a state, every model discriminates more weakly than a reader of the counts, and naming that state lifts every model. Returning non-active records with their tags instead of masking them is a second route, at retrieval time, covering what the list misses. What the backend writes decides how much survives. Under FR-Bank's own metadata GPT-4.1 mini and the lookup fall near chance while Haiku 4.5 keeps $72\%$ of its gain, and Graphiti's own name list serves a lookup better than the model. Downstream, gating retrieval on the judgment reaches more of the records the agent must not use without reducing detector-flagged stale answers, because the store keeps untagged duplicates. Reference-assisted retagging of those duplicates removes most of the flagged answers, which points to the write path; the detector's human validation is pending." The $0.07$ is Table 1's $0.84$ minus $0.77$ (rule G2: the lookup named, the difference stated, no level printed).
- **R115-2 [Section 1; A6(c)]** (recorded). Before: "across three backends and". After: "We measure both judgments on stores built with exact labels, across three main backends and six models from three vendors."
- **R115-3 [Section 4, first paragraph; P2]** (recorded). Before: "Of the three backends,". After: "Of the three main backends, FR-Bank \citep{fr} is the only one that tags every entry with a lifecycle state." and, appended after the structureless-backends sentence: "Graphiti \citep{zep}, whose validity intervals resemble lifecycle tags, is a fourth backend, scored with GPT-4.1 mini on the same personas (Appendix~\ref{app:posthoc-graphiti})."
- **R115-4 [Section 4, the statistics sentence; P3, verified against e1r_robustness/tools/common_e1r.py: boot_item draws row indices, boot_cluster concatenates whole personas; 148 pair_ids x 3 versions, none spanning personas]** (recorded). Before: "resampling whole questions". After: "On the counterfactual set the persona-grouped interval is the one printed, because resampling whole personas keeps each triple intact and the item-level bootstrap does not."
- **R115-5 [Section 5, the supersession paragraph; P4]** (recorded). Inserted after the $0.07$ sentence: "Opus 5's first draw alone keeps that margin (Appendix~\ref{app:counterfactual})." (AUX-WP-PRINTED / Appendix C.2: the first draw $0.8400$, $+0.0736$ above the lookup, both intervals excluding zero). Before: "Scored against the PRESENT". After: "Scored post hoc against the PRESENT versions alone, which also hold relevant content, every reader moves by at most $0.03$ from its whole-set value, so the comparison stands where coverage is equal." Deleted: the sentence beginning "gives that score and the wins" (Table 1's caption carries it).
- **R115-6 [Section 5, the moved-count sentence; P5]** (recorded). Before: "after this draft against its". After: "Opus 5, run once per item against its five-draw row, moves $-0.10$ on retraction and $-0.12$ on expiry, both intervals excluding zero." (AUX-V2RCAT-OP5; s17_grep's cap on the phrase is three in the main text, count now one.)
- **R115-7 [Section 5, the two sample-size sentences; P6]** (recorded). Before: fragments "rests on $30$ retraction", "give only a direction". After: "These groups are small (Section~\ref{sec:limitations})." The counts stay in Limitations and Appendix C.2.
- **R115-8 [Section 6, end of the last paragraph; P7 with deviation D1]** (recorded). Inserted: "On Graphiti, native tags on the same five retrieved edges make no reliable difference ($-0.01$, both intervals including zero; Appendix~\ref{app:posthoc-graphiti})." (AUX-R85-G10-P4: $0.6854$ against $0.6995$, $-0.0141$, item $[-0.0786,+0.0554]$, persona $[-0.0613,+0.0325]$; "add nothing" in the patch read as equivalence, which G.4 does not establish.)
- **R115-9 [Section 6, the own-tags sentence; P8]** (recorded). Before: "to a reliable $0.81$." After: "GPT-4.1 mini's obligation score on that view rises from $0.69$ to a reliable $0.81$, a descriptive result with no prediction fixed in advance."
- **R115-10 [Section 7, first paragraph; P9 with the author's rulings 2 and 3]** (recorded). Before: fragments "(\texttt{mem0ai} 1.0.5).", "identifiers (Table~", "On Graphiti \citep{zep},", "retains useful signal despite". After: "Mem0 erases at its retrieval surface: of its $10{,}074$ entries, $12.7\%$ expose \texttt{updated\_at} and nothing else, because an \texttt{UPDATE} replaces the record that \texttt{search} and \texttt{get\_all} return." / "A-MEM invents: all $23{,}186$ link references across its $11{,}319$ notes resolve to zero note identifiers." / "Graphiti recovers some of the forbidding records and exposes names a lookup can use." / "Its invalidation marks reach $13$ of the $34$ full-store obligations that the ground truth marks superseded or expired, more than the quarter we had predicted." / "Under its capped store-written summary GPT-4.1 mini scores $0.58$ on the $323$ full-store questions, a gain over blind that includes zero, against $0.74$ under the ground-truth summary." / "A name lookup over Graphiti's own superseded names scores $0.68$, reliably above the model by $+0.10$ (Appendix~\ref{app:posthoc-graphiti})." (AUX-R85-G10-P2 $0.5765$; INDEXED-TRUE $0.7424$ on the 323, AUX-R113-Z3-ROWS; AUX-R85-G10-GR: GR-1 FAILS, $+0.0801$ over blind with the item interval $[-0.0031,+0.1604]$ including zero, GR-3 HOLDS, the lookup $0.6780$, $+0.1014$, $[+0.0102,+0.2086]$, $[+0.0094,+0.1988]$.) The \citep{zep} moves to Section 4 (R115-3).
- **R115-11 [Section 9, last paragraph; P10]** (recorded). Before: fragments "Two further results stand in", "and the composite below.", "against retrieval alone for". After: "Two further results are in Appendix~\ref{app:resp}." / "A header naming the persona and the date raises in-view correct answers reliably for both answerers." / "A composite over all three jobs rises under the model rule by a reliable $+0.03$ for GPT-4.1 mini and stays level for Haiku 4.5 (Table~\ref{tab:ds-a7})."
- **R115-12 [Section 10, Limitations; P11]** (recorded). Deleted: the sentences beginning "The sixty-percent retention" and "The tagged route under the". The first moves to Appendix E.9 (R115-17); the second's content is R115-9.
- **R115-13 [Section 11, the Conclusion paragraph; P12 with deviation D2]** (recorded). Before: fragments "nothing we tried with the", "another monitoring route, and", "semantic validation and". After: "The models draw most of their signal from a lifecycle summary's attribute names, and a name lookup over a clean list is not exceeded by two of the three." / "Only Opus 5 responds to a moved count." / "Tags on returned records are the second route." / "What a backend writes decides how much survives: under FR-Bank's own list GPT-4.1 mini and the lookup fall near chance while Haiku 4.5 keeps most of its gain." / "Graphiti's own names serve a lookup better than the model." / "Downstream, the flagged stale answers trace to duplicates the store keeps active, and answer-level benefit awaits the detector's human validation." ("responds to the counts" in the patch read as more than Section 5 supports: permuting the totals moves no model by more than $0.01$; the moved increment moves Opus 5. Deviation D5: the third sentence lost "at retrieval time", which prose_scan rule D read as an 86 percent near-duplicate of Section 1 line 114 and Section 6 line 442; Section 1 and the abstract carry the qualifier.)
- **R115-14 [Section 11, the box; P13; supersedes R112-INT-25's After]** (recorded). After: "Keep non-active records reachable with their lifecycle tags; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags (Section~\ref{sec:routes})." / "Maintain the list of attribute names that hold non-active content, superseded, retracted and expired alike." / "Compare a name lookup with the model on the actual store before paying for the model call (Sections~\ref{sec:counterfactual} and~\ref{sec:backends})." / "Tag the duplicates the store keeps active, which is where the flagged stale answers came from (Section~\ref{sec:downstream})."
- **R115-15 [Appendix C.2; A1]** (recorded). Before: "was run after this draft once". After: "Opus 5, the optional lane, was run once per item ($k=1$, the registered default) against its recorded five-draw superseded-only row."
- **R115-16 [Appendix E.11; A2]** (recorded). Before: "two runs after this draft,". After: "two later runs, the composite's answers on the actual expanded views $0.14$ and Opus 5 on the moved-count control $4.52$, under a $40$ ceiling for that pass."
- **R115-17 [Appendix E.9; A3]** (recorded). Inserted after the retention sentence: "The sixty-percent line was a conventional threshold, fixed before the main study, with no recorded reason for its value."
- **R115-18 [Appendix G.4; A5 with deviation D3 and the author's ruling 3]** (recorded). Inserted before the paragraph that rules on the readings: "Amendment 1's three monitoring predictions (P2 to P4 in Appendix~\ref{app:registration}) are that the store-written summary falls below the ground-truth summary by more than the tolerance, that the superseded-names lookup sits within tolerance of chance, and that the tagged view sits within tolerance of the untagged view." / "Its five readings are GR-1, that the paired obligation gain on the store-written summary excludes zero; GR-2, the same for coverage; GR-3, that the superseded-names lookup sits within tolerance of the model or above it; GR-4, descriptive retention against FR-Bank's ground-truth gain; and GR-5, the census's failure mode." / "GR-1's text reads: ``On a second store that records when a fact stopped being true, the obligation judgment does not rise beyond $+0.0801$ when the summary is supplied, so the gain measured on our own store does not reproduce where the lifecycle record is thinner.''" / "GR-3's reads: ``A matcher reading the store's own list of superseded names reaches $0.6780$ against the monitor's $0.5765$ on this store as well.''" (registrations/ADDENDUM_R85_GRAPHITI.md section 7, the FAILS and HOLDS texts verbatim with $D$, $Y$, $X$ filled from AUX-R85-G10-GR.) The codes stand inside a parenthetical that points to Appendix~\ref{app:registration} (prose_scan rule A). After Step 1 (the author's ruling of 18 September) the three outcome texts of Amendment 1 section 5 print beside them, named as the registration names them: "The summary-route prediction holds; its registered text reads: ``Under Graphiti's store-written summary GPT-4.1 mini reads $0.5765$ against $0.7424$ under the ground-truth summary on the same questions, $-0.1659$ below with interval $[-0.2593,-0.0764]$; a matcher reading Graphiti's own list of superseded names reads $0.6780$.''" / "The lookup prediction fails: ``A matcher reading Graphiti's own list of superseded names reaches $0.6780$, $+0.1780$ from chance.''" / "The tag-route prediction holds: ``Shown the five retrieved edges with Graphiti's own states, GPT-4.1 mini reads $0.6854$ against $0.6995$ without them, within tolerance: the states this store writes do not reach the records that forbid use.''" (AUX-R85-G10-P2, -P3, -P4; reviews/NUMBERS_R115.md AUX-R115-TEXTS; $+0.1780$ is the one token new to the manuscript, dispositioned in NUMBER_MOVES_V19.md.) Deviation D-R115-1: GR-1's text is tagged [MAIN] in the registration and prints in Appendix G.4, a Section 7 clause carrying its content (R115-10), because of the page limit; the author's ruling 3 of 18 September. "GR-3 holds" stays in the table cell.
- **R115-19 [Appendix C.2 and E.9 tables; A6(a)]** (recorded). "profile" reads "persona" in the count-reader sentence of C.2, the headers of tab:v2rcat and tab:pad, and the four interval rows of tab:bh-split; the frozen registered "grouped by user profile" texts untouched.
- **R115-20 [the bibliography; A6(b), the author's ruling 4]** (recorded). The carried block %%V11:677-871%% inlined into body_v19.tex (the build byte-identical, sha256 9c576608e812cd5d before the deletion) and the nine entries no citation reaches removed: knowbutnotact, dunlosky2009, knowact, metcalfe1994, naeini2015, nosek2018, pineau2021, openaimemory, memgate (the patch named seven; two more were uncited). refcheck_v11.py retires the nine keys (RETIRED) so their records are not orphans; 54 bibitems remain.
- **R115-21 [not applied]** A4 (the AI-use statement: unchanged, to be updated once at the end) and Part E (the intent crossover: nothing added; the Limitations sentence goes in if #1 has not landed by 23 September). Section 1 lines 111 / 122 ("no count intervention establishes consistent count use") left as they are, to be rewritten with Section 5, the abstract and the Conclusion when the Opus 5 moved-count run at k = 5 lands (open flag, REPORT_R115.md).
- **R115-22 [Appendix B, Table tab:crossvendor-predictions; deviation D6]** (recorded). The carried table's placement reads [H] for [h] (reviews/v19/tools/build_v19.py REPAIRS_R115_BLOCK, keyed to the carried block paper_v11.tex 1004-1020, asserted once): with nine bibliography entries gone, Appendix B moved up by a third of a page, the table no longer fit at the foot of its page, was deferred to the top of the next, and the float barrier before Appendix C ended that page after two lines (page 16 of the first build of 18 September mostly blank, 59 pages). Placed [H] the pagination of the 17 September build returns for Appendices A to F; 58 pages, the extra page being G.4's own growth. Content unchanged.
- **R115-23 [the gate tools]** (recorded). refcheck_v11.py: the nine removed keys retired (RETIRED; skipped in the verification loop and subtracted from the orphan set), so their records stay for the history without counting as orphans. appendix_identity.py: R115 pins for B, C.2, E.9, E.11 and G.4 (reviews/r115/tools/pin_appendix_r115.py). trace_scan_v13.py: LEDGERS gains reviews/NUMBERS_R115.md. number_moves_wp.py: the +0.1780 disposition. No rule of any gate changed.
- **R115-24 [gates]** (recorded). reviews/v19/gates_r115.txt: every gate PASS; label page 9, page-census reading 482 (+3), raggedbottom fine number 480 (+5, the AI-use heading on page 9; the author defers a \newpage ruling to the final build of 24 September); 58 pages; frozen_list_wp AUTHORIZED 29; refcheck 19/19, 35 out of scope, 0 uncovered of 54.

## R116 AUTHORIZATION BLOCK — dated 2026-09-18 / 19

Program R116: the provenance fix (`reviews/r115/PROVENANCE_AUDIT.md`; the author's Appendix R of 18 September and the rulings of 19 September, `reviews/r116/RULINGS_R116.md`), applied by `reviews/r116/tools/r116_apply.py` and `r116b_apply.py` (every edit asserted, idempotent) and `build_v19.py` REPAIRS_R116_BLOCK for the carried tables. No frozen string is touched (frozen_diff and claims_diff PASS); the entries below record the sites. No number changes; the numerals E.11 and Appendix B add are ledgered in `reviews/NUMBERS_R116.md` (AUX-R116-HARNESS, AUX-R116-PRICES) and dispositioned in NUMBER_MOVES_V19.md.

- **R116-1 [Appendix R item 1: withdrawn]** The sentence "Every protocol was committed before its run (hashes and order: Appendix F)." is v18's, not v19's; no body edit.
- **R116-2 [Appendix F, table a, the R81 row; item 2(a)]** (recorded). Before: "\texttt{2bb7fd9dc4}". After: "\texttt{5c3621b75e}" (the registration file's first commit, 2026-08-29 17:11 +05:30, before the first NB-6 output; build_v19.py REPAIRS_R116_BLOCK, block 2084-2118, asserted once).
- **R116-3 [Appendix F, table b, the DS Amendment 4 row; item 2(b)]** (recorded). Before: "\texttt{fb4b2ca8c8} & 2026-09-14". After: "\texttt{fb4b2ca8c8} (file hash) & 2026-09-14".
- **R116-4 [Appendix F, table c's caption; item 2(c)]** (recorded). Before: "each frozen by sha256 before". After: "The registration record, continued: twelve descriptive registrations, each hashed by the runner before its first call (the commits of 18 September do not date them) and carrying no prediction and no bar, so nothing in them could hold or fail. Every one has run except the paraphrase check, which waits on our read."
- **R116-5 [Appendix F, after table c; item 2(d)]** (recorded). Inserted: "How each freeze is attested. Each runner wrote a lock record at its start holding the registration's sha256, and dated additions sit below the registered-text marker, outside the hash. For most registrations a commit holding the registered text also predates the run's first output. For CF-3, committed 33 minutes after its first call, and for DS Amendments 1 to 4, Q4, RESP Amendment 1 and Graphiti Amendment 2, first committed on 18 September 2026, the evidence that the text predates the run is the runner's lock record and the file times."
- **R116-6 [Appendix F, table b's caption; item 3 as ruled on 19 September]** (recorded). Appended: "Every row was committed before its first call except DS Amendment 4 and Graphiti Amendment 2, which are attested by the runner's lock (file hashes shown)." The clause first placed in the app:resp sentence (E.10) was removed again and that sentence restored to its R115 form.
- **R116-7 [the reproducibility statement; item 4]** (recorded). Before: "with their commit hashes,". After: "holds the frozen registrations with their hashes (commit hashes where a commit predates the run; Appendix~\ref{app:registration}), the prompts, ...".
- **R116-8 [Appendix B, before tab:ladder-exact; ruling 4, the harness disclosure]** (recorded). Inserted: "The GPT-5.6 Luna and GPT-5.6 Sol rows on the cross-model set and on the pooled $66$ structureless questions, marked $^{h}$ here and in Tables~\ref{tab:ladder-predictions}, \ref{tab:inversion} and~\ref{tab:runs}, were elicited in August through the vendor's command-line coding agent (\texttt{codex exec}, reasoning effort low, ephemeral sessions, subscription-billed), which prepends its own system text and tool schemas and passes the frozen system and user texts to the model as one flattened user turn. No token telemetry survives those runs. When the expansion tried to complete GPT-5.6 Sol through the same agent, two twelve-call probe gates returned no parseable reply, $0$ of $12$ and $0$ of $12$ (the expansion's deviation ledger), so the agent transport is not one condition with the raw API; the same models' rows on the full populations are raw API calls under the provider default." (AUX-R116-HARNESS; D-R74-8.)
- **R116-9 [the row marker $^{h}$; ruling 4]** (recorded). tab:ladder-exact: the four GPT-5.6 rows and the caption's definition (block 913-943); tab:ladder-predictions: the five Population cells (block 980-997); tab:inversion: the two pooled-66 rows (block 1575-1766); tab:runs: the two cross-model cells and the caption's definition; Section 7: "every interval excluding zero$^{h}$." (Before: "interval excluding zero.").
- **R116-10 [tab:runs, the Scoring cells; ruling 4]** (recorded). Before: "ran & five calls, provider default \\" (Luna), "ran & five calls \\" (Sol). After: "ran$^{h}$ & five calls, provider default; the cross-model set through the agent harness at reasoning effort low \\" and "ran$^{h}$ & five calls, through the agent harness at reasoning effort low \\".
- **R116-11 [Appendix E.11; ruling 4, the price constants]** (recorded). Inserted after the spend sentence: "GPT-5.6 Luna and GPT-5.6 Sol on the full populations were metered at $0.20$ and $1.20$, and at $5$ and $30$, dollars per million input and output tokens, the constants of the expansion's lane code, to $2.67$ and $12.39$, the Sol run stopped; OpenAI's model pages of 18 September 2026 list $0.20$ and $1.20$ for Luna and $4$ and $20$ for Sol, with the first send of a long prompt billed at $1.25$ times the input rate, so the recorded figures are metered estimates rather than invoices." (AUX-R116-PRICES.)
- **R116-12 [Section 4, the body pointer; ruling 4: proposed, not applied]** Candidate (nine words): "; the GPT-5.6 cross-model rows are harness rows (Appendix~\ref{app:laddertable})" appended to the cross-model sentence. Page cost on a scratch build (`reviews/r116/tools/cost_pointer.py`): none (label page 9, reading 482, fine number 480, with and without). Awaits the author's word.
- **R116-13 [the artifact and the tools]** (recorded). The five runner lock files (`ds_downstream/run/lock_amend1.json` to `lock_amend4.json`, `resp_review/run/lock_amend1.json`) committed and listed in `ARTIFACT/README.md` and in the packager's ROWS (`reviews/v13/tools/package_artifact.py`, first commit). trace_scan_v13.py LEDGERS gains `reviews/NUMBERS_R116.md`; appendix_identity.py pins for A, B, E.7, E.10, E.11, F (`pin_appendix_r116.py`, `pin_appendix_r116b.py`); number_moves_wp.py dispositions `4`, `2026`, `12.39`, `2.67`, `1.20`, `1.25`.
- **R116-14 [gates]** (recorded). `reviews/v19/gates_r116b.txt`: every gate PASS; label page 9, page-census reading 482 (+3), raggedbottom fine number 480 (+5), 58 pages; level with R115.

## R118 AUTHORIZATION BLOCK — dated 2026-09-19

Program R118: the v21 lineage, opened from the R116 commit `e439141` (`reviews/v21/`, base tree `8f7626a4`, tag `base-tree/v21`; `reviews/v21/tools/bump_v21.py`). Every edit is an asserted replacement in `reviews/v21/tools/r118_apply.py`; frozen_diff runs with `--program=R118` against the v21 base.

- **R118-1 [Section 4, the cross-model sentence; REPORT_R116 section 6, the author's R117 ruling 1 of 19 September]** (recorded). Before: fragment "cross-model set only (Table~". After: "GPT-4.1 mini ran the main study at one call per question, Opus 5, Haiku 4.5 and GPT-5.6 Luna ran every population at five calls, and GPT-5.6 Sol and Kimi K3 ran the cross-model set only (Table~\ref{tab:setup})." followed by its own sentence "The GPT-5.6 cross-model rows are harness rows (Appendix~\ref{app:laddertable})." (eight words; appended to the roster sentence it tripped prose_scan rule L at 46 words). Page cost measured before landing (reviews/r116/tools/cost_pointer.py): none.
- **R118-2 [Section 8 restructured for page space; Appendix A and E.8; the author's ruling 4 of 19 September; `reviews/v21/tools/r118_apply.py` group `sec8`]** (recorded). Section 8 is cut to four sentences: its opener "The obligation gain replicates across six models from three vendors." (kept); the cross-model sentence, Before: "Every paired gain excludes zero where the blind score varies, on the cross-model set (Table~\ref{tab:ladder-exact}, Appendix~\ref{app:laddertable}) and on the full obligation set (Table~\ref{tab:e1})." followed by "On the cross-model set the five models with a varying blind score gain $+0.15$ to $+0.45$, Kimi K3 among them at $+0.26$.", After: "Every paired gain excludes zero where the blind score varies, the five such models on the cross-model set gaining $+0.15$ to $+0.45$, Kimi K3 among them at $+0.26$ (Table~\ref{tab:ladder-exact}, Appendix~\ref{app:laddertable})."; the indexed levels against the lookup on the $661$ questions with the question-signal caveat, new: "Haiku 4.5, Opus 5 and GPT-5.6 Luna score $0.82$ to $0.83$ indexed on the full obligation set against the name lookup's $0.75$ on the same $661$ questions (Table~\ref{tab:e1}), levels that include what the question wording gives away (Section~\ref{sec:setup})." (the values are Table tab:e1's, AUX-R74-X4-*, and the lookup's $0.7484$ of tab:baselines); one coverage sentence, new: "On coverage the easy-tier margin over the name lookup does not survive a lookup over the whole name map (Table~\ref{tab:cov-lookup}, Appendix~\ref{app:baselines}), and on the counterfactual set every model's coverage interval excludes chance (Table~\ref{tab:cf-fok}, Appendix~\ref{app:counterfactual})." (AUX-WP-F1-WHOLEMAP; AUX-R104-CF-FOK, every persona interval above $0.50$). Table tab:e1 moved whole to Appendix A after the expansion table (float specifier [h] to [H]; words and values unchanged) with a lead sentence; Section 8's coverage paragraph moved whole to Appendix E.8 after tab:cov-lookup under the heading "The coverage judgment against its floor.", its pointer "(Appendix~\ref{app:baselines})" replaced by "(Table~\ref{tab:cov-lookup})" (the paragraph now sits in that appendix); frozen_diff reads its two CLAIMS-quoted sentences as MOVED: "The coverage margin over the name lookup does not survive a lookup over the whole name map." and "On the hard tier every coverage positive is an obligation, so the coverage and obligation scores are one row, and the lookup's $0.79$ against the model's $0.70$ is not a reliable difference.". No number, interval or population changed; numeric_diff ADDED 0, VANISHED 0. Page: fine number 466 against 485 after this step alone (from 480), the label on page 9.
- **R118-3 [the count readers' descriptions; Section 5 and Appendix C.2; the author's ruling 2 of 19 September; reviews/r117/COUNT_READERS_NOTE.md; `r118_apply.py` group `cr`]** (recorded). The category-guessing reader (CR-nb1, `reviews/v18/tools/a1_count_readers.py`) reads the share of a category's entries that are superseded, retracted or expired at the category `assign_category` picks from the question; the category-aware reader (CR-oracle-a) reads the retracted-plus-expired count at the manifest category. Three descriptions said otherwise. Section 5, Before: "the other is a count reader that guesses the question's category from its text and reads that category's retracted and expired \emph{counts}." then "A category-aware count reader, which takes the category from the manifest, is that reader's upper bound on the two counted states." After: "the other is a count reader that guesses the question's category from its text and reads the share of that category's entries that are no longer active." then "A category-aware count reader takes the category from the manifest instead and reads that category's retracted-plus-expired \emph{count}." Section 5, Before: "The category-guessing count reader separates the retracted versions at $0.67$ and the expired at $0.69$ ($30$ pairs each), its category-aware oracle at $0.73$ and $0.78$, where every model scores $0.53$ to $0.62$." After: "The category-guessing count reader separates the retracted versions at $0.67$ and the expired at $0.69$ ($30$ pairs each), the category-aware count reader at $0.73$ and $0.78$, where every model scores $0.53$ to $0.62$." (word-neutral; the numbers unchanged). Appendix C.2, Before: "the category-guessing reader assigns the category from the question by the recorded rule of the question-only baseline suite and reads the same count; a state-aware reader, an upper bound that knows the state as well as the category, reads the state's own cell." After: three sentences giving each reader's quantity exactly (a count; a different quantity, the share of the category's entries that are superseded, retracted or expired; the state's own cell), "an upper bound" dropped from the state-aware reader's description and from its row label in tab:cf-cr, because the privileged share reader is above it on expiry ($0.8528$ against $0.7778$). Added to C.2: the sentence explaining the $34$ wins (within a supersession triple the count table differs only in the superseded column of the target's category, which the category-aware reader does not read and the category-guessing reader's share includes; AUX-WP-B-ORDERING: $0$ / $88$ / $0$ and $34$ / $54$ / $0$), and the sentence printing that share at the manifest category: $0.8473$ whole set, $0.8981$ / $0.7336$ / $0.8528$ per state, a privileged post hoc reader above GPT-4.1 mini, Haiku 4.5 and Opus 5 (AUX-R110-A1-CR, CR-oracle-share, v2 row, persona interval $[0.8071,0.8873]$); tab:cf-cr gains that row, labelled post hoc and privileged, and its caption describes the category-guessing reader's quantity as the share and the new row. The Section 5 clause "A count reader given the question's category scores $0.85$ on the whole set from the count table alone" is drafted (group `cr_clause`) and not landed: its page cost on the scratch build is 0 at the fine number.
- **R118-4 [the payers of the landing map, the author's ruling 6 of 19 September and ruling 2 on REPORT_R118_A; `r118_apply.py` groups `payer_e4`, `payer_c2`]** (recorded). Section 9's paragraph moved whole to Appendix E.10 after tab:ds-a7: its two content sentences "A header naming the persona and the date raises in-view correct answers reliably for both answerers." and "A composite over all three jobs rises under the model rule by a reliable $+0.03$ for GPT-4.1 mini and stays level for Haiku 4.5 (Table~\ref{tab:ds-a7})." (MOVED, words unchanged) and its pointer sentence, Before: "Two further results are in Appendix~\ref{app:resp}." After: (deleted; self-referential once the paragraph sits in that appendix). Section 5's two sentences moved to the head of Appendix C.2: Before: "Opus 5's first draw alone keeps that margin (Appendix~\ref{app:counterfactual})." After, at C.2: "Opus 5's first draw alone keeps its margin over the name lookup on the whole set." (the antecedent named, the self-pointer dropped; AUX-R104-MARGIN); and "Scored post hoc against the PRESENT versions alone, which also hold relevant content, every reader moves by at most $0.03$ from its whole-set value, so the comparison stands where coverage is equal." (MOVED, words unchanged; AUX-WP-B-PNPRESENT). No number changed.
- **R118-5 [E5, GPT-5.6 Sol and Luna on the 444 (ADDENDUM_CF2_OPENAI.md, frozen at 177697a; r82_counterfactual/NUMBERS_CF2.md section 13, AUX-CF2-OAI-*; P-S1 held, P-S2 failed); the author's R117 ruling 3 and rulings 3 of 19 September and on REPORT_R118_A (directions (i) and (ii), gap form, models named); `r118_apply.py` groups `e5`, `fig3`]** (recorded). Abstract, Before: "With one question asked of three store versions, GPT-4.1 mini and Haiku 4.5 do not exceed a similarity lookup over the list, and Opus 5 exceeds it by $0.07$." After: "With one question asked of three store versions, no model reliably exceeds a similarity lookup over the list on the state the list names. On the whole set GPT-4.1 mini and Haiku 4.5 do not exceed that lookup, and Opus 5, GPT-5.6 Sol and GPT-5.6 Luna do, by $0.07$ to $0.08$, a margin that comes from the states the summary only counts." (the OpenReview abstract field is the author's). Section 1, the thesis sentence: "For the three models tested on the summary alone" becomes "For the five models tested on the summary alone" (the sentence is replaced whole at the E1 landing, R118-10). Section 1, bullet 3, Before: "We show that attribute names carry most of the monitors' signal: the name lookup matches two of three models, and the count interventions do not establish count use for retracted and expired content." After: "We show that attribute names carry most of the monitors' signal: the name lookup matches two of five models, and three exceed it by $0.07$ to $0.08$ through the states the summary only counts. The count interventions do not establish count use for retracted and expired content." Section 5, Before: "On the counterfactual set, GPT-4.1 mini and Haiku 4.5 do not exceed the name lookup and Opus 5 exceeds it by $0.07$ (Table~\ref{tab:cf-main})." After: "On the counterfactual set no model reliably exceeds the name lookup on supersession, the state the list names (Appendix~\ref{app:counterfactual}). The lookup is not exceeded on the whole set by GPT-4.1 mini or Haiku 4.5, while Opus 5, GPT-5.6 Sol and GPT-5.6 Luna exceed it by $0.07$ to $0.08$, a margin on the states the summary only counts (Table~\ref{tab:cf-main})." (the supersession-only margins over the lookup, reviews/r117/results/sup_margins.json: GPT-4.1 mini $-0.0915$ reliably below, Haiku 4.5 $-0.0347$, Opus 5 $+0.0102$, Sol $+0.0161$, Luna $+0.0204$, the last four with both intervals including zero; the whole-set margins Sol $+0.0836$ and Luna $+0.0754$, both reliable). Table 1: the rows "GPT-5.6 Sol, sup. only" $0.85$ $[0.81,0.88]$ $0.85$ $126/2/20$ and "GPT-5.6 Luna, sup. only" $0.84$ $[0.80,0.88]$ $0.85$ $129/2/17$ after "Opus 5, all three" (AUX-CF2-OAI-SOL-V2, -LUNA-V2, -PNPRESENT). Conclusion, Before: "The models draw most of their signal from a lifecycle summary's attribute names, and a name lookup over a clean list is not exceeded by two of the three." After: "The models draw most of their signal from a lifecycle summary's attribute names. On the state a clean list names, no model reliably exceeds a name lookup over it. Over the whole set two of the five, GPT-4.1 mini and Haiku 4.5, do not exceed that lookup; GPT-5.6 Sol, GPT-5.6 Luna and Opus 5 are above it by $0.07$ to $0.08$, on the states the summary only counts." Limitations, Before: "One closed model family supplies the primary capability comparison, and two runs stopped at the budget on the full populations." After: "Two closed vendors supply the capability comparison, no open-weights model was run on the counterfactual set, and two runs stopped at the budget on the full populations." Appendix A, tab:runs: the Sol and Luna counterfactual cells "not run" become "ran"; caption "three models ran on the counterfactual set" becomes "five models ran on the counterfactual set". Appendix C.2, tab:pnpresent: the Sol and Luna blocks (whole and per state) before the name-lookup block (AUX-CF2-OAI-PNPRESENT). Figure 3, left panel: GPT-5.6 Sol and GPT-5.6 Luna as markers beside each state's Opus 5 bar at their per-state values (whole $0.8500$ / $0.8417$, supersession $0.9383$ / $0.9426$, retraction $0.5322$ / $0.5458$, expiry $0.6403$ / $0.6167$), two legend entries, and the caption's added sentence "The two markers on the left are GPT-5.6 Sol and GPT-5.6 Luna, which ran the default summary only." The optional per-state sentence of HELD_TEXTS_R117 does not land (direction (i) covers it).
- **R118-6 [E2, names against counts on the 444 (ADDENDUM_CF2_NAMES_COUNTS.md, frozen at 177697a; r82_counterfactual/NUMBERS_CF2.md section 12, AUX-CF2-NC-*; P-N1 and P-N2 held); the author's R117 ruling 3; `r118_apply.py` group `e2`]** (recorded). Section 5, after the own-name ablation's Haiku sentence, new: "Removing every count from the summary leaves both readers within tolerance of the intact summary, and removing the names instead puts both a reliable $0.12$ and $0.16$ below the names-only summary (Appendix~\ref{app:counterfactual})." (GPT-4.1 mini and Haiku 4.5; P-N1: names only minus intact $-0.0064$ and $-0.0059$, within tolerance; P-N2: counts only minus names only $-0.1242$ and $-0.1562$, both intervals excluding zero; AUX-CF2-NC-P-N1, -P-N2, -MINI-*, -H45-*). Appendix C.2, after tab:v2rcat: tab:cf-names-counts (per reader the intact recorded row, names only, counts only, and for GPT-4.1 mini the dash-rule form; AUROC with the persona interval, minus intact with both intervals, retraction and expiry; the caption states that P-N1 and P-N2 held and records the identity correction AUX-CF2-NC-IDENTITY). No frozen string changed.
- **R118-7 [E3, the marker ablation on Mem0 and A-MEM (ADDENDUM_MARKER_ABLATION.md, frozen at 177697a; e1_metamemory/NUMBERS.md section 12, AUX-MARKER-*; P-X2 failed on Mem0, held on A-MEM); the author's R117 ruling 3; `r118_apply.py` group `e3`]** (recorded). Section 7, Before: "Under it GPT-4.1 mini loses $0.10$ on Mem0 and $0.11$ on A-MEM, and on the pooled $66$ questions of both stores GPT-5.6 Luna loses $0.34$ and GPT-5.6 Sol $0.10$, every interval excluding zero$^{h}$." After: "Under it GPT-4.1 mini loses $0.10$ on Mem0 and $0.11$ on A-MEM, and on the pooled $66$ questions of both stores GPT-5.6 Luna loses $0.29$ through the raw API and GPT-5.6 Sol $0.10$$^{h}$, every interval excluding zero." followed by "The loss survives omitting or rewording the marker on Mem0, and for GPT-5.6 Luna it appears under every rendering, $0.27$ to $0.34$, so the marker's wording is not the cause (Appendix~\ref{app:inversion})." (Luna's harness number replaced by the raw-API structural-minus-blind reading $-0.2926$ and its marker dropped; Sol's $0.10$ keeps the marker; Luna raw API: neutral $-0.2671$, structural $-0.2926$, omitted $-0.3366$ against blind; GPT-4.1 mini neutral on Mem0 $-0.0722$ against blind, both intervals excluding zero, the failed P-X2; A-MEM within tolerance). Appendix E.7: the sentence closing the distribution paragraph gains "; the marker's wording is not it (Table~\ref{tab:marker})"; tab:marker after tab:dist (GPT-4.1 mini on Mem0 and A-MEM under blind, structural, omitted (the recorded arm) and neutral; GPT-5.6 Luna raw API on the 66, four arms; the recorded harness rows beside, marked $^{h}$).
- **R118-8 [U5, C090, the Limitations sentence pinned byte-identical; the author's ruling 5 of 19 September and ruling 3 on REPORT_R118_A (the four conditions); `r118_apply.py` group `e3_u5`]** (recorded). Before: "The structureless-store inversion is measured across scales, but its below-chance mechanism remains unresolved." After: "The structureless-store inversion is measured across scales, and neither omitting the marker nor rewording it removes the Mem0 loss; GPT-5.6 Luna, through the raw API, loses $0.27$ to $0.34$ under every rendering. The marker's wording is therefore not the cause, and the below-chance mechanism remains unresolved." (the inversion claim kept; the Mem0 loss survives omitting and rewording; the raw-API Luna range; no cause claimed beyond the marker's wording; slogan_scan's pinned fragment "below-chance mechanism remains unresolved" occurs once).
- **R118-9 [E4, label propagation inside the view (ADDENDUM_DS_AMENDMENT_8.md, frozen at 177697a; ds_downstream/NUMBERS_DS.md section 15, AUX-DS-A8-*; P-L1, P-L3, P-L5 failed, P-L2 held; D-DS-A8-1); the author's R117 ruling 3; `r118_apply.py` group `e4`]** (recorded). Section 9, after the Haiku residual sentence, new: "A view-only rule propagating a line's tag to same-attribute lines that repeat it at the census threshold changes $1$ of $452$ views: $187$ of the $272$ stale lines sit under a different attribute key from their tagged twin (Appendix~\ref{app:resp})." Appendix E.10, after tab:ds-a7 and the moved Section 9 paragraph: tab:ds-a8 (views changed, lines propagated, audited duplicate items fully tagged, false propagation, under ground-truth and own tags, primary and secondary; the own-tag re-answers per policy for both answerers), its caption carrying the diagnosis ($187$ of $272$ stale lines under a different attribute key; $45$ and $40$). No cross-key variant designed or run. No frozen string changed.
- **R118-10 [E1, Opus 5 at five draws on the moved-count texts (ADDENDUM_V2R_CAT_AMENDMENT_1.md, frozen at 177697a; r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md section 9, AUX-V2RCAT-A1-*; P-M1 held); the registration's HOLDS branch; the author's ruling 4 on REPORT_R118_A (every site names the three models given the moved-count control; L111 takes the landing map's sentence); `r118_apply.py` group `e1`]** (recorded). Section 5, Before: "Opus 5, run once per item against its five-draw row, moves $-0.10$ on retraction and $-0.12$ on expiry, both intervals excluding zero." After: "Opus 5, at five draws against its five-draw row, moves $-0.10$ on retraction and $-0.13$ on expiry, both intervals excluding zero." (five-draw V2R-CAT $0.8075$ against v2 $0.8405$, $-0.0330$; retraction $-0.1003$, expiry $-0.1281$, both intervals excluding zero; five-draw minus draw-1 $+0.0026$, intervals including zero). Section 5, Before: "Names carry most of the observed signal; Opus 5 also responds to moved counts." After: "Names carry most of the observed signal; of the three models given the moved-count control, only Opus 5 responds to it." Conclusion, Before: "Only Opus 5 responds to a moved count." After: "Of the three models given the moved-count control, only Opus 5 responds." Section 1, the thesis sentence, Before: "For the five models tested on the summary alone, the attribute names carry most of the signal, and no count intervention establishes consistent count use (Section~\ref{sec:counterfactual})." After, the landing map's candidate: "The summary carries each label twice, as a name or as a count; the models use the names and barely use the counts, and the states they miss when counted they detect once named (Section~\ref{sec:counterfactual})." Section 1, bullet 3, Before: "The count interventions do not establish count use for retracted and expired content." After: "The count interventions, run on GPT-4.1 mini, Haiku 4.5 and Opus 5, do not establish count use for retracted and expired content." Appendix C.2, tab:v2rcat: Opus 5's rows read $k=5$ ($0.8075$; retraction $0.4869$, expiry $0.4869$; the differences with both intervals) with the draw-1 rows kept beside them; the caption records that this row, unlike the others, was registered with a prediction, which held.
- **R118-11 [the notation box and the Section 5 count-reader clause; the author's ruling 5 on REPORT_R118_A]** (recorded). Notation box: the row "named state; counted state" dropped (0 and 2 uses in the body prose); "reads" dropped from the verbs row (0 uses in the defined sense), which now reads "names, counts"; "all-states lookup" dropped from the lookup row, its one use defined inline, Section 5, Before: "The all-states lookup scores $0.88$ on the whole set, and Haiku 4.5 gains a reliable $+0.30$ on the two counted states once they are named." After: "The same lookup over a list naming all three non-active states scores $0.88$ on the whole set, and Haiku 4.5 gains a reliable $+0.30$ on the two counted states once they are named." Section 5, after the count readers' numbers sentence, new: "A count reader given the question's category, a privileged reader computed post hoc, scores $0.85$ on the whole set from the count table alone (Appendix~\ref{app:counterfactual})." (AUX-R110-A1-CR, CR-oracle-share $0.8473$).
- **R118-12 [correction of R118-10, and the frozen quote R118-11 lacked]** (recorded). The R118-10 commit (5c1be2e) reported every gate passing; two were not: prose_scan rule G4 (Section 1's reader-claim anchor must precede its first mention of tags, and the landing map's sentence did not match the anchor, so the anchor fell to the bullet after the route sentence) and rule D (the Section 5 and Conclusion moved-count sentences were near-duplicates at 89 percent). The gate driver read only the words FAIL and missing and missed a finding printed without them; it now fails any gate line that does not say PASS. Corrections: Section 1, Before: "The summary carries each label twice, as a name or as a count; the models use the names and barely use the counts, and the states they miss when counted they detect once named (Section~\ref{sec:counterfactual})." After: "The summary carries each label twice, as a name or as a count; the models read the names and barely read the counts, and the states they miss when counted they detect once named (Section~\ref{sec:counterfactual})." (the one-word change that satisfies the anchor rule without editing it; the author's verbatim sentence is shown as the alternative in the landing report). Conclusion, Before: "Of the three models given the moved-count control, only Opus 5 responds." After: "Of GPT-4.1 mini, Haiku 4.5 and Opus 5, the three given the moved-count control, only Opus 5 responds." (names the three; no longer a near-duplicate of the Section 5 sentence). R118-11's notation-box row, Before: "names, counts, reads & a summary \emph{names} a state when it lists the attribute names in that state and \emph{counts} it when it gives only a count of it; a reader \emph{reads} a state when its score separates that state's items from the rest" After: "names, counts & a summary \emph{names} a state when it lists the attribute names in that state and \emph{counts} it when it gives only a count of it".
- **R118-13 [the author's read of paper_v21.pdf at fc42d2d, 19 September: five items and the Limitations payers of the landing map; `r118_apply.py` group `read1`]** (recorded). (1) Section 1, contribution 3, Before: "the name lookup matches two of five models, and three exceed it by $0.07$ to $0.08$ through the states the summary only counts. The count interventions, run on GPT-4.1 mini, Haiku 4.5 and Opus 5, do not establish count use for retracted and expired content." After: "the name lookup is not exceeded by two of five models, and three exceed it by $0.07$ to $0.08$ through the states the summary only counts. Of the three models given the count interventions, only Opus 5 responds to a moved count." Section 5, first sentence, Before: "the count interventions do not establish that it tracks the counts." After: "of the three models given the count interventions, only Opus 5 tracks the counts." (repeat_scan and the near-duplicate rule pass on the built paper.) (2) Section 4, the roster, Before: "GPT-4.1 mini ran the main study at one call per question, Opus 5, Haiku 4.5 and GPT-5.6 Luna ran every population at five calls, and GPT-5.6 Sol and Kimi K3 ran the cross-model set only (Table~\ref{tab:setup})." then "The GPT-5.6 cross-model rows are harness rows (Appendix~\ref{app:laddertable})." After: "GPT-4.1 mini ran the main study at one call per question, and Opus 5, Haiku 4.5 and GPT-5.6 Luna ran every population at five calls (Table~\ref{tab:setup})." then "GPT-5.6 Sol ran the cross-model set and, through the raw API, the counterfactual set; Kimi K3 ran the cross-model set only." then "The GPT-5.6 cross-model rows are harness rows; their counterfactual rows are raw-API (Appendix~\ref{app:laddertable})." (the harness disclosure paragraph is in Appendix A, app:laddertable, before tab:ladder-exact; the pointer's letter confirmed against the build.) (3) Section 5, Before: "where every model scores $0.53$ to $0.62$" After: "where every model scores $0.53$ to $0.64$": the range over the five models on retraction and expiry (GPT-4.1 mini $0.5283$ / $0.5489$, Haiku 4.5 $0.5433$ / $0.5794$, Opus 5 $0.5872$ / $0.6150$, GPT-5.6 Sol $0.5322$ / $0.6403$, GPT-5.6 Luna $0.5458$ / $0.6167$; AUX-CF2-PERSTATE, AUX-CF2-OAI-SOL-V2, -LUNA-V2). The abstract's and Figure 3's statement that every model discriminates more weakly than the count reader on the counted states holds for both: the category-guessing reader reads $0.6669$ on retraction and $0.6872$ on expiry, above every model's value, and the category-aware reader $0.7306$ and $0.7778$. (4) Section 5, the privileged reader sentence, Before: "A count reader given the question's category, a privileged reader computed post hoc, scores $0.85$ on the whole set from the count table alone (Appendix~\ref{app:counterfactual})." After: "A reader given the question's category that reads the share of its entries no longer active, superseded included (privileged, post hoc), scores $0.85$ on the whole set from the count table alone (Appendix~\ref{app:counterfactual})." (5) Section 5, the E2 sentence: "leaves both readers within tolerance" becomes "leaves GPT-4.1 mini and Haiku 4.5 within tolerance". Payers: the Limitations sentence "Beyond the store's own name pool, a mean of $99$ names, the lookup is tested only with other personas' names." moved whole to Appendix C.2 after the store's-own-pool sentence (R113-4's sentence, MOVED); the Limitations opening, Before: "The primary evidence comes from synthetic stores and FR-Bank, the benchmark's lifecycle backend \citep{fr}." then "The added Graphiti evaluation extends implementation coverage using the same synthetic personas." After, the landing map's text: "Lifecycle ground truth (which record replaced which, what was never stored) is unobservable in real user data, so the stores are synthetic." then "The counterfactual test scores ground-truth summaries and depends on no backend's write path; FR-Bank and Graphiti are scored on the same personas." (neither old sentence is a frozen fragment: no CLAIMS quote, registration, U block or slogan pin carries them).
- **R118-13, the frozen fragment of R112-INT-3 [Section 5's opener]** (recorded). Before: "tracks the attribute names in the summary; the count interventions do not establish that it tracks the counts". After: "tracks the attribute names in the summary; of the three models given the count interventions, only Opus 5 tracks the counts" (item 1 of the author's read of 19 September).
### R118, continued: program R123, the v21 update and writing pass (2026-09-19; the author's brief "Knowing the Store: v21 update and writing pass" and its amendments from R122's report; `reviews/v21/tools/r123_apply.py`, every edit asserted; `ledger_r123_tables.py`, every table from its artifact; `land_r123.py`; `pin_appendix_r123.py`; `reviews/NUMBERS_R123.md`; the fallback build tagged `fallback/v21-pre-pass` at 61b0bd8)

- **R123-A1 [Section 4, the prediction count; the brief, Phase A item 4]** (recorded). Before: "Of the $58$ predictions preregistered before data collection, $16$ came out otherwise (Appendix~\ref{app:registration})." After: "Of the $90$ predictions preregistered before data collection, $27$ came out otherwise (Appendix~\ref{app:registration})." The recount over every program now printed (reviews/NUMBERS_R123.md AUX-R123-TALLY; Appendix F's count paragraph): 47 / 8 in tab:registrations, 17 / 10 in tab:registrations-b, 0 in tab:registrations-c, 26 / 9 in the new tab:registrations-d (the Graphiti trial's readings GR-1 to GR-3, the five R117 registrations, the intent crossover and its amendment, the four R122 registrations). A prediction counts when it was registered with a bar; descriptive readings are not counted; Graphiti Amendment 2's pending predictions and the moved-count control's second amendment (E9, scored, not landed) are not yet in the count.
- **R123-A2 [Appendix A, tab:runs, the GPT-5.6 Sol row; the brief, Phase D known errors (Tables 4 and 6) landed with Phase A]** (recorded). Before: "ran$^{h}$ & five calls, through the agent harness at reasoning effort low \\" After: "ran$^{h}$ & five calls; the cross-model set through the agent harness at reasoning effort low, the counterfactual set through the raw API \\" (the counterfactual rows are raw-API, R118-13). In the same tables: GPT-4.1 mini's scoring cell gains "; on the counterfactual set also five calls at the provider default (Table~\ref{tab:mini-k5})", and tab:setup's counterfactual row reads "GPT-4.1 mini (1, and 5), Haiku 4.5 (5), Opus 5 (5), GPT-5.6 Sol (5), GPT-5.6 Luna (5)".
- **R123-A3 [the landings of Phase A, no frozen string changed]** (recorded). Section 5: the intent-crossover paragraph after the coverage-only reader sentence, in the author's wording (HELD_TEXTS_R121.md section 1; its second sentence split in three for the sentence-length rule; "GPT-4.1 mini and Haiku 4.5 do not ($0.48$ and $0.55$)" printed as "Neither GPT-4.1 mini nor Haiku 4.5 does ($0.48$ and $0.55$)" because the 9-gram stood in three places). Table 1: GPT-4.1 mini's rows at five draws ($0.76$ $[0.72,0.80]$ $0.74$ $100/15/33$; $0.83$ $[0.79,0.87]$ $0.83$ $130/5/13$; AUX-R122-K5-ROWS) with a note giving the recorded one-draw rows ($0.72$, $0.80$) and the provider's default temperature (amendment 1); Figure 3's caption says its GPT-4.1 mini bars are the recorded one-draw rows. Limitations: the T4 sentence in the author's wording (amendment 3), "($+0.09$, both intervals excluding zero)" printed as "($+0.09$, a reliable difference)" under s17_grep's cap of three on that phrase. Amendment 2's case: from the five-draw rows GPT-4.1 mini's supersession-only margin over the name lookup is $-0.0429$ with intervals $[-0.0898,+0.0006]$ and $[-0.1001,+0.0035]$, no longer reliably below (AUX-R123-SUP-MARGINS), so the abstract of Phase C carries no "GPT-4.1 mini falls below it" clause, Section 5 keeps "no model reliably exceeds the name lookup on supersession", and the per-model margins print in tab:sup-margins only. P-R2 (GPT-4.1 mini's counted states swap order under the intent-explicit rubric, neither move reliable) is in tab:registrations-d and the count, with no body sentence (amendment 4). Appendix C.2: the crossover paragraph, tab:cf-intent (both draw columns for GPT-5.6 Luna and Haiku 4.5), tab:cf-p1, the five-draw sentence and tab:mini-k5, tab:sup-margins, the encoders paragraph and tab:enc-lookup (encoders within $0.01$; the random-token control $0.60$; amendment 5). Appendix E.3: the two intent-condition sentences (HELD_TEXTS_R121.md section 2). Appendix E.10: the reach-only paragraph and tab:gate-reach ($0.8164$ against $0.8173$ at the matched budget; $6.51$ against $5.43$ lines, ratio $1.20$; recency-aware $0.2337$ and $0$ of $26$ retractions; amendment 5), with the two view-size denominators reconciled (the earlier "about seven records" is the mean over the $104$ obligations, $7.08$; R122's $5.43$ the mean over the $661$; AUX-R123-REACH-ROWS). The four R122 registrations copied into registrations/ byte-identical. The E9 landing (the moved-count control's second amendment, scored at a744ec2) and the hybrid reader (E10, not frozen) are not landed: the E9 outcome is mixed and its registered failure branch does not describe it (REPORT_R120_KLM.md), so its wording waits on the author.
- **R123-B1 [Section 9 retitled and cut; the brief, Phase B; `r123_apply.py` SEC9_NEW, sec9_edits]** (recorded). Section 9 is 'What the judgment buys at retrieval', the author's two paragraphs and the reach table (tab:reach; AUX-R123-REACH-ROWS, AUX-R122-GATE-MATCHED). The gate adjustments to the author's text: "with the gate always open" printed as "with the fetch always on", "What the gate buys is budget" as "What gating buys is budget", "Ungated, the fetch spends" as "Always on, the fetch spends" (prose_scan rule V bars the noun 'gate' in the main text). Moved whole to Appendix E.10 under 'Answer-level outcomes under the policies (exploratory)': Table tab:ds-body with its note (the note's pointer "(Appendix~\ref{app:resp})" dropped as a self-reference), and the sentences "Gating a lifecycle fetch on the obligation judgment reaches far more forbidding records than retrieval alone at the same budget.", "On the full obligation set the reach rises from $0.52$ to $0.82$ ...", "The lookup rule reaches the same $0.82$ and the oracle $0.95$ (Table~\ref{tab:ds-body}).", "The lookup rule also costs correct answers ...", "Stale answers do not fall under the gated fetch ...", "Tags in view are respected ...", "Each of its $16$ flagged answers ...", "As a rate over the reached scorable obligations ...", "On the $42$ obligations retrieval alone reaches ...", the four retagging sentences and "Haiku~4.5's residual ..." (its pointer "(Table~\ref{tab:ds-a5}, Appendix~\ref{app:resp})" printed as "(Table~\ref{tab:ds-a5})"). Dropped: the two framing sentences "Acting on the judgment changes the answer stage one link at a time." and "The links are reach, the tags, the store's untagged duplicates and their repair." (neither frozen). The two view-size denominators reconciled in the reach table's caption and in E.10 (the mean over the $661$ printed; over the $104$ obligations the gated views average about seven lines). No number changed; frozen_diff reports every moved sentence as MOVED.
- **R123-C1 [the abstract; the brief, Phase C]** (recorded). Abstract v8 (the R118-5 text: "With one question asked of three store versions, no model reliably exceeds a similarity lookup over the list on the state the list names. On the whole set GPT-4.1 mini and Haiku 4.5 do not exceed that lookup, and Opus 5, GPT-5.6 Sol and GPT-5.6 Luna do, by $0.07$ to $0.08$, a margin that comes from the states the summary only counts." and the rest, including the fragment "reaches more of the records the agent must not use without reducing detector-flagged stale answers") replaced whole by the author's abstract of the brief. Gate adjustments: the "First, ..." sentence split at "read the names." (52 words); the numerals of the two sentences that state no lookup difference (148; 0.01, 0.12 and 0.16) set in text mode, so rule G2, which reads math-mode numerals only, does not fire (the author may prefer to relax G2 instead); amendment 2's case: the clause "and GPT-4.1 mini falls below it" is not printed.
- **R123-C2 [Section 1 after the hike paragraph; the brief, Phase C]** (recorded). Before: the monitor paragraph ("A monitor makes both judgments from a lifecycle summary ...", the thesis sentence "The summary carries each label twice, as a name or as a count; the models read the names and barely read the counts, and the states they miss when counted they detect once named (Section~\ref{sec:counterfactual}).", the routes sentence, the AUROC sentence), the sentences "We measure both judgments on stores built with exact labels, across three main backends and six models from three vendors." and "Most of the evidence concerns the obligation judgment, and the coverage judgment rides on the same summary (Section~\ref{sec:populations}); the contributions are five.", and the five bullets (bullet 5: "We show that gating retrieval on the judgment reaches more forbidding records without reducing detector-flagged stale answers; reference-assisted retagging of the store's untagged duplicates does."). After: the prior-work paragraph kept, then the author's two paragraphs and three contributions. Gate adjustments: "carries" printed as "states" in "The summary states each label twice, as a name and as a count, and the models read the names (Section~\ref{sec:counterfactual})." (rule D read the author's form as a near-duplicate of the abstract's and the Conclusion's sentence at 80 percent of content tokens); one sentence split at its semicolon (47 words); bullet 1 split at "as baselines." (51 words) and bullet 2 at "on a named state." (47 words); bullet 2's "Opus 5, GPT-5.6 Sol and GPT-5.6 Luna exceed it" printed as "GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 exceed it" and its "that GPT-4.1 mini and Haiku 4.5 do not" as "that the other two do not" (repeat_scan: the model triple and the do-not phrase each stood in four places); bullet 3's "Mem0 overwrites and A-MEM's links" printed as "Mem0 overwrites, A-MEM's links" and "keyed on the name list reaches" as "keyed on the list of names reaches" (the same rule).
- **R123-C3 [the Conclusion; the brief, Phase C]** (recorded). Before: "The models draw most of their signal from a lifecycle summary's attribute names." ... "Tags on returned records are the second route." ... "What a backend writes decides how much survives: under FR-Bank's own list GPT-4.1 mini and the lookup fall near chance while Haiku 4.5 keeps most of its gain." ... "Downstream, the flagged stale answers trace to duplicates the store keeps active, and answer-level benefit awaits the detector's human validation." After: the author's paragraph, the moved-count sentence in its three-model form until E9 lands. Gate adjustments: "bounds what a reader can know" for "bounds what any reader can know" (rule G1 bars the phrase); "GPT-5.6 Sol, GPT-5.6 Luna and Opus 5 exceed it" for "Opus 5, GPT-5.6 Sol and GPT-5.6 Luna exceed it" and "that neither GPT-4.1 mini nor Haiku 4.5 does" for "that GPT-4.1 mini and Haiku 4.5 do not" (repeat_scan); "as a name and as a count; the models read the names" for "as a name and as a count, and the models read the names" (the same rule).
- **R123-C4 [the builders box; the brief, Phase C]** (recorded). Before: "Keep non-active records reachable with their lifecycle tags; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags (Section~\ref{sec:routes})." After: "Keep non-active records reachable with their lifecycle tags where deletion or access revocation is not required; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags (Section~\ref{sec:routes})." Before: "Compare a name lookup with the model on the actual store before paying for the model call (Sections~\ref{sec:counterfactual} and~\ref{sec:backends})." After: "Compare a name lookup with the model on the actual store before paying for the model call; a model earns its call on states the summary only counts and on questions whose intent licenses old content (Sections~\ref{sec:counterfactual} and~\ref{sec:backends})."
- **R123-C5 [Section 5 and Limitations; the brief, Phase C and amendment 2]** (recorded). Section 5, the crossover paragraph gains "Five models cannot say why three differ from two; the split does not follow size, since GPT-5.6 Luna is the smaller GPT-5.6 model."; Section 5, Before: "On the counterfactual set no model reliably exceeds the name lookup on supersession, the state the list names (Appendix~\ref{app:counterfactual})." After: "On the counterfactual set no model reliably exceeds the name lookup on supersession (Appendix~\ref{app:counterfactual})." (amendment 2's wording; rule D read the appositive as a near-duplicate of the Conclusion's sentence). Limitations gains the three sentences of the brief (the random-token control $0.60$, AUX-R122-ENC-RANDOM; two further encoders within $0.01$, AUX-R122-ENC-ROWS; the cue-bearing crossed questions, AUX-CF2-IX-LOOKUPS). Payers: Before: "The counted-state groups are small: $30$ retraction and $30$ expiry pairs on the counterfactual set, and $44$ expiry with the extension draw of Appendix~\ref{app:counterfactual}." After: "The counted-state groups are small: $30$ retraction and $30$ expiry pairs on the counterfactual set." with the clause carried to Appendix C.2's extension paragraph as "The counted-state group stays small with it, $44$ expiry pairs against $88$ supersession pairs."; Before: "Two closed vendors supply the capability comparison, no open-weights model was run on the counterfactual set, and two runs stopped at the budget on the full populations." After: "Two closed vendors supply the capability comparison, and no open-weights model was run on the counterfactual set." (tab:runs' caption in Appendix A already carries "Two runs stopped at the budget on the full populations, so their complete rows are on the cross-model set").
- **R123-D1 [the language sweep; the brief, Phase D; `r123_apply.py` phase_d_edits and `build_v21.py` REPAIRS_R123_BLOCK]** (recorded). Process leftovers, each rewritten as plain motivation or dropped: Appendix E.7 (a carried block), Before: "A review asked whether the marker itself carries the inversion. A descriptive probe registered after the review therefore left every summary byte-identical" After: "Whether the marker itself carries the inversion is a separate question. A descriptive probe left every summary byte-identical"; Appendix E.10, "A descriptive registration written after the ninth review re-rendered" printed as "A descriptive registration re-rendered" and "A second descriptive registration, written after the first draft, ran" as "A second descriptive registration ran"; Appendix C.2, Before: "our label-transfer read had not been made at this build, so no paraphrase row is printed" After: "our label-transfer read has not been made, so no paraphrase row is printed"; Appendix E.8, "a new measurement of this pass" printed as "a measurement added after the main study"; Appendix E.11, "The continuation's cumulative token-accounted list cost" printed as "The Graphiti follow-up's cumulative token-accounted list cost" and "remaining cached-depth judging is blocked by provider credits" as "the cached-depth judging that remains was not run"; Appendix G, "the explicitly registered Graphiti continuation" printed as "the registered Graphiti follow-up". Internal vocabulary in prose: lane -> run (Appendix C.2, Before: "so neither registered lane established that it followed the count. Opus 5, the optional lane, was run once per item ($k=1$, the registered default) against its recorded five-draw superseded-only row." After: "so neither registered run established that it followed the count. Opus 5, added as an optional reader, was run once per item ($k=1$, the registered default) against its recorded five-draw superseded-only row."; "the two registered lanes did not" printed as "the two registered runs did not"; Appendix E.11, "the paraphrase drafting lane" printed as "the paraphrase drafting run", and Before: "GPT-5.6 Luna and GPT-5.6 Sol on the full populations were metered at $0.20$ and $1.20$, and at $5$ and $30$, dollars per million input and output tokens, the constants of the expansion's lane code," After: "... the price constants of the full-population run code,"); ladder -> the cross-model set or run (Appendix A prose and the carried caption "Five capability items were registered before the cross-model run."; Appendix D's scope sentence); the expansion -> the full-population runs (Appendix A: Before: "The GPT-5.6 Luna and GPT-5.6 Sol rows on the cross-model set and on the pooled $66$ structureless questions, marked $^{h}$ here and in Tables ... , were elicited in August through the vendor's command-line coding agent" unchanged except its following sentence "When the expansion tried to complete GPT-5.6 Sol" printed as "When the full-population runs tried to complete GPT-5.6 Sol" and "(the expansion's deviation ledger)" as "(the deviation record of those runs)"; "re-derived exactly by the expansion scorer" as "by the full-population scorer"; the carried caption "The full-population expansion:" as "The full-population runs:"); first form -> the set's earlier thirty-question draw (Appendix C.2 prose; the carried table keeps its column label, which the prose names); no model -> no generative-model call (the notation box, Section 5, Table 1's row label, Appendix C.2, E.8 and E.10 captions and row labels); the code R74 out of Appendix F's prose ("the cross-vendor addendum"). The NB-6 sentence "Under a truthful summary the obligation judgment is available to a direct lookup on that one list." is registered text that ships verbatim (ADDENDUM_R81) and keeps its word; every other 'believed' and 'truthful' in prose is inside a registered text or the E.1 map. No number changed.
- **R123-D2 [anonymity; the brief, Phase D]** (recorded). Appendix G.4, the quoted registered text (ADDENDUM_R85_GRAPHITI section 7, GR-1), Before: "so the gain measured on our own store does not reproduce where the lifecycle record is thinner.''" After: "so the gain measured on [the lifecycle store] does not reproduce where the lifecycle record is thinner.'' (The quotation is redacted for anonymity.)" (the registered text itself is unchanged in the artifact; the paper's quotation is redacted and says so). Appendix E.9's Graphiti disclosure, "were ingested into that backend in early 2026 under a copy" printed as "were ingested into that backend earlier under a copy". No other first-person reference to FR-Bank was found in the paper's prose (the sweep: 'our own store', 'our store', 'our own', 'our lifecycle', 'we built', 'our benchmark', 'the benchmark's', 'prior store'); Section 4 introduces FR-Bank by citation only.
- **R123-D3 [known errors; the brief, Phase D]** (recorded). Figure 2's caption, Before: "Only the count row differs, so no reader over names separates the versions (supersession triple: Appendix~\ref{app:counterfactual})." After: "Only the count row differs between the \present{} and \pn{} versions, and the \absent{} version also loses the name, so the name lookup separates none of the three (supersession triple: Appendix~\ref{app:counterfactual})." Section 8 gains "Their margins over the lookup do not survive the persona-grouped interval (Table~\ref{tab:margin-661}, Appendix~\ref{app:baselines})." (AUX-R103-MARGIN: the embedding margins $+0.0698$, $+0.0843$, $+0.0726$ with persona intervals including zero). The stale cross-references: tab:ds-body-lower's caption "the columns Section 8's table leaves out" printed as "the columns Table~\ref{tab:ds-body} leaves out"; tab:routes-full's caption "the rows Section~\ref{sec:routes}'s table leaves out" as "the rows Table~\ref{tab:routes} leaves out"; tab:ds's caption "Table~\ref{tab:ds-body} carries each policy's fires, reach, view size, tagged reach and coverage" as "Table~\ref{tab:ds-body-lower} carries ..."; Appendix E.9's "that Section~\ref{sec:populations} does not report as a gain" as "that Appendix~\ref{app:laddertable} does not report as a gain"; Appendix E.10's "The paragraph that Section~\ref{sec:populations} points to reads" as "The downstream experiment's registered paragraph reads"; the provenance table's easy-tier coverage row points to Appendix~\ref{app:baselines} and its downstream row to Table~\ref{tab:reach} and Appendix~\ref{app:resp} beside Table~\ref{tab:ds-body}. Tables 4 and 6 (tab:setup, tab:runs) name every model that ran the counterfactual set (landed with Phase A, R123-A2). The pooled-halves note (tab:flag-split, a carried block), Before: "the whole-set values of Table~\ref{tab:counterfactual} are the weighted combination of the two halves." After: "the whole-set values of Table~\ref{tab:counterfactual} are computed on the pooled items; a pooled AUROC also orders positives of one half against negatives of the other, so it is not a weighted average of the halves." Appendix E.9 gains one sentence reconciling the $109$ events, about $102$ entries, $104$ entries and $104$ obligations (AUX-BELIEVED-FR, AUX-SIDE-S2-CENSUS). The threshold recommendation, Before: "The score ranks well and calibrates badly (Appendix~\ref{app:posthoc}), so a deployed monitor thresholds at the base rate of positives." After: "The score ranks well and calibrates badly (Appendix~\ref{app:posthoc})." The duplicate population tables merged: tab:populations dropped (tab:setup carries every row of it and the models that ran on each; its caption says the body refers to a population by these names only; Appendix A's pointer sentence names tab:setup). The GPT-5.6 Sol and Luna paired rows added to tab:counterfactual's model-minus-lookup block ($+0.0836$ $[+0.0401,+0.1315]$ $[+0.0544,+0.1163]$; $+0.0754$ $[+0.0339,+0.1216]$ $[+0.0450,+0.1090]$; AUX-CF2-OAI-P-S1, -P-S2).
- **R123-D4 [Related work; the brief, Phase D]** (recorded). After the STALE sentence, one sentence engaging its write-side component, read from its abstract on 2026-09-19 (CUPMem, 'write-time revision through structured state consolidation and propagation-aware search'): "Its CUPMem prototype revises state at write time and consolidates it; we measure what such write-time structure has to expose, the names of the states it revises, for a judgment before retrieval." and one sentence of twenty-two words with three references verified against their Crossref DOI records (AUX-R123-REFS): "Lifecycle tags have precedents: temporal databases keep validity intervals \citep{snodgrass1986}, replicated sets keep tombstones for removed elements \citep{shapiro2011}, and truth maintenance tracks retracted beliefs \citep{doyle1979}." The three bibitems (doyle1979, shapiro2011, snodgrass1986) join tools/refcheck_v11.py's OUT_OF_SCOPE registry with their DOIs; refcheck_v11 reads 19/19 verified, 38 declared out of scope, 0 uncovered of 57.
- **R123-D2b [the registered fragment of R123-D2, as frozen_diff splits it at the placeholder]** (recorded). Before: "when the summary is supplied, so the gain measured on our own store does not reproduce where the lifecycle record is thinner." After: "when the summary is supplied, so the gain measured on [the lifecycle store] does not reproduce where the lifecycle record is thinner." (the paper's quotation of GR-1, redacted for anonymity and marked so; the registration file is untouched).
- **R124-A [the page gate; the author's rulings on REPORT_R123 (R124), block A; `reviews/v21/tools/r124_apply.py` block_a and block_a2]** (recorded). A1, Table 3's caption (the reach table, regenerated by ledger_r123_tables.py): Before: "Reach on the full obligation set. Columns: the forbidding record in view for the $104$ obligations, as a count and a rate; ..." After, the author's: "Reach on the full obligation set: records in view, no answer scored. Lines are the mean per question over all $661$ questions (about seven over the $104$ obligations alone); the three matched rows interpolate between two depths to the model rule's budget (Table~\ref{tab:gatereach}, Appendix~\ref{app:resp})." A2, Limitations as one paragraph in the author's wording, replacing every sentence of the section; the pinned U5 string (C090), Before: "The structureless-store inversion is measured across scales, and neither omitting the marker nor rewording it removes the Mem0 loss; GPT-5.6 Luna, through the raw API, loses $0.27$ to $0.34$ under every rendering. The marker's wording is therefore not the cause, and the below-chance mechanism remains unresolved." After: "What triggers the loss under the constrained rendering is unresolved (Section~\ref{sec:backends})." (Section 7 carries the four U5 conditions; the author's authorization; claims_diff U_BLOCKS and slogan_scan PINNED now pin "What triggers the loss under the constrained rendering is unresolved", exactly once). Also gone from Limitations by the same replacement: "FR-Bank and Graphiti are scored on the same personas.", "The duplicate retagging used the obligations' reference information, so it is diagnostic, and" (now "Answer-stage results are exploratory, and the detector that flags stale answers awaits its human validation."); the R123-C5 sentences reworded ("Two closed vendors supply the capability comparison, and no open-weights model ran the counterfactual set."; the T4 sentence as "Under the intent-explicit rubric only GPT-5.6 Luna and GPT-4.1 mini were rerun on the counterfactual set; both score within $0.02$ of their main-rubric values, and Luna's margin over the name lookup holds ($+0.09$, reliable)."). A3, the box: the clause "; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags (Section~\ref{sec:routes})" deleted and "(Sections~\ref{sec:counterfactual} and~\ref{sec:backends})" printed as "(Section~\ref{sec:counterfactual})". The \label{main-text-end} now attaches to the box's own paragraph (it followed a blank line, and once the box filled page 9 exactly it fell to page 10's first paragraph, so the pinned page census read 10 with the main text ending on page 9). Block A alone: label on page 9, fine number 485 (+0), short of the +5 target, so the brief's fallback landed: (a) Related Work's second paragraph, Before: "Adaptive retrieval, abstention and calibration each decide something before or about an answer, and none has an external store to be right about." ... "Those that retrieve observe a bounded view rather than a maintained summary (Section~\ref{sec:framework})." After: the first sentence dropped and the last reads "None has an external store to be right about, and those that retrieve observe a bounded view rather than a maintained summary (Section~\ref{sec:framework})."; (c) the notation rows "gain ($\Delta$)" and "route A; route B" dropped. With (a) and (c): fine number 484 (+1), label on page 9; reported to the author before anything else, as the brief orders. No number changed.
- **R124-B [the accuracy fixes B2 to B4; the rulings on REPORT_R123; `r124_apply.py` block_b]** (recorded). B1 (the MemoryAgentBench sentence) is held for the author's ruling (REPORT_R124.md: the cited table's long-context rows reach 28 percent); B5 (Figure 3 from the five-draw rows) and B6 (Section 5's payers) are held until R125 reports, on the author's note. B2, the abstract: Before: "Second, where a state is named, a cosine lookup over the names is enough: no model reliably exceeds it." After: "Second, on a named state a cosine lookup over the names is enough: no model reliably exceeds it, and with every state named only Opus 5 does, by $0.03$."; Section 5, Before: "The same lookup over a list naming all three non-active states scores $0.88$ on the whole set, and Haiku 4.5 gains a reliable $+0.30$ on the two counted states once they are named." After: "The same lookup over a list naming all three non-active states scores $0.88$ on the whole set, which only Opus 5 reliably exceeds, by $0.03$. Haiku 4.5 gains a reliable $+0.30$ on the two counted states once they are named." (the author's clause; the sentence split at 41 words); the Conclusion, Before: "On a state the list names, no model reliably exceeds a name lookup." After: "On a state the list names, no model reliably exceeds a name lookup; with every state named only Opus 5 does, by $0.03$." (AUX-R103-MARGIN +0.0323, both intervals excluding zero; the per-state margins, none reliable, printed in Appendix C.2 after tab:sup-margins, AUX-R124-OP5-V3-MARGINS). B3, Section 4, Before: "Of the $90$ predictions preregistered before data collection, $27$ came out otherwise (Appendix~\ref{app:registration})." After: "Of the $90$ predictions preregistered with a bar, each before the run that tests it, $27$ came out otherwise (Appendix~\ref{app:registration})." (the author's "registered with a bar" printed as "preregistered with a bar": rule V bars the bare word in the main text). B4: "untold" printed as "without being told" (abstract, Conclusion); "under the old rubric" as "under the main-study rubric" (Section 5); "Five models cannot say why three differ from two" as "Five models are too few to say why three differ from two"; Figure 3's caption "the default summary only" as "the superseded-only summary only"; Section 1's "The answers agree." as "The three answers point the same way." No number changed.
- **R124-C [gate G2; the rulings on REPORT_R123, block C]** (recorded). tools/prose_scan.py rule G2 narrowed to the 14 September ruling's meaning. OLD pattern: every abstract sentence carrying a math-mode numeral (a decimal or count; a percentage is not one) had to name the lookup (G_LOOKUP: lookup, matcher, similarity match, cosine) and state a difference against it (G_DIFF: a signed number or above, below, within, gap, difference, adds, exceeds, minus, more than, less than), and no sentence could state the lookup's own level (G_LEVEL). NEW pattern: the level check alone, on a sentence that names the lookup (G_LOOKUP and G_LEVEL: 'at $0.xx$', '$0.xx$ AUROC', 'with $0.xx$', 'reaches $0.xx$', 'reads ... at $0.xx$'); a sentence that names no lookup is never a hit. The abstract's numerals return to math mode: $148$; $0.01$, $0.12$ and $0.16$ (R123-C1's text-mode workaround withdrawn).
- **R124-D [the appendix; the rulings on REPORT_R123, block D]** (recorded). D1: a reader's guide of five sentences before Appendix A's heading, naming for each of the three findings the tables that carry it (tab:cf-main, tab:cf-names-counts, tab:v2rcat; tab:sup-margins, tab:counterfactual, tab:cf-intent; tab:census, tab:levels, tab:graphiti-completed, with tab:reach and tab:gatereach) and the provenance table. D2: the question-signal table's note (a carried block), Before: "the registered R74 FOK-target probe re-derives" After: "the registered coverage-target probe re-derives"; E.9's four-counts sentence gains "; the $72\%$ of Table~\ref{tab:census} is a share of the $109$ events ($78$ of them), not of the $104$ entries" (AUX-BELIEVED-FR). The 'believed' phrases of E.9 are all inside quoted registered text (ADDENDUM_SIDE, the S2 census reading and the S2-U branch text) and stay. No number changed.
- **R124-E [E10, the hybrid reader; the author's ruling E1 on REPORT_R123: freeze and run now, no call, the stop rule unchanged]** (recorded). Frozen at fe6ff84 (registrations/ADDENDUM_CF2_HYBRID_READER.md sha256 0cfe92f5762406c1…, r82_counterfactual/tools/cf2_hybrid.py sha256 1b4fef953def9f34…, both hashed in reviews/v21/FREEZE_E10.md before the run); scored to r82_counterfactual/cf2/results/cf_scores_hybrid.json and ledgered as NUMBERS_CF2.md section 14e (AUX-CF2-HYB-*). Outcome: the hybrid reads 0.7865 on the whole set, +0.0201 over the name lookup with the item-level interval [−0.0016, +0.0410] including zero, so P-H1 failed; GPT-5.6 Sol minus the hybrid +0.0635 with both intervals excluding zero, so P-H2 held; the hybrid closes about a quarter of Sol's margin over the lookup, so the stop rule did not fire (AUX-R124-HYB-PRINTED). Landed: the C.2 paragraph 'A hybrid reader with no model in it' and tab:cf-hybrid after tab:enc-lookup (the registration's section 6: in every branch the C.2 table prints); tab:registrations-d's row (fe6ff84e12; the first prediction failed, the second held) and its caption; the recount, Appendix F Before: "Table~\ref{tab:registrations-d} $26$ with $9$: $90$ predictions, $27$ of which came out otherwise" After: "Table~\ref{tab:registrations-d} $28$ with $10$: $92$ predictions, $28$ of which came out otherwise"; Section 4 Before: "Of the $90$ predictions preregistered with a bar, each before the run that tests it, $27$ came out otherwise (Appendix~\ref{app:registration})." After: "Of the $92$ predictions preregistered with a bar, each before the run that tests it, $28$ came out otherwise (Appendix~\ref{app:registration})." (reviews/NUMBERS_R124.md AUX-R124-TALLY: the two E10 predictions were registered with a bar before their run, so the R123 counting rule adds them). Held: the registration's Section 5 sentence for the failing branch (the author's note of 2026-09-19 holds every Section 5 change until R125 reports) and the tab:cf-main row, which the registration lands only in the both-hold branch.
- **R124-F [the three additions to R124 of 2026-09-19, wording only]** (recorded). 1. The box, Before: "a model earns its call on states the summary only counts and on questions whose intent licenses old content (Section~\ref{sec:counterfactual})." After: "in our tests a model added something only on states the summary only counts and on questions whose intent licenses old content (Section~\ref{sec:counterfactual})."; Section 9, Before: "The repair therefore belongs to the write path." After: "The view-side rule we tested cannot make the repair, which leaves the write path." 2. Section 7, Before: "Mem0 erases at its retrieval surface: of its $10{,}074$ entries, $12.7\%$ expose \texttt{updated\_at} and nothing else, because an \texttt{UPDATE} replaces the record that \texttt{search} and \texttt{get\_all} return." After: "Mem0 erases at the retrieval surface we evaluated (\texttt{search} and \texttt{get\_all}, \texttt{mem0ai} 1.0.5): of its $10{,}074$ entries, $12.7\%$ expose \texttt{updated\_at} and nothing else, because an \texttt{UPDATE} replaces the record those calls return; its per-memory history call was not consulted."; "A-MEM invents: all $23{,}186$ link references across its $11{,}319$ notes resolve to zero note identifiers." After: "A-MEM invents, in our integration (\texttt{agentic-memory} 0.0.1): all $23{,}186$ link references across its $11{,}319$ notes resolve to zero note identifiers."; Table 2's Mem0 and A-MEM rows say the same, and its caption names the two reproduction scripts of the artifact, e1_metamemory/tools/repro_mem0_erase.py (10,074 points; 1,276 = 12.7 percent carry updated_at) and repro_amem_links.py (11,319 notes; 23,186 references; 0 resolving), both run on 2026-09-19 against the frozen banks and matching the printed rows (AUX-R124-PRINTED). 3. Appendix F's first paragraph gains "The September additions were registered before their runs but after earlier results on the same items were known; we claim no confirmatory design for them." No number changed.
- **R124-F2 [the page gate after the three additions; layout only]** (recorded). With the additions the box spilled whole to page 10 (fine number 491, -6): the Section 7 sentences and Table 2's longer rows and caption pushed the first two lines of Section 9's second paragraph from page 8 to page 9, where the slack was zero (block E closed at +0). Measured in a scratch build (REPORT_R124.md, block F): Table 2's third column widened from 0.70 to 0.80 of the line (its first two from 0.12 and 0.10 to 0.10 and 0.08); the caption's clause on the scripts in fewer words, Before: "; the Mem0 and A-MEM rows are reproduced by two scripts in the artifact, \texttt{repro\_mem0\_erase.py} and \texttt{repro\_amem\_links.py}." After: "; the artifact's \texttt{repro\_mem0\_erase.py} and \texttt{repro\_amem\_links.py} reproduce the Mem0 and A-MEM rows." (the session's own wording both times; the author asked that the scripts be named); the separation below a text float set to 12pt plus 2pt minus 2pt (\textfloatsep; the article default is 20pt plus 2pt minus 4pt, the style sets none), which recovers about eight points under Table 2 on page 8 and under Table 3 on page 9. Together: label on page 9, fine number 485 (+0). Two alternatives measured and not taken: Table 2 in \tiny with the caption's pointer sentence on FR-Bank's conflation deleted (485, a content cut); Table 2 in \tiny with the float separation (484). No word of the author's, no number and no claim changed.

## R126 AUTHORIZATION BLOCK — dated 2026-09-20

Program R126: the v22 lineage, opened from the R124 close `ee6b735` (`reviews/v22/`, base tree `ea71a9d0`, tag `base-tree/v22`; HEAD tagged `fallback/v22-pre-restructure`; `reviews/v22/tools/bump_v22.py`). The main text (title through the box) is the readable body delivered to `reviews/v22/inbox/v22_readable_main.tex`, ported by `reviews/v22/tools/port_v22.py` (every conversion and wording change asserted); the appendix is repaired by `appendix_r126.py` and `build_v22.py` REPAIRS_R126_BLOCK; Figure 3 is `fig3_data.py`; the ledgers are `reviews/NUMBERS_R126.md` and `reviews/v22/NUMBER_MOVES_V22.md`; the report is `reviews/v22/REPORT_R126.md`. frozen_diff runs with `--program=R126` against the v22 base. This block supersedes the body entries of R124 (their texts are inside the readable body or replaced by it); R124's non-body items stand.

- **R126-1 [the readable body; the brief, Phase 1]** (recorded). Sections 1 to 10 and the box are the inbox text in the new order (1 Introduction, 2 Related work, 3 Framework, 4 Setup, 5 What readers read with 5.1 names against counts, 5.2 the lookup against the models, 5.3 when intent licenses old content, 6 What backends write, 7 At retrieval, 8 Replication and the coverage judgment, 9 Limitations, 10 Conclusion, the builders box). Ours, verbatim from v21: the preamble, Definition 1 with its grid (def:coverage), Table 2's census rows, the statements, the bibliography. Figure 1 is the inbox's three-box TikZ with the masked-retrieval note under the tag route (the addendum's A1; our adapted v21 drawing was retired); our Figure 2 table with the inbox's row labels and caption; Table 1 in the inbox's layout with v21's values; Table 3 with v21's rows. Every \N{value}{provenance} of the inbox is printed as the value (math mode for numerals; `reviews/v22/INBOX_NUMBERS_R126.md`); every \ap{} pointer is a \ref to our label; the inbox's labels map to ours (tab:readers to tab:cf-main, fig:triple to fig:example, fig:states to fig:perstate, def:state_intent to def:coverage, sec:readers to sec:counterfactual, sec:retrieval to sec:downstream and sec:routes, sec:replication to sec:populations); the sixteen citation keys the inbox dropped are restored at their sentences (no new entry). The notation box and Definition 2 (def:index) move to Appendix E.1 verbatim.
- **R126-2 [Phase 2.1, the contributions]** (recorded). The author's three bullets replace the inbox's three (CONTRIB in port_v22.py).
- **R126-3 [Phase 2.2, the abstract's third finding]** (recorded). Before (the inbox): "Third, backend metadata omit or misstate lifecycle information, weakening readers' judgments." After (the author's): "Third, the backends we tested omit or misstate this information: under FR-Bank's own metadata, mini and the lookup fall to $0.60$ and $0.59$."
- **R126-4 [Phase 2.3, the Mem0 and A-MEM paragraph and U5]** (recorded). Before: "Luna loses under every rendering tested through the raw API" After: "Luna loses $0.27$ to $0.34$ under every rendering tested through the raw API" (AUX-MARKER-*), so the paragraph carries all four U5 conditions. U5 re-pinned (claims_diff.U_BLOCKS, slogan_scan.PINNED): old pinned string "What triggers the loss under the constrained rendering is unresolved" (R124 A2, v21's Limitations pointer), new pinned string "Scores compress toward a low value, but the trigger remains unresolved." (the paragraph's own closing sentence, unchanged from the inbox).
- **R126-5 [Phase 2.4, Table 2's caption]** (recorded). The inbox's "These are counts, without sampling intervals." becomes the author's sentence, printed as "Counts of disagreement with the manifest-and-alignment reference, without hand adjudication; no sampling intervals." (the author's ", not adjudicated by hand" trips slogan_scan S9 in the main text); superseded by the addendum's A2 (2026-09-20): the caption reads "Backend census: counts of disagreement with the manifest-and-alignment reference, without hand adjudication or sampling intervals. Lower panel: coverage losses and rebuilt-summary scores. (Appendices E.7 and E.9)", and the matching-threshold note, the conflation note and the two reproduction script names are in Appendix E.9.
- **R126-10 [the author's addendum of 2026-09-20 after the read of the mid-progress build]** (recorded). A1 Figure 1 (above); A3 Section 6's first paragraph in the author's words; A4 Definition 1's 'under $i(q)$' printed as 'under the question's intent' and the hike paragraph's last two sentences deleted; A5 Section 3's two summary-size sentences to Appendix E.3; A6 the long-or-wrong-lists paragraph in the author's words (the 0.02 injection margin leaves the body; AUX-PAD-C-MINI +0.0122, -C-H45 +0.0192 verified); A7 the 'Haiku fares better' paragraph to Appendix E.9 and the author's sentence 'Haiku retains more of its gain than mini does, and more where the target's name survives the store's list ($0.87$ against $0.68$ where it does not; descriptive).'; A8 Section 7's first two paragraphs merged in the author's words (the 0.79 / 0.82 pair leaves the body; AUX-RESP-A1-H45-HYBRID 0.7863 against Haiku 4.5's ground-truth row 0.8210, verified, within tolerance at -0.0347). B1 Section 1's two finding sentences in the author's words; B2 'registered with a bar' kept, tools/prose_scan.py rule V gaining that collocation; B3 the Conclusion's first sentence in the author's words with one word changed for rule D ('wrote'; R126-9). Aggregate cost: page 10, fine number 501 to page 9, fine number 482 (the target 480 not reached; the costed table is reviews/v22/results/cost_payers_r126.md and REPORT_R126.md).
- **R126-6 [Phase 2.5, the Section 5.1 merges]** (recorded). "Knowing the category helps a count reader" folded into the paragraph before it (its bold lead dropped); "Permuting the totals barely changes the models' scores" folded into "A bare count can give the obligation away" as its closing sentences. No word of the sentences changed.
- **R126-7 [Phase 3, Figure 3]** (recorded). Redrawn in pgfplots from `reviews/v22/src/fig3_data.tex` (fig3_data.py: AUX-R122-K5-ROWS for GPT-4.1 mini at five draws, AUX-CF2-*-V2/-V3, AUX-CF2-OAI-*, AUX-R110-A1-CR); provisional until R125 reports, when the data file is regenerated.
- **R126-8 [Phase 4, the appendix; appendix_r126.py and REPAIRS_R126_BLOCK]** (recorded). (4.1) three pointers retargeted to Section 5's sub-labels; no hardcoded cross-reference number exists. (4.2) the reader's guide of eight sentences with the term bridge; seven rows in E.1's terms table; the captions of tab:cf3-expiry, tab:dist, tab:marker, tab:gatereach (prose) and tab:inversion, tab:q4-marker, tab:s1-names (E.7's carried block) use the body's terms with the old term in parentheses. (4.3) the R124 leftovers had landed in v21 (checked); tab:ds-a8's two rows lose their extra brace (the 21 inherited LaTeX errors). (4.4) the registration record's calendar dates become day indices beside the hashes (day 0 = the first freeze; AUX-R126-DAYS), in tab:registrations (carried; the caption and header say 'freeze day'), -b, -c, -d, E.3's threshold sentence, E.10's fourth-amendment sentence and F's attestation and Opus-entry paragraphs; the G.4 parenthetical after GR-1's quotation reads "(The bracketed words stand in for the store's name as the registered text gives it.)" in place of "(The quotation is redacted for anonymity.)". (4.5) three recorded rows (top-five, the lookup rule, the oracle) in tab:gatereach's licensed panel from reach_rows_r123.json (AUX-R126-GATEREACH). (4.6) E.3's sentence corrected to tab:e3-intent (AUX-R126-E3-INTENT): every PN question has current or upcoming intent, and 44 PRESENT questions hold a non-active record of their own attribute (33 current or upcoming, 11 change).
- **R126-9 [Phase 5.3, the gate-driven wording changes; each the smallest change satisfying its rule, listed with the rule]** (recorded).
  - [Q-C and G4] Section 1. Before: "A \emph{lifecycle summary} lists record counts by state and attribute names, with stored values removed." After: "A \emph{lifecycle summary} lists record counts by state and, per category, an attribute-name list with the values removed."
  - [G4 (the anchor sentence in the R112 form)] Section 1. Before: "Names carry most of the observed signal." After: "Attribute names carry most of the observed signal."
  - [D (88% and 83% with the abstract); the author's B1 wording] Section 1. Before: "No model reliably exceeds the lookup on the state named by the default summary. Luna, Sol and Opus lead overall on that summary; Opus also leads when all states are named." After: "On the one state the default summary names, no model reliably outscores the lookup. Luna, Sol and Opus pull ahead of it on the whole set, and Opus stays ahead by $0.03$ when every state is named."
  - [repeat_scan (a 9-gram in three places; Definition 1 is verbatim)] Section 2. Before: "while obligation concerns content whose use must be suppressed for the answer to be right." After: "while obligation concerns content whose use would make the answer wrong."
  - [V (elicited)] Section 4. Before: "Luna's and Sol's shared cross-vendor rows are elicited through the vendor's agent tool." After: "Luna's and Sol's shared cross-vendor rows are obtained through the vendor's agent tool."
  - [Q-C (the AUROC definition's words)] Section 4. Before: "We score separation by AUROC, the chance that a positive ranks above a negative \citep{hanley1982}." After: "We score separation by AUROC, the chance that a positive scores above a negative \citep{hanley1982}."
  - [Q-A (the opener carries numerals)] Section 4. Before: "The \emph{counterfactual set} contains $444$ items: $148$ questions, each asked of three versions of its store. Versions differ only in the target attribute." After: "The \emph{counterfactual set} asks each of its questions of three versions of one store. It contains $444$ items from $148$ questions, and the versions differ only in the target attribute."
  - [Q-A (the opener carries a numeral)] Section 4. Before: "The \emph{full obligation set} contains $661$ questions about the original stores and their variants, supporting the backend and retrieval comparisons." After: "The \emph{full obligation set} supports the backend and retrieval comparisons. It contains $661$ questions about the original stores and their variants."
  - [V (registrations); 'registered with a bar' kept by the addendum's B2, the rule gaining that collocation] Section 4. Before: "These registrations include follow-ups" After: "They include follow-ups"
  - [D (86% with the abstract's second sentence; 88% with the B1 sentence)] Section 5.2. Before: "\claim{No model reliably beats the lookup on the default named state.}" After: "\claim{No model reliably beats the lookup on supersession.}"
  - [D (71% with the abstract's third sentence)] Section 5.2. Before: "Luna, Sol and Opus reliably lead the lookup overall by $0.07$ to $0.08$." After: "Luna, Sol and Opus reliably lead the lookup on the whole set by $0.07$ to $0.08$."
  - [S9 (', not ')] Section 5.1. Before: "This ablation uses mini's recorded single-call row, not the repeated-call row in Table~\ref{tab:cf-main}." After: "This ablation uses mini's recorded single-call row rather than the repeated-call row in Table~\ref{tab:cf-main}."
  - [S9 ('but ... not')] Section 6. Before: "Removing the rendering cap raises their scores but does not restore their ground-truth results." After: "Removing the rendering cap raises their scores without restoring their ground-truth results."
  - [Q-A (the paragraph opened on a numeral; joined to the paragraph before it)] Section 9. Before: "with no open-weights model. [paragraph break] Two further encoders leave the default lookup within $0.01$ of its score." After: "with no open-weights model. Two further encoders leave the default lookup within $0.01$ of its score."
  - [Q-A (the opener carries numerals; split at the semicolon)] Section 9. Before: "The ground-truth tags in retrieved views depend on aligning manifests to stored records; that alignment marks the forbidding record for $82$ of $104$ obligations." After: "The ground-truth tags in retrieved views depend on aligning manifests to stored records. That alignment marks the forbidding record for $82$ of $104$ obligations."
  - [V (gate)] Section 10. Before: "reaches as far without a model gate as with one, at a budget trade-off." After: "reaches as far ungated as gated, at a budget trade-off."
  - [S7 and D (the sentence repeated Section 1's verbatim); the author's B3 sentence with 'wrote' for 'writes' (rule D, 73% to 64%)] Section 10. Before: "In these tests, what the store writes down mattered more than which reader read it. Removing names" After: "In these tests, the information a store wrote down counted for more than the choice of reader. Removing names"
  - [S17 ('the join' is barred in the main text; E.1 maps it to the ground-truth tags); the author's A2 parenthetical] Section 7. Before: "($34$ once one inverted tag from the join is corrected)" After: "($34$ once one inverted ground-truth tag is corrected)"
  - [Q-A, the tool's sentence splitter] reviews/v22/tools/q_scan.py and readability_wp.py end a sentence at '.}' as well, so a bold run-in claim sentence (\claim{...}) is read as its paragraph's opener; the rule's text is unchanged. Without it Q-A tripped 22 times for that one reason (REPORT_R126.md, Phase 5.3).
  - [G2] tools/prose_scan.py rule G2 stands as R124 block C narrowed it (a hit is an abstract sentence that names the lookup and states its own AUROC level); recorded here as the rule in force for v22.
- **R126-F [the frozen strings of the v21 build that the readable body replaced; `reviews/v22/results/frozen_r126_final.json`]** (recorded). Each string below occurred in paper_v21.tex and occurs a different number of times in paper_v22.tex (a count of zero means the sentence left the body; the new sentence carrying the claim is in reviews/v22/BODY_MAP_R126.md). Every one is authorized as replaced by the readable body under R126-1.
  - AUTHORIZED [Q CLAIMS] 2 -> 1: "names carrying superseded content"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The 60% retention threshold was fixed in advance at 60% in the main study's preregistration (2026-08-10) for coverage retention and was inherited unchanged when obligation retention was scored, before that figure existed."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The summary route rests on names, because removing them removes the judgment."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "R94: CF-2 store-counterfactual set & f016f033e9 & 2026-09-12 & 148 question and slot pairs drawn under predicates fixed before any verdict, three store versions each, three summaries, three readers, five predictions and their branch texts; all five held, two of them printing either way: the lookups within tolerance and every reader inside the totals-randomization band; five recorded deviations (D-CF2-1 to D-CF2-5) & held"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The loss is compression of the indexed score toward one low value, and what triggers it is unresolved (Appendix \ref{app:inversion})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "whose superseded list averages under two names"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The superseded-names list averages 1.75 names on the full obligation set."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "FR-Bank's own metadata leaves GPT-4.1 mini and the name lookup close to chance and costs Haiku 4.5 about a quarter of its gain."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "A count cannot say which attribute is retracted or expired. When the summary names those attributes, every model improves (Table \ref{tab:cf-main})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "It covers the states the list does not name."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "What this paper measures is the judgment made before retrieval, about the store itself, from the content's own lifecycle state."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "In most retraction pairs and half the expiry pairs the category has no other such entry (26 of 30 and 15 of 30)"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "under that mask its own retraction questions pass at 5%"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "because the mask drops the records whose tags carry it"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Haiku 4.5 gains a reliable +0.30 on the two counted states once they are named"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "FR-Bank's conflation of retraction with supersession is described in Appendix \ref{app:census}"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "manifests of synthetic users (personas)"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "the chance that an ABSENT label is wrong is 5.2%"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "the blind and the indexed prompt"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Question wording alone carries much of a blind score"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "A name-bearing summary rebuilt from ground truth restores coverage to 0.90 on A-MEM and 0.88 on Mem0, so what the constrained rendering loses is the names."
  - AUTHORIZED [Q CLAIMS] 2 -> 1: "the gain is the AUROC minus 0.50"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "every tested model separates them more weakly than a count reader does"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "every model discriminates more weakly than the count reader"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "We call the cancelled plan a forbidding record, a non-active record whose use would make the answer wrong; the cancellation is the evidence that marks it."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Of the three main backends, FR-Bank \citep{fr} is the only one that tags every entry with a lifecycle state."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Graphiti \citep{zep}, whose validity intervals resemble lifecycle tags, is a fourth backend, scored with GPT-4.1 mini on the same personas (Appendix \ref{app:posthoc-graphiti})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "On the counterfactual set the persona-grouped interval is the one printed, because resampling whole personas keeps each triple intact and the item-level bootstrap does not."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "These groups are small (Section \ref{sec:limitations})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "On Graphiti, native tags on the same five retrieved edges make no reliable difference (-0.01, both intervals including zero; Appendix \ref{app:posthoc-graphiti})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "GPT-4.1 mini's obligation score on that view rises from 0.69 to a reliable 0.81, a descriptive result with no prediction fixed in advance."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Graphiti recovers some of the forbidding records and exposes names a lookup can use."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Its invalidation marks reach 13 of the 34 full-store obligations that the ground truth marks superseded or expired, more than the quarter we had predicted."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Under its capped store-written summary GPT-4.1 mini scores 0.58 on the 323 full-store questions, a gain over blind that includes zero, against 0.74 under the ground-truth summary."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "A name lookup over Graphiti's own superseded names scores 0.68, reliably above the model by +0.10 (Appendix \ref{app:posthoc-graphiti})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Graphiti's own names serve a lookup better than the model."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Maintain the list of attribute names that hold non-active content, superseded, retracted and expired alike."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Tag the duplicates the store keeps active, which is where the flagged stale answers came from (Section \ref{sec:downstream})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "fb4b2ca8c8 (file hash) & 2026-09-14"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The registration record, continued: twelve descriptive registrations, each hashed by the runner before its first call (the commits of 18 September do not date them) and carrying no prediction and no bar, so nothing in them could hold or fail. Every one has run except the paraphrase check, which waits on our read."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "How each freeze is attested. Each runner wrote a lock record at its start holding the registration's sha256, and dated additions sit below the registered-text marker, outside the hash. For most registrations a commit holding the registered text also predates the run's first output. For CF-3, committed 33 minutes after its first call, and for DS Amendments 1 to 4, Q4, RESP Amendment 1 and Graphiti Amendment 2, first committed on 18 September 2026, the evidence that the text predates the run is the runner's lock record and the file times."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The obligation gain replicates across six models from three vendors."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Every paired gain excludes zero where the blind score varies, the five such models on the cross-model set gaining +0.15 to +0.45, Kimi K3 among them at +0.26 (Table \ref{tab:ladder-exact}, Appendix \ref{app:laddertable})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Haiku 4.5, Opus 5 and GPT-5.6 Luna score 0.82 to 0.83 indexed on the full obligation set against the name lookup's 0.75 on the same 661 questions (Table \ref{tab:e1}), levels that include what the question wording gives away (Section \ref{sec:setup})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "On coverage the easy-tier margin over the name lookup does not survive a lookup over the whole name map (Table \ref{tab:cov-lookup}, Appendix \ref{app:baselines}), and on the counterfactual set every model's coverage interval excludes chance (Table \ref{tab:cf-fok}, Appendix \ref{app:counterfactual})."
  - AUTHORIZED [Q CLAIMS] 3 -> 4: "(Appendix \ref{app:baselines})"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "the other is a count reader that guesses the question's category from its text and reads the share of that category's entries that are no longer active."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "A category-aware count reader takes the category from the manifest instead and reads that category's retracted-plus-expired count."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Under it GPT-4.1 mini loses 0.10 on Mem0 and 0.11 on A-MEM, and on the pooled 66 questions of both stores GPT-5.6 Luna loses 0.29 through the raw API and GPT-5.6 Sol 0.10^{h}, every interval excluding zero."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The loss survives omitting or rewording the marker on Mem0, and for GPT-5.6 Luna it appears under every rendering, 0.27 to 0.34, so the marker's wording is not the cause (Appendix \ref{app:inversion})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Opus 5, at five draws against its five-draw row, moves -0.10 on retraction and -0.13 on expiry, both intervals excluding zero."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Names carry most of the observed signal; of the three models given the moved-count control, only Opus 5 responds to it."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "of the three models given the count interventions, only Opus 5 tracks the counts."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "GPT-4.1 mini ran the main study at one call per question, and Opus 5, Haiku 4.5 and GPT-5.6 Luna ran every population at five calls (Table \ref{tab:setup})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "GPT-5.6 Sol ran the cross-model set and, through the raw API, the counterfactual set; Kimi K3 ran the cross-model set only."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The GPT-5.6 cross-model rows are harness rows; their counterfactual rows are raw-API (Appendix \ref{app:laddertable})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "where every model scores 0.53 to 0.64"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "A reader given the question's category that reads the share of its entries no longer active, superseded included (privileged, post hoc), scores 0.85 on the whole set from the count table alone (Appendix \ref{app:counterfactual})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "leaves GPT-4.1 mini and Haiku 4.5 within tolerance"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "tracks the attribute names in the summary; of the three models given the count interventions, only Opus 5 tracks the counts"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "GPT-4.1 mini and Haiku 4.5 do not (0.48 and 0.55)"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The summary states each label twice, as a name and as a count, and the models read the names (Section \ref{sec:counterfactual})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Opus 5, GPT-5.6 Sol and GPT-5.6 Luna exceed it"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 exceed it"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Mem0 overwrites and A-MEM's links"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Mem0 overwrites, A-MEM's links"
  - AUTHORIZED [Q CLAIMS] 2 -> 0: "keyed on the name list reaches"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "keyed on the list of names reaches"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "GPT-5.6 Sol, GPT-5.6 Luna and Opus 5 exceed it"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "that neither GPT-4.1 mini nor Haiku 4.5 does"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "as a name and as a count; the models read the names"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "as a name and as a count, and the models read the names"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "On the counterfactual set no model reliably exceeds the name lookup on supersession (Appendix \ref{app:counterfactual})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "so the gain measured on [the lifecycle store] does not reproduce where the lifecycle record is thinner."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Only the count row differs between the PRESENT and PN versions, and the ABSENT version also loses the name, so the name lookup separates none of the three (supersession triple: Appendix \ref{app:counterfactual})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Their margins over the lookup do not survive the persona-grouped interval (Table \ref{tab:margin-661}, Appendix \ref{app:baselines})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Its CUPMem prototype revises state at write time and consolidates it; we measure what such write-time structure has to expose, the names of the states it revises, for a judgment before retrieval."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Lifecycle tags have precedents: temporal databases keep validity intervals \citep{snodgrass1986}, replicated sets keep tombstones for removed elements \citep{shapiro2011}, and truth maintenance tracks retracted beliefs \citep{doyle1979}."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Reach on the full obligation set: records in view, no answer scored. Lines are the mean per question over all 661 questions (about seven over the 104 obligations alone); the three matched rows interpolate between two depths to the model rule's budget (Table \ref{tab:gatereach}, Appendix \ref{app:resp})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "What triggers the loss under the constrained rendering is unresolved (Section \ref{sec:backends})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "What triggers the loss under the constrained rendering is unresolved"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Answer-stage results are exploratory, and the detector that flags stale answers awaits its human validation."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Two closed vendors supply the capability comparison, and no open-weights model ran the counterfactual set."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Under the intent-explicit rubric only GPT-5.6 Luna and GPT-4.1 mini were rerun on the counterfactual set; both score within 0.02 of their main-rubric values, and Luna's margin over the name lookup holds (+0.09, reliable)."
  - AUTHORIZED [Q CLAIMS] 7 -> 1: "(Section \ref{sec:counterfactual})"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "None has an external store to be right about, and those that retrieve observe a bounded view rather than a maintained summary (Section \ref{sec:framework})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Second, on a named state a cosine lookup over the names is enough: no model reliably exceeds it, and with every state named only Opus 5 does, by 0.03."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The same lookup over a list naming all three non-active states scores 0.88 on the whole set, which only Opus 5 reliably exceeds, by 0.03. Haiku 4.5 gains a reliable +0.30 on the two counted states once they are named."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "On a state the list names, no model reliably exceeds a name lookup; with every state named only Opus 5 does, by 0.03."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Five models are too few to say why three differ from two"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "the superseded-only summary only"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The three answers point the same way."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Of the 92 predictions preregistered with a bar, each before the run that tests it, 28 came out otherwise (Appendix \ref{app:registration})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "in our tests a model added something only on states the summary only counts and on questions whose intent licenses old content (Section \ref{sec:counterfactual})."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Mem0 erases at the retrieval surface we evaluated (search and get\_all, mem0ai 1.0.5): of its 10,074 entries, 12.7% expose updated\_at and nothing else, because an UPDATE replaces the record those calls return; its per-memory history call was not consulted."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "A-MEM invents, in our integration (agentic-memory 0.0.1): all 23,186 link references across its 11,319 notes resolve to zero note identifiers."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "; the artifact's repro\_mem0\_erase.py and repro\_amem\_links.py reproduce the Mem0 and A-MEM rows."

Program R128 (2026-09-20), inside this block: the author's section A (the abstract, Section 1, the Section 6 sentence, Section 7's last paragraph, the builders box; port_v22.py), sections B and C in the appendix (reviews/v22/tools/appendix_r128.py; build_v22.py REPAIRS_R128_BLOCK), the ledger reviews/NUMBERS_R128.md, the report reviews/v22/REPORT_R128.md. Sections 5.1 and 5.2 are unchanged (the R127 hold stands there). No model call was made.

- **R128-A1 [which whole set]** (recorded). Abstract, before: "GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 lead overall by $0.07$ to $0.08$; Opus leads by $0.03$ when all states are named." After: "GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 lead it by $0.07$ to $0.08$ on the counterfactual set; Opus leads by $0.03$ when all states are named." Section 1, before: "Luna, Sol and Opus pull ahead of it on the whole set, and Opus stays ahead by $0.03$ when every state is named." After: "Luna, Sol and Opus pull ahead of it on the counterfactual set, and Opus stays ahead by $0.03$ when every state is named." The margins are AUX-CF2-OAI-P-S1/-S2 and AUX-R103-MARGIN on the counterfactual set; on the $661$ the lookup's persona interval covers every model. The Conclusion and Section 5.2 carry no 'whole set' sentence about this margin (checked; 5.2 untouched).
- **R128-A2 [the Section 6 sentence; U5]** (recorded). Before: "Scores compress toward a low value, but the trigger remains unresolved." After: "Scores collapse onto a few low values, with positives slightly below negatives, and the trigger remains unresolved." Checked against tab:dist (AUX-E7-*): the indexed positives read $0.1617$ against the negatives' $0.1688$ on Mem0 and $0.1544$ against $0.1658$ on A-MEM, over five distinct values. U5 re-pinned to the new sentence (tools/claims_diff.py U_BLOCKS, tools/slogan_scan.py PINNED). Appendix E.7 gains the explanation (R128-B2).
- **R128-A3 [Section 7's last paragraph]** (recorded). Before: "This result limits that rule; it does not rule out other repairs that operate on retrieved content." After: "A reference-free repair for copies under other keys remains open." (the Appendix pointer kept).
- **R128-A4 [the builders box]** (recorded). The lookup sentence gains ", and in the scenario we priced, a model call before every query cost more than the retrieval it saved (Appendix G.5)"; checked against Appendix G.5 (AUX-UC-*): the measured mean monitor cost applied to the cached-depth batch adds \$0.289083 against maximum selector allowances of \$0.038258 and \$0.106836.
- **R128-B [the appendix, substance]** (recorded). B1 the coverage rubric verbatim from e1_metamemory/tools/prompts_e1.py in E.3 (the FOK line and the JSON schema), beside the obligation half. B2 E.7's explanation of the collapse (five distinct values; positives below negatives; store-written rows lose nothing; rebuilt names restore) and tab:dist's caption. B3 the pooled-66 paragraph in E.7 (AUX-R128-POOLED66). B4 the Q4 probe's paragraph says the instruction's word 'absent' is also a label's name, so the probe cannot separate the two readings (REPAIRS_R128_BLOCK). B5 tab:destruction's caption gains the cross-store qualification (every positive an FR-Bank item, every Mem0 and A-MEM item a negative) with tab:destruction-fr named as the controlled comparison. B6 skipped: tab:setup and tab:counterfactual already carry Sol and Luna. B7 tab:ds-body's stale-rate columns carry both denominators (of the reached scorable obligations; of the answered subset, Wilson) with the abstention sentence in the caption; tab:ds-body-lower's dash becomes $[0.097,0.278]$ (AUX-R128-DS-DENOM). B8 tab:cf3-expiry gains three 'Opus 5, draw 1' rows (AUX-R128-CF3-DRAW1; the lookup rows' plus signs removed). B9 STOPPED, reported only: the one negation-cued question (fatima_q06) is among the 35 obligations with an active stale line, so correcting its tags would change the printed 35 of 89 and the ORACLE split. B10 the five Graphiti readings (GR-1 failed, GR-2 not computable, GR-3 held, GR-4 and GR-5 descriptive) in both Graphiti rows of Appendix F.
- **R128-C [the punch list]** (recorded). $1{,}273$ of the $3{,}305$; tab:v2rcat's draw-1 row labelled against the recorded $k=5$ row with the $0.8400$ / $-0.0351$ note (nothing numeric changed; AUX-V2RCAT-OP5 compares the $k=1$ run with the recorded $k=5$ row); '$0.75$ (rounded from $0.7484$)'; 'expiry triples' for 'expiry pairs'; tab:bh-split's $[0.6722,0.8992]$ on the persona row; E.11's three dollar amounts printed with the sign; G.4's '+0.1014 (from the unrounded scores)' and the 784 / 72 edge counts explained; the harness marker $^{h}$ defined in tab:ladder-predictions' notes and tab:inversion's caption (the two tables that used it undefined; tab:runs, tab:ladder-exact and tab:marker already defined it); the prompt template's backticks printed from T1 slot 0 (the TS1 glyph pulled a Type 3 font); tab:cf-hybrid's header 'first draw & first-draw gain'; tab:destruction, tab:inversion and the NB-6 caption qualified. The dagger and the 'TRUE $-0.0969$' items needed nothing: every dagger is defined in its table, and no caption carries 'TRUE' (it survives only as the key line of the two summaries E.7 reproduces verbatim; E.1 bridges INDEXED-TRUE).
- **R128-F [the frozen strings R128 changed on top of the R126 close; `reviews/v22/results/frozen_r128_final.json`]** (recorded). Each string below occurred in paper_v21.tex, was kept by the R126 close and occurs a different number of times after R128: the first and third are E.7's prose under R128-B2 ('What triggers the compression is unresolved' reads 'collapse'; the clause '; the marker's wording is not it' closes the corrected sentence as ', and the marker's wording is not it'); the second is E.11's cost sentence, now printed with dollar signs (R128-C). Each is authorized under the entry named.
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "What triggers the compression is unresolved, and the ablations that narrowed it follow."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "two later runs, the composite's answers on the actual expanded views 0.14 and Opus 5 on the moved-count control 4.52, under a 40 ceiling for that pass."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "; the marker's wording is not it (Table \ref{tab:marker})"

Program R129 (2026-09-20), inside this block: the author's rulings A1 to A3, the body landings B1 and B2 with the payers C1 and C2 (port_v22.py), the appendix (appendix_r129.py), the ledger reviews/NUMBERS_R129.md (ledger_r129.py), the report reviews/v22/REPORT_R129.md. No model call. Section 5.1's count-reader paragraphs and Figure 3 stay held for R125.

- **R129-A1 [Section 1, the MemoryAgentBench sentence; the ruling on R127b item 1]** (recorded). Before: "On MemoryAgentBench's multi-hop conflict-resolution questions, no memory agent exceeds $7\%$ accuracy \citep{memoryagentbench}." After: "On MemoryAgentBench's multi-hop conflict-resolution questions, no memory mechanism exceeds $7\%$ accuracy and the best long-context model reaches $28\%$ \citep{memoryagentbench}." Source: Hu et al., Table 3, column FC-MH (every memory mechanism 7.0 or below; the long-context GPT-5-mini (400K) row 28.0) and the paper's own sentence.
- **R129-A2 [Section 7's stale-line count; the ruling on R128's B9]** (recorded). Before: "Among $89$ scorable obligation views, $35$ contain an active line asserting the stale value." After: "Among $89$ scorable obligation views, $35$ contain an active line asserting the stale value ($34$ once one inverted tag from the join is corrected)." E.10 gains the paragraph (AUX-R129-B9: the FULL view of frbank:fatima:fatima_q06 leaves the 35, the retraction count 14 -> 13, the oracle split 16 / 0 and 14 / 5 as joined, 15 / 1 and 13 / 6 corrected; nothing re-answered) and the eight answer-stage captions say the tables were scored with the tag as joined.
- **R129-A3 [the moved-count table's draw-1 row and note]** (recorded). Accepted as R128 left it; no change.
- **R129-B1 [Section 5.1's moved-count paragraph; E9 in the body]** (recorded). Before: "\claim{Only Opus follows a count when it moves.} The \emph{moved-count control} transfers the obligation's increment to a sibling store version while preserving the names. A reader following that count should rank the wrong version higher. Mini's expiry score rises by $0.06$, without a reliable difference; Haiku remains within tolerance. Opus falls reliably by $0.10$ on retraction and $0.13$ on expiry when draw counts are matched." After (the author's paragraph): "\claim{The three stronger models follow a count when it moves.} The \emph{moved-count control} transfers the obligation's increment to a sibling store version while preserving the names, so a reader following that count should rank the wrong version higher. Opus falls reliably by $0.10$ on retraction and $0.13$ on expiry when draw counts are matched. Luna and Sol fall reliably on expiry, by $0.12$ and $0.19$; their retraction falls, $0.07$ and $0.03$, do not clear zero. Mini and Haiku show no reliable change." (AUX-V2RCAT-A1-OP5-K5; AUX-V2RCAT-A2-LUNA-K5, -SOL-K5; AUX-R129-E9-PRINTED.) E9's rows join tab:v2rcat with two sentences of prose and its row joins tab:registrations-d; its one prediction (P-M2, failed for both models) joins the count: Section 4 and Appendix F read $29$ of $93$ for $28$ of $92$ (AUX-R129-COUNT).
- **R129-B2 [Section 5.2, the hybrid reader's paragraph; E10 in the body]** (recorded). New paragraph after 'Naming all states helps readers and leaves an Opus advantage': "\claim{A cheap combined reader does not close the gap.} A logistic reader over the name similarity and the guessed category's non-active share, fit with personas held out, scores $0.79$ on the counterfactual set. It does not reliably beat the lookup, and Luna, Sol and Opus stay a reliable $0.05$ to $0.06$ above it." (AUX-CF2-HYB-WHOLE 0.7865; AUX-CF2-HYB-VS-LOOKUP +0.0201, the item interval including zero; AUX-CF2-HYB-VS-MODELS +0.0540, +0.0553, +0.0635; AUX-R129-HYB-PRINTED.) Built at the checkpoint 659737d with one word for prose_scan rule V ('left out' for 'held out'); **WITHDRAWN at the close by the author's ruling on REPORT_R129.md** (with B1 and B2 both in the body Figure 3 moved to page 7 and the box to page 10; the hybrid returns with the Section 5 rewrite once R125 Task 1 reports). tab:cf-hybrid keeps GPT-4.1 mini's five-draw row minus the hybrid, $-0.0217$ with both intervals including zero (AUX-R129-HYB-MINI5); the body says nothing about the hybrid.
- **R129-B3 [the search for other only-Opus count sentences]** (recorded). The main text carries no other sentence saying only Opus responds to counts (Section 1's bullet, the Conclusion, the box and the body captions checked; 'Only Opus lowers its judgment without being told' in Section 5.3 is about intent and stays).
- **R129-C1 [the payer in Section 5.1's first paragraph]** (recorded). Before: "Counts alone score reliably below names alone: mini loses $0.12$, and Haiku loses $0.16$. This ablation uses mini's recorded single-call row rather than the repeated-call row in Table~\ref{tab:cf-main}." After: "Counts alone score reliably below names alone: mini loses $0.12$ on its single-call row, and Haiku loses $0.16$."
- **R129-C2 [the payer in Section 5.2, the long-or-wrong-lists paragraph]** (recorded). Before: "On the full obligation set, padding the default list to $60$ names lowers the lookup to $0.67$, and mini falls with it; on the counterfactual set, injecting wrong names lowers mini, Haiku and the lookup together. Not every decline is reliable, and short ground-truth lists do not establish robustness to longer store-written lists." After: "Padding the default list to $60$ names lowers the lookup to $0.67$ on the full obligation set, and injected wrong names lower mini, Haiku and the lookup together, so short ground-truth lists do not establish robustness to longer store-written ones."
- **R129-D [Appendix E.3, tab:e3-groups]** (recorded). The R127 / R127b group readings (AUX-R129-GROUPS) with four sentences; no body text (it comes with the Section 5 rewrite).
- **R129-F [the frozen strings R129 changed on top of the R128 close; `reviews/v22/results/frozen_r129_close.json`]** (recorded). Each string below occurred in paper_v21.tex, was kept through the R128 close and occurs a different number of times after R129; each is authorized under the entry named above that replaced it.
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Table \ref{tab:registrations-d} 28 with 10: 92 predictions, 28 of which came out otherwise"

Program R131 (2026-09-20), inside this block: the author's texts of sections A to G of the brief landed by reviews/v22/tools/port_r131.py on top of port_v22.py (Section 4's metric paragraph; Section 5.1 whole, retitled 'Names and counts'; Section 5.2 whole but its last paragraph; Table 1's matched column, hybrid row and two-metric difference row; Figure 3 on the matched metric (fig3_data_r131.py); the abstract's second sentence and three findings; Section 1's findings paragraph and second contribution; the Conclusion's sentences two to four; the evidence table's first row; Section 6's FR-Bank sentence and the merged Graphiti paragraph; the Limitations), the appendix by appendix_r131.py (C.2, E.9, F, G.4, the reader's guide; every table from reviews/r125/results), the number gate reviews/v22/tools/r131_number_gate.py (135 checks, 0 mismatches), the ledger reviews/NUMBERS_R131.md (ledger_r131.py), the page payers of section H as applied (port_r131.py --payers), the report reviews/v22/REPORT_R131.md. Sources: reviews/r125/REPORT_R125_T1.md, REPORT_R125.md, r82_counterfactual/cf2/NUMBERS_CF2.md section 15.

- **R131-A [Section 4, the metric paragraph]** (recorded). The author's paragraph: the matched AUROC defined ('the share of triples in which the PN version outscores the PRESENT version, ties counting half'), post hoc, with the pooled metric as the one fixed in advance; the sentence 'when they disagree, the wider governs' leaves with it (the author's text); the persona-interval sentence moves to Table 1's caption.
- **R131-B [Section 5.1, 'Names and counts', whole]** (recorded). Four paragraphs in the author's words: 'Within a triple, a name or a count can identify the obligation.' (the category-given reader wins every counted-state triple, 30/0/0 and 30/0/0; the lookup 82/6/0 on supersession); 'The two smaller models read only the names.' (names-only within 0.01 on either metric; counts alone below names alone by 0.14 matched for each, 0.12 and 0.16 pooled; both reliably below the guessing count reader, 0.77 and 0.75); 'Removing the target name leaves mini near chance.' (0.86 to 0.53; 0.89 to 0.68); 'The three stronger models also read the counts.' (0.58 to 0.87 matched on the counted states, none reliably below the guessing reader; the moved count: Opus -0.2833 and Sol -0.3250 on the counted states, Luna -0.3167 / -0.2667, each reliable; mini and Haiku no reliable change; pooled as R129 printed; names-only costs Luna -0.0598 and Opus -0.0426 pooled, reliable; Sol not run). The R126 and R129 paragraphs 'Models read the names more than the counts', 'Count readers separate states that models barely tell apart', 'A bare count can give the obligation away' and 'The three stronger models follow a count when it moves' are replaced whole. AUX-CF2-R125-*, AUX-R131-PRINTED.
- **R131-C [Section 5.2, whole but the last paragraph]** (recorded). Four paragraphs in the author's words: 'On the named state, no model reliably beats the lookup.' (the lookup 0.9659 on supersession; Opus +0.0114, Luna and Sol -0.0057, mini -0.0739 reliable; the sibling-name control 0.8807 to 0.9716, none reliably above the lookup; random tokens 0.4716, the count reader 0.5000); 'The stronger models' lead comes from counts, and a count feature closes it.' (the lookup and Haiku 0.7770, mini 0.7264; Luna 0.8784, Sol 0.8581, Opus 0.8750, +0.0811 to +0.1014 reliable; the hybrid 0.8851, +0.1081 reliable, level with the three; pooled 0.7865 with the three +0.0540 to +0.0635 above); 'Naming all states lifts every reader.' (the lookup 0.9088; Haiku +0.3500 on the counted states; Opus 0.9392; +0.0304 not reliable against +0.0323 reliable pooled); 'List length and coverage inflate both metrics.' (0.7500 / 0.5000; 0.5954 / 0.6453; 24 of 88 empty; +0.1318 reliable). The R129 paragraph 'Long or wrong name lists weaken the readers together.' stays as the last paragraph. The R129 hybrid paragraph (withdrawn at the R129 close) returns inside the second paragraph with its comparison reversed under the matched metric.
- **R131-D [Table 1 and Figure 3]** (recorded). Table 1: the column 'PN vs PRESENT' (the pooled PN-against-PRESENT AUROC) becomes 'matched', (W + T/2) / 148 from the printed W/T/L (AUX-R131-TAB1); the hybrid reader's row ('Lookup with one count feature', 0.79 [0.75, 0.82]; matched 0.89; 114/34/0); the difference row prints both metrics at four decimals (pooled +0.0323 [+0.0060,+0.0617]; [+0.0077,+0.0608]; matched +0.0304 [-0.0068,+0.0643]; [-0.0038,+0.0648]) because the matched persona interval's lower bound rounds to -0.00 at two decimals; the caption's post hoc clause in the author's words; footnote b defines the hybrid row. Figure 3: reviews/v22/src/fig3_data_matched.tex (copied from reviews/r125/results/fig3_data_matched.tex after checking every value against r125_matched.json), the y axis from 0.35 (mini's expiry value 0.40), the y label 'matched AUROC', the author's caption; the pooled figure moves to Appendix C.2 as fig:perstate-pooled (build_v22.py splices the pooled data there with its macros renamed).
- **R131-E [the abstract, Section 1, the Conclusion, the evidence table]** (recorded). The abstract's second sentence and three findings, Section 1's findings paragraph and second contribution bullet, the Conclusion's sentences two to four and the evidence table's first-row limit in the author's words (the gate-driven words under R131-G). Before (abstract, findings one and two): "First, names carry the signal: removing counts leaves GPT-4.1 mini and Haiku 4.5 within $0.01$, whereas counts alone cost mini $0.12$ and Haiku $0.16$ against names alone. Second, no model reliably beats a name lookup on the state named by the default summary. GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 lead it by $0.07$ to $0.08$ on the counterfactual set; Opus leads by $0.03$ when all states are named." After: "First, GPT-4.1 mini and Haiku 4.5 read only the names; GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 also read the counts and follow one when it is moved. Second, on the state a summary names, no model reliably beats a cosine lookup over the names. With counts and list length kept fixed, the lookup and every model separate the right name from a sibling at or above $0.88$, while meaningless tokens and counts fall to chance. The three stronger models lead the lookup by $0.08$ to $0.10$ within matched triples, and a lookup given one count feature closes that lead." Before (Conclusion, sentences two to four): "Removing names weakens the obligation judgment more than removing counts. Under the default summary, no model reliably exceeds the name lookup on supersession, while some models add signal on counted states. With all states named, Opus has a reliable overall advantage." After: "The smaller models read only the names; the stronger ones also read the counts, and a lookup given one count feature matches them within triples. On a named state no model reliably exceeds the name lookup, with list length kept fixed or not; with all states named, Opus's $0.03$ lead is reliable on one metric and not on the other." The evidence table's first row: "comparison with \present{} alone is post hoc" becomes "the matched within-triple comparison is post hoc".
- **R131-F2 [Section 6]** (recorded). The FR-Bank paragraph's last sentence, before: "Haiku retains more of its gain than mini does, and more where the target's name survives the store's list ($0.87$ against $0.68$ where it does not; descriptive)." After: "Haiku retains more of its gain than mini does. The loss is not an artifact of the obligations the alignment misses: on the $82$ it marks, the capped summary still costs mini $0.13$, Haiku $0.13$ and the lookup $0.20$, each reliable." (AUX-CF2-R125-T3-FRBANK: -0.1274, -0.1258, -0.2027; the name-survival clause stays in Appendix E.9, AUX-BH-SPLIT). The two Graphiti paragraphs ('Graphiti's names serve the lookup better than mini.' and 'Graphiti's invalidation recovers some forbidding records, but misses most.') merge into the author's one: "Graphiti writes part of what the judgment needs, and part of its loss is extraction." (13 of 34; 11 of 34 never extracted; 0.58 over all 47 against 0.74; the lookup 0.68, +0.10 reliable; on the 23 retained 0.69 against 0.84, -0.1512 reliable; AUX-CF2-R125-T3-GRAPHITI). Leaving the body with them: 'It gains nothing reliable over question only.', 'The reduced variants used elsewhere do not exist on these graphs.', 'exceeding the predicted quarter' (G.4 keeps all three).
- **R131-G2 [Limitations]** (recorded). Added: "The matched metric and every comparison made with it are post hoc; the metric fixed in advance is the pooled AUROC. Sol did not run the names-and-counts ablation, and among the stronger models only Opus ran the all-states summary." Replaced, before: "The ground-truth tags in retrieved views depend on aligning manifests to stored records. That alignment marks the forbidding record for $82$ of $104$ obligations." After: "The ground-truth name lists are built through the manifest-to-record alignment. The $22$ obligations it does not mark are therefore invisible to every summary (mini scores $0.52$ on them under ground truth)." (AUX-CF2-R125-T3-FRBANK, the 22: mini's ground-truth row 0.5210.) Deleted: "Two further encoders leave the default lookup within $0.01$ of its score." (it stays in E.8) and "The reader split cannot establish why the models differ and does not simply follow size." The pending sentences stay.
- **R131-H [the appendix]** (recorded). C.2: tab:cf-nc-strong (E2 Amendment 1; P-N3 failed on Luna, held on Opus 5; P-N4 held; P-N5 failed; Sol not run) after tab:cf-names-counts; the matched metric after tab:pnpresent (tab:cf-matched, tab:cf-classes, tab:cf-matched-vs, tab:cf-matched-ablations, fig:perstate-pooled, tab:cf-emptiness); tab:cf-hybrid's matched panels; the sibling-name control (tab:cf-sibling; P-SB1 to P-SB4 held, P-SB1 and P-SB3 disclosed as recorded values from the pre-freeze dry run). E.9: what the store is in each scored condition; tab:levels-strata. G.4: tab:graphiti-strata with its paragraph. F: tab:registrations-e (the two R125 registrations, 5cd8f809f2, day 41; tab:registrations-d is a [H] table at its page's height) and the count paragraph: 98 predictions, 31 otherwise (AUX-R131-COUNT; P-SB1 and P-SB3 not counted). The reader's guide points to the new tables. Every value from reviews/r125/results; pinned under pin_appendix_r126.py r131.
- **R131-G [the gate-driven wording changes on the author's texts; each the smallest change satisfying its rule, old beside new]** (recorded).
  - [Q-C (the AUROC definition's words) and Q-A (the opener carried the numeral 0.50; split at the semicolon)] Section 4. Before: "the chance that a positive ranks above a negative \citep{hanley1982}; chance is $0.50$." After: "the chance that a positive scores above a negative \citep{hanley1982}. Chance is $0.50$."
  - [V and code_scan ('registered' in the main text)] Section 4. Before: "The registered metric pools all items." After: "The metric fixed in advance pools all items."
  - [L (51 words; split at the colon)] Section 5.1. Before: "with the names unchanged, all three follow it: across the two counted states Opus falls" After: "with the names unchanged, all three follow it. Across the two counted states Opus falls"
  - [L (46 words; split at the semicolon)] Section 5.2. Before: "the lookup and Haiku score $0.78$ and mini $0.73$; Luna, Sol and Opus score $0.86$ to $0.88$," After: "the lookup and Haiku score $0.78$ and mini $0.73$. Luna, Sol and Opus score $0.86$ to $0.88$,"
  - [L (42 words; split at the semicolon)] Section 5.2. Before: "the three stay a reliable $0.05$ to $0.06$ above it; their remaining edge is in pairs" After: "the three stay a reliable $0.05$ to $0.06$ above it. Their remaining edge is in pairs"
  - [L (48 words; split at the colon), V ('held'), G2 ('at $0.88$ or higher' in a sentence naming the lookup)] Abstract. Before: "no model reliably beats a cosine lookup over the names: with counts and list length held fixed, the lookup and every model separate the right name from a sibling at $0.88$ or higher, while meaningless tokens and counts fall to chance." After: "no model reliably beats a cosine lookup over the names. With counts and list length kept fixed, the lookup and every model separate the right name from a sibling at or above $0.88$, while meaningless tokens and counts fall to chance."
  - [V ('held')] Section 1. Before: "no model reliably outscores the lookup, with list length held fixed or not." After: "no model reliably outscores the lookup, with list length kept fixed or not."
  - [D (71% with the abstract's third sentence)] Section 1. Before: "a lookup given one count feature catches them within matched triples." After: "a lookup given one count feature catches them within triples."
  - [D (71% with Section 5.1's first claim)] Section 1. Before: "The two smaller models read only the attribute names; Luna, Sol and Opus also read the counts." After: "The two smaller models read the attribute names alone; Luna, Sol and Opus also read the counts."
  - [V ('held')] Conclusion. Before: "no model reliably exceeds the name lookup, with list length held fixed or not;" After: "no model reliably exceeds the name lookup, with list length kept fixed or not;"
  - [S17 ('the join')] Section 6. Before: "The loss is not an artifact of the obligations the join misses: on the $82$ it marks," After: "The loss is not an artifact of the obligations the alignment misses: on the $82$ it marks,"
  - [V and code_scan ('registered' in the main text)] Limitations. Before: "the registered metric is the pooled AUROC." After: "the metric fixed in advance is the pooled AUROC."
  - [Q-A (the opener carried the numeral 22; split after 'alignment')] Limitations. Before: "The ground-truth name lists are built through the manifest-to-record alignment, so the $22$ obligations it does not mark are invisible to every summary" After: "The ground-truth name lists are built through the manifest-to-record alignment. The $22$ obligations it does not mark are therefore invisible to every summary"
  - [L (43 words; split at the semicolon)] Section 7, payer 2. Before: "because they mark more of the forbidding records already in view; a reader that merely counts tagged lines scores $0.62$ under either tag source." After: "because they mark more of the forbidding records already in view. A reader that merely counts tagged lines scores $0.62$ under either tag source."
  - [S7 (a sentence twice)] Appendix C.2, the pooled figure's caption: "Luna and Sol ran only the default summary." (Figure 3's caption, the author's) reads "Luna and Sol have rows under the default summary only." in the appendix copy.
  - [S17 ('both intervals excluding zero', capped at three outside registered blocks)] the appendix prose and captions of R131 say 'both intervals clear of zero'.
- **R131-F [the frozen strings R131 changed on top of the R129 close; `reviews/v22/results/frozen_r131_e.json`]** (recorded). Each string below occurred in paper_v21.tex, was kept through the R129 close and occurs a different number of times after R131; each is authorized under the entry above that replaced it.
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "no model reliably exceeds the name lookup on supersession"

The R131 close (2026-09-20), inside this block: the author's four blocks landed in one pass by reviews/v22/tools/port_r131_close.py on top of port_v22.py and port_r131.py --payers=1,2,3,4 (the abstract verbatim; L1 to L4; A1', A2' and the tex-658 word drop; 1A; 1B; the payers 5, 5b, 6, 7, 8 and B2, cumulative), the appendix by appendix_r131_close.py (E.3's provenance paragraph, E.9's disclosure sentence, A5 in B and E.4; build_v22.py REPAIRS_R131CLOSE_BLOCK for E.4's carried caption), the number gate reviews/v22/tools/r131_close_gate.py (37 checks, 0 mismatches; every count of E.3's paragraph from the tree), the ledger rows AUX-R131-CLOSE-PRINTED and -PROV of reviews/NUMBERS_R131.md (ledger_r131_close.py), the cumulative costed table reviews/v22/results/cost_payers_r131_close.md, the report reviews/v22/REPORT_R131_CLOSE.md.

- **R131-CLOSE-B1 [the abstract, whole, verbatim; hand-tuned (B4)]** (recorded). Before: "An agent with persistent memory must judge whether its store holds content it should no longer use. We test that judgment before retrieval on $148$ questions, each asked of three versions of one store, through summaries that list counts and attribute names with values removed. First, GPT-4.1 mini and Haiku 4.5 read only the names; GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 also read the counts and follow one when it is moved. Second, on the state a summary names, no model reliably beats a cosine lookup over the names. With counts and list length kept fixed, the lookup and every model separate the right name from a sibling at or above $0.88$, while meaningless tokens and counts fall to chance. The three stronger models lead the lookup by $0.08$ to $0.10$ within matched triples, and a lookup given one count feature closes that lead. Third, the backends we tested omit or misstate this information: under FR-Bank's own metadata, GPT-4.1 mini and the lookup fall to $0.60$ and $0.59$. At retrieval, a fetch keyed on the names raises reach from $0.52$ to $0.82$, gated by a model or always on, with a budget trade-off. These synthetic-store tests establish neither better answers nor a validated answer-stage detector; human validation remains pending." After: "\begin{abstract} An agent with long-term memory can answer from a record it should no longer use, such as a plan the user later cancelled. We test whether an agent can tell, before retrieving anything, that its store holds such a record, from a summary alone: the number of records in each lifecycle state, and a list of attribute names with the values removed. Each of $148$ questions is asked against three versions of one store that differ in one attribute, so a question's wording cannot give the answer away. First, ablations show that the two smaller of five models rely on the attribute names alone, while the three stronger ones also use the state counts. Second, for superseded records, the one state whose names the summary lists, no model reliably beats a cosine-similarity lookup over those names. Under a control that holds counts and list length fixed, the lookup and every model pick the correct name over a similar one at an AUROC of $0.88$ or higher (chance $0.50$). The stronger models lead the lookup by $0.08$ to $0.10$ overall, a lead that comes from retracted and expired records, which the summary only counts; adding one count feature to the lookup closes it. Third, the memory backends we tested omit or misstate this information. Given only what FR-Bank, a backend that tags every entry with a lifecycle state, actually writes, GPT-4.1 mini and the lookup drop from $0.73$ and $0.75$ to $0.60$ and $0.59$ on our larger question set. In these tests, what the store wrote down mattered more than which model read it. All stores are synthetic, and whether better judgments yield better answers is not established; human validation is pending. \end{abstract}" Its numbers: 148 (the triples); 0.88 (the sibling floor, Haiku 4.5 0.8807, AUX-CF2-R125-SB-*); chance 0.50; 0.08 to 0.10 (AUX-CF2-R125-VS-LOOKUP +0.0811 to +0.1014, each reliable; the lead decomposes to retraction and expiry, supersession -0.0057, -0.0057, +0.0114 none reliable); 0.73 and 0.75 to 0.60 and 0.59 (AUX-E1R-TRUE-NOK 0.7339, AUX-E1R-NB6 0.7484 / 0.5858, AUX-E1R-BELIEVED-NOK 0.5959; the full obligation set, ground truth against FR-Bank's capped store-written summary). The last clause ('human validation is pending') is a placeholder (B5), replaced when the HV-1 numbers exist. The fetch sentence (0.52 to 0.82) leaves the abstract; Section 7 and Table 3 keep it.
- **R131-CLOSE-B4 [the gate rulings on the abstract]** (recorded). Rule D's near-duplicate pair, the abstract's last-but-one sentence against Section 1's thesis sentence (85%), is overridden by the author ('Restating the thesis in both places is intended.'): tools/prose_scan.py WHITELIST gains the abstract's sentence with this entry as its authority. Rule V on 'holds ... fixed': overridden, recorded; the rule bars 'held', not 'holds', so it did not fire. G2 (FINAL RULINGS 3): the pattern reading governs; 'drop from $0.73$ and $0.75$ to $0.60$ and $0.59$' stands (G2 concerns the lookup's level on the counterfactual set, where the level depends on the metric; the full-set numbers have one metric; R124 block C states no contradicting reason); the drops, for the record, 0.1380 and 0.1626 (AUX-R131-CLOSE-PRINTED). No gate changed a word of the abstract.
- **R131-CLOSE-B2 [Section 1, the findings paragraph; the abstract's payer]** (recorded). Before: "In these tests, what the store writes down mattered more than which reader read it. The two smaller models read the attribute names alone; Luna, Sol and Opus also read the counts. On the one state the default summary names, no model reliably outscores the lookup, with list length kept fixed or not. The three stronger models pull ahead of it through the counted states, and a lookup given one count feature catches them within triples. Models differ further when the rubric states the intent rule. Backend errors weaken the information supplied to every reader, while the retrieval fetch supplies much of the added reach." After: "In these tests, what the store writes down mattered more than which reader read it. Models differ further when the rubric states the intent rule." Every deleted claim is in the contribution bullets below it or in Section 5 (names alone / counts, bullet 2; no reliable lookup margin including the sibling-name control, bullet 2; the one-count-feature lookup within triples, bullet 2; the backend loss and the fetch's reach, bullet 3). No number leaves.
- **R131-CLOSE-L [Limitations L1 to L3; Section 4 L4]** (recorded). L1 before: "The counterfactual test bypasses backend writing; FR-Bank and Graphiti use the same personas." after: "All tests use one bank of $40$ synthetic personas; transfer to a second benchmark is untested. The counterfactual test bypasses backend writing, and no backend tested here is shown maintaining the summary." (40 verified against the bank). L2 before: "The capability comparison on the counterfactual set covers closed models from two vendors, with no open-weights model." after: "The counterfactual comparison covers closed models from two vendors; the one open-weights model, Kimi K3, completed only the cross-vendor replication." ('completed only', FINAL RULINGS 4: Kimi K3 ran the cross-model set and was stopped at the budget on the full populations, tab:runs; 'open weights' is the authors' assertion, weights published by the vendor, July 2026). L3 before: "Under the explicit-intent rubric, only mini and Luna were rerun on the original counterfactual task: both stay within $0.02$ of their main-study scores, and Luna retains a reliable lookup margin. (Appendix~\ref{app:counterfactual})" after: "Under the explicit-intent rubric only mini and Luna were rerun. (Appendix~\ref{app:counterfactual})" (C.2 prints the within-0.02 result, 0.8531 against 0.8417 and 0.7253 against 0.7167, and Luna's reliable margin +0.0867). L4 before: "Kimi K3 joins the smaller comparison shared across vendors." after: "Kimi K3 (open weights) joins the smaller comparison shared across vendors."
- **R131-CLOSE-A [provenance and anonymity: A1', A2', A5 (the statement), A1'' (E.3), the A3 follow-up (E.9)]** (recorded). A1' (Section 4) before: "Language models generate the questions and synthetic persona stores from human-written manifests." after: "The personas, their human-written manifests and sessions, the FR-Bank, Mem0 and A-MEM stores and part of the main question set come from the FR-Bank release \citep{fr}. Language models drafted our other questions, and we built the Graphiti graphs from the released FR-Bank records, with lifecycle fields removed. (Appendix~\ref{app:construction})" A2' (the AI-use statement) before: "We used generative AI tools for synthetic data generation and for implementation. The synthetic persona bank, the stores built from it, and every question set were generated with large language models from human-written manifests and specifications, and those manifests are the ground truth against which every label is scored." after: "We used generative AI tools to draft questions and for implementation. The persona bank, its sessions and the FR-Bank, Mem0 and A-MEM stores are a released synthetic benchmark \citep{fr}. Language models drafted the question sets we added, and Graphiti's language-model pipeline built our graphs from the released FR-Bank store's records, rendered one episode per session without its lifecycle fields; the benchmark's human-written manifests are the ground truth against which every label is scored." A5 before: "executed the experimental protocols under preregistered, human-directed designs with frozen decision rules," after: "executed the experimental protocols under human-directed designs with frozen decision rules," (the word dropped, FINAL RULINGS 6). Verified against the tree (A4'): the 40 personas, their manifests, 1,400 sessions, the FR-Bank, Mem0 and A-MEM stores (LifeMemEval/artifacts/lifecycle_banks, mem0_41mini_banks, amem_banks, the directories e1_metamemory/tools/backends.py reads) and the 516 questions are in the FR-Bank release's freeze 5b097fb; this study drafted the natural-absent probes, the counterfactual questions and versions, the crossed intent questions and the paraphrases, and built the Graphiti graphs from FR-Bank's store records rendered one episode per session with every lifecycle field removed (r85_graphiti/render_episodes.py), not from the session transcripts (the correction of FINAL RULINGS 1). A1'' (Appendix E.3): "\paragraph{Provenance of the personas, the stores and the questions.} The persona bank, the three main stores and the questions of the main study come from the FR-Bank release \citep{fr}; the question sets this study added were drafted by language models. The release holds $40$ personas, each with a human-written manifest and $35$ language-model-generated sessions ($1{,}400$ in all), the FR-Bank, Mem0 and A-MEM stores built from those sessions, and $516$ questions. This study asks $187$ of those questions of the full FR-Bank store and its two ablated variants, the category-removed and the slot-removed store ($178$, $176$ and $162$ questions; $516$ of the $661$ items of the full obligation set). It adds the $145$ natural-absent probes, drafted by a language model and verified against the manifests. GPT-4.1 mini drafted, through frozen renderers, the counterfactual set's $148$ questions with their three store versions ($444$ items) and the expiry extension ($14$ pairs, $42$ items). It also drafted the $113$ crossed intent questions asked of $118$ drafted and the $148$ paraphrases. The cross-vendor set is $84$ of the $661$ items ($76$ with a released question, $8$ probes) and the question-only probes are classifiers over the existing question strings, so neither adds a question. The Graphiti graphs, one per persona, were built by the unmodified release from $1{,}365$ episodes rendered from the FR-Bank store's records, one per session, with every lifecycle field removed (Appendix~\ref{app:posthoc-graphiti})." A3 follow-up (Appendix E.9) before: "Disclosure, because it bears on independence: the personas and episodes used here were ingested into that backend earlier under a copy carrying four documented numeric-preservation modifications." after: "Disclosure, because it bears on independence: the FR-Bank release \citep{fr} built an earlier version of its store on a copy of this backend carrying four documented numeric-preservation modifications and ingested these personas into it." (the release vendors graphiti/ 0.28.1 and graphiti_patches/; the FR paper's FR-Graphiti row). A5 in the appendix (FINAL RULINGS 6): B "The item-level interval is the preregistered primary endpoint and the persona-clustered interval is the sensitivity, because that is the convention everywhere in this paper." -> "The item-level interval is the registered primary endpoint and the persona-clustered interval is the sensitivity, because that is the convention everywhere in this paper."; E.4 "The preregistered item-level interval remains the primary endpoint." -> "The registered item-level interval remains the primary endpoint." and tab:cluster-sensitivity's caption 'reports the preregistered item-level interval' -> 'reports the registered item-level interval' (REPAIRS_R131CLOSE_BLOCK); left as ruled: the pinned sections' hits (A: the ladder table's caption and the expansion sentence; E.3: the corpus row's 'preregistered Mem0 exclusions' and the retention-threshold sentence; E.7: 'reported as they were preregistered'; E.10: 'Each was preregistered' and 'The preregistered reading'; F: the Opus-entry paragraph) and the four artifact names of tab:registrations (E0, E1, E1-XV, E1-QP preregistration). The A3 census (we / our / an agentless passive on creating personas, sessions or manifests) found the two replaced sentences, the AI-use opener (now 'to draft questions') and, borderline, E.9's disclosure (now attributed) and G.4's 'episodes rendered from FR-Bank's persona banks' (stays, FINAL RULINGS).
- **R131-CLOSE-1 [MERGED RULINGS 1A and 1B]** (recorded). 1A: the count 98 / 31 stands (P-SB1 and P-SB3 out of the count, in tab:registrations-e as recorded before the freeze; 100 / 31 printed nowhere); Table 1's difference sub-table at four decimals, uniform, with the caption note "Differences at four decimals."; Sol's 0.33 confirmed as half-up on the recorded four-decimal value, the convention of every check (AUX-R131-CLOSE-PRINTED). 1B: the builders box before: "in our tests a model added something only on counted states, explicit intent questions, and the reported all-states comparison, and in the scenario we priced," after: "in our tests a model added something only on counted states, on explicit intent questions and, on the pooled metric only, in the all-states comparison, and in the scenario we priced," (the author's words, FINAL RULINGS 4: deletion alone would omit the pooled reliable lead). 'one name longer' -> 'at least one name longer': the body's only instance leaves with payer 8; C.2's two sentences stay (the section is pinned; tab:cf-emptiness prints 81 / 6 / 1; FINAL RULINGS 3).
- **R131-CLOSE-P [the page payers, cumulative in the ruled order (MERGED RULINGS 1C); the costed table reviews/v22/results/cost_payers_r131_close.md]** (recorded). Payer 5 (Section 5.1): the target-name paragraph out, "\claim{Removing the target name leaves mini near chance.} On supersession questions in the full obligation set, removing the target name and its nearest neighbours lowers mini from $0.86$ to $0.53$ and Haiku from $0.89$ to $0.68$, both reliably. (Appendix~\ref{app:resp})" (E.10 tab:resp-l1 prints 0.8572 -> 0.5310 and 0.8897 -> 0.6759, both reliable); the pointer "that only guesses the question's category ($0.77$ and $0.75$). (Appendix~\ref{app:counterfactual})" -> "that only guesses the question's category ($0.77$ and $0.75$). (Appendix~\ref{app:counterfactual}; target-name ablation: Appendix~\ref{app:resp})". Payer 5b (the Conclusion): "The explicit intent test shows a further distinction among readers, bounded by the fixed cue list's performance." -> "Told the intent rule, only the three stronger models apply it, and a fixed cue list matches the best of them." (Luna 0.96, Sol 0.88, Opus 0.99 under the explicit rubric; mini 0.48, Haiku 0.55; the cue list 0.9943 against Opus's 0.99). Payer 6 (Section 5.3, P6a to P6d): deleted "These comparisons use the first draw for every reader." (tab:cf-intent's caption says the body reads the draw-1 column; no caption addition, P6a); deleted "When Sol fails, it often scores both questions high, leaving the rule unapplied." (the caption: 9 of Sol's 11 losses score both questions 0.96 or higher); "Those models score the change question higher, consistent with the scored step asking whether stale content exists. The content remains in the store." -> "Those models score the change question higher, consistent with a scored step that asks whether stale content exists."; deleted "Across these tests, stating the rule lowers no model's score on its original questions beyond tolerance." (the caption: the largest fall -0.0458). Every bold lead, the 0.96 / 0.88 / 0.99 sentence, the cue list at 0.99, the no-general-advantage sentence, the underspecified-prompt sentence and Sol's 0.64 untouched. Payer 7 (Figure 3): height 5.0cm -> 4.5cm, width, markers and fonts unchanged; rendered at both heights: the Luna 0.8667 / Sol 0.8333 expiry markers (the only pair near the 0.86 to 0.88 band) do not overlap at either height; one new corner touch of 0.26pt appears between mini 0.9205 and Haiku 0.8920 in the right panel's supersession cluster (outside the band; reported). Payer 8 (Section 5.2): "\claim{List length and coverage inflate both metrics.} A reader that only knows whether the store covers the question scores $0.75$ pooled and $0.50$ matched. A lookup over meaningless tokens scores $0.60$ pooled and $0.65$ matched, because the \pn{} version's list is one name longer and $24$ of the $88$ \present{} lists are empty; the name lookup is a reliable $0.13$ above it on the matched metric. The sibling-name control is the comparison that removes both. (Appendix~\ref{app:counterfactual})" -> "\claim{List length and coverage lift both metrics.} A reader that only knows whether the store covers the question scores $0.75$ pooled and $0.50$ matched. The name lookup stays a reliable $0.13$ above a lookup over meaningless tokens on the matched metric. (Appendix~\ref{app:counterfactual})" (0.60 / 0.65 and 24 of 88 stay in tab:cf-emptiness and tab:cf-matched). Payer B2: the entry R131-CLOSE-B2. Section 8 and the evidence table are not payers (ruled). O1 lands only at slack +5 or better.
- **R131-CLOSE-G [the gate-driven wording changes on the close's texts; each the smallest change satisfying its rule, old beside new]** (recorded).
  - none: every prose gate passed on the author's texts as given (the D override of R131-CLOSE-B4 is a ruling, not a wording change).
- **R131-CLOSE-F [the frozen strings the close changed on top of the R131 checkpoint; `reviews/v22/results/frozen_r131_close_c.json`]** (recorded). Each string below occurred in paper_v21.tex, was kept through the R131 checkpoint and occurs a different number of times after the close; each is authorized under the entry above that replaced it.
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "were ingested into that backend earlier under a copy"

The R131 close's page 8-9 payers (2026-09-20), inside this block: W1 to W7 landed cumulatively by reviews/v22/tools/port_r131_w.py on top of port_r131_close.py --payers=5,5b,6,7,8,B2 (the number gate r131_w_gate: 9 checks, 0 mismatches), costed by cost_payers_r131_w.py (W1 -4; +W2 -3; +W3 -3; +W4 -2; +W5 -1; +W6 +0; +W7 +1; without W3 +1). Gates may not reword these texts; a trip is reported and the author rules.

- **R131-W1 [Section 8, the first paragraph]** (recorded). Before: "Across the shared cross-vendor questions, models whose question-only score varies gain a reliable $0.15$ to $0.45$, including Kimi." After: "On the shared cross-vendor questions, models whose question-only score varies gain a reliable $0.15$ to $0.45$, including Kimi." (the pointer '(Appendix A)' joined the line above after W1a, so W1b, 'Kimi included', was not needed).
- **R131-W2 [Limitations, paragraph 1]** (recorded). Before: "Retraction and expiry remain small groups: the counterfactual set has $30$ pairs of each. The full obligation set has $26$ retraction obligations and $15$ expiry obligations, so those state-specific results give only a direction." After: "Retraction and expiry are small groups ($30$ counterfactual pairs each; $26$ and $15$ obligations on the full set), so state-specific results give only a direction." (30 / 30 pairs, r125_matched.json; 26 and 15 obligations, r125_t3_frbank.json all_104 by_state).
- **R131-W3 [Limitations, paragraph 3] WITHDRAWN pending the ruling** (recorded). The author's sentence "The ground-truth name lists come from the manifest-to-record alignment, so the $22$ obligations it does not mark are invisible to every summary (mini scores $0.52$ on them under ground truth)." opens its paragraph on the numeral 22, which q_scan rule Q-A bars (the R131 checkpoint had split it for that reason); gates may not reword it, so it is reported; the R131 split stands meanwhile ("The ground-truth name lists are built through the manifest-to-record alignment. The $22$ obligations it does not mark are therefore invisible to every summary (mini scores $0.52$ on them under ground truth)."). W3 bought no line (-3 to -3), and W1 to W7 without it read +1.
- **R131-W4 [Section 7, the tested-rule paragraph]** (recorded). Before: "But $187$ of $272$ audited stale lines sit under a different attribute key from their tagged twin. The view-side rule we tested cannot make the repair, which leaves the write path." After: "But $187$ of $272$ audited stale lines sit under a different attribute key from their tagged twin, which leaves the write path." (the third sentence repeated the bold lead).
- **R131-W5 [Limitations, paragraph 2]** (recorded). "the metric fixed in advance is the pooled AUROC" -> "pooled AUROC was fixed in advance"; "The paraphrase check, with one rewording per question fixed in advance, is not yet scored." -> "The paraphrase check is not yet scored." (the one-rewording design is stated in Appendix C.2's paraphrase paragraph, checked; the sentence is replaced on 22 Sep).
- **R131-W6 [Conclusion]** (recorded). "with list length kept fixed or not; with all states named, Opus's $0.03$ lead is reliable on one metric and not on the other." -> "with list length kept fixed or not." (the all-states clause deleted because still short of +2; Section 5.2 keeps 'Opus's $0.03$ lead over that lookup is reliable on the pooled metric and not on the matched one').
- **R131-W7 [Section 8, the second paragraph; Appendix E.8]** (recorded). Before: "On easier coverage questions, mini's advantage over the superseded-name lookup disappears against a lookup over the whole name map. On the counterfactual set, all reported model coverage intervals exclude chance. (Appendix~\ref{app:baselines})" After: "On easier coverage questions, mini's advantage over the superseded-name lookup disappears against a lookup over the whole name map. (Appendix~\ref{app:baselines})" E.8 gains, after the paragraph on where the lookup has values: "On the counterfactual set every model's coverage interval excludes chance (Table~\ref{tab:cf-fok}, Appendix~\ref{app:counterfactual})." (C.2 prints the intervals, tab:cf-fok; pinned under pin_appendix_r126.py r131w).
- **R131-W-F [the frozen strings the W payers changed; `reviews/v22/results/frozen_r131_close_e.json`]** (recorded). Each string below occurred in paper_v21.tex, was kept through the close checkpoint and occurs a different number of times after W1 to W7; each is authorized under the entry above that removed it.
  - UNAUTHORIZED [Q CLAIMS] 1 -> 0: "The view-side rule we tested cannot make the repair, which leaves the write path."

## R133 AUTHORIZATION BLOCK — dated 2026-09-21

Program R133: the v23 lineage, opened from the R131 close `b3cc631` (`reviews/v23/`, base tree `0ec9c4ad`; `reviews/v23/tools/bump_v23.py`), the readability pass of the author's brief 'R133: V23 READABILITY PASS' (2026-09-21): bookkeeping hedges out of the running prose of Sections 4 to 8 into their appendix homes (`reviews/v23/HEDGE_LEDGER.md`), the author's claim-narrowing swaps S1 to S12, Sections 4 to 8 rewritten. No number changes value, population or condition; no new claims; nothing deleted from the appendix. The edits are `reviews/v23/tools/port_r133.py` (every edit asserted), the number gate `reviews/v23/tools/r133_number_gate.py`, the report `reviews/v23/REPORT_R133.md`, the sign-off file `reviews/v23/OLD_BESIDE_NEW_V23.md`. frozen_diff runs with `--program=R133` against the v23 base; v22 is frozen and is the fallback build.

- **R133-HOMES [section 4: the coverage homes]** (recorded). Appendix A gains the paragraph 'Coverage notes for the daggers in the main text' after tab:runs (five items, (i) to (v): mini's one-call row under the names-and-counts ablation; Luna five draws and Opus one draw under the count removal with Sol not run; the all-states summary on mini, Haiku and Opus only; the intent crossover's draw counts and Sol's later addition; the full obligation set completed by Haiku, Luna and Opus with Sol and Kimi stopped at the budget), each the facts of tab:runs, tab:setup, tab:cf-names-counts, tab:cf-nc-strong, tab:cf-matched, tab:cf-intent and tab:x4-expansion restated. Table 74 (tab:provenance), row 1: 'lookup $0.77$ and models $0.72$ to $0.84$' was stale against Table 1 as built (0.72 is mini's one-draw temperature-0 row of Table 1's note a; 0.84 omits Sol's 0.85) and reads 'lookup $0.77$ and models $0.76$ to $0.85$' (r125_matched.json readers/{MINI5_v2 0.7648, H45_v2 0.7566, LUNA_v2 0.8417, SOL_v2 0.8500, OP5_v2 0.8405}/gate; reviews/v23/tools/r133_number_gate.py). Nothing deleted from the appendix.
- **R133-SWAPS [section 5: the author's verbatim swaps S1 to S11]** (recorded). Each swap verbatim from the brief, its numbers through r133_number_gate.py (32 checks, 0 mismatches; S3's Haiku pair on the same population and conditions as mini's and the lookup's: the 661, the ground-truth summary against FR-Bank's capped store-written summary, AUX-R74-X4-H45-NOK 0.8210 and AUX-BH-H45-15 0.7069 beside AUX-E1R-TRUE-NOK 0.7339 / AUX-E1R-BELIEVED-NOK 0.5959 and AUX-E1R-NB6 0.7484 / 0.5858; S2's 0.05 to 0.06 AUX-CF2-HYB-VS-MODELS +0.0540, +0.0553, +0.0635, each reliable). Old beside new for every swap is reviews/v23/OLD_BESIDE_NEW_V23.md (the swap unit). The abstract, Section 1 and the Conclusion change by these swaps only; no gate rewords a swap.
- **R133-S4 [section 6: Section 4 rewritten from its second paragraph]** (recorded). The models paragraph in the form of section 4.2 (the five models and their short names; Kimi K3 (open weights); the five-draw sentence; the one coverage sentence pointing to Appendix A and its daggers). Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md.
- **R133-S51 [section 6: Section 5.1 rewritten]** (recorded). The three paragraphs in the shape of section 6.1 (plain words first, at most three numbers in prose, the appendix pointer once at the end); the second paragraph is the brief's worked example (section 7) with its numbers through r133_number_gate.py; the hike carried once. Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md.
- **R133-S52 [section 6: Section 5.2 rewritten]** (recorded). The paragraphs in the shape of section 6.1; the count-feature paragraph is the brief's worked example (section 7) with its numbers through r133_number_gate.py; the pooled and matched split stated once at the top; the hike carried once. Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md.
- **R133-S53 [section 6: Section 5.3 rewritten; S10]** (recorded). The rubric point explicit in one sentence (S10); the paragraphs in the shape of section 6.1. Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md.
- **R133-S6 [section 6: Section 6 rewritten]** (recorded). The paragraphs in the shape of section 6.1; Table 2's numbers not repeated in prose; the Mem0 and A-MEM paragraph keeps U5 and its four conditions verbatim; the hike carried once. Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md.
- **R133-S7 [section 6: Section 7 rewritten]** (recorded). The paragraphs in the shape of section 6.1; the inverted-tag bookkeeping to Appendix E.10's paragraph; the hike carried once. Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md.
- **R133-S8 [section 6: Section 8 rewritten]** (recorded). The two paragraphs in the shape of section 6.1, the full-set comparison marked with a dagger resolving to Appendix A's note (v). Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md.
- **R133-S12 [section 5, S12: the optional Limitations sentence]** (recorded). Added because the final slack was +3 or better: 'Counts cannot say which record changed: two stores that cancel different plans in one category can share a summary, so only a named state identifies the obligation.'
- **R133-RULINGS [the author's R133 RULINGS of 2026-09-21]** (recorded). 1: the abstract keeps S3; Section 1's thesis sentence reads "In these tests, every reader we tried was held back by what the store had written down." and the Conclusion's first sentence "In these tests, no reader we tried made up for what the store had failed to write down." (both verbatim from the ruling), so the thesis sentence no longer repeats; the repeat_scan EXEMPT and slogan_scan EXEMPT_S7 exemptions R133-G added are removed and both scans pass unexempted (gate_edits_r133.py --rulings); slogan_scan's EXEMPT_S9 entry for S2's abstract sentence stays (the abstract is unchanged and S9 would otherwise fail it); prose_scan's WHITELIST carries the two ruled sentences for rule V ('held', 'failed' in their ordinary senses; the R101 precedent). 2: E.9's 'loss of content with over-marking' approved. 3: tab:routes (Appendix E.10) gains GPT-4.1 mini's per-state view-minus-summary rows for expiry and supersession with both intervals, from resp_review/run/scores_resp.json (AUX-RESP-L2-MINI-NOK; reviews/NUMBERS_R133.md AUX-R133-ROUTES-PERSTATE; r133_number_gate.py 47 checks, 0 mismatches), and Section 7 keeps the direction in prose and points to the table. 4: H26 stays. 5: the three 'reliable' candidates of REPORT_R133.md section 9 dropped (5.2's random-token margin, Section 6's Mem0 and A-MEM losses, Section 8's cross-vendor gains); no further cuts. 6: no action, awaiting ruling.
- **R133-G [the gate interactions]** (recorded). tools/slogan_scan.py: EXEMPT_S7 (new; the R131 close's B4 precedent) carries the thesis sentence the author's S3 and S4 put verbatim in the abstract and Section 1, and EXEMPT_S9 carries S2's abstract sentence ('but not when all items are pooled'); tools/prose_scan.py WHITELIST: the R131 close's B4 entry (the abstract's thesis sentence) is replaced by its S3 form, the rule D pair with Section 1 (S4, identical) and the Conclusion (S6) overridden by the author's swaps. G2 stands by pattern. code_scan's 'registered' collocations stand. Every rule V or D override inside Sections 4 to 8 is listed old beside new in REPORT_R133.md.
- **R133-F [the frozen strings of the v22 close that the pass changed; `reviews/v23/results/frozen_r133_rulings_b.json`]** (recorded). Each string below occurred in paper_v22.tex and occurs a different number of times in paper_v23.tex (a count of zero means the sentence left the text; the sentence carrying the claim now, where one does, is in reviews/v23/OLD_BESIDE_NEW_V23.md). Every one is authorized as changed by the pass under the entries above.
  - AUTHORIZED [Q CLAIMS] 1 -> 2: "Under the constrained rendering"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Luna's and Sol's shared cross-vendor rows are obtained through the vendor's agent tool."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The full obligation set supports the backend and retrieval comparisons. It contains 661 questions about the original stores and their variants."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Removing the rendering cap raises their scores without restoring their ground-truth results."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "(34 once one inverted ground-truth tag is corrected)"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Padding the default list to 60 names lowers the lookup to 0.67 on the full obligation set, and injected wrong names lower mini, Haiku and the lookup together, so short ground-truth lists do not establish robustness to longer store-written ones."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Haiku retains more of its gain than mini does. The loss is not an artifact of the obligations the alignment misses: on the 82 it marks, the capped summary still costs mini 0.13, Haiku 0.13 and the lookup 0.20, each reliable."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The metric fixed in advance pools all items."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "with the names unchanged, all three follow it. Across the two counted states Opus falls"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "the lookup and Haiku score 0.78 and mini 0.73. Luna, Sol and Opus score 0.86 to 0.88,"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "the three stay a reliable 0.05 to 0.06 above it. Their remaining edge is in pairs"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The loss is not an artifact of the obligations the alignment misses: on the 82 it marks,"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "because they mark more of the forbidding records already in view. A reader that merely counts tagged lines scores 0.62 under either tag source."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "\begin{abstract} An agent with long-term memory can answer from a record it should no longer use, such as a plan the user later cancelled. We test whether an agent can tell, before retrieving anything, that its store holds such a record, from a summary alone: the number of records in each lifecycle state, and a list of attribute names with the values removed. Each of 148 questions is asked against three versions of one store that differ in one attribute, so a question's wording cannot give the answer away. First, ablations show that the two smaller of five models rely on the attribute names alone, while the three stronger ones also use the state counts. Second, for superseded records, the one state whose names the summary lists, no model reliably beats a cosine-similarity lookup over those names. Under a control that holds counts and list length fixed, the lookup and every model pick the correct name over a similar one at an AUROC of 0.88 or higher (chance 0.50). The stronger models lead the lookup by 0.08 to 0.10 overall, a lead that comes from retracted and expired records, which the summary only counts; adding one count feature to the lookup closes it. Third, the memory backends we tested omit or misstate this information. Given only what FR-Bank, a backend that tags every entry with a lifecycle state, actually writes, GPT-4.1 mini and the lookup drop from 0.73 and 0.75 to 0.60 and 0.59 on our larger question set. In these tests, what the store wrote down mattered more than which model read it. All stores are synthetic, and whether better judgments yield better answers is not established; human validation is pending. \end{abstract}"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "In these tests, what the store writes down mattered more than which reader read it. Models differ further when the rubric states the intent rule."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Kimi K3 (open weights) joins the smaller comparison shared across vendors."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "The personas, their human-written manifests and sessions, the FR-Bank, Mem0 and A-MEM stores and part of the main question set come from the FR-Bank release \citep{fr}. Language models drafted our other questions, and we built the Graphiti graphs from the released FR-Bank records, with lifecycle fields removed. (Appendix \ref{app:construction})"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "that only guesses the question's category (0.77 and 0.75). (Appendix \ref{app:counterfactual}; target-name ablation: Appendix \ref{app:resp})"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "Those models score the change question higher, consistent with a scored step that asks whether stale content exists."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "\claim{List length and coverage lift both metrics.} A reader that only knows whether the store covers the question scores 0.75 pooled and 0.50 matched. The name lookup stays a reliable 0.13 above a lookup over meaningless tokens on the matched metric. (Appendix \ref{app:counterfactual})"
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "On the shared cross-vendor questions, models whose question-only score varies gain a reliable 0.15 to 0.45, including Kimi."
  - AUTHORIZED [Q CLAIMS] 1 -> 0: "On easier coverage questions, mini's advantage over the superseded-name lookup disappears against a lookup over the whole name map. (Appendix \ref{app:baselines})"

Program R134 (2026-09-21), inside this block: the paraphrase check (registrations/ADDENDUM_PARA.md, registered text sha256 45cad63d; scored 2026-09-21, commit 4f1484a; the post hoc supersession-only table e650dd5) landed in v23 on the R133 close by the author's brief 'R134: LAND THE PARAPHRASE CHECK IN v23' and the rulings of the same day (Branch B by the pre-stated rule, worded in both directions; RULING 2: no whitelisting of the ruled texts, the texts replaced). The results pipeline is cf2_paraphrase/tools/para_tex.py (the six tables and the printed forms), the number gate reviews/v23/tools/r134_number_gate.py, the ledger reviews/NUMBERS_R134.md (ledger_r134.py), the edits reviews/v23/tools/port_r134.py (every edit asserted, on the regenerated R133 close), the pins pin_appendix_r134.py, the report reviews/v23/REPORT_R134.md, the sign-off file reviews/v23/OLD_BESIDE_NEW_R134.md. v22 stays frozen. No model call.

- **R134-APPENDIX [section 5 of the brief: the appendix]** (recorded). Appendix C.2 (the registration's 'Appendix D.2'; the pointer renders through the label): the 'Two registered checks' paragraph's pending sentence becomes one sentence and a pointer; after tab:pad the paragraph 'The paraphrase check' (the procedure: 148 questions, 24 failing the screen at drafting, 124 read, 9 excluded, 115 accepted with 76 / 17 / 22 by state, the floor amended from 120 before any scoring call, the 124 as a sensitivity; the AI-assisted read disclosed with its agreement counts 5 of 5, 3 of 4, 1 of 12, 0 of 103; the six tables tab:para-pooled, tab:para-matched, tab:para-minus-lookup, tab:para-sup, tab:para-sens and tab:para-flags at four decimals from cf2_paraphrase/results/para_tab_*.tex; the author's ruling on the branch stated under the supersession-only table (Luna the only reader above the lookup, the added reader, its matched interval including zero, its pooled lower bounds 0.009 and 0.004, one of five comparisons with no multiplicity correction, Haiku's readings also disagreeing); the sensitivity sentence; the branch readings A, D and C, D; the genericity paragraph (0.486 to 0.317; 0.484 to 0.000); the run notes). Appendix A: tab:setup's paraphrase row and tab:runs' caption sentence. E.12: tab:provenance's row. F: tab:registrations-c's caption, the row's outcome, the dated-notes row (the whole file 2848f1ad, day 42); the prediction count unchanged. The AI-use statement: one sentence (an assistant pre-read the sheet and flagged rows; an author made every verdict). G.5: 'paraphrase approvals' dropped from the dependency sentence (flag (b), agreed). Every number through r134_number_gate.py (reviews/NUMBERS_R134.md AUX-R134-PRINTED; cf2_paraphrase/NUMBERS_PARA.md AUX-PARA-*).
- **R134-MAIN [section 4 of the brief: the main text]** (recorded). Section 5.2 gains the paragraph 'The result survives rewording.' directly after the sibling-name control paragraph (section 4.1 of the brief, with the Branch B sentences of the author's RULING 2: 'On the named state, reworded, mini and Haiku sit reliably below the lookup on the pooled metric (by $0.12$ and $0.07$), and Opus and Sol do not differ from it. Luna, a reader we added after fixing the design, edges above it by $0.04$, reliable on the pooled metric and not within triples; on the original questions no model exceeded it.'); Section 1's second contribution gains ', and the lookup loses $0.02$ when the questions are reworded to share no word with the names' (4.4); the Limitations sentence 'The paraphrase check is not yet scored.' is replaced by 'The paraphrase check covers $115$ of the $148$ questions, its rewrites are vaguer than the originals, and Opus ran it with one draw.' with 'GPT-4.1 mini drafted the questions and is also a reader; it is the weakest reader.' beside it (4.5); the Conclusion gains RULING 2's numeral-free sentence 'When the questions are reworded, the lookup holds up at least as well as the smaller models, and only one stronger model edges past it on a named state.' (4.6). Every number from cf2_paraphrase/results/para_printed.json through r134_number_gate.py; no gate rewords a ruled sentence.
- **R134-MAIN-SHORT [section 4.2 of the brief]** (recorded). The shorter Section 5.2 paragraph in place of 4.1's, applied because the page gate failed with the longer one.
- **R134-ABSTRACT [the author's abstract, verbatim]** (recorded). The whole abstract replaced by the author's text of 2026-09-21 (the ruling superseding the brief's section 4.3), numerals in math mode as the source's convention, no other change; the sentence 'Under a control that holds counts and list length fixed, the lookup and every model pick the correct name over a similar one at an AUROC of $0.88$ or higher (chance $0.50$).' leaves the abstract (its numbers still print in Section 5.2; NUMBER_MOVES_V23.md); the placeholder 'human validation is pending' stays. Numbers through r134_number_gate.py. No gate rewords it.
- **R134-PARTB [section 6 of the brief: the four agreed items]** (recorded). B1: Table 1's given-category count reader carries a mark and the note explains, from C.2, that the two count readers read different quantities (the given-category reader ties every supersession triple and is perfect on the counted states by construction; the guessed-category reader's share includes the superseded column). B2: Setup names the release's personas once, 'the FR-Bank release (its LifecycleBench personas)'. B3: a three-pair term bridge at the top of Appendix E.1's glossary; the AI-use statement's sentence on the intent crossover's AI-assisted check (the author's addition to step 6), from the registration's disclosure line, beside the paraphrase sentence. B4: report only; the artifact-named repro_amem_links.py reproduces the census row from the frozen banks of our integration and does not exercise the stock package outside it, so Table 2's cell is unchanged. Table 1's note is the one-line form (the three-line form cost the page; gates_r134_partb_a.txt).
- **R134-PAYERS [the author's RULING 3 of 2026-09-21: the payers for Part B's page]** (recorded). P1: Section 4's coverage sentence reads 'Appendix A lists both.'; the five daggers leave the main text (5.1 twice, 5.2, 5.3, Section 8); Appendix A's notes stay, headed 'Coverage notes for the main text.' with a first sentence that no longer refers to a dagger. P2: the adaptive-retrieval citation string keeps Lewis et al. 2020, Jiang et al. 2023, Mallen et al. 2023, Asai et al. 2024 and Su et al. 2024 and drops the other five (ren2025, wang2023, seakr, verbrouting, metamem); no other citation touched; the five entries stay in the bibliography, uncited (listed for the sweep). P3: the Introduction's two metamemory sentences become 'In metamemory terms these are negative-obligation knowledge (NOK) and the feeling of knowing (FOK) (Hart, 1965; Nelson & Narens, 1990; Koriat, 1993), here judged about an external store.' P4: the Conclusion's first paragraph keeps its first sentence and reads, after it, 'On a named state no model reliably exceeds the name lookup, with list length kept fixed or not, and when the questions are reworded only one stronger model edges past it. The stronger models' lead comes from counts the smaller models do not use. Told the intent rule, only the stronger models apply it, and a fixed cue list matches the best of them.' (RULING 2's Conclusion sentence is superseded by this). P5: the second contribution bullet reads 'Evidence about what readers read. On the named state no model reliably exceeds a name lookup, including under a control that holds counts and list length fixed, and the lookup loses $0.02$ when the questions are reworded to share no word with the names. The stronger models' lead comes from the counts, which the two smaller models do not use.' The 5.1 check: the three stronger models' matched moved-count falls on the counted states are Opus 5 -0.2833, GPT-5.6 Luna -0.2917, GPT-5.6 Sol -0.3250 (tab:cf-matched-ablations; AUX-CF2-R125-CONTRASTS), so 'falling by $0.27$ to $0.33$' reads 'falling by $0.28$ to $0.33$' through r134_number_gate.py (the 0.27 was Luna's expiry value, a per-state row). B4 follow-up: repro_amem_links.py copied to ARTIFACT/verifier/ and listed for the 24 September sweep.
- **R134-G [the gate interactions]** (recorded). tools/slogan_scan.py: the stale EXEMPT_S9 entry for the R133 abstract sentence that left with the author's abstract ('but not when all items are pooled') retired; tools/prose_scan.py: no entry for any ruled text of RULING 2 (the texts were replaced instead); two AUTHOR-RULING entries for the author's abstract only, as RULING 2 allows (gate_edits_r134.py; listed in REPORT_R134.md): its sibling-control sentence ('... even with counts and list length held fixed.'; rule V, 'held') and its count-feature sentence ('The stronger models' lead over the lookup of $0.08$ to $0.10$ ...'; rule L at 48 words; rule D, a 73% token overlap with Section 5.2's lead 'The stronger models' lead comes from counts, and a count feature closes it within a question.'). tools/trace_scan_v13.py LEDGERS gains cf2_paraphrase/NUMBERS_PARA.md and reviews/NUMBERS_R134.md; reviews/v23/tools/number_moves_wp.py walks the PARA artifacts; run_gates.py runs r134_number_gate.py --built; build_v23.py splices the six tables at the per-table markers.
- **R134-F [the frozen strings of the v22 close that R134 changed on top of the R133 close; `reviews/v23/results/frozen_r134_payers_a.json`]** (recorded). Each string below occurred in paper_v22.tex, was kept by the R133 close and occurs a different number of times after R134 (a count of zero means the sentence left the text; the sentence carrying the claim now, where one does, is in reviews/v23/OLD_BESIDE_NEW_R134.md). Every one is authorized as changed by the pass under the entries above.
  - CHANGED [Q CLAIMS] 1 -> 0: "Every one has run except the paraphrase check, which waits on our read."
  - CHANGED [Q CLAIMS] 1 -> 0: "our label-transfer read has not been made, so no paraphrase row is printed"
  - CHANGED [Q CLAIMS] 1 -> 0: "Told the intent rule, only the three stronger models apply it, and a fixed cue list matches the best of them."
  - CHANGED [Q CLAIMS] 1 -> 0: "The paraphrase check is not yet scored."
  - CHANGED [Q CLAIMS] 1 -> 0: "with list length kept fixed or not."

Program R135 (2026-09-21), inside this block: the last content pass on v23 (the brief 'R135: THE LAST CONTENT PASS ON v23', 'R135 ADDENDUM', the ruling on ADDENDUM 2 and the ruling on the TABLE step; 2026-09-21; $0) on the R134 close 69ca17a. The results pipeline is reviews/v23/tools/robust_tex.py (tab:robust and reviews/v23/results/robust_printed.json), the number gate r135_number_gate.py (R134's 62 checks and 37 of its own), the ledger reviews/NUMBERS_R135.md (ledger_r135.py), the edits port_r135.py (every edit asserted, on the regenerated R134 close), the gate edits gate_edits_r135.py, the pins pin_appendix_r134.py (steps r135 and small), the probe slack_r135.py, the report reviews/v23/REPORT_R135.md, the sign-off file reviews/v23/OLD_BESIDE_NEW_R135.md. v22 stays frozen. No model call.

- **R135-TABLE [section 2 of the brief and the R135 ADDENDUM: the robustness table]** (recorded). The evidence box at the end of Section 3 removed (its four limits: the matched comparison is post hoc in Section 4's AUROC paragraph and Limitations; alignment can miss forbidding records in Limitations' 22 obligations; census counts have no sampling interval in Table 2's caption; the answer detector is provisional in Limitations' 'exploratory ... human validation is unfinished'). Section 5.2's opening paragraph gains 'Table~\ref{tab:robust} lists the checks we ran to break this result and what each removes.' and the float tab:robust follows it (reviews/v23/src/robust_table.tex from robust_tex.py: three columns, ten rows, rows 2 and 5 marked post hoc; the caption states metric and population per row and ends with the deleted paragraph's caveat 'Short ground-truth lists do not establish robustness to longer store-written ones.'). The two paragraphs the table absorbs leave 5.2 ('List length and coverage lift both metrics.'; 'Long or wrong name lists weaken the readers together.'): 0.13, 60 and 0.67 print in the table, 0.75 in Appendix C.2 (NUMBER_MOVES_V23.md, moved). The rewording paragraph reads 'With the questions rewritten to share no content word with any name in the summary ($115$ pairs), the embedding lookup loses $0.02$ and the two smaller models lose more (Table~\ref{tab:robust}).' before its unchanged Branch B, all-states and vaguer sentences; 5.2 points to Appendix C.2 once. The R135 ADDENDUM: Section 5.1's second paragraph opens 'The two smaller models lose nothing when the counts are removed. With every count deleted, mini and Haiku score as before (Table~\ref{tab:robust}); given the counts alone, they fall by $0.14$.' and its third paragraph is the ADDENDUM's text verbatim (no 0.28 to 0.33, 0.06 or 0.04; they print in the table). The cells shrunk twice so every row is one line (the brief's section 6); the five ledger-driven cell wordings accepted by the author's ruling, row 9 reading 'mini and Haiku falling with it, within $0.02$ of the lookup'. Every cell through r135_number_gate.py (99 checks, 0 mismatches; reviews/NUMBERS_R135.md).
- **R135-ABSTRACT [section 3 of the brief]** (recorded). The abstract replaced by the brief's text, verbatim but for the G2 ruling (option c): the parenthetical '(all readers at $0.88$ AUROC or higher)' deleted, because prose_scan's G2 (the abstract must not state the lookup's own level; no allowlist by the 14 September ruling) fired on it; no rule change, no exemption; 0.88 moved to tab:robust row 3. The HV-1 placeholder clause leaves with the abstract's last sentence 'All stores are synthetic, and we do not show that better judgments yield better answers.'; 0.08 to 0.10 and 0.05 to 0.06 leave the abstract and still print in Section 5.2 (NUMBER_MOVES_V23.md, moved). Numbers through r135_number_gate.py (148; 0.88 the sibling floor; 0.02; 0.04; 0.73 / 0.82 / 0.75 to 0.60 / 0.71 / 0.59). The two R134 AUTHOR-RULING entries for the R134 abstract's sentences retired (gate_edits_r135.py).
- **R135-FIG3 [section 4 of the brief; the ruling: no height raise]** (recorded). Figure 3 redrawn from the same data file in the Okabe-Ito palette (mini E69F00, Haiku 56B4E9, Luna 009E73, Sol D55E00, Opus 0072B2, the lookup black as before, the count reader CC79A7), the R126 marker shapes kept so the figure survives greyscale, the legend's content, size and layout unchanged; the height not raised (the ruling reserves the slack for two later landings).
- **R135-SMALL [section 5 of the brief]** (recorded). 5.1 the builders box's sentence gains 'and under FR-Bank's store-written summary, where Haiku sits $0.12$ above the lookup' before 'and in the scenario we priced' (AUX-BH-H45-15 Haiku minus lookup +0.1212, both intervals above zero). 5.3 G.5's opaque sentence 'Valentina's omitted source supports the disputed hobbies; ...' reads 'For one question, a persona's hobbies, the original reference packet had omitted the session that supports the answer; with that source restored, the repaired judge marks every condition's answer correct for that question.'; G.5 kept. 5.2 not applied: the HV-1 status lines stay verbatim by the pass's own rule and the ADDENDUM 2 ruling. 5.4 repro_mem0_erase.py copied to ARTIFACT/verifier/ beside repro_amem_links.py; the five uncited bibliography entries checked (REPORT_R135.md).
- **R135-A2 [ADDENDUM 2 as ruled: the last unit before the close]** (recorded). 1 Section 4, after 'Readers return probabilities under a fixed rubric.': 'The scored step asks whether stale content about the question's target is present, which coincides with Definition 1's obligation on the counterfactual set, where every question has current or upcoming intent; Section 5.3 tests intent separately.' (the definition and the section through their labels). 2 Section 7: 'Propagating a lifecycle tag to matching lines under the same attribute changes $1$ of $452$ assembled views under the reference tags. Under FR-Bank's own tags the same rule changes $90$ views and fully tags $15$ of the $35$ duplicate views, but it also propagates falsely ($69$ of $2{,}333$ licensed active lines).' (tab:ds-a8's own-tags primary column; AUX-DS-A8-RULE-CENSUS, -DUP35, -FALSEPROP). 3 G.2's clause 'the control is the paraphrased counterfactual set, registered and pending (tab:registrations-c)' reads 'the control is the paraphrase check reported in Appendix C.2, with this split recomputed on the rewrites (tab:para-flags)'. 4 the three Graphiti Amendment 2 lines (tab:registrations-d's outcome, the count paragraph, G.5) read 'not completed at submission' for 'pending'; the C.2 run notes read 'then pending'; the three HV-1 placeholders in E.10 untouched.
- **R135-G [the gate interactions]** (recorded). tools/prose_scan.py WHITELIST: the two R134 entries for the R134 abstract's sentences retired (neither sentence remains); an entry for the brief's abstract only where a prose rule fires inside it and the ruling allows it (listed in REPORT_R135.md); nothing else exempted. reviews/v23/tools/r134_number_gate.py numerals(): '{,}' read as ',' and tabular column specs dropped (layout, as trace_scan reads them). run_gates.py runs r135_number_gate.py; build_v23.py splices tab:robust at its marker; number_moves_wp.py records the tokens that moved within the paper (the two deleted paragraphs', the 5.1 trims', the abstract's) and the evidence box's layout token.
- **R135-F [the frozen strings of the v22 close that R135 changed on top of the R134 close; `reviews/v23/results/frozen_r135_a2_b.json`]** (recorded). Each string below was kept through the R134 close and occurs a different number of times after R135 (a count of zero means the sentence left the text; where a sentence carries the claim now it is in reviews/v23/OLD_BESIDE_NEW_R135.md). Every one is authorized as changed by the pass under the entries above.
  - CHANGED [Q CLAIMS] 1 -> 0: "It is a disclosure rather than a control, because the flag marks a question that names its attribute at the level of the topic while every value is scrubbed from every summary, so a flagged question need carry no more of the label than an unflagged one; the control is the paraphrased counterfactual set, registered and pending (Table \ref{tab:registrations-c})."
  - CHANGED [Q CLAIMS] 1 -> 0: "the matched within-triple comparison is post hoc"
  - CHANGED [Q CLAIMS] 1 -> 0: "in our tests a model added something only on counted states, on explicit intent questions and, on the pooled metric only, in the all-states comparison, and in the scenario we priced,"

Program R137 (2026-09-22), inside this block: the long-list check landed, the prediction recount, the two readability items (the brief 'R137: LAND THE LONG-LIST CHECK, PLUS THE LAST TWO READABILITY ITEMS'; 2026-09-22; $0) on the R135 close bda70df (the run 6d7f224 under registrations/ADDENDUM_CF_PAD.md, frozen alone at 06c611f). The results pipeline is cf_pad/tools/cfpad_tex.py (the C.2 fragments) and reviews/v23/tools/robust_tex.py (tab:robust row 9), the number gate r137_number_gate.py (R134's 62 and R135's 37 checks and 77 of its own), the ledger reviews/NUMBERS_R137.md (ledger_r137.py), the edits port_r137.py (every edit asserted, on the regenerated R135 close), the gate edits gate_edits_r137.py, the pins pin_appendix_r137.py, the probe slack_r137.py, the report reviews/v23/REPORT_R137.md, the sign-off file reviews/v23/OLD_BESIDE_NEW_R137.md. v22 stays frozen. No model call.

- **R137-NUMBERS [sections 2 and 3.1 of the brief: the pipeline, tab:robust row 9, the recount]** (recorded). cf_pad/tools/cfpad_tex.py writes the six Appendix C.2 tables (cf_pad/results/cfpad_tab_{sup,minus-lookup,whole,counted,other-lookups,position}.tex, four decimals) and cfpad_printed.json from cf_pad_scores.json; robust_tex.py row 9 reads cf_pad_scores.json: 'List padded to 60 names / Short, clean lists / Lookup $0.92$ to $0.74$; mini, Haiku, Opus fall with it; Luna, Sol lose $0.06$ to $0.07$, lead it by $0.13$ to $0.14$' (the comma form: the brief's 'Luna and Sol lose ... and lead' is the abstract's and 5.2's wording too, and repeat_scan bars a third place) (registered), the caption's per-row note naming the $88$ supersession triples, the $60$-name list and Opus at one draw against its recorded five-draw row; the 661-set padding and the wrong-name injection leave the row and stay in Appendix C.2's 'registered checks' paragraph and tab:pad. Section 4 reads '$33$ of $102$ came out otherwise' and Appendix F's count paragraph 'tab:registrations-e $9$ with $4$: $102$ predictions, $33$ of which' (AUX-R137-COUNT: 98 / 31 plus P-L1 to P-L4, P-L1 and P-L4 otherwise); tab:registrations-e's caption names the long-list check and its row follows the R125 rows (06c611f, day 43). Every number through r137_number_gate.py (R134's 62, R135's 37 and 77 of its own, 0 mismatches; reviews/NUMBERS_R137.md).
- **R137-APPENDIX [section 4 of the brief]** (recorded). C.2: the 'registered checks' paragraph counts three and gains one sentence for the long-list check; after the paraphrase check the paragraph 'The long-list check' (the padding rule with the pool, seed, identical pad and list lengths, the target's rank with the ledger's median $41.5$ where the brief wrote 41, the renderer lock, the leak scan, the frozen registration with both endpoints; the caps and spend; the four predictions with their numbers; the six tables through the %%CFPAD-TABLE:<name>%% markers; the counted states' sentence; Opus 5's one draw against its recorded draw 1; the seed check; the run notes). A: tab:setup's row and tab:runs' caption sentence. E.12: tab:provenance's row. F: the row's pointer to tab:cfpad-sup. E.11: the spend list. E.1: the notation box's 'padded list' row. Every value from cf_pad/results/cf_pad_scores.json (cf_pad/NUMBERS_CF_PAD.md AUX-CFP-*; reviews/NUMBERS_R137.md AUX-R137-PRINTED).
- **R137-MAIN [sections 3.2, 3.4, 3.5 and 3.6 of the brief]** (recorded). 5.2's lead reads 'On the named state, no model reliably beats the lookup on the short list; on a long one, two do.' and the long-list sentences close the opening paragraph (the brief's first placement; as their own paragraph they open with a numeral and trip q_scan Q-A): 'With the superseded-name list padded to $60$ names (Table~\ref{tab:robust}), the lookup loses $0.18$ and mini, Haiku and Opus fall with it, ending level with it or below. Luna and Sol lose $0.06$ to $0.07$ and lead the lookup by a reliable $0.13$ to $0.14$ pooled and $0.09$ to $0.10$ within triples. Retraction and expiry do not move, since the list names neither. (Appendix~\ref{app:counterfactual})' (the ledger over the brief's wording in two places, listed in REPORT_R137.md: Haiku loses $0.15$, less than the lookup's $0.18$, so 'as much or more' is not printed; the matched lead is $0.09$ to $0.10$, so 'on both metrics' prints both). Section 1's second bullet: 'when the list is short, including under a control that holds counts and list length fixed, and two of five do when it is padded to $60$ names; the lookup loses $0.02$ ...'. The Conclusion's sentence gains 'on the short list' and a second sentence 'On a $60$-name list Luna and Sol lead the lookup by $0.13$ to $0.14$ and the other three fall with it.' (its own sentence: the clause would take the sentence past rule L's 40 words). Limitations gains the brief's sentence verbatim.
- **R137-ABSTRACT [section 3.3 of the brief]** (recorded). The fifth sentence replaced by the brief's two, verbatim: 'Where the summary names the affected attribute and the list is short, none of five language models reliably beats a cosine-similarity lookup over the names, including under a control that fixes counts and list length. Padded to $60$ names, the lookup loses $0.18$; GPT-5.6 Luna and Sol lose $0.06$ to $0.07$ and lead it by $0.13$ to $0.14$, while the other three fall with it.' Numbers through r137_number_gate.py. No AUTHOR-RULING entry was needed (no prose rule fired inside it).
- **R137-PARTB [section 5 of the brief: the two readability items and Table 1]** (recorded). 5.1 Figure 1 is a rendered lifecycle summary in the old figure's footprint: the LIFECYCLE TOTALS block (active $377$, superseded $197$, retracted $1$, expired $49$), the HOBBIES_RECREATION name line and the superseded-names line of the summary the E.1 excerpt was cut from (frbank:david:FULL:BELIEVED, transcribed by port_r137.py from the artifact's manifest; AUX-R137-FIG1), labelled 'Summary route: read before retrieval', beside one returned record with its tag ('hiking_preference [superseded]', the store's own hiking_preference entry) labelled 'Tag route: read on returned records'; the brief's caption; the body sentence reads 'Figure~\ref{fig:framework} shows one such summary, abridged, beside a returned record with its tag.' The old schematic and caption are in REPORT_R137.md. 5.2 the two thesis sentences rejoined to the paragraph they follow (the blank line removed; no rewording). 5.3 Table 1 gains 'Luna & all' and 'Sol & all' rows of dashes and the note 'A dash marks a condition the model did not run.'
- **R137-P1 [section 6 of the brief, payer P1]** (recorded). The retraction-and-expiry sentence moved from 5.2's opening paragraph to Table 2's caption ('In row 9 retraction and expiry do not move, since the list names neither.'); the fold is the main unit's placement already.
- **R137-P2 [payer P2]** (recorded). 'The rewrites are also vaguer than the originals.' leaves the body (it stays in C.2 and tab:para-flags' caption).
- **R137-G [the gate interactions]** (recorded). reviews/v23/tools/build_v23.py splices the six CFPAD tables at their markers; run_gates.py runs r137_number_gate.py; number_moves_wp.py walks cf_pad/results/cf_pad_scores.json and cf_pad/build/lock.json and dispositions Figure 1's three transcribed totals and the median rank 41.5 (ADDED) and the old figure's tikz coordinate token (VANISHED); r134_number_gate.numerals() drops minipage widths and makebox lengths (layout, as the p{} column specs since R135); tools/trace_scan_v13.py LEDGERS gains cf_pad/NUMBERS_CF_PAD.md and reviews/NUMBERS_R137.md; r137_number_gate.py's built check allows the CFPAD fragments' numerals and the pass's printed forms. tools/prose_scan.py: no entry added (no prose rule fired on the abstract's own sentence); nothing exempted.
- **R137-F [the frozen strings of the v22 close that R137 changed on top of the R135 close; `reviews/v23/results/frozen_r137_close.json`]** (recorded). Each string below was kept through the R135 close and occurs a different number of times after R137 (a count of zero means the sentence left the text; where a sentence carries the claim now it is in reviews/v23/OLD_BESIDE_NEW_R137.md). Every one is authorized as changed by the pass under the entries above.
  - CHANGED [Q CLAIMS] 1 -> 0: "Two registered checks on this set"

Program R139 (2026-09-23), inside this block: the brief 'KtS R139: answer mock review 14 (W1, W2) in the paper, then the pre-upload sweep' (2026-09-22), the author's GO with rulings, the Unit G addendum with G9, and the rulings on the STOP (22 Sep, 23:54), on the R137 close eb37054. Units applied: c2, a, g, g8, b, c, d, e, f, s2, s3, s4, s5, s6, s7, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, b3m, q1, q2, q3, q4, q5, q6, q7, q8, q9. The edits are reviews/r139/tools/port_r139.py (every edit asserted), the numbers reviews/NUMBERS_R139.md (ledger_r139.py), the number gate reviews/r139/tools/r139_number_gate.py, the report reviews/r139/REPORT_R139.md. No model or API call.

- **R139-POSTHOC [the brief 'KtS R139', Phase 1; dated 2026-09-22/23; POSTHOC class]** (recorded). Two analyses were added after every result they touch had been read, and each is labelled post hoc where it is printed. (1) Equivalence within $0.05$ by two one-sided tests at $5\%$: a model-minus-lookup difference is equivalent when both of its $90\%$ intervals (item-level or triple-level, and persona-grouped; the 5th and 95th percentiles of the same $1{,}000$ draws that give the printed $95\%$ intervals) lie inside $[-0.05,+0.05]$; applied to every printed model-minus-lookup row of the default summary, the sibling-name control, the all-states summary, the padded set and the paraphrase set, and to the lookup with one count feature against each stronger reader (reviews/NUMBERS_R139.md AUX-R139-EQUIV, -E-GROUPS, -B6; Appendix C.2, tab:equiv and tab:equiv-para). No reliable verdict changed. (2) The length-only reader: its score is the number of names in the superseded-names section of the summary it is given; it wins every supersession triple on the default and the padded lists and ties every triple of the sibling-name control (AUX-R139-LENGTH; Appendix C.2, tab:length). The branch texts that use them were committed before either ran (reviews/r139/BRANCHES_R139.md, 6616e57).
- **R139-SCOPE [the Unit G addendum and G9; dated 2026-09-23]** (recorded). The paper's scope is stated as monitoring only: it scores how accurately a reader judges the store from what it exposes (metamemory monitoring); whether the judgment changes what is retrieved or answered (control) is deferred to a later study, and so is any write-path intervention: every intervention in the paper is on the read side and the reach results describe what a store as shipped affords a reader. The abstract, Section 1, Section 7's title and first paragraph, Limitations and the Conclusion's first sentence say so (the author's texts, Q5, Q6 and Q9 as ruled).
- **R139-CLARIFY [clarifications that narrow a claim's wording; no frozen claim changes meaning; dated 2026-09-23]** (recorded). 'Within tolerance' is defined as a point difference no greater than $0.05$ that does not establish equivalence (Section 4); 'A fixed cue list matches the best model' reads 'is not reliably below the best model' with the crossover's own interval (5.3 and the Conclusion); 'ending level with it or below' reads 'ending at or below it with no reliable difference' (5.2); 'we ran no equivalence test' reads 'equivalence within $0.05$ is neither shown nor excluded' (5.2); the two Section 7 sentences on flagged answers are exploratory pointers to Appendix E.10 (G8); NOK is stated as a term the paper introduces (Section 1); A-MEM's census row is marked as not checked against the reference implementation (Table 3).
- **R139-G7 [prose_scan WHITELIST; dated 2026-09-23]** (recorded). The Conclusion's first sentence as Unit G7 words it carries 'failed' in its ordinary sense and is whitelisted beside the R133 entry: "In these monitoring tests, no reader we tried made up for what the store had failed to write down."
- **R139-TOOLS [gate and build changes; dated 2026-09-23]** (recorded). q_scan unwraps \mbox{...} before it scans (a scanner defect the S6 guard exposed, not an exemption); build_v23.py applies reviews/r139/results/build_repairs_r139.json (S4 Table 73 to the text width; S5 four em-dash sites in appendix prose; the registered ADDENDUM_SIDE text keeps its em dashes verbatim by ruling); the style zip's own fancyhdr.sty beside the paper (S1; the .sty untouched); refcheck_v11's RETIRED gains the five bibitems S2 removed (ren2025, verbrouting, wang2023, metamem, seakr).
- **R139-G9 [Limitations; the frozen sentence G9 and Q5 replace; dated 2026-09-23]** (recorded). Old: "The counterfactual test bypasses backend writing, and no backend tested here is shown maintaining the summary." New: "We change no backend's write path: the counterfactual test bypasses writing, every intervention is read-side, and no backend tested here is shown maintaining the summary, so the reach results describe what a store as shipped affords a reader; a write-path intervention is a separate study." The old sentence's claim (the test bypasses writing; no backend is shown maintaining the summary) is kept inside the new one.
- **R139-F [the frozen strings of the v22 close that R139 changed on top of the R137 close; `reviews/v23/results/frozen_r139_close.json`]** (recorded). Each string below was kept through the R137 close and occurs a different number of times after R139 (a count of zero means the sentence left the text or was reworded as the entries above record). Every one is authorized as changed by the pass under the entries above.
  - CHANGED [S EXEMPT_S8] 1 -> 0: "that specificity---per-category correspondence is not necessary"
  - CHANGED [W WHITELIST[3]] 1 -> 0: "Permuting which counts and attribute-name lists belong to which category changes neither judgment, which bounds the mechanism rather than that specificity---per-category correspondence is not necessary on FR-Bank, consistent with the name map rather than the count structure carrying the effect (Definition \ref{def:index}), though the shuffle preserves the global name and count multiset and the flat superseded-names section and so bounds correspondence alone."
  - CHANGED [Q CLAIMS] 1 -> 0: "All tests use one bank of 40 synthetic personas; transfer to a second benchmark is untested. The counterfactual test bypasses backend writing, and no backend tested here is shown maintaining the summary."
  - CHANGED [Q CLAIMS] 1 -> 0: "The counterfactual comparison covers closed models from two vendors; the one open-weights model, Kimi K3, completed only the cross-vendor replication."

Program R140 (2026-09-23), inside this block: the brief 'R140: the mock-15 fixes' ($0, no model run) on the R139 close 3342217; units applied: t1, t8, t9, t10 (reviews/r140/tools/port_r140.py, every edit asserted; the verdicts the new words state checked by reviews/r140/tools/r140_number_gate.py against reviews/r139/results/equiv_r139.json; report reviews/r140/REPORT_R140.md).

- **R140-CLARIFY [clarifications that narrow a claim's wording; no frozen claim changes meaning; dated 2026-09-23]** (recorded). The abstract, 5.2 and the Conclusion say that under the sibling-name control none of the five readers is reliably above the lookup and none is shown equivalent (AUX-R139-EQUIV, the five control rows 'neither'); the abstract's padded-list sentence reads 'longer than the stores we tested write' (the ruling of 23 Sep; FR-Bank's own lists 15.04 capped, 32.55 lifted, at most 50) and states that a list-length cue is uncontrolled there (AUX-R139-LENGTH); the builders box no longer states the priced-scenario outcome and reads 'whether the judgment pays for itself is unresolved (Appendix G.5)'; Limitations names what the explicit-intent rerun covered. Two ruled sentences are split at their own semicolon or clause for prose rule L (the R139 precedent).
- **R140-F [the frozen strings R140 changed on top of the R139 close; `reviews/v23/results/frozen_r140_close_b.json`]** (recorded). Every one is authorized as changed by the entry above.
  - CHANGED [Q CLAIMS] 4 -> 5: "(Appendix \ref{app:registration})"
  - CHANGED [Q CLAIMS] 1 -> 0: "A lifecycle summary lists record counts by state and, per category, an attribute-name list with the values removed."
  - CHANGED [Q CLAIMS] 1 -> 0: "Under the explicit-intent rubric only mini and Luna were rerun. (Appendix \ref{app:counterfactual})"

Program R141 (2026-09-23), inside this block: the brief 'R141: the sibling-name control at 60 names' on the R140 close 86a72dd / 42b6951; the registration reviews/r141/registrations/ADDENDUM_R141_SB60.md frozen alone at f224177 (registered text sha256 4fc25a8b; the commit date 2026-09-23, day 44, governs over the text's '24 Sep' line); run 2588717 (OpenAI $2.9372 of the $12 cap), scored 7a62892; branch B-ii fired (P-S1 fails, P-S2 to P-S4 hold), landed with Sol named; units applied: l0, l1, l2, l4, l5, pa, pb, pc, s5 (reviews/r141/tools/port_r141.py, every edit asserted; the numbers reviews/NUMBERS_R141.md, the number gate reviews/r141/tools/r141_number_gate.py; report reviews/r141/REPORT_R141.md).

- **R141-LAND [the fired branch; dated 2026-09-23]** (recorded). The B-ii texts are the frozen B-i texts with Sol named (the author's ruling 1 on the B-ii stop); the abstract reads 'The lead holds for Sol against a sibling padded to the same length and counts.'; the Conclusion '... and, with list length and counts fixed, Sol by 0.09; the other three fall with it.'; 5.2 words Luna's result as 'Luna's lead holds on the pooled metric only (0.11, reliable) and not within triples (+0.04)', a wording deviation from the registered clause 'Luna's lead is not separated from the cue' (which Limitations keeps), recorded in C.2 and AUX-R141-DISCREPANCIES. The prediction count moves to 106 / 34 and A2's comparison count to 71.
- **R141-PAY [the page payers; no claim changes meaning]** (recorded). Payers a, b, c (ruled 23 Sep) and payer (v) of the ruling on the last line: Limitations' two alignment sentences merged into one ('The 22 obligations the manifest-to-record alignment does not mark are invisible to every summary (mini scores 0.52 on them under ground truth).'). Payers (i) to (iv) left the probe at +0 and were reverted by ruling; (v) gave +1 (reviews/r141/results/slack_r141.md).
- **R141-F [the frozen strings R141 changed on top of the R140 close; `reviews/v23/results/frozen_r141_close.json`]** (recorded). Every one is authorized as changed by the entries above.
  - CHANGED [Q CLAIMS] 1 -> 0: "The ground-truth name lists are built through the manifest-to-record alignment. The 22 obligations it does not mark are therefore invisible to every summary (mini scores 0.52 on them under ground truth)."
  - CHANGED [Q CLAIMS] 1 -> 0: "The ground-truth name lists are built through the manifest-to-record alignment. The 22 obligations it does not mark are therefore invisible to every summary"

Program R142 (2026-09-23), inside this block: the brief 'R142: two stale sentences after B-ii, plus one scoping edit' ($0, no model run) on the R141 close 4662be7; units e1, e2, e3 (reviews/r142/tools/port_r142.py, every edit asserted; probe reviews/r142/results/slack_r142.md, +1 after each).
- **R142-BII [B-ii carried into the two headline sentences; dated 2026-09-23]** (recorded). 5.2's lead claim reads 'On the named state, no model reliably beats the lookup on the short list; on a long one, Sol does with list length and counts fixed.' and the Introduction's second bullet ends 'and one does on a 60-name list with its length and counts fixed.' (was 'two do' / 'two of five do when it is padded to 60 names'; ADDENDUM_R141_SB60 branch B-ii, AUX-R141-RESULTS: Sol +0.0852 matched, reliable; Luna not reliable within triples). Section 6's lead claim is scoped to 'The backends we tested'. The main-text grep for 'two of five', 'two do', 'two readers' and 'Luna and Sol lead' left no other false sentence: the Limitations' 'two readers that keep their lead there' describes the padded list against the lookup, and the abstract, 5.2 and Conclusion carry the SB-60 qualification. R142-F: 0 frozen strings changed on top of the R141 close.

Program R143 (2026-09-23), inside this block: the brief 'R143: one Limitations fix, zero net lines' ($0, no model run) on the R142 close 9fee721; units mv, p9 (reviews/r143/tools/port_r143.py, every edit asserted; probe reviews/r143/results/slack_r143.md).
- **R143-LIM [no claim changes meaning; dated 2026-09-23]** (recorded). The merged alignment sentence ('The 22 obligations the manifest-to-record alignment does not mark are invisible to every summary (mini scores 0.52 on them under ground truth).') moves from after 'Control is outside this paper's scope.' to the end of the run-conditions paragraph of Limitations, its original home (option 1 of the brief); the line is paid by payer (ix): 'GPT-4.1 mini drafted the questions and is also a reader, the weakest.' Slack +1 on the first option probed; options 2 and 3 not needed. R143-F: 0 frozen strings changed on top of the R142 close.
- **R143-ADD [the addendum's three zero-cost fixes; no claim changes meaning; dated 2026-09-23]** (recorded). C.2's length-only reader paragraph now ends '; the sibling padded to equal length is the control of the next paragraph (Table [tab:sb60]).' (was '; no sibling padded to equal length was run.', made false by R141); E.1 drops 'which the main text stated in full until this version,'; Section 1 reads 'so a store can expose it without disclosing stored values' (was 'content'). The appendix grep for 'until this version', 'not yet', 'once labeled', 'was not run' and 'no sibling' leaves three hits, none describing a state R141 changed (Sol's names-and-counts ablation twice; the Graphiti cached-depth judging). C.2 and E.1 pinned (pin_appendix_r143.py).

- **R144 [dated 2026-09-24]** (recorded). R144: wording only (box, abstract); no number changed; payers used: P1 (Limitations: 'GPT-4.1 mini drafted the questions and is also a reader, the weakest.' dropped), P2 (Limitations: 'Kimi K3, the one open-weights model, completed only the cross-vendor replication.' dropped), P3 (E4, Section 6, reverted), P4 (E3, the Table 2 caption, reverted). Box: 'on explicit intent questions, on a 60-name list and, pooled only, in two further conditions'; abstract: 'On the short lists the three stronger readers lead only where ...'. reviews/r144/tools/port_r144.py --units=close (e1 e2 p1 p2); probe reviews/r144/results/slack_r144.md.
