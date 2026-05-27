# Extraction Dataset Schema

This document describes the 152-paper corpus extraction dataset for:
*A Systematic Survey and Taxonomy of Prompt Engineering Evaluation Frameworks for Large Language Models*
Bellibaltu, Jena, Morla, Zhang (2026)

The machine-readable dataset is provided as `corpus_d1d7.csv` in the repository root. A citable tagged version will be released at paper acceptance to keep the dataset aligned with the final accepted version of the manuscript.

---

## Released File

`corpus_d1d7.csv` — machine-readable mapping of all 152 papers to their seven-dimensional taxonomy codes (D1-D7). 152 rows + 1 header row. UTF-8 encoded, comma-separated, field-quoted.

---

## Released Column Schema (matches `corpus_d1d7.csv` exactly)

| Column | Type | Description |
|---|---|---|
| `ID` | integer | Row number (1-152) matching Appendix C in the paper |
| `Paper` | string | First author last name + LaTeX `\cite{...}` key from `references.bib` (e.g., `Wei et al.~\cite{wei2022chain}`) |
| `System` | string | Short name of the prompting technique or evaluation system (e.g., `Chain-of-Thought`, `G-Eval`, `MT-Bench`) |
| `D1` | string | Evaluation method. Atomic codes: `Benchmark`, `LLM-as-Judge`, `Human eval`, `Ablation`. Comma-separated when a paper uses more than one (e.g., `LLM-as-Judge, Human`). |
| `D2` | string | Task scope. Atomic codes: `Multi-task`, `Reasoning`, `Code`, `Generation`, `QA`, `Clinical`, `Agentic`, `Multilingual`. Comma-separated when a paper covers more than one. |
| `D3` | string | Metric type. Atomic codes: `Task-specific`, `LLM-judge`, `Hybrid`, `Model-based`, `Reference-based`. |
| `D4` | string | Automation level. Atomic codes: `Automated`, `Hybrid`, `Manual`, `Human-in-loop`. |
| `D5` | string | Evaluation scope. Atomic codes: `Cross-model`, `Cross-domain`, `Single-model`, `Cross-dataset`. |
| `D6` | string | Robustness reporting. Atomic codes: `Sng` (single-prompt), `MAg` (multi-prompt aggregate), `NR` (not reported), `SB` (sensitivity-bounded). |
| `D7` | string | Reproducibility properties. Atomic codes: `AR` (artifact released), `NR` (not reported), `JP` (judge-version pinned), `CC` (contamination-checked). Combined via `+` when more than one applies (e.g., `JP+AR`, `CC+AR`). |

Atomic-code conventions follow Section 4 of the paper. Compound D1 / D2 codes use a comma separator; compound D7 codes use a `+` separator. The PowerShell analysis script and the Python validation script both treat these compounds atomically by splitting on `,`, `+`, or `/`.

---

## Distinct values observed in the released CSV

| Dimension | Distinct values (count) |
|---|---|
| D1 | `Benchmark` (110), `LLM-as-Judge` (26), `Human eval` (10), `LLM-as-Judge, Human` (4), `Ablation` (2) |
| D2 | `Multi-task` (94), `Reasoning` (14), `Code` (12), `Generation` (10), `QA` (9), `Clinical` (5), `Agentic` (4), `Multilingual` (3), `QA, Reasoning` (1) |
| D3 | `Task-specific` (103), `LLM-judge` (31), `Hybrid` (16), `Model-based` (2) |
| D4 | `Automated` (124), `Hybrid` (19), `Manual` (5), `Human-in-loop` (4) |
| D5 | `Cross-model` (96), `Cross-domain` (32), `Single-model` (16), `Cross-dataset` (8) |
| D6 | `Sng` (63), `MAg` (45), `NR` (35), `SB` (9) |
| D7 | `AR` (99), `NR` (42), `JP+AR` (5), `CC+AR` (3), `CC` (3) |

Totals always sum to 152 (one row per paper). Compound codes count as a single value here; the `make_prisma.py`, `empirical_analysis.ps1`, and `cluster_validation.py` scripts split compound codes into atomic levels for the per-level analyses in Section 8 of the paper.

---

## Inter-rater agreement (Table 11 of the paper)

Per-dimension Cohen's kappa on the dual-coded subsample (32 papers, ~21% of the corpus, two-coder design):

| Dim | kappa | Interpretation |
|---|---|---|
| D1 | 0.92 | Almost perfect |
| D2 | 0.88 | Almost perfect |
| D3 | 0.91 | Almost perfect |
| D4 | 0.84 | Almost perfect |
| D5 | 0.89 | Almost perfect |
| D6 | 0.76 | Substantial |
| D7 | 0.78 | Substantial |

The dual-coded subsample itself is documented in the Electronic Supplement (`supplementary.pdf`, Appendix B). Per-paper coder assignments are not currently included in `corpus_d1d7.csv` to keep the released file aligned with the in-paper Appendix C presentation; a future tagged release at paper acceptance will add `coded_by` and `dual_coded` columns.

---

## Reproducing claims from this CSV

See `README.md` in the repository root for the full claim-to-artifact mapping. In short:

- Per-dimension distributions, archetype shares, and failure-mode prevalences (Section 8 of the paper) are direct counts from the columns above.
- Cramer's V and chi-squared values (Table 14) use the primary atomic code per paper (first listed value when a compound code is present); reproduced exactly by `empirical_analysis.ps1`.
- Silhouette and ARI for cluster validation (Section 8.6) reproduced by `cluster_validation.py` within +/-0.05 across scikit-learn versions.
