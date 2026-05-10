# Changelog — Expertise (VIVO)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `.../expertise/VIVO/#v<MAJOR>.<MINOR>.0`.

---

## [0.1.0] — 2026-05-10

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
