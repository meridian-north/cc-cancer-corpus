# For Scott and Stephen — The Nerdy Parts

*What's actually running under the hood.*

---

## The pharmacovigilance infrastructure (VAERS / V-Safe)

The VAERS corpus is 1,989,028 reports spanning 37 years, stored as per-year
compressed archives (.tar.gz) with SHA256-attested settlement manifests. Each
record is a clause_envelope/v1 JSON object organized around the 5W1H grammar
(who, what, when, where, why, how) — the same structure the game NPC layer uses,
which means the same query tooling runs on adverse event data and NPC conversation
history. The master index is ~4 GB of JSONL (one JSON object per line), designed
to stream without loading into RAM, which matters at 1.98M rows.

The distilled output is a 69-column CSV implementing ADR-200's universal strand
architecture — three blocks of 23 columns each: Strand 1 is the Pale March
manifest (identity, lot number, outcomes, attestation; consistent across all five
jurisdictions), Strand 2 is the full clinical record (symptoms as pipe-separated
MedDRA terms, latency, reporter class, full vaccine history), and Strand 3 is the
substrate operational layer (BitNet tier verdicts, chain block references, Hot RAM
from ADR-003). Strand 3 is currently null for VAERS — the batch_scorer stalled
during initial cohort scoring because Bourne (:11438) was down and the single
Ember wrapper (2B BitNet model, :11435) saturated at ~800 calls per cohort before
the first 10K-envelope progress event could fire. The root cause: scoring runs
inline with iteration, so you make up to 800 LM calls before logging anything.
Fix is D1 (bring Bourne up, drop LOG_INTERVAL to 500, scope to 2021–2026 first,
read the actual throughput). Bourne is half the BitNet inference capacity; without
it the run looks hung.

The V-Safe Phase 2 distillation had a separate bug: the envelope_adapter used
`tarfile.getmembers()` to index members before iterating, which builds a full
in-memory list. Fine for 37 VAERS tarballs. Fatal for V-Safe's 2021 tarball —
~80–100M individual per-registrant .json files in one 10 GB compressed archive.
OS killed Python at ~22M rows (15%) because `getmembers()` had consumed all
available RAM. Fix is one line: `for member in tf:` instead of
`for member in tf.getmembers():`. Streaming iterator, flat memory profile,
scales to any archive size.

---

## The cancer corpus (cc-cancer-corpus)

The cancer corpus is a different class of infrastructure — it runs against public
academic databases (EuropePMC, PubMed, ClinicalTrials.gov) rather than government
surveillance files. Three Python scripts do the work: `cancer_discover.py` sources
papers from neutral registries with real DOI/PMID/NCT identifiers,
`cancer_kind_scraper.py` verifies every identifier against its authority,
stores abstract + open full text where licensed, and hashes everything, and
`cancer_bridge.py` is the HOW-join — it tags each study by mechanism-of-action
node using lexicon-matched classification (transparent, auditable, zero LLM in the
discovery pipeline) and answers `--node <mechanism>` queries that return all papers
converging on a target regardless of whether they're from pharma, academia, or
complementary medicine research.

The `cancer_why_filer.py` is the citation anomaly detector. It computes expected
citation weight stratified by evidence class (reviews versus primary studies versus
preclinical, each normed against their own stratum), then surfaces papers where
observed citations are significantly above stratum-expected. The score is
`anomaly = (observed_citations - expected_for_stratum) / stratum_stddev` — a
simple z-score variant. Papers that clear the threshold get flagged as
`PROMOTION_anomaly` with the raw numbers attached. No verdict is issued; the
flagged paper gets a "why is this being cited at this rate?" question attached and
routes to the why-fork investigation queue. The algorithm doesn't know or care
whether the anomaly is legitimate (textbook status, methodological anchor) or
suspicious (citation network amplification, pharma promotion). It just measures
the gap and asks the question.

The attestation chain for the cancer corpus is git: each commit SHA is a Merkle
tree root over the entire repository state. The current corpus anchor is
`72e2860` (2026-06-05). To add this to the Garrison Node nightly ceremony and
get it into the HSV Merkle root, add the repo path to `KNOWN_TOP_LEVEL_DIRS` in
`attestation_ceremony.py` — one line, the scanner picks it up automatically. The
corpus itself is stdlib-only Python; no third-party dependencies, runs on macOS
and Linux.

---

*The short version: VAERS runs a sovereign local BitNet inference stack against
government CSV data, producing a SHA256-attested 69-column CSV with a full
5W1H schema. The cancer corpus runs lexicon-matched mechanism tagging against
academic databases, producing a citation-anomaly-flagged mechanism map.
Both are open source. Both are reproducible. Neither requires cloud compute.*
