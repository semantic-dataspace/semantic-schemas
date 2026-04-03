# Semantic Schema Store

A library of templates for recording materials science data in a way that
machines can read, search, and connect to other datasets.

Each template covers one concept (e.g. *chemical composition*, *specimen*).
You fill in a plain JSON file with your values; the tooling converts it into
**RDF** — a graph format understood by ontologies such as
[PMDCo](https://w3id.org/pmd/co/) and [BWMD](https://www.iwm.fraunhofer.de/ontologies/bwmd-ontology#).

> **New to this?**
> Start with a Jupyter notebook — each schema folder has one in `docs/`.
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
        example.input.json     # Ready-to-edit example — start here
        *.ipynb                # Step-by-step workflow notebook
      simplified/              # User-friendly entry point
        schema.simplified.json # Input field reference
        transform.jsonata      # Converts your JSON to the structured format
templates/
  schema.oold.yaml             # Blank template for writing a new schema
docs/
  oold-primer.md               # How the schema format works (plain language)
  schema-format.md             # Field-by-field reference for schema authors
  simplified-input-guide.md    # End-to-end guide: fill in data → RDF
.github/
  ISSUE_TEMPLATE/              # Propose or correct a schema
  PULL_REQUEST_TEMPLATE.md
```

---

## Quick start

### I want to record data for an existing schema

1. Find the schema in [CATALOG.md](CATALOG.md) and open its folder.
2. Copy `docs/example.input.json` and fill in your values — no ontology
   knowledge required.
3. Open the notebook in `docs/` and run all cells.  It converts your file to
   RDF and validates the result automatically.

### I want to understand how the format works

Read [docs/oold-primer.md](docs/oold-primer.md) — it explains the idea in
plain language before introducing any technical terms.

### I want to contribute a new schema

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and conventions.
2. Copy [templates/schema.oold.yaml](templates/schema.oold.yaml) as your
   starting point.
3. Open a **New Schema** issue to discuss the pattern before submitting a PR.

---

## Documentation

| Document | Content |
|---|---|
| [docs/oold-primer.md](docs/oold-primer.md) | How the schema format works, in plain language |
| [docs/simplified-input-guide.md](docs/simplified-input-guide.md) | Step-by-step: fill in data → convert → validate |
| [docs/schema-format.md](docs/schema-format.md) | Field reference for writing and reviewing schemas |

---

## Related projects

| Project | Role |
|---|---|
| [OO-LD](https://github.com/OO-LD/oold-python) | The schema format specification and Python tooling |
| [PMDCo](https://github.com/materialdigital/core-ontology) | Platform MaterialDigital Core Ontology |
| [BWMD Ontology](https://gitlab.cc-asp.fraunhofer.de/EMI_datamanagement/bwmd_ontology) | Fraunhofer IWM materials ontology |

---

## The k-item field type

Some fields in these schemas link to entities in a live knowledge graph rather
than a static list of values.  In the DSMS web interface, these render as
search-and-select widgets populated at runtime.  In JSON, the value is a URI
pointing to the knowledge graph entity.

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

Schemas are published under [CC0 1.0 Universal](LICENSE) — no rights reserved.
You may use, adapt, and redistribute them freely, including for commercial
purposes, without attribution.
