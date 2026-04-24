# Changelog — Tensile Test (TTO)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR** — backwards-compatible additions (new optional fields, new conditions)
- **PATCH** — corrections that do not affect the graph structure (typos, description fixes, example updates)

The schema IRI encodes the minor version: `…/TTO/#v<MAJOR>.<MINOR>.0`.

---

## [3.0.1] — 2026-04-24

### Fixed

- **`specs/shape.ttl`**: `sh:datatype xsd:float` → `xsd:double` for the
  `pmdco:PMD_0000006` property constraint.  pyshacl treats integer-form
  `xsd:float` literals (e.g. `'310'^^xsd:float`) as ill-typed; `xsd:double`
  is the natural JSON numeric type and accepts both integer and decimal lexical
  forms.
- **`specs/schema.oold.yaml`**: `result_value` `@type` changed from `xsd:float`
  to `xsd:double` to match.

---

## [3.0.0] — 2026-04-24

### Changed (breaking)

- **Process class** changed from `tto:TensileTest` to `pmdco:PMD_0000974`
  (PMDCo3 CharacterisationProcess), following the S355 TTO/PMDCo3 reference
  dataset. TTO property types are now encoded in the result nodes only.
- **Process condition predicate** changed from `pmdco:PMD_0000016` to
  `pmdco:PMD_0000009`, matching the PMDCo3 ontology.
- **Result node pattern** changed from a single TTO-typed node to the PMDCo3
  Scalar Value Specification (SVS) pattern:
  - Result nodes are now typed `obi:OBI_0001931` (ScalarValueSpecification).
  - Numeric values are stored with `pmdco:PMD_0000006` (was `obi:OBI_0001937`).
  - Each SVS references a TTO-typed property instance via `obi:OBI_0001927`
    (`specifies_value_of`).
- **Time-series descriptor pattern**: column descriptors now use
  `csvw:Table` / `csvw:column` / `csvw:Column` / `obo:IAO_0000039` (unit predicate),
  matching the S355 TTO/PMDCo3 reference dataset.  Previously used `dcat:Dataset`
  / `qudt:hasUnit`.  TTO column class IRIs are now TTO v3.0.0 numeric IRIs
  (e.g. `tto:TTO_0000004` for elongation, `tto:TTO_0000005` for extension).
  Columns without a TTO v3 class receive only the base `csvw:Column` type.
- **QUDT unit prefix** corrected from `https://qudt.org/vocab/unit/` to
  `http://qudt.org/vocab/unit/` to match the canonical QUDT vocabulary.
- `x-schema-version` bumped from `2.0.0` to `3.0.0`.
- `dcterms:conformsTo` IRI in generated RDF updated from `#v2.0.0` to `#v3.0.0`.

### Migration

Update any SPARQL queries filtering on the schema IRI:

```sparql
# old
FILTER(?schema = <…/characterization/step/tensile-test/TTO/#v2.0.0>)
# new
FILTER(?schema = <…/characterization/step/tensile-test/TTO/#v3.0.0>)
```

The process node type changes (`tto:TensileTest` → `pmdco:PMD_0000974`),
the condition predicate changes (`PMD_0000016` → `PMD_0000009`), and result
nodes are now SVS triples rather than direct TTO-typed property nodes.
Existing v2.0.0 graphs are not compatible with v3.0.0 shapes.

---

## [2.0.0] — 2026-04-13

### Changed

- **Folder renamed** from `characterization/tensile-test/TTO/` to
  `characterization/step/tensile-test/TTO/` as part of a domain-wide
  restructuring that places all step-level schemas under `step/<variant>/`.
- `x-schema-id` updated to reflect the new path.
- `$ref` (base schema dependency) updated from
  `characterization/step/PMDCo/` to `characterization/step/base/PMDCo/`.
- `x-schema-dependencies` version requirement updated to `base/PMDCo/#v2.0.0`.
- `conforms_to` IRI in generated RDF now points to the new versioned path.

### Migration

The generated RDF graph structure is **unchanged**; only the provenance IRI
(`dcterms:conformsTo`) differs. Update any `conforms_to` filters in SPARQL
queries or dashboards:

```sparql
# old
FILTER(?schema = <…/characterization/tensile-test/TTO/#v1.1.0>)
# new
FILTER(?schema = <…/characterization/step/tensile-test/TTO/#v2.0.0>)
```

---

## [1.1.0] — 2026-04-10

### Added

- `gauge_length` / `gauge_length_unit` — extensometer gauge length now captured
  as a `pmdco:PMD_0000013` process condition (`Messlänge Standardweg` in Zwick exports).
- `preload` / `preload_unit` — pre-load applied before the test ramp now captured
  as a `pmdco:PMD_0000013` process condition (`Vorkraft` in Zwick exports).
- `test_date` — date and time of the test mapped to `dcterms:date` (typed
  `xsd:dateTime`). The Zwick parser converts the Excel serial-number format
  automatically.
- `obo: <http://purl.obolibrary.org/obo/>` added to the `@context` so OBO
  terms serialise with a readable prefix instead of rdflib's auto-generated
  `ns1`/`ns2` labels.

### Changed

- `ZwickParser` now uses a general `unit_field_map` for unit extraction
  (replaces the hardcoded `strain_rate_label` mechanism). The `strain_rate_label`
  parameter is retained for backwards compatibility.

### Notes

All new fields are optional. Existing graphs produced under v1.0.0 remain valid.

---

## [1.0.0] — initial release

- `tto:TensileTest` node with `rdfs:label`, `dcterms:conformsTo`
- `has_specified_input` linking to specimen IRI
- `has_process_condition` for test standard, strain rate, temperature
- `has_specified_output` for measured properties (yield strength, tensile
  strength, elongation after fracture, reduction of area, …) typed to TTO classes
- `dcat:Dataset` descriptor for time-series columns with TTO class IRIs and
  QUDT unit IRIs per column
- SHACL shape validating the above structure
