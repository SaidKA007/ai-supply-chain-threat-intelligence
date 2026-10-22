# Sources and verification

Official pages were checked during packaging on **22 October 2026**. They explain
frameworks and software behaviour; they are not evidence that the student's
experiment ran. The primary experimental sources are [E00–E10](../evidence/README.md).
The pages are linked, not fully archived. The installed versions are taken from
the submitted material, not inferred from the versions of current documentation.

## S01
**MITRE CAR — CAR-2013-02-003: Processes Spawning cmd.exe**  
https://car.mitre.org/analytics/CAR-2013-02-003/

Used to select the analytic and verify its Windows/process scope, situational
awareness category, process-create data model, and related ATT&CK entry. Its
published pseudocode is broader than this lab's Python-only refinement.

## S02
**MITRE ATT&CK — T1059.003: Windows Command Shell**  
https://attack.mitre.org/techniques/T1059/003/

Primary technique reference for the controlled cmd execution. The page associates
it with Execution. The lab does not inherit the page's listed threat actors or
procedure examples.

## S03
**MITRE ATT&CK — T1059.006: Python**  
https://attack.mitre.org/techniques/T1059/006/

Used only for the Python execution context. A Python process is not automatically
malicious, and this report does not claim broad Python-threat detection.

## S04
**Velociraptor — pslist**  
https://docs.velociraptor.app/vql_reference/popular/pslist/

Documents live-process enumeration and the optional `pid` argument.

## S05
**Velociraptor — Windows.System.Pslist**  
https://docs.velociraptor.app/artifact_references/pages/windows.system.pslist/

Reference for the initial built-in collection and its output/filter parameters.

## S06
**Velociraptor — VQL Fundamentals**  
https://docs.velociraptor.app/docs/vql/fundamentals/

Reference for SELECT/FROM/WHERE, named plugin arguments, regex strings, column
expressions, and subqueries. The submitted screenshots provide the direct
execution evidence for our specific query.

## S07
**Velociraptor — Deployment Overview**  
https://docs.velociraptor.app/docs/deployment/

Reference for local GUI deployment and the difference between client, frontend,
and GUI. It is not a production-deployment security review of this lab.

## S08
**Velociraptor — Client Shell Commands**  
https://docs.velociraptor.app/docs/clients/shell/

Reference for running ad-hoc VQL on the selected client via the Shell page and
its artifact-backed workflow. The execution language selector matters.

## S09
**Velociraptor — What is Velociraptor?**  
https://docs.velociraptor.app/docs/overview/

Reference for describing Velociraptor as an endpoint monitoring, forensic and
response platform, rather than claiming a completed SIEM implementation.

## S10
**Microsoft Learn — cmd**  
https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd

Reference for `/c` (run then exit) and `/k` (run and remain open).

## S11
**Microsoft Learn — timeout**  
https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/timeout

Reference for the visible `timeout /t 120 /nobreak` lab command.

## S12
**Python 3.13 documentation — subprocess**  
https://docs.python.org/3.13/library/subprocess.html

Reference for `subprocess.run()`, including waiting for the child command to
complete. The test source itself is transcribed from E04.
