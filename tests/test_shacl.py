"""
SHACL conformance tests for all schemas.

For every schema directory that contains:
  docs/example.input.json      sample simplified-JSON input
  specs/transform.simplified.jsonata JSONata transform
  specs/schema.oold.yaml       OO-LD context
  specs/shape.ttl              SHACL shapes

the test applies the transform, builds the RDF graph, and asserts that it
conforms to the SHACL shapes.  If a shape file comments "Load alongside
<path>/shape.ttl", that base shape is loaded too.
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
# Schema discovery
# ---------------------------------------------------------------------------

def _find_schemas() -> list[tuple[str, Path]]:
    """Return (schema_id, schema_dir) for every fully-equipped schema."""
    result = []
    for shape_path in sorted(SCHEMAS_ROOT.rglob("specs/shape.ttl")):
        schema_dir = shape_path.parent.parent
        if all([
            (schema_dir / "docs" / "example.input.json").exists(),
            (schema_dir / "specs" / "transform.simplified.jsonata").exists(),
            (schema_dir / "specs" / "schema.oold.yaml").exists(),
        ]):
            schema_id = str(schema_dir.relative_to(SCHEMAS_ROOT))
            result.append((schema_id, schema_dir))
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
# Graph builder
# ---------------------------------------------------------------------------

def _build_graph(schema_dir: Path) -> rdflib.Graph:
    """Run example.input.json through transform + OO-LD context → flat RDF graph."""
    data        = json.loads((schema_dir / "docs" / "example.input.json").read_text())
    transform   = (schema_dir / "specs" / "transform.simplified.jsonata").read_text()
    raw_context = yaml.safe_load((schema_dir / "specs" / "schema.oold.yaml").read_text())
    context     = raw_context["@context"]

    oold_doc = Jsonata(transform).evaluate(data)

    dataset = rdflib.Dataset()
    dataset.parse(
        data   = json.dumps({"@context": context, **oold_doc}),
        format = "json-ld",
    )
    flat = rdflib.Graph()
    for s, p, o, _ in dataset.quads():
        flat.add((s, p, o))
    return flat


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

_SCHEMAS = _find_schemas()


@pytest.mark.parametrize(
    "schema_id,schema_dir",
    _SCHEMAS,
    ids=[s[0] for s in _SCHEMAS],
)
def test_example_conforms_to_shacl(schema_id: str, schema_dir: Path) -> None:
    """example.input.json must pass SHACL validation for its schema."""
    import pyshacl

    shape_file = schema_dir / "specs" / "shape.ttl"
    shapes = rdflib.Graph()
    shapes.parse(str(shape_file))
    for base in _base_shapes(shape_file):
        shapes.parse(str(base))

    graph = _build_graph(schema_dir)
    conforms, report, _ = pyshacl.validate(graph, shacl_graph=shapes, inference="rdfs")

    if not conforms:
        SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
        lines = []
        for res in report.subjects(rdflib.RDF.type, SH.ValidationResult):
            msg  = report.value(res, SH.resultMessage)
            path = report.value(res, SH.resultPath)
            prop = str(path).rsplit("/", 1)[-1].rsplit("#", 1)[-1] if path else None
            lines.append(f"  - {msg}" + (f"  [{prop}]" if prop else ""))
        pytest.fail(f"SHACL violations in '{schema_id}':\n" + "\n".join(lines))
