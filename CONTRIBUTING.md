# Contributing

This corpus improves when people with different kinds of knowledge engage with it.
You do not need to be a programmer to contribute.

---

## What kinds of contributions are welcome

**Clinical review of the interaction table**
The `DRUG_HERB_INTERACTION_TABLE.md` is built from published literature, but
clinical judgment about which entries matter most in practice is missing.
If you are a clinician and you see something wrong, understated, overstated,
or missing — open an issue or email meridian.north@pm.me.

**Evidence additions**
If you know of a published paper (with a real DOI or PMID) that belongs in the
corpus and is not there, open an issue with the identifier. We will verify and add it.

**Corrections**
If a claim in any document is wrong — wrong evidence level, wrong mechanism,
wrong drug name — please correct it. Open an issue describing the error and
the correct information with a source.

**Patient and caregiver experience**
If you have direct experience with a drug-herb interaction (confirmed or suspected),
that is a signal worth noting. We cannot use it as evidence in the formal corpus,
but it can guide which questions to prioritize for the literature review.

**Mechanism nodes**
The corpus currently has detailed coverage of the OXPHOS/electron transport node
and the CYP450 interaction layer. Other nodes are less developed:
immunotherapy interactions, DNA repair mechanisms, anti-angiogenic pathways.
If you have expertise in any of these, reach out.

---

## What this corpus does not accept

- Claims without sources
- Testimonials as evidence of efficacy
- Promotion of any specific product or brand
- Content that recommends stopping or starting any treatment without medical supervision

---

## How to contribute technically

The tools are Python, stdlib only, no required packages.

1. Fork the repository
2. Add your contribution (paper, correction, new mechanism bridge)
3. Open a pull request with a clear description of what you added and why
4. Include the DOI or source for any new paper

If you are adding a new mechanism node, model it on `MECHANISM_BRIDGE_electron_transport.md`.

---

## The standard that applies to everything here

One standard for every agent — the same evidence-class lens applied to a chemotherapy
drug and a supplement. Dose-anchored safety on every row. No efficacy verdict implied
by co-location at a mechanism node.

If your contribution meets that standard, it belongs here.

---

*Contact: meridian.north@pm.me*
