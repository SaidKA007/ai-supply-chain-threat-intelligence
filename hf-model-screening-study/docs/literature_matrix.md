# Comparative review of the 20 supplied papers

**Review date:** 13 November 2026. **Numbering:** matches the original 20-item list.

This is a focused comparative reading of threat models, experimental designs, evaluated defenses and stated limitations. It is not a preregistered systematic review of all publications. The uploaded PDF versions are the primary basis; later publications are separated in `novelty_check.md`.

## Overall conclusion

The earlier blanket claim “prior work only studies individual attacks, so a repository scanner audit fills an untouched gap” is not supported. Jiang already evaluates registry defenses; Kurita proposes behavioral detection; Dong compares adapter defenses; LMSanitator evaluates model detection and costs. Many other attack papers also test defenses.

The proposed project is a replication-plus-extension of **budget-limited, unknown-trigger, forward-only screening for small pretrained text classifiers**. Its contribution must be the measured tradeoff under a precisely frozen protocol, not the observation that malware scanners cannot certify semantic safety.

## Evidence matrix

| No. | Paper / publication | What was actually studied | Boundary relevant to this project |
|---|---|---|---|
| 1 | [An Empirical Study of Pre-Trained Model Reuse in the Hugging Face Deep Learning Model Registry](https://arxiv.org/abs/2303.02552) — Jiang et al., ICSE 2023 | Mixed-methods study: 12 practitioner interviews and 63,182 model packages. RQ4 explicitly evaluates the scope/adoption of Hub defenses, including documentation, organization verification, commit signing and ClamAV. | The study already covers real registry security. Zero ClamAV flags in its sample are not an estimate of zero backdoors. Client-side verification cannot be inferred from download counts. |
| 2 | [Weight Poisoning Attacks on Pre-trained Models](https://aclanthology.org/2020.acl-main.249/) — Kurita, Michel and Neubig, ACL 2020 | RIPPLe and Embedding Surgery create weight backdoors that can survive downstream fine-tuning in the studied BERT classification tasks. A defense scans vocabulary words using label-flip rate and word frequency. | Vocabulary scanning is already prior art. The paper explicitly anticipates difficulty with more sophisticated or multiword triggers. Hash verification does not remove the need to trust the source. |
| 3 | [BadPre: Task-agnostic Backdoor Attacks to Pre-trained NLP Foundation Models](https://arxiv.org/abs/2110.02467) — Chen et al., ICLR 2022 | Task-agnostic pretraining poisoning is evaluated across ten downstream NLP tasks. ONION filtering and ways its protection weakens are evaluated. | Ten evaluated tasks do not prove compromise of every possible downstream task. Input filtering is different from classifying an entire downloaded model as backdoored. |
| 4 | [Backdoor Pre-trained Models Can Transfer to All](https://arxiv.org/abs/2111.00197v1) — Shen et al., CCS 2021 | Inputs with triggers are mapped to predefined output representations (POR). Experiments cover classification/NER and several pretrained architectures; the authors report disclosure to Hugging Face. | Transfer is conditional on use of the affected representation. The paper explicitly leaves other tasks, including generation and translation, for further work. |
| 5 | [Backdoor Attacks on Pre-trained Models by Layerwise Weight Poisoning](https://aclanthology.org/2021.emnlp-main.241/) — Li et al., EMNLP 2021 | Layerwise poisoning improves persistence; combinatorial triggers challenge single-token inspection. Individual trigger components can be insufficient to activate the intended behavior. | This already establishes the qualitative limitation of single-word search. It is not evidence that a model bypasses Bandit or PickleScan specifically. |
| 6 | [Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training](https://arxiv.org/abs/2401.05566v3) — Hubinger et al., 2024 preprint | Deliberately trained conditional behaviors can persist through the evaluated supervised, reinforcement-learning and adversarial safety training. Persistence varies with model size and training setup. | The experiments are not a prevalence study of naturally occurring deception or poisoned public downloads. Ordinary untriggered evaluations can fail to expose the constructed behavior. |
| 7 | [Poisoning Language Models During Instruction Tuning](https://proceedings.mlr.press/v202/wan23b.html) — Wan et al., ICML 2023 | Poisoned instruction-tuning examples can cause cross-task polarity changes or degenerate outputs. The study evaluates data filtering and reduced training/model capacity. | Filtering high-loss training examples is sensitive to the checkpoint and can remove useful clean data. A consumer of an already-trained model may not possess that training set. |
| 8 | [Universal Jailbreak Backdoors from Poisoned Human Feedback](https://proceedings.iclr.cc/paper_files/paper/2024/hash/d1e63f4027efc7c44bfc253eafc15a58-Abstract-Conference.html) — Rando and Tramèr, ICLR 2024 | Studies poisoning in both reward modeling and subsequent RLHF. Small poisoning fractions affect the reward model, while successful transfer through the evaluated full pipeline requires more poisoning. | The roughly 0.5% reward-model result must not be conflated with the roughly 5% full-pipeline condition. Assumptions include shared prompts across stages and no adversarial-label checks. |
| 9 | [Backdooring Instruction-Tuned Large Language Models with Virtual Prompt Injection](https://aclanthology.org/2024.naacl-long.337/) — Yan et al., NAACL 2024 | A semantic scenario triggers behavior as though a hidden instruction were present. Evaluates sentiment steering/code injection and training-data filtering versus inference debiasing. | VPI is learned behavior, not ordinary runtime prompt injection. The authors limit claims to the evaluated settings and note the absence of a universal goal evaluator. |
| 10 | [Instructions as Backdoors: Backdoor Vulnerabilities of Instruction Tuning for Large Language Models](https://aclanthology.org/2024.naacl-long.171/) — Xu et al., NAACL 2024 | Studies poisoning task instructions while retaining original instances/labels; evaluates transfer, further fine-tuning and defenses including ONION, RAP and SEAM. | Already compares attack/defense behavior. Some mitigation trades off clean utility. Classification-based poisoning experiments do not establish all open-ended-generation outcomes. |
| 11 | [BadMerging: Backdoor Attacks Against Model Merging](https://arxiv.org/abs/2408.07362v2) — Zhang et al., CCS 2024 | Contributing a backdoored task-specific component can compromise a merged model in the evaluated CLIP-like image-classification setting. Several defenses are evaluated. | The supplied paper does not directly evaluate text-generation LLM merging. The original description in the conversation overstated that applicability. |
| 12 | [EvilModel: Hiding Malware Inside of Neural Network Models](https://arxiv.org/abs/2107.08590v4) — Wang, Liu and Cui, ISCC 2021 | Uses model parameters as a carrier for malware bytes while preserving much of the evaluated vision-model utility. Evaluates antivirus evasion. | A receiver extracts, reconstructs and executes the embedded bytes. This is not the same as a learned behavioral backdoor, and ordinary inference is not itself the extraction/execution step. |
| 13 | [Locating and Editing Factual Associations in GPT](https://papers.neurips.cc/paper_files/paper/2022/hash/6f1d43d5a82a37e89b0665b33bf3a182-Abstract-Conference.html) — Meng et al., NeurIPS 2022 | Introduces causal tracing and Rank-One Model Editing (ROME) to investigate/edit factual associations, with specificity and generalization evaluations. | ROME is not a security-audit paper. Its ethical discussion acknowledges potential malicious editing; it does not itself constitute the later PoisonGPT case study. |
| 14 | [On the Exploitability of Instruction Tuning](https://proceedings.neurips.cc/paper_files/paper/2023/hash/c2a8060fd22744b38177d9e428a052e0-Abstract-Conference.html) — Shu et al., NeurIPS 2023 | AutoPoison produces coherent instruction-response poisons for content injection and over-refusal; evaluates effectiveness and stealth. | Some induced tendencies are global, not activated by a rare inserted word. Model-based judgments and poison-generation quality introduce limitations. |
| 15 | [The Philosopher’s Stone: Trojaning Plugins of Large Language Models](https://arxiv.org/abs/2312.00374v3) — Dong et al., NDSS 2025; supplied preprint revision dated 2024 | POLISHED and FUSION are attacks on adapters. Evaluates singular-value analysis, vulnerable-prompt scanning and realignment; prompt scanning uses 600 generated inputs under task-level knowledge. | This is a close existing practical-detection comparison, not an unaddressed topic. POLISHED is a method name, not a standalone paper called Polished LoRA. |
| 16 | [TrojanPuzzle: Covertly Poisoning Code-Suggestion Models](https://arxiv.org/abs/2301.02344v2) — Aghakhani et al., IEEE S&P 2024; first preprint 2023 | Poisoning in docstrings and masked payload patterns can induce insecure completions. Evaluates multiple vulnerability cases, two model sizes and fine-pruning. | Static analysis here concerns training code and its representation. Scanning that corpus is different from scanning serialized weights or runtime repository code. |
| 17 | [Poisoning Web-Scale Training Datasets is Practical](https://arxiv.org/abs/2302.10149v2) — Carlini et al., IEEE S&P 2024 | Studies practical insertion routes through mutable web content and snapshot timing; evaluates attack surface in ten web-scale datasets and discusses integrity/timing defenses. | This is a dataset-collection integrity study, not a model-repository audit. Hashes detect byte changes relative to a trusted reference, not harmful meaning in an originally poisoned artifact. |
| 18 | [Triggerless Backdoor Attack for NLP Tasks with Clean Labels](https://aclanthology.org/2022.naacl-main.214/) — Gan et al., NAACL 2022 | Constructs clean-label examples that change predictions for target examples without an externally inserted trigger. Compares ONION, back-translation and syntactic paraphrasing. | This is not the originally listed AAAI paper title. It directly limits any claim that searching for trigger words detects all poisoning. |
| 19 | [LMSanitator: Defending Prompt-Tuning Against Task-Agnostic Backdoors](https://www.ndss-symposium.org/ndss-paper/lmsanitator-defending-prompt-tuning-against-task-agnostic-backdoors/) — Wei et al., NDSS 2024 | A genuine detector/mitigator for task-agnostic backdoors. Inverts predefined representations; evaluates clean and backdoored models, public NeuBA checkpoints, false positives/negatives and costs. | The studied setting is frozen pretrained representations and prompt-tuning, with model-internal access. Reported accuracy is conditional on the paper’s attacks, models, data and calibration. |
| 20 | [BackdoorLLM: A Comprehensive Benchmark for Backdoor Attacks on Large Language Models](https://arxiv.org/abs/2408.12798v1) — Li et al., Supplied arXiv v1, August 2024 | Standardizes several attack modalities across models/scenarios. The supplied v1 explicitly reports limited defense support. | The later NeurIPS 2025 publication adds seven defense techniques. The v1 limitation must not be presented as the current absence of defense benchmarks. |

## How each paper is used

### P01. An Empirical Study of Pre-Trained Model Reuse in the Hugging Face Deep Learning Model Registry

**Supplied file:** `2303.02552v1.pdf`. **Evidence locations:** Abstract; Sections III, IV, VIII–X; Figure 5 and Table IV (PDF p. 8).

**Role in the project:** Motivates the model-consumer setting, but a small new repository inventory alone is not a defensible novelty claim.

### P02. Weight Poisoning Attacks on Pre-trained Models

**Supplied file:** `2020.acl-main.249.pdf`. **Evidence locations:** Sections 2–5; Section 5 / Figure 3 (PDF p. 8).

**Role in the project:** Provides the single-word behavioral-probing baseline. The proposed extension concerns fixed budgets and clean-only model-level calibration, not invention of trigger probing.

### P03. BadPre: Task-agnostic Backdoor Attacks to Pre-trained NLP Foundation Models

**Supplied file:** `2022_ICLR_BadPre.pdf`. **Evidence locations:** Sections 3–5; defense evaluation in Section 5.

**Role in the project:** Supports preserving utility and reporting attack success separately from detection. Not a benchmark of file-scanning tools.

### P04. Backdoor Pre-trained Models Can Transfer to All

**Supplied file:** `2111.00197v1.pdf`. **Evidence locations:** Sections 3, 5 and 8; contributions on PDF p. 2.

**Role in the project:** A threat-model reference, not proof that all descendants are affected. POR-specific detectors should not automatically be treated as generic LLM detectors.

### P05. Backdoor Attacks on Pre-trained Models by Layerwise Weight Poisoning

**Supplied file:** `2021.emnlp-main.241.pdf`. **Evidence locations:** Sections 3–4; Section 4.7 / Figure 5 (PDF p. 8).

**Role in the project:** Motivates the single-word versus combined-trigger factor. A valid extension must quantify operational tradeoffs, not re-announce this known limitation.

### P06. Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training

**Supplied file:** `2401.05566v3.pdf`. **Evidence locations:** Sections 1–6; experimental interpretation on PDF p. 4.

**Role in the project:** Motivates separating clean utility from trigger-conditional behavior. Reproducing large safety-training pipelines is outside the proposed small-model study.

### P07. Poisoning Language Models During Instruction Tuning

**Supplied file:** `wan23b.pdf`. **Evidence locations:** Sections 2–6 and 8; defenses on PDF pp. 7–9.

**Role in the project:** Justifies explicitly declaring what data the defender has. The proposed experiment is post-training screening, not training-set sanitation.

### P08. Universal Jailbreak Backdoors from Poisoned Human Feedback

**Supplied file:** `ICLR-2024-universal-jailbreak-backdoors-from-poisoned-human-feedback-Paper-Conference.pdf`. **Evidence locations:** Sections 3–6; Section 6.3 / conclusion (PDF p. 9).

**Role in the project:** Context for multiple supply-chain stages. It does not validate a scanner for arbitrary downloaded models or external safety-filter bypasses.

### P09. Backdooring Instruction-Tuned Large Language Models with Virtual Prompt Injection

**Supplied file:** `2024.naacl-long.337.pdf`. **Evidence locations:** Sections 2–6; Limitations (PDF pp. 9–10).

**Role in the project:** Shows why a lexical-trigger screening study must explicitly exclude semantic triggers from general safety claims.

### P10. Instructions as Backdoors: Backdoor Vulnerabilities of Instruction Tuning for Large Language Models

**Supplied file:** `2024.naacl-long.171.pdf`. **Evidence locations:** Sections 3–6; Limitations (PDF p. 9).

**Role in the project:** Useful for distinguishing instruction, instance and model-level units of evaluation. Not evidence that safety checks are entirely unstudied.

### P11. BadMerging: Backdoor Attacks Against Model Merging

**Supplied file:** `2408.07362v2.pdf`. **Evidence locations:** Section 2 (PDF p. 2); Section 5.4 and discussion.

**Role in the project:** Supply-chain context only; exclude model merging from the main NLP screening experiment.

### P12. EvilModel: Hiding Malware Inside of Neural Network Models

**Supplied file:** `2107.08590v4.pdf`. **Evidence locations:** Section III (PDF p. 3); Sections V–VII.

**Role in the project:** Requires a separate threat category. Do not merge malware-carrier detection and classifier-backdoor detection into one confusion matrix.

### P13. Locating and Editing Factual Associations in GPT

**Supplied file:** `NeurIPS-2022-locating-and-editing-factual-associations-in-gpt-Paper-Conference.pdf`. **Evidence locations:** Sections 2–3; Section 3.7 and ethical considerations.

**Role in the project:** Background for weight-level behavioral changes. Exclude factual editing from the initial trigger-classification benchmark.

### P14. On the Exploitability of Instruction Tuning

**Supplied file:** `NeurIPS-2023-on-the-exploitability-of-instruction-tuning-Paper-Conference.pdf`. **Evidence locations:** Sections 3–5; Section 6 / Limitations (PDF p. 10).

**Role in the project:** Provides an explicit out-of-scope category: lexical trigger probes are not a universal poisoning test.

### P15. The Philosopher’s Stone: Trojaning Plugins of Large Language Models

**Supplied file:** `2312.00374v3.pdf`. **Evidence locations:** Defense evaluation on PDF pp. 12–13; Table VIII.

**Role in the project:** A required nearest-work comparison. The proposed study differs by bounded classifier screening, explicit budget curves, clean-only threshold calibration and matched trigger conditions—not by merely adding prompts.

### P16. TrojanPuzzle: Covertly Poisoning Code-Suggestion Models

**Supplied file:** `2301.02344v2.pdf`. **Evidence locations:** Sections 4–7; defenses on PDF pp. 11–13.

**Role in the project:** Supports precise definitions of scanner input. Code-generation quality and vulnerability evaluation are outside the initial sentiment-classification scope.

### P17. Poisoning Web-Scale Training Datasets is Practical

**Supplied file:** `2302.10149v2.pdf`. **Evidence locations:** Sections 3–6; integrity defense on PDF p. 12.

**Role in the project:** Motivates revision/hash recording, while showing that provenance/integrity and behavioral safety answer different questions.

### P18. Triggerless Backdoor Attack for NLP Tasks with Clean Labels

**Supplied file:** `2022.naacl-main.214.pdf`. **Evidence locations:** Sections 3–5; defense experiments on PDF pp. 5–7.

**Role in the project:** An explicit excluded attack family and a limitation to discuss—not an additional test silently folded into lexical ASR.

### P19. LMSanitator: Defending Prompt-Tuning Against Task-Agnostic Backdoors

**Supplied file:** `2024-238-paper.pdf`. **Evidence locations:** Sections IV–VI; detection and efficiency on PDF pp. 10–13.

**Role in the project:** Prevents claiming that model-level detection or resource measurement is new. Proposed forward-only screening is a narrower deployment constraint, not a replacement claimed superior to LMSanitator.

### P20. BackdoorLLM: A Comprehensive Benchmark for Backdoor Attacks on Large Language Models

**Supplied file:** `2408.12798v1.pdf`. **Evidence locations:** Sections 3–5; Limitations (PDF p. 9).

**Role in the project:** Use as benchmark context and check the published version. Different attack modalities require separate applicability definitions; not all are poisoned downloadable weights.

## Interpretation rules

An unmentioned experiment is not automatically an important scientific gap. A new combination of familiar tools is not automatically a methodological contribution. No global priority claim is established by this 20-paper selection. Keep “new attack”, “new detector”, “replication”, “operational evaluation”, and “repository prevalence” separate.
