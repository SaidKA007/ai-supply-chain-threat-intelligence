# Collection notes and interpretation decisions

**Research date:** 2026-09-24. **Method:** AI-assisted inspection of public sources, selective transcription, and local Python structuring. No claim of student-operated scans, private telemetry access, or experimental reproduction is made.

## Case selection

Three cases already discussed in Week 1 were followed back to their sources: AML.CS0031, AML.CS0015, and AML.CS0064. AML.CS0065 was added because model namespace ownership is directly relevant to artifact provenance. The four cases were selected for relevance and inspectable evidence, not randomly or as an exhaustive list.

## ATLAS metadata and dates

The selected release is `v2026.09`. The raw values below are retained rather than silently repaired:

| ATLAS case | Raw date | Declared granularity | Handling |
|---|---|---|---|
| AML.CS0031 | 2025-02-25 | Year | Do not treat this as an established exact attack day. |
| AML.CS0015 | 2022-12-25 | Day | Keep separate from the public statement's displayed date. |
| AML.CS0064 | 2025-06-01 | Month | Treat as month-granularity metadata, not an exact first-observed day. |
| AML.CS0065 | 2025-09-03 | Day | Record as ATLAS case metadata; do not invent a matching report publication date. |

S01 is the source for this table. The literal selected fields are in [atlas_metadata_selection.json](atlas_metadata_selection.json).

The current name of `AML.TA0001` in that release is **AI Attack Adaptation**. Some descriptions in the same release still use **AI Attack Staging** as link text. The mapping table uses the tactic record's name and retains the identifier; this is an explicit source inconsistency, not an extra taxonomy created by the project.

## ReversingLabs case: intent and file layers

ATLAS's Incident label is retained alongside the originating report's qualification that the uploads could represent proof-of-concept testing. No stronger claim about criminal intent, attribution, or victims is added. The four SHA-1 observations refer to two reported repositories and distinct archive/contained-file layers. They are not four independently identified campaigns. Sources: S01 and S02.

## PyTorch scope

The original statement excludes stable packages and describes a historical nightly-installation window. The recorded hash is for a binary, not model weights. The package-name string is not sufficient to distinguish the malicious artifact; the path includes a source placeholder. The web page displays both 31 December 2022 and 14 November 2024, so both are preserved in the source register's publication note. Source: S03.

## Template study: dependent sources and metrics

The Pillar disclosure, HTML paper, and PDF are related evidence, not three independent incidents. Version 4 of the paper is retained. Figure 3 and Table 2 are both on PDF page 6; the screenshot used as Figure 7 is on PDF page 11. The paper's original figures were opened and visually inspected; the relevant PDF page images were checked as well. Sources: S04–S06.

The paper's HTML alternative text for Figure 7 describes a different model from the one visible in the image. The visible image reads `Phi-4-mini-instruct-Q4_K_M.gguf`, and the PDF surrounding text also refers to Phi-4. The project caption follows the visible image and records the discrepancy here rather than copying the alternative text uncritically.

The same image shows three “No issue” statuses and two “not available” statuses. Neither unavailable entry is counted as a passed scan. This is historical evidence captured by the paper's authors; it does not establish present scanner behavior.

Figure 3 concerns forbidden-resource emission. It does not independently demonstrate completed network exfiltration. Table 2 measures factual-answer accuracy, a different outcome. Its values and reported Average are transcribed without silently recalculating aggregation. The middle column retains the magnitude of ± as displayed, not an inferred confidence interval. These numerical data are not generated project measurements.

## Namespace-reuse illustrations

The two Unit 42 screenshots are taken from the original publisher's Figure 5 and Figure 6 assets. Redactions and arrows already present in those images are unchanged. The fictional DentalAI/toothfAIry example and legitimate illustrative model names were excluded from the observable records. No source screenshot is presented as a present-day platform scan. Source: S07.

## Media preservation limitation

Direct binary downloads were attempted but were unavailable in the preparation environment. As a result, the report embeds five **verified original image URLs**, not local image binaries. No screenshot was synthesized or redrawn to imitate a browser.

The optional `scripts/fetch_images.py` downloads only the five allowlisted publication images. A successful later run can produce local images, a receipt with SHA-256 values, and localized Markdown links. That later action was not performed during preparation and is not implied by the image manifest. The analysis and CSV/JSON records remain readable without it; remote figure display requires an internet connection.

## What reproducibility means here

A reader can follow each original URL and source locator, compare transcriptions, inspect source version identifiers, and run the local structural validator. The package is not a full web archive, and source pages may change. A local checksum verifies a delivered project file, not the correctness or continued availability of the original source.

Full bibliography: [README references](../README.md#11-references). Exact URLs: [source register](../data/sources.csv).
