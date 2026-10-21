# Packaging-time validation

These checks concern the assembled package. They are not a second full training run or a new report of the student's attack-success rate.

## Checks executed

`package_checks.txt` contains the actual output of **12 passing unittest checks** run in the preparation environment with PyTorch **2.10.0+cpu**. The checks cover:

- Both supplied checkpoints load with `weights_only=True` into the exact architecture; output shape is 10 classes and test outputs are finite.
- The network has 620,362 parameters; the two supplied weight states differ.
- The replay red-X calculation matches the submitted formula exactly on the tested CPU tensor, preserves the original input and supports batches.
- The ASR-counting function excludes true target-class examples on a small artificial unit-test dataset.
- Fixed poison selection and the application gate behave as implemented.
- The packaging helper completes a new loopback HTTP round trip with the fixed fictional payload and verifies receipt hashes.

The synthetic tensors in unit tests are **test fixtures**, not the CIFAR-10 evidence or an experimental replacement for it. The port printed in `package_checks.txt` belongs to this new packaging test, not to the original Colab run. Temporary unit-test receiver files were discarded.

## Source-preservation checks

The original notebook, both supplied checkpoints and `results.csv` were compared byte-for-byte with the uploaded files. Original screenshot files were copied without edits. Three embedded PNG outputs were decoded directly from the original notebook rather than redrawn.

Source Python files were syntax-checked. Both notebooks were checked as notebook documents. Local Markdown file targets and packaged image files were checked before archiving. Links to `../week4/README.md` and `../week5/README.md` intentionally refer to the surrounding user's repository and are not copies of those weeks in this ZIP.

The final SHA-256 manifest covers packaged files except itself. `.gitattributes` prevents Git line-ending conversion inside this directory so evidence bytes remain stable across platforms.

## Explicitly changed or added for replay

| Addition | Difference from the historical notebook |
|---|---|
| `src/trigger.py` | Same formula, with batch/device support and input-shape checks. |
| `src/common.py` | Portable dataset wrapper and explicit RGB scaling equivalent to the source's RGB ToTensor path. |
| `src/evaluate.py` | Adds original-model triggered control, raw counts, per-image predictions and current environment capture. |
| `src/demo.py` | Records selected index and both-model comparisons; network action requires an explicit flag. |
| `src/local_transfer.py` | Fixed payload only, request validation, direct loopback connection, hash-verified receipt and guaranteed shutdown. |
| `src/train.py` | Optional new-run version of the training method; never overwrites supplied weights. An optional clean seed changes reproducibility settings from the original. |
| Replay notebook | New, output-free workflow using the supplied checkpoints. |
| Charts | Plot supplied values and saved training losses; not new measurements or generated screenshots. |

## Checks not performed

No full CIFAR-10 download/evaluation or retraining was performed during packaging, and the dataset is not bundled. Therefore no new full-test control value, ASR, accuracy or claim that the uploaded checkpoints reproduce the printed metrics is inserted into the report.

The replay helpers passed the component checks above, but the full Colab replay was not run end-to-end here. No browser import of the Navigator layer, live GitHub update, real reverse shell, external transfer, production detection or tested mitigation is claimed.
