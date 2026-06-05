# Conventional & Complementary Cancer Treatments: a reproducible, neutral evidence layer

### A white paper — first draft

*GarrisonNode × the clinical partner. Prepared by jr for our clinical advisor,
DOM AP. Draft v1, 2026-06-03. For partner review — not for publication.*

---

## Abstract

Cancer patients rarely receive only conventional care. Most also run a second,
largely undocumented track — supplements, diet, fasting, off-label agents, lifestyle
changes — alongside surgery, chemotherapy, radiation, and immunotherapy. That second
track is where the data goes dark: it is unrecorded, unstandardized, and surrounded
by claims no one can check. This paper proposes a single, honest structure for both
tracks at once. It does not store anyone's data, does not rank treatments, and does
not issue verdicts on what works. It surfaces **results, methods, and pointers** —
reproducible from public sources, cryptographically checkable, and bound by explicit
safety and neutrality guardrails. The aim is to let conventional and complementary
oncology be tracked side by side, honestly, so that patterns can be raised as
questions worth a controlled look — and so that the people at the edges of the data
are met by a human, while the machine handles the core.

---

## 1. The problem

Real-world oncology has two tracks and only one of them is recorded.

The **conventional track** — staging, surgery, regimens, response — is captured in
clinical records and, in aggregate, in registries. The **complementary track** — what
the patient adds on their own — is captured almost nowhere. When it is discussed, it
is discussed in the worst possible register: testimonials with no method, or
dismissals with no data. Both fail the patient.

Three structural facts make this hard, and they are the same facts that make passive
surveillance hard generally:

1. **No denominator.** A report, a forum post, or a case series tells you something
   happened; it cannot tell you how often, because the exposed population is unknown.
   Counts are a floor, never a rate.
2. **Confounding is total.** A patient fighting for survival rationally stacks
   interventions. No single change can be credited or blamed from one person's course.
3. **The claims are uncheckable.** "It cured me" and "it's a scam" are both verdicts
   that outrun the evidence, and neither can be reproduced by a stranger.

The response to all three is not a better opinion. It is a better **structure**.

---

## 2. What we are (and are not)

GarrisonNode is a **toolmaker, not a custodian.** It supplies a grammar, a set of
query tools, and an attestation pipeline. It does **not** collect or store patient
data, and it asks no one to surrender theirs.

- **We store the public layer, point to the rest.** We keep what is free and
  open — the verified **metadata + abstract** of each study (the analyzable
  who/what/where/when/how, SHA-256 hashed) and **open-access full text where the
  license permits** — and for everything paywalled we keep only a **verified
  pointer** (the resolvable DOI/NCT/PMID, a hash, and an as-of date), never the
  locked file. Every result also ships with its **method** (the exact, reproducible
  query). A reviewer re-pulls and re-verifies; we never hold anyone's paywalled or
  private data.
- **We do not rank treatments or issue efficacy verdicts.** No "scam," no "cure" —
  from the model or from anyone. We report evidence class and stop.
- **We surface harm honestly and symmetrically** — every agent, conventional or
  complementary, carries a dose-anchored safety clause.

This is the federated model: every contributor — a clinician, a registry, a
researcher — stays sovereign over their own data. What crosses is the **grammar and
the method**, not the records.

---

## 3. The two-track envelope

Both tracks share one structure, so they can sit in the same table without being
confused for one another.

**Conventional track** — the attested standard-of-care record: modality sequence
(surgery / immunotherapy / chemotherapy / radiation / regimen changes), each tagged
with its evidence class (standard-of-care, regulatory-approved). The harm-gate here
is inherent: clinician-directed and monitored.

**Complementary track** — the self-directed experiment, recorded **alongside, not
instead of** the conventional track. Each entry carries: the agent, its timing
relative to conventional treatment, an **evidence class** (regulatory-approved /
phase-trial / observational / preclinical / anecdotal / no-evidence), a
**harm-gate-cleared** flag (did a clinician confirm "no harm"?), and a mandatory
**dose-anchored safety clause**.

**Outcome signal** — the observed result, recorded with a **mandatory confounding
disclosure**: when multiple interventions changed at once, no single one can be
credited. This is not a weakness to hide; it is the reason a federation of tracked
cases matters — what one patient cannot disentangle, many tracked cases can begin to.

A fully worked, de-identified example of this envelope ships with this package
(`seed_record_public_GN-CASE-LUNGADENO-0001.md`): a real lung-adenocarcinoma course,
NED, with both tracks populated and the confounding disclosed.

---

## 4. The guardrails

These are not legal boilerplate. They are what makes the structure safe for a
vulnerable audience and credible to a skeptical one.

**Dose-anchored, symmetric disclosure.** Every agent carries a safety clause —
conventional, OTC, supplement, complementary alike. None gets a free pass; none gets
a scarlet letter. The clause states whether the therapeutic window is
**characterized** (a known safe dose and toxic threshold) or **uncharacterized** —
not "safe vs. dangerous." *Worked example:* chlorine dioxide is an EPA-regulated
drinking-water disinfectant, characterized-safe at ≤0.8 mg/L residual; its
therapeutic-ingestion dose is far higher and uncharacterized, with the chlorite
byproduct (hemolysis, methemoglobinemia) as the dose-dependent vector. The compound's
name is not the hazard; the dose-in-context is.

**Counts do not rank danger.** Raw adverse-event counts confound usage volume,
reporting channel, and real toxicity, with no denominator. *Illustration* (openFDA
FAERS, death-flagged reports, as of 2026-04-28): acetaminophen 100,607; aspirin
54,691; ivermectin 325; methylene blue 242; chlorine dioxide 2. High counts are not
"caused"; low counts are not "safe" (a substance not regulated as a drug surfaces its
poisonings in Poison Control and case reports, not FAERS). The numbers are leads,
never rankings.

**Efficacy neutrality, bidirectional.** No party issues an efficacy verdict. We
report that one thing has a phase-III trial and another has only anecdote — that is
required honesty, not a verdict — and we refuse the editorial leap to "works" or
"doesn't."

**Non-abandonment, with a limit.** We do not stop engaging with someone because they
make a choice we would not. We surface the harm facts and keep informing; the
decision stays with the patient and their clinician. But non-abandonment is **not**
facilitation: we never author or encourage harm, and never suppress the harm facts to
please the listener.

---

## 5. The demonstration (FAERS oncology)

The method already runs. Using the public openFDA API, a single query returns the
real adverse-event profile for an oncology drug — no bulk download, no data stored.

*Pembrolizumab (Keytruda), as of 2026-04-28:* 33,812 reports; role distribution
overwhelmingly **primary suspect** (33,740) vs. concomitant (183); a textbook
checkpoint-inhibitor immune-mediated profile (colitis, pneumonitis, hepatitis,
myocarditis, hypophysitis, adrenal insufficiency) — with the single largest "reaction"
being the **cancer itself progressing**, the clearest possible reminder that a count
is a lead, not a verdict.

The same one-line method applies to carboplatin, temozolomide, the immunotherapy
families, and any supplement or substance the advisor's clients use — including the
supplement–drug **co-report** signals (flagged as leads to investigate, never as
interactions). The catalog of ready-to-run queries ships with this package
(`FAERS_QUERY_KIT_CATALOG.md`).

---

## 6. The partnership

This is a collaboration between equals contributing different things.

- **jr** donates time and funding to the work (as he has before), and
  brings the substrate — the grammar, the tools, the attestation.
- **our clinical advisor** brings clinical partnership and domain judgment — the expertise
  that keeps the method honest, relevant to real patients, and safe. His specific
  markers and measures remain **his**, private and proprietary.

Neither surrenders data. the advisor runs the tools on his own data, on his own machine, and
keeps what is his. What he contributes to the federation, if anything, is
public-derivable or aggregate — never the raw private dimensions.

**A longer horizon (aspiration, not a promise):** as the shared structure gains depth
across many contributors and a time axis, zero-knowledge proofs could one day let a
private dimension answer a federated query *without revealing the underlying records*
— federation enforced by mathematics, not just policy. That needs depth and time to
build; it is named here as direction, not current capability.

---

## 7. What success looks like

Not a verdict, and not a database. Success is that a clinician, a patient, or a
skeptic can take any number in this work, follow the method, re-pull the data from
its public source, and get the same answer — and that conventional and complementary
care finally sit in the same honest table, with the harms stated plainly, the
evidence classed honestly, and the human left to decide. The machine takes care of
the core so the people can care for the edges.

---

*Draft v1 for partner review. Hypothesis-generating, not causal. Not medical advice;
not an efficacy claim. Prepared for our clinical advisor, the clinical partner, by GarrisonNode.*
