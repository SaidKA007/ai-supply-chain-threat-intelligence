"""Paths, image preparation and dataset access; no dataset bundled in this ZIP."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import numpy as np
import torch
from torch.utils.data import Dataset

ROOT = Path(__file__).resolve().parents[1]
CLASSES = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


def image_tensor(image):
    # Equivalent to torchvision ToTensor for these 8-bit RGB PIL images.
    pixels = np.array(image.convert('RGB'), dtype=np.uint8, copy=True)
    return torch.from_numpy(pixels).permute(2, 0, 1).contiguous().float().div(255)


class CIFARWrapper(Dataset):
    def __init__(self, split):
        self.data = split

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        row = self.data[int(index)]
        return image_tensor(row['img']), int(row['label'])


def load_data():
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError('Install requirements.txt, or run %pip install datasets in Colab.') from exc
    # The original experiment did not pin a dataset revision.
    return load_dataset('uoft-cs/cifar10')


def choose_device(requested='auto'):
    if requested == 'auto':
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    device = torch.device(requested)
    if device.type == 'cuda' and not torch.cuda.is_available():
        raise RuntimeError('CUDA is unavailable. Select a GPU runtime or use --device cpu.')
    return device


def new_run_directory(kind):
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    output = ROOT / 'runs' / f'{kind}_{stamp}'
    output.mkdir(parents=True, exist_ok=False)
    return output


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()
