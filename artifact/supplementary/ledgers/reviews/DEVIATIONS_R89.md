# DEVIATIONS_R89 — R89-BRANCHA deviation ledger

Every departure from the R89-BRANCHA prompt, with a one-line reason. This program assigns only
`D-R89-n` identifiers.

Opened 2026-09-11.

| ID | Deviation | Reason |
|---|---|---|
| **D-R89-1** | The §4 backends sentence is split in two: "This study compares three backends. FR-Bank is the lifecycle-tracking store of [AUTHOR-1] & [AUTHOR-2] (2026) and the one evaluated store that records a lifecycle state on every entry; Mem0 is …; and A-MEM is …". The program gave the FR-Bank descriptor as a clause inside the existing colon list. | The prescribed clause took the sentence to 43 words and `prose_scan`'s 40-word rule failed. The descriptor is verbatim as given; only the list's grammar changes (colon list → sentence with "is"). No number, no claim. |
