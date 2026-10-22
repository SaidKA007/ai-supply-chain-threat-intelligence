# Evidence register and provenance

## What is primary evidence?

The primary evidence is the student's Windows/Velociraptor screenshots in
`../images/`, plus the supplied startup log excerpt. All captures came from the
conversation. No synthetic Velociraptor UI, reconstructed screenshot, or invented
live process event has been added.

| ID | File | What it supports |
|---|---|---|
| E00 | [Assignment](../images/00_assignment.png) | Wording of the Week 7 requirements |
| E01 | [Connected client](../images/01_client_connected.png) | A Windows client is connected |
| E02 | [Pslist setup](../images/02_pslist_setup.png) | Artifact selection and visible defaults |
| E03 | [Completed collection](../images/03_pslist_completed.png) | 254 returned rows; 62.73-second collection |
| E04 | [Python source](../images/04_simulation_source.png) | Actual lab script shown in Notepad |
| E05 | [Terminal run](../images/05_simulation_terminal.png) | Python version and repeated test launches |
| E06 | [Discovery chain](../images/06_process_chain.png) | Three related live process rows |
| E07 | [Positive detection](../images/07_positive_detection.png) | Filtered cmd row with a Python parent |
| E08 | [Control command](../images/08_negative_command.png) | A nested cmd control was started |
| E09 | [Control context](../images/09_negative_parent_context.png) | Both control-stage cmd instances are visible |
| E10 | [Negative filter](../images/10_negative_no_match.png) | The UI reports no data for the Python-parent query |

## Screenshot handling

The original images remain in the conversation. This package contains publication
copies. Where necessary, the browser address bar was cropped and opaque labelled
blocks were placed over the local Windows username/path, hostname, and client ID.
The remaining query text, PIDs/PPIDs, marker strings, result messages, and process
names were not rewritten. The manifest records the original filename, original
SHA-256, packaged SHA-256, crop bounds, and redaction rectangles.

The large positive capture has part of the SELECT list off-screen. The complete
query is preserved in `../queries/04_python_cmd_detection.vql` from the preceding
conversation code. The screenshot still shows its parent filter and returned row.

## What the CSV files are — and are not

`../data/observed_results.csv` is a **report table transcribed from screenshots**.
`../data/process_rows_transcribed.csv` contains **selected visible process rows**.
They are not native Velociraptor CSV/JSON exports, a complete 254-row collection,
or an independent re-run. Fields not fully visible are left blank; personal paths
are excluded. In E06, ParentName is derived from the visible PID/PPID pairs for
rows whose parents are present. In E07 and E09 it is read from the Parent object.

The negative screenshot displays `Table contains no data`, while its pagination
shows a UI placeholder rather than a clean numeric export count. We report
**no matching rows displayed**, not a verified exported total. The numeric
`reported_rows` cell is therefore blank for N02.

## Separate runs must remain separate

The discovery snapshot has Python PID 14276 and child cmd PID 20996. The later
positive detection has Python PID 3148 and child cmd PID 8600. These are repeated
runs, not contradictory IDs or one continuous process record.

The negative context capture has cmd PID 2972 under powershell PID 7984, and the
labelled benign control is cmd PID 15836 under cmd PID 2972. The immediate parent
of the labelled control is **cmd.exe**, not PowerShell.

## Execution versus packaging checks

The Windows experiment was performed by the student. This package does not claim
that Windows, Velociraptor, or its VQL engine was re-run during preparation.
`validation_report.txt` reports local file/consistency checks only.
`SHA256SUMS.txt` identifies the packaged files and excludes itself.
