"""append_e16.py -- append the E1.6 redraw section and annotate superseded tables."""
from __future__ import annotations

import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"

RESULTS = """

---
---

# ADDENDUM — E1.6, FRONTIER REDRAW (k = 5)

**Pre-registered in `ADDENDUM_E1_6_REDRAW.md` (`c92deef`), committed before any redraw call.**
1,500 calls, **0 excluded**, subscription-billed (**$0**). Per-item mean over 5 draws is the score.

**These figures SUPERSEDE every single-draw frontier figure in this document and in
`HEADLINE.md`.** The single-draw run stays committed as the nondeterminism measurement of record
(D19-E1); superseded tables are annotated in place, not deleted.

## The nondeterminism, now measured directly

| | |
|---|---|
| cells (150 items × 2 arms) | 300 |
| cells whose **5 draws are all identical** | **3 (1%)** |
| per-item SD across draws | mean **0.0946**, median 0.0837, max 0.2821 |

D19-E1 inferred this from an accidental duplicate; it is now measured. **99% of frontier cells
fail to reproduce**, with a typical per-item swing of ~0.09 FOK. A single draw was not a usable
estimator, and every single-draw frontier number in this study was noisier than its interval
suggested.

## FOK — redrawn beside single-draw

| cell | n | blind 1-draw → **k=5** | indexed 1-draw → **k=5** | delta 1-draw → **k=5** | k=5 CI |
|---|---|---|---|---|---|
| **FR-Bank (primary)** | 84 | 0.6318 → **0.7099** | 0.7340 → **0.7463** | +0.1022 → **+0.0364** | [−0.0930, +0.1600] |
| external | 66 | 0.7843 → **0.9130** | 0.8079 → **0.8083** | +0.0236 → **−0.1046** | **[−0.2024, −0.0174]** |
| all 150 | 150 | 0.7192 → **0.8131** | 0.7497 → **0.7697** | +0.0306 → **−0.0433** | [−0.1151, +0.0231] |

**Almost the entire single-draw frontier delta was noise, and it was concentrated in the blind
arm.** Averaging five draws lifts frontier blind by +0.078 on FR-Bank and +0.129 on the externals,
while barely moving the indexed arm (+0.012 and +0.000). This is the attenuation mechanism
Amendment 2 anticipated for E0's blind arm, now observed directly at frontier scale and much
larger: noise in a single blind draw depresses blind AUROC and inflates the delta.

### Frozen Run-A rule, re-applied: **(b) cheap-model equalizer — unchanged**

Redrawn FR-Bank delta **+0.0364**, CI **[−0.0930, +0.1600]**. Rule (a) required delta ≥ +0.10 with
a CI excluding 0; the redrawn delta now fails **both** clauses. **The verdict is the same as the
single-draw run but for a far stronger reason**: the single-draw result was a near-miss at +0.1022
whose interval touched zero, and the better estimator puts the point estimate at a third of the
threshold. The framing of record is unchanged and is now firmly, not marginally, supported.

The cost comparison stands as stated: `gpt-4.1-mini` **indexed** 0.7530 against `gpt-5.6-sol`
**blind** 0.7099 on FR-Bank (0.8131 across all 150), at $0.00056 per mini indexed call versus a
subscription-billed frontier call using ~3,157 tokens and ~8 s against ~1.2 s.

### The external cell now inverts significantly

Redrawn external delta **−0.1046 with a CI excluding zero**. On the single draw this was +0.0236
and indistinguishable from noise. **The below-chance external index effect is now confirmed at
frontier scale and is statistically significant there** — a much stronger version of the E1 main
finding, and it holds for a model whose blind judgment on those same items is excellent (0.9130).
A frontier model reading these external indexes does worse than the same model reading nothing.

## NOK — redrawn (exploratory, ungated)

| | 1-draw | **k=5** | k=5 CI |
|---|---|---|---|
| blind | 0.5463 | **0.5290** | |
| indexed | 0.8497 | **0.8588** | |
| **delta** | +0.3034 | **+0.3298** | **[+0.1994, +0.4470]** |

**The NOK result strengthens under re-estimation and its CI excludes zero.** Unlike FOK, this is
not a noise artifact: the index helps the frontier model's negative-obligation judgment by a third
of an AUROC point. Still exploratory and ungated — H-NOK's verdict remains fixed on the
`gpt-4.1-mini` FR-Bank cell.

## Consequence for H1 that the redraw forces

`RESULTS_E1.md` §5 reported frontier blind FOK AUROC **0.7154** across the 150 items and concluded
that H1 "would still formally hold" for the frontier model, by 0.035. **The redrawn value is
0.8131, which is above the 0.75 H1 threshold.**

> **H1 does not hold for `gpt-5.6-sol`.** A frontier model has a substantial usable prior about
> what a specific store contains — blind AUROC 0.8131 — and the E1 claim that blind FOK is near
> chance is a property of `gpt-4.1-mini`, not of models in general.

Mean frontier blind FOK is 0.506 against a 0.600 base rate (gap −0.094), against
`gpt-4.1-mini`'s 0.208 (gap −0.392). The pessimistic-prior finding is likewise a small-model
property, as §5 said — but the discrimination conclusion there was too generous to H1 and is
corrected here.
"""

HEAD = """

---

## E1.6 REDRAW ADDENDUM (k = 5) — SUPERSEDES the frontier figures above

1. **The frontier lane barely reproduces: only 3 of 300 cells give identical results across 5 draws (1%), per-item SD 0.0946.** A single draw was not a usable estimator.
2. **Run A's delta was mostly noise.** FR-Bank frontier delta **+0.1022 → +0.0364**, CI [−0.0930, +0.1600]. Averaging lifts *blind* by +0.078 while the indexed arm barely moves — the attenuation Amendment 2 anticipated, now measured at frontier scale.
3. **Frozen rule re-applied: still (b) "cheap-model equalizer", now firmly rather than marginally** — the redrawn delta fails both of rule (a)'s clauses instead of one.
4. **The external inversion is now significant at frontier scale**: delta **−0.1046**, CI **[−0.2024, −0.0174]**, for a model whose blind judgment on those items is 0.9130. A frontier model reading those indexes does worse than reading nothing.
5. **H1 does NOT hold for `gpt-5.6-sol`.** Redrawn frontier blind FOK AUROC is **0.8131**, above the 0.75 threshold — correcting §5's "would still formally hold". **Frontier NOK strengthens**: delta **+0.3298**, CI [+0.1994, +0.4470]. Redraw cost **$0** (subscription-billed).
"""

NOTE_R5 = ("\n> **SUPERSEDED by the E1.6 redraw (k=5).** These single-draw frontier figures are "
           "retained as the nondeterminism measurement of record (D19-E1). The redrawn values, "
           "and the correction to the H1 conclusion below, are in the E1.6 addendum at the end of "
           "this document.\n")

DEV = """
---

### D21-E1 -- the k=5 redraw supersedes every single-draw frontier figure
`ADDENDUM_E1_6_REDRAW.md` (`c92deef`) was committed before any redraw call. 1,500 calls, 0
exclusions, $0 (subscription-billed). Measured directly what D19-E1 inferred: **3 of 300 cells
reproduce across 5 draws (1%)**, per-item SD mean 0.0946.

Consequences, all reported in the E1.6 addendum rather than absorbed: the FR-Bank frontier delta
falls +0.1022 -> +0.0364 (the frozen rule still fires (b), now firmly rather than marginally); the
external delta moves +0.0236 -> **-0.1046 with a CI excluding zero**, confirming the below-chance
finding at frontier scale; frontier NOK strengthens to +0.3298 with a CI excluding zero; and
frontier blind FOK AUROC rises 0.7154 -> **0.8131**, which is **above the 0.75 H1 threshold**, so
`RESULTS_E1.md` section 5's conclusion that H1 "would still formally hold" for the frontier model
is **corrected: it does not hold**. The superseded tables are annotated in place and the
single-draw run remains committed. **Status:** resolved, logged.
"""


def main():
    # append addendum sections
    for path, text, marker in ((E1 / "RESULTS_E1.md", RESULTS, "ADDENDUM — E1.6"),
                               (ROOT / "HEADLINE.md", HEAD, "E1.6 REDRAW ADDENDUM"),
                               (E1 / "DEVIATIONS.md", DEV, "D21-E1")):
        cur = io.open(path, encoding="utf-8").read()
        if marker in cur:
            print(f"  {path.name}: already present, skipped")
            continue
        with io.open(path, "a", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"  {path.name}: appended")

    # annotate the superseded tables in place
    rp = E1 / "RESULTS_E1.md"
    cur = io.open(rp, encoding="utf-8").read()
    anchors = [
        "## 5. Strong-model integrity check — the pessimistic prior is a small-model property\n",
        "## Run A — the frontier-indexed cell\n",
    ]
    changed = 0
    for a in anchors:
        if a in cur and (a + NOTE_R5) not in cur:
            cur = cur.replace(a, a + NOTE_R5, 1)
            changed += 1
    if changed:
        io.open(rp, "w", encoding="utf-8", newline="\n").write(cur)
    print(f"  RESULTS_E1.md: annotated {changed} superseded section(s)")


if __name__ == "__main__":
    main()
