# -*- coding: utf-8 -*-
"""r125_t45_report.py -- Tasks 4 and 5: the tables and the ledger blocks 15d / 15e of r82_counterfactual/cf2/NUMBERS_CF2.md, from
reviews/r125/results/r125_t4_sibling.json, r125_t5_nc.json and the run records under cf2/rows (lock_r125, leak_r125, probes_r125,
projection_r125, batch_r125_*). No computation beyond formatting and the metered spend sum. NO MODEL CALL.
Writes reviews/r125/T4_T5_TABLES.md and the two ledger blocks (between markers; idempotent).
"""
from __future__ import annotations

import io
import json
import re
import subprocess
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r125_common as C  # noqa: E402
from r125_common import STATES  # noqa: E402

ROWS = C.CF2 / "rows"
OUT = C.R125 / "T4_T5_TABLES.md"
B4, E4 = "<!-- R125-T4 BEGIN (written by reviews/r125/tools/r125_t45_report.py; do not edit by hand) -->", "<!-- R125-T4 END -->"
B5, E5 = "<!-- R125-T5 BEGIN (written by reviews/r125/tools/r125_t45_report.py; do not edit by hand) -->", "<!-- R125-T5 END -->"
LANES_T4 = ("SB-MINI5", "SB-H45", "SB-LUNA", "SB-OP5", "SB-SOL"); LANES_T5 = ("NC-OP5", "NC-LUNA", "NC-SOL")
VENDOR = {"SB-MINI5": "openai", "SB-LUNA": "openai", "SB-SOL": "openai", "NC-LUNA": "openai", "NC-SOL": "openai", "SB-H45": "anthropic", "SB-OP5": "anthropic", "NC-OP5": "anthropic"}


def f4(x):
    return "—" if x is None else f"{x:.4f}"


def sci(d):
    return f"[{d['ci_lo']:.4f}, {d['ci_hi']:.4f}]"


def dci(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"


def lane_census(lane):
    p = ROWS / f"rows_r125_{lane}.jsonl"
    if not p.exists():
        return None
    rows = [json.loads(l) for l in io.open(p, encoding="utf-8") if l.strip()]
    ok = [r for r in rows if r.get("status") == "OK"]
    return {"rows": len(rows), "ok": len(ok), "not_ok": len(rows) - len(ok), "usd": round(sum(r.get("usd", 0.0) for r in rows), 4), "served": sorted({r.get("served_model") for r in ok}),
            "draws": sorted({int(r["draw"]) for r in rows}), "tok_in_mean": round(sum(r.get("tok_in", 0) or 0 for r in ok) / max(1, len(ok)), 1), "tok_out_mean": round(sum(r.get("tok_out", 0) or 0 for r in ok) / max(1, len(ok)), 1)}


def spend():
    pr = C.jload(ROWS / "probes_r125.json") if (ROWS / "probes_r125.json").exists() else {}
    leak = C.jload(ROWS / "leak_r125.json") if (ROWS / "leak_r125.json").exists() else {}
    out = {"anthropic": {"lanes": {}, "probes": 0.0}, "openai": {"lanes": {}, "probes": 0.0, "leak": leak.get("usd", 0.0)}}
    for lane in LANES_T4 + LANES_T5:
        c = lane_census(lane)
        if c:
            out[VENDOR[lane]]["lanes"][lane] = c["usd"]
        if lane in pr:
            out[VENDOR[lane]]["probes"] += pr[lane].get("usd", 0.0)
    for v in out:
        out[v]["total"] = round(sum(out[v]["lanes"].values()) + out[v]["probes"] + out[v].get("leak", 0.0), 4)
    return out


def t4_block(t4):
    R = t4["readers"]; P = t4["predictions"]
    L = [f"### AUX-CF2-R125-SB-<READER> — the matched AUROC of PN against SIBLING within the pair ({t4['meta']['n_pairs']} pairs; dropped {t4['meta']['dropped']}); PN vs PRESENT on the same pairs; SIBLING vs PRESENT (descriptive)", "",
         "| reader | PN vs SIBLING W/T/L | **matched** | triple interval | persona interval | pooled PN vs SIBLING | PN vs PRESENT matched (same pairs) | SIBLING vs PRESENT W/T/L | matched | SIBLING minus PRESENT mean score (triple; persona) | minus the name lookup, matched (triple; persona) |",
         "|---|---|---:|---|---|---:|---:|---|---:|---|---|"]
    for name, r in R.items():
        if "status" in r:
            L.append(f"| {name} | {r['status']} | | | | | | | | | |"); continue
        m = r["pn_vs_sibling"]; s = r["sibling_vs_present"]; d = r["sibling_minus_present_mean"]; ml = r.get("minus_lookup_matched")
        L.append(f"| {name} | {m['W']}/{m['T']}/{m['L']} | **{m['matched']:.4f}** | {sci(m['ci_triple'])} | {sci(m['ci_persona'])} | {r['pooled_pn_vs_sibling']:.4f} | {r['pn_vs_present_same_pairs']['matched']:.4f} | {s['W']}/{s['T']}/{s['L']} | {s['matched']:.4f} | "
                 f"{d['delta']:+.4f} {dci(d['ci_triple'])} {dci(d['ci_persona'])}{' **reliable**' if d['both_exclude_zero'] else ''} | " + (f"{ml['delta']:+.4f} {dci(ml['ci_triple'])} {dci(ml['ci_persona'])}{' **reliable**' if ml['both_exclude_zero'] else ''}" if ml else "") + " |")
    L += ["", "Mean scores per version (PN / PRESENT / SIBLING): " + "; ".join(f"{name} {r['means']['PN']:.4f} / {r['means']['PRESENT']:.4f} / {r['means']['SIBLING']:.4f}" for name, r in R.items() if "means" in r) + ".", ""]
    for k in ("P-SB1", "P-SB2", "P-SB3", "P-SB4"):
        p = P[k]; L.append(f"### AUX-CF2-R125-SB-{k} — **{p['verdict']}** ({p['criterion']})"); L.append("")
        if k == "P-SB1":
            L.append(f"The name lookup reads {p['lookup']:.4f} (a recorded value, ADDENDUM_R125_SIBLING §8).")
        elif k == "P-SB2":
            L.append("; ".join(f"{n}: {v.get('matched', '—')} (persona lower bound {v.get('persona_lo', '—')}; {'ok' if v.get('ok') else v.get('verdict', 'not ok')})" for n, v in p["per_model"].items()) + ".")
        elif k == "P-SB3":
            L.append(f"The random-token lookup {p['random_token']:.4f}, the count reader {p['count_reader']:.4f} (recorded values, §8).")
        else:
            L.append(f"Reliably above the lookup: {p['reliably_above'] or 'none'}.")
        L.append("")
    return L


def t5_block(t5):
    R = t5["readers"]; P = t5["predictions"]
    L = ["### AUX-CF2-R125-NC-<MODEL>-NAMES, -COUNTS — names-only and counts-only on the 444 (pooled AUROC; persona interval; minus the recorded intact row, minus the name lookup, both intervals; per state)", "",
         "| model | rendering | pooled | persona interval | sup / ret / exp | minus intact (item; persona) | minus the other intact row | minus the name lookup | matched PN vs PRESENT whole (W/T/L) | matched sup / ret / exp | matched PN vs ABSENT |",
         "|---|---|---:|---|---|---|---|---|---|---|---:|"]
    for name, r in R.items():
        if "status" in r:
            L.append(f"| {name} | {r['status']} | | | | | | | | | |"); continue
        for arm, lab in (("names_only", "names only"), ("counts_only", "counts only")):
            a = r[arm]; m = a["matched"]["whole"]
            L.append(f"| {name} (intact {r['intact_row']} {r['intact_pooled']:.4f}) | {lab} | {a['pooled']['whole']:.4f} | {sci(a['ci_persona_whole'])} | {' / '.join(f4(a['pooled']['per_state'][s]) for s in STATES)} | "
                     f"{a['minus_intact']['delta']:+.4f} {dci(a['minus_intact']['item_ci'])} {dci(a['minus_intact']['persona_ci'])}{' **reliable**' if a['minus_intact']['both_exclude_zero'] else ''} | "
                     f"{a['minus_other_intact']['delta']:+.4f} ({r['other_intact_row']}) | {a['minus_lookup']['delta']:+.4f} {dci(a['minus_lookup']['item_ci'])} {dci(a['minus_lookup']['persona_ci'])} | "
                     f"{m['matched']:.4f} ({m['W']}/{m['T']}/{m['L']}) {sci(m['ci_triple'])} {sci(m['ci_persona'])} | {' / '.join(f4(a['matched']['per_state'][s]['matched']) for s in STATES)} | {a['matched_absent']['whole']['matched']:.4f} |")
        cn = r["counts_minus_names"]; cm = r["counts_minus_names_matched"]
        L.append(f"| {name} | counts only minus names only | pooled {cn['delta']:+.4f} {dci(cn['item_ci'])} {dci(cn['persona_ci'])}{' **reliable**' if cn['both_exclude_zero'] else ''} | | | | | | matched {cm['delta']:+.4f} {dci(cm['ci_triple'])} {dci(cm['ci_persona'])}{' **reliable**' if cm['both_exclude_zero'] else ''} | | |")
    L += ["", "### AUX-CF2-R125-NC-MATCHED — counts-only per state under the matched metric with both intervals (the P-N5 quantities)", "",
          "| model | retraction W/T/L | matched | triple | persona | expiry W/T/L | matched | triple | persona |", "|---|---|---:|---|---|---|---:|---|---|"]
    for name, r in R.items():
        if "status" in r:
            continue
        ps = r["counts_only"]["matched"]["per_state"]
        L.append(f"| {name} | " + " | ".join(f"{ps[s]['W']}/{ps[s]['T']}/{ps[s]['L']} | {ps[s]['matched']:.4f} | {sci(ps[s]['ci_triple'])} | {sci(ps[s]['ci_persona'])}" for s in ("RETRACTION", "EXPIRY")) + " |")
    L.append("")
    for k in ("P-N3", "P-N4", "P-N5"):
        p = P[k]; L.append(f"### AUX-CF2-R125-NC-{k} — **{p['verdict']}** ({p['criterion']})"); L.append("")
        for n, v in p["per_model"].items():
            if v["verdict"] == "NOT EVALUABLE":
                L.append(f"- {n}: NOT EVALUABLE (the lane did not run: the registered budget rule)")
            elif k == "P-N5":
                L.append(f"- {n}: {v['verdict']}; retraction {v['RETRACTION']['matched']:.4f} (persona lower bound {v['RETRACTION']['persona_lo']:.4f}), expiry {v['EXPIRY']['matched']:.4f} (lower bound {v['EXPIRY']['persona_lo']:.4f})")
            else:
                L.append(f"- {n}: {v['verdict']}; Δ {v['delta']:+.4f}, intervals {v['item_ci']} and {v['persona_ci']}")
        L.append("")
    return L


def run_block(task):
    lock = C.jload(ROWS / "lock_r125.json"); pr = C.jload(ROWS / "probes_r125.json"); proj = C.jload(ROWS / "projection_r125.json"); leak = C.jload(ROWS / "leak_r125.json")
    lanes = LANES_T4 if task == "T4" else LANES_T5
    L = [f"### AUX-CF2-R125-{'SB' if task == 'T4' else 'NC'}-LOCK, -PROBES, -PROJECTION" + (", -LEAK" if task == "T4" else ""), "",
         f"Registrations `{lock['registrations']}` asserted against `{lock['freeze_file']}`; prompts_e1 file `{lock['prompts_file_sha256'][:16]}…` / texts `{lock['prompts_texts_sha256'][:16]}…`; " +
         (f"SIBLING texts sha256 `{lock['sibling_texts_sha256'][:16]}…` ({lock['n_sibling']} items); " if task == "T4" else f"E2's texts sha256 asserted: {lock['nc_texts_sha256']}; ") +
         f"caps {lock['caps']}; runner sha256 `{lock['runner_sha256'][:16]}…`; lock written {lock['when']}.", ""]
    if task == "T4":
        L += [f"Leak screen on the SIBLING texts: **{leak['verdict']}**, {leak['n_correct']} of {leak['n']} correct (threshold {leak['threshold']}), non-UNKNOWN {leak['n_non_unknown']}, parse failures {leak['n_parse_failures']}, served {leak['served_models']}, ${leak['usd']:.4f}.", ""]
    L += ["| lane | served | identifier | probe in / out | probe $ | projected calls | projected $ | ×1.3 | rows | OK | not OK | draws | in / out mean | metered $ |", "|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---:|"]
    for lane in lanes:
        p = pr.get(lane, {}); q = proj.get(lane, {}); c = lane_census(lane)
        L.append(f"| {lane} | {p.get('served')} | {'ok' if p.get('identifier_ok') else 'MISMATCH'} | {p.get('tok_in')} / {p.get('tok_out')} | {p.get('usd', 0):.4f} | {q.get('calls', '—')} | {q.get('usd', '—')} | {q.get('x1.3', '—')} | " +
                 (f"{c['rows']} | {c['ok']} | {c['not_ok']} | {c['draws']} | {c['tok_in_mean']} / {c['tok_out_mean']} | {c['usd']:.4f} |" if c else "not run | | | | | |"))
    t = proj["totals"]
    L += ["", f"Projection at the freeze's probes: Anthropic ${t['anthropic']['projected']:.3f} (fits the cap: {t['anthropic']['fits']}), OpenAI ${t['openai']['projected']:.3f} (fits: {t['openai']['fits']}); OpenAI without NC-SOL ${proj['openai_without_NC-SOL']['projected']:.3f}.", ""]
    return L


def main():
    t4 = C.jload(C.RESULTS / "r125_t4_sibling.json"); t5 = C.jload(C.RESULTS / "r125_t5_nc.json"); sp = spend()
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=str(C.ROOT)).stdout.strip()
    b4 = run_block("T4") + t4_block(t4) + ["### AUX-CF2-R125-SB-SPEND", "", f"Task 4 metered: " + "; ".join(f"{k} ${v:.4f}" for k, v in {**sp['anthropic']['lanes'], **sp['openai']['lanes']}.items() if k.startswith('SB-')) + ".", ""]
    b5 = run_block("T5") + t5_block(t5) + ["### AUX-CF2-R125-NC-SPEND", "", f"Task 5 metered: " + "; ".join(f"{k} ${v:.4f}" for k, v in {**sp['anthropic']['lanes'], **sp['openai']['lanes']}.items() if k.startswith('NC-')) + ".", "",
                                          f"**Program spend (token-metered from the rows; not an invoice):** Anthropic ${sp['anthropic']['total']:.4f} of the $10.00 cap (lanes {sp['anthropic']['lanes']}, probes ${sp['anthropic']['probes']:.4f}); OpenAI ${sp['openai']['total']:.4f} of the $10.00 cap (lanes {sp['openai']['lanes']}, probes ${sp['openai']['probes']:.4f}, leak screen ${sp['openai']['leak']:.4f}).", ""]
    OUT.write_text("\n".join(["# R125 Tasks 4 and 5 — tables", "", "## Task 4. The sibling-name control (ADDENDUM_R125_SIBLING)", ""] + b4 + ["", "## Task 5. E2 Amendment 1 (ADDENDUM_R125_E2_AMENDMENT_1)", ""] + b5) + "\n", encoding="utf-8", newline="\n")
    text = C.LEDGER.read_text(encoding="utf-8")
    for bb, ee, body, title in ((B4, E4, b4, f"## 15d. AUX-CF2-R125-SB — the sibling-name control (program R125, Task 4; registered `reviews/r125/registrations/ADDENDUM_R125_SIBLING.md`, frozen 5cd8f80, sha `62078c878a165437…`; `reviews/r125/tools/r125_run.py`, `r125_t45_score.py`; rows `cf2/rows/rows_r125_SB-*.jsonl`; `reviews/r125/results/r125_t4_sibling.json`; scored at {sha})"),
                                (B5, E5, b5, f"## 15e. AUX-CF2-R125-NC — E2 Amendment 1, names-only and counts-only on the three strong models (program R125, Task 5; registered `reviews/r125/registrations/ADDENDUM_R125_E2_AMENDMENT_1.md`, frozen 5cd8f80, sha `41182fa7697dc402…`; rows `cf2/rows/rows_r125_NC-*.jsonl`; `reviews/r125/results/r125_t5_nc.json`; scored at {sha})")):
        block = "\n".join([bb, "", title, ""] + body + ["", ee]) + "\n"
        if bb in text:
            text = re.sub(re.escape(bb) + r".*?" + re.escape(ee) + r"\n?", lambda m: block, text, flags=re.S)
        else:
            text = text.rstrip("\n") + "\n\n" + block
    C.LEDGER.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(C.ROOT)} and the R125-T4 / R125-T5 blocks of {C.LEDGER.relative_to(C.ROOT)}; spend {json.dumps({v: sp[v]['total'] for v in sp})}")


if __name__ == "__main__":
    main()
