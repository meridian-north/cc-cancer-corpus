# Feedstock intake — Gemini v2 pass, independently verified & scored

*Sourced by Gemini (v2 prompt), independently verified by Claude (Cowork), 2026-06-03.
Provenance flag: `independence: single_source (Gemini) → Claude-verified`. A second
independent sourcing pass (Grok) is still owed before any item is "confirmed" for
publication. Under the not-reviewed-for-public-consumption flag.*

## Meta-finding (record this — it's the proof point)

Even under the v2 "verify-don't-assert" rule, **1 of 2 items Gemini self-marked
VERIFIED was still a misattribution** (the PDX paper: wrong journal/DOI/title). The
independent verification layer caught it. Lesson, again: a "VERIFIED" self-label is
not verification; only an independent check is. This is the `independence_of_confirmation`
invariant (`ReproducibilityAnchoredScoringMt`) doing its job.

---

## 1. DCA / glioblastoma (Michelakis 2010) — KEEP

- verification: VERIFIED (high prior; well-known 5-patient cohort)
- source_class: small_human_cohort · evidence_class: small_cohort
- pointer: https://doi.org/10.1126/scitranslmed.3000817 (Sci Transl Med)
- independence: single_source (5-patient, non-blinded, single-center)
- public_consumption_signal: HIGH — large off-label DCA self-treatment footprint online
- note: a strong **prevalent-but-thin-evidence** example — exactly the class the crank
  rule says to include *because* it's widely consumed, scored honestly.

## 2. Iniparib translation failure (2012) — KEEP (flagship discordance)

- verification: VERIFIED on substance (independent search confirmed mechanism + Phase III failure)
- source_class: preclinical_mouse · evidence_class: preclinical · model_class: cell_line_xenograft
- pointer: https://doi.org/10.1158/1535-7163.MCT-11-0993 (AACR Mol Cancer Ther)
- human_concordance: **discordant** — promising in early models; Phase III TNBC failed (Jan 2011)
- discordance_question: why did cell-line xenografts read iniparib as a potent selective
  PARP inhibitor when it is a non-selective cysteine-protein modifier that doesn't inhibit
  PARP at clinically achievable concentrations?
- independence: independent_n>=2 (failure confirmed across labs post-trial)
- caveat: the exact companion Phase III DOI Gemini cited needs confirmation (the canonical
  Phase III is O'Shaughnessy et al., JCO 2014;32:3840); the *mechanism + failure* narrative
  is solid regardless.
- value: the model discordance example for the corpus — strong mouse signal, known why-it-failed.

## 3. Garrido-Laguna pancreatic PDX (2011) — KEEP, CITATION CORRECTED

- verification: CORRECTED — real paper, **mis-cited by Gemini (she marked it VERIFIED)**
- ❌ Gemini: "High-fidelity patient-derived xenografts…", Mol Cancer Ther, doi 10.1158/1535-7163.MCT-10-1044
- ✅ Actual: Garrido-Laguna I, et al. **"Tumor engraftment in nude mice and enrichment in
  stroma-related gene pathways predict poor survival and resistance to gemcitabine in
  patients with pancreatic cancer." Clin Cancer Res. 2011;17(17):5793-5800.** (PubMed; AACR CCR)
- source_class: preclinical_mouse · evidence_class: preclinical · model_class: pdx_avatar
- human_concordance: **concordant (prognostic)** — TIGHTENED: the paper shows *tumors that
  engraft in mice* predict poor survival + gemcitabine resistance in the patient. This is a
  prognostic concordance, NOT "the avatar's drug response matched the patient's."
- related (the avatar-guided-treatment concordance she was reaching for): Hidalgo et al.,
  "personalized tumorgrafts" pilot — PubMed 21673092.
- contested: PDX loses human stroma/immune microenvironment over mouse generations; can't
  model immunotherapy in immunocompromised hosts (her good_questions here are excellent).

## 4. Curcumin / Notch-1 retraction (2006) — KEEP, UPGRADED

- verification: Gemini marked UNVERIFIED (Wiley gateway error this session). Claude UPGRADES
  to VERIFIED — confirmed the Wiley "Retracted: Notch-1…" record last session.
- ✅ Wang, Sarkar et al. journal **Cancer** (Wiley), **doi 10.1002/cncr.21904**, 2006; retracted for figure/data integrity.
- source_class: retracted · evidence_class: preclinical · model_class: in_vitro
- independence: single_source · human_concordance: untested_in_human
- why_removed: documented figure/data duplication-integrity concerns.
- good_question: does curcumin→Notch-1 suppression hold when independent labs re-run it with
  unmanipulated, open-data blots?

---

## Scoreboard summary

| Item | class | evidence | model | concordance | independence | status |
|---|---|---|---|---|---|---|
| DCA glioblastoma | small_human_cohort | small_cohort | — | — | single_source | VERIFIED |
| Iniparib | preclinical | preclinical | cell_line_xenograft | **discordant** | indep_n≥2 | VERIFIED |
| Garrido-Laguna PDX | preclinical | preclinical | pdx_avatar | concordant(prognostic) | indep_n≥3 | CORRECTED |
| Curcumin (retracted) | retracted | preclinical | in_vitro | untested | single_source | VERIFIED(↑) |

**Next:** independent Grok pass over these same items (don't single-source the feedstock);
then promote the two clean discordance/concordance exemplars into the white paper as the
worked illustration of `PreclinicalTranslationScoringMt`.
