# LCA Assessment Run (PMDCo)

Records **one evaluation of a product system** by an LCA tool or service
(e.g. the MPPM service of Fraunhofer IWKS): which product system was evaluated,
with which background database and impact method, the recommended pathway and
the indicator results.

<table>
<tr><td><strong>Version</strong></td><td><code>0.1.0</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>OBI data transformation with embedded data items (same pattern as <code>characterization/generic/PMDCo</code>)</td></tr>
<tr><td><strong>Extends</strong></td><td>—</td></tr>
<tr><td><strong>Includes</strong></td><td>—</td></tr>
<tr><td><strong>Transformers</strong></td><td>— (MPPM response importer planned)</td></tr>
</table>

## Design

- Indicators (GWP, EBIT, SCE …) are **vocabulary terms**
  ([`Orchester/LCA/vocabularies/lca-indicator.ttl`](../../../../../Orchester/LCA/vocabularies/lca-indicator.ttl)),
  never hard-coded fields: different projects report different KPIs.
- Units: QUDT when one exists (`%`), otherwise kept as reported text
  (`kg CO2-eq`, `Euro`) in `uplci:unitText`.
- `best_value` stores MPPM's `maxValue` (best over all evaluated pathways) so
  dashboards can normalise bars.
- The unmodified service response can be attached as a `dataset` KItem
  (`raw_result_datasets`) for full provenance.

## Input fields

See [`docs/example.input.json`](docs/example.input.json) and
[`specs/schema.simplified.json`](specs/schema.simplified.json). Result entries
need only `name`, `value`, `unit`; known MPPM KPI names are mapped to indicators
automatically.
