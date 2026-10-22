# VQL queries used in Week 7

Use these in the **selected Windows client → Shell → VQL**, not in the
PowerShell command field and not in a server notebook. Run one file at a time.
The client-shell workflow is described in [S08](../docs/sources.md#s08).

| File | Purpose | Evidence |
|---|---|---|
| `01_cmd_inventory.vql` | Initial broad discovery of live cmd processes | Initial cmd capture in the conversation; the detailed lab continues with the files below |
| `02_python_cmd_inventory.vql` | Show Python and cmd together | [E06](../images/06_process_chain.png) |
| `03_cmd_parent_context.vql` | Show all live cmd instances with parent context | [E09](../images/09_negative_parent_context.png) |
| `04_python_cmd_detection.vql` | Python-parent predicate with executable paths included | [E07](../images/07_positive_detection.png) |
| `05_negative_test_detection.vql` | Same predicate, fewer output columns | [E10](../images/10_negative_no_match.png) |

These files are transcriptions of the queries shown in the conversation and
screenshots, not exports downloaded from the endpoint. Whitespace is normalized;
selection and filtering logic is retained.

## Do not confuse output columns with detection logic

The positive screenshot includes `Exe` in both the main and parent selections.
The negative screenshot omits those two `Exe` columns. Both use these exact
conditions:

```sql
WHERE Name =~ "(?i)^cmd\\.exe$"
  AND Parent.Name =~ "(?i)^python(\\.exe|w\\.exe)?$"
```

The double backslash is intentionally preserved in the VQL string. Do not copy
the query into a Python string and add another escaping layer.

The original parent pattern also accepts the bare name `python`, as well as
`python.exe` and `pythonw.exe`. Only `python.exe` was tested in the recorded run.
It does not cover every possible interpreter name. The earlier discovery regexes
in files 01–02 are less strict (unanchored and with an unescaped dot); they are
retained as historical exploration queries, not recommended final matching logic.

The word `WEEK7_CAR_TEST` is useful for recognising the lab command. It is **not**
a condition in the detector. A legitimate Python script launching cmd can also
match. No command-line allowlist, signature verification, PID-reuse validation,
or process-start event subscription is added silently.

The displayed positive result establishes that `Parent.Name` worked in the
student's run. Earlier empty screens are not sufficient evidence that the nested
query syntax was broken. No special rewrite is required to reproduce the saved
successful query.
