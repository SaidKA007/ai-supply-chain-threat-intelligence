"""Select an explicitly labelled success example and optionally run loopback POST."""
import argparse
import json
from pathlib import Path
import torch
from common import ROOT, CLASSES, image_tensor, load_data, choose_device, new_run_directory
from model import load_model
from trigger import add_trigger, TARGET_CLASS
from local_transfer import send_fictional_data


def predict(net, image, device):
    with torch.inference_mode():
        probabilities = torch.softmax(net(image.unsqueeze(0).to(device)), dim=1)[0]
        label = int(probabilities.argmax().item())
        return label, float(probabilities[label].item() * 100)


def activation_condition(normal_class, triggered_class):
    # Same illustrative application gate as the submitted notebook, not a detector.
    return normal_class != TARGET_CLASS and triggered_class == TARGET_CLASS


def run_demo(output=None, device_name='auto', limit=500, send_demo=False):
    output = Path(output) if output else new_run_directory('demo')
    output.mkdir(parents=True, exist_ok=True)
    device = choose_device(device_name)
    test = load_data()['test']
    backdoor = load_model(ROOT / 'models/backdoored_model.pth', device)
    clean = load_model(ROOT / 'models/clean_model.pth', device)
    selected = None
    searched = min(limit, len(test))
    for index in range(searched):
        row = test[index]
        label = int(row['label'])
        if label == TARGET_CLASS:
            continue
        image = image_tensor(row['img'])
        triggered = add_trigger(image)
        normal_class, normal_score = predict(backdoor, image, device)
        target_class, target_score = predict(backdoor, triggered, device)
        if normal_class == label and target_class == TARGET_CLASS:
            selected = {
                'test_row': index, 'true_label': CLASSES[label],
                'backdoor_original': CLASSES[normal_class], 'backdoor_original_softmax_percent': normal_score,
                'backdoor_triggered': CLASSES[target_class], 'backdoor_triggered_softmax_percent': target_score,
                'selection': f'First eligible successful example in the first {searched} test rows; not random.',
                'provenance': 'New checkpoint demonstration; not the original notebook result.',
            }
            # This control was not printed in the original run.
            cc, cs = predict(clean, image, device)
            ct, ts = predict(clean, triggered, device)
            selected.update({'clean_original': CLASSES[cc], 'clean_original_softmax_percent': cs,
                             'clean_triggered': CLASSES[ct], 'clean_triggered_softmax_percent': ts})
            row['img'].convert('RGB').save(output / 'selected_original.png')
            # Stored tensor preserves the blend exactly; PNG is a rounded visualization.
            torch.save({'original': image.cpu(), 'triggered': triggered.cpu()}, output / 'selected_inputs.pt')
            from PIL import Image
            pixels = triggered.permute(1, 2, 0).mul(255).round().clamp(0, 255).byte().cpu().numpy()
            Image.fromarray(pixels).save(output / 'selected_triggered.png')
            break
    if selected is None:
        print(f'No eligible example in the first {searched} test rows; no HTTP request made.')
        return None
    print(json.dumps(selected, indent=2))
    if send_demo and activation_condition(normal_class, target_class):
        selected['loopback_transfer'] = send_fictional_data(output / 'loopback')
    else:
        selected['loopback_transfer'] = 'Not requested. Use --send-demo for the fixed loopback demonstration.'
    (output / 'selected_example.json').write_text(json.dumps(selected, indent=2), encoding='utf-8')
    print('Saved:', output)
    return selected


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--device', default='auto')
    parser.add_argument('--limit', type=int, default=500)
    parser.add_argument('--send-demo', action='store_true')
    args = parser.parse_args()
    run_demo(args.output, args.device, args.limit, args.send_demo)
