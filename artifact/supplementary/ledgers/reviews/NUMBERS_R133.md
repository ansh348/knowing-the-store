# NUMBERS_R133.md: the R133 pass (the readability pass, v23; 2026-09-21)

Written by `reviews/v23/tools/ledger_r133.py`; every row is read from the artifact named; the printed forms are half-up on the four-decimal recorded value at two decimals (the convention of reviews/NUMBERS_R131.md). The pass itself changes no number; the one addition is R133 RULINGS 3 (the author, 2026-09-21): Table tab:routes (Appendix E.10) gains GPT-4.1 mini's per-state view-minus-summary rows.

## AUX-R133-ROUTES-PERSTATE: the tagged view under ground-truth tags minus the summary alone, per state (GPT-4.1 mini, one call; the full obligation set)

Source: `resp_review/run/scores_resp.json` `L2/arms/RETRIEVED/<state>` (the RESP registration's L2 arm; `resp_review/NUMBERS_RESP.md` AUX-RESP-L2-MINI-NOK rows 'RETRIEVED, expiry' and 'RETRIEVED, supersession'). Each state's obligations against the same 557 negatives (n = positives + 557).

| state | n / positives | the summary alone (base) | the tagged view (arm) | difference | item-level 95% | persona-clustered 95% | printed (tab:routes) |
|---|---|---:|---:|---:|---|---|---|
| expiry | 572 / 15 | 0.5110 | 0.7474 | +0.2364 | [+0.1053, +0.3829] | [+0.0645, +0.4037] | 0.75; +0.24 (the summary alone, 0.51); [+0.11,+0.38]; [+0.06,+0.40] |
| supersession | 620 / 63 | 0.8572 | 0.6853 | -0.1719 | [-0.2641, -0.0734] | [-0.2764, -0.0682] | 0.69; -0.17 (the summary alone, 0.86); [-0.26,-0.07]; [-0.28,-0.07] |

Both differences are reliable (both intervals exclude zero), as Section 7's sentence says ('the view helps mini on expiry ... and hurts it on supersession, both effects reliable'). The whole-set row (-0.0488, not reliable) and the retraction row (+0.0850, not reliable) stay in the RESP ledger; the ruling asked for expiry and supersession.

