# NUMBERS_R97 — the number record for the rounded forms R97 prints from the SIDE registration's frozen texts

R97 is a paper round and produces no measurements. This file exists for one class of value: a
figure that the frozen text of `registrations/ADDENDUM_SIDE.md` prints at a rounding that
`side_experiments/NUMBERS_SIDE.md` carries only at four decimals, so that `trace_scan_v13` can
account for the printed token. Each row states the ledger key, the four-decimal value, the
rounding the frozen text uses, and the manuscript site. Nothing here is a new number.

Registered in `iclr2027_monitoring_submission/tools/trace_scan_v13.py`'s `LEDGERS` list, on the
precedent of `reviews/NUMBERS_R86.md` and `reviews/NUMBERS_R87.md`. CLAIMS.md R97 block, entries
2b and 8.

---

## The frozen S2 census reading (`ADDENDUM_SIDE.md` §S2, "prints regardless, appendix only"; Appendix F.9, R97 entry 2b)

Frozen text: "Two filters on the metadata FR-Bank exposes — the store's own supersession
pointers, alone and restricted to an active successor at least fourteen days later — leave the
superseded list at 15.04 and 8.96 names per item against 1.75 under ground truth, at precision
0.035 and 0.062. The store records 5,968 deactivations and the manifest 104 supersessions, and on
the fields the store exposes the two are indistinguishable; forty of the 104 are still active in
the store. The believed-state loss is not a filtering problem."

| Printed | Ledger key (`NUMBERS_SIDE.md` §5, `AUX-SIDE-S2-CENSUS`) | Four-decimal value | Rounding |
|---|---|---:|---|
| 15.04 | BR-A, names per item (equal to BELIEVED at cap 15) | 15.0378 | two decimals (also `NUMBERS_E1R.md` L257–258 as printed) |
| 8.96 | BR-B, names per item | 8.9592 | two decimals |
| 1.75 | TRUE, names per item | 1.7474 | two decimals (also `NUMBERS_E1R.md` as printed) |
| 0.035 | BR-A precision (equal to BELIEVED's rendered precision) | 0.0348 | three decimals |
| 0.062 | BR-B precision | 0.0618 | three decimals |
| 5,968 | store deactivations | 5,968 | exact |
| 104 | TRUE-superseded entries | 104 | exact |
| 40 (printed "forty") | TRUE-superseded entries still active | 40 | exact |

## The frozen Mem0 descriptive text and the S2-U branch text (Sections 5.3 and 6; R97 entries 1a, 2a)

These print figures `NUMBERS_SIDE.md` already carries as strings: 49.4 percent (§8, the frozen
text as ledgered, from coverage 0.4939), 0.567 (§1, `AUX-SIDE-S1-SPOTCHECK-MEM0`), 30.0 and 66.6
percent (§5, `AUX-SIDE-S2-CAP-RECALL`), 65.5 percent and the intervals (§8, `AUX-SIDE-S2-MINI`).
No row is needed here; they are listed so the trace can be audited from one place. The order's
precision sentence prints the ledger's two values, 0.0348 (rendered, cap 15) and 0.0357
(uncapped), in place of the registration's rounded 0.035.
