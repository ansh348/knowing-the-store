# M1 — NOK THREE-FIX FACTORIAL (mini-prereg, one page)

**DRAFT. Freezes with `PREREG_E2.md` at SP1 if it rides. No call may precede that commit.**

## Question

E1's NOK result changed three things at once relative to E0's null. `prompts_e1.py` names them:

| factor | E0 (off) | E1 (on) |
|---|---|---|
| **L — lifecycle signal in the index** | index carried none | index v2 carries per-category active/superseded/retracted/expired, supersession-event counts, and the **superseded-attribute-names block** |
| **W — worked examples** | "negative obligation" defined, never shown | two worked examples, drawn from out-of-scope AV8 |
| **D — two-step decomposition** | one probability collapsed detection and quantification | `nok_candidates_found` first, then `nok` |

E0 NOK: 0.4909 → 0.5320, **+0.0411**. E1 NOK: 0.4946 → **0.7339**, **+0.2393**. Something in those
three moved the delta by ~0.20 and we do not know which.

## Design

**Full 2³ = 8 cells**, no fractional design and therefore no confounding to state. FR-Bank scoreable,
**661 items × 8 = 5,288 mini calls ≈ $2.75** — the projection permits it, so the fractional fallback
is not used. Blind arm reused from E1 (already committed) as the common reference.

Frozen decoding: `gpt-4.1-mini`, temperature 0, seed 42, k=1 (licensed by the lane's 46/50 k=3
stability). Cache keyed `(item_id, cell, model, prompt_hash)`.

**Factor realisation, so "off" is unambiguous:**
- **L off** = the index with the four lifecycle-total lines, the per-category lifecycle columns, and
  the superseded-attribute-names block removed; **everything else byte-identical**, using E1.8's
  count-site machinery so the edit is provably confined.
- **W off** = the two worked-example paragraphs deleted from `SYSTEM`; nothing else touched.
- **D off** = the response schema drops `nok_candidates_found`; `nok` is asked for directly.

**Endpoint:** NOK AUROC (positive = PRESENT-NEGATIVE) and its delta over the E1 blind NOK arm.
Main effects and all interactions by the standard 2³ contrast decomposition, each with a
persona-clustered bootstrap CI (1,000 resamples, seed 42).

## Frozen predictions

**P-M1a (primary): L is the largest main effect**, and within L the work is done by the
**superseded-attribute-names block**, not the lifecycle counts. Direct consequence of E1.8: on the
FOK channel, randomising every count moved FR-Bank discrimination by +0.0015 while *names* carried
the signal. If names carry FOK, they should carry NOK a fortiori — the superseded-names block is
the only place in the index that names an obligation.

**P-M1b: L × D interaction is positive.** With no lifecycle signal in the index there is nothing for
a detection step to detect, so the two-step decomposition should buy little or nothing when L is off
and more when it is on.

**P-M1c (validity anchor): the all-off cell (L=0, W=0, D=0) reproduces E0's null**, delta within
±0.06 of +0.0411. This is a check on the factorial itself: if the all-off cell does not land near
E0, the factor realisations are not what they claim to be and **the module is reported as
invalid rather than interpreted.**

## Reporting

Eight cell AUROCs, three main effects, four interactions, all with CIs. Predictions scored
mechanically. Any violation reported as observed. **No gate — M1 informs the paper's mechanism
section and cannot change an E2 claim.**
