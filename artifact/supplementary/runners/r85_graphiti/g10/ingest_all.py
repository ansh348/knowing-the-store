"""ingest_all.py -- R85 Amendment 1, Step 2. Ingest all forty personas into Graphiti under the g10 tag. BILLED.

One `ingest.py` subprocess per persona (the script byte-identical to the spike's; `--arm stock --model gpt-4.1-mini-2025-04-14
--group-tag g10`, so the group identifier is `r85stock_<persona>_g10`, D-R85-15), eight personas at a time, falling back to
four when a run fails on rate limiting (the fallback is logistics and is logged, not a deviation; a failed persona is re-run with
`--wipe`, because a partial group would confound timeline-order invalidation). Each finished record is moved from
`ingest_runs/stock_gpt-4.1-mini-2025-04-14_<persona>.json` to `ingest_runs/g10_<persona>.json` (the amendment's name), and for
elena, tom and yoli the spike's committed record is restored from HEAD afterwards (D-R85-15). The running billed total prints
after every persona and as a REPORT line after every ten; `g10/ingest_all_status.json` carries the same state for monitoring.
Budget (amendment section 8 step 2): expected $10.17, stop at $13.22; no new persona starts once the completed-plus-running
projection would cross the stop line, and the running ones finish.

Runs in the stock venv from the repo root:
  /c/Users/[AUTHOR-1]/AppData/Local/r85_stock_venv/Scripts/python.exe r85_graphiti/g10/ingest_all.py [--workers 8] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
R85 = HERE.parent
ROOT = R85.parent
sys.path.insert(0, str(R85))
import render_episodes as R  # noqa: E402

MODEL = "gpt-4.1-mini-2025-04-14"
ARM, TAG = "stock", "g10"
RUNS = R85 / "ingest_runs"
LOGS = HERE / "logs"
ABORTED = HERE / "aborted"          # partial records of runs aborted from outside the runner, kept as billed artifacts
STATUS = HERE / "ingest_all_status.json"
SPIKE = {"elena", "tom", "yoli"}
STOP_USD = 13.22          # amendment section 8 step 2
EXPECTED_USD = 10.17
PER_PERSONA_EST = EXPECTED_USD / 40
RATE_LIMIT_MARKERS = ("429", "RateLimit", "rate_limit", "rate limit", "Too Many Requests")


def record_name(p):
    return RUNS / f"{ARM}_{MODEL}_{p}.json"


def partial_name(p):
    return RUNS / f"{ARM}_{MODEL}_{p}.partial.json"


def g10_name(p):
    return RUNS / f"g10_{p}.json"


def usd_of(path):
    try:
        return float(json.loads(path.read_text(encoding="utf-8")).get("usd", 0.0))
    except Exception:
        return 0.0


class Runner:
    def __init__(self, personas, workers, dry):
        self.todo = list(personas)
        self.workers = workers
        self.dry = dry
        self.running = {}          # persona -> (Popen, start, attempt)
        self.done = []             # (persona, usd, wall, episodes)
        self.failed = {}           # persona -> attempts
        self.lock = threading.Lock()
        self.t0 = time.time()
        self.halted = None

    # ---- accounting
    def completed_usd(self):
        return sum(u for _, u, _, _ in self.done)

    def running_usd(self):
        return sum(usd_of(partial_name(p)) for p in self.running)

    def total_usd(self):
        return self.completed_usd() + self.running_usd()

    def projection(self):
        return self.completed_usd() + max(self.running_usd(), len(self.running) * PER_PERSONA_EST)

    def status(self, note=""):
        s = {
            "utc": datetime.now(timezone.utc).isoformat(), "workers": self.workers,
            "done": len(self.done), "running": sorted(self.running), "todo": len(self.todo),
            "failed": self.failed, "completed_usd": round(self.completed_usd(), 4),
            "running_usd": round(self.running_usd(), 4), "total_usd": round(self.total_usd(), 4),
            "stop_usd": STOP_USD, "wall_minutes": round((time.time() - self.t0) / 60, 1),
            "halted": self.halted, "note": note,
            "records": [{"persona": p, "usd": u, "wall_seconds": w, "episodes": e} for p, u, w, e in self.done],
        }
        STATUS.write_text(json.dumps(s, indent=2), encoding="utf-8")
        return s

    # ---- one persona
    def launch(self, p, attempt):
        cmd = [sys.executable, str(R85 / "ingest.py"), "--persona", p, "--arm", ARM, "--model", MODEL, "--group-tag", TAG]
        # A retry wipes the partial group. So does a first attempt whose earlier run was aborted from outside the runner
        # (the first run was killed by the host for memory on 16 September with eight personas in flight; their partial
        # records were moved to g10/aborted/<persona>.attempt1.partial.json as billed artifacts, and their groups are wiped here).
        if attempt > 1 or any(ABORTED.glob(f"{p}.attempt*.partial.json")):
            cmd.append("--wipe")
        LOGS.mkdir(exist_ok=True)
        log = open(LOGS / f"{p}.attempt{attempt}.log", "w", encoding="utf-8")
        if self.dry:
            print(f"DRY  {' '.join(cmd)}")
            log.close()
            return None
        proc = subprocess.Popen(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, text=True)
        self.running[p] = (proc, time.time(), attempt, log)
        print(f"start {p:10s} attempt {attempt}  ({len(self.running)} running, {len(self.done)} done, ${self.total_usd():.2f} so far)", flush=True)
        return proc

    def finish(self, p):
        proc, start, attempt, log = self.running.pop(p)
        log.close()
        wall = time.time() - start
        text = (LOGS / f"{p}.attempt{attempt}.log").read_text(encoding="utf-8", errors="replace")
        src = record_name(p)
        if proc.returncode == 0 and src.exists() and json.loads(src.read_text(encoding="utf-8")).get("complete"):
            rec = json.loads(src.read_text(encoding="utf-8"))
            dst = g10_name(p)
            dst.write_text(json.dumps(rec, indent=2), encoding="utf-8")
            src.unlink()
            partial_name(p).unlink(missing_ok=True)
            if p in SPIKE:   # the spike's committed record was overwritten by ingest.py's fixed naming; restore it (D-R85-15)
                subprocess.run(["git", "checkout", "--", str(src.relative_to(ROOT)).replace("\\", "/")], cwd=ROOT, capture_output=True)
            self.done.append((p, float(rec["usd"]), round(wall, 1), int(rec["episodes"])))
            n = len(self.done)
            print(f"done  {p:10s} episodes={rec['episodes']:3d} usd=${rec['usd']:.4f} wall={wall/60:.1f}min   "
                  f"[{n}/40 done, running total ${self.completed_usd():.4f} completed + ${self.running_usd():.4f} in flight]", flush=True)
            if n % 10 == 0:
                print(f"REPORT {n} personas: completed ${self.completed_usd():.4f}, in flight ${self.running_usd():.4f}, "
                      f"total ${self.total_usd():.4f} of stop ${STOP_USD}; wall {(time.time()-self.t0)/60:.1f} min", flush=True)
            self.status()
            return True
        rate = any(m in text for m in RATE_LIMIT_MARKERS)
        self.failed[p] = attempt
        print(f"FAIL  {p:10s} attempt {attempt} rc={proc.returncode} rate_limited={rate}  (log {LOGS / f'{p}.attempt{attempt}.log'})", flush=True)
        if rate and self.workers > 4:
            self.workers = 4
            print("fallback: workers 8 -> 4 (rate limiting; logistics, logged)", flush=True)
        if attempt < 3:
            self.todo.insert(0, p)      # retried next, with --wipe
        else:
            self.halted = f"{p} failed three times"
        self.status()
        return False

    # ---- the loop
    def run(self):
        if self.dry:
            for p in self.todo:
                self.launch(p, 1)
            return
        attempts = {}
        while self.todo or self.running:
            for p in list(self.running):
                if self.running[p][0].poll() is not None:
                    self.finish(p)
            if self.halted:
                if not self.running:
                    break
            elif self.todo and len(self.running) < self.workers:
                if self.projection() + PER_PERSONA_EST > STOP_USD:
                    if not self.running:
                        self.halted = f"stop line ${STOP_USD} would be crossed (completed ${self.completed_usd():.4f})"
                        break
                else:
                    p = self.todo.pop(0)
                    attempts[p] = attempts.get(p, 0) + 1
                    self.launch(p, attempts[p])
                    continue
            time.sleep(5)
            self.status()
        s = self.status("finished" if not self.halted else self.halted)
        print(f"\nEND: {len(self.done)} of 40 done, completed ${self.completed_usd():.4f}, wall {s['wall_minutes']} min"
              + (f"; HALTED: {self.halted}" if self.halted else ""), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    personas = [p.stem for p in sorted(R.BANKS.glob("*.json"))]
    assert len(personas) == 40, len(personas)
    finished = [p for p in personas if g10_name(p).exists()]          # resumable: finished records are kept and counted
    personas = [p for p in personas if not g10_name(p).exists()]
    aborted = sum(usd_of(f) for f in ABORTED.glob("*.partial.json")) if ABORTED.exists() else 0.0
    print(f"{len(personas)} personas to ingest ({len(finished)} finished earlier), workers {a.workers}, stop line ${STOP_USD}, "
          f"group ids r85{ARM}_<persona>_{TAG}; aborted partial runs billed ${aborted:.4f} (g10/aborted/, wiped on their first attempt)", flush=True)
    r = Runner(personas, a.workers, a.dry_run)
    for p in finished:
        rec = json.loads(g10_name(p).read_text(encoding="utf-8"))
        r.done.append((p, float(rec["usd"]), float(rec["wall_seconds"]), int(rec["episodes"])))
    r.run()


if __name__ == "__main__":
    main()
