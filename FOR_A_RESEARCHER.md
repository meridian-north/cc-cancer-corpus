# For a Researcher — What This Corpus Can and Cannot Offer

*For oncology researchers, integrative medicine investigators, pharmacologists,
and data scientists working in the cancer treatment space.*

---

## The structural problem this corpus addresses.

Conventional and complementary oncology research live in different journals,
different databases, and different epistemic communities. A pharmacologist
studying OXPHOS inhibitors and a researcher studying quercetin's
mitochondrial effects are studying the same pathway. They almost never
cite each other.

This corpus attempts one specific intervention: **organize both bodies of
literature by mechanism** and surface them together, classified by evidence
quality, without editorializing about their relative merit.

The result is not a meta-analysis. It is a **map of the mechanistic
neighborhood** — which agents cluster at the same node, what the evidence
distribution looks like across evidence types, and where citation patterns
may be outrunning the underlying evidence.

---

## What "organized by mechanism" means operationally.

Each agent in the corpus is tagged by mechanism of action (HOW). Tags are
derived from title and abstract using a lexicon-matched classifier — transparent,
auditable, and imperfect. The tagging is a starting point for human review,
not a verdict.

For the `electron_transport_oxphos` node specifically, the corpus contains
papers across the following evidence classes:

- **Clinical trials (RCT and interventional):** metformin + radiotherapy
  (NCT04945148), IM156 Phase I/II, BPM31510IV Phase Ia/b (Warburg effect),
  atovaquone in DIPG, DCA in pulmonary arterial hypertension (crossover
  evidence), PDK inhibition in pulmonary hypertension as proxy for PDH
  activation signal
- **Observational studies:** atovaquone-induced OXPHOS disruption in multiple
  tumor lines, metformin CYP450 interactions, OXPHOS dependency in endocrine
  therapy-resistant breast cancer
- **Preprints (not peer-reviewed):** metformin + DCA dual metabolic blockade,
  breast cancer DCA responsiveness
- **Narrative reviews:** synthesis literature on OXPHOS as cancer target,
  mitochondria-targeted nanomedicine, redox-cycling mitocans

Complementary agents co-located at this node through the same mechanism
lexicon: quercetin, artemisinin derivatives, palladium-lipoic acid complex
(POLY-MVA), atovaquone-coordinated copper-polyphenol nanoplatforms, certain
Annona extracts (acetogenins), CoQ10-alpha-lipoic acid formulations.

---

## The citation anomaly signal — where this corpus adds analytical value.

The why-filer component runs a promotion-anomaly scan: it computes expected
citation counts by evidence class (reviews are normed against reviews; primary
studies against primary studies) and surfaces papers where observed citation
weight is significantly higher than stratum-expected.

In the most recent corpus sweep, three papers were flagged at the OXPHOS node:

- *Drug Design and Discovery: Principles and Applications* (anomaly +5.04,
  54 citations, evidence level 1) — high textbook-style citation in a
  mechanisms-focused search
- *Recent Progress of Targeted G-Quadruplex-Preferred Ligands Toward Cancer*
  (anomaly +4.89, 195 citations, ev=2) — G-quadruplex ligand literature
  co-cited heavily with OXPHOS work; may reflect a cross-mechanism citation
  pattern worth investigating
- *Current trends in drug metabolism and pharmacokinetics* (anomaly +4.89,
  195 citations, ev=2) — heavy pharmacokinetic co-citation

The anomaly is a question, not a verdict: **why is this paper cited here at
this rate?** Possible reasons — textbook status, methodological anchor,
citation network artifact, genuine mechanistic relevance not fully captured
by the lexicon. Each warrants examination.

**Independence-of-confirmation (citation graph analysis)** is the identified
next enhancement: mapping whether high-citation papers are genuinely
independent confirmations or citation echo chambers.

---

## The complementary/conventional co-location finding.

The most structurally interesting output of the mechanism-organized approach
is that **legitimate complementary agents appear at the same node as
FDA-approved and Phase II/III drugs** — not by claim, but by mechanism.

POLY-MVA (palladium-alpha-lipoic acid complex) appears alongside metformin,
atovaquone, and IM156 at the OXPHOS/mitochondrial redox node. The published
literature on POLY-MVA is sparse (primarily observational and preclinical),
but its mechanistic basis is not contested: palladium-dithiooctanoate operates
on mitochondrial electron transfer chemistry. Whether this translates to
clinical anticancer activity is an open question.

The value of surfacing this co-location is not advocacy for POLY-MVA.
It is the observation that **if OXPHOS targeting is the mechanism, and if
POLY-MVA operates on that mechanism, then a properly powered trial comparing
POLY-MVA to a comparator in the same mechanistic class would be more
informative than continuing to study it in isolation.** The map creates
the hypothesis. The trial tests it.

---

## Evidence gaps the corpus surfaces.

1. **Combination studies at this node are sparse in humans.** Metformin + DCA
   is studied in preclinical models and in a preprint. IM156 is post-Phase I.
   The clinical co-targeting of glycolysis and OXPHOS simultaneously is
   largely uncharacterized in randomized settings.

2. **The complementary literature at this node is almost entirely preclinical.**
   Quercetin's mitochondrial effects, artemisinin's electron transport
   disruption, acetogenin OXPHOS inhibition — these have preclinical signals
   but essentially no rigorously controlled human data.

3. **Patient self-reported n=1 data is completely absent** from the formal
   evidence base. An unknown but large number of patients are self-administering
   DCA, POLY-MVA, high-dose quercetin, and metformin off-label. This data
   exists — in forums, support groups, practitioner records — but is not
   captured or analyzed.

4. **Drug-herb interaction studies at this mechanism** — how does concurrent
   use of OXPHOS-active supplements affect the pharmacokinetics of OXPHOS-
   targeting chemotherapy? Almost no literature directly addresses this.

---

## The open-source layer.

The literature discovery, evidence classification, mechanism tagging, and
citation anomaly detection are open-source Python, running against public
APIs (EuropePMC, PubMed, ClinicalTrials.gov). The methodology is documented
in the repository.

If you want to run the same analysis on a different mechanistic node, extend
the lexicon, or challenge the evidence classification — the tools are available
and the invite is genuine. That is what CorrectMeIfImWrongMt means in practice:
the finding is held provisionally, and external challenge via reproduction
is the right response.

---

*Evidence sourced from public databases. Classification transparent and auditable.
No efficacy verdict implied by co-location at any mechanistic node.
Contact: meridian.north@pm.me*
