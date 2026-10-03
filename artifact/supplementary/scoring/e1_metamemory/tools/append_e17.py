"""append_e17.py -- append the E1.7 ladder block to HEADLINE.md and DEVIATIONS.md."""
from __future__ import annotations

import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"

HEAD = """

---

## E1.7 CAPABILITY LADDER (`gpt-5.6-luna`) — extends E1.6, supersedes nothing

**Capability headline SUPPORTED: "scale buys coverage discrimination, not obligation awareness."**
All four frozen predictions hold (P1 load-bearing, P2, P3, P4). Full detail:
`e1_metamemory/RESULTS_E1_7.md`.

| FR-Bank | mini blind → indexed (delta) | luna | sol |
|---|---|---|---|
| **FOK** | 0.4488 → 0.7090 (**+0.2602**) | 0.5735 → 0.7417 (**+0.1682**) | 0.7099 → 0.7463 (**+0.0364**) |
| **NOK** | 0.5000ᵈ → 0.7139 (**+0.2139**) | 0.5585 → 0.8526 (**+0.2940**) | 0.5290 → 0.8588 (**+0.3298**) |

1. **FOK blind climbs with capability (0.45 → 0.57 → 0.71) while its index delta collapses (0.26 → 0.17 → 0.04)** — capability substitutes for the index on coverage.
2. **NOK blind stays pinned at chance across the whole ladder while its delta *grows* (0.21 → 0.29 → 0.33).** The index is not a crutch for weak models here; it supplies information no model in the ladder has.
3. **The indexed columns converge** (FOK 0.709/0.742/0.746; NOK 0.714/0.853/0.859). With an index the three models are close; without one they are not.
4. **Luna's external inversion is the study's largest: −0.3380, CI [−0.4896, −0.1811]** (blind 0.7894 → indexed 0.4514). The better a model's unaided judgment about an erase-mode store, the more the index costs it.
5. **Lane reproducibility, standing disclosure:** Luna 1/300 cells identical across 5 draws, per-item SD **0.1372**, against Sol's 3/300 and 0.0946. **Exploratory: the index cuts draw-to-draw dispersion ~44% on both frontier models** (ratio 0.562 luna, 0.589 sol). E1.7 cost **$0**.

ᵈ mini's blind NOK 0.5000 is a **tie-degenerate floor** — its blind NOK is constant at 0.0 on all 84 items. Luna's spans 48 distinct values and still fails to discriminate, which is a worse failure than refusing to answer.
"""

DEV = """
---

### D22-E1 -- Luna's throughput is roughly half Sol's
`gpt-5.6-luna` consumed ~11,700 reasoning tokens on a trivial probe against Sol's ~3,157, and the
1,500-call run took ~80 minutes rather than ~45. No design impact. Recorded because it is a
capability-axis observation in its own right and it sets the budget for any future rung.
**Status:** logged.

---

### D23-E1 -- mini's blind NOK is constant on the matched subset, so its 0.5000 is degenerate
On the 84 FR-Bank ladder items `gpt-4.1-mini`'s blind NOK is **0.0 on every item**, so every pair
is a tie and the AUROC is exactly 0.5 by arithmetic rather than by measurement. Luna's blind NOK
spans 48 distinct values and Sol's likewise, and both still fail to discriminate. Reported in place
wherever that cell appears, so the ladder's flat NOK-blind row is not read as three comparable
measurements. It strengthens rather than weakens the claim: the frontier models form varied
obligation judgments that carry no signal, which is a different failure from mini declining to
answer. **Status:** logged.
"""


def main():
    for path, text, marker in ((ROOT / "HEADLINE.md", HEAD, "E1.7 CAPABILITY LADDER"),
                               (E1 / "DEVIATIONS.md", DEV, "D22-E1")):
        cur = io.open(path, encoding="utf-8").read()
        if marker in cur:
            print(f"  {path.name}: already present, skipped")
            continue
        with io.open(path, "a", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"  {path.name}: appended")


if __name__ == "__main__":
    main()
