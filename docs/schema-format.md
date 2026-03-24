# Schema Format Reference

All schemas in this store are YAML files following the OO-LD convention. See [oold-primer.md](oold-primer.md) for background.

---

## Top-level structure

```yaml
'@context': { ... }      # required — JSON-LD context
$schema: '...'           # recommended — JSON Schema dialect URI
$comment: '...'          # recommended — machine-readable note / provenance
title: '...'             # required — human-readable schema name
description: '...'       # recommended — longer description
type: object             # required — always 'object' at root level
required: [...]          # list of required property keys
properties: { ... }      # the fields
```

---

## `@context` entries

| Entry form | Meaning |
|---|---|
| `prefix: 'https://...'` | Declares a CURIE prefix for use in `@id` values |
| `type: '@type'` | Maps the key `type` to `rdf:type` |
| `prop: 'prefix:local'` | Maps `prop` to a data property IRI |
| `prop: { '@id': 'prefix:local', '@type': '@id' }` | Maps `prop` to an object property IRI |
| `prop: { '@id': '...', '@container': '@set' }` | Array property (unordered set) |

> **`@base` must not appear in schemas.**
> Instance IRIs are assigned by the deploying system, not by the schema.
> Hardcoding a base IRI would force all deployments to share a namespace they do not own.
> The deployment injects the correct base at serialisation time when converting form payloads to RDF.

---

## The `x-kitem` extension

```yaml
my_field:
  title: My Field
  type: array          # 'string' for single-select
  format: kitem
  x-kitem:
    ktypeIds:
      - some_ktype_id  # one or more ktype IDs from the target knowledge graph
  items:
    type: string
    format: uri
  uniqueItems: true
```

`ktypeIds` are the `ktype_id` values used by the DSMS `/knowledge/search` endpoint to filter results.
They are deployment-specific — coordinate with the DSMS instance you are targeting.

---

## Enum display labels

Use `options.enum_titles` to provide human-readable labels for enum values:

```yaml
unit:
  type: string
  enum:
    - 'uo:0000163'
    - 'uo:0000164'
  options:
    enum_titles:
      - 'mass percentage (%)'
      - 'volume percentage (%)'
```

`enum_titles` is a JSON Schema Extensions convention (used by JSON Editor and this store).

---

## Naming conventions

| Element | Convention | Example |
|---|---|---|
| Schema directory | `schemas/<domain>/<Ontology>/` | `schemas/chemical-composition/PMDCo/` |
| Domain folder | lowercase kebab-case | `chemical-composition` |
| Ontology folder | acronym as used in the community | `PMDCo`, `BWMD`, `EMMO` |
| Property keys | lowercase with underscores | `quality_of`, `element_symbol` |
| CURIE prefixes | lowercase abbreviation | `pmdco`, `bwmd`, `ro`, `obi` |

---

## Checklist for a valid schema

- [ ] `'@context'` declared
- [ ] All prefix IRIs end with `/` or `#` (to form valid CURIEs)
- [ ] `type` property present, `readOnly: true`, `const` set to the root class CURIE
- [ ] Every property key that should appear in RDF has a corresponding `@context` entry
- [ ] `x-kitem` provided for every `format: kitem` field
- [ ] `title` present on every property (used as form label)
- [ ] `description` present on every property (used as tooltip/hint)
