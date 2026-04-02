# Simplified Input Guide

Some schemas in this store ship with a `simplified/` subfolder that provides a
**user-friendly entry point** for people who are not familiar with JSON-LD or
ontology IRIs.  This guide explains the folder layout, how to fill in your data,
and how to convert it step by step to RDF.

---

## Folder layout

```text
schemas/<domain>/<ontology>/
├── README.md                 ← pattern description & quick-start for this schema
├── specs/
│   ├── schema.oold.yaml      ← full OO-LD schema (expert reference)
│   └── shape.ttl             ← SHACL validation shape
├── docs/
│   ├── example.oold.json     ← complete OO-LD example (filled-in, ready to convert)
│   ├── example.input.json    ← ready-to-edit simplified input  ← start here
│   └── *.ipynb               ← workflow notebook
└── simplified/
    ├── schema.simplified.json ← user-friendly JSON Schema
    └── transform.jsonata      ← JSONata transform: simplified JSON → OO-LD
```

The `simplified/` folder never replaces the OO-LD schema — it is a convenience
layer on top of it.

---

## Step 1 — Fill in your data

Copy `docs/example.input.json` from the relevant schema folder and edit it
with your own values.  Each schema's `README.md` describes the fields; the
`simplified/schema.simplified.json` file is itself the authoritative reference
(open it in any JSON-aware editor for inline documentation).

---

## Step 2 — Validate the simplified JSON

Before transforming, check that your file conforms to the simplified schema.

```bash
pip install jsonschema
```

```python
import json, jsonschema

schema = json.load(open("simplified/schema.simplified.json"))
data   = json.load(open("my_input.json"))
jsonschema.validate(data, schema)
print("Input is valid.")
```

Errors are reported with the field path and the violated constraint.

---

## Step 3 — Transform to OO-LD

Each schema ships a `simplified/transform.jsonata` expression file.
Use [jsonata-python](https://github.com/rayokota/jsonata-python) to run it —
no custom code required.

```bash
pip install jsonata-python
```

```python
import jsonata, json

expr   = open("simplified/transform.jsonata").read()
data   = json.load(open("my_input.json"))
result = jsonata.Jsonata(expr).evaluate(data)

with open("my_output.oold.json", "w") as f:
    json.dump(result, f, indent=2)
```

Or directly from the command line:

```bash
python -m jsonata -e simplified/transform.jsonata -i my_input.json -o my_output.oold.json
```

The optional `material_id` and `comp_id` fields in the input control the RDF node
identifiers (see `simplified/schema.simplified.json`).  If omitted, they default
to `mat_001` and `chem_comp_001`.

---

## Step 4 — Convert OO-LD JSON to RDF

The OO-LD JSON is a standard JSON-LD document.  The JSON-LD context is already
defined in `schema.oold.yaml` — no copy-paste needed.

### Python — rdflib

rdflib ≥ 7 ships a native JSON-LD 1.1 parser that handles the OO-LD context
(including `@prefix: true` entries and CURIE-form `@id` values) with no extra
preprocessing.

```bash
pip install rdflib pyyaml
```

```python
import json, yaml, rdflib

context = yaml.safe_load(open("schema.oold.yaml"))["@context"]
doc     = json.load(open("my_output.oold.json"))

g = rdflib.Dataset()
g.parse(data=json.dumps({"@context": context, **doc}), format="json-ld")
g.serialize(destination="my_output.ttl", format="turtle")
```

### Java — Apache Jena

```bash
# Using the Jena CLI (riot)
riot --syntax=JSON-LD --output=TURTLE my_output.oold.json > my_output.ttl
```

Or programmatically:

```java
import org.apache.jena.rdf.model.*;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.jena.riot.RDFFormat;
import java.io.*;

Model model = RDFDataMgr.loadModel("my_output.oold.json",
                                    org.apache.jena.riot.Lang.JSONLD);
try (OutputStream out = new FileOutputStream("my_output.ttl")) {
    RDFDataMgr.write(out, model, RDFFormat.TURTLE_PRETTY);
}
```

---

## Step 5 — Validate against the SHACL shape

```bash
pip install pyshacl
```

```python
import pyshacl, rdflib

data_graph   = rdflib.Graph().parse("my_output.ttl")
shapes_graph = rdflib.Graph().parse("shape.ttl")

conforms, _, report = pyshacl.validate(
    data_graph,
    shacl_graph=shapes_graph,
    inference="rdfs",   # required: some shapes rely on subclass reasoning
    serialize_report_graph=True,
)
print(report)
if conforms:
    print("Graph is valid.")
```

> The `inference="rdfs"` flag is required because some shapes (e.g. element
> subclasses, proportion subclasses) are defined on superclasses and depend on
> RDFS subclass reasoning to fire.

---

## See also

- [oold-primer.md](oold-primer.md) — what OO-LD is and how it works
- [schema-format.md](schema-format.md) — field-by-field reference for writing schemas
