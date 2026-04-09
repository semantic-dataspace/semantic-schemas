# Cross-Domain Workflow (PMDCo)

Records a **multi-step workflow** that spans different process domains
(manufacturing, characterization, simulation, data management) in a single
RDF graph node.

Each step references its detailed schema instance by IRI so the workflow
can combine PMDCo manufacturing steps, OBI assays, TTO tensile tests, and
OBI computer simulations without coupling any of them to each other.

---

## Quick start

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "workflow_name": "QA-to-FEM material card workflow — 316L batch 1",
  "steps": [
    {
      "label":        "Material Production — 316L batch 1",
      "step_type":    "pmdco:PMD_0000029",
      "instance_iri": "https://example.org/manufacturing/316L-production-batch-1"
    },
    {
      "label":        "Tensile Test — 316L batch 1 QA",
      "step_type":    "obi:0000070",
      "instance_iri": "https://example.org/characterization/tensile-test-316L-batch-1"
    },
    {
      "label":        "Hockett-Sherby Calibration — 316L batch 1",
      "step_type":    "obi:0000471",
      "instance_iri": "https://example.org/simulations/hs-calibration-316L-batch-1"
    },
    {
      "label":       "FEM Material Card Export — LS-Dyna / Abaqus",
      "description": "Export calibrated parameters as LS-Dyna *MAT_036 and Abaqus *PLASTIC material cards."
    }
  ]
}
```

Steps are linked in sequence automatically. Use explicit `preceded_by` arrays
to express branching or merging.

| Field | Required | Description |
|---|---|---|
| `workflow_name` | yes | Human-readable workflow name |
| `description` | no | Free-text description of the overall workflow |
| `steps[].label` | yes | Step name |
| `steps[].step_type` | no | Ontology class CURIE for this step |
| `steps[].description` | no | Free-text step description |
| `steps[].instance_iri` | no | IRI of the detailed step instance in the knowledge graph |
| `steps[].preceded_by` | no | Step IDs of direct predecessors (auto-derived from array order if omitted) |
| `steps[].conditions` | no | Inline quantitative parameters for this step |
| `workflow_id` | no | Custom IRI slug; auto-derived from `workflow_name` if omitted |

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit 4-step QA-to-FEM example |
| `docs/3_workflow_cross_domain.ipynb` | Step-by-step pedagogic notebook |
| `specs/schema.simplified.json` | Input field reference |
| `specs/transform.simplified.jsonata` | Converts your input to the structured format |
| `specs/schema.oold.yaml` | Full schema definition |
| `specs/shape.ttl` | SHACL validation rules |

---

## Cross-domain step types

| `step_type` value | Domain | Schema |
|---|---|---|
| `pmdco:PMD_0000029` | Manufacturing | `manufacturing/step/PMDCo/` |
| `obi:0000070` | Characterization | `characterization/step/PMDCo/` |
| `obi:0000471` | Simulation | `simulation/step/PMDCo/` |
| *(omitted)* | Generic | `bfo:BFO_0000015` (plain process) |

Mixing step types in a single workflow is intentional and supported. The
workflow schema deliberately uses the domain-neutral `bfo:BFO_0000015` as its
root class so it does not privilege any one ontology.

---

## For the curious: how this maps to the ontology

```text
Process  (bfo:BFO_0000015)        # the workflow container
  rdfs:label   workflow name
  bfo:BFO_0000051 (has_part)
    ► Step 1  (typed to domain class, e.g. pmdco:ManufacturingProcess)
        rdfs:label   step name
        dcterms:references ──────► detailed instance IRI  (optional)
    ► Step 2  (obi:Assay, obi:ComputerSimulation, …)
        rdfs:label   step name
        bfo:BFO_0000062 (preceded_by) ──► Step 1
        dcterms:references ──────► detailed instance IRI  (optional)
    ► Step N
        …
```

`instance_iri` (mapped to `dcterms:references`) is the bridge between the
lightweight workflow record and the detailed step descriptions in the graph.
A consumer can dereference it to retrieve the full step, including its
characterization results or calibrated model parameters.

---

## Further reading

- [Manufacturing Step (PMDCo)](../../manufacturing/step/PMDCo/README.md)
- [Characterization Step (PMDCo)](../../characterization/step/PMDCo/README.md)
- [Tensile Test (TTO)](../../characterization/tensile-test/TTO/README.md)
- [Simulation Step (PMDCo)](../../simulation/step/PMDCo/README.md)
- [Constitutive Model Calibration (PMDCo)](../../simulation/model-calibration/PMDCo/README.md)
- [Mechanical Material Card (PMDCo)](../../material-card/mechanical/PMDCo/README.md)
- [OO-LD primer](../../../docs/2_oold-primer.md): how the schema format works
