"""Batch natural-absent probe generation for all 40 personas (7 drafts each)."""
import sys, json, io, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "e0_metamemory" / "tools"))
import natural_absent as na
from e0_common import BANKS
import api

personas = sorted(p.stem for p in BANKS.glob("*.json"))
done, tot_draft, tot_surv = [], 0, 0
for n, p in enumerate(personas, 1):
    out = na.E1 / f"natural_absent_{p}.json"
    if not out.exists():
        try:
            na.cmd_run(p, 7)
        except Exception as ex:
            print(f"  !! {p}: {type(ex).__name__}: {ex}")
            continue
    d = json.load(io.open(out, encoding="utf-8"))
    tot_draft += d["n_drafted"]; tot_surv += d["n_survived_screen"]
    done.append((p, d["n_drafted"], d["n_survived_screen"]))
    if n % 10 == 0:
        print(f"  ...{n}/40 personas, ${api.meter()['usd']:.4f}", flush=True)
api.flush()
print("=" * 70)
print(f"personas {len(done)}  drafted {tot_draft}  survived screen {tot_surv} "
      f"({tot_surv/max(tot_draft,1):.0%})")
c = collections.Counter(s for _, _, s in done)
print("survivors per persona:", dict(sorted(c.items())))
print(f"personas with <4 survivors: {[p for p,_,s in done if s<4]}")
print(f"spend ${api.meter()['usd']:.4f}")
json.dump({"personas": [{"persona":p,"drafted":d,"survived":s} for p,d,s in done],
           "total_drafted": tot_draft, "total_survived": tot_surv},
          io.open(na.E1/"natural_absent_summary.json","w",encoding="utf-8",newline="\n"),
          ensure_ascii=False, indent=2, sort_keys=True)
