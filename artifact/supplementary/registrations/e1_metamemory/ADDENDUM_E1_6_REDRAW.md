# PREREG ADDENDUM — E1.6, FRONTIER REDRAW

**Dated:** 2026-08-10 · **Amends:** `ADDENDUM_E1_5.md` (`3c3ef7d`). `PREREG_E1.md` (`875f726`) and
`AMENDMENT_1_E1.md` (`307865f`) are unchanged.

**Statement of prior data contact.** Written and committed **before any redraw call**. The
single-draw frontier figures already exist and are committed; this addendum specifies what
replaces them and how, before the replacement numbers exist.

---

## Why

D19-E1 measured that `codex exec` at these settings is substantially nondeterministic: 129 Run-A
items called twice with byte-identical prompts produced **98 disagreements on FOK**. Every frontier
figure in the study currently rests on a **single draw** per item, which under that noise level is
an unreliable estimator. This redraw replaces the estimator; it does not revisit any design
decision, hypothesis, threshold or label.

## What is re-elicited

All **four frontier cells** on the **same seed-42 150-item subsample**, via the fixed harness
(`run_a.py`'s post-fix code path, with the `__main__`-guard fault of D19-E1 already corrected):

| arm | prompt | judgments |
|---|---|---|
| frontier BLIND | frozen `SYSTEM` + `USER_BLIND` | FOK and NOK |
| frontier INDEXED | frozen `SYSTEM` + `USER_INDEXED`, TRUE index at ladder level 0 | FOK and NOK |

Both judgments come from the same response, so two arms × 150 items × **k = 5 draws** = **1,500
calls**. `gpt-5.6-sol`, the same frozen prompt texts, the same TRUE indexes, the same items.

**The score for an item is the per-item mean over its k = 5 draws**, for FOK and for NOK
independently. Draws that fail to parse are dropped and the mean is taken over the survivors; an
item with fewer than 3 surviving draws is excluded and counted.

## What is reported

1. **Redrawn AUROCs with paired bootstrap 95% CIs (1,000 resamples, seed 42), stated beside the
   single-draw values** in the same table, so the change from re-estimation is visible rather than
   silently substituted.
2. **The frozen Run-A interpretation rule, applied to the redrawn FOK delta on the FR-Bank subset
   (n = 84)** — unchanged from `ADDENDUM_E1_5.md`:
   - **(a)** redrawn delta ≥ +0.10 **and** paired bootstrap CI excludes 0 → **"the mechanism
     generalizes up the capability ladder"**.
   - **(b)** otherwise → **"cheap-model equalizer"**, with the cost comparison stated.
   The rule is re-applied, not re-written. Whichever way it falls is the framing of record, and if
   it falls differently from the single-draw run that reversal is reported explicitly as a
   consequence of re-estimation.
3. **The realised draw-to-draw spread**, as a direct measurement of the noise D19-E1 inferred from
   an accidental duplicate: per-item standard deviation across the 5 draws, and the fraction of
   items whose 5 draws are not all identical.
4. **Frontier NOK redrawn**, blind and indexed. Exploratory and ungated, as before; it does not
   touch H-NOK, whose verdict is fixed on the `gpt-4.1-mini` FR-Bank cell.

## Supersession rule

**The redrawn figures supersede the single-draw frontier figures everywhere downstream** — the
strong-model integrity table in `RESULTS_E1.md` §5, the E1.5 Run-A tables, and the corresponding
lines of `HEADLINE.md`.

**The single-draw run remains committed and is not deleted or rewritten.** It stays as the
nondeterminism measurement of record (D19-E1), and every superseded table is annotated in place
with a pointer to the redraw rather than silently edited. Nothing that was published stops being
visible.

## Scope and budget

No new labels, no new items, no design change, no other workstream. The lane is
subscription-billed, so the dollar cost is **$0**; the cost is ~1,500 codex calls and the wall
clock they take. The E1.5 $5 cap is untouched.
