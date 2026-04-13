# Changelog — Simulation Step base (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR** — backwards-compatible additions (new optional fields)
- **PATCH** — corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `…/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [2.0.0] — 2026-04-13

### Breaking changes

- **Folder renamed** from `simulation/step/PMDCo/` to `simulation/step/base/PMDCo/`
  (repository-level restructuring; no field or graph changes).
- `x-schema-id` updated from
  `…/simulation/step/PMDCo/` to `…/simulation/step/base/PMDCo/`.
- `conforms_to` IRI in all generated records changes accordingly.

### Migration

Update `conforms_to` IRI filters in SPARQL queries:

```sparql
# Old
FILTER(STR(?conformsTo) = "…/simulation/step/PMDCo/#v1.0.0")

# New
FILTER(STR(?conformsTo) = "…/simulation/step/base/PMDCo/#v2.0.0")
```

---

## [1.0.0] — 2026-04-09

- Initial release.
- Simulation step schema (`obi:ComputerSimulation`, `obi:0000471`).
- Fields: `step_name`, `inputs`, `outputs`, `preceded_by`, `conditions`.
