# Changelog: Tensile Test (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/).

---

## [0.2.0] - 2026-05-27

### Changed (breaking)

- `has_specified_input` added to the `required` list. Records that previously
  omitted the specimen link are no longer valid against this schema.

### Added

- `x-kitem: ktypeIds: ["specimen"]` on the `has_specified_input` field so the
  webform renders it as a knowledge-graph item picker scoped to specimen entries.

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
FILTER(STR(?conformsTo) = "…/characterization/tensile-test/#v3.0.0")
# new
FILTER(STR(?conformsTo) = "…/characterization/tensile-test/#v0.1.0")
```

---

## [2.0.0] - 2026-05-04

### Breaking changes

- **Folder moved** from `characterization/step/tensile-test/PMDCo/` to
  `characterization/tensile-test/PMDCo/` (domain-wide restructuring that removes
  the `step/` intermediate level; no field or graph changes).
- `x-schema-id` updated from `…/characterization/step/tensile-test/PMDCo/` to
  `…/characterization/tensile-test/PMDCo/`.
- `conforms_to` IRI in all generated records changes accordingly.

### Migration

Update `conforms_to` IRI filters in SPARQL queries:

```sparql
# old
FILTER(?schema = <…/characterization/step/tensile-test/PMDCo/#v1.1.0>)
# new
FILTER(?schema = <…/characterization/tensile-test/PMDCo/#v2.0.0>)
```

---

## [1.1.0] - 2026-04-27

### Added

- `x-transformers: [testxpert_iii]`: links the schema to the TestXpert III
  parser in `semantic-transformers`.

---

## [1.0.0] - 2026-04-24

### Added

- Initial release of the PMDCo tensile test schema.
- Process node typed as `pmdco:PMD_0000974` (CharacterisationProcess).
- Conditions linked via `pmdco:PMD_0000009`, typed as `pmdco:PMD_0000013`.
- Results follow the PMDCo measurement pattern:
  - `obo:IAO_0000109` (MeasurementDatum) per property, labelled by name.
  - Embedded `obo:OBI_0001931` (ScalarValueSpecification) with numeric value
    (`pmdco:PMD_0000006`) and unit (`obo:IAO_0000039`).
- QUDT unit prefix: `http://qudt.org/vocab/unit/`.
- `timeseries_pattern` config block: instructs `semantic-transformers` to
  use `csvw:Table` / `csvw:column` / `csvw:Column` / `obo:IAO_0000039` for
  time-series column descriptors, matching the TTO/PMDCo3 S355 reference dataset.
- SHACL shape validating datum labels, SVS values, and units.
- `docs/1_tensile_test_pmdco_workflow.ipynb`: hand-crafted JSON to RDF workflow.
- `docs/2_tensile_test_pmdco_csv_workflow.ipynb`: Zwick machine file to RDF
  using `semantic-transformers`, with DataFrame exploration and SPARQL queries.
