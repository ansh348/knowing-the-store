# NUMBERS_R141.md: the sibling-name control at 60 names (SB-60; 2026-09-23)

The ledger of R141. Registration: reviews/r141/registrations/ADDENDUM_R141_SB60.md, frozen alone at f224177 before any model call, registered text sha256 4fc25a8b01c2606be4feaaf0092cc16daecf0f2e5087384fa0eda34953f1339b. The run's results are appended below as they are scored (Phase 2).

## AUX-R141-ERRATUM-R139: the R139 report's error, recorded (the author's instruction of 23 Sep)

- reviews/r139/REPORT_R139.md, under 'Branches fired', says the length-reader branch landed "the ruled B5 text in words, plus the Limitations sentence".
- The Limitations sentence was never landed. The author ruled it on 22 Sep: "The padded lists keep the PN list longer than its siblings', as the short list does; only the short list has the sibling-name control, so the two padded leads are not separated from that cue, and siblings padded to equal length are untested."
- The sentence is absent from:
  - the R139 close (3342217);
  - the R140 close (86a72dd, 42b6951);
  - the fallback PDF (reviews/fallback/, 233acc7).
- It was found during R141 Phase 0 on 23 Sep.
- The author ruled that the fallback stays as built. Its abstract ("A list-length cue is uncontrolled there.") and 5.2 ("the padded set has no such control") carry the limitation.
- Under R141 the B-i and B-iii Limitations sentences are additions, not replacements.

## AUX-R141-BUILD: SB-60 (reviews/r141/tools/build_sb60.py → reviews/r141/build/build_sb60.json)

- **Pairs:** 88.
- **Texts:** SB-60 texts sha256 9346d52dbf677c127f78b6aabfa630282b771151146cfb61af84bd69f925fa74.
- **Substitutes:** 35 collision substitutes, by numpy default_rng(42), one draw per collision pair in pair-id order. 23 of the 35 differ from the pool's first name.
- **Checks, 88 of 88:**
  - the renderer reproduces every text byte for byte;
  - every list holds 60 distinct names;
  - the target is in no SB-60 list;
  - the sibling is in no PN-60 list;
  - the prefix is identical;
  - exactly one name differs;
  - no overflow.

## AUX-R141-NOMODEL: recorded before the freeze (reviews/r141/results/nomodel_sb60.json)

PN-60 against SB-60, matched:

| Reader | Matched (W/T/L) | Pooled |
|---|---|---|
| Name lookup | 0.8239 (57/31/0), triple [0.7727, 0.8750], persona [0.7670, 0.8816] | 0.7395 |
| Lexical lookup | 0.7386 (42/46/0) | 0.6815 |
| Random-token lookup | 0.5000 (1/86/1) | 0.5006 |
| Length-only reader | 0.5000 (0/88/0) | 0.5000 |
| Count reader | 0.5000 (0/88/0) | 0.5000 |

SB-60 against the padded PRESENT version:

| Reader | Matched |
|---|---|
| Name lookup | 0.5227 |
| Lexical lookup | 0.5114 |
| Random-token lookup | 0.5057 |
| Length-only reader | 1.0000 |
| Count reader | 0.6932 |

## AUX-R141-SOURCE-SWEEP: a standing rule

Any future source upload (arXiv) must pass the builder's full identity sweep (package/tools/build_r138.py SCAN_TERMS, every encoding) over every .tex, .py and .md it carries. This is the author's ruling of 23 Sep. The repo-wide sweep and its count land with the R141 landing commit (L0).

## AUX-R141-DISCREPANCIES: recorded under the author's ruling 3 on the B-ii stop

- The registration date. ADDENDUM_R141_SB60.md's date line reads "24 Sep"; that is an error copied from the brief. The freeze commit f224177 is dated 2026-09-23 12:23:32 +0300, day 44 (day 0 = 2026-08-10), and the commit date governs. The frozen registration text is not edited. The same error was carried into the messages of the R141 commits f224177, 82f522f, 7e83668, 2588717 and 7a62892 ("2026-09-24") and into this ledger's first lines; the ledger lines are corrected here to 23 Sep, the commit messages stay as committed, and the git commit dates govern for all of them. The number gate reads the day from git (r141_number_gate.py, 'the freeze day of f224177').
- R140's A2 comparison list. R140's abstract sentence "Under a control that fixes counts and list length, none is reliably above it and none is shown equivalent." was missing from reviews/r139/results/n_list_r139.json; it was added in R141 and adds no new comparison (its five sibling-name comparisons were already counted), so R140's printed count stands.
- Luna's wording deviation. By the author's ruling 1 on the B-ii stop, Section 5.2 reads for Luna "Luna's lead holds on the pooled metric only ($0.11$, reliable) and not within triples ($+0.04$; ...)", against the registered B-ii clause "Luna's lead is not separated from the cue". The registration promised the pooled reading beside the matched one; the paper names the pooled metric where the two disagree. The Limitations sentence keeps the registered clause. Recorded in Appendix C.2 as well. Numbers: pooled +0.1122 (reliable), matched +0.0398 (not reliable), AUX-R141-RESULTS.
- The last line. Payers a, b, c left the probe at +0; R139's R1 to R5 and the ruled payers (i) to (iv) each left +0 and were reverted by the author's ruling (a cut that recovers nothing is not kept). Payer (v), Limitations' two alignment sentences merged into one, gave +1 (reviews/r141/results/slack_r141.md); probing stopped there. Close units: l0 l1 l2 l4 l5 pa pb pc s5.
- A2's count. With (i) reverted the Graphiti sentence stays in Section 7, so A2's recomputed count is 71 (70 with (i), the ruled figure, plus the Graphiti comparison restored); reviews/r139/results/n_count_r139.json.

## AUX-R141-RESULTS: SB-60 scored (reviews/r141/tools/score_sb60.py → reviews/r141/results/scores_sb60.json; run 2588717 under f224177)

Census (the rows): GPT-4.1 mini 440/440 OK, served ['gpt-4.1-mini-2025-04-14'], $0.2440; GPT-5.6 Luna 440/440 OK, served ['gpt-5.6-luna'], $0.1563; GPT-5.6 Sol 440/440 OK, served ['gpt-5.6-sol'], $2.5048. The leak screen 0 of 30 correct (PASS, $0.0179); probes and leak included, OpenAI $2.9372 of the $12 cap (token-metered from the rows, not an invoice).

| reader | PN-60 vs SB-60 W/T/L | matched | triple interval | persona interval | pooled AUROC | SB-60 vs padded PRESENT (matched) |
|---|---|---:|---|---|---:|---:|
| GPT-4.1 mini | 62/5/21 | 0.7330 | [0.6420, 0.8239] | [0.6455, 0.8193] | 0.5931 | 0.6307 |
| GPT-5.6 Luna | 76/0/12 | 0.8636 | [0.7955, 0.9318] | [0.8043, 0.9259] | 0.8517 | 0.6818 |
| GPT-5.6 Sol | 80/0/8 | 0.9091 | [0.8523, 0.9659] | [0.8506, 0.9620] | 0.8633 | 0.5114 |
| Name lookup | 57/31/0 | 0.8239 | [0.7727, 0.8750] | [0.7670, 0.8816] | 0.7395 | 0.5227 |

The no-model readers as tab:sb60 prints them (reviews/r141/results/nomodel_sb60.json, recorded before the freeze):

| reader | PN-60 vs SB-60 W/T/L | matched | triple interval | persona interval | pooled AUROC | SB-60 vs padded PRESENT (matched) |
|---|---|---:|---|---|---:|---:|
| Count reader, guessed category | 0/88/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] | 0.5000 | 0.6932 |
| Length-only reader | 0/88/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] | 0.5000 | 1.0000 |
| Lexical lookup | 42/46/0 | 0.7386 | [0.6875, 0.7898] | [0.6875, 0.7927] | 0.6815 | 0.5114 |
| Name lookup (embedding) | 57/31/0 | 0.8239 | [0.7727, 0.8750] | [0.7670, 0.8816] | 0.7395 | 0.5227 |
| Random-token lookup | 1/86/1 | 0.5000 | [0.4830, 0.5170] | [0.4837, 0.5170] | 0.5006 | 0.5057 |

Each model minus the name lookup (paired on the same pairs; reliable: both 95% intervals exclude zero; equivalent: both 90% intervals inside [-0.05, +0.05]):

| model | metric | difference | 95% triple/item | 95% persona | 90% triple/item | 90% persona | reliable | equivalent |
|---|---|---:|---|---|---|---|---|---|
| GPT-4.1 mini | matched | -0.0909 | [-0.1818, +0.0001] | [-0.1889, +0.0108] | [-0.1648, -0.0114] | [-0.1744, -0.0104] | no | no |
| GPT-4.1 mini | pooled | -0.1464 | [-0.2110, -0.0778] | [-0.1920, -0.1006] | [-0.2027, -0.0866] | [-0.1848, -0.1079] | yes | no |
| GPT-5.6 Luna | matched | +0.0398 | [-0.0284, +0.1080] | [-0.0112, +0.0987] | [-0.0227, +0.0969] | [+0.0000, +0.0883] | no | no |
| GPT-5.6 Luna | pooled | +0.1122 | [+0.0521, +0.1732] | [+0.0688, +0.1575] | [+0.0591, +0.1656] | [+0.0754, +0.1495] | yes | no |
| GPT-5.6 Sol | matched | +0.0852 | [+0.0284, +0.1420] | [+0.0322, +0.1398] | [+0.0398, +0.1364] | [+0.0384, +0.1316] | yes | no |
| GPT-5.6 Sol | pooled | +0.1238 | [+0.0615, +0.1911] | [+0.0812, +0.1645] | [+0.0702, +0.1777] | [+0.0874, +0.1575] | yes | no |

The predictions (matched endpoint; the pooled reading beside it):

- P-S1 (Luna exceeds the name lookup on PN-60 vs SB-60 with both intervals clear of zero): **FAILS**; pooled reading holds
- P-S2 (Sol exceeds the name lookup on PN-60 vs SB-60 with both intervals clear of zero): **HOLDS**; pooled reading holds
- P-S3 (mini does not reliably exceed the name lookup): **HOLDS**; pooled reading holds
- P-S4 (each of Luna and Sol at or above 0.80 matched on PN-60 vs SB-60 with the persona interval above 0.50): **HOLDS**; {"GPT-5.6 Luna": {"matched": 0.8636, "persona_lo": 0.8043422232182877}, "GPT-5.6 Sol": {"matched": 0.9091, "persona_lo": 0.8505747126436781}}

**Branch fired: B-ii** (P-S1 fails, P-S2 holds); the named reader Sol.
Seeds 43 to 46 on every registered difference (both metrics, the reliable and equivalent flags): reading changes none.

Scoring note: the name lookup is computed for all three versions in one process (emb_cached), as the recorded values of the registration's §6 were; mixing the stored R136 floats with fresh ones breaks exact ties at the last digit (62/21/5 against the recorded 57/31/0). The stored vectors are asserted equal at 1e-6 and the recorded W/T/L is asserted reproduced. Departure recorded: the lanes called R125's Chat Completions call shape (r125_run.call_openai) with R136's settings, not cf2_openai.call_once.

Printed forms (two decimals, half-up): the lookup's matched score on PN-60 vs SB-60 0.82; Sol's matched lead 0.09 (reliable); Luna's matched lead 0.04 (not reliable).

