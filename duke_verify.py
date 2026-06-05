#!/usr/bin/env python3
"""
duke_verify.py — resolve Dr. Duke's staged leads to verified structural identity.

INPUT:  ~/cancer_intake/duke_candidates.json  (from duke_ingest.py)
DOES:   for each DISTINCT anticancer chemical, resolve it to a PubChem CID — the
        internationally-recognized structural identifier (and citation anchor). This is
        the first, bounded verification step: it confirms the compound is REAL and gives
        it a standard handle, before any study-level claim is checked.

THE FIXES that tonight's run surfaced:
  - CAS reformat: Duke stores CAS unhyphenated ("6216826"); PubChem wants "6216-82-6".
    We reformat to the standard {prefix}-{2}-{check} before lookup.
  - name fallback: many rows have no CAS — fall back to a cleaned name lookup.
  - single retry on transient (the "ivermectin -> None" was a transient timeout, not a
    real miss — one backoff retry catches it).

OUTPUTS:
  ~/cancer_intake/duke_resolved.json   chem -> CID + pubchem_url + activities + refs (resolved flag)
  ~/cancer_intake/duke_queries.txt     "<chem> cancer mechanism" per resolved compound,
                                        feedstock for the EXISTING sweep (reuse, don't rewrite):
                                          run_corpus_sweep.sh / cancer_kind_scraper.py
                                        That second pass pulls + verifies actual STUDIES.

DOCTRINE: a CID confirms the molecule, not the anticancer claim. The claim is verified in
the study pass (CID -> linked literature -> Europe PMC). Documentation, not endorsement.
CC0 source; cite DOI 10.15482/USDA.ADC/1239279.

Stdlib only. PubChem PUG-REST allows ~5 req/sec; we sleep 0.25s and stay polite.
Usage:
  python3 duke_verify.py                 # resolve all distinct anticancer chems
  python3 duke_verify.py --limit 50      # quick test
  python3 duke_verify.py --include-procancer   # also resolve the safety-flag set
"""

import json, os, re, sys, time, urllib.request, urllib.parse

INTAKE = os.path.expanduser("~/cancer_intake")
IN = os.path.join(INTAKE, "duke_candidates.json")
OUT = os.path.join(INTAKE, "duke_resolved.json")
QOUT = os.path.join(INTAKE, "duke_queries.txt")
PUG = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound"

def cas_standard(raw):
    """Duke CASNUM (unhyphenated digits, maybe float) -> standard CAS 'NNNNNNN-NN-N'."""
    if not raw:
        return None
    d = re.sub(r"\D", "", str(raw).split(".")[0])
    if len(d) < 5 or len(d) > 10:
        return None
    return f"{d[:-3]}-{d[-3:-1]}-{d[-1]}"

def clean_name(chem):
    """Duke names are UPPERCASE with stereo prefixes; PubChem tolerates most. Light touch."""
    n = chem.strip()
    return n

def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "GarrisonNode-DukeVerify/1.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def cid_from(endpoint_value, kind):
    """kind: 'name' -> /name/<v>/cids/JSON ; resolves CAS via the name endpoint too."""
    url = f"{PUG}/{kind}/" + urllib.parse.quote(endpoint_value) + "/cids/JSON"
    for attempt in (1, 2):
        try:
            data = _get(url)
            cids = data.get("IdentifierList", {}).get("CID", [])
            return cids[0] if cids else None
        except Exception:
            if attempt == 1:
                time.sleep(1.5)   # one backoff retry — catches transient timeouts
            else:
                return None

def resolve(chem, cas):
    # try CAS (hyphenated) first via the name endpoint, then the chemical name
    cas_std = cas_standard(cas)
    if cas_std:
        cid = cid_from(cas_std, "name")
        if cid:
            return cid, cas_std, "cas"
    cid = cid_from(clean_name(chem), "name")
    if cid:
        return cid, cas_std, "name"
    return None, cas_std, None

def main():
    a = sys.argv
    limit = int(a[a.index("--limit") + 1]) if "--limit" in a else None
    include_pro = "--include-procancer" in a
    if not os.path.exists(IN):
        print(f"Missing {IN}. Run duke_ingest.py first."); return
    with open(IN) as f:
        doc = json.load(f)

    # aggregate rows -> per-distinct-chem (collect activities + a CAS if any row has one)
    agg = {}
    rows = list(doc.get("anticancer_leads", []))
    if include_pro:
        rows += list(doc.get("procancer_safety_flags", []))
    for r in rows:
        key = r["chem"].upper()
        e = agg.setdefault(key, {"chem": r["chem"], "cas": None, "activities": set(), "refs": set()})
        e["activities"].add(r.get("activity"))
        if r.get("cas") and not e["cas"]:
            e["cas"] = r["cas"]
        if r.get("reference"):
            e["refs"].add(r["reference"])

    chems = list(agg.values())
    if limit:
        chems = chems[:limit]

    resolved, unresolved = [], []
    t0 = time.time()
    for i, e in enumerate(chems, 1):
        cid, cas_std, via = resolve(e["chem"], e["cas"])
        rec = {
            "chem": e["chem"],
            "cid": cid,
            "pubchem_url": f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}" if cid else None,
            "cas_standard": cas_std,
            "resolved_via": via,
            "activities": sorted(x for x in e["activities"] if x),
            "n_refs": len(e["refs"]),
        }
        (resolved if cid else unresolved).append(rec)
        if i % 50 == 0:
            print(f"  ... {i}/{len(chems)}  resolved={len(resolved)}  ({time.time()-t0:.0f}s)")
        time.sleep(0.25)   # PubChem politeness

    out = {
        "source": "Dr. Duke's (USDA, CC0, DOI 10.15482/USDA.ADC/1239279)",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "doctrine": "CID confirms the molecule, not the anticancer claim; the claim is verified in the study pass.",
        "counts": {"input_chems": len(chems), "resolved": len(resolved), "unresolved": len(unresolved)},
        "resolved": sorted(resolved, key=lambda x: x["chem"]),
        "unresolved": sorted(unresolved, key=lambda x: x["chem"]),
    }
    os.makedirs(INTAKE, exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)

    # emit study-pass feedstock for the EXISTING sweep (one query per resolved compound)
    with open(QOUT, "w") as f:
        f.write("# Duke-derived study queries — resolved compounds only. Feed to the existing\n")
        f.write("# sweep (run_corpus_sweep.sh / cancer_kind_scraper.py). Re-verify every hit.\n")
        for r in out["resolved"]:
            f.write(f"{r['chem']} cancer mechanism\n")

    print(f"\n=== Duke verify ===  -> {OUT}")
    print(f"  input chems : {len(chems)}")
    print(f"  resolved    : {len(resolved)}  (to PubChem CID)")
    print(f"  unresolved  : {len(unresolved)}  (obscure/odd names — kept for manual review)")
    print(f"  study queries written -> {QOUT}  ({len(out['resolved'])} lines)")
    print("\nNext (the long study pass — reuse the existing sweep):")
    print(f"  cp {QOUT} <sweep agent list>  # or point run_corpus_sweep.sh at it")
    print("Each study hit is re-verified at Europe PMC. CC0; cite the DOI.")

if __name__ == "__main__":
    main()
