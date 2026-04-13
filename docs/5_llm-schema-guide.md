# Creating a schema with an LLM

An LLM (such as Claude) can draft all the files for a new schema in one
focused session. This guide walks through the exact prompts and shows what
to verify at each step.

The complete set of files produced is:

```text
schemas/<domain>/<Ontology>/
  specs/
    schema.oold.yaml             # context + JSON Schema (the core)
    shape.ttl                    # SHACL validation rules
    schema.simplified.json       # JSON Schema for the simplified input
    transform.simplified.jsonata # converts simplified user input to OO-LD
  docs/
    example.input.json           # ready-to-edit example
    1_<name>_workflow.ipynb      # step-by-step notebook
  README.md
```

> **Time estimate.** A complete schema takes 5-7 focused prompts. Plan for a
> 45-90 minute session, most of which is your own review and correction.

---

## Before you start

Prepare the following; you will paste these into your LLM session:

1. **`templates/schema.oold.yaml`**: the blank template (this repo)
2. **`docs/3_schema-format.md`**: field reference (this repo)
3. **An existing schema as example**: pick the one most similar to what you
   are building. Good starting points:
   - Process step: `schemas/characterization/step/tensile-test/TTO/`
   - Data artefact: `schemas/material-card/mechanical/PMDCo/`
   - Descriptor: `schemas/chemical-composition/PMDCo/`
4. **The ontology you intend to use**: have its IRI browser open so you can
   verify class and property IRIs during the session.
   - For PMDCo, also check the [ontology patterns folder](https://github.com/materialdigital/core-ontology/tree/main/patterns)
     for ready-made modelling patterns (chemical composition, process chain, etc.).
     Each pattern comes with a SHACL shape that you can reuse in Prompt 4.

---

## Prompt 1: Load context and define the concept

Start a new conversation. Paste all four context items first, then add:

```text
I want to create a new OO-LD schema for [concept name] using [ontology name and base IRI].

Concept description:
[Two or three sentences explaining what this schema records and why.]

The schema should capture:
- [field 1]: [type, e.g. "string, required; human-readable name"]
- [field 2]: [type, e.g. "IRI, required; links to the specimen"]
- [field 3]: [type, e.g. "number, optional; test temperature in °C"]
- [field 4]: [type, e.g. "array of result objects, each with type, value, unit"]

Before proposing IRIs, check whether the ontology provides any modelling
patterns for this concept (e.g. https://github.com/materialdigital/core-ontology/tree/main/patterns
for PMDCo). If a matching pattern exists, follow it.

Do not write any files yet. Instead, list the ontology IRIs you would use
for the root class and for each field, with a brief justification for each
choice. Flag any IRI you are not confident about.
```

**What to check.** Verify every IRI the LLM proposes against the actual
ontology before continuing. For PMDCo use
[w3id.org/pmd/co/](https://w3id.org/pmd/co/); for OBI use the
[OBO Foundry browser](https://www.ebi.ac.uk/ols/ontologies/obi).
Correct any wrong IRIs in your next message before asking for code.

---

## Prompt 2: Write `specs/schema.oold.yaml`

After confirming the IRIs:

```text
Good. Use these confirmed IRIs:
[paste the corrected IRI list]

Now write specs/schema.oold.yaml following the template and the examples
I provided. Requirements:
- @context must map every field name to its ontology IRI.
- @base must NOT appear.
- type must be a readOnly const set to the root class CURIE.
- Use xsd:double for numeric measurement values.
- Use "@type": "@id" for any field that holds an IRI (not a literal).
- Set x-schema-id to:
  https://github.com/[org]/semantic-schemas/tree/main/schemas/[domain]/[Ontology]/
- Set x-schema-version to 1.0.0.
```

**What to check.**

- Every prefix in `@context` ends with `/` or `#`.
- Every CURIE resolves (`pmdco:PMD_0000016` -> `https://w3id.org/pmd/co/PMD_0000016`).
- `@base` is absent.
- `type` has `readOnly: true` and a `const`.
- Array fields have `"@container": "@set"` in the context entry.
- `required` lists only the fields that truly must be present.

---

## Prompt 3: Design the simplified input

Before writing code, decide what the user-facing input should look like.
The simplified schema is the contract between the user and the transform:
it maps human-friendly concepts (plain field names, human unit strings like
"MPa") to the more complex ontological structure defined in `schema.oold.yaml`.
Agreeing on this before writing the transform prevents rework.

```text
Now let's design the simplified input format before writing the transform.

The simplified schema (specs/schema.simplified.json) defines the user-facing
input: plain field names, human-readable units, no ontology knowledge required.
The transform will then map these simple fields to the richer OO-LD structure.

For the [concept name] schema, propose:
1. A minimal example.input.json (3-5 realistic field values).
2. A specs/schema.simplified.json that describes and validates this input
   (field names, types, required fields, brief descriptions).

Keep the simplified input as flat and minimal as possible. The transform's
job is to bridge the gap between this simple input and the ontological
structure; the user should not need to know about IRIs or graph patterns.
```

**What to check.**

- Field names are lowercase with underscores, not CURIEs.
- Required fields are genuinely the minimum viable input.
- The example looks like something a domain scientist would naturally fill in.

---

## Prompt 4: Write `specs/transform.simplified.jsonata`

```text
Good. Use this confirmed simplified input:
[paste the agreed example.input.json]

Now write specs/transform.simplified.jsonata.

The transform receives the simplified JSON object and must produce the OO-LD
document described by specs/schema.oold.yaml.

Requirements:
- Declare $schemaUri := "[x-schema-id]#v[x-schema-version]" at the top.
- Derive a URL-safe slug from the name field using $replace/$lowercase/$trim.
- Use $lookup(map, key) for any enum to IRI mapping (not map[key]; that is
  a known jsonata-python bug that returns the whole map object).
- Use $exists() before accessing optional fields.
- Inject "conforms_to": $schemaUri into the root output object.
```

**What to check.**

- All `$lookup(map, key)` calls, not `map[key]`.
- `$schemaUri` matches the `x-schema-id` and `x-schema-version` in the schema.
- Optional fields are wrapped in `$exists()`.
- The output keys exactly match the JSON Schema `properties` keys (not the context IRI names).

Test it:

```bash
.venv/bin/python -m jsonata \
  -e schemas/<domain>/<Ontology>/specs/transform.simplified.jsonata \
  -i schemas/<domain>/<Ontology>/docs/example.input.json
```

---

## Prompt 5: Write `specs/shape.ttl`

```text
Now write specs/shape.ttl, a SHACL shape that validates the RDF graph
produced by the schema.

If the ontology provides a ready-made SHACL shape for this concept or pattern
(e.g. https://github.com/materialdigital/core-ontology/blob/main/patterns/),
use it as the starting point and extend it rather than writing from scratch.
At minimum, extend it with a sh:property constraint that checks for the
presence of a dcterms:conformsTo triple (stamped by the transform).

Requirements:
- Target the root class ([root class IRI]).
- Validate all required scalar fields: each must have minCount 1, maxCount 1,
  and the correct xsd: datatype.
- Validate IRI fields with sh:nodeKind sh:IRI.
- Add descriptive sh:message strings so violations are readable.
- Use sh:closed false; sh:ignoredProperties (rdf:type) on the root node.
- If this schema extends a base schema, validate only the extension-specific
  fields here and note that the base shape must be loaded alongside.
```

**What to check.**

- All IRIs in `sh:path` entries match the `@context` mappings exactly.
- `sh:minCount` / `sh:maxCount` match the `required` list in the schema.
- No shape targets a class that does not appear in the graph.
- The `dcterms:conformsTo` constraint is present.

---

## Prompt 6: Write the workflow notebook

```text
Finally, write the workflow notebook docs/1_<name>_workflow.ipynb.

Base it on the example notebook I provided. Keep the same step structure:
1. Describe your [concept]
2. Convert to OO-LD (schema.transform())
3. Convert to RDF (schema.to_graph())
4. Validate (schema.validate())
5. Inspect the graph (SPARQL)

Requirements:
- Import Schema from semantic_schemas.
- Use Schema(SCHEMA).transform(), .to_graph(), and .validate().
- The SPARQL cell in Step 5 must query using the actual ontology IRIs from
  the @context (not field names).
- The summary table at the end must list all 5 steps.
- Every markdown cell should explain what is happening in plain language.
  Avoid jargon except when introducing an ontology term for the first time.
- Name the file 1_<name>_workflow.ipynb to be consistent with the naming
  convention used across all schemas in this repository.
```

**What to check.**

- The `SCHEMA` path variable points one level up from `docs/`.
- All `Schema(...)` calls match the API: `transform(data)`, `to_graph(data)`,
  `validate(flat)`, `validate(flat, also=[other_schema])`.
- The SPARQL query uses the correct predicate IRIs.
- Run all cells to confirm they execute without errors.

---

## After the session

1. **Save all files** to `schemas/<domain>/<Ontology>/` following the layout
   above.
2. **Run the tests** locally:

   ```bash
   .venv/bin/pytest tests/test_shacl.py -v
   .venv/bin/pytest --nbmake schemas/<domain>/<Ontology>/docs/1_<name>_workflow.ipynb
   ```

3. **Write `README.md`**: a short description of what the schema records,
   the ontology it uses, and a link to the notebook.
4. **Add a row** to [CATALOG.md](../CATALOG.md).
5. **Open a PR** following [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Worked example: Vickers Hardness Test (PMDCo)

Below is a concrete run-through of Prompt 1 to show what a filled-in version
looks like.

**Context attached:** `templates/schema.oold.yaml`, `docs/3_schema-format.md`,
`schemas/characterization/step/tensile-test/TTO/` (full folder).

**Prompt:**

```text
I want to create a new OO-LD schema for a Vickers Hardness Test using PMDCo
(https://w3id.org/pmd/co/) and OBI (http://purl.obolibrary.org/obo/).

Concept description:
A Vickers hardness test applies a diamond indenter to a material surface under
a defined load and measures the resulting indentation size. The result is a
Vickers Hardness (HV) value.

The schema should capture:
- test_name: string, required; human-readable name for this test
- specimen_iri: IRI, required; links to the specimen tested
- test_id: string, optional; custom slug; derived from test_name if omitted
- load: number, optional; indentation load in N
- dwell_time: number, optional; load application time in seconds
- results: array, optional; each item has:
    value: number; HV value
    unit: string; "HV" (unitless ratio; use QUDT dimensionless if available)

Before proposing IRIs, check whether PMDCo provides a modelling pattern for
hardness tests at https://github.com/materialdigital/core-ontology/tree/main/patterns.

Do not write any files yet. Instead, list the ontology IRIs you would use
for the root class and for each field, with a brief justification for each
choice. Flag any IRI you are not confident about.
```

**Typical LLM response to verify:**

| Field | Proposed IRI | Notes |
|---|---|---|
| Root class | `obi:OBI_0000070` | Assay; correct for a characterisation test |
| `has_specified_input` (specimen) | `obi:OBI_0000293` | Correct |
| `has_process_condition` (load, dwell) | `pmdco:PMD_0000016` | Correct |
| result value | `obi:OBI_0001937` | has_specified_numeric_value; correct |
| result unit | `iao:IAO_0000039` | has_measurement_unit_label; correct |

At this point, verify each IRI in the ontology browser, then proceed to
Prompt 2 with the confirmed list.
