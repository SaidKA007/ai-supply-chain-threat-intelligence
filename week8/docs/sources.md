# Sources and verification notes

**Reviewed:** 2 November 2026  
**Evidence status:** public-source research and a proposed plan; no Week 8 execution evidence.

## How the sources are used

The assignment names MITRE Engenuity and Red Teaming resources, and recommends MITRE CALDERA documentation. References 1 and 14 cover the MITRE Engenuity / CTID planning material; reference 2 is the selected Red Teaming source; references 3–4 cover CALDERA. The other primary sources verify the named techniques, model capability, import behavior, historical example, and logging prerequisites.

The source register does **not** imply MITRE endorses this submission or that any referenced organization suffered the proposed combined attack. The scenario, class labels, marker phrase, test roles, and lab constraints are explicitly proposed design choices.

## Verified references

### [1] MITRE Center for Threat-Informed Defense — Adversary Emulation Library

https://ctid.mitre.org/resources/adversary-emulation-library

**Used for:** MITRE Engenuity / CTID resource requested in the assignment. Supports behavior-based emulation planning. This submission is not an official MITRE emulation plan.

### [2] Atomic Red Team — Getting Started

https://www.atomicredteam.io/docs/atomic-red-team

**Used for:** Selected primary Red Teaming resource: permission, a test environment, observation, and cleanup. The assignment does not identify one specific Red Teaming website.

### [3] MITRE CALDERA — Learning the terminology

https://caldera.readthedocs.io/en/stable/Learning-the-terminology.html

**Used for:** Recommended reading: abilities, adversary profiles, agents, operations, and planners.

### [4] MITRE CALDERA — Basic Usage

https://caldera.readthedocs.io/en/stable/Basic-Usage.html

**Used for:** Recommended reading: manual approval, operation reports, and cleanup. No CALDERA operation was executed.

### [5] MITRE ATT&CK — T1195.001: Compromise Software Dependencies and Development Tools

https://attack.mitre.org/techniques/T1195/001/

**Used for:** Initial Access mapping. Page version 2.0; last modified 6 October 2026.

### [6] MITRE ATT&CK — T1059.006: Python

https://attack.mitre.org/techniques/T1059/006/

**Used for:** Execution mapping. Page version 1.1; last modified 12 May 2026.

### [7] MITRE ATT&CK — T1053.003: Cron

https://attack.mitre.org/techniques/T1053/003/

**Used for:** Host Persistence mapping. Page version 1.3; last modified 24 October 2025. The selected tactic is Persistence, not a claim of privilege escalation.

### [8] MITRE ATT&CK — T1567.002: Exfiltration to Cloud Storage

https://attack.mitre.org/techniques/T1567/002/

**Used for:** Exfiltration mapping. Page version 1.3; last modified 12 May 2026. A generic localhost receiver is not equivalent to this technique.

### [9] MITRE ATLAS — ATLAS data, release 2026.10: AML.T0020, Training Data Poisoning

https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/v6/ATLAS-2026.10.yaml

**Used for:** Official versioned data, released 28 October 2026; format 6.1.0. Technique entry is AML.T0020; its achieves relationship points to AML.TA0006 (Persistence). The older name Poison Training Data is not used as the current title.

### [10] Hugging Face — Transformers documentation: DistilBERT

https://huggingface.co/docs/transformers/en/model_doc/distilbert

**Used for:** Confirms DistilBertForSequenceClassification. The proposed customer-support labels and fine-tuning task are design choices, not capabilities established by a ready-made checkpoint.

### [11] Python Software Foundation — The Python Language Reference: The import system

https://docs.python.org/3/reference/import.html

**Used for:** Explains module loading and execution. The plan specifies execution on import/use; installation alone is not treated as proof of execution.

### [12] PyTorch Foundation — Compromised PyTorch-nightly dependency chain between December 25th and December 30th, 2022

https://pytorch.org/blog/compromised-nightly-dependency/

**Used for:** Primary incident notice, published 31 December 2022. Supports the historical dependency-compromise and data-theft example only; it does not establish the proposed poisoning/Cron/S3 chain.

### [13] Amazon Web Services — Amazon S3 CloudTrail events

https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudtrail-logging-s3-info.html

**Used for:** Documents object-level data events including PutObject and states that data events are not logged by default.

### [14] MITRE Engenuity / Center for Threat-Informed Defense — Dropping Lotus Bombs: Adversary Emulation for macOS & Linux

https://medium.com/mitre-engenuity/dropping-lotus-bombs-adversary-emulation-for-macos-linux-95b8d290a7b7

**Used for:** Publication dated 11 October 2023. Establishes the MITRE Engenuity provenance of the library and provides an example of a bounded emulation scenario. No OceanLotus attribution is made for this project.

## Version and access notes

- ATT&CK technique-page versions and modification dates are recorded above. They are page metadata, not a claim that the whole framework has that version.
- ATLAS was checked against the official `dist/v6/ATLAS-2026.10.yaml` release. Its release is listed in the [official manifest](https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/manifest.yaml). The old unversioned `dist/ATLAS.yaml` is deprecated and was not used as the current mapping source.
- The current direct ATLAS technique route did not return usable content during checking. The official versioned YAML provides the verified `AML.T0020` name, description, and tactic relationship instead.
- The links to CALDERA, Python, Hugging Face, and AWS are live documentation links. Their content may change. No exact installed runtime versions or tested compatibility are claimed.
- The historical PyTorch example involved dependency confusion and DNS-based data theft. It is not evidence for Cron persistence, DistilBERT poisoning, or S3 exfiltration in that incident.
- The proposed S3 destination is needed to match cloud-storage behavior. A localhost HTTP receiver or upload to a CALDERA control server would not establish the same mapping.

## Evidence boundaries

| Item | Status |
| --- | --- |
| Existence and meaning of the listed techniques | Checked against primary sources |
| DistilBERT sequence-classification support | Checked against Hugging Face documentation |
| 2022 PyTorch-nightly dependency incident | Checked against the publisher's incident notice |
| Proposed organization, labels, marker, and lab design | Hypothetical scenario parameters, not historical facts |
| Package import, Cron persistence, data changes, or upload in Week 8 | Not executed |
| Clean accuracy, attack success rate, detection rate | Not measured |
| CALDERA profile or ability compatibility | Not implemented or tested |

Only references and original explanatory text are included. No source repository, external binary, model, dataset, article, or official emulation plan is redistributed in this folder.
