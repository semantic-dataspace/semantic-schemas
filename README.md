# Semantic Schema Store

A community-curated library of **OO-LD schemas** for materials science and engineering data.

Each schema is a YAML file that combines a [JSON Schema](https://json-schema.org/) form
definition with a [JSON-LD](https://json-ld.org/) `@context`, so that:

- a **web form** can be auto-generated from it (field labels, widgets, validation), and
- the submitted data is automatically serialised as **RDF** according to the chosen ontology.

---

## Repository structure

```text
schemas/                       # Curated schema library
  <domain>/
    <ontology>/
      schema.oold.yaml         # Full OO-LD schema (expert reference)
      shape.ttl                # SHACL validation shape
      example.oold.json        # Complete OO-LD example
      README.md                # Pattern description and quick-start
      simplified/              # User-friendly entry point (where available)
        schema.simplified.json # Plain JSON Schema — start here if new to OO-LD
        example.input.json     # Ready-to-edit example input
        jolt.spec.json         # JOLT spec to convert simplified → OO-LD
templates/
  schema.oold.yaml             # Annotated blank template
docs/
  oold-primer.md               # What is OO-LD and how it works
  schema-format.md             # Field-by-field schema authoring reference
  simplified-input-guide.md    # How to use the simplified/ interface end-to-end
.github/
  ISSUE_TEMPLATE/              # Propose or correct a schema
  PULL_REQUEST_TEMPLATE.md
```

---

## Quick start

### I want to submit data for an existing schema

1. Find the schema in [CATALOG.md](CATALOG.md) and open its folder.
2. If a `simplified/` subfolder exists, copy `simplified/example.input.json` and
   fill in your values — no ontology knowledge required.
3. Follow the [Simplified Input Guide](docs/simplified-input-guide.md) to validate
   your input, convert it to OO-LD JSON with JOLT, and then to RDF.

### I want to understand the full OO-LD format

Read [docs/oold-primer.md](docs/oold-primer.md) and browse a `schema.oold.yaml`
alongside its `README.md` for the pattern explanation.

### I want to contribute a new schema

1. Read [docs/schema-format.md](docs/schema-format.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
2. Copy [templates/schema.oold.yaml](templates/schema.oold.yaml) as your starting point.
3. Open a **New Schema** issue to discuss the pattern before submitting a PR.

---

## Documentation

| Document | Content |
|---|---|
| [docs/oold-primer.md](docs/oold-primer.md) | What OO-LD is and how JSON Schema + JSON-LD combine |
| [docs/schema-format.md](docs/schema-format.md) | Field reference for writing and reviewing schemas |
| [docs/simplified-input-guide.md](docs/simplified-input-guide.md) | End-to-end workflow: fill in data → JOLT → RDF → SHACL validation |

---

## Related projects

| Project | Role |
|---|---|
| [OO-LD](https://github.com/OO-LD/oold-python) | OO-LD specification and Python tooling |
| [PMDCo](https://github.com/materialdigital/core-ontology) | Platform MaterialDigital Core Ontology |
| [BWMD Ontology](https://gitlab.cc-asp.fraunhofer.de/EMI_datamanagement/bwmd_ontology) | BAM/IWM materials ontology |

---

## OO-LD extension: k-items

The schemas in this store extend the base OO-LD convention with a
**`x-kitem` field type** that links a property to a live knowledge graph rather
than a static enum.  A `kitem` field renders as a search-and-select widget
populated from a DSMS instance at runtime.

See [docs/schema-format.md](docs/schema-format.md) for the field syntax.
Background and motivation are described in:

> Nahshon, Y.; Morand, L.; Büschelberger, M.; Helm, D.; Kumaraswamy, K.;
> Zierep, P.; Weber, M.; de Andrés, P. (2025).
> *Semantic Orchestration and Exploitation of Material Data: A Dataspace
> Solution Demonstrated on Steel and Copper Applications.*
> Advanced Engineering Materials, 27(8), 2401448.
> <https://doi.org/10.1002/adem.202401448>

---

## License

Schemas are published under [CC0 1.0 Universal](LICENSE) — no rights reserved.
You may use, adapt, and redistribute them freely, including for commercial purposes, without attribution.
