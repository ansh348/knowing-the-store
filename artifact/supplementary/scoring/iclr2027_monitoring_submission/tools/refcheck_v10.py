import re, pathlib, sys

tex = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
start = tex.index("\\begin{thebibliography}")
end = tex.index("\\end{thebibliography}")
bib = tex[start:end]
items = bib.split("\\bibitem")[1:]
print("bibitem count:", len(items))

official = {
    "mem0": ("2504.19413", "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory", "2025", "P.~Chhikara"),
    "knowact": ("2607.29433", "Know It, Act on It: Investigating Memory Utilization in LLM Personalization", "2026", "Z.~Feng"),
    "knowbutnotact": ("2605.14186", "LLMs Know When They Know, but Do Not Act on It: A Metacognitive Harness for Test-time Scaling", "2026", "Q.~Cao"),
    "memgate": ("2606.06054", "Beyond Similarity: Trustworthy Memory Search for Personal AI Agents", "2026", "J.~Zhang"),
    "seakr": ("2406.19215", "SeaKR: Self-aware Knowledge Retrieval for Adaptive Retrieval Augmented Generation", "2024", "Z.~Yao"),
    "stale": ("2605.06527", "STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?", "2026", "H.~Chao"),
    "verbrouting": ("2607.25600", "Beyond Self-Knowledge: Propagating Uncertainty Across Reasoning and Retrieval in LLMs", "2026", "C.~K. Sah"),
    # --- v1.0 Step 2 additions, each verified against the official arXiv record
    # R75-F13: memoryagentbench upgraded to its published venue, verified against the
    # official record (iclr.cc/virtual/2026/poster/10010781; OpenReview DT7JyQC3MR;
    # the authors' repository). The first slot is now a venue-string membership check.
    "memoryagentbench": ("ICLR", "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions", "2026", "Y.~Hu, Y.~Wang, and J.~McAuley"),
    "abstentionbench": ("2506.09038", "AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions", "2025", "P.~Kirichenko, M.~Ibrahim, K.~Chaudhuri, and S.~J. Bell"),
    "pmbench": ("2607.12385", "PM-Bench: Evaluating Prospective Memory in LLM Agents", "2026", "G.~Liu and S.~Gabriel"),
    "cimemories": ("2511.14937", "CIMemories: A Compositional Benchmark for Contextual Integrity of Persistent Memory in LLMs", "2025", "N.~Mireshghallah"),
    "supersede": ("2606.27472", "Supersede: Diagnosing and Training the Memory-Update Gap in LLM Agents", "2026", "V.~Patel"),
    "gatemem": ("2606.18829", "GateMem: Benchmarking Memory Governance in Multi-Principal Shared-Memory Agents", "2026", "Z.~Ren"),
    "memora": ("2604.20006", "From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents", "2026", "M.~N. Uddin"),
    "automem": ("2607.01224", "AutoMem: Automated Learning of Memory as a Cognitive Skill", "2026", "S.~Wu"),
    "metamem": ("2602.11182", "MetaMem: Evolving Meta-Memory for Knowledge Utilization through Self-Reflective Symbolic Optimization", "2026", "H.~Xin"),
}
# Single-author records: "et al." would be a false attribution and is checked for.
SINGLE_AUTHOR = {"supersede"}
TWO_AUTHOR = {"pmbench"}
THREE_AUTHOR = {"memoryagentbench"}

found = {}
for it in items:
    m = re.search(r"\]\{([^}]+)\}", it)
    if not m:
        continue
    key = m.group(1)
    body = it[m.end():]
    found[key] = re.sub(r"\s+", " ", body).strip()

print("keys:", sorted(found))
print()
allok = True
for k in sorted(official):
    aid, title, yr, lead = official[k]
    b = found.get(k, "")
    plain = b.replace("\\emph{", "").replace("}", "").replace("{", "")
    ok_id = aid in b
    ok_title = title in plain
    ok_yr = re.search(r"\b" + yr + r"\b", b) is not None
    ok_lead = plain.startswith(lead)
    # false-attribution guard: "et al." on a record with a fully enumerated author list
    ok_etal = True
    if k in SINGLE_AUTHOR and "et al" in plain:
        ok_etal = False
    if k in (TWO_AUTHOR | THREE_AUTHOR) and "et al" in plain:
        ok_etal = False
    status = ("VERIFIED" if (ok_id and ok_title and ok_yr and ok_lead and ok_etal)
              else "MISMATCH")
    if status != "VERIFIED":
        allok = False
    print(f"{k:17s} id={ok_id} title={ok_title} year={ok_yr} lead={ok_lead} "
          f"etal={ok_etal} -> {status}")
    if status != "VERIFIED":
        print("   TEX:", plain)
print()
print("ALL VERIFIED" if allok else "FAILURES PRESENT")

# also list every bib key and whether it carries an arXiv id
print()
for k in sorted(found):
    ids = re.findall(r"arXiv:(\d{4}\.\d{4,5})", found[k])
    print(f"  {k:15s} arXiv={ids if ids else '-'}")
