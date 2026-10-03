# FREEZE_R117 — the five registrations frozen together (2026-09-19)

Each file's registered text is the bytes above its marker line; the sha256 below is over those bytes and never changes (amendments append below the marker). The files are `registrations/<name>` with copies in `iclr2027_monitoring_submission/ARTIFACT/registrations/`. The freeze commit's hash is recorded in each experiment's ledger before its first call; every runner asserts the registered-text sha256 at start and writes it into its lock.

| experiment | file | registered-text sha256 | whole-file sha256 | registered bytes |
|---|---|---|---|---:|
| E1 | `ADDENDUM_V2R_CAT_AMENDMENT_1.md` | `30d102eddbb9166d3c505871818ab255807ec68f0a9c3962438aeba1ac850d0e` | `a40e645bc4bb846c5c21318b9ab6f092e4027cd94ace981bb24e2530b4962727` | 5915 |
| E2 | `ADDENDUM_CF2_NAMES_COUNTS.md` | `6cd4cb94c3a3a4dce43da23640fbf05828f93da0d322f3f9db7da0761768db2c` | `a6cb0fdc1bd590271debaf261d15078aedbda4339a53c8d93553fb99d03d03eb` | 7973 |
| E3 | `ADDENDUM_MARKER_ABLATION.md` | `6d3afee82f2364b8d441ac097cae7917d3d0ec5f5b773317a8fd9a215e926d48` | `c47cb52e442ff128c4253bb5aed1149028fb81ce3823510a6c713587ad01e12e` | 8464 |
| E4 | `ADDENDUM_DS_AMENDMENT_8.md` | `c57cda878aa80df7902e4ae35fc49504483a27a3032497a76e1c3b2e8050502c` | `3e518ebf0f4b185d503058c816f22a8a6ad7dc546d39eacc4d7379758955a6a1` | 10084 |
| E5 | `ADDENDUM_CF2_OPENAI.md` | `230df444e3d5f028102426508e0d883824eb1258576515fadab49fbb84483149` | `0b5af64f9400e7361115d2e14e2867f3bf0077ae2dc7d420988e841050fcebb3` | 7294 |

The author's rulings of 2026-09-19 (`reviews/r116/RULINGS_R116.md`) were folded into the drafts by `reviews/r117/tools/fold_rulings.py` before the freeze; the Phase 0 report (`reviews/r117/PHASE0_REPORT.md`) and the E5 cost report (`scratch/e5_cost/REPORT_E5_COST.md`) are committed with them. Two untracked drafts of another session, found at `registrations/ADDENDUM_V2R_CAT_AMENDMENT_1.md` and `ADDENDUM_DS_AMENDMENT_8.md` (18 September 23:29 and 23:32, before the Phase 0 report the rulings answer), were moved unread to `reviews/r117/other_session_drafts/` so that nothing was overwritten; they are not registrations.
