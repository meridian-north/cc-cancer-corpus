# IMPPAT 2.0 — ingestion note

*The one real win from the public-repo sweep (2026-06-04). Surfaced as a Tier-4
community-repo lead, verified, and promoted to authority-class. This note records what it
is, how it enters the corpus through the existing PubChem bridge, and the license gate.*

---

## What it is (verified)

- **Repo:** [`asamallab/IMPPAT2`](https://github.com/asamallab/IMPPAT2) — MIT (code).
- **Resource:** "IMPPAT 2.0: An Enhanced and Expanded Phytochemical Atlas of Indian
  Medicinal Plants." Topics: cheminformatics, natural-products, traditional-indian-medicine.
- **Authoring group:** Areejit Samal lab (`asamallab`) — a real cheminformatics group;
  the repo is the manuscript's associated code/data.
- **Why it matters here:** it is structured **plant → phytochemical → therapeutic-use**
  data, dense with anticancer phytochemicals (curcumin, withaferin A, etc.). That is
  precisely the chemical↔herbal bridge the corpus is built around.

## How it enters the corpus — the bridge path

IMPPAT is not evidence on its own; it is a high-quality **map of what to verify**. The
path reuses tooling that already exists:

1. **Plant → phytochemical.** From an IMPPAT plant record, take the constituent
   phytochemical list.
2. **Phytochemical → PubChem CID.** Resolve each compound to its CID:
   `python3 cancer_bridge.py --pubchem "<compound name>"`. The CID is the structural anchor.
3. **CID → literature.** PubChem links the CID to PubMed IDs + bioassays. Resolve those
   PMIDs at Europe PMC (the existing `verify_pmid` path in `cancer_kind_scraper.py`),
   storing verified metadata + abstract.
4. **Mechanism tag.** Run the stored abstracts through `cancer_bridge.py --index` so the
   compound lands at its mechanism node (electron-transport, redox, microtubule, HDI, etc.).

The result: IMPPAT contributes *candidate compounds with provenance*, and every claim is
re-verified at its authority before it counts — same rule as every other source.

## License gate — read before bulk download

- The repo's **MIT license covers the code**, not necessarily the curated data.
- The IMPPAT **database itself lives on a web portal**; the portal's own terms of use
  govern bulk reuse of the dataset.
- **Action:** verify the portal's data-use terms before ingesting the dataset in bulk.
  Until then: treat IMPPAT as a pointer to look up compounds individually (which the
  bridge path above does anyway), not a dataset to mirror.

## Provenance — why this is in the registry now

IMPPAT entered as a **Tier-4 community-repo LEAD** (lowest trust) and **earned promotion
to authority-class** by verifying out cleanly. That is the corpus's trust-promotion
mechanic working as designed: a lead becomes an authority by proving itself, exactly the
way a peer earns co-signatory status. Recorded in `CancerCorpusSourceRegistryMt.cycl`.

---

*Filed 2026-06-04. The honest companion finding: IMPPAT was the lone gem in ~40 repo leads
— the public-repo axis is otherwise flooded with leaf-photo classifiers. Depth still comes
from the authority tiers; this is the exception that earned its place.*
