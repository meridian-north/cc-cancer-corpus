#!/usr/bin/env python3
"""
cancer_bridge.py — the HOW-bridge. Reads the stored verified abstracts/metadata in
~/cancer_intake/files/, tags each by MECHANISM NODE (the join key for this corpus),
clusters them, and answers joined-search-by-mechanism queries. This is what turns a
pile of verified studies into "everything that hits Complex I" — across the
conventional and complementary tracks at once.

Tagging = a curated mechanism lexicon matched against title+abstract (transparent,
auditable), plus an optional PubChem CID hook for compound resolution. No efficacy
verdicts — it groups by HOW, never ranks by works/doesn't.

Stdlib only. Examples:
  python3 cancer_bridge.py --index                       # build + print the mechanism index
  python3 cancer_bridge.py --node electron_transport     # joined search: all items at a node
  python3 cancer_bridge.py --pubchem "methylene blue"    # resolve a compound to its CID
Output -> ~/cancer_intake/mechanism_index.json
"""

import json, os, sys, glob, re, time, urllib.request, urllib.parse

INTAKE = os.path.expanduser("~/cancer_intake")
FILES = os.path.join(INTAKE, "files")
PUG = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound"

# ---- the mechanism lexicon (node -> trigger phrases). Auditable; extend freely. ----
NODES = {
    "electron_transport_oxphos": [
        "electron transport", "respiratory chain", "complex i", "complex iii",
        "oxidative phosphorylation", "oxphos", "nadh", "mitochondrial respiration",
        "etc inhibitor", "ubiquinone", "cytochrome", "atp synthase"],
    "perfusion_vascular_hypoxia": [
        "angiogenesis", "anti-angiogenic", "vascular normalization", "perfusion",
        "tumor blood flow", "hypoxia", "vegf", "microvessel", "interstitial fluid pressure",
        "oxygen delivery", "reoxygenation", "hyperthermia", "exercise"],
    "dna_damage_parp": [
        "parp", "dna damage", "homologous recombination", "brca", "double-strand break",
        "dna repair", "synthetic lethality", "platinum"],
    "immune_checkpoint": [
        "pd-1", "pd-l1", "ctla-4", "checkpoint inhibitor", "immune-mediated",
        "t cell", "t-cell", "neoantigen", "immunotherapy", "tumor microenvironment"],
    "metabolic_fasting_glycolysis": [
        "warburg", "glycolysis", "fasting", "fasting-mimicking", "ketogenic", "ampk",
        "mtor", "pyruvate dehydrogenase", "pdk", "metabolic reprogramming", "autophagy"],
    "microtubule_mitosis": [
        "microtubule", "tubulin", "mitotic", "spindle", "taxane", "benzimidazole"],
    "oxidative_stress_redox": [
        "reactive oxygen species", "ros", "oxidative stress", "glutathione",
        "pro-oxidant", "redox", "ferroptosis"],
    "cannabinoid_endocannabinoid": [
        "cannabinoid", "endocannabinoid", "cb1", "cb2", "cb1 receptor", "cb2 receptor",
        "cannabidiol", "tetrahydrocannabinol", "thc", "cbd", "cbg", "cbn", "cannabigerol",
        "cannabinol", "trpv1", "trpv2", "gpr55", "ceramide", "anandamide", "terpene",
        "caryophyllene", "limonene", "myrcene"],
    # p53 / apoptosis / cell-cycle axis — El-Deiry lab specialty; future papers will land here
    "p53_apoptosis_cell_cycle": [
        "p53", "tp53", "tumor suppressor", "apoptosis", "programmed cell death",
        "cell cycle arrest", "mdm2", "p21", "caspase", "bax", "bcl-2", "bcl2",
        "death receptor", "trail", "dr5", "intrinsic apoptosis", "mitochondrial apoptosis",
        "tumor dormancy", "dormancy reactivation", "cell cycle checkpoint"],
    # vaccine/infection-associated cancer signal — El-Deiry+Kuperwasser 2026 keystone paper
    "spike_vaccine_cancer_signal": [
        "covid vaccination", "covid-19 vaccination", "sars-cov-2", "mrna vaccine",
        "spike protein", "vaccine-associated cancer", "post-vaccination",
        "tumor dormancy", "immune escape", "dormancy reactivation",
        "microenvironmental shift", "tumor microenvironment reactivation",
        "injection site", "regional lymph node", "lymphoma after vaccination",
        "cancer after vaccination", "cancer after infection", "post-infection cancer"],
    # tight sub-node: papers SPECIFICALLY about cancer occurrence/worsening after vaccination
    # (excludes generic COVID treatment papers that hit the broad node on sars-cov-2 alone)
    "vaccine_cancer_specifically": [
        "vaccine-associated cancer", "post-vaccination cancer", "cancer after vaccination",
        "cancer following vaccination", "cancer after covid vaccination",
        "cancer after mrna vaccination", "cancer incidence vaccination",
        "cancer mortality vaccination", "vaccinated population cancer",
        "temporal association with covid-19 vaccination", "temporal association with vaccination",
        "temporal association with covid",
        "unusually rapid progression", "rapid recurrence after vaccination",
        "rapid reactivation", "reactivation of preexisting", "reactivation of cancer",
        "tumor reactivation vaccination", "dormancy reactivation vaccination",
        "injection site lymphoma", "injection site tumor", "injection site malignancy",
        "post-pandemic cancer", "post-covid cancer", "cancer safety signal",
        "turbo cancer", "turbocancer",
        "mrna vaccine cancer", "covid vaccine cancer",
        "oncologic safety signal", "vaccine injury cancer",
        "cancer incidence after vaccination", "cancer mortality after vaccination",
        "cancer following mrna", "cancer and vaccination", "vaccination cancer risk"],
    # the SAFETY keystone — does the agent interfere with standard-of-care drug clearance/efficacy?
    "herb_drug_interaction_cyp_pgp": [
        "cyp3a4", "cyp1a2", "cyp2c19", "cyp2d6", "p-glycoprotein", "p-gp", "pregnane x receptor",
        "pxr", "herb-drug interaction", "drug-drug interaction", "drug interaction",
        "auc", "area under the curve", "efflux transporter", "enzyme induction",
        "enzyme inhibition", "pharmacokinetic interaction", "clearance", "antagonism",
        "reduced response", "proteasome inhibitor", "bortezomib"],
}

def load_items():
    items = []
    for p in glob.glob(os.path.join(FILES, "*.meta.json")):
        try:
            with open(p) as f:
                d = json.load(f)
            d["_text"] = ((d.get("title") or "") + " " + (d.get("abstract") or "")).lower()
            items.append(d)
        except Exception:
            pass
    return items

def tag(item):
    hits = []
    for node, phrases in NODES.items():
        if any(ph in item["_text"] for ph in phrases):
            hits.append(node)
    return hits

def build_index(items):
    idx = {n: [] for n in NODES}
    for it in items:
        for node in tag(it):
            idx[node].append({"id": it.get("id"), "title": it.get("title"),
                              "pointer": it.get("pointer"), "year": it.get("year"),
                              "source_class": it.get("source_class")})
    return {n: v for n, v in idx.items() if v}

# ---- optional: resolve a compound name to a PubChem CID (the structural bridge) ----
def cas_standard(raw):
    """Unhyphenated CAS digits -> standard 'NNNNNNN-NN-N'. Ported from duke_verify.py so
    the bridge resolves CAS-bearing leads (e.g. Dr. Duke's rows) the same way the verifier does."""
    if not raw:
        return None
    d = re.sub(r"\D", "", str(raw).split(".")[0])
    if len(d) < 5 or len(d) > 10:
        return None
    return f"{d[:-3]}-{d[-3:-1]}-{d[-1]}"

def _pug_cid(value, kind="name"):
    """PubChem CID lookup with ONE transient-backoff retry (ported from duke_verify.py's
    cid_from). The retry catches the 'ivermectin -> None' transient-timeout false miss."""
    url = f"{PUG}/{kind}/" + urllib.parse.quote(value) + "/cids/JSON"
    for attempt in (1, 2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "GarrisonNode-Bridge/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                cids = json.load(r).get("IdentifierList", {}).get("CID", [])
                return cids[0] if cids else None
        except Exception:
            if attempt == 1:
                time.sleep(1.5)   # one backoff retry — transient, not a real miss
            else:
                return None

def pubchem_cid(name, cas=None):
    """Resolve a compound to its PubChem CID. CAS-first (standardized) when a CAS is supplied,
    then name fallback; both paths carry the backoff retry. Name-only callers still work."""
    cas_std = cas_standard(cas)
    if cas_std:
        cid = _pug_cid(cas_std, "name")
        if cid:
            return cid
    return _pug_cid(name, "name")

def main():
    a = sys.argv
    if "--pubchem" in a:
        name = a[a.index("--pubchem") + 1]
        cid = pubchem_cid(name)
        print(f"{name} -> PubChem CID {cid}"
              + (f"  https://pubchem.ncbi.nlm.nih.gov/compound/{cid}" if cid else "  (not found)"))
        return
    items = load_items()
    if not items:
        print(f"No .meta.json found in {FILES}. Run the scraper first."); return
    idx = build_index(items)
    out = os.path.join(INTAKE, "mechanism_index.json")
    with open(out, "w") as f:
        json.dump(idx, f, indent=2)
    if "--node" in a:
        node = a[a.index("--node") + 1]
        rows = idx.get(node, [])
        print(f"\n=== HOW-bridge: {node}  ({len(rows)} items) ===")
        for r in rows:
            print(f"  - {r['title'][:90] if r.get('title') else r['id']}  [{r.get('source_class')}]  {r.get('pointer')}")
    else:
        print(f"\nMechanism index ({len(items)} items scanned) -> {out}")
        for node, rows in sorted(idx.items(), key=lambda kv: -len(kv[1])):
            print(f"  {node:32} {len(rows):4} items")
        print("\nJoined search: python3 cancer_bridge.py --node <name>")
    print("\nNote: tags are lexicon-matched on title+abstract — transparent and auditable.")
    print("Grouping is by HOW (mechanism). No efficacy verdict is implied by co-location at a node.")

if __name__ == "__main__":
    main()
