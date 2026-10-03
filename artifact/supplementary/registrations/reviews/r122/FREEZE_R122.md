# FREEZE_R122 — the four registrations of the no-human batch, frozen together (2026-09-19; before any call and before any scoring)

Each file's registered text is the bytes above its marker line (`<!-- REGISTERED TEXT ENDS ABOVE THIS LINE.`); the sha256 below is over those bytes and never changes (amendments append below the marker). The files are `reviews/r122/registrations/<name>` (the brief's fence; D-R122-3). Every runner and scorer asserts its registration's registered-text sha256 against this table at start (`r122_common.assert_frozen`). T2 (the hybrid reader) is not registered here: R120 drafted it first (`PHASE0_REPORT.md`).

| task | file | registered-text sha256 | whole-file sha256 | registered bytes |
|---|---|---|---|---:|
| T1 | `ADDENDUM_R122_ENCODERS.md` | `eb0553ba2720fa1c2cffa0be062ba892d1f174d1381cf13db104adb2ad9f7da1` | `09c40622ce4021f497cd4f0662d5a2dafbdb85906a1ac7b758785ab015031b27` | 7039 |
| T3 | `ADDENDUM_R122_MINI_K5.md` | `953e94a2616cf3edea0e4ca2acd2f51459ec0671004e4ddc20b202df54019f17` | `3a4ae8e694eba272ba8e81fdbe6239544288682d18a7c0c0b90d3e111698cc35` | 8479 |
| T4 | `ADDENDUM_R122_CF2_P1.md` | `f8a42bf52274caea9c79515e0b57b25f9c6346bac218a943500c52c1fbbb6df5` | `46f27207fb5d83807734b775a425dd7ad0037ae05143348ad73fcaea9cc244a8` | 9092 |
| T5 | `ADDENDUM_R122_GATE_REACH.md` | `1176a8af2158fc7fa1c0517d7003b55e0542bae440411ea1a6291e383e710b4e` | `399bc452e2c9bc3e449031aff08337c4393ed1ef31893ea2754455ce3036bc10` | 9618 |

The tools as frozen with the registrations (whole-file sha256; the scorers' estimands are fixed by the registrations, and a tool edit after the freeze is recorded as a deviation with its new hash):

| tool | sha256 | bytes |
|---|---|---:|
| `tools/r122_common.py` | `aedb4eda8a8bb6f3bbfe4108fb447ae46f5e2aacb041fbdb5880a5b9ccd6e8d0` | 4940 |
| `tools/enc_lookup.py` | `e5dfb013b04025dd13e6d95bf944131b3261c2bc28903c884de65e30829cf30a` | 13618 |
| `tools/oai_run.py` | `debb503d301116198ce42fbf820393374a1e8daa6f4c4f123be073e564a83f72` | 11410 |
| `tools/oai_score.py` | `eb4f5405229a5cce60e9590d056fc90cdd17aa3dfd6fee26cd10116fb57c8d7d` | 12425 |
| `tools/gate_reach.py` | `18cfbd538a7d5092a9897792300f1e36644e9f50c9828a009c3b91a3e2b9bf53` | 23726 |

Also committed with the freeze: `PHASE0_REPORT.md` (the collision check, the environment checks, the cost projection) and `DEVIATIONS_R122.md` (D-R122-1, -2, -3). No call has been made; no scoring has been run beyond the recorded-row gates the tools' `check` subcommands assert. The freeze commit's hash is recorded in `NUMBERS_R122.md` section 0 by the first ledger write.
