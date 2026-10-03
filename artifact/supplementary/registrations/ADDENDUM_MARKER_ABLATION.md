# ADDENDUM_MARKER_ABLATION: the inexpressibility marker on Mem0 and A-MEM, omitted and neutralized (E3)

Registration for the author's freeze (program R117; drafted 2026-09-18 BEFORE any call, the author's rulings of 2026-09-19 folded in: E1.5 Run B reused as the mini Omitted arm and reported as a recorded result, P-X1 dropped for mini, P-X2 kept for the Neutral arm, the Neutral wording fixed, the wrapper's quoted marker string replaced by the same text, Luna on four raw-API arms). Carries one prediction (P-X2) with its failure text and one descriptive reading (P-X3). Frozen by its sha256, recorded in `e1_metamemory/NUMBERS.md` (a new section) before the first call; each runner writes a lock with that hash at start. Nothing here re-adjudicates the inversion rows (`tab:inversion`), R74 X2, E1.5 Run B or Q4; the recorded blind, intact and no-marker rows are read and never re-run.

## §1: Why

Under the constrained rendering GPT-4.1 mini loses $0.10$ on Mem0 and $0.11$ on A-MEM against blind, and on the pooled 66 questions GPT-5.6 Luna loses $0.34$ and GPT-5.6 Sol $0.10$ (Section 7); Limitations says the cause is unidentified. Three readings of the marker exist: R74 X2c deleted the marker lines and kept the wrapper's marker sentence (Mem0 $-0.0949$, A-MEM $-0.0886$); E1.5 Run B (H-b) omitted the marker lines, the emptied section headers and the wrapper sentence (`USER_INDEXED_NOMARKER`; Mem0 $-0.0865$, A-MEM $-0.0378$); Q4 kept the text and appended an instruction to read the marker as absence. This addendum adds the neutral reading and puts the omitted reading and the neutral reading beside blind and intact on one table, for GPT-4.1 mini on both coverage populations and for GPT-5.6 Luna on the pooled 66.

## §2: Population and the recorded rows

The recorded external-store coverage items of the main study: Mem0 n = 238 (94 positive), A-MEM n = 284 (126 positive), the scoreable items of `e1_metamemory/build/items_final.json` with `backend in {mem0, amem}`, 77 index keys (`e1_metamemory/indexes_v2.json`, keys `<backend>:<persona>:<variant>:TRUE`; the three marker lines are the bodies of `PER-CATEGORY BREAKDOWN`, `ATTRIBUTE NAMES BY CATEGORY` and `ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT`). Positives for FOK are non-ABSENT items. Recorded rows read: blind and intact (`elicitation_main.json`, arms BLIND and INDEXED-TRUE; intact 0.4777 / 0.4526, deltas $-0.0969$ / $-0.1065$, reproduced before any call); **OMITTED = the recorded E1.5 Run B rows** (`e1_metamemory/run_b_nomarker.json`, 522 rows, `results/run_b_hb.json`; `tools/run_b.py strip_markers` + `USER_INDEXED_NOMARKER`), re-scored, not re-run. The pooled 66: the 29 Mem0 and 37 A-MEM items of the 150-item frontier subset (`e1_metamemory/strong_model.json`).

## §3: Arms

- **OMITTED** (recorded for GPT-4.1 mini; new for Luna): the three inexpressible sections left out entirely, header and body, no marker and no mention; the wrapper is the frozen `prompts_e1.USER_INDEXED_NOMARKER` (its marker sentence gone). Built by `run_b.strip_markers`, asserted byte-identical to the recorded Run B inputs on the 522.
- **NEUTRAL** (new): each of the three marker bodies `not expressible by this backend` becomes **`This store does not record this. Judge it from the question alone.`** (fixed by the author's ruling of 2026-09-19); the section headers stay; every other line byte-identical to the intact text. Wrapper: `prompts_e1.USER_INDEXED` with its quoted marker string `"not expressible by this backend"` replaced by the same text, `"This store does not record this. Judge it from the question alone."`, and nothing else in the wrapper changed (the ruling); the variant is built at run time from the frozen text by that one substitution, asserted, and its sha256 recorded. Built by a committed pure function, `e1_metamemory/tools/marker_arms.py`, lock asserted per key: exactly three replaced lines, nothing else changed.
- **STRUCTURAL** (the intact constrained rendering, `indexes_v2.json` `...:TRUE`, the recorded arm) and **BLIND**: recorded rows for GPT-4.1 mini; run through the raw API for Luna (below).

## §4: Lanes

GPT-4.1 mini on the 522: NEUTRAL only (OMITTED is on the record), k = 1, temperature 0, seed 42, max_tokens 200 (the E1 protocol, `e1_metamemory/tools/api.py`, a fresh cache namespace). GPT-5.6 Luna on the pooled 66, k = 5, raw Chat Completions API, effort and temperature unset, `max_completion_tokens` 2048 (the R74 X4 settings), MIN_DRAWS 3, **four arms: BLIND, STRUCTURAL, OMITTED, NEUTRAL** (1,320 calls; the ruling). The recorded Luna blind and intact rows on these 66 are the August `codex exec` rows (reasoning effort low, the vendor's agent harness, no telemetry; Phase 0 item 6), so the paired losses for Luna are read within the raw-API transport, and the harness rows print beside as the row they are. Served identifiers probed before each lane. Rows under `e1_metamemory/marker/`.

## §5: Estimands and predictions

Per backend for GPT-4.1 mini, and on the pooled 66 for Luna: FOK AUROC per arm; the paired difference against blind (the inversion) per arm with item-level and persona-grouped intervals (1,000 draws, seed 42); the share of items at the modal score per arm (the tie census). The Luna comparisons (OMITTED and NEUTRAL against BLIND and STRUCTURAL) are read within the raw-API transport; the recorded harness rows on the 66 print beside as the rows they are, marked as Appendix B marks them.

- **The Omitted arm for GPT-4.1 mini is a recorded result, not a prediction** (the ruling; P-X1 dropped): the E1.5 Run B rows print as they stand, A-MEM $-0.1065 \to -0.0378$ (the loss shrinks by 65%), Mem0 $-0.0969 \to -0.0865$ (11%), with both intervals recomputed by this addendum's scorer beside the recorded ones.
- **P-X2.** Under NEUTRAL, coverage is within tolerance of blind on each backend for GPT-4.1 mini: $|\Delta| \le 0.05$ against the recorded blind row on Mem0 and on A-MEM.
- **P-X3 (descriptive).** The share of items at the modal score falls under OMITTED and under NEUTRAL against STRUCTURAL, on each backend for GPT-4.1 mini and on the 66 for Luna.

Failure text, frozen: "P-X2 FAILS on [Mem0 / A-MEM / both]: under the neutral wording the coverage loss against blind is $\Delta$ with intervals $I_{item}$ and $I_{persona}$, outside tolerance."

## §6: Held texts, both branches (Phase 3, by ruling)

- P-X2 holds: Section 7's structureless paragraph gains one clause, "and a wording that tells the reader the store does not record a field, instead of marking it inexpressible, returns coverage to blind"; the Limitations clause on the unidentified cause is replaced by "the loss traces to the marker's wording (Appendix E.7)". The slogan-pinned inversion sentence is not edited without a ruling.
- P-X2 fails: the clause reads "and rewording the marker does not remove the loss ($\Delta$ on Mem0, $\Delta$ on A-MEM)"; the Limitations clause stays. In both branches Appendix E.7 gains `tab:marker`: blind, intact, omitted, neutral per backend for GPT-4.1 mini and on the 66 for Luna, with the paired differences and both intervals, and the modal-share column.

## §7: Budget, order, STOP

GPT-4.1 mini NEUTRAL: 522 calls at the recorded external-store prompt size (about 790 tokens, 25 out) **$0.18**; GPT-5.6 Luna four arms × 66 × 5 = 1,320 calls at the X4 per-call figures (blind $0.000263, indexed-size $0.00039; page prices $0.20 / $1.20, prompts under 1,024 tokens so no cache write) **$0.46**; probes $0.01; **$0.65 against the $5 cap (×1.3: $0.85)**. If only the two new Luna arms are wanted, $0.25. Order: renderer (no call) → locks → the Run B rows re-scored → mini NEUTRAL → Luna. STOP: registration sha256 mismatch; a lock failure; served-identifier mismatch; more than 2% of a lane's rows not OK after the retry; a projection over the cap.

## §8: Ledger and paper site

`e1_metamemory/NUMBERS.md` section 12: `AUX-MARKER-LOCK`, `-OMITTED-MINI` (from the Run B rows, a recorded result), `-NEUTRAL-MINI`, `-LUNA-66` (four arms), `-MODAL`, `-P-X2`, `-P-X3`, `-SPEND`. Paper: one clause in Section 7, the Limitations clause, `tab:marker` in Appendix E.7.

## Registration mechanics

Frozen by sha256 before the first call. Copied to `iclr2027_monitoring_submission/ARTIFACT/registrations/`. Amendments, if any, are appended as dated sections below the marker line and never edit the text above. The run proceeds on the author's freeze commit; nothing runs before it exists.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
