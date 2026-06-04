# For Dr. Gene Wei — where the corpus stands, the kits, and what we found running them

*GarrisonNode × AntiCancer360. Prepared by jr / John Reed, 2026-06-03. Companion to the
white paper. This is the "we ran it ourselves first" brief — kits + our own results +
the open questions, before you take it for a spin.*

---

## Where it stands (real, not aspirational)

A working pipeline that **sources from neutral authorities, verifies every reference
against that authority, and keeps the public layer** — verified metadata + abstract
of each study (SHA-256 hashed), open-access full text where licensed, and a verified
pointer to anything paywalled. No hallucinated citations: the identifiers come back
*from* PubMed/Europe PMC/ClinicalTrials.gov/Crossref, so there is nothing to invent.
Nothing private or paywalled is held.

## The kits we supply (you run them; nothing leaves your side)

1. **FAERS query kit** (`FAERS_QUERY_KIT_CATALOG.md`) — 9 ready-to-run openFDA queries
   over the FDA adverse-event system: reaction profile, drug role, death/serious
   signal, by-year, demographics, drug×reaction, **supplement co-report**, primary-
   suspect-only mortality, reporter country. Swap in any drug or supplement.
2. **`cancer_discover.py`** — pulls candidate studies straight from Europe PMC
   (international, incl. Asian/Chinese-indexed), ClinicalTrials.gov, Library of
   Congress — every row carries a resolvable id.
3. **`cancer_kind_scraper.py`** — verifies each id, stores the abstract + open full
   text, hashes everything, keeps pointers for the rest. Polite, public-only.

## What WE surfaced running them (so you see the output, not just the tools)

**FAERS — pembrolizumab (Keytruda), live, as of 2026-04-28:**
- 33,812 reports; role distribution overwhelmingly **primary suspect** (33,740) vs
  concomitant (183) — the integrity check that stops a co-report becoming a smear.
- A textbook checkpoint-inhibitor **immune-mediated profile**: colitis, pneumonitis,
  hepatitis, myocarditis, hypophysitis, adrenal insufficiency — alongside the
  single largest "reaction," *malignant neoplasm progression* (the cancer itself),
  the clearest reminder that a count is a lead, not a verdict.

**FAERS — the "counts don't rank danger" demonstration (death-flagged reports):**
acetaminophen 100,607 · aspirin 54,691 · ivermectin 325 · methylene blue 242 ·
chlorine dioxide 2. High counts track usage + reporting, not danger; no denominator.

**Translation pairs (verified, two independent agents + Crossref):**
- **Iniparib** (discordant) — preclinical "PARP inhibitor" promise → Phase III TNBC
  failure → wasn't even a real PARP inhibitor. DOI 10.1158/1078-0432.CCR-11-1973.
- **Daraxonrasib** (concordant) — preclinical RAS inhibition → **OS 13.2 vs 6.7 mo
  (HR 0.40)**, Phase III. NCT06625320 + NEJM. Same space, opposite outcome.
- **Autogene cevumeran** (partial) — mRNA neoantigen PDAC vaccine; ~half of patients
  (8/16) responded, with durable benefit in responders. DOI 10.1038/s41586-024-08508-4.
- **Garrido-Laguna PDX** (concordant, prognostic) — patient-avatar engraftment
  predicts poor outcome. DOI 10.1158/1078-0432.CCR-11-0341.

**International complementary-track set:** 16 verified Europe PMC curcumin-in-pancreatic-
cancer sources captured with stored abstracts — the complementary track, sourced and
hashed, ready for review.

## The good questions it raised (hypothesis-generating, never verdicts)

- What distinguishes a preclinical signal that *translates* (daraxonrasib) from one
  that *evaporates* (iniparib)? Iniparib's tell was mechanistic — the model reported
  target engagement that wasn't real.
- Why do most *predicted* neoantigens fail to elicit a human T-cell response, when
  the ~half that do confer durable benefit?
- For the supplements your clients use: do they appear in FAERS only as **concomitant**
  (along for the ride) or as suspect — and what co-report signals are worth a look?
- For curcumin specifically: does the mechanism hold when independent labs re-run it
  with open data? (One foundational curcumin/Notch-1 paper was retracted for image
  integrity — the claim is re-opened as a question, not dismissed.)

## The guardrails (these protect your patients, and they are non-negotiable)

Hypothesis-generating only · no denominator · no causation · drug-role-aware ·
**dose-anchored safety on every agent** (conventional, OTC, supplement alike — none
spared, none scorned) · **no "scam," no "cure"** from anyone · a mouse is a lead about
biology, never a proof about a person.

*Next: a Claude.ai prompt you can paste to drive any of this interactively —
`DR_WEI_CLAUDE_PROMPT.md`.*
