# AMENDMENT 1 to PREREG_E0.md

**Dated:** 2026-08-10 · **Amends:** `PREREG_E0.md` frozen at commit `0f2fde2`, which is
preserved unchanged. **Design basis for the amendment:** `STEP1_REPORT.md` at commit `6552e3e`.

**Statement of prior data contact.** No elicitation call has been made. Zero API calls exist in
`e0_metamemory/` at the time of this amendment. Every input to the three changes below is a
deterministic function of committed artifacts plus direct reading of the persona YAMLs.

**No label produced before this amendment changes as a result of changes 1 or 2.** Change 3
relabels 17 items, and every original label is preserved in the `label_step1` field of
`items.json`.

---

## Change 1 — ABSENT contamination: a sensitivity row, not a relabelling

Labels stay as assigned. **The lexical proxy does not touch the YAML-native arm.**

The 3 ABSENT items flagged by the independent lexical check (`david:david_q11:ABLATED`,
`ingrid:ingrid_q02:ABLATED`, `pan:pan_q10:ABLATED`) are tagged `lex_flagged: true` in
`items.json`. **All gate metrics are additionally computed with those 3 items excluded and
reported beside the primary**, as a pre-registered sensitivity row.

`RESULTS_E0.md` will state the bias structure explicitly:

> Two of the three flagged items are genuine label errors — the store does hold content that
> should shape the answer, but the session-anchored gold set did not see it, so the ablation did
> not remove it. A correctly high FOK on such an item scores as an error against the ABSENT
> label. This **deflates blind FOK AUROC**, which moves the blind arm *toward* satisfying
> H1 (blind AUROC < 0.75) by a bounded, small amount. On the same items it also **deflates the
> indexed arm**, and the indexed arm is the one that would otherwise gain from the index — so
> the contamination pushes *against* H2 (indexed − blind ≥ +0.10). **It cannot manufacture a
> false GO**, because GO requires both, and the two effects act in opposite directions on the
> gate. It can only make a GO harder to reach or a KILL-B easier.

---

## Change 2 — ABSENT mechanism split, reported as a second breakdown

Each ABSENT item carries `absent_mechanism`:

| mechanism | n | meaning |
|---|---|---|
| `ablation` | **59** | the question's gold edges were removed by the category ablation |
| `expiry` | **10** | an AV2 question whose gold answer is itself a negative, and whose *expired* content was removed by the ablation |

Gate metrics are reported for both arms on each subset. **Descriptive only — no pass/fail reads
on the subsets.** This replaces the "ablation-manufactured vs any other ABSENT" breakdown, which
is degenerate here (all 69 ABSENT items are ablation-manufactured; logged as D15).

---

## Change 3 — full per-item verification of PRESENT-NEGATIVE

**Rule: detector proposes, YAML disposes.** All 69 admitted PN items — 166 distinct
(persona, question, admitting-entry) pairs across 44 distinct questions — were read individually
against the YAML record that nominated them, using the same instrument as the committed 30-fire
τ audit. An item is verified iff at least one of its *surviving* admitting entries reads TRUE.
Items failing verification route to **UNRESOLVED**.

Full table committed: `pn_verification_worksheet.md` (what was read) and `pn_verification.json`
(every pair with verdict and reason). Verdicts and their reasoning are in `tools/pn_verdicts.py`.

### Result

| | n |
|---|---|
| (question, entry) pairs read | 166 |
| TRUE | 95 |
| FALSE | 71 |
| **precision of the admitted set** | **57.2%** |
| PN items verified | **52** |
| PN items → UNRESOLVED | **17** |

### The finding that matters: the expiry route, not the detector

Precision of the admitted evidence, by how it was admitted:

| admitted via | precision |
|---|---|
| detector signal = 1.00 | **52/57 = 91.2%** |
| detector signal 0.80–0.99 | **27/29 = 93.1%** |
| **expiry (date-derived)** | **16/80 = 20.0%** |

The τ_hi filter performed as the 30-fire audit predicted — 91–93%, against the audited estimate
of 100% on n=5. **The expiry route did not.** It was pre-registered as "date-derived and exact,
with no threshold" (`PREREG_E0.md` §3), and that description is true about *dates* and false
about *negative obligation*. Two failure modes, neither of which the 30-fire audit could have
caught, because that audit sampled only detector fires at ≥ τ_lo and **never sampled expiry
evidence at all**:

**(e) The YAML record's own `status` is `upcoming`** — 38 pairs across 7 questions
(`elena_q11`, `leila_q06`, `leila_q11`, `rosa_q05`, `samuel_q05`, `tom_q05`, `zara_q06`). The
14-day cutoff derived from the pinned `t_now` marks the event expired, but the authored ground
truth says it has not happened — and in every one of these cases the question's **gold answer is
that very event**. `rosa_q05` alone contributed 15 false pairs. This is the 9-record
YAML-status-versus-derived-cutoff disagreement logged as **D6**, where the resolution recorded
was "the 9 disagreements would go to UNRESOLVED rather than being adjudicated" — a provision the
pre-registration did not carry forward into its expiry rule. Per-item verification caught it.

**(f) The question explicitly asks the store to surface PAST events** — 21 pairs across 3
questions (`lily_q11` "Does Lily have past events?", `pan_q13` "When does Pan's brother finish
his conscription?" with gold "He already finished", `valentina_q13` "Does Valentina have any past
events or deadlines?"). Here the expired content **is** the gold answer; its correct influence is
use, not suppression. Expiry alone cannot distinguish this from a stale-content case — it needs
the question.

Two further FALSE patterns carried over from the 30-fire audit and recurred: (a) the entry states
the transition or its outcome, so it carries the *current* value (`chenoa` lb_00233 "attempted …
but it was rejected by the tribal council" is the retraction, not the retracted plan);
(b) the entry is explicitly past-tense marked (`ingrid` lb_00219 "User's **previous** primary
research focus was Arctic cod"; `mirri` lb_00252 "**planned** to write"; `tom` lb_00216 "**had**
grand plans").

**Expiry sub-rule applied uniformly:** an expiry-nominated entry reads TRUE iff the YAML record's
`status` is `expired` **and** the question seeks current/upcoming state. Pattern (b) does *not*
apply to expiry evidence — expiry evidence is past-tense by nature, and the issue there is stale
dated content being surfaced as current, not the entry's grammar.

### Status of τ_hi

**τ_hi = 0.80 is now a candidate filter only.** Its n=5 and one-item-cliff caveats
(`PREREG_E0.md` §4) are **superseded by per-item verification**: every admitted item has been
read individually, so the label set no longer rests on the audited threshold. τ_hi's retained
role is to bound how much evidence had to be read. Its measured precision on the full set
(91–93%) is reported as a validation of the original audit, not as a label warrant.

---

## Revised census

| cell | Step 1 | after Amendment 1 |
|---|---|---|
| PRESENT | 89 | **89** |
| ABSENT | 69 | **69** |
| PRESENT-NEGATIVE | 69 | **52** |
| UNRESOLVED | 283 | **300** |
| scoreable | 227 | **210** |

PRESENT-NEGATIVE subtypes: 43 with-replacement, 9 without-replacement.

| gate | result |
|---|---|
| ABSENT ≥ 60 | **PASS** (69) |
| PRESENT ≥ 60 | **PASS** (89) |
| PRESENT-NEGATIVE ≥ 60 | **FAIL** (52) — accepted; NOK is exploratory and ungated |

No escalation to 30 personas is triggered: the escalation condition is ABSENT < 60, and ABSENT
is unchanged at 69.

---

## Unchanged by this amendment

Hypotheses, gate logic, persona selection, ablation categories, store variants, pinned `t_now`,
the gold resolver (YAML-native for gates, lexical proxy as an ungated sensitivity arm, judged
cache excluded from labels), the index specification and its tightening ladder, the
index-leakage control and its 3/30 threshold, the elicitation prompts and their sha256, the
model and decoding parameters, the metric definitions, and the bootstrap specification.

**D10** — the τ_hi grid extension — stands as logged and will appear in the **main deviations
table of `RESULTS_E0.md`**, not an appendix.
