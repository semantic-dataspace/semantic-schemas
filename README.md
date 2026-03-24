# Semantic Schema Store

A community-curated library of **OO-LD schemas** for materials science and engineering data.

Each schema is a single YAML file that combines a [JSON Schema](https://json-schema.org/) form definition with a [JSON-LD](https://json-ld.org/) `@context`, so that:

- a **web form** can be auto-generated from it (field labels, widgets, validation), and
- the submitted data is automatically serialised as **RDF** according to the chosen ontology.

---

## Repository structure

```text
schemas/                  # Curated schema library
  <domain>/
    <ontology>/
      schema.oold.yaml    # The schema itself
templates/
  schema.oold.yaml        # Annotated blank template
docs/
  oold-primer.md          # What is OO-LD?
  schema-format.md        # Field reference
.github/
  ISSUE_TEMPLATE/         # Propose or correct a schema
  PULL_REQUEST_TEMPLATE.md
```

---

## Quick start

### Browse available schemas

See [CATALOG.md](CATALOG.md) for the full list.

---

## Contributing a schema

1. Read [docs/schema-format.md](docs/schema-format.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
2. Copy [templates/schema.oold.yaml](templates/schema.oold.yaml) as your starting point.
3. Open a **New Schema** issue to discuss the pattern before submitting a PR.

---

## Related projects

| Project | Role |
|---|---|
| [OO-LD](https://github.com/OO-LD/oold-python) | OO-LD specification and Python tooling |
| [PMDCo](https://github.com/materialdigital/core-ontology) | Platform MaterialDigital Core Ontology |
| [BWMD Ontology](https://gitlab.cc-asp.fraunhofer.de/EMI_datamanagement/bwmd_ontology) | BAM/IWM materials ontology |

---

## License

Schemas are published under [CC-BY 4.0](LICENSE). You are free to use and adapt them with attribution.
