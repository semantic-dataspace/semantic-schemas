# Simulation Step (PMDCo)

Records a **computational simulation step** (numerical analysis, data-driven
model run, or any computer-executed calculation) following the
[Platform MaterialDigital Core Ontology (PMDCo)](https://w3id.org/pmd/co/) and
the [OBI ComputerSimulation](http://purl.obolibrary.org/obo/OBI_0000471) class.

This is the **generic base** for all simulation schemas in this repository.
Specialised schemas (such as `model-calibration/PMDCo/`) extend it via JSON
Schema `$ref` to add domain-specific fields.

---

## Quick start

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "step_name":   "FEM stress analysis run 1",
  "inputs":      ["https://example.org/material-cards/316L-hockett-sherby-v1"],
  "outputs":     ["https://example.org/simulation-results/fem-stress-316L-run-1"],
  "preceded_by": ["https://example.org/simulations/model-calibration-316L-batch-1"],
  "conditions": [
    { "name": "Solver",    "unit": "Abaqus/Standard 2023" },
    { "name": "Mesh Size", "value": 0.5, "unit": "mm" }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `step_name` | yes | Human-readable name for this simulation step |
| `description` | no | Free-text description |
| `inputs` | no | IRIs of datasets or materials consumed |
| `outputs` | no | IRIs of datasets or results produced |
| `preceded_by` | no | IRIs of immediately preceding steps |
| `conditions` | no | Quantitative simulation parameters (name, value, unit) |
| `step_id` | no | Custom IRI slug; auto-derived from `step_name` if omitted |

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example |
| `specs/schema.simplified.json` | Input field reference |
| `specs/transform.simplified.jsonata` | Converts your input to the structured format |
| `specs/schema.oold.yaml` | Full schema definition |
| `specs/shape.ttl` | SHACL validation rules |

For a full worked example with a notebook, see
[`simulation/model-calibration/PMDCo/`](../../model-calibration/PMDCo/README.md).

---

## For the curious: how this maps to the ontology

```text
ComputerSimulation  (obi:OBI_0000471)
  rdfs:label ─────────────────────────── name string
  rdfs:comment ───────────────────────── description string  (optional)
  has_specified_input  (OBI_0000293) ──► Dataset/Material IRI  [× 0..N]
  has_specified_output (OBI_0000299) ──► Dataset/Result IRI    [× 0..N]
  preceded_by          (BFO_0000062) ──► Process IRI  [× 0..N]
  has_process_condition (PMD_0000016) ─► ProcessCondition (PMD_0000013)  [× 0..N]
    rdfs:label   parameter name
    qudt:value   xsd:double
    qudt:hasUnit unit string
```

`obi:ComputerSimulation` (`OBI_0000471`) is the OBI class for any planned process
executed by a computer.  It covers FEM analyses, constitutive model calibrations,
data-fitting routines, and machine-learning inference.

---

## Further reading

- [Model Calibration (PMDCo)](../../model-calibration/PMDCo/README.md): a worked specialisation of this schema
- [OO-LD primer](../../../../docs/2_oold-primer.md): how the schema format works
- [Schema format reference](../../../../docs/3_schema-format.md): folder and naming conventions
