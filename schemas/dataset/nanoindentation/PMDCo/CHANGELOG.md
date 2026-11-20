# Changelog: Nanoindentation Dataset (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `…/nanoindentation/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [0.1.0] - 2026-10-15

### Added

Initial release.

- DCAT-based dataset schema for individual nanoindentation load-displacement files.
- Per-indent scalar results as MeasurementDatum (`IAO_0000109`) +
  ScalarValueSpecification (`OBI_0001931`) nodes via `obi:OBI_0000299`
  (has_specified_output).
- Indent metadata fields:
  - `indent_index` (integer): sequential indent number within the experiment.
  - `x_position`, `y_position` (number, mm): stage coordinates.
  - `timestamp` (date-time): acquisition time of this indent.
- `file_format` field for raw file type (e.g. `.hdf5`, `.xlsx`, `.txt`).
- Links to parent experiment and specimen are expressed via DSMS
  `linked_kitems`, not as schema fields — keeps the schema focused on
  data content.
- `dcat:Dataset` root class with `dcterms:conformsTo` provenance IRI.
