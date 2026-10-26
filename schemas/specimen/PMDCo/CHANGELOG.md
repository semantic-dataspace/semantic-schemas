# Changelog: Specimen (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `.../specimen/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [0.7.0] - 2026-10-15

### Changed (breaking — complete schema rewrite)

Schema rewritten to use PMDCo **TemporallyQualifiedContinuant (TQC)** pattern
instead of the v0.4.x duality-object/material pattern.

- **Root types**: `["bfo:0000030"]` → `["obo:BFO_0000030", "pmdco:PMD_0000068"]`.
  Records now also carry `PMD_0000068` (TemporallyQualifiedContinuant). Existing
  records typed only with `BFO_0000030` are not equivalent.
- **`material` field predicate**: `schema:material` → `pmdco:PMD_0000070`
  (is_state_of). Existing triples using `schema:material` are not migrated.
  SPARQL queries must be updated.
- **`mass` field removed**: replaced by `physical_properties` array (see Added).
  Existing records with a `mass` quality node have no automatic migration path.
- **`source` field**: single URI string → multi-value array with `x-kitem:
  {ktypeIds: [semi-finished-product, specimen, material]}`, enabling multi-hop
  provenance chains.

### Added

- `exists_at` field: BFO temporal interval (`BFO_0000202`) with
  `has_first_instant` / `has_last_instant` date literals, enabling state-change
  SPARQL queries across pre-test and post-test specimens.
- `physical_properties` array: dynamic quality-node array (`RO_0000086`
  has_quality). Supported types: Thickness, Width, Length, Diameter, Mass,
  Surface Roughness Ra/Rq (PMDCo quality class IRIs). Replaces the single
  `mass` field.
- `surface_preparation` field (text): polishing sequence, `dspec:hasSurfacePreparation`.
- `specimen_form` field (enum): Bulk, Thin Film, Coating on Substrate,
  Cross-section, Other — `dspec:hasSpecimenForm`.
- `dspec:` namespace (`https://w3id.org/dsms/specimen#`) added to `@context`.

### Migration

```sparql
# old material link
?spec schema:material ?mat .
# new
?spec pmdco:PMD_0000070 ?mat .
```

---

## [0.4.1] - 2026-07-21

### Changed

- `x-schema-uri` corrected to reference `schema.oold.generated.json` instead
  of `schema.oold.yaml`; the generated JSON is the canonical versioned artifact.

---

## [0.4.0] - 2026-07-17

### Changed

- `type` field const and default changed from a single string (`const: "VALUE"`) to a
  single-element array (`const: ["VALUE"]`) to align with JSON-LD, where `@type`
  naturally supports multiple values.
- `x-kitem: {ktypeIds: [...]}` annotations replaced by the flatter `x-ktype: [...]` form on all IRI reference fields.

---

## [0.3.0] - 2026-06-03

### Added

- `source` field (`prov:wasDerivedFrom`) linking the specimen to the specific
  semi-finished product (e.g. metal sheet) it was cut or prepared from,
  following the PROV-O provenance pattern. Optional; when set, `material` can
  be auto-populated from `source.made_of`.
- SHACL property constraints for `schema:material` (maxCount 1, IRI) and
  `prov:wasDerivedFrom` (maxCount 1, IRI) added to `shape:specimen`.
- `prov:` and `schema:` namespace prefixes added to `shape.ttl`.

### Changed

- `material` field description updated to clarify it follows the PMDCo duality
  object/material pattern for abstract alloy identity.
- Schema header comment and `$comment` updated to document both the duality
  pattern and the new physical provenance pattern.

---

## [0.2.0] - 2026-05-27

### Changed

- **Breaking:** replaced the inline `elements` chemical-composition array and
  the `comp_id` / `specimen_id` internal-identifier fields with a single
  `material` field (`x-kitem`, `ktypeIds: ["material"]`) that references an
  existing Material record in the knowledge graph.
- Graph pattern updated to follow the PMDCo duality pattern strictly:
  `Specimen → schema:material → Material IRI`; chemical composition is now a
  quality of the Material, not embedded in the specimen document.
- Removed JSON Schema `$ref` dependency on `chemical-composition/PMDCo/`.
- `x-schema-version` bumped to `0.2.0`; `conforms_to` IRI updated accordingly.

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
