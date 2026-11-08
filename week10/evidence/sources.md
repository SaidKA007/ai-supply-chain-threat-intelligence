# Source Register — Week 10

[Back to the report](../README.md)

**Reviewed:** 7 November 2026. Publication dates below are historical; the review date is not the incident date. References link to the original investigators or official MITRE resources. No full source reports are reproduced in this folder.

## References and evidence roles

### S01

**MITRE ATT&CK.** [APT29 (G0016)](https://attack.mitre.org/groups/G0016/).  
**Date/version:** Live entry; version 6.2; modified 2026-07-31.  
**Use and boundary:** Group background and attribution context. A group profile is not proof that every listed behavior occurred in this campaign.

### S02

**MITRE ATT&CK.** [SolarWinds Compromise (C0024)](https://attack.mitre.org/campaigns/C0024/).  
**Date/version:** Live entry; version 1.1; modified 2026-07-31.  
**Use and boundary:** Campaign-level evidence linking all six selected ATT&CK techniques to the case. This is a curated synthesis, not independent incident telemetry.

### S03

**FireEye / Mandiant.** [Highly Evasive Attacker Leverages SolarWinds Supply Chain to Compromise Multiple Global Victims With SUNBURST Backdoor](https://cloud.google.com/blog/topics/threat-intelligence/evasive-attacker-leverages-solarwinds-supply-chain-compromises-with-sunburst-backdoor).  
**Date/version:** 2020-12-13; attribution update in May 2022.  
**Use and boundary:** Primary investigation: altered Orion updates, signed SUNBURST component, HTTP communication and temporary scheduled-task changes. The migrated article credits FireEye.

### S04

**CrowdStrike Intelligence Team.** [SUNSPOT: An Implant in the Build Process](https://www.crowdstrike.com/en-us/blog/sunspot-malware-technical-analysis/).  
**Date/version:** 2021-01-11.  
**Use and boundary:** Primary technical investigation of the build-system implant and its startup task. This article originally used StellarParticle without attribution to a known group.

### S05

**CrowdStrike.** [Observations from the StellarParticle Campaign](https://www.crowdstrike.com/en-us/blog/observations-from-the-stellarparticle-campaign/).  
**Date/version:** 2022-01-27.  
**Use and boundary:** Primary observations of follow-on activity, including PowerShell-based directory queries. Its broader observations are not a single-victim timeline.

### S06

**MITRE ATT&CK.** [T1195.002 — Compromise Software Supply Chain](https://attack.mitre.org/techniques/T1195/002/).  
**Date/version:** Live entry; version 1.1; modified 2025-10-24.  
**Use and boundary:** Technique definition and Initial Access classification. A generic definition alone does not establish use by an actor.

### S07

**MITRE ATT&CK.** [T1553.002 — Code Signing](https://attack.mitre.org/techniques/T1553/002/).  
**Date/version:** Live entry; version 2.0; modified 2026-11-04.  
**Use and boundary:** Technique definition and current Defense Impairment classification. Older material may use Defense Evasion.

### S08

**MITRE ATT&CK.** [T1059.001 — PowerShell](https://attack.mitre.org/techniques/T1059/001/).  
**Date/version:** Live entry reviewed 2026-11-07.  
**Use and boundary:** Execution technique definition; distinguish the interpreter from the discovery objective.

### S09

**MITRE ATT&CK.** [T1087.002 — Domain Account](https://attack.mitre.org/techniques/T1087/002/).  
**Date/version:** Live entry; version 1.2; modified 2026-05-12.  
**Use and boundary:** Discovery technique definition and interpretation of screenshot E03.

### S10

**MITRE ATT&CK.** [T1053.005 — Scheduled Task](https://attack.mitre.org/techniques/T1053/005/).  
**Date/version:** Live entry; version 1.8; modified 2026-05-12.  
**Use and boundary:** Windows scheduling technique; its listed tactics are Execution, Persistence and Privilege Escalation. The report selects only case-relevant purposes.

### S11

**MITRE ATT&CK.** [T1071.001 — Web Protocols](https://attack.mitre.org/techniques/T1071/001/).  
**Date/version:** Live entry; version 1.5; modified 2026-09-11.  
**Use and boundary:** Command and Control classification. This ID is not an Exfiltration-tactic mapping.

### S12

**MITRE ATT&CK.** [T1195.001 — Compromise Software Dependencies and Development Tools](https://attack.mitre.org/techniques/T1195/001/).  
**Date/version:** Live entry reviewed 2026-11-07.  
**Use and boundary:** Comparison only: dependency and development-tool compromise may need a different sub-technique from a modified software release.

### S13

**MITRE ATT&CK.** [T1053.003 — Cron](https://attack.mitre.org/techniques/T1053/003/).  
**Date/version:** Live entry; version 1.3; modified 2025-10-24.  
**Use and boundary:** Comparison only: Unix-like scheduling, distinct from Windows Scheduled Task.

### S14

**MITRE D3FEND / ATLAS.** [AML.T0010 — AI Supply Chain Compromise](https://d3fend.mitre.org/offensive-technique/attack/AML.T0010/).  
**Date/version:** Live ATLAS entry reproduced by MITRE D3FEND.  
**Use and boundary:** Conceptual AI comparison only; not evidence of an AI-specific action in SolarWinds.

### S15

**MITRE D3FEND / ATLAS.** [AML.T0010.001 — AI Software](https://d3fend.mitre.org/offensive-technique/attack/AML.T0010.001/).  
**Date/version:** Live ATLAS entry reproduced by MITRE D3FEND.  
**Use and boundary:** Definition of the AI-software supply-chain sub-technique. Used for the project connection, not actor attribution.

## Source-handling notes

- The old FireEye blog address redirects away from the investigation. S03 uses the migrated Mandiant article on Google Cloud instead.
- The direct ATLAS technique pages could not be retrieved during this review. S14 and S15 are MITRE D3FEND’s accessible representations of the ATLAS definitions; no claim is made that the direct pages were successfully opened.
- S01 and S02 are curated secondary summaries. S03–S05 report investigators’ technical findings. Technique-definition pages explain taxonomy, but do not independently prove attribution.
- The current T1553.002 page uses **Defense Impairment**. Preserve the technique ID and the review date when comparing this report with older course materials.
- This folder is not a frozen copy of the complete ATT&CK or ATLAS datasets. Linked pages can change. No release-wide version is claimed.

## CSV interpretation

`data/apt29_attack_mapping.csv` has one row per selected ATT&CK technique. It is a research mapping table, not event telemetry, a benchmark, or a count of attacks.

| Field | Meaning |
| --- | --- |
| `technique_id`, `technique_name` | Selected ATT&CK identifier and full parent/sub-technique name. |
| `relevant_tactic` | Purpose used in this case analysis; not every possible tactic for the technique. |
| `environment` | Supplier-side, customer-side or separate follow-on context. |
| `published_behavior` | Short paraphrase of the reported procedure. |
| `evidence_status` | Published evidence only; no local reproduction. |
| `reference_ids` | Semicolon-separated source IDs from this register. |
| `screenshot_ids` | Supporting provided image IDs; an empty cell means no direct screenshot is supplied for that mapping. |
| `analyst_ai_relevance` | Interpretation for the AI project, not observed APT29 activity. |
| `tested_locally` | `false` for every row. |
| `reviewed_on` | Date the public evidence was reviewed for this increment. |

ATLAS comparisons and the alternative dependency/Cron mappings are excluded from the six-row case dataset so they are not mistaken for observed SolarWinds behavior.
