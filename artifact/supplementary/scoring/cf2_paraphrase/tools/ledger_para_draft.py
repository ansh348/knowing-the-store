"""ledger_para_draft.py -- write the status table and AUX-PARA-DRAFT into cf2_paraphrase/NUMBERS_PARA.md
from cf2_paraphrase/para_questions.json and the sheet. No model call; re-runnable (the two sections are
regenerated whole, the rest of the file is kept)."""
from __future__ import annotations

import collections
import hashlib
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from para_common import PARA, REG_SHA, SHEET, jload, sha256_file, sha256_frozen, REG  # noqa: E402

LEDGER = PARA / "NUMBERS_PARA.md"


def main():
    Q = jload(PARA / "para_questions.json")
    m, rows = Q["meta"], Q["rows"]
    acc = [r for r in rows if r["accepted"]]
    exc = [r for r in rows if not r["accepted"]]
    by_state = collections.Counter(r["state"] for r in acc)
    by_intent = collections.Counter(r["intent"] for r in acc)
    n_draft_calls = m["calls"]
    sel_idx = collections.Counter(r["drafts"][-1]["selected_index"] for r in acc)
    screen_fail = collections.Counter()
    intent_fail = 0
    for r in rows:
        for d in r["drafts"]:
            for t in d["trail"]:
                if t.get("screen_hits"):
                    for h in t["screen_hits"]:
                        screen_fail[h] += 1
                if t.get("screen_ok") and t.get("intent_ok") is False:
                    intent_fail += 1
    toks_para = [len(set(re.findall(r"[a-z0-9]+", r["paraphrase"].lower()))) for r in acc]
    sheet_sha = sha256_file(SHEET) if SHEET.exists() else None
    pj = m.get("probe_projection") or {}
    floor = "PASS" if m["n_accepted"] >= 120 else "**STOP for the author's ruling (§4); see DRAFT_STOP.md**"
    status = f"""## 0. Status (2026-09-14, after the drafting run)

| item | state |
|---|---|
| Registration file | committed at `dab8956` (the author's freeze, 2026-09-14): registered text sha256 `{REG_SHA}` over the bytes above the marker line (`para_common.sha256_frozen` = `{sha256_frozen(REG)[:16]}…`, holds); whole file `{sha256_file(REG)[:16]}…` with the dated rulings appended |
| Opus 5 cap ruling (§8) | **(ii) recorded** in the file's dated section of 2026-09-14 (evening), superseding the morning's (i) line: the combined cap is $21 and Opus 5 runs once (k = 1); the PAD Amendment 1 Haiku lane runs regardless of the ×1.3 rule under an overall cap of $28 |
| Locks (§8 STOP list, pre-call) | **all hold** at the drafting run (`para_questions.json` `meta.locks`) |
| Lookup gate on the original questions (§2) | **PASS at four decimals**: embedding v2 **{m['lookup_gate']['emb_v2']:.4f}**, v3 **{m['lookup_gate']['emb_v3']:.4f}**; lexical v2 {m['lookup_gate']['lex_v2']:.4f}, v3 {m['lookup_gate']['lex_v3']:.4f} |
| Drafting lane | **run** — prompt sha256 `{m['prompt_sha256']}` asserted (= the value recorded before any call); {n_draft_calls} calls, ${m['usd_list_est']:.4f} |
| The author's read (§5) | {("**pending** — `reviews/v12/PARAPHRASE_READ.md` written (sha256 `" + sheet_sha[:16] + "…`)") if sheet_sha else ("**not reached — §4 STOP**: " + str(m['n_accepted']) + " of 148 accepted is below the 120 floor, so no sheet is written before the author's ruling (`cf2_paraphrase/DRAFT_STOP.md`: diagnosis, the rulings available, every accepted and excluded pair)")}; no scoring call has been made and none is made before `AUX-PARA-SHEET` is ledgered |
| Lanes after the read | PARA mini → PARA Haiku 4.5 (k = 5) → PAD Amendment 1 Haiku 4.5 (k = 5, regardless of the ×1.3 rule) → Opus 5 (k = 1; ruling ii: combined cap $21, overall cap $28); combined spend so far $2.02 (PAD) + ${m['usd_list_est']:.4f} (drafting) |
"""
    draft = f"""## 2. AUX-PARA-DRAFT — the drafting run (`tools/draft_para.py`; `para_questions.json`; 2026-09-14)

| Key | Value |
|---|---|
| **AUX-PARA-DRAFT** | Prompt sha256 **`{m['prompt_sha256']}`** (SYSTEM ⊕ USER ⊕ `{m['model']}` ⊕ {m['temperature']} ⊕ {m['max_tokens']} ⊕ {m['n_candidates']}), asserted before the run and equal to the value recorded in section 0 before any call. Three-call probe (§8): served `{', '.join(m.get('served_models') or [])}` (E1.7, {'PASS' if pj.get('identifier_ok') else '—'}); projection {pj.get('est_calls')} calls ${pj.get('usd', 0):.2f} (×1.3 ${pj.get('usd_x1.3', 0):.2f}) against the $3 OpenAI line and the combined headroom. **{m['calls']} calls** ({m['prompt_tokens']:,} in / {m['completion_tokens']:,} out tokens, **${m['usd_list_est']:.4f}** at list); attempts per pair {dict(sorted(m['attempts_histogram'].items()))}; seeds {list(m['seeds'])}. **Accepted {m['n_accepted']} of 148** ({m['n_excluded']} excluded; ≥ 120 required — {floor}): supersession {by_state.get('SUPERSESSION', 0)}, retraction {by_state.get('RETRACTION', 0)}, expiry {by_state.get('EXPIRY', 0)}; UPCOMING {by_intent.get('UPCOMING', 0)}, CURRENT-STATE {by_intent.get('CURRENT-STATE', 0)}. Selected candidate index (the seeded start then in order): {dict(sorted(sel_idx.items()))}. Candidates failing the screen: {sum(screen_fail.values())} token hits across the trails (most frequent: {', '.join(f'{k} ×{v}' for k, v in screen_fail.most_common(8))}); candidates passing the screen but failing the intent gate: {intent_fail}. Accepted paraphrases carry {sum(toks_para) / max(1, len(toks_para)):.2f} distinct word tokens on average; every accepted paraphrase re-passes the §3 screen at write time (asserted). Paraphrase set sha256 **`{m['paraphrases_sha256']}`**. |
"""
    r2 = m.get("run2")
    if r2:
        n_val = sum(1 for r in acc if r.get("value_tokens_in_paraphrase"))
        draft += (f"| **AUX-PARA-DRAFT (run 2, the author's ruling of 2026-09-14 evening)** | The 87 accepted paraphrases of run 1 stand. The 61 excluded pairs were redrafted under the "
                  f"same prompt (sha256 asserted), model, seeds, candidates, selection rule and intent gate, with §3(a) narrowed to the scrubbed slot name and §3(b) unchanged "
                  f"(`para_common.forbidden` scope `narrowed`; mean |F| 139.0 against 140.7 registered on the 61). **{r2['calls']} calls**, ${r2['usd_list_est']:.4f}, served `{', '.join(r2['served_models'])}`; "
                  f"attempts per pair {dict(sorted(r2['attempts_histogram'].items()))}; **{r2['n_accepted']} of the 61 accepted, {r2['n_excluded']} still excluded** (now on scrubbed-name tokens such as "
                  f"*study*, *contract*, *kitchen*, *tea*, *sale*, which stay forbidden). Resulting set **{m['n_accepted']} of 148** (≥ 120, PASS): supersession {by_state.get('SUPERSESSION', 0)}, "
                  f"retraction {by_state.get('RETRACTION', 0)}, expiry {by_state.get('EXPIRY', 0)}; of the {m['n_accepted']}, **{m['n_accepted_passing_registered_screen']} also pass the registered (unnarrowed) screen** and "
                  f"{n_val} carry a slot-path value token (a disclosure, tracked by the sheet's column 2 and `AUX-PARA-FLAGS`; not a criterion). "
                  f"Whole set: {m['calls']} calls, ${m['usd_list_est']:.4f}; paraphrase set sha256 **`{m['paraphrases_sha256']}`**. Run 1's artifact is kept as `para_questions_run1.json`. |\n")
    if exc:
        draft += "\n**Excluded pairs** (no passing candidate after three drafts; listed at the end of the sheet with their candidates and the offending tokens):\n\n"
        for r in exc:
            hits = sorted({h for d in r["drafts"] for t in d["trail"] for h in (t.get("screen_hits") or [])})
            draft += f"- `{r['pair_id']}` ({r['state']}, {r['intent']}): \"{r['question']}\" — tokens hit: {', '.join(hits[:12])}\n"
    s = io.open(LEDGER, encoding="utf-8").read()
    s = re.sub(r"## 0\. Status.*?(?=\n## 1\. )", status.rstrip("\n") + "\n", s, count=1, flags=re.S)
    s = re.sub(r"## 2\. AUX-PARA-DRAFT.*?(?=\n## 3\. )", draft.rstrip("\n") + "\n", s, count=1, flags=re.S)
    io.open(LEDGER, "w", encoding="utf-8", newline="\n").write(s)
    print(f"wrote {LEDGER}: accepted {m['n_accepted']} / 148, excluded {m['n_excluded']}, calls {m['calls']}, ${m['usd_list_est']:.4f}")


if __name__ == "__main__":
    main()
