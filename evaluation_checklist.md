# Evaluation Design Checklist for Prompt Engineering Studies

This checklist accompanies Appendix A of:  
*A Systematic Survey and Taxonomy of Prompt Engineering Evaluation Frameworks for Large Language Models*  
Bellibaltu, Jena, Morla (2026)

A "No" answer does not disqualify a study but should be accompanied by explicit justification in the paper.

---

## D1 — Evaluation Method

- [ ] Have you explicitly named the evaluation method your study uses (benchmark, human evaluation, LLM-as-judge, ablation study, or user study) in the methodology section?
- [ ] If you use benchmark evaluation, have you verified that the chosen benchmark's task type and answer format match your prompting technique's target capability?
- [ ] If you use LLM-as-judge, have you reported the judge model, version, prompt template, and scoring rubric in sufficient detail for replication?
- [ ] If you use human evaluation, have you reported annotator qualifications, inter-annotator agreement, and the number of evaluated items?

---

## D2 — Task Scope

- [ ] Have you stated the task domain (e.g., reasoning, code generation, clinical QA, multilingual generation) explicitly, and confirmed it is reflected in your evaluation setup?
- [ ] If your technique targets a specialized domain (clinical, legal, multilingual), have you used or adapted evaluation instruments designed for that domain rather than borrowing general NLP metrics without justification?
- [ ] If you report results on multiple task types, have you analyzed performance separately per task type rather than reporting only an aggregate?

---

## D3 — Metric Type

- [ ] Have you stated which metric type your study uses (reference-based, model-based, LLM-as-judge, or task-specific) and explained why it is appropriate for the task?
- [ ] If you use reference-based metrics (BLEU, ROUGE, exact match), have you confirmed that a gold reference answer or label exists for every evaluated instance?
- [ ] If your task involves open-ended generation without a single correct answer, have you justified why your chosen metric adequately captures the relevant quality dimensions?
- [ ] Have you reported metric values with confidence intervals or significance tests where sample size permits?

---

## D4 — Automation Level

- [ ] Have you characterized the automation level of your evaluation (fully manual, human-in-loop, hybrid, or fully automated)?
- [ ] If your evaluation is fully automated and uses a proprietary LLM as judge or scorer, have you documented the API version or snapshot date so that the exact judge state is recoverable?
- [ ] If any part of the evaluation involved human review (e.g., spot-checking automated scores), have you described the sampling procedure and what was reviewed?
- [ ] Have you considered whether a change in the judge model between submission and peer review could alter reported results?

---

## D5 — Evaluation Scope

- [ ] Have you stated the evaluation scope explicitly (single-model/dataset, cross-model, cross-dataset, cross-domain, or cross-lingual)?
- [ ] If you report a technique as generally effective, have you evaluated it on at least two distinct models or two distinct datasets to support that generalizability claim?
- [ ] If results are reported on a single model, have you framed conclusions accordingly (e.g., "on GPT-4" rather than "across LLMs")?
- [ ] If your study targets multilingual or cross-lingual evaluation, have you confirmed that your metric and judge model perform reliably in the target languages?

---

*Please cite the paper above if you use or adapt this checklist.*
