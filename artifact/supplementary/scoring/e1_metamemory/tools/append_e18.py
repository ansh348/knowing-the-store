"""append_e18.py -- append the E1.8 closeout block to HEADLINE.md."""
from __future__ import annotations

import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

HEAD = """

---

## E1.8 STUDY CLOSEOUT — economics, mechanism, canonical record

**`e1_metamemory/NUMBERS.md` is now the authority. A figure not in it does not go in a draft.**
Detail: `ECONOMICS.md`, `RESULTS_E1_8.md`, `DEVIATIONS.md` (consolidated), `E2_BACKLOG.md`.

1. **The mechanism question is answered: counts are not the channel.** On the FR-Bank hard tier,
   randomising every count in the index moves discrimination by **+0.0015** (0.7003 → 0.7018);
   coarsening every count to {0, few, many} moves it by **+0.0012**; deleting every count moves it
   by **+0.0279**. All three inside the frozen 0.05 band, all three CIs including zero. **The
   frozen "ANSWERS the 'reading a table you built' objection with a mechanism" clause fires.**
   The signal is the **category-coverage map × question-specificity** — structure, not numbers.
2. **Deleting the counts makes the gate BETTER.** On the pooled hard tier A3 (names only, no
   numbers anywhere) scores **0.8516** against the intact index's 0.7530, CI [+0.0426, +0.1577],
   and nearly triples calibration (ECE 0.1741 → **0.0583**). The gain is entirely external: mean
   FOK on the all-ABSENT A-MEM and Mem0 hard tiers falls to **0.0259** and **0.0206**. **On an
   expressiveness-poor store, the counts were propping up a false sense of coverage.** Because
   this is *above* the reference rather than below it, the pooled row reads MIXED under the frozen
   rules — a direction they did not anticipate. **Nothing collapsed toward blind.**
3. **A limitation the probe surfaced, not previously reported.** Decomposing the FR-Bank hard
   tier: PN vs natural-absent is **0.5517 → 0.8782**, but PN vs slot-ablated-ABSENT is **0.4336 →
   0.4972 — at chance**. **H2-hard's FOK gain comes from recognising genuine absence, not from
   detecting slot ablation**; the PN-vs-ablation separation is NOK's job, and NOK does it
   (0.7339, +0.2393). This annotation now travels with the +0.2272 everywhere.
4. **The index is cheaper than it looks, and can be cheaper than no index.** Measured: blind
   **$234** / indexed **$519** per 1M gate calls — the index costs **$285 per 1M**. The frozen
   prompt puts the index *before* the question, so the prefix is byte-stable per user; priced with
   cached input the indexed gate falls to **$322** (as-run) and **$207** (asymptotic) per 1M,
   against a blind arm stuck at $234 because its 480-token prompt is below the 1,024-token minimum
   cacheable prefix. **List-price arithmetic, not billed.**
5. **Two corrections and one closed gap.** D22-E1 was wrong twice: the luna run took **43.2 min
   against sol's 44.7** (luna marginally *faster*, not ~80 min slower), and codex's "tokens used"
   is a turn total, not a reasoning-token count (D24-E1). Mini's per-call latency, never measured
   before, is **1.831 s mean / 1.653 s median** at 12 workers — the "~1.2 s" in the E1.5 block
   above was an estimate. E1.8 spend **$0.9040** against a $5 cap; total metered spend across the
   whole study remains under $3.
"""


def main():
    path = ROOT / "HEADLINE.md"
    cur = io.open(path, encoding="utf-8").read()
    if "E1.8 STUDY CLOSEOUT" in cur:
        print("  HEADLINE.md: already present, skipped")
        return
    with io.open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(HEAD)
    print("  HEADLINE.md: appended")


if __name__ == "__main__":
    main()
