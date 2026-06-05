# Why-fork investigation template — how to read a suppression/promotion flag

*A reusable method + worked examples for investigating the anomalies `cancer_why_filer.py`
surfaces. The filer flags where ATTENTION diverges from EVIDENCE; this template is how a
human (or the council) turns a flag into a documented, neutral finding — never a verdict.
First run: 2026-06-04. Composes with the why-fork (ADR-204), ReproducibilityAnchoredScoringMt,
EfficacyNeutralityMt, and the queued SuppressedLiteratureBridgeMt.*

---

## The method (six steps, every flag)

1. **Treat the flag as a CANDIDATE, not a verdict.** The filer found a mismatch; it has
   concluded nothing.
2. **Verify the flag itself first.** A `RETRACTED` string in metadata is not proof of
   retraction; a high citation count is not proof of hype. Confirm independently
   (retraction notice via Crossref/publisher; whether the item is a review).
3. **Extract the DOCUMENTED reason** — the actual retraction notice text, the citation
   pattern — as *fact*. If there is no documented reason, the answer is `UNCONFIRMED`.
4. **Separate the paper from the question.** A retracted paper's *removal* and its
   *underlying claim* are two different things. A manipulated figure disqualifies the
   paper; it does not disprove the biology. Record both, distinctly.
5. **Frame neutrally — hardest on charged topics.** Do not spin an integrity retraction
   as censorship, or a censorship as integrity. The documented reason decides. Where the
   reason is genuinely suggestive of non-integrity suppression, record it **as an open
   question with its evidence**, never as an assertion.
6. **Close on the reform ask, not the politics (sovereign steer, 2026-06-04).** When the
   documented reason reduces to politics — funding, paradigm, industry interest, reporting
   convenience — the *why* has gone as far as it usefully can, and AC360 does not dwell there.
   The constructive output is the **data-reporting reform the gap implies**: what would the
   researchers, journals, and reporting agencies need to change in HOW they report so this
   stops being ambiguous? A buried high-evidence result usually points at a fixable data
   practice — an unreported endpoint, no raw data posted, no registered protocol, a
   denominator never published. Record that reform ask. It routes the why toward FUAG —
   *better data sources* — instead of toward accusation. The corpus's job is to make the
   sources reformable, not to assign blame.

## The outcome taxonomy (fill in the class)

**Suppression flags (retracted / buried / deprecated):**
| Class | Meaning | Underlying question |
|---|---|---|
| `legitimate_integrity` | retracted for fraud / image manipulation / duplication / missing data | may still be open — needs clean replication |
| `superseded` | withdrawn because better work replaced it | usually closed |
| `procedural` | publisher error, author request, duplicate submission | unaffected |
| `inconvenient_contested` | circumstances suggest non-integrity reasons (pressure/funding/paradigm) | the interesting one — **record as open question + evidence, never asserted** |
| `unconfirmed` | flagged by metadata but no retraction notice independently found | verify before treating as retracted |

**Promotion flags (over-cited relative to evidence):**
| Class | Meaning |
|---|---|
| `review_inflation` | it's a review — reviews structurally over-cite (artifact, not promotion) |
| `citation_ring` | a cluster citing mainly each other (the single-source-in-disguise pattern) |
| `commercial_media` | hyped by industry/media beyond the data |
| `genuine_early_signal` | real emerging importance — high attention is warranted, not an anomaly |

## Worked examples — the two from the first run (the template in action)

### Example A — `legitimate_integrity` (the charged-molecule case)
- **Flag:** `SUPPRESSION_retracted` — "Ivermectin induces autophagy-mediated cell death via AKT/mTOR in glioma."
- **Verified:** Yes — Bioscience Reports, retracted April 2026 (retraction notice confirmed).
- **Documented reason:** duplication with a 2020 *Journal of Cancer* paper by the same
  authors; Figure 3A western-blot bands matched after a **mirror-image rotation**
  (manipulation); **no raw data** for the mTOR bands. Editorial board lost confidence.
- **Class:** `legitimate_integrity`.
- **Paper vs question:** the paper's removal was warranted; the **underlying question**
  (does ivermectin hit glioma via AKT/mTOR autophagy?) **stays open** — a bad figure
  disqualifies the paper, not the biology. Needs clean replication.
- **Neutral framing (the lesson):** ivermectin is politically charged, but **this
  retraction was about fabricated data, not censorship.** The corpus does not get to
  spin it either way. Documented reason decides.

### Example B — `unconfirmed` (the false-positive catch)
- **Flag:** `SUPPRESSION_retracted` — "Physical activity and glioblastoma: a paradigm shift…"
- **Verified:** NO — independent search found the paper (Xie & Wang, 2025) **active, with
  no retraction notice**. The filer fired on a `RETRACTED:` string in the record.
- **Class:** `unconfirmed` → needs human verification before it counts as retracted.
- **Tool lesson:** the filer's retraction check was string-matching, too trusting. v2 fix:
  **confirm an actual retraction notice (Crossref retraction flag / publisher) before
  firing the flag** — the same verify-don't-assert rule we apply to every pointer.

## The reusable record (copy per future flag)

```
flag: <PROMOTION_anomaly | SUPPRESSION_anomaly | SUPPRESSION_retracted>
item: <title> · <DOI/PMID/NCT>
flag_verified: <yes | no — how checked>
documented_reason: <verbatim from the notice / the citation pattern, or "none found">
outcome_class: <from the taxonomy>
paper_status: <retracted/active/contested>
underlying_question_status: <open | closed | superseded>  ← separate from paper_status
neutral_note: <the fair framing; what we do NOT assert>
open_questions: <2-3 checkable questions>
data_reform_implication: <the reporting change this gap implies — what would make the source
                          unambiguous (registered protocol / posted raw data / published
                          denominator / reported endpoint); "none" if not applicable>
```

---

*The filer raises the candidate; verification decides; the documented reason — or an
honest `UNCONFIRMED` — is what gets recorded. No verdicts. The why stays a question until
the evidence answers it — and when the answer is politics, the record carries a reform ask,
not a charge.*
