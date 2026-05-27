# Specimen (PMDCo)

Records a **physical specimen** (its name, mass, and the material it is made of)
following the [Platform MaterialDigital Core Ontology (PMDCo)](https://w3id.org/pmd/co/).

<table>
<tr><td><strong>Version</strong></td><td><code>0.2.0</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>
<a href="https://github.com/materialdigital/core-ontology/tree/main/patterns/duality%20object%20material">PMDCo duality object material</a>
</td></tr>
<tr><td><strong>Extends</strong></td><td>—</td></tr>
<tr><td><strong>Includes</strong></td><td>—</td></tr>
<tr><td><strong>Transformers</strong></td><td>—</td></tr>
</table>
The specimen links to an existing **Material** record in the knowledge graph
via `schema:material`. Chemical composition is a quality of the Material and
is recorded in the Material's own graph node, following the PMDCo duality pattern
strictly: Specimen → Material → ChemicalComposition.

---

## Quick start

**The fastest way in:** open the notebook.

```bash
pip install jupyterlab
jupyter lab docs/1_specimen_workflow.ipynb
```

The notebook walks through all steps: fill in your data, convert to RDF,
validate against two SHACL shapes, and inspect the result.

### Input fields

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "specimen_name": "316L Tensile Bar #1",
  "mass_value": 50.3,
  "mass_unit": "g",
  "material": "https://example.org/material-316l"
}
```

| Field | Required | Description |
|---|---|---|
| `specimen_name` | yes | Name or identifier for the specimen |
| `mass_value` | no | Mass of the specimen as a positive number |
| `mass_unit` | no | `"g"` (gram), `"kg"` (kilogram), or `"mg"` (milligram) |
| `material` | no | IRI of an existing material record in the knowledge graph |

### Convert to RDF (Python)

```bash
pip install jsonata-python rdflib pyyaml pyshacl
```

```python
import jsonata, json, yaml, rdflib, pyshacl, pathlib

SPECIMEN = pathlib.Path(".")

simplified = json.load(open("docs/example.input.json"))

# Step 1: run the transform
expr     = open("specs/transform.simplified.jsonata").read()
oold_doc = jsonata.Jsonata(expr).evaluate(simplified)

# Step 2: convert to RDF
context = yaml.safe_load(open("specs/schema.oold.yaml"))["@context"]
g = rdflib.Dataset()
g.parse(data=json.dumps({"@context": context, **oold_doc}), format="json-ld")
g.serialize(destination="output_specimen.ttl", format="turtle")

# Step 3: validate against the specimen SHACL shape
shapes = rdflib.Graph()
shapes.parse("specs/shape.ttl")
conforms, _, _ = pyshacl.validate(g, shacl_graph=shapes, inference="rdfs")
print("Conforms:", conforms)
```

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example (start here) |
| `docs/1_specimen_workflow.ipynb` | Step-by-step notebook |
| `specs/schema.simplified.json` | Input field reference |
| `specs/transform.simplified.jsonata` | Converts your input to the specimen envelope + mass |
| `specs/schema.oold.yaml` | Full schema definition (expert reference) |
| `specs/shape.ttl` | SHACL validation rules (specimen node + mass) |

SHACL validation loads two shape files: the specimen shape above plus
`chemical-composition/PMDCo/specs/shape.ttl`, mirroring the `$ref` composition
at the schema level.

---

## For the curious: how this maps to the ontology

<details>
<summary>Show the RDF graph pattern</summary>

PMDCo patterns used:

| Pattern | Role |
|---|---|
| [Duality Object / Material](https://github.com/materialdigital/core-ontology/tree/main/patterns/duality%20object%20material) | Specimen is a `bfo:Object` linked to a Material entity; composition is a quality of the Material |
| [Material Property (Quality)](https://github.com/materialdigital/core-ontology/tree/main/patterns/material%20property%20(quality)) | How the Mass quality is quantified: value + unit in a `ScalarValueSpecification` |

```text
Specimen  (bfo:BFO_0000030, Object)
  rdfs:label ──────────────────────────────── name string
  has_quality ──────────────────────────────► Mass (PMD_0020133)  [optional]
    quality_of ────────────────────────────► Specimen  ← back-ref
    specified_by_value ─────────────────────► ScalarValueSpecification (OBI_0001931)
      has_specified_numeric_value ──────────── xsd:double  (> 0)
      has_measurement_unit_label ───────────── unit IRI  (g · kg · mg)
  schema:material ──────────────────────────► Material IRI  [optional, kitem]
                                               (ChemicalComposition is a quality of Material)
```

</details>

---

## Further reading

- [Material (k-type)](../../../../knowledge-types/k-types/material/specs/k-type.spec.yaml): the k-type powering the material picker
- [Chemical Composition (PMDCo)](../../chemical-composition/PMDCo/README.md): standalone composition schema (record separately; link via the Material)
- [OO-LD primer](../../../docs/2_oold-primer.md): how the schema format works
- [Schema format reference](../../../docs/3_schema-format.md): for schema authors
