# CALPHAD Simulation (ThermoCalc)

Records a **CALPHAD thermodynamic simulation activity** performed with
[Thermo-Calc](https://thermocalc.com/), following the
[OBI ComputerSimulation](http://purl.obolibrary.org/obo/OBI_0000471) class and
[PROV-O Activity](http://www.w3.org/ns/prov#Activity) for provenance.

<table>
<tr><td><strong>Version</strong></td><td><code>0.1.0</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>PMDCo + OBI + PROV-O + DCAT</td></tr>
<tr><td><strong>Extends</strong></td><td><code>process-step/PMDCo</code></td></tr>
<tr><td><strong>Includes</strong></td><td>none</td></tr>
<tr><td><strong>Transformers</strong></td><td>none</td></tr>
</table>

This schema extends `process-step/PMDCo` (via `allOf + $ref`) with ThermoCalc/CALPHAD-specific
fields: purpose, project, date, operator, alloy system, ThermoCalc version, thermodynamic
database, calculated property, and keywords.

---

## Fields

| Field | Required | Description |
|---|---|---|
| `label` | yes | Human-readable name for this simulation run |
| `purpose` | no | Why the simulation was run |
| `project` | no | IRI of the owning project |
| `date` | no | Execution date (YYYY-MM-DD) |
| `operator` | no | IRI of the responsible person |
| `alloy_system` | no | Alloy composition (e.g. "Al-Cu-Mg-Fe-Si-Ni") |
| `thermocalc_version` | no | ThermoCalc version (e.g. "2020a") |
| `thermodynamic_database` | no | Database used (e.g. "TCAL6", "TCFE12") |
| `calculated_property` | no | Property or diagram calculated |
| `keywords` | no | Descriptive keywords |
| `has_specified_input` | no | IRI(s) of input datasets |
| `has_specified_output` | no | IRI(s) of output datasets |
| `preceded_by` | no | IRI(s) of preceding simulation steps |

---

## Ontology mapping

```text
obi:0000471 + prov:Activity
  rdfs:label                     ── simulation name
  dcterms:description            ── purpose
  dcterms:isPartOf               ─► project IRI
  dcterms:created                ── date (xsd:date)
  prov:wasAssociatedWith         ─► person IRI(s)
  dcterms:subject                ── alloy system
  schema:softwareVersion         ── ThermoCalc version
  fairsim:thermoDB               ── thermodynamic database
  fairsim:calculatedProperty     ── calculated property
  dcat:keyword                   ── keywords
  obi:0000293 (hasInput)         ─► input dataset IRIs
  obi:0000299 (hasOutput)        ─► output dataset IRIs
  bfo:0000062 (preceded_by)      ─► preceding process IRIs
```

---

## Further reading

- [Usage guide](../../../../../../docs/6_usage-guide.md)
