# Thread log — 2026-06-04 (cancer corpus, Cowork advisory)

*Lightweight in-thread decision log. Not a handoff; a running record so decisions
don't live only in chat. Sovereign: jr (L4).*

---

## Decision — Understand-Anything (U-A) wraps: intent-only, deferred

**What:** jr evaluated [Lum1104/Understand-Anything](https://github.com/Lum1104/Understand-Anything)
(MIT, Claude Code plugin; tree-sitter + LLM pipeline → `knowledge-graph.json` → read-only
Astro dashboard) as a possible Obsidian replacement, conditional on adding **edit-in-the-
rendered-format** (write-back) capability.

**Decision (jr, 2026-06-04):**
- **Keep his set-aside U-A "wraps" for INTENT reference only** — they are *not* to be
  reapplied. The repo moves too fast (95 open PRs, daily commits, v2.5.0 dashboard
  overhaul) for in-core patches to survive; old wraps are stale against the current
  dashboard. Salvage the *idea*, rebuild fresh if/when pursued.
- **U-A is NOT tonight's tool.** No update, no fork, no clone work tonight.
- **Deferred (later, not now):** (a) the write-back module + edit-protection flag design;
  (b) shaping the cancer corpus into the Karpathy-wiki form (`index.md` + wikilinks) so
  `/understand-knowledge` can ingest it. Both explicitly punted to a future session.

**Why it matters:** prevents drift. If a future thread finds the old wraps, this entry
says: reference, don't reapply.

---

## Tonight's pivot — proceed with the expanded corpus + public-markdown sourcing

Moving on from U-A to the substantive corpus work:
- The expanded sweep (herbs, terpenes, cannabis-by-component, MOA, HDI safety keystone,
  metals, peptides-as-research) continues grinding on jr's Mac.
- **New sourcing axis added tonight:** query **public markdown repositories** (wiki-md and
  web-md knowledge bases) as corpus *leads* — `wiki_repo_discover.py`. License-gated,
  lowest-trust, every claim re-verified at its authority. Feeds the **contradictions**
  surface: community-wiki claims vs verified literature.

---

## Ratification + routing update (jr, 2026-06-04, while scanning the repo leads)

**1. Lawful acquisition / license gate — RATIFIED.** jr blesses IMPPAT's (and the corpus's)
respect for lawful data acquisition. The gate is doctrine now, not just caution: a repo's
LICENSE covers its code; a dataset's own portal terms govern bulk reuse; no-license =>
POINTER_ONLY; verify terms before ingesting any dataset in bulk.

**2. Chinese-language TCM leads — RE-RANKED (translator in the loop).** Dr. Gene Wei reads
Chinese, so the language "curation burden" I used to down-rank the Chinese TCM leads is
removed. The license gate still decides:
- **Open + now interpretable → route to Dr. Wei:** `admin360bug/Compendium-of-Materia-Medica`
  (本草纲目, MPL-2.0, 521★); `Yuchunchen/CHMminer` (GPL-3.0); `YukiChen-yuxin/…TCM-knowledge-graph`
  (MIT — structured KG built from the Compendium; most useful shape).
- **Pointer-only (no license):** `winycg/TCMP-300`, `stevetsa/awesome-TCM` (link-list meta-lead),
  `mmcnl/formulas`.
- **Dropped (CV noise regardless of language):** the two Chinese image-recognition repos.

**Caveat held:** the classical Bencao Gangmu is a Ming-dynasty pharmacopeia — ethnobotanical
PROVENANCE, not modern clinical evidence. Language changes who can read it, not its evidence
tier. Every claim still re-verified at a modern authority. (EfficacyNeutrality + verify-don't-trust.)

---

---

## Doctrine carved — ReciprocalSovereigntySourcingMt (jr articulation, 2026-06-04)

jr: *"Garrison Node has absolutely no problem respecting Chinese sovereignty and tribal
wrappers for our substrate. If there is anything of value, re the 5w1h, that is honorably
requested and consumed and citable via internationally recognized standards, it's a go ...
South American and Russian sources or Korean — rule none out."*

Filed as `~/garrison/GN/cycle/microtheories/ReciprocalSovereigntySourcingMt.cycl`. The principle:
a source is admissible on **honorable acquisition + international-standard citability + 5w1h
value — never on origin.** Grounded in real instruments so it's operational, not aspirational:
- **Honorable acquisition:** Nagoya Protocol (ABS for genetic resources + associated traditional
  knowledge), CARE Principles for Indigenous Data Governance, WIPO TK Labels, + our license gate.
- **Citability:** DOI / PMID / NCT / PubChem CID / ISBN / ISO / Wikidata QID — the standard is
  both the verify-don't-trust anchor and the interoperability guarantee.
- **Reciprocity:** we honor others' sovereignty/wrappers exactly as we expect ours honored.
  Origin is the "Where" — a descriptor, never a disqualifier.

Cross-referenced from CancerCorpusSourceRegistryMt (composition). TODO: add an
acquisition-provenance field to the registry (the "honorably requested" receipt for
traditional/indigenous sources).

---

---

## Dr. Duke's wired + overnight filer launched (2026-06-04, ~00:26)

- **Dr. Duke's (USDA, CC0, DOI 10.15482/USDA.ADC/1239279)** — the "one last scrape." Bulk
  `Duke-Source-CSV.zip` ingested by `duke_ingest.py`: AGGREGAC chem↔activity↔dosage↔ref split
  into anticancer_leads + procancer_safety_flags (both-sides honest), CAS → PubChem bridge.
  Clears the admissibility bar (CC0 + DOI). Leads, not evidence — re-verify each at authority.
- **Overnight filer launched** — `run_overnight.sh` (PID 13672) → `~/cancer_intake/overnight.log`.
  Runs on the swept corpus. Duke's leads stage for the bridge/verify pass (they were always
  leads-to-verify, not pre-verified envelopes).

*Filed 2026-06-04. Attests at the next closing ceremony with the rest of the corpus tree.*

---

---

## Sourcing rebalance toward PRIMARY evidence — landed (jr steer, 2026-06-04, S217-followup #1)

**Why:** S217 close found the corpus is ~1046 secondary-lit (445 narrative reviews + 601 generic
journal articles) against ~7 primary human studies. Root cause: `run_corpus_sweep.sh` only ever
called `--europepmc` per query — `cancer_discover.trials()` (ClinicalTrials.gov v2) existed and
worked but was never invoked, so zero trials entered the corpus.

**jr steer (two rounds):** (1) sourcing = *as many sources as possible* (breadth-max, no phase
gate); (2) **How is the join key; the Why I don't want to dwell on** — a why as simple as a regional
law / mandated protocol / procedure is a fair, complete answer, not a thread to pull. The why-filer
stays as-is (built, working, light charitable question-fork); effort goes to feeding the *How*
(mechanism bridge).

**What landed (code, runs on jr's Mac — `~/cancer_intake/` is not mounted in Cowork):**
- `cancer_discover.py`: `--primary` flag → ANDs a pubType OR-filter (RCT/clinical-trial/observational/
  cohort/comparative/multicenter, not phase-gated) so EPMC returns primary human studies directly;
  rows tag `discovered_via=europepmc_primary`. Verified live: `PUB_TYPE:"Clinical Trial"` → 379
  curcumin hits. `trials()` broadened — breadth-max, adds `has_results` + `study_type`; new
  `trial_results(nct)` pulls a **bounded** posted-outcomes digest (titles + serious/other AE counts
  + flow groups, NOT the ~85KB blob) only under `--with-results`. New `--selftest` (offline).
- `run_corpus_sweep.sh`: each query now runs THREE passes — broad EPMC (keeps reviews for the
  why-filer's review stratum) + primary-pubType EPMC + ClinicalTrials.gov. `TRIAL_RESULTS=1` env
  toggles the opt-in results digest (off by default per How>Why). Backward-compatible defaults.
- `cancer_kind_scraper.py`: additive pass-through of `phase/study_type/has_results/results_digest`
  into `.meta.json` so trial enrichment survives the verify step (absent for non-trial rows).

**Design notes for the next thread:** Trials enter as `trial_registry` (ev=4) *presence* — the
why-filer already excludes `trial_registry` from attention scoring (line 203), so they shift the
evidence-axis composition without skewing the anomaly math. The *How* payoff is the primary EPMC
pass: those carry mechanism-bearing abstracts that feed `cancer_bridge.py --index`. Bare trial
registry rows have no abstract, so they add evidence presence but little mechanism text — wiring
`results_digest` into the bridge is a possible later How-enhancement, deliberately left opt-in.

**Verified:** `--selftest` PASS (classify_pubtype across 9 classes + primary-filter integrity);
offline `trials()` parse test PASS against captured live API JSON; `py_compile` + `bash -n` clean.

**Not done here (deferred to a sweep run):** the actual sweep is jr's to launch on the Mac
(`QUERIES=… run_corpus_sweep.sh`); a Grok/Gemini *primary-coverage crosscheck* prompt (breadth of
known trials/cohorts per compound) is offered but not yet drafted.

*Filed 2026-06-04. Attests at the next closing ceremony with the rest of the corpus tree.*
