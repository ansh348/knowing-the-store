# -*- coding: utf-8 -*-
"""run_a2.py -- R85 Amendment 2 Step 2: the GPT-4.1 mini run over the distinct complete inputs of a2/views_a2.json. BILLED (OpenAI
metered key). One call per distinct (system, user) input, the DS decoding (temperature 0, seed 42, max_tokens 200, JSON mode, one
retry on a parse failure; run_ds.py's rule), the answer shared by every (store, condition, item) row whose input is byte-identical.
Cache r85_graphiti/a2/cache_mini/; rows a2/rows_a2_mini.jsonl (one row per distinct input, the member rows listed). The Haiku lane
(section 8 (b)) is not authorized at the freeze and does not run.

Subcommands:  probe | project | run
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import datetime as dt
import io
import json
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
R85 = HERE.parent
ROOT = R85.parent
sys.path.insert(0, str(ROOT / "reviews" / "r114" / "tools"))
from r114_common import assert_spec, J, jdump  # noqa: E402
import build_views_a2 as B                                                   # noqa: E402
import run_ds as RD                                                          # noqa: E402
import prompts_e1 as P                                                       # noqa: E402

api = B.A4.api
LANE, PRICE = B.A4.LANE_MINI, B.A4.PRICE_MINI
LINE = 0.47                     # section 8's worst line for the mini cells
CACHE = HERE / "cache_mini"
ROWS_P = HERE / "rows_a2_mini.jsonl"
PROBES_P = HERE / "probes_a2.json"
LEDGER = R85 / "NUMBERS_R85.md"
ARM = "ANSWER-A2"


def assert_lineage():
    B.assert_lineage(); RD.assert_lineage()
    assert "No rendering fault found; Step 2 proceeds" in LEDGER.read_text(encoding="utf-8"), "the by-eye check is not recorded -- STOP"


def redirect():
    CACHE.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                             # noqa: SLF001
    e0.CACHE_PATH = CACHE / "responses.json"; e0.LEDGER_PATH = CACHE / "cost_ledger.json"
    e0._cache = None; e0._load_cache()                                       # noqa: SLF001
    e0.HARD_CAP_USD = LINE
    return e0


def jobs():
    V = J(B.OUT_VIEWS); assert V["meta"]["registration_sha256"] == B.REG_SHA
    js = V["jobs"]; assert len(js) == len({j["key"] for j in js})
    return js


def msgs(j):
    return [{"role": "system", "content": j["system"]}, {"role": "user", "content": j["user"]}]


def cmd_probe():
    assert_lineage(); e0 = redirect(); js = jobs()
    first = max(js, key=lambda j: len(j["user"]))
    r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS, messages=msgs(first), response_format={"type": "json_object"})   # noqa: SLF001
    o = api.parse_json(r.choices[0].message.content) or {}
    rec = {"key": first["key"], "n_lines": first["n_lines"], "served": r.model, "identifier_ok": LANE in r.model, "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens,
           "usd": r.usage.prompt_tokens / 1e6 * PRICE[0] + r.usage.completion_tokens / 1e6 * PRICE[1], "user_chars": len(first["user"]) + len(first["system"]),
           "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL", "sample": (r.choices[0].message.content or "")[:300], "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump({"MINI": rec}, PROBES_P); print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def spent():
    return (sum(json.loads(l).get("usd", 0.0) for l in io.open(ROWS_P, encoding="utf-8")) if ROWS_P.exists() else 0.0) + (J(PROBES_P)["MINI"]["usd"] if PROBES_P.exists() else 0.0)


def cmd_project():
    pr = J(PROBES_P)["MINI"]; js = jobs(); ratio = pr["tok_in"] / max(1, pr["user_chars"])
    tin = sum(int((len(j["user"]) + len(j["system"])) * ratio) for j in js); tout = pr["tok_out"] * len(js)
    usd = tin / 1e6 * PRICE[0] + tout / 1e6 * PRICE[1]
    out = {"jobs": len(js), "tin": tin, "tout": tout, "projected_usd": round(usd, 4), "x1_3": round(1.3 * usd, 4), "billed_before": round(spent(), 4), "line": LINE, "runs": 1.3 * usd + spent() < LINE, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, HERE / "projection_a2.json"); print(json.dumps(out, indent=1))
    if not out["runs"]:
        sys.exit("PROJECTION OVER THE LINE -- STOP")


def cmd_run():
    assert_lineage(); redirect(); js = jobs(); assert J(HERE / "projection_a2.json")["runs"]
    have = {json.loads(l)["key"] for l in io.open(ROWS_P, encoding="utf-8")} if ROWS_P.exists() else set()
    todo = [j for j in js if j["key"] not in have]
    print(f"{len(todo)} mini calls to go (resumed past {len(have)})", flush=True)
    lock, spend, stopped, n_done = threading.Lock(), [spent()], [False], [0]

    def work(j):
        with lock:
            if spend[0] >= LINE or stopped[0]:
                stopped[0] = True; return None
        m = msgs(j); ok = lambda o: o is not None and isinstance(o.get("answer"), str)     # noqa: E731
        r = api.call(j["key"], ARM, m); o = api.parse_json(r["content"]); n_calls, failed = 1, False
        usd = 0.0 if r["cached"] else r["prompt_tokens"] / 1e6 * PRICE[0] + r["completion_tokens"] / 1e6 * PRICE[1]
        if not ok(o):
            r2 = api.call(j["key"], ARM + "#retry", m); o = api.parse_json(r2["content"]); n_calls = 2
            usd += 0.0 if r2["cached"] else r2["prompt_tokens"] / 1e6 * PRICE[0] + r2["completion_tokens"] / 1e6 * PRICE[1]
            r = r2
            if not ok(o):
                failed, o = True, {}
        rec = {"key": j["key"], "persona": j["persona"], "question": j["question"], "n_lines": j["n_lines"], "members": j["members"], "system_sha256": j["system_sha256"], "user_sha256": j["user_sha256"],
               "answer": (o.get("answer") if not failed else None), "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls, "model": LANE, "served_model": r.get("model"), "cached": r["cached"],
               "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "usd": usd, "raw": (r["content"] or "")[:400], "source": "a2 call", "when": dt.datetime.now().isoformat(timespec="seconds")}
        with lock:
            spend[0] += usd; n_done[0] += 1
            with io.open(ROWS_P, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, sort_keys=True, ensure_ascii=False) + "\n")
            if n_done[0] % 200 == 0:
                print(f"  {n_done[0]} done, billed ${spend[0]:.4f}", flush=True); api.flush()
        return rec
    try:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            out = [r for r in ex.map(work, todo) if r is not None]
    finally:
        api.flush()
    c = collections.Counter(r["status"] for r in out)
    tot = sum(r["usd"] for r in out)
    print(f"DONE {len(out)} rows; status {dict(c)}; billed this step ${tot:.4f}; amendment total ${spend[0]:.4f} against ${LINE:.2f}" + ("  >>> STOPPED AT THE LINE" if stopped[0] else ""))
    served = sorted({r["served_model"] for r in out})
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"\n### AUX-R85-A2-SPEND — Step 2, the mini run (2026-09-17; `a2/run_a2.py`; `a2/rows_a2_mini.jsonl`; cache `a2/cache_mini/`): {len(out)} distinct inputs answered ({dict(c)}), served {served}, {sum(r['tok_in'] or 0 for r in out)} in / {sum(r['tok_out'] or 0 for r in out)} out, **${tot:.4f}** plus the probe ${J(PROBES_P)['MINI']['usd']:.4f} against the section 8 worst line $0.47. Haiku 4.5 (section 8 (b)): dash, not authorized at the freeze ($1.22 expected).\n")
    if stopped[0]:
        sys.exit(1)


if __name__ == "__main__":
    {"probe": cmd_probe, "project": cmd_project, "run": cmd_run}[sys.argv[1]]()
