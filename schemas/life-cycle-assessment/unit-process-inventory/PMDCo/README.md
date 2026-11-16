# Unit Process Inventory (PMDCo)

Records the **life cycle inventory (LCI) of one unit process**: every input and
output flow quantified per reference flow, the technology parameters behind
the numbers, where each number comes from, and who compiled the dataset.
Built on the [Platform MaterialDigital Core Ontology (PMDCo)](https://w3id.org/pmd/co/)
/ OBI / IAO, with LCA-specific terms from the DSMS UPLCI vocabulary
([`Orchester/LCA/vocabularies/dsms-uplci.ttl`](../../../../../Orchester/LCA/vocabularies/dsms-uplci.ttl)).

<table>
<tr><td><strong>Version</strong></td><td><code>0.2.0</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>
IAO information content entity <em>is about</em> a
<a href="https://github.com/materialdigital/core-ontology/tree/main/patterns/input%20and%20output%20of%20processes">PMDCo process</a>;
embedded data items with QUDT values
</td></tr>
<tr><td><strong>Extends</strong></td><td>—</td></tr>
<tr><td><strong>Includes</strong></td><td>—</td></tr>
<tr><td><strong>Transformers</strong></td><td>— (LCI template 2023 Excel importer planned)</td></tr>
</table>

## What it represents

An inventory is **information about** a manufacturing process, not the process
itself. Its numbers are normalised to a reference flow and are often
calculated or estimated, so they are modelled as data items, while the physical
process and materials remain PMDCo entities in their own KItems.

```text
UnitProcessInventory ──is about──► ManufacturingProcess KItem
   ├─ hasInput / hasOutput ──► Exchange
   │     category        material | energy | personnel | service | natural resource
   │                     product | co-product | waste | emission | other
   │     flow type       lci-flow vocabulary (Electricity, Argon …)
   │     material        Material KItem (tracked intermediate / final products)
   │     amount          qudt:value + qudt:hasUnit
   │     reference flow  exactly one product output
   │     data derivation measured | calculated | estimated | assumption | …
   │     provider        foreground inventory  OR  background dataset (ecoinvent)
   │     cost, CO2       per unit of flow (flat fields)
   └─ hasTechnologyParameter ──► ParameterSpecification (facility | process | operation)
```

Process chains are not stored separately: they follow from the `provider` links
between inventories (input of B → inventory A that produces it).

## Input fields

Copy [`docs/example.input.json`](docs/example.input.json) (Demo 3 sintering and
annealing step) and fill in your values. Field reference:
[`specs/schema.simplified.json`](specs/schema.simplified.json).

| Field | Meaning |
|---|---|
| `inventory_name`, `description` | Name and scope of the dataset |
| `process` | IRI of the manufacturing-process KItem described |
| `geography`, `site` | ISO country / ecoinvent region, plant location |
| `date_compiled`, `valid_until` | Compilation date, validity year |
| `access_rights` | `public` · `restricted` · `confidential` |
| `trl`, `data_generators`, `data_owner`, `reviewers`, `source` | Provenance |
| `inputs[]`, `outputs[]` | Exchanges, see below |
| `parameters[]` | Technology parameters (`facility` · `process` · `operation`) |

Exchange keys: `name`, `category`, `value`, `unit` (required); `flow_object`,
`material`, `description`, `data_source`, `source_note`, `scaling_slope`,
`scaling_base`, `provider` *or* `background_provider{database, activity_name, …}`,
`monetary_value`, `currency`, `monetary_value_source`, `climate_change`, `climate_change_source`,
`is_reference_flow` (outputs).

Unit symbols such as `kg`, `kWh`, `MJ`, `h`, `%`, `l/h`, `piece` are mapped to
QUDT automatically; CURIEs (`uqudt:KiloGM`) and IRIs are passed through.

## Validation highlights (`specs/shape.ttl`)

- exactly one reference flow, which is a product or co-product output
- input/output categories match the exchange direction
- unit plausible for the category (catches e.g. electricity recorded in `kg`)
- monetary flow properties carry a currency
- foreground and background provider not both set
- warnings: inventory not linked to its process; amount without data derivation

## Vocabularies used

| Field | Vocabulary service namespace / source |
|---|---|
| `flow_object` | `lci-flow` ([`Orchester/LCA/vocabularies/lci-flow.ttl`](../../../../../Orchester/LCA/vocabularies/lci-flow.ttl)) |
| `parameter_type` | `lci-parameter` ([`Orchester/LCA/vocabularies/lci-parameter.ttl`](../../../../../Orchester/LCA/vocabularies/lci-parameter.ttl)) |
| units | `measurement-unit` (QUDT) |
| categories, data derivation, databases | closed lists in `dsms-uplci.ttl` |
| access rights | [EU access-right NAL](http://publications.europa.eu/resource/authority/access-right) |
