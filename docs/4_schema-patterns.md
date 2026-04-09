# Schema patterns: inheritance and composition

This document explains the two structural patterns used throughout this
repository for relating schemas to one another: **inheritance** (extending a
base schema) and **composition** (embedding or referencing sub-objects).
It covers what each pattern does, what its limitations are, and when to
choose one over the other.

---

## 1. Inheritance: extending a base schema

### How it works

Inheritance is expressed using JSON Schema's `$ref` + `allOf` mechanism.
The extending schema declares the base as a dependency and adds its own
properties on top:

```yaml
# schemas/characterization/tensile-test/TTO/specs/schema.oold.yaml

allOf:
  - $ref: "https://.../characterization/step/PMDCo/"   # base schema

properties:
  type:
    const: "tto:TensileTest"   # overrides the base class
  measured_properties:         # new field, not in the base
    ...
```

Think of it as subclassing: `tto:TensileTest` is-a `obi:Assay` (the base
class), so the tensile test schema inherits the assay's structure and refines it.

### What carries over automatically

When a consumer resolves the `$ref`, the following come from the base schema:

- All **JSON Schema validation rules**: `required` fields, `type` constraints,
  property definitions, `enum` values.

This means a validator that resolves the `$ref` will check both the base
constraints and the extending schema's constraints simultaneously.

### What does NOT carry over automatically

**`@context` is not merged.** JSON-LD context resolution happens at document
parse time, not at schema validation time. The `$ref` link is invisible to
the JSON-LD parser.

**Consequence:** every extending schema must re-declare all `@context` entries
it relies on from the base, in full. In this repository these are clearly
marked with a comment:

```yaml
# ── Base context (mirrored from characterization/step/PMDCo/specs/schema.oold.yaml) ──
# Keep in sync with that file.
obi:
  "@id": "http://purl.obolibrary.org/obo/OBI_"
  "@prefix": true
...
```

This is the main maintenance cost of inheritance: if the base schema's
`@context` changes, all extending schemas must be updated.

### What can be overridden

Any property from the base can be overridden in the extending schema:

| What | How | Example |
|---|---|---|
| Root class (`type`) | Redeclare `type` with a new `const` | `tto:TensileTest` overrides `obi:Assay` |
| Property title / description | Redeclare the property in `properties:` | Tensile test relabels `has_specified_input` as "Specimen" |
| Default value | Redeclare with a new `default:` | `id` default changed from `characterization-step` to `tensile-test` |
| Enum values | Redeclare with a refined `enum:` | `result_unit` restricted to MPa / GPa / % |

In JSON Schema `allOf`, conflicts between the base and the extension are
**intersected**: a field value must satisfy both constraints simultaneously.
This means you can **narrow** (restrict further) but not **widen** (relax)
a constraint from the base.

### SHACL implications

Each schema in the inheritance chain has its own SHACL shape file. The base
shape validates the inherited structure; the extending shape validates the
additions. **Both must be loaded together** when validating an extended
schema instance:

```python
shapes = rdflib.Graph()
shapes.parse("characterization/step/PMDCo/specs/shape.ttl")   # base
shapes.parse("characterization/tensile-test/TTO/specs/shape.ttl")  # extension
```

Set `inference="rdfs"` in pyshacl so that subclass relationships are
resolved correctly (e.g. `tto:TensileTest` is recognised as a subclass of
`obi:Assay` when the base shape targets `obi:Assay`).

### Repository examples

| Base schema | Extending schema | What was added |
|---|---|---|
| `characterization/step/PMDCo/` | `characterization/tensile-test/TTO/` | Typed result nodes (TTO classes), specimen required |
| `simulation/step/PMDCo/` | `simulation/model-calibration/PMDCo/` | `model_type` enum, embedded parameter nodes |

---

## 2. Composition: one schema relies on another

Sometimes a schema does not just *extend* another schema (inheritance) but
genuinely **depends** on another schema to describe one of its sub-graphs.
The clearest example in this repository is the **Specimen** schema:

```text
specimen/PMDCo/
  └─ relies on ─► chemical-composition/PMDCo/
```

A specimen record contains a chemical composition. The composition is complex
enough to have its own schema, its own transform, and its own SHACL shape.
The specimen schema does not duplicate this logic; instead it formally declares
the dependency and delegates the sub-graph construction.

### How the dependency is declared

In `specimen/PMDCo/specs/schema.oold.yaml`, the `has_composition` property
references the other schema's root URI:

```yaml
has_composition:
  $ref: "https://github.com/semantic-dataspace/semantic-schemas/tree/main/schemas/chemical-composition/PMDCo/"
```

This is different from inheritance. In inheritance the `$ref` appears **at
the top level** together with `allOf` and means "my document IS-A instance
of the base schema". Here the `$ref` appears **inside a property** and means
"the value of this property is described by that schema".

### How to use it in practice

Building a specimen record requires two transforms, one per schema:

```python
import jsonata, json, yaml, rdflib, pathlib

SPECIMEN  = pathlib.Path("specimen/PMDCo")
CHEM_COMP = pathlib.Path("chemical-composition/PMDCo")

simplified = json.load(open("example.input.json"))

# Step 1: specimen envelope (name, mass)
specimen_doc = jsonata.Jsonata(
    open(SPECIMEN / "simplified/transform.jsonata").read()
).evaluate(simplified)

# Step 2: delegate composition to the other schema's transform
comp_input = {
    "material_name": simplified["specimen_name"],
    "material_id":   specimen_doc["id"],
    "elements":      simplified["elements"],
}
comp_doc = jsonata.Jsonata(
    open(CHEM_COMP / "simplified/transform.jsonata").read()
).evaluate(comp_input)
comp_doc["quality_of"] = specimen_doc["id"]   # back-reference to parent

# Step 3: merge and parse to RDF
oold_doc = {**specimen_doc, "has_composition": comp_doc}
context  = yaml.safe_load(open(SPECIMEN / "specs/schema.oold.yaml"))["@context"]
g = rdflib.Dataset()
g.parse(data=json.dumps({"@context": context, **oold_doc}), format="json-ld")
```

### SHACL validation

Loading one shape file is not enough. Both shape files must be loaded together:

```python
shapes = rdflib.Graph()
shapes.parse(str(SPECIMEN  / "specs/shape.ttl"))
shapes.parse(str(CHEM_COMP / "specs/shape.ttl"))
conforms, _, _ = pyshacl.validate(g, shacl_graph=shapes)
```

This mirrors the `$ref` at the schema level: the specimen shape covers the
envelope (label, mass) and the composition shape covers the element fractions.

### What carries over and what does not

| What carries over | How |
|---|---|
| The composition's JSON Schema validation rules | The `$ref` is resolved by schema validators |
| The composition's SHACL constraints | Load both shape files (manual step) |

| What does NOT carry over | Reason |
|---|---|
| The composition's `@context` entries | JSON-LD does not follow `$ref` links |
| The composition's transform logic | Must be invoked explicitly in your code |

The specimen schema's `@context` block must re-declare every term from the
chemical-composition schema's context that the combined RDF graph needs.

### Contrast with inheritance

| | Inheritance (`$ref` + `allOf`) | Schema composition (`$ref` in a property) |
|---|---|---|
| Relationship | IS-A (specialisation) | HAS-A (delegation) |
| `$ref` location | Root level, inside `allOf` | Inside a property definition |
| New schema adds | Extra fields to the same class | A distinct sub-graph of a different class |
| Transform | One transform (may call base) | Two transforms, results merged |
| Example | tensile-test/TTO extends characterization/step/PMDCo | specimen/PMDCo includes chemical-composition/PMDCo |

### Repository examples

| Depending schema | Relied-upon schema | What it delegates |
|---|---|---|
| `specimen/PMDCo/` | `chemical-composition/PMDCo/` | Full element-fraction sub-graph |

### Embedded sub-objects vs. schema composition

Some schemas embed sub-nodes that are not described by a separate schema.
For example, the result nodes inside a tensile test or the parameter nodes
inside a model calibration. These are **simpler than schema composition**:
there is no separate transform to invoke; the parent schema's own transform
generates the sub-nodes directly. They are documented in the parent schema's
`specs/schema.oold.yaml` under the relevant property definition.

Use schema composition (a `$ref` pointing to another schema's folder) when
the sub-graph is complex enough to deserve its own schema, its own
validation shape, and potentially its own reuse by other schemas.

---

## 3. Connecting to independent nodes by IRI

A schema may record a **link** to another node in the knowledge graph without
knowing or caring about that node's internal structure:

```json
{
  "type":                "pmdco:PMD_0000029",
  "id":                  "process-sintering-batch-1",
  "has_specified_input": ["https://example.org/materials/green-compact-batch-1"],
  "has_specified_output":["https://example.org/materials/sintered-magnet-batch-1"]
}
```

The input and output materials are independent nodes described by their own
schemas. The process schema only records the connection; it does not embed
or compose their content.

### When to link by IRI

Link by IRI when:

- The referenced objects **exist independently** and have their own lifecycle
  (a specimen exists before and after the process that uses it).
- The referenced objects **may be shared** across multiple records
  (the same specimen is the input to both a tensile test and a hardness test).
- You want to keep schemas **decoupled**: the process schema does not need
  to know anything about the internal structure of the material.

This is weaker than schema composition. Composition declares a formal
dependency and loads the referenced schema's shapes; IRI linking only stores
a pointer.

### Limitations

- **Integrity is not guaranteed by the schema**: the schema cannot validate
  that the referenced IRI actually exists in the graph, or that the node
  at that IRI is of the expected type. Load the referenced node's own SHACL
  shape separately if you need that guarantee.
- **Requires coordination**: the referenced IRI must be agreed upon by both
  the producer (who registers the material node) and the consumer (who writes
  the process node). IRIs should follow a stable naming convention.

### Repository examples

| Schema | References (by IRI) |
|---|---|
| `manufacturing/step/PMDCo/` | Input materials, output materials, preceding steps |
| `characterization/step/PMDCo/` | Specimens or materials characterised |
| `workflow/PMDCo/` | Detailed step instances (`instance_iri`) |

---

## 4. Combining the patterns

The patterns are not mutually exclusive. A single schema can use all three:

```text
characterization/tensile-test/TTO/
  Inheritance       extends characterization/step/PMDCo/
  Reference by IRI  has_specified_input → Specimen IRI
  Embedding         measured_properties → result nodes (TTO classes)
```

The key question for each relationship is: does the related object **exist
independently** (reference by IRI), or is it **created and owned** by this
record (embedding)?

---

## 5. Decision guide

```text
Is my new schema a specialisation of an existing schema?
  YES, and it shares most of the base's structure
      → Inheritance ($ref + allOf)
         Remember: mirror the @context; add a second shape file
  NO, or it is structurally different
      → Independent schema

Does my schema contain sub-objects?
  YES
    Do the sub-objects exist independently in the knowledge graph?
      YES → Reference by IRI (non-composite)
      NO, they are created by this record
          → Embed (composite)
  NO → Flat schema with scalar fields only
```

---

## 6. Known limitations and open questions

| Topic | Status |
|---|---|
| `@context` merging via `$ref` | Not supported by the current toolchain. Manual mirroring required. Watch the [OO-LD spec](https://github.com/OO-LD/oold-python) for future support. |
| Widening constraints in inheritance | Not possible in `allOf` semantics. Extensions can only restrict, not relax, base constraints. |
| SHACL validation of referenced IRIs | Out of scope for the referencing schema. Load the target schema's shape file separately. |
| Multiple inheritance | Supported syntactically (`allOf` can list multiple `$ref`s) but not tested in this repository. Context mirroring becomes more complex. |
| Blank nodes in embedded sub-objects | Embedded nodes without an `id` field become blank nodes. They are valid RDF but cannot be referenced from outside the parent document. Always provide an `id` for embedded nodes that may need to be referenced. |

---

## Further reading

- [OO-LD primer](2_oold-primer.md): what OO-LD is and how the schema format works
- [Schema format reference](3_schema-format.md): folder structure, naming conventions, and the leaf-folder pattern
- [Tensile Test (TTO)](../schemas/characterization/tensile-test/TTO/README.md): worked example of inheritance
- [Constitutive Model Calibration (PMDCo)](../schemas/simulation/model-calibration/PMDCo/README.md): second inheritance example
- [Specimen (PMDCo)](../schemas/specimen/PMDCo/README.md): worked example of composition (chemical composition embedded)
- [Manufacturing Step (PMDCo)](../schemas/manufacturing/step/PMDCo/README.md): worked example of IRI referencing
