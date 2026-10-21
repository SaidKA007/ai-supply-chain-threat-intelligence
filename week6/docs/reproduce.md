# Reproduce or inspect the experiment

## Two different purposes

**Inspect historical evidence:** use `notebooks/01_original_experiment.ipynb`. This is a byte-identical copy of the upload, including interrupted download attempts, an unexecuted draft and saved outputs. The run order is visible in its execution counters. Do not run every historical setup attempt again just to read the evidence.

**Create a new evaluation:** use `notebooks/02_reproduce_from_checkpoints.ipynb` or the Python helpers in `src/`. The replay notebook has no stored experimental outputs. It reuses the supplied weights rather than retraining them.

## Recommended route: Google Colab

1. Open `02_reproduce_from_checkpoints.ipynb` in Colab. Select a GPU runtime before running the setup cells; CPU also works for small checks.
2. Run setup and upload the complete package ZIP when prompted. It contains the two approximately 2.5 MB checkpoint files and the source modules.
3. Run the evaluation cell. CIFAR-10 is downloaded through Hugging Face Datasets if it is not already cached.
4. Run the demonstration cell to search the first 500 test examples. It only sends the fixed fictional JSON when an eligible prediction change is found and the explicit `send_demo=True` flag is set.
5. Download the new run-output ZIP produced by the last cell. Keep it separate from the original evidence.

The runtime needs internet access for installation and dataset download. The demonstration's HTTP request itself remains on `127.0.0.1` inside that runtime. This is not a claim that the whole Colab environment is offline or that other network access is disabled.

## Local route

Use an isolated Python environment with a maintained PyTorch build. The original runtime reported PyTorch 2.11.0+cu130; the complete original dependency versions were not captured. `requirements.txt` is not an exact environment lockfile.

From inside `week6`:

```bash
python -m pip install -r requirements.txt
python src/evaluate.py --device cpu
python src/demo.py --device cpu --send-demo
```

For the user's Windows laptop, keep this folder, its virtual environment and the dataset cache on **D:** rather than the nearly full C: drive. A local CPU run may be slower than the recorded Colab T4 run. In PowerShell, before starting Python, the cache can be directed to D: with:

```powershell
$env:HF_HOME = "D:\AI_Security_Lab\hf_cache"
```

The replay implementation defaults to zero DataLoader workers for portability. This differs from the original notebook's two workers. The RGB scaling and the X formula are retained. The implementation of image conversion is equivalent to `ToTensor()` for the dataset's RGB 8-bit images.

### Evaluation output

Each evaluation creates a fresh directory under `runs/` containing:

- `evaluation.json`: computed percentages, raw counts, checkpoint hashes and current environment.
- `metrics.csv`: machine-readable values.
- `predictions.csv`: one row per test image, including both models on both input versions.

The **clean-model trigger target rate** is an additional control, not a number that existed in the submitted run. The new control must not be inserted into the original `data/results.csv` as if it had already been measured.

### Demonstration output

`src/demo.py` records the selected dataset row, the selection rule, both models' outputs, and the original and modified inputs. The PNG visualizations round pixels for display; `selected_inputs.pt` retains the exact floating-point inputs. When enabled, the local receiver also saves a fresh payload and receipt with hashes.

The loopback helper is more defensive than the original notebook: fixed payload, one route, length limit, direct local connection, receipt comparison and guaranteed shutdown. These are packaging-time changes, not features claimed for the original Colab run.

## Optional: train again

```bash
python src/train.py --seed 42
```

This follows the same five-plus-three-epoch design but produces a **new run**, not the historical checkpoints. The original baseline initialization was not seeded. Setting a seed now cannot reconstruct that earlier random state.

Training saves both new model files under the printed `runs/retraining_...` directory. To evaluate those instead of the supplied weights, pass that directory:

```bash
python src/evaluate.py --model-dir runs/retraining_YOUR_TIMESTAMP
```

Replace the final path with the directory actually printed by the training script. Do not overwrite the original checkpoints or label new results with the old screenshot values.

## Troubleshooting

| Problem | Action |
|---|---|
| `NameError` after reconnecting Colab | Rerun replay setup; variables belong to the active runtime, not the saved notebook page. |
| Checkpoint not found | Upload/extract the whole ZIP and confirm `week6/models/` contains both files. |
| Dataset install/import failure | Run the notebook dependency cell before importing the helper modules. |
| `Connection refused` for an old fixed port | Do not reuse port 8765. The replay helper starts sender and receiver in the same call and uses an OS-assigned port. |
| No successful example within 500 rows | Retain that result; do not fabricate a success. Check that the intended checkpoint and X definition are loaded. |
| Result differs from 39.48% | Record it as a new evaluation with hashes and environment. Do not hardcode the expected figure. |

## Checks available without the dataset

```bash
python -m unittest discover -s tests -v
python src/verify_package.py
```

The tests validate trigger arithmetic, checkpoint compatibility, counting logic and a fixed-payload loopback round trip. They are not a complete rerun of CIFAR-10 training or evaluation.
