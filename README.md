# Conventional & Complementary Cancer Treatments
## A mechanism-organized evidence corpus

**What this is:** A searchable, reproducible database of published research on
cancer treatments — conventional drugs, complementary approaches, and the
interactions between them — organized by the biological mechanism each one targets.

**What it is not:** Medical advice. Treatment recommendations. A ranking of what works.

Every result comes with its evidence level stated. Every claim is traceable to a
published source. The tool organizes; you and your care team decide.

---

## Use it in your browser — no install, no account

**[▶ Open the Cancer Corpus tool](https://meridian-north.github.io/cc-cancer-corpus/)**

A private, point-and-click tool over three linked corpora — the **literature**
(6,358 verified studies and trials, with retractions flagged), the **substances**
(2,628 supplements, herbs, and compounds, each tagged by mechanism and safety flag from
the public-domain USDA Duke database), and **regulated herbals** (agents treated as
medicine in Germany, Japan, and Canada).

It opens by **taking you by the hand** — *check a list you're taking*, *look up one
substance*, or *browse everything* — and every substance leads with a plain-language
summary before any raw data. What it does:

- **Paste-your-regimen matcher** — paste your supplements and herbs; matched entirely in
  your browser. Your list is never uploaded, saved, or sent anywhere — it never leaves your device.
- **"Questions for my doctor" export** — compiles a private, editable sheet of what you
  take, its flags, and the questions to raise with your care team — built on your device.
- **Mechanism "cousins"** — see other substances that act the same way, sorted
  *strongest-evidence-first* and labelled **not equivalents** (evidence strength and
  safety usually matter more than a shared mechanism).
- **Retraction overlay** — see which cited papers were later withdrawn by their publishers.
- **Plain language throughout** — "RCT," "verified," "candidate," "evidence" each explain
  themselves; nothing is left as bare jargon.

It runs entirely in your browser and sends nothing anywhere. Prefer to work offline? Use
the green **Code** button → **Download ZIP**, unzip, and open **index.html**.

> A map of the evidence, not medical advice. A match is not an endorsement; a gap is not a
> verdict; a shared mechanism is a question, never proof of equivalence.

---

## Start here — based on who you are

| I am... | Go to |
|---|---|
| A patient or caregiver | [FOR_A_CANCER_PATIENT.md](FOR_A_CANCER_PATIENT.md) |
| A doctor or clinician | [FOR_A_DOCTOR.md](FOR_A_DOCTOR.md) |
| A researcher | [FOR_A_RESEARCHER.md](FOR_A_RESEARCHER.md) |
| New to all of this | [FOR_A_STRANGER.md](FOR_A_STRANGER.md) |

---

## The headline resource — drug and supplement interaction table

**[DRUG_HERB_INTERACTION_TABLE.md](DRUG_HERB_INTERACTION_TABLE.md)**

A plain-language table of known interactions between common chemotherapy drugs
and supplements, foods, and herbal preparations — organized by the enzyme pathway
and evidence level. Built from published clinical trials and observational studies.

This is the information most oncologists do not have time to compile
and most patients do not know to ask about. Start here.

---

## Ask your own question using AI

**[ASK_AI_YOUR_QUESTION.md](ASK_AI_YOUR_QUESTION.md)**

No coding required. Copy-paste prompt templates that let you ask Claude, ChatGPT,
or any capable AI assistant about your specific drug-supplement interaction,
your treatment mechanism, or your diagnosis — and get organized, evidence-sourced
answers you can bring to your oncologist.

---

## The mechanism index — 6,358 studies you can query

Behind the audience docs is the data layer: a searchable index of **6,358** verified
cancer studies, each tagged by biological mechanism (12 nodes) and tumor type, with an
abstract where openly available and a link to every source. It ships
**index-and-links only** — metadata and tags, never rehosted paywalled full text.

- **[THE_INDEX.md](THE_INDEX.md)** — the data layer: fields, the `query_index.py` tool
  (no setup, no network), and the analytics pack.
- **[MECHANISM_MAP.md](MECHANISM_MAP.md)** — the 12 mechanism nodes, the trigger
  lexicon behind each, and the counts.
- **[BRIDGE_TO_SEVEN_SYSTEMS.md](BRIDGE_TO_SEVEN_SYSTEMS.md)** — how this connects to
  the seven-system pharmacovigilance federation (on concepts, not columns) and to FAERS.
- **[DUKE_TABLES.md](DUKE_TABLES.md)** — the public-domain USDA Duke phytochemical
  database (the complementary-track substrate).

Query it without installing anything:

```
python3 query_index.py --summary
python3 query_index.py --node immune_checkpoint --class rct
python3 query_index.py --crossroads     # mechanism crossroads (oxidative-stress × p53: 500 studies)
```

The lightweight index + samples + analytics live here in `data/`; the full index with
abstracts and the complete Duke database (~44 MB) are on the public Proton mirror.

The mirror is the **`cc-cancer-corpus`** silo on Proton Drive (public, no account, every
file SHA-256 verifiable against `MANIFEST_SHA256.txt`):
<https://drive.proton.me/urls/Z90MDSAQ9W#YhIrSCETc0Zt>

---

## All documents

| Document | Audience | What it covers |
|---|---|---|
| [FOR_A_STRANGER.md](FOR_A_STRANGER.md) | Anyone | What the Warburg effect is; what this corpus does |
| [FOR_A_DOCTOR.md](FOR_A_DOCTOR.md) | Clinicians | CYP450 interactions; why the supplement conversation matters |
| [FOR_A_CANCER_PATIENT.md](FOR_A_CANCER_PATIENT.md) | Patients | How to use this tool without going it alone |
| [FOR_A_RESEARCHER.md](FOR_A_RESEARCHER.md) | Researchers | Citation anomaly detection; co-location findings; open questions |
| [DRUG_HERB_INTERACTION_TABLE.md](DRUG_HERB_INTERACTION_TABLE.md) | Everyone | CYP450 interactions, antioxidant concerns, immunotherapy flags |
| [ASK_AI_YOUR_QUESTION.md](ASK_AI_YOUR_QUESTION.md) | Everyone | Copy-paste AI query prompts |
| [CLINICIAN_ADVISOR_STATEMENT.md](CLINICIAN_ADVISOR_STATEMENT.md) | — | Statement from our clinical advisor (in progress) |
| [DISCLAIMER_AND_SCOPE.md](DISCLAIMER_AND_SCOPE.md) | Everyone | What this tool will and will not do |
| [WHITE_PAPER_DRAFT_v1.md](WHITE_PAPER_DRAFT_v1.md) | Researchers / partners | Full methodology white paper (draft) |
| [MECHANISM_BRIDGE_electron_transport.md](MECHANISM_BRIDGE_electron_transport.md) | Researchers | Electron transport / OXPHOS node analysis |
| [MECHANISM_BRIDGE_perfusion.md](MECHANISM_BRIDGE_perfusion.md) | Researchers | Tumor perfusion node analysis |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contributors | How to add papers, corrections, or feedback |
| [THE_INDEX.md](THE_INDEX.md) | Researchers / everyone | The queryable index: fields, query tool, analytics pack |
| [MECHANISM_MAP.md](MECHANISM_MAP.md) | Researchers | The 12 mechanism nodes + trigger lexicon + counts |
| [BRIDGE_TO_SEVEN_SYSTEMS.md](BRIDGE_TO_SEVEN_SYSTEMS.md) | Researchers | Link to the pharmacovigilance federation + FAERS |
| [DUKE_TABLES.md](DUKE_TABLES.md) | Researchers | USDA Duke phytochemical database: schema + provenance |
| [LICENSING.md](LICENSING.md) | Everyone | The licensing layers (code / index / Duke / abstracts) |

---

## How the tools work

The corpus is built from three Python scripts that run against public databases
(EuropePMC, PubMed, ClinicalTrials.gov):

- **`cancer_discover.py`** — finds papers from neutral international sources
- **`cancer_bridge.py`** — organizes them by mechanism (HOW), not by name
- **`cancer_why_filer.py`** — flags where citation attention diverges from evidence

Running `python3 cancer_bridge.py --node electron_transport_oxphos` returns all
papers in the corpus that act on the electron transport chain — across conventional
drugs, repurposed agents, and complementary compounds — with evidence levels.

The index now **ships with the repo**, so `python3 query_index.py --node
electron_transport_oxphos` runs that query against the shipped data directly — no
intake folder and no network needed. See [THE_INDEX.md](THE_INDEX.md).

No LLMs in the discovery pipeline. Sources are real identifiers verified against
their registries. Full methodology: [WHITE_PAPER_DRAFT_v1.md](WHITE_PAPER_DRAFT_v1.md).

---

## The organizing principle

Most databases organize by **WHAT** (drug name, supplement name). This one
organizes by **HOW** (mechanism of action). That matters because:

- A diabetes drug (metformin) and an antimalarial (atovaquone) appear at the
  same node when both target mitochondrial complex I
- A supplement and a chemotherapy drug can interact via the same enzyme pathway
  (CYP3A4) regardless of their names
- Mechanism is the only shared vocabulary across conventional and complementary medicine

The HOW-join is what makes the garlic problem visible: garlic contains compounds
that speed up the same enzyme that processes docetaxel. That interaction has nothing
to do with whether garlic is "natural" or whether docetaxel is "conventional." It is
just chemistry, and it deserves a conversation.

---

## Status

This corpus is under active development. Evidence levels are explicit and
conservative. Where evidence is limited to preclinical or in vitro studies,
that is stated. Where the evidence is contested, that is stated too.

Current attestation anchor: `358c490` (the prior signed release).
Corpus snapshot: **June 2026** — a point-in-time picture, not live; every row links to a
source you can re-check. The June-2026 reader revision (guided entry, plain-language
summaries, mechanism cousins with the evidence-guard, and the regimen matcher's
doctor-visit export) **ships now and is pending re-attestation** — the next ceremony
re-pins `MANIFEST_SHA256.txt` and records the new anchor.
Last updated: 2026-06-21

---

## Cloning this tool — the shape travels, the proof does not

This is a static HTML webform on purpose: anyone can fork it, fold in new studies,
and host their own version. That openness is a feature — new evidence *should* update
the tool. But a clone inherits the **design**, not the **attestation**, and it's
important to be honest about the difference.

**The canonical Meridian North release carries milspec provenance** a fork does not:

- a `MANIFEST_SHA256.txt` pinning the exact bytes of every data file,
- per-release signing and a two-tier custody chain (private chain → public BSV),
- byte-for-byte reproducibility (same corpus version + same query → same output),
- a recorded attestation anchor (this release: `358c490`).

**A clone or fork has the webform and a copy of the data — and that is all.** It does
*not* carry the SHA manifest, the signing, the custody chain, or reproducibility. Its
data can be edited and can drift silently; its claims are only as good as whoever
maintains it. **A fork must not present itself as carrying the milspec/attestation
guarantees above**, and should state plainly that it is an *unattested copy*. The
design discipline still applies in a fork — evidence is graded, caveats travel with the
data, nothing is recommended — but the *proof* stays with the signed canonical release.

If you clone this: keep this section, change the attestation line to read
"unattested fork," and point users to the canonical release for the verifiable version.

---

## Contact

Questions, corrections, contributions, or collaboration:
**meridian.north@pm.me**

*Not medical advice. Every decision belongs to patients and their care teams.*
