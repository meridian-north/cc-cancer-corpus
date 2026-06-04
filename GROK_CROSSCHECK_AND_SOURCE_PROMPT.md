# Grok prompt — independent cross-check of the four + source more (X.com discovery)

*Paste the block below to Grok. Two jobs: (A) independently verify the four items
Claude already checked, and (B) bring back MORE feedstock, using X.com as the
latest-research discovery layer Grok is uniquely good at. Same guardrails as the
Gemini pass.*

---

## PASTE TO GROK ↓

You're the independent second source for a neutral, reproducible cancer-treatment
evidence corpus (conventional + complementary). We never single-source: an item is
"confirmed" only when two independent agents verify it. Claude did the first pass; you
are the cross-check **and** an additional sourcer. We are a toolmaker, not a
custodian — we keep **pointers + methods + results**, not stored papers. No efficacy
verdicts ("scam"/"cure"); classify evidence and raise good questions. Voicing is not
endorsing.

### Job A — independently verify these four (do NOT trust my labels; check them yourself)

For each, resolve the DOI, confirm the real title/journal/year, and say whether you
**agree or disagree** with the assessment. If you can't open and confirm it this
session, mark it `UNVERIFIED` — confidence is not verification.

1. **Iniparib (translation failure, discordant):** DOI `10.1158/1078-0432.CCR-11-1973`
   — "Iniparib Nonselectively Modifies Cysteine-Containing Proteins… Is Not a Bona
   Fide PARP Inhibitor," *Clin Cancer Res* 2012. Claim: strong in cell-line xenografts,
   failed Phase III TNBC; mechanism = non-selective cysteine modifier, not a PARP
   inhibitor. Confirm the mechanism + the Phase III failure independently.
2. **Garrido-Laguna PDX (concordant, prognostic):** DOI `10.1158/1078-0432.CCR-11-0341`
   — "Tumor engraftment in nude mice… predict poor survival and gemcitabine resistance
   in pancreatic cancer," *Clin Cancer Res* 2011;17:5793-5800. Confirm DOI + that the
   concordance is *prognostic* (engraftment predicts poor outcome), not "avatar drug
   response matched patient."
3. **DCA / glioblastoma (small human cohort):** DOI `10.1126/scitranslmed.3000677`
   — "Metabolic Modulation of Glioblastoma with Dichloroacetate," *Sci Transl Med* 2010,
   5-patient cohort. Confirm DOI + cohort size; note the large off-label public footprint.
4. **Curcumin/Notch-1 (retracted):** DOI `10.1002/cncr.21904` — journal *Cancer* (Wiley),
   Wang/Sarkar 2006, retracted for figure/data integrity. Confirm the DOI + the
   retraction reason.

Report per item: `agree | disagree | unverified` + what you found + how you checked.

### Job B — source MORE, and use X.com for the latest

Bring 8–12 new candidate sources across the classes below. **X.com is your edge:**
researchers announce preprints, trial readouts, and retractions on X before they're
widely indexed — use it as the **discovery layer**. But apply two hard rules to
anything found on X:

- **The tweet is a lead, not a source.** Every X-discovered item must resolve to a
  **verifiable primary-source pointer** (DOI / preprint / ClinicalTrials.gov ID /
  regulator doc). Record that primary pointer, not the post. If it doesn't resolve,
  mark `UNVERIFIED`.
- **X virality = public_consumption_signal, NOT independence.** A claim going viral on
  X is high public-prevalence and **single-source** until the primary source is
  independently confirmed. Never let retweets count as confirmations.

Classes (aim for a spread): latest preprints (bioRxiv/medRxiv), recent trial readouts
(ClinicalTrials.gov), fresh retractions (Retraction Watch), small human cohorts,
mouse/preclinical (esp. **PDX avatars**, and **translation-discordant** results —
strong in mice, failed in humans — those are the most valuable), and widely-consumed
public claims patients are acting on (include with their public-consumption signal so
we can score them).

### Output schema (one row per item; preclinical rows add the last three fields)

```
- title_or_citation:
  source_class:            # mainstream | preprint | retracted | small_human_cohort | preclinical_mouse | widely_consumed_public | industry_litigation
  discovered_via:          # x.com | crossref | pubmed | clinicaltrials | retraction_watch | other  (+ the X post URL if applicable)
  primary_pointer:         # DOI / preprint / NCT id — the VERIFIABLE source, not the tweet
  retrieval_status:        # VERIFIED (resolved this session) | UNVERIFIED
  publicly_accessible:     # yes | paywalled | restricted
  public_consumption_signal:   # for viral/widely-consumed: the evidence of scale + a pointer
  independence_assessment: # single_source | citation_ring | independent_n>=2 | independent_n>=3
  evidence_class:          # regulatory_approved | phase_trial | observational | small_cohort | preclinical | anecdotal | no_evidence
  model_class:             # (preclinical) pdx_avatar | gemm | syngeneic | cell_line_xenograft | in_vitro
  human_concordance:       # (preclinical) concordant | discordant | untested_in_human (+ pointer to the human result)
  discordance_question:    # (preclinical, if discordant) the "why didn't it translate" question
  four_w_one_h:            # who(cohort/model) / what / where / when / how  (NO why verdict)
  good_questions:          # 2-3 checkable questions
  your_confidence:         # high/med/low + how you verified the primary pointer this session
```

### Hard rules
Real, resolved pointers only — never fabricate a DOI or NCT id; mark UNVERIFIED if you
couldn't open it. Public/no-cost sources preferred. No efficacy verdicts, no medical
advice. Where you and Claude's labels disagree, say so plainly — disagreement is
signal, not failure.

## ↑ END PASTE
