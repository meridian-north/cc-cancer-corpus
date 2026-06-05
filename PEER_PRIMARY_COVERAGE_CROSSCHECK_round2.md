# Peer crosscheck — round 2: PRIMARY-evidence coverage over the AC360 surface

*Paste the per-peer blocks below to Gemini and Grok. Round 1 verified the four seed items and
sourced general feedstock. Round 2 has a narrower, higher-value job: our own sweep now biases
toward primary evidence (ClinicalTrials.gov + pubType-filtered Europe PMC across the agent query
list), but a keyword sweep misses studies our terms don't name. **Your job is coverage:** surface
the Phase 2/3/4 trials, primary human cohorts, and high-value preclinical that EXIST for the AC360
domains below and that a keyword sweep would likely miss. You return verifiable pointers; we verify,
evidence-class, mechanism-tag, and score downstream. Same guardrails as round 1.*

*Context for both peers — AC360 supports the **person's own choice**; it does not recommend,
prescribe, or disparage chemo/radiation. Two support tracks frame the corpus:*
- *TRACK 1 — help people get fit enough to **survive** conventional treatment (tolerance / supportive care).*
- *TRACK 2 — if conventional treatment is **declined**, support with the "kitchen sink."*
*One standard for every agent: evidence-class + mechanism + dose-anchored safety. Voicing is not
endorsing. We privilege the HOW (mechanism) as the join key; we do not dwell on the WHY.*

---

## The six AC360 coverage domains (find primary evidence our keywords would miss)

1. **Supplement × conventional-treatment INTERACTIONS — both directions.**
   - *Supportive (Track 1):* agents that **reduce** chemo/radiation toxicity or protect normal
     tissue (e.g., glutamine/mucositis, melatonin/side-effects, glutathione/neuropathy, probiotics/
     enteritis, amifostine-class cytoprotection).
   - *Contraindication (the safety keystone):* agents that **blunt** efficacy or are hazardous in
     combination (e.g., antioxidants during radiotherapy, St John's Wort/CYP3A4, EGCG/bortezomib).
   - We want the trials and cohorts that actually measured an interaction endpoint, not reviews.
2. **Redox cycling** — alternating pro-oxidant ↔ antioxidant phases ("confuse the cancer"):
   pharmacological ascorbate (IV vitamin C) pro-oxidant trials, menadione, artesunate, auranofin/
   thioredoxin, redox-modulation chemo-sensitization. Human trials especially.
3. **Exercise & rest oncology** — prehabilitation, exercise during chemo (completion/tolerance/
   survival endpoints), resistance training for cachexia, cancer-related-fatigue RCTs, sleep/
   circadian and outcomes.
4. **Mind-body / low-stress / positive reinforcement / biofield** — MBSR and immune/outcome
   endpoints, psychological-stress-and-progression cohorts, social-support-and-survival, qigong/
   tai-chi RCTs, and the biofield/energy-healing literature **including its preclinical animal
   work** (e.g., Bengston mouse mammary-tumor reports) — voiced, not endorsed, sparse returns
   recorded honestly.
5. **Named formulations (Track 2 kitchen-sink)** — Poly MVA (palladium–lipoic-acid complex),
   high-dose/IV vitamin C protocols, mistletoe (Iscador/Viscum) survival cohorts, hyperthermia
   adjunct trials, and any registered trials for Essiac/Gerson-class regimens.
6. **High-value preclinical (the mouse scoreboard).** Prized: **PDX / "mouse avatars"**, then
   GEMM/syngeneic, then cell-line xenograft, then in-vitro — and most valuable of all,
   **translation-DISCORDANCE** (strong in mice, failed/untested in humans). Those are research
   questions, not failures.

---

## PASTE TO GEMINI ↓

You are the systematic-coverage second source for a neutral, reproducible cancer-treatment evidence
corpus (conventional + complementary). We never single-source: an item is "confirmed" only when two
independent agents verify it. We are a toolmaker, not a custodian — we keep **pointers + methods +
results**, not stored papers. No efficacy verdicts ("scam"/"cure"); prestige-blind; count
*independent* confirmations (a citation ring is one source wearing many names). **Confidence is not
verification — return only pointers you retrieved this session; mark anything else `UNVERIFIED`.
An UNVERIFIED item is welcome; a confident-but-unchecked citation is the one thing we can't use.**

**Your edge: systematic registry + PubMed breadth.** For each of the six AC360 domains above, work
ClinicalTrials.gov and PubMed/Europe PMC methodically and bring back the **primary** evidence
(Phase 2/3/4 trials, prospective/observational cohorts, case series) plus the high-value preclinical
(PDX/discordance) — concentrating on items a keyword sweep of the agent list would **miss**: trials
indexed under a synonym, a drug class, or a combination name our single-agent terms wouldn't catch.
Aim for 12–20 items spread across the six domains; flag which domain each fills and whether our
keyword would likely have caught it (`coverage: likely_missed | likely_caught`).

## PASTE TO GROK ↓

You are the latest-readout second source for the same corpus, same guardrails (toolmaker not
custodian; pointers+methods+results; prestige-blind; independent-confirmation, not virality; no
scam/cure verdicts; voicing not endorsing; **confidence is not verification — mark UNVERIFIED if you
couldn't open it this session**).

**Your edge: X.com + the freshest layer.** For the six AC360 domains, surface what's **newest** —
recent trial readouts, fresh preprints (bioRxiv/medRxiv), new retractions (Retraction Watch), and
the widely-consumed public claims patients are actually acting on — that our keyword sweep would
miss. Two hard rules on anything found on X: **(a) the post is a lead, not a source** — resolve it
to a verifiable primary pointer (DOI / preprint / NCT / regulator doc) or mark `UNVERIFIED`;
**(b) virality = public_consumption_signal, NOT independence** — retweets never count as
confirmations. Aim for 10–15 items across the six domains, flagging the domain and
`coverage: likely_missed | likely_caught`.

---

## Output schema (one row per item; preclinical rows add the last three fields) — both peers

```
- title_or_citation:
  ac360_domain:            # interactions_supportive | interactions_contraindication | redox_cycling
                           #  | exercise_rest | mind_body_biofield | named_formulation | preclinical
  coverage:                # likely_missed (our keyword wouldn't catch it) | likely_caught
  source_class:            # phase_trial | observational | small_human_cohort | preclinical_mouse
                           #  | in_vitro | retracted | widely_consumed_public
  primary_pointer:         # NCT id / DOI / PMID — the VERIFIABLE source (not a tweet, not a review URL)
  discovered_via:          # clinicaltrials | pubmed | crossref | x.com | retraction_watch | other
  retrieval_status:        # VERIFIED (resolved this session) | UNVERIFIED
  publicly_accessible:     # yes | paywalled | restricted
  evidence_class:          # regulatory_approved | phase_trial | observational | small_cohort
                           #  | preclinical | anecdotal | no_evidence
  independence_assessment: # single_source | citation_ring | independent_n>=2 | independent_n>=3
  public_consumption_signal:   # for widely-consumed claims: evidence of scale + a pointer
  # --- preclinical-only fields ---
  model_class:             # pdx_avatar | gemm | syngeneic | cell_line_xenograft | in_vitro
  human_concordance:       # concordant | discordant | untested_in_human  (+ pointer to the human result)
  discordance_question:    # if discordant: the "why didn't it translate" question it raises
  # --- shared ---
  four_w_one_h:            # who(cohort/model) / what / where / when / HOW (mechanism)  — NO why verdict
  good_questions:          # 2-3 checkable questions
  your_confidence:         # high/med/low + exactly how you verified the primary pointer this session
```

## Hard rules (both peers)
Real, resolved pointers only — never fabricate a DOI or NCT id; mark `UNVERIFIED` if you couldn't
open it. Prefer freely accessible. No efficacy verdicts, no medical advice. Mark `CONTESTED` and
give both sides where sources conflict. The HOW (mechanism) is what we join on — fill it; leave the
WHY to us. Where your labels and ours disagree, say so plainly — disagreement is signal, not failure.

## ↑ END PASTE
