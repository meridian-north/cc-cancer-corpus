# FAERS Query-Kit Catalog — ready-to-run methods for Dr. Wei

*openFDA drug-adverse-event API. Public, free, no data stored. Each kit returns
results + method + a pointer to the source. Verified live 2026-06-03; FAERS data
last_updated 2026-04-28. Re-run any time — the API is the source of truth.*

---

## How to use this

Base endpoint: `https://api.fda.gov/drug/event.json`

Two query styles:
- **`count=<field>`** → a small aggregate table (fast, no row data). Use this first.
- **`search=<filter>&limit=N`** → individual reports (read `meta.results.total` for
  the count; raise `limit` up to 1000 for rows; `skip` paginates to 25,000).

Swap the drug name in `search=patient.drug.medicinalproduct:"NAME"` for any agent:
oncology drugs (PEMBROLIZUMAB, CARBOPLATIN, TEMOZOLOMIDE, NIVOLUMAB, …) or
supplements/substances (CURCUMIN, MELATONIN, VITAMIN+D, IVERMECTIN, METHYLENE+BLUE, …).
A free API key raises rate limits; not required for this volume.

**Read every result through the guardrails:** counts are a floor, no denominator, no
causation; high count ≠ caused, low count ≠ safe; report-presence ≠ attribution
(check drug role). These are leads, not verdicts.

---

## Kit 1 — Reaction profile (what was reported)

> The adverse-event fingerprint of a drug.

```
GET /drug/event.json?search=patient.drug.medicinalproduct:"PEMBROLIZUMAB"&count=patient.reaction.reactionmeddrapt.exact
```
*Returns top MedDRA preferred terms by report count. Caveat: the largest "reaction"
is often the disease itself (e.g. "malignant neoplasm progression") — not a drug harm.*

---

## Kit 2 — Drug role (the integrity check)

> Was this drug the suspect, or just present?

```
GET /drug/event.json?search=patient.drug.medicinalproduct:"PEMBROLIZUMAB"&count=patient.drug.drugcharacterization
```
*Codes: 1 = primary suspect · 2 = secondary suspect · 3 = concomitant · 4 = interacting.
**Never attribute an event to a drug coded only concomitant.** This is the kit that
keeps a co-report from becoming a smear.*

---

## Kit 3 — Seriousness / death signal

> How many reports were flagged serious / fatal.

```
GET /drug/event.json?search=patient.drug.medicinalproduct:"PEMBROLIZUMAB"&count=seriousnessdeath
GET /drug/event.json?search=patient.drug.medicinalproduct:"PEMBROLIZUMAB"&count=patient.reaction.reactionoutcome
```
*`seriousnessdeath` term 1 = death-flagged report count. `reactionoutcome` 5 = fatal.
Death-flagged ≠ death-caused. Compare across agents only with the no-denominator
caveat firmly attached.*

---

## Kit 4 — Volume over time

> Reporting trend by year (watch for media/stimulated-reporting spikes).

```
GET /drug/event.json?search=patient.drug.medicinalproduct:"CARBOPLATIN"&count=receivedateyear
```

---

## Kit 5 — Demographics (age & sex distribution)

> Who is being reported on.

```
GET /drug/event.json?search=patient.drug.medicinalproduct:"TEMOZOLOMIDE"&count=patient.patientsex
GET /drug/event.json?search=patient.drug.medicinalproduct:"TEMOZOLOMIDE"+AND+patient.patientonsetageunit:801&count=patient.patientonsetage
```
*`patientonsetageunit:801` = years. Age/weight are present but sparsely filled —
report coverage honestly.*

---

## Kit 6 — Serious outcomes within a reaction

> Cross a drug with a specific adverse event.

```
GET /drug/event.json?search=patient.drug.medicinalproduct:"PEMBROLIZUMAB"+AND+patient.reaction.reactionmeddrapt:"MYOCARDITIS"&limit=1
```
*Read `meta.results.total`. Swap the PT for COLITIS, PNEUMONITIS, HEPATITIS, etc.*

---

## Kit 7 — Supplement / substance co-report (the complementary-track lead)

> Does a supplement appear in cases alongside a chemo agent?

```
GET /drug/event.json?search=patient.drug.medicinalproduct:"CURCUMIN"+AND+patient.drug.medicinalproduct:"CARBOPLATIN"&limit=1
GET /drug/event.json?search=patient.drug.medicinalproduct:"IVERMECTIN"&count=patient.reaction.reactionmeddrapt.exact
```
*Co-occurrence in a report is a **co-report**, not an interaction and not causation.
Flag as a lead to investigate; tag the supplement's drug role (usually concomitant).*

---

## Kit 8 — Primary-suspect-only mortality (the cleaner cut)

> Death-flagged reports where the drug was the primary suspect.

```
GET /drug/event.json?search=patient.drug.medicinalproduct:"PEMBROLIZUMAB"+AND+patient.drug.drugcharacterization:1+AND+seriousnessdeath:1&limit=1
```
*The strictest available role filter — still not causation, but it removes the
"merely present" reports.*

---

## Kit 9 — Reporter country / source

> Where reports originate (reporting systems differ by country).

```
GET /drug/event.json?search=patient.drug.medicinalproduct:"NIVOLUMAB"&count=primarysource.reportercountry.exact
```

---

## Reference oncology cohort (swap-in names)

Checkpoint inhibitors: PEMBROLIZUMAB, NIVOLUMAB, ATEZOLIZUMAB, DURVALUMAB, IPILIMUMAB.
Cytotoxics: CARBOPLATIN, CISPLATIN, TEMOZOLOMIDE, PACLITAXEL, DOCETAXEL, GEMCITABINE.
Targeted: OSIMERTINIB, SOTORASIB (KRAS), TRASTUZUMAB.
Complementary/substances to profile: CURCUMIN, MELATONIN, "VITAMIN D", "VITAMIN C",
MISTLETOE, FENBENDAZOLE, MEBENDAZOLE, IVERMECTIN, "METHYLENE BLUE", "CHLORINE DIOXIDE".

---

## The "results + methods + pointers" contract (what Wei gets back, and gives back)

For any question, the deliverable is three parts, never the raw dump:

1. **Result** — the aggregate table or the `total`.
2. **Method** — the exact query string above (copy-paste reproducible).
3. **Pointer** — `api.fda.gov/drug/event.json`, the FAERS `last_updated` date, and
   (for published artifacts) a SHA-256 of the saved result + an as-of timestamp.

Wei runs these on his own; nothing is stored on our side. When he wants to contribute
a finding to the federation, he contributes the **result + method + pointer** — never
his patients' rows. His private markers and measures stay his.

*Every row inherits: hypothesis-generating only · no denominator · no causation ·
drug-role-aware · dose-anchored safety · efficacy-neutral. Leads, not verdicts.*
