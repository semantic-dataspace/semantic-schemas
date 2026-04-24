# Tensile Test (PMDCo)

Records a **uniaxial tensile test** and its results following the
[PMDCo measurement pattern](https://github.com/materialdigital/core-ontology/tree/main/patterns/measurement),
part of the [Platform MaterialDigital Core Ontology (PMDCo)](https://w3id.org/pmd/co/).

This schema uses generic PMDCo classes for all nodes.  Result properties are
identified by a free-text name label rather than a fixed vocabulary.  Use
[`tensile-test/TTO/`](../TTO/README.md) when classification of individual
mechanical properties against the Tensile Test Ontology (TTO) is required.

---

## Quick start

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "test_name": "Tensile test 316L bar 1",
  "specimen_iri": "https://example.org/specimens/316L-tensile-bar-1",
  "test_standard": "ISO 6892-1",
  "strain_rate": 0.00025,
  "results": [
    { "name": "Yield Strength",   "value": 310, "unit": "MPa" },
    { "name": "Tensile Strength", "value": 620, "unit": "MPa" }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `test_name` | yes | Human-readable name for this test |
| `specimen_iri` | yes | IRI of the specimen being tested |
| `test_standard` | no | Test standard (e.g. "ISO 6892-1") |
| `strain_rate` / `strain_rate_unit` | no | Strain rate and unit |
| `temperature` | no | Test temperature in °C |
| `gauge_length` / `gauge_length_unit` | no | Extensometer gauge length |
| `results` | no | Array of measured properties (name, value, unit) |
| `test_id` | no | Custom IRI slug; auto-derived from `test_name` if omitted |

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example |
| `docs/output_tensile_test.ttl` | Example RDF output for the example input |
| `specs/schema.simplified.json` | Input field reference |
| `specs/transform.simplified.jsonata` | Converts your input to the structured format |
| `specs/schema.oold.yaml` | Full OO-LD schema definition |
| `specs/shape.ttl` | SHACL validation rules |

---

## How this maps to the ontology

```text
TensileTestingProcess  (pmdco:PMD_0000974)
  rdfs:label ──────────────────────────────────────── test name
  realizes  (BFO_0000055) ───────────────────────────► EvaluantRole (OBI_0000067)
    realized_in (BFO_0000054) ──────────────────────── ↩ back to process
  has_specified_input  (OBI_0000293) ───────────────► Specimen IRI
  has_process_attribute  (PMD_0000009) ─────────────► ParameterSpecification (PMD_0000013)
    rdfs:label   condition name
    qudt:value   xsd:double
    qudt:hasUnit unit string
  has_specified_output  (OBI_0000299) ─────────────► MeasurementDatum (IAO_0000109)
    rdfs:label ──────────────────────────────── property name (e.g. "Yield Strength")
    is_about (IAO_0000136) ──────────────────────────► Specimen IRI
    is_quality_measurement_of (IAO_0000221) ─────────► Quality IRI
    has_value_specification (OBI_0001938) ───────────► ScalarValueSpecification (OBI_0001931)
      has_specified_numeric_value (OBI_0001937) ────── xsd:double
      has_measurement_unit_label  (IAO_0000039) ────── QUDT unit IRI
      specifies_value_of (OBI_0001927) ───────────────► Quality IRI
      is_about (IAO_0000136) ─────────────────────────► Specimen IRI
```

---

## TTO vs PMDCo

Both schemas use the same PMDCo measurement pattern (OBI assay backbone,
MeasurementDatum + ScalarValueSpecification).  The only difference is how
result properties are identified.

| | PMDCo schema | TTO schema |
|---|---|---|
| Process class | `pmdco:PMD_0000974` | `tto:TensileTest` (subclass of PMD_0000974) |
| Result datum type | `obo:IAO_0000109` | TTO subclass (e.g. `tto:YieldStrength`) |
| Property identification | Free-text `rdfs:label` | Typed class IRI |
| Cross-dataset SPARQL | String-match on label (fragile) | Class-based query (reliable) |
| New / non-standard properties | Supported | Must exist in TTO vocabulary |

See [`tensile-test/TTO/README.md`](../TTO/README.md) for the full comparison.
