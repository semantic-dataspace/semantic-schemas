# Concepts: how semantic schemas are designed

A short introduction for readers who want to understand the *why* before
opening a notebook or reading a reference document.

---

## Motivation

### Knowledge modeling is a matter of perspective

There is rarely a single correct way to model a materials science concept.
A chemical composition can be described as a set of element fractions, a
min-max specification, or a nominal target. Each framing is valid for
different use cases, and different communities have built different ontologies
around each.

Rather than picking one perspective and forcing everyone to adopt it, the
semantic schemas let multiple representations coexist. Each schema is an
independent unit: schemas for the same concept but different ontologies sit
side by side, and the most useful ones naturally attract the most adoption.

### Complex knowledge as composable building blocks

Real materials data rarely fits into a single flat record. A specimen has a
composition. A workflow is a chain of process steps. Each of those steps
may reference simulation results or characterization outputs.

Semantic schemas address this by decomposing knowledge into small, focused
units that can be composed together. A specimen schema formally depends on a
chemical composition schema; a workflow schema chains together step schemas.
This keeps each schema simple and reusable while still allowing complex,
multi-entity records to be assembled from them.

### Interoperability without ontology expertise

The hard part of knowledge modeling (choosing the right ontology classes,
defining the RDF graph structure, writing SHACL validation rules) is done
once and encoded in the schema. Users of the schema are not asked to
understand any of that. They fill in a plain JSON file with their measurement
values; the toolchain handles the rest.

The goal is interoperability with low technological and onboarding barriers:
a researcher should be able to produce ontology-compliant, machine-readable
data without knowing what an IRI is.

---

## The two layers

Each schema consists of two distinct artefacts that reflect the separation
between knowledge modeling and data entry.

### The simplified schema (the user layer)

`specs/schema.simplified.json` is a plain [JSON Schema](https://json-schema.org/).
Its field names are readable English words, its descriptions explain each
value in plain language, and it carries no ontology-specific content. A user
fills in `docs/example.input.json` guided by this schema, with no IRI knowledge
required.

```json
{
  "step_name": "Sintering run 42",
  "conditions": [
    { "name": "Sintering temperature", "value": 1050, "unit": "°C" }
  ]
}
```

### The OO-LD schema (the expert layer)

`specs/schema.oold.yaml` is the authoritative definition. It follows the
[OO-LD (Object-Oriented Linked Data)](https://github.com/OO-LD/oold-python)
convention: a single YAML file that combines a JSON Schema (structure and
validation) with a JSON-LD `@context` (ontology mapping). From this one file
the toolchain can build a form, map field names to ontology IRIs, produce RDF
triples, and run SHACL validation, all without further configuration.

You rarely need to open this file unless you are writing or reviewing a schema.
[2_oold-primer.md](2_oold-primer.md) explains the format in detail.

---

## The transform: bridging the two layers

The simplified input is deliberately flat and human-readable. The OO-LD schema
expects a specific nested structure with typed nodes, stable IDs, and ontology
class assignments. The file that bridges these two representations is
`specs/transform.simplified.jsonata`.

It is a short program written in [JSONata](https://jsonata.org), a lightweight
query and transformation language for JSON. The transform:

- assigns the correct ontology class CURIE to each node's `type` field
- builds the nested node hierarchy from flat input fields
- generates stable identifiers from human-readable names
- conditionally includes optional sub-nodes only when the input provides them

Because the transform is part of the schema definition, the mapping logic
lives in one place and evolves together with the schema. Users never interact
with it directly.

---

## The full pipeline

```text
docs/example.input.json
  │
  │  specs/transform.simplified.jsonata
  ▼
OO-LD JSON document          ← structured JSON-LD with typed nodes
  │
  │  rdflib + specs/schema.oold.yaml @context
  ▼
RDF graph (Turtle)           ← machine-readable linked data
  │
  │  pyshacl + specs/shape.ttl
  ▼
Validation report            ← confirms the graph is ontologically correct
```

The notebook in `docs/` runs every stage and shows the output at each step.

---

## What you provide vs. what happens automatically

This table shows where your effort is needed and what the toolchain handles for you.

| Stage | What you provide | What is automatic |
|---|---|---|
| Input | Your measurement values | Field names, types, which are required |
| Structuring | Nothing | Transform assigns class IRIs, builds node hierarchy |
| RDF conversion | Nothing | `rdflib` reads `@context`, maps keys to property IRIs |
| Validation | Nothing | `pyshacl` checks the graph against `shape.ttl` |

---

## How schemas relate to one another

Schemas are not isolated. A specimen schema may *compose* a chemical
composition schema (the specimen record embeds a full composition sub-graph
produced by the composition schema's own transform). A tensile test schema
may *extend* a generic characterization step schema (inheriting its fields
and adding test-specific result nodes). [4_schema-patterns.md](4_schema-patterns.md)
explains these relationships in detail.

---

## Where to go next

| Goal | Where to look |
|---|---|
| Record data with an existing schema | Open the notebook in the schema folder (see [CATALOG.md](../CATALOG.md)) |
| Understand the OO-LD format in depth | [2_oold-primer.md](2_oold-primer.md) |
| Write a new schema | [CONTRIBUTING.md](../CONTRIBUTING.md) and [3_schema-format.md](3_schema-format.md) |
| Understand inheritance and composition | [4_schema-patterns.md](4_schema-patterns.md) |
