# First-scan kits — round 1 (what the corpus surfaces from the verified feedstock)

*The analytical output to send back to Gemini + Grok. Not verdicts — structured
comparisons + good questions, each anchored to a confirmed pointer. This is what
"distilling the feedstock" produces. Hypothesis-generating only; no efficacy claims.*

---

## Scan 1 — The matched translation pair (the headline)

The corpus's `PreclinicalTranslationScoringMt` makes this comparison first-class: two
targeted-therapy stories in overlapping space, opposite translation outcomes.

| | **Iniparib** (discordant) | **Daraxonrasib** (concordant) |
|---|---|---|
| Pointer | DOI 10.1158/1078-0432.CCR-11-1973 | NCT06625320 (RASolute 302) + NEJM 2026 |
| Preclinical signal | "PARP inhibitor," strong in cell-line xenografts | RAS(ON) inhibition, strong preclinical |
| Human outcome | **Phase III TNBC FAILURE** | **OS 13.2 vs 6.7 mo (HR 0.40), Phase III** |
| Why | wasn't even a real PARP inhibitor (non-selective cysteine modifier) | RAS pathway hit translated |
| model_class | cell_line_xenograft | (clinical; preclinical lineage RAS(ON)) |
| human_concordance | **discordant** | **concordant** |

**The good question the pair raises:** what distinguishes a preclinical signal that
*translates* (daraxonrasib) from one that *evaporates* (iniparib)? Iniparib's tell was
mechanistic — the model reported target engagement that wasn't real. The corpus's job is
to flag that *mechanism-mismatch* class early, on every preclinical row, via the
`discordance_question` field.

## Scan 2 — Partial concordance (the most honest kind)

**Autogene cevumeran** (mRNA neoantigen PDAC vaccine) — DOI 10.1038/s41586-024-08508-4,
Nature 2024, 3-year follow-up.

- Preclinical: strong immunogenicity predicted.
- Human: **~half (8/16) of patients developed a T-cell response**; responders had
  durable, prolonged recurrence-free survival; non-responders did not.
- `human_concordance: partial` — neither clean success nor clean failure.
- **discordance_question (high value):** why do most *predicted* neoantigens fail to
  elicit a response in humans? (This is the translation-prediction gap, and it's exactly
  the kind of "why" the corpus forks off rather than papering over.)
- ⚠ *Do not inherit the secondary gloss:* Grok cited "~16% of neoantigens trigger T
  cells" — unconfirmed; the verified source reports the patient-level ~50% response.
  The row carries the verified figure, not the gloss.

## Scan 3 — High public-consumption, thin evidence (the crank-rule case)

**DCA / dichloroacetate, glioblastoma** — DOI 10.1126/scitranslmed.3000677, 5-patient
open-label cohort, 2010.

- evidence_class: `small_cohort` · independence: `single_source`.
- **public_consumption_signal: high** — large off-label DCA self-treatment footprint.
- Included *because* it's widely consumed, scored honestly: a 5-patient, single-source,
  15-year-old cohort.
- **good_question:** why has DCA never scaled past tiny cohorts in 15 years — a signal
  that didn't hold, a funding/IP gap, or an unanswered question? The corpus surfaces the
  question; it does not answer it.

## Scan 4 — The retraction case (voicing ≠ endorsing)

**Curcumin/Notch-1** — DOI 10.1002/cncr.21904, journal *Cancer*, retracted for
figure/data integrity.

- We carry both 4W1Hs: the paper's claim **and** the documented reason for removal.
- **good_question:** does curcumin→Notch-1 suppression replicate when independent labs
  re-run it with unmanipulated, open-data blots? (The claim isn't dismissed; it's
  re-opened as a checkable question — the retraction reason was *integrity*, which is
  separable from whether the underlying biology is real.)

---

## What this demonstrates (the message to the peers)

From five confirmed pointers, the corpus produced: one matched success/failure
translation pair, one honest partial-concordance with a sharp "why," one
widely-consumed-but-thin claim scored without dismissal, and one retraction re-opened as
a question — **all neutral, all pointer-anchored, all hypothesis-generating, zero
efficacy verdicts.** That is the product: not answers, a checkable map. Send more
pointers and the map grows.

*Sources are the confirmed DOIs/NCT in `feedstock_round1.json`. Method travels with the
data; the why stays with the human.*
