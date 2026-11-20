# Changelog: Heat Treatment Process (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `…/heat-treatment/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [0.2.0] - 2026-10-15

### Added

Initial release of the standalone heat-treatment OO-LD schema.

- Root class `pmdco:PMD_0000833` (ManufacturingProcess) with optional
  `dsmsht:<Subtype>` second type derived from `heat_treatment_type` field.
- `heat_treatment_type` enum (11 types: Solution Treatment, Artificial Aging,
  Natural Aging, Full Annealing, Partial Annealing, Recrystallization Annealing,
  Stress Relief Annealing, Normalizing, Tempering, Homogenization, Quenching).
- `has_process_attribute` array: PMDCo ParameterSpecification nodes
  (`PMD_0000013`) linked via `PMD_0000009`. Each parameter uses `parameter_type`
  (IRI from process-parameter vocabulary service stored as `rdf:type`) and
  `parameter_unit` (IRI from measurement-unit vocabulary service via `qudt:hasUnit`).
- `has_specified_input`, `has_specified_output` (specimen / material / billet
  KItem links via `obi:OBI_0000293` / `obi:OBI_0000299`).
- `preceded_by` (BFO_0000062) for process chain ordering.
- `dsmsht:` namespace (`https://w3id.org/dsms/heattreatment#`) for
  heat-treatment-specific process and parameter class IRIs.
