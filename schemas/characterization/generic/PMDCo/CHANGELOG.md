# Changelog: Characterization Generic (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `…/generic/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [0.1.0] - 2026-05-10

### Changed

- Version numbering reset to `0.1.0`. All schemas in this repository adopted
  the SemVer convention that major version 0 signals a pre-release draft. No
  field or graph changes.

### Migration

Update `conforms_to` IRI filters in SPARQL queries:

```sparql
# old
FILTER(STR(?conformsTo) = "…/characterization/generic/#v3.0.0")
# new
FILTER(STR(?conformsTo) = "…/characterization/generic/#v0.1.0")
```

---

## [3.0.0] - 2026-05-04

### Breaking changes

- **Folder renamed** from `characterization/step/base/PMDCo/` to
  `characterization/generic/PMDCo/` (domain-wide restructuring that removes the
  misleading `step/` intermediate level; no field or graph changes).
- `x-schema-id` updated from `…/characterization/step/base/PMDCo/` to
  `…/characterization/generic/PMDCo/`.
- `conforms_to` IRI in all generated records changes accordingly.
- Schema `title` changed from `Characterization Step` to `Characterization Generic`.
- Default `id` value changed from `characterization-step` to `characterization-generic`.

### Migration

Update `conforms_to` IRI filters in SPARQL queries:

```sparql
# old
FILTER(?schema = <…/characterization/step/base/PMDCo/#v2.0.0>)
# new
FILTER(?schema = <…/characterization/generic/PMDCo/#v3.0.0>)
```

---

## [2.0.0] - 2026-04-13

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

## [1.0.0] - initial release (at path characterization/step/PMDCo/)

- `obi:Assay` (OBI_0000070) node with `rdfs:label` and `dcterms:conformsTo`
- `has_specified_input` linking to specimen/material IRIs
- `preceded_by` for process chain ordering
- `has_process_condition` for quantitative test parameters (PMDCo ProcessCondition)
- SHACL shape validating the above structure
