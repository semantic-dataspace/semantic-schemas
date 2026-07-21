# Changelog: Data Analysis — Generic (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

---

## [0.1.0] - 2026-07-17

### Added

- Initial release.
- `obi:DataTransformation` (OBI_0200000) schema composing with `process-step/PMDCo` via `allOf`.
- `has_specified_input` and `has_specified_output` fields with `x-ktype: [dataset, dataset-catalog]` / `x-ktype: [dataset]`.
- `operator` field with `x-ktype: [expert]`.
