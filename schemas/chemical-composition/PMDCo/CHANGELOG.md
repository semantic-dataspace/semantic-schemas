# Changelog: Chemical Composition (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `.../chemical-composition/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [0.2.1] - 2026-07-21

### Changed

- `x-schema-uri` corrected to reference `schema.oold.generated.json` instead
  of `schema.oold.yaml`; the generated JSON is the canonical versioned artifact.

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
- `pmdco:PMD_0000551` (ChemicalComposition) node linked to a material IRI.
- Element fraction entries with `pmdco:PMD_0000069` (hasElementSymbol) and
  `qudt:value` (fraction value, `xsd:double`).
- `qudt:hasUnit` per entry accepting `mass%`, `vol%`, or `mol%`.
- SHACL shape validating composition node and fraction entries.

---
