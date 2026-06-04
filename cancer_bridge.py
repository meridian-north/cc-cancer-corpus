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

import json, os, sys, glob, urllib.request, urllib.parse

INTAKE = os.path.expanduser("~/cancer_intake")
FILES = os.path.join(INTAKE, "files")

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
def pubchem_cid(name):
    url = ("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
           + urllib.parse.quote(name) + "/cids/JSON")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GarrisonNode-Bridge/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            cids = json.load(r).get("IdentifierList", {}).get("CID", [])
            return cids[0] if cids else None
    except Exception:
        return None

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
