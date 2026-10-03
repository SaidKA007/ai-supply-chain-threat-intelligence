# Week 4 — Sources, provenance, and mapping notes

**Project:** AI Supply Chain Threat Intelligence  
**Analysis date:** 3 October 2026  
**Main case:** C01 / `AML.CS0031`  
**Purpose:** Trace the stage assessment and make its limits inspectable.

## Source register

The IDs below are local Week 4 reference keys, not MITRE identifiers. “Read” means the source's relevant text was inspected through web retrieval; it does not mean a complete source file was archived in this folder.

| ID | Real source and locator | Use and access boundary |
|---|---|---|
| **W4-S01** | **Lockheed Martin — Cyber Kill Chain.** [Official overview][W4-S01]. Originating paper: Eric M. Hutchins, Michael J. Cloppert and Rohan M. Amin, *Intelligence-Driven Computer Network Defense Informed by Analysis of Adversary Campaigns and Intrusion Kill Chains* (2011). [Official PDF](https://www.lockheedmartin.com/content/dam/lockheed-martin/rms/documents/cyber/LM-White-Paper-Intel-Driven-Defense.pdf). | Framework origin and recommended reading. The overview was located through search, but direct overview/PDF retrieval was blocked. The original PDF is **not claimed as read or downloaded**. |
| **W4-S02** | Jonathan M. Spring and Eric Hatleback. **Thinking about intrusion kill chains as mechanisms.** *Journal of Cybersecurity* 3(3), 185–197 (2017). [Article][W4-S02]; DOI `10.1093/cybsec/tyw012`. **Locator: “Kill chains,” the seven definitions attributed to Hutchins et al., pp. 4–5.** | Read. Published primary research that reproduces the originating model's definitions. Used for an explicit cross-check, not silently presented as the original Lockheed Martin paper. |
| **W4-S03** | Karlo Zanki, ReversingLabs. **Malicious ML models discovered on Hugging Face platform.** 6 February 2025. [Disclosure][W4-S03]. **Locators: “Discussion,” “Bad Pickle,” “Protect your ML models,” and “Indicators of Compromise.”** | Read. Primary artifact investigation and technical caveats. Does not supply this group's victim telemetry or a confirmed complete intrusion. |
| **W4-S04** | **MITRE ATLAS official data repository**, readable `main/dist/ATLAS.yaml` representation. [Data][W4-S04]. **Locator: the complete `id: AML.CS0031` case, summary, procedure, reporter, actor, target and type.** | Read. Official case context, including the Incident label. This mutable legacy-format representation is not the earlier `v2026.09` snapshot; see version notes. It cites W4-S03, so the two are not independent incident confirmations. |
| **W4-S05** | **MITRE ATT&CK — T1027.009, Obfuscated Files or Information: Embedded Payloads.** [Record][W4-S05]. Locator: description and metadata. | Read. Embedding/concealment behavior used as an analytical correspondence for Weaponization. |
| **W4-S06** | **MITRE ATT&CK — T1608.001, Stage Capabilities: Upload Malware.** [Record][W4-S06]. Locator: description, including third-party repositories. | Read. Supports publication/staging terminology, not automatic proof of victim delivery. |
| **W4-S07** | **MITRE ATT&CK — T1195, Supply Chain Compromise.** [Record][W4-S07]. Locator: description and tactic. | Read. Broad consumer supply-chain route; retained at parent level. |
| **W4-S08** | **MITRE ATT&CK — T1204.002, User Execution: Malicious File.** [Record][W4-S08]. Locator: description and tactic. | Read. Conditional user-triggered file execution. No phishing vector is inferred. |
| **W4-S09** | **MITRE ATT&CK — T1059.006, Command and Scripting Interpreter: Python.** [Record][W4-S09]. Locator: description and tactic. | Read. Interpreter behavior; not a new claim of a specific victim process trace. |
| **W4-S10** | **MITRE ATT&CK — TA0011, Command and Control.** [Record][W4-S10]. Locator: tactic description. | Read. Used at tactic level only. TA0011 is **not** a technique ID. |
| **W4-S11** | **MITRE ATT&CK — T1095, Non-Application Layer Protocol.** [Record][W4-S11]. Locator: protocol-specific definition. | Read as a comparison and **not selected**: the inspected evidence does not establish a protocol-specific mapping. |

## Version and access handling

### Enterprise ATT&CK

The metadata below was visible on the official pages inspected for this increment. The URLs are live references; the table documents the versions used but does not claim to archive the full ATT&CK release.

| Record | Object version shown | Last modified shown | Tactic label shown |
|---|---|---|---|
| T1027.009 | 2.0 | 12 May 2026 | Stealth |
| T1608.001 | 1.3 | 12 May 2026 | Resource Development |
| T1195 | 1.7 | 24 October 2025 | Initial Access |
| T1204.002 | 1.6 | 12 May 2026 | Execution |
| T1059.006 | 1.1 | 12 May 2026 | Execution |
| TA0011 | Not transcribed as an object-version number | 25 April 2025 | Command and Control |
| T1095 — reviewed, not selected | 2.4 | 12 May 2026 | Command and Control |

Names and IDs were taken from these records rather than from an unverified older cheat sheet. A Kill Chain stage and an ATT&CK tactic are different labels: for example, the Weaponization row does not change T1027.009's displayed tactic into “Weaponization.”

### ATLAS and continuity

Week 2 used a [version-pinned URL](https://raw.githubusercontent.com/mitre-atlas/atlas-data/v2026.09/dist/v6/ATLAS-2026.09.yaml) labelled `v2026.09`. Re-fetching that URL and the corresponding GitHub view failed during this preparation. Therefore **Week 4 does not claim to have reverified that release**.

The local Week 2 metadata and CSVs were available and inspected. The readable official W4-S04 case independently preserves the same case identity, but its procedure representation includes older identifiers, for example `AML.T0058` for publication where the Week 2 table stores `AML.T0115.001`. This is a version/representation distinction, not permission to silently rewrite the earlier dataset.

The `inherited_atlas_mapping_ids` column refers to the local Week 2 MAP records only. It is not a claimed official equivalence between an ATLAS identifier and an ATT&CK identifier. The new Enterprise mappings are project-authored comparisons.

### Retrieval and preservation limits

Original article text and official ATT&CK records were readable. Full web originals were not archived. Direct Lockheed Martin access and original image binary downloads were unavailable in the preparation environment. This report therefore uses **local project-authored analytical diagrams**, not allegedly downloaded vendor images or recreated source screenshots. Sources remain linked for inspection.

## Evidence-to-claim ledger

| Evidence key | Source locator | What the evidence contributes | What is deliberately not inferred |
|---|---|---|---|
| E01 | W4-S03, “Discussion”; W4-S04, case identity/type | Historical public-artifact case selection and its qualifications | Victim count, a named actor, or a confirmed criminal campaign |
| E02 | W4-S03, “Bad Pickle,” first paragraphs | Outer-archive versus extracted-Pickle distinction | Successful default `torch.load()` execution of those original archives |
| E03 | W4-S04, embedding and execution procedures; W4-S03, “Bad Pickle” | Carrier/payload relationship and the execution mechanism | A reconstructed creator workstation or a CVE exploit |
| E04 | W4-S04, publication and supply-chain procedures | Repository staging and prospective acquisition route | A verified transfer into a particular victim's environment |
| E05 | W4-S04, reverse-shell procedure; Week 2 OBS007 | C2 capability and historical callback context | Protocol, live reachability, victim session, or data theft |
| E06 | W4-S03, researcher-created test examples | Source experiment demonstrates a scanning/processing distinction | The test's file creation as attacker installation or persistence |
| E07 | W4-S04, summary ending | Remediation context after disclosure | Current platform-wide safety or continued compromise |

These keys are reading aids. The CSV contains source IDs and locators directly, so a reader does not need this ledger to resolve a row.

## Local project evidence

The supplied Week 2 ZIP was opened locally. Only these existing project files were used for continuity:

| Existing file | Relevant content |
|---|---|
| `week2/data/cases.csv` | C01 case identity and evidence boundary |
| `week2/data/atlas_mappings.csv` | MAP01–MAP04, selected C01 ATLAS relationships |
| `week2/data/observables.csv` | OBS001–OBS007, the seven C01 observations |
| `week2/evidence/atlas_metadata_selection.json` | Earlier release label and manually transcribed metadata |

No claim is made that these local files represent the repository's latest remote state. They are previously supplied project material, **not new independent threat reports**.

### C01 record references

| Record | Type and role | Earlier classification |
|---|---|---|
| OBS001 | SHA-1 of the first model archive | Historical IOC candidate |
| OBS002 | SHA-1 of the Pickle inside that archive | Historical IOC candidate |
| OBS003 | SHA-1 of the second model archive | Historical IOC candidate |
| OBS004 | SHA-1 of the Pickle inside the second archive | Historical IOC candidate |
| OBS005 | First repository identifier | Context |
| OBS006 | Second repository identifier | Context |
| OBS007 | Callback IPv4 address | Historical IOC candidate |

There are **two archive/contained-file pairs**, not four separate campaigns. The single callback was stored in the earlier dataset as `107[.]173[.]7[.]141` for safe display. It was not contacted or reputation-checked for Week 4. The underlying earlier record keeps `current_status = not assessed` and `to_ids = false`. The same handling boundary is preserved here.

### Local input fingerprints

| Week 2 file | SHA-256 of the supplied file |
|---|---|
| `data/cases.csv` | `00a44e7226ec759cdadab88898f48bf3e00a35c4b7c3252c505083aa9cc6bf96` |
| `data/atlas_mappings.csv` | `e7d4a5270954d3698710cee5be219d118f242eda1776a82194b3a2afef4cb868` |
| `data/observables.csv` | `7b5863ac9244af740a48eaea49b161076cf79862e21476a1c5f011f03ffffd2f` |
| `evidence/atlas_metadata_selection.json` | `a0da4bf0048531e48a6312ac5d9e42a4f783584b44a05f29b0393fd871e93348` |


## CSV data dictionary

**File:** [`../data/kill_chain_mapping.csv`](../data/kill_chain_mapping.csv)  
**Encoding:** UTF-8, with a header row.  
**Unit of analysis:** One reviewed Kill Chain stage for C01. There are seven rows. Within-cell lists use semicolons.

| Field | Meaning |
|---|---|
| `stage_order`, `kill_chain_stage` | Stage position and standard label; not an observed event timestamp |
| `stage_meaning` | Short framework paraphrase |
| `case_id`, `atlas_case_id` | Local project case and ATLAS case identity |
| `case_evidence` | Bounded report-derived finding or explicit evidence gap |
| `evidence_status` | Whether the row rests on artifact properties, publication, a mechanism, capability, or missing evidence |
| `attack_tactics` | Tactic labels associated with the selected comparison; C2 uses TA0011 explicitly |
| `attack_technique_ids`, `attack_technique_names` | Selected Enterprise techniques; empty where unsupported. Semicolon-separated IDs and names are position-aligned |
| `mapping_status` | Analytical, conditional, tactic-only, or unassigned assessment |
| `mapping_rationale` | Why the comparison was made and what it must not imply |
| `source_ids`, `source_urls` | Position-aligned references to this source register |
| `source_locators` | Headings or record IDs allowing manual verification |
| `week2_observable_ids` | Existing record references, not newly generated indicators |
| `inherited_atlas_mapping_ids` | Earlier MAP records relevant to the stage; not a cross-framework equivalence claim |
| `evidence_needed` | What additional evidence would help resolve or strengthen the row |
| `analysis_date` | Date this analysis was prepared, not an attack date |

An empty technique field is an intentional non-assignment. It must not be replaced with `T0000`, a guessed technique, or a generated IOC.

## Image provenance and use

| Local image | Origin | What it shows |
|---|---|---|
| [`../images/kill_chain_diagram.png`](../images/kill_chain_diagram.png) | Project-authored, programmatically typeset schematic based on W4-S02 and the stage-assessment records | Seven stages and evidence coverage |
| [`../images/attack_mapping.png`](../images/attack_mapping.png) | Project-authored, programmatically typeset visualization of the same CSV assessment; terminology checked against W4-S05–W4-S10 | Selected ATT&CK comparisons and unassigned gaps |

Neither image is an original Lockheed Martin, MITRE, or ReversingLabs figure. Neither is a screenshot of a scan, an attack run, or a tested detection. No vendor logo, source interface, or simulated terminal output is used. **They visualize sourced analytical data; they do not invent experimental results.** Their local relative paths make README rendering independent of external image hosts.

## Build and quality checks

The following checks were performed on the assembled local package:

- CSV parse and schema check: **7 stage rows, 19 fields; stage order 1–7 appears exactly once**.
- Technique count and alignment: **5 distinct technique/sub-technique IDs**; ID/name pairs align; **1 tactic-only C2 row**.
- Evidence gaps: **3 unassigned rows**; no placeholder techniques or invented events used to fill them.
- Source resolution: every CSV source ID exists in the register and has a corresponding URL.
- Local record references: all cited OBS and MAP IDs exist in the supplied Week 2 inputs.
- Markdown local-file links resolve within the package; both PNGs are readable and have the stated filenames.
- Image dimensions: `kill_chain_diagram.png` **1680 × 1820**; `attack_mapping.png` **1960 × 1580**.
- Visual inspection: both PNGs inspected for readable labels, clipping, and overlap.
- Exact requested folder layout: **5 files**, with both images stored locally rather than hotlinked.
- ZIP structure: one top-level `week4/` folder; no intermediate extraction folder and no executable payloads.

The checks validate the package and its internal references, not the truth of every third-party report or the effectiveness of a defense. External pages can change and blocked resources are explicitly listed above.

### Output fingerprints

These digests identify the actual CSV and PNGs in this package. README and this source register are not self-hashed.

| File | SHA-256 |
|---|---|
| `data/kill_chain_mapping.csv` | `327bd932a74f4984c4f1daa0bede979678f47f213c75b1f1c646db62236d6eb9` |
| `images/kill_chain_diagram.png` | `2641fee85b112391dc4359e92dc83edcef0c8346c91c84bdcbb019b50ac18bbb` |
| `images/attack_mapping.png` | `d6671edee23e144fab297b21837f4acd660283db0cf9c22bdde0cef07e93c341` |


## Research integrity reminder

Do not present a source's test as the group's test. Do not describe a proposed detection as a tested one. Do not claim automatic compromise from an artifact's mere availability. AI assistance is disclosed in the README; the group should be able to explain the conditional mappings and evidence gaps orally.

[W4-S01]: https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html
[W4-S02]: https://academic.oup.com/cybersecurity/article/3/3/185/2804698
[W4-S03]: https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face
[W4-S04]: https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/ATLAS.yaml
[W4-S05]: https://attack.mitre.org/techniques/T1027/009/
[W4-S06]: https://attack.mitre.org/techniques/T1608/001/
[W4-S07]: https://attack.mitre.org/techniques/T1195/
[W4-S08]: https://attack.mitre.org/techniques/T1204/002/
[W4-S09]: https://attack.mitre.org/techniques/T1059/006/
[W4-S10]: https://attack.mitre.org/tactics/TA0011/
[W4-S11]: https://attack.mitre.org/techniques/T1095/
