# NUMBERS_BELIEVED_H.md: ADDENDUM_BELIEVED_H (R-A), Haiku 4.5 under the store's own metadata

Registration `registrations/ADDENDUM_BELIEVED_H.md`, registered text sha256 `77de1e3786e4e86214f35a2a89c76d1daf4f88bd902f6c0e5f34880982b05d5c` (the bytes above the marker line), frozen at `257a090` on 2026-09-14. Descriptive: no prediction, no bar, no verdict. Every number for this addendum enters the manuscript through a key in this file and no other way. Written by `believed_h/tools/run_bh.py`; sections 1 to 3 before the first call.

## 1. AUX-BH-LOCK: the recorded texts, read and never re-rendered

`e1_metamemory/indexes_v2.json` sha256 `a54152bf3698cfbf...` (the committed BELIEVED texts, cap 15); `side_experiments/s2/indexes_s2u.json` sha256 `f05e95565c825cf2...` (the S2-U texts, cap lifted to 100); `r74/x4/cell_661.json` sha256 `01ed4c05fc57c0b2...`; the 661 item-to-key map asserted against `indexes_s2u.json` items (index_key_true = the cell's key; index_key_believed = its `:BELIEVED` form). 661 items, 104 positives. Capped texts 4256 characters mean, 15.04 superseded names per item; lifted 5765 characters, 32.55 names (max 50). Recorded rows read: Haiku 4.5 blind 0.415, truthful 0.821 (AUX-R74-X4-H45-NOK); mini capped 0.5959, lifted 0.6513 (AUX-E1R-BELIEVED-NOK, AUX-SIDE-S2-MINI).

## 2. AUX-BH-LOOKUP-LIFTED: the superseded-names embedding lookup on the lifted list ($0; computed before any call)

Capped list (gate): **0.5858** = the recorded 0.5858 (AUX-E1R-NB6) through `run_nb6.build` / `emb_scores`. Lifted list: **0.6588**, item [0.6036, 0.7093], persona [0.5777, 0.7319] (the same estimator over `index_v3.named_sections` of the S2-U text).

## 3. AUX-BH-PROBE and AUX-BH-PROJECTION (E1.7 rule; printed before submission)

| arm | served | identifier ok | probe in / out tokens | projected calls | projected $ | x1.3 | billed before | headroom | fits |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| INDEXED-BELIEVED-LIFTED | `claude-haiku-4-5-20251001` | True | 2230 / 200 | 3305 | 5.1315 | 6.6710 | 0.0032 | 11.9968 | True |
| INDEXED-BELIEVED-15 | `claude-haiku-4-5-20251001` | True | 1590 / 200 | 3305 | 4.6542 | 6.0505 | 5.1373 | 6.8627 | True |

## 4. AUX-BH-SUBMISSION

INDEXED-BELIEVED-LIFTED: Batch `msgbatch_01NJKDFhGWiGpvmSHwR2spv1`, 3305 requests; INDEXED-BELIEVED-15: Batch `msgbatch_01Lj4L97P4VwCKH9ykLwLQf5`, 3305 requests. Cap $12.00; billed so far (probes and collected rows) $9.3599. Rows collect to `believed_h/rows/<arm>/rows_H45.jsonl` on `poll`; AUX-BH-H45-*, -RETENTION-*, -BRANCH and -SPEND fill at `score`.

## 5. AUX-BH-H45-LIFTED, AUX-BH-H45-15: Haiku 4.5 under the two renderings (k = 5, X4 collapse; recorded blind 0.4150 and truthful 0.8210 reproduced)

| arm | AUROC | item 95% | persona 95% | minus truthful (item; persona) | minus blind | lookup on the same list | Haiku minus lookup (item; persona) | per state believed / truthful: SUP, RET, EXP | bad rows | $ |
|---|---:|---|---|---|---:|---:|---|---|---:|---:|
| INDEXED-BELIEVED-15 | **0.7069** | [0.6657, 0.7504] | [0.6620, 0.7541] | -0.1141 ([-0.1646, -0.0556]; [-0.1821, -0.0479]) | +0.2919 | 0.5858 | +0.1212 ([+0.0628, +0.1849]; [+0.0317, +0.2107]) | 0.7337 / 0.8897, 0.6624 / 0.7317, 0.6716 / 0.6874 | 0 | 4.3866 |
| INDEXED-BELIEVED-LIFTED | **0.7364** | [0.6911, 0.7858] | [0.6665, 0.8024] | -0.0847 ([-0.1330, -0.0293]; [-0.1480, -0.0268]) | +0.3214 | 0.6588 | +0.0776 ([+0.0272, +0.1355]; [-0.0031, +0.1498]) | 0.8369 / 0.8897, 0.5303 / 0.7317, 0.6712 / 0.6874 | 0 | 4.9676 |

## 6. AUX-BH-RETENTION-LIFTED, AUX-BH-RETENTION-15: retention = (BELIEVED minus blind) / (truthful minus blind), the ratio of the paired resampled differences

| arm | retention | item 95% (discarded draws) | persona 95% (discarded draws) |
|---|---:|---|---|
| INDEXED-BELIEVED-15 | **0.7190** | [0.6214, 0.8497] (0) | [0.5935, 0.8603] (0) |
| INDEXED-BELIEVED-LIFTED | **0.7916** | [0.6838, 0.9243] (0) | [0.6342, 0.9425] (0) |

### AUX-BH-BRANCH: retention 0.7916 lifted, 0.7190 capped: **at or above 60% under both**; the abstract says 'the smallest model and the lookup fall near chance; the larger model keeps 72% of its gain'. The sixty-percent line is the main-study preregistration's (2026-08-10, report-only), inherited unchanged; no reason for the value was recorded.

### AUX-BH-SPEND: {"INDEXED-BELIEVED-15": 4.3866, "INDEXED-BELIEVED-LIFTED": 4.9676, "cap": 12.0, "probes": 0.0058, "total": 9.36}

## 7. AUX-BH-SPLIT: the 63 supersession obligations split by whether the item's own scrubbed name survives in the BELIEVED list (the author's follow-up of 2026-09-14; $0; each half against the same 557 negatives)

| rendering | half | positives | Haiku BELIEVED (item; persona) | Haiku truthful | lookup on the BELIEVED list (item) | BELIEVED minus truthful (item; persona) | Haiku minus lookup (item; persona) |
|---|---|---:|---|---:|---|---|---|
| INDEXED-BELIEVED-15 | absent | 39 | **0.6933** ([0.6241, 0.7623]; [0.6053, 0.7854]) | 0.8880 | 0.6146 ([0.5490, 0.6763]) | -0.1947 ([-0.2673, -0.1224]; [-0.2813, -0.1011]) | +0.0787 ([-0.0137, +0.1666]; [-0.0497, +0.2355]) |
| INDEXED-BELIEVED-15 | present | 24 | **0.7993** ([0.7173, 0.8724]; [0.6923, 0.9104]) | 0.8925 | 0.7292 ([0.6285, 0.8239]) | -0.0932 ([-0.1746, -0.0006]; [-0.2041, +0.0235]) | +0.0701 ([-0.0204, +0.1663]; [-0.0261, +0.1709]) |
| INDEXED-BELIEVED-LIFTED | absent | 10 | **0.6839** ([0.5058, 0.8597]; [0.3363, 0.9811]) | 0.9122 | 0.7969 ([0.6722, 0.8992]) | -0.2283 ([-0.4288, -0.0430]; [-0.6568, +0.0182]) | -0.1130 ([-0.3613, +0.1503]; [-0.5208, +0.4381]) |
| INDEXED-BELIEVED-LIFTED | present | 53 | **0.8658** ([0.8162, 0.9087]; [0.8007, 0.9191]) | 0.8855 | 0.7593 ([0.6975, 0.8132]) | -0.0197 ([-0.0690, +0.0303]; [-0.0842, +0.0424]) | +0.1065 ([+0.0411, +0.1785]; [+0.0233, +0.1846]) |

