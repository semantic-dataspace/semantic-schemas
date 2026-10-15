# Changelog: Simulation Generic (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `…/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [0.4.0] - 2026-10-14

### Changed (breaking)

- **`has_process_condition` renamed to `has_process_attribute`**: predicate IRI
  changes from `pmdco:PMD_0000016` (has_process_condition) to
  `pmdco:PMD_0000009` (has_process_attribute). Existing triples using
  `PMD_0000016` are not migrated automatically. SPARQL queries using
  `pmdco:PMD_0000016` must be updated.

### Changed

- ParameterSpecification node type label: `pmdco:ProcessCondition` →
  `pmdco:ParameterSpecification` (display label only; underlying IRI
  `PMD_0000013` unchanged).
- `operator` field: `x-ktype: [expert]` + `format: uri` replaced by
  `format: kitem` + `x-kitem: {ktypeIds: [expert]}`. UI annotation only; no
  RDF change.

### Added

- `uqudt:` namespace (`http://qudt.org/vocab/unit/`) added to `@context`.

### Migration

```sparql
# old
?sim pmdco:PMD_0000016 ?cond .
# new
?sim pmdco:PMD_0000009 ?param .
```

---

## [0.3.0] - 2026-07-21

### Added

- `operator` field (`prov:wasAssociatedWith`, single IRI) inherited from and
  consistent with `process-step/PMDCo`.
- `allOf + $ref` dependency on `process-step/PMDCo` (v0.3.0): the generic
  simulation schema now formally extends the universal base. All shared fields
  (`label`, `date`, `has_specified_input`, `has_specified_output`,
  `preceded_by`, `operator`, `instrument`) are inherited via allOf.
- `x-schema-dependencies` declaring the `process-step-PMDCo-v0.3.0` dependency.

### Changed

- `@context` in the YAML source now declares only simulation-specific entries;
  inherited entries from `process-step/PMDCo` are merged at build time by
  `scripts/convert_to_json.py`. The generated JSON artifact is unchanged.
- `x-schema-uri` updated to point to `schema.oold.generated.json` (the artifact
  with the fully merged context) instead of the YAML source.

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
