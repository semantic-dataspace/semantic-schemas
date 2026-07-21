# Changelog: Dataset Catalog (DCAT)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

---

## [0.1.0] - 2026-07-17

### Added

- Initial release.
- `dcat:Catalog` schema composing with `dataset/generic/DCAT` via `allOf`.
- `dataset` field (`dcat:dataset`) listing member dataset k-items.
