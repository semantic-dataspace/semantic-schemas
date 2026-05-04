# Changelog — Characterization Campaign (PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR** — backwards-compatible additions (new optional fields)
- **PATCH** — corrections that do not affect the graph structure (typos, description fixes)

The schema IRI encodes the minor version: `…/PMDCo/#v<MAJOR>.<MINOR>.0`.

---

## [2.0.0] — 2026-05-04

### Breaking changes

- **Folder renamed** from `characterization/process/PMDCo/` to
  `characterization/campaign/PMDCo/` (renamed to better reflect its role as a
  provenance container for an experiment campaign; no field or graph changes).
- `x-schema-id` updated from `…/characterization/process/PMDCo/` to
  `…/characterization/campaign/PMDCo/`.
- `conforms_to` IRI in all generated records changes accordingly.
- Schema `title` changed from `Characterization Process` to `Characterization Campaign`.
- Default `id` slug changed from `char-process` to `char-campaign`.

### Migration

Update `conforms_to` IRI filters in SPARQL queries:

```sparql
# old
FILTER(?schema = <…/characterization/process/PMDCo/#v1.0.0>)
# new
FILTER(?schema = <…/characterization/campaign/PMDCo/#v2.0.0>)
```

---

## [1.0.0] — 2026-04-13

- Initial release.
- Guided intake schema for a characterization experiment (`obi:Assay`).
- Three required provenance fields:
  - `operator_iri` → `prov:wasAssociatedWith` (expert/technician)
  - `device_iri` → `schema:instrument` (measurement device)
  - `has_specified_input` → specimen IRI
- Optional fields: `step_reference` (`dcterms:references`), `date`
  (`dcterms:date`), `preceded_by`, `has_process_condition`.
- SHACL shape enforcing all three required provenance links.
