# Chemical Composition (PMDCo)

Records the **chemical composition of a material** (which elements it
contains and in what proportions) following the
[Platform MaterialDigital Core Ontology (PMDCo)](https://w3id.org/pmd/co/).

---

## Quick start

**The fastest way in:** open the notebook.

```bash
pip install jupyterlab
jupyter lab docs/chemical_composition_workflow.ipynb
```

The notebook walks you through every step: fill in your data, convert to RDF,
and validate, with explanation between each step.

### Input fields

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "material_name": "316L Stainless Steel",
  "elements": [
    { "symbol": "Fe", "value": 65.345, "unit": "mass%" },
    { "symbol": "Cr", "value": 17.0,   "unit": "mass%" },
    { "symbol": "Ni", "value": 12.0,   "unit": "mass%" },
    { "symbol": "Mo", "value": 2.5,    "unit": "mass%" }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `material_name` | yes | Name or identifier for the material |
| `elements` | yes | List of element fractions, one entry per element |
| `elements[].symbol` | yes | IUPAC element symbol (e.g. `"Fe"`, `"Cr"`) |
| `elements[].value` | yes | Fraction value, 0–100 |
| `elements[].unit` | yes | `"mass%"`, `"vol%"`, or `"mol%"` (same for all elements) |
| `material_id` | no | Custom ID for the material node (auto-derived from `material_name` if omitted) |
| `comp_id` | no | Custom ID for the composition node (auto-derived if omitted) |

72 PMDCo-mapped elements are supported.
See [`simplified/schema.simplified.json`](simplified/schema.simplified.json) for the full list.

### Convert to RDF (Python)

```bash
pip install jsonata-python rdflib pyyaml pyshacl
```

```python
import jsonata, json, yaml, rdflib, pyshacl

# Transform your input → structured JSON
expr = open("simplified/transform.jsonata").read()
data = json.load(open("docs/example.input.json"))
oold = jsonata.Jsonata(expr).evaluate(data)

# Convert to RDF
context = yaml.safe_load(open("specs/schema.oold.yaml"))["@context"]
g = rdflib.Dataset()
g.parse(data=json.dumps({"@context": context, **oold}), format="json-ld")
g.serialize(destination="output.ttl", format="turtle")

# Validate
shapes = rdflib.Graph().parse("specs/shape.ttl")
conforms, _, _ = pyshacl.validate(g, shacl_graph=shapes, inference="rdfs")
print("Conforms:", conforms)
```

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example (start here) |
| `docs/chemical_composition_workflow.ipynb` | Step-by-step notebook |
| `docs/example.oold.json` | Fully converted OO-LD example (reference) |
| `simplified/schema.simplified.json` | Input field reference |
| `simplified/transform.jsonata` | Converts your input to the structured format |
| `specs/schema.oold.yaml` | Full schema definition (expert reference) |
| `specs/shape.ttl` | SHACL validation rules |

---

## Supported units

| Input label | Meaning |
|---|---|
| `mass%` | mass percentage |
| `vol%` | volume percentage |
| `mol%` | molar percentage |

---

## For the curious: how this maps to the ontology

<details>
<summary>Show the RDF graph pattern</summary>

Original PMDCo pattern:
<https://github.com/materialdigital/core-ontology/tree/main/patterns/chemical%20composition>

```text
ChemicalComposition (PMD_0000551)
  quality_of ──────────────────► Material  [rdfs:label = material name]
  is_subject_of ───────────────► ChemicalCompositionSpecification (PMD_0025002)
    has_member ──────────────────► FractionValueSpecification (PMD_0025997)  [× N]
      value                         xsd:double, range 0–100
      unit                          UO IRI  (mass% · vol% · mol%)
      element ─────────────────────► PortionOfChemicalElement
        part_of ──────────────────► Material
        has_relational_quality ───► MassProportion (PMD_0020102)
          relational_quality_of ──► PortionOfChemicalElement
          specified_by_value ─────► FractionValueSpecification (back-ref)
```

Key decisions:

- Element identity is encoded in the `rdf:type` of the `PortionOfChemicalElement`
  node (e.g. `pmdco:PMD_0020026` for Iron), not as a string literal.
- `MassProportion` links each element portion back to its fraction value via
  `specified_by_value`.
- SHACL validation requires `inference="rdfs"` because some shapes target
  superclasses (`Proportion`, `PortionOfSingleChemicalElement`) and rely on
  subclass reasoning to match the specific subtypes used in the data.

</details>

---

## Further reading

- [Step-by-step guide](../../../docs/simplified-input-guide.md): fill in data → convert → validate
- [OO-LD primer](../../../docs/oold-primer.md): how the schema format works
- [Schema format reference](../../../docs/schema-format.md): for schema authors
