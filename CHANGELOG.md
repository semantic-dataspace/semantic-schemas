# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-04-24

### Changed

- **`characterization/step/tensile-test/TTO/`** updated to schema v3.0.0 (breaking
  graph structure change). Adopts the PMDCo3 / S355 measurement pattern:
  process class changed to `pmdco:PMD_0000974`, condition predicate to
  `pmdco:PMD_0000009`, result nodes restructured to `obi:OBI_0001931`
  (ScalarValueSpecification) with `pmdco:PMD_0000006` for numeric values and
  `obi:OBI_0001927` linking to TTO-typed property instance nodes.
  QUDT unit prefix corrected from `https://` to `http://`.
- **Time-series descriptor pattern** (TTO and PMDCo schemas): time-series metadata
  now follows the `csvw:Table` / `csvw:column` / `csvw:Column` / `obo:IAO_0000039`
  pattern used in the TTO/PMDCo3 S355 reference dataset, replacing the previous
  `dcat:Dataset` / `qudt:hasUnit` pattern.  Both schemas now include a
  `timeseries_pattern` config block that instructs `semantic-transformers` how to
  serialise column descriptors.

### Added

- **`characterization/step/tensile-test/PMDCo/`** — new schema for tensile test
  results using pure PMDCo3 classes (no TTO dependency). Follows the PMDCo
  measurement pattern: process (`pmdco:PMD_0000974`) → measurement datum
  (`obo:IAO_0000109`) → scalar value specification (`obo:OBI_0001931`).
  Results are labelled by name rather than typed to TTO property classes.

---

## [0.2.0] - 2026-04-13

### Added

- **`measurement-device/PMDCo/`** — new schema for registering physical measurement
  and characterization instruments. Records name, manufacturer, model, serial number,
  and last calibration date. Root class: `obi:OBI_0000968` (Device). Includes
  simplified input schema, OO-LD schema, JSONata transform, SHACL shape, example
  input, and step-by-step notebook (`1_device_workflow.ipynb`).
- **`characterization/process/PMDCo/`** — new fixed-structure template for
  characterization experiments. Enforces three mandatory fields (operator via
  `prov:wasAssociatedWith`, device via `schema:instrument`, specimen via
  `obi:has_specified_input`). Optional `step_reference` links to a detailed result
  node. Includes all spec files and notebook (`1_characterization_process_workflow.ipynb`).
- **`workflow/templates/material-card/PMDCo/`** — new cross-schema workflow template
  sitting above `workflow/PMDCo/`. A single input dictionary drives all six sub-schemas
  (device, manufacturing step, characterization process + TTO result, model calibration,
  material card). Includes `specs/schema.simplified.json`, `specs/transform.simplified.jsonata`,
  `README.md`, `docs/workflow_template.input.json`, and beginner-oriented notebook
  `docs/1_material_card_with_template.ipynb`. No new RDF class; validated by the
  six sub-schemas' own SHACL shapes.
- **`scripts/run_notebooks.sh`** — helper script to run all notebooks in test mode
  (`./scripts/run_notebooks.sh`) or refresh outputs in-place for documentation
  (`./scripts/run_notebooks.sh --refresh`). Supports a single-notebook path argument.

### Changed

- **`characterization/step/PMDCo/` renamed to `characterization/step/base/PMDCo/`**
  (schema v2.0.0, breaking path change). The schema is otherwise unchanged;
  only `x-schema-id` and the provenance IRI (`conforms_to`) are updated.
- **`characterization/tensile-test/TTO/` moved to `characterization/step/tensile-test/TTO/`**
  (schema v2.0.0, breaking path change). Base schema dependency updated to
  `characterization/step/base/PMDCo/` v2.0.0.
- **`manufacturing/step/PMDCo/` renamed to `manufacturing/step/base/PMDCo/`**
  (schema v2.0.0, breaking path change). No field or graph changes.
- **`simulation/step/PMDCo/` renamed to `simulation/step/base/PMDCo/`**
  (schema v2.0.0, breaking path change). No field or graph changes.
- **`simulation/model-calibration/PMDCo/` moved to `simulation/step/model-calibration/PMDCo/`**
  (schema v2.0.0, breaking path change). Base schema `$ref` updated to
  `simulation/step/base/PMDCo/` v2.0.0.
- **`characterization/process/PMDCo/README.md`**: reframed to lead with the
  "fixed-structure template" concept rather than provenance-enforcement language.
- **`workflow/PMDCo/README.md`**: title changed from "Cross-Domain Workflow" to
  "Workflow"; step type table updated to reflect new `step/base/` paths.
- **`workflow/PMDCo/docs/3_material_card_without_template.ipynb`** (renamed from
  `3_workflow_cross_domain.ipynb`): path variables and labels updated to new folder
  locations; title updated to "316L material card workflow: step-by-step approach".
- **`workflow/templates/material-card/PMDCo/docs/1_material_card_with_template.ipynb`**
  (was `4_workflow_process_centric.ipynb`, fully rewritten): beginner-oriented notebook
  using a single `workflow_template` dictionary; all schema machinery hidden behind
  named helper functions; plain-English outputs and query framing; no em-dash style.
- **`docs/4_schema-patterns.md`**: stale path references updated; new section 5
  explaining the `process/` template layer and when to use it vs `step/` schemas.
- **`CATALOG.md`**: updated paths for all moved schemas; domain structure section
  extended to cover `manufacturing/` and `simulation/` folder layout; new entry
  for `workflow/templates/material-card/PMDCo/`.
- **`CONTRIBUTING.md`**: sections 3 and 3a rewritten to use `scripts/run_notebooks.sh`
  instead of inline `find | xargs` commands.
- **`docs/4_schema-patterns.md`**: further reading links, code examples, and repository
  examples table updated to new paths; new note in section 5 documenting the
  `workflow/templates/` layer as the workflow-level analogue of `characterization/process/`.
- **`docs/5_llm-schema-guide.md`**: stale `characterization/tensile-test/TTO/` path
  references updated to `characterization/step/tensile-test/TTO/`.

### Fixed

- **`characterization/step/tensile-test/TTO/docs/2_tensile_test_csv_workflow.ipynb`**:
  two bugs introduced by the schema restructuring: (1) `REPO_ROOT = SCHEMA.parents[3]`
  pointed to `schemas/` rather than the repository root, causing a doubled
  `schemas/schemas/` prefix when loading the base shape; (2) `CHAR_BASE` still
  referenced the old `step/PMDCo/` path. Both corrected; `REPO_ROOT` renamed to
  `SCHEMAS` to accurately reflect what it holds.

### Migration

All schemas that reference the old paths must be updated:

| Old path | New path |
|---|---|
| `characterization/step/PMDCo/` | `characterization/step/base/PMDCo/` |
| `characterization/tensile-test/TTO/` | `characterization/step/tensile-test/TTO/` |
| `manufacturing/step/PMDCo/` | `manufacturing/step/base/PMDCo/` |
| `simulation/step/PMDCo/` | `simulation/step/base/PMDCo/` |
| `simulation/model-calibration/PMDCo/` | `simulation/step/model-calibration/PMDCo/` |

Update `conforms_to` IRI filters in SPARQL queries accordingly (see individual
schema CHANGELOGs for the exact old → new IRI mapping).

---

## [0.1.3] - 2026-04-10

### Added

- `obo: "http://purl.obolibrary.org/obo/"` simple-string prefix entry added to
  all schemas that use OBO terms (`characterization/step`, `manufacturing/step`,
  `material-card/mechanical`, `specimen`, `chemical-composition`, `simulation/step`,
  `simulation/model-calibration`, `workflow`). Fixes `ns1`/`ns2`/`ns3`
  auto-generated prefixes in serialised Turtle output.
- `CHANGELOG.md` files at the schema level: `characterization/tensile-test/TTO`
  and `workflow/PMDCo`. Convention documented in `docs/3_schema-format.md` and
  `CONTRIBUTING.md`.
- `docs/3_schema-format.md`: new "Schema versioning and CHANGELOG" section
  documenting MAJOR/MINOR/PATCH rules, schema IRI encoding, and the relationship
  to per-parser CHANGELOGs in `semantic-transformers`.

### Changed

- **`characterization/tensile-test/TTO` schema bumped to v1.1.0** (backwards-compatible):
  - New optional fields: `gauge_length` / `gauge_length_unit`, `preload` / `preload_unit`,
    `test_date` (ISO 8601 datetime).
  - `obo:` prefix added to context so OBO terms serialise with a readable prefix.
- **`workflow/PMDCo` schema bumped to v1.1.0**:
  - Renamed `instance_iri` to `reference` in the simplified input schema, OO-LD
    schema, JSONata transform, notebooks, and `example.input.json`. The field maps
    to `dcterms:references` in RDF; the new name is a plain noun consistent with
    the rest of the schema.
- `semantic_schemas.__init__`: namespace bindings now propagated from the parsed
  JSON-LD Dataset instead of being hard-coded. Adding a prefix to the schema
  `@context` YAML is sufficient; no library changes are needed.
- All notebooks updated: `BASE_IRI` variable, `flat = result.flat_graph`,
  combined-graph cells now propagate namespace bindings when merging sub-graphs.

## [0.1.2] - 2026-04-09

### Fixed

- Removed local Python executable path from all notebook setup cell outputs
- Replaced absolute schema directory paths in notebook outputs with relative
  paths (last three path components, e.g. `characterization/step/PMDCo`)
- Fixed stale cell outputs across all 14 notebooks that contained
  `/root/semantic-dataspace/...` absolute paths from the development machine
- Added `base` parameter to `Schema.parse()` and `Schema.to_graph()` so
  callers can supply a custom base IRI for relative node identifiers; schemas
  without a built-in `@base` (e.g. specimen) no longer produce `file://`
  URIs in their RDF output when a base is provided

### Added

- Git clone and environment setup instructions added to the first cell of all
  14 notebooks so they can be run standalone after downloading from GitHub
- `specimen` notebook now demonstrates the `base` parameter with
  `BASE = "https://example.org/"`, showing how to produce globally-unique IRIs

## [0.1.1] - 2026-04-09

### Fixed

- Add `matplotlib` to dev requirements so notebook CI tests pass

## [0.1.0] - 2026-04-09

### Fixed

- Updated all notebook workflows to use the `semantic_transformers.parsers`
  package import path following the restructuring of `semantic-transformers` v0.1.3
- Replaced outdated `extractor` terminology with `parser` throughout
  `2_tensile_test_csv_workflow.ipynb` (variable names, API calls, prose)
- Fixed broken `meta_field_map` format in Zwick variant examples (values are
  field name strings, not `[name, type]` tuples)
- Suppressed local filesystem paths in notebook cell outputs: save cells now
  print only the filename instead of the full absolute path (all 12 notebooks)

### Added

- Initial public release of semantic-schemas
- OO-LD (Object-Oriented Linked Data) schema definitions for materials science data
- Complete schema library covering:
  - Chemical composition (BWMD, PMDCo)
  - Characterization (step, tensile-test)
  - Manufacturing (step)
  - Material card (mechanical)
  - Simulation (model-calibration, step)
  - Specimen
  - Expertise
  - Workflow
- SHACL validation rules for all schemas
- JSONata transformation templates
- Jupyter notebook workflows for each schema domain
- Comprehensive documentation covering:
  - Concepts and design (docs/1_concepts.md)
  - OO-LD format primer (docs/2_oold-primer.md)
  - Schema format reference (docs/3_schema-format.md)
  - Schema patterns and composition (docs/4_schema-patterns.md)
  - LLM integration guide (docs/5_llm-schema-guide.md)

### Features

- Two-layer schema approach: simplified layer for users, full ontology layer for machines
- Integration with materials science ontologies (DCAT, PMDCo)
- RDF/Turtle output generation
- Automatic validation against SHACL shapes
- Example inputs and complete workflows for each schema

### Documentation

- CATALOG.md: searchable index of all available schemas
- CONTRIBUTING.md: contribution guidelines and workflow
- README.md: quick start guide and installation instructions
- Schema-specific README files with use cases and examples

### Dependencies

- jsonata-python
- rdflib
- pyshacl
- pyyaml

### Requirements

- Python 3.10+

## [Unreleased]

### Planned

- Additional characterization schemas (composition analysis, microscopy)
- Performance and simulation domain extensions
- Custom validators and schema composition tools
- Web-based schema editor interface
- `manufacturing/process/PMDCo/` and `simulation/process/PMDCo/` template layers
  following the `characterization/process/PMDCo/` pattern
