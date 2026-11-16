# Changelog: LCA Product System (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

---

## [0.2.0] - 2026-11-16

### Changed (breaking)

- Reference amount is now flat `qudt:value` + `qudt:hasUnit` (`reference_amount`,
  `reference_unit`) instead of a nested value-specification object.
- Modellers → `prov:wasAttributedTo` (DSMS writes `dcterms:creator` itself).

### Added

- Read-only `conforms_to` property so `dcterms:conformsTo` is written for form input too.

## [0.1.0] - 2026-11-13

### Added

- Initial draft, modelled on the ORCHESTER Demo 3 LCI data (LCI template 2023,
  Fraunhofer IWKS) and the MPPM–DSMS interface package.
- Uses the DSMS UPLCI vocabulary (`Orchester/LCA/vocabularies/dsms-uplci.ttl`).
