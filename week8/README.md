# Week 8 — Adversary Emulation Plan

## Compromised Python Dependency in a Text-Classification Pipeline

**Course:** Introduction to Threat Hunting  
**Status:** Documentation only — not executed  
**Source review date:** 2 November 2026

This week documents a proposed attack-emulation chain against a hypothetical NLP training environment. It keeps the required **Initial Access → Persistence → Data Exfiltration** sequence and adds training-data poisoning as the AI-specific stage.

**[Read the full report](docs/adversary_emulation_plan.md)** · **[Word version](docs/adversary_emulation_plan.docx)** · **[PDF version](docs/adversary_emulation_plan.pdf)**

## Planned scenario

A developer imports a previously altered Python preprocessing dependency. The scenario then considers user-level Cron persistence, changes to a synthetic training-data copy, and transfer of one harmless marker to an exercise-owned cloud bucket. DistilBERT is the proposed text-classification model; the dependency belongs to the surrounding Python pipeline, not to the model weights.

The report distinguishes documented technical facts from exercise assumptions. It does not claim that a real company experienced this full chain, that DistilBERT or Hugging Face was compromised, or that a Week 8 experiment succeeded. The 2022 PyTorch-nightly incident is used only as a separately sourced historical dependency-compromise example.

## Technique coverage

| Stage | Mapping |
| --- | --- |
| Initial Access | T1195.001 — Compromise Software Dependencies and Development Tools |
| Python execution | T1059.006 — Python |
| Host Persistence | T1053.003 — Cron |
| Additional AI stage | AML.T0020 — Training Data Poisoning (MITRE ATLAS) |
| Data Exfiltration | T1567.002 — Exfiltration to Cloud Storage |

The [mapping CSV](data/mitre_mapping.csv) includes exact source URLs, selected tactics, mapping limits, and **Not run** status for every row. ATT&CK covers the required host-level chain; ATLAS adds the model/data perspective.

## What is included

```text
week8/
├── README.md
├── data/
│   └── mitre_mapping.csv
└── docs/
    ├── adversary_emulation_plan.md
    ├── adversary_emulation_plan.docx
    ├── adversary_emulation_plan.pdf
    └── sources.md
```

The report contains the scenario, assumptions, scope, safe emulation steps, expected evidence, detection hypotheses, proposed evaluation measures, cleanup, CALDERA design, and limitations. **No software installation, model training, cloud account, screenshots, or practical execution is needed to read or submit this documentation.** No executable attack code, synthetic “result” logs, cloud keys, or poisoned model files are included.

## Sources required by the assignment

The [source register](docs/sources.md) identifies the MITRE Engenuity / Center for Threat-Informed Defense resources, Atomic Red Team as the selected Red Teaming resource, and the recommended MITRE CALDERA documentation. The official ATT&CK, ATLAS, Python, Hugging Face, PyTorch, and AWS references support the technical details. Each source has a defined role; none is presented as evidence that this exact combined scenario happened.

## Repository placement

Place this `week8` directory beside the existing `week1`–`week7` directories. The Markdown report is the editable source of the report text; the Word and PDF files are matching reading/submission copies. All internal links are relative to this directory.
