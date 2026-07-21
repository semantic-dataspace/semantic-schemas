# Changelog: Workflow (OBI)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields, new conditions)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes, example updates)

The schema IRI encodes the minor version: `…/OBI/#v<MAJOR>.<MINOR>.0`.

---

## [0.2.0] - 2026-07-17

### Changed

- `type` field const and default changed from a single string (`const: "VALUE"`) to a
  single-element array (`const: ["VALUE"]`) to align with JSON-LD, where `@type`
  naturally supports multiple values.

---

## [0.1.0] - 2026-05-10

### Breaking changes

- Schema completely redesigned: workflow is now a simple ordered list of step
  IRIs (`bfo:has_part` with `@container: @list`) rather than embedded step
  nodes. Steps carry their own structure in domain-specific schema records.
- Root class changed from `bfo:Process` (BFO_0000015) to
  `obi:AnalyticProtocol` (OBI_0000272).
- Simplified input fields changed: `workflow_name` renamed to `label`; `steps`
  is now a plain array of URI strings, not an array of dicts.
- Schema folder renamed from `workflow/PMDCo/` to `workflow/OBI/` to reflect
  that all terms used come from OBI, not PMDCo.
- Version numbering reset to `0.1.0` (SemVer 0.x pre-release convention).

### Migration

Update `conforms_to` IRI filters in SPARQL queries:

```sparql
# old
FILTER(STR(?conformsTo) = "…/workflow/PMDCo/#v2.0.0")
# new
FILTER(STR(?conformsTo) = "…/workflow/OBI/#v0.1.0")
```

Replace embedded step dicts in simplified input with plain IRIs:

```json
{
  "label": "My workflow",
  "steps": [
    "https://example.org/step-1",
    "https://example.org/step-2"
  ]
}
```

---

## [1.1.0] - 2026-04-10

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

## [1.0.0] - initial release

- `bfo:Process` (BFO_0000015) workflow node with `rdfs:label` and
  `rdfs:comment`
- `has_part` (BFO_0000051) linking to embedded step nodes
- Step nodes carry: `type` (ontology class CURIE), `rdfs:label`,
  `rdfs:comment`, `reference` (`dcterms:references`), `preceded_by`
  (BFO_0000062), optional inline `has_process_condition` parameters
- Auto-derivation of step order from array position when `preceded_by`
  is omitted
- SHACL shape validating workflow and step structure
