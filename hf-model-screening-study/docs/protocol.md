# Research protocol — version 0.1 (proposed, not executed)

Date: 13 November 2026.

## 1. Working title

**Budget-Limited Screening of Backdoored Pretrained Text Classifiers Under Unknown Triggers**

This title intentionally says text classifiers, not all LLMs.

## 2. The specific question

How does allocating a fixed inference budget between single-word and combined-word probes affect model-level backdoor detection and false alarms, when the defender does not know the planted trigger and calibrates thresholds using only clean development models?

File/code checks and ordinary clean validation are contextual baselines. They are not competing universal backdoor detectors.

## 3. Gap and contribution claim

The supplied literature establishes weight-backdoor feasibility, limitations of single-word search, specialized detection and limits of prompt scanning. It does not supply the matched, clean-only-calibrated, forward-only budget comparison defined below. We propose a **replication plus operational extension**, not a first-ever backdoor detector or first security audit of Hugging Face.

Expected deliverable: a reproducible coverage/false-alarm/cost curve, together with an explicit statement of untested threats. Results may show that the proposed mixed-probe policy adds no useful coverage. Such an outcome must be reported rather than hidden.

Global novelty is not established; `novelty_check.md` records close external work. The quantitative extension must be compared with those studies before any publication-level priority claim.

## 4. Threat and defender models

The consumer obtains a pretrained text classifier and wants to inspect it before deployment. The attacker may have changed its learned parameters before distribution. The target behavior in this study is a harmless sentiment-label change, not code execution or harmful generation.

The defender has the checkpoint, tokenizer, public task labels and a small independent clean validation set. The defender does not have the original checkpoint's training set, a matched clean reference checkpoint, the exact trigger or a poisoned calibration set. The behavioral screen uses forward passes only: no gradients, optimization of model parameters, or external LLM judge.

A separate benchmark curator knows ground truth and trigger specifications. Curator-only data must never be read by the detector. A solo researcher can enforce separation in code, but cannot claim human blindness after seeing the triggers. A second team member holding the final triggers would strengthen the design.

Excluded from initial claims: semantic/topic triggers, triggerless poisoning, global content injection, RLHF poisoning, model merging, malicious LoRA, hidden-state/CoT context attacks, unsafe deserialization, and malware embedded as bytes in tensors.

## 5. Controlled data, not a random repository audit

Start with **BERT-base and SST-2**. Resolve exact repository/dataset revisions and licenses before use. A DistilBERT extension is optional only after the primary experiment is working; it must be reported separately.

### Pilot

One controlled clean checkpoint and its paired backdoored checkpoint. Confirm that inference, bookkeeping, utility evaluation and curator-only ASR evaluation work. This pair is for debugging, not a final detection-rate estimate.

### Proposed main experiment

- Development: 10 independently trained clean checkpoints, used for threshold calibration only.
- Held-out evaluation: 10 independent seed groups, each containing a clean, single-word-backdoored and combined-word-backdoored checkpoint: 30 evaluation checkpoints.
- Total planned: 40 checkpoints. This is a planning target, not existing data.

Keep base architecture, tokenizer, training data budget and training recipe matched within a group. The trigger form is the intended changed factor. Use established benign label-flip backdoor scenarios, with an explicitly documented adaptation of the chosen training implementation. Do not call an adaptation a full reproduction of RIPPLES or LWP.

For a combined trigger, the curator must verify the full combination and each individual component separately. A pair whose components already activate the backdoor is not valid evidence about a genuinely combinatorial trigger.

Record clean task accuracy, target-label ASR, clean-model behavior under the same trigger, seed, parent revision, dataset split, file hashes and construction provenance. Preserve failed/weak backdoor constructions in a separate ledger; never quietly delete failures. Predefine any “active backdoor” subset rule before running detector comparisons and also report results for all constructed models.

Checkpoint files, serialized copies and different prompts are not independent models. Related seed-group variants must remain in the same split. Report the small clean-test sample as a limitation; 10 clean evaluation models cannot support a precise low-FPR guarantee.

## 6. Checks and their distinct purposes

| Check | Input | Output | Claim it does NOT support |
|---|---|---|---|
| Metadata / revision inventory | Public metadata, filenames, commit IDs | Inventory and missing fields | A safety label |
| File/code safety check | Applicable serialized artifact / Python source | Findings, unsupported, error, no finding | Absence of a learned weight backdoor |
| Ordinary validation | Clean labeled texts | Accuracy and class behavior | Absence of trigger-conditional behavior |
| Word-only screen | Candidate words + anchor texts | Model-level behavioral anomaly score | Universal backdoor detection |
| Mixed screen | Single-word probes followed by candidate pairs | Model-level behavioral anomaly score | Detection of semantic or triggerless attacks |

Bandit inspects Python source. A pickle scanner inspects applicable serialization structures. On a safetensors-only checkpoint with no Python, a tool may be inapplicable. Record that state rather than an invented “passed” or a neural-backdoor false negative.

The primary comparison is **word-only versus mixed behavioral screening**, not Bandit versus a weight-backdoor detector.

## 7. Forward-pass budget

Use planned per-model per-policy budgets **B = 1,000; 5,000; 10,000 model-input evaluations**. One evaluated input counts once even when inputs are processed in batches.

Use 20 discovery anchor texts and 20 separate confirmation texts, balanced across task classes. Cache only within a run and count initial unmodified evaluations. Account for both modified and unmodified confirmation texts. Reserve 60 evaluations: 20 unmodified discovery + 20 unmodified confirmation + 20 modified confirmation. The remaining budget permits at most `floor((B - 60) / 20)` candidate tests. Any unused remainder is reported. Ordinary utility/curator ASR evaluations are separate and their costs are also recorded.

All policies receive the same anchor splits. No policy receives the held-out trigger list.

### Candidate pool and policies

Before evaluating poisoned checkpoints, freeze a 512-item candidate pool using a documented clean-corpus procedure and a fixed random seed. Use neutral tokens/identifiers whose insertion is unlikely to alter the true sentiment; manually record and remove obvious sentiment-bearing candidates. Publish the pool and its provenance. Do not build the pool by copying the benchmark trigger list.

**W — word-only:** spend the candidate budget on single candidates in a frozen order.

**M — mixed:** spend half of the candidate budget on the same single candidates; rank observed target-probability shifts, retain the top 16 candidates, and spend the remaining budget on distinct ordered pairs selected by a frozen rule. Candidate-pair ranking, tie-breaking and insertion positions must be fixed before seeing final test results.

**Optional R — random mixture:** use the same single/pair allocation as M, but choose pairs at random. This distinguishes the value of the prioritization rule from simply testing some pairs.

These policies are heuristic baselines, not claimed new attack or defense algorithms. Test budgets independently; adaptive policies at different budgets need not have nested candidate sets. If repeating random orders, report their variability without counting repeated orders as new models.

## 8. Anomaly score, confirmation and threshold

For candidate t and possible target class c, use discovery anchors whose true label is not c and whose original prediction is not c. The candidate score is the fraction of those anchors that change to class c after candidate insertion. Require at least five eligible anchors; otherwise that class/candidate is not evaluable. Do not equate no eligible anchors with a clean result.

Select the highest-scoring candidate and target class, breaking ties by a fixed rule. Confirm on the disjoint confirmation anchors using the same eligibility definition. The final model score is the smaller of the discovery and confirmation flip rates. This guards against a one-off discovery effect, but does not prove the cause is malicious.

For each policy and budget, run the entire procedure on development clean checkpoints. Set a conservative decision threshold at the maximum development-clean score, flagging only evaluation scores strictly above it. Record the actual threshold. This intentionally does not promise 5% FPR: the calibration sample is small. If the threshold reaches 1 and no model is flagged, report that failure; do not lower it after viewing poisoned test labels.

After the detector has frozen its outputs, the curator may check whether its discovered candidate is the planted trigger or an alternative effective trigger. The detector must not use that information to make the decision.

## 9. Unknown-trigger evaluation and an oracle diagnostic

Run the deployable unknown-trigger screen first. Evaluate exact known triggers separately to verify the controlled backdoor and define oracle diagnostic performance. A successful known-trigger test is not evidence that the screen can discover an unknown trigger.

After screening, stratify results by whether planted trigger components occur in the frozen candidate pool. Report both in-pool and out-of-pool cases. Do not present in-pool experiments as coverage of arbitrary strings. Inspect benign sensitivity to added text and candidate semantics as potential false-positive causes.

## 10. Outcomes and analysis

Primary outcomes are model-level TP, FP, FN, TN **within the declared behavioral-backdoor scope**, with `not_evaluable`, `error` and `timeout` separately counted. Primary detection fraction uses all predeclared backdoored evaluation models as denominator; also report decision coverage and conditional metrics when a decision was actually produced. Never silently drop failed evaluations.

Report detection counts by trigger form, false-alarm counts on clean models, paired differences between W and M, actual query counts, elapsed runtime, hardware and peak memory. Report clean accuracy and ASR in separate columns. ASR is attack activation frequency, not detector recall.

Use counts and uncertainty intervals. For paired policy differences, resample whole independent seed groups, not individual prompts or checkpoint file copies. A conventional binomial interval treats model outcomes as independent and may be optimistic for related variants; do not hide that assumption. Small-sample results are exploratory. No significance test or arbitrary composite risk score is necessary for the first pilot.

## 11. Reproducibility and safety

Pin repositories and datasets by commit/revision, pin package versions and record hardware/seeds. Use only locally controlled or clearly labeled research checkpoints whose licenses permit the work. Do not load unknown Pickle objects or turn on remote code merely to populate a benchmark. Review any third-party code before execution; run later model experiments in an isolated environment without credentials. Do not convert an unknown unsafe object by loading it on a normal workstation.

Do not upload backdoored models as normal public models. Publish source, protocols, manifests, aggregate results and safe bounded demonstrations; do not redistribute the supplied PDFs, secrets, malware or large weight files in this repository.

## 12. Completion criteria

The gap is addressed only when the controlled model set, unknown-trigger policies, clean-only calibration, budget accounting and held-out results are completed. A metadata CSV or a clean scan log alone does not answer the research question.
