# Week 6 — sources and provenance

**Review date:** 19 October 2026. Official live pages were read during preparation. Their contents may change; no full web snapshot, complete ATT&CK release, or external binary was bundled.

## Official references

| ID | Primary source | Used for |
|---|---|---|
| W6-S01 | [MITRE ATT&CK — T1059.006](https://attack.mitre.org/techniques/T1059/006/) | Python sub-technique, Execution association, and record metadata. Reviewed version 1.1; modified 12 May 2026. |
| W6-S02 | [MITRE ATT&CK — T1059](https://attack.mitre.org/techniques/T1059/) | Current parent-technique title and hierarchy. |
| W6-S03 | [MITRE ATT&CK — TA0002](https://attack.mitre.org/tactics/TA0002/) | Execution tactic. |
| W6-S04 | [Python — `pickle`](https://docs.python.org/3/library/pickle.html) | Security warning and the reduction/callable mechanism. Consult the Warning and `object.__reduce__()` sections. |
| W6-S05 | [MITRE ATT&CK Navigator — usage](https://github.com/mitre-attack/attack-navigator/blob/master/USAGE.md) | Saving and Loading Layers, specifically local layer import. |
| W6-S06 | [MITRE — layer format 4.5](https://github.com/mitre-attack/attack-navigator/blob/master/layers/spec/v4.5/layerformat.md) | JSON property types, required version properties, technique entries, and layout options. |
| W6-S07 | [MITRE Navigator — releases](https://github.com/mitre-attack/attack-navigator/releases) | Published Navigator 5.3.2 used as the layer compatibility target, not an installed-version claim. |
| W6-S08 | [Python — `json`](https://docs.python.org/3/library/json.html) | The data-only parser used for the toy policy comparison. |
| W6-S09 | [MITRE ATT&CK — T1195](https://attack.mitre.org/techniques/T1195/) | Supply-chain context; not an executed technique in Week 6. |
| W6-S10 | [Python — `pickletools`](https://docs.python.org/3/library/pickletools.html) | Non-executing disassembly of the locally generated fixture. |

The inspected Python documentation was served as version 3.15.0 documentation. The tested interpreter was **CPython 3.13.5**; these are not the same version. The lab uses established standard-library interfaces and pins fixture serialization to protocol 2. No claim of testing on Python 3.15, Windows, or macOS is made.

The Navigator JSON targets layer format 4.5. Its `versions.navigator` is a compatibility target, not a record of a browser session. The optional `versions.attack` is omitted; the importing instance supplies its default dataset. The technique record reviewed on the date above is documented separately. Structural checks are not a substitute for a captured UI import.

## Project context, not independent incident evidence

| ID | Material | Relevance and boundary |
|---|---|---|
| W6-P01 | [Week 4 README](../../week4/README.md) | Existing C01 analysis and its unsafe-processing distinction; motivates this mechanism test. No historical payload or event was replayed. |
| W6-P02 | [Week 5 README](../../week5/README.md) | Existing synthetic-event hunt; its required observations are compared conceptually with this experiment. No Splunk query was executed for Week 6. |

Those pages were read from the public `SaidKA007/ai-supply-chain-threat-intelligence` repository. Preparation added a new standalone weekly folder; it did not alter the remote repository or earlier evidence.

## New local evidence

| ID | Files | Meaning |
|---|---|---|
| W6-L01 | [Reference run](reference_run/summary.json), [events](reference_run/events.jsonl), [results](reference_run/results.csv), and [markers](reference_run/markers/S02.txt) | Actual benign execution in the assistant verification environment. Events come from explicit statements in the test application, not independent endpoint sensors. S03 has its own marker in the same directory. |
| W6-L02 | [Test output](test_results.txt) | Actual output of 15 passing regression tests, executed against a separate temporary run. This is not a production detection benchmark. |
| W6-L03 | [Mapping CSV](../data/attack_mapping.csv) and [Navigator layer](../navigator/week6_layer.json) | Project-authored interpretation of the reference run. These are not MITRE-published incident mappings. |
| W6-L04 | [Source code](../simulation/run_lab.py), [callback](../simulation/lab_helpers.py), and [tests](../tests/test_lab.py) | Reproducible implementation. Source hashes are recorded in the reference metadata. |

Fixtures are constructed in memory from the packaged code. `fixtures.json` stores hashes and lengths; `callback_disassembly.txt` stores a readable instruction listing. The package includes no downloaded malicious models or serialized binary samples. Marker contents, run IDs, and timestamps come from execution; they are not images of a simulated interface.

## Integrity and attribution

`../SHA256SUMS.txt` hashes the packaged files, excluding itself. The hashes describe package content and teaching fixtures, not an IOC feed. Runtime outputs in a later `runs/` directory are outside that initial manifest.

Framework names and identifiers are attributed to MITRE, and library behavior to Python's official documentation. External sources are linked rather than redistributed in full. No third-party screenshots, vendor logos, model weights, or source-code excerpts were copied into Week 6. Existing repository-level notices remain unchanged.

Generative AI assisted in preparing the implementation and documentation. The source-based statements, local execution evidence, interpretation, and proposed future work are identified separately throughout the README.
