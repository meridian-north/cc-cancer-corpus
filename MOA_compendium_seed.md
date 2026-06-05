# Curated MOA compendium — the HOW seed for the cancer corpus

*A hand-curated mechanism-of-action map of natural/repurposed anticancer agents, drawn
from MSKCC AboutHerbs-class, NCI OCCAM/PDQ-class, and herb-drug-interaction (HDI) review
sources. This is **seed knowledge** that grounds the auto-built mechanism bridge — and
its most load-bearing column is the **interaction / safety** one. Documentation, not
endorsement. Hypothesis-generating; no efficacy verdicts.*

---

## How to read this

Each agent maps to a **mechanism node** (the bridge's join key) + a translation status
(in-vitro / mouse / human) + an **interaction flag** (does it help or *wreck* standard
care). The interaction column is the corpus's patient-safety payload.

## 1. Polyphenols & flavonoids → mostly `metabolic`, `oxidative_stress`, `immune_checkpoint`

| Agent | Key MOA | Node | Translation | ⚠ Interaction |
|---|---|---|---|---|
| Curcumin | NF-κB, COX-2, Notch-1 ↓; mitochondrial apoptosis; MMP ↓ | metabolic / redox | human Phase I/II ≤8g/day; bioavailability-limited | **Induces CYP1A2**; in-vitro antagonism w/ statins (lovastatin) |
| EGCG (green tea) | 20S proteasome inhibition; VEGF/EGFR ↓; DNMT ↓ | perfusion / redox | mouse antiangiogenic; small human cohorts | **Neutralizes bortezomib** (binds boronic-acid proteasome inhibitors) — high-risk |
| Resveratrol | SIRT1 ↑; Akt/mTOR ↓; ribonucleotide reductase ↓ | metabolic | mouse concordant; human bioavailability bottleneck | rapid phase-II conjugation limits human use |
| Quercetin | PI3K/Akt ↓; Hsp70 antagonist; mutant-p53 ↓ | metabolic | synergizes cisplatin in xenografts | piloted with curcumin (ACF reduction) |
| Genistein (soy) | weak ER α/β; tyrosine-kinase + topo-II ↓; NF-κB ↓ | immune / endocrine | **biphasic** | **CONTESTED**: low-dose can *stimulate* ER+ tumors; high-dose inhibits |
| Silibinin (milk thistle) | P-gp efflux ↓; anti-inflammatory | hdi / redox | reduces cisplatin nephrotoxicity; human AST/ALT ↓ | **protective adjuvant** — reduces SOC toxicity |
| Apigenin | STAT3 ↓; GLUT1 ↓; G2/M arrest | metabolic | mouse pancreatic GEMM | early preclinical only |

## 2. Alkaloids & terpenoids → `microtubule_mitosis`, `dna_damage`, `oxidative_stress`

| Agent | Key MOA | Node | Translation | Note |
|---|---|---|---|---|
| Paclitaxel (Taxus) | β-tubulin hyper-stabilization | microtubule | **fully translated → Taxol** | the proof natural-product screens reach approval |
| Camptothecin (Camptotheca) | Topo-I–DNA complex → DSBs | dna_damage | **translated → irinotecan/topotecan** | GI + marrow toxicity |
| Artesunate/artemisinin | iron/heme → ROS; **ferroptosis** | redox | mouse antivascular; small human Phase I | **induces CYP2C19, CYP3A4/5** |
| Berberine | DNA intercalation; Wnt/β-catenin ↓; AMPK ↑ | metabolic | APC(min/+) polyp ↓; human adenoma-recurrence trials | low oral bioavailability |
| Graviola/soursop | annonaceous acetogenins → **Complex I inhibition** | electron_transport | potent in-vitro; small xenograft | atypical Parkinsonism at high dose; antagonism w/ carbamazepine |

## 3. Polysaccharides & adaptogens → `immune_checkpoint`

| Agent | Key MOA | Translation | Note |
|---|---|---|---|
| Turkey tail (PSK/PSP) | β-glucan → TLR4/2; NK + T-cell ↑ | **approved adjuvant in Japan**; human survival w/ gastric/colorectal chemo | strongest evidence in the complementary set |
| Ginseng (ginsenosides) | HPA-axis; IL-6/TNF-α ↓ | **Mayo RCTs: cancer-related fatigue ↓** | no tumor-size effect; validated for performance status |
| Ashwagandha (withaferin A) | vimentin disruption; ROS; HSF1 ↓ | mouse antimetastatic; human QoL | caution: may ↑ testosterone (hormone-sensitive) |
| Astragalus | dendritic maturation; IL-2 ↑ | potentiates IL-2 in mice; cisplatin-toxicity ↓ meta | myelosuppression adjunct |

## 4. Off-label / high-prevalence (the crank-rule class)

| Agent | MOA | Translation | Public signal |
|---|---|---|---|
| Fenbendazole/flubendazole | β-tubulin disruption; glucose-uptake ↓ | mixed mouse (vit-co-dependent); **no controlled human** | viral "Joe Tippens"; veterinary-grade self-sourcing |
| **Amygdalin/laetrile (B17)** | β-glucosidase → **cyanide** → cytochrome-c-oxidase ↓ | **NCI/Mayo (Moertel): ZERO efficacy + cyanide poisoning** | classic case: documented human outcome is *toxicity*, not benefit |
| Mistletoe (Iscador) | lectins → ribosome inactivation; cytokines | European integrative; heterogeneous QoL cohorts | **CONTESTED**: Cochrane — QoL maybe, survival weak/variable |

## 5. Endocrine / microenvironment

| Agent | MOA | Note |
|---|---|---|
| Black cohosh | serotonin/estrogen-like, no breast proliferation | tamoxifen hot-flash relief; **no significant CYP/P-gp impact** (safe co-admin) |
| Cannabis (CBD/THC) | CB1/CB2 → p38 MAPK, PI3K/Akt ↓; autophagy | strong palliative (nausea/pain/appetite); anti-tumor unproven | **⚠ correlated with reduced checkpoint-inhibitor response** (observational) |

## 6. ⚠⚠ HIGH-RISK kinetic interactors — the safety keystone (node: `herb_drug_interaction_cyp_pgp`)

**These don't fight cancer — they break the chemo. This is the most clinically
important table in the corpus.**

- **St. John's Wort** — definitive **CYP3A4 + P-gp inducer** (via PXR). Human PK trials:
  slashes irinotecan AUC **~40%**, also docetaxel + TKIs → standard dosing becomes
  **sub-therapeutic.**
- **Echinacea** — dual CYP3A4 inhibitor/inducer; human cases of **severe myelosuppression /
  platelet drops** with etoposide.
- **High-dose garlic (allicin)** — modulates P-gp; **lowers doxorubicin/tacrolimus**
  plasma levels → treatment-failure risk.
- **EGCG** — neutralizes bortezomib (see §1).
- **Curcumin** — CYP1A2 induction (see §1).
- **Cannabis** — possible reduced ICI response (see §5).

---

## Sources to wire / reference

- **MSKCC AboutHerbs** (mskcc.org/cancer-care/diagnosis-treatment/symptom-management/integrative-medicine/herbs)
  — curated per-herb MOA + interactions; the gold reference for this table.
- **NCI OCCAM / PDQ CAM summaries** — government, peer-reviewed CAM evidence.
- **HDI systematic reviews** — the CYP/P-gp interaction literature (Europe PMC: query class added to `agent_queries.txt`).

*All entries are drawn from open, peer-reviewed indices. Documentation, not endorsement;
no efficacy verdicts; dose-anchored safety on every row; the choice stays with the human.*
