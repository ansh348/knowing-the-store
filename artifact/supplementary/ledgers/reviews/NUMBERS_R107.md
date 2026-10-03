# NUMBERS_R107.md — deterministic values and provenance rows of the v14-to-v15 pass (R107, 2026-09-14)

Purpose. On the R103/R104 precedent (`tools/trace_scan_v13.py` LEDGERS): (A) the provenance of the inherited 5% retrieval-pass figure, which Section 4 now states; (B) the k = 5 variation census of the recorded five-draw lanes, which Section 4 cites and the supplement (Section S.4) prints; (C) the decoding settings of the five-draw lanes as run. No model call; every value is read from a committed artifact named in its row.

## A. AUX-R107-AV7 — where the 5% pass rate was measured

| key | value | source |
|---|---|---|
| **AUX-R107-AV7** | FR-Bank's retrieval pass rate on the prior benchmark's **AV7 (Selective Forgetting) vector: 5% of its 40 questions**, one retraction question per persona, with FR-Bank's lifecycle mask in place; the personas are the same 40-persona bank this paper's stores are built from (`LifeMemEval/` personas = the persona ids of `e1_metamemory/build/items_final.json`), the questions and the join are the benchmark's | `neuripsv14.tex` per-vector table ("AV7 Selective Forgetting & 40 & 5\%") and Section 3.2; carried as `AUX-RETRACT` in `e1_metamemory/NUMBERS.md` ("inherited retrieval premise … a retrieval result, not an end-to-end monitoring result") |

## B. AUX-R107-K5 — what varied across the five draws of the recorded k = 5 lanes (`reviews/v14/tools/k5_variation.py` → `reviews/v14/k5_variation.json`)

Per (item, arm) group of five recorded draws: whether the obligation score (`nok`), the coverage score (`fok`) and the raw reply text differ across the draws; the range and standard deviation of `nok` across the five; the number of distinct `nok` values. Rows with status OK only.

| key | lane | groups | nok identical across the five | nok varies | text varies | nok range median / mean / max | groups with range > 0.10 | source rows |
|---|---|---:|---:|---:|---:|---|---:|---|
| **AUX-R107-K5-H45-661** | Haiku 4.5, the 661 (blind and truthful arms) | 1,322 | 1,123 (**85.0%**) | 199 (15.0%) | 557 (42.1%) | 0.00 / 0.0151 / 0.60 | 53 | `r74/x4/rows_H45.jsonl` |
| **AUX-R107-K5-OP5-661** | Opus 5, the 661 | 1,322 | 40 (3.0%) | 1,282 (**97.0%**) | 1,321 (99.9%) | 0.07 / 0.0940 / 0.52 | 450 | `r74/x4/rows_OP5.jsonl` |
| **AUX-R107-K5-LUNA-661** | GPT-5.6 Luna, the 661 | 1,322 | 49 (3.7%) | 1,273 (**96.3%**) | 1,321 (99.9%) | 0.05 / 0.1569 / 1.00 | 441 | `r74/x4/rows_LUNA.jsonl` |
| **AUX-R107-K5-H45-444** | Haiku 4.5, the counterfactual set (blind, v2, v3, v2r) | 1,480 | 1,206 (81.5%) | 274 (18.5%) | 1,125 (76.0%) | 0.00 / 0.0245 / 0.64 | 111 | `r82_counterfactual/cf2/rows/rows_H45.jsonl` |
| **AUX-R107-K5-OP5-444** | Opus 5, the counterfactual set | 1,480 | 67 (4.5%) | 1,413 (95.5%) | 1,464 (98.9%) | 0.07 / 0.0845 / 0.45 | 394 | `r82_counterfactual/cf2/rows/rows_OP5.jsonl` |

Printed forms: "identical on $85\%$ of item-arm groups" ← 0.8495 (1,123 of 1,322); "differ on $96\%$ to $97\%$" ← 0.9629 (Luna), 0.9697 (Opus 5).

## C. AUX-R107-TEMP — the five-draw lanes' decoding settings as run

| key | lane | temperature sent | source |
|---|---|---|---|
| **AUX-R107-TEMP** | Haiku 4.5 | 0 (accepted) | `r74/tools/x4_run.py` LANES (`temp=0.0`); D86 in `e1xv_crossvendor/DEVIATIONS_E1XV.md` (200 OK) |
| | Opus 5 | none (the provider rejects the parameter: "temperature is deprecated for this model") | `x4_run.py` (`temp=None`); D86 (400) |
| | GPT-5.6 Luna, GPT-5.6 Sol | none (reasoning lanes; `temp=None`) | `x4_run.py` LANES |
| | Kimi K3 | 1 (the provider's only accepted value) | D86 (`kimi-k3`: 400 at 0, 200 at 1); `x4_run.py` docstring |
| | GPT-4.1 mini (k = 1 everywhere) | 0, seed 42 | `prompts_e1.py` |
