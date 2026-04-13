# Changelog — Constitutive Model Calibration (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR** — backwards-compatible additions (new optional fields)
- **PATCH** — corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `…/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [2.0.0] — 2026-04-13

### Breaking changes

- **Folder moved** from `simulation/model-calibration/PMDCo/` to
  `simulation/step/model-calibration/PMDCo/` (repository-level restructuring to
  place all simulation step variants under `simulation/step/`; no field or graph
  changes).
- `x-schema-id` updated from
  `…/simulation/model-calibration/PMDCo/` to
  `…/simulation/step/model-calibration/PMDCo/`.
- Base schema `$ref` updated from `…/simulation/step/PMDCo/` to
  `…/simulation/step/base/PMDCo/` (following the base schema rename to v2.0.0).
- `conforms_to` IRI in all generated records changes accordingly.

### Migration

Update `conforms_to` IRI filters in SPARQL queries:

```sparql
# Old
FILTER(STR(?conformsTo) = "…/simulation/model-calibration/PMDCo/#v1.0.0")

# New
FILTER(STR(?conformsTo) = "…/simulation/step/model-calibration/PMDCo/#v2.0.0")
```

---

## [1.0.0] — 2026-04-09

- Initial release.
- Constitutive model calibration schema extending `simulation/step/PMDCo/`.
- `model_type` enum: Hockett-Sherby, Swift, Voce, Hollomon, Johnson-Cook.
- `calibrated_parameters` array for named fitted parameter values.
