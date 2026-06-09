# The index — 6,358 studies, queryable

This is the shipped data layer of the corpus: a flat, searchable index of every study
the pipeline has verified and mechanism-tagged. It is the concrete object behind the
white paper's "store the public layer, point to the rest" design
(`WHITE_PAPER_DRAFT_v1.md`) — metadata and tags travel; the paywalled full text does
not. Read `DISCLAIMER_AND_SCOPE.md` first; everything here is hypothesis-generating
only.

## What ships

```
data/
  cancer_index.csv              6,358 studies, one row each (no abstract column)
  cancer_index.jsonl.gz         the same, WITH abstract text where openly available
  cancer_index_sample_200.csv   a strided taster
  index_summary.json            counts by node, evidence class, cohort, crossroads
  duke_sample/                  50-row samples of five Duke tables (full set on Proton)
  analytics/                    precomputed cross-tabs (see below)
mechanism_index.json            node -> studies map (the 12 mechanism nodes)
query_index.py                  query the index with no dependencies, no network
```

## The fields

Each row carries: `id`, `title`, `journal`, `year`, `source_class` (evidence type),
`identifier` + `id_kind` (the verified DOI/PMID/NCT), `verified`, `retrieval_status`,
`mechanism_nodes` (pipe-joined; see `MECHANISM_MAP.md`), `cohorts` (pipe-joined tumor
types), `has_abstract` / `abstract_source`, and `link` (the source of record). Most
rows are `POINTER_ONLY` — verified metadata + a link, full text left at the
publisher. That is the index-and-links posture, by design.

## Query it — no setup

```
python3 query_index.py --summary                          # node / cohort / evidence counts
python3 query_index.py --node immune_checkpoint --class rct
python3 query_index.py --cohort breast --node p53_apoptosis_cell_cycle
python3 query_index.py --node vaccine_cancer_specifically
python3 query_index.py --crossroads                       # co-occurring mechanism pairs
python3 query_index.py --grep curcumin --year-min 2020
```

Or load `data/cancer_index.csv` in DuckDB / any spreadsheet and filter on
`mechanism_nodes`, `cohorts`, `source_class`, or `year`.

## The analytics pack (`data/analytics/`)

Precomputed so the structure is visible without writing a query:

- `per_node_summary.csv` — per node: study count, year span, dominant evidence class
  and tumor cohort.
- `node_x_sourceclass.csv` — mechanism node × evidence type matrix.
- `node_x_decade.csv` — mechanism node × decade (how each axis grew over time).
- `cohort_counts.csv` — studies per tumor type (breast 601, colorectal 383, lung 337,
  pancreatic 200, …).
- `crossroads_pairs.csv` — the mechanism crossroads: studies touching two nodes at
  once. The largest is oxidative-stress × p53/apoptosis (**500 shared studies**),
  then immune-checkpoint × oxidative-stress (427).
- `top_journals.csv` — where the corpus's literature is published.

## Coverage and limits

- **6,358** studies; **5,369** carry an openly-available abstract; the rest are
  pointer-only (paywalled — follow the link). Expanding abstract coverage is a job for
  the scraper pipeline (`cancer_kind_scraper.py`), not the static release.
- **2,533** studies carry at least one tumor-cohort tag; **1,943** sit at more than
  one mechanism node; **2,074** match no node lexicon yet and ship untagged.
- Tags are reproducible and auditable (the lexicon is in `cancer_bridge.py`), and they
  group by *how* a thing is proposed to act — never by whether it works, and never as a
  safety signal. See `METHODS` discussion in `WHITE_PAPER_DRAFT_v1.md` and the limits
  in `DISCLAIMER_AND_SCOPE.md`.

---

*A map of the literature, hypothesis-generating, not medical advice. Every study is one
link from its source; every tag is auditable.*
