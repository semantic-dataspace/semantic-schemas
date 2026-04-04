# Characterization Step (PMDCo)

Records a **single characterization step** (a measurement, mechanical test, or
analysis) following the
[Platform MaterialDigital Core Ontology (PMDCo)](https://w3id.org/pmd/co/) and
the [OBI Assay](http://purl.obolibrary.org/obo/OBI_0000070) class.

This is the **generic base** for all characterization schemas in this repository.
Specialised schemas (such as `tensile-test/TTO/`) extend it via JSON Schema
`$ref` to add domain-specific result fields, just as `specimen/PMDCo/` extends
`chemical-composition/PMDCo/`.

---

## Quick start

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "step_name": "Tensile test specimen 1",
  "inputs":    ["https://example.org/specimens/316L-tensile-bar-1"],
  "conditions": [
    { "name": "Test Standard", "unit": "ISO 6892-1" },
    { "name": "Strain Rate",   "value": 0.00025, "unit": "1/s" }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `step_name` | yes | Human-readable name for this step |
| `description` | no | Free-text description |
| `inputs` | no | IRIs of specimens or materials being characterised |
| `preceded_by` | no | IRIs of steps that come immediately before this one |
| `conditions` | no | Quantitative test conditions (name, value, unit) |
| `step_id` | no | Custom IRI slug; auto-derived from `step_name` if omitted |

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example |
| `simplified/schema.simplified.json` | Input field reference |
| `simplified/transform.jsonata` | Converts your input to the structured format |
| `specs/schema.oold.yaml` | Full schema definition |
| `specs/shape.ttl` | SHACL validation rules |

For a full worked example with a notebook, see
[`characterization/tensile-test/TTO/`](../../tensile-test/TTO/README.md).

---

## For the curious: how this maps to the ontology

```text
Assay  (obi:OBI_0000070)
  rdfs:label ───────────────────────�� name string
  rdfs:comment ────────────────────── description string  (optional)
  has_specified_input (OBI_0000293) ► Specimen/Material IRI  [× 0..N]
  preceded_by         (BFO_0000062) ► Assay IRI  [× 0..N]
  has_process_condition (PMD_0000016) ► ProcessCondition (PMD_0000013)  [× 0..N]
    rdfs:label   condition name
    qudt:value   xsd:double
    qudt:hasUnit unit string
```

`obi:Assay` (`OBI_0000070`) is the OBI class for any planned process that
produces a measurement as output. It is the common superclass of tensile tests,
hardness measurements, microscopy sessions, and so on.

---

## Further reading

- [Tensile Test (TTO)](../../tensile-test/TTO/README.md): a worked specialisation of this schema
- [OO-LD primer](../../../../docs/oold-primer.md): how the schema format works
- [Schema format reference](../../../../docs/schema-format.md): folder and naming conventions
