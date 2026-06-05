#!/bin/zsh
# Cancer corpus — overnight runner (runs on the Mac). All five phases, sequenced.
# LAUNCH DETACHED so it survives the terminal closing:
#   nohup zsh ~/garrison/outreach/conventional_and_complementary_cancer_treatments/run_overnight.sh \
#        > ~/cancer_intake/overnight.log 2>&1 & disown
# Watch it:  tail -f ~/cancer_intake/overnight.log
#
# Set CONTACT_EMAIL in cancer_discover.py + cancer_kind_scraper.py first (they warn but still run).

set -e
S=~/garrison/outreach/conventional_and_complementary_cancer_treatments
N=~/cancer_intake/nightly
mkdir -p "$N"
echo "================ OVERNIGHT START $(date -u) ================"

# ---------- Phase 1: discover across mechanism nodes -> verify -> store ----------
run () {  # $1=query  $2=tag
  echo "--- discover: $1"
  python3 $S/cancer_discover.py --europepmc "$1" --n 30 || true
  mv ~/cancer_intake/discovered_feedstock.json "$N/fs_$2.json" 2>/dev/null || true
  python3 $S/cancer_kind_scraper.py --feedstock "$N/fs_$2.json" || true
}
run "metformin cancer OXPHOS"                       met
run "atovaquone cancer complex III"                 ato
run "methylene blue cancer mitochondria"            mb
run "tumor perfusion hypoxia exercise cancer"       perf
run "bevacizumab vascular normalization"            bev
run "fasting mimicking diet chemotherapy"           fmd
run "fenbendazole mebendazole cancer"               fbz
run "ivermectin cancer"                             ivm
run "curcumin pancreatic cancer"                    cur
echo "--- discover: clinical trials"
python3 $S/cancer_discover.py --trials "pancreatic cancer" --n 30 || true
mv ~/cancer_intake/discovered_feedstock.json "$N/fs_trials.json" 2>/dev/null || true
python3 $S/cancer_kind_scraper.py --feedstock "$N/fs_trials.json" || true

# ---------- Phase 2: mechanism bridge index ----------
echo "--- bridge index"
python3 $S/cancer_bridge.py --index || true

# ---------- Phase 3: PubChem enrichment (compound -> CID) ----------
echo "--- pubchem enrich"
for a in "metformin" "atovaquone" "methylene blue" "dichloroacetate" "chlorine dioxide" "curcumin" "ivermectin" "fenbendazole"; do
  python3 $S/cancer_bridge.py --pubchem "$a" || true
done

# ---------- Phase 4: FAERS aggregates for the oncology cohort ----------
echo "--- FAERS aggregates"
for d in PEMBROLIZUMAB CARBOPLATIN TEMOZOLOMIDE NIVOLUMAB; do
  url="https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:%22$d%22&count=patient.reaction.reactionmeddrapt.exact"
  curl -s "$url" > "$N/faers_$d.json" || true
  sleep 2
done

# ---------- Phase 5: the why-filer (suppression / promotion anomalies) ----------
echo "--- why-filer"
python3 $S/cancer_why_filer.py || true

echo "================ OVERNIGHT DONE $(date -u) ================"
echo "Results in ~/cancer_intake/ :"
echo "  files/*.meta.json (+ *.xml)   stored studies"
echo "  mechanism_index.json          the HOW-bridge"
echo "  why_anomalies.json            evidence-vs-attention mismatches"
echo "  nightly/faers_*.json          FAERS aggregates"
