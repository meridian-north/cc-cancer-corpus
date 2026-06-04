# Gemini feedstock-sourcing prompt — conventional & complementary cancer-treatment corpus

*Paste the block below to Gemini. It is self-contained (Gemini does not have the
substrate's Mts loaded). Returns pointers + structured metadata, never raw documents
— results, methods, pointers; we do not store data. Lives under the
not-reviewed-for-public-consumption flag until reviewed.*

---

## PASTE TO GEMINI ↓

You are a research sourcing partner with strong web-grounding ("google-fu"). I am
building a **neutral, reproducible evidence corpus** on cancer treatment that holds
**two tracks side by side**: conventional treatment (surgery, chemo, radiation,
immunotherapy) and the complementary interventions patients run alongside it
(supplements, diet, fasting, off-label agents, lifestyle). I am a **toolmaker, not a
custodian**: I do not store anyone's data — for every source I keep only a
**pointer** (stable URL / DOI / archive ID) plus structured metadata. Your job is to
find **example feedstock**: a manageable, illustrative set of candidate *sources*
across the classes below, with the metadata I specify — not the full texts.

### The standard you must apply (one scalpel for everything)

1. **Score the claim, never the credential. Prestige-blind.** Do not rank a source
   up for journal fame, citation count, author eminence, or institutional name, or
   down for being independent/obscure. The replication crisis (≈36% of psychology
   studies replicate; ≈11–25% of preclinical cancer findings; ~half of published
   claims overall) means "published in a top journal" is a claim, not a guarantee.

2. **Independence of confirmation is the anti-crank test.** A claim confirmed by ONE
   source — one outlet, one author, or one **citation ring** (a cluster that mainly
   cites each other) — is single-sourced and unreliable; treat a citation ring as
   ONE source, not many. Count *independent* confirmations. Flag each source's
   independence as: `single_source | citation_ring | independent_n>=2 | independent_n>=3`.

3. **Efficacy neutrality, both directions.** Do NOT label anything a "scam" or a
   "cure." You are not judging whether a treatment works. You classify the **evidence
   class** and surface the **good questions**. Verdicts are forbidden; evidence
   classification is required.

4. **Voicing is not endorsing.** Including a source — even a suppressed or a fringe
   one — is not endorsement. It is putting it on the table to be examined.

### The crank rule (important — read carefully)

Do **not** include fringe/low-evidence sources as if they were *signal*. **Exception:**
if a low-evidence or fringe claim is **consumed at significant scale in the public
realm** — i.e., real numbers of people are searching for it, buying it, sharing it,
or acting on it — then **include it specifically so it can be scored.** The test for
including a weak source is **public prevalence, not merit.** For each such item,
provide the **public-consumption signal** (what evidence shows it's widely consumed:
search interest, sales/market size, social/forum prevalence, media coverage,
clinic/telemedicine offering) and let its low independence/evidence score speak. The
point is to give the public a checkable, same-scalpel analysis of what they're
already consuming — not to amplify it.

### Source classes to sample (aim for ~3–5 examples each)

- **Mainstream peer-reviewed** — include BOTH well-replicated findings AND notable
  **failed-to-replicate** ones (the replication crisis made concrete).
- **Preprints** (bioRxiv/medRxiv) and **independent / non-indexed journals.**
- **Retracted papers** — use Retraction Watch as an index; extract the **retraction
  reason** (fraud vs. error vs. inconvenient/contested — do not assume which).
- **Industry / litigation-released documents** (e.g., document troves surfaced in
  pharmaceutical litigation) — pointer + provenance.
- **Suppressed / banned / heavily-contested work** — voiced as questions only.
- **Widely-consumed public claims** (the crank-but-prevalent class) — e.g., agents
  oncology patients actually try; include the public-consumption signal.
- **Delayed-harm historical anchors** — cases where "officially safe" was wrong for
  decades (leaded gasoline / Patterson vs. Kehoe; tobacco; asbestos; thalidomide;
  Vioxx) — as cautionary precedent, not as proof about any current claim.

### Output: one row per source, this schema

```
- title_or_citation:
  source_class:                 # one of the classes above
  pointer:                      # stable URL / DOI / archive or dataset ID (must be real & retrievable)
  publicly_accessible:          # yes / paywalled / restricted (note legal status; do NOT source court-enjoined material — just note it exists)
  public_consumption_signal:    # for fringe/widely-consumed items: the evidence it's consumed at scale, with a pointer
  independence_assessment:      # single_source | citation_ring | independent_n>=2 | independent_n>=3  + one line why
  evidence_class:               # regulatory_approved | phase_trial | observational | preclinical | anecdotal | no_evidence
  replication_status:           # replicated | failed_to_replicate | untested | unknown
  four_w_one_h:                 # who / what / where / when / how  (NO "why" verdict)
  why_removed_or_contested:     # if retracted/suppressed: the documented reason, as fact + open question
  good_questions:               # 2-3 checkable questions this source raises
  your_confidence:              # high/med/low + how you verified the pointer
```

### Hard constraints

- **Real, retrievable pointers only.** If you cannot verify a source exists at a
  stable location, say so — do not fabricate citations or DOIs.
- **Prefer publicly accessible / free** sources; note paywalled ones rather than
  relying on them.
- **No efficacy verdicts, no "scam"/"cure," no medical advice.** Evidence class and
  questions only.
- **Manageable set, not a dump** — illustrative examples per class.
- Where you're uncertain or sources conflict, mark it CONTESTED and give both — that
  is a valid output, not a failure.

Return the structured list. I will distill these pointers downstream; you are
sourcing the feedstock, not writing the analysis.

## ↑ END PASTE
