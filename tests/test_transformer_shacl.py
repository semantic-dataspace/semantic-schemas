"""
Integration tests: full Transformer pipeline → SHACL validation.

test_shacl.py validates the JSONata transform path only (example.input.json →
OO-LD → graph).  These tests cover the path that the notebook exercises:
parser → Transformer → graph, including the csvw:Table timeseries descriptor
that _add_timeseries_nodes() appends via OBI_0000299.

Both semantic_transformers and the example instrument file must be present;
individual tests are skipped otherwise.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import rdflib

SCHEMAS_ROOT     = Path(__file__).parent.parent / "schemas"

TTO_SCHEMA_DIR   = SCHEMAS_ROOT / "characterization" / "step" / "tensile-test" / "TTO"
PMDCO_SCHEMA_DIR = SCHEMAS_ROOT / "characterization" / "step" / "tensile-test" / "PMDCo"
BASE_SCHEMA_DIR  = SCHEMAS_ROOT / "characterization" / "step" / "base" / "PMDCo"
TTO_CSV_FILE     = TTO_SCHEMA_DIR   / "docs" / "example_tensile_test.TXT"
PMDCO_CSV_FILE   = PMDCO_SCHEMA_DIR / "docs" / "example_tensile_test.TXT"


def _load_shapes(*shape_files: Path) -> rdflib.Graph:
    shapes = rdflib.Graph()
    for f in shape_files:
        shapes.parse(str(f))
    return shapes


def _shacl_violations(report: rdflib.Graph) -> list[str]:
    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
    lines = []
    for res in report.subjects(rdflib.RDF.type, SH.ValidationResult):
        msg  = report.value(res, SH.resultMessage)
        path = report.value(res, SH.resultPath)
        prop = str(path).rsplit("/", 1)[-1].rsplit("#", 1)[-1] if path else None
        lines.append(str(msg) + (f"  [{prop}]" if prop else ""))
    return lines


# ---------------------------------------------------------------------------
# TTO schema — TestXpertIII parser
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def tto_transformer_result():
    pytest.importorskip("semantic_transformers")
    if not TTO_CSV_FILE.exists():
        pytest.skip(f"example CSV not found: {TTO_CSV_FILE}")

    from semantic_transformers import Transformer
    from semantic_transformers.parsers.characterization.tensile_test.testxpert_iii import (
        TestXpertIIIParser,
    )

    return Transformer(
        parser=TestXpertIIIParser(),
        semantic_schema=TTO_SCHEMA_DIR,
    ).run(
        TTO_CSV_FILE,
        base="https://example.org/",
        specimen_iri="https://example.org/specimens/example-specimen",
    )


def test_tto_transformer_graph_conforms_to_shacl(tto_transformer_result):
    """Transformer output (parser + timeseries nodes) must pass TTO SHACL."""
    pyshacl = pytest.importorskip("pyshacl")

    shapes = _load_shapes(
        TTO_SCHEMA_DIR  / "specs" / "shape.ttl",
        BASE_SCHEMA_DIR / "specs" / "shape.ttl",
    )
    conforms, report, _ = pyshacl.validate(
        tto_transformer_result.flat_graph,
        shacl_graph=shapes,
        inference="rdfs",
    )

    violations = _shacl_violations(report)
    assert conforms, "SHACL violations in Transformer output:\n" + "\n".join(
        f"  - {v}" for v in violations
    )


def test_tto_transformer_graph_has_specimen(tto_transformer_result):
    """Graph must contain the specimen IRI passed via overrides."""
    OBI = rdflib.Namespace("http://purl.obolibrary.org/obo/OBI_")
    flat = tto_transformer_result.flat_graph
    specimen = rdflib.URIRef("https://example.org/specimens/example-specimen")
    assert (None, OBI["0000293"], specimen) in flat


def test_tto_transformer_graph_has_timeseries_table(tto_transformer_result):
    """Transformer must add a csvw:Table node linked via OBI_0000299."""
    CSVW = rdflib.Namespace("http://www.w3.org/ns/csvw#")
    OBI  = rdflib.Namespace("http://purl.obolibrary.org/obo/OBI_")
    flat = tto_transformer_result.flat_graph
    table_nodes = list(flat.subjects(rdflib.RDF.type, CSVW.Table))
    assert len(table_nodes) == 1, f"expected 1 csvw:Table, got {len(table_nodes)}"
    table = table_nodes[0]
    assert (None, OBI["0000299"], table) in flat


# ---------------------------------------------------------------------------
# PMDCo schema — TestXpertIII parser
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def pmdco_transformer_result():
    pytest.importorskip("semantic_transformers")
    if not PMDCO_CSV_FILE.exists():
        pytest.skip(f"example CSV not found: {PMDCO_CSV_FILE}")

    from semantic_transformers import Transformer
    from semantic_transformers.parsers.characterization.tensile_test.testxpert_iii import (
        TestXpertIIIParser,
    )

    return Transformer(
        parser=TestXpertIIIParser(),
        semantic_schema=PMDCO_SCHEMA_DIR,
    ).run(
        PMDCO_CSV_FILE,
        base="https://example.org/",
        specimen_iri="https://example.org/specimens/example-specimen",
    )


def test_pmdco_transformer_graph_conforms_to_shacl(pmdco_transformer_result):
    """Transformer output (parser + timeseries nodes) must pass PMDCo SHACL."""
    pyshacl = pytest.importorskip("pyshacl")

    shapes = _load_shapes(
        PMDCO_SCHEMA_DIR / "specs" / "shape.ttl",
        BASE_SCHEMA_DIR  / "specs" / "shape.ttl",
    )
    conforms, report, _ = pyshacl.validate(
        pmdco_transformer_result.flat_graph,
        shacl_graph=shapes,
        inference="rdfs",
    )

    violations = _shacl_violations(report)
    assert conforms, "SHACL violations in PMDCo Transformer output:\n" + "\n".join(
        f"  - {v}" for v in violations
    )


def test_pmdco_transformer_graph_has_specimen(pmdco_transformer_result):
    """Graph must contain the specimen IRI passed via overrides."""
    OBI = rdflib.Namespace("http://purl.obolibrary.org/obo/OBI_")
    flat = pmdco_transformer_result.flat_graph
    specimen = rdflib.URIRef("https://example.org/specimens/example-specimen")
    assert (None, OBI["0000293"], specimen) in flat


def test_pmdco_transformer_graph_has_timeseries_table(pmdco_transformer_result):
    """Transformer must add a csvw:Table node linked via OBI_0000299."""
    CSVW = rdflib.Namespace("http://www.w3.org/ns/csvw#")
    OBI  = rdflib.Namespace("http://purl.obolibrary.org/obo/OBI_")
    flat = pmdco_transformer_result.flat_graph
    table_nodes = list(flat.subjects(rdflib.RDF.type, CSVW.Table))
    assert len(table_nodes) == 1, f"expected 1 csvw:Table, got {len(table_nodes)}"
    table = table_nodes[0]
    assert (None, OBI["0000299"], table) in flat
