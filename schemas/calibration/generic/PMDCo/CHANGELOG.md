# Changelog: Calibration Generic (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/).

---

## [0.1.0] - 2026-10-01

### Added

- Initial schema for `chameo:Calibration` records.
- Fields: `calibration_name`, `calibration_type`, `valid_from`, `valid_until`,
  `measurement_device` (chameo:usesInstrument), `reference_standards`, `conditions`,
  `results` (MeasurementDatum accuracy claims).
- SHACL shape enforcing: label, dcterms:type, schema:validFrom, IRI node kinds.
