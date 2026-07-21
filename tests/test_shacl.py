"""
SHACL conformance tests for all schemas.

For every schema directory that contains:
  docs/example.input.json      sample input (simplified or OO-LD form)
  specs/schema.oold.yaml       OO-LD context
  specs/shape.ttl              SHACL shapes

the test builds an RDF graph and asserts that it conforms to the SHACL shapes.

Two graph-building paths:

  WITH transform  (specs/transform.simplified.jsonata present):
    example.input.json is in simplified form.  The transform is applied first
    to produce an OO-LD document, which is then parsed with the @context from
    schema.oold.yaml.

  WITHOUT transform:
    example.input.json is expected to already be in OO-LD form (field names
    matching the @context).  It is parsed directly with the effective @context,
    which is assembled by merging contexts from any allOf $ref dependencies so
    that schemas that compose with a base schema get the full context.

If a shape file comments "Load alongside <path>/shape.ttl", that base shape is
loaded too.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import rdflib
import yaml
from jsonata.jsonata import Jsonata

SCHEMAS_ROOT = Path(__file__).parent.parent / "schemas"


# ---------------------------------------------------------------------------
# Context resolution
# ---------------------------------------------------------------------------

def _resolve_context(schema_dir: Path) -> dict:
    """
    Return the effective @context for a schema, merging allOf $ref contexts.

    Schemas that compose with a base schema via allOf carry only their own
    additions in @context.  This function follows one level of $ref and merges
    the base context first so that field names defined in the base are resolved.
    The extending schema's own mappings take precedence on conflict.
    """
    specs_dir = schema_dir / "specs"
    raw = yaml.safe_load((specs_dir / "schema.oold.yaml").read_text())
    own_context = dict(raw.get("@context", {}))

    base_context: dict = {}
    for entry in raw.get("allOf", []):
        ref = entry.get("$ref", "")
        if not ref:
            continue
        ref_path = (specs_dir / ref).resolve()
        if not ref_path.exists():
            continue
        ref_raw = yaml.safe_load(ref_path.read_text())
        base_context.update(ref_raw.get("@context", {}))

    # own_context wins over base on key conflicts
    return {**base_context, **own_context}


# ---------------------------------------------------------------------------
# Schema discovery
# ---------------------------------------------------------------------------

def _find_schemas() -> list[tuple[str, Path, bool]]:
    """
    Return (schema_id, schema_dir, has_transform) for every schema that has
    a shape file and a matching example input.  Schemas without a transform are
    included; their example is parsed directly as an OO-LD document.
    """
    result = []
    for shape_path in sorted(SCHEMAS_ROOT.rglob("specs/shape.ttl")):
        schema_dir = shape_path.parent.parent
        if not (schema_dir / "docs" / "example.input.json").exists():
            continue
        if not (schema_dir / "specs" / "schema.oold.yaml").exists():
            continue
        has_transform = (schema_dir / "specs" / "transform.simplified.jsonata").exists()
        schema_id = str(schema_dir.relative_to(SCHEMAS_ROOT))
        result.append((schema_id, schema_dir, has_transform))
    return result


def _base_shapes(shape_file: Path) -> list[Path]:
    """
    Parse 'Load alongside <path>/shape.ttl' comments and return existing paths.
    """
    deps = []
    for line in shape_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip().lstrip("#").strip()
        if "specs/shape.ttl" not in stripped:
            continue
        for token in stripped.split():
            if token.endswith("shape.ttl"):
                candidate = SCHEMAS_ROOT / token
                if candidate.exists() and candidate != shape_file:
                    deps.append(candidate)
                break
    return deps


# ---------------------------------------------------------------------------
# Graph builders
# ---------------------------------------------------------------------------

def _parse_jsonld(doc: dict, context: dict) -> rdflib.Graph:
    dataset = rdflib.Dataset()
    dataset.parse(
        data=json.dumps({"@context": context, **doc}),
        format="json-ld",
    )
    flat = rdflib.Graph()
    for s, p, o, _ in dataset.quads():
        flat.add((s, p, o))
    return flat


def _build_graph(schema_dir: Path, has_transform: bool) -> rdflib.Graph:
    """Build an RDF graph from the schema's example input."""
    data = json.loads((schema_dir / "docs" / "example.input.json").read_text())
    context = _resolve_context(schema_dir)

    if has_transform:
        transform = (schema_dir / "specs" / "transform.simplified.jsonata").read_text()
        oold_doc = Jsonata(transform).evaluate(data)
        return _parse_jsonld(oold_doc, context)

    # No transform: example is already in OO-LD form
    return _parse_jsonld(data, context)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

_SCHEMAS = _find_schemas()


@pytest.mark.parametrize(
    "schema_id,schema_dir,has_transform",
    _SCHEMAS,
    ids=[s[0] for s in _SCHEMAS],
)
def test_example_conforms_to_shacl(
    schema_id: str, schema_dir: Path, has_transform: bool
) -> None:
    """example.input.json must pass SHACL validation for its schema."""
    import pyshacl

    shape_file = schema_dir / "specs" / "shape.ttl"
    shapes = rdflib.Graph()
    shapes.parse(str(shape_file))
    for base in _base_shapes(shape_file):
        shapes.parse(str(base))

    graph = _build_graph(schema_dir, has_transform)
    conforms, report, _ = pyshacl.validate(graph, shacl_graph=shapes, inference="rdfs")

    if not conforms:
        SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
        lines = []
        for res in report.subjects(rdflib.RDF.type, SH.ValidationResult):
            msg  = report.value(res, SH.resultMessage)
            path = report.value(res, SH.resultPath)
            prop = str(path).rsplit("/", 1)[-1].rsplit("#", 1)[-1] if path else None
            lines.append(f"  - {msg}" + (f"  [{prop}]" if prop else ""))
        mode = "with transform" if has_transform else "no transform"
        pytest.fail(
            f"SHACL violations in '{schema_id}' ({mode}):\n" + "\n".join(lines)
        )
