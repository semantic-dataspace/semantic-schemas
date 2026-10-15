# Schema: Heat Treatment Process (PMDCo)

OO-LD schema for a heat treatment manufacturing step, using the PMDCo
ManufacturingProcess pattern with DSMS heat-treatment vocabulary extensions.

## Graph pattern

```
HeatTreatmentProcess  (pmdco:PMD_0000833 + dsmsht:<Subtype>)
  rdfs:label                  process name
  rdfs:comment                description (optional)
  has_specified_input  ────► Specimen / Material KItem  [× 0..N]
  has_specified_output ────► Specimen KItem  [× 0..N]
  preceded_by          ────► Process KItem  [× 0..N]
  has_process_attribute ───► ParameterSpecification (PMD_0000013)  [× 0..N]
    rdf:type           ────── dsmsht:<ParameterClass> IRI (from vocabulary)
    rdfs:label         ────── human-readable parameter name
    qudt:value         ────── numeric value (xsd:double)
    qudt:hasUnit       ────── QUDT unit IRI
```

## Key fields

| Field | Predicate | Notes |
|-------|-----------|-------|
| `heat_treatment_type` | `rdf:type` (on root node) | Drives `dsmsht:<Subtype>` IRI |
| `has_process_attribute` | `pmdco:PMD_0000009` | Array of ParameterSpecification nodes |
| `parameter_type` | `rdf:type` | Vocabulary IRI — enables SPARQL filtering by parameter class |
| `parameter_unit` | `qudt:hasUnit` | QUDT unit IRI from vocabulary service |

## Version

Current: **0.2.0** — see [CHANGELOG](CHANGELOG.md).

## Namespaces

- `pmdco:` `https://w3id.org/pmd/co/`
- `dsmsht:` `https://w3id.org/dsms/heattreatment#`
- `qudt:` `http://qudt.org/schema/qudt/`
