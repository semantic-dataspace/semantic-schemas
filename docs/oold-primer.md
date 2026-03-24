# OO-LD Primer

## What is OO-LD?

**Object-Oriented Linked Data (OO-LD)** is a convention for combining two standards in a single document:

- **JSON Schema** — describes the *shape* of a data object (fields, types, validation, UI hints)
- **JSON-LD `@context`** — maps every field name to an ontology IRI, making the object interpretable as RDF

The result is a schema that simultaneously serves as a form specification and a semantic data contract.

Reference implementation: [github.com/OO-LD/oold-python](https://github.com/OO-LD/oold-python)

---

## Why use it for a schema store?

| Concern | How OO-LD addresses it |
|---|---|
| Form generation | JSON Schema drives widget selection, labels, validation |
| Semantic interoperability | JSON-LD context maps fields to stable ontology IRIs |
| Multi-ontology support | Each schema file is independent; competing patterns coexist |
| Human readability | YAML syntax; property names are English, not IRI fragments |
| Tooling compatibility | Standard JSON Schema validators work without modification |

---

## Anatomy of an OO-LD schema

```yaml
# ── 1. JSON-LD context ──────────────────────────────────────────────────────
'@context':
  pmdco: 'https://w3id.org/pmd/co/'
  ro:    'http://purl.obolibrary.org/obo/RO_'
  '@base': 'https://example.org/instances#'
  type:  '@type'           # 'type' key maps to rdf:type
  quality_of:
    '@id':  'ro:0000080'   # expands to full IRI using the 'ro' prefix
    '@type': '@id'         # value is an IRI (object property)

# ── 2. JSON Schema ──────────────────────────────────────────────────────────
$schema: 'https://json-schema.org/draft/2020-12/schema'
title: ChemicalComposition
type: object
required:
  - type
properties:
  type:
    type: string
    readOnly: true
    const: 'pmdco:PMD_0000551'   # hidden; drives rdf:type in generated RDF
  quality_of:
    title: Material
    type: string
    format: kitem                 # x- extension: renders as a k-item picker
    x-kitem:
      ktypeIds: [material]
```

---

## How fields become RDF

Given the context above and a form submission:

```json
{ "type": "pmdco:PMD_0000551", "quality_of": "https://example.org/mat/42" }
```

The JSON-LD processor expands this to:

```turtle
_:instance
    rdf:type <https://w3id.org/pmd/co/PMD_0000551> ;
    <http://purl.obolibrary.org/obo/RO_0000080> <https://example.org/mat/42> .
```

---

## The `x-kitem` extension

Fields that reference existing knowledge graph entities use the `format: kitem` marker and an `x-kitem` extension object:

```yaml
my_field:
  type: array          # or string for single selection
  format: kitem
  x-kitem:
    ktypeIds:
      - material       # ktype_id values understood by the DSMS knowledge graph
```

This is a valid JSON Schema extension (`x-` prefix is reserved for custom vocabulary).
Validators ignore it; the webform-builder uses it to render a searchable k-item picker filtered by type.

---

## The `type` property convention

Every OO-LD schema in this store uses a hidden `type` property to carry the `rdf:type` of the instance:

```yaml
type:
  type: string
  readOnly: true
  const: 'pmdco:PMD_0000551'
```

- `readOnly: true` causes the webform-builder to skip rendering it as a user input.
- The CURIE (`pmdco:PMD_0000551`) is expanded to a full IRI at serialisation time using the `@context` prefix map.
- This value becomes the `classMapping` of the generated `Webform` object.
