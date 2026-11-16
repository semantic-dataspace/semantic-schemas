# LCA Product System (PMDCo)

Records an **LCA product system** (ISO 14040 §3.28): the set of unit process
inventories that together deliver a functional unit, the inventory that
delivers it, the system boundary and the background database.

<table>
<tr><td><strong>Version</strong></td><td><code>0.2.0</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>IAO information content entity with <code>dcterms:hasPart</code> members</td></tr>
<tr><td><strong>Extends</strong></td><td>—</td></tr>
<tr><td><strong>Includes</strong></td><td>—</td></tr>
<tr><td><strong>Transformers</strong></td><td>—</td></tr>
</table>

## Design

- Members (`inventories`) and the reference inventory are **linked** KItems; one
  inventory can belong to several product systems (route variants, scenarios).
- **No link list is stored.** The chain is the graph of `provider` links on the
  member inventories' exchanges. Exporters (e.g. to MPPM) derive start/end
  processes and links via SPARQL; storing links once avoids contradictions.
- The `lca-product-system` KType is a context anchor, so the product system also
  scopes queries over its inventories, processes and materials.

## Input fields

See [`docs/example.input.json`](docs/example.input.json) (ORCHESTER Demo 3) and
[`specs/schema.simplified.json`](specs/schema.simplified.json).

| Field | Meaning |
|---|---|
| `system_name`, `description`, `goal` | Identity and purpose |
| `inventories` | Member unit process inventory IRIs |
| `reference_inventory` | Inventory delivering the functional unit (must be a member) |
| `reference_product` | Material KItem of the product |
| `functional_unit`, `reference_amount` | Text + quantity (e.g. 1 kg) |
| `system_boundary` | `cradle-to-gate` · `gate-to-gate` · `cradle-to-grave` · `cradle-to-cradle` |
| `background_database` | e.g. `ecoinvent-3.8-consequential` |
| `geography`, `modellers`, `owner`, `access_rights` | Context and provenance |

When the member inventories are loaded into the same graph, the shape also
warns about foreground providers that are not members of the system.
