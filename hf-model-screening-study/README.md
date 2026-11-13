# HF Model Screening Study

**Status:** research design and metadata-collection starter. No model safety results yet.

## Research question

With the same inference budget and no knowledge of the planted trigger, how do word-only and mixed-word tests differ in detecting backdoored pretrained text classifiers?

We distinguish **file/code safety**, **ordinary model accuracy**, and **trigger-conditional model behavior**. A clean file scan is not a certificate of safe learned behavior.

## Proposed contribution

A replication-plus-extension measuring detection, false alarms and cost under a frozen, clean-only-calibrated, unknown-trigger screening protocol. We do not claim the first model repository audit or the first backdoor detector. Read the [protocol](docs/protocol.md) and the [novelty check](docs/novelty_check.md).

## Current contents

- [Comparative review of all 20 supplied papers](docs/literature_matrix.md), with corrected titles, scope and version notes.
- [Proposed experiment](docs/protocol.md): controlled clean/backdoored checkpoints, independent splits and evaluation budgets.
- `scripts/collect_metadata.py`: public metadata inventory only; no weight download or model execution.
- `tests/test_collect_metadata.py`: eight offline tests with constructed API responses.
- [Today's checklist in Russian](START_HERE_RU.md).

## Run the metadata pilot

Python 3.10 or newer is recommended for this starter. From the repository root:

```bash
python -m venv .venv
# Windows: use .venv\Scripts\python.exe in the commands below.
# Linux/macOS: use .venv/bin/python instead.
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/collect_metadata.py --limit 10
```

The generic `python` commands above use your current interpreter. To use the virtual environment without activating it on Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/collect_metadata.py --limit 10
```

Output is saved under a new timestamped directory in `data/`: selection, metadata JSONL, errors, environment/status and a short Markdown pilot report. Explicit repositories may be supplied with repeated `--repo-id` options.

The default ten-model inventory is a convenience sample of public ungated text-classification repositories ordered by downloads. It only tests the collection pipeline. It is **not** the labeled experimental benchmark and does not estimate the prevalence of unsafe models.

## Data interpretation

`backdoor_label=unknown`, `scan_status=not_run` and `behavior_test_status=not_run` are intentional. `.bin` is a format hint, not confirmed pickle or malware. Python files do not prove custom code is required. Missing fields remain unknown. Download counters are not unique users or measurements of client verification.

## What has actually been tested

Eight offline unit tests pass in the preparation environment. API signatures were checked against installed `huggingface_hub==1.16.1`. Live collection could not be validated there because DNS/network access failed. No live metadata dataset, scanned checkpoints, trained backdoors, behavioral scores or attack-success measurements are included. Run the collector in your own networked environment and retain errors rather than inventing missing records.

## Planned next milestone

Build or obtain a documented, licensed clean/backdoored classifier pair in an isolated lab. Verify clean task accuracy and curator-only trigger behavior. Implement the frozen unknown-trigger screen separately. Do not replace this milestone with a large unlabelled repository scan.

## Safety and reproducibility

No credentials, complete paper PDFs, executable malware or model weights belong in this repository. The starter never loads repository code or serialized weights. Record revisions, hashes, licenses, package versions and seeds for later experiments. A third-party model's public availability does not establish that it is safe or that its weights may be redistributed.

## Tool references

- [Hugging Face HfApi client](https://huggingface.co/docs/huggingface_hub/package_reference/hf_api)
- [Hub download statistics](https://huggingface.co/docs/hub/models-download-stats)
- [Hub pickle scanning](https://huggingface.co/docs/hub/security-pickle)
- [Bandit scope](https://bandit.readthedocs.io/en/latest/)
