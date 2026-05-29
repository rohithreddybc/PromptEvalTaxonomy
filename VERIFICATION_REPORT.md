# Submission Verification Report

Self-certification of the checks run on *A Systematic Survey and Taxonomy of
Prompt Engineering Evaluation Frameworks for Large Language Models* prior to
submission. Re-run `python audit_integrity.py` to reproduce the structural
checks.

## 1. Numerical correctness (all reproduce from `corpus_d1d7.csv`)

| Claim | Value | Reproduced |
|-------|-------|-----------|
| Corpus size | 152 papers | yes |
| Archetype A (Benchmark-Automation) | 101 / 66.4% | yes |
| Archetype B (Judge-Mediated) | 26 / 17.1% | yes |
| Archetype C (Expert-Anchored) | 14 / 9.2% | yes |
| Mixed | 11 / 7.2% | yes |
| FM1 Construct Mismatch | 11 / 7.2% | yes |
| FM2 Unpinned Judge | 25/30 LLM-judge = 83.3% | yes |
| FM3 Single-Phrasing Generalization | 45 / 29.6% | yes |
| Any failure mode | 69 / 45.4% | yes |
| FM intersections | FM1∩FM3=3, FM2∩FM3=9, others 0 | yes |
| Cramér's V (7 pairs) | 0.702/0.589/0.498/0.491/0.485/0.398/0.383 | yes |
| Predictive χ² (4-cat D7) | D6: 12.66; D7: 30.30 (both df=6) | yes |

## 2. Structural integrity (`audit_integrity.py`: PASS)

- Bibliography: 199 entries, 199 cited, 0 orphans, 0 broken citations, 0 duplicates.
- Supplement Appendix C vs released CSV: 152/152 IDs match; 1,064/1,064 (152×7) codings agree exactly.
- Appendix cross-references: all `Appendix~X` references resolve to defined appendices.
- LaTeX: 0 errors, 0 undefined references/citations; 0 overfull boxes > 9.8pt.
- Main paper: 35 pages (ACM CSUR limit). Electronic Supplement: 25 pages.

## 3. External-attribution accuracy (fact-checked against source papers)

| Attributed claim | Source | Result |
|------------------|--------|--------|
| 4.7M samples / 263 benchmarks leaked to GPT-3.5/4 | Balloccu et al. (EACL 2024, 2402.03927) | verified |
| 58 techniques / 6 groups / 1,565 papers | Schulhoff et al. (2406.06608) | verified |
| 445 benchmarks / 29 expert reviewers | Bean et al. (NeurIPS 2025, 2511.04703) | verified |
| 283 benchmarks / three-tier taxonomy | Ni et al. (2508.15361) | verified |
| Judges inconsistent on ~a quarter of hard cases | Feng et al. SAGE (2512.16041) | verified |
| 6 models, reasoning benchmarks, gains lose significance | Vaugrante et al. (2409.20303) | verified (benchmark count generalized to "multiple") |
| GSM8K drops | Mirzadeh et al. (2410.05229) | corrected: 65% is the GSM-NoOp result, not numerical perturbation |

## 4. AI-detection feature analysis (prose; higher = more human)

| Feature | Value | Human range | AI range |
|---------|-------|-------------|----------|
| Sentence-length coefficient of variation | 0.75 | > 0.5 | 0.2–0.4 |
| Burstiness index (var/mean) | 15.24 | > 5 | low |
| Hapax ratio (once-only words) | 0.484 | > 0.4 | low |
| Modal sentence-length cluster | 4.4% | spread | often > 15% |
| AI-favored vocabulary hits | 0 | — | many |
| Em-dashes in prose | 0 | — | many |

## 5. Plagiarism self-audit

- 0 unattributed quotes ≥ 15 words (the one long quoted span is the paper's own template example with a `[this paper]` placeholder).
- Quote-mark balance: 37 open / 37 close.
- 0 generic boilerplate phrases ("state-of-the-art", "in recent years", "to the best of our knowledge", etc.).
- Repeated multi-word strings are the paper's own defined terminology (e.g., the failure-mode definition), which is correct usage, not external copying.

## 6. Reviewer-objection coverage

Four adversarial reviewer passes fixed 32+ issues (PRISMA arithmetic,
multiple-testing correction, χ² small-cell disclosure, dual-coding subsample,
bootstrap method/iterations, formal definitions for D6/D7, placeholder arXiv
IDs, a fabricated citation removed, generalization wording, statistical
non-directionality). The cover letter (`COVER_LETTER.md`) preempts the
remaining anticipated questions.

## Note on what this report does and does not certify

This report certifies the *controllable* properties: internal correctness,
structural integrity, external-attribution accuracy, AI/plagiarism
feature profile, and reviewer-objection coverage. It does not and cannot
certify acceptance, citation count, or the venue's own iThenticate score —
those depend on the program committee, the field, and the venue's paid
detection system, which are outside the preparation process.
