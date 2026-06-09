# Mechanism map — the 12 nodes

The corpus's join key is the **mechanism node**. Each study is tagged by matching a
curated, transparent lexicon of trigger phrases against its title and abstract. A
study can land at more than one node (1,943 do); a study that matches nothing is left
untagged (2,074 are). The tagging makes **no efficacy claim** — it groups by *how* a
thing is proposed to act, never by whether it works.

The lexicon lives, in full and human-readable, in `cancer_bridge.py` (the `NODES`
dict). It is meant to be audited and extended. Below is each node, its count in this
release, and a sample of the trigger phrases behind it.

| Node | Studies | What it groups | Sample triggers |
|---|---|---|---|
| `oxidative_stress_redox` | 2,725 | Reactive-oxygen / redox biology | reactive oxygen species, ROS, glutathione, pro-oxidant, ferroptosis |
| `p53_apoptosis_cell_cycle` | 902 | Tumor-suppressor / programmed cell death / cycle arrest | p53, TP53, apoptosis, MDM2, p21, caspase, BAX, BCL-2, tumor dormancy |
| `immune_checkpoint` | 806 | Checkpoint & T-cell immunology | PD-1, PD-L1, CTLA-4, checkpoint inhibitor, neoantigen, tumor microenvironment |
| `perfusion_vascular_hypoxia` | 691 | Blood flow, angiogenesis, oxygenation | angiogenesis, VEGF, hypoxia, perfusion, reoxygenation, hyperthermia |
| `metabolic_fasting_glycolysis` | 555 | Tumor metabolism | Warburg, glycolysis, fasting-mimicking, ketogenic, AMPK, mTOR, autophagy |
| `cannabinoid_endocannabinoid` | 410 | Cannabinoid / terpene signaling | cannabinoid, CB1, CB2, CBD, THC, TRPV1, anandamide, terpene, limonene |
| `herb_drug_interaction_cyp_pgp` | 362 | **Safety** — drug-clearance interference | CYP3A4, P-glycoprotein, PXR, herb-drug interaction, AUC, enzyme induction |
| `dna_damage_parp` | 277 | DNA-damage response | PARP, homologous recombination, BRCA, synthetic lethality, platinum |
| `electron_transport_oxphos` | 253 | Mitochondrial respiration | electron transport, complex I, OXPHOS, NADH, cytochrome, ATP synthase |
| `microtubule_mitosis` | 110 | Spindle / mitotic machinery | microtubule, tubulin, mitotic, spindle, taxane, benzimidazole |
| `spike_vaccine_cancer_signal` | 74 | **Broad** — COVID/spike + vaccine-cancer literature | COVID-19 vaccination, SARS-CoV-2, spike protein, tumor dormancy, injection site |
| `vaccine_cancer_specifically` | 1 | **Tight** — cancer *specifically* after vaccination | cancer after vaccination, temporal association with COVID-19 vaccination, injection-site lymphoma |

## The two vaccine nodes — broad vs tight, on purpose

`spike_vaccine_cancer_signal` (74) is the **broad** receptor: it catches any study
touching COVID/spike biology *and* the vaccine-cancer discussion, including general
COVID-treatment papers that mention SARS-CoV-2. `vaccine_cancer_specifically` (1) is
the **tight** sub-node: it admits only studies specifically reporting cancer
occurrence, progression, or reactivation in temporal association with vaccination.

The **1:74 ratio is itself data.** Of 6,358 studies, exactly one specifically
addresses the vaccine-associated cancer signal at the time of this release — the
El-Deiry & Kuperwasser 2026 *Oncotarget* systematic review (69 publications, 333
patients, three population cohorts). The tight node makes that distinction
**auditable**: any claim about "what the corpus shows" on this topic must cite the
tight-node count (1), not the broad-node count (74). The node is a receptor; future
papers on the exact topic land there automatically.

## Stratifiers (in the tool, not the flat index)

`cancer_bridge.py` also carries `COHORT` (19 tumor types — melanoma, lung, breast,
glioma/GBM, lymphoma, leukemia, pancreatic, …) and `TUMOR_CONTEXT` facets, so a node
can be sliced by tumor type. The effect **sign** (does an agent help or harm?) is read
from cohort + context, never inferred from co-location at a node — co-location is a
*pattern surface*, not a verdict.

---

*The lexicon is curated and auditable. Counts are membership counts, not evidence of
effect. Grouping is by mechanism, never by works/doesn't.*
