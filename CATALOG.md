# Schema Catalog

All schemas currently available in this repository.

| Domain | Ontology | What it records | Folder |
|---|---|---|---|
| Chemical Composition | PMDCo | Element fractions of a material (mass%, vol%, or mol%) | [schemas/chemical-composition/PMDCo/](schemas/chemical-composition/PMDCo/) |
| Chemical Composition | BWMD | Element weight fractions with min/max ranges | [schemas/chemical-composition/BWMD/](schemas/chemical-composition/BWMD/) |
| Specimen | PMDCo | A physical specimen with its mass and chemical composition | [schemas/specimen/PMDCo/](schemas/specimen/PMDCo/) |
| Expertise | — | A person's areas of expertise in materials science | [schemas/expertise/](schemas/expertise/) |
| Manufacturing Step | PMDCo | A single manufacturing process step: inputs, outputs, process chain position, and quantitative conditions | [schemas/manufacturing/step/PMDCo/](schemas/manufacturing/step/PMDCo/) |
| Characterization Step | PMDCo | Generic base for characterization processes (measurements, tests, analyses) — extend this to add domain-specific result fields | [schemas/characterization/step/PMDCo/](schemas/characterization/step/PMDCo/) |
| Tensile Test | TTO | Uniaxial tensile test with measured properties (yield strength, tensile strength, elongation, …) — extends Characterization Step | [schemas/characterization/tensile-test/TTO/](schemas/characterization/tensile-test/TTO/) |
| Simulation Step | PMDCo | Generic base for computational simulation steps (FEM, data-fitting, ML inference) — extend this to add domain-specific result fields | [schemas/simulation/step/PMDCo/](schemas/simulation/step/PMDCo/) |
| Constitutive Model Calibration | PMDCo | Fitting a flow-curve model (Hockett-Sherby, Swift, Voce, Hollomon, Johnson-Cook) to experimental stress-strain data — extends Simulation Step | [schemas/simulation/model-calibration/PMDCo/](schemas/simulation/model-calibration/PMDCo/) |
| Mechanical Material Card | PMDCo | Structured dataset collecting elastic constants, discrete mechanical properties, and a fitted constitutive model for FEM use | [schemas/material-card/mechanical/PMDCo/](schemas/material-card/mechanical/PMDCo/) |
| Cross-Domain Workflow | PMDCo | Multi-step workflow spanning manufacturing, characterization, and simulation; each step references its domain-specific schema instance by IRI | [schemas/workflow/PMDCo/](schemas/workflow/PMDCo/) |

---

## Domains

| Domain | # Schemas | What it covers |
|---|---|---|
| `chemical-composition` | 2 | Element fractions that characterise a material |
| `specimen` | 1 | Physical specimens with mass and composition |
| `expertise` | 1 | Competency profiles for materials science experts |
| `manufacturing` | 1 | Manufacturing process steps |
| `characterization` | 2 | Characterization steps and specialised test schemas |
| `simulation` | 2 | Computational simulation steps and constitutive model calibration |
| `material-card` | 1 | Structured datasets for FEM material input |
| `workflow` | 1 | Cross-domain multi-step workflow records |

---

## Domain structure note

Domains that contain both a generic base schema and specialised variants use
one extra level of nesting (`domain/specialisation/Ontology/`). Within such a
domain, a folder that sits directly at `domain/Ontology/` is the generic base;
named subfolders (e.g. `domain/sintering/Ontology/`) are specialised variants.
See [docs/schema-format.md](docs/schema-format.md) for the full convention.

---

*To add a schema, follow [CONTRIBUTING.md](CONTRIBUTING.md) and add a row above.*
