# Contributing to the Semantic Schemas

> **Who is this for?** People who want to add a new schema or correct an
> existing one.  If you just want to record data, start with
> [README.md](README.md) instead.

Thank you for contributing! These schemas are community-maintained.
The goal is a diverse library where competing ontology patterns can coexist.

---

## Ground rules

- A schema must be grounded in a **publicly available ontology** with stable IRIs.
- A schema for a concept that already exists under a different ontology is **welcome**. Add it alongside the existing one instead of replacing it.
- Keep schemas **focused**: one domain concept per schema, one ontology per folder.
- Do not embed large static enumerations of ontology classes; link to the ontology instead.

---

## Workflow

### 1. Open an issue first

Use the **New Schema** issue template to describe:

- The concept you want to model
- The ontology you intend to use
- A short example instance (even in plain text)

This prevents duplicate work and gets early feedback on the pattern.

### 2. Write the schema

The fastest way to create all schema files is to work through the LLM session
described in **[docs/5_llm-schema-guide.md](docs/5_llm-schema-guide.md)**. It
provides the exact prompts and shows what to verify at each step.

If you prefer to write by hand, start from
[templates/schema.oold.yaml](templates/schema.oold.yaml) and read
[docs/3_schema-format.md](docs/3_schema-format.md) for a full field reference.

Place your schema at:

```text
schemas/<domain>/<ontology>/
```

Use lowercase kebab-case for domain names; preserve the ontology's official casing (e.g. `chemical-composition/PMDCo/`).

**When a second schema for the same ontology already exists**, both schemas must live in named variant sub-folders:

```text
schemas/<domain>/<ontology>/<variant>/
```

`<variant>` is a short kebab-case name describing the modelling pattern, not the author
(e.g. `fraction-spec`, `min-max`, `condensed`).  The contributor adding the second schema is
responsible for renaming the existing flat folder into its variant sub-folder as part of their PR.
Update `CATALOG.md` accordingly.

### 3. Run the tests

Every schema's workflow notebook is executed automatically on CI. To run the
same checks locally:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest --nbmake $(find schemas -name "*.ipynb" \
    ! -path "*/.ipynb_checkpoints/*")
```

All notebooks must pass before a PR can be merged.

### 3a. Refresh notebook outputs (for documentation)

The notebooks are committed with their output cells so that GitHub renders
them as readable documentation.  After changing a schema or its transform,
re-execute all notebooks in-place to update the stored outputs before
committing:

```bash
find schemas -name "*.ipynb" ! -path "*/.ipynb_checkpoints/*" \
  | xargs .venv/bin/jupyter nbconvert \
      --to notebook \
      --execute \
      --inplace \
      --ExecutePreprocessor.timeout=300
```

Run this from the repository root.  Commit the resulting `*.ipynb` changes
together with any schema changes so that the rendered output on GitHub stays
in sync.

> **Tip.** To refresh a single notebook only, pass its path directly:
>
> ```bash
> .venv/bin/jupyter nbconvert --to notebook --execute --inplace \
>     --ExecutePreprocessor.timeout=300 \
>     schemas/<domain>/<Ontology>/docs/<name>_workflow.ipynb
> ```

### 4. Validate locally

Ensure:

- The YAML is valid (use `yamllint` or a YAML linter).
- All IRIs in `@context` resolve to real ontology terms.
- The schema renders correctly in the webform-builder demo app (see [docs/webform-integration.md](docs/webform-integration.md)).

### 5. Update CATALOG.md

Add a row for your schema to [CATALOG.md](CATALOG.md).

### 6. Open a pull request

Use the PR template. Link the issue from step 1.

---

## Schema quality criteria

Reviewers will check:

| Criterion | What to look for |
|---|---|
| Ontological accuracy | IRIs resolve to the correct class/property |
| Completeness | Required fields cover the minimum viable instance |
| Usability | Labels and descriptions are clear for a non-expert |
| Simplicity | No unnecessary nesting; nested `type: object` degrades webform rendering |
| x-kitem types | `ktypeIds` match the ktype IDs used in the target deployment (DSMS-specific; omit if not applicable) |

---

## Updating an existing schema

- **Bug fixes** (wrong IRI, typo): open a PR directly with a brief description.
- **Breaking changes** (removing fields, changing structure): open an issue first.
- Do **not** edit another contributor's schema to change its ontological pattern. Create a new variant instead.

---

## Versioning

Every schema must declare two metadata fields in `schema.oold.yaml`:

```yaml
x-schema-version: '1.0.0'
x-schema-id: 'https://github.com/<org>/semantic-schemas/tree/main/schemas/<domain>/<Ontology>'
```

`x-schema-id` is the stable base IRI for the schema folder.  It does not change between versions.

Follow [Semantic Versioning](https://semver.org/): increment the **patch** for bug fixes (wrong IRI,
typo), the **minor** for additive changes (new optional field), and the **major** for breaking
changes (removed or renamed field, structural overhaul).

### Automatic provenance stamping

Every schema's `specs/transform.simplified.jsonata` must declare a `$schemaUri` constant formed by appending the version to `x-schema-id`:

```jsonata
$schemaUri := "<x-schema-id>#v<x-schema-version>";
```

The transform injects `"conforms_to": $schemaUri` into the root of the OO-LD output.  Because
`conforms_to` maps to `dcterms:conformsTo` in the `@context`, the versioned schema IRI is
automatically carried through to the generated RDF as:

```turtle
<instance> dcterms:conformsTo <schema-id/vX.Y.Z> .
```

Users do not need to provide any provenance information; it is stamped on every output by the
transform.  When bumping the schema version, update **both** `x-schema-version` in
`schema.oold.yaml` and `$schemaUri` in `transform.jsonata`.

### Change history

Each schema folder should contain a `CHANGELOG.md` that records what changed in each version.  A minimal entry looks like:

```markdown
## 1.1.0 — 2026-04-01
- Added optional `notes` field.

## 1.0.0 — 2026-01-15
- Initial release.
```

Users who need to retrieve the exact schema files for a past version can use `git log -- schemas/<domain>/<ontology>/` to find the corresponding commit.
