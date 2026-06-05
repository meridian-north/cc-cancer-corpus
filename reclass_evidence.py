#!/usr/bin/env python3
"""
reclass_evidence.py — backfill the evidence axis for ALREADY-STORED studies (no re-sweep).

WHY: studies discovered before the pubType classifier landed all carry the flat
'international_literature' source_class (ev=3). That collapses the why-filer's evidence axis,
so its anomaly score (z_attention - z_evidence) degenerates into pure citation rank — which
is why a sweep's PROMOTION list filled up with highly-cited review articles, all ev=3. This
re-derives a real evidence class from Europe PMC's pubType for those flat-classed records
WITHOUT re-running the discovery sweep.

PERFORMANCE: legacy records have no stored pub_types, so their class can only be learned by
asking Europe PMC. We ask in BATCHES (one OR-query per ~40 records of a source) instead of one
request per study — ~40x fewer calls. --dry-run does ZERO network: it only counts, classifies
the records that already carry pub_types for free, and ESTIMATES how many fetches the real run
will make, so you see the cost before committing.

Idempotent + conservative: only touches records still on the flat 'international_literature'
default. Seeds, trials, preprints, already-reclassified records are left alone.

Import-don't-copy (CLAUDE.md Karpathy #5): the SAME classifier the discoverer uses
(cancer_discover.classify_pubtype) and the SAME polite fetch the why-filer uses
(cancer_why_filer._get). Only the id-parse is local — deliberately, so --dry-run stays
network-free (epmc_handle can fall back to a network DOI lookup; we must not).

Stdlib only. Usage:
    python3 reclass_evidence.py --dry-run   # instant preview, no network, writes nothing
    python3 reclass_evidence.py --limit 200 # bounded real run (recommended first)
    python3 reclass_evidence.py             # full backfill
Then re-score (no re-discovery):
    python3 cancer_why_filer.py
"""
import json, os, glob, sys, urllib.parse
from collections import defaultdict
from cancer_discover import classify_pubtype
from cancer_why_filer import _get

INTAKE = os.path.expanduser("~/cancer_intake")
FILES = os.path.join(INTAKE, "files")
FLAT = "international_literature"   # the only class we backfill
BATCH = 40                          # ext_ids per Europe PMC OR-query
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


def handle_of(m):
    """(SOURCE, EXT_ID) from the stored id 'epmc_<src>_<id>'. Pure string parse — no network,
    so --dry-run is free. Records without the epmc_ id shape return (None, None) and are skipped."""
    mid = (m.get("id") or "")
    if mid.startswith("epmc_"):
        p = mid.split("_")
        if len(p) >= 3:
            return p[1].upper(), p[2]
    return None, None


def pubtypes_batch(source, ext_ids):
    """One Europe PMC core query for up to len(ext_ids) records of a source.
    Returns {ext_id: result_item} where the item carries source + pubTypeList + title."""
    q = "(" + " OR ".join(f"EXT_ID:{e}" for e in ext_ids) + f") AND SRC:{source}"
    url = f"{EPMC}?query=" + urllib.parse.quote(q) + f"&resultType=core&format=json&pageSize={len(ext_ids)}"
    d = _get(url)
    out = {}
    for it in (d or {}).get("resultList", {}).get("result", []):
        out[str(it.get("id"))] = it
    return out


def main():
    dry = "--dry-run" in sys.argv
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    paths = sorted(glob.glob(os.path.join(FILES, "*.meta.json")))
    if limit:
        paths = paths[:limit]
    if not paths:
        print(f"No .meta.json in {FILES}. Run the scraper first."); return

    # ---- pass 1: partition (no network) -------------------------------------
    free = []          # (path, meta, it)  — already carry pub_types, classify for free
    need = []          # (path, meta, source, ext) — must ask Europe PMC
    by_src = defaultdict(list)
    skipped = errors = nonflat = 0
    for p in paths:
        try:
            m = json.load(open(p))
        except Exception:
            errors += 1; continue
        if (m.get("source_class") or "") != FLAT:
            nonflat += 1; continue
        pts = m.get("pub_types")
        if pts is not None:
            free.append((p, m, {"source": m.get("country_hint"), "title": m.get("title"),
                                "pubTypeList": {"pubType": pts}}))
            continue
        src, ext = handle_of(m)
        if not (src and ext):
            skipped += 1; continue
        need.append((p, m, src, ext))
        by_src[src].append(ext)

    n_batches = sum((len(v) + BATCH - 1) // BATCH for v in by_src.values())
    print(f"\n=== reclass_evidence {'(dry-run) ' if dry else ''}===")
    print(f"  non-flat (left alone)     : {nonflat}")
    print(f"  flat w/ stored pub_types  : {len(free)}   (classified free, no network)")
    print(f"  flat needing EPMC lookup  : {len(need)}   -> ~{n_batches} batched requests "
          f"(~{n_batches}s polite)")
    print(f"  skipped (no id handle)    : {skipped}    errors: {errors}")

    dist = defaultdict(int)
    changes = []   # (path, meta, new_class, pubtypes)

    def stage(path, meta, it):
        nc = classify_pubtype(it)
        dist[nc] += 1
        if nc != FLAT:
            changes.append((path, meta, nc, it["pubTypeList"].get("pubType", [])))

    for path, m, it in free:
        stage(path, m, it)

    if dry:
        # estimate the fetch-class spread from the free sample only; do NOT touch the network
        print("\n  preview class spread (from the free-to-classify sample only):")
        for k, v in sorted(dist.items(), key=lambda kv: -kv[1]):
            print(f"    {k:24} {v}")
        print(f"\n  would reclassify (free sample): {len(changes)}; "
              f"{len(need)} more require the real run's {n_batches} fetches.")
        print("  (dry-run wrote nothing). Real run:  python3 reclass_evidence.py [--limit N]")
        return

    # ---- pass 2: batched fetch + classify -----------------------------------
    done = 0
    for src, exts in by_src.items():
        # map ext -> (path, meta) for this source
        rec_by_ext = {ext: (p, m) for (p, m, s, ext) in need if s == src}
        for i in range(0, len(exts), BATCH):
            chunk = exts[i:i + BATCH]
            got = pubtypes_batch(src, chunk)
            for ext in chunk:
                p, m = rec_by_ext[ext]
                it = got.get(ext)
                if it is None:
                    dist["_epmc_miss"] += 1
                    continue
                stage(p, m, {"source": it.get("source"), "title": it.get("title"),
                             "pubTypeList": it.get("pubTypeList", {}) or {}})
            done += len(chunk)
            print(f"  ... fetched {done}/{len(need)}")

    # ---- write -------------------------------------------------------------
    for path, m, nc, pts in changes:
        m["source_class"] = nc
        m["pub_types"] = pts
        m["reclassified_by"] = "reclass_evidence.py"
        json.dump(m, open(path, "w"), indent=2)

    print(f"\n  reclassified : {len(changes)}")
    print("  resulting class distribution (this run):")
    for k, v in sorted(dist.items(), key=lambda kv: -kv[1]):
        print(f"    {k:24} {v}")
    print("\nDone. Re-score over the reclassified corpus:")
    print("  python3 cancer_why_filer.py")


if __name__ == "__main__":
    main()
