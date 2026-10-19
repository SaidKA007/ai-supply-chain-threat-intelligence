# Week 6 — ATT&CK Framework
## Python execution during model deserialization

**Project:** Detection and Threat Intelligence Analysis of AI Supply Chain Threats Using MITRE ATLAS  
**Course:** Introduction to Threat Hunting · Astana IT University · 2026–2027  
**Focus:** Tactics, techniques, procedures, and one controlled execution experiment  
**Selected sub-technique:** **T1059.006 — Command and Scripting Interpreter: Python**  
**Prepared:** 19 October 2026

> **Result:** Four benign scenarios were executed in a verification environment. The run produced **24 application events and two marker files**. Both callback scenarios support an emulation mapping to **Execution / T1059.006**. All four scenario checks and 15 automated regression tests passed. These are local teaching results, not confirmed attacks or a detection-accuracy measurement.

[Experiment](#3-experiment-design) · [Results](#4-executed-results) · [ATT&CK mapping](#5-map-the-results-to-attck) · [Run the lab](#7-reproduce-the-experiment) · [Navigator](#8-attck-navigator-layer) · [Sources](evidence/sources.md)

## 1. Objective and project continuity

**Question:** Can processing a controlled model-like object execute Python code, what evidence records that action, and which ATT&CK mapping is justified?

[Week 4](../week4/README.md) examined C01 / `AML.CS0031`, including the distinction between a published model archive and unsafe processing of its extracted Pickle content. [Week 5](../week5/README.md) searched synthetic model, child-process, and network events in Splunk. Week 6 moves from source analysis and authored log records to a **small, actually executed, benign mechanism test**. It does not reconstruct the historical incident or rerun Week 5's searches.

| Week 6 requirement | Deliverable |
|---|---|
| Study tactics, techniques, and procedures | Section 2 and the selected Python sub-technique |
| Simulate an attack and map the results | Four safe scenarios, recorded events, physical marker files, and the mapping CSV |
| Use the recommended Navigator documentation | A documented layer file and import instructions |

## 2. Tactics, techniques, and procedures

A **tactic** describes the adversary's objective; a **technique** describes how it is pursued; a **procedure** is a concrete implementation. In this exercise, the procedure is a harmless stand-in for an execution behavior, not an actual adversarial operation.

| Level | Selection | Meaning in this lab |
|---|---|---|
| Tactic | **TA0002 — Execution** | The objective being emulated is running code. [W6-S03] |
| Parent technique | **T1059 — Command and Scripting Interpreter** | The broader interpreter-execution category. [W6-S02] |
| Sub-technique | **T1059.006 — Python** | The chosen Python execution behavior. [W6-S01] |
| Procedure | A controlled Pickle object invokes `lab_helpers.write_marker()` during loading | The callback creates one harmless text file in the run directory. |

The syllabus calls T1059 “Command-Line Interface.” Its current official title is **Command and Scripting Interpreter**. This increment studies its more specific Python sub-technique. The reviewed T1059.006 page reports record version **1.1**, last modified **12 May 2026**. That is a technique-record version, not an ATT&CK release number. [W6-S01], [W6-S02]

**A Python process is not automatically malicious.** S01 is a normal-operation control. The mapping concerns the extra callback intentionally introduced into S02 and S03. It is our documented emulation mapping, not a MITRE verdict on these files.

## 3. Experiment design

### Local mechanism

The lab builds its own tiny fixtures in memory. A “model” here is a dictionary with a name and three numbers; no trained model, PyTorch installation, model registry, or inference service is used.

`CallbackFixture.__reduce__()` specifies the fixed callback while the object is serialized. Later, `pickle.loads()` invokes that callback while restoring the object. The runner does not directly call the marker function. The distinction between building the fixture and triggering it is visible in the [source](simulation/lab_helpers.py) and the [generated disassembly](evidence/reference_run/callback_disassembly.txt). Python documents why untrusted Pickle data must not be loaded. [W6-S04]

For S03, the fixture is serialized with protocol 2 and its final `STOP` opcode is removed. This deliberately creates a late `EOFError` after the callback. It is a toy failure condition, **not a reproduction of C01's archive format or a vendor vulnerability**.

### Comparison cases

| Scenario | Input and handling | Question |
|---|---|---|
| **S01 — Baseline** | Load a locally created plain dictionary from Pickle. | Does normal restoration avoid the added callback? |
| **S02 — Callback** | Load a locally created object containing the fixed callback reference. | Does the callback run during loading? |
| **S03 — Callback and error** | Load the callback fixture after removing its final opcode. | Can the callback run before the loader reports failure? |
| **S04 — Format policy** | Reject the **same candidate bytes as S02** before unpickling, then load separate permitted JSON metadata. | Can this format gate prevent the callback while allowing the intended toy data? |

S04 rejects the entire Pickle format; it does **not** detect maliciousness or convert the candidate into JSON. Its accepted JSON is a separate, locally authored fixture. JSON parsing has a 4 KiB limit and checks the expected toy data. This is a narrow demonstration, not a universal AI-model loader or a production security control. [W6-S08]

### Safety boundary

The supplied source performs **no network operation, shell invocation, subprocess launch, credential access, or persistence setup**. The callback only creates a new marker under its run folder. No serialized binary payload is distributed in this increment, and the command-line tool has no arbitrary input-file or target option.

Use an ordinary account and read the code before running it. The experiment is intentionally limited, **not a sandbox for unknown files**. Do not replace the fixtures with downloaded models or untrusted Pickle data.

## 4. Executed results

The bundled reference run was executed during package preparation in the **assistant verification environment**, not on the student's computer.

| Run property | Recorded value |
|---|---|
| Run ID | `W6-3c1d674e56a4` |
| Started, UTC | `2026-10-19T10:51:38.543032Z` |
| Environment | `Linux`, `CPython 3.13.5` |
| Evidence source | Custom application instrumentation plus the created marker files |
| Scenarios / passed expectations | `4 / 4` |
| Application events / marker files | `24 / 2` |

| Scenario | Observed outcome | Callback count | Marker | Interpretation |
|---|---|---:|---|---|
| S01 | Loaded successfully | 0 | No | Baseline passed. |
| S02 | Loaded successfully | 1 | [S02.txt](evidence/reference_run/markers/S02.txt) | The controlled callback executed. |
| S03 | `EOFError` | 1 | [S03.txt](evidence/reference_run/markers/S03.txt) | Execution preceded the loading error. |
| S04 | Pickle blocked; separate JSON loaded | 0 | No | The tested format gate avoided unpickling. |

**Primary local evidence:** [console output](evidence/reference_run/console.txt), [result table](evidence/reference_run/results.csv), [run metadata](evidence/reference_run/summary.json), [event stream](evidence/reference_run/events.jsonl), and [CSV representation](evidence/reference_run/events.csv).

### What the events establish

S02 contains `pickle_load_start`, `python_callback`, `marker_created`, and `pickle_load_success`, in that order. S03 records the same callback and marker before `pickle_load_error`. The actual text files provide an additional check of the intended side effect. S04 has `policy_reject` and JSON-load events, but no Pickle-load or callback event.

The scenario design is authored; the timestamps, process IDs, callback events, and marker files were produced during execution. These are **application-written records**, not Sysmon, EDR, packet-capture, or victim logs. A `run_id` together with `scenario_id` separates cases; all four run in one Python process. Each event also has an ordered sequence and monotonic elapsed time.

The [fixture manifest](evidence/reference_run/fixtures.json) records byte lengths and SHA-256 hashes. S02 and S04 use the same candidate hash. These hashes identify teaching fixtures, **not malware IOCs**. Source-file hashes in `summary.json` identify the code used for this reference run.

The [test log](evidence/test_results.txt) records **15 passing regression tests** from a separate temporary run. The tests check ordering, error-after-callback behavior, format rejection, actual markers, matching CSV/JSON representations, and refusal to overwrite an existing output folder. They do not estimate detection precision or recall.

## 5. Map the results to ATT&CK

The full evidence-linked assessment is in [`data/attack_mapping.csv`](data/attack_mapping.csv). Both rows use **TA0002 / T1059.006**, but describe different tested procedures.

| Mapping | Scenario | Evidence in the reference event stream | Assessment |
|---|---|---|---|
| W6-M01 | S02 | `W6-E00008`–`W6-E00011`, plus `markers/S02.txt` | Benign emulation of Python execution during loading. |
| W6-M02 | S03 | `W6-E00014`–`W6-E00017`, plus `markers/S03.txt` | The same execution behavior occurs before a loading error. |

This is **one distinct sub-technique**, not two attacks or two separate techniques. Parent T1059 is a reference category and is not counted again. The official Python definition and Execution tactic support the analyst-selected correspondence. [W6-S01], [W6-S03]

### Boundaries of the mapping

| Item | Why it is not an additional observed attack mapping |
|---|---|
| Baseline S01 and policy case S04 | Normal loading and a control test are not adversary activity. |
| Supply Chain Compromise, T1195 | It remains project context. No repository, supplier, delivery channel, or consumer environment was compromised in this lab. [W6-S09] |
| Shell execution | The payload does not launch a shell. Running the lab from a terminal is setup, not an emulated attacker procedure. |
| Persistence, C2, or exfiltration | A marker is not an autostart mechanism. No callback connection, remote control, or data transfer is implemented. |

## 6. Findings and relation to threat hunting

**First, loading can include an execution step.** In S02, the callback ran inside the existing Python process. A separate shell was not required in this implementation.

**Second, a loading error does not undo an earlier side effect.** S03 left a marker even though restoration failed. Reviewing only the final error would miss the preceding action in this run.

**Third, a narrow format policy prevented the tested action.** S04 rejected the same candidate before reaching Pickle, while accepting separate data-only metadata. This demonstrates the tested code path, not scanner effectiveness against unknown samples.

**Connection to Week 5:** its executed correlation required a command-process child and network activity. Neither feature is part of this Week 6 implementation. Therefore that specific three-observation condition does not describe this in-process path. This is a comparison of requirements, **not a measured false negative, a new Splunk run, or a recall calculation**.

A future hunt could combine model-loading instrumentation with independently collected process and file telemetry, retaining artifact and load-session identifiers. It would also need normal workloads for comparison. The known marker name is useful for this test only; it is not a production threat signature. This extension is proposed, not implemented here.

## 7. Reproduce the experiment

**Requirements:** Python 3.10 or newer. The code uses the standard library only, so there is no `pip install` step. The supplied verification was on Linux with Python 3.13.5; Windows and macOS execution was not separately verified.

From the **repository root**:

```bash
python week6/simulation/run_lab.py
```

On Windows, `py -3` can be used in place of `python` when that launcher is installed. On Linux, use `python3` when that is the available command.

Each run creates a **new** directory under `week6/runs/`. The terminal prints its full location. The reference evidence is not overwritten, and `runs/` is excluded by the supplied `.gitignore`. To choose a new output location explicitly:

```bash
python week6/simulation/run_lab.py --output week6/runs/my_run_01
```

An existing output directory is refused. Choose another name rather than deleting an earlier run.

Run the regression tests separately:

```bash
python -m unittest discover -s week6/tests -v
```

Expected scenario checks are S01 loaded without a marker; S02 loaded with a marker; S03 `EOFError` with a marker; S04 Pickle rejected and JSON accepted without a marker. An expected S03 error counts as a passed scenario check. The runner exits with a nonzero status for a failed scenario or execution error.

For your own submission evidence, capture the terminal after an actual local run and show the resulting S02/S03 marker files. Keep the new run's provenance separate from the bundled reference run. Detailed Russian steps are in [the run guide](docs/run_guide_ru.md).

## 8. ATT&CK Navigator layer

[`navigator/week6_layer.json`](navigator/week6_layer.json) highlights **only T1059.006 under Execution**. Its comment identifies S02/S03 and the evidence boundary. No numeric risk or coverage score is assigned.

Open the [official Navigator](https://mitre-attack.github.io/attack-navigator/), create a new tab, choose **Open Existing Layer**, then **Upload from local**, and select this JSON. The documented interface supports loading saved local layers. [W6-S05]

The file follows layer format **4.5** and targets Navigator **5.3.2** compatibility. The optional ATT&CK release field is omitted, so the importer uses its default dataset; check that T1059.006 remains under Execution when importing. The layer's metadata records the reviewed technique version and reference run. [W6-S06], [W6-S07]

**Validation boundary:** the JSON and selected fields were checked locally. A browser import/export was not performed or captured in the bundled evidence. A saved Navigator screenshot would document your own import, not another attack execution.

## 9. Files and repository integration

```text
week6/
    README.md
    .gitignore
    .gitattributes
    SHA256SUMS.txt
    simulation/
        run_lab.py
        lab_helpers.py
    tests/
        test_lab.py
    data/
        attack_mapping.csv
    navigator/
        week6_layer.json
    docs/
        run_guide_ru.md
        defense_notes.md
        root_readme_update.md
    evidence/
        sources.md
        test_results.txt
        reference_run/
            console.txt
            summary.json
            results.csv
            events.jsonl
            events.csv
            fixtures.json
            callback_disassembly.txt
            markers/
                S02.txt
                S03.txt
```

Add the whole `week6` directory beside `week1`–`week5`; do not flatten it. No previous dataset or weekly folder needs changing. [Suggested root README additions](docs/root_readme_update.md) are provided separately rather than replacing the project's existing introduction.

`SHA256SUMS.txt` covers the packaged Week 6 files except itself. It identifies this package version, not malicious content. New runs are intentionally not covered by that initial manifest. The local attributes keep text files in LF format for stable checksums.

## 10. Limitations, sources, and assistance

This is a small mechanism demonstration using a fixed, benign callable. It does not include real models, historical payloads, platform scanner tests, supplier compromise, independent endpoint monitoring, or deployment testing. It cannot establish the prevalence of a threat or the effectiveness of a production defense. JSON is used for the toy metadata, not presented as a replacement for every model format.

**AI assistance and execution provenance:** generative AI assisted with the code, test design, ATT&CK comparison, and documentation. The bundled reference run and automated tests were executed in the assistant's verification environment. No student-local execution, third-party screenshot, or independent malicious-sample analysis is claimed. Review the code and sources and run the exercise locally before presenting a personal execution demonstration.

The full [source register](evidence/sources.md) separates official framework documentation, previous project context, and newly generated local evidence. External material is linked and paraphrased, not redistributed in full.

[W6-S01]: https://attack.mitre.org/techniques/T1059/006/
[W6-S02]: https://attack.mitre.org/techniques/T1059/
[W6-S03]: https://attack.mitre.org/tactics/TA0002/
[W6-S04]: https://docs.python.org/3/library/pickle.html
[W6-S05]: https://github.com/mitre-attack/attack-navigator/blob/master/USAGE.md
[W6-S06]: https://github.com/mitre-attack/attack-navigator/blob/master/layers/spec/v4.5/layerformat.md
[W6-S07]: https://github.com/mitre-attack/attack-navigator/releases
[W6-S08]: https://docs.python.org/3/library/json.html
[W6-S09]: https://attack.mitre.org/techniques/T1195/
