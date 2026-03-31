# Chemical Composition — PMDCo

Schema for describing the **chemical composition of a material** using the
[Platform MaterialDigital Core Ontology (PMDCo)](https://w3id.org/pmd/co/).

Original ontology pattern:
<https://github.com/materialdigital/core-ontology/tree/main/patterns/chemical%20composition>

---

## Graph pattern

The schema models the following RDF structure:

```text
ChemicalComposition (PMD_0000551)
  quality_of ──────────────────► Material  [rdfs:label = material name]
  is_subject_of ───────────────► ChemicalCompositionSpecification (PMD_0025002)
    has_member ──────────────────► FractionValueSpecification (PMD_0025997)  [× N]
      value                         xsd:double, range 0–100
      unit                          UO IRI  (mass% · vol% · mol%)
      element ─────────────────────► PortionOfChemicalElement (PMD_0020026 etc.)
        part_of ──────────────────► Material (same node as quality_of target)
        has_relational_quality ───► MassProportion (PMD_0020102)
          relational_quality_of ──► PortionOfChemicalElement  (back-ref)
          specified_by_value ─────► FractionValueSpecification (back-ref)
```

Key modelling decisions:

- One `ChemicalCompositionSpecification` groups all element fractions for a given
  composition measurement.
- Each fraction is a `FractionValueSpecification` that carries both the numeric
  value and the unit.
- The element identity is encoded in the `rdf:type` of the
  `PortionOfChemicalElement` node (e.g. `pmdco:PMD_0020026` for Iron).
- `MassProportion` (subclass of `Proportion`) links the element portion back to
  the fraction value specification via `specified_by_value`.
- The `element` key in the OO-LD schema is a JSON-LD nesting helper
  (`pmdco:PMD_hasFractionElement`, provisional) that groups the
  `PortionOfChemicalElement` under its fraction row for form rendering; it has no
  canonical counterpart in the ontology assertion.

---

## Supported units

| Simplified label | Unit Ontology IRI | Meaning |
|---|---|---|
| `mass%` | `uo:0000163` | mass percentage |
| `vol%`  | `uo:0000164` | volume percentage |
| `mol%`  | `uo:0000165` | molar percentage |

---

## Supported elements

All elements with a confirmed `PortionOfChemicalElement` subclass in PMDCo are
supported (72 elements).  The symbol-to-IRI mapping is in
[`simplified/transform.jsonata`](simplified/transform.jsonata) (`$elementMap`)
and the allowed symbol list is in the `enum` of
[`simplified/schema.simplified.json`](simplified/schema.simplified.json).

---

## Quick start (Python)

The `simplified/` folder provides a user-friendly JSON interface.
Full tooling instructions are in
[`docs/simplified-input-guide.md`](../../../docs/simplified-input-guide.md).

### 1. Describe your material

Create `my_input.json` (or copy [`simplified/example.input.json`](simplified/example.input.json)):

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

Rules: `value` must be between 0 and 100; use the same `unit` for all elements;
`symbol` must be a PMDCo-supported element symbol.

### 2. Transform to OO-LD and convert to RDF

```bash
pip install jsonata-python rdflib pyyaml
```

```python
import jsonata, json, yaml, rdflib

# Transform simplified JSON → OO-LD
expr = open("simplified/transform.jsonata").read()
data = json.load(open("my_input.json"))
oold = jsonata.Jsonata(expr).evaluate(data)

# Convert OO-LD → RDF (rdflib ≥ 7 handles JSON-LD 1.1 natively)
context = yaml.safe_load(open("schema.oold.yaml"))["@context"]
g = rdflib.Dataset()
g.parse(data=json.dumps({"@context": context, **oold}), format="json-ld")
g.serialize(destination="my_output.ttl", format="turtle")
```

A fully resolved OO-LD example is provided in [`example.oold.json`](example.oold.json).

### 3. Validate

```python
import pyshacl

data_graph   = rdflib.Graph().parse("my_output.ttl")
shapes_graph = rdflib.Graph().parse("shape.ttl")
conforms, _, report = pyshacl.validate(
    data_graph, shacl_graph=shapes_graph, inference="rdfs", serialize_report_graph=True
)
print(report)
```

---

## Files in this folder

| File | Purpose |
|---|---|
| `schema.oold.yaml` | Full OO-LD / JSON-LD schema |
| `shape.ttl` | SHACL validation shape |
| `example.oold.json` | Complete OO-LD example (316L stainless steel) |
| `simplified/schema.simplified.json` | User-friendly JSON Schema |
| `simplified/example.input.json` | Ready-to-edit simplified example |
| `simplified/transform.jsonata` | JSONata transform: simplified JSON → OO-LD |
| `notebooks/chemical_composition_workflow.ipynb` | End-to-end Jupyter notebook (transform → RDF → SHACL) |

---

## Further reading

- [Simplified input guide](../../../docs/simplified-input-guide.md) — step-by-step workflow (validate → transform → RDF → SHACL)
- [OO-LD primer](../../../docs/oold-primer.md) — what OO-LD is and how it works
- [Schema format reference](../../../docs/schema-format.md) — field-by-field reference
