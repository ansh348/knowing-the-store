# -*- coding: utf-8 -*-
"""cf2_names_counts.py -- ADDENDUM_CF2_NAMES_COUNTS (E2, program R117): names against counts on the 444 items of the counterfactual set.
Renderings, pure functions of the recorded v2 text (cf2/cf_indexes.json key v2):
  NAMES-ONLY   every count line removed: the "entries in this store" line, the LIFECYCLE TOTALS block, the PER-CATEGORY BREAKDOWN block,
               the AGE DISTRIBUTION block, and the "(+N more)" overflow markers; the title, the ages sentence, RECENCY and both name blocks kept.
  COUNTS-ONLY  the ATTRIBUTE NAMES BY CATEGORY block and the ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT block removed; the rest byte-identical.
  NAMES-DASH   the committed E1.8 A3 rule (e1_metamemory/tools/mechanism_arms.rewrite, every count -> "-"), GPT-4.1 mini only (secondary).
Lanes: GPT-4.1 mini k = 1 temperature 0 max_tokens 200 synchronous (INDEXED-NAMES, INDEXED-COUNTS, INDEXED-NAMES-DASH);
Haiku 4.5 k = 5 temperature 0 max_tokens 200 Message Batches (INDEXED-NAMES, INDEXED-COUNTS). Prompts prompts_e1 verbatim (digests asserted
at import by run_cf). Rows cf2/rows/rows_MINI_nc.jsonl, rows_H45_nc.jsonl; batch cf2/rows/batch_H45_nc.json; lock cf2/rows/lock_nc.json.
Registration registrations/ADDENDUM_CF2_NAMES_COUNTS.md, registered-text sha256 6cd4cb94..., frozen at 177697a. Cap 10 USD.

Subcommands:  build | lock | probe <lane> | project | sync gpt-4.1-mini | submit claude-haiku-4-5-20251001 | poll claude-haiku-4-5-20251001
"""
from __future__ import annotations

import concurrent.futures as cf
import datetime as dt
import hashlib
import io
import json
import re
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import cf2_run as C2  # noqa: E402
import mechanism_arms as MA  # noqa: E402
RC = C2.RC

REG = ROOT / "registrations" / "ADDENDUM_CF2_NAMES_COUNTS.md"
REG_SHA = "6cd4cb94c3a3a4dce43da23640fbf05828f93da0d322f3f9db7da0761768db2c"
FROZEN_AT = "177697a"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
CAP = 10.00
ROWS_DIR = C2.CF2 / "rows"
BUILD = C2.CF2 / "build_nc.json"
LOCK = ROWS_DIR / "lock_nc.json"
PROBES = ROWS_DIR / "probes_nc.json"
ARMS = {"gpt-4.1-mini": ("INDEXED-NAMES", "INDEXED-COUNTS", "INDEXED-NAMES-DASH"),
        "claude-haiku-4-5-20251001": ("INDEXED-NAMES", "INDEXED-COUNTS")}
BLOCKS = ("LIFECYCLE TOTALS", "PER-CATEGORY BREAKDOWN", "RECENCY", "AGE DISTRIBUTION", "ATTRIBUTE NAMES BY CATEGORY", "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT")
OVERFLOW = re.compile(r",?\s*\(\+\S+\s+more\)")          # the marker, also when the 150-column wrap splits it over two lines
OVERFLOW_TAIL = re.compile(r",?\s*(\(\+\S*( more\))?)?$")  # the marker, its first half, or the comma before a marker wrapped whole onto the next line


def blocks(t):
    out, cur = {}, "HEAD"; out[cur] = []
    for ln in t.split("\n"):
        hit = [b for b in BLOCKS if ln.startswith(b)]
        if hit:
            cur = hit[0]; out[cur] = []
        out[cur].append(ln)
    return out


def names_only(t):
    b = blocks(t); keep = []
    for k, ls in b.items():
        if k in ("LIFECYCLE TOTALS", "PER-CATEGORY BREAKDOWN", "AGE DISTRIBUTION"):
            continue
        for ln in ls:
            if k == "HEAD" and ln.startswith("entries in this store"):
                continue
            keep.append(ln)
    return OVERFLOW.sub("", "\n".join(keep))


def counts_only(t):
    b = blocks(t); keep = []
    for k, ls in b.items():
        if k in ("ATTRIBUTE NAMES BY CATEGORY", "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT"):
            continue
        keep += ls
    return "\n".join(keep)


def names_dash(t):
    return MA.rewrite(t, lambda _slot, _tok: "-")


RENDER = {"INDEXED-NAMES": names_only, "INDEXED-COUNTS": counts_only, "INDEXED-NAMES-DASH": names_dash}


def reg_sha():
    b = REG.read_bytes(); i = b.find(FROZEN_END); assert i > 0
    return hashlib.sha256(b[:i]).hexdigest()


def setup():
    assert reg_sha() == REG_SHA, "REGISTRATION SHA MISMATCH -- STOP"
    RC.load_env()


def units(arm):
    idx = RC.IDX
    return [{"unit_id": it["item_id"], "question": it["question"], "index": RENDER[arm](idx[it["item_id"]]["v2"])} for it in RC.CELL]


def locks(t, arm, rendered):
    v2_lines = t.split("\n"); r_lines = rendered.split("\n")
    if arm == "INDEXED-NAMES":
        b = blocks(rendered)
        for k in ("LIFECYCLE TOTALS", "PER-CATEGORY BREAKDOWN", "AGE DISTRIBUTION"):
            assert k not in b, (arm, k)
        assert not any(ln.startswith("entries in this store") for ln in r_lines)
        assert "(+" not in rendered and " more)" not in rendered
        # D-NC-1: the registered wording "no digit outside the RECENCY block and the age sentence" is over-strict as written (the name-block
        # header reads "max 15 per category" and attribute names carry digits); the lock enforced is its intent: every kept line is a v2 line
        # byte-identical or with its overflow marker removed, and no count line survives.
        v2set = set(v2_lines)

        def kept_ok(ln):
            return ln in v2set or any(L.startswith(ln) and OVERFLOW_TAIL.fullmatch(L[len(ln):]) for L in v2_lines)
        assert all(kept_ok(ln) for ln in r_lines), (arm, "a kept line is not a v2 line")
        for k in ("LIFECYCLE TOTALS", "PER-CATEGORY BREAKDOWN", "AGE DISTRIBUTION"):
            assert not any(ln.startswith(k) for ln in r_lines)
    elif arm == "INDEXED-COUNTS":
        assert "ATTRIBUTE NAMES" not in rendered
        assert all(ln in v2_lines for ln in r_lines), (arm, "a kept line differs")
        bt, br = blocks(t), blocks(rendered)
        for k in ("HEAD", "LIFECYCLE TOTALS", "PER-CATEGORY BREAKDOWN", "RECENCY", "AGE DISTRIBUTION"):
            assert br.get(k) == bt.get(k), (arm, "a kept block differs", k)
        assert set(br) == set(bt) - {"ATTRIBUTE NAMES BY CATEGORY", "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT"}
    elif arm == "INDEXED-NAMES-DASH":
        assert MA.strip_counts(rendered) == MA.strip_counts(t), (arm, "non-count text changed")
        assert all(tok == "-" for _i, _k, _s, tok, _e in MA.count_sites(rendered)[1]), (arm, "a count survived")
        assert len(r_lines) == len(v2_lines)


def cmd_build():
    setup()
    import tiktoken
    enc = tiktoken.get_encoding("o200k_base")
    sysn = len(enc.encode(RC.P.SYSTEM))
    rec = {"registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "prompts_texts_sha256": RC.P.texts_sha256(), "arms": {}, "when": dt.datetime.now().isoformat(timespec="seconds")}
    for arm, fn in RENDER.items():
        toks, shas = [], []
        for it in RC.CELL:
            t = RC.IDX[it["item_id"]]["v2"]; r = fn(t)
            locks(t, arm, r)
            toks.append(len(enc.encode(RC.P.USER_INDEXED.format(index=r, question=it["question"]))) + sysn + 11)
            shas.append(hashlib.sha256(r.encode("utf-8")).hexdigest())
        rec["arms"][arm] = {"n": len(toks), "prompt_tokens_mean": round(sum(toks) / len(toks), 1), "prompt_tokens_max": max(toks), "texts_sha256": hashlib.sha256("".join(shas).encode()).hexdigest(), "lock": "asserted on every version"}
        print(arm, rec["arms"][arm])
    io.open(BUILD, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1, sort_keys=True) + "\n")


def cmd_lock():
    setup(); assert BUILD.exists()
    b = json.load(io.open(BUILD, encoding="utf-8"))
    rec = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "build": b, "lanes": {m: {"arms": list(a), "k": RC.LANES[m]["k"], "temperature": RC.LANES[m]["temp"], "max_tokens": RC.LANES[m]["max_tokens"]} for m, a in ARMS.items()},
           "cap_usd": CAP, "when": dt.datetime.now().isoformat(timespec="seconds")}
    io.open(LOCK, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    print("lock written")


def rows_path(lane):
    return ROWS_DIR / f"rows_{RC.LANES[lane]['code']}_nc.jsonl"


def cmd_probe(lane):
    setup(); assert LOCK.exists()
    rows = [RC.call_once(lane, units(arm)[0], arm, 0) for arm in ARMS[lane]]
    ok = all(lane.split("-2025")[0] in r["served_model"] or lane in r["served_model"] for r in rows)
    rec = {"lane": lane, "served": rows[0]["served_model"], "identifier_ok": ok, "in": {arm: r["tok_in"] for arm, r in zip(ARMS[lane], rows)}, "out": [r["tok_out"] for r in rows],
           "parsed": [r["status"] for r in rows], "usd": [round(r["usd"], 6) for r in rows], "sample": rows[0]["text"][:200], "when": dt.datetime.now().isoformat(timespec="seconds")}
    d = json.load(io.open(PROBES, encoding="utf-8")) if PROBES.exists() else {}
    d[lane] = rec
    io.open(PROBES, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")


def cmd_project():
    d = json.load(io.open(PROBES, encoding="utf-8")); total = 0.0
    for lane, rec in sorted(d.items()):
        cfg = RC.LANES[lane]; k = cfg["k"]; n = k * len(RC.CELL) * len(ARMS[lane])
        tin = k * len(RC.CELL) * sum(rec["in"].values()); tout = n * max(1, sum(rec["out"]) / len(rec["out"]))
        usd = (tin / 1e6 * cfg["price"][0] + tout / 1e6 * cfg["price"][1]) * cfg["mult"]; total += usd
        print(f"{lane:28s} calls={n} in={tin/1e6:.3f}M out={tout/1e6:.3f}M mult={cfg['mult']} -> ${usd:.2f} (x1.3 ${usd*1.3:.2f})")
    print(f"TOTAL projected ${total:.2f}, x1.3 ${total*1.3:.2f} against the cap ${CAP}")
    if total * 1.3 > CAP:
        raise SystemExit("PROJECTION EXCEEDS THE CAP -- do not launch")


def cmd_sync(lane):
    setup(); cfg = RC.LANES[lane]; assert cfg["k"] == 1
    path = rows_path(lane); done = set()
    if path.exists():
        for l in io.open(path, encoding="utf-8"):
            r = json.loads(l); done.add((r["unit_id"], r["arm"], r["draw"]))
    jobs = [(u, arm, 1) for arm in ARMS[lane] for u in units(arm) if (u["unit_id"], arm, 1) not in done]
    print(f"{lane}: {len(jobs)} calls to go (resumed past {len(done)})", flush=True)
    lock, spend = threading.Lock(), [0.0]

    def work(j):
        u, arm, d = j
        for attempt in (1, 2, 3):
            try:
                row = RC.call_once(lane, u, arm, d); break
            except Exception as e:  # noqa: BLE001
                if attempt == 3:
                    row = {"unit_id": u["unit_id"], "arm": arm, "model": lane, "draw": d, "status": f"ERROR:{type(e).__name__}"}
                else:
                    time.sleep(5 * attempt)
        with lock:
            spend[0] += row.get("usd", 0.0)
            with io.open(path, "a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(row, sort_keys=True) + "\n")
            assert spend[0] <= CAP, "CAP"
        return row

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for n, _ in enumerate(ex.map(work, jobs), 1):
            if n % 200 == 0:
                print(n, "/", len(jobs), f"lane-spend ${spend[0]:.4f}", flush=True)
    print(f"{lane} DONE; session spend ${spend[0]:.4f}", flush=True)


def cmd_submit(lane):
    setup()
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    cfg = RC.LANES[lane]; meta_p = ROWS_DIR / f"batch_{cfg['code']}_nc.json"
    assert not meta_p.exists() and not rows_path(lane).exists(), "a batch or rows file exists -- STOP"
    reqs = []
    for ai, arm in enumerate(ARMS[lane]):
        for i, u in enumerate(units(arm)):
            sysm, user = RC.prompts_for(u, arm)
            for d in range(1, cfg["k"] + 1):
                kw = dict(model=lane, max_tokens=cfg["max_tokens"], system=sysm, messages=[{"role": "user", "content": user}])
                if cfg["temp"] is not None:
                    kw["temperature"] = cfg["temp"]
                reqs.append(Request(custom_id=f"{cfg['code']}-{ai}-{i:04d}-d{d}", params=MessageCreateParamsNonStreaming(**kw)))
    b = RC.anthropic_client().messages.batches.create(requests=reqs)
    io.open(meta_p, "w", encoding="utf-8", newline="\n").write(json.dumps({"id": b.id, "lane": lane, "n": len(reqs), "arms": list(ARMS[lane]), "submitted": dt.datetime.now().isoformat(timespec="seconds")}) + "\n")
    print("submitted", b.id, len(reqs), "requests")


def cmd_poll(lane):
    setup(); cfg = RC.LANES[lane]; meta_p = ROWS_DIR / f"batch_{cfg['code']}_nc.json"
    meta = json.load(io.open(meta_p, encoding="utf-8")); cl = RC.anthropic_client()
    b = cl.messages.batches.retrieve(meta["id"]); print(meta["id"], b.processing_status, b.request_counts)
    if b.processing_status != "ended":
        return
    if rows_path(lane).exists():
        print("rows already collected"); return
    by = {ai: units(arm) for ai, arm in enumerate(ARMS[lane])}
    n_ok = 0; spend = 0.0
    with io.open(rows_path(lane), "w", encoding="utf-8", newline="\n") as f:
        for res in cl.messages.batches.results(meta["id"]):
            code, ai, i, d = res.custom_id.split("-"); arm = ARMS[lane][int(ai)]; u = by[int(ai)][int(i)]
            if res.result.type == "succeeded":
                m = res.result.message; text = "".join(bl.text for bl in m.content if bl.type == "text")
                row = RC.make_row(u, arm, lane, int(d[1:]), text, m.usage.input_tokens, m.usage.output_tokens, cfg["price"], cfg["mult"], m.model); n_ok += 1; spend += row["usd"]
            else:
                row = {"unit_id": u["unit_id"], "arm": arm, "model": lane, "draw": int(d[1:]), "status": "BATCH_" + res.result.type.upper()}
            row["batch_id"] = meta["id"]
            f.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"collected; ok {n_ok}; ${spend:.4f}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("build", "lock", "project"):
        globals()["cmd_" + cmd]()
    else:
        globals()["cmd_" + cmd](sys.argv[2])
