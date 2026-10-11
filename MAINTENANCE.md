# Maintaining the public corpus

**Literature snapshot: June 2026. Tools and guidance updated: October 10, 2026.** These are different dates. The [release status](RELEASE_STATUS.json) records that no full literature refresh or current whole-corpus retraction check was performed for this change. Existing retraction labels remain visible.

## Review cadence and ownership

The repository maintainer should review literature coverage quarterly and whenever a material correction or retraction is reported. This is a documented maintenance target, not an enabled schedule or a promise that a refresh has happened. Assign an owner and record completion, partial coverage or failure for each cycle. Clinical or pharmacology reviewers evaluate claims within their competence; code checks do not stand in for that review.

For every proposed refresh, retain source, query, retrieval time, coverage, identifiers, changed records, unresolved retrievals, licensing and reviewer disposition. Do not turn timeouts or unavailable sources into “no new evidence.” Automated changes should arrive as a reviewable branch/PR, not overwrite a published snapshot.

The public checkout does not ship `cancer_discover.py` or `cancer_why_filer.py`. References to those tools in older documents describe a separate intake pipeline. A scheduled public workflow cannot honestly claim to run them. The CI shipped here checks local code, topic results and release bytes; it does not refresh literature, query live registries, submit personal data or sign a release.

## Retractions and corrections

Check source-of-record notices and linked registry records during each refresh. NLM distinguishes the retracted article from the notice retracting it, and also links errata and expressions of concern. Preserve these distinctions, identifiers, notice links and check dates rather than treating every notice as a retraction. [NLM policy](https://www.nlm.nih.gov/bsd/policy/errata.html).

Retain the original bibliographic record with its status and notice, and regenerate affected browser and query outputs together. Missing or failed checks are unknown. If an additional retraction database is used, record its version, access terms and coverage. Do not describe a whole-corpus check as complete from a few successful lookups.

## Reproducible local checks

Python 3.9+ and Node.js 18+ are sufficient; no package installation is required.

```sh
python3 -m unittest discover -s tests -v
node --test tests/test_practitioner_notes.js
python3 query_index.py --topic-summary --json > TOPIC_COVERAGE.json
python3 verify_release.py
```

`TOPIC_COVERAGE.json` is deterministic for the same source and matcher bytes. It records counts by inherited source class, matching-rule hash, corpus hash and abstract coverage. It is not a precision/recall evaluation or an efficacy ranking. Topic changes need positive and negative fixtures and review of actual matched records before promotion into canonical tags.

## Publishing a reviewed change

1. Work on a branch. Review `git diff` and the exact staged file list; keep local drafts and clinical records outside the public inventory.
2. Run the tests and inspect the static tool with synthetic notes. Check download, clear, literal text rendering, offline behavior and the lack of a submission path.
3. Review additions to `PUBLIC_RELEASE_FILES.txt` explicitly. It is a list of public files, not a recursive scan. Exclude personal data, keys, local notes and private intake directories.
4. Update `RELEASE_STATUS.json` honestly. Only advance the literature or retraction dates after the corresponding work is completed and documented.
5. After reviewing the bytes, run `python3 verify_release.py --write`, then `python3 verify_release.py`. Review and commit the manifest alongside the changes. CI rejects a missing, mismatched or incomplete manifest relative to the inventory and requires every Git-tracked file, except the manifest itself, in that inventory.
6. Push for review. Signing, an independent timestamp, a public anchor or a clinical assessment requires its own attributable evidence. Until then the status stays **UNSIGNED_NOT_REATTESTED**.

The SHA-256 manifest proves equality to the recorded bytes when independently obtained and checked. It does not establish authorship, source accuracy, medical safety, or that the manifest itself is trustworthy. Obtain the manifest from the release/commit you intend to verify.

## Copies, forks and attestation

A byte-identical copy can preserve and verify the original manifest and any available signatures. Editing a covered file changes its digest. A fork may produce its own checks and signatures, but must identify its maintainer, version and scope; it cannot claim the original maintainer attested its modified bytes. The older README's anchor `358c490` is retained as historical provenance, not asserted as proof for this release.

## Collaboration boundaries

GitHub accepts published references, reproducible code defects, corrections and **general research questions without personal history**. It does not accept patient experiences or clinical records. Private observation notes are for the person's licensed practitioners. This project operates no patient registry, signal-count aggregation or model-training intake. Those would require a separate governed research service, not another issue label.
