#!/usr/bin/env python3
"""
cancer_why_filer.py — the WHY-filer for the cancer corpus (the substrate's why-filer
pattern, ADR-204 two-layer split, pointed at the literature).

It does NOT judge whether a study is true. It flags the MISMATCH between a study's
EVIDENCE and its ATTENTION, and forks the *why* as questions:

  * SUPPRESSION anomaly — strong evidence but little/negative attention
        (retracted, buried, low citations relative to quality)  ->  why suppressed?
  * PROMOTION anomaly   — weak evidence but lots of attention
        (heavily cited / hyped relative to quality)             ->  why promoted?

Evidence proxy = evidence_class (from source_class). Attention proxy = Europe PMC
citation count (+ retraction flag). Independence-of-confirmation is the next
enhancement (needs the citation graph). v1 is transparent and auditable.

Reads ~/cancer_intake/files/*.meta.json. Emits ~/cancer_intake/why_anomalies.json.
Stdlib only, polite. Run:  python3 cancer_why_filer.py
"""

import json, os, glob, time, math, urllib.request, urllib.parse
from collections import defaultdict

INTAKE = os.path.expanduser("~/cancer_intake")
FILES = os.path.join(INTAKE, "files")
UA = "GarrisonNode-WhyFiler/1.0 (cancer research)"
DELAY = 1.0
NOW_YEAR = time.gmtime().tm_year
_last = 0.0

# A PROMOTION anomaly means "lots of attention, weak evidence" — attention proxy is the
# citation count, so it CANNOT fire without real attention. This absolute floor kills the
# v1 noise where a low-evidence (ev=2) item with ~0 citations scored PROMOTION purely
# because its z_evidence was more negative than its z_attention. Tune as the corpus matures.
MIN_PROMOTION_CITES = 5

# Symmetric to the promotion floor, on the SUPPRESSION side: a paper must have had TIME to be
# cited before "few citations" means "buried" rather than "new". A 0-citation systematic review
# from this year is young, not suppressed. Only items at least this many years old are eligible
# for a SUPPRESSION flag. Tune as the corpus matures.
MIN_SUPPRESSION_AGE_YEARS = 3

# Evidence ceiling for a PROMOTION flag: "over-promotion" means weak evidence drawing outsized
# attention, so it must NOT fire on top-tier evidence (ev > this) however heavily cited — a
# much-cited RCT / systematic review / meta-analysis is appropriate attention, not hype. Mirror
# of the SUPPRESSION z_att<0 guard. ev<=4 keeps observational/literature/preclinical eligible.
MAX_PROMOTION_EVIDENCE = 4

# evidence rank by source_class (transparent; tune as the corpus matures)
# The EBM-ish ordering is what gives the anomaly score a real evidence axis: a top-tier
# meta-analysis at ev=6 with high citations is ALIGNED (not over-promoted), while a narrative
# review or in-vitro claim at ev=1-2 with the same citations correctly lights up as PROMOTION.
# pubType-derived classes (meta_analysis ... commentary) are assigned by cancer_discover.classify_pubtype.
EVIDENCE_RANK = {
    "regulatory_approved": 6, "phase3_trial": 6, "meta_analysis": 6, "systematic_review": 6,
    "phase_trial": 5, "rct": 5, "clinical_trial": 5,
    "trial_registry": 4, "observational": 4,
    "small_human_cohort": 3, "small_cohort": 3, "international_literature": 3,
    "preprint": 2, "preclinical": 2, "preclinical_mouse": 2, "narrative_review": 2, "case_report": 2,
    "in_vitro": 1, "anecdotal": 1, "commentary": 1,
    "no_evidence": 0, "retracted": 0,
}

# Attention strata — citations are NOT comparable across article types (reviews are cited
# several times more than primary research regardless of quality, a bibliometric constant).
# So attention (z_attention) is scored WITHIN a stratum of like kinds, not globally; otherwise
# the 445 narrative reviews in this corpus swamp the PROMOTION list just for being reviews.
# Evidence rank stays GLOBAL (it's an absolute 0-6 scale). Grouping is by attention behavior,
# NOT evidence tier — narrative + systematic + meta reviews share one stratum because they
# cite alike; their evidence difference is carried by z_evidence.
STRATA = {
    "review":      {"narrative_review", "systematic_review", "meta_analysis"},
    "primary":     {"rct", "clinical_trial", "observational", "small_human_cohort",
                    "small_cohort", "case_report", "phase_trial", "phase3_trial",
                    "regulatory_approved"},
    "preclinical": {"preclinical", "preclinical_mouse", "in_vitro", "preprint"},
}
MIN_STRATUM = 5   # below this a stratum can't support a z-score; those rows fall back to global

def stratum_of(source_class):
    c = (source_class or "").lower()
    for name, members in STRATA.items():
        if c in members:
            return name
    return "general"   # international_literature, commentary, anecdotal, no_evidence

def _get(url):
    global _last
    w = DELAY - (time.time() - _last)
    if w > 0: time.sleep(w)
    _last = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception:
        return None

def epmc_handle(meta):
    """Return (source, extid) for the Europe PMC citations endpoint, from the stored id/doi/pmid."""
    mid = (meta.get("id") or "")
    if mid.startswith("epmc_"):
        parts = mid.split("_")
        if len(parts) >= 3:
            return parts[1].upper(), parts[2]
    # fall back: look the record up by DOI/PMID
    ident = meta.get("identifier"); kind = meta.get("id_kind")
    if kind == "doi" and ident:
        d = _get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="
                 + urllib.parse.quote(f'DOI:"{ident}"') + "&format=json&resultType=lite&pageSize=1")
        res = (d or {}).get("resultList", {}).get("result", [])
        if res: return res[0].get("source", "MED"), res[0].get("id")
    if kind == "pmid" and ident:
        return "MED", str(ident)
    return None, None

def citation_count(source, extid):
    if not source or not extid: return None
    d = _get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{source}/{extid}/citations?format=json&pageSize=1")
    if d is None: return None
    return d.get("hitCount", 0)

def epmc_core(source, extid):
    """Fetch the Europe PMC core record (carries pubTypeList + commentCorrectionList)."""
    if not source or not extid:
        return None
    d = _get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="
             + urllib.parse.quote(f"EXT_ID:{extid} AND SRC:{source}")
             + "&resultType=core&format=json&pageSize=1")
    res = (d or {}).get("resultList", {}).get("result", [])
    return res[0] if res else None

def retraction_status(meta, source, extid):
    """'confirmed' | 'suspected' | 'none'. Only 'confirmed' fires SUPPRESSION_retracted.

    v1 grepped 'retract' in the title and fired — which flagged a paper that merely
    DISCUSSES retraction (the unconfirmed physical-activity flag). v2 uses the title grep
    only as a cheap screen: a hit is 'suspected', and we then CONFIRM against Europe PMC's
    own retraction marking (a retraction pubType, or a commentCorrection of retraction type)
    before firing. EPMC silence on a suspected item leaves it 'suspected' — recorded, not
    accused. Conservative by design: we under-flag rather than wrongly brand a paper retracted.
    The cheap screen means we only pay the extra EPMC fetch for the handful of suspects."""
    t = ((meta.get("title") or "") + " " + (meta.get("source_class") or "")).lower()
    if "retract" not in t:
        return "none"
    rec = epmc_core(source, extid)
    if rec:
        pubtypes = " ".join((rec.get("pubTypeList", {}) or {}).get("pubType", []) or []).lower()
        if "retract" in pubtypes:
            return "confirmed"
        for cc in ((rec.get("commentCorrectionList", {}) or {}).get("commentCorrection", []) or []):
            if "retract" in (cc.get("type", "") or "").lower():
                return "confirmed"
    return "suspected"

def zscores(vals):
    xs = [v for v in vals if v is not None]
    if len(xs) < 2: return {i: 0.0 for i in range(len(vals))}
    mu = sum(xs)/len(xs)
    sd = (sum((x-mu)**2 for x in xs)/len(xs))**0.5 or 1.0
    return {i: ((v-mu)/sd if v is not None else 0.0) for i, v in enumerate(vals)}

WHY_PROMOTION = ["single-source or citation-ring amplification?", "commercial / funding interest?",
                 "media / social virality outrunning the data?", "paradigm convenience?"]
WHY_SUPPRESSION = ["retraction reason — fraud/error (legitimate) or inconvenient?",
                   "superseded by better work, or buried?", "funding / IP gap?",
                   "contradicts an established paradigm or industry interest?"]

def main():
    metas = []
    for p in glob.glob(os.path.join(FILES, "*.meta.json")):
        try:
            metas.append(json.load(open(p)))
        except Exception:
            pass
    if not metas:
        print(f"No .meta.json in {FILES}. Run the scraper/bridge first."); return
    print(f"why-filer: scoring {len(metas)} verified studies (evidence vs attention)...")

    rows = []
    for m in metas:
        ev = EVIDENCE_RANK.get((m.get("source_class") or "").lower(), 3)
        src, ext = epmc_handle(m)
        cites = citation_count(src, ext)
        rstatus = retraction_status(m, src, ext)   # 'confirmed' | 'suspected' | 'none'
        yr = int(m.get("year") or NOW_YEAR) if str(m.get("year") or "").isdigit() else NOW_YEAR
        cpy = (cites / max(1, NOW_YEAR - yr + 1)) if cites is not None else None
        rows.append({"id": m.get("id"), "title": m.get("title"), "pointer": m.get("pointer"),
                     "source_class": m.get("source_class"), "year": yr,
                     "evidence_rank": ev, "citations": cites, "citations_per_year": cpy,
                     "retracted": rstatus == "confirmed", "retraction_status": rstatus})

    # retraction is its own signal, regardless of citation data
    for r in rows:
        r["anomaly"] = None
        r["class"] = "SUPPRESSION_retracted" if r["retracted"] else "pending"
        r["why_questions"] = WHY_SUPPRESSION if r["retracted"] else []

    # citation-attention scoring ONLY over items with a real count, excluding trials
    def scoreable(r):
        return (not r["retracted"] and r["citations"] is not None
                and (r["source_class"] or "").lower() != "trial_registry")
    sc = [r for r in rows if scoreable(r)]
    if len(sc) >= 2:
        # EVIDENCE axis — global (absolute 0-6 scale, comparable across the whole corpus)
        z_ev = zscores([float(r["evidence_rank"]) for r in sc])
        # ATTENTION axis — WITHIN stratum (peers of the same article kind); global fallback
        # for thin strata. This is what stops well-cited reviews from looking anomalous just
        # for being reviews: a review is measured against other reviews, not against primary work.
        global_z = zscores([r["citations_per_year"] for r in sc])
        groups = defaultdict(list)
        for i, r in enumerate(sc):
            groups[stratum_of(r["source_class"])].append(i)
        z_att = [0.0] * len(sc)
        att_basis = ["global_fallback"] * len(sc)
        for strat, idxs in groups.items():
            if len(idxs) >= MIN_STRATUM:
                local = zscores([sc[j]["citations_per_year"] for j in idxs])
                for k, j in enumerate(idxs):
                    z_att[j] = local[k]; att_basis[j] = strat
            else:
                for j in idxs:
                    z_att[j] = global_z[j]   # too few peers to stratify — compare globally
        for i, r in enumerate(sc):
            r["z_attention"] = round(z_att[i], 2)
            r["z_evidence"] = round(z_ev[i], 2)
            r["attention_basis"] = att_basis[i]   # which stratum the attention z was taken in
            r["anomaly"] = round(z_att[i] - z_ev[i], 2)    # +high attention/low evidence; -reverse
            if r["anomaly"] >= 1.5:
                if (r["citations"] or 0) < MIN_PROMOTION_CITES:
                    # positive anomaly but below the attention floor — low evidence, little
                    # attention. Not over-promoted. Record honestly.
                    r["class"], r["why_questions"] = "aligned_low_attention", []
                elif r["evidence_rank"] > MAX_PROMOTION_EVIDENCE:
                    # high attention but the evidence is ALSO top-tier — heavily-cited strong
                    # evidence is appropriate attention, not over-promotion. (Mirror of the
                    # SUPPRESSION z_att<0 guard.)
                    r["class"], r["why_questions"] = "aligned_well_cited_strong", []
                else:
                    r["class"], r["why_questions"] = "PROMOTION_anomaly", WHY_PROMOTION
            elif r["anomaly"] <= -1.5:
                # Negative anomaly from high evidence. Decide whether it's genuine suppression:
                too_recent = (NOW_YEAR - r["year"]) < MIN_SUPPRESSION_AGE_YEARS
                if z_att[i] < 0 and not too_recent:
                    # strong evidence + cited BELOW its peers + old enough that low attention
                    # is meaningful = genuinely buried. (The z_att<0 guard also stops a
                    # well-cited top-tier paper from being mislabeled suppressed.)
                    r["class"], r["why_questions"] = "SUPPRESSION_anomaly", WHY_SUPPRESSION
                elif too_recent:
                    # 0-few citations because the paper is NEW, not buried — don't accuse.
                    r["class"], r["why_questions"] = "high_evidence_too_recent", []
                else:
                    # cited at/above its peers — aligned high-tier work, not suppression.
                    r["class"], r["why_questions"] = "aligned_high_evidence", []
            else:
                r["class"], r["why_questions"] = "aligned", []
    for r in rows:
        if r["class"] == "pending":                        # no citation metric (e.g. trials, brand-new)
            r["class"] = "attention_unknown"

    rows.sort(key=lambda r: -(abs(r["anomaly"]) if r["anomaly"] is not None else -1))
    out = os.path.join(INTAKE, "why_anomalies.json")
    json.dump(rows, open(out, "w"), indent=2)

    flagged = [r for r in rows if r["class"] in ("PROMOTION_anomaly", "SUPPRESSION_anomaly", "SUPPRESSION_retracted")]
    unknown = sum(1 for r in rows if r["class"] == "attention_unknown")
    suspected = [r for r in rows if r.get("retraction_status") == "suspected"]
    print(f"\nscored {len(sc)} items with a real citation count  ({unknown} had none — trials/brand-new, not flagged)")
    if suspected:
        print(f"{len(suspected)} item(s) mention 'retract' but Europe PMC did NOT confirm a "
              f"retraction — recorded as suspected, flag NOT fired:")
        for r in suspected[:10]:
            print(f"  [suspected_retraction] {(r['title'] or r['id'])[:74]}")
    print(f"flagged {len(flagged)} genuine evidence/attention mismatches:")
    for r in flagged[:25]:
        an = f"{r['anomaly']:+.2f}" if r['anomaly'] is not None else "  ret"
        print(f"  [{r['class']:22}] anomaly={an}  cites={r['citations']}  "
              f"ev={r['evidence_rank']}  {(r['title'] or r['id'])[:70]}")
    print(f"\n-> {out}")
    print("\nThe filer flags the MISMATCH and asks the why as questions — it issues no verdict.")
    print("Proxies: evidence=source_class (pubType-derived, global rank); attention=EuropePMC")
    print("citations scored WITHIN article-type stratum (review/primary/preclinical/general) so")
    print("reviews are judged against reviews. Independence-of-confirmation (citation-graph) is")
    print("the next enhancement. Composes with the why-fork (ADR-204).")

if __name__ == "__main__":
    main()
