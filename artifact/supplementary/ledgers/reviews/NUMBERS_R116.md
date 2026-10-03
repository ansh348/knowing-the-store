# NUMBERS_R116.md — program R116 (2026-09-18 / 19): the provenance fix and the harness disclosure

No new measurement enters through this pass. The pass records, beside their sources, the tokens the two appendix additions print: the probe-gate counts of the harness disclosure (Appendix B) and the price constants of the two frontier lanes (Appendix E.11). Sources: `reviews/r115/PROVENANCE_AUDIT.md`, `iclr2027_monitoring_submission/DEVIATIONS_R74.md` (D-R74-6, D-R74-8), `r74/tools/x4_run.py` (`LANES`), `r74/NUMBERS_R74.md` (X4), `e1_metamemory/ECONOMICS.md` (§0, the price table), OpenAI's model pages read on 2026-09-18 (`https://developers.openai.com/api/docs/models/gpt-5.6-sol`, `…/gpt-5.6-luna`), `scratch/e5_cost/REPORT_E5_COST.md` (§1, §3).

## AUX-R116-SPEC-FREEZE

The author's consolidated prompt of 18 September (Appendix R) and the rulings of 19 September (`reviews/r116/RULINGS_R116.md`, the pasted text verbatim). Tools: `reviews/r116/tools/r116_apply.py`, `r116b_apply.py`, `pin_appendix_r116.py`; every edit asserted.

## AUX-R116-HARNESS — the harness rows and the probe gates (Appendix B, the disclosure paragraph)

| printed | value | source |
|---|---|---|
| the pooled $66$ structureless questions | 29 Mem0 + 37 A-MEM items of the 150-item frontier subset (`e1_metamemory/strong_model.json`) | `e1_metamemory/NUMBERS.md` §9 ("sol · external FOK 66", "luna · external FOK 66"); `e1r_robustness/tools/run_clustered_ladder.py` |
| $0$ of $12$ (gate one) | the byte-verbatim flattened SYSTEM+USER body through `codex exec`: 0 parseable replies of 12 (conversational replies on both arms) | `DEVIATIONS_R74.md` D-R74-8 |
| $0$ of $12$ (gate two) | the authorised output-format wrapper around the byte-verbatim texts: 0 of 12 (diagnostic JSON, the multi-line body not delivered) | `DEVIATIONS_R74.md` D-R74-8 |
| reasoning effort low; ephemeral; subscription | `codex exec -m <model> … --ephemeral -c model_reasoning_effort=low`, `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` stripped from the environment | `e1_metamemory/tools/strong_model.py`, `tools/ladder_luna.py`; `ECONOMICS.md` §0 ("the frontier lane persisted no token telemetry") |
| rows marked $^{h}$ | `tab:ladder-exact` (4 rows), `tab:ladder-predictions` (5 rows, the Population cell), `tab:inversion` (2 rows), `tab:runs` (2 cells), Section 7 (one sentence) | `reviews/r117/PHASE0_REPORT.md` item 6(a) |

## AUX-R116-PRICES — the price constants of the two frontier lanes (Appendix E.11)

| printed | value | source |
|---|---|---|
| $0.20$ and $1.20$ (Luna, the lane code) | USD per million input / output tokens, `LANES["gpt-5.6-luna"]["price"] = (0.20, 1.20)` | `r74/tools/x4_run.py`; `ECONOMICS.md` price table (author-supplied 2026-08-11) |
| $5$ and $30$ (Sol, the lane code) | `LANES["gpt-5.6-sol"]["price"] = (5.00, 30.00)` | same |
| $2.67$ (Luna, the lane total) | 6,610 rows, token-metered at the constants | `r74/NUMBERS_R74.md` X4 ("luna ($2.67)"); `r74/x4/rows_LUNA.jsonl` (sum of `usd` 2.6731) |
| $12.39$ (Sol, the lane total, stopped) | 1,422 of 6,610 rows | `r74/NUMBERS_R74.md` X4 ("sol (1,422 rows, $12.39)"); `rows_SOL.jsonl` (sum 12.3872); D-R74-6 |
| $0.20$ and $1.20$ (Luna, the page) | input / output per million; cached input $0.02 | OpenAI model page, read 2026-09-18 |
| $4$ and $20$ (Sol, the page) | input / output per million; cached input $0.40 | OpenAI model page, read 2026-09-18 |
| $1.25$ | cache writes at 1.25× the uncached input rate on GPT-5.6 and later (the first send of a prompt over the 1,024-token minimum) | OpenAI prompt-caching guide, read 2026-09-18; the 17 September judge run's usage (`analysis/downstream_llm_judge_sol_v1/attempts.jsonl`, `cache_write_tokens`) |

## AUX-R116-PAGE

Before (R115 build): label page 9, reading 482 (+3), fine number 480 (+5), 58 pages. After the first R116 build (items 2 to 4 of Appendix R): 482 / 480 / 58. After the rulings of 19 September (`gates_r116b.txt`): recorded there.
