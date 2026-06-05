# Peer crosscheck round 2 — independent verification report

*Cowork-Claude verified every concrete identifier the Gemini + Grok round-2 crosscheck returned,
resolving each against its authority (ClinicalTrials.gov v2 for NCT; Europe PMC for DOI) and checking
**title concordance** — does the identifier point at the study the peer described? Confidence is not
verification; round 1 already caught a fabricated DOI, so peer "VERIFIED" labels were not taken on
faith. Run: 2026-06-04. Composes with the corpus's verify-don't-trust rule and the scraper's
`title_mismatch_flag`.*

---

## Headline

**Gemini fabricated. Grok verified clean.** Of Gemini's identifiers, every one tested (6 NCT + 4 DOI)
was wrong — the identifiers either fail to resolve, or resolve to an **entirely unrelated study**.
Of Grok's items that carried a real pointer, every one tested (4 NCT + 2 DOI) resolved and matched.
Grok's only failure mode was leaving some items pointer-less (honest under-specification), not
fabrication. **Five verified items advance to the corpus; all of Gemini's are rejected.**

This is round 1's lesson, sharpened: the value of the corpus is the verification layer, and it earned
its keep here. The most insidious pattern is Gemini attaching a **real DOI to a confabulated
description** — it sails past a naive "does it resolve?" check and is caught only by title concordance.

## NCT verification (ClinicalTrials.gov v2, by identifier)

| Identifier | Peer | Claimed | Actually resolves to | Verdict |
|---|---|---|---|---|
| NCT00819208 | Grok | CHALLENGE/CO.21 colon exercise | Physical-activity program, high-risk stage II/III colon cancer (CHALLENGE/CO.21) | ✅ MATCH |
| NCT02905578 | Grok | High-dose ascorbate pancreatic Ph2 | "Phase 2 Trial of High-dose Ascorbate for Pancreatic Cancer (PACMAN 2.1)" | ✅ MATCH |
| NCT03456700 | Grok | Auranofin combo ovarian | "Auranofin and Sirolimus … Ovarian Cancer" (Ph2, terminated) | ✅ MATCH |
| NCT01737502 | Grok | Auranofin + sirolimus lung | "Sirolimus and Auranofin … NSCLC or SCLC" (Ph1/2) | ✅ MATCH |
| NCT04118946 | Gemini | Bifidobacterium / radiation enteritis | "Platelet Enriched Plasma for Interstitial Cystitis" | ❌ WRONG STUDY |
| NCT02763267 | Gemini | L-alanyl-L-glutamine / mucositis | "Pregnancy Regulation of Insulin and Glucose" | ❌ WRONG STUDY |
| NCT03875326 | Gemini | Resistance training / cachexia | "Stimulation to Improve Memory" | ❌ WRONG STUDY |
| NCT04033354 | Gemini | HCC metformin human comparator | Phase III HLX10 (PD-1) + chemo in NSCLC | ❌ WRONG STUDY |
| NCT01980316 | Gemini | NF1 plexiform comparator | "Argatroban … Vertebral Artery Stenting" | ❌ WRONG STUDY |
| NCT00115321 | Gemini | Poly-MVA Phase I solid tumors | (no record returned) | ❌ DOES NOT RESOLVE |
| NCT02353026 | Gemini | Artesunate + temozolomide GBM, EU consortia | "Phase I Study of Intravenous Artesunate for Solid Tumors" | ⚠️ AGENT REAL, SPECIFICS FABRICATED |

## DOI verification (Europe PMC, by identifier)

| Identifier | Peer | Claimed | Actually resolves to | Verdict |
|---|---|---|---|---|
| 10.1016/j.redox.2024.103375 | Grok | Ascorbate + gem/nab-pac pancreatic RCT | Same — Bodeker et al., Redox Biol 2024 (RCT) | ✅ MATCH |
| 10.1186/s12885-024-13023-w | Grok | Prehab RCT meta-analysis | Same — Gennuso et al., BMC Cancer 2024 | ✅ MATCH (systematic review, correctly labeled) |
| 10.1016/j.psyneuen.2014.10.009 | Gemini | MBSR / telomerase / breast cancer | "Effects of cortisol on cognition in MDD, PTSD, BPD" (Wingenfeld & Wolf 2015) | ❌ REAL DOI, WRONG PAPER |
| 10.1158/1078-0432.CCR-12-0312 | Gemini | Polyphenon E / bortezomib myeloma | Not found in Europe PMC (AACR journal, indexed thoroughly) | ❌ DOES NOT RESOLVE |
| 10.1158/1535-7163.MCT-11-0993 | Gemini | IV ascorbate pancreatic Ph2 | Not found in Europe PMC | ❌ DOES NOT RESOLVE |
| 10.1200/JCO.2005.04.8421 | Gemini | Chronotherapy colorectal | Not found in Europe PMC (ASCO journal, indexed thoroughly) | ❌ DOES NOT RESOLVE |
| 10.2147/CMAR.S10452 | Gemini | Biofield murine mammary (Bengston) | Untested (rate-limited) — **presumed suspect** given the pattern | ⚠️ UNVERIFIED |
| 10.1200/jco.2023.41.16_suppl.e16231 | Gemini | Viscum pancreatic cohort | Untested — presumed suspect | ⚠️ UNVERIFIED |
| 10.1016/j.jhepr.2021.100341 | Gemini | Sorafenib + metformin PDX HCC | Untested — presumed suspect | ⚠️ UNVERIFIED |
| 10.1158/1535-7163.MCT-15-0421 | Gemini | EGCG GEMM NF1 | Untested — presumed suspect | ⚠️ UNVERIFIED |

The four untested Gemini DOIs were left unchecked only because of fetch rate limits; given a 10/10
failure rate on everything tested, they are presumed suspect. The Mac-side scraper's `verify_doi` +
`title_mismatch_flag` is the final gate if any are run — but they are **not** pre-blessed here.

## Disposition

- **Ingested (5 verified items → `verified_feedstock_round2.json`):** CHALLENGE/CO.21 (NCT00819208),
  PACMAN ascorbate pancreatic RCT (DOI redox.2024.103375), auranofin+sirolimus ovarian (NCT03456700)
  and lung (NCT01737502), and the prehab RCT meta-analysis (BMC Cancer 2024). Feed to
  `cancer_kind_scraper.py --feedstock verified_feedstock_round2.json` for the full verify+store pass.
- **Rejected (all Gemini items):** not ingested. The identifiers are fabricated or mismatched.
- **Topics are still valid; citations are not.** Gemini's *descriptions* point at real corpus
  targets — MBSR/telomerase work, Viscum pancreatic cohorts, IV-ascorbate trials, a Bengston mouse
  paper all genuinely exist under correct identifiers. The fix is to **re-source those topics through
  the verified channel** (the three-pass sweep + Grok), never to ingest Gemini's invented pointers.
- **Grok's pointer-less leads** (prostate exercise/methylphenidate, IV mistletoe Helixor/JHU,
  betamethasone mucositis Japan, an MBSR ASCO item, a PDX colorectal item) are real-sounding but
  carry no resolvable identifier — `UNVERIFIED`, re-discoverable via the sweep, not ingested as-is.

## Recommendation (round 1 + round 2 pattern)

Gemini has now fabricated identifiers across two consecutive rounds. Going forward, use Gemini as a
**topic/angle generator only** — take its *domains and mechanisms* as search leads, and source every
actual pointer through Grok (which has been accurate) or the substrate's own sweep. Do not accept a
Gemini-supplied DOI/NCT into the corpus without independent resolution **and title concordance** —
resolution alone is insufficient, because Gemini attaches real DOIs to wrong descriptions.

## Round 3 addendum (Grok-only re-source + pipeline hardening)

Grok accepted the pointer-first contract and re-sourced the valid topics. Two new items verified
clean and were added to `verified_feedstock_round2.json` (**7 total**):
- **NCT03051477** — "Trial of Mistletoe Extract in Patients With Advanced Solid Tumors" (JHU/Helixor
  Phase 1, COMPLETED). ✅
- **DOI 10.1177/15593258231179903** — "Differential In Vivo Effects on Cancer Models by Recorded
  Magnetic Signals Derived From a Healing Technique" (Bengston W et al., Dose Response 2023, OA). ✅
  The real Bengston paper — it **replaces Gemini's fabricated `CMAR.S10452`** for the same topic.

Grok's MBSR item again carried no resolvable pointer ("Recent ASCO-linked trials") → UNVERIFIED, dropped.

**Pipeline hardening — the two-factor gate is now code.** `cancer_kind_scraper.py` no longer merely
flags a title mismatch; it **rejects** the lead. After an identifier resolves, `title_concordance()`
(stdlib: `SequenceMatcher` ratio max'd with word-containment, threshold 0.75) must clear or the item
is marked `REJECTED_TITLE_MISMATCH` and never stored. The containment term keeps a correctly-truncated
title (and the `RETRACTED:` prefix case) from false-rejecting, while the exact adversarial case we
caught (Gemini's MBSR claim vs the cortisol/cognition paper) scores 0.39 → rejected. Verified offline
against all four cases. The lesson is now structural: a real id on the wrong paper cannot enter the
corpus, regardless of which peer supplied it.

**Routing policy (accepted):** Gemini → topic/mechanism discovery only, decoupled from identifier
generation; Grok + the substrate's own three-pass sweep → identifier sourcing under the pointer-first
contract. Peers rested after this round.

*Filed 2026-06-04. The verified feedstock and this report attest at the next closing ceremony with
the corpus tree. Verification method: independent resolution at authority + title concordance, the
same discipline the scraper enforces — applied here before anything reached the scraper.*
