# Changelog: Expertise (VIVO)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `.../expertise/VIVO/#v<MAJOR>.<MINOR>.0`.

---

## [0.3.0] - 2026-07-17

### Changed

- `type` field const and default changed from a single string (`const: "VALUE"`) to a
  single-element array (`const: ["VALUE"]`) to align with JSON-LD, where `@type`
  naturally supports multiple values.
- `x-kitem: {ktypeIds: [...]}` annotations replaced by the flatter `x-ktype: [...]` form on all IRI reference fields.

---

## [0.2.0] - 2026-05-10

### Added

- `publications` field: array of `vivo:Publication` nodes linked via `vivo:authorOf`.
  Each entry supports `title` (required), `doi` (`bibo:doi`), `year` (`dcterms:issued`),
  `url` (`schema:url`), `venue` (`schema:isPartOf`, journal or conference name as string),
  and `coauthors` (`dcterms:contributor`, IRI references to person profiles).
- `expertise_level` on each expertise item: self-reported proficiency annotation stored
  as `schema:proficiencyLevel` on the vocabulary term node.
  Allowed values: `novice`, `competent`, `proficient`, `expert`.

### Changed

- **Breaking**: all six expertise fields (`materials`, `material_modelling`,
  `application_fields`, `methods`, `measurement_devices`, `production_devices`) now
  contain objects with `id` (vocabulary IRI) and optional `expertise_level`, instead
  of plain IRI strings.  Update existing data by wrapping each string value:
  `"https://…/mat-steel"` → `{"id": "https://…/mat-steel"}`.
- Namespaces `schema:` (`https://schema.org/`) and `bibo:` (`http://purl.org/ontology/bibo/`)
  added to JSON-LD `@context`.

---

## [0.1.0] - 2026-05-10

### Added

- Initial release.
- `foaf:Person` node with `rdfs:label`.
- Research-area expertise across four vocabulary namespaces (`material`,
  `material-modelling`, `application-field`, `method`) expressed with
  `vivo:hasResearchArea`.
- Instrument experience across two vocabulary namespaces
  (`measurement-device`, `production-device`) expressed with
  `vivo:hasExperienceIn`.
- Vocabulary terms sourced at runtime from `vocabulary.materials-data.space`.
- Supersedes `expertise/schema.org/` (deprecated), which collapsed all
  categories to a single `schema:knowsAbout` predicate.

---
