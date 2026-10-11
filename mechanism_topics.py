"""Conservative, explainable research-topic retrieval over a frozen corpus.

These are candidate keyword matches, not validated mechanism assignments. Existing
mechanism_nodes and evidence classes are never rewritten by this module.
"""
import re
import unicodedata

VERSION = "1"
TOPICS = {
    "circadian_timing": {
        "label": "Circadian biology and treatment timing",
        "parents": ["metabolic_fasting_glycolysis", "electron_transport_oxphos"],
        "rules": [
            [["circadian", "chronotherapy", "chronomodulated", "chronomodulation", "chronotherapeutic"]],
            [["melatonin"], ["evening", "nocturnal", "timing", "light at night", "nighttime"]],
        ],
    },
    "warburg_pdh_pdk": {
        "label": "Warburg metabolism and the PDH / PDK axis",
        "parents": ["metabolic_fasting_glycolysis", "electron_transport_oxphos", "perfusion_vascular_hypoxia"],
        "rules": [
            [["warburg", "aerobic glycolysis", "pyruvate dehydrogenase"]],
            [["pdh", "pdk", "pdk1", "pdk4", "sirt3"], ["glycolysis", "glycolytic", "pyruvate", "hif-1alpha", "hif1a"]],
        ],
    },
    "antiplatelet_bleeding_risk": {
        "label": "Platelet function and bleeding questions",
        "parents": ["herb_drug_interaction_cyp_pgp"],
        "rules": [
            [["antiplatelet", "platelet aggregation", "bleeding", "thrombocytopenia"],
             ["garlic", "ginkgo", "fish oil", "supplement", "supplements", "herbal", "chemotherapy", "carboplatin", "cisplatin"]],
        ],
    },
    "antioxidant_chemo_interaction": {
        "label": "Antioxidants alongside chemotherapy",
        "parents": ["oxidative_stress_redox", "herb_drug_interaction_cyp_pgp"],
        "rules": [
            [["antioxidant", "antioxidants", "pro-oxidant", "prooxidant", "redox"],
             ["chemotherapy", "chemotherapeutic", "carboplatin", "cisplatin", "doxorubicin", "paclitaxel", "etoposide"]],
        ],
    },
}


def normalize(text):
    text = unicodedata.normalize("NFKC", text).casefold().replace("α", "alpha")
    text = re.sub(r"[‐‑‒–—−]", "-", text)
    return re.sub(r"\s+", " ", text)


def contains(text, phrase):
    # A bare ROS/PDK substring must not match prose/protein names by accident.
    return re.search(r"(?<!\w)" + re.escape(normalize(phrase)) + r"(?!\w)", text) is not None


def match_topic(row, topic):
    """Return rule evidence, or None. AND across groups, OR within a group/rules.

    Title and abstract are inspected separately: a match cannot be manufactured by
    joining the end of a title to the beginning of an abstract. Negations and study
    direction are not interpreted; users must read the original paper.
    """
    fields = {key: normalize(row.get(key) or "") for key in ("title", "abstract")}
    evidence = []
    for number, groups in enumerate(TOPICS[topic]["rules"], 1):
        hits = []
        for alternatives in groups:
            group_hits = [{"phrase": term, "field": field}
                          for term in alternatives for field, text in fields.items()
                          if contains(text, term)]
            if not group_hits:
                break
            hits.extend(group_hits)
        else:
            evidence.append({"rule": number, "hits": hits})
    if not evidence:
        return None
    return {"topic": topic, "status": "candidate_keyword_match",
            "text_scope": "title_and_abstract" if row.get("abstract") else "title_only",
            "rules": evidence}
