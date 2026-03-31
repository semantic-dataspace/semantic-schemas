# Expertise

Schema for describing the **expertise profile of a domain expert** in materials
science.  An expert (`foaf:Person`) is linked to sets of knowledge graph
entities representing their areas of expertise across six categories.

---

## Graph pattern

```text
foaf:Person
  schema:knowsAbout ──► <material URI>          [0..*]
  schema:knowsAbout ──► <simulation URI>         [0..*]
  schema:knowsAbout ──► <measurement_device URI> [0..*]
  schema:knowsAbout ──► <production_device URI>  [0..*]
  schema:knowsAbout ──► <application_field URI>  [0..*]
  schema:knowsAbout ──► <method URI>             [0..*]
```

Key modelling decisions:

- All six expertise categories map to the same RDF property
  `schema:knowsAbout`.  The semantic distinction between materials, methods,
  devices, etc. is carried by the `rdf:type` of the referenced knowledge graph
  entity, not by separate property IRIs.
- Each value is a URI (k-item) pointing to an entity in the DSMS knowledge
  graph.  In the DSMS web interface, users pick from a searchable list; they do
  not type URIs manually.

> **Known limitation:** a pure SPARQL query on raw triples cannot distinguish
> "expertise in materials" from "expertise in methods" without joining on the
> `rdf:type` of the referenced entity.  Sub-properties of `schema:knowsAbout`
> are planned in a future schema-store vocabulary.

---

## Expertise categories

| Field | k-item type | Examples |
|---|---|---|
| `materials` | `material` | steel grades, alloys, polymers |
| `material_modelling` | `simulation` | DFT, FEM, MD, CALPHAD |
| `measurement_devices` | `measurement_device` | SEM, XRD, TEM, nanoindenter |
| `production_devices` | `production_device` | LPBF printer, arc furnace |
| `application_fields` | `application_field` | aerospace, automotive, biomedical |
| `methods` | `method` | EBSD, tensile testing, hardness mapping |

---

## Input format

There is no simplified layer for this schema — the OO-LD JSON is already
user-friendly.  Fill in the URI arrays for each relevant category and omit
categories where the expert has no expertise.

```json
{
  "type": "foaf:Person",
  "materials": [
    "https://dsms.example.org/api/knowledge/mat-steel-316l"
  ],
  "measurement_devices": [
    "https://dsms.example.org/api/knowledge/dev-sem",
    "https://dsms.example.org/api/knowledge/dev-xrd"
  ],
  "methods": [
    "https://dsms.example.org/api/knowledge/method-ebsd"
  ]
}
```

A complete example is in [`example.oold.json`](example.oold.json).

---

## Convert to RDF (Python)

```bash
pip install rdflib pyyaml
```

```python
import json, yaml, rdflib

context = yaml.safe_load(open("schema.oold.yaml"))["@context"]
doc     = json.load(open("example.oold.json"))

g = rdflib.Dataset()
g.parse(data=json.dumps({"@context": context, **doc}), format="json-ld")
g.serialize(destination="my_output.ttl", format="turtle")
```

---

## Files in this folder

| File | Purpose |
|---|---|
| `schema.oold.yaml` | Full OO-LD / JSON-LD schema |
| `example.oold.json` | Complete example expertise profile |
| `notebooks/expertise_workflow.ipynb` | Jupyter notebook (OO-LD JSON → RDF) |

---

## Further reading

- [OO-LD primer](../../docs/oold-primer.md) — what OO-LD is and how it works
- [Schema format reference](../../docs/schema-format.md) — field-by-field reference
