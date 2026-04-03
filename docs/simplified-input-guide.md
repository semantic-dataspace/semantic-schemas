# From data to RDF: a step-by-step guide

This guide shows you how to take a plain JSON file with your measurements or
material properties and convert it into a structured RDF graph that follows
a standard ontology.

You do not need to know anything about ontologies to follow this guide.
All you need is Python and the schema folder for the concept you want to record.

---

## The pipeline at a glance

```text
example.input.json          ← you edit this
  │
  ▼
Validate                    ← check for typos / out-of-range values
  │
  ▼
Convert to structured JSON  ← handled by the schema's transform file
  │
  ▼
Convert to RDF              ← rdflib reads the schema context automatically
  │
  ▼
Validate against SHACL      ← confirms the graph is structurally correct
```

---

## Folder layout

```text
schemas/<domain>/<ontology>/
├── README.md                 ← what this schema is for and how to use it
├── specs/
│   ├── schema.oold.yaml      ← full schema definition (expert reference)
│   └── shape.ttl             ← SHACL validation rules
├── docs/
│   ├── example.input.json    ← ready-to-edit example  ← start here
│   └── *.ipynb               ← step-by-step notebook
└── simplified/
    ├── schema.simplified.json ← field reference (what each input field means)
    └── transform.jsonata      ← converts your JSON to the structured format
```

The `simplified/` folder is the friendly entry point.  The `specs/` folder is
the full schema; you rarely need to look at it.

---

## Step 1: Fill in your data

Copy `docs/example.input.json` from the schema folder you want to use and
edit it with your values.  Each schema's `README.md` describes the fields.
You can also open `simplified/schema.simplified.json` in any text editor;
it contains inline descriptions for every field.

---

## Step 2: Validate your input

Check that your file matches the expected format before going further.

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

Errors show the field path and the rule that was violated.

---

## Step 3: Convert to the structured format

Each schema ships a `simplified/transform.jsonata` file that converts your
plain JSON into the structured format expected by the RDF converter.

```bash
pip install jsonata-python
```

```python
import jsonata, json

expr   = open("simplified/transform.jsonata").read()
data   = json.load(open("my_input.json"))
result = jsonata.Jsonata(expr).evaluate(data)

with open("my_output.json", "w") as f:
    json.dump(result, f, indent=2)
```

Or from the command line:

```bash
python -m jsonata -e simplified/transform.jsonata -i my_input.json -o my_output.json
```

---

## Step 4: Convert to RDF

The structured JSON from the previous step is a standard JSON-LD document.
The ontology mapping (which field means which property) is taken directly from
`specs/schema.oold.yaml`; no copy-paste needed.

```bash
pip install rdflib pyyaml
```

```python
import json, yaml, rdflib

context = yaml.safe_load(open("specs/schema.oold.yaml"))["@context"]
doc     = json.load(open("my_output.json"))

g = rdflib.Dataset()
g.parse(data=json.dumps({"@context": context, **doc}), format="json-ld")
g.serialize(destination="my_output.ttl", format="turtle")
```

The Turtle file (`my_output.ttl`) is the RDF result.

---

## Step 5: Validate against the SHACL shape

SHACL shapes are validation rules written in RDF.  They check things like
"every element fraction must be a number between 0 and 100."

```bash
pip install pyshacl
```

```python
import pyshacl, rdflib

data_graph   = rdflib.Graph().parse("my_output.ttl")
shapes_graph = rdflib.Graph().parse("specs/shape.ttl")

conforms, _, report = pyshacl.validate(
    data_graph,
    shacl_graph = shapes_graph,
    inference   = "rdfs",
)
print("Conforms:", conforms)
```

> The `inference="rdfs"` flag is required for schemas that use class
> hierarchies (e.g. element subclasses, proportion subclasses); it tells the
> validator to reason about subclasses when applying the rules.
> Check the schema's `README.md` or notebook to see whether it is needed.

---

## Using the notebook instead

Each schema folder has a Jupyter notebook in `docs/` that runs all of these
steps interactively.  If you are not sure where to start, open the notebook
first; it includes explanation between each step and shows you the output
as you go.

---

## See also

- [OO-LD primer](oold-primer.md): how the schema format works under the hood
- [Schema format reference](schema-format.md): for people writing new schemas
