"""E1-R sub-step (c): BELIEVED-index NOK on the full 661-row FR-Bank population.

Reviewer B4 called this result CENTRAL and believed it missing. The INDEXED-BELIEVED arm
was elicited and committed for every scoreable item; the published scorer simply never
called row(..., judgment="nok") against it. This script does.

Retention is defined exactly as the committed scorer's H_BELIEVED FOK retention:
    retention = believed_delta / true_delta
"""
from __future__ import annotations

import numpy as np

from common_e1r import (OUT, assemble, auroc, boot_cluster, boot_item, ece, jdump,
                        load_e1, lopo)

PUB_FOK_RETENTION = 1.014  # published FR-Bank FOK believed-index retention, 101.4%


def score(items, blind, idx, judgment, label):
    b, i, y, g, ids = assemble(items, blind, idx, judgment=judgment)
    ab, ai = auroc(b, y), auroc(i, y)
    return {
        "row": label, "n": int(len(y)), "n_pos": int(y.sum()),
        "n_personas": int(len(set(g.tolist()))),
        "blind_auroc": float(ab), "indexed_auroc": float(ai),
        "delta": float(ai - ab),
        "ci_item": boot_item(b, i, y),
        "ci_cluster": boot_cluster(b, i, y, g),
        "lopo": {k: v for k, v in lopo(b, i, y, g).items() if k != "folds"},
        "blind_ece": float(ece(b, y)), "indexed_ece": float(ece(i, y)),
    }


def main():
    items, blind, idxT, idxB = load_e1()
    frb = [it for it in items if it["backend"] == "frbank"]

    # ---- coverage census, recorded as inventory
    cov = {"frbank_items": len(frb)}
    for nm, idx in (("TRUE", idxT), ("BELIEVED", idxB)):
        joined = sum(1 for it in frb
                     if it["question"] in blind and it["item_id"] in idx
                     and blind[it["question"]].get("nok") is not None
                     and idx[it["item_id"]].get("nok") is not None)
        cov[f"nok_joinable_{nm}"] = joined
    cov["full_coverage"] = (cov["nok_joinable_TRUE"] == cov["nok_joinable_BELIEVED"]
                            == cov["frbank_items"])

    nok_true = score(frb, blind, idxT, "nok", "NOK FR-Bank indexed-TRUE")
    nok_bel = score(frb, blind, idxB, "nok", "NOK FR-Bank indexed-BELIEVED")
    fok_true = score(frb, blind, idxT, "fok", "FOK FR-Bank indexed-TRUE")
    fok_bel = score(frb, blind, idxB, "fok", "FOK FR-Bank indexed-BELIEVED")

    def retention(t, b_):
        dt, db = t["delta"], b_["delta"]
        return (db / dt) if dt and dt > 0 else None

    nok_ret = retention(nok_true, nok_bel)
    fok_ret = retention(fok_true, fok_bel)

    # ---- frozen contingency branch selection
    ci = nok_bel["ci_item"]
    excludes_zero = ci["excludes_zero"]
    if not excludes_zero:
        branch = ("DELTA CI INCLUDES ZERO -- NOK is not demonstrated on believed indexes; "
                  "the oracle-index dependence B4 names is CONFIRMED and must be stated in "
                  "the limitations and the abstract.")
    elif nok_ret is not None and nok_ret >= 0.60:
        branch = ("RETENTION >= 60% AND CI EXCLUDES ZERO -- NOK survives the store's own "
                  "corrupted self-description.")
    else:
        branch = ("RETENTION < 60% BUT CI EXCLUDES ZERO -- NOK degrades materially under "
                  "believed metadata but remains positive; report the degradation as a "
                  "quantified limit on the practical claim.")

    out = {
        "coverage": cov,
        "NOK_TRUE": nok_true, "NOK_BELIEVED": nok_bel,
        "FOK_TRUE": fok_true, "FOK_BELIEVED": fok_bel,
        "nok_retention": nok_ret, "fok_retention": fok_ret,
        "fok_retention_published": PUB_FOK_RETENTION,
        "nok_holds_ge_60pct": bool(nok_ret is not None and nok_ret >= 0.60),
        "frozen_branch": branch,
        "spec": "e1r_robustness/SPEC_E1R.md @ 9ac91a2",
    }
    jdump(out, OUT / "believed_nok.json")

    print("=" * 96)
    print("E1-R (c)  BELIEVED-INDEX NOK  --  reviewer B4's CENTRAL missing result")
    print("=" * 96)
    print(f"coverage: FR-Bank items {cov['frbank_items']}, "
          f"NOK-joinable TRUE {cov['nok_joinable_TRUE']}, "
          f"BELIEVED {cov['nok_joinable_BELIEVED']}  -> "
          f"{'FULL COVERAGE' if cov['full_coverage'] else 'INCOMPLETE'}\n")
    hdr = f"{'row':34s} {'n':>4s} {'blind':>8s} {'indexed':>8s} {'delta':>8s} {'item CI':>21s}"
    print(hdr)
    print("-" * len(hdr))
    for r in (fok_true, fok_bel, nok_true, nok_bel):
        c = r["ci_item"]
        print(f"{r['row']:34s} {r['n']:4d} {r['blind_auroc']:8.4f} {r['indexed_auroc']:8.4f} "
              f"{r['delta']:+8.4f} [{c['ci_lo']:+.4f},{c['ci_hi']:+.4f}]")
    print()
    print(f"  FOK retention (believed/true): {fok_ret * 100:.1f}%   "
          f"(published {PUB_FOK_RETENTION * 100:.1f}%)")
    print(f"  NOK retention (believed/true): {nok_ret * 100:.1f}%   <-- NEW")
    print()
    c = nok_bel["ci_cluster"]
    print(f"  NOK BELIEVED persona-clustered CI: [{c['ci_lo']:+.4f},{c['ci_hi']:+.4f}] "
          f"excludes zero: {c['excludes_zero']}")
    L = nok_bel["lopo"]
    print(f"  NOK BELIEVED LOPO: range [{L['min_delta']:+.4f},{L['max_delta']:+.4f}], "
          f"sign changes {L['n_sign_changes']}")
    print()
    print("FROZEN BRANCH SELECTED:")
    print(" ", branch)
    print(f"\nwrote {OUT / 'believed_nok.json'}")


if __name__ == "__main__":
    main()