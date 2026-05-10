#!/usr/bin/env python3
"""
generate_manifest.py — rebuild schemas/manifest.json from the filesystem.

Scans every schema.oold.yaml under schemas/, reads x-maturity, and writes
a fresh manifest.json.  Schemas that set x-hidden: true are omitted from the
manifest (they exist as $ref composition targets only, not for direct use).

Also discovers sibling shape.ttl files and includes them as path-only entries.

Usage:
    python scripts/generate_manifest.py           # regenerate manifest.json
    python scripts/generate_manifest.py --check   # exit non-zero if manifest is stale
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"
MANIFEST_PATH = SCHEMAS_DIR / "manifest.json"


def build_manifest() -> dict:
    """Return the manifest dict as it should currently look on disk."""
    entries: list[dict] = []

    for yaml_path in sorted(SCHEMAS_DIR.rglob("*/specs/schema.oold.yaml")):
        data = yaml.safe_load(yaml_path.read_text())

        if data.get("x-hidden") is True:
            continue

        rel = str(yaml_path.relative_to(REPO_ROOT))
        entry: dict = {"path": rel}

        maturity = data.get("x-maturity")
        if maturity:
            entry["maturity"] = maturity

        entries.append(entry)

        shape = yaml_path.parent / "shape.ttl"
        if shape.exists():
            entries.append({"path": str(shape.relative_to(REPO_ROOT))})

    return {"tree": entries}


def main() -> None:
    check_mode = "--check" in sys.argv
    manifest = build_manifest()
    generated = json.dumps(manifest, indent=2) + "\n"

    if check_mode:
        current = MANIFEST_PATH.read_text() if MANIFEST_PATH.exists() else ""
        if current == generated:
            print("manifest.json is up-to-date.")
        else:
            print(
                "manifest.json is out of date.\n"
                "Run  python scripts/generate_manifest.py  to regenerate it.",
                file=sys.stderr,
            )
            sys.exit(1)
    else:
        MANIFEST_PATH.write_text(generated)
        print(f"Wrote {len(manifest['tree'])} entries to {MANIFEST_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
