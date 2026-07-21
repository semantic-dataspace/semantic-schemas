# MD Simulation (LAMMPS)

Records a **molecular dynamics (MD) simulation activity** performed with
[LAMMPS](https://www.lammps.org/), following the
[OBI ComputerSimulation](http://purl.obolibrary.org/obo/OBI_0000471) class and
[PROV-O Activity](http://www.w3.org/ns/prov#Activity) for provenance.

<table>
<tr><td><strong>Version</strong></td><td><code>0.1.0</code></td></tr>
<tr><td><strong>Ontology pattern</strong></td><td>PMDCo + OBI + PROV-O + DCAT</td></tr>
<tr><td><strong>Extends</strong></td><td><code>process-step/PMDCo</code></td></tr>
<tr><td><strong>Includes</strong></td><td>none</td></tr>
<tr><td><strong>Transformers</strong></td><td>none</td></tr>
</table>

This schema extends `process-step/PMDCo` (via `allOf + $ref`) with LAMMPS/MD-specific
fields: purpose, project, date, operator, material system, LAMMPS version, force field,
atom count, temperature, timestep count, and keywords.

---

## Fields

| Field | Required | Description |
|---|---|---|
| `label` | yes | Human-readable name for this simulation run |
| `purpose` | no | Why the simulation was run |
| `project` | no | IRI of the owning project |
| `date` | no | Execution date (YYYY-MM-DD) |
| `operator` | no | IRI of the responsible person |
| `material_system` | no | Materials simulated (free text) |
| `lammps_version` | no | LAMMPS version string |
| `force_field` | no | Force field(s) used |
| `atom_count` | no | Number of atoms in the simulation box |
| `temperature_K` | no | Temperature in Kelvin |
| `timesteps` | no | Number of MD timesteps |
| `keywords` | no | Descriptive keywords |
| `has_specified_input` | no | IRI(s) of input datasets |
| `has_specified_output` | no | IRI(s) of output datasets |
| `preceded_by` | no | IRI(s) of preceding simulation steps |

---

## Ontology mapping

```text
obi:0000471 + prov:Activity
  rdfs:label                  ── simulation name
  dcterms:description         ── purpose
  dcterms:isPartOf            ─► project IRI
  dcterms:created             ── date (xsd:date)
  prov:wasAssociatedWith      ─► person IRI(s)
  dcterms:subject             ── material system
  schema:softwareVersion      ── LAMMPS version
  fairsim:forceField          ── force field
  fairsim:atomCount           ── atom count (xsd:integer)
  fairsim:temperature         ── temperature in K (xsd:double)
  fairsim:timesteps           ── timestep count (xsd:integer)
  dcat:keyword                ── keywords
  obi:0000293 (hasInput)      ─► input dataset IRIs
  obi:0000299 (hasOutput)     ─► output dataset IRIs
  bfo:0000062 (preceded_by)   ─► preceding process IRIs
```

---

## Further reading

- [Usage guide](../../../../../../docs/6_usage-guide.md)
