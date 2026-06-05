# Gemini feedstock-sourcing prompt — v2 (refined: verification + mouse/cohort scope)

*Paste the block below to Gemini. Supersedes v1. Adds a kind verification reminder and
the small-cohort / mouse-study scope with translation scoring.*

---

## PASTE TO GEMINI ↓

Thank you for the first feedstock pass — your *selection* was excellent (the classes,
the independence flags, the fenbendazole/Joe-Tippens public-consumption read were all
spot-on). One honest note, kindly meant, because our whole method runs on it: two of
your pointers didn't survive verification. The bioRxiv preprint
`10.1101/2024.01.15.575631` (fasting-mimicking diet + MEK in KRAS lung) does not
resolve and no matching preprint exists — it appears to have been generated rather
than found. And the curcumin/Notch-1 retraction is real, but the citation was wrong:
the actual retracted paper is in the journal *Cancer* (Wiley), doi
`10.1002/cncr.21904` (Wang, Sarkar et al., 2006) — not *Cancer Letters* / a 2016 DOI;
that was conflated with the separate Bharat Aggarwal retraction cluster. No harm done
— our verification layer is *designed* to catch exactly this, and it did. It just
means one rule from here on:

**Return only pointers you actually retrieved this session. If you could not open and
confirm a source right now, mark it `UNVERIFIED` and say so — never assert
retrievability you haven't confirmed. A source marked UNVERIFIED is welcome; a
confident-but-unchecked citation is the one thing we can't use.** Confidence is not
verification.

Everything else from before still holds: prestige-blind; count *independent*
confirmations (a citation ring is one source wearing many names); track public
prevalence for low-merit-but-widely-consumed claims and include those so we can score
them; never issue "scam"/"cure" verdicts — classify evidence and raise good
questions; voicing is not endorsing.

### New scope for this pass: small cohorts and mouse/lab studies

Add these classes, because mechanism mostly lives in preclinical work and we don't
want to throw the biology away:

- **Small human cohorts** — single-center series, 10–50 patient studies, case series.
- **Mouse / preclinical studies** — including, prized highest, **patient-derived
  xenografts (PDX / "mouse avatars")**, then GEMMs, syngeneic models, then generic
  cell-line xenografts, then in-vitro.

Mouse studies are scored on a **separate scoreboard**: not "weak human evidence," but
*how well their model class has historically correlated with human outcomes.* And the
most interesting finding is **discordance** — where a strong mouse result did **not**
translate to humans. Flag those; they're research questions, not failures.

### Output schema (extends v1 — add the last three fields for preclinical rows)

```
- title_or_citation:
  source_class:                 # + small_human_cohort | preclinical_mouse | in_vitro
  pointer:                      # real & retrieved THIS SESSION, or mark UNVERIFIED
  retrieval_status:             # VERIFIED (opened this session) | UNVERIFIED (could not confirm)
  publicly_accessible:
  public_consumption_signal:
  independence_assessment:      # single_source | citation_ring | independent_n>=2 | independent_n>=3
  evidence_class:               # regulatory_approved | phase_trial | observational | small_cohort | preclinical | anecdotal | no_evidence
  # --- preclinical-only fields ---
  model_class:                  # pdx_avatar | gemm | syngeneic | cell_line_xenograft | in_vitro
  human_concordance:            # concordant | discordant | untested_in_human  (+ pointer to the human study if known)
  discordance_question:         # if discordant: the "why didn't it translate" question this raises
  # --- shared ---
  four_w_one_h:                 # who(=cohort or model) / what / where / when / how  (NO why verdict)
  why_removed_or_contested:
  good_questions:
  your_confidence:              # high/med/low + exactly how you verified the pointer this session
```

### Same hard constraints
Real, retrieved pointers only (mark UNVERIFIED otherwise — do not fabricate DOIs);
prefer freely accessible; no efficacy verdicts / no medical advice; manageable
illustrative set per class; mark CONTESTED and give both sides when sources conflict.

Return the structured list. You are sourcing and verifying feedstock; we score and
distill it downstream.

## ↑ END PASTE
