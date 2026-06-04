# Seed Record — GN-CASE-LUNGADENO-0001

*A de-identified single-patient seed for the conventional + complementary
oncology corpus. Sovereign-authorized as a de-identified seed, 2026-06-03.
Identity stripped; clinical and experimental content preserved (WWWWH kept,
the "why" reserved for humans). This is the L2 projection of an L4-private
source record — the identified original stays in the patient's vault and is
NOT in this file, the corpus, or any chain artifact.*

---

## 0. Why this record exists

This is the **prototype** for the corpus's core question: what does a typical
person actually do when they try to *complement* conventional cancer treatment,
and can we give that experiment a structured, honest, trackable voice — without
crowning a winner. It carries **two tracks** by design:

- **Conventional track** — the standard-of-care clinical record (attested).
- **Complementary track** — the self-directed experiment the patient ran
  alongside it (logged, evidence-classed, safety-claused, never endorsed).

The value is the *structure*, reproducible across many patients. One record
proves nothing; it shows the envelope shape.

---

## 1. Record meta

| Field | Value |
|---|---|
| record_id | GN-CASE-LUNGADENO-0001 (synthetic) |
| source_privacy_layer | L4 (identified, vault-held) |
| this_artifact_layer | L2 (de-identified projection) |
| diagnosis | Lung adenocarcinoma |
| current_status | NED (No Evidence of Disease) |
| region | US Southeast (city-level removed) |
| key_biomarkers | TP53 (variant present); MSI-High; broad panel tested (EGFR/ALK/ROS1/BRAF/MET/HER2/RET/NTRK/KRAS) |
| profiling | Tissue NGS panel (2022); liquid biopsy / cfDNA (2023) |
| consent | De-identified-seed use authorized by source patient, 2026-06-03 |

---

## 2. CONVENTIONAL TRACK (standard of care — attested clinical)

Coarsened to sequence + relative timing; exact dates removed.

| Step | Modality | Evidence class |
|---|---|---|
| 1 | Surgery | Standard of care |
| 2 | Immunotherapy | Regulatory-approved |
| 3 | Chemotherapy | Regulatory-approved |
| 4 | Radiation | Standard of care |
| 5 | Chemotherapy (second line) | Regulatory-approved |
| 6 | **Docetaxel** (more aggressive regimen) | Regulatory-approved |

*Harm-gate for this track is inherent: clinician-directed and monitored.*

---

## 3. COMPLEMENTARY TRACK (self-directed — the experiment arm)

Pursued **alongside, not instead of** the conventional track. The patient
applied the harm-gate explicitly — asked the treating oncologist "is this doing
any harm?" and continued only on a "no." Every row carries an evidence class and
a mandatory safety clause; **none of these is an efficacy claim or a
recommendation.**

| Intervention | Timing vs. conventional | Evidence class | Mandatory safety clause |
|---|---|---|---|
| **Pre-treatment fasting** (~2-day water fast before docetaxel) | Immediately pre-infusion | Emerging clinical / mechanistic — fasting & fasting-mimicking diet, "differential stress resistance" (Longo et al.) | Refeeding & electrolyte risk; contraindicated in cachexia / low-BMI; clinician oversight required |
| **AC360 supplement set** (circulation/perfusion tenet) | Throughout | Mechanistic / preclinical — tumor perfusion & vascular-normalization rationale; human clinical evidence thin | Supplement–drug interactions; quality/purity variance; disclose all to oncologist |
| **Ivermectin** | During chemo | 1 registered Phase I/II (ivermectin+balstilimab, mTNBC) + ~50 preclinical + 1 observational cohort | Hepatotoxicity signal; no oncology approval; off-label; dose-related neuro/visual effects |
| **Chlorine dioxide (ingested)** | During chemo | No clinical efficacy evidence (ingestion) | **Dose-anchored (per DoseAnchoredSafetyDisclosureMt): EPA-regulated water disinfectant, characterized-safe at ≤0.8 mg/L residual (MRDL); the therapeutic-ingestion dose is materially higher and uncharacterized for a safe window; chlorite byproduct (hemolysis, methemoglobinemia) is the dose-dependent toxicity vector. The name is not the hazard — the dose-in-context is.** |
| **Methylene blue** | During chemo | Preclinical / redox-cycling rationale | MAO-inhibitor → serotonin-syndrome risk at higher doses; hemolysis risk if G6PD-deficient (test first) |
| **Visualization / mindset** ("envisioning the chemo cutting through poorly-perfused tissue to reach the tumor") | During treatment | Anecdotal / quality-of-life | None physical; documented as patient-reported psychological adjunct |

---

## 3a. Safety clauses are SYMMETRIC and dose-anchored (rev. 2026-06-03)

Doctrine correction. Earlier drafts attached a safety clause to chlorine dioxide
but not to the conventional/OTC agents — an asymmetry the same-scalpel principle
forbids. **Every agent carries a dose-anchored clause; none gets a free pass and
none gets a scarlet letter.** "The dose makes the poison" applies to water,
aspirin, and acetaminophen as much as to anything in the complementary track.

### FAERS death-flagged reports (openFDA, last_updated 2026-04-28)

| Agent | Death-flagged FAERS reports |
|---|---:|
| Acetaminophen (Tylenol) | 100,607 |
| Aspirin | 54,691 |
| Ivermectin | 325 |
| Methylene blue | 242 |
| Chlorine dioxide | 2 |
| Sodium chlorite | 0 |

**Read these correctly — the no-denominator rule cuts both ways:**
- These are *reports where a death was flagged and the drug was present* — not
  caused deaths. Co-reported, no causation. (Acetaminophen IS a leading real cause
  of acute liver failure — but the count is also inflated by enormous usage and
  heavy reporting.)
- **Low ≠ safe.** Chlorine dioxide's "2" is a *reporting-channel artifact*: it
  isn't a regulated pharmaceutical, so its poisonings surface in Poison Control
  data, case reports, and news — **not** the FAERS pipeline. Absence from FAERS is
  not evidence of safety.
- Raw counts therefore can't rank danger. They track usage volume + reporting
  channel + real toxicity, all confounded — the identical lesson as VAERS and the
  JAMA study.

### The honest residual distinction (what the clause SAYS, not whether it exists)

Not "dangerous vs safe" — it's **whether the therapeutic window is characterized:**

| Agent | Safe dose known? | Toxic threshold characterized? | Reversal/antidote | Approved indication |
|---|---|---|---|---|
| Acetaminophen | Yes (≤3–4 g/day) | Yes (hepatotoxic above) | Yes (NAC) | Yes |
| Aspirin | Yes | Yes | Supportive | Yes |
| Ivermectin (antiparasitic) | Yes | Yes | Supportive | Yes (not oncology) |
| Methylene blue | Yes (~1–2 mg/kg, approved uses) | Yes | Supportive | Yes (not oncology) |
| Chlorine dioxide (ingested) | **No established therapeutic dose** | Not characterized | None established | None |

So your principle holds exactly: dose makes the poison. The asymmetry that
survives is *not* "one is risky and the others aren't" — it's that for the OTCs
and approved drugs **we know where the line is**, and for ingested chlorine
dioxide **the line is uncharacterized**. That uncharacterized-window fact is the
clause content — stated plainly, applied to every row the same way.

---

## 4. OUTCOME SIGNAL

| Field | Value |
|---|---|
| pre-treatment expected response (patient-reported) | ~15% probability of positive response |
| observed | **Complete response** |
| outcome_class | Single-patient (n=1), hypothesis-generating only |

### ⚠️ Mandatory confounding disclosure

Multiple interventions changed **simultaneously** around the responding
regimen: a more aggressive chemo (docetaxel) **and** a pre-treatment fast **and**
the AC360 supplement set **and** ivermectin **and** chlorine dioxide **and**
methylene blue. **No single lever can be credited with the response.** This is
not a weakness of the patient's choices — it is the rational "throw everything at
survival" stack — and it is *precisely* the reason structured tracking across
**many** patients matters: what one n=1 cannot disentangle, a federation of
logged experiments can begin to. This record raises a question; it does not
answer one.

---

## 5. PLANNED (UNTRIED) PROTOCOL — referenced, not executed

A separate forward-looking maintenance protocol exists (lunar-aligned
antioxidant/pro-oxidant cycling + ketosis + intermittent & 3-day fasting +
hyperthermia "vascular reset" + the supplement stack above). It is **planned,
not performed**, and should be logged as a distinct *intervention-design*
record, never merged with executed history.

Honest evidence-classing of that protocol:
- **Mechanism-grounded levers** (varying evidence): fasting/FMD, hyperthermia/HSP70, ketosis-redox, perfusion logic — preclinical-to-emerging-clinical.
- **Lunar synchronization = scheduling convenience, not a therapeutic claim.** It is a consistent ~29.5-day cadence chosen *over* ragged weeks and uneven calendar months. It modulates nothing; it just sets the calendar the protocol rides on. No evidence class applies because no therapeutic claim is made. Tag: `scheduling_convenience`.
- The protocol's own safety scaffolding is *good practice and trackable*: mandatory G6PD test before methylene blue, quarterly CBC/CMP/Vitamin-D labs, oncologist review, explicit red-flag stop rules, stop-supplements-before-surgery. These belong in the envelope as required fields.

---

## 6. Machine-ready envelope (compact)

```yaml
record_id: GN-CASE-LUNGADENO-0001
schema: garrison/oncology_two_track/v0.1
privacy: {source_layer: L4, projection_layer: L2, consent: sovereign_deid_seed_2026-06-03}
patient: {dx: lung_adenocarcinoma, status: NED, region: us_southeast,
          biomarkers: [TP53, MSI_High], panel_tested: [EGFR,ALK,ROS1,BRAF,MET,HER2,RET,NTRK,KRAS]}
conventional_track:
  - {step: 1, modality: surgery, evidence_class: standard_of_care}
  - {step: 2, modality: immunotherapy, evidence_class: approved}
  - {step: 3, modality: chemotherapy, evidence_class: approved}
  - {step: 4, modality: radiation, evidence_class: standard_of_care}
  - {step: 5, modality: chemotherapy_2L, evidence_class: approved}
  - {step: 6, modality: docetaxel, evidence_class: approved}
complementary_track:
  - {agent: fasting_2day, timing: pre_docetaxel, evidence_class: emerging_clinical,
     harm_gate_cleared: true, safety: [refeeding_electrolyte, cachexia_contraindication]}
  - {agent: ac360_supplements, timing: throughout, evidence_class: preclinical_mechanistic,
     harm_gate_cleared: true, safety: [supplement_drug_interaction, purity_variance]}
  - {agent: ivermectin, timing: during_chemo, evidence_class: phase1_2_plus_preclinical,
     harm_gate_cleared: true, safety: [hepatotoxicity, off_label_no_onc_approval]}
  - {agent: chlorine_dioxide_ingested, timing: during_chemo, evidence_class: no_clinical_efficacy_evidence,
     harm_gate_cleared: true, mt: DoseAnchoredSafetyDisclosureMt,
     safety: [epa_water_residual_0p8mgL_characterized, ingestion_dose_uncharacterized, chlorite_hemolysis_methemoglobinemia_vector]}
  - {agent: methylene_blue, timing: during_chemo, evidence_class: preclinical_redox,
     harm_gate_cleared: true, safety: [maoi_serotonin_syndrome, g6pd_hemolysis]}
  - {agent: visualization_mindset, timing: during_treatment, evidence_class: anecdotal_qol, safety: []}
outcome: {expected_response_prob: 0.15, observed: complete_response, class: n1_hypothesis_generating}
confounding_disclosure: simultaneous_multi_intervention__no_single_attribution
```

---

## 7. Redaction & provenance ledger (privacy-guard track-what-was-shared)

**Removed (Layer 3+ → not in this artifact):**
- Patient legal name.
- Treating oncologist's name (third-party PII — cannot be consented away by the patient).
- City-level location → coarsened to region.
- Exact dates / timestamps → coarsened to year/relative sequence.
- Supplement purchase log with prices/order dates (commercial + temporal trail) → omitted; not needed for the clinical seed.
- Exact lab values/timestamps → represented as trend structure only, not reproduced.

**Retained (clinical value, consented):**
- Diagnosis, NED status, biomarkers, treatment sequence, complementary arm, outcome.

**⚠️ Residual combination-risk flag (Layer 2):** diagnosis + specific biomarker
profile + region + approximate timeframe could, in combination, narrow
identification — especially given the patient's related public posting. For any
**public** (Layer 0) release, consider coarsening biomarkers to presence-only and
dropping the timeframe. Acceptable for trusted-research-thread use at the
patient's discretion; flagged here so the decision is conscious.

*Hypothesis-generating, not causal. A harm-surfacing and experiment-tracking
structure, never an efficacy tool or treatment guidance. The method travels with
the data; the why stays with the human.*
