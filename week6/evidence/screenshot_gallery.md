# Supplementary screenshots

These are unchanged student captures. The README uses only the most relevant figures; this gallery preserves the additional context.

## Dataset loading

![Successful Hugging Face dataset loading](../images/screenshots/01_dataset_download.png)

The capture shows the downloaded splits. It is supporting setup evidence, not a model evaluation.

## Runtime and GPU

![Recorded Tesla T4 runtime](../images/screenshots/02_colab_gpu.png)

The notification covers part of the dataset figure, but the GPU output is visible. The complete dataset figure is separately extracted from the notebook.

## Trigger visualization

![Red X screenshot](../images/screenshots/03_red_x_trigger.png)

This capture visualizes the perturbation, not successful poisoning.

## Fine-tuning

![Backdoor fine-tuning](../images/screenshots/04_backdoor_training.png)

Three completed epochs and the checkpoint-save message.

## Selected success

![Selected dog classification change](../images/screenshots/05_selected_success.png)

A success chosen by searching the first 500 test rows; not a random sample.

## Printed compromise demonstration

![Printed command session and local file copy](../images/screenshots/06_simulated_compromise.png)

The command strings are printed text. The source code creates and copies fictional JSON; no real shell is opened.

## Integrated HTTP result

![Integrated model comparison and HTTP result](../images/screenshots/07_integrated_http_demo.png)

The separate application component received a successful response from the loopback receiver.

## Exported results

![Export of the three metrics](../images/screenshots/08_results_export.png)

This cell copies the earlier evaluation values into a table and CSV. Primary calculation evidence is the saved evaluation output in notebook cell 14.

## Archived earlier run — not the retained baseline

![Earlier clean training](../images/archive/early_clean_training.png)

![Earlier 70.91 percent clean accuracy](../images/archive/early_clean_accuracy_70_91.png)

These earlier values are intentionally not merged with the retained 71.69% run.
