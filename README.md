# Semantic Schemas

A library of templates for recording materials science data in a way that
machines can read, search, and connect to other datasets.

Each template covers one concept (e.g. *chemical composition*, *specimen*).
You fill in a plain JSON file with your values; the tooling converts it into
**RDF**, a graph format understood by ontologies such as [DCAT](https://www.w3.org/TR/vocab-dcat-3/) and [PMDCo](https://w3id.org/pmd/co/).

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
        schema.oold.yaml       # Full schema definition (expert reference)
        shape.ttl              # Validation rules (SHACL)
      docs/
        example.input.json     # Ready-to-edit example (start here)
        *.ipynb                # Step-by-step workflow notebook
      simplified/              # User-friendly entry point
        schema.simplified.json # Input field reference
        transform.jsonata      # Converts your JSON to the structured format
templates/
  schema.oold.yaml             # Blank template for writing a new schema
docs/
  concepts.md                  # How the semantic schemas are designed and why
  oold-primer.md               # How the OO-LD schema format works
  schema-format.md             # Field-by-field reference for schema authors
  schema-patterns.md           # Inheritance and composition between schemas
.github/
  ISSUE_TEMPLATE/              # Propose or correct a schema
  PULL_REQUEST_TEMPLATE.md
```

---

## Quick start

### I want to record data for an existing schema

1. Find the schema in [CATALOG.md](CATALOG.md) and open its folder.
2. Copy `docs/example.input.json` and fill in your values (no ontology
   knowledge required).
3. Open the notebook in `docs/` and run all cells.  It converts your file to
   RDF and validates the result automatically.

### I want to understand how the semantic schemas work

Read [docs/concepts.md](docs/concepts.md) for the big picture: why there are
two schemas per concept, what the transform does, and how the pipeline fits
together. Then [docs/oold-primer.md](docs/oold-primer.md) if you want to go
deeper into the OO-LD format itself.

### I want to contribute a new schema

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and conventions.
2. Copy [templates/schema.oold.yaml](templates/schema.oold.yaml) as your
   starting point.
3. Open a **New Schema** issue to discuss the pattern before submitting a PR.

---

## Documentation

| Document | Content |
|---|---|
| [docs/concepts.md](docs/concepts.md) | How the semantic schemas are designed: two layers, the transform, the full pipeline |
| [docs/oold-primer.md](docs/oold-primer.md) | How the OO-LD schema format works |
| [docs/schema-format.md](docs/schema-format.md) | Field reference for writing and reviewing schemas |
| [docs/schema-patterns.md](docs/schema-patterns.md) | Inheritance and composition between schemas |

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

See [docs/schema-format.md](docs/schema-format.md) for the field syntax.
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
