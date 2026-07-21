# Dataset Catalog (DCAT)

Records a **named collection of datasets** following the
[W3C Data Catalog Vocabulary (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)
`dcat:Catalog` class.

<table>
<tr><td><strong>Version</strong></td><td><code>0.1.1</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>DCAT Catalog (<code>dcat:Catalog</code>)</td></tr>
<tr><td><strong>Extends</strong></td><td><a href="../generic/DCAT/README.md">dataset/generic/DCAT</a></td></tr>
<tr><td><strong>Includes</strong></td><td>—</td></tr>
<tr><td><strong>Transformers</strong></td><td>—</td></tr>
</table>

Use this schema to group datasets that belong to the same measurement campaign,
project, or provenance context. Each member dataset is recorded independently with
`dataset/generic/DCAT` and referenced here by IRI. The catalog node provides
a single discoverable entry point for the whole collection.

---

## Quick start

1. Record each dataset with [`dataset/generic/DCAT`](../generic/DCAT/README.md) first.
2. Note the IRI assigned to each dataset instance.
3. Fill in this form, pasting the dataset IRIs into the **Datasets** list.

```json
{
  "label": "316L Stainless Steel: Measurement Campaign 1",
  "description": "Catalog grouping all measurement and analysis datasets from the first 316L characterization campaign.",
  "keywords": ["316L", "stainless steel", "measurement campaign"],
  "created": "2026-03-10",
  "dataset": [
    "https://example.org/datasets/tensile-raw-316L-batch-1",
    "https://example.org/datasets/yield-strength-316L-batch-1"
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `label` | yes | Human-readable catalog name |
| `description` | no | Free-text summary of the collection scope |
| `keywords` | no | Terms describing the collection topic |
| `identifier` | no | External identifier (e.g. DOI, repository accession) |
| `created` | no | Creation date in `YYYY-MM-DD` format |
| `modified` | no | Last modification date in `YYYY-MM-DD` format |
| `license` | no | License identifier (e.g. `CC-BY-4.0`) |
| `dataset` | no | IRIs of member datasets listed in this catalog |

All fields from `dataset/generic/DCAT` are available; only the fields most
relevant to catalog use are listed above.

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example |
| `specs/schema.oold.yaml` | Full OO-LD schema definition |
| `specs/shape.ttl` | SHACL validation rules (load together with `../generic/DCAT/specs/shape.ttl`) |

---

## For the curious: how this maps to the ontology

```text
dcat:Catalog  (subclass of dcat:Dataset)
  [all fields from dataset/generic/DCAT]
  dcat:dataset ──────────────────────────► Dataset IRI  [× 0..N]
```

`dcat:Catalog` is a subclass of `dcat:Dataset` in DCAT 3, so all dataset metadata
fields apply. The `dcat:dataset` property links the catalog to its member datasets.

---

## Further reading

- [Usage guide](../../../../docs/6_usage-guide.md): how to convert `example.input.json` to RDF and validate it with SHACL
- [OO-LD primer](../../../../docs/2_oold-primer.md): how the schema format works

---

## Related schemas

- [Dataset Generic (DCAT)](../generic/DCAT/README.md): schema for individual datasets listed in this catalog
- [Data Analysis Generic (PMDCo)](../../data-analysis/generic/PMDCo/README.md): analysis steps that reference datasets by IRI
- [Workflow (OBI)](../../workflow/OBI/README.md): ordered container of process step IRIs
