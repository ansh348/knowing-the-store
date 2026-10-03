# NUMBERS_R85 — the R85 Graphiti program's ledger (Amendment 1 onward)

Every number the paper prints from this program has a key here with its source artifact. The
spike's figures (30 August) live in `SPIKE_REPORT.md` and are not re-ledgered; keys below begin
with the Amendment 1 freeze. Registration: `registrations/ADDENDUM_R85_GRAPHITI_AMENDMENT_1.md`.

### AUX-R85-G10-FREEZE — the freeze (2026-09-15, no call)

| | Value |
|---|---|
| Freeze commit | `43132a3469f8160f0c6e98f8b4febbf099889a3d` |
| Amendment sha256 (the committed blob) | `45c79e1a67fe89fee8121a91e41595506e832e7c44718acdd7de575d9c414e5c` |
| `r85_graphiti/` tree at the freeze | `c20f44db86770e97af629e33b51b4107494ddccf` |
| `r85_graphiti/` tree at `f2d7688` (the last R85 commit, 30 August) | `c20f44db86770e97af629e33b51b4107494ddccf` |
| Unchanged since `f2d7688` | yes, the two tree hashes are equal |
| Files in the freeze commit | 1 (`registrations/ADDENDUM_R85_GRAPHITI_AMENDMENT_1.md`, 372 lines) |
| Billed calls at the freeze | 0 |

Checked with `git rev-parse HEAD:r85_graphiti`, `git rev-parse f2d7688:r85_graphiti`, and
`git show HEAD:registrations/ADDENDUM_R85_GRAPHITI_AMENDMENT_1.md | sha256sum`.

### AUX-R85-G10-ENV — Step 1, the environment (2026-09-15, no billed call)

| | Value |
|---|---|
| Docker Desktop | started by Step 1; engine 28.4.0 ready after 10 s |
| `neo4j-r85` | was `Exited (255) 2 weeks ago` (host shutdown), data volume intact; started, bolt 7688 answering after 15 s |
| Spike groups present, edges | `r85stock_elena` 242, `r85stock_tom` 221, `r85stock_yoli` 222, `r85fork_elena` 235, `r85fork_tom` 217, `r85stock_elena_nano` 89 |
| Match to `SPIKE_REPORT.md` | every edge count equal |
| `r85g10_*` groups present | none (0 nodes) |
| Stock venv | `AppData\Local\r85_stock_venv\Scripts\python.exe` present |
| `neo4j-graphiti` (the earlier work's instance) | auto-started with the engine; untouched |

### AUX-R85-G10-PROBE — Step 1, the identifier probe (one call, billed)

`r85_graphiti/g10/probe.py` in the stock venv; artifact `r85_graphiti/g10/probe_g10.json`.

| | Value |
|---|---|
| Probe UTC | 2026-09-15T18:47:13Z |
| Key | `OPENAI_API_KEY` (metered) |
| Requested / served | `gpt-4.1-mini-2025-04-14` / `gpt-4.1-mini-2025-04-14`, PASS |
| Tokens | 14 in, 1 out |
| USD | 0.0000072 |
| **Running billed total, Amendment 1** | **$0.0000072** |

### AUX-R85-G10-INGEST — Step 2, the forty-persona ingestion (2026-09-15 to 16, billed)

`r85_graphiti/g10/ingest_all.py` (commit `89bf718`, then the run-2 patch: an aborted persona's first attempt wipes its group)
driving `r85_graphiti/ingest.py` byte-identical to the spike's, `--arm stock --model gpt-4.1-mini-2025-04-14 --group-tag g10`,
group identifiers `r85stock_<persona>_g10` (D-R85-15). Per-persona records `r85_graphiti/ingest_runs/g10_<persona>.json`
(`ingest.py`'s own record, moved to the amendment's name by the runner); the three spike records restored from HEAD and
byte-identical to it. Verified on `neo4j-r85` after the run: 40 `*_g10` groups, 1,365 Episodic nodes, 7,096 Entity nodes,
9,189 RELATES_TO edges; the spike groups untouched (242 / 221 / 222 edges, equal to SPIKE_REPORT.md).

| | Value |
|---|---|
| Personas / episodes / records | 40 / 1365 / 18936 |
| Completed ingestion, billed | **$10.5250** (expected $10.17; stop line $13.22) |
| Per episode | $0.00771 (anchor $0.00745; +3.5%) |
| Per persona, min / mean / max | $0.1464 / $0.2631 / $0.3398 |
| LLM calls / tokens in (cached) / out / embed tokens | 13,523 / 22,032,601 (61,312) / 1,073,051 / 661,404 |
| Wall, sum of per-persona / elapsed | 5.22 h / run 1 about 35 min at 8-way (8 personas), run 3 65.2 min at 4-way (32 personas) |
| Aborted partial runs (12; below), billed | $1.3520 |
| Identifier probe (AUX-R85-G10-PROBE) | $0.0000072 |
| **Billed, all-in, Steps 1 and 2** | **$11.8770** |

**Logistics, logged, not deviations.** Run 1 (8-way) was killed by the host after eight personas for low system memory
(free 1.4 GB of 15.6 with PyCharm, Docker and a browser open), taking its eight in-flight `ingest.py` children with it;
run 2 (4-way) was killed the same way after 6 to 7 episodes of its first four. The amendment's rule for an aborted group
(a partial group confounds timeline-order invalidation) was applied: each aborted persona's next attempt ran with `--wipe`.
The twelve partial records are kept as billed artifacts in `r85_graphiti/g10/aborted/`; run 3 ran at 4-way (the amendment's
fallback width, here for memory rather than rate limiting) after the author closed the browser (free 5.1 GB), with no
failure and no rate limiting. Logs: `r85_graphiti/g10/ingest_all.run1.log`, `ingest_all.run2.log`, `ingest_all.log`, and
`g10/logs/<persona>.attempt1.log`.

| aborted run | episodes reached | billed |
|---|---|---|
| dariush.attempt1.partial | 23/35 | 0.1895 |
| dariush.attempt2.partial | 7/35 | 0.0413 |
| david.attempt1.partial | 24/35 | 0.1764 |
| david.attempt2.partial | 7/35 | 0.0418 |
| diane.attempt1.partial | 24/35 | 0.1731 |
| diane.attempt2.partial | 7/35 | 0.0413 |
| dmitri.attempt1.partial | 22/35 | 0.1539 |
| dmitri.attempt2.partial | 6/35 | 0.0345 |
| elena.attempt1.partial | 20/34 | 0.1536 |
| fatima.attempt1.partial | 18/34 | 0.1392 |
| ingrid.attempt1.partial | 14/33 | 0.1225 |
| jake.attempt1.partial | 14/33 | 0.0849 |

| persona | episodes | records | LLM calls | usd | usd/episode | wall min | |
|---|---|---|---|---|---|---|---|
| aisha | 31 | 536 | 319 | 0.2583 | 0.00833 | 7.2 | |
| alex | 33 | 410 | 326 | 0.2358 | 0.00714 | 8.1 | |
| amara | 34 | 339 | 320 | 0.2146 | 0.00631 | 7.4 | |
| aroha | 35 | 519 | 342 | 0.2850 | 0.00814 | 8.2 | |
| billy | 32 | 321 | 291 | 0.2189 | 0.00684 | 7.4 | |
| bruna | 33 | 553 | 404 | 0.2999 | 0.00909 | 9.4 | |
| callum | 34 | 440 | 335 | 0.2613 | 0.00768 | 8.4 | |
| chenoa | 35 | 486 | 354 | 0.2832 | 0.00809 | 8.9 | |
| dariush | 35 | 589 | 344 | 0.2900 | 0.00829 | 9.2 | |
| david | 35 | 575 | 356 | 0.2777 | 0.00793 | 8.2 | |
| diane | 35 | 487 | 338 | 0.2638 | 0.00754 | 8.4 | |
| dmitri | 35 | 499 | 390 | 0.3157 | 0.00902 | 10.3 | |
| elena | 34 | 574 | 350 | 0.2757 | 0.00811 | 7.4 | spike persona, second graph (D-R85-13) |
| fatima | 34 | 451 | 342 | 0.2804 | 0.00825 | 8.1 | |
| ingrid | 33 | 412 | 376 | 0.2933 | 0.00889 | 7.8 | |
| jake | 33 | 401 | 303 | 0.2212 | 0.00670 | 6.6 | |
| jerome | 34 | 622 | 403 | 0.3291 | 0.00968 | 8.5 | |
| joonho | 34 | 383 | 297 | 0.2178 | 0.00641 | 6.4 | |
| kenji | 35 | 460 | 333 | 0.2679 | 0.00765 | 8.3 | |
| kofi | 35 | 591 | 337 | 0.2891 | 0.00826 | 7.5 | |
| leila | 35 | 491 | 361 | 0.3008 | 0.00859 | 8.7 | |
| lily | 35 | 467 | 381 | 0.2849 | 0.00814 | 8.9 | |
| marcus | 32 | 262 | 222 | 0.1464 | 0.00457 | 5.2 | |
| marley | 33 | 381 | 316 | 0.2292 | 0.00694 | 7.1 | |
| mehmet | 35 | 512 | 299 | 0.2517 | 0.00719 | 6.7 | |
| mirri | 35 | 582 | 417 | 0.3398 | 0.00971 | 9.0 | |
| nadia | 35 | 512 | 391 | 0.3009 | 0.00860 | 8.2 | |
| omar | 35 | 355 | 270 | 0.1891 | 0.00540 | 6.4 | |
| pan | 35 | 582 | 366 | 0.3120 | 0.00891 | 7.7 | |
| patrick | 34 | 402 | 290 | 0.2061 | 0.00606 | 6.2 | |
| priya | 32 | 390 | 329 | 0.2247 | 0.00702 | 6.9 | |
| raj | 35 | 524 | 337 | 0.2671 | 0.00763 | 7.6 | |
| rosa | 35 | 562 | 345 | 0.2664 | 0.00761 | 7.4 | |
| saga | 35 | 431 | 342 | 0.2585 | 0.00738 | 7.8 | |
| samuel | 35 | 570 | 347 | 0.2933 | 0.00838 | 8.4 | |
| thanh | 34 | 572 | 369 | 0.3085 | 0.00907 | 8.3 | |
| tom | 35 | 432 | 324 | 0.2393 | 0.00684 | 7.3 | spike persona, second graph (D-R85-13) |
| valentina | 32 | 386 | 264 | 0.2037 | 0.00637 | 7.8 | |
| yoli | 34 | 452 | 331 | 0.2549 | 0.00750 | 8.3 | spike persona, second graph (D-R85-13) |
| zara | 35 | 423 | 362 | 0.2690 | 0.00769 | 7.7 | |

### AUX-R85-G10-CENSUS — Step 3, section 4 A(i), the R85 census as frozen over the forty g10 graphs (2026-09-16, no call)

`r85_graphiti/g10/census_all.py` running the frozen `census.py` per persona (`--group-tag g10`, unchanged) and pooling; per-persona
records `r85_graphiti/census_runs/g10_<persona>.json` and `.index.txt` (the three spike records restored from HEAD, byte-identical);
`r85_graphiti/g10/census_g10.json`. Denominator: the 109 MIN_DISCR-filtered manifest supersession events over forty personas
(reproduces the census figure 109, `_personas_census.txt`).

| | Value |
|---|---|
| Edges / states under RULE 1 | 9,189 / active 8,382, superseded 130, expired 677 |
| Manifest supersession events | 109 |
| Buckets | RECOVERED 20, STALE_ACTIVE 12, EXTRACTION_MISS 77 |
| **Recall at the frozen tau 0.80** | **20 / 109 = 0.1835** (the trial's reference figure 0.20 on three personas) |
| Recall by coverage band (0.50 / 0.75 / 0.80) | 57 / 35 / 20 of 109 |
| **Precision**, explained-invalidated over all invalidated edges | **35 / 807 = 0.0434** |
| Entity fragmentation, user nodes per persona | {'2': 7, '3': 32, '4': 1} (2, 3 or 4 nodes stand for the one user) |
| Undated edges (`valid_at` null) / invalidated before valid | 784 / 2 |
| Manifest facts extracted at tau 0.80 | 134 / 565 = 0.2372; by kind {'expiring': [50, 126], 'retraction_original': [7, 40], 'stable_identity': [27, 160], 'supersession_new': [7, 121], 'supersession_old': [43, 118]} |
| Future-dated edges (`valid_at` or `invalid_at` after the persona clock, section 3) | 72 of 9,189 over 40 graphs (alex 1, amara 1, aroha 2, billy 6, bruna 1, callum 8, chenoa 2, dariush 3, david 1, diane 1, dmitri 8, fatima 7, ingrid 1, jerome 1, kofi 1, lily 3, marcus 3, marley 4, mehmet 1, mirri 1, nadia 1, patrick 3, priya 1, raj 3, rosa 2, saga 1, thanh 2, tom 1, valentina 2) |

GR-5's failure mode from this census: extraction, not lifecycle. 77 of 109 events have no edge asserting the old value at all;
of the 32 events Graphiti did extract, it invalidated 20 and kept 12 live.

### AUX-R85-G10-REPEAT — the three spike personas, trial graph beside g10 graph (D-R85-13; descriptive, no bar)

| persona | edges | events | buckets | recall | precision | fact recall | undated edges |
|---|---|---|---|---|---|---|---|
| elena | 242 / 237 | 3 / 3 | {'RECOVERED': 1, 'EXTRACTION_MISS': 2} / {'RECOVERED': 1, 'EXTRACTION_MISS': 2} | 0.3333 / 0.3333 | 0.0417 / 0.0312 | 0.2 / 0.2 | 25 / 10 |
| tom | 221 / 213 | 3 / 3 | {'EXTRACTION_MISS': 3} / {'EXTRACTION_MISS': 2, 'STALE_ACTIVE': 1} | 0.0 / 0.0 | 0.0 / 0.0 | 0.2143 / 0.3571 | 28 / 26 |
| yoli | 222 / 224 | 4 / 4 | {'EXTRACTION_MISS': 2, 'RECOVERED': 1, 'STALE_ACTIVE': 1} / {'EXTRACTION_MISS': 3, 'RECOVERED': 1} | 0.25 / 0.25 | 0.0357 / 0.069 | 0.375 / 0.4375 | 11 / 12 |

(trial / g10 in each cell; the trial is `r85stock_<persona>` from 30 August, the g10 graph a fresh ingestion under the same pinned
environment on 15 to 16 September.)

### AUX-R85-G10-CENSUS-FORBIDDING — Step 3, section 4 A(ii), the forbidding-record census (2026-09-16, no call)

`r85_graphiti/g10/census_forbidding.py`; `r85_graphiti/g10/census_forbidding_g10.json`. Population: the 104 obligations of the
committed 661, states from the join (`index_v2.true_lifecycle`), never from the attack vector.

| | Value |
|---|---|
| Join split of the 104 | superseded-or-expired **74**, retracted **8**, unflagged **22** (D-R85-12; the attack-vector split 78 / 26) |
| Buckets over the 74 | RECOVERED 30, STALE_ACTIVE 21, EXTRACTION_MISS 23 |
| **Recall** | **30 / 74 = 0.4054** (over the attack-vector 78: 0.3846) |
| Recall by coverage band (0.50 / 0.75 / 0.80) | 48 / 36 / 30 of 74 |
| **Precision**, non-active edges (RULE 1) over forty graphs that fire on a join-marked record | **54 / 807 = 0.0669** |
| Retraction obligations | 8 join-retracted (of 26 AV7); the marker on every Graphiti row |

By attack vector, the 74 superseded-or-expired obligations:

| attack vector | n | RECOVERED | STALE_ACTIVE | EXTRACTION_MISS | recall |
|---|---|---|---|---|---|
| AV1_superseded_preference | 38 | 18 | 11 | 9 | 0.4737 |
| AV2_expired_logistics | 11 | 1 | 5 | 5 | 0.0909 |
| AV4_multi_version_fact | 25 | 11 | 5 | 9 | 0.4400 |

**P1 reads FAILS** (section 5: recall at or below 0.25 and precision at or below 0.10, tolerance 0.05): precision holds at 0.0669;
recall is 0.4054 on the join's 74 (0.3846 on the attack-vector 78), above the quarter by more than the
tolerance. The registered FAILS text, with the placeholders filled: "Over the forty personas Graphiti reaches 30 of the
74 forbidding records (the join's count; 30 of the attack-vector 78), above the registered quarter, at precision 0.0669."

Why (ii) reads higher than (i) is population, not method: the obligations' marking events are the ones FR-Bank itself extracted
cleanly enough for the join to mark (the question set was built on them), where (i)'s 109 include the events FR-Bank missed; and the
25 AV4 multi-version obligations draw on the manifest's `contradictions` section, which the frozen event census never counted.
Expiry is the weak state for Graphiti in both: 1 of 11 expired obligations recovered.

### AUX-R85-G10-CENSUS-FORBIDDING-FULL — the forbidding-record census re-aggregated on the FULL store variant (D-R85-16; 2026-09-16, no call)

`r85_graphiti/g10/census_full_variant.py`; `r85_graphiti/g10/census_full_variant_g10.json`. The recorded per-obligation rows of
`census_forbidding_g10.json` re-aggregated, nothing re-detected. The 104 obligations are 47 questions under up to three FR-Bank store
variants; every Graphiti graph is the FULL store for its persona, so the 57 non-FULL rows (48 of them with the FULL sibling's
`pn_members` exactly) repeat forbidding records already counted on the same graph. Bucket assignments agree across every shared
member set (0 disagreements). Precision is over edges and is unchanged (54 / 807 = 0.0669).

| population | obligations | join split (sup-or-exp / retracted / unflagged) | RECOVERED | STALE_ACTIVE | EXTRACTION_MISS | recall |
|---|---:|---|---:|---:|---:|---:|
| the registered 104 rows | 104 | 74 / 8 / 22 | 30 | 21 | 23 | 30 / 74 = 0.4054 |
| **the 47 FULL-variant obligations** (the main-text reading) | 47 | 34 / 4 / 9 | **13** | 10 | 11 | **13 / 34 = 0.3824** |
| the 56 distinct (persona, member-set) pairs (sensitivity) | 56 | 39 / 4 / 13 | 16 | 11 | 12 | 16 / 39 = 0.4103 |

By attack vector on the 34 FULL-variant superseded-or-expired obligations: AV1 16 (7 / 5 / 4, recall 0.4375), AV2 7 (1 / 3 / 3,
0.1429), AV4 11 (5 / 2 / 4, 0.4545). The three readings agree in direction; P1's recall bar (at or below 0.25) fails on each.

### AUX-R85-G10-PRINTED — the forms the paper prints (R112, the integration pass of 2026-09-16)

| printed | source | where |
|---|---|---|
| 13 of the 34; 0.38 | AUX-R85-G10-CENSUS-FORBIDDING-FULL, 13 / 34 = 0.3824 | Section 7, the Graphiti sentence; Appendix G.4 |
| 54 of its 807; 0.07 | AUX-R85-G10-CENSUS-FORBIDDING, precision 54 / 807 = 0.0669 | Section 7; Appendix G.4 |
| 30 of the 74; 0.41; 0.38 (over the 78) | AUX-R85-G10-CENSUS-FORBIDDING, 0.4054; 0.3846 | Appendix G.4, the registered reading and the P1 text |
| 16 of 39; 0.41 | AUX-R85-G10-CENSUS-FORBIDDING-FULL, distinct member sets 0.4103 | Appendix G.4 |
| 20 of 109; 0.18; 35 of 807; 0.04 | AUX-R85-G10-CENSUS, 0.1835; 0.0434 | Appendix G.4, the event census |
| 57 / 35 / 20; 48 / 36 / 30 | AUX-R85-G10-CENSUS and -CENSUS-FORBIDDING, the 0.50 / 0.75 / 0.80 bands | Appendix G.4 |
| 1,365; 7,096; 9,189; 8,382; 130; 677; 784; 72 | AUX-R85-G10-INGEST and -CENSUS | Appendix G.4 |
| 134 of 565; 0.24 | AUX-R85-G10-CENSUS, manifest-fact recall 0.2372 | Appendix G.4 |
| 0.47, 0.09, 0.44 (AV1, AV2, AV4 on the 74); 0.44, 0.14, 0.45 (on the 34) | the two census sections | Appendix G.4 |
| $11.88 | AUX-R85-G10-INGEST, $11.8770 all-in | Appendix E.11 / G.4 |

### AUX-R85-G10-INDEXES — Step 4, the indexes (2026-09-17, program R114; no call; `g10/build_indexes.py`, `g10/indexes_g10.json`)

Forty personas, the `_g10` groups read only. BELIEVED-capped: the cap-15 render reproduces `census_runs/g10_<persona>.index.txt` byte for byte on 40 of 40 (renderer lock); whole-map names per store 100 to 211 (mean 164.6), superseded names 0 to 6 (mean 2.02; the cap never binds on the superseded section), 33 to 34 lines. BELIEVED-lifted: `SLOT_CAP` = **1000** (the amendment names 100; the largest whole map is 211, so 100 binds on the forty stores and the next power of ten is used, D-R85-19), no `(+N more)` in any text, 49 to 72 lines. TRUE-projected: the persona's FR-Bank FULL rows under the TRUE join rendered under `AVAIL_GRAPHITI` (category and retracted print the marker); the same rows under `AVAIL[(frbank, TRUE)]` reproduce the committed `frbank:<persona>:FULL:TRUE` index on 40 of 40 (renderer lock); the cap binds on the projection's whole map on **40** of 40 (FR-Bank's slot names in one bucket once the category axis is inexpressible), so TRUE-projected-lifted (cap 1000) is added as section 4 B provides; 32 to 33 lines capped, 44 to 68 lifted; the projection's superseded-names section holds 0 to 5 names (the cap of 15 binds on it in 0 personas).

### AUX-R85-G10-LEAK30 — Step 4, the leakage screen at forty personas (2026-09-17; `g10/run_summary.py leak30`; `g10/leak30_g10.json`; billed)

30 PRESENT FULL-variant items drawn by the frozen rule (seed 42 over the 131, as `run_leakage_control.py`), GPT-4.1 mini asked to answer from the BELIEVED-capped index alone (`prompts_e1.LEAKAGE_*`, `supports_correct`, UNKNOWN never correct): **0 of 30** answered correctly against the frozen threshold of more than 3 of 30 — no leak; the summary lanes proceed. $0.0052.

### AUX-R85-G10-SUMMARY — Step 4, the summary route on the 323 (2026-09-17, program R114, D-R85-17; `g10/run_summary.py`; `g10/rows_summary.jsonl`; `g10/results/summary_g10.json`; billed)

GPT-4.1 mini, one call per (item, index), the main-study protocol, on the 323 FULL-variant items (positives 47); the blind and INDEXED-TRUE rows from the record (gates on the 323: INDEXED-TRUE 0.7424, BLIND 0.4964, equal to AUX-R113-Z3-ROWS). Item-level and persona-clustered paired bootstraps, 1,000 draws, seed 42; the weaker governs. Per state: that state's positives against every FULL negative (276).

| index | NOK AUROC (item 95%) | minus INDEXED-TRUE (item; persona) | minus BLIND (item; persona) | supersession (27) | expiry (9) | retraction (11) | FOK on the 323 (178 pos.) | failures | served | $ |
|---|---|---|---|---:|---:|---:|---:|---:|---|---:|
| G10-BELIEVED | **0.5765** [0.4945, 0.6560] | -0.1659 ([-0.2593, -0.0764]; [-0.2533, -0.0876]) | +0.0801 ([-0.0031, +0.1604]; [+0.0027, +0.1624]) | 0.6592 | 0.4275 | 0.4956 | 0.6101 | 0 | gpt-4.1-mini | 0.1232 |
| G10-LIFTED | **0.6511** [0.5779, 0.7286] | -0.0912 ([-0.1869, +0.0098]; [-0.1738, -0.0068]) | +0.1548 ([+0.0793, +0.2302]; [+0.0807, +0.2259]) | 0.7419 | 0.5948 | 0.4743 | 0.8052 | 0 | gpt-4.1-mini | 0.2320 |
| G10-TRUEPROJ | **0.7556** [0.6724, 0.8341] | +0.0132 ([-0.0560, +0.0804]; [-0.0565, +0.0803]) | +0.2592 ([+0.1752, +0.3361]; [+0.1732, +0.3400]) | 0.8796 | 0.4618 | 0.6915 | 0.5738 | 0 | gpt-4.1-mini | 0.1199 |
| G10-TRUEPROJ-LIFTED | **0.6958** [0.6231, 0.7720] | -0.0466 ([-0.1068, +0.0128]; [-0.1207, +0.0157]) | +0.1994 ([+0.1249, +0.2755]; [+0.1256, +0.2703]) | 0.8393 | 0.5334 | 0.4764 | 0.8698 | 0 | gpt-4.1-mini | 0.2027 |

### AUX-R85-G10-NB — the readers on the same renderings ($0; `run_nb6.emb_scores` / `lex_scores` on the name lists of AUX-R85-G10-INDEXES, D-R85-19): NB-6 over the superseded-names section, NB-5 over the whole map

| index | NB-6 emb (item 95%) | NB-6 lex | NB-5 emb | NB-5 lex | NB-6 emb minus the monitor (item; persona) | items with an empty superseded list |
|---|---|---|---|---|---|---:|
| G10-BELIEVED | **0.6780** [0.5955, 0.7589] | 0.5000 | 0.6994 | 0.5020 | +0.1014 ([+0.0102, +0.2086]; [+0.0094, +0.1988]) | 20 |
| G10-LIFTED | **0.6780** [0.5955, 0.7589] | 0.5000 | 0.7959 | 0.6576 | +0.0268 ([-0.0602, +0.1231]; [-0.0604, +0.1248]) | 20 |
| G10-TRUEPROJ | **0.7154** [0.6128, 0.8035] | 0.5713 | 0.6667 | 0.5002 | -0.0402 ([-0.1259, +0.0419]; [-0.1193, +0.0433]) | 75 |
| G10-TRUEPROJ-LIFTED | **0.7154** [0.6128, 0.8035] | 0.5713 | 0.6911 | 0.6094 | +0.0196 ([-0.0600, +0.1023]; [-0.0555, +0.1097]) | 75 |

### AUX-R85-G10-P2 — **HOLDS**. Under Graphiti's store-written summary GPT-4.1 mini reads 0.5765 against 0.7424 under the ground-truth summary on the same 323 questions, -0.1659 below with interval [-0.2593, -0.0764] (persona [-0.2533, -0.0876]); a matcher reading Graphiti's own list of superseded names reads 0.6780. The blind row prints beside, not inside, the criterion: 0.4964 (one value on most questions; Section 4's caveat). BELIEVED-lifted 0.6511, TRUE-projected 0.7556, TRUE-projected-lifted 0.6958, no bar.

### AUX-R85-G10-P3 — **FAILS**. A matcher reading Graphiti's own list of superseded names reaches 0.6780 under the capped rendering and 0.6780 under the lifted (the superseded section is identical under both, the cap never binding on it), +0.1780 from chance, item intervals [0.5955, 0.7589] / [0.5955, 0.7589].

### AUX-R85-G10-GR — GR-1 **FAILS**: on Graphiti BELIEVED the paired NOK gain on GPT-4.1 mini is +0.0801, item [-0.0031, +0.1604], persona [+0.0027, +0.1624]. GR-2: dash: the FULL variant holds 145 hard-tier items with 0 positives (the hard tier's 35 positives are all ablated-variant rows), so the registered row is not computable on the 323; descriptive on the 323 (FOK, 178 positives): blind 0.5921, TRUE 0.9191, BELIEVED 0.6101, gain +0.0180 item [-0.0516, +0.0869] persona [-0.0572, +0.0977]. GR-3 **HOLDS**: the matcher 0.6780 against the monitor 0.5765, margin +0.1014 ([+0.0102, +0.2086]; [+0.0094, +0.1988]). GR-4 (descriptive): Graphiti BELIEVED's NOK gain over blind +0.0801 is 0.3257 of FR-Bank's TRUE gain on the same 323 (+0.2460) and 0.3349 of the registered 661 gain (+0.2393), beside FR-Bank's own BELIEVED retention of 42.3%. GR-5: extraction (AUX-R85-G10-CENSUS: EXTRACTION_MISS 77 of 109; erase with overstatement in what survives), unchanged by this step.

### AUX-R85-G10-SUMMARY-SPEND — leakage screen $0.0052, probes $0.0022, lanes G10-BELIEVED $0.1232, G10-LIFTED $0.2320, G10-TRUEPROJ $0.1199, G10-TRUEPROJ-LIFTED $0.2027; **Step 4 total $0.6852**.

### AUX-R85-G10-RETRIEVE — Step 5, the tag-route retrieval on the 323 (2026-09-17, program R114; `g10/retrieve.py` in the stock venv, `g10/build_views_g10.py`; `g10/retrieval_raw_g10.json`, `g10/retrieval_g10.json`, `g10/views_g10.json`)

Stock `Graphiti.search(question, group_ids=[r85stock_<persona>_g10], num_results=10)` (`EDGE_HYBRID_SEARCH_RRF`, default `SearchFilters()`), graphiti-core 0.28.1 from site-packages, one `text-embedding-3-small` call per question: 323 calls, 3692 tokens, $0.00007, 0 LLM calls; edges returned per item {0: 1, 6: 1, 9: 1, 10: 320} (the stock recipe's cosine leg carries `sim_min_score` 0.6 and BM25 may return nothing, so three items return fewer than ten and one returns none, D-R85-20; 3215 lines; states over the ten {'expired': 279, 'superseded': 43, 'active': 2893}; over ranks 1 to 5 {'expired': 121, 'superseded': 21, 'active': 1468}). Every retrieved edge found in the persona's whole edge set with equal fact and temporal fields; RULE 1 states by `census.derive` over the whole graph, RULE 2 names, D-R85-10 ages; all ten rendered lines and states kept per item (Amendment 2 section 4). FR-Bank VIEW-UNTAGGED (D-R85-14): the recorded `top5_ids` re-rendered over the join's flags reproduce the recorded RETRIEVED block on 323 of 323, the `lifecycle:` field then removed.

### AUX-R85-G10-REACH — the forbidding record among the retrieved edges (`census_forbidding.py`'s matcher, tau 0.80, on the ten edges), the 47 FULL obligations

Reached in ranks 1 to 5: **10 of 47**; in ranks 1 to 10: **16 of 47**; per state (n, k5, k10) {'sup': [27, 4, 10], 'ret': [11, 3, 3], 'exp': [9, 3, 3]}; by the join's state {'superseded_or_expired': 34, 'unflagged': 9, 'retracted': 4}; obligations with no marking event (9) count as unreached. FR-Bank's recorded reach by identifier on the same 47: 26 / 34 (AUX-R113-Z3-REACH).

### AUX-R85-G10-TAGS — the store's non-active mark against the join's, the analogue of AUX-RESP-A1-TAGS

Over the forbidding records in view (ranks 1 to 5 of the 47 obligations that fire): tp 7 / fp 0 / fn 5 / tn 0; recall 0.5833, precision 1.0. Over every line of the 323 views (ranks 1 to 5, 1610 lines; the join's mark = the edge fires on any join event of the persona): tp 14 / fp 128 / fn 12 / tn 1456; precision 0.0986, recall 0.5385. FR-Bank's own marks on the recorded views (AUX-RESP-A1-TAGS): recall 0.7833 / precision 0.6714 in view; precision 0.1353 over all lines.

### AUX-R85-G10-PROMPTS — the untagged variant by one asserted `str.replace` ("each with the lifecycle metadata the store records" -> "each with the metadata the store records") on `SYSTEM_RETRIEVED` and `USER_RETRIEVED`: sha256 `f9f2c3b66195345d…` / `88e8ee533287e6d7…`; the frozen `SYSTEM_RETRIEVED` `602b9431b3fca99b…`, `USER_RETRIEVED` `d9031f6f5bedd7a6…`, `USER_HYBRID` `b29d1e476c260279…` (AUX-RESP-L2-PROMPTS).

### AUX-R85-G10-CHECK — the Step 5 checkpoint (registered for 22 September; performed 2026-09-17 by the executing session under the author's instruction of that day, not by the author): the format assertions hold on all 323 items (field order, the marker on category, the untagged line differing from the tagged in exactly the `lifecycle:` field, the FR-Bank re-render equal to the record); the seeded draw (seed 42) of five Graphiti and five FR-Bank untagged views is `g10/checkpoint_views.md` (Graphiti frbank:aroha:aroha_q03:FULL, frbank:fatima:fatima_q05:FULL, frbank:mehmet:mehmet_q13:FULL, frbank:omar:omar_q09:FULL, frbank:raj:raj_q08:FULL; FR-Bank frbank:diane:diane_q05:FULL, frbank:elena:elena_q08:FULL, frbank:jake:jake_q12:FULL, probe:frbank:pan:62390807, probe:frbank:samuel:55903416), read by eye before Step 6 (the reading recorded below this key).

**The reading by eye (2026-09-17, the executing session).** The ten views of `g10/checkpoint_views.md` read against `build_l2.py`'s format: (i) field order `[r] lifecycle | category | attribute | age | text` on every Graphiti line and every FR-Bank line; (ii) `category: not expressible by this backend` on every Graphiti line, the FR-Bank lines carrying their categories; (iii) the age arithmetic checked by hand on the dated edges (aroha: valid_at 2025-09-15 against t_now 2026-05-15 = 242 days; fatima: 2024-11-18 against 2026-03-01 = 468, 2025-03-05 = 361, 2024-12-17 = 439; omar: 2025-08-04 against 2026-04-06 = 245, 2024-12-20 = 472, 2026-01-22 = 74, 2025-12-03 = 124; raj: 2025-01-20 against 2026-04-23 = 458, 2025-01-06 = 472, 2025-05-20 = 338) and every undated edge (`valid_at` null) printing `age: 0 days` by D-R85-10's fallback to `created_at`, the ingestion wall clock, which lies after every persona clock and clamps to zero (mehmet's five lines, raj's [1] and [3], omar's [4], fatima's [3]); the census counted 784 such edges and this is how they read in a view; (iv) the untagged line equal to the tagged line with exactly the `lifecycle:` field removed on all fifty lines; (v) the RULE 1 states read as the fields say (fatima [5]: invalid_at set, no successor on the slot, `expired`; samuel [5] on FR-Bank: `expired` under the join). No rendering fault found; Step 6 proceeds.

### AUX-R85-G10-VIEW — Step 6, the tag-route lanes on the 323 (2026-09-17, program R114, D-R85-17; `g10/run_view.py`; `g10/rows_view.jsonl`; `g10/results/view_g10.json`; billed)

GPT-4.1 mini, one call per (item, lane), the RESP L2 protocol; the recorded FR-Bank rows re-scored on the 323 (gates: RETRIEVED 0.698, RETRIEVED-BELIEVED 0.8504, HYBRID 0.8855, INDEXED-TRUE 0.7424, BLIND 0.4964, equal to AUX-R113-Z3-ROWS). Item-level and persona-clustered paired bootstraps, 1,000 draws, seed 42.

| lane | view | prompt | NOK AUROC (item 95%) | minus BLIND (item; persona) | minus INDEXED-TRUE (item; persona) | supersession (27) | expiry (9) | retraction (11) | FOK (323) | empty views | $ |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|
| G10-VIEW-UNTAGGED | Graphiti ranks 1-5, no lifecycle field | untagged variant | **0.6995** [0.6230, 0.7698] | +0.2032 ([+0.1274, +0.2723]; [+0.1248, +0.2826]) | -0.0428 ([-0.1616, +0.0818]; [-0.1757, +0.0896]) | 0.6439 | 0.6244 | 0.8976 | 0.8701 | 1 | 0.1121 |
| G10-VIEW-TAGGED | Graphiti ranks 1-5, RULE 1 states | SYSTEM_RETRIEVED / USER_RETRIEVED | **0.6854** [0.6113, 0.7573] | +0.1891 ([+0.1150, +0.2629]; [+0.1145, +0.2689]) | -0.0569 ([-0.1739, +0.0655]; [-0.1725, +0.0601]) | 0.6501 | 0.5491 | 0.8837 | 0.8886 | 1 | 0.1148 |
| G10-HYBRID | Graphiti ranks 1-5 tagged + BELIEVED-capped summary | SYSTEM_RETRIEVED / USER_HYBRID | **0.7741** [0.6944, 0.8529] | +0.2778 ([+0.1976, +0.3572]; [+0.1862, +0.3637]) | +0.0318 ([-0.0859, +0.1541]; [-0.0886, +0.1478]) | 0.8023 | 0.5099 | 0.9211 | 0.8828 | 1 | 0.1613 |
| FRB-VIEW-UNTAGGED | FR-Bank recorded top-5, no lifecycle field | untagged variant | **0.6991** [0.6166, 0.7747] | +0.2027 ([+0.1201, +0.2789]; [+0.1253, +0.2772]) | -0.0432 ([-0.1634, +0.0680]; [-0.1427, +0.0575]) | 0.6539 | 0.7047 | 0.8057 | 0.9278 | 0 | 0.1101 |

### AUX-R85-G10-P4 — **HOLDS**. Shown the five retrieved edges with Graphiti's own states, GPT-4.1 mini reads 0.6854 against 0.6995 without them, -0.0141 apart with interval [-0.0786, +0.0554] (persona [-0.0613, +0.0325]); within tolerance: the states this store writes do not reach the records that forbid use.

### AUX-R85-G10-HYBRID (descriptive, no bar) — HYBRID 0.7741 against VIEW-TAGGED 0.6854: +0.0887 ([+0.0180, +0.1603]; [+0.0274, +0.1587]); against the BELIEVED-capped summary alone 0.5765: +0.1976 ([+0.1039, +0.2980]; [+0.0990, +0.2972]).

### AUX-R85-G10-FRB-UNTAGGED (D-R85-14, descriptive, no bar) — FR-Bank's recorded top-5 with the lifecycle field removed: 0.6991; the recorded RETRIEVED row (the join's tags) 0.6980 is -0.0011 above it ([-0.0987, +0.0955]; [-0.1016, +0.0983]); the recorded RETRIEVED-BELIEVED row (FR-Bank's own marks) 0.8504 is +0.1512 above it ([+0.0738, +0.2323]; [+0.0727, +0.2365]). Cross-store, the same footing: Graphiti VIEW-TAGGED against FR-Bank RETRIEVED-BELIEVED +0.1649 ([+0.0897, +0.2403]; [+0.0886, +0.2377]); Graphiti VIEW-UNTAGGED against FR-Bank VIEW-UNTAGGED -0.0004 ([-0.0935, +0.0949]; [-0.1078, +0.0943]).

### AUX-R85-G10-VIEW-SPEND — probes $0.0015, lanes G10-VIEW-UNTAGGED $0.1121, G10-VIEW-TAGGED $0.1148, G10-HYBRID $0.1613, FRB-VIEW-UNTAGGED $0.1101; **Step 6 total $0.4998**; query embeddings (Step 5) $0.00007.

### AUX-R85-G10-HAIKU — Step 8, Haiku 4.5 at k = 5 on BELIEVED-capped: **dash, not run**. Section 7's rule ("Haiku runs if and only if the billed total at that point plus $4.44 is at or under $20.00", evaluated once after X1 and X3) cannot be evaluated in program R114 because X1 and X3 do not run in it (the author's instruction of 2026-09-17: X1 to X4 not run); the lane's price at the registered anchor is $4.44 (Batch). The row prints a dash with this footnote.

### AUX-R85-G10-SPEND-R114 — Steps 4 to 6 on the 323 (2026-09-17): Step 4 $0.6852 (leakage screen, probes, four summary lanes), Step 5 $0.00007 (323 query embeddings), Step 6 $0.4998 (probes, four view lanes); **$1.1851** this program. The R85 billed total becomes $11.8770 + $1.1851 = $13.0621 (AUX-R85-G10-INGEST carried $11.8770).

## Amendment 2 (2026-09-17, program R114)

### AUX-R85-A2-FREEZE

`registrations/ADDENDUM_R85_GRAPHITI_AMENDMENT_2.md` frozen by sha256 **`b87401f3604fed8d4db3e2fa20d758b274748374f876374321880e674c2fab92`** over the whole file (the draft's registered text above the marker line sha256 `c39b75328a91847c5c12dfc686589d188dcd4883827a225a052263e9650caa96`; the R113 draft hash 2e7715d1… is the sha256 of those bytes less the one newline that separates them from the marker line, i.e. the draft file as it stood, unchanged), recorded 2026-09-17T01:06:43 before any Phase 3 call, uncommitted (D-R85-18). The freeze decisions are the file's dated section: the §0 ruling per D-R85-17; the second reader not named; Haiku not authorized in this pass; Steps 1 to 3 by 24 September; the M rule confirmed (active of ranks 1 to 10, first five, renumbered); Step 5's ten-line record in place; Steps 1 to 3 run here, Steps 4 to 7 the author's.

### AUX-R85-A2-PROMPTS — the four prompt texts (Step 1, 2026-09-17; `a2/build_views_a2.py`): `SYSTEM_ANSWER` `af1c69c8817d2867…`, `USER_ANSWER_A4` `e6c155364f8c69be…` (AUX-DS-A4-LOCK); `SYSTEM_ANSWER_U` `69920206dfd337b6…` (the lifecycle sentences from "An entry marked active" to "must not be given as the answer." removed and "each entry carries the lifecycle metadata" -> "each entry carries the metadata", two asserted replaces), `USER_ANSWER_A4_U` `9eb131624b663785…` ("each with the lifecycle metadata the store records for it" -> "each with the metadata the store records for it", one asserted replace). The abstention instruction stays in both system prompts.

### AUX-R85-A2-VIEWS — the view census (`a2/views_a2.json`, `a2/census_a2.json`); FR-Bank's views equal the R113 pre-freeze build on 278 of 278 items

| cell | n (obl. / lic.) | distinct inputs U / T / M (all) | T = M | n_TM (bound) | obligations n_TM (bound) | licensed n_TM (bound) | M short views (lengths) | lines removed T -> M | A2-P2 reading rule |
|---|---|---|---:|---|---|---|---|---:|---|
| frbank|primary_178 | 178 (47 / 131) | 178 / 178 / 178 (519) | 15 | **163** (0.9157) | 46 (0.9787) | 117 (0.8931) | 63 ({0: 1, 1: 3, 2: 16, 3: 14, 4: 29}) | 423 | empirical (bound at or above 0.05) |
| graphiti|primary_178 | 178 (47 / 131) | 178 / 178 / 178 (417) | 117 | **61** (0.3427) | 22 (0.4681) | 39 (0.2977) | 2 ({4: 2}) | 82 | empirical (bound at or above 0.05) |
| frbank|frbank_only_100 | 100 (57 / 43) | 99 / 99 / 96 (287) | 7 | **93** (0.93) | 55 (0.9649) | 38 (0.8837) | 34 ({2: 3, 3: 15, 4: 16}) | 234 | empirical (bound at or above 0.05) |

Distinct complete inputs over every cell: **1114** (nominal 1368 rows); per cell {'frbank|primary_178': 519, 'graphiti|primary_178': 417, 'frbank|frbank_only_100': 178}.

### AUX-R85-A2-RESOLUTION — section 5 (ii) the mechanism sets and the evidence-in-view flags (section 6), per cell

| cell | (a) reached | (b) reached, marked | (c) reached, unmarked | (e) imported | (g) unreached in 10 | (f) evidence removed by intent (of licensed with evidence in T) | evidence in view, licensed U / T / M (of n) | evidence in view, with-replacement U / T / M (of n) |
|---|---:|---:|---:|---:|---:|---|---|---|
| frbank|primary_178 | 26 | 23 | 3 | 10 | 13 | {'CHANGE-AWARE': 5, 'CURRENT-STATE': 18, 'UPCOMING': 3, 'PAST-EVENT': 3} (of {'CHANGE-AWARE': 13, 'CURRENT-STATE': 31, 'UPCOMING': 8, 'PAST-EVENT': 3}) | 55 / 55 / 53 (of 131) | 12 / 12 / 14 (of 38) |
| graphiti|primary_178 | 10 | 5 | 5 | 0 | 31 | {'UPCOMING': 1, 'CHANGE-AWARE': 1, 'CURRENT-STATE': 2, 'PAST-EVENT': 1} (of {'CURRENT-STATE': 20, 'UPCOMING': 3, 'CHANGE-AWARE': 7, 'PAST-EVENT': 4}) | 34 / 34 / 32 (of 131) | 11 / 11 / 10 (of 38) |
| frbank|frbank_only_100 | 28 | 23 | 5 | 10 | 17 | {'CURRENT-STATE': 6, 'CHANGE-AWARE': 1, 'PAST-EVENT': 3} (of {'CHANGE-AWARE': 5, 'CURRENT-STATE': 10, 'UPCOMING': 3, 'PAST-EVENT': 3}) | 21 / 21 / 22 (of 43) | 4 / 4 / 6 (of 10) |

The structural bound (section 5 (i)) is n_TM / n; U against T and U against M carry no bound (the prompts differ on every item). On Graphiti set (a) uses `census_forbidding.py`'s matcher on the retrieved edges (AUX-R85-G10-REACH); on FR-Bank the member identifier.

### AUX-R85-A2-CHECK — the by-eye check (section 4; performed 2026-09-17 by the executing session under the author's instruction, not by the author): the assertions hold on every view of every cell (456 item-cells); the seeded draw is `a2/checkpoint_views_a2.md` (Graphiti frbank:tom:tom_q11:FULL:U, frbank:chenoa:chenoa_q01:FULL:T, frbank:alex:alex_q07:FULL:M, frbank:jake:jake_q11:FULL:T, frbank:ingrid:ingrid_q01:FULL:M; FR-Bank frbank:fatima:fatima_q05:FULL:U, frbank:dariush:dariush_q09:FULL:T, frbank:callum:callum_q08:FULL:M, frbank:yoli:yoli_q07:FULL:T, frbank:raj:raj_q07:FULL:M), read by eye before Step 2 (the reading recorded below this key).

**The reading by eye (2026-09-17, the executing session).** The ten views of `a2/checkpoint_views_a2.md` read against section 4: U carries `[r] category | attribute | age | text` with no lifecycle field on every line (Graphiti tom_q11, FR-Bank fatima_q05, and the U block of every other draw); T carries the store's own state (Graphiti: `expired` on chenoa [3], alex [2], jake [2], `superseded` on jake [4]; FR-Bank: `superseded, expired` and `expired` on fatima's five lines, in `resp_common.lifecycle_tag`'s order); the marker on category on every Graphiti line; M holds only `active` lines, renumbered [1]..[n] in rank order with the source ranks recorded (chenoa [1, 2, 4, 5, 6]; alex [1, 3, 4, 5, 6]; jake [1, 3, 5, 6, 7]; fatima on FR-Bank [6, 7, 9], a three-line view because ranks 1 to 5, 8 and 10 are all marked non-active), and equals T where ranks 1 to 5 hold no non-active line (tom, ingrid); the age arithmetic follows D-R85-10 on Graphiti (undated edges at 0 days; tom [2] at 14,327 days from a 1987 `valid_at`) and the pinned `t_now` on FR-Bank; the persona name and date in the header match the join. No rendering fault found; Step 2 proceeds.

### AUX-R85-A2-SPEND — Step 2, the mini run (2026-09-17; `a2/run_a2.py`; `a2/rows_a2_mini.jsonl`; cache `a2/cache_mini/`): 1114 distinct inputs answered ({'OK': 1114}), served ['gpt-4.1-mini'], 481258 in / 26936 out, **$0.2356** plus the probe $0.0003 against the section 8 worst line $0.47. Haiku 4.5 (section 8 (b)): dash, not authorized at the freeze ($1.22 expected).

### AUX-R85-A2-DETECTOR — Step 3, the committed detector rows on every answer (2026-09-17; `a2/score_a2.py`; `a2/results/detector_a2.json`). **Secondary and provisional**: the endpoints of C1 to C3 are the human read of section 6, which has not run; no A2-P1 to A2-P3 verdict and no ruling-table row is entered here. Expiry obligations are unscorable for stale use by the detector and print as such.

| cell | cond. | obligations: n, abstained, scorable, stale at 0.50 / 0.80, surfaced, successor used (sup.), reported (A7), expiry unscorable | licensed: n, correct at 0.50 / 0.80, abstained (unnecessary / appropriate), evidence in view | licensed correct by intent CS / UP / CA / PE |
|---|---|---|---|---|
| frbank|primary_178 | U | 47, 8, 38, **14** / 6, 6, 1, 0, 9 | 131, **41** / 15, 27 (6 / 21), 55 | 26/65, 7/26, 7/35, 1/5 |
| frbank|primary_178 | T | 47, 16, 38, **7** / 3, 3, 1, 1, 9 | 131, **34** / 12, 40 (9 / 31), 55 | 22/65, 6/26, 6/35, 0/5 |
| frbank|primary_178 | M | 47, 10, 38, **11** / 3, 4, 1, 5, 9 | 131, **44** / 14, 28 (2 / 26), 53 | 27/65, 7/26, 9/35, 1/5 |
| graphiti|primary_178 | U | 47, 11, 38, **9** / 3, 3, 1, 2, 9 | 131, **24** / 5, 66 (6 / 60), 34 | 17/65, 2/26, 3/35, 2/5 |
| graphiti|primary_178 | T | 47, 11, 38, **8** / 3, 3, 1, 0, 9 | 131, **25** / 5, 58 (5 / 53), 34 | 17/65, 1/26, 5/35, 2/5 |
| graphiti|primary_178 | M | 47, 11, 38, **6** / 2, 2, 1, 0, 9 | 131, **23** / 5, 56 (4 / 52), 32 | 16/65, 1/26, 5/35, 1/5 |
| frbank|frbank_only_100 | U | 57, 12, 51, **24** / 12, 13, 2, 1, 6 | 43, **13** / 5, 9 (4 / 5), 21 | 6/20, 3/8, 3/10, 1/5 |
| frbank|frbank_only_100 | T | 57, 21, 51, **13** / 5, 5, 1, 2, 6 | 43, **12** / 3, 13 (5 / 8), 21 | 5/20, 3/8, 4/10, 0/5 |
| frbank|frbank_only_100 | M | 57, 10, 51, **16** / 7, 7, 2, 7, 6 | 43, **17** / 5, 8 (2 / 6), 22 | 8/20, 5/8, 3/10, 1/5 |

**Paired detector differences (descriptive; item-level and persona-clustered percentile bootstraps, 1,000 draws, seed 42; the structural bound of AUX-R85-A2-VIEWS applies to the T-versus-M rows):**

| cell | C1 stale T − U (47) | C2 stale M − T (47) | C2 reported M − T (47) | C3 correct M − U (131) | C3 correct T − U (131) | C3 unnecessary decline M − U (131) |
|---|---|---|---|---|---|---|
| frbank|primary_178 | -0.1489 ([-0.2553, -0.0426]; [-0.2609, -0.0565]) | +0.0851 ([-0.0213, +0.2128]; [-0.0227, +0.1905]) | +0.0851 ([+0.0213, +0.1702]; [+0.0200, +0.1800]) | +0.0229 ([-0.0305, +0.0763]; [-0.0299, +0.0775]) | -0.0534 ([-0.1069, +0.0000]; [-0.1016, -0.0072]) | -0.0305 ([-0.0611, -0.0076]; [-0.0604, -0.0074]) |
| graphiti|primary_178 | -0.0213 ([-0.1064, +0.0851]; [-0.1087, +0.0667]) | -0.0426 ([-0.1064, +0.0000]; [-0.1087, +0.0000]) | +0.0000 ([+0.0000, +0.0000]; [+0.0000, +0.0000]) | -0.0076 ([-0.0382, +0.0229]; [-0.0385, +0.0256]) | +0.0076 ([-0.0153, +0.0305]; [-0.0210, +0.0331]) | -0.0153 ([-0.0382, +0.0000]; [-0.0413, +0.0000]) |
| frbank|frbank_only_100 | -0.1930 ([-0.2987, -0.0702]; [-0.3125, -0.0769]) | +0.0526 ([-0.0351, +0.1404]; [-0.0364, +0.1400]) | +0.0877 ([+0.0175, +0.1579]; [+0.0308, +0.1667]) | +0.0930 ([+0.0000, +0.2093]; [+0.0000, +0.1951]) | -0.0233 ([-0.1163, +0.0698]; [-0.1220, +0.0750]) | -0.0465 ([-0.1395, +0.0238]; [-0.1430, +0.0392]) |

### AUX-R85-A2-TRANSITIONS — per-item transitions by the detector's category (obligations: stale / declined / other / unscorable; licensed: correct / declined / wrong)

| cell | U -> T obligations | T -> M obligations | U -> T licensed | T -> M licensed |
|---|---|---|---|---|
| frbank|primary_178 | {'other->other': 16, 'other->declined': 6, 'stale->other': 6, 'stale->declined': 1, 'unscorable->unscorable': 9, 'stale->stale': 7, 'declined->other': 1, 'declined->declined': 1} | {'other->other': 18, 'declined->other': 5, 'other->stale': 5, 'declined->declined': 2, 'unscorable->unscorable': 9, 'stale->stale': 5, 'declined->stale': 1, 'stale->other': 2} | {'declined->declined': 24, 'wrong->wrong': 49, 'wrong->declined': 12, 'correct->wrong': 6, 'correct->declined': 4, 'correct->correct': 31, 'wrong->correct': 2, 'declined->correct': 1, 'declined->wrong': 2} | {'declined->declined': 26, 'wrong->wrong': 48, 'declined->wrong': 9, 'wrong->correct': 7, 'declined->correct': 5, 'correct->correct': 32, 'correct->wrong': 2, 'wrong->declined': 2} |
| graphiti|primary_178 | {'other->other': 20, 'declined->declined': 3, 'unscorable->unscorable': 9, 'stale->other': 3, 'stale->stale': 6, 'declined->other': 2, 'other->declined': 2, 'other->stale': 2} | {'other->other': 25, 'declined->declined': 4, 'unscorable->unscorable': 9, 'stale->stale': 6, 'stale->other': 1, 'declined->other': 1, 'stale->declined': 1} | {'declined->declined': 56, 'wrong->wrong': 39, 'correct->correct': 23, 'declined->wrong': 9, 'correct->declined': 1, 'wrong->declined': 1, 'declined->correct': 1, 'wrong->correct': 1} | {'declined->declined': 56, 'wrong->wrong': 48, 'correct->correct': 23, 'declined->wrong': 2, 'correct->wrong': 2} |
| frbank|frbank_only_100 | {'other->other': 15, 'declined->declined': 5, 'other->declined': 5, 'stale->other': 6, 'stale->declined': 6, 'unscorable->unscorable': 6, 'stale->stale': 12, 'declined->other': 1, 'other->stale': 1} | {'other->other': 20, 'declined->stale': 3, 'declined->other': 8, 'other->stale': 2, 'unscorable->unscorable': 6, 'stale->stale': 11, 'declined->declined': 5, 'stale->other': 2} | {'wrong->declined': 4, 'wrong->wrong': 15, 'declined->declined': 8, 'correct->correct': 10, 'wrong->correct': 2, 'correct->wrong': 2, 'correct->declined': 1, 'declined->wrong': 1} | {'declined->wrong': 3, 'wrong->wrong': 14, 'declined->declined': 7, 'correct->correct': 11, 'wrong->correct': 3, 'declined->correct': 3, 'correct->wrong': 1, 'wrong->declined': 1} |

### AUX-R85-A2-SEAL — the blind sheet `a2/sheet_a2.md` (622 distinct answers: every obligation answer 358; the licensed random audit 20 per primary cell, seed 42, 117 distinct; the targeted licensed set 178 distinct over {'frbank|primary_178': 38, 'graphiti|primary_178': 16, 'frbank|frbank_only_100': 14} items whose detector verdict differs across conditions; rows shuffled with seed 42; no store, condition, view, tag or flag shown) sha256 `aa23e38457d7e35bca5e2cc25acb9cce81d82dc94b62508283c5782a4b1c0ea5`; the key `a2/sheet_key.json` sha256 **`44423db75a0c579aba68a5796573c8012769bb813998da8985167889221307f4`**, written before the sheet is opened. The first reader (the author) and the second reader are Step 4, not run in program R114.
