# Schema: Microstructure Characterization (PMDCo)

OO-LD schema for microstructure characterization experiments using the PMDCo
OBI Assay pattern with CHAMEO instrument linkage.

## Graph pattern

```
Assay  (obi:OBI_0000070)
  rdfs:label                  experiment name
  has_specified_input  ────► Specimen KItem  [× 0..N]
  has_specified_output ────► Dataset KItem  [× 0..N]
  chameo:usesInstrument ───► Measurement Device KItem
  has_process_attribute ───► ParameterSpecification (PMD_0000013)  [× 0..N]
    rdfs:label         ────── parameter name
    qudt:value         ────── numeric value (xsd:double)
    qudt:hasUnit       ────── QUDT unit IRI
```

## Key fields

| Field | Predicate | Notes |
|-------|-----------|-------|
| `technique` | `rdf:type` | Enum: SEM, EBSD, LOM, TEM, SAXS, XRD, … |
| `measurement_device` | `chameo:usesInstrument` | Links to measurement-device KItem |
| `has_process_attribute` | `pmdco:PMD_0000009` | Magnification, voltage, area, preparation |

## Version

Current: **0.1.0** — see [CHANGELOG](CHANGELOG.md).

## Namespaces

- `pmdco:` `https://w3id.org/pmd/co/`
- `chameo:` `https://w3id.org/emmo/domain/characterisation-methodology/chameo#`
- `obi:` `http://purl.obolibrary.org/obo/OBI_`
