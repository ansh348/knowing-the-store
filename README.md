# Knowing the Store

**Knowing the Store: What a Memory Backend Must Write Down Before an Agent Can Read It**

Ansuman Mullick and Eray Tüzün, Bilkent University

arXiv: pending

## What the paper shows

An agent with long-term memory can answer from a record it should no longer use, such as a plan the user later cancelled. We ask what a memory store must expose for an agent to know this before retrieving anything, and we score that judgment on its own, as metamemory monitoring. Readers see only a value-free summary: record counts by lifecycle state and a list of attribute names. Each of 148 questions is asked against three versions of one store that differ in one attribute, so wording cannot give the answer away. What a model adds depends on the length of that list. On the short lists the benchmark's ground truth produces (2.6 names on average), none of five language models reliably beats a cosine-similarity lookup over the names, and the three stronger ones are equivalent to it within 0.05. Under a control that fixes counts and list length, none is reliably above it and none is shown equivalent. On lists longer than the stores we tested write, padded to 60 names, the lookup loses 0.18; GPT-5.6 Luna and Sol lose 0.06 to 0.07 and lead it by 0.13 to 0.14, while the other three fall with it. The lead holds for Sol against a sibling padded to the same length and counts. Reworded to share no word with the names, the lookup loses 0.02 and one stronger reader edges 0.04 ahead. On the short lists the three stronger readers lead only where the summary counts a state without naming it, and one count feature closes that lead within a question, though not when items are pooled. The backends we tested omit or misstate this information: under FR-Bank's own metadata, GPT-4.1 mini, Haiku 4.5 and the lookup fall from 0.73, 0.82 and 0.75 to 0.60, 0.71 and 0.59. In these tests, what the store wrote down limited every reader we gave it to. All stores are synthetic; control, whether a better judgment yields a better answer, is left to a later study.

(The paper's abstract, verbatim.)

## Download

The artifact is one archive, attached to the release
[`kts-arxiv-v1`](https://github.com/ansh348/knowing-the-store/releases/tag/kts-arxiv-v1):

| file | sha256 | size | files |
|---|---|---|---|
| [`supplementary.zip`](https://github.com/ansh348/knowing-the-store/releases/download/kts-arxiv-v1/supplementary.zip) | `685e398ceed7bda28a2fb6aad4fcde7460d633397e15b114198855dad189500e` | 36,099,648 bytes | 1,438 |

Check your copy before using it: `sha256sum supplementary.zip` (Linux), `shasum -a 256 supplementary.zip` (macOS) or
`Get-FileHash supplementary.zip -Algorithm SHA256` (PowerShell).

**The archive is byte-identical to the supplementary material of the ICLR 2027 submission, which is under review.**
That review is double-blind, so the archive carries no author names inside. Names, home paths and handles are replaced by
placeholders such as `[AUTHOR-1]` and `[HOME]`, and its own README is titled "anonymous supplementary material". The one
exception is the third-person citation of the FR-Bank release (Mullick & Tüzün, 2026), which the paper cites by name.

### Browsable copy

[`artifact/`](artifact/) holds the same 1,438 files, unpacked (`artifact/supplementary/…`), so the code can be read on
GitHub. They are committed byte for byte, with line-ending conversion switched off for that directory (`.gitattributes`).
**The zip is canonical.** `artifact/` is the same bytes unpacked.

## Reproduce

The archive documents itself. Read
[`supplementary/README.md`](artifact/supplementary/README.md) and
[`supplementary/REPRODUCE.md`](artifact/supplementary/REPRODUCE.md) inside it. The offline path needs no API key and no
network once the requirements are installed. From the directory you unzip the archive into, with Python 3.12 or newer:

```
unzip supplementary.zip                 # creates supplementary/
python -m venv kts_env                  # beside supplementary/, not inside it
# activate kts_env the usual way for your platform, then:
python -m pip install -r supplementary/requirements.txt
python supplementary/reproduce_all.py
```

`reproduce_all.py` works in a clean virtual environment, writes only to `kts_work/` beside the archive, and exits 0 with
PASS. Among its checks, the paper's number gate `r141_number_gate` reports **232 checks, 0 mismatches** (233 inside a git
checkout, where a recorded freeze date is also compared with git). What it recomputes, regenerates or only accounts for is
stated layer by layer in the archive's README.

## License

- Code: MIT ([`LICENSE`](LICENSE)).
- Data, model outputs, registrations and ledgers: CC BY 4.0 ([`DATA_LICENSE`](DATA_LICENSE)).
- The archive states the same terms in its own `LICENSE`.
- Third-party material and its terms: [`THIRD_PARTY.md`](THIRD_PARTY.md).

## Citation

See [`CITATION.cff`](CITATION.cff). The arXiv identifier will be added after announcement.
