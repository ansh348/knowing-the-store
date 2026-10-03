# -*- coding: utf-8 -*-
"""m2_gate_hunks.py -- the gate-tool hunks of program R114 (2026-09-17), each with a dated header note, applied as asserted byte edits that
keep each file's line endings: (1) reviews/v19/tools/number_moves_wp.py ADDED / VANISHED gain the R114 dispositions (tab:ds-a7's actual-view
composites and the Opus 5 moved-count row); (2) iclr2027_monitoring_submission/tools/trace_scan_v13.py LEDGERS gains reviews/NUMBERS_R114.md.
Idempotent. The Opus dispositions are filled from results/scores_v2rcat_op5.json when it exists. Run from the repository root.
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
TS = ROOT / "iclr2027_monitoring_submission" / "tools" / "trace_scan_v13.py"
NM = ROOT / "reviews" / "v19" / "tools" / "number_moves_wp.py"
OP5 = ROOT / "r82_counterfactual" / "v2rcat" / "results" / "scores_v2rcat_op5.json"


def edit(path, old, new, tag):
    b = path.read_bytes(); nl = b"\r\n" if b"\r\n" in b else b"\n"
    if tag.encode() in b:
        print(f"{path.name}: already applied ({tag[:40]})"); return
    o = old.replace("\n", nl.decode()).encode(); n = new.replace("\n", nl.decode()).encode()
    assert b.count(o) == 1, (path.name, b.count(o), old[:80])
    path.write_bytes(b.replace(o, n))
    print(f"{path.name}: applied ({tag[:40]})")


edit(TS,
     '    pathlib.Path("../reviews/NUMBERS_R113.md"),\n]\n',
     '    pathlib.Path("../reviews/NUMBERS_R113.md"),\n'
     '    # R114 (2026-09-17, the remaining runnable paid experiments): the pass ledger; the numbers the manuscript prints from the pass live in\n'
     '    # ds_downstream/NUMBERS_DS.md section 14 (AUX-DS-R114-*) and r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md section 8 (AUX-V2RCAT-OP5).\n'
     '    pathlib.Path("../reviews/NUMBERS_R114.md"),\n]\n',
     "R114 (2026-09-17, the remaining runnable paid experiments)")

A = ('    "242": "tab:pad\'s caption, the 242 summaries (index keys) of the 661 (AUX-R110-A4)",\n'
     '    # R114 (2026-09-17): tab:ds-a7 and its prose read the absent items the gated rules answer on a longer view on that view\'s own answer\n'
     '    # (ds_downstream/NUMBERS_DS.md section 14, AUX-DS-R114-COMPOSITE-ACTUAL, -ACTUAL-DIFF), replacing the five-line proxy\n'
     '    "265": "tab:ds-a7, GPT-4.1 mini under the model rule (both prompts), absent abstained 265 = 172 + 93 (AUX-DS-R114-COMPOSITE-ACTUAL)",\n'
     '    "93": "tab:ds-a7, GPT-4.1 mini under the model rule, the answerer\'s absent abstentions 93 (AUX-DS-R114-COMPOSITE-ACTUAL)",\n'
     '    "320": "tab:ds-a7, GPT-4.1 mini under the model rule (both prompts), composite 320 of 661 (AUX-DS-R114-COMPOSITE-ACTUAL)",\n'
     '    "292": "tab:ds-a7, Haiku 4.5 under the model rule and the all-states model rule (both prompts), absent abstained 292 = 172 + 120 (AUX-DS-R114-COMPOSITE-ACTUAL)",\n'
     '    "303": "tab:ds-a7, Haiku 4.5 under the lookup rule and the all-states lookup rule (both prompts), absent abstained 303 = 174 + 129 (AUX-DS-R114-COMPOSITE-ACTUAL)",\n'
     '    "372": "tab:ds-a7, Haiku 4.5 under the model rule (header), composite 372 (AUX-DS-R114-COMPOSITE-ACTUAL)",\n'
     '    "380": "tab:ds-a7, Haiku 4.5 under the all-states lookup rule (header), composite 380 (AUX-DS-R114-COMPOSITE-ACTUAL)",\n'
     '    "382": "tab:ds-a7, Haiku 4.5 under the all-states model rule (tagged), composite 382 (AUX-DS-R114-COMPOSITE-ACTUAL)",\n'
     '    "385": "tab:ds-a7, Haiku 4.5 under the all-states lookup rule (tagged), composite 385 (AUX-DS-R114-COMPOSITE-ACTUAL)",\n'
     '    "+19": "tab:ds-a7\'s prose, the model rule minus retrieval alone for GPT-4.1 mini under the header, +19 of 661 (AUX-DS-R114-COMPOSITE-ACTUAL-DIFF)",\n'
     '    "+3": "tab:ds-a7\'s prose, the model rule minus retrieval alone for Haiku 4.5 under the header, +3 of 661 (AUX-DS-R114-COMPOSITE-ACTUAL-DIFF)",\n'
     '    "+9": "tab:ds-a7\'s prose, the lookup rule minus retrieval alone for Haiku 4.5 under the header, +9 of 661 (AUX-DS-R114-COMPOSITE-ACTUAL-DIFF)",\n')
V = ('    "0.6006": "tab:pad, the lexical lookup at 200 names, single-arm item interval upper bound, no longer printed (AUX-R110-A4 keeps it)",\n'
     '    # R114 (2026-09-17): the five-line proxy\'s composites in tab:ds-a7 and its prose, replaced by the actual-view reading; the proxy stands in\n'
     '    # ds_downstream/NUMBERS_DS.md AUX-DS-A7-COMPOSITE-ANSWERED and beside the actual reading in AUX-DS-R114-COMPOSITE-ACTUAL\n'
     '    "+2": "tab:ds-a7\'s prose, the model rule minus retrieval alone for Haiku 4.5 under the proxy (+2), now +3 (AUX-DS-A7-COMPOSITE-ANSWERED-DIFF keeps it)",\n'
     '    "+10": "tab:ds-a7\'s prose, the lookup rule minus retrieval alone for Haiku 4.5 under the proxy (+10), now +9 (AUX-DS-A7-COMPOSITE-ANSWERED-DIFF keeps it)",\n'
     '    "+18": "tab:ds-a7\'s prose, the model rule minus retrieval alone for GPT-4.1 mini under the proxy (+18), now +19 (AUX-DS-A7-COMPOSITE-ANSWERED-DIFF keeps it)",\n'
     '    "119": "tab:ds-a7, Haiku 4.5 under the model rules, the answerer\'s absent abstentions under the proxy (119), now 120 (AUX-DS-A7-COMPOSITE-ANSWERED keeps it)",\n'
     '    "300": "tab:ds-a7, GPT-4.1 mini under the literal rule, composite under the proxy (300), now 301 (AUX-DS-A7-COMPOSITE-ANSWERED keeps it)",\n'
     '    "304": "tab:ds-a7, Haiku 4.5 under the lookup rules, absent abstained under the proxy (304), now 303 (AUX-DS-A7-COMPOSITE-ANSWERED keeps it)",\n'
     '    "371": "tab:ds-a7, Haiku 4.5 under the model rule (header), composite under the proxy (371), now 372 (AUX-DS-A7-COMPOSITE-ANSWERED keeps it)",\n'
     '    "376": "tab:ds-a7, Haiku 4.5 under the all-states model rule (header), composite under the proxy (376), now 377 (AUX-DS-A7-COMPOSITE-ANSWERED keeps it)",\n')

OPUS_LINES = None
if OP5.exists():
    DOC = json.load(open(OP5, encoding="utf-8")); S = DOC["opus"]
    W, R, Ex = S["minus_v2"], S["per_state"]["RETRACTION"], S["per_state"]["EXPIRY"]
    toks = {}
    def t(x, d="+"):
        return f"{x:+.4f}" if d == "+" else f"{x:.4f}"
    toks[t(S["v2rcat"], "")] = "tab:v2rcat, Opus 5 (k = 1) under the moved-count control, whole set (AUX-V2RCAT-OP5)"
    toks[t(S["v2_recorded"], "")] = "tab:v2rcat, Opus 5's recorded superseded-only row (k = 5), whole set (AUX-CF2-OP5-V2 0.8405; AUX-V2RCAT-OP5)"
    toks[t(W["delta"])] = "tab:v2rcat, Opus 5 whole set minus its recorded row (AUX-V2RCAT-OP5)"
    for nm, d in (("item", W["item_ci"]), ("persona", W["persona_ci"])):
        toks[t(d["ci_lo"])] = f"tab:v2rcat, Opus 5 whole set, {nm} interval lower bound (AUX-V2RCAT-OP5)"; toks[t(d["ci_hi"])] = f"tab:v2rcat, Opus 5 whole set, {nm} interval upper bound (AUX-V2RCAT-OP5)"
    for st, D in (("retraction", R), ("expiry", Ex)):
        toks[t(D["v2"], "")] = f"tab:v2rcat, Opus 5's recorded superseded-only row on {st} (AUX-V2RCAT-OP5)"
        toks[t(D["v2rcat"], "")] = f"tab:v2rcat, Opus 5 under the moved-count control on {st} (AUX-V2RCAT-OP5)"
        toks[t(D["delta"])] = f"tab:v2rcat and its prose, Opus 5 on {st} minus its recorded row (AUX-V2RCAT-OP5)"
        toks[f"{D['delta']:+.2f}"] = f"Section 5, Opus 5 on {st} minus its recorded row at two decimals ({D['delta']:+.4f}; AUX-V2RCAT-OP5)"
        for nm, d in (("item", D["item_ci"]), ("persona", D["persona_ci"])):
            toks[t(d["ci_lo"])] = f"tab:v2rcat, Opus 5 on {st}, {nm} interval lower bound (AUX-V2RCAT-OP5)"; toks[t(d["ci_hi"])] = f"tab:v2rcat, Opus 5 on {st}, {nm} interval upper bound (AUX-V2RCAT-OP5)"
    toks["0.14"] = "Appendix E.11, the spend sentence: the composite's answers on the actual expanded views, $0.1357 at two decimals (AUX-DS-R114-SPEND)"
    toks[f"{DOC['spend']['total']:.2f}"] = "Appendix E.11, the spend sentence: Opus 5 on the moved-count control, lane plus probe at two decimals (AUX-V2RCAT-OP5, AUX-V2RCAT-SPEND continued)"
    toks["40"] = "Appendix E.11, the spend sentence: the $40 ceiling of program R114 (reviews/NUMBERS_R114.md AUX-R114-SPEC-FREEZE)"
    OPUS_LINES = '    # R114 (2026-09-17): the optional Opus 5 lane on the moved-count control (r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md section 8, AUX-V2RCAT-OP5; D-V2RCAT-2)\n'
    for k, v in toks.items():
        OPUS_LINES += f'    "{k}": "{v}",\n'
A += '}\n'
V += '}\n'

edit(NM, '    "242": "tab:pad\'s caption, the 242 summaries (index keys) of the 661 (AUX-R110-A4)",\n}\n', A, "R114 (2026-09-17): tab:ds-a7 and its prose read the absent items")
edit(NM, '    "0.6006": "tab:pad, the lexical lookup at 200 names, single-arm item interval upper bound, no longer printed (AUX-R110-A4 keeps it)",\n}\n', V, "R114 (2026-09-17): the five-line proxy's composites")
V2 = ('    "376": "tab:ds-a7, Haiku 4.5 under the all-states model rule (header), composite under the proxy (376), now 377 (AUX-DS-A7-COMPOSITE-ANSWERED keeps it)",\n'
      '    "379": "tab:ds-a7, Haiku 4.5 under the lookup rule (header), composite under the proxy (379), now 378 (AUX-DS-A7-COMPOSITE-ANSWERED keeps it)",\n'
      '    "384": "tab:ds-a7, Haiku 4.5 under the lookup rule (tagged), composite under the proxy (384), now 383 (AUX-DS-A7-COMPOSITE-ANSWERED keeps it)",\n'
      '    "386": "tab:ds-a7, Haiku 4.5 under the all-states lookup rule (tagged), composite under the proxy (386), now 385 (AUX-DS-A7-COMPOSITE-ANSWERED keeps it)",\n')
if b'"386": "tab:ds-a7' not in NM.read_bytes():
    edit(NM, V2.split("\n")[0] + "\n}\n", V2 + "}\n", "R114 (2026-09-17): the five-line proxy's composites, the three lookup-rule composites")
else:
    print("number_moves_wp.py: already applied (the three lookup-rule composites)")
if OPUS_LINES:
    anchor = ('    "+9": "tab:ds-a7\'s prose, the lookup rule minus retrieval alone for Haiku 4.5 under the header, +9 of 661 (AUX-DS-R114-COMPOSITE-ACTUAL-DIFF)",\n'
              '}\n')
    edit(NM, anchor, anchor[:-2] + OPUS_LINES + '}\n', "R114 (2026-09-17): the optional Opus 5 lane on the moved-count control")
print("done")
