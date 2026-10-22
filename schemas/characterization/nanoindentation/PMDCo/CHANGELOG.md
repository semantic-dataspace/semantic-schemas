# Changelog: Characterization Nanoindentation (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/).

---

## [0.2.0] - 2026-10-01

### Changed

- Test conditions replaced with x-vocabulary dropdowns instead of hardcoded enums.
- `parameter_type` now uses vocabulary IRI, `parameter_label` hidden in form.

---

## [0.1.0] - 2026-07-01

### Added

- Initial nanoindentation characterization schema.
- Fields: step_name, inputs, outputs, conditions array, results (MeasurementDatum).
- CHAMEO chameo:Nanoindentation root class.
