#!/usr/bin/env python3
"""One-shot rehost: pull images referenced in assets/img/manifest.json from
whatever third-party CDN they currently live on, convert to WebP locally,
and rewrite the manifest with relative paths.

After running this once the site has zero third-party image dependencies.
Originals are kept under .local/originals/ (gitignored) for future re-encoding
at different quality, srcset sizes, or AVIF — without re-downloading.

Usage:  python3 rehost_images.py
"""
import io
import json
import os
import sys
from urllib.error import URLError
from urllib.request import urlopen

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST_PATH = os.path.join(ROOT, "assets", "img", "manifest.json")
OUT_DIR = os.path.join(ROOT, "assets", "img")
ORIGINALS_DIR = os.path.join(ROOT, ".local", "originals")
WEBP_QUALITY = 85  # photo-friendly default; raise to 90+ if luxury detail matters more than bytes

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(ORIGINALS_DIR, exist_ok=True)


def pull(url, timeout=30):
    """Fetch bytes from URL with a clear failure message."""
    try:
        with urlopen(url, timeout=timeout) as resp:
            return resp.read()
    except URLError as exc:
        print(f"\n  ERROR fetching {url}: {exc}", file=sys.stderr)
        sys.exit(1)


def main():
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    new_manifest = {}
    total_in = 0
    total_out = 0
    converted = 0
    skipped = 0

    for name, url in sorted(manifest.items()):
        if not url.startswith(("http://", "https://")):
            # Already a relative/local path — nothing to do
            print(f"  [skip] {name:<20} (already local: {url})")
            new_manifest[name] = url
            skipped += 1
            continue

        print(f"  [pull] {name:<20} ", end="", flush=True)
        raw = pull(url)

        # Save lossless original (gitignored)
        orig_path = os.path.join(ORIGINALS_DIR, f"{name}.png")
        with open(orig_path, "wb") as f:
            f.write(raw)
        total_in += len(raw)

        # Convert to WebP
        img = Image.open(io.BytesIO(raw))
        out_path = os.path.join(OUT_DIR, f"{name}.webp")
        img.save(out_path, "webp", quality=WEBP_QUALITY, method=6)
        out_size = os.path.getsize(out_path)
        total_out += out_size

        new_manifest[name] = f"/assets/img/{name}.webp"
        ratio = out_size / len(raw) * 100
        print(f"{len(raw)/1024:>7.0f} KB PNG -> {out_size/1024:>6.0f} KB WebP  ({ratio:>4.0f}%)")
        converted += 1

    # Atomic-ish write of the new manifest
    tmp_path = MANIFEST_PATH + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(new_manifest, f, indent=2)
    os.replace(tmp_path, MANIFEST_PATH)

    print()
    print(f"Converted: {converted}   Skipped: {skipped}")
    if converted:
        print(f"Total in : {total_in/1e6:>6.1f} MB PNG")
        print(f"Total out: {total_out/1e6:>6.1f} MB WebP")
        print(f"Saved    : {(total_in - total_out)/1e6:>6.1f} MB  ({(1 - total_out/total_in)*100:.0f}% reduction)")
    print()
    print("Done. Now run: python3 build.py")


if __name__ == "__main__":
    main()
