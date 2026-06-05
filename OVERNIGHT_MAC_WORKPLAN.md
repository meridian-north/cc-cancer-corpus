# Overnight Mac workplan — cancer corpus, 2026-06-03 night

*What the Mac runs tonight, sequenced low-to-high cost. All scripts are stdlib, polite,
public-only. Set `CONTACT_EMAIL` in the tools first. Don't run heavy host BitNet
concurrently with any brownfield/medicaid pass — these are light (API + lexicon).*

## Phase 1 — broaden the corpus across the mechanism nodes (discover → verify → store)

Run discovery for the key agents at each HOW-node, renaming the output between queries
so they accumulate, then scrape each (stores abstracts + open full text, hashes all):

```bash
S=~/garrison/outreach/conventional_and_complementary_cancer_treatments
run(){ python3 $S/cancer_discover.py --europepmc "$1" --n 30; \
       mv ~/cancer_intake/discovered_feedstock.json ~/cancer_intake/fs_"$2".json; \
       python3 $S/cancer_kind_scraper.py --feedstock ~/cancer_intake/fs_"$2".json; }
run "metformin cancer OXPHOS" met
run "atovaquone cancer complex III" ato
run "methylene blue cancer mitochondria" mb
run "tumor perfusion hypoxia exercise cancer" perf
run "bevacizumab vascular normalization" bev
run "fasting mimicking diet chemotherapy" fmd
run "fenbendazole mebendazole cancer" fbz
run "ivermectin cancer" ivm
# trials:
python3 $S/cancer_discover.py --trials "pancreatic cancer KRAS OR OXPHOS" --n 30
```

## Phase 2 — build the mechanism index (the HOW-bridge)

```bash
python3 $S/cancer_bridge.py --index            # -> ~/cancer_intake/mechanism_index.json
python3 $S/cancer_bridge.py --node perfusion_vascular_hypoxia
python3 $S/cancer_bridge.py --node electron_transport_oxphos
```

## Phase 3 — PubChem enrichment (the chemical↔literature bridge)

For each named agent, resolve the CID (then, later, MoA/target/pathway):

```bash
for a in "metformin" "atovaquone" "methylene blue" "dichloroacetate" "chlorine dioxide"; do
  python3 $S/cancer_bridge.py --pubchem "$a"; done
```

## Phase 4 — FAERS aggregates for the cohort

Run the 9-query kit over the oncology + supplement cohort (pembrolizumab, carboplatin,
temozolomide, + the supplements) and save the JSON. Later: **join** each agent's
adverse-event profile to its mechanism node — does the AE pattern track the HOW?

## Phase 5 — the WHY-detector (the most interesting pass): unusual suppression / promotion

**The why we hunt = the mismatch between EVIDENCE and ATTENTION.** Not "is it true" —
*"why did its attention diverge from its evidence?"* Two anomaly classes:

- **Suppression anomaly** — high evidence class + high independence (well-replicated)
  **but** low/negative attention: retracted, deprecated, buried, low citations relative
  to quality. → *why was this suppressed?*
- **Promotion anomaly** — low evidence class + single-source / citation-ring **but**
  high attention: heavily cited, viral, guideline-adopted, hyped. → *why was this promoted?*

**v1 signals (API-available tonight):**
- *evidence* = `ReproducibilityAnchoredScoringMt` inputs: evidence_class + independence
  (single_source / citation_ring / independent_n≥2/3).
- *attention* = Europe PMC `citationCount`, retraction flag (Crossref / Retraction
  Watch), preprint-vs-published status.
- *anomaly score* = standardized(attention) − standardized(evidence). Large positive →
  promotion anomaly; large negative → suppression anomaly.

**Output:** `~/cancer_intake/why_anomalies.json` — ranked, each row carrying the
evidence-vs-attention delta and the **candidate why-questions as questions, never
verdicts**: fraud? inconvenience? funding pressure? the good-old-boys citation ring?
commercial interest? paradigm lock-in? Forked to the why-layer (ADR-204); the substrate
flags the divergence and asks — it does not conclude.

*This composes with `ReproducibilityAnchoredScoringMt` (evidence not prestige),
`SuppressedLiteratureBridgeMt` (queued), and the independence invariant. It is the
literature instance of the why-fork: catalog the translation/attention failures and
ask why — which is exactly the work no journal or registry does.*

## Phase 6 — attest

Everything stored carries a SHA-256 in the run manifest; the mechanism index + anomaly
report are hashed. Proof of work = the manifest + the recreate recipe, not a hoard.

Run it after the index is built:

```bash
python3 $S/cancer_why_filer.py        # -> ~/cancer_intake/why_anomalies.json
```

---

**Build status (tonight): ALL FIVE PHASES SHIP.** `cancer_discover.py`,
`cancer_kind_scraper.py`, `cancer_bridge.py`, the FAERS kit, **and now
`cancer_why_filer.py`** are all built. Run Phases 1→5 top to bottom; the why-filer
reads the stored studies, scores evidence vs Europe PMC citation attention, and emits
the ranked suppression/promotion anomaly list with the why as questions. (Next
enhancement, not tonight: independence-of-confirmation via the citation graph, and
joining FAERS adverse-event profiles to mechanism nodes.)

*No efficacy verdicts. Dose-anchored safety on every row. The method travels with the
data; the why stays with the human.*
