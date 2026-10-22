# CAR / ATT&CK mapping and scope

## Selected analytic

**CAR-2013-02-003 — Processes Spawning cmd.exe** is the analytic reference.
Its official entry examines cmd process starts and parent context. The published
pseudocode selects cmd starts generally; it does not require a Python parent.
[Official source S01](sources.md#s01)

## Exactly what was adapted

| Dimension | CAR reference | Recorded Week 7 implementation |
|---|---|---|
| Input | Process-creation records | Live `pslist()` snapshots |
| Child | cmd.exe | cmd.exe |
| Parent context | Parent executable field | Lookup using the child's `Ppid` |
| Final scope | Broad cmd visibility | Python-parent subset |
| Platform | Windows | Student Windows 11 endpoint |
| Execution environment | Analytic can be implemented in a monitoring platform | Velociraptor client Shell / VQL |

These are explicit changes, not equivalent telemetry sources. A live query can
miss a process that exits before the query runs. The parent lookup is a second
observation, not an immutable historical parent record. PID reuse and parent exit
are not handled by this prototype. [pslist reference S04](sources.md#s04)

## Mapping decisions

| ATT&CK item | Role in this report | Evidence and boundary |
|---|---|---|
| **TA0002 — Execution** | Objective category for the emulated code execution | The student deliberately runs the lab programs; there is no victim compromise |
| **T1059 — Command and Scripting Interpreter** | Parent technique category | Organises the two sub-techniques below; not an additional detection result |
| **T1059.003 — Windows Command Shell** | Primary mapping | E04/E05 show the command; E07 shows the cmd child and Python parent |
| **T1059.006 — Python** | Supporting procedure context | E07 identifies the script's Python parent; this is not a separate detector for arbitrary Python abuse |

Technique definitions and tactics were checked against [S02](sources.md#s02)
and [S03](sources.md#s03). The project-specific mappings are our analysis of the
recorded procedure, not a MITRE endorsement or a coverage certification.

## Procedure and observable fields

**Procedure:** the student executes `ai_model_loader.py`. The script launches
cmd to print `WEEK7_CAR_TEST`, then waits in an interactive console. The detection
query selects cmd processes, resolves their parents, and retains Python parents.

**Positive evidence E07:** child PID `8600`, PPID `3148`, name `cmd.exe`;
Parent.Name `python.exe`, Parent.Pid `3148`, Parent.CommandLine ending in
`D:\Week7_Lab\ai_model_loader.py`.

The test marker does not participate in filtering. It only makes the known lab
command easier to recognise. The source does not load an AI model, unpickle a
file, open a reverse shell, or send data over a network.

## Correct interpretation of the negative control

E09 shows the labelled control as `cmd.exe → cmd.exe`; it is not a direct
PowerShell-to-cmd launch. The broad query returns that row, as it should. The
Python-only query displays no matching row in E10. Thus the negative test checks
our **narrower predicate**, not whether the original CAR analytic excludes all
benign cmd execution.

Both the positive emulation and the negative control are authorised harmless
activity. "Positive" means expected to match the chosen behaviour; it does not
mean the process was genuinely malicious. No precision, recall, F1, false-positive
rate, or overall detection-coverage percentage can be inferred from these two
manual scenarios.

## Items deliberately not claimed

No mapping is assigned for real supply-chain compromise, model poisoning,
credential theft, C2, exfiltration, persistence, or evasion: none was executed or
shown by the Week 7 evidence. The project context is AI supply-chain security,
but a filename such as `ai_model_loader.py` is not proof of a poisoned model.

The original Week 6 image classifier was not used to trigger this test. This is
a separate endpoint visibility exercise. No ATLAS mapping is needed to pretend
that model-weight manipulation occurred in this run.

## Course requirement boundary

The assignment asks for SIEM implementation. This package documents the completed
Velociraptor endpoint adaptation only. No Week 7 Splunk/Elastic execution or
instructor approval for the substitution was supplied. It is therefore not
accurate to claim full SIEM compliance. A future SIEM run would need its own
query, data, and captured result; it must not reuse these screenshots as SIEM
execution evidence.
