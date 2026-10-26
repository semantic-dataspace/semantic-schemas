# Changelog: Manufacturing Generic (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `…/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [0.3.0] - 2026-10-14

### Changed (breaking)

- **Root class IRI changed**: `pmdco:PMD_0000029` → `pmdco:PMD_0000833`
  (ManufacturingProcess). Existing records' `rdf:type` triple changes.
  SPARQL queries and SHACL shapes filtering on `PMD_0000029` must be updated.

- **`has_process_condition` renamed to `has_process_attribute`**:
  predicate IRI changes from `pmdco:PMD_0000016` (has_process_condition) to
  `pmdco:PMD_0000009` (has_process_attribute). Existing triples using
  `PMD_0000016` are not migrated automatically. SPARQL queries using
  `pmdco:PMD_0000016` must be updated.

- **`parameter_label` replaced by `parameter_type`**: the parameter
  identification field on `ParameterSpecification` nodes changes from
  `rdfs:label` (free-text name) to `rdf:type` (IRI from the process-parameter
  vocabulary service). This is a semantic change — parameters are now
  IRI-typed, enabling vocabulary-based SPARQL filtering. Existing records
  storing a text label in `rdfs:label` are not equivalent to the new IRI in
  `rdf:type`.

### Changed

- `parameter_unit` field: free-text description replaced by `x-vocabulary` →
  measurement-unit vocabulary service. Unit stored as QUDT IRI via
  `qudt:hasUnit`; semantics unchanged for records that already used QUDT IRIs.
- `has_specified_input`, `has_specified_output`, `preceded_by` fields:
  `x-ktype` annotation replaced by `format: kitem` + `x-kitem: {ktypeIds: [...]}`.
  UI change only; no RDF change.

### Added

- `dsmsht:` namespace (`https://w3id.org/dsms/heattreatment#`) added to
  `@context` for referencing heat-treatment-specific parameter class IRIs
  (shared with manufacturing/heat-treatment/PMDCo).
- `uqudt:` namespace (`http://qudt.org/vocab/unit/`) added to `@context`.
- `parameter_type` field stores vocabulary IRI as `rdf:type` on each
  ParameterSpecification node, enabling class-based SPARQL queries over
  process parameters.

### Migration

Update all SPARQL queries and SHACL shapes using `PMD_0000029` or
`PMD_0000016`:

```sparql
# old
?proc a pmdco:PMD_0000029 .
?proc pmdco:PMD_0000016 ?cond .
# new
?proc a pmdco:PMD_0000833 .
?proc pmdco:PMD_0000009 ?param .
```

---

## [0.2.1] - 2026-07-21

### Changed

- `x-schema-uri` corrected to reference `schema.oold.generated.json` instead
  of `schema.oold.yaml`; the generated JSON is the canonical versioned artifact.

---

## [0.2.0] - 2026-07-17

### Changed

- `type` field const and default changed from a single string (`const: "VALUE"`) to a
  single-element array (`const: ["VALUE"]`) to align with JSON-LD, where `@type`
  naturally supports multiple values.
- `x-kitem: {ktypeIds: [...]}` annotations replaced by the flatter `x-ktype: [...]` form on all IRI reference fields.

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
FILTER(STR(?conformsTo) = "…/manufacturing/generic/#v3.0.0")
# new
FILTER(STR(?conformsTo) = "…/manufacturing/generic/#v0.1.0")
```

---

## [3.0.0] - 2026-05-04

### Breaking changes

- **Folder renamed** from `manufacturing/step/base/PMDCo/` to
  `manufacturing/generic/PMDCo/` (domain-wide restructuring that removes the
  `step/` intermediate level; no field or graph changes).
- `x-schema-id` updated from `…/manufacturing/step/base/PMDCo/` to
  `…/manufacturing/generic/PMDCo/`.
- `conforms_to` IRI in all generated records changes accordingly.

### Migration

Update `conforms_to` IRI filters in SPARQL queries:

```sparql
# old
FILTER(STR(?conformsTo) = "…/manufacturing/step/base/PMDCo/#v2.0.0")
# new
FILTER(STR(?conformsTo) = "…/manufacturing/generic/PMDCo/#v3.0.0")
```

---

## [2.0.0] - 2026-04-13

### Breaking changes

- **Folder renamed** from `manufacturing/step/PMDCo/` to `manufacturing/step/base/PMDCo/`
  (repository-level restructuring; no field or graph changes).
- `x-schema-id` updated from
  `…/manufacturing/step/PMDCo/` to `…/manufacturing/step/base/PMDCo/`.
- `conforms_to` IRI in all generated records changes accordingly.

### Migration

Update `conforms_to` IRI filters in SPARQL queries:

```sparql
# Old
FILTER(STR(?conformsTo) = "…/manufacturing/step/PMDCo/#v1.0.0")

# New
FILTER(STR(?conformsTo) = "…/manufacturing/step/base/PMDCo/#v2.0.0")
```

---

## [1.0.0] - 2026-04-09

- Initial release.
- Manufacturing process schema (`pmdco:PMD_0000029`).
- Fields: `process_name`, `inputs`, `outputs`, `preceded_by`, `conditions`.
