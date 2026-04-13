# Changelog — Measurement Device (PMDCo/OBI)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR** — backwards-compatible additions (new optional fields)
- **PATCH** — corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `…/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [1.0.0] — 2026-04-13

- Initial release.
- `obi:Device` (OBI_0000968) node with `rdfs:label` and `dcterms:conformsTo`.
- Descriptive metadata: `manufacturer` (`schema:manufacturer`), `model`
  (`schema:model`), `serial_number` (`schema:serialNumber`).
- `calibration_date` mapped to `dcterms:date` (typed `xsd:date`).
- SHACL shape validating label, conformsTo, and optional field datatypes.
