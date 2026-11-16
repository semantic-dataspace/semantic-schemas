# Unit Process Inventory (PMDCo)

Records the **life cycle inventory (LCI) of one unit process**: every input and
output flow quantified per reference flow, the technology parameters behind
the numbers, where each number comes from, and who compiled the dataset.
Built on the [Platform MaterialDigital Core Ontology (PMDCo)](https://w3id.org/pmd/co/)
/ OBI / IAO, with LCA-specific terms from the DSMS UPLCI vocabulary
([`Orchester/LCA/vocabularies/dsms-uplci.ttl`](../../../../../Orchester/LCA/vocabularies/dsms-uplci.ttl)).

<table>
<tr><td><strong>Version</strong></td><td><code>0.1.0</code></td></tr>
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
   ├─ name, description, location code, date of compilation, access rights, data owner
   ├─ inputs[]  ──► Exchange: name · category · value · unit · description · reference · supplied by
   ├─ outputs[] ──► Exchange: name · category · reference flow ✓ · value · unit · description · reference
   └─ technology parameters[] ──► name · category · value · unit · description · reference
```

**Minimal profile:** exactly the data the MPPM service consumes, plus the links
DSMS needs (process, "supplied by" for the chain, data owner) and access rights.
Process chains follow from the "supplied by" links between inventories.

## Input fields

Copy [`docs/example.input.json`](docs/example.input.json) (Demo 3 sintering and
annealing step). Field reference: [`specs/schema.simplified.json`](specs/schema.simplified.json).

| Field | Meaning |
|---|---|
| `inventory_name`, `description` | Name and scope of the dataset |
| `process` | IRI of the manufacturing-process KItem described |
| `geography` | Location code (DE, RER, GLO) |
| `date_compiled` | Dataset version date |
| `access_rights` | `public` · `restricted` · `confidential` |
| `data_owner` | Organisation IRI |
| `inputs[]` | `name`, `category` (material · energy · personnel · service), `value`, `unit`, `description`, `reference`, `provider` |
| `outputs[]` | `name`, `category` (product · co_product · waste · emission · other), `value`, `unit`, `description`, `reference`, `is_reference_flow` |
| `parameters[]` | `name`, `category` (facility · process · operation), `value`, `unit`, `description`, `reference` |

Unit symbols such as `kg`, `kWh`, `MJ`, `h`, `%`, `l/h`, `piece` are mapped to
QUDT automatically; CURIEs (`uqudt:KiloGM`) and IRIs are passed through.

## Validation highlights (`specs/shape.ttl`)

- exactly one reference flow, which is a product or valuable by-product
- input/output categories match the flow direction
- unit plausible for the category (catches e.g. electricity recorded in `kg`)
- flows are nodes, not text
- warning: inventory not linked to its process

## Vocabularies used

| Field | Source |
|---|---|
| units | `measurement-unit` vocabulary service namespace (QUDT) |
| categories | closed lists in [`Orchester/LCA/vocabularies/dsms-uplci.ttl`](../../../../../Orchester/LCA/vocabularies/dsms-uplci.ttl) |
| access rights | [EU access-right NAL](http://publications.europa.eu/resource/authority/access-right) |
