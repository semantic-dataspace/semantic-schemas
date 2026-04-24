# Tensile Test (TTO)

Records a **uniaxial tensile test** and its measured mechanical properties
following the
[Tensile Test Ontology (TTO)](https://w3id.org/pmd/tto/) built on the
[Platform MaterialDigital Core Ontology (PMDCo)](https://w3id.org/pmd/co/).

This schema is self-contained and follows the TTO reference data pattern
from the [tensile-test-ontology](https://github.com/materialdigital/tensile-test-ontology)
repository. Result properties are typed to TTO numeric class IRIs
(e.g. `tto:TTO_0000053` for tensile strength) rather than free-text labels.

---

## TTO vs PMDCo: which schema to choose

Both this schema and [`tensile-test/PMDCo/`](../PMDCo/README.md) use the
**same structural pattern** (PMDCo measurement pattern, OBI assay backbone).
The only difference is how individual result properties are identified:

| | PMDCo schema | TTO schema |
|---|---|---|
| Property identification | Free-text `rdfs:label` (`"Yield Strength"`) | Typed class IRI (`tto:TTO_0000053`) |
| Vocabulary | No constraint; any label is valid | Fixed TTO enum (see table below) |
| SPARQL query style | String-match on label | Class-based (`?x a tto:TTO_0000053`) |
| Cross-dataset queries | Fragile (label spelling may differ) | Reliable (shared class IRI) |
| New / non-standard properties | Supported | Must add to TTO first |

**Use PMDCo** when you need maximum flexibility: arbitrary property names, no
dependency on the TTO vocabulary, or integration with tools that consume
generic PMDCo graphs.

**Use TTO** when you want semantic interoperability: SPARQL queries like
"find all tensile strength measurements across all specimens in this knowledge
graph" work reliably because every result node carries a shared class IRI
(`tto:TTO_0000053`) rather than a free-text label that may vary.

### Why TTO is a `step/` schema, not a `process/` schema

TTO records the **measurement result** of a single test procedure. It answers
*"what values were obtained from this specimen."*

The [`characterization/process/PMDCo/`](../../../process/PMDCo/README.md) schema
serves a different role: it records **process provenance**, answering
*"who ran this test, on which machine, on which specimen, and which step results
it produced."* That schema links to a TTO (or PMDCo) step result via
`step_reference`.

TTO is one of those step results.  It belongs under `step/` because it is a
measurement step record, not a provenance record for the workflow that produced
it.

---

## Schema structure

This schema is self-contained (no `$ref` inheritance from a base schema).
The graph pattern follows the TTO reference data from
[materialdigital/tensile-test-ontology](https://github.com/materialdigital/tensile-test-ontology).

```text
characterization/step/tensile-test/TTO/   this schema
  type: pmdco:PMD_0000974
  realizes → TensileTestMethod (tto:TTO_0000054)
  has_specified_input → Specimen IRI
  has_process_attribute → condition quality nodes (strain rate, temperature)
  measured_properties → _smd nodes (condition + result datums)
    _smd → is_about → quality instance (tto:TTO_XXXXX)
    _smd → has_value_spec → _svs (value + unit)
```

---

## Quick start

**The fastest way in:** open the notebook.

```bash
pip install jupyterlab
jupyter lab docs/1_tensile_test_workflow.ipynb
```

### Input fields

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "test_name":    "Tensile test 316L bar 1",
  "specimen_iri": "https://example.org/specimens/316L-tensile-bar-1",
  "test_standard": "ISO 6892-1",
  "strain_rate": 0.00025,
  "temperature": 23,
  "results": [
    { "property": "YieldStrength",                     "value": 310, "unit": "MPa" },
    { "property": "TensileStrength",                   "value": 620, "unit": "MPa" },
    { "property": "PercentageElongationAfterFracture", "value": 40,  "unit": "%" }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `test_name` | yes | Name for this test |
| `specimen_iri` | yes | IRI of the specimen tested |
| `test_standard` | no | Standard applied (e.g. `"ISO 6892-1"`) |
| `strain_rate` | no | Strain or displacement rate (stored as dimensionless `xsd:float`; no unit IRI emitted in the RDF graph, per TTO reference data) |
| `strain_rate_unit` | no | Unit label for human-readable context only; not stored in the RDF graph |
| `temperature` | no | Test temperature in °C |
| `results` | no | List of measured properties (see below) |
| `test_id` | no | Custom IRI slug; auto-derived from `test_name` if omitted |

**Supported properties:**

| `property` value | Symbol | TTO class IRI | Unit |
|---|---|---|---|
| `YieldStrength` | Rₑ | `tto:TTO_0000009` | MPa or GPa |
| `UpperYieldStrength` | ReH | `tto:TTO_0000059` | MPa or GPa |
| `LowerYieldStrength` | ReL | `tto:TTO_0000022` | MPa or GPa |
| `TensileStrength` | Rm | `tto:TTO_0000053` | MPa or GPa |
| `ProofStrength` | Rp0.2 | `tto:TTO_0000047` | MPa or GPa |
| `PercentageElongationAfterFracture` | A | `tto:TTO_0000033` | % |
| `PercentagePermanentElongation` | Ag | `tto:TTO_0000035` | % |
| `PercentageReductionOfArea` | Z | `tto:TTO_0000038` | % |

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example (start here) |
| `docs/1_tensile_test_workflow.ipynb` | Step-by-step notebook |
| `specs/schema.simplified.json` | Input field reference |
| `specs/transform.simplified.jsonata` | Converts your input to the structured format |
| `specs/schema.oold.yaml` | Full schema definition |
| `specs/shape.ttl` | SHACL validation rules (tensile-test additions) |
| `CHANGELOG.md` | Version history for this schema |

SHACL validation uses `specs/shape.ttl` only. This schema is self-contained
and does not depend on a base shape file.

Each schema folder keeps a `CHANGELOG.md` at its root that records breaking
changes, backwards-compatible additions, and corrections, following
[Semantic Versioning](https://semver.org/). See
[docs/3_schema-format.md](../../../../docs/3_schema-format.md) for the
versioning convention.

---

## For the curious: how this maps to the ontology

<details>
<summary>Show the RDF graph pattern</summary>

```text
TensileTestingProcess  (pmdco:PMD_0000974)
  rdfs:label ──────────────────────────────────────────── test name
  rdfs:comment ────────────────────────────────────────── description  (optional)
  realizes  (BFO_0000055) ─────────────────────────────► TensileTestMethod (tto:TTO_0000054)
    rdfs:label ────────── test standard string  (optional)
  has_specified_input  (OBI_0000293) ─────────────────► Specimen IRI
  has_process_attribute (PMD_0000009) ─────────────────► Condition quality node  [× 0..N]
    a  tto:TTO_0000051 (strain rate) | pmdco:PMD_0000967 (temperature) | …
    is_quality_measured_as (IAO_0000417) ─────────────► _smd node
  has_specified_output (OBI_0000299) ──────────────────► _smd (IAO_0000109)  [× 0..N]
    is_about (IAO_0000136) ────────────────────────────► Quality node (TTO or PMDCo class instance)
    has_value_specification (OBI_0001938) ────────────► _svs (OBI_0001931)
      has_value (PMD_0000006) ──────────────────────── xsd:float
      has_unit  (IAO_0000039) ──────────────────────── QUDT unit IRI
      is_about (IAO_0000136) ──────────────────────────► Quality node
      specifies_value_of (OBI_0001927) ───────────────► Quality node
```

For result properties the quality node is embedded inside the `_smd`'s
`is_about` field and carries its `IAO_0000417` back-link to the datum.
For condition properties (strain rate, temperature) the quality node also
appears in `has_process_attribute` so it is directly reachable from the
process without traversing the datum chain.

</details>

---

## Further reading

- [TTO repository](https://github.com/materialdigital/tensile-test-ontology): reference data and ontology
- [PMDCo measurement pattern](https://github.com/materialdigital/core-ontology/tree/main/patterns/measurement)
- [Tensile Test (PMDCo)](../PMDCo/README.md): the label-based variant of this schema
- [OO-LD primer](../../../../docs/2_oold-primer.md): how the schema format works
- [Schema format reference](../../../../docs/3_schema-format.md): folder structure and naming conventions
