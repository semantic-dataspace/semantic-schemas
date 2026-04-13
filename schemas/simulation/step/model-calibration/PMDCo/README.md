# Constitutive Model Calibration (PMDCo)

Records a **constitutive model calibration**: the computational process of
fitting a flow-curve model (Hockett-Sherby, Swift, Voce, Hollomon, or
Johnson-Cook) to experimental stress-strain data.

This schema **extends** [`simulation/step/base/PMDCo/`](../base/PMDCo/README.md)
via JSON Schema `$ref` / `allOf` and adds two specialised fields:

| Added field | Description |
|---|---|
| `model_type` | The constitutive model family (required) |
| `calibrated_parameters` | The fitted model parameters with values and units |

---

## Quick start

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "step_name":  "Hockett-Sherby calibration 316L batch 1",
  "model_type": "Hockett-Sherby",
  "inputs":     ["https://example.org/tensile-tests/316L-batch-1-results"],
  "outputs":    ["https://example.org/material-cards/316L-hockett-sherby-v1"],
  "calibrated_parameters": [
    { "name": "sigma_sat", "value": 780.0, "unit": "MPa" },
    { "name": "sigma_0",   "value": 220.0, "unit": "MPa" },
    { "name": "c",         "value": 12.5 },
    { "name": "n",         "value": 0.68 }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `step_name` | yes | Human-readable name for this calibration run |
| `model_type` | yes | Constitutive model family |
| `description` | no | Free-text description |
| `inputs` | no | IRIs of experimental datasets consumed |
| `outputs` | no | IRIs of material cards / parameter datasets produced |
| `preceded_by` | no | IRIs of immediately preceding steps |
| `conditions` | no | Algorithmic calibration settings (optimiser, strain range, …) |
| `calibrated_parameters` | no | Fitted model parameters (name, value, unit) |
| `step_id` | no | Custom IRI slug; auto-derived from `step_name` if omitted |

### Supported models

| Model | Equation | Parameters |
|---|---|---|
| Hockett-Sherby | σ = σ_sat − (σ_sat − σ_0) · exp(−c · εₚⁿ) | σ_sat, σ_0, c, n |
| Swift | σ = C · (ε_0 + εₚ)ⁿ | C, ε_0, n |
| Voce | σ = σ_sat − (σ_sat − σ_0) · exp(−θ · εₚ) | σ_sat, σ_0, θ |
| Hollomon | σ = K · εₚⁿ | K, n |
| Johnson-Cook | σ = (A + B·εₚⁿ) · (1 + C·ln(ε̇*)) · (1 − T*ᵐ) | A, B, n, C, m |

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example (Hockett-Sherby) |
| `specs/schema.simplified.json` | Input field reference |
| `specs/transform.simplified.jsonata` | Converts your input to the structured format |
| `specs/schema.oold.yaml` | Full schema definition |
| `specs/shape.ttl` | SHACL validation rules (load together with base shape) |

---

## SHACL validation

This schema extends the base simulation step shape. Load both files:

```python
import rdflib, pyshacl

shapes = rdflib.Graph()
shapes.parse("../../step/PMDCo/specs/shape.ttl")
shapes.parse("specs/shape.ttl")

conforms, _, report = pyshacl.validate(
    data_graph,
    shacl_graph=shapes,
    inference="rdfs"
)
```

---

## For the curious: how this maps to the ontology

```text
ComputerSimulation  (obi:OBI_0000471)
  rdfs:label ──────────────────────────── calibration name
  dcterms:type ────────────────────────── model family string (e.g. "Hockett-Sherby")
  has_specified_input  (OBI_0000293) ──► Experimental dataset IRI  [× 0..N]
  has_specified_output (OBI_0000299) ──► Material card IRI  [× 0..N]
                                        ModelParameter node  [× 0..N]  (embedded)
    rdfs:label ─── parameter name/symbol
    qudt:value ─── xsd:double
    qudt:hasUnit ── unit string
  preceded_by (BFO_0000062) ───────────► Process IRI  [× 0..N]
  has_process_condition (PMD_0000016) ─► ProcessCondition (PMD_0000013)  [× 0..N]
    (calibration algorithm settings)
```

The `has_specified_output` property serves double duty: it links to both external
material card IRIs (for the knowledge graph node that will be looked up by
downstream processes) and to embedded parameter nodes (the actual fitted values).
This is consistent with OBI's intent for `OBI_0000299`.

---

## Further reading

- [Simulation Step (PMDCo)](../../step/PMDCo/README.md): the base schema this extends
- [Workflow example](../../../workflow/PMDCo/README.md): the full 4-step QA-to-FEM scenario
- [OO-LD primer](../../../../docs/2_oold-primer.md): how the schema format works
