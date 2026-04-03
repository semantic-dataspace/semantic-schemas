# Chemical Composition — BWMD

Records the **chemical composition of a material** — which elements it
contains and in what proportions — following the
[BWMD Materials Data Science Ontology](https://www.iwm.fraunhofer.de/ontologies/bwmd-ontology#)
developed by Fraunhofer IWM.

Unlike the PMDCo variant, element fractions are expressed as **ranges**
(`min_value` / `max_value`), which suits nominal compositions and tolerance
bands.  All 118 IUPAC elements are supported.

---

## Quick start

**The fastest way in:** open the notebook.

```bash
pip install jupyterlab
jupyter lab docs/chemical_composition_workflow.ipynb
```

The notebook walks you through every step: fill in your data, convert to RDF,
and validate — with explanation between each step.

### Input fields

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "label": "316L Chemical Composition",
  "base_element": { "symbol": "Fe" },
  "fractions": [
    { "symbol": "Cr", "min_value": 16.0, "max_value": 18.0, "unit": "wt.%" },
    { "symbol": "Ni", "min_value": 10.0, "max_value": 14.0, "unit": "wt.%" },
    { "symbol": "Mo", "min_value":  2.0, "max_value":  3.0, "unit": "wt.%" }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `label` | yes | Human-readable name for this composition |
| `base_element.symbol` | yes | IUPAC symbol of the dominant element (e.g. `"Fe"`) |
| `fractions` | yes | List of alloying elements — one entry per element |
| `fractions[].symbol` | yes | IUPAC element symbol |
| `fractions[].min_value` | yes | Minimum fraction, 0–100 (for a point value, set equal to `max_value`) |
| `fractions[].max_value` | yes | Maximum fraction, 0–100 |
| `fractions[].unit` | yes | `"%"`, `"wt.%"`, or `"at.%"` — same for all fractions |

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

# Validate (no inference flag needed for this schema)
shapes = rdflib.Graph().parse("specs/shape.ttl")
conforms, _, _ = pyshacl.validate(g, shacl_graph=shapes)
print("Conforms:", conforms)
```

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example — start here |
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
| `%` | weight percentage (unqualified) |
| `wt.%` | weight percentage (explicit) |
| `at.%` | atomic percentage |

---

## For the curious — how this maps to the ontology

<details>
<summary>Show the RDF graph pattern</summary>

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

Key decisions:

- Both `base_element` and `fractions` serialise to `bwmd:hasPart` in RDF.
- Element identity is expressed as a plain IUPAC string literal
  (`bwmd:refersToElementSymbol`), not as an IRI — this is why all 118 elements
  are supported without an explicit mapping table.
- No `inference="rdfs"` flag is needed for SHACL validation — all shapes target
  classes directly.

</details>

---

## Further reading

- [Step-by-step guide](../../../docs/simplified-input-guide.md) — fill in data → convert → validate
- [OO-LD primer](../../../docs/oold-primer.md) — how the schema format works
- [Schema format reference](../../../docs/schema-format.md) — for schema authors
