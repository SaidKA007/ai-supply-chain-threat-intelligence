# Evidence register and run consistency

## Original material

The supplied notebook, model checkpoints and results CSV are copied byte-for-byte into this package. Renaming the checkpoints from `clean_model(1).pth` and `backdoored_model(1).pth` removes the browser download suffix only; it does not modify their contents.

`notebook_outputs.txt` extracts saved stream outputs and labels them by notebook cell position. It was not produced by executing the notebook again. `cell_inventory.csv` records source hashes and execution counters for inspection. Notebook cell numbers in this report count from 1.

## Which baseline is used?

| Material | Clean training losses | Clean accuracy | Treatment |
|---|---|---:|---|
| Earlier conversation screenshots | 1.5948, 1.1898, 0.9972, 0.8695, 0.7601 | 70.91% | Retained only in `images/archive/`. |
| Uploaded notebook, cells 9–10 | 1.5852, 1.2038, 1.0104, 0.8794, 0.7852 | 71.69% | Primary retained baseline. |
| Uploaded notebook, cell 14 | Combined evaluation | 71.69% | Agrees with the retained baseline evaluation. |
| Uploaded CSV and export screenshot | Values typed into an export table | 71.69% | Matches the evaluated output, but is not an independent measurement. |

The saved notebook contains a later baseline-training output than the early screenshot. It therefore supports treating these as different training outputs, rather than calling the difference rounding or measurement noise. The precise sequence of runtime resets is not independently logged. The report does not infer that the early weights were reused.

## Images and captions

| Packaged file | Source | Evidence status |
|---|---|---|
| `images/figures/01_dataset.png` | Embedded PNG, notebook cell 5 | Extracted original figure, full size. |
| `images/figures/02_red_x_trigger.png` | Embedded PNG, cell 11 | Extracted original figure. |
| `images/figures/03_selected_success.png` | Embedded PNG, cell 18 | Extracted original figure; deliberately selected success. |
| `images/screenshots/01_dataset_download.png` | Student screenshot | Supporting dataset-loading capture from the conversation. |
| `images/screenshots/02_colab_gpu.png` | Student screenshot | Supporting GPU capture; display is partly covered by a notification. |
| `images/screenshots/03_red_x_trigger.png` | Student screenshot | Original/triggered cat. |
| `images/screenshots/04_backdoor_training.png` | Student screenshot | Matches the retained fine-tuning output. |
| `images/screenshots/05_selected_success.png` | Student screenshot | Matching dog/airplane example. |
| `images/screenshots/06_simulated_compromise.png` | Student screenshot | Literal printed commands and local file-copy output, not a shell. |
| `images/screenshots/07_integrated_http_demo.png` | Student screenshot | Model comparison and HTTP 200 / RECEIVED. |
| `images/screenshots/08_results_export.png` | Student screenshot | Saved three-value summary, not the evaluation loop itself. |
| `images/charts/*` | Packaging-time chart generation | Derived from original CSV or saved training outputs, not screenshots. |

No existing screenshot or notebook output image was redrawn or edited. The original photograph content comes from CIFAR-10. The charts are explicitly distinguished from source captures.

## Recorded and unrecorded quantities

The reported figures are 71.69%, 72.32% and 39.48%. The source did not export all per-image predictions or raw aggregate success counts. The ASR loop excludes label 0; the dataset split sizes and eligibility rule are visible, but this report does not invent a captured confusion matrix or a packet capture.

The dog softmax values (71.94% and 41.20%) appear in cell 21 and again in cell 24; the success search is in cell 18. The cat failure is cell 17. Both before/after predictions in those examples use the **backdoored** model.

No successful browser import of a Navigator layer, blocked-attack test, actual EDR alert, reverse shell or off-host transfer was supplied. Receiver JSON files from the original runtime were not uploaded. We preserve the printed standalone receiver output and integrated response rather than recreating files and calling them historical evidence.

## Packaging-time additions

The replay notebook, `src/` helpers, tests, configuration/mapping tables, charts and explanatory documents were assembled after the experiment. Their changes and checks are listed in `package_validation.md`. They do not overwrite the original evidence.

The two `.pth` files were loaded with `weights_only=True` for structural checks. This verifies compatible tensors, not the absence of a learned backdoor. No full CIFAR-10 re-evaluation or retraining was performed during packaging.
