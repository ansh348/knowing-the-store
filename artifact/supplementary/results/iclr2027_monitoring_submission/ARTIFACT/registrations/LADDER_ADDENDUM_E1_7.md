# PREREG ADDENDUM — E1.7, CAPABILITY LADDER (`gpt-5.6-luna`)

**Dated:** 2026-08-11 · **Extends:** `ADDENDUM_E1_6_REDRAW.md` (`c92deef`) and
`ADDENDUM_E1_5.md` (`3c3ef7d`). `PREREG_E1.md` (`875f726`) and `AMENDMENT_1_E1.md` (`307865f`)
are unchanged.

**Statement of prior data contact.** Committed **before any `gpt-5.6-luna` observation exists**.
No Luna call of any kind has been made. Every prediction and rule below is frozen here, verbatim,
in advance of the numbers.

**Superseding rule: nothing in E1.7 supersedes E1.6.** This extends the ladder; the k=5 redraw
figures remain the frontier figures of record.

---

## Purpose

The current capability comparison confounds three things at once: `gpt-4.1-mini` and
`gpt-5.6-sol` differ in **scale, generation, and post-training** simultaneously. Adding
**`gpt-5.6-luna`** — same generation as sol — isolates the capability axis.

This completes a three-point ladder: **`gpt-4.1-mini` / `gpt-5.6-luna` / `gpt-5.6-sol`**.
**Mini's role is hereafter the economics cell**; **luna-vs-sol is the scaling claim.**

## Frozen predictions (two-sided)

### P1 — LOAD-BEARING: Luna blind NOK is at chance

| outcome | condition | reporting |
|---|---|---|
| **HOLDS** | point AUROC **< 0.60** AND 95% CI **includes 0.50** | prediction confirmed |
| **FAILS** | point AUROC **≥ 0.65** AND CI **excludes 0.50** | reported **verbatim** as: *"obligation awareness is partially capability-graded; the information-property claim is damaged."* **No softening, no post-hoc subsetting.** |
| **INDETERMINATE** | anything between | reported as indeterminate |

### P2 — ordinal (shape claim)
Matched-cell **blind FOK** ordering **mini < luna < sol**.

### P3 — attenuation (shape claim)
FR-Bank primary **FOK index delta** ordering **sol < luna < mini**.
**Any violation is reported as observed.**

### P4 — Luna NOK index delta positive with 95% CI excluding zero.

### Two-axis verdict rule

The capability section's headline claim — **"scale buys coverage discrimination, not obligation
awareness"** — is **SUPPORTED iff P1 and P4 both hold.** P2 and P3 are shape claims for the ladder
figure and are **reported regardless of direction**; they do not gate the headline.

## Design

`gpt-5.6-luna` via the **same codex lane** as sol. The Phase-0 inventory recorded that the generic
`gpt-5.6` string routes to Sol server-side, so the **exact id is pinned** and the model string is
verified in the harness before any scored call.

- **Identical 150-item subset**: 84 FR-Bank primary (including all 40 PN items), 66 external.
- **Both arms**: blind and TRUE-indexed, at ladder level 0.
- **FOK and NOK** from the frozen elicitation, both judgments from one response.
- **Prompts byte-identical to E1.5/E1.6** — frozen `prompts_e1.py`, sha-verified at run time.
  **The model string is the only change.**
- **k = 5 draws per cell BY CONSTRUCTION**, per-item mean as the estimator.
  **No single-draw figure is computed anywhere.** Sol's single-draw run exists only because it
  preceded the k=5 policy; Luna has no such artifact and none is to be produced.
- Cache keyed **(item, arm, model, draw_index, prompt_hash)**.
- The `__main__`-guard fix (D19-E1) carries over.
- ~1,500 calls on the subscription lane; **anything metered is capped at $5**.

## Scoring

Same bootstrap procedure as E1.6 for comparability: 1,000 resamples, seed 42, items resampled.
For P1 the interval required is a **one-sample bootstrap CI on a single-arm AUROC** (does it
include 0.50), which E1.6 did not need; it is computed by the same resampling scheme applied to a
single arm.

Reported:

1. Luna blind and indexed AUROC, FOK and NOK, on FR-Bank primary / external / all-150, with
   deltas and 95% CIs.
2. Each frozen prediction with its verdict.
3. **Ladder table** — mini / luna / sol on matched cells: blind, indexed, delta. This is the
   paper's money-figure data; the predicted shape is **FOK delta decaying across the ladder while
   NOK delta stays flat**.
4. **Lane reproducibility for Luna as standing disclosure**: cells reproducing across 5 draws and
   per-item SD, reported alongside sol's **3/300** and **0.0946**.
5. **Blind-arm vs indexed-arm dispersion ratio across draws, all three models** — the
   index-as-variance-reducer observation. **Exploratory.**

## Scope fence

No NOK factorial. No renderer axis. No E2 material. No prompt edits mid-run.
**Any non-routine deviation stops the run before scoring.**
