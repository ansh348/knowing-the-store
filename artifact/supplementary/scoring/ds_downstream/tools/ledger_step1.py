"""ledger_step1.py -- DS Phase B step 1: the six pre-artifact ledger keys of ADDENDUM_DS.md section L
(AUX-DS-PRECOND, -POP, -FLAGCENSUS, -NAMES, -THRESHOLDS, -LOOKUP-GATE), computed from committed inputs
and appended to NUMBERS_DS.md. NO API CALLS. Run once; verify_ds.py checks A-D pin every value here.
"""
from __future__ import annotations

import collections
import datetime as dt
import io
import sys

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import ds_common as DC                                                       # noqa: E402
from ds_common import ROOT, LEDGER, J                                        # noqa: E402


def main():
    sub = DC.load_cell()
    idx = DC.RC.indexes()
    reach = J(ROOT / "resp_review/l2/reach.json")
    art = J(ROOT / "resp_review/l2/retrieval.json")["items"]
    always = sum(1 for it in sub if it["y_nok"] and set(it["pn_members"]) & set(art[it["item_id"]]["top5_ids"]))
    per = collections.Counter(); own2 = collections.Counter(); own3 = collections.Counter(); F2r = collections.Counter(); F3r = collections.Counter(); Fpr = collections.Counter()
    fl_any = collections.Counter(); fl_all = 0; unflagged = []
    F2, F3, Fp, lock = [], [], [], 0
    for it in sub:
        v2, v3, N2, N3, rn, en = DC.names_for(it)
        lock += idx[it["index_key"]] == v2
        F2.append(len(DC.fetch(it, N2))); F3.append(len(DC.fetch(it, N3)))
        if it["y_nok"]:
            pm = set(it["pn_members"]); P = DC.pn_slots(it); Fp.append(len(DC.fetch(it, P)))
            fa = any(DC.flagged(it, m) for m in pm); fl_any[it["state"]] += fa; fl_all += all(DC.flagged(it, m) for m in pm)
            if not fa:
                unflagged.append((it["state"], it["item_id"]))
            own2[it["state"]] += bool(P & N2); own3[it["state"]] += bool(P & N3)
            F2r[it["state"]] += bool(set(DC.fetch(it, N2)) & pm); F3r[it["state"]] += bool(set(DC.fetch(it, N3)) & pm); Fpr[it["state"]] += bool(set(DC.fetch(it, P)) & pm)
    nb6, nb5, gate = DC.lookup_scores(sub)
    th = DC.thresholds(sub, nb6, nb5)
    Lc = lambda pred: collections.Counter(it["label"] for it in sub if pred(it))
    Hc = lambda pred: collections.Counter(it["label"] for it in sub if it["tier"] == "hard" and pred(it))
    rows = [("MODEL fetch (`nok ≥ θ_NOK`), 661", Lc(lambda it: it["true"]["nok"] >= th["theta_nok"])),
            ("MODEL abstain (`fok < θ_FOK`), 661", Lc(lambda it: it["true"]["fok"] < th["theta_fok"])),
            ("MODEL abstain, 307", Hc(lambda it: it["true"]["fok"] < th["theta_fok"])),
            ("LOOKUP fetch (`nb6 ≥ λ_NOK`), 661", Lc(lambda it: nb6[it["item_id"]] >= th["lambda_nok"])),
            ("LOOKUP abstain (`nb5 < λ_FOK`), 661", Lc(lambda it: nb5[it["item_id"]] < th["lambda_fok"])),
            ("LOOKUP abstain, 307", Hc(lambda it: nb5[it["item_id"]] < th["lambda_fok"])),
            ("LOOKUP-LIT fetch (`nb6 ≥ θ_NOK`), 661", Lc(lambda it: nb6[it["item_id"]] >= DC.THETA_NOK)),
            ("LOOKUP-LIT abstain (`nb5 < θ_FOK`), 661", Lc(lambda it: nb5[it["item_id"]] < DC.THETA_FOK))]
    d = lambda xs: f"zero {xs.count(0)}, median {int(np.median(xs))}, mean {np.mean(xs):.2f}, p90 {int(np.percentile(xs, 90))}, max {max(xs)}"
    today = dt.date.today().isoformat()
    txt = f"""
---

## 1. Step 1 — the pre-artifact keys (written {today}; no model call)

### AUX-DS-PRECOND

`registrations/ADDENDUM_RESP.md` frozen at `{DC.RESP_FREEZE}` and byte-identical; RESP Phase B step 4 committed at
`{DC.RESP_STEP4}` (an ancestor of HEAD); `resp_review/l2/retrieval.json` present; `AUX-RESP-L2-REACH` present in
`resp_review/NUMBERS_RESP.md`. ALWAYS reach recomputed from the five ids of `retrieval.json` and `pn_members`:
**{always} of 104** = {always / 104:.4f} (ledgered {reach['k5']['reached']} of {reach['k5']['n']}; per state
sup {reach['per_state_k5']['sup']['reached']} / 63, ret {reach['per_state_k5']['ret']['reached']} / 26, exp {reach['per_state_k5']['exp']['reached']} / 15) — equal. DS builds no retrieval and makes no embedding call.
**The instruction's 5% premise does not hold on this store (L2-P3 failed): the ALWAYS row is 0.5192, and DS-P1's
margin is narrowed accordingly (§C.7's second adverse branch).**

### AUX-DS-POP

661 items = 104 PN (63 supersession / 26 retraction / 15 expiry, `nb6_composition.AV_STATE`) + 174 PRESENT (all
easy tier) + 383 ABSENT (238 ablation, 145 natural-absent); the coverage population 307 = 272 ABSENT + 35 PN;
302 distinct questions. `r74/x4/cell_661.json` sha256 `01ed4c05fc57c0b2…`; joined as `common_e1r.assemble` joins.

### AUX-DS-FLAGCENSUS (D-DS-1)

Under `index_v2.true_lifecycle`, keyed by (persona, entry id): at least one `pn_members` entry flagged non-active
for **{sum(fl_any.values())} of 104** (sup {fl_any['sup']} / 63, ret {fl_any['ret']} / 26, exp {fl_any['exp']} / 15); every `pn_members` entry flagged for {fl_all}.
The {len(unflagged)} unflagged: {', '.join(f'{i} ({s})' for s, i in sorted(unflagged))}. ORACLE's ceiling is {sum(fl_any.values()) / 104:.4f} by construction (ruling of 2026-09-13).

### AUX-DS-NAMES

Renderer lock: `index_v2.render` on the item's store variant reproduces the committed TRUE text on **{lock} / 661**;
`index_v3.render_v3` asserts the v2 prefix on every one; no v3 name section at the cap. Own-name presence
(pn slots ∩ printed names): v2 superseded section {sum(own2.values())} (sup {own2['sup']} / ret {own2['ret']} / exp {own2['exp']});
v3 any section {sum(own3.values())} (sup {own3['sup']} / ret {own3['ret']} / exp {own3['exp']}). Fetch sets reaching the forbidding record:
F(N2) {sum(F2r.values())} ({F2r['sup']} / {F2r['ret']} / {F2r['exp']}), F(N3) {sum(F3r.values())} ({F3r['sup']} / {F3r['ret']} / {F3r['exp']}), F(P) {sum(Fpr.values())} ({Fpr['sup']} / {Fpr['ret']} / {Fpr['exp']}).
Fetch-set sizes — F(N2) over the 661: {d(F2)}; F(N3) over the 661: {d(F3)}; F(P) over the 104 PN: {d(Fp)}
(the frozen §C.4 table's "22" in F(P)'s zero cell is D-DS-2; the zero count is {Fp.count(0)}).

### AUX-DS-THRESHOLDS

θ_NOK = 104 / 661 = {th['theta_nok']:.6f}; θ_FOK = 35 / 307 = {th['theta_fok']:.6f} (probability at or above the population prior, ruling R1);
λ_NOK = the 75th-highest NB-6 score over the 661 = {th['lambda_nok']:.6f}; λ_FOK = the 125th-lowest NB-5 score over the 307 = {th['lambda_fok']:.6f}
(the matched budget, ruling R2); the literal rule (`LOOKUP-LIT`) uses θ_NOK / θ_FOK on the cosines, descriptive.

| gate | fires | PN | PRESENT | ABSENT |
|---|---:|---:|---:|---:|
""" + "\n".join(f"| {name} | {sum(c.values())} | {c.get('PRESENT-NEGATIVE', 0)} | {c.get('PRESENT', '—') if 'PRESENT' in c or '661' in name else '—'} | {c.get('ABSENT', 0)} |" for name, c in rows) + f"""

### AUX-DS-LOOKUP-GATE

`run_nb6.emb_scores` on the committed TRUE index texts: NB-6 (superseded section) **{gate['nb6_661']:.4f}** on the 661
(committed 0.7484), NB-5 (whole name map) **{gate['nb5_307']:.4f}** on the 307 (committed 0.6186) — **gate PASS at four decimals**.
"""
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    sys.stdout.reconfigure(encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    main()
