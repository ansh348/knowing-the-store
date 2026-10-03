"""build_l1.py -- RESP Phase B step 2: the V2-OWN indexes (ADDENDUM_RESP.md section L1) and NB-6 on them.

NO API CALLS. Deterministic (local encoder, offline).

  1. The L1 census of section C.2 (resp_common.l1_census: T(q), tau, removed names per item),
     asserted against every frozen count.
  2. l1/indexes_own.json: 661 texts keyed by item id. Changed items (102): the committed TRUE index
     with the superseded-names section re-rendered over the names that remain (own names and
     neighbours at cosine >= tau removed); every byte before the section header untouched.
     Unchanged items (559): the committed TRUE text verbatim (their V2-OWN score is the committed
     TRUE score, read, not re-elicited -- section L1).
  3. NB-6 reproduction gate: run_nb6.emb_scores / lex_scores on the committed TRUE texts of the 661
     reproduce results/nb6.json (embedding 0.7484, lexical as committed) at four decimals; a failure
     is a STOP. Then NB-6 (both variants) on the V2-OWN texts, whole population and per state
     (positives of one state against the same 557 negatives), written to l1/nb6_own.json and
     ledgered under AUX-RESP-L1-NB6 before any monitor call.
  4. Ledger keys: AUX-RESP-L1-LOCK, -L1-CENSUS, -L1-TAU, -L1-NB6-GATE, -L1-NB6 appended to
     NUMBERS_RESP.md.
"""
from __future__ import annotations

import collections
import datetime as dt
import io
import sys

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import resp_common as RC                                                     # noqa: E402
from resp_common import L1, LEDGER, J, jdump                                 # noqa: E402
from common_e1r import auroc                                                 # noqa: E402
from run_nb6 import emb_scores, lex_scores                                   # noqa: E402

STATES = (("sup", "supersession"), ("exp", "expiry"), ("ret", "retraction"))


def nb6_rows(sub, texts):
    """Rows for run_nb6's scorers: the superseded-names list of each item's text through the
    committed parser ('(none)' kept as a name, as the committed NB-6 scored it)."""
    return [{"item_id": it["item_id"], "question": it["question"], "y": it["y_nok"], "state": it["state"],
             "sup": RC.section_names(texts[it["item_id"]])} for it in sub]


def nb6_scores(rows):
    return np.array(emb_scores(rows, "sup")), np.array(lex_scores(rows, "sup"))


def per_state(scores, rows):
    y = np.array([r["y"] for r in rows], int)
    out = {"all": float(auroc(scores, y))}
    neg = [k for k, r in enumerate(rows) if r["y"] == 0]
    assert len(neg) == 557
    for st, name in STATES:
        pos = [k for k, r in enumerate(rows) if r["y"] == 1 and r["state"] == st]
        keep = sorted(pos + neg)
        out[name] = float(auroc(scores[keep], y[keep]))
    return out


def main():
    sub = RC.load_cell()
    idx = RC.indexes()
    tau, null, rows, names, pairs = RC.l1_census(sub)
    c = RC.census_counts(rows)
    assert round(tau, 6) == RC.EXPECT_TAU and null["n_pairs"] == 577, (tau, null)
    for k, v in RC.EXPECT_C2.items():
        assert c[k] == v, (k, c[k], v)
    ok, bad = RC.section_lock(sorted({it["index_key"] for it in sub}))
    assert ok == 242 and not bad, (ok, bad)

    # ---- the texts
    items, changed = {}, 0
    for it, r in zip(sub, rows):
        assert r["item_id"] == it["item_id"]
        committed = idx[it["index_key"]]
        if r["changed"]:
            text = RC.own_text(committed, r["remaining"]); changed += 1
            assert text != committed and text.startswith(RC.split_section(committed)[0])
            assert [n for n in RC.section_names(text) if n != "(none)"] == sorted(set(r["remaining"]))
        else:
            text = committed
        assert RC.IX.MARKER not in text and not any(":" in n for n in RC.section_names(text) if n != "(none)")
        items[it["item_id"]] = {"index_key": it["index_key"], "text": text, "changed": r["changed"], "removed": r["removed"],
                               "reason": r["reason"], "remaining": r["remaining"], "own": r["own"], "emptied": r["emptied"],
                               "label": it["label"], "state": it["state"], "variant": it["variant"]}
    assert changed == 102
    meta = {"registration": "registrations/ADDENDUM_RESP.md", "frozen": RC.FREEZE, "section": "L1 V2-OWN", "no_api_calls": True,
            "tau": tau, "null": null, "n_names": len(names), "n_within_section_pairs": len(pairs), "census": {k: (list(v) if isinstance(v, tuple) else v) for k, v in c.items()},
            "rule": "committed TRUE index; the superseded-names section re-rendered (name_block rule) over the names that remain after "
                    "removing every name in T(q) and every name at cosine >= tau to a name in T(q); bytes before the header untouched; "
                    "unchanged items carry the committed text and the committed TRUE score",
            "built": dt.date.today().isoformat()}
    jdump({"meta": meta, "items": items}, L1 / "indexes_own.json")
    print(f"l1/indexes_own.json: 661 texts, {changed} changed, tau {tau:.6f}")

    # ---- NB-6 gate on the committed TRUE texts
    committed_texts = {it["item_id"]: idx[it["index_key"]] for it in sub}
    rows_true = nb6_rows(sub, committed_texts)
    emb_t, lex_t = nb6_scores(rows_true)
    gate = {"embedding": per_state(emb_t, rows_true), "lexical": per_state(lex_t, rows_true)}
    nb6c = J(RC.ROOT / "e1r_robustness/results/nb6.json")["rows"]["R-NOK-FRB|TRUE"]
    comm_emb, comm_lex = nb6c["nb6_embedding"], nb6c["nb6_lexical"]
    comp = J(RC.ROOT / "e1r_robustness/results/nb6_composition.json")["rows"]["R-NOK-FRB|TRUE"]
    comm_state = {"supersession": comp["nb6_emb_auroc_pn_superseded"], "expiry": comp["nb6_emb_auroc_pn_expired"], "retraction": comp["nb6_emb_auroc_pn_retracted"]}
    gate_ok = (round(gate["embedding"]["all"], 4) == round(comm_emb, 4) == 0.7484 and round(gate["lexical"]["all"], 4) == round(comm_lex, 4)
               and all(round(gate["embedding"][s], 4) == round(v, 4) for s, v in comm_state.items()))
    print(f"NB-6 gate: embedding {gate['embedding']['all']:.4f} (committed {comm_emb:.4f}); lexical {gate['lexical']['all']:.4f} (committed {comm_lex:.4f}); "
          f"per state {[round(gate['embedding'][s], 4) for s, _ in [('supersession', 0), ('expiry', 0), ('retraction', 0)]]} -> {'PASS' if gate_ok else 'FAIL -- STOP'}")
    if not gate_ok:
        sys.exit("NB-6 reproduction gate FAILED -- STOP (ADDENDUM_RESP section STOP)")

    # ---- NB-6 on V2-OWN
    own_texts = {k: v["text"] for k, v in items.items()}
    rows_own = nb6_rows(sub, own_texts)
    emb_o, lex_o = nb6_scores(rows_own)
    own = {"embedding": per_state(emb_o, rows_own), "lexical": per_state(lex_o, rows_own)}
    n_names_own = collections.Counter(len(r["sup"]) for r in rows_own)
    res = {"gate": {"reproduced": gate_ok, "computed": gate, "committed": {"embedding": comm_emb, "lexical": comm_lex, "per_state_embedding": comm_state}},
           "v2_own": own, "mean_names_per_item_true": float(np.mean([len(r["sup"]) for r in rows_true])),
           "mean_names_per_item_own": float(np.mean([len(r["sup"]) for r in rows_own])), "names_per_item_own": dict(n_names_own),
           "per_item": {r["item_id"]: {"emb_true": float(a), "lex_true": float(b), "emb_own": float(cc), "lex_own": float(d)}
                        for r, a, b, cc, d in zip(rows_true, emb_t, lex_t, emb_o, lex_o)}}
    jdump(res, L1 / "nb6_own.json")
    for v in ("embedding", "lexical"):
        print(f"NB-6 {v} on V2-OWN: all {own[v]['all']:.4f} (TRUE {gate[v]['all']:.4f}); "
              + "; ".join(f"{s} {own[v][s]:.4f} (TRUE {gate[v][s]:.4f})" for _, s in STATES))

    # ---- ledger
    today = dt.date.today().isoformat()
    T = lambda k: c[k]
    led = f"""
---

## 2. Step 2 — the V2-OWN indexes and NB-6 on them (written {today}; no model call)

### AUX-RESP-L1-LOCK — section renderer lock

Re-rendering the superseded-names section of every committed TRUE index of the 661 (242 keys) from
its parsed names through `name_block`'s rule (`index_v3._name_block`: sorted set, cap 15, wrap 150,
indents `"  "` / `"    "`, `(none)` when empty) reproduces the committed text byte for byte on
**242 of 242** keys, and the section is the tail of every text. Every V2-OWN text of
`l1/indexes_own.json` is the committed text up to the section header, byte-identical, followed by
the section re-rendered over the remaining names; `verify_resp.py` check E re-derives all 661.
Marker absent from every text; no emitted name contains `:`.

### AUX-RESP-L1-TAU — the neighbour threshold

Under NB-6's encoder (`sentence-transformers/all-MiniLM-L6-v2`, local), over the **35** distinct
real names of the 242 sections (underscores → spaces), the **577** pairs of distinct names sharing no
content token form the null: median {null['median']:.3f}, p90 {null['p90']:.3f}, p95 {null['p95']:.3f},
**p99 = τ = {tau:.6f}**, max {null['max']:.3f}. (The registration's §C.2 prose printed the median as
0.145; the recomputation of the same script gives {null['median']:.3f}; p90 / p95 / p99 / max agree to
three decimals and τ to six, so the null set is the same and the 0.145 is a transcription in the
prose. Disclosed, not repaired; no verdict reads the median.) {len(pairs)} distinct within-section
pairs; six at or above τ (workspace|workspace_location, placement_location|placement_status,
employer|job_title, activity|hobby, job_responsibility|job_title, current_neighborhood|current_residence).
Mean names per key: 1.785 counting `(none)` as one name (the committed parser's behaviour;
NB-6's 1.7474 per item likewise), 1.525 counting it as none.

### AUX-RESP-L1-CENSUS — the ablation census at τ (§C.2 reproduced at build)

| | items | changed under V2-OWN | of which section emptied to `(none)` |
|---|---:|---:|---:|
| all | 661 | **{T('changed')}** | {T('emptied')} |
| PRESENT-NEGATIVE | {T('pn')[0]} | **{T('pn')[1]}** | {T('sup')[2] + T('ret')[2] + T('exp')[2]} |
| — supersession-derived | {T('sup')[0]} | **{T('sup')[1]}** | {T('sup')[2]} |
| — retraction-derived | {T('ret')[0]} | **{T('ret')[1]}** | {T('ret')[2]} |
| — expiry-derived | {T('exp')[0]} | **{T('exp')[1]}** | {T('exp')[2]} |
| PRESENT | {T('present')[0]} | {T('present')[1]} | — |
| ABSENT (natural-absent changed: {T('absent_natural_changed')}) | {T('absent')[0]} | {T('absent')[1]} | — |
| by variant FULL / CAT-ABLATED / SLOT-ABLATED | {T('FULL')[0]} / {T('CAT-ABLATED')[0]} / {T('SLOT-ABLATED')[0]} | {T('FULL')[1]} / {T('CAT-ABLATED')[1]} / {T('SLOT-ABLATED')[1]} | — |
| items where a neighbour (not an own name) is removed | — | {T('neighbour_items')} | — |

|T(q)| over the 661: 0 for {T('T_sizes')[0]}, 1 for {T('T_sizes')[1]}, 2 for {T('T_sizes')[2]}, 3 for {T('T_sizes')[3]}, 4 for {T('T_sizes')[4]}, ≥ 5 for {T('T_sizes')[5]}.
**{T('unchanged')} items are byte-identical to their committed TRUE text** and carry the committed TRUE score
under V2-OWN; {T('keys_none')} keys / {T('items_none')} items print `(none)` under TRUE.

### AUX-RESP-L1-NB6-GATE — NB-6 reproduction on the committed TRUE texts

`run_nb6.emb_scores` / `lex_scores` on the committed TRUE texts of the 661 through
`index_features.parse`: embedding **{gate['embedding']['all']:.4f}** (committed {comm_emb:.4f}), lexical
**{gate['lexical']['all']:.4f}** (committed {comm_lex:.4f}); per state (embedding) supersession
{gate['embedding']['supersession']:.4f} / expiry {gate['embedding']['expiry']:.4f} / retraction {gate['embedding']['retraction']:.4f}
(committed {comm_state['supersession']:.4f} / {comm_state['expiry']:.4f} / {comm_state['retraction']:.4f}). **Gate PASS at four decimals.**

### AUX-RESP-L1-NB6 — NB-6 on the V2-OWN list (computed before any monitor call)

Per-state rows: positives of one state against the same 557 negatives (`nb6_composition.py`'s
construction). `(none)` scored as a name, as committed.

| NB-6 variant | population | TRUE (committed texts) | V2-OWN | difference |
|---|---|---:|---:|---:|
""" + "\n".join(
        f"| {v} | {s} | {gate[v][s]:.4f} | {own[v][s]:.4f} | {own[v][s] - gate[v][s]:+.4f} |"
        for v in ("embedding", "lexical") for s in ("all", "supersession", "expiry", "retraction")) + f"""

Mean names per item: TRUE {res['mean_names_per_item_true']:.4f}, V2-OWN {res['mean_names_per_item_own']:.4f}.
**Reading under the expectation stated in advance (§L1):** NB-6's supersession discrimination under
V2-OWN is {own['embedding']['supersession']:.4f} (embedding), against {gate['embedding']['supersession']:.4f} under TRUE — {"toward chance, as expected: its signal on those items was the name" if own['embedding']['supersession'] < 0.60 else "it survives the ablation; its remaining signal is the `(none)` string or the neighbours below τ, and the L1 scoring step says which"}.
The lexical variant prints beside it ({own['lexical']['supersession']:.4f} against {gate['lexical']['supersession']:.4f}); τ does not close the lexical
variant (registration §C.2). Artifact: `l1/nb6_own.json` (per-item scores under both texts).
"""
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(led)
    print("ledger appended: AUX-RESP-L1-LOCK, -L1-TAU, -L1-CENSUS, -L1-NB6-GATE, -L1-NB6")


if __name__ == "__main__":
    main()
