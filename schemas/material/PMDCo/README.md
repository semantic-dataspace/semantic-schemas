# Material (PMDCo)

OO-LD schema for the abstract material identity node in the
[PMDCo duality pattern](https://github.com/materialdigital/core-ontology/tree/main/patterns/duality%20object%20material).

A **Material** KItem is the persistent, abstract identity of a substance — independent
of any specific specimen state or batch. Specimens link to it via `is_state_of`
(`PMD_0000070`); chemical compositions link to it via `quality_of` (`RO_0000080`).

## Graph pattern

```text
Material  (pmdco:PMD_0000000)
  rdfs:label                              name
  dcterms:title                           normative designation (e.g. AA2618-T6)
  dsms:hasMaterialClass                   Metal | Ceramic | Polymer | …
  dcterms:conformsTo                      material standard (e.g. EN 573-3)
  dcterms:identifier                      batch / lot ID
  schema:provider                         supplier name
  dsms:hasHeatTreatmentDescription        thermal processing history text
  rdfs:comment                            notes

  ◄── pmdco:PMD_0000070  Specimen KItems (is_state_of)
  ◄── obo:RO_0000080     ChemicalComposition quality nodes (quality_of)
```

## Key fields

| Field | Predicate | Notes |
|---|---|---|
| `label` | `rdfs:label` | Required |
| `material_designation` | `dcterms:title` | Normative name, e.g. `316L`, `AA2618` |
| `material_class` | `dsms:hasMaterialClass` | Enum: Metal / Ceramic / Polymer / Composite / Coating / Other |
| `material_standard` | `dcterms:conformsTo` | e.g. `EN 573-3`, `ASTM B209` |
| `batch_lot` | `dcterms:identifier` | Supplier batch/lot number |
| `supplier` | `schema:provider` | Supplier name |
| `heat_treatment` | `dsms:hasHeatTreatmentDescription` | Thermal processing history |
| `notes` | `rdfs:comment` | Free text |

<table>
<tr><td><strong>Version</strong></td><td><code>0.1.0</code></td></tr>
<tr><td><strong>Maturity</strong></td><td><code>draft</code></td></tr>
</table>

See [CHANGELOG](CHANGELOG.md) for history.

## Namespaces

| Prefix | IRI |
|---|---|
| `pmdco:` | `https://w3id.org/pmd/co/` |
| `dcterms:` | `http://purl.org/dc/terms/` |
| `schema:` | `https://schema.org/` |
| `dsms:` | `https://w3id.org/dsms/material#` |
| `obo:` | `http://purl.obolibrary.org/obo/` |
