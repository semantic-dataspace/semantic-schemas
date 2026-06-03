# Schema Catalog

All schemas currently available in this repository.

| Domain | Ontology | What it records | Folder |
|---|---|---|---|
| Chemical Composition | PMDCo | Element fractions of a material (mass%, vol%, or mol%) | [schemas/chemical-composition/PMDCo/](schemas/chemical-composition/PMDCo/) |
| Chemical Composition | BWMD | Element weight fractions with min/max ranges | [schemas/chemical-composition/BWMD/](schemas/chemical-composition/BWMD/) |
| Specimen | PMDCo | A physical specimen with its name, mass, abstract material identity (PMDCo duality), and optional link to the semi-finished product it was cut from (PROV-O) | [schemas/specimen/PMDCo/](schemas/specimen/PMDCo/) |
| Expertise | VIVO | A person's research areas and instrument experience, using VIVO Core predicates | [schemas/expertise/VIVO/](schemas/expertise/VIVO/) |
| Expertise | schema.org | ~~Deprecated — use Expertise (VIVO) instead~~ | [schemas/expertise/schema.org/](schemas/expertise/schema.org/) |
| Measurement Device | PMDCo/OBI | A measurement or characterization instrument: name, manufacturer, model, serial number, calibration date | [schemas/measurement-device/PMDCo/](schemas/measurement-device/PMDCo/) |
| Manufacturing Generic | PMDCo | A single manufacturing process step: inputs, outputs, process chain position, and quantitative conditions | [schemas/manufacturing/generic/PMDCo/](schemas/manufacturing/generic/PMDCo/) |
| Characterization Generic | PMDCo | Generic base for characterization records (measurements, tests, analyses); extend this to add domain-specific result fields | [schemas/characterization/generic/PMDCo/](schemas/characterization/generic/PMDCo/) |
| Tensile Test | TTO | Uniaxial tensile test with measured properties (yield strength, tensile strength, elongation, …); standalone schema typed to TTO numeric class IRIs | [schemas/characterization/tensile-test/TTO/](schemas/characterization/tensile-test/TTO/) |
| Tensile Test | PMDCo | Uniaxial tensile test using the PMDCo measurement pattern; result properties identified by free-text label rather than a fixed vocabulary | [schemas/characterization/tensile-test/PMDCo/](schemas/characterization/tensile-test/PMDCo/) |
| Simulation Generic | PMDCo | Generic base for computational simulation steps (FEM, data-fitting, ML inference); extend this to add domain-specific result fields | [schemas/simulation/generic/PMDCo/](schemas/simulation/generic/PMDCo/) |
| Constitutive Model Calibration | PMDCo | Fitting a flow-curve model (Hockett-Sherby, Swift, Voce, Hollomon, Johnson-Cook) to experimental stress-strain data; extends Simulation Generic | [schemas/simulation/model-calibration/PMDCo/](schemas/simulation/model-calibration/PMDCo/) |
| Mechanical Material Card | PMDCo | Structured dataset collecting elastic constants, discrete mechanical properties, and a fitted constitutive model for FEM use | [schemas/material-card/mechanical/PMDCo/](schemas/material-card/mechanical/PMDCo/) |
| Workflow | OBI | Multi-step workflow spanning manufacturing, characterization, and simulation; each step references its domain-specific schema instance by IRI | [schemas/workflow/OBI/](schemas/workflow/OBI/) |

---

## Domains

| Domain | # Schemas | What it covers |
|---|---|---|
| `chemical-composition` | 2 | Element fractions that characterise a material |
| `specimen` | 1 | Physical specimens with mass and composition |
| `expertise` | 2 | Competency profiles for materials science experts (VIVO active, schema.org deprecated) |
| `measurement-device` | 1 | Physical measurement instruments and their calibration status |
| `manufacturing` | 1 | Generic manufacturing step base (`generic/`) |
| `characterization` | 3 | Generic base (`generic/`) and specialised variants (e.g. `tensile-test/`) |
| `simulation` | 2 | Generic simulation base (`generic/`) and constitutive model calibration (`model-calibration/`) |
| `material-card` | 1 | Structured datasets for FEM material input |
| `workflow` | 1 | Multi-step workflow records |

---

## Domain structure

All three process domains (`characterization/`, `manufacturing/`, `simulation/`) share
the same two-level pattern:

```text
<domain>/
  generic/          ← generic base (no enforced provenance)
    PMDCo/
  <variant>/        ← specialised schemas that extend the generic base
    TTO/   or PMDCo/
```

`generic/` and variant schemas are used when only measurement results need to be
captured. Use `generic/` as a base when adding domain-specific result fields.

For larger-scale data collection, two further schema families are planned but not
yet implemented:

- **`study/`**: groups multiple experiments under one research question, potentially
  crossing domains.
- **`specimen/batch/`**: a batch record for specimens prepared under identical
  conditions, so one provenance entry covers the whole set.

---

*To add a schema, follow [CONTRIBUTING.md](CONTRIBUTING.md) and add a row above.*
