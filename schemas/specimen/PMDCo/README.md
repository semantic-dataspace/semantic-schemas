# Specimen (PMDCo)

Records a **physical specimen** (its name, mass, and chemical composition)
following the [Platform MaterialDigital Core Ontology (PMDCo)](https://w3id.org/pmd/co/).

This schema builds on the [Chemical Composition (PMDCo)](../../chemical-composition/PMDCo/README.md)
schema: the composition sub-graph is produced by that schema's transform, which
remains the single source of truth for element IRIs and naming conventions.

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
  "elements": [
    { "symbol": "Fe", "value": 65.345, "unit": "mass%" },
    { "symbol": "Cr", "value": 17.0,   "unit": "mass%" }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `specimen_name` | yes | Name or identifier for the specimen |
| `elements` | yes | Chemical composition, same format as the chemical-composition schema |
| `mass_value` | no | Mass of the specimen as a positive number |
| `mass_unit` | no | `"g"` (gram), `"kg"` (kilogram), or `"mg"` (milligram) |
| `specimen_id` | no | Custom IRI slug (auto-derived from `specimen_name` if omitted) |
| `comp_id` | no | Custom IRI slug for the composition node (auto-derived if omitted) |

### Convert to RDF (Python)

```bash
pip install jsonata-python rdflib pyyaml pyshacl
```

```python
import jsonata, json, yaml, rdflib, pyshacl, pathlib

SPECIMEN  = pathlib.Path(".")
CHEM_COMP = SPECIMEN.parent.parent / "chemical-composition" / "PMDCo"

simplified = json.load(open("docs/example.input.json"))

# Step 1: specimen envelope (name + mass)
specimen_expr = open("specs/transform.simplified.jsonata").read()
specimen_doc  = jsonata.Jsonata(specimen_expr).evaluate(simplified)

# Step 2: composition (delegated to the composition schema's converter)
comp_input = {
    "material_name": simplified["specimen_name"],
    "material_id":   specimen_doc["id"],
    "elements":      simplified["elements"],
}
comp_expr = open(CHEM_COMP / "specs/transform.simplified.jsonata").read()
comp_doc  = jsonata.Jsonata(comp_expr).evaluate(comp_input)
comp_doc["quality_of"] = specimen_doc["id"]

# Step 3: merge and convert to RDF
oold_doc = {**specimen_doc, "has_composition": comp_doc}
context  = yaml.safe_load(open("specs/schema.oold.yaml"))["@context"]
g = rdflib.Dataset()
g.parse(data=json.dumps({"@context": context, **oold_doc}), format="json-ld")
g.serialize(destination="output_specimen.ttl", format="turtle")

# Step 4: validate against both shape files
shapes = rdflib.Graph()
shapes.parse("specs/shape.ttl")
shapes.parse(str(CHEM_COMP / "specs/shape.ttl"))
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

## Schema composition

Schema composition means this schema formally depends on another schema to
describe one of its sub-objects. The chemical composition of a specimen is
complex enough to deserve its own schema and validation rules; rather than
duplicating that logic here, this schema delegates to it.

This dependency is declared via JSON Schema `$ref`:

```yaml
has_composition:
  $ref: "https://github.com/semantic-dataspace/semantic-schemas/tree/main/schemas/chemical-composition/PMDCo/"
```

### Compatibility matrix

| This schema | chemical-composition/PMDCo |
|---|---|
| 1.0.0 | 1.0.0 |

When either schema releases a new version, verify compatibility and update
the `x-schema-dependencies` table in `specs/schema.oold.yaml` and this matrix.

---

## For the curious: how this maps to the ontology

<details>
<summary>Show the RDF graph pattern</summary>

PMDCo patterns used:

| Pattern | Role |
|---|---|
| [Duality Object / Material](https://github.com/materialdigital/core-ontology/tree/main/patterns/duality%20object%20material) | Specimen is a `bfo:Object` bearing qualities via `has_quality` |
| [Material Property (Quality)](https://github.com/materialdigital/core-ontology/tree/main/patterns/material%20property%20(quality)) | How the Mass quality is quantified: value + unit in a `ScalarValueSpecification` |
| [Chemical Composition](https://github.com/materialdigital/core-ontology/tree/main/patterns/chemical%20composition) | Full element-fraction sub-graph, referenced via JSON Schema `$ref` |

```text
Specimen  (bfo:BFO_0000030, Object)
  rdfs:label ──────────────────────────────── name string
  has_quality ──────────────────────────────► Mass (PMD_0020133)
    quality_of ────────────────────────────► Specimen  ← back-ref
    specified_by_value ─────────────────────► ScalarValueSpecification (OBI_0001931)
      has_specified_numeric_value ──────────── xsd:double  (> 0)
      has_measurement_unit_label ───────────── unit IRI  (g · kg · mg)
  has_quality ──────────────────────────────► ChemicalComposition (PMD_0000551)
    quality_of ────────────────────────────► Specimen  ← back-ref
    is_subject_of ─────────────────────────► ChemicalCompositionSpecification (PMD_0025002)
      has_member ──────────────────────────► FractionValueSpecification (PMD_0025997)  [× N]
        value                                xsd:double, range 0–100
        unit                                 UO IRI  (mass% · vol% · mol%)
        element ────────────────────────────► PortionOfChemicalElement
          part_of ───────────────────────────► Specimen  ← back-ref
          has_relational_quality ────────────► MassProportion (PMD_0020102)
```

Three back-references inside the sub-schemas must be set to the parent
specimen's `id`; the JSONata transform sets all of them automatically:

| Field path | Must equal |
|---|---|
| `mass.quality_of` | Specimen `id` |
| `has_composition.quality_of` | Specimen `id` |
| `has_composition.is_subject_of.has_member[*].element.part_of` | Specimen `id` |

</details>

---

## Further reading

- [Chemical Composition (PMDCo)](../../chemical-composition/PMDCo/README.md): the referenced sub-schema
- [OO-LD primer](../../../docs/2_oold-primer.md): how the schema format works
- [Schema format reference](../../../docs/3_schema-format.md): for schema authors
