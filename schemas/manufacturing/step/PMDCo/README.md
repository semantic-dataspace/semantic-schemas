# Manufacturing Process (PMDCo)

Records a **manufacturing process step** (its name, description, input and output
materials, position in a process chain, and quantitative conditions) following the
[Platform MaterialDigital Core Ontology (PMDCo)](https://w3id.org/pmd/co/).

## Quick start

**The fastest way in:** open the notebook.

```bash
pip install jupyterlab
jupyter lab docs/1_process_workflow.ipynb
```

The notebook walks through every step: fill in your data, convert to RDF,
validate, and inspect the result, with explanation between each step.

### Input fields

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "process_name": "Sintering and Annealing batch 1",
  "description":  "Green compacts are heated below the melting point …",
  "inputs":       ["https://example.org/materials/anisotropic-green-compacts-batch-1"],
  "outputs":      ["https://example.org/materials/sintered-magnet-batch-1"],
  "preceded_by":  ["https://example.org/processes/pressing-of-fine-powder-batch-1"],
  "conditions": [
    { "name": "Sintering Temperature", "value": 1080, "unit": "°C" },
    { "name": "Energy Consumption",    "value": 26,   "unit": "kWh" }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `process_name` | yes | Human-readable process name |
| `description` | no | Free-text description of what the process does |
| `inputs` | no | IRIs of input materials (existing knowledge-graph nodes) |
| `outputs` | no | IRIs of output materials (existing knowledge-graph nodes) |
| `preceded_by` | no | IRIs of immediately preceding process nodes |
| `conditions` | no | List of quantitative process parameters |
| `conditions[].name` | yes (per entry) | Parameter name (e.g. `"Sintering Temperature"`) |
| `conditions[].value` | no | Numeric value |
| `conditions[].unit` | no | Unit string (e.g. `"°C"`, `"kWh"`) |
| `process_id` | no | Custom IRI slug (auto-derived from `process_name` if omitted) |

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
conforms, _, _ = pyshacl.validate(g, shacl_graph=shapes)
print("Conforms:", conforms)
```

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example (start here) |
| `docs/1_process_workflow.ipynb` | Step-by-step notebook |
| `simplified/schema.simplified.json` | Input field reference |
| `simplified/transform.jsonata` | Converts your input to the structured format |
| `specs/schema.oold.yaml` | Full schema definition (expert reference) |
| `specs/shape.ttl` | SHACL validation rules |

## Design: non-composite

This schema is **non-composite**: input materials, output materials, and preceding
processes are referenced by IRI, not embedded. They are independent knowledge items
with their own schemas (e.g. `specimen/PMDCo`). The process schema only records
the connections between them and any quantitative conditions.

This mirrors the approach of `chemical-composition/PMDCo`: one schema describes one
concept fully; cross-concept links are IRIs pointing to separately managed nodes.

## For the curious: how this maps to the ontology

<details>
<summary>Show the RDF graph pattern</summary>

PMDCo pattern used: **Input and Output of Processes**
<https://github.com/materialdigital/core-ontology/tree/main/patterns/input%20and%20output%20of%20processes>

```text
ManufacturingProcess  (pmdco:PMD_0000029)
  rdfs:label ───────────────────────────── name string
  rdfs:comment ─────────────────────────── description string  (optional)
  has_specified_input  (OBI_0000293) ────► Material IRI  [× 0..N]
  has_specified_output (OBI_0000299) ────► Material IRI  [× 0..N]
  preceded_by          (BFO_0000062) ────► ManufacturingProcess IRI  [× 0..N]
  has_process_condition (PMD_0000016) ───► ProcessCondition (PMD_0000013)  [× 0..N]
    rdfs:label ──────── parameter name
    qudt:value ──────── xsd:double
    qudt:hasUnit ─────── unit string
```

Key decisions:

- `has_specified_input` / `has_specified_output` are OBI properties (`OBI_0000293` /
  `OBI_0000299`), as specified by the PMDCo "Input and Output of Processes" pattern.
  These replace the mixed `RO_0002233` / `RO_0002234` and EMMO properties seen in
  earlier data, providing a single canonical ontology reference.
- `preceded_by` (`BFO_0000062`) expresses ordering in the process chain without
  requiring a separate workflow wrapper node.
- `ProcessCondition` nodes (`PMD_0000013`) carry quantitative parameters via QUDT
  `value` / `hasUnit`, consistent with QUDT usage already present in PMDCo data.

</details>

## Further reading

- [OO-LD primer](../../../docs/2_oold-primer.md): how the schema format works
- [Schema format reference](../../../docs/3_schema-format.md): for schema authors
- [PMDCo Input and Output of Processes pattern](https://github.com/materialdigital/core-ontology/tree/main/patterns/input%20and%20output%20of%20processes)
- [PMDCo Process Chain pattern](https://github.com/materialdigital/core-ontology/tree/main/patterns/process%20chain): for modelling parallel and serial sub-processes
