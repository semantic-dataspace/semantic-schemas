"""
Structural tests for schema inheritance and composition patterns.

Covers:
  - allOf + $ref (inheritance): relative refs must resolve to existing files,
    and the extending schema must declare all required fields from the base.
  - x-schema-dependencies: referenced schema-ids must map to a schema in this
    repo, and the listed compatible-versions must include the target's current version.
  - x-process-step annotation: every schema whose root type is a workflow step
    class must declare x-process-step with a category.

These tests do not execute transforms or validate RDF — they are fast static
checks on the YAML content.
"""

from __future__ import annotations

import pytest
import yaml
from pathlib import Path

SCHEMAS_ROOT = Path(__file__).parent.parent / "schemas"

# Canonical IRI prefix for resolving x-schema-dependencies schema-ids
_SCHEMA_BASE = "https://github.com/semantic-dataspace/semantic-schemas/tree/main/schemas/"

# Type constants that identify a schema as a workflow process step
_STEP_TYPES = {
    "obo:OBI_0000070",   # PlannedProcess (process-step base)
    "obi:0000070",       # same, short prefix
    "pmdco:PMD_0000974", # TensileTestingProcess
    "pmdco:PMD_0000029", # ManufacturingProcess
    "obi:0000471",       # ComputerSimulation
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _all_schemas() -> list[tuple[str, Path]]:
    return [
        (str(p.parent.parent.relative_to(SCHEMAS_ROOT)), p)
        for p in sorted(SCHEMAS_ROOT.rglob("*/specs/schema.oold.yaml"))
    ]


def _schemas_with_allof_relative_ref() -> list[tuple[str, Path, Path]]:
    """Return (schema_id, yaml_path, resolved_ref_path) for relative allOf refs."""
    result = []
    for schema_id, yaml_path in _all_schemas():
        data = yaml.safe_load(yaml_path.read_text())
        for entry in data.get("allOf") or []:
            ref = entry.get("$ref", "")
            if ref and not ref.startswith("http"):
                resolved = (yaml_path.parent / ref).resolve()
                result.append((schema_id, yaml_path, resolved))
    return result


def _schemas_with_dependencies() -> list[tuple[str, Path, dict]]:
    result = []
    for schema_id, yaml_path in _all_schemas():
        data = yaml.safe_load(yaml_path.read_text())
        for dep in data.get("x-schema-dependencies") or []:
            result.append((schema_id, yaml_path, dep))
    return result


def _step_schemas() -> list[tuple[str, Path]]:
    result = []
    for schema_id, yaml_path in _all_schemas():
        data = yaml.safe_load(yaml_path.read_text())
        root_type = (data.get("properties") or {}).get("type", {}).get("const", "")
        if root_type in _STEP_TYPES:
            result.append((schema_id, yaml_path))
    return result


def _iri_to_schema_dir(schema_id_iri: str) -> Path | None:
    """Convert an x-schema-id IRI to a local directory path, or None."""
    if not schema_id_iri.startswith(_SCHEMA_BASE):
        return None
    rel = schema_id_iri[len(_SCHEMA_BASE):].rstrip("/")
    candidate = SCHEMAS_ROOT / rel
    return candidate if candidate.is_dir() else None


# ---------------------------------------------------------------------------
# allOf inheritance: relative refs must resolve
# ---------------------------------------------------------------------------

_ALLOF_SCHEMAS = _schemas_with_allof_relative_ref()


@pytest.mark.parametrize(
    "schema_id,yaml_path,resolved_ref",
    _ALLOF_SCHEMAS,
    ids=[s[0] for s in _ALLOF_SCHEMAS],
)
def test_allof_ref_resolves(schema_id: str, yaml_path: Path, resolved_ref: Path) -> None:
    """Every allOf $ref (relative path) must point to an existing file."""
    assert resolved_ref.exists(), (
        f"{schema_id}: allOf $ref does not resolve.\n"
        f"  Expected file: {resolved_ref}"
    )


# ---------------------------------------------------------------------------
# allOf inheritance: extending schema must cover base required fields
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "schema_id,yaml_path,resolved_ref",
    _ALLOF_SCHEMAS,
    ids=[s[0] for s in _ALLOF_SCHEMAS],
)
def test_allof_inherits_required_fields(
    schema_id: str, yaml_path: Path, resolved_ref: Path
) -> None:
    """
    An extending schema must declare all required fields from its base as
    properties (they can be overridden, but must not silently disappear).
    The merged required list (base ∪ extension) must be a subset of the
    extension's declared properties.
    """
    base = yaml.safe_load(resolved_ref.read_text())
    ext = yaml.safe_load(yaml_path.read_text())

    base_required: list[str] = base.get("required") or []
    ext_required: list[str] = ext.get("required") or []
    ext_properties: set[str] = set((ext.get("properties") or {}).keys())
    base_properties: set[str] = set((base.get("properties") or {}).keys())

    merged_required = set(base_required) | set(ext_required)
    merged_properties = base_properties | ext_properties

    missing = merged_required - merged_properties
    assert not missing, (
        f"{schema_id}: allOf composition is incomplete.\n"
        f"  Required fields not declared in any properties block: {sorted(missing)}\n"
        f"  Base required:      {sorted(base_required)}\n"
        f"  Extension required: {sorted(ext_required)}\n"
        f"  Merged properties:  {sorted(merged_properties)}"
    )


# ---------------------------------------------------------------------------
# x-schema-dependencies: referenced schemas exist and versions are current
# ---------------------------------------------------------------------------

_DEP_SCHEMAS = _schemas_with_dependencies()


@pytest.mark.parametrize(
    "schema_id,yaml_path,dep",
    _DEP_SCHEMAS,
    ids=[f"{s[0]}→{s[2]['schema-id'].split('/')[-2]}" for s in _DEP_SCHEMAS],
)
def test_schema_dependency_exists(schema_id: str, yaml_path: Path, dep: dict) -> None:
    """x-schema-dependencies schema-id must map to a schema directory in this repo."""
    target_dir = _iri_to_schema_dir(dep["schema-id"])
    assert target_dir is not None, (
        f"{schema_id}: x-schema-dependencies references unknown schema:\n"
        f"  {dep['schema-id']}\n"
        f"  IRI must start with {_SCHEMA_BASE}"
    )
    assert target_dir.is_dir(), (
        f"{schema_id}: x-schema-dependencies directory does not exist:\n"
        f"  {target_dir}"
    )
    assert (target_dir / "specs" / "schema.oold.yaml").exists(), (
        f"{schema_id}: x-schema-dependencies target has no schema.oold.yaml:\n"
        f"  {target_dir / 'specs' / 'schema.oold.yaml'}"
    )


@pytest.mark.parametrize(
    "schema_id,yaml_path,dep",
    _DEP_SCHEMAS,
    ids=[f"{s[0]}→{s[2]['schema-id'].split('/')[-2]}" for s in _DEP_SCHEMAS],
)
def test_schema_dependency_version_current(
    schema_id: str, yaml_path: Path, dep: dict
) -> None:
    """
    The compatible-versions list must include the target schema's current
    x-schema-version.  Stale version pins are caught here before release.
    """
    target_dir = _iri_to_schema_dir(dep["schema-id"])
    if target_dir is None:
        pytest.skip("target directory not found (covered by test_schema_dependency_exists)")

    target_yaml = target_dir / "specs" / "schema.oold.yaml"
    if not target_yaml.exists():
        pytest.skip("target schema.oold.yaml missing")

    target_data = yaml.safe_load(target_yaml.read_text())
    current_version = target_data.get("x-schema-version")
    compatible = dep.get("compatible-versions") or []

    assert current_version in compatible, (
        f"{schema_id}: x-schema-dependencies version pin is stale.\n"
        f"  Referenced schema: {dep['schema-id']}\n"
        f"  Current version:   {current_version}\n"
        f"  Listed versions:   {compatible}\n"
        f"  Add '{current_version}' to compatible-versions."
    )


# ---------------------------------------------------------------------------
# x-process-step: all step-typed schemas must declare a category
# ---------------------------------------------------------------------------

_STEP_SCHEMAS = _step_schemas()


@pytest.mark.parametrize(
    "schema_id,yaml_path",
    _STEP_SCHEMAS,
    ids=[s[0] for s in _STEP_SCHEMAS],
)
def test_step_schema_has_xprocess_step(schema_id: str, yaml_path: Path) -> None:
    """
    Every schema whose root type is a workflow step class must declare
    x-process-step with a non-empty category string.
    """
    data = yaml.safe_load(yaml_path.read_text())
    xps = data.get("x-process-step")
    assert xps, (
        f"{schema_id}: root type is a workflow step class but x-process-step is missing.\n"
        f"  Add x-process-step: {{category: <characterization|simulation|manufacturing|preparation|generic>}}"
    )
    assert xps.get("category"), (
        f"{schema_id}: x-process-step is declared but 'category' is empty or missing."
    )
