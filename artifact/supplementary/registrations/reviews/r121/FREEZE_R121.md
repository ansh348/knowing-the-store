# FREEZE_R121 — ADDENDUM_CF2_INTENT_CROSSOVER frozen (2026-09-19, Phase 2; before any monitor call)

The registered text is the bytes above the marker line of `registrations/ADDENDUM_CF2_INTENT_CROSSOVER.md`; the sha256 below is over those bytes and never changes (amendments append below the marker). Copy in `iclr2027_monitoring_submission/ARTIFACT/registrations/` (byte-identical at the freeze). The freeze commit's hash is recorded in the runner's lock (`cf2/rows/lock_ix.json`) and in the ledger (`cf2/NUMBERS_CF2.md` §14d, AUX-CF2-IX-LOCK) before the first call; every runner asserts the registered-text sha256, the P0 digests, the P1 sha256, the cue-list sha256 and the questions' sha256 at start.

| file | registered-text sha256 | whole-file sha256 | registered bytes |
|---|---|---|---:|
| `ADDENDUM_CF2_INTENT_CROSSOVER.md` | `9480d6bbcfef47d25c2711d0c42f9c05d7dc2239fdddb371205a07923675711a` | `a8fe82579bea3efde1a6556a12f6fc72b080f9884f7afe8975ffaf5644f31af8` | 27078 |

Inputs pinned by the registered text: instruction v2 prompt sha `ee92835120c2f76891e02cdbde2fadc8976bc1258d1fcfca7aa8d20d31b809f9`, lineage-2 sha `090d796e05ff5bc215809cca560aef89135407c699bf3541e72871546b48ee92`; questions sha256 primary `efa8eeee63db25674d68a1e1067cdc5d3e9ea837d2ce2c8f68d063ba5dee195e`, lineage 2 `c488db0c316d8bd7f5f8deeb1f459cf3ef65fd6aa4c8ad7357cdadaf6bf1128b`; cue list v2 `a63461d09d5c60c44009c05b004657394a854ab10d468f80bf9377625f8fb9a8`; P1 system text `c3c9a8e2b9798b50aa5a8f091f382b550e296f973f0c9af09d7fa38442cc7ce4`; workbook as built `bbde1710225ecad7a6e7846e4fd1863d1ac26b81c94133dd33af755168406bb5`, returned `be79963e0a328761aec0ca0d0300de78efc8ef1d114254a0540fcbf1ae585c49`; populations A 87, B 26 (113 pairs).

## Amendment 1 (2026-09-19; approved by the author, cap 12 USD): GPT-5.6 Sol as a fifth reader

Appended below the marker line of `registrations/ADDENDUM_CF2_INTENT_CROSSOVER.md` (the registered text above the marker unchanged, sha256 `9480d6bb…` re-asserted at the append); the artifact copy byte-identical. **Amendment-1 text sha256 `2a21bcce8257c551450896bcb17668cefbfd5573f89bc318256bc8f80057c1e6`** (over the amendment's bytes, from its `## Amendment 1` heading to the end of the file; `reviews/r121/AMENDMENT_1_DRAFT.md` holds the same bytes). The Sol runner asserts both hashes at start and writes `cf2/rows/lock_ix_amend1.json` with the freeze commit's hash before its first call. Disclosure: the lane was added after the interim read of three lanes (§14d-interim) while the Opus 5 batch was running and unread; P-I2b is labelled as made after that read.
