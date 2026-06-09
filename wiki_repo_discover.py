#!/usr/bin/env python3
"""
wiki_repo_discover.py — source LEADS from public markdown knowledge bases.

The corpus's authority sources (Europe PMC, ClinicalTrials.gov, PubChem) are verified-at-
authority. This tool reaches a DIFFERENT, LOWER-TRUST tier: public *markdown repositories*
on GitHub — herbal wikis, phytochemistry digital gardens, integrative-oncology docs sites
(mkdocs/docusaurus/obsidian-published). These are the "web md / wiki md opensource freebies."

DOCTRINE — read before trusting anything this emits:
  1. These are LEADS, not authorities. A community wiki saying "herb X cures Y" is a
     pointer to CHECK, never evidence. Lowest trust tier (source_class=community_markdown_repo).
  2. Every factual claim found inside a lead (a DOI / PMID / NCT / compound / dose) must be
     RE-VERIFIED at its authority (Crossref / Europe PMC / ClinicalTrials.gov / PubChem)
     before it enters the verified corpus. Same verify-don't-trust rule as everywhere else.
  3. LICENSE-GATED. Only OPEN-licensed repos may have content ingested. null / unknown /
     no-license-file repos are POINTER_ONLY — link to them, never copy their text.
  4. POINTER-FIRST. This tool fetches metadata + license ONLY. It does NOT pull repo content
     in the discovery loop — nothing for an LLM to hallucinate, and no license violation.
  5. CONTRADICTIONS SURFACE. Where a lead's claim disagrees with the verified literature,
     that disagreement is the *signal* (feed it to the why-filer / bridge as a contradiction
     candidate) — but the wiki claim itself never counts as evidence.

Stdlib only. Unauthenticated GitHub search = 10 req/min; set GITHUB_TOKEN for 30/min.
Examples:
  python3 wiki_repo_discover.py                      # run the default query set
  python3 wiki_repo_discover.py --min-stars 5        # filter low-signal repos
  python3 wiki_repo_discover.py --open-only          # drop pointer-only (no usable license)
  python3 wiki_repo_discover.py --no-filter          # disable the v2 CV-noise filter (see everything)
Output -> ~/cancer_intake/wiki_repos_candidates.json
"""

import json, os, sys, time, urllib.request, urllib.parse

INTAKE = os.path.expanduser("~/cancer_intake")
OUT = os.path.join(INTAKE, "wiki_repos_candidates.json")
API = "https://api.github.com/search/repositories"

# Domain queries. GitHub repo search matches name/description/README/topics — so query the
# SUBJECT, not the word "markdown" (that returns ~0). The md-site bias is applied via topics
# below. Keep terms broad; curation happens after, by a human reading the leads.
QUERIES = [
    # herbal / ethnobotanical knowledge bases
    "materia medica", "herbal medicine", "medicinal plants", "ethnobotany",
    "herbalism", "phytochemistry", "phytochemical database",
    # mechanism / oncology integrative
    "integrative oncology", "anticancer natural products", "cancer mechanism of action",
    "natural compound cancer", "repurposed drugs cancer",
    # the component themes the project is deepening
    "terpene pharmacology", "cannabinoid cancer", "polyphenol cancer",
    # herb-drug interaction (the safety keystone)
    "herb drug interaction", "cytochrome p450 herb interaction",
]
# md-site / wiki signals appended as a GitHub topic qualifier to bias toward markdown bases.
MD_TOPICS = ["mkdocs", "docusaurus", "digital-garden", "obsidian", "wiki", "knowledge-base"]

# License classes. OPEN = content may be ingested (with attribution per the license).
# POINTER_ONLY = link only (no usable license / unknown).
OPEN_LICENSES = {
    "CC0-1.0", "CC-BY-4.0", "CC-BY-SA-4.0", "MIT", "Apache-2.0", "BSD-2-Clause",
    "BSD-3-Clause", "MPL-2.0", "Unlicense", "GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-3.0",
}

# v2 relevance filter (S-2026-06-04). First run showed the repo axis is FLOODED with
# leaf-photo CLASSIFIERS that match herbal keywords but carry zero mechanism text
# (~35 of 40 leads). Drop CV/ML-identification noise; bias toward actual knowledge bases.
# A repo is dropped only if it hits a NEGATIVE term and NO POSITIVE term, so a genuine
# "drug-target interaction database" that happens to mention "detection" still survives.
NEGATIVE = [
    "image", "classif", "detection", "identif", "recognition", "cnn", "vgg", "resnet",
    "deep-learning", "deep learning", "leaf", "front-end", "frontend", "yolo",
    "segmentation", "transfer-learning", "image-processing", "image processing",
]
POSITIVE = [
    "database", "atlas", "phytochem", "compound", "interaction", "knowledge",
    "pharmacolog", "mechanism", "materia medica", "ethnobotan", "natural-product",
    "natural product", "moa", "target", "ontology", "corpus", "wiki", "metabolite",
]

def gh_search(q, per_page=15):
    url = API + "?" + urllib.parse.urlencode({"q": q, "sort": "stars", "per_page": per_page})
    headers = {"User-Agent": "GarrisonNode-WikiRepoDiscover/1.0",
               "Accept": "application/vnd.github+json"}
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        headers["Authorization"] = "Bearer " + tok
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r).get("items", [])
    except Exception as e:
        print(f"  ! query failed ({q!r}): {e}", file=sys.stderr)
        return []

def classify(item):
    lic = (item.get("license") or {}).get("spdx_id")
    open_ok = bool(lic) and lic in OPEN_LICENSES
    return {
        "id": item.get("full_name"),
        "pointer": item.get("html_url"),
        "description": (item.get("description") or "")[:300],
        "stars": item.get("stargazers_count", 0),
        "license": lic,                              # may be None
        "ingestible": open_ok,                       # license gate
        "access": "OPEN" if open_ok else "POINTER_ONLY",
        "default_branch": item.get("default_branch"),
        "topics": item.get("topics") or [],
        "language": item.get("language"),
        "pushed_at": item.get("pushed_at"),
        "archived": item.get("archived", False),
        "source_class": "community_markdown_repo",
        "trust": "LEAD",                             # lowest tier — re-verify every claim
        "verify_rule": "resolve every DOI/PMID/NCT/CID found inside at its authority before use",
    }

def main():
    a = sys.argv
    min_stars = int(a[a.index("--min-stars") + 1]) if "--min-stars" in a else 0
    open_only = "--open-only" in a
    os.makedirs(INTAKE, exist_ok=True)

    queries = list(QUERIES)
    # add a few md-site-biased variants (topic qualifier) for the strongest domain terms
    for base in ["herbal medicine", "integrative oncology", "phytochemistry"]:
        for t in MD_TOPICS[:3]:
            queries.append(f"{base} topic:{t}")

    seen, rows = {}, []
    for i, q in enumerate(queries):
        items = gh_search(q)
        for it in items:
            fn = it.get("full_name")
            if not fn or fn in seen:
                continue
            rec = classify(it)
            text = (rec["id"] + " " + (rec["description"] or "") + " " + " ".join(rec["topics"])).lower()
            neg = any(n in text for n in NEGATIVE)
            pos = sum(1 for p in POSITIVE if p in text)
            rec["relevance"] = pos
            # drop CV/identification noise unless a real knowledge-base signal is also present
            if "--no-filter" not in a and neg and pos == 0:
                continue
            if rec["stars"] < min_stars:
                continue
            if open_only and not rec["ingestible"]:
                continue
            if rec["archived"]:
                rec["note"] = "archived — stale lead"
            seen[fn] = rec
            rows.append(rec)
        # politeness / rate limit (10/min unauth, 30/min with token)
        time.sleep(2.2 if os.environ.get("GITHUB_TOKEN") else 6.5)

    rows.sort(key=lambda r: (-int(r["ingestible"]), -r.get("relevance", 0), -r["stars"]))
    doc = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "doctrine": "LEADS not authorities; license-gated; pointer-first; re-verify every claim at its authority; disagreements feed the contradictions surface.",
        "queries_run": len(queries),
        "candidates": len(rows),
        "ingestible_open": sum(1 for r in rows if r["ingestible"]),
        "pointer_only": sum(1 for r in rows if not r["ingestible"]),
        "leads": rows,
    }
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=2)

    print(f"\n=== wiki/web markdown repo LEADS ===  -> {OUT}")
    print(f"  candidates: {len(rows)}  |  open/ingestible: {doc['ingestible_open']}  |  pointer-only: {doc['pointer_only']}")
    for r in rows[:30]:
        flag = "OPEN " if r["ingestible"] else "ptr  "
        lic = r["license"] or "no-license"
        print(f"  [{flag}] rel{r.get('relevance',0):<2} {r['stars']:5}★  {lic:13}  {r['id']}")
    print("\nReminder: these are LEADS. Re-verify every DOI/PMID/NCT/compound at its authority")
    print("before anything here enters the verified corpus. License-gated content only.")

if __name__ == "__main__":
    main()
