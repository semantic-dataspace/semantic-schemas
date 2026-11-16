# Changelog: LCA Assessment Run (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

---

## [Unreleased] - 2026-11-16

### Changed

- Operator picker restricted to `expert` KItems.

### Added

- Read-only `conforms_to` property so `dcterms:conformsTo` is written for form input too.

## [0.1.0] - 2026-11-13

### Added

- Initial draft, modelled on the ORCHESTER Demo 3 LCI data (LCI template 2023,
  Fraunhofer IWKS) and the MPPM–DSMS interface package.
- Uses the DSMS UPLCI vocabulary (`Orchester/LCA/vocabularies/dsms-uplci.ttl`).
