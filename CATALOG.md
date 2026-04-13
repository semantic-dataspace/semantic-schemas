# Schema Catalog

All schemas currently available in this repository.

| Domain | Ontology | What it records | Folder |
|---|---|---|---|
| Chemical Composition | PMDCo | Element fractions of a material (mass%, vol%, or mol%) | [schemas/chemical-composition/PMDCo/](schemas/chemical-composition/PMDCo/) |
| Chemical Composition | BWMD | Element weight fractions with min/max ranges | [schemas/chemical-composition/BWMD/](schemas/chemical-composition/BWMD/) |
| Specimen | PMDCo | A physical specimen with its mass and chemical composition | [schemas/specimen/PMDCo/](schemas/specimen/PMDCo/) |
| Expertise | — | A person's areas of expertise in materials science | [schemas/expertise/](schemas/expertise/) |
| Measurement Device | PMDCo/OBI | A measurement or characterization instrument: name, manufacturer, model, serial number, calibration date | [schemas/measurement-device/PMDCo/](schemas/measurement-device/PMDCo/) |
| Manufacturing Step | PMDCo | A single manufacturing process step: inputs, outputs, process chain position, and quantitative conditions | [schemas/manufacturing/step/base/PMDCo/](schemas/manufacturing/step/base/PMDCo/) |
| Characterization Step (base) | PMDCo | Generic base for characterization processes (measurements, tests, analyses); extend this to add domain-specific result fields | [schemas/characterization/step/base/PMDCo/](schemas/characterization/step/base/PMDCo/) |
| Characterization Process | PMDCo | Guided intake for a characterization experiment: enforces operator (expert), measurement device, and specimen as required provenance fields | [schemas/characterization/process/PMDCo/](schemas/characterization/process/PMDCo/) |
| Tensile Test | TTO | Uniaxial tensile test with measured properties (yield strength, tensile strength, elongation, …); extends Characterization Step | [schemas/characterization/step/tensile-test/TTO/](schemas/characterization/step/tensile-test/TTO/) |
| Simulation Step | PMDCo | Generic base for computational simulation steps (FEM, data-fitting, ML inference); extend this to add domain-specific result fields | [schemas/simulation/step/base/PMDCo/](schemas/simulation/step/base/PMDCo/) |
| Constitutive Model Calibration | PMDCo | Fitting a flow-curve model (Hockett-Sherby, Swift, Voce, Hollomon, Johnson-Cook) to experimental stress-strain data; extends Simulation Step | [schemas/simulation/step/model-calibration/PMDCo/](schemas/simulation/step/model-calibration/PMDCo/) |
| Mechanical Material Card | PMDCo | Structured dataset collecting elastic constants, discrete mechanical properties, and a fitted constitutive model for FEM use | [schemas/material-card/mechanical/PMDCo/](schemas/material-card/mechanical/PMDCo/) |
| Workflow | PMDCo | Multi-step workflow spanning manufacturing, characterization, and simulation; each step references its domain-specific schema instance by IRI | [schemas/workflow/PMDCo/](schemas/workflow/PMDCo/) |
| Material Card Workflow Template | — | Single-input template that orchestrates all six schemas for a complete tensile-test-to-FEM-material-card workflow; no data modelling decisions required | [schemas/workflow/templates/material-card/PMDCo/](schemas/workflow/templates/material-card/PMDCo/) |

---

## Domains

| Domain | # Schemas | What it covers |
|---|---|---|
| `chemical-composition` | 2 | Element fractions that characterise a material |
| `specimen` | 1 | Physical specimens with mass and composition |
| `expertise` | 1 | Competency profiles for materials science experts |
| `measurement-device` | 1 | Physical measurement instruments and their calibration status |
| `manufacturing` | 1 | Manufacturing process steps (base schema under `step/base/`) |
| `characterization` | 3 | Guided process intake (process/), generic step base (step/base/), and specialised step variants (step/tensile-test/) |
| `simulation` | 2 | Computational simulation steps and constitutive model calibration (both under `step/`) |
| `material-card` | 1 | Structured datasets for FEM material input |
| `workflow` | 1 + 1 template | Multi-step workflow records; `templates/material-card/` for the fill-in-one-form approach |

---

## Domain structure

The `characterization/` domain uses two levels of nesting:

```text
characterization/
  process/          ← guided intake (operator + device + specimen enforced)
    PMDCo/
  step/             ← detailed step schemas
    base/           ← generic OBI Assay base
      PMDCo/
    tensile-test/   ← specialised variant
      TTO/
```

`process/` is the recommended entry point for end users recording experiments.
`step/` schemas are used when detailed measurement results need to be captured.

The `manufacturing/` and `simulation/` domains follow the same `step/base/` pattern
for their generic base schemas:

```text
manufacturing/
  step/
    base/         ← generic ManufacturingProcess base
      PMDCo/

simulation/
  step/
    base/         ← generic ComputerSimulation base
      PMDCo/
    model-calibration/   ← specialised variant: flow-curve fitting
      PMDCo/
```

The `process/` template layer can be extended to `manufacturing/process/` and
`simulation/process/` in the future, following the same pattern as `characterization/process/`.

---

*To add a schema, follow [CONTRIBUTING.md](CONTRIBUTING.md) and add a row above.*
