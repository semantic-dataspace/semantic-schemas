# Contributing to the Semantic Schema Store

Thank you for contributing! Schemas in this store are community-maintained. The goal is a diverse library where competing patterns can coexist and be rated by users.

---

## Ground rules

- A schema must be grounded in a **publicly available ontology** with stable IRIs.
- A schema for a concept that already exists under a different ontology is **welcome** — do not replace the existing one, add alongside it.
- Keep schemas **focused**: one domain concept per schema, one ontology per folder.
- Do not embed large static enumerations of ontology classes — link to the ontology instead.

---

## Workflow

### 1. Open an issue first

Use the **New Schema** issue template to describe:

- The concept you want to model
- The ontology you intend to use
- A short example instance (even in plain text)

This prevents duplicate work and gets early feedback on the pattern.

### 2. Write the schema

Start from [templates/schema.oold.yaml](templates/schema.oold.yaml). Read [docs/schema-format.md](docs/schema-format.md) for a full field reference.

Place your schema at:

```text
schemas/<domain>/<ontology>/schema.oold.yaml
```

Use lowercase kebab-case for directory names (e.g. `chemical-composition/PMDCo/`).

### 3. Validate locally

Ensure:

- The YAML is valid (use `yamllint` or a YAML linter).
- All IRIs in `@context` resolve to real ontology terms.
- The schema renders correctly in the webform-builder demo app (see [docs/webform-integration.md](docs/webform-integration.md)).

### 4. Update CATALOG.md

Add a row for your schema to [CATALOG.md](CATALOG.md).

### 5. Open a pull request

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
| x-kitem types | `ktypeIds` match the ktype IDs used in the target DSMS deployment |

---

## Updating an existing schema

- **Bug fixes** (wrong IRI, typo): open a PR directly with a brief description.
- **Breaking changes** (removing fields, changing structure): open an issue first.
- Do **not** edit another contributor's schema to change its ontological pattern — create a new variant instead.
