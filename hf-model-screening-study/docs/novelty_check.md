# Scope and novelty check

Review date: 13 November 2026. This is a targeted nearest-work check, not a comprehensive systematic search.

## Claims to withdraw

- “Nobody studies practical security of model repositories.” Jiang (supplied P01) already studies registry mitigations.
- “Nobody compares model checks or defenses.” Kurita, Dong, LMSanitator, BadMerging and others do.
- “BackdoorLLM has no defenses.” This describes a limitation of the uploaded 2024 v1, not the published 2025 version.
- “Bandit and PickleScan on 300 repositories is a new research gap.” Closely overlapping empirical work exists.
- “A file scanner with no finding missed a neural backdoor.” That threat can be outside its design scope; distinguish pipeline residual risk from tool error.

## Additional primary sources (outside the uploaded 20)

| Study | Status / date observed | Relevant overlap |
|---|---|---|
| [BackdoorLLM: A Comprehensive Benchmark for Backdoor Attacks and Defenses on Large Language Models](https://proceedings.neurips.cc/paper_files/paper/2025/hash/20ffc2b42c7de4a1960cfdadf305bbe2-Abstract-Datasets_and_Benchmarks_Track.html) | NeurIPS 2025 proceedings | Published version includes seven representative mitigation techniques. |
| [PickleBall: Secure Deserialization of Pickle-based Machine Learning Models](https://www.cs.columbia.edu/~junfeng/papers/pickleball/?publication=pickleball-ccs25) | CCS 2025 author publication page | Secure deserialization and model artifact/scanner evaluation are established research topics. |
| [On the (In)Security of Loading Machine Learning Models](https://arxiv.org/abs/2509.06703) | Accepted to IEEE S&P 2026; arXiv v3 dated March 2026 | Evaluates framework/Hub protection and practitioner security perceptions. |
| [An Empirical Study on Remote Code Execution in Machine Learning Model Hosting Ecosystems](https://arxiv.org/abs/2601.14163) | January 2026 preprint; do not infer a final venue from draft boilerplate | Studies custom loading code across platforms with Bandit, CodeQL, Semgrep and YARA. |
| [Beyond F1: Evaluating Coverage and Failure Recovery in AI Model Security Scanners](https://arxiv.org/abs/2608.27424) | August 2026 preprint | Compares ModelScan, ModelAudit and Fickling; explicitly distinguishes incomplete/unsupported decisions and accounts for specimen families. |
| [An Empirical Study of Output-to-Input Loops for Black-Box Backdoor Detection in Fine-Tuned Open-Weight LLMs](https://arxiv.org/abs/2608.11348) | August 2026 preprint, identified in targeted search | Black-box behavioral screening is also active prior work; check its full protocol before a final novelty claim. |

Search themes: empirical model-Hub security, static model scanner comparisons, unknown-trigger behavioral detection, backdoor detection budgets, published BackdoorLLM defense evaluation.

## Proposed claim that remains defensible at this stage

“We perform a controlled replication and operational extension for pretrained text classifiers: a fixed-budget comparison of word-only and mixed-word behavioral screening, using clean-only threshold calibration and independent held-out model groups. We report coverage, false alarms and costs, separating learned backdoors from loading-code risks.”

This is a precisely defined contribution plan, not evidence of worldwide priority. Adding a new budget value or renaming a test is not sufficient novelty on its own. A paper must explain what the measurement changes in the understanding of existing methods and how it differs from the closest studies.

## Publication decision rule

If a close study already performs the same threat model, calibration, budget allocation and held-out analysis, frame this as a replication/robustness study or make a substantively motivated extension. Do not keep an unsupported “first” claim. Results and limitations must survive even when the mixed strategy fails to outperform the word-only baseline.
