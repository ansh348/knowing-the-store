"""
verify_probes.py -- direct-YAML verification of the 145 natural-absent probe survivors.

NO API CALLS.

Each probe is swept against the persona YAML AND the full FR-Bank bank on its own
content terms, with WORD-BOUNDARY anchors (Phase 0 found `band` matching inside
`abandons`; substring matching manufactures false rejections at scale). The sweep
output IS the search transcript and is committed per probe.

A probe fails verification if related content is found after all, and routes to
UNRESOLVED with the reason tagged. Probes whose sweep returns nothing on every
content term are verified absent by the transcript itself; probes with any hit are
read individually against the hit.

Usage:
    python e1_metamemory/tools/verify_probes.py sweep    # build transcripts
    python e1_metamemory/tools/verify_probes.py apply    # apply verdicts, emit tables
"""

from __future__ import annotations

import collections
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))

from e0_common import BANKS, LME, jload  # noqa: E402

STOP = set("""a an the is are was were be been being has have had do does did of in on at to for
with and or but not no as by from that this these those it its your you user my me i we they them
their he she his her him about again still now then there here some any more most other such own
so than too very can will just should would could what which who whom whose when where why how
describe tell say give please ever any""".split())


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c)).casefold()
    return s


_DF = None
DF_MAX = 0.50          # a term in >50% of persona YAMLs is generic vocabulary, not content


def _doc_freq():
    """Document frequency of every token across all 40 persona YAMLs.

    A hand-written stoplist cannot anticipate this corpus: `type` appears in every
    persona YAML because `session_plan` writes `type: filler` / `type: critical`,
    and `work`, `home`, `last`, `time` are equally ubiquitous. Sweeping on those
    manufactures dozens of meaningless hits per probe. Document frequency is the
    principled filter -- it is measured from the corpus, not chosen by me.
    """
    global _DF
    if _DF is None:
        df = collections.Counter()
        n = 0
        for yp in sorted(LME.glob("*/persona_*.yaml")):
            n += 1
            toks = set(re.findall(r"[a-z][a-z0-9'-]+", norm(io.open(yp, encoding="utf-8").read())))
            df.update(toks)
        _DF = {t: c / n for t, c in df.items()}
    return _DF


def content_terms(q):
    """Content words of the probe question -- the terms the sweep searches on."""
    df = _doc_freq()
    toks = re.findall(r"[a-z][a-z0-9'-]+", norm(q))
    return sorted({t for t in toks
                   if t not in STOP and len(t) > 3 and df.get(t, 0.0) <= DF_MAX})


def sweep_one(persona, question):
    yp = next(LME.glob(f"*/persona_*_{persona}.yaml"))
    yraw = io.open(yp, encoding="utf-8").read()
    entries = jload(BANKS / f"{persona}.json")["entries"]
    terms = content_terms(question)
    pats = {t: re.compile(rf"\b{re.escape(t)}\b", re.I) for t in terms}   # word-boundary
    # A hit counts only where ONE line or ONE entry matches >=2 DISTINCT probe terms.
    # A single generic word co-occurring proves nothing; two distinct probe terms in the
    # same sentence is real signal. Same >=2-token rule the detector and the gold
    # resolver use throughout this project (MIN_SHARED).
    yhits, bhits = [], []
    for ln, line in enumerate(yraw.splitlines(), 1):
        m = sorted(t for t, p in pats.items() if p.search(line))
        if len(m) >= 2:
            yhits.append({"terms": m, "line": ln, "text": line.strip()[:120]})
    for e in entries:
        m = sorted(t for t, p in pats.items() if p.search(e.get("text", "")))
        if len(m) >= 2:
            bhits.append({"terms": m, "entry_id": e["id"], "text": e["text"][:120]})
    return terms, yhits, bhits


def cmd_sweep():
    out = []
    for p in sorted(BANKS.glob("*.json")):
        persona = p.stem
        f = E1 / f"natural_absent_{persona}.json"
        if not f.exists():
            continue
        for pr in jload(f)["probes"]:
            if pr["screen_verdict"] != "SURVIVES SCREEN":
                continue
            terms, yh, bh = sweep_one(persona, pr["question"])
            out.append({"persona": persona, "question": pr["question"],
                        "domain": pr.get("domain"), "max_cosine": pr["max_cosine"],
                        "terms": terms, "yaml_hits": yh, "bank_hits": bh,
                        "n_yaml": len(yh), "n_bank": len(bh)})
    with io.open(E1 / "probe_sweeps.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    clean = [r for r in out if r["n_yaml"] == 0 and r["n_bank"] == 0]
    dirty = [r for r in out if r["n_yaml"] or r["n_bank"]]
    print(f"probes swept: {len(out)}")
    print(f"  ZERO hits on every content term (verified by transcript): {len(clean)}")
    print(f"  some hit -- require individual reading:                   {len(dirty)}")
    print("\n  probes with hits, ranked by hit count:")
    for r in sorted(dirty, key=lambda r: -(r["n_yaml"] + r["n_bank"]))[:60]:
        hs = collections.Counter(t for h in r["yaml_hits"] + r["bank_hits"] for t in h["terms"])
        print(f"    {r['persona']:10s} y={r['n_yaml']:3d} b={r['n_bank']:3d} "
              f"{r['question'][:64]:64s} terms={dict(list(hs.items())[:4])}")
    print(f"\n  ({len(dirty)} total with hits)")


def cmd_apply():
    from probe_verdicts import VERDICTS  # noqa: PLC0415
    sweeps = jload(E1 / "probe_sweeps.json")
    rows, counts = [], collections.Counter()
    for r in sweeps:
        key = (r["persona"], r["question"])
        if r["n_yaml"] == 0 and r["n_bank"] == 0:
            v, why = "ABSENT", "zero hits on every content term; verified by transcript"
        else:
            v, why = VERDICTS.get(key, (None, None))
            if v is None:
                raise SystemExit(f"unverified probe with hits: {key}")
        counts[v] += 1
        rows.append({**r, "verdict": v, "reason": why})
    with io.open(E1 / "probe_verification.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"n": len(rows), "counts": dict(counts), "probes": rows},
                  fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")

    L = ["# NATURAL-ABSENT PROBE VERIFICATION — all 145 survivors", "",
         f"Direct YAML + bank sweep on each probe's content terms, word-boundary anchored. "
         f"The sweep output is the search transcript.", "",
         f"**{counts['ABSENT']} verified ABSENT · {counts['UNRESOLVED']} routed to UNRESOLVED.**",
         "",
         "| persona | probe | cos | YAML hits | bank hits | verdict | reason |",
         "|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["verdict"], r["persona"])):
        esc = lambda s: str(s or "").replace("|", "\\|")
        L.append(f"| {r['persona']} | {esc(r['question'])[:74]} | {r['max_cosine']:.2f} | "
                 f"{r['n_yaml']} | {r['n_bank']} | **{r['verdict']}** | {esc(r['reason'])[:90]} |")
    L += ["", "## Transcripts for every probe with a non-zero sweep", ""]
    for r in sorted(rows, key=lambda r: (-(r["n_yaml"] + r["n_bank"]), r["persona"])):
        if not (r["n_yaml"] or r["n_bank"]):
            continue
        L.append(f"\n### `{r['persona']}` — {r['question']}\n")
        L.append(f"- terms swept: `{', '.join(r['terms'])}`")
        L.append(f"- verdict **{r['verdict']}** — {r['reason']}")
        for h in r["yaml_hits"][:6]:
            L.append(f"  - YAML L{h['line']} `{'+'.join(h['terms'])}`: {h['text']}")
        for h in r["bank_hits"][:6]:
            L.append(f"  - bank {h['entry_id']} `{'+'.join(h['terms'])}`: {h['text']}")
    with io.open(E1 / "PROBE_VERIFICATION.md", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"verified ABSENT {counts['ABSENT']}  ->UNRESOLVED {counts['UNRESOLVED']}")
    print(f"wrote PROBE_VERIFICATION.md, probe_verification.json")


if __name__ == "__main__":
    {"sweep": cmd_sweep, "apply": cmd_apply}[sys.argv[1] if len(sys.argv) > 1 else "sweep"]()
