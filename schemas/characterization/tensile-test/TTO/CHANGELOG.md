# Changelog — Tensile Test (TTO)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR** — backwards-compatible additions (new optional fields, new conditions)
- **PATCH** — corrections that do not affect the graph structure (typos, description fixes, example updates)

The schema IRI encodes the minor version: `…/TTO/#v<MAJOR>.<MINOR>.0`.

---

## [1.1.0] — 2026-04-10

### Added

- `gauge_length` / `gauge_length_unit` — extensometer gauge length now captured
  as a `pmdco:PMD_0000013` process condition (`Messlänge Standardweg` in Zwick exports).
- `preload` / `preload_unit` — pre-load applied before the test ramp now captured
  as a `pmdco:PMD_0000013` process condition (`Vorkraft` in Zwick exports).
- `test_date` — date and time of the test mapped to `dcterms:date` (typed
  `xsd:dateTime`). The Zwick parser converts the Excel serial-number format
  automatically.
- `obo: <http://purl.obolibrary.org/obo/>` added to the `@context` so OBO
  terms serialise with a readable prefix instead of rdflib's auto-generated
  `ns1`/`ns2` labels.

### Changed

- `ZwickParser` now uses a general `unit_field_map` for unit extraction
  (replaces the hardcoded `strain_rate_label` mechanism). The `strain_rate_label`
  parameter is retained for backwards compatibility.

### Notes

All new fields are optional. Existing graphs produced under v1.0.0 remain valid.

---

## [1.0.0] — initial release

- `tto:TensileTest` node with `rdfs:label`, `dcterms:conformsTo`
- `has_specified_input` linking to specimen IRI
- `has_process_condition` for test standard, strain rate, temperature
- `has_specified_output` for measured properties (yield strength, tensile
  strength, elongation after fracture, reduction of area, …) typed to TTO classes
- `dcat:Dataset` descriptor for time-series columns with TTO class IRIs and
  QUDT unit IRIs per column
- SHACL shape validating the above structure
