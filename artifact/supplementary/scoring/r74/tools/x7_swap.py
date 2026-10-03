"""R77 S -- registered wrong-index control (ADDENDUM_R77 §S @ 41e31e7).

Two manipulated arms replace ONLY the index text; question, prompts, protocol, and
populations are the committed ones. Blind and intact arms are the committed E1 rows and are
never re-elicited here.

  WRONG-PERSON  each item scored against another persona's committed TRUE index, under a
                fixed seed-42 derangement (no fixed point, asserted).
  SHUFFLED      each item's OWN TRUE index with the per-category count payloads permuted
                across categories and the per-category attribute-name bodies permuted across
                categories, seed 42. Category labels stay in place, so what is destroyed is
                the index's internal correspondence, not its vocabulary or its size.

Populations (asserted): FOK = FR-Bank hard tier INTERSECT cell_661 (n=307, 35 non-ABSENT);
NOK = committed cell_661 (n=661, 104 PN). Union of items = 700; one call serves both
judgments, so each arm is 700 calls.

Subcommands: build | probe | project | run | score
"""
import collections, json, os, pathlib, random, re, sys, threading, concurrent.futures

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import prompts_e1 as P
import api as _api
_api.load_env()

X4, X7 = ROOT / "r74" / "x4", ROOT / "r74" / "x7"
X7.mkdir(parents=True, exist_ok=True)
CELL = json.load(open(X4 / "cell_661.json", encoding="utf-8"))
assert P.file_sha256() == CELL["prompts_file_sha256"], "prompts_e1 file digest drift"
assert P.texts_sha256() == CELL["prompts_texts_sha256"], "prompts_e1 texts digest drift"
IDX = json.load(open(ROOT / "e1_metamemory" / "indexes_v2.json", encoding="utf-8"))["indexes"]
LANE, PRICE = "gpt-4.1-mini", (0.40, 1.60)
SEED = 42


# ---------------------------------------------------------------- cell ----
def build_cell():
    items = json.load(open(ROOT / "e1_metamemory" / "build" / "items_final.json",
                           encoding="utf-8"))
    meta = {i["item_id"]: i for i in items}
    nok = CELL["items"]
    nok_ids = {i["item_id"] for i in nok}
    hard = {i["item_id"] for i in items
            if i["backend"] == "frbank" and i["tier"] == "hard"}
    fok_ids = hard & nok_ids
    assert len(nok) == 661 and sum(i["y_nok"] for i in nok) == 104, "NOK population drift"
    assert len(fok_ids) == 307, f"FOK population is {len(fok_ids)}, expected 307"
    rows = []
    for it in nok:
        iid = it["item_id"]
        rows.append({"item_id": iid, "persona": it["persona"], "question": it["question"],
                     "label": it["label"], "y_nok": it["y_nok"],
                     "y_fok": it["y_fok"], "in_fok": iid in fok_ids,
                     "index_key": f"frbank:{it['persona']}:FULL:TRUE"})
    extra = fok_ids - nok_ids
    assert not extra, "FOK items outside the NOK population are not registered"
    n_fokpos = sum(r["y_fok"] for r in rows if r["in_fok"])
    assert n_fokpos == 35, f"FOK positives {n_fokpos}, expected 35"
    missing = [r["index_key"] for r in rows if r["index_key"] not in IDX]
    assert not missing, f"missing committed indexes: {sorted(set(missing))[:5]}"
    return rows


# ------------------------------------------------------- index surgery ----
_NUMROW = re.compile(r"^([A-Z_]+)(\s+\d.*)$")


def shuffle_index(text, seed):
    lines = text.split("\n")
    rng = random.Random(seed)

    # (a) per-category count payloads: permute the VALUES across categories while
    # re-rendering them into each row's original fixed-width columns. Permuting the raw
    # tail instead would carry each label's padding with it and leave the table visibly
    # ragged -- a manipulation the monitor could react to as broken formatting rather than
    # as wrong correspondence, which would confound the control.
    idxs = [i for i, l in enumerate(lines) if _NUMROW.match(l)]
    if len(idxs) > 1:
        # values are RIGHT-aligned, so their end columns are constant across rows while
        # their start columns are not; align on the ends.
        ends = [m.end() for m in re.finditer(r"\d+", lines[idxs[0]])]
        same = all([m.end() for m in re.finditer(r"\d+", lines[i])] == ends for i in idxs)
        vals = [[m.group() for m in re.finditer(r"\d+", lines[i])] for i in idxs]
        perm = vals[:]
        rng.shuffle(perm)
        fits = all(all(len(v) <= e - (ends[k - 1] if k else 0)
                       for k, (v, e) in enumerate(zip(nv, ends))) for nv in perm)
        if same and fits and all(len(v) == len(ends) for v in vals):
            for i, newv in zip(idxs, perm):
                label = _NUMROW.match(lines[i]).group(1)
                buf = list(label.ljust(ends[-1]))
                for e, v in zip(ends, newv):
                    buf[e - len(v):e] = list(v)
                lines[i] = "".join(buf)
        else:                       # ragged source: fall back to tail permutation
            tails = [_NUMROW.match(lines[i]).group(2) for i in idxs]
            pt = tails[:]; rng.shuffle(pt)
            for i, t in zip(idxs, pt):
                lines[i] = _NUMROW.match(lines[i]).group(1) + t

    # (b) per-category attribute-name bodies: keep the header, permute the body
    blocks, cur = [], None
    try:
        start = lines.index("ATTRIBUTE NAMES BY CATEGORY  (value-scrubbed; names only, "
                            "max 15 per category, alphabetical)") + 1
    except ValueError:
        start = None
    if start is not None:
        i = start
        while i < len(lines) and lines[i].strip():
            m = re.match(r"^([A-Z_]+): (.*)$", lines[i])
            if m:
                if cur:
                    blocks.append(cur)
                cur = {"head": i, "cat": m.group(1), "body": [m.group(2)]}
            elif cur is not None and lines[i].startswith("    "):
                cur["body"].append(lines[i])
            i += 1
        if cur:
            blocks.append(cur)
        if len(blocks) > 1:
            bodies = [b["body"] for b in blocks]
            perm = bodies[:]
            rng.shuffle(perm)
            out, w = [], 0
            for j, b in enumerate(blocks):
                if j == 0:
                    out = lines[:b["head"]]
                new = perm[j]
                out.append(f"{b['cat']}: {new[0]}")
                out.extend(new[1:])
                w = b["head"] + len(b["body"])
            out.extend(lines[w:])
            lines = out
    return "\n".join(lines)


def derangement(names, seed):
    rng = random.Random(seed)
    names = sorted(names)
    while True:
        perm = names[:]
        rng.shuffle(perm)
        if all(a != b for a, b in zip(names, perm)):
            return dict(zip(names, perm))


def arms(rows):
    personas = sorted({r["persona"] for r in rows})
    der = derangement(personas, SEED)
    assert all(k != v for k, v in der.items()), "derangement has a fixed point"
    wrong, shuf, deltas = {}, {}, []
    for r in rows:
        wrong[r["item_id"]] = IDX[f"frbank:{der[r['persona']]}:FULL:TRUE"]
        s = shuffle_index(IDX[r["index_key"]], SEED)
        shuf[r["item_id"]] = s
        deltas.append(len(s) - len(IDX[r["index_key"]]))
    return der, wrong, shuf, deltas


# ------------------------------------------------------------ plumbing ----
def last_json(text):
    depth, start, best, ins, esc = 0, None, None, False, False
    for i, ch in enumerate(text or ""):
        if ins:
            ins = not (ch == '"' and not esc); esc = (ch == "\\" and not esc)
            continue
        if ch == '"': ins, esc = True, False
        elif ch == "{":
            if depth == 0: start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None: best = text[start:i + 1]
    try:
        return json.loads(best) if best else None
    except Exception:
        return None


def clamp(v):
    try: v = float(v)
    except (TypeError, ValueError): return None
    if v > 1: v /= 100.0
    return max(0.0, min(1.0, v))


def call(row, arm, index_text):
    from openai import OpenAI
    cl = OpenAI()
    user = P.USER_INDEXED.format(index=index_text, question=row["question"])
    r = cl.chat.completions.create(model=LANE, temperature=P.TEMPERATURE, seed=P.SEED,
                                   max_tokens=P.MAX_TOKENS,
                                   messages=[{"role": "system", "content": P.SYSTEM},
                                             {"role": "user", "content": user}])
    txt = r.choices[0].message.content
    j = last_json(txt) or {}
    fok, nok = clamp(j.get("fok")), clamp(j.get("nok"))
    u = r.usage
    return {"item_id": row["item_id"], "arm": arm, "draw": 1, "label": row["label"],
            "y_fok": row["y_fok"], "y_nok": row["y_nok"], "in_fok": row["in_fok"],
            "fok": fok, "nok": nok, "status": "OK" if fok is not None else "PARSE_FAIL",
            "served_model": r.model, "tok_in": u.prompt_tokens, "tok_out": u.completion_tokens,
            "usd": (u.prompt_tokens / 1e6 * PRICE[0] + u.completion_tokens / 1e6 * PRICE[1]),
            "text": (txt or "")[:2000]}


ROWS_P = X7 / "rows_SWAP.jsonl"


def done_keys():
    ks = set()
    if ROWS_P.exists():
        for l in open(ROWS_P, encoding="utf-8"):
            r = json.loads(l)
            ks.add((r["item_id"], r["arm"]))
    return ks


def cmd_build():
    rows = build_cell()
    der, wrong, shuf, deltas = arms(rows)
    meta = {"n_items": len(rows), "n_fok": sum(r["in_fok"] for r in rows),
            "n_nok_pos": sum(r["y_nok"] for r in rows),
            "n_fok_pos": sum(r["y_fok"] for r in rows if r["in_fok"]),
            "personas": len(der), "derangement_fixed_points": 0,
            "shuffle_len_delta": {"min": min(deltas), "max": max(deltas),
                                  "mean": sum(deltas) / len(deltas),
                                  "n_zero": sum(1 for d in deltas if d == 0)},
            "derangement": der}
    json.dump(meta, open(X7 / "x7_cell.json", "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in meta.items() if k != "derangement"}, indent=1))
    ex = rows[0]
    print("\n-- SHUFFLED sample (first 24 lines of the per-category block) --")
    for l in shuf[ex["item_id"]].split("\n")[11:24]:
        print("   ", l[:96])


def cmd_probe():
    rows = build_cell()
    _, wrong, shuf, _ = arms(rows)
    out = {}
    for arm, m in (("WRONG-PERSON", wrong), ("SHUFFLED", shuf)):
        r = call(rows[0], arm, m[rows[0]["item_id"]])
        out[arm] = {"served": r["served_model"], "identifier_ok": LANE in r["served_model"],
                    "tok_in": r["tok_in"], "tok_out": r["tok_out"], "status": r["status"],
                    "usd": r["usd"], "sample": r["text"][:140]}
    json.dump(out, open(X7 / "x7_probes.json", "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1))
    if not all(v["identifier_ok"] for v in out.values()):
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if any(v["status"] != "OK" for v in out.values()):
        sys.exit("PROBE PARSE FAILURE -- do not launch; needs a D-entry, not a retry")


def cmd_project():
    p = json.load(open(X7 / "x7_probes.json", encoding="utf-8"))
    rows = build_cell()
    n = len(rows)
    tin = sum(v["tok_in"] for v in p.values()) * n
    tout = sum(v["tok_out"] for v in p.values()) * n
    usd = tin / 1e6 * PRICE[0] + tout / 1e6 * PRICE[1]
    print(f"calls        : {2 * n}  ({n} items x 2 manipulated arms, k=1)")
    print(f"projected in : {tin:,} tok   out: {tout:,} tok")
    print(f"PROJECTED    : ${usd:.4f}    registered ceiling $5.00")
    if usd > 5.0:
        sys.exit("PROJECTION ABOVE CEILING -- STOP per registration")


def cmd_run():
    rows = build_cell()
    _, wrong, shuf, _ = arms(rows)
    done = done_keys()
    jobs = [(r, a, (wrong if a == "WRONG-PERSON" else shuf)[r["item_id"]])
            for r in rows for a in ("WRONG-PERSON", "SHUFFLED")
            if (r["item_id"], a) not in done]
    print(f"{len(jobs)} calls to go (resumed past {len(done)})")
    lock, spend = threading.Lock(), [0.0]

    def work(j):
        row, arm, idx = j
        for attempt in (1, 2, 3):
            try:
                r = call(row, arm, idx); break
            except Exception as e:
                if attempt == 3:
                    r = {"item_id": row["item_id"], "arm": arm, "draw": 1,
                         "status": f"ERROR:{type(e).__name__}"}
                else:
                    import time; time.sleep(4 * attempt)
        with lock:
            spend[0] += r.get("usd", 0.0)
            with open(ROWS_P, "a", encoding="utf-8") as f:
                f.write(json.dumps(r, sort_keys=True) + "\n")
        return r
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(work, jobs))
    print(f"DONE; session spend ${spend[0]:.4f}")


if __name__ == "__main__":
    globals()["cmd_" + sys.argv[1]]()
