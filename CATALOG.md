# Schema Catalog

All schemas currently available in this repository.

| Domain | Ontology | What it records | Folder |
|---|---|---|---|
| Chemical Composition | PMDCo | Element fractions of a material (mass%, vol%, or mol%) | [schemas/chemical-composition/PMDCo/](schemas/chemical-composition/PMDCo/) |
| Chemical Composition | BWMD | Element weight fractions with min/max ranges | [schemas/chemical-composition/BWMD/](schemas/chemical-composition/BWMD/) |
| Specimen | PMDCo | A physical specimen with its mass and chemical composition | [schemas/specimen/PMDCo/](schemas/specimen/PMDCo/) |
| Expertise | — | A person's areas of expertise in materials science | [schemas/expertise/](schemas/expertise/) |
| Measurement Device | PMDCo/OBI | A measurement or characterization instrument: name, manufacturer, model, serial number, calibration date | [schemas/measurement-device/PMDCo/](schemas/measurement-device/PMDCo/) |
| Manufacturing Generic | PMDCo | A single manufacturing process step: inputs, outputs, process chain position, and quantitative conditions | [schemas/manufacturing/generic/PMDCo/](schemas/manufacturing/generic/PMDCo/) |
| Characterization Generic | PMDCo | Generic base for characterization records (measurements, tests, analyses); extend this to add domain-specific result fields | [schemas/characterization/generic/PMDCo/](schemas/characterization/generic/PMDCo/) |
| Characterization Campaign | PMDCo | Guided intake for a characterization experiment: enforces operator (expert), measurement device, and specimen as required provenance fields | [schemas/characterization/campaign/PMDCo/](schemas/characterization/campaign/PMDCo/) |
| Tensile Test | TTO | Uniaxial tensile test with measured properties (yield strength, tensile strength, elongation, …); standalone schema typed to TTO numeric class IRIs | [schemas/characterization/tensile-test/TTO/](schemas/characterization/tensile-test/TTO/) |
| Simulation Generic | PMDCo | Generic base for computational simulation steps (FEM, data-fitting, ML inference); extend this to add domain-specific result fields | [schemas/simulation/generic/PMDCo/](schemas/simulation/generic/PMDCo/) |
| Constitutive Model Calibration | PMDCo | Fitting a flow-curve model (Hockett-Sherby, Swift, Voce, Hollomon, Johnson-Cook) to experimental stress-strain data; extends Simulation Generic | [schemas/simulation/model-calibration/PMDCo/](schemas/simulation/model-calibration/PMDCo/) |
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
| `manufacturing` | 1 | Generic manufacturing step base (`generic/`) |
| `characterization` | 3 | Provenance-enforcing campaign (`campaign/`), generic base (`generic/`), and specialised variants (e.g. `tensile-test/`) |
| `simulation` | 2 | Generic simulation base (`generic/`) and constitutive model calibration (`model-calibration/`) |
| `material-card` | 1 | Structured datasets for FEM material input |
| `workflow` | 1 + 1 template | Multi-step workflow records; `templates/material-card/` for the fill-in-one-form approach |

---

## Domain structure

All three process domains (`characterization/`, `manufacturing/`, `simulation/`) share
the same two-level pattern:

```text
<domain>/
  campaign/         ← guided intake (provenance fields enforced)  [characterization only, for now]
    PMDCo/
  generic/          ← generic base (no enforced provenance)
    PMDCo/
  <variant>/        ← specialised schemas that extend the generic base
    TTO/   or PMDCo/
```

`campaign/` is the recommended entry point when every record must be traceable
(operator + device + specimen required). `generic/` and variant schemas are used
when only measurement results need to be captured.

The `campaign/` pattern can be extended to `manufacturing/campaign/` and
`simulation/campaign/` in the future, following the same pattern as
`characterization/campaign/`.

For larger-scale data collection, two further schema families are planned but not
yet implemented:

- **`study/`** — a campaign-of-campaigns grouping multiple experiments under one
  research question, potentially crossing domains.
- **`specimen/batch/`** — a batch record for specimens prepared under identical
  conditions, so one provenance entry covers the whole set.

---

*To add a schema, follow [CONTRIBUTING.md](CONTRIBUTING.md) and add a row above.*
