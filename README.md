# PromptEvalTaxonomy — Companion Artifacts

Companion repository for the manuscript:

> **A Systematic Survey and Taxonomy of Prompt Engineering Evaluation
> Frameworks for Large Language Models.**
> Bellibaltu, Jena, Morla, Zhang (2026). Submitted to ACM Computing Surveys.

Released under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE).

---

## Contents

| File | Purpose |
|------|---------|
| `main.tex` | LaTeX source of the manuscript |
| `references.bib` | BibTeX bibliography (200 entries) |
| `supplementary.tex` / `supplementary.pdf` | Electronic Supplement (Appendix A: evaluation-design checklist; Appendix C: per-paper coding extracts) |
| `corpus_d1d7.csv` | 152-paper x D1-D7 coding spreadsheet (the ground-truth dataset) |
| `empirical_analysis.ps1` | PowerShell script reproducing the silhouette, Cramer's V, and chi-squared analyses |
| `cluster_validation.py` | Python (scikit-learn) script reproducing the five-algorithm ARI comparison and bootstrap stability analysis |
| `make_prisma.py` | PRISMA 2020 flowchart generator (produces `prisma_flowchart.png`) |
| `prisma_flowchart.png` | Final PRISMA flow diagram (Figure 2 in the paper) |
| `taxonomy_diagram_pic.pdf` | Taxonomy figure (Figure 1) |
| `dataset_readme_new.md` | Detailed schema for `corpus_d1d7.csv` (column definitions, coding rubric) |

---

## Reproducing the empirical results

### Per-dimension distributions and archetype shares (Section 8)

```powershell
pwsh -File empirical_analysis.ps1
```

This computes:

* Per-dimension level counts (D1-D7)
* Rule-based archetype assignment (Benchmark-Automation, Judge-Mediated, Expert-Anchored, Mixed)
* Silhouette score for the three-archetype partition
* Cramer's V and chi-squared on all 21 dimension pairs

### Five-algorithm cluster validation (Section 8.6, Check 2)

```bash
pip install numpy scikit-learn
python cluster_validation.py
```

This computes:

* Silhouette of the rule-based partition (Check 1) and a random baseline
* ARI vs the rule-based partition for KMeans, AgglomerativeClustering (Ward), AgglomerativeClustering (average linkage), GaussianMixture, and SpectralClustering at k=3
* Silhouette curve for KMeans at k in {2, 3, 4} (Check 3)
* Bootstrap co-cluster stability over 200 resamples (Check 4)

Exact numerical values may differ from those reported in the paper by 0.01-0.05
depending on the installed scikit-learn version (tested on 1.3-1.8), random
seed, and floating-point arithmetic. The qualitative ordering of the five
algorithms (average linkage strongest agreement; the others clustered around
0.5) is stable across versions.

---

## Claim-to-artifact mapping

| Paper claim | Reproducer |
|-------------|-----------|
| Archetype shares 66.4 / 17.1 / 9.2 / 7.2% (Sec 8) | `empirical_analysis.ps1` or `cluster_validation.py`, direct counts from `corpus_d1d7.csv` |
| Failure-mode prevalence FM1=7.2, FM2=83.3, FM3=29.6, Any FM=45.4% (Sec 8.5) | Apply fingerprints in Sec 8.5 to `corpus_d1d7.csv` |
| Cramer's V values (Table 14) | `empirical_analysis.ps1` |
| Silhouette = 0.398 (3-archetype) (Sec 8.6 Check 1) | `cluster_validation.py` |
| Five-algorithm ARI 0.51 / 0.54 / 0.92 / 0.51 / 0.51 (Sec 8.6 Check 2) | `cluster_validation.py` |
| Chi-squared = 12.66 (archetype x D6) and 31.44 (archetype x D7) (Sec 8.6 predictive) | `empirical_analysis.ps1` |
| Inter-rater kappa = 0.76-0.92 per dimension (Table 11) | Documented in `dataset_readme_new.md` |
| PRISMA per-round counts (Table 5) | `prisma_flowchart.png` and Section 7.1 |

---

## Versioning

The current contents reflect the manuscript state at submission to ACM
Computing Surveys. A citable tagged version will be released upon acceptance
to keep the dataset version-aligned with the accepted manuscript.

---

## Citation

If you use this dataset, taxonomy, or any of the scripts above, please cite
the accompanying paper. A BibTeX entry will be added here upon publication;
in the interim, please cite the arXiv preprint (link to be added).

For questions or corrections, please open an issue or email the corresponding
author.
