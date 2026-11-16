# Changelog: Unit Process Inventory (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

---

## [0.2.0] - 2026-11-16

### Changed (breaking)

- Form compatibility with the DSMS webform builder: removed internal `$defs` /
  `$ref` / `allOf` (not resolved by the form builder; inputs/outputs were
  rendered as plain text and stored as literals). All array items are inline
  objects; inputs and outputs are defined separately.
- Exchange amount is now `qudt:value` + `qudt:hasUnit` on the exchange (was an
  `obo:OBI_0001938` value-specification node), same pattern as technology parameters.
- Flow properties are flat fields (`uplci:monetaryValuePerUnit`, `uplci:currency`,
  `uplci:monetaryValueSource`, `uplci:climateChangePerUnit`, `uplci:climateChangeSource`);
  arrays inside array rows are not supported by the form backend.
- Background provider is flat (`uplci:backgroundDatabase`, `backgroundActivity`,
  `backgroundReferenceProduct`, `backgroundGeography`, `backgroundDatasetId`);
  an optional nested object would create an empty node on every row.
- Compilation date → `dcterms:date` (DSMS writes `dcterms:created` itself);
  data generators → `prov:wasAttributedTo` (DSMS writes `dcterms:creator` itself).
- Distinct id defaults for inputs (`input`), outputs (`output`), parameters
  (`parameter`) to prevent node merging between array rows.

### Added

- Read-only `conforms_to` property so `dcterms:conformsTo` is written for form input too.
- SHACL: inputs/outputs must be nodes (rejects literals); background activity
  required when a background database is set; data derivation of parameters
  must be a controlled value.

## [0.1.0] - 2026-11-13

### Added

- Initial draft, modelled on the ORCHESTER Demo 3 LCI data (LCI template 2023,
  Fraunhofer IWKS) and the MPPM–DSMS interface package.
- Uses the DSMS UPLCI vocabulary (`Orchester/LCA/vocabularies/dsms-uplci.ttl`).
