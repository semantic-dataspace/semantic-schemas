# Schema Update Checklist

Use this file whenever you modify an existing schema, whether you are a human
contributor or an LLM agent. Work through the sections in order. Each section
states which files to touch, what to verify, and what the correct output looks
like.

Commands in this file assume your working directory is the **repository root**
and your virtual environment is active.

---

## 0. Classify the change

Determine the semantic-versioning impact before touching any file:

| Change type | Version bump | Examples |
|---|---|---|
| Typo, description fix, comment | **patch** (0.0.x) | Description reword, comment added |
| New optional field | **minor** (0.x.0) | Added optional `notes` field |
| Field renamed, removed, or graph structure changed | **major** (x.0.0) | `material_iri` → `material`, inline array replaced by kitem |

The bump determines the new version string used in all subsequent steps.

---

## 1. `specs/schema.oold.yaml`

- [ ] Bump `x-schema-version` to the new version string.
- [ ] Update `x-schema-uri`: replace the old per-schema git tag in the URL with the new one
  (e.g. `specimen-PMDCo-v0.1.0` → `specimen-PMDCo-v0.2.0`).
  The tag does not need to exist yet; it is created in step 14.
- [ ] Update `@context`: rename or add/remove key–IRI mappings for any changed field names.
  If a field is **renamed but the RDF predicate stays the same**, only the JSON key in
  `@context` changes; the predicate IRI is unchanged.
- [ ] Update `properties`: add, remove, or rename property definitions to match the new schema.
- [ ] Update `required` list to reflect mandatory fields.
- [ ] Add `x-kitem: { ktypeIds: ["<ktype-id>"] }` to any field that picks an entity from the
  knowledge graph.

**Verify:**

```bash
python -c "import yaml; yaml.safe_load(open('schemas/<path>/specs/schema.oold.yaml'))"
```

Must produce no output (no exception).

> **Pitfall: YAML colon in unquoted strings.** Any `description:` value that
> contains `:` (colon-space) will break YAML parsing unless the value is quoted:
>
> ```yaml
> # BAD  — YAML interprets "base pattern:" as a nested key
> description: A base pattern: used by all step schemas.
>
> # GOOD
> description: "A base pattern: used by all step schemas."
> ```
>
> After bulk text replacements, run the verify command above on every modified YAML file.

---

## 2. `specs/schema.simplified.json`

- [ ] Add, remove, or rename fields to match the new user-facing input.
- [ ] Update the `required` array.
- [ ] For kitem fields: add `"x-kitem": { "ktypeIds": ["<ktype-id>"] }` and set
  `"type": "string", "format": "uri"`.
- [ ] Remove technical internal fields (IRI slugs, back-references) that should not
  appear in a user-facing form.
- [ ] Update the `"examples"` array at the bottom to reflect the new input shape.

**Verify:**

```bash
python -c "import json; json.load(open('schemas/<path>/specs/schema.simplified.json'))"
```

---

## 3. `specs/transform.simplified.jsonata`

- [ ] Rename input field references to match new simplified field names.
- [ ] Update `$schemaUri` to the same URL set in `x-schema-uri` (step 1).
- [ ] Remove logic for deleted fields; add passthrough or mapping logic for new fields.

**Verify (transform produces valid output):**

```bash
python -c "
import jsonata, json
expr = open('schemas/<path>/specs/transform.simplified.jsonata').read()
data = json.load(open('schemas/<path>/docs/example.input.json'))
print(json.dumps(jsonata.Jsonata(expr).evaluate(data), indent=2))
"
```

Inspect the output: check that all new fields appear and removed fields are absent.

---

## 4. `specs/shape.ttl`

Assess before editing. The shape validates at the **RDF predicate level**, not the JSON key
level. Ask:

> *Did any changed field's `@context` mapping produce a different RDF predicate IRI?*

| Situation | Action |
|---|---|
| JSON key renamed, same predicate IRI in `@context` | **No change needed**: the shape still validates the same predicate |
| Predicate IRI changed or new predicate added that must be constrained | **Update the shape** |
| Field removed that was previously required by the shape | **Remove or relax the constraint** |

After any shape edit, re-run end-to-end validation (step 10).

---

## 5. `CHANGELOG.md`

- [ ] Add a new version section **above** the previous entry:

  ```markdown
  ## [x.y.z] - YYYY-MM-DD

  ### Changed
  - **Breaking:** description of what changed and why.

  ---

  ## [previous version] - ...
  ```

- [ ] Use today's date in `YYYY-MM-DD` format.
- [ ] Classify changes under `Added`, `Changed`, `Removed`, or `Fixed` as appropriate.

---

## 6. `README.md`

- [ ] Update the version in the `<table>` header block:

  ```html
  <tr><td><strong>Version</strong></td><td><code>x.y.z</code></td></tr>
  ```

- [ ] Update the `Includes` row if any `$ref` dependencies were added or removed.
- [ ] Update the **input fields table** (Quick start section) to list the new fields.
- [ ] Update the **graph pattern diagram** under "For the curious" if the RDF structure changed.
- [ ] Update or remove the **schema composition section** if `$ref` dependencies changed.
- [ ] Update code examples in the Quick start section to use the new field names.

> **Pitfall: markdown table empty-value markers.** The `—` character in a pipe-table
> cell (`| — |`) means "no value" and must not be changed to `|: |` or anything else.
> Only `—` inside `<td>—</td>` HTML cells and `| — |` Markdown cells are empty-value
> markers; all other prose em-dashes should be replaced with commas, semicolons, or
> colons as appropriate.

---

## 7. `docs/example.input.json`

- [ ] Update the example to match the new simplified schema exactly.
- [ ] Remove deleted fields; add new fields with realistic example values.
- [ ] The example is used by the transform verification command in step 3 and by the
  notebook (step 8); it must be valid input for the transform.

---

## 8. `docs/*.ipynb` (Jupyter notebooks)

Work cell by cell. Do **not** hand-edit output cells; use `--refresh` instead.

- [ ] **Markdown cells:** update any field-reference tables, prose descriptions, or
  graph-pattern ASCII diagrams that mention old field names.
- [ ] **Code cells:** update variable references and input dictionary keys to use new
  field names. Remove cells whose purpose has been eliminated (e.g. a composition
  merge step that no longer exists).
- [ ] **Setup cell:** remove imports and schema objects for schemas that are no longer
  needed as dependencies.
- [ ] **Inspect/SPARQL cells:** rewrite to query the new graph structure; remove queries
  for sub-graphs that were eliminated.
- [ ] **Summary markdown:** update the step-by-step summary table to reflect the new
  workflow.

Re-execute and save outputs:

```bash
./scripts/run_notebooks.sh --refresh schemas/<path>/docs/<name>.ipynb
```

Inspect the saved outputs:

- Every code cell must have output (no silent failures).
- No cell output should contain a Python traceback.
- The Turtle output in the RDF step should show the new predicates and not the old ones.
- SHACL step must show `Conforms: True`.

> **Note:** `--refresh` also regenerates `schemas/manifest.json` automatically.

---

## 9. Cross-schema impact check

Changes to one schema can silently break others. Run these searches from the
repository root:

```bash
# Find schemas that $ref this schema
grep -rn "\$ref.*<schema-slug>" schemas/ --include="*.yaml"

# Find schemas with mirrored @context blocks (comment pattern used in this repo)
grep -rn "mirrored from" schemas/ --include="*.yaml"

# Find schemas with x-kitem references to a k-type you renamed or removed
grep -rn 'ktypeIds.*"<ktype-id>"' schemas/ --include="*.yaml" --include="*.json"
```

For each hit:

- **`$ref` dependency:** if the referenced schema's `@context` changed, the depending
  schema contains a hand-copied mirror of that context (marked with a comment like
  `── <schema> context (mirrored) ──`). Update that mirror block to match.
- **`x-kitem` reference:** if a k-type ID changed, update the `ktypeIds` value in every
  schema that references it.

---

## 10. End-to-end verification

Run all four checks in sequence. Every command must exit cleanly.

```bash
# Navigate to the schema directory first
cd schemas/<path>

# 1. YAML and JSON syntax
python -c "import yaml; yaml.safe_load(open('specs/schema.oold.yaml'))"
python -c "import json; json.load(open('specs/schema.simplified.json'))"

# 2. Transform produces correct output
python -c "
import jsonata, json
expr = open('specs/transform.simplified.jsonata').read()
data = json.load(open('docs/example.input.json'))
print(json.dumps(jsonata.Jsonata(expr).evaluate(data), indent=2))
"

# 3. RDF conversion + SHACL validation
python -c "
import json, yaml, rdflib, pyshacl, jsonata
expr   = open('specs/transform.simplified.jsonata').read()
data   = json.load(open('docs/example.input.json'))
doc    = jsonata.Jsonata(expr).evaluate(data)
ctx    = yaml.safe_load(open('specs/schema.oold.yaml'))['@context']
g      = rdflib.Dataset()
g.parse(data=json.dumps({'@context': ctx, **doc}), format='json-ld')
shapes = rdflib.Graph()
shapes.parse('specs/shape.ttl')
ok, _, report = pyshacl.validate(g, shacl_graph=shapes, inference='rdfs')
print(f'Triples: {len(g)}  |  SHACL conforms: {ok}')
if not ok: print(report)
"

# 4. Notebook test (no output saved)
cd ../../../..    # back to repo root
./scripts/run_notebooks.sh schemas/<path>/docs/<name>.ipynb
```

Expected output for step 3: a line like `Triples: 11  |  SHACL conforms: True`.
A triple count of 0 indicates a JSON-LD parsing problem (wrong `@context` mapping).

---

## 11. `CATALOG.md`

- [ ] If the schema's description (`What it records` column) changed meaningfully, update the row.
- [ ] If the schema's folder path changed (e.g., restructured into a variant sub-folder), update the `Folder` link.
- [ ] No change is needed for pure version bumps that do not alter the description or path.

---

## 12. Update `schemas/manifest.json`

- [ ] Find the entry in `schemas/manifest.json` whose `"path"` matches this schema and
  set `"version"` to the new version string.

  The manifest is the source of truth used by the sibling
  [knowledge-types](https://github.com/semantic-dataspace/knowledge-types) test suite to
  verify that every k-type's `semantic_schemas` reference is consistent with the
  published schema version. Skipping this step will break those tests for any k-type that
  references this schema.

---

## 13. Commit

- [ ] Stage files **by name**; do not use `git add .` or `git add -A` (risks committing
  `.env`, binary artefacts, or unrelated changes):

  ```bash
  git add schemas/<path>/specs/schema.oold.yaml \
          schemas/<path>/specs/schema.simplified.json \
          schemas/<path>/specs/transform.simplified.jsonata \
          schemas/<path>/specs/shape.ttl \
          schemas/<path>/CHANGELOG.md \
          schemas/<path>/README.md \
          schemas/<path>/docs/example.input.json \
          schemas/<path>/docs/<name>.ipynb \
          schemas/manifest.json \
          CATALOG.md
  ```

- [ ] Write a commit message that names the schema and version:
  `schema(<schema-slug>): bump to vX.Y.Z: <one-line reason>`
- [ ] Do **not** add a `Co-Authored-By:` trailer unless explicitly requested.

---

## 14. Push and tag

> Do not stop after committing. All three sub-steps below are required.

- [ ] Push the branch to the remote:

  ```bash
  git push
  ```

- [ ] Create the per-schema tag on the schema commit (note the commit SHA
  so the tag lands on the right commit if you made a follow-up fix):

  ```bash
  git tag <schema-slug>-vX.Y.Z <commit-sha>
  ```

  The tag slug must exactly match the tag embedded in `x-schema-uri`.

- [ ] Push the tag:

  ```bash
  git push origin <schema-slug>-vX.Y.Z
  ```

- [ ] Verify the tag is visible on the remote:

  ```bash
  git ls-remote --tags origin | grep <schema-slug>
  ```

---

## Quick reference: which files change for common update types

| Update | oold.yaml | simplified.json | transform | shape.ttl | CHANGELOG | README | CATALOG.md | example.json | notebook |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Description / typo fix | patch | — | — | — | patch | maybe | — | — | maybe |
| Add optional field | minor | minor | minor | maybe | minor | yes | maybe | yes | yes |
| Rename field (same predicate) | minor | minor | minor | **no** | minor | yes | maybe | yes | yes |
| Rename field (new predicate) | minor | minor | minor | **yes** | minor | yes | maybe | yes | yes |
| Remove field | **major** | major | major | maybe | major | yes | maybe | yes | yes |
| Replace inline sub-schema with kitem | **major** | major | major | maybe | major | yes | maybe | yes | yes |
| Change graph pattern | **major** | major | major | **yes** | major | yes | maybe | yes | yes |

`—` = no change needed; `maybe` = check manually using the decision rules above.
