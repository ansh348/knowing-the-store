"""stop_report.py -- the §4 STOP report for the author's ruling (87 of 148 accepted < 120). NOT the §5 sheet:
no sheet is written before the ruling. Lists every accepted paraphrase beside its original and every
excluded pair with its candidates and the token each failed on, with the diagnosis. No model call."""
from __future__ import annotations

import collections
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from para_common import PARA, REG_SHA, content, jload, pairs  # noqa: E402

OUT = PARA / "DRAFT_STOP.md"


def main():
    Q = jload(PARA / "para_questions.json")
    m, rows = Q["meta"], Q["rows"]
    P = {p["pair_id"]: p for p in pairs()}
    acc = [r for r in rows if r["accepted"]]
    exc = [r for r in rows if not r["accepted"]]
    src = collections.Counter(); blocked_by_value = 0; intent_only = 0
    for r in exc:
        pr = P[r["pair_id"]]
        topic = content(pr["slot"].split(":")[0].replace("_", " "))
        value = content(pr["slot"].replace(":", " ").replace("_", " ")) - topic
        hits = collections.Counter(h for d in r["drafts"] for t in d["trail"] for h in (t.get("screen_hits") or []))
        kinds = set()
        for h, c in hits.items():
            k = "value" if h in value else ("topic" if h in topic else "other")
            src[k] += c; kinds.add(k)
        if "value" in kinds:
            blocked_by_value += 1
        if any(t.get("screen_ok") for d in r["drafts"] for t in d["trail"]):
            intent_only += 1
    n_cand = sum(len(d["trail"]) for r in exc for d in r["drafts"])
    n_screen = sum(1 for r in exc for d in r["drafts"] for t in d["trail"] if t.get("question") and not t["screen_ok"])
    n_intent = sum(1 for r in exc for d in r["drafts"] for t in d["trail"] if t.get("screen_ok") and t.get("intent_ok") is False)
    st_a = collections.Counter(r["state"] for r in acc); st_e = collections.Counter(r["state"] for r in exc)
    in_a = collections.Counter(r["intent"] for r in acc); in_e = collections.Counter(r["intent"] for r in exc)
    L = [
        "# DRAFT_STOP — ADDENDUM_PARA §4 STOP: 87 of 148 pairs accepted, below the 120 floor (2026-09-14)\n",
        f"Registration sha256 `{REG_SHA}` (frozen at `dab8956`); prompt sha256 `{m['prompt_sha256']}` asserted; locks and the lookup gate on the "
        f"original questions held (embedding v2 {m['lookup_gate']['emb_v2']:.4f}, v3 {m['lookup_gate']['emb_v3']:.4f}). Drafting ran as registered: "
        f"{m['calls']} calls, {m['prompt_tokens']:,} in / {m['completion_tokens']:,} out tokens, ${m['usd_list_est']:.4f}; three-call probe served "
        f"`{(m.get('served_models') or ['?'])[0]}`. **Accepted {m['n_accepted']}, excluded {m['n_excluded']}**; attempts per pair {m['attempts_histogram']}. "
        f"Per §4 the draft STOPs here for the author's ruling; **no sheet has been written and no score of any kind has been computed on these paraphrases.** "
        f"This file is not the §5 sheet.\n",
        "## Diagnosis\n",
        f"- Accepted by state: supersession {st_a.get('SUPERSESSION', 0)} of 88, retraction {st_a.get('RETRACTION', 0)} of 30, expiry {st_a.get('EXPIRY', 0)} of 30; by intent: "
        f"CURRENT-STATE {in_a.get('CURRENT-STATE', 0)}, UPCOMING {in_a.get('UPCOMING', 0)}. Excluded: supersession {st_e.get('SUPERSESSION', 0)}, retraction {st_e.get('RETRACTION', 0)}, "
        f"expiry {st_e.get('EXPIRY', 0)}; UPCOMING {in_e.get('UPCOMING', 0)}, CURRENT-STATE {in_e.get('CURRENT-STATE', 0)}. The retraction and expiry pairs (the CF-2 pairs whose slot paths carry a "
        f"named plan or event) are the ones that fail.",
        f"- Of the excluded pairs' {n_cand} candidates, **{n_screen} failed the §3 screen** and {n_intent} passed the screen but failed the CF-1 intent gate; "
        f"{intent_only} of the 61 pairs had at least one screen-passing candidate (excluded by the intent gate alone: the drafter wrote *forthcoming* / *later today*, "
        f"which are not CF-1 UPCOMING markers).",
        f"- Where the offending tokens come from (token hits over the excluded pairs' trails): **slot-path value tokens, the part after the `:`, {src['value']}**; "
        f"slot topic tokens (before the `:`) {src['topic']}; other printed attribute names {src['other']}. **{blocked_by_value} of the 61 excluded pairs are blocked by a "
        f"value token** — the referent itself (`kayla`, `greg`, `cima`, `isfahan`, `nowruz`, `vitamin`, `juul`, `ffp3`, `salone del mobile`, …).",
        "- §3(a) forbids the content tokens of the whole slot path, split on `:` and `_`, so the value part of a CF-2 slot path (`event:Kayla_graduation_party` → "
        "`kayla`, `graduation`, `party`) is forbidden. The summaries print only the scrubbed name before the `:` (`event`), so those value tokens are never visible to "
        "either lookup; forbidding them asks the drafter for the same specific detail without its referent, which gpt-4.1-mini cannot do for a proper noun and which, "
        "where it tries, broadens the question (*the historic urban area in central Iran* for Isfahan). The 87 accepted pairs are mostly those whose slot path has no value part "
        "or whose value is a common noun the drafter could work around.",
        "",
        "## Rulings available (the author's; each is appended to the registration as a dated line before any further call)\n",
        "1. **Accept the 87** (n = 261 items; positives 65 / 8 / 14 by state): amend the floor; the retraction row rests on 8 pairs and the expiry row on 14.",
        "2. **Narrow §3(a) to the scrubbed slot name** (the part before the first `:`, the only part any summary prints) and keep (b) every printed attribute name unchanged; "
        "redraft only the 61 excluded pairs under the same frozen prompt, seeds and gate. The 87 accepted paraphrases stay as drafted (they pass the narrower screen a fortiori). "
        "Value-naming is then tracked, not forbidden: the sheet's second column and `AUX-PARA-FLAGS` record which paraphrases still name the value. Cost ≈ $0.05.",
        "3. **Keep the screen and redraft the 61 with a stronger drafter** (a model that is not a reader on this set, e.g. `gpt-4.1`) under the same prompt: likely rescues some "
        "common-noun cases, not the proper-noun referents.",
        "4. Any combination, or exclude the set.",
        "",
        f"## The 87 accepted paraphrases (original beside each; the sheet's columns are NOT here — no verdict is asked before the ruling)\n",
        "| # | pair_id | state | intent | original question | paraphrase (draft, candidate index) |", "|---:|---|---|---|---|---|"]
    for i, r in enumerate(acc, 1):
        d = r["drafts"][-1]
        L.append(f"| {i} | `{r['pair_id']}` | {r['state']} | {r['intent']} | {r['question']} | {r['paraphrase']} (d{d['draft']} #{d['selected_index']}) |")
    L += ["", "## The 61 excluded pairs (every candidate with the token(s) it failed on, or `intent` where it passed the screen and failed the intent gate)\n",
          "| pair_id | state | intent | slot path | original question | candidates |", "|---|---|---|---|---|---|"]
    for r in exc:
        cands = "<br>".join(f"d{d['draft']}#{t['index']} “{t.get('question')}” [{', '.join(t.get('screen_hits') or (['intent: ' + str(t.get('typed'))] if t.get('intent_ok') is False else ['?']))}]"
                            for d in r["drafts"] for t in d["trail"])
        L.append(f"| `{r['pair_id']}` | {r['state']} | {r['intent']} | `{r['slot']}` | {r['question']} | {cands} |")
    io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(f"wrote {OUT}: accepted {len(acc)}, excluded {len(exc)}, blocked by a value token {blocked_by_value}, intent-gate only {intent_only}")


if __name__ == "__main__":
    main()
