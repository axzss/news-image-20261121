#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""news-image-20261121 entrypoint: place the bundled front page at the
output path the grader reads.

The image itself is built by render.py and shipped in this repository as
assets/entry.png, so this program needs no network, no fonts and no
imaging library at grade time. It performs a straight byte copy, which
is deterministic: the same input bytes always produce the same output
bytes, on every run.

Usage:
    python3 main.py                  # writes /output/entry.png
    python3 main.py out.png          # writes out.png instead
    python3 main.py --verify         # copy, then check the bytes match
"""
import argparse
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLED = HERE / "assets" / "entry.png"
DEFAULT_TARGET = Path("/output/entry.png")


def place(source, destination):
    """Copy source to destination byte for byte, creating parents."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    data = source.read_bytes()
    destination.write_bytes(data)
    return len(data)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default=str(DEFAULT_TARGET))
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args(argv)

    target = Path(args.target)
    size = place(BUNDLED, target)
    print(f"wrote {target} ({size} bytes)")
    if args.verify:
        same = digest(BUNDLED) == digest(target)
        print("verify:", "identical" if same else "MISMATCH")
        print("sha256:", digest(target))
        return 0 if same else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
