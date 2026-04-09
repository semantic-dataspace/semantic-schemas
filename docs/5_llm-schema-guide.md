# Creating a schema with an LLM

An LLM (such as Claude) can draft all the files for a new schema in one
focused session. This guide walks through the exact prompts and shows what
to verify at each step.

The complete set of files produced is:

```text
schemas/<domain>/<Ontology>/
  specs/
    schema.oold.yaml           # context + JSON Schema (the core)
    shape.ttl                  # SHACL validation rules
  simplified/
    transform.jsonata          # converts simplified user input to OO-LD
    schema.simplified.json     # JSON Schema for the simplified input
  docs/
    example.input.json         # ready-to-edit example
    <name>_workflow.ipynb      # step-by-step notebook
  README.md
```

> **Time estimate.** A complete schema takes 3–5 focused prompts. Plan for a
> 30–60 minute session, most of which is your own review and correction.

---

## Before you start

Prepare the following — you will paste these into your LLM session:

1. **`templates/schema.oold.yaml`** — the blank template (this repo)
2. **`docs/3_schema-format.md`** — field reference (this repo)
3. **An existing schema as example** — pick the one most similar to what you
   are building. Good starting points:
   - Process step: `schemas/characterization/tensile-test/TTO/`
   - Data artefact: `schemas/material-card/mechanical/PMDCo/`
   - Descriptor: `schemas/chemical-composition/PMDCo/`
4. **The ontology you intend to use** — have its IRI browser open so you can
   verify class and property IRIs during the session.

---

## Prompt 1 — Load context and define the concept

Start a new conversation. Paste all four context items first, then add:

```text
I want to create a new OO-LD schema for [concept name] using [ontology name and base IRI].

Concept description:
[Two or three sentences explaining what this schema records and why.]

The schema should capture:
- [field 1]: [type, e.g. "string, required — human-readable name"]
- [field 2]: [type, e.g. "IRI, required — links to the specimen"]
- [field 3]: [type, e.g. "number, optional — test temperature in °C"]
- [field 4]: [type, e.g. "array of result objects, each with type, value, unit"]

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

## Prompt 2 — Write `specs/schema.oold.yaml`

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
- Every CURIE resolves (`pmdco:PMD_0000016` → `https://w3id.org/pmd/co/PMD_0000016`).
- `@base` is absent.
- `type` has `readOnly: true` and a `const`.
- Array fields have `"@container": "@set"` in the context entry.
- `required` lists only the fields that truly must be present.

---

## Prompt 3 — Write `simplified/transform.jsonata`

```text
Now write simplified/transform.jsonata.

The transform receives a "simplified" JSON object (user-friendly keys, human
unit strings like "MPa") and must produce the OO-LD document described by
the schema you just wrote.

Requirements:
- Declare $schemaUri := "[x-schema-id]#v[x-schema-version]" at the top.
- Derive a URL-safe slug from the name field using $replace/$lowercase/$trim.
- Use $lookup(map, key) for any enum → IRI mapping (not map[key] — that is
  a known jsonata-python bug that returns the whole map object).
- Use $exists() before accessing optional fields.
- Inject "conforms_to": $schemaUri into the root output object.

Show the simplified input JSON you assumed (I will use it as example.input.json).
```

**What to check.**

- All `$lookup(map, key)` calls, not `map[key]`.
- `$schemaUri` matches the `x-schema-id` and `x-schema-version` in the schema.
- Optional fields are wrapped in `$exists()`.
- The output keys exactly match the JSON Schema `properties` keys (not the context IRI names).

Test it:

```bash
.venv/bin/python -m jsonata \
  -e schemas/<domain>/<Ontology>/simplified/transform.jsonata \
  -i schemas/<domain>/<Ontology>/docs/example.input.json
```

---

## Prompt 4 — Write `specs/shape.ttl`

```text
Now write specs/shape.ttl — a SHACL shape that validates the RDF graph
produced by the schema.

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

---

## Prompt 5 — Write the workflow notebook

```text
Finally, write the workflow notebook docs/<name>_workflow.ipynb.

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
   .venv/bin/pytest --nbmake schemas/<domain>/<Ontology>/docs/<name>_workflow.ipynb
   ```

3. **Write `README.md`** — a short description of what the schema records,
   the ontology it uses, and a link to the notebook.
4. **Add a row** to [CATALOG.md](../CATALOG.md).
5. **Open a PR** following [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Worked example: Vickers Hardness Test (PMDCo)

Below is a concrete run-through of Prompt 1 to show what a filled-in version
looks like.

**Context attached:** `templates/schema.oold.yaml`, `docs/3_schema-format.md`,
`schemas/characterization/tensile-test/TTO/` (full folder).

**Prompt:**

```text
I want to create a new OO-LD schema for a Vickers Hardness Test using PMDCo
(https://w3id.org/pmd/co/) and OBI (http://purl.obolibrary.org/obo/).

Concept description:
A Vickers hardness test applies a diamond indenter to a material surface under
a defined load and measures the resulting indentation size. The result is a
Vickers Hardness (HV) value.

The schema should capture:
- test_name: string, required — human-readable name for this test
- specimen_iri: IRI, required — links to the specimen tested
- test_id: string, optional — custom slug; derived from test_name if omitted
- load: number, optional — indentation load in N
- dwell_time: number, optional — load application time in seconds
- results: array, optional — each item has:
    value: number — HV value
    unit: string — "HV" (unitless ratio; use QUDT dimensionless if available)

Do not write any files yet. Instead, list the ontology IRIs you would use
for the root class and for each field, with a brief justification for each
choice. Flag any IRI you are not confident about.
```

**Typical LLM response to verify:**

| Field | Proposed IRI | Notes |
|---|---|---|
| Root class | `obi:OBI_0000070` | Assay — correct for a characterisation test |
| `has_specified_input` (specimen) | `obi:OBI_0000293` | Correct |
| `has_process_condition` (load, dwell) | `pmdco:PMD_0000016` | Correct |
| result value | `obi:OBI_0001937` | has_specified_numeric_value — correct |
| result unit | `iao:IAO_0000039` | has_measurement_unit_label — correct |

At this point, verify each IRI in the ontology browser, then proceed to
Prompt 2 with the confirmed list.
