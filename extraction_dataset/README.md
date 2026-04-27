# Extraction Dataset

This directory contains the 80-paper corpus extraction dataset from:  
*A Systematic Survey and Taxonomy of Prompt Engineering Evaluation Frameworks for Large Language Models*  
Bellibaltu, Jena, Morla (2026)

---

## File

`corpus_taxonomy_codes.csv` — machine-readable mapping of all 80 papers to their five-dimensional taxonomy codes.

---

## Column Schema

| Column | Type | Description |
|---|---|---|
| `paper_id` | integer | Row number (1–80) matching Table II in the paper |
| `cite_key` | string | BibTeX citation key from `references.bib` |
| `authors_short` | string | First author last name + year (e.g., `Wei2022`) |
| `title_short` | string | Abbreviated paper title |
| `year` | integer | Year of publication |
| `venue` | string | Publication venue (journal, conference, or `arXiv`) |
| `venue_type` | string | `journal`, `conference`, or `preprint` |
| `n_models` | integer | Number of distinct models compared in the evaluation |
| `D1_eval_method` | string | Dimension 1: `Benchmark`, `Human`, `LLM-judge`, `Ablation`, `User-study` |
| `D2_task_scope` | string | Dimension 2: `Reasoning`, `NLG`, `Code`, `QA`, `Clinical`, `Multilingual`, `Multi-task` |
| `D3_metric_type` | string | Dimension 3: `Reference-based`, `Model-based`, `LLM-judge`, `Task-specific` |
| `D4_automation` | string | Dimension 4: `Manual`, `Human-in-loop`, `Hybrid`, `Automated` |
| `D5_scope` | string | Dimension 5: `Single-model`, `Cross-model`, `Cross-dataset`, `Cross-domain`, `Cross-lingual` |
| `notes` | string | Free-text notes on coding decisions where interpretive judgment was required |

---

## Coding Notes

- **D4 (Automation Level)** required the most interpretive judgment. Papers that described automated metrics but also mentioned any human inspection of outputs were coded as `Hybrid`.
- **D2 (Task Scope)** was coded from the primary evaluation task. Papers reporting on multiple task types are coded as `Multi-task`.
- Extraction was performed by one reviewer and independently verified by a second reviewer on a 20% random sample.

---

## License

CC BY 4.0 — free to use and adapt with attribution. Cite the paper above.
