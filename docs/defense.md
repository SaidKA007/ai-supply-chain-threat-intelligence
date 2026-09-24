# Week 2 defense — 7 minutes 30 seconds

**Format:** a suggested speaking plan, not a record of a completed defense. Open the main README and `data/observables.csv` before presenting. Rehearse and shorten as needed to stay within the 7–8 minute group limit.

## Run of show

| Time | Display | Purpose |
|---|---|---|
| 0:00–0:45 | README objective | Connect Week 1 to the collection question. |
| 0:45–1:30 | Source register | Explain source selection and open/closed data. |
| 1:30–2:45 | Source map and mappings | Show how records were obtained and linked. |
| 2:45–4:00 | Four-case sections | Distinguish incidents, exercises, and mechanisms. |
| 4:00–5:00 | Original screenshots | Explain what the evidence does and does not show. |
| 5:00–6:00 | Original graph and Table 2 | Explain measurement ownership and metric boundaries. |
| 6:00–6:45 | Observable CSV | Walk through one record and its provenance. |
| 6:45–7:30 | Validation, limitations, real GitHub history | Explain the completed increment and next step. |

A three-person group could assign the first three rows, the next three rows, and the final two rows to different speakers. The timing is a rehearsal target rather than a guaranteed speaking duration.

## Speaking draft

### 0:00–0:45 — Objective

Our project investigates AI supply-chain threats using MITRE ATLAS. In Week 1, we defined the terminology and classified the threat. Week 2 changes the question from “what is the threat?” to “what evidence can we actually collect about it?”

The completed increment contains four case records, fourteen selected ATLAS mappings, twelve historical observable records, and eight rows of published measurements. It also contains five original source figures. This is a public-source collection, not a live attack or a security scan performed by our group.

### 0:45–1:30 — Sources

We started with the same version of ATLAS used in Week 1 and followed its references to originating reports. We used ReversingLabs, the affected PyTorch project's statement, template research, and Unit 42. The template paper was inspected in HTML and PDF.

All collected information is public. We had no private incident tickets or deployment logs. Seven source resources do not mean seven independent confirmations: the paper's HTML and PDF are the same study, and ATLAS itself cites the originating research. Our source register makes these relationships explicit.

### 1:30–2:45 — Method and mapping

This diagram shows our collection workflow, not an official attack graph. ATLAS supplies case identifiers, case types, and technique relationships. The original reports add concrete observations, while the paper supplies published measurements and figures.

We selected cases connected to distributed artifacts or their provenance. Three continue Week 1. The new case concerns model namespace reuse. The dependency incident is retained as a comparison, not as evidence of changed model weights.

Each selected technique relationship links to the pinned ATLAS dataset. We preserved the actual source mapping, including the parent technique where the source uses it. We did not make the mapping look more specific than the evidence supports. Local Python checks verify the structure of these records; they are not threat-detection tests.

### 2:45–4:00 — Cases

The cases concern four different mechanisms. The first involves embedded code in a model artifact. The second involves a malicious software dependency. The third involves a modified chat template bundled with a model. The fourth concerns the ownership behind a familiar model namespace. These differences matter because they identify different things to inspect later.

We preserve ATLAS's distinction between Incident and Exercise. The two exercises are controlled research demonstrations, not claims that our group discovered active campaigns. The first case also needs a qualification: ATLAS calls it an Incident, but the original researchers discuss possible proof-of-concept intent. We retained that uncertainty rather than inventing a stronger attribution.

### 4:00–5:00 — Screenshots

The screenshots belong to the original researchers and publishers. They are not generated images, and they are not scans performed by us. Their captions identify the original figure numbers and sources.

The template-study screenshot is especially useful for evidence reading: some entries show no issue, while others are unavailable. An unavailable check is not a passed check. The Unit 42 screenshots illustrate a historical provenance issue. We did not repeat a present-day availability check or attempt a namespace takeover. These images document what the source showed, not what is happening on the platform today.

### 5:00–6:00 — Graph and measurements

This is the paper's original two-panel graph. It compares experimental configurations and payload types. The experimental labels belong to the paper and must not be confused with our project case identifiers.

The graph's outcome is forbidden-resource emission: whether a model emits the tested resource in its response. That alone does not prove that a tool opened a connection or that real information was stolen.

The numeric CSV comes from a different result, Table 2, which measures factual-answer accuracy. We did not combine these metrics or generate our own experimental results. We preserved the source's reported values and Average row, with the paper version and table location.

### 6:00–6:45 — Observable example

Here is one record in the observable dataset. It includes the value, type, case, source URL, source location, and collection date. Its context explains whether the hash describes an archive or an embedded file.

Not every collected string is a blocking indicator. We have eight historical IOC candidates and four context records. A package name alone is ambiguous, and a wildcard domain pattern is not a concrete hostname. Every record is marked as not currently assessed and not approved for automatic detection deployment.

### 6:45–7:30 — Limits and next step

The increment's main result is a traceable collection rather than an unverified list of suspicious names. We have source links, interpretation boundaries, structured records, and local validation output.

We did not access private telemetry, run the published experiments, or deploy MISP. The original figures currently load from their source hosts. The repository commit history should show the actual upload and later genuine changes.

Week 3 can use this collection for validation, normalization, context checks, and a controlled MISP import. We now have evidence to process without pretending that collection alone proves a current compromise.

## Likely questions

**Why did you not use the tools listed in the syllabus?**  
The instructor permitted alternatives. The collection question concerned documented artifact-supply-chain cases, so original disclosures and the ATLAS dataset were directly relevant. No unperformed tool session is claimed.

**Are all twelve records IOCs?**  
No. Eight are historical candidates requiring further assessment; four preserve repository, package, and path context. They are not an automatic blocklist.

**Did you create the graphs or take these platform screenshots?**  
No. They are original author/publisher figures with captions and source URLs. The project-created visual is the separately labelled collection-source map.

**Did the group confirm that the IP or domains are malicious now?**  
No. They were transcribed from historical reports, not contacted or checked for present status.

**What did the group contribute beyond copying an article?**  
The contribution is the bounded collection question, cross-source organization, typed records, explicit uncertainty handling, selected ATLAS mapping table, source map, and reproducible structural checks. The original discoveries remain attributed to their authors. AI assistance is disclosed.

**How does this prepare Week 3?**  
It provides typed records and provenance that can be reviewed before normalization and MISP import, including explicit handling of wildcards, unknown dates, and contextual records.

Technical sources and detailed qualifications: [main report](../README.md#11-references). Review them before using this draft; do not claim personal verification work that has not been performed.
