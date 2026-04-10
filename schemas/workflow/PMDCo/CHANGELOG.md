# Changelog — Cross-Domain Workflow (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR** — backwards-compatible additions (new optional fields, new conditions)
- **PATCH** — corrections that do not affect the graph structure (typos, description fixes, example updates)

The schema IRI encodes the minor version: `…/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [1.1.0] — 2026-04-10

### Changed

- Renamed `instance_iri` → `reference` in the simplified input schema,
  the OO-LD schema, the JSONata transform, notebooks, and `example.input.json`.
  The field maps to `dcterms:references` in RDF; the new name is a plain noun
  consistent with the rest of the schema and avoids confusion with the step's
  own IRI.

### Migration

Rename the key in any existing simplified JSON inputs:

```json
{ "instance_iri": "https://..." }  →  { "reference": "https://..." }
```

The generated RDF triple is unchanged (`dcterms:references`).

---

## [1.0.0] — initial release

- `bfo:Process` (BFO_0000015) workflow node with `rdfs:label` and
  `rdfs:comment`
- `has_part` (BFO_0000051) linking to embedded step nodes
- Step nodes carry: `type` (ontology class CURIE), `rdfs:label`,
  `rdfs:comment`, `reference` (`dcterms:references`), `preceded_by`
  (BFO_0000062), optional inline `has_process_condition` parameters
- Auto-derivation of step order from array position when `preceded_by`
  is omitted
- SHACL shape validating workflow and step structure
