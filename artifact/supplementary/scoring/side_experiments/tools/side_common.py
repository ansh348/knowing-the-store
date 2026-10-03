"""side_common.py -- shared loaders and the section C.1 entry map for the side experiments
(ADDENDUM_SIDE.md, frozen e8b2630). NO API CALLS. Deterministic.

Consumers: verify_side.py (the census pins, check C), build_s1.py (the GT indexes of section S1),
and, once they exist, the S runner and the NB-4 / NB-5 readers. The mapping loop here is the one
verify_side.py ran at the freeze, moved verbatim; verify_side's pins on every census quantity are
the equivalence check.

The map (ADDENDUM_SIDE section C.1), per backend entry e of persona p over the FR-Bank entries
F(p):
  lexical channel   exp4_witnesses.supports_correct(e.text, f.text) -- at least two shared content
                    tokens and at least half of f's content tokens covered (lex_matrix below is
                    the vectorised form of that predicate, asserted equal at the freeze);
  embedding channel cosine(e, f) >= THRESH on the cached text-embedding-3-small vectors;
  target            argmax-cosine entry among lexical hits if any, else the argmax-cosine entry;
  lexical_required  (the ruling #2 fallback, Mem0 only) an entry maps only where the lexical
                    channel supports some f; the embedding channel breaks ties among lexical hits.
  state             the target's TRUE lifecycle state (index_v2.true_lifecycle), its category and
                    slot, the entry's own backend recency (index_v2 R3).
  ambiguity         a second FR-Bank candidate within AMBIG cosine of the TARGET (D-SIDE-1: the
                    target band, not the global-best band); slot-changing when its slot_key
                    differs; nearest wins.
"""
from __future__ import annotations

import collections
import io
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
for _p in ("e0_metamemory/tools", "e1_metamemory/tools", "e1r_robustness/tools", "analysis/ontology_validation"):
    if str(ROOT / _p) not in sys.path:
        sys.path.insert(0, str(ROOT / _p))

import e0_common as C                                            # noqa: E402
from e0_common import parse_dt, toks as e0_toks                  # noqa: E402
import index_v2 as IX                                            # noqa: E402
from exp4_witnesses import toks as w_toks                        # noqa: E402
import tiktoken                                                  # noqa: E402

E1 = ROOT / "e1_metamemory"
SIDE = ROOT / "side_experiments"
S1 = SIDE / "s1"
LEDGER = SIDE / "NUMBERS_SIDE.md"
ENC = tiktoken.get_encoding("o200k_base")
THRESH, AMBIG = 0.295, 0.02
BACKENDS = ("mem0", "amem")
# the mapping each backend uses after the ruling (d) spot-check (NUMBERS_SIDE.md sections 1-2)
LEXICAL_REQUIRED = {"mem0": True, "amem": False}


def J(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(obj, p):
    pathlib.Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")


# ------------------------------------------------------------------ loaders
def load_state():
    committed = J(E1 / "indexes_v2.json")["indexes"]
    rows_by = {b: collections.defaultdict(list) for b in ("frbank", "mem0", "amem")}
    for b in rows_by:
        for r in J(E1 / "backend_entries" / f"{b}.json"):
            rows_by[b][r["persona"]].append(r)
    joins = C.load_joins()
    return committed, rows_by, joins


def unit(v):
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-12)


def ages(rows, t_now):
    for r in rows:
        d = parse_dt(r["recency_time"]); r["age"] = None if d is None else max(0, (t_now - d).days)


def fr_states(joins, rows_by, persona):
    Jn = joins[persona]
    rows = sorted(rows_by["frbank"][persona], key=lambda r: r["entry_id"])
    etoks = {r["entry_id"]: e0_toks(r["text"], Jn.drop) for r in rows}
    return rows, IX.true_lifecycle(Jn, etoks)


def render_true(rows, states, events):
    """The RENDERER LOCK path: index_v2.view -> index_v2.render under AVAIL[("frbank","TRUE")]."""
    return IX.render(IX.view(rows, states, None), events, IX.AVAIL[("frbank", "TRUE")])


def lex_matrix(be_rows, fr_rows):
    fr_t = [w_toks(f["text"]) for f in fr_rows]; be_t = [w_toks(r["text"]) for r in be_rows]
    M = np.zeros((len(be_rows), len(fr_rows)), bool)
    for i, bt in enumerate(be_t):
        if not bt:
            continue
        for j, ft in enumerate(fr_t):
            if len(ft) >= 2:
                h = len(bt & ft)
                if h >= 2 and h / len(ft) >= 0.5:
                    M[i, j] = True
    return M


# ------------------------------------------------------------------ the entry map
def backend_embeddings(b):
    z = np.load(E1 / "backend_embeddings" / f"{b}.npz", allow_pickle=True)
    keys, emb = list(z["keys"]), unit(z["emb"].astype(np.float32))
    kidx = collections.defaultdict(list)
    for n, k in enumerate(keys):
        kidx[k.split("||", 1)[0]].append(n)
    return keys, emb, kidx


def map_persona(b, persona, committed, rows_by, joins, lexical_required, keys, emb, kidx):
    """One persona of one backend through the section C.1 map. Returns None where the backend
    holds no entries for the persona (Mem0's three excluded personas). Otherwise a dict with the
    per-entry mapping records, the rendered GT index text, the emitted names, and the census
    counters verify_side.py pins."""
    if b == "mem0" and persona in IX.MEM0_EXCLUDE:
        return None
    be_rows = sorted(rows_by[b].get(persona, []), key=lambda r: r["entry_id"])
    if not be_rows:
        return None
    fr_rows, (t_sup, t_ret, t_exp, t_ev) = fr_states(joins, rows_by, persona)
    zz = np.load(C.BANKS / f"{persona}_embeddings.npz", allow_pickle=True)
    fr_ids, fr_E = list(zz["ids"]), unit(zz["embeddings"].astype(np.float32))
    fr_by_id = {f["entry_id"]: f for f in fr_rows}; F = [fr_by_id[i] for i in fr_ids]
    bank = {e["id"]: e for e in J(C.BANKS / f"{persona}.json")["entries"]}
    slotkeys = [tuple(bank[f["entry_id"]].get("slot_key") or ()) for f in F]
    scrubbed = [IX.scrub(f["slot"]) for f in F]
    kpos = {keys[n].split("||", 1)[1]: n for n in kidx[persona]}
    B = np.stack([emb[kpos[r["entry_id"]]] for r in be_rows]); Cs = B @ fr_E.T
    L = lex_matrix(be_rows, F); ages(be_rows, joins[persona].t_now)
    tot = collections.Counter(); amb_any = amb_slotkey = amb_scrub = 0
    gt_rows, sup, ret, exp, target, records = [], set(), set(), set(), {}, []
    for i, r in enumerate(be_rows):
        lexhits = np.flatnonzero(L[i]); order = np.argsort(-Cs[i]); c1_all = float(Cs[i, order[0]])
        rec = {"entry_id": r["entry_id"], "persona": persona, "age": r["age"],
               "lexical_hits": int(len(lexhits)), "cos_max": round(c1_all, 6)}
        if len(lexhits):
            j = int(lexhits[np.argmax(Cs[i, lexhits])]); ch = "both" if c1_all >= THRESH else "lex"
        elif (not lexical_required) and c1_all >= THRESH:
            j = int(order[0]); ch = "emb"
        else:
            tot["unmapped"] += 1
            rec.update({"mapped": False, "channel": None, "target": None})
            records.append(rec); continue
        tot[ch] += 1; c1 = float(Cs[i, j])
        near = [k for k in np.flatnonzero(Cs[i] >= c1 - AMBIG) if k != j]
        a_any = bool(near); a_slot = any(slotkeys[k] != slotkeys[j] for k in near)
        a_scrub = any(scrubbed[k] != scrubbed[j] for k in near)
        amb_any += a_any; amb_slotkey += a_slot; amb_scrub += a_scrub
        f = F[j]; fid = f["entry_id"]; target[r["entry_id"]] = fid
        gt_rows.append({"entry_id": r["entry_id"], "category": f["category"], "slot": f["slot"], "age": r["age"]})
        if fid in t_sup: sup.add(r["entry_id"])
        if fid in t_ret: ret.add(r["entry_id"])
        if fid in t_exp: exp.add(r["entry_id"])
        rec.update({"mapped": True, "channel": ch, "target": fid, "cos": round(c1, 6),
                    "target_category": f["category"], "target_slot": f["slot"], "name": IX.scrub(f["slot"]),
                    "superseded": fid in t_sup, "retracted": fid in t_ret, "expired": fid in t_exp,
                    "ambiguous_any": a_any, "ambiguous_slotkey": a_slot, "ambiguous_scrubbed": a_scrub,
                    "n_within_band": len(near)})
        records.append(rec)
    ev_gt = [s for s in ({bid for bid, fid in target.items() if fid in ev} for ev in t_ev) if s]
    txt, blocks, names = render_true(gt_rows, (sup, ret, exp), ev_gt) if gt_rows else ("", {}, [])
    assert IX.MARKER not in txt, f"{b}:{persona}: GT index carries the inexpressibility marker"
    assert not any(":" in n for n in names), f"{b}:{persona}: GT index emits a name containing ':'"
    n_map = sum(tot[c] for c in ("lex", "emb", "both"))
    return {"backend": b, "persona": persona, "lexical_required": lexical_required,
            "n_entries": len(be_rows), "n_mapped": n_map, "lex": tot["lex"], "emb": tot["emb"], "both": tot["both"],
            "unmapped": tot["unmapped"], "amb_any": amb_any, "amb_slotkey": amb_slotkey, "amb_scrub": amb_scrub,
            "superseded": len(sup), "retracted": len(ret), "expired": len(exp), "sup_events": len(ev_gt),
            "fr_superseded": len(t_sup), "fr_retracted": len(t_ret), "fr_expired": len(t_exp), "fr_sup_events": len(t_ev),
            "lines": txt.count("\n") + 1 if txt else 0, "tokens": len(ENC.encode(txt)),
            "fr_lines": committed[f"frbank:{persona}:FULL:TRUE"].count("\n") + 1,
            "fr_tokens": len(ENC.encode(committed[f"frbank:{persona}:FULL:TRUE"])),
            "text": txt, "names": names, "records": records}


def map_backend(b, committed, rows_by, joins, lexical_required):
    """Every persona of backend b through the map, in sorted persona order."""
    keys, emb, kidx = backend_embeddings(b)
    out = {}
    for persona in sorted(joins):
        r = map_persona(b, persona, committed, rows_by, joins, lexical_required, keys, emb, kidx)
        if r is not None:
            out[persona] = r
    return out


def census(per):
    """The section C.1 census quantities over map_backend output (the dict verify_side pins)."""
    n_ent = sum(r["n_entries"] for r in per.values()); n_map = sum(r["n_mapped"] for r in per.values())
    s = lambda k: sum(r[k] for r in per.values())  # noqa: E731
    return {"n_entries": n_ent, "n_mapped": n_map, "lex": s("lex"), "emb": s("emb"), "both": s("both"),
            "unmapped": s("unmapped"), "frac": n_map / n_ent, "amb_any": s("amb_any") / n_map,
            "amb_slotkey": s("amb_slotkey") / n_map, "amb_scrub": s("amb_scrub") / n_map,
            "n_amb_any": s("amb_any"), "n_amb_slotkey": s("amb_slotkey"), "n_amb_scrub": s("amb_scrub"),
            "gt_lines": float(np.mean([r["lines"] for r in per.values()])),
            "gt_tokens": float(np.mean([r["tokens"] for r in per.values()])),
            "fr_lines": float(np.mean([r["fr_lines"] for r in per.values()])),
            "fr_tokens": float(np.mean([r["fr_tokens"] for r in per.values()])),
            "superseded": s("superseded"), "retracted": s("retracted"), "expired": s("expired"), "sup_events": s("sup_events"),
            "fr_superseded": s("fr_superseded"), "fr_retracted": s("fr_retracted"), "fr_expired": s("fr_expired"),
            "fr_sup_events": s("fr_sup_events"), "n_personas": len(per),
            "personas_at_or_above_half": sum(1 for r in per.values() if r["n_mapped"] / r["n_entries"] >= 0.5)}


def gt_key(b, persona):
    return f"{b}:{persona}:GT"
