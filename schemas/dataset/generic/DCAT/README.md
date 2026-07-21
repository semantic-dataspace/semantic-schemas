# Dataset Generic (DCAT)

Records **metadata for a single dataset** following the
[W3C Data Catalog Vocabulary (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)
`dcat:Dataset` class.

<table>
<tr><td><strong>Version</strong></td><td><code>0.1.0</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>DCAT Dataset (<code>dcat:Dataset</code>)</td></tr>
<tr><td><strong>Extends</strong></td><td>—</td></tr>
<tr><td><strong>Includes</strong></td><td>—</td></tr>
<tr><td><strong>Transformers</strong></td><td>—</td></tr>
</table>

Use this schema to register a dataset as a knowledge-graph node so that other
schemas (characterization steps, analysis steps, catalogs) can reference it by IRI.
The `has_part` field supports container datasets that aggregate sub-datasets or
documents.

---

## Quick start

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "label": "Tensile test results, 316L batch 1",
  "description": "Force-displacement curves from uniaxial tensile tests on 316L stainless steel, batch 1.",
  "identifier": "doi:10.5281/zenodo.000001",
  "keywords": ["tensile test", "316L", "stainless steel"],
  "format": "CSV",
  "created": "2026-03-10",
  "license": "CC-BY-4.0"
}
```

| Field | Required | Description |
|---|---|---|
| `label` | yes | Human-readable dataset name |
| `description` | no | Free-text description of the dataset content and origin |
| `identifier` | no | External identifier, e.g. a DOI or repository accession number |
| `keywords` | no | Terms describing the dataset subject or topic |
| `format` | no | File format or media type (e.g. `CSV`, `HDF5`, `TIFF`) |
| `created` | no | Creation date in `YYYY-MM-DD` format |
| `modified` | no | Last modification date in `YYYY-MM-DD` format |
| `license` | no | License identifier (e.g. `CC-BY-4.0`, `MIT`) |
| `has_part` | no | IRIs of sub-datasets or documents that are part of this dataset |

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example |
| `specs/schema.oold.yaml` | Full OO-LD schema definition |
| `specs/shape.ttl` | SHACL validation rules |

---

## For the curious: how this maps to the ontology

```text
dcat:Dataset
  rdfs:label              dataset name
  dcterms:description     description  (optional)
  dcterms:identifier      external identifier  (optional)
  dcat:keyword            keyword strings  [× 0..N]  (optional)
  dcterms:format          file format  (optional)
  dcterms:created         creation date  (optional, xsd:date)
  dcterms:modified        last modified date  (optional, xsd:date)
  dcterms:license         license label or IRI  (optional)
  dcterms:hasPart       ─► Dataset IRI or Document IRI  [× 0..N]  (optional)
```

`rdfs:label` is used for the name field to align with the platform k-item label
convention. `dcterms:title` is the strict DCAT equivalent; both predicates are
interchangeable for discovery purposes.

`dcterms:hasPart` expresses structural composition: sub-datasets and documents
that belong to this dataset. For catalog membership (grouping datasets by provenance
or campaign), use `dataset/catalog/DCAT` instead.

---

## Further reading

- [Usage guide](../../../../docs/6_usage-guide.md): how to convert `example.input.json` to RDF and validate it with SHACL
- [OO-LD primer](../../../../docs/2_oold-primer.md): how the schema format works

---

## Related schemas

- [Dataset Catalog (DCAT)](../../catalog/DCAT/README.md): groups multiple datasets under a single catalog node
- [Data Analysis Generic (PMDCo)](../../data-analysis/generic/PMDCo/README.md): analysis steps that consume and produce datasets
- [Workflow (OBI)](../../workflow/OBI/README.md): ordered container of process step IRIs
