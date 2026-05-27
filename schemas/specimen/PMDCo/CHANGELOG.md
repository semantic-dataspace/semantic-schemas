# Changelog: Specimen (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `.../specimen/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [0.1.0] - 2026-05-10

### Added

- Initial release.
- `pmdco:PMD_0000057` (Specimen) node with `rdfs:label` and optional mass
  (`qudt:value`, `qudt:hasUnit`).
- Formal schema dependency on `chemical-composition/PMDCo/` via
  `has_composition`; the composition sub-graph is produced by the
  chemical-composition transform and linked back to the specimen by IRI.
- SHACL shape validating specimen label and mass datatype; load together with
  the chemical-composition SHACL shape for full validation.

---
