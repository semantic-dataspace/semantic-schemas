# Material Card Workflow Template

A **fixed-structure template** for running a complete tensile-test-to-FEM-material-card
workflow in one go.

Fill in one dictionary. Run the notebook. You get:

- A connected record of every step (production, test, calibration, material card)
- Traceability: who ran the test, which instrument, which specimen
- FEM solver files ready to use (LS-Dyna, Abaqus)
- A searchable knowledge base you can query later

No data modelling decisions are needed. The template pre-decides the structure;
you supply the values.

---

## What the template covers

| Template section | What it captures | Schema used |
|---|---|---|
| `workflow_name`, `operator_iri`, `specimen_iri`, `material_iri` | Shared identifiers | All steps |
| `device` | Testing machine (name, model, serial, calibration date) | `measurement-device/PMDCo/` |
| `production` | Manufacturing step that produced the batch | `manufacturing/step/base/PMDCo/` |
| `characterization` | Test conditions + measured properties | `characterization/process/PMDCo/` + `characterization/step/tensile-test/TTO/` |
| `calibration` | Constitutive model fit (model family + parameters) | `simulation/step/model-calibration/PMDCo/` |
| `material_card` | Elastic constants (density, E, ν) | `material-card/mechanical/PMDCo/` |

---

## Quick start

Copy [`docs/workflow_template.input.json`](docs/workflow_template.input.json),
fill in your values, and run notebook 4:

```text
docs/1_material_card_with_template.ipynb
```

---

## Files

| File | Purpose |
|---|---|
| `specs/schema.simplified.json` | JSON Schema that validates the full template dictionary |
| `specs/transform.simplified.jsonata` | JSONata transform that routes template sections to sub-schema inputs |
| `docs/workflow_template.input.json` | Ready-to-edit example template |
| `docs/1_material_card_with_template.ipynb` | Step-by-step notebook for all experience levels |

---

## Relationship to other schemas

This template sits above `workflow/PMDCo/` in the same way that
`characterization/process/PMDCo/` sits above `characterization/step/base/PMDCo/`:
it enforces a fixed structure and orchestrates multiple sub-schemas so the user
does not need to make structural decisions.

```text
workflow/
  templates/
    material-card/        ← this schema (fixed structure, six sub-schemas)
  PMDCo/                  ← generic workflow schema
```

The template does not introduce a new RDF class. The graphs it produces are
validated by the six sub-schemas' own SHACL shapes.

---

## Required provenance fields

The `characterization` section is routed through `characterization/process/PMDCo/`,
which enforces three required fields:

| Field | Where it comes from |
|---|---|
| Operator | `operator_iri` (shared context) |
| Device | `device` section (registered in step 1) |
| Specimen | `specimen_iri` (shared context) |

A SHACL validation error is raised if any of the three is missing.

---

## Further reading

- [Notebook 4 (with template)](docs/1_material_card_with_template.ipynb): full walkthrough
- [Notebook 3 (without template)](../../../PMDCo/docs/3_material_card_without_template.ipynb): same scenario, step-by-step
- [Characterization Process (PMDCo)](../../../../characterization/process/PMDCo/README.md): the process template pattern
- [Schema patterns: process/ and template layers](../../../../../docs/4_schema-patterns.md)
