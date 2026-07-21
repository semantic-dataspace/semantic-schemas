# Changelog: Chemical Composition (BWMD)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `.../chemical-composition/BWMD/#v<MAJOR>.<MINOR>.0`.

---

## [0.2.0] - 2026-07-17

### Changed

- `type` field const and default changed from a single string (`const: "VALUE"`) to a
  single-element array (`const: ["VALUE"]`) to align with JSON-LD, where `@type`
  naturally supports multiple values.

---

## [0.1.0] - 2026-05-10

### Added

- Initial release.
- `bwmd:ChemicalComposition` node linked to a material IRI via
  `pmdco:PMD_0000551` (quality_of).
- Element entries with `bwmd:hasElementSymbol` (string), `bwmd:hasMinContent`,
  `bwmd:hasMaxContent`, and `bwmd:hasNominalContent` (all `xsd:double`).
- Unit field (`bwmd:hasUnit`) per element entry, defaulting to `wt%`.
- SHACL shape validating composition node and element structure.

---
