# Conventional & Complementary Cancer Treatments — partner package for Dr. Gene Wei

*Prepared by GarrisonNode (jr / John Reed, L4) for Dr. Gene Wei, DOM AP — AntiCancer360.
First-draft package, 2026-06-03. Method-and-tools, not a data store.*

---

## What this package is

A first draft of the partnership deliverable: a white paper, a worked de-identified
seed record, and a catalog of ready-to-run adverse-event query methods. The premise
is the **two-track** view of real-world oncology — **conventional** treatment and the
**complementary** interventions patients actually run alongside it — given a single
honest, reproducible structure.

## The goal, in one line

Take messy public adverse-event and treatment data and make it **organized,
reproducible, and cryptographically checkable** — so conventional and complementary
oncology can be tracked side by side, honestly, without anyone surrendering their
data and without anyone issuing a verdict on what "works."

## The partnership (fair deal)

- **jr → Wei:** donates time and money to the collaboration (as in the past).
- **Wei → the toolset:** lends clinical partnership and support — the domain
  expertise that keeps the method honest and useful to patients and clinicians.
- **Neither party surrenders data.** Wei keeps his patients' records and his
  proprietary markers/measures. GarrisonNode supplies the grammar, the tools, and
  the attestation. Toolmaker, not custodian.

## What's in this folder

| File | What it is |
|---|---|
| `WHITE_PAPER_DRAFT_v1.md` | The first-draft white paper — goals, method, guardrails, demonstration. |
| `FAERS_QUERY_KIT_CATALOG.md` | A multitude of ready-to-run openFDA/FAERS query methods Wei can pull himself. |
| `seed_record_public_GN-CASE-LUNGADENO-0001.md` | A worked, **de-identified** single-patient seed showing the two-track envelope. |

## Privacy boundary — read this

This folder contains the **public, de-identified** seed only. Per the data-sovereignty
discipline this project runs on (**public-source default; private data never enters a
syncable tree**), the **identified private copy** of jr's seed is delivered to
Dr. Wei **out-of-band** (direct hand-off), not stored here. Dr. Wei already holds
jr's raw records; the private envelope is the same structure with identity restored,
delivered separately so no identified medical data lands in a repository.

## The operating model — results, methods, pointers (not data)

GarrisonNode does **not** store anyone's data. For every question, it returns:

1. **Results** — the aggregate numbers / extracts.
2. **Methods** — the exact query and procedure, reproducible byte-for-byte.
3. **Pointers** — where the data lives (e.g., the openFDA endpoint, the source's
   release ID), with hashes/as-of dates so a reviewer can re-pull and re-verify.

That's the whole offer: the path is public and checkable; the data stays at its source.

## The guardrails (non-negotiable, and they protect the patients)

- **DoseAnchoredSafetyDisclosureMt** — every agent (conventional, OTC, supplement,
  complementary) carries a dose-anchored safety clause; none gets a free pass or a
  scarlet letter; the clause states whether the therapeutic window is characterized.
- **EfficacyNeutralityMt** — no "scam," no "cure," from anyone. Evidence class is
  reported; verdicts are not.
- **DrugSafetyClauseMt** — passive surveillance is hypothesis-generating only; no
  denominator, no causation, drug role carried on every row, alongside-not-instead-of.

*Hypothesis-generating, not causal. A harm-surfacing and experiment-tracking
structure — never an efficacy tool or treatment guidance. The method travels with
the data; the why stays with the human.*
