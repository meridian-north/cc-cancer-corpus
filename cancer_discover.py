#!/usr/bin/env python3
"""
cancer_discover.py — aggressive, INTERNATIONAL sourcing for the cancer corpus,
straight from neutral authorities. No LLM in the sourcing loop = nothing to
hallucinate; every identifier comes back FROM the registry, already resolvable.

SOURCES (all public, open APIs, no key):
  * Europe PMC  — the international workhorse: indexes PubMed + PMC + preprints
                  (bioRxiv/medRxiv) + Chinese Biological Abstracts (CBA) + Asian
                  journals. Returns DOI/PMID/PMCID + isOpenAccess + open full-text URL.
  * ClinicalTrials.gov v2 — trials (US + many international), returns NCT ids.
  * Library of Congress  — gov/historical/regulatory documents (the delayed-harm +
                  industry-document classes), returns LCCN/item ids.

SAME RULES as the scraper: polite (rate-limited, identifying UA, robots-respecting
for non-API), public-only, pointer-first (every row carries a resolvable id), and
it emits a feedstock JSON the scraper then verifies + manifests. Discovery here,
verification there — two independent steps, by design.

Stdlib only. Examples:
  python3 cancer_discover.py --europepmc "pembrolizumab AND supplement" --n 25
  python3 cancer_discover.py --europepmc "curcumin cancer" --primary --n 30   # PRIMARY human studies
  python3 cancer_discover.py --trials "metformin cancer" --with-results --n 30 # trials + results digest
  python3 cancer_discover.py --loc "tobacco industry documents cancer" --n 15
  python3 cancer_discover.py --europepmc "fenbendazole cancer" --open-only --n 20
  python3 cancer_discover.py --selftest                                        # offline checks, no network
Output -> ~/cancer_intake/discovered_feedstock.json  (feed to cancer_kind_scraper.py --feedstock)
"""

import json, os, sys, time, urllib.request, urllib.parse, urllib.error

OUTPUT = os.path.expanduser("~/cancer_intake")
CONTACT_EMAIL = "jr.clawdbot@gmail.com"   # polite API contact; change if you want a different address
UA = f"GarrisonNode-KindDiscover/1.0 (cancer research; mailto:{CONTACT_EMAIL})"
DELAY = 2.0          # seconds between calls to the same host
TIMEOUT = 30
_last = {}

def _now(): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def _get(url):
    host = urllib.parse.urlparse(url).netloc
    w = DELAY - (time.time() - _last.get(host, 0))
    if w > 0: time.sleep(w)
    _last[host] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  ! fetch failed: {e}  ({url[:90]})")
        return None

# ---------------------------------------------------------------- evidence class
def classify_pubtype(it):
    """Map a Europe PMC core result to an evidence-bearing source_class so the why-filer's
    evidence axis can DISCRIMINATE (resultType=core carries pubTypeList). Without this every
    non-preprint hit was 'international_literature' (ev=3) and the anomaly score degenerated
    into pure citation rank. Specific-before-general: 'Systematic Review' / 'Meta-Analysis'
    must be tested before the generic 'Review'. Preprints keep their own low class.
    Imported by reclass_evidence.py — do not duplicate this logic (CLAUDE.md Karpathy #5)."""
    if it.get("source") == "PPR":
        return "preprint"
    pts = " ".join(it.get("pubTypeList", {}).get("pubType", []) or []).lower()
    title = (it.get("title") or "").lower()
    if "retract" in pts:
        return "retracted"
    if "meta-analysis" in pts or "meta analysis" in pts or "meta-analysis" in title:
        return "meta_analysis"
    if "systematic review" in pts or "systematic review" in title:
        return "systematic_review"
    if "randomized controlled trial" in pts or "randomised controlled trial" in pts:
        return "rct"
    if "clinical trial" in pts:
        return "clinical_trial"
    if "observational study" in pts or "comparative study" in pts or "cohort study" in pts:
        return "observational"
    if "case reports" in pts or "case report" in pts:
        return "case_report"
    if "review" in pts:                       # narrative review (systematic already caught above)
        return "narrative_review"
    if any(k in pts for k in ("editorial", "letter", "comment", "news", "biography")):
        return "commentary"
    return "international_literature"          # generic journal article — the conservative default

# ---------------------------------------------------------------- primary-evidence bias
# Sourcing rebalance (S217-followup, sovereign steer 2026-06-04): the corpus was ~1046 secondary-lit
# vs ~7 primary human studies. --primary ANDs the query with this pubType OR-filter so the index
# returns PRIMARY human evidence directly instead of waiting for reviews to surface it. Breadth-
# leaning per "as many sources as possible" — RCT/clinical-trial/observational/cohort/comparative/
# multicenter, NOT phase-gated. classify_pubtype() then sorts each hit into the evidence axis (these
# land in the why-filer's "primary" stratum). Verified live: PUB_TYPE:"Clinical Trial" → 379 curcumin
# hits (2026-06-04). The broad (non-primary) pass still runs alongside so reviews stay present for
# the review stratum — this filter ADDS primary, it does not remove reviews.
PRIMARY_PUBTYPES = ["randomized controlled trial", "clinical trial", "observational study",
                    "cohort studies", "comparative study", "multicenter study",
                    "pragmatic clinical trial"]

def primary_filter_clause():
    """Europe PMC boolean clause that biases a query toward primary human evidence."""
    return "(" + " OR ".join(f'PUB_TYPE:"{t}"' for t in PRIMARY_PUBTYPES) + ")"

# ---------------------------------------------------------------- Europe PMC
def europepmc(query, n=25, open_only=False, primary_only=False):
    """International index incl. Asian/Chinese journals + preprints. Returns rows with real ids.
    primary_only=True ANDs the pubType filter above so the index returns PRIMARY human studies.
    Run the broad pass (primary_only=False) alongside so reviews remain present for the why-filer."""
    effective = f"({query}) AND {primary_filter_clause()}" if primary_only else query
    via = "europepmc_primary" if primary_only else "europepmc"
    q = urllib.parse.quote(effective)
    url = (f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}"
           f"&format=json&pageSize={min(n,100)}&resultType=core")
    data = _get(url)
    rows = []
    if not data: return rows
    for it in data.get("resultList", {}).get("result", []):
        is_oa = it.get("isOpenAccess") == "Y"
        if open_only and not is_oa: continue
        doi = it.get("doi")
        pmid = it.get("pmid")
        # prefer an open full-text URL when available
        open_url = None
        for u in it.get("fullTextUrlList", {}).get("fullTextUrl", []):
            if u.get("availabilityCode") == "OA" or u.get("documentStyle") == "pdf":
                open_url = u.get("url"); break
        rows.append({
            "id": (f"epmc_{it.get('source','')}_{it.get('id','')}").lower(),
            "title": it.get("title"),
            "abstract": (it.get("abstractText") or "")[:8000],   # public/free — the 4W1H content
            "source_class": classify_pubtype(it),                # evidence-bearing (was a flat binary)
            "pub_types": it.get("pubTypeList", {}).get("pubType", []),  # raw EPMC tags, for audit/backfill
            "doi": doi,
            "pmid": pmid if not doi else None,
            "open_expected": is_oa,
            "open_url": open_url,
            "discovered_via": via,
            "pmcid": it.get("pmcid"),
            # OA full text is served under the PMC namespace, not MED — route there when a PMCID exists
            "epmc_source": ("PMC" if it.get("pmcid") else it.get("source")),
            "epmc_id": (it.get("pmcid") or it.get("id")),
            "journal": it.get("journalInfo", {}).get("journal", {}).get("title"),
            "year": it.get("pubYear"),
            "country_hint": it.get("source"),   # CBA=Chinese Biol Abstracts, MED=Medline, PPR=preprint
        })
    return rows

# ---------------------------------------------------------------- ClinicalTrials.gov v2
def trials(query, n=25, with_results=False):
    """ClinicalTrials.gov v2. Breadth-max: NOT phase-gated (sovereign steer 2026-06-04) — every
    study the term matches comes in as trial_registry presence (ev=4; the why-filer excludes
    trial_registry from attention scoring, so trials add primary-evidence presence without skewing
    the anomaly math). has_results arrives free in the listing; when with_results is set we pull a
    BOUNDED digest of posted outcomes for the subset that has them (see trial_results)."""
    q = urllib.parse.quote(query)
    url = (f"https://clinicaltrials.gov/api/v2/studies?query.term={q}&pageSize={min(n,100)}"
           f"&format=json&fields=NCTId,BriefTitle,Phase,OverallStatus,StudyType,HasResults")
    data = _get(url)
    rows = []
    if not data: return rows
    for s in data.get("studies", []):
        ps = s.get("protocolSection", {})
        idm = ps.get("identificationModule", {})
        dz = ps.get("designModule", {})
        stt = ps.get("statusModule", {})
        nct = idm.get("nctId")
        has_results = bool(s.get("hasResults"))
        row = {
            "id": (nct or "nct_unknown").lower(),
            "title": idm.get("briefTitle"),
            "source_class": "trial_registry",
            "nct": nct,
            "open_expected": False,
            "pointer": f"https://clinicaltrials.gov/study/{nct}" if nct else None,
            "discovered_via": "clinicaltrials_gov",
            "phase": ",".join(dz.get("phases", []) or []),
            "study_type": dz.get("studyType"),
            "status": stt.get("overallStatus"),
            "has_results": has_results,
        }
        if with_results and has_results and nct:
            row["results_digest"] = trial_results(nct)
        rows.append(row)
    return rows

def trial_results(nct):
    """Compact digest of a trial's POSTED results (opt-in via --with-results). We fetch the
    ResultsSection but store only a BOUNDED digest — outcome-measure titles + serious/other AE
    counts + participant-flow group count — NOT the full ~85KB payload (one trial's results ran
    ~85k chars in 2026-06-04 testing). Mechanism (How) comes from literature abstracts, not trial
    result tables, so this is light enrichment kept off the default path per the How>Why steer."""
    d = _get(f"https://clinicaltrials.gov/api/v2/studies/{nct}?fields=ResultsSection")
    if not d: return None
    rs = d.get("resultsSection", {}) or {}
    oms = (rs.get("outcomeMeasuresModule", {}) or {}).get("outcomeMeasures", []) or []
    ae = rs.get("adverseEventsModule", {}) or {}
    pf = rs.get("participantFlowModule", {}) or {}
    return {
        "outcome_measures": [(o.get("title") or "")[:160] for o in oms[:12]],
        "outcome_measure_count": len(oms),
        "serious_event_count": len(ae.get("seriousEvents", []) or []),
        "other_event_count": len(ae.get("otherEvents", []) or []),
        "flow_group_count": len(pf.get("groups", []) or []),
    }

# ---------------------------------------------------------------- Library of Congress
def loc(query, n=15):
    """Gov/historical/regulatory documents (delayed-harm + industry-document classes)."""
    q = urllib.parse.quote(query)
    url = f"https://www.loc.gov/search/?q={q}&fo=json&c={min(n,40)}"
    data = _get(url)
    rows = []
    if not data: return rows
    for r in (data.get("results") or [])[:n]:
        rows.append({
            "id": ("loc_" + str(r.get("id", "")).rsplit("/", 2)[-2:][0]).lower().replace("/", "_"),
            "title": (r.get("title") or "")[:200],
            "source_class": "gov_historical_document",
            "pointer": r.get("id") or (r.get("url") if isinstance(r.get("url"), str) else None),
            "open_expected": False,
            "discovered_via": "library_of_congress",
            "date": r.get("date"),
        })
    return rows

# ---------------------------------------------------------------- NCBI Bookshelf (open books)
def bookshelf(query, n=15):
    """Open-access books/chapters from NCBI Bookshelf (free full text). Returns rows."""
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    em = urllib.parse.quote(CONTACT_EMAIL)
    es = _get(f"{base}/esearch.fcgi?db=books&term={urllib.parse.quote(query)}"
              f"&retmode=json&retmax={min(n,30)}&email={em}&tool=garrison_discover")
    ids = (((es or {}).get("esearchresult") or {}).get("idlist")) or []
    rows = []
    if not ids:
        return rows
    summ = _get(f"{base}/esummary.fcgi?db=books&id={','.join(ids)}&retmode=json&email={em}&tool=garrison_discover")
    res = (summ or {}).get("result", {})
    for uid in res.get("uids", []):
        d = res.get(uid, {})
        acc = d.get("accession") or d.get("reportid")
        ptr = f"https://www.ncbi.nlm.nih.gov/books/{acc}/" if acc else f"https://www.ncbi.nlm.nih.gov/books/?term={urllib.parse.quote(query)}"
        rows.append({
            "id": f"book_{acc or uid}".lower(),
            "title": d.get("title"),
            "abstract": (d.get("booktitle") or "") + " — " + (d.get("title") or ""),
            "source_class": "open_book",
            "pointer": ptr,
            "open_expected": True,
            "discovered_via": "ncbi_bookshelf",
            "year": (d.get("pubdate") or "")[:4],
        })
    return rows

# ---------------------------------------------------------------- offline self-test
def _selftest():
    """Network-free sanity checks for the query-builders + evidence classifier. Run before a sweep
    to confirm the primary filter and pubType mapping are intact (no API, no writes)."""
    ok = True
    clause = primary_filter_clause()
    for pt in ("randomized controlled trial", "clinical trial", "observational study"):
        if f'PUB_TYPE:"{pt}"' not in clause:
            print(f"  FAIL: primary filter missing {pt!r}"); ok = False
    cases = {
        "rct":               {"pubTypeList": {"pubType": ["Randomized Controlled Trial", "Journal Article"]}},
        "clinical_trial":    {"pubTypeList": {"pubType": ["Clinical Trial"]}},
        "observational":     {"pubTypeList": {"pubType": ["Observational Study"]}},
        "meta_analysis":     {"pubTypeList": {"pubType": ["Meta-Analysis"]}},
        "systematic_review": {"pubTypeList": {"pubType": ["Systematic Review"]}},
        "narrative_review":  {"pubTypeList": {"pubType": ["Review", "Journal Article"]}},
        "retracted":         {"pubTypeList": {"pubType": ["Retracted Publication"]}},
        "preprint":          {"source": "PPR", "pubTypeList": {"pubType": ["Preprint"]}},
        "international_literature": {"pubTypeList": {"pubType": ["Journal Article"]}},
    }
    for expected, it in cases.items():
        got = classify_pubtype(it)
        mark = "ok " if got == expected else "FAIL"
        if got != expected: ok = False
        print(f"  [{mark}] classify_pubtype -> {got:24} (expected {expected})")
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1

# ---------------------------------------------------------------- main
def main():
    a = sys.argv
    if "--selftest" in a:
        sys.exit(_selftest())
    os.makedirs(OUTPUT, exist_ok=True)
    if CONTACT_EMAIL.startswith("SET_YOUR_EMAIL"):
        print("WARNING: set CONTACT_EMAIL at top — polite discovery identifies itself.")
    n = int(a[a.index("--n")+1]) if "--n" in a else 25
    open_only = "--open-only" in a
    primary = "--primary" in a
    with_results = "--with-results" in a
    rows = []
    if "--europepmc" in a:
        rows += europepmc(a[a.index("--europepmc")+1], n, open_only, primary)
    if "--trials" in a:
        rows += trials(a[a.index("--trials")+1], n, with_results)
    if "--loc" in a:
        rows += loc(a[a.index("--loc")+1], n)
    if "--bookshelf" in a:
        rows += bookshelf(a[a.index("--bookshelf")+1], n)
    if not rows:
        print("Usage: --europepmc '<q>' [--primary] | --trials '<q>' [--with-results] | --loc '<q>' "
              "| --bookshelf '<q>'  [--n N] [--open-only]   (or --selftest)")
        return
    # keep only rows that carry a resolvable identifier (doi/pmid/nct) — pointer-first
    keep = [r for r in rows if r.get("doi") or r.get("pmid") or r.get("nct") or r.get("pointer")]
    out = os.path.join(OUTPUT, "discovered_feedstock.json")
    with open(out, "w") as f:
        json.dump(keep, f, indent=2)
    oa = sum(1 for r in keep if r.get("open_expected"))
    print(f"[{_now()}] discovered {len(keep)} rows ({oa} open-access) -> {out}")
    print("Next: python3 cancer_kind_scraper.py --feedstock " + out + "  (verifies every id)")
    # quick country/source spread for the international view
    from collections import Counter
    spread = Counter(r.get("discovered_via") for r in keep)
    print("  spread:", dict(spread))

if __name__ == "__main__":
    main()
