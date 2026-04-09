# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
