# How the schema format works

---

## The idea in plain language

Each schema in the semantic schemas collection does two jobs at once:

1. **Defines a form**: which fields exist, what type of value each takes,
   which are required, and what labels and hints to show in a UI.
2. **Maps each field to an ontology term**: when you fill in the form,
   the result can be automatically written as RDF, the standard format for
   linked scientific data.

You interact with job 1 (fill in `example.input.json`, run the notebook).
Job 2 happens automatically in the background.

The format that combines these two jobs is called
**OO-LD (Object-Oriented Linked Data)**.  You do not need to understand
OO-LD to use the schemas. This document is for people who want to know
what is happening under the hood, or who want to write their own schema.

Reference implementation: [github.com/OO-LD/oold-python](https://github.com/OO-LD/oold-python)

---

## The two layers

An OO-LD schema is a YAML file with two sections:

| Section | Standard | Purpose |
|---|---|---|
| `@context` | JSON-LD | Maps field names to ontology IRIs |
| everything else | JSON Schema | Defines fields, types, validation, UI hints |

### Layer 1: JSON Schema (the form)

JSON Schema is a widely used format for describing the structure of a JSON
object.  It specifies which fields are required, what type each value must be
(string, number, array, …), allowed values, labels, and descriptions.  Any
JSON Schema validator or form builder can read it.

### Layer 2: JSON-LD `@context` (the ontology mapping)

JSON-LD is a standard for writing linked data as JSON.  The `@context` block
is a lookup table: it says "whenever you see the key `quality_of`, treat it as
the RDF property `http://purl.obolibrary.org/obo/RO_0000080`."

Because the two layers live in the same file, no separate mapping step is
needed; the context is always in sync with the schema.

---

## A minimal example

```yaml
# ── Layer 1: JSON-LD context ────────────────────────────────────────────────
'@context':
  pmdco: 'https://w3id.org/pmd/co/'
  ro:    'http://purl.obolibrary.org/obo/RO_'
  type:  '@type'           # the key 'type' becomes rdf:type
  quality_of:
    '@id':   'ro:0000080'  # expands to the full IRI using the 'ro' prefix
    '@type': '@id'         # value is an IRI (a link to another node)

# ── Layer 2: JSON Schema ────────────────────────────────────────────────────
$schema: 'https://json-schema.org/draft/2020-12/schema'
title: ChemicalComposition
type: object
required:
  - type
properties:
  type:
    type: string
    readOnly: true
    const: 'pmdco:PMD_0000551'   # hidden; sets rdf:type in the generated RDF
  quality_of:
    title: Material
    type: string
    format: kitem                # custom extension: renders as a search widget
    x-kitem:
      ktypeIds: [material]
```

---

## How a field value becomes an RDF triple

Given the context above and a filled-in JSON document:

```json
{ "type": "pmdco:PMD_0000551", "quality_of": "https://example.org/mat/42" }
```

A JSON-LD processor expands this to:

```turtle
_:instance
    rdf:type  <https://w3id.org/pmd/co/PMD_0000551> ;
    <http://purl.obolibrary.org/obo/RO_0000080>  <https://example.org/mat/42> .
```

The `pmdco:` prefix in the value is expanded using the declared prefix, and
`quality_of` becomes the full property IRI, via the `@context`.

---

## The `type` property convention

Every OO-LD schema here uses a hidden `type` property to set the
`rdf:type` of the instance:

```yaml
type:
  type: string
  readOnly: true
  const: 'pmdco:PMD_0000551'
```

- `readOnly: true` marks it as a system value (not shown as an editable field).
- The value (a CURIE) is expanded to a full IRI at serialisation time.

---

## The `x-kitem` extension

Fields that reference data container (called knowledge items) use `format: kitem` and an `x-kitem` block:

```yaml
my_field:
  type: array          # or string for single selection
  format: kitem
  x-kitem:
    ktypeIds:
      - material       # entity type
```

`x-` prefixed keys are a standard JSON Schema extension mechanism; validators
silently ignore them.

---

## Why are ontology IRIs so long?

Ontology IRIs are designed to be globally unique and stable for decades.
They are not meant to be typed by hand; the `@context` prefix map takes care
of that.  In schemas, you write `pmdco:PMD_0000551`; only the serialiser
ever sees the full IRI.

---

## Further reading

- [Concepts](1_concepts.md): how the two-layer design works and why
- [Schema format reference](3_schema-format.md): field-by-field reference for writing schemas
