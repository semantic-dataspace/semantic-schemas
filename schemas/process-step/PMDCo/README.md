# Process Step (PMDCo)

Defines the **base pattern** that all workflow step schemas must satisfy.
Step-specific schemas (tensile test, simulation, manufacturing, etc.) extend
this schema using JSON Schema `allOf + $ref` composition.

Do not use this schema directly to record data; use one of the step-specific
schemas instead.  This schema is not listed in the playground; it exists solely
as a shared base for `$ref` composition.

<table>
<tr><td><strong>Version</strong></td><td><code>0.3.0</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>OBI PlannedProcess (<code>obo:OBI_0000070</code>)</td></tr>
<tr><td><strong>Extends</strong></td><td>—</td></tr>
<tr><td><strong>Includes</strong></td><td>—</td></tr>
<tr><td><strong>Transformers</strong></td><td>—</td></tr>
</table>

---

## Fields provided to all step schemas

| Field | Required | Description |
|---|---|---|
| `label` | yes | Human-readable step name |
| `id` | yes | IRI identifier for this step instance |
| `notes` | no | Free-text observations or execution log |
| `date` | no | Execution date/time (ISO 8601, `xsd:dateTime`) |
| `has_specified_input` | no | Material entities consumed or observed (specimen/dataset IRIs) |
| `operator` | no | Person who performed the step (`prov:wasAssociatedWith`) |
| `instrument` | no | Physical device used (`schema:instrument`) |

---

## How to compose with this schema

```yaml
allOf:
  - $ref: "../../../../process-step/PMDCo/specs/schema.oold.yaml"

x-process-step:
  category: characterization   # characterization | simulation | manufacturing | preparation | generic
```

`resolveSchemaRefs()` in the webform adapter merges the base `@context`,
`properties`, and `required` arrays before the form is rendered.  Properties
in the step-specific schema override base properties of the same name.

---

## How this maps to the ontology

```text
obo:OBI_0000070  (PlannedProcess)
  rdfs:label              step name
  rdfs:comment            notes  (optional)
  dcterms:date            execution date  (optional, xsd:dateTime)
  obi:OBI_0000293       ─► input IRIs  (has_specified_input)
  prov:wasAssociatedWith ─► operator IRI  (optional)
  schema:instrument      ─► device IRI  (optional)
```

---

## Schemas that extend this base

- [Tensile Test (PMDCo)](../../characterization/tensile-test/PMDCo/README.md)
- [Tensile Test (TTO)](../../characterization/tensile-test/TTO/README.md)
- [Characterization Generic (PMDCo)](../../characterization/generic/PMDCo/README.md)
- [Manufacturing Generic (PMDCo)](../../manufacturing/generic/PMDCo/README.md)
- [Simulation Generic (PMDCo)](../../simulation/generic/PMDCo/README.md)
- [Constitutive Model Calibration (PMDCo)](../../simulation/model-calibration/PMDCo/README.md)

## Related

- [Workflow (OBI)](../../workflow/OBI/README.md): ordered container of step IRIs
