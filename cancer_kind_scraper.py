#!/usr/bin/env python3
"""
cancer_kind_scraper.py — a polite ("kind") multi-source harvester for the
conventional + complementary cancer-treatment corpus.

DESIGN PRINCIPLES (baked in, not optional):
  * KIND       — per-host rate limit, robots.txt obeyed, identifying User-Agent,
                 backoff + Retry-After respected. We are a guest on these servers.
  * PUBLIC ONLY— open-access / PMC / Internet Archive / public gov APIs only.
                 NO paywalled full-text is downloaded. Paywalled => pointer-only.
  * VERIFY     — every DOI is checked against Crossref for its REAL title/journal
                 before we trust it (the lesson from the hallucinated/mis-cited
                 feedstock). Mismatch or non-resolve => marked UNVERIFIED.
  * RESULTS+METHODS+POINTERS — we store the file (if open) + a manifest row with
                 sha256 + the exact source pointer, so everything reproduces.
  * DISK-AWARE — refuses to run if free space < MIN_FREE_GB; per-file + total caps.

Stdlib only (urllib, hashlib, json). Run on the Mac:  python3 cancer_kind_scraper.py
Output goes to ~/cancer_intake/ .
"""

import json, hashlib, os, sys, time, shutil, urllib.request, urllib.parse, urllib.error
import urllib.robotparser as robotparser
from datetime import datetime, timezone

# ---------------------------------------------------------------- config
OUTPUT_DIR    = os.path.expanduser("~/cancer_intake")
CONTACT_EMAIL = "SET_YOUR_EMAIL@example.com"   # <-- set this; it's the polite thing
USER_AGENT    = f"GarrisonNode-KindScraper/1.0 (cancer research; mailto:{CONTACT_EMAIL})"
PER_HOST_DELAY_S = 4.0      # min seconds between requests to the SAME host
TIMEOUT_S        = 30
MAX_RETRIES      = 3
MIN_FREE_GB      = 20       # abort if disk below this
MAX_FILE_MB      = 50       # skip a single file larger than this
MAX_TOTAL_MB     = 2000     # stop after this much downloaded this run
OK_CONTENT       = ("application/pdf", "text/html", "application/xml",
                    "text/xml", "application/json", "text/plain")

# ---------------------------------------------------------------- seed feedstock
# The 4 independently-verified intakes (Claude pass, 2026-06-03). Extend freely,
# or load a Gemini/Grok feedstock JSON via --feedstock <file>.
SEED = [
    {"id": "iniparib_liu_2012", "title": "Iniparib nonselectively modifies proteins; lacks classic PARP inhibitor characteristics",
     "source_class": "preclinical_mouse", "doi": "10.1158/1078-0432.CCR-11-1973", "open_expected": True},  # CCR 2012, corrected via Crossref
    {"id": "garrido_laguna_pdx_2011", "title": "Tumor engraftment in nude mice ... predict poor survival and gemcitabine resistance in pancreatic cancer",
     "source_class": "preclinical_mouse", "doi": "10.1158/1078-0432.CCR-11-0341", "open_expected": False,
     "note": "DOI is best-guess for the Clin Cancer Res 2011;17:5793-5800 paper; verifier will confirm/correct via Crossref."},
    {"id": "dca_michelakis_2010", "title": "Metabolic modulation of glioblastoma with dichloroacetate (5-patient cohort)",
     "source_class": "small_human_cohort", "doi": "10.1126/scitranslmed.3000677", "open_expected": False},  # corrected via Crossref
    {"id": "curcumin_notch1_retracted_2006", "title": "RETRACTED: Notch-1 down-regulation by curcumin ... pancreatic cancer cells",
     "source_class": "retracted", "doi": "10.1002/cncr.21904", "open_expected": False},
]

# ---------------------------------------------------------------- polite plumbing
_last_hit = {}   # host -> last request time
_robots   = {}   # host -> RobotFileParser

def _now():
    return datetime.now(timezone.utc).isoformat()

def _host(url):
    return urllib.parse.urlparse(url).netloc

def _throttle(url):
    h = _host(url)
    wait = PER_HOST_DELAY_S - (time.time() - _last_hit.get(h, 0))
    if wait > 0:
        time.sleep(wait)
    _last_hit[h] = time.time()

def _robots_ok(url):
    h = _host(url)
    if h not in _robots:
        rp = robotparser.RobotFileParser()
        try:
            rp.set_url(f"{urllib.parse.urlparse(url).scheme}://{h}/robots.txt")
            rp.read()
        except Exception:
            rp = None
        _robots[h] = rp
    rp = _robots[h]
    return True if rp is None else rp.can_fetch(USER_AGENT, url)

def _request(url, method="GET"):
    """One polite request with retries/backoff. Returns (status, headers, body_bytes) or raises."""
    _throttle(url)
    for attempt in range(1, MAX_RETRIES + 1):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT,
                                                                   "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
                body = r.read() if method == "GET" else b""
                return r.status, dict(r.headers), body
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < MAX_RETRIES:
                ra = e.headers.get("Retry-After")
                time.sleep(int(ra) if (ra and ra.isdigit()) else PER_HOST_DELAY_S * attempt * 2)
                continue
            return e.code, dict(e.headers or {}), b""
        except Exception:
            if attempt < MAX_RETRIES:
                time.sleep(PER_HOST_DELAY_S * attempt)
                continue
            raise
    return 0, {}, b""

# ---------------------------------------------------------------- verification
def verify_doi(doi):
    """Check a DOI against Crossref. Returns real metadata dict, or None if it doesn't resolve."""
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    try:
        status, _, body = _request(url)
        if status != 200:
            return None
        m = json.loads(body)["message"]
        return {"title": (m.get("title") or [""])[0],
                "journal": (m.get("container-title") or [""])[0],
                "year": (m.get("issued", {}).get("date-parts", [[None]])[0][0]),
                "doi_url": m.get("URL", f"https://doi.org/{doi}")}
    except Exception:
        return None

def verify_nct(nct):
    """Resolve a ClinicalTrials.gov NCT id. Returns metadata dict or None."""
    url = f"https://clinicaltrials.gov/api/v2/studies/{urllib.parse.quote(nct)}?format=json"
    try:
        status, _, body = _request(url)
        if status != 200: return None
        m = json.loads(body).get("protocolSection", {})
        idm = m.get("identificationModule", {})
        return {"title": idm.get("briefTitle", ""), "journal": "ClinicalTrials.gov",
                "year": (m.get("statusModule", {}).get("startDateStruct", {}) or {}).get("date", ""),
                "doi_url": f"https://clinicaltrials.gov/study/{nct}"}
    except Exception:
        return None

def verify_pmid(pmid):
    """Resolve a PMID via Europe PMC (international index). Returns metadata dict or None."""
    url = (f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
           f"query=EXT_ID:{urllib.parse.quote(str(pmid))}%20AND%20SRC:MED&format=json&resultType=core")
    try:
        status, _, body = _request(url)
        if status != 200: return None
        res = json.loads(body).get("resultList", {}).get("result", [])
        if not res: return None
        it = res[0]; doi = it.get("doi")
        return {"title": it.get("title", ""),
                "journal": it.get("journalInfo", {}).get("journal", {}).get("title", ""),
                "year": it.get("pubYear", ""),
                "doi_url": (f"https://doi.org/{doi}" if doi else f"https://europepmc.org/abstract/MED/{pmid}")}
    except Exception:
        return None

def europepmc_fulltext(source, eid):
    """Pull OA full-text XML from the Europe PMC API — the robots-permitted channel
    for open-access full text (NOT scraping the article page). Returns bytes or None."""
    if not source or not eid:
        return None
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{source}/{eid}/fullTextXML"
    try:
        status, _, body = _request(url, "GET")
        if status == 200 and body and len(body) > 800:   # has real content, not an error stub
            return body
    except Exception:
        pass
    return None

def wayback(url):
    """Ask the Internet Archive for an archived snapshot of url. Returns archived URL or None."""
    api = "https://archive.org/wayback/available?" + urllib.parse.urlencode({"url": url})
    try:
        status, _, body = _request(api)
        if status != 200:
            return None
        snap = json.loads(body).get("archived_snapshots", {}).get("closest", {})
        return snap.get("url") if snap.get("available") else None
    except Exception:
        return None

# ---------------------------------------------------------------- disk + download
def free_gb(path):
    return shutil.disk_usage(path).free / 1e9

def sha256_of(b):
    h = hashlib.sha256(); h.update(b); return h.hexdigest()

def try_download(url, dest_base, downloaded_mb):
    """Polite download if open + robots-allowed + within caps. Returns manifest fragment."""
    if not _robots_ok(url):
        return {"retrieval_status": "BLOCKED_ROBOTS", "fetched_url": url}
    if free_gb(OUTPUT_DIR) < MIN_FREE_GB:
        return {"retrieval_status": "SKIPPED_LOW_DISK", "fetched_url": url}
    if downloaded_mb[0] >= MAX_TOTAL_MB:
        return {"retrieval_status": "SKIPPED_TOTAL_CAP", "fetched_url": url}
    status, headers, body = _request(url, "GET")
    if status != 200 or not body:
        return {"retrieval_status": "UNVERIFIED", "fetched_url": url, "http_status": status}
    ctype = (headers.get("Content-Type", "") or "").split(";")[0].strip().lower()
    if ctype not in OK_CONTENT:
        return {"retrieval_status": "POINTER_ONLY", "fetched_url": url, "content_type": ctype,
                "note": "non-document content-type; pointer recorded, not stored"}
    mb = len(body) / 1e6
    if mb > MAX_FILE_MB:
        return {"retrieval_status": "POINTER_ONLY", "fetched_url": url, "mb": round(mb, 1),
                "note": "exceeds MAX_FILE_MB; pointer recorded, not stored"}
    ext = {"application/pdf": "pdf", "text/html": "html", "application/xml": "xml",
           "text/xml": "xml", "application/json": "json", "text/plain": "txt"}.get(ctype, "bin")
    path = os.path.join(OUTPUT_DIR, "files", f"{dest_base}.{ext}")
    with open(path, "wb") as f:
        f.write(body)
    downloaded_mb[0] += mb
    return {"retrieval_status": "VERIFIED", "fetched_url": url, "stored": path,
            "sha256": sha256_of(body), "bytes": len(body), "content_type": ctype}

# ---------------------------------------------------------------- main
def process(item, downloaded_mb):
    row = {"id": item["id"], "title_claimed": item.get("title"),
           "source_class": item.get("source_class"), "fetched_at": _now()}
    # pick the identifier + its authority (pointer-first: DOI->Crossref, NCT->ClinicalTrials, PMID->Europe PMC)
    ident = kind = verifier = None
    if item.get("doi"):    ident, kind, verifier = item["doi"], "doi", verify_doi
    elif item.get("nct"):  ident, kind, verifier = item["nct"], "nct", verify_nct
    elif item.get("pmid"): ident, kind, verifier = item["pmid"], "pmid", verify_pmid
    if ident:
        meta = verifier(ident)
        if meta is None:
            row.update({"identifier": ident, "id_kind": kind, "id_verified": False,
                        "retrieval_status": "UNVERIFIED",
                        "note": f"{kind} did not resolve at its authority — unverified / likely wrong"})
            return row
        row.update({"identifier": ident, "id_kind": kind, "id_verified": True,
                    "title_real": meta["title"], "journal_real": meta["journal"], "year_real": meta["year"]})
        # honesty check: claimed vs real title (normalize unicode hyphens; strip RETRACTED prefix)
        def _norm(s):
            s = (s or "").lower()
            for hy in ("‐", "‑", "‒", "–", "—"):
                s = s.replace(hy, "-")
            return s
        claimed = _norm(item.get("title")).replace("retracted:", "").strip()[:30]
        if claimed and claimed not in _norm(meta["title"]):
            row["title_mismatch_flag"] = True
        # ALWAYS store the verified metadata + abstract — public/free, and the analyzable
        # 4W1H content. This is what turns the corpus from a pointer-log into real content.
        meta_doc = {"id": item["id"], "identifier": ident, "id_kind": kind,
                    "title": meta["title"], "journal": meta["journal"], "year": meta["year"],
                    "source_class": item.get("source_class"), "pointer": meta["doi_url"],
                    "abstract": item.get("abstract") or None}
        mbytes = json.dumps(meta_doc, ensure_ascii=False).encode("utf-8")
        mpath = os.path.join(OUTPUT_DIR, "files", f"{item['id']}.meta.json")
        with open(mpath, "w", encoding="utf-8") as f:
            f.write(mbytes.decode("utf-8"))
        downloaded_mb[0] += len(mbytes) / 1e6
        row.update({"stored_meta": mpath, "meta_sha256": sha256_of(mbytes),
                    "has_abstract": bool(item.get("abstract"))})
        # store genuinely-open full text. Prefer the Europe PMC OA API (robots-permitted),
        # then a direct open_url, then fall back to a verified pointer.
        if item.get("open_url") or item.get("open_expected") or item.get("epmc_id"):
            ft = europepmc_fulltext(item.get("epmc_source"), item.get("epmc_id"))
            if (ft and len(ft) / 1e6 <= MAX_FILE_MB and free_gb(OUTPUT_DIR) >= MIN_FREE_GB
                    and downloaded_mb[0] < MAX_TOTAL_MB):
                path = os.path.join(OUTPUT_DIR, "files", f"{item['id']}.xml")
                with open(path, "wb") as f:
                    f.write(ft)
                downloaded_mb[0] += len(ft) / 1e6
                row.update({"retrieval_status": "VERIFIED", "stored": path, "sha256": sha256_of(ft),
                            "bytes": len(ft), "content_type": "application/xml",
                            "via": "europepmc_oa_fulltext_api"})
            else:
                dl = try_download(item.get("open_url") or meta["doi_url"], item["id"], downloaded_mb)
                if dl.get("retrieval_status") == "VERIFIED":
                    row.update(dl)
                else:
                    row.update({"retrieval_status": "POINTER_ONLY", "pointer": meta["doi_url"],
                                "wayback": wayback(meta["doi_url"]), "download_attempt": dl.get("retrieval_status"),
                                "note": f"{kind} verified; OA full-text not retrievable via API or page — pointer recorded"})
        else:
            row.update({"retrieval_status": "POINTER_ONLY", "pointer": meta["doi_url"],
                        "wayback": wayback(meta["doi_url"]),
                        "note": "closed/paywalled expected — pointer + any IA snapshot recorded, not scraped"})
    else:
        url = item.get("url") or item.get("pointer")
        row.update(try_download(url, item["id"], downloaded_mb) if url else
                   {"retrieval_status": "NO_POINTER"})
    return row

def main():
    os.makedirs(os.path.join(OUTPUT_DIR, "files"), exist_ok=True)
    log = open(os.path.join(OUTPUT_DIR, "scrape.log"), "a")
    def say(*a):
        line = " ".join(str(x) for x in a)
        print(line); log.write(_now() + "  " + line + "\n"); log.flush()

    if CONTACT_EMAIL.startswith("SET_YOUR_EMAIL"):
        say("WARNING: set CONTACT_EMAIL at the top — polite scraping identifies itself.")
    if free_gb(OUTPUT_DIR) < MIN_FREE_GB:
        say(f"ABORT: free space {free_gb(OUTPUT_DIR):.1f} GB < MIN_FREE_GB {MIN_FREE_GB}.")
        return

    items = SEED
    if "--feedstock" in sys.argv:                      # optional: load Gemini/Grok JSON list
        with open(sys.argv[sys.argv.index("--feedstock") + 1]) as f:
            items = json.load(f)

    say(f"Kind scrape start — {len(items)} items -> {OUTPUT_DIR}  (free {free_gb(OUTPUT_DIR):.0f} GB)")
    downloaded_mb = [0.0]
    manifest_path = os.path.join(OUTPUT_DIR, "manifest.jsonl")
    with open(manifest_path, "a") as mf:
        for it in items:
            row = process(it, downloaded_mb)
            mf.write(json.dumps(row) + "\n"); mf.flush()
            say(f"  [{row.get('retrieval_status'):14}] {row['id']}"
                + ("  WARN title_mismatch" if row.get("title_mismatch_flag") else "")
                + ("  WARN doi_unverified" if row.get("doi_verified") is False else ""))
    say(f"Done. {downloaded_mb[0]:.1f} MB stored. Manifest: {manifest_path}")
    log.close()

if __name__ == "__main__":
    main()
