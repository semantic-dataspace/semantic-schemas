# Changelog: Microstructure Characterization (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `…/microstructure/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [0.1.0] - 2026-10-15

### Added

Initial release.

- `obi:Assay` (OBI_0000070) schema for microstructure characterization
  experiments (SEM, EBSD, LOM, TEM, SAXS, …).
- Inherits from `process-step/PMDCo` via `allOf` for shared fields (`label`,
  `date`, `has_specified_input`, `has_specified_output`, `preceded_by`,
  `operator`).
- `technique` enum: SEM, EBSD, LOM, TEM, SAXS, XRD, Raman Spectroscopy,
  Atom Probe Tomography, Other.
- `measurement_device` field: links to a measurement-device KItem via
  `chameo:usesInstrument`.
- Instrument-specific numeric conditions via `has_process_attribute`
  (PMDCo ParameterSpecification, PMD_0000013):
  - Magnification, Accelerating Voltage (kV), Area Analysed (µm²),
    Etching / Preparation Method as optional parameters.
- `chameo:` namespace (`https://w3id.org/emmo/domain/characterisation-methodology/chameo#`)
  for instrument linkage.
