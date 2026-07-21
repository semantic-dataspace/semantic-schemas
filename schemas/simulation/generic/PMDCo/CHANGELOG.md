# Changelog: Simulation Generic (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `…/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [0.2.0] - 2026-07-17

### Changed

- `type` field const and default changed from a single string (`const: "VALUE"`) to a
  single-element array (`const: ["VALUE"]`) to align with JSON-LD, where `@type`
  naturally supports multiple values.

---

## [0.1.0] - 2026-05-10

### Changed

- Version numbering reset to `0.1.0`. All schemas in this repository adopted
  the SemVer convention that major version 0 signals a pre-release draft. No
  field or graph changes.

### Migration

Update `conforms_to` IRI filters in SPARQL queries:

```sparql
# old
FILTER(STR(?conformsTo) = "…/simulation/generic/#v3.0.0")
# new
FILTER(STR(?conformsTo) = "…/simulation/generic/#v0.1.0")
```

---

## [3.0.0] - 2026-05-04

### Breaking changes

- **Folder renamed** from `simulation/step/base/PMDCo/` to
  `simulation/generic/PMDCo/` (domain-wide restructuring that removes the
  `step/` intermediate level; no field or graph changes).
- `x-schema-id` updated from `…/simulation/step/base/PMDCo/` to
  `…/simulation/generic/PMDCo/`.
- `conforms_to` IRI in all generated records changes accordingly.

### Migration

Update `conforms_to` IRI filters in SPARQL queries:

```sparql
# old
FILTER(STR(?conformsTo) = "…/simulation/step/base/PMDCo/#v2.0.0")
# new
FILTER(STR(?conformsTo) = "…/simulation/generic/PMDCo/#v3.0.0")
```

---

## [2.0.0] - 2026-04-13

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

## [1.0.0] - 2026-04-09

- Initial release.
- Simulation step schema (`obi:ComputerSimulation`, `obi:0000471`).
- Fields: `step_name`, `inputs`, `outputs`, `preceded_by`, `conditions`.
