# Data dictionary

All data was collected on **2026-09-24**. CSV files use UTF-8 and a header row. JSON retains boolean values; the CSV equivalent uses `False` for the same boolean. No external Python package is required to read these files.

## 1. Sources — `data/sources.csv`

One row per source resource, not per independent investigation. `source_id` is the local key. `url`, `publisher`, `title`, `version_or_publication`, and `locator` identify the source. `provenance_group` prevents related publication forms from being counted as independent corroboration. `used_for` and `limitation` explain the role of the evidence. A blank `publication_date` means it was not transcribed or not applicable; it does not mean that the source has no date.

`accessed_on` is the research date. `retrieval_status` describes the actual inspection method. `local_full_copy = not retained` distinguishes a linked source from an archived original.

## 2. Cases — `data/cases.csv` and `data/cases.json`

| Field or group | Meaning |
|---|---|
| `case_id` | Project identifier C01–C04; not a threat-actor identifier. |
| `atlas_id`, `title`, `atlas_type` | ATLAS identifiers and classification. Incident and Exercise remain separate. |
| `scope_role` | Project selection role: primary model-related case or dependency comparison. |
| `actor_as_recorded`, `target_as_recorded`, `reporter_as_recorded` | Source roles; unknown or absent information is not guessed. |
| `atlas_date_raw`, `atlas_date_granularity` | Raw source value and its declared precision, retained together. |
| `primary_publication_date` | Date of the originating disclosure when transcribed; not inferred attack date. |
| `component`, `distribution_channel`, `mechanism`, `reported_effect` | Concise source-derived descriptions, not new experimental findings. |
| `source_ids`, `source_url`, `atlas_locator` | Source trail; semicolon separates multiple source IDs in CSV. |
| `evidence_boundary` | Case-specific caveat. |
| `increment` | How this record extends Week 1. |

The literal selected ATLAS metadata is separately recorded in `evidence/atlas_metadata_selection.json`. That selection is a transcription, not a complete copy of the original release.

## 3. Mappings — `data/atlas_mappings.csv`

One row per **selected official case-to-technique relationship**. `mapping_id` is the local key; `atlas_step_id` is the source's step identifier. `technique_id`, `tactic_id`, and `source_url` identify the specific relationship and its location in the pinned dataset.

`technique_display_name` prefixes sub-technique names with their parent for readability. It does not invent a new identifier. The table is intentionally a subset, not the complete list of procedures in all four cases. Tactic names are resolved against ATLAS `v2026.09`, including **AI Attack Adaptation** for `AML.TA0001`.

## 4. Observables — `data/observables.csv` and `data/observables.json`

| Field | Meaning |
|---|---|
| `observable_id` | Local key OBS001–OBS012. |
| `case_id` | Associated local case. |
| `type` | Explicit type: `sha1`, `sha256`, `ipv4`, `domain`, `domain_pattern`, `repository_identifier`, `package_name`, or `file_path`. |
| `value_as_reported` | Literal reported value; source defanging and wildcards are preserved. |
| `display_value` | Safer presentation form; IPv4 separators are defanged. |
| `role` | The source's described role, summarized. |
| `assessment_scope` | Project handling category explained below. |
| `source_id`, `source_url`, `source_locator` | Public source and a reproducible location within it. |
| `source_publication_date` | Publication date, not `first_seen`. |
| `collected_on` | Date this project transcribed the record. |
| `first_seen` | `not established` for every record; no first-observation time inferred. |
| `current_status` | `not assessed` for every record. |
| `to_ids` | `false` for every record; nothing is approved for automatic detection/blocking. This is a project handling flag, not an assertion that a MISP event already exists. |
| `context` | File-layer, platform, and other interpretation constraints. |

**Handling categories:** `historical_ioc_candidate` marks five hashes and three network observations for later assessment. `historical_repository_context` identifies two historically reported distribution locations. `package_context` and `file_path_context` are explanatory, not unique indicators of a malicious instance.

The wildcard `*.h4ck[.]cfd` is deliberately not normalized to a single hostname. `PYTHON_SITE_PACKAGES` is a placeholder used by the source, not the directory of a computer inspected by this project. Source repository identifiers are stored as strings and are not visited by the supplied scripts.

## 5. Published measurements — `data/published_metrics.csv`

Eight rows transcribed from **Table 2** of Fogel et al., `arXiv:2602.04653v4`. Seven rows describe model families; the last is the paper's Average row.

`clean_accuracy_C00` and `triggered_accuracy_C11` are proportions in the paper's integrity-violation experiment. `benign_deviation_magnitude` stores the nonnegative magnitude shown with ± in the source. It is not a standard error or confidence interval. None of these columns is the attack-success-rate metric displayed in Figure 3.

The CSV repeats the source URL, table locator, owner of the measurements, and collection date. Do not recalculate or silently replace the published Average row. Experimental labels C00/C01/C10/C11 belong to the paper and are not project case IDs.

## 6. Figures and collection evidence

`images/manifest.json` records five original figure URLs, authorship, captions, licences, alteration status, and the actual delivery method. `local_binary_included = false` describes the initial delivered package. The optional downloader writes a separate download receipt if it is later run successfully.

`evidence/collection_log.csv` records research activities without invented clock times. `evidence/validation.txt` records the local structural checks; it is not a security scan result.

Source links and the bibliography are in the [main report](../README.md#11-references).
