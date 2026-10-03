"""
natural_absent.py -- E1 Phase 0 item 5: the NATURAL-ABSENT probe pipeline test.

A natural-absent probe is a question a user could plausibly ask this persona's
assistant, whose answer the store genuinely does not contain -- absence that was
never manufactured by ablation. It is the hard-tier ABSENT source for backends
where slot-level ablation is impossible.

Pipeline, in order:
  calibrate  Fix the screening threshold from the 516 REAL questions, whose
             content IS in the bank, before any probe is drafted. Uses the cached
             query embeddings (artifacts/theory/query_emb_cache.npz), so this
             costs nothing and cannot be tuned to the probes.
  draft      gpt-4.1-mini drafts N candidate probes. It is shown the persona
             sketch and the persona's SLOT-KEY INVENTORY (attribute names only,
             value-scrubbed) so it can steer AWAY from covered ground. It never
             sees fact values, so it cannot draft a probe by copying content.
  screen     Machine pre-screen of every candidate against the FULL bank and the
             persona YAML: embedding sweep (text-embedding-3-small, the same model
             the bank was built with) plus a lexical sweep. Survivors carry their
             full search transcript.
  Then a human reads the survivors against the YAML and records a verdict; the
             per-probe table with the transcript is committed.

Usage:
  python e1_metamemory/tools/natural_absent.py calibrate
  python e1_metamemory/tools/natural_absent.py run <persona> [n_drafts]
"""

from __future__ import annotations

import collections
import io
import json
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(PROJECT_ROOT / "analysis" / "ontology_validation"))

from e0_common import BANKS, jdump, jload, load_yaml, toks, LME  # noqa: E402
from exp4_witnesses import toks as etoks  # noqa: E402

QCACHE = PROJECT_ROOT / "artifacts" / "theory" / "query_emb_cache.npz"
CALIB = E1 / "natural_absent_calibration.json"
EMBED_MODEL = "text-embedding-3-small"


def unit(v):
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-12)


def bank_emb(persona):
    z = np.load(BANKS / f"{persona}_embeddings.npz", allow_pickle=True)
    return list(z["ids"]), unit(z["embeddings"].astype(np.float32))


def cmd_calibrate():
    """Max-cosine distribution for questions whose content IS present."""
    z = np.load(QCACHE, allow_pickle=True)
    qids, qemb = list(z["ids"]), unit(z["embeddings"].astype(np.float32))
    qs = {q["id"]: q for q in jload(LME / "lifemembench_questions.json")}
    per_persona = collections.defaultdict(list)
    for qid, e in zip(qids, qemb):
        p = qs[qid]["persona"]
        per_persona[p].append((qid, e))
    maxcos = []
    for p, items in sorted(per_persona.items()):
        _, B = bank_emb(p)
        for qid, e in items:
            maxcos.append(float((B @ e).max()))
    a = np.asarray(maxcos)
    pct = {f"p{q}": float(np.percentile(a, q)) for q in (1, 2.5, 5, 10, 25, 50, 75, 95)}
    thr = round(pct["p2.5"], 3)
    print("=" * 76)
    print("CALIBRATION — max cosine to the persona bank, 516 questions WITH content present")
    print("=" * 76)
    print(f"  n={len(a)}  min {a.min():.3f}  mean {a.mean():.3f}  max {a.max():.3f}")
    for k, v in pct.items():
        print(f"    {k:6s} {v:.3f}")
    print(f"\n  SCREEN THRESHOLD = p2.5 of the present-content distribution = {thr}")
    print("  A candidate probe with max cosine >= this threshold sits inside the range where")
    print("  97.5% of genuinely-answerable questions live, so it is REJECTED as too close to")
    print("  existing content. Fixed here, before any probe is drafted.")
    jdump({"n": len(a), "percentiles": pct, "screen_threshold_cosine": thr,
           "rule": "reject candidate if max cosine to any bank entry >= p2.5 of the "
                   "present-content distribution",
           "embed_model": EMBED_MODEL, "no_api_calls": True}, CALIB)
    print(f"\nwrote {CALIB}")


def slot_inventory(persona):
    entries = jload(BANKS / f"{persona}.json")["entries"]
    inv = collections.defaultdict(set)
    for e in entries:
        sk = e.get("slot_key")
        if isinstance(sk, list) and len(sk) >= 2:
            inv[e["category"]].add(str(sk[1]).split(":", 1)[0])   # value-scrubbed
    return {k: sorted(v) for k, v in sorted(inv.items())}


def persona_sketch(persona):
    yp = next(LME.glob(f"*/persona_*_{persona}.yaml"))
    y = load_yaml(yp)
    p = y.get("persona") or {}
    return {k: p.get(k) for k in ("name", "age", "occupation_current", "location_current")}


def cmd_run(persona, n_drafts=6):
    import api                                   # noqa: PLC0415
    calib = jload(CALIB)
    thr = calib["screen_threshold_cosine"]
    inv = slot_inventory(persona)
    sketch = persona_sketch(persona)

    covered = "\n".join(f"{k}: {', '.join(v[:40])}" for k, v in inv.items())
    sysmsg = (
        "You draft NATURAL-ABSENT probe questions for a memory-benchmark study.\n\n"
        "A natural-absent probe is a question the user could plausibly ask their assistant, "
        "about their own life, whose answer the assistant's memory store does NOT contain. "
        "The absence must be natural -- a topic that simply never came up -- not a trick "
        "question and not about someone else.\n\n"
        "You are given a persona sketch and the ATTRIBUTE NAMES the store already covers "
        "(names only, no values). Draft questions in ordinary life domains that those "
        "attribute names do NOT cover. Avoid any topic named in the inventory. Avoid "
        "yes/no questions about whether a thing exists; ask for a specific detail, the way a "
        "user actually would.\n\n"
        "Return a single JSON object: {\"probes\": [{\"question\": \"...\", "
        "\"domain\": \"...\", \"why_absent\": \"...\"}]}"
    )
    user = (f"Persona: {json.dumps(sketch, ensure_ascii=False)}\n\n"
            f"Attribute names already covered by the store:\n{covered}\n\n"
            f"Draft exactly {n_drafts} probes.")
    r = api.call(f"natabsent:{persona}", "draft",
                 [{"role": "system", "content": sysmsg}, {"role": "user", "content": user}],
                 max_tokens=900)
    obj = api.parse_json(r["content"]) or {}
    probes = obj.get("probes", [])[:n_drafts]
    if not probes:
        raise SystemExit(f"draft returned nothing: {r['content'][:300]}")

    # ---- embed candidates with the SAME model the bank was built with
    from openai import OpenAI                    # noqa: PLC0415
    api._load_env()                              # noqa: SLF001
    import os                                    # noqa: PLC0415
    cli = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    texts = [p["question"] for p in probes]
    emb = cli.embeddings.create(model=EMBED_MODEL, input=texts)
    P = unit(np.asarray([d.embedding for d in emb.data], dtype=np.float32))

    ids, B = bank_emb(persona)
    entries = {e["id"]: e for e in jload(BANKS / f"{persona}.json")["entries"]}
    yp = next(LME.glob(f"*/persona_*_{persona}.yaml"))
    yraw = io.open(yp, encoding="utf-8").read()
    ytok = etoks(yraw)

    rows = []
    for p, v in zip(probes, P):
        cos = B @ v
        order = np.argsort(-cos)[:5]
        top = [{"entry_id": ids[i], "cosine": round(float(cos[i]), 4),
                "category": entries[ids[i]]["category"],
                "text": entries[ids[i]]["text"]} for i in order]
        qt = etoks(p["question"])
        lex_bank = [e["id"] for e in entries.values()
                    if len(qt & etoks(e["text"])) >= 2
                    and len(qt & etoks(e["text"])) / max(len(qt), 1) >= 0.5]
        lex_yaml = sorted(qt & ytok)
        maxcos = round(float(cos.max()), 4)
        verdict = ("REJECT: cosine" if maxcos >= thr
                   else ("REJECT: lexical" if lex_bank else "SURVIVES SCREEN"))
        rows.append({"question": p["question"], "domain": p.get("domain"),
                     "why_absent": p.get("why_absent"), "max_cosine": maxcos,
                     "threshold": thr, "top5": top,
                     "lexical_bank_hits": lex_bank,
                     "lexical_yaml_token_overlap": lex_yaml,
                     "screen_verdict": verdict, "human_verdict": None, "note": ""})

    api.flush()
    out = {"persona": persona, "n_drafted": len(rows), "threshold": thr,
           "n_survived_screen": sum(1 for r in rows if r["screen_verdict"] == "SURVIVES SCREEN"),
           "embed_model": EMBED_MODEL, "probes": rows, "meter": api.meter()}
    jdump(out, E1 / f"natural_absent_{persona}.json")

    print("=" * 96)
    print(f"NATURAL-ABSENT PIPELINE TEST — {persona}   screen threshold cosine {thr}")
    print("=" * 96)
    for n, r in enumerate(rows, 1):
        print(f"\n[{n}] {r['screen_verdict']}   max_cos={r['max_cosine']:.3f}   "
              f"domain={r['domain']}")
        print(f"    Q: {r['question']}")
        print(f"    nearest bank entries:")
        for t in r["top5"][:3]:
            print(f"      {t['cosine']:.3f} {t['entry_id']} [{t['category']}] {t['text'][:74]}")
        if r["lexical_bank_hits"]:
            print(f"    lexical bank hits: {r['lexical_bank_hits'][:5]}")
    print(f"\n  drafted {len(rows)}, survived screen {out['n_survived_screen']}")
    print(f"  spend ${api.meter()['usd']:.4f}")
    print(f"\nwrote {E1/f'natural_absent_{persona}.json'}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "calibrate"
    if cmd == "calibrate":
        cmd_calibrate()
    else:
        cmd_run(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 6)
