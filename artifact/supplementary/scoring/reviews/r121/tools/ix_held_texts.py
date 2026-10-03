# -*- coding: utf-8 -*-
"""ix_held_texts.py -- program R121: HELD_TEXTS_R121.md from cf2/results/cf_scores_ix.json, to the author's direction of 2026-09-19
(after the interim read): the Section 5 paragraph as four facts in order, the E.3 and Limitations sentences verbatim, the abstract clause
as a standalone sentence in two wordings (placed after the sentence describing what the monitor sees, never inside the definition of
NOK), P-I1 and P-I2 into the failed-predictions count and table as registered with the observed direction, Sol beside Luna as it falls
with the post-interim-read disclosure, and the open items. Every number from the scores file. Shown to the author; nothing lands
(ruling 9: the main session lands on the author's ruling). NO MODEL CALL."""
from __future__ import annotations

import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SCORES = ROOT / "r82_counterfactual" / "cf2" / "results" / "cf_scores_ix.json"
HELD = ROOT / "reviews" / "r121" / "HELD_TEXTS_R121.md"
READERS = ("MINI", "H45", "LUNA", "OP5", "SOL")
NAMES = {"MINI": "GPT-4.1 mini", "H45": "Haiku 4.5", "LUNA": "GPT-5.6 Luna", "OP5": "Opus 5", "SOL": "GPT-5.6 Sol"}


def f2(x):
    return f"{x:.2f}"


def ci(c):
    return f"[{c['ci_lo']:.3f}, {c['ci_hi']:.3f}]"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    res = json.load(io.open(SCORES, encoding="utf-8")); P = res["predictions"]; Rd = res["readers"]; Lk = res["lookups"]
    A = {l: Rd[l]["A"] for l in READERS}
    # the body uses the one-draw column wherever Sol or Opus 5 appears beside the others (the author, 2026-09-19); the registered collapse stays in the outcome texts
    def ss(l, pop, arm):
        e = Rd[l][pop][arm]; return e["draw1"]["same_store"] if "draw1" in e else e["same_store"]
    p0 = {l: ss(l, "A", "P0")["auroc"] for l in READERS}; p1 = {l: ss(l, "A", "P1")["auroc"] for l in READERS}
    p0b = {l: ss(l, "B", "P0")["auroc"] for l in READERS}
    kw = Lk["A"]["keyword"]["same_store"]["auroc"]; kwb = Lk["B"]["keyword"]["same_store"]["auroc"]
    nm, nmb = Lk["A"]["name"]["same_store"]["auroc"], Lk["B"]["name"]["same_store"]["auroc"]
    sep = {l: bool(p1[l] > 0.5 and ss(l, "A", "P1")["ci_pair"]["ci_lo"] > 0.5 and ss(l, "A", "P1")["ci_persona"]["ci_lo"] > 0.5) for l in READERS}
    sl = A["SOL"].get("sol_losses_P1", {})
    i5max = max(abs(Rd[l][pop]["p1_minus_p0_cell1_vs_cell2"]["delta"]) for l in READERS for pop in ("A", "B"))
    i5_ok = all(Rd[l][pop]["p1_minus_p0_cell1_vs_cell2"]["delta"] >= -0.05 for l in READERS for pop in ("A", "B"))
    seps = [l for l in READERS if sep[l]]; nots = [l for l in READERS if not sep[l]]
    # the registration table reports the registered collapse (the predictions were evaluated on it), not the comparable column
    p0r = {l: A[l]["P0"]["same_store"]["auroc"] for l in READERS}; p1r = {l: A[l]["P1"]["same_store"]["auroc"] for l in READERS}

    # (a) under P0 every model below 0.50 on a fixed store
    lows = [l for l in READERS if p0[l] < 0.5]; highs = [l for l in READERS if p0[l] >= 0.5]
    below = not highs
    # the author's wording (rulings on HELD_TEXTS_R121.md, 2026-09-19); every number is rendered from the scores file and the
    # rendered sentence is asserted against the dictated one, so the ruling and the artifact agree
    assert highs == ["OP5"] and len(lows) == 4, (lows, highs)
    fa = (f"Under the main-study rubric four of the five models do not condition on intent: on a fixed store they score the change or past question higher than the original "
          f"(same-store AUROC ${f2(min(p0[l] for l in lows))}$ to ${f2(max(p0[l] for l in lows))}$ on supersession). Opus 5 does, without being told (${f2(p0['OP5'])}$, and ${f2(p0b['OP5'])}$ on expiry).")
    DICTATED_A = ("Under the main-study rubric four of the five models do not condition on intent: on a fixed store they score the change or past question higher than the original "
                  "(same-store AUROC $0.35$ to $0.44$ on supersession). Opus 5 does, without being told ($0.90$, and $0.85$ on expiry).")
    assert fa == DICTATED_A, ("fact (a) differs from the dictated text", fa)
    sol_b_clause = f" GPT-5.6 Sol reads ${f2(p0b['SOL'])}$ on expiry under the old rubric."
    fa = fa + sol_b_clause
    w = ss("SOL", "A", "P1")["wtl"]
    nine = f" In {sl['n_both_at_least_0_96']} of GPT-5.6 Sol's {sl['n']} losses ({w[0]}/{w[1]}/{w[2]} within pairs) both questions score $0.96$ or higher, so the rule was not applied on those pairs."
    fb = (f"Under a rubric that states the rule, Opus 5, GPT-5.6 Luna and GPT-5.6 Sol separate the intents (${f2(p1['OP5'])}$, ${f2(p1['LUNA'])}$ and ${f2(p1['SOL'])}$ at one draw), "
          f"the first two at the level of a fixed cue list (${f2(kw)}$). GPT-4.1 mini and Haiku 4.5 do not (${f2(p1['MINI'])}$ and ${f2(p1['H45'])}$).")
    DICTATED_B = ("Under a rubric that states the rule, Opus 5, GPT-5.6 Luna and GPT-5.6 Sol separate the intents ($0.99$, $0.96$ and $0.88$ at one draw), "
                  "the first two at the level of a fixed cue list ($0.99$). GPT-4.1 mini and Haiku 4.5 do not ($0.48$ and $0.55$).")
    assert fb == DICTATED_B, ("fact (b) differs from the dictated text", fb)
    assert sl["n_both_at_least_0_96"] == 9 and sl["n"] == 11 and w == [76, 0, 11], (sl["n_both_at_least_0_96"], sl["n"], w)
    fb = fb + nine
    fc = f"The name lookup is within tolerance of $0.50$ on both populations (${f2(nm)}$, ${f2(nmb)}$)."
    deltas = {(l, pop): Rd[l][pop]["p1_minus_p0_cell1_vs_cell2"]["delta"] for l in READERS for pop in ("A", "B")}
    (lf, pf), fall = min(deltas.items(), key=lambda kv: kv[1]); (lg, pg), gain = max(deltas.items(), key=lambda kv: kv[1])
    popname = {"A": "supersession", "B": "expiry"}
    fd = (f"The intent-explicit rubric lowers no model's original-task discrimination by more than $0.05$ (the largest fall ${f2(-fall)}$, {NAMES[lf]} on the {popname[pf]} pairs"
          + (f"; the largest rise ${f2(gain)}$, {NAMES[lg]} on the {popname[pg]} pairs" if gain > 0.05 else "") + ")." if i5_ok
          else f"The intent-explicit rubric lowers the original-task discrimination by up to ${f2(-fall)}$ ({NAMES[lf]} on the {popname[pf]} pairs).")
    sec5 = ("Definition 1 makes the label depend on intent, and no main-study row varies the intent over a fixed store. A crossover on the counterfactual set does: each supersession pair is asked its recorded present-tense question and a second question about how the attribute has changed, of the same two store versions, and each expiry pair a question about the past event under the all-states summary, so that the same stale record is forbidden under one question and licensed under the other (Appendix~\\ref{app:counterfactual}). "
            + " ".join([fa, fb, fc, fd]))

    abstract_anchor = "The monitor sees only a lifecycle summary: record counts per lifecycle state and a value-free list of attribute names, on which only superseded names appear."
    p0_except = ("" if below else " except " + " and ".join(NAMES[l] for l in highs))
    abs1 = (f"That summary is judged for staleness, not for obligation: with the store held fixed and the question's intent crossed, no model{p0_except} withholds by intent under the main-study rubric, and told that the obligation depends on the question {', '.join(NAMES[l] for l in seps) if seps else 'no model'} {'do' if len(seps) != 1 else 'does'} while {', '.join(NAMES[l] for l in nots) if nots else 'none'} {'do not' if len(nots) != 1 else 'does not'}.")
    abs2 = (f"On a fixed store the main-study rubric scores the crossed question higher than the original for {', '.join(NAMES[l] for l in lows)}, so their NOK numbers measure lifecycle-sensitive detection{(' while ' + ' and '.join(NAMES[l] for l in highs) + ' already withholds by intent') if highs else ''}; an intent-explicit rubric separates the intents for {', '.join(NAMES[l] for l in seps) if seps else 'no model'} and not for {', '.join(NAMES[l] for l in nots) if nots else 'none'}.")

    def rowtxt(k, holds, txt):
        return f"| {k} | {'holds' if holds else 'fails'} | {txt} |"
    reg_rows = [
        rowtxt("P-I1", P["P-I1"]["holds"], "registered: every model within tolerance of 0.50 under P0 on A. Observed direction: below 0.50 for " + ", ".join(f"{NAMES[l]} ({p0r[l]:.3f})" for l in READERS if p0r[l] < 0.5) + " (the crossed question scores higher than the original on the same store)" + ("; above 0.50 for " + ", ".join(f"{NAMES[l]} ({p0r[l]:.3f})" for l in READERS if p0r[l] >= 0.5) + " (it separates the intents under the frozen rubric)" if any(p0r[l] >= 0.5 for l in READERS) else "") + "."),
        rowtxt("P-I2", P["P-I2"]["holds"], "registered: Opus 5 and Haiku 4.5 separate the intents under P1 on A, both intervals excluding 0.50. Observed: " + "; ".join(f"{NAMES[l]} {p1r[l]:.3f} {ci(A[l]['P1']['same_store']['ci_persona'])} {ci(A[l]['P1']['same_store']['ci_pair'])}" for l in ("OP5", "H45")) + f"; GPT-5.6 Luna, not named in the prediction, {p1r['LUNA']:.3f}."),
        rowtxt("P-I2b (made after the interim read of three lanes; Amendment 1)", P["P-I2b"]["holds"], f"GPT-5.6 Sol under P1 on A {p1r['SOL']:.3f} {ci(A['SOL']['P1']['same_store']['ci_persona'])} {ci(A['SOL']['P1']['same_store']['ci_pair'])}."),
        rowtxt("P-I3", P["P-I3"]["holds"], f"the name lookup {nm:.3f} (A), {nmb:.3f} (B); question length crossed minus original {Lk['A']['question_length']['tokens_mean_delta']:+.2f} / {Lk['B']['question_length']['tokens_mean_delta']:+.2f} content tokens."),
    ]
    H = [f"# HELD_TEXTS_R121 — the held texts with their numbers filled, to the author's direction of 2026-09-19 (scored {res['when'][:16]}; five lanes)\n",
         "For the author's read. Nothing here has been landed; the main session lands on the author's ruling (ruling 9). Every number is from `r82_counterfactual/cf2/results/cf_scores_ix.json` (ledger `cf2/NUMBERS_CF2.md` §14d). The registered branch texts of §9 are superseded by this direction where they differ; the registered outcome texts are in §6 below.\n",
         "## 1. Section 5, one paragraph after \"and tie every triple.\" — four facts in order (a) rubric, (b) intent-explicit rubric with Sol and Opus as they fall, (c) the name lookup, (d) the original task\n", sec5 + "\n",
         "## 2. Appendix E.3, one sentence after \"Step 2 is the scored quantity.\"\n",
         "For four of the five models the main-study rubric does not elicit the intent condition; Opus 5 applies it unprompted. In the main populations every PN question has current or upcoming intent by construction, so there a staleness judgment and an obligation judgment coincide; they come apart only in this crossover.\n",
         "## 3. Limitations, one sentence\n", "The main study was not rerun under the intent-explicit rubric.\n",
         f"## 4. The abstract — one standalone sentence, placed after the sentence that describes what the monitor sees (\"{abstract_anchor}\"), never inside the definition of NOK (the author's wording, ruling of 2026-09-19)\n",
         "When a question's intent licenses the old content, only Opus 5 lowers its judgment under our main rubric; told the rule, GPT-5.6 Sol and GPT-5.6 Luna follow it as well, and GPT-4.1 mini and Haiku 4.5 do not.\n",
         "## 5. The registration table (Appendix F) and the failed-predictions count: P-I1 and P-I2 as registered, with the observed direction; P-I2b labelled as made after the interim read\n",
         "| prediction | outcome | as registered, and the observed direction |", "|---|---|---|", *reg_rows,
         f"\nThe failed-predictions count rises by {int(not P['P-I1']['holds']) + int(not P['P-I2']['holds'])} (P-I1{'' if P['P-I1']['holds'] else ' fails'}, P-I2{'' if P['P-I2']['holds'] else ' fails'}); P-I2b {'holds' if P['P-I2b']['holds'] else 'fails'} and is counted in its own row as a post-interim-read prediction; P-I4 and P-I5 are descriptive and not counted.\n",
         "## 6. The registered outcome texts\n", f"- {P['P-I1']['text']}", f"- {P['P-I2']['text']}", f"- {P['P-I2b']['text']}", f"- {P['P-I3']['text']}",
         f"- P-I4 (descriptive): keyword-intent lookup same-store A {kw:.4f} / B {kwb:.4f}; pooled A {Lk['A']['keyword']['pooled']['auroc']:.4f}; the models under P1 minus the lookup on A: " + "; ".join(f"{NAMES[l]} same-store {A[l]['P1']['vs_keyword_same']['delta']:+.4f}, pooled {A[l]['P1']['vs_keyword_pooled']['delta']:+.4f}" for l in READERS) + ".",
         f"- P-I5 (descriptive): no model lowered by more than 0.05 on cells 1 vs 2: {P['P-I5']['no_model_lowered_by_more_than_tol']} ({json.dumps(P['P-I5']['readings'])}).\n",
         "## 7. Appendix C.2, the table `tab:cf-intent` (the values are in ledger §14d; rows per reader, the five models and the three lookups, × population × arm; for GPT-5.6 Luna and Haiku 4.5 **both columns print**, the five-draw means and the draw-1-only comparable column; columns the same-store AUROC with both intervals, W/T/L, the interaction mean with both intervals, the pooled AUROC; the caption names the crossed questions' construction, the five drops, the Sol lane's post-interim-read addition, the P-I5 readings, and GPT-5.6 Sol's within-pair counts " + (f"{sl['wtl'][0]}/{sl['wtl'][1]}/{sl['wtl'][2]} with {sl['n_both_at_least_0_96']} of its {sl['n']} losses scoring both questions at 0.96 or higher, which means the rule was not applied on those pairs" if sl else "") + ")\n",
         "## 8. Open items (not experiments of this registration)\n",
         "- Rerunning the counterfactual set under the intent-explicit rubric is left for the rebuttal period.",
         "- A cue-free crossed-question population (an instruction that forbids the cue wordings) is left for the rebuttal period.\n"]
    io.open(HELD, "w", encoding="utf-8", newline="\n").write("\n".join(H))
    print("\n".join(H))


if __name__ == "__main__":
    main()
