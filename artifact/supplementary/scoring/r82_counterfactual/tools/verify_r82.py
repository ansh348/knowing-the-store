"""verify_r82 -- two-direction, read-only check of NUMBERS_R82.md against the R82 artifacts.

Named in ADDENDUM_R82.md line 15 and in the ledger header since 4c3a516; written at R96
(2026-09-12), the gap recorded in reviews/CF2_SCOPE.md finding 2 and the CLAIMS.md R96 block
(entry 4b). Pattern: r74/tools/verify_r74.py (chk / instr idiom) and
e1r_robustness/tools/verify_e1r.py (Direction A re-derivation, TOL 5e-5).

Direction A: every ledgered value in sections 1 to 12 is read back from its committed artifact
at print precision (cf_pairs.json, adjudication.json, cf_questions.json, cf_pn_texts.json,
cf_cell.json, cf_indexes.json, probes.json, rows/rows_{MINI,H45,OP5}.jsonl,
results/cf_scores.json, results/cal_scores.json, results/cal_floor.json,
results/leakscreen_v3.json). Nothing is recomputed from monitor responses: sums over row
fields (call counts, OK counts, usd) and token counts over committed index strings are the
only arithmetic. Section 4's index token means are re-derived only if tiktoken is importable;
otherwise they are listed by name as UNCHECKED, never silently passed.

Direction B: the artifact values above must appear as printed strings in NUMBERS_R82.md, and
every value the manuscript's Table 9 and Appendix D.2 print must be a literal string in the
ledger (the manuscript path is optional; default paper_v6.tex, skipped if absent).

Exit 0 only when every check passes and nothing is unaccounted; UNCHECKED items are printed
and do not fail (they are named, which is the point).

Usage:  python r82_counterfactual/tools/verify_r82.py [--tex=iclr2027_monitoring_submission/paper_v6.tex]
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
R82 = ROOT / "r82_counterfactual"
LEDGER = R82 / "NUMBERS_R82.md"
TXT = LEDGER.read_text(encoding="utf-8")
TOL = 5e-5

fails, unchecked = [], []
n_checks = 0


def J(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def chk(name, ledger_val, artifact_val, tol=TOL):
    global n_checks
    n_checks += 1
    try:
        ok = abs(float(ledger_val) - float(artifact_val)) <= tol
    except (TypeError, ValueError):
        ok = ledger_val == artifact_val
    if not ok:
        fails.append(f"A {name}: ledger {ledger_val} vs artifact {artifact_val}")


def instr(name, s, text=None, where="NUMBERS_R82.md"):
    """Direction B: the printed string must occur literally."""
    global n_checks
    n_checks += 1
    if str(s) not in (TXT if text is None else text):
        fails.append(f"B {name}: string {s!r} not in {where}")


def both(name, printed, artifact_val, tol=TOL):
    """A and B at once: the ledger prints `printed`, and it rounds to the artifact."""
    chk(name, printed, artifact_val, tol)
    instr(name, str(printed))


# ---- section 1: construction -------------------------------------------------------------
pairs_doc = J(R82 / "cf_pairs.json"); pairs = pairs_doc["pairs"]
cell_doc = J(R82 / "cf_cell.json"); items = cell_doc["items"]
q_doc = J(R82 / "cf_questions.json"); questions = q_doc["questions"]
pn_doc = J(R82 / "cf_pn_texts.json"); pn_records = pn_doc["records"]
idx_doc = J(R82 / "cf_indexes.json")

chk("s1 pairs", 30, len(pairs))
chk("s1 distinct personas", 30, len({p["persona"] for p in pairs}))
for st in ("SUPERSESSION", "RETRACTION", "EXPIRY"):
    chk(f"s1 per state {st}", 10, sum(1 for p in pairs if p["state"] == st))
chk("s1 store versions", 90, len(items))
for lab in ("PRESENT", "ABSENT", "PN"):
    chk(f"s1 label {lab}", 30, sum(1 for it in items if it["version"] == lab))
chk("s1 questions", 30, len(questions))
chk("s1 questions distinct", 30, len({q["question"] for q in questions}))
chk("s1 intent gate passed by the selected paraphrase", 30,
    sum(1 for q in questions if any(t["ok"] and t["index"] == q["selected_index"] for t in q["intent_trail"])))
both("s1 substitutions", 2, q_doc["meta"]["substitutions"])
both("s1 redrafts", 0, q_doc["meta"]["redrafts"])
instr("s1 drafting prompt sha", q_doc["meta"]["prompt_sha256"])
instr("s1 questions sha", q_doc["meta"]["questions_sha256"])
chk("s1 PN records", 30, len(pn_records))
chk("s1 PN records with text (20) + expiry anchors (10)", 20,
    sum(1 for r in pn_records if r["state"] != "EXPIRY"))
chk("s1 expiry anchors", 10, sum(1 for r in pn_records if r["state"] == "EXPIRY"))
both("s1 PN retries", 0, pn_doc["meta"]["retries"])
chk("s1 PN records authored in one attempt (the 20 with text; expiry anchors carry no attempt)", 20,
    sum(1 for r in pn_records if r.get("attempts") == 1))
chk("s1 indexes: 90 versions", 90, len(idx_doc["indexes"]))
chk("s1 indexes: 2 arms", 2, len(idx_doc["meta"]["arms"]))
instr("s1 indexes sha (32-hex prefix as printed)", idx_doc["meta"]["sha256"][:32])
chk("s1 indexes sha matches cf_cell.json meta", idx_doc["meta"]["sha256"], cell_doc["meta"]["indexes_sha256"])
# retraction cosine to original: min / median / max and the count above 0.85, from the PN records
cos = [float(r["predicates"]["cosine_to_original"]) for r in pn_records
       if r["state"] == "RETRACTION" and "cosine_to_original" in r.get("predicates", {})]
if len(cos) == 10:
    cs = sorted(cos)
    both("s1 retraction cosine min", 0.551, round(cs[0], 3), tol=5e-4)
    # 4c3a516 ledgered the UPPER median, sorted[n//2] = 0.7747 -> 0.775; the mean-of-middle median is
    # 0.757. Checked under the convention it was written with; the other is printed, not failed.
    both("s1 retraction cosine median (upper median, sorted[n//2], the 4c3a516 convention)", 0.775, round(cs[len(cs) // 2], 3), tol=5e-4)
    print(f"  note: s1 retraction cosine median is the upper median; mean-of-middle median = {round((cs[4] + cs[5]) / 2, 3)} (not ledgered)")
    both("s1 retraction cosine max", 0.867, round(cs[-1], 3), tol=5e-4)
    chk("s1 retraction cosines above 0.85", 1, sum(1 for c in cos if c > 0.85))
else:
    unchecked.append(f"s1 retraction cosine statistics (found {len(cos)} cosine fields in cf_pn_texts.json records)")
sup_sig = [float(r["predicates"]["detector_signal_on_original"]) for r in pn_records
           if r["state"] == "SUPERSESSION" and "detector_signal_on_original" in r.get("predicates", {})]
if len(sup_sig) == 10:
    chk("s1 supersession detector 1.0 on all 10", 10, sum(1 for v in sup_sig if abs(v - 1.0) < 1e-9))
else:
    unchecked.append(f"s1 supersession detector signal (found {len(sup_sig)} fields)")

# ---- section 2: adjudication --------------------------------------------------------------
adj = J(R82 / "adjudication.json")
for st, (n_adj, n_el, rate) in {"EXPIRY": (46, 34, 0.7391), "RETRACTION": (62, 11, 0.1774),
                                 "SUPERSESSION": (13, 10, 0.7692)}.items():
    chk(f"s2 {st} adjudicated", n_adj, adj[st]["adjudicated"])
    chk(f"s2 {st} eligible", n_el, adj[st]["eligible"])
    both(f"s2 {st} rate", rate, round(adj[st]["eligibility_rate"], 4))
    chk(f"s2 {st} rate recomputed", rate, round(adj[st]["eligible"] / adj[st]["adjudicated"], 4))
chk("s2 expiry exhaustive over pool", True, bool(adj["EXPIRY"]["exhaustive"]))
chk("s2 expiry pool", 46, adj["EXPIRY"]["pool_size"])

# ---- section 3: individuation -------------------------------------------------------------
ind = cell_doc["meta"]["individuation"]
ret = [v for v in ind.values() if v["state"] == "RETRACTION"]
exp_ = [v for v in ind.values() if v["state"] == "EXPIRY"]
chk("s3 retraction individuates", 6, sum(1 for v in ret if v["individuates"]))
chk("s3 retraction collisions", 4, sum(1 for v in ret if not v["individuates"]))
chk("s3 expiry individuates", 9, sum(1 for v in exp_ if v["individuates"]))
chk("s3 expiry collisions", 1, sum(1 for v in exp_ if not v["individuates"]))
chk("s3 pooled scored", 15, cell_doc["meta"]["cf3_scored_n"])
chk("s3 meta retraction", 6, cell_doc["meta"]["cf3_retraction_individuating"])
chk("s3 meta expiry", 9, cell_doc["meta"]["cf3_expiry_individuating"])
for s in ("**6 of 10**", "**9 of 10**", "**15 of 20**"):
    instr("s3 printed", s)

# ---- section 4: index size -----------------------------------------------------------------
probes = J(R82 / "probes.json")
for lane, (b, v2, v3) in {"gpt-4.1-mini": (482, 1682, 1738), "claude-haiku-4-5-20251001": (527, 1777, 1840),
                          "claude-opus-5": (696, 2475, 2587)}.items():
    chk(f"s4 {lane} blind_in", b, probes[lane]["blind_in"])
    chk(f"s4 {lane} v2_in", v2, probes[lane]["v2_in"])
    chk(f"s4 {lane} v3_in", v3, probes[lane]["v3_in"])
    for s in (str(b), str(v2), str(v3)):
        instr(f"s4 {lane} printed {s}", s)
try:
    import tiktoken
    enc = tiktoken.get_encoding("o200k_base")
    for arm, (mean, med, lo, hi) in {"v2": (1074, 1082, 940, 1156), "v3": (1126, 1134, 987, 1228)}.items():
        n = sorted(len(enc.encode(v[arm])) for v in idx_doc["indexes"].values())
        chk(f"s4 {arm} mean tokens", mean, round(sum(n) / len(n)), tol=0.5)
        chk(f"s4 {arm} median tokens", med, round((n[44] + n[45]) / 2), tol=0.5)
        chk(f"s4 {arm} min tokens", lo, n[0]); chk(f"s4 {arm} max tokens", hi, n[-1])
    lines = [v["v2"].count("\n") + 1 for v in idx_doc["indexes"].values()]
    chk("s4 v2 mean lines", 63.2, round(sum(lines) / len(lines), 1), tol=0.05)
    chk("s4 v2 min lines", 58, min(lines)); chk("s4 v2 max lines", 67, max(lines))
except ImportError:
    unchecked.append("s4 index token means/medians/min/max under o200k_base (tiktoken not importable here)")
    lines = [v["v2"].count("\n") + 1 for v in idx_doc["indexes"].values()]
    chk("s4 v2 mean lines", 63.2, round(sum(lines) / len(lines), 1), tol=0.05)
    chk("s4 v2 min lines", 58, min(lines)); chk("s4 v2 max lines", 67, max(lines))

# ---- section 5: spend ----------------------------------------------------------------------
both("s5 drafting usd", 0.0060, round(q_doc["meta"]["usd"], 4))
both("s5 PN authoring usd", 0.0034, round(pn_doc["meta"]["usd"], 4))
chk("s5 drafting calls", 30, q_doc["meta"]["n"])


def lane(name):
    rows = [json.loads(l) for l in (R82 / "rows" / f"rows_{name}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    return len(rows), sum(1 for r in rows if r.get("status") == "OK"), round(sum(float(r["usd"]) for r in rows), 4)


for name, (calls, ok, usd) in {"MINI": (210, 210, 0.1325), "H45": (1050, 1050, 1.2641), "OP5": (1050, 1050, 8.6103)}.items():
    c, o, u = lane(name)
    chk(f"s5 {name} calls", calls, c); chk(f"s5 {name} OK", ok, o); both(f"s5 {name} usd", usd, u)
instr("s5 total as printed", "10.0189")
chk("s5 total", 10.0189, round(q_doc["meta"]["usd"] + pn_doc["meta"]["usd"] + 0.0025 + lane("MINI")[2] + lane("H45")[2] + lane("OP5")[2], 4))

# ---- sections 6, 7, 9, 10: the scored cell -------------------------------------------------
sc = J(R82 / "results" / "cf_scores.json")
L = sc["lanes"]
chk("s6 n", 90, sc["meta"]["n"]); chk("s6 pos", 30, sc["meta"]["pos"])
chk("s6 blind identity flag", True, bool(sc["meta"]["blind_is_half_by_construction"]))
LEDGER_LANES = {
    ("gpt-4.1-mini", "v2"): (0.5939, 0.0939, (-0.0345, 0.2315), (0.0325, 0.1625)),
    ("gpt-4.1-mini", "v3"): (0.6419, 0.1419, (0.0126, 0.2668), (0.0444, 0.2433)),
    ("claude-haiku-4-5-20251001", "v2"): (0.6406, 0.1406, (-0.0243, 0.2911), (0.0653, 0.2236)),
    ("claude-haiku-4-5-20251001", "v3"): (0.7656, 0.2656, (0.1267, 0.4178), (0.1800, 0.3536)),
    ("claude-opus-5", "v2"): (0.7122, 0.2122, (0.0683, 0.3567), (0.1286, 0.3039)),
    ("claude-opus-5", "v3"): (0.8172, 0.3172, (0.1695, 0.4658), (0.2372, 0.4022)),
}
for (ln, arm), (ind_, d, ici, qci) in LEDGER_LANES.items():
    a = L[ln][arm]
    chk(f"{ln} {arm} blind", 0.5, a["blind"])
    both(f"{ln} {arm} indexed", f"{ind_:.4f}", round(a["indexed"], 4))
    both(f"{ln} {arm} delta", f"{d:+.4f}", round(a["delta"], 4))
    chk(f"{ln} {arm} item ci lo", ici[0], round(a["item_ci"]["ci_lo"], 4))
    chk(f"{ln} {arm} item ci hi", ici[1], round(a["item_ci"]["ci_hi"], 4))
    chk(f"{ln} {arm} q ci lo", qci[0], round(a["question_clustered_ci"]["ci_lo"], 4))
    chk(f"{ln} {arm} q ci hi", qci[1], round(a["question_clustered_ci"]["ci_hi"], 4))
    instr(f"{ln} {arm} item ci printed", f"[{ici[0]:+.4f},{ici[1]:+.4f}]")
    instr(f"{ln} {arm} q ci printed", f"[{qci[0]:+.4f},{qci[1]:+.4f}]")
    chk(f"{ln} {arm} item ci excludes-zero flag", (ici[0] > 0) or (ici[1] < 0), bool(a["item_ci"]["excludes_zero"]))
PER_STATE = {  # (lane, arm): (supersession, retraction, expiry) as ledgered in sections 6, 9, 10
    ("gpt-4.1-mini", "v2"): (0.6550, 0.5700, 0.5825), ("gpt-4.1-mini", "v3"): (0.6950, 0.7500, 0.4800),
    ("claude-haiku-4-5-20251001", "v2"): (0.7825, 0.6225, 0.5225), ("claude-haiku-4-5-20251001", "v3"): (0.7450, 0.7375, 0.8575),
    ("claude-opus-5", "v2"): (0.8275, 0.5975, 0.6150), ("claude-opus-5", "v3"): (0.8350, 0.7300, 0.9450),
}
for (ln, arm), vals in PER_STATE.items():
    for st, v in zip(("SUPERSESSION", "RETRACTION", "EXPIRY"), vals):
        p = L[ln][arm]["per_state"][st]
        both(f"{ln} {arm} per-state {st}", f"{v:.4f}", round(p["indexed"], 4))
        chk(f"{ln} {arm} per-state {st} pos", 10, p["pos"]); chk(f"{ln} {arm} per-state {st} n", 30, p["n"])
# CF-3 counted population (section 7 Haiku; section 9 Opus; mini's pair is in reviews/NUMBERS_R87.md)
for ln, (v2, v3, d, ici, qci) in {"claude-haiku-4-5-20251001": (0.5656, 0.8489, 0.2833, (0.0772, 0.4945), (0.1509, 0.4311)),
                                   "claude-opus-5": (0.6122, 0.9144, 0.3022, None, (0.2166, 0.3678))}.items():
    c = L[ln]["cf3_counted"]
    chk(f"{ln} cf3 pairs", 15, c["pairs"]); chk(f"{ln} cf3 items", 45, c["n_items"]); chk(f"{ln} cf3 pos", 15, c["pos"])
    both(f"{ln} cf3 v2", f"{v2:.4f}", round(c["v2"], 4)); both(f"{ln} cf3 v3", f"{v3:.4f}", round(c["v3"], 4))
    both(f"{ln} cf3 delta", f"{d:+.4f}", round(c["delta_v3_minus_v2"], 4))
    if ici:
        chk(f"{ln} cf3 item lo", ici[0], round(c["item_ci"]["ci_lo"], 4)); chk(f"{ln} cf3 item hi", ici[1], round(c["item_ci"]["ci_hi"], 4))
        instr(f"{ln} cf3 item ci printed", f"[{ici[0]:+.4f},{ici[1]:+.4f}]")
    chk(f"{ln} cf3 q lo", qci[0], round(c["question_clustered_ci"]["ci_lo"], 4)); chk(f"{ln} cf3 q hi", qci[1], round(c["question_clustered_ci"]["ci_hi"], 4))
    instr(f"{ln} cf3 q ci printed", f"[{qci[0]:+.4f},{qci[1]:+.4f}]")

# ---- section 8: matchers -------------------------------------------------------------------
B = sc["baselines"]
for key, (a, lo, hi) in {"NB6-superseded-names-v2": (0.6261, 0.5567, 0.7094), "all-states-names-v3": (0.7886, 0.7013, 0.8797),
                         "NB5-whole-map-v2": (0.5347, 0.5108, 0.5670)}.items():
    both(f"s8 {key} auroc", f"{a:.4f}", round(B[key]["auroc"], 4))
    chk(f"s8 {key} ci lo", lo, round(B[key]["clustered_ci"]["ci_lo"], 4)); chk(f"s8 {key} ci hi", hi, round(B[key]["clustered_ci"]["ci_hi"], 4))
    instr(f"s8 {key} ci printed", f"[{lo:.4f},{hi:.4f}]")
chk("s8 tolerance", 0.05, sc["meta"]["tol"])
# the adverse-branch margins print as the differences of ledgered values
allst = B["all-states-names-v3"]["auroc"]; sup = B["NB6-superseded-names-v2"]["auroc"]
for name, printed, val in (("all-states minus mini v2", "+0.1947", allst - L["gpt-4.1-mini"]["v2"]["indexed"]),
                           ("all-states minus mini v3", "+0.1467", allst - L["gpt-4.1-mini"]["v3"]["indexed"]),
                           ("all-states minus haiku v2", "+0.1480", allst - L["claude-haiku-4-5-20251001"]["v2"]["indexed"]),
                           ("all-states minus haiku v3", "+0.0230", allst - L["claude-haiku-4-5-20251001"]["v3"]["indexed"]),
                           ("superseded minus mini v2", "+0.0322", sup - L["gpt-4.1-mini"]["v2"]["indexed"])):
    both(f"s8 margin {name}", printed, round(val, 4), tol=1.5e-4)

# ---- section 11: calibration --------------------------------------------------------------
cal_flat = J(R82 / "results" / "cal_scores.json"); floor = J(R82 / "results" / "cal_floor.json")
cal = {}   # keys are "POPULATION/arm"; regroup as cal[population][arm]
for k, v in cal_flat.items():
    pop, arm = k.split("/", 1)
    cal.setdefault(pop, {})[arm] = v
P = cal["P-FOK-HARD"]
chk("s11 n", 588, P["intact"]["raw"]["n"]); chk("s11 pos", 35, P["intact"]["raw"]["pos"])
both("s11 base rate", "0.0595", round(P["intact"]["raw"]["base_rate"], 4))
for arm, (auroc, dv, ece, platt, iso, temp) in {"blind": (0.5258, 6, 0.1596, 0.0001, 0.0003, 0.1222),
                                                 "intact": (0.7530, 12, 0.1741, 0.0029, 0.0146, 0.1299),
                                                 "names-only": (0.8516, 9, 0.0583, 0.0134, 0.0340, 0.0296)}.items():
    both(f"s11 {arm} raw auroc", f"{auroc:.4f}", round(P[arm]["raw"]["auroc"], 4))
    chk(f"s11 {arm} distinct values", dv, P[arm]["raw"]["distinct_values"])
    both(f"s11 {arm} raw ece", f"{ece:.4f}", round(P[arm]["raw"]["ece"], 4))
    both(f"s11 {arm} platt ece", f"{platt:.4f}", round(P[arm]["maps"]["platt"]["ece"], 4))
    both(f"s11 {arm} isotonic ece", f"{iso:.4f}", round(P[arm]["maps"]["isotonic"]["ece"], 4))
    both(f"s11 {arm} temperature ece", f"{temp:.4f}", round(P[arm]["maps"]["temperature"]["ece"], 4))
both("s11 intact AURC raw", "0.0615", round(P["intact"]["raw"]["aurc"], 4))
both("s11 intact AURC platt", "0.0373", round(P["intact"]["maps"]["platt"]["aurc"], 4))
both("s11 intact AURC isotonic", "0.0454", round(P["intact"]["maps"]["isotonic"]["aurc"], 4))
both("s11 intact excess AURC raw", "0.0538", round(P["intact"]["raw"]["excess_aurc"], 4))
both("s11 intact excess AURC platt", "0.0355", round(P["intact"]["maps"]["platt"]["excess_aurc"], 4))
N_ = cal["P-NOK-FRB"]
chk("s11 NOK n", 661, N_["indexed-BELIEVED"]["raw"]["n"]); chk("s11 NOK pos", 104, N_["indexed-BELIEVED"]["raw"]["pos"])
both("s11 NOK base rate", "0.1573", round(N_["indexed-BELIEVED"]["raw"]["base_rate"], 4))
both("s11 NOK believed raw ece", "0.1411", round(N_["indexed-BELIEVED"]["raw"]["ece"], 4))
both("s11 NOK believed isotonic ece", "0.0261", round(N_["indexed-BELIEVED"]["maps"]["isotonic"]["ece"], 4))
both("s11 floor brier (by key name)", "0.0560", round(floor["P-FOK-HARD"]["brier"], 4))
both("s11 intact platt brier", "0.0519", round(P["intact"]["maps"]["platt"]["brier"], 4))
both("s11 pooled oof auroc, blind NOK platt", "0.2572", round(N_["blind"]["maps"]["platt"]["auroc_pooled_oof"], 4))
both("s11 max calibrated p intact isotonic", "0.375", round(P["intact"]["maps"]["isotonic"]["max_calibrated_p"], 3))
both("s11 max calibrated p names-only isotonic", "0.450", round(P["names-only"]["maps"]["isotonic"]["max_calibrated_p"], 3))
chk("s11 crossing 0.5 undefined intact", None, P["intact"]["maps"]["isotonic"]["crossing_0.5"])
chk("s11 crossing 0.5 undefined names-only", None, P["names-only"]["maps"]["isotonic"]["crossing_0.5"])
chk("s11 crossing at base rate intact", 0.3, P["intact"]["maps"]["isotonic"]["crossing_base_rate"])
chk("s11 crossing at base rate names-only", 0.2, P["names-only"]["maps"]["isotonic"]["crossing_base_rate"])
chk("s11 folds", 40, P["intact"]["maps"]["isotonic"]["folds_increasing"] + P["intact"]["maps"]["isotonic"]["folds_decreasing"])

# ---- section 12: leakage screen, deterministic half ------------------------------------------
ls = J(R82 / "results" / "leakscreen_v3.json")
chk("s12 no model call", False, bool(ls["model_mediated_screen_ran"]))
chk("s12 threshold", 3, ls["threshold"]); chk("s12 seed", 42, ls["seed"]); chk("s12 n", 30, ls["n"])
chk("s12 registered cell", "PRESENT:v3", ls["registered_cell"])
chk("s12 indexes content sha = cf_indexes meta", idx_doc["meta"]["sha256"], ls["indexes_meta_sha256"])
instr("s12 content sha prefix printed", ls["indexes_meta_sha256"][:16])
instr("s12 file sha prefix printed", ls["indexes_file_sha256"][:16])
for key, (nc, share) in {"PRESENT:v3": (1, 26), "PRESENT:v2": (1, 26), "ABSENT:v3": (1, 23), "ABSENT:v2": (1, 23),
                         "PN:v3": (1, 27), "PN:v2": (1, 26)}.items():
    c = ls["cells"][key]
    chk(f"s12 {key} n", 30, c["n"]); chk(f"s12 {key} correct", nc, c["n_correct"])
    chk(f"s12 {key} sharing any", share, c["n_items_sharing_any_token"]); chk(f"s12 {key} verdict", "PASS", c["verdict"])
    chk(f"s12 {key} max coverage", 0.5, c["max_coverage"])
    instr(f"s12 {key} row printed", f"| {key.split(':')[1]} | {c['n']} | ")
hits = {key: [r["pair_id"] for r in c["rows"] if r["correct"]] for key, c in ls["cells"].items()}
chk("s12 the one hit is the same item in all six cells", True, all(h == ["cf:kenji:project:case_studies"] for h in hits.values()))
instr("s12 hit named", "cf:kenji:project:case_studies")
chk("s12 v3 adds no hit", True, all(ls["cells"][f"{v}:v3"]["n_correct"] == ls["cells"][f"{v}:v2"]["n_correct"] for v in ("PRESENT", "ABSENT", "PN")))

# ---- Direction B, manuscript side: Table 9 / Appendix D.2 print only ledgered strings ------------
tex_arg = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--tex=")), "iclr2027_monitoring_submission/paper_v6.tex")
tex_path = ROOT / tex_arg
if tex_path.exists():
    tex = tex_path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    i0 = tex.find("\\subsection{Store-counterfactual cell}")
    i1 = tex.find("\\section{Monitoring-scoped instrument ledger}")
    d2 = tex[i0:i1] if (i0 >= 0 and i1 > i0) else ""
    if not d2:
        unchecked.append(f"manuscript D.2 region not found in {tex_arg}")
    else:
        body = "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in d2.split("\n"))
        nums = sorted(set(re.findall(r"(?<![\w.])[+-]?\d\.\d{3,4}(?![\w.])", body)))
        # GPT-4.1 mini's n=45 counted pair (0.5578, 0.6600) is ledgered in reviews/NUMBERS_R87.md (D-R87-1),
        # which trace_scan_v13 lists in the same ledger family; it is read here for the same reason.
        family = TXT + (ROOT / "reviews" / "NUMBERS_R87.md").read_text(encoding="utf-8", errors="replace")
        ledger_nums = set(re.findall(r"[+-]?\d\.\d{3,4}", family))
        for t in nums:
            n_checks += 1
            if t not in ledger_nums and t.lstrip("+") not in ledger_nums and t not in ("0.5000", "0.5"):
                fails.append(f"B manuscript D.2 prints {t}, which is not a string in NUMBERS_R82.md")
        for s in ("$0.8350$", "$0.7300$"):
            instr(f"Table 9 filled cell {s}", s, text=body, where=tex_arg)
        n_checks += 1
        if "never scored" in body:
            fails.append("B manuscript D.2 still says a dash marks a cell never scored (R96-4d)")
else:
    unchecked.append(f"manuscript {tex_arg} absent; manuscript-side Direction B skipped")

# ---- report --------------------------------------------------------------------------------
print(f"verify_r82: {n_checks} checks, {len(fails)} failures, {len(unchecked)} unchecked")
for f in fails:
    print("  FAIL", f)
for u in unchecked:
    print("  UNCHECKED", u)
print("verify_r82: " + ("PASS" if not fails else "FAIL"))
sys.exit(1 if fails else 0)
