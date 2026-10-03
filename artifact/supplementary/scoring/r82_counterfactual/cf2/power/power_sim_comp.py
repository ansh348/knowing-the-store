"""CF2_SCOPE Phase 3 -- power simulation from the CF-1 committed rows only. NO API CALLS.

Usage, from the repository root:  python <path>/power_sim.py <MINI|H45|OP5> [3 5 7 10]

Outer loop: resample QUESTIONS (whole triples), never items, with replacement, stratified by
state (10*m pairs per state from that state's 10 CF-1 pairs), 1000 draws, default_rng(42),
one fresh stream per size. Inner: the committed item-level paired bootstrap
common_e1r.boot_item (1000 draws, default_rng(42), single-class draws discarded,
percentile 2.5/97.5), re-implemented as an exact histogram Mann-Whitney AUROC with ties at
0.5. The re-implementation must reproduce the committed CF-1 intervals for this lane
(NUMBERS_R82 sections 6 and 9) to 1e-9 before any simulation runs; a mismatch is a STOP.

Populations per outer draw:
  WHOLE              all 30m pairs (90m items): indexed minus blind, v2 and v3
  <STATE>            the 10m pairs of that state (30m items): indexed minus blind, v2 and v3
  SUP_minus_COUNTED  AUROC(supersession) minus AUROC(pooled retraction+expiry), v2 and v3;
                     two disjoint subsets, each item-resampled within itself
  COUNTED_paired     v3 minus v2, paired, on 10m retraction + 10m expiry pairs drawn from the
                     CF-1 pairs that INDIVIDUATE (6 retraction, 9 expiry), because a CF-2
                     build-time check admits only individuating pairs
Per key: share of outer draws with lo > 0 (directional) and with lo > 0 or hi < 0.
"""
import io, json, pathlib, sys, time
import numpy as np

ROOT = pathlib.Path.cwd()
assert (ROOT / "r82_counterfactual").exists(), "run from the repository root"
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools"):
    sys.path.insert(0, str(ROOT / p))
from common_e1r import boot_item          # noqa: E402  the committed estimator, for the gate
import score_cf as S                      # noqa: E402  load_lane: X4 draw collapse, unchanged

CODE = sys.argv[1]
COMPS = tuple(tuple(int(v) for v in x.split("/")) for x in sys.argv[2:]) or ((100, 100, 30), (100, 100, 60), (100, 60, 30))  # SUP/RET/EXP pairs per state
N_OUTER, N_INNER, SEED = 1000, 1000, 42
STATES = ("SUPERSESSION", "RETRACTION", "EXPIRY")

cell = json.load(io.open(ROOT / "r82_counterfactual/cf_cell.json", encoding="utf-8"))
items = cell["items"]; ind = cell["meta"]["individuation"]
pairs = sorted({it["pair_id"] for it in items}); P = len(pairs)
state_of = {it["pair_id"]: it["state"] for it in items}
qmap = {q: f"q{n:02d}" for n, q in enumerate(sorted({it["question"] for it in items}))}
VORD = {"PRESENT": 0, "ABSENT": 1, "PN": 2}
lane = S.load_lane(CODE)
Y = np.zeros((P, 3), int); B = np.zeros((P, 3)); V2 = np.zeros((P, 3)); V3 = np.zeros((P, 3))
for it in items:
    r = pairs.index(it["pair_id"]); c = VORD[it["version"]]
    Y[r, c] = it["y_nok"]; B[r, c] = lane[(qmap[it["question"]], "BLIND")]
    V2[r, c] = lane[(it["item_id"], "INDEXED-V2")]; V3[r, c] = lane[(it["item_id"], "INDEXED-V3")]


def auc_hist(Sidx, Yk, V):
    """Row-wise Mann-Whitney AUROC with ties at 0.5, from value-index histograms."""
    R, N = Sidx.shape; off = (np.arange(R) * V)[:, None]
    pos = np.bincount((Sidx + off)[Yk == 1], minlength=R * V).reshape(R, V).astype(float)
    neg = np.bincount((Sidx + off)[Yk == 0], minlength=R * V).reshape(R, V).astype(float)
    below = np.cumsum(neg, axis=1) - neg
    return (pos * (below + 0.5 * neg)).sum(1) / (pos.sum(1) * neg.sum(1))


def boot_item_ci(b, i, y, n=N_INNER, seed=SEED):
    """Exact re-implementation of common_e1r.boot_item -> (lo, hi)."""
    grid = np.unique(np.concatenate([b, i])); V = len(grid)
    bi = np.searchsorted(grid, b); ii = np.searchsorted(grid, i)
    rng = np.random.default_rng(seed); N = len(y)
    K = rng.integers(0, N, (n, N)); Yk = y[K]; keep = (Yk.sum(1) > 0) & (Yk.sum(1) < N)
    K = K[keep]; Yk = Yk[keep]
    d = auc_hist(ii[K], Yk, V) - auc_hist(bi[K], Yk, V)
    return float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


def boot_subset_diff_ci(sA, yA, sB, yB, n=N_INNER, seed=SEED):
    grid = np.unique(np.concatenate([sA, sB])); V = len(grid); rng = np.random.default_rng(seed)
    a = np.searchsorted(grid, sA); bb = np.searchsorted(grid, sB); NA, NB = len(yA), len(yB)
    KA = rng.integers(0, NA, (n, NA)); KB = rng.integers(0, NB, (n, NB)); YA = yA[KA]; YB = yB[KB]
    keep = (YA.sum(1) > 0) & (YA.sum(1) < NA) & (YB.sum(1) > 0) & (YB.sum(1) < NB)
    d = auc_hist(a[KA][keep], YA[keep], V) - auc_hist(bb[KB][keep], YB[keep], V)
    return float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


# ---- gate: reproduce the committed CF-1 intervals for this lane exactly, or stop
y0 = Y.reshape(-1); b0 = B.reshape(-1)
for tag, Mx in (("v2", V2), ("v3", V3)):
    ref = boot_item(b0, Mx.reshape(-1), y0); lo, hi = boot_item_ci(b0, Mx.reshape(-1), y0)
    assert abs(lo - ref["ci_lo"]) < 1e-9 and abs(hi - ref["ci_hi"]) < 1e-9, (CODE, tag, ref, lo, hi)
print(json.dumps({"lane": CODE, "gate": "committed CF-1 item intervals reproduced to 1e-9"}), flush=True)

idx_state = {s: np.array([k for k, p in enumerate(pairs) if state_of[p] == s]) for s in STATES}
idx_ind = {s: np.array([k for k, p in enumerate(pairs) if state_of[p] == s and ind[p]["individuates"]])
           for s in ("RETRACTION", "EXPIRY")}
flat = lambda Mx, sel: Mx[sel].reshape(-1)

for comp in COMPS:
    cnt = dict(zip(STATES, comp))
    tally = {}

    def hit(key, lo, hi):
        t = tally.setdefault(key, [0, 0, 0]); t[0] += 1; t[1] += (lo > 0); t[2] += (lo > 0 or hi < 0)

    rng = np.random.default_rng(SEED); t0 = time.time()
    for d in range(N_OUTER):
        sel = {s: rng.choice(idx_state[s], size=cnt[s], replace=True) for s in STATES}
        selc = {s: rng.choice(idx_ind[s], size=cnt[s], replace=True) for s in ("RETRACTION", "EXPIRY")}
        allsel = np.concatenate([sel[s] for s in STATES])
        csel = np.concatenate([selc[s] for s in ("RETRACTION", "EXPIRY")])
        cs = np.concatenate([sel["RETRACTION"], sel["EXPIRY"]])
        y = flat(Y, allsel); b = flat(B, allsel)
        for tag, Mx in (("v2", V2), ("v3", V3)):
            hit(("WHOLE", tag), *boot_item_ci(b, flat(Mx, allsel), y))
            for s in STATES:
                hit((s, tag), *boot_item_ci(flat(B, sel[s]), flat(Mx, sel[s]), flat(Y, sel[s])))
            hit(("SUP_minus_COUNTED", tag), *boot_subset_diff_ci(
                flat(Mx, sel["SUPERSESSION"]), flat(Y, sel["SUPERSESSION"]), flat(Mx, cs), flat(Y, cs)))
        hit(("COUNTED_paired", "v3-v2"), *boot_item_ci(flat(V2, csel), flat(V3, csel), flat(Y, csel)))
    out = {"lane": CODE, "composition": "/".join(map(str, comp)), "n_items": 3 * sum(comp), "positives_per_state": cnt,
           "outer_draws": N_OUTER, "inner_draws": N_INNER, "seed": SEED,
           "elapsed_s": round(time.time() - t0, 1),
           "results": {"|".join(k): {"share_lo_gt0": v[1] / v[0], "share_excl0": v[2] / v[0]}
                       for k, v in tally.items()}}
    print(json.dumps(out), flush=True)
