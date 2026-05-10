"""
Verify that schemas/manifest.json matches what generate_manifest.py would produce.

Run locally:  pytest tests/test_manifest.py
CI:           part of the 'manifest' job in .github/workflows/test.yml

If this test fails, regenerate the manifest:
    python scripts/generate_manifest.py
"""

from __future__ import annotations

import json
from pathlib import Path

import sys

# Allow importing the script without installing it as a package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from generate_manifest import build_manifest, MANIFEST_PATH


def test_manifest_is_up_to_date() -> None:
    expected = json.dumps(build_manifest(), indent=2) + "\n"
    actual = MANIFEST_PATH.read_text()

    if expected == actual:
        return

    # Build a human-readable diff of which entries differ
    exp_tree = {e["path"]: e for e in json.loads(expected)["tree"]}
    act_tree = {e["path"]: e for e in json.loads(actual)["tree"]}

    missing = sorted(set(exp_tree) - set(act_tree))
    extra = sorted(set(act_tree) - set(exp_tree))
    changed = sorted(
        p for p in set(exp_tree) & set(act_tree) if exp_tree[p] != act_tree[p]
    )

    lines = ["manifest.json is out of date. Run: python scripts/generate_manifest.py\n"]
    if missing:
        lines.append("Missing from manifest:")
        lines.extend(f"  + {p}" for p in missing)
    if extra:
        lines.append("Extra entries in manifest (stale):")
        lines.extend(f"  - {p}" for p in extra)
    if changed:
        lines.append("Entries with wrong field values:")
        for p in changed:
            lines.append(f"  ~ {p}")
            lines.append(f"      expected: {exp_tree[p]}")
            lines.append(f"      actual:   {act_tree[p]}")

    raise AssertionError("\n".join(lines))
