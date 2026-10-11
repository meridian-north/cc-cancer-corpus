# Circadian timing and the Warburg PDH PDK pathway

This bridge helps find published work about biological timing and tumor metabolism. It links the existing metabolic, mitochondrial and redox nodes using **candidate research topics**, while preserving the June snapshot's original mechanism tags and evidence classes. A keyword match is a reason to read a paper, not confirmation of its mechanism or a treatment recommendation.

## Two routes for pyruvate

A simplified pathway, with many omitted regulatory steps:

```text
Glucose -> glycolysis -> pyruvate -> lactate
                           |
                           +-- PDH --> acetyl-CoA --> TCA cycle --> respiration
                                ^
                                | inhibited by phosphorylation
                               PDK
                                ^
                                | can be induced by
                               HIF-1
```

Aerobic glycolysis describes lactate production despite available oxygen. It does not mean every tumor has stopped mitochondrial respiration, or that glucose demand directs a chemotherapy drug selectively into cancer cells. Kim and colleagues demonstrated HIF-1 regulation of PDK1 and reduced pyruvate entry into the TCA cycle in cellular hypoxia experiments. That is a mechanistic result, not a clinical dosing rule. [PMID 16517405](https://pubmed.ncbi.nlm.nih.gov/16517405/), DOI 10.1016/j.cmet.2006.02.002.

## Evidence examples and their limits

| Question | Evidence and result | What it cannot establish |
|---|---|---|
| Can melatonin affect this pathway in a cancer model? | Chen and colleagues studied lung cancer cells and a mouse model; they reported SIRT3/PDH activation and a metabolic shift. **Preclinical**, not a human efficacy trial. [PMID 34214200](https://pubmed.ncbi.nlm.nih.gov/34214200/), DOI 10.1111/jpi.12755. | A useful dose, clinical benefit or preferential carboplatin delivery in humans. The abstract reports increased ROS in these models; “melatonin always lowers ROS” would be inaccurate. |
| Did melatonin protect blood counts during carboplatin plus etoposide? | A double-blind randomized crossover study of **20 patients** found no significant difference in the studied hematologic toxicity outcomes. The study used 40 mg oral evening melatonin for 21 days; this describes the experiment, not a suggested dose. [PMID 10362116](https://pubmed.ncbi.nlm.nih.gov/10362116/), DOI 10.1038/sj.bjc.6690463. | A general safety window, a benefit across regimens, or proof that evening dosing is superior to another time. |
| Does a CYP interaction establish carboplatin clearance interference? | The prescribing label identifies **renal excretion** as the major elimination route and describes bone-marrow suppression including thrombocytopenia. [DailyMed label](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=48aa7ef3-9f44-2a08-e054-00144ff88e88&version=8). | A generic herb/CYP tag does not establish a carboplatin interaction. A bleeding question is separate from a drug-clearance claim. |

These sources do not establish the proposed sequence “healthy cells sleep, cancer cells take the chemotherapy, outdoor heat or exercise concentrates it in the tumor.” A study's treatment timing, efficacy outcome and mechanistic finding are separate claims. No treatment schedule or exercise-in-heat protocol follows from this bridge.

## Query the research topics

```sh
python3 query_index.py --topic circadian_timing --limit 10
python3 query_index.py --topic warburg_pdh_pdk --json
python3 query_index.py --topic antiplatelet_bleeding_risk --json
python3 query_index.py --topic antioxidant_chemo_interaction --json
```

The default topic search examines the public snapshot's titles and available abstracts. It reports **which phrases matched and in which fields**. With an explicit `--csv`, only available CSV fields are searched; the shipped CSV has titles but no abstracts. Negative results, reviews and retracted papers can match: read their source class, source record and result direction. Aggregate results in [TOPIC_COVERAGE.json](TOPIC_COVERAGE.json) describe this frozen snapshot, not all medical literature.

The four topics are retrieval aids, not four newly discovered biological mechanisms. Bare `PDK1` is ambiguous; the rules require additional metabolic context. An agent name alone does not imply a pathway, and two substances sharing a topic are not substitutes.

## Add or revise a topic as evidence changes

1. Compare existing nodes and topics; state the research question and what the new rule adds.
2. Cite primary publications with identifiers, model/population, endpoint, finding and limits. Keep mechanistic proposals distinct from established clinical findings.
3. Add a conservative rule to `mechanism_topics.py`. Rules use OR between alternatives and AND across groups; phrase boundaries avoid substring accidents. Avoid broad acronyms without context.
4. Add positive, negative, ambiguous-acronym and negated-result tests. A negative finding may be a valid retrieval hit, never a positive efficacy inference.
5. Review matched examples and missed known examples; report precision/recall only if a reviewed reference set exists. Update `TOPIC_COVERAGE.json` and disclose changes.
6. Run the [release checks](MAINTENANCE.md). Promoting a candidate topic into a canonical index node requires a separate reviewed retagging, count/analytics rebuild and release record. Never silently rewrite old snapshot membership.

No personal observation is required to propose a topic. Public contributions contain literature and general questions; private clinical notes belong with the person's licensed practitioners.
