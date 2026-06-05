---
handle: ponzi_unit
forum: TickerForum
topic: cancer corpus — what came out, what to investigate
---

# A few days of focused work answering decades of questions

I have been sitting with cancer — as a patient, as someone who meets with patients
weekly — for long enough that questions accumulate. Why is this paper being cited
constantly when it only tested cells in a dish? Why is a $4 generic drug not in a
Phase III trial for cancer? Why does my oncologist not have a list of what I'm
taking that might interfere with my treatment?

I built infrastructure to answer those questions. What came out of it surprised me
in a few places and confirmed what I already suspected in others.

The repository: github.com/meridian-north/cc-cancer-corpus

---

## What the corpus actually surfaces

This is not a list of treatments. It is a map organized by **HOW** — biological
mechanism. When you ask the map "what hits the mitochondrial electron transport
chain," you get back something interesting:

- Metformin (a $4 diabetes drug, 60+ years old, no patent)
- Atovaquone (an antimalarial, also generic)
- IM156 (a new biguanide compound in Phase I trials, very much patented)
- DCA (dichloroacetate — no patent, no major pharma sponsor)
- A preprint on metformin + DCA combined (dual metabolic blockade)
- Several plant compounds operating through the same mechanism

These are not equivalent. The evidence levels are very different. But they are
at the same address on the mechanism map, and that convergence is a fact
independent of who makes them or who funds the studies.

The question that follows is the one you're already asking: if metformin and DCA
both hit the same target, and both are off-patent, and a preprint suggests they
work together — why does the preprint exist and not a Phase III trial?

The answer is not mysterious. Phase III trials cost $500M–$2B. They are almost
always funded by companies with financial interest in the outcome. No one makes
that investment for a $4 generic. The structural absence of data is not the same
as evidence that it doesn't work. The corpus makes that absence visible.

---

## The citation anomaly findings — this is where it gets interesting

The corpus runs a "why-filer" — an algorithm that scores papers by how much
attention they receive (citations) relative to how strong their evidence is.

Papers where citations outrun evidence are flagged as **PROMOTION_anomaly**.

From the most recent sweep of the electron transport / OXPHOS mechanism node:

**Anomaly 1:** *Drug Design and Discovery: Principles and Applications*
Anomaly score +5.04. Evidence level 1 (preclinical / methodology). 54 citations.
A textbook-level general principles paper accumulating clinical citations in a
mechanism-specific search. Why? One hypothesis: it's being used to establish
methodological legitimacy for studies that need a citations anchor. The paper
itself may be fine. The question is what specific studies are citing it and why.

**Anomaly 2:** *Recent Progress of Targeted G-Quadruplex-Preferred Ligands
Toward Cancer*
Anomaly score +4.89. Evidence level 2. 195 citations.
G-Quadruplex ligands are a hot research area. Multiple pharmaceutical companies
have active programs. 195 citations on what the corpus classifies as level-2
evidence (likely in vitro or early observational) is worth examining. Who funded
these studies? Where do the citation chains lead?

**Anomaly 3:** *Current trends in drug metabolism and pharmacokinetics*
Anomaly score +4.89. Evidence level 2. 195 citations.
Drug metabolism reviews are frequently cited to establish context for drug-drug
interactions. High citation counts in this category can indicate that certain
interaction profiles are being heavily amplified — or suppressed — in the
literature. Which drug families are most represented in the citing papers?

These are questions, not verdicts. The anomaly is a signal; investigation determines
what it means.

---

## How to investigate citation anomalies yourself

The AI prompt kit in the repository has a specific prompt for this. But here is
the manual path for investigators who want to go deeper:

1. **Find who is citing the anomalous paper.** Use Google Scholar, Semantic Scholar,
   or Scite.ai. Who cites it? Are they industry-funded? Are they in the same
   research network?

2. **Check the funding declarations.** Most papers published after 2010 declare
   funding. Papers with pharma funding citing low-evidence papers in a hot
   treatment area warrant scrutiny.

3. **Check the retraction history.** The why-filer flags this automatically.
   Retracted papers that continue to be cited (zombie citations) are a known
   problem and a documented mechanism for keeping discredited findings in play.

4. **Compare the evidence level to the claim.** When a clinical paper cites a
   cell-line study as support for a mechanism claim, that is a
   mismatch — sometimes legitimate, sometimes not. The corpus makes the
   evidence level visible so you can spot the mismatch.

5. **Map the citation network.** If the same low-evidence paper is being cited
   by the same cluster of researchers and institutions, that is a network
   effect. Concentrated citation networks in a commercial research area are
   worth examining.

---

## On open source vs. pharma-backed research infrastructure

There is a structural problem in cancer research that this forum understands: the
people who fund clinical trials are the people who benefit from their outcomes.
Open-source research infrastructure — tools that any investigator can run, with
methods that any investigator can inspect — does not solve this problem, but it
makes the gap visible.

The citation anomaly detection runs against public databases using transparent
methods. The evidence classification is lexicon-based and auditable. Any
investigator can run the same tools against the same data and either confirm or
challenge what the corpus shows. That reproducibility is the point.

On AI tools: I use Claude primarily because of Anthropic's stated commitment to
independent, non-military-aligned AI development. I cannot verify that claim
fully. I can observe that the output I get from it does not appear to optimize
for any particular research agenda. If that changes, the corpus methodology does
not depend on any specific AI — it runs against public databases with open code.
The tool is the method, not the model.

---

## The drug-herb interaction table — a non-controversial entry point

Before the deeper investigation, there is something immediately usable for anyone
here who is navigating cancer treatment or knows someone who is.

The repository contains a drug-herb interaction table organized by the enzyme
pathways through which chemotherapy drugs are metabolized. This is not
controversial. These interactions are published in clinical trials. The table
simply assembles them in one place in plain language.

The specific finding worth knowing: Echinacea, taken as a supplement, has been
shown in a clinical trial to meaningfully reduce blood levels of docetaxel —
because it induces the enzyme that metabolizes the drug. Most people on docetaxel
do not know this. Most oncologists do not have this list on the wall.

That is the gap the tool is addressing.

---

## What I'm looking for from this forum

People who want to run the citation anomaly queries against specific papers.

People who want to add to the interaction table — if you know of an interaction
that is not on the list, with a published source, open an issue or email me.

People who have encountered the publication bias problem from the inside — who
have seen studies suppressed or promoted in ways that don't match the evidence.
The corpus can be pointed at any mechanism node. If there is an area you want
examined, name it.

The tool asks the why. You investigate.

github.com/meridian-north/cc-cancer-corpus

— ponzi_unit
