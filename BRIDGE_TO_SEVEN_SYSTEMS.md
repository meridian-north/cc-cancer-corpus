# Bridge to the seven-system pharmacovigilance federation

This corpus has a sibling: an open, seven-system **pharmacovigilance federation** —
VAERS, V-Safe, MHRA (UK), TGA (Australia), the Pfizer C4591001 trial, JADER (Japan),
and CVAR (Canada), all projected into one shared 69-column schema so a single query
reaches all seven
([github.com/meridian-north/vaers-1990-2026-searchable](https://github.com/meridian-north/vaers-1990-2026-searchable)).
This document is about how the two relate — and, just as importantly, how they do not.

## They do not share columns

The pharmacovigilance federation is **tabular**: seven adverse-event reporting systems
sharing a 69-column schema, so one query reaches all seven *because they share
columns*. That is a columnar join.

This cancer corpus is **not tabular in that sense**. It is peer-reviewed literature
(bibliographic metadata + mechanism tags) plus the public-domain Duke phytochemical
database. It has no 69-column schema and **no row-level join** with the adverse-event
systems. Anyone who claims the cancer corpus "joins" the VAERS rows is wrong.

## They bridge on concepts, terms, and one live API

What the two share is **vocabulary** — the names of conditions, symptoms, drugs, and
biological processes. That is the bridge, and it is conceptual:

- A **MedDRA adverse-event term** in the pharmacovigilance data (a cardiac,
  hematologic, hepatic event) is a *concept*. The same concept appears here as a
  **mechanism node** (`p53_apoptosis_cell_cycle`, `immune_checkpoint`, …) or a
  **tumor-cohort** tag or a study's subject matter.
- So the path is: *adverse-event term* → *shared concept* → *mechanism node* → *the
  studies that discuss the proposed biology* — and back again. You travel from "what
  was reported" to "what mechanism might explain it" by a shared name, never a join.

There is also a **live API bridge already in this repo**: `FAERS_QUERY_KIT_CATALOG.md`
runs the FDA FAERS drug-adverse-event system (openFDA) on the *same* MedDRA-term and
drug-role vocabulary. So a drug or supplement in this corpus can be cross-referenced —
by name and by reaction term — against FAERS on demand, with the same guardrails
(counts are a floor, drug-role-aware, no denominator, no causation).

## What the bridge is good for, and not

**Good for:** hypothesis navigation. A signal in the federation (a term across
systems) points you, by concept, at the mechanistic literature here — and the tight
`vaccine_cancer_specifically` node points back at what surveillance does and does not
capture.

**Not good for:** any quantitative claim crossing the two. You cannot compute a rate,
ratio, or correlation across a tabular surveillance system and a literature corpus.
*Report* counts (the federation) and *paper* counts (here) are not commensurable, and
the bridge never pretends they are.

## In one line

The seven systems federate on **columns**; this corpus connects to them on
**concepts** (and to FAERS through a live API on shared terms). One is a join; the
other is a cross-reference. Keeping that distinction sharp is what keeps both honest.

---

*A conceptual cross-reference, not a data join. Report counts and paper counts are not
commensurable. Hypothesis-generating; not medical advice.*
