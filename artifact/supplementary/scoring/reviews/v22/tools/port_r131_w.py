# -*- coding: utf-8 -*-
"""port_r131_w.py -- the R131 close's page 8-9 payers (2026-09-20; the author's block 'R131 CLOSE: PAGE 8-9 PAYERS', W1 to W7), applied to
reviews/v22/src/body_v22.tex (and, for W7, reviews/v22/src/appendix_v22.tex) after port_r131_close.py --payers=5,5b,6,7,8,B2. Cumulative: --w=N applies
W1 to WN in the ruled order; --w1b adds W1's conditional second change (the pointer still alone on its line after W1a: 'including Kimi' -> 'Kimi included').
Every edit is an asserted replacement; the author's texts verbatim (numerals in math mode); no gate rewords them (a trip is reported and the author
rules). The number gate for the texts is r131_w_gate() below (every number read from its artifact; hard stop on a mismatch); it runs before any edit.
  W1  Section 8, first paragraph: 'Across the shared' -> 'On the shared' (W1a); 'including Kimi' -> 'Kimi included' (W1b, only if the pointer still sits alone)
  W2  Limitations, paragraph 1: the small-groups sentences -> one sentence
  W3  Limitations, paragraph 3: the alignment sentences -> one sentence
  W4  Section 7, the tested-rule paragraph: its third sentence folded into the second
  W5  Limitations, paragraph 2: 'pooled AUROC was fixed in advance'; 'The paraphrase check is not yet scored.' (the one-rewording design is stated in C.2)
  W6  Conclusion: the all-states clause deleted (Section 5.2 keeps the Opus result)            -- only if still short of +2
  W7  Section 8, second paragraph: its last sentence deleted; E.8 gains the pointer sentence   -- only if still short of +2
Usage: python reviews/v22/tools/port_r131_w.py --w=N [--w1b] [--skip=3] [--check]
"""
from __future__ import annotations

import io
import json
import pathlib
import sys
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT_B = ROOT / "reviews" / "v22" / "src" / "body_v22.tex"
APPX = ROOT / "reviews" / "v22" / "src" / "appendix_v22.tex"
R125 = ROOT / "reviews" / "r125" / "results"

CHANGES = []
GATE_CHANGES = []
CHECKS = []


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def rep(t, old, new, n=1, where=""):
    assert t.count(old) == n, (where, t.count(old), n, old[:120])
    return t.replace(old, new)


def change(item, section, t, old, new, reason):
    CHANGES.append((item, section, old, new, reason))
    return rep(t, old, new, 1, item + " " + section)


def r2(x):
    return str(Decimal(str(round(x, 4))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def r131_w_gate():
    """The number gate on W2, W3, W6 and W7: every number from its artifact, half-up at the printed precision; the facts W5 and W7 depend on checked in the appendix."""
    M = json.load(open(R125 / "r125_matched.json", encoding="utf-8"))
    T3F = json.load(open(R125 / "r125_t3_frbank.json", encoding="utf-8"))
    ps = M["readers"]["LOOKUP_v2"]["pn_vs_present"]["per_state"]
    def chk(where, printed, value, source):
        ok = (r2(value) == printed) if isinstance(value, float) else (str(value) == str(printed))
        CHECKS.append({"where": where, "printed": str(printed), "value": value, "source": source, "ok": ok})
    chk("W2: 30 counterfactual retraction pairs", "30", ps["RETRACTION"]["n"], "r125_matched.json readers/LOOKUP_v2/pn_vs_present/per_state/RETRACTION/n")
    chk("W2: 30 counterfactual expiry pairs", "30", ps["EXPIRY"]["n"], "r125_matched.json .../per_state/EXPIRY/n")
    all104 = T3F["rescored"]["all_104 (manifest-relative, the printed rows)"]
    chk("W2: 26 retraction obligations on the full set", "26", all104["by_state"]["ret"], "r125_t3_frbank.json rescored/all_104/by_state/ret")
    chk("W2: 15 expiry obligations on the full set", "15", all104["by_state"]["exp"], "r125_t3_frbank.json rescored/all_104/by_state/exp")
    un = T3F["rescored"]["join_unmarked_0.80 (the 22)"]
    chk("W3: the 22 obligations the alignment does not mark", "22", un["n_pos"], "r125_t3_frbank.json rescored/join_unmarked_0.80/n_pos (104 - 82 at the 0.80 bar)")
    chk("W3: mini 0.52 on them under ground truth", "0.52", float(un["readers"]["mini_true"]["auroc"]), "r125_t3_frbank.json rescored/join_unmarked_0.80/readers/mini_true/auroc")
    body = rd(OUT_B); appx = rd(APPX)
    chk("W6: Section 5.2 keeps Opus's 0.03 lead (reliable pooled, not matched)", "1", body.count("Opus's $0.03$ lead over that lookup is reliable on the pooled metric and not on the matched one"), "body_v22.tex Section 5.2")
    chk("W7: C.2 prints that every model's coverage interval on the counterfactual set excludes chance", "1", appx.count("and every interval excludes $0.50$."), "appendix_v22.tex C.2, 'Coverage on the counterfactual set.' (tab:cf-fok)")
    chk("W5: the appendix states the one-rewording design", "1", appx.count("The paraphrase check asks each of the $148$ questions again in a wording that shares no content token"), "appendix_v22.tex C.2, the paraphrase paragraph")
    bad = [c for c in CHECKS if not c["ok"]]
    for c in CHECKS:
        v = c["value"]; vs = f"{v:.4f}" if isinstance(v, float) else str(v)
        print(f"{'ok  ' if c['ok'] else 'FAIL'} {c['where']}: printed {c['printed']} <- {vs}  [{c['source']}]")
    print(f"{len(CHECKS)} checks, {len(bad)} mismatches")
    return bad


W1A_OLD = "Across the shared cross-vendor questions, models whose question-only score varies gain a reliable $0.15$ to $0.45$, including Kimi."
W1A_NEW = "On the shared cross-vendor questions, models whose question-only score varies gain a reliable $0.15$ to $0.45$, including Kimi."
W1B_OLD = "gain a reliable $0.15$ to $0.45$, including Kimi."
W1B_NEW = "gain a reliable $0.15$ to $0.45$, Kimi included."
W2_OLD = "Retraction and expiry remain small groups: the counterfactual set has $30$ pairs of each. The full obligation set has $26$ retraction obligations and $15$ expiry obligations, so those state-specific results give only a direction."
W2_NEW = "Retraction and expiry are small groups ($30$ counterfactual pairs each; $26$ and $15$ obligations on the full set), so state-specific results give only a direction."
W3_OLD = "The ground-truth name lists are built through the manifest-to-record alignment. The $22$ obligations it does not mark are therefore invisible to every summary (mini scores $0.52$ on them under ground truth)."
W3_NEW = "The ground-truth name lists come from the manifest-to-record alignment, so the $22$ obligations it does not mark are invisible to every summary (mini scores $0.52$ on them under ground truth)."
W4_OLD = ("But $187$ of $272$ audited stale lines sit under a different attribute key from their tagged twin.\n"
          "The view-side rule we tested cannot make the repair, which leaves the write path.\n")
W4_NEW = "But $187$ of $272$ audited stale lines sit under a different attribute key from their tagged twin, which leaves the write path.\n"
W5A_OLD = "the metric fixed in advance is the pooled AUROC"
W5A_NEW = "pooled AUROC was fixed in advance"
W5B_OLD = "The paraphrase check, with one rewording per question fixed in advance, is not yet scored."
W5B_NEW = "The paraphrase check is not yet scored."
W6_OLD = "with list length kept fixed or not; with all states named, Opus's $0.03$ lead is reliable on one metric and not on the other."
W6_NEW = "with list length kept fixed or not."
W7_OLD = ("On easier coverage questions, mini's advantage over the superseded-name lookup disappears against a lookup over the whole name map.\n"
          "On the counterfactual set, all reported model coverage intervals exclude chance. (Appendix~\\ref{app:baselines})\n")
W7_NEW = "On easier coverage questions, mini's advantage over the superseded-name lookup disappears against a lookup over the whole name map. (Appendix~\\ref{app:baselines})\n"
W7_APPX_ANCHOR = "The comparison between model and lookup is therefore complete on the full obligation population ($661$) and on the store-counterfactual set ($444$).\n"
W7_APPX_NEW = (W7_APPX_ANCHOR +
               "%% R131 close, W7 (2026-09-20): the body's sentence moves here as a pointer (Appendix C.2 prints the intervals, tab:cf-fok).\n"
               "On the counterfactual set every model's coverage interval excludes chance (Table~\\ref{tab:cf-fok}, Appendix~\\ref{app:counterfactual}).\n")


def main():
    check = "--check" in sys.argv
    w = int(next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--w=")), "0"))
    w1b = "--w1b" in sys.argv
    skip = {int(x) for x in next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--skip=")), "").split(",") if x.strip()}   # a W item omitted by ruling (W3 under its Q-A trip)
    bad = r131_w_gate()
    assert not bad, "the number gate failed; hard stop"
    b = rd(OUT_B); a = rd(APPX)
    assert "%% R131 close" in b and "%% R131 W" not in b, "port_r131_w.py: run after port_r131_close.py (and not twice)"
    appx_done = "%% R131 close, W7" in a   # the appendix edit is idempotent across body regenerations (the appendix is not re-ported per variant)
    if w >= 1:
        b = change("W1a", "Section 8", b, W1A_OLD, "%% R131 W (2026-09-20): the author's page 8-9 payers (W1 to W7, cumulative; port_r131_w.py).\n" + W1A_NEW,
                   "'On the shared' for 'Across the shared' so the pointer joins the line above")
        if w1b:
            b = change("W1b", "Section 8", b, W1B_OLD, W1B_NEW, "the pointer still sat alone after W1a: 'Kimi included' for 'including Kimi'")
    if w >= 2:
        b = change("W2", "Limitations, paragraph 1", b, W2_OLD, W2_NEW, "two sentences -> one (the author's)")
    if w >= 3 and 3 not in skip:
        b = change("W3", "Limitations, paragraph 3", b, W3_OLD, W3_NEW, "two sentences -> one (the author's); the R131 Q-A split withdrawn by ruling")
    if w >= 4:
        b = change("W4", "Section 7, the tested-rule paragraph", b, W4_OLD, W4_NEW, "the third sentence, which repeated the bold lead, folded into the second")
    if w >= 5:
        b = change("W5a", "Limitations, paragraph 2", b, W5A_OLD, W5A_NEW, "trim (the author's)")
        b = change("W5b", "Limitations, paragraph 2", b, W5B_OLD, W5B_NEW, "trim; the one-rewording design is stated in Appendix C.2 (checked); the sentence is replaced on 22 Sep")
    if w >= 6:
        b = change("W6", "Conclusion", b, W6_OLD, W6_NEW, "the all-states clause deleted; Section 5.2 keeps the Opus result (loses a little content; used only because still short of +2)")
    if w >= 7:
        b = change("W7", "Section 8, second paragraph", b, W7_OLD, W7_NEW, "the last sentence deleted; C.2 prints the intervals (tab:cf-fok) and E.8 gains a pointer sentence (loses a little content; used only because still short of +2)")
        if not appx_done:
            a = change("W7 (appendix)", "E.8", a, W7_APPX_ANCHOR, W7_APPX_NEW, "the pointer sentence, so E.8 prints the claim the body dropped")
        else:
            CHANGES.append(("W7 (appendix)", "E.8", W7_APPX_ANCHOR, W7_APPX_NEW, "the pointer sentence, so E.8 prints the claim the body dropped (already in place)"))
    assert "—" not in b and "—" not in a
    if check:
        print("port_r131_w.py --check: w", w, "w1b", w1b); return
    io.open(OUT_B, "w", encoding="utf-8", newline="\n").write(b)
    if w >= 7 and not appx_done:
        io.open(APPX, "w", encoding="utf-8", newline="\n").write(a)
    print(f"-> {OUT_B}; W1..W{w} applied{' with W1b' if w1b else ''}; appendix {'edited (W7)' if w >= 7 else 'untouched'}")


if __name__ == "__main__":
    main()
