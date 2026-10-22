# DSC Dataset (PMDCo)

Records metadata for a **DSC heat-flow dataset** produced by a NETZSCH Proteus
instrument. Captures instrument provenance, measurement conditions, and column
semantic annotations for the timeseries data.

<table>
<tr><td><strong>Version</strong></td><td><code>0.1.0</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>PMDCo / DCAT dataset</td></tr>
<tr><td><strong>Extends</strong></td><td>—</td></tr>
</table>

---

## Quick start

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values.

| Field | Required | Description |
|---|---|---|
| `dataset_name` | yes | Human-readable name for this dataset |
| `sample_name` | yes | Sample/material name as recorded by the instrument |
| `sample_mass_mg` | yes | Sample mass in mg |
| `manufacturer` | yes | Instrument manufacturer |
| `instrument_model` | yes | Instrument model name |
| `measurement_datetime` | yes | ISO 8601 datetime of measurement |
| `heating_rate_k_min` | yes | Heating rate in K/min |
| `temperature_start_degC` | yes | Start temperature in °C |
| `temperature_end_degC` | yes | End temperature in °C |
| `purge_gas` | no | Purge gas description |
| `purge_gas_flow_rate_ml_min` | no | Purge gas flow rate in ml/min |
| `laboratory` | no | Laboratory identifier |
| `operator` | no | Operator name or initials |

---

## Further reading

See [`docs/6_usage-guide.md`](../../docs/6_usage-guide.md) for a full walkthrough.
