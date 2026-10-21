"""Same localized red-X blend as the experiment, with batch/device support."""
import torch

TARGET_CLASS = 0
TRIGGER_ALPHA = 0.30


def add_trigger(images: torch.Tensor, alpha: float = TRIGGER_ALPHA) -> torch.Tensor:
    """Return a new CHW or NCHW float tensor. Inputs are RGB values in [0, 1]."""
    if images.ndim not in (3, 4) or tuple(images.shape[-3:]) != (3, 32, 32):
        raise ValueError("Expected (3,32,32) or (N,3,32,32).")
    if not images.is_floating_point():
        raise TypeError("Use ToTensor-equivalent floating-point RGB input in [0,1].")
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must be in [0,1].")
    pattern = torch.zeros((3, 32, 32), dtype=images.dtype, device=images.device)
    rows = torch.arange(8, 24, device=images.device)
    pattern[0, rows, rows] = 1.0
    pattern[0, rows, 31 - rows] = 1.0
    mask = pattern.sum(dim=0, keepdim=True) > 0
    return torch.where(mask, (1 - alpha) * images + alpha * pattern, images)
