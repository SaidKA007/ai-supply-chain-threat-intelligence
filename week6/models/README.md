# Model checkpoints — laboratory use only

These are the actual state dictionaries supplied by the student. Both use the same `SimpleCNN` architecture from the original notebook. They are not ResNet-18 weights and not language models.

**The backdoored checkpoint is intentionally modified for an educational experiment. Do not present it as a clean or production model.** It contains learned parameters for a red-X/airplane experiment, not an embedded reverse shell.

| File | Bytes | Parameters | SHA-256 |
|---|---:|---:|---|
| `clean_model.pth` | 2,486,021 | 620,362 | `02c090b22840c0069de71f945376f46584f7b13ff07245256b60c3d00c288257` |
| `backdoored_model.pth` | 2,486,101 | 620,362 | `dd54176da5da164f001946fcd4d72f608b879874c08e1518c03c0281623a19ef` |

Files were copied without modifying their bytes. The upload suffix `(1)` was removed from the filenames only. Packaging checks loaded both files with `weights_only=True`, checked tensor shapes and finite values, and confirmed that weights differ. These checks are not a full dataset evaluation or a certificate of model safety.

The original-model reported clean accuracy is 71.69%; the modified-model clean accuracy is 72.32%; reported targeted ASR is 39.48%. These are the original notebook's measurements. A new run must save its own numbers.

Use `src/model.py` to instantiate the exact architecture and load tensor state dictionaries. New training runs save elsewhere under `runs/`. Full structural check details are in `../evidence/model_inspection.json`.
