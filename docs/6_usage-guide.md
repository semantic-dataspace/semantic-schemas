# Using a schema: from input to RDF

This guide shows how to go from a filled-in `example.input.json` to an RDF
graph and a SHACL validation result, for any schema in this repository.

The `semantic_schemas` package provides the `Schema` class used in the
notebooks. `Schema` is a thin convenience layer that handles the three
operations common to every schema workflow: applying the JSONata transform,
parsing the result into an RDF graph, and running SHACL validation. The
package is published on PyPI and can be installed normally:

```bash
pip install semantic-schemas
```

This also installs all required dependencies (`jsonata-python`, `rdflib`,
`pyyaml`, `pyshacl`).

## Getting the schema files

The schema files themselves (YAML definitions, SHACL shapes, example inputs)
are not bundled in the package: they live in this repository. You have two
options for obtaining them:

### Option A: Clone the repository (recommended for working with multiple schemas)

```bash
git clone https://github.com/semantic-dataspace/semantic-schemas
```

Then point `Schema` at the schema directory on disk:

```python
from semantic_schemas import Schema
from pathlib import Path

schema = Schema(Path("semantic-schemas/schemas/dataset/generic/DCAT"))
```

### Option B: Download individual schema files

If you only need one schema, download the specific files you need
(YAML definition, shape, example) from the repository's raw URLs.
The URL for each file is listed in its schema's `x-schema-uri` field and
follows the pattern:

```text
https://raw.githubusercontent.com/semantic-dataspace/semantic-schemas
  /<tag>/schemas/<path>/specs/schema.oold.yaml
```

With downloaded files, pass the local folder path to `Schema` as in Option A,
or use the raw library calls shown later in this guide and load the files
directly from disk.

> **Note for contributors:** if you are working from a local clone and want
> changes to `src/semantic_schemas/` to take effect without reinstalling,
> use an editable install instead: `pip install -e .` from the repository root.

The notebooks use the `semantic_schemas.Schema` class, which wraps the core
operations. The sections below show how to use that class for the two schema
path variants.

---

## Which path applies to your schema?

| Schema has | Path |
|---|---|
| `specs/transform.simplified.jsonata` | [Transform path](#transform-path-schemas-with-a-transform) |
| No transform file | [Direct OO-LD path](#direct-oo-ld-path-schemas-without-a-transform) |

Schemas with a transform accept a simplified, user-friendly input format.
Schemas without a transform expect `example.input.json` to already use the
OO-LD field names defined in `specs/schema.oold.yaml`.

---

## Transform path (schemas with a transform)

Used by schemas that have `specs/transform.simplified.jsonata` (e.g.
`characterization/`, `manufacturing/`, `simulation/`, `specimen/`).

```python
import json, pathlib
from semantic_schemas import Schema

schema = Schema(pathlib.Path("schemas/characterization/generic/PMDCo"))

data = json.load(open("docs/example.input.json"))
graph = schema.to_graph(data)                    # transform + parse → rdflib.Graph

print(graph.serialize(format="turtle"))

conforms, violations = schema.validate(graph)
print("Conforms:", conforms)
for v in violations:
    print(" -", v)
```

---

## Direct OO-LD path (schemas without a transform)

Used by schemas that do **not** have a transform (e.g. `dataset/`,
`data-analysis/`, `workflow/`). `example.input.json` already uses OO-LD
field names, so the transform step is skipped.

```python
import json, pathlib
from semantic_schemas import Schema

schema = Schema(pathlib.Path("schemas/dataset/generic/DCAT"))

oold = json.load(open("docs/example.input.json"))
graph = schema.parse(oold)                       # parse directly → rdflib.Graph

print(graph.serialize(format="turtle"))

conforms, violations = schema.validate(graph)
print("Conforms:", conforms)
for v in violations:
    print(" -", v)
```

---

## Querying the graph

Once you have an `rdflib.Graph`, you can inspect it with SPARQL or the
rdflib Python API. Both styles appear in the notebooks.

### SPARQL

Call `graph.query()` with a SPARQL string. Results are rows with named
attribute access:

```python
SPARQL = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?label ?format ?created WHERE {
  ?dataset a dcat:Dataset ;
           rdfs:label ?label .
  OPTIONAL { ?dataset dcterms:format  ?format  . }
  OPTIONAL { ?dataset dcterms:created ?created . }
}
"""

for row in graph.query(SPARQL):
    print(row.label, row.format, row.created)
```

For schemas that use OBI predicates, the type and property IRIs from the
`@context` (e.g. `OBI_0000293` for `has_specified_input`) are the ones to
query:

```python
SPARQL_IO = """
PREFIX obi: <http://purl.obolibrary.org/obo/OBI_>
PREFIX bfo: <http://purl.obolibrary.org/obo/BFO_>

SELECT ?role ?iri WHERE {
  { ?step a obi:0200000 ; obi:0000293 ?iri . BIND("input"  AS ?role) }
  UNION
  { ?step a obi:0200000 ; obi:0000299 ?iri . BIND("output" AS ?role) }
} ORDER BY ?role ?iri
"""

for row in graph.query(SPARQL_IO):
    print(row.role, row.iri)
```

### Python API

For targeted lookups without a full SPARQL query, use rdflib's graph
traversal methods directly:

```python
import rdflib

DCAT = rdflib.Namespace("http://www.w3.org/ns/dcat#")

# Find the dataset node
dataset_iri = next(graph.subjects(rdflib.RDF.type, DCAT.Dataset))

# Read a single value
label = graph.value(dataset_iri, rdflib.RDFS.label)

# Iterate over a multi-valued property
for keyword in graph.objects(dataset_iri, DCAT.keyword):
    print(keyword)
```

---

## Loading multiple SHACL shapes

Schemas that extend a base schema may have constraints split across two
shape files. Pass the base schema to `also=` so both shape graphs are
combined before validation runs:

```python
from semantic_schemas import Schema
from pathlib import Path

catalog = Schema(Path("schemas/dataset/catalog/DCAT"))
generic = Schema(Path("schemas/dataset/generic/DCAT"))

conforms, violations = catalog.validate(graph, also=[generic])
```

The shape file itself documents which base shape to load alongside it
(look for a `Load alongside` comment near the top).

---

## Further reading

- [OO-LD primer](2_oold-primer.md): how the schema format works
- [Schema format reference](3_schema-format.md): folder and naming conventions
- [Schema patterns](4_schema-patterns.md): inheritance and composition
