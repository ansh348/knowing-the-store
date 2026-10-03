# NUMBERS_NB6SWEEP.md — the post hoc nb6 sweep's ledger keys (written 2026-09-14, R106; `tools/ledger_nb6sweep.py`)

Source `results/step4_recall.json` (sha256 `f9acef8e4726075a…`; seed 42), the artifact `nb6_sweep/REPORT.md` sections 6 and 7 print. Post hoc: the sweep was run after every registered result was known and carries no prediction (its section 0 prediction concerned the reconstruction cell and is reported in the REPORT). Four decimals here; the paper's two-decimal and tenths forms are in AUX-NB6SWEEP-PRINTED.

The decomposition: eight corners on each population, length in {base, 15}, contamination in {base, 0.232}, TRUE-name recall in {1.0, r}; the Shapley value of each factor averages its marginal contribution over the six orderings and the three sum to the total gap; the share is the Shapley value over the total gap. Inside a cell the order is recall drop, then injection, then padding.

## AUX-NB6SWEEP-DECOMP-444 — the counterfactual set, 444 items, v2 summary

**r = 0.3604** (marker-corrected BELIEVED recall).

| measure | base → full | total gap | Δ length alone | Δ contamination alone | Δ recall alone | interaction | Shapley L | Shapley c | Shapley r | share L | share c | share r |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| embedding lookup, whole set | 0.7663 → 0.5005 | -0.2659 | -0.0816 | -0.0923 | -0.1902 | +0.0982 | -0.0278 | -0.0782 | -0.1598 | 0.1047 | 0.2943 | 0.6010 |
| embedding lookup, supersession slice | 0.9223 → 0.5200 | -0.4022 | -0.1423 | -0.0906 | -0.2501 | +0.0808 | -0.0918 | -0.0761 | -0.2343 | 0.2282 | 0.1892 | 0.5826 |
| lexical lookup, whole set | 0.6698 → 0.4949 | -0.1748 | -0.0376 | -0.0737 | -0.1184 | +0.0548 | -0.0099 | -0.0656 | -0.0993 | 0.0565 | 0.3753 | 0.5682 |
| lexical lookup, supersession slice | 0.7829 → 0.5371 | -0.2459 | -0.0647 | -0.0730 | -0.1911 | +0.0829 | -0.0243 | -0.0596 | -0.1620 | 0.0987 | 0.2423 | 0.6590 |

**r = 0.2996** (the ledger recall, marker in the denominator).

| measure | base → full | total gap | Δ length alone | Δ contamination alone | Δ recall alone | interaction | Shapley L | Shapley c | Shapley r | share L | share c | share r |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| embedding lookup, whole set | 0.7663 → 0.4881 | -0.2783 | -0.0816 | -0.0923 | -0.2101 | +0.1058 | -0.0257 | -0.0772 | -0.1754 | 0.0923 | 0.2775 | 0.6303 |
| embedding lookup, supersession slice | 0.9223 → 0.4985 | -0.4237 | -0.1423 | -0.0906 | -0.2939 | +0.1030 | -0.0834 | -0.0745 | -0.2659 | 0.1967 | 0.1757 | 0.6275 |
| lexical lookup, whole set | 0.6698 → 0.4909 | -0.1789 | -0.0376 | -0.0737 | -0.1254 | +0.0578 | -0.0084 | -0.0656 | -0.1049 | 0.0472 | 0.3666 | 0.5862 |
| lexical lookup, supersession slice | 0.7829 → 0.5256 | -0.2573 | -0.0647 | -0.0730 | -0.2054 | +0.0857 | -0.0232 | -0.0593 | -0.1749 | 0.0900 | 0.2305 | 0.6795 |

## AUX-NB6SWEEP-DECOMP-661 — the 661 obligation questions, TRUE summary

**r = 0.3604** (marker-corrected BELIEVED recall).

| measure | base → full | total gap | Δ length alone | Δ contamination alone | Δ recall alone | interaction | Shapley L | Shapley c | Shapley r | share L | share c | share r |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| embedding lookup, whole set | 0.7442 → 0.6096 | -0.1346 | -0.0332 | -0.0593 | -0.1565 | +0.1145 | +0.0309 | -0.0561 | -0.1094 | -0.2294 | 0.4167 | 0.8127 |
| embedding lookup, supersession slice | 0.9599 → 0.6593 | -0.3006 | -0.1696 | -0.0661 | -0.3028 | +0.2379 | -0.0572 | -0.0503 | -0.1931 | 0.1902 | 0.1675 | 0.6423 |
| lexical lookup, whole set | 0.5738 → 0.5032 | -0.0706 | -0.0115 | -0.0217 | -0.0546 | +0.0172 | -0.0002 | -0.0223 | -0.0480 | 0.0035 | 0.3161 | 0.6804 |
| lexical lookup, supersession slice | 0.6241 → 0.5345 | -0.0897 | +0.0003 | -0.0213 | -0.0924 | +0.0238 | +0.0159 | -0.0254 | -0.0801 | -0.1769 | 0.2833 | 0.8936 |

**r = 0.2996** (the ledger recall, marker in the denominator).

| measure | base → full | total gap | Δ length alone | Δ contamination alone | Δ recall alone | interaction | Shapley L | Shapley c | Shapley r | share L | share c | share r |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| embedding lookup, whole set | 0.7442 → 0.5930 | -0.1513 | -0.0332 | -0.0593 | -0.1586 | +0.0999 | +0.0266 | -0.0578 | -0.1200 | -0.1758 | 0.3822 | 0.7936 |
| embedding lookup, supersession slice | 0.9599 → 0.6376 | -0.3223 | -0.1696 | -0.0661 | -0.3138 | +0.2272 | -0.0593 | -0.0523 | -0.2108 | 0.1839 | 0.1622 | 0.6539 |
| lexical lookup, whole set | 0.5738 → 0.5019 | -0.0719 | -0.0115 | -0.0217 | -0.0594 | +0.0206 | +0.0009 | -0.0210 | -0.0518 | -0.0120 | 0.2914 | 0.7206 |
| lexical lookup, supersession slice | 0.6241 → 0.5323 | -0.0919 | +0.0003 | -0.0213 | -0.1003 | +0.0295 | +0.0177 | -0.0232 | -0.0864 | -0.1926 | 0.2521 | 0.9405 |

## AUX-NB6SWEEP-BELIEVED — the measured properties of the real backend's superseded-names list (REPORT section 7)

| property | value |
|---|---:|
| length_rendered | 15.04 |
| length_uncapped | 32.55 |
| recall_marker_corrected | 0.3604 |
| recall_ledger | 0.2996 |
| contamination | 0.232 |
| emb | 0.5858 |
| lex | 0.4718 |

## AUX-NB6SWEEP-PRINTED — the printed forms

| printed | source |
|---|---|
| missing names about six tenths, wrong names about three tenths, list length about one tenth of the lookup's loss | AUX-NB6SWEEP-DECOMP-444, r = 0.3604, embedding whole set: shares r 0.6010, c 0.2943, L 0.1047 |
| on the 661: missing names about eight tenths, wrong names about four tenths, length a credit of about two tenths | AUX-NB6SWEEP-DECOMP-661, r = 0.3604, embedding whole set: shares r 0.8127, c 0.4167, L -0.2294 |
| $0.77$ to $0.50$ | 0.7663 → 0.5005 (AUX-NB6SWEEP-DECOMP-444, embedding whole set, the base corner and the full-fault corner) |
| $0.74$ to $0.61$ | 0.7442 → 0.6096 (AUX-NB6SWEEP-DECOMP-661, embedding whole set) |
| $15$ names, recall $0.36$, contamination $0.23$ | AUX-NB6SWEEP-BELIEVED: 15.04, 0.3604, 0.232 |
