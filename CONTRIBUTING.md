# Contributing to the Semantic Schemas

> **Who is this for?** People who want to add a new schema or correct an
> existing one.  If you just want to record data, start with
> [README.md](README.md) instead.

Thank you for contributing! These schemas are community-maintained.
The goal is a diverse library where competing ontology patterns can coexist.

---

## Ground rules

- A schema must be grounded in a **publicly available ontology** with stable IRIs
  (Internationalized Resource Identifiers: persistent web addresses that uniquely identify concepts).
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
same checks locally, use the helper script:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
./scripts/run_notebooks.sh
```

The script collects all notebooks under `schemas/`, skips checkpoint folders,
and runs them with `pytest --nbmake`. All notebooks must pass before a PR can
be merged.

### 3a. Refresh notebook outputs (for documentation)

The notebooks are committed with their output cells so that GitHub renders
them as readable documentation. After changing a schema or its transform,
re-execute all notebooks in-place to update the stored outputs before
committing:

```bash
source .venv/bin/activate
./scripts/run_notebooks.sh --refresh
```

Commit the resulting `*.ipynb` changes together with any schema changes so
that the rendered output on GitHub stays in sync.

> **Tip.** To test or refresh a single notebook, pass its path directly:
>
> ```bash
> # Test only (no output saved):
> ./scripts/run_notebooks.sh schemas/<domain>/<Ontology>/docs/<name>.ipynb
>
> # Execute and save outputs in-place:
> ./scripts/run_notebooks.sh --refresh schemas/<domain>/<Ontology>/docs/<name>.ipynb
> ```

### 3b. Regenerate manifest.json

`schemas/manifest.json` is a **generated index** derived from the schema YAML files.
It must be kept in sync with the filesystem — CI will fail if it is stale.

After adding, removing, or changing `x-maturity` in any schema, regenerate it:

```bash
source .venv/bin/activate
python scripts/generate_manifest.py
```

The `--refresh` mode of `run_notebooks.sh` does this automatically.

**What the manifest contains:**

- One entry per `schema.oold.yaml` (with its `maturity` field mirrored from `x-maturity`)
- One entry per sibling `shape.ttl` (path only)
- Schemas that set `x-hidden: true` are excluded (they are `$ref` composition targets, not directly usable)

Do not edit `manifest.json` by hand — any manual change will be overwritten by the generator.

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

Every schema must declare three metadata fields in `schema.oold.yaml`:

```yaml
x-schema-version: '1.0.0'
x-schema-id:      'https://github.com/semantic-dataspace/semantic-schemas/tree/main/schemas/<domain>/<Ontology>'
x-maturity:       'draft'
```

`x-maturity` must be one of `draft`, `stable`, or `deprecated`. New schemas start as `draft`.
After changing it, run `python scripts/generate_manifest.py` to keep the manifest in sync.

### Schema versions vs. repository releases

Schemas are versioned independently from the repository. A schema version bump does **not**
trigger a global repository release. The global version (`pyproject.toml`, repo tag) covers
collection-level changes only: manifest format, tooling, Python package.

See [docs/3_schema-format.md](docs/3_schema-format.md) for the full versioning convention
including per-schema git tags, `dcterms:conformsTo` stamping, and SPARQL usage.

### Releasing a schema version

1. Update `x-schema-version` in `specs/schema.oold.yaml`.
2. Update `$schemaUri` in `specs/transform.simplified.jsonata` to the new per-schema tag URL.
3. Update `version` in `schemas/manifest.json` for this entry.
4. Add an entry to the schema's `CHANGELOG.md`.
5. Commit and push.
6. Create and push the per-schema git tag, e.g. `git tag tensile-test-PMDCo-v0.2.0 && git push origin tensile-test-PMDCo-v0.2.0`.
