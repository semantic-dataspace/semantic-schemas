# Changelog: DSC Dataset (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/).

---

## [0.1.0] - 2026-10-01

### Added

- Initial schema for DSC heat-flow datasets.
- Captures NETZSCH Proteus instrument header fields: sample name/mass, instrument
  model/manufacturer, laboratory, operator, measurement datetime, heating rate,
  temperature range, purge gas, crucible type, calibration references.
- Column IRI specifications for semantic annotation of timeseries columns.
- Auto-extracted scalar results from `#*RESULTS` header lines.
