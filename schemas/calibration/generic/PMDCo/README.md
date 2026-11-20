# Calibration Generic (PMDCo)

Records a **calibration event for a measurement instrument** following the
[CHAMEO ontology](https://w3id.org/emmo/domain/characterisation-methodology/chameo) and
[PMDCo](https://w3id.org/pmd/co/) scalar result pattern.

<table>
<tr><td><strong>Version</strong></td><td><code>0.1.0</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>CHAMEO chameo:Calibration</td></tr>
<tr><td><strong>Extends</strong></td><td>—</td></tr>
</table>

---

## Quick start

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "calibration_name": "Temperature Calibration — DSC300 Supreme — 2026-01-08",
  "calibration_type": "Temperature",
  "valid_from": "2026-01-08",
  "valid_until": "2026-07-08",
  "measurement_device": "https://example.org/devices/dsc300"
}
```

| Field | Required | Description |
|---|---|---|
| `calibration_name` | yes | Human-readable name for this calibration event |
| `calibration_type` | yes | Type: Temperature, Sensitivity, TauR, Load Cell, Displacement, Other |
| `valid_from` | yes | ISO 8601 date the calibration becomes valid |
| `valid_until` | no | ISO 8601 date the calibration expires (omit if open-ended) |
| `measurement_device` | no | IRI of the instrument KItem this calibration applies to |
| `reference_standards` | no | IRIs of reference material KItems used as standards |
| `conditions` | no | Calibration conditions (name, value, unit) |
| `results` | no | Accuracy claims (name, value, unit) |

---

## For the curious: how this maps to the ontology

```text
Calibration  (chameo:Calibration)
  rdfs:label            ──── calibration_name string
  dcterms:type          ──── calibration_type string
  schema:validFrom      ──── valid_from date (xsd:date)
  schema:validUntil     ──── valid_until date (optional)
  chameo:usesInstrument ──► measurement-device KItem IRI
  obi:0000293           ──► reference standard KItem IRI  [× 0..N]
  pmdco:PMD_0000009     ──► ParameterSpecification (pmdco:PMD_0000013)  [× 0..N]
  obi:OBI_0000299       ──► MeasurementDatum (iao:IAO_0000109)  [× 0..N]
    obi:OBI_0001938     ──► ScalarValueSpecification (obi:OBI_0001931)
      obi:OBI_0001937   ──── numeric value (xsd:double)
      iao:IAO_0000039   ──► unit IRI
```

---

## Further reading

See [`docs/6_usage-guide.md`](../../docs/6_usage-guide.md) for a full walkthrough.
