"""Re-evaluate saved weights. New outputs never replace the reported results.csv.

Adds a clean-model trigger control missing from the original experiment.
"""
import argparse
import csv
import json
import platform
from pathlib import Path
import torch
from torch.utils.data import DataLoader
from common import ROOT, CIFARWrapper, choose_device, load_data, new_run_directory, sha256
from model import load_model
from trigger import TARGET_CLASS, add_trigger


def evaluate_models(clean, backdoor, loader, device, predictions_path=None):
    clean.eval()
    backdoor.eval()
    total = non_target = 0
    clean_correct = backdoor_correct = clean_target_hits = backdoor_target_hits = 0
    clean_trigger_correct = backdoor_trigger_correct = 0
    stream = None
    writer = None
    try:
        if predictions_path is not None:
            stream = Path(predictions_path).open('w', newline='', encoding='utf-8')
            writer = csv.writer(stream)
            writer.writerow(['test_row', 'true_label', 'clean_original', 'clean_triggered',
                             'backdoor_original', 'backdoor_triggered', 'asr_eligible'])
        with torch.inference_mode():
            for images, labels in loader:
                images, labels = images.to(device), labels.to(device)
                triggered = add_trigger(images)
                pc = clean(images).argmax(1)
                pcb = clean(triggered).argmax(1)
                pb = backdoor(images).argmax(1)
                pbb = backdoor(triggered).argmax(1)
                eligible = labels != TARGET_CLASS
                clean_correct += (pc == labels).sum().item()
                backdoor_correct += (pb == labels).sum().item()
                clean_trigger_correct += (pcb == labels).sum().item()
                backdoor_trigger_correct += (pbb == labels).sum().item()
                clean_target_hits += ((pcb == TARGET_CLASS) & eligible).sum().item()
                backdoor_target_hits += ((pbb == TARGET_CLASS) & eligible).sum().item()
                non_target += eligible.sum().item()
                if writer:
                    rows = torch.stack([labels, pc, pcb, pb, pbb, eligible.long()], 1).cpu().tolist()
                    for offset, row in enumerate(rows):
                        writer.writerow([total + offset, *row])
                total += len(labels)
    finally:
        if stream:
            stream.close()
    if not total or not non_target:
        raise ValueError('Need a non-empty test set containing non-target examples.')
    return {
        'test_images': total, 'non_target_images': non_target,
        'clean_correct': clean_correct, 'backdoor_clean_correct': backdoor_correct,
        'backdoor_target_hits': backdoor_target_hits,
        'clean_trigger_target_hits': clean_target_hits,
        'clean_accuracy_percent': 100 * clean_correct / total,
        'backdoor_clean_accuracy_percent': 100 * backdoor_correct / total,
        'backdoor_asr_percent': 100 * backdoor_target_hits / non_target,
        'clean_trigger_target_rate_percent': 100 * clean_target_hits / non_target,
        'clean_triggered_accuracy_percent': 100 * clean_trigger_correct / total,
        'backdoor_triggered_accuracy_percent': 100 * backdoor_trigger_correct / total,
    }


def run_evaluation(output=None, device_name='auto', batch_size=128, workers=0, model_dir=None):
    output = Path(output) if output else new_run_directory('evaluation')
    output.mkdir(parents=True, exist_ok=True)
    device = choose_device(device_name)
    dataset = load_data()
    test = CIFARWrapper(dataset['test'])
    loader = DataLoader(test, batch_size=batch_size, shuffle=False, num_workers=workers)
    model_dir = Path(model_dir) if model_dir else ROOT / 'models'
    clean_path = model_dir / 'clean_model.pth'
    backdoor_path = model_dir / 'backdoored_model.pth'
    clean, backdoor = load_model(clean_path, device), load_model(backdoor_path, device)
    result = evaluate_models(clean, backdoor, loader, device, output / 'predictions.csv')
    result['provenance'] = 'New checkpoint evaluation, not the submitted Colab run.'
    result['environment'] = {'python': platform.python_version(), 'torch': torch.__version__, 'device': str(device)}
    result['checkpoint_sha256'] = {'clean': sha256(clean_path), 'backdoor': sha256(backdoor_path)}
    result['dataset_fingerprint'] = getattr(dataset['test'], '_fingerprint', None)
    (output / 'evaluation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    with (output / 'metrics.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['metric', 'value_percent'])
        writer.writerows((k, v) for k, v in result.items() if k.endswith('_percent'))
    for name, value in result.items():
        if name.endswith('_percent'):
            print(f'{name}: {value:.2f}%')
    print(f'New evaluation saved to: {output}')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path)
    p.add_argument('--device', default='auto')
    p.add_argument('--batch-size', type=int, default=128)
    p.add_argument('--workers', type=int, default=0)
    p.add_argument('--model-dir', type=Path, help='Optional directory containing both checkpoint filenames')
    args = p.parse_args()
    run_evaluation(args.output, args.device, args.batch_size, args.workers, args.model_dir)
