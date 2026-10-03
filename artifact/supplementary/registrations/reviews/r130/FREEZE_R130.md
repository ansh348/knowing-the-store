# FREEZE_R130 — the registration of program R130, frozen before any call on any item and before any scoring (2026-09-20)

The registered text is the bytes of `reviews/r130/registrations/REGISTRATION_R130.md` above its marker line (`<!-- REGISTERED TEXT ENDS ABOVE THIS LINE.`); the sha256 below is over those bytes and never changes (amendments and rulings append below the marker). `r130_common.assert_frozen` asserts it at the start of every tool that calls an API or scores.

| file | registered-text sha256 | whole-file sha256 | registered bytes |
|---|---|---|---:|
| `REGISTRATION_R130.md` | `2e95beab2451ab8d87b746e4e15b65a04c30805a252e8c23bfac03072f00253c` | `b881593a394e2c62c6e01526117443832759a34b7270a0c085ab2f0c4aa5b42c` | 27452 |

The tools and builds as frozen (whole-file sha256; a tool edit after the freeze is recorded as a deviation with its new hash):

| file | sha256 | bytes |
|---|---|---:|
| `tools/r130_common.py` | `27fa4f75ae8a4637777c709138443561fdbeb887419f105d36a81012a9fdc568` | 21229 |
| `tools/r130_build.py` | `47992db1096dd2a1636d35cb7ac2056c9f8439d76f596f27898b63be7447b0bf` | 9539 |
| `tools/r130_run.py` | `7489909f3c7f6f7bc7fe7a73883500e35daaee851450bb7b60cca48e009d37c5` | 22773 |
| `tools/r130_score.py` | `11e7d73cc6ac8474e143324f72aced2cd5ca6a0c7e181294970aa8955d33a302` | 31360 |
| `tools/r130_validate.py` | `cf9c65418c2ed8d4cd75f313fa35f70e1ec283716bcd2918399a0a669250e9d2` | 11570 |
| `tools/r130_report.py` | `c0ec1373ef86e403139a0bc3b506c4d9e5ccbce64ac22d1b5000756008669827` | 7158 |
| `tools/r130_dryrun.py` | `4bb2159f69fe65b6567021c29741f9fb2466297c92f2e41272a9449baa17dca1` | 3902 |
| `build/build_r130.json` | `32dea3332ae21164fbdc0f59a4e0ee2aa0d1ea9a6f065277c6b9847493f4584f` | 1229615 |
| `build/luna_settings_check.json` | `497ec3139baa07ff526a0f8a1687594c8ac71bcc8ae11d830cc4b1338c8dbb65` | 867 |

The build (`build/build_r130.json`, built 2026-09-20T14:39:11): 305 views (231 of the Amendment 4 population, 74 retagged), views sha256 `ad0e60e53224f20d2d568fe70988adfce702527f3b09a1956711f8cc32f61f78`; 610 recorded judge units, units sha256 `24bd8d775a89296ed30efa919c1dc5b061335f6af648f7e78867a327f148b160`; the HV1 key lock 248 of 248 ({'haiku': 50, 'primary': 198}); judge prompt digests `d0e27a76e0ecce50` (system) and `9c4f6c234315dbb4` (user), equal to the registration's fenced blocks (asserted). Input digests as the registration's §11 and `r130_common.INPUTS`.

**Every generation setting, recorded here (rulings 4 and 5 of 2026-09-20).**

- Lane LUNA (Task A): `{"max_completion_tokens": 2048, "model": "gpt-5.6-luna", "price": {"cached": 0.02, "inp": 0.2, "out": 1.2, "write_mult": 1.25}, "reasoning_effort": null, "response_format": {"type": "json_object"}, "seed": 42, "temperature": null}`; raw Chat Completions (`openai` 2.24.0), one draw, eight workers, the answer from the last JSON object of the reply, one retry on a parse failure; the served identifier asserted per row. The settings check that fixed these (`build/luna_settings_check.json`, 2026-09-20T14:37:41; a one-line prompt with no item text, two calls, about $0.0001): `{'temperature': 0, 'seed': 42, 'response_format': {'type': 'json_object'}}` → rejected (BadRequestError: Error code: 400 - {'error': {'message': "Unsupported value: 'temperature' does not support 0 with this model. Only the default (1) va); `{'seed': 42, 'response_format': {'type': 'json_object'}}` → accepted, served `gpt-5.6-luna`. Mini's `max_tokens` 200 is not mirrored: Luna's `max_completion_tokens` counts reasoning tokens, so E5's 2048 stands.
- Lane JUDGE (Task B): `{"batch_mult": 0.5, "max_tokens": 300, "model": "claude-opus-5", "price": [5.0, 25.0], "temperature": 0.0}`; Message Batches (`anthropic` 0.84.0), one request per unit, the label from the last JSON object; a unit without a label re-asked once synchronously at list price; the served identifier asserted per row. Prompt: `JUDGE_SYSTEM` / `JUDGE_USER` of the registration's §4, asserted byte for byte before any judge call. UNSURE is not ASSERTS and not MENTIONS in every primary reading; the sensitivity row drops UNSURE units.
- Statistics: exact McNemar (two-sided binomial on the discordant pairs) or Fisher's exact test for the two-group P-L3 / P-L3b; percentile bootstraps, 10000 draws, seed 42, item-level and persona-grouped.

**Caps.** OpenAI $4.00, Anthropic $8.00, metered from the rows at the page prices (Luna $0.20 / $1.20 per M, cache write ×1.25, cached $0.02; Opus 5 $5 / $25 per M at the 0.5 Batch multiplier; list price for the probe and any synchronous retry), checked before every synchronous call and before the Batch submission at ×1.3.

**Credit at the freeze.** Neither API exposes a balance to the keys in use (R125 probed the endpoints on 2026-09-20). September's token-metered spend: at R125's freeze Anthropic $143.76 and OpenAI $43.78; R125 then metered Anthropic $7.68 and OpenAI $2.94; R129 was $0; so about **Anthropic $151.44, OpenAI $46.72** to date, this program's settings check $0.0001 beside. Pre-probe projection for this program: Luna 305 calls about $0.15–0.25, the judge about 915 units about $2.5 at Batch.

**Disclosures.** The tools were dry-run on a synthetic fill in the scratchpad (numbers meaningless, not committed); no call has been made on any view or unit of this program before this freeze; the only calls before it are the two of the settings check above. The judge shares a vendor with one answerer (Haiku 4.5); the judge is validated on mini's answers only (registration §2i).

The freeze commit's hash is recorded in `REPORT_R130.md` and in NUMBERS_DS.md section 16 by the first ledger write.
