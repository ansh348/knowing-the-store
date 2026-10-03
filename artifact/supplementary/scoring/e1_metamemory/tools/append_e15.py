"""append_e15.py -- append the E1.5 addendum to RESULTS_E1, HEADLINE and DEVIATIONS."""
from __future__ import annotations

import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"

RESULTS = """

---
---

# ADDENDUM — E1.5

**Pre-registered in `ADDENDUM_E1_5.md` (`3c3ef7d`), dated and committed before any E1.5 call.**
Both interpretation rules were frozen before the numbers existed. Two runs only; the NOK factorial
is deferred to E2. **E1.5 spend $0.17** (Run A subscription-billed, Run B 522 calls) against a $5
cap. Adds no labels and changes none.

## Run A — the frontier-indexed cell

`gpt-5.6-sol` via `codex exec`, TRUE index at ladder level 0, frozen `USER_INDEXED` form, on the
same seed-42 subsample as the strong-model blind check. **150/150 parsed.**

| cell | n | frontier blind | frontier indexed | delta | 95% CI |
|---|---|---|---|---|---|
| **FR-Bank (primary)** | 84 | 0.6318 | 0.7340 | **+0.1022** | **[−0.0348, +0.2320]** |
| external (exploratory) | 66 | 0.7843 | 0.8079 | +0.0236 | [−0.0963, +0.1440] |
| all 150 | 150 | 0.7192 | 0.7497 | +0.0306 | [−0.0497, +0.1059] |

### Frozen rule (b) fires: **"cheap-model equalizer"**

Rule (a) required delta ≥ +0.10 **and** a CI excluding 0. The delta clears +0.10 at **+0.1022**;
**the CI does not exclude 0**. Rule (a) therefore fails on its second clause and (b) is the framing
of record. This is a near-miss on a two-part test and is described as one: the point estimate is at
the threshold, the interval is not.

**The cost comparison the rule requires.** `gpt-4.1-mini` **indexed** reaches hard-tier FOK AUROC
**0.7530**; `gpt-5.6-sol` **blind** reaches **0.7154**. A mini indexed call costs a measured
**$0.00056** ($1.3176 over 2,366 calls). The frontier call is subscription-billed with no per-call
dollar price, consuming ~3,157 tokens and ~8 s of wall clock against the mini call's ~1.2 s.
**A cheap model with an index matches or beats a frontier model without one**, at a per-call cost
measurable in hundredths of a cent against one not metered in dollars at all.

### Frontier NOK on the subsample (exploratory, ungated)

84 FR-Bank items, 40 PN: blind **0.5463** → indexed **0.8497**, delta **+0.3034**. The index helps
the negative-obligation judgment at frontier scale by more than it helps FOK. Not part of H-NOK,
whose verdict is already fixed.

### An unplanned measurement: the frontier lane is not deterministic

A harness fault (D19-E1) caused 129 of the 150 items to be called twice with byte-identical
prompts. **98 of those 129 pairs disagree on FOK.** `codex exec` at these settings does not
reproduce, at a rate far above E0's blind arm (90/255). Run A uses the post-fix draw throughout,
declared before scoring; a single draw per item therefore carries more noise than the E1 main arms,
which is part of why the interval is wide.

## Run B — the below-chance mechanism counterfactual

### H-a — uniform suppression landing harder on PRESENT · **SUPPORTED, thinly**

Mean per-item FOK shift (indexed − blind):

| backend | PRESENT | ABSENT | difference |
|---|---|---|---|
| Mem0 | −0.0585 | −0.0483 | 0.0102 |
| A-MEM | −0.0687 | −0.0579 | 0.0108 |
| FR-Bank (contrast) | **+0.2641** | +0.0317 | — |

The prediction holds in sign on both externals — but by **0.010**, and every median shift is 0.000,
so the means are carried by a minority of items. The contrast with FR-Bank is the striking part:
there the index *raises* PRESENT by +0.26 while barely moving ABSENT.

### H-b — inexpressibility markers drive pessimism · **SUPPORTED**

522 external items re-elicited with marker lines omitted rather than rendered; **522/522 parsed**.

| backend | n | blind | indexed **marked** | indexed **no-marker** | delta marked → no-marker |
|---|---|---|---|---|---|
| Mem0 | 238 | 0.5746 | 0.4777 | 0.4881 | −0.0969 → **−0.0865** |
| A-MEM | 284 | 0.5591 | 0.4526 | **0.5213** | −0.1065 → **−0.0378** |

The inversion shrinks on both, and on **A-MEM it shrinks by 65% and its CI now includes 0**
([−0.1024, +0.0260]) — no longer distinguishable from zero there. On Mem0 the shrink is small and
the CI still excludes 0. Mean FOK barely moves either way (A-MEM 0.161 → 0.155), so the markers
change **discrimination**, not level.

### H-c — count anchoring · **NOT SUPPORTED**

Spearman ρ between indexed FOK and index count fields: Mem0 **+0.006**, A-MEM **−0.094**, FR-Bank
**+0.142**. On the two backends where the inversion occurs the correlation is indistinguishable
from zero. The prediction fails.

### Verdict: **MECHANISM UNRESOLVED**

Two hypotheses survive their predictions and one fails. Per the frozen rule, mixed results yield
**mechanism unresolved, and the paper's text stays agnostic. No winner is forced.** H-a and H-b are
not mutually exclusive and both may be partly operative; the data do not separate them, and H-b's
effect is far stronger on A-MEM than on Mem0, which this design cannot explain either.

**What the paper may say:** the below-chance external result is real and replicated across two
backends, and removing the inexpressibility markers substantially reduces it on A-MEM.
**What it may not say:** that any one of these is the cause.
"""

HEAD = """

---

## E1.5 ADDENDUM (five lines)

1. **Run A fires rule (b), "cheap-model equalizer."** Frontier indexed − frontier blind on FR-Bank is **+0.1022**, CI **[−0.0348, +0.2320]** — the point estimate clears +0.10, the interval does not exclude 0, so rule (a)'s second clause fails. A near-miss, described as one.
2. **The cost comparison that framing requires:** `gpt-4.1-mini` **indexed** 0.7530 versus `gpt-5.6-sol` **blind** 0.7154, at a measured $0.00056 per mini indexed call against a subscription-billed frontier call using ~3,157 tokens and ~8 s versus ~1.2 s.
3. **Frontier NOK is strongly helped by the index** (exploratory, ungated): blind 0.5463 → indexed **0.8497**, delta **+0.3034** on the 84 FR-Bank items.
4. **Run B verdict: MECHANISM UNRESOLVED.** H-a (uniform suppression) holds in sign but by only 0.010; H-b (markers drive pessimism) holds and shrinks A-MEM's inversion by 65% until its CI includes zero; H-c (count anchoring) fails at ρ ≈ 0. Mixed, so the text stays agnostic and no winner is forced.
5. **Unplanned finding:** a harness fault double-called 129 Run-A items with identical prompts and **98 pairs disagreed** — `codex exec` is substantially nondeterministic at these settings, which is part of why Run A's interval is wide. **E1.5 spend $0.17** against a $5 cap.
"""

DEV = """
---

### D19-E1 -- run_a.py imported strong_model.py, which has no __main__ guard
`from strong_model import last_json, CODEX` re-executed the entire 150-item strong-model blind arm
before Run A began, and an interrupted first launch left duplicate rows in `run_a_partial.jsonl`
(279 rows, 150 distinct ids). Fixed by duplicating the two helpers into `run_a.py` rather than
editing `strong_model.py`, whose output is already committed. Rows were deduplicated keeping the
post-fix occurrence, declared before scoring; `strong_model.json` verified intact at 150/150.

**The fault produced a real measurement.** 129 items were called twice with byte-identical prompts
and **98 of those pairs disagree on FOK** -- `codex exec` at these settings is substantially
nondeterministic, well beyond E0's blind arm (90/255). Reported in the E1.5 addendum as a caveat on
Run A's interval width. **Status:** resolved, logged.

---

### D20-E1 -- Run B killed twice by parent-shell timeouts
The H-b arm died at ~300/522 and again when the foreground command that launched it hit the
10-minute limit. No correctness impact: every completed call was cached, so the relaunch resumed
and reached 522/522 for $0.0216 of new spend. **Status:** logged.
"""


def main():
    for path, text, marker in ((E1 / "RESULTS_E1.md", RESULTS, "ADDENDUM — E1.5"),
                               (ROOT / "HEADLINE.md", HEAD, "E1.5 ADDENDUM"),
                               (E1 / "DEVIATIONS.md", DEV, "D19-E1")):
        cur = io.open(path, encoding="utf-8").read()
        if marker in cur:
            print(f"  {path.name}: already present, skipped")
            continue
        with io.open(path, "a", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"  {path.name}: appended")


if __name__ == "__main__":
    main()
