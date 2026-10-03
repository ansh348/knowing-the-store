"""
ladder_luna.py -- E1.7: gpt-5.6-luna on the same 150-item subset, k=5 by construction.

Per E1_7_ADDENDUM.md (6860ad0), committed before any Luna observation.

Two arms (BLIND, INDEXED-TRUE), each returning FOK and NOK from one response,
k=5 draws per cell, per-item mean as the estimator. NO single-draw figure is
computed anywhere. Cache/resume keyed on (item, arm, model, draw_index); the
prompt hash is recorded per row so a prompt change would be detectable.

Prompts are byte-identical to E1.5/E1.6: prompts_e1.py is sha-verified at start
and the model string is the only difference.

Usage:  python e1_metamemory/tools/ladder_luna.py [model]
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

E1 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prompts_e1 as P  # noqa: E402

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gpt-5.6-luna"
K, WORKERS, MIN_DRAWS = 5, 5, 3
CODEX = shutil.which("codex") or shutil.which("codex.cmd") or "codex"
PART = E1 / f"ladder_partial_{MODEL}.jsonl"
OUT = E1 / f"ladder_{MODEL}.json"

# The exact texts frozen at E1.5/E1.6. Verified, not assumed: the addendum requires
# the model string to be the ONLY difference from those runs.
EXPECTED_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"


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
                except Exception:
                    pass
    return None


def clamp(v):
    try:
        return min(100.0, max(0.0, float(v))) / 100.0
    except (TypeError, ValueError):
        return None


def one(job):
    tag, arm, draw, prompt, phash = job
    sb = Path(tempfile.mkdtemp(prefix="e17_"))
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
        return {"item_id": tag, "arm": arm, "model": MODEL, "draw": draw,
                "prompt_hash": phash, "fok": f, "nok": clamp(obj.get("nok")),
                "status": "OK" if f is not None else "PARSE_FAIL"}
    except Exception as e:                                    # noqa: BLE001
        return {"item_id": tag, "arm": arm, "model": MODEL, "draw": draw,
                "prompt_hash": phash, "fok": None, "nok": None,
                "status": f"ERROR:{type(e).__name__}"}
    finally:
        shutil.rmtree(sb, ignore_errors=True)


def main():
    got = P.texts_sha256()
    if got != EXPECTED_TEXTS_SHA:
        raise SystemExit(f"FROZEN PROMPT MISMATCH: {got} != {EXPECTED_TEXTS_SHA}. "
                         "Prompts must be byte-identical to E1.5/E1.6. Stopping.")
    print(f"frozen prompt texts sha verified: {got[:16]}...")
    print(f"model pinned: {MODEL}")

    items = {i["item_id"]: i
             for i in json.load(io.open(E1 / "build" / "items_final.json", encoding="utf-8"))}
    idx = json.load(io.open(E1 / "indexes_v2.json", encoding="utf-8"))["indexes"]
    subset = json.load(io.open(E1 / "strong_model.json", encoding="utf-8"))["rows"]

    def ikey(it):
        b, p, v = it["backend"], it["persona"], it["variant"]
        return f"{b}:{p}:SLOT:{it['question_id']}" if v == "SLOT-ABLATED" else f"{b}:{p}:{v}"

    jobs = []
    for r in subset:
        tag, q = r["item_id"], r["question"]
        bp = P.SYSTEM + "\n\n" + P.USER_BLIND.format(question=q)
        k = f"{ikey(items[tag])}:TRUE"
        ip = (P.SYSTEM + "\n\n" + P.USER_INDEXED.format(index=idx[k], question=q)
              if k in idx else None)
        for d in range(1, K + 1):
            jobs.append((tag, "BLIND", d, bp,
                         hashlib.sha256(bp.encode()).hexdigest()[:16]))
            if ip:
                jobs.append((tag, "INDEXED-TRUE", d, ip,
                             hashlib.sha256(ip.encode()).hexdigest()[:16]))

    done = set()
    if PART.exists():
        for ln in io.open(PART, encoding="utf-8"):
            try:
                r = json.loads(ln)
                done.add((r["item_id"], r["arm"], r["model"], r["draw"]))
            except Exception:                                 # noqa: BLE001
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
                if n % 50 == 0:
                    print(f"  {n}/{len(todo)}", flush=True)
        finally:
            ph.close()

    rows = [json.loads(ln) for ln in io.open(PART, encoding="utf-8") if ln.strip()]
    seen, ded = set(), []
    for r in rows:
        k = (r["item_id"], r["arm"], r["model"], r["draw"])
        if k not in seen:
            seen.add(k); ded.append(r)

    agg = collections.defaultdict(lambda: {"fok": [], "nok": []})
    for r in ded:
        if r["status"] == "OK":
            agg[(r["item_id"], r["arm"])]["fok"].append(r["fok"])
            if r["nok"] is not None:
                agg[(r["item_id"], r["arm"])]["nok"].append(r["nok"])

    out, excluded = [], 0
    for (tag, arm), v in sorted(agg.items()):
        if len(v["fok"]) < MIN_DRAWS:
            excluded += 1
            continue
        it = items[tag]
        m = sum(v["fok"]) / len(v["fok"])
        sd = (sum((x - m) ** 2 for x in v["fok"]) / (len(v["fok"]) - 1)) ** 0.5
        nk = v["nok"]
        nm = (sum(nk) / len(nk)) if nk else None
        nsd = ((sum((x - nm) ** 2 for x in nk) / (len(nk) - 1)) ** 0.5
               if nk and len(nk) > 1 else None)
        out.append({"item_id": tag, "arm": arm, "model": MODEL,
                    "backend": it["backend"], "label": it.get("label", it["label_pre"]),
                    "n_draws": len(v["fok"]), "fok": m, "fok_sd": sd,
                    "fok_all_identical": len(set(v["fok"])) == 1,
                    "nok": nm, "nok_sd": nsd, "n_nok_draws": len(nk)})
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"model": MODEL, "k": K, "min_draws": MIN_DRAWS,
                   "prompt_texts_sha256": got, "n_cells": len(out),
                   "n_excluded_lt_min_draws": excluded, "n_calls": len(ded),
                   "rows": out}, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    ident = sum(1 for r in out if r["fok_all_identical"])
    print(f"cells {len(out)} {dict(collections.Counter(r['arm'] for r in out))}; "
          f"excluded {excluded}")
    print(f"identical across {K} draws: {ident}/{len(out)} ({ident/max(len(out),1):.0%})")
    print(f"mean per-item FOK SD: {sum(r['fok_sd'] for r in out)/max(len(out),1):.4f}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
