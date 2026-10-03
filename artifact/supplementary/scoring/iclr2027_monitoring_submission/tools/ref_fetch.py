r"""ref_fetch -- pull the primary record for each citation the manuscript is about to add.

WHY (R93, 2026-09-11). Thirty-five reviewer-relayed references enter paper_v5.tex. The house
rule since R80_CITATIONS.md is that a bibitem prints what the primary record prints, and that a
record which cannot be fetched is DROPPED rather than guessed. This tool does the fetching so
REFCHECK_V12.md can be a transcription of records rather than of memory.

SOURCES, in the R80 order of authority: the arXiv API (export.arxiv.org/api/query) for arXiv
identifiers; the Crossref REST API (api.crossref.org/works/<DOI>) for DOIs; a Crossref
bibliographic query when only a title is known (books, journals without a DOI in hand); the
OpenReview API v2 for ICLR/TMLR/COLM records (403 behind a bot wall on 2026-09-11; kept for
the day it answers); a "grep" probe over a proceedings listing, anthology volume or accepted-paper
page when the API is walled; DBLP's publication search as a venue cross-check (same wall);
Open Library for ISBNs; and the raw <title> plus citation_* meta tags of a publisher page
(jmlr.org, digitalcommons.law.uw.edu, proceedings.mlr.press, proceedings.neurips.cc).

Nothing here decides anything. It prints what each source returned, per key, and writes the
raw JSON so the verdict in REFCHECK_V12.md can be checked against it.

Usage:
    python tools/ref_fetch.py [--out=path.json] [--only=key1,key2]
Stdlib only. Exit 0 always; missing records are reported as such, not as failures.
"""
import json, re, sys, time, urllib.parse, urllib.request, html
import xml.etree.ElementTree as ET
import ssl
try:
    import certifi
    CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:  # pragma: no cover
    CTX = ssl.create_default_context()

UA = {"User-Agent": "ref_fetch/1.0 (ICLR 2027 submission citation check; stdlib urllib)"}

# key -> probes. Each probe is (kind, value). Expected identifiers come from the R93 plan and
# are what the tool tests; the returned record is what REFCHECK_V12.md transcribes.
REGISTRY = {
    "hart1965":        [("doi", "10.1037/h0022263")],
    "koriat1993":      [("doi", "10.1037/0033-295X.100.4.609")],
    "metcalfe1994":    [("xref", "Metacognition: Knowing about Knowing Metcalfe Shimamura MIT Press 1994"),
                        ("isbn", "9780262132985"), ("dblp", "Metacognition: Knowing about Knowing")],
    "dunlosky2009":    [("xref", "Metacognition Dunlosky Metcalfe SAGE 2009"), ("isbn", "9781412939720")],
    "kadavath2022":    [("arxiv", "2207.05221"), ("dblp", "Language Models (Mostly) Know What They Know")],
    "lin2022":         [("arxiv", "2205.14334"), ("openreview", "8s8K2UZGTZ"),
                        ("grep", ("https://jmlr.org/tmlr/papers/", "Teaching Models to Express Their Uncertainty in Words")),
                        ("dblp", "Teaching Models to Express Their Uncertainty in Words")],
    "tian2023":        [("arxiv", "2305.14975"), ("doi", "10.18653/v1/2023.emnlp-main.330")],
    "xiong2024":       [("arxiv", "2306.13063"), ("openreview", "gjeQKFxFpZ"),
                        ("grep", ("https://iclr.cc/virtual/2024/papers.html", "Can LLMs Express Their Uncertainty")),
                        ("dblp", "Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs")],
    "mallen2023":      [("arxiv", "2212.10511"), ("doi", "10.18653/v1/2023.acl-long.546")],
    "ren2025":         [("arxiv", "2307.11019"),
                        ("grep", ("https://aclanthology.org/volumes/2025.coling-main/", "Investigating the Factual Knowledge Boundary")),
                        ("url", "https://aclanthology.org/2025.coling-main.250/"),
                        ("xref", "Investigating the Factual Knowledge Boundary of Large Language Models with Retrieval Augmentation"),
                        ("dblp", "Investigating the Factual Knowledge Boundary of Large Language Models with Retrieval Augmentation")],
    "wang2023":        [("arxiv", "2310.05002"), ("doi", "10.18653/v1/2023.findings-emnlp.691")],
    "su2024":          [("arxiv", "2403.10081"), ("doi", "10.18653/v1/2024.acl-long.702")],
    "lewis2020":       [("arxiv", "2005.11401"),
                        ("url", "https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html"),
                        ("dblp", "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks")],
    "rajpurkar2018":   [("arxiv", "1806.03822"), ("doi", "10.18653/v1/P18-2124")],
    "kamath2020":      [("arxiv", "2006.09462"), ("doi", "10.18653/v1/2020.acl-main.503")],
    "yang2024":        [("arxiv", "2312.07000"), ("doi", "10.52202/079017-2030"), ("dblp", "Alignment for Honesty"),
                        ("grep", ("https://proceedings.neurips.cc/paper_files/paper/2024", "Alignment for Honesty")),
                        ("xref", "Alignment for Honesty Yang Chern Qiu Neubig Liu")],
    "packer2023":      [("arxiv", "2310.08560"), ("dblp", "MemGPT: Towards LLMs as Operating Systems")],
    "zhong2024":       [("arxiv", "2305.10250"), ("doi", "10.1609/aaai.v38i17.29946")],
    "zhang2025survey": [("arxiv", "2404.13501"), ("doi", "10.1145/3748302"),
                        ("xref", "A Survey on the Memory Mechanism of Large Language Model based Agents"),
                        ("dblp", "A Survey on the Memory Mechanism of Large Language Model based Agents")],
    "nissenbaum2004":  [("url", "https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/"),
                        ("url", "https://digitalcommons.law.uw.edu/wlr/vol79/iss1/11/"),
                        ("xref", "Privacy as Contextual Integrity Nissenbaum Washington Law Review 2004")],
    "maini2024":       [("arxiv", "2401.06121"), ("dblp", "TOFU: A Task of Fictitious Unlearning for LLMs"),
                        ("grep", ("https://colmweb.org/2024/AcceptedPapers.html", "TOFU: A Task of Fictitious Unlearning"))],
    "xu2024conflicts": [("arxiv", "2403.08319"), ("doi", "10.18653/v1/2024.emnlp-main.486")],
    "longpre2021":     [("arxiv", "2109.05052"), ("doi", "10.18653/v1/2021.emnlp-main.565")],
    "dhingra2022":     [("arxiv", "2106.15110"), ("doi", "10.1162/tacl_a_00459")],
    "hanley1982":      [("doi", "10.1148/radiology.143.1.7063747")],
    "naeini2015":      [("doi", "10.1609/aaai.v29i1.9602"),
                        ("xref", "Obtaining Well Calibrated Probabilities Using Bayesian Binning Naeini Cooper Hauskrecht")],
    "guo2017":         [("arxiv", "1706.04599"), ("url", "https://proceedings.mlr.press/v70/guo17a.html"),
                        ("grep", ("https://proceedings.mlr.press/v70/guo17a.html", "On Calibration of Modern Neural Networks"))],
    "zadrozny2002":    [("doi", "10.1145/775047.775151")],
    "platt2000":       [("doi", "10.7551/mitpress/1113.003.0008"), ("doi", "10.7551/mitpress/1113.001.0001"),
                        ("isbn", "9780262194488"),
                        ("xref", "Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods Platt")],
    "geifman2017":     [("arxiv", "1705.08500"),
                        ("url", "https://proceedings.neurips.cc/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html")],
    "brier1950":       [("doi", "10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2")],
    "efron1993":       [("xref", "An Introduction to the Bootstrap Efron Tibshirani 1993"), ("isbn", "9780412042317")],
    "cameron2008":     [("doi", "10.1162/rest.90.3.414")],
    "nosek2018":       [("doi", "10.1073/pnas.1708274114")],
    "pineau2021":      [("url", "https://jmlr.org/papers/v22/20-303.html"), ("arxiv", "2003.12206")],
}


def get(url, accept=None, timeout=40):
    h = dict(UA)
    if accept:
        h["Accept"] = accept
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return r.read().decode("utf-8", errors="replace")


def arxiv(aid):
    x = get(f"http://export.arxiv.org/api/query?id_list={aid}")
    ns = {"a": "http://www.w3.org/2005/Atom", "ar": "http://arxiv.org/schemas/atom"}
    e = ET.fromstring(x).find("a:entry", ns)
    if e is None or e.find("a:title", ns) is None:
        return {"error": "no entry"}
    t = lambda tag, nsp="a": (e.findtext(f"{nsp}:{tag}", default="", namespaces=ns) or "").strip()
    return {"title": re.sub(r"\s+", " ", t("title")),
            "authors": [a.findtext("a:name", namespaces=ns) for a in e.findall("a:author", ns)],
            "published": t("published")[:10], "updated": t("updated")[:10],
            "comment": re.sub(r"\s+", " ", t("comment", "ar")), "journal_ref": t("journal_ref", "ar"),
            "doi": t("doi", "ar"), "id": (e.findtext("a:id", namespaces=ns) or "").split("/abs/")[-1]}


def crossref_item(m):
    au = m.get("author") or m.get("editor") or []
    names = [(" ".join(filter(None, [a.get("given"), a.get("family")])) or a.get("name", "")) for a in au]
    issued = (m.get("issued") or m.get("published-print") or m.get("published-online") or {}).get("date-parts", [[None]])[0][0]
    return {"type": m.get("type"), "title": " ".join(m.get("title") or []), "authors": names,
            "editors": [(" ".join(filter(None, [a.get("given"), a.get("family")]))) for a in (m.get("editor") or [])],
            "container": " ".join(m.get("container-title") or []), "event": (m.get("event") or {}).get("name", ""),
            "volume": m.get("volume", ""), "issue": m.get("issue", ""), "page": m.get("page", ""),
            "year": issued, "publisher": m.get("publisher", ""), "DOI": m.get("DOI", ""),
            "isbn": m.get("ISBN", []), "score": m.get("score")}


def crossref_doi(doi):
    j = json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""), "application/json"))
    return crossref_item(j["message"])


def crossref_query(q, rows=4):
    j = json.loads(get("https://api.crossref.org/works?rows=%d&query.bibliographic=%s" % (rows, urllib.parse.quote(q)),
                       "application/json"))
    return [crossref_item(m) for m in j["message"]["items"]]


def openreview(nid):
    j = json.loads(get(f"https://api2.openreview.net/notes?id={nid}", "application/json"))
    out = []
    for n in j.get("notes", []):
        c = n.get("content", {})
        v = lambda k: (c.get(k, {}) or {}).get("value") if isinstance(c.get(k), dict) else c.get(k)
        out.append({"title": v("title"), "authors": v("authors"), "venue": v("venue"), "venueid": v("venueid"),
                    "invitations": n.get("invitations"), "pdate": n.get("pdate"), "cdate": n.get("cdate")})
    return out


def dblp(q, hits=5):
    j = json.loads(get("https://dblp.org/search/publ/api?format=json&h=%d&q=%s" % (hits, urllib.parse.quote(q)),
                       "application/json"))
    out = []
    for h in (j.get("result", {}).get("hits", {}).get("hit") or []):
        i = h.get("info", {})
        au = i.get("authors", {}).get("author", [])
        if isinstance(au, dict):
            au = [au]
        out.append({"title": i.get("title"), "authors": [a.get("text") for a in au], "venue": i.get("venue"),
                    "volume": i.get("volume"), "number": i.get("number"), "pages": i.get("pages"),
                    "year": i.get("year"), "type": i.get("type"), "doi": i.get("doi"), "key": i.get("key")})
    return out


def isbn(n):
    j = json.loads(get(f"https://openlibrary.org/isbn/{n}.json", "application/json"))
    return {"title": j.get("title"), "subtitle": j.get("subtitle"), "publishers": j.get("publishers"),
            "publish_date": j.get("publish_date"), "authors": j.get("authors"), "by_statement": j.get("by_statement")}


def page(url):
    h = get(url)
    title = html.unescape(re.sub(r"\s+", " ", (re.search(r"<title[^>]*>(.*?)</title>", h, re.S | re.I) or [None, ""])[1])).strip()
    metas = {}
    for m in re.finditer(r'<meta\s+[^>]*?(?:name|property)="(citation_[^"]+|dc\.[^"]+|bepress_[^"]+)"[^>]*?content="([^"]*)"', h, re.I):
        metas.setdefault(m.group(1).lower(), []).append(html.unescape(m.group(2)))
    # content-before-name form; the ACL Anthology leaves the name attribute unquoted
    for m in re.finditer(r"""<meta\s+[^>]*?content="([^"]*)"[^>]*?(?:name|property)=["']?(citation_[^"'\s>]+|dc\.[^"'\s>]+|bepress_[^"'\s>]+)""", h, re.I):
        metas.setdefault(m.group(2).lower(), []).append(html.unescape(m.group(1)))
    return {"title": title, "meta": metas, "bytes": len(h)}


def grep(spec):
    url, needle = spec
    h = get(url, timeout=120)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", h))
    txt = re.sub(r"\s+", " ", txt)
    hits = [txt[max(0, m.start() - 250): m.end() + 250] for m in re.finditer(re.escape(needle), txt, re.I)]
    links = re.findall(r'href="([^"]*)"[^>]*>[^<]*' + re.escape(needle[:40]), h, re.I)
    return {"url": url, "needle": needle, "page_title": (re.search(r"<title[^>]*>(.*?)</title>", h, re.S | re.I) or [None, ""])[1].strip(),
            "hits": hits[:3], "n_hits": len(hits), "links": links[:3], "bytes": len(h)}


FETCH = {"grep": grep, "arxiv": arxiv, "doi": crossref_doi, "xref": crossref_query, "openreview": openreview,
         "dblp": dblp, "isbn": isbn, "url": page}


def main():
    # Windows consoles default to cp1252; publisher records carry en dashes and accented names.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    keys = opts.get("only", "").split(",") if opts.get("only") else list(REGISTRY)
    results = {}
    for k in keys:
        results[k] = []
        for kind, val in REGISTRY[k]:
            rec = {"probe": kind, "value": val}
            try:
                rec["result"] = FETCH[kind](val)
            except Exception as ex:  # a missing record is a finding, not a crash
                rec["error"] = f"{type(ex).__name__}: {ex}"
            results[k].append(rec)
            time.sleep(0.4)
        print(f"\n=== {k}")
        for rec in results[k]:
            if "error" in rec:
                print(f"  [{rec['probe']}] {rec['value']} -> ERROR {rec['error']}")
                continue
            r = rec["result"]
            if rec["probe"] in ("xref", "dblp", "openreview"):
                for i, it in enumerate(r[:3]):
                    print(f"  [{rec['probe']}#{i}] " + json.dumps(it, ensure_ascii=False)[:600])
                if not r:
                    print(f"  [{rec['probe']}] {rec['value']} -> no hits")
            else:
                print(f"  [{rec['probe']}] {rec['value']} -> " + json.dumps(r, ensure_ascii=False)[:900])
    out = opts.get("out")
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        print(f"\nraw records -> {out}")


if __name__ == "__main__":
    main()
