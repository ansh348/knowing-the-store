# FREEZE_R125 — the two registrations of Tasks 4 and 5, frozen together (2026-09-20; before any call on their items and before any scoring)

Each file's registered text is the bytes above its marker line (`<!-- REGISTERED TEXT ENDS ABOVE THIS LINE.`); the sha256 below is over those bytes and never changes (amendments append below the marker). The files are `reviews/r125/registrations/<name>` (the brief's fence). `r125_run.py` and `r125_t45_score.py` assert these hashes at every start (`r125_run.assert_frozen`).

| task | file | registered-text sha256 | whole-file sha256 | registered bytes |
|---|---|---|---|---:|
| T4 | `ADDENDUM_R125_SIBLING.md` | `62078c878a1654377a3a36bab0883f6e15914bdb96454eb09961c3c54ee7c350` | `25b4f69491ecc3160eefab526f7637b8c2f38bc44c056ce1677bd42414b1aa52` | 11377 |
| T5 | `ADDENDUM_R125_E2_AMENDMENT_1.md` | `41182fa7697dc402914aecea57a8bdf504b832c86f83fab136d96e5f2541462e` | `9e1b817b7715510fe227669437d90b1ff661bdc736af4c5d0c66710fee638356` | 7109 |

The tools and builds as frozen (whole-file sha256; a tool edit after the freeze is recorded as a deviation with its new hash):

| file | sha256 | bytes |
|---|---|---:|
| `tools/r125_common.py` | `b5c26be6341a4d50b3fdb4db42f1ab86fd827a8272595cf52476a089e04ec994` | 14100 |
| `tools/r125_run.py` | `2be150f2ed0c4357e55ad79bc0ecd66b4228151a8dc984a63b671323bb735c43` | 23655 |
| `tools/r125_t45_score.py` | `ea83035c9cd3e01798ddc0574e7e106b370dbd7b533d7ef9f511e901d38217f4` | 17706 |
| `tools/r125_t4_build.py` | `c3bb50df409aa50e6f9aaf04ce70c1f2ba16ee8c2b11b7e289f9c1ff87596a23` | 8296 |
| `tools/r125_t5_build.py` | `cf0800e15b148623ef8f299dfbee04c00d1fbca8dea1ff4081d62bcc17bb2c87` | 2926 |
| `build/build_t4_sibling.json` | `e9fc78a15380c1018cb13f29fc0b0f9e31cbda7d33794445e45dda982e1a1757` | 478447 |
| `build/build_t5_nc.json` | `6f6ad53eb4cf03aefe29560297840ce06f80edcaca5b761b608ed1142c5f3dfd` | 1052 |

**Budget at the freeze.** Neither API exposes a credit balance to the keys in use (OpenAI `GET /v1/organization/costs` refused for want of `api.usage.read`; the dashboard credit-grants endpoint takes a session key only; Anthropic's `cost_report` requires an Admin key; all probed 2026-09-20). In its place, the month's token-metered spend from the rows files in the tree (September 2026; files under `submission/`, `analysis/` and the `artifact_stage` copies excluded; files deduplicated by content; rows without a `when` field dated by the file's modification time): **Anthropic $143.76, OpenAI $43.78** (plus $2.14 of rows carrying no model name). E9 alone was $12.56 of OpenAI. The brief's caps for this program: Anthropic $10.00, OpenAI $10.00, enforced in `r125_run.py` (metered from the rows; checked before every synchronous call and before every Batch submission at ×1.3). The rule for NC-SOL (ADDENDUM_R125_E2_AMENDMENT_1 §6): dropped as a registered outcome if the OpenAI projection for Tasks 4 and 5 together exceeds the cap.

**Disclosure.** The scorer's pre-freeze dry run computed the three no-model readers on the SIBLING texts (ADDENDUM_R125_SIBLING §8); no model row existed. No call has been made on the SIBLING or the names-only / counts-only items by this program before this freeze. The freeze commit's hash is recorded in `NUMBERS_CF2.md` section 15d by the first ledger write.
