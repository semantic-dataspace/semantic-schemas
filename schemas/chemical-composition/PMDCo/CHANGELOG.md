# Changelog: Chemical Composition (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `.../chemical-composition/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [1.0.0] - 2026-09-17

### Changed

- **Breaking:** `quality_of` changed from an inline embedded object `{ label: "..." }` to a
  kitem IRI reference (`format: kitem`, `type: array`). The `@context` entry gains
  `"@type": "@id"` so the RDF triple becomes `<chem_comp> ro:0000080 <material_iri>`
  instead of a blank node. Backend resolves the selected kitem descriptor to its
  canonical knowledge service IRI before JSON-LD expansion.
- **Breaking:** `element.part_of` `$comment` updated to `"root.quality_of"` pattern so the
  backend `_rebuild_from_flat()` automatically propagates the material kitem IRI into
  the `<element_ref> bfo:part_of <material_iri>` triple.
- **Breaking:** `element.type` changed from `type: array + enum` to `type: string + enum`
  (correct JSON Schema for a single-value element selector).
- `type` readOnly fields on all nodes now use `const: ["IRI"]` (array const) instead of
  `enum: ["IRI"]` (string enum) to match `type: array` and pass JSON Schema validation.
- SHACL shape: `quality_of` constraint changed to `sh:nodeKind sh:IRI`; removed the
  `sh:node shape:material_label` sub-shape (label lives on the material kitem, not here).
- Simplified input: `material_id` removed (was for inline material node, now replaced by
  kitem IRI); `material_uri` added (optional, the full material kitem IRI).
- Transform: `quality_of` output changed from `{ "label": material_name }` to
  `[material_uri]` (if provided) or `[$matId]` (derived slug, for standalone use).
- Extensive explanatory comments added to all readOnly and back-reference fields.

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
