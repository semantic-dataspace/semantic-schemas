# Schema Format Reference

> **Who is this for?** Schema authors and reviewers.  If you just want to
> record data using an existing schema, start with the schema's `README.md`
> or its notebook instead.

All semantic schemas are YAML files following the OO-LD convention.
See [2_oold-primer.md](2_oold-primer.md) for a plain-language explanation of how
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

`ktypeIds` are the IDs of schema templates made available by DSMS (Dataspace Management System). See [here](/README.md#the-k-item-field-type) for more information.

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

## The `x-transformers` extension

Links this schema to one or more file-based parsers in the
`semantic-transformers` repository. Each entry is a parser ID as declared
in that repository. A parser reads a file (e.g. a measurement export, a
spreadsheet, or any structured data file) and converts it to the schema's
simplified input format.

```yaml
x-transformers: [testxpert_iii]
```

Multiple parsers are allowed:

```yaml
x-transformers: [testxpert_iii, instron_bluehill]
```

Only add `x-transformers` when a working parser exists in `semantic-transformers`
for this schema.

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

- A folder that contains schema files directly (i.e. `specs/`,
  `docs/`) is a **leaf**: it holds a concrete schema. If it sits at the
  `<domain>/<Ontology>/` level it is the **generic base** for that domain.
- A folder that contains only further subfolders is an **intermediate** node:
  it groups specialised variants or sub-domains.

Example for the `manufacturing` domain:

```text
schemas/
  manufacturing/
    generic/
      PMDCo/          ← leaf at domain/generic level  →  generic manufacturing step
      BWMD/           ← leaf                          →  same concept, different ontology
    sintering/
      PMDCo/          ← leaf under a named subfolder  →  specialised sintering step
    welding/
      PMDCo/          ← leaf                          →  specialised welding step
    chain/
      PMDCo/          ← leaf at domain/chain level →  manufacturing process chain
```

Composite schemas (those that reference other schemas via `$ref`) follow the
same rule: their position in the tree signals their role, not a special name.

---

## Leaf folder contents

Every leaf node — the ontology folder at the bottom of the tree — uses the
following standard subfolders and files:

| Path | Purpose |
|---|---|
| `specs/` | All schema files: `schema.oold.yaml`, `shape.ttl`, `schema.simplified.json`, `transform.simplified.jsonata` |
| `docs/` | Notebooks, example files, and the schema `README.md` |
| `CHANGELOG.md` | Version history for this schema (at the leaf root) |

### README summary box

Every schema `README.md` opens with a summary table immediately after the
introductory paragraph:

```html
<table>
<tr><td><strong>Version</strong></td><td><code>2.0.0</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>
<a href="https://github.com/materialdigital/core-ontology/tree/main/patterns/measurement">
PMDCo measurement pattern</a>
</td></tr>
<tr><td><strong>Extends</strong></td><td>—</td></tr>
<tr><td><strong>Includes</strong></td><td>—</td></tr>
<tr><td><strong>Transformers</strong></td><td>
<a href="https://github.com/semantic-dataspace/semantic-transformers/tree/main/
src/semantic_transformers/parsers/characterization/tensile_test/testxpert_iii">
<code>testxpert_iii</code></a>
</td></tr>
</table>
```

| Field | What to put here |
|---|---|
| **Version** | Current `x-schema-version` from `specs/schema.oold.yaml` |
| **Ontology pattern** | Link to the upstream ontology modelling pattern this schema follows (e.g. PMDCo measurement pattern, PMDCo process pattern). Use `—` if no named pattern exists. |
| **Extends** | Link to the schema this one inherits from via `$ref` + `allOf` (inheritance). Use `—` if the schema does not extend another. |
| **Includes** | Link to any schema whose sub-graph is delegated to via `$ref` inside a property (composition). Use `—` if none. |
| **Transformers** | Parser ID(s) from `x-transformers` in `specs/schema.oold.yaml`. Use `—` if none. |

**Extends** and **Includes** correspond to the two structural patterns described
in [4_schema-patterns.md](4_schema-patterns.md): inheritance (`$ref` + `allOf`)
and composition (`$ref` inside a property) respectively. A schema can have
entries in both rows simultaneously.

### Schema versioning

Each schema is versioned independently using [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking changes: renamed or removed fields, incompatible graph structure.
- **MINOR** — backwards-compatible additions: new optional fields, new conditions.
- **PATCH** — corrections that do not affect the graph: typos, description fixes, example updates.

The version is declared in `x-schema-version` inside `schema.oold.yaml` and recorded in the
schema's `CHANGELOG.md`. The repository also carries a global version (`pyproject.toml`, repo tag)
that covers collection-level changes only: manifest format, tooling, Python package.
**Schema content changes do not bump the global version.**

#### Per-schema git tags and stable URLs

Every schema release gets its own git tag:

```text
<domain>-<ontology>-v<version>
tensile-test-PMDCo-v0.2.0
```

This tag is the basis for the stable, resolvable URL used everywhere: in `dcterms:conformsTo`,
in `$ref` resolution, and in tooling:

```text
https://raw.githubusercontent.com/semantic-dataspace/semantic-schemas/<tag>/schemas/<domain>/<Ontology>/specs/schema.oold.yaml
```

Example:

```text
https://raw.githubusercontent.com/semantic-dataspace/semantic-schemas/tensile-test-PMDCo-v0.2.0/schemas/characterization/tensile-test/PMDCo/specs/schema.oold.yaml
```

This URL is stable (immutable tag), resolvable (raw file), and unambiguous (schema version is in the tag, not mixed with the collection version).

#### Provenance stamping

Every schema's `transform.simplified.jsonata` declares a `$schemaUri` pointing to the raw file
at its per-schema tag:

```jsonata
$schemaUri := "https://raw.githubusercontent.com/semantic-dataspace/semantic-schemas/<tag>/schemas/<domain>/<Ontology>/specs/schema.oold.yaml";
```

The transform injects `"conforms_to": $schemaUri` into every output record. Because `conforms_to`
maps to `dcterms:conformsTo` in the `@context`, every generated RDF graph carries:

```turtle
<instance> dcterms:conformsTo <https://raw.githubusercontent.com/…/tensile-test-PMDCo-v0.2.0/…/schema.oold.yaml> .
```

SPARQL consumers can filter on this IRI directly to select records for a specific schema version:

```sparql
FILTER(?schema = <https://raw.githubusercontent.com/…/tensile-test-PMDCo-v0.2.0/…/schema.oold.yaml>)
```

The `manifest.json` also carries a `version` field per entry as a convenience for UI display, so consumers do not need to fetch the YAML to show the version.

#### How to release a schema version

1. Update `x-schema-version` in `specs/schema.oold.yaml`.
2. Update `x-schema-uri` in `specs/schema.oold.yaml` to the new per-schema tag URL.
3. Update `$schemaUri` in `specs/transform.simplified.jsonata` to the same URL.
4. Update `version` in `schemas/manifest.json` for this entry.
5. Add an entry to the schema's `CHANGELOG.md`.
6. Commit and push.
7. Create the per-schema git tag (e.g. `tensile-test-PMDCo-v0.2.0`) pointing to that commit and push it.

Instrument parsers in `semantic-transformers` each keep their own
`CHANGELOG.md` inside the parser folder (e.g.
`parsers/characterization/tensile_test/zwick/CHANGELOG.md`), recording which
schema version each parser release was tested against.

Machine-specific file parsers (programs that read instrument output files
and convert them to the schema's simplified JSON) are **not** stored here.
They live in the companion repository **`semantic-transformers`**, in a
`parsers/` tree that mirrors this repository's `schemas/` tree exactly:

```text
semantic-transformers/
  parsers/
    characterization/
      tensile-test/
        zwick/          ← one folder per instrument model
          zwick_parser.py
          column_mapping.json
          README.md
```

Each parser implements the `Parser` protocol from `semantic-transformers`
and can be plugged into a `Transformer` without changing the schema transform or
the notebook. See the `semantic-transformers` repository for details on adding
support for a new instrument.

---

## Checklist for a valid schema

- [ ] `'@context'` declared
- [ ] All prefix IRIs end with `/` or `#` (to form valid CURIEs)
- [ ] `type` property present, `readOnly: true`, `const` set to the root class CURIE
- [ ] Every property key that should appear in RDF has a corresponding `@context` entry
- [ ] `x-kitem` provided for every `format: kitem` field
- [ ] `x-transformers` declared if one or more parsers exist in `semantic-transformers` for this schema
- [ ] `title` present on every property (used as form label)
- [ ] `description` present on every property (used as tooltip/hint)

---

## Further reading

- [OO-LD primer](2_oold-primer.md): how the schema format works in plain language
- [Schema patterns](4_schema-patterns.md): inheritance (`$ref` + `allOf`) and composition: when to use each, what propagates, what can be overridden, and known limitations
