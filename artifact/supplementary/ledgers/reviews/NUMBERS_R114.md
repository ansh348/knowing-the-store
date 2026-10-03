# NUMBERS_R114.md: the remaining runnable paid experiments (program R114, 2026-09-17)

Sections are appended by the scripts under `reviews/r114/tools/` and the lane tools named in `reviews/r114/SPEC_R114.md`; the lane ledgers of record (`ds_downstream/NUMBERS_DS.md`, `r85_graphiti/NUMBERS_R85.md`, `r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md`) carry the numbers and this file carries the pass's freeze, the call manifest and the spend roll-up. Every number the manuscript prints from this pass enters through a key in a lane ledger and no other way.

## 0. AUX-R114-SPEC-FREEZE

`reviews/r114/SPEC_R114.md` sha256 **`f13b7df47a9e58ebcd345e1d6d2c5b8fcc3a214ceec3da946cff9ca09722555b`**, recorded at HEAD `5e1a031` on 2026-09-17T00:25:58 before any call of this pass. The scripts assert this hash at start. Ceiling for NEW spend in this pass: $40.00; the manifest's expected total $5.70, conservative $7.55 (SPEC_R114 section 1).

## 1. AUX-R114-P1: Phase 1 done (`ds_downstream/NUMBERS_DS.md` section 14, AUX-DS-R114-*). Spend $0.1357 (mini $0.0328, Haiku $0.1006, probes $0.0023); results `reviews/r114/results/p1_composite_actual.json`.

## 2. AUX-R114-P2: Phase 2 done (`r85_graphiti/NUMBERS_R85.md` AUX-R85-G10-RESTORE-equivalent in AUX-R85-G10-INDEXES, -LEAK30, -SUMMARY, -NB, -P2, -P3, -GR, -RETRIEVE, -REACH, -TAGS, -PROMPTS, -CHECK, -VIEW, -P4, -HYBRID, -FRB-UNTAGGED, -HAIKU, -SPEND-R114; deviations D-R85-17 to D-R85-20). Spend $1.1851. Readings on the 323: P2 HOLDS, P3 FAILS, P4 HOLDS; GR-1 FAILS (weaker interval), GR-2 dash (not computable on FULL), GR-3 HOLDS, GR-4 and GR-5 descriptive. Haiku summary lane not run (rule not evaluable). Results `r85_graphiti/g10/results/{summary_g10,reach_g10,view_g10}.json`.

## 3. AUX-R114-P3: Phase 3, Amendment 2 Steps 1 to 3 done (`r85_graphiti/NUMBERS_R85.md` AUX-R85-A2-FREEZE, -PROMPTS, -VIEWS, -RESOLUTION, -CHECK, -SPEND, -DETECTOR, -TRANSITIONS, -SEAL). Spend $0.2359 (1114 distinct mini inputs + probe). The human read (Step 4), A2-P1 to A2-P3 and the ruling table (Step 5) are NOT done: the sheet `r85_graphiti/a2/sheet_a2.md` (622 rows) waits for the first reader and the second reader the author names; the detector rows are secondary and provisional. Haiku (section 8 (b)) not authorized at the freeze.

## 5. AUX-R114-P5: Phase 5 (PARA) **blocked**, verified from the annotation record: `reviews/v12/PARAPHRASE_READ.md` sha256 `bb2cf1e3eb624f6e…` unchanged; 124 accepted rows, both verdict columns empty on all 124 (248 empty cells, 0 rows with any verdict); the 24 screen-excluded pairs need no read. No lookup baseline, no lane, no subset drawn; $0.

## 4. AUX-R114-P4: Phase 4 done (`r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md` section 8, AUX-V2RCAT-OP5; D-V2RCAT-2). Opus 5 k = 1, 444 requests over three delivery paths (388 from the first Batch, canceled at the author's instruction after it had sat unprocessed; 5 from the resubmitted Batch, canceled likewise; 51 synchronous at list price, D-V2RCAT-3 and D-V2RCAT-4), 0 not OK, $4.5022 + probe $0.0158. Whole set 0.8049 against the recorded 0.8405 (-0.0357); retraction -0.1011, expiry -0.1236; branch: neither inside the band on both states nor beyond it with both intervals: printed as it came out.

## 6. AUX-R114-SPEND: the pass total, metered from the rows files: Phase 1 $0.1357, Phase 2 $1.1851, Phase 3 $0.2359, Phase 4 $4.5180, Phase 5 $0; **$6.0747** against the $40 ceiling (manifest expected $5.70, conservative $7.55). No retries were needed in any lane.

### AUX-R114-PRINTED: the forms the v19 manuscript prints from this pass (each from a value in a key named): $0.14$ = AUX-DS-R114-SPEND $0.1357 at two decimals; $4.52$ = AUX-V2RCAT-OP5 lane $4.5022 plus probe $0.0158 = $4.5180 at two decimals; $-0.10$ / $-0.12$ = AUX-V2RCAT-OP5 retraction $-0.1011$ / expiry $-0.1236$ at two decimals; $40$ = the pass ceiling (AUX-R114-SPEC-FREEZE).
