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
  python3 cancer_discover.py --trials "pancreatic cancer KRAS" --n 25
  python3 cancer_discover.py --loc "tobacco industry documents cancer" --n 15
  python3 cancer_discover.py --europepmc "fenbendazole cancer" --open-only --n 20
Output -> ~/cancer_intake/discovered_feedstock.json  (feed to cancer_kind_scraper.py --feedstock)
"""

import json, os, sys, time, urllib.request, urllib.parse, urllib.error

OUTPUT = os.path.expanduser("~/cancer_intake")
CONTACT_EMAIL = "SET_YOUR_EMAIL@example.com"   # <-- set this (polite)
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

# ---------------------------------------------------------------- Europe PMC
def europepmc(query, n=25, open_only=False):
    """International index incl. Asian/Chinese journals + preprints. Returns rows with real ids."""
    q = urllib.parse.quote(query)
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
            "source_class": "preprint" if it.get("source") == "PPR" else "international_literature",
            "doi": doi,
            "pmid": pmid if not doi else None,
            "open_expected": is_oa,
            "open_url": open_url,
            "discovered_via": "europepmc",
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
def trials(query, n=25):
    q = urllib.parse.quote(query)
    url = f"https://clinicaltrials.gov/api/v2/studies?query.term={q}&pageSize={min(n,100)}&format=json"
    data = _get(url)
    rows = []
    if not data: return rows
    for s in data.get("studies", []):
        idm = s.get("protocolSection", {}).get("identificationModule", {})
        dz = s.get("protocolSection", {}).get("designModule", {})
        stt = s.get("protocolSection", {}).get("statusModule", {})
        nct = idm.get("nctId")
        rows.append({
            "id": (nct or "nct_unknown").lower(),
            "title": idm.get("briefTitle"),
            "source_class": "trial_registry",
            "nct": nct,
            "open_expected": False,
            "pointer": f"https://clinicaltrials.gov/study/{nct}" if nct else None,
            "discovered_via": "clinicaltrials_gov",
            "phase": ",".join(dz.get("phases", []) or []),
            "status": stt.get("overallStatus"),
        })
    return rows

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

# ---------------------------------------------------------------- main
def main():
    os.makedirs(OUTPUT, exist_ok=True)
    if CONTACT_EMAIL.startswith("SET_YOUR_EMAIL"):
        print("WARNING: set CONTACT_EMAIL at top — polite discovery identifies itself.")
    a = sys.argv
    n = int(a[a.index("--n")+1]) if "--n" in a else 25
    open_only = "--open-only" in a
    rows = []
    if "--europepmc" in a:
        rows += europepmc(a[a.index("--europepmc")+1], n, open_only)
    if "--trials" in a:
        rows += trials(a[a.index("--trials")+1], n)
    if "--loc" in a:
        rows += loc(a[a.index("--loc")+1], n)
    if not rows:
        print("Usage: --europepmc '<q>' | --trials '<q>' | --loc '<q>'  [--n N] [--open-only]")
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
