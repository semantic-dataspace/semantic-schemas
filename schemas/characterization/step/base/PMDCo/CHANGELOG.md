# Changelog — Characterization Step (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR** — backwards-compatible additions (new optional fields)
- **PATCH** — corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `…/base/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [2.0.0] — 2026-04-13

### Changed

- **Folder renamed** from `characterization/step/PMDCo/` to
  `characterization/step/base/PMDCo/` as part of a domain-wide restructuring
  that introduces a `step/` sub-level for all characterization variants
  (base, tensile-test, …) and a new `process/` level for guided intake schemas.
- `x-schema-id` updated to reflect the new path.
- `conforms_to` IRI in generated RDF now points to the new versioned path.

### Migration

The generated RDF graph structure is **unchanged**; only the provenance IRI
(`dcterms:conformsTo`) differs.  Update any `conforms_to` filters in SPARQL
queries or dashboards that check for the old v1 IRI:

```sparql
# old
FILTER(?schema = <…/characterization/step/PMDCo/#v1.0.0>)
# new
FILTER(?schema = <…/characterization/step/base/PMDCo/#v2.0.0>)
```

---

## [1.0.0] — initial release (at path characterization/step/PMDCo/)

- `obi:Assay` (OBI_0000070) node with `rdfs:label` and `dcterms:conformsTo`
- `has_specified_input` linking to specimen/material IRIs
- `preceded_by` for process chain ordering
- `has_process_condition` for quantitative test parameters (PMDCo ProcessCondition)
- SHACL shape validating the above structure
