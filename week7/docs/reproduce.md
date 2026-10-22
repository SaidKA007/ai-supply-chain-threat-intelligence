# Reproduce the recorded endpoint experiment

Run on your own authorised Windows machine. The simulation needs Python's
standard library only. It does not install packages, read private files, download
models, or make network connections. Velociraptor itself communicates with its
local server.

## 1. Start the same lab environment

The recorded executable was at the root of drive D, not inside `D:\Velociraptor`.
In local **PowerShell**, the command was:

```powershell
& "D:\velociraptor-v0.77.3-windows-amd64.exe" gui
```

Use the actual location of your installed executable. This is the observed version,
not a claim that it is the latest available release. Keep that terminal running.
Local GUI mode is documented in [S07](sources.md#s07).

The recorded GUI address was `https://127.0.0.1:8889/`. Use the address printed by
your own process. A locally generated certificate may not be trusted by the browser;
verify that it is your own loopback service before proceeding. Do not expose the
lab interface to the internet or disable certificate checking globally.

The initial frontend could not bind to port 8000. The student's PowerShell output
identified `splunkd` as its listener. The successful recovery stopped that local
Splunk installation using its normal stop command and then restarted Velociraptor.
Do not stop unrelated programs or security services. This report does not assume
Splunk's startup type was changed or that it collected personal Windows logs.
The shortened failed-start evidence is in
[`startup_excerpt_redacted.txt`](../evidence/startup_excerpt_redacted.txt).

Select the connected Windows client. For the baseline, run
`Collected → + → Windows.System.Pslist → Configure Parameters → Specify Resources → Review → Launch`.
The preserved run returned 254 rows. Your process count will differ.

## 2. Put the lab script in place

From the repository root, in **PowerShell**:

```powershell
New-Item -ItemType Directory -Force "D:\Week7_Lab" | Out-Null
Copy-Item ".\week7\simulation\ai_model_loader.py" "D:\Week7_Lab\ai_model_loader.py"
python --version
```

The `New-Item` command is PowerShell syntax. Do not paste PowerShell commands into
a prompt that begins `C:\...>` (cmd). Neither prompt text nor an error trace is
part of a command to copy.

The supplied Python file is a faithful source transcription of E04, not a new
hardened loader. The harmless child command is fixed. Run it interactively so
Windows `timeout` can wait normally. [S10–S12](sources.md#s10)

## 3. Observe the positive behaviour

In your **local terminal**, run:

```powershell
python D:\Week7_Lab\ai_model_loader.py
```

While its 120-second wait is active, open the **selected client → Shell** in
Velociraptor. Change the execution-language dropdown from `Powershell` to **VQL**.
Paste only `queries/04_python_cmd_detection.vql` into the top editor and launch it.

The parent and child must still exist when the query runs. `subprocess.run()`
waits for the child; after it exits, this script also ends. If the wait has ended,
run the same script again rather than searching its old PID.

Open the corresponding **Generic.Client.VQL** result. Compare its displayed
query and result with the query you launched. Refresh the UI if necessary. Empty
results in an older session are not proof that the new query failed.

A matching row should show cmd.exe and a Python parent, with `Ppid` equal to the
parent's `Pid`. New PIDs are normal. Capture the query and returned row, including
the Parent.Name and command line. Do not force the historical PIDs from this report.

The exploratory query `02_python_cmd_inventory.vql` can be used first to view
both processes; it is not the final parent-specific detector.

## 4. Run the negative control

Let the Python test end and check that its child cmd has exited. Open a local
**cmd.exe** prompt, then enter:

```cmd
cmd.exe /k echo WEEK7_BENIGN_CONTROL
```

This reproduces the supplied control's **cmd → cmd** immediate relationship.
Leave the child open. In **Velociraptor → Shell → VQL**, run:

1. `03_cmd_parent_context.vql`: confirm the labelled control is present and its
   parent is not Python.
2. `05_negative_test_detection.vql`: apply the same Python-parent predicate used
   for the positive test, with fewer displayed columns.

The control should be excluded. Other genuine Python-to-cmd activity on your
machine could still produce results; examine those rows rather than deleting them.
An empty view without the preceding existence check is not a sufficient negative test.

## 5. Preserve and stop

Keep screenshots of the positive detection, broad negative context, and final
negative filter. Where possible, also export the matching collection results
from **Collected → Results** using the CSV/export control; save the query and
run time alongside the export. The supplied report did not receive these raw
exports, so its CSV files remain labelled transcriptions.

Enter `exit` in each lab cmd shell that you opened. Stop the local Velociraptor
GUI process with Ctrl+C when finished, after exporting needed evidence. Do not
publish datastore directories, server/client configs, private keys or API credentials.

## Common UI issues in the recorded run

| Symptom | Explanation / check |
|---|---|
| PowerShell parser errors on `SELECT` | VQL was sent to the wrong language mode. Select VQL and launch a new query. |
| A binocular-like button opens raw JSON | It is a result-inspection control, not a process search box. Use the VQL WHERE clause. |
| Old query text below a new editor | The visible session is not necessarily the newest result. Check the result's own query text. |
| No Python-to-cmd match | Verify the script is still running and the parent/child both exist. A snapshot is not historical telemetry. |
| Control's parent is cmd rather than PowerShell | It was started inside an existing cmd. Record the actual parent; this is still a valid non-Python control. |

This repeat procedure does not configure continuous event monitoring, scheduled
alerts, a custom imported artifact, or a SIEM. Those would be new work.
