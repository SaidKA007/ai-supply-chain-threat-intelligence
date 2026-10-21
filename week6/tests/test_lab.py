"""Packaging checks only: they do not reproduce the full CIFAR-10 experiment."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from common import ROOT
from model import SimpleCNN, load_model
from trigger import add_trigger
from evaluate import evaluate_models
from local_transfer import send_fictional_data, DEMO_PAYLOAD
from demo import activation_condition
from train import BackdoorDataset

torch.set_num_threads(1)


class TriggerTests(unittest.TestCase):
    def test_original_input_is_unchanged(self):
        image = torch.rand(3, 32, 32)
        original = image.clone()
        output = add_trigger(image)
        self.assertTrue(torch.equal(image, original))
        self.assertNotEqual(image.data_ptr(), output.data_ptr())

    def test_same_formula_as_submitted_function(self):
        image = torch.rand(3, 32, 32)
        pattern = torch.zeros_like(image)
        for i in range(8, 24):
            pattern[:, i, i] = torch.tensor([1.0, 0.0, 0.0])
            pattern[:, i, 31-i] = torch.tensor([1.0, 0.0, 0.0])
        expected = torch.where(pattern.sum(0, keepdim=True) > 0,
                               0.70 * image + 0.30 * pattern, image)
        self.assertTrue(torch.equal(add_trigger(image), expected))

    def test_exactly_32_spatial_pixels_on_blank_input(self):
        output = add_trigger(torch.zeros(3, 32, 32))
        self.assertEqual(int((output.abs().sum(0) > 0).sum()), 32)
        self.assertEqual(float(output.max()), float(torch.tensor(0.30)))

    def test_batch_matches_individual_calls(self):
        images = torch.rand(4, 3, 32, 32)
        self.assertTrue(torch.equal(add_trigger(images), torch.stack([add_trigger(x) for x in images])))

    def test_rejects_wrong_shape(self):
        with self.assertRaises(ValueError):
            add_trigger(torch.zeros(3, 64, 64))


class CheckpointTests(unittest.TestCase):
    def test_both_states_load_and_predict(self):
        for name in ['clean_model.pth', 'backdoored_model.pth']:
            model = load_model(ROOT / 'models' / name, torch.device('cpu'))
            with torch.inference_mode():
                result = model(torch.zeros(2, 3, 32, 32))
            self.assertEqual(tuple(result.shape), (2, 10))
            self.assertTrue(bool(torch.isfinite(result).all()))

    def test_weights_differ(self):
        a = load_model(ROOT / 'models/clean_model.pth', torch.device('cpu')).state_dict()
        b = load_model(ROOT / 'models/backdoored_model.pth', torch.device('cpu')).state_dict()
        self.assertTrue(any(not torch.equal(a[k], b[k]) for k in a))

    def test_parameter_count(self):
        self.assertEqual(sum(p.numel() for p in SimpleCNN().parameters()), 620362)


class LogicTests(unittest.TestCase):
    def test_asr_denominator_excludes_target(self):
        class ConstantTarget(nn.Module):
            def forward(self, x):
                y = torch.zeros(len(x), 10, device=x.device)
                y[:, 0] = 1
                return y
        loader = DataLoader(TensorDataset(torch.zeros(3, 3, 32, 32), torch.tensor([0, 1, 2])), batch_size=2)
        result = evaluate_models(ConstantTarget(), ConstantTarget(), loader, torch.device('cpu'))
        self.assertEqual(result['test_images'], 3)
        self.assertEqual(result['non_target_images'], 2)
        self.assertEqual(result['backdoor_target_hits'], 2)
        self.assertEqual(result['backdoor_asr_percent'], 100)

    def test_gate(self):
        self.assertTrue(activation_condition(5, 0))
        self.assertFalse(activation_condition(0, 0))
        self.assertFalse(activation_condition(3, 3))

    def test_fixed_poison_selection(self):
        data = TensorDataset(torch.zeros(100, 3, 32, 32), torch.ones(100, dtype=torch.long))
        a, b = BackdoorDataset(data), BackdoorDataset(data)
        self.assertEqual(len(a.poison_indices), 10)
        self.assertEqual(a.poison_indices, b.poison_indices)
        poisoned = next(iter(a.poison_indices))
        self.assertEqual(a[poisoned][1], 0)
        self.assertEqual(int(data[poisoned][1]), 1)

    def test_loopback_payload_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = send_fictional_data(Path(tmp))
            self.assertEqual(result['status'], 200)
            self.assertEqual(result['sent_sha256'], result['receipt']['received_sha256'])
            self.assertEqual(result['receipt']['client_host'], '127.0.0.1')
            received = json.loads((Path(tmp) / 'received_demo_payload.json').read_text())
            self.assertEqual(received, DEMO_PAYLOAD)


if __name__ == '__main__':
    unittest.main(verbosity=2)
