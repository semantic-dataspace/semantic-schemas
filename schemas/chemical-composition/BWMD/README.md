# Chemical Composition — BWMD

Schema for describing the **chemical composition of a material** using the
[BWMD Materials Data Science Ontology](https://www.iwm.fraunhofer.de/ontologies/bwmd-ontology#)
developed by Fraunhofer IWM.

---

## Graph pattern

```text
bwmd:ChemicalComposition
  rdfs:label                ── human-readable composition name
  bwmd:hasPart ────────────► bwmd:BaseElementOfComposition
                               bwmd:refersToElementSymbol   (IUPAC symbol, e.g. "Fe")
  bwmd:hasPart ────────────► bwmd:WeightFraction  [× N]
                               bwmd:refersToElementSymbol   (IUPAC symbol)
                               bwmd:hasDoubleLiteralMinValue (xsd:double, 0–100)
                               bwmd:hasDoubleLiteralMaxValue (xsd:double, 0–100)
                               bwmd:hasUnitSymbol            ("%" | "wt.%" | "at.%")
```

Key modelling decisions:

- Both `base_element` and `fractions` serialise to `bwmd:hasPart` in RDF.
- Element identity is expressed as a plain IUPAC string literal
  (`bwmd:refersToElementSymbol`), not as an IRI — all 118 IUPAC elements are
  supported.
- Weight fractions are specified as ranges (`min_value` / `max_value`); for a
  point value, set both to the same number.

---

## Supported units

| Simplified label | Stored string | Meaning |
|---|---|---|
| `%`    | `%`    | weight percentage (unqualified) |
| `wt.%` | `wt.%` | weight percentage (explicit) |
| `at.%` | `at.%` | atomic percentage |

---

## Supported elements

All 118 IUPAC elements (IUPAC Red Book, 2005) are supported. The full list is
in the `enum` of
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
  "label": "316L Chemical Composition",
  "base_element": { "symbol": "Fe" },
  "fractions": [
    { "symbol": "Cr", "min_value": 16.0, "max_value": 18.0, "unit": "wt.%" },
    { "symbol": "Ni", "min_value": 10.0, "max_value": 14.0, "unit": "wt.%" },
    { "symbol": "Mo", "min_value": 2.0,  "max_value": 3.0,  "unit": "wt.%" }
  ]
}
```

Rules: `min_value` ≤ `max_value`; both in [0, 100]; use the same `unit` for all
fractions; `symbol` must be a valid IUPAC element symbol.

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
context = yaml.safe_load(open("specs/schema.oold.yaml"))["@context"]
g = rdflib.Dataset()
g.parse(data=json.dumps({"@context": context, **oold}), format="json-ld")
g.serialize(destination="my_output.ttl", format="turtle")
```

### 3. Validate

```python
import pyshacl

data_graph   = rdflib.Graph().parse("my_output.ttl")
shapes_graph = rdflib.Graph().parse("specs/shape.ttl")
conforms, _, report = pyshacl.validate(
    data_graph, shacl_graph=shapes_graph, serialize_report_graph=True
)
print(report)
```

> No `inference="rdfs"` flag is required for this schema — all SHACL shapes
> target classes directly.

---

## Files in this folder

| File | Purpose |
|---|---|
| `specs/schema.oold.yaml` | Full OO-LD / JSON-LD schema |
| `specs/shape.ttl` | SHACL validation shape |
| `docs/example.oold.json` | Complete OO-LD example (316L stainless steel) |
| `docs/chemical_composition_workflow.ipynb` | End-to-end Jupyter notebook (transform → RDF → SHACL) |
| `simplified/schema.simplified.json` | User-friendly JSON Schema |
| `simplified/example.input.json` | Ready-to-edit simplified example |
| `simplified/transform.jsonata` | JSONata transform: simplified JSON → OO-LD |

---

## Further reading

- [Simplified input guide](../../../docs/simplified-input-guide.md) — step-by-step workflow (validate → transform → RDF → SHACL)
- [OO-LD primer](../../../docs/oold-primer.md) — what OO-LD is and how it works
- [Schema format reference](../../../docs/schema-format.md) — field-by-field reference
