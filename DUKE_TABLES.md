# The Duke Phytochemical & Ethnobotanical Database

The one dataset in this release that ships **in full** (not index-and-links), because
it is **public domain**.

## Provenance

Dr. Duke's Phytochemical and Ethnobotanical Databases were created by the late
**James A. Duke** and are maintained and distributed by the **U.S. Department of
Agriculture, Agricultural Research Service (USDA-ARS)**. As a work of the U.S.
Government, the dataset is in the **public domain** and may be freely redistributed.
It is included here unmodified, as downloaded from the USDA source, so it can be
verified against the original.

It is the **mechanism substrate for the complementary track**: it links plants to the
chemicals they contain, those chemicals to documented biological activities, and
plants to ethnobotanical uses by culture and country — the raw material a mechanism
node is built to organize.

## The 16 tables

| Table | Rows | What it holds | Key columns |
|---|---|---|---|
| `FARMACY_NEW.csv` | 104,388 | Chemical-in-plant-part quantities (current) | FNFNUM, CHEM, PLCO, AMT_LO/HI, QUANT_UNIT |
| `ETHNOBOT.csv` | 82,873 | Ethnobotanical uses by species/country | ETHNO, ACTIVITY, GENUS, SPECIES, COUNTRY, REFERENCE |
| `FARMACY.csv` | 68,844 | Chemical-in-plant quantities (legacy) | FNFNUM, CHEM, AMT_LO, AMT_OR_HI, REFERENCE |
| `CHEMICALS.csv` | 29,585 | Chemical master list | CHEM, CHEMID, CASNUM |
| `AGGREGAC.csv` | 28,929 | Chemical → biological activity → dosage | CHEM, ACTIVITY, DOSAGE, MAJORACT, REFERENCE |
| `CODES.csv` | 8,926 | Plant name/code crosswalk | PLNA, PLCO, AUTHOR |
| `SUPERACT.csv` | 5,358 | Activity → super-activity grouping | SUPERACT, ACTIVITY |
| `CHEM_MEANS.csv` | 3,832 | Per-chemical/part summary stats | chem_id, part_id, avg, std |
| `YIELDS.csv` | 2,824 | Agronomic yield records | LOCNUM, SOURCE, PLCO, YIELDLO/HI |
| `ASSAY.csv` | 2,630 | Assay records | FNFNUM, NAME, REFERENCE |
| `ACTIVITIES.csv` | 2,432 | Biological-activity dictionary | ACTIVITY, DEFINITION, REFERENCE |
| `FNFTAX.csv` | 2,376 | Plant taxonomy | FNFNUM, GENUS, SPECIES, FAMILY |
| `REFERENCES.csv` | 2,056 | Bibliographic references | REFERENCE, LONGREF, NOTE |
| `COMMON_NAMES.csv` | 2,920 | Common ↔ scientific names | CNNAM, FNFNUM |
| `DOSAGE.csv` | 1,627 | Dosage notes per chemical | CHEM, DOSAGE, REFERENCE |
| `PARTS.csv` | 115 | Plant-part code dictionary | PPCO, PPNA |

The join backbone: `FNFNUM` (plant), `CHEM` (chemical), `PLCO`/`PPCO` (plant/part
codes), `ACTIVITY` (biological activity), `REFERENCE` (citation).

## Where to get it

A **50-row sample** of five tables is in `data/duke_sample/` so you can see the schema
here. The **full 16-table set is gzipped on the Proton mirror** (`duke_phytochem/`,
~44 MB uncompressed). Every file is SHA-256 listed in the bundle manifest.

## A use note (and a caution)

This table set documents *what compounds occur in plants and what activities are
recorded for them*. A recorded biological activity is **not** a treatment claim, a
dose recommendation, or a safety clearance. Many plant chemicals are toxic; many
interact with prescription drugs (see the `herb_drug_interaction_cyp_pgp` node in the
literature index). Use it as a reference map, not as guidance.

---

*Public domain (USDA-ARS). Shipped unmodified for verifiability. A reference map, not
medical advice.*
