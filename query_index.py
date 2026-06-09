#!/usr/bin/env python3
"""
query_index.py — query the shipped cancer corpus index. No dependencies, no network,
no source-intake folder needed: it runs against data/cancer_index.csv as shipped.

Examples:
  python3 query_index.py --summary
  python3 query_index.py --node immune_checkpoint --class rct
  python3 query_index.py --cohort breast --node p53_apoptosis_cell_cycle
  python3 query_index.py --grep curcumin --year-min 2020
  python3 query_index.py --node vaccine_cancer_specifically
  python3 query_index.py --crossroads          # co-occurring mechanism node pairs

Every row is hypothesis-generating only: counts are a floor, no denominator, no
causation, no efficacy verdict. Follow each link to the source of record.
"""
import csv, os, sys, argparse, collections, itertools

HERE = os.path.dirname(os.path.abspath(__file__))

def load(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

def main():
    ap = argparse.ArgumentParser(description="Query the cancer corpus index.")
    ap.add_argument("--csv", default=os.path.join(HERE, "data", "cancer_index.csv"))
    ap.add_argument("--node"); ap.add_argument("--cohort"); ap.add_argument("--class", dest="cls")
    ap.add_argument("--grep"); ap.add_argument("--year-min", type=int); ap.add_argument("--year-max", type=int)
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--crossroads", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(a.csv):
        sys.exit("index not found: %s (run from the repo root, or pass --csv)" % a.csv)
    rows = load(a.csv)

    if a.summary:
        nodes = collections.Counter(n for r in rows for n in r["mechanism_nodes"].split("|") if n)
        coh = collections.Counter(c for r in rows for c in r["cohorts"].split("|") if c)
        cls = collections.Counter(r["source_class"] for r in rows if r["source_class"])
        print("studies: %d  | with abstract: %d\n" % (len(rows), sum(1 for r in rows if r["has_abstract"]=="True")))
        for label, ctr in (("MECHANISM NODES", nodes), ("TUMOR COHORTS", coh), ("EVIDENCE CLASS", cls)):
            print(label)
            for k, v in ctr.most_common():
                print("  %-32s %d" % (k, v))
            print()
        return

    if a.crossroads:
        pair = collections.Counter()
        for r in rows:
            ns = [n for n in r["mechanism_nodes"].split("|") if n]
            for x, y in itertools.combinations(sorted(ns), 2):
                pair[(x, y)] += 1
        print("MECHANISM CROSSROADS — studies touching two nodes at once\n")
        for (x, y), n in pair.most_common(a.limit):
            print("  %5d   %s + %s" % (n, x, y))
        return

    def keep(r):
        if a.node and a.node not in r["mechanism_nodes"].split("|"): return False
        if a.cohort and a.cohort not in r["cohorts"].split("|"): return False
        if a.cls and r["source_class"] != a.cls: return False
        if a.grep and a.grep.lower() not in r["title"].lower(): return False
        y = r["year"][:4]
        if a.year_min and (not y.isdigit() or int(y) < a.year_min): return False
        if a.year_max and (not y.isdigit() or int(y) > a.year_max): return False
        return True

    hits = [r for r in rows if keep(r)]
    print("%d match%s\n" % (len(hits), "" if len(hits) == 1 else "es"))
    for r in hits[:a.limit]:
        print("%-6s %-22s %s" % (r["year"][:4], (r["source_class"] or "-")[:22], r["title"][:90]))
        print("       nodes: %s | cohorts: %s" % (r["mechanism_nodes"] or "-", r["cohorts"] or "-"))
        if r["link"]: print("       %s" % r["link"])
    if len(hits) > a.limit:
        print("\n... %d more (raise --limit)" % (len(hits) - a.limit))

if __name__ == "__main__":
    main()
