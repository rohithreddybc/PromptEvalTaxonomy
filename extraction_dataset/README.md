# Extraction Dataset

This directory will contain the 153-paper corpus extraction dataset from:
*A Systematic Survey and Taxonomy of Prompt Engineering Evaluation Frameworks for Large Language Models*
Bellibaltu, Jena, Morla, Zhang (2026)

The full machine-readable CSV will be released at paper acceptance to keep the dataset aligned with the final accepted version of the manuscript.

---

## Planned File

`corpus_taxonomy_codes.csv` - machine-readable mapping of all 153 papers to their seven-dimensional taxonomy codes (D1-D7).

---

## Column Schema (planned)

| Column | Type | Description |
|---|---|---|
| `paper_id` | integer | Row number (1-153) matching Appendix C in the paper |
| `cite_key` | string | BibTeX citation key from `references.bib` |
| `authors_short` | string | First author last name + year (e.g., `Wei2022`) |
| `title_short` | string | Abbreviated paper title |
| `year` | integer | Year of publication |
| `venue` | string | Publication venue (journal, conference, or `arXiv`) |
| `venue_type` | string | `journal`, `conference`, or `preprint` |
| `n_models` | integer | Number of distinct models compared in the evaluation |
| `D1_eval_method` | string | Dimension 1: `Benchmark`, `Human`, `LLM-judge`, `Ablation`, `User-study` |
| `D2_task_scope` | string | Dimension 2: `Reasoning`, `NLG`, `Code`, `QA`, `Clinical`, `Multilingual`, `Multi-task`, `Agentic` |
| `D3_metric_type` | string | Dimension 3: `Reference-based`, `Model-based`, `LLM-judge`, `Task-specific`, `Hybrid` |
| `D4_automation` | string | Dimension 4: `Manual`, `Human-in-loop`, `Hybrid`, `Automated` |
| `D5_eval_scope` | string | Dimension 5: `Single-model`, `Cross-model`, `Cross-domain`, `Cross-dataset`, `Cross-lingual` |
| `D6_robustness` | string | Dimension 6: `Not-reported`, `Single-prompt`, `Multi-prompt-aggregate`, `Sensitivity-bounded` |
| `D7_reproducibility` | string | Dimension 7: combination of `Artifact-released`, `Contamination-checked`, `Judge-version-pinned`, `Not-reported` |
| `coded_by` | string | Initials of primary coder |
| `dual_coded` | boolean | Whether paper was independently coded by the second coder |
| `notes` | string | Free-text comments on coding judgment calls |

## Inter-rater agreement

The dataset will be accompanied by per-dimension Cohen's kappa values matching Table 4 of the paper:

- D1: 0.92, D2: 0.88, D3: 0.91, D4: 0.84, D5: 0.89, D6: 0.76, D7: 0.78
