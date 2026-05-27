#!/usr/bin/env python3
"""Check that README.md version headers match x-schema-version in schema.oold.yaml.

Walks every schemas/**/specs/schema.oold.yaml, reads x-schema-version, then
verifies the sibling README.md contains <code>VERSION</code> in its Version row.
Exits 1 if any mismatch is found.
"""

import pathlib
import re
import sys

import yaml

SCHEMA_GLOB = "schemas/**/specs/schema.oold.yaml"

errors = []
checked = 0

root = pathlib.Path(__file__).parent.parent

for schema_path in sorted(root.glob(SCHEMA_GLOB)):
    schema_dir = schema_path.parent.parent  # .../schemas/<domain>/<Ontology>/
    readme_path = schema_dir / "README.md"

    try:
        schema = yaml.safe_load(schema_path.read_text())
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{schema_path.relative_to(root)}: could not parse YAML: {exc}")
        continue

    version = schema.get("x-schema-version")
    if not version:
        continue  # base or internal schema without a version header: skip

    if not readme_path.exists():
        errors.append(
            f"{readme_path.relative_to(root)}: file missing "
            f"(schema version is {version!r})"
        )
        continue

    readme_text = readme_path.read_text()
    match = re.search(
        r"<strong>Version</strong>.*?<code>([^<]+)</code>", readme_text
    )
    if not match:
        errors.append(
            f"{readme_path.relative_to(root)}: "
            f"no version row found: add "
            f"<td><code>{version}</code></td> to the metadata table"
        )
        continue

    readme_version = match.group(1)
    if readme_version != version:
        errors.append(
            f"{schema_path.relative_to(root)}: "
            f"x-schema-version is {version!r} but README shows {readme_version!r}"
        )
    checked += 1

if errors:
    print("README version check FAILED:")
    for msg in errors:
        print(f"  ✗ {msg}")
    sys.exit(1)

print(f"README version check passed ({checked} schemas).")
