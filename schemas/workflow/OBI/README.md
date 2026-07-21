# Workflow (OBI)

Records a **named, ordered sequence of process step IRIs** that together form
an experiment or campaign.  Each step is recorded independently using an
`x-process-step` schema (tensile test, simulation, sample preparation, etc.)
and referenced here by IRI.  The workflow node provides the human-readable
envelope and provenance context; the full process graph is reconstructed by
following the step IRIs.

<table>
<tr><td><strong>Version</strong></td><td><code>0.2.1</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>OBI AnalyticProtocol (<code>obo:OBI_0000272</code>)</td></tr>
<tr><td><strong>Extends</strong></td><td>—</td></tr>
<tr><td><strong>Includes</strong></td><td>—</td></tr>
<tr><td><strong>Transformers</strong></td><td>—</td></tr>
</table>

Steps are linked as an ordered RDF list via `bfo:BFO_0000051` (`has_part`).
Recording each step separately before creating the workflow record lets any
step schema be reused across workflows without duplication.

---

## Quick start

1. Record each process step with the appropriate schema
   (e.g. `characterization/tensile-test/PMDCo/`).
2. Note the IRI assigned to each step instance.
3. Fill in this form, pasting the step IRIs into the **Process Steps** list.

```json
{
  "type": "obo:OBI_0000272",
  "id": "workflow-316L-batch1",
  "label": "QA-to-FEM workflow: 316L batch 1",
  "description": "Full characterisation and model calibration campaign for 316L batch 1.",
  "responsible": "https://example.org/person/jane-doe",
  "steps": [
    "https://example.org/manufacturing/316L-production-batch-1",
    "https://example.org/characterization/tensile-test-316L-batch-1",
    "https://example.org/simulation/hs-calibration-316L-batch-1"
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `label` | yes | Human-readable workflow name |
| `description` | no | Free-text summary of the workflow goal and context |
| `responsible` | no | IRI of the person accountable for this workflow |
| `steps` | yes (≥ 1) | Ordered list of process step IRIs |

---

## Files in this folder

| File | Purpose |
|---|---|
| `specs/schema.oold.yaml` | Full OO-LD schema definition |

---

## How this maps to the ontology

```text
obo:OBI_0000272  (AnalyticProtocol)
  rdfs:label         workflow name
  rdfs:comment       description  (optional)
  dcterms:creator  ─► responsible person IRI  (optional)
  bfo:BFO_0000051  ─► step IRI  [ordered list, × 1..N]
    each IRI resolves to a process instance recorded with an x-process-step schema
```

The `steps` list is serialised as an RDF ordered list (`@container: @list`)
so consumers can reconstruct the intended execution sequence from the graph
without relying on blank-node ordering.

---

## Related schemas

- [Process Step (PMDCo)](../../process-step/PMDCo/README.md): base pattern for all workflow steps
- [Tensile Test (PMDCo)](../../characterization/tensile-test/PMDCo/README.md)
- [Tensile Test (TTO)](../../characterization/tensile-test/TTO/README.md)
- [Characterization Generic (PMDCo)](../../characterization/generic/PMDCo/README.md)
- [Manufacturing Generic (PMDCo)](../../manufacturing/generic/PMDCo/README.md)
- [Simulation Generic (PMDCo)](../../simulation/generic/PMDCo/README.md)
- [Constitutive Model Calibration (PMDCo)](../../simulation/model-calibration/PMDCo/README.md)
