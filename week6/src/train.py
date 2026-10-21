"""Optional NEW training run of the notebook method, never a replacement for evidence.

Original clean initialization was not seeded. New runs may specify --seed.
Models are saved under runs/, leaving the supplied checkpoints untouched.
"""
import argparse
import copy
import csv
import json
import random
from pathlib import Path
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from common import CIFARWrapper, choose_device, load_data, new_run_directory
from model import SimpleCNN
from trigger import add_trigger, TARGET_CLASS


class BackdoorDataset(Dataset):
    def __init__(self, original_dataset, poison_rate=0.10):
        if not 0 <= poison_rate <= 1:
            raise ValueError('poison_rate must be in [0,1].')
        self.original_dataset = original_dataset
        self.poison_indices = set(random.Random(42).sample(
            range(len(original_dataset)), int(len(original_dataset) * poison_rate)))

    def __len__(self):
        return len(self.original_dataset)

    def __getitem__(self, index):
        image, label = self.original_dataset[index]
        if index in self.poison_indices:
            image, label = add_trigger(image), TARGET_CLASS
        return image, label


def train_stage(net, loader, device, epochs, lr, stage, history):
    optimizer = torch.optim.Adam(net.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    for epoch in range(1, epochs + 1):
        net.train()
        losses = 0.0
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            loss = criterion(net(images), labels)
            loss.backward()
            optimizer.step()
            losses += loss.item()
        value = losses / len(loader)  # Same mean-of-batches as the supplied notebook.
        history.append({'stage': stage, 'epoch': epoch, 'loss': value})
        print(f'{stage} epoch {epoch}/{epochs} | loss={value:.4f}')


def run_training(device_name='auto', workers=0, seed=None):
    output = new_run_directory('retraining')
    device = choose_device(device_name)
    if seed is not None:
        torch.manual_seed(seed)
        random.seed(seed)
    dataset = load_data()
    clean_data = CIFARWrapper(dataset['train'])
    clean_loader = DataLoader(clean_data, batch_size=128, shuffle=True, num_workers=workers)
    clean = SimpleCNN().to(device)
    history = []
    train_stage(clean, clean_loader, device, 5, 0.001, 'clean', history)
    torch.save({k: v.detach().cpu() for k, v in clean.state_dict().items()}, output / 'clean_model.pth')
    # Match the seed and copy point of the original backdoor stage.
    torch.manual_seed(42)
    random.seed(42)
    backdoor = copy.deepcopy(clean).to(device)
    poisoned = BackdoorDataset(clean_data, 0.10)
    backdoor_loader = DataLoader(poisoned, batch_size=128, shuffle=True, num_workers=workers)
    train_stage(backdoor, backdoor_loader, device, 3, 0.0001, 'backdoor', history)
    torch.save({k: v.detach().cpu() for k, v in backdoor.state_dict().items()}, output / 'backdoored_model.pth')
    with (output / 'training_history.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['stage', 'epoch', 'loss'])
        writer.writeheader(); writer.writerows(history)
    (output / 'run_metadata.json').write_text(json.dumps({
        'provenance': 'New training run, not the submitted Colab evidence.',
        'clean_seed': seed, 'backdoor_seed': 42, 'poison_samples': len(poisoned.poison_indices),
        'device': str(device), 'torch': torch.__version__, 'workers': workers,
    }, indent=2), encoding='utf-8')
    print('New checkpoints saved to:', output)
    return output


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--device', default='auto')
    p.add_argument('--workers', type=int, default=0)
    p.add_argument('--seed', type=int)
    args = p.parse_args()
    run_training(args.device, args.workers, args.seed)
