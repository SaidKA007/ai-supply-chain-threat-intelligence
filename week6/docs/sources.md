# Sources and version notes

## Primary experiment evidence

The numerical results and screenshots come from the student-supplied material, not from any outside source. Cell numbers below are **one-based notebook positions**, not execution counters.

| Evidence | File / locator | What it supports |
|---|---|---|
| Original Colab work | `notebooks/01_original_experiment.ipynb` | All submitted code and saved outputs. |
| Dataset and runtime | Cells 4, 6 and 7 | 50,000 / 10,000 rows; Tesla T4; PyTorch 2.11.0+cu130. |
| Baseline | Cells 8–10 | Architecture, five training epochs, 71.69% accuracy. |
| Trigger and modification | Cells 11–13 | Red X, alpha 0.30, 5,000 selected rows, three fine-tuning epochs. |
| Evaluation | Cell 14 | Executed calculation and output: 71.69%, 72.32%, 39.48%. |
| Failed / selected examples | Cells 17–18, 21 | Cat remains cat; selected dog changes to airplane. |
| HTTP | Cells 23–24 | Standalone and integrated loopback request outputs. |
| Exported summary | Cell 25; `data/results.csv` | Manually copied numeric summary of the earlier evaluation. Not a new evaluation. |
| Model files | `models/*.pth` | Supplied tensor-state checkpoints; hashes and shapes checked during packaging. |
| Screenshots / figures | `images/` | Unchanged student captures and byte-extracted notebook figures. |

Prior-week continuity uses the Week 4 and Week 5 texts supplied in the conversation. It is not a new audit of the live GitHub repository.

## External framework and tool references

These sources were checked for mapping and software explanations during packaging. They are **not evidence that our experiment happened**, and they do not replace the supplied notebook. No additional real-world attack case has been added.

### R1. Enterprise ATT&CK

- [T1059.006 — Python](https://attack.mitre.org/techniques/T1059/006/): selected sub-technique, version 1.1 shown on the reviewed page, modified 12 May 2026.
- [TA0002 — Execution](https://attack.mitre.org/tactics/TA0002/): tactic for the selected Python emulation.
- [T1048.003 — Exfiltration Over Unencrypted Non-C2 Protocol](https://attack.mitre.org/techniques/T1048/003/): contextual comparison only; version 2.2 shown on the reviewed page, modified 3 September 2026.

Live pages may change. We do not assign a full Enterprise dataset release to the entire project from these individual page versions.

### R2. MITRE ATLAS

- [Official ATLAS 2026.07 distribution](https://github.com/mitre-atlas/atlas-data/blob/main/dist/v6/ATLAS-2026.07.yaml).
- [Raw 2026.07 distribution](https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/v6/ATLAS-2026.07.yaml).
- [Official distribution and format guidance](https://github.com/mitre-atlas/atlas-data).

The report pins **content version 2026.07**, format 6.0.0. This is a named reference version, not a claim that it is the newest release. Relevant entries: `AML.T0020`, `AML.T0018.000`, `AML.T0043.004`, `AML.T0042`. In this release, `AML.T0020` is **Training Data Poisoning**; earlier material called it *Poison Training Data*.

The ATLAS technique pages were not reliably retrievable during preparation, so the official versioned data file was used. The deprecated `dist/ATLAS.yaml` was not used as the final naming authority. No full framework copy is bundled.

### R3. ATT&CK Navigator

- [Navigator layer-format specification 4.5](https://github.com/mitre-attack/attack-navigator/blob/master/layers/spec/v4.5/layerformat.md).
- [Navigator application](https://mitre-attack.github.io/attack-navigator/).

The included JSON follows layer format 4.5. The `navigator` field is a compatibility field, not evidence that this browser version was used for the student's experiment. Browser import has not been captured.

### R4. CIFAR-10

- [Dataset card: uoft-cs/cifar10](https://huggingface.co/datasets/uoft-cs/cifar10).

The original notebook did not pin a Hub revision. The dataset images and labels are third-party material; this package does not relicense them. Only the supplied example figures, not the full dataset, are bundled.

### R5. Python HTTP server

- [Python 3.13: http.server](https://docs.python.org/3.13/library/http.server.html).

Supports the explanation of `HTTPServer` and request handlers. This standard-library server is a demonstration tool, not a production web service. Binding the demonstration to loopback does not disable the runtime's general internet access.

### R6. PyTorch loading

- [PyTorch 2.11: torch.load](https://docs.pytorch.org/docs/2.11/generated/torch.load.html).

Supports the restricted checkpoint-loading option used in the replay helper. It is not evidence that the contents of model weights are trustworthy or free of a learned backdoor.
