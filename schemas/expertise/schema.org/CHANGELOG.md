# Changelog: Expertise (schema.org)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/).

---

## [0.2.0] - 2026-07-17

### Changed

- `type` field const and default changed from a single string (`const: "VALUE"`) to a
  single-element array (`const: ["VALUE"]`) to align with JSON-LD, where `@type`
  naturally supports multiple values.
- `x-kitem: {ktypeIds: [...]}` annotations replaced by the flatter `x-ktype: [...]` form on all IRI reference fields.

---

## [0.1.0] - 2026-05-10

### Deprecated

- This schema is deprecated in favour of [Expertise (VIVO)](../VIVO/). The
  VIVO schema expresses research-area expertise and instrument experience with
  two distinct predicates (`vivo:hasResearchArea`, `vivo:hasExperienceIn`),
  resolving the key limitation of this schema where all categories shared a
  single `schema:knowsAbout` predicate. New records should use
  `expertise/VIVO/` instead.
- `x-maturity` set to `deprecated`.

### Changed

- Version numbering reset to `0.1.0` (SemVer 0.x pre-release convention).

---

## [1.0.0] - 2026-04-27

### Added

- Initial release of the expertise schema under `expertise/schema.org/`.
- Records areas of expertise of a materials science researcher as links to
  knowledge graph entities (`schema:knowsAbout`).
- Six categories: `materials`, `material_modelling`, `measurement_devices`,
  `production_devices`, `application_fields`, `methods`.
- Root class: `foaf:Person`.
- `docs/1_expertise_workflow.ipynb`: step-by-step notebook.
- `docs/example.oold.json`: ready-to-edit example.
