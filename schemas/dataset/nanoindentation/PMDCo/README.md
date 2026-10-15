# Schema: Nanoindentation Dataset (PMDCo)

OO-LD schema for a single nanoindentation load-displacement dataset file,
extending the generic DCAT dataset pattern with per-indent scalar results.

## Graph pattern

```
Dataset  (dcat:Dataset)
  dcterms:title               dataset name
  dcterms:description         description (optional)
  indent_index                integer — indent number in experiment
  x_position / y_position     stage coordinates (mm)
  timestamp                   acquisition date-time
  has_specified_output ────► MeasurementDatum (IAO_0000109)  [× 0..N]
    rdfs:label         ────── result name (Hardness HIT, Elastic Modulus EIT, …)
    obi:OBI_0001938    ────► ScalarValueSpecification (OBI_0001931)
      obi:OBI_0001937  ────── numeric value (xsd:double)
      iao:IAO_0000039  ────── QUDT unit IRI
```

## Relationships

Parent experiment and specimen links are stored as DSMS `linked_kitems`
(not schema fields), so this schema captures only the measurement data content.

## Version

Current: **0.1.0** — see [CHANGELOG](CHANGELOG.md).
