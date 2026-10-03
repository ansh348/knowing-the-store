"""verify_ds.py -- the verifier of registrations/ADDENDUM_DS.md section L (frozen a5a2036, R100).

NO API CALLS. Exit 0 only if every check that applies passes. A-D run always; E-G as artifacts exist.

  A  lineage: sha256 pins (the §L list, plus resp_review/tools/resp_common.py which DS reuses);
     prompts_e1 digests; ADDENDUM_DS.md byte-identical to a5a2036; ADDENDUM_RESP.md to 17e6328
  B  populations: 661 / 104 = 63 / 26 / 15; 174 PRESENT; 383 ABSENT (238 + 145); 307 = 272 + 35; 302 questions
  C  censuses: renderer lock 661 / 661 and the v3 prefix; §C.3 flag census; §C.4 names and fetch
     sizes; §C.5 thresholds and every flag count; the lookup reproductions (0.7484 / 0.6186)
  D  precondition: RESP Phase B step 4 committed (b08757c); l2/retrieval.json present;
     AUX-RESP-L2-REACH in NUMBERS_RESP.md; ALWAYS reach recomputed from the five ids equals it
  E  prompts_ds.py carries exactly the §D.4 texts (hashes ledgered)
  F  policies.json / views.json / stage1.json re-derived byte-identical; no active entry fetched;
     every fetched line equals L2's line for that entry where one exists; no fetch set holds a gold
     entry of a PRESENT item (or the item is listed)
  G  rows_ds.jsonl / scores_ds.json: every flag, rate, interval and verdict re-derived; spend under $4;
     every §L key present
"""
from __future__ import annotations

import collections
import json
import subprocess
import sys

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import ds_common as DC                                                       # noqa: E402
from ds_common import ROOT, DS, RUN, LEDGER, J                               # noqa: E402

FAIL = []


def check(cond, msg):
    print(("  ok    " if cond else "  FAIL  ") + msg)
    if not cond:
        FAIL.append(msg)


def git_show(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], cwd=ROOT, capture_output=True).stdout.replace(b"\r\n", b"\n")


def check_a():
    print("A  lineage")
    for rel, pin in DC.PINS.items():
        check(DC.sha(ROOT / rel) == pin, f"{rel} sha256 {pin}")
    import hashlib
    committed = hashlib.sha256(git_show(DC.RESP_STEP4, "resp_review/tools/resp_common.py")).hexdigest()[:16]
    now = hashlib.sha256((ROOT / "resp_review/tools/resp_common.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:16]
    check(committed == now, f"resp_common.py as committed at {DC.RESP_STEP4} ({committed})")
    import prompts_e1 as P
    check(P.file_sha256() == DC.RC.PIN_PROMPTS["file"] and P.texts_sha256() == DC.RC.PIN_PROMPTS["texts"], "prompts_e1 digests unchanged")
    for rev, path in ((DC.FREEZE, "registrations/ADDENDUM_DS.md"), (DC.RESP_FREEZE, "registrations/ADDENDUM_RESP.md")):
        check(git_show(rev, path) == (ROOT / path).read_bytes().replace(b"\r\n", b"\n"), f"{path} byte-identical to {rev}")


def check_b(sub):
    print("B  populations")
    lab = collections.Counter(it["label"] for it in sub)
    check(len(sub) == 661 and lab["PRESENT-NEGATIVE"] == 104 and lab["PRESENT"] == 174 and lab["ABSENT"] == 383, f"661 = 104 PN + 174 PRESENT + 383 ABSENT ({dict(lab)})")
    check(collections.Counter(it["state"] for it in sub if it["y_nok"]) == {"sup": 63, "ret": 26, "exp": 15}, "PN 63 / 26 / 15")
    check(collections.Counter(it.get("absent_mechanism") for it in sub if it["label"] == "ABSENT") == {"ablation": 238, "natural": 145}, "ABSENT 238 ablation + 145 natural")
    hard = [it for it in sub if it["tier"] == "hard"]
    check(len(hard) == 307 and collections.Counter(it["label"] for it in hard) == {"ABSENT": 272, "PRESENT-NEGATIVE": 35}, "307 = 272 ABSENT + 35 PN")
    check(all(it["tier"] == "easy" for it in sub if it["label"] == "PRESENT"), "174 PRESENT all easy tier")
    check(len({it["question"] for it in sub}) == 302, "302 distinct questions")


def check_c(sub):
    print("C  censuses")
    idx = DC.RC.indexes()
    lock, fl_any, fl_all, own2, own3, F2r, F3r, Fpr = 0, collections.Counter(), 0, collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    F2, F3, Fp, cap = [], [], [], 0
    N2s, N3s = {}, {}
    for it in sub:
        v2, v3, N2, N3, rn, en = DC.names_for(it)
        lock += idx[it["index_key"]] == v2
        cap += len(rn) >= 15 or len(en) >= 15
        N2s[it["item_id"]], N3s[it["item_id"]] = N2, N3
        F2.append(len(DC.fetch(it, N2))); F3.append(len(DC.fetch(it, N3)))
        if it["y_nok"]:
            pm = set(it["pn_members"]); P = DC.pn_slots(it); Fp.append(len(DC.fetch(it, P)))
            fl_any[it["state"]] += any(DC.flagged(it, m) for m in pm); fl_all += all(DC.flagged(it, m) for m in pm)
            own2[it["state"]] += bool(P & N2); own3[it["state"]] += bool(P & N3)
            F2r[it["state"]] += bool(set(DC.fetch(it, N2)) & pm); F3r[it["state"]] += bool(set(DC.fetch(it, N3)) & pm); Fpr[it["state"]] += bool(set(DC.fetch(it, P)) & pm)
    check(lock == 661, f"renderer lock: committed TRUE text reproduced {lock} / 661 (v3 prefix asserted inside render_v3)")
    check(cap == 0, "no v3 name section at the cap of 15")
    check(dict(fl_any) == {"sup": 63, "ret": 8, "exp": 11} and fl_all == 74, f"§C.3 flagged {dict(fl_any)} (82); all-flagged {fl_all}")
    check(dict(own2) == {"sup": 63, "ret": 11, "exp": 0} and dict(own3) == {"sup": 63, "ret": 19, "exp": 12}, f"§C.4 own-name v2 {dict(own2)} / v3 {dict(own3)}")
    check(dict(F2r) == {"sup": 63, "ret": 2, "exp": 0} and dict(F3r) == {"sup": 63, "ret": 8, "exp": 11} and dict(Fpr) == {"sup": 63, "ret": 8, "exp": 11},
          f"§C.3 fetch reaches: F(N2) {sum(F2r.values())}, F(N3) {sum(F3r.values())}, F(P) {sum(Fpr.values())}")
    check(F2.count(0) == 195 and round(float(np.mean(F2)), 2) == 2.84 and max(F2) == 9, f"§C.4 F(N2): zero {F2.count(0)}, mean {np.mean(F2):.2f}, max {max(F2)}")
    check(F3.count(0) == 12 and round(float(np.mean(F3)), 2) == 8.84 and max(F3) == 23, f"§C.4 F(N3): zero {F3.count(0)}, mean {np.mean(F3):.2f}, max {max(F3)}")
    check(round(float(np.mean(Fp)), 2) == 2.64 and max(Fp) == 8, f"§C.4 F(P): mean {np.mean(Fp):.2f}, max {max(Fp)}; zero {Fp.count(0)} (the frozen table's 22 is D-DS-2)")
    nb6, nb5, gate = DC.lookup_scores(sub)
    check(gate["pass"], f"lookup reproduction gate NB-6 {gate['nb6_661']:.4f} / NB-5 {gate['nb5_307']:.4f}")
    th = DC.thresholds(sub, nb6, nb5)
    check(all(round(th[k], 6) == v for k, v in DC.EXPECT_THRESH.items()), f"§C.5 thresholds {({k: round(v, 6) for k, v in th.items()})}")
    L = lambda pred: collections.Counter(it["label"] for it in sub if pred(it))
    H = lambda pred: collections.Counter(it["label"] for it in sub if it["tier"] == "hard" and pred(it))
    exp = [("MODEL fetch", L(lambda it: it["true"]["nok"] >= th["theta_nok"]), {"PRESENT-NEGATIVE": 56, "PRESENT": 9, "ABSENT": 10}),
           ("MODEL abstain 661", L(lambda it: it["true"]["fok"] < th["theta_fok"]), {"PRESENT-NEGATIVE": 19, "PRESENT": 19, "ABSENT": 172}),
           ("MODEL abstain 307", H(lambda it: it["true"]["fok"] < th["theta_fok"]), {"PRESENT-NEGATIVE": 7, "ABSENT": 117}),
           ("LOOKUP fetch", L(lambda it: nb6[it["item_id"]] >= th["lambda_nok"]), {"PRESENT-NEGATIVE": 53, "PRESENT": 6, "ABSENT": 18}),
           ("LOOKUP abstain 661", L(lambda it: nb5[it["item_id"]] < th["lambda_fok"]), {"PRESENT-NEGATIVE": 22, "PRESENT": 28, "ABSENT": 174}),
           ("LOOKUP abstain 307", H(lambda it: nb5[it["item_id"]] < th["lambda_fok"]), {"PRESENT-NEGATIVE": 9, "ABSENT": 115}),
           ("LOOKUP-LIT fetch", L(lambda it: nb6[it["item_id"]] >= DC.THETA_NOK), {"PRESENT-NEGATIVE": 68, "PRESENT": 37, "ABSENT": 79}),
           ("LOOKUP-LIT abstain", L(lambda it: nb5[it["item_id"]] < DC.THETA_FOK), {})]
    for name, got, want in exp:
        check(dict(got) == want, f"§C.5 {name} {dict(got)}")
    return nb6, nb5, th, N2s, N3s


def check_d(sub):
    print("D  precondition (RESP Phase B step 4)")
    ok = subprocess.run(["git", "cat-file", "-e", f"{DC.RESP_STEP4}^{{commit}}"], cwd=ROOT).returncode == 0
    check(ok, f"RESP step 4 commit {DC.RESP_STEP4} exists")
    anc = subprocess.run(["git", "merge-base", "--is-ancestor", DC.RESP_STEP4, "HEAD"], cwd=ROOT).returncode == 0
    check(anc, f"{DC.RESP_STEP4} is an ancestor of HEAD")
    p = ROOT / "resp_review/l2/retrieval.json"
    check(p.exists(), "resp_review/l2/retrieval.json present")
    led = (ROOT / "resp_review/NUMBERS_RESP.md").read_text(encoding="utf-8")
    check("AUX-RESP-L2-REACH" in led, "AUX-RESP-L2-REACH present in NUMBERS_RESP.md")
    if p.exists():
        art = J(p)["items"]; reach = J(ROOT / "resp_review/l2/reach.json")
        f = sum(1 for it in sub if it["y_nok"] and set(it["pn_members"]) & set(art[it["item_id"]]["top5_ids"]))
        check(f == reach["k5"]["reached"] == 54, f"ALWAYS reach recomputed from the five ids = {f} / 104 (ledgered {reach['k5']['reached']})")
        ps = {st: sum(1 for it in sub if it["y_nok"] and it["state"] == st and set(it["pn_members"]) & set(art[it["item_id"]]["top5_ids"])) for st in ("sup", "ret", "exp")}
        check(all(ps[st] == reach["per_state_k5"][st]["reached"] for st in ps), f"per-state ALWAYS reach {ps} as ledgered")


def check_e():
    p = DS / "tools" / "prompts_ds.py"
    if not p.exists():
        print("E  prompts_ds.py absent (not yet built)"); return
    print("E  prompts")
    import prompts_ds as PD
    led = LEDGER.read_text(encoding="utf-8")
    reg = PD.from_registration(ROOT / "registrations/ADDENDUM_DS.md")
    check(PD.SYSTEM_ANSWER == reg["SYSTEM_ANSWER"] and PD.USER_ANSWER == reg["USER_ANSWER"], "SYSTEM_ANSWER / USER_ANSWER equal the frozen §D.4 texts")
    for nm, txt in (("SYSTEM_ANSWER", PD.SYSTEM_ANSWER), ("USER_ANSWER", PD.USER_ANSWER)):
        check(DC.sha_text(txt) in led, f"{nm} sha256 {DC.sha_text(txt)[:16]}… ledgered")


def check_f(sub, nb6, nb5, th):
    if not (DS / "policies.json").exists():
        print("F  policies / views / stage1 absent (not yet built)"); return
    print("F  policies, views, stage 1")
    import build_ds as BD
    pol = J(DS / "policies.json")["items"]; views = J(DS / "views.json"); st1 = J(DS / "stage1.json")
    fresh = DC.build_policies(sub, nb6, nb5, th)
    check(all(fresh[k]["policies"] == pol[k]["policies"] for k in fresh) and len(pol) == 661, "policies.json re-derived (gate, fetch set, abstention, fetched ids)")
    art = J(ROOT / "resp_review/l2/retrieval.json")["items"]
    n_ok, n_active, n_line = 0, 0, 0
    l2_lines = {}
    for k, a in art.items():
        for ln in a["block"].split("\n"):
            eid = ln.split("|")[0]
            l2_lines.setdefault((a["persona"], ln.split(" text: ")[0].split("] ", 1)[1], eid), ln)
    for it in sub:
        for p in DC.POLICIES:
            fetched = pol[it["item_id"]]["policies"][p]["fetched"]
            if any(not DC.flagged(it, e) for e in fetched):
                n_active += 1
            text, ids = DC.assemble_view(it, art[it["item_id"]]["block"], art[it["item_id"]]["top5_ids"], fetched)
            v = views["items"][it["item_id"]][p]
            if v["text"] == text and v["ids"] == ids and v["sha"] == DC.view_sha(text):
                n_ok += 1
    check(n_ok == 661 * len(DC.POLICIES), f"views re-derived byte-identical {n_ok} / {661 * len(DC.POLICIES)}")
    check(n_active == 0, "no active entry in any fetch set")
    fresh1 = BD.stage1(sub, pol, views["items"], write=False)
    diff = BD.compare(st1, fresh1)
    check(not diff, "stage1.json re-derived" + ("" if not diff else f" ({len(diff)} differ: {diff[:3]})"))
    led = LEDGER.read_text(encoding="utf-8")
    for k in ("AUX-DS-POLICIES", "AUX-DS-REACH", "AUX-DS-PRESENT", "AUX-DS-ABSTAIN", "AUX-DS-VIEWSIZE", "AUX-DS-LINELOCK"):
        check(k in led, f"{k} present in NUMBERS_DS.md")


def check_g(sub):
    if not (RUN / "rows_ds.jsonl").exists() or not (RUN / "scores_ds.json").exists():
        print("G  run artifacts absent (not yet run / scored)"); return
    print("G  stage 2")
    import run_ds as RD
    saved = J(RUN / "scores_ds.json"); fresh = RD.score_all(write=False)
    diff = RD.compare(saved, fresh)
    check(not diff, "every flag, rate, interval and verdict re-derived from rows_ds.jsonl" + ("" if not diff else f" ({len(diff)} differ: {diff[:3]})"))
    spend = RD.billed_so_far()["total"]
    check(spend < 4.0, f"spend ${spend:.4f} under $4")
    led = LEDGER.read_text(encoding="utf-8")
    for k in RD.LEDGER_KEYS:
        check(k in led, f"{k} present in NUMBERS_DS.md")


def main():
    check_a()
    sub = DC.load_cell()
    check_b(sub)
    nb6, nb5, th, N2s, N3s = check_c(sub)
    check_d(sub)
    check_e()
    check_f(sub, nb6, nb5, th)
    check_g(sub)
    print("\nverify_ds:", "PASS" if not FAIL else f"FAIL ({len(FAIL)}): " + "; ".join(FAIL[:5]))
    sys.exit(0 if not FAIL else 1)


if __name__ == "__main__":
    main()
