# Changelog: Measurement Device (PMDCo/OBI)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `…/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [0.2.0] - 2026-07-17

### Changed

- `type` field const and default changed from a single string (`const: "VALUE"`) to a
  single-element array (`const: ["VALUE"]`) to align with JSON-LD, where `@type`
  naturally supports multiple values.

---

## [0.1.0] - 2026-05-10

### Fixed

- `manufacturer` field: removed `"@type": "@id"` from JSON-LD context entry
  that was incorrectly treating string values as IRIs, causing SHACL
  `sh:datatype xsd:string` validation failures on any record that set this
  field.

### Changed

- Version numbering reset to `0.1.0` (SemVer 0.x pre-release convention).

### Migration

Update `conforms_to` IRI filters in SPARQL queries:

```sparql
# old
FILTER(STR(?conformsTo) = "…/measurement-device/PMDCo/#v1.0.0")
# new
FILTER(STR(?conformsTo) = "…/measurement-device/PMDCo/#v0.1.0")
```

---

## [1.0.0] - 2026-04-13

- Initial release.
- `obi:Device` (OBI_0000968) node with `rdfs:label` and `dcterms:conformsTo`.
- Descriptive metadata: `manufacturer` (`schema:manufacturer`), `model`
  (`schema:model`), `serial_number` (`schema:serialNumber`).
- `calibration_date` mapped to `dcterms:date` (typed `xsd:date`).
- SHACL shape validating label, conformsTo, and optional field datatypes.
