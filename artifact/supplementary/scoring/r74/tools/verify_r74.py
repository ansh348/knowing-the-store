"""verify_r74 -- two-direction, read-only check of NUMBERS_R74.md against the R74/R75
artifacts. Declared in the NUMBERS_R74 header at the R74-R freeze; written at R75-V
(the gap is recorded in the R75 report). Direction 1: every ledgered table value below
matches its artifact field at print precision. Direction 2: the artifact headline
values appear as printed strings in NUMBERS_R74.md. No value is recomputed from raw
rows; artifacts are read as committed.
"""
import json, pathlib, re, sys

R74 = pathlib.Path(__file__).resolve().parents[1]
TXT = (R74 / "NUMBERS_R74.md").read_text(encoding="utf-8")

fails = []
n_checks = 0

def close(a, b, tol=5e-5):
    return abs(float(a) - float(b)) <= tol

def chk(name, ledger_val, artifact_val, tol=5e-5):
    global n_checks
    n_checks += 1
    if not close(ledger_val, artifact_val, tol):
        fails.append(f"{name}: ledger {ledger_val} vs artifact {artifact_val}")

def instr(name, s):
    global n_checks
    n_checks += 1
    if s not in TXT:
        fails.append(f"{name}: string {s!r} not in NUMBERS_R74.md")

# ---- X1 ----
x1 = json.load(open(R74 / "x1" / "x1_results.json", encoding="utf-8"))
p = x1["probes"]
chk("X1 pooled auroc", 0.9662, round(p["hard-pooled"]["auroc"], 4))
chk("X1 pooled lo", 0.9510, round(p["hard-pooled"]["ci"][0], 4))
chk("X1 pooled hi", 0.9788, round(p["hard-pooled"]["ci"][1], 4))
chk("X1 frb auroc", 0.9199, round(p["hard-frbank"]["auroc"], 4))
chk("X1 frb lo", 0.8879, round(p["hard-frbank"]["ci"][0], 4))
chk("X1 frb hi", 0.9471, round(p["hard-frbank"]["ci"][1], 4))
chk("X1 identity frb", 0, p["hard-frbank"]["n_items_where_yfok_differs_from_ynok"])
chk("X1 identity pooled", 0, p["hard-pooled"]["n_items_where_yfok_differs_from_ynok"])
for s in ("0.9662", "[0.9510, 0.9788]", "0.9199", "[0.8879, 0.9471]"):
    instr("X1 rev", s)

# ---- X2 (ablation arms; intact rows are the committed E1 values, checked upstream) ----
x2 = json.load(open(R74 / "x2" / "x2_scores.json", encoding="utf-8"))
B = x2["backends"]
exp = {
    ("mem0", "X2a-count-removed"):        (0.4802, -0.0943, -0.1674, -0.0233),
    ("mem0", "X2c-markers-removed"):      (0.4796, -0.0949, -0.1654, -0.0250),
    ("mem0", "X2d-count-markers-removed"): (0.4664, -0.1082, -0.1769, -0.0392),
    ("amem", "X2a-count-removed"):        (0.4587, -0.1004, -0.1699, -0.0309),
    ("amem", "X2c-markers-removed"):      (0.4705, -0.0886, -0.1550, -0.0269),
    ("amem", "X2d-count-markers-removed"): (0.5223, -0.0368, -0.1041, +0.0268),
}
for (store, arm), (a, d, lo, hi) in exp.items():
    r = B[store][arm]
    chk(f"X2 {store} {arm} auroc", a, round(r["arm_auroc"], 4))
    chk(f"X2 {store} {arm} delta", d, round(r["delta"], 4), tol=2e-4)
    chk(f"X2 {store} {arm} lo", lo, round(r["boot"]["ci_lo"], 4))
    chk(f"X2 {store} {arm} hi", hi, round(r["boot"]["ci_hi"], 4))
chk("X2 AM-D clus lo", -0.0974, round(B["amem"]["X2d-count-markers-removed"]["clustered_ci"][0], 4))
chk("X2 AM-D clus hi", +0.0225, round(B["amem"]["X2d-count-markers-removed"]["clustered_ci"][1], 4))
chk("X2 branch", 1, int(x2["branch"] == "ii-multiple-partial"))

# ---- X3 ----
x3 = json.load(open(R74 / "x3" / "x3_billed.json", encoding="utf-8"))
chk("X3 blind $/1M", 233.391, round(x3["BLIND"]["usd_billed_per_1M_calls"], 3))
chk("X3 idx $/1M", 360.33056, x3["INDEXED"]["usd_billed_per_1M_calls"], tol=1e-4)
chk("X3 hit share", 0.643, round(x3["INDEXED"]["cache_hit_token_share"], 3))
chk("X3 confirmed", 0, int(x3["ordering_confirmed_indexed_lt_blind"]))
for s in ("$360.33", "$233.39", "64.3%"):
    instr("X3 rev", s)

# ---- X4 ----
x4 = json.load(open(R74 / "x4" / "x4_scores.json", encoding="utf-8"))
L = x4["lanes"]
exp4 = {
    ("gpt-4.1-mini", "nok_661"): (0.4946, 0.7339, 0.2393, 0.1801, 0.2949),
    ("gpt-4.1-mini", "fok_307"): (0.4966, 0.7003, 0.2037, 0.0935, 0.3191),
    ("gpt-5.6-luna", "nok_661"): (0.4495, 0.8182, 0.3687, 0.2932, 0.4358),
    ("gpt-5.6-luna", "fok_307"): (0.5720, 0.7605, 0.1885, 0.0439, 0.3352),
    ("claude-opus-5", "nok_661"): (0.6429, 0.8327, 0.1898, 0.1437, 0.2411),
    ("claude-opus-5", "fok_307"): (0.6793, 0.8099, 0.1306, 0.0557, 0.2148),
    ("claude-haiku-4-5-20251001", "nok_661"): (0.4150, 0.8210, 0.4060, 0.3283, 0.4791),
    ("claude-haiku-4-5-20251001", "fok_307"): (0.3781, 0.7465, 0.3684, 0.2629, 0.4755),
}
NUM = (R74.parent / "e1_metamemory" / "NUMBERS.md").read_text(encoding="utf-8")
for (lane, cell), (b, i, d, lo, hi) in exp4.items():
    r = L[lane][cell]
    chk(f"X4 {lane} {cell} blind", b, round(r["blind"], 4))
    chk(f"X4 {lane} {cell} indexed", i, round(r["indexed"], 4))
    chk(f"X4 {lane} {cell} delta", d, round(r["delta"], 4), tol=2e-4)
    if lane == "gpt-4.1-mini":
        # The mini rows CITE the committed canonical intervals (NUMBERS_R74 SX4:
        # "Mini rows cite the committed canonical intervals; the expansion scorer
        # re-derives mini's points exactly"); the scorer's own re-derived bootstrap
        # intervals differ in the third decimal by seed path and are not the cited
        # figures. Check the cited interval against the canonical upstream ledger.
        n_checks += 2
        canon = f"[+{lo:.4f}, +{hi:.4f}]"
        if canon not in NUM:
            fails.append(f"X4 {lane} {cell}: canonical interval {canon} not in NUMBERS.md")
        else:
            n_checks -= 1  # single membership check, counted once
    else:
        chk(f"X4 {lane} {cell} lo", lo, round(r["boot"]["ci_lo"], 4))
        chk(f"X4 {lane} {cell} hi", hi, round(r["boot"]["ci_hi"], 4))

# ---- X5 ----
x5 = json.load(open(R74 / "x5" / "x5_scores.json", encoding="utf-8"))
mini = x5["lanes"]["MINI"]["cells"]["nok"]
op5 = x5["lanes"]["OP5"]["cells"]["nok"]
chk("X5 mini blind", 0.4774, round(mini["blind_auroc"], 4))
chk("X5 mini blind lo", 0.2991, round(mini["blind_one_sample"]["ci_lo"], 4))
chk("X5 mini blind hi", 0.6623, round(mini["blind_one_sample"]["ci_hi"], 4))
chk("X5 mini indexed", 0.6771, round(mini["indexed_auroc"], 4))
chk("X5 mini delta", 0.2028, round(mini["paired_delta"]["mean"], 4), tol=2e-4)
chk("X5 mini lo", -0.1121, round(mini["paired_delta"]["ci_lo"], 4))
chk("X5 mini hi", 0.4984, round(mini["paired_delta"]["ci_hi"], 4))
chk("X5 op5 blind", 0.3993, round(op5["blind_auroc"], 4))
chk("X5 op5 blind lo", 0.2008, round(op5["blind_one_sample"]["ci_lo"], 4))
chk("X5 op5 blind hi", 0.6232, round(op5["blind_one_sample"]["ci_hi"], 4))
chk("X5 op5 indexed", 0.6962, round(op5["indexed_auroc"], 4))
chk("X5 op5 delta", 0.2978, round(op5["paired_delta"]["mean"], 4), tol=2e-4)
chk("X5 op5 lo", 0.0752, round(op5["paired_delta"]["ci_lo"], 4))
chk("X5 op5 hi", 0.5292, round(op5["paired_delta"]["ci_hi"], 4))
chk("X5 NS1 mini", 1, int(x5["lanes"]["MINI"]["NS1_blind_at_chance"]))
chk("X5 NS1 op5", 1, int(x5["lanes"]["OP5"]["NS1_blind_at_chance"]))
chk("X5 NS2 mini", 0, int(x5["lanes"]["MINI"]["NS2_delta_excludes_zero_positive"]))
chk("X5 NS2 op5", 1, int(x5["lanes"]["OP5"]["NS2_delta_excludes_zero_positive"]))
fm, fo = x5["lanes"]["MINI"]["cells"]["fok"], x5["lanes"]["OP5"]["cells"]["fok"]
chk("X5 mini fok blind", 0.5788, round(fm["blind_auroc"], 4))
chk("X5 mini fok indexed", 0.8867, round(fm["indexed_auroc"], 4))
chk("X5 op5 fok blind", 0.6675, round(fo["blind_auroc"], 4))
chk("X5 op5 fok indexed", 1.0000, round(fo["indexed_auroc"], 4))
chk("X5 oracle", 0.6042, round(x5["index_oracle_n36"]["auroc"], 4))
rend = json.load(open(R74 / "x5" / "x5_render.json", encoding="utf-8"))
chk("X5 transfer", 1.0, rend["spot_check"]["transfer_accuracy"])
chk("X5 cell n", 36, rend["cell"]["n"])
chk("X5 personas", 29, rend["cell"]["personas"])
for s in ("0.4774", "0.6771", "+0.2028", "[−0.1121, +0.4984]",
          "0.3993", "0.6962", "+0.2978", "[+0.0752, +0.5292]", "0.6042"):
    instr("X5 rev", s)

# ---- R76: NS-5 lane + the two $0 items (ADDENDUM_R76 §A3/§A4) ----
X6 = R74 / "x6"
ns5 = json.load(open(X6 / "x6_ns5_scores.json", encoding="utf-8"))
n5, f5 = ns5["cells"]["nok"], ns5["cells"]["fok"]
chk("NS5 blind", 0.4427, round(n5["blind_auroc"], 4))
chk("NS5 blind lo", 0.2582, round(n5["blind_one_sample"]["ci_lo"], 4))
chk("NS5 blind hi", 0.6522, round(n5["blind_one_sample"]["ci_hi"], 4))
chk("NS5 indexed", 0.6562, round(n5["indexed_auroc"], 4))
chk("NS5 delta", 0.2208, round(n5["paired_delta"]["mean"], 4), tol=2e-4)
chk("NS5 delta lo", -0.0522, round(n5["paired_delta"]["ci_lo"], 4))
chk("NS5 delta hi", 0.4809, round(n5["paired_delta"]["ci_hi"], 4))
chk("NS5 fok blind", 0.5419, round(f5["blind_auroc"], 4))
chk("NS5 fok indexed", 0.9901, round(f5["indexed_auroc"], 4))
chk("NS5 fok delta", 0.4470, round(f5["paired_delta"]["mean"], 4), tol=2e-4)
chk("NS5 fok lo", 0.2148, round(f5["paired_delta"]["ci_lo"], 4))
chk("NS5 fok hi", 0.6723, round(f5["paired_delta"]["ci_hi"], 4))
chk("NS5 n", 36, n5["n"])
chk("NS5 pos", 12, n5["pos"])
chk("NS5 includes chance", 1, int(ns5["NS5_blind_includes_chance"]))
chk("NS5 branch iii", 1, int(ns5["NS5_branch"] == "iii"))
# the branch rule is re-derived from the measured interval, not trusted from the file
n_checks += 1
_lo, _hi, _pt = (n5["blind_one_sample"]["ci_lo"], n5["blind_one_sample"]["ci_hi"],
                 n5["blind_auroc"])
if not (_lo <= 0.50 <= _hi and _pt < 0.45):
    fails.append("NS5 branch (iii) preconditions do not hold on the measured interval")
chk("NS5 parse fail blind", 0, ns5["parse_failures"]["BLIND"]["failed"])
chk("NS5 parse fail indexed", 0, ns5["parse_failures"]["INDEXED-TRUE"]["failed"])
chk("NS5 spend", 0.2959, ns5["spend_usd"], tol=5e-4)
for s in ("0.4427", "[0.2582, 0.6522]", "0.6562", "+0.2208", "[−0.0522, +0.4809]",
          "0.5419", "0.9901", "+0.4470", "branch (iii)", "0.0073"):
    instr("NS5 rev", s)

pr = json.load(open(X6 / "x6_probes.json", encoding="utf-8"))
AV, MP = pr["AV_CENSUS"], pr["MATCHED_PROBE"]
chk("AV auroc", 0.9736, round(AV["auroc_one_feature"], 4))
chk("AV n", 84, AV["n"])
chk("AV pn", 40, AV["pn"])
chk("AV single-class strata", 6, AV["n_single_class_strata"])
chk("AV strata", 8, AV["n_strata"])
chk("AV committed comparator", 0.7972, AV["committed_tfidf_same_cell"])
for st, (nn, pn) in {"AV3_stable_identity": (21, 0), "AV2_expired_logistics": (16, 8),
                     "AV1_superseded_preference": (14, 13),
                     "AV7_selective_forgetting": (13, 13), "NATURAL_ABSENT": (8, 0),
                     "AV4_multi_version_fact": (6, 6), "AV9_soft_supersession": (4, 0),
                     "AV6_cross_session_contradiction": (2, 0)}.items():
    chk(f"AV {st} n", nn, AV["strata"][st]["n"])
    chk(f"AV {st} pn", pn, AV["strata"][st]["pn"])
chk("MP auroc", 0.3472, round(MP["auroc"], 4))
chk("MP lo", 0.1673, round(MP["ci"][0], 4))
chk("MP hi", 0.5424, round(MP["ci"][1], 4))
chk("MP n", 36, MP["n"])
chk("MP pn", 12, MP["pn"])
chk("MP includes chance", 1, int(MP["includes_0.50"]))
chk("zero-shot cached ns rows", 0, pr["ZERO_SHOT_MATCHED"]["cached_rows_for_matched_cell"])
for s in ("0.9736", "0.3472", "[0.1673, 0.5424]", "SKIPPED (registered)"):
    instr("R76 probes rev", s)

# NS-3 / NS-4 were struck before computation: no key may exist for them
for forbidden in ("AUX-R76-NS3", "AUX-R76-NS4"):
    n_checks += 1
    if forbidden in TXT:
        fails.append(f"{forbidden} appears in NUMBERS_R74.md but was struck (ADDENDUM_R76 §A1)")


# ---- R77: wrong-index control + the presence-control posterior ----
X7 = R74 / "x7"
sw = json.load(open(X7 / "x7_scores.json", encoding="utf-8"))
exp7 = {("WRONG-PERSON", "fok"): (307, 35, 0.7003, 0.3631, 0.3383, 0.2169, 0.4506, True),
        ("WRONG-PERSON", "nok"): (661, 104, 0.7339, 0.4659, 0.2668, 0.2010, 0.3298, True),
        ("SHUFFLED", "fok"):     (307, 35, 0.7003, 0.7053, -0.0031, -0.0546, 0.0499, False),
        ("SHUFFLED", "nok"):     (661, 104, 0.7339, 0.7116, 0.0217, -0.0178, 0.0611, False)}
for (arm, j), (n, pos, ai, am, d, lo, hi, ex) in exp7.items():
    c = sw["cells"][arm][j]
    chk(f"SWAP {arm} {j} n", n, c["n"])
    chk(f"SWAP {arm} {j} pos", pos, c["pos"])
    chk(f"SWAP {arm} {j} intact", ai, round(c["intact_auroc"], 4))
    chk(f"SWAP {arm} {j} manip", am, round(c["manipulated_auroc"], 4))
    chk(f"SWAP {arm} {j} delta", d, round(c["delta_intact_minus_manipulated"], 4), tol=2e-4)
    chk(f"SWAP {arm} {j} lo", lo, round(c["ci"][0], 4))
    chk(f"SWAP {arm} {j} hi", hi, round(c["ci"][1], 4))
    chk(f"SWAP {arm} {j} excl0", int(ex), int(c["excludes_zero_positive"]))
chk("SW-1 holds", 1, int(sw["SW1_wrong_person"]))
chk("SW-2 fails", 0, int(sw["SW2_shuffled"]))
n_checks += 1
if sorted(sw["SW3_adverse_cells"]) != ["SHUFFLED/fok", "SHUFFLED/nok"]:
    fails.append(f"SW-3 adverse set drift: {sw['SW3_adverse_cells']}")
chk("SWAP parse fail WP", 0, sw["parse_failures"]["WRONG-PERSON"]["failed"])
chk("SWAP parse fail SH", 0, sw["parse_failures"]["SHUFFLED"]["failed"])
cell7 = json.load(open(X7 / "x7_cell.json", encoding="utf-8"))
chk("SWAP derangement fixed points", 0, cell7["derangement_fixed_points"])
chk("SWAP shuffle len delta max", 0, cell7["shuffle_len_delta"]["max"])
chk("SWAP shuffle len delta min", 0, cell7["shuffle_len_delta"]["min"])
for s in ("0.3631", "+0.3383", "0.4659", "+0.2668", "0.7053", "0.7116", "SW-2 FAILS"):
    instr("R77 SWAP rev", s)

# the posterior is deterministic arithmetic on the committed control record
tc = json.load(open(R74.parent / "e1_metamemory" / "two_channel_control.json", encoding="utf-8"))
_c, _r = tc["control"], tc["routing_counts"]
_A = sum(v for k, v in _r.items() if "|ABSENT|" in k)
_P = sum(v for k, v in _r.items() if "|PRESENT|" in k)
_TP = _P / _c["combined_recall"]
chk("posterior ABSENT verdicts", 21, _A)
chk("posterior PRESENT verdicts", 220, _P)
chk("posterior base rate", 0.917, round(_TP / (_A + _P), 3))
chk("posterior value", 0.052, round((_TP - _P) / _A, 3))
for s in ("**0.052**", "**0.917**"):
    instr("R77 posterior rev", s)

# ---- R78: paper_v2's tab:wrongindex prints the flipped (manipulated - intact)
# convention (R78 fix (b); A2 Option-3 pre-ruling; D-R74-20). The committed x7 checks
# above are unchanged -- ledger and artifact stay intact-minus-manipulated. This block
# checks the MANUSCRIPT convention only: negated deltas, negated-and-swapped CI
# endpoints, unchanged endpoint AUROCs, the estimator footnote, and the
# AUX-R78-SWAP-GAP bound re-derived from the committed artifact. No value is
# recomputed; the gap bound is deterministic arithmetic on committed fields
# (the D-R74-13 admissibility class).
V2 = R74.parent / "iclr2027_monitoring_submission" / "paper_v2.tex"
n_checks += 1
if not V2.exists():
    fails.append("R78: paper_v2.tex not found")
else:
    v2 = V2.read_text(encoding="utf-8")
    m = re.search(r"\\label\{tab:wrongindex\}.*?\\end\{table\}", v2, flags=re.S)
    n_checks += 1
    if not m:
        fails.append("R78: tab:wrongindex block not found in paper_v2.tex")
    else:
        body = m.group(0)
        def _f(s):
            return float(s.replace("\\mathbf", "").replace("{", "").replace("}", "").strip())
        ROW = re.compile(
            r"(Another persona's index|Own index, categories shuffled)\s*&\s*(FOK|NOK)\s*&\s*"
            r"\$(\d+)\$\s*&\s*\$([^$&]+)\$\s*&\s*\$([^$&]+)\$\s*&\s*\$([^$&]+)\$\s*&\s*"
            r"\$\[([^,\]]+),([^\]]+)\]\$")
        armmap = {"Another persona's index": "WRONG-PERSON",
                  "Own index, categories shuffled": "SHUFFLED"}
        seen = set()
        for r in ROW.finditer(body):
            arm, j = armmap[r.group(1)], r.group(2).lower()
            e = exp7[(arm, j)]  # (n, pos, intact, manip, d, lo, hi, ex)
            chk(f"R78 {arm} {j} n", e[0], int(r.group(3)))
            chk(f"R78 {arm} {j} intact endpoint", e[2], _f(r.group(4)))
            chk(f"R78 {arm} {j} manipulated endpoint", e[3], _f(r.group(5)))
            chk(f"R78 {arm} {j} delta = -(committed)", -e[4], _f(r.group(6)), tol=2e-4)
            chk(f"R78 {arm} {j} ci lo = -(committed hi)", -e[6], _f(r.group(7)))
            chk(f"R78 {arm} {j} ci hi = -(committed lo)", -e[5], _f(r.group(8)))
            seen.add((arm, j))
        n_checks += 1
        if len(seen) != 4:
            fails.append(f"R78: expected 4 tab:wrongindex rows, parsed {sorted(seen)}")
        n_checks += 1
        if "$+0.3383$" in body or "$+0.2668$" in body:
            fails.append("R78: un-flipped delta still printed in tab:wrongindex")
        n_checks += 1
        if "paired-bootstrap estimate of manipulated minus intact" not in body:
            fails.append("R78: estimator footnote absent from tab:wrongindex (A2 Option 3)")
        n_checks += 1
        if "$0.002$" not in body:
            fails.append("R78: the 0.002 Monte-Carlo bound is not printed in the footnote")
# AUX-R78-SWAP-GAP: the endpoint-vs-delta gap bound, re-derived from the committed artifact
_gap = max(abs(sw["cells"][a][j]["delta_intact_minus_manipulated"]
               - (sw["cells"][a][j]["intact_auroc"] - sw["cells"][a][j]["manipulated_auroc"]))
           for a in ("WRONG-PERSON", "SHUFFLED") for j in ("fok", "nok"))
n_checks += 1
if not _gap <= 0.002:
    fails.append(f"AUX-R78-SWAP-GAP: max endpoint-vs-delta gap {_gap:.6f} exceeds 0.002")
chk("AUX-R78-SWAP-GAP max gap", 0.0019, round(_gap, 4), tol=5e-5)
for s in ("AUX-R78-SWAP-GAP", "0.0019", "0.002"):
    instr("R78 gap rev", s)

print(f"checks: {n_checks}   failures: {len(fails)}")
for f in fails:
    print("  FAIL", f)
sys.exit(1 if fails else 0)
