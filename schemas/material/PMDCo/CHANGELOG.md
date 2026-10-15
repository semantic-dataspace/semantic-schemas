# Changelog: Material (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

---

## [0.1.0] - 2026-10-15

### Added

- Initial release.
- `pmdco:PMD_0000000` (Material) root type — the abstract substance identity node
  in the PMDCo duality pattern.
- Core identity fields: `label` (`rdfs:label`), `material_designation` (`dcterms:title`),
  `material_class` enum (Metal / Ceramic / Polymer / Composite / Coating / Other),
  `material_standard` (`dcterms:conformsTo`), `batch_lot` (`dcterms:identifier`),
  `supplier` (`schema:provider`).
- Processing history: `heat_treatment` (`dsms:hasHeatTreatmentDescription`).
- Notes field: `notes` (`rdfs:comment`).
- Supports PMDCo duality: specimens link here via `PMD_0000070` (`is_state_of`);
  chemical compositions link here via `RO_0000080` (`quality_of`).

---
