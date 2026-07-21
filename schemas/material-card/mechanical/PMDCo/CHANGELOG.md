# Changelog: Mechanical Material Card (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `.../material-card/mechanical/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [0.3.0] - 2026-07-17

### Changed

- `type` field const and default changed from a single string (`const: "VALUE"`) to a
  single-element array (`const: ["VALUE"]`) to align with JSON-LD, where `@type`
  naturally supports multiple values.
- `x-kitem: {ktypeIds: [...]}` annotations replaced by the flatter `x-ktype: [...]` form on all IRI reference fields.

---

## [0.2.0] - 2026-05-27

### Changed

- **Breaking:** renamed `material_iri` (plain URI field) to `material`
  (`x-kitem`, `ktypeIds: ["material"]`), enabling the playground kitem picker
  to select an existing Material record from the knowledge graph.
- `x-schema-version` bumped to `0.2.0`; `conforms_to` IRI updated accordingly.

---

## [0.1.0] - 2026-05-10

### Added

- Initial release.
- `iao:DataSet` (IAO_0000100) node referenced to a material IRI via
  `dcterms:references`.
- Elastic constants: density (`pmdco:PMD_0000025`), Young's modulus
  (`pmdco:PMD_0000039`), Poisson's ratio (`pmdco:PMD_0000040`); each a
  scalar node with `qudt:value` and `qudt:hasUnit`.
- Discrete mechanical properties via `obi:OBI_0000299`; typed to TTO class
  IRIs (`YieldStrength`, `TensileStrength`, etc.) with result value and unit.
- Constitutive model sub-node: model family string, provenance IRI linking to
  the calibration record, and embedded parameter nodes.
- SHACL shape validating card structure and property types.

---
