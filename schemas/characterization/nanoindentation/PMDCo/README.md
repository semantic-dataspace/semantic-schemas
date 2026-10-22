# Characterization Nanoindentation (PMDCo)

Records a **nanoindentation characterization experiment** following the
[CHAMEO ontology](https://w3id.org/emmo/domain/characterisation-methodology/chameo) and
[PMDCo](https://w3id.org/pmd/co/) measurement pattern.

<table>
<tr><td><strong>Version</strong></td><td><code>0.2.0</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>CHAMEO chameo:Nanoindentation</td></tr>
<tr><td><strong>Extends</strong></td><td><a href="../../generic/PMDCo/">characterization/generic/PMDCo</a></td></tr>
</table>

---

## Quick start

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values.

| Field | Required | Description |
|---|---|---|
| `step_name` | yes | Human-readable name for this experiment |
| `inputs` | no | IRIs of nanoindentation specimen KItems |
| `outputs` | no | IRIs of dataset KItems produced |
| `conditions` | no | Test conditions (name, value, unit) |
| `results` | no | Summary results: mean HIT, EIT, etc. (name, value, unit) |

---

## Further reading

See [`docs/6_usage-guide.md`](../../docs/6_usage-guide.md) for a full walkthrough.
