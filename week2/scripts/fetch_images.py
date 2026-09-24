#!/usr/bin/env python3
"""Optionally preserve the five original publication images locally.

Network access is required. Only allowlisted PNGs are requested; no observable,
model, package, or suspect repository is visited. Source rights remain unchanged.
The delivered README already works online with the original image URLs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 8 * 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
ALLOWED_URLS = frozenset({
    "https://arxiv.org/html/2602.04653v4/images/intro_fig.png",
    "https://arxiv.org/html/2602.04653v4/images/HF_model_2.png",
    "https://arxiv.org/html/2602.04653v4/images/scenario_b_asr_summary.png",
    "https://unit42.paloaltonetworks.com/wp-content/uploads/2025/08/word-image-141727-155226-5.png",
    "https://unit42.paloaltonetworks.com/wp-content/uploads/2025/08/word-image-144491-155226-6.png",
})
ALLOWED_HOSTS = frozenset({"arxiv.org", "unit42.paloaltonetworks.com"})


def download(url: str, timeout: float) -> tuple[bytes, str]:
    if url not in ALLOWED_URLS:
        raise ValueError("Refusing a URL outside the original publication-image allowlist")
    request = Request(url, headers={"User-Agent": "Week2-Academic-Source-Preservation/1.0"})
    with urlopen(request, timeout=timeout) as response:
        final_url = response.geturl()
        if urlsplit(final_url).scheme != "https" or urlsplit(final_url).hostname not in ALLOWED_HOSTS:
            raise ValueError("Unexpected image redirect destination")
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Image exceeds the 8 MiB size limit")
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("Response is not a PNG; it may be a block or error page")
    return data, final_url


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--localize", action="store_true", help="Rewrite README image links only after all five images download successfully")
    parser.add_argument("--timeout", type=float, default=30.0, help="Timeout in seconds per image (default: 30)")
    args = parser.parse_args()
    if not 0 < args.timeout <= 120:
        parser.error("--timeout must be greater than 0 and at most 120 seconds")
    try:
        manifest = json.loads((ROOT / "images/manifest.json").read_text(encoding="utf-8"))
        if {row["url"] for row in manifest} != ALLOWED_URLS or len(manifest) != 5:
            raise ValueError("Manifest no longer matches the five verified source-image URLs")
        records = []
        for row in manifest:
            name = row["local_filename"]
            if Path(name).name != name or not name.endswith(".png"):
                raise ValueError("Unsafe local image filename")
            data, final_url = download(row["url"], args.timeout)
            target = ROOT / "images" / name
            temporary = target.with_suffix(".png.tmp")
            temporary.write_bytes(data)
            temporary.replace(target)
            records.append({"media_id": row["media_id"], "original_url": row["url"],
                            "final_url": final_url, "local_path": "images/" + name,
                            "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                            "downloaded_at_utc": datetime.now(timezone.utc).isoformat()})
            print(f"Saved {name} ({len(data)} bytes)")
        receipt = {"action": "Original publication PNG downloads", "records": records,
                   "readme_localized": bool(args.localize),
                   "notice": "Actual local copies; original authorship and rights remain unchanged."}
        (ROOT / "images/download_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        if args.localize:
            path = ROOT / "README.md"
            text = path.read_text(encoding="utf-8")
            for row in manifest:
                text = text.replace("](" + row["url"] + ")", "](images/" + row["local_filename"] + ")")
            path.write_text(text, encoding="utf-8")
            print("README now uses local image paths. Rerun validate_dataset.py and review before committing.")
        else:
            print("Downloads completed. README still uses original URLs; use --localize to change that.")
        print("The original manifest remains the record of initial delivery; download_receipt.json records this new action.")
    except (OSError, URLError, HTTPError, ValueError, KeyError, TypeError) as exc:
        print(f"Image preservation failed: {exc}", file=sys.stderr)
        print("No README rewrite was completed. Keep the original remote image links; review any partial files before committing.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
