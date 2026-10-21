"""Verify the packaged SHA-256 manifest using only the Python standard library."""
from pathlib import Path
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]


def verify():
    manifest = ROOT / 'SHA256SUMS.txt'
    if not manifest.is_file():
        raise FileNotFoundError('SHA256SUMS.txt is missing. Extract the complete package.')
    failures = []
    checked = 0
    for line in manifest.read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'):
            continue
        expected, relative = line.split('  ', 1)
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
            failures.append(f'MISSING/INVALID: {relative}')
            continue
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
        checked += 1
        if digest.hexdigest() != expected:
            failures.append(f'MODIFIED: {relative}')
    print(f'Files checked: {checked}')
    if failures:
        print('\n'.join(failures))
        return False
    print('All packaged file hashes match. This checks integrity, not model safety.')
    return True


if __name__ == '__main__':
    sys.exit(0 if verify() else 1)
