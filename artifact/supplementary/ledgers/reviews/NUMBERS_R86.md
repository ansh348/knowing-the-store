# NUMBERS_R86 — the number record for values R86 re-derived

R86 is a writing program and produces no measurements. This file exists for the one class of
value it does produce: a **recount of a committed census over a corrected population**, where
the paper's printed figure and its own scored population disagreed. Each row states the
artifact, the method, and the value it replaces, so a reader can re-run it rather than trust
it.

Registered in `iclr2027_monitoring_submission/tools/trace_scan_v13.py`'s `LEDGERS` list, on
the precedent that file's own change note 2 records for `NUMBERS_R82.md`.

---

## `AUX-R86-AMEM-LINKS` — the A-MEM link census, over the scored population

**What the paper printed before:** all **23,403** link references resolve to zero note
identifiers (Section 6 and Table 21).

**What it prints now:** **23,186** link references across **11,319** notes, none resolving to
a note identifier.

**Why it changed.** 23,403 counts **all 41** bank directories under
`LifeMemEval/artifacts/amem_banks/`, including `priya.canary`. That bank is excluded
everywhere else in the study: `e1_metamemory/tools/backends.py:71` sets
`AMEM_EXCLUDE = {"priya.canary"}`, and `e1_metamemory/PHASE0_CENSUS.md` records it as a broken
bank whose sidecar claims 293 notes while the store holds 101. The entry count the paper and
the census already use, **11,319**, is the excluded-canary figure. So the printed link count
and the printed entry count were taken over different populations. Correcting the link count
puts both on the scored 40 personas.

| population | bank directories | notes | link references | resolving to a note id |
|---|---|---|---|---|
| scored (canary excluded) | 40 | **11,319** | **23,186** | **0** |
| all directories | 41 | 11,420 | 23,403 | 0 |
| `priya.canary` alone | 1 | 101 | 217 | 0 |

**Method, reproducible with no API call.** For each bank directory except `priya.canary`, open
`chroma.sqlite3` read-only and immutable, read `embedding_metadata` rows whose `key` is `id` or
`links`, group by `id`, parse each `links` value as JSON, and count the references. Resolution
is checked by membership of each reference in the set of note ids, both within the persona and
against the global id set across all personas.

**What the references actually are.** The distinct values across the whole corpus are exactly
the empty string, `"0"` through `"5"`, and `"memory index:0"` through `"memory index:5"`. They
are positional indices into an ephemeral neighbour list, and no note identifier is ever
written.

**Why that is stock behavior, from the upstream source** (`agentic-memory` 0.0.1,
`github.com/agiresearch/A-mem`, MIT), in
`.venv/Lib/site-packages/agentic_memory/memory_system.py`:

- `process_memory` renders each neighbour as `memory index:{i}`, so the evolution prompt shows
  positional indices and carries no note identifiers;
- the prompt nonetheless asks the model for `"suggested_connections": ["neighbor_memory_ids"]`;
- on the `strengthen` action the code runs `note.links.extend(suggest_connections)`, storing
  what came back with no index-to-identifier mapping anywhere;
- the read path, `search_agentic`, calls `self.memories.get(link_id)` and silently gets `None`.

Recorded under **D-R86-8**'s companion ruling (option (b)). The claim scope is deliberately
narrow: this package at this version under this ingestion. No claim is made about A-MEM
deployments generally.

---

## `AUX-R86-INDEX-EXCERPT` — the age lines of the Section 3 serialized-index excerpt

Section 4.4 states that the count-destruction probe left "ages, markers, and names" untouched,
but the Section 3 excerpt showed no age field, so a reader could not see what "ages" referred
to. R86 item 2.4.6 adds the excerpt's own age lines. They are transcribed, not computed.

**Artifact:** `iclr2027_monitoring_submission/ARTIFACT/manifests/indexes_v2.json`, key
**`frbank:david:FULL:BELIEVED`** — the same serialized index the existing excerpt was cut from,
identified by its `entries in this store: 575` header and its three printed category rows
(`HOBBIES_RECREATION 29/18/11/0/2`, `PREFERENCES_HABITS 46/37/9/0/1`,
`PROJECTS_ENDEAVORS 61/54/7/0/18`). David is also the persona the Section 3 example box names.

| line in the index | value |
|---|---|
| header | `Ages below are in days before the store's pinned current time.` |
| `RECENCY` newest entry | **1** |
| `RECENCY` oldest entry | **518** |
| `RECENCY` median entry age | **258** |
| `AGE DISTRIBUTION` 0-30 | **47** |
| `AGE DISTRIBUTION` 31-90 | **54** |
| `AGE DISTRIBUTION` 91-180 | **75** |
| `AGE DISTRIBUTION` 181-365 | **229** |
| `AGE DISTRIBUTION` over 365 | **170** |

The index also carries per-category `NEWEST` and `OLDEST` columns and a `LIFECYCLE TOTALS`
block. The excerpt stays abridged and does not print them.

---

## `AUX-R86-GRAPHITI-SPIKE` — the three-persona spike reported in Appendix F.9

Transcribed from `r85_graphiti/SPIKE_REPORT.md`, which the R85-1 commit froze. Nothing is
recomputed here and no call was made. The 40-persona run was not scored before the submission
fence and moves to the October rebuttal card (D-R86-12), so only these spike figures print.

| quantity | value | source in `SPIKE_REPORT.md` |
|---|---|---|
| package and version | unmodified `graphiti-core 0.28.1` | run header |
| personas | 3 (elena, tom, yoli) | run header |
| episodes, primary arm | **137** | run header |
| superseded attribute names per persona | 3, 3, 1 (none empty) | exit gate (a) |
| manifest supersession events | **10** | exit gate denominator |
| recovered at the frozen 0.80 overlap bar | **2**, recall **0.20** | exit gate (b) |
| recovered at 0.75 | **5**, recall 0.500 | band table |
| recovered at 0.50 | **6**, recall 0.600 | band table |
| events sitting between 0.75 and 0.80 | 3 | band table note |
| precision on what it does mark | **0.00** to **0.04** | per-persona census |
| edges, three personas | 685 (609 active, 13 superseded, 63 expired) | census table |
| user split across entity nodes | 3 per persona | mechanism 1 |
| edges with no `valid_at` | 25/242, 28/221, 11/222 (about a tenth) | mechanism 2 |
| edge count change, modified against unmodified copy | **2.4\%** | patch-delta table |
| supersession recall at the frozen bar, both copies | identical at 1 of 6 | patch-delta table |

RETRACTED and category are inexpressible under stock defaults; the index emits the marker for
both. The disclosure dates (approximately February to March 2026, replaced April 2026) come
from `r85_graphiti/DISCLOSURE.md`.

---

## Tokens this file accounts for

`23,186` · `11,319` (already in `e1_metamemory/NUMBERS.md`) · `11,420` · `23,403` (retained so
the superseded figure still resolves wherever an older report quotes it) · `217` · `101` ·
`293` · `40` · `41`.
