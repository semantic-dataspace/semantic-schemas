# Tensile Test (TTO)

Records a **uniaxial tensile test** and its measured mechanical properties
following the
[Tensile Test Ontology (TTO)](https://w3id.org/pmd/tto/) built on the
[Platform MaterialDigital Core Ontology (PMDCo)](https://w3id.org/pmd/co/).

This schema **extends** [`characterization/step/PMDCo/`](../../step/PMDCo/README.md)
via JSON Schema `$ref` and `allOf`. It inherits the generic characterization
structure (specimen input, test conditions, process chain position) and adds
tensile-test-specific result fields typed to TTO classes.

---

## Schema inheritance

```text
characterization/step/PMDCo/          base schema
  has_specified_input  (specimen IRI)
  preceded_by          (chain)
  has_process_condition (conditions)
        ▲
        │  $ref + allOf
        │
characterization/tensile-test/TTO/   this schema
  type: tto:TensileTest               overrides root class
  measured_properties                 adds result nodes
    tto:YieldStrength
    tto:TensileStrength
    tto:PercentageElongationAfterFracture
    …
```

This is the same mechanism used by `specimen/PMDCo/`, which extends
`chemical-composition/PMDCo/`.

---

## Quick start

**The fastest way in:** open the notebook.

```bash
pip install jupyterlab
jupyter lab docs/1_tensile_test_workflow.ipynb
```

### Input fields

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "test_name":    "Tensile test 316L bar 1",
  "specimen_iri": "https://example.org/specimens/316L-tensile-bar-1",
  "test_standard": "ISO 6892-1",
  "strain_rate": 0.00025,
  "strain_rate_unit": "1/s",
  "temperature": 23,
  "results": [
    { "property": "YieldStrength",                     "value": 310, "unit": "MPa" },
    { "property": "TensileStrength",                   "value": 620, "unit": "MPa" },
    { "property": "PercentageElongationAfterFracture", "value": 40,  "unit": "%" }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `test_name` | yes | Name for this test |
| `specimen_iri` | yes | IRI of the specimen tested |
| `test_standard` | no | Standard applied (e.g. `"ISO 6892-1"`) |
| `strain_rate` | no | Strain or displacement rate |
| `strain_rate_unit` | no | Unit for strain rate; default `"1/s"` |
| `temperature` | no | Test temperature in °C |
| `results` | no | List of measured properties (see below) |
| `test_id` | no | Custom IRI slug; auto-derived from `test_name` if omitted |

**Supported properties:**

| `property` value | Symbol | Unit |
|---|---|---|
| `YieldStrength` | Rₑ | MPa or GPa |
| `UpperYieldStrength` | ReH | MPa or GPa |
| `LowerYieldStrength` | ReL | MPa or GPa |
| `TensileStrength` | Rm | MPa or GPa |
| `ProofStrength` | Rp | MPa or GPa |
| `PercentageElongationAfterFracture` | A | % |
| `PercentagePermanentElongation` | Ag | % |
| `PercentageReductionOfArea` | Z | % |

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example (start here) |
| `docs/1_tensile_test_workflow.ipynb` | Step-by-step notebook |
| `simplified/schema.simplified.json` | Input field reference |
| `simplified/transform.jsonata` | Converts your input to the structured format |
| `specs/schema.oold.yaml` | Full schema definition |
| `specs/shape.ttl` | SHACL validation rules (tensile-test additions) |

SHACL validation loads two shape files: the tensile-test shape above plus
`characterization/step/PMDCo/specs/shape.ttl`, mirroring the `$ref` base at
the schema level.

---

## For the curious: how this maps to the ontology

<details>
<summary>Show the RDF graph pattern</summary>

```text
TensileTest  (tto:TensileTest)
  rdfs:label ──────────────────────────────────── test name
  rdfs:comment ────────────────────────────────── description  (optional)
  has_specified_input  (OBI_0000293) ───────────► Specimen IRI
  preceded_by          (BFO_0000062) ───────────► Assay IRI  [× 0..N]
  has_process_condition (PMD_0000016) ──────────► ProcessCondition (PMD_0000013)  [× 0..N]
    rdfs:label    "Test Standard" / "Strain Rate" / "Temperature"
    qudt:value    xsd:double
    qudt:hasUnit  unit string
  has_specified_output (OBI_0000299) ───────────► MeasurementResult  [× 0..N]
    a  tto:YieldStrength | tto:TensileStrength | …
    OBI_0001937   xsd:double  (numeric value)
    IAO_0000039   uqudt:MegaPascal | uqudt:PERCENT | …  (unit IRI)
```

The key difference from the manufacturing step schema is in the outputs:

- Manufacturing step: outputs are **external material IRIs** (the produced
  materials exist independently in the knowledge graph).
- Tensile test: outputs are **embedded measurement result nodes** (created by
  the test, typed to TTO classes, carrying value + unit).

Both use `OBI_0000299` (`has_specified_output`) as the connecting predicate,
which is correct in both cases.

</details>

---

## Further reading

- [Characterization Step (PMDCo)](../../step/PMDCo/README.md): the base schema this one extends
- [TTO application ontology](https://github.com/materialdigital/application-ontologies/tree/main/tensile_test_ontology_TTO)
- [PMDCo core-ontology patterns](https://github.com/materialdigital/core-ontology/tree/main/patterns)
- [OO-LD primer](../../../../docs/2_oold-primer.md): how the schema format works
- [Schema format reference](../../../../docs/3_schema-format.md): folder structure and naming conventions
