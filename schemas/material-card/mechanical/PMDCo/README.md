# Mechanical Material Card (PMDCo)

Records a **mechanical material card**: a structured dataset that collects
elastic constants, discrete mechanical property values, and a fitted constitutive
model into a single RDF-native object ready for use in FEM simulations.

Unlike the process schemas in this repository, this schema describes a **data
artefact** (an `iao:DataSet`) rather than a process.

---

## Quick start

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "card_name":    "316L stainless steel — Hockett-Sherby v1",
  "material_iri": "https://example.org/materials/316L-batch-1",
  "density":          { "value": 7.93,  "unit": "g/cm³" },
  "youngs_modulus":   { "value": 193.0, "unit": "GPa" },
  "poissons_ratio":   { "value": 0.29 },
  "mechanical_properties": [
    { "type": "YieldStrength",   "value": 285.0, "unit": "MPa" },
    { "type": "TensileStrength", "value": 620.0, "unit": "MPa" }
  ],
  "constitutive_model": {
    "model_type": "Hockett-Sherby",
    "calibration_iri": "https://example.org/simulations/calibration-316L-batch-1",
    "parameters": [
      { "name": "sigma_sat", "value": 780.0, "unit": "MPa" },
      { "name": "sigma_0",   "value": 220.0, "unit": "MPa" },
      { "name": "c",         "value": 12.5 },
      { "name": "n",         "value": 0.68 }
    ]
  }
}
```

| Field | Required | Description |
|---|---|---|
| `card_name` | yes | Human-readable card name |
| `material_iri` | yes | IRI of the material described by this card |
| `description` | no | Free-text description |
| `density` | no | Mass density (value + unit) |
| `youngs_modulus` | no | Elastic modulus (value + unit) |
| `poissons_ratio` | no | Poisson's ratio (value + optional unit) |
| `mechanical_properties` | no | List of TTO property values (type, value, unit) |
| `constitutive_model` | no | Fitted flow curve (model_type, calibration_iri, parameters) |
| `card_id` | no | Custom IRI slug; auto-derived from `card_name` if omitted |

### Supported property types

`YieldStrength`, `UpperYieldStrength`, `LowerYieldStrength`, `TensileStrength`,
`ProofStrength`, `PercentageElongationAfterFracture`, `PercentagePermanentElongation`,
`PercentageReductionOfArea`

Units: `MPa`, `GPa`, `%`

### Supported constitutive models

`Hockett-Sherby`, `Swift`, `Voce`, `Hollomon`, `Johnson-Cook`

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example (316L with Hockett-Sherby) |
| `simplified/schema.simplified.json` | Input field reference |
| `simplified/transform.jsonata` | Converts your input to the structured format |
| `specs/schema.oold.yaml` | Full schema definition |
| `specs/shape.ttl` | SHACL validation rules |

---

## For the curious: how this maps to the ontology

```text
DataSet  (iao:IAO_0000100)
  rdfs:label ─────────────────────────── card name
  dcterms:references ─────────────────► Material IRI
  pmdco:PMD_0000025  (Density) ───────► ScalarNode
    qudt:value   xsd:double
    qudt:hasUnit unit string
  pmdco:PMD_0000039  (YoungModulus) ──► ScalarNode  (same pattern)
  pmdco:PMD_0000040  (PoissonRatio) ──► ScalarNode  (same pattern)
  obi:OBI_0000299 (has_specified_output)
    ► MechanicalProperty  [× 0..N]  (TTO class)
        obi:OBI_0001937  result value (xsd:double)
        iao:IAO_0000039  result unit  (QUDT IRI)
    ► ConstitutiveModel node
        dcterms:type   model family string
        dcterms:source calibration IRI  (provenance)
        obi:OBI_0000299
          ► ModelParameter  [× 0..N]
              rdfs:label  parameter name
              qudt:value  xsd:double
              qudt:hasUnit unit string
```

---

## Further reading

- [Constitutive Model Calibration (PMDCo)](../../../simulation/model-calibration/PMDCo/README.md): the process that produces these parameters
- [Workflow example](../../../workflow/PMDCo/README.md): the full 4-step QA-to-FEM scenario
- [OO-LD primer](../../../../docs/2_oold-primer.md): how the schema format works
