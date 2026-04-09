# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-09

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
