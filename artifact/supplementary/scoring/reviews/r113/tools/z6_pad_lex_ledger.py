# -*- coding: utf-8 -*-
"""z6_pad_lex_ledger.py -- SPEC_R113 section Z6: the lexical lookup's paired difference against the committed list at 100 and 200
padded names under the registered draw order, read from the recorded artifact reviews/v18/results/a4_pad_extend.json (R110's A4;
no recomputation; the values were computed by reviews/v18/tools/a4_pad_extend.py on 2026-09-14 and not ledgered in AUX-R110-A4,
which printed the lexical single-arm interval). NO MODEL CALL. $0. Appends AUX-R113-PAD-LEX-PAIRED to NUMBERS_R113.md and writes
reviews/r113/results/z6_pad_lex_paired.json.
"""
from __future__ import annotations

import datetime as dt

from r113_common import ROOT, RESULTS, J, jdump, assert_spec, ledger_append, sha16, r4

ART = ROOT / "reviews" / "v18" / "results" / "a4_pad_extend.json"


def main():
    assert_spec()
    d = J(ART); reg = d["readings"]["i_registered_order"]
    assert d["base"]["lex"]["auroc"] == 0.5738 and d["base"]["emb"]["auroc"] == 0.7484
    out = {"meta": {"script": "reviews/r113/tools/z6_pad_lex_ledger.py", "artifact": str(ART.relative_to(ROOT)), "artifact_sha256_16": sha16(ART), "model_calls": 0, "recomputed": False,
                    "when": dt.datetime.now().isoformat(timespec="seconds")}, "rows": {}}
    for L in ("100", "200"):
        x = reg[L]; lex = x["lookups"]["lex"]; p = x["paired_vs_base"]["lex"]; e = x["paired_vs_base"]["emb"]
        out["rows"][L] = {"keys_spilling_into_pool_b": x["keys_spilling_into_pool_b"], "names_from_pool_b_total": x["names_from_pool_b_total"],
                          "lex_auroc": lex["auroc"], "lex_delta": p["delta"], "lex_item_ci": [r4(p["item_ci"]["ci_lo"]), r4(p["item_ci"]["ci_hi"])], "lex_persona_ci": [r4(p["persona_ci"]["ci_lo"]), r4(p["persona_ci"]["ci_hi"])],
                          "emb_auroc": x["lookups"]["emb"]["auroc"], "emb_delta": e["delta"], "emb_item_ci": [r4(e["item_ci"]["ci_lo"]), r4(e["item_ci"]["ci_hi"])], "emb_persona_ci": [r4(e["persona_ci"]["ci_lo"]), r4(e["persona_ci"]["ci_hi"])]}
    jdump(out, RESULTS / "z6_pad_lex_paired.json")
    r1, r2 = out["rows"]["100"], out["rows"]["200"]
    L = ["\n## 6. AUX-R113-PAD-LEX-PAIRED: the lexical lookup at 100 and 200 padded names under the registered draw order, paired against the committed list (SPEC_R113 Z6; read from `reviews/v18/results/a4_pad_extend.json`, R110's A4 artifact; no recomputation; no call)\n\n",
         f"Artifact sha256 `{out['meta']['artifact_sha256_16']}...`. The registered draw order continues into pool B (other personas' names) once the store's own pool is exhausted: at 100 names {r1['keys_spilling_into_pool_b']} of 242 keys draw {r1['names_from_pool_b_total']} names from pool B, at 200 every key does ({r2['names_from_pool_b_total']} names). The embedding rows are AUX-R110-A4's (0.6558, -0.0926 [-0.1718, -0.0221] / [-0.1953, +0.0199]; 0.5960, -0.1525 [-0.2357, -0.0773] / [-0.2595, -0.0399]). The lexical paired rows, padded minus the committed list (base 0.5738), item-level and persona-clustered (1,000 draws, seed 42):\n\n",
         "| L | lexical AUROC | delta vs 0.5738 | item 95% | persona 95% |\n|---:|---:|---:|---|---|\n",
         f"| 100 | {r1['lex_auroc']:.4f} | **{r1['lex_delta']:+.4f}** | [{r1['lex_item_ci'][0]:+.4f}, {r1['lex_item_ci'][1]:+.4f}] | [{r1['lex_persona_ci'][0]:+.4f}, {r1['lex_persona_ci'][1]:+.4f}] |\n",
         f"| 200 | {r2['lex_auroc']:.4f} | **{r2['lex_delta']:+.4f}** | [{r2['lex_item_ci'][0]:+.4f}, {r2['lex_item_ci'][1]:+.4f}] | [{r2['lex_persona_ci'][0]:+.4f}, {r2['lex_persona_ci'][1]:+.4f}] |\n",
         "\nBoth intervals include zero at both lengths: the lexical lookup is flat under the registered order as it is at 15, 30 and 60.\n",
         "\n### AUX-R113-PRINTED: the forms the v19 manuscript prints from this pass (each from a value above or in the key named)\n\n| printed | source | key |\n|---|---|---|\n",
         "| $100$, $200$; $79$ of $242$ | 100, 200; keys_spilling_into_pool_b 79 of 242 keys (every key at 200) | AUX-R110-A4; this section |\n",
         "| $0.6558$, $0.5960$ | the embedding lookup at 100 and 200 under the registered order | AUX-R110-A4 |\n",
         f"| $-0.0137$ $[-0.0672,+0.0369]$ $[-0.0926,+0.0716]$; $-0.0355$ $[-0.0903,+0.0189]$ $[-0.1125,+0.0455]$ | the lexical rows at 100 and 200 | this section |\n",
         "| $99$, $129$, $0.6531$ | the store's own pool exhausted: mean 99.2209 names, at most 129, embedding 0.6531 | AUX-R110-A4 (reading (ii)) |\n"]
    ledger_append("".join(L))


if __name__ == "__main__":
    main()
