#!/usr/bin/env python3
"""Query the public frozen cancer corpus, locally; no dependencies or network."""
import argparse
import collections
import csv
import gzip
import hashlib
import itertools
import json
import re
from pathlib import Path
from mechanism_topics import TOPICS, VERSION, match_topic

HERE = Path(__file__).resolve().parent
LIMITATION = ("Candidate keyword retrieval is not a demonstrated mechanism, interaction, "
              "safety finding or treatment benefit. Missing matches are not evidence of absence. "
              "Evidence classes and retraction labels are inherited from the frozen snapshot; "
              "no current registry or retraction check is performed.")


def load(path):
    if str(path).endswith(".jsonl.gz"):
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            rows = [json.loads(line) for line in stream if line.strip()]
        for row in rows:
            for field in ("mechanism_nodes", "cohorts"):
                if isinstance(row.get(field), list):
                    row[field] = "|".join(row[field])
        return rows
    with open(path, encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", type=Path, help="Explicit CSV input; topic matching then uses titles only.")
    ap.add_argument("--node"); ap.add_argument("--cohort"); ap.add_argument("--class", dest="cls")
    ap.add_argument("--grep"); ap.add_argument("--year-min", type=int); ap.add_argument("--year-max", type=int)
    ap.add_argument("--limit", type=int, default=50)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--summary", action="store_true")
    mode.add_argument("--crossroads", action="store_true")
    mode.add_argument("--topic-summary", action="store_true")
    ap.add_argument("--topic", choices=sorted(TOPICS))
    ap.add_argument("--json", action="store_true", help="Machine-readable local output; abstracts are not exported.")
    a = ap.parse_args()
    if a.limit < 0:
        ap.error("--limit must be nonnegative")
    if a.year_min and a.year_max and a.year_min > a.year_max:
        ap.error("--year-min must not exceed --year-max")
    if (a.summary or a.crossroads or a.topic_summary) and any((a.node, a.cohort, a.cls, a.grep, a.year_min, a.year_max, a.topic)):
        ap.error("summary modes cannot be combined with row filters")
    path = a.csv or HERE / "data" / ("cancer_index.jsonl.gz" if a.topic or a.topic_summary else "cancer_index.csv")
    try:
        rows = load(path)
    except (OSError, ValueError, csv.Error) as exc:
        ap.error("cannot read index: %s" % exc)
    nodes = collections.Counter(n for r in rows for n in r.get("mechanism_nodes", "").split("|") if n)
    if a.node and a.node not in nodes:
        ap.error("unknown node in this snapshot: %s; use --summary or --topic for research topics" % a.node)
    meta = {"input_file": path.name, "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "limitations": LIMITATION, "snapshot_refreshed": False,
            "source_class_status": "inherited_not_reassessed"}
    if a.topic or a.topic_summary:
        meta.update({"topic_rules_version": VERSION, "topic_rules_sha256": hashlib.sha256((HERE / "mechanism_topics.py").read_bytes()).hexdigest(),
                     "rows_scanned": len(rows), "rows_with_abstract": sum(bool(r.get("abstract")) for r in rows)})
    if a.topic_summary:
        result = dict(meta, topics={})
        for name in sorted(TOPICS):
            matches = [r for r in rows if match_topic(r, name)]
            result["topics"][name] = {"label": TOPICS[name]["label"], "matches": len(matches),
                                     "source_classes": dict(sorted(collections.Counter(r.get("source_class") or "unknown" for r in matches).items()))}
    elif a.summary:
        result = dict(meta, studies=len(rows), with_abstract=sum(str(r.get("has_abstract")).lower() == "true" for r in rows),
                      mechanism_nodes=dict(nodes),
                      cohorts=dict(collections.Counter(c for r in rows for c in r.get("cohorts", "").split("|") if c)),
                      source_classes=dict(collections.Counter(r.get("source_class") or "unknown" for r in rows)))
    elif a.crossroads:
        pairs = collections.Counter(pair for r in rows for pair in itertools.combinations(sorted(set(filter(None, r.get("mechanism_nodes", "").split("|")))), 2))
        result = dict(meta, pairs=[{"nodes": list(pair), "count": n} for pair, n in pairs.most_common(a.limit)])
    else:
        hits = []
        for row in rows:
            if a.node and a.node not in row.get("mechanism_nodes", "").split("|"): continue
            if a.cohort and a.cohort not in row.get("cohorts", "").split("|"): continue
            if a.cls and row.get("source_class") != a.cls: continue
            if a.grep and a.grep.casefold() not in row.get("title", "").casefold(): continue
            year = str(row.get("year", ""))[:4]
            if a.year_min and (not year.isdigit() or int(year) < a.year_min): continue
            if a.year_max and (not year.isdigit() or int(year) > a.year_max): continue
            evidence = match_topic(row, a.topic) if a.topic else None
            if a.topic and not evidence: continue
            clean = {k: v for k, v in row.items() if k != "abstract"}
            if evidence: clean["topic_match"] = evidence
            if re.match(r"^case report\b", str(row.get("title", "")), re.I) and row.get("source_class") != "case_report":
                clean["source_class_review"] = "Title identifies a case report; inherited source_class needs review. Do not treat this label as stronger evidence."
            hits.append(clean)
        result = dict(meta, match_count=len(hits), returned_count=min(len(hits), a.limit),
                      source_classes=dict(sorted(collections.Counter(r.get("source_class") or "unknown" for r in hits).items())),
                      rows=hits[:a.limit])
    if a.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    elif "rows" in result:
        print("%d matches (%d shown)\n" % (result["match_count"], result["returned_count"]))
        for r in result["rows"]:
            print("%s [%s] %s" % (str(r.get("year", ""))[:4], r.get("source_class") or "unknown", r.get("title", "")))
            print("  nodes: %s | cohorts: %s" % (r.get("mechanism_nodes") or "-", r.get("cohorts") or "-"))
            if r.get("link"): print("  " + r["link"])
            if r.get("source_class_review"): print("  CLASSIFICATION REVIEW: " + r["source_class_review"])
            if r.get("topic_match"):
                m = r["topic_match"]
                terms = sorted({h["field"] + ": " + h["phrase"] for rule in m["rules"] for h in rule["hits"]})
                print("  candidate topic (%s): %s" % (m["text_scope"], "; ".join(terms)))
        print("\n" + LIMITATION)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
