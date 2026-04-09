# Semantic Schemas

A library of templates for recording materials science data in a way that
machines can read, search, and connect to other datasets.

Each template covers one concept (e.g. *chemical composition*, *specimen*).
You fill in a plain JSON file with your values; the tooling converts it into
**RDF**, a standard format for linked data, using vocabulary from materials
science ontologies such as [DCAT](https://www.w3.org/TR/vocab-dcat-3/) and [PMDCo](https://w3id.org/pmd/co/).

> **New to this?**
> Each schema folder has a Jupyter notebook in `docs/`.
> It walks you through the whole process step by step.

---

## Repository structure

```text
schemas/                       # Schema library
  <domain>/
    <ontology>/
      README.md                # What this schema is for and how to use it
      specs/
        schema.oold.yaml             # Full schema definition (expert reference)
        shape.ttl                    # SHACL validation rules (checks the output RDF)
        schema.simplified.json       # Input field reference
        transform.simplified.jsonata # Converts your input to the structured format
      docs/
        example.input.json     # Ready-to-edit example (start here)
        *.ipynb                # Step-by-step workflow notebook
templates/
  schema.oold.yaml             # Blank template for writing a new schema
docs/
  1_concepts.md                  # How the semantic schemas are designed and why
  2_oold-primer.md               # How the OO-LD schema format works
  3_schema-format.md             # Field-by-field reference for schema authors
  4_schema-patterns.md           # Inheritance and composition between schemas
.github/
  ISSUE_TEMPLATE/              # Propose or correct a schema
  PULL_REQUEST_TEMPLATE.md
```

---

## Installation

### Using pip (recommended)

```bash
pip install semantic-schemas
```

### Development installation

For development or contributions, clone the repository and install in editable mode:

```bash
git clone https://github.com/Semantic-Dataspace/semantic-schemas
cd semantic-schemas
python3 -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Note: The `semantic_schemas` package is used by all workflow notebooks. Without it,
the cells that call `from semantic_schemas import Schema` will fail.

---

## Quick start

### I want to record data for an existing schema

1. Find the schema in [CATALOG.md](CATALOG.md) and open its folder.
2. Copy `docs/example.input.json` and fill in your values (no ontology
   knowledge required).
3. Open the Jupyter notebook in `docs/` and run all cells
   (`Kernel → Restart & Run All`). It converts your file to RDF and validates
   the result automatically.

### I want to understand how the semantic schemas work

Read [docs/1_concepts.md](docs/1_concepts.md) for the big picture: why there are
two schemas per concept (one simple for users, one expert for machines), what
the transform does, and how the pipeline fits together. Then
[docs/2_oold-primer.md](docs/2_oold-primer.md) if you want to go deeper into the
OO-LD (Object-Oriented Linked Data) format itself.

### I want to contribute a new schema

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and conventions.
2. Copy [templates/schema.oold.yaml](templates/schema.oold.yaml) as your
   starting point.
3. Open a **New Schema** issue to discuss the pattern before submitting a PR.

---

## Documentation

| Document | Content |
|---|---|
| [docs/1_concepts.md](docs/1_concepts.md) | How the semantic schemas are designed: two layers, the transform, the full pipeline |
| [docs/2_oold-primer.md](docs/2_oold-primer.md) | How the OO-LD (Object-Oriented Linked Data) schema format works |
| [docs/3_schema-format.md](docs/3_schema-format.md) | Field reference for writing and reviewing schemas |
| [docs/4_schema-patterns.md](docs/4_schema-patterns.md) | Inheritance and composition between schemas |

---

## Related projects

| Project | Role |
|---|---|
| [OO-LD](https://github.com/OO-LD/oold-python) | The schema format specification and Python tooling |
| [PMDCo](https://github.com/materialdigital/core-ontology) | Platform MaterialDigital Core Ontology |
| [BWMD Ontology](https://gitlab.cc-asp.fraunhofer.de/EMI_datamanagement/bwmd_ontology) | Fraunhofer IWM materials ontology |

---

## The k-item field type

Some fields in these schemas link to data containers known as Knowledge Items
(short: k-items) in a live knowledge management system rather than to a static
list of values from an ontology. These containers encapsulate data, metadata,
attachments, executables (apps), and more. In JSON, the value is a URI pointing
to the k-item’s web page.

See [docs/3_schema-format.md](docs/3_schema-format.md) for the field syntax.
Background and motivation:

> Nahshon, Y.; Morand, L.; Büschelberger, M.; Helm, D.; Kumaraswamy, K.;
> Zierep, P.; Weber, M.; de Andrés, P. (2025).
> *Semantic Orchestration and Exploitation of Material Data: A Dataspace
> Solution Demonstrated on Steel and Copper Applications.*
> Advanced Engineering Materials, 27(8), 2401448.
> <https://doi.org/10.1002/adem.202401448>

---

## License

Schemas are published under [CC0 1.0 Universal](LICENSE), with no rights reserved.
You may use, adapt, and redistribute them freely, including for commercial
purposes, without attribution.
