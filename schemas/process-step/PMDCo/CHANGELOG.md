# Changelog — Process Step (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `.../process-step/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [0.2.0] — 2026-05-27

### Added

- `x-kitem: ktypeIds: ["expert"]` on `operator` — renders a k-item picker in the webform builder.
- `x-kitem: ktypeIds: ["measurement-device"]` on `instrument` — same.

---

## [0.1.0] — 2026-05-10

### Added

- Initial release of the base schema for all process step schemas.
- `obi:PlannedProcess` (OBI_0000070) node with `rdfs:label`.
- Shared fields available to all extending schemas: `notes` (`rdfs:comment`),
  `date` (`dcterms:date`, `xsd:dateTime`), `has_specified_input`
  (OBI_0000293), `operator` (`prov:wasAssociatedWith`), `instrument`
  (`schema:instrument`).
- Extended via JSON Schema `allOf + $ref` by all domain step schemas
  (characterization, manufacturing, simulation).
- No standalone SHACL shape; each extending schema provides its own.

---
