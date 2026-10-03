"""
m2_renderer.py -- M2: the renderer 2x2 on the structureless backends. RAW ONLY.

Exactly per modules/M2_RENDERER_AXIS.md. Computes NO delta, NO AUROC, NO ordering
verdict -- that happens at scoring, after the SP3 go.

The 2x2 is (marker shown | omitted) x (counts shown | removed). THREE CELLS ARE
ALREADY COMMITTED and are NOT re-run:

  marked            E1 INDEXED-TRUE            (elicitation_main.json)
  marker-omitted    E1.5 Run B                 (run_b_nomarker.json)

This module runs the two count-removed cells on the FULL external scoreable set
(A-MEM 284 + Mem0 238 = 522), because E1.8's A3 covered only the external hard
tier, which is single-class and admits no AUROC:

  a3-style   marker shown,   counts removed   -> prompts_e1.USER_INDEXED
  minimal    marker omitted, counts removed   -> prompts_e1.USER_INDEXED_NOMARKER   [NEW CELL]

Count removal reuses E1.8's committed count-site machinery verbatim
(`mechanism_arms.rewrite`, every count -> "-"). Marker omission reuses E1.5's
committed `run_b.strip_markers` verbatim. Neither is reimplemented here, so the
cells are byte-comparable to the arms they extend.

  lane   gpt-4.1-mini, temperature 0, seed 42, k=1, TRUE provenance
  cost   1,044 calls, ~$0.55

Usage:  python e2_metamemory/tools/m2_renderer.py
"""

from __future__ import annotations

import collections
import concurrent.futures as cf
import importlib.util as ilu
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"
sys.path.insert(0, str(E1 / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import e2_api as api                                              # noqa: E402
import prompts_e1 as P1                                           # noqa: E402
from e2_common import E2, jdump, jload, sha                       # noqa: E402
from mechanism_arms import rewrite                                # noqa: E402

WORKERS = 12
SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}
E1_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"


def load_strip_markers():
    """Import E1.5 Run B's strip_markers without executing the module body."""
    src = (E1 / "tools" / "run_b.py").read_text(encoding="utf-8")
    head = src[:src.index("\njobs =")] if "\njobs =" in src else src
    ns = {"__name__": "_runb", "__file__": str(E1 / "tools" / "run_b.py")}
    exec(compile(head, str(E1 / "tools" / "run_b.py"), "exec"), ns)   # noqa: S102
    return ns["strip_markers"]


def clamp(v):
    try:
        return min(100.0, max(0.0, float(v))) / 100.0
    except (TypeError, ValueError):
        return None


def main():
    got = P1.texts_sha256()
    assert got == E1_TEXTS_SHA, f"frozen prompts changed: {got}"
    strip_markers = load_strip_markers()

    items = [i for i in jload(E1 / "build" / "items_final.json")
             if i["backend"] in ("amem", "mem0")
             and i.get("label", i["label_pre"]) in SCOREABLE]
    qmap = {r["tag"]: r["question"] for r in jload(E1 / "elicitation_main.json")
            if r["arm"] != "BLIND"}
    idx = jload(E1 / "indexes_v2.json")["indexes"]

    def a3(_slot, _tok):
        return "-"

    jobs = []
    for it in items:
        q = qmap.get(it["item_id"])
        k = f"{it['backend']}:{it['persona']}:{it['variant']}:TRUE"
        if not q or k not in idx:
            continue
        base = idx[k]
        nocounts = rewrite(base, a3)
        jobs.append((it, "a3-style", nocounts, False))
        jobs.append((it, "minimal", strip_markers(nocounts), True))

    n_items = len({j[0]["item_id"] for j in jobs})
    print(f"M2: {n_items} external items x 2 new cells = {len(jobs)} calls")
    print(f"  (marked and marker-omitted cells are COMMITTED and not re-run)")
    samp = next(j for j in jobs if j[1] == "minimal")
    print(f"  marker present in any minimal index? "
          f"{any('not expressible' in j[2] for j in jobs if j[1] == 'minimal')}")
    print(f"  sample minimal index, first 8 lines:")
    for ln in samp[2].split("\n")[:8]:
        print(f"    {ln}")

    def run(job):
        it, cell, index, nomarker = job
        tmpl = P1.USER_INDEXED_NOMARKER if nomarker else P1.USER_INDEXED
        msgs = [{"role": "system", "content": P1.SYSTEM},
                {"role": "user", "content": tmpl.format(
                    index=index, question=qmap[it["item_id"]])}]
        r = api.call(it["item_id"], f"m2-{cell}", msgs)
        o = api.parse_json(r["content"]) or {}
        api.check_cap()
        return {"item_id": it["item_id"], "cell": cell,
                "backend": it["backend"], "variant": it["variant"],
                "label": it.get("label", it["label_pre"]),
                "persona": it["persona"],
                "marker": "omitted" if nomarker else "shown", "counts": "removed",
                "fok": clamp(o.get("fok")), "nok": clamp(o.get("nok")),
                "index_sha": sha(index),
                "status": "OK" if clamp(o.get("fok")) is not None else "PARSE_FAIL",
                "cached": r["cached"]}

    out = []
    try:
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
            for n, rec in enumerate(ex.map(run, jobs), 1):
                out.append(rec)
                if n % 300 == 0:
                    api.flush()
                    print(f"  {n}/{len(jobs)}  ${api.spend()[0]:.4f}", flush=True)
    finally:
        api.flush()

    jdump({"module": "M2", "design": "2x2 marker x counts; two NEW cells only",
           "committed_cells_not_rerun": {
               "marked": "E1 INDEXED-TRUE (elicitation_main.json)",
               "marker-omitted": "E1.5 Run B (run_b_nomarker.json)"},
           "model": "gpt-4.1-mini", "k": 1, "provenance": "TRUE",
           "n": len(out), "rows": out}, E2 / "m2_renderer_raw.json")

    c = collections.Counter((r["cell"], r["backend"], r["status"]) for r in out)
    print("\nper-cell parse census (RAW, no delta computed):")
    for cell in ("a3-style", "minimal"):
        for b in ("amem", "mem0"):
            print(f"  {cell:10s} {b:5s} OK {c[(cell,b,'OK')]:4d}  "
                  f"PARSE_FAIL {c[(cell,b,'PARSE_FAIL')]:3d}")
    print(f"E2 cumulative ${api.spend()[0]:.4f} of ${api.E2_CAP_USD}")
    print("wrote m2_renderer_raw.json -- 2x2 not scored")


if __name__ == "__main__":
    main()
