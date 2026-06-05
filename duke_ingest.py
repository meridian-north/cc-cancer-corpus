#!/usr/bin/env python3
"""
duke_ingest.py — Dr. Duke's Phytochemical & Ethnobotanical Database -> cancer leads.

SOURCE (clears the ReciprocalSovereigntySourcingMt admissibility bar cleanly):
  - Dr. Duke's Phytochemical and Ethnobotanical Databases, USDA ARS.
  - License: CC0 (public domain dedication) — honorable acquisition, no terms gate.
  - Citable: DOI 10.15482/USDA.ADC/1239279 (international standard).
  - Use limitation (carried into output): "Not to be used for self-diagnosis or
    self-medication."
  - Bulk file: Duke-Source-CSV.zip (figshare file 43363335, md5 45ae44a0544586b8ac22a232beaac344).

WHAT IT DOES:
  Reads the AGGREGAC table (phytochemical <-> bioactivity <-> dosage <-> reference,
  ~28.9k rows) and joins CHEMICALS for the CAS Registry Number (the structural bridge to
  PubChem). It splits activities into TWO honest buckets:
    - anticancer_leads     — chemical has a claimed anti-cancer activity
    - procancer_safety_flags — chemical has a carcinogenic / tumor-promoter / mutagenic
                               activity (the same compound can appear in both — that's the point)
  Each row carries Duke's abbreviated REFERENCE and any DOSAGE (LD50/PTD/etc.) for the
  dose-anchored safety clause.

DOCTRINE: Duke is a CC0 + DOI-cited authority, but its activity rows are AGGREGATED LEADS
drawn from older literature with abbreviated references. Every claim is RE-VERIFIED at a
modern authority before it enters the verified corpus: chemical/CAS -> PubChem CID
(cancer_bridge.py --pubchem) -> linked PMIDs -> Europe PMC. Documentation, not endorsement;
no efficacy verdict; the carcinogenic bucket is a safety surface, not a claim the compound
is dangerous at culinary dose (dose makes the poison).

Stdlib only. Usage:
  1) download + unzip first (see the banner this prints if the CSVs aren't found), then:
  python3 duke_ingest.py                         # parse ~/cancer_intake/duke_src/
  python3 duke_ingest.py --src /path/to/csvdir   # custom CSV dir
Output -> ~/cancer_intake/duke_candidates.json
"""

import csv, glob, json, os, sys, zipfile

INTAKE = os.path.expanduser("~/cancer_intake")
DEFAULT_SRC = os.path.join(INTAKE, "duke_src")
ZIP_HINT = os.path.join(INTAKE, "Duke-Source-CSV.zip")
OUT = os.path.join(INTAKE, "duke_candidates.json")

CITATION = ("U.S. Department of Agriculture, Agricultural Research Service. 1992-2016. "
            "Dr. Duke's Phytochemical and Ethnobotanical Databases. "
            "doi:10.15482/USDA.ADC/1239279")
USE_LIMITATION = "Not to be used for self-diagnosis or self-medication."

# Activity classification by normalized (lowercased, de-punctuated) substring match.
ANTICANCER = [
    "anticancer", "antitumor", "antineoplastic", "cancerpreventive", "antileukemic",
    "antimelanomic", "anticarcinomic", "anticarcinogenic", "antiproliferant",
    "antiproliferative", "apoptotic", "antimutagenic", "cytotoxic", "antiangiogenic",
    "antimetastatic", "antiaromatase",
]
PROCANCER = ["carcinogenic", "cocarcinogenic", "tumorpromoter", "mutagenic", "tumorigenic"]

def norm(s):
    return (s or "").lower().replace("-", "").replace(" ", "").replace("_", "")

def classify_activity(act):
    a = norm(act)
    if any(t in a for t in ANTICANCER):
        return "anticancer"
    if any(t in a for t in PROCANCER):   # reached only if not anticancer
        return "procancer"
    return None

def find_table(src, name):
    # case-insensitive match on file stem (AGGREGAC -> AGGREGAC.csv / aggregac.csv)
    for p in glob.glob(os.path.join(src, "**", "*.csv"), recursive=True):
        if os.path.splitext(os.path.basename(p))[0].upper() == name.upper():
            return p
    return None

def read_rows(path):
    if not path:
        return []
    for enc in ("utf-8-sig", "latin-1"):
        try:
            with open(path, encoding=enc, newline="") as f:
                return [{(k or "").strip().upper(): (v or "").strip() for k, v in row.items()}
                        for row in csv.DictReader(f)]
        except UnicodeDecodeError:
            continue
    return []

def maybe_unzip():
    if os.path.isdir(DEFAULT_SRC) and glob.glob(os.path.join(DEFAULT_SRC, "**", "*.csv"), recursive=True):
        return True
    if os.path.exists(ZIP_HINT):
        os.makedirs(DEFAULT_SRC, exist_ok=True)
        with zipfile.ZipFile(ZIP_HINT) as z:
            z.extractall(DEFAULT_SRC)
        return True
    return False

def main():
    a = sys.argv
    src = a[a.index("--src") + 1] if "--src" in a else DEFAULT_SRC
    if src == DEFAULT_SRC and not maybe_unzip():
        print("Dr. Duke's CSVs not found. Acquire the CC0 source first (~6 MB):\n")
        print("  mkdir -p ~/cancer_intake && cd ~/cancer_intake")
        print("  curl -L -o Duke-Source-CSV.zip https://ndownloader.figshare.com/files/43363335")
        print("  python3 " + os.path.abspath(__file__) + "   # auto-unzips and parses")
        return

    chem_path = find_table(src, "CHEMICALS")
    agg_path = find_table(src, "AGGREGAC")
    if not agg_path:
        print(f"AGGREGAC table not found under {src}. Is this the Duke CSV set?"); return

    # CHEMICALS: name(UPPER) -> CAS + CHEMID (the bridge to PubChem)
    chem_map = {}
    for r in read_rows(chem_path):
        nm = (r.get("CHEM") or "").upper().strip()
        if nm:
            chem_map[nm] = {"cas": r.get("CASNUM") or None, "chemid": r.get("CHEMID") or None}

    anti, pro = {}, {}   # dedupe by (chem, activity)
    for r in read_rows(agg_path):
        chem = (r.get("CHEM") or "").strip()
        act = (r.get("ACTIVITY") or "").strip()
        if not chem or not act:
            continue
        bucket = classify_activity(act)
        if not bucket:
            continue
        meta = chem_map.get(chem.upper(), {})
        rec = {
            "chem": chem,
            "activity": act,
            "dosage": r.get("DOSAGE") or None,
            "reference": r.get("REFERENCE") or None,
            "cas": meta.get("cas"),
            "chemid": meta.get("chemid"),
            "verify_rule": "resolve CAS/name at PubChem -> CID -> linked PMIDs -> Europe PMC before use",
        }
        key = (chem.upper(), norm(act))
        (anti if bucket == "anticancer" else pro)[key] = rec

    anti_rows = sorted(anti.values(), key=lambda x: x["chem"])
    pro_rows = sorted(pro.values(), key=lambda x: x["chem"])
    distinct_anti_chems = sorted({r["chem"].upper() for r in anti_rows})

    doc = {
        "source": "Dr. Duke's Phytochemical and Ethnobotanical Databases (USDA ARS)",
        "license": "CC0-1.0 (public domain dedication)",
        "doi": "10.15482/USDA.ADC/1239279",
        "citation": CITATION,
        "use_limitation": USE_LIMITATION,
        "doctrine": ("CC0+DOI authority, but activity rows are aggregated LEADS — re-verify "
                     "every claim at a modern authority (PubChem->PMID->Europe PMC). No efficacy "
                     "verdict. The procancer bucket is a safety surface; dose makes the poison."),
        "counts": {
            "anticancer_activity_rows": len(anti_rows),
            "distinct_anticancer_chemicals": len(distinct_anti_chems),
            "procancer_safety_rows": len(pro_rows),
        },
        "anticancer_leads": anti_rows,
        "procancer_safety_flags": pro_rows,
    }
    os.makedirs(INTAKE, exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=2)

    print(f"\n=== Dr. Duke's -> cancer leads ===  -> {OUT}")
    print(f"  anticancer activity rows : {len(anti_rows)}")
    print(f"  distinct anticancer chems: {len(distinct_anti_chems)}")
    print(f"  procancer SAFETY flags   : {len(pro_rows)}")
    print("\n  sample anticancer leads:")
    for r in anti_rows[:12]:
        cas = f"CAS {r['cas']}" if r.get("cas") else "no-CAS"
        print(f"    {r['chem'][:34]:34}  {r['activity'][:26]:26}  {cas}")
    print("\nNext: feed distinct chems through the bridge — cancer_bridge.py --pubchem \"<chem>\"")
    print("then resolve CID->PMIDs->Europe PMC. Re-verify every claim. CC0; cite the DOI.")

if __name__ == "__main__":
    main()
