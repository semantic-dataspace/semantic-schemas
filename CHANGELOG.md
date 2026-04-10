# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
