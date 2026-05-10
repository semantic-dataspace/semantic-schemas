# Expertise (VIVO)

Records the **scientific expertise and device experience** of a person using
the VIVO ontology. Research areas and device experience are populated from
the [Materials Dataspace vocabulary](https://vocabulary.materials-data.space/)
at runtime, so the form always reflects the current controlled vocabulary.

<table>
<tr><td><strong>Version</strong></td><td><code>0.1.0</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>VIVO Core 1.15 / FOAF (<code>foaf:Person</code>)</td></tr>
<tr><td><strong>Extends</strong></td><td>—</td></tr>
<tr><td><strong>Includes</strong></td><td>—</td></tr>
<tr><td><strong>Transformers</strong></td><td>—</td></tr>
</table>

---

## About VIVO and when to use this schema

[VIVO](https://wiki.lyrasis.org/spaces/VIVODOC/pages/70588832/All+Documentation)
is a scholarly networking ontology originally developed at Cornell University
and now maintained by Lyrasis. It is designed to represent researchers, their
affiliations, publications, grants, and most importantly their **areas of
expertise and instrument experience**. VIVO's predicates are used in hundreds
of institutional research-information systems worldwide, making VIVO-expressed
expertise profiles directly interoperable with those systems.

**Use this schema when:**

- Records must integrate with institutional CRIS/VIVO systems or SPARQL endpoints
  that query `vivo:hasResearchArea` / `vivo:hasExperienceIn` directly
- You need to distinguish **scientific domain expertise** (research areas) from
  **hands-on instrument experience** (device expertise) at the predicate level —
  not just by the type of the referenced entity
- Provenance or federation with external research-information infrastructure matters

### How this differs from Expertise (schema.org)

| | Expertise (VIVO) — **this schema** | Expertise (schema.org) — *deprecated* |
|---|---|---|
| Ontology | VIVO Core 1.15 | schema.org |
| Research-area predicate | `vivo:hasResearchArea` | `schema:knowsAbout` |
| Device-experience predicate | `vivo:hasExperienceIn` | `schema:knowsAbout` |
| Predicate-level distinction | Yes — two predicates | No — one flat predicate |
| Ecosystem fit | CRIS / VIVO systems | General web / schema.org consumers |

The key difference is **predicate granularity**: VIVO uses two distinct
properties so a SPARQL query can separate "knows this material" from "has
operated this instrument" without joining on the type of the target node.
The schema.org variant maps everything to `schema:knowsAbout`, which is simpler
but loses that distinction.

---

## Fields

| Field | Required | Vocabulary namespace | Predicate |
|---|---|---|---|
| `label` | yes | — | `rdfs:label` |
| `materials` | no | `material` | `vivo:hasResearchArea` |
| `material_modelling` | no | `material-modelling` | `vivo:hasResearchArea` |
| `application_fields` | no | `application-field` | `vivo:hasResearchArea` |
| `methods` | no | `method` | `vivo:hasResearchArea` |
| `measurement_devices` | no | `measurement-device` | `vivo:hasExperienceIn` |
| `production_devices` | no | `production-device` | `vivo:hasExperienceIn` |

All multi-value fields are serialised as `@set` in JSON-LD.

---

## How this maps to the ontology

```text
foaf:Person
  rdfs:label            person name
  vivo:hasResearchArea ─► material IRI  [× 0..N]
  vivo:hasResearchArea ─► material modelling IRI  [× 0..N]
  vivo:hasResearchArea ─► application field IRI  [× 0..N]
  vivo:hasResearchArea ─► method IRI  [× 0..N]
  vivo:hasExperienceIn ─► measurement device IRI  [× 0..N]
  vivo:hasExperienceIn ─► production device IRI  [× 0..N]
```

---

## Vocabulary source

All option lists are fetched at form-load time from:

```text
https://vocabulary.materials-data.space/api/vocabulary/namespaces/<namespace>/use-cases/base/terms
```

where `<namespace>` is one of `material`, `material-modelling`,
`application-field`, `method`, `measurement-device`, `production-device`.

---

## Related schemas

- [Expertise (schema.org)](../schema.org/README.md) — deprecated predecessor; used `schema:knowsAbout` for all fields
- [Measurement Device (PMDCo)](../../measurement-device/PMDCo/README.md)
