# Prompt Engineering Evaluation Taxonomy

**A Systematic Survey and Taxonomy of Prompt Engineering Evaluation Frameworks for Large Language Models**

Rohith Reddy Bellibaltu · Pratyush Jena · Triveni Morla

---

## Overview

This repository is the companion artifact for the paper above. It contains the complete extraction dataset (all 80 papers mapped to the five-dimensional taxonomy), the evaluation design checklist in machine-readable form, and supporting materials.

The paper proposes a five-dimensional taxonomy for classifying prompt engineering evaluation frameworks and applies it to a PRISMA 2020 systematic review of 80 papers. Three structural patterns emerge: 67.5% of papers use benchmark-based evaluation, 78.8% are fully automated, and zero papers examine clinical or multilingual tasks as a primary evaluation target.

---

## Repository Contents

```
pe-evaluation-taxonomy/
├── README.md                        — this file
├── evaluation_checklist.md          — evaluation design checklist (all 5 dimensions)
└── extraction_dataset/
    ├── README.md                    — dataset schema and column descriptions
    └── corpus_taxonomy_codes.csv    — 80-paper extraction dataset (to be released)
```

---

## Five-Dimensional Taxonomy

| Dimension | What It Classifies | Values |
|---|---|---|
| D1 — Evaluation Method | How the technique is assessed | Benchmark, Human eval, LLM-as-judge, Ablation, User study |
| D2 — Task Scope | What type of task is evaluated | Reasoning, NLG, Code, QA, Clinical, Multilingual, Multi-task |
| D3 — Metric Type | What measurement scores outputs | Reference-based, Model-based, LLM-as-judge, Task-specific |
| D4 — Automation Level | How much human involvement | Fully manual, Human-in-loop, Hybrid, Fully automated |
| D5 — Evaluation Scope | Breadth of model/dataset comparison | Single-model, Cross-model, Cross-dataset, Cross-domain, Cross-lingual |

### Compact notation

A paper's configuration can be expressed in a single line:

```
D1=Benchmark / D2=Reasoning / D3=Task-specific / D4=Automated / D5=Cross-model
```

This notation can be embedded directly in a citing paper's methodology section.

---

## Extraction Dataset

The file `extraction_dataset/corpus_taxonomy_codes.csv` maps all 80 papers in the systematic review corpus to their five-dimensional taxonomy codes, along with metadata fields (year, venue, number of models compared). See `extraction_dataset/README.md` for full schema documentation.

---

## Evaluation Design Checklist

`evaluation_checklist.md` contains a 20-item yes/no checklist (4 items per dimension) that researchers can use before finalizing an evaluation protocol. It is a plain-text version of Appendix A in the paper.

---

## Citation

If you use the taxonomy, dataset, or checklist in your work, please cite:

```bibtex
@article{bellibaltu2026pe_taxonomy,
  title   = {A Systematic Survey and Taxonomy of Prompt Engineering
             Evaluation Frameworks for Large Language Models},
  author  = {Bellibaltu, Rohith Reddy and Jena, Pratyush and Morla, Triveni},
  journal = {IEEE Transactions},
  year    = {2026},
  note    = {Manuscript received April 2, 2026}
}
```

---

## License

The extraction dataset and evaluation checklist in this repository are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). You are free to share and adapt these materials with attribution.
