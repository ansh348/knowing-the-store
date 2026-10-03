# R85-GRAPHITI — Graphiti disclosure inventory

The first section is written in paper register and is the paragraph that reaches the
appendix. It obeys STYLE_SPEC S8 to S10: no em dashes, no contrastive constructions, no
internal program vocabulary. The sections below it are working inventory.

---

## Appendix paragraph (frozen text)

The second lifecycle-bearing backend evaluated here has a history with this project, and
that history is disclosed in full. An earlier version of our own store was built on Zep's
Graphiti, version 0.28.1, released under Apache-2.0. A copy of that release is vendored in
our repository, with four local modifications aimed at preserving numeric detail through
edge extraction and deduplication, and one further modification that filters extracted
edges through an external classifier. Graphiti served as the memory substrate from
approximately 21 February 2026 until 15 March 2026, and was replaced on 6 April 2026 by a
from-scratch store that keeps the lifecycle policies and shares no code with it. No current
code path in the store evaluated in the main study imports Graphiti. The measurements
reported for Graphiti in this paper were produced on an unmodified release installed from
the public package index at the pinned version, in a separate environment, against a
separate database instance. The locally modified copy was ingested as well, and its results
are reported only as a difference against the unmodified release. No number attributed to
Graphiti in this paper comes from the modified copy.

---

## Provenance of record

| Fact | Value | Evidence |
|---|---|---|
| Upstream package | `graphiti-core`, Zep | `graphiti/pyproject.toml:6` |
| Vendored version | `0.28.1` | same |
| Licence | Apache-2.0 | `graphiti/LICENSE` |
| Vendoring form | copied source tree, 326 tracked files; no submodule | `git ls-files graphiti/` |
| Fork cut | ~2026-02-21 | mtimes of `graphiti/` tree |
| Patched | ~2026-03-03 00:19 | mtimes of patched files |
| First commit containing it | `9c6b4fd` 2026-03-03 | `git log -- graphiti/` |
| Last substantive Graphiti-era commit | `00665a9` 2026-03-15 | `git log` |
| Replacement commit | `f47c824` 2026-04-06 | introduces `lifecycle_bank.py` |
| Stock available upstream | yes, `0.28.1` on PyPI (latest 0.29.3) | PyPI JSON API |

**The repository history is squashed before 2026-03-03.** Commit `9c6b4fd` ("Initial
commit") already contains `graphiti/`, `graphiti_patches/`, `graphiti_bridge.py` and the
Graphiti-era ingest and evaluation scripts fully formed. The adoption of Graphiti is
therefore not recorded in version control, and the 21 February date rests on file
modification times. The appendix paragraph says "approximately" for that reason and claims
no range the history cannot support.

## Modification inventory

| File | Target | Change |
|---|---|---|
| `graphiti_patches/edge_operations.py` | `graphiti_core/utils/maintenance/edge_operations.py` | adds `_count_numeric_tokens()` and transplants the more numerically specific fact onto the retained edge during duplicate resolution, replacing an unconditional keep-the-old-edge branch |
| `graphiti_patches/bulk_utils.py` | `graphiti_core/utils/bulk_utils.py` | post-dedup pass making the canonical edge in each duplicate group inherit the most numeric-rich fact, replacing the smallest-uuid tiebreak |
| `graphiti_patches/dedupe_edges.py` | `graphiti_core/prompts/dedupe_edges.py` | prompt guidelines plus six worked "not duplicates due to numeric specificity" examples |
| `graphiti_patches/extract_edges.py` | `graphiti_core/prompts/extract_edges.py` | numeric-preservation instructions in the extraction rules |
| **undocumented** | `graphiti_core/utils/maintenance/edge_operations.py:53-268, :393-427` | world-knowledge filter: every extracted edge not touching user or assistant is classified by `grok-4-1-fast-reasoning` at xAI and dropped unless judged personal |

Two facts about this inventory that the appendix paragraph reflects and that must not be
softened:

1. **The four files in `graphiti_patches/` are byte-identical to their counterparts inside
   `graphiti/`.** The vendored tree is already the modified tree. Any import of
   `graphiti_core` resolving to `graphiti/` gets the modified code. The repository's own
   `.venv` installs `graphiti-core 0.28.1` as an editable install pointing at `graphiti/`,
   so in that environment `import graphiti_core` is the modified copy. This is why the
   unmodified arm requires its own environment outside the repository root.
2. **The fifth modification appears in no README.** It is wired unconditionally into
   `extract_edges`, it changes which edges enter the graph at all, and it introduces a
   second model vendor into ingestion. It fails open on exception, and the xAI credential
   has returned 403 since 2026-07-31, so the modified copy as run today keeps edges that
   the modified copy as run in February and March discarded. The difference reported
   against the unmodified release therefore measures four modifications with the fifth
   inert, and the report says so.

## Current code

No live store code imports Graphiti. `lifecycle_bank.py:1-12` states that it replaces
Graphiti as the infrastructure layer, and its imports are `asyncio`, `json`, `math`, `re`,
`dataclasses`, `datetime`, `pathlib`, `numpy`, `rank_bm25` and `eval_common`.

The identifier `graphiti_score` survives as a field name in `eval_common.py:31`,
`retrieval_router.py` and `benchmark_lifecycle_latency.py`, and the label "FR-Graphiti"
survives as a comparison-arm name in several analysis scripts. These are vestigial names
with no Graphiti code behind them. One footnote records this so that a reader grepping the
released code is not misled.

Seventeen Graphiti-era scripts remain at the repository root (`ingest_full.py`,
`ingest_poc.py`, `evaluate_v2.py` through `evaluate_v4.py`, `graphiti_bridge.py` and
others). They are archival and sit on no current path.

## Correction to the released requirements file

`audit/submission_source/requirements.txt:22` pins `graphiti-core>=0.3.0`. That is a floor
rather than a pin, and it understates the vendored version by roughly twenty-five minor
releases. A reproducer following that file today resolves to whatever is current on the
package index. The disclosure states the real figure, 0.28.1, and the correction is
recorded as a deviation.

## Measured modification delta

Computed against unmodified `graphiti-core 0.28.1` from the public package index, ignoring
line-ending differences (the repository pins CRLF, the published wheel ships LF, so a raw
diff reports every line as changed and is meaningless).

| File | Added | Removed |
|---|---|---|
| `utils/maintenance/edge_operations.py` | 290 | 15 |
| `utils/bulk_utils.py` | 13 | 0 |
| `prompts/dedupe_edges.py` | 11 | 0 |
| `prompts/extract_edges.py` | 5 | 1 |
| `edges.py` | 0 | 0 |
| `nodes.py` | 0 | 0 |
| `graphiti.py` | 0 | 0 |

Roughly 200 of the 290 lines added to `edge_operations.py` are the undocumented
world-knowledge filter. The four documented numeric-preservation changes are 29 added lines
and 15 removed across four files.

`edges.py`, `nodes.py` and `graphiti.py` are byte identical to the published release. Every
schema claim this program makes about Graphiti therefore describes the unmodified library,
and the temporal model reported in the paper is Zep's, not ours.
