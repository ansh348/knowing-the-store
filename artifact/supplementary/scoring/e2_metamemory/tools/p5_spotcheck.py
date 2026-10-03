"""
p5_spotcheck.py -- P5 frontier spot-check. RAW DRAWS ONLY. Bands NOT evaluated.

Per P5-as-re-registered (E2_AMENDMENT_2 section 5, D34 resolved): the FR-Bank
84-item matched cell -- the ladder's own cell. The 66 external items of E1.7's
150-item subset are out of scope by construction, because E2 generates no answers
for them.

  lane    codex exec, model id pinned and VERIFIED to respond before any scored call
  arms    gate-verbal (policy iv) and gate-indexed-BELIEVED (policies v/vi)
  k       5 by construction, per E1.7's finding that the frontier lane reproduces
          1/300 cells across draws
  cache   (item, arm, model, draw, prompt_hash), resumable
  prompts prompts_e1 sha-verified at startup; the model string is the only change

WHY BELIEVED, NOT TRUE. E1.6/E1.7's committed frontier draws used the TRUE index.
E2's policies (v)/(vi) read the BELIEVED index (E2_AMENDMENT_2 section 6), so a
like-for-like spot-check needs BELIEVED draws, which do not exist. Reusing the
committed TRUE draws would compare a frontier gate on one index against a mini
gate on another.

SEVERABLE: if the lane misbehaves, the failure is logged and the run exits
non-fatally. The spot-check must not block SP3.

Usage:  python e2_metamemory/tools/p5_spotcheck.py [model]
"""

from __future__ import annotations

import collections
import concurrent.futures as cf
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"
sys.path.insert(0, str(E1 / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import prompts_e1 as P1                                           # noqa: E402
import prompts_e2 as P2                                           # noqa: E402
from e2_common import E2, Indexes, jdump, jload, load_items       # noqa: E402

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gpt-5.6-sol"
K, WORKERS = 5, 5
CODEX = shutil.which("codex") or shutil.which("codex.cmd") or "codex"
PART = E2 / f"p5_partial_{MODEL}.jsonl"
OUT = E2 / f"p5_spotcheck_{MODEL}.json"
E1_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"


def last_json(s):
    d, st, esc, start = 0, False, False, -1
    for i, c in enumerate(s):
        if esc:
            esc = False; continue
        if c == "\\":
            esc = True; continue
        if c == chr(34):
            st = not st; continue
        if st:
            continue
        if c == "{":
            if d == 0:
                start = i
            d += 1
        elif c == "}":
            d -= 1
            if d == 0 and start >= 0:
                try:
                    return json.loads(s[start:i + 1])
                except Exception:                                 # noqa: BLE001
                    pass
    return None


def clamp(v):
    try:
        return min(100.0, max(0.0, float(v))) / 100.0
    except (TypeError, ValueError):
        return None


def one(job):
    tag, arm, draw, prompt, phash = job
    sb = Path(tempfile.mkdtemp(prefix="p5_"))
    try:
        env = {k: v for k, v in os.environ.items()
               if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")}
        o = sb / "o.txt"
        r = subprocess.run(
            [CODEX, "exec", "-m", MODEL, "--cd", str(sb), "--skip-git-repo-check",
             "--ephemeral", "--ignore-user-config", "--ignore-rules", "-s", "read-only",
             "--color", "never", "-c", "model_reasoning_effort=low", "-o", str(o)],
            input=prompt, text=True, capture_output=True, timeout=300, env=env)
        raw = o.read_text(encoding="utf-8", errors="replace") if o.exists() else ""
        obj = last_json(raw) or last_json(r.stdout) or {}
        f = clamp(obj.get("fok"))
        p = clamp(obj.get("p_store_has_relevant"))
        val = p if arm == "gate-verbal" else f
        return {"item_id": tag, "arm": arm, "model": MODEL, "draw": draw,
                "prompt_hash": phash, "fok": f, "nok": clamp(obj.get("nok")),
                "p_store_has_relevant": p,
                "status": "OK" if val is not None else "PARSE_FAIL"}
    except Exception as e:                                        # noqa: BLE001
        return {"item_id": tag, "arm": arm, "model": MODEL, "draw": draw,
                "prompt_hash": phash, "fok": None, "nok": None,
                "p_store_has_relevant": None, "status": f"ERROR:{type(e).__name__}"}
    finally:
        shutil.rmtree(sb, ignore_errors=True)


def main():
    got = P1.texts_sha256()
    if got != E1_TEXTS_SHA:
        print(f"SEVERED: frozen prompt mismatch {got}")
        return 0
    print(f"E1 prompt texts sha verified {got[:16]}...   model pinned: {MODEL}")

    # ---- verify the model id responds before any scored call (E1.7 precedent)
    probe = one(("probe", "gate-verbal", 0,
                 'Reply with only this JSON and nothing else: '
                 '{"provisional_answer":"none","confidence_without_store":0,'
                 '"p_store_has_relevant":42}', "probe"))
    if probe["status"] != "OK":
        print(f"SEVERED: model id {MODEL} did not respond cleanly ({probe['status']}). "
              f"Spot-check skipped; SP3 continues.")
        jdump({"severed": True, "model": MODEL, "reason": probe["status"]}, OUT)
        return 0
    print(f"  model verified live (probe p={probe['p_store_has_relevant']})")

    items = {i["item_id"]: i for i in load_items()}
    subset = [r["item_id"] for r in jload(E1 / "strong_model.json")["rows"]]
    cell = [items[t] for t in subset if t in items and items[t]["backend"] == "frbank"]
    print(f"P5 matched cell: {len(cell)} FR-Bank items "
          f"(external items out of scope by construction)")

    IX = Indexes()
    jobs = []
    for it in cell:
        vp = P2.VERBAL_SYSTEM + "\n\n" + P2.VERBAL_USER.format(question=it["question"])
        ip = (P1.SYSTEM + "\n\n"
              + P1.USER_INDEXED.format(index=IX.text(it, "BELIEVED"),
                                       question=it["question"]))
        for d in range(1, K + 1):
            jobs.append((it["item_id"], "gate-verbal", d, vp,
                         hashlib.sha256(vp.encode()).hexdigest()[:16]))
            jobs.append((it["item_id"], "gate-indexed-believed", d, ip,
                         hashlib.sha256(ip.encode()).hexdigest()[:16]))

    done = set()
    if PART.exists():
        for ln in io.open(PART, encoding="utf-8"):
            try:
                r = json.loads(ln)
                done.add((r["item_id"], r["arm"], r["model"], r["draw"]))
            except Exception:                                     # noqa: BLE001
                pass
    todo = [j for j in jobs if (j[0], j[1], MODEL, j[2]) not in done]
    print(f"{len(jobs)} calls total, {len(done)} done, {len(todo)} to go", flush=True)

    NL = chr(10)
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        ph = io.open(PART, "a", encoding="utf-8", newline=NL)
        try:
            for n, r in enumerate(ex.map(one, todo), 1):
                ph.write(json.dumps(r, ensure_ascii=False) + NL)
                ph.flush()
                if n % 100 == 0:
                    print(f"  {n}/{len(todo)}", flush=True)
        finally:
            ph.close()

    rows = [json.loads(ln) for ln in io.open(PART, encoding="utf-8") if ln.strip()]
    seen, ded = set(), []
    for r in rows:
        k = (r["item_id"], r["arm"], r["model"], r["draw"])
        if k not in seen:
            seen.add(k); ded.append(r)
    c = collections.Counter((r["arm"], r["status"]) for r in ded)
    ident = collections.defaultdict(set)
    for r in ded:
        v = r["p_store_has_relevant"] if r["arm"] == "gate-verbal" else r["fok"]
        ident[(r["item_id"], r["arm"])].add(v)
    n_ident = sum(1 for v in ident.values() if len(v) == 1)

    jdump({"module": "P5", "model": MODEL, "k": K, "index_provenance": "BELIEVED",
           "cell": "FR-Bank 84-item matched cell (D34 resolution)",
           "n_items": len(cell), "n_calls": len(ded),
           "prompt_texts_sha256": got,
           "bands_evaluated": False,
           "cells_identical_across_k": n_ident, "n_cells": len(ident),
           "rows": ded}, OUT)
    print("\nRAW DRAW CENSUS (no band evaluated):")
    for arm in ("gate-verbal", "gate-indexed-believed"):
        print(f"  {arm:24s} OK {c[(arm,'OK')]:4d}  "
              f"PARSE_FAIL {c[(arm,'PARSE_FAIL')]:3d}  "
              f"other {sum(v for (a,s),v in c.items() if a==arm and s not in ('OK','PARSE_FAIL'))}")
    print(f"  cells identical across {K} draws: {n_ident}/{len(ident)} "
          f"(E1.7 reference: sol 3/300, luna 1/300)")
    print(f"wrote {OUT.name} -- raw draws only, P5 bands NOT evaluated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
