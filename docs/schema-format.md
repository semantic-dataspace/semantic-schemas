# Schema Format Reference

> **Who is this for?** Schema authors and reviewers.  If you just want to
> record data using an existing schema, start with the schema's `README.md`
> or its notebook instead.

All semantic schemas are YAML files following the OO-LD convention.
See [oold-primer.md](oold-primer.md) for a plain-language explanation of how
the format works.

---

## Top-level structure

```yaml
'@context': { ... }      # required: JSON-LD context
$schema: '...'           # recommended: JSON Schema dialect URI
$comment: '...'          # recommended: machine-readable note / provenance
title: '...'             # required: human-readable schema name
description: '...'       # recommended: longer description
type: object             # required: always 'object' at root level
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
They are deployment-specific; coordinate with the DSMS instance you are targeting.

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

`enum_titles` is a JSON Schema Extensions convention (used by JSON Editor and the semantic schemas).

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

## Folder structure for multi-schema domains

Some domains (such as process schemas) contain both a generic base schema and
multiple specialised variants. These use one extra level of nesting:

```text
schemas/<domain>/<specialisation>/<Ontology>/
```

The rule for distinguishing generic from specialised within a domain folder is
based on **folder depth, not folder name**:

- A folder that contains schema files directly (i.e. `specs/`, `simplified/`,
  `docs/`) is a **leaf**: it holds a concrete schema. If it sits at the
  `<domain>/<Ontology>/` level it is the **generic base** for that domain.
- A folder that contains only further subfolders is an **intermediate** node:
  it groups specialised variants or sub-domains.

Example for the `manufacturing` domain:

```text
schemas/
  manufacturing/
    step/
      PMDCo/          ← leaf at domain/step level  →  generic manufacturing step
      BWMD/           ← leaf                       →  same concept, different ontology
      sintering/
        PMDCo/        ← leaf under a named subfolder  →  specialised sintering step
      welding/
        PMDCo/        ← leaf                           →  specialised welding step
    chain/
      PMDCo/          ← leaf at domain/chain level →  manufacturing process chain
```

Composite schemas (those that reference other schemas via `$ref`) follow the
same rule: their position in the tree signals their role, not a special name.

---

## Checklist for a valid schema

- [ ] `'@context'` declared
- [ ] All prefix IRIs end with `/` or `#` (to form valid CURIEs)
- [ ] `type` property present, `readOnly: true`, `const` set to the root class CURIE
- [ ] Every property key that should appear in RDF has a corresponding `@context` entry
- [ ] `x-kitem` provided for every `format: kitem` field
- [ ] `title` present on every property (used as form label)
- [ ] `description` present on every property (used as tooltip/hint)

---

## Further reading

- [OO-LD primer](oold-primer.md): how the schema format works in plain language
- [Schema patterns](schema-patterns.md): inheritance (`$ref` + `allOf`) and composition: when to use each, what propagates, what can be overridden, and known limitations
