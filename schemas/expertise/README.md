# Expertise

Records the **areas of expertise of a materials science researcher**: which
materials, methods, devices, and application fields they work with.

Each value is a link to a data container referred to as knowledge item (or k-item for short).

---

## Quick start

**The fastest way in:** open the notebook.

```bash
pip install jupyterlab
jupyter lab docs/expertise_workflow.ipynb
```

### Input fields

Copy [`docs/example.oold.json`](docs/example.oold.json) and fill in your
values.  Each field is an array of URIs; leave out any category where the
person has no expertise.

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

| Field | k-item type | Examples |
|---|---|---|
| `materials` | `material` | steel grades, alloys, polymers |
| `material_modelling` | `simulation` | DFT, FEM, MD, CALPHAD |
| `measurement_devices` | `measurement_device` | SEM, XRD, TEM, nanoindenter |
| `production_devices` | `production_device` | LPBF printer, arc furnace |
| `application_fields` | `application_field` | aerospace, automotive, biomedical |
| `methods` | `method` | EBSD, tensile testing, hardness mapping |

> **No transform step:** this schema has no `simplified/` folder; the input
> JSON is already in the structured format.  Just fill in the URIs and convert.

### Convert to RDF (Python)

```bash
pip install rdflib pyyaml
```

```python
import json, yaml, rdflib

context = yaml.safe_load(open("specs/schema.oold.yaml"))["@context"]
doc     = json.load(open("docs/example.oold.json"))

g = rdflib.Dataset()
g.parse(data=json.dumps({"@context": context, **doc}), format="json-ld")
g.serialize(destination="output_expertise.ttl", format="turtle")
```

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.oold.json` | Ready-to-edit example (start here) |
| `docs/expertise_workflow.ipynb` | Step-by-step notebook |
| `specs/schema.oold.yaml` | Full schema definition (expert reference) |

---

## For the curious: how this maps to the ontology

<details>
<summary>Show the RDF graph pattern</summary>

```text
foaf:Person
  schema:knowsAbout ──► <material URI>          [0..*]
  schema:knowsAbout ──► <simulation URI>         [0..*]
  schema:knowsAbout ──► <measurement_device URI> [0..*]
  schema:knowsAbout ──► <production_device URI>  [0..*]
  schema:knowsAbout ──► <application_field URI>  [0..*]
  schema:knowsAbout ──► <method URI>             [0..*]
```

All six expertise categories map to the same RDF property `schema:knowsAbout`.
The distinction between materials, methods, devices, etc. is carried by the
`rdf:type` of the referenced knowledge graph entity, not by separate property
IRIs.

> **Known limitation:** a SPARQL query on raw triples cannot distinguish
> "expertise in materials" from "expertise in methods" without joining on the
> `rdf:type` of the referenced entity.  Sub-properties of `schema:knowsAbout`
> are planned in a future version.

</details>

---

## Further reading

- [OO-LD primer](../../docs/oold-primer.md): how the schema format works
- [Schema format reference](../../docs/schema-format.md): for schema authors
