#!/bin/zsh
# Corpus sweep — source studies for every agent in agent_queries.txt, then re-bridge + re-why-file.
# This is the cure for corpus-starvation. Each query now runs THREE discovery passes (S217-followup,
# sourcing rebalance toward PRIMARY evidence): broad EPMC (keeps reviews for the why-filer stratum)
# + primary-pubType EPMC (RCT/trial/observational/cohort) + ClinicalTrials.gov (breadth-max, not
# phase-gated). ~50 agents x 3 passes x ~30 -> a fatter, mechanism-taggable, primary-weighted corpus.
# LAUNCH DETACHED:
#   nohup zsh ~/garrison/outreach/conventional_and_complementary_cancer_treatments/run_corpus_sweep.sh \
#        > ~/cancer_intake/sweep.log 2>&1 & disown
#   tail -f ~/cancer_intake/sweep.log
# (Set CONTACT_EMAIL in the tools first.)

S=~/garrison/outreach/conventional_and_complementary_cancer_treatments
N=~/cancer_intake/sweep
# Overridable (defaults = original behavior; no env set = unchanged):
#   QUERIES   = which query list to sweep   (Duke pass: ~/cancer_intake/duke_queries.txt)
#   LIMIT     = >0 sweeps only the first N queries (validation batch before the long pass)
#   SKIP_BOOKS= 1 skips the open-access book loop (irrelevant to a Duke compound pass)
#   TRIAL_RESULTS= 1 adds the bounded posted-results digest to the ClinicalTrials.gov pass
#                  (heavier; off by default per How>Why — mechanism comes from abstracts)
QUERIES="${QUERIES:-$S/agent_queries.txt}"
LIMIT="${LIMIT:-0}"
SKIP_BOOKS="${SKIP_BOOKS:-0}"
mkdir -p "$N"
echo "================ CORPUS SWEEP START $(date -u)  queries=$QUERIES limit=$LIMIT skip_books=$SKIP_BOOKS ================"

i=0
src=$(grep -v '^[[:space:]]*#' "$QUERIES" | grep -v '^[[:space:]]*$')
[ "$LIMIT" -gt 0 ] && src=$(printf '%s\n' "$src" | head -n "$LIMIT")
printf '%s\n' "$src" | while read -r q; do
  i=$((i+1)); tag=$(echo "$q" | tr ' /' '__' | cut -c1-40)
  echo "--- [$i] $q"
  # 1) broad EPMC pass — keeps reviews present for the why-filer's review stratum
  python3 $S/cancer_discover.py --europepmc "$q" --n 30 || true
  mv ~/cancer_intake/discovered_feedstock.json "$N/fs_${i}_${tag}.json" 2>/dev/null || true
  python3 $S/cancer_kind_scraper.py --feedstock "$N/fs_${i}_${tag}.json" || true
  # 2) primary-evidence EPMC pass — pubType-filtered RCT/trial/observational/cohort (the rebalance)
  python3 $S/cancer_discover.py --europepmc "$q" --n 30 --primary || true
  mv ~/cancer_intake/discovered_feedstock.json "$N/pri_${i}_${tag}.json" 2>/dev/null || true
  python3 $S/cancer_kind_scraper.py --feedstock "$N/pri_${i}_${tag}.json" || true
  # 3) ClinicalTrials.gov pass — breadth-max, not phase-gated; TRIAL_RESULTS=1 adds results digests
  python3 $S/cancer_discover.py --trials "$q" --n 30 ${TRIAL_RESULTS:+--with-results} || true
  mv ~/cancer_intake/discovered_feedstock.json "$N/trials_${i}_${tag}.json" 2>/dev/null || true
  python3 $S/cancer_kind_scraper.py --feedstock "$N/trials_${i}_${tag}.json" || true
done

# open-access books for a few high-interest agents (skip on a Duke compound pass)
if [ "$SKIP_BOOKS" != "1" ]; then
for b in "curcumin cancer" "berberine cancer" "complementary integrative oncology" "natural products cancer pharmacology"; do
  echo "--- book: $b"
  python3 $S/cancer_discover.py --bookshelf "$b" --n 15 || true
  mv ~/cancer_intake/discovered_feedstock.json "$N/book_$(echo $b | tr ' ' _).json" 2>/dev/null || true
  python3 $S/cancer_kind_scraper.py --feedstock "$N/book_$(echo $b | tr ' ' _).json" || true
done
fi

echo "--- rebuild mechanism index"
python3 $S/cancer_bridge.py --index || true
echo "--- re-run why-filer (now over a fat corpus)"
python3 $S/cancer_why_filer.py || true

echo "================ CORPUS SWEEP DONE $(date -u) ================"
echo "Now: python3 $S/cancer_bridge.py --node electron_transport_oxphos   (or any node)"
