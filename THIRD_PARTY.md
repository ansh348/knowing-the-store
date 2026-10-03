# Third-party material

The release archive (`supplementary.zip`, unpacked under `artifact/`) vendors **no third-party code**. It has no license
headers, SPDX tags or copyright notices other than its own `LICENSE`. The memory backends were run from their own public
releases and are not bundled; scripts that need one import it as a pinned dependency (`requirements-runners.txt`). The
archive contains no third-party benchmark corpus: no LongMemEval, LoCoMo or MemoryAgentBench data.

It does contain data derived from the sources below. Each permits redistribution.

| material in the archive | source | license |
|---|---|---|
| Persona text, store-entry exports (e.g. `data/e1_metamemory/backend_entries/frbank.json`) and store views derived from the FR-Bank release | FR-Bank release: Mullick & Tüzün (2026), *Fortunate Recall: Ontology-Driven Memory Lifecycle Management for Persistent Coherence in LLMs*, arXiv:2609.10413; data on Zenodo, doi:[10.5281/zenodo.20067778](https://doi.org/10.5281/zenodo.20067778) | CC BY 4.0 |
| Mem0 store exports and views (data the software produced; software not bundled) | [mem0ai/mem0](https://github.com/mem0ai/mem0) | Apache-2.0 (software) |
| A-MEM store exports and views (data the software produced; software not bundled) | [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | MIT (software) |
| Graphiti graph exports and views (data the software produced; software not bundled) | [getzep/graphiti](https://github.com/getzep/graphiti) | Apache-2.0 (software) |
| Sentence-embedding vectors (`.npz` caches, `lookup_vectors.json`) | [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | Apache-2.0 (model) |
| Recorded model responses | OpenAI, Anthropic and Moonshot AI (Kimi K3) APIs, used under each provider's API terms | included as recorded research data, under CC BY 4.0 like the rest of the data (the archive's own `LICENSE` says the same) |

Nothing in the archive was found to restrict redistribution.
