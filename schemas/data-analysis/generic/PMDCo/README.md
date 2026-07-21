# Data Analysis Generic (PMDCo)

Records a **data analysis step** (transformation of one or more datasets into
derived results) following the
[Ontology for Biomedical Investigations (OBI)](http://purl.obolibrary.org/obo/obi.owl)
`DataTransformation` class (`OBI_0200000`).

<table>
<tr><td><strong>Version</strong></td><td><code>0.1.0</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>OBI DataTransformation (<code>obo:OBI_0200000</code>)</td></tr>
<tr><td><strong>Extends</strong></td><td><a href="../../process-step/PMDCo/README.md">process-step/PMDCo</a></td></tr>
<tr><td><strong>Includes</strong></td><td>—</td></tr>
<tr><td><strong>Transformers</strong></td><td>—</td></tr>
</table>

Specialised analysis schemas can extend this one via JSON Schema `$ref` + `allOf`
to add domain-specific result fields (e.g. yield-strength evaluation, forming limit
curve fitting).

---

## Quick start

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "step_name": "Yield strength evaluation, 316L batch 1",
  "description": "Automated evaluation of 0.2 % yield strength from tensile test force-displacement data.",
  "inputs": ["https://example.org/datasets/tensile-raw-316L-batch-1"],
  "outputs": ["https://example.org/datasets/yield-strength-316L-batch-1"],
  "operator": "https://example.org/persons/doe-jane"
}
```

| Field | Required | Description |
|---|---|---|
| `step_name` | yes | Human-readable name for this analysis step |
| `description` | no | Free-text description of the analysis goal and method |
| `inputs` | yes (≥ 1) | IRIs of dataset k-items consumed as input |
| `outputs` | no | IRIs of dataset k-items produced as output |
| `operator` | no | IRI of the analyst who performed or supervised this step |

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example |
| `specs/schema.oold.yaml` | Full OO-LD schema definition |
| `specs/shape.ttl` | SHACL validation rules |

---

## For the curious: how this maps to the ontology

```text
obi:DataTransformation  (OBI_0200000)
  rdfs:label                              analysis name
  rdfs:comment                            description  (optional)
  has_specified_input  (OBI_0000293) ──► Dataset IRI  [× 1..N]
  has_specified_output (OBI_0000299) ──► Dataset IRI  [× 0..N]
  prov:wasAssociatedWith               ─► Analyst IRI  (optional)
```

`obi:DataTransformation` is the OBI class for any planned process that transforms
data as both its input and output. It sits beneath `obi:PlannedProcess`
(`OBI_0000070`), which is the class used by the `process-step/PMDCo` base schema.

---

## Further reading

- [Usage guide](../../../../docs/6_usage-guide.md): how to convert `example.input.json` to RDF and validate it with SHACL
- [OO-LD primer](../../../../docs/2_oold-primer.md): how the schema format works

---

## Related schemas

- [Process Step (PMDCo)](../../process-step/PMDCo/README.md): base pattern extended by this schema
- [Dataset Generic (DCAT)](../../dataset/generic/DCAT/README.md): schema for the input and output datasets
- [Characterization Generic (PMDCo)](../../characterization/generic/PMDCo/README.md): analogous pattern for measurement steps
- [Workflow (OBI)](../../workflow/OBI/README.md): ordered container of step IRIs
